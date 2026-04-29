from machine import Pin
from time import sleep


led1 = Pin(8, Pin.OUT) # led 1 - buttom 
led2 = Pin(9, Pin.OUT) # led 2 - bottom left
led3 = Pin(10, Pin.OUT) # led 3 - middle 
led4 = Pin(11, Pin.OUT) # led 4 - top left
led5 = Pin(12, Pin.OUT) # led 5 - top 
led6 = Pin(13, Pin.OUT) # led 6 - top right
led7 = Pin(14, Pin.OUT) # led 7 - bottum right 
led8 = Pin(15, Pin.OUT) # led 8 - dot



led_lst  = [led1, led2, led3, led4, led5, led6, led7, led8]

while True:
    for led in led_lst:
        led.off()
        sleep(2)

    for led in led_lst:
        led.on()
        sleep(2)
