import socket
import signal
import sys
import time
from gpt import run_gpt
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('192.168.3.70', 6666)
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
            if received_text == 'Oliver waiting':
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