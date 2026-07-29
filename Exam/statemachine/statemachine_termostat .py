# 11 (bonus) - Hysterese-sløjfe / termostat (Statemachine_v2.pptx, slide 17-18)
# Kun 2 states: "on" og "off", men med to forskellige tærskler så det ikke
# "flimrer" hele tiden omkring én værdi:
#   Tænd varme  hvis værdi <= 23
#   Sluk varme  hvis værdi >= 25
#
# Vi har ikke en rigtig temperatursensor på boardet, så et potentiometer på
# ADC (GP26) bruges som "fup-temperatur" (0-3,3V mappes til fx 0-50 grader).
#
# Pin-layout:
#   temp_sensor = ADC(Pin(26))
#   ledRL = Pin(0)   -> "varme tændt" indikator

from machine import Pin, ADC
from time import sleep

temp_sensor = ADC(Pin(26))
ledRL = Pin(0, Pin.OUT)     # varme-indikator

TAENDT_GRAENSE = 23
SLUKKET_GRAENSE = 25


def laes_temperatur():
    raw = temp_sensor.read_u16()          # 0-65535
    return raw / 65535 * 50               # simuleret 0-50 grader


varme_er_taendt = False

try:
    while True:
        temp = laes_temperatur()

        if varme_er_taendt and temp >= SLUKKET_GRAENSE:
            varme_er_taendt = False
        elif not varme_er_taendt and temp <= TAENDT_GRAENSE:
            varme_er_taendt = True
        # ellers: bliv i samme state (det er selve hysteresen)

        ledRL.value(1 if varme_er_taendt else 0)
        print(f"Temp: {temp:.1f} grader - Varme: {'ON' if varme_er_taendt else 'OFF'}")
        sleep(0.5)
except KeyboardInterrupt:
    ledRL.value(0)
    print("Stoppet.")
