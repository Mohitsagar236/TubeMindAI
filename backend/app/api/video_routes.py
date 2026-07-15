from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Video
from ..schemas import (
    SummaryRequest,
    SummaryResponse,
    VideoHistoryItem,
    VideoHistoryResponse,
    VideoProcessRequest,
    VideoProcessResponse,
)
from .dependencies import get_services, select_api_key

router = APIRouter(prefix="/videos", tags=["videos"])


@router.get("/history", response_model=VideoHistoryResponse)
def video_history(limit: int = Query(default=50, ge=1, le=200), db: Session = Depends(get_db)):
    videos = db.scalars(select(Video).order_by(Video.created_at.desc()).limit(limit)).all()
    return VideoHistoryResponse(
        videos=[
            VideoHistoryItem(
                youtube_video_id=video.youtube_video_id,
                title=video.title,
                thumbnail_url=video.thumbnail_url,
                indexed_status=video.indexed_status,
                created_at=video.created_at,
            )
            for video in videos
        ]
    )


@router.post("/process", response_model=VideoProcessResponse)
async def process_video(
    payload: VideoProcessRequest,
    db: Session = Depends(get_db),
    services=Depends(get_services),
    x_openai_api_key: str | None = Header(default=None),
):
    video = await services.videos.process_video(
        db,
        str(payload.youtube_url),
        payload.youtube_video_id,
        payload.title,
        str(payload.thumbnail_url) if payload.thumbnail_url else None,
        x_openai_api_key,
    )
    return VideoProcessResponse(
        video_id=video.id,
        youtube_video_id=video.youtube_video_id,
        indexed_status=video.indexed_status,
        transcript_status=video.transcript_status,
    )


@router.post("/summary", response_model=SummaryResponse)
async def generate_summary(
    payload: SummaryRequest,
    db: Session = Depends(get_db),
    services=Depends(get_services),
    x_openai_api_key: str | None = Header(default=None),
):
    summary = await services.content.summary(
        db, payload.youtube_video_id, payload.summary_type, select_api_key(payload.api_key, x_openai_api_key)
    )
    return SummaryResponse(summary=summary)
