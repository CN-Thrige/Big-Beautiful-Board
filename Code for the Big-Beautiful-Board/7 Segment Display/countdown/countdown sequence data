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

def one():
    led6.on()
    led7.on()
    led8.off()
    
def two():
    led1.on()
    led2.on()
    led3.on()
    led4.on()
    led5.on()
    led8.off()


def three():
    led5.on()
    led1.on()
    led2.on()
    led6.on()
    led4.on()
    led8.off()


def four():
    led7.on()
    led6.on()
    led3.on()
    led4.on()
    led8.off()


def five():
    led5.on()
    led4.on()
    led3.on()
    led6.on()
    led7.on()
    led8.off()


def six():
    led1.on()
    led2.on()
    led3.on()
    led4.on()
    led5.on()
    led7.on()
    led8.off()

def seven():
    led7.on()
    led6.on()
    led5.on()
    led8.off()

def eight():
    led1.on()
    led2.on()
    led3.on()
    led4.on()
    led5.on()
    led6.on()
    led7.on()
    led8.off()

def nine():
    led3.on()
    led4.on()
    led5.on()
    led6.on()
    led7.on()
    led8.off()

def sleep_function():
    while True:
        for led in led_lst:
            led.off()
