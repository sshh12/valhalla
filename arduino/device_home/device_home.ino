#include "heltec.h"
#include <WiFi.h>

#include "valhalla.h"
#include "secrets.h"

#define ADDR ADDR_HOME

const char *ssid = "";
const char *password = "";
const char *host = "10.0.0.7";
const int port = 8111;

bool updated = false;
bme280data_t catbarntemp;

void setup()
{
  Heltec.begin(false, true, true, true, BAND);
  LoRa.onReceive(onReceive);
  LoRa.receive();
  Serial.println("Started");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
}

void loop()
{
  if (!updated)
  {
    delay(1000);
    return;
  }
  updated = false;
  WiFiClient client;
  if (!client.connect(host, port))
  {
    Serial.println("connection failed");
    return;
  }

  String url = "/";
  client.print("GET /?");
  client.printf("temp=%f&pressure=%f&hum=%f", catbarntemp.temp, catbarntemp.pressure, catbarntemp.hum);
  client.print(String(" HTTP/1.1\r\n") +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");
  unsigned long timeout = millis();
  while (client.available() == 0)
  {
    if (millis() - timeout > 5000)
    {
      Serial.println(">>> Client Timeout !");
      client.stop();
      return;
    }
  }
  while (client.available())
  {
    client.readStringUntil('\r');
  }
}

void onReceive(int packetSize)
{
  packet_t packet;
  loraDecode(packetSize, &packet);
  if (packet.to != ADDR || packet.type == PACKET_INVALID)
  {
    return;
  }
  if (packet.type == PACKET_BME280DATA)
  {
    catbarntemp = packet.data.bme280data;
    Serial.printf("%.1fF %.1fhPa %.1f%%\n", catbarntemp.temp, catbarntemp.pressure, catbarntemp.hum);
    updated = true;
  }
}
