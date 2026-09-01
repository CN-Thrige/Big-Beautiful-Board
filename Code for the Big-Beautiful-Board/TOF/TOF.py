import time
from machine import Pin

#############################################################
# Module setup
#############################################################
TOF_TASK_INTERVAL_MS = 100
TOF_AVERAGE_COUNT = 3 # Tag 3 målinger og udregn middelværdi

#############################################################
# Hardware config
#############################################################
pwmPin = Pin( 28, Pin.IN )

#############################################################
# Local variables
#############################################################
iPWMRising_us = 0 # Store clock at rising IRQ
iPulseWidth_sum_us = 0 # Used to sum up 3 values to calculate average value
iPulseWidthCount = 0 # Used to count to 3 for average value
iPulseWidth_us = 0 # The result of the average calculation. Used to calculate distance. Updated every 3*50 ms

iDistance_mm = 0 # The actual distance, filtered.

#############################################################
# Name definitions
#############################################################

###################################################################################################
# Private functions
###################################################################################################

###################################################################################################
# Brief         PWM ISR function. Called at every rising and falling edge of the PWM signal.
#               Measures the pulse width, which is used to calculate the distance.
#               In this ISR, we only use the puse width in micro seconds.
#               A small simple filter is implemented, simply calculating the mean value of 4 
#               samples, because this is fast to divide by 4 using bit shift.
#               The sensor PWM is 20 Hz, so this means we have a new value every 4 * 50 ms = 200 ms
#
# Param[in]     None
# Return        None
#
# Warning       Called from IRQ
###################################################################################################
def pwmIRQHandler_ISR( irqPin ):
    global iPWMRising_us, iPulseWidth_sum_us, iPulseWidthCount, iPulseWidth_us

    # On rising edge, save the current timer value:
    if irqPin.value() == 1:
        iPWMRising_us = time.ticks_us()
    else:
        # On falling edge we can calculate the pulse width.
        # We will sum up the last 4 values:

        iPulseWidth_now = time.ticks_us() - iPWMRising_us
        # The sensor makes some weird stuff wen changing the distance fast.
        # In this case it sometimes makes very long pulses.
        # We need to ignore these errors.
        # If pulse is more than 2 meters (20000 us) then ignore it:
        if iPulseWidth_now < 20000: 
            iPulseWidth_sum_us = iPulseWidth_sum_us + (time.ticks_us() - iPWMRising_us) 
            iPulseWidthCount += 1
            # If we have measured the needed number of pulses, calculate average:
            if iPulseWidthCount == TOF_AVERAGE_COUNT:
                iPulseWidth_us = iPulseWidth_sum_us / TOF_AVERAGE_COUNT
                iPulseWidth_sum_us = 0
                iPulseWidthCount = 0

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
    pwmPin.irq( handler = pwmIRQHandler_ISR, trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING )

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
    global iDistance_mm, iPulseWidth_sum_us
    iDistance_mm = int(iPulseWidth_us / 10)

    return iDistance_mm

