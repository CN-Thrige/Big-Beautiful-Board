from machine import Pin, PWM
from time import sleep

pwm1 = PWM(Pin(0))
pwm0 = PWM(Pin(1))
pwm1.freq(1000)
pwm0.freq(1000)

duty = 0
retning = 1

while True:
    pwm1.duty_u16(duty)
    pwm0.duty_u16(65535 - duty)   # modsat lysstyrke af pwm1
    duty += retning * 2000

    if duty >= 65535 or duty <= 0:
        retning *= -1

    sleep(0.01)
