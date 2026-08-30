from machine import Pin
from time import sleep
import random

p1 = Pin(0, Pin.OUT)
p0 = Pin(1, Pin.OUT)

while True:
    antal_blink = random.randint(2, 6)

    for _ in range(antal_blink):
        p1.on(); p0.off()
        sleep(0.3)
        p1.off(); p0.on()
        sleep(0.3)

    p1.off()
    p0.off()
    sleep(random.uniform(1, 3))  # tilfældig pause mellem "serier"
