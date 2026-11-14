# cell: internal_carrier
# cell: internal_carrier
# cell: internal_carrier
from screwjoint import make_screw_joint_v1
f=part('fuselage')
pcb_z=param('pcb_bottom_z',-4.0)
pcb_engage=param('pcb_thread_engagement',2.2)
motor_axis_x=param('fan_motor_axis_x',23.0)
motor_front_z=param('fan_motor_front_z',29.3)
motor_plate_t=param('fan_motor_plate_thickness',2.0)
motor_plate_w=param('fan_motor_plate_width',16.0)
motor_plate_d=param('fan_motor_plate_depth',20.0)
motor_boss_clear=param('fan_motor_boss_clearance',4.6)
motor_screw_pitch=param('fan_motor_screw_pitch',9.0)
motor_screw_clear=param('fan_motor_screw_clearance',1.8)
motor_tension_travel=param('fan_motor_tension_travel',1.2)
motor_support_y=param('fan_motor_support_y',8.0)
support_d=param('fan_motor_support_diameter',4.4)
strap_width=param('battery_strap_width',10.5)
strap_gap=param('battery_strap_slot_width',1.8)
body=f.carrier_shell_cut
for x in [-16,16]:
 body=body+Pos(x,-11,-7.05)*Cylinder(3.0,5.9)
# Manufacturer HPCB gearbox front plane; through holes into metal M1.6 threads.
# No printed thread is modeled at this motor interface.
plate=Pos(motor_axis_x,0,motor_front_z+motor_plate_t/2)*Box(motor_plate_w,motor_plate_d,motor_plate_t)
plate=plate-Pos(motor_axis_x,0,motor_front_z+motor_plate_t/2)*extrude(SlotOverall(motor_boss_clear+motor_tension_travel,motor_boss_clear),(motor_plate_t+1)/2,both=True)
for dx in [-motor_screw_pitch/2,motor_screw_pitch/2]:
 plate=plate-Pos(motor_axis_x+dx,0,motor_front_z+motor_plate_t/2)*extrude(SlotOverall(motor_screw_clear+motor_tension_travel,motor_screw_clear),(motor_plate_t+1)/2,both=True)
body=body+plate
for side in [-1,1]:
 y=side*motor_support_y
 # Hidden deck extension joins posts to the existing carrier without crossing PCB.
 body=body+Pos(21,y,f.carrier_top-1)*Box(8,7,2)
 body=body+Pos(motor_axis_x,y,(f.carrier_top+motor_front_z+0.5)/2)*Cylinder(support_d/2,motor_front_z+0.5-f.carrier_top)

board_thickness=param('pcb_stack_thickness',1.58)
board_w=param('pcb_mount_outline_width',40.0)
board_d=param('pcb_mount_outline_depth',30.0)
# Unpublished construction slab supplies only the screw kit through-stack.
# Actual board outline, holes and components are the released imported assembly.
pcb=Pos(0,0,pcb_z+0.755)*Box(board_w,board_d,board_thickness)
board_top_z=pcb_z+1.545
pcb_hardware=[]
for i,x in enumerate([-16,16]):
 j=make_screw_joint_v1(size='M2',at=Location((x,-11,board_top_z)),through=[(pcb,board_thickness)],seat='surface',engage_depth=pcb_engage,into=body,material='PETG',label='connection-board-'+str(i),finish='stainless')
 body=body+j.bosses-j.engage_cuts
 pcb_hardware.append(j.hardware)
 print('PCB screw',i,j.screw_length_mm,'boss',j.boss_length_mm)

