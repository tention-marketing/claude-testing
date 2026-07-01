---
name: railway-hermes-deployment
description: Deploy, manage, migrate, and back up a Hermes bot running on Railway — covers volume management, bot.py pitfalls, SOUL.md updates, account migration, and auth token preservation across redeploys.
triggers:
  - "railway deployment"
  - "move to another railway account"
  - "backup hermes volume"
  - "migrate hermes"
  - "redeploy broke tokens"
  - "SOUL.md not updating"
  - "where are instructions stored"
  - "bot.py overwrites"
---

# Railway Hermes Deployment

## ARCHITECTURE OVERVIEW

```
GitHub repo (Rajeevboy/...)
  ├── bot.py          ← runs on startup, writes config, starts hermes gateway
  └── SOUL.md         ← system prompt, copied to /app/data/SOUL.md on deploy

Railway Volume mounted at /app/data/
  ├── config.yaml     ← model, provider, Discord settings (OVERWRITTEN by bot.py on redeploy)
  ├── auth.json       ← Spotify + provider tokens (OVERWRITTEN by bot.py on redeploy ⚠️)
  ├── SOUL.md         ← copied from /app/SOUL.md each deploy
  ├── memories/       ← MEMORY.md + USER.md (persistent, survives redeploys)
  ├── skills/         ← all skill files (persistent, survives redeploys)
  ├── google_drive_token.json  ← Google Drive OAuth token (persistent)
  ├── google_credentials.json  ← Google OAuth client credentials (persistent)
  └── openai_key.txt  ← OpenAI API key (persistent)
```

## WHAT LIVES WHERE

| Update needed | Where to edit |
|---|---|
| Bot personality, Discord IDs, curl commands | GitHub → `SOUL.md` → push → redeploy |
| Skills (workflows, task instructions) | Tell agent → edits `/app/data/skills/` directly |
| Memory notes, user profile | Tell agent → edits `/app/data/memories/` directly |
| Model / provider settings | GitHub → `bot.py` config section → push |
| API keys (Anthropic, Discord) | Railway environment variables (never hardcode) |

## CRITICAL PITFALL — bot.py OVERWRITES auth.json ON EVERY REDEPLOY

`bot.py` runs on every Railway deploy and **overwrites** `/app/data/auth.json` with a blank template. This **erases Spotify tokens** every time you push to GitHub.

**Fix:** Add this guard to `bot.py` before writing auth.json:
```python
import os, json
auth_path = f"{HERMES_HOME}/auth.json"
if not os.path.exists(auth_path):
    # Only write blank auth if file doesn't exist yet
    with open(auth_path, "w") as f:
        json.dump(auth_template, f)
else:
    print("auth.json already exists — skipping overwrite to preserve tokens")
```

Until this fix is applied: **re-auth Spotify and Google Drive after every redeploy.**

## HOW TO UPDATE SOUL.md (Bot Instructions)

1. Edit `SOUL.md` in the GitHub repo
2. `git push` to `main` branch
3. Railway auto-detects push and redeploys
4. `bot.py` copies `/app/SOUL.md` → `/app/data/SOUL.md` automatically
5. Hermes restarts with new instructions

Note: The system prompt Rajeev sees in chat is injected at the Hermes level from `SOUL.md` — it is NOT the same as skills or memory.

## BACKUP VOLUME (before migration or as routine)

```bash
cd /app/data && tar \
  --exclude='lost+found' \
  --exclude='*.lock' \
  --exclude='sessions' \
  --exclude='logs' \
  --exclude='cache' \
  --exclude='audio_cache' \
  --exclude='image_cache' \
  --exclude='cron/output' \
  -czf /tmp/hermes_backup_$(date +%Y%m%d).tar.gz .
```

Then upload to Google Drive for safe keeping (see google-drive-oauth skill for upload pattern).

## GITHUB-PORTABLE DEPLOYMENT (deploy anywhere, zero data loss)

The best setup bundles skills + memories INTO the Docker image via a `data_github/` folder. On fresh deploy, `bot.py` copies these to the volume. On redeploys, the volume takes priority (live updates preserved).

### Repo structure:
```
your-repo/
├── bot.py              ← v6+, with auto-restore logic
├── SOUL.md             ← bot personality + Discord instructions
├── Dockerfile          ← COPY data_github/ /app/data_github/
├── .gitignore          ← excludes secrets
└── data_github/        ← committed to GitHub (NO secrets)
    ├── memories/
    │   ├── MEMORY.md
    │   └── USER.md
    └── skills/
        ├── discord/
        ├── integrations/
        ├── marketing/
        └── devops/
```

### Dockerfile:
```dockerfile
FROM ghcr.io/nousresearch/hermes:latest
WORKDIR /app
COPY bot.py .
COPY SOUL.md .
COPY data_github/ /app/data_github/
CMD ["python3", "bot.py"]
```

