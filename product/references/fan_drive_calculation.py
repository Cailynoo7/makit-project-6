"""Preliminary annular BEM + motor operating-point calculation, SI units.
Run from project root. Aerodynamic coefficients are assumptions, NOT measurements.
No CFD, structural certification, desktop air-speed or acoustic prediction.
"""
import json, math
from pathlib import Path
PI=math.pi
R, ROOT, RC, AR, CHORD, PITCH, BLADES=.125,.01625,.06875,.05625,.0375,math.radians(12),4
RHO=1.2
# Exact committed CAD geometric inertia mm^5, converted using solid PETG density.
INERTIA=120900741.49420139*1250*1e-15
RATIO=30/8
SCENARIOS={
 'low_load':dict(lift_slope=6,cd0=.03,belt_eff=.85,friction=.0002,ceiling=1),
 'nominal':dict(lift_slope=4.5,cd0=.08,belt_eff=.75,friction=.0005,ceiling=1.2),
 'high_load':dict(lift_slope=3,cd0=.15,belt_eff=.60,friction=.001,ceiling=1.5),
}
def rotor(n,s):
    omega=n*2*PI/60; thrust=torque=flow=area=0
    dr=(R-ROOT)/180
    for i in range(180):
        r=ROOT+(i+.5)*dr
        c=CHORD*math.sqrt(max(0,1-((r-RC)/AR)**2))
        if c==0: continue
        def terms(phi):
            cl=max(-1.2,min(1.2,s['lift_slope']*(PITCH-phi)))
            cd=s['cd0']+.1*cl*cl
            F=2/PI*math.acos(math.exp(-BLADES*(R-r)/(2*r*max(1e-8,math.sin(phi)))))
            cn=cl*math.cos(phi)-cd*math.sin(phi)
            return cl,cd,F,cn
        lo,hi=1e-8,PITCH
        for _ in range(45):
            phi=(lo+hi)/2;cl,cd,F,cn=terms(phi)
            if .5*BLADES*c*cn/math.cos(phi)**2-4*PI*F*r*math.tan(phi)**2>0:lo=phi
            else:hi=phi
        phi=(lo+hi)/2;cl,cd,F,cn=terms(phi)
        vi=omega*r*math.tan(phi);v2=(omega*r)**2+vi*vi
        thrust+=.5*RHO*BLADES*c*v2*cn*dr
        torque+=.5*RHO*BLADES*c*v2*(cl*math.sin(phi)+cd*math.cos(phi))*r*dr
        if r>=.05: flow+=vi*2*PI*r*dr;area+=2*PI*r*dr
    return dict(torque_Nm=torque,power_W=torque*omega,thrust_N=thrust,annular_induced_ms=flow/area)
def operating_point(battery,duty,s,motor='3060',rd=.56,speed_factor=1):
    if motor=='3060':vr,nr,ts,ir,i0=6,6500,.9*.00980665,1.5,.17
    else:vr,nr,ts,ir,i0=3,3700,.00191,.30,.018;rd=.08
    # DC equivalent PWM approximation; slow-decay brake PWM; current ripple makes actual result differ.
    # n0/torque scale with voltage; i0 is conservatively held constant.
    loadk=rotor(600,s)['torque_Nm']/600**2*s['ceiling']
    def calc(n):
        q=loadk*n*n+s['friction']
        qm=q/(RATIO*s['belt_eff'])
        current=i0+qm/(ts/(ir-i0))
        v=max(.01,battery*duty-current*rd)
        n0=nr*v/vr*speed_factor
        available=ts*v/vr*max(0,1-n*RATIO/n0)*RATIO*s['belt_eff']
        return available-q,current,v,q
    lo,hi=0,nr*battery/vr/RATIO*speed_factor
    for _ in range(60):
        n=(lo+hi)/2
        if calc(n)[0]>0:lo=n
        else:hi=n
    n=(lo+hi)/2;_,current,v,q=calc(n)
    return dict(rotor_rpm=round(n,1),motor_output_rpm=round(n*RATIO,1),winding_current_A=round(current,3),motor_equiv_V=round(v,3),rotor_load_mNm=round(q*1000,3),rotor_power_W=round(q*n*2*PI/60,3))
