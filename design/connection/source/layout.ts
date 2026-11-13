// Exterior and carrier interfaces remain fixed. Top=service cavity; bottom=low-profile passives/protection.
export const board={width:40,height:50,thickness:1.6};
export const mounting=[{x:-16,y:-11},{x:16,y:-11}];
export const headers=[
 {name:'J1',x:-16,y:14.04,rotation:0,nets:['KEY_L','KEY_R','FAN_CTL','LIGHT_CTL','USB_SENSE','VBUS','GND'],bom:'headers_7',section:'Control'},
 {name:'J2',x:-9.27,y:18.72,rotation:90,nets:['CELL_P','CELL_N'],bom:'headers_2',section:'Protection'},
 {name:'J12',x:-2.27,y:18.72,rotation:90,nets:['VBAT','GND'],bom:'protected_battery_header',section:'Protection'},
 {name:'J3',x:4.73,y:18.72,rotation:90,nets:['MOTOR_A','MOTOR_B'],bom:'headers_2',section:'Fan'},
 {name:'J4',x:4.73,y:-18.72,rotation:90,nets:['LED_PLUS','LED_FB'],bom:'headers_2',section:'Light'},
 {name:'J5',x:-9.27,y:-18.72,rotation:90,nets:['KEY_L','GND'],bom:'headers_2',section:'Control'},
 {name:'J6',x:-2.27,y:-18.72,rotation:90,nets:['KEY_R','GND'],bom:'headers_2',section:'Control'},
 {name:'J7',x:-11.27,y:-12.792,rotation:90,nets:['FAN_EN','GND'],bom:'headers_2',section:'Fan'},
 {name:'J8',x:6.46,y:-12.324,rotation:90,nets:['V3V3','I2C_SDA','I2C_SCL'],bom:'thermal_header',section:'Temperature'},
 {name:'J9',x:17,y:16.9572,rotation:0,nets:['NTC_LED','GND'],bom:'probe_headers',section:'Temperature'},
 {name:'J10',x:12.08,y:5.3912,rotation:90,nets:['NTC_SHELL','GND'],bom:'probe_headers',section:'Temperature'},
 {name:'J11',x:12.08,y:-4.9048,rotation:90,nets:['NTC_BAT','GND'],bom:'probe_headers',section:'Temperature'},
] as const;
