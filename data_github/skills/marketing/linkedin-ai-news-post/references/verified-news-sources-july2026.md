# Verified AI News Sources — Fetch Reliability Map (July 2026)

Confirmed from live fetches on 2026-07-07. Re-check periodically as sites change.

## ✅ Reliable — fetch directly with urllib

| Source | URL Pattern | What you get |
|--------|-------------|-------------|
| Hacker News | `news.ycombinator.com` | Full front page HTML; parse titleline spans with regex |
| Anthropic Newsroom | `anthropic.com/news` | Title list + dates in readable text |
| Anthropic Research | `anthropic.com/research/<slug>` | Full article body loads cleanly |
| Artificial Analysis | `artificialanalysis.ai/models/<model-slug>` | Intelligence Index score, rank/N, speed (tok/s), price ($/MTok), context window |
| Hugging Face Daily Papers | `huggingface.co/papers` or `huggingface.co/papers?date=YYYY-MM-DD` | Paper titles + upvote counts |
| GitHub Raw README | `raw.githubusercontent.com/<owner>/<repo>/main/README.md` | Clean markdown, no JS noise |
| LTT Labs | `lttlabs.com/articles/YYYY/MM/DD/<slug>` | Full hardware review with specs and pricing |
| Zhipu AI | `zhipuai.cn` | Homepage with model summaries; contains Artificial Analysis rank quotes (in Chinese) |
| martinalderson.com | Any post URL | Full article body, JSON-LD metadata with datePublished |
| IEEE Spectrum | `spectrum.ieee.org/<slug>` | JSON-LD metadata (headline, date, description); article body may be paywalled |

## ❌ Blocked or unreliable from Railway server

| Source | Reason |
|--------|--------|
| `openai.com/news/` | HTTP 403 Forbidden |
| Reddit (`reddit.com/r/*/`.json) | HTTP 403 Blocked |
| TechCrunch | Turnstile/Cloudflare bot protection |
| The Verge | Heavy JS, minimal readable text from curl |
| Bloomberg | Paywall |

## 🟡 Partial — metadata only

| Source | What loads |
|--------|-----------|
| Google DeepMind blog | Navigation JS only; no article text |
| Product Hunt | Apollo SSR JSON shell; no product names |
| Ars Technica | Snowplow config JS; article list not parseable via simple strip |

## Batched fetch pattern (confirmed working)

```python
from hermes_tools import execute_code

# Inside execute_code:
import urllib.request, re

def fetch_url(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=timeout) as r:
            html = r.read().decode('utf-8', errors='ignore')
        text = re.sub('<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text)
        return text[:6000]
    except Exception as e:
        return f"ERROR: {e}"

sources = {
    "story_name": "https://url.here/",
    "another_story": "https://another.url/",
}

for name, url in sources.items():
    print(f"\n{'='*60}")
    print(f"SOURCE: {name} | {url}")
    print(fetch_url(url)[:2500])
```

## Artificial Analysis model slug convention

Model slugs follow the pattern `artificialanalysis.ai/models/<model-name-lowercase-hyphens>`.
Examples confirmed working:
- `artificialanalysis.ai/models/glm-5-2` → GLM-5.2 (returns rank, score, price, speed)

The page renders "Intelligence Index" score (0–100 scale), rank out of total models evaluated, 
input/output price per 1M tokens, and tokens/second speed. All values appear in plain text after 
tag stripping — no JS required to get the numbers.

## HN title extraction regex (confirmed working)

```python
import re
html = ... # curl/urllib fetch of news.ycombinator.com
titles = re.findall(r'<span class=\"titleline\"><a href=\"([^\"]+)\">([^<]+)</a>', html)
for url, title in titles[:30]:
    print(f"{title} | {url}")
```

Note: HN item URLs (starting `item?id=`) are job postings — skip them for news research.
