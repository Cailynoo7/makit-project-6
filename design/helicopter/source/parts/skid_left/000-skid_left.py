from math import atan2,sin,cos,sqrt
f=part('fuselage')
length=param('enlarged_skid_length',90)
width=param('enlarged_skid_width',3.75)
leg=param('enlarged_skid_leg_diameter',3.5)
tip_run=param('enlarged_skid_tip_run',7.5)
front_rise=param('enlarged_skid_front_rise',3.75)
curve_handle=param('enlarged_skid_curve_handle',12.5)
peg_exit=param('enlarged_skid_peg_exit',1.8)
peg_inset=param('retained_skid_peg_inset',9)
a=-length/2+tip_run
b=length/2-tip_run
h=f.skid_mount_z-f.skid_rail_z
def arc_mid(x,direction):
 r=(tip_run*tip_run+front_rise*front_rise)/(2*front_rise)
 theta=atan2(tip_run,r-front_rise)
 return (x+direction*r*sin(theta/2),0,r*(1-cos(theta/2)))
def make_skid(rail_width):
 path=Wire([ThreePointArc((-length/2,0,front_rise),arc_mid(a,-1),(a,0,0)),Line((a,0,0),(b,0,0)),ThreePointArc((b,0,0),arc_mid(b,1),(length/2,0,front_rise))])
 rail=sweep(Plane(origin=path@0,z_dir=path%0)*Circle(rail_width/2),path)
 rail=rail+Pos(-length/2,0,front_rise)*Sphere(rail_width/2)
 rail=rail+Pos(length/2,0,front_rise)*Sphere(rail_width/2)
 caps=[]
 hardware=[]
 from screwjoint import make_screw_joint_v1
 for x in [-f.skid_mount_half_pitch,f.skid_mount_half_pitch]:
  start=(x,f.skid_root_y-peg_inset-f.skid_rail_y,h)
  exit_point=(x,f.skid_root_y+peg_exit-f.skid_rail_y,h)
  curve=Wire([Line(start,exit_point),Bezier(exit_point,(x,exit_point[1]+curve_handle,h),(x,0,h*0.55),(x,0,0))])
  rail=rail+sweep(Plane(origin=start,z_dir=(0,1,0))*Circle(leg/2),curve)
  peg=Pos(x,f.skid_root_y-3.5-f.skid_rail_y,h)*Rot(90,0,0)*Cylinder(2.5,11)
  collar=(Sphere(f.body_width/2+1.2)-Sphere(f.body_width/2)).intersect(Pos(x,f.skid_root_y,f.skid_mount_z)*Rot(90,0,0)*Cylinder(3.5,12))
  rail=rail.fuse(peg)
  rail=rail.fuse(Pos(0,-f.skid_rail_y,-f.skid_rail_z)*collar)
  cap=(Pos(x,34.75,f.skid_mount_z)*Rot(90,0,0)*Cylinder(4.6,20.5)).intersect(Sphere(f.body_width/2-f.wall))
  cap=cap.cut(Pos(x,38.9,f.skid_mount_z)*Rot(90,0,0)*Cylinder(3.35,22.2))
  cap=Pos(0,-f.skid_rail_y,-f.skid_rail_z)*cap
  j=make_screw_joint_v1(size='M2',at=Location((x,24.5-f.skid_rail_y,h),(90,0,0)),through=[(cap,3.3)],seat='surface',head='socket_cap',engage_depth=4.5,into=rail,material='PETG',print_axis='horizontal',label='skid-root-'+str(x),finish='stainless')
  if j.boss_length_mm is not None and j.boss_length_mm>0:
   support=j.bosses.intersect(Pos(x,f.skid_root_y-3.5-f.skid_rail_y,h)*Rot(90,0,0)*Cylinder(2.5,12))
   rail=rail.fuse(support)
  rail=rail.cut(j.engage_cuts)
  cap=cap.cut(j.through_cuts[0])
  caps.append(cap)
  hardware.append(j.hardware)
 return rail,caps,hardware
body,caps,hardware=make_skid(width)
body.color=srgb('#FFFFFF')
publish('skid_left',body,'左滑橇',material='petg')

publish('skid_root_screws_left',[Pos(0,f.skid_rail_y,f.skid_rail_z)*h for h in hardware],'左起落架内部螺钉',role='fastener',material='stainless_steel')
