---
name: email-campaign-calendar
description: Build a monthly email marketing campaign calendar for an eCommerce client using the campaigns/ skill library, then deliver it to a formatted Google Sheet. Covers calendar generation rules, segment/exclusion logic, A/B test structure, and the Drive + Sheets delivery workflow.
version: 1.0.0
author: Nous Research
platforms: [linux, macos, windows]
tags: [email-marketing, klaviyo, shopify, campaign-calendar, google-sheets, ecommerce]
---

# Email Campaign Calendar — Build & Deliver

Use this skill when asked to generate a monthly email campaign calendar for a client and write it to Google Sheets. The campaigns/ folder in the user's project contains the authoritative rule set — always read those files first.

## References

- `references/steenbrand-dec-2026.md` — Worked example: Steenbrand, December 2026 (apparel brand, men 55+).
- `references/purely-nutrient-july-2026.md` — Worked example: Purely Nutrient, July 2026 (supplement brand, older wellness audience, single SKU). Documents creative mechanic selection, Recharge subscription segment logic, promo sequence, and a targeted cell-update pass.

---

## Step 0: Read the Skill Library First

Before generating anything, read ALL of these files in order:

```
campaigns/CLAUDE.md
campaigns/strategy-planning/SKILL.md
campaigns/email-ideas/SKILL.md
campaigns/audience-data/SKILL.md
campaigns/testing-optimization/SKILL.md
campaigns/content-calendar/SKILL.md
```

The rules inside those files govern everything: content/promo ratio, email type mix, segment/exclusion logic, A/B test structure, column format, send times. Do not skip or skim.

---

## Step 1: Absorb Client Data

From the onboarding input, extract and hold in mind:

- Brand name, founder name, website, location, timezone
- Audience: age range, persona, key desires and fears
- Tone of voice
- Products (especially best sellers)
- USPs (unique selling propositions)
- Objections and FAQs (pre- and post-purchase)
- First-time offer and VIP tier structure
- Discount range (use SKILL.md recommended range if not specified)
- Colors and fonts (for design reference, not needed for calendar)
- Shipping info
- Priority: brand storytelling vs. sales vs. balanced

---

## Step 2: Generate 12 Campaigns Applying All Rules

### Content/Promo Ratio (from strategy-planning/SKILL.md)
- Minimum 3 value emails per 1 promotional email
- Max 2–3 promotional emails per segment per month
- One big sale = 3–5 email sequence (Announce → Reminder → Last Chance → [Thank You])

### Required Email Types (must include all of these per month)
- 1 big sale sequence (4 emails: Launch → Reminder → Last Chance → Thank You)
- 1 founder personal email (plain-text, warm, long-form storytelling — CTA is always reply, never a buy button as lead)
- 1 objection handling email (single objection per email, grounded in research — not generic)
- 1 subscription-focused email (retention, value of subscribing, or subscription-exclusive offer — exclude active subscribers)
- 1 reply-based email (CTA = reply — boosts deliverability)
- 1 data collection email (click-to-tag with Klaviyo update_property_link or survey)
- Minimum 2 creative mechanic emails — mandatory, not optional (see mechanic selection guide below)
- Value/education emails filling the remainder

### Offers to Spread Through the Month
- Big sale discount (15–20% typical for December)
- VIP-only exclusive (higher % or early access)
- Smaller test offers inside value emails (e.g. 48-hr welcome code, mystery discount)

### Creative Mechanics (from email-ideas/SKILL.md)
- MANDATORY: minimum 2 creative mechanic emails per calendar — never skip
- Max 1 mechanic per email, never stack two mechanics
- Match mechanic to audience age and brand voice — NEVER use bold/edgy mechanics (One-Shot Game, aggressive countdown) for older wellness audiences
- For supplement/health brands with older audiences: Toggle Email, Faux AI Chat UI, Flowchart/Product Finder, Wrapped/Recap are safe choices
- Faux AI Chat UI works exceptionally well for research-oriented wellness audiences — "borrowed authority" framing (AI recommends the product) feels like discovery, not advertising
- Toggle Email works for product feature education — list 3–5 benefits as ON/OFF switches in iOS/Android style
- See `references/purely-nutrient-july-2026.md` for a worked example of mechanic selection for an older wellness brand

