import os
from io import BytesIO
from pydub import AudioSegment
import numpy as np
import sounddevice as sd
import openai 
from openai import OpenAI


import tempfile
import time
import pygame
from pygame import mixer

from deepgram import Deepgram
import elevenlabs
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
deepgram = Deepgram(os.getenv("DEEPGRAM_API_KEY"))
elevenlabs.set_api_key(os.getenv("ELEVENLABS_API_KEY"))
RECORDING_PATH = os.getenv("RECORDING_PATH")
RESPONSE_PATH = os.getenv("RESPONSE_PATH")

def openai_tts(text, filename="audio.wav", model="tts-1", voice="alloy"):
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
    )
    response.stream_to_file(filename)


# def read_audio(file_obj):
#     audio_bytes = BytesIO(file_obj.read())
#     audio_segment = AudioSegment.from_file(audio_bytes, format="mp3")
#     audio_array = np.array(audio_segment.get_array_of_samples())
#     return audio_array

import sounddevice as sd
import wave
import numpy as np
from pydub import AudioSegment
from pydub.silence import split_on_silence

# def record_audio(duration=5, sample_rate=16000):
#     print("Listening...")
    
#     # Record the audio
#     recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
#     sd.wait()
    
#     # Save raw recording to 'recording.wav'
#     wav_file = 'recording.wav'
#     wf = wave.open(wav_file, 'wb')
#     wf.setnchannels(1)
#     wf.setsampwidth(2)  # 16-bit audio
#     wf.setframerate(sample_rate)
#     wf.writeframes(recording.tobytes())
#     wf.close()

#     # Load the recording into pydub for silence removal
#     sound = AudioSegment.from_wav(wav_file)
#     chunks = split_on_silence(
#         sound, 
#         min_silence_len=500,  # Silence length threshold (in ms)
#         silence_thresh=-40  # Silence threshold (in dB)
#     )
    
#     # Combine chunks and remove the silence
#     if chunks:
#         processed_audio = sum(chunks)
#     else:
#         processed_audio = sound  # Fallback if no chunks are detected
    
#     # Export the processed audio (without silence)
#     processed_file = 'processed_recording.wav'
#     processed_audio.export(processed_file, format="wav")
    
#     print(f"Processed audio saved to {processed_file}")
#     return processed_file

import wave
# def record_audio(duration=5, sample_rate=16000):
#     print("Listening...")
#     recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
#     sd.wait()
#     wf = wave.open('recording.wav', 'wb')
#     wf.setnchannels(1)
#     wf.setsampwidth(2)  # 16-bit audio
#     wf.setframerate(sample_rate)
#     wf.writeframes(recording.tobytes())
#     wf.close()
#     return np.squeeze(recording)

# def speech_to_text(audio_data):
#     # Save audio data to a temporary file
#     audio_segment = AudioSegment(
#         data=audio_data.tobytes(),
#         sample_width=2,
#         frame_rate=16000,
#         channels=1,
#     )
#     with tempfile.NamedTemporaryFile(suffix=".mp3") as temp_audio_file:
#         audio_segment.export(temp_audio_file.name, format="mp3")
#         with open(temp_audio_file.name, 'rb') as file_obj:
#             # Transcribe audio using OpenAI's Whisper API
#             transcription = openai.audio.transcriptions.create(
#                 model="whisper-1", 
#                 file=file_obj,
#             )
#     print(transcription.text)
#     return transcription.text


# def play_audio(audio_data, sample_rate=16000):
#     print("Playing audio...")
#     sd.play(audio_data, sample_rate)
#     sd.wait()

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

# async def speech_to_text_deepgram(file_path):
#     with open(file_path, 'rb') as audio_file:
#         transcription = await deepgram.transcription.prerecorded(audio_file, language="zh-TW", model="nova-2")
#         # Extract the text from the response
#         words = transcription["results"]["channels"][0]["alternatives"][0]["words"]
#         text = " ".join([word["word"] for word in words])
#         return text

# async def transcribe(file_path):
#     with open(file_path, "rb") as audio:
#         source = {"buffer": audio, "mimetype": "audio/wav"}
#         response = deepgram.transcription.prerecorded(source, language="zh-TW", model="nova-2")
#         return response["results"]["channels"][0]["alternatives"][0]["words"]

# def elevenlabs_tts(text, voice="TX3LPaxmHKxFdv7VOQHJ", model="eleven_multilingual_v2"):
#     mixer.init()
#     current_time = time.time()
#     print("Generating speech...")

#     audio = elevenlabs.generate(
#         text=text,  # Directly use the text passed to the function
#         voice=voice,  # Use the provided voice or default to Joanne's voice
#         model=model  # Use the provided model or default to eleven_multilingual_v2
#     )
#     elevenlabs.save(audio, "./audio.wav")
    
#     audio_time = time.time() - current_time
#     print(f"Finished generating audio in {audio_time:.2f} seconds.")
#     print("Playing audio response...")
#     sound = mixer.Sound(str("./audio.wav"))
#     sound.play()
#     pygame.time.wait(int(sound.get_length() * 1000))
#     print("Audio playback completed.")
#     mixer.quit()



def elevenlabs_tts(text, voice="TX3LPaxmHKxFdv7VOQHJ", model="eleven_multilingual_v2"):
    current_time = time.time()
    print("Generating speech...")

    audio = elevenlabs.generate(
        text=text,  # Directly use the text passed to the function
        voice=voice,  # Use the provided voice or default to Joanne's voice
        model=model  # Use the provided model or default to eleven_multilingual_v2
    )
    filename = "./audio.wav"
    elevenlabs.save(audio, filename)
    
    audio_time = time.time() - current_time
    print(f"Finished generating audio in {audio_time:.2f} seconds.")
    return filename

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


