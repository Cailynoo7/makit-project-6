p=part('battery_strap_front')
c=part('battery_cradle')
w=param('strap_width',10.0)
body=Pos(0,-2*c.station,0)*p.body
publish('battery_strap_rear',body,'后电池绑带',material='nylon')