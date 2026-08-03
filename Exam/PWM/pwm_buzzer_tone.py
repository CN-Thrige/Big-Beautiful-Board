from machine import Pin, PWM
from time import sleep

buzzer = PWM(Pin(8))   # buzzer - change pin to match your wiring

# Here PWM is used for AUDIO, not dimming:
#   - freq() sets the actual TONE (pitch) you hear, e.g. 440 Hz = A4
#   - duty_u16() at 50% just makes a clean square wave; it does NOT
#     control "brightness" here, it controls loudness/wave shape


def get_int(prompt, lo, hi):
    while True:
        try:
            val = int(input(prompt))
            if lo <= val <= hi:
                return val
            print(f"Enter a value between {lo} and {hi}.")
        except ValueError:
            print("Please type a whole number.")


tone_hz = get_int("Tone frequency (100-2000 Hz): ", 100, 2000)
duration_s = get_int("Beep duration in seconds (0-5): ", 0, 5)

HALF_DUTY = 32768   # 50% duty_u16 -> square wave, on for equal time as off


def beep(freq, seconds):
    buzzer.freq(freq)
    buzzer.duty_u16(HALF_DUTY)
    sleep(seconds)
    buzzer.duty_u16(0)   # silence


try:
    beep(tone_hz, duration_s)
    print("Beep done.")
    while True:
        sleep(1)         # idle, program stays alive until Ctrl+C

except KeyboardInterrupt:
    buzzer.duty_u16(0)
    buzzer.deinit()
    print("Stopped, PWM deinitialized.")
