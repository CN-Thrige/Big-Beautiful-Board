from machine import Pin, PWM
from time import sleep

ledRL = PWM(Pin(0))   # red left
ledGL = PWM(Pin(2))   # green left

PWM_CARRIER = 1000   # fixed internal switching freq, used only for dimming
ledRL.freq(PWM_CARRIER)
ledGL.freq(PWM_CARRIER)


def get_int(prompt, lo, hi):
    while True:
        try:
            val = int(input(prompt))
            if lo <= val <= hi:
                return val
            print(f"Enter a value between {lo} and {hi}.")
        except ValueError:
            print("Please type a whole number.")


fade_seconds = get_int("Crossfade time in seconds (0-10): ", 0, 10)

STEPS = 100
step_delay = fade_seconds / STEPS


def pct_to_duty(pct):
    return int(pct / 100 * 65535)


try:
    while True:
        # red rises 0 -> 100% while green falls 100 -> 0%
        for pct in range(0, 101):
            ledRL.duty_u16(pct_to_duty(pct))
            ledGL.duty_u16(pct_to_duty(100 - pct))
            sleep(step_delay)

        # red falls 100 -> 0% while green rises 0 -> 100%
        for pct in range(100, -1, -1):
            ledRL.duty_u16(pct_to_duty(pct))
            ledGL.duty_u16(pct_to_duty(100 - pct))
            sleep(step_delay)

except KeyboardInterrupt:
    ledRL.duty_u16(0)
    ledGL.duty_u16(0)
    ledRL.deinit()
    ledGL.deinit()
    print("Stopped, PWM deinitialized.")
