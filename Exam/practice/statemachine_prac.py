from machine import Pin
from time import sleep
import random

u1 = Pin(6, Pin.IN, Pin.PULL_UP)
u2 = Pin(7, Pin.IN, Pin.PULL_UP)

d1 = Pin(0, Pin.OUT)
d2 = Pin(1, Pin.OUT)
d3 = Pin(2, Pin.OUT)

d4 = Pin(3, Pin.OUT)
d5 = Pin(4, Pin.OUT)
d6 = Pin(5, Pin.OUT)

state = 0 

def all_off():
    d1.off(); d2.off(); d3.off(); d4.off(); d5.off(); d6.off()

def main():
    global state
    
    state = d1_state()
    
    while state:
        state
        
def d1_state():
    all_off()
    print("> Red on\n")
    d1.on()
    sleep(0.5)
    print("> Red off\n")
    sleep(0.5)
    return d2_state()

def d2_state():
    all_off()
    print("> Yellow on\n")
    d2.on()
    sleep(0.5)
    print("> Yellow off\n")
    sleep(0.5)
    return d3_state()


def d3_state():
    all_off()
    print("> Green on\n")
    d3.on()
    sleep(0.5)
    print("> Green off\n")
    sleep(0.5)
    return d4_state()

def d4_state():
    all_off()
    print("> Red on\n")
    d4.on()
    sleep(0.5)
    print("> Red off\n")
    sleep(0.5)
    return d5_state()

def d5_state():
    all_off()
    print("> Yellow on\n")
    d5.on()
    sleep(0.5)
    print("> Yellow off\n")
    sleep(0.5)
    return d6_state()

def d6_state():
    all_off()
    print("> Green on\n")
    d6.on()
    sleep(0.5)
    print("> Green off\n")
    sleep(0.5)
    return d1_state()    

main()
