# cell: button_left
# cell: button_left
s=part('fuselage')
radius=param('button_left_radius',10)
gap=param('button_left_clearance',0.25)
thick=param('button_left_pane_depth',3.5)
flange_overhang=param('button_left_flange_overhang',1.0)
def ell(ry):
 return Sphere(ry)
outer=ell(s.body_width/2)
inner=ell(s.body_width/2-thick)
region=Pos(s.window_x,s.body_width/2,s.window_z)*Rot(90,0,0)*Cylinder(radius,s.body_width)
body=(outer-inner)&region
flange=(ell(s.body_width/2-thick)-ell(s.body_width/2-thick-1.5))&Pos(s.window_x,s.body_width/2,s.window_z)*Rot(90,0,0)*Cylinder(radius+flange_overhang,s.body_width)
stem_setback=param('button_left_stem_setback',0.2)
travel=param('button_left_travel',0.45)
stem_radius=param('button_left_stem_radius',2.5)
stem_outer=s.body_width/2-1.0
stem_inner=s.body_width/2-8.0+stem_setback
stem=Pos(s.window_x,(stem_outer+stem_inner)/2,s.window_z)*Rot(90,0,0)*Cylinder(stem_radius,stem_outer-stem_inner)
body=body+flange+stem
icon=(Pos(0,1.4)*Circle(3.0)-Pos(0,1.4)*Circle(2.1))+Pos(0,-2.3)*Rectangle(1.8,2.2)+Pos(0,-4.0)*Rectangle(3.0,0.8)
engraving=(outer-ell(s.body_width/2-0.6))&Pos(s.window_x,s.body_width/2,s.window_z)*Rot(90,0,0)*extrude(icon,10,both=True)
body=body-engraving
body.color=srgb(s.window_pale_blue)
publish('button_left',body,'灯泡按钮',material='petg')
