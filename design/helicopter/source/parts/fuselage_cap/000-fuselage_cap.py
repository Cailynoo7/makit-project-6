f=part('fuselage')
reveal=param('cap_seam_reveal',0.12)
body=f.cap_shape
rim_r=f.body_width/2-0.65
body=body-Pos(0,f.service_plane+reveal/2,0)*Rot(90,0,0)*(Cylinder(f.body_width/2,reveal)-Cylinder(rim_r,reveal+1))
assert len(body.solids())==1
body.color=srgb('#87CEEB')
publish('fuselage_cap',body,'可拆机壳半边',material='petg')
