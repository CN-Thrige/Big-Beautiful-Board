import socket
from network import WLAN
from time import sleep_ms

import sumo.sumo

# Opret et WLAN-objekt til at styre Wi-Fi chippen på Pico W
wlan = WLAN()
wlan.active(True)  # Tænd for Wi-Fi

# Forbind til det lokale Wi-Fi netværk
wlan.connect("ITEK 2nd", "2nd_Semester_E25")

# Vent i en løkke, indtil forbindelsen er oprettet
while not wlan.isconnected():
    print("Venter på Wi-Fi forbindelse...")
    sleep_ms(500)  # Pause i 500 ms for ikke at overbelaste CPU'en

print(f"Pico W er på netværket! IP: {wlan.ifconfig()[0]}")

# Opret en UDP socket (SOCK_DGRAM angiver at vi bruger UDP frem for TCP)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind socketen til IP "0.0.0.0" (lytter på alle netværkskort) og port 5005
sock.bind(("0.0.0.0", 5005))

print("Klar til at modtage UDP-pakker fra bærbaren...")

while True:
    # Læs indkommende UDP-data fra netværket
    # recvfrom(1024) venter her, indtil der modtages en pakke (op til 1024 bytes)
    data, addr = sock.recvfrom(1024)

    # Konverter de rå bytes til en almindelig tekststreng (UTF-8)
    tekst = data.decode("utf-8")

    # Udpak den komma-separerede streng "mode,styring,fart" til 3 variabler
    del_mode, del_styring, del_fart = tekst.split(",")

    # Konverter tekstværdierne til heltal (int)
    mode = int(del_mode)
    styring = int(del_styring)
    fart = int(del_fart)

    if mode == 0:
        # MODE 0: Standby / Pause (Sikkerhedstilstand)
        print("Mode 0: IDLE (Motorer stoppet)")

    elif mode == 1:
        # MODE 1: Manuel Fodbold-styring (PS4 controller)
        # Her sendes styring og fart videre til motor-beregningen
        print(f"Mode 1: Fodbold | Styring: {styring}, Fart: {fart}")

    elif mode == 2:
        # MODE 2: Autonom Sumo
        sumo.kor_sumo_step()
        # Bilen overtager selv styringen via sine sensorer
        print("Mode 2: SUMO (Autonom)")

    elif mode == 3:
        # MODE 3: Autonom Wall-Follow
        # Bilen følger væggen autonomt vha. afstandssensorer
        print("Mode 3: WALL-FOLLOW (Autonom)")

    # tag en slapper lille pico
    sleep_ms(20)