from machine import Pin, PWM
from time import sleep
import urandom

Btn1 = Pin(6, Pin.IN, Pin.PULL_UP)   # "it's on the left" guess
Btn2 = Pin(7, Pin.IN, Pin.PULL_UP)   # "it's on the right" guess

ledRL = PWM(Pin(0))   # red left
ledYL = PWM(Pin(1))   # yellow left
ledGL = PWM(Pin(2))   # green left
ledRR = PWM(Pin(3))   # red right
ledYR = PWM(Pin(4))   # yellow right
ledGR = PWM(Pin(5))   # green right

left_leds = [ledRL, ledYL, ledGL]
right_leds = [ledRR, ledYR, ledGR]
all_leds = left_leds + right_leds

PWM_CARRIER = 1000   # fixed internal switching freq, used only for dimming
for led in all_leds:
    led.freq(PWM_CARRIER)

FULL = 65535
OFF = 0


def all_off():
    for led in all_leds:
        led.duty_u16(OFF)


def flash_all(times, on_time):
    for _ in range(times):
        for led in all_leds:
            led.duty_u16(FULL)
        sleep(on_time)
        all_off()
        sleep(on_time)


def wait_for_press():
    while True:
        if Btn1.value() == 0:
            return "left"
        if Btn2.value() == 0:
            return "right"
        sleep(0.01)


def wait_for_release():
    while Btn1.value() == 0 or Btn2.value() == 0:
        sleep(0.01)


score = 0

try:
    all_off()
    print("Simon Says: Left or Right? Press Btn1 = left, Btn2 = right.")
    sleep(1)

    while True:
        side = urandom.getrandbits(1)   # 0 = left, 1 = right
        led_group = left_leds if side == 0 else right_leds
        answer = "left" if side == 0 else "right"

        for led in led_group:
            led.duty_u16(FULL)
        sleep(0.5)
        all_off()

        guess = wait_for_press()
        wait_for_release()

        if guess == answer:
            score += 1
            print(f"Correct! Score: {score}")
            sleep(0.5)
        else:
            print(f"Wrong! Game over. Final score: {score}")
            flash_all(4, 0.15)
            score = 0
            sleep(1)

except KeyboardInterrupt:
    for led in all_leds:
        led.duty_u16(0)
        led.deinit()
    print("Stopped, PWM deinitialized.")
