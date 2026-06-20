from machine import Pin, PWM
from time import sleep

led_pwm1 = PWM(Pin(0))   # red
led_pwm2 = PWM(Pin(1))   # yellow

PWM_CARRIER = 1000   # fixed internal switching freq, used only for dimming
led_pwm1.freq(PWM_CARRIER)
led_pwm2.freq(PWM_CARRIER)


def get_int(prompt, lo, hi):
    while True:
        try:
            val = int(input(prompt))
            if lo <= val <= hi:
                return val
            print(f"Enter a value between {lo} and {hi}.")
        except ValueError:
            print("Please type a whole number.")


frequency = get_int("Blink frequency (0-20 Hz, 0 = no blinking): ", 0, 20)
brightness_pct = get_int("Brightness (0-100%): ", 0, 100)

duty = int(brightness_pct / 100 * 65535)


def set_leds(on):
    d = duty if on else 0
    led_pwm1.duty_u16(d)
    led_pwm2.duty_u16(d)


try:
    if frequency == 0:
        set_leds(True)          # solid, at whatever brightness was chosen (0% = off)
        while True:
            sleep(1)
    else:
        half_period = (1 / frequency) / 2
        while True:
            set_leds(True)
            sleep(half_period)
            set_leds(False)
            sleep(half_period)
except KeyboardInterrupt:
    led_pwm1.duty_u16(0)
    led_pwm2.duty_u16(0)
    led_pwm1.deinit()
    led_pwm2.deinit()
    print("Stopped, PWM deinitialized.")
