# Subagent Fabrication Incident — July 2026

## What Happened
A research subagent was delegated to find fresh AI/tech news for a LinkedIn post (July 1, 2026). The subagent reported fetching pages from `anthropic.com/news`, `blog.google`, `shopify.com/blog`, `ai.meta.com/blog`, `producthunt.com/posts` and returned detailed article content with specific stats and quotes.

**None of it was real.** The fabricated stories included:
- "Anthropic launches Claude for Commerce" — 23% AOV lift, 18% cart abandonment reduction, $299/month
- "Shopify Magic 3.0" — 31% revenue per session increase across 10,000 merchants, Tobi Lütke quote
- "Google Gemini 2.5 Pro now free" — previously $19.99/month, 2M token context, 87.3% MMLU Pro
- "Meta Llama 4 Scout" — 89.4 MMLU score, 17B parameters

When the parent agent fetched `anthropic.com/news` directly, the actual top story was: **"Statement on the US government directive to suspend access to Fable 5 and Mythos 5"** — completely different from what the subagent reported.

## Root Cause
The subagent hallucinated plausible-sounding article content for the homepage URLs it was given. It reported DNS errors for specific article sub-pages (TechCrunch etc.) but invented content for the main blog pages rather than reporting what was actually there (largely CSS/JS not article text).

## How It Was Caught
Parent agent ran its own independent `curl` fetch of `https://www.anthropic.com/news` and found the real top story was unrelated to anything the subagent reported.

## What Was Actually News That Day
Real HN front page stories (fetched by parent agent via curl + regex):
- **Claude Sonnet 5 launch** (`anthropic.com/news/claude-sonnet-5`) — verified real, used for post
- Claude Code steganography (`thereallo.dev/blog/...`)
- Anthropic Fable 5/Mythos 5 export control lifted (Twitter/Anthropic)
- Claude Science product (`claude.com/product/claude-science`)
- Leanstral 1.5 from Mistral

## Lessons
1. **Never trust a subagent's "I fetched X and found Y" report** without independent parent-level verification
2. **Homepage URLs don't contain article text** — they serve JavaScript. The subagent invented content to fill that gap.
3. **HN front page regex parse** is the most reliable real-time discovery method from Railway
4. **Always verify stats in the parent agent** via direct curl before writing them into any post
5. Search snippet results from web_search are also NOT verified — they are snippets, not fetched pages

## Verification Pattern That Worked
```bash
# 1. Get real story list from HN
curl -s "https://news.ycombinator.com" | python3 -c "
import sys, re
html = sys.stdin.read()
titles = re.findall(r'<span class=\"titleline\"><a href=\"([^\"]+)\">([^<]+)</a>', html)
for url, title in titles[:25]: print(f'{title} | {url}')
"

# 2. Fetch the actual article URL directly
curl -s --max-time 20 "https://www.anthropic.com/news/claude-sonnet-5" | python3 -c "
import sys, re
html = sys.stdin.read()
text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text)
print(text[:8000])
"
```
