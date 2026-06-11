import os
import subprocess
import sys

# Write config from environment variables
import json

HERMES_HOME = os.environ.get("HERMES_HOME", "/app/data")
os.makedirs(HERMES_HOME, exist_ok=True)

# Write config.yaml
config = f"""model:
  default: claude-sonnet-4-6
  provider: anthropic
providers: {{}}
agent:
  max_turns: 90
  gateway_timeout: 1800
discord:
  require_mention: true
  free_response_channels: 1436302755441410150
  allowed_channels: ''
  auto_thread: true
  reactions: true
  token: {os.environ.get('DISCORD_BOT_TOKEN', '')}
display:
  personality: kawaii
  streaming: true
memory:
  memory_enabled: true
  user_profile_enabled: true
pairing:
  approved_users:
    discord:
      - user_id: "1427987539691835442"
        name: "Rajeev"
"""

with open(f"{HERMES_HOME}/config.yaml", "w") as f:
    f.write(config)

# Write .env to allow all Discord users
with open(f"{HERMES_HOME}/.env", "w") as f:
    f.write("GATEWAY_ALLOW_ALL_USERS=true\n")

# Write auth.json with API key
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

# Run hermes gateway
env = os.environ.copy()
env["HERMES_HOME"] = HERMES_HOME

subprocess.run(
    ["hermes", "gateway", "run"],
    env=env,
    check=True
)
