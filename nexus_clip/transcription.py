from pathlib import Path
from typing import Protocol

from nexus_clip.schemas import TranscriptSegment


class Transcriber(Protocol):
    """Provider-neutral interface for timestamped speech transcription."""

    def transcribe(self, audio_path: Path) -> list[TranscriptSegment]:
        ...


class NotConfiguredTranscriber:
    """Explicit placeholder until a Whisper provider is configured."""

    def transcribe(self, audio_path: Path) -> list[TranscriptSegment]:
        raise NotImplementedError(
            "Transcription provider is not configured yet. "
            "The interface is ready for faster-whisper or a hosted API."
        )
