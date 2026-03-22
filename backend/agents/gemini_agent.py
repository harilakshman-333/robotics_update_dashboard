import google.generativeai as genai
import os
import json
from backend.config import get_settings
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from typing import Dict, Any

settings = get_settings()
genai.configure(api_key=settings.GEMINI_API_KEY)

MODEL_NAME = "gemini-1.5-pro"

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10), retry=retry_if_exception_type(Exception))
def enrich_item(item: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""
Given the following robotics news item, return a JSON object with:
- summary: 2-3 sentence summary
- category: Research|Product Launch|Funding|Policy|Events|General
- sentiment: positive|neutral|negative
- entities: companies, robots, people, technologies (as lists)
- relevance_score: 1-10

News item:
Title: {item.get('title')}
Text: {item.get('raw_text')}
"""
    try:
        response = genai.GenerativeModel(MODEL_NAME).generate_content(prompt)
        text = response.text.strip()
        try:
            data = json.loads(text)
        except Exception:
            # Try to extract JSON from text
            import re
            match = re.search(r'{.*}', text, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
            else:
                raise ValueError("Could not parse JSON from Gemini response")
        # Validate fields
        data.setdefault("summary", "")
        data.setdefault("category", "General")
        data.setdefault("sentiment", "neutral")
        data.setdefault("entities", {"companies": [], "robots": [], "people": [], "technologies": []})
        data.setdefault("relevance_score", 5)
        return data
    except Exception as e:
        # Fallback: minimal enrichment
        return {
            "summary": "",
            "category": "General",
            "sentiment": "neutral",
            "entities": {"companies": [], "robots": [], "people": [], "technologies": []},
            "relevance_score": 5
        }
