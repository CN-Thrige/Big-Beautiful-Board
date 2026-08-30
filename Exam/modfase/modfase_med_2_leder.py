from machine import Pin
from time import sleep

p1 = Pin(0, Pin.OUT)  # red
p0 = Pin(1, Pin.OUT)  # yellow

while True:
    p1.on()
    p0.off()
    sleep(0.5)

    p1.off()
    p0.on()
    sleep(0.5)
