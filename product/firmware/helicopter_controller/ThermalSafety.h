#pragma once
#include <math.h>
#include "ControlConfig.h"
namespace heli {
struct Sample {
 float c[3]={0,0,0};
 float batteryV=0;
 uint32_t at=0;
 bool valid=false;
};
inline bool ntcTemperature(int16_t raw,uint8_t channel,float &c) {
 if(channel>=3 || raw<=0) return false;
 const float v=raw*kAdcLsbV;
 if(v<=0.04f || v>=kNtcSupplyV-0.10f) return false; // short/open, conservative rails
 const float r=kNtcPullupOhm*v/(kNtcSupplyV-v);
 c=1.0f/(1.0f/298.15f+logf(r/kNtcR25Ohm)/kNtcBeta)-273.15f+kTempOffsetsC[channel];
 return isfinite(c) && c>=-20 && c<=110;
}
inline bool decodeSample(const int16_t raw[4],uint32_t at,Sample &s) {
 s={}; s.at=at;
 for(uint8_t i=0;i<3;++i) if(!ntcTemperature(raw[i],i,s.c[i])) return false;
 s.batteryV=raw[3]*kAdcLsbV*kBatteryDividerGain;
 s.valid=raw[3]>0 && isfinite(s.batteryV) && s.batteryV>=2.0f && s.batteryV<=4.5f;
 return s.valid;
}
enum class Fault:uint8_t { Waiting, None, Adc, Sensor, Stale, Temperature, LowBattery, HighBattery, ColdBattery };
struct Safety {
 bool allowed=false;
 bool coldStartAllowed=false;
 uint16_t lightPermille=0;
 Fault fault=Fault::Waiting;
};
class ThermalSafety {
public:
 Safety step(uint32_t now,const Sample &s,bool adcHealthy) {
  Fault reason=Fault::None;
  if(!adcHealthy) reason=Fault::Adc;
  else if(!s.valid) reason=Fault::Sensor;
  else if(elapsed(now,s.at,kSampleStaleMs)) reason=Fault::Stale;
  else if(s.batteryV<kBatteryLowV) reason=Fault::LowBattery;
  else if(s.batteryV>kBatteryHighV) reason=Fault::HighBattery;
  else if(s.c[2]<kBatteryColdC) reason=Fault::ColdBattery;
  else for(uint8_t i=0;i<3;++i) {
   if(!isfinite(s.c[i]) || s.c[i]<-20 || s.c[i]>110) {reason=Fault::Sensor;break;}
   if(s.c[i]>=kTripC[i]) {reason=Fault::Temperature;break;}
  }
  if(!isfinite(s.batteryV)) reason=Fault::Sensor;
  if(reason!=Fault::None) {
   blocked_=true; tracking_=false; lastFault_=reason;
   return {false,false,0,reason};
  }
  if(blocked_) {
   bool recover=s.batteryV>=kBatteryRecoverV && s.batteryV<=kBatteryRecoverHighV
      && s.c[2]>=kBatteryRecoverColdC;
   for(uint8_t i=0;i<3;++i) recover=recover && s.c[i]<=kRecoverC[i];
   if(!recover) {tracking_=false;return {false,false,0,lastFault_};}
   if(!tracking_) {tracking_=true;recoverAt_=now;}
   if(!elapsed(now,recoverAt_,kRecoveryMs)) return {false,false,0,lastFault_};
   blocked_=false; lastFault_=Fault::None;
  }
  uint16_t limit=kLightMaxPermille;
  bool cold=true;
  for(uint8_t i=0;i<3;++i) {
   if(s.c[i]>=kDimC[i]) {
    cold=false;
    const float fraction=(s.c[i]-kDimC[i])/(kTripC[i]-kDimC[i]);
    const auto scaled=static_cast<uint16_t>(kLightMaxPermille*
                (1.0f-fraction*(1000-kMinimumThermalPermille)/1000.0f));
    if(scaled<limit) limit=scaled;
   }
  }
  return {true,cold,limit,Fault::None};
 }
private:
 bool blocked_=true,tracking_=false;
 uint32_t recoverAt_=0;
 Fault lastFault_=Fault::Waiting;
};
}
