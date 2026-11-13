p=part('thermal_bridge_left')
t=param('contact_wall',1.0)
body=p.rear_fixed
publish('thermal_aft_shoe_left',body,'固定导热接触座',material='aluminum')