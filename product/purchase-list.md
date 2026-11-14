# 当前版本购买清单

按一台整机净用量列出，用户自行打印、焊接、接线和装配，无厂家预装。123行工程BOM包含打印件、PCB散件及可选试件，不能按123种商品全买。库存和价格仍是历史参考，本次未刷新报价。

整机31件塑料打印件另见打印清单；自行打印时不采购这些成品。六片独立均热片已删除，只加工一体金属热桥1件，制造工艺与报价仍须确认。线束及插壳包络不打印、不作为一个成品下单，用以下电线、连接器和端子自行制作。

## 定制金属加工

|编号|型号或制作规格|净用量|说明|
|---|---|---:|---|
|led_spreader|One-piece aluminium COB thermal bridge with integral branches and shell-contact faces|1|Custom machined solid metal part;COB platform and both shell-contact branches are one piece. Replaces15 aluminium pieces,including6 separate liners;no separate thermal contact shoes or internal clamp screws. Keep electrically insulating thin shell TIM and COB bond.|

## 裸PCB，不含预装器件

|编号|型号或制作规格|净用量|说明|
|---|---|---:|---|
|connection_pcb|Custom40x50mm6-layer1.6mm PCB: TPS61500 COB + DRV8213 fan + ADS1115 temperature + BQ29700 protection|1|40x50x1.6mm6layer,outer1oz/inner2oz;X40 and mounting holes(-16,-11),(16,-11) unchanged. J10/J11 row centres[13.35,5.3912]and[13.35,-4.9048],90degree rotation,pin1originX12.08,pin2X14.62, same pinout. Neighbouring passives,fan bias tap,inner2 sensor GND corridors and off-hole ground transfers updated;F1 relief and cable guides internal only.|
|key_pcbs|Window button daughterboard,14x18mm,2-layer FR41.6mm|2||

## 购买散件、线束材料与耗材

