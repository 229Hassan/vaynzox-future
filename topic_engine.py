
import os, json, random
from google import genai

def get_topic():
    api_key = os.getenv("GEMINI_API_KEY")
    fallback_topics = [
        {"title": "The Invention That Will Make Smartphones Disappear by 2027", "thumbnail_text": "PHONE IS DEAD?", "description": "Future tech invention that will replace smartphones. You won't believe what's coming.", "keywords": ["future tech","invention","smartphone","AI"], "hook": "What if I told you the smartphone you hold will be extinct in 2 years?"},
        {"title": "America's Secret AI Factory That Builds Itself", "thumbnail_text": "AI FACTORY?", "description": "US secret invention - AI that builds factories without humans. Future of invention.", "keywords": ["AI","future tech","invention","USA"], "hook": "America built a factory that has zero humans inside - and it builds everything."},
        {"title": "Why China's Quantum Chip Could End the Internet in 2026", "thumbnail_text": "QUANTUM WAR?", "description": "Geopolitics meets future tech - China's quantum invention vs USA.", "keywords": ["quantum","China","USA","future tech","geopolitics"], "hook": "China's new quantum chip is so powerful it could break the entire internet - and USA is scared."}
    ]
    if not api_key:
        return random.choice(fallback_topics)
    
    client = genai.Client(api_key=api_key)
    prompt = """
You are a VIRAL YouTube strategist for US audience for channel VAYNZOX.
MAIN NICHE: FUTURE TECHNOLOGIES & INVENTIONS (AI, Quantum, Robotics, Chips, Drones, Brain Chips, Invisibility, Fusion)
SECONDARY NICHE: GEOPOLITICS - sometimes merge (e.g. USA vs China tech war, secret inventions)

You must create 1 UNIQUE topic TODAY. Mix these 3 types randomly:
Type A (70%): Pure Future Tech Invention - e.g. "The Invention That Will Replace Cars", "This AI Can Build Anything"
Type B (20%): Geopolitics x Future Tech - e.g. "Why USA's Secret Chip Could End China", "America's Quantum Shield"
Type C (10%): Wild Future Invention - e.g. "The Device That Makes You Invisible"

Rules:
- Title 45-60 chars, curiosity gap, US audience, HIGH CTR
- Thumbnail text: 2-3 WORDS, CAPS, SHOCKING (e.g. INVISIBLE?, END OF PHONES?, AI GOD?)
- Hook: 1 powerful line that shocks

Return ONLY valid JSON, no markdown:
{"title": "...", "thumbnail_text": "2-3 WORDS", "description": "SEO 2 lines with keywords future tech invention", "keywords": ["future tech","invention","AI","USA"], "hook": "Shocking hook line"}
"""
    try:
        res = client.models.generate_content(model='gemini-3.8-flash', contents=prompt)
        text = res.text.replace('```json','').replace('```','').strip()
        data = json.loads(text)
        data['thumbnail_text'] = data.get('thumbnail_text','FUTURE?')[:20].upper()
        return data
    except Exception as e:
        print(f"Topic error {e}")
        return random.choice(fallback_topics)
