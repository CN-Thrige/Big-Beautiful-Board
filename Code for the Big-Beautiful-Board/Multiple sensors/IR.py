from machine import Pin

#############################################################
# Module setup
#############################################################
IR_REF_TASK_INTERVAL_MS = 100

#############################################################
# Hardware config
#############################################################

# Grove IR sensor signal
sensor = Pin(27, Pin.IN)


#############################################################
# Local variables
#############################################################
sensor_value = 1

#############################################################
# Public functions
#############################################################

###################################################################################################
# Brief         Init function for the infrared reflection sensor.
#
# Param[in]     None
# Return        None
#
# Warning       Must be called at power up
###################################################################################################
def IR_REF_Init():
    pass


###################################################################################################
# Brief         Reads the infrared reflection sensor and updates the LED.
#               A sensor value of 0 means that a reflection/object is detected.
#
# Param[in]     None
# Return        sensor_value
#
# Warning       Must be called every IR_REF_TASK_INTERVAL_MS
###################################################################################################
def IR_REF_Task():
    global sensor_value

    sensor_value = sensor.value()

    if sensor_value == 0:
        # Reflection/object detected
        print("Object detected")
    else:
        # Nothing detected
        print("Nothing detected")

    return sensor_value
