#pragma once
#include <stdint.h>
namespace heli {
constexpr uint8_t kLightKeyGpio=3, kFanKeyGpio=4, kFanIn1Gpio=5;
constexpr uint8_t kLightGpio=6, kFanIn2Gpio=7, kUsbSenseGpio=10;
constexpr uint8_t kSdaGpio=20, kSclGpio=21, kAdsAddress=0x48;
constexpr uint32_t kI2cHz=100000, kI2cTimeoutMs=5;
constexpr uint32_t kDebounceMs=25, kBootGuardMs=250, kUsbAbsentStableMs=500;
constexpr uint32_t kDriverResetMs=10, kLightOffMs=10, kLightStartupMs=50;
constexpr uint32_t kFanPwmHz=20000, kLightPwmHz=5000;
constexpr uint8_t kPwmBits=10;
constexpr uint32_t kPwmPeriodTicks=1U<<kPwmBits;
constexpr uint16_t kFanDrivePermille=600, kLightMaxPermille=1000;
constexpr uint32_t kFanIn1HighTicks=((1000U-kFanDrivePermille)*kPwmPeriodTicks+500)/1000;
constexpr uint32_t kScanPeriodMs=100, kConversionWaitMs=9, kConversionTimeoutMs=20;
constexpr uint32_t kAdcRetryMs=250, kSampleStaleMs=250, kRecoveryMs=5000;
constexpr float kAdcLsbV=0.000125f; // PGA +/-4.096V, signed16-bit.
constexpr float kNtcSupplyV=3.3f, kNtcPullupOhm=10000, kNtcR25Ohm=10000, kNtcBeta=3950;
constexpr float kTempOffsetsC[3]={0,0,0}; // Calibrate installed probes, not just ADC.
constexpr float kBatteryDividerGain=2.0f; // R26/R27=100k/100k; calibrate actual divider.
constexpr float kDimC[3]={60,43,40}, kTripC[3]={70,48,45};
constexpr float kRecoverC[3]={55,40,37};
constexpr float kBatteryLowV=3.3f, kBatteryRecoverV=3.5f;
constexpr float kBatteryHighV=4.30f, kBatteryRecoverHighV=4.25f;
constexpr float kBatteryColdC=0, kBatteryRecoverColdC=5; // Conservative discharge default.
constexpr uint16_t kMinimumThermalPermille=250;
static_assert(kFanIn1HighTicks==410 && kFanDrivePermille<=600,"Revalidate motor load before raising drive");
static_assert(kLightMaxPermille>0 && kLightMaxPermille<=1000,"Invalid light maximum");
inline bool elapsed(uint32_t now,uint32_t since,uint32_t interval) {
 return static_cast<uint32_t>(now-since)>=interval;
}
inline uint32_t lightTicks(uint16_t permille) {
 return (static_cast<uint32_t>(permille)*kPwmPeriodTicks+500)/1000;
}
}
