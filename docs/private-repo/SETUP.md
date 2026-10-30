# Private repo setup — `agentic-ai-private`

Create a **private** GitHub repo under `shiva171289` for metrics and contacts. Do not commit these files to the public hub.

## Create repo

1. GitHub → New repository → `agentic-ai-private` → **Private**
2. Local:

```powershell
mkdir d:\projects\agentic-ai-private
cd d:\projects\agentic-ai-private
git init -b main
git config user.name "Shivashanmugam Mohan"
git config user.email "shiva17121989@gmail.com"
git remote add origin git@github.com-personal:shiva171289/agentic-ai-private.git
```

3. Copy templates below, commit, push.

## metrics.md (template)

```markdown
# Metrics log

## YYYY-MM
- LinkedIn followers:
- Newsletter subscribers:
- GitHub stars (hub):
- OpenRouter spend ($):
- Patterns published:
- Top post (link):
- Notes:
```

## contacts.md (template)

```markdown
# Practitioner contacts (learning conversations)

| Name | Role | Topic | Last touch | Notes |
|------|------|-------|------------|-------|
```

## offers/ (optional Year 2+)

Store draft SOW and architecture review templates here only after activating monetization track.

## Hermes access

GrowthAnalyst may read `metrics.md` if you add a **second deploy key** on the private repo and clone to VPS `~/work/agentic-ai-private`. Optional; manual paste works for Year 1.
