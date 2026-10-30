
import os
from google import genai

def write_script(topic_data):
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    prompt = f'''
You are a TOP US YouTube scriptwriter (like MrBeast + Wendover + Marques Brownlee) for channel VAYNZOX.

MAIN NICHE: Future Technologies & Inventions
Title: {topic_data['title']}
Hook: {topic_data['hook']}

Write a 1000-1100 word VIRAL script that feels like a professional documentary.

Structure:
1. HOOK (0-25 sec): Start with a mind-blowing question. NO "Welcome". Example: "What if I told you the phone in your hand will be worthless in 2 years?" Add [PAUSE] [EMPHASIS]
2. THE PROBLEM (25sec-2min): Why current tech is failing? Why we need this invention?
3. THE INVENTION (2-8min): Explain the future tech invention like I'm 15 but smart. Use: How it works, Who invented, Numbers, "Here's the insane part", Compare to sci-fi movies. If geopolitics angle, add USA vs China race.
4. THE TWIST (8-10min): What no one is telling you? Dark side? Secret US/China plan? Will it replace jobs?
5. FUTURE & CTA (10-12min): When will you get it? 2026-2028 timeline? What happens if you ignore? Subscribe for future.

Rules:
- American confident native English
- Short sentences, conversational, powerful
- Each sentence on new line (for captions)
- Add [PAUSE] and [EMPHASIS] for voice
- No fluff, no "As an AI"
- Make it so engaging that viewer watches till end
'''
    res = client.models.generate_content(model='gemini-3.8-flash', contents=prompt)
    return res.text
