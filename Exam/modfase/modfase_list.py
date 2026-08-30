from machine import Pin
from time import sleep

leds = [Pin(0, Pin.OUT), Pin(1, Pin.OUT)]

state = True

while True:
    leds[0].value(state)
    leds[1].value(not state)
    state = not state
    sleep(0.5)
