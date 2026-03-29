from machine import Pin
from time import sleep

sleep(1)
knap = Pin(2, Pin.IN, Pin.PULL_UP)
print("Running")
def light_up_led(led_pin, duration):

    # Create an instance of the Pin class for the LED
    led = Pin(led_pin, Pin.OUT)
    led1 = Pin(led_pin+1, Pin.OUT)
    led1 = Pin(led_pin+1, Pin.OUT)
    led2 = Pin(led_pin+2, Pin.OUT)

    led.off()
    led1.off()
    led2.off()
    led.on()
    print("LED on")
    led1.on()
    led2.on()

    # Wait for the specified duration
    sleep(duration)

    # Turn the LED off
    # Turn the LED off
    # Turn the LED off
    led.off()
    led1.off()
    led2.off()
    print("Waiting for")


while True:
    if knap.value() == 0:
        print("Button Pressed")
        light_up_led(0, 3)
    sleep(0.1)
