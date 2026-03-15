"""Tests for scan_revenue_skills module."""

import json
import os
import tempfile
import textwrap
import unittest

# Allow import from parent directory
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scan_revenue_skills import (
    classify_skill,
    format_skill,
    generate_report,
    infer_level,
    is_polymarket,
    monetization_paths,
    parse_frontmatter,
    read_skill,
    scan_skills,
)


class TestParserFrontmatter(unittest.TestCase):
    """Tests for the lightweight YAML-frontmatter parser."""

    def test_basic_frontmatter(self):
        text = textwrap.dedent("""\
            ---
            name: my-skill
            description: A useful skill
            version: 1.0.0
            ---
            # My Skill
        """)
        result = parse_frontmatter(text)
        self.assertEqual(result["name"], "my-skill")
        self.assertEqual(result["description"], "A useful skill")
        self.assertEqual(result["version"], "1.0.0")

    def test_no_frontmatter(self):
        result = parse_frontmatter("# Just a heading\nSome text")
        self.assertEqual(result["name"], "")
        self.assertEqual(result["description"], "")

    def test_empty_input(self):
        result = parse_frontmatter("")
        self.assertEqual(result["name"], "")

    def test_none_input(self):
        result = parse_frontmatter(None)
        self.assertEqual(result["name"], "")

    def test_quoted_values(self):
        text = '---\nname: "quoted-name"\ndescription: \'single\'\n---\n'
        result = parse_frontmatter(text)
        self.assertEqual(result["name"], "quoted-name")
        self.assertEqual(result["description"], "single")


class TestPolymarketDetection(unittest.TestCase):
    """Polymarket / prediction-market skills must be excluded."""

    def test_polymarket_in_name(self):
        self.assertTrue(is_polymarket("polymarket-trader", "", ""))

    def test_polymarket_in_description(self):
        self.assertTrue(is_polymarket("trader", "Trade on Polymarket", ""))

    def test_polymarket_in_path(self):
        self.assertTrue(is_polymarket("", "", "/skills/user/polymarket-bot"))

    def test_prediction_market(self):
        self.assertTrue(is_polymarket("prediction-market-bot", "", ""))

    def test_non_polymarket(self):
        self.assertFalse(is_polymarket("crypto-trader", "Trade BTC", "/skills/u/x"))

    def test_case_insensitive(self):
        self.assertTrue(is_polymarket("POLYMARKET", "", ""))

    def test_empty_strings(self):
        self.assertFalse(is_polymarket("", "", ""))


class TestInferLevel(unittest.TestCase):
    """Skill-level inference heuristic."""

    def test_advanced_keywords(self):
        self.assertEqual(infer_level("Uses GARCH volatility forecasting"), "advanced")
        self.assertEqual(infer_level("ML model for predictions"), "advanced")

    def test_intermediate_keywords(self):
        self.assertEqual(infer_level("API integration webhook"), "intermediate")
        self.assertEqual(infer_level("Deploy with Docker"), "intermediate")

    def test_basic_default(self):
        self.assertEqual(infer_level("A simple note-taking skill"), "basic")

    def test_empty(self):
        self.assertEqual(infer_level(""), "basic")
        self.assertEqual(infer_level(None), "basic")


class TestClassifySkill(unittest.TestCase):
    """Domain classification based on keywords."""

    def test_crypto_trading(self):
        info = {"name": "crypto-levels", "description": "Analyze cryptocurrency", "displayName": "", "path": ""}
        domains = classify_skill(info)
        self.assertIn("crypto trading", domains)

    def test_stock_trading(self):
        info = {"name": "idx-scalper", "description": "scalping for IDX stocks", "displayName": "", "path": ""}
        domains = classify_skill(info)
        self.assertIn("stock trading", domains)

    def test_options_trading(self):
        info = {"name": "options-engine", "description": "options spread analysis", "displayName": "", "path": ""}
        domains = classify_skill(info)
        self.assertIn("options trading", domains)

    def test_automation(self):
        info = {"name": "workspace-automation", "description": "Automate workflows", "displayName": "", "path": ""}
        domains = classify_skill(info)
        self.assertIn("automation services", domains)

    def test_no_match(self):
        info = {"name": "random-notes", "description": "personal journal", "displayName": "", "path": ""}
        domains = classify_skill(info)
        self.assertEqual(domains, [])

    def test_multiple_domains(self):
        info = {
            "name": "crypto-arbitrage",
            "description": "Arbitrage strategies for cryptocurrency",
            "displayName": "",
            "path": "",
        }
        domains = classify_skill(info)
        self.assertIn("crypto trading", domains)
        self.assertIn("arbitrage strategies", domains)


class TestMonetizationPaths(unittest.TestCase):
    """Monetization-path mapping."""

    def test_trading(self):
        paths = monetization_paths(["crypto trading"])
        self.assertIn("Algorithmic or manual trading", paths)

    def test_software(self):
        paths = monetization_paths(["software or SaaS"])
        self.assertIn("Software or SaaS", paths)
        self.assertIn("Freelancing", paths)

    def test_dedup(self):
        paths = monetization_paths(["crypto trading", "forex trading"])
        self.assertEqual(paths.count("Algorithmic or manual trading"), 1)

    def test_empty(self):
        self.assertEqual(monetization_paths([]), [])


