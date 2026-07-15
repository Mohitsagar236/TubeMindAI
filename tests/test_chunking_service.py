from app.services.chunking_service import ChunkingService, TranscriptSegment


def test_chunking_preserves_text_order_and_timestamp_boundaries():
    service = ChunkingService(target_chars=13, overlap_segments=1)
    chunks = service.chunk(
        [
            TranscriptSegment(" first  ", 5, 2),
            TranscriptSegment("second", 7, 3),
            TranscriptSegment("third", 10, 4),
        ]
    )

    assert [chunk.index for chunk in chunks] == list(range(len(chunks)))
    assert chunks[0].text == "first second"
    assert chunks[0].start == 5
    assert chunks[0].end == 10
    assert chunks[1].text == "second third"
    assert chunks[1].start == 7
    assert chunks[1].end == 14


def test_chunking_discards_blank_segments_and_clamps_negative_times():
    chunks = ChunkingService().chunk(
        [
            TranscriptSegment("  ", 100, 10),
            TranscriptSegment(" useful text ", -5, -2),
        ]
    )
    assert len(chunks) == 1
    assert chunks[0].text == "useful text"
    assert chunks[0].start == 0
    assert chunks[0].end == 0


def test_chunking_empty_transcript_is_empty():
    assert ChunkingService().chunk([]) == []
