# cell: window_retainer_left
# cell: window_retainer_left
# cell: window_retainer_left
# cell: window_retainer_left
w=part('window_left')
f=part('fuselage')
press=part('button_left')
slot=param('retainer_cable_slot_width',8.0)
seat_wall=param('retainer_stop_wall',1.6)
bridge_width=param('retainer_stop_bridge_width',14.0)
bridge_wall=param('retainer_stop_bridge_wall',2.4)
R=f.body_width/2
body=w.retainer.cut(Pos(0,f.body_width/2-17,15)*Box(slot,4,12))
# Removable rear stop lets the cap install from inside before the clamp.
radial_gap=param('retainer_stop_radial_clearance',0.2)
seat_overhang=param('retainer_stop_outer_overhang',1.0)
stop_outer=press.radius+press.flange_overhang
stop_inner=press.radius+radial_gap
zone=Pos(0,R,0)*Rot(90,0,0)*(Cylinder(stop_outer,2*R)-Cylinder(stop_inner,2*R+2))
seat=(Pos(0,-press.travel,0)*(Sphere(R-press.thick-1.5)-Sphere(R-press.thick-1.5-seat_wall)))&zone
# Bridge runs below both PCB and its guide-rail bottom stop; cable exits above.
bridge=Pos(0,R-11.65,-12)*Box(bridge_width,10.7,bridge_wall)
webs=[Pos(sx*5,R-7.3,-3.8)*Box(1.6,1.6,18.6) for sx in [-1,1]]
back_bridge_z=param('retainer_rear_bridge_z',-5.0)
rear_bar=Pos(0,R-17,back_bridge_z)*Box(23,2,2.4)
rear_pads=[Pos(sx*5,R-15,-2.2)*Box(2.4,2.2,12.4) for sx in [-1,1]]
ledge=Pos(0,R-14.05,-7.8)*Box(14,2.7,1.2)
stop=seat.fuse(bridge,*webs,rear_bar,*rear_pads,ledge)
body=body.fuse(stop)
assert len(body.solids())==1
body.color=srgb('#FFFFFF')
publish('window_retainer_left',body,'左圆窗压环及限位',material='petg')
