from machine import Pin, PWM
from time import sleep

ledRL = PWM(Pin(0))   # red left
ledYL = PWM(Pin(1))   # yellow left
ledGL = PWM(Pin(2))   # green left
ledRR = PWM(Pin(3))   # red right
ledYR = PWM(Pin(4))   # yellow right
ledGR = PWM(Pin(5))   # green right

leds = [ledRL, ledYL, ledGL, ledGR, ledYR, ledRR]   # order = physical left-to-right sweep

PWM_CARRIER = 1000   # fixed internal switching freq, used only for dimming
for led in leds:
    led.freq(PWM_CARRIER)

STEP_DELAY = 0.08     # time the "eye" spends on each LED before moving on
TRAIL = [100, 40, 15]  # brightness % for current LED, one-behind, two-behind


def pct_to_duty(pct):
    return int(pct / 100 * 65535)


def show_eye_at(index):
    for i, led in enumerate(leds):
        distance = abs(i - index)
        pct = TRAIL[distance] if distance < len(TRAIL) else 0
        led.duty_u16(pct_to_duty(pct))


try:
    positions = list(range(len(leds))) + list(range(len(leds) - 2, 0, -1))
    while True:
        for pos in positions:
            show_eye_at(pos)
            sleep(STEP_DELAY)

except KeyboardInterrupt:
    for led in leds:
        led.duty_u16(0)
        led.deinit()
    print("Stopped, PWM deinitialized.")
