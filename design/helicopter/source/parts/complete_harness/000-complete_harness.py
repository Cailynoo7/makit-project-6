# cell: complete_harness
from math import acos,tan,sin,sqrt,ceil
def rounded_path(points,radius=6):
 p=[Vector(*q) for q in points];edges=[];at=p[0];min_radius=1000.
 for i in range(1,len(p)-1):
  u=(p[i-1]-p[i]).normalized();v=(p[i+1]-p[i]).normalized()
  angle=acos(max(-1.,min(1.,u.dot(v))))
  if abs(angle-3.14159265358979)<1e-4:continue
  d=min(radius/tan(angle/2),.44*(p[i]-p[i-1]).length,.44*(p[i+1]-p[i]).length)
  rr=d*tan(angle/2);min_radius=min(min_radius,rr)
  a=p[i]+u*d;b=p[i]+v*d;c=p[i]+(u+v).normalized()*(rr/sin(angle/2))
  mid=c+(p[i]-c).normalized()*rr
  if (a-at).length>1e-6:edges.append(Edge.make_line(at,a))
  edges.append(Edge.make_three_point_arc(a,mid,b));at=b
 if (p[-1]-at).length>1e-6:edges.append(Edge.make_line(at,p[-1]))
 return Wire(edges),min_radius
def tube_route(row):
 p=row['points']
 if row['id'] in ['H10','H11']:
  side=1 if row['id']=='H10' else -1
  p0,p1,p2=map(lambda q:Vector(*q),p[:3])
  pm=Vector(p1.X,p1.Y+side*(6-6/sqrt(2)),p1.Z+6/sqrt(2))
  edges=[Edge.make_line(p0,p1),Edge.make_three_point_arc(p1,pm,p2)]
  tail,rmin=rounded_path(p[2:])
  path=Wire([*edges,*tail.edges()]);rmin=min(6,rmin)
 else:path,rmin=rounded_path(row['points'])
 if 'arc' in row:
  path=Wire([*path.edges(),Edge.make_three_point_arc(row['points'][-1],*row['arc']),Edge.make_line(row['arc'][-1],row['end'])])
 p0=Vector(*row['points'][0]);d=Vector(*row['points'][1])-p0
 return sweep(Plane(origin=p0,z_dir=d)*Circle(row['r']),path=path),path.length,rmin

