from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import QuizRequest, QuizResponse
from .dependencies import get_services, select_api_key

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.post("/generate", response_model=QuizResponse)
async def generate_quiz(
    payload: QuizRequest,
    db: Session = Depends(get_db),
    services=Depends(get_services),
    x_openai_api_key: str | None = Header(default=None),
):
    return await services.content.quiz(
        db,
        payload.youtube_video_id,
        payload.number_of_questions,
        payload.difficulty,
        select_api_key(payload.api_key, x_openai_api_key),
    )
