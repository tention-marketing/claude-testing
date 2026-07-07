#!/usr/bin/env python3
"""
Scrape ALL videos from a YouTube channel using the internal browse API.
Works as of June 2026. Uses lockupViewModel (new format) + shortsLockupViewModel.
No API key required. Completes in <60s for 400+ video channels.

Usage:
    python3 scrape_channel_browse_api.py
Output:
    /root/channel_videos.json  — list of all video dicts
"""
import requests, json, sys

CHANNEL_ID = "UC2ojq-nuP8ceeHqiroeKhBA"  # Nate Herk — change as needed
OUTPUT_FILE = "/root/channel_videos.json"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/json',
}

def browse(browse_id=None, params=None, continuation=None):
    payload = {"context": {"client": {"clientName": "WEB", "clientVersion": "2.20231121.08.00"}}}
    if continuation:
        payload["continuation"] = continuation
    else:
        payload["browseId"] = browse_id
        payload["params"] = params
    r = requests.post('https://www.youtube.com/youtubei/v1/browse',
                      headers=HEADERS, json=payload, timeout=30)
    return r.json()

def parse_lockup(item_content):
    """Parse lockupViewModel → video dict. Returns None if not a video."""
    vm = item_content.get('lockupViewModel', {})
    if not vm:
        return None
    vid_id = vm.get('contentId', '')
    metadata = vm.get('metadata', {}).get('lockupMetadataViewModel', {})
    title = metadata.get('title', {}).get('content', '')
    rows = metadata.get('metadata', {}).get('contentMetadataViewModel', {}).get('metadataRows', [])
    views, published = 0, ''
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
    duration, duration_secs = '', 0
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
    return {'video_id': vid_id, 'title': title, 'duration': duration,
            'duration_secs': duration_secs, 'views': views, 'published': published,
            'type': 'Short' if is_short else 'Long', 'is_short': is_short,
            'url': f'https://www.youtube.com/watch?v={vid_id}'}

def parse_short_item(obj):
    """Parse shortsLockupViewModel → video dict. Returns None if not a short."""
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

def scrape_shorts_recursive(obj, depth=0):
    results = []
    if depth > 25: return results
    if isinstance(obj, dict):
        v = parse_short_item(obj)
        if v: results.append(v)
        else:
            for val in obj.values(): results.extend(scrape_shorts_recursive(val, depth+1))
    elif isinstance(obj, list):
        for item in obj: results.extend(scrape_shorts_recursive(item, depth+1))
    return results

# Step 1: Get correct tab params dynamically
print(f"Fetching channel tabs for {CHANNEL_ID}...", flush=True)
data = browse(CHANNEL_ID, "EgZ2aWRlb3PyBgQKAjoA")
tabs = data['contents']['twoColumnBrowseResultsRenderer']['tabs']
videos_params = tabs[1]['tabRenderer']['endpoint']['browseEndpoint']['params']
shorts_params  = tabs[2]['tabRenderer']['endpoint']['browseEndpoint']['params']
print(f"Videos params: {videos_params}")
print(f"Shorts params:  {shorts_params}")

# Step 2: Scrape long-form videos
print("\nScraping Videos tab...", flush=True)
all_videos = []
page = 1
data = browse(CHANNEL_ID, videos_params)
tabs2 = data['contents']['twoColumnBrowseResultsRenderer']['tabs']
contents = tabs2[1]['tabRenderer']['content']['richGridRenderer']['contents']
for item in contents:
    if 'richItemRenderer' in item:
        v = parse_lockup(item['richItemRenderer'].get('content', {}))
        if v: all_videos.append(v)
token = find_continuation(contents)
while token:
    page += 1
    data = browse(continuation=token)
    new_items = []
    for action in data.get('onResponseReceivedActions', []):
        new_items.extend(action.get('appendContinuationItemsAction', {}).get('continuationItems', []))
    for item in new_items:
        if 'richItemRenderer' in item:
            v = parse_lockup(item['richItemRenderer'].get('content', {}))
            if v: all_videos.append(v)
    token = find_continuation(new_items)
    print(f"  Page {page}: total long-form = {len(all_videos)}", flush=True)
    if page > 50: break
print(f"Total long-form: {len(all_videos)}")

# Step 3: Scrape Shorts
print("\nScraping Shorts tab...", flush=True)
shorts = []
data = browse(CHANNEL_ID, shorts_params)
shorts.extend(scrape_shorts_recursive(data))
token = find_continuation(data)
while token:
    data = browse(continuation=token)
    shorts.extend(scrape_shorts_recursive(data))
    token = find_continuation(data)
    print(f"  Shorts so far: {len(shorts)}", flush=True)
    if len(shorts) > 5000: break
print(f"Total shorts: {len(shorts)}")

# Step 4: Save
all_combined = all_videos + shorts
print(f"\nGrand total: {len(all_combined)} (Long: {len(all_videos)}, Shorts: {len(shorts)})")
with open(OUTPUT_FILE, 'w') as f:
    json.dump(all_combined, f, indent=2)
print(f"Saved to {OUTPUT_FILE}")
