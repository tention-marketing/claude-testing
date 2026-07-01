# Spotify Redirect URI Rules (enforced April 2025+)

Source: Spotify Developer Blog / Dashboard warning text

## Rules
- HTTPS required for all redirect URIs **except** loopback addresses
- `localhost` is **NOT allowed** as a redirect URI (banned since April 2025)
- Loopback IP literals (`127.0.0.1` or `[::1]`) are allowed with HTTP
- Port number in loopback URIs can be dynamic (register without port, add port at auth request time)

## Valid Examples
```
https://example.com/callback          ✅ HTTPS non-loopback
http://127.0.0.1:8000/callback        ✅ IPv4 loopback
http://[::1]:8000/callback            ✅ IPv6 loopback
http://127.0.0.1/callback             ✅ loopback without port (dynamic port allowed)
```

## Invalid Examples
```
http://localhost:8888/callback        ❌ localhost banned
http://example.com/callback           ❌ HTTP on non-loopback
```

## Migration Deadline
- April 9, 2025: enforcement began for new apps
- November 2025: all existing apps must comply
