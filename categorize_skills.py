#!/usr/bin/env python3
"""Categorize skills into folders by asset class and function type.

Scans the skills/ directory, filters for specific asset classes
(stocks, commodities, forex, crypto) and function types (traders,
monitors, analysis, news/sentiment), then writes a README.md in each
category folder.

Polymarket / prediction-market skills are excluded.
"""

import os
import sys

from scan_revenue_skills import (
    is_polymarket,
    parse_frontmatter,
    read_skill,
)

# ── Asset-class keywords ──────────────────────────────────────────────

ASSET_CLASSES = {
    "stocks": [
        "stock", "equity", "equities", "shares", "nasdaq", "nyse",
        "s&p", "dow jones", "bursa", "idx", "a-share", "a share",
        "ticker", "watchlist", "day trading", "scalping", "scalper",
        "earnings", "dividend",
    ],
    "commodities": [
        "gold", "xau", "silver", "xag", "oil", "crude", "wti",
        "brent", "commodity", "commodities", "futures", "natural gas",
        "platinum", "palladium", "copper",
    ],
    "forex": [
        "forex", "fx ", "fx-", "currency pair", "currency trading",
        "foreign exchange", "cfd", "eur/usd", "gbp/usd", "usd/jpy",
        "aud/usd", "usd/cad", "usd/chf", "nzd/usd", "eur/gbp",
        "eur/jpy", "gbp/jpy", "metatrader", "mt4", "mt5",
    ],
    "crypto": [
        "bitcoin", "btc", "ethereum", "eth", "crypto", "binance",
        "defi", "dex", "perpetual", "token swap", "solana", "sol",
        "blockchain", "web3", "wallet",
    ],
}

# ── Function-type keywords ────────────────────────────────────────────

FUNCTION_TYPES = {
    "traders": [
        "execute", "trade", "trading bot", "buy", "sell",
        "position", "order", "automated trad", "grid trad",
        "scalp", "perpetual", "perp", "swap", "long", "short",
        "copy-trad", "copy trad", "signal",
    ],
    "monitors": [
        "monitor", "watch", "track", "alert", "notify",
        "real-time", "realtime", "real time", "price alert",
        "threshold", "surveillance", "dashboard", "screener",
    ],
    "analysis": [
        "analy", "technical", "fundamental", "chart", "indicator",
        "rsi", "macd", "bollinger", "moving average", "pattern",
        "backtest", "forecast", "predict", "valuation", "research",
        "deep dive", "k-line", "kline", "candle",
    ],
    "news_and_sentiment": [
        "news", "sentiment", "report", "article", "social media",
        "twitter", "headline", "press", "newsletter", "blog",
        "opinion", "rumor", "feed",
    ],
}

# Human-friendly labels
ASSET_LABELS = {
    "stocks": "Stocks",
    "commodities": "Commodities (Gold, Oil, Silver & Futures)",
    "forex": "Forex & CFD Currency Pairs",
    "crypto": "Crypto (BTC & ETH Focus)",
}

FUNCTION_LABELS = {
    "traders": "Traders & Execution",
    "monitors": "Monitors & Watchers",
    "analysis": "Analysis Tools",
    "news_and_sentiment": "News & Sentiment",
}


# ── Classification helpers ────────────────────────────────────────────

def _match_keywords(text, keywords):
    """Return True if any keyword is found in *text*."""
    text_lower = text.lower()
    return any(kw in text_lower for kw in keywords)


def classify_asset_classes(info):
    """Return list of matching asset-class keys for a skill."""
    searchable = " ".join([
        info.get("name") or "",
        info.get("description") or "",
        info.get("displayName") or "",
        os.path.basename(info.get("path", "")),
    ])
    return [ac for ac, kws in ASSET_CLASSES.items()
            if _match_keywords(searchable, kws)]


def classify_function_types(info):
    """Return list of matching function-type keys for a skill."""
    searchable = " ".join([
        info.get("name") or "",
        info.get("description") or "",
        info.get("displayName") or "",
    ])
    return [ft for ft, kws in FUNCTION_TYPES.items()
            if _match_keywords(searchable, kws)]


# ── Markdown formatting ──────────────────────────────────────────────

def _format_skill_entry(info, func_types):
    """Format one skill as a markdown list item."""
    name = info.get("name") or info.get("displayName") or os.path.basename(info["path"])
    owner = info.get("owner") or ""
    path = info.get("path", "")
    desc = info.get("description", "")
    version = info.get("version", "")
    funcs = ", ".join(FUNCTION_LABELS.get(f, f) for f in func_types) if func_types else "General"

    lines = [f"### {name}"]
    lines.append(f"- **Path:** `{path}`")
    if owner:
        lines.append(f"- **Owner:** {owner}")
    if desc:
        if len(desc) > 300:
            desc = desc[:297] + "..."
        lines.append(f"- **Description:** {desc}")
    if version:
        lines.append(f"- **Version:** {version}")
    lines.append(f"- **Type:** {funcs}")
    return "\n".join(lines)


