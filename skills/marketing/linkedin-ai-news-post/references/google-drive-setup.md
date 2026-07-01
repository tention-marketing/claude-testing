# Google Drive Setup — LinkedIn Post Delivery

## Status: ✅ Connected (as of 2026-06-30)

## Credentials
- Credentials file: `/app/data/google_credentials.json`
- Token file: `/app/data/google_drive_token.json` (has refresh_token — persists)
- Client ID: `920737519873-nibcrhe9vl6ts19ltfdhs0mfequu0m64.apps.googleusercontent.com`
- Project: `hermes-496118`
- Scope: `https://www.googleapis.com/auth/drive`

## Folder Structure
- Parent folder: `daily-post-linkedin` → Drive ID: `1jhlQkTd7bwFuX3UWwqkVeet6LFvG8v0-`
- Each run creates: `daily-post-linkedin / YYYY-MM-DD / LinkedIn Post — YYYY-MM-DD` (Google Doc)

## Upload Pattern (Python, no external libs beyond stdlib)

```python
import json, urllib.parse, urllib.request, datetime

# 1. Load + refresh token if needed
with open('/app/data/google_drive_token.json') as f:
    token_data = json.load(f)
access_token = token_data['access_token']

def refresh_access_token():
    data = urllib.parse.urlencode({
        'client_id': token_data['client_id'],
        'client_secret': token_data['client_secret'],
        'refresh_token': token_data['refresh_token'],
        'grant_type': 'refresh_token'
    }).encode()
    req = urllib.request.Request('https://oauth2.googleapis.com/token', data=data, method='POST')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    with urllib.request.urlopen(req) as resp:
        new_token = json.loads(resp.read())
    token_data['access_token'] = new_token['access_token']
    with open('/app/data/google_drive_token.json', 'w') as f:
        json.dump(token_data, f)
    return new_token['access_token']

def drive_api(method, endpoint, body=None, params=None, token=None):
    url = f"https://www.googleapis.com/drive/v3/{endpoint}"
    if params:
        url += '?' + urllib.parse.urlencode(params)
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('Authorization', f'Bearer {token or access_token}')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = json.loads(e.read())
        if e.code == 401:
            new_tok = refresh_access_token()
            req2 = urllib.request.Request(url, data=data, method=method)
            req2.add_header('Authorization', f'Bearer {new_tok}')
            req2.add_header('Content-Type', 'application/json')
            with urllib.request.urlopen(req2) as resp:
                return json.loads(resp.read())
        raise

# 2. Create date subfolder inside parent
PARENT_ID = '1jhlQkTd7bwFuX3UWwqkVeet6LFvG8v0-'
today = datetime.date.today().strftime('%Y-%m-%d')
subfolder = drive_api('POST', 'files', {
    'name': today,
    'mimeType': 'application/vnd.google-apps.folder',
    'parents': [PARENT_ID]
})
subfolder_id = subfolder['id']

# 3. Upload content as Google Doc (multipart)
content = "Your post content here..."
boundary = "boundary_hermes_linkedin"
metadata = json.dumps({
    'name': f'LinkedIn Post — {today}',
    'parents': [subfolder_id],
    'mimeType': 'application/vnd.google-apps.document'
}).encode()
body = (
    f'--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n'.encode() +
    metadata +
    f'\r\n--{boundary}\r\nContent-Type: text/plain; charset=UTF-8\r\n\r\n'.encode() +
    content.encode('utf-8') +
    f'\r\n--{boundary}--'.encode()
)
req = urllib.request.Request(
    'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart',
    data=body, method='POST'
)
req.add_header('Authorization', f'Bearer {access_token}')
req.add_header('Content-Type', f'multipart/related; boundary={boundary}')
with urllib.request.urlopen(req) as resp:
    file_data = json.loads(resp.read())
file_id = file_data['id']

# 4. Make shareable
perm_req = urllib.request.Request(
    f'https://www.googleapis.com/drive/v3/files/{file_id}/permissions',
    data=json.dumps({'role': 'reader', 'type': 'anyone'}).encode(), method='POST'
)
perm_req.add_header('Authorization', f'Bearer {access_token}')
perm_req.add_header('Content-Type', 'application/json')
with urllib.request.urlopen(perm_req) as resp:
    resp.read()

drive_link = f"https://docs.google.com/document/d/{file_id}/edit"
print("Drive link:", drive_link)
```

## PKCE Auth Flow (if token ever needs re-auth)
The PKCE code_verifier MUST be saved to disk before generating the auth URL.
The library does NOT persist state across Python calls. Pattern:

```python
import secrets, hashlib, base64, json

code_verifier = secrets.token_urlsafe(64)
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b'=').decode()

# Save immediately
with open('/app/data/google_pkce.json', 'w') as f:
    json.dump({"code_verifier": code_verifier}, f)

# Build auth URL with code_challenge + code_challenge_method=S256
# redirect_uri = 'urn:ietf:wg:oauth:2.0:oob' (for copy-paste code flow)
# After user pastes code, load verifier from file and exchange manually via urllib
```

## Common Pitfalls
- **InvalidGrantError: Missing code verifier** — happened when using InstalledAppFlow without preserving the PKCE state. Fix: generate PKCE manually and save verifier to disk before showing auth URL. Exchange code manually via urllib (not via flow.fetch_token).
- **401 on upload** — access_token expired. Call refresh_access_token() and retry. refresh_token is long-lived and saved in the token file.
- **Do NOT use InstalledAppFlow.run_local_server()** on Railway — no browser available. Always use the copy-paste OOB flow.
