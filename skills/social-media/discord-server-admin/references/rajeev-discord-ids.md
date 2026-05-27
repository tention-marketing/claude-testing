# Rajeev's Discord Server — ID Reference Map

## Guild
- Name: Rajeev's server
- Guild ID: 1432708001868812401

## Bot
- Bot User ID: 1503655222361456651
- Bot Role: Hermes Agent (ID: 1503659544335745088, Position: 1 — needs to be moved to top by owner)

## Message Backup
- Full history: `/home/rajeev/.hermes/discord_backup/all_channel_messages.json` (permanent, survives restart)
- Sync log: `/home/rajeev/.hermes/discord_backup/sync.log`
- Cron job: `discord-channel-sync` (ID: f5973a47ca58, every 5 min)
- Script: `/home/rajeev/.hermes/scripts/discord_sync.py`

## Categories
| Name | ID | Notes |
|---|---|---|
| Text Channels | 1432708002489827408 | Default category |
| Voice Channels | 1432708002489827409 | Default category |
| churn-client-testing | 1470608471597777170 | Bot lacks access (403) |
| Clients | 1508829395790467104 | Created May 2026 |
| EMAIL STRATEGISTS | 1508843682399256788 | Active category (2nd replica, kept) |
| Virtual Office | 1508878844654911538 | Private voice channels |

Note: First EMAIL STRATEGISTS category (1508831628372217957) and all its channels were superseded by the second set.

## Text Channels — Current State (May 2026)
| Channel | ID | Category | Messages | Notes |
|---|---|---|---|---|
| #general | 1432708002489827410 | Text Channels | 34 | Bot has access |
| #hello | 1435280521134477322 | Text Channels | 185 | Bot has access |
| #aleart | 1436302755441410150 | Text Channels | 175 | free_response_channels — no @mention needed |
| #huu | 1470608523217080371 | churn-client-testing | 0 | Bot blocked (403) |
| #learning-headphones | 1470609241047044149 | Text Channels | 0 | Bot blocked (403) |
| #hiiii | 1470609283333885984 | churn-client-testing | 0 | Bot blocked (403) |
| #hell | 1508810133613051986 | churn-client-testing | 0 | Bot blocked (403) |
| #hermes-channel | 1508815045998542968 | churn-client-testing | 15 | Bot has access |
| #most | 1508829673587474444 | Clients | 3 | Created May 2026 |
| #churn-client-testing | 1508837921170391160 | churn-client-testing | 0 | |
| #churn-client-testing | 1508838756281745410 | Clients | 0 | |
| #mosity | 1508840274636439684 | Clients | 0 | Private |
| #new-client-alert | 1508850201325211859 | EMAIL STRATEGISTS | 0 | Active (kept) |
| #es-room | 1508850212674732092 | EMAIL STRATEGISTS | 2+ | Active — Klaviyo link pinned; voice message from rsr077 (forwarded, ogg, ~2m9s, May 26 2026) |
| #testing-channel | 1508850227719962716 | EMAIL STRATEGISTS | 0 | Active (kept) |
| #weekly-report | 1508850254429294714 | EMAIL STRATEGISTS | 0 | Active (kept) |
| #monthly-report | 1508850267876229222 | EMAIL STRATEGISTS | 0 | Active (kept) |
| #client-churn-alert | 1508850280853278962 | EMAIL STRATEGISTS | 0 | Active (kept) |
| #strategy-and-testing | 1509063798609154169 | EMAIL STRATEGISTS | 0 | Active |

## Deleted Channels (May 27 2026)
| Channel | ID | Reason |
|---|---|---|
| #strategy-and-testing | 1508850239900225556 | Deleted by user request (had 3 msgs — backed up) |
| #strategy-and-testing | 1508843749604855840 | Attempted delete — blocked (private, bot no access). User to delete manually. |
| #tention-digest (TEXT) | 1508843778398748723 | Duplicate of voice channel — deleted |

## Channels Still Needing Cleanup (user to delete manually — bot blocked)
- #strategy-and-testing (ID: 1508843749604855840) — private channel, bot can't access

## Pinned Messages
- #es-room (1508850212674732092): Klaviyo email editor link (msg ID: 1509051111082950787)
  URL: https://www.klaviyo.com/login?next=/email-editor/SY7Xr7/edit
  Note: requires rsr077's Klaviyo account credentials — link alone won't work for other users

## Voice Channels (Virtual Office: 1508878844654911538 — all private)
| Channel | ID |
|---|---|
| manager | 1508879009750978591 |
| acc-management | 1508879077694505010 |
| copy | 1508879107231056045 |
| design | 1508879185853153280 |
| tech | 1508879209102315550 |
| developers | 1508879256481169408 |
| deep-work | 1508879312642773092 |
| AFK | 1508879390363095102 |
| tention-digest (VOICE) | 1508851766517567488 | EMAIL STRATEGISTS | Active |

## Voice Channels (legacy)
- General: 1432708002489827411

## Roles
| Name | ID | Permissions | Notes |
|---|---|---|---|
| @everyone | 1432708001868812401 | 2248473465835073 | |
| Email Strategist | 1450009917196079184 | 0 | |
| Hermes Agent (bot) | 1503659544335745088 | 8866461766385655 | Must be top role for perm management |
| Members | 1508816446116069457 | 0 | Created May 2026 |
| Everyone | 1508829980824440914 | 0 | Mentionable, assigned to all 6 members May 2026 |
| clickup | 1508841084422455437 | 2248473465835073 | Blue, hoisted, mentionable |
| hermes-bot | 1508822307269902336 | 0 | |
| Test-bot | 1436255599292710987 | 68608 | |
| 7 Nov | 1436221381049192481 | 68608 | |
| testing-bot | 1432714553979834473 | 347136 | |

## Members (as of May 2026)
| Username | User ID | Roles |
|---|---|---|
| rsr077 | 1235236826793381908 | Email Strategist, Everyone |
| 7 Nove | 1427692009128464394 | 7 Nov, Everyone |
| rajeevkumar_8809 | 1427987539691835442 | Everyone |
| testing-bot | 1432710283142496337 | testing-bot, Everyone |
| Test-bot | 1436255228591738933 | Test-bot, Everyone |
| Hermes Agent | 1503655222361456651 | Hermes Agent, Everyone |

## Access Notes
- Bot CANNOT read/post to churn-client-testing channels (#huu, #hiiii, #hell) — server owner must grant
- Bot CAN read/post to: #general, #hello, #aleart, #hermes-channel, #most, all EMAIL STRATEGISTS channels
- Hermes Agent role position must be moved to TOP of role list by server owner to unlock permission management via API
- Private channels with @everyone VIEW_CHANNEL denied will block bot DELETE even with guild-level Manage Channels — user must delete these manually
