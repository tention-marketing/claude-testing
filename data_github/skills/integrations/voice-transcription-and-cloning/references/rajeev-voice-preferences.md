# Rajeev's Voice & Audio Preferences

## Voice Profile
- **Name on recording**: Rajeev (Whisper `tiny` transcribed as "Arif" — confirmed inaccurate)
- **Accent**: Indian English, non-native speaker actively practicing English
- **Context**: Handles US/UK/Australia clients; improving English for client communication
- **Clarity**: Speaks clearly but with natural hesitations; use `base` or `small` Whisper model — `tiny` is unreliable
- **Voice sample on file**: `/app/data/audio_cache/audio_d1e389378d17.ogg` (~2 min, good quality for cloning)

## Audio Summary Preferences (discovered July 2026)
- **Structure**: General book/topic content FIRST → personal application to Rajeev's life/business at the END
- **Tone**: Warm, conversational, "friend explaining to friend" — NOT lecture style, NOT formal
- **Length**: ~10 minutes is the target for full book/topic summaries
- **No dry reading**: Feels like a "jamming book" — relaxed, flowing, engaging
- **Personal tie-in**: Always connect back to Tention Marketing, his role as founder, his purpose

## Voice Cloning Status (July 2026)
- Rajeev wants future audio replies to sound like HIM speaking
- Sent a ~2-minute OGG voice sample (`audio_d1e389378d17.ogg`) as voice clone source
- **ElevenLabs**: NOT yet configured — user needs to sign up at elevenlabs.io and share API key
- **XTTS-v2 (Coqui TTS)**: Attempted locally — FAILS on Railway (OOM, ~4GB RAM required). Do not retry on Railway.
- **Fallback**: Eric Neural TTS voice (`en-US-EricNeural`) is acceptable in the interim

## Ikigai Audio — What Worked Well (July 4, 2026)
- Full ~10 min script delivered as single `text_to_speech` call — no issues with length
- Book summary + personal Rajeev story woven at the end was well received
- He chose "General book summary first, then personal at the end" option explicitly
- Content covered: Ikigai 4 circles, Flow, Okinawa lifestyle, wabi-sabi, ichigo ichie → then Tention Marketing tie-in
