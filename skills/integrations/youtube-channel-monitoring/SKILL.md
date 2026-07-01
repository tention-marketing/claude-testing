---
name: youtube-channel-monitoring
description: Monitor YouTube channels for latest videos, get video details and summaries — without the YouTube API. Uses RSS feeds and web search.
tags: [youtube, rss, monitoring, video, web-search]
triggers:
  - "check youtube channel"
  - "latest video from"
  - "what did X post on youtube"
  - "find youtube channel"
  - "youtube channel update"
---

# YouTube Channel Monitoring (No API Key Required)

## When to Load
When Rajeev asks to check a YouTube channel for latest videos, get video summaries, or monitor a creator's uploads.

## Key Insight
YouTube has no public API without a key, but every channel has a **free RSS feed** that returns the latest 15 videos with full metadata (title, description, views, publish date, URL). No authentication needed.

---

## Step 1 — Find the Channel ID

YouTube RSS feeds require a **channel ID** (format: `UCxxxxxxxxxxxxxxxxxxxxxxxxx`), not a handle like `@nateherk`.

### Method: Fetch channel page and extract from `<head>`
```bash
curl -s --max-time 15 "https://www.youtube.com/@CHANNEL_HANDLE" | grep -o 'channel_id=[^"&]*' | head -1
```
Or look for the RSS link in the HTML head:
```
<link rel="alternate" type="application/rss+xml" href="https://www.youtube.com/feeds/videos.xml?channel_id=UCxxxxxxx">
```

**Known channel IDs:**
| Channel | Handle | Channel ID |
|---------|--------|------------|
| Nate Herk (AI Automation / n8n) | @nateherk | `UC2ojq-nuP8ceeHqiroeKhBA` |

> ✅ `UC2ojq-nuP8ceeHqiroeKhBA` confirmed working June 2026 — RSS feed returns "Nate Herk | AI Automation" channel correctly. `UCfWg1ceoKD5JKo8GCMCBb3g` returns 404. Always re-fetch from the channel page head when in doubt.

Add more as discovered.

---

## Step 2 — Fetch the RSS Feed

```bash
curl -s --max-time 15 "https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID" > /tmp/yt_feed.xml
```

> ⚠️ The old `?user=HANDLE` format does NOT work — always use `?channel_id=UC...`

---

## Step 3 — Parse the Feed

```python
import xml.etree.ElementTree as ET

ns = {
    'atom': 'http://www.w3.org/2005/Atom',
    'media': 'http://search.yahoo.com/mrss/',
    'yt': 'http://www.youtube.com/xml/schemas/2015'
}

tree = ET.parse('/tmp/yt_feed.xml')
root = tree.getroot()

for entry in root.findall('atom:entry', ns)[:5]:
    title = entry.find('atom:title', ns).text
    url = entry.find('atom:link', ns).get('href')
    published = entry.find('atom:published', ns).text[:10]
    views_el = entry.find('.//media:statistics', ns)
    views = views_el.get('views') if views_el is not None else 'N/A'
    desc_el = entry.find('.//media:description', ns)
    description = desc_el.text[:400] if desc_el is not None else ''
    print(f"{published} | {views} views | {title}")
    print(f"  URL: {url}")
    print(f"  {description[:200]}...")
    print()
```

---

## What the RSS Feed Returns Per Video
- ✅ Title
- ✅ URL
- ✅ Publish date + last updated
- ✅ Full description
- ✅ View count
- ✅ Star rating count + average
- ✅ Thumbnail URL
- ❌ Like count (not in RSS)
- ❌ Comment count (not in RSS)

---

## Getting Video Summary Without API

Since YouTube pages require JavaScript (bot-blocked), get summaries via:

1. **RSS description** — often contains chapter timestamps and full description (best source)
2. **Creator's website** — many YouTubers like Nate Herk post blog summaries at `nateherk.com`
3. **Web search**: `site:youtube.com "Channel Name" video title` for snippets

---

## ⚠️ "Summary" Means NARRATIVE Summary — NOT Raw Description

When Rajeev asks for a "video summary" or "what is this video about", he wants a **human-written narrative** explaining what the creator actually talks about — NOT the raw YouTube description text.

The raw description is mostly promo links, affiliate codes, and chapter headers. A real summary should answer: *"What does the creator teach/discuss/argue in this video?"*

