## spørgsmålet - 25 points 

2 tilføj endnu en lysdiode og modificer programmet så Pin1 dioden forsætter med at at blinke. og den tilføjerede lysdiode blinker i modfase med dne første diode. (den ene er slukket mens den anden lyser og omvendt) - 10 points 

tilføj en knap og modificer programmet så føglende opnås
a. mens knappen er trykket skal: 
- i lysdioden blinker i takt 
b. når knappen er sluppet skal 
i. lysdioden blinker i modfase - 15 points 

## først kodeblok uden knap - 10 points 

'{ from machine import Pin
from time import sleep

p1 = Pin(0, Pin.OUT)  # red
p0 = Pin(1, Pin.OUT)  # yellow

while True:
    p0.on()
    sleep(0.5)
    p0.off()
    p1.on()
    sleep(0.5)
    p1.off()}
    

## med knappen giver 25 points 

