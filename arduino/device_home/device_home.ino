#include "heltec.h"
#include <WiFi.h>
#include "valhalla.h"

#define ADDR ADDR_ROUTER

volatile char packetIdx = 0;
volatile char packetReadIdx = 0;
packet_t lastPacket;
packet_t fwdPacket;
size_t fwdCnt;

void setup()
{
  Heltec.begin(false, true, true, true, BAND);
  Serial.println("Started");
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
  }
  Serial.print("WiFi Connected.");
}

void loop()
{
  Serial.println(sizeof(packet_t));
  WiFiClient client;
  if (!client.connect(WIFI_HOST, WIFI_PORT))
  {
    Serial.println("TCP conn failed...");
    return;
  }
  while (client.connected())
  {
    loraDecode(LoRa.parsePacket(), &lastPacket);
    if (lastPacket.type != PACKET_INVALID) {
      Serial.println("recv");
      client.write((byte*)&lastPacket, sizeof(packet_t));
    }
    fwdCnt = client.readBytes((byte*)&fwdPacket, sizeof(packet_t));
    if(fwdCnt == sizeof(packet_t)) {
      Serial.println("send");
      loraSend(fwdPacket.from, fwdPacket.to, fwdPacket.type, fwdPacket.data.body, sizeof(fwdPacket.data.body));
    }
  }
}
