import socket
import sys
from pynput import keyboard
from gpt import run_gpt
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

def create_movement_packet(command):
    packet = bytes([0xFF, 0x01, command])
    print(f"Sending movement packet: {packet.hex(' ')}")
    return packet

def decode_response(response):
    print(f"Received raw response: {response.hex(' ')}")
    
    if len(response) < 3:
        print("Error: Invalid response length")
        return "Invalid response length"
    
    header, function_code, command = response[:3]
    print(f"Decoded response - Header: {header:#x}, Function Code: {function_code:#x}, Command: {command:#x}")
    
    if header != 0xFF:
        print("Error: Invalid header")
        return "Invalid header"
    
    if function_code == 0x02:  # State Feedback
        states = {
            0x00: "Walking State",
            0x01: "Navigation State"
        }
        result = f"State Feedback: {states.get(command, 'Unknown state')}"
        print(f"Interpreted as state feedback: {result}")
        return result
    elif function_code == 0x03:  # Error Feedback
        errors = {
            0x00: "Both arms out of working range",
            0xFF: "Unknown command"
        }
        result = f"Error: {errors.get(command, 'Unknown error')}"
        print(f"Interpreted as error feedback: {result}")
        return result
    
    print("Unknown response type")
    return "Unknown response type"

class Client:
    def __init__(self):
        self.client_socket = None
        self.is_connected = False
        self.is_processing = False
        self.listener = None

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('192.168.1.87', 55635)
        print(f"Connecting to {server_address}...")
        
        try:
            self.client_socket.connect(server_address)
            self.is_connected = True
            print("Connected successfully!")
            return True
        except ConnectionRefusedError:
            print("Error: Could not connect to server. Make sure the server is running.")
            return False
        except Exception as e:
            print(f"Error: {str(e)}")
            return False

    def on_press(self, key):
        try:
            if key == keyboard.KeyCode.from_char('g') and not self.is_processing:
                self.is_processing = True
                print("\nTriggering GPT interaction...")
                try:
                    # Run GPT and get control number
                    control_number = run_gpt()
                    print(f"GPT returned control number: {control_number}")
                    
                    # If GPT returns 1, send movement packet
                    if control_number == 1:
                        print("Sending pour coffee command...")
                        message = create_movement_packet(0x00)
                        self.client_socket.sendall(message)
                        
                        # Wait for and decode response
                        response = self.client_socket.recv(1024)
                        result = decode_response(response)
                        print(f"Server response: {result}")
                    else:
                        print("GPT did not return coffee command (control number != 1)")
                        
                except Exception as e:
                    print(f"Error during GPT interaction: {str(e)}")
                finally:
                    self.is_processing = False
                    print("\nPress 'G' to trigger GPT interaction")
                    print("Press 'Q' to quit")
            
            elif key == keyboard.KeyCode.from_char('q'):
                print("\nQuitting...")
                return False  # Stop listener
                
        except AttributeError:
            pass  # Ignore special keys

    def on_release(self, key):
        pass  # We don't need to do anything on key release

    def run(self):
        if not self.connect():
            return

        print("\nPress 'G' to trigger GPT interaction")
        print("Press 'Q' to quit")
        
        # Start keyboard listener
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            self.listener = listener
            listener.join()  # Wait for listener to stop

    def cleanup(self):
        if self.client_socket:
            print("Closing connection...")
            self.client_socket.close()

def main():
    client = Client()
    try:
        client.run()
    except KeyboardInterrupt:
        print("\nShutdown requested")
    finally:
        client.cleanup()

if __name__ == "__main__":
    main() 