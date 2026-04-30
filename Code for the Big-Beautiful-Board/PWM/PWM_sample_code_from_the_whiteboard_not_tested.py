#WARNING THIS IS NOT TESTED CODE. DO NOT USE IT!

from machine import Pin
from time import sleep

led = Pin(1, Pin.OUT)
led_PWM =PWM (led)

for duty_cycle in range(0.65536, duty_cycle)
  led_pwm.duty_u16(duty_cycle)
  sleep(0.005)
