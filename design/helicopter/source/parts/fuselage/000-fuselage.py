# cell: fuselage
# cell: fuselage
# cell: fuselage
body_length=param('cabin_diameter',100.0)
body_width=body_length
body_height=body_length
wall=param('shell_wall',2.4)
front_plane=param('enlarged_front_plane',-40.1875)
bottom_plane=param('enlarged_bottom_plane',-36.25)
window_radius = param('window_aperture_radius',19.0)
window_x = param('window_x', -8.0)
window_z = param('window_z', 6.0)
outer=Sphere(body_length/2)
inner=Sphere(body_length/2-wall)
motor_pocket=(Pos(23,0,24)*Cylinder(15.2,21)).intersect(Sphere(body_length/2-1.8))
inner=inner.fuse(motor_pocket)
inner=inner.fuse(Pos(23,0,35.3)*Cylinder(5.5,5))
shell = outer-inner
shell = shell - Pos(front_plane-60,0,0)*Box(120,160,160)
shell = shell - Pos(0,0,bottom_plane-50)*Box(180,180,100)
shell = shell - Pos(window_x,0,window_z)*Rot(90,0,0)*Cylinder(window_radius,100)
tail_clearance=param('tail_socket_clearance',0.25)
skid_hole=param('skid_root_socket_diameter',5.3)
ts=part('tail')
shell=shell-Pos(ts.root_x,0,-3.75)*ts.cone_clearance
shell=shell-Pos(ts.root_x,0,-3.75)*ts.receiver_slot
for slide_cut in ts.boss_slide_cuts:
 shell=shell-Pos(ts.root_x,0,-3.75)*slide_cut
tail_receiver=Pos(ts.root_x,0,-3.75)*ts.receiver
tail_receiver=tail_receiver&outer
# Right half slides off sideways: the motor supports stay on the main carrier.
# Receiver is entirely contained inside the original spherical envelope.


from math import sqrt
skid_mount_half_pitch=param('enlarged_skid_half_pitch',22.5)
skid_mount_z=param('enlarged_skid_mount_z',-25.0)
skid_rail_y=param('enlarged_skid_rail_y',56.25)
skid_rail_z=param('enlarged_skid_rail_z',-51.25)
skid_root_y=(body_width/2)*sqrt(1-(skid_mount_half_pitch/(body_length/2))**2-(skid_mount_z/(body_height/2))**2)
for x in [-skid_mount_half_pitch,skid_mount_half_pitch]:
 for side in [-1,1]:
  shell=shell-Pos(x,side*skid_root_y,skid_mount_z)*Rot(90,0,0)*Cylinder(skid_hole/2,20)
