# server.py
import socket
from gpt import run_gpt
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

def create_state_packet(state):
    return bytes([0xFF, 0x02, state])

def create_error_packet(error):
    return bytes([0xFF, 0x03, error])

def handle_movement_command(command):
    if command == 0x00:  # Pour Coffee
        try:
            control_number = run_gpt()
            # Assuming success, send state feedback
            return create_state_packet(0x00)  # Walking State
        except Exception as e:
            # If there's an error, send error feedback
            return create_error_packet(0x00)
    return create_error_packet(0xFF)  # Unknown command

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_address = ('0.0.0.0', 6000)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)
print("Server is listening on port 6000...")

while True:
    connection, client_address = server_socket.accept()
    try:
        print(f"Connection from {client_address}")

        while True:
            data = connection.recv(1024)
            if not data:
                break

            if len(data) >= 3 and data[0] == 0xFF:
                function_code = data[1]
                command = data[2]

                if function_code == 0x01:  # Movement Command
                    print(f"Received movement command: {command}")
                    response = handle_movement_command(command)
                    connection.sendall(response)
                else:
                    # Invalid function code
                    connection.sendall(create_error_packet(0xFF))
            else:
                # Invalid packet format
                connection.sendall(create_error_packet(0xFF))
    finally:
        connection.close()