**Wrong** (just cleaning description):
> "My FREE AI OS Course: https://... There are a lot of ways to make money with your AI skills."

**Correct** (narrative summary):
> "Nate breaks down the different ways to make money with AI skills — starting your own agency, leveling up at your current job, or running your own business. He explains why learning Claude is just the beginning and what to do next."

### How to write a good summary from the description:
1. Skip all lines starting with `http`, `►`, `#`, emoji promo prefixes (`📩`, `✅`, `🖥`, `🤝`, `📌`, `My `, `Full courses`, `Apply`, `Work with me`, `Code `)
2. Find the substantive paragraph(s) that explain what the video covers
3. Write 2-3 sentences in plain language about the actual content
4. If the description is mostly promo with no substance, note the chapter titles as a fallback

Rajeev explicitly corrected this — "this is not summary video I told what is talking about the summary do understand what i said you" — after the first Excel export used cleaned descriptions instead of real summaries.

---

## Exporting Videos to Excel (openpyxl)

When Rajeev asks for a summary file or `.xlsx` export of channel videos:

```bash
pip install openpyxl -q
```

```python
import xml.etree.ElementTree as ET
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ns = {
    'atom': 'http://www.w3.org/2005/Atom',
    'media': 'http://search.yahoo.com/mrss/',
    'yt': 'http://www.youtube.com/xml/schemas/2015'
}

tree = ET.parse('/tmp/yt_feed.xml')
root = tree.getroot()
entries = root.findall('atom:entry', ns)

videos = []
for entry in entries:
    title = entry.find('atom:title', ns).text
    url = entry.find('atom:link', ns).get('href')
    published = entry.find('atom:published', ns).text[:10]
    views_el = entry.find('.//media:statistics', ns)
    views = int(views_el.get('views', 0)) if views_el is not None else 0
    desc_el = entry.find('.//media:description', ns)
    desc = desc_el.text if desc_el is not None else ''
    # Clean description: skip lines starting with http, ►, #, emoji-prefixed promo lines
    clean = [l.strip() for l in desc.split('\n')
             if l.strip() and not any(l.strip().startswith(x) for x in
             ['http', '►', '#', '📩', '🖥', '🤝', '✅', '📌'])]
    summary = ' '.join(clean[:5])[:400]
    videos.append({'title': title, 'published': published, 'views': views, 'url': url, 'summary': summary})

wb = Workbook()
ws = wb.active
ws.title = "Videos"

# Style helpers
header_fill = PatternFill("solid", fgColor="1E1E2E")
thin = Side(style='thin', color="CCCCCC")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

# Title banner row
ws.merge_cells('A1:F1')
ws['A1'].value = "🎬 YouTube Channel Videos Summary"
ws['A1'].font = Font(bold=True, size=14, color="FFFFFF")
ws['A1'].fill = PatternFill("solid", fgColor="FF0000")
ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
ws.row_dimensions[1].height = 35

headers = ['#', 'Video Title', 'Published Date', 'Views', 'YouTube Link', 'Summary']
for col, h in enumerate(headers, 1):
    cell = ws.cell(row=2, column=col, value=h)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal='center', vertical='center')
    cell.border = border

for i, v in enumerate(videos, 1):
    row = i + 2
    fill = PatternFill("solid", fgColor="F0F4FF" if i % 2 == 0 else "FFFFFF")
    for col, val in enumerate([i, v['title'], v['published'], v['views'], v['url'], v['summary']], 1):
        cell = ws.cell(row=row, column=col, value=val)
        cell.fill = fill
        cell.border = border
        cell.alignment = Alignment(vertical='top', wrap_text=True,
                                   horizontal='center' if col in [1,3,4] else 'left')
        if col == 5:
            cell.font = Font(color="0563C1", underline='single')
    ws.row_dimensions[row].height = 60

for col, width in enumerate([5, 45, 15, 12, 45, 60], 1):
    ws.column_dimensions[get_column_letter(col)].width = width

ws.freeze_panes = 'A3'

output_path = '/tmp/YouTube_Videos_Summary.xlsx'
wb.save(output_path)
print(f"Saved: {output_path}")
```

After saving, send with:
```python
send_message(message="MEDIA:/tmp/YouTube_Videos_Summary.xlsx", target="discord:CHANNEL_ID")
```

---

## Getting ALL Videos (Beyond 15-Video RSS Limit) — Browse API (Preferred)

