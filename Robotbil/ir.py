from machine import Pin

IRSensor = Pin(28, Pin.IN)

def IR_GetValue():
    # Returnerer True hvis den ser sort/kant (lavt signal)
    return IRSensor.value() == 0

def IR_Task():
    # Returnerer direkte tilstand uden at tælle i en blokerende løkke
    return IR_GetValue()