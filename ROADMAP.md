# Roadmap

Committed doc, not scratch. Kept current by hand as work ships.
**Shipped** = live in production. **Next** = intended, not promised.
**Declined** = decided against, with the reason, so it doesn't get re-proposed.
**Open questions** = unresolved calls, with what would settle them.

## Next

- [security] **Formula injection into a Google Sheet (Medium).** `nobugs/nobugs.py#create_email` appends with `valueInputOption='USER_ENTERED'` and the email regex allows `=+-` in the local part; also unlimited spam writes and CORS `*`. Only matters if the appspot service still answers (it returned 404 on 2026-09-28). Fix: use RAW or prefix `'`, rate limit, or decommission.

- [security] **EOL runtime (Low).** `app.yaml` is `runtime: python27` (last commit 2018, placeholders only). Fix: delete the GAE app if unused.
