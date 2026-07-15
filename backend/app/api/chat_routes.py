from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import ChatRequest, ChatResponse
from .dependencies import get_services, select_api_key

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    services=Depends(get_services),
    x_openai_api_key: str | None = Header(default=None),
):
    await services.videos.process_video(
        db,
        str(payload.youtube_url),
        payload.youtube_video_id,
        payload.title,
        str(payload.thumbnail_url) if payload.thumbnail_url else None,
        select_api_key(payload.api_key, x_openai_api_key),
    )
    session_id, answer, sources = await services.rag.chat(
        db,
        payload.youtube_video_id,
        payload.question,
        payload.chat_session_id,
        select_api_key(payload.api_key, x_openai_api_key),
    )
    return ChatResponse(chat_session_id=session_id, answer=answer, sources=sources)
