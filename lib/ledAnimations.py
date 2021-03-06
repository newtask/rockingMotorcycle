import time

from neopixel import *


class RGBColor():
    def __init__(self, r, g, b, w=0):
        self.r = r
        self.g = g
        self.b = b
        self.w = w

    def toColor(self):
        return Color(self.g, self.r, self.b, self.w)


class LEDAnimation:
    COLOR_GREEN = Color(255, 0, 0)  # green, red, blue
    COLOR_RED = Color(0, 255, 0)
    COLOR_BLUE = Color(0, 0, 255)
    COLOR_MAGENTA = Color(0, 255, 255)
    COLOR_YELLOW = Color(255, 255, 0)
    COLOR_CYAN = Color(255, 0, 255)

    COLOR_WHITE = Color(255, 255, 255)
    COLOR_BLACK = Color(0, 0, 0)

    def __init__(self, name="LEDAnimation", wait_ms=50):
        self.name = name
        self.isRunning = False
        self.isStopped = True
        self.wait_ms = wait_ms
        self.strip = None

    @staticmethod
    def wheel(pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(255 - pos * 3, pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(0, 255 - pos * 3, pos * 3)
        else:
            pos -= 170
            return Color(pos * 3, 0, 255 - pos * 3)

    def isValid(self):
        return self.isStopped is False and self.strip is not None

    def loop(self):
        if self.isValid() is False:
            return

        self.isRunning = True

        print("loop")
        self.setColor(self.COLOR_WHITE)
        time.sleep(1)
        self.setColor(self.COLOR_BLACK)
        time.sleep(1)

        self.isRunning = False

    def setStrip(self, strip: Adafruit_NeoPixel):
        self.strip = strip

    def stop(self):
        self.isStopped = True

        while self.isRunning:
            time.sleep(0.1)

    def start(self):
        self.isStopped = False

    def setColor(self, color):
        for i in range(self.strip.numPixels()):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, color)
                self.strip.show()

    def __str__(self):
        return self.name


class FadeAnimation(LEDAnimation):

    def __init__(self, c1, c2, iterations: int = 10, wait_ms: int = 50):
        super().__init__("Fade", wait_ms)

        self.iterations = iterations
        self.c1 = c1
        self.c2 = c2

    def fade(self, c1, c2):
        for i in range(1, self.iterations + 1):

            if self.isStopped:
                break

            color = self.calcColor(c1, c2, i)
            for j in range(self.strip.numPixels()):
                self.strip.setPixelColor(j, color)
            self.strip.show()

            time.sleep(self.wait_ms / 1000.0)

    def loop(self):
        if self.isValid() is False:
            return

        self.isRunning = True

        print("fade")

        self.fade(self.c1, self.c2)

        self.isRunning = False

    def calcColor(self, c1, c2, i):
        r = int(((c1.r * (self.iterations - i)) + (c2.r * i)) / self.iterations)
        g = int(((c1.g * (self.iterations - i)) + (c2.g * i)) / self.iterations)
        b = int(((c1.b * (self.iterations - i)) + (c2.b * i)) / self.iterations)
        w = int(((c1.w * (self.iterations - i)) + (c2.w * i)) / self.iterations)

        return Color(g, r, b, w)


class FadeCycleAnimation(FadeAnimation):

    def __init__(self, c1, c2, iterations: int = 10, wait_ms: int = 50):
        super().__init__(c1, c2, iterations, wait_ms)

        self.name = "Fade cycle"

    def loop(self):
        if self.isValid() is False:
            return

        self.isRunning = True

        # print("fad cyclee")

        self.fade(self.c1, self.c2)
        self.fade(self.c2, self.c1)

        self.isRunning = False


class ColorSetAnimation(LEDAnimation):
    def __init__(self, color: Color, wait_ms: int = 50):
        super().__init__("Color set", wait_ms)

        self.color = color

    def loop(self):
        if self.isValid() is False:
            return

        self.isRunning = True

        # print("color", self.color)

        self.setColor(self.color)
        time.sleep(1)

        self.isRunning = False


class TheaterChaseAnimation(LEDAnimation):
    def __init__(self, color: Color, wait_ms: int = 50, iterations: int = 10, distance: int = 3, splitAndInvert=False):
        super().__init__("Theater Chase", wait_ms)

        self.splitAndInvert = splitAndInvert
        self.update(color, wait_ms, iterations, distance)

    def update(self, color: Color, wait_ms: int, iterations: int, distance: int):
        self.wait_ms = wait_ms
        self.color = color
        self.iterations = iterations
        self.distance = distance

    def loop(self):
        if self.isValid() is False:
            return

        self.isRunning = True

        # print("theaterChase")

        """Movie theater light style chaser animation."""
        for j in range(self.iterations):
            if self.isStopped:
                break

            for q in range(self.distance):
                if self.isStopped:
                    break

                numPixels = self.strip.numPixels()

                if self.splitAndInvert is False:
                    for i in range(0, numPixels, self.distance):
                        self.strip.setPixelColor(i + q, self.color)
                else:
                    halfNumPixels = int(numPixels / 2)

                    for i in range(0, halfNumPixels, self.distance):
                        self.strip.setPixelColor(i + q, self.color)
                    for i in range(numPixels, halfNumPixels, -self.distance):
                        self.strip.setPixelColor(numPixels - (numPixels - i + q) - 1, self.color)

                self.strip.show()

                time.sleep(self.wait_ms / 1000.0)

                if self.splitAndInvert is False:
                    for i in range(0, self.strip.numPixels(), self.distance):
                        self.strip.setPixelColor(i + q, 0)
                else:
                    halfNumPixels = int(numPixels / 2)

                    for i in range(0, halfNumPixels, self.distance):
                        self.strip.setPixelColor(i + q, 0)
                    for i in range(numPixels, halfNumPixels, -self.distance):
                        self.strip.setPixelColor(numPixels - (numPixels - i + q) - 1, 0)

        self.isRunning = False


class TheaterChaseRainbowAnimation(LEDAnimation):
    def __init__(self, wait_ms: int = 50, iterations: int = 10):
        super().__init__("Theater Chase Rainbow", wait_ms)

        self.iterations = iterations

    def loop(self):
        if self.isValid() is False:
            return

        self.isRunning = True

        # print("theaterChaseRainbow")

        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                if self.isStopped:
                    break

                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, self.wheel((i + j) % 255))
                self.strip.show()

                time.sleep(self.wait_ms / 1000.0)

                if self.isStopped:
                    break

                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

        self.isRunning = False


