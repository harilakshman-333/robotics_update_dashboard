import logging
import asyncio
from celery import shared_task, Task
from backend.scrapers.apify_x_fetcher import fetch_top_robotics_tweets
from backend.scrapers.gmail_fetcher import fetch_gmail_news
from backend.scrapers.web_scraper import fetch_web_news
from backend.agents.gemini_agent import enrich_item
from backend.database import SessionLocal
from backend.models.feed_item import FeedItem
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger("celery.jobs")

class BaseTask(Task):
    autoretry_for = (Exception,)
    max_retries = 3
    retry_backoff = True
    retry_backoff_max = 60
    retry_jitter = True

@shared_task(bind=True, base=BaseTask)
def run_x_scraper(self):
    logger.info("Starting X scraper task")
    async def _run():
        try:
            items = await fetch_top_robotics_tweets(max_items=50)
            count = 0
            async with SessionLocal() as session:
                for item in items:
                    feed = FeedItem(
                        url=item.get("url", ""),
                        title=item.get("title", ""),
                        source="x",
                        raw_text=item.get("raw_text", ""),
                        created_at=datetime.utcnow(),
                        enriched=False
                    )
                    try:
                        session.add(feed)
                        await session.commit()
                        count += 1
                    except IntegrityError:
                        await session.rollback()
            logger.info(f"X scraper: fetched {len(items)} top robotics tweets from yesterday")
        except Exception as e:
            logger.error(f"X scraper failed: {e}")
            raise e
    asyncio.run(_run())

@shared_task(bind=True, base=BaseTask)
def run_gmail_scraper(self):
    logger.info("Starting Gmail scraper task")
    async def _run():
        try:
            items = fetch_gmail_news()
            count = 0
            async with SessionLocal() as session:
                for item in items:
                    feed = FeedItem(
                        url="",
                        title=item.get("title", ""),
                        source="gmail",
                        raw_text=item.get("raw_text", ""),
                        created_at=datetime.utcnow(),
                        enriched=False
                    )
                    try:
                        session.add(feed)
                        await session.commit()
                        count += 1
                    except IntegrityError:
                        await session.rollback()
            logger.info(f"Gmail scraper finished, {count} new items saved.")
        except Exception as e:
            logger.error(f"Gmail scraper failed: {e}")
            raise e

    asyncio.run(_run())

@shared_task(bind=True, base=BaseTask)
def run_web_scraper(self):
    logger.info("Starting Web scraper task")
    async def _run():
        try:
            items = await fetch_web_news()
            count = 0
            async with SessionLocal() as session:
                for item in items:
                    feed = FeedItem(
                        url=item.get("url", ""),
                        title=item.get("title", ""),
                        source="web",
                        raw_text=item.get("raw_text", ""),
                        created_at=datetime.utcnow(),
                        enriched=False
                    )
                    try:
                        session.add(feed)
                        await session.commit()
                        count += 1
                    except IntegrityError:
                        await session.rollback()
            logger.info(f"Web scraper finished, {count} new items saved.")
        except Exception as e:
            logger.error(f"Web scraper failed: {e}")
            raise e

    asyncio.run(_run())

@shared_task(bind=True, base=BaseTask)
def run_gemini_enrichment(self):
    logger.info("Starting Gemini enrichment task")
    async def _run():
        try:
            async with SessionLocal() as session:
                result = await session.execute(select(FeedItem).where(FeedItem.enriched == False).limit(20))
                items = result.scalars().all()
                count = 0
                for item in items:
                    enriched = enrich_item({
                        "title": item.title,
                        "raw_text": item.raw_text
                    })
                    item.summary = enriched.get("summary", "")
                    item.category = enriched.get("category", "General")
                    item.sentiment = enriched.get("sentiment", "neutral")
                    item.entities_json = enriched.get("entities", {})
                    item.relevance_score = enriched.get("relevance_score", 5)
                    item.enriched = True
                    item.enriched_at = datetime.utcnow()
                    session.add(item)
                    count += 1
                await session.commit()
            logger.info(f"Gemini enrichment finished, {count} items enriched.")
        except Exception as e:
            logger.error(f"Gemini enrichment failed: {e}")
            raise e

    asyncio.run(_run())
