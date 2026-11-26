import unittest

from nexus_clip.schemas import ClipCandidate, TranscriptSegment, VideoMetadata


class SchemaTests(unittest.TestCase):
    def test_transcript_segment_keeps_timestamps(self):
        segment = TranscriptSegment(1.25, 3.5, "That was incredible!")
        self.assertEqual(segment.start_seconds, 1.25)
        self.assertEqual(segment.end_seconds, 3.5)

    def test_clip_candidate_defaults_to_suggested(self):
        candidate = ClipCandidate(
            start_seconds=12.0,
            end_seconds=35.0,
            title="Unexpected comeback",
            rationale="Strong emotional payoff",
            score=0.87,
        )
        self.assertEqual(candidate.status, "suggested")
        self.assertGreater(candidate.score, 0.8)

    def test_video_metadata_can_represent_unprobed_media(self):
        metadata = VideoMetadata("sample.mp4", 2048, "video/mp4")
        self.assertIsNone(metadata.duration_seconds)
        self.assertIsNone(metadata.width)


if __name__ == "__main__":
    unittest.main()
