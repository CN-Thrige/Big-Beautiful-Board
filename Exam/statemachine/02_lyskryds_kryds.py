# 02 - Lyskryds, fuldt kryds (statemachine med 6 states)
# Pin-layout:
#   ledRL = Pin(0)  ledYL = Pin(1)  ledGL = Pin(2)   -> Venstre lys (fx Nord-Syd)
#   ledRR = Pin(3)  ledYR = Pin(4)  ledGR = Pin(5)   -> Højre lys  (fx Øst-Vest)
#
# Statemachine:
#   S0: GL grøn / RR rød
#   S1: YL gul  / RR rød
#   S2: RL rød  / RR rød   (alt rødt, sikkerhedspause)
#   S3: RL rød  / GR grøn
#   S4: RL rød  / YR gul
#   S5: RL rød  / RR rød   (alt rødt, sikkerhedspause)
#   S5 -> S0 (loop)

from machine import Pin
from time import sleep


def get_int(prompt, lo, hi):
    while True:
        try:
            val = int(input(prompt))
            if lo <= val <= hi:
                return val
            print(f"Enter a value between {lo} and {hi}.")
        except ValueError:
            print("Please type a whole number.")


ledRL = Pin(0, Pin.OUT)
ledYL = Pin(1, Pin.OUT)
ledGL = Pin(2, Pin.OUT)
ledRR = Pin(3, Pin.OUT)
ledYR = Pin(4, Pin.OUT)
ledGR = Pin(5, Pin.OUT)

groen_tid = get_int("Grøn tid pr. retning i sekunder (1-30): ", 1, 30)
gul_tid = get_int("Gul tid i sekunder (1-5): ", 1, 5)
alrod_tid = get_int("Alt-rødt sikkerhedspause i sekunder (1-5): ", 1, 5)


def saet(rl, yl, gl, rr, yr, gr):
    ledRL.value(rl); ledYL.value(yl); ledGL.value(gl)
    ledRR.value(rr); ledYR.value(yr); ledGR.value(gr)


def s0_groen_venstre():
    saet(0, 0, 1,  1, 0, 0)
    print("S0: Venstre grøn / Højre rød")
    sleep(groen_tid)
    return s1_gul_venstre


def s1_gul_venstre():
    saet(0, 1, 0,  1, 0, 0)
    print("S1: Venstre gul / Højre rød")
    sleep(gul_tid)
    return s2_alt_roedt_a


def s2_alt_roedt_a():
    saet(1, 0, 0,  1, 0, 0)
    print("S2: Alt rødt (sikkerhedspause)")
    sleep(alrod_tid)
    return s3_groen_hoejre


def s3_groen_hoejre():
    saet(1, 0, 0,  0, 0, 1)
    print("S3: Venstre rød / Højre grøn")
    sleep(groen_tid)
    return s4_gul_hoejre


def s4_gul_hoejre():
    saet(1, 0, 0,  0, 1, 0)
    print("S4: Venstre rød / Højre gul")
    sleep(gul_tid)
    return s5_alt_roedt_b


def s5_alt_roedt_b():
    saet(1, 0, 0,  1, 0, 0)
    print("S5: Alt rødt (sikkerhedspause)")
    sleep(alrod_tid)
    return s0_groen_venstre


try:
    state = s0_groen_venstre    # initial state
    while state:
        state = state()
except KeyboardInterrupt:
    saet(0, 0, 0, 0, 0, 0)
    print("Stoppet, alle LED'er slukket.")
