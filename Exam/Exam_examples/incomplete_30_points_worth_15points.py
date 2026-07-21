#this gave 15 points at the exam!
from machine import Pin, PWM
from time import sleep

#this program gave 15 points doing the exam 

#button1 = Pin(6, Pin.IN, Pin.PULL_UP)

led = Pin(0, Pin.OUT)

p1 = machine.Pin(0)  #red
led_pwm1 = PWM(p1)

p0 = machine.Pin(1) #yellow
led_pwm2 = PWM(p0)

duty_step = int(input("type a brightness of PMW between 0 to 100%: "))
#duty_step = 129  


# Set PWM frequency
freqlim = 20
frequency = int(input("type a frequency between 0 to 20Hz: "))
led_pwm1.freq(frequency)
led_pwm2.freq(frequency)

try:
    while True:

        for duty_cycle in range(0, 65536, duty_step): #65536
            led_pwm1.duty_u16(duty_cycle)
            sleep(0.005)
            
            led_pwm2.duty_u16(duty_cycle)
            sleep(0.005)

        for duty_cycle in range(65536, 0, -duty_step):
            led_pwm1.duty_u16(duty_cycle)
            sleep(0.005)
            
            led_pwm2.duty_u16(duty_cycle)
            sleep(0.005)
            

except KeyboardInterrupt:
    print("Keyboard interrupt")
    led_pwm1.duty_u16(0)
    led_pwm2.duty_u16(0)

    print(led_pwm1)
    print(led_pwm2)
    led_pwm1.deinit()
    led_pwm2.deinit()

