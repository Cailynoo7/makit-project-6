# 新版连接板接线

连接板顶面为内部检修侧，以板上J编号和方形1脚为准；底视图左右镜像，不能据屏幕左右猜极性。电芯先接保护板J2，XIAO及负载接保护后的PACK侧。

|连接板接口|顺序及作用|
|---|---|
|J1 7P|1灯键、2风扇键、3反相风扇PWM、4灯EN、5 USB检测、6 VBUS检测电源、7 PACK GND|
|J2 2P|1裸电芯正极CELL_P、2裸电芯负极CELL_N|
|J12 2P|1保护后PACK正极VBAT、2保护后PACK GND；到XIAO电池焊盘|
|J3 2P|1 MOTOR_A、2 MOTOR_B；到Pololu3060|
|J4 2P|1 COB正极LED_PLUS、2 COB负极LED_FB；负极不是GND|
|J5/J6 2P|1按键信号、2 PACK GND；分别接灯/风扇窗内小板|
|J7 2P|1风扇使能D5/GPIO7、2 PACK GND|
|J8 3P|1 3V3、2 SDA(D7/GPIO20)、3 SCL(D6/GPIO21)|
|J9/J10/J11 2P|1 NTC采样、2 PACK GND；分别是COB、壳体、电芯探头|

## 逐线接线

|起点|终点|说明|
|---|---|---|
|XIAO.D1|PCB.J1.1|26AWG wire harness|
|XIAO.D2|PCB.J1.2|26AWG wire harness|
|XIAO.D3|PCB.J1.3|GPIO5, inverse20kHz PWM: IN1 high during brake portion; motor ON fraction=1-PWM_high_fraction, initial0.60; IN2 supplied separately by D5.|
|XIAO.D4|PCB.J1.4|GPIO6 -> TPS61500ENvia100ohm;DIMC1uFselectsanalogdimming.Normalfullcurrent267mA,5kHzfordimming.StartcontinuousHIGH50ms,OFFLOW>=10ms;USB/temperaturefaultoverrides.|
|XIAO.D10|PCB.J1.5|26AWG; VBUS divider top100k/bottom150k; GPIO10 digital INPUT, no pull resistor; nominal3.0V at5V USB|
|XIAO.VBUS|PCB.J1.6|26AWG wire harness; sense only|
|XIAO.GND|PCB.J1.7|24AWG wire harness|
|PCB.J3.1|MOTOR.terminal_A|24AWG; H-bridge output OUT1; during reverse/slow-decay PWM OUT2 is positive. Bench-verify CCW from above/downward air; swap motor leads if needed. Neither lead is fixed ground.|
|PCB.J3.2|MOTOR.terminal_B|24AWG; H-bridge output OUT2; during reverse/slow-decay PWM OUT2 is positive. Bench-verify CCW from above/downward air; swap motor leads if needed. Neither lead is fixed ground.|
|PCB.J4.1|LED.+|26AWGCOBpolarity;boosted14-18Vnominal,OVP19.65-21.67V;LEDnegativeisFBsense,NOTground. No hot-plugging.|
|PCB.J4.2|LED.-|26AWGCOBpolarity;boosted14-18Vnominal,OVP19.65-21.67V;LEDnegativeisFBsense,NOTground. No hot-plugging.|
|PCB.J5.1|SW_L.J1.1|26AWG left button harness; connect daughterboard J1, NOT bare switch leg numbers|
|PCB.J5.2|SW_L.J1.2|26AWG left button harness; connect daughterboard J1, NOT bare switch leg numbers|
|PCB.J6.1|SW_R.J1.1|26AWG right button harness; connect daughterboard J1, NOT bare switch leg numbers|
|PCB.J6.2|SW_R.J1.2|26AWG right button harness; connect daughterboard J1, NOT bare switch leg numbers|
|XIAO.D5|PCB.J7.1|GPIO7; driver IN2 enable, with IN1 inverse20kHz PWM for slow-decay drive/brake. OFF requires both low >=10ms.|
|XIAO.GND|PCB.J7.2|Paired26AWG enable/ground harness.|
|BAT.+|PCB.J2.1|RAWcellonly;24AWG,doNOTbranchrawcellnegativetoXIAOorGND.|
|BAT.-|PCB.J2.2|RAWcellonly;24AWG,doNOTbranchrawcellnegativetoXIAOorGND.|
|XIAO.BAT+|PCB.J12.1|ProtectedPACKoutputonly;24AWG;allUSB/XIAOgroundsarePACK-side.|
|XIAO.BAT-|PCB.J12.2|ProtectedPACKoutputonly;24AWG;allUSB/XIAOgroundsarePACK-side.|
|XIAO.3V3|PCB.J8.1|InternalADCinterface3V3/SDA20/SCL21;explicitWire.begin(20,21),100kHz;GPIO6/7alreadydriveLED/fan.|
|XIAO.D7|PCB.J8.2|InternalADCinterface3V3/SDA20/SCL21;explicitWire.begin(20,21),100kHz;GPIO6/7alreadydriveLED/fan.|
|XIAO.D6|PCB.J8.3|InternalADCinterface3V3/SDA20/SCL21;explicitWire.begin(20,21),100kHz;GPIO6/7alreadydriveLED/fan.|
|NTC_LED.1|PCB.J9.1|Probe10k/B3950;pin1NTCnode,pin2PACK_GND;labelbylocation,notpolarized.|
|NTC_LED.2|PCB.J9.2|Probe10k/B3950;pin1NTCnode,pin2PACK_GND;labelbylocation,notpolarized.|
|NTC_SHELL.1|PCB.J10.1|Probe10k/B3950;pin1NTCnode,pin2PACK_GND;labelbylocation,notpolarized.|
|NTC_SHELL.2|PCB.J10.2|Probe10k/B3950;pin1NTCnode,pin2PACK_GND;labelbylocation,notpolarized.|
|NTC_BAT.1|PCB.J11.1|Probe10k/B3950;pin1NTCnode,pin2PACK_GND;labelbylocation,notpolarized.|
|NTC_BAT.2|PCB.J11.2|Probe10k/B3950;pin1NTCnode,pin2PACK_GND;labelbylocation,notpolarized.|

