import threading
import time

from lib.LSM6DS3 import LSM6DS3
from lib.listener import Listener


class IMUController(threading.Thread, Listener):

    def __init__(self, address=0x6a, intervalMs=100, limit=100):
        Listener.__init__(self)
        threading.Thread.__init__(self)

        self.isRunning = True
        self.lsm = LSM6DS3(address)
        self.interval = intervalMs / 1000
        self.limit = limit

        self.lastGyroX = self.lsm.readRawGyroX()
        self.lastGyroY = self.lsm.readRawGyroY()
        self.lastGyroZ = self.lsm.readRawGyroZ()

    def hasGyroXChanged(self):

        cx = self.lsm.readRawGyroX()
        dx = cx - self.lastGyroX

        if dx > self.limit or dx < -self.limit:
            print("dx", dx)
            self.lastGyroX = cx
            return True

        return False

    def hasGyroYChanged(self):

        cy = self.lsm.readRawGyroY()
        dy = cy - self.lastGyroY

        if dy > self.limit or dy < -self.limit:
            print("dy", dy)
            self.lastGyroX = cy
            return True

        return False

    def hasGyroZChanged(self):

        cz = self.lsm.readRawGyroZ()
        dz = cz - self.lastGyroZ

        if dz > self.limit or dz < -self.limit:
            print("dz", dz)
            self.lastGyroZ = cz
            return True

        return False

    def hasChanged(self):
        return self.hasGyroXChanged() or self.hasGyroYChanged() or self.hasGyroZChanged()

    def stop(self):
        self.isRunning = False

    def run(self):
        while self.isRunning:
            if self.listener is not None and self.hasChanged():
                self.listener()

            time.sleep(self.interval)
