// Target: Seeed XIAO ESP32C3; Arduino-ESP32 3.3.12.
// No network stack, third-party library, flash-persisted ON state or auto-retry.
#include <Arduino.h>
#include <Wire.h>
#include "Ads1115Sampler.h"
#include <driver/gpio.h>
#include <driver/ledc.h>
#include "ControllerLogic.h"

#if !defined(CONFIG_IDF_TARGET_ESP32C3)
#error "Select XIAO_ESP32C3; this sketch is for ESP32-C3 only."
#endif
static_assert(D1 == heli::kLightKeyGpio && D2 == heli::kFanKeyGpio &&
              D3 == heli::kFanIn1Gpio && D4 == heli::kLightGpio &&
              D5 == heli::kFanIn2Gpio && D10 == heli::kUsbSenseGpio &&
              D7 == heli::kSdaGpio && D6 == heli::kSclGpio,
              "Selected Arduino board does not match the verified XIAO pin map");

class Esp32Hardware {
public:
  bool initialize() {
    // Existing external pulldowns keep fan inputs and TPS61500 EN low at reset.
    // Establish safe GPIO latches before connecting any PWM peripheral.
    const uint8_t safePins[] = {heli::kFanIn1Gpio, heli::kFanIn2Gpio, heli::kLightGpio};
    for (auto pin : safePins) {
      if (!outputLow(pin)) return false;
    }
    pinMode(heli::kLightKeyGpio, INPUT_PULLUP);
    pinMode(heli::kFanKeyGpio, INPUT_PULLUP);
    pinMode(heli::kUsbSenseGpio, INPUT); // Existing100k/150k divider; NO pull.

    if (!timer(LEDC_TIMER_0, heli::kFanPwmHz) ||
        !timer(LEDC_TIMER_1, heli::kLightPwmHz)) return false;
    if (!channel(LEDC_CHANNEL_0, LEDC_TIMER_0, heli::kFanIn1Gpio)) return false;
    fanConfigured_ = true;
    if (!channel(LEDC_CHANNEL_1, LEDC_TIMER_1, heli::kLightGpio)) return false;
    lightConfigured_ = true;
    return ledc_get_freq(LEDC_LOW_SPEED_MODE, LEDC_TIMER_0) == heli::kFanPwmHz &&
           ledc_get_freq(LEDC_LOW_SPEED_MODE, LEDC_TIMER_1) == heli::kLightPwmHz;
  }
  bool startFan(uint32_t in1HighTicks) {
    // From OFF(0,0), IN2 rises first: any first-cycle transient drives in the
    // intended direction and remains subject to the hardware current limit.
    if (gpio_set_level(gpio(heli::kFanIn2Gpio), 1) != ESP_OK) return false;
    return ledc_set_duty_and_update(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0,
                                    in1HighTicks, 0) == ESP_OK;
  }
  bool stopFan() {
    // Stop the IN1 waveform at LOW before lowering IN2. Merely lowering IN2
    // while PWM continues would drive the motor in the opposite direction.
    const bool stopped = !fanConfigured_ ||
        ledc_stop(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, 0) == ESP_OK;
    const bool disabled = gpio_set_level(gpio(heli::kFanIn2Gpio), 0) == ESP_OK;
    return stopped && disabled;
  }
  bool startLightContinuous() {
    return ledc_stop(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_1, 1) == ESP_OK;
  }
  bool setLightDuty(uint32_t highTicks) {
    // Avoid relying on a PWM full-scale endpoint for true continuous HIGH.
    if(highTicks >= heli::kPwmPeriodTicks) return startLightContinuous();
    return ledc_set_duty_and_update(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_1,
                                    highTicks, 0) == ESP_OK;
  }
  bool stopLight() {
    return !lightConfigured_ ||
        ledc_stop(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_1, 0) == ESP_OK;
  }
  void emergencyOff() {
    stopFan();
    stopLight();
    // A PWM/GPIO API error latches software OFF until reset. Disconnect PWM
    // routing as a final fallback, rather than retrying the load in a loop.
    outputLow(heli::kFanIn1Gpio);
    outputLow(heli::kFanIn2Gpio);
    outputLow(heli::kLightGpio);
    fanConfigured_ = lightConfigured_ = false;
  }
private:
  static gpio_num_t gpio(uint8_t pin) { return static_cast<gpio_num_t>(pin); }
  static bool outputLow(uint8_t pin) {
    // gpio_reset_pin() enables a default pull-up. Avoid that transient on
    // IN1: with IN2 low, a high IN1 would command the opposite direction.
    if (gpio_set_level(gpio(pin), 0) != ESP_OK) return false;
    gpio_config_t cfg = {};
    cfg.pin_bit_mask = 1ULL << pin;
    cfg.mode = GPIO_MODE_OUTPUT;
    cfg.pull_up_en = GPIO_PULLUP_DISABLE;
    cfg.pull_down_en = GPIO_PULLDOWN_DISABLE;
    cfg.intr_type = GPIO_INTR_DISABLE;
    return gpio_config(&cfg) == ESP_OK;
  }
  static bool timer(ledc_timer_t id, uint32_t hz) {
    ledc_timer_config_t cfg = {};
    cfg.speed_mode = LEDC_LOW_SPEED_MODE;
    cfg.timer_num = id;
    cfg.duty_resolution = LEDC_TIMER_10_BIT;
    cfg.freq_hz = hz;
    cfg.clk_cfg = LEDC_USE_XTAL_CLK; // Same40MHz source for both C3 timers.
    return ledc_timer_config(&cfg) == ESP_OK;
  }
  static bool channel(ledc_channel_t id, ledc_timer_t timerId, uint8_t pin) {
    ledc_channel_config_t cfg = {};
    cfg.gpio_num = pin;
    cfg.speed_mode = LEDC_LOW_SPEED_MODE;
    cfg.channel = id;
    cfg.intr_type = LEDC_INTR_DISABLE;
    cfg.timer_sel = timerId;
    cfg.duty = 0;
    cfg.hpoint = 0;
    return ledc_channel_config(&cfg) == ESP_OK;
  }
  bool fanConfigured_ = false, lightConfigured_ = false;
};

