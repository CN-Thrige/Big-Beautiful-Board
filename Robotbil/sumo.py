import time
import ir
import TOF, VL53L0X

start_tid = 0
tilstand = "SOEG"
t_start = 0
tid_tilbage = 0


def kor_sumo_step(robot):
    global start_tid, tilstand, t_start, tid_tilbage

    nu = time.ticks_ms()

    # Læs filtrerede sensorværdier
    ser_kant = ir.IR_Task()
    afstand_cm = tof.TOF_GetDistance()

    # 1. Prio: Kant opdaget (IR)
    if ser_kant and tilstand != "BAK" and tilstand != "DREJ":
        tilstand = "BAK"
        start_tid = nu
        robot.drive(-60, -60)

    # 2. Prio: Bak og drej væk fra kanten
    elif tilstand == "BAK":
        if time.ticks_diff(nu, start_tid) >= 300:
            tilstand = "DREJ"
            start_tid = nu
            robot.drive(70, -70)

    elif tilstand == "DREJ":
        if time.ticks_diff(nu, start_tid) >= 250:
            tilstand = "SOEG"

    # 3. Prio: Søg, Sweep og Angreb (baseret på TOF afstand)
    elif tilstand == "SOEG":
        robot.drive(35, -35)
        if 2 < afstand_cm < 90:
            t_start = nu
            tilstand = "SWEEP"

    elif tilstand == "SWEEP":
        robot.drive(35, -35)
        if afstand_cm >= 90 or afstand_cm < 2:
            t_slut = nu
            passage_tid = time.ticks_diff(t_slut, t_start)
            tid_tilbage = passage_tid // 2

            tilstand = "DREJ MOD MIDTE"
            start_tid = nu
            robot.drive(-35, 35)

    elif tilstand == "DREJ MOD MIDTE":
        if time.ticks_diff(nu, start_tid) >= tid_tilbage:
            tilstand = "ANGREB"

    elif tilstand == "ANGREB":
        robot.drive(100, 100)
        if afstand_cm >= 90:
            tilstand = "SOEG"

    return afstand_cm