from screwjoint import make_screw_joint_v1
roof_radius=param('suspension_roof_radius',8.0)
roof_height=param('suspension_roof_thickness',3.0)
roof_top=33.0
belly_opening=param('enlarged_belly_aperture_diameter',63.75)
shell=shell-Pos(0,0,bottom_plane+1.1)*Cylinder(belly_opening/2+0.25,2.2)
# Concealed bearing bridge: the sphere remains smooth above it.
beam_w=param('fixed_roof_beam_width',16.0)
beam_t=param('fixed_roof_beam_thickness',5.0)
beam_reach=param('fixed_roof_crosslap_y',8.0)
bridge=(Pos(0,(beam_reach-body_width/2)/2,33-beam_t/2)*Box(beam_w,body_width/2+beam_reach,beam_t)).intersect(outer)
shell=shell.fuse(bridge)
raw_cap=Pos(0,0,106.875)*Cone(8.75,22.5,13.75)
mast_step=66.05
raw_mast=Pos(0,0,(33+mast_step)/2)*Cylinder(4.9,mast_step-33)
raw_mast=raw_mast.fuse(Pos(0,0,(mast_step+100)/2)*Cylinder(6.75,100-mast_step))
joint=make_screw_joint_v1(size='M4',at=Location((0,0,112.25)),through=[(raw_cap,12.25),(raw_mast,67)],seat='countersink',into=shell,strategy='through_nut',material='PETG',label='suspension',finish='stainless')
print('Suspension screw length:',joint.screw_length_mm,'protrusion:',joint.screw_protrusion_mm)
body=shell
if joint.boss_length_mm is not None and joint.boss_length_mm>0: body=body.fuse(joint.bosses)
body=body.cut(joint.engage_cuts)
carrier_width=param('carrier_width',43.0)
carrier_depth=param('carrier_depth',38.0)
carrier_thickness=param('carrier_thickness',2.0)
carrier_top=param('carrier_top',-6.0)
frame_front_x=param('frame_front_locator_x',-30.5)
frame_front_y=param('frame_front_host_y',-34.0)
frame_rear_x=param('frame_rear_mount_x',31.0)
frame_rear_y=param('frame_rear_host_y',-31.0)
frame_mount_z=carrier_top-carrier_thickness/2
frame_flange_w=param('frame_flange_width',8.0)
frame_flange_h=param('frame_flange_height',8.0)
frame_flange_t=param('frame_flange_thickness',2.0)
frame_locator_d=param('frame_locator_diameter',3.0)
frame_locator_gap=param('frame_locator_radial_clearance',0.2)
frame_locator_l=param('frame_locator_length',6.0)
frame_engage=param('frame_mount_engagement',4.0)
front_face=frame_front_y+3
rear_face=frame_rear_y+5
front_host=(Pos(frame_front_x,frame_front_y,frame_mount_z)*Box(frame_flange_w,6,frame_flange_h)).intersect(outer)
rear_host=(Pos(frame_rear_x,frame_rear_y,frame_mount_z)*Box(frame_flange_w,10,frame_flange_h)).intersect(outer)
for x,y in [(frame_front_x,frame_front_y),(frame_rear_x,frame_rear_y)]:
 sign=1 if x>0 else -1
 rib=(Pos(x+sign*3,(y-50)/2,frame_mount_z)*Box(4,50+y,frame_flange_h)).intersect(outer)
 body=body.fuse(rib)
body=body.fuse(front_host,rear_host)
locator_cut=Pos(frame_front_x,frame_front_y,frame_mount_z)*Rot(90,0,0)*Cylinder(frame_locator_d/2+frame_locator_gap,frame_locator_l+0.4)
body=body-locator_cut
raw_carrier=Pos(0,0,carrier_top-carrier_thickness)*extrude(RectangleRounded(carrier_width,carrier_depth,3),carrier_thickness)
arm_end=-carrier_depth/2+2
front_root_x=-carrier_width/2+1.5
rear_root_x=carrier_width/2-1.5
raw_carrier=raw_carrier.fuse(
 Pos((frame_front_x+front_root_x)/2,(front_face+arm_end)/2,frame_mount_z)*Box(abs(frame_front_x-front_root_x)+4,arm_end-front_face,carrier_thickness),
 Pos((frame_rear_x+rear_root_x)/2,(rear_face+arm_end)/2,frame_mount_z)*Box(abs(frame_rear_x-rear_root_x)+6,arm_end-rear_face,carrier_thickness),
 Pos(frame_front_x,front_face+frame_flange_t/2,frame_mount_z)*Box(frame_flange_w,frame_flange_t,frame_flange_h),
 Pos(frame_front_x,frame_front_y+0.2,frame_mount_z)*Rot(90,0,0)*Cylinder(frame_locator_d/2,frame_locator_l),
 Pos(frame_rear_x,rear_face+frame_flange_t/2,frame_mount_z)*Box(frame_flange_w,frame_flange_t,frame_flange_h))
j=make_screw_joint_v1(size='M2',at=Location((frame_rear_x,rear_face+frame_flange_t,frame_mount_z),(-90,0,0)),through=[(raw_carrier,frame_flange_t)],seat='surface',head='socket_cap',engage_depth=frame_engage,into=body,material='PETG',print_axis='vertical',label='unit-frame-rear',finish='stainless')
body=body+j.bosses-j.engage_cuts
carrier_shell_cut=raw_carrier-j.through_cuts[0]
carrier_joints=[j]
carrier_hardware=[j.hardware]
carrier_tool_y_start=rear_face+frame_flange_t
carrier_tool_y_end=body_width/2
carrier_tool_y_center=(carrier_tool_y_start+carrier_tool_y_end)/2
carrier_tool_y_length=carrier_tool_y_end-carrier_tool_y_start
print('Unit frame screw',j.screw_length_mm)
publish('carrier_shell_screws',carrier_hardware,'内架单颗固定螺钉',role='fastener',material='stainless_steel')

