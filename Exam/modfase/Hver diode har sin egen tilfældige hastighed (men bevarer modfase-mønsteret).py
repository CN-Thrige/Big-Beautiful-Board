from machine import Pin
from time import sleep
import random

p1 = Pin(0, Pin.OUT)
p0 = Pin(1, Pin.OUT)

while True:
    t1 = random.uniform(0.1, 0.8)
    t2 = random.uniform(0.1, 0.8)

    p1.on()
    p0.off()
    sleep(t1)

    p1.off()
    p0.on()
    sleep(t2)
