---
name: google-drive-oauth
description: One-time Google Drive OAuth2 setup for Hermes — manual PKCE flow for installed apps (no browser on server). Produces a persistent token file with refresh_token. Required once; afterwards auto-refreshes.
triggers:
  - "set up google drive"
  - "connect google drive"
  - "google drive credentials"
  - "drive oauth"
  - "drive access token"
  - "authenticate google drive"
---

# Google Drive OAuth — Manual PKCE Flow

Use this when `/app/data/google_drive_token.json` does not exist or has no `refresh_token`.
After first run, token auto-refreshes — never repeat this flow unless token is fully revoked.

---

## PREREQS

- OAuth client credentials at `/app/data/google_credentials.json`
- Format: `{"installed": {"client_id": "...", "client_secret": "...", ...}}`
- If user hasn't shared credentials yet, ask for the JSON from Google Cloud Console → APIs & Services → Credentials → OAuth 2.0 Client ID (type: Desktop/Installed app)

---

## STEP 1 — Generate auth URL + save PKCE verifier

Run this in terminal — saves verifier to `/app/data/google_pkce.json`:

```python
import json, secrets, hashlib, base64, urllib.parse

code_verifier = secrets.token_urlsafe(64)
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b'=').decode()

with open('/app/data/google_pkce.json', 'w') as f:
    json.dump({"code_verifier": code_verifier}, f)

with open('/app/data/google_credentials.json') as f:
    c = json.load(f)['installed']

params = {
    "response_type": "code",
    "client_id": c['client_id'],
    "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
    "scope": "https://www.googleapis.com/auth/drive",
    "code_challenge": code_challenge,
    "code_challenge_method": "S256",
    "access_type": "offline",
    "prompt": "consent"
}
auth_url = c['auth_uri'] + '?' + urllib.parse.urlencode(params)
print("AUTH_URL:", auth_url)
```

Send auth URL to user. Ask them to click, sign in, and paste back the code shown.

---

## STEP 2 — Exchange code for tokens

Replace `CODE_HERE` with what the user pastes:

```python
import json, urllib.parse, urllib.request

with open('/app/data/google_pkce.json') as f:
    pkce = json.load(f)
with open('/app/data/google_credentials.json') as f:
    c = json.load(f)['installed']

code = 'CODE_HERE'

data = urllib.parse.urlencode({
    'code': code,
    'client_id': c['client_id'],
    'client_secret': c['client_secret'],
    'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
    'grant_type': 'authorization_code',
    'code_verifier': pkce['code_verifier']
}).encode()

req = urllib.request.Request('https://oauth2.googleapis.com/token', data=data, method='POST')
req.add_header('Content-Type', 'application/x-www-form-urlencoded')
with urllib.request.urlopen(req) as resp:
    token_data = json.loads(resp.read())

with open('/app/data/google_drive_token.json', 'w') as f:
    json.dump(token_data, f)

print("Has refresh_token:", 'refresh_token' in token_data)
print("Token saved!")
```

Confirm `Has refresh_token: True`. If False, re-run Step 1 with `prompt=consent` (already included).

---

## STEP 3 — Verify

```python
import json, urllib.request

with open('/app/data/google_drive_token.json') as f:
    td = json.load(f)

req = urllib.request.Request('https://www.googleapis.com/drive/v3/about?fields=user',
    method='GET')
req.add_header('Authorization', f'Bearer {td["access_token"]}')
with urllib.request.urlopen(req) as r:
    print(json.loads(r.read()))
```

---

## PITFALLS

- **Always refresh the access token before Drive operations** — do not assume the stored access_token in `google_drive_token.json` is still valid. Access tokens expire in ~1 hour. Always call the refresh endpoint first, update the file, then proceed. The refresh_token does not expire (unless revoked). See TOKEN AUTO-REFRESH section below.
- **PKCE verifier must be saved before generating the URL** — if the flow is interrupted, regenerate from Step 1. The verifier and code are a matched pair; using a mismatched pair gives `invalid_grant: Missing code verifier`.
- **Auth codes expire in ~10 minutes** — if the user is slow, regenerate the URL (Step 1 again). Reuse of an expired code gives `invalid_grant`.
- **Do NOT use `google_auth_oauthlib` flow object for PKCE** — the library's `fetch_token()` discards the verifier stored in the flow object when called in a fresh Python process. Use raw `urllib` instead (as shown above). This was the root cause of the `Missing code verifier` error in session June 2026.
- **`redirect_uri` must match exactly** — use `urn:ietf:wg:oauth:2.0:oob` for server-side flows with no browser redirect.
- **Scope** — `https://www.googleapis.com/auth/drive` gives full Drive access. Use `https://www.googleapis.com/auth/drive.file` for narrower scope (only files created by the app).

---

## TOKEN AUTO-REFRESH (after initial setup)

Always refresh the access token at the start of every Drive operation — do not assume the stored token is still valid (expires in ~1 hour). The `refresh_token` does not expire.

See `references/drive-file-operations.md` for token refresh, find-or-create folder, multipart upload, share, and link format patterns — all confirmed working June 2026.

Quick inline refresh:

```python
import json, urllib.parse, urllib.request

with open('/app/data/google_drive_token.json') as f:
    td = json.load(f)
with open('/app/data/google_credentials.json') as f:
    creds = json.load(f)['installed']

data = urllib.parse.urlencode({
    'client_id': creds['client_id'],
    'client_secret': creds['client_secret'],
    'refresh_token': td['refresh_token'],
    'grant_type': 'refresh_token'
}).encode()
req = urllib.request.Request('https://oauth2.googleapis.com/token', data=data, method='POST')
req.add_header('Content-Type', 'application/x-www-form-urlencoded')
with urllib.request.urlopen(req) as r:
    nt = json.loads(r.read())
ACCESS = nt['access_token']
td['access_token'] = ACCESS
with open('/app/data/google_drive_token.json', 'w') as f:
    json.dump(td, f)
```

```python
import json, urllib.parse, urllib.request

with open('/app/data/google_drive_token.json') as f:
    td = json.load(f)
with open('/app/data/google_credentials.json') as f:
    creds = json.load(f)['installed']

data = urllib.parse.urlencode({
    'client_id': creds['client_id'],
    'client_secret': creds['client_secret'],
    'refresh_token': td['refresh_token'],
    'grant_type': 'refresh_token'
}).encode()
req = urllib.request.Request('https://oauth2.googleapis.com/token', data=data, method='POST')
req.add_header('Content-Type', 'application/x-www-form-urlencoded')
with urllib.request.urlopen(req) as r:
    nt = json.loads(r.read())
ACCESS = nt['access_token']
td['access_token'] = ACCESS
with open('/app/data/google_drive_token.json', 'w') as f:
    json.dump(td, f)
```
