import base64
import json
from typing import List, Dict, Any
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from backend.config import get_settings
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

settings = get_settings()

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10), retry=retry_if_exception_type(Exception))
def fetch_gmail_news() -> List[Dict[str, Any]]:
    creds = Credentials(
        None,
        refresh_token=settings.GOOGLE_REFRESH_TOKEN,
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES
    )
    service = build("gmail", "v1", credentials=creds)
    query = "label:unread subject:(robotics OR robot OR ROS OR automation)"
    results = service.users().messages().list(userId="me", q=query, maxResults=20).execute()
    messages = results.get("messages", [])
    items = []
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        payload = msg_data.get("payload", {})
        headers = {h["name"]: h["value"] for h in payload.get("headers", [])}
        subject = headers.get("Subject", "(No Subject)")
        parts = payload.get("parts", [])
        body = ""
        if parts:
            for part in parts:
                if part.get("mimeType") == "text/html":
                    data = part["body"].get("data", "")
                    body = base64.urlsafe_b64decode(data + "==").decode("utf-8", errors="ignore")
                    break
        else:
            data = payload.get("body", {}).get("data", "")
            if data:
                body = base64.urlsafe_b64decode(data + "==").decode("utf-8", errors="ignore")
        soup = BeautifulSoup(body, "html.parser")
        text = soup.get_text()
        text = text[:3000]
        items.append({
            "title": subject,
            "raw_text": text,
            "url": "",
            "source": "gmail"
        })
        # Mark as read
        service.users().messages().modify(userId="me", id=msg["id"], body={"removeLabelIds": ["UNREAD"]}).execute()
    return items
