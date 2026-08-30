from machine import Pin
from time import sleep
import random

p1 = Pin(0, Pin.OUT)
p0 = Pin(1, Pin.OUT)

state = 0

while True:
    if random.random() > 0.1:  # 90% chance for normalt skift
        state = not state

    p1.value(state)
    p0.value(not state)
    sleep(0.5)
