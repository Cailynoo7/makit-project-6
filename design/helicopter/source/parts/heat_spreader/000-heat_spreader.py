c=part('internal_carrier')
edge_relief=param('collector_edge_relief',0.2)
body=c.heat_cut
# Small deburring relief, outside the COB bond land.
body=body-Pos(c.heat_x-c.heat_height/2,0,c.heat_bottom)*Rot(90,0,0)*Cylinder(edge_relief,c.heat_width+2)
assert len(body.solids())==1
publish('heat_spreader',body,'COB铝集热板',material='aluminum')