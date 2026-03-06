---
name: "newsriver-global-intelligence"
version: "2.1.0"
description: "Intelligence and proxy infrastructure for AI Agents. 277+ news sources across 137 countries, semantic vector search, AI intelligence reports, and Web2 proxies (email, SMS, scraping, storage). Dual-auth: API key or x402 USDC micropayments on Base."
tags: ["finance", "crypto", "trading", "macro", "sentiment", "rag", "x402", "proxy"]
author: "YieldCircle Infrastructure"
homepage: "https://agent.yieldcircle.app"
author_url: "https://agent.yieldcircle.app"
env:
  NEWSRIVER_API_KEY:
    description: "Your NewsRiver API key for subscription-based access. Required if not using x402 micropayments."
    required: false
---

# NewsRiver Global Intelligence & Infrastructure Skill

## What This Skill Does
NewsRiver gives AI agents access to a global news intelligence API and Web2 communication proxies (email, SMS, scraping, storage). All calls are paid — either via API key subscription or x402 USDC micropayments on Base chain.

## ⚠️ Spending & Safety: What Is Enforced vs. Advisory

### Server-Enforced Protections (cannot be bypassed)
These protections are enforced server-side regardless of agent behavior:

| Protection | Mechanism | Limit |
|---|---|---|
| **IP rate limiting** | KV-based, per IP | 60 requests/minute |
| **API key daily caps** | D1-enforced per tier | Free: 50/day, Trader: 10K, Pro: 100K |
| **Email rate limit** | Per wallet + per IP | 50/hour |
| **SMS rate limit** | Per wallet + per IP | 10/hour |
| **Dry-Run returns mock data only** | No real data without payment | `X-Dry-Run: true` returns `[SAMPLE]` data |
| **Hardcoded sender identity** | Email `From` and SMS `[NewsRiver Agent]` prefix | Cannot be changed by caller |
| **SSRF blocking** | Hostname blacklist on scraper | Blocks localhost, internal IPs, .local, .internal |
| **Storage isolation** | KV namespaced per owner | Cannot read other users' data |

### Advisory (recommended but not enforced by the API)
- **Human approval before paid/outbound calls.** The API does not enforce this — your agent platform must handle it. We strongly recommend configuring your platform to require manual approval for any call to paid endpoints.

### Spending Guardrails: Your Responsibility
> **IMPORTANT:** If using x402 micropayments, the API charges per-request automatically upon valid payment signature. To prevent unexpected charges:
> 1. Use a **limited allowance contract** (e.g., PaySponge) that caps spending — never give the agent your full wallet.
> 2. Configure your agent platform to **require manual approval** for paid calls.
> 3. Set **daily spending alerts** on your wallet.
> 4. Test with `X-Dry-Run: true` first — it's free and returns mock data.

## Authentication
Two options (choose one):

**Option A — API Key (subscription):**
```
X-API-Key: your_key_here
```
Keys are SHA-256 hashed server-side. Raw keys are never stored after first use. Analytics logs mask keys to last 4 chars only (`key_***xxxx`).

**Option B — x402 Micropayments (per-request):**
No API key needed. Agent pays USDC on Base chain per request. Payment details returned in `402` response.

## Testing with Dry-Run (Free)
Always test first. Dry-Run returns clearly labeled mock data (`source: "dry_run_mock"`), verifiable by the agent:
```bash
curl -H "X-Dry-Run: true" https://api.yieldcircle.app/api/v1/articles
# Returns: {"source": "dry_run_mock", "data": [{"title": "[SAMPLE] ..."}]}
```

## Paid Endpoints (13)

| Endpoint | Method | Price |
|---|---|---|
| `/api/v1/articles` | GET | $0.001 |
| `/api/v1/river` | GET | $0.002 |
| `/api/v1/countries` | GET | $0.001 |
| `/api/v1/search/semantic?q=` | GET | $0.001 |
| `/api/v1/intelligence/:timeframe` | GET | $0.05–$1.00 |
| `/api/v1/intelligence/history` | GET | $0.10 |
| `/api/v1/intelligence/generate` | POST | $0.25 |
| `/api/v1/trends/timeline?topic=` | GET | $0.001 |
| `/api/v1/proxy/email` | POST | $0.05 |
| `/api/v1/proxy/sms` | POST | $0.25 |
| `/api/v1/proxy/scrape` | POST | $0.10 |
| `/api/v1/proxy/storage` (write) | POST | $0.01 |
| `/api/v1/proxy/storage?key=` (read) | GET | $0.01 |

## Free Endpoints (5, no auth required)

| Endpoint | Description |
|---|---|
| `/api/v1/docs` | Full API reference with pricing |
| `/api/v1/stats` | Platform statistics |
| `/api/v1/sectors` | Available intelligence sectors |
| `/api/v1/categories` | News categories |
| `/api/v1/intelligence/status` | Latest report availability |

## Error Handling
On `402 Payment Required`, inform the user:
> "This endpoint requires payment. You can set up access at [agent.yieldcircle.app/#pricing](https://agent.yieldcircle.app/#pricing)."

## Contact
Homepage: https://agent.yieldcircle.app
Support: support@yieldcircle.app
