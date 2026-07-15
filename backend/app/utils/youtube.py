from urllib.parse import parse_qs, urlparse

from ..exceptions import InvalidVideoError


def extract_youtube_video_id(url: str) -> str | None:
    parsed = urlparse(str(url))
    host = (parsed.hostname or "").lower()
    if host in {"youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com"}:
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]
        if parsed.path.startswith(("/shorts/", "/embed/", "/live/")):
            return parsed.path.split("/")[2]
    if host in {"youtu.be", "www.youtu.be"}:
        return parsed.path.strip("/").split("/")[0] or None
    return None


def validate_video_reference(url: str, claimed_id: str) -> None:
    actual_id = extract_youtube_video_id(url)
    if not actual_id:
        raise InvalidVideoError("Only valid YouTube video URLs can be processed.")
    if actual_id != claimed_id:
        raise InvalidVideoError("youtubeVideoId does not match the supplied YouTube URL.")


def timestamp_url(video_id: str, seconds: float) -> str:
    return f"https://www.youtube.com/watch?v={video_id}&t={max(0, int(seconds))}s"
