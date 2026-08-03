from machine import Pin, PWM
from time import sleep

Btn1 = Pin(6, Pin.IN, Pin.PULL_UP)   # hold to ramp brightness up
Btn2 = Pin(7, Pin.IN, Pin.PULL_UP)   # hold to ramp brightness down

ledGR = PWM(Pin(5))   # green right

PWM_CARRIER = 1000   # fixed internal switching freq, used only for dimming
ledGR.freq(PWM_CARRIER)

brightness_pct = 50.0     # start at 50%
RAMP_RATE = 40.0          # % per second while a button is held down
TICK = 0.02               # loop interval


def pct_to_duty(pct):
    return int(pct / 100 * 65535)


try:
    ledGR.duty_u16(pct_to_duty(brightness_pct))
    last_print = 0

    while True:
        changed = False

        if Btn1.value() == 0:
            brightness_pct = min(100.0, brightness_pct + RAMP_RATE * TICK)
            changed = True
        elif Btn2.value() == 0:
            brightness_pct = max(0.0, brightness_pct - RAMP_RATE * TICK)
            changed = True

        if changed:
            ledGR.duty_u16(pct_to_duty(brightness_pct))
            print(f"Brightness: {int(brightness_pct)}%")

        sleep(TICK)

except KeyboardInterrupt:
    ledGR.duty_u16(0)
    ledGR.deinit()
    print("Stopped, PWM deinitialized.")