|编号|型号或制作规格|净用量|说明|
|---|---|---:|---|
|controller|Seeed Studio XIAO ESP32C3|1||
|magnet|圆片强力磁铁 Ø30×2 mm（用户指定）|1||
|battery|FLY.18650.3200.3C|1|User selected3200mAh18650. FLY.18650.3200.3C is a bare3.6V cell,typ3200/min3100mAh,max18.6x65.2mm,46g. No built-in protection claimed. Supplier spot-welded tabs/leads plus the new PCB protection are required; no direct cell soldering. Datasheet pp4,7-8.|
|motor|Pololu 5:1 Micro Metal Gearmotor HPCB 6V (no encoder), item3060|1|12x10mm gearbox;3mm D-shaft;4.995:1 internal and3.75:1 belt reduction. Single-cell performance is extrapolated; initial60%PWM, winding current <=0.375A. Long-life carbon brushes; no interchangeable generic N20 accepted without matching motor curve.|
|led_star|HL-LM002H384W-5B2C5(Ra2)(ANSI-4000K)|1|Finished COB light source on its own aluminium substrate,4000K,Ra>=80,13.5x13.5x1.5mm,LES11.2mm. At300mA,Tc25C:570/620/680lm and14/16/18V. Selected nominal266.7mA,approximately4W. The substrate size does not limit brightness to0.5W. Optical/thermal validation of the assembled lamp remains necessary. Datasheet pp2-5.|
|bearings|6800 deep-groove ball bearing 10x19x5mm|2||
|drive_belt|EPDM70A O-ring,32mm inside diameter x1.5mm section, internal drive belt|1|Nominal5.53% neutral-line stretch at23mm centres,30/8mm pitch diameters. Hidden motor slots give+/-0.3mm adjustment. Choose actual preload by slip,current and bearing-temperature tests.|
|internal_mount_screws|M2x6mm ISO4762 stainless steel socket-head screw|1|Single rear horizontal chassis clamp plus front locating pin;length verified by screw-joint build.|
|battery_strap|25mm wide buckle-free double-sided hook-and-loop tape,<=0.8mm single layer,cut75mm|1|One 25mm strap centred Y=0 replaces two 10mm straps;cradle groove widened to26mm. Top overlap only;axial end gate and two buffers retained.|
|battery_foam|PET/polyimide insulating contact film,0.1mm thick,10x20mm|2|Include films,wrap and welded tabs within the reserved19x66.2mm pack envelope;do not add a70mm protected-cell variant.|
|pcb_mount_screws|M2 x 4mm ISO 7045 pan-head stainless steel machine screw|2||
|led_thermal_adhesive|Electrically insulating thermal adhesive,k>=1.5W/mK,bond line0.10-0.15mm|1|Thin bond to finished COB metal substrate;keep light-emitting area and terminals clean. Thermal contact resistance target<=0.75K/W.|
|tail_lock_screws|M2x5mm ISO4762 stainless steel socket-head cap screw|1|One hidden screw on fixed negative-Y half;D-flat short plug supplies anti-rotation.|
|service_screws|M2x8mm ISO4762 stainless steel socket-head screw|2|Two M2x8 normal-Y case clamps,front-upper and rear-lower;kit-generated4mm engagement. Integral rear tongue/groove aligns before clamping. Front and bottom diffusers must both be removed for access;no separate locating parts,new exterior holes,nuts or inserts.|
|heat_mount_screws|M1.6x5mm ISO7045 stainless steel pan-head screw|2|Through3mm aluminium collector into kit-generated ASA pilot joints;do not substitute the former4mm length.|
|led_bracket_screws|M1.6x4mm ISO7045 stainless steel pan-head screw|2||
|window_retainer_screws|M2x6mm ISO4762 stainless steel socket-head cap screw|4|Four internal M2x6 socket-cap screws, two per pane; kit-derived nominal geometry, printed fit still needs coupon.|
|skid_root_screws|M2x8mm ISO4762 stainless steel socket-head cap screw|4|Four M2x8 socket-cap screws into5mm locating pins; internal heads; kit-derived nominal geometry, printed fit still needs coupon.|
|suspension_bolt|M4x90mm ISO10642 stainless steel countersunk socket screw|1||
|suspension_nut|M4 ISO4032 stainless steel hex nut|1||
|bearing_retaining_adhesive|Bearing-retaining adhesive compatible with PETG and steel; bond only outer races to rotor hub|1||
|diffuser_reversible_adhesive|Peelable elastic adhesive compatible with PETG for curved front and belly diffusers|1||
|female_housing_2|2.54mm1x02 narrow female crimp housing,maximum5.6x3x14mm|7|Seven mainboard housings:J2,J3,J4,J5,J6,J7,J12;14mm total installed height. Side-window ends are separate low-profile solder sockets;do not buy nine standard crimp housings.|
|female_housing_7|2.54mm1x07 narrow female crimp housing,maximum3x18.3x14mm|1|J1;0.64mm square mating pins,7contacts;wire fanout to XIAO solder pads.|
|female_contacts|Matching female crimp contacts for0.64mm square pin,24-26AWG|24|24 loose matching crimp contacts=7x2+7+3 for mainboard generic housings;window sockets include their own4contacts;three TE probe plugs use separate6TE contacts. >=3A for power contacts.|
|power_wire|24AWG flexible insulated copper wire,OD<=1.4mm,red1m+black1m|1|24AWG red1m+black1m for protected PACK,motor and shared GND;raw cell leads supplied by spot-weld service. Finished cuts in harness table;no RAW negative Y split.|
|signal_wire|26AWG flexible insulated copper wire,OD<=1.1mm,total4m including>=0.5m white|1|H01/H04/H05/H06/H07/H08 stock;total4m includes>=0.5m white for visible optical cavity. Finished26AWG OD<=1.1mm to match fanout/tip envelopes;NTC adapter OD0.89-1.4mm as separately specified. White COB insulation uses red/yellow end labels,not an extra thick sleeve.|
|usb_cable|USB Type-C data+charge cable1m,slim plug body at most12.35x6.5mm at enclosure entry|1||
|usb_adapter|Regulated5V USB power supply,at least1A,matching USB cable|1||
|magnet_adhesive|Thin-bond two-part epoxy compatible with PETG and nickel-plated NdFeB,small kit|1||
|heatshrink|Heat shrink tube assortment1-4mm,small pack|1||
|insulation_tape|Polyimide insulating tape,10mm wide,one roll|1||
|solder_consumables|Electronics solder+flux,small manual assembly kit|1||
|motor_mount_screws|ISO4762 M1.6x3 socket head cap screw, stainless|2|Through2mm motor plate into existing threaded metal gearbox;1mm engagement.|
|motor_pulley_epoxy|Two-part epoxy adhesive suitable for PETG and steel, small tube|1|Spot at exposed D-shaft/pulley end provides axial retention only. Do not bond motor bearing or gearbox; replace pulley and motor together for service.|
|thermal_probes|HNTC-103F3950FB-100P|3|HNTC-103F3950FB-100P finished epoxy-bead probe,10kohm1%,B25/50=3950K1%,100+/-5mm overall length INCLUDING bead,not free lead length,head max2.8x7.5mm. Typical tau<=15s in liquid; installed thermal lag must be checked. Remote sensors on COB,opaque-shell hot spot and battery. Datasheet pp1,3. Wire gauge is unspecified; do not crimp unknown probe wire directly into22-26AWG terminal. Commission a26AWG terminated adapter with staggered insulated splices.|
|probe_female_housings|TE Connectivity 1375820-2 CST-100 II 2-position housing,2.54mm|3|TE supplier drawing p1: housing2P A5.59+0.25/-0.13mm,12.95mm axial length,6.60mm max cross section,pitch2.54mm;accepts1375819 family. J10/J11 rotated90degrees,row alongX,centreX13.35;conservative installed/service reserve6.5x9x20mm includes14mm plug and6mm bend allowance. 3 probes labelled COB/SHELL/BAT. Supplier drawing envelope,not a supplier STEP model.|
|battery_spot_weld_service|Supplier spot-weld service:18650 nickel tabs,24AWG insulated leads and positive insulating ring|1|Exact bare cell with nickel tabs,positive insulating ring,24AWG red/black leads supplied by battery service;cut stock125/165mm,trim on routing jig. Wrapped cell reserveØ19x66.2mm;do not solder directly to cell.|
|probe_crimp_contacts|TE Connectivity 1375819-1 CST-100 II female crimp contact,22-26AWG|6|Exact1375820 housing contact family;datasheet p1:22-26AWG,insulationOD0.89-1.65mm. Crimp only onto specified26AWG adapter wire,not unspecified factory probe lead.|
|ntc_guide_ties|PA66 cable ties 2.5x100mm,temperature rating>=85C|2|Two2.5x100 ties:one softly anchors H10 alongside+Y motor post,one closes existing lower guide for H11. New H01 guide tie is separately listed.|
|battery_gate_screws|M2x6mm ISO4762 stainless steel socket-head cap screw|2|Kit-generated recessed joints atX=+/-11.3,Y=24,Z=-8mm. Self-forming PETG pilot holes;no metal tapping of the printed part.|
|battery_end_spacers|Silicone foam cushions,7x3x3mm stock,compressed to2.3mm|2|Axial buffers between cell end faces and end stops atY=+/-36.4,Z=-21mm. Keep terminal centre and spot-welded lead exits clear.|
|noncuring_thermal_filler|Electrically insulating non-curing thermal filler,k>=3W/mK,0.1mm installed gaps|1|Only thin electrically insulating shell-contact interfaces;no filler interfaces within monolithic thermal bridge.|
|probe_retention_tape|10mm polyimide electrical-insulation tape,<=0.06mm thick|1|Hold battery NTC over a thin non-curing thermal layer so it can be removed without stripping the cell sleeve. COB and shell probes use insulating thermal adhesive away from solder pads and emitting area.|
|female_housing_3|2.54mm1x03 narrow female crimp housing,maximum8.1x3x14mm|1|J8;3matching contacts included in24 loose contacts;0.64mm square mating pins.|
|key_low_profile_sockets|2.54mm1x02 low-profile solder-wire female socket,body<=8.5mm,total depth<=11.5mm|2|Custom harness termination specification;cross section<=3x5.6mm including insulation,contacts included. No extra PCB. Window ends only;fit actual0.64mm pins. Self-made soldered and heat-shrunk terminations must remain inside total envelope. Physical sample inspection required.|
|controller_guide_tie|PA66 cable tie2.5x100mm,temperature rating>=85C|1|Closes new H01 open guide. Release or replace for deep service;do not compress wire insulation.|

