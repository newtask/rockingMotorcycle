import threading
import time


class LEDTask:
    repeat = 0
    onDuration = 0
    offDuration = 0

    def __init__(self, repeat, onDuration, offDuration):
        self.repeat = repeat
        self.onDuration = onDuration
        self.offDuration = offDuration


class LEDController(threading.Thread):

    def __init__(self, led):
        threading.Thread.__init__(self)

        self.cancelTask = False
        self.taskIsRunning = False
        self.led = led
        self.minWaitTime = 0.1
        self.currentTask = None
        self.isRunning = False

    def start(self):
        self.isRunning = True
        super(LEDController, self).start()


    def blink(self, repeat, onDuration, offDuration):
        self.cancelTask = True

        # wait until current task is finished
        while self.taskIsRunning:
            time.sleep(self.minWaitTime)

        self.cancelTask = False
        self.currentTask = LEDTask(repeat, onDuration, offDuration)

    def sleep(self, sec):

        millis = int(sec * 10)
        for i in range(millis):
            if self.cancelTask:
                return
            time.sleep(self.minWaitTime)

    def stop(self):
        self.cancelTask = True
        self.isRunning = False

    def run(self):
        while self.isRunning:
            if self.currentTask is not None:
                self.taskIsRunning = True

                for i in range(self.currentTask.repeat):
                    self.led.on()

                    self.sleep(self.currentTask.onDuration)

                    self.led.off()

                    if self.cancelTask:
                        break

                    self.sleep(self.currentTask.offDuration)

                    if self.cancelTask:
                        break

                self.taskIsRunning = False

            self.currentTask = None

            # prevent restarting directly
            time.sleep(self.minWaitTime)
