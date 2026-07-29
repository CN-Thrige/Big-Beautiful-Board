"""
Statemachine - Lyskryds (Nord/Syd + Øst/Vest)
------------------------------------------------
Fra Lyskryds.pptx: et lyskryds er delt i 2 dele, Nord-Syd og Øst-Vest,
som ALDRIG må have grønt samtidig.

6 LED'er i alt: rød/gul/grøn for hver retning.
Rækkefølge (klassisk kryds-cyklus):
  1) NS grøn,  EW rød
  2) NS gul,   EW rød
  3) NS rød,   EW rød    (kort "alt rødt" - sikkerhedspause)
  4) NS rød,   EW grøn
  5) NS rød,   EW gul
  6) NS rød,   EW rød    (kort "alt rødt")
  -> tilbage til 1)
"""

from machine import Pin
from time import sleep

# Nord-Syd LED'er
ns_red = Pin(2, Pin.OUT)
ns_yellow = Pin(3, Pin.OUT)
ns_green = Pin(4, Pin.OUT)

# Øst-Vest LED'er
ew_red = Pin(5, Pin.OUT)
ew_yellow = Pin(6, Pin.OUT)
ew_green = Pin(7, Pin.OUT)

GREEN_TIME = 5.0
YELLOW_TIME = 1.5
ALL_RED_TIME = 1.0


def set_ns(red, yellow, green):
    ns_red.value(red)
    ns_yellow.value(yellow)
    ns_green.value(green)


def set_ew(red, yellow, green):
    ew_red.value(red)
    ew_yellow.value(yellow)
    ew_green.value(green)


def state_ns_green():
    set_ns(0, 0, 1)
    set_ew(1, 0, 0)
    print("NS: Grøn  | EW: Rød")
    sleep(GREEN_TIME)
    return state_ns_yellow


def state_ns_yellow():
    set_ns(0, 1, 0)
    set_ew(1, 0, 0)
    print("NS: Gul   | EW: Rød")
    sleep(YELLOW_TIME)
    return state_all_red_1


def state_all_red_1():
    set_ns(1, 0, 0)
    set_ew(1, 0, 0)
    print("NS: Rød   | EW: Rød  (sikkerhedspause)")
    sleep(ALL_RED_TIME)
    return state_ew_green


def state_ew_green():
    set_ns(1, 0, 0)
    set_ew(0, 0, 1)
    print("NS: Rød   | EW: Grøn")
    sleep(GREEN_TIME)
    return state_ew_yellow


def state_ew_yellow():
    set_ns(1, 0, 0)
    set_ew(0, 1, 0)
    print("NS: Rød   | EW: Gul")
    sleep(YELLOW_TIME)
    return state_all_red_2


def state_all_red_2():
    set_ns(1, 0, 0)
    set_ew(1, 0, 0)
    print("NS: Rød   | EW: Rød  (sikkerhedspause)")
    sleep(ALL_RED_TIME)
    return state_ns_green


state = state_ns_green
try:
    while state:
        state = state()
except KeyboardInterrupt:
    set_ns(0, 0, 0)
    set_ew(0, 0, 0)
    print("Lyskryds stoppet.")