# New downward COB collector and detachable internal supports.
heat_x=param('cob_collector_x',-28.0)
heat_bottom=param('cob_collector_bottom_z',0.0)
heat_height=param('cob_collector_length_x',18.0)
heat_width=param('cob_collector_width_y',34.0)
heat_thickness=param('cob_collector_thickness',3.0)
heat_frame=Pos(heat_x,0,heat_bottom+heat_thickness/2)
heat_raw=heat_frame*Box(heat_height,heat_width,heat_thickness)
heat_cut=heat_raw
led_wing_top=param('led_wing_top_z',-5.0)
led_bracket_t=param('led_bracket_base_thickness',2.0)
bracket_station=param('cob_bracket_station_y',20.5)
bracket_mount_y=param('cob_collector_mount_y',10.5)
wing_bottom=f.carrier_top-f.carrier_thickness
led_brackets={}; bracket_hardware=[];heat_hardware=[]
for side in [-1,1]:
 wing=Pos(-23,side*18,(wing_bottom+led_wing_top)/2)*Box(6,10,led_wing_top-wing_bottom)
 body=body.fuse(wing)
 bracket=Pos(-23,side*18,led_wing_top+led_bracket_t/2)*Box(6,10,led_bracket_t)
 bracket=bracket.fuse(Pos(-23,side*13,-1.6)*Box(4,10,3.2))
 mount=make_screw_joint_v1(size='M1.6',at=Location((-23,side*bracket_station,led_wing_top+led_bracket_t)),through=[(bracket,led_bracket_t)],seat='surface',engage_depth=2,into=body,material='PETG',label='cob-bracket-'+str(side),finish='stainless')
 body=body+mount.bosses-mount.engage_cuts
 bracket=bracket-mount.through_cuts[0]
 bracket_hardware.append(mount.hardware)
 joint=make_screw_joint_v1(size='M1.6',at=Location((-23,side*bracket_mount_y,heat_bottom+heat_thickness)),through=[(heat_raw,heat_thickness)],seat='surface',engage_depth=2,into=bracket,material='ASA',label='cob-collector-'+str(side),finish='stainless')
 bracket=bracket+joint.bosses-joint.engage_cuts
 heat_cut=heat_cut-joint.through_cuts[0]
 heat_hardware.append(joint.hardware)
 assert len(bracket.solids())==1
 led_brackets[side]=bracket
 print('COB support screws',mount.screw_length_mm,joint.screw_length_mm)
publish('led_bracket_screws',bracket_hardware,'COB支座固定螺钉',role='fastener',material='stainless_steel')
publish('heat_mount_screws',heat_hardware,'COB集热板固定螺钉',role='fastener',material='stainless_steel')

connections={'shell':'kit: f.carrier_joints','pcb':'kit: M2 self-forming joints','motor':'free: Pololu3060 metal gearbox front face, 2xM1.6x3 through 2mm PETG plate, 1mm metal engagement','battery':'free: integral19x66.2mm18650cradle with removable end gate'}
connections['controller']='free: integral controller rails on two frame supports'
connections['loom']='free: integral open guide closed with one nylon tie'
assert len(connections)==6
assert len(body.solids())==1
body=body-Pos(0,18.5,-7.5)*Box(4,5,6)
# F1 underside relief: blind pocket, with a locally reinforced floor.
fuse_x=param('fuse_clearance_x',-8.0)
fuse_y=param('fuse_clearance_y',12.84)
fuse_pocket_w=param('fuse_pocket_width',8.1)
fuse_pocket_d=param('fuse_pocket_depth',4.7)
fuse_pocket_floor_z=param('fuse_pocket_floor_z',-7.5)
fuse_pad_bottom=param('fuse_relief_pad_bottom_z',-9.2)
fuse_pad_border=param('fuse_relief_pad_border',1.0)
fuse_corner=param('fuse_relief_corner_radius',0.8)
reinforce=Pos(fuse_x,fuse_y,fuse_pad_bottom)*extrude(RectangleRounded(fuse_pocket_w+2*fuse_pad_border,fuse_pocket_d+2*fuse_pad_border,fuse_corner+fuse_pad_border),(-7.6)-fuse_pad_bottom)
body=body.fuse(reinforce)
relief=Pos(fuse_x,fuse_y,fuse_pocket_floor_z)*extrude(RectangleRounded(fuse_pocket_w,fuse_pocket_d,fuse_corner),f.carrier_top-fuse_pocket_floor_z+0.2)
body=body.cut(relief)
assert fuse_pocket_floor_z-fuse_pad_bottom>=1.6
assert len(body.solids())==1
print('F1 relief',fuse_pocket_w,fuse_pocket_d,'floor thickness',fuse_pocket_floor_z-fuse_pad_bottom)
# Local solder/part clearances beside the left mounting land.
# Keep the screw axis and load-bearing centre intact.
mount_relief_floor=param('pcb_mount_edge_relief_floor_z',-5.1)
for rx,ry,rw,rd in [(-16.5,-14.0,3.5,1.9),(-12.825,-10.6,2.25,1.55)]:
 body=body-Pos(rx,ry,mount_relief_floor)*extrude(RectangleRounded(rw,rd,0.25),(-3.9)-mount_relief_floor)
