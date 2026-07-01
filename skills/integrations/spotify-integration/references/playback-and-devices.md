# Spotify Playback Reference — Rajeev's Setup

## Known Devices

| Device | ID | Type | Notes |
|---|---|---|---|
| Galaxy A35 5G | `dca9712f11444ac997f258f36b9ce9f910ca5d31` | Smartphone | Most commonly active |
| MacBook Pro | `6bb75732f2edc46f7cc193d7add1811d7efa0186` | Computer | Active when Spotify open on Mac |

> Device IDs can change if Spotify is reinstalled. Re-verify with `/v1/me/player/devices` if playback returns 404.

## Known Artist URIs

| Artist | URI | Notes |
|---|---|---|
| Arijit Singh | `spotify:artist:4YRxDV8wJFPHPTeXepOstw` | Rajeev's favourite |

## Known Album URIs

| Album | URI | Notes |
|---|---|---|
| Alarm Clock Sound | `spotify:album:2BSXZv0v8qluXEXuk2QwYp` | Confirmed working June 2026 for wake-up alarm |

## Rajeev's Music Preferences
- Hindi / Bollywood (Arijit Singh, Mika Singh, Himesh Reshammiya)
- Uses Spotify as wake-up alarm via cron job
- When searching Indian artists, always use `market=IN` for best results
- Volume control (403 on Free accounts): Setting volume via `/me/player/volume` returns 403 on Spotify Free — this is expected. Skip volume commands or note gracefully.

## Wake-Up Alarm Cron Job

**Cron:** `30 2 * * *` (= 8:00 AM IST / 2:30 AM UTC), runs daily forever  
**Job name:** "Spotify Wake-Up Alarm 8am IST"  
**Job ID:** `3c6c659f4659` (created June 2026 — verify with `cronjob action=list`)

**What it does:**
1. Refreshes Spotify access token (token expires every 3600s)
2. Sets volume to 85% on Galaxy A35 5G
3. Plays Arijit Singh artist context on Galaxy A35 5G
4. Sends confirmation message back to Discord chat

**Limitation:** Requires Spotify app to be open/active on the phone at alarm time. If the device is not found (404), it sends a warning message to Discord instead. Rajeev should keep Spotify installed and not force-quit it.

## Alarm / Scheduled Playback Pattern

For any "play X at Y time" request from Rajeev:
1. Ask timezone if not IST (Rajeev is in India IST = UTC+5:30)
2. Convert to UTC for cron schedule: `HH:MM IST` → `(HH - 5):MM - 30 UTC` (adjust for midnight crossing)
3. Create cron job with `schedule="MM HH * * *"` in UTC
4. Token refresh MUST be the first step — tokens expire after 1 hour
5. Check devices API and use active device — don't hardcode MacBook if phone is more likely active
6. Set volume to 85% before play (loud enough to wake up)
7. Deliver confirmation back to origin chat

## Spotify Cannot Do
- Set phone alarms (Clock/alarm app)
- Trigger notification sounds
- Ring the phone
- Play without Spotify app being open/active on device
