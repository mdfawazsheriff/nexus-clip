import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from nexus_clip.api import app
from nexus_clip.schemas import VideoMetadata


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        os.environ["NEXUS_CLIP_UPLOAD_DIR"] = self.temp_dir.name
        os.environ["NEXUS_CLIP_MAX_UPLOAD_MB"] = "1"
        os.environ["NEXUS_CLIP_ALLOWED_EXTENSIONS"] = ".mp4"
        self.client = TestClient(app)

    def tearDown(self):
        self.temp_dir.cleanup()
        for key in (
            "NEXUS_CLIP_UPLOAD_DIR",
            "NEXUS_CLIP_MAX_UPLOAD_MB",
            "NEXUS_CLIP_ALLOWED_EXTENSIONS",
        ):
            os.environ.pop(key, None)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_rejects_unsupported_upload_type(self):
        response = self.client.post(
            "/api/v1/videos",
            files={"file": ("script.exe", b"not a video", "application/octet-stream")},
        )
        self.assertEqual(response.status_code, 415)

    @patch("nexus_clip.api.probe_video")
    def test_accepts_valid_upload_and_returns_metadata(self, mock_probe):
        mock_probe.return_value = VideoMetadata(
            filename="sample.mp4",
            size_bytes=4,
            content_type="video/mp4",
            duration_seconds=12.5,
            width=1280,
            height=720,
            video_codec="h264",
            audio_codec="aac",
        )
        response = self.client.post(
            "/api/v1/videos",
            files={"file": ("sample.mp4", b"data", "video/mp4")},
        )
        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertEqual(body["metadata"]["duration_seconds"], 12.5)
        self.assertEqual(body["metadata"]["width"], 1280)
        self.assertEqual(body["processing_status"], "uploaded")
        mock_probe.assert_called_once()

    def test_rejects_upload_over_size_limit(self):
        response = self.client.post(
            "/api/v1/videos",
            files={"file": ("large.mp4", b"x" * (1024 * 1024 + 1), "video/mp4")},
        )
        self.assertEqual(response.status_code, 413)
        self.assertEqual(list(Path(self.temp_dir.name).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
