from audio import record_audio, speech_to_text, text_to_speech, play_audio
import os 
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import threading
import re
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def resolve_prompt_path():
    """Return an absolute path to the root-level prompt.txt with fallbacks."""
    # Primary: ../prompt.txt relative to this file
    primary_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "prompt.txt"))
    if os.path.exists(primary_path):
        return primary_path
    # Fallback: prompt.txt relative to CWD
    cwd_path = os.path.abspath(os.path.join(os.getcwd(), "prompt.txt"))
    if os.path.exists(cwd_path):
        return cwd_path
    # Last resort: use file next to this module (if present)
    local_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "prompt.txt"))
    return local_path

with open(resolve_prompt_path(), "r") as file:
    system_prompt = file.read()
    messages = [{"role": "system", "content": system_prompt}]

def run_gpt():
    while True:     
        # content = input("User: ") keyboard input

        # chime_1 = threading.Thread(target=lambda: os.system('afplay ./audio_files/init.wav'))
        chime_1 = threading.Thread(target=lambda: os.system('afplay /System/Library/Sounds/Blow.aiff'))
        chime_1.start()

        content = speech_to_text(record_audio()) # speech input

        # chime_2 = threading.Thread(target=lambda: os.system('afplay ./audio_files/conf.wav'))
        chime_2 = threading.Thread(target=lambda: os.system('afplay /System/Library/Sounds/Glass.aiff'))
        chime_2.start()

        messages.append ({"role": "user", "content": content})
        completion = openai.chat.completions.create(
            # model="gpt-3.5-turbo", 
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=200, 
            temperature=0.2
        )
        chat_response = completion.choices[0].message.content
        match = re.search(r'\{(\d+)\}', chat_response)
        if match:
            control_number = int(match.group(1))
            print(control_number) # send this number to control system
            chat_response = re.sub(r'\{\d+\}', '', chat_response)
        else:
            control_number = 0
        print(f'NTU Humanoid: {chat_response}')
        messages.append ({"role": "assistant", "content": chat_response})

        text_to_speech(chat_response)
        play_audio("./audio_files/output.wav")
        return control_number





