p=part('thermal_bridge_left')
t=param('contact_wall',1.0)
body=mirror(p.rear_fixed,about=Plane.XZ)
publish('thermal_aft_shoe_right',body,'固定导热接触座',material='aluminum')