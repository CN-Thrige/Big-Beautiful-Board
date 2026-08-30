from machine import Pin
from time import sleep

p1 = Pin(0, Pin.OUT)
p0 = Pin(1, Pin.OUT)

state = 0  # 0 eller 1

while True:
    p1.value(state)
    p0.value(not state)   # altid det modsatte af p1
    state = not state
    sleep(0.5)
