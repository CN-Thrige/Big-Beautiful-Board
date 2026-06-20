"""
countdown.py

Rocket launcher countdown, shown on the 7-segment display instead of
printed to the screen (per the exam brief).

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


start = get_int("Countdown start (0-9): ", 0, 9)
step_seconds = get_int("Seconds per count (1-5): ", 1, 5)

try:
    for n in range(start, -1, -1):
        seg.show_digit(n)
        print(n)
        sleep(step_seconds)

    # Lift-off: flash all segments + dot a few times
    for _ in range(6):
        seg.show_digit(8, dot=True)
        sleep(0.2)
        seg.clear()
        sleep(0.2)
    print("Lift off!")

except KeyboardInterrupt:
    seg.clear()
    print("Stopped, display cleared.")
