# cell: thermal_bridge_left
from bd_warehouse.fastener import SocketHeadCapScrew
h=part('internal_carrier')
root_t=param('manifold_root_thickness',4.0)
stem_w=param('manifold_stem_width',10.0)
bridge_t=param('manifold_web_thickness',4.0)
metal_r=param('manifold_outer_radius',46.85)
contact_t=param('manifold_contact_thickness',1.0)
service_travel=param('service_inward_shift',10.4)
# A machined or brazed aluminium assembly, not a printed imitation of stock hardware.
root_w=param('root_plate_width',8.0)
root=Pos(h.heat_x+1,17,3.1+root_t/2)*Box(root_w,10.0,root_t)
stem=Pos(h.heat_x,20,15)*Box(stem_w,bridge_t,22)
fore=Pos(h.heat_x,22.5,17)*Box(8,15,bridge_t)
bar=Pos(2,24.5,19)*Box(64,bridge_t,10)
bypass=Pos(13.35,32,19.5)*Box(14,4,9)
for bx in [7.35,19.35]:
 bypass=bypass.fuse(Pos(bx,28.25,19.5)*Box(4,11.5,9))
bar=bar.fuse(bypass)
bar=bar-Pos(13.35,26,20)*Box(8.5,7.2,24)
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
contact_gap=param('shoe_contact_gap',0.1)
contact_clear=param('shoe_bolt_clearance',1.9)
contact_major=param('shoe_thread_major',1.6)
shoe_top_z=13.9
fore_bolt=(h.heat_x,24.0);aft_bolt=(27.0,24.5)
fore_fixed=fore_foot.fuse(Pos(h.heat_x,27.65,12.9)*Box(4,10.7,shoe_t),Pos(h.heat_x,33.3,16)*Box(4,6,5)) & Sphere(metal_r)
rear_plate=Pos(28.5,29,12.9)*Box(7,11,shoe_t)
rear_plate=rear_plate-Pos(25.5,33,12.9)*Box(3,6,shoe_t+2)
rear_fixed=rear_foot.fuse(rear_plate,Pos(29.5,33.9,16)*Box(5,6,5)) & Sphere(metal_r)
body=root.fuse(stem,fore,bar,rear,Pos(h.heat_x,24,19)*Cylinder(2.5,10),Pos(27,24.5,19)*Cylinder(2.5,10)) & Sphere(metal_r)
for x,y in [fore_bolt,aft_bolt]:
 body=body-Pos(x,y,19)*Cylinder(contact_clear/2,12)
 body=body-Pos(x,y,23.15)*Cylinder(1.7,1.7)
fore_fixed=fore_fixed-Pos(fore_bolt[0],fore_bolt[1],12.9)*Cylinder(contact_major/2,4)
rear_fixed=rear_fixed-Pos(aft_bolt[0],aft_bolt[1],12.9)*Cylinder(contact_major/2,4)
upper_raw=cap_link.fuse(cap_foot) & Sphere(metal_r)
# Open grooves permit disengagement inward without snagging existing wire guides.
body=body-Pos(13.35,24.5,24.135)*Rot(90,0,0)*Cylinder(param('shell_ntc_exit_channel_radius',4.0),40)
# Vertical release corridor for the J2/J12/J3 header housings (and mirrored J5/J6/J4).
body=body-Pos(-1,23,19)*Box(22,1.4,14)
# Remove clamp screws completely before retracting each bridge10.4mm inward.
body=body-Pos(h.heat_x,16.5,5.1)*Rot(0,0,90)*extrude(SlotOverall(6.4,2.4),4,both=True)
body=body-Pos(-23,12.5,5.1)*Rot(0,0,90)*extrude(SlotOverall(8.4,4.4),4,both=True)
features=part('liner_left').features
for shift in [(0,0,0),(.4,0,0),(-.4,0,0),(0,.4,0),(0,-.4,0),(0,0,.4),(0,0,-.4)]:
 body=body-Pos(*shift)*features
 upper_raw=upper_raw-Pos(*shift)*features
 fore_fixed=fore_fixed-Pos(*shift)*features
 rear_fixed=rear_fixed-Pos(*shift)*features
# Driver corridors are wholly internal and open only after the top module is removed.
body=body-Pos(h.heat_x,14.5,30)*Cylinder(2.1,45.8)
body=body-Pos(-23,10.5,26.5)*Cylinder(1.8,47)
assert len(body.solids())==1
assert len(upper_raw.solids())==1
assert len(fore_fixed.solids())==1
assert len(rear_fixed.solids())==1
left=body
right=mirror(body,about=Plane.XZ)
screw=SocketHeadCapScrew(size='M2-0.4',length=8,fastener_type='iso4762',simple=True)
hardware=[Pos(h.heat_x,side*14.5,7.1)*screw for side in [-1,1]]
publish('thermal_bridge_left',left,'左铝导热桥',material='aluminum')
publish('thermal_clamp_screws',hardware,'导热桥M2×8夹紧螺钉',role='fastener',material='stainless_steel')

contact_screw=SocketHeadCapScrew(size='M1.6-0.35',length=10,fastener_type='iso4762',simple=True)
contact_hardware=[Pos(x,side*y,22.3)*contact_screw for side in [-1,1] for x,y in [fore_bolt,aft_bolt]]
publish('thermal_contact_screws',contact_hardware,'导热接触座M1.6螺钉',role='fastener',material='stainless_steel')