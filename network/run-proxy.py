import subprocess
import time
import re

LISTEN_PORT = 4080
BASE_LOCAL_PORT = 1080
ANDROID_PORT = 1080


class Glider:
    def __init__(self):
        self.p = None

    def update(self, forwards):
        if self.p is not None:
            self.p.terminate()
        if len(forwards) == 0:
            return
        cmd = [
            "glider",
            "-listen",
            "mixed://:" + str(LISTEN_PORT),
            "-check",
            "www.google.com",
            "-checkinterval",
            "300",
            "-strategy",
            "rr",
        ]
        for port in forwards:
            cmd.extend(["-forward", "socks5://127.0.0.1:" + str(port)])
        print("$ " + " ".join(cmd))
        self.p = subprocess.Popen(cmd)


def run_cmd(cmd):
    print("$ " + " ".join(cmd))
    try:
        out = str(subprocess.check_output(cmd), "ascii")
    except subprocess.CalledProcessError as e:
        print("error", e)
        out = ""
    return out


def get_adb_devices():
    devices = []
    out = run_cmd(["adb", "devices"])
    for match in re.finditer(r"(\w+)\tdevice[\r\n]", out):
        devices.append(match.group(1))
    return devices


def update_adb_forwarding(port_map):
    for device_id, _ in port_map.items():
        run_cmd(["adb", "-s", device_id, "forward", "--remove-all"])
    for device_id, port in port_map.items():
        run_cmd(["adb", "-s", device_id, "forward", "tcp:" + str(port), "tcp:" + str(ANDROID_PORT)])


def get_current_port_map(_port=[BASE_LOCAL_PORT]):
    port_map = {}
    for device_id in get_adb_devices():
        port = _port[0]
        port_map[device_id] = port
        _port[0] += 1
        if _port[0] > BASE_LOCAL_PORT + 1000:
            _port[0] = BASE_LOCAL_PORT
    return port_map


def main():
    glider = Glider()
    port_map = None
    while True:
        new_port_map = get_current_port_map()
        if port_map is None or new_port_map.keys() != port_map.keys():
            print("Updating...", new_port_map, "(old ", port_map, ")")
            update_adb_forwarding(new_port_map)
            glider.update(list(new_port_map.values()))
        port_map = new_port_map
        time.sleep(10)


if __name__ == "__main__":
    main()
