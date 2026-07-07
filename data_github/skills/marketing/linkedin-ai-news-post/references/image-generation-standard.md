# LinkedIn Post Image Generation Standard

## Approved Format (from Rajeev, June 2026)

**Size:** 1080×1350px (4:5 portrait) — LinkedIn optimal  
**Engine:** Python Pillow + matplotlib via `terminal()` heredoc  
**Font:** `/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf` (confirmed working)  
**Save path:** `/tmp/linkedin_image1.png` and `/tmp/linkedin_image2.png`

⚠️ Generate images in the MAIN agent's terminal — not in a subagent. Subagent /tmp files do not persist.

---

## Gold Standard Prompt (approved by Rajeev)

This prompt produced the image Rajeev held up as the benchmark:

> A bold, high-contrast vertical marketing graphic (4:5 portrait, 1080×1350) for a LinkedIn/DTC audience, dark navy background with subtle tech-grid texture.
>
> LEFT THIRD: Large punchy headline stacked in white and gold condensed bold sans-serif: "ADS NOW LIVE" (white) / "INSIDE THE AI ANSWER" (gold). Below it, smaller white subhead: "Google's AI Overview is the new first position." Bottom-left: a gold warning-triangle icon next to a blue banner reading: "New placement. Higher CPC. Feed quality wins."
>
> CENTER: A clean, realistic mockup of a Google search results page on a white rounded card. Search bar shows "best running shoes." Below it an "AI Overview" block with a small sparkle icon and a "Sponsored" tag, two lines of generic summary text, and a row of three product cards showing GENERIC unbranded running shoes (no real logos) — neutral labels like "Trail Runner Pro," "Cloud Glide," "Pace X," each with a price and star rating. Small "AI-generated" footer line.
>
> RIGHT THIRD: Two stacked stat callouts in clean panels. Top panel, green up-arrow: "+12% CPC YoY" with smaller text "(WordStream 2026)". Bottom panel, blue icon: "FEED QUALITY = NEW RANKING SIGNAL." Below them a small red rising-line chart labeled "AD COSTS RISING."
>
> BOTTOM CENTER: Back view of 4–5 diverse people in plain dark tees facing the screen, with thought bubbles: "Why aren't we cited?" / "Our ads cost more" / "ROAS slipping" / "What are we missing?"
>
> Style: modern, confident, agency-grade, sharp typography, strong color blocking (navy, white, gold, accents of green and red). No real brand logos or trademarked products anywhere.

---

## Layout Template (3-column + bottom)

```
┌─────────────────────────────────────────────────────────────┐
│ [colour strip top — 4 Google brand colours]                 │
├──────────────┬──────────────────────┬───────────────────────┤
│ LEFT (0-308) │  CENTER (316-716)    │  RIGHT (724-1064)     │
│              │                      │                       │
│ Headline     │  SERP mockup card    │  +12% CPC panel       │
│ white/gold   │  (white rounded)     │  (green border)       │
│              │                      │                       │
│ Bullets      │  - Google wordmark   │  Feed Quality panel   │
│              │  - Search bar        │  (blue border)        │
│ Warning      │  - AI Overview box   │                       │
│ banner       │  - 3 product cards   │  Rising cost chart    │
│              │  - Organic results   │  (red border)         │
│ CTA button   │  - Ad result         │                       │
│ (gold)       │                      │  ROAS panel           │
│              │                      │  Action list          │
├──────────────┴──────────────────────┴───────────────────────┤
│  BOTTOM (BOT_Y=868 → H)  dark section                       │
│  Gold divider line                                          │
│  "What merchants are thinking right now..."                 │
│  5 × silhouette person + coloured thought bubble above      │
│  [red] [yellow] [blue] [green] [gold]                       │
├─────────────────────────────────────────────────────────────┤
│  Bottom bar: hashtags (left) | SHARE THIS INSIGHT (gold R)  │
└─────────────────────────────────────────────────────────────┘
```

## Color Palette

| Element | Hex |
|---|---|
| Background | `#0D1B2A` |
| Grid lines | `#131F30` |
| Bottom section | `#08101A` |
| White text | `#FFFFFF` |
| Gold (headline accent) | `#F4B942` |
| Blue accent | `#4285F4` |
| Green (positive stat) | `#34A853` |
| Red (warning/rising) | `#EA4335` |
| Light text | `#AABBCC` / `#CCDDEE` |
| SERP card bg | `#FFFFFF` |
| AI Overview bg | `#EAF2FF` |

