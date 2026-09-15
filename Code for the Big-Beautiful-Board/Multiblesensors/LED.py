from machine import Pin

#############################################################
# Module setup
#############################################################
LED_TASK_INTERVAL_MS = 100

LED_PICO = 1
LED_GREEN = 2
LED_YELLOW = 3
LED_RED = 4

#############################################################
# Local variables
#############################################################
ledPico_timer = 0
ledPico_interval = 1000

ledGreen_timer = 0
ledGreen_interval = 1000

ledYellow_timer = 0
ledYellow_interval = 1000

ledRed_timer = 0
ledRed_interval = 1000

#############################################################
# Hardware config
#############################################################
ledPico = Pin("LED", Pin.OUT )
ledGreen = Pin( 1, Pin.OUT )
ledYellow = Pin( 2, Pin.OUT )
ledRed = Pin( 3, Pin.OUT )

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
    ledGreen.off()
    ledYellow.off()
    ledRed.off()

###################################################################################################
# Brief         Takes care of the blinking the LED's
#
# param[in]     None
# Return        None
#
# Warning       Must be called every LED_TASK_INTERVAL_MS
###################################################################################################
def LED_Task():
    global ledPico_timer, ledGreen_timer, ledYellow_timer, ledRed_timer
    global ledPico_interval, ledGreen_interval, ledYellow_interval, ledRed_interval

    # Toggle LED, but only if LED is not set to ON or OFF:
    if ledPico_timer >= ledPico_interval and ledPico_interval > 1:
        ledPico.toggle()
        ledPico_timer = 0

    if ledGreen_timer >= ledGreen_interval and ledGreen_interval > 1:
        ledGreen.toggle()
        ledGreen_timer = 0

    if ledYellow_timer >= ledYellow_interval and ledYellow_interval > 1:
        ledYellow.toggle()
        ledYellow_timer = 0

    if ledRed_timer >= ledRed_interval and ledRed_interval > 1:
        ledRed.toggle()
        ledRed_timer = 0

    # Increment LED timers:
    ledPico_timer = ledPico_timer + LED_TASK_INTERVAL_MS
    ledGreen_timer = ledGreen_timer + LED_TASK_INTERVAL_MS
    ledYellow_timer = ledYellow_timer + LED_TASK_INTERVAL_MS
    ledRed_timer = ledRed_timer + LED_TASK_INTERVAL_MS

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
    global ledPico_interval, ledGreen_interval, ledYellow_interval, ledRed_interval

    # Pico LED:
    if ledName == LED_PICO:
        # Save new interval
        ledPico_interval = interval_ms
        # Check if new interval is 0 or 1 (OFF or ON):
        if interval_ms == 0:
            ledPico.off()
        elif interval_ms == 1:
            ledPico.on()

    # Green LED:
    if ledName == LED_GREEN:
        # Save new interval
        ledGreen_interval = interval_ms
        # Check if new interval is 0 or 1 (OFF or ON):
        if interval_ms == 0:
            ledGreen.off()
        elif interval_ms == 1:
            ledGreen.on()

    # Yellow LED:
    if ledName == LED_YELLOW:
        # Save new interval
        ledYellow_interval = interval_ms
        # Check if new interval is 0 or 1 (OFF or ON):
        if interval_ms == 0:
            ledYellow.off()
        elif interval_ms == 1:
            ledYellow.on()

    # Red LED:
    if ledName == LED_RED:
        # Save new interval
        ledGreen_interval = interval_ms
        # Check if new interval is 0 or 1 (OFF or ON):
        if interval_ms == 0:
            ledRed.off()
        elif interval_ms == 1:
            ledRed.on()
