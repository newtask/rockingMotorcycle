import time

import RPi.GPIO as GPIO

from button import Button
from led import LED

GPIO.setmode(GPIO.BCM)


def printResult(result):
    print("Result: {}".format(result))


def ledTest():
    print("Start LED test")

    pinLED = 17

    led = LED(pinLED)
    led.setListener(printResult)

    while True:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)


def buttonTest():
    print("Start button test")

    pinBTN = 27

    button = Button(pinBTN)
    button.setListener(printResult)

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

# Cleanup GPIO settings
GPIO.cleanup()

print("All tests done")