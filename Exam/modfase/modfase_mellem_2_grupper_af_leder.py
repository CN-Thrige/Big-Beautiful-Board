from machine import Pin
from time import sleep

gruppe_a = [Pin(0, Pin.OUT), Pin(2, Pin.OUT)]
gruppe_b = [Pin(1, Pin.OUT), Pin(3, Pin.OUT)]

while True:
    for led in gruppe_a:
        led.on()
    for led in gruppe_b:
        led.off()
    sleep(0.5)

    for led in gruppe_a:
        led.off()
    for led in gruppe_b:
        led.on()
    sleep(0.5)
