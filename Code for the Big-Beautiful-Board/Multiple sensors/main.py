
#############################################################
# Import external modules
#############################################################
from TaskManager import *
from LED import *
from TOF import * 
from IR import *
#############################################################
# Module setup
#############################################################

#############################################################
#Hardware config

#############################################################

#############################################################
# Local variables

#############################################################
testCounter = 0

#############################################################
# Init external modules
#############################################################
LED_Init()
TM_Init()
TOF_Init()
IR_REF_Init()

#############################################################
# Test tasks
# Bruges her til at skrive noget ud.
#############################################################
def taskTest():
    global testCounter

    print( f"Test count = {testCounter}" )
    testCounter = testCounter + 1
   

#############################################################
# Start tasks
#############################################################

TM_CreateTask( "LED", 100, LED_Task )
TM_CreateTask( "TEST", 1000, taskTest )
TM_CreateTask( "TOF", 1000, TOF_Task)
TM_CreateTask( "IR", 1000, IR_REF_Task)

###################################################################################################
# Application is now ready to fly...

###################################################################################################
print("Application running...")

# Test LED modul:
LED_Set( LED_PICO, 500 )

# Main loop: Simply calls the TM as fast as possible
# TM is now in control of the system.
try:
    while True:
        TM_Execute()
except KeyboardInterrupt:
    tim.deinit()
    print( "Application exit")

finally:
    # Clean up before exit
    pass
