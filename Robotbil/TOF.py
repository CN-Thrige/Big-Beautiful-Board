from machine import Pin, time_pulse_us

# Konfiguration af PWM input-pin (GP5)
pwm_pin = Pin(5, Pin.IN)


def TOF_Init():
    """Initialiserer TOF PWM-modulet."""
    print("PWM TOF klar på GP5!")


def TOF_GetDistance_Fast():
    """Returnerer afstanden i cm baseret på PWM-pulslængden.

    Returnerer None ved timeout eller fejl.
    """
    try:
        # Måler hvor mange mikrosekunder pinnen er HØJ (1)
        # Timeout er sat til 100.000 µs (100 ms)
        puls_us = time_pulse_us(pwm_pin, 1, 100000)

        # Hvis sensoren har timeout eller er uden for rækkevidde
        if puls_us < 0:
            return None

        # Omregner µs til cm (/ 100.0)
        afstand_cm = puls_us / 100.0

        # Filtrerer åbenlyse fejl-stænk fra (f.eks. over 200 cm)
        if afstand_cm <= 0 or afstand_cm > 200:
            return None

        return afstand_cm

    except Exception:
        return None