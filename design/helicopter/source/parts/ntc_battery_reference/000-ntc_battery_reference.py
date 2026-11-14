r=param('head_max_radius',1.4)
length=param('head_max_length',7.5)
x=param('cell_probe_axis_x',11.0)
y=param('cell_probe_axis_y',-18.0)
z=part('internal_carrier').pack_cell_z
body=Pos(x,y,z)*Rot(90,0,0)*Cylinder(r,length)
body.color=srgb('#40342E')
publish('ntc_battery_reference',body,'电芯探头上限包络',role='reference')
