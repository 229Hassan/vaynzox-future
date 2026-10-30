
import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_notification(topic_data, video_path, thumb_path):
    # Ammi ka account sender hoga
    sender = os.getenv("EMAIL_USER", "saimakhalid510@gmail.com")
    # Tumhara account receiver hoga
    receiver = "229m.hassan@gmail.com"
    app_pass = os.getenv("EMAIL_PASS")
    
    if not app_pass:
        print("EMAIL_PASS missing, no email sent")
        return
        
    msg = MIMEMultipart()
    msg['From'] = f"VAYNZOX Studio <{sender}>"
    msg['To'] = receiver
    msg['Subject'] = f"VIDEO READY: {topic_data['title']}"
    body = f'''
Salam Hassan!

Ammi ke account se VAYNZOX Studio ne aaj ki video bana di hai (FREE Version).

TITLE: {topic_data['title']}
DESCRIPTION: {topic_data['description']}
KEYWORDS: {', '.join(topic_data.get('keywords',[]))}

Download: GitHub > Actions > Latest Run > Artifacts

- VAYNZOX FREE Studio
'''
    msg.attach(MIMEText(body, 'plain'))
    try:
        if os.path.exists(thumb_path):
            with open(thumb_path, "rb") as f:
                part = MIMEBase('application','octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition','attachment; filename=thumbnail.jpg')
                msg.attach(part)
    except Exception as e: print(e)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender, app_pass)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()
    print(f"Email sent from {sender} to {receiver}!")
