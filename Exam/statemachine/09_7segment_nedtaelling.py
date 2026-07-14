# 09 - 7-segment nedtælling ("Rocket launcher"-opgaven fra 7_segment.pptx)
# I stedet for at printe nedtællingen på skærmen, vises den på 7-segmentet.
#
# Pin-layout (JUSTER til hvilke ben der reelt er loddet til a-g på jeres print!
# Slides siger: "find ud af hvilke ben der er tilsluttet hvilke segmenter"):
#   a=GP10  b=GP11  c=GP12  d=GP13  e=GP14  f=GP15  g=GP16
#
# SEGMENT_ON = 1 hvis fælles-katode (segment tændes ved 1).
# Sæt SEGMENT_ON = 0 hvis I har fælles-anode i stedet.

from machine import Pin
from time import sleep

SEGMENT_ON = 1
SEGMENT_OFF = 0 if SEGMENT_ON == 1 else 1

segmenter = {
    "a": Pin(10, Pin.OUT), "b": Pin(11, Pin.OUT), "c": Pin(12, Pin.OUT),
    "d": Pin(13, Pin.OUT), "e": Pin(14, Pin.OUT), "f": Pin(15, Pin.OUT),
    "g": Pin(16, Pin.OUT),
}

# Hvilke segmenter der skal lyse for hvert ciffer 0-9
CIFRE = {
    0: "abcdef",
    1: "bc",
    2: "abdeg",
    3: "abcdg",
    4: "bcfg",
    5: "acdfg",
    6: "acdefg",
    7: "abc",
    8: "abcdefg",
    9: "abcdfg",
}


def get_int(prompt, lo, hi):
    while True:
        try:
            val = int(input(prompt))
            if lo <= val <= hi:
                return val
            print(f"Enter a value between {lo} and {hi}.")
        except ValueError:
            print("Please type a whole number.")


def vis_ciffer(tal):
    tal = tal % 10
    aktive = CIFRE[tal]
    for navn, pin in segmenter.items():
        pin.value(SEGMENT_ON if navn in aktive else SEGMENT_OFF)


def sluk_alt():
    for pin in segmenter.values():
        pin.value(SEGMENT_OFF)


start_tal = get_int("Start nedtælling fra (0-9): ", 0, 9)

try:
    for tal in range(start_tal, -1, -1):
        vis_ciffer(tal)
        print(tal)
        sleep(1)
    print("Affyring!")
    sleep(2)
    sluk_alt()
except KeyboardInterrupt:
    sluk_alt()
    print("Stoppet.")