class TestReadSkill(unittest.TestCase):
    """Reading skill metadata from disk."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def _write(self, relpath, content):
        full = os.path.join(self.tmpdir, relpath)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            f.write(content)

    def test_read_skill_md(self):
        self._write("SKILL.md", "---\nname: test-skill\ndescription: A test\n---\n# Test")
        info = read_skill(self.tmpdir)
        self.assertEqual(info["name"], "test-skill")
        self.assertEqual(info["description"], "A test")

    def test_read_meta_json(self):
        self._write("_meta.json", json.dumps({
            "owner": "alice",
            "slug": "my-tool",
            "displayName": "My Tool",
            "latest": {"version": "2.0.0"},
        }))
        info = read_skill(self.tmpdir)
        self.assertEqual(info["owner"], "alice")
        self.assertEqual(info["displayName"], "My Tool")
        self.assertEqual(info["name"], "my-tool")
        self.assertEqual(info["version"], "2.0.0")

    def test_skill_md_takes_priority(self):
        self._write("SKILL.md", "---\nname: from-skill-md\n---\n")
        self._write("_meta.json", json.dumps({"slug": "from-meta"}))
        info = read_skill(self.tmpdir)
        self.assertEqual(info["name"], "from-skill-md")

    def test_fallback_to_dirname(self):
        skill_dir = os.path.join(self.tmpdir, "fallback-name")
        os.makedirs(skill_dir)
        info = read_skill(skill_dir)
        self.assertEqual(info["name"], "fallback-name")


class TestScanSkills(unittest.TestCase):
    """Integration test: scan a small synthetic skills directory."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def _add_skill(self, owner, slug, name, description):
        d = os.path.join(self.tmpdir, owner, slug)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "SKILL.md"), "w") as f:
            f.write(f"---\nname: {name}\ndescription: {description}\n---\n")
        with open(os.path.join(d, "_meta.json"), "w") as f:
            json.dump({"owner": owner, "slug": slug, "displayName": name}, f)

    def test_finds_revenue_skills(self):
        self._add_skill("alice", "crypto-bot", "crypto-bot", "Trade cryptocurrency on Binance")
        self._add_skill("bob", "web-notes", "web-notes", "Personal journal notes")
        results = list(scan_skills(self.tmpdir))
        names = [r["name"] for r in results]
        self.assertIn("crypto-bot", names)
        self.assertNotIn("web-notes", names)  # no revenue domain match

    def test_excludes_polymarket(self):
        self._add_skill("eve", "polymarket-trader", "polymarket-trader",
                        "Trade on Polymarket prediction markets")
        results = list(scan_skills(self.tmpdir))
        names = [r["name"] for r in results]
        self.assertNotIn("polymarket-trader", names)

    def test_trading_categories(self):
        self._add_skill("carol", "fx-bot", "fx-bot", "Forex trading bot")
        results = list(scan_skills(self.tmpdir))
        fx = [r for r in results if r["name"] == "fx-bot"][0]
        self.assertIn("forex trading", fx["trading_categories"])

    def test_non_trading_skill(self):
        self._add_skill("dave", "auto-deploy", "auto-deploy",
                        "Automate deployment pipelines")
        results = list(scan_skills(self.tmpdir))
        dep = [r for r in results if r["name"] == "auto-deploy"][0]
        self.assertEqual(dep["trading_categories"], [])
        self.assertIn("Automation services", dep["monetization_paths"])


class TestFormatSkill(unittest.TestCase):
    """Output formatting."""

    def test_format_contains_required_fields(self):
        skill = {
            "name": "test-skill",
            "owner": "alice",
            "path": "skills/alice/test-skill",
            "description": "A test skill",
            "version": "1.0.0",
            "level": "intermediate",
            "domains": ["software or SaaS"],
            "scores": {"Demand": 5, "Ease of monetization": 4,
                       "Startup cost (low = easy)": 5,
                       "Time to first income": 3, "Scalability": 5},
            "monetization_paths": ["Software or SaaS", "Freelancing"],
            "trading_categories": [],
        }
        output = format_skill(skill)
        self.assertIn("Skill: test-skill", output)
        self.assertIn("Owner: alice", output)
        self.assertIn("Demand: 5/5", output)
        self.assertIn("Software or SaaS", output)
        self.assertNotIn("Trading categories", output)

    def test_trading_categories_shown(self):
        skill = {
            "name": "fx-bot",
            "owner": "bob",
            "path": "skills/bob/fx-bot",
            "description": "Forex trading",
            "version": "",
            "level": "intermediate",
            "domains": ["forex trading"],
            "scores": {"Demand": 3},
            "monetization_paths": ["Algorithmic or manual trading"],
            "trading_categories": ["forex trading"],
        }
        output = format_skill(skill)
        self.assertIn("Trading categories: forex trading", output)


class TestGenerateReport(unittest.TestCase):
    """Full report generation."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def _add_skill(self, owner, slug, name, description):
        d = os.path.join(self.tmpdir, owner, slug)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "SKILL.md"), "w") as f:
            f.write(f"---\nname: {name}\ndescription: {description}\n---\n")
        with open(os.path.join(d, "_meta.json"), "w") as f:
            json.dump({"owner": owner, "slug": slug, "displayName": name}, f)

    def test_report_header(self):
        self._add_skill("u", "s", "s", "stock trading bot")
        report = generate_report(self.tmpdir)
        self.assertIn("Revenue-Generating Skills Report", report)
        self.assertIn("Polymarket", report)

    def test_report_excludes_polymarket(self):
        self._add_skill("u", "poly-bot", "poly-bot", "Polymarket trading")
        self._add_skill("u", "btc-bot", "btc-bot", "Bitcoin crypto trading")
        report = generate_report(self.tmpdir)
        self.assertNotIn("poly-bot", report)
        self.assertIn("btc-bot", report)


if __name__ == "__main__":
    unittest.main()
