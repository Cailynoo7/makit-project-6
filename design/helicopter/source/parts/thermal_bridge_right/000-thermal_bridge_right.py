p=part('thermal_bridge_left')
check_t=param('minimum_web',4.0)
body=p.right
publish('thermal_bridge_right',body,'右铝导热桥',material='aluminum')