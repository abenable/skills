---
name: predictfish
description: "Predict project success using MiroFish swarm intelligence. Simulate market reactions before you build."
license: "MIT-0"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔮",
        "requires": { "bins": ["uv", "docker"] },
        "primaryEnv": "LLM_API_KEY",
      },
  }
---

# 🔮 PredictFish

**Predict project success using MiroFish swarm intelligence.**

Simulate market reactions, customer behavior, and competitive dynamics before writing a single line of code. PredictFish connects to MiroFish (a swarm intelligence engine) to run multi-agent simulations of your product idea in the market.

## Why This Exists

From AGENTS.md:

> **Rent Reminder Pro:** 6시간 개발 후 근본 결함 발견 (세입자 Telegram 안 씀)  
> 랜딩 카피 먼저 보여줬으면 5분 만에 발견했을 것

PredictFish adds **quantitative prediction** to the landing-page sanity check. Before PM starts development:

1. Write landing page copy
2. **Run PredictFish simulation** ← this skill
3. Show Director: copy + prediction score
4. Director approves or kills the project

## How It Works

```
Project Info → Seed Document → MiroFish API → Swarm Simulation → Prediction Report
```

**MiroFish API Flow:**

1. Build knowledge graph from seed
2. Prepare simulation environment
3. Run N rounds of multi-agent simulation
4. Generate prediction report

**Prediction Output:**

- Success score (0-100)
- Risk factors
- Market reaction summary
- Improvement suggestions

## Usage

### 1. Check MiroFish Status

```bash
uv run scripts/predict.py status
```

### 2. Run Prediction

```bash
uv run scripts/predict.py predict \
  --name "Rent Reminder Pro" \
  --description "Telegram bot that reminds tenants to pay rent on time" \
  --target "Property managers in Korea" \
  --market "5000+ property managers, competitors use email/SMS" \
  --rounds 20 \
  --output results.json
```

### 3. Retrieve Saved Report

```bash
uv run scripts/predict.py report <report_id>
```

## OpenClaw Integration

When PM receives a new project request:

```bash
# Generate landing page copy first (existing process)
# Then run prediction:
cd ~/ubik-collective/systems/ubik-pm/skills/predictfish
uv run scripts/predict.py predict \
  --name "$PROJECT_NAME" \
  --description "$DESCRIPTION" \
  --target "$TARGET_CUSTOMER" \
  --market "$MARKET_INFO" \
  --output ~/ubik-collective/systems/ubik-pm/memory/prediction-$(date +%Y%m%d-%H%M%S).json

# Show Director: landing copy + prediction score
# Wait for Go/No-Go
```

## Requirements

- **Python 3.11+** (via `uv`)
- **MiroFish API** running on `http://localhost:5001`
  - Typically via Docker: `docker-compose up mirofish`
- **Environment Variable (optional):**
  - `MIROFISH_URL` - override default API endpoint

## Architecture

```
predictfish/
├── SKILL.md              # This file
├── scripts/
│   └── predict.py        # Main CLI
├── lib/
│   ├── mirofish_client.py   # API client
│   ├── seed_generator.py    # Project → seed document
│   └── report_parser.py     # Report → prediction score
├── templates/
│   └── seed_template.md     # Seed document template
├── README.md
└── pyproject.toml
```

## Example Output

```
🔮 PredictFish: Rent Reminder Pro
📍 MiroFish API: http://localhost:5001

[1/6] 🌱 Generating seed document...
[2/6] 🕸️  Building knowledge graph...
      Graph ID: graph_abc123
[3/6] ⚙️  Preparing simulation (20 rounds)...
      Simulation ID: sim_def456
[4/6] 🏃 Starting simulation...
      Run ID: run_ghi789
[5/6] ⏳ Running swarm intelligence simulation...
      ... running (5s)
      ... running (10s)
      ✅ Simulation completed
[6/6] 📊 Generating prediction report...

============================================================
🎯 **성공 예측 점수**: 35/100

📊 **시장 반응**
타겟 고객(부동산 관리자)는 Telegram보다 이메일/문자를 선호함.
세입자 대부분이 Telegram 미사용으로 도달률 낮음.

⚠️ **주요 리스크** (3개)
1. 플랫폼 미스매치: 타겟 유저가 Telegram 사용 안 함
2. 기존 솔루션 충분: 이메일/문자로 이미 해결 가능
3. 네트워크 효과 부족: 양측(관리자+세입자) 모두 필요

💡 **개선 제안** (2개)
1. 이메일/문자 기반으로 전환 검토
2. 부동산 관리 소프트웨어와 통합 검토
============================================================

💾 Results saved to: results.json
```

**Interpretation:**

- Score: 35/100 → **DO NOT BUILD**
- Fatal flaw caught in 2 minutes (vs 6 hours of dev)
- Director kills project before wasting resources

## Error Handling

**MiroFish not running:**

```
❌ MiroFish API: http://localhost:5001
   Error: Cannot connect to MiroFish (is Docker running?)

💡 Start MiroFish with: docker-compose up mirofish
```

**Invalid input:**

```
❌ Validation error: Project description too short (minimum 10 characters)
```

**Simulation timeout:**

```
❌ Timeout waiting for simulation
```

## API Reference

### `predict.py status`

Check MiroFish connection.

**Returns:** 0 if connected, 1 if error.

### `predict.py predict`

Run success prediction.

**Required:**

- `--name` - Project name
- `--description` - Project description

**Optional:**

- `--target` - Target customer (default: "일반 사용자")
- `--market` - Market info (default: "미정의 시장")
- `--rounds` - Simulation rounds (default: 20)
- `--output` - Save results JSON
- `--verbose` - Show seed document and debug info

**Returns:** 0 if success, 1 if error.

### `predict.py report <report_id>`

Retrieve existing report by ID.

## Integration with PM Workflow

See `AGENTS.md` for PM rules:

```markdown
## 🚨 절대 규칙 (Director 명령)

### **신규 프로젝트 시작 프로세스 (필수)**

✅ 필수 절차:

1. 랜딩 페이지 카피 작성 (30분)
2. **PredictFish 예측 실행** ← NEW STEP
3. Director에게 제시 (카피 + 예측 점수)
4. Director 승인 후에만 개발 시작
```

## License

MIT-0 (Public Domain)

## Credits

Built for UBIK Systems by PM 팀장.  
Powered by MiroFish swarm intelligence engine.
