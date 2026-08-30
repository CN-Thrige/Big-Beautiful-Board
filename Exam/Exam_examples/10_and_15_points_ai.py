from machine import Pin
import time

button1 = Pin(6, Pin.IN, Pin.PULL_UP)

p1 = Pin(0, Pin.OUT)  # red
p0 = Pin(1, Pin.OUT)  # yellow

while True:
    if button1.value() == 0:
        # ---------- Knappen ER trykket: LED'erne blinker I TAKT ----------
        p1.value(1)
        p0.value(1)
        time.sleep(0.5)

        p1.value(0)
        p0.value(0)
        time.sleep(0.5)

    else:
        # ---------- Knappen ER IKKE trykket: LED'erne blinker i MODFASE ----------
        p1.value(1)
        p0.value(0)
        time.sleep(0.5)

        p1.value(0)
        p0.value(1)
        time.sleep(0.5)
