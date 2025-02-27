# server.py
import socket
from gpt import run_gpt
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

def create_state_packet(state):
    packet = bytes([0xFF, 0x02, state])
    print(f"4. Server creating state packet: {packet.hex(' ')}")
    return packet

def create_error_packet(error):
    packet = bytes([0xFF, 0x03, error])
    print(f"4. Server creating error packet: {packet.hex(' ')}")
    return packet

def handle_movement_command(command):
    print(f"3. Server handling movement command: {command:#x}")
    if command == 0x00:  # Pour Coffee
        try:
            print("3a. Running GPT function...")
            control_number = run_gpt()
            print("3b. GPT function completed successfully")
            return create_state_packet(0x00)  # Walking State
        except Exception as e:
            print(f"3c. Error occurred: {str(e)}")
            return create_error_packet(0x00)
    return create_error_packet(0xFF)  # Unknown command

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_address = ('0.0.0.0', 6000)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)
print("1. Server is listening on port 6000...")

while True:
    connection, client_address = server_socket.accept()
    try:
        print(f"2. New connection accepted from {client_address}")

        while True:
            data = connection.recv(1024)
            if not data:
                print("Connection closed by client")
                break

            print(f"2a. Received raw data: {data.hex(' ')}")
            
            if len(data) >= 3 and data[0] == 0xFF:
                function_code = data[1]
                command = data[2]
                print(f"2b. Decoded packet - Function Code: {function_code:#x}, Command: {command:#x}")

                if function_code == 0x01:  # Movement Command
                    response = handle_movement_command(command)
                    print(f"5. Sending response to client: {response.hex(' ')}")
                    connection.sendall(response)
                else:
                    print(f"2c. Invalid function code: {function_code:#x}")
                    connection.sendall(create_error_packet(0xFF))
            else:
                print("2d. Invalid packet format")
                connection.sendall(create_error_packet(0xFF))
    finally:
        print("6. Connection closed")
        connection.close()