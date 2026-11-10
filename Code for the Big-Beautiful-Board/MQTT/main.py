import network
import utime
import json
from umqtt.simple import MQTTClient # type: ignore

#########################################################################
# Connect til WiFi
#########################################################################
print('Connecting to WiFi...' )
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("ITEK 2nd", "2nd_Semester_E26")

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
# createMQTTClient_RPi()
# VIGTIGT: Konfigurer klient til Raspberry Pi Broker
#########################################################################
def createMQTTClient_RPi():
    client = MQTTClient(client_id=b"ThrigePico2", # Skal være unikt navn
    server = "10.100.0.96",#if this does not work, put port 1883 back into server and vice versa
    port = 1883,
    #user = strUsername.encode(),
    #password = strPassword.encode(),
    user = "ExtUser_1",
    password = "ExtUser_1p",
    keepalive = 7200,
    ssl = False,
    ssl_params = {'server_hostname':'10.120.0.96:1883'} )
    
    return client


#########################################################################
# Callback funktion 
# Kaldes hver gang der modtages en besked som vi har lavet en "Subscribe" på
#########################################################################
def cbHome( mqttTopic, mqttMsg ):
    print( f"Received: {mqttTopic.decode()} : {mqttMsg.decode()}" )


#########################################################################
# Opret MQTT klient og lav forbindelse til Broker
#########################################################################
myClient = createMQTTClient_RPi()
myClient.set_callback( cbHome )
myClient.connect()

#connnect to my own iphone with MQTT
#myClient.subscribe("thrige/led/#") #thrige/led/#

#connect to collectiv MQTT database for bord 1
myClient.subscribe("ITEK2/Bord_1/#") #thrige/led/#


# Send besked til Broker, at vi er på:
print( "Publish startup besked til Broker")
myClient.publish( "ThrigeStatus", "Thrige is in the house", qos = 1) #quality of service 

#connect to phone 
myClient.publish( "thrige/led/red", "0" ) 

#JSON test (doesn't work)
#tempDict={"Class": "A2.09", "Students": 16, "Date": "10.11.2026","TemperatureLog": [18.5, 20.1, 19.8, 19.7]}
                      
#json.load(str(tempDict))

#myClient.publish( "ITEK2/Bord_1/#", "fuck_this" ) 


# Main loop
print( "Venter på subscription beskeder...")
try:
    while True:
        # Check om der er kommet meddelelser ind (som vi abonnerer på)
        myClient.check_msg()
        utime.sleep_ms( 100 )

except KeyboardInterrupt:
    print( "Exception exit")
    try:
        myClient.disconnect()
    except OSError:
        pass
    wlan.deinit()
finally:
    print( "Clean up and exit")
    # Clean up before exit
    try:
        myClient.disconnect()
    except OSError:
        pass

    wlan.deinit()


