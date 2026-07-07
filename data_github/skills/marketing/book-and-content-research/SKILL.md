---
name: book-and-content-research
description: Research books, authors, and content topics on the internet — finding free/legal access links, chapter structure, author backstory, key concepts, and summary resources. Used when Rajeev asks "can you find this book PDF" or "research this topic for me".
triggers:
  - User asks to find a book PDF or ebook
  - User asks to research a book, author, or topic online
  - User says "can you find this on the internet"
  - User wants a summary or chapter breakdown of a book
  - User asks about an author's personal story or background
---

# Book & Content Research

## Overview
When Rajeev asks to research a book or topic, delegate to a subagent with web + search toolsets. The subagent does parallel deep research across multiple sources and returns structured findings. Do NOT just do a single web search — the value is in comprehensive cross-referencing.

---

## Step 1: Delegate to a Research Subagent

Use `delegate_task` with toolsets `["web", "search"]`. Give the subagent a clear multi-part goal covering:
1. Free/legal download or access links (Archive.org, Open Library, etc.)
2. Key book facts (authors, publisher, year, pages, sales, awards)
3. Chapter structure / table of contents
4. Author personal backstory — how they came to write this book
5. Free summary resources and official author pages

**This always produces better results than doing web searches yourself** — the subagent can batch-fetch many pages concurrently without flooding your own context.

---

## Step 2: Format the Output

Return results in a clean structured format with these sections:

### 1. 🆓 Free Legal Access Links
Table with: Source | URL | Access Type

**Common free/legal sources to check:**
- `archive.org` — Controlled Digital Lending (borrow 14 days, PDF/EPUB)
- `openlibrary.org` — links to Archive.org borrow
- `standardebooks.org` — public domain classics only
- `gutenberg.org` — pre-1928 public domain only
- Scribd — summary PDFs (not full books)
- Shortform / Blinkist — licensed summary services

> ⚠️ Always clarify if it's a borrow (14-day) vs permanent download. Modern books (post-2000) are almost never freely downloadable permanently — be honest about this.

### 2. 📋 Key Book Facts
Table: Title, Authors, Original Language, Publisher, Year, Pages, Sales, Languages, Awards, ISBN

### 3. 📖 Chapter Structure
Table: Chapter | Title | Key Topics Covered

### 4. 🌐 Free Resources & Official Pages
Table: Resource | URL

### 5. 👤 Author Personal Backstory
Narrative — how they met, what inspired the book, personal journey. This is often the most engaging part for Rajeev.

---

## Pitfalls
- **Copyright reality**: Most books published after ~2000 are NOT freely downloadable. Archive.org offers legal borrowing (14 days), not permanent download. Be upfront — don't imply a book can be permanently downloaded when it can't.
- **Fabrication risk**: Never invent URLs, ISBNs, sales figures, or chapter titles. All facts must come from pages actually fetched during the research run. If a stat is unverified, drop it or flag `[UNVERIFIED]`.
- **Subagent self-reports**: Verify key URLs returned by the subagent (especially claimed "free download" links) before presenting them to the user. A subagent may hallucinate a working URL.
- **Single web search is not enough**: One search gives surface results. The delegate pattern fetches 10–15 pages and synthesises them — always use it for book research tasks.

---

## Reference Files
- `references/ikigai-book-research.md` — Full research findings for *Ikigai: The Japanese Secret to a Long and Happy Life* (July 2026), usable as a template for output structure.
