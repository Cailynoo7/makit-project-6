"""Project aluminium drawings, derived only from the final CAD handoff STEP."""
import argparse
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / "Library/Application Support/Makit/codex/skills/engineering-drawing/scripts"))
from build123d import import_step
from eng_drawing import Sheet, write_pdf

ROOT=Path(__file__).resolve().parents[3]
PARTS=[
("AL01","heat_spreader","COB COLLECTOR"),
("AL02","thermal_bridge_left","LEFT THERMAL BRIDGE"),
("AL03","thermal_bridge_right","RIGHT THERMAL BRIDGE"),
("AL04","upper_heat_link_left","LEFT UPPER HEAT LINK"),
("AL05","upper_heat_link_right","RIGHT UPPER HEAT LINK"),
("AL06","thermal_fore_shoe_left","LEFT FORE CONTACT SHOE"),
("AL07","thermal_fore_shoe_right","RIGHT FORE CONTACT SHOE"),
("AL08","thermal_aft_shoe_left","LEFT AFT CONTACT SHOE"),
("AL09","thermal_aft_shoe_right","RIGHT AFT CONTACT SHOE"),
("AL10","liner_left","LEFT FORE SHELL LINER"),
("AL11","liner_right","RIGHT FORE SHELL LINER"),
("AL12","liner_aft_left","LEFT AFT SHELL LINER"),
("AL13","liner_aft_right","RIGHT AFT SHELL LINER"),
("AL14","cap_liner_left","LEFT CAP LINER"),
("AL15","cap_liner_right","RIGHT CAP LINER"),
]
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--step",required=True,type=Path)
 ap.add_argument("--revision",required=True)
 a=ap.parse_args()
 source=a.step.resolve()
 if not source.is_relative_to(ROOT/"manufacturing/helicopter/releases"):
  raise ValueError("Use the exact CAD handoff STEP in this project")
 assembly=import_step(str(source))
 by_id={p.label:p for p in assembly.children}
 if not all(pid in by_id for _,pid,_ in PARTS):
  raise ValueError("Expected fifteen named aluminium objects in this handoff")
 sheets=[];index=[]
 for number,pid,title in PARTS:
  p=by_id[pid];box=p.bounding_box()
  small=max(box.size)<30
  liner="liner" in pid
  notes=[
   "NOMINAL3D PROFILE FROM SAME REVISION STEP; DO NOT SCALE PAPER.",
   "LINEAR +/-0.10; HOLE POSITIONS +/-0.05 UNLESS MARKED.",
   "CONTACT SIZE +/-0.05; PLANAR CONTACT FLATNESS0.05.",
   "FITTING PROFILE:0.10 MAX MATERIAL REMOVAL FROM STEP.",
   "EDGE BREAK0.10-0.20; LIGHT DEBURR ONLY ON THIN LINER RIMS.",
  ]
  if liner:
   notes += ["FORMED SPHERICAL SHEET; NOT A DEVELOPABLE FLAT PATTERN.",
    "R OUT<=47.45; R IN>=46.95; NOM T0.50; MIN FORMED T0.40.",
    "FORM ON TOOL, THEN TRIM; DRY FIT TO ACTUAL PRINTED SHELL."]
  elif "shoe" in pid:
   notes += ["TAP M1.6x0.35-6H THRU AFTER1.25 DRILL.",
             "SPHERICAL CONTACT R46.85 PER STEP; HAND-TIGHTEN SHALLOW THREAD."]
  elif pid=="heat_spreader":
   notes += ["TAP2xM2x0.4-6H THRU AFTER1.60 DRILL; KEEP COB LAND FLAT.",
             "COB BOND LAND12x12; NO GLUE OR BURRS ON OPTICAL FACE."]
  elif "bridge" in pid:
   notes += ["WIRE EXIT CHANNEL R4.00; KEEP LOWER WEB INTACT.",
             "TWO CLEARANCE HOLES1.90; CBORE3.40x1.70 AT TOP.",
             "ROOT SLOT6.40x2.40; SIDE RELIEF8.40x4.40 PER STEP."]
  else:
   notes += ["LOWER LAP Z26.10; SEPARABLE0.10 THERMAL INTERFACE.",
             "SPHERICAL CAP FOOT R46.85; DO NOT GLUE LOWER SPLIT LAP."]
  sheet=Sheet("A3",scale=3 if small else 1.5,title=title,part_number=number,
              material="1050/1060 ALUMINIUM",revision=a.revision[:8],
              author="Makit",notes=notes,text_height=3.0)
  top=sheet.view(p,"top",at=(145,235))
  front=sheet.view(p,"front",at=(145,140))
  right=sheet.view(p,"right",at=(265,140))
  iso=sheet.view(p,"iso",at=(330,232),label="ISOMETRIC (2:1)" if small else "ISOMETRIC (1:1)",scale=2 if small else 1)
  front.overall()
  verts=list(p.vertices())
  lo=min(verts,key=lambda v:v.Y).center()
  hi=max(verts,key=lambda v:v.Y).center()
  if (hi-lo).length>1e-5:top.dim(lo,hi,orientation="v",side="left")
  if pid=="heat_spreader":
   top.hole((-28,14.5,3),2,thru=True,thread="M2x0.4-6H",count=2,angle=45)
   top.hole((-23,-10.5,3),1.9,thru=True,count=2,angle=-45)
   top.dim((-28,-14.5,3),(-28,14.5,3),orientation="v",side="right")
  elif "bridge" in pid:
   side=-1 if pid.endswith("right") else 1
   top.hole((27,side*24.5,24),1.9,thru=True,cbore=(3.4,1.7),count=2,angle=45)
   top.dim((-28,side*24,24),(27,side*24.5,24),orientation="h",side="top")
  elif "shoe" in pid:
   side=-1 if pid.endswith("right") else 1
   x,y=(-28,24) if "fore" in pid else (27,24.5)
   top.hole((x,side*y,13.9),1.6,thru=True,thread="M1.6x0.35-6H",angle=45)
  sheets.append(sheet)
  index.append({"part_number":number,"object_id":pid,"quantity":1,
                "bbox_min_mm":list(box.min),"bbox_max_mm":list(box.max),
                "volume_mm3":p.volume,"sheet":len(sheets)})
 out=ROOT/"manufacturing/helicopter/drawing"
 out.mkdir(parents=True,exist_ok=True)
 write_pdf(sheets,out/"helicopter-aluminium-drawing.pdf")
 (out/"drawing-index.json").write_text(json.dumps({
    "source_step":str(source.relative_to(ROOT)),
    "source_step_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),
    "cad_revision":a.revision,"units":"mm","projection":"THIRD ANGLE",
    "parts":index,"limitations":"Orthographic and hidden-line views;no sections. STEP defines remaining complex surfaces."},
    indent=2)+"\n")
 machining_source=ROOT/"product/铝件加工说明.md"
 (out/"machining-notes.md").write_text(machining_source.read_text())
 import csv
 with (out/"part-inspection-list.csv").open("w",newline="")as f:
  writer=csv.writer(f)
  writer.writerow(["part_number","object_id","quantity","drawing_sheet","bbox_X_mm","bbox_Y_mm","bbox_Z_mm","volume_mm3","first_article_result"])
  for row in index:
   sizes=[row["bbox_max_mm"][i]-row["bbox_min_mm"][i]for i in range(3)]
   writer.writerow([row["part_number"],row["object_id"],1,row["sheet"],*[round(v,4)for v in sizes],round(row["volume_mm3"],4),""])
 print("15 aluminium drawings, machining notes and blank first-article list generated from final STEP")
if __name__=="__main__":main()
