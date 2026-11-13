solder_gap=param('lead_mounting_clearance',0.05)
# Exact C2837530 manufacturer drawing; conservative solid case envelope.
# Drawing-derived reference, not an original vendor STEP. No footprint changes.
H=4.3
body_size=6.0
body_height=3.15
cover_height=0.3
plunger_d=3.5
base=Pos(0,0,body_height/2)*Box(body_size,body_size,body_height)
base.color=srgb('#303237')
cover=Pos(0,0,body_height+cover_height/2)*Box(body_size,body_size,cover_height)
cover.color=srgb('#BDC0C5')
plunger=Pos(0,0,(body_height+cover_height+H)/2)*Cylinder(plunger_d/2,H-body_height-cover_height)
plunger.color=srgb('#303237')
# Gull-wing contact envelope:9mm overall,4.5mm row pitch,0.7mm width,0.23mm thick.
# Bend location is an engineering envelope; the manufacturer land pattern owns pads.
profile=Plane.XZ*Polygon((2.8,0.45),(3.35,0.45),(3.95,0),(4.5,0),(4.5,0.23),(4.03,0.23),(3.43,0.68),(2.8,0.68),align=None)
lead=extrude(profile,0.35,both=True)
leads=[]
for sx in [-1,1]:
 for sy in [-1,1]:
  l=Pos(0,sy*2.25,0)*(lead if sx>0 else mirror(lead,about=Plane.YZ))
  l.color=srgb('#B9BCC3')
  leads.append(l)
body=Pos(0,0,solder_gap)*Compound([base,cover,plunger]+leads)
assert abs(body.bounding_box().max.Z-(H+solder_gap))<1e-6
publish('switch',body,'图纸开关装配参考',role='reference')