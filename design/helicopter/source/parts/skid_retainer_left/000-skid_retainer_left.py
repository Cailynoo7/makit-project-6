s=part('skid_left')
f=part('fuselage')
edge=param('clamp_edge_fillet',0.2)
caps=[fillet(c.edges().filter_by(GeomType.CIRCLE),edge) for c in s.caps]
body=Pos(0,f.skid_rail_y,f.skid_rail_z)*caps[0]
body.color=srgb('#FFFFFF')
publish('skid_clamps_left',body,'左前曲面压帽',material='petg')
