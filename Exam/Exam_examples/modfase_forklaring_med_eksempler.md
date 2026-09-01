# Eksamen eksempel med modfase 

## Spørgsmål
2 tilføj endnu en lysdiode og modificer programmet så Pin1 dioden forsætter med at at blinke. og den tilføjerede lysdiode blinker i modfase med dne første diode. (den ene er slukket mens den anden lyser og omvendt) - 10 points 

tilføj en knap og modificer programmet så føglende opnås
a. mens knappen er trykket skal: 
- i lysdioden blinker i takt 
b. når knappen er sluppet skal 
i. lysdioden blinker i modfase - 15 points

## modfase forklaring 

Modfase betyder omvendt el. modsat. 


## 10 points (reeksamen)

    from machine import Pin
    from time import sleep

    p1 = Pin(0, Pin.OUT)  # red
    p0 = Pin(1, Pin.OUT)  # yellow

        while True:
    
            p0.on()
            sleep(0.5)
            p0.off()
            p1.on()
            sleep(0.5)
            p1.off()
        
    
## 25 points (reeksamen)

    from machine import Pin
    from time import sleep
    
    button1 = Pin(6, Pin.IN, Pin.PULL_UP)
    
    p1 = Pin(0, Pin.OUT)  # red
    p0 = Pin(1, Pin.OUT)  # yellow
    
    led = p1, p0
    
    
    def task2():
        p0.on()
        sleep(0.5)
        p0.off()
    
        p1.on()
        sleep(0.5)
        p1.off()
    
    
    def task3():
        if button1.value() == 0:
            p0.on()
            p1.on()
    
            sleep(0.5)
    
            p0.off()
            p1.off()
            sleep(0.5)
    
    
    
        else:
            task2()
    
    
    while True:
        task3()

## 20 points (1. eksamen)
    from machine import Pin
    from time import sleep
    
    button1 = Pin(6, Pin.IN, Pin.PULL_UP)
    
    p1 = Pin(0, Pin.OUT)  #red
    p0 = Pin(1, Pin.OUT) #yellow
    
    
    while True:
        if button1.value() == 0:
            p0.on()
            sleep(0.5)
            print("Yellow")
            p0.off()
    
            p1.on()
            sleep(0.5)
            print("Red")
            p1.off()
