p=part('battery_end_pad_front')
t=param('end_pad_thickness',2.3)
body=mirror(p.body,about=Plane.XZ)
publish('battery_end_pad_rear',body,'后端缓冲垫',material='silicone')