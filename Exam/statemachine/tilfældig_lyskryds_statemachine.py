# 12 (bonus) - "Random machine" (Statemachine_v2.pptx, slide 5-7)
# Pointe: en state behøver ikke gå til en FAST næste state - den kan vælge
# næste state tilfældigt. Her "leger" krydset med sine lys i vilkårlig
# rækkefølge (KUN til demonstration af konceptet - IKKE en rigtig trafikstyring,
# da der ingen sikkerhed er for at lysene ikke er grønne samtidig!).
#
# Pin-layout: samme 6 LED'er som i lyskryds-programmerne.

from machine import Pin
from time import sleep
import random

ledRL = Pin(0, Pin.OUT)
ledYL = Pin(1, Pin.OUT)
ledGL = Pin(2, Pin.OUT)
ledRR = Pin(3, Pin.OUT)
ledYR = Pin(4, Pin.OUT)
ledGR = Pin(5, Pin.OUT)

alle_leds = [ledRL, ledYL, ledGL, ledRR, ledYR, ledGR]


def sluk_alt():
    for led in alle_leds:
        led.value(0)


def tilfaeldig_state():
    sluk_alt()
    valgt = random.choice(alle_leds)
    valgt.value(1)
    print("Tilfældig LED valgt:", alle_leds.index(valgt))
    sleep(0.5)
    return tilfaeldig_state       # næste state er "sig selv" - valget sker igen


try:
    state = tilfaeldig_state
    while state:
        state = state()
except KeyboardInterrupt:
    sluk_alt()
    print("Stoppet, alle LED'er slukket.")
