from machine import Pin
from time import sleep
import dev_test

u1 = Pin(6, Pin.IN, Pin.PULL_UP)
u2 = Pin(7, Pin.IN, Pin.PULL_UP)

d1 = Pin(0, Pin.OUT)
d2 = Pin(1, Pin.OUT)
d3 = Pin(2, Pin.OUT)

d4 = Pin(3, Pin.OUT)
d5 = Pin(4, Pin.OUT)
d6 = Pin(5, Pin.OUT)

sleep_var = 0.5

#red = [d1, d4]
#yellow = [d2, d5]
#green = [d3, d6]

def main():
    d1.off(), d2.off(), d3.off()
    
    while True:
        btn_led()
        blinking_led()
        test()
        test_two()
        test_3()   
        
def btn_led():
    d1.value(u1.value(0))
    
def blinking_led():
    while True: 
        d1.value(not d1.value())
        sleep(sleep_var)
        
def test():
    for i in range(1,11):
        d1.value(0)
        sleep(sleep_var)
        d1.value(1)
        sleep(sleep_var)

        if u1.value() == 0:
            break
    
    print("DONE!")

def test_two():
    while True:
        d1.on()
        sleep(sleep_var)
        d1.off()
    
        d2.on()
        sleep(sleep_var)
        d2.off()
        
        if u1.value()==0:
            break
            
def test_3():
    for i in range(1,21):
        d1.value(0)
        sleep(sleep_var)
        d1.value(1)
    
        d2.value(0)
        sleep(sleep_var)
        d2.value(1)
        
        if u1.value()==0:
            break

main()
