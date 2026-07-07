# Dual-Model AI News Verification Pattern
*Captured July 7, 2026 — from live session running 7-story cross-verification*

## When to use
When Rajeev requests a **verified news digest** or explicitly asks to "cross-verify with two AI models" — not standard LinkedIn post runs. This adds ~2–3 minutes of API calls but produces a publishable confidence table.

## Architecture

| Layer | Model | Role |
|---|---|---|
| Layer 1 (primary) | Claude (this agent) | Live urllib fetches — the ground truth. Reads actual page content. |
| Layer 2 | GPT-4o | Cross-check for plausibility, flag contradictions or fabrications |
| Layer 3 | GPT-4.1 | Independent second opinion, different training run, stricter cutoff |

## Verdict logic

| Condition | Verdict |
|---|---|
| Claude confirmed from live source + both GPT = Uncertain (plausible) | ✅ VERIFIED |
| Claude confirmed from live source + one GPT = Contradicts | ⚠️ PARTIAL |
| Claude CANNOT confirm from source OR both GPT = Contradicts | ❌ FLAGGED |

**Critical interpretation rule:** Both GPT models have knowledge cutoffs BEFORE the present date. "Contradicts" from a GPT model on a recent story most often means the story post-dates its training — not that the story is false. Always explain the discrepancy; never suppress it.

## API call pattern (confirmed working July 2026)

```python
import urllib.request, json, time

openai_key = open('/app/data/openai_key.txt').read().strip()

PROMPT = """You are a fact-checker for AI industry news. Assess this recent story's plausibility.

Respond in EXACTLY this format:
VERDICT: [Confirmed / Uncertain / Contradicts]
REASONING: [2-3 sentences]
CUTOFF_NOTE: [yes/no/partial - whether within your training data]

Story: {headline}
Details: {summary}
Source: {source}"""

def call_openai(story, model):
    prompt = PROMPT.format(**story)
    data = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 250,
        "temperature": 0.1
    }).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=data, method="POST",
        headers={"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        result = json.loads(r.read())
    return result['choices'][0]['message']['content'].strip()

def parse_verdict(r):
    u = r.upper()
    if "VERDICT: CONFIRMED" in u: return "Confirmed"
    if "VERDICT: CONTRADICTS" in u: return "Contradicts"
    return "Uncertain"

# Run both models on all stories (rate-limit courtesy sleep)
for story in STORIES:
    r4o = call_openai(story, "gpt-4o")
    time.sleep(0.3)
    r41 = call_openai(story, "gpt-4.1")
    time.sleep(0.3)
```

## Known model routing (July 2026)

| Model ID | Status |
|---|---|
| `gpt-4o` | ✅ Works, returns structured responses |
| `gpt-4.1` | ✅ Works, knowledge cutoff ~June 2024, stricter |
| `gpt-4.1-2025-04-14` | ✅ Versioned alias |
| `gpt-5` (bare) | ❌ HTTP 404 — do NOT use |
| `gpt-5-2025-08-07` | Likely works (in model list) — test before use |
| `gpt-4o-search-preview` | ❌ HTTP 400 for chat completions format |

Always check `/v1/models` if unsure whether a model ID is live in this account.

## Output format (verified July 2026)

Deliver as:
1. Methodology table (3 layers explained)
2. Summary verification table (all stories, verdicts in one view)
3. Per-story detail blocks (Claude source evidence + GPT-4o response + GPT-4.1 response + discrepancy explanation)
4. Final summary counts (✅ / ⚠️ / ❌)

## Pitfalls

- **Don't batch GPT calls inside one execute_code call without sleep.** Rate limit courtesy: 0.3s between calls.
- **STORIES dict must be redefined in each execute_code block** — variables do not persist between calls.
- **GPT-4.1 "Contradicts" is not the same as "fabricated."** Always explain the cutoff gap in the discrepancy note.
- **Never suppress a discrepancy** — if models disagree, explain it in one sentence. The user is relying on this for publishing decisions.
- **Claude's live fetch IS the ground truth.** A GPT "Contradicts" on a story Claude read directly from an official source page should be classified ⚠️ PARTIAL, not ❌ FLAGGED.