## PCB器件，用户自行焊接

|编号|型号或制作规格|净用量|说明|
|---|---|---:|---|
|headers_2|1x02 2.54mm vertical pin header, 2.54mm insulator, 6mm mating pin|6|J2 raw cell, J3 motor, J4 COB, J5/J6 keys, J7 fan enable; choose0.64mm square-pin2.54mm vertical family rated>=3A for power circuits.|
|headers_7|1x07 2.54mm vertical pin header, 2.54mm insulator, 6mm mating pin|1||
|led_regulator|TPS61500PWP|1|TPS61500 analog-dimming boost topology,2.9-18V input,200mV feedback,3A minimum switch-current limit;3A is NOT LED output current. Rsense0.75ohm1%,nom266.7mA;DIMC1uF,EN5kHz. Selected for full1S discharge coverage and matched14-18V COB; obsolete MEL7135/Q2 path cannot drive this source. Datasheet pp3-6,10-15,18-19.|
|gate_resistors|0603WAF1000T5E|2|R1 filtered DRV8213 VCC feed100ohm;R3 TPS61500 EN control series100ohm.|
|bias_resistors|RC0603FR-07100KL|4|R2 fan-input pulldown,R4 lamp EN pulldown,R5 USB sense divider top,R10 fan nFAULT pullup,100kohm each.|
|decoupling|CC0603KRX7R9BB104|5||
|bulk|CL21A106KAYNNNE|1||
|switches|KH-6X6X4.3H-STM|2||
|key_headers|1x02 2.54mm vertical pin header for window daughterboard|2||
|usb_sense_bottom|0603WAF1503T5E|2|Two150kohm resistors:R6 USB sense bottom andR7 fan VREF divider top.|
|fan_driver|DRV8213RTER|1|Current regulation and latched stall shutdown at1S voltage; no Basic candidate with the same functions was found. WQFN requires reflow assembly.|
|fan_current_scale|0603WAF4991T5E|1|4.99k IPROPI resistor; AIPROPI205uA/A.|
|fan_vref_bottom|0603WAF2202T5E|1|22k bottom with150k top gives VREF=VBAT*22/172.|
|fan_start_timer|CL10B474KA8NNNC|1|470nF timer: nominal3.055s startup blanking.|
|fan_bulk|CL31A476MPHNNNE|1|47uF10V1206 local motor input bulk; capacitance under DC bias must be checked on prototype.|
|led_inductor|MHCC06030-100M-R7|1|MHCC06030-100M-R7 shielded10uH20%,DCR68mohm max,Isat5.5A typ at30% inductance drop,Irms4A typ at40C rise;7.3x6.6x3mm. At8uH and assumed480kHz low-frequency bound,calculated worst switch peak2.49A. Supplier datasheet pp2,17 marks series not for new design; accepted for limited-stock prototype,requires lifecycle substitution review before production.|
|led_schottky|SS3P6L-M3/86A|1|SS3P6L-M3/86A,60V3A,TO-277A,chosen from TPS61500 recommended diode family; reverse rating exceeds40V switch rating. AverageLED current<=0.277A; calculated inductor peak2.49A. Datasheet pp1-2; footprint/polarity to be checked in PCB revision.|
|thermal_adc|ADS1115IDGSR|1|ADS1115IDGSR,3.3V I2C four-input ADC: AIN0 COB NTC,AIN1 shell NTC,AIN2 battery NTC,AIN3 divided protected battery. ADDR ground gives0x48;100nF bypass,4.7k I2C pull-ups. Uses explicitly remapped XIAO D7/GPIO20 SDA and D6/GPIO21 SCL; default I2C GPIO6/7 already drive loads. Datasheet pp3-5,11,23.|
|battery_protection_ic|BQ29700DSER|1|BQ29700DSER1S protector:OVP4.275V,UVP2.8V,OCD100mV20ms,SCD500mV250us nominal. Common-drain back-to-back low-side FET application with330ohm BAT filter,100nF,2.2kohm V-minus resistor,5Mohm gate-source bleeds. All loads and XIAO charging connect to PACK side,never bypass CELL-minus. Datasheet pp4-8,21-22.|
|battery_protection_fets|CSD85301Q2|5|Five paralleled back-to-back pairs using each CSD85301Q2 independent dual N-MOS;join drains externally,balanced copper. Rds each max39mohm atVgs2.5V,Tj25C;combined five-pair path max15.6mohm. One pair would trigger100mV protection too early at this load. Design bound1.5x hot Rds plus3mohm traces gives26.4mohm,85mV minimum OCD=>3.22A above2.63A load budget. Hot factor and sharing require prototype measurement; protector is not a calibrated current limiter. Datasheet pp1,3-4.|
|battery_fuse|0451004.MRL|1|Littelfuse0451004.MRL,4A125V very-fast fuse,2410;series raw cell positive at battery entry. Datasheet p2 givesRnom16mohm andI2t3.152A2s;catalogI2t0.0551 is inconsistent and NOT used. Secondary fault protection,not a4A constant-current limiter. Startup inrush/temperature coordination must be tested.|
|led_sense_resistor|0.75ohm1%1206 current-sense resistor,>=0.25W|1|Rsense Kelvin route,200mV nominal;nom266.67mA,bounds257.43..276.09mA including195..205mV FB and1%R;maxdissipation0.0566W.|
|led_freq_resistor|176kohm1%0603 resistor|1|TPS61500 FREQ nominal600kHz;frequency tolerance not specified for this exact resistor in datasheet,480kHz used as sensitivity assumption,not guaranteed limit.|
|led_ovp_top|158kohm1%0603 resistor|1|OVP upper resistor,Vnom20.6472V,min19.6527,max21.6729 including1%R and1.192..1.266V reference.|
|led_ovp_bottom|10kohm1%0603 resistor|1|OVP lower resistor;above LED14..18V plus3%VF measurement bound andFB0.205V.|
|led_soft_start|47nF X7R25V0603 capacitor|1|SS soft-start capacitor per TI guidance.|
|led_compensation|470nF X7R16V0603 capacitor|1|COMP to ground;layout and loop response must be checked on new board.|
|led_dim_filter|1uF X7R10V0805 capacitor|1|DIMC to ground selects analog dimming;5kHz EN input. Start with continuous HIGH>=50ms before reducing duty;datasheet minimum start PWM on-time is200us,not20us.|
|led_input_cap|4.7uF X7R10V0805 capacitor|1|Local VIN/PGND bypass,effective>=3.3uF at4.2V;shared battery bulk capacitor remains.|
|led_output_caps|2.2uF X7R50V1210 capacitor|2|4.4uF nominal total,require>=2.2uF combined at21.7V from chosen supplier DC-bias curve;1..10uF effective output range.|
|led_bleeder|1Mohm1%0603 resistor|1|Across boosted output to discharge capacitance;do not hot-plug COB at charged output.|
|temperature_pullups|10kohm0.1%0603 resistor|3|3.3V to each NTC node,NTC toPACK_GND;maxNTC selfheat0.273mW at3.3V.|
|temperature_input_filter|1kohm1%0603 resistor|4|Series ADC input resistors;separate analogue returns from switching ground.|
|temperature_filter_caps|100nF X7R16V0603 capacitor|4|One per ADC input;NTC settling and multiplexer timing handled in firmware.|
|i2c_pullups|4.7kohm1%0603 resistor|2|SDA/SCL pull-ups to3.3V,100kHz internal bus.|
|battery_adc_top|100kohm1%0603 resistor|1|Protected battery toAIN3 divider top.|
|battery_adc_bottom|100kohm1%0603 resistor|1|AIN3 divider bottom,2.1V nominal at4.2V battery.|
|protection_bat_filter|330ohm1%0603 resistor|1|BQ29700 BAT input filter.|
|protection_vminus|2.2kohm1%0603 resistor|1|PACK-minus toBQ29700 V-minus.|
|protection_gate_bleeds|5.1Mohm1%0603 resistor|2|Shared CHG/DSG gate-to-source bleed resistors,close to paired FET bank.|
|added_bypass|100nF X7R16V0603 capacitor|2|One BQ29700 BAT-VSS,one ADS1115 VDD-GND.|
|thermal_header|1x03 2.54mm vertical pin header,2.54mm body,6mm mating pin|1|Internal extension forXIAO3V3,D7 SDA,D6 SCL;not an exterior port.|
|probe_headers|1x02 2.54mm vertical pin header,2.54mm body,6mm mating pin|3|Three internal probe ports,NTC input plus ground;avoid swapped channels.|
|protected_battery_header|1x02 2.54mm vertical power header,rated>=3A,2.54mm body,6mm mating pins|1|NewPACK+/-outputtoXIAOBAT+/BAT-;allXIAOgroundsPACK-side. Do not reuse raw-cell negative as ground.|
|led_bias_link|0ohm0603 resistor|1|R31 populated0ohm0603 separates the TPS61500 VIN-bias/C3 branch from the 3A inductor feeder.|
|protection_vss_link|0ohm0603 resistor|1|R32 populated0ohm0603 forms Kelvin raw-cell-negative reference for U4 VSS,C15 bypass andR19 discharge gate bleed; not a load return.|

