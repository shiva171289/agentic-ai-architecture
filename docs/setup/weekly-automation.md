# Weekly automation (medium option)

Two human taps per week: **ADR approve** → **publish approve**.

## Schedule (UTC)

Add to [hermes/cron.md](../../hermes/cron.md) on the VPS:

1. **Friday 07:05** — `weekly_pipeline.py friday-adr --next` (scout + ADR + Telegram card).
2. Do **not** schedule `telegram_poll_approvals.py` while the Hermes gateway owns this bot.
   Only one client may call `getUpdates`, so the poller gets HTTP 409 on every tick (981
   conflicts logged) and races the gateway for inbound messages. Approve with **text**
   commands through Hermes: `adr approve w05` / `publish approve w05`.

`weekly_pipeline.py friday-adr` commits `patterns/wNN-slug/` and pushes `drafts/wNN`
**before** it sends the card, so the links in that message always resolve. If the push
fails it does not send the card.

## Flow

```text
Friday cron → brief + ADR draft → Telegram (link + Approve/Reject)
Approve ADR → pack to drafts/wNN → Telegram publish card
Approve publish → CI + PR merge → Pages live → tag stage-wNN
```

## Next week id

Automation uses [content/publish-progress.json](../../content/publish-progress.json), not the calendar date.

```bash
python3 hermes/tools/calendar_week.py --next --json
```

After w01–w04 content ships, set `last_published_week` to `w04` so the next run targets **w05 orchestrator-workers**.

## One-time catch-up (w02–w04)

Content for w02–w04 exists locally but:

- Only **`stage-w01`** tag exists on the remote today.
- **w02–w04 are not on `main`** until you merge and run publish-gate.

### Publish w02–w04 manually

1. Merge branch to `main` (or four PRs).
2. For each week:
   ```bash
   python3 hermes/tools/trigger_publish.py w02 w02-prompt-chaining
   python3 hermes/tools/tag_stage.py w02 --push
   ```
3. Set `last_merged_to_main_week` and `last_published_week` to `w04` in `publish-progress.json`.

## Telegram + Hermes conflict

Hermes gateway and `telegram_poll_approvals.py` both use the Bot API. Use **text** `adr approve wNN` through Hermes, or pause gateway polling if you rely on inline buttons only.

## Related

- [weekly-approval SKILL](../../hermes/skills/weekly-approval/SKILL.md)
- [model-tiers-qwen.md](model-tiers-qwen.md)
