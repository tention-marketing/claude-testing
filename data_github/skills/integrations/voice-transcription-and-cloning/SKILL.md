---
name: voice-transcription-and-cloning
description: Transcribe user voice messages (OGG/MP3/WAV) sent via Discord, generate audio replies in the user's cloned voice or a TTS voice, and manage the full voice-in/voice-out workflow. Covers local Whisper transcription, ElevenLabs voice cloning setup, and TTS delivery.
triggers:
  - User sends a voice/audio message and wants it transcribed
  - User says "listen to my voice", "record my voice", "clone my voice"
  - User wants AI replies delivered as audio in their own voice
  - User says "convert to audio" or "reply in my voice"
  - User sends an OGG file from Discord voice message
---

# Voice Transcription & Cloning

## Overview
When a user sends a Discord voice message, it arrives as an `.ogg` file saved at `/app/data/audio_cache/<filename>.ogg`. The workflow is:
1. **Transcribe** the OGG → text (local Whisper)
2. **Process** the content (understand intent, generate reply)
3. **Reply** as audio — either via TTS (Eric Neural) or cloned user voice (ElevenLabs)

---

## Step 1: Transcribe OGG Voice Message (Local Whisper)

Claude does NOT natively accept audio input. OpenAI Whisper API requires an API key (not always configured). **Use `faster-whisper` locally — works offline, no API key needed.**

### Install (once per environment)
```bash
apt-get install -y ffmpeg 2>&1 | tail -3
pip install faster-whisper -q
```
> Note: `ffmpeg` may not be available via apt on Railway — if `apt-get install ffmpeg` fails with "Unable to locate package", try `apt-get update` first. `faster-whisper` uses its own bundled `av` library and can decode OGG without system ffmpeg.

### Transcribe
```python
from faster_whisper import WhisperModel

model = WhisperModel("tiny", device="cpu", compute_type="int8")
segments, info = model.transcribe("/app/data/audio_cache/audio_XXXXX.ogg", beam_size=5)

print(f"Language: {info.language} ({info.language_probability:.0%})")
full_text = " ".join(seg.text for seg in segments)
print(full_text)
```

**Model size tradeoffs:**
| Model | Speed | Accuracy |
|-------|-------|----------|
| `tiny` | Fastest | Good for clear speech |
| `base` | Fast | Better for accented English |
| `small` | Medium | Good for non-native speakers |
| `medium` | Slow | Best accuracy |

> For Rajeev (Indian accent, English practice): `base` or `small` gives noticeably better accuracy than `tiny`.

### Pitfalls
- Whisper `tiny` struggles with Indian-accented English — words get misheard. Use `base` when transcription accuracy matters (e.g. client names, numbers).
- The HF_TOKEN warning is harmless — transcription still works without it.
- OGG files from Discord are Opus-encoded; `faster-whisper` handles them via the bundled `av` library.

---

## Step 2: Voice Cloning (ElevenLabs — Requires API Key)

**Current status**: ElevenLabs is NOT configured on this bot. User must provide an API key.