### Send Date Spacing
- Space sends 2–4 days apart minimum (except promo sequence: can be 2 days)
- Avoid sending on the same day of the week every time — vary across the month
- Test send times: 6–8 AM, 11 AM–2 PM, 5–8 PM in client's timezone

---

## Step 3: Column Format (from content-calendar/SKILL.md)

Every row = one email. Use exactly these 9 columns:

| Column | What to Fill |
|---|---|
| Date | Specific date (e.g. Dec 10) |
| Day | Day of week |
| Email Topic | Clear title of the email |
| Strategy | Email type + objective + angle description (2–3 sentences) |
| Discount / Offer | Exact offer, code, duration — or "None" for value emails |
| A/B Testing | "SL A: [subject line A] vs SL B: [subject line B]" |
| Sent to Segment | Which Klaviyo segment receives this |
| Exclude List | Which segments are excluded |
| Send Time | Time + timezone (e.g. 8 AM PST) |

### Segment Naming Conventions
- Engaged last 30D / 60D / 90D / 180D / 365D
- VIP Bronze / VIP Silver / VIP Gold
- New subscribers (joined last 30D)
- Browsed products, no purchase last 30D
- Placed order last 30D
- Active site visitors last 30D
- Opened [Campaign X] but did not click

### Exclusion Rules (ALWAYS apply — from audience-data/SKILL.md)
Every send must exclude at minimum:
- Bounced
- Marked as Spam
- Unsubscribed

