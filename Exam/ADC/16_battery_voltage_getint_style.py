from machine import Pin, ADC
from time import sleep

adc = ADC(Pin(26))
green = Pin(2, Pin.OUT)
yellow = Pin(1, Pin.OUT)
red = Pin(0, Pin.OUT)

def get_int(prompt, lo, hi):
    while True:
        try:
            val = int(input(prompt))
            if lo <= val <= hi:
                return val
            print(f"Enter a value between {lo} and {hi}.")
        except ValueError:
            print("Please type a whole number.")

green_threshold = get_int("Green threshold in volts (1-12): ", 1, 12)
yellow_threshold = get_int("Yellow threshold in volts (1-12): ", 1, 12)
red_threshold = get_int("Red threshold in volts (0-12): ", 0, 12)

SCALE = 12 / 3.3   # replace with R2/(R1+R2) from your actual divider

def read_voltage():
    raw = adc.read_u16()
    adc_voltage = (raw / 65535) * 3.3
    return adc_voltage * SCALE

def all_off():
    green.off(); yellow.off(); red.off()

try:
    while True:
        v = read_voltage()
        all_off()
        if v >= green_threshold:
            green.on()
        elif v >= yellow_threshold:
            yellow.on()
        elif v >= red_threshold:
            red.on()
        else:
            red.on()
            sleep(0.2)
            red.off()
            sleep(0.2)
            continue
        sleep(0.5)
except KeyboardInterrupt:
    all_off()
    print("Stopped, outputs cleared.")
