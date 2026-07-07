# ✅ MASTER PRE-PUBLISH CHECKLIST
# One place. All instructions. Check EVERYTHING against this before any post goes out.
# Updated: July 2026 — Rajeev's standing orders

---

## 🔴 BEFORE YOU RESEARCH (run every single time)

- [ ] Check the real system date — never assume the year
- [ ] Only use news from the LAST 24 HOURS — discard anything older (or label as "context only")
- [ ] Do NOT rely on training memory for current events — always fetch live pages
- [ ] Use `execute_code` + urllib for fetches — avoid `curl | python3` (triggers security gate)

---

## 🔴 DURING RESEARCH — SOURCE RULES

- [ ] **Primary source first** — company blog, official repo, official newsroom. Not an aggregator.
- [ ] **2 independent sources** for any number or superlative claim — or label it "[developer reports]"
- [ ] **Never fabricate** a URL, stat, quote, or story detail — not even a plausible-looking one
- [ ] **Subagent output is NOT trusted** until you independently fetch and confirm the source URL yourself
- [ ] **Feed pages don't count** — techcrunch.com/category/ai, reddit.com/r/LocalLLaMA — these are NOT sources. Open the actual article.
- [ ] **Search superlatives from both directions** — "GLM first place" AND "GLM overall ranking" — to catch cherry-picking

### Verified sources that load from Railway (July 2026):
| Source | What you get |
|---|---|
| `news.ycombinator.com` | HN front page — parse titleline spans for story URLs |
| `anthropic.com/news` | Newsroom index — titles + dates load cleanly |
| `anthropic.com/research/<slug>` | Individual research papers — load cleanly |
| `artificialanalysis.ai/models/<slug>` | Live benchmark: score, rank, speed, price |
| `huggingface.co/papers` | Daily papers + upvote counts |
| `lttlabs.com` | Hardware reviews with full specs and pricing |
| `raw.githubusercontent.com/<owner>/<repo>/main/README.md` | GitHub README (use raw, not github.com page) |
| `zhipuai.cn` | GLM model pages (Chinese) |
| `spectrum.ieee.org` | JSON-LD metadata loads; article body may be paywalled |

### Blocked from Railway — DO NOT ATTEMPT:
- TechCrunch, Reddit, Bloomberg, Reuters, The Verge — all blocked or paywalled

---

## 🔴 CLAIM-BY-CLAIM VERIFICATION RULES

### Units (the #1 error in AI posts)
- [ ] **Tokens ≠ words** — API pricing is ALWAYS per token, never per word. 1 token ≈ 0.75 words. Correct any "per million words" to "per million tokens"
- [ ] **Input price ≠ output price** — always specify which. Default to input price when citing a single number
- [ ] **#1 in a category ≠ #1 overall** — always name the benchmark pool (e.g. "among 93 models tested")
- [ ] **Vendor benchmark ≠ independent benchmark** — developer-reported specs from a README/demo page are self-reported. Say "the developer reports" unless independently confirmed
- [ ] **"Just launched" needs a date** — check the actual release date; HN trending ≠ new today

### Superlatives — highest risk, always double-check
- [ ] "First ever" — actually verify no prior art
- [ ] "Best in class" — name the class and the benchmark
- [ ] "Beats X" — confirm X is in the benchmark pool and not excluded
- [ ] "#1 overall" — confirm the pool includes all major competitors

### Freshness
- [ ] "New" / "just released" / "this week" — must have a dated article from the last 48h
- [ ] If you can't find a dated article → downgrade to "gaining traction" or drop it

---

## 🔴 THE 8-RULE VERIFICATION GATE (MANDATORY — every post)

**No post ships as "READY TO POST" unless all 8 pass.**

**RULE 1 — PROOF, NOT LABELS**
For every factual claim: paste the EXACT sentence from the fetched page that supports it + the URL. A "[VERIFIED]" tag with no quoted sentence is treated as unverified.

**RULE 2 — REAL ARTICLES ONLY**
Source must be a specific dated article or official announcement. Homepages, category pages, search results = NOT a source. If your only source is a feed page, the story does not exist. Kill it.

**RULE 3 — URLS FROM FETCHES ONLY**
Only cite a URL that appeared in your search/fetch results this run. Never construct a URL from memory. No URL from this run = claim fails.

**RULE 4 — PRIMARY SOURCE OVERRIDES EVERYTHING**
Check the company's own docs/newsroom/release notes. If the primary source contradicts the blog post you found — the blog post is wrong. Primary source always wins.

**RULE 5 — "TODAY/JUST/NOW" NEEDS A DATED ARTICLE**
Any freshness claim = dated article published within 48h that explicitly says so. No dated article = drop the freshness language.

**RULE 6 — NUMBERS ARE GUILTY UNTIL PROVEN**
Every %, $, multiple, and count must appear VERBATIM in a fetched page (Rule 1). No estimating, rounding, or combining numbers. If you can't source it verbatim → use qualitative language or drop it.

**RULE 7 — STALENESS CHECK**
Before saying "newest/best/most powerful" — check if something has superseded it. A replaced or retired product is NOT "the latest."

**RULE 8 — WHEN IN DOUBT, FLAG — DON'T FABRICATE**
Mark uncertain claims [UNVERIFIED]. Never invent a source or number to fill a gap. A vaguer true post always beats a precise false one.

---

## 🔴 WRITING RULES (every post)

