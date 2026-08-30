from machine import Pin
from time import sleep
import random

button1 = Pin(6, Pin.IN, Pin.PULL_UP)
p1 = Pin(0, Pin.OUT)  # red
p0 = Pin(1, Pin.OUT)  # yellow

def modfase():
    p1.on(); p0.off()
    sleep(0.5)
    p1.off(); p0.on()
    sleep(0.5)

def random_flimmer():
    p1.value(random.randint(0, 1))
    p0.value(random.randint(0, 1))
    sleep(random.uniform(0.05, 0.3))

while True:
    if button1.value() == 0:
        random_flimmer()
    else:
        modfase()
