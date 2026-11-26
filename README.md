# NEXUS CLIP

**Turn long videos into short-form content worth sharing.**

NEXUS CLIP is an AI-assisted clipping platform for streamers, podcasters, and video creators. It is being built to analyze long-form content, discover compelling moments, generate short clips, and give creators control over the final edit.

> v0.1 is an engineering foundation, not a finished AI clipping product. It currently provides video upload/inspection primitives and a provider-neutral transcription interface.

## Product direction

1. Ingest creator-owned videos and authorized stream recordings.
2. Extract audio and inspect video metadata.
3. Transcribe speech with timestamps.
4. Discover candidate moments using context, hooks, storytelling, reactions, and visual signals.
5. Render vertical clips with captions and creator-controlled styling.
6. Let creators preview, edit, and export.

## v0.1 implemented

- FastAPI health endpoint.
- Chunked video upload with a configurable size limit.
- Extension validation and safe, collision-resistant storage names.
- FFprobe metadata extraction.
- FFmpeg audio extraction utility (16 kHz mono WAV).
- Provider-neutral transcription protocol.
- Unit tests for upload validation and storage paths.

## Requirements

- Python 3.10+
- FFmpeg and FFprobe installed and available on `PATH`.

## Setup

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

python -m pip install -e ".[dev]"
```

Copy `.env.example` to `.env` and adjust settings if needed. The application currently reads environment variables directly; load your `.env` values in your shell or deployment environment.

## Run

```bash
uvicorn nexus_clip.api:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API.

## Test

```bash
python -m unittest discover -s tests -v
```

## API

- `GET /health` — service health.
- `POST /api/v1/videos` — upload a supported video file as multipart form field `file`.

Uploads are stored locally in `./uploads` by default. Do not expose this development storage directly in production.

## Safety and privacy

Only upload videos you own or have permission to process. Production deployment must add authentication, per-user authorization, malware/content validation, quotas, retention controls, private object storage, and secure deletion before accepting customer uploads.

## Roadmap

- [x] Upload and validation foundation
- [x] Media metadata extraction
- [x] Audio extraction utility
- [x] Transcription interface
- [ ] Whisper transcription implementation
- [ ] Transcript-aware candidate moment detection
- [ ] Clip scoring and boundary refinement
- [ ] Vertical reframing and subtitle rendering
- [ ] Browser-based editing studio
- [ ] Creator accounts, billing, and usage limits
- [ ] Authorized livestream/VOD ingestion

## License

MIT
