# 07 - Robotbil batteri-måling via spændingsdeler (AD_converter_Pico.pptx, slide 10)
# Problem: Batteriet leverer 6,4V - 8,4V, men Pico'en kan kun måle 0-3,3V.
# Løsning: en modstands-spændingsdeler ned foran ADC-indgangen, og i koden
# ganges målingen op igen med den samme faktor, så vi printer den RIGTIGE
# batterispænding.
#
# Pin-layout:
#   batt = ADC(Pin(26))   -> spændingsdeler-udgang ind på GP26 (ADC0)
#
# VIGTIGT: R1/R2 herunder SKAL passe til jeres egen opbygning på printet!
# Sæt dem til de modstandsværdier I rent faktisk har loddet på (se jeres
# eget regneark til spændingsdeleren).

from machine import Pin, ADC
from time import sleep

batt = ADC(Pin(26))
MAKS_SPAENDING = 3.3
MAKS_VAERDI = 65535

# Spændingsdeler: Vud = Vind * R2 / (R1 + R2)  -> Vind = Vud * (R1+R2)/R2
R1 = 10_000     # Ohm, øverste modstand (juster til egen opkobling!)
R2 = 4_700      # Ohm, nederste modstand (juster til egen opkobling!)
SKALA_FAKTOR = (R1 + R2) / R2

try:
    while True:
        raw = batt.read_u16()
        v_ved_pico = raw / MAKS_VAERDI * MAKS_SPAENDING
        v_batteri = v_ved_pico * SKALA_FAKTOR
        print(f"Pico ser: {v_ved_pico:.2f} V  ->  Batteri: {v_batteri:.2f} V")

        if v_batteri < 6.4:
            print("  ADVARSEL: Under min. batterispænding (6,4V)!")

        sleep(0.5)
except KeyboardInterrupt:
    print("Stoppet.")
