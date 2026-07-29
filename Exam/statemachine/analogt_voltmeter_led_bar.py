# 08 - "Analogt" voltmeter som LED-bar, digital udgave (Voltmeter_analog_og_digitalt.pptx
# + Spændingsdeler_Pico.xlsx). Måleområde 0-12V, samme tærskler som i regnearket:
#   Grøn tændt      = 12V på batteriet
#   Gul tændt       = 8V på batteriet
#   Rød tændt       = 4V på batteriet
#   Rød BLINKER     = 2V på batteriet (kritisk lavt)
#
# Pin-layout:
#   maal = ADC(Pin(26))               -> spændingsdeler-udgang (0-3,3V)
#   ledGL = Pin(2)  ledYL = Pin(1)  ledRL = Pin(0)   -> "Venstre" lys bruges som bar-graf
#
# Juster SKALA_FAKTOR til jeres egen spændingsdeler, så 12V batteri svarer
# til <= 3,3V ved Pico'ens ADC-indgang.

from machine import Pin, ADC
from time import sleep

maal = ADC(Pin(26))
ledRL = Pin(0, Pin.OUT)
ledYL = Pin(1, Pin.OUT)
ledGL = Pin(2, Pin.OUT)

MAKS_SPAENDING = 3.3
MAKS_VAERDI = 65535
SKALA_FAKTOR = 12 / 3.3     # 12V batteri -> 3,3V ved fuld udslag (juster efter egen deler)


def maal_batteri():
    raw = maal.read_u16()
    v_pico = raw / MAKS_VAERDI * MAKS_SPAENDING
    return v_pico * SKALA_FAKTOR


try:
    blink_tilstand = False
    while True:
        v_batt = maal_batteri()
        print(f"Batteri: {v_batt:.1f} V")

        if v_batt >= 10:                 # omkring 12V
            ledGL.value(1); ledYL.value(0); ledRL.value(0)
        elif v_batt >= 6:                # omkring 8V
            ledGL.value(0); ledYL.value(1); ledRL.value(0)
        elif v_batt >= 3:                # omkring 4V
            ledGL.value(0); ledYL.value(0); ledRL.value(1)
        else:                            # omkring 2V, kritisk -> blink rød
            ledGL.value(0); ledYL.value(0)
            blink_tilstand = not blink_tilstand
            ledRL.value(blink_tilstand)

        sleep(0.5)
except KeyboardInterrupt:
    ledRL.value(0); ledYL.value(0); ledGL.value(0)
    print("Stoppet, alle LED'er slukket.")