RSS only returns 15 videos. **`scrapetube` returns 0 results on Railway** (confirmed June 2026 — channel iterator yields nothing for this channel). Use the **YouTube internal browse API** instead — it's faster and more reliable.

### Step 1: Get the correct tab params
YouTube's browse API requires **tab-specific params**, NOT generic ones. The params differ per channel and must be fetched dynamically:

```python
import requests, json

channel_id = "UC2ojq-nuP8ceeHqiroeKhBA"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/json',
}
payload = {
    "context": {"client": {"clientName": "WEB", "clientVersion": "2.20231121.08.00"}},
    "browseId": channel_id,
    "params": "EgZ2aWRlb3MyAggA"  # initial request — used only to get tab endpoints
}
r = requests.post('https://www.youtube.com/youtubei/v1/browse', headers=headers, json=payload, timeout=30)
data = r.json()

tabs = data['contents']['twoColumnBrowseResultsRenderer']['tabs']
for tab in tabs:
    tr = tab.get('tabRenderer', {})
    ep = tr.get('endpoint', {}).get('browseEndpoint', {})
    print(f"{tr.get('title','?')}: params={ep.get('params','')}")
# Videos tab params example: EgZ2aWRlb3PyBgQKAjoA
# Shorts tab params example:  EgZzaG9ydHPyBgUKA5oBAA%3D%3D
```

> ⚠️ The params `EgZ2aWRlb3MyAggA` / `EgZzaG9ydHMyAggJ` (used in older sessions) do NOT return video content — they return the tab list only. Always fetch the real params from the tab endpoint first.

### Step 2: Parse `lockupViewModel` (YouTube's new format as of mid-2026)

YouTube changed from `videoRenderer` to `lockupViewModel` for the Videos tab. **`videoRenderer` returns 0 results on the Videos tab now.**

```python
def parse_lockup(item_content):
    vm = item_content.get('lockupViewModel', {})
    if not vm:
        return None
    vid_id = vm.get('contentId', '')
    metadata = vm.get('metadata', {}).get('lockupMetadataViewModel', {})
    title = metadata.get('title', {}).get('content', '')
    rows = metadata.get('metadata', {}).get('contentMetadataViewModel', {}).get('metadataRows', [])
    views = 0
    published = ''
    for row in rows:
        for part in row.get('metadataParts', []):
            txt = part.get('text', {}).get('content', '')
            if 'view' in txt.lower():
                try:
                    num = txt.lower().replace(' views','').replace(' view','').replace(',','').strip()
                    if num.endswith('k'): views = int(float(num[:-1]) * 1000)
                    elif num.endswith('m'): views = int(float(num[:-1]) * 1000000)
                    else: views = int(num)
                except: pass
            elif any(x in txt.lower() for x in ['ago', 'year', 'month', 'week', 'day', 'hour']):
                published = txt
    duration = ''
    duration_secs = 0
    try:
        for ov in vm['contentImage']['thumbnailViewModel']['overlays']:
            for badge in ov.get('thumbnailBottomOverlayViewModel', {}).get('badges', []):
                text = badge.get('thumbnailBadgeViewModel', {}).get('text', '')
                if ':' in text:
                    duration = text
                    parts = text.split(':')
                    if len(parts) == 2: duration_secs = int(parts[0])*60 + int(parts[1])
                    elif len(parts) == 3: duration_secs = int(parts[0])*3600 + int(parts[1])*60 + int(parts[2])
                    break
    except: pass
    if not vid_id or not title:
        return None
    is_short = 0 < duration_secs <= 60
    return {
        'video_id': vid_id, 'title': title, 'duration': duration,
        'duration_secs': duration_secs, 'views': views, 'published': published,
        'type': 'Short' if is_short else 'Long', 'is_short': is_short,
        'url': f'https://www.youtube.com/watch?v={vid_id}'
    }
```

### Step 3: Pagination with continuation tokens

```python
def find_continuation(obj, depth=0):
    if depth > 25: return None
    if isinstance(obj, dict):
        if 'continuationCommand' in obj:
            token = obj['continuationCommand'].get('token', '')
            if token: return token
        for v in obj.values():
            r = find_continuation(v, depth+1)
            if r: return r
    elif isinstance(obj, list):
        for item in obj:
            r = find_continuation(item, depth+1)
            if r: return r
    return None

# Initial page: videos are in tabs[1]['tabRenderer']['content']['richGridRenderer']['contents']
# Continuation pages: data['onResponseReceivedActions'][N]['appendContinuationItemsAction']['continuationItems']
```

