import pytest

from app.exceptions import InvalidVideoError
from app.utils.youtube import (
    extract_youtube_video_id,
    timestamp_url,
    validate_video_reference,
)


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://youtu.be/dQw4w9WgXcQ?t=42", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/shorts/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://m.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://example.com/watch?v=dQw4w9WgXcQ", None),
        ("not a url", None),
    ],
)
def test_extract_youtube_video_id(url, expected):
    assert extract_youtube_video_id(url) == expected


def test_video_reference_rejects_mismatched_id():
    with pytest.raises(InvalidVideoError, match="does not match"):
        validate_video_reference(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "aaaaaaaaaaa"
        )


def test_video_reference_rejects_non_youtube_url():
    with pytest.raises(InvalidVideoError, match="valid YouTube"):
        validate_video_reference("https://example.com/video", "dQw4w9WgXcQ")


def test_timestamp_url_clamps_and_truncates_seconds():
    assert timestamp_url("dQw4w9WgXcQ", 252.9).endswith("&t=252s")
    assert timestamp_url("dQw4w9WgXcQ", -4).endswith("&t=0s")