drive_axis=23.0
# Drawing-based XIAO cassette. PCB plane X=25; USB mouth at lower board edge.
controller_pcb_x=param('charging_board_plane_x',32.8)
controller_centre_z=param('enlarged_controller_centre_z',-21.0)
controller_clearance=param('controller_edge_clearance',0.25)
cx=controller_pcb_x
cz=controller_centre_z
controller_board_thickness=1.6 # Seeed official v1.3 PCB general.thickness, nominal only
controller_slot_clearance=param('controller_slot_clearance',0.3)
controller_clip_x=cx-1.4+controller_board_thickness+controller_slot_clearance+0.6
print('Controller board slot:',controller_board_thickness+controller_slot_clearance)
usb_mouth_x=param('charging_mouth_final_x',36.0)
usb_recess=param('enlarged_usb_recess_depth',4.75)
charging_raise=param('charging_opening_raise',10.0)
usb_plug_corner_radius=param('charging_plug_corner_radius',0.5)
charging_opening_z=bottom_plane+charging_raise
charging_opening_x=sqrt((body_length/2)**2-charging_opening_z**2)
# Carry the complete cassette from its old downward-facing datum to the rear face.
# Community STEP: PCB 20.955x17.78x1; USB front-to-board-centre11.9855,
# mouth centre2.605 above PCB underside.0.6mm removable shim keeps1.9mm slot.
controller_shift_x=-1.4855
controller_mount_raise=1.395
charging_frame=Pos(charging_opening_x+controller_shift_x,0,charging_opening_z+controller_mount_raise)*Rot(0,-90,0)*Pos(-usb_mouth_x,0,-bottom_plane)
print('Charging opening:',charging_opening_x,0,charging_opening_z,'vertical raise:',charging_raise)
controller_raw=Pos(cx-2.2,0,cz)*Box(1.6,21.8,22.0)
controller_raw=controller_raw-Pos(cx-2.2,0,cz)*Box(4,15,16)
for side in [-1,1]:
 for z in [cz-9.0,cz+9.0]:
  controller_raw=controller_raw+Pos(cx+0.1,side*9.95,z)*Box(6.6,1.6,2.4)
  controller_raw=controller_raw+Pos(controller_clip_x,side*9.3,z)*Box(1.2,3.0,2.4)
 controller_raw=controller_raw+Pos(cx-2.2,side*17,-20)*Rot(0,90,0)*Cylinder(3,1.6)
 controller_raw=controller_raw+Pos(cx-2.2,side*14,-20)*Box(1.6,8,3)
 controller_raw=controller_raw+Pos(cx-0.7,side*8.8,cz-11.2)*Box(5.0,3.4,1.2)
controller_raw=charging_frame*controller_raw
# Short inner bridges keep both end stops joined after spherical wall clearance.
for side in [-1,1]:
 controller_raw=controller_raw.fuse(Pos(charging_opening_x+controller_shift_x-5.0,side*8.8,charging_opening_z+controller_mount_raise-0.75)*Box(3.4,2.4,1.8))
# Wall clearance follows the relocated cassette; outer sphere remains intact.
controller_cavity=(charging_frame*Pos(cx,0,cz)*Box(8,23,22.6)).intersect(Sphere(body_length/2-1.8))
body=body-controller_cavity
for side in [-1,1]:
 body=body-charging_frame*Pos(cx-2.4,side*17,-20)*Rot(0,90,0)*Cylinder(3.25,4)
