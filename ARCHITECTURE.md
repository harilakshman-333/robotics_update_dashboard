# Robotics Update Dashboard – Architecture & Integration Documentation

## Overview
This project is a full-stack, production-grade dashboard for real-time robotics news and intelligence. It aggregates, enriches, and displays data from Gmail, web scrapers, and X/Twitter (via Apify), with modular backend, automated scheduling, and a modern React frontend.

---

## System Architecture Diagram

```
+-------------------+         +-------------------+         +-------------------+
|   Gmail Scraper   |         |   Web Scraper     |         |   Apify X Fetcher |
+-------------------+         +-------------------+         +-------------------+
         |                           |                              |
         +---------------------------+------------------------------+
                                         |
                                         v
                                +-------------------+
                                |   Celery Worker   |
                                +-------------------+
                                         |
                                         v
                                +-------------------+
                                |   PostgreSQL DB   |
                                +-------------------+
                                         |
                                         v
                                +-------------------+
                                |   FastAPI Backend |
                                +-------------------+
                                         |
                                         v
                                +-------------------+
                                |   React Frontend  |
                                +-------------------+
```

---

## Key Components

### 1. Backend (Python/FastAPI)
- **Scrapers**: Modular fetchers for Gmail (IMAP), web (Playwright/BS4), and X/Twitter (Apify API).
- **Enrichment**: Gemini agent for NLP tagging, company detection, and demo/video flagging.
- **Database**: Async SQLAlchemy with PostgreSQL for storing all feed items.
- **Scheduler**: Celery with beat for periodic jobs (scraping, enrichment, etc.).
- **API**: FastAPI exposes REST endpoints and WebSocket for real-time updates.

### 2. Frontend (React/TypeScript/Vite)
- **Dashboard**: Modern UI with search, filters, and real-time updates.
- **State**: Zustand for state management, React Query for data fetching.
- **Styling**: Tailwind CSS for rapid, responsive design.

### 3. Orchestration
- **Docker Compose**: All services (backend, frontend, Celery, Redis, Postgres) run in containers for easy deployment.

---

## Third-Party Integrations

### 1. Apify (X/Twitter Scraping)
- **Actor**: apidojo/tweet-scraper (Tweet Scraper V2)
- **API**: Used via async httpx client in backend/scrapers/apify_x_fetcher.py
- **Purpose**: Fetches top robotics tweets daily, deduplicates, enriches, and stores in DB.
- **Scheduling**: Celery beat runs this every morning at 8am UTC.

### 2. Gmail (IMAP)
- **Integration**: Direct IMAP login using app password (no OAuth hassle).
- **Purpose**: Fetches unread robotics emails, parses, and stores in DB.

### 3. Web Scraping
- **Stack**: Playwright (headless browser) + BeautifulSoup4.
- **Purpose**: Scrapes robotics news from curated web sources.

### 4. Gemini (Google Generative AI)
- **Integration**: Used for NLP enrichment (summarization, tagging, company detection).

### 5. Database & Messaging
- **PostgreSQL**: Main data store for all feed items.
- **Redis**: Celery broker and cache for fast task/message passing.

---

## How It Works

1. **Scheduled Jobs**: Celery beat triggers scrapers and enrichment jobs on a schedule.
2. **Scraping**: Each fetcher pulls new data (Gmail, web, X/Twitter via Apify).
3. **Enrichment**: Gemini agent processes new items for tags, companies, demo/video flags.
4. **Storage**: All items are deduplicated and saved to PostgreSQL.
5. **API/Frontend**: FastAPI serves data to the React dashboard, which displays unified, enriched feeds in real time.

---

## Deployment & Extensibility
- All config (API tokens, DB URLs) is managed via .env files (never hardcoded).
- Add new scrapers or enrichment agents by dropping in a new module and wiring to the scheduler.
- Fully containerized for local or cloud deployment.

---

## Security & Privacy
- No API keys or secrets are stored in code or documentation.
- All sensitive config is loaded from environment variables.

---

## Authors & Credits
- System design, backend, and integration: You & GitHub Copilot (GPT-4.1)
- Apify actor: apidojo/tweet-scraper
- Frontend: React, Zustand, TanStack Query, Tailwind
- Backend: FastAPI, Celery, SQLAlchemy, Playwright, Gemini

---

For any further integration or scaling, just add new modules and update the scheduler as shown above.
