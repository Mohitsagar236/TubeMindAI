import asyncio

from ..exceptions import ExternalServiceError, TranscriptUnavailableError
from .chunking_service import TranscriptSegment


class TranscriptService:
    async def fetch(self, video_id: str, languages: list[str] | None = None) -> tuple[list[TranscriptSegment], str | None]:
        return await asyncio.to_thread(self._fetch_sync, video_id, languages or ["en"])

    @staticmethod
    def _fetch_sync(video_id: str, languages: list[str]) -> tuple[list[TranscriptSegment], str | None]:
        try:
            from youtube_transcript_api import YouTubeTranscriptApi

            # youtube-transcript-api 1.x uses an instance; older releases expose a class method.
            if hasattr(YouTubeTranscriptApi, "fetch"):
                api = YouTubeTranscriptApi()
                try:
                    result = api.fetch(video_id, languages=languages)
                except Exception as preferred_error:
                    if "notranscript" not in preferred_error.__class__.__name__.lower():
                        raise
                    available = list(api.list(video_id))
                    if not available:
                        raise
                    result = available[0].fetch()
            else:
                try:
                    result = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
                    fallback_language = None
                except Exception as preferred_error:
                    if "notranscript" not in preferred_error.__class__.__name__.lower():
                        raise
                    available = list(YouTubeTranscriptApi.list_transcripts(video_id))
                    if not available:
                        raise
                    transcript = available[0]
                    result = transcript.fetch()
                    fallback_language = getattr(transcript, "language_code", None)
            raw = result.to_raw_data() if hasattr(result, "to_raw_data") else result
            language = getattr(result, "language_code", None) or locals().get("fallback_language")
            segments = [
                TranscriptSegment(
                    text=item.text if hasattr(item, "text") else item["text"],
                    start=item.start if hasattr(item, "start") else item.get("start", 0),
                    duration=item.duration if hasattr(item, "duration") else item.get("duration", 0),
                )
                for item in raw
            ]
            if not segments:
                raise TranscriptUnavailableError("Transcript is not available for this video.")
            return segments, language
        except TranscriptUnavailableError:
            raise
        except ImportError as exc:
            raise ExternalServiceError("Transcript support is not installed on the backend.") from exc
        except Exception as exc:
            name = exc.__class__.__name__.lower()
            unavailable = ("disabled", "notranscript", "unavailable", "notranscripts")
            if any(token in name for token in unavailable):
                raise TranscriptUnavailableError("Transcript is not available for this video.") from exc
            raise ExternalServiceError("YouTube transcript service is temporarily unavailable.") from exc