controller_stop_clearance=(charging_frame*Pos(cx,0,-32.55)*Box(8,23,0.9)).intersect(Sphere(body_length/2-1.8))
body=body.cut(controller_stop_clearance)
# Board rails are integral with the unit frame; no separate cassette fasteners.
controller_cut=controller_raw.intersect(Sphere(body_length/2-2.0))
controller_hardware=[]
controller_joints=[]
from portcut import port_cut,PortSpec
usb_cut=port_cut('usb_c',at=(charging_opening_x,0,charging_opening_z),facing='+X',vertical=False,depth=12,clearance=0.15,recess=usb_recess)
plug_body_cut=port_cut(PortSpec('rounded',13.3,7.3,usb_plug_corner_radius),at=(body_length/2,0,charging_opening_z),facing='+X',vertical=False,depth=body_length/2-charging_opening_x+usb_recess,clearance=0)
usb_cut=usb_cut.fuse(plug_body_cut)
body=body-usb_cut

body=body.fuse(tail_receiver-controller_cavity-controller_stop_clearance-usb_cut)
# Only the central rotor sleeve passes through the roof, hidden under its hub.
body=body.cut(Pos(0,0,56)*Cylinder(13.3,22))
# Curved shallow rebates retain pane shoulders beneath separate overlay rings.
for side in [-1,1]:
 rebate=(outer-Sphere(body_length/2-1.2)).intersect(Pos(0,side*body_width/2,0)*Rot(90,0,0)*Cylinder(21.55,body_width))
 body=body.cut(rebate)
# Internal lead-in within the existing front lens opening; outer outline unchanged.
tool_mouth_r=param('case_tool_mouth_inner_radius',27.0)
tool_mouth_d=param('case_tool_mouth_leadin_depth',1.2)
tool_mouth_end_r=param('case_tool_mouth_end_radius',25.5)
body=body.cut(Pos(front_plane+tool_mouth_d/2,0,0)*Rot(0,90,0)*Cone(tool_mouth_r,tool_mouth_end_r,tool_mouth_d))
if isinstance(body,ShapeList):body=Compound(children=list(body))
assert len(body.solids())==1, 'Internal supports must join shell'


# Positive half draws directly toward the fixed half along -Y.
# Integral rear guide is derived from the verified tongue-and-groove kit.
from splitjoint import PrinterBedV1,split_for_bed_v1
def solid_shape(s):
 return Compound(children=list(s)) if isinstance(s,ShapeList) else s
service_split_axis='y'
service_fastener_axis='y'
service_plane=param('service_split_y',0.0)
case_clamp_front_x=param('case_clamp_front_x',-35.0)
case_clamp_front_z=param('case_clamp_front_z',12.0)
case_clamp_rear_x=param('case_clamp_rear_x',21.5)
case_clamp_rear_z=param('case_clamp_rear_z',-32.2)
case_clamp_through_t=param('case_clamp_through_t',3.0)
case_clamp_receiver_t=param('case_clamp_receiver_t',5.0)
case_clamp_engagement=param('case_clamp_engagement',4.0)
case_front_pad_w=param('case_front_pad_width',8.0)
case_front_pad_h=param('case_front_pad_height',7.0)
case_rear_pad_w=param('case_rear_pad_width',7.0)
case_rear_pad_h=param('case_rear_pad_height',5.0)
case_root_web_t=param('case_root_web_thickness',6.0)
case_front_web_x=param('case_front_web_x',-37.75)
case_front_web_w=param('case_front_web_width',3.5)
case_front_web_top=param('case_front_web_top_z',34.0)
case_rear_web_end=param('case_rear_web_end_x',36.5)
case_rear_web_z=param('case_rear_low_web_centre_z',-33.45)
case_rear_web_h=param('case_rear_low_web_height',2.5)
case_root_overlap=param('case_root_overlap',0.2)
guide_x=param('closure_alignment_inner_x',37.5)
guide_z=param('closure_alignment_z',18.0)
guide_male_h=param('closure_alignment_tongue_height',6.0)
guide_back_h=param('closure_alignment_backing_height',9.0)
guide_half_y=param('case_guide_backing_half_y',8.0)
guide_r=param('case_guide_radial_limit',46.9)
guide_gap=param('case_guide_clearance',0.2)
case_joint_gap=param('case_joint_keepout_gap',0.6)
full_body=body
half_depth=body_width+2
lower_shape=solid_shape(full_body.intersect(Pos(0,-half_depth/2,0)*Box(body_length+4,half_depth,body_height+4)))
cap_shape=solid_shape(full_body.intersect(Pos(0,half_depth/2,0)*Box(body_length+4,half_depth,body_height+4)))
fixed_roof=solid_shape(full_body.intersect(Pos(0,0,30)*Box(20,20,24)))
lower_shape=solid_shape(lower_shape.fuse(fixed_roof))
cap_shape=solid_shape(cap_shape.cut(Pos(0,0,30)*Box(20.6,20.6,24.6)))

