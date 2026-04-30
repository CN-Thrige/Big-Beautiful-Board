# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-micropython-ebook/

from machine import Pin, PWM
from time import sleep

# Set up PWM Pin
redledleft = machine.Pin(0)
yellowledleft= machine.Pin(1)
greenledleft = machine.Pin(2)

redledright= machine.Pin(3)
yellowledright = machine.Pin(4)
greenledright = machine.Pin(5)


led1_pwm = PWM(redledleft)
led2_pwm = PWM(yellowledleft)
led3_pwm = PWM(greenledleft)

led4_pwm = PWM(redledright)
led5_pwm = PWM(yellowledright)
led6_pwm = PWM(greenledright)
duty_step = 129  # Step size for changing the duty cycle

# Set PWM frequency
frequency = 5000
led1_pwm.freq(frequency)
led2_pwm.freq(frequency)
led3_pwm.freq(frequency)

led4_pwm.freq(frequency)
led5_pwm.freq(frequency)
led6_pwm.freq(frequency)

try:
    while True:
        # Increase the duty cycle gradually
        for duty_cycle in range(0, 65536, duty_step):
            led1_pwm.duty_u16(duty_cycle)
            led2_pwm.duty_u16(duty_cycle)
            led3_pwm.duty_u16(duty_cycle)

            led4_pwm.duty_u16(duty_cycle)
            led5_pwm.duty_u16(duty_cycle)
            led6_pwm.duty_u16(duty_cycle)
            sleep(0.005)

        # Decrease the duty cycle gradually
        for duty_cycle in range(65536, 0, -duty_step):
            led1_pwm.duty_u16(duty_cycle)
            led2_pwm.duty_u16(duty_cycle)
            led3_pwm.duty_u16(duty_cycle)
            
            led4_pwm.duty_u16(duty_cycle)
            led5_pwm.duty_u16(duty_cycle)
            led6_pwm.duty_u16(duty_cycle)
            sleep(0.005)

except KeyboardInterrupt:
    print("Keyboard interrupt")

    led1_pwm.duty_u16(0)
    led2_pwm.duty_u16(0)
    led3_pwm.duty_u16(0)
    
    led5_pwm.duty_u16(0)
    led6_pwm.duty_u16(0)
    led7_pwm.duty_u16(0)
    
    print(led1_pwm, led2_pwm, led3_pwm)
    led1_pwm.deinit()
    led2_pwm.deinit()
    led3_pwm.deinit()
    
    led4_pwm.deinit()
    led5_pwm.deinit()
    led6_pwm.deinit()
