# cell: key_board_pair
# cell: key_board_pair
pcb_y=param('right_pcb_back_y',-26.155)
pcb_centre_z=param('right_pcb_centre_z',2.0)
# Second instance of the identical, released STEP asset; no replacement geometry.
body=Pos(-100,pcb_y,pcb_centre_z+100)*Rot(90,0,0)*asset('design/helicopter/source/assets/61bb522824f253e41ba5f03eeadca6c897be14ab9506143808c88acf5f8c076b.step')
publish('key_board_right',body,'右窗按键小板',role='reference')
