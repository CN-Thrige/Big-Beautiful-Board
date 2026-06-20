"""
seven_segment_hex.py

Extends seven_segment_digits.py to also show hexadecimal digits A-F
(values 10-15), so the display can show any single hex digit 0-F.

Needs seven_segment_digits.py saved on the same Pico.
"""

from seven_segment_digits import SEGMENT_PINS, DIGITS, clear

# Extra segment patterns for hex letters A-F, using the same letter
# names (A-G) as seven_segment_digits.py.
HEX_LETTERS = {
    10: ('A', 'B', 'C', 'E', 'F', 'G'),  # A
    11: ('C', 'D', 'E', 'F', 'G'),       # b
    12: ('A', 'D', 'E', 'F'),            # C
    13: ('B', 'C', 'D', 'E', 'G'),       # d
    14: ('A', 'D', 'E', 'F', 'G'),       # E
    15: ('A', 'E', 'F', 'G'),            # F
}

ALL_DIGITS = {**DIGITS, **HEX_LETTERS}


def show_hex_digit(value, dot=False):
    """Display one hex digit, value 0-15 (0-9 and A-F)."""
    if value not in ALL_DIGITS:
        raise ValueError("show_hex_digit only accepts whole numbers 0-15")
    clear()
    for seg in ALL_DIGITS[value]:
        SEGMENT_PINS[seg].on()
    if dot:
        SEGMENT_PINS['DP'].on()


# Quick self-test: cycles 0-F once if this file is run directly.
if __name__ == "__main__":
    from time import sleep
    for n in range(16):
        show_hex_digit(n)
        sleep(0.5)
    clear()
