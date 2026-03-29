from machine import Pin
from time import sleep
# Tidskonstant til sleep
tid = 2 # 3 sekunds pause
led1 = Pin(0, Pin.OUT) #led kan tilsluttes GP0
led2 = Pin(1, Pin.OUT) #led kan tilsluttes GP1
led3 = Pin(2, Pin.OUT) #led kan tilsluttes GP2
led4 = Pin(3, Pin.OUT) #led kan tilsluttes GP3
led5 = Pin(4, Pin.OUT) #led kan tilsluttes GP4
led6 = Pin(5, Pin.OUT) #led kan tilsluttes GP5

# Nu skal led'erne tændes
led1.on()
sleep(tid)
led2.on()
sleep(tid)
led3.on()
sleep(tid)
led4.on()
sleep(tid)
led5.on()
sleep(tid)
led6.on()
sleep(tid)

# Nu skal led'erne slukkes
led1.off()
led2.off()
led3.off()
led4.off()
led5.off()
led6.off()

