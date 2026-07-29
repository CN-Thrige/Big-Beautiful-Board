"""
Statemachine - Trafiklys (1 retning)
--------------------------------------
Samme mønster som slide "Lyskryds" i Statemachine_v2.pptx:
Hver "state" er en funktion, der udfører sit arbejde og
returnerer NAVNET (funktionsreferencen) på den næste state.
Hovedprogrammet er bare en while-løkke der kalder den aktuelle state.

Dette er selve skabelonen du skal genbruge til alle statemachine-opgaver:
grøn -> gul -> rød -> grøn -> ...
"""

from machine import Pin
from time import sleep

led_green = Pin(2, Pin.OUT)
led_yellow = Pin(3, Pin.OUT)
led_red = Pin(4, Pin.OUT)


def all_off():
    led_green.off()
    led_yellow.off()
    led_red.off()


def state_green():
    all_off()
    led_green.on()
    print("Grøn! Kør")
    sleep(5.5)
    return state_yellow


def state_yellow():
    all_off()
    led_yellow.on()
    print("Gul! Stop")
    sleep(1.5)
    return state_red


def state_red():
    all_off()
    led_red.on()
    print("Rød! Stop")
    sleep(5.5)
    return state_green


state = state_green          # startstate
try:
    while state:
        state = state()      # kør den nuværende state, få den næste igen
except KeyboardInterrupt:
    all_off()
    print("Statemachine stoppet.")