bundle_scale=param('bundle_radius_scale',1.0)
plug_h=param('standard_plug_height',14.0)
key_h=param('key_socket_total_depth',11.5)
pin_base=param('header_mating_base_z',0.135)
layout=part('internal_carrier')
raw_drop_x=layout.raw_wire_x
raw_positive_y=layout.raw_positive_y
raw_negative_y=layout.raw_negative_y
rows=[{"id":"H01","name":"XIAO主控制束","r":3,"points":[[-16,6.42,14.135],[-16,6.42,24],[-16,-16,24],[20,-16,24],[25,-16,10],[37.5,-16,0],[37.5,-16,-20],[20,-16,-20],[20,-6,-20],[32,-6,-20]],"arc":[[38,0,-20],[32,6,-20]],"end":[26,6,-20]},{"id":"H02P","name":"电芯正极","r":0.7,"points":[[-9.27,18.72,14.135],[-9.27,18.72,28],[raw_drop_x,raw_positive_y,28],[raw_drop_x,raw_positive_y,-14],[15.5,raw_positive_y,-18],[15.5,35,-24],[0,35,-24]]},{"id":"H02N","name":"电芯负极","r":0.7,"points":[[-6.73,18.72,14.135],[-6.73,21,25.5],[raw_drop_x,raw_negative_y,25.5],[raw_drop_x,raw_negative_y,-18],[15.5,20,-23.8],[15.5,-35,-23.8],[0,-35,-24]]},{"id":"H03","name":"电机双线","r":1.4,"points":[[6,18.72,14.135],[6,18.72,30],[25,20,30],[33,14,20],[33,13,-1],[23,0,-1]]},{"id":"H04","name":"COB双线","r":1.2,"points":[[6,-18.72,14.135],[6,-18.72,24],[-17,-8,24],[-28,-8,24],[-28,-8,8],[-40,-8,5],[-40,0,-2.6]]},{"id":"H05","name":"左窗按键","r":1.2,"points":[[-8,-18.72,14.135],[-8,-18.72,22],[-8,0,24],[-8,20,20],[0,22,8]]},{"id":"H06","name":"右窗按键","r":1.2,"points":[[-1,-18.72,14.135],[-1,-18.72,20],[6,-18,20],[6,-18,8],[0,-22,8]]},{"id":"H07","name":"风扇使能","r":1.2,"points":[[-10,-12.792,14.135],[-10,-12.792,22],[-10,-16,22]]},{"id":"H08","name":"ADC三线","r":1.7,"points":[[9,-12.324,14.135],[9,-12.324,22],[9,-16,22]]},{"id":"H09","name":"COB温度","r":1.7,"points":[[17,15.6872,14.135],[19,13,22],[9,11,28],[-28,11,28],[-28,8,8],[-40,8,5],[-39,6,-2.1]]},{"id":"H10","name":"壳体温度","r":1.7,"points":[[13.35,5.3912,14.135],[13.35,5.3912,18.135],[13.35,11.3912,24.135],[23,13,27],[34,15,19],[35,20,12],[36.035,24.725,9.94]]},{"id":"H11","name":"电芯温度","r":1.7,"points":[[13.35,-4.9048,14.135],[13.35,-4.9048,18.135],[13.35,-10.9048,24.135],[13.35,-19.5,24.135],[13.35,-19.5,10],[13.35,-27.5,2],[13.35,-27.5,-16],[11.4,-23.5,-24]]},{"id":"H12","name":"PACK至XIAO","r":1.4,"points":[[-1,18.72,14.135],[-1,18.72,24],[10,21,28],[20,21,28],[24,14.5,10],[24,14.5,-20],[13,16,-20],[13,16,-27.0],[26.5,16,-27.0],[26.5,10,-30.3],[26.137,4.445,-30.3]]}]
fans=[["D1",30.8361,7.62,0.55],["D2",28.2961,7.62,0.55],["D3",25.7561,7.62,0.55],["D4",23.2161,7.62,0.55],["D10",25.7561,-7.62,0.55],["VBUS",33.3761,-7.62,0.55],["GND",30.8361,-7.62,0.7],["D5",20.6761,7.62,0.55],["EN_GND",30.8361,-7.62,0.55],["3V3",28.2961,-7.62,0.55],["SDA_D7",18.1361,-7.62,0.55],["SCL_D6",18.1361,7.62,0.55]]
geometry=[];lengths={}
for row in rows:
 row=dict(row);row['r']*=bundle_scale
 tube,length,rmin=tube_route(row)
 assert tube.is_valid,row['id']
 geometry.append(tube);lengths[row['id']]=round(length,3)
# Twelve loose conductors fan out from the shared service bow to actual XIAO edge pads.
for name,x,y,r in fans:
 points=[(26,6,-20),(x,y,-23),(x,y,-26.7)]
 path,rmin=rounded_path(points,4)
 geometry.append(sweep(Plane(origin=points[0],z_dir=Vector(*points[1])-Vector(*points[0]))*Circle(r),path=path))
 geometry.append(Pos(x,y,-27.16)*Cylinder(.22,.92))
 lengths['fanout_'+name]=round(path.length+.92,3)
# Main seven-pin fan-in; each pin exits separately before gathering above the board.
for i in range(7):
 y=14.04-2.54*i;p=[(-16,y,14.135),(-16,y,18.135),(-16,6.42,24)]
 path,rr=rounded_path(p,3)
 geometry.append(sweep(Plane(origin=p[0],z_dir=(0,0,1))*Circle(.55 if i<6 else .7),path=path))
 lengths['J1_fanin_'+str(i+1)]=round(path.length,3)
