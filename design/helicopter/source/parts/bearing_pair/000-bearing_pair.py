gap=param('bearing_axial_gap',0.1)
body=asset('design/helicopter/source/assets/6cf33efeb8fe32725a1a155d6954e6ae308a159887b4417ea369cf881fb90549.step')
publish('bearing_upper',Pos(0,0,53.9+gap)*body,'上轴承6800',material='steel',role='fastener')
