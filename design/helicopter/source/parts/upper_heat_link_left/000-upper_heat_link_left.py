p=part('thermal_bridge_left')
t=param('lap_gap',0.1)
body=p.upper_raw
publish('upper_heat_link_left',body,'上盖左导热连接件',material='aluminum')