## 专用操作工具

|编号|型号或制作规格|净用量|说明|
|---|---|---:|---|
|hex_key_1p5|Wera950 PKLS L-key,metric,chrome plated,1.5x90mm (05022040001)|1|Manufacturer90/4.5mm arms,Wera05022040001. Tool geometry checks include5mm threaded withdrawal,60degree re-indexing,key disengagement and ordinary hand seating/removal of freed screws. Shaft envelope1.8mm,bend envelope4.5mm are conservative engineering defaults;actual fit/torque not measured.|

## 可选USB试配件，默认不采购

|编号|型号或制作规格|净用量|说明|
|---|---|---:|---|
|controller_mount_screws|M1.6x5mm ISO4762 stainless steel socket-head cap screw|2|Optional charging-fit coupon only;main XIAO support is integral and uses no separate mounting screws.|
|charging_fit_shell_print|Optional USB fit-test print set: local coupon shell x1 and test XIAO cassette x1|1|Test fixture only;main unit uses integral chassis rails. Two M1.6x5 screws belong to coupon,not final lamp.|

## 紧固件合并采购数量

|规格|整机净用量|用途|
|---|---:|---|
|M2×8 ISO4762内六角|6|锁壳2、起落架4|
|M2×6 ISO4762内六角|7|内架1、窗压环4、电池端挡2|
|M2×5 ISO4762内六角|1|尾梁|
|M2×4 ISO7045盘头十字|2|主板|
|M1.6×3 ISO4762内六角|2|电机|
|M1.6×4 ISO7045盘头十字|2|反光罩|
|M1.6×5 ISO7045盘头十字|2|一体热桥|
|M4×90 ISO10642沉头内六角|1|承重连接|
|M4 ISO4032六角螺母|1|承重连接|

