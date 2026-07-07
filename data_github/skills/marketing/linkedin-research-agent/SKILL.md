---
name: linkedin-research-agent
description: >
  Research and verify news roundups, tech/AI stories, statistics, and claims before
  the user posts them on LinkedIn (or any social platform). Use this skill whenever
  the user shares a news roundup, article draft, list of stories, or individual
  claims and asks anything like "is this authentic?", "check this data", "can I post
  this?", "fact check my post", "verify before I publish", "is this real?", or
  pastes a LinkedIn-style post containing factual claims — even if they don't say
  the word "fact-check". Also use it when the user asks to research a topic FOR a
  future LinkedIn post. Produces a per-story verdict, corrected rewrites for
  anything misleading, and a post-ready version.
triggers:
  - "is this authentic"
  - "check this data"
  - "can I post this"
  - "fact check"
  - "verify before I publish"
  - "is this real"
  - "fact check my post"
  - "verify this"
  - "check these stories"
  - "is this accurate"
  - "research this topic for linkedin"
  - "research mode"
  - "verify mode"
  - "can I use this"
  - "is this safe to post"
---

# LinkedIn Research Agent

Verify every factual claim in content the user intends to publish, then hand back a
publish-ready version. The audience on LinkedIn includes domain experts who will
publicly call out errors, so the bar is: **every story must survive a hostile
expert reader.**

Two modes — detect from the user's request:

- **Verify mode** (default): the user pastes content (roundup, post draft, article,
  screenshot text) → verify it story-by-story, fix what's wrong, return a
  post-ready version.
- **Research mode**: the user asks you to research a topic to CREATE a LinkedIn
  post → gather from primary sources first, then draft, so nothing needs
  fact-checking afterwards. Every claim in the draft must carry a source you
  actually read.

---

## Verify Mode — Workflow

### Step 1: Decompose

Split the content into stories/items. Within each, extract the individual
checkable claims:

- **Core claim** — the headline fact (X released Y, X ranked first, X costs $Z)
- **Numbers** — prices, benchmarks, dates, percentages, model sizes. Check each
  number separately; roundups most often get the framing of a number wrong, not
  the number itself (e.g. "per million words" vs "per million tokens", input
  price vs output price).
- **Superlatives & firsts** — "first", "best", "topped the charts", "beats X".
  These are the highest-risk claims. A model can be #1 *among open models* and
  #4 *overall* — the difference decides whether the post is accurate or
  misleading.
- **Recency claims** — "new", "just launched", "this week". Verify the actual
  date; projects are often months old.
- **Meta-claims** — lines like "all stories independently verified". Treat as a
  claim about the whole document.
- Skip pure opinions and predictions — mark them "not checkable" and move on.

### Step 2: Search — primary sources first

For each story, run web_search (1–2 searches per story is usually enough; add
web_fetch when a snippet is inconclusive). Source priority:

1. **The primary source itself** — the company's own announcement/blog
   (anthropic.com, amd.com, the GitHub repo, the Hugging Face page), official
   product/retail listings, the actual paper.
2. **Independent benchmarkers / wire-quality tech press** — Artificial Analysis,
   Reuters, AP, VentureBeat, Axios, StorageReview-class outlets.
3. Blogs, aggregators, HN/Reddit — only as supplementary; a Show HN post proves a
   project *exists* but its performance numbers are developer-reported until an
   independent test confirms them.

