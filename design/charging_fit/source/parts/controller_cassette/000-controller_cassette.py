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
assert len(body.solids())==1
body.color=srgb('#87CEEB')
publish('controller_cassette',body,'XIAO尾根充电卡座',material='petg')