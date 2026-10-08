import time
from machine import Pin

#############################################################
# Module setup
#############################################################
TOF_TASK_INTERVAL_MS = 100
TOF_AVERAGE_COUNT = 3  # Tag 3 målinger og udregn middelværdi

#############################################################
# Hardware config
#############################################################
pwmPin = Pin(2, Pin.IN)

#############################################################
# Local variables
#############################################################
iPWMRising_us = 0  # Store clock at rising IRQ
iPulseWidthBuffer = []


#############################################################
# Name definitions
#############################################################

###################################################################################################
# Private functions
###################################################################################################

###################################################################################################
# Brief         PWM ISR function. Called at every rising and falling edge of the PWM signal.
#               Copies the new value to circular buffer.
# Param[in]     None
# Return        None
#
# Warning       Interrupt Service Rutine
#               This version is not bullet proof. Only for simple testing.
###################################################################################################
def pwmIRQHandler_ISR(irqPin):
    global iPWMRising_us  # , iPulseWidthCount #, iPulseWidth_sum_us, , iPulseWidth_us

    # On rising edge, save the current timer value:
    if irqPin.value() == 1:
        iPWMRising_us = time.ticks_us()
    else:
        # On falling edge we will save the value in circulat buffer:
        iPulseWidth_now = time.ticks_us() - iPWMRising_us
        # Sensor reading is not stable over 2 meters / 20000 us:
        if iPulseWidth_now > 20000:
            iPulseWidth_now = 20000
        # Kopier til buffer:
        iPulseWidthBuffer.append(iPulseWidth_now)
        # Hvis buffer er fyldt, skal vi fjerne den ældste...
        if len(iPulseWidthBuffer) >= TOF_AVERAGE_COUNT:
            iPulseWidthBuffer.pop(0)


###################################################################################################
# Public functions
###################################################################################################

###################################################################################################
# Brief         Init function
#
# Param[in]     None
# Return        None
#
# Warning       Must be called at power up
###################################################################################################
def TOF_Init():
    # Start IRQ on PWM rising and falling edges:
    pwmPin.irq(handler=pwmIRQHandler_ISR, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)


###################################################################################################
# Brief         Continously measures the distance value from the GY53 sensor using the PWM output.   
#               Calculates a mean value to minimize noise
#
# Param[in]     
# Return        None
#
# Warning       Must be called every TOF_TASK_INTERVAL_MS
###################################################################################################
def TOF_Task():
    pass


###################################################################################################
# Brief         
#
# Param[in]     
# Return        None
#
# Warning       None
###################################################################################################
def TOF_GetDistance():
    global iDistance_mm

    iDistance_mm = 0

    if len(iPulseWidthBuffer) > 0:
        fDistance = (sum(iPulseWidthBuffer) / len(iPulseWidthBuffer)) / 10
        iDistance_mm = int(fDistance + 0.5)

    return iDistance_mm

