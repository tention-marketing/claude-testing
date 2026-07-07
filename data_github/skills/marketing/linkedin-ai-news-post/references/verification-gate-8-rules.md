# Verification Gate — All 8 Rules (Mandatory Before Any Post)

A post MUST NOT be output as "ready to post" unless every rule below passes.
If any claim fails → either drop the claim OR output the whole post as **DRAFT — NOT VERIFIED**.

---

## RULE 1 — PROOF, NOT LABELS
For each factual claim (event, stat, date, price, name), paste the EXACT sentence from the fetched page that supports it + the URL it came from.
No supporting sentence = claim fails.
A "[VERIFIED]" tag with no quoted sentence behind it = treated as unverified.

## RULE 2 — REAL ARTICLES ONLY, NEVER FEEDS
Source must be a specific dated article or official announcement/docs page.
These NEVER count as verification:
- Homepages (techcrunch.com, theverge.com)
- Category/tag/feed pages (…/category/ai, …/tag/…)
- Search result pages or snippets you did not open

If the only "sources" for a claim are feeds or homepages → kill the claim.

## RULE 3 — URLS COME FROM FETCHES, NEVER FROM MEMORY
Only cite a URL that literally appeared in your search or fetch results this run.
Never construct a plausible-looking URL, never recall one from training.
If you cannot produce a fetched URL for a claim → the claim fails.

## RULE 4 — PRIMARY SOURCE OVERRIDES THE HOOK
For any product/company claim, check the primary source (company's own docs, release notes, pricing, or newsroom).
If the primary source contradicts the story — or says nothing about it — the story is wrong.
Primary source wins over any blog, aggregator, or assumption.

## RULE 5 — "TODAY/JUST/NOW" NEEDS A DATED ARTICLE FROM TODAY
Any freshness claim (launched today, just announced, now free) requires a dated article published within the last 48 hours that explicitly states it.
No such article = downgrade to a general observation or drop it.

## RULE 6 — NUMBERS ARE GUILTY UNTIL PROVEN
Every %, multiple, dollar figure, and count must appear verbatim in a fetched page, quoted under Rule 1.
Do not round, combine, or "estimate" a number into existence.
If a specific figure can't be sourced → use qualitative language ("rising", "cheaper") or drop it.

## RULE 7 — STALENESS CHECK
Before calling something "the newest/best/most powerful X", confirm nothing has superseded it.
Check for a newer version or a retirement/sunset notice.
A model, feature, or product that has been replaced or is being retired is NOT "the latest."

## RULE 8 — WHEN IN DOUBT, FLAG — DON'T FABRICATE
If you cannot verify something, output the claim marked [UNVERIFIED] with what you tried.
Never invent a source, a number, a quote, or a verification tag to fill the gap.
A vaguer true post always beats a precise false one.

---

## Post Output States
- ✅ **READY TO POST** — all 8 rules pass for every claim
- ⚠️ **DRAFT — NOT VERIFIED** — one or more claims failed, flagged inline

---

## Quick Checklist (run silently before output)
- [ ] Every stat has an exact quoted sentence + fetched URL behind it (Rule 1)
- [ ] All sources are specific dated articles, not feeds or homepages (Rule 2)
- [ ] Every URL was fetched this run, not recalled from memory (Rule 3)
- [ ] Primary source checked for all product/company claims (Rule 4)
- [ ] Any "today/just/now" claim backed by article dated within 48h (Rule 5)
- [ ] Every number appears verbatim in a fetched page (Rule 6)
- [ ] "Latest/best/most powerful" claims checked for successors (Rule 7)
- [ ] Unverifiable claims flagged [UNVERIFIED] or dropped (Rule 8)
