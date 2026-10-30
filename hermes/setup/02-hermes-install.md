# Hermes Agent install (VPS)

Confirm commands against [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) README before running.

## 1. Install (as `hermes`)

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.bashrc
```

## 2. OpenRouter

```bash
hermes setup   # or: hermes model
```

- Provider: **OpenRouter**
- Paste API key; set default model to your **Tier 1** choice
- `chmod 600 ~/.hermes/.env`

In OpenRouter dashboard: set key **monthly limit = $10**.

## 3. Cheap-first routing

Edit `~/.hermes/config.yaml` (paths may vary by Hermes version):

- Main model: Tier 1 (tool calling)
- Auxiliary / subagents: Tier 0 free model
- Fallback: Tier 1 only

Disable unused expensive tools (vision, etc.) if not needed.

Example snippet (adjust model IDs to current OpenRouter slugs):

```yaml
# Illustrative — verify against Hermes docs
model: openrouter/deepseek/deepseek-chat
auxiliary_model: openrouter/qwen/qwen3-235b-a22b:free
```

## 4. GitHub deploy key

```bash
ssh-keygen -t ed25519 -f ~/.ssh/gh_deploy -N ""
cat ~/.ssh/gh_deploy.pub
```

GitHub → `shiva171289/agentic-ai-architecture` → Settings → Deploy keys → Add → **Allow write access**

`~/.ssh/config`:

```sshconfig
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/gh_deploy
  IdentitiesOnly yes
```

```bash
mkdir -p ~/work
git clone git@github.com:shiva171289/agentic-ai-architecture.git ~/work/agentic-ai-architecture
cd ~/work/agentic-ai-architecture
git config user.name "Hermes (drafts)"
git config user.email "41898282+shiva171289@users.noreply.github.com"
```

GitHub → Settings → Branches → protect `main` (PR required).

## 5. Skills sync

```bash
mkdir -p ~/.hermes/skills
for d in ~/work/agentic-ai-architecture/hermes/skills/*/; do
  ln -sf "$d" ~/.hermes/skills/"$(basename "$d")"
done
```

Optional cron (as hermes): pull before Friday scout — see [../cron.md](../cron.md).

## 6. Smoke test

```bash
cd ~/work/agentic-ai-architecture
hermes
```

Ask: list skills; summarize `roadmap.md`.

Next: [03-telegram-gateway.md](03-telegram-gateway.md)
