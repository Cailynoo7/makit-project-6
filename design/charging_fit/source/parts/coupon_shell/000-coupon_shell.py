# Same spherical skin, port cutters, cassette and screw joints as the main enclosure.
from math import sqrt
from screwjoint import make_screw_joint_v1
body_length=param('cabin_diameter',100.0)
wall=param('shell_wall',2.4)
bottom_plane=param('bottom_plane',-36.25)
coupon_width=param('coupon_width',46.0)
coupon_height=param('coupon_height',20.25)
coupon_back_depth=param('coupon_back_depth',45.0)
outer=Sphere(body_length/2)
body=outer-Sphere(body_length/2-wall)
body=body-Pos(0,0,bottom_plane-50)*Box(180,180,100)
body=body-Pos(0,0,bottom_plane+1.1)*Cylinder(63.75/2+0.25,2.2)
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
crop=Pos(32.5,0,bottom_plane+coupon_height/2)*Box(coupon_back_depth,coupon_width,coupon_height)
body=body.intersect(crop)
assert len(body.solids())==1
body.color=srgb('#87CEEB')
publish('coupon_shell',body,'局部充电口球壳',material='petg')
