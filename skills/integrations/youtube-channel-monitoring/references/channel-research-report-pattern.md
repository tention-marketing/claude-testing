# YouTube Channel Research Report — Multi-Sheet Excel Pattern

## When to Use
When Rajeev asks for a "full research" or "analysis" of a YouTube channel — not just a video list but performance insights, viral patterns, content ideas, and competitor context.

---

## 6-Sheet Structure (proven pattern, upgraded June 2026)

### Sheet 1: 📊 All Videos (ranked by views)
Columns: Rank, Title, Views, Formatted Views (e.g. "487K"), Published, Duration, Type (Long/Short), Performance Label, Why It Performed, URL

**Performance label + row color coding:**
| Tier | Views | Row Color | Label |
|------|-------|-----------|-------|
| MEGA VIRAL | 500K+ | RED `FF0000` | 🔥🔥🔥 MEGA VIRAL |
| VERY HIGH | 100K–500K | ORANGE `FF6B35` | 🔥🔥 VERY HIGH |
| HIGH | 50K–100K | YELLOW `F7C59F` | 🔥 HIGH |
| ABOVE AVERAGE | 20K–50K | LIGHT GREEN `EFEFD0` | ✅ ABOVE AVERAGE |
| AVERAGE | <20K | LIGHT GREY `E0E0E0` | 📊 AVERAGE |

**"Why It Performed" heuristics (auto-generate from title keywords):**
- `I Built/Made/Created` → "First-person 'I Built' = trust + personal proof"
- `Watch Me` → "'Watch Me' = live/real-time = authenticity magnet"
- `ULTIMATE/PERFECT/COMPLETE/ONLY` → "Superlative = implies definitive answer"
- `Mistake/Stop Using/Wrong` → "Mistake/warning angle = fear of missing out"
- `$X/Month / Make Money / Income` → "Money/income angle = high emotional trigger"
- `Replaced/Replacing` → "Replacement angle = controversial + emotional"
- `I Tested/Tested` → "'I Tested' = saves viewer research time"
- `Free` → "'Free' in title = always boosts clicks"
- `Secret` → "Exclusivity/insider knowledge framing"
- `LIVE` → "'LIVE' = raw/unscripted = high watch time"
- `Blueprint/System` → "Blueprint = framework = high perceived value"
- `Game Changer / Changed Everything` → "Game-changer framing = urgency"
- `No Code / No-Code / Without` → "Accessible to all = wider audience"
- Duration 45min+ → "Long-form = high watch time signal to YouTube"

### Sheet 2: 🏆 Performance Breakdown
- Summary table at top: tier name, # videos, total views, avg views, % of total
- Below: each tier listed separately with its videos, color-coded header block

### Sheet 3: 🔍 Viral Patterns
Title pattern analysis — for each pattern: description, examples from channel, avg views, psychology of why it works.

**7 core patterns for Nate's n8n/AI channel:**
1. `"I Built..."` — first-person proof (195K+ avg)
2. `"Watch Me Build... LIVE"` — authenticity (261K)
3. Superlatives: ULTIMATE/PERFECT/COMPLETE/ONLY (120K–488K)
4. `"TOP X Mistakes / Stop Using"` — fear hook (54K–219K)
5. `"Blueprint/System"` — framework promise (176K)
6. `"I Replaced..."` — controversy (91K–99K)
7. Tool tutorial: `"How to Use X in n8n"` — search traffic gold (54K–181K)

### Sheet 4: 💡 Content Ideas (15–20)
Columns: #, Video Title Idea, Predicted Views, Format/Length, Why It Will Work

**Title formulas for email marketing YouTube channel (Rajeev's niche):**
- `"5 [Tool] Mega-Prompts That Will 10x Your Email Marketing (Steal These)"` → 500K+ potential (copies Nate's #1 formula)
- `"I Replaced My Email Marketing Team with AI for 30 Days (Here's What Happened)"` → experiment format
- `"The AI Tool That Writes Better Emails Than I Do (I Tested 10 Tools)"` → 'I Tested' proven format
- `"Watch Me Build a Complete Email Marketing System with AI LIVE"` → live build
- `"The Email Marketing AI Agent Blueprint (Build ANY Campaign With This)"` → blueprint format
- `"This AI Wrote My Client's Email Sequence and It Made $50K (Full Breakdown)"` → money case study
- `"The ONLY Email Marketing AI Tutorial You Need in 2025 (Full Course)"` → authority claim
- `"How I Increased My Clients' Email Revenue by 300% Using AI (Step-by-Step)"` → % result

**Priority order:** money/result videos → experiment/story videos → tutorial/how-to videos → tool comparison videos

### Sheet 5: 🔍 Competitor Analysis
5–7 similar channels with: subscribers, total views, avg views/video, content focus, what to copy from each.

**Confirmed competitor channels (AI/automation niche):**
| Channel | Subs | Avg Views | Key Differentiation |
|---------|------|-----------|---------------------|
| Matt Wolfe (@mreflow) | 1.04M | ~170K | AI news roundups + tool reviews |
| The AI Advantage (@aiadvantage) | 535K | ~90K | ChatGPT workflows, productivity |
| AI Explained (@aiexplained) | 622K | ~194K | News/analysis deep dives |
| AI Jason (@AIJasonZ) | 310K | ~118K | Technical AI agent building |
| Income Stream Surfers | 298K | ~66K | n8n/Make.com automation |
| Liam Ottley (@liamottley) | 278K | ~76K | AI SaaS, sell AI services |

### Sheet 6: 📈 Channel Stats
- Core metrics (subs, videos, views, avg/video, upload frequency)
- Performance tier summary
- Content strategy overview
- Top 5 proven title formulas
- Growth strategy notes

---

## Color Scheme (consistent across all sheets)
- **Sheet headers/banners:** Dark navy `1A1A2E` with white text
- **Section dividers:** Red `E74C3C` with white text
- **Alternating rows:** `F9F9F9` / `FFFFFF`
- **Tier colors:** As per Sheet 1 table above

## Excel Setup Tips
```python
ws.freeze_panes = 'A2'  # or 'A3' if there's a banner row
ws.column_dimensions['A'].width = 5   # rank column
ws.column_dimensions['B'].width = 65  # title column
ws.row_dimensions[1].height = 35      # banner row
```

## Sending to Rajeev
After saving Excel file, send to DM:
```python
send_message(message="MEDIA:/path/to/file.xlsx", target="discord:rsr077")
```
`discord:rsr077` = Rajeev's DM (chat_id: 1503759738863751282).

---

## Nate Herk Channel Quick Reference (confirmed June 2026)
- **Channel:** @nateherk | ID: `UCfWg1ceoKD5JKo8GCMCBb3g`
- **Subscribers:** ~184K–186K
- **Total videos:** 127 (97 long + 30 Shorts)
- **Total views:** ~9.1M
- **Avg views/video:** ~66K
- **Top video:** "I Built a FULL AI Agent System in n8n (Watch Me Build)" — 487K views
- **Content niche:** n8n AI automation + agent building
- **Upload frequency:** 1–2/week
- **No content on:** Email marketing (gap Rajeev can exploit)
