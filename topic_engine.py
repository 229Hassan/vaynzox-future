import os, json, random, time
from google import genai

def get_topic():
    api_key = os.getenv("GEMINI_API_KEY")
    fallback = [
        {"title": "The Invention That Will Make Smartphones Disappear by 2027", "thumbnail_text": "PHONE IS DEAD?", "description": "Future tech invention that will replace smartphones.", "keywords": ["future tech","invention"], "hook": "What if the phone you hold will be extinct in 2 years?"},
        {"title": "America's Secret AI Factory That Builds Itself", "thumbnail_text": "AI FACTORY?", "description": "US secret AI invention - AI builds factories without humans.", "keywords": ["AI","future tech"], "hook": "America built a factory with zero humans inside."},
        {"title": "Why China's Quantum Chip Could End Internet in 2026", "thumbnail_text": "QUANTUM WAR?", "description": "China's quantum invention vs USA geopolitics.", "keywords": ["quantum","China","USA"], "hook": "China's chip could break entire internet."}
    ]
    if not api_key:
        return random.choice(fallback)
    
    client = genai.Client(api_key=api_key)
    prompt = """You are a viral YouTube strategist for US audience for channel VAYNZOX. Niche: Future Technologies & Inventions (AI, Quantum, Robotics, Chips). Sometimes merge with Geopolitics (USA vs China). Give 1 UNIQUE topic TODAY. Return ONLY valid JSON: {"title": "...", "thumbnail_text": "2-3 WORDS", "description": "SEO 2 lines", "keywords": ["future tech","invention"], "hook": "Powerful hook"} Title 45-60 chars."""
    
    for attempt in range(3):
        try:
            res = client.models.generate_content(model='gemini-3.8-flash', contents=prompt)
            text = res.text.replace('json','').replace('','').strip()
            data = json.loads(text)
            return data
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            if "disconnected" in str(e).lower() or "RemoteProtocol" in str(e):
                time.sleep(5)
                continue
            time.sleep(2)
    
    print("All attempts failed, using fallback")
    return random.choice(fallback)