## Column Pixel Boundaries (1080px wide)

```python
LX, LW = 16, 296      # left col: x-start, x-end
CX, CW = 312, 400     # center col: x-start, width
RX, RW = 724, 344     # right col: x-start, width
BOT_Y  = 868          # y where bottom people section starts
```

## Person Silhouette Pattern

```python
# Head
draw.ellipse([px-20, tby+70, px+20, tby+112], fill='#1E3050')
# Body
draw.polygon([(px-26,tby+112),(px+26,tby+112),(px+34,tby+230),(px-34,tby+230)], fill='#182840')
# Arms
draw.line([(px-26,tby+126),(px-50,tby+162)], fill='#182840', width=11)
draw.line([(px+26,tby+126),(px+50,tby+162)], fill='#182840', width=11)
```

## OpenAI API Image Generation — PRIMARY METHOD (gpt-image-1)

Key at `/app/data/openai_key.txt`. This is now the default image generation path.

**Working invocation pattern (CONFIRMED June 2026):**
```python
# Write to file first — do NOT use heredoc for API calls
# File: /tmp/gen_image.py

import urllib.request, json, base64

key = open('/app/data/openai_key.txt').read().strip()
prompt = """[YOUR DETAILED PROMPT]"""

data = json.dumps({
    "model": "gpt-image-1",
    "prompt": prompt,
    "n": 1,
    "size": "1024x1536",
    "quality": "medium"       # "high" reliably times out at 60s limit
}).encode()

req = urllib.request.Request(
    "https://api.openai.com/v1/images/generations",
    data=data, method="POST",
    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
)
with urllib.request.urlopen(req, timeout=300) as r:
    result = json.loads(r.read())

img_b64 = result['data'][0]['b64_json']  # always b64_json — never a URL
with open('/tmp/linkedin_ai_image.png', 'wb') as f:
    f.write(base64.b64decode(img_b64))
print("DONE")
```

Then run: `terminal('cd /tmp && python3 gen_image.py', timeout=300)`

**Available models (confirmed):** `gpt-image-1`, `gpt-image-1-mini`, `gpt-image-1.5`, `gpt-image-2`
**NOT available:** `dall-e-3` → 400 "model does not exist"

**Key settings:**
- size: `1024x1536` (4:5 portrait, closest to 1080×1350)
- quality: `medium` — high times out; medium delivers in ~30-60s
- response: always `b64_json` — decode with `base64.b64decode()`
- timeout: 300s on `urlopen`

**CRITICAL — AI cannot reliably render exact text.** Numbers, labels, and thought bubble text will be garbled. Rajeev accepts this — the visual quality is agency-grade and he uses the image as-is. If exact text matters for a specific post, use hybrid approach: AI base image → Pillow text overlay.

**Prompt structure that produced Rajeev-approved output:**
```
A bold, high-contrast vertical marketing graphic (4:5 portrait) for a LinkedIn/DTC audience,
dark navy background with subtle tech-grid texture.
LEFT THIRD: large punchy headline in white bold / gold bold. White subhead. Gold warning
triangle + blue banner with key takeaway.
CENTER: clean [relevant mockup] on white rounded card — e.g. Google SERP, split comparison,
stat card — with specific labels and values.
RIGHT THIRD: 2-3 stat panels (green/blue/red borders). Rising line chart if relevant.
BOTTOM: back view of 5 diverse people in dark tees with colourful thought bubbles containing
short questions/reactions relevant to the post topic.
Style: modern, agency-grade, navy/white/gold/green/red. No real brand logos.
```

## Pitfalls

- **Heredoc + long API call = shell `&` backgrounding error.** If you put a `urllib.urlopen()` call with timeout=300 inside a terminal heredoc (`<< 'EOF'`), the shell treats it as a background process and blocks. Fix: write the script to a file with `write_file()` then run `python3 /tmp/gen_image.py`. This is the confirmed working pattern.
- **Headline clipping**: left column headline font must be ≤46px at 1080×1350 or text overflows into center column
- **Subagent /tmp isolation**: if you generate images in a delegate_task subagent, those files DO NOT exist in the parent session. Always generate images in the main agent via `terminal()`.
- **Empty gap in middle**: if SERP card height < column height, a large navy gap appears below it. Set card height to match column (CH ≈ 845px).
- **execute_code blocked**: in cron/railway contexts, use `terminal()` heredoc for image generation, not execute_code.
- **Pillow not installed**: run `pip install Pillow matplotlib` if ModuleNotFoundError occurs.
