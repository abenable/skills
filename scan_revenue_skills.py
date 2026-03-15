#!/usr/bin/env python3
"""Scan a directory of skills and identify which ones can realistically generate revenue.

Revenue can come from services, products, software, consulting, teaching,
or financial trading. Prediction market trading on Polymarket is excluded.
"""

import json
import os
import re
import sys


# ---------------------------------------------------------------------------
# Domain keywords  – used to classify each skill into a revenue domain
# ---------------------------------------------------------------------------

DOMAIN_KEYWORDS = {
    "crypto trading": [
        "crypto", "bitcoin", "btc", "ethereum", "eth", "binance",
        "defi", "dex", "perpetual", "token swap", "solana",
    ],
    "forex trading": ["forex", "fx trading", "currency trading", "foreign exchange"],
    "stock trading": [
        "stock", "equity", "idx", "nasdaq", "nyse", "bursa",
        "shares", "day trading", "scalping", "scalper",
    ],
    "options trading": ["options", "spread", "iron condor", "butterfly", "straddle"],
    "arbitrage strategies": ["arbitrage", "arb"],
    "market making": ["market making", "market-making", "liquidity provision"],
    "quantitative strategies": [
        "quantitative", "quant", "algorithmic trading", "algo trading",
        "backtesting", "backtest",
    ],
    "software or SaaS": [
        "api", "saas", "platform", "sdk", "cli tool", "framework",
        "plugin", "extension", "integration", "webhook", "microservice",
    ],
    "automation services": [
        "automation", "automate", "workflow", "pipeline", "scheduler",
        "cron", "bot", "scraper", "scraping",
    ],
    "consulting": [
        "consult", "advisory", "audit", "pentest", "security",
        "compliance", "assessment", "analysis",
    ],
    "teaching or courses": [
        "teach", "course", "tutorial", "learn", "education",
        "training", "mentor", "onboard",
    ],
    "digital products": [
        "template", "design", "content", "generator", "builder",
        "creator", "converter", "media",
    ],
    "freelancing": ["freelance", "service", "custom"],
    "agency services": ["agency", "white-label", "managed"],
    "affiliate or content revenue": [
        "affiliate", "blog", "newsletter", "seo", "content marketing",
        "social media",
    ],
    "hardware products": [
        "hardware", "iot", "device", "sensor", "robotics", "embedded",
        "3d print", "firmware",
    ],
}

# Trading-related domains (for the trading section of the report)
TRADING_DOMAINS = {
    "crypto trading",
    "forex trading",
    "stock trading",
    "options trading",
    "arbitrage strategies",
    "market making",
    "quantitative strategies",
}

# Scoring heuristics per domain  (demand, ease, low_startup, speed, scalability)
# Each score is 1-5
DOMAIN_SCORES = {
    "crypto trading":              (4, 3, 4, 3, 4),
    "forex trading":               (3, 3, 4, 3, 4),
    "stock trading":               (4, 3, 4, 3, 4),
    "options trading":             (3, 2, 3, 3, 4),
    "arbitrage strategies":        (3, 2, 3, 3, 5),
    "market making":               (3, 2, 2, 3, 5),
    "quantitative strategies":     (4, 2, 3, 3, 5),
    "software or SaaS":            (5, 4, 5, 3, 5),
    "automation services":         (5, 4, 5, 4, 4),
    "consulting":                  (4, 4, 5, 4, 3),
    "teaching or courses":         (4, 3, 5, 3, 5),
    "digital products":            (4, 4, 5, 4, 5),
    "freelancing":                 (4, 5, 5, 5, 2),
    "agency services":             (3, 3, 4, 3, 4),
    "affiliate or content revenue": (3, 3, 5, 2, 4),
    "hardware products":           (3, 2, 2, 2, 3),
}

SCORE_LABELS = ["Demand", "Ease of monetization", "Startup cost (low = easy)",
                "Time to first income", "Scalability"]


# ---------------------------------------------------------------------------
# Polymarket detection
# ---------------------------------------------------------------------------

POLYMARKET_PATTERNS = re.compile(
    r"polymarket|prediction[\s_-]?market|poly[\s_-]?market", re.IGNORECASE,
)


def is_polymarket(name, description, path):
    """Return True when the skill is related to Polymarket prediction markets."""
    for text in (name, description, path):
        if text and POLYMARKET_PATTERNS.search(text):
            return True
    return False


# ---------------------------------------------------------------------------
# Skill level heuristic
# ---------------------------------------------------------------------------

