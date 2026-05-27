---
name: discord-server-admin
description: "Discord server admin via bot REST API: create channels, roles, manage permissions across a guild."
triggers:
  - create a discord channel
  - create a role in discord
  - add role to all channels
  - manage discord server permissions
  - discord bot admin
  - update discord channel permissions
  - read messages from discord channel
  - fetch discord channel history
  - what's in the hermes-channel
  - send a message to every channel
  - broadcast to all channels
  - send an image to discord
  - replicate a discord server structure
  - create a category with channels
  - mention everyone in discord
---

# Discord Server Admin via Bot API

Manage a Discord guild (channels, categories, roles, permissions) using the bot token from Hermes config and the Discord REST API v10.

## Setup

Bot token lives in Hermes config:

    cat ~/.hermes/config.yaml | grep -i discord -A 10

Extract the token value. Guild ID comes from listing the bot's guilds:

    curl -s -H "Authorization: Bot TOKEN" https://discord.com/api/v10/users/@me/guilds

## Core Reference IDs (Rajeev's server)

- Guild ID: 1432708001868812401
- Hermes Agent role ID: 1503659544335745088
- Category "churn-client-testing" ID: 1470608471597777170

See references/rajeev-discord-ids.md for a full channel/role ID map.
See scripts/discord_sync.py for the ready-to-run incremental message sync script (runs every 5m via cron job 'discord-channel-sync').

## Step-by-Step Workflows

### 1. List all channels (with types)

    curl -s -H "Authorization: Bot TOKEN" \
      https://discord.com/api/v10/guilds/GUILD_ID/channels

Channel types: 0 = text, 2 = voice, 4 = category.

### 2. Create a text channel inside a category

    curl -s -X POST \
      -H "Authorization: Bot TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"name":"channel-name","type":0,"parent_id":"CATEGORY_ID"}' \
      https://discord.com/api/v10/guilds/GUILD_ID/channels

### 3. Create a role

    curl -s -X POST \
      -H "Authorization: Bot TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"name":"Members","permissions":"0","color":3447003,"hoist":false,"mentionable":true}' \
      https://discord.com/api/v10/guilds/GUILD_ID/roles

### 4. Add role permission overwrite to a channel

Permission bits: VIEW_CHANNEL=1024, SEND_MESSAGES=2048, READ_MESSAGE_HISTORY=65536. Sum them for ALLOW value.

    curl -s -X PUT \
      -H "Authorization: Bot TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"allow":"68608","deny":"0","type":0}' \
      https://discord.com/api/v10/channels/CHANNEL_ID/permissions/ROLE_ID

type 0 = role, type 1 = member.

### 5. Loop across all text channels (Python)

```python
import json
from hermes_tools import terminal

TOKEN = "..."
GUILD_ID = "..."
ROLE_ID = "..."
ALLOW_PERMS = str(1024 + 2048 + 65536)

result = terminal(f'curl -s -H "Authorization: Bot {TOKEN}" https://discord.com/api/v10/guilds/{GUILD_ID}/channels')
channels = json.loads(result['output'])
text_channels = [ch for ch in channels if ch['type'] == 0]

for ch in text_channels:
    payload = json.dumps({"allow": ALLOW_PERMS, "deny": "0", "type": 0})
    res = terminal(f'''curl -s -o /dev/null -w "%{{http_code}}" -X PUT \
      -H "Authorization: Bot {TOKEN}" \
      -H "Content-Type: application/json" \
      -d '{payload}' \
      https://discord.com/api/v10/channels/{ch["id"]}/permissions/{ROLE_ID}''')
    print(f"{'OK' if res['output'].strip() == '204' else 'FAIL'} | #{ch['name']}")
```

### 6. Create a category

    curl -s -X POST \
      -H "Authorization: Bot TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"name":"Category Name","type":4}' \
      https://discord.com/api/v10/guilds/GUILD_ID/channels

type 4 = category. Returns id, name, position. Use the returned id as parent_id when creating channels inside it.

### 7. Assign a role to ALL guild members (bulk)

Fetch all members first (limit 100), then PUT the role onto each:

