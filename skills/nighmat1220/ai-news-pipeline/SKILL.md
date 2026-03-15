---
name: ai-news-pipeline
description: Run a self-contained Chinese and international AI news workflow inside the current workspace. Use when the user wants to collect RSS news, filter domestic and global AI items, generate cumulative Excel reports, score international news, and build a merged Word brief without relying on an external local repository path.
---

# AI News Pipeline

## Overview

This skill is executable by itself. The actual workflow scripts are bundled in `scripts/`.
Run them against the current workspace or pass `--workspace /path/to/workspace` explicitly.

## Workspace Requirements

The target workspace should contain or accept these files and folders:

- `config/sources.json`
- `config/international_sources.json`
- `companies.txt`
- `data/`
- `reports/`
- `state/`

If the folders do not exist, the scripts create them.

## Install Dependencies

Install Python dependencies before first use:

```bash
python -m pip install -r /path/to/skill/scripts/requirements.txt
```

## Run The Full Workflow

Use the bundled Python entrypoint:

```bash
python /path/to/skill/scripts/run_full_workflow.py --workspace /path/to/workspace
```

Optional time window:

```bash
python /path/to/skill/scripts/run_full_workflow.py --workspace /path/to/workspace --time-window "2026年3月15日0点到2026年3月15日18点"
```

Optional skip-AI mode:

```bash
python /path/to/skill/scripts/run_full_workflow.py --workspace /path/to/workspace --disable-ai
```

## What The Workflow Does

1. Collect domestic RSS items into `data/YYYY-MM-DD.jsonl`.
2. Collect and keyword-filter international RSS items into `data/international_YYYY-MM-DD.jsonl`.
3. Build cumulative domestic Excel output in `reports/company_mentions.xlsx`.
4. Build cumulative international Excel output in `reports/international_company_mentions.xlsx`.
5. Build a merged daily Word brief in `reports/`.

## Inputs

- Domestic RSS config: `config/sources.json`
- International RSS config: `config/international_sources.json`
- Company list: `companies.txt`
- Volcengine key: `ARK_API_KEY`
- Optional model override: `ARK_MODEL`

## Important Behavior

- `state/feed_state.json` controls RSS deduplication.
- Excel files are cumulative.
- The Word brief is rebuilt per run.
- The Word international section only includes the top 5 items by impact score inside the selected time window.
- AI cache files are deleted automatically after each run.

## Troubleshooting

1. If the workflow does not rerun old RSS items, check `state/feed_state.json`.
2. If AI columns are empty, check whether `ARK_API_KEY` is set in the execution environment.
3. If the user wants a full rebuild, delete the relevant daily `data` files and `state/feed_state.json`, then rerun.
4. If the user needs exact commands, read `references/commands.md`.

## References

- `references/commands.md`