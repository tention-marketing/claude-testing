---
name: spotify-integration
description: Complete Spotify integration for Hermes — Developer App setup, PKCE OAuth auth, playback control, token refresh, device management, cron alarm, and API patterns.
tags: [spotify, integration, music, api, setup, oauth, pkce, playback, devices, cron]
triggers:
  - "connect spotify"
  - "spotify setup"
  - "play a song"
  - "search spotify"
  - "spotify client id"
  - "spotify client secret"
  - "spotify auth"
  - "spotify token"
  - "spotify not working"
  - "wake up alarm spotify"
  - "play music at"
  - "spotify re-authenticate"
---

# Spotify Integration

## When to Load
Any time Rajeev asks to connect Spotify, play/search music, or configure Spotify credentials.

---

## Step 1 — Spotify Developer App Setup

Direct Rajeev to: https://developer.spotify.com/dashboard

### Create App form — recommended values:
| Field | Value |
|---|---|
| Name | `Tention Marketing Bot` |
| Description | `Internal bot for searching and playing music via Spotify` |
| Website | `https://tention.co` |
| Redirect URI | `http://127.0.0.1:8888/callback` |
| API Type | **Web API** (not Android, not iOS) |

### ⚠️ REDIRECT URI PITFALL (Spotify rule since April 2025)
- ❌ `http://localhost:8888/callback` — **NOT ALLOWED** (localhost banned)
- ✅ `http://127.0.0.1:8888/callback` — **CORRECT** (explicit IPv4 loopback)
- Spotify enforces HTTPS for all non-loopback URIs
- For loopback addresses, HTTP is permitted
- See: references/spotify-redirect-uri-rules.md

---

## Step 2 — Account Setup Note

If Rajeev's Spotify account uses a **phone number** (no email):
- He must add an email to his account before accessing the Developer Dashboard
- Path: Spotify App → Settings → Account → "Add email address"
- This does NOT affect subscription or data

---

## Step 3 — Configure Credentials in Hermes

Once Rajeev has Client ID and Client Secret:

```bash
hermes config set spotify.client_id "CLIENT_ID_HERE"
hermes config set spotify.client_secret "CLIENT_SECRET_HERE"
hermes config set spotify.redirect_uri "http://127.0.0.1:8888/callback"
```

---

## Step 4 — Enable Spotify Toolset

```bash
hermes tools list | grep -i spotify   # check current status
hermes tools enable spotify           # enable if disabled
```

---

## Step 5 — Authorize Spotify Account

After enabling, follow the PKCE auth flow below. Key points:
- Correct command: `hermes auth spotify login` (NOT `hermes spotify auth` — that does not exist)
- Bot runs on Railway: redirect listener output to `/tmp/spotify_out.txt`, read the auth URL from that file, send it to user, then curl their callback URL on the server
- **Do NOT start a new listener after the user approves** — the existing one must still be running when you curl the callback or state will mismatch
- **Do NOT ask user to paste callback URL and then start a fresh listener** — the state will be different and auth will fail with `state mismatch` or `invalid_grant: code_verifier was incorrect`
- **Authorization codes are single-use** — if you curl a callback URL that was obtained from a *previous* listener run (even one that was killed), Spotify returns `invalid_grant`. The only fix is: fresh listener → new auth URL → user approves → immediately curl that callback. No reuse of old codes ever.

### ✅ The Only Working Sequence (Railway remote server)

This is the exact order — do NOT deviate:

1. Kill any existing processes on port 8888:
   ```bash
   inode=$(cat /proc/net/tcp | grep "22B8" | awk '{print $10}')
   for pid in $(ls /proc | grep '^[0-9]'); do
     ls -la /proc/$pid/fd/ 2>/dev/null | grep -q "socket:\[$inode\]" && kill -9 $pid && echo "Killed $pid"
   done
   ```
2. Confirm port is free: `cat /proc/net/tcp | awk '$4=="0A"' | grep "22B8"` → must return empty
3. Start listener: `hermes auth spotify login --no-browser --redirect-uri "http://127.0.0.1:8888/callback" --timeout 120 > /tmp/spotify_out.txt 2>&1` (background=True)
4. Wait 4s, read auth URL: `cat /tmp/spotify_out.txt` — extract the full `https://accounts.spotify.com/authorize?...` URL and the `state=` value
5. Send user the auth URL — tell them to click, approve, then **copy the full URL from their browser address bar** (it will show `http://127.0.0.1:8888/callback?code=...&state=...`)
6. When user pastes that URL: **BEFORE curling**, verify the `state=` in their URL matches the `state=` in the auth URL you sent in step 4. If states differ, the listener has restarted or the user approved an old link — start over from step 1 immediately.
7. If states match: **immediately** curl it from the server — the listener must still be running
8. Check output: `<html><body><h1>Spotify authorization received.</h1>` = success
9. Verify: `hermes auth spotify status` → should show logged in

