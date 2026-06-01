# -------- IMPORTS --------
from machine import Pin, PWM
import time
import network
import gc
import uasyncio as asyncio

try:
    import usocket as socket
except:
    import socket

gc.collect()

# -------- MOTOR PINS --------
in1 = Pin(19, Pin.OUT)
in2 = Pin(18, Pin.OUT)
enable_pin = PWM(Pin(20))
enable_pin.freq(1500)

# -------- TOF SENSOR (GY-53 pulse mode) --------
gy53 = Pin(28, Pin.IN)

# -------- GLOBAL TILSTAND --------
position_mm = -1
motor_kører = False

current_floor = "Etage 1"
previous_floor = "Etage 1"


# -------- MOTOR FUNKTIONER --------
def set_speed(speed):
    enable_pin.duty_u16(speed)


def stop_motor():
    in1.value(0)
    in2.value(0)
    set_speed(0)


stop_motor()


# -------- AFSTANDSMÅLING --------
def get_distance_mm():
    try:
        # Sænket timeout til 30ms for at forhindre async-blokering ved fejl
        timeout = time.ticks_ms()
        while gy53.value() == 1:
            if time.ticks_diff(time.ticks_ms(), timeout) > 30:
                return -1

        timeout = time.ticks_ms()
        while gy53.value() == 0:
            if time.ticks_diff(time.ticks_ms(), timeout) > 30:
                return -1

        start = time.ticks_us()
        timeout = time.ticks_ms()
        while gy53.value() == 1:
            if time.ticks_diff(time.ticks_ms(), timeout) > 30:
                return -1
        end = time.ticks_us()

        pulse_us = time.ticks_diff(end, start)
        if pulse_us <= 0:
            return -1
        return pulse_us / 10

    except:
        return -1


# -------- ETAGEDEFINITIONER --------
ETAGE_OP = {1: 43, 2: 155, 3: 275}
ETAGE_NED = {1: 43, 2: 155, 3: 275}
TOLERANCE_MM = 5


def hvilken_etage(mm):
    for etage in ETAGE_OP:
        mål = (ETAGE_OP[etage] + ETAGE_NED[etage]) / 2
        if abs(mm - mål) <= TOLERANCE_MM:
            return etage
    return None


# -------- PID KONSTANTER --------
Kp = 150.0
Ki = 2.5
Kd = 0.0

MIN_FART = 10000
MAX_FART = 16000
DT = 0.03
MAX_INTEGRAL = 500.0


# -------- ASYNC TASKS --------

async def sensor_task():
    global position_mm
    while True:
        mm = get_distance_mm()
        if mm >= 0:
            position_mm = mm
        await asyncio.sleep_ms(50)


async def kør_til_etage(mål_etage):
    global motor_kører, current_floor, previous_floor
    motor_kører = True

    # Opdater "Kom fra" status inden vi flytter os
    if current_floor != f"Etage {mål_etage}":
        previous_floor = current_floor
        current_floor = f"Etage {mål_etage}"

    if position_mm >= 0 and position_mm < ETAGE_OP[mål_etage]:
        mål_mm = ETAGE_OP[mål_etage]
        retning_tekst = "op"
    else:
        mål_mm = ETAGE_NED[mål_etage]
        retning_tekst = "ned"

    print("Kører til etage", mål_etage, "(", mål_mm, "mm,", retning_tekst, ")")

    integral = 0.0
    forrige_fejl = 0.0
    timeout_start = time.ticks_ms()
    MAX_KØR_MS = 15000

    while True:
        mm = position_mm
        if mm < 0:
            print("Sensor fejl – stopper")
            stop_motor()
            break

        fejl = mål_mm - mm

        if abs(fejl) <= 15:
            stop_motor()
            print("  Ankom til etage", mål_etage, "| Endelig position:", round(mm), "mm")
            break

        # Anti-overshoot: nulstil I-led hvis vi krydser målet
        if (fejl > 0 and forrige_fejl < 0) or (fejl < 0 and forrige_fejl > 0):
            integral = 0.0

        integral += fejl * DT
        integral = max(-MAX_INTEGRAL, min(MAX_INTEGRAL, integral))
        derivative = (fejl - forrige_fejl) / DT
        output = (Kp * fejl) + (Ki * integral) + (Kd * derivative)
        forrige_fejl = fejl

        fart = int(abs(output))
        fart = max(MIN_FART, min(MAX_FART, fart))

        set_speed(fart)
        if output > 0:
            in1.value(1)
            in2.value(0)
        else:
            in1.value(0)
            in2.value(1)

        if time.ticks_diff(time.ticks_ms(), timeout_start) > MAX_KØR_MS:
            stop_motor()
            print("Timeout – stopper motor")
            break

        await asyncio.sleep_ms(int(DT * 1000))

    stop_motor()
    await asyncio.sleep(2)
    motor_kører = False