assert len(body.solids())==1
# Open cable saddles accept the harness laterally; 2.5mm ties close the mouths.
wire_x=param('ntc_wire_axis_x',12.5)
wire_pair_r=param('ntc_wire_pair_radius',1.5)
wire_guide_r=param('ntc_wire_guide_inner_radius',2.0)
wire_guide_wall=param('ntc_wire_guide_wall',1.5)
wire_guide_t=param('ntc_wire_guide_width',4.0)
wire_guide_y=param('ntc_battery_guide_y',-27.5)
wire_bridge_w=param('ntc_battery_bridge_width',7.0)
wire_bridge_t=param('ntc_battery_bridge_thickness',2.0)
outer_r=wire_guide_r+wire_guide_wall
# Lower saddle lies outside the board edge; extension roots in the existing deck at Y=-18.
low=Pos(wire_x,wire_guide_y,-7)*Cylinder(outer_r,wire_guide_t)
low=low.fuse(Pos(wire_x,-22.5,-7)*Box(wire_bridge_w,10,wire_bridge_t))
low=low-Pos(wire_x,wire_guide_y,-7)*Cylinder(wire_guide_r,wire_guide_t+2)
low=low-Pos(wire_x+outer_r/2,wire_guide_y,-7)*Box(outer_r,2*outer_r+0.2,wire_guide_t+2)
# Upper NTC branches tie directly to the existing motor post; no redundant ring.
body=body.fuse(low)
assert len(body.solids())==1
print('NTC wire guides: pair diameter',2*wire_pair_r,'bore',2*wire_guide_r,'wall',wire_guide_wall)
def make_cradle():
 from screwjoint import make_screw_joint_v1
 cell_d=param('pack_design_diameter',19)
 cell_l=param('pack_design_length',66.2)
 cell_z=param('pack_axis_z',-24)
 radial_gap=param('pack_radial_clearance',0.3)
 wall=param('saddle_wall',2)
 rail_x=param('cradle_rail_x',11.3)
 rail_w=param('cradle_rail_width',2.4)
 rail_top=param('cradle_top_z',-10)
 rail_t=param('cradle_rail_thickness',2)
 rail_l=param('cradle_rail_length',56)
 station=param('inner_saddle_station',7)
 band=param('inner_saddle_band_width',12)
 saddle_floor=param('saddle_lowest_z',-30.5)
 tie_slot_x=param('deck_tie_slot_x',-2)
 tie_slot_w=param('cradle_deck_tie_slot_width',4)
 tie_slot_t=param('cradle_deck_tie_slot_thickness',1.3)
 end_y=param('cell_end_stop_y',36.4)
 end_bar_w=param('end_bar_width',12)
 end_bar_h=param('end_bar_height',3)
 end_bar_t=param('end_bar_thickness',2)
 end_z=param('end_stop_centre_z',-21)
 arm_r=param('end_brace_radius',1.2)
 rear_brace_y=param('battery_rear_brace_station_y',24.0)
 gate_pad_y=param('battery_gate_station_y',29.0)
 gate_t=param('gate_foot_actual_thickness',3.8)
 gate_top=param('gate_foot_actual_top_z',-8.2)
 gate_engage=param('gate_thread_engagement',2.2)
 gate_foot_w=param('gate_foot_width_x',7.0)
 gate_foot_d=param('gate_foot_depth_y',5.0)
 inner=cell_d/2+radial_gap
 outer=inner+wall
 body=Pos(-rail_x,0,rail_top-rail_t/2)*Box(rail_w,rail_l,rail_t)
 body=body+Pos(rail_x,0,rail_top-rail_t/2)*Box(rail_w,rail_l,rail_t)
 for y in [-17,17]:
  body=body+Pos(0,y,rail_top-rail_t/2)*Box(2*rail_x+rail_w,14,rail_t)

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
  a=Vector(side*rail_x,-rear_brace_y,rail_top-1)
  m1=Vector(side*16.9,-24,-16);m2=Vector(side*16.9,-28,-19)
  b=Vector(side*5,-end_y,end_z)
  rods=[Solid.make_cylinder(arm_r,(q-p).length,Plane(origin=p,z_dir=q-p)) for p,q in [(a,m1),(m1,m2),(m2,b)]]
  rear=rear.fuse(*rods,Pos(m1)*Sphere(arm_r),Pos(m2)*Sphere(arm_r))
  host=Pos(side*rail_x,gate_pad_y,-17)*extrude(RectangleRounded(gate_foot_w,gate_foot_d,1),5)
  body=body.fuse(Pos(side*rail_x,(18.5+gate_pad_y)/2,-13.5)*Box(7,gate_pad_y-12.5,3),host)
  foot=Pos(side*rail_x,gate_pad_y,gate_top-gate_t)*extrude(RectangleRounded(gate_foot_w,gate_foot_d,1),gate_t)
  a=Vector(side*14,gate_pad_y,-9);m0=Vector(side*16.9,gate_pad_y,-9)
  m1=Vector(side*16.9,gate_pad_y,-16);m2=Vector(side*16.9,28,-19);b=Vector(side*5,end_y,end_z)
  rods=[Solid.make_cylinder(arm_r,(q-p).length,Plane(origin=p,z_dir=q-p)) for p,q in [(a,m0),(m0,m1),(m1,m2),(m2,b)]]
  gate=gate.fuse(foot,*rods,Pos(m0)*Sphere(arm_r),Pos(m1)*Sphere(arm_r),Pos(m2)*Sphere(arm_r))
 body=body+rear
 assert len(body.solids())==1
 assert len(gate.solids())==1
 gate_hardware=[]
 for side in [-1,1]:
  j=make_screw_joint_v1(size='M2',at=Location((side*rail_x,gate_pad_y,gate_top)),through=[(gate,gate_t)],seat='surface',head='socket_cap',engage_depth=gate_engage,into=body,material='PETG',label='18650-end-gate-'+str(side),finish='stainless')
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
 # Recess the single replaceable wide fabric strap into the saddle; protect the pack wrap.
 belt_outer=param('belt_groove_outer_radius',10.55)
 belt_width=param('belt_groove_width',26)
 body=body-Pos(0,0,cell_z)*Rot(90,0,0)*Cylinder(belt_outer,belt_width)
 assert len(body.solids())==1
 # Pack reference remains unpublished: full wrapped/welded envelope for clearance checks.
 cell_envelope=Pos(0,0,cell_z)*Rot(90,0,0)*Cylinder(cell_d/2,cell_l)
 # Integral hard datums fix cell height; zip ties supply clamp force, not a compressible Z datum.
 datum_h=param('deck_datum_height',2)
 stop_h=param('deck_stop_height',3)
 stop_t=param('deck_stop_wall',1.2)
 deck_half_x=param('carrier_half_width',21.5)
 deck_half_y=param('carrier_half_depth',19)
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

 return {"body":body,"gate":gate,"gate_hardware":gate_hardware,"end_y":end_y,"end_z":end_z,"end_bar_h":end_bar_h,"end_bar_t":end_bar_t,"station":station,"cell_z":cell_z,"cell_envelope":cell_envelope}

