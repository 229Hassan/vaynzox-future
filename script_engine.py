import os, time
from google import genai

def write_script(topic_data):
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    prompt = f'''Write a 1000 word viral YouTube script for VAYNZOX. Future Tech niche. Title: {topic_data['title']} Hook: {topic_data['hook']} Audience: US 18-45. Structure: 1. HOOK (0-25s) shocking question 2. CONTEXT (25s-2min) 3. DEEP DIVE (2-8min) invention explained 4. TWIST (8-10min) USA vs China 5. FUTURE & CTA. Rules: American English, short sentences, [PAUSE] [EMPHASIS], each sentence new line.'''
    
    for attempt in range(3):
        try:
            res = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            return res.text
        except Exception as e:
            print(f"Script attempt {attempt+1} failed: {e}")
            time.sleep(5)
            if attempt == 2:
                return f"{topic_data['hook']} [PAUSE] Today we explore {topic_data['title']}. [PAUSE] This invention will change everything. [PAUSE] Let's dive in. [PAUSE] {topic_data['description']} [PAUSE] The future is here. Subscribe to VAYNZOX for more future tech."
            continue