ADVANCED_HINTS = [
    "garch", "quantitative", "ml ", "machine learning", "deep learning",
    "neural", "reinforcement", "backtest", "walk-forward", "regime",
    "options spread", "iron condor", "arbitrage", "market making",
    "kubernetes", "distributed", "microservice",
]
INTERMEDIATE_HINTS = [
    "api", "webhook", "integration", "pipeline", "automation",
    "trading", "analysis", "monitoring", "deploy", "docker",
]


def infer_level(description):
    """Return basic / intermediate / advanced based on description keywords."""
    lower = (description or "").lower()
    for hint in ADVANCED_HINTS:
        if hint in lower:
            return "advanced"
    for hint in INTERMEDIATE_HINTS:
        if hint in lower:
            return "intermediate"
    return "basic"


# ---------------------------------------------------------------------------
# YAML-frontmatter parser (lightweight, no external deps)
# ---------------------------------------------------------------------------

def parse_frontmatter(text):
    """Extract YAML front-matter from a markdown string.

    Returns a dict with at least ``name`` and ``description`` keys
    (possibly empty strings).
    """
    result = {"name": "", "description": ""}
    if not text:
        return result

    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return result

    block = match.group(1)
    for line in block.splitlines():
        for key in ("name", "description", "version", "author", "emoji", "homepage"):
            # Simple "key: value" extraction – good enough for the fields we need
            pattern = rf"^{key}\s*:\s*(.+)"
            m = re.match(pattern, line.strip())
            if m:
                value = m.group(1).strip().strip('"').strip("'")
                result[key] = value
    return result


# ---------------------------------------------------------------------------
# Read a single skill
# ---------------------------------------------------------------------------

def read_skill(skill_dir):
    """Return a dict describing one skill, or None if unreadable."""
    skill_md = os.path.join(skill_dir, "SKILL.md")
    meta_json = os.path.join(skill_dir, "_meta.json")

    info = {
        "path": skill_dir,
        "name": "",
        "displayName": "",
        "description": "",
        "version": "",
        "author": "",
        "owner": "",
    }

    # -- SKILL.md --------------------------------------------------------
    if os.path.isfile(skill_md):
        try:
            with open(skill_md, encoding="utf-8", errors="replace") as fh:
                fm = parse_frontmatter(fh.read())
                info["name"] = fm.get("name", "")
                info["description"] = fm.get("description", "")
                info["version"] = fm.get("version", info["version"])
                info["author"] = fm.get("author", info["author"])
        except OSError:
            pass

    # -- _meta.json ------------------------------------------------------
    if os.path.isfile(meta_json):
        try:
            with open(meta_json, encoding="utf-8", errors="replace") as fh:
                meta = json.load(fh)
                info["displayName"] = meta.get("displayName", "")
                info["owner"] = meta.get("owner", "")
                if not info["name"]:
                    info["name"] = meta.get("slug", "")
                latest = meta.get("latest", {})
                if not info["version"]:
                    info["version"] = latest.get("version", "")
        except (OSError, json.JSONDecodeError):
            pass

    # Fall back to directory name
    if not info["name"]:
        info["name"] = os.path.basename(skill_dir)

    return info


# ---------------------------------------------------------------------------
# Classify a skill
# ---------------------------------------------------------------------------

def classify_skill(info):
    """Return a list of matching domain labels for the skill."""
    searchable = " ".join([
        (info.get("name") or ""),
        (info.get("description") or ""),
        (info.get("displayName") or ""),
        os.path.basename(info.get("path", "")),
    ]).lower()

    matched = []
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in searchable:
                matched.append(domain)
                break
    return matched


# ---------------------------------------------------------------------------
# Monetization paths for a set of domains
# ---------------------------------------------------------------------------

DOMAIN_TO_MONETIZATION = {
    "crypto trading":              ["Algorithmic or manual trading"],
    "forex trading":               ["Algorithmic or manual trading"],
    "stock trading":               ["Algorithmic or manual trading"],
    "options trading":             ["Algorithmic or manual trading"],
    "arbitrage strategies":        ["Algorithmic or manual trading"],
    "market making":               ["Algorithmic or manual trading"],
    "quantitative strategies":     ["Algorithmic or manual trading"],
    "software or SaaS":            ["Software or SaaS", "Freelancing", "Consulting"],
    "automation services":         ["Automation services", "Software or SaaS", "Consulting"],
    "consulting":                  ["Consulting", "Freelancing", "Agency services"],
    "teaching or courses":         ["Teaching or courses", "Digital products"],
    "digital products":            ["Digital products", "Affiliate or content revenue"],
    "freelancing":                 ["Freelancing"],
    "agency services":             ["Agency services", "Consulting"],
    "affiliate or content revenue":["Affiliate or content revenue", "Digital products"],
    "hardware products":           ["Hardware products"],
}


