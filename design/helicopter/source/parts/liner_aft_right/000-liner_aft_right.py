p=part('liner_left')
gap=param('centre_gap',1.5)
a=p.lower_raw & Pos(0,-(50+gap)/2,0)*Box(110,50-gap,120)
body=sorted([s for s in a.solids() if s.center().X>0],key=lambda s:s.volume)[-1]
publish('liner_aft_right',body,'右后贴壳均热片',material='aluminum')