# 10 - GY-53 afstandssensor (PWM-mode) + 3 LED-zoner (GY53_Presentation.pptx, slide 9+13)
# Sensoren sender en puls hvor pulslængden (i mikrosekunder) svarer til afstanden:
#   Afstand (mm) = Pulslængde (µs) / 10
#
# Pin-layout:
#   gy53 = Pin(16, IN)   -> PWM-signal fra sensoren (VCC->3V3, GND->GND)
#   ledGL = Pin(2)  0-10 cm   (tæt på)
#   ledYL = Pin(1)  11-20 cm  (mellem)
#   ledRL = Pin(0)  21-30 cm  (langt væk)
# (Bruger de 3 "Venstre" LED'er på krydset som zone-indikator, som foreslået i opgaven.)

import time
from machine import Pin

gy53 = Pin(16, Pin.IN)

ledRL = Pin(0, Pin.OUT)   # 21-30 cm
ledYL = Pin(1, Pin.OUT)   # 11-20 cm
ledGL = Pin(2, Pin.OUT)   # 0-10 cm


def maal_afstand_mm():
    while gy53.value() == True:          # vent til sensor er klar
        pass
    while gy53.value() == False:         # vent til puls starter
        pass
    starttime = time.ticks_us()
    while gy53.value() == True:          # vent til puls slutter
        pass
    endtime = time.ticks_us()
    pulslaengde_us = time.ticks_diff(endtime, starttime)
    return pulslaengde_us / 10           # mm


def vis_zone(afstand_cm):
    ledGL.value(0); ledYL.value(0); ledRL.value(0)
    if 0 <= afstand_cm <= 10:
        ledGL.value(1)
    elif 11 <= afstand_cm <= 20:
        ledYL.value(1)
    elif 21 <= afstand_cm <= 30:
        ledRL.value(1)
    # udenfor 0-30 cm: alle 3 LED'er forbliver slukket


try:
    while True:
        afstand_mm = maal_afstand_mm()
        afstand_cm = afstand_mm / 10
        print(f"Afstand: {afstand_cm:.1f} cm")
        vis_zone(afstand_cm)
        time.sleep(1)
except KeyboardInterrupt:
    ledGL.value(0); ledYL.value(0); ledRL.value(0)
    print("Stoppet, alle LED'er slukket.")