### Voice & tone
- [ ] No AI tells: "game-changer", "revolutionary", "groundbreaking", "the future is here", "AI is changing everything"
- [ ] No filler verbs: "delve", "leverage", "harness", "unlock", "elevate", "supercharge"
- [ ] No AI cadences: "It's not just X — it's Y", "Here's the kicker", "Here's the thing", "Let that sink in"
- [ ] No throat-clearing openers: "In today's fast-paced world / digital age"
- [ ] No fake urgency. No robotic writing. No generic hype with no substance.
- [ ] No emoji stacking — ONE emoji max, only if it adds something
- [ ] No fake first-person stories — real specifics only

### Structure (every LinkedIn post)
1. **Hook** — stops the scroll. Specific claim, number, tension, or short story. First 1-2 lines only.
2. **What happened** — clear, 2-4 short lines
3. **Why it matters** — impact for founders/builders/marketers
4. **Practical takeaway** — action someone can take tomorrow
5. **Smart opinion** — a clear point of view, not a recap
6. **Discussion question** — a real one, not "What do you think? 👇"
7. **Hashtags** — 3-5, specific, at the very end

### Length
- Single-story post: **120–220 words** (tight is better)
- Roundup post (multiple stories): **50-80 words per story** + 2-3 sentence closer + hashtags

### Hashtags — tailor to the actual content
- Always include: `#AI #ArtificialIntelligence`
- Add topic-specific: `#Cybersecurity` (security), `#OpenSource` (open-source tools), `#LLM` (models), `#Ecommerce` (DTC/Shopify stories), `#MachineLearning` (research), `#AITools` (tools)
- Max 8 hashtags for a roundup

---

## 🔴 POST FORMAT RULES (roundup posts specifically)

- [ ] Title line: `🤖 AI News Roundup — [Date]`
- [ ] Subtitle: `(All stories independently verified against primary sources)` — only include this if they actually were
- [ ] Story numbering: Unicode bold numerals — 𝟭 𝟮 𝟯 𝟰 𝟱 𝟲 𝟳 𝟴 𝟵
- [ ] Horizontal rule `---` between every story
- [ ] **Rewrite headlines** — not the raw source headline; make it scannable, active voice, no jargon
- [ ] **Correct spin** — if a source says "#1 overall" but it's "#1 in a subcategory", correct it in the post
- [ ] **No verification methodology** in the post — no tables, verdict badges, model names used for checking. That's the backend report only.
- [ ] **Closing paragraph** — 2-3 sentences synthesizing the theme across stories. Not a recap list.

---

## 🔴 MANDATORY DELIVERABLES (every full run — no exceptions)

- [ ] **Post text** — saved locally to `/app/data/linkedin_posts/linkedin_post_YYYY-MM-DD.txt`
- [ ] **Image** — generated via OpenAI API (`gpt-image-1`, 1024×1536, quality medium). Saved to `/tmp/linkedin_ai_image.png`. Write script to file first, then run — never use heredoc for API calls.
- [ ] **Google Drive upload** — post doc + image → `daily-post-linkedin/YYYY-MM-DD/` subfolder. Root folder ID: `1jhlQkTd7bwFuX3UWwqkVeet6LFvG8v0-`
- [ ] **Share links** — folder link + doc link + image link delivered to Rajeev
- [ ] **Show image in chat** — `MEDIA:/tmp/linkedin_ai_image.png` in the reply

Any missing deliverable = incomplete run. Do not stop early.

---

## 🔴 DUAL-MODEL VERIFICATION (for news briefings / cross-check requests)

When Rajeev asks for a verified briefing, dual-check, or cross-verification:
- **Layer 1:** Claude (this agent) — live source fetches. Ground truth.
- **Layer 2:** GPT-4o via `/app/data/openai_key.txt`
- **Layer 3:** GPT-4.1 via OpenAI API

Key rules:
- `gpt-5` (bare) returns HTTP 404 — use `gpt-4o` + `gpt-4.1`
- Both GPT models have cutoffs before July 2026 — "Uncertain" = plausible post-cutoff, NOT a red flag
- "Contradicts" from one GPT with known cutoff gap = ⚠️ PARTIAL, not ❌ FLAGGED
- ❌ FLAGGED only when Claude cannot confirm from a live source OR both models flag contradiction

---

## 🔴 RAJEEV'S AUDIENCE — always weight toward this

- Ecommerce founders
- Shopify brand owners
- Email marketers
- DTC (direct-to-consumer) operators

When scoring stories or choosing angles, prioritise what this audience can ACT on tomorrow. Never write a post that only matters to ML researchers.

---

## 🔴 COMMON ERRORS CAUGHT THIS SESSION (July 2026)

| Error | What happened | Fix |
|---|---|---|
| "per million words" | Used wrong unit — API pricing is per TOKEN not per word | Always say "per million tokens" |
| Subagent fabrication | Research subagent invented entire articles (Claude for Commerce, Shopify Magic 3.0) that didn't exist | Always independently verify subagent claims by fetching the source URL yourself |
| gpt-5 bare ID | Returns HTTP 404 from this account | Use gpt-4o + gpt-4.1 as the two verifiers |
| curl pipe python3 | Triggers security approval gate | Use execute_code + urllib instead |
| "#1 overall" | GLM-5.2 is #1 among 93 models tested — pool may not include all models | Say "among [N] models tested on [benchmark name]" |
| Post not saved to Drive | Only saved locally | Always upload to Drive AND share the link |
