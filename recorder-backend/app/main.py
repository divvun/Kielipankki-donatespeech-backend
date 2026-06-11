"""
FastAPI application factory for the Kielipankki speech donation recorder.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import Schedule
from app.routers import content, media, upload
from app.schedule_processing import pre_process_schedule as _pre_process_schedule

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Kielipankki Recorder Backend",
    description="Speech donation recorder backend with Azure Blob Storage",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(content.router)
app.include_router(media.router)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "kielipankki-recorder-backend"}


def pre_process_schedule(schedule: Schedule) -> Schedule:
    """Compatibility wrapper for schedule preprocessing."""
    return _pre_process_schedule(schedule)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
