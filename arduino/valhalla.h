#define BAND 915E6
#define TX_POWER 15

#define ADDR_BROADCAST 0x00
#define ADDR_HOME 0x01
#define ADDR_CATBARN 0x02

#define PACKET_INVALID 0x00
#define PACKET_BME280DATA 0x01

struct bme280data_t
{
  float temp;
  float pressure;
  float hum;
};

struct packet_t
{
  byte from;
  byte to;
  byte type;
  int rssi;
  union
  {
    bme280data_t bme280data;
    byte body[100];
  } data;
};

void loraSend(byte from, byte to, byte type, byte dat[], int sz);
void loraDecode(int packetSize, packet_t *packet);
