from machine import Pin
from time import sleep

btn_up = Pin(6, Pin.IN, Pin.PULL_UP)
btn_down = Pin(7, Pin.IN, Pin.PULL_UP)

def wait_release(btn):
    while btn.value() == 0:
        sleep(0.05)

def main_floor():
    print("Floor: Main")
    while True:
        if btn_up.value() == 0:
            wait_release(btn_up)
            return second_floor
        sleep(0.05)

def second_floor():
    print("Floor: 2nd")
    while True:
        if btn_down.value() == 0:
            wait_release(btn_down)
            return main_floor
        sleep(0.05)

state = main_floor
while True:
    state = state()