def _write_readme(folder, asset_key, grouped):
    """Write a README.md for one asset-class folder."""
    label = ASSET_LABELS[asset_key]
    total = sum(len(skills) for skills in grouped.values())

    lines = [f"# {label}\n"]
    lines.append(f"> {total} skills found (Polymarket excluded)\n")

    for func_key in ["traders", "monitors", "analysis", "news_and_sentiment"]:
        skills = grouped.get(func_key, [])
        if not skills:
            continue
        func_label = FUNCTION_LABELS[func_key]
        lines.append(f"\n## {func_label} ({len(skills)} skills)\n")
        for info, func_types in skills:
            lines.append(_format_skill_entry(info, func_types))
            lines.append("")  # blank line between entries

    # Catch skills that matched the asset class but no specific function type
    uncategorized = grouped.get("general", [])
    if uncategorized:
        lines.append(f"\n## Other / General ({len(uncategorized)} skills)\n")
        for info, func_types in uncategorized:
            lines.append(_format_skill_entry(info, func_types))
            lines.append("")

    os.makedirs(folder, exist_ok=True)
    readme_path = os.path.join(folder, "README.md")
    with open(readme_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return readme_path, total


# ── Main scan ────────────────────────────────────────────────────────

def scan_and_categorize(skills_root, output_root):
    """Scan skills_root, write categorized READMEs under output_root."""
    if not os.path.isdir(skills_root):
        print(f"Error: directory not found: {skills_root}", file=sys.stderr)
        sys.exit(1)

    # Collect per asset class → function type → list of (info, func_types)
    buckets = {ac: {} for ac in ASSET_CLASSES}

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

            asset_classes = classify_asset_classes(info)
            if not asset_classes:
                continue

            func_types = classify_function_types(info)

            for ac in asset_classes:
                if func_types:
                    for ft in func_types:
                        buckets[ac].setdefault(ft, []).append((info, func_types))
                else:
                    buckets[ac].setdefault("general", []).append((info, []))

    # Write READMEs
    os.makedirs(output_root, exist_ok=True)

    # Write top-level index
    index_lines = ["# Curated Skills by Asset Class\n"]
    index_lines.append("> Skills organized into folders for easy management.")
    index_lines.append("> Polymarket / prediction-market skills excluded.\n")

    results = []
    for ac in ["stocks", "commodities", "forex", "crypto"]:
        folder = os.path.join(output_root, ac)
        grouped = buckets[ac]
        if not any(grouped.values()):
            continue
        readme_path, total = _write_readme(folder, ac, grouped)
        results.append((ac, total, readme_path))
        label = ASSET_LABELS[ac]
        index_lines.append(f"- [{label}](./{ac}/README.md) — {total} skills")

    # Also write a cross-cutting news & sentiment file
    news_folder = os.path.join(output_root, "news_and_sentiment")
    news_grouped = {"news_and_sentiment": []}
    for ac in ASSET_CLASSES:
        for info, func_types in buckets[ac].get("news_and_sentiment", []):
            news_grouped["news_and_sentiment"].append((info, func_types))
    # Deduplicate by path
    seen_paths = set()
    deduped = []
    for info, func_types in news_grouped["news_and_sentiment"]:
        if info["path"] not in seen_paths:
            seen_paths.add(info["path"])
            deduped.append((info, func_types))
    if deduped:
        os.makedirs(news_folder, exist_ok=True)
        total_news = len(deduped)
        news_lines = ["# News & Sentiment Skills\n"]
        news_lines.append(f"> {total_news} skills for tracking news, reports, and sentiment across all asset classes.")
        news_lines.append("> Polymarket / prediction-market skills excluded.\n")
        for info, func_types in deduped:
            news_lines.append(_format_skill_entry(info, func_types))
            news_lines.append("")
        news_path = os.path.join(news_folder, "README.md")
        with open(news_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(news_lines) + "\n")
        index_lines.append(f"- [News & Sentiment](./news_and_sentiment/README.md) — {total_news} skills")

    index_lines.append("")
    index_path = os.path.join(output_root, "README.md")
    with open(index_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(index_lines) + "\n")

    print(f"Output written to: {output_root}/")
    for ac, total, path in results:
        print(f"  {ASSET_LABELS[ac]}: {total} skills → {path}")
    if deduped:
        print(f"  News & Sentiment: {len(deduped)} skills → {news_folder}/README.md")


def main():
    skills_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skills")
    output_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "curated_skills")

    if len(sys.argv) >= 2:
        skills_root = sys.argv[1]
    if len(sys.argv) >= 3:
        output_root = sys.argv[2]

    scan_and_categorize(skills_root, output_root)


if __name__ == "__main__":
    main()
