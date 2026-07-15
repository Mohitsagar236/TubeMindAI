from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ChatSession, GeneratedFlashcard, GeneratedNote, GeneratedQuiz, GeneratedSummary, Video
from ..schemas import HistoryItem, HistoryResponse

router = APIRouter(prefix="/history", tags=["history"])


@router.get("", response_model=HistoryResponse)
def history(limit: int = Query(default=50, ge=1, le=200), db: Session = Depends(get_db)):
    items: list[HistoryItem] = []
    for video in db.scalars(select(Video).order_by(Video.created_at.desc()).limit(limit)).all():
        items.append(HistoryItem(id=video.id, type="video", youtube_video_id=video.youtube_video_id, title=video.title, content={"indexedStatus": video.indexed_status}, created_at=video.created_at))
    generated = [
        (GeneratedSummary, "summary", lambda x: x.content),
        (GeneratedNote, "notes", lambda x: x.content),
        (GeneratedQuiz, "quiz", lambda x: x.quiz_json),
        (GeneratedFlashcard, "flashcards", lambda x: x.flashcards_json),
    ]
    for model, type_name, content_getter in generated:
        rows = db.execute(select(model, Video).join(Video, model.video_id == Video.id).order_by(model.created_at.desc()).limit(limit)).all()
        for row, video in rows:
            items.append(HistoryItem(id=row.id, type=type_name, youtube_video_id=video.youtube_video_id, title=getattr(row, "title", video.title), content=content_getter(row), created_at=row.created_at))
    sessions = db.execute(select(ChatSession, Video).join(Video, ChatSession.video_id == Video.id).order_by(ChatSession.created_at.desc()).limit(limit)).all()
    for session, video in sessions:
        items.append(HistoryItem(id=session.id, type="chat", youtube_video_id=video.youtube_video_id, title=session.title, created_at=session.created_at))
    items.sort(key=lambda item: item.created_at, reverse=True)
    return HistoryResponse(items=items[:limit])
