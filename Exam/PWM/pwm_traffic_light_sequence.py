from machine import Pin, PWM
from time import sleep

ledRL = PWM(Pin(0))   # red left
ledYL = PWM(Pin(1))   # yellow left
ledGL = PWM(Pin(2))   # green left

leds = [ledRL, ledYL, ledGL]

PWM_CARRIER = 1000   # fixed internal switching freq, used only for dimming
for led in leds:
    led.freq(PWM_CARRIER)

FULL = 65535
OFF = 0
FADE_STEPS = 30
FADE_DELAY = 0.01   # total fade time per transition = FADE_STEPS * FADE_DELAY

# how long each state stays fully lit before the next transition (seconds)
HOLD_RED = 3
HOLD_RED_YELLOW = 1
HOLD_GREEN = 3
HOLD_YELLOW = 1


def fade_to(targets):
    """targets is a list of 3 duty values, one per LED in `leds`, and this
    ramps every LED linearly from its current duty to its target duty."""
    starts = [led.duty_u16() for led in leds]   # duty_u16() with no args reads current duty
    for step in range(FADE_STEPS + 1):
        ratio = step / FADE_STEPS
        for led, start, target in zip(leds, starts, targets):
            duty = int(start + (target - start) * ratio)
            led.duty_u16(duty)
        sleep(FADE_DELAY)


try:
    # start solid red
    ledRL.duty_u16(FULL)
    ledYL.duty_u16(OFF)
    ledGL.duty_u16(OFF)

    while True:
        sleep(HOLD_RED)

        fade_to([FULL, FULL, OFF])       # red + yellow together
        sleep(HOLD_RED_YELLOW)

        fade_to([OFF, OFF, FULL])        # green
        sleep(HOLD_GREEN)

        fade_to([OFF, FULL, OFF])        # yellow
        sleep(HOLD_YELLOW)

        fade_to([FULL, OFF, OFF])        # back to red

except KeyboardInterrupt:
    for led in leds:
        led.duty_u16(0)
        led.deinit()
    print("Stopped, PWM deinitialized.")
