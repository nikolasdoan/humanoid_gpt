# client.py
import socket

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server (replace 'server_ip' with your server's IP address)
server_address = ('0.0.0.0', 6000)  # Change 'server_ip' to your server's IP
client_socket.connect(server_address)

try:
    message = "start"  # Replace 'start' with the specific character or string
    print(f"Sending: {message}")
    client_socket.sendall(message.encode())  # Send message
    
    # Receive response from the server
    response = client_socket.recv(1024)
    print(f"Received: {response.decode()}")
finally:
    client_socket.close()