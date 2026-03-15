# PredictFish Usage Examples

## Example 1: Good Project (Expected High Score)

```bash
uv run scripts/predict.py predict \
  --name "DevOps Dashboard for Startups" \
  --description "All-in-one monitoring dashboard for startups using Vercel and Supabase. Shows deployment status, database metrics, errors, and costs in one place." \
  --target "Startup CTOs and tech leads (1-10 engineers)" \
  --market "10,000+ startups in Korea using Vercel/Supabase. Existing solutions (Datadog, New Relic) are too complex and expensive for small teams." \
  --rounds 20 \
  --output devops-dashboard-prediction.json
```

**Expected Output:**
- Success Score: 75-85
- Strong PMF signal (clear pain point)
- Low risk (proven market, simple solution)
- Improvements: Add freemium tier, integrate with Slack

---

## Example 2: Bad Project (Expected Low Score)

```bash
uv run scripts/predict.py predict \
  --name "Rent Reminder Pro" \
  --description "Telegram bot that sends automated rent reminders to tenants. Property managers can schedule reminders and track payment status." \
  --target "Property managers in Korea (managing 10+ units)" \
  --market "Approximately 5,000 property managers in Korea. Most use email or SMS for communication. Tenants primarily use KakaoTalk, not Telegram." \
  --rounds 20 \
  --output rent-reminder-prediction.json
```

**Expected Output:**
- Success Score: 30-40
- Platform mismatch (tenants don't use Telegram)
- Existing solutions work fine (email/SMS)
- Improvements: Switch to KakaoTalk or email, integrate with property management software

---

## Example 3: Validation Error

```bash
uv run scripts/predict.py predict \
  --name "X" \
  --description "short"
```

**Expected Output:**
```
❌ Validation error: Project name too short (minimum 3 characters)
```

---

## Example 4: MiroFish Not Running

```bash
# Make sure MiroFish is NOT running
uv run scripts/predict.py status
```

**Expected Output:**
```
❌ MiroFish API: http://localhost:5001
   Error: Cannot connect to MiroFish (is Docker running?)

💡 Start MiroFish with: docker-compose up mirofish
```

---

## Example 5: Retrieve Previous Report

```bash
# After running a prediction, get the report_id from the output
uv run scripts/predict.py report report_abc123xyz
```

**Expected Output:**
```
📊 Fetching report: report_abc123xyz

============================================================
🎯 **성공 예측 점수**: 75/100
...
============================================================
```

---

## Integration with PM Workflow

```bash
#!/bin/bash
# PM auto-validation script

PROJECT_NAME="My New Feature"
PROJECT_DESC="Description here"
TARGET="Target users"
MARKET="Market info"

# 1. Generate landing page copy (separate process)
# ...

# 2. Run PredictFish
cd ~/ubik-collective/systems/ubik-pm/skills/predictfish
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
OUTPUT_FILE=~/ubik-collective/systems/ubik-pm/memory/prediction-${TIMESTAMP}.json

uv run scripts/predict.py predict \
  --name "$PROJECT_NAME" \
  --description "$PROJECT_DESC" \
  --target "$TARGET" \
  --market "$MARKET" \
  --rounds 20 \
  --output "$OUTPUT_FILE"

# 3. Extract score
SCORE=$(cat "$OUTPUT_FILE" | jq -r '.prediction.success_score')

# 4. Decision
if [ "$SCORE" -ge 70 ]; then
  echo "✅ High score ($SCORE/100) - RECOMMEND GO"
elif [ "$SCORE" -ge 50 ]; then
  echo "⚠️  Medium score ($SCORE/100) - RISKY, needs improvements"
else
  echo "❌ Low score ($SCORE/100) - RECOMMEND NO-GO"
fi

# 5. Show Director (landing copy + prediction)
```

---

## Notes

- **Rounds:** More rounds = more accurate, but slower
  - 10 rounds: ~30s (quick check)
  - 20 rounds: ~60s (recommended default)
  - 50 rounds: ~3min (deep analysis)

- **Score Interpretation:**
  - 80-100: Strong idea, likely success
  - 60-79: Promising, needs refinement
  - 40-59: Risky, major improvements needed
  - 0-39: Fundamental flaws, pivot or abandon

- **MiroFish Setup:**
  ```bash
  # Start MiroFish (example - actual setup may vary)
  docker-compose up -d mirofish
  
  # Check status
  curl http://localhost:5001/health
  ```
