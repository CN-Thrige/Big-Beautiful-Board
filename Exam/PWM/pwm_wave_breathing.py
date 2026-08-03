from machine import Pin, PWM
from time import sleep
import math

ledRL = PWM(Pin(0))   # red left
ledYL = PWM(Pin(1))   # yellow left
ledGL = PWM(Pin(2))   # green left
ledRR = PWM(Pin(3))   # red right
ledYR = PWM(Pin(4))   # yellow right
ledGR = PWM(Pin(5))   # green right

leds = [ledRL, ledYL, ledGL, ledRR, ledYR, ledGR]

PWM_CARRIER = 1000   # fixed internal switching freq, used only for dimming
for led in leds:
    led.freq(PWM_CARRIER)

PHASE_STEP = math.pi / 3   # offset between neighboring LEDs (radians)
SPEED = 0.15                # how fast the wave rolls (radians per loop)
TICK = 0.02                 # loop interval

angle = 0.0

try:
    while True:
        for i, led in enumerate(leds):
            # sin() gives -1..1, shift/scale it to a 0..100% brightness wave
            brightness_pct = (math.sin(angle + i * PHASE_STEP) + 1) / 2 * 100
            led.duty_u16(int(brightness_pct / 100 * 65535))

        angle += SPEED
        sleep(TICK)

except KeyboardInterrupt:
    for led in leds:
        led.duty_u16(0)
        led.deinit()
    print("Stopped, PWM deinitialized.")