def make_controller_rails():
 f=part('fuselage')
 charging_frame=f.charging_frame
 wire_relief=param('controller_wire_relief_diameter',3)
 floor=param('cassette_lower_face_z',-33.5)
 body=f.controller_cut-charging_frame*Pos(f.controller_pcb_x-2.2,0,-8.0)*Rot(0,90,0)*Cylinder(wire_relief/2,4)
 body=body-charging_frame*Pos(0,0,floor-50)*Box(100,100,100)
 fanout_r=param('edge_pad_wire_clearance_radius',1)
 for x,y in [(18.1361,7.62),(18.1361,-7.62),(33.3761,-7.62)]:
  body=body-Pos(x,y,-26.2)*Cylinder(fanout_r,4.2)
 support_h=param('integral_board_support_height',0.6)
 support_l=param('integral_board_support_length',20.5)
 support_w=param('integral_board_support_width',17.2)
 board_centre_x=f.charging_opening_x+f.controller_shift_x-15.25
 support_z=f.charging_opening_z+f.controller_mount_raise+f.controller_pcb_x-1.4-f.usb_mouth_x
 if support_h>0:
  support_profile=RectangleRounded(support_l,support_w,0.5)-RectangleRounded(support_l-3.5,support_w-4.0,0.5)
  body=body+Pos(board_centre_x,0,support_z)*extrude(support_profile,support_h)
 assert len(body.solids())==1
 body.color=srgb('#87CEEB')

 # Open the rear PCB stop for straight bench installation; one removable tape tab retains it axially.
 rear_release=Pos(43.1,0,-28.3)*Box(13.9,18.4,1.5)
 body=body.cut(rear_release)
 if isinstance(body,ShapeList):body=Compound(children=list(body))
 assert len(body.solids())==1
 return {"body":body}

