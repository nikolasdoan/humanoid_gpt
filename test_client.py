# client.py
import socket
import struct

def create_movement_packet(command):
    return bytes([0xFF, 0x01, command])

def decode_response(response):
    if len(response) < 3:
        return "Invalid response length"
    
    header, function_code, command = response[:3]
    
    if header != 0xFF:
        return "Invalid header"
    
    if function_code == 0x02:  # State Feedback
        states = {
            0x00: "Walking State",
            0x01: "Navigation State"
        }
        return f"State Feedback: {states.get(command, 'Unknown state')}"
    elif function_code == 0x03:  # Error Feedback
        errors = {
            0x00: "Both arms out of working range"
        }
        return f"Error: {errors.get(command, 'Unknown error')}"
    
    return "Unknown response type"

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('0.0.0.0', 6000)
client_socket.connect(server_address)

try:
    # Send pour coffee command (0x00)
    message = create_movement_packet(0x00)
    print(f"Sending movement command: Pour Coffee")
    client_socket.sendall(message)
    
    # Receive response from the server
    response = client_socket.recv(1024)
    print(decode_response(response))
finally:
    client_socket.close()