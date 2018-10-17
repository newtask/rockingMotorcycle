import threading
import time


class LEDController(threading.Thread):
    IDLE = 0
    BLINKMIN = 10
    BLINKMAX = 19
    LONGMIN = 20
    LONGMAX = 29

    def __init__(self, led):
        threading.Thread.__init__(self)

        self.isRunning = True
        self.cancelTask = False
        self.taskIsRunning = False
        self.led = led
        self.minWaitTime = 0.1

        self.currentTask = LEDController.IDLE

    def blink(self, count):
        self.taskIsRunning = True

        waitTime = 0.1
        # blink once

        for i in range(count):
            self.led.on()
            self.sleep(waitTime)

            self.led.off()
            self.sleep(waitTime)

            if self.cancelTask:
                break

        self.taskIsRunning = False

    def sleep(self, sec):

        millis = int(sec * 10)
        for i in range(millis):
            if self.cancelTask:
                return
            time.sleep(self.minWaitTime)

    def long(self, waitTime):
        self.taskIsRunning = True

        self.led.on()
        self.sleep(waitTime)
        self.led.off()

        self.taskIsRunning = False

    def do(self, task):
        self.cancelTask = True

        # wait until current task is finished
        while self.taskIsRunning:
            time.sleep(self.minWaitTime)

        self.cancelTask = False
        self.currentTask = task

    def stop(self):
        self.isRunning = False

    def run(self):
        while self.isRunning:
            if LEDController.BLINKMIN <= self.currentTask <= LEDController.BLINKMAX:
                self.blink(self.currentTask - LEDController.BLINKMIN + 1)
            elif LEDController.LONGMIN <= self.currentTask <= LEDController.LONGMAX:
                self.long(self.currentTask - LEDController.LONGMIN + 1)

            self.currentTask = LEDController.IDLE

            # prevent restarting directly
            time.sleep(self.minWaitTime)
