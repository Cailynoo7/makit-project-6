tail_length=param('visible_tail_length',127.5)
root_radius=param('shoulder_radius',10.6136363636)
tip_radius=param('enlarged_tail_tip_radius',2.5)
fin_height=param('enlarged_fin_height',50.0)
fin_width=param('enlarged_fin_width',12.5)
fin_thickness=param('enlarged_fin_thickness',3.75)
root_x=param('shoulder_plane_x',47.5)
edge_radius=param('fin_edge_radius',0.45)
prop_axis_height=param('enlarged_prop_axis_height',17.5)
prop_aft_offset=param('enlarged_prop_aft_offset',1.875)
prop_pin_hole=param('enlarged_tail_prop_pin_hole',3.5)
def p(x,z):
 return (x*fin_width/10,z*fin_height/40)
half_outline=Wire([
 Line(p(-6,0),p(5,0)),
 Line(p(5,0),p(5,18)),
 ThreePointArc(p(5,18),p(4.4,19.6),p(3,20)),
 Bezier(p(3,20),p(0.7,20),p(-1.3,19),p(-2,16)),
 Line(p(-2,16),p(-6,0))
])
half_plate=extrude(make_face(half_outline),fin_thickness/2,both=True)
full_plate=half_plate+mirror(half_plate,about=Plane.XZ)
full_plate=fillet(full_plate.edges().filter_by(Axis.Z,reverse=True),edge_radius)
fin=Pos(tail_length,0,0)*Rot(90,0,0)*full_plate
# Right horizontal trim fin reuses the identical half-outline at full size.
trim_half=fillet(half_plate.edges().filter_by(Axis.Z,reverse=True),edge_radius)
trim_fin=Pos(tail_length,0,0)*trim_half
body=Pos(tail_length/2,0,0)*Rot(0,90,0)*Cone(root_radius,tip_radius,tail_length)
body=body+fin+trim_fin
# Solid tapered boom and complete circular locating plug with a circular bearing shoulder.
plug_length=param('tail_plug_length',4.0)
plug_radius=param('tail_plug_radius',8.0)
key_gap=param('tail_plug_clearance',0.2)
key=Pos(-plug_length/2,0,0)*Rot(0,90,0)*Cylinder(plug_radius,plug_length)
flat_z=param('hidden_tail_key_flat_z',6.5)
key=key-Pos(-plug_length/2,0,flat_z+5)*Box(plug_length+2,2*plug_radius+2,10)
body=body.fuse(key)
receiver_slot=Pos(-2.10,0,0)*Rot(0,90,0)*Cylinder(plug_radius+key_gap,4.3)
receiver_slot=receiver_slot-Pos(-2.1,0,flat_z+key_gap+5)*Box(6,24,10)
cone_clearance=Pos(15,0,0)*Rot(0,90,0)*Cylinder(root_radius+0.45,30)
receiver=Pos(-2.85,0,0)*Rot(0,90,0)*Cylinder(root_radius+0.45,5.7)
receiver=receiver.cut(receiver_slot)
from screwjoint import make_screw_joint_v1
tail_lock_joints=[]
tail_lock_hardware=[]
boss_slide_cuts=[]
for i,y in enumerate([-4]):
 j=make_screw_joint_v1(size='M2',at=Location((-5.7,y,0),(0,-90,0)),through=[(receiver,1.45)],seat='surface',head='socket_cap',engage_depth=3.5,into=body,material='PETG',print_axis='horizontal',label='tail-internal-'+str(i),finish='stainless')
 if j.boss_length_mm is not None and j.boss_length_mm>0:
  body=body.fuse(j.bosses)
 body=body.cut(j.engage_cuts)
 receiver=receiver.cut(j.through_cuts[0])
 tail_lock_joints.append(j)
 tail_lock_hardware.append(j.hardware)
 print('Internal tail screw',j.screw_length_mm)
hole_back=fin_thickness/2-0.625
hole_start=-fin_thickness/2-5
body=body-Pos(tail_length+prop_aft_offset,(hole_start+hole_back)/2,prop_axis_height)*Rot(90,0,0)*Cylinder(prop_pin_hole/2,hole_back-hole_start)
connections={'right_trim_fin':'integral: same half-outline as vertical fin; fused to tail tip','tail_propeller_pin':'free: clearance-fit cosmetic pin; adhesive retention'}
connections['round_tail_joint']='circular visible shoulder;hidden keyed plug;one axial M2 screw on the fixed negative-Y half'
assert len(connections)==3
body_sky_blue='#87CEEB'
body.color=srgb(body_sky_blue)
publish('tail_lock_screws',tail_lock_hardware,'尾梁锁紧螺钉',role='fastener',material='stainless_steel')
publish('tail',body,'尾梁与尾翼',material='petg')
