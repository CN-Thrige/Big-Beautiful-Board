from machine import Pin
from random import random
from time import sleep

led0 = Pin(0, Pin.OUT)
led1 = Pin(1, Pin.OUT)
led2 = Pin(2, Pin.OUT)

def get_int(prompt, lo, hi):
    while True:
        try:
            val = int(input(prompt))
            if lo <= val <= hi:
                return val
            print(f"Enter a value between {lo} and {hi}.")
        except ValueError:
            print("Please type a whole number.")

step_time = get_int("Seconds per state (1-5): ", 1, 5)
stop_chance_pct = get_int("Chance to stop at State2, in % (0-100): ", 0, 100)
stop_threshold = stop_chance_pct / 100

def all_off():
    led0.off(); led1.off(); led2.off()

def state0():
    all_off(); led0.on()
    sleep(step_time)
    return state1 if random() >= 0.5 else state2

def state1():
    all_off(); led1.on()
    sleep(step_time)
    return state0 if random() >= 0.5 else state2

def state2():
    all_off(); led2.on()
    sleep(step_time)
    if random() < stop_threshold:
        return None
    return state0

try:
    state = state0
    while state:
        state = state()
    all_off()
    print("Stopped at State2.")
except KeyboardInterrupt:
    all_off()
    print("Stopped, outputs cleared.")
