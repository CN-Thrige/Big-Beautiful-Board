from machine import Pin, ADC
from time import sleep

adc = ADC(Pin(26))
green = Pin(2, Pin.OUT)
yellow = Pin(1, Pin.OUT)
red = Pin(0, Pin.OUT)

SCALE = 12 / 3.3   # replace with R2/(R1+R2) from your actual divider

def read_voltage():
    raw = adc.read_u16()
    adc_voltage = (raw / 65535) * 3.3
    return adc_voltage * SCALE

def all_off():
    green.off(); yellow.off(); red.off()

while True:
    v = read_voltage()
    all_off()
    if v >= 10:
        green.on()
    elif v >= 6:
        yellow.on()
    elif v >= 3:
        red.on()
    else:
        red.on()
        sleep(0.2)
        red.off()
        sleep(0.2)
        continue
    sleep(0.5)
