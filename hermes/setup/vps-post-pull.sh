#!/bin/bash
# Run on VPS as user hermes after git pull (cron or manual).
set -euo pipefail
REPO="${HOME}/work/agentic-ai-architecture"
cd "$REPO"
git pull --ff-only origin main
for skill in "$REPO"/hermes/skills/*/; do
  name="$(basename "$skill")"
  mkdir -p "${HOME}/.hermes/skills"
  ln -sfn "$skill" "${HOME}/.hermes/skills/${name}"
done
if [ -f "$REPO/hermes/setup/crontab.hermes" ]; then
  crontab "$REPO/hermes/setup/crontab.hermes"
  echo "Crontab installed from hermes/setup/crontab.hermes"
fi
echo "Skills symlinked."
python3 "$REPO/hermes/tools/calendar_week.py" --next --json
python3 "$REPO/hermes/tools/job_status.py" || true
