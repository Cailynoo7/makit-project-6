# cell: window_left
s=part('fuselage')
radius=param('pane_register_radius',18.75)
flange_radius=param('pane_shoulder_radius',21.3)
gap=param('pane_button_clearance',0.25)
thick=param('pane_radial_thickness',3.5)
R=s.body_width/2
d=R-40
outer=Sphere(R)
inner=Sphere(R-thick)
region=Pos(0,R,0)*Rot(90,0,0)*Cylinder(radius,2*R)
flange_region=Pos(0,R,0)*Rot(90,0,0)*Cylinder(flange_radius,2*R)
body=(outer-Sphere(R-1.2)).intersect(flange_region)
body=body.fuse((Sphere(R-1.2)-inner).intersect(region))
button_radius=part('button_left').radius
body=body.cut(Pos(0,R,0)*Rot(90,0,0)*Cylinder(button_radius+gap,2*R))
holder_t=param('holder_wall',1.6)
holder=Pos(0,25.1+d,2)*Box(17.8,holder_t,21.6)
# Rear opening permits straight inward withdrawal with the removable clamp.
# Side strips remain1.4mm thick; guide clearance is0.3mm per board edge.
holder=holder.cut(Pos(0,25.1+d,2)*Box(15,holder_t+0.4,22.4))
for sx in [-1,1]:
 holder=holder.fuse(Pos(sx*8.1,27+d,2)*Box(1.6,3.8,21.6))
 holder=holder.fuse(Pos(sx*7.35,28.3+d,2)*Box(2.1,1.2,21.6))
 holder=holder.fuse(Pos(sx*10.4,25.1+d,0)*Box(4.8,1.6,3.2))
 holder=holder.fuse(Pos(sx*12,29.75+d,0)*Rot(90,0,0)*Cylinder(3.2,11.5))
holder=holder.cut(Pos(0,28.3+d,0)*Box(15,1.6,7.0))
# PCB rear pads and lower ledge belong to the removable clamp, not this window.
holder=holder.cut(Pos(0,24.7+d,12)*Box(4.2,4.5,14))
body=body.fuse(holder)
# Separate internal U-ring clamps the spherical shell against the pane shoulder.
retainer=Pos(0,23+d,0)*Box(48,2,28)
retainer=retainer.cut(Pos(0,23+d,0)*Box(19,4,23))
retainer=retainer.cut(Pos(0,23+d,15)*Box(6,4,12))
for sx in [-1,1]:
 foot=(Pos(sx*23,39+d,0)*Box(6,30,8)).intersect(Sphere(R-s.wall))
 retainer=retainer.fuse(foot)
from screwjoint import make_screw_joint_v1
window_hardware=[]
for sx in [-1,1]:
 j=make_screw_joint_v1(size='M2',at=Location((sx*12,22+d,0),(90,0,0)),through=[(retainer,2)],seat='surface',head='socket_cap',engage_depth=3.5,into=body,material='PETG',print_axis='horizontal',label='window_left-'+str(sx),finish='stainless')
 if j.boss_length_mm is not None and j.boss_length_mm>0: body=body.fuse(j.bosses)
 body=body.cut(j.engage_cuts)
 retainer=retainer.cut(j.through_cuts[0])
 window_hardware.append(j.hardware)
assert len(body.solids())==1

body.color=srgb(s.window_pale_blue)
publish('window_left',body,'左浅蓝承肩圆窗',material='petg')
publish('window_left_screws',window_hardware,'圆窗内部压紧螺钉',role='fastener',material='stainless_steel')
