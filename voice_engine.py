
import os, asyncio, re
import edge_tts

VOICES = {
    "confident": "en-US-AndrewMultilingualNeural", # Most realistic confident male - BEST for geopolitics
    "deep": "en-US-GuyNeural",
    "female_pro": "en-US-AriaNeural"
}

async def _make_edge(text, path, voice_name):
    # Clean text for TTS
    clean_text = re.sub(r'\[PAUSE\]|\[EMPHASIS\]', '...', text)
    communicate = edge_tts.Communicate(clean_text, voice_name, rate="+5%", pitch="+2Hz")
    await communicate.save(path)

def create_voiceover(script_text):
    # Take first 4500 chars for stability but keep powerful parts
    text = script_text[:4500]
    path = "output/voiceover.mp3"
    voice = VOICES["confident"]  # Andrew - super realistic native confident
    
    # Try Edge TTS Pro
    try:
        print(f"Trying PRO voice {voice}...")
        asyncio.run(_make_edge(text, path, voice))
        if os.path.exists(path) and os.path.getsize(path) > 5000:
            print(f"PRO Voice success: {os.path.getsize(path)} bytes")
            return path
    except Exception as e:
        print(f"Edge PRO failed: {e}")

    # Fallback 1: GuyNeural
    try:
        print("Trying GuyNeural...")
        asyncio.run(_make_edge(text, path, VOICES["deep"]))
        if os.path.exists(path) and os.path.getsize(path) > 1000:
            return path
    except Exception as e:
        print(f"Guy failed {e}")

    # Fallback 2: gTTS US
    try:
        from gtts import gTTS
        print("Trying gTTS US...")
        tts = gTTS(text=text, lang='en', tld='us')
        tts.save(path)
        if os.path.exists(path) and os.path.getsize(path) > 1000:
            return path
    except Exception as e:
        print(f"gTTS failed {e}")

    with open("output/voiceover.txt", "w", encoding="utf-8") as f:
        f.write(text)
    return "output/voiceover.txt"
