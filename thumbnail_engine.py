
from PIL import Image, ImageDraw, ImageFont
import textwrap, random

def create_thumbnail(topic_data):
    W, H = 1280, 720
    # Modern gradient background - dark blue to black
    img = Image.new('RGB', (W, H), color=(15, 20, 40))
    draw = ImageDraw.Draw(img)
    
    # Modern 2025 style - 3 colors
    colors = [(200, 20, 20), (20, 120, 200), (220, 180, 0)]
    accent = random.choice(colors)
    
    # Top bar - modern thin
    draw.rectangle([(0, 0), (W, 90)], fill=accent)
    
    # Big 3D text effect - MrBeast style
    try:
        font_top = ImageFont.truetype("DejaVuSans-Bold.ttf", 42)
        font_main = ImageFont.truetype("DejaVuSans-Bold.ttf", 125)
        font_sub = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
    except:
        font_top = ImageFont.load_default()
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Top
    draw.text((35, 22), "VAYNZOX EXCLUSIVE • 2026", fill="white", font=font_top)

    # Main text - with 3D shadow
    thumb_text = topic_data.get('thumbnail_text', 'BREAKING').upper()
    # Wrap to 2 lines max
    lines = textwrap.wrap(thumb_text, width=10)
    y = 160
    for line in lines[:2]:
        # Shadow
        draw.text((53, y+6), line, fill="black", font=font_main)
        # Main with stroke
        draw.text((50, y), line, fill="white", font=font_main, stroke_width=10, stroke_fill="black")
        y += 145

    # Bottom - Yellow highlighter style
    draw.rectangle([(45, 520), (500, 590)], fill=(255, 230, 0))
    draw.text((60, 525), "USA vs CHINA", fill="black", font=font_sub)

    # Add subtle vignette
    draw.rectangle([(0, 0), (W, H)], outline=(255,255,255), width=4)

    path = "output/THUMBNAIL_MODERN.jpg"
    img.save(path, quality=95)
    return path
