import requests

XI_API_KEY = "your_api_key_here"
url = "https://api.elevenlabs.io/v1/voices"
headers = {
  "Accept": "application/json",
  "xi-api-key": "4b1dfa1c6c7cbe69c54446348e7e0d42"
}

response = requests.get(url, headers=headers)
data = response.json()

for voice in data['voices']:
  print(f"{voice['name']}; {voice['voice_id']}")

"""
Aria; 9BWtsMINqrJLrRacOk9x
Roger; CwhRBWXzGAHq8TQ4Fs17
Sarah; EXAVITQu4vr4xnSDxMaL
Laura; FGY2WhTYpPnrIDTdsKH5
Charlie; IKne3meq5aSn9XLyUdCD
George; JBFqnCBsd6RMkjVDRZzb
Callum; N2lVS1w4EtoT3dr4eOWO
River; SAz9YHcvj6GT2YYXdXww
Liam; TX3LPaxmHKxFdv7VOQHJ
Charlotte; XB0fDUnXU5powFXDhCwa
Alice; Xb7hH8MSUJpSbSDYk0k2
Matilda; XrExE9yKIg1WjnnlVkGX
Will; bIHbv24MWmeRgasZH58o
Jessica; cgSgspJ2msm6clMCkdW9
Eric; cjVigY5qzO86Huf0OWal
Chris; iP95p4xoKVk53GoZ742B
Brian; nPczCjzI2devNBz1zQrb
Daniel; onwK4e9ZLuTAKqWW03F9
Lily; pFZP5JQG7iQjIQuC4Bku
Bill; pqHfZKP75CvOlQylNhV4
Markus - Mature and Chill; 6CIWY45ExhhlHeEsgHlo
Joanne - pensive, introspective, soft and lovely; UIpYR5ztFVFz4W8qqDfi
OmniBot - cyborg; rPxck1zibbCKXXRCSuxa

Martin Li -WuLq5z7nEcrhppO0ZQJw
"""