p=part('thermal_bridge_left');c=part('internal_carrier')
t=param('installed_putty_gap',0.1)
r=p.metal_r
def norm(s):return Compound(children=s) if isinstance(s,list) else s
ring=Sphere(r+t)-Sphere(r)
k=(r+t)/r
fore=norm(norm(ring & p.fore_foot.scale(k)) & part('liner_left').body.scale((r+t)/47.45))
aft=norm(norm(ring & p.rear_foot.scale(k)) & part('liner_aft_left').body.scale((r+t)/47.45))
cap=norm(norm(ring & p.cap_foot.scale(k)) & part('cap_liner_left').body.scale((r+t)/47.45))
root=norm(norm((Pos(0,0,-t)*p.left) & (Pos(0,0,t)*part('heat_spreader').body)) & Pos(c.heat_x,0,3+t/2)*Box(20,40,t))
cz=getattr(p,'shoe_top_z',14.9)+t/2
fx,fy=getattr(p,'fore_bolt',(c.heat_x,28))
ax,ay=getattr(p,'aft_bolt',(29.5,28.5))
couple_fore=norm(norm((Pos(0,0,-t)*p.left) & (Pos(0,0,t)*p.fore_fixed)) & Pos(fx,fy,cz)*Box(10,12,t))
couple_aft=norm(norm((Pos(0,0,-t)*p.left) & (Pos(0,0,t)*p.rear_fixed)) & Pos(ax,ay,cz)*Box(10,12,t))
couple_cap=norm(norm((Pos(0,0,-t)*p.upper_raw) & (Pos(0,0,t)*p.left)) & Pos(c.heat_x,20,26.05)*Box(12,8,t))
for name,shape in [('root',root),('fore',fore),('aft',aft),('cap',cap),('couple_fore',couple_fore),('couple_aft',couple_aft),('couple_cap',couple_cap)]:
 assert shape.volume>0
 publish('thermal_'+name+'_pad_left',shape,'左导热界面层',role='reference',material='silicone')
