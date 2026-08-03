from machine import Pin, PWM
from time import sleep

Btn1 = Pin(6, Pin.IN, Pin.PULL_UP)   # cycle brightness preset
Btn2 = Pin(7, Pin.IN, Pin.PULL_UP)   # toggle blinking on/off

ledYL = PWM(Pin(1))   # yellow left

PWM_CARRIER = 1000   # fixed internal switching freq, used only for dimming
ledYL.freq(PWM_CARRIER)

PRESETS = [25, 50, 75, 100]   # % brightness presets to cycle through
preset_index = 0
blinking = False

BLINK_HALF_PERIOD = 0.3   # fixed blink speed while blinking is on


def pct_to_duty(pct):
    return int(pct / 100 * 65535)


def current_duty():
    return pct_to_duty(PRESETS[preset_index])


try:
    ledYL.duty_u16(current_duty())
    print(f"Preset: {PRESETS[preset_index]}%  Blinking: {blinking}")

    led_on = True
    last_blink = 0.0
    t = 0.0

    while True:
        sleep(0.01)
        t += 0.01

        if Btn1.value() == 0:
            preset_index = (preset_index + 1) % len(PRESETS)
            if not blinking:
                ledYL.duty_u16(current_duty())
            print(f"Preset: {PRESETS[preset_index]}%  Blinking: {blinking}")
            sleep(0.2)   # simple debounce

        elif Btn2.value() == 0:
            blinking = not blinking
            if not blinking:
                ledYL.duty_u16(current_duty())   # solid at preset when blinking stops
                led_on = True
            print(f"Preset: {PRESETS[preset_index]}%  Blinking: {blinking}")
            sleep(0.2)

        if blinking and t - last_blink >= BLINK_HALF_PERIOD:
            led_on = not led_on
            ledYL.duty_u16(current_duty() if led_on else 0)
            last_blink = t

except KeyboardInterrupt:
    ledYL.duty_u16(0)
    ledYL.deinit()
    print("Stopped, PWM deinitialized.")
