from machine import Pin
from time import sleep

red = Pin(0, Pin.OUT)
yellow = Pin(1, Pin.OUT)
green = Pin(2, Pin.OUT)

def all_off():
    red.off(); yellow.off(); green.off()

def state_green():
    all_off()
    green.on()
    sleep(5.5)
    return state_yellow

def state_yellow():
    all_off()
    yellow.on()
    sleep(1.5)
    return state_red

def state_red():
    all_off()
    red.on()
    sleep(5.5)
    return state_green

state = state_green
while state:
    state = state()
