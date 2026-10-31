# Week 1 operating guide

Use this guide in your first calendar week after you clone the hub repo. Complete each day in order. Store secrets only on the VPS or in your password manager. Do not commit secrets to git.

**Related docs:** [Week 0 checklist](week0-accounts-checklist.md) · [Agent stack](agent-stack.md) · [Hermes pilot runbook](../../hermes/PILOT-RUNBOOK.md)

---

## Day 1 — Accounts and repository safety

### Goal

Create accounts, set spend limits, and protect the `main` branch.

### Steps

1. Open [week0-accounts-checklist.md](week0-accounts-checklist.md).
2. Create or confirm the GitHub repo `shiva171289/agentic-ai-architecture`.
3. Create an OpenRouter account. Set the API key monthly limit to **$10**.
4. Create a Telegram bot with @BotFather. Save the bot token.
5. Message @userinfobot. Save your numeric Telegram user ID.
6. Create a Buttondown account. Save your embed username for the blog.
7. Configure git on your laptop with your personal name and email.
8. Add the GitHub remote with your personal SSH alias.
9. In GitHub, open **Settings → Branches**. Require a pull request before merge to `main`.
10. Create the private repo `shiva171289/agentic-ai-private`. Copy templates from [private-repo/SETUP.md](../private-repo/SETUP.md).

### Done when

- Every row in the Week 0 table is checked.
- `main` is branch-protected.
- You can run `ssh -T git@github.com-personal` successfully.

### If blocked

- OpenRouter limit: use the dashboard **Limits** page on the key.
- SSH fails: confirm the key is added to GitHub **SSH keys**, not only deploy keys.

---

## Day 2 — Hostinger VPS

### Goal

Run a hardened Ubuntu VPS with a non-root `hermes` user.

### Steps

1. Provision Hostinger KVM with **Ubuntu 24.04**. Add your SSH public key in hPanel.
2. Log in as `root` over SSH.
3. Create user `hermes`. Copy root `~/.ssh` to `/home/hermes/.ssh`.
4. Install updates, `ufw`, `fail2ban`, and `git`.
5. Enable UFW. Allow OpenSSH only.
6. Disable root SSH login and password authentication in `sshd_config`. Restart SSH.
7. Add a 2 GB swap file if RAM is 4 GB.
8. Log in as `hermes`. Confirm `sudo` works.

### Done when

- You can `ssh hermes@<VPS_IP>` without the root account.
- `ufw status` shows OpenSSH allowed.

### If blocked

- Lockout risk: keep one root session open until `hermes` sudo works.
- Full guide: [hermes/setup/01-hostinger-vps.md](../../hermes/setup/01-hostinger-vps.md).

---

## Day 3 — Hermes Agent and repo clone

### Goal

Install Hermes, connect OpenRouter, clone the hub repo, and symlink skills.

### Steps

1. Log in to the VPS as `hermes`.
2. Run the Hermes install script from the Nous Research README. Reload your shell.
3. Run `hermes setup`. Choose **OpenRouter**. Paste the API key. Pick a **Tier 1** model for tool calling.
4. Run `chmod 600 ~/.hermes/.env`.
5. Edit `~/.hermes/config.yaml`. Set a **Tier 0 free** model for auxiliary tasks. Set fallback to Tier 1 only.
6. Generate an ed25519 deploy key. Add the public key to GitHub **Deploy keys** with write access.
7. Configure `~/.ssh/config` to use the deploy key for `github.com`.
8. Clone `git@github.com:shiva171289/agentic-ai-architecture.git` to `~/work/agentic-ai-architecture`.
9. Set git identity to `Hermes (drafts)` and your GitHub noreply email in that clone.
10. Symlink each folder under `hermes/skills/*` into `~/.hermes/skills/`.
11. Run `hermes` in the repo. Ask it to list skills and summarize `roadmap.md`.

### Done when

- Hermes lists skills including `weekly-pack` and `research-scout`.
- The repo clone is at `~/work/agentic-ai-architecture`.

### If blocked

- Tool calling errors: switch Tier 1 model in OpenRouter to a model known for tools.
- Full guide: [hermes/setup/02-hermes-install.md](../../hermes/setup/02-hermes-install.md).

---

## Day 4 — Telegram gateway

### Goal

Connect Telegram to Hermes. Restrict the bot to your user ID only.

### Steps

