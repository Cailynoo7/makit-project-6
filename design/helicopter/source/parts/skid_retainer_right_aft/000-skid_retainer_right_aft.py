s=part('skid_right')
f=part('fuselage')
edge=param('clamp_edge_fillet',0.2)
caps=[fillet(c.edges().filter_by(GeomType.CIRCLE),edge) for c in s.caps]
body=Pos(0,-f.skid_rail_y,f.skid_rail_z)*caps[1]
body.color=srgb('#FFFFFF')
publish('skid_clamp_right_aft',body,'右后曲面压帽',material='petg')
