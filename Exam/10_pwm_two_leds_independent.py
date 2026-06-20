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

print("--- Red LED ---")
freq1 = get_int("Blink frequency (0-20 Hz, 0 = no blinking): ", 0, 20)
bright1 = get_int("Brightness (0-100%): ", 0, 100)

print("--- Yellow LED ---")
freq2 = get_int("Blink frequency (0-20 Hz, 0 = no blinking): ", 0, 20)
bright2 = get_int("Brightness (0-100%): ", 0, 100)

duty1 = int(bright1 / 100 * 65535)
duty2 = int(bright2 / 100 * 65535)

def set_led(pwm, duty, on):
    pwm.duty_u16(duty if on else 0)

try:
    t = 0.0
    state1_on = True
    state2_on = True
    last_toggle1 = 0.0
    last_toggle2 = 0.0
    half1 = (1 / freq1) / 2 if freq1 > 0 else None
    half2 = (1 / freq2) / 2 if freq2 > 0 else None

    set_led(led_pwm1, duty1, True)
    set_led(led_pwm2, duty2, True)

    while True:
        sleep(0.01)
        t += 0.01

        if half1 is not None and t - last_toggle1 >= half1:
            state1_on = not state1_on
            set_led(led_pwm1, duty1, state1_on)
            last_toggle1 = t

        if half2 is not None and t - last_toggle2 >= half2:
            state2_on = not state2_on
            set_led(led_pwm2, duty2, state2_on)
            last_toggle2 = t
except KeyboardInterrupt:
    led_pwm1.duty_u16(0)
    led_pwm2.duty_u16(0)
    led_pwm1.deinit()
    led_pwm2.deinit()
    print("Stopped, PWM deinitialized.")
