from machine import Pin
from random import random
from time import sleep

led0 = Pin(0, Pin.OUT)
led1 = Pin(1, Pin.OUT)
led2 = Pin(2, Pin.OUT)

def all_off():
    led0.off(); led1.off(); led2.off()

def state0():
    all_off(); led0.on()
    sleep(1)
    return state1 if random() >= 0.5 else state2

def state1():
    all_off(); led1.on()
    sleep(1)
    return state0 if random() >= 0.5 else state2

def state2():
    all_off(); led2.on()
    sleep(1)
    if random() < 0.5:
        return None
    return state0

state = state0
while state:
    state = state()

all_off()
print("Stop")