### ⚠️ Why Users Say "done" But Auth Fails
Rajeev's phone browser cannot reach `127.0.0.1:8888` on the Railway server. So saying "done" is NOT enough — the callback never reaches the server. He MUST paste the full redirect URL from his browser address bar.

**Always say this BEFORE sending the auth link — every single time:**
> "After you tap Agree, your browser will show an error page — that's completely normal. The most important thing: look at the address bar at the top of your browser, it will show a long URL starting with `http://127.0.0.1:8888/callback?code=...`. Long-press that URL, select all, copy it, and paste the whole thing here. Do NOT just say 'done' — I need the actual URL."

If Rajeev says "done" without pasting a URL, immediately remind him: *"I need the full URL from your browser address bar, not just 'done' — can you paste it here?"*

> ⚠️ **Rajeev consistently says "done" or "check" without pasting the URL** — this happened multiple times in the same session. Do not proceed or say "still waiting" more than once. After the second "done" without a URL, proactively say: "I can see you've approved it! I just need you to copy the URL from your browser address bar and paste it here. It starts with `http://127.0.0.1:8888/callback?code=...`"

### Rajeev's Known Spotify Account & Devices (as of June 2026)
- **Spotify account name**: Rajput
- **Developer App name**: teting (created June 2026)
- **Device 1**: Rajeev's MacBook Pro | ID: `6bb75732f2edc46f7cc193d7add1811d7efa0186` | Type: Computer
- **Device 2**: Galaxy A35 5G | ID: `dca9712f11444ac997f258f36b9ce9f910ca5d31` | Type: Smartphone
- **Always check active devices first** via `/me/player/devices` before sending play commands — the active device changes depending on which has Spotify open. Never hardcode device ID without checking.
- **Preferred music**: Bollywood/Hindi songs — Arijit Singh, Mika Singh, Himesh Reshammiya. When asked to play a song by an Indian artist, search with `market=IN` for best results.
- **Volume control (403 on Free)**: Setting volume via `/me/player/volume` returns 403 on Spotify Free accounts — this is expected. Playback still works fine; just skip volume commands or note it gracefully.

### Spotify as Wake-Up Alarm (Cron Pattern)
Rajeev uses Spotify + cron for a daily 8am IST wake-up alarm. The alarm cron job:
1. Refreshes the token (always — tokens expire in 3600s)
2. Plays a specific album/artist URI on the Galaxy A35 5G
3. Sends a Discord message as a wake-up ping

**Alarm Clock Sound album URI**: `spotify:album:2BSXZv0v8qluXEXuk2QwYp` (confirmed working June 2026)
**Cron schedule for 8am IST**: `30 2 * * *` (2:30am UTC = 8:00am IST)

> ⚠️ The cron alarm only works if Spotify is open/active on the phone at 8am. If the device isn't active, playback returns 404. The cron job should send a Discord message regardless so Rajeev gets a notification either way.

---

## Step 6 (Last Resort): Manual PKCE Fallback

If `hermes auth spotify login` fails 2+ times with state mismatch or `invalid_grant`, **bypass the hermes listener entirely** using a manual PKCE flow:

1. Generate your own `code_verifier`, `code_challenge`, and `state` using Python and save to `/tmp/spotify_pkce.json`
2. Build the Spotify authorize URL manually with those values
3. Send user the URL — they approve and paste the callback URL
4. POST directly to `https://accounts.spotify.com/api/token` with the code + verifier
5. Save the returned tokens directly into `/app/data/auth.json` under `providers.spotify`

**Key advantage**: No timing dependency — the verifier is saved to disk and can be used whenever the user pastes the callback URL, even minutes later.

### Manual PKCE — Step-by-step

#### 6a. Generate PKCE verifier + auth URL
```python
import base64, hashlib, secrets, urllib.parse, json

code_verifier = secrets.token_urlsafe(64)
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b'=').decode()
state = secrets.token_hex(16)

with open('/tmp/spotify_pkce.json', 'w') as f:
    json.dump({'code_verifier': code_verifier, 'state': state}, f)

params = {
    'client_id': 'YOUR_CLIENT_ID',
    'response_type': 'code',
    'redirect_uri': 'http://127.0.0.1:8888/callback',
    'scope': 'user-modify-playback-state user-read-playback-state user-read-currently-playing user-read-recently-played playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private user-library-read user-library-modify',
    'state': state,
    'code_challenge_method': 'S256',
    'code_challenge': code_challenge,
}
print('https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(params))
```

#### 6b. Send user the auth URL, get callback URL back

