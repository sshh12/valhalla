import subprocess
import time
import re

LISTEN_PORT = 4080
BASE_PORT = 1080
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
            "-verbose",
        ]
        for port in forwards:
            cmd.extend(["-forward", "socks5://127.0.0.1:" + str(port)])
        print("$ " + " ".join(cmd))
        self.p = subprocess.Popen(cmd)


def run_cmd(cmd):
    out = str(subprocess.check_output(cmd), "ascii")
    print("$ " + " ".join(cmd), "->", out)
    return out


def get_adb_devices():
    devices = []
    out = run_cmd(["adb", "devices"])
    for match in re.finditer(r"\n(\w+)\t\w+[\r\n]", out):
        devices.append(match.group(1))
    return devices


def update_adb_forwarding(port_map):
    for device_id, _ in port_map.items():
        run_cmd(["adb", "-s", device_id, "forward", "--remove-all"])
    for device_id, port in port_map.items():
        run_cmd(["adb", "-s", device_id, "forward", "tcp:" + str(port), "tcp:" + str(ANDROID_PORT)])


def get_current_port_map():
    port_map = {}
    for device_id in get_adb_devices():
        port = max([BASE_PORT] + list(port_map.values())) + 1
        port_map[device_id] = port
    return port_map


def main():
    glider = Glider()
    port_map = None
    while True:
        new_port_map = get_current_port_map()
        if new_port_map != port_map:
            print("Updating...", new_port_map)
            update_adb_forwarding(new_port_map)
            glider.update(list(new_port_map.values()))
        port_map = new_port_map
        time.sleep(10)


if __name__ == "__main__":
    main()