from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class VideoMetadata:
    filename: str
    size_bytes: int
    content_type: str | None
    duration_seconds: float | None = None
    width: int | None = None
    height: int | None = None
    video_codec: str | None = None
    audio_codec: str | None = None


@dataclass(frozen=True)
class TranscriptSegment:
    start_seconds: float
    end_seconds: float
    text: str


@dataclass(frozen=True)
class ClipCandidate:
    start_seconds: float
    end_seconds: float
    title: str
    rationale: str
    score: float
    status: Literal["suggested", "approved", "rejected"] = "suggested"
