from math import sqrt
r=param('head_max_radius',1.4)
length=param('head_max_length',7.5)
x=param('liner_probe_anchor_x',34.0)
z=param('liner_probe_anchor_z',10.5)
liner_r=part('liner_left').inner_r
y=sqrt(liner_r**2-x**2-z**2)
n=Vector(x,y,z).normalized()
direction=Vector(-n.Y,n.X,0).normalized()
centre=n*(liner_r-r-.2)
body=Solid.make_cylinder(r,length,Plane(origin=centre-direction*length/2,z_dir=direction))
body.color=srgb('#40342E')
publish('ntc_shell_reference',body,'壳体探头上限包络',role='reference')
