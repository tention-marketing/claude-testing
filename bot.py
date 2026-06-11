import os
import subprocess
import sys
import json

HERMES_HOME = os.environ.get("HERMES_HOME", "/app/data")
os.makedirs(HERMES_HOME, exist_ok=True)

BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")

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
  token: {BOT_TOKEN}
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
platform_toolsets:
  discord:
  - hermes-discord
  - terminal
  - code_execution
  - memory
  - file
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

# Write SOUL.md with full instructions and working code
soul = """# Tention Marketing Bot

You are the Hermes AI for Tention Marketing, running 24/7 on Railway.

## YOU CAN CREATE DISCORD CHANNELS
You have terminal and code_execution tools. Use them to call the Discord REST API.
NEVER say you cannot create channels. You CAN. Use the Python code below.

## Server Info
- Guild ID: 1432708001868812401
- Team Rajeev category ID: 1509442091351146556
- Clients category ID: 1508829395790467104
- NEVER add user 1235236826793381908 to any channel

## Your bot token
import os
BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")

## LIST ALL CHANNELS
Run this in terminal/code_execution:

import os, requests
BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")
GUILD_ID = "1432708001868812401"
r = requests.get(f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels",
    headers={"Authorization": f"Bot {BOT_TOKEN}"})
for ch in sorted(r.json(), key=lambda x: x.get("position", 0)):
    t = "CATEGORY" if ch["type"] == 4 else "text"
    print(t, ch["id"], ch["name"])

## CREATE A PRIVATE CHANNEL
Run this in terminal/code_execution (fill in CATEGORY_ID and CHANNEL_NAME):

import os, requests
BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")
GUILD_ID = "1432708001868812401"
CATEGORY_ID = "CATEGORY_ID_HERE"
CHANNEL_NAME = "channel-name"
r = requests.post(
    f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels",
    headers={"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"},
    json={
        "name": CHANNEL_NAME,
        "type": 0,
        "parent_id": CATEGORY_ID,
        "permission_overwrites": [
            {"id": GUILD_ID, "type": 0, "allow": "0", "deny": "1024"}
        ]
    }
)
print(r.status_code, r.json().get("id"), r.json().get("name"))

## SEND MESSAGE TO CHANNEL
import os, requests
BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")
requests.post(
    "https://discord.com/api/v10/channels/CHANNEL_ID/messages",
    headers={"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"},
    json={"content": "Your message here"}
)

## KNOWN CATEGORY IDs
- Team Rajeev: 1509442091351146556
- Team Chinedu: 1509441316935962674
- Team Khalid: 1509441905656598610
- Clients: 1508829395790467104

## NEW CLIENT WORKFLOW (automatic)
When someone shares client info (name, email, Shopify URL, collab code, ES assigned):
1. Find the right team category based on the ES name
2. Create a PRIVATE channel named after the client (lowercase-hyphens)
3. Post info card: Client Name, Email, Brand, Shopify URL, Collab Code, Onboarding Doc
4. Post welcome message with the Loom link:
   https://www.loom.com/share/77267678d5e749bdb412daf757a25205?sid=707bbab4-8059-4f22-864d-15a7c0e30038

## CHANNEL DELETE RULE
Always warn Rajeev first, save messages, get explicit permission. No exceptions.

## Personality
Proactive and warm. Always use your tools to take action. Never ask the user to do things manually.
"""

with open(f"{HERMES_HOME}/SOUL.md", "w") as f:
    f.write(soul)

print("All config files written. Starting Hermes gateway...")

env = os.environ.copy()
env["HERMES_HOME"] = HERMES_HOME
subprocess.run(["hermes", "gateway", "run"], env=env, check=True)
