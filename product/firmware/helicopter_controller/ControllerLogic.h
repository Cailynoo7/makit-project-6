#pragma once
#include "ThermalSafety.h"

namespace heli {
struct Inputs {
  bool lightPressed;
  bool fanPressed;
  bool usbPresent;
};
struct Request {
  bool light;
  bool fan;
  uint16_t lightPermille=kLightMaxPermille;
  bool coldStartAllowed=true;
};

class Button {
public:
  void reset(uint32_t now, bool pressed) {
    candidate_ = stable_ = pressed;
    changedAt_ = now;
    armed_ = false;
  }
  bool update(uint32_t now, bool pressed) {
    if (pressed != candidate_) {
      candidate_ = pressed;
      changedAt_ = now;
    }
    if (!elapsed(now, changedAt_, kDebounceMs)) return false;
    const bool wasPressed = stable_;
    stable_ = candidate_;
    if (!stable_) armed_ = true;
    if (!wasPressed && stable_ && armed_) {
      armed_ = false;
      return true;
    }
    return false;
  }
private:
  bool candidate_ = false;
  bool stable_ = false;
  bool armed_ = false;
  uint32_t changedAt_ = 0;
};

class Controller {
public:
  void begin(uint32_t now, Inputs in) {
    bootAt_ = usbLowAt_ = now;
    usbLowTracking_ = !in.usbPresent;
    usbBlocked_ = true;
    fault_ = false;
    requested_ = {false, false};
    lightKey_.reset(now, in.lightPressed);
    fanKey_.reset(now, in.fanPressed);
  }
  Request step(uint32_t now, Inputs in, Safety safety) {
    // A single observed HIGH wins over any button event. LOW must stay stable.
    if (in.usbPresent) {
      usbBlocked_ = true;
      usbLowTracking_ = false;
    } else {
      if (!usbLowTracking_) {
        usbLowTracking_ = true;
        usbLowAt_ = now;
      }
      if (elapsed(now, usbLowAt_, kUsbAbsentStableMs)) usbBlocked_ = false;
    }
    if (fault_ || !safety.allowed || usbBlocked_ || !elapsed(now, bootAt_, kBootGuardMs)) {
      requested_ = {false, false};
      // Held keys and clicks while charging are deliberately not queued.
      lightKey_.reset(now, in.lightPressed);
      fanKey_.reset(now, in.fanPressed);
      return requested_;
    }
    if (lightKey_.update(now, in.lightPressed)) {
      if (requested_.light) requested_.light=false;
      else if (safety.coldStartAllowed) requested_.light=true;
    }
    requested_.lightPermille=safety.lightPermille;
    requested_.coldStartAllowed=safety.coldStartAllowed;
    if (fanKey_.update(now, in.fanPressed)) requested_.fan = !requested_.fan;
    return requested_;
  }
  void latchSoftwareFault() { fault_ = true; requested_ = {false, false}; }
  void cancelLightRequest() { requested_.light=false; }
  bool faulted() const { return fault_; }
 private:
  Button lightKey_, fanKey_;
  uint32_t bootAt_ = 0, usbLowAt_ = 0;
  bool usbLowTracking_ = false, usbBlocked_ = true, fault_ = false;
  Request requested_ = {false, false};
};

// Used by the sketch AND host tests. Only output transitions touch hardware;
// a steady ON request must not reset/retry a hardware-latched motor stall.
template <class Hal> class OutputDriver {
public:
 explicit OutputDriver(Hal &hal):hal_(hal){}
 bool begin(uint32_t now) {
  healthy_=hal_.initialize();
  if(!healthy_ || !hal_.stopFan() || !hal_.stopLight()) return fail();
  fanOn_=false; lightState_=LightState::Off; fanStoppedAt_=lightStoppedAt_=now;
  return true;
 }
 bool apply(uint32_t now,Request req) {
  if(!healthy_) return false;
  if(!req.fan && fanOn_) {
   if(!hal_.stopFan()) return fail();
   fanOn_=false;fanStoppedAt_=now;
  }
  if(!req.light && lightState_!=LightState::Off) {
   if(!hal_.stopLight()) return fail();
   lightState_=LightState::Off;lightStoppedAt_=now;
  }
  // If a temperature limit arrives during50ms full-HIGH startup, abort.
  // Stay OFF until the request is released, even if temperatures fall again.
  if(!req.light) startupAborted_=false;
  if(lightState_==LightState::Starting && !req.coldStartAllowed) {
   if(!hal_.stopLight()) return fail();
   lightState_=LightState::Off;lightStoppedAt_=now;startupAborted_=true;
  }
  if(req.fan && !fanOn_ && elapsed(now,fanStoppedAt_,kDriverResetMs)) {
   if(!hal_.startFan(kFanIn1HighTicks)) return fail();
   fanOn_=true;
  }
  if(req.light && !startupAborted_ && lightState_==LightState::Off &&
     req.coldStartAllowed && req.lightPermille>0 && elapsed(now,lightStoppedAt_,kLightOffMs)) {
   if(!hal_.startLightContinuous()) return fail();
   lightState_=LightState::Starting;lightStartedAt_=now;
  }
  if(lightState_==LightState::Starting && elapsed(now,lightStartedAt_,kLightStartupMs)) {
   lightState_=LightState::Running;lastDuty_=UINT16_MAX;
  }
  if(lightState_==LightState::Running) {
   uint16_t duty=req.lightPermille;
   if(duty>kLightMaxPermille) duty=kLightMaxPermille;
   if(duty==0) {
    if(!hal_.stopLight()) return fail();
    lightState_=LightState::Off;lightStoppedAt_=now;startupAborted_=true;
   } else if(duty!=lastDuty_) {
    if(!hal_.setLightDuty(lightTicks(duty))) return fail();
    lastDuty_=duty;
   }
  }
  return true;
 }
 bool startupAborted()const{return startupAborted_;}
private:
 enum class LightState:uint8_t {Off,Starting,Running};
 bool fail() {
  hal_.emergencyOff();healthy_=false;fanOn_=false;lightState_=LightState::Off;return false;
 }
 Hal &hal_;
 bool healthy_=false,fanOn_=false,startupAborted_=false;
 LightState lightState_=LightState::Off;
 uint32_t fanStoppedAt_=0,lightStoppedAt_=0,lightStartedAt_=0;
 uint16_t lastDuty_=0;
};
} // namespace heli
