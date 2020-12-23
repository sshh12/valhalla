#include "heltec.h"
#include "valhalla.h"

void loraSend(byte from, byte to, byte type, byte dat[], int sz)
{
  LoRa.beginPacket();
  LoRa.setTxPower(TX_POWER, RF_PACONFIG_PASELECT_PABOOST);
  LoRa.write(from);
  LoRa.write(to);
  LoRa.write(type);
  LoRa.write(sz);
  LoRa.write(dat, sz);
  LoRa.endPacket();
}

void loraDecode(int packetSize, packet_t *packet)
{
  if (packetSize == 0)
  {
    packet->type = PACKET_INVALID;
    return;
  }
  packet->from = LoRa.read();
  packet->to = LoRa.read();
  packet->type = LoRa.read();
  packet->rssi = LoRa.packetRssi();
  byte incomingLength = LoRa.read();
  int i = 0;
  while (LoRa.available())
  {
    packet->data.body[i++] = LoRa.read();
  }
}
