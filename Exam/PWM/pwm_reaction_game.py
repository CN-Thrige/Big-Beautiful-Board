from machine import Pin, PWM
from time import sleep, ticks_ms, ticks_diff
import urandom

Btn1 = Pin(6, Pin.IN, Pin.PULL_UP)   # "react" button

ledGL = PWM(Pin(2))   # green left = the "go" signal
ledRL = PWM(Pin(0))   # red left = shown while waiting

PWM_CARRIER = 1000   # fixed internal switching freq, used only for dimming
ledGL.freq(PWM_CARRIER)
ledRL.freq(PWM_CARRIER)

FULL = 65535
OFF = 0


def wait_for_release():
    while Btn1.value() == 0:
        sleep(0.01)


def play_round():
    # red on: get ready, don't press yet
    ledRL.duty_u16(FULL)
    ledGL.duty_u16(OFF)
    print("Get ready...")

    wait_ms = urandom.getrandbits(12) % 3000 + 1000   # random 1-4 second wait

    start_wait = ticks_ms()
    while ticks_diff(ticks_ms(), start_wait) < wait_ms:
        if Btn1.value() == 0:
            print("Too soon! Wait for green.")
            wait_for_release()
            return
        sleep(0.01)

    # green on: go!
    ledRL.duty_u16(OFF)
    ledGL.duty_u16(FULL)
    go_time = ticks_ms()
    print("GO!")

    while Btn1.value() != 0:
        sleep(0.001)

    reaction_ms = ticks_diff(ticks_ms(), go_time)
    print(f"Reaction time: {reaction_ms} ms")
    wait_for_release()

    ledGL.duty_u16(OFF)


try:
    while True:
        play_round()
        sleep(1)

except KeyboardInterrupt:
    ledRL.duty_u16(0)
    ledGL.duty_u16(0)
    ledRL.deinit()
    ledGL.deinit()
    print("Stopped, PWM deinitialized.")
