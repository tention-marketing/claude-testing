---
name: hermes-railway-deploy
description: "Deploy Hermes as a 24/7 cloud Discord bot on Railway — Dockerfile, env vars, multi-instance setup, and daily GitHub backup."
version: 1.0.0
author: Hermes Agent
platforms: [linux]
metadata:
  hermes:
    tags: [Railway, Discord, deployment, cloud, 24/7, bot, hermes]
    related_skills: [discord-server-admin, github-pr-workflow]
---

# Deploy Hermes Bot on Railway (24/7 Cloud)

Use this when the user wants the Hermes Discord bot to stay online even when their PC is off. Railway hosts the bot on a cloud server.

## Why Railway

- Free tier available
- Connects directly to GitHub — auto-deploys on every push
- No server management needed
- Bot stays online 24/7 regardless of local PC state

## Architecture

```
GitHub repo (claude-testing)
    |
    | (auto-deploy on push)
    v
Railway Cloud Server
    └── Docker container
        └── hermes gateway run  ->  Discord Server (always online)

Local PC (.hermes/)
    └── discord_backup/         ->  messages saved locally every 5 mins
    └── sessions/, memories/    ->  private data (never pushed)
```

## What Goes in the Repo (safe to push)

- `Dockerfile` — installs hermes via pip, runs gateway
- `bot.py` — writes config from env vars, starts hermes gateway
- `railway.toml` — build + deploy settings
- `railway/config.yaml` — template config (uses `${ENV_VAR}` substitution)
- `railway/SOUL.md` — agent personality
- `.env.example` — env var reference (no real values)
- `scripts/` — automation scripts (token replaced with env var)
- `skills/` — saved workflows

## What NEVER Goes in the Repo

- `config.yaml` with real tokens
- `auth.json`, `google_token.json`
- `sessions/`, `memories/`, `discord_backup/`

## Dockerfile (lightweight — pip install hermes)

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV HERMES_HOME=/app/data

RUN apt-get update && apt-get install -y \
    curl git ripgrep nodejs npm \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir hermes-agent

RUN mkdir -p /app/data

WORKDIR /app
COPY bot.py .

CMD ["python", "bot.py"]
```

## bot.py (writes config from env vars at startup)

```python
import os, json, subprocess

HERMES_HOME = os.environ.get("HERMES_HOME", "/app/data")
os.makedirs(HERMES_HOME, exist_ok=True)

# Write config.yaml using env vars
config = f"""model:
  default: claude-sonnet-4-6
  provider: anthropic
agent:
  max_turns: 90
  gateway_timeout: 1800
discord:
  require_mention: true
  auto_thread: true
  reactions: true
  token: {os.environ.get('DISCORD_BOT_TOKEN', '')}
display:
  personality: kawaii
  streaming: true
memory:
  memory_enabled: true
  user_profile_enabled: true
"""
with open(f"{HERMES_HOME}/config.yaml", "w") as f:
    f.write(config)

# Write auth.json with Anthropic API key
auth = {
    "version": 1,
    "providers": {},
    "active_provider": None,
    "credential_pool": {
        "anthropic": [{
            "id": "railway",
            "label": "railway_key",
            "auth_type": "api_key",
            "priority": 0,
            "source": "env:ANTHROPIC_API_KEY",
            "access_token": os.environ.get("ANTHROPIC_API_KEY", ""),
            "last_status": "ok"
        }]
    }
}
with open(f"{HERMES_HOME}/auth.json", "w") as f:
    json.dump(auth, f)

print("Config written. Starting Hermes gateway...")
env = os.environ.copy()
env["HERMES_HOME"] = HERMES_HOME
subprocess.run(["hermes", "gateway", "run"], env=env, check=True)
```

## railway.toml

```toml
[build]
builder = "dockerfile"

[deploy]
startCommand = "python bot.py"
restartPolicyType = "always"
```

## Environment Variables (set in Railway dashboard)

```
ANTHROPIC_API_KEY  =  sk-ant-api03-...
DISCORD_BOT_TOKEN  =  MTUwMzY1...
HERMES_HOME        =  /app/data
```

## Deployment Steps

1. Push Dockerfile + bot.py + railway.toml to GitHub
2. Go to railway.app -> New Project -> Deploy from GitHub
3. Fix GitHub permissions if repo doesn't show:
   - Go to https://github.com/settings/installations
   - Find Railway -> Configure -> All repositories (or select specific repo)
4. Select the repo, branch: main
5. Go to Variables tab -> add the 3 env vars above
6. Railway auto-builds (5-10 mins first time)
7. Bot goes live 24/7

## Multi-Instance Setup (two bots, two servers)

Each Hermes instance needs its own HERMES_HOME folder and config:

```
Local PC:
~/.hermes/   -> Instance 1 (Server 1, Bot Token 1)
~/.hermes2/  -> Instance 2 (Server 2, Bot Token 2)