class AdsWireBus {
public:
 bool writeRegister(uint8_t reg,uint16_t value) {
  Wire.beginTransmission(heli::kAdsAddress);
  if(Wire.write(reg)!=1 || Wire.write(static_cast<uint8_t>(value>>8))!=1 ||
     Wire.write(static_cast<uint8_t>(value))!=1) return false;
  return Wire.endTransmission(true)==0;
 }
 bool readRegister(uint8_t reg,uint16_t &value) {
  Wire.beginTransmission(heli::kAdsAddress);
  if(Wire.write(reg)!=1 || Wire.endTransmission(false)!=0) return false;
  if(Wire.requestFrom(heli::kAdsAddress,static_cast<size_t>(2),true)!=2) return false;
  const int hi=Wire.read(),lo=Wire.read();
  if(hi<0 || lo<0) return false;
  value=static_cast<uint16_t>((hi<<8)|lo);
  return true;
 }
};
Esp32Hardware hardware;
heli::OutputDriver<Esp32Hardware> outputs(hardware);
heli::Controller controller;
heli::ThermalSafety thermal;
AdsWireBus adcBus;
heli::Ads1115Sampler<AdsWireBus> adc(adcBus);

heli::Inputs readInputs() {
 return {digitalRead(heli::kLightKeyGpio)==LOW,
         digitalRead(heli::kFanKeyGpio)==LOW,
         digitalRead(heli::kUsbSenseGpio)==HIGH};
}
void setup() {
 const bool ready=outputs.begin(millis());
 controller.begin(millis(),readInputs());
 if(!ready) controller.latchSoftwareFault();
 const bool busReady=Wire.begin(heli::kSdaGpio,heli::kSclGpio,heli::kI2cHz);
 Wire.setTimeOut(heli::kI2cTimeoutMs);
 adc.begin(millis());
 if(!busReady) controller.latchSoftwareFault();
 // No Serial/UART: GPIO20/21 are explicitly reassigned to the ADC I2C bus.
}
void updateControls() {
 const uint32_t now=millis();
 const auto wanted=controller.step(now,readInputs(),
                   thermal.step(now,adc.sample(),adc.healthy()));
 if(!outputs.apply(now,wanted)) controller.latchSoftwareFault();
 if(outputs.startupAborted()) controller.cancelLightRequest();
}
void loop() {
 updateControls(); // Observe USB and turn loads off before doing I2C work.
 adc.poll(millis()); // Single-shot state machine; never wait for a conversion.
 updateControls(); // Recheck USB, time and sensor errors after bounded I2C calls.
 delay(1);
}
