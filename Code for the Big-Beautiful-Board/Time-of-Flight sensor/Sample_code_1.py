import time
from machine import Pin

gy53 = Pin(16, Pin.IN)  # Initialize GY-53 I2C pin

while True:
    while gy53.value() == True:  # Wait for the GY-53 to become ready
        #print("Waiting for GY-53 to become ready...")
        pass
    while gy53.value() == False:  # Read the GY-53 data
        #print("Reading GY-53 data...")
        pass
    starttime = time.ticks_us()
    while gy53.value() == True:  # Wait for the GY-53 to finish reading
        #print("Waiting for GY-53 to finish reading...")
        pass
    endtime = time.ticks_us()
    print("Time elapsed: ", (endtime - starttime) / 1000, "ms")
    print("Millimterters: ", (endtime - starttime) / 1000 / 10, "m")
    time.sleep(1)  # Wait for 1 second before starting the next measurement
