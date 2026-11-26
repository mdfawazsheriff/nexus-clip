from pathlib import Path
import unittest

from nexus_clip.config import Settings
from nexus_clip.storage import (
    UploadValidationError, build_storage_path, safe_filename, validate_upload
)


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings(
            upload_dir=Path("uploads"),
            max_upload_bytes=10 * 1024 * 1024,
            allowed_extensions=frozenset({".mp4", ".mov"}),
        )

    def test_accepts_allowed_video(self):
        validate_upload("stream.mp4", 1024, self.settings)

    def test_rejects_disallowed_extension(self):
        with self.assertRaises(UploadValidationError):
            validate_upload("payload.exe", 1024, self.settings)

    def test_rejects_empty_file(self):
        with self.assertRaises(UploadValidationError):
            validate_upload("empty.mp4", 0, self.settings)

    def test_rejects_oversized_file(self):
        with self.assertRaises(UploadValidationError):
            validate_upload("large.mp4", 11 * 1024 * 1024, self.settings)

    def test_filename_is_sanitized(self):
        self.assertEqual(safe_filename("../../my video!.mp4"), "my_video_.mp4")

    def test_storage_path_is_unique(self):
        first = build_storage_path("clip.mp4", self.settings)
        second = build_storage_path("clip.mp4", self.settings)
        self.assertNotEqual(first, second)
        self.assertEqual(first.parent, self.settings.upload_dir)


if __name__ == "__main__":
    unittest.main()
