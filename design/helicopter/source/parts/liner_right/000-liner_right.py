p=part('liner_left')
gap=param('liner_split_gap',1.5)
a=p.lower_raw & Pos(0,-(50+gap)/2,0)*Box(110,50-gap,120)
ss=[s for s in a.solids() if s.center().X<0]
body=sorted(ss or list(a.solids()),key=lambda s:s.volume)[-1]
publish('liner_right',body,'右前贴壳均热片',material='aluminum')