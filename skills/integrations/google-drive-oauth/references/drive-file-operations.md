# Google Drive File Operations — Confirmed Working Patterns

Token files:
- OAuth client: `/app/data/google_credentials.json`
- Token (with refresh_token): `/app/data/google_drive_token.json`

---

## Token Refresh (run at start of every Drive session)

```python
import json, urllib.parse, urllib.request

with open('/app/data/google_drive_token.json') as f:
    td = json.load(f)
with open('/app/data/google_credentials.json') as f:
    creds = json.load(f)['installed']

r = urllib.request.urlopen(urllib.request.Request(
    'https://oauth2.googleapis.com/token',
    data=urllib.parse.urlencode({
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'refresh_token': td['refresh_token'],
        'grant_type': 'refresh_token'
    }).encode(),
    method='POST',
    headers={'Content-Type': 'application/x-www-form-urlencoded'}))
ACCESS = json.loads(r.read())['access_token']
td['access_token'] = ACCESS
with open('/app/data/google_drive_token.json', 'w') as f:
    json.dump(td, f)
```

---

## Find or Create Folder (avoids duplicates on repeated runs)

```python
def find_or_create_folder(name, parent_id=None, access_token=None):
    q = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        q += f" and '{parent_id}' in parents"
    params = urllib.parse.urlencode({'q': q, 'fields': 'files(id)'})
    req = urllib.request.Request(
        f'https://www.googleapis.com/drive/v3/files?{params}',
        headers={'Authorization': f'Bearer {access_token}'})
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read())
    if res.get('files'):
        return res['files'][0]['id']
    # Create
    body = {'name': name, 'mimeType': 'application/vnd.google-apps.folder'}
    if parent_id:
        body['parents'] = [parent_id]
    req = urllib.request.Request(
        'https://www.googleapis.com/drive/v3/files',
        data=json.dumps(body).encode(), method='POST',
        headers={'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())['id']
```

---

## Multipart Upload (text file → Google Doc, or PNG image)

```python
def upload_file(path, name, content_type, parent_id, access_token, as_gdoc=False):
    bnd = 'bnd987xyz'
    meta = {'name': name, 'parents': [parent_id]}
    if as_gdoc:
        meta['mimeType'] = 'application/vnd.google-apps.document'
    with open(path, 'rb') as f:
        fb = f.read()
    body = (
        f'--{bnd}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n'.encode()
        + json.dumps(meta).encode()
        + f'\r\n--{bnd}\r\nContent-Type: {content_type}\r\n\r\n'.encode()
        + fb
        + f'\r\n--{bnd}--'.encode()
    )
    req = urllib.request.Request(
        'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart',
        data=body, method='POST',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': f'multipart/related; boundary={bnd}'
        })
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())  # returns {'id': '...', 'name': '...'}

# Upload a text file as Google Doc:
# upload_file('/tmp/post.txt', 'My Post', 'text/plain', folder_id, ACCESS, as_gdoc=True)

# Upload a PNG:
# upload_file('/tmp/image.png', 'image.png', 'image/png', folder_id, ACCESS)
```

---

## Share File/Folder Publicly (anyone with link can view)

```python
def share(file_id, access_token):
    try:
        urllib.request.urlopen(urllib.request.Request(
            f'https://www.googleapis.com/drive/v3/files/{file_id}/permissions',
            data=json.dumps({'role': 'reader', 'type': 'anyone'}).encode(),
            method='POST',
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            })).read()
    except Exception as e:
        print(f"Share error (non-fatal): {e}")
```

---

## Standard Link Formats

| Type | URL Pattern |
|---|---|
| Google Doc (edit) | `https://docs.google.com/document/d/{id}/edit` |
| Google Drive file | `https://drive.google.com/file/d/{id}/view` |
| Google Drive folder | `https://drive.google.com/drive/folders/{id}` |

---

## LinkedIn Post Drive Folder Structure

```
daily-post-linkedin/          ← parent folder (find-or-create, never duplicate)
  └── YYYY-MM-DD/             ← date subfolder (find-or-create)
        ├── LinkedIn Post — YYYY-MM-DD.gdoc
        ├── Image 1 — [description].png
        └── Image 2 — [description].png
```

Folder IDs (Rajeev's account, confirmed June 2026):
- `daily-post-linkedin` folder: `1jhlQkTd7bwFuX3UWwqkVeet6LFvG8v0-`
- Always use find-or-create pattern — do NOT hardcode subfolder IDs.
