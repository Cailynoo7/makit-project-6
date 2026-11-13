p=part('thermal_interfaces_left')
t=param('installed_gap',0.1)
for name,shape in [('root',p.root),('fore',p.fore),('aft',p.aft),('cap',p.cap),('couple_fore',p.couple_fore),('couple_aft',p.couple_aft),('couple_cap',p.couple_cap)]:
 publish('thermal_'+name+'_pad_right',mirror(shape,about=Plane.XZ),'右导热界面层',role='reference',material='silicone')