# Tooling blank forces the kit's explicit split. Only the integral local joint
# profile/backing is retained, trimmed to the real curved inner wall.
guide_blank=Pos(guide_x+12,0,guide_z)*Box(24,32,28)
guide_result=split_for_bed_v1(guide_blank,bed=PrinterBedV1(100,32,100,margin=5),joint='tongue_groove',cuts={'y':[0]},material='PETG',clearance=guide_gap,inside_hint=(0,0,guide_z))
assert not guide_result.unjoined and not guide_result.problems
guide_parts=sorted(guide_result.pieces,key=lambda p:p.shape.center().Y)
guide_negative_blank=Pos(guide_x+12,-8,guide_z)*Box(24,16,28)
guide_positive_blank=Pos(guide_x+12,8,guide_z)*Box(24,16,28)
guide_male_tool=solid_shape(guide_parts[0].shape.cut(guide_negative_blank))
guide_female_tool=solid_shape(guide_positive_blank.cut(guide_parts[1].shape))
guide_back_mask=Sphere(body_length/2).intersect(Pos(guide_x+12,0,guide_z)*Box(48,2*guide_half_y,guide_back_h))
guide_tongue_mask=Sphere(guide_r).intersect(Pos(guide_x+12,0,guide_z)*Box(48,2*guide_half_y,guide_male_h))
guide_pocket_mask=Sphere(guide_r+guide_gap).intersect(Pos(guide_x+12,0,guide_z)*Box(48,2*guide_half_y,guide_male_h+2*guide_gap))
guide_fixed=solid_shape(guide_negative_blank.intersect(guide_back_mask)).fuse(solid_shape(guide_male_tool.intersect(guide_tongue_mask)))
guide_receiver=solid_shape(guide_positive_blank.intersect(guide_back_mask)).cut(solid_shape(guide_female_tool.intersect(guide_pocket_mask)))
guide_fixed=solid_shape(guide_fixed);guide_receiver=solid_shape(guide_receiver)
assert len(guide_fixed.solids())==1 and len(guide_receiver.solids())==1
guide_entry=param('closure_alignment_entry_chamfer',0.5)
guide_tip_edges=[]
for face in guide_fixed.faces():
 if abs(face.center().Y-6)<1e-5 and face.normal_at().Y>.99:guide_tip_edges.extend(face.edges())
