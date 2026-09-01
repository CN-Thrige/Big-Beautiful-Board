from machine import Pin, PWM
from time import sleep

u1 = Pin(6, Pin.IN, Pin.PULL_UP)
u2 = Pin(7, Pin.IN, Pin.PULL_UP)

d1 = Pin(0, Pin.OUT)
d1_pwm =  PWM(Pin(0))

d2 = Pin(1, Pin.OUT)
d3 = Pin(2, Pin.OUT)

d4 = Pin(3, Pin.OUT)
d5 = Pin(4, Pin.OUT)
d6 = Pin(5, Pin.OUT)

d1_pwm.freq(1000)

brightness_pct = 0
STEP = 5
SPEED = 10
direction = 1

def main():
    #Husk at kryds dem ud når du er færdig.
    #opg1()
    #opg2()
    #opg3()
    #opg4()
    opg5()

def opg1():
    """Opgave 1 – Grundlæggende blink (10 point)
    Skriv et MicroPython-program til Pico'en der:
    a. Tilslutter en lysdiode til Pin 1
    b. Får lysdioden til at blinke med 1 sekunds mellemrum (tændt 1 sek, slukket 1 sek)"""
    while True:
        d2.on()
        sleep(1)
        d2.off()
        sleep(1)

def opg2(): #rettet!
    """Opgave 2 – To lysdioder i modfase (15 point)
    Tag udgangspunkt i programmet fra opgave 1 og modificer det så:
    a. Lysdioden på Pin 1 fortsætter med at blinke
    b. Tilføj endnu en lysdiode og få den til at blinke i modfase med den første (den ene er tændt mens den anden er slukket, og omvendt)"""
    while True:
        d1.on()
        d2.off()
        sleep(0.5)

        d2.on()
        d1.off()
        sleep(0.5)

def opg3():
    """Opgave 3 – Knapstyret blink (20 point)
    Tilføj en trykknap (med korrekt pull-up eller pull-down, alt efter hvordan den er tilsluttet på jeres print) og modificer programmet så:
    a. Mens knappen er trykket ned, skal de to lysdioder blinke i takt (begge tændt/slukket samtidig)
    b. Når knappen slippes, skal lysdioderne igen blinke i modfase (som i opgave 2)"""
    while True:
        if u1.value() == 0:
            d1.on()
            d2.on()
    
            sleep(0.5)
    
            d1.off()
            d2.off()
            sleep(0.5)
            
        else:
            d1.on()
            d2.off()
            sleep(0.5)

            d2.on()
            d1.off()
            sleep(0.5)


def opg4(): #rettet og virker 
    global brightness_pct, STEP, direction 
    """Opgave 4 – PWM lysstyrke (20 point)
    Brug PWM til at regulere lysstyrken på d1 i stedet for bare on/off:
    a. Få d1 til at "ånde" (pulsere op og ned i lysstyrke) ved at øge duty cycle fra 0% til 100% og derefter tilbage til 0%, i et jævnt loop
    b. Brug knap u1 til at ændre hastigheden af pulseringen: når knappen er trykket ned, skal ånde-effekten gå dobbelt så hurtigt som normalt"""

    try:
        while True:
            duty = int(brightness_pct / 100 * 65535)
            d1_pwm.duty_u16(duty)
            
           
        
            if brightness_pct >= 100:
                direction = -1
                
            elif brightness_pct <= 0:
                direction = 1
            
            sleep(0.15)

            current_step = STEP
                
            if u1.value() == 0: #Undgå at ændre de globale variabler permanent 
                #det vil sige, hvis jeg skifter step undervejs, vil den stadigvæk være fanget i den global værdi step!
                current_step = STEP * 2
                sleep(0.15)
            
            brightness_pct = brightness_pct + current_step * direction

                
            
    except KeyboardInterrupt:
        led_pwm.duty_u16(0)
        led_pwm.deinit()

def all_off():
    d1.off()
    d2.off()
    d3.off()


def state_green():
    all_off()
    d3.on()
    print("Running green")
    sleep(5.5)

    if u1.value() == 0:
        for i in range(5):
            # tænd alle
            sleep(0.5)
            # sluk alle
            sleep(0.5)
            
    return state_yellow


def state_yellow():
    all_off()
    d2.on()
    print("Running yellow")
    sleep(1.5)
    return state_red


def state_red():
    all_off()
    d1.on()
    print("Running Red")
    sleep(5.5)
    return state_green


def opg5():
    """Opgave 5 – Trafiklys statemachine (25 point)
    lav en statemachine der styrer et trafiklys med d1 (rød), d2 (gul) og d3 (grøn) og modificer programmet så følgende opnås
    a. trafiklyset skifter automatisk mellem rød, rød+gul, grøn og gul i en fast rækkefølge med passende tidsintervaller
    b. tilføj en knap og modificer programmet så
    i. når knappen trykkes mens lyset er grønt, skal alle tre lysdioder blinke samtidig 5 gange
    ii. statemachinen skal derefter fortsætte fra rød"""

    state = state_green  # startstate
    try:
        while state:
            state = state()  # kør den nuværende state, få den næste igen
    except KeyboardInterrupt:
        all_off()
        print("Statemachine stoppet.")
    
main()
