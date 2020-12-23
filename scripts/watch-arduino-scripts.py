from watchdog.observers import Observer
import shutil
import glob
import time
import os

FILES = ["valhalla.cpp", "valhalla.h", "secrets.h"]


def sync():
    print("Syncing...")
    for dir_ in glob.iglob("arduino/device_*"):
        for fn in FILES:
            shutil.copyfile(os.path.join("arduino", fn), os.path.join(dir_, fn))


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