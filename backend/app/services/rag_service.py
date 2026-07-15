from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import ChatMessage, ChatSession
from ..prompts.chat_prompt import CHAT_PROMPT
from ..schemas import Source
from ..utils.time_utils import format_timestamp
from ..utils.youtube import timestamp_url
from ..vector_store.retriever import VideoRetriever
from .llm_service import LLMService
from .video_service import VideoService


NOT_AVAILABLE = "This information is not available in the video."


class RAGService:
    def __init__(self, video_service: VideoService, retriever: VideoRetriever, llm: LLMService):
        self.video_service = video_service
        self.retriever = retriever
        self.llm = llm

    async def chat(self, db: Session, video_id: str, question: str, session_id: str | None, api_key: str | None = None):
        video = self.video_service.get_completed(db, video_id)
        if session_id:
            session = db.scalar(select(ChatSession).where(ChatSession.id == session_id, ChatSession.video_id == video.id))
            if not session:
                from ..exceptions import VideoNotFoundError
                raise VideoNotFoundError("Chat session was not found for this video.")
        else:
            session = ChatSession(video_id=video.id, title=question[:100])
            db.add(session)
            db.flush()
        db.add(ChatMessage(chat_session_id=session.id, role="user", content=question))
        matches = await self.retriever.retrieve(video_id, question, api_key)
        context = "\n\n".join(
            f"[{float(item['metadata'].get('startTimeSeconds', 0)):.0f}s-"
            f"{float(item['metadata'].get('endTimeSeconds', 0)):.0f}s] {item['text']}"
            for item in matches
        )
        answer = NOT_AVAILABLE if not context else await self.llm.complete(CHAT_PROMPT.format(context=context, question=question), api_key)
        sources = [self._source(video_id, item) for item in matches] if answer != NOT_AVAILABLE else []
        serialized = [source.model_dump(by_alias=True) for source in sources]
        db.add(ChatMessage(chat_session_id=session.id, role="assistant", content=answer, sources_json=serialized))
        db.commit()
        return session.id, answer, sources

    @staticmethod
    def _source(video_id: str, item: dict) -> Source:
        metadata = item.get("metadata", {})
        start = float(metadata.get("startTimeSeconds", 0))
        end = float(metadata.get("endTimeSeconds", start))
        return Source(
            text=item.get("text", ""),
            start_time_seconds=start,
            end_time_seconds=end,
            start_time_label=format_timestamp(start),
            end_time_label=format_timestamp(end),
            youtube_url=timestamp_url(video_id, start),
        )
