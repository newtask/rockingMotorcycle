#!/usr/bin/python3

import time

import RPi.GPIO as GPIO

from controller.imuController import IMUController
from controller.ledController import LEDController
from controller.lsmController import LSMController
from lib.LSM6DS3 import LSM6DS3
from lib.LSM6DS3_ALT import LSM6DS3_alt
from lib.audio import Audio
from lib.audioMixer import AudioMixer
from lib.button import Button
from lib.led import LED
from lib.ledAnimations import TheaterChaseAnimation, LEDAnimation, ColorWipeAnimation, RainbowAnimation, \
    RainbowCycleAnimation, TheaterChaseRainbowAnimation, ColorSetAnimation, FadeAnimation, RGBColor, FadeCycleAnimation
from lib.ledStrip import LEDStrip

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


    animations.append(ColorSetAnimation(LEDAnimation.COLOR_BLACK))
    animations.append(TheaterChaseAnimation(LEDAnimation.COLOR_YELLOW, 100, 50, 15, True))
    animations.append(TheaterChaseAnimation(LEDAnimation.COLOR_CYAN, 100, 50, 15))


    animations.append(TheaterChaseAnimation(LEDAnimation.COLOR_BLUE, 500, 10, 15))
    animations.append(TheaterChaseAnimation(LEDAnimation.COLOR_GREEN, 50, 10, 15))
    animations.append(TheaterChaseAnimation(LEDAnimation.COLOR_RED, 50, 50, 15))
    animations.append(TheaterChaseAnimation(LEDAnimation.COLOR_MAGENTA, 20, 50, 15))
    animations.append(TheaterChaseAnimation(LEDAnimation.COLOR_CYAN, 20, 50, 15))
    animations.append(TheaterChaseAnimation(LEDAnimation.COLOR_YELLOW, 20, 100, 15))
    animations.append(FadeCycleAnimation(RGBColor(0, 0, 0), RGBColor(255, 255, 255), 25, int(1000 / 200)))
    animations.append(FadeAnimation(RGBColor(255, 0, 0), RGBColor(0, 255, 0), 50, int(1000 / 50)))
    animations.append(FadeAnimation(RGBColor(0, 255, 0), RGBColor(0, 0, 255), 50, int(1000 / 50)))
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


def imuTest():
    print("Start imu test")
    lsm = LSM6DS3(0x6a)
    try:
        while True:
            acclX = lsm.readRawAccelX()
            acclY = lsm.readRawAccelX()
            acclZ = lsm.readRawAccelX()
            gyroX = lsm.readRawGyroX()
            gyroY = lsm.readRawGyroY()
            gyroZ = lsm.readRawGyroZ()
            print("accl {} ".format((acclX, acclY, acclZ)))
            print("gyro {} ".format((gyroX, gyroY, gyroZ)))
            print("angle {} {}".format(lsm.calcAnglesXY(), lsm.calcGyroXAngle()))

            time.sleep(0.2)
    except KeyboardInterrupt:
        print("Cancel imu test")


def imuTestAlt():
    print("Start imu test")
    lsm_alt = LSM6DS3_alt(0x6a)
    try:
        while True:
            accl = lsm_alt.accel.xyz()
            gyro = lsm_alt.gyro.xyz()
            print("acclx {} ".format(accl))
            print("gyro {} ".format(gyro))
            # print("temp {} ".format(lsm_alt.temperature()))

            time.sleep(0.2)
    except KeyboardInterrupt:
        print("Cancel imu test")


def imuControllerTest():
    print("Start imu controller test")

    def onChange():
        print("has changed")

    imuController = IMUController(0x6a, limit=1000)
    imuController.setListener(onChange)
    imuController.start()

    try:
        while True:
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("Cancel imu controller test")


def audioTest():
    print("Start audio test")
    audio = Audio(70)

    def onPressed(mode):
        vol = audio.getVolume()
        if mode is Button.NORMAL_PRESS:
            if vol == 100:
                audio.setVolume(70)
            else:
                audio.volumeUp()

        else:
            if audio.isMute:
                audio.unmute()
            else:
                audio.mute()

        print("volume {}".format(audio.getVolume()))

    btn = Button(pinBTN)
    btn.setListener(onPressed)

    try:
        print(audio.getVolume())
        print(audio.setVolume(20))
        print(audio.getVolume())

        while True:
            btn.loop()
    except KeyboardInterrupt:
        print("Cancel audio test")


def lsm303dTest():
    import time
    from lsm303d import LSM303D

    lsm = LSM303D(0x1d)


    while True:
        t = lsm.temperature()
        m = lsm.magnetometer()
        a = lsm.accelerometer()
        # t_raw = lsm._lsm303d.values['TEMPERATURE']
        # print("{:04.1f} {:016b}".format(t, t_raw))

        values = list(m) + list(a)

        print(("{:+06.2f} : {:+06.2f} : {:+06.2f}   " * 2).format(*values))
        # print(("{:+06.2f} : {:+06.2f} : {:+06.2f}   " ).format(*a))
        # print(a)

        time.sleep(1.0 / 25)

def lsmControllerTest():
    def onChanged():
        print("changed")

    lsm = LSMController(limit=0.2)
    lsm.setListener(onChanged)
    lsm.start()



def audioMixerTest():
    print("Start audio mixer test")

    import os
    from os import path

    appPath = os.path.dirname(os.path.abspath(__file__))
    audioFolder = path.join(appPath, "audio")

    audio = Audio(70)
    mixer = AudioMixer()
 
    mixer.addSound("start", path.join(audioFolder, "h_start.wav"))
    mixer.addSound("stop", path.join(audioFolder, "h_stop.wav"))
    mixer.addSound("speedUp", path.join(audioFolder, "h_speedup.wav"))
    mixer.addSound("idle", path.join(audioFolder, "h_idle.wav"))
    mixer.addSound("drive", path.join(audioFolder, "h_drive.wav"))


    def onPressed(mode):
        if mode is Button.NORMAL_PRESS:
            mixer.clearQueue()
            mixer.playSound("speedUp", False, 300)
            mixer.queue("drive", True)
        else:
            mixer.clearQueue()
            mixer.playSound("stop", False, 300)
            mixer.queue("idle", True)

    btn = Button(pinBTN)
    btn.setListener(onPressed)

    mixer.playSound("start", False, 0)
    mixer.queue("idle", True)

    try:
        while True:
            btn.loop()
    except KeyboardInterrupt:
        print("Cancel audio mixer test")

    mixer.stop()


print("Start test units. Use ctrl+c to stop current test.")

# audioTest()
# audioMixerTest()
# ledStripTest()
lsmControllerTest()
# lsm303dTest()
#
#imuControllerTest()
# imuTest()
# imuTestAlt()
# ledTest()
# buttonTest()
# buttonLedTest()

# Cleanup GPIO settings
GPIO.cleanup()

print("All tests done")
