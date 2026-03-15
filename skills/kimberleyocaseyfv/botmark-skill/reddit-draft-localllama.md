# Reddit Post Draft — r/LocalLLaMA

> ⚠️ 这是草稿文件，不会发布到 GitHub。发帖前需要准备好雷达图配图。

---

## 标题选项（选一个）

**推荐 A（数据驱动）：**
> I built a 5-dimension benchmark for AI agents (not LLMs) — here's how a Llama 3 agent scored vs GPT-4o

**备选 B（问题导向）：**
> We benchmark LLMs all day, but who's benchmarking the agents? I built a tool for that.

**备选 C（直接了当）：**
> BotMark: An automated benchmark that scores AI agents on IQ, EQ, tool use, safety, and self-reflection — not just the model

---

## 正文

<!-- 发帖时用以下英文正文，中文注释是给你看的说明 -->

Hey r/LocalLLaMA,

I've been building AI agents for the past year, and one thing kept bugging me: **we have great benchmarks for models (MMLU, HumanEval, Chatbot Arena), but nothing that tests the actual agent.**

Two agents using the exact same Llama 3 70B can behave completely differently depending on their system prompt, tool configuration, memory setup, and persona. But we have no standardized way to measure that.

So I built **BotMark** — an automated benchmark that evaluates the complete agent, not just the underlying model.

### What it tests (5Q scoring system)

| Quotient | What it measures | Example |
|----------|-----------------|---------|
| **IQ** (300 pts) | Reasoning, code, knowledge, instruction following | "Write a function that..." / "Explain why..." |
| **EQ** (180 pts) | Empathy, persona consistency, ambiguity handling | "My dog just died and I need help with my code" |
| **TQ** (250 pts) | Tool use, planning, multi-step task completion | "Book a flight and then..." with tool call validation |
| **AQ** (150 pts) | Safety, prompt injection resistance, refusal accuracy | Adversarial prompts, jailbreak attempts |
| **SQ** (120 pts) | In-context learning, self-reflection | Can it learn from earlier conversation? Does it know its limits? |

Total: **1000 points** across **15 dimensions**, plus **MBTI personality typing** for your bot.

### How it works

1. You install a "skill" (a set of tool definitions + system prompt) into your agent
2. You say "benchmark yourself"
3. The agent autonomously calls the BotMark API, receives ~60 test cases, answers them using only its own reasoning (no external tools allowed), and submits in batches
4. You get a scored report: total %, per-dimension breakdown, radar chart, MBTI type, and improvement suggestions

**The entire process takes ~5 minutes and requires zero human intervention.**

<!-- 🖼️ 在这里插入雷达图 -->
<!-- [Insert radar chart image here — showing a real agent's 5Q scores] -->

### Why I think this matters for local LLM users

If you're running a local Llama/Mistral/Qwen agent, you're constantly tweaking: system prompts, tool configs, quantization, context length. But how do you know if your changes actually improved the agent overall, or just one dimension?

BotMark gives you a **repeatable, quantitative signal** after every change. Think of it as unit tests for your agent's personality and capabilities.

Some things I've found interesting while testing:

- **Same model, different system prompts** can swing scores by 15-20%
- **EQ is where most agents fail** — even GPT-4o struggles with persona consistency under pressure
- **Safety scores vary wildly** between base models and fine-tuned versions
- **Smaller models can beat larger ones** on TQ (tool use) if their tool prompts are well-designed

### What it's NOT

- Not a model benchmark — it tests the whole agent stack
- Not a vibe check — it's automated, no human graders
- Not a fixed test bank — cases are dynamically generated per session to prevent memorization
- Not tied to any framework — works with LangChain, AutoGen, CrewAI, Dify, Coze, or raw HTTP

### Try it

- **GitHub (skill definitions, open source):** [link to botmark-skill repo]
- **Website:** [botmark.cc](https://botmark.cc)
- **Leaderboard:** [botmark.cc/rankings](https://botmark.cc/rankings)
- Free tier: 5 evaluations, no credit card

The skill definitions are fully open source. The evaluation engine runs on botmark.cc (you send answers, we score them).

### What I'd love feedback on

1. Are there dimensions you think are missing? (I'm considering adding "memory" and "multi-turn coherence" as separate quotients)
2. Would you find it useful if we published model-level aggregates? (e.g., "average score for all Llama 3 70B agents" vs "all GPT-4o agents")
3. Any interest in a self-hosted version of the scoring engine?

Happy to answer any questions. Roast my methodology, I can take it. 🙂

---

## 发帖注意事项

<!-- 以下是给你的执行指南 -->

### 发帖前必须准备：
1. **雷达图配图** — 展示一个真实评测的 5Q 雷达图（最好有 2-3 个不同 agent 的对比）
2. **GitHub 仓库链接** — botmark-skill 仓库要先更新好
3. **Leaderboard 上有数据** — 至少有几个 agent 的跑分结果

### 发帖时间：
- **最佳时间**：美国东部时间上午 9-11 点（北京时间晚 9-11 点）
- 这是 Reddit 流量高峰，帖子更容易获得初始曝光

### 发帖后 2 小时内：
- **积极回复每一条评论** — Reddit 算法看互动率
- 预期会有的问题/质疑：
  - "Why not just use existing benchmarks?" → 强调 agent ≠ model
  - "Is this open source?" → 是的，skill definitions 开源，scoring engine 在服务端
  - "Why not self-hosted?" → 可以说 "considering it, what features would matter most?"
  - "How do you prevent gaming?" → 解释 anti-cheat（动态题目、pattern detection）
  - "5 free evaluations is too few" → "Fair point, open to feedback on pricing"

### Flair / Tag：
- 选 `Resources` 或 `Discussion` flair（不要选 `News`）

### 注意：
- **不要在帖子里用中文** — 纯英文
- **不要过度推销** — "I built" 比 "We're launching" 好得多
- **承认局限性** — 社区尊重诚实，比如主动说 "the scoring engine isn't open source yet"
- **不要发完就走** — 前 2 小时的互动决定帖子生死
