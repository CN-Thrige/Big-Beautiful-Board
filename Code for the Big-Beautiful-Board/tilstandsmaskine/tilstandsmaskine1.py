from machine import Pin
from time import sleep_ms

u1 = Pin(6, Pin.IN, Pin.PULL_UP)
u2 = Pin(7, Pin.IN, Pin.PULL_UP)

d1 = Pin(0, Pin.OUT)
d2 = Pin(1, Pin.OUT)
d3 = Pin(2, Pin.OUT)

d4 = Pin(3, Pin.OUT)
d5 = Pin(4, Pin.OUT)
d6 = Pin(5, Pin.OUT)

iTimer_ms = 0  # Bruges som stopur til at generere et TIMEOUT event

# STATE

STATE_INIT = 1
STATE_RED = 2
STATE_RED_ACCEPT_BTN = 3
STATE_GREEN = 4

# EVENT

EVENT_INIT_OK = False
EVENT_TIMER = False
EVENT_BTN = False


# @brief Sets the timer seconds. When timer runs out, EVENT_TIMER is thrown
#
# @param[in] None
# @param[out] None
# @return None
#
# @warning None

def smSetTimer(iTimerValue_sec):
    global iTimer_ms
    iTimer_ms = iTimerValue_sec


# EVENT tjek

def checkEventTimer():  # kaldt en task, udfører en fast opgave
    # TODO: Lav en funktion der tæller iTimerValue_sec ned. Når den bliver 0, skal event sættes til True
    # Funktionen skal kaldes fra main loop med 100 ms interval
    if iTimer_ms > 0:
        iTimer_ms = iTimer_ms - 100
        if iTimer_ms <= 0:
            EVENT_TIMER = True
            print("Event timer ")


# Initier programmet (startup), inden vi starter selve programmet

# Start med at sætte aktiv state til den vi skal starte med efter startup:
smActiveState = STATE_INIT
EVENT_INIT_OK = True
EVENT_TIMER = True

# Tilstandsmaskine task (100 ms)

while True:
    print(f"Active state = {smActiveState}")
    # STATE_A

    if smActiveState == STATE_INIT:

        if EVENT_INIT_OK == True:
            # ACTION:
            d1.on()  # initialize
            d2.off()
            d3.off()  # green off

            # timer = 10 seconds
            iTimer_ms = 10000

            # TRANSITION:
            smActiveState = STATE_RED

            # Reset event:
            EVENT_INIT_OK = False
    # STATE_RED

    elif smActiveState == STATE_RED:
        if EVENT_TIMER == True:
            # ACTION:
            iTimer_ms = 10000

            # TRANSITION:
            smActiveState = STATE_RED_ACCEPT_BTN
            # Reset event:
            EVENT_TIMER = False
        # STATE_RED

    elif smActiveState == STATE_RED_ACCEPT_BTN:
        if EVENT_TIMER == True:
            # ACTION:
            d1.off()  # initialize
            d2.off()
            d3.on()  # green off

            # timer = 20 seconds
            iTimer_ms = 20000

            # TRANSITION:
            smActiveState = STATE_GREEN
            # Reset event:
            EVENT_TIMER = False

        elif EVENT_BTN == True:
            d2.on()
            if iTimer_ms > 5000:
                iTimer_ms = 5000

            iTimer_ms = 10000
            EVENT_BTN = False

    elif smActiveState == STATE_GREEN:
        if EVENT_TIMER == True:
            # ACTION:
            d1.on()
            d3.off()

            iTimer_ms = 10000

            # TRANSITION:
            smActiveState = STATE_RED
            # Reset event:
            EVENT_TIMER = False
        # STATE_RED

# Tjek for events:
# TODO: Lav de nødvendig funktioner som skal kaldes for at tjekke for events.F.eks. checkEventTimer()
# Kør tilstandsmaskinen i et loop på 10 gange i sekundet (100 ms interval):'

# lav et event der får hele tilstandsmaksinen til at virke
# der mangler en knap?
checkEventTimer()

sleep_ms(100)
