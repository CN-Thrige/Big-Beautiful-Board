import TOF # Henter I2C-sensorfunktionen fra tof.py

def constrain(val, min_val, max_val):
    return max(min_val, min(val, max_val))

sidst_fejl = 0

def wall_follow_step(robot):
    global sidst_fejl

    SET_PUNKT = 22.0
    BASIS_FART = 45

    # 1. Hent afstand via I2C
    maal_afstand_cm = TOF.TOF_GetDistance_Fast()

    # 2. MISTET VÆG (> 50 cm / intet signal) -> Søg mod højre
    if maal_afstand_cm is None:
        sidst_fejl = 0
        robot.drive(60, 20)
        return

    # 3. NØDSVING / KRITISK VENSTRESVING (Muren < 11 cm)
    if maal_afstand_cm < 11.0:
        sidst_fejl = 0
        robot.drive(-10, 65)
        return

    # 4. NORMAL PD-REGULERING
    fejl = maal_afstand_cm - SET_PUNKT
    delta_fejl = fejl - sidst_fejl
    sidst_fejl = fejl

    if fejl > 0:
        KP = 1.0
        KD = 1.8
    else:
        KP = 2.2
        KD = 1.5

    justering = (KP * fejl) + (KD * delta_fejl)

    venstre = int(constrain(BASIS_FART + justering, 0, 75))
    hoejre = int(constrain(BASIS_FART - justering, 0, 75))

    robot.drive(venstre, hoejre)