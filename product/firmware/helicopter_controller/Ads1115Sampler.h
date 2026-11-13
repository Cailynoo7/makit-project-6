#pragma once
#include "ThermalSafety.h"
namespace heli {
// Transport must implement readRegister(reg,value), writeRegister(reg,value).
// ADS1115 Rev.E tables8-1/8-3: OS=1, MUX=4+channel, PGA=1,
// MODE=1, DR=4(128SPS), comparator disabled. No blocking conversion wait.
inline uint16_t adsConfig(uint8_t channel) {
 return static_cast<uint16_t>(0x8383U | ((4U+channel)<<12));
}
template<class Bus> class Ads1115Sampler {
public:
 explicit Ads1115Sampler(Bus &bus):bus_(bus){}
 void begin(uint32_t now) { lastScan_=now-kScanPeriodMs; healthy_=false; waiting_=false; retrying_=false;sample_={}; }
 void poll(uint32_t now) {
  if(!waiting_) {
   if(retrying_ && !elapsed(now,failedAt_,kAdcRetryMs)) return;
   if(!elapsed(now,lastScan_,kScanPeriodMs)) return;
   lastScan_=now;channel_=0;
   start(now);return;
  }
  if(elapsed(now,startedAt_,kConversionTimeoutMs)) { fail(now);return; }
  if(!elapsed(now,startedAt_,kConversionWaitMs)) return;
  uint16_t config;
  if(!bus_.readRegister(1,config) ||
     (config&0x7FFF)!=(adsConfig(channel_)&0x7FFF)) {fail(now);return;}
  if(!(config&0x8000)) return; // bounded by20ms timeout.
  uint16_t value;
  if(!bus_.readRegister(0,value)) {fail(now);return;}
  raw_[channel_]=static_cast<int16_t>(value);
  // Reject a dangerous channel before waiting for the remaining channels.
  if(channel_<3) {
   float t;
   if(!ntcTemperature(raw_[channel_],channel_,t) || t>=kTripC[channel_] ||
      (channel_==2 && t<kBatteryColdC)) {fail(now);return;}
  }
  ++channel_;
  if(channel_<4) {start(now);return;}
  waiting_=false;
  if(!decodeSample(raw_,now,sample_)) {fail(now);return;}
  healthy_=true;retrying_=false;
 }
 const Sample &sample()const{return sample_;}
 bool healthy()const{return healthy_;}
private:
 void start(uint32_t now) {
  if(!bus_.writeRegister(1,adsConfig(channel_))) {fail(now);return;}
  startedAt_=now; waiting_=true;
 }
 void fail(uint32_t now) {
  healthy_=false;waiting_=false;retrying_=true;failedAt_=now;sample_.valid=false;
 }
 Bus &bus_;
 Sample sample_;
 int16_t raw_[4]={};
 uint32_t lastScan_=0, startedAt_=0, failedAt_=0;
 uint8_t channel_=0;
 bool healthy_=false,waiting_=false,retrying_=false;
};
}