def monetization_paths(domains):
    """Return a deduplicated list of monetization paths for given domains."""
    paths = []
    seen = set()
    for d in domains:
        for p in DOMAIN_TO_MONETIZATION.get(d, []):
            if p not in seen:
                paths.append(p)
                seen.add(p)
    return paths


# ---------------------------------------------------------------------------
# Scan the entire skills directory
# ---------------------------------------------------------------------------

def scan_skills(skills_root):
    """Walk *skills_root* and yield analysed skill dicts.

    Expected layout::

        skills_root/
            owner1/
                skill-a/
                    SKILL.md
                    _meta.json
                skill-b/
                    …
            owner2/
                …
    """
    if not os.path.isdir(skills_root):
        return

    for owner in sorted(os.listdir(skills_root)):
        owner_dir = os.path.join(skills_root, owner)
        if not os.path.isdir(owner_dir):
            continue
        for skill_slug in sorted(os.listdir(owner_dir)):
            skill_dir = os.path.join(owner_dir, skill_slug)
            if not os.path.isdir(skill_dir):
                continue

            info = read_skill(skill_dir)

            # Polymarket exclusion
            if is_polymarket(info["name"], info["description"], info["path"]):
                continue

            domains = classify_skill(info)
            if not domains:
                continue  # not revenue-relevant

            level = infer_level(info["description"])
            paths = monetization_paths(domains)

            # Aggregate scores (average across matched domains)
            scores_sum = [0] * 5
            count = 0
            for d in domains:
                if d in DOMAIN_SCORES:
                    for i, s in enumerate(DOMAIN_SCORES[d]):
                        scores_sum[i] += s
                    count += 1
            if count:
                scores_avg = [round(s / count, 1) for s in scores_sum]
            else:
                scores_avg = [0] * 5

            trading_cats = [d for d in domains if d in TRADING_DOMAINS]

            yield {
                "name": info["name"] or info["displayName"] or skill_slug,
                "owner": info["owner"] or owner,
                "path": os.path.relpath(skill_dir, os.path.dirname(skills_root)),
                "description": info["description"],
                "version": info["version"],
                "level": level,
                "domains": domains,
                "scores": dict(zip(SCORE_LABELS, scores_avg)),
                "monetization_paths": paths,
                "trading_categories": trading_cats,
            }


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def format_skill(skill):
    """Return a formatted string block for one skill."""
    lines = []
    lines.append(f"Skill: {skill['name']}")
    lines.append(f"  Owner: {skill['owner']}")
    lines.append(f"  Path: {skill['path']}")
    if skill["description"]:
        desc = skill["description"]
        if len(desc) > 200:
            desc = desc[:197] + "..."
        lines.append(f"  Description: {desc}")
    if skill["version"]:
        lines.append(f"  Version: {skill['version']}")
    lines.append(f"  Skill level: {skill['level']}")
    lines.append(f"  Domains: {', '.join(skill['domains'])}")
    lines.append("  Revenue scores:")
    for label, value in skill["scores"].items():
        lines.append(f"    {label}: {value}/5")
    lines.append(f"  Monetization paths: {', '.join(skill['monetization_paths'])}")
    if skill["trading_categories"]:
        lines.append(f"  Trading categories: {', '.join(skill['trading_categories'])}")
    return "\n".join(lines)


def generate_report(skills_root):
    """Scan *skills_root* and return the full report as a string."""
    results = list(scan_skills(skills_root))

    sections = []
    sections.append("# Revenue-Generating Skills Report\n")
    sections.append(f"Directory scanned: {skills_root}")
    sections.append(f"Skills with revenue potential: {len(results)}")
    sections.append(f"(Polymarket / prediction-market skills excluded)\n")

    # Group by primary domain
    domain_groups = {}
    for skill in results:
        primary = skill["domains"][0]
        domain_groups.setdefault(primary, []).append(skill)

    for domain in sorted(domain_groups):
        group = domain_groups[domain]
        sections.append(f"\n## {domain.title()} ({len(group)} skills)\n")
        for skill in group:
            sections.append(format_skill(skill))
            sections.append("")  # blank line between skills

    return "\n".join(sections)


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        skills_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skills")
    else:
        skills_root = sys.argv[1]

    if not os.path.isdir(skills_root):
        print(f"Error: directory not found: {skills_root}", file=sys.stderr)
        sys.exit(1)

    print(generate_report(skills_root))


if __name__ == "__main__":
    main()