### Shorts use `shortsLockupViewModel` (different from Videos tab)

```python
def parse_shorts(obj, depth=0):
    results = []
    if depth > 25: return results
    if isinstance(obj, dict):
        if 'shortsLockupViewModel' in obj:
            sl = obj['shortsLockupViewModel']
            vid_id = ''
            try:
                cmd = sl['onTap']['innertubeCommand']
                vid_id = cmd.get('reelWatchEndpoint', {}).get('videoId', '')
            except: pass
            title = ''
            try: title = sl['overlayMetadata']['primaryText']['content']
            except: pass
            if vid_id:
                results.append({'video_id': vid_id, 'title': title, 'duration': '<60s',
                                 'duration_secs': 30, 'views': 0, 'published': '',
                                 'type': 'Short', 'is_short': True,
                                 'url': f'https://www.youtube.com/shorts/{vid_id}'})
        else:
            for v in obj.values():
                results.extend(parse_shorts(v, depth+1))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(parse_shorts(item, depth+1))
    return results
```

**Nate Herk confirmed stats (June 2026, browse API):**
- Long videos: **282**
- YouTube Shorts: **160**
- Total: **442**

---

## Getting ALL Videos (Beyond 15-Video RSS Limit) — scrapetube (Fallback)

> ⚠️ scrapetube returns 0 results on Railway for this channel (confirmed June 2026). Use the browse API above instead. Keeping this section as reference for other environments.

To get the full channel history, use **`scrapetube`**:

### scrapetube (use only for channels under ~100 videos on Railway)


RSS only returns 15 videos. To get the full channel history, use the **YouTube Internal Browse API** (see the full scraper section above). This is the preferred method — it completes in under 60 seconds for channels with 400+ videos.

> ⚠️ **Do NOT use `scrapetube`** for large channels in Railway — it returned 0 results for Nate Herk's channel (442 videos) in June 2026. The browse API is more reliable and faster.

> ⚠️ Published dates from the browse API are **relative** ("3 months ago") not absolute — this is a YouTube limitation without the Data API. The RSS feed gives absolute dates for the 15 most recent videos.

---

## Scraping ALL Videos (YouTube Internal Browse API — Updated June 2026)

> ⚠️ **BREAKING CHANGE (June 2026):** YouTube's internal browse API no longer returns `videoRenderer` objects for the Videos tab. They switched to `lockupViewModel`. The old params `EgZ2aWRlb3MyAggA` and `EgZzaG9ydHMyAggJ` no longer work correctly — the tabs return empty unless you use the **correct params fetched from the channel's tab endpoint**.

### Step 1: Get the correct tab params dynamically

Always fetch the tab params from the channel page first — do NOT hardcode:

```python
import requests, json

channel_id = "UC2ojq-nuP8ceeHqiroeKhBA"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/json',
}

# Fetch channel home to get tab endpoints
payload = {
    "context": {"client": {"clientName": "WEB", "clientVersion": "2.20231121.08.00"}},
    "browseId": channel_id,
    "params": "EgZ2aWRlb3PyBgQKAjoA"   # Videos tab — confirmed working June 2026
}
r = requests.post('https://www.youtube.com/youtubei/v1/browse', headers=headers, json=payload, timeout=30)
data = r.json()

# Navigate: contents > twoColumnBrowseResultsRenderer > tabs
tabs = data['contents']['twoColumnBrowseResultsRenderer']['tabs']
# Tab indices: 0=Home, 1=Videos, 2=Shorts, 3=Podcasts, 4=Playlists, 5=Posts
videos_params = tabs[1]['tabRenderer']['endpoint']['browseEndpoint']['params']
shorts_params  = tabs[2]['tabRenderer']['endpoint']['browseEndpoint']['params']
print(f"Videos params: {videos_params}")  # e.g. EgZ2aWRlb3PyBgQKAjoA
print(f"Shorts params:  {shorts_params}")  # e.g. EgZzaG9ydHPyBgUKA5oBAA%3D%3D
```

**Known-good params as of June 2026 for Nate Herk:**
- Videos tab: `EgZ2aWRlb3PyBgQKAjoA`
- Shorts tab: `EgZzaG9ydHPyBgUKA5oBAA%3D%3D`

### Step 2: Parse `lockupViewModel` (new renderer format)

