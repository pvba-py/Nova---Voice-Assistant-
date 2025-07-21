import elevenlabs
from dotenv import load_dotenv
import os

load_dotenv()  # Loads your .env file if you use one
api_key = os.getenv("ELEVENLABS_API_KEY")
elevenlabs.set_api_key(api_key)

voices = elevenlabs.voices()
print("Available voices for your API key:")
for voice in voices:
    print(f"- {voice.name}")