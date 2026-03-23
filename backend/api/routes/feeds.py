from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from backend.models.feed_item import FeedItem, FeedItemOut
from backend.database import SessionLocal
from datetime import datetime, timedelta
from typing import List, Optional

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/feeds", response_model=List[FeedItemOut])
async def get_feeds(
    source: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    sentiment: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    query = select(FeedItem).where(FeedItem.enriched == True)
    if source:
        query = query.where(FeedItem.source == source)
    if category:
        query = query.where(FeedItem.category == category)
    if sentiment:
        query = query.where(FeedItem.sentiment == sentiment)
    if search:
        query = query.where(or_(FeedItem.title.ilike(f"%{search}%"), FeedItem.summary.ilike(f"%{search}%")))
    query = query.order_by(FeedItem.created_at.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    items = result.scalars().all()
    return [FeedItemOut.model_validate(item) for item in items]

@router.get("/feeds/trending")
async def get_trending(db: AsyncSession = Depends(get_db)):
    week_ago = datetime.utcnow() - timedelta(days=7)
    query = select(FeedItem.entities_json).where(FeedItem.created_at >= week_ago, FeedItem.enriched == True)
    result = await db.execute(query)
    entities = result.scalars().all()
    company_counts = {}
    tech_counts = {}
    for e in entities:
        if not e:
            continue
        for c in e.get("companies", []):
            company_counts[c] = company_counts.get(c, 0) + 1
        for t in e.get("technologies", []):
            tech_counts[t] = tech_counts.get(t, 0) + 1
    top_companies = sorted(company_counts.items(), key=lambda x: -x[1])[:10]
    top_tech = sorted(tech_counts.items(), key=lambda x: -x[1])[:10]
    return {"companies": top_companies, "technologies": top_tech}

@router.post("/feeds/refresh")
async def refresh_feeds():
    from backend.scheduler.jobs import run_x_scraper, run_gmail_scraper, run_web_scraper
    run_x_scraper.delay()
    run_gmail_scraper.delay()
    run_web_scraper.delay()
    return {"status": "refresh triggered"}
