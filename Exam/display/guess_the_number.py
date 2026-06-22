"""
guess_the_number.py

Small game: the Pico picks a secret digit 0-9, you guess via the serial
console, each guess shows on the display, and you get a higher/lower
hint until you find it. Display flashes when you're right.

Needs seven_segment_digits.py saved on the same Pico.
"""

import random
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


secret = random.randint(0, 9)
print("I'm thinking of a digit between 0 and 9. Guess it!")

try:
    while True:
        guess = get_int("Your guess (0-9): ", 0, 9)
        seg.show_digit(guess)
        if guess == secret:
            print("Correct!")
            for _ in range(6):
                seg.show_digit(8, dot=True)
                sleep(0.2)
                seg.clear()
                sleep(0.2)
            secret = random.randint(0, 9)
            print("New round! Guess again.")
        elif guess < secret:
            print("Higher!")
        else:
            print("Lower!")
except KeyboardInterrupt:
    seg.clear()
    print("Stopped, display cleared.")
