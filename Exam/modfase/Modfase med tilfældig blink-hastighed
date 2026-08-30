from machine import Pin
from time import sleep
import random

p1 = Pin(0, Pin.OUT)  # red
p0 = Pin(1, Pin.OUT)  # yellow

while True:
    ventetid = random.uniform(0.2, 1.0)  # tilfældig tid mellem 0.2 og 1.0 sek

    p1.on()
    p0.off()
    sleep(ventetid)

    p1.off()
    p0.on()
    sleep(ventetid)
