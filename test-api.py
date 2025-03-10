import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

AUDIO_FILE = "video_audio.mp3"  

with open(AUDIO_FILE, "rb") as audio:
    transcript = openai.audio.transcriptions.create(
        model="whisper-1",
        file=audio
    )

print("Transcription:\n", transcript.text)

with open("transcription.txt", "w") as f:
    f.write(transcript.text)
