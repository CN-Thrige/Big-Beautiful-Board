"""
cycle_demo.py

Loops the display through 0-9 over and over. Handy as a quick wiring
check or just a demo running in the background. Speed is adjustable.

Needs seven_segment_digits.py saved on the same Pico.
"""

from time import sleep
import seven_segment_digits as seg


def get_float(prompt, lo, hi):
    while True:
        try:
            val = float(input(prompt))
            if lo <= val <= hi:
                return val
            print(f"Enter a value between {lo} and {hi}.")
        except ValueError:
            print("Please type a number.")


delay = get_float("Seconds between digits (0.1-2.0): ", 0.1, 2.0)

try:
    while True:
        for n in range(10):
            seg.show_digit(n)
            sleep(delay)
except KeyboardInterrupt:
    seg.clear()
    print("Stopped, display cleared.")
