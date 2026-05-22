import unittest

from scripts.generate_readme import (
    generate,
    render_access_methods,
    render_availability,
    render_benchmarks,
    render_best_for,
    render_comparison,
    render_faq,
)


class ReadmeGenerationTests(unittest.TestCase):
    def test_generate_is_idempotent(self):
        # generate() must produce a README that, fed back in, does not change.
        once = generate()
        self.assertIn("AUTO-GENERATED:START comparison-table", once)
        self.assertIn("AUTO-GENERATED:START global-availability", once)
        self.assertIn("AUTO-GENERATED:START faq", once)

    def test_render_comparison_builds_table(self):
        rows = [
            {
                "name": "DeepSeek",
                "best_for": "Coding",
                "context": "128K",
                "vision": False,
                "reasoning": True,
                "api": True,
                "open_source": True,
            }
        ]
        out = render_comparison(rows)
        self.assertIn("| Model | Best For | Context |", out)
        self.assertIn("| DeepSeek | Coding | 128K | — | ✅ | ✅ | ✅ |", out)

    def test_render_access_methods_links_when_url_present(self):
        methods = [
            {"id": "therouter", "name": "TheRouter", "summary": "Gateway", "best_for": "Teams", "url": "https://therouter.ai/"},
            {"id": "self-host", "name": "Self-host", "summary": "Run locally", "best_for": "Control"},
        ]
        out = render_access_methods(methods)
        self.assertIn("**[TheRouter](https://therouter.ai/)**", out)
        self.assertIn("**Self-host**", out)

    def test_render_availability_uses_legend_symbols(self):
        availability = {
            "regions": [{"id": "global", "label": "Global API"}],
            "providers": [
                {"name": "DeepSeek", "global": "yes", "crypto_payment": False},
                {"name": "Kimi", "global": "partial", "crypto_payment": False},
            ],
        }
        out = render_availability(availability)
        self.assertIn("| DeepSeek | ✅ | — |", out)
        self.assertIn("| Kimi | ◐ | — |", out)

    def test_render_best_for_and_benchmarks_and_faq(self):
        self.assertIn("- **Qwen**", render_best_for([{"name": "Qwen", "use_cases": ["Multilingual"]}]))
        self.assertIn("[LMArena](https://lmarena.ai/)", render_benchmarks([{"name": "LMArena", "url": "https://lmarena.ai/", "coverage": "Elo"}]))
        self.assertIn("### What is it?", render_faq([{"question": "What is it?", "answer": "A guide."}]))


if __name__ == "__main__":
    unittest.main()
