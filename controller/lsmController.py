import threading
import time

from lsm303d import LSM303D

from lib.listener import Listener


class LSMController(threading.Thread, Listener):

    def __init__(self, address=0x1d, intervalMs=100, limit=100):
        Listener.__init__(self)
        threading.Thread.__init__(self)

        self.isRunning = True
        self.lsm = LSM303D(address)
        self.interval = intervalMs / 1000
        self.limit = limit

        self.lastAccl = self.lsm.accelerometer()

    def hasChanged(self):
        a = self.lsm.accelerometer()

        d = []

        for i in range(0, 3):
            dv = a[i] - self.lastAccl[i]

            if dv > self.limit or dv < -self.limit:
                # print("dy", dy)
                self.lastAccl = a
                return True

            d.append(dv)


        # print(("{:+06.2f} : {:+06.2f} : {:+06.2f}   " ).format(*d))
        # print("d", d)
        return False

    def stop(self):
        self.isRunning = False

    def run(self):
        while self.isRunning:
            if self.listener is not None and self.hasChanged():
                self.listener()

            time.sleep(self.interval)