def make_loom_guide():
 x=param('guide_axis_x',23)
 y=param('guide_axis_y',-16)
 z=param('guide_axis_z',15)
 bore=param('unit_loom_bore_radius',4.0)
 outer=param('unit_loom_outer_radius',5.2)
 t=param('guide_width',2)
 bond_gap=param('post_adhesive_gap',0.2)
 guide=Pos(x,y,z)*(Cylinder(outer,t)-Cylinder(bore,t+2))
 guide=guide-Pos(x-outer/2,y,z)*Box(outer,2*outer+1,t+2)
 root=Pos(24,-12.25,z)*Box(2,1.1,t)
 body=guide.fuse(root)
 body=body-Pos(x,-11.5-bond_gap+20,z)*Box(20,40,t+2)
 assert len(body.solids())==1
 body.color=srgb('#FFFFFF')
 return {"body":body}

cradle_layout=make_cradle()
controller=make_controller_rails()
loom_guide=make_loom_guide()
pack_gate=cradle_layout['gate']
pack_end_y=cradle_layout['end_y']
pack_end_z=cradle_layout['end_z']
pack_end_bar_h=cradle_layout['end_bar_h']
pack_end_bar_t=cradle_layout['end_bar_t']
pack_station=cradle_layout['station']
pack_cell_z=cradle_layout['cell_z']
pack_cell_envelope=cradle_layout['cell_envelope']
controller_support_x=param('controller_post_axis_x',28.5)
controller_support_y=param('controller_post_axis_y',21.5)
controller_support_r=param('unit_controller_support_radius',2.2)
controller_support_bottom=param('unit_controller_support_bottom_z',-30.8)
controller_support_top=param('unit_controller_support_top_z',-7.0)
posts=[]
for side in [-1,1]:
 posts.append(Pos(controller_support_x,side*controller_support_y,(controller_support_bottom+controller_support_top)/2)*Cylinder(controller_support_r,controller_support_top-controller_support_bottom))
 posts.append(Pos(controller_support_x,side*19.5,-30.4)*Box(5,5,2))
 posts.append(Pos(23,side*19.5,-7.2)*Box(9,6,2.4))
controller_bridge_t=param('controller_bridge_thickness',3.2)
controller_bridge_z=param('controller_bridge_centre_z',-11.5)
for side in [-1,1]:
 posts.append(Pos(22.0,side*11,controller_bridge_z)*Box(12,3,controller_bridge_t))
 posts.append(Pos(18.5,side*11,-9.6)*Box(5,3,5.0))
 posts.append(Pos(controller_support_x,side*16,-11.0)*Box(3,14,4))
guide_root=Pos(24,-10.9,15)*Box(2,3.2,2)
body=body.fuse(cradle_layout['body'],controller['body'],loom_guide['body'],*posts,guide_root)
assert not isinstance(body,ShapeList), 'Unit union disconnected: '+str([(round(s.volume,2),tuple(s.bounding_box().min),tuple(s.bounding_box().max)) for s in body])
# Reinforced motor-foot arches keep a straight tool corridor to the rear clamp.
driver_r=param('frame_fastener_passage_radius',2.2)
for side in [-1,1]:
 body=body.fuse(Pos(24,side*motor_support_y,f.carrier_top-1.0)*Box(6,7,5.0))
