"""
Hysterese-sløjfe - Termostat
--------------------------------
Fra Statemachine_v2.pptx: "Hysterese sløjfe" med eksemplet
on = 23 grader, off = 25 grader.

Pointen med hysterese: uden den ville en varmelegeme tænde/slukke
konstant lige omkring et enkelt sæt-punkt (f.eks. 24 grader) pga.
små udsving i målingen. Med et "on"- og et "off"-punkt undgår vi det.

Her simuleres temperaturen med et potmeter på ADC0 (0-3,3V -> 0-50°C).
Bytter du potmeteret ud med en rigtig temperatursensor, er koden den
samme - kun formlen der regner spænding om til grader skal ændres.
"""

from machine import ADC, Pin
from time import sleep

temp_sensor = ADC(Pin(26))
heater = Pin(2, Pin.OUT)     # LED/relæ der simulerer varmelegeme

ON_TEMP = 23.0     # tænd varmen når temperaturen kommer under denne
OFF_TEMP = 25.0     # sluk varmen når temperaturen kommer over denne

MAX_DIGITAL = 65535
MAX_VOLTAGE = 3.3
MAX_TEMP = 50.0     # 3,3V svarer til 50 grader i denne simulation

heater_on = False


def read_temperature():
    raw = temp_sensor.read_u16()
    voltage = raw / MAX_DIGITAL * MAX_VOLTAGE
    return voltage / MAX_VOLTAGE * MAX_TEMP


try:
    while True:
        temp = read_temperature()

        if heater_on:
            if temp >= OFF_TEMP:
                heater_on = False
        else:
            if temp <= ON_TEMP:
                heater_on = True

        heater.value(1 if heater_on else 0)
        status = "TÆNDT" if heater_on else "slukket"
        print(f"Temperatur: {temp:.1f}°C  ->  Varme: {status}")
        sleep(0.5)

except KeyboardInterrupt:
    heater.off()
    print("Termostat stoppet.")
