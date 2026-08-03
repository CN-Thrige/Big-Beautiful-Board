from machine import Pin, PWM
from time import sleep
import urandom

Btn1 = Pin(6, Pin.IN, Pin.PULL_UP)   # player 1
Btn2 = Pin(7, Pin.IN, Pin.PULL_UP)   # player 2

led_p1 = PWM(Pin(2))   # green left = player 1 indicator
led_p2 = PWM(Pin(5))   # green right = player 2 indicator
led_ready = PWM(Pin(0))   # red left = "wait" indicator, shown to both players

leds = [led_p1, led_p2, led_ready]

PWM_CARRIER = 1000   # fixed internal switching freq, used only for dimming
for led in leds:
    led.freq(PWM_CARRIER)

FULL = 65535
OFF = 0


def wait_for_release():
    while Btn1.value() == 0 or Btn2.value() == 0:
        sleep(0.01)


def play_round():
    led_ready.duty_u16(FULL)
    led_p1.duty_u16(OFF)
    led_p2.duty_u16(OFF)
    print("Get ready...")

    wait_ms = urandom.getrandbits(12) % 3000 + 1000   # random 1-4 second wait
    waited = 0
    while waited < wait_ms:
        if Btn1.value() == 0:
            print("Player 1 jumped the gun - Player 2 wins by default!")
            wait_for_release()
            return
        if Btn2.value() == 0:
            print("Player 2 jumped the gun - Player 1 wins by default!")
            wait_for_release()
            return
        sleep(0.01)
        waited += 10

    led_ready.duty_u16(OFF)
    led_p1.duty_u16(FULL)
    led_p2.duty_u16(FULL)
    print("GO!")

    while True:
        if Btn1.value() == 0:
            print("Player 1 wins!")
            break
        if Btn2.value() == 0:
            print("Player 2 wins!")
            break

    wait_for_release()
    led_p1.duty_u16(OFF)
    led_p2.duty_u16(OFF)


try:
    while True:
        play_round()
        sleep(1.5)

except KeyboardInterrupt:
    for led in leds:
        led.duty_u16(0)
        led.deinit()
    print("Stopped, PWM deinitialized.")