### Setup
1. User signs up at [elevenlabs.io](https://elevenlabs.io) (free tier: 10k chars/month)
2. User shares API key → save it:
   ```bash
   hermes config set ELEVENLABS_API_KEY <key>
   ```
3. Clone voice from a 30–60 second audio sample:
   ```python
   import requests

   API_KEY = "<elevenlabs_api_key>"
   headers = {"xi-api-key": API_KEY}

   # Upload voice sample
   with open("/app/data/audio_cache/audio_sample.ogg", "rb") as f:
       resp = requests.post(
           "https://api.elevenlabs.io/v1/voices/add",
           headers=headers,
           data={"name": "Rajeev", "description": "Rajeev's voice"},
           files={"files": ("voice.ogg", f, "audio/ogg")}
       )
   voice_id = resp.json()["voice_id"]
   print(f"Voice ID: {voice_id}")  # Save this!
   ```

4. Generate audio in cloned voice:
   ```python
   resp = requests.post(
       f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
       headers={**headers, "Content-Type": "application/json"},
       json={"text": "Your reply text here", "model_id": "eleven_multilingual_v2"}
   )
   with open("/app/data/audio_cache/reply.mp3", "wb") as f:
       f.write(resp.content)
   ```

### Fallback: TTS (No API Key Needed)
Until ElevenLabs is configured, use the built-in `text_to_speech` tool:
- Rajeev's configured voice: `en-US-EricNeural`
- This uses Edge TTS — no API key, works immediately

---

## Step 3: Deliver Audio Reply

After generating the MP3, deliver it back to Discord (see `discord-api-via-terminal` skill):
```bash
curl -s -X POST https://discord.com/api/v10/channels/CHANNEL_ID/messages \
  -H "Authorization: Bot TOKEN" \
  -F "files[0]=@/app/data/audio_cache/reply.mp3"
```
Or simply use the `text_to_speech` tool and include `MEDIA:/path/to/file.mp3` in your reply — Discord delivers it as an attachment.

---

## Full Workflow Summary

```
User sends OGG voice message
        ↓
[faster-whisper] → transcription text
        ↓
Understand intent / generate reply text
        ↓
[ElevenLabs] (if configured) OR [text_to_speech tool]
        ↓
MEDIA:/app/data/audio_cache/reply.mp3 in response
```

---

## Audio Summary Generation (Long-form TTS)

For generating ~10-minute educational audio summaries (e.g. book summaries, explainers):
- Write the full script as a single `text_to_speech` call — the tool handles long text
- Structure: general content first → personal/contextual application at the end (Rajeev's preference)
- Warm, conversational tone — "friend explaining to friend", NOT lecture style
- Keep it flowing naturally — no bullet points, no headers in the spoken script

---

## User-Specific Notes
See `references/rajeev-voice-preferences.md` for Rajeev's audio style preferences, voice profile, and the Ikigai summary workflow that worked well.

## Local Voice Cloning — XTTS-v2 (Coqui TTS)

Coqui TTS XTTS-v2 is the best free/local voice cloning model. **However it is NOT viable on Railway** — the model requires ~4GB RAM to load and Railway containers OOM-kill it. Do not attempt on Railway.

### If you do want to try locally (non-Railway environments):
```bash
pip install TTS
```
```python
import os
os.environ["COQUI_TOS_AGREED"] = "1"  # Required — bypasses interactive license prompt
from TTS.api import TTS

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
tts.tts_to_file(
    text="Your text here",
    speaker_wav="/path/to/voice_sample.ogg",
    language="en",
    file_path="/output/cloned.wav"
)
```

**Pitfalls for XTTS-v2:**
- Without `COQUI_TOS_AGREED=1`, it hangs on an interactive `input()` prompt and crashes with `EOFError`
- Needs `transformers==4.40.0` — newer versions (5.x) break XTTS import with `ImportError: cannot import name 'BeamSearchScorer'`
- Model download is 1.87GB — subsequent runs reuse cache at `~/.local/share/tts/`
- **Railway: OOM-killed at load time** — do not attempt. Recommend ElevenLabs API instead.

---

## Pitfalls
- **Claude cannot accept audio as input** — do not try passing OGG/MP3 to Anthropic API (it only accepts PDF for documents, images for vision). Always transcribe locally first.
- **OpenAI Whisper API** requires `OPENAI_API_KEY` — check `hermes config show` before assuming it's available. If not set, use local `faster-whisper`.
- **Anthropic API key access from Python**: Do NOT instantiate `anthropic.Anthropic()` without explicitly passing `api_key`. The key lives in Railway env as `ANTHROPIC_API_KEY` — read it from `/proc/1/environ` if `os.environ` doesn't expose it in child processes.
- **ElevenLabs is the only practical voice cloning option on Railway** — XTTS-v2 (Coqui) OOMs, OpenVoice has same issue. Be upfront: cloning on Railway requires ElevenLabs API key. Free tier (10k chars/month) is enough for demos.
- **OGG from Discord = Opus codec** — most tools handle it fine, but if a tool insists on WAV/MP3, convert first: `ffmpeg -i input.ogg output.wav` (requires ffmpeg to be installed).
- **Whisper `tiny` is unreliable for Indian-accented English** — confirmed: transcribed "Rajeev" as "Arif", misheard multiple words. Always use `base` or `small` for Rajeev's voice messages.
