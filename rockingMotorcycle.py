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
from lib.ledAnimations import TheaterChaseAnimation, LEDAnimation, RGBColor, FadeCycleAnimation, ColorSetAnimation
from lib.ledStrip import LEDStrip


class RockingMotorcycleGame:
    SOUND_START = "start"  # 11 sec
    SOUND_STOP = "stop"  # 6 sev
    SOUND_SPEEDUP = "speedUp"  # 13 sec
    SOUND_IDLE = "idle"  # 40 sec
    SOUND_DRIVE = "drive"  # 22 sec

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

        self.changeDelta = 1500
        self.currentMode = -1

        self.imuController = IMUController(imuAddress, limit=3000)
        self.initImuController()

        self.animDrive = TheaterChaseAnimation(LEDAnimation.COLOR_CYAN, 20, 50, 15, True)
        self.animIdle = FadeCycleAnimation(RGBColor(0, 0, 0), RGBColor(0, 80, 0), 25, 20)

        self.ledStrip = LEDStrip()
        self.ledStrip.start()

        self.speed = 0
        self.lastLoop = self.getMillis()

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

    def run(self):
        # indicate start
        self.ledControl.blink(2, 100, 100)

        while True:
            self.btn.loop()

            mode = self.getMode(self.imuChangeTime)

            accl = self.getAcceleration(mode, self.lastLoop)

            self.speed += accl

            if self.speed < 0:
                self.speed = 0
            elif self.speed > 100:
                self.speed = 100

            self.playLEDAnimation(mode, self.speed)

            self.playSound(mode)

            self.lastLoop = self.getMillis()

            self.currentMode = mode

            time.sleep(0.1)

    def mixerListener(self, id):
        return

    def playLEDAnimation(self, mode: int, speed: int):
        curAnim = self.ledStrip.getAnimation()

        if mode == self.MODE_START or speed <= 5:
            if curAnim != self.animIdle:
                self.ledStrip.setAnimation(self.animIdle)
        else:
            if curAnim is None or curAnim != self.animDrive:
                curAnim = self.animDrive
                self.ledStrip.setAnimation(curAnim)

            percentage = (100 - speed) / 100
            color = LEDAnimation.wheel(int(80 * (1 - percentage)))
            self.animDrive.update(color, int(10 + 200 * percentage), curAnim.iterations,
                                  curAnim.distance)

    def stop(self):
        self.mixer.stop()
        self.ledControl.stop()
        self.ledStrip.setAnimation(ColorSetAnimation(LEDAnimation.COLOR_BLACK))
        time.sleep(1)
        self.ledStrip.stop()
        self.imuController.stop()
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

    def getMode(self, imuChangeTime: int):
        if imuChangeTime == 0:
            return self.MODE_START
        elif self.getMillis() - imuChangeTime < self.changeDelta:
            return self.MODE_DRIVE
        else:
            return self.MODE_STOP

    def playSound(self, mode: int):

        if self.currentMode == mode:
            return

        self.mixer.clearQueue()

        if mode == self.MODE_START:
            self.mixer.playSound(self.SOUND_START, False, 0)
            self.mixer.queue(self.SOUND_IDLE, True)
        elif mode == self.MODE_DRIVE:
            self.mixer.playSound(self.SOUND_SPEEDUP, False)
            self.mixer.queue(self.SOUND_DRIVE, True)
        elif mode == self.MODE_STOP:
            self.mixer.playSound(self.SOUND_STOP, False)
            self.mixer.queue(self.SOUND_IDLE, True)

    def getAcceleration(self, mode: int, lastLoop: int):

        accl = 0

        if mode != self.MODE_START:
            # get time between loops
            diff = self.getMillis() - lastLoop

            speedChange = (diff / 1000) * 5  # 17 kmh per sec

            if mode == self.MODE_DRIVE:
                # decreases speed
                accl = speedChange

            elif mode == self.MODE_STOP:
                # increase speed
                accl -= 2 * speedChange

        return accl
