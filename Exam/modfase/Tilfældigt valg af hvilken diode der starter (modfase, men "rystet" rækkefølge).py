from machine import Pin
from time import sleep
import random

p1 = Pin(0, Pin.OUT)
p0 = Pin(1, Pin.OUT)

while True:
    if random.choice([True, False]):
        p1.on(); p0.off()
    else:
        p1.off(); p0.on()

    sleep(0.5)