#### 6c. Exchange the code for tokens
```python
import json, urllib.request, urllib.parse

with open('/tmp/spotify_pkce.json', 'r') as f:
    pkce = json.load(f)

callback_url = 'PASTE_FULL_CALLBACK_URL_HERE'
params = urllib.parse.parse_qs(urllib.parse.urlparse(callback_url).query)
code = params['code'][0]

data = urllib.parse.urlencode({
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': 'http://127.0.0.1:8888/callback',
    'client_id': 'YOUR_CLIENT_ID',
    'code_verifier': pkce['code_verifier'],
}).encode()

req = urllib.request.Request(
    'https://accounts.spotify.com/api/token',
    data=data,
    headers={'Content-Type': 'application/x-www-form-urlencoded'},
    method='POST'
)
with urllib.request.urlopen(req) as resp:
    tokens = json.loads(resp.read())
    with open('/tmp/spotify_tokens.json', 'w') as f:
        json.dump(tokens, f)
    print("SUCCESS! Access token:", tokens['access_token'][:30], "...")
```

#### 6d. Save tokens into Hermes auth.json
```python
import json, time

with open('/tmp/spotify_tokens.json', 'r') as f:
    tokens = json.load(f)
with open('/app/data/auth.json', 'r') as f:
    auth = json.load(f)

auth['providers']['spotify'] = {
    'access_token': tokens['access_token'],
    'refresh_token': tokens['refresh_token'],
    'token_type': tokens['token_type'],
    'expires_in': tokens['expires_in'],
    'scope': tokens['scope'],
    'issued_at': time.time(),
    'client_id': 'YOUR_CLIENT_ID',
    'redirect_uri': 'http://127.0.0.1:8888/callback',
}
with open('/app/data/auth.json', 'w') as f:
    json.dump(auth, f, indent=2)
print("Saved!")
```

Then verify: `hermes auth spotify status` → should show `spotify: logged in`

---

## Token Refresh (access tokens expire after 3600s)

When Spotify API calls start returning 401, the access token has expired. Use the stored refresh_token:

```python
import json, urllib.request, urllib.parse, time

with open('/app/data/auth.json') as f:
    auth = json.load(f)
spotify = auth['providers']['spotify']
refresh_token = spotify['refresh_token']
client_id = spotify['client_id']

data = urllib.parse.urlencode({
    'grant_type': 'refresh_token',
    'refresh_token': refresh_token,
    'client_id': client_id,
}).encode()

req = urllib.request.Request(
    'https://accounts.spotify.com/api/token',
    data=data,
    headers={'Content-Type': 'application/x-www-form-urlencoded'},
    method='POST'
)
with urllib.request.urlopen(req) as resp:
    tokens = json.loads(resp.read())

spotify['access_token'] = tokens['access_token']
spotify['issued_at'] = time.time()
if 'refresh_token' in tokens:
    spotify['refresh_token'] = tokens['refresh_token']

with open('/app/data/auth.json', 'w') as f:
    json.dump(auth, f, indent=2)
print("Token refreshed!")
```

---

## Security Warning — Shared Credentials

If Rajeev shares Client ID/Secret in chat (publicly visible):
1. **Immediately warn him** that credentials are exposed
2. Advise: Developer Dashboard → App → Settings → **"Rotate Secret"**
3. Use the new secret in config

---

## Playback & Control API

Since bot runs on Railway (server), Spotify playback commands are sent to Rajeev's **active device** (phone/laptop with Spotify open). Spotify Premium required for playback control.

### Get Active Devices
Always check devices before sending play commands — the device_id is required:
```python
import json, urllib.request
with open('/app/data/auth.json') as f:
    token = json.load(f)['providers']['spotify']['access_token']

req = urllib.request.Request(
    'https://api.spotify.com/v1/me/player/devices',
    headers={'Authorization': f'Bearer {token}'}
)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read())
for d in data['devices']:
    print(d['id'], d['name'], d['type'], 'active:', d['is_active'])
```

### Play a Track by URI
```python
import json, urllib.request
with open('/app/data/auth.json') as f:
    token = json.load(f)['providers']['spotify']['access_token']

device_id = 'DEVICE_ID_HERE'
track_uri = 'spotify:track:TRACK_ID_HERE'

req = urllib.request.Request(
    f'https://api.spotify.com/v1/me/player/play?device_id={device_id}',
    data=json.dumps({'uris': [track_uri]}).encode(),
    headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
    method='PUT'
)
urllib.request.urlopen(req)
```

### Search for Songs
```python
import json, urllib.request, urllib.parse
with open('/app/data/auth.json') as f:
    token = json.load(f)['providers']['spotify']['access_token']

query = urllib.parse.quote('Arijit Singh new 2025')
req = urllib.request.Request(
    f'https://api.spotify.com/v1/search?q={query}&type=track&limit=5&market=IN',
    headers={'Authorization': f'Bearer {token}'}
)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read())
for t in data['tracks']['items']:
    print(t['name'], '—', ', '.join(a['name'] for a in t['artists']), '|', t['uri'])
```

