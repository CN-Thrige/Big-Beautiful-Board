# 05 - PWM lysstyrke styret med knapper (fra PWM.pptx opgave: "Brug knapperne
# til at skrue op og ned for LED'en")
# Pin-layout:
#   button1 = Pin(6, PULL_UP)  -> skru OP for lysstyrken (0 = trykket)
#   button2 = Pin(7, PULL_UP)  -> skru NED for lysstyrken
#   ledGL   = Pin(2)           -> LED der dæmpes

from machine import Pin, PWM
from time import sleep

button1 = Pin(6, Pin.IN, Pin.PULL_UP)   # op
button2 = Pin(7, Pin.IN, Pin.PULL_UP)   # ned

led_pwm = PWM(Pin(2))     # Venstre grøn LED bruges som dæmpe-LED
PWM_CARRIER = 1000
led_pwm.freq(PWM_CARRIER)

TRIN = 5           # % pr. tryk
brightness_pct = 50
led_pwm.duty_u16(int(brightness_pct / 100 * 65535))
print(f"Lysstyrke: {brightness_pct}%")

try:
    while True:
        if button1.value() == 0:            # OP
            brightness_pct = min(100, brightness_pct + TRIN)
            led_pwm.duty_u16(int(brightness_pct / 100 * 65535))
            print(f"Lysstyrke: {brightness_pct}%")
            sleep(0.2)                       # simpel "debounce"

        elif button2.value() == 0:           # NED
            brightness_pct = max(0, brightness_pct - TRIN)
            led_pwm.duty_u16(int(brightness_pct / 100 * 65535))
            print(f"Lysstyrke: {brightness_pct}%")
            sleep(0.2)

except KeyboardInterrupt:
    led_pwm.duty_u16(0)
    led_pwm.deinit()
    print("Stopped, PWM deinitialized.")
