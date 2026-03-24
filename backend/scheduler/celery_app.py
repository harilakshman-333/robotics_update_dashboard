from celery import Celery
from celery.schedules import crontab
from backend.config import get_settings

settings = get_settings()

celery_app = Celery(
    "robotics_dashboard",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["backend.scheduler.jobs"]
)

celery_app.conf.beat_schedule = {
    # This runs every morning at 8am UTC. Adjust hour for your timezone if needed.
    "scrape-x-top-tweets-daily": {
        "task": "backend.scheduler.jobs.run_x_scraper",
        "schedule": crontab(hour=8, minute=0),
        "options": {"timezone": "UTC"}
    },
    "run_gmail_scraper": {
        "task": "backend.scheduler.jobs.run_gmail_scraper",
        "schedule": crontab(hour=8, minute=0),
    },
    "run_web_scraper": {
        "task": "backend.scheduler.jobs.run_web_scraper",
        "schedule": crontab(hour="*/3", minute=30),
    },
    "run_gemini_enrichment": {
        "task": "backend.scheduler.jobs.run_gemini_enrichment",
        "schedule": crontab(minute=15),
    },
}

celery_app.conf.timezone = "UTC"
