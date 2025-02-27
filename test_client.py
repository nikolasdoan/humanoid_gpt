# client.py
import socket
import struct

def create_movement_packet(command):
    packet = bytes([0xFF, 0x01, command])
    print(f"2. Client creating movement packet: {packet.hex(' ')}")
    return packet

def decode_response(response):
    print(f"4. Client received raw response: {response.hex(' ')}")
    
    if len(response) < 3:
        print("4a. Error: Invalid response length")
        return "Invalid response length"
    
    header, function_code, command = response[:3]
    print(f"4b. Decoded response - Header: {header:#x}, Function Code: {function_code:#x}, Command: {command:#x}")
    
    if header != 0xFF:
        print("4c. Error: Invalid header")
        return "Invalid header"
    
    if function_code == 0x02:  # State Feedback
        states = {
            0x00: "Walking State",
            0x01: "Navigation State"
        }
        result = f"State Feedback: {states.get(command, 'Unknown state')}"
        print(f"4d. Interpreted as state feedback: {result}")
        return result
    elif function_code == 0x03:  # Error Feedback
        errors = {
            0x00: "Both arms out of working range",
            0xFF: "Unknown command"
        }
        result = f"Error: {errors.get(command, 'Unknown error')}"
        print(f"4d. Interpreted as error feedback: {result}")
        return result
    
    print("4e. Unknown response type")
    return "Unknown response type"

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('0.0.0.0', 6000)
print(f"1. Client connecting to {server_address}")
client_socket.connect(server_address)

try:
    # Send pour coffee command (0x00)
    message = create_movement_packet(0x00)
    print(f"3. Sending movement command to server")
    client_socket.sendall(message)
    
    # Receive response from the server
    response = client_socket.recv(1024)
    result = decode_response(response)
    print(f"5. Final result: {result}")
finally:
    print("6. Closing connection")
    client_socket.close()