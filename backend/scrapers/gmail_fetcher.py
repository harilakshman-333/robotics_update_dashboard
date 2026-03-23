import imaplib
import email
from email.header import decode_header
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from backend.config import get_settings
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

settings = get_settings()

def get_text_from_email(msg):
    text = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    body = part.get_payload(decode=True).decode()
                    text += body
                except Exception:
                    pass
            elif content_type == "text/html" and "attachment" not in content_disposition:
                try:
                    body = part.get_payload(decode=True).decode()
                    soup = BeautifulSoup(body, "html.parser")
                    text += soup.get_text(separator=' ')
                except Exception:
                    pass
    else:
        content_type = msg.get_content_type()
        try:
            body = msg.get_payload(decode=True).decode()
            if content_type == "text/plain":
                text += body
            elif content_type == "text/html":
                soup = BeautifulSoup(body, "html.parser")
                text += soup.get_text(separator=' ')
        except Exception:
            pass
    return text

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10), retry=retry_if_exception_type(Exception))
def fetch_gmail_news() -> List[Dict[str, Any]]:
    if not settings.GMAIL_USER or not settings.GMAIL_APP_PASSWORD:
        print("Gmail credentials missing in environment.")
        return []

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    try:
        mail.login(settings.GMAIL_USER, settings.GMAIL_APP_PASSWORD)
    except Exception as e:
        print(f"Gmail IMAP login failed: {e}")
        return []
        
    mail.select("inbox")
    
    # Use native IMAP X-GM-RAW to search using Gmail powerful search syntax
    status, messages = mail.search(None, 'X-GM-RAW', '"label:unread subject:(robotics OR robot OR ROS OR automation)"')
    if status != "OK":
        return []

    message_numbers = messages[0].split()
    items = []
    
    for num in message_numbers[:20]:
        status, msg_data = mail.fetch(num, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")
                else:
                    subject = str(subject)
                
                body = get_text_from_email(msg)
                body = body[:3000]
                
                items.append({
                    "title": subject,
                    "raw_text": body,
                    "url": "",
                    "source": "gmail"
                })
        
        # Mark as read
        mail.store(num, '+FLAGS', '\\Seen')

    mail.logout()
    return items
