# Roadmap

Committed doc, not scratch. Kept current by hand as work ships.
**Shipped** = live in production. **Next** = intended, not promised.
**Declined** = decided against, with the reason, so it doesn't get re-proposed.
**Open questions** = unresolved calls, with what would settle them.

## Next

## Shipped

- **Retired 2018 credentials deleted** (2026-10) — the never-expiring `credentials.json` key `d41e0f20…` was deleted 2026-10-13 after two weeks disabled with `py313` healthy (0 errors, a live sign-up 201 on 2026-10-03, no audit-log use of the key). The 68 `2018*` App Engine versions went 2026-09-30, so there is no rollback: a `py313` regression is fixed forward. The App Engine service account now holds only Google-managed keys.
- **Security fixes, python 3.13 runtime** (2026-09) — sign-ups append with `RAW` so an address can never be evaluated as a formula in the owners' sheet (`nobugs/nobugs.py#create_email`); CORS limited to nobugsphilly.com; 5 sign-ups per IP per hour on a single instance; 254-char cap; plain-text responses. Moved off EOL `python27` to `python313`, authenticating as the App Engine service account instead of a key file. Verified live: 400/409 paths, CORS preflight, Sheets read with the old key disabled. The sheet held 774 addresses, none formula-shaped.
