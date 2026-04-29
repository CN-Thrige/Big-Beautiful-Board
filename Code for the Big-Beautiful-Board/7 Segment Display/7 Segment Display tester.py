from machine import Pin
from time import sleep

#Thanks to CatDad for the code

LedSyv1 = Pin(8, Pin.OUT) #SyvSekment led 1
LedSyv2 = Pin(9, Pin.OUT) #SyvSekment led 2
LedSyv3 = Pin(10, Pin.OUT) #SyvSekment led 3
LedSyv4 = Pin(11, Pin.OUT) #SyvSekment led 4
LedSyv5 = Pin(12, Pin.OUT) #SyvSekment led 5
LedSyv6 = Pin(13, Pin.OUT) #SyvSekment led 6
LedSyv7 = Pin(14, Pin.OUT) #SyvSekment led 7
LedSyv8 = Pin(15, Pin.OUT) #SyvSekment led 8

LedSyvListe = [LedSyv1, LedSyv2, LedSyv3, LedSyv4, LedSyv5, LedSyv6, LedSyv7, LedSyv8]

while True:
    for led in LedSyvListe:
        led.off()

    for led in LedSyvListe:
        led.on()
        sleep(2)
