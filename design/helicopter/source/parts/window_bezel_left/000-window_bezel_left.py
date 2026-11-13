f=part('fuselage')
def ell(ry):
 return Sphere(1).transform_geometry(Matrix([[f.body_length/2,0,0,0],[0,ry,0,0],[0,0,f.body_height/2,0],[0,0,0,1]]))
outer=ell(f.body_width/2)
w=part('window_left')
radius=param('enlarged_bezel_outer_radius',21.875)
height=param('bezel_left_height',1.2)
edge=param('bezel_left_edge_radius',0.3)
overlap=param('bezel_left_window_overlap',0.5)
glue_gap=param('bezel_left_glue_gap',0.15)
inner_radius=w.radius-overlap
region=Pos(f.window_x,f.body_width/2,f.window_z)*Rot(90,0,0)*Cylinder(radius,f.body_width)
raw=(ell(f.body_width/2+height)-outer)&region
raw=raw-Pos(f.window_x,f.body_width/2,f.window_z)*Rot(90,0,0)*Cylinder(inner_radius,f.body_width)
ring=fillet(raw.edges(),edge)
body=Pos(0,glue_gap,0)*ring
body.color=srgb('#FFFFFF')
assert inner_radius>part('button_left').radius+2
publish('window_bezel_left',body,'左白色覆盖窗框',material='petg')
