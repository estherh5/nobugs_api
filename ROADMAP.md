# Roadmap

Committed doc, not scratch. Kept current by hand as work ships.
**Shipped** = live in production. **Next** = intended, not promised.
**Declined** = decided against, with the reason, so it doesn't get re-proposed.
**Open questions** = unresolved calls, with what would settle them.

## Next

- [from 2026-10-13] **Delete the retired python27 versions and the disabled 2018 key.** Production moved to version `py313` on 2026-09-29; the ten `2018071*` versions stay as a rollback for two weeks, and service-account key `d41e0f20…` (bundled as `credentials.json` in the 2018 deploys, never expiring) was disabled, not deleted. If nothing broke, `gcloud app versions delete` the old versions and `gcloud iam service-accounts keys delete` the key.

## Shipped

- **Security fixes, python 3.13 runtime** (2026-09) — sign-ups append with `RAW` so an address can never be evaluated as a formula in the owners' sheet (`nobugs/nobugs.py#create_email`); CORS limited to nobugsphilly.com; 5 sign-ups per IP per hour on a single instance; 254-char cap; plain-text responses. Moved off EOL `python27` to `python313`, authenticating as the App Engine service account instead of a key file. Verified live: 400/409 paths, CORS preflight, Sheets read with the old key disabled. The sheet held 774 addresses, none formula-shaped.
