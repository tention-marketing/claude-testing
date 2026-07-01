# New Client Alert Workflow (Rajeev's Server)

## Trigger
A new client alert message appears in **#new-client-alert** channel.

## ES → Category Mapping
| ES Name | Discord Category |
|---------|-----------------|
| @Rajeev | team-rajeev (ID: 1509442091351146556) |
| @Taiwo  | (find dynamically — check channel list) |

## Steps
1. Read the onboarding Google Doc link from the alert message
2. Identify **ES Assigned** → map to the correct Discord category
3. Check if channel with the brand name already exists (avoid duplicates!)
4. Create text channel using brand name (lowercase, hyphens) inside the mapped category
5. Send the formatted NEW CLIENT ALERT message inside the newly created channel

## Duplicate Check Pattern
```python
existing = [ch for ch in channels if ch.get('name') == brand_name_slug]
if existing:
    channel_id = existing[0]['id']
else:
    # create new
```

## Message Format
```
🚨 NEW CLIENT ALERT 🚨

**Name:** [Brand Name]
**Website:** [Store URL]
**Intake Form:** [Google Doc URL]
**ES Assigned:** @[ES Name]
**Contact Person:** [Client Name]
**Service Package:** [Package]
**Call Recording:** [URL or N/A]
**Timezone:** [TZ]
**Lead ES:** @[Lead ES]
**Channel:** [Slack/Email/etc]
**Signup Platform:** [Platform or Not determined]
```

## Example — Little Chicken (June 2026)
- Client: Megan O'Donnell | megan@littlechickenkids.com
- Brand: Little Chicken → channel name: `little-chicken`
- Store: https://littlechickenkids.com/
- Onboarding Doc: https://docs.google.com/document/d/1mMm_97nC3zr6TdqkeNYnmSiVZ9kAI-GJ53kT0IdKe6M
- ES: @Rajeev → team-rajeev category
- Lead ES: @Taiwo
- Package: Full recurring service
- Call Recording: https://fathom.video/share/pSHhR58s3GB5rr_AiSF31yJ4z3vhxFxM
- Timezone: EST
- Channel: Slack
