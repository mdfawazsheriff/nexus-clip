from pathlib import Path
import json
import shutil
import subprocess

from nexus_clip.schemas import VideoMetadata


class MediaToolError(RuntimeError):
    """Raised when FFmpeg/FFprobe is unavailable or media processing fails."""


def _require_binary(name: str) -> str:
    binary = shutil.which(name)
    if not binary:
        raise MediaToolError(
            f"{name} was not found. Install FFmpeg and ensure it is on PATH."
        )
    return binary


def probe_video(path: Path, content_type: str | None = None) -> VideoMetadata:
    """Read media metadata using ffprobe without loading the whole video into memory."""
    ffprobe = _require_binary("ffprobe")
    command = [
        ffprobe, "-v", "error", "-show_format", "-show_streams",
        "-of", "json", str(path)
    ]
    try:
        completed = subprocess.run(
            command, check=True, capture_output=True, text=True, timeout=30
        )
        payload = json.loads(completed.stdout)
    except (subprocess.SubprocessError, json.JSONDecodeError) as exc:
        raise MediaToolError(f"Could not inspect uploaded video: {exc}") from exc

    streams = payload.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = next((s for s in streams if s.get("codec_type") == "audio"), {})
    duration = payload.get("format", {}).get("duration")
    return VideoMetadata(
        filename=path.name,
        size_bytes=path.stat().st_size,
        content_type=content_type,
        duration_seconds=float(duration) if duration is not None else None,
        width=video.get("width"),
        height=video.get("height"),
        video_codec=video.get("codec_name"),
        audio_codec=audio.get("codec_name"),
    )


def extract_audio(video_path: Path, output_path: Path) -> Path:
    """Extract mono 16 kHz WAV audio for downstream transcription."""
    ffmpeg = _require_binary("ffmpeg")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        ffmpeg, "-y", "-i", str(video_path), "-vn",
        "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(output_path)
    ]
    try:
        subprocess.run(
            command, check=True, capture_output=True, text=True, timeout=600
        )
    except subprocess.SubprocessError as exc:
        raise MediaToolError(f"Audio extraction failed: {exc}") from exc
    return output_path
