import network
import socket

ROBOTBIL_IP = "192.168.0.51"
UDP_PORT = 5005

def opret_udp_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return sock

def send_styring(sock, bytes_data):
    sock.sendto(bytes_data,(ROBOTBIL_IP, UDP_PORT))