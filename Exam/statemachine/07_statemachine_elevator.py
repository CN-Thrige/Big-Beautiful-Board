"""
Statemachine - Elevator (3 etager)
-------------------------------------
Fra Statemachine_v2.pptx ("Elevator" slides). Elevatoren står stille
og venter på et etage-kald. Når en knap trykkes, kører den op eller
ned ét "skridt" (1 sekund pr. etage) indtil den når den ønskede etage.

Knapper: GP6 = etage 1, GP7 = etage 2, GP8 = etage 3
LED'er:  GP2 = etage 1, GP3 = etage 2, GP4 = etage 3 (viser hvor kabinen er)
"""

from machine import Pin
from time import sleep

button_floor1 = Pin(6, Pin.IN, Pin.PULL_UP)
button_floor2 = Pin(7, Pin.IN, Pin.PULL_UP)
button_floor3 = Pin(8, Pin.IN, Pin.PULL_UP)

led_floor1 = Pin(2, Pin.OUT)
led_floor2 = Pin(3, Pin.OUT)
led_floor3 = Pin(4, Pin.OUT)

TRAVEL_TIME = 1.0     # sekunder pr. etage
current_floor = 1
target_floor = 1


def show_current_floor():
    led_floor1.value(1 if current_floor == 1 else 0)
    led_floor2.value(1 if current_floor == 2 else 0)
    led_floor3.value(1 if current_floor == 3 else 0)


def state_idle():
    """Venter på et kald."""
    global target_floor
    show_current_floor()

    if button_floor1.value() == 0:
        target_floor = 1
        print("Kald til etage 1")
        return state_moving
    if button_floor2.value() == 0:
        target_floor = 2
        print("Kald til etage 2")
        return state_moving
    if button_floor3.value() == 0:
        target_floor = 3
        print("Kald til etage 3")
        return state_moving

    return state_idle


def state_moving():
    """Kører ét skridt nærmere target_floor, etage for etage."""
    global current_floor

    if current_floor == target_floor:
        print(f"Ankommet til etage {current_floor}")
        return state_idle

    if current_floor < target_floor:
        print(f"Kører op fra {current_floor}...")
        current_floor += 1
    else:
        print(f"Kører ned fra {current_floor}...")
        current_floor -= 1

    show_current_floor()
    sleep(TRAVEL_TIME)
    return state_moving


state = state_idle
try:
    while state:
        state = state()
        sleep(0.1)     # lille pause så knap-aflæsning ikke løber løbsk
except KeyboardInterrupt:
    led_floor1.off()
    led_floor2.off()
    led_floor3.off()
    print("Elevator stoppet.")