```python
import json, time
from hermes_tools import terminal

TOKEN = "..."
GUILD_ID = "..."
ROLE_ID = "..."

result = terminal(f'curl -s -H "Authorization: Bot {TOKEN}" "https://discord.com/api/v10/guilds/{GUILD_ID}/members?limit=100"')
members = json.loads(result['output'])

for m in members:
    uid = m['user']['id']
    uname = m['user']['username']
    res = terminal(f'curl -s -o /dev/null -w "%{{http_code}}" -X PUT -H "Authorization: Bot {TOKEN}" -H "Content-Type: application/json" "https://discord.com/api/v10/guilds/{GUILD_ID}/members/{uid}/roles/{ROLE_ID}"')
    status = res['output'].strip()
    print(f"  {uname}: {'OK' if status == '204' else 'Failed (' + status + ')'}")
    time.sleep(0.5)  # avoid rate limits
```

HTTP 204 = success. Add time.sleep(0.5) between calls to avoid rate limiting.

### 8. Send an image/file to a channel

Use multipart form upload — NOT JSON. JSON payload cannot carry binary attachments.

    curl -s -X POST \
      -H "Authorization: Bot TOKEN" \
      -F "file=@/path/to/image.png" \
      "https://discord.com/api/v10/channels/CHANNEL_ID/messages"

HTTP 200 = success. Works for PNG, JPG, GIF, PDF, etc.

To send image + text together:

    curl -s -X POST \
      -H "Authorization: Bot TOKEN" \
      -F "file=@/path/to/image.png" \
      -F 'payload_json={"content":"Caption here"}' \
      "https://discord.com/api/v10/channels/CHANNEL_ID/messages"

### 9. Send a message mentioning a role

    curl -s -X POST \
      -H "Authorization: Bot TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"content":"Hello everyone, <@&ROLE_ID>","allowed_mentions":{"parse":["roles"]}}' \
      https://discord.com/api/v10/channels/CHANNEL_ID/messages

Use allowed_mentions.parse to control which mention types actually ping. Options: "roles", "users", "everyone".

### 10. Broadcast a message to ALL text channels in a guild

Always use `@everyone` mention + `allowed_mentions` so Discord actually pings. Without `allowed_mentions`, the @everyone text renders but does NOT ping.

```python
import json, time, shlex
from hermes_tools import terminal

TOKEN = "..."
GUILD_ID = "..."

result = terminal(f'curl -s -H "Authorization: Bot {TOKEN}" "https://discord.com/api/v10/guilds/{GUILD_ID}/channels"')
channels = json.loads(result['output'])
text_channels = [c for c in channels if c['type'] == 0]

payload = json.dumps({
    "content": "@everyone Hey everyone, ready for the meeting? It's 9am EST!",
    "allowed_mentions": {"parse": ["everyone"]}
})
quoted = shlex.quote(payload)

for ch in text_channels:
    res = terminal(f'curl -s -o /dev/null -w "%{{http_code}}" -X POST -H "Authorization: Bot {TOKEN}" -H "Content-Type: application/json" -d {quoted} "https://discord.com/api/v10/channels/{ch["id"]}/messages"')
    status = res['output'].strip()
    print(f"  #{ch['name']}: {'OK' if status == '200' else 'FAIL (HTTP ' + status + ')'}")
    time.sleep(0.5)
```

403 on some channels = bot lacks VIEW_CHANNEL or SEND_MESSAGES on those channels. Note which ones failed and report to user — cannot self-grant permissions.

### 11. Replicate a channel structure from a screenshot/image

When the user shares a screenshot of another Discord server's channel list, read the category name and all channel names visible, then recreate them exactly. If the screenshot shows lock icons (🔒) next to channels, create them as **private** (deny @everyone VIEW_CHANNEL). When in doubt, default to private — it's easier to open a private channel than to accidentally expose a public one.

1. Create the category (type 4) first — capture returned `id`
2. Create each channel (type 0) with `parent_id` set to the category id
3. Channel names are case-sensitive; preserve hyphens and spaces exactly as shown

```python
import json, time, shlex
from hermes_tools import terminal

TOKEN = "..."
GUILD_ID = "..."

category_payload = shlex.quote(json.dumps({"name": "CATEGORY NAME", "type": 4}))
cat = terminal(f'curl -s -X POST -H "Authorization: Bot {TOKEN}" -H "Content-Type: application/json" -d {category_payload} "https://discord.com/api/v10/guilds/{GUILD_ID}/channels"')
category_id = json.loads(cat['output'])['id']

channels = ["channel-one", "channel-two", "channel-three"]
for name in channels:
    ch_payload = shlex.quote(json.dumps({"name": name, "type": 0, "parent_id": category_id}))
    res = terminal(f'curl -s -X POST -H "Authorization: Bot {TOKEN}" -H "Content-Type: application/json" -d {ch_payload} "https://discord.com/api/v10/guilds/{GUILD_ID}/channels"')
    data = json.loads(res['output'])
    print(f"  #{data['name']} created (ID: {data['id']})")
    time.sleep(0.5)
```

