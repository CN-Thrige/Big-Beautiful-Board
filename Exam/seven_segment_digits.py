"""
seven_segment_digits.py

Module for driving the single 7-segment display on the Big Beautiful Board
(Raspberry Pi Pico WH). Import this from another program to show digits
0-9 without re-typing the pin and segment setup every time.

Segment -> GPIO pin map (matches the silkscreen / your working test code):
    A (top)           -> GPIO 12
    B (top right)     -> GPIO 13
    C (bottom right)  -> GPIO 14
    D (bottom)        -> GPIO 8
    E (bottom left)   -> GPIO 9
    F (top left)      -> GPIO 11
    G (middle)        -> GPIO 10
    DP (dot)          -> GPIO 15
"""

from machine import Pin

SEGMENT_PINS = {
    'A': Pin(12, Pin.OUT),
    'B': Pin(13, Pin.OUT),
    'C': Pin(14, Pin.OUT),
    'D': Pin(8, Pin.OUT),
    'E': Pin(9, Pin.OUT),
    'F': Pin(11, Pin.OUT),
    'G': Pin(10, Pin.OUT),
    'DP': Pin(15, Pin.OUT),
}

# Which segments must be ON to draw each digit, 0-9.
DIGITS = {
    0: ('A', 'B', 'C', 'D', 'E', 'F'),
    1: ('B', 'C'),
    2: ('A', 'B', 'D', 'E', 'G'),
    3: ('A', 'B', 'C', 'D', 'G'),
    4: ('B', 'C', 'F', 'G'),
    5: ('A', 'C', 'D', 'F', 'G'),
    6: ('A', 'C', 'D', 'E', 'F', 'G'),
    7: ('A', 'B', 'C'),
    8: ('A', 'B', 'C', 'D', 'E', 'F', 'G'),
    9: ('A', 'B', 'C', 'D', 'F', 'G'),
}


def clear():
    """Turn every segment, including the dot, off."""
    for pin in SEGMENT_PINS.values():
        pin.off()


def show_digit(number, dot=False):
    """Light up the segments needed to show `number` (0-9 only)."""
    if number not in DIGITS:
        raise ValueError("show_digit only accepts whole numbers 0-9")
    clear()
    for seg in DIGITS[number]:
        SEGMENT_PINS[seg].on()
    if dot:
        SEGMENT_PINS['DP'].on()


# Quick self-test: running this file directly (not importing it)
# flashes through 0-9 once, so you can check the wiring is right.
if __name__ == "__main__":
    from time import sleep
    for n in range(10):
        show_digit(n)
        sleep(0.5)
    clear()
