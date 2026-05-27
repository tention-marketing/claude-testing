#!/usr/bin/env python3
"""
Discord channel message sync script.
Fetches all new messages since last run and appends to saved data.
Set DISCORD_BOT_TOKEN environment variable before running.
"""
import json, re, os, time, subprocess
from datetime import datetime

TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")
if not TOKEN:
    raise ValueError("Set DISCORD_BOT_TOKEN environment variable")
GUILD_ID = "1432708001868812401"
DATA_FILE = "/home/rajeev/.hermes/discord_backup/all_channel_messages.json"
LOG_FILE = "/home/rajeev/.hermes/discord_backup/sync.log"

def api(path):
    result = subprocess.run(
        ['curl', '-s', '-H', f'Authorization: Bot {TOKEN}',
         f'https://discord.com/api/v10{path}'],
        capture_output=True, text=True
    )
    raw = result.stdout
    raw_clean = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', raw)
    return json.loads(raw_clean)

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{ts}] {msg}\n")
    print(f"[{ts}] {msg}")

# Load existing data
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
if os.path.exists(DATA_FILE):
    with open(DATA_FILE) as f:
        all_data = json.load(f)
else:
    all_data = {}

# Get all channels
channels = api(f"/guilds/{GUILD_ID}/channels")
cat_map = {ch['id']: ch['name'] for ch in channels if ch['type'] == 4}
text_channels = [ch for ch in channels if ch['type'] in [0, 5]]

new_total = 0

for ch in text_channels:
    ch_id = ch['id']
    ch_name = ch['name']
    parent = cat_map.get(ch.get('parent_id', ''), 'No Category')

    existing = all_data.get(ch_id, {'name': ch_name, 'category': parent, 'id': ch_id, 'messages': []})
    existing_ids = {m['id'] for m in existing['messages']}

    # Get newest message id we already have — fetch only newer messages
    after = None
    if existing['messages']:
        after = max(existing['messages'], key=lambda m: m['id'])['id']

    new_msgs = []
    while True:
        url = f"/channels/{ch_id}/messages?limit=100"
        if after:
            url += f"&after={after}"

        try:
            batch = api(url)
        except Exception as e:
            log(f"ERROR fetching #{ch_name}: {e}")
            break

        if not isinstance(batch, list) or len(batch) == 0:
            break

        fresh = [m for m in batch if m['id'] not in existing_ids]
        new_msgs.extend(fresh)
        existing_ids.update(m['id'] for m in fresh)

        if len(batch) < 100:
            break
        after = batch[0]['id']  # newest for next page
        time.sleep(0.2)

    if new_msgs:
        existing['messages'].extend(new_msgs)
        new_total += len(new_msgs)
        log(f"#{ch_name} ({parent}): +{len(new_msgs)} new messages")

    existing['name'] = ch_name
    existing['category'] = parent
    all_data[ch_id] = existing

# Save updated data
with open(DATA_FILE, 'w') as f:
    json.dump(all_data, f, indent=2)

log(f"Sync complete. {new_total} new messages saved. Total channels: {len(all_data)}")