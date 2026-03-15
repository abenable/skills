# OpenClaw Setup

OpenClaw bots have native skill support with persistent configuration.

## Method 1: Install via Skill URL (Recommended)

1. In your OpenClaw bot settings, add a new skill with this URL:
   ```
   https://botmark.cc/api/v1/bot-benchmark/skill?format=openclaw
   ```

2. Configure the skill's `BOTMARK_API_KEY` setting with your API Key:
   ```
   bm_live_your_key_here
   ```

3. The skill will be automatically registered with all 5 tools.

## Method 2: One-step Install + Bind

Fetch the skill with your API Key to auto-bind (pass the key in the Authorization header, not as a query parameter):
```bash
curl -H "Authorization: Bearer bm_live_xxx" \
  "https://botmark.cc/api/v1/bot-benchmark/skill?format=openclaw&agent_id=your-bot-id"
```

The response will include a `binding` object with your `binding_id`. Store the `binding_id` in the `BOTMARK_BINDING_ID` environment variable.

## Method 3: Manual Install

1. Download [`skill_openclaw.json`](../skill_openclaw.json)
2. Import it into your OpenClaw bot's skill registry
3. Set environment variables:
   ```
   BOTMARK_SERVER_URL=https://botmark.cc
   BOTMARK_API_KEY=bm_live_xxx
   ```

## Usage

Once installed, your bot's owner can say:
- "Run BotMark" / "benchmark" / "evaluate yourself" / "test yourself"
- The bot will handle everything automatically
