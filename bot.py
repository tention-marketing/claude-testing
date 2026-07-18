# v6 - auto-restore skills + memory from GitHub on fresh deploy
import os, subprocess, sys, json, shutil
from pathlib import Path

HERMES_HOME = os.environ.get("HERMES_HOME", "/app/data")
os.makedirs(HERMES_HOME, exist_ok=True)

_d_key = "DISCORD_" + "BOT_TOKEN"
_a_key = "ANTHROPIC_" + "API_KEY"
DISCORD_TOKEN = os.environ.get(_d_key, "")
ANTHROPIC_KEY = os.environ.get(_a_key, "")

# ── 1. Write config.yaml (always overwrite — no secrets here) ──────────────
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
  - memory
  - file
"""
with open(f"{HERMES_HOME}/config.yaml", "w") as f:
    f.write(config)
print("✅ config.yaml written")

# ── 2. Write auth.json ONLY if it doesn't exist (protect live tokens) ───────
auth_path = f"{HERMES_HOME}/auth.json"
if not os.path.exists(auth_path):
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
    with open(auth_path, "w") as f:
        json.dump(auth, f)
    print("✅ auth.json created (fresh deploy)")
else:
    # Update only the anthropic key, preserve all other tokens (Spotify, etc.)
    with open(auth_path) as f:
        auth = json.load(f)
    if "credential_pool" not in auth:
        auth["credential_pool"] = {}
    auth["credential_pool"]["anthropic"] = [{
        "id": "railway",
        "label": "railway_key",
        "auth_type": "api_key",
        "priority": 0,
        "source": "env:ANTHROPIC_API_KEY",
        "access_token": ANTHROPIC_KEY,
        "last_status": "ok"
    }]
    with open(auth_path, "w") as f:
        json.dump(auth, f)
    print("✅ auth.json updated (Anthropic key refreshed, other tokens preserved)")

# ── 3. Write .env ────────────────────────────────────────────────────────────
# GATEWAY_ALLOW_ALL_USERS is intentionally NOT set here — access is gated by
# config.yaml's pairing.approved_users list. Setting it to true bypasses that
# allowlist entirely, letting any Discord user talk to (and instruct) the bot.
with open(f"{HERMES_HOME}/.env", "w") as f:
    f.write("")

# ── 4. Copy SOUL.md ──────────────────────────────────────────────────────────
soul_src = "/app/SOUL.md"
soul_dst = f"{HERMES_HOME}/SOUL.md"
if os.path.exists(soul_src):
    shutil.copy(soul_src, soul_dst)
    print("✅ SOUL.md copied")

# ── 5. Restore skills from GitHub → volume (ONLY if skill doesn't exist) ────
# This means: fresh deploy = full restore | running bot = volume wins
GITHUB_DATA = "/app/data_github"  # skills/memories bundled in image at this path

def restore_from_github(src_dir, dst_dir, label):
    if not os.path.exists(src_dir):
        print(f"⚠️  No {label} found in image at {src_dir} — skipping restore")
        return
    os.makedirs(dst_dir, exist_ok=True)
    restored = 0
    for root, dirs, files in os.walk(src_dir):
        # Skip hidden/internal dirs
        dirs[:] = [d for d in dirs if not d.startswith('.curator')]
        for file in files:
            if file.endswith('.lock'):
                continue
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(src_file, src_dir)
            dst_file = os.path.join(dst_dir, rel_path)
            if not os.path.exists(dst_file):
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy2(src_file, dst_file)
                restored += 1
    print(f"✅ {label}: {restored} new files restored from GitHub")

restore_from_github(
    f"{GITHUB_DATA}/skills",
    f"{HERMES_HOME}/skills",
    "Skills"
)
restore_from_github(
    f"{GITHUB_DATA}/memories",
    f"{HERMES_HOME}/memories",
    "Memories"
)

# ── 6. Start Hermes ──────────────────────────────────────────────────────────
print("🚀 Starting Hermes gateway...")
env = os.environ.copy()
env["HERMES_HOME"] = HERMES_HOME
subprocess.run(["hermes", "gateway", "run"], env=env, check=True)
