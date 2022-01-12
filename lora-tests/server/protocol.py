import construct as cstruct

packet_t = cstruct.Struct(
    "from_" / cstruct.Byte,
    "to" / cstruct.Byte,
    "type" / cstruct.Byte,
    "empty" / cstruct.Byte,
    "rssi" / cstruct.Int32sl,
    "data" / cstruct.Bytes(12),
)
packet_t_size = packet_t.sizeof()

bme280data_t = cstruct.Struct(
    "temp" / cstruct.Float32l,
    "pressure" / cstruct.Float32l,
    "hum" / cstruct.Float32l,
)

switchdata_t = cstruct.Struct(
    "onoff" / cstruct.Int32sl,
    "toggle" / cstruct.Int32sl,
    "swId" / cstruct.Int32sl,
)