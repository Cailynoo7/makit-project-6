p=part('liner_left')
gap=param('liner_split_gap',1.5)
a=p.upper_raw & Pos(0,-(50+gap)/2,0)*Box(110,50-gap,120)
body=sorted(a.solids(),key=lambda s:s.volume)[-1]
publish('cap_liner_right',body,'上盖右均热片',material='aluminum')