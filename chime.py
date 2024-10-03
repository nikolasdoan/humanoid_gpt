# On macOS, you can play a variety of system sounds using built-in terminal commands. Here are a few ways you can trigger sounds using `osascript` or `afplay`:

# ### 1. **Using `osascript` with System Sounds**
# You can trigger system sounds (like notifications or alerts) via AppleScript with the `osascript` command.

# ```python
# import os

# # Play the default system alert sound
# def play_system_alert():
#     os.system('osascript -e "beep"')

# # Play multiple beeps
# def play_multiple_beeps():
#     os.system('osascript -e "repeat 3 times" -e "beep" -e "end repeat"')
# ```

# ### 2. **Using `afplay` to Play Audio Files**
# You can use the `afplay` command to play any audio file (WAV, MP3, etc.). macOS has several system sounds located at `/System/Library/Sounds`.

# ```python
import os

# Play the default system sound using afplay
os.system('afplay /System/Library/Sounds/Glass.aiff')

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

# This command will list all available system sounds on your macOS. You can then use any of these files with `afplay`.