assert len(guide_tip_edges)==4
guide_fixed=chamfer(guide_tip_edges,length=guide_entry)
assert len(guide_fixed.solids())==1
lower_shape=solid_shape(lower_shape.fuse(guide_fixed))
cap_shape=solid_shape(cap_shape.fuse(guide_receiver))
seam_hardware=[]
service_joint_lengths=[]
case_clamp_joints=[]
service_lug_keepouts=[Pos((guide_x+50)/2,0,guide_z)*Box(50-guide_x+2*case_joint_gap,120,guide_back_h+2*case_joint_gap)]
for index,(x,z,w,h) in enumerate([(case_clamp_front_x,case_clamp_front_z,case_front_pad_w,case_front_pad_h),(case_clamp_rear_x,case_clamp_rear_z,case_rear_pad_w,case_rear_pad_h)]):
 front=Pos(x,case_clamp_through_t/2,z)*Box(w,case_clamp_through_t,h)
 back=Pos(x,-case_clamp_receiver_t/2,z)*Box(w,case_clamp_receiver_t,h)
 if index==0:
  web_low=z+h/2-case_root_overlap
  pos_web=Pos(case_front_web_x,case_root_web_t/2,(web_low+case_front_web_top)/2)*Box(case_front_web_w,case_root_web_t,case_front_web_top-web_low)
  neg_web=Pos(case_front_web_x,-case_clamp_receiver_t/2,(z+case_front_web_top)/2)*Box(case_front_web_w,case_clamp_receiver_t,case_front_web_top-z)
 else:
  web_start=x+w/2-case_root_overlap
  # The long root web sits below, rather than through, the XIAO support.
  pos_web=Pos((web_start+case_rear_web_end)/2,case_root_web_t/2,case_rear_web_z)*Box(case_rear_web_end-web_start,case_root_web_t,case_rear_web_h)
  thin_web=Pos((x+web_start)/2,case_clamp_through_t/2,case_rear_web_z)*Box(web_start-x+case_root_overlap,case_clamp_through_t,case_rear_web_h)
  pos_web=pos_web.fuse(thin_web)
  neg_web=Pos((x+case_rear_web_end)/2,-case_clamp_receiver_t/2,case_rear_web_z)*Box(case_rear_web_end-x,case_clamp_receiver_t,case_rear_web_h)
 front=solid_shape(front.fuse(pos_web).intersect(outer))
 if index==0:
  front_wire_edge=param('closure_front_wire_relief_x',-34.0)
  front_wire_top=param('closure_front_wire_relief_top_z',10.0)
  front=solid_shape(front.cut(Pos(front_wire_edge+2.25,case_clamp_through_t/2,front_wire_top-1.1)*Box(4.5,case_clamp_through_t+0.2,2.2)))
 if index==1:
  rear_wire_edge=param('case_rear_wire_edge_x',24.4)
  rear_wire_low=param('case_rear_wire_relief_low_z',-31.8)
  wire_relief=Pos(rear_wire_edge+1,case_clamp_through_t/2,rear_wire_low+1.3)*Box(2,case_clamp_through_t+0.2,2.6)
  front=solid_shape(front.cut(wire_relief))
 back=solid_shape(back.fuse(neg_web).intersect(outer))
 sj=make_screw_joint_v1(size='M2',at=Location((x,case_clamp_through_t,z),(-90,0,0)),through=[(front,case_clamp_through_t)],seat='surface',head='socket_cap',engage_depth=case_clamp_engagement,into=back,termination='through',material='PETG',print_axis='vertical',label='case-normal-clamp-'+str(index),finish='stainless')
 lower_shape=solid_shape(lower_shape.fuse(back,sj.bosses).cut(sj.engage_cuts))
 cap_shape=solid_shape(cap_shape.fuse(front).cut(sj.through_cuts[0]))
 seam_hardware.append(sj.hardware);service_joint_lengths.append(sj.screw_length_mm);case_clamp_joints.append(sj)
 bb=Compound(children=[front,back]).bounding_box()
 service_lug_keepouts.append(Pos(bb.center().X,0,bb.center().Z)*Box(bb.size.X+2*case_joint_gap,120,bb.size.Z+2*case_joint_gap))
 print('Normal-Y case clamp',index,sj.screw_length_mm,'engagement',sj.engage_depth_mm,'boss',sj.boss_length_mm,'protrusion',sj.screw_protrusion_mm,'land',sj.head_land_mm)
assert len(lower_shape.solids())==1 and len(cap_shape.solids())==1
print('Integral guide',guide_result.report)
publish('case_front_screw',seam_hardware[0],'前口锁壳螺钉',role='fastener',material='stainless_steel')
publish('case_rear_screw',seam_hardware[1],'底口后锁壳螺钉',role='fastener',material='stainless_steel')
body=lower_shape
window_pale_blue='#C9EAF8'
body.color=srgb(ts.body_sky_blue)
publish('fuselage',body,'天蓝色机身',material='petg')
publish('suspension_screw',joint.hardware,'吊杆承重螺栓螺母',material='stainless_steel',role='fastener')
