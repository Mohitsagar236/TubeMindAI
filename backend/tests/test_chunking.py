from app.services.chunking_service import ChunkingService, TranscriptSegment


def test_chunks_preserve_timestamp_boundaries_and_overlap():
    segments = [
        TranscriptSegment("one two", 0, 2),
        TranscriptSegment("three four", 2, 2),
        TranscriptSegment("five six", 4, 3),
    ]
    chunks = ChunkingService(target_chars=12, overlap_segments=1).chunk(segments)
    assert len(chunks) >= 2
    assert chunks[0].start == 0
    assert chunks[-1].end == 7
    assert "three four" in chunks[0].text or "three four" in chunks[1].text


def test_empty_segments_are_ignored():
    assert ChunkingService().chunk([TranscriptSegment("   ", 0, 1)]) == []
