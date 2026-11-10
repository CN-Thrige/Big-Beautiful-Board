import utime
import network

#########################################################################
# MQTT installeres på Pico via WiFi/Internet.
# Vi skal derfor først oprette forbindelse via WiFi.
#########################################################################
# Tilslut WiFi:
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("ITEK 2nd", "2nd_Semester_E26")
#wlan.connect("KSV_Internet", "99009900")

# Vent på WiFi connection:
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
max_wait -= 1
print('Waiting for connection...' )
utime.sleep(1)
#Handle connection error
bWiFi_connected = False
if wlan.status() != 3:
    raise RuntimeError('WiFi connection failed !')
else:
    bWiFi_connected = True
    status = wlan.ifconfig()
    print('WiFi connected: IP = ' + status[0])

#########################################################################
# Installer MQTT package på Pico. 
# Her bruger vi "mip install" som kan installere direkte fra
# micropython-lib, GitHub mm.
#########################################################################
if bWiFi_connected == True:
    import mip
    mip.install("umqtt.simple")
    wlan.deinit()

