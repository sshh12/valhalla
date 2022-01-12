from watchdog.observers import Observer
import shutil
import glob
import time
import os
import re

FILES = ["valhalla.cpp", "valhalla.h", "secrets.h"]


def sync():
    print("Syncing...")
    for dir_ in glob.iglob("arduino/device_*"):
        for fn in FILES:
            shutil.copyfile(os.path.join("arduino", fn), os.path.join(dir_, fn))

    defines = {}
    define_types = {}
    with open(os.path.join("arduino", "valhalla.h"), "r") as fp:
        for match in re.finditer(r"#define (\w+) (\S+)\s", fp.read()):
            name = match.group(1)
            val = match.group(2)
            defines[name] = val
            if "_" in name:
                group, type_ = name.split("_", 1)
                if group not in define_types:
                    define_types[group] = {}
                define_types[group][type_] = val
    with open(os.path.join("server", "valhalla.py"), "w") as fp:
        fp.write('"""Autogenerated constants"""\n')
        for name, val in defines.items():
            fp.write("{} = {}\n".format(name, val))
        for group, group_vals in define_types.items():
            fp.write(
                "{}_DICT = {}\n".format(
                    group, "{" + (", ".join(['"{}": {}'.format(k, v) for k, v in group_vals.items()])) + "}"
                )
            )


class Handler:
    def __init__(self, f):
        self.f = f

    def dispatch(self, evt):
        self.f()


if __name__ == "__main__":
    sync()
    observer = Observer()
    observer.schedule(Handler(sync), "arduino")
    observer.start()
    try:
        while True:
            time.sleep(999)
    finally:
        observer.stop()
        observer.join()