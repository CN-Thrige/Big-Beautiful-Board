from machine import Pin
from time import sleep

led1 = Pin(8, Pin.OUT)  # led 1 - buttom
led2 = Pin(9, Pin.OUT)  # led 2 - bottom left
led3 = Pin(10, Pin.OUT)  # led 3 - middle
led4 = Pin(11, Pin.OUT)  # led 4 - top left
led5 = Pin(12, Pin.OUT)  # led 5 - top
led6 = Pin(13, Pin.OUT)  # led 6 - top right
led7 = Pin(14, Pin.OUT)  # led 7 - bottum right

led_lst = [led1, led2, led3, led4, led5, led6, led7]

led5.on()
led4.on()
led3.on()
led2.on()

def one():
    led6.on()
    led7.on()


def two():
    led1.on()
    led2.on()
    led3.on()
    led6.on()
    led5.on()


def three():
    #led5.on()
    #led1.on()
    #led2.on()
    #led6.on()
   # led4.on()

    led5.on()
    led4.on()
    led3.on()
    led2.on()
    led1.on()

def four():
    led7.on()
    led6.on()
    led3.on()
    led4.on()


def five():
    led5.on()
    led4.on()
    led3.on()
    led7.on()
    led1.on()

def six():
    led1.on()
    led2.on()
    led3.on()
    led4.on()
    led5.on()
    led7.on()


def seven():
    led7.on()
    led6.on()
    led5.on()


def eight():
    led1.on()
    led2.on()
    led3.on()
    led4.on()
    led5.on()
    led6.on()
    led7.on()


def nine():
    led3.on()
    led4.on()
    led5.on()
    led6.on()
    led7.on()


def led_off():  # issue right now. this makes it so it does not work
    for led in led_lst:
        led.off()
