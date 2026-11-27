---
name: weekly-pack
description: Orchestrate full weekly pattern pack onto drafts branch after ADR approval.
---

# WeeklyPack orchestrator

Enforce `_shared/ground-rules.md` across subagents.

## Command

`pack wNN` (Telegram or CLI)

## Workflow

1. **SourceHarvester** if `content/source-corpus/latest.md` missing or older than 7 days (or `sources refresh` on Telegram).
2. **ResearchScout** if `brief.md` missing or stale (>7 days).
3. **PatternArchitect** → pause until human approves ADR on Telegram.
4. Parallel:
   - **CloudMapper**
   - **CodeBuilder** (pattern sample + Acme stage in `projects/acme-support/`)
   - **DiagramAgent**
5. **BlogWriter** (after step 4 completes)
6. **LinkedInEditor**
7. **ReviewerCritic** → fix loop once
8. Git:
   - `git checkout -B drafts/wNN`
   - Commit all files under `patterns/wNN-slug/` **and** changes under `projects/acme-support/` (if any)
   - `git push -u origin drafts/wNN`
9. Telegram checklist (branch link + file list) — send it to the owner's **DM** with `python3 hermes/tools/notify_dm.py`, never by calling `send_message` yourself with a chat id you picked.

## Model policy

SourceHarvester script: no LLM. Scout, Diagram, Blog draft, LinkedIn: Tier 0. Architect, CloudMapper, Critic: Tier 1.

For Tier 0 drafts, run the sub-skill in a one-shot session and keep the output:

```bash
hermes chat --query-file q_blog.txt --oneshot -m "$OPENROUTER_NEWS_MODEL" -Q > blog_raw.txt 2>&1
```

The session appends a `session_id:` line — strip it before saving the artifact. Never pipe that command to `tail`; the body is lost. Put every fact the writer may use in the query file (`--query-file` preserves quotes and backticks), and state "do not use tools" — the draft comes back as text, then the editor pass fixes table schemas and unsupported claims.

## Notes from runs

- Tier-0 drafts on Qwen need `export PATH="$HOME/.local/bin:$PATH"` and `set -a; . ~/.hermes/.env; set +a` in the terminal first (sessions do not inherit the env file). Then `hermes chat --query-file q.txt --oneshot -m "$OPENROUTER_NEWS_MODEL" -Q > raw.txt 2>&1`; strip the trailing `session_id:` line. Two defects recur every time: the scenario-ladder table's last two columns come back swapped (values land under `This week` instead of `Ships`), and the LinkedIn Post A hook opens with a voice-guide ban-list phrase (e.g. "changes the game"). The editor pass must fix both — verify with a `grep` for the ban list and a word count of the blog body (floor 1,200).
- Before staging, `git add` only `patterns/wNN-slug` and `projects/acme-support` — the repo root can hold stray untracked `q_*.txt` / `*_raw.txt` from prior or concurrent runs that must never be committed, alongside the generated `content/source-corpus` and `content/daily-brief`.
- The ground-rules block is `hermes/skills/_shared/ground-rules.md`, not `_shared/ground-rules.md` inside each skill directory.
- The pattern-sample suite and the Acme suite use different `pythonpath` roots: run them from their own directories (`cd patterns/wNN-slug/code && pytest`, `cd projects/acme-support && pytest`). A single root invocation fails collection.
- Where no `uv` is on PATH, run the bundled interpreter: `"$(dirname "$(readlink -f "$(which python)")")/python" -m pytest -q`.
- Send the step-9 checklist with `python3 hermes/tools/notify_dm.py --file <path>`. It sources `~/.hermes/.env` itself (terminal sessions do not inherit it) and resolves the owner's DM internally: `TELEGRAM_APPROVAL_CHAT_ID` → `TELEGRAM_HOME_CHANNEL` → first `TELEGRAM_ALLOWED_USERS` entry. Do **not** build a chat id from `TELEGRAM_CHAT_ID` — that is the news group, and a checklist landing there is the exact bug this helper exists to prevent.

Never commit secrets. Never push to `main`.
