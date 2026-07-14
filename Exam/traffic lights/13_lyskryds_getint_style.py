from machine import Pin
from time import sleep

ns_red, ns_yellow, ns_green = Pin(0, Pin.OUT), Pin(1, Pin.OUT), Pin(2, Pin.OUT)
ev_red, ev_yellow, ev_green = Pin(3, Pin.OUT), Pin(4, Pin.OUT), Pin(5, Pin.OUT)

def get_int(prompt, lo, hi):
    while True:
        try:
            val = int(input(prompt))
            if lo <= val <= hi:
                return val
            print(f"Enter a value between {lo} and {hi}.")
        except ValueError:
            print("Please type a whole number.")

green_time = get_int("Green time per direction in seconds (1-30): ", 1, 30)
yellow_time = get_int("Yellow time in seconds (1-10): ", 1, 10)
all_red_time = get_int("All-red safety time in seconds (1-5): ", 1, 5)

def set_lights(ns, ev):
    ns_red.value(ns[0]); ns_yellow.value(ns[1]); ns_green.value(ns[2])
    ev_red.value(ev[0]); ev_yellow.value(ev[1]); ev_green.value(ev[2])

def all_off():
    set_lights((0,0,0), (0,0,0))

def all_red():
    set_lights((1,0,0), (1,0,0))
    sleep(all_red_time)
    return ns_ready

def ns_ready():
    set_lights((1,1,0), (1,0,0))
    sleep(yellow_time)
    return ns_go

def ns_go():
    set_lights((0,0,1), (1,0,0))
    sleep(green_time)
    return ns_stop

def ns_stop():
    set_lights((0,1,0), (1,0,0))
    sleep(yellow_time)
    return all_red2

def all_red2():
    set_lights((1,0,0), (1,0,0))
    sleep(all_red_time)
    return ev_ready

def ev_ready():
    set_lights((1,0,0), (1,1,0))
    sleep(yellow_time)
    return ev_go

def ev_go():
    set_lights((1,0,0), (0,0,1))
    sleep(green_time)
    return ev_stop

def ev_stop():
    set_lights((1,0,0), (0,1,0))
    sleep(yellow_time)
    return all_red

try:
    state = all_red
    while state:
        state = state()
except KeyboardInterrupt:
    all_off()
    print("Stopped, outputs cleared.")
