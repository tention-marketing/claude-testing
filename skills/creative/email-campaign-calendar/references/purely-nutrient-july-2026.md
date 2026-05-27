# Purely Nutrient — July 2026 Calendar
## Worked Example: Supplement Brand, Older Wellness Audience

Google Sheet: https://docs.google.com/spreadsheets/d/10hcRgL7gLSQKTCFN-R9ySg7InxsEbsbCORsU2aVYVw0/edit
Drive subfolder: 1QLiQNUkTHdjyuXGfveU_PLDAtdf0vHCD (inside parent 1A4q6oWFdROXQ1xbEOOUGLFUEpaS6h0zJ)

---

## Client Profile (condensed)

- Brand: Purely Nutrient
- Founder: Tyler
- Product: Single SKU — Ethiopian Black Seed Oil
- USPs: Up to 9x more potent than regular BSO; up to 4.64% thymoquinone (always say "up to 4.64%"); penetrates biofilm; Ethiopian highland sourcing; single ingredient no fillers
- Audience: Modestly older adults — 3 avatars:
  - Avatar 1: General wellness (gut, bloating, brain fog, inflammation)
  - Avatar 2: Parasite/detox researchers (biofilm, gut cleansing)
  - Avatar 3: Men's health and performance
- Tone: Honest, knowledgeable, warm — NOT hype, NOT clinical
- Discount range: 10–15% approved without checking. Above 15%: flag with "CHECK WITH CLIENT BEFORE SENDING"
- VIP tiers: NOT active — never include VIP tier language
- Subscription: Brand is subscription-heavy — always include at least 1 subscription email per calendar

---

## The 12 Emails (final state after updates)

| # | Date | Day | Email Topic | Type | Key Notes |
|---|------|-----|-------------|------|-----------|
| 1 | July 1 | Wed | A Note From Tyler: Why I Spent 2 Years Finding This One Ingredient | Founder Personal | Reply CTA primary. 10% off (code TYLER10) in PS only. Send: 11 AM EST |
| 2 | July 4 | Sat | Freedom From Bloating, Brain Fog & Low Energy — Happy 4th | Seasonal / Value | Independence Day hook. Biofilm angle. No offer. |
| 3 | July 7 | Tue | Everything You Need — All Switched ON | Creative Mechanic: Toggle Email | iOS toggle switches (Biofilm: ON, Thymoquinone: ACTIVE, etc). No offer. |
| 4 | July 10 | Fri | Does It Actually Work? Here's the Honest Answer | Objection Handling | Thymoquinone concentration science, plain English. No offer. |
| 5 | July 14 | Tue | Quick question — what health goal brought you here? | Data Collection + Reply-Based | Klaviyo update_property_link for 3 avatar tags. Also invites reply. |
| 6 | July 17 | Fri | 15% Off — Our Biggest July Offer (3 Days Only) | Promo Launch (1/4) | Code: JULY15. Expires July 20 midnight EST. Auto-apply link. Exclude buyers 10D. |
| 7 | July 19 | Sun | Reminder: 15% Off Closes Tomorrow Night | Promo Reminder (2/4) | Non-openers AND non-clickers from July 17 only. Code: JULY15, closes July 20. |
| 8 | July 20 | Mon | Last Chance: 15% Off Ends at Midnight | Promo Last Chance (3/4) | Evening send (6 PM). Maximum urgency. Single link only. |
| 9 | July 22 | Wed | Thank You — A Small Gift From Us | Promo Thank You (4/4) | Free shipping (code SHIPFREE, 7 days). No % discount. Segment: opened/clicked any of July 17/19/20. |
| 10 | July 24 | Fri | Why Consistency Is the Real Secret (And How to Make It Automatic) | Subscription | Recharge segment logic (see below). Exclude active subscribers. |
| 11 | July 27 | Mon | We Asked AI About the Best Gut Health Supplement. Here's What It Said. | Creative Mechanic: Faux AI Chat UI | ChatGPT screenshot recommending Purely Nutrient. No offer. |
| 12 | July 30 | Thu | The Protective Shield Pathogens Hide Behind (And How Thymoquinone Breaks It) | Value / Education | All 3 avatars. CTA button: "Start Your Protocol" → product page. No discount. |

---

## Key Segment Definitions Used

**July 17/18/20 Promo sequence — sent to:**
- Engaged 90D
- Exclude: Bounced, Marked as Spam, Unsubscribed, Placed Order last 10D

**July 19 Reminder — critical segment note:**
- Target: Non-openers AND non-clickers from July 17 email (both conditions, not OR)
- Exclude from reminder: anyone who opened OR clicked July 17 (they already engaged)

**July 22 Thank You — segment:**
- Opened OR clicked at least one of: July 17 email OR July 19 email OR July 20 email
- (Not "all who received" — that would include unengaged; this rewards engagers)

**July 24 Subscription — segment:**
- Primary: Placed Order at least 1 time AND Recharge subscription status is not Active
- Fallback (if Recharge not live): Placed Order at least 1 time AND has not placed order in last 45 days
- Always exclude active subscribers

---

## Creative Mechanic Selection Rationale

This client targets modestly older adults. Mechanic choices were constrained accordingly:

| Rejected | Reason |
|----------|--------|
| One-Shot Game | Bold/edgy — Saw movie aesthetic. Wrong for this audience. |
| Mystery Discount | Too gamified for trust-first wellness positioning |
| This or That Showdown | Single SKU brand — nothing to compare |

| Selected | Reason |
|----------|--------|
| Toggle Email | Familiar iOS/Android UI. Fast to scan. Non-threatening. Perfect for feature education. |
| Faux AI Chat UI | Research-oriented older audience trusts evidence. Borrowed authority (AI recommends). Feels like discovery. |

---

## Discount Rules for This Client

- 10%: approved, usable freely (first-time offers, PS codes)
- 15%: approved, usable for main monthly promo
- Above 15%: FLAG — "CHECK WITH CLIENT BEFORE SENDING"
- Never use % discount in Thank You email — use free shipping or bonus instead (avoids conditioning)

---

## Updates Applied After Initial Build

The calendar was updated in a second pass with targeted batchUpdate (not a full rewrite):

1. July 1 — Send Time: 8 AM → 11 AM EST
2. July 17 — Offer expiry corrected: July 19 → July 20. Strategy CTA updated to match.
3. July 19 — Topic updated ("Tomorrow" → "Tomorrow Night"). Offer and strategy urgency updated to July 20.
4. July 22 — Segment tightened: "All who received" → "Opened OR clicked at least one of July 17/19/20"
5. July 24 — Segment replaced with Recharge-conditional definition
6. July 30 — Strategy appended: CTA button "Start Your Protocol" → product page, no discount
