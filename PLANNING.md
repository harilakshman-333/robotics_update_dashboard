# Robotics News Intelligence Dashboard — Project Planning Document

## Project Overview
A full-stack AI-powered robotics news aggregation dashboard that automatically scrapes X/Twitter (via Grok API), Gmail newsletters (via Google Gmail API), and open web sources (via Playwright), enriches every article with Gemini Pro (summaries + entity extraction), and serves the results to a React dashboard with real-time updates.

## Tech Stack
| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Backend framework | FastAPI (async) |
| ORM | SQLAlchemy (async) + Alembic |
| Database | PostgreSQL 16 |
| Cache / Queue broker | Redis 7 |
| Task scheduler | Celery + Celery Beat |
| X/Twitter data | xAI Grok API (model: grok-3, OpenAI-SDK compatible) |
| AI enrichment | Google Gemini Pro API (gemini-1.5-pro) |
| Gmail | Google Gmail API with OAuth2 (headless refresh token) |
| Web scraping | Playwright (async, chromium) + BeautifulSoup4 |
| Frontend | React 18 + TypeScript + Tailwind CSS + Vite |
| State management | Zustand |
| Data fetching | TanStack React Query |
| Realtime | FastAPI native WebSocket |
| Containerisation | Docker + Docker Compose |
| Retry logic | Tenacity |

## Project Structure
(see planning doc for full tree)

## Phase Checklist

### Phase 1 — Foundation
- [ ] backend/config.py — pydantic-settings BaseSettings loading all env vars
- [ ] backend/database.py — async SQLAlchemy engine using postgresql+asyncpg://, AsyncSession factory, get_db dependency
- [ ] backend/models/feed_item.py — SQLAlchemy model FeedItem, Pydantic FeedItemOut
- [ ] backend/migrations/versions/001_initial.py — Alembic migration creating feed_items table
- [ ] alembic.ini — Alembic config pointing to DATABASE_URL
- [ ] .env.example — all required keys listed with empty values
- [ ] .env — populated with real keys (never committed to git)
- [ ] .gitignore — includes .env, __pycache__, node_modules, .playwright
- [ ] PostgreSQL running locally (or via Docker)
- [ ] Redis running locally (or via Docker)

### Phase 2 — Scrapers
- [ ] backend/scrapers/grok_x_fetcher.py — fetches robotics news from X via Grok API
- [ ] backend/scrapers/gmail_fetcher.py — fetches robotics newsletters from Gmail
- [ ] backend/scrapers/web_scraper.py — scrapes IEEE Spectrum, The Robot Report, arXiv

### Phase 3 — AI Enrichment
- [ ] backend/agents/gemini_agent.py — enriches articles with Gemini Pro

### Phase 4 — Scheduling
- [ ] backend/scheduler/celery_app.py — Celery app and beat schedule
- [ ] backend/scheduler/jobs.py — Celery tasks for scrapers and enrichment

### Phase 5 — API
- [ ] backend/api/routes/feeds.py — GET /feeds, /feeds/trending, POST /feeds/refresh
- [ ] backend/api/routes/status.py — GET /status, WebSocket /ws/status
- [ ] backend/main.py — FastAPI app, routers, CORS, WebSocket, Alembic migrations
- [ ] backend/requirements.txt — all dependencies pinned

### Phase 6 — Frontend
- [ ] frontend/src/types/feed.ts — TypeScript interfaces
- [ ] frontend/src/store/feedStore.ts — Zustand store
- [ ] frontend/src/hooks/useFeeds.ts — React Query for feeds
- [ ] frontend/src/hooks/useStatus.ts — WebSocket hook
- [ ] frontend/src/components/FeedCard.tsx — feed card UI
- [ ] frontend/src/components/TrendPanel.tsx — trending companies/tech
- [ ] frontend/src/components/AgentStatusBar.tsx — status bar
- [ ] frontend/src/components/SourceFilter.tsx — filter UI
- [ ] frontend/src/components/SearchBar.tsx — search input
- [ ] frontend/src/components/Dashboard.tsx — main dashboard layout
- [ ] frontend/src/App.tsx — app root
- [ ] frontend/package.json — dependencies

### Phase 7 — Docker & Final Integration
- [ ] docker-compose.yml — all services
- [ ] backend/Dockerfile — Python, Playwright
- [ ] frontend/Dockerfile — Node, build, nginx

## Environment Variables Reference
(see planning doc for full list)

## Copilot Instructions
(see planning doc for usage)

## Notes
- Never build frontend before GET /feeds returns real enriched data
- Always test each scraper independently before wiring to Celery
- Gemini free tier: 15 requests/minute — add time.sleep(4) during testing
- Grok credits: running X scraper every 2 hours costs ~$0.005/day
- Gmail OAuth: generate GOOGLE_REFRESH_TOKEN once, then headless
- Both celery worker AND celery beat must run simultaneously
