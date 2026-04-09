
from machine import Pin
from time import sleep

time = 2

button1 = Pin(6, Pin.IN, Pin.PULL_UP)
button2 = Pin(7, Pin.IN, Pin.PULL_UP)

ledRL = Pin(0, Pin.OUT)
ledYL = Pin(1, Pin.OUT)
ledGL = Pin(2, Pin.OUT)

ledRR = Pin(3, Pin.OUT)
ledYR = Pin(4, Pin.OUT)
ledGR = Pin(5, Pin.OUT)


def  main():
    # variable

    while True:
        if button1.value() == 0:
            green()

        if button1.value() == 0:
            yellow()


        if button1.value() == 0:
            red()

def green():
    ledGR.on()
    sleep(1)
    ledGR.off()

def yellow ():
    ledYR.on()
    sleep(1)
    ledYR.off()

def red():
    ledRR.on()
    sleep(1)
    ledRR.off()

main()
