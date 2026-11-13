wall=param('reflector_wall',1.6)
top_z=param('reflector_top_z',-4.0)
bottom_z=param('reflector_bottom_z',-25.5)
top_front=param('reflector_top_front_x',-39.0)
bottom_front=param('reflector_bottom_front_x',-28.0)
rear_x=param('reflector_rear_x',-14.0)
top_half=param('reflector_top_half_width',18.0)
bottom_half=param('reflector_bottom_half_width',11.0)
def section(z,front,rear,half):
 return Pos(0,0,z)*Polygon((front,-half),(rear,-half),(rear,half),(front,half),align=None)
outer=loft([section(bottom_z,bottom_front,rear_x,bottom_half),section(top_z,top_front,rear_x,top_half)])
inner=loft([section(bottom_z-.2,bottom_front+wall,rear_x-wall,bottom_half-wall),section(top_z+.2,top_front+wall,rear_x-wall,top_half-wall)])
body=outer-inner
# A permanent open centre channel clears the cradle's hard locating outrigger.
body=body-Pos(rear_x,0,-15)*Box(5,8,32)
# Hidden front diffuse port; white internal visor hides a direct source view.
port_z=param('front_mix_port_z',-14.0)
body=body-Pos(-35,0,port_z)*Box(14,16,2.0)
visor=Pos(-35.5,0,-10.5)*Rot(0,25,0)*Box(6,18,wall)
body=body.fuse(visor)
# Two front-facing adhesive lands release toward the nose; no hooked shell feet.
pad_t=param('bracket_bond_pad_thickness',1.6)
pad_gap=param('bracket_bond_gap',0.2)
for side in [-1,1]:
 pad=Pos(-26-pad_gap-pad_t/2,side*18,-4)*Box(pad_t,4,2)
 body=body.fuse(pad)
body=Compound(children=list(body.solids()))
# Clear internal lands with0.5mm envelope, retaining one optical insert.
clearance=param('optical_hard_clearance',0.5)
support_source=part('internal_carrier')
supports=[support_source.led_brackets[side]-Pos(-26,side*15,-4)*Cylinder(0.8,4) for side in [-1,1]]
clear_shapes=[part(name).body for name in ['internal_carrier','battery_cradle','battery_gate','fuselage']]+supports
for shape in clear_shapes:
 for v in [(0,0,0),(clearance,0,0),(-clearance,0,0),(0,clearance,0),(0,-clearance,0),(0,0,clearance),(0,0,-clearance)]:
  body=body-Pos(*v)*shape
# Nose-service cylinder and inverse sweep of fixed internal lands.
service_r=param('nose_service_clear_radius',25.0)
body=body & Pos(-25,0,0)*Rot(0,90,0)*Cylinder(service_r,100)
feature=part('fuselage').body & Pos(-25,0,-12)*Box(55,50,36)
for dx in range(0,29,2):
 body=body-Pos(dx,0,0)*feature
# Remove only disconnected trimming crumbs: they have no optical/support function.
fragments=sorted(body.solids(),key=lambda s:s.volume,reverse=True)
assert fragments[0].volume>1000
body=fragments[0]
assert len(body.solids())==1
join_length=param('support_join_length',1.5)
join_width=param('support_join_width',4.0)
join_height=param('support_join_height',2.0)
joins=[Pos(-26.35,side*18,-4)*Box(join_length,join_width,join_height) for side in [-1,1]]
body=body.fuse(*supports,*joins)
assert len(body.solids())==1
body.color=srgb('#FFFFFF')
publish('optical_reflector',body,'一体反光罩与灯源支座',material='asa')
