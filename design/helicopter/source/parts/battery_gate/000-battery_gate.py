c=part('battery_cradle')
wire_r=param('terminal_wire_relief_radius',1.5)
body=c.gate-Pos(0,c.end_y,c.end_z+c.end_bar_h/2)*Rot(90,0,0)*Cylinder(wire_r,c.end_bar_t+2)
assert len(body.solids())==1
body.color=srgb('#FFFFFF')
publish('battery_gate',body,'电池可拆端挡',material='petg')