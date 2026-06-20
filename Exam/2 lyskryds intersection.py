from machine import Pin
from time import sleep

ns_red, ns_yellow, ns_green = Pin(0, Pin.OUT), Pin(1, Pin.OUT), Pin(2, Pin.OUT)
ev_red, ev_yellow, ev_green = Pin(3, Pin.OUT), Pin(4, Pin.OUT), Pin(5, Pin.OUT)

def set_lights(ns, ev):
    ns_red.value(ns[0]); ns_yellow.value(ns[1]); ns_green.value(ns[2])
    ev_red.value(ev[0]); ev_yellow.value(ev[1]); ev_green.value(ev[2])

def all_red():
    set_lights((1,0,0), (1,0,0))
    sleep(1.0)
    return ns_ready

def ns_ready():
    set_lights((1,1,0), (1,0,0))
    sleep(1.0)
    return ns_go

def ns_go():
    set_lights((0,0,1), (1,0,0))
    sleep(5.0)
    return ns_stop

def ns_stop():
    set_lights((0,1,0), (1,0,0))
    sleep(1.5)
    return all_red2

def all_red2():
    set_lights((1,0,0), (1,0,0))
    sleep(1.0)
    return ev_ready

def ev_ready():
    set_lights((1,0,0), (1,1,0))
    sleep(1.0)
    return ev_go

def ev_go():
    set_lights((1,0,0), (0,0,1))
    sleep(5.0)
    return ev_stop

def ev_stop():
    set_lights((1,0,0), (0,1,0))
    sleep(1.5)
    return all_red

state = all_red
while state:
    state = state()
