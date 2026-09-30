# Roadmap

Committed doc, not scratch. Kept current by hand as work ships.
**Shipped** = live in production. **Next** = intended, not promised.
**Declined** = decided against, with the reason, so it doesn't get re-proposed.
**Open questions** = unresolved calls, with what would settle them.

## Next

- [from 2026-10-13] **Delete the disabled 2018 service-account key.** Key `d41e0f20…` (bundled as `credentials.json` in the 2018 deploys, never expiring) was disabled, not deleted, when production moved to `py313` on 2026-09-29. If nothing has broken by then, `gcloud iam service-accounts keys delete` it. The retired versions are already gone: all 68 `2018*` versions (not ten; 62 were still SERVING at 0% traffic, returning 500 on pre-fix code) were deleted 2026-09-30 at Esther's go-ahead, leaving `py313` alone at 100%. That removed the planned rollback, so a `py313` regression is fixed forward.

## Shipped

- **Security fixes, python 3.13 runtime** (2026-09) — sign-ups append with `RAW` so an address can never be evaluated as a formula in the owners' sheet (`nobugs/nobugs.py#create_email`); CORS limited to nobugsphilly.com; 5 sign-ups per IP per hour on a single instance; 254-char cap; plain-text responses. Moved off EOL `python27` to `python313`, authenticating as the App Engine service account instead of a key file. Verified live: 400/409 paths, CORS preflight, Sheets read with the old key disabled. The sheet held 774 addresses, none formula-shaped.
