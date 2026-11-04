---
name: publish-gate
description: After human Telegram approval, test drafts/wNN in CI and merge it to main through a pull request.
---

# PublishGate

Read `_shared/ground-rules.md` and [hermes/CONSTITUTION.md](../../CONSTITUTION.md).

## Command

`approve publish wNN` (Telegram)

Optional: `publish status wNN` — summarize whether `drafts/wNN` exists and the last CI state.

## Why the merge is not done inside Actions

The `main` ruleset requires **changes to arrive through a pull request**. A direct
`git push origin main` from a workflow is always rejected:

```text
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote: - Changes must be made through a pull request.
! [remote rejected] main -> main (push declined due to repository rule violations)
```

The workflow [publish-approved-week.yml](../../../.github/workflows/publish-approved-week.yml)
therefore **only tests** the draft branch. The merge is done over the
pull-request API by [trigger_publish.py](../../tools/trigger_publish.py), which
runs on the ops host with `GITHUB_PAT`.

## Preconditions

1. Branch `drafts/wNN` exists on `origin` with the full weekly pack.
2. Human already polished code on laptop (recommended) or accepts agent draft quality.
3. `~/.hermes/.env` contains `GITHUB_PAT` on the hub repo with:
   - **Actions**: read and write (dispatch the CI gate)
   - **Contents**: read and write
   - **Pull requests**: read and write (open and merge the PR)
4. Repo has workflow [publish-approved-week.yml](../../../.github/workflows/publish-approved-week.yml).
5. Key name is exactly `GITHUB_PAT` (or `GH_TOKEN`). A near-miss such as
   `GITHUBPAT` is ignored and the script exits with
   `Set GITHUB_PAT or GH_TOKEN in ~/.hermes/.env`.

## Workflow

1. Load `patterns/wNN-slug/` from the local clone (`git fetch origin drafts/wNN`).
2. Send the Telegram **approval checklist** before dispatch:
   - Blog title (from `blog.md` H1)
   - First ~200 words of blog body
   - LinkedIn Post A and Post B headers from `linkedin.md`
   - Branch link on GitHub
   - Text: **Reply `approve publish wNN` to test and publish to GitHub Pages.**
3. On explicit `approve publish wNN`:
   - Resolve the slug from [content/calendar.md](../../../content/calendar.md) (e.g. `w01` → `w01-augmented-llm`).
   - Run:
     ```bash
     cd ~/work/agentic-ai-architecture
     python3 hermes/tools/trigger_publish.py wNN wNN-slug
     ```
   - The script dispatches CI, waits for it, opens the pull request, and merges it.
     Add `--skip-ci` to go straight to the pull request. Add `--dry-run` to print the plan.
4. Verify the merge landed before you report success: check `GET /repos/{repo}/commits/main`
   and confirm the Pages URL returns HTTP 200.
5. Reply with the pull-request URL, the merge sha, and the Pages path `/blog/wNN-slug/`.
6. Paste LinkedIn Post A/B bodies from `linkedin.md` for **manual** posting (agents never post to LinkedIn).

## Failure handling

1. If the CI gate fails, print the run URL and stop. Do not merge.
2. If the pull request is not mergeable, print `mergeable_state` and stop.
3. Never push to `main` directly, and never add a ruleset bypass to work around the gate.
4. If the API returns `Resource not accessible by personal access token`, the token is
   missing a permission. Report which call failed; do not retry blindly.

## Security

- Never commit `GITHUB_PAT`.
- Log the approval date and week in private `metrics.md`.

## Related

- [weekly-pack/SKILL.md](../weekly-pack/SKILL.md)
- [trigger_publish.py](../../tools/trigger_publish.py)
- [04-agent-operations.md](../../../docs/roadmap/04-agent-operations.md)
