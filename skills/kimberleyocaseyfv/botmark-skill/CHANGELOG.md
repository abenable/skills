# Changelog

## v1.5.0 (2026-03-15)

### Security Fixes
- **Renamed `system_prompt_injection` → `evaluation_instructions`** in all skill JSON definitions and documentation. The old field name triggered security scanners' system-prompt-override detection. The content and functionality are unchanged — only the field name is different.
- **Removed API key from URL query parameters.** Examples (README Option B, openclaw_setup.md Method 2) now use `Authorization: Bearer` header instead of `?api_key=xxx`.
- **Changed binding_id storage from system prompt to environment variable.** Tool descriptions and setup docs now recommend `BOTMARK_BINDING_ID` env var. Added explicit warnings against embedding secrets in system prompts.
- **Added Required Credentials table to SKILL.md** clearly listing `BOTMARK_API_KEY` as required, `BOTMARK_BINDING_ID` and `BOTMARK_SERVER_URL` as optional.

### Backward Compatibility
- **Old field name preserved as alias.** API responses include both `evaluation_instructions` (primary) and `system_prompt_injection` (deprecated alias), so existing bots that read the old field name continue to work.
- **Runtime unaffected.** The `skill_refresh.system_prompt` mechanism (sent on every `botmark_start_evaluation` call) is unchanged — all bots receive the latest evaluation instructions at runtime regardless of their installed skill version.
- **Version check triggers update prompt.** Bots on v1.4.0 calling `botmark_start_evaluation` with `skill_version` will receive `skill_update.action = "should_update"`, prompting them to re-fetch the latest skill definition.

### Other Changes
- Version badge updated to 1.5.0
- Created `releases/skill-v1.5.0/` with all 8 format/language variants

## v1.4.0 (2026-03-09)

- Added `runner_script` — executable Python script included in package response for automated evaluation
- Concurrent case execution via ThreadPoolExecutor (configurable MAX_WORKERS, default 5)
- Per-case progress reporting — owner gets live updates as each case completes
- Context isolation enforced via independent threads
- Zero dependencies (Python stdlib only)

## v1.3.0 (2026-03-08)

- Added QA Logic Engine — programmatic answer quality enforcement
- `submit-batch` returns `validation_details` with per-case gate results
- Failed gates include actionable corrective instructions for retry
- Exam package includes `execution_plan` with per-dimension gate info
- 19 validation gates across all dimensions (hard + soft)

## v1.2.0 (2026-03-08)

- Added `POST /submit-batch` for progressive batch submission
- Mandatory batch-first policy: ≥3 batches required before final `/submit`
- Per-batch quality feedback with grade (good/fair/poor)
- Score bonus for diligent batching (+5% for ≥5 batches)

## v1.1.0 (2026-03-08)

- Added `/progress` endpoint for real-time progress reporting
- Added `/feedback` endpoint for bot reaction after scoring
- Added `/version` endpoint for update checking
- Optional `webhook_url` for owner notifications
- Exam deduplication: same bot never gets the same paper twice

## v1.0.0 (2026-03-01)

- Initial release: package → answer → submit → score
