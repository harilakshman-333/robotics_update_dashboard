import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import feeds, status
from backend.database import engine
from alembic.config import Config
from alembic import command
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.main")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(feeds.router)
app.include_router(status.router)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Robotics Update Dashboard API executing. Go to /docs for Swagger UI."}


@app.on_event("startup")
async def on_startup():
    logger.info("Starting up FastAPI app...")
    # Run Alembic migrations programmatically with granular debug logging
    try:
        alembic_ini_path = os.path.join(os.path.dirname(__file__), "../alembic.ini")
        logger.debug(f"Alembic ini path: {alembic_ini_path}")
        alembic_cfg = Config(alembic_ini_path)
        logger.debug("Alembic Config object created.")
        logger.info("Running Alembic migrations...")
        logger.debug("About to call command.upgrade...")
        command.upgrade(alembic_cfg, "head")
        logger.debug("command.upgrade returned successfully.")
        logger.info("Alembic migrations complete.")
    except Exception as e:
        logger.error(f"Alembic migration failed: {e}")
        raise

if __name__ == "__main__":
    logger.info("Starting Uvicorn server...")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