合计23颗螺钉及1颗螺母。可选USB试件另需M1.6×5 ISO4762内六角2颗，不与热桥盘头螺钉混用。表格是前面分项的合并视图，不额外加购。

## 接插件与耗材避免重复购买

普通母插壳：2P共7只、7P与3P各1只，普通端子共24只。三路NTC另用TE1375820-2插壳3只及1375819-1端子6只。窗端另用低型焊线母座2只，不能买成普通14mm高母壳。所有包络均包含焊线/绝缘空间，实际买到的插壳不得超过列出的尺寸。

聚酰亚胺胶带两行用途可用同一卷（10mm宽、厚≤0.06mm）；三处扎带合计3根；按包装采购而非重复计入装配数量。导线毛坯长度和引线修整按现行线束裁线表，不能按三维管状包络买塑料管。

## 自备工具与试装

确认有小号十字螺丝刀、匹配M4承重螺栓/螺母的扳手、电烙铁、剥线钳、适配普通及TE端子的压接工具和万用表；已有则不重复买。指定1.5mm超短臂扳手用于前/底两口锁壳，普通长短臂尺寸不能自动视为可替代。电池选带点焊引线规格，不直接在裸电芯上锡焊。

可先打印和采购已确定的散件；一体铝热桥须先拿到可制造方案与报价，整机配合、温升、保护和承重仍待样机实测。
