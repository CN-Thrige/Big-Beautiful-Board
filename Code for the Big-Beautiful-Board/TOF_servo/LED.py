from machine import Pin
import time

#############################################################
# Module setup
#############################################################
LED_TASK_INTERVAL_MS = 100

LED_PICO = 1

#############################################################
# Local variables
#############################################################
ledPico_timer = 0
ledPico_interval = 1000

testTime_last = 0

#############################################################
# Hardware config
#############################################################
ledPico = Pin("LED", Pin.OUT )

#############################################################
# Name definitions for the LEDs in the system
#############################################################

#############################################################
# Public functions
#############################################################

###################################################################################################
# Brief         Initialize the LED pins
#
# param[in]     None
# Return        None
#
# Warning       Must be called before usiong the LED module
###################################################################################################
def LED_Init():
    ledPico.off()

###################################################################################################
# Brief         Takes care of the blinking the LED's
#
# param[in]     None
# Return        None
#
# Warning       Must be called every LED_TASK_INTERVAL_MS
###################################################################################################
def LED_Task():
    global ledPico_timer
    global ledPico_interval

    # Toggle LED, but only if LED is not set to ON or OFF:
    if ledPico_timer >= ledPico_interval and ledPico_interval > 1:
        ledPico.toggle()
        ledPico_timer = 0

    # Increment LED timers:
    ledPico_timer = ledPico_timer + LED_TASK_INTERVAL_MS

###################################################################################################
# Brief         Sets the function of an LED
#
# param[in]     0 : OFF
#               1 : ON
#               all other: The blink interval in ms
# Return        None
#
# Warning       None
###################################################################################################
def LED_Set( ledName, interval_ms ):
    global ledPico_interval

    # Pico LED:
    if ledName == LED_PICO:
        # Save new interval
        ledPico_interval = interval_ms
        # Check if new interval is 0 or 1 (OFF or ON):
        if interval_ms == 0:
            ledPico.off()
        elif interval_ms == 1:
            ledPico.on()

