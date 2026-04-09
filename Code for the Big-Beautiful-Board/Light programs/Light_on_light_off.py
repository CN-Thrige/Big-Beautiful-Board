
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
            green_r()

        if button1.value() == 0:
            yellow_r()


        if button1.value() == 0:
            red_r()
            
        if button2.value() == 0:
            green_l()

        if button2.value() == 0:
            yellow_l()

        if button2.value() == 0:
            red_l()

def green_r():
    ledGR.on()
    sleep(0.5)
    ledGR.off()

def yellow_r ():
    ledYR.on()
    sleep(0.5)
    ledYR.off()

def red_r():
    ledRR.on()
    sleep(0.5)
    ledRR.off()
    

def green_l():
    ledGL.on()
    sleep(0.5)
    ledGL.off()

def yellow_l():
    ledYL.on()
    sleep(0.5)
    ledYL.off()

def red_l():
    ledRL.on()
    sleep(0.5)
    ledRL.off()



main()
