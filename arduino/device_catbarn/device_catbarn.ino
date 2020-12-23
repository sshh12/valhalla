#include <Wire.h>
#include <SPI.h>
#include "heltec.h"
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include "valhalla.h"

#define ADDR ADDR_CATBARN
#define INTERVAL 2000

Adafruit_BME280 bme;
long lastSendTime = 0;
int interval = INTERVAL;

void setup()
{
  Heltec.begin(false, true, true, true, BAND);
  if (!bme.begin())
  {
    Serial.println("BME FAILED");
    while (1)
      ;
  }
  else
  {
    Serial.println("BME SUCCESS");
  }
}

void loop()
{
  float temp = bme.readTemperature() * 9 / 5 + 32;
  float pressure = bme.readPressure() / 100.0F;
  float hum = bme.readHumidity();
  if (millis() - lastSendTime > interval)
  {
    bme280data_t tempdata;
    tempdata.temp = temp;
    tempdata.pressure = pressure;
    tempdata.hum = hum;
    loraSend(ADDR, ADDR_HOME, PACKET_BME280DATA, (byte *)&tempdata, sizeof(bme280data_t));
    Serial.println("Sending...");
    lastSendTime = millis();
    interval = random(INTERVAL) + 1000;
    LoRa.receive();
  }
  delay(1000);
}
