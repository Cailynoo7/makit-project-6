#!/usr/bin/env python3
"""Offline commissioning calculations; no hardware, no serial, no automatic calibration writes."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import sys

SOURCE = Path(__file__).resolve().parents[1] / "helicopter_controller"
PROBES = ("COB", "SHELL", "BAT")

def config():
    text = (SOURCE / "ControlConfig.h").read_text()
    def number(key):
        m = re.search(r"\b" + key + r"\s*=\s*(-?[0-9.]+)", text)
        if not m:
            raise ValueError("Cannot parse constant: " + key)
        return float(m.group(1))
    def array(key):
        m = re.search(r"\b" + key + r"\[3\]\s*=\s*\{([^}]+)\}", text)
        if not m:
            raise ValueError("Cannot parse array: " + key)
        return [float(x.strip().rstrip("fF")) for x in m.group(1).split(",")]
    return {**{key: number(key) for key in ("kNtcSupplyV", "kNtcPullupOhm", "kNtcR25Ohm",
             "kNtcBeta", "kAdcLsbV", "kBatteryDividerGain", "kLightMaxPermille",
             "kMinimumThermalPermille")},
            **{key: array(key) for key in ("kDimC", "kTripC", "kRecoverC", "kTempOffsetsC")}}

def numeric_code(s):
    value = int(str(s), 16) if str(s).lower().startswith("0x") else int(str(s))
    if not -32768 <= value <= 65535:
        raise ValueError("ADC code outside signed16/unsigned16 range")
    return value - 65536 if value > 32767 else value

def temperature(raw, p, cfg, with_offset=True):
    raw = numeric_code(raw)
    v = raw * cfg["kAdcLsbV"]
    if raw <= 0 or v <= 0.04 or v >= cfg["kNtcSupplyV"] - 0.10:
        raise ValueError("NTC rail fault")
    r = cfg["kNtcPullupOhm"] * v / (cfg["kNtcSupplyV"] - v)
    c = 1 / (1/298.15 + math.log(r/cfg["kNtcR25Ohm"])/cfg["kNtcBeta"]) - 273.15
    if with_offset:
        c += cfg["kTempOffsetsC"][PROBES.index(p)]
    if not math.isfinite(c) or c < -20 or c > 110:
        raise ValueError("Temperature outside firmware plausibility range")
    return c

def threshold_rows(cfg):
    for i, probe in enumerate(PROBES):
        dim, trip, recover = (cfg[k][i] for k in ("kDimC", "kTripC", "kRecoverC"))
        for label, c in (("baseline",25+cfg["kTempOffsetsC"][i]),("recover",recover),
                         ("below_dim",dim-0.5),("dim",dim),("mid_dim",(dim+trip)/2),
                         ("below_trip",trip-0.5),("above_trip",trip+0.5)):
            physical = c - cfg["kTempOffsetsC"][i]
            r = cfg["kNtcR25Ohm"] * math.exp(cfg["kNtcBeta"]*(1/(physical+273.15)-1/298.15))
            v = cfg["kNtcSupplyV"]*r/(cfg["kNtcPullupOhm"]+r)
            parallel = 1/(1/r-1/10000) if r < 9999.999 else None
            max_duty = cfg["kLightMaxPermille"]
            duty = 0 if c >= trip else int(max_duty*(1-(max(0,c-dim)/(trip-dim))*
                    (1000-cfg["kMinimumThermalPermille"])/1000))
            yield {"probe":probe,"point":label,"display_C":round(c,3),"ntc_ohm":round(r,2),
                   "parallel_to_fixed_10k_ohm":round(parallel,2) if parallel else "",
                   "node_V":round(v,6),"raw_code_approx":round(v/cfg["kAdcLsbV"]),
                   "nominal_running_light_permille":duty}

def calibrate(path, cfg, margin):
    points = {p: [] for p in PROBES}
    for row in csv.DictReader(path.open(newline="", encoding="utf-8-sig")):
        if not row.get("raw_code","").strip() or not row.get("reference_C","").strip():
            continue
        p = row["probe"].strip().upper()
        if p not in points:
            raise ValueError("Unknown probe " + p)
        if row.get("stable","").strip().lower() != "yes":
            continue
        base = temperature(row["raw_code"],p,cfg,with_offset=False)
        ref = float(row["reference_C"])
        if not math.isfinite(ref):
            raise ValueError("Non-finite reference temperature")
        rail_text = row.get("rail_V","").strip()
        rail = float(rail_text) if rail_text else None
        if rail is not None and (not math.isfinite(rail) or not 2.9 <= rail <= 3.6):
            raise ValueError("Invalid measured3V3 rail")
        points[p].append((base,ref,rail,row.get("stage","")))
    result = {}
    for p, data in points.items():
        if not data:
            result[p] = {"status":"no_measurements","candidate_offset_C":None}
            continue
        delta = [ref-base for base,ref,_,_ in data]
        offset = max(0.0,max(delta)+margin)
        residual = [base+offset-ref for base,ref,_,_ in data]
        warnings = []
        if len(data)<3 or max(x[1] for x in data)-min(x[1] for x in data)<10:
            warnings.append("Need >=3 stable points spanning >=10C")
        stages = {x[3] for x in data}
        if not {"electrical","installed"}.issubset(stages):
            warnings.append("Both electrical and installed calibration data required")
        for stage in ("electrical", "installed"):
            group = [x for x in data if x[3] == stage]
            if len(group) < 3:
                warnings.append(stage + ": need >=3 stable points")
            elif max(x[1] for x in group) - min(x[1] for x in group) < 10:
                warnings.append(stage + ": measured coverage below10C; do not claim full range")
        if offset>5:
            warnings.append("Required offset>5C: inspect thermal contact; do not apply automatically")
        if max(delta)-min(delta)>2 or max(residual)>2:
            warnings.append("One constant offset cannot meet +/-2C commissioning target")
        if any(rail is not None and abs(rail-cfg["kNtcSupplyV"])>0.03 for _,_,rail,_ in data):
            warnings.append("Calibrate measured NTC supply first and repeat calculations")
        result[p] = {"status":"review_required" if warnings else "candidate_only",
                     "points":len(data),"candidate_offset_C":round(offset,3),
                     "residual_overread_C":[round(min(residual),3),round(max(residual),3)],
                     "warnings":warnings}
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("thresholds")
    read=sub.add_parser("reading")
    read.add_argument("--probe",choices=PROBES+("VBAT",),required=True)
    read.add_argument("--raw",required=True)
    cal=sub.add_parser("calibrate")
    cal.add_argument("csv",type=Path)
    cal.add_argument("--margin",type=float,default=0.5)
    limited=sub.add_parser("limited-build")
    limited.add_argument("destination",type=Path,help="New/nonexistent sketch folder named helicopter_controller")
    args=parser.parse_args()
    cfg=config()
    if args.command=="thresholds":
        rows=list(threshold_rows(cfg))
        writer=csv.DictWriter(sys.stdout,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)
    elif args.command=="reading":
        raw=numeric_code(args.raw)
        result={"probe":args.probe,"signed_code":raw,"input_V":raw*cfg["kAdcLsbV"]}
        if args.probe=="VBAT":
            if raw<=0:
                raise ValueError("Invalid battery ADC code")
            result["battery_V"]=raw*cfg["kAdcLsbV"]*cfg["kBatteryDividerGain"]
        else:
            result["temperature_C"]=temperature(args.raw,args.probe,cfg)
        print(json.dumps(result,indent=2))
    elif args.command=="calibrate":
        if not math.isfinite(args.margin) or not 0<=args.margin<=2:
            raise ValueError("Margin must be0..2C")
        print(json.dumps(calibrate(args.csv,cfg,args.margin),indent=2))
    else:
        dest=args.destination
        if dest.name!="helicopter_controller" or dest.exists():
            raise ValueError("Choose a new folder named helicopter_controller; existing work is never overwritten")
        dest.mkdir(parents=True)
        for source in SOURCE.iterdir():
            if source.suffix in (".h",".ino"):
                shutil.copy2(source,dest/source.name)
        p=dest/"ControlConfig.h"
        text=p.read_text()
        changed,n=re.subn(r"\bkLightMaxPermille\s*=\s*[0-9]+", "kLightMaxPermille=500",text)
        if n!=1:
            raise ValueError("Expected exactly one light limit")
        p.write_text(changed)
        print(json.dumps({"test_only":True,"sketch":str(dest),
              "difference":"kLightMaxPermille=500 only;50ms startup remains full HIGH",
              "production_config_sha256":hashlib.sha256((SOURCE/"ControlConfig.h").read_bytes()).hexdigest()},indent=2))

if __name__=="__main__":
    try:
        main()
    except (ValueError,KeyError,OSError) as exc:
        print("ERROR: "+str(exc),file=sys.stderr)
        sys.exit(2)
