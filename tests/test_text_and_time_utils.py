import pytest

from app.utils.text_utils import clean_text, parse_json_object
from app.utils.time_utils import format_timestamp


@pytest.mark.parametrize(
    ("seconds", "label"),
    [(None, "00:00"), (-1, "00:00"), (65.9, "01:05"), (3661, "01:01:01")],
)
def test_format_timestamp(seconds, label):
    assert format_timestamp(seconds) == label


def test_clean_text_normalizes_whitespace():
    assert clean_text("  hello\n\tTubeMind   AI ") == "hello TubeMind AI"


@pytest.mark.parametrize(
    "value",
    [
        '{"questions": []}',
        '```json\n{"questions": []}\n```',
        'Model preamble: {"questions": []} trailing text',
    ],
)
def test_parse_json_object_accepts_common_model_output(value):
    assert parse_json_object(value) == {"questions": []}


@pytest.mark.parametrize("value", ["not json", "[]", "```json\n[]\n```"])
def test_parse_json_object_rejects_non_objects(value):
    with pytest.raises(ValueError):
        parse_json_object(value)

