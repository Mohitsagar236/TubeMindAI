from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import NotesRequest, NotesResponse
from .dependencies import get_services, select_api_key

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/generate", response_model=NotesResponse)
async def generate_notes(
    payload: NotesRequest,
    db: Session = Depends(get_db),
    services=Depends(get_services),
    x_openai_api_key: str | None = Header(default=None),
):
    title, content = await services.content.notes(
        db, payload.youtube_video_id, payload.format, select_api_key(payload.api_key, x_openai_api_key)
    )
    return NotesResponse(title=title, content=content)
