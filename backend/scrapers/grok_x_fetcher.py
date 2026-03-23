import os
import json
from openai import OpenAI
from backend.config import get_settings
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from typing import List, Dict, Any
from difflib import SequenceMatcher

settings = get_settings()

MODEL = "grok-3"
KEYWORDS = [
    "humanoid robots", "Figure AI", "Boston Dynamics", "1X Technologies", "Apptronik",
    "Agility Robotics", "ROS2", "robot manipulation", "SLAM", "autonomous mobile robots", "robotics funding"
]

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10), retry=retry_if_exception_type(Exception))
def fetch_grok_x_news(hours: int = 6) -> List[Dict[str, Any]]:
    client = OpenAI(
        api_key=settings.XAI_API_KEY,
        base_url="https://api.x.ai/v1"
    )
    prompt = (
        f"Search X for robotics news from the past {hours} hours. "
        f"Track these keywords: {', '.join(KEYWORDS)}. "
        "Return a JSON list of dicts: title, summary, source_handle, topic, sentiment, companies_mentioned."
    )
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            temperature=0.2,
        )
        text = response.choices[0].message.content.strip()
        try:
            items = json.loads(text)
        except Exception:
            import re
            match = re.search(r'\[.*\]', text, re.DOTALL)
            if match:
                items = json.loads(match.group(0))
            else:
                raise ValueError("Could not parse JSON from Grok response")
        # Deduplicate by title similarity
        deduped = []
        seen = []
        for item in items:
            title = item.get("title", "")
            if not any(SequenceMatcher(None, title, s).ratio() > 0.85 for s in seen):
                deduped.append(item)
                seen.append(title)
        return deduped
    except Exception as e:
        print(f"fetch_grok_x_news error: {e}")
        raise e
