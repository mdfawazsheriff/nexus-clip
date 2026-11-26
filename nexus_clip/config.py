from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    upload_dir: Path
    max_upload_bytes: int
    allowed_extensions: frozenset[str]


def get_settings() -> Settings:
    max_mb = int(os.getenv("NEXUS_CLIP_MAX_UPLOAD_MB", "500"))
    extensions = os.getenv(
        "NEXUS_CLIP_ALLOWED_EXTENSIONS", ".mp4,.mov,.mkv,.webm"
    )
    return Settings(
        upload_dir=Path(os.getenv("NEXUS_CLIP_UPLOAD_DIR", "./uploads")),
        max_upload_bytes=max_mb * 1024 * 1024,
        allowed_extensions=frozenset(
            item.strip().lower() for item in extensions.split(",") if item.strip()
        ),
    )
