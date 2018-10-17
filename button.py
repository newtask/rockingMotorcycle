import time

import RPi.GPIO as GPIO


class Button:

    def __init__(self, pin, longPressTime=1000):

        self.NORMAL_PRESS = 0
        self.LONG_PRESS = 1

        self.RELEASED = 0
        self.PRESSED = 1
        self.IDLE = 2

        self.state = self.RELEASED
        self.listener = None

        self.longPressTime = longPressTime
        self.pressedTime = 0

        self.pin = pin

        GPIO.setup(pin, GPIO.IN)

    def loop(self):

        currentState = GPIO.input(self.pin)

        # check if button was pressed before
        if self.state is self.PRESSED:

            # check if the user is doing a long press
            if currentState is self.PRESSED:
                if self.get_millis() - self.pressedTime > self.longPressTime:
                    self.state = self.IDLE
                    self.pressedTime = 0
                    self.notifyLongPressed()
                    return

            else:  # RELEASED
                self.pressedTime = 0
                self.notifyNormalPressed()

        elif self.state is self.RELEASED:
            if currentState is self.PRESSED:
                self.pressedTime = self.get_millis()
            else:
                self.pressedTime = 0
        elif self.state is self.IDLE and currentState is self.PRESSED:
            # keep IDLE state as long the used presses the button
            return

        self.state = currentState

    def notifyLongPressed(self):
        if self.listener is None:
            return

        self.listener(self.LONG_PRESS)

    def notifyNormalPressed(self):
        if self.listener is None:
            return

        self.listener(self.NORMAL_PRESS)

    def get_millis(self):
        return int(round(time.time() * 1000))

    def setListener(self, listener):
        self.listener = listener

    def removeListener(self):
        self.listener = None