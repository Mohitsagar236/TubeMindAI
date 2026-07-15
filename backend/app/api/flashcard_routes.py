from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import FlashcardsRequest, FlashcardsResponse
from .dependencies import get_services, select_api_key

router = APIRouter(prefix="/flashcards", tags=["flashcards"])


@router.post("/generate", response_model=FlashcardsResponse)
async def generate_flashcards(
    payload: FlashcardsRequest,
    db: Session = Depends(get_db),
    services=Depends(get_services),
    x_openai_api_key: str | None = Header(default=None),
):
    return await services.content.flashcards(
        db, payload.youtube_video_id, payload.number_of_cards, select_api_key(payload.api_key, x_openai_api_key)
    )
