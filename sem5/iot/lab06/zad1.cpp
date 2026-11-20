#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define IDX_IN   1      // po teście z ogrzaniem sondy ewentualnie zamień 0 <-> 1
#define IDX_OUT  0
#define LED_RED   6
#define LED_GREEN 5
#define LED_BLUE  3
#define T_COLD 20.0     // poniżej: za zimno
#define T_HOT  24.0     // powyżej: za gorąco

LiquidCrystal_I2C lcd(0x27, 16, 2);
OneWire oneWire(A1);
DallasTemperature sensors(&oneWire);

float tMin = 1000.0, tMax = -1000.0;

void setColor(byte r, byte g, byte b) {
  digitalWrite(LED_RED, r);
  digitalWrite(LED_GREEN, g);
  digitalWrite(LED_BLUE, b);
}

void setup() {
  sensors.begin();
  lcd.init(); lcd.backlight(); lcd.clear();
  pinMode(LED_RED, OUTPUT); pinMode(LED_GREEN, OUTPUT); pinMode(LED_BLUE, OUTPUT);
}

void loop() {
  sensors.requestTemperatures();
  float tIn  = sensors.getTempCByIndex(IDX_IN);
  float tOut = sensors.getTempCByIndex(IDX_OUT);

  if (tOut != DEVICE_DISCONNECTED_C) {          // pomijamy błędny odczyt -127
    if (tOut < tMin) tMin = tOut;
    if (tOut > tMax) tMax = tOut;
  }

  if (tOut < T_COLD)      setColor(LOW, LOW, HIGH);   // niebieski
  else if (tOut > T_HOT)  setColor(HIGH, LOW, LOW);   // czerwony
  else                    setColor(LOW, HIGH, LOW);   // zielony

  char buf[17];                                       // 16 znaków + '\0'
  snprintf(buf, sizeof(buf), "IN%5s OUT%5s", String(tIn, 1).c_str(), String(tOut, 1).c_str());
  lcd.setCursor(0, 0); lcd.print(buf);
  snprintf(buf, sizeof(buf), "Lo%5s  Hi%5s", String(tMin, 1).c_str(), String(tMax, 1).c_str());
  lcd.setCursor(0, 1); lcd.print(buf);
}