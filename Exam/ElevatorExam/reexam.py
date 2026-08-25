# 12 (bonus) - "Random machine" (Statemachine_v2.pptx, slide 5-7)
# Pointe: en state behøver ikke gå til en FAST næste state - den kan vælge
# næste state tilfældigt. Her "leger" krydset med sine lys i vilkårlig
# rækkefølge (KUN til demonstration af konceptet - IKKE en rigtig trafikstyring,
# da der ingen sikkerhed er for at lysene ikke er grønne samtidig!).
#
# Pin-layout: samme 6 LED'er som i lyskryds-programmerne.

from machine import Pin
from time import sleep
from random import random

ledRL = Pin(0, Pin.OUT)
ledYL = Pin(1, Pin.OUT)
ledGL = Pin(2, Pin.OUT)
ledRR = Pin(3, Pin.OUT)
ledYR = Pin(4, Pin.OUT)
ledGR = Pin(5, Pin.OUT)

Btn1 = Pin(6, Pin.IN, Pin.PULL_UP)

red_led = [ledRL, ledRR]
green_led = [ledGR, ledGL]
yellow_led = [ledYL, ledYR]

alle_leds = [red_led, green_led, yellow_led]


while True: 

    if btn1.value() == 0:
        choice = random.choice(alle_leds)
        print("Tilfældig LED valgt:", alle_leds.index(choice))
        sleep(0.5)

