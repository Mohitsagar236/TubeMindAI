from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from ..exceptions import ServiceError, TranscriptUnavailableError, VideoNotFoundError
from ..models import TranscriptChunk, Video
from ..utils.youtube import validate_video_reference
from .chunking_service import ChunkingService
from .embedding_service import EmbeddingService
from .transcript_service import TranscriptService
from ..vector_store.chroma_client import ChromaStore


class VideoService:
    def __init__(self, transcript: TranscriptService, chunker: ChunkingService, embeddings: EmbeddingService, store: ChromaStore):
        self.transcript = transcript
        self.chunker = chunker
        self.embeddings = embeddings
        self.store = store

    async def process_video(
        self,
        db: Session,
        youtube_url: str,
        youtube_video_id: str,
        title: str | None = None,
        thumbnail_url: str | None = None,
        api_key: str | None = None,
    ) -> Video:
        validate_video_reference(youtube_url, youtube_video_id)
        video = db.scalar(select(Video).where(Video.youtube_video_id == youtube_video_id))
        if video and video.indexed_status == "completed" and video.transcript_status == "completed":
            return video
        if video is None:
            video = Video(youtube_video_id=youtube_video_id, youtube_url=youtube_url)
            db.add(video)
        video.youtube_url = youtube_url
        video.title = title or video.title
        video.thumbnail_url = thumbnail_url or video.thumbnail_url
        video.transcript_status = "processing"
        video.indexed_status = "processing"
        video.error_message = None
        db.commit()
        try:
            segments, language = await self.transcript.fetch(youtube_video_id)
            chunks = self.chunker.chunk(segments)
            if not chunks:
                raise TranscriptUnavailableError("Transcript is not available for this video.")
            embeddings = await self.embeddings.embed_documents([item.text for item in chunks], api_key)
            db.execute(delete(TranscriptChunk).where(TranscriptChunk.video_id == video.id))
            records = [
                TranscriptChunk(
                    video_id=video.id,
                    chunk_index=item.index,
                    text=item.text,
                    start_time_seconds=item.start,
                    end_time_seconds=item.end,
                    metadata_json={"youtubeVideoId": youtube_video_id},
                )
                for item in chunks
            ]
            db.add_all(records)
            db.flush()
            metadatas = [
                {
                    "youtubeVideoId": youtube_video_id,
                    "videoDbId": video.id,
                    "chunkId": record.id,
                    "chunkIndex": item.index,
                    "startTimeSeconds": float(item.start),
                    "endTimeSeconds": float(item.end),
                }
                for item, record in zip(chunks, records)
            ]
            await self.store.delete_video(youtube_video_id)
            await self.store.upsert([r.id for r in records], [c.text for c in chunks], embeddings, metadatas)
            video.language = language
            video.duration_seconds = int(max(item.end for item in chunks))
            video.transcript_status = "completed"
            video.indexed_status = "completed"
            db.commit()
            db.refresh(video)
            return video
        except Exception as exc:
            db.rollback()
            failed = db.scalar(select(Video).where(Video.youtube_video_id == youtube_video_id))
            if failed:
                failed.transcript_status = "failed" if isinstance(exc, TranscriptUnavailableError) else failed.transcript_status
                failed.indexed_status = "failed"
                failed.error_message = str(exc)[:2000]
                db.commit()
            if isinstance(exc, ServiceError):
                raise
            raise

    @staticmethod
    def get_completed(db: Session, youtube_video_id: str) -> Video:
        video = db.scalar(select(Video).where(Video.youtube_video_id == youtube_video_id))
        if not video or video.indexed_status != "completed":
            raise VideoNotFoundError("Video has not been processed yet.")
        return video

    @staticmethod
    def transcript_text(db: Session, video: Video, max_chars: int) -> str:
        chunks = db.scalars(
            select(TranscriptChunk).where(TranscriptChunk.video_id == video.id).order_by(TranscriptChunk.chunk_index)
        ).all()
        # De-overlap approximately by joining stored chunks; generation remains grounded even with repeated text.
        text = "\n".join(f"[{c.start_time_seconds:.0f}s] {c.text}" for c in chunks)
        return text[:max_chars]
