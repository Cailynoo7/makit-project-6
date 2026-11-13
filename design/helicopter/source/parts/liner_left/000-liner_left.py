f=part('fuselage'); cap=part('fuselage_cap')
outer_r=param('liner_outer_radius',47.45)
liner_t=param('liner_thickness',0.5)
inner_r=outer_r-liner_t
base=(Sphere(outer_r)-Sphere(inner_r)) & Pos(6,0,9)*Box(88,110,80)
base=base-Pos(0,0,0)*Rot(90,0,0)*Cylinder(22.5,120)
base=base-Pos(34,0,-26)*Box(52,110,20)
base=base-Pos(0,0,42)*Cylinder(15,28)
features=f.body.fuse(cap.body) & Sphere(47.55)
for shift in [(0,0,0),(.4,0,0),(-.4,0,0),(0,.4,0),(0,-.4,0),(0,0,.4),(0,0,-.4)]:base=base-Pos(*shift)*features
left_skid=Pos(0,f.skid_rail_y,f.skid_rail_z)*part('skid_left').body
right_skid=Pos(0,-f.skid_rail_y,f.skid_rail_z)*part('skid_right').body
tail=Pos(47.5,0,-3.75)*part('tail').body
extra=[left_skid,right_skid,tail,part('window_retainer_left').body,part('window_retainer_right').body]
for n in ['skid_retainer_left','skid_retainer_right','skid_retainer_left_aft','skid_retainer_right_aft']:extra.append(part(n).body)
for h in f.seam_hardware:
 b=h.bounding_box();extra.append(Pos((b.min+b.max)/2)*Box(b.size.X+1.2,b.size.Y+1.2,b.size.Z+1.2))
for shape in extra:
 for shift in [(0,0,0),(.4,0,0),(-.4,0,0),(0,.4,0),(0,-.4,0),(0,0,.4),(0,0,-.4)]:base=base-Pos(*shift)*shape

gap=param('liner_centre_gap',1.5)
lower_raw=base & Pos(0,0,2)*Box(110,110,40)
upper_raw=base & Pos(0,0,39)*Box(110,110,22)
left=lower_raw & Pos(0,25.75,0)*Box(110,48.5,120)
fore_raw=Compound(children=[s for s in lower_raw.solids() if s.volume>100 and s.center().X<0])
aft_raw=Compound(children=[s for s in lower_raw.solids() if s.volume>100 and s.center().X>0])
body=sorted([s for s in left.solids() if s.center().X<0],key=lambda s:s.volume)[-1]
body.color=srgb('#A8AEB6')
publish('liner_left',body,'左前贴壳均热片',material='aluminum')
print('fore left metal equivalent area mm2',body.volume/liner_t)