Rules:
- Search superlative claims from the opposite direction too ("GLM-5.2 ranking
  overall" not just "GLM-5.2 first place") to catch cherry-picked framing.
- Never mark a claim confirmed from a single low-tier source.
- If the topic post-dates your knowledge, that is exactly why you search —
  never judge recent tech news from memory.

### Step 3: Verdict per story

Assign each story one of:

| Verdict | Meaning | Action for the post |
|---|---|---|
| ✅ CONFIRMED | Primary source + independent coverage agree | Post as-is |
| ✅ CONFIRMED (nuance) | True, but a minor detail needs softening | Give the one-line softening |
| ⚠️ MISLEADING | Real event, wrong framing (the dangerous case) | Provide a corrected rewrite |
| ❓ UNVERIFIED | Exists, but a specific figure has no independent confirmation | Attribute it: "the developer reports…" |
| ❌ FALSE | Contradicted by evidence | Cut it |

The most common failure in roundups is **MISLEADING, not FALSE**: the story is
real but a superlative, comparison, or unit is inflated. Always state exactly
which words are wrong and why.

### Step 4: Deliver

Structure the response as:

1. **One-line overall verdict up top** — e.g. "6 of 7 stories are authentic;
   Story 1 is misleading as written — fix it before posting."
2. **Per-story verdicts** with the key evidence, citing sources.
3. **Corrected rewrites** for every ⚠️/❌ item — ready to paste, keeping the
   user's tone and hook strength. Don't just criticize; give them the accurate
   version that is still a strong post.
4. **Softening suggestions** for nuance items ("say 'the developer reports
   ~5ms'", "change 'new' to 'gaining traction'").
5. **Meta-claim check**: if the post claims "verified against primary sources",
   state whether that's now honest after the fixes.
6. End with a one-sentence disclaimer that this is AI-assisted analysis, not a
   definitive fact-check.

Keep it conversational prose per story — no giant tables, no HTML unless the
user asks for a card/report.

---

## Research Mode — Workflow

When the user wants a post *created* from research:

1. Clarify the angle only if genuinely ambiguous; otherwise pick the strongest
   verifiable angle and proceed.
2. Search primary sources first (official announcements, papers, repos), then
   independent coverage for context and skeptical takes.
3. Draft the post with LinkedIn conventions: strong hook, short paragraphs,
   concrete numbers with correct units, no invented superlatives, 3–6 relevant
   hashtags, and a closing insight that ties the items together.
4. Every number and superlative in the draft must trace to a source found in
   step 2 — apply Step 3's verdict standard to your own draft before showing it.
5. List the sources under the draft so the user can defend the post in comments.

---

## ⚡ MASTER CHECKLIST — Load Before Every Run

Before doing ANYTHING — research, writing, verifying, posting — load and run through:
`references/master-checklist.md`

This is the single source of truth for ALL instructions: research rules, unit errors to avoid, the 8-rule verification gate, writing rules, post format, deliverables, audience, and known pitfalls. Every new instruction Rajeev gives gets added here first.

**Rule: if an instruction isn't in the master checklist, add it there before acting on it.**

---

## Hard Rules (both modes)

- Never confirm a claim you didn't search. "Sounds plausible" is not a verdict.
- Distinguish "no evidence found" (UNVERIFIED) from "evidence contradicts"
  (FALSE) — never conflate them.
- **Tokens ≠ words.** Input price ≠ output price. #1 in a category ≠ #1 overall.
  Vendor benchmark ≠ independent benchmark. Flag every such conflation.
- Preserve the user's voice in rewrites — fix facts, not style.
- If the user's related fact-check skill (e.g. a full HTML Fact-Check Card
  skill) is installed and they explicitly ask for a card/detailed report, hand
  off to that skill; this skill's default output is a fast, post-ready text verdict.

---

## Integration with linkedin-ai-news-post skill

- This skill handles **verification and research** — the raw fact-checking layer.
- The `linkedin-ai-news-post` skill handles **formatting and publishing** — images,
  Drive upload, tone, hooks, hashtags.
- Typical flow: run this skill first to verify/research → hand the cleaned data
  to `linkedin-ai-news-post` to format and publish.
- If the user asks to "write a post about X", and X requires research (not just
  today's news), use **Research Mode** here first, then hand off.

---

## Common Pitfalls

- **"Per million words" vs "per million tokens"** — tokens are roughly 0.75 words.
  API pricing is always quoted per million *tokens*, never per million *words*.
  Always correct this unit error in any post that says "per million words."
- **Benchmark cherry-picking** — "ranked #1" is only valid if it covers ALL
  comparable models. If the benchmark pool excludes major proprietary models,
  say "#1 among models tested" not "#1 overall."
- **Vendor self-reporting vs independent tests** — performance claims from a
  GitHub README, a demo page, or a developer blog are self-reported. Never
  present them as independently confirmed unless a third-party test source agrees.
- **Cutoff confusion** — if researching recent news (last 7 days), always fetch
  live via web_search. Do NOT rely on training data for current events.
- **"Just launched" vs old news** — always check the actual release date.
  Projects trending on HN/Reddit are often weeks or months old.
- **Recency of #1 claims** — benchmark leaderboards update daily. A "#1" claim
  from a blog post may already be stale. Check the live leaderboard.
