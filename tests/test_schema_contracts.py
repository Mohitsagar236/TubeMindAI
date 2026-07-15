import pytest
from pydantic import ValidationError

from app.schemas import ChatRequest, ChatResponse, QuizRequest, Source, VideoProcessRequest


VIDEO_ID = "dQw4w9WgXcQ"
VIDEO_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"


def test_requests_accept_documented_camel_case_contract():
    request = VideoProcessRequest.model_validate(
        {
            "youtubeUrl": VIDEO_URL,
            "youtubeVideoId": VIDEO_ID,
            "thumbnailUrl": f"https://img.youtube.com/vi/{VIDEO_ID}/hqdefault.jpg",
        }
    )
    assert request.youtube_video_id == VIDEO_ID
    assert request.model_dump(by_alias=True)["youtubeVideoId"] == VIDEO_ID


def test_chat_question_is_trimmed_and_secret_is_not_serialized():
    request = ChatRequest.model_validate(
        {
            "youtubeUrl": VIDEO_URL,
            "youtubeVideoId": VIDEO_ID,
            "question": "  What is the main topic?  ",
            "apiKey": "sk-test-secret-value-1234567890",
        }
    )
    assert request.question == "What is the main topic?"
    assert "apiKey" not in request.model_dump(by_alias=True)
    assert "sk-test" not in repr(request.model_dump(by_alias=True))


def test_chat_rejects_blank_question():
    with pytest.raises(ValidationError):
        ChatRequest.model_validate(
            {"youtubeUrl": VIDEO_URL, "youtubeVideoId": VIDEO_ID, "question": "   "}
        )


def test_quiz_bounds_match_public_contract():
    with pytest.raises(ValidationError):
        QuizRequest(youtube_video_id=VIDEO_ID, number_of_questions=0)
    with pytest.raises(ValidationError):
        QuizRequest(youtube_video_id=VIDEO_ID, number_of_questions=21)


def test_chat_response_serializes_timestamp_source_as_camel_case():
    response = ChatResponse(
        chat_session_id="session-1",
        answer="The video explains retrieval augmented generation.",
        sources=[
            Source(
                text="Relevant transcript text",
                start_time_seconds=252,
                end_time_seconds=318,
                start_time_label="04:12",
                end_time_label="05:18",
                youtube_url=f"{VIDEO_URL}&t=252s",
            )
        ],
    )
    payload = response.model_dump(by_alias=True)
    assert payload["chatSessionId"] == "session-1"
    assert payload["sources"][0]["startTimeSeconds"] == 252
    assert payload["sources"][0]["youtubeUrl"].endswith("&t=252s")
