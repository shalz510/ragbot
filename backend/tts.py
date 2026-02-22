from gtts import gTTS
import os
import uuid


def text_to_speech(text):
    os.makedirs("data/audio", exist_ok=True)

    filename = f"data/audio/{uuid.uuid4()}.mp3"
    tts = gTTS(text=text, lang="en")
    tts.save(filename)

    return filename
