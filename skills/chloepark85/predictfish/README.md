# 🔮 PredictFish

**Predict project success using MiroFish swarm intelligence.**

Stop wasting dev time on doomed ideas. Run a multi-agent market simulation before you build.

## Quick Start

### 1. Install

This is an OpenClaw skill. If you have the skill loaded:

```bash
cd ~/ubik-collective/systems/ubik-pm/skills/predictfish
```

### 2. Start MiroFish

```bash
# MiroFish runs in Docker
docker-compose up mirofish
```

### 3. Run Prediction

```bash
uv run scripts/predict.py predict \
  --name "My Product Idea" \
  --description "What it does and why it's cool" \
  --target "Who will use it" \
  --market "Market size, competitors" \
  --rounds 20
```

### 4. Get Score

```
🎯 성공 예측 점수: 75/100

📊 시장 반응
Strong demand from early adopters. Differentiation is clear.

⚠️ 주요 리스크 (2개)
1. High customer acquisition cost
2. Strong competitor X in market

💡 개선 제안 (3개)
1. Target niche segment first
2. Partner with distribution channel Y
3. Add feature Z for lock-in
```

**Decision:**

- Score ≥ 70: Show Director, likely go-ahead
- Score 50-69: Risky, needs improvements
- Score < 50: Don't build (or major pivot needed)

## Why This Exists

From the UBIK Systems playbook:

> **Rent Reminder Pro:** 6 hours dev → fundamental flaw discovered  
> "Tenants don't use Telegram"  
> Landing page copy would've caught this in 5 minutes.

PredictFish adds **quantitative validation** to the landing page sanity check.

## How It Works

```
Your Idea → Seed Document → MiroFish API → Swarm Simulation → Prediction
```

**MiroFish** runs a multi-agent simulation:

- Agents represent customers, competitors, market forces
- N rounds of interaction (default: 20)
- Emergent behavior reveals success/failure patterns

**Output:**

- Success score (0-100)
- Risk factors (what could go wrong)
- Improvements (how to increase success rate)
- Market reaction summary

## CLI Reference

### Status Check

```bash
uv run scripts/predict.py status
```

Check if MiroFish API is reachable.

### Predict

```bash
uv run scripts/predict.py predict \
  --name "Product Name" \
  --description "What it does" \
  --target "Target customer segment" \
  --market "Market info" \
  --rounds 20 \
  --output results.json \
  --verbose
```

**Arguments:**

- `--name` (required): Project name
- `--description` (required): Project description (min 10 chars)
- `--target`: Target customer (default: "일반 사용자")
- `--market`: Market info (default: "미정의 시장")
- `--rounds`: Simulation rounds (default: 20, more = slower but deeper)
- `--output`: Save JSON results to file
- `--verbose`: Show seed document and debug logs

### Retrieve Report

```bash
uv run scripts/predict.py report <report_id>
```

Re-fetch a previous prediction report.

## Example: Good vs Bad Score

### ✅ Good Idea (Score: 82)

```bash
uv run scripts/predict.py predict \
  --name "DevOps Dashboard for Startups" \
  --description "All-in-one monitoring for small teams using Vercel/Supabase" \
  --target "Startup CTOs (1-10 eng)" \
  --market "10K startups in Korea, existing tools too complex/expensive"

# Output:
🎯 성공 예측 점수: 82/100
📊 시장 반응: Strong PMF signal, clear pain point
⚠️ 리스크: 1) Vercel may add native monitoring
💡 개선: 1) Add Supabase-specific insights 2) Freemium pricing
```

**Decision:** Show Director → Likely approved ✅

### ❌ Bad Idea (Score: 35)

```bash
uv run scripts/predict.py predict \
  --name "Rent Reminder Pro" \
  --description "Telegram bot for property managers to remind tenants" \
  --target "Property managers in Korea" \
  --market "5K property managers, use email/SMS currently"

# Output:
🎯 성공 예측 점수: 35/100
📊 시장 반응: Platform mismatch, tenants don't use Telegram
⚠️ 리스크: 1) Wrong platform 2) Email/SMS already work
💡 개선: 1) Switch to email/SMS 2) Integrate with property mgmt software
```

**Decision:** Kill project ❌ (or pivot to email/SMS)

## Integration with OpenClaw PM

In `AGENTS.md`, PM has this rule:

```
✅ 필수 절차:
1. 랜딩 페이지 카피 작성 (30분)
2. PredictFish 예측 실행 ← THIS SKILL
3. Director에게 제시 (카피 + 점수)
4. Director 승인 후에만 개발 시작
```

PM workflow:

```bash
# 1. Generate landing copy (existing process)
# 2. Run prediction
cd ~/ubik-collective/systems/ubik-pm/skills/predictfish
uv run scripts/predict.py predict \
  --name "$PROJECT" \
  --description "$DESC" \
  --output ~/ubik-collective/systems/ubik-pm/memory/prediction-$(date +%Y%m%d).json

# 3. Send to Director:
# - Landing page copy
# - PredictFish score + insights
# 4. Wait for Go/No-Go
```

## Architecture

```
predictfish/
├── scripts/
│   └── predict.py           # Main CLI
├── lib/
│   ├── mirofish_client.py   # API wrapper
│   ├── seed_generator.py    # Project → seed document
│   └── report_parser.py     # Report → structured prediction
├── templates/
│   └── seed_template.md     # Seed format
├── SKILL.md                 # OpenClaw skill spec
├── README.md                # This file
└── pyproject.toml           # Python deps
```

## Requirements

- **Python 3.11+** via `uv`
- **MiroFish API** (Docker): `http://localhost:5001`
- **Dependencies:** `requests` (auto-installed by uv)

## Environment Variables

- `MIROFISH_URL`: Override API endpoint (default: `http://localhost:5001`)
- `LLM_API_KEY`: For MiroFish's internal LLM (if configured)

## Troubleshooting

### "Cannot connect to MiroFish"

**Problem:** API not running.

**Solution:**

```bash
docker-compose up mirofish
# or
docker run -p 5001:5001 mirofish:latest
```

### "Validation error: description too short"

**Problem:** Project description < 10 characters.

**Solution:** Provide a real description, not just "test".

### Simulation hangs forever

**Problem:** MiroFish stuck or crashed.

**Solution:**

1. Check MiroFish logs: `docker logs mirofish`
2. Restart: `docker-compose restart mirofish`
3. Reduce rounds: `--rounds 10` (faster, less accurate)

## Performance

**Typical run time:**

- 10 rounds: ~30 seconds
- 20 rounds: ~60 seconds
- 50 rounds: ~3 minutes

Higher rounds = more accurate, but slower.

**Recommendation:** Start with 20 rounds for most projects.

## License

MIT-0 (Public Domain). Do whatever you want with this.

## Credits

Built for **UBIK Systems** by PM 팀장.  
Powered by **MiroFish** swarm intelligence engine.

---

**Remember:** The best code is the code you never write. 🔮
