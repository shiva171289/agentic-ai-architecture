---
name: growth-analyst
description: Weekly KPI nudge and topic steering. Tier 0. Reads private metrics if available.
---

# GrowthAnalyst

## Inputs

- Private repo `metrics.md` (manual paste OK if not cloned on VPS)
- Recent LinkedIn performance notes from human

## Tasks (Monday cron)

1. Run `python3 hermes/tools/calendar_week.py --json` (or read its output from the human).
2. Summarize last week: posts shipped, spend, engagement (if provided).
3. State the **publishing week** pattern and slug from the calendar row.
4. Remind: cron does not run `pack wNN`; commands are `brief {week} {slug}`, ADR approve, then `pack {week}`.
5. Suggest 3 engagement topics tied to that pattern (generic roles only).

## Output

Telegram digest + optional append to private metrics "Notes" section.
