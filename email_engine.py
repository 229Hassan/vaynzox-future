import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_notification(topic_data, video_path, thumb_path):
    try:
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASS")
        to_email = "229m.hassan@gmail.com"
        
        if not email_user or not email_pass:
            print("Email secrets missing, skipping email")
            return
        
        print(f"Trying to send email from {email_user} to {to_email}")
        
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = to_email
        msg['Subject'] = f"VIDEO READY: {topic_data['title'][:40]}"

        body = f"""
Title: {topic_data['title']}
Thumbnail Text: {topic_data.get('thumbnail_text','')}
Description: {topic_data.get('description','')}
Hook: {topic_data.get('hook','')}

Video: {video_path}
Thumb: {thumb_path}

Upload to VAYNZOX channel!
"""
        msg.attach(MIMEText(body, 'plain'))

        # Try to attach thumbnail only (small)
        try:
            if thumb_path and os.path.exists(thumb_path):
                with open(thumb_path, "rb") as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(thumb_path)}")
                    msg.attach(part)
        except Exception as e:
            print(f"Thumb attach failed: {e}")

        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=20)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email_user, email_pass)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Email failed (but video is OK, skipping): {e}")
        # Do NOT raise error - video is more important than email
        return
