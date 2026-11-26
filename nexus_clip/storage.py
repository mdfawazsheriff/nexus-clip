from pathlib import Path
from uuid import uuid4
import re

from nexus_clip.config import Settings


class UploadValidationError(ValueError):
    pass


def safe_filename(filename: str) -> str:
    """Strip path components and unsafe characters from a client-supplied name."""
    basename = Path(filename).name
    cleaned = re.sub(r"[^A-Za-z0-9._-]", "_", basename).strip("._")
    return cleaned or "uploaded_video"


def validate_upload(filename: str, size_bytes: int, settings: Settings) -> None:
    suffix = Path(filename).suffix.lower()
    if suffix not in settings.allowed_extensions:
        raise UploadValidationError(
            f"Unsupported file extension '{suffix}'. Allowed: "
            f"{', '.join(sorted(settings.allowed_extensions))}"
        )
    if size_bytes <= 0:
        raise UploadValidationError("The uploaded file is empty.")
    if size_bytes > settings.max_upload_bytes:
        raise UploadValidationError(
            f"File exceeds the {settings.max_upload_bytes // (1024 * 1024)} MB limit."
        )


def build_storage_path(filename: str, settings: Settings) -> Path:
    """Create a unique destination to avoid collisions and path traversal."""
    safe_name = safe_filename(filename)
    return settings.upload_dir / f"{uuid4().hex}_{safe_name}"
