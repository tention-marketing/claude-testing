# Google Drive Upload — Working Patterns (June 2026)

Credentials:
- OAuth client: `/app/data/google_credentials.json`
- Token: `/app/data/google_drive_token.json` (contains `access_token` + `refresh_token`)

## Token Refresh

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

## Find or Create Folder (avoids duplicates)

```python
def find_or_create_folder(name, parent_id=None):
    q = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        q += f" and '{parent_id}' in parents"
    s = drive_api('GET', 'files', params={'q': q, 'fields': 'files(id)'})
    if s.get('files'):
        return s['files'][0]['id']
    body = {'name': name, 'mimeType': 'application/vnd.google-apps.folder'}
    if parent_id:
        body['parents'] = [parent_id]
    r = drive_api('POST', 'files', body)
    return r['id']
```

## Multipart Upload (text file as Google Doc, or image as PNG)

```python
def upload(path, name, mime, parent_id, as_gdoc=False):
    boundary = 'bnd987xyz'
    meta = {'name': name, 'parents': [parent_id]}
    if as_gdoc:
        meta['mimeType'] = 'application/vnd.google-apps.document'
    with open(path, 'rb') as f:
        fb = f.read()
    body = (
        f'--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n'.encode()
        + json.dumps(meta).encode()
        + f'\r\n--{boundary}\r\nContent-Type: {mime}\r\n\r\n'.encode()
        + fb
        + f'\r\n--{boundary}--'.encode()
    )
    req = urllib.request.Request(
        'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart',
        data=body, method='POST'
    )
    req.add_header('Authorization', f'Bearer {ACCESS}')
    req.add_header('Content-Type', f'multipart/related; boundary={boundary}')
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())
```

## Share File (anyone with link can view)

```python
def share(fid):
    req = urllib.request.Request(
        f'https://www.googleapis.com/drive/v3/files/{fid}/permissions',
        data=json.dumps({'role': 'reader', 'type': 'anyone'}).encode(),
        method='POST'
    )
    req.add_header('Authorization', f'Bearer {ACCESS}')
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req) as r:
        r.read()
```

## drive_api helper

```python
def drive_api(method, ep, body=None, params=None):
    url = 'https://www.googleapis.com/drive/v3/' + ep
    if params:
        url += '?' + urllib.parse.urlencode(params)
    d = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=d, method=method)
    req.add_header('Authorization', f'Bearer {ACCESS}')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())
```

## DELETE API (returns 204 No Content — don't JSON-parse the response)

When deleting old docs in a folder:
```python
# WRONG — will crash with JSONDecodeError on empty 204 response:
api('DELETE', f'files/{fid}')  # if your api() tries to json.loads() the result

# RIGHT — handle DELETE separately:
req = urllib.request.Request(url, method='DELETE')
req.add_header('Authorization', f'Bearer {ACCESS}')
try:
    with urllib.request.urlopen(req) as r: r.read()
except: pass
```

## Folder/Doc Links

- Folder: `https://drive.google.com/drive/folders/{folder_id}`
- Google Doc: `https://docs.google.com/document/d/{file_id}/edit`
- Image: `https://drive.google.com/file/d/{file_id}/view`

## Pitfalls

- **DELETE returns 204 (empty body)** — do not try to JSON-parse delete responses. Crashes with JSONDecodeError.
- **Always search before creating folders** — running twice creates duplicate folders. Use find_or_create_folder().
- **Token refresh must happen first** — stale access_token gives 401. Always refresh at the start of every run.
- **Images generated in subagents are lost** — subagent /tmp files don't persist to parent. Generate images in the main agent's terminal call.
- **execute_code is blocked in cron/certain contexts** — use terminal() heredoc instead.