### bot.py auto-restore logic (add after config.yaml write):
```python
import shutil
from pathlib import Path

GITHUB_DATA = "/app/data_github"

def restore_from_github(src_dir, dst_dir, label):
    if not os.path.exists(src_dir):
        print(f"⚠️  No {label} in image — skipping")
        return
    os.makedirs(dst_dir, exist_ok=True)
    restored = 0
    for root, dirs, files in os.walk(src_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.curator')]
        for file in files:
            if file.endswith('.lock'):
                continue
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(src_file, src_dir)
            dst_file = os.path.join(dst_dir, rel_path)
            if not os.path.exists(dst_file):   # ← only restore if missing
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy2(src_file, dst_file)
                restored += 1
    print(f"✅ {label}: {restored} new files restored from GitHub")

restore_from_github(f"{GITHUB_DATA}/skills",   f"{HERMES_HOME}/skills",   "Skills")
restore_from_github(f"{GITHUB_DATA}/memories", f"{HERMES_HOME}/memories", "Memories")
```

### .gitignore (keep secrets OUT):
```
data_github/auth.json
data_github/google_drive_token.json
data_github/google_credentials.json
data_github/google_pkce.json
data_github/openai_key.txt
data_github/state.db*
data_github/sessions/
data_github/logs/
data_github/cache/
data_github/*.lock
data_github/skills/.curator_backups/
data_github/skills/.usage.json
data_github/skills/.curator_state
```

### How to export current volume → data_github/ for first commit:
```bash
# On the Railway server (run via agent terminal tool):
mkdir -p /tmp/github_push/data_github/skills
mkdir -p /tmp/github_push/data_github/memories

find /app/data/skills -type f \( -name "*.md" -o -name "*.py" -o -name "*.json" \) \
  | grep -v '.curator_backups' | grep -v '.usage.json' | grep -v '.curator_state' \
  | while read file; do
      rel="${file#/app/data/skills}"
      mkdir -p "/tmp/github_push/data_github/skills$(dirname $rel)"
      cp "$file" "/tmp/github_push/data_github/skills$rel"
    done

cp /app/data/memories/MEMORY.md /tmp/github_push/data_github/memories/
cp /app/data/memories/USER.md   /tmp/github_push/data_github/memories/

cd /tmp && tar -czf github_push_ready.tar.gz github_push/
# Then upload to Drive and give Rajeev the download link
```

### Deploy on any new Railway account:
1. Connect GitHub repo
2. Set env vars: `DISCORD_BOT_TOKEN`, `ANTHROPIC_API_KEY`
3. Add Volume at `/app/data`
4. Deploy → bot.py auto-restores skills + memories from image
5. Add secrets manually (Spotify re-auth, Google Drive re-auth, openai_key.txt)

### Key rule: volume always wins over GitHub image
- If a skill file already exists on volume → GitHub version is NOT copied
- This preserves live updates made by the agent between deploys
- To force-update a skill from GitHub: delete it from volume first, then redeploy

## MIGRATION TO NEW RAILWAY ACCOUNT

### Step 1 — Backup current volume (command above)
### Step 2 — Upload backup to Google Drive
### Step 3 — On new Railway account:
1. Connect same GitHub repo (`Rajeevboy/[repo]`)
2. Set environment variables: `DISCORD_BOT_TOKEN`, `ANTHROPIC_API_KEY`
3. Add Railway Volume mounted at `/app/data`
4. Deploy (bot.py runs, creates fresh config)

### Step 4 — Restore volume data:
```bash
cd /app/data
tar -xzf /path/to/hermes_backup_YYYYMMDD.tar.gz
```

### Step 5 — Post-restore checklist:
- [ ] Skills restored ✅ (in backup)
- [ ] Memory restored ✅ (in backup)
- [ ] openai_key.txt restored ✅ (in backup)
- [ ] Spotify tokens — may need re-auth (tokens expire)
- [ ] Google Drive tokens — may need re-auth (tokens expire)
- [ ] Discord bot token — set via env var ✅

## RAILWAY ENVIRONMENT INFO

Key env vars available at runtime:
- `RAILWAY_GIT_REPO_OWNER` — GitHub repo owner
- `RAILWAY_GIT_BRANCH` — current branch
- `RAILWAY_GIT_COMMIT_SHA` — last deployed commit
- `RAILWAY_ENVIRONMENT_NAME` — e.g. "production"
- `RAILWAY_VOLUME_NAME` — persistent volume name
- `HERMES_HOME` — set to `/app/data`

## PITFALLS

- **config.yaml is overwritten on every redeploy** — any manual edits to config.yaml are lost on next push. Keep config changes in `bot.py` instead.
- **auth.json was overwritten on every redeploy in bot.py v1–v5** — Spotify tokens wiped each push. Fixed in v6: bot.py now checks `if not os.path.exists(auth_path)` before writing, and only refreshes the Anthropic key in the existing file. If still on an old bot.py, apply the guard from the CRITICAL PITFALL section above.
- **data_github/ skills only restore to volume if the file doesn't exist yet** — if you update a skill in GitHub and want it to propagate to a running bot, you must delete the old skill file from the volume first (or tell the agent to patch it directly).
- **Backup does not include sessions/logs/cache** — these are large and not needed for migration.
- **Google Drive and Spotify OAuth tokens may expire** — always re-auth these after a long-dormant migration restore.
- **Volume is NOT included in Railway backups by default** — always maintain your own tar.gz backup before any risky operation.
