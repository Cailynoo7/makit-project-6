c=part('internal_carrier')
wire_d=param('led_wire_guide_diameter',1.6)
body=c.led_brackets[1]-Pos(-26,15,-4)*Cylinder(wire_d/2,4)
assert len(body.solids())==1
body.color=srgb('#FFFFFF')
publish('led_bracket_left',body,'耐温COB支座',material='asa')