### 12. Read ALL messages from every channel (full history scan)

Before any destructive action (deleting channels, cleanup), always read the FULL message history of every channel and save to disk. Never rely on a 1-message peek — it will miss things.

```python
import json, re, time, subprocess

TOKEN = "..."
GUILD_ID = "..."
DATA_FILE = "/tmp/all_channel_messages.json"

def fetch_batch(channel_id, after=None):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages?limit=100"
    if after:
        url += f"&after={after}"
    result = subprocess.run(
        ['curl', '-s', '-H', f'Authorization: Bot {TOKEN}', url],
        capture_output=True, text=True
    )
    raw_clean = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', result.stdout)
    return json.loads(raw_clean)

# Get channels
channels_raw = subprocess.run(
    ['curl', '-s', '-H', f'Authorization: Bot {TOKEN}',
     f'https://discord.com/api/v10/guilds/{GUILD_ID}/channels'],
    capture_output=True, text=True
).stdout
channels = json.loads(channels_raw)
cat_map = {ch['id']: ch['name'] for ch in channels if ch['type'] == 4}
text_channels = [ch for ch in channels if ch['type'] in [0, 5]]

all_data = {}
for ch in text_channels:
    ch_id = ch['id']
    messages = []
    after = None
    while True:
        batch = fetch_batch(ch_id, after=after)
        if not isinstance(batch, list) or len(batch) == 0:
            break
        messages.extend(batch)
        if len(batch) < 100:
            break
        after = batch[0]['id']   # newest → paginate forward
        time.sleep(0.2)
    all_data[ch_id] = {
        'name': ch['name'],
        'category': cat_map.get(ch.get('parent_id', ''), 'No Category'),
        'id': ch_id,
        'messages': messages
    }
    print(f"#{ch['name']}: {len(messages)} messages")

with open(DATA_FILE, 'w') as f:
    json.dump(all_data, f, indent=2)
```

PITFALL: Messages contain control characters that break `json.loads()`. Always strip `[\x00-\x08\x0b\x0c\x0e-\x1f]` before parsing. Write to file via subprocess curl rather than passing through Python string to avoid encoding issues.

PITFALL: Use `subprocess.run(['curl', ...])` not `terminal(f'curl ... | python3 ...')` — shell f-string escaping with embedded Python is fragile. Save API response to file first, then parse in Python.

### 13. Auto-sync new messages via cron

To keep channel data always fresh, deploy a sync script + cron job. Script lives at `/home/rajeev/.hermes/scripts/discord_sync.py`. It fetches only NEW messages (using `?after=<last_known_id>`) and appends them to the saved JSON.

Set up via Hermes cron:
```
hermes cron create --name discord-channel-sync --schedule "every 5m" --script discord_sync.py --no-agent
```

Or use `mcp_cronjob` tool with `deliver=local`, `no_agent=true`, `schedule="every 5m"`.

Log file: `/home/rajeev/.hermes/discord_backup/sync.log`

**Permanent backup location:** `/home/rajeev/.hermes/discord_backup/all_channel_messages.json`
Save ALL message data here, not `/tmp` — /tmp is wiped on restart. If a channel is accidentally deleted, this file is the recovery source. The cron job ID is `f5973a47ca58` (job name: `discord-channel-sync`).

### 14. Pin a message in a channel

    curl -s -X PUT \
      -H "Authorization: Bot TOKEN" \
      -H "Content-Length: 0" \
      "https://discord.com/api/v10/channels/CHANNEL_ID/pins/MESSAGE_ID"

Empty response (204) = success. Get MESSAGE_ID from the message object's `id` field. The bot needs MANAGE_MESSAGES permission to pin.

PITFALL: Requires `Content-Length: 0` header — omitting it causes some curl versions to hang.

### 16. Find voice messages and audio files in a channel

Discord voice messages are stored differently depending on whether they are native or forwarded:

