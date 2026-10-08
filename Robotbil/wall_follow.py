from motor import Motor, RobotDrive

def constrain(val, min_val, max_val):
    return max(min_val, min(val, max_val))

def wall_follow_step(robot, maal_afstand_cm):
    SET_PUNKT = 20       # Ønsket afstand til væggen i cm
    MAX_AFSTAND = 50     # Grænse for hvornår vi betragter væggen som "mistet"
    BASIS_FART = 60
    KP = 2.5

    # 1. Hvis afstanden er ugyldig eller væggen er mistet (> 50 cm):
    if maal_afstand_cm is None or maal_afstand_cm <= 0 or maal_afstand_cm > MAX_AFSTAND:
        print(f"Målt: {maal_afstand_cm} cm -> VÆG MISTET! Søger til højre...")
        # Drej blødt til højre ved at lade venstre hjul køre hurtigere end højre
        robot.drive(35, 10)
        return

    # 2. Normal PID-regulering når væggen er inden for rækkevidde
    fejl = maal_afstand_cm - SET_PUNKT
    justering = KP * fejl

    # Højre-monteret TOF-sensor:
    venstre_fart = int(constrain(BASIS_FART + justering, 15, 70))
    højre_fart   = int(constrain(BASIS_FART - justering, 15, 70))

    print(f"Målt: {maal_afstand_cm:.1f} cm | Fejl: {fejl:.1f} | L: {venstre_fart} | R: {højre_fart}")

    robot.drive(venstre_fart, højre_fart)