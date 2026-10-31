# Week 0 — accounts and budgets checklist

Complete these before running Hermes on the VPS. Store secrets only on the VPS (`~/.hermes/.env`) or in your password manager — never in this repo.

## Accounts

| Item | Action | Done |
|------|--------|------|
| GitHub personal | Repo: `shiva171289/agentic-ai-architecture` | ☐ |
| OpenRouter | Buy ~$10 credits; set API key **monthly limit** to $10 | ☐ |
| Telegram | Create bot via @BotFather; get user ID from @userinfobot | ☐ |
| AWS | Free tier account; **Budget $5** with email alert | ☐ |
| Azure | Free account; **Cost Management budget $5** with alert | ☐ |
| Hostinger VPS | Ubuntu 24.04 KVM (see `hermes/setup/01-hostinger-vps.md`) | ☐ |
| Newsletter | Buttondown free tier; set username in `site/src/site-config.ts` | ☐ |

## Git on your laptop (personal identity)

```powershell
cd d:\projects\agentic-ai-architecture
git config user.name "Shivashanmugam Mohan"
git config user.email "shiva17121989@gmail.com"
ssh -T git@github.com-personal
```

Remote (personal SSH alias):

```powershell
git remote add origin git@github.com-personal:shiva171289/agentic-ai-architecture.git
```

## Private repo (Month 1)

Create **`shiva171289/agentic-ai-private`** and copy templates from [docs/private-repo/SETUP.md](../private-repo/SETUP.md).

## After VPS is ready

Follow in order:

1. [hermes/setup/01-hostinger-vps.md](../../hermes/setup/01-hostinger-vps.md)
2. [hermes/setup/02-hermes-install.md](../../hermes/setup/02-hermes-install.md)
3. [hermes/setup/03-telegram-gateway.md](../../hermes/setup/03-telegram-gateway.md)
4. [hermes/PILOT-RUNBOOK.md](../../hermes/PILOT-RUNBOOK.md) — Week 1 end-to-end test