```python
def parse_lockup(item_content):
    """Parse a lockupViewModel into a video dict. Returns None if not a video."""
    vm = item_content.get('lockupViewModel', {})
    if not vm:
        return None

    vid_id = vm.get('contentId', '')
    metadata = vm.get('metadata', {}).get('lockupMetadataViewModel', {})
    title = metadata.get('title', {}).get('content', '')

    # Views and published date are in metadataRows
    rows = metadata.get('metadata', {}).get('contentMetadataViewModel', {}).get('metadataRows', [])
    views = 0
    published = ''
    for row in rows:
        for part in row.get('metadataParts', []):
            txt = part.get('text', {}).get('content', '')
            if 'view' in txt.lower():
                try:
                    num = txt.lower().replace(' views','').replace(' view','').replace(',','').strip()
                    if num.endswith('k'):   views = int(float(num[:-1]) * 1000)
                    elif num.endswith('m'): views = int(float(num[:-1]) * 1000000)
                    else:                   views = int(num)
                except: pass
            elif any(x in txt.lower() for x in ['ago','year','month','week','day','hour']):
                published = txt

    # Duration is in the thumbnail overlay
    duration = ''
    duration_secs = 0
    try:
        for ov in vm['contentImage']['thumbnailViewModel']['overlays']:
            for badge in ov.get('thumbnailBottomOverlayViewModel', {}).get('badges', []):
                text = badge.get('thumbnailBadgeViewModel', {}).get('text', '')
                if ':' in text:
                    duration = text
                    parts = text.split(':')
                    if len(parts) == 2:   duration_secs = int(parts[0])*60 + int(parts[1])
                    elif len(parts) == 3: duration_secs = int(parts[0])*3600 + int(parts[1])*60 + int(parts[2])
                    break
    except: pass

    if not vid_id or not title:
        return None

    is_short = 0 < duration_secs <= 60
    return {
        'video_id': vid_id, 'title': title, 'duration': duration,
        'duration_secs': duration_secs, 'views': views, 'published': published,
        'type': 'Short' if is_short else 'Long', 'is_short': is_short,
        'url': f'https://www.youtube.com/watch?v={vid_id}'
    }
```

### Step 3: Parse Shorts (`shortsLockupViewModel`)

```python
def parse_short(obj):
    sl = obj.get('shortsLockupViewModel', {})
    if not sl: return None
    vid_id = ''
    try:
        cmd = sl['onTap']['innertubeCommand']
        vid_id = cmd.get('reelWatchEndpoint', {}).get('videoId', '')
    except: pass
    title = ''
    try: title = sl['overlayMetadata']['primaryText']['content']
    except: pass
    views = 0
    try:
        vt = sl['overlayMetadata']['secondaryText']['content']
        num = vt.lower().replace(' views','').replace(',','').strip()
        if num.endswith('k'):   views = int(float(num[:-1])*1000)
        elif num.endswith('m'): views = int(float(num[:-1])*1000000)
        else:                   views = int(num)
    except: pass
    if not vid_id: return None
    return {'video_id': vid_id, 'title': title, 'duration': '<60s',
            'duration_secs': 30, 'views': views, 'published': '',
            'type': 'Short', 'is_short': True,
            'url': f'https://www.youtube.com/shorts/{vid_id}'}
```

### Step 4: Paginate with continuation tokens

