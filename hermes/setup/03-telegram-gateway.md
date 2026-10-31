# Telegram gateway

## 1. Create bot

1. Telegram → **@BotFather** → `/newbot`
2. Name e.g. `ArchFactory`, username `*_bot`
3. Save **bot token** (never commit to git)

## 2. Your user ID

Message **@userinfobot** → copy numeric **Id**.

## 3. Connect Hermes

On VPS as `hermes`:

```bash
hermes gateway setup
```

- Channel: **Telegram**
- Token: from BotFather
- **Allowed users:** your numeric ID only (critical)

## 4. Service

```bash
hermes gateway install
loginctl enable-linger hermes
```

Verify: `systemctl --user status` (exact unit name per Hermes version).

## 5. BotFather commands (optional)

`/setcommands`:

```text
brief - Research brief for a pattern week
pack - Generate full weekly draft pack
status - Agent and repo health
cost - OpenRouter spend summary
news - Daily AI brief (today)
digest - Latest scout digest
```

## 6. Test

From phone: send `status` to your bot → reply from VPS.

## 7. Security

- Never allow open/public bot without user ID filter
- Rotate token if leaked
- Do not store token in hub repo

Next: [../PILOT-RUNBOOK.md](../PILOT-RUNBOOK.md)
