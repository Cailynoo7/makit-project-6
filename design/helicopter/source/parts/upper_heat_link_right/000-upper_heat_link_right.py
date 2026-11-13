p=part('upper_heat_link_left')
t=param('lap_gap',0.1)
body=mirror(p.body,about=Plane.XZ)
publish('upper_heat_link_right',body,'上盖右导热连接件',material='aluminum')