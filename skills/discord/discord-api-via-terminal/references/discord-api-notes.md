# Discord REST API Reference Notes

## Base URL
`https://discord.com/api/v10`

## Common Endpoints

| Action | Method | Endpoint |
|--------|--------|----------|
| List guilds | GET | `/users/@me/guilds` |
| List channels | GET | `/guilds/{guild_id}/channels` |
| Create channel | POST | `/guilds/{guild_id}/channels` |
| Delete channel | DELETE | `/channels/{channel_id}` |
| Edit channel | PATCH | `/channels/{channel_id}` |
| List roles | GET | `/guilds/{guild_id}/roles` |
| Create role | POST | `/guilds/{guild_id}/roles` |
| Send message | POST | `/channels/{channel_id}/messages` |

## Required Bot Permissions
- `MANAGE_CHANNELS` (0x10) — create, delete, edit channels
- `MANAGE_ROLES` (0x10000000) — manage roles
- `SEND_MESSAGES` (0x800) — send messages

## How to Grant Permissions (Rajeev's workflow)
1. Go to Discord Developer Portal → Your App → Bot
2. Enable the permission under "Bot Permissions"
3. Re-invite the bot to the server using the OAuth2 URL with updated scopes
4. Or: Server Settings → Integrations → Bot → Edit permissions directly

## Session Notes (June 2026)
- Bot token confirmed working for guild listing and channel creation
- Team Rajeev category ID: `1509442091351146556`
- Rajeev's server guild ID: `1432708001868812401`
- Bot successfully created `#test-bot` channel via POST /guilds/.../channels (HTTP 201)
- Token was readable from `/app/data/config.yaml` under `discord.token`