assert not isinstance(body,ShapeList), 'Arches disconnected: '+str([(round(s.volume,2),tuple(s.bounding_box().min),tuple(s.bounding_box().max)) for s in body])
body=body.cut(Pos(f.frame_rear_x,f.carrier_tool_y_center,f.frame_mount_z)*Rot(90,0,0)*Cylinder(driver_r,f.carrier_tool_y_length))
if isinstance(body,ShapeList): body=Compound(children=list(body))
assert len(body.solids())==1, 'Passage split: '+str([(round(s.volume,2),tuple(s.bounding_box().min),tuple(s.bounding_box().max)) for s in body.solids()])
raw_wire_x=param('raw_pair_drop_x',21.0)
raw_positive_y=param('raw_positive_drop_y',18.5)
raw_negative_y=param('raw_negative_drop_y',20.5)
for drop_y in [raw_positive_y,raw_negative_y]:
 body=body.cut(Pos(raw_wire_x,drop_y,-5)*Cylinder(1.0,50))
 if isinstance(body,ShapeList): body=Compound(children=list(body))
body=body.cut(f.lower_shape,f.cap_shape)
if isinstance(body,ShapeList): body=Compound(children=list(body))
for hardware in f.carrier_hardware:
 body=body.cut(hardware)
 if isinstance(body,ShapeList): body=Compound(children=list(body))
if isinstance(body,ShapeList): body=Compound(children=list(body))
pcb_driver_r=param('pcb_driver_corridor_radius',1.3)
body=body.cut(Pos(16,-11,20)*Cylinder(pcb_driver_r,40))
if isinstance(body,ShapeList): body=Compound(children=list(body))
# Open wire relief below the XIAO edge; the remaining perimeter still supports the PCB.
pack_relief_x=param('closure_pack_channel_x',24.5)
pack_relief_y=param('closure_pack_channel_y',14.5)
pack_relief_z=param('case_pack_wire_relief_z',-30.9)
pack_relief_w=param('closure_pack_channel_width',3.4)
pack_relief_d=param('closure_pack_channel_depth',18.0)
pack_relief_h=param('case_pack_wire_relief_height',4.4)
body=body.cut(Pos(pack_relief_x,pack_relief_y,pack_relief_z)*Box(pack_relief_w,pack_relief_d,pack_relief_h))
if isinstance(body,ShapeList):body=Compound(children=list(body))
# Open -Y release around the new rear case clamp, preserving the PCB support top.
rear_clear_x=param('closure_rear_service_x',21.5)
rear_clear_z=param('closure_rear_service_z',-32.35)
rear_clear_w=param('closure_rear_service_width',7.8)
rear_clear_h=param('closure_rear_service_height',5.9)
body=body.cut(Pos(rear_clear_x,0,rear_clear_z)*Box(rear_clear_w,120,rear_clear_h))
if isinstance(body,ShapeList):body=Compound(children=list(body))
# Wider exit at the actual battery pads; outside the load-bearing rear post.
pack_exit_x=param('closure_pack_exit_x',26.137)
pack_exit_y=param('closure_pack_exit_route_y',10.75)
pack_exit_w=param('closure_pack_exit_width',4.0)
pack_exit_d=param('closure_pack_exit_route_depth',10.5)
body=body.cut(Pos(pack_exit_x,pack_exit_y,pack_relief_z)*Box(pack_exit_w,pack_exit_d,pack_relief_h))
if isinstance(body,ShapeList):body=Compound(children=list(body))
unit_solids=sorted(body.solids(),key=lambda s:s.volume,reverse=True)
unit_trim_mm3=sum(s.volume for s in unit_solids[1:])
if unit_trim_mm3<20 and all(s.volume<12 for s in unit_solids[1:]): body=unit_solids[0]
assert len(body.solids())==1,'Unit frame disconnected: '+str([(round(s.volume,3),tuple(s.bounding_box().min),tuple(s.bounding_box().max)) for s in body.solids()])
publish('unit_frame_gate_screws',cradle_layout['gate_hardware'],'电池端挡固定螺钉',role='fastener',material='stainless_steel')
body.color=srgb('#FFFFFF')
publish('internal_carrier',body,'电池电路电机一体内架',material='petg')
publish('pcb_mount_screws',pcb_hardware,'连接板固定螺钉',role='fastener',material='stainless_steel')