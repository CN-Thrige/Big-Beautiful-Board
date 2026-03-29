from machine import Pin
from time import sleep

button1 = Pin(6, Pin.IN, Pin.PULL_UP)
button2 = Pin(7, Pin.IN, Pin.PULL_UP)

ledrL = Pin(0, Pin.OUT)
ledgL = Pin(2, Pin.OUT)
ledyL = Pin(1, Pin.OUT)

ledrR = Pin(3, Pin.OUT)
ledyR = Pin(4, Pin.OUT)
ledgR = Pin(5, Pin.OUT)

while True:
    if button1.value() == 1:
        ledgR.off()
        ledyR.off()
        ledrR.off()

    if button1.value() == 0:
        ledgR.on()
        ledyR.on()
        ledrR.on()

    if button2.value() == 1:
        ledgL.off()
        ledyL.off()
        ledrL.off()

    if button2.value() == 0:
        ledgL.on()
        ledyL.on()
        ledrL.on()