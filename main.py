
import os, datetime, glob
from topic_engine import get_topic
from script_engine import write_script
from voice_engine import create_voiceover
from video_engine import create_video
from thumbnail_engine import create_thumbnail
from email_engine import send_notification

os.makedirs("output", exist_ok=True)
print("VAYNZOX PRO MAX Starting...")

topic = get_topic()
print(f"Topic: {topic['title']} | Thumb: {topic['thumbnail_text']}")

script = write_script(topic)
script_file = f"output/{datetime.date.today()}_SCRIPT_PRO.txt"
with open(script_file,"w",encoding="utf-8") as f: f.write(script)
print(f"Script saved: {len(script)} chars")

audio = create_voiceover(script)
print(f"Audio: {audio} exists={os.path.exists(audio) if isinstance(audio,str) else False}")

video = create_video(audio, topic)
print(f"Video: {video}")

thumb = create_thumbnail(topic)
print(f"Thumb: {thumb}")

# META
with open(f"output/{datetime.date.today()}_META_PRO.txt","w",encoding="utf-8") as f:
    f.write(f"TITLE: {topic['title']}\n\nDESCRIPTION:\n{topic['description']}\n\nHook: {topic.get('hook','')}\n\nKEYWORDS: {', '.join(topic.get('keywords',[]))}\n\nTHUMBNAIL TEXT: {topic.get('thumbnail_text','')}\n\nVOICE: AndrewMultilingual - Confident Native US\n")

send_notification(topic, video, thumb)
print("DONE PRO MAX - 7 files in output/")
