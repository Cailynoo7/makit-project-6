c=part('internal_carrier')
wire_r=param('terminal_wire_relief_radius',1.5)
body=c.pack_gate-Pos(0,c.pack_end_y,c.pack_end_z+c.pack_end_bar_h/2)*Rot(90,0,0)*Cylinder(wire_r,c.pack_end_bar_t+2)
assert len(body.solids())==1
body.color=srgb('#FFFFFF')
publish('battery_gate',body,'电池可拆端挡',material='petg')