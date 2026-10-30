
import os, textwrap, re
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

def create_gradient_bg(W, H, color1, color2):
    img = Image.new('RGB', (W, H), color1)
    return img

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
    # Center vertically
    draw.text((100, 350), wrapped, fill=(255,255,255), font=font_title, spacing=18, stroke_width=2, stroke_fill=(0,0,0))
    draw.text((100, 800), "VAYNZOX | Geopolitics x Future Tech • 2026", fill=accent, font=font_sub)
    img.save(filename)
    return filename

def create_video(audio_path, topic_data):
    try:
        W, H = 1920, 1080
        if audio_path.endswith(".mp3") and os.path.exists(audio_path):
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            print(f"Audio duration: {duration}")
        else:
            print("No audio, using 60 sec")
            duration = 60
            audio = None

        # Clean script for captions
        script_path = [f for f in os.listdir("output") if "SCRIPT" in f]
        script_text = ""
        if script_path:
            with open(os.path.join("output", script_path[0]), "r", encoding="utf-8") as f:
                script_text = f.read()
        
        # Split into sentences for captions
        sentences = re.split(r'(?<=[.!?])\s+', script_text)[:12]
        sentences = [s.replace("[PAUSE]","").replace("[EMPHASIS]","").strip() for s in sentences if len(s.strip())>10]

        # Create 3 PRO slides with effects
        slides = []
        # Slide 1: Title
        make_title_image(topic_data['title'], "output/slide1.jpg", bg_color=(12,18,35), accent=(255,215,0))
        clip1 = ImageClip("output/slide1.jpg").set_duration(duration*0.5)
        # Zoom in effect (Ken Burns)
        clip1 = clip1.resize(lambda t: 1 + 0.05*t/duration)
        slides.append(clip1)

        # Slide 2: Hook
        hook_text = topic_data.get('hook','The next war will be invisible')
        make_title_image(hook_text, "output/slide2.jpg", bg_color=(35,12,12), accent=(255,255,255))
        clip2 = ImageClip("output/slide2.jpg").set_duration(duration*0.3)
        clip2 = clip2.resize(lambda t: 1.05 - 0.05*t/duration)
        slides.append(clip2)

        # Slide 3: Outro CTA
        make_title_image("Subscribe for Future Wars Explained", "output/slide3.jpg", bg_color=(12,35,18), accent=(255,215,0))
        clip3 = ImageClip("output/slide3.jpg").set_duration(duration*0.2)
        slides.append(clip3)

        # Concatenate with fade
        final = concatenate_videoclips(slides, method="compose")
        
        # Add captions - modern style bottom
        caption_clips = []
        if sentences:
            total_chars = sum(len(s) for s in sentences)
            time_per_char = duration / max(total_chars,1)
            current_time = 0
            for sent in sentences[:8]:  # Max 8 captions
                dur = len(sent) * time_per_char * 2.5
                if dur < 1.5: dur = 1.5
                if current_time + dur > duration: break
                
                # Create caption image
                cap_img = Image.new('RGBA', (W, 200), (0,0,0,0))
                cap_draw = ImageDraw.Draw(cap_img)
                try:
                    cap_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 56)
                except:
                    cap_font = ImageFont.load_default()
                # Wrap caption
                cap_wrapped = "\n".join(textwrap.wrap(sent, width=45))
                cap_draw.text((50, 10), cap_wrapped, fill=(255,255,255), font=cap_font, stroke_width=4, stroke_fill=(0,0,0), spacing=8)
                cap_path = f"output/cap_{current_time:.0f}.png"
                cap_img.save(cap_path)
                
                cap_clip = ImageClip(cap_path).set_duration(dur).set_start(current_time).set_position(('center', 0.75), relative=True)
                caption_clips.append(cap_clip)
                current_time += dur

        # Composite final with captions
        if caption_clips:
            final = CompositeVideoClip([final] + caption_clips)

        if audio:
            final = final.set_audio(audio)

        out = "output/VIDEO_PRO_MAX_1080p.mp4"
        final.write_videofile(out, fps=30, codec='libx264', audio_codec='aac', bitrate="8000k", audio_bitrate="192k", preset='medium', threads=4)
        return out
    except Exception as e:
        print(f"Video PRO error: {e}")
        import traceback; traceback.print_exc()
        return audio_path