```python
def find_continuation(obj, depth=0):
    """Recursively find continuationCommand token."""
    if depth > 25: return None
    if isinstance(obj, dict):
        if 'continuationCommand' in obj:
            token = obj['continuationCommand'].get('token', '')
            if token: return token
        for v in obj.values():
            r = find_continuation(v, depth+1)
            if r: return r
    elif isinstance(obj, list):
        for item in obj:
            r = find_continuation(item, depth+1)
            if r: return r
    return None

def browse(browse_id=None, params=None, continuation=None):
    payload = {"context": {"client": {"clientName": "WEB", "clientVersion": "2.20231121.08.00"}}}
    if continuation:
        payload["continuation"] = continuation
    else:
        payload["browseId"] = browse_id
        payload["params"] = params
    r = requests.post('https://www.youtube.com/youtubei/v1/browse',
                      headers=headers, json=payload, timeout=30)
    return r.json()

# --- Scrape all long-form videos ---
all_videos = []
data = browse(channel_id, videos_params)
tabs = data['contents']['twoColumnBrowseResultsRenderer']['tabs']
contents = tabs[1]['tabRenderer']['content']['richGridRenderer']['contents']
for item in contents:
    if 'richItemRenderer' in item:
        v = parse_lockup(item['richItemRenderer'].get('content', {}))
        if v: all_videos.append(v)
token = find_continuation(contents)
while token:
    data = browse(continuation=token)
    new_items = []
    for action in data.get('onResponseReceivedActions', []):
        new_items.extend(action.get('appendContinuationItemsAction', {}).get('continuationItems', []))
    for item in new_items:
        if 'richItemRenderer' in item:
            v = parse_lockup(item['richItemRenderer'].get('content', {}))
            if v: all_videos.append(v)
    token = find_continuation(new_items)

# --- Scrape all Shorts ---
shorts = []
data = browse(channel_id, shorts_params)
token = find_continuation(data)
# parse initial page
def scrape_shorts_page(obj):
    results = []
    if isinstance(obj, dict):
        v = parse_short(obj)
        if v: results.append(v)
        else:
            for val in obj.values(): results.extend(scrape_shorts_page(val))
    elif isinstance(obj, list):
        for item in obj: results.extend(scrape_shorts_page(item))
    return results

shorts.extend(scrape_shorts_page(data))
while token:
    data = browse(continuation=token)
    shorts.extend(scrape_shorts_page(data))
    token = find_continuation(data)

all_combined = all_videos + shorts
print(f"Long: {len(all_videos)}, Shorts: {len(shorts)}, Total: {len(all_combined)}")
```

**Nate Herk confirmed stats (June 2026):**
- Long videos: **282**
- YouTube Shorts: **160**
- Total: **442**
- Subscribers: **~823,000**

---

## Multi-Sheet Research Report
When Rajeev asks for full channel research (performance analysis + content ideas), use the **6-sheet Excel pattern**.
See: `references/channel-research-report-pattern.md` for full structure, color scheme, title formulas, and high-performing topic list.

---

## ⚠️ execute_code is Blocked in Cron/Railway Context

`execute_code` (the inline Python tool) is **blocked** in this deployment. Use `delegate_task` with toolsets `["terminal", "file"]` for all Python scripts that build Excel files or process JSON data. Pass the full script content in the goal. The subagent will write it to a temp file and run it via `python3`.

---

## Pitfalls

- **`?user=handle` returns 404** — only `?channel_id=UC...` works
- **YouTube HTML pages are JavaScript-rendered** — `curl` or `web_fetch` of youtube.com pages returns a login wall or empty content. Always use the RSS feed for structured data.
- **RSS only returns latest 15 videos** — can't get full history
- **Channel ID ≠ handle** — `@nateherk` ≠ the channel ID. Always resolve the handle to a UC... ID first.
- **`videoRenderer` is DEAD on the Videos tab (mid-2026)** — YouTube replaced it with `lockupViewModel`. Parsing for `videoRenderer` in browse API responses for the Videos tab returns 0 results. Use `lockupViewModel` parser (see above).
- **Browse API params must be fetched dynamically** — the params `EgZ2aWRlb3MyAggA` (Videos) and `EgZzaG9ydHMyAggJ` (Shorts) return tab listings only, not video content. The real content params (e.g. `EgZ2aWRlb3PyBgQKAjoA`) are in `tabs[N].tabRenderer.endpoint.browseEndpoint.params`. Always fetch them from a first request.
- **scrapetube returns 0 on Railway** — confirmed June 2026. Use the YouTube internal browse API instead for all "get all videos" tasks on Railway.
- **delegate_task subagents may fabricate video IDs and view counts** — observed multiple times in this task class. Subagents returned plausible-looking but entirely invented video IDs, fabricated view counts, and invented titles. **Always fetch data directly via `terminal` for reliable data.** Only use delegation for supplementary web searches, never as the primary data source.
- **Rajeev wants narrative summaries, not cleaned descriptions** — see the "Summary Means NARRATIVE Summary" section above. First export attempt was rejected because it used cleaned description text instead of real explanations of video content.
- **"All videos" research means truly ALL, not just latest 15** — when Rajeev says "I want to research all Nate videos" or "all videos on channel", he means the complete channel history. Do not use RSS (15 videos only). Use the browse API pagination approach.
- **JSON file storage on Railway is ephemeral** — scraped data saved to `/root/` between sessions will be gone after Railway restarts. If re-analysis is needed, scrape again. Do not assume prior-session JSON files still exist.
- **`execute_code` is blocked in this deployment** — Railway/cron context blocks the inline Python execution tool. Use `terminal` with heredoc (`python3 /dev/stdin << 'PYEOF'`) for all Python scripts. Heredocs require approval but work reliably.
- **yt-dlp times out on Railway for single video lookups** — confirmed June 2026. `yt-dlp --print-json` hangs and never returns. Use the oEmbed + RSS fast-path instead (see "Fast-Path" section above).
- **Subagent delegation for YouTube video info times out** — confirmed June 2026. Delegating a "fetch this YouTube video details" task hit the 600s timeout. Always fetch video details directly in the parent agent using oEmbed + RSS. Only delegate for supplementary tasks.
- **YouTube internal player API (`/youtubei/v1/player`) returns empty videoDetails** — confirmed June 2026. The `videoDetails` and `shortDescription` fields came back null/empty for single video lookups. Do not use this endpoint. Use oEmbed + RSS instead.

