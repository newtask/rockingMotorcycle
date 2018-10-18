#!/usr/bin/python3

import time

import RPi.GPIO as GPIO

from button import Button
from led import LED
from ledController import LEDController

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
    lc = LEDController(led)
    lc.start()

    def buttonListner(mode):
        printResult(mode)
        if mode is Button.NORMAL_PRESS:
            lc.blink(3, 0.5, 0.5)
        else:
            lc.blink(1, 3, 0)

    button.setListener(buttonListner)
    try:
        while True:
            button.loop()
    except KeyboardInterrupt:
        print("Cancel button-LED test")

    lc.stop()


print("Start test units. Use ctrl+c to stop current test.")

try:
    ledTest()
except KeyboardInterrupt:
    print("Cancel led test")

try:
    buttonTest()
except KeyboardInterrupt:
    print("Cancel button test")

    buttonLedTest()

# Cleanup GPIO settings
GPIO.cleanup()

print("All tests done")
