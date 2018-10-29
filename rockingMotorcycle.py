'''
Game for a awesome rocking motorcycle with lights, sound and motionsensor
'''
import time
from os import path

import RPi.GPIO as GPIO

from controller.imuController import IMUController
from controller.ledController import LEDController
from lib.audio import Audio
from lib.audioMixer import AudioMixer
from lib.button import Button
from lib.led import LED
from lib.ledAnimations import TheaterChaseAnimation, LEDAnimation, RGBColor, FadeCycleAnimation, RainbowCycleAnimation
from lib.ledStrip import LEDStrip


class RockingMotorcycleGame:
    SOUND_START = "start"
    SOUND_STOP = "stop"
    SOUND_SPEEDUP = "speedUp"
    SOUND_IDLE = "idle"
    SOUND_DRIVE = "drive"

    MODE_START = 0
    MODE_DRIVE = 1
    MODE_STOP = 2

    LED_SPEED = 100

    def __init__(self, pinBTN=27, pinLED=17, startVolume=70, imuAddress=0x6a):
        GPIO.setmode(GPIO.BCM)

        led = LED(pinLED)

        self.ledStrip = LEDStrip()
        self.audio = Audio(startVolume)

        self.mixer = AudioMixer()
        self.initAudioMixer()

        self.btn = Button(pinBTN)
        self.btn.setListener(self.audioBtnListener)

        self.ledControl = LEDController(led)
        self.ledControl.start()

        self.changeDelta = 3000
        self.currentMode = -1

        self.imuController = IMUController(imuAddress, limit=3000)
        self.initImuController()

        self.animSlow = TheaterChaseAnimation(LEDAnimation.COLOR_GREEN, 250, 10, 15)
        self.animMedium = TheaterChaseAnimation(LEDAnimation.COLOR_BLUE, 50, 50, 15)
        self.animFast = TheaterChaseAnimation(LEDAnimation.COLOR_RED, 20, 50, 15)
        self.animFade = FadeCycleAnimation(RGBColor(0, 0, 0), RGBColor(80, 80, 80), 25, 20)
        self.animRainbow = RainbowCycleAnimation()

        self.ledStrip = LEDStrip()
        self.ledStrip.start()

    def initImuController(self):
        self.imuChangeTime = 0
        self.imuController.setListener(self.imuListener)
        self.imuController.start()

    def initAudioMixer(self):
        appPath = path.dirname(path.abspath(__file__))
        audioFolder = path.join(appPath, "audio")

        self.mixer.addSound(self.SOUND_START, path.join(audioFolder, "h_start.wav"))
        self.mixer.addSound(self.SOUND_STOP, path.join(audioFolder, "h_stop.wav"))
        self.mixer.addSound(self.SOUND_SPEEDUP, path.join(audioFolder, "h_speedup.wav"))
        self.mixer.addSound(self.SOUND_IDLE, path.join(audioFolder, "h_idle.wav"))
        self.mixer.addSound(self.SOUND_DRIVE, path.join(audioFolder, "h_drive.wav"))

        self.mixer.setListener(self.mixerListener)

    def mixerListener(self, id):
        if id == self.SOUND_START:
            self.ledStrip.setAnimation(self.animRainbow)
        elif id == self.SOUND_IDLE:
            self.ledStrip.setAnimation(self.animFade)
        elif id == self.SOUND_DRIVE:
            self.ledStrip.setAnimation(self.animFast)
        elif id == self.SOUND_SPEEDUP:
            self.ledStrip.setAnimation(self.animSlow)
        elif id == self.SOUND_STOP:
            self.ledStrip.setAnimation(self.animMedium)

    def stop(self):
        self.mixer.stop()
        self.ledControl.stop()
        self.ledStrip.stop()
        GPIO.cleanup()

    def imuListener(self):
        self.imuChangeTime = self.getMillis()

    def getMillis(self):
        return int(round(time.time() * 1000))

    def audioBtnListener(self, mode):
        vol = self.audio.getVolume()

        if mode is Button.NORMAL_PRESS:
            if vol == 100:
                self.audio.setVolume(70)
                vol = 70
            else:
                vol = self.audio.volumeUp()

        else:
            if self.audio.isMute:
                vol = self.audio.unmute()
            else:
                self.audio.mute()
                vol = 0

        if vol >= 70:
            self.ledControl.blink(int(vol / 10) - 6, self.LED_SPEED, self.LED_SPEED)
        else:
            self.ledControl.blink(1, 1000, self.LED_SPEED)

    def run(self):
        # indicate start
        self.ledControl.blink(2, 100, 100)

        # Start the engine
        self.setMode(self.MODE_START)

        while True:
            self.btn.loop()

            if self.imuChangeTime == 0:
                pass
            elif self.getMillis() - self.imuChangeTime < self.changeDelta:
                self.setMode(self.MODE_DRIVE)
            else:
                self.setMode(self.MODE_STOP)

            time.sleep(0.1)

    def setMode(self, mode: int):

        if self.currentMode == mode:
            return

        print("set mode: {}".format(mode))

        self.mixer.clearQueue()

        if mode == self.MODE_START:
            self.mixer.playSound(self.SOUND_START, False, 0)
            self.mixer.queue(self.SOUND_IDLE, True)
            # self.ledStrip.setAnimation(self.animSlow)
        elif mode == self.MODE_DRIVE:
            self.mixer.playSound(self.SOUND_SPEEDUP, False, 0)
            self.mixer.queue(self.SOUND_DRIVE, True)
            # self.ledStrip.setAnimation(self.animFast)
        elif mode == self.MODE_STOP:
            self.mixer.playSound(self.SOUND_STOP, False, 0)
            self.mixer.queue(self.SOUND_IDLE, True)
            # self.ledStrip.setAnimation(self.animMedium)

        self.currentMode = mode