# -------- FLOT WEB TEMPLATE --------
def get_html_template():
    mm = position_mm
    pos_tekst = f"{round(mm)} mm" if mm >= 0 else "Sensor fejl"

    # Dynamisk valg af billede ud fra nuværende registrerede etage
    if current_floor == "Etage 1":
        image_src = "/groundfloor.jpg"
    elif current_floor == "Etage 2":
        image_src = "/floor1.png"
    elif current_floor == "Etage 3":
        image_src = "/floor2.jpg"
    else:
        image_src = "/groundfloor.jpg"

    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <title>Elevator Kontrol</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="refresh" content="2">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f9; }}
            .header {{ text-align: center; background-color: #333; color: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; }}
            .grid-container {{ display: grid; grid-template-columns: 1fr 2fr 1.5fr; gap: 20px; }}
            .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
            .btn-container {{ display: flex; flex-direction: column; gap: 15px; align-items: center; }}
            .btn {{ width: 80%; padding: 15px; font-size: 18px; border: none; border-radius: 5px; cursor: pointer; color: white; transition: 0.3s; }}
            .btn-gnd {{ background-color: #2ecc71; }}
            .btn-1st {{ background-color: #3498db; }}
            .btn-2nd {{ background-color: #9b59b6; }}
            .btn:hover {{ opacity: 0.8; }}
            .image-box img {{ width: 100%; max-width: 250px; border-radius: 8px; border: 3px solid #333; }}
            .status-text {{ margin-top: 10px; font-style: italic; color: #555; }}
            .refresh-btn {{ background-color: #555; color: white; border: none; padding: 8px 12px; border-radius: 4px; cursor: pointer; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Elevator Kontrolpanel</h1>
        </div>
        <div class="grid-container">
            <div class="card">
                <h3>TOF Sensor Data</h3>
                <p><strong>Afstand:</strong> {pos_tekst}</p>
                <p><strong>Status:</strong> {"Kører..." if motor_kører else "Stille"}</p>
                <hr>
                <button class="refresh-btn" onclick="window.location.reload();">Opdater måling</button>
            </div>
            <div class="card btn-container">
                <h3>Vælg Etage</h3>
                <a href="/floor?set=1" style="width:100%; text-align:center;"><button class="btn btn-gnd">Etage 1</button></a>
                <a href="/floor?set=2" style="width:100%; text-align:center;"><button class="btn btn-1st">Etage 2</button></a>
                <a href="/floor?set=3" style="width:100%; text-align:center;"><button class="btn btn-2nd">Etage 3</button></a>
            </div>
            <div class="card image-box" style="text-align: center;">
                <h3>Elevator Status</h3>
                <img src="{image_src}" alt="Elevator etage">
                <p class="status-text">Nuværende: <strong>{current_floor}</strong></p>
                <p class="status-text">Kom fra: {previous_floor}</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html


# -------- FIL-SENDER (Til billeder lagret på Pico) --------
def send_file(writer, filename):
    try:
        with open(filename, "rb") as f:
            writer.write(b'HTTP/1.1 200 OK\r\n')
            if filename.endswith(".png"):
                writer.write(b'Content-Type: image/png\r\n')
            else:
                writer.write(b'Content-Type: image/jpeg\r\n')
            writer.write(b'Connection: close\r\n\r\n')

            while True:
                chunk = f.read(256)  # Mindre chunks for asynkron stabilitet på Pico
                if not chunk:
                    break
                writer.write(chunk)
    except Exception as e:
        writer.write(b'HTTP/1.1 404 Not Found\r\n\r\n')


# -------- ASYNC WEBSERVER HANDLING --------
async def handle_request(reader, writer):
    global motor_kører
    try:
        request = await reader.read(1024)
        request = str(request)

        # 1. Server billeder hvis websiden beder om dem
        if "GET /groundfloor.jpg" in request or "GET /groundfloor.png" in request:
            send_file(writer, "groundfloor.jpg" if "jpg" in request else "groundfloor.png")
            await writer.drain()
            writer.close()
            return
        elif "GET /floor1.jpg" in request or "GET /floor1.png" in request:
            send_file(writer, "floor1.jpg" if "jpg" in request else "floor1.png")
            await writer.drain()
            writer.close()
            return
        elif "GET /floor2.jpg" in request or "GET /floor2.png" in request:
            send_file(writer, "floor2.jpg" if "jpg" in request else "floor2.png")
            await writer.drain()
            writer.close()
            return

        # 2. Håndter tryk på etageknapper (Kun hvis motoren ikke allerede kører)
        if not motor_kører:
            if "/floor?set=1" in request:
                asyncio.create_task(kør_til_etage(1))
            elif "/floor?set=2" in request:
                asyncio.create_task(kør_til_etage(2))
            elif "/floor?set=3" in request:
                asyncio.create_task(kør_til_etage(3))

        # 3. Generer og send HTML-siden
        response = get_html_template()
        writer.write(b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n')
        writer.write(response.encode('utf-8'))
        await writer.drain()

    except Exception as e:
        print("Fejl i request:", e)
    finally:
        writer.close()
        await writer.wait_closed()
        gc.collect()  # Ryd op i RAM efter hver anmodning


# -------- MAIN SETUP --------
async def main():
    ssid = 'ITEK 1st'
    password = 'itekf25v'

    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    print("Forbinder til WiFi...")
    while not station.isconnected():
        await asyncio.sleep_ms(100)

    print("Forbundet! IP:", station.ifconfig()[0])

    asyncio.create_task(sensor_task())

    server = await asyncio.start_server(handle_request, '0.0.0.0', 80)
    print("Webserver kører på http://" + station.ifconfig()[0])

    while True:
        await asyncio.sleep(1)


# -------- START --------
asyncio.run(main())