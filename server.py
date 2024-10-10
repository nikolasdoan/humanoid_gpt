import socket
import signal
import sys
from gpt import run_gpt
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_address = ('192.168.1.87', 6666)  # Listen on all interfaces
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)
print("Server is listening on port 6666...")

def signal_handler(sig, frame):
    print("Interrupt received, shutting down...")
    server_socket.close()
    sys.exit(0)

# Register the signal handler for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

try:
    while True:
        # Wait for a connection
        connection, client_address = server_socket.accept()
        try:
            print(f"Connection from {client_address}")

            while True:
                # Receive data from the client
                data = connection.recv(1024)
                if data:
                    received_text = data.decode()
                    print(f"Received: {received_text}")
                    if received_text == 'start':  # Replace 'start' with the specific character or string you want
                        control_number = run_gpt()
                        connection.sendall(str(control_number).encode()) # Send control_number back to the client
                    else:
                        connection.sendall(data)  # Echo back the received data
                else:
                    break
        finally:
            connection.close()
finally:
    server_socket.close()