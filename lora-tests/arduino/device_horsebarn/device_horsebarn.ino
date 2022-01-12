#include "heltec.h"
#include "valhalla.h"
#include "DHTesp.h"

#define ADDR ADDR_HORSEBARN
#define INTERVAL 1000 * 60 * 10

packet_t lastPacket;
bool switchPos = false;
bool newPos;

DHTesp dht;
long lastSendTime = 0;
long interval = INTERVAL;

void setup()
{
  Heltec.begin(false, true, true, true, BAND);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  digitalWrite(12, LOW);
  digitalWrite(13, LOW);
  dht.setup(21, DHTesp::AUTO_DETECT);
  Serial.println(dht.getStatusString());
}

void loop()
{
  if (millis() - lastSendTime > interval)
  {
    TempAndHumidity lastValues = dht.getTempAndHumidity();
    envdata_t tempdata;
    tempdata.temp = lastValues.temperature * 9 / 5 + 32;
    tempdata.hum = lastValues.humidity;
    loraSend(ADDR, ADDR_ROUTER, PACKET_ENVDATA, (byte *)&tempdata, sizeof(envdata_t));
    Serial.println("Sending...");
    lastSendTime = millis();
    interval = random(INTERVAL / 10) + INTERVAL;
    LoRa.receive();
  }
  loraDecode(LoRa.parsePacket(), &lastPacket);
  if (lastPacket.type != PACKET_INVALID && lastPacket.to == ADDR) {
    if (lastPacket.type == PACKET_SWITCHDATA) {
      if (lastPacket.data.switchdata.toggle) {
        newPos = !switchPos;
      }
      else {
        newPos = (lastPacket.data.switchdata.onoff != 0);
      }
    }

  }
  if (newPos != switchPos) {
    if (newPos) {
      Serial.println("on");
      turnOn();
    } else {
      Serial.println("off");
      turnOff();
    }
    switchPos = newPos;
  }
}

void turnOn() {
  digitalWrite(12, HIGH);
  delay(750);
  digitalWrite(12, LOW);
}

void turnOff() {
  digitalWrite(13, HIGH);
  delay(750);
  digitalWrite(13, LOW);
}