1. On the VPS as `hermes`, run `hermes gateway setup`.
2. Choose **Telegram**. Paste the bot token from BotFather.
3. Set **allowed users** to your numeric ID only.
4. Run `hermes gateway install`.
5. Run `loginctl enable-linger hermes`.
6. From your phone, message the bot: `status`.
7. Confirm you receive a reply. Confirm strangers cannot use the bot.

### Done when

- `status` returns a healthy reply within one minute.
- Gateway service survives logout (linger enabled).

### If blocked

- No reply: check `systemctl --user status` for the gateway unit.
- Full guide: [hermes/setup/03-telegram-gateway.md](../../hermes/setup/03-telegram-gateway.md).

---

## Day 5 — Source harvest and Week 1 draft pack

### Goal

Refresh the vendor corpus and generate the Week 1 draft pack on branch `drafts/w01`.

### Steps

1. On the VPS or laptop, run `python3 hermes/tools/harvest_sources.py --days 30 --keywords "llm,augmented,bedrock"`.
2. Confirm `content/source-corpus/latest.md` updated.
3. Commit corpus updates on a branch if needed, or let the pack skill commit on `drafts/w01`.
4. In Telegram, send: `brief w01 augmented-llm`.
5. Review the brief summary in Telegram or on the draft branch.
6. In Telegram, send: `pack w01`.
7. Wait for branch `drafts/w01` on GitHub with brief, adr, cloud-mapping, code, blog, linkedin, and diagram.

### Done when

- Branch `drafts/w01` exists on GitHub with the weekly pack files.
- Corpus file is not older than seven days.

### If blocked

- Pack fails: run steps manually using skills in Cursor on your laptop (document in private `metrics.md`).
- Full guide: [hermes/PILOT-RUNBOOK.md](../../hermes/PILOT-RUNBOOK.md).

---

## Day 6 — Polish, test, merge, deploy

### Goal

Polish drafts locally, pass tests, merge to `main`, and verify GitHub Pages.

### Steps

1. On your laptop, run `git fetch origin` and check out `drafts/w01`.
2. Open the repo in Cursor. Read [hermes/CONSTITUTION.md](../../hermes/CONSTITUTION.md) and [content/voice-guide.md](../../content/voice-guide.md).
3. Run `uv run pytest` under `patterns/w01-augmented-llm/code`.
4. Compare drafts to the reference pack on `main` under `patterns/w01-augmented-llm/`.
5. Improve code, ADR, blog voice, and diagram.
6. Check out `main`. Merge `drafts/w01`. Push to `origin main`.
7. Open GitHub Actions. Confirm **Deploy site** and **test-patterns** succeed.
8. Open the live site URL. Confirm Week 1 blog renders.

### Done when

- CI is green.
- Blog post appears at `/blog/w01-augmented-llm/` on GitHub Pages.

### If blocked

- pytest fails: fix on a fix branch; do not merge broken tests.
- Site 404: confirm `base` in `site/astro.config.mjs` matches the GitHub Pages project path.

---

## Day 7 — LinkedIn, metrics, and cron

### Goal

Publish the first LinkedIn posts, log spend, and schedule recurring jobs.

### Steps

1. In Telegram, send `cost`. Record spend in private repo `metrics.md`.
2. If spend exceeds **$3** for the pilot week, move BlogWriter and LinkedInEditor to Tier 0 in config.
3. Edit `patterns/w01-augmented-llm/linkedin.md` for your voice.
4. Post **Post A** on Tuesday and **Post B** on Thursday per [content strategy](../roadmap/02-content-strategy.md).
5. Put the blog link in the first comment on Post B.
6. Update LinkedIn Featured using [linkedin-featured-checklist.md](linkedin-featured-checklist.md).
7. On the VPS, edit crontab as `hermes`. Add jobs from [hermes/cron.md](../../hermes/cron.md) **only after** pilot cost is acceptable.
8. Schedule Thursday harvest and Friday scout first. Add daily news cron after the second week if stable.

### Done when

- Two LinkedIn posts are published or scheduled.
- `metrics.md` has Week 1 pilot numbers.
- Cron entries exist for harvest and scout (optional daily brief later).

### If blocked

- High token cost: reduce pack scope; run brief only until tiers are tuned.

---

## Executive summary (Week 1 outcomes)

1. Hermes runs on the VPS with skills synced.
2. Telegram controls drafts; only your user ID can talk to the bot.
3. Week 1 pattern is merged to `main` with passing tests.
4. GitHub Pages shows the blog.
5. You started LinkedIn rhythm and metrics logging.

Next week: follow [content/calendar.md](../../content/calendar.md) for **w02** and advance Acme stage **stage-w02** in `projects/acme-support/`.
