# Godot Post — Gold Standard Verification Example (July 1, 2026)

## Why This Example Matters
This post followed the correct end-to-end workflow after the subagent fabrication incident earlier the same session. It shows the right pattern: HN discovery → official source fetch → verbatim quotes → clean post.

## Story Discovery
- Source: `news.ycombinator.com` front page, fetched directly with curl + python3
- Title seen: "Godot will no longer accept AI-authored code contributions"
- HN link pointed to: `https://www.pcgamer.com/...` (third-party, body not readable)

## Primary Source Verification
- Fetched `https://godotengine.org/blog/` → found `contribution-policy-2026` URL
- Fetched `https://godotengine.org/article/contribution-policy-2026/` directly
- Article body loaded fully — all quotes confirmed verbatim

## Verified Claims Used in Post
| Claim | Verbatim from page | Source |
|---|---|---|
| Date: June 30, 2026 | "By: Godot Foundation 30 June 2026" | godotengine.org/article/contribution-policy-2026/ |
| Can't trust AI users to fix code | "we can't trust heavy users of AI to understand their code enough to fix it" | same |
| Demoralizing for reviewers | "If your feedback on PRs is just being absorbed by a machine and not going towards mentoring a potential future maintainer, it becomes much harder to justify spending your free time on PR review." | same |
| Banned: AI agents, vibe coding | "No autonomous AI agent use or vibe coding" | same |
| Banned: AI-generated code | "No use of AI to generate substantial pieces of code... We require all code to be human authored." | same |

## What Was NOT Used
- PCGamer article body (unreadable — only JSON/nav returned)
- Any search snippet stats
- Any number claims (none in post — qualitative language used throughout)

## Key Lesson
When the linked article from HN is a third-party site that doesn't load cleanly, go find the **official source** directly. In this case: HN → PCGamer (failed) → godotengine.org/blog/ → correct URL found → full body fetched. Always one more step to the primary source.

## The Post (approved / published)
> One of the most popular open-source engines just banned AI-generated code. Completely.
> Godot published its new contribution policy on June 30. The rule: no AI-generated code, no vibe coding, no AI agents submitting PRs.
> "We can't trust heavy users of AI to understand their code enough to fix it."
> ...
> What's your line between AI-assisted and AI-authored? Where do you draw it?
> #AI #OpenSource #SoftwareDevelopment #AITools #Developers

## Why It Worked
- Hook names a specific concrete action (banned, completely) — not vague
- Every quote is verbatim from the official source
- No numbers invented — qualitative language throughout (Rule 6 compliance)
- Contrarian angle: pushback isn't from AI-fearers, it's from burned-out maintainers
- Discussion question is genuinely strategic
