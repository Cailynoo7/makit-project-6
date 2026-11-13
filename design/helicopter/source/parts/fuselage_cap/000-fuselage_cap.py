f=part('fuselage')
reveal=param('cap_seam_reveal',0.12)
skin_t=param('cap_minimum_outer_skin',1.2)
R=f.body_width/2
region=Pos(0,0,(R+f.service_plane)/2)*Box(2*R+2,2*R+2,R-f.service_plane)
envelope=f.outer.intersect(region)
envelope=envelope.cut(Pos(f.front_plane-60,0,0)*Box(120,160,160))
envelope=envelope.cut(Pos(0,0,56)*Cylinder(13.3,22))
inside_void=Sphere(R-skin_t).intersect(region).cut(f.cap_shape)
if not hasattr(inside_void,'wrapped'): inside_void=Compound(children=list(inside_void))
body=envelope.cut(inside_void).fix()
rim_r=((f.body_height/2)**2-f.service_plane**2)**0.5-0.65
rim=Pos(0,0,f.service_plane+reveal/2)*(Cylinder(50,reveal)-Cylinder(rim_r,reveal+1))
body=body.cut(rim)
assert len(body.solids())==1
body.color=srgb('#87CEEB')
publish('fuselage_cap',body,'天蓝色可拆机身上盖',material='petg')
