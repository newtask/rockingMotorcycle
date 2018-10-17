import RPi.GPIO as GPIO
from listener import Listener

class LED(Listener):

    def __init__(self, pin):
        Listener.__init__(self)

        self.pin = pin

        self.state = GPIO.LOW

        GPIO.setup(pin, GPIO.OUT)

    def on(self):
        self.state = GPIO.HIGH
        self.update()

    def off(self):
        self.state = GPIO.LOW
        self.update()

    def update(self):
        self.notifyState()
        GPIO.output(self.pin, self.state)

    def isOn(self):
        return self.state == GPIO.HIGH

    def notifyState(self):
        if self.listener is None:
            return

        self.listener(self.state)

