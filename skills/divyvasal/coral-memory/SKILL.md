---
name: coral-memory
description: "Memory storage and retrieval via Coral Bricks. Store facts, preferences, and context; retrieve them by meaning. Use when: (1) remembering facts or preferences for later, (2) recalling stored memories by topic or intent, (3) forgetting/removing memories matching a query. NOT for: web search, file system search, or code search — use other tools for those."
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["CORAL_API_KEY"], "bins": ["curl", "python3"] },
        "primaryEnv": "CORAL_API_KEY",
        "homepage": "https://coralbricks.ai",
        "privacyPolicy": "https://www.coralbricks.ai/privacy",
        "emoji": "🧠",
      },
  }
---

# Coral Memory

Memory storage and retrieval powered by Coral Bricks embeddings (768-dim vectors). Store facts, preferences, and context; retrieve them later by meaning. All memories are stored in the default collection.

## Setup

Set your API key (get one at https://coralbricks.ai):

```bash
export CORAL_API_KEY="ak_..."
```

Optionally override the API URL (defaults to `https://search-api.coralbricks.ai`):

```bash
export CORAL_API_URL="https://search-api.coralbricks.ai"
```

## Tools

### coral_store — Store a memory

Store text with optional metadata for later retrieval by meaning.

```bash
scripts/coral_store "text to store" [metadata_json]
```

- `text` (required): Content to remember
- `metadata_json` (optional): JSON string of metadata, e.g. `'{"source":"chat","topic":"fitness"}'`

Output: JSON with `status` (e.g. `{"status": "indexed"}`). Use coral_delete_matching to remove memories by query.

Example:

```bash
scripts/coral_store "User prefers over-ear headphones with noise cancellation"
scripts/coral_store "Q3 revenue was $2.1M" '{"source":"report"}'
```

### coral_retrieve — Retrieve memories by meaning

Retrieve stored memories by semantic similarity. Returns matching content ranked by relevance.

```bash
scripts/coral_retrieve "query" [k]
```

- `query` (required): Natural language query describing what to recall
- `k` (optional, default 10): Number of results to return

Output: JSON with `results` array, each containing `text` and `score`. Use coral_delete_matching to remove memories by query.

Example:

```bash
scripts/coral_retrieve "wireless headphones preference" 5
scripts/coral_retrieve "quarterly revenue" 10
```

### coral_delete_matching — Forget memories by query

Remove memories that match a semantic query. Specify what to forget by meaning.

```bash
scripts/coral_delete_matching "query" [limit]
```

- `query` (required): Natural language query describing memories to remove
- `limit` (optional, default 1): Maximum number of matching memories to delete

Output: JSON with `deleted` count.

Example:

```bash
scripts/coral_delete_matching "dark mode preference" 1
scripts/coral_delete_matching "forget my workout notes" 5
```

## Privacy

[Privacy Policy](https://www.coralbricks.ai/privacy)

## Notes

- All memories are stored in the default collection; collections are not exposed to the agent
- All text is embedded into 768-dimensional vectors for semantic matching
- Results are ranked by cosine similarity (higher score = more relevant)
- Stored memories persist across sessions
- The `metadata` field is free-form JSON; use it to tag memories for easier filtering

## Indexing delay (store then retrieve)

**Memories take ~60 seconds to become retrievable** after `coral_store`. If you store something and immediately retrieve it, the results may be empty or incomplete.

When the user asks you to store and then retrieve in the same turn:
1. Run `coral_store` first
2. Inform the user the memory was stored successfully
3. If you need to verify via retrieve: **tell the user you are waiting ~60 seconds** for the memory to become retrievable, then wait, then run `coral_retrieve`. Alternatively, skip the retrieve and confirm the store succeeded (the user can retrieve later)
4. If you retrieve once and get empty results: **tell the user you are waiting ~60 seconds**, then retry once