- **Native voice message**: `flags & 8192`, attachment is in the top-level `attachments[]` array.
- **Forwarded voice message**: `flags & 16384`, attachment is buried inside `message_snapshots[0].message.attachments[]` — NOT in the top-level `attachments[]`.

A search that only checks `attachments[]` will miss forwarded voice messages entirely and falsely report "no audio found". Always check **both** locations.

```python
import json
from hermes_tools import terminal

TOKEN = "..."
GUILD_ID = "..."

# Get all text channels
r = terminal(f'curl -s -H "Authorization: Bot {TOKEN}" "https://discord.com/api/v10/guilds/{GUILD_ID}/channels"')
channels = [ch for ch in json.loads(r['output']) if ch['type'] == 0]

found_audio = []
audio_exts = ['.mp3', '.ogg', '.wav', '.m4a', '.aac', '.flac', '.opus', '.webm']

for ch in channels:
    r = terminal(f'curl -s -H "Authorization: Bot {TOKEN}" "https://discord.com/api/v10/channels/{ch["id"]}/messages?limit=50"')
    msgs = json.loads(r['output'])
    if not isinstance(msgs, list):
        continue
    for m in msgs:
        author = m.get('author', {}).get('username', 'unknown')

        # 1. Native voice message (flag 8192) or plain audio attachment
        for a in m.get('attachments', []):
            fname = a.get('filename', '')
            ctype = a.get('content_type', '')
            if any(ext in fname.lower() for ext in audio_exts) or 'audio' in ctype:
                found_audio.append((ch['name'], fname, a.get('url'), author, 'native'))

        # 2. Forwarded voice message (flag 16384) — attachment in message_snapshots
        if m.get('flags', 0) & 16384:
            for snap in m.get('message_snapshots', []):
                for a in snap.get('message', {}).get('attachments', []):
                    fname = a.get('filename', '')
                    ctype = a.get('content_type', '')
                    if any(ext in fname.lower() for ext in audio_exts) or 'audio' in ctype:
                        found_audio.append((ch['name'], fname, a.get('url'), author, 'forwarded'))

for ch_name, fname, url, author, kind in found_audio:
    print(f"#{ch_name} [{kind}] {fname} by {author}")
    print(f"  URL: {url}")
```

PITFALL: Forwarded voice messages have **empty top-level `attachments[]`**. The only way to find the audio URL is via `message_snapshots[0].message.attachments[0].url`. Never declare "no audio found" until you have checked both paths across all channels.

PITFALL: The audio CDN URL has a short-lived `ex=` expiry parameter. Download the file immediately after finding it — don't save the URL for later.

To download and transcribe once you have the URL:
```bash
curl -sL "CDN_URL" -o /tmp/voice-message.ogg
ffmpeg -y -i /tmp/voice-message.ogg /tmp/voice-message.mp3
# Then transcribe with whisper (install: pip install openai-whisper)
python3 -c "import whisper; m=whisper.load_model('base'); print(m.transcribe('/tmp/voice-message.mp3')['text'])"
```

### 15. Read recent messages from a channel

    curl -s -H "Authorization: Bot TOKEN" \
      "https://discord.com/api/v10/channels/CHANNEL_ID/messages?limit=20"

Returns a JSON array of message objects (most-recent first). Key fields: `author.username`, `content`, `timestamp`. Reverse the array for chronological order.

Python pattern:

```python
import json
from hermes_tools import terminal

TOKEN = "..."
CHANNEL_ID = "..."

result = terminal(f'curl -s -H "Authorization: Bot {TOKEN}" "https://discord.com/api/v10/channels/{CHANNEL_ID}/messages?limit=20"')
messages = json.loads(result['output'])

# Check for access error before iterating
if isinstance(messages, dict) and 'code' in messages:
    print("Error:", messages)
else:
    for msg in reversed(messages):
        print(f"[{msg['timestamp'][:19]}] {msg['author']['username']}: {msg['content']}")
```

PITFALL: if the response is `{"message": "Missing Access", "code": 50001}`, the bot's role does not have VIEW_CHANNEL permission on that channel. The channel has an explicit deny on @everyone and the bot's role is not in the allow list. Fix: in Discord UI, go to the channel > Edit Channel > Permissions > add the Hermes Agent role and allow View Channel + Read Message History. The bot cannot grant itself permission via API.

## Pitfalls

