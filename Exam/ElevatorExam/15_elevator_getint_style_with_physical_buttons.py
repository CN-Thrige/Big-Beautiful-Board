from machine import Pin
from time import sleep

btn_up = Pin(6, Pin.IN, Pin.PULL_UP)
btn_down = Pin(7, Pin.IN, Pin.PULL_UP)

def get_int(prompt, lo, hi):
    while True:
        try:
            val = int(input(prompt))
            if lo <= val <= hi:
                return val
            print(f"Enter a value between {lo} and {hi}.")
        except ValueError:
            print("Please type a whole number.")

debounce_ms = get_int("Button debounce time in ms (50-500): ", 50, 500)
debounce_s = debounce_ms / 1000

def wait_release(btn):
    while btn.value() == 0:
        sleep(0.02)
    sleep(debounce_s)

def main_floor():
    print("Floor: Main")
    while True:
        if btn_up.value() == 0:
            wait_release(btn_up)
            return second_floor
        sleep(0.02)

def second_floor():
    print("Floor: 2nd")
    while True:
        if btn_down.value() == 0:
            wait_release(btn_down)
            return main_floor
        sleep(0.02)

try:
    state = main_floor
    while state:
        state = state()
except KeyboardInterrupt:
    print("Stopped.")
