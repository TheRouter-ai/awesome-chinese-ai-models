import unittest
from pathlib import Path
import tempfile

from scripts.maintainer import (
    canonicalize_url,
    dedupe_candidates,
    score_candidate,
    render_daily_digest,
    load_source_catalog,
)


class MaintainerTests(unittest.TestCase):
    def test_canonicalize_url_removes_tracking_and_normalizes_github(self):
        raw = "https://github.com/QwenLM/Qwen3?utm_source=x#readme"
        self.assertEqual(canonicalize_url(raw), "https://github.com/QwenLM/Qwen3")

    def test_score_candidate_rewards_official_chinese_ai_model_release(self):
        candidate = {
            "title": "Qwen releases a new coding model",
            "summary": "Official release for a Chinese coding model.",
            "source_type": "official_release",
            "category": "model_release",
            "provider_id": "qwen",
            "model_id": "qwen-coder",
            "source_url": "https://qwenlm.github.io/blog/qwen-coder/",
            "published_at": "2026-05-18",
            "signals": {"chinese_ai_relevance": 20, "awesome_value": 18, "freshness": 10, "verifiability": 10, "category_clarity": 10, "community_signal": 5},
            "risks": [],
        }
        result = score_candidate(candidate)
        self.assertGreaterEqual(result["score"], 65)
        self.assertEqual(result["decision"], "stable_entry")

    def test_dedupe_candidates_prefers_official_source_over_media_duplicate(self):
        candidates = [
            {
                "id": "media-1",
                "title": "Qwen releases model",
                "canonical_url": "https://example.com/news/qwen",
                "entity_key": "qwen:qwen-coder:v1",
                "source_type": "credible_media",
            },
            {
                "id": "official-1",
                "title": "Qwen releases model",
                "canonical_url": "https://qwenlm.github.io/blog/qwen-coder/",
                "entity_key": "qwen:qwen-coder:v1",
                "source_type": "official_release",
            },
        ]
        accepted, duplicates = dedupe_candidates(candidates, seen_urls=set(), seen_entities=set())
        self.assertEqual([item["id"] for item in accepted], ["official-1"])
        self.assertEqual(duplicates[0]["id"], "media-1")
        self.assertEqual(duplicates[0]["duplicate_reason"], "lower_priority_same_entity")

    def test_render_daily_digest_writes_ten_plus_updates_with_sources(self):
        candidates = []
        for idx in range(12):
            candidates.append({
                "title": f"Update {idx}",
                "summary": f"Summary {idx}",
                "category": "model_update",
                "canonical_url": f"https://example.com/{idx}",
                "provider_id": "qwen",
                "score": 70 - idx,
            })
        digest = render_daily_digest("2026-05-18", candidates)
        self.assertIn("# Chinese AI Models Digest — 2026-05-18", digest)
        self.assertIn("Accepted updates: 12", digest)
        self.assertIn("[Update 0](https://example.com/0)", digest)
        self.assertIn("[Update 11](https://example.com/11)", digest)

    def test_load_source_catalog_rejects_missing_required_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.yaml"
            path.write_text("sources:\n  - id: qwen\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_source_catalog(path)


if __name__ == "__main__":
    unittest.main()
