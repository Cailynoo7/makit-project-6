# cell: heat_spreader
def build_thermal_bridge():
 # Monolithic metal thermal bridge: no separate liners, shoes or cap links.
 def cut_shape(shape,tool):
  if isinstance(shape,ShapeList): shape=Compound(children=list(shape))
  if isinstance(tool,ShapeList): tool=Compound(children=list(tool))
  result=shape.cut(tool)
  return Compound(children=list(result)) if isinstance(result,ShapeList) else result
 f=part('fuselage')
 h=part('internal_carrier')
 root_t=param('manifold_root_thickness',4.0)
 stem_w=param('manifold_stem_width',10.0)
 bridge_t=param('manifold_web_thickness',4.0)
 metal_r=param('manifold_outer_radius',46.85)
 contact_t=param('manifold_contact_thickness',1.0)
 # One-piece machined aluminium thermal bridge.
 root_w=param('root_plate_width',8.0)
 root_offset_x=param('collector_root_offset_x',-1.0)
 root_x=h.heat_x+root_offset_x
 root=Pos(root_x,17,3.1+root_t/2)*Box(root_w,10.0,root_t)
 stem=Pos(h.heat_x,20,15)*Box(stem_w,bridge_t,22)
 fore=Pos(h.heat_x,22.5,17)*Box(8,15,bridge_t)
 bar=Pos(2,24.5,19)*Box(64,bridge_t,10)
 rear=Pos(29.5,28.05,17)*Box(5,5.1,bridge_t)
 feet_shell=Sphere(metal_r)-Sphere(metal_r-contact_t)
 fore_foot=feet_shell & Pos(h.heat_x,26,18)*Box(stem_w,20,6)
 rear_foot=feet_shell & Pos(31.5,32,18.5)*Box(9,16,7)
 fore_foot=fore_foot & Pos(h.heat_x,40.15,18)*Box(30,19.7,20)
 rear_foot=rear_foot & Pos(32.5,40.45,18.5)*Box(20,19.1,20)
 cap_x=param('upper_contact_x',-17.0)
 cap_z=param('upper_contact_z',40.4)
 cap_foot=feet_shell & Pos(cap_x,25,cap_z)*Box(stem_w,45,3.2)
 cap_link=loft([Pos(h.heat_x,20,26.1)*Rectangle(stem_w,bridge_t),Pos(cap_x,18,40)*Rectangle(stem_w,bridge_t)])
 shoe_t=param('contact_shoe_thickness',2.0)
 fore_bolt=(h.heat_x,24.0);aft_bolt=(27.0,24.5)
 fore_fixed=fore_foot.fuse(Pos(h.heat_x,27.65,12.9)*Box(4,10.7,shoe_t),Pos(h.heat_x,33.3,16)*Box(4,6,5)) & Sphere(metal_r)
 rear_plate=Pos(28.5,29,12.9)*Box(7,11,shoe_t)
 rear_plate=cut_shape(rear_plate,Pos(25.5,33,12.9)*Box(3,6,shoe_t+2))
 rear_fixed=rear_foot.fuse(rear_plate,Pos(29.5,33.9,16)*Box(5,6,5)) & Sphere(metal_r)
 body=root.fuse(stem,fore,bar,rear,Pos(h.heat_x,24,19)*Cylinder(2.5,10),Pos(27,24.5,19)*Cylinder(2.5,10)) & Sphere(metal_r)

 upper_raw=cap_link.fuse(cap_foot) & Sphere(metal_r)
 # Open grooves permit disengagement inward without snagging existing wire guides.
 # Vertical release corridor for the J2/J12/J3 header housings (and mirrored J5/J6/J4).
 body=cut_shape(body,Pos(-1,23,19)*Box(22,1.4,14))
 # Remove clamp screws completely before retracting each bridge10.4mm inward.

 features=Compound(children=[f.lower_shape,f.cap_shape])
 for shift in [(0,0,0)]:
  body=cut_shape(body,Pos(*shift)*features)
  upper_raw=cut_shape(upper_raw,Pos(*shift)*features)
  fore_fixed=cut_shape(fore_fixed,Pos(*shift)*features)
  rear_fixed=cut_shape(rear_fixed,Pos(*shift)*features)
 # Driver corridors are wholly internal and open only after the top module is removed.
 body=cut_shape(body,Pos(-23,10.5,26.5)*Cylinder(1.8,47))
 assert len(body.solids())==1
 assert len(upper_raw.solids())==1
 assert len(fore_fixed.solids())==1
 assert len(rear_fixed.solids())==1
 join_t=param('integral_shoe_web_thickness',0.4)
 shoe_joins=[Pos(x,y,13.95)*Box(4,4,join_t) for x,y in [fore_bolt,aft_bolt]]
 body=body.fuse(fore_fixed,rear_fixed,*shoe_joins)
 assert len(body.solids())==1

 core_left=body
 cap_stem=upper_raw
 f=part('fuselage'); cap=part('fuselage_cap')
 outer_r=param('thermal_contact_outer_radius',47.45)
 liner_t=param('integral_contact_thickness',0.65)
 inner_r=outer_r-liner_t
 base=(Sphere(outer_r)-Sphere(inner_r)) & Pos(6,0,9)*Box(88,110,80)
 base=cut_shape(base,Pos(0,0,0)*Rot(90,0,0)*Cylinder(22.5,120))
 base=cut_shape(base,Pos(34,0,-26)*Box(52,110,20))
 base=cut_shape(base,Pos(0,0,42)*Cylinder(15,28))
 features=Compound(children=[f.lower_shape,f.cap_shape])
 for shift in [(0,0,0)]:base=base-Pos(*shift)*features
 left_skid=Pos(0,f.skid_rail_y,f.skid_rail_z)*part('skid_left').body
 right_skid=Pos(0,-f.skid_rail_y,f.skid_rail_z)*part('skid_right').body
 tail=Pos(47.5,0,-3.75)*part('tail').body
 extra=[left_skid,right_skid,tail,part('window_retainer_left').body,part('window_retainer_right').body]
 for n in ['skid_retainer_left','skid_retainer_right','skid_retainer_left_aft','skid_retainer_right_aft']:extra.append(part(n).body)
 for seam_hw in f.seam_hardware:
  b=seam_hw.bounding_box();extra.append(Pos((b.min+b.max)/2)*Box(b.size.X+1.2,b.size.Y+1.2,b.size.Z+1.2))
 for shape in extra:
  base=cut_shape(base,shape)

 lower_raw=base & Pos(0,0,2)*Box(110,110,40)
 contact_upper_raw=base & Pos(0,0,39)*Box(110,110,22)
 left=lower_raw & Pos(0,25.75,0)*Box(110,48.5,120)
 fore_contact=sorted([s for s in left.solids() if s.center().X<0],key=lambda s:s.volume)[-1]
 aft_contact=sorted([s for s in left.solids() if s.center().X>0],key=lambda s:s.volume)[-1]
 cap_region=contact_upper_raw & Pos(0,25.75,0)*Box(110,48.5,120)
 cap_contact=sorted(cap_region.solids(),key=lambda s:s.volume)[-1]

 cap_joint_t=param('integral_upper_web_thickness',0.4)
 cap_joint=Pos(h.heat_x,20,26.05)*Box(10,4,cap_joint_t)
 side=core_left.fuse(cap_stem,fore_contact,aft_contact,cap_contact,cap_joint)
 print('Thermal half solids',len(side.solids()))
 assert len(side.solids())==1,'Thermal half must be connected'
 root_gap_fill=param('integral_collector_root_fill',0.3)
 root_joins=[Pos(root_x,side_sign*14.5,3.05)*Box(8,5,root_gap_fill) for side_sign in [-1,1]]
 collector=h.heat_cut
 body=collector.fuse(side,mirror(side,about=Plane.XZ),*root_joins)
 rear_spine=loft([Pos(29.5,24.5,23.8)*Rectangle(5,4),Pos(27,24,30.7)*Rectangle(5,4)])
 body=body.fuse(rear_spine,mirror(rear_spine,about=Plane.XZ))
 edge_relief=param('collector_edge_relief',0.2)
 body=cut_shape(body,Pos(h.heat_x-h.heat_height/2,0,h.heat_bottom)*Rot(90,0,0)*Cylinder(edge_relief,h.heat_width+2))
 # A common radial envelope keeps all branches inside the original shell.
 body=body & Sphere(outer_r)
 # Clear the actual shell reinforcements once; keep parts separate as a compound.
 for shift in [(0,0,0)]:
  body=cut_shape(body,Pos(*shift)*features)
 # Open side channels are required for BOTH case halves and the fixed shaft.
 body=cut_shape(body,Pos(0,0,41.5)*Box(34.5,120,41))
 body=cut_shape(body,Pos(44,0,-3.75)*Box(18,120,24.5))
 for sign in [-1,1]:
  body=cut_shape(body,Pos(0,sign*50,-2.5)*Box(54,40,35))
 body=cut_shape(body,Pos(31,-49,-7)*Box(10,50,12))
 body=cut_shape(body,Pos(-30.5,-51,-16)*Box(10,46.8,30))
 if hasattr(f,'service_lug_keepouts'):
  for tool in f.service_lug_keepouts:
   body=cut_shape(body,tool)
 else:
  for seam_hw in f.seam_hardware:
   bb=seam_hw.bounding_box()
   body=cut_shape(body,Pos(bb.center().X,0,bb.center().Z)*Box(bb.size.X+8,120,bb.size.Z+8))
 # Preserve straight tool access on the bench and during side installation.
 for side_sign in [-1,1]:
  body=cut_shape(body,Pos(-23,side_sign*10.5,26.5)*Cylinder(1.8,47))
  body=cut_shape(body,Pos(-23,side_sign*20.5,24)*Cylinder(1.8,54))
 body=cut_shape(body,Pos(getattr(f,'frame_rear_x',24.0),0,f.carrier_top-f.carrier_thickness/2)*Box(5,120,6))
 for hardware in h.heat_hardware:
  body=cut_shape(body,hardware)
 mouth_chamfer=param('mount_hole_mouth_chamfer',0.25)
 for sign in [-1,1]:
  body=cut_shape(body,Pos(-23,sign*10.5,h.heat_bottom+h.heat_thickness-mouth_chamfer/2)*Cone(0.95,0.95+mouth_chamfer,mouth_chamfer))
 if isinstance(body,ShapeList): body=Compound(children=list(body))
 body=body.cut(Pos(-30.5,-51,-16)*Box(10,44,30))
 if isinstance(body,ShapeList): body=Compound(children=list(body))
 body=body.cut(Pos(31,-49,-7)*Box(10,50,12))
 if isinstance(body,ShapeList): body=Compound(children=list(body))
 print('Complete bridge solids',len(body.solids()))
 thermal_solids=sorted(body.solids(),key=lambda shape:shape.volume,reverse=True)
 trim_volume=sum(shape.volume for shape in thermal_solids[1:])
 assert trim_volume<=max(1.0,0.005*thermal_solids[0].volume) and all(shape.volume<=100 for shape in thermal_solids[1:]),'Disconnected thermal regions: '+str([(round(shape.volume,3),tuple(shape.bounding_box().min),tuple(shape.bounding_box().max)) for shape in thermal_solids])
 body=thermal_solids[0]
 assert len(body.solids())==1,'Complete thermal bridge must be one solid'
 contact_area_mm2=(fore_contact.volume+aft_contact.volume+cap_contact.volume)*2/liner_t
 print('Integral shell-contact equivalent area cm2',contact_area_mm2/100)
 body.color=srgb('#A8AEB6')

 return body,contact_area_mm2,trim_volume
body,blank_contact_area_mm2,trimmed_disconnected_volume_mm3=build_thermal_bridge()
publish('heat_spreader',body,'一体金属散热桥',material='aluminum')