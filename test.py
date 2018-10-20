#!/usr/bin/python3

import time

import RPi.GPIO as GPIO

from button import Button
from led import LED
from ledController import LEDController
from ledStrip import LEDStrip, TheaterChaseAnimation, LEDAnimation, ColorWipeAnimation, RainbowAnimation, \
    RainbowCycleAnimation, TheaterChaseRainbowAnimation, ColorSetAnimation

GPIO.setmode(GPIO.BCM)

pinLED = 17
pinBTN = 27


def printResult(result):
    print("Result: {}".format(result))


def ledTest():
    print("Start LED test")

    led = LED(pinLED)
    led.setListener(printResult)
    try:

        while True:
            led.on()
            time.sleep(1)
            led.off()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Cancel led test")


def buttonTest():
    print("Start button test")

    button = Button(pinBTN)
    button.setListener(printResult)
    try:

        while True:
            button.loop()
    except KeyboardInterrupt:
        print("Cancel button test")


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


animIndex = -1


def ledStripTest():
    print("Start led strip test")
    ledStrip = LEDStrip()

    animations = []
    animations.append(RainbowAnimation())
    animations.append(TheaterChaseAnimation(LEDAnimation.COLOR_WHITE))
    animations.append(ColorWipeAnimation(LEDAnimation.COLOR_RED))
    animations.append(RainbowCycleAnimation())
    animations.append(TheaterChaseRainbowAnimation())
    animations.append(ColorSetAnimation(LEDAnimation.COLOR_BLACK))

    ledStrip.start()

    def setNextAnimation():
        global animIndex
        animIndex += 1
        if animIndex >= len(animations):
            animIndex = 0

        a = animations[animIndex]
        ledStrip.setAnimation(a)

    def onButtonClick(mode):
        if mode is Button.NORMAL_PRESS:
            setNextAnimation()

        else:
            a = ColorWipeAnimation(LEDAnimation.COLOR_BLACK)
            ledStrip.setAnimation(a)

    button = Button(pinBTN)
    button.setListener(onButtonClick)
    setNextAnimation()

    try:
        while True:
            button.loop()
    except KeyboardInterrupt:
        print("Cancel button-LED test")

    ledStrip.stop()


print("Start test units. Use ctrl+c to stop current test.")

ledStripTest()
# ledTest()
# buttonTest()
# buttonLedTest()

# Cleanup GPIO settings
GPIO.cleanup()

print("All tests done")
