from math import acos,cos,sin,degrees,pi
R=param('enlarged_belt_driven_pitch_radius',15.0)
r=param('belt_driver_pitch_radius',4.0)
c=param('enlarged_belt_axis_distance',23.0)
section=param('belt_section_diameter',1.5)
free_id=param('belt_free_inside_diameter',32.0)
z=param('internal_belt_z',35.3)
t=acos((R-r)/c)
a=degrees(t)
p=(R*cos(t),R*sin(t));q=(c+r*cos(t),r*sin(t))
wire=Wire([CenterArc((0,0),R,a,360-2*a).edge(),Line((p[0],-p[1]),(q[0],-q[1])).edge(),CenterArc((c,0),r,-a,2*a).edge(),Line(q,p).edge()])
path=Pos(0,0,z)*wire
profile=Plane(origin=(p[0],p[1],z),z_dir=(-sin(t),cos(t),0))*Circle(section/2)
body=sweep(profile,path)
print('Belt neutral length',path.length,'32ID stretch%',100*(path.length/(pi*(free_id+section))-1))
body.color=srgb('#303030')
# Deliberately modeled deformed purchasing envelope; no catalog STEP exists for this size.
publish('drive_belt',body,'32×1.5 O形圈工作状态示意',material='rubber',role='reference')