### Pause / Resume Playback
```python
import json, urllib.request
with open('/app/data/auth.json') as f:
    token = json.load(f)['providers']['spotify']['access_token']
device_id = 'DEVICE_ID_HERE'

# ⚠️ Always check player state BEFORE sending pause — pausing an already-paused
# player returns 403 Forbidden. Check is_playing first:
req = urllib.request.Request(
    'https://api.spotify.com/v1/me/player',
    headers={'Authorization': f'Bearer {token}'}
)
with urllib.request.urlopen(req) as resp:
    state = json.loads(resp.read())
    is_playing = state.get('is_playing', False)

if is_playing:
    req2 = urllib.request.Request(
        f'https://api.spotify.com/v1/me/player/pause?device_id={device_id}',
        data=b'',
        headers={'Authorization': f'Bearer {token}'},
        method='PUT'
    )
    urllib.request.urlopen(req2)
    print("Paused.")
else:
    print("Already paused.")
```

### Volume Control
```python
# volume_percent: 0–100
import urllib.request, json
with open('/app/data/auth.json') as f:
    token = json.load(f)['providers']['spotify']['access_token']
device_id = 'DEVICE_ID_HERE'
req = urllib.request.Request(
    f'https://api.spotify.com/v1/me/player/volume?volume_percent=50&device_id={device_id}',
    data=b'',
    headers={'Authorization': f'Bearer {token}'},
    method='PUT'
)
urllib.request.urlopen(req)
```

### Trending Songs Workaround
⚠️ The Spotify `/browse/featured-playlists`, `/browse/new-releases`, and direct access to Spotify editorial playlists (Global Top 50: `37i9dQZEVXbMDoHDwVN2tF`, India Top 50: `37i9dQZEVXbLZ52XmnySJg`) all return **403 Forbidden** with a Developer App (limited quota mode). These endpoints require Spotify's Extended Quota approval.

**Workaround**: Use search with trending-oriented queries instead:
```python
# Search for top hits to surface trending songs
query = urllib.parse.quote('top hits 2026')
# or: 'trending india 2026', 'new releases hindi 2026', etc.
```
This returns real results though not a true chart — set user expectations accordingly.

### Token Storage in auth.json
Tokens are stored at `/app/data/auth.json` under `providers.spotify`. Access pattern:
```python
import json
with open('/app/data/auth.json') as f:
    token = json.load(f)['providers']['spotify']['access_token']
```
Tokens expire in 3600s. If API calls return 401, the token needs refresh via the refresh_token stored in the same location.

### Reference Files
- `references/playback-and-devices.md` — known device IDs, artist/album URIs, cron alarm pattern, Rajeev's music preferences
- `references/spotify-redirect-uri-rules.md` — Spotify redirect URI rules enforced April 2025+

### ⚠️ Shell Interpolation Pitfall — DO NOT use `$(python3 -c "...")` in eval context
On Railway, using `ACCESS_TOKEN=$(python3 -c "import json; ...")` inside a shell command passed through Hermes's eval wrapper causes a syntax error:
```
/usr/bin/bash: eval: line N: syntax error near unexpected token `)'
```
**Always use Python heredoc or inline Python scripts instead**:
```python
# ✅ CORRECT — use python3 heredoc
python3 << 'EOF'
import json, urllib.request
with open('/app/data/auth.json') as f:
    token = json.load(f)['providers']['spotify']['access_token']
# ... rest of API call
EOF
```
Never interpolate the token into shell variables via `$(...)` — keep all Spotify API calls inside Python scripts.

### Get Track Details (release date, duration, etc.)
```python
import json, urllib.request
with open('/app/data/auth.json') as f:
    token = json.load(f)['providers']['spotify']['access_token']

track_id = 'TRACK_ID_HERE'
req = urllib.request.Request(
    f'https://api.spotify.com/v1/tracks/{track_id}?market=IN',
    headers={'Authorization': f'Bearer {token}'}
)
with urllib.request.urlopen(req) as resp:
    track = json.loads(resp.read())

print(f"Name: {track['name']}")
print(f"Artists: {', '.join(a['name'] for a in track['artists'])}")
print(f"Album: {track['album']['name']}")
print(f"Release Date: {track['album']['release_date']}")
duration_ms = track['duration_ms']
print(f"Duration: {duration_ms // 60000}:{(duration_ms % 60000) // 1000:02d}")
```
Note: `track['popularity']` is NOT always present — use `.get('popularity', 'N/A')` to avoid KeyError.
