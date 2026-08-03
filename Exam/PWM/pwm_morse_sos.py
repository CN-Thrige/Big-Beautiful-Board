from machine import Pin, PWM
from time import sleep

ledRL = PWM(Pin(0))   # red left

PWM_CARRIER = 1000   # fixed internal switching freq, used only for dimming
ledRL.freq(PWM_CARRIER)

FULL = 65535
OFF = 0

DOT = 0.2               # length of one "dot" unit, in seconds
DASH = DOT * 3           # a dash is 3 dots long
GAP_SYMBOL = DOT         # gap between dot/dash within the same letter
GAP_LETTER = DOT * 3     # gap between letters (S, O, S)
GAP_WORD = DOT * 7       # gap after the whole word, before repeating

# S = ... , O = ---
PATTERN = [
    [DOT, DOT, DOT],       # S
    [DASH, DASH, DASH],    # O
    [DOT, DOT, DOT],       # S
]


def blink(duration):
    ledRL.duty_u16(FULL)
    sleep(duration)
    ledRL.duty_u16(OFF)
    sleep(GAP_SYMBOL)


try:
    while True:
        for letter in PATTERN:
            for symbol in letter:
                blink(symbol)
            sleep(GAP_LETTER - GAP_SYMBOL)   # replace the last symbol gap with a letter gap

        sleep(GAP_WORD - GAP_LETTER)         # replace the last letter gap with a word gap

except KeyboardInterrupt:
    ledRL.duty_u16(0)
    ledRL.deinit()
    print("Stopped, PWM deinitialized.")
