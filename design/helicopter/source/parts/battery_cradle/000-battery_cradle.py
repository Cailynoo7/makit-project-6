from screwjoint import make_screw_joint_v1
cell_d=param('pack_design_diameter',19.0)
cell_l=param('pack_design_length',66.2)
cell_z=param('pack_axis_z',-24.0)
radial_gap=param('pack_radial_clearance',0.3)
wall=param('saddle_wall',2.0)
rail_x=param('cradle_rail_x',11.3)
rail_w=param('cradle_rail_width',2.4)
rail_top=param('cradle_top_z',-10.0)
rail_t=param('cradle_rail_thickness',2.0)
rail_l=param('cradle_rail_length',56.0)
station=param('inner_saddle_station',7.0)
band=param('inner_saddle_band_width',12.0)
saddle_floor=param('saddle_lowest_z',-30.5)
tie_slot_x=param('deck_tie_slot_x',-2.0)
tie_slot_w=param('cradle_deck_tie_slot_width',4.0)
tie_slot_t=param('cradle_deck_tie_slot_thickness',1.3)
end_y=param('cell_end_stop_y',34.4)
end_bar_w=param('end_bar_width',12.0)
end_bar_h=param('end_bar_height',3.0)
end_bar_t=param('end_bar_thickness',2.0)
end_z=param('end_stop_centre_z',-21.0)
arm_r=param('end_brace_radius',1.2)
gate_pad_y=param('gate_service_station_y',24.0)
gate_t=param('gate_foot_thickness',4.0)
gate_top=param('gate_foot_top_z',-8.0)
gate_engage=param('gate_thread_engagement',2.2)
inner=cell_d/2+radial_gap
outer=inner+wall
body=Pos(-rail_x,0,rail_top-rail_t/2)*Box(rail_w,rail_l,rail_t)
body=body+Pos(rail_x,0,rail_top-rail_t/2)*Box(rail_w,rail_l,rail_t)
for y in [-17,17]:
 body=body+Pos(0,y,rail_top-rail_t/2)*Box(2*rail_x+rail_w,14,rail_t)
 body=body-Pos(tie_slot_x,y,rail_top-rail_t/2)*Box(tie_slot_w,tie_slot_t,rail_t+2)
for y in [-station,station]:
 ring=Pos(0,y,cell_z)*Rot(90,0,0)*(Cylinder(outer,band)-Cylinder(inner,band+2))
 ring=ring & Pos(0,y,(saddle_floor+cell_z+1)/2)*Box(2*outer+2,band+2,cell_z+1-saddle_floor)
 for side in [-1,1]:
  rib=Pos(side*rail_x,y,(saddle_floor+rail_top)/2)*Box(rail_w,band,rail_top-saddle_floor)
  ring=ring+rib
 body=body+ring
body=body-Pos(0,27.5,-10)*Box(40,14,4)
# End stops leave the centre of each terminal free for spot-welded leads.
rear=Pos(0,-end_y,end_z)*Box(end_bar_w,end_bar_t,end_bar_h)
gate=Pos(0,end_y,end_z)*Box(end_bar_w,end_bar_t,end_bar_h)
for side in [-1,1]:
 # Narrow braces remain inboard of the four skid-root clamps.
 a=Vector(side*rail_x,-gate_pad_y,rail_top-1)
 m1=Vector(side*16.9,-24,-16);m2=Vector(side*16.9,-28,-19)
 b=Vector(side*5,-end_y,end_z)
 rods=[Solid.make_cylinder(arm_r,(q-p).length,Plane(origin=p,z_dir=q-p)) for p,q in [(a,m1),(m1,m2),(m2,b)]]
 rear=rear.fuse(*rods,Pos(m1)*Sphere(arm_r),Pos(m2)*Sphere(arm_r))
 host=Pos(side*rail_x,gate_pad_y,-14.5)*Cylinder(3.5,5)
 body=body.fuse(Pos(side*rail_x,21.5,-13.5)*Box(7,6,3),host)
 foot=Pos(side*rail_x,gate_pad_y,gate_top-gate_t/2)*Cylinder(3.5,gate_t)
 a=Vector(side*14,24,-9);m0=Vector(side*16.9,24,-9)
 m1=Vector(side*16.9,24,-16);m2=Vector(side*16.9,28,-19);b=Vector(side*5,end_y,end_z)
 rods=[Solid.make_cylinder(arm_r,(q-p).length,Plane(origin=p,z_dir=q-p)) for p,q in [(a,m0),(m0,m1),(m1,m2),(m2,b)]]
 gate=gate.fuse(foot,*rods,Pos(m0)*Sphere(arm_r),Pos(m1)*Sphere(arm_r),Pos(m2)*Sphere(arm_r))
