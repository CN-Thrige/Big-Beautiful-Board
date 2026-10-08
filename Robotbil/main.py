import socket
import network
from time import sleep_ms
from motor import RobotDrive
import sumo
import wall_follow
import TOF
import ir

# 1. Init hardware og sensor-interrupts
robot = RobotDrive(left_trim=1.0, right_trim=1.0)
TOF.TOF_GetDistance_Fast()

# 2. Wi-Fi Opsætning
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("ITEK 2nd", "2nd_Semester_E25")

while not wlan.isconnected():
    print("Venter på Wi-Fi forbindelse...")
    sleep_ms(500)

print(f"Pico W er på netværket! IP: {wlan.ifconfig()[0]}")

# 3. UDP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 5005))
sock.setblocking(False)

print("Klar til at modtage UDP-pakker...")

# 4. Hoved-løkke
aktiv_mode = 0

while True:
    try:
        data, addr = sock.recvfrom(1024)
        tekst = data.decode("utf-8")

        if "," in tekst:
            del_mode, del_styring, del_fart = tekst.split(",")
            aktiv_mode = int(del_mode)
            styring_val = int(del_styring)
            fart_val = int(del_fart)

            # Mode 1: PS4 / Manuel styring
            if aktiv_mode == 1:
                v_speed = max(-100, min(100, fart_val + styring_val))
                h_speed = max(-100, min(100, fart_val - styring_val))
                robot.drive(v_speed, h_speed)

    except (OSError, ValueError, IndexError):
        pass

    # --- Mode håndtering ---
    if aktiv_mode == 0:
        robot.stop()

    elif aktiv_mode == 2:
        # Autonom Sumo
        #afstand_cm = TOF.TOF_GetDistance_Fast()
        sumo.kor_sumo_step(robot)
        #print(f"Dist: {afstand_cm} cm")
        # Tjek hvad den siger midt på den hvide plade:
        #print("Hvid plade test (skal være False):", ir.IR_Task())



    elif aktiv_mode == 3:

        try:

            # ÆNDRET HER: Brug TOF_Task() for at hente den opdaterede median-måling!

            afstand_cm = TOF.TOF_GetDistance_Fast()

            #print(f"Dist: {afstand_cm} cm")

            wall_follow.wall_follow_step(robot, afstand_cm)

        except Exception as e:

            pass

    sleep_ms(10)