# Voice Message Delivery — Rajeev's Dictation Workflow

## Core Workflow
1. User dictates the message content verbally
2. Call `text_to_speech` with EXACTLY what the user said — nothing more, nothing less
3. Send the resulting MP3 to the target Discord channel via curl multipart upload
4. Confirm with a brief one-line acknowledgement

## Critical User Preference — Rajeev
**Send ONLY what Rajeev dictated. Do NOT add:**
- Greetings or sign-offs around the dictated text
- Explanatory framing ("Here's your voice message...")
- Extra sentences beyond the literal dictation

❌ WRONG: `"Hello, what's going on? Send invoice."` — user only said *"Hello, what's going on?"*
✅ CORRECT: `"Hello, what's going on?"` — send exactly that, nothing else

The phrase "send invoice" / "send voice message" / "send it" is the **command trigger**, not content to include in the audio.

## TTS → Discord Send Pattern

```bash
# Step 1: Generate audio (tool call)
text_to_speech(text="<exactly what user said>", output_path="/tmp/voice_message.mp3")

# Step 2: Send to Discord channel
curl -s -X POST https://discord.com/api/v10/channels/CHANNEL_ID/messages \
  -H "Authorization: Bot TOKEN" \
  -F "files[0]=@/tmp/voice_message.mp3"
```

- No `Content-Type: application/json` header when sending files
- Use the channel ID, not channel name
- Load TOKEN from `/app/data/config.yaml` (see main skill)

## Voice Selection
Rajeev's preferred voice: `en-US-EricNeural` (Male, US English) — chosen June 2026.

To list available English voices:
```python
import asyncio, edge_tts
async def main():
    voices = await edge_tts.list_voices()
    en_voices = [v for v in voices if v['Locale'].startswith('en-')]
    for v in en_voices:
        print(v['ShortName'], '-', v['Gender'])
asyncio.run(main())
```

## Channel Name → ID Resolution
Check cached channel list first. Known channel IDs for common targets:
- **#developers** (Virtual Office, voice): `1508879256481169408`
- **#little** (Team Rajeev): `1514538903502323873`
- **#hermes-channel** (primary bot/Rajeev comms): `1508815045998542968`

For unlisted channels, use the list endpoint (see main skill).

## Limitations
- Audio is sent as an **MP3 attachment**, not a native Discord voice bubble (waveform UI)
- Voice channels can receive file attachments — sending to them works even though they're voice-type channels
- TTS provider is `edge` by default (fast, no cost); quality is robotic but clear

## Pitfalls
- **Don't include the trigger phrase in the audio** — "send voice message", "send invoice", "send it to [channel]" are commands, not content.
- **Don't add wrapper sentences** — user corrected this explicitly. Just generate and send.
- **Don't explain TTS limitations unprompted** — only mention them if the user asks why it doesn't look like a voice bubble.
