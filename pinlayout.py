from machine import Pin
from time import sleep

u1 = Pin(6, Pin.IN, Pin.PULL_UP)
u2 = Pin(7, Pin.IN, Pin.PULL_UP)

d1 = Pin(0, Pin.OUT)
d2 = Pin(1, Pin.OUT)
d3 = Pin(2, Pin.OUT)

d4 = Pin(3, Pin.OUT)
d5 = Pin(4, Pin.OUT)
d6 = Pin(5, Pin.OUT)

state = 0 
