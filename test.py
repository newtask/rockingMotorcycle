import time

import RPi.GPIO as GPIO

from button import Button
from led import LED

GPIO.setmode(GPIO.BCM)

pinLED = 17
pinBTN = 27


def printResult(result):
    print("Result: {}".format(result))


def ledTest():
    print("Start LED test")

    led = LED(pinLED)
    led.setListener(printResult)

    while True:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)


def buttonTest():
    print("Start button test")

    button = Button(pinBTN)
    button.setListener(printResult)

    while True:
        button.loop()


def buttonLedTest():
    print("Start Button-LED test")

    led = LED(pinLED)
    button = Button(pinBTN)

    def blink(count):
        waitTime = 0.1
        # blink once

        for i in range(count):
            led.on()
            time.sleep(waitTime)

            led.off()
            time.sleep(waitTime)

    def buttonListner(mode):
        blink(mode + 1)


    button.setListener(buttonListner)

    while True:
        button.loop()

print("Start test units. Use ctrl+c to stop current test.")

try:
    ledTest()
except KeyboardInterrupt:
    print("Cancel led test")

try:
    buttonTest()
except KeyboardInterrupt:
    print("Cancel button test")

try:
    buttonLedTest()
except KeyboardInterrupt:
    print("Cancel button-LED test")

# Cleanup GPIO settings
GPIO.cleanup()

print("All tests done")