## 电源与安装

裸18650只接J2两脚，不再有电芯到XIAO的Y分支。XIAO BAT+/-接J12，XIAO其余GND与按钮/传感器全部为PACK GND；不能把电芯负极与这些地线直接并在一起绕过保护。电机、灯源不由XIAO的3V3稳压器供电，J1.6 VBUS只供检测。

电池供电和电机线用24AWG铜软线；信号用26AWG。主电源接插件及触点额定至少3A，电芯由供应商点焊引线，不能直接焊电芯。区分并标记RAW-、PACK-和LED_FB，COB光腔段用外径≤1.1mm白色绝缘线，两端分别红色LED+、黄色LED_FB标签，避免把LED回路误作地线。三只NTC无极性，但必须贴上COB/SHELL/BAT标签防止换位。I²C使用3.3V、100kHz、0x48，禁止上拉5V。

COB探头贴金属基板热点，壳体探头贴预计最热的内壁并校准内外温差，电池探头贴电芯筒身、与集热件隔开；绝缘导热胶不得覆盖发光面、电池泄压结构或电极。与热件和旋转件留线束间隙，按内部结构更新后再确定绑扎点。

## 程序配套状态

先读取三路温度和电池电压并通过合理性检查，才能允许用户按键启动。ADS1115 AIN0/1/2对应COB/壳体/电芯，AIN3为100k/100k分压，满电4.2V对应ADC约2.1V。10k上拉/10k B3950 NTC在25℃约1.65V；开路接近3.3V、短路接近0V应判故障。

程序已适配TPS61500连续高50ms启动/5kHz调光、ADS1115四通道及三只NTC；独立按键、USB负载关闭和DRV8213反相20kHz保持。温度减光/关闭为COB60/70℃、壳体43/48℃、电芯40/45℃；ADC/探头异常、过期数据及电池低于3.3V关闭两路。恢复回差和5秒稳定期后仍须重新按键，详见固件说明。当前源码已通过主机测试和真实目标编译，未烧录测波形。这些探头不能切断XIAO原充电器，充电环境及温升仍需符合电芯0–45℃要求。

接线引脚的来源和每根线的供应商证据保留在结构化接线表中，XIAO数字脚映射采用Espressif官方XIAO_ESP32C3变体定义及Seeed官方针脚图。裸板制板已通过，不等于带电原型、散热或新内部结构已通过验收。


## 完整线束与插接

现版完整路由、毛坯线长、固定点及释放顺序见产品线束装配与裁线表和harness-routing记录。J1是H01，J2为H02，依次J3至J12对应H03–H12；H07/H08只是汇入主束的短分支，不能按10mm模型支段裁整根线。主束外包络Ø6，已有R6检修半圆。12根线分别落到XIAO焊盘，不在汇合位置电气并接。RAW-/PACK-/LED_FB严格区分。

普通主板母壳总高≤14mm：2P≤5.6×3、7P≤3×18.3、3P≤8.1×3mm。窗端为低型1×2焊线母座，壳≤8.5、含焊线热缩总深≤11.5、截面≤3×5.6mm。三只NTC用TE1375820-2壳与1375819-1触点；使用26AWG、外径0.89–1.4mm转接线，未知原探头线径不能直接压接。接头错开≥8mm，单处外径≤1.8mm，合拢≤3.4mm。COB/SHELL/BAT探头到插壳总毛坯分别125/80/105mm（含头与插壳），按工装修线。

J10经R4桥侧开放槽和后侧短路径到壳体探头，软绑在+Y电机柱旁；J11经下导向到电芯探头。检修先断USB/J2、拆上部/解除皮带、解开扎带及贴带，将已拔主板端支线停到尾侧/底口外。J9先+Z6.3、+X5、+Z12，其余主板插壳+Z12；主板托架移出后才拔窗端，向中心6.3再上提12mm。夹插壳，不拉线。

程序、引脚和供应商证据未改；结构化接线只追加路由标签。12主板插壳和2窗端插座按0.5mm步长BRep检查无相交，仍不替代实物插合、端子拉力与打印公差测试。
