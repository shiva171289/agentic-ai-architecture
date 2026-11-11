---
name: weekly-approval
description: Telegram medium automation — ADR and publish gates via text or inline buttons.
---

# WeeklyApproval

Read [hermes/CONSTITUTION.md](../../CONSTITUTION.md) automation boundary.

## Text commands (works with Hermes gateway)

| Command | Action |
|---------|--------|
| `adr approve w05` | Run `python3 hermes/tools/weekly_pipeline.py on-adr-approved --week w05 --slug <from calendar>` |
| `adr reject w05: notes` | Clear pending; human revises ADR |
| `publish approve w05` | Run `on-publish-approved` → CI + PR merge |
| `pipeline friday` | Run `weekly_pipeline.py friday-adr --next` |

Resolve slug from [content/calendar.md](../../../content/calendar.md) or `calendar_week.py --next --json`.

## Inline buttons

[approval_notify.py](../../tools/approval_notify.py) sends Approve/Reject keyboards.

**Note:** Only one Telegram client may call `getUpdates` per bot. If Hermes gateway already polls, use **text commands** above, or run [telegram_poll_approvals.py](../../tools/telegram_poll_approvals.py) on a schedule when the gateway does not consume callbacks (see [weekly-automation.md](../../../docs/setup/weekly-automation.md)).

## After publish

1. Update [content/publish-progress.json](../../../content/publish-progress.json) (pipeline updates on success).
2. Run `python3 hermes/tools/tag_stage.py wNN --push` on the merge commit.

## Models

Prefer Qwen per [model-tiers-qwen.md](../../../docs/setup/model-tiers-qwen.md).