---

## Quick One-Liner (Latest Video Only)
```bash
curl -s "https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID" | \
  python3 -c "
import sys, xml.etree.ElementTree as ET
ns = {'atom': 'http://www.w3.org/2005/Atom', 'media': 'http://search.yahoo.com/mrss/'}
root = ET.fromstring(sys.stdin.read())
e = root.findall('atom:entry', ns)[0]
print(e.find('atom:title', ns).text)
print(e.find('atom:link', ns).get('href'))
print(e.find('atom:published', ns).text[:10])
print(e.find('.//media:statistics', ns).get('views'), 'views')
"
```

---

## Fast-Path: Getting Info for a Specific Video ID

When given a specific YouTube URL/video ID (not a whole channel), use these two lightweight calls — **do NOT use yt-dlp or subagent delegation** (both timed out in June 2026 on Railway):

### Step 1 — oEmbed for title and author (no auth needed)
```python
import urllib.request, json

video_id = "S2ME69hra-k"
url = f'https://www.youtube.com/oembed?url=https://youtu.be/{video_id}&format=json'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15)
data = json.loads(resp.read())
print(data['title'])        # "Two AI Events I Want You At This Summer"
print(data['author_name'])  # "Nate Herk | AI Automation"
```

### Step 2 — RSS feed for description, publish date, views
If the video belongs to a known channel, fetch the RSS and look up the entry by video ID:
```python
import urllib.request, xml.etree.ElementTree as ET

channel_id = "UC2ojq-nuP8ceeHqiroeKhBA"
url = f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15)
xml_text = resp.read().decode()

ns = {'atom': 'http://www.w3.org/2005/Atom', 'media': 'http://search.yahoo.com/mrss/', 'yt': 'http://www.youtube.com/xml/schemas/2015'}
root = ET.fromstring(xml_text)
for entry in root.findall('atom:entry', ns):
    vid_id = entry.find('yt:videoId', ns).text
    if vid_id == video_id:
        title = entry.find('atom:title', ns).text
        published = entry.find('atom:published', ns).text
        desc = entry.find('.//media:description', ns).text
        views = entry.find('.//media:statistics', ns).get('views')
        print(f"Title: {title}")
        print(f"Published: {published}")
        print(f"Views: {views}")
        print(f"Description:\n{desc}")
        break
```

> ✅ This combo (oEmbed + RSS) confirmed working June 2026 on Railway. Returns title, author, publish date (ISO), full description, and view count — everything needed for a summary.

> ⚠️ RSS only covers the **latest 15 videos**. If the target video is older, you'll need the browse API or a web search fallback.

---

## Voice Summary Workflow (YouTube → TTS → Discord)

When Rajeev shares a YouTube link and asks for a "summary in recording" or "voice summary":

1. Fetch video details via oEmbed + RSS (see Fast-Path above)
2. If the description references external URLs (event sites, landing pages), **fetch those too** for richer detail (e.g. `workless.ai` gave event dates, location, programme)
3. Write a narrative summary (NOT cleaned description — see rule above)
4. Call `text_to_speech` with the summary
5. Send the MP3 to the target Discord channel via curl multipart upload
6. Confirm with one line — no need to repeat the full summary in text

> ✅ Confirmed working pattern June 2026: oEmbed + RSS + external URL scrape → TTS → Discord #little
