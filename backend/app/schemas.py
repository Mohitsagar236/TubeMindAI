from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


def to_camel(value: str) -> str:
    head, *tail = value.split("_")
    return head + "".join(word.capitalize() for word in tail)


class APIModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)


class VideoProcessRequest(APIModel):
    youtube_url: HttpUrl
    youtube_video_id: str = Field(min_length=6, max_length=20, pattern=r"^[A-Za-z0-9_-]+$")
    title: str | None = Field(default=None, max_length=500)
    thumbnail_url: HttpUrl | None = None


class VideoProcessResponse(APIModel):
    video_id: str
    youtube_video_id: str
    indexed_status: str
    transcript_status: str


class VideoRefRequest(APIModel):
    youtube_video_id: str = Field(min_length=6, max_length=20, pattern=r"^[A-Za-z0-9_-]+$")


class ChatRequest(VideoRefRequest):
    youtube_url: HttpUrl
    question: str = Field(min_length=1, max_length=4000)
    chat_session_id: str | None = None
    title: str | None = Field(default=None, max_length=500)
    thumbnail_url: HttpUrl | None = None
    api_key: str | None = Field(default=None, min_length=20, max_length=500, exclude=True)

    @field_validator("question")
    @classmethod
    def question_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Question cannot be blank")
        return value


class Source(APIModel):
    text: str
    start_time_seconds: float
    end_time_seconds: float
    start_time_label: str
    end_time_label: str
    youtube_url: str


class ChatResponse(APIModel):
    chat_session_id: str
    answer: str
    sources: list[Source]


class SummaryRequest(VideoRefRequest):
    summary_type: Literal["short", "detailed", "key_points", "chapter_wise"] = "short"
    api_key: str | None = Field(default=None, exclude=True)


class SummaryResponse(APIModel):
    summary: str


class NotesRequest(VideoRefRequest):
    format: Literal["study_notes"] = "study_notes"
    api_key: str | None = Field(default=None, exclude=True)


class NotesResponse(APIModel):
    title: str
    content: str


class QuizRequest(VideoRefRequest):
    number_of_questions: int = Field(default=5, ge=1, le=20)
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    api_key: str | None = Field(default=None, exclude=True)


class QuizQuestion(APIModel):
    question: str
    options: list[str]
    correct_answer: str
    explanation: str


class QuizResponse(APIModel):
    questions: list[QuizQuestion]


class FlashcardsRequest(VideoRefRequest):
    number_of_cards: int = Field(default=10, ge=1, le=30)
    api_key: str | None = Field(default=None, exclude=True)


class Flashcard(APIModel):
    front: str
    back: str


class FlashcardsResponse(APIModel):
    flashcards: list[Flashcard]


class HistoryItem(APIModel):
    id: str
    type: str
    youtube_video_id: str
    title: str | None = None
    content: Any | None = None
    created_at: datetime


class HistoryResponse(APIModel):
    items: list[HistoryItem]


class VideoHistoryItem(APIModel):
    youtube_video_id: str
    title: str | None = None
    thumbnail_url: str | None = None
    indexed_status: str
    created_at: datetime


class VideoHistoryResponse(APIModel):
    videos: list[VideoHistoryItem]
