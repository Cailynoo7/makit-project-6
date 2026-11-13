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
seam_band=Pos(0,0,30)*Box(body_length+2,body_width+2,16)
inner=inner.cut(seam_band.cut(Sphere(body_length/2-4.4)))
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
bridge=(Pos(0,0,31.5)*Box(10,100,3)).intersect(outer)
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
carrier_mount_x=param('carrier_mount_x',26.0)
carrier_tab_radius=param('carrier_tab_radius',4.0)
raw_carrier=Pos(0,0,carrier_top-carrier_thickness)*extrude(RectangleRounded(carrier_width,carrier_depth,3),carrier_thickness)
carrier_front_y=param('carrier_front_mount_y',-6.0)
carrier_mounts=[(-carrier_mount_x,carrier_front_y),(24,-20)]
for x,y in carrier_mounts:
 raw_carrier=raw_carrier+Pos(x,y,carrier_top-carrier_thickness/2)*Cylinder(carrier_tab_radius,carrier_thickness)
 if x<0:
  raw_carrier=raw_carrier+Pos(x*0.88,y,carrier_top-carrier_thickness/2)*Box(8,6,carrier_thickness)
 else:
  raw_carrier=raw_carrier+Pos(21.5,-17.5,carrier_top-carrier_thickness/2)*Box(7,7,carrier_thickness)
carrier_joints=[]
carrier_hardware=[]
for x,y in carrier_mounts:
 sign=1 if x>0 else -1
 if x<0:
  shelf=Pos(x,y,carrier_top-6)*Cylinder(4,8)
  rib=(Pos(x-3,(y-50)/2,carrier_top-6)*Box(4,50+y,8)).intersect(outer)
  body=body.fuse(rib)
  body=body.fuse(shelf)
 else:
  rib=(Pos(x+3,(y-50)/2,carrier_top-6)*Box(4,50+y,8)).intersect(outer)
  body=body.fuse(rib)
  body=body.fuse(Pos(x,y,carrier_top-6)*Cylinder(4,8))
for i,(x,y) in enumerate(carrier_mounts):
 j=make_screw_joint_v1(size='M2',at=Location((x,y,carrier_top)),through=[(raw_carrier,carrier_thickness)],seat='surface',engage_depth=4.0,into=body,material='PETG',label='carrier-to-shell-'+str(i),finish='stainless')
 if j.boss_length_mm is not None and j.boss_length_mm>0: body=body.fuse(j.bosses)
 body=body.cut(j.engage_cuts)
 carrier_joints.append(j)
 carrier_hardware.append(j.hardware)
 print('Carrier shell mount',i,'screw',j.screw_length_mm,'boss length',j.boss_length_mm,'root',j.boss_root_offset_mm)
carrier_shell_cut=raw_carrier
for j in carrier_joints:
 carrier_shell_cut=carrier_shell_cut-j.through_cuts[0]
publish('carrier_shell_screws',carrier_hardware,'内部托架固定螺钉',role='fastener',material='stainless_steel')


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
# Two hidden ledges support the horizontal cassette without exterior screw holes.
for side in [-1,1]:
 mount_point=(charging_frame*Location((cx-3,side*17,-20))).position
 pad=Pos(mount_point.X,mount_point.Y,mount_point.Z+3.6)*Cylinder(3.0,4.0)
 rear_rib=(Pos(mount_point.X+6.0,mount_point.Y,mount_point.Z+3.6)*Box(14.0,4.0,4.0)).intersect(outer)
 body=body.fuse(rear_rib)
 body=body.fuse(pad)
controller_joints=[]
controller_hardware=[]
controller_cut=controller_raw
for side in [-1,1]:
 j=make_screw_joint_v1(size='M1.6',at=charging_frame*Location((cx-3,side*17,-20),(0,-90,0)),through=[(controller_raw,1.6)],seat='surface',engage_depth=3.0,into=body,material='PETG',print_axis='vertical',head='socket_cap',label='controller-'+str(side),finish='stainless')
 body=body+j.bosses-j.engage_cuts
 controller_cut=controller_cut-j.bosses-j.through_cuts[0]
 controller_cut=controller_cut-charging_frame*Pos(cx-4,side*17,-20)*Rot(0,90,0)*Cylinder(2.0,2.0)
 controller_cut=controller_cut.intersect(Sphere(body_length/2-2.0))
 controller_joints.append(j)
 controller_hardware.append(j.hardware)
