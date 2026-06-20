

from machine import Pin
from time import sleep

button1 = Pin(6, Pin.IN, Pin.PULL_UP)

p1 = Pin(0, Pin.OUT)  #red
p0 = Pin(1, Pin.OUT) #yellow



while True:
    if button1.value() == 0:
        p0.on()
        sleep(0.5)
        p0.off()

        p1.on()
        sleep(0.5)
        p1.off()
