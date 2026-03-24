# Robotics Update Dashboard – Quick Start

## Prerequisites
- Docker & Docker Compose installed
- (Optional) Node.js & Python 3.11+ if running locally without Docker
- API keys for Gmail, Gemini, Apify, etc. (see `.env.example`)

## Quick Start (Docker Compose)

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd robotics_update_dashboard
   ```

2. **Configure environment variables:**
   - Copy `.env.example` to `.env` and fill in all required API keys and settings.
   ```sh
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Build and start all services:**
   ```sh
   docker compose up --build -d
   ```

4. **Access the dashboard:**
   - Frontend: http://localhost:3000
   - Backend API docs: http://localhost:8000/docs

5. **Verify scheduled jobs:**
   - Celery Beat will run all scrapers and enrichment jobs automatically (see `backend/scheduler/celery_app.py` for schedule).
   - X/Twitter (Apify) fetcher runs daily at 8am UTC.

## Manual Run (for development)

- **Backend only:**
  ```sh
  cd backend
  uvicorn backend.main:app --reload
  ```
- **Frontend only:**
  ```sh
  cd frontend
  npm install
  npm run dev
  ```

## Architecture & Integrations
See [ARCHITECTURE.md](ARCHITECTURE.md) for a full system overview, third-party integrations, and deployment details.

---

**Need help?**
- Check logs with `docker compose logs` or view API docs at `/docs`.
- For advanced configuration, see the scheduler and config files in `backend/`.
