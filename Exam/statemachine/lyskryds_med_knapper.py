# 03 - Lyskryds med kaldeknapper (input-styret statemachine)
# Pin-layout:
#   button1 = Pin(6, PULL_UP)  -> kald "skift til Højre grøn" (aktiv lav, dvs. 0 = trykket)
#   button2 = Pin(7, PULL_UP)  -> kald "skift til Venstre grøn"
#   ledRL = Pin(0)  ledYL = Pin(1)  ledGL = Pin(2)   -> Venstre lys
#   ledRR = Pin(3)  ledYR = Pin(4)  ledGR = Pin(5)   -> Højre lys
#
# Samme statemachine som 02, men den grønne fase kan afkortes hvis der
# trykkes på den knap der "kalder" den modsatte retnings grønne lys.
# Min. grøn-tid overholdes altid, så lyset ikke skifter for hurtigt.

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


button1 = Pin(6, Pin.IN, Pin.PULL_UP)   # kalder Højre grøn
button2 = Pin(7, Pin.IN, Pin.PULL_UP)   # kalder Venstre grøn

ledRL = Pin(0, Pin.OUT)
ledYL = Pin(1, Pin.OUT)
ledGL = Pin(2, Pin.OUT)
ledRR = Pin(3, Pin.OUT)
ledYR = Pin(4, Pin.OUT)
ledGR = Pin(5, Pin.OUT)

min_groen_tid = get_int("Minimum grøn tid i sekunder (1-10): ", 1, 10)
maks_groen_tid = get_int("Maksimum grøn tid i sekunder (min-30): ", min_groen_tid, 30)
gul_tid = get_int("Gul tid i sekunder (1-5): ", 1, 5)
alrod_tid = get_int("Alt-rødt sikkerhedspause i sekunder (1-5): ", 1, 5)


def saet(rl, yl, gl, rr, yr, gr):
    ledRL.value(rl); ledYL.value(yl); ledGL.value(gl)
    ledRR.value(rr); ledYR.value(yr); ledGR.value(gr)


def groen_med_afkortning(kalder_knap):
    """Hold grøn i min_groen_tid, derefter vent til enten maks_groen_tid
    er nået, eller kalder_knap bliver trykket (værdi 0, fordi PULL_UP)."""
    sleep(min_groen_tid)
    tid_gaaet = min_groen_tid
    while tid_gaaet < maks_groen_tid:
        if kalder_knap.value() == 0:
            print("Kaldeknap trykket - afkorter grøn fase")
            break
        sleep(0.1)
        tid_gaaet += 0.1


def s0_groen_venstre():
    saet(0, 0, 1,  1, 0, 0)
    print("S0: Venstre grøn / Højre rød")
    groen_med_afkortning(button1)
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
    groen_med_afkortning(button2)
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
    state = s0_groen_venstre
    while state:
        state = state()
except KeyboardInterrupt:
    saet(0, 0, 0, 0, 0, 0)
    print("Stoppet, alle LED'er slukket.")
