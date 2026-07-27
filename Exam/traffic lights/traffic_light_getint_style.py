from machine import Pin
from time import sleep

red = Pin(0, Pin.OUT)
yellow = Pin(1, Pin.OUT)
green = Pin(2, Pin.OUT)

def get_int(prompt, lo, hi):
    while True:
        try:
            val = int(input(prompt))
            if lo <= val <= hi:
                return val
            print(f"Enter a value between {lo} and {hi}.")
        except ValueError:
            print("Please type a whole number.")

green_time = get_int("Green time in seconds (1-30): ", 1, 30)
yellow_time = get_int("Yellow time in seconds (1-10): ", 1, 10)
red_time = get_int("Red time in seconds (1-30): ", 1, 30)

def all_off():
    red.off(); yellow.off(); green.off()

def state_green():
    all_off()
    green.on()
    sleep(green_time)
    return state_yellow

def state_yellow():
    all_off()
    yellow.on()
    sleep(yellow_time)
    return state_red

def state_red():
    all_off()
    red.on()
    sleep(red_time)
    return state_green

try:
    state = state_green
    while state:
        state = state()
except KeyboardInterrupt:
    all_off()
    print("Stopped, outputs cleared.")
