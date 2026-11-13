# 最简装配首样采购与询价清单

用户实际采购：下壳功能总成1套、上盖旋翼总成1套；可由厂家整机交付时优先整机交付。以下140行仅为加工商备料，不是要求用户逐件购买和装配。

对应47a887e8机身、171fcced主板和53c419c4按键板。安装数量如下；MOQ与备用数量另行询价。本表从当前BOM同步，库存和价格未刷新，不承诺国内全有现货。

铝件15件按AL01–15各1件，组别BOM行不得再另加完整总成。线束默认工厂预装：散料供料、服务行只计人工；工厂包料则扣除对应散料。普通母壳9只/触点24、窗端短母座2只自带4触点、TE壳3只/触点6；不要按旧21触点或旧100mm统长下单。

|编号|确切料号/制造规格|安装数量|采购说明|
|---|---|---|---|
|controller|Seeed Studio XIAO ESP32C3|1|现成XIAO整板，自带Type-C与充电，无须另买充电模块。|
|magnet|圆片强力磁铁 Ø30×2 mm（用户指定）|1|Ø30×2mm钕铁硼圆片，不用带壳加厚型。槽深1.5mm；磁力和涂层钢架上的保持力仍需验证。|
|connection_pcb|Custom40x50mm6-layer1.6mm PCB: TPS61500 COB + DRV8213 fan + ADS1115 temperature + BQ29700 protection|1|40x50mm6层1.6mm外1oz/内2oz，76器件模型已补齐并装配检查。采用现用171fcced制造包；双面手工或委托回流，不把空JLC自动SMT清单当包焊订单。六层、双面装配及铝件按新图询价，旧100–250元小板估价失效。|
|battery|FLY.18650.3200.3C|1|User selected3200mAh18650. FLY.18650.3200.3C is a bare3.6V cell,typ3200/min3100mAh,max18.6x65.2mm,46g. No built-in protection claimed. Supplier spot-welded tabs/leads plus the new PCB protection are required; no direct cell soldering. Datasheet pp4,7-8.|
|motor|Pololu 5:1 Micro Metal Gearmotor HPCB 6V (no encoder), item3060|1|12x10mm gearbox;3mm D-shaft;4.995:1 internal and3.75:1 belt reduction. Single-cell performance is extrapolated; initial60%PWM, winding current <=0.375A. Long-life carbon brushes; no interchangeable generic N20 accepted without matching motor curve.|
|led_star|HL-LM002H384W-5B2C5(Ra2)(ANSI-4000K)|1|Finished COB light source on its own aluminium substrate,4000K,Ra>=80,13.5x13.5x1.5mm,LES11.2mm. At300mA,Tc25C:570/620/680lm and14/16/18V. Selected nominal266.7mA,approximately4W. The substrate size does not limit brightness to0.5W. Optical/thermal validation of the assembled lamp remains necessary. Datasheet pp2-5.|
|bearings|6800 deep-groove ball bearing 10x19x5mm|2|6800标准轴承10×19×5mm，优先低摩擦金属防尘盖型ZZ；不能改变摩擦负载后仍沿用未验证的电机结论。|
|headers_2|1x02 2.54mm vertical pin header, 2.54mm insulator, 6mm mating pin|6|J2 raw cell, J3 motor, J4 COB, J5/J6 keys, J7 fan enable; choose0.64mm square-pin2.54mm vertical family rated>=3A for power circuits.|
|headers_7|1x07 2.54mm vertical pin header, 2.54mm insulator, 6mm mating pin|1||
|led_regulator|TPS61500PWP|1|TPS61500 analog-dimming boost topology,2.9-18V input,200mV feedback,3A minimum switch-current limit;3A is NOT LED output current. Rsense0.75ohm1%,nom266.7mA;DIMC1uF,EN5kHz. Selected for full1S discharge coverage and matched14-18V COB; obsolete MEL7135/Q2 path cannot drive this source. Datasheet pp3-6,10-15,18-19.|
|gate_resistors|0603WAF1000T5E|2|R1 filtered DRV8213 VCC feed100ohm;R3 TPS61500 EN control series100ohm.|
|bias_resistors|RC0603FR-07100KL|4|R2 fan-input pulldown,R4 lamp EN pulldown,R5 USB sense divider top,R10 fan nFAULT pullup,100kohm each.|
|decoupling|CC0603KRX7R9BB104|5||
|bulk|CL21A106KAYNNNE|1||
|switches|KH-6X6X4.3H-STM|2|两块按键板各1只6×6×4.3mm，不能改买不同总高的按钮。|
|drive_belt|EPDM70A O-ring,32mm inside diameter x1.5mm section, internal drive belt|1|Nominal5.53% neutral-line stretch at23mm centres,30/8mm pitch diameters. Hidden motor slots give+/-0.3mm adjustment. Choose actual preload by slip,current and bearing-temperature tests.|
|led_spreader|1050/1060 aluminium COB collector,18x34x3mm,2xM2 tapped thermal-bridge holes|1|铝件总数15：集热板1、桥2、上盖连接件2、接触座4、内衬6；各AL01–15一件，禁止重复采购总成和组成件。按同版STEP与15页图加工。|
|belly_diffuser|Printed translucent PETG belly diffuser, diameter 63.75mm, thickness 1.2mm|1||
|nose_diffuser|Printed translucent PETG nose diffuser, opening approximately59.5mm|1||
|button_caps|Opaque pale-blue curved Ø12mm button caps,Ø14mm internal flange,calibrated pusher,bulb/fan icons|2||
|fixed_windows|Pale-blue curved window insert,37.5mm register,42.6mm shoulder,12.5mm button bore,open rear PCB guides|2|Pale-blue pane with37.5mm register,42.6mm shoulder; separate12mm button in12.5mm clearance hole; internal retaining ring; independent white overlay frame.|
|main_rotor_print|Printed white four-blade main rotor,diameter250mm,chord37.5mm,blade thickness1.6mm|1|250mm一体旋翼，厚度保持1.6mm；需更大有效平台或打印服务，动平衡和允许转速尚未验证。|
|skid_print|White90mm landing skid with curved struts and internally retained mounting roots|2|Curved struts; rail Z=-51.25mm,Y=+/-56.25mm; mounts X=+/-22.5mm,Z=-25mm;26.25mm vertical drop; front/rear symmetric; internally retained5mm pins.|
|tail_print|Solid sky-blue tail boom,50mm symmetric vertical fin,right half-profile trim,4mm cylindrical locating plug and circular shoulder|1|Solid circular taper and full-round4mm locating plug with circular bearing shoulder; two hidden axial M2 screws. Symmetric vertical fin and same-half-profile right trim are integral; left white decorative tail propeller is separate.|
|tail_prop_print|Printed white three-blade decorative tail propeller, rounded paddle blades, domed hub and locating pin|1|White three-blade decorative left tail propeller; centre[176.875,-4.625,13.75]mm; aft offset1.875mm;3mm pin in3.5mm blind socket.|
|window_bezel_left_print|Printed white curved overlay window frame, left|1|Independent white PETG ring covering pale-blue window edge by 0.5mm; curved back follows cabin surface with nominal 0.15mm glue allowance; free curved adhesive interface.|
|window_bezel_right_print|Printed white curved overlay window frame, right|1|Independent white PETG ring covering pale-blue window edge by 0.5mm; curved back follows cabin surface with nominal 0.15mm glue allowance; free curved adhesive interface.|
|internal_carrier_print|PETG removable motor/PCB carrier with F1 relief, NTC guides and recessed cradle-tie seats|1|Approved exterior retained. Separate18650 cradle attaches using two2.5mm PA66 ties; integral PETG hard datums fix2mm deck gap and four stops locate laterally. Support cradle before cutting ties; PCB and motor stay on carrier during withdrawal.|
|internal_mount_screws|M2 x 6mm ISO 7045 pan-head stainless steel machine screw|2||
|battery_strap|10mm wide buckle-free double-sided hook-and-loop tape,<=0.8mm single layer,cut75mm|2|Two removable straps atY=+/-7mm. Recessed saddles accept0.8mm strap with0.8mm overlap at the top;no bulky buckle. Keep the bottom overlap-free.|
|battery_foam|PET/polyimide insulating contact film,0.1mm thick,10x20mm|2|Include films,wrap and welded tabs within the reserved19x66.2mm pack envelope;do not add a70mm protected-cell variant.|
|pcb_mount_screws|M2 x 4mm ISO 7045 pan-head stainless steel machine screw|2||
|key_headers|1x02 2.54mm vertical pin header for window daughterboard|2|主板普通2P六组+J12一组；按键板另2组；NTC三组另列。不要将合计数量混写成同一BOM行。|
|key_pcbs|Window button daughterboard,14x18mm,2-layer FR41.6mm|2|同一14×18mm按键板制作2块，2层FR4、1.6mm；左右同板不同装配朝向。|
|drive_pulley_print|White PETG D-shaft pulley,8mm effective diameter,3mm bore with flat at1mm; calibrate fit and spot-epoxy axial retention|1||
|controller_cassette_print|PETG removable horizontal XIAO cassette below battery,USB facing rear through raised opening|1|Current horizontal XIAO cassette plus three internalR1 solder-wire reliefs at D6/D7/VBUS;charging fit coupon synchronized. Port centre and visible opening unchanged.|
|led_thermal_adhesive|Electrically insulating thermal adhesive,k>=1.5W/mK,bond line0.10-0.15mm|1|Thin bond to finished COB metal substrate;keep light-emitting area and terminals clean. Thermal contact resistance target<=0.75K/W.|
|tail_lock_screws|M2x5mm ISO4762 stainless steel socket-head cap screw|2||
|service_screws|M2x10mm ISO4762 stainless steel socket-head screw|3||
|controller_mount_screws|M1.6x5mm ISO4762 stainless steel socket-head cap screw|2||
|heat_mount_screws|M1.6x5mm ISO7045 stainless steel pan-head screw|2|Through3mm aluminium collector into kit-generated ASA pilot joints;do not substitute the former4mm length.|
|fuselage_lower_print|Sky-blue PETG100mm spherical lower cabin with fully internal mounting supports|1||
|fuselage_cap_print|Sky-blue PETG removable upper cabin cap|1||
|led_bracket_left_print|White ASA left detachable COB collector support|1|Use ASA for the two hot collector supports;0.2mm layers,0.4mm nozzle. Collector screw joint is generated for ASA. Keep the carrier and battery cradle PETG; machine no visible exterior openings.|
|led_bracket_right_print|White ASA right detachable COB collector support|1|Use ASA for the two hot collector supports;0.2mm layers,0.4mm nozzle. Collector screw joint is generated for ASA. Keep the carrier and battery cradle PETG; machine no visible exterior openings.|
|led_bracket_screws|M1.6x4mm ISO7045 stainless steel pan-head screw|2||
|window_retainer_print|White PETG curved-window clamp with integrated removable button stop,PCB rear pads and lower ledge|2|Internal U-ring and curved saddle feet clamp each pane shoulder against the100mm cabin; twoM2x6 per window.|
|window_retainer_screws|M2x6mm ISO4762 stainless steel socket-head cap screw|4|Four internal M2x6 socket-cap screws, two per pane; kit-derived nominal geometry, printed fit still needs coupon.|
|skid_root_caps_print|White PETG curved internal saddle cap,9.2mm OD,6.7mm peg cavity,quantity4|4|Four independently printable curved saddle caps,9.2mm OD,6.7mm cavity; two per skid, matching the sphere interior.|
|skid_root_screws|M2x8mm ISO4762 stainless steel socket-head cap screw|4|Four M2x8 socket-cap screws into5mm locating pins; internal heads; kit-derived nominal geometry, printed fit still needs coupon.|
|rotor_bearing_spacer_print|PETG bearing outer-race spacer,19mm OD,16mm ID,7.9mm long|1|7.9mm spacer bears only on the two6800 outer races; separate from stationary inner spacer.|
|rotor_inner_spacer_print|PETG bearing inner-race spacer,12.6mm OD,10.2mm ID,7.9mm long|1||
|suspension_bolt|M4x90mm ISO10642 stainless steel countersunk socket screw|1|暂缓直接下单：M4×90 ISO10642沉头内六角，A2/304，90mm含头。尚无完全匹配现货证据，向紧固件商询价；不能换成ISO4762圆柱头或DIN965十字沉头。|
|suspension_nut|M4 ISO4032 stainless steel hex nut|1|M4 ISO4032普通六角螺母，螺距0.7mm；没有另加垫圈或加厚件的空间验证。|
|bearing_retaining_adhesive|Bearing-retaining adhesive compatible with PETG and steel; bond only outer races to rotor hub|1|须供应商明确兼容PETG和钢，只粘外圈，不进入滚道；不默认用仅适于金属的厌氧胶。|
|magnet_base_print|White PETG magnetic cup,45mm OD,13.75mm high,30.3mm pocket1.5mm deep|1||
|mast_print|White PETG stepped hollow mast,visible13.5x33.95mm,12.6mm inner-race foot7.05mm long|1||
|rotor_fixed_axle_print|White PETG9.8mm fixed axle with12.6mm lower inner-race shoulder,4.6mm bolt bore|1||
|hub_cover_print|White PETG32.5mm rotor hub cover with integral outer-race retainer|1||
|diffuser_reversible_adhesive|Peelable elastic adhesive compatible with PETG for curved front and belly diffusers|1|可剥离弹性胶，灯罩及覆盖窗框使用；先验证PETG粘接与透光外观。|
|usb_sense_bottom|0603WAF1503T5E|2|Two150kohm resistors:R6 USB sense bottom andR7 fan VREF divider top.|
|female_housing_2|2.54mm1x02 narrow female crimp housing,maximum5.6x3x14mm|7|Seven mainboard housings:J2,J3,J4,J5,J6,J7,J12;14mm total installed height. Side-window ends are separate low-profile solder sockets;do not buy nine standard crimp housings.|
|female_housing_7|2.54mm1x07 narrow female crimp housing,maximum3x18.3x14mm|1|J1;0.64mm square mating pins,7contacts;wire fanout to XIAO solder pads.|
|female_contacts|Matching female crimp contacts for0.64mm square pin,24-26AWG|24|24 loose matching crimp contacts=7x2+7+3 for mainboard generic housings;window sockets include their own4contacts;three TE probe plugs use separate6TE contacts. >=3A for power contacts.|
|power_wire|24AWG flexible insulated copper wire,OD<=1.4mm,red1m+black1m|1|24AWG red1m+black1m for protected PACK,motor and shared GND;raw cell leads supplied by spot-weld service. Finished cuts in harness table;no RAW negative Y split.|
|signal_wire|26AWG flexible insulated copper wire,OD<=1.1mm,total4m including>=0.5m white|1|H01/H04/H05/H06/H07/H08 stock;total4m includes>=0.5m white for visible optical cavity. Finished26AWG OD<=1.1mm to match fanout/tip envelopes;NTC adapter OD0.89-1.4mm as separately specified. White COB insulation uses red/yellow end labels,not an extra thick sleeve.|
|usb_cable|USB Type-C data+charge cable1m,slim plug body at most12.35x6.5mm at enclosure entry|1|必须支持数据，插头包胶在入口处≤12.35×6.5mm；XIAO插口实际高度尚待样板适配核对。|
|usb_adapter|Regulated5V USB power supply,at least1A,matching USB cable|1|普通合规5V≥1A电源，不用9V/12V诱骗板。|
|magnet_adhesive|Thin-bond two-part epoxy compatible with PETG and nickel-plated NdFeB,small kit|1|PETG/镀镍钕铁硼兼容的薄胶层，固定磁铁。|
|heatshrink|Heat shrink tube assortment1-4mm,small pack|1||
|insulation_tape|Polyimide insulating tape,10mm wide,one roll|1||
|solder_consumables|Electronics solder+flux,small manual assembly kit|1||
|xiao_shim_print|Removable PETG XIAO PCB support shim,20.5x17.2x0.6mm,for1.0mm model board in1.9mm slot;omit for1.6mm bare board|1||
|charging_fit_shell_print|Optional local USB-C curved shell fit-test coupon,approximately25.55x46x20.25mm;reuse main XIAO cassette and2xM1.6x5 screws|1||
|fan_driver|DRV8213RTER|1|Current regulation and latched stall shutdown at1S voltage; no Basic candidate with the same functions was found. WQFN requires reflow assembly.|
|fan_current_scale|0603WAF4991T5E|1|4.99k IPROPI resistor; AIPROPI205uA/A.|
|fan_vref_bottom|0603WAF2202T5E|1|22k bottom with150k top gives VREF=VBAT*22/172.|
|fan_start_timer|CL10B474KA8NNNC|1|470nF timer: nominal3.055s startup blanking.|
|fan_bulk|CL31A476MPHNNNE|1|47uF10V1206 local motor input bulk; capacitance under DC bias must be checked on prototype.|
|motor_mount_screws|ISO4762 M1.6x3 socket head cap screw, stainless|2|Through2mm motor plate into existing threaded metal gearbox;1mm engagement.|
|motor_pulley_epoxy|Two-part epoxy adhesive suitable for PETG and steel, small tube|1|Spot at exposed D-shaft/pulley end provides axial retention only. Do not bond motor bearing or gearbox; replace pulley and motor together for service.|
|fan_enable_harness|H07 two-wire harness assembly service,26AWG,cut stock160/170mm|1|J7 to XIAO D5/GND,joining H01 common loom. Housing,contacts and wire listed separately;this row is assembly labour,not a second materials kit.|
|led_inductor|MHCC06030-100M-R7|1|MHCC06030-100M-R7 shielded10uH20%,DCR68mohm max,Isat5.5A typ at30% inductance drop,Irms4A typ at40C rise;7.3x6.6x3mm. At8uH and assumed480kHz low-frequency bound,calculated worst switch peak2.49A. Supplier datasheet pp2,17 marks series not for new design; accepted for limited-stock prototype,requires lifecycle substitution review before production.|
|led_schottky|SS3P6L-M3/86A|1|SS3P6L-M3/86A,60V3A,TO-277A,chosen from TPS61500 recommended diode family; reverse rating exceeds40V switch rating. AverageLED current<=0.277A; calculated inductor peak2.49A. Datasheet pp1-2; footprint/polarity to be checked in PCB revision.|
|thermal_adc|ADS1115IDGSR|1|ADS1115IDGSR,3.3V I2C four-input ADC: AIN0 COB NTC,AIN1 shell NTC,AIN2 battery NTC,AIN3 divided protected battery. ADDR ground gives0x48;100nF bypass,4.7k I2C pull-ups. Uses explicitly remapped XIAO D7/GPIO20 SDA and D6/GPIO21 SCL; default I2C GPIO6/7 already drive loads. Datasheet pp3-5,11,23.|
|thermal_probes|HNTC-103F3950FB-100P|3|HNTC-103F3950FB-100P finished epoxy-bead probe,10kohm1%,B25/50=3950K1%,100+/-5mm overall length INCLUDING bead,not free lead length,head max2.8x7.5mm. Typical tau<=15s in liquid; installed thermal lag must be checked. Remote sensors on COB,opaque-shell hot spot and battery. Datasheet pp1,3. Wire gauge is unspecified; do not crimp unknown probe wire directly into22-26AWG terminal. Commission a26AWG terminated adapter with staggered insulated splices.|
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
|thermal_harness|H08 three-wire harness assembly service,26AWG,cut stock150/150/145mm|1|J8 to XIAO3V3/D7/D6,joining H01 common loom;housing,contacts and stock wire separately listed.|
|probe_headers|1x02 2.54mm vertical pin header,2.54mm body,6mm mating pin|3|Three internal probe ports,NTC input plus ground;avoid swapped channels.|
|probe_female_housings|TE Connectivity 1375820-2 CST-100 II 2-position housing,2.54mm|3|TE supplier drawing p1: housing2P A5.59+0.25/-0.13mm,12.95mm axial length,6.60mm max cross section,pitch2.54mm;accepts1375819 family. J10/J11 rotated90degrees,row alongX,centreX13.35;conservative installed/service reserve6.5x9x20mm includes14mm plug and6mm bend allowance. 3 probes labelled COB/SHELL/BAT. Supplier drawing envelope,not a supplier STEP model.|
|battery_spot_weld_service|Supplier spot-weld service:18650 nickel tabs,24AWG insulated leads and positive insulating ring|1|Exact bare cell with nickel tabs,positive insulating ring,24AWG red/black leads supplied by battery service;cut stock125/165mm,trim on routing jig. Wrapped cell reserveØ19x66.2mm;do not solder directly to cell.|
|conformal_heat_spreaders|Six-piece formed1050/1060 aluminium shell-liner set,0.5mm thick,about72.1cm2 equivalent area|1|Two fore,two aft,two cap liners fit the actual100mm cabin and avoid windows,skid roots,seams,USB and antenna. Bond to shell with<=0.15mm insulating thermal adhesive.72.1cm2 is volume/thickness equivalent metal area,not a verified thermal capacity. The500lx warm-state reading target remains unchanged.|
|heat_transfer_straps|1050/1060 aluminium removable thermal bridge,left and right|2|Two1050/1060 aluminium thermal bridges AL02/03;open R4 NTC exit channel replaces R2.1. Mounting axes and thermal interfaces unchanged;use final STEP and drawings.|
|internal_reflector|Opaque matte-white ASA internal reflector with front mixing port and glare visor|1|1.6mm wall;top Z-4,bottom Z-25.5;front16x2mm port,25deg visor. Bond two front-facing lands to ASA supports with0.2mm peelable adhesive. Remove with both supports as one group after collector removal;not a shell-glued hooked insert.|
|protected_battery_header|1x02 2.54mm vertical power header,rated>=3A,2.54mm body,6mm mating pins|1|NewPACK+/-outputtoXIAOBAT+/BAT-;allXIAOgroundsPACK-side. Do not reuse raw-cell negative as ground.|
|protected_battery_harness|H12 protected PACK harness assembly service,24AWG,cut stock150mm each|1|J12 to actual XIAO bottom BAT pads;housing/contacts/wire separately listed. Route under cassette;never join RAW negative.|
|led_bias_link|0ohm0603 resistor|1|R31 populated0ohm0603 separates the TPS61500 VIN-bias/C3 branch from the 3A inductor feeder.|
|protection_vss_link|0ohm0603 resistor|1|R32 populated0ohm0603 forms Kelvin raw-cell-negative reference for U4 VSS,C15 bypass andR19 discharge gate bleed; not a load return.|
|probe_crimp_contacts|TE Connectivity 1375819-1 CST-100 II female crimp contact,22-26AWG|6|Exact1375820 housing contact family;datasheet p1:22-26AWG,insulationOD0.89-1.65mm. Crimp only onto specified26AWG adapter wire,not unspecified factory probe lead.|
|probe_adapter_service|Three NTC harness adaptation services,finished head-to-housing stock125/80/105mm|1|H09 COB125,H10 SHELL80,H11 BAT105;includes7.5mm head and14mm housing,not extra extension. Use26AWG adapter OD0.89-1.4mm for TE1375819-1. Stagger splices>=8mm,individual heatshrink<=1.8mm and pair<=3.4mm;3housings/6contacts separately listed. Cut and preform on jig;no added15-20mm loose loops.|
|ntc_guide_ties|PA66 cable ties 2.5x100mm,temperature rating>=85C|2|Two2.5x100 ties:one softly anchors H10 alongside+Y motor post,one closes existing lower guide for H11. New H01 guide tie is separately listed.|
|battery_cradle_print|PETG transverse18650 cradle and removable end gate,two-piece set|1|For19x66.2mm maximum wrapped/tabbed cell at[0,0,-24],axisY.0.3mm radial hard clearance,two straps,two axial cushions and two M2x6 gate screws. PETG,0.2mm layers,0.4mm nozzle;band wall remaining after strap groove>=1.25mm. Integral2mm hard deck datums and3mm lateral stops;X/Y clearance0.3/0.4mm. No compressible deck spacer.|
|battery_gate_screws|M2x6mm ISO4762 stainless steel socket-head cap screw|2|Kit-generated recessed joints atX=+/-11.3,Y=24,Z=-8mm. Self-forming PETG pilot holes;no metal tapping of the printed part.|
|battery_end_spacers|Silicone foam cushions,7x3x3mm stock,compressed to2.3mm|2|Axial buffers between cell end faces and end stops atY=+/-36.4,Z=-21mm. Keep terminal centre and spot-welded lead exits clear.|
|battery_cradle_ties|PA66 cable tie2.5x100mm,band<=0.8mm,head<=4.6x3.4x4.6mm|2|Route through aligned deck/cradle slots atX=-2,Y=+/-17mm. Heads face outward below PCB. Two recessed deck seats protect solder tails. Cut for deep service and replace;buy spare ties. Separate from the two NTC-guide ties.|
|thermal_upper_links|1050/1060 aluminium upper-cap heat link,left and right|2|Bond spherical feet to the cap liners with0.1mm insulating thermal adhesive. Lower planar lap interfaces atZ26/26.1 use0.1mm non-curing thermal filler;links leave with upper cap.|
|thermal_contact_shoes|1050/1060 aluminium spherical thermal contact shoes,fore/aft,left/right set|1|Four metal pieces. Spherical faces couple to lower shell liners through0.1mm non-curing insulating thermal filler;they remain removable. M1.6x0.35 through threads:1.25mm tap drill,not the modeled1.6mm major envelope. Disconnect four bridge screws before extracting shoes.|
|thermal_contact_screws|M1.6x10mm ISO4762 stainless steel socket-head cap screw|4|Recessed0.1mm below thermal-bridge top.3.4mm counterbore,1.7mm deep;1.9mm bridge clearance bore. About1.6mm engagement in aluminium contact shoes. Fore axes[-28,+/-24],aft[27,+/-24.5].|
|thermal_clamp_screws|M2x8mm ISO4762 stainless steel socket-head cap screw|2|Clamp4mm bridge root plus0.1mm thermal layer into3mm tapped collector. Tip protrusion about0.9mm occurs beyond the COB footprint atY=+/-14.5.|
|noncuring_thermal_filler|Electrically insulating non-curing thermal filler,k>=3W/mK,0.1mm installed gaps|1|Collector roots,bridge/shoe laps,shoe/liner spherical interfaces and cap split laps. Fill the specified thin gaps;avoid thick pads. Do not permanently glue removable contact shoes.|
|probe_retention_tape|10mm polyimide electrical-insulation tape,<=0.06mm thick|1|Hold battery NTC over a thin non-curing thermal layer so it can be removed without stripping the cell sleeve. COB and liner probes use insulating thermal adhesive away from solder pads and emitting area.|
|hex_key_1p5|1.5mm hex key with slender shaft<=1.8mm diameter|1|For internal ISO4762 screws. Remove the upper assembly before reaching thermal-contact screws;verify the purchased key against the checked access corridor.|
|female_housing_3|2.54mm1x03 narrow female crimp housing,maximum8.1x3x14mm|1|J8;3matching contacts included in24 loose contacts;0.64mm square mating pins.|
|key_low_profile_sockets|2.54mm1x02 low-profile solder-wire female socket,body<=8.5mm,total depth<=11.5mm|2|采购/线束定制规格已确定：2.54mm1x2焊线母座，壳<=8.5mm、总深<=11.5mm、含热缩截面<=3x5.6mm；不是已经取得厂家认证STEP的特定商品。先让供应商按此规格交样，外形大于包络不得直接代替。|
|controller_wire_guide_print|White ASA open main-loom guide,R3.6 bore,R5 outer,width2mm|1|Internal guide on existing rear motor post;0.2mm peelable adhesive gap to flat post side. Remove before thermal bridge service. No exterior hole or new screw.|
|controller_guide_tie|PA66 cable tie2.5x100mm,temperature rating>=85C|1|Closes new H01 open guide. Release or replace for deep service;do not compress wire insulation.|
|main_harness_assembly|H01-H06 preformed harness assembly and XIAO soldering service|1|Labour only:components/wire/housings separately listed. H07/H08/H09-11/H12 have their own labour rows. Supply routing jig data,individual labels,continuity test and strain relief. Shared Ø6 reserve is not an electrical splice.|

现用六层主板采用双面手工/委托回流装配，空JLC SMT表不代表包焊订单。Pololu3060与M4×90 ISO10642按确切身份询交期；低型窗插座按已给总包络交样，不接受任意大壳替换。铝加工按同版STEP+15页图+中文说明。整机照度、温度、磁吸和风扇仍须首样实测；这些未实测项目不通过采购名称或CAD间隙自动获得合格结论。
