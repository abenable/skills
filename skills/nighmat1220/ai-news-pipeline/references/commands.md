# Commands

## Install dependencies

```bash
python -m pip install -r /path/to/skill/scripts/requirements.txt
```

## Full workflow

```bash
python /path/to/skill/scripts/run_full_workflow.py --workspace /path/to/workspace
```

## Full workflow with time window

```bash
python /path/to/skill/scripts/run_full_workflow.py --workspace /path/to/workspace --time-window "2026年3月15日0点到2026年3月15日18点"
```

## Full workflow without AI generation

```bash
python /path/to/skill/scripts/run_full_workflow.py --workspace /path/to/workspace --disable-ai
```

## Direct scripts

```bash
python /path/to/skill/scripts/collect_feeds.py
python /path/to/skill/scripts/generate_company_report.py
python /path/to/skill/scripts/generate_international_report.py
```

## Required workspace files

- `config/sources.json`
- `config/international_sources.json`
- `companies.txt`

## Outputs

- `data/YYYY-MM-DD.jsonl`
- `data/international_YYYY-MM-DD.jsonl`
- `reports/company_mentions.xlsx`
- `reports/international_company_mentions.xlsx`
- merged daily Word brief in `reports/`