class RainbowAnimation(LEDAnimation):
    def __init__(self, wait_ms: int = 50, iterations: int = 10):
        super().__init__("Reainbow", wait_ms)

        self.iterations = iterations

    def loop(self):
        if self.isValid() is False:
            return

        self.isRunning = True

        # print("rainbow")

        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * self.iterations):
            if self.isStopped:
                break

            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i + j) & 255))
                self.strip.show()

            time.sleep(self.wait_ms / 1000.0)

        self.isRunning = False


class RainbowCycleAnimation(LEDAnimation):
    def __init__(self, wait_ms: int = 50, iterations: int = 10):
        super().__init__("Reainbow cycle", wait_ms)

        self.iterations = iterations

    def loop(self):
        if self.isValid() is False:
            return

        self.isRunning = True

        # print("rainbowCycle")

        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256 * self.iterations):
            if self.isStopped:
                break

            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))

            self.strip.show()
            time.sleep(self.wait_ms / 1000.0)

        self.isRunning = False


class ColorWipeAnimation(LEDAnimation):
    def __init__(self, color: Color, wait_ms: int = 50, iterations: int = 10):
        super().__init__("Color wipe", wait_ms)

        self.color = color

    def loop(self):

        if self.isValid() is False:
            return

        self.isRunning = True

        # print("colorWipe")

        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            if self.isStopped:
                break

            self.strip.setPixelColor(i, self.color)
            self.strip.show()

            time.sleep(self.wait_ms / 1000.0)

        self.isRunning = False
