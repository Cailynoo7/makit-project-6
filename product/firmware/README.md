# 直升机灯扇控制程序

适用：Seeed XIAO ESP32C3、当前连接板a775a125f18a8423be0a2ba88a937e442a0c12100c13393ab9c8c7c26812f82e、DRV8213、TPS61500、HL-LM002H384W-5B2C5(Ra2)(ANSI-4000K) COB、ADS1115和三只HNTC-103F3950FB-100P。程序替代旧MEL7135原型，保持外观和现行接线。五个源文件必须放在同一helicopter_controller文件夹内；不依赖第三方库，Wire为Arduino核心自带。

## 操作

- 左灯泡键控制灯，右风扇键控制风扇；低电平按下、25ms去抖，短按切换，长按不连发。
- 上电关闭两路。温度、电压采样连续正常且满足恢复范围5秒后才接受按键；上电按住的键需先松开。
- USB检测为高立即关闭两路，拔线连续稳定500ms后仍关闭，重新按键启动。USB输入RC约6ms，I²C调用也有超时，不能理解成插头物理接触瞬间的零延迟关断。
- 任一硬温限、探头异常、ADC通信/配置/转换超时、数据陈旧或电池电压异常关闭两路，清除开机请求。条件恢复并稳定5秒后仍须松键再重新按键。
- PWM/GPIO初始化或输出API失败锁存关闭，重启后才重新初始化。不会循环重置DRV8213的硬件堵转锁存；须先按键关、再开。nFAULT/nSTALL没有接入MCU，程序不能报告堵转或测电机电流。

## 接线与波形

|作用|XIAO/GPIO|连接板|
|---|---|---|
|灯键|D1/3|J1.1|
|风扇键|D2/4|J1.2|
|风扇IN1|D3/5|J1.3|
|TPS61500 EN|D4/6|J1.4|
|USB检测|D10/10|J1.5，INPUT，不启用内部上拉/下拉|
|风扇IN2|D5/7|J7.1|
|ADC供电|3V3|J8.1|
|SDA|D7/20|J8.2|
|SCL|D6/21|J8.3|

显式Wire.begin(20,21,100000)，地址0x48。禁止默认GPIO6/7总线、5V上拉或同时启动使用GPIO20/21的UART。

风扇：20kHz、10位计数。运行IN2=1，IN1高410/1024、低614/1024，即约60%驱动、40%低侧制动；启动先升IN2，再更新IN1。关闭先停IN1为低，再拉低IN2；两输入低至少10ms才允许再启。电机接线须使旋翼从上方看逆时针，换向只能断电互换电机线。首周期瞬态、电机绕组RMS电流≤0.375A及实际风量仍须实测。

灯：DIMC=1µF，使用EN输入进行模拟调光；5kHz、10位计数，与风扇用独立LEDC定时器。每次启动先连续高至少50ms，随后按温限设置占空比；100%用连续高，降功率时才输出5kHz波形。关断保持EN低至少10ms。启动等待不阻塞按键、USB及ADC检查；若50ms启动段已进入降额区，立即中止并清除本次灯请求。温度已在降额区时不允许重新启动灯，防止每次重试再次注入满电流；风扇仍可独立操作。

冷机上限默认100%：由0.75Ω采样电阻限定约266.7mA，器差预算257–276mA；不是GPIO直接给COB供电，也不是3A LED电流。全功率约4W是电路工作点，不能据此认定现有外壳可持续散热或已达到500lx。可在ControlConfig.h降低kLightMaxPermille做首样限功率；启动段仍为受硬件恒流限制的50ms连续高，首次测试应使用限流电源并监测COB。

## 测温与保护

ADS1115 AIN0=J9 COB、AIN1=J10壳体、AIN2=J11电芯、AIN3=电池100k/100k分压。单端、±4.096V量程、125µV/LSB、128SPS、单次转换，比较器关闭。配置字依次C383/D383/E383/F383；逐次读取配置回验及OS就绪位，不能把上一通道结果当新通道。每100ms开始一轮，正常约36ms完成；9ms后轮询，单次20ms未完成判故障。每个温度通道一读到开短路或硬超温便禁止负载，无须等其余通道。

I²C每次调用超时5ms；通信失败立即使旧结果失效，250ms后仅重试采集，不重启负载。最后完整数据年龄≥250ms关断。主循环在采集前后均检查USB及输出，不使用阻塞式等待转换。通信超时、转换故障及高温通道提前中止统一禁止负载；这些诊断不是硬件故障引脚。

10kΩ上拉、10kΩ@25℃、B3950公式换算；默认NTC电源3.300V、温度偏移0、电池分压增益2.000。电压≤0.04V或≥3.20V、负码、非有限值、换算超出−20至110℃判异常。25℃应约1.65V、码13200；满电4.2V的电池通道约2.1V、码16800。未加软件平滑延迟硬关断。

|探头|开始减光|关闭两路|故障恢复上限|
|---|---:|---:|---:|
|COB|60℃|70℃|55℃|
|壳体|43℃|48℃|40℃|
|电芯|40℃|45℃|37℃|

软降额为线性：从正常上限降至该上限的25%，达到硬关断值后完全关闭；三路取最小值。风扇保持原60%驱动，不用升速补偿未知风路。高温下降后允许已运行灯的功率恢复；硬故障后的负载不会自动恢复。

