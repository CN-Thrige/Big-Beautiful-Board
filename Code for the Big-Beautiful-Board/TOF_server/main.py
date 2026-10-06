
#############################################################
# Import external modules
#############################################################

from TaskManager import *
from LED import *
from TOF import *
from servo import Servo

#############################################################
# Module setup
#############################################################

#############################################################
# Hardware config


    
#user_input = input(num)
my_servo = Servo(15)
#############################################################

#############################################################
# Local variables
#############################################################

#############################################################
# Init external modules
#############################################################
LED_Init()
TM_Init()
TOF_Init()

#############################################################
# Test tasks
# Bruges her til at skrive noget ud.
#############################################################
def taskTest():
    print( f"TOF dist = {TOF_GetDistance()} mm")

def taskServoTest():
    num_input = input()

    if "." in num_input:
        num_input = float(num_input)
    else:
        num_input = int(float(num_input))

    my_servo.write(num_input)
    
def taskServoAuto():
    global number 
    value = TOF_GetDistance()
    my_servo.write(value)
    if value == 180: #180
        value = 0 #0
    
    return value
    
    
            
        

#############################################################
# Start tasks
#############################################################
TM_CreateTask( "LED", LED_TASK_INTERVAL_MS, LED_Task )
TM_CreateTask( "TEST", 1000, taskTest )
#TM_CreateTask( "SERVO", 2000, taskServoTest )
TM_CreateTask( "SERVO2", 10, taskServoAuto )

# Add more tasks here...


###################################################################################################
# Application is now ready to fly...
###################################################################################################
print("Application running X ...")

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
