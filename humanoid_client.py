import socket
import signal
import sys
import time
from scripts.gpt import run_gpt
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import os

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server (allow override via environment variables)
server_host = os.getenv('SERVER_HOST', '192.168.3.70')
server_port = int(os.getenv('SERVER_PORT', '6666'))
server_address = (server_host, server_port)
print("... connecting to", server_address)
client_socket.connect(server_address)
print("--- connected to", server_address)

def signal_handler(sig, frame):
    print("Interrupt received, shutting down...")
    client_socket.close()
    sys.exit(0)

# Register the signal handler for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

try:
    while True:
        # Receive data from the server
        print("waiting for data from server")
        data = client_socket.recv(1024)
        if data:
            received_text = data.decode()
            print(f"Received: {received_text}")
            if received_text == 'Humanoid waiting':
                client_socket.sendall(str("0").encode())  # Send 0 as handshake back to the server
            if received_text == 'start GPT task':
                control_number = run_gpt()
                client_socket.sendall(str(control_number).encode())  # Send control_number back to the server
        else:
            print("No data received from the server")
            time.sleep(2)
except Exception as e:
    print(f"Error: {e}")
finally:
    client_socket.close()