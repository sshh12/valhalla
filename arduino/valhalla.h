#include "secrets.h"

#define ADDR_BROADCAST 0x00
#define ADDR_ROUTER 0x01
#define ADDR_CATBARN 0x02
#define ADDR_HORSEBARN 0x03

#define PACKET_INVALID 0x00
#define PACKET_ENVDATA 0x01
#define PACKET_SWITCHDATA 0x02

struct envdata_t
{
  float temp;
  float pressure;
  float hum;
};

struct switchdata_t
{
  int onoff;
  int toggle;
  int swId;
};

struct packet_t
{
  byte from;
  byte to;
  byte type;
  int rssi;
  union
  {
    envdata_t envdata;
    switchdata_t switchdata;
    byte body[12];
  } data;
};

void loraSend(byte from, byte to, byte type, byte dat[], int sz);
void loraDecode(int packetSize, packet_t *packet);
