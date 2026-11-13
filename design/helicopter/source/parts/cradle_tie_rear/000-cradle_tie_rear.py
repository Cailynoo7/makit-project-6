p=part('cradle_tie_front')
t=param('tie_width',2.5)
body=mirror(p.body,about=Plane.XZ)
publish('cradle_tie_rear',body,'后托座扎带包络',role='reference',material='nylon')