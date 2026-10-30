# Week 1 pilot — Augmented LLM pattern

Validate the pipeline end-to-end after VPS + Telegram + Hermes are live.

## Preconditions

- [ ] Week 0 checklist done ([docs/setup/week0-accounts-checklist.md](../docs/setup/week0-accounts-checklist.md))
- [ ] Hermes skills symlinked
- [ ] Telegram bot responds to `status`

## Steps

### 1. Local reference (already in repo)

Review polished reference pack:

- `patterns/w01-augmented-llm/`

This is the **target quality** after Cursor polish. Agents produce first drafts; you merge improvements.

### 2. Harvest vendor sources (VPS or laptop)

```bash
python3 hermes/tools/harvest_sources.py --days 30 --keywords "llm,augmented,bedrock"
```

Confirm `content/source-corpus/latest.md` exists and is recent.

### 3. Telegram — scout

```text
brief w01 augmented-llm
```

Expect: summary + 3 angles in reply or branch note.

### 4. Telegram — full pack

```text
pack w01
```

Expect: branch `drafts/w01` pushed with brief, adr, cloud-mapping, code skeleton, blog, linkedin, diagram.

### 5. Laptop — polish

```powershell
cd d:\projects\agentic-ai-architecture
git fetch origin
git checkout drafts/w01
```

In Cursor:

- Run `uv run pytest` under `patterns/w01-augmented-llm/code`
- Improve code, diagrams, ADR
- Compare to reference files on `main`

### 6. Merge

```powershell
git checkout main
git merge drafts/w01
git push origin main
```

Confirm GitHub Actions: site deploy + pytest.

### 6. Cost tuning

Telegram: `cost`

- Target: **<$3/week** paid tokens
- If high: move BlogWriter/LinkedInEditor to Tier 0; keep ADR/Critic on Tier 1

Log in private repo `metrics.md`:

```markdown
## Week 1 pilot
- OpenRouter spend: $
- Time (you): h
- Notes:
```

### 7. Publish

- Edit blog voice → site live
- LinkedIn Post A (Tue), Post B (Thu) from `linkedin.md`

## Success criteria

- [ ] Draft branch created by agents OR manual fallback documented
- [ ] Tests pass in CI
- [ ] Blog renders on GitHub Pages
- [ ] Spend within budget
- [ ] No employer-specific content (ReviewerCritic rules)