from portcut import port_cut,PortSpec
usb_cut=port_cut('usb_c',at=(charging_opening_x,0,charging_opening_z),facing='+X',vertical=False,depth=12,clearance=0.15,recess=usb_recess)
plug_body_cut=port_cut(PortSpec('rounded',13.3,7.3,usb_plug_corner_radius),at=(body_length/2,0,charging_opening_z),facing='+X',vertical=False,depth=body_length/2-charging_opening_x+usb_recess,clearance=0)
usb_cut=usb_cut.fuse(plug_body_cut)
body=body-usb_cut
publish('controller_mount_screws',controller_hardware,'充电基板卡座螺钉',role='fastener',material='stainless_steel')
body=body.fuse(tail_receiver-controller_cavity-controller_stop_clearance-usb_cut)
# Only the central rotor sleeve passes through the roof, hidden under its hub.
body=body.cut(Pos(0,0,56)*Cylinder(13.3,22))
# Curved shallow rebates retain pane shoulders beneath separate overlay rings.
for side in [-1,1]:
 rebate=(outer-Sphere(body_length/2-1.2)).intersect(Pos(0,side*body_width/2,0)*Rot(90,0,0)*Cylinder(21.55,body_width))
 body=body.cut(rebate)
assert len(body.solids())==1, 'Internal supports must join shell'

# Shared thermal layout is read by the removable carrier and the cap keepout.
heat_plan_width=param('heat_plan_width',32.0)
heat_plan_height=param('heat_plan_height',20.0)
heat_plan_thickness=param('heat_plan_thickness',2.0)
heat_plan_frame=Location((-26,0,7),(0,45,0))
thermal_keepouts=[heat_plan_frame*extrude(RectangleRounded(heat_plan_height,heat_plan_width,4),heat_plan_thickness/2,both=True)]
for side in [-1,1]:
 thermal_keepouts.append(heat_plan_frame*Pos(0,side*13.5,-2.6)*Box(12,3,3.2))
 pts=[(-20.5,side*13.5,-7),(-24,side*13.5,-3),(-27.98,side*13.5,5.02)]
 for a,b in zip(pts,pts[1:]):
  va,vb=Vector(a),Vector(b)
  thermal_keepouts.append(Solid.make_cylinder(1.5,(vb-va).length,Plane(origin=va,z_dir=vb-va)))
from splitjoint import PrinterBedV1,split_for_bed_v1,publish_split_v1
service_plane=param('enlarged_service_split_z',25.0)

body=body.cut(joint.engage_cuts)
full_body=body
service_keepouts=[raw_carrier,Pos(0,0,1)*Box(40,36,13),Pos(23,0,24)*Cylinder(15.2,21),Pos(0,0,49)*Cylinder(16.8,32),Pos(23,0,35.3)*Cylinder(5.5,5)]+thermal_keepouts
for side in [-1,1]:
 service_keepouts.append(Pos(0,side*38,0)*Rot(90,0,0)*Cylinder(17.8,14))
# This is a per-piece planning envelope, not a claimed printer model.
service_split=split_for_bed_v1(full_body,bed=PrinterBedV1(120,120,82,margin=5),joint='screw',screw='M2',cuts={'z':[service_plane]},pitch=60,inside_hint=(0,0,0),keepouts=tuple(service_keepouts),material='PETG')
print(service_split.report)
assert not service_split.unjoined and not service_split.problems and not service_split.assembly_blocked
assert len(service_split.pieces)==2
lower_shape=min(service_split.pieces,key=lambda p:p.shape.bounding_box().min.Z).shape.intersect(outer)
cap_shape=max(service_split.pieces,key=lambda p:p.shape.bounding_box().min.Z).shape.intersect(outer)
seam_hardware=[]
def collect_split(oid,shape,label,**metadata):
 if metadata.get('role')=='fastener':
  if isinstance(shape,(list,tuple)): seam_hardware.extend(shape)
  else: seam_hardware.append(shape)
publish_split_v1(service_split,collect_split,material='petg')
assert seam_hardware
publish('service_screws',seam_hardware,'机身检修固定螺钉',role='fastener',material='stainless_steel')

body=lower_shape
window_pale_blue='#C9EAF8'
body.color=srgb(ts.body_sky_blue)
publish('fuselage',body,'天蓝色机身',material='petg')

publish('suspension_screw',joint.hardware,'吊杆承重螺栓螺母',material='stainless_steel',role='fastener')