p=part('thermal_bridge_left')
t=param('contact_wall',1.0)
body=p.fore_fixed
publish('thermal_fore_shoe_left',body,'固定导热接触座',material='aluminum')