Run Instance 2:
HERMES_HOME=~/.hermes2 hermes

Shortcut (add to ~/.bashrc):
alias hermes2="HERMES_HOME=~/.hermes2 hermes"

Railway:
Repo 1 -> Railway Project 1 -> Server 1 -> Bot Token 1
Repo 2 -> Railway Project 2 -> Server 2 -> Bot Token 2
```

Data is FULLY SEPARATE between instances:
- discord_backup/ — only that server's messages
- sessions/ — only that instance's chat history
- memories/ — only that instance's memory
- config.yaml — only that instance's tokens

## Hermes Auth: OAuth vs API Key

Hermes can run two ways on Railway:

| Method | How to get | Works on Railway |
|--------|-----------|-----------------|
| OAuth (claude_code) | Login via browser | NO — expires, needs browser |
| API Key | console.anthropic.com -> API Keys | YES — static, env var |

Always use a real `sk-ant-api03-...` API key for Railway/cloud deployments. OAuth tokens expire and cannot be refreshed headlessly.

## File Watcher: Auto-Push Personal Files to GitHub

If you want any change to your personal Hermes files (skills, scripts, config) to auto-push to GitHub in real time, use a file watcher — NOT a push of the full hermes-agent/ source.

**Key distinction:**
- `~/.hermes/hermes-agent/` = full Hermes source code (10k+ files, NOT yours to push — belongs to NousResearch)
- `~/.hermes/skills/`, `~/.hermes/scripts/`, `~/.hermes/config.yaml` = YOUR personal data (safe and sensible to back up)

**What to watch and push:**
```
~/.hermes/skills/         -> your custom skills
~/.hermes/scripts/        -> automation scripts
~/.hermes/discord_backup/ -> message backups
~/.hermes/config.yaml     -> config (exclude auth.json — has tokens)
```

See `github-repo-management` skill, section "File Watcher — Auto-Commit and Push on Change" for the full watcher script and setup.

**Remote setup for personal backup repo:**
```bash
# Add a secondary remote pointing to your backup repo (keep origin as upstream)
GH_TOKEN=$(git credential fill <<< $'protocol=https\nhost=github.com\n' | grep password | cut -d= -f2)
git remote add rajeev "https://Rajeevboy:${GH_TOKEN}@github.com/Rajeevboy/claude-testing.git"
```

## Daily GitHub Backup (data safety)

To auto-backup discord messages to GitHub every night:

```bash
# Create backup script at /home/rajeev/.hermes/scripts/github_backup.sh
#!/bin/bash
cd /tmp/claude-testing
git pull
cp /home/rajeev/.hermes/discord_backup/all_channel_messages.json ./backups/
git add backups/
git commit -m "backup: discord messages $(date +%Y-%m-%d)" || true
git push https://Rajeevboy:$GH_TOKEN@github.com/Rajeevboy/claude-testing.git main
```

Then set up a daily cron via Hermes:
```
hermes cron create --name daily-github-backup --schedule "every 24h" --script github_backup.sh --no-agent
```

## Pitfalls

### Repo not showing in Railway after connecting GitHub
Railway app needs explicit repository permission. Fix:
1. https://github.com/settings/installations -> Railway -> Configure
2. Change "Only select repositories" to include your repo (or "All repositories")
3. Save -> back to Railway -> repo will appear

### Heavy Dockerfile takes 30+ mins on Railway
The official Hermes Dockerfile (in hermes-agent/) builds everything from source including Playwright browsers. Do NOT use it on Railway — it exceeds free tier build limits.
Use the lightweight `pip install hermes-agent` Dockerfile instead (see above).

### ANTHROPIC_API_KEY vs OAuth token
Hermes on your local PC uses OAuth (claude_code source) stored in auth.json. This cannot be used on Railway — it's a browser-flow credential. You need a proper API key from console.anthropic.com for cloud deployment.

### Discord backup data is local only
All Discord message data (discord_backup/all_channel_messages.json) is saved on YOUR PC only. If PC dies, data is lost. Mitigate with daily GitHub backup (see above). The cron sync script runs every 5 mins and keeps the file fresh.