工程默认：电池<3.3V、>4.30V或电芯<0℃也关闭两路；恢复需电池3.5–4.25V、电芯≥5℃，且全部温度低于表中恢复上限，连续5秒。阈值是未校准样机的保守默认，不能替代电芯硬件保护。初次上电也执行这些恢复条件；电芯环境过冷/过热时不能启动。

**本程序只能关闭灯和风扇，不能停止XIAO原板充电器。** USB充电期间即使探头温度超限也无软件断充路径，必须满足电芯0–45℃充电条件并实测充电温升。若需要自动温控断充，须另改充电硬件。

## 编译与烧录

Arduino-ESP32固定3.3.12，FQBN esp32:esp32:XIAO_ESP32C3。程序编译时静态检查D1/D2/D3/D4/D5/D6/D7/D10映射，不使用网络栈或保存上次开启状态。

```sh
arduino-cli core update-index --additional-urls https://espressif.github.io/arduino-esp32/package_esp32_index.json
arduino-cli core install esp32:esp32@3.3.12 --additional-urls https://espressif.github.io/arduino-esp32/package_esp32_index.json
arduino-cli compile --fqbn esp32:esp32:XIAO_ESP32C3 --warnings all product/firmware/helicopter_controller
```

按Seeed官方入门指南，在Arduino IDE添加ESP32软件包地址并安装3.3.12；打开helicopter_controller.ino，选择Tools → Board → esp32 → XIAO_ESP32C3、Tools → Port，再Upload。如端口不识别，按住BOOT接USB，再松开重试。板上必须是本项目新版连接板，不能搭配旧MEL7135板。烧录用USB时负载保持关闭；拔掉USB、使用电池、等待采样恢复，再重新按键。不要通过删去USB互锁来测试。

Makit没有烧录控件；可右击Product页签 → Show in Finder，找到firmware内的程序和说明，用Arduino IDE打开。

## 首样实验包

完整接法、仪器、逐步预期和停测条件见 [首样通电与温度校准](commissioning/首样通电与温度校准.md)。配套含待填写的测试/校准CSV、21个名义电阻测试点，以及读取正式配置的离线换算工具；记录表为空白，不代表实测通过。当前程序没有串口读数，流程采用被动I²C监听，不修改正式程序或占用GPIO20/21的UART。

先做功率级隔离的逻辑测试，再接散热完整的COB；正式100%EN为持续高，只有降额时才有5kHz波形。工具可生成仅修改灯上限为500的测试副本以观察50ms启动边界，正式源码不变，结束必须恢复正式配置。

## 已验证及首样检查

2026-11-13：35组主机测试、11329次断言通过，启用AddressSanitizer及UndefinedBehaviorSanitizer。生产控制器、输出时序和ADC寄存器采集状态机共同测试；覆盖独立按键、USB、恢复需重按、各温度阈值、NTC开短路、ADC NACK/配置错误/忙超时、数据过期、低压/过压/低温、50ms启动、10ms关闭、millis回绕及HAL错误。

Arduino CLI1.6.0、Arduino-ESP32 3.3.12真实XIAO_ESP32C3目标编译通过，全部警告开启且未输出警告。程序314386字节，静态RAM14312字节。验证记录包含源码哈希；未烧录或连接实物，模拟结果不等于实物波形。

```sh
clang++ -std=c++17 -Wall -Wextra -Werror -fsanitize=address,undefined product/firmware/tests/controller_tests.cpp -o /tmp/helicopter-controller-tests
/tmp/helicopter-controller-tests
```

首样先不装旋翼：
1. 接妥三只探头，万用表校准3V3、电池读数；用已知10k电阻替代每只NTC应读25℃，逐路开路/短路应关闭负载。再以电阻箱模拟表内温限及电池3.3V边界，验证冷却和拔USB均不自动复开。
2. 示波器测EN连续高≥50ms、随后5kHz，风扇IN1=20kHz/高约40%、IN2使能和关闭顺序；在启动途中插USB、拔ADC、断探头，确认两路实际停止。核对关断后至少10ms低电平。
3. 把探头贴到已确认位置，校准COB边缘探头对Ts、壳内探头对最热外壳的差值；珠头热滞后及粘接脱落无法由软件完全检测。温度阈值需结合热电偶测试修订。
4. 完成铝件后测试封壳单灯/灯扇连续运行、照度分布及温升；若温控降额后不足500lx，应改热路/光学或运行功率，不放宽既定读写目标。程序未测温升、亮度、充电控制、风量或旋翼平衡。

## 原始依据

- [Seeed XIAO ESP32C3入门和烧录](https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/)。
- [Espressif XIAO引脚变体3.3.12](https://github.com/espressif/arduino-esp32/blob/3.3.12/variants/XIAO_ESP32C3/pins_arduino.h)。
- [TI TPS61500手册第11页](https://www.ti.com/lit/ds/symlink/tps61500.pdf)：DIMC电容、5kHz/1µF、最小启动200µs；本项目沿用50ms连续启动工程余量。
- [TI ADS1115 Rev.E第24–26页](https://www.ti.com/lit/ds/symlink/ads1115.pdf)：寄存器、量程、OS/MUX、128SPS。
- [Espressif Wire超时与总线API](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/i2c.html)。
- 项目HNTC-103F3950FB-100P供应商手册第1/3页、现行连接板逐线表：10k/B3950、探头与分压接线。安装校准、恢复回差和额外低温/过压保护为source=default工程配置。
