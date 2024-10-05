import threading
import os

def play_audio():
    try:
        os.system('afplay ./audio_files/init.wav')
    except Exception as e:
        print(f"Error playing audio: {e}")

chime_1 = threading.Thread(target=play_audio)
chime_1.start()