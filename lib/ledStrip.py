import threading
import time

from neopixel import *
from lib.ledAnimations import LEDAnimation


class LEDStrip(threading.Thread):
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10  # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

    def __init__(self, pin=21, ledCount=30):
        super(LEDStrip, self).__init__()

        self.LED_PIN = pin  # 10 spi  12 pwm GPIO pin connected to the pixels (18 uses PWM!).
        self.LED_COUNT = ledCount  # Number of LED pixels.
        self.isRunning = False
        self.animation = None

        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT,
                                       self.LED_BRIGHTNESS, self.LED_CHANNEL)

        # Initialize the library (must be called once before other functions).
        self.strip.begin()

    def start(self):
        print("Start")
        self.isRunning = True
        super(LEDStrip, self).start()

    def getAnimation(self):
        return self.animation

    def setAnimation(self, animation: LEDAnimation):
        print("Set animation", animation)

        if self.animation is not None:
            self.animation.stop()

        print("Start new animation")
        self.animation = animation
        self.animation.setStrip(self.strip)
        self.animation.start()

    def run(self):
        while self.isRunning:
            if self.animation is not None:
                self.animation.loop()
            else:
                time.sleep(0.1)

    def stop(self):
        if self.animation is not None:
            self.animation.stop()

        self.isRunning = False
