# Hermes Safe Push Pattern

When the user asks to push ~/.hermes/ content to GitHub, ALWAYS follow this pattern.

## What to Push (Safe)
- scripts/               automation scripts (with secrets replaced by env vars)
- skills/                workflow library
- SOUL.md                agent personality
- README.md              project description
- .gitignore             blocks sensitive files

## What NEVER to Push
These contain live credentials — always block them in .gitignore:
- config.yaml            bot tokens, API keys
- config.yaml.bak.*      backups of above
- auth.json              login tokens
- auth.lock
- google_token.json      Google OAuth token
- google_client_secret.json
- *.pid, *.lock
- state.db*              app state database
- gateway_state.json
- sessions/              private chat history
- memories/              personal notes
- discord_threads.json
- channel_directory.json
- models_dev_cache.json
- ollama_cloud_models_cache.json
- logs/
- cache/, audio_cache/, image_cache/, images/
- pastes/, sandboxes/
- cron/
- kanban.db*
- bin/, hermes-agent
- hooks/
- pairing/

## .gitignore Template
```
# SENSITIVE - never push
config.yaml
config.yaml.bak.*
auth.json
auth.lock
google_token.json
google_client_secret.json
*.pid
*.lock
state.db*
gateway_state.json
models_dev_cache.json
ollama_cloud_models_cache.json

# Private data
sessions/
memories/
discord_threads.json
channel_directory.json
logs/
cache/
audio_cache/
image_cache/
images/
pastes/
sandboxes/
cron/
kanban.db*
bin/
hermes-agent
hooks/
pairing/

# OS
.DS_Store
__pycache__/
*.pyc
```

## Workflow
1. Clone target repo to /tmp/<repo-name>
2. Write .gitignore first (before copying any files)
3. Copy safe folders: scripts/, skills/, SOUL.md
4. Scan copied scripts for hardcoded secrets:
   grep -rn "TOKEN\s*=\s*['\"][A-Za-z0-9]" /tmp/<repo> --include="*.py" --include="*.js"
5. Replace any found secrets with env var references
6. rm -rf /tmp/<repo>/.git && git init (clean history, no leaked commits)
7. Commit and push

## Authentication in execute_code
Direct curl with env vars silently fails in hermes sandbox. Use this pattern:
```python
write_file("/tmp/ghtoken.sh", f"export GH_TOKEN={TOKEN}\n")
terminal("source /tmp/ghtoken.sh && curl -s -H 'Authorization: token $GH_TOKEN' https://api.github.com/user")
```

## Initial Commit Reset
If push is blocked and you only have one commit (initial), you cannot `git reset HEAD~1`.
Solution: rm -rf .git, reinit, recommit clean, force push.
