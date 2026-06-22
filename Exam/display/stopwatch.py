"""
stopwatch.py

Counts elapsed whole seconds and shows the ones digit (0-9, wraps after 9)
on the display. Uses time.ticks_ms()/ticks_diff() instead of just sleep(),
so the count stays accurate even though show_digit() itself takes a little
time to run - sleep()-only timing would slowly drift.

Needs seven_segment_digits.py saved on the same Pico.
"""

from time import ticks_ms, ticks_diff, sleep
import seven_segment_digits as seg

start = ticks_ms()
last_shown = -1
elapsed_seconds = 0

try:
    while True:
        elapsed_seconds = ticks_diff(ticks_ms(), start) // 1000
        digit = elapsed_seconds % 10
        if digit != last_shown:
            seg.show_digit(digit)
            print(elapsed_seconds)
            last_shown = digit
        sleep(0.05)  # check often without hammering the CPU
except KeyboardInterrupt:
    seg.clear()
    print(f"Stopped after {elapsed_seconds} seconds, display cleared.")
