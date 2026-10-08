import socket
import time
import pygame

PICO_IP = "10.120.0.13"  # Retter sig mod din Pico W!
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Ingen controller fundet! Sæt USB-kabel i PS4-controlleren.")
    exit()

controller = pygame.joystick.Joystick(0)
controller.init()
print(f"Forbundet til controller: {controller.get_name()}")

# Variabler til mode-skift
mode = 0
knap_sidste_status = False

while True:
    pygame.event.pump()

    # 1. Læs PS4 joystick (skaleret -100 til 100)
    styring = int(controller.get_axis(0) * 100)
    fart = int(-controller.get_axis(1) * 100)

    #deadzone (tvinger små slør-værdier til 0)
    if abs(styring) < 5:
        styring = 0
    if abs(fart) < 5:
        fart = 0

    # 2. Læs knapperne og sæt mode direkte
    if controller.get_button(0):  # Kryds - IDLE
        mode = 0
    elif controller.get_button(1):  # Cirkel - FODBOLD
        mode = 1
    elif controller.get_button(2):  # Firkant - SUMO
        mode = 2
    elif controller.get_button(3):  # Trekant - WALL-FOLLOW
        mode = 3

    # 3. Send pakken med det DYNAMISKE mode-tal
    besked = f"{mode},{styring},{fart}"
    sock.sendto(besked.encode("utf-8"), (PICO_IP, UDP_PORT))

    print(f"Sender til Pico: {besked}")
    time.sleep(0.05)