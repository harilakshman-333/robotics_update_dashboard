import logging
from datetime import datetime, timedelta
from typing import List, Dict
import httpx
from backend.config import get_settings

logger = logging.getLogger(__name__)

APIFY_API_URL = "https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items"

async def fetch_top_robotics_tweets(max_items: int = 50) -> List[Dict]:
    settings = get_settings()
    api_token = getattr(settings, "APIFY_API_TOKEN", None)
    if not api_token:
        logger.error("APIFY_API_TOKEN is not set in environment/config.")
        return []
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
    today = datetime.utcnow().strftime("%Y-%m-%d")
    payload = {
        "searchTerms": [
            "robotics",
            "humanoid robot",
            "Boston Dynamics",
            "Figure AI",
            "1X Technologies",
            "Agility Robotics",
            "ROS2",
            "robot manipulation",
            "autonomous mobile robot",
            "robotics funding"
        ],
        "maxItems": max_items,
        "sort": "Top",
        "lang": "en",
        "since": yesterday,
        "until": today
    }
    headers = {"Content-Type": "application/json"}
    params = {"token": api_token}
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(APIFY_API_URL, headers=headers, params=params, json=payload)
            resp.raise_for_status()
            tweets = resp.json()
        # Map to required shape
        results = []
        seen_urls = set()
        for tweet in tweets:
            url = f"https://x.com/i/web/status/{tweet.get('id_str', '')}"
            if url in seen_urls:
                continue
            seen_urls.add(url)
            results.append({
                "title": tweet.get("full_text", "")[:100],
                "raw_text": tweet.get("full_text", ""),
                "source_handle": tweet.get("user", {}).get("screen_name", ""),
                "url": url,
                "source": "x",
                "enriched": False,
                "engagement": {
                    "likes": tweet.get("favorite_count", 0),
                    "retweets": tweet.get("retweet_count", 0),
                    "views": tweet.get("views_count", 0),
                    "replies": tweet.get("reply_count", 0)
                }
            })
        # Sort by likes descending
        results.sort(key=lambda x: x["engagement"]["likes"], reverse=True)
        return results
    except Exception as e:
        logger.error(f"fetch_top_robotics_tweets error: {e}")
        return []import os
import time
import requests
from typing import List, Dict, Any

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
ACTOR_ID = "apidojo/twitter-scraper-lite"
APIFY_API_URL = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={APIFY_TOKEN}"

# --- Advanced Query Builder ---
def build_queries() -> List[str]:
    queries = [
        '("robotics" OR "physical AI" OR humanoid OR "embodied AI") AND (startup OR funding OR demo OR launch)',
        '("VLA" OR "robot learning" OR "foundation model") AND (paper OR code OR demo)',
        '("Unitree G1" OR humanoid robot) AND (video OR demo OR unveiled)'
    ]
    hashtags = ["robotics", "humanoid", "embodiedAI"]
    usernames = ["unitree", "bostonrobotics"]
    for tag in hashtags:
        queries.append(f"#{tag}")
    for user in usernames:
        queries.append(f"from:{user}")
    return queries

# --- Trigger Apify Actor Run ---
def trigger_apify_run(queries: List[str], max_tweets: int = 100) -> str:
    payload = {
        "input": {
            "searchTerms": queries,
            "maxTweets": max_tweets,
            "lang": "en"
        }
    }
    resp = requests.post(APIFY_API_URL, json=payload)
    resp.raise_for_status()
    run_id = resp.json()["data"]["id"]
    return run_id

# --- Poll for Completion ---
def wait_for_run(run_id: str, poll_interval: int = 10) -> str:
    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={APIFY_TOKEN}"
    while True:
        resp = requests.get(status_url)
        resp.raise_for_status()
        data = resp.json()["data"]
        if data["status"] in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
            if data["status"] != "SUCCEEDED":
                raise RuntimeError(f"Apify run failed: {data['status']}")
            return data["defaultDatasetId"]
        time.sleep(poll_interval)

# --- Download Results ---
def fetch_results(dataset_id: str) -> List[Dict[str, Any]]:
    url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={APIFY_TOKEN}&format=json"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

# --- Post-processing & Enrichment ---
def enrich_tweets(tweets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    enriched = []
    for t in tweets:
        tid = t.get("tweetId")
        if tid in seen:
            continue
        seen.add(tid)
        # Simple enrichment example
        t["classification"] = classify_tweet(t)
        t["tags"] = extract_tags(t)
        t["has_demo"] = has_demo(t)
        t["signal_score"] = compute_signal_score(t)
        enriched.append(t)
    return enriched

def classify_tweet(tweet: Dict[str, Any]) -> str:
    text = tweet.get("fullText", "").lower()
    if any(x in text for x in ["startup", "funding", "launch", "demo"]):
        return "startup"
    if any(x in text for x in ["paper", "code", "research", "arxiv"]):
        return "research"
    if any(x in text for x in ["product", "unveiled", "release"]):
        return "product launch"
    if any(x in text for x in ["discussion", "thread", "opinion"]):
        return "discussion"
    return "noise"

def extract_tags(tweet: Dict[str, Any]) -> List[str]:
    tags = []
    text = tweet.get("fullText", "").lower()
    if "humanoid" in text:
        tags.append("humanoid")
    if "digital twin" in text:
        tags.append("digital twin")
    if "robotics" in text:
        tags.append("robotics")
    return tags

def has_demo(tweet: Dict[str, Any]) -> bool:
    text = tweet.get("fullText", "").lower()
    return any(x in text for x in ["demo", "video", "watch", "see"]) or bool(tweet.get("mediaUrls"))

def compute_signal_score(tweet: Dict[str, Any]) -> float:
    score = tweet.get("likeCount", 0) + tweet.get("retweetCount", 0) * 2 + tweet.get("authorFollowersCount", 0) * 0.001
    if tweet.get("tags"):
        score += 5
    return score

# --- Main Entrypoint ---
def run_apify_x_scraper():
    queries = build_queries()
    run_id = trigger_apify_run(queries)
    dataset_id = wait_for_run(run_id)
    tweets = fetch_results(dataset_id)
    enriched = enrich_tweets(tweets)
    # TODO: Save to DB or return as needed
    print(f"Fetched and enriched {len(enriched)} tweets from Apify.")
    return enriched

if __name__ == "__main__":
    run_apify_x_scraper()
