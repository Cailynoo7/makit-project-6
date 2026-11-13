s=part('skid_left')
f=part('fuselage')
width=param('enlarged_right_skid_width',3.75)
result=s.make_skid(width)
if isinstance(result,tuple): body,caps,hardware=result
else: body=result;caps=[];hardware=[]
body=mirror(body,about=Plane.XZ)
caps=[mirror(c,about=Plane.XZ) for c in caps]
hardware=[mirror(h,about=Plane.XZ) for h in hardware]
body.color=srgb('#FFFFFF')
publish('skid_right',body,'右弧形滑橇',material='petg')
if hardware: publish('skid_root_screws_right',[Pos(0,-f.skid_rail_y,f.skid_rail_z)*h for h in hardware],'右起落架内部螺钉',role='fastener',material='stainless_steel')
