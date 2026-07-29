# 01 - Trafiklys, enkelt lys (statemachine)
# Kryds/BBB pin-layout:
#   ledRL = Pin(0)  ledYL = Pin(1)  ledGL = Pin(2)   -> Venstre lys (bruges her)
#   ledRR = Pin(3)  ledYR = Pin(4)  ledGR = Pin(5)   -> Højre lys (ikke brugt i dette program)
#
# Statemachine: state0 (Grøn) -> state1 (Gul) -> state2 (Rød) -> state0 ...
# Samme princip som slides: hver state er en funktion der "return'er" næste state.

from machine import Pin
from time import sleep


def get_int(prompt, low, high):
    while True:
        try:
            value = int(input(prompt))
            if low <= value <= high:
                return value
            print(f"Enter a value between {low} and {high}.")
        except ValueError:
            print("Please type a whole number.")


ledRL = Pin(0, Pin.OUT)
ledYL = Pin(1, Pin.OUT)
ledGL = Pin(2, Pin.OUT)

ledRR = Pin(3, Pin.OUT)
ledYR = Pin(4, Pin.OUT)
ledGR = Pin(5, Pin.OUT)

groen_tid = get_int("Enter a 1-20 seconds for green led: ", 1, 20)
gul_tid = get_int("Enter a 1-20 seconds for yellow led: ", 1, 10)
roed_tid = get_int("Enter a 1-20 seconds for red led: ", 1, 20)


def alle_slukket():
    ledRL.value(0)
    ledYL.value(0)
    ledGL.value(0)
    
    ledRR.value(0)
    ledYR.value(0)
    ledGR.value(0)


def state_groen():
    alle_slukket()
    ledGL.value(1)
    ledGR.value(1)
    print("Green... ready...")
    sleep(groen_tid)
    return state_gul


def state_gul():
    alle_slukket()
    ledYL.value(1)
    ledYR.value(1)
    print("Yellow... ready...")
    sleep(gul_tid)
    return state_roed


def state_roed():
    alle_slukket()
    ledRL.value(1)
    ledRR.value(1)
    print("Red... ready...")
    sleep(roed_tid)
    return state_groen


try:
    state = state_groen        # initial state
    while state:
        state = state()        # kør statemachine
        
except KeyboardInterrupt:
    alle_slukket()
    print("Stoppet, alle LED'er slukket.")