def startup(battery,s,duty=.60):
    # Approximate conservative lumped inertia, limit at divider's nominal threshold.
    kt=(.9*.00980665)/(1.5-.17);limit=battery*22000/172000/(4990*205e-6)
    n0=6500*battery*duty/6/RATIO
    omega=0;dt=.001;end=operating_point(battery,duty,s)['rotor_rpm']*.9*2*PI/60
    k=rotor(600,s)['torque_Nm']/600**2*s['ceiling']
    for i in range(10000):
        n=omega*60/(2*PI)
        qload=k*n*n+s['friction']
        # Available average voltage model, current limited; saturates at start.
        q0=.9*.00980665*battery*duty/6*max(0,1-n/n0)
        qmotor=min(q0,max(0,limit-.17)*kt)
        omega=max(0,omega+(qmotor*RATIO*s['belt_eff']-qload)/INERTIA*dt)
        if omega>=end:return round((i+1)*dt,3)
    return None
def main():
    D,d,C=30,8,23
    alpha=math.asin((D-d)/(2*C))
    belt=2*math.sqrt(C*C-((D-d)/2)**2)+(PI+2*alpha)*D/2+(PI-2*alpha)*d/2
    result={'status':'preliminary_theory_only','geometry':{'rotor_diameter_mm':250,'blade_thickness_mm':1.6,'maximum_chord_mm':37.5,'pitch_deg':12,'solid_PETG_density_kg_m3_default':1250,'rotor_inertia_kg_m2':INERTIA},
      'assumptions':SCENARIOS,'motor':{'selected':'Pololu3060 5:1 HPCB6V no encoder','rated_output_n0_rpm':6500,'rated_stall_current_A_extrapolated':1.5,'rated_stall_torque_Nm_extrapolated':.9*.00980665,'speed_tolerance_fraction':.2,'noload_current_A_conservative':.17,'manufacturer_continuous_current_guideline_A':.375,'driver_path_resistance_ohm_conservative':.56},
      'transmission':{'belt_reduction':RATIO,'gearbox_reduction':4.995,'total_reduction':RATIO*4.995,'pitch_length_mm':belt,'free_neutral_length_mm':PI*33.5,'stretch_percent':100*(belt/(PI*33.5)-1),'small_pulley_wrap_deg':180-2*math.degrees(alpha),'belt_ID_mm':32,'tension_adjustment_mm':[-.3,.3],'traction_assumptions_source':'default sensitivity only, not measured EPDM data','traction':{name:{'modulus_MPa':E,'friction_coefficient':mu,'preload_per_span_N':E*PI*.75**2*(belt/(PI*33.5)-1),'driven_torque_capacity_mNm':2*E*PI*.75**2*(belt/(PI*33.5)-1)*math.tanh(mu*(PI-2*alpha)/2)*15,'approx_motor_radial_load_N':2*E*PI*.75**2*(belt/(PI*33.5)-1)} for name,E,mu in [('low',3,.3),('nominal',5,.5),('high',10,.7)]}},
      'rotor_only_nominal':{str(n):rotor(n,SCENARIOS['nominal']) for n in [500,600,700,800]},
      'old_RF300_full_duty':{str(v):{k:operating_point(v,1,s,'RF300') for k,s in SCENARIOS.items()} for v in [3.3,3.7,4.2]},
      'selected_initial_60_percent':{str(v):{k:operating_point(v,.60,s) for k,s in SCENARIOS.items()} for v in [2.8,3.3,3.7,4.2]},
      'selected_full_duty_unqualified':{str(v):{k:operating_point(v,1,s) for k,s in SCENARIOS.items()} for v in [3.3,3.7,4.2]},
      'startup_90_percent_s':{str(v):{k:startup(v,s) for k,s in SCENARIOS.items()} for v in [3.3,3.7,4.2]},
      'protection':{'itrip_A_nominal':{str(v):v*22000/172000/(4990*205e-6) for v in [2.8,3.3,3.7,4.2]},'startup_blank_s_nominal':6.5e6*470e-9,'stall_after_blank':'latch outputs off, IN1=IN2=0 long enough for sleep resets latch','limitations':'threshold/timer tolerances and current ripple must be measured; no guarantee against every mechanical jam'},
      'limitations':['Blade polars and ceiling/bearing/belt losses assumed; no measured coefficient or wind guarantee.','PWM uses drive/brake via two GPIOs. DC-equivalent approximation is not a switching simulation; winding RMS and ripple must be measured.','Manufacturer endpoints and undervoltage scaling are extrapolations; temperature changes curves.','No desktop air-speed inference from disk induced velocity.','No fatigue, blade strength, noise, balance, magnet holding or heat test performed.','Continuous winding current must remain <=0.375A in prototype; initial60% PWM is not closed-loop speed control.']}
    Path('product/references/fan_drive_analysis.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['transmission','selected_initial_60_percent','selected_full_duty_unqualified','startup_90_percent_s','protection']},indent=2))
if __name__=='__main__':main()
