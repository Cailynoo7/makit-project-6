f=part('internal_carrier')
flange_r=param('pulley_flange_radius',4.9)
bore=param('motor_d_shaft_bore',3.0)
flat_y=param('motor_d_shaft_flat',1.0)
h=param('driver_pulley_height',4.0)
z=param('internal_belt_plane',35.3)
axis=f.motor_axis_x
body=Pos(axis,0,z)*Cylinder(flange_r,h)
groove=Torus(4.05,0.8)+(Cylinder(flange_r+1,1.6)-Cylinder(4.05,2.6))
body=body.cut(Pos(axis,0,z)*groove)
hole=Pos(axis,0,z)*Cylinder(bore/2,h+1)
hole=hole.intersect(Pos(axis,-5+flat_y,z)*Box(10,10,h+2))
body=body.cut(hole)
# Nominal D-profile. Calibrate print bore before assembly; epoxy spot provides
# axial retention only, D-flat transmits torque. Keep adhesive off gearbox.
body.color=srgb('#FFFFFF')
publish('drive_pulley',body,'3mm D轴小皮带轮',material='petg')