# Final low-voltage and COB branches stop at the solder allowance; no insulation over LES.
tips=[
 ('COB+',.55,[(-40,0,-2.6),(-40,7.8,-2.6),(-33.5,7.8,-2.6),(-33.5,5.5,-2.6)]),
 ('COB-',.55,[(-40,0,-2.6),(-40,-6.6,-2.6),(-22.5,-6.6,-2.6),(-22.5,-5.5,-2.6)]),
 ('MOTOR_A',.7,[(23,0,-1),(19.85,0,1.9)]),
 ('MOTOR_B',.7,[(23,0,-1),(26.15,0,1.9)]),
 ('BAT+',.7,[(26.137,4.445,-30.3),(26.137,4.445,-29.8)]),
 ('BAT-',.7,[(26.137,4.445,-30.3),(28.042,4.445,-30.3),(28.042,4.445,-29.8)]),
 ('COB_NTC1',.7,[(-39,6,-2.1),(-37.0,4.6,-1.4)]),
 ('COB_NTC2',.7,[(-39,6,-2.1),(-35.6,4.6,-1.4)])
]
for name,r,p in tips:
 path,rr=rounded_path(p,2)
 geometry.append(sweep(Plane(origin=p[0],z_dir=Vector(*p[1])-Vector(*p[0]))*Circle(r),path=path));lengths[name]=round(path.length,3)
for x in [26.137,28.042]:
 geometry.append(Pos(x,4.445,-29.25)*Cylinder(.25,.7))
# Dimensioned standard/procurement envelopes. Female cavities use their matching male reference.
board=asset('design/helicopter/source/assets/4e0aa490b5d737619f6fee8720de3aa324388a98d51fd871130856d8007742a3.step')
board=Pos(-100,100,-4)*board
header_solids=list(board.solids())
plugs=[
 ('J1',-16,6.42,3,18.3),('J2',-8,18.72,5.6,3),('J3',6,18.72,5.6,3),
 ('J4',6,-18.72,5.6,3),('J5',-8,-18.72,5.6,3),('J6',-1,-18.72,5.6,3),
 ('J7',-10,-12.792,5.6,3),('J8',9,-12.324,8.1,3),('J9',17,15.6872,9,6.5),
 ('J10',13.35,5.3912,6.5,9),('J11',13.35,-4.9048,6.5,9),('J12',-1,18.72,5.6,3)]
for name,x,y,sx,sy in plugs:
 box=Pos(x,y,pin_base+plug_h/2)*Box(sx,sy,plug_h)
 matches=[s for s in header_solids if s.bounding_box().size.Z>10 and abs(s.bounding_box().center().X-x)<.05 and abs(s.bounding_box().center().Y-y)<.05]
 assert len(matches)==1,(name,len(matches))
 geometry.append(box.cut(matches[0]))
# Low-profile side-window sockets, soldered by the user; not14mm crimp housings.
for side,target in [(1,'key_board_left'),(-1,'key_board_right')]:
 key=Pos(0,-10,0)*part('key_board_pair').body if side<0 else Pos(100,36.155,102)*Rot(-90,0,180)*asset('design/helicopter/source/assets/61bb522824f253e41ba5f03eeadca6c897be14ab9506143808c88acf5f8c076b.step')
 box=Pos(0,side*(33.53-key_h/2),8)*Box(3,key_h,5.6)
 male=[s for s in key.solids() if s.bounding_box().size.Y>6 and s.bounding_box().size.X<6]
 assert len(male)==1
 geometry.append(box.cut(male[0]))
body=Compound(children=geometry)
body.color=srgb('#C3C5C7')
print('wire centreline lengths mm',lengths)
publish('complete_harness',body,'整套线束与插壳包络',role='reference')