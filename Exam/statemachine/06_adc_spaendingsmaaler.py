# 06 - A/D konvertering: simpelt voltmeter på Pico (0-3,3V)
# Pin-layout:
#   pot = ADC(Pin(26))   -> analog indgang (GP26 / ADC0), jf. slides:
#                            "Port 26 benyttes til indgang til A/D konverteren"
#
# Pico's ADC:
#   Analog værdi = 0V     -> Digital værdi = 0
#   Analog værdi = 1,65V  -> Digital værdi = 32767
#   Analog værdi = 3,3V   -> Digital værdi = 65535
#
# Der måles 10 gange hvert sekund, ligesom i slides.

from machine import Pin, ADC
from time import sleep

pot = ADC(Pin(26))
MAKS_SPAENDING = 3.3
MAKS_VAERDI = 65535

try:
    while True:
        pot_value = pot.read_u16()                       # 0-65535
        spaending = pot_value / MAKS_VAERDI * MAKS_SPAENDING
        print(f"ADC: {pot_value}  ->  {spaending:.2f} V")
        sleep(0.1)          # 10 målinger pr. sekund
except KeyboardInterrupt:
    print("Stoppet.")
