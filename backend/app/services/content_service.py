from sqlalchemy.orm import Session

from ..config import Settings
from ..exceptions import ExternalServiceError
from ..models import GeneratedFlashcard, GeneratedNote, GeneratedQuiz, GeneratedSummary
from ..prompts.flashcard_prompt import FLASHCARD_PROMPT
from ..prompts.notes_prompt import NOTES_PROMPT
from ..prompts.quiz_prompt import QUIZ_PROMPT
from ..prompts.summary_prompt import SUMMARY_PROMPT
from ..schemas import FlashcardsResponse, QuizResponse
from ..utils.text_utils import parse_json_object
from .llm_service import LLMService
from .video_service import VideoService


class ContentService:
    def __init__(self, videos: VideoService, llm: LLMService, settings: Settings):
        self.videos = videos
        self.llm = llm
        self.settings = settings

    def transcript(self, db: Session, youtube_video_id: str) -> tuple[object, str]:
        video = self.videos.get_completed(db, youtube_video_id)
        return video, self.videos.transcript_text(db, video, self.settings.max_transcript_chars)

    async def summary(self, db: Session, youtube_video_id: str, summary_type: str, api_key: str | None):
        video, transcript = self.transcript(db, youtube_video_id)
        content = await self.llm.complete(SUMMARY_PROMPT.format(summary_type=summary_type, transcript=transcript), api_key)
        db.add(GeneratedSummary(video_id=video.id, summary_type=summary_type, content=content))
        db.commit()
        return content

    async def notes(self, db: Session, youtube_video_id: str, format_name: str, api_key: str | None):
        video, transcript = self.transcript(db, youtube_video_id)
        content = await self.llm.complete(NOTES_PROMPT.format(transcript=transcript), api_key)
        title = video.title or "Study Notes"
        db.add(GeneratedNote(video_id=video.id, title=title, content=content, format=format_name))
        db.commit()
        return title, content

    async def quiz(self, db: Session, youtube_video_id: str, count: int, difficulty: str, api_key: str | None):
        video, transcript = self.transcript(db, youtube_video_id)
        raw = await self.llm.complete(QUIZ_PROMPT.format(number_of_questions=count, difficulty=difficulty, transcript=transcript), api_key)
        try:
            response = QuizResponse.model_validate(parse_json_object(raw))
            if any(len(q.options) != 4 or q.correct_answer not in q.options for q in response.questions):
                raise ValueError("Invalid quiz option structure")
        except (ValueError, TypeError) as exc:
            raise ExternalServiceError("The language model returned an invalid quiz.") from exc
        db.add(GeneratedQuiz(video_id=video.id, quiz_json=response.model_dump(by_alias=True)))
        db.commit()
        return response

    async def flashcards(self, db: Session, youtube_video_id: str, count: int, api_key: str | None):
        video, transcript = self.transcript(db, youtube_video_id)
        raw = await self.llm.complete(FLASHCARD_PROMPT.format(number_of_cards=count, transcript=transcript), api_key)
        try:
            response = FlashcardsResponse.model_validate(parse_json_object(raw))
        except (ValueError, TypeError) as exc:
            raise ExternalServiceError("The language model returned invalid flashcards.") from exc
        db.add(GeneratedFlashcard(video_id=video.id, flashcards_json=response.model_dump(by_alias=True)))
        db.commit()
        return response
