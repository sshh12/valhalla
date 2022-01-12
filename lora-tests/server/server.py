from flask import Flask
import socket
import sys
import queue
import threading
import time

from protocol import *
from valhalla import *

DEVICE_PORT = 8111
HTTP_PORT = 5000


def on_packet(packet):
    print(packet)
    if packet.type == PACKET_ENVDATA:
        print(envdata_t.parse(packet.data))


def write_queue_to_conn(conn, data_q):
    while True:
        try:
            packet_bytes = data_q.get()
            conn.sendall(packet_bytes)
            data_q.task_done()
        except Exception as e:
            print(e)
            break


def listen_for_http(data_q):
    app = Flask(__name__)

    @app.route("/")
    def index():
        sw = switchdata_t.build(dict(onoff=1, toggle=1, swId=0))
        data_q.put(
            packet_t.build(dict(from_=ADDR_ROUTER, to=ADDR_HORSEBARN, data=sw, type=PACKET_SWITCHDATA, empty=0, rssi=0))
        )
        return "!"

    app.run("0.0.0.0", HTTP_PORT, debug=False)


def listen_for_devices(data_q):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", DEVICE_PORT))
    sock.listen(1)

    while True:
        conn, addr = sock.accept()
        print(addr)
        wt = threading.Thread(target=write_queue_to_conn, args=(conn, data_q))
        wt.start()
        try:
            d = b""
            while True:
                data = conn.recv(4)
                if not data:
                    break
                d += data
                if len(d) >= packet_t_size:
                    packet = packet_t.parse(d[:packet_t_size])
                    d = d[packet_t_size:]
                    on_packet(packet)
        finally:
            print("conn close")
            conn.close()
            wt.join()


if __name__ == "__main__":
    q = queue.Queue()
    device_thread = threading.Thread(target=listen_for_devices, args=(q,))
    device_thread.start()
    http_thread = threading.Thread(target=listen_for_http, args=(q,))
    http_thread.start()
    device_thread.join()
    http_thread.join()
