"""
type_a_digit.py

Type any digit 0-9 and it lights up on the 7-segment display.
Keeps asking until you press Ctrl-C.

Needs seven_segment_digits.py saved on the same Pico.
"""

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
        digit = get_int("Enter a digit to display (0-9): ", 0, 9)
        seg.show_digit(digit)
except KeyboardInterrupt:
    seg.clear()
    print("Stopped, display cleared.")
