from machine import Pin, PWM
from time import sleep

btn_up = Pin(6, Pin.IN, Pin.PULL_UP)
btn_down = Pin(7, Pin.IN, Pin.PULL_UP)

led_pwm = PWM(Pin(0))
led_pwm.freq(1000)

brightness_pct = 0
STEP = 5

try:
    while True:
        if btn_up.value() == 0:
            brightness_pct = min(100, brightness_pct + STEP)
            sleep(0.15)
        elif btn_down.value() == 0:
            brightness_pct = max(0, brightness_pct - STEP)
            sleep(0.15)

        duty = int(brightness_pct / 100 * 65535)
        led_pwm.duty_u16(duty)
except KeyboardInterrupt:
    led_pwm.duty_u16(0)
    led_pwm.deinit()