body=body+rear
assert len(body.solids())==1
assert len(gate.solids())==1
gate_hardware=[]
for side in [-1,1]:
 j=make_screw_joint_v1(size='M2',at=Location((side*rail_x,gate_pad_y,gate_top)),through=[(gate,gate_t)],seat='counterbore',head_recess=0.2,engage_depth=gate_engage,into=body,material='PETG',label='18650-end-gate-'+str(side),finish='stainless')
 body=body+j.bosses-j.engage_cuts
 gate=gate-j.through_cuts[0]
 gate_hardware.append(j.hardware)
 print('Gate screw',j.screw_length_mm,'head land',j.head_land_mm)
assert len(body.solids())==1
assert len(gate.solids())==1
# The J11 pair descends outside the shortened free rail end.
body=body-Pos(rail_x,-27.65,rail_top-1)*Box(rail_w+1,4.7,4)
# The end braces follow the pack clearance envelope, with no load on its insulation.
pack_relief=Pos(0,0,cell_z)*Rot(90,0,0)*Cylinder(cell_d/2+radial_gap,cell_l+0.6)
body=body-pack_relief
gate=gate-pack_relief
assert len(body.solids())==1
assert len(gate.solids())==1
# Recess the replaceable fabric straps into the saddle; protect the pack wrap.
belt_outer=param('belt_groove_outer_radius',10.55)
belt_width=param('belt_groove_width',11.0)
for y in [-station,station]:
 body=body-Pos(0,y,cell_z)*Rot(90,0,0)*Cylinder(belt_outer,belt_width)
assert len(body.solids())==1
# Pack reference remains unpublished: full wrapped/welded envelope for clearance checks.
cell_envelope=Pos(0,0,cell_z)*Rot(90,0,0)*Cylinder(cell_d/2,cell_l)
# Integral hard datums fix cell height; zip ties supply clamp force, not a compressible Z datum.
datum_h=param('deck_datum_height',2.0)
stop_h=param('deck_stop_height',3.0)
stop_t=param('deck_stop_wall',1.2)
deck_half_x=param('carrier_half_width',21.5)
deck_half_y=param('carrier_half_depth',19.0)
clear_x=param('carrier_side_clearance',0.3)
clear_y=param('carrier_end_clearance',0.4)
members=[Pos(8,12,rail_top+datum_h/2)*Box(6,4,datum_h),Pos(-8,-12,rail_top+datum_h/2)*Box(6,4,datum_h)]
for side in [-1,1]:
 members.append(Pos(0,side*(deck_half_y+clear_y+stop_t/2),rail_top+stop_h/2)*Box(4,stop_t,stop_h))
 edge=deck_half_x+clear_x+stop_t/2
 members.append(Pos(side*(rail_x+edge)/2,0,rail_top+datum_h/2)*Box(edge-rail_x,3,datum_h))
 members.append(Pos(side*edge,0,rail_top+stop_h/2)*Box(stop_t,4,stop_h))
body=body.fuse(*members)
assert len(body.solids())==1
body.color=srgb('#FFFFFF')
publish('battery_cradle',body,'18650可拆托座',material='petg')
publish('battery_gate_screws',gate_hardware,'电池端挡固定螺钉',role='fastener',material='stainless_steel')
