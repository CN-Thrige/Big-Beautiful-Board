from machine import Pin

# Init
IRSensor = Pin(28, Pin.IN)

# Variabler
trueCounter = 0
falseCounter = 0
loopCount = 5


# Task
def IR_Task():
    global trueCounter, falseCounter
    for tal in range(loopCount):
        Status = IR_GetValue()
        if Status == True:
            trueCounter += 1
        else:
            falseCounter += 1
    if trueCounter == 3:
        print("Jeg køre meget fint og ser ik noget sort")
        trueCounter = 0
        falseCounter = 0
    elif falseCounter == 3:
        print("Jeg ser sort")
        trueCounter = 0
        falseCounter = 0


# Get
def IR_GetValue():
    value = IRSensor.value()
    if value == 0:
        return True
    else:
        return False