from time import sleep_ms
import TOF

###################################################################################################
# Globale variabler for dette modul
###################################################################################################
iTimer_ms = 0 # Bruges som stopur til at generere et TIMEOUT event
distanceTOF_cm = 0 # Den målte afstand fra TOF sensor

###################################################################################################
# Definition of STATEs and EVENTs in the statemachine
###################################################################################################
STATE_A = 1
STATE_B = 2

EVENT_A = False
EVENT_B = False


###################################################################################################
# @brief        Sets the timer seconds. When timer runs out, EVENT_TIMER is thrown
#
# @param[in]    None
# @param[out]   None
# @return       None
#
# @warning      None
###################################################################################################
def smSetTimer( iTimerValue_sec ):
    global iTimer_ms
    iTimer_ms = iTimerValue_sec



###################################################################################################
# EVENT tjek
###################################################################################################

###################################################################################################
# TODO: Lav en funktion der tæller iTimerValue_sec ned. Når den bliver 0, skal event sættes til True
# Funktionen skal kaldes fra main loop med 100 ms interval
###################################################################################################
def checkEventTimer():
    # TODO
    pass




###################################################################################################
# Initier programmet (startup), inden vi starter selve programmet
###################################################################################################
# Start med at sætte aktiv state til den vi skal starte med efter startup:
smActiveState = STATE_A

# Init TOF sensor modul:
TOF.TOF_Init()

###################################################################################################
# Tilstandsmaskine task (100 ms)
###################################################################################################
while True:

    ###############################################################
    # STATE_A
    ###############################################################
    if smActiveState == STATE_A:
        if EVENT_A == True:
            # ACTION:
            # TODO...
            # TRANSITION:
            # TODO... 
            # Reset event:
            # TODO...
            pass

    ###############################################################
    # STATE_B
    ###############################################################
    elif smActiveState == STATE_B:
        if EVENT_B == True:
            # ACTION:
            # TODO...
            # TRANSITION:
            # TODO... 
            # Reset event:
            # TODO...
            pass

    # Tjek for events:
    # TODO: Lav de nødvendig funktioner som skal kaldes for at tjekke for events. F.eks. checkEventTimer()

    # TODO: Test TOF sensor. Fjern det når I ikke skal bruge det mere.
    distanceTOF = TOF.TOF_GetDistance()
    print( f"Dist: {distanceTOF} mm" )

    # Kør tilstandsmaskinen i et loop på 10 gange i sekundet (100 ms interval):
    sleep_ms( 100 )
