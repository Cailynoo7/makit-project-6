export const ics = [
  {
    "name": "U1",
    "code": "C1554283",
    "x": -7,
    "y": -2.34,
    "side": "top",
    "section": "Light",
    "bom": "led_regulator",
    "pins": [
      [
        "SW1",
        "BOOST_SW"
      ],
      [
        "SW2",
        "BOOST_SW"
      ],
      [
        "VIN",
        "VBOOST_BIAS"
      ],
      [
        "EN",
        "LIGHT_EN"
      ],
      [
        "SS",
        "LED_SS"
      ],
      [
        "DIMC",
        "LED_DIM"
      ],
      [
        "AGND",
        "GND"
      ],
      [
        "COMP",
        "LED_COMP"
      ],
      [
        "FB",
        "LED_FB"
      ],
      [
        "FREQ",
        "LED_FREQ"
      ],
      [
        "OVP",
        "LED_OVP"
      ],
      [
        "PGND1",
        "GND"
      ],
      [
        "PGND2",
        "GND"
      ],
      [
        "PGND3",
        "GND"
      ],
      [
        "EP",
        "GND"
      ]
    ],
    "rotation": 180
  },
  {
    "name": "D1",
    "code": "C968580",
    "x": 0.6,
    "y": 12.96,
    "rotation": 180,
    "side": "top",
    "section": "Light",
    "bom": "led_schottky",
    "pins": [
      [
        "A1",
        "BOOST_SW"
      ],
      [
        "A2",
        "BOOST_SW"
      ],
      [
        "K",
        "LED_PLUS"
      ]
    ]
  },
  {
    "name": "U2",
    "code": "C31829946",
    "x": 8,
    "y": 3.9,
    "side": "top",
    "section": "Fan",
    "bom": "fan_driver",
    "pins": [
      [
        "IPROPI",
        "FAN_IPROPI"
      ],
      [
        "VCC",
        "FAN_VCC"
      ],
      [
        "nSTALL",
        "FAN_FAULT"
      ],
      [
        "nFAULT",
        "FAN_FAULT"
      ],
      [
        "VM",
        "VBAT"
      ],
      [
        "OUT1",
        "MOTOR_A"
      ],
      [
        "PGND",
        "GND"
      ],
      [
        "OUT2",
        "MOTOR_B"
      ],
      [
        "GND",
        "GND"
      ],
      [
        "TINRUSH",
        "FAN_TIMER"
      ],
      [
        "SMODE",
        "GND"
      ],
      [
        "IN2",
        "FAN_EN"
      ],
      [
        "IN1",
        "FAN_CTL"
      ],
      [
        "GAINSEL",
        "GND"
      ],
      [
        "IMODE",
        "FAN_VCC"
      ],
      [
        "VREF",
        "FAN_VREF"
      ],
      [
        "EP",
        "GND"
      ]
    ]
  },
  {
    "name": "U3",
    "code": "C37593",
    "x": 7,
    "y": -1.56,
    "side": "bottom",
    "section": "Temperature",
    "bom": "thermal_adc",
    "pins": [
      [
        "ADDR",
        "GND"
      ],
      [
        "ALERT",
        ""
      ],
      [
        "GND",
        "GND"
      ],
      [
        "AIN0",
        "TEMP_LED"
      ],
      [
        "AIN1",
        "TEMP_SHELL"
      ],
      [
        "AIN2",
        "TEMP_BAT"
      ],
      [
        "AIN3",
        "BAT_ADC"
      ],
      [
        "VDD",
        "V3V3"
      ],
      [
        "SDA",
        "I2C_SDA"
      ],
      [
        "SCL",
        "I2C_SCL"
      ]
    ],
    "rotation": 90
  },
  {
    "name": "U4",
    "code": "C183096",
    "x": -12,
    "y": -15.72,
    "side": "bottom",
    "section": "Protection",
    "bom": "battery_protection_ic",
    "pins": [
      [
        "NC",
        ""
      ],
      [
        "COUT",
        "CHG_GATE"
      ],
      [
        "DOUT",
        "DSG_GATE"
      ],
      [
        "VSS",
        "BQ_VSS"
      ],
      [
        "BAT",
        "PROT_BAT"
      ],
      [
        "VMINUS",
        "PROT_VMINUS"
      ]
    ],
    "rotation": 180
  },
  {
    "name": "F1",
    "code": "C27515",
    "x": -8,
    "y": 12.84,
    "side": "bottom",
    "section": "Protection",
    "bom": "battery_fuse",
    "pins": [
      [
        "IN",
        "CELL_P"
      ],
      [
        "OUT",
        "VBAT"
      ]
    ]
  },
  {
    "name": "Q3",
    "code": "C544396",
    "x": -10,
    "y": 7.02,
    "side": "bottom",
    "section": "Protection",
    "bom": "battery_protection_fets",
    "pins": [
      [
        "S1",
        "GND"
      ],
      [
        "G1",
        "CHG_GATE"
      ],
      [
        "D2",
        "FET_MID"
      ],
      [
        "S2",
        "CELL_N"
      ],
      [
        "G2",
        "DSG_GATE"
      ],
      [
        "D1",
        "FET_MID"
      ],
      [
        "D1EP",
        "FET_MID"
      ],
      [
        "D2EP",
        "FET_MID"
      ]
    ]
  },
  {
    "name": "Q4",
    "code": "C544396",
    "x": -6.5,
    "y": 7.02,
    "side": "bottom",
    "section": "Protection",
    "bom": "battery_protection_fets",
    "pins": [
      [
        "S1",
        "GND"
      ],
      [
        "G1",
        "CHG_GATE"
      ],
      [
        "D2",
        "FET_MID"
      ],
      [
        "S2",
        "CELL_N"
      ],
      [
        "G2",
        "DSG_GATE"
      ],
      [
        "D1",
        "FET_MID"
      ],
      [
        "D1EP",
        "FET_MID"
      ],
      [
        "D2EP",
        "FET_MID"
      ]
    ]
  },
  {
    "name": "Q5",
    "code": "C544396",
    "x": -3,
    "y": 7.02,
    "side": "bottom",
    "section": "Protection",
    "bom": "battery_protection_fets",
    "pins": [
      [
        "S1",
        "GND"
      ],
      [
        "G1",
        "CHG_GATE"
      ],
      [
        "D2",
        "FET_MID"
      ],
      [
        "S2",
        "CELL_N"
      ],
      [
        "G2",
        "DSG_GATE"
      ],
      [
        "D1",
        "FET_MID"
      ],
      [
        "D1EP",
        "FET_MID"
      ],
      [
        "D2EP",
        "FET_MID"
      ]
    ]
  },
  {
    "name": "Q6",
    "code": "C544396",
    "x": 0.5,
    "y": 7.02,
    "side": "bottom",
    "section": "Protection",
    "bom": "battery_protection_fets",
    "pins": [
      [
        "S1",
        "GND"
      ],
      [
        "G1",
        "CHG_GATE"
      ],
      [
        "D2",
        "FET_MID"
      ],
      [
        "S2",
        "CELL_N"
      ],
      [
        "G2",
        "DSG_GATE"
      ],
      [
        "D1",
        "FET_MID"
      ],
      [
        "D1EP",
        "FET_MID"
      ],
      [
        "D2EP",
        "FET_MID"
      ]
    ]
  },
  {
    "name": "Q7",
    "code": "C544396",
    "x": 4,
    "y": 7.02,
    "side": "bottom",
    "section": "Protection",
    "bom": "battery_protection_fets",
    "pins": [
      [
        "S1",
        "GND"
      ],
      [
        "G1",
        "CHG_GATE"
      ],
      [
        "D2",
        "FET_MID"
      ],
      [
        "S2",
        "CELL_N"
      ],
      [
        "G2",
        "DSG_GATE"
      ],
      [
        "D1",
        "FET_MID"
      ],
      [
        "D1EP",
        "FET_MID"
      ],
      [
        "D2EP",
        "FET_MID"
      ]
    ]
  }
];
export const passives = [
  {
    "type": "R",
    "name": "R1",
    "value": "100",
    "x": 14.8,
    "y": 10,
    "a": "VBAT",
    "b": "FAN_VCC",
    "bom": "gate_resistors",
    "section": "Fan",
    "side": "top",
    "code": "C22775",
    "rotation": 90
  },
  {
    "type": "R",
    "name": "R2",
    "value": "100k",
    "x": 16,
    "y": -1,
    "a": "FAN_EN",
    "b": "GND",
    "bom": "bias_resistors",
    "section": "Fan",
    "side": "top",
    "code": "C14675",
    "rotation": 90
  },
  {
    "type": "R",
    "name": "R3",
    "value": "100",
    "x": -11.3,
    "y": 1.5,
    "a": "LIGHT_CTL",
    "b": "LIGHT_EN",
    "bom": "gate_resistors",
    "section": "Light",
    "side": "top",
    "code": "C22775",
    "rotation": 90
  },
  {
    "type": "R",
    "name": "R4",
    "value": "100k",
    "x": -4.5,
    "y": -4,
    "a": "LIGHT_EN",
    "b": "GND",
    "bom": "bias_resistors",
    "section": "Light",
    "side": "bottom",
    "code": "C14675",
    "rotation": 90
  },
  {
    "type": "R",
    "name": "R5",
    "value": "100k",
    "x": -13,
    "y": 10.452,
    "a": "VBUS",
    "b": "USB_SENSE",
    "bom": "bias_resistors",
    "section": "Control",
    "side": "bottom",
    "code": "C14675",
    "rotation": 90
  },
  {
    "type": "R",
    "name": "R6",
    "value": "150k",
    "x": -13,
    "y": 5.148,
    "a": "USB_SENSE",
    "b": "GND",
    "bom": "usb_sense_bottom",
    "section": "Control",
    "side": "bottom",
    "code": "C22807",
    "rotation": 90
  },
  {
    "type": "R",
    "name": "R7",
    "value": "150k",
    "x": 3,
    "y": 17.472,
    "a": "VBAT",
    "b": "FAN_VREF",
    "bom": "usb_sense_bottom",
    "section": "Fan",
    "side": "bottom",
    "code": "C22807",
    "rotation": 90
  },
  {
    "type": "R",
    "name": "R8",
    "value": "22k",
    "x": 3,
    "y": 12.168,
    "a": "FAN_VREF",
    "b": "GND",
    "bom": "fan_vref_bottom",
    "section": "Fan",
    "side": "bottom",
    "code": "C31850",
    "rotation": 90
  },
  {
    "type": "R",
    "name": "R9",
    "value": "4.99k",
    "x": 5.4,
    "y": -5.3,
    "a": "FAN_IPROPI",
    "b": "GND",
    "bom": "fan_current_scale",
    "section": "Fan",
    "side": "top",
    "code": "C23046",
    "rotation": 0
  },
  {
    "type": "R",
    "name": "R10",
    "value": "100k",
    "x": 13,
    "y": -9.2,
    "a": "FAN_VCC",
    "b": "FAN_FAULT",
    "bom": "bias_resistors",
    "section": "Fan",
    "side": "top",
    "code": "C14675",
    "rotation": 0
  },
  {
    "type": "C",
    "name": "C1",
    "value": "10uF",
    "x": -2,
    "y": 14.04,
    "a": "VBAT",
    "b": "GND",
    "bom": "bulk",
    "section": "Fan",
    "side": "bottom",
    "code": "C15850",
    "rotation": 0
  },
  {
    "type": "C",
    "name": "C2",
    "value": "100nF",
    "x": 12.2,
    "y": 1.56,
    "a": "VBAT",
    "b": "GND",
    "bom": "decoupling",
    "section": "Fan",
    "side": "top",
    "code": "C14663",
    "rotation": 0
  },
  {
    "type": "C",
    "name": "C3",
    "value": "100nF",
    "x": -7.05,
    "y": -0.8,
    "a": "VBOOST_BIAS",
    "b": "GND",
    "bom": "decoupling",
    "section": "Light",
    "side": "bottom",
    "code": "C14663",
    "rotation": 0
  },
  {
    "type": "C",
    "name": "C4",
    "value": "100nF",
    "x": -13,
    "y": -3.9,
    "a": "USB_SENSE",
    "b": "GND",
    "bom": "decoupling",
    "section": "Control",
    "side": "bottom",
    "code": "C14663",
    "rotation": 90
  },
  {
    "type": "C",
    "name": "C5",
    "value": "100nF",
    "x": 8.2,
    "y": -1.716,
    "a": "FAN_VCC",
    "b": "GND",
    "bom": "decoupling",
    "section": "Fan",
    "side": "top",
    "code": "C14663",
    "rotation": 0
  },
  {
    "type": "C",
    "name": "C6",
    "value": "470nF",
    "x": 8.7,
    "y": -5.46,
    "a": "FAN_TIMER",
    "b": "GND",
    "bom": "fan_start_timer",
    "section": "Fan",
    "side": "top",
    "code": "C1623",
    "rotation": 0
  },
  {
    "type": "C",
    "name": "C7",
    "value": "100nF",
    "x": 4.6,
    "y": 0.78,
    "a": "FAN_VREF",
    "b": "GND",
    "bom": "decoupling",
    "section": "Fan",
    "side": "top",
    "code": "C14663",
    "rotation": 90
  },
  {
    "type": "C",
    "name": "C8",
    "value": "47uF",
    "x": 10.5,
    "y": 12.48,
    "a": "VBAT",
    "b": "GND",
    "bom": "fan_bulk",
    "section": "Fan",
    "side": "top",
    "code": "C96123",
    "rotation": 0
  },
  {
    "type": "R",
    "name": "R11",
    "value": "0.75",
    "x": -3,
    "y": -8.736,
    "a": "LED_FB",
    "b": "GND",
    "bom": "led_sense_resistor",
    "section": "Light",
    "side": "top",
    "size": "1206_3216Metric",
    "rotation": 270
  },
  {
    "type": "R",
    "name": "R12",
    "value": "176k",
    "x": -3,
    "y": -0.936,
    "a": "LED_FREQ",
    "b": "GND",
    "bom": "led_freq_resistor",
    "section": "Light",
    "side": "bottom",
    "rotation": 0
  },
  {
    "type": "R",
    "name": "R13",
    "value": "158k",
    "x": -5.8,
    "y": -10.15,
    "a": "LED_PLUS",
    "b": "LED_OVP",
    "bom": "led_ovp_top",
    "section": "Light",
    "side": "top",
    "rotation": 0
  },
  {
    "type": "R",
    "name": "R14",
    "value": "10k",
    "x": -7,
    "y": -8.2,
    "a": "LED_OVP",
    "b": "GND",
    "bom": "led_ovp_bottom",
    "section": "Light",
    "side": "top",
    "rotation": 0
  },
  {
    "type": "R",
    "name": "R15",
    "value": "1M",
    "x": -4,
    "y": -15.6,
    "a": "LED_PLUS",
    "b": "GND",
    "bom": "led_bleeder",
    "section": "Light",
    "side": "bottom",
    "rotation": 0
  },
  {
    "type": "C",
    "name": "C9",
    "value": "47nF",
    "x": -5.1,
    "y": -13.26,
    "a": "LED_SS",
    "b": "GND",
    "bom": "led_soft_start",
    "section": "Light",
    "side": "bottom",
    "rotation": 0
  },
  {
    "type": "C",
    "name": "C10",
    "value": "470nF",
    "x": -8.5,
    "y": -9.984,
    "a": "LED_COMP",
    "b": "GND",
    "bom": "led_compensation",
    "section": "Light",
    "side": "bottom",
    "rotation": 0
  },
  {
    "type": "C",
    "name": "C11",
    "value": "1uF",
    "x": -5,
    "y": -8.892,
    "a": "LED_DIM",
    "b": "GND",
    "bom": "led_dim_filter",
    "section": "Light",
    "side": "bottom",
    "size": "0805_2012Metric",
    "rotation": 0
  },
  {
    "type": "C",
    "name": "C12",
    "value": "4.7uF",
    "x": -12.5,
    "y": 18.72,
    "a": "VBAT",
    "b": "GND",
    "bom": "led_input_cap",
    "section": "Light",
    "side": "top",
    "size": "0805_2012Metric",
    "rotation": 90
  },
  {
    "type": "C",
    "name": "C13",
    "value": "2.2uF",
    "x": 0.5,
    "y": 1.56,
    "a": "LED_PLUS",
    "b": "GND",
    "bom": "led_output_caps",
    "section": "Light",
    "side": "top",
    "size": "1210_3225Metric",
    "rotation": 0
  },
  {
    "type": "C",
    "name": "C14",
    "value": "2.2uF",
    "x": 0.5,
    "y": -4.68,
    "a": "LED_PLUS",
    "b": "GND",
    "bom": "led_output_caps",
    "section": "Light",
    "side": "top",
    "size": "1210_3225Metric",
    "rotation": 0
  },
  {
    "type": "R",
    "name": "R16",
    "value": "330",
    "x": -12,
    "y": -10.6,
    "a": "CELL_P",
    "b": "PROT_BAT",
    "bom": "protection_bat_filter",
    "section": "Protection",
    "side": "bottom"
  },
  {
    "type": "R",
    "name": "R17",
    "value": "2.2k",
    "x": -13,
    "y": -20.76,
    "a": "GND",
    "b": "PROT_VMINUS",
    "bom": "protection_vminus",
    "section": "Protection",
    "side": "bottom",
    "rotation": 90
  },
  {
    "type": "R",
    "name": "R18",
    "value": "5.1M",
    "x": -2.5,
    "y": 2.496,
    "a": "CHG_GATE",
    "b": "GND",
    "bom": "protection_gate_bleeds",
    "section": "Protection",
    "side": "bottom",
    "rotation": 0
  },
  {
    "type": "R",
    "name": "R19",
    "value": "5.1M",
    "x": -16.5,
    "y": -14,
    "a": "DSG_GATE",
    "b": "BQ_VSS",
    "bom": "protection_gate_bleeds",
    "section": "Protection",
    "side": "bottom"
  },
  {
    "type": "C",
    "name": "C15",
    "value": "100nF",
    "x": -15.3,
    "y": -17.76,
    "a": "PROT_BAT",
    "b": "BQ_VSS",
    "bom": "added_bypass",
    "section": "Protection",
    "side": "bottom"
  },
  {
    "type": "C",
    "name": "C16",
    "value": "100nF",
    "x": 2,
    "y": -1.248,
    "a": "V3V3",
    "b": "GND",
    "bom": "added_bypass",
    "section": "Temperature",
    "side": "bottom",
    "rotation": 0
  },
  {
    "type": "R",
    "name": "R20",
    "value": "10k",
    "x": 13,
    "y": 14.04,
    "a": "V3V3",
    "b": "NTC_LED",
    "bom": "temperature_pullups",
    "section": "Temperature",
    "side": "bottom",
    "rotation": 90
  },
  {
    "type": "R",
    "name": "R21",
    "value": "1k",
    "x": 7.5,
    "y": 10.5,
    "a": "NTC_LED",
    "b": "TEMP_LED",
    "bom": "temperature_input_filter",
    "section": "Temperature",
    "side": "bottom",
    "rotation": 0
  },
  {
    "type": "C",
    "name": "C17",
    "value": "100nF",
    "x": 11.7,
    "y": -0.468,
    "a": "TEMP_LED",
    "b": "GND",
    "bom": "temperature_filter_caps",
    "section": "Temperature",
    "side": "bottom",
    "rotation": 0
  },
  {
    "type": "R",
    "name": "R22",
    "value": "10k",
    "x": 10,
    "y": 9.2,
    "a": "V3V3",
    "b": "NTC_SHELL",
    "bom": "temperature_pullups",
    "section": "Temperature",
    "side": "bottom",
    "rotation": 90
  },
  {
    "type": "R",
    "name": "R23",
    "value": "1k",
    "x": 11,
    "y": -8.4,
    "a": "NTC_SHELL",
    "b": "TEMP_SHELL",
    "bom": "temperature_input_filter",
    "section": "Temperature",
    "side": "bottom",
    "rotation": 0
  },
  {
    "type": "C",
    "name": "C18",
    "value": "100nF",
    "x": 9,
    "y": -4.8,
    "a": "TEMP_SHELL",
    "b": "GND",
    "bom": "temperature_filter_caps",
    "section": "Temperature",
    "side": "bottom",
    "rotation": 0
  },
  {
    "type": "R",
    "name": "R24",
    "value": "10k",
    "x": 10,
    "y": 6,
    "a": "V3V3",
    "b": "NTC_BAT",
    "bom": "temperature_pullups",
    "section": "Temperature",
    "side": "bottom",
    "rotation": 90
  },
  {
    "type": "R",
    "name": "R25",
    "value": "1k",
    "x": 8,
    "y": -9.36,
    "a": "NTC_BAT",
    "b": "TEMP_BAT",
    "bom": "temperature_input_filter",
    "section": "Temperature",
    "side": "bottom",
    "rotation": 0
  },
  {
    "type": "C",
    "name": "C19",
    "value": "100nF",
    "x": 4,
    "y": -9.672,
    "a": "TEMP_BAT",
    "b": "GND",
    "bom": "temperature_filter_caps",
    "section": "Temperature",
    "side": "bottom",
    "rotation": 0
  },
  {
    "type": "R",
    "name": "R26",
    "value": "100k",
    "x": -1,
    "y": -3.9,
    "a": "VBAT",
    "b": "BAT_DIV",
    "bom": "battery_adc_top",
    "section": "Temperature",
    "side": "bottom"
  },
  {
    "type": "R",
    "name": "R27",
    "value": "100k",
    "x": -1,
    "y": -7.488,
    "a": "BAT_DIV",
    "b": "GND",
    "bom": "battery_adc_bottom",
    "section": "Temperature",
    "side": "bottom"
  },
  {
    "type": "R",
    "name": "R28",
    "value": "1k",
    "x": 2,
    "y": -5.304,
    "a": "BAT_DIV",
    "b": "BAT_ADC",
    "bom": "temperature_input_filter",
    "section": "Temperature",
    "side": "bottom",
    "rotation": 90
  },
  {
    "type": "C",
    "name": "C20",
    "value": "100nF",
    "x": 5,
    "y": -6.24,
    "a": "BAT_ADC",
    "b": "GND",
    "bom": "temperature_filter_caps",
    "section": "Temperature",
    "side": "bottom",
    "rotation": 0
  },
  {
    "type": "R",
    "name": "R29",
    "value": "4.7k",
    "x": 0,
    "y": -12.168,
    "a": "V3V3",
    "b": "I2C_SDA",
    "bom": "i2c_pullups",
    "section": "Temperature",
    "side": "bottom",
    "rotation": 0
  },
  {
    "type": "R",
    "name": "R30",
    "value": "4.7k",
    "x": 1.4,
    "y": 2.496,
    "a": "V3V3",
    "b": "I2C_SCL",
    "bom": "i2c_pullups",
    "section": "Temperature",
    "side": "bottom",
    "rotation": 0
  },
  {
    "type": "R",
    "name": "R31",
    "value": "0",
    "x": 2.5,
    "y": -10.2,
    "a": "VBAT",
    "b": "VBOOST_BIAS",
    "bom": "led_bias_link",
    "section": "Light",
    "side": "top"
  },
  {
    "type": "R",
    "name": "R32",
    "value": "0",
    "x": -7.5,
    "y": -15.48,
    "rotation": 180,
    "a": "CELL_N",
    "b": "BQ_VSS",
    "bom": "protection_vss_link",
    "section": "Protection",
    "side": "bottom"
  }
];
