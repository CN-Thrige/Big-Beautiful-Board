from machine import Pin
from time import sleep

#this code makes the inbuild led on the Pico to blink.

led = Pin('LED', Pin.OUT)

while True:
    led.value(not led.value())
    sleep(0.5)
