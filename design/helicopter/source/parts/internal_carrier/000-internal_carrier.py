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
for y in [-17,17]:
 body=body-Pos(0,y,f.carrier_top-1)*Box(strap_width,strap_gap,4)
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
strap_tap_y=param('thermal_strap_tap_y',14.5)
strap_tap_major=param('thermal_strap_thread_envelope',2.0)
for side in [-1,1]:
 heat_cut=heat_cut-Pos(heat_x,side*strap_tap_y,heat_bottom+heat_thickness/2)*Cylinder(strap_tap_major/2,heat_thickness+2)
publish('led_bracket_screws',bracket_hardware,'COB支座固定螺钉',role='fastener',material='stainless_steel')
publish('heat_mount_screws',heat_hardware,'COB集热板固定螺钉',role='fastener',material='stainless_steel')

connections={'shell':'kit: f.carrier_joints','pcb':'kit: M2 self-forming joints','motor':'free: Pololu3060 metal gearbox front face, 2xM1.6x3 through 2mm PETG plate, 1mm metal engagement','battery':'free: separate19x66.2mm18650cradle;two removable deck ties,cell straps and captive end gate'}
assert len(connections)==4
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
wire_guide_z=param('ntc_shell_guide_z',24.135)
wire_bridge_w=param('ntc_battery_bridge_width',7.0)
wire_bridge_t=param('ntc_battery_bridge_thickness',2.0)
wire_arm_r=param('ntc_shell_support_radius',1.5)
outer_r=wire_guide_r+wire_guide_wall
# Lower saddle lies outside the board edge; extension roots in the existing deck at Y=-18.
low=Pos(wire_x,wire_guide_y,-7)*Cylinder(outer_r,wire_guide_t)
low=low.fuse(Pos(wire_x,-22.5,-7)*Box(wire_bridge_w,10,wire_bridge_t))
low=low-Pos(wire_x,wire_guide_y,-7)*Cylinder(wire_guide_r,wire_guide_t+2)
low=low-Pos(wire_x+outer_r/2,wire_guide_y,-7)*Box(outer_r,2*outer_r+0.2,wire_guide_t+2)
# Upper saddle is supported from the existing motor plate, outside the plug service volume.
a=Vector(15.5,8,30.0); b=Vector(wire_x+2,17,wire_guide_z+2)
upper=Solid.make_cylinder(wire_arm_r,(b-a).length,Plane(origin=a,z_dir=b-a))
upper=upper.fuse(Pos(wire_x,17,wire_guide_z)*Rot(90,0,0)*Cylinder(outer_r,wire_guide_t))
upper=upper-Pos(wire_x,17,wire_guide_z)*Rot(90,0,0)*Cylinder(wire_guide_r,wire_guide_t+2)
upper=upper-Pos(wire_x-outer_r/2,17,wire_guide_z)*Box(outer_r,wire_guide_t+2,2*outer_r+0.2)
body=body.fuse(low,upper)
assert len(body.solids())==1
print('NTC wire guides: pair diameter',2*wire_pair_r,'bore',2*wire_guide_r,'wall',wire_guide_wall)
# Recess the deck straps below the PCB's solder-tail envelope.
tie_seat_floor=param('deck_tie_recess_floor_z',-6.7)
for sy in [-1,1]:
 body=body-Pos(-2,sy*18.6,(tie_seat_floor-5.9)/2)*Box(3.5,1.4,-5.9-tie_seat_floor)
assert len(body.solids())==1
body.color=srgb('#FFFFFF')
publish('internal_carrier',body,'电路电池电机托架',material='petg')
publish('pcb_mount_screws',pcb_hardware,'连接板固定螺钉',role='fastener',material='stainless_steel')