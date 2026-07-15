import pytest

from app.exceptions import InvalidVideoError
from app.utils.youtube import extract_youtube_video_id, validate_video_reference


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://www.youtube.com/watch?v=abc_123-XYZ", "abc_123-XYZ"),
        ("https://youtu.be/abc_123-XYZ?t=5", "abc_123-XYZ"),
        ("https://www.youtube.com/shorts/abc_123-XYZ", "abc_123-XYZ"),
    ],
)
def test_extract_supported_urls(url, expected):
    assert extract_youtube_video_id(url) == expected


def test_rejects_non_youtube_and_mismatched_ids():
    with pytest.raises(InvalidVideoError):
        validate_video_reference("https://youtube.com.evil.example/watch?v=safe123", "safe123")
    with pytest.raises(InvalidVideoError):
        validate_video_reference("https://youtube.com/watch?v=one123", "two123")
