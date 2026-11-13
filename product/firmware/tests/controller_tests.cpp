#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include "../helicopter_controller/Ads1115Sampler.h"
#include "../helicopter_controller/ControllerLogic.h"

static int assertions = 0, scenarios = 0;
#define CHECK(x) do { ++assertions; if (!(x)) { \
  fprintf(stderr, "FAIL line %d: %s\n", __LINE__, #x); exit(1); } } while (0)

struct FakeHal {
  bool fan = false, light = false;
  bool initOk = true, fanStartOk = true, lightStartOk = true, fanStopOk = true;
  int starts = 0, stops = 0, emergencies = 0;
  uint32_t in1High = 0, lightHigh = 0;
  std::vector<std::string> calls;
  bool initialize() { calls.push_back("initialize"); return initOk; }
  bool stopFan() { calls.push_back("fanOff"); fan = false; ++stops; return fanStopOk; }
  bool stopLight() { calls.push_back("lightOff"); light = false; return true; }
  bool startFan(uint32_t ticks) {
    calls.push_back("fanOn"); in1High = ticks; fan = true; ++starts; return fanStartOk;
  }
  bool startLightContinuous() { return setLightDuty(1024); }
  bool setLightDuty(uint32_t ticks) {
    calls.push_back("lightOn"); lightHigh = ticks; light = true; return lightStartOk;
  }
  void emergencyOff() {
    calls.push_back("emergencyOff"); fan = light = false; ++emergencies;
  }
};

struct Rig {
  FakeHal hal;
  heli::OutputDriver<FakeHal> outputs{hal};
  heli::Controller logic;
  heli::ThermalSafety thermal;
  heli::Sample sample{{25,25,25},3.8f,0,true};
  bool adcHealthy=true, fresh=true;
  heli::Inputs in{false, false, false};
  heli::Request wanted{false, false};
  uint32_t now;
  explicit Rig(uint32_t start = 0, heli::Inputs initial = {false, false, false})
      : in(initial), now(start) {
    CHECK(outputs.begin(now));
    logic.begin(now, in);
    tick();
  }
  void tick() {
    if(fresh) sample.at=now;
    wanted = logic.step(now, in, thermal.step(now,sample,adcHealthy));
    if (!outputs.apply(now, wanted)) logic.latchSoftwareFault();
    if(outputs.startupAborted()) logic.cancelLightRequest();
  }
  void advance(uint32_t ms) { for (uint32_t i=0; i<ms; ++i) { ++now; tick(); } }
  void ready() { advance(5500); }
  void press(bool light, bool fan) {
    in.lightPressed = light; in.fanPressed = fan; tick(); advance(25);
  }
  void release() { in.lightPressed = in.fanPressed = false; tick(); advance(25); }
};

template <typename F> void scenario(const char *name, F f) {
  f(); ++scenarios; printf("PASS %s\n", name);
}

struct FakeAdcBus {
 bool writeOk=true,readOk=true,busy=false,badConfig=false;
 uint16_t config=0;
 int16_t values[4]={13200,13200,13200,15200};
 int writes=0,reads=0;
 std::vector<uint16_t> commands;
 bool writeRegister(uint8_t reg,uint16_t value) {
  CHECK(reg==1);++writes;config=value;commands.push_back(value);return writeOk;
 }
 bool readRegister(uint8_t reg,uint16_t &value) {
  ++reads;if(!readOk)return false;
  if(reg==1) {
   value=static_cast<uint16_t>(config&0x7FFF);
   if(!busy)value|=0x8000;
   if(badConfig)value^=0x1000;
  }else {
   CHECK(reg==0);
   const uint8_t ch=static_cast<uint8_t>(((config>>12)&7)-4);
   CHECK(ch<4);value=static_cast<uint16_t>(values[ch]);
  }
  return true;
 }
};
template<class Sampler> void scanTo(Sampler &a,uint32_t first,uint32_t last) {
 for(uint32_t t=first;t<=last;++t)a.poll(t);
}

int main() {
  scenario("power-on OFF and released-key arming", [] {
    Rig r; r.advance(499); CHECK(!r.hal.fan && !r.hal.light);
    r.advance(5001); CHECK(!r.hal.fan && !r.hal.light && r.hal.starts == 0);
    r.press(true,false); CHECK(r.hal.light && !r.hal.fan);
  });
  scenario("independent light/fan and simultaneous keys", [] {
    Rig r; r.ready(); r.press(true,true); CHECK(r.hal.light && r.hal.fan);
    r.release(); r.press(false,true); CHECK(r.hal.light && !r.hal.fan);
    r.release(); r.press(true,false); CHECK(!r.hal.light && !r.hal.fan);
    r.release(); r.press(false,true); CHECK(!r.hal.light && r.hal.fan);
  });
  scenario("both-edge bounce and held-key no-repeat", [] {
    Rig r; r.ready();
    for (int i=0;i<4;++i) { r.in.fanPressed=true;r.tick();r.advance(8);
      r.in.fanPressed=false;r.tick();r.advance(8); }
    CHECK(r.hal.starts == 0);
    r.press(false,true); CHECK(r.hal.fan && r.hal.starts==1);
    r.advance(2000); CHECK(r.hal.fan && r.hal.starts==1);
    r.in.fanPressed=false;r.tick();r.advance(8);
    r.in.fanPressed=true;r.tick();r.advance(8);CHECK(r.hal.fan);
    r.release();r.press(false,true);CHECK(!r.hal.fan);
  });
  scenario("keys held across boot require release then fresh press", [] {
    Rig r(0,{true,true,false});r.ready();r.advance(1000);
    CHECK(!r.hal.fan && !r.hal.light);
    r.release();r.press(true,true);CHECK(r.hal.light && r.hal.fan);
  });
  scenario("USB HIGH shuts both down on the same sampled update", [] {
    Rig r;r.ready();r.press(true,true);CHECK(r.hal.fan && r.hal.light);
    r.in.usbPresent=true;r.tick();CHECK(!r.wanted.fan && !r.wanted.light);
    CHECK(!r.hal.fan && !r.hal.light);
    r.advance(3000);CHECK(r.hal.starts==1);
  });
  scenario("USB overrides a coincident debounced press", [] {
    Rig r;r.ready();r.in.lightPressed=r.in.fanPressed=true;r.tick();r.advance(24);
    r.in.usbPresent=true;++r.now;r.tick();CHECK(!r.hal.fan && !r.hal.light);
  });
  scenario("USB chatter resets the 500ms absent guard", [] {
    Rig r;r.ready();r.in.usbPresent=true;r.tick();
    r.in.usbPresent=false;r.tick();r.advance(499);
    r.in.usbPresent=true;r.tick();r.in.usbPresent=false;r.tick();r.advance(499);
    r.press(true,true);CHECK(!r.hal.fan && !r.hal.light);
    r.release();r.press(true,true);CHECK(r.hal.fan && r.hal.light);
  });
  scenario("unplug never restores loads or queued/held presses", [] {
    Rig r;r.ready();r.press(true,true);r.in.usbPresent=true;r.tick();
    r.in.usbPresent=false;r.tick();r.advance(2000);
    CHECK(!r.hal.light && !r.hal.fan && r.hal.starts==1);
    r.release();r.press(true,true);CHECK(r.hal.fan && r.hal.light && r.hal.starts==2);
  });
  scenario("USB present at boot remains inhibited", [] {
    Rig r(0,{false,false,true});r.advance(5000);r.press(true,true);
    CHECK(!r.hal.fan && !r.hal.light);
  });
  scenario("millis rollover preserves USB and button guards", [] {
    Rig r(UINT32_MAX-300U);r.ready();r.press(true,true);CHECK(r.hal.fan&&r.hal.light);
    r.in.usbPresent=true;r.tick();CHECK(!r.hal.fan&&!r.hal.light);
    r.in.usbPresent=false;r.tick();r.advance(550);r.release();r.press(false,true);
    CHECK(r.hal.fan && !r.hal.light);
  });
  scenario("waveform polarity and independent light duty", [] {
    Rig r;r.ready();r.press(true,true);
    CHECK(r.hal.in1High==410);CHECK(r.hal.lightHigh==1024);
    CHECK(heli::kFanPwmHz==20000);CHECK(heli::kLightPwmHz==5000);
    CHECK(heli::kPwmPeriodTicks-r.hal.in1High==614);
  });
  scenario("10ms actual OFF interval before motor restart", [] {
    FakeHal h;heli::OutputDriver<FakeHal> d(h);CHECK(d.begin(0));
    CHECK(d.apply(9,{true,true}));CHECK(!h.light&&!h.fan);
    CHECK(d.apply(10,{true,true}));CHECK(h.fan);
    CHECK(d.apply(11,{true,false}));CHECK(!h.fan&&h.light);
    CHECK(d.apply(20,{true,true}));CHECK(!h.fan);
    CHECK(d.apply(21,{true,true}));CHECK(h.fan&&h.starts==2);
  });
  scenario("steady ON never reinitializes/retries hardware stall", [] {
    FakeHal h;heli::OutputDriver<FakeHal> d(h);CHECK(d.begin(0));
    CHECK(d.apply(10,{false,true}));
    for(uint32_t t=11;t<10000;++t)CHECK(d.apply(t,{false,true}));
    CHECK(h.starts==1&&h.stops==1);
    CHECK(d.apply(10000,{false,false}));CHECK(d.apply(10010,{false,true}));
    CHECK(h.starts==2);
  });
  scenario("init failure stays OFF until reset", [] {
    FakeHal h;h.initOk=false;heli::OutputDriver<FakeHal> d(h);CHECK(!d.begin(0));
    CHECK(!d.apply(100,{true,true}));CHECK(h.emergencies==1&&!h.fan&&!h.light);
  });
  scenario("fan PWM failure shuts both loads and latches fault", [] {
    Rig r;r.ready();r.press(true,false);CHECK(r.hal.light);r.release();
    r.hal.fanStartOk=false;r.press(false,true);
    CHECK(r.logic.faulted()&&!r.hal.light&&!r.hal.fan);
    const int starts=r.hal.starts;r.release();r.press(true,true);r.advance(2000);
    CHECK(r.hal.starts==starts&&r.hal.emergencies==1);
  });
  scenario("light PWM failure and shutdown failure also fail OFF", [] {
    Rig r;r.ready();r.press(false,true);CHECK(r.hal.fan);r.release();
    r.hal.lightStartOk=false;r.press(true,false);
    CHECK(r.logic.faulted()&&!r.hal.light&&!r.hal.fan);
    Rig s;s.ready();s.press(false,true);s.release();s.hal.fanStopOk=false;
    s.in.usbPresent=true;s.tick();CHECK(s.logic.faulted()&&!s.hal.fan&&!s.hal.light);
  });

  scenario("NTC conversion: known points and all channel open/short rails", [] {
    float c=0;
    CHECK(heli::ntcTemperature(13200,0,c));CHECK(fabsf(c-25)<0.002f);
    for(int temp=-20;temp<=100;++temp) {
      const float resistance=10000*expf(3950*(1.0f/(temp+273.15f)-1.0f/298.15f));
      const int16_t raw=static_cast<int16_t>(lroundf(3.3f*resistance/(10000+resistance)/0.000125f));
      CHECK(heli::ntcTemperature(raw,0,c));CHECK(fabsf(c-temp)<0.08f);
    }
    for(uint8_t i=0;i<3;++i) {
      CHECK(!heli::ntcTemperature(0,i,c));CHECK(!heli::ntcTemperature(-1,i,c));
      CHECK(!heli::ntcTemperature(26400,i,c));CHECK(!heli::ntcTemperature(32767,i,c));
    }
    const int16_t raw[4]={13200,13200,13200,16800};
    heli::Sample sample;CHECK(heli::decodeSample(raw,123,sample));
    CHECK(fabsf(sample.batteryV-4.2f)<0.001f&&sample.at==123);
  });
  scenario("sensor readiness: no button starts without five seconds healthy", [] {
    Rig r;r.advance(4900);r.press(true,true);CHECK(!r.hal.light&&!r.hal.fan);
    r.advance(700);CHECK(!r.hal.light&&!r.hal.fan);
    r.release();r.press(true,true);CHECK(r.hal.light&&r.hal.fan);
  });
  scenario("three independent derating curves are monotonic and bounded", [] {
    for(int ch=0;ch<3;++ch) {
      Rig r;r.ready();r.press(true,true);r.advance(50);
      uint16_t last=1000;
      for(int j=0;j<100;++j) {
        r.sample.c[ch]=heli::kDimC[ch]+j*(heli::kTripC[ch]-heli::kDimC[ch])/100;
        r.tick();
        CHECK(r.wanted.lightPermille<=last&&r.wanted.lightPermille>=250);
        CHECK(r.hal.light&&r.hal.fan);
        last=r.wanted.lightPermille;
      }
      r.sample.c[ch]=heli::kTripC[ch];r.tick();CHECK(!r.hal.light&&!r.hal.fan);
    }
  });
  scenario("each hard temperature trip shuts both loads; cooling never restores ON", [] {
    for(int ch=0;ch<3;++ch) {
      Rig r;r.ready();r.press(true,true);r.release();
      r.sample.c[ch]=heli::kTripC[ch];r.tick();CHECK(!r.hal.light&&!r.hal.fan);
      r.sample.c[ch]=heli::kRecoverC[ch]+0.1f;r.advance(6000);
      CHECK(!r.hal.light&&!r.hal.fan);
      r.sample.c[ch]=25;r.advance(5500);CHECK(!r.hal.light&&!r.hal.fan);
      r.press(true,true);CHECK(r.hal.light&&r.hal.fan);
    }
  });
  scenario("all sensor failures ADC loss NaN and stale data fail OFF", [] {
    for(int kind=0;kind<8;++kind) {
      Rig r;r.ready();r.press(true,true);
      if(kind==0)r.adcHealthy=false;
      if(kind==1)r.sample.valid=false;
      if(kind>=2&&kind<=4)r.sample.c[kind-2]=NAN;
      if(kind==5)r.sample.batteryV=NAN;
      if(kind==6){r.fresh=false;r.advance(249);CHECK(r.hal.light&&r.hal.fan);++r.now;}
      if(kind==7)r.sample.c[0]=-21;
      r.tick();CHECK(!r.hal.light&&!r.hal.fan);
    }
  });
  scenario("battery3.3V cutoff and3.5V recovery hysteresis", [] {
    Rig r;r.ready();r.press(true,true);r.release();r.sample.batteryV=3.299f;r.tick();
    CHECK(!r.hal.light&&!r.hal.fan);
    r.sample.batteryV=3.49f;r.advance(6000);r.press(true,true);CHECK(!r.hal.light&&!r.hal.fan);
    r.sample.batteryV=3.5f;r.advance(5100);CHECK(!r.hal.light&&!r.hal.fan);
    r.release();r.press(true,true);CHECK(r.hal.light&&r.hal.fan);
  });
  scenario("cold and excessive battery voltage also inhibit both loads", [] {
    for(int kind=0;kind<2;++kind) {
      Rig r;r.ready();r.press(true,true);
      if(kind==0)r.sample.c[2]=-0.1f;else r.sample.batteryV=4.31f;
      r.tick();CHECK(!r.hal.light&&!r.hal.fan);
    }
  });
  scenario("recovery timer resets on intermittent faults and wraps millis", [] {
    Rig r(UINT32_MAX-3000);r.ready();r.press(true,true);
    r.adcHealthy=false;r.tick();r.adcHealthy=true;r.advance(4999);
    CHECK(!r.hal.fan);r.adcHealthy=false;r.tick();r.adcHealthy=true;r.advance(4999);
    CHECK(!r.hal.fan);r.advance(100);CHECK(!r.hal.fan);r.release();r.press(true,true);
    CHECK(r.hal.fan&&r.hal.light);
  });
  scenario("startup stays HIGH50ms then follows5kHz dimming request", [] {
    FakeHal h;heli::OutputDriver<FakeHal>d(h);CHECK(d.begin(0));
    CHECK(d.apply(10,{true,false,500,true}));CHECK(h.lightHigh==1024);
    CHECK(d.apply(59,{true,false,500,true}));CHECK(h.lightHigh==1024);
    CHECK(d.apply(60,{true,false,500,true}));CHECK(h.lightHigh==512);
    CHECK(d.apply(61,{true,false,250,false}));CHECK(h.lightHigh==256);
    CHECK(d.apply(62,{false,false}));CHECK(!h.light);
    CHECK(d.apply(71,{true,false,1000,true}));CHECK(!h.light);
    CHECK(d.apply(72,{true,false,1000,true}));CHECK(h.light&&h.lightHigh==1024);
  });
  scenario("USB interrupts light startup immediately", [] {
    Rig r;r.ready();r.press(true,false);CHECK(r.hal.light);
    r.advance(20);r.in.usbPresent=true;r.tick();CHECK(!r.hal.light);
    r.advance(100);CHECK(!r.hal.light);
  });
  scenario("warm light cold-start is refused; fan remains independently available", [] {
    Rig r;r.ready();r.sample.c[0]=65;r.tick();r.press(true,true);
    CHECK(!r.hal.light&&r.hal.fan);
    r.sample.c[0]=25;r.advance(1000);CHECK(!r.hal.light);
    r.release();r.press(true,false);CHECK(r.hal.light);
  });
  scenario("derating during full-HIGH startup aborts without automatic restart", [] {
    Rig r;r.ready();r.press(true,false);r.sample.c[1]=44;r.tick();CHECK(!r.hal.light);
    r.sample.c[1]=25;r.advance(1000);CHECK(!r.hal.light);
    r.release();r.press(true,false);CHECK(r.hal.light);
  });
  scenario("dimming HAL failure latches both loads OFF until reset", [] {
    Rig r;r.ready();r.press(true,true);r.advance(60);r.hal.lightStartOk=false;
    r.sample.c[0]=65;r.tick();CHECK(r.logic.faulted()&&!r.hal.light&&!r.hal.fan);
  });


  scenario("ADS1115 real register sequence, four muxes, scaling and freshness", [] {
    FakeAdcBus b;heli::Ads1115Sampler<FakeAdcBus>a(b);a.begin(0);
    a.poll(0);CHECK(!a.healthy()&&b.writes==1&&b.reads==0);
    scanTo(a,1,8);CHECK(b.reads==0);
    scanTo(a,9,36);CHECK(a.healthy()&&a.sample().valid);
    CHECK(b.commands.size()==4);
    const uint16_t expected[4]={0xC383,0xD383,0xE383,0xF383};
    for(int ch=0;ch<4;++ch)CHECK(b.commands[ch]==expected[ch]);
    CHECK(a.sample().at==36&&fabsf(a.sample().batteryV-3.8f)<0.001f);
    scanTo(a,37,99);CHECK(b.writes==4);
    a.poll(100);CHECK(b.writes==5);
    scanTo(a,101,136);CHECK(a.healthy()&&a.sample().at==136);
  });
  scenario("ADS1115 NACK, config mismatch and busy timeout fail immediately", [] {
    for(int mode=0;mode<4;++mode) {
      FakeAdcBus b;heli::Ads1115Sampler<FakeAdcBus>a(b);a.begin(0);
      if(mode==0)b.writeOk=false;
      if(mode==1)b.readOk=false;
      if(mode==2)b.badConfig=true;
      if(mode==3)b.busy=true;
      scanTo(a,0,21);CHECK(!a.healthy()&&!a.sample().valid);
      const int writes=b.writes;scanTo(a,22,249);CHECK(b.writes==writes);
      b.writeOk=b.readOk=true;b.badConfig=b.busy=false;
      scanTo(a,250,400);CHECK(a.healthy()&&a.sample().valid);
    }
  });
  scenario("all three remote NTC open and short cases invalidate completed frames", [] {
    for(int ch=0;ch<3;++ch)for(int mode=0;mode<2;++mode){
      FakeAdcBus b;heli::Ads1115Sampler<FakeAdcBus>a(b);a.begin(0);
      scanTo(a,0,36);CHECK(a.healthy());
      b.values[ch]=mode?26400:0;scanTo(a,37,140);
      CHECK(!a.healthy()&&!a.sample().valid);
    }
  });
  scenario("hot first channel disables before waiting for full scan", [] {
    FakeAdcBus b;heli::Ads1115Sampler<FakeAdcBus>a(b);a.begin(0);
    scanTo(a,0,36);CHECK(a.healthy());
    const float resistance=10000*expf(3950*(1.0f/348.15f-1.0f/298.15f)); //75C
    b.values[0]=static_cast<int16_t>(lroundf(3.3f*resistance/(10000+resistance)/0.000125f));
    scanTo(a,37,109);CHECK(!a.healthy()&&!a.sample().valid);
    CHECK(b.writes==5); // no AIN1/2/3 conversion for this invalid frame
  });
  scenario("ADS disconnect during operation clears previous good frame", [] {
    FakeAdcBus b;heli::Ads1115Sampler<FakeAdcBus>a(b);a.begin(0);
    scanTo(a,0,36);CHECK(a.healthy());b.readOk=false;
    scanTo(a,37,109);CHECK(!a.healthy()&&!a.sample().valid);
  });
  scenario("ADS conversion deadline and scan scheduler survive millis rollover", [] {
    FakeAdcBus b;heli::Ads1115Sampler<FakeAdcBus>a(b);
    const uint32_t begin=UINT32_MAX-15;a.begin(begin);
    for(uint32_t dt=0;dt<=36;++dt)a.poll(begin+dt);
    CHECK(a.healthy()&&a.sample().at==begin+36);
    for(uint32_t dt=37;dt<=136;++dt)a.poll(begin+dt);
    CHECK(a.healthy()&&b.writes==8);
  });

  printf("%d scenarios, %d assertions passed\n",scenarios,assertions);
}
