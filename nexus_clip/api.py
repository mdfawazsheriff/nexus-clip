from pathlib import Path
import os

from fastapi import FastAPI, File, HTTPException, UploadFile

from nexus_clip.config import get_settings
from nexus_clip.media import MediaToolError, probe_video
from nexus_clip.storage import (
    UploadValidationError, build_storage_path, validate_upload
)

app = FastAPI(
    title="NEXUS CLIP API",
    version="0.1.0",
    description="Upload and inspect creator-owned video for AI-assisted clipping.",
)

CHUNK_SIZE = 1024 * 1024


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "nexus-clip"}


@app.post("/api/v1/videos", status_code=201)
async def upload_video(file: UploadFile = File(...)) -> dict:
    settings = get_settings()
    filename = file.filename or "uploaded_video"
    suffix = Path(filename).suffix.lower()

    # Validate the extension before writing any data.
    if suffix not in settings.allowed_extensions:
        raise HTTPException(status_code=415, detail="Unsupported video file type.")

    destination = build_storage_path(filename, settings)
    destination.parent.mkdir(parents=True, exist_ok=True)
    total = 0

    try:
        with destination.open("wb") as output:
            while chunk := await file.read(CHUNK_SIZE):
                total += len(chunk)
                if total > settings.max_upload_bytes:
                    raise HTTPException(status_code=413, detail="Upload exceeds size limit.")
                output.write(chunk)

        validate_upload(filename, total, settings)
        metadata = probe_video(destination, file.content_type)
        return {
            "video_id": destination.stem.split("_", 1)[0],
            "stored_filename": destination.name,
            "metadata": {
                "filename": metadata.filename,
                "size_bytes": metadata.size_bytes,
                "content_type": metadata.content_type,
                "duration_seconds": metadata.duration_seconds,
                "width": metadata.width,
                "height": metadata.height,
                "video_codec": metadata.video_codec,
                "audio_codec": metadata.audio_codec,
            },
            "processing_status": "uploaded",
        }
    except HTTPException:
        destination.unlink(missing_ok=True)
        raise
    except (UploadValidationError, MediaToolError) as exc:
        destination.unlink(missing_ok=True)
        status = 422 if isinstance(exc, UploadValidationError) else 503
        raise HTTPException(status_code=status, detail=str(exc)) from exc
    finally:
        await file.close()
