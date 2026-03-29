from machine import Pin #Import af funktionen Pin
from time import sleep # Import af funktionen sleep
# Tidskonstant til sleep
tid = 3 # 3 sekunds pause
led1 = Pin(0, Pin.OUT) #led tilsluttes GP0

# Nu bliver led'en tændt
led1.on()
if led1.value() == 1:
    print("Tændt")
else:
    print("Slukket")
# Programmet stopper i 3 sekunder!
sleep(tid)

# Nu bliver led'en slukket
led1.off()
if led1.value() == 1:
    print("Tændt")
else:
    print("Slukket")