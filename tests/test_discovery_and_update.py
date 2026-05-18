import json
import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.discovery import (
    discover_from_github_releases,
    discover_from_huggingface_models,
    discover_from_modelscope_models,
    discover_from_rss,
    discover_from_static_source,
    discover_from_therouter_catalog,
    normalize_raw_item,
)
from scripts.update_repo import append_news_items, render_newsletter_files, load_therouter_model_links
from scripts.run_daily_update import filter_fresh_candidates


class DiscoveryTests(unittest.TestCase):
    def test_normalize_raw_item_builds_entity_key_and_default_signals(self):
        item = normalize_raw_item(
            {
                "title": "Qwen3 Coder released",
                "url": "https://github.com/QwenLM/Qwen3-Coder/releases/tag/v1?utm_source=x",
                "summary": "Official release",
                "source_type": "github_release",
                "provider_id": "qwen",
                "model_id": "qwen3-coder",
                "version": "v1",
                "category": "model_release",
            }
        )
        self.assertEqual(item["canonical_url"], "https://github.com/QwenLM/Qwen3-Coder/releases/tag/v1")
        self.assertEqual(item["entity_key"], "qwen:qwen3-coder:v1")
        self.assertEqual(item["signals"]["chinese_ai_relevance"], 20)
        self.assertEqual(item["risks"], [])

    def test_discover_from_github_releases_maps_release_payloads(self):
        releases = [
            {
                "name": "v1.0",
                "tag_name": "v1.0",
                "html_url": "https://github.com/deepseek-ai/project/releases/tag/v1.0",
                "published_at": "2026-05-18T00:00:00Z",
                "body": "Release notes for DeepSeek model.",
            }
        ]
        items = discover_from_github_releases(
            releases,
            source={"id": "deepseek-github", "provider_id": "deepseek", "source_type": "github_release"},
            repo="deepseek-ai/project",
        )
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["category"], "open_source")
        self.assertEqual(items[0]["provider_id"], "deepseek")
        self.assertIn("deepseek-ai/project", items[0]["title"])

    def test_discover_from_huggingface_models_maps_model_payloads(self):
        models = [
            {
                "modelId": "Qwen/Qwen3-Embedding",
                "lastModified": "2026-05-18T00:00:00Z",
                "tags": ["text-embeddings-inference", "sentence-transformers"],
            }
        ]
        items = discover_from_huggingface_models(
            models,
            source={"id": "qwen-huggingface", "provider_id": "qwen", "source_type": "model_card"},
        )
        self.assertEqual(items[0]["model_id"], "qwen3-embedding")
        self.assertEqual(items[0]["category"], "model_update")
        self.assertEqual(items[0]["source_url"], "https://huggingface.co/Qwen/Qwen3-Embedding")

    def test_discover_from_modelscope_models_maps_flexible_payloads(self):
        models = [
            {
                "modelId": "Qwen3-Embedding",
                "owner": "qwen",
                "lastUpdated": "2026-05-18T00:00:00Z",
                "tags": ["embedding"],
                "description": "Qwen embedding model.",
            }
        ]
        items = discover_from_modelscope_models(models, source={"id": "modelscope-qwen", "provider_id": "qwen", "source_type": "model_card"})
        self.assertEqual(items[0]["model_id"], "qwen3-embedding")
        self.assertEqual(items[0]["source_url"], "https://modelscope.cn/models/qwen/Qwen3-Embedding")

    def test_discover_from_therouter_catalog_extracts_allowlisted_models(self):
        html = '<a href="/models/qwen--qwen3-235b/">Qwen</a><a href="/models/openai--gpt-5/">GPT</a>'
        items = discover_from_therouter_catalog(
            html,
            source={"id": "therouter", "provider_allowlist": ["qwen"], "source_type": "official_docs"},
        )
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["provider_id"], "qwen")
        self.assertEqual(items[0]["model_id"], "qwen3-235b")
        self.assertEqual(items[0]["category"], "api_update")

    def test_discover_from_rss_extracts_items(self):
        xml = """<?xml version='1.0'?><rss><channel><item><title>New GLM update</title><link>https://example.com/glm</link><description>GLM docs update</description><pubDate>Mon, 18 May 2026 00:00:00 GMT</pubDate></item></channel></rss>"""
        items = discover_from_rss(
            xml,
            source={"id": "media", "provider_id": "zhipu", "source_type": "credible_media"},
        )
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "New GLM update")
        self.assertEqual(items[0]["category"], "community")

    def test_discover_from_static_source_emits_source_health_candidate(self):
        item = discover_from_static_source(
            {"id": "qwen-official", "name": "Qwen Official", "provider_id": "qwen", "source_type": "official_release", "url": "https://qwenlm.github.io/"}
        )
        self.assertEqual(item["category"], "official_resource")
        self.assertEqual(item["source_url"], "https://qwenlm.github.io/")


class UpdateRepoTests(unittest.TestCase):
    def test_append_news_items_is_idempotent_and_preserves_existing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / "data"
            data.mkdir()
            news_path = data / "news.yaml"
            news_path.write_text("news:\n  - id: existing\n    date: '2026-05-17'\n    title: Old\n    summary: Old summary\n    category: community\n    source:\n      url: https://example.com/old\n      type: credible_media\n    verification:\n      status: verified\n", encoding="utf-8")
            items = [
                {"id": "new", "date": "2026-05-18", "title": "New", "summary": "New summary", "category": "model_update", "canonical_url": "https://example.com/new", "source_type": "official_release", "provider_id": "qwen", "score": 80, "decision": "stable_entry"},
                {"id": "existing", "date": "2026-05-17", "title": "Duplicate", "summary": "dup", "category": "community", "canonical_url": "https://example.com/old", "source_type": "credible_media"},
            ]
            written = append_news_items(root, items)
            self.assertEqual(written, 1)
            doc = yaml.safe_load(news_path.read_text(encoding="utf-8"))
            self.assertEqual([item["id"] for item in doc["news"]], ["new", "existing"])

    def test_render_newsletter_files_writes_latest_and_daily(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / "data"
            data.mkdir()
            (data / "therouter_model_links.yaml").write_text(
                "model_links:\n"
                "  - provider_id: qwen\n"
                "    model_id: qwen3-235b\n"
                "    title: Qwen3 235B\n"
                "    url: https://therouter.ai/models/qwen--qwen3-235b/\n"
                "  - provider_id: deepseek\n"
                "    model_id: deepseek-r1\n"
                "    title: DeepSeek R1\n"
                "    url: https://therouter.ai/models/deepseek--deepseek-r1/\n",
                encoding="utf-8",
            )
            items = [{"title": "New", "summary": "Summary", "category": "model_update", "canonical_url": "https://example.com/new", "provider_id": "qwen", "score": 80}]
            daily = render_newsletter_files(root, "2026-05-18", items)
            digest = daily.read_text(encoding="utf-8")
            self.assertTrue(daily.exists())
            self.assertTrue((root / "newsletters" / "latest.md").exists())
            self.assertIn("Accepted updates: 1", digest)
            self.assertIn("## TheRouter model pages", digest)
            self.assertIn("https://therouter.ai/models/qwen--qwen3-235b/", digest)
            self.assertNotIn("https://therouter.ai/models/deepseek--deepseek-r1/", digest)
            self.assertEqual(len(load_therouter_model_links(root)), 2)

    def test_filter_fresh_candidates_drops_stale_items(self):
        items = [
            {"id": "fresh", "published_at": "2026-05-18T00:00:00Z"},
            {"id": "stale", "published_at": "2026-04-01T00:00:00Z"},
            {"id": "future", "published_at": "2026-05-19T00:00:00Z"},
        ]
        self.assertEqual([item["id"] for item in filter_fresh_candidates(items, "2026-05-18", 7)], ["fresh"])


if __name__ == "__main__":
    unittest.main()
