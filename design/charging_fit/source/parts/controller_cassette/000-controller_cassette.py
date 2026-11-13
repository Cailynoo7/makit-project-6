# cell: controller_cassette
f=part('coupon_shell')
charging_frame=f.charging_frame
wire_relief=param('controller_wire_relief_diameter',3.0)
floor=param('cassette_lower_face_z',-33.5)
body=f.controller_cut-charging_frame*Pos(f.controller_pcb_x-2.2,0,-8.0)*Rot(0,90,0)*Cylinder(wire_relief/2,4)
body=body-charging_frame*Pos(0,0,floor-50)*Box(100,100,100)
wire_r=param('solder_wire_relief_radius',1.0)
for wx,wy in [(18.1361,7.62),(18.1361,-7.62),(33.3761,-7.62)]:
 body=body-Pos(wx,wy,-26.2)*Cylinder(wire_r,4.2)
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
publish('controller_cassette',body,'一体承托XIAO卡座',material='petg')