Promotional sends also exclude:
- Buyers last 10D (avoids buyer's remorse)

VIP sends also exclude:
- Non-VIP
- Recent buyers (last 5–10D depending on offer)

---

## Step 4: Deliver to Google Sheet

### Prerequisites
- Google auth must be working: `python3 ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --check` returns `AUTHENTICATED`
- Target Drive folder ID provided by user

### Workflow

```
1. Create subfolder for client:
   $GAPI drive create-folder "ClientName" --parent PARENT_FOLDER_ID
   → Capture the returned folder ID

2. Create the spreadsheet:
   $GAPI sheets create --title "ClientName — Month YYYY Campaign Calendar"
   → Capture the spreadsheetId

3. Move sheet into the client subfolder (Drive API — must use Python directly,
   not the GAPI wrapper, because gapi has no move command):
   → Get current parents, then call files().update() with addParents + removeParents
   → See scripts/move_sheet.py template

4. Write all rows (header + 12 campaigns) in one call:
   → Build rows as a Python list of lists
   → Use service.spreadsheets().values().update() with valueInputOption='RAW'
   → Range: 'Sheet1!A1:I{total_rows}'

5. Apply formatting in one batchUpdate:
   → Bold header row (black bg, white text)
   → Freeze row 1
   → Set column widths (Strategy/Offer/A/B cols: 320px; Segment/Exclude: 240px)
   → Wrap text + vertical align TOP for all cells
   → Alternate row banding (white / light grey #F0F0F0)
```

### Key API Pitfall — Cell Formatting
When using `repeatCell` in batchUpdate, text colour goes inside `textFormat`, not at the format level:

```python
# CORRECT
"textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}

# WRONG — causes HttpError 400
"foregroundColorStyle": {"rgbColor": {"red": 1, "green": 1, "blue": 1}}
```

The `fields` string must match exactly what you set:
```python
"fields": "userEnteredFormat(textFormat,backgroundColor)"
```

### Write Rows as Python Script (not via GAPI CLI)
For multi-row writes with complex string content (long strategy text, quotes, em dashes), write a Python file to `/tmp/` and run it — do not try to shell-escape a large JSON payload inline. The GAPI CLI wrapper can struggle with special characters in large payloads.

---

## Step 5: Updating an Existing Calendar (Targeted Cell Edits)

When the user asks to update specific rows/cells in a calendar that already exists in a Sheet, use `batchGet` + `batchUpdate` — not a full rewrite.

### Workflow

```
1. Read current cell values first (batchGet) for every cell you'll touch:
   → sheets.spreadsheets().values().batchGet(spreadsheetId=ID, ranges=[...])
   → For Strategy cells, always read the full value — it will be truncated in the preview

2. Build updated values:
   → For in-place text changes (e.g. update one sentence in a Strategy field):
      read the full current value, make the surgical edit in Python string, write back
   → For field replacements (Offer, Segment, Topic): write the new value directly

3. Write all changes in a single batchUpdate:
   → sheets.spreadsheets().values().batchUpdate(
         spreadsheetId=ID,
         body={"valueInputOption": "RAW", "data": [{"range": "Sheet!X1", "values": [[new_val]]}, ...]}
     )

4. Verify by reading back the changed cells (batchGet again):
   → Print each updated cell's value as confirmation
```

### Sheet naming convention used for Purely Nutrient calendars
- Spreadsheet title: `ClientName — month = Month YYYY, campaigns = N`
- Tab name: `Month YYYY`
- Example: `Purely Nutrient — month = July 2026, campaigns = 12` with tab `July 2026`

### Column index reference (1-indexed in Sheets notation)
| Col | Letter | Field |
|-----|--------|-------|
| 1 | A | Date |
| 2 | B | Day |
| 3 | C | Email Topic |
| 4 | D | Strategy |
| 5 | E | Discount / Offer |
| 6 | F | A/B Testing |
| 7 | G | Sent to Segment |
| 8 | H | Exclude List |
| 9 | I | Send Time |

---

## Step 6: Verification

After writing, read back columns A–C to verify all 12 rows landed correctly:

```python
result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID,
    range='Sheet1!A1:C13'
).execute()
for row in result.get('values', []):
    print(' | '.join(row))
```

---

## Quality Checklist Before Marking Done

### Mandatory email types
- [ ] 1 founder personal email (reply CTA, never a buy button as lead)
- [ ] 1 objection handling email (single objection, research-grounded)
- [ ] 1 subscription-focused email (retain/subscribe value — exclude active subscribers from segment)
- [ ] 1 reply-based email (CTA = reply, boosts deliverability)
- [ ] 1 data collection email (click-to-tag or survey)
- [ ] Minimum 2 creative mechanic emails (matched to audience — older audiences: Toggle, Faux AI Chat, Flowchart, Wrapped)

### Structure
- [ ] Content/promo ratio is at least 3:1 (value:promo)
- [ ] Big monthly sale = 4 emails: Launch → Reminder → Last Chance → Thank You (Thank You mandatory)
- [ ] Thank You email uses a non-% offer (free shipping, small bonus) — never repeat the % discount
- [ ] Reminder email targets non-openers AND non-clickers from launch — not just one group
- [ ] At least 1 seasonal hook if the month has a key calendar moment

### Segmentation + exclusions
- [ ] Every send excludes: Bounced, Marked as Spam, Unsubscribed
- [ ] All promotional sends exclude Buyers last 10D (never 5 or 7 — it's 10)
- [ ] No lower % discount sent within 10 days of a higher % offer to the same person
- [ ] No VIP tier language if VIP tiers are not active for this client

### A/B + timing
- [ ] Every campaign has A/B test (Subject Line A vs B format)
- [ ] Send times vary — not all the same window across the month
- [ ] Minimum 3 days between sends (promo sequence exception: 2 days allowed within sequence)

### Delivery
- [ ] Spreadsheet title follows naming convention: `ClientName — month = Month YYYY, campaigns = N`
- [ ] Sheet tab named: `Month YYYY`
- [ ] Sheet is in the correct client subfolder inside Drive
- [ ] Header row: bold, dark background, white text, frozen
- [ ] Row count verified by read-back (columns A–C minimum)
