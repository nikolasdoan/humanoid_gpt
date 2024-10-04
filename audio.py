import os
import sounddevice as sd
import pygame
from pygame import mixer
import wave
import openai 
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def record_audio(duration=5, sample_rate=16000):
    print("Listening...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    file_path = 'recording.wav'
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)  # 16-bit audio
    wf.setframerate(sample_rate)
    wf.writeframes(recording.tobytes())
    wf.close()
    return file_path  # Return the file path instead of the raw audio data

def speech_to_text(wav_file_path):
    with open(wav_file_path, 'rb') as audio_file:
        transcription = openai.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file, 
            prompt="There are only two language spoken and can be spoken: English and Traditional Chinese."
        )
    print(transcription.text)
    return transcription.text

def text_to_speech(text, filename="output.wav", model="tts-1", voice="alloy"):
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
    )
    response.stream_to_file(filename)

def play_audio(filename):
    """
    Play an audio file using Pygame.

    Args:
        filename (str): The filename of the audio file to play.
    """
    mixer.init()
    print("Playing audio response...")
    sound = mixer.Sound(str(filename))
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))
    print("Audio playback completed.")
    mixer.quit()



# On macOS, you can play a variety of system sounds using built-in terminal commands. Here are a few ways you can trigger sounds using `osascript` or `afplay`:

# import os

# # Play the default system sound using afplay
# os.system('afplay /System/Library/Sounds/Glass.aiff')

# ### Available Sounds on macOS:
# macOS comes with a few system sounds located at `/System/Library/Sounds`. Some of the available sounds include:
# - **Glass.aiff**
# - **Sosumi.aiff**
# - **Basso.aiff**
# - **Blow.aiff**
# - **Frog.aiff**
# - **Hero.aiff**
# - **Pop.aiff**
# - **Ping.aiff**
  
# You can replace the sound file in the `afplay` command with any of these to play a different sound.

# ### Example to List All Sounds:
# ```bash
# ls /System/Library/Sounds
# ```