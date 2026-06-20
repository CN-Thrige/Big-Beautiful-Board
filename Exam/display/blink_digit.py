"""
blink_digit.py

Shows one digit, blinking on/off at a chosen frequency - same idea as
your LED PWM blink script, but applied to the 7-segment display. The
segments are wired straight to GPIO pins (not PWM), so this just
toggles them on and off in a loop instead of dimming.

Needs seven_segment_digits.py saved on the same Pico.
"""

from time import sleep
import seven_segment_digits as seg


def get_int(prompt, lo, hi):
    while True:
        try:
            val = int(input(prompt))
            if lo <= val <= hi:
                return val
            print(f"Enter a value between {lo} and {hi}.")
        except ValueError:
            print("Please type a whole number.")


digit = get_int("Digit to blink (0-9): ", 0, 9)
frequency = get_int("Blink frequency (1-10 Hz): ", 1, 10)
half_period = (1 / frequency) / 2

try:
    while True:
        seg.show_digit(digit)
        sleep(half_period)
        seg.clear()
        sleep(half_period)
except KeyboardInterrupt:
    seg.clear()
    print("Stopped, display cleared.")
