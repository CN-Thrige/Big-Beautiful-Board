"""
scroll_number.py

The display can only show one digit at a time, so to show a bigger
number (a score, a measurement, whatever) this scrolls through its
digits one at a time, left to right.

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


try:
    while True:
        number = get_int("Number to display (0-99999): ", 0, 99999)
        digits = [int(d) for d in str(number)]
        for d in digits:
            seg.show_digit(d)
            sleep(0.6)
        seg.clear()
        sleep(0.3)
except KeyboardInterrupt:
    seg.clear()
    print("Stopped, display cleared.")
