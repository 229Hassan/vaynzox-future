import os, textwrap, re
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

def make_title_image(text, filename, W=1920, H=1080, bg_color=(12, 18, 35), accent=(255,215,0)):
    img = Image.new('RGB', (W, H), color=bg_color)
    draw = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 78)
        font_sub = ImageFont.truetype("DejaVuSans.ttf", 42)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
    wrapped = "\n".join(textwrap.wrap(text, width=30))
    draw.text((100, 350), wrapped, fill=(255,255,255), font=font_title, spacing=18)
    draw.text((100, 800), "VAYNZOX | Future Tech & Inventions", fill=accent, font=font_sub)
    img.save(filename)
    return filename

def create_video(audio_path, topic_data):
    W, H = 1920, 1080
    if audio_path.endswith(".mp3") and os.path.exists(audio_path):
        audio = AudioFileClip(audio_path)
        duration = audio.duration
    else:
        duration = 28
        audio = None
        if os.path.exists("output/voiceover.mp3"):
            audio = AudioFileClip("output/voiceover.mp3")
            duration = audio.duration

    make_title_image(topic_data['title'], "output/slide1.jpg", bg_color=(12,18,35))
    make_title_image(topic_data.get('hook','Future is here'), "output/slide2.jpg", bg_color=(35,12,12))
    make_title_image("Subscribe for Future Tech", "output/slide3.jpg", bg_color=(12,35,18))

    clip1 = ImageClip("output/slide1.jpg").set_duration(duration*0.5)
    clip2 = ImageClip("output/slide2.jpg").set_duration(duration*0.3)
    clip3 = ImageClip("output/slide3.jpg").set_duration(duration*0.2)
    final = concatenate_videoclips([clip1, clip2, clip3], method="compose")

    # Captions - simple bottom text
    if audio:
        final = final.set_audio(audio)

    out = "output/VIDEO_PRO_MAX_1080p.mp4"
    final.write_videofile(out, fps=30, codec='libx264', audio_codec='aac', bitrate="8000k", preset='medium', threads=4)
    return out
    except Exception as e:
        print(f"Video PRO error: {e}")
        import traceback; traceback.print_exc()
        return audio_path
