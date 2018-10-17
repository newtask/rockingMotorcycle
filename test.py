from button import Button
import RPi.GPIO as GPIO

pinLED = 17
GPIO.setmode(GPIO.BCM)


def printResult(result):
    print("Result: {}".format(result))


# test button
def buttonTest():
    print("Start button test")

    pinBTN = 27

    button = Button(pinBTN)
    button.setListener(printResult)

    while True:
        button.loop()


buttonTest()
