from dataclasses import dataclass

from ..utils.text_utils import clean_text


@dataclass(frozen=True)
class TranscriptSegment:
    text: str
    start: float
    duration: float


@dataclass(frozen=True)
class TranscriptChunkData:
    index: int
    text: str
    start: float
    end: float


class ChunkingService:
    """Groups complete timestamped segments without losing source boundaries."""

    def __init__(self, target_chars: int = 1100, overlap_segments: int = 2):
        self.target_chars = target_chars
        self.overlap_segments = overlap_segments

    def chunk(self, segments: list[TranscriptSegment]) -> list[TranscriptChunkData]:
        normalized = [
            TranscriptSegment(clean_text(s.text), max(0.0, float(s.start)), max(0.0, float(s.duration)))
            for s in segments
            if clean_text(s.text)
        ]
        if not normalized:
            return []
        groups: list[list[TranscriptSegment]] = []
        current: list[TranscriptSegment] = []
        length = 0
        for segment in normalized:
            if current and length + len(segment.text) + 1 > self.target_chars:
                groups.append(current)
                current = current[-self.overlap_segments :] if self.overlap_segments else []
                length = sum(len(item.text) + 1 for item in current)
            current.append(segment)
            length += len(segment.text) + 1
        if current and (not groups or current != groups[-1]):
            groups.append(current)
        return [
            TranscriptChunkData(
                index=index,
                text=" ".join(item.text for item in group),
                start=group[0].start,
                end=max(item.start + item.duration for item in group),
            )
            for index, group in enumerate(groups)
        ]