### @everyone text does not ping without allowed_mentions
Writing `@everyone` in the `content` field is NOT enough. Discord suppresses the ping unless you explicitly pass:
```json
{"allowed_mentions": {"parse": ["everyone"]}}
```
This is the most common mistake when broadcasting meeting reminders or announcements. Always include `allowed_mentions`.

### Sending images: use multipart, not JSON
`-d '{"content":"..."}` cannot carry binary files. Use `-F "file=@path"` for image/file uploads. Mixing JSON content with a file requires a second `-F 'payload_json=...'` field.

### 403 on channel permission updates (role hierarchy)
Discord rule: a bot can only manage roles/permissions for roles that sit BELOW it in the server hierarchy. If the bot's role is at position 1 (same or lower than target role), all PUT /permissions calls return 403.

FIX: Server owner must manually drag the Hermes Agent role to the TOP of the role list in Server Settings > Roles. The bot cannot move its own role via API.

When bulk-granting a new role access to all channels, expect ~50% failure rate on channels the bot doesn't already have access to (50001 Missing Access). Report which channels succeeded and which failed, then ask the user to elevate the bot role in Discord UI so retries can be done.

### Bot CAN manage Discord server via API — do not refuse
The bot has full Discord REST API v10 access via the token in `~/.hermes/config.yaml`. It CAN: create channels, create roles, set permissions, bulk-grant role access. Do NOT tell the user it cannot do these things. The only real blocker is the bot's role hierarchy position for permission management — which is fixable by the server owner.

### Checking bot permissions
    curl -s -H "Authorization: Bot TOKEN" https://discord.com/api/v10/guilds/GUILD_ID/members/BOT_USER_ID

Permission bits to check:
- ADMINISTRATOR: 1 << 3
- MANAGE_CHANNELS: 1 << 4
- MANAGE_ROLES: 1 << 28

### ALWAYS read full message history before deleting any channel
Never delete a channel after checking only the last 1 message. Always run a full paginated scan (Workflow #12) across ALL channels first, save to disk, then confirm which channels are truly empty. Discord channel deletion is permanent — no recycle bin, no undo, even Discord support cannot recover messages.

Safe duplicate-deletion workflow:
1. List all channels → identify duplicates by name
2. Full message scan → save to **permanent** location `/home/rajeev/.hermes/discord_backup/all_channel_messages.json` (NOT /tmp — that is lost on restart)
3. Report to user: which channels have messages, which are empty, which to keep/delete
4. Only delete after explicit user confirmation per-channel (ask "delete both?" for pairs)
5. Keep channels with messages; delete only confirmed-empty ones
6. After deletion, tell user which were deleted and remind them backup is safe

### Private channels block DELETE even with guild-level Manage Channels
If a channel has `permission_overwrites` that deny @everyone VIEW_CHANNEL (`1024`), the bot cannot see or delete the channel — even if its role has MANAGE_CHANNELS at the guild level. The API returns `{"message": "Missing Access", "code": 50001}`.

Diagnosis: fetch `/guilds/GUILD_ID/channels`, look at `permission_overwrites` on the target channel. If `deny` includes `1024` and the bot's role/user ID is not in the allow list, it's blocked.

Fix options:
- Ask user to delete the channel manually in Discord UI (fastest for one-offs)
- Ask user to add Hermes Agent to the channel's permissions with View Channel ON, then retry DELETE

The bot CANNOT grant itself permission via API on a channel it can't already see.

### Deleting a channel requires Manage Channels permission
Bot needs MANAGE_CHANNELS (`1 << 4`) on the guild or the specific channel. Without it, DELETE /channels/CHANNEL_ID returns `{"message": "Missing Access", "code": 50001}`. Fix: server owner grants the bot role Manage Channels in Server Settings > Roles, or in the specific channel's permission overrides.

### PATCH /roles returns a dict not a list on error
When role position update fails, the response is a dict {"message":...,"code":...} not a list. Always check isinstance(resp, list) before iterating.

### Role position update (bot cannot self-elevate)
PATCH /guilds/GUILD_ID/roles to reorder returns 403 if the bot tries to move itself above its current position. Only the server owner can do this via UI.

## Hermes-as-Discord-bot capability
Everything executable from the terminal/CLI can also be triggered directly from Discord by @mentioning the bot in any channel. The bot has the same tool access. Users can say "@Hermes create a channel called X inside Y category" directly in Discord.

Config key: `require_mention: true` means the bot only acts when @mentioned. The channel set in `free_response_channels` can talk to the bot without @mention.
