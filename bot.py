import os, subprocess, sys, json, shutil

HERMES_HOME = os.environ.get("HERMES_HOME", "/app/data")
os.makedirs(HERMES_HOME, exist_ok=True)

DISCORD_TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

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
  token: {DISCORD_TOKEN}
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

# Write .env
with open(f"{HERMES_HOME}/.env", "w") as f:
    f.write("GATEWAY_ALLOW_ALL_USERS=true\n")

# Write auth.json
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
            "access_token": ANTHROPIC_KEY,
            "last_status": "ok"
        }]
    }
}
with open(f"{HERMES_HOME}/auth.json", "w") as f:
    json.dump(auth, f)

# Write SOUL.md
soul_src = "/app/SOUL.md"
soul_dst = f"{HERMES_HOME}/SOUL.md"
if os.path.exists(soul_src):
    shutil.copy(soul_src, soul_dst)
    print("Copied SOUL.md from image")
else:
    with open(soul_dst, "w") as f:
        f.write("# Tention Marketing Bot\n\nYou are the Hermes AI for Tention Marketing, running 24/7 on Railway.\n\nYOU HAVE terminal AND code_execution TOOLS. Use them.\nNEVER say you cannot create channels. You CAN via Discord REST API.\n\nGuild ID: 1432708001868812401\nTeam Rajeev category ID: 1509442091351146556\nClients category ID: 1508829395790467104\nNEVER add user 1235236826793381908 to any channel.\n\nTo CREATE a channel, run this in code_execution:\n\nimport os, requests\ntok = os.environ.get('DISCORD_BOT_TOKEN', '')\ngid = '1432708001868812401'\nr = requests.post(f'https://discord.com/api/v10/guilds/{gid}/channels',\n    headers={'Authorization':f'Bot {tok}','Content-Type':'application/json'},\n    json={'name':'channel-name','type':0,'parent_id':'1509442091351146556',\n          'permission_overwrites':[{'id':gid,'type':0,'allow':'0','deny':'1024'}]})\nprint(r.status_code, r.json())\n\nNEW CLIENT WORKFLOW (automatic):\n1. List channels to find right category\n2. Create private channel named after client\n3. Post info card (Name, Email, Brand, Shopify URL, Collab Code, Onboarding Doc)\n4. Post welcome message with Loom: https://www.loom.com/share/77267678d5e749bdb412daf757a25205\n\nCHANNEL DELETE RULE: Always warn Rajeev first, save messages, get permission. No exceptions.\n")
    print("Wrote inline SOUL.md")

print("All config written. Starting Hermes gateway...")
env = os.environ.copy()
env["HERMES_HOME"] = HERMES_HOME
subprocess.run(["hermes", "gateway", "run"], env=env, check=True)
