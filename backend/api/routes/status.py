from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.models.feed_item import FeedItem
from backend.database import SessionLocal
from datetime import datetime
from typing import Dict
import asyncio

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/status")
async def get_status(db: AsyncSession = Depends(get_db)):
    sources = ["x", "gmail", "web"]
    counts = {}
    for src in sources:
        q = select(func.count()).where(FeedItem.source == src)
        result = await db.execute(q)
        counts[src] = result.scalar()
    unenriched_q = select(func.count()).where(FeedItem.enriched == False)
    unenriched = await db.execute(unenriched_q)
    unenriched_count = unenriched.scalar()
    last_scraped = {}
    for src in sources:
        q = select(func.max(FeedItem.created_at)).where(FeedItem.source == src)
        result = await db.execute(q)
        last_scraped[src] = result.scalar()
    return {
        "counts": counts,
        "unenriched": unenriched_count,
        "last_scraped": last_scraped
    }

# WebSocket status push
class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/status")
async def ws_status(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Push status every 10 seconds
            await asyncio.sleep(10)
            # You could trigger this on enrichment completion for real-time
            async with SessionLocal() as session:
                sources = ["x", "gmail", "web"]
                counts = {}
                for src in sources:
                    q = select(func.count()).where(FeedItem.source == src)
                    result = await session.execute(q)
                    counts[src] = result.scalar()
                unenriched_q = select(func.count()).where(FeedItem.enriched == False)
                unenriched = await session.execute(unenriched_q)
                unenriched_count = unenriched.scalar()
                last_scraped = {}
                for src in sources:
                    q = select(func.max(FeedItem.created_at)).where(FeedItem.source == src)
                    result = await session.execute(q)
                    last_scraped[src] = result.scalar()
                await manager.broadcast({
                    "counts": counts,
                    "unenriched": unenriched_count,
                    "last_scraped": last_scraped,
                    "timestamp": datetime.utcnow().isoformat()
                })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
