from machine import Pin, PWM, ADC
from time import sleep

pot = ADC(Pin(26))     # potentiometer on ADC0
ledGL = PWM(Pin(2))    # green left

PWM_CARRIER = 1000     # fixed internal switching freq, used only for dimming
ledGL.freq(PWM_CARRIER)

# ADC.read_u16() returns 0-65535, which happens to match duty_u16() 1:1,
# so no percent-conversion is needed here - just read and write straight through.

try:
    while True:
        raw = pot.read_u16()          # 0 (0 V) .. 65535 (3.3 V)
        ledGL.duty_u16(raw)

        brightness_pct = int(raw / 65535 * 100)
        print(f"Brightness: {brightness_pct}%")
        sleep(0.1)

except KeyboardInterrupt:
    ledGL.duty_u16(0)
    ledGL.deinit()
    print("Stopped, PWM deinitialized.")
