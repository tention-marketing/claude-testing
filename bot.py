import os, subprocess, sys, json

HERMES_HOME = os.environ.get("HERMES_HOME", "/app/data")
os.makedirs(HERMES_HOME, exist_ok=True)

BOT_TOKEN=os.env...N", "")

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
            "access_token": os.environ.get("ANTHROPIC_API_KEY", ""),
            "last_status": "ok"
        }]
    }
}
with open(f"{HERMES_HOME}/auth.json", "w") as f:
    json.dump(auth, f)

# Write SOUL.md — copy from /app/SOUL.md if it exists, else write inline
soul_src = "/app/SOUL.md"
soul_dst = f"{HERMES_HOME}/SOUL.md"
if os.path.exists(soul_src):
    import shutil
    shutil.copy(soul_src, soul_dst)
    print("Copied SOUL.md from image")
else:
    # fallback inline
    with open(soul_dst, "w") as f:
        f.write("""# Tention Marketing Bot\n\nYou are the Hermes AI for Tention Marketing.\n\nYOU HAVE terminal AND code_execution TOOLS. USE THEM.\nNEVER say you cannot create channels. You CAN via Discord REST API.\n\nGuild ID: 1432708001868812401\nTeam Rajeev category ID: 1509442091351146556\nNEVER add user 1235236826793381908 to any channel.\n\nTo create a channel, run this Python in your code_execution tool:\n\nimport os, requests\nBOT_TOKEN=os.env...N","")\nGUILD_ID="1432708001868812401"\nCATEGORY_ID="1509442091351146556"\nr = requests.post(\n    f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels",\n    headers={"Authorization":f"Bot {BOT_TOKEN}","Content-Type":"application/json"},\n    json={"name":"channel-name","type":0,"parent_id":CATEGORY_ID,\n          "permission_overwrites":[{"id":GUILD_ID,"type":0,"allow":"0","deny":"1024"}]}\n)\nprint(r.status_code, r.json())\n""")
    print("Wrote inline SOUL.md")

print("All config written. Starting Hermes gateway...")
env = os.environ.copy()
env["HERMES_HOME"] = HERMES_HOME
subprocess.run(["hermes", "gateway", "run"], env=env, check=True)
