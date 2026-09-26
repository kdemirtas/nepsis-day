# HANDOVER: nepsis.day
Type: webpage
Resume point. Full detail in `STATUS.md` (top blockquote); shape of the code in `ARCHITECTURE.md`.

## CURRENT: live at nepsis.day in English, one zone setting to switch off (2026-09-26)
`/`, `/privacy` and `404` are served by Cloudflare Pages from `main`; every merge to `main` now publishes. Everything served matches the repo except `/privacy`, where the zone's Email Address Obfuscation hides the contact address and injects a script. BACKLOG 7 (next ring of CSS gaps) is due for Kerem to promote or re-park. Decisions so far: D-2026-09-12-1 to -20, D-2026-09-26-1 and -2.
**RESUME:** Kerem turns off Email Address Obfuscation for `nepsis.day` (Security, Settings, or Scrape Shield); then diff every live page against the repo (`curl -s https://nepsis.day/privacy | cmp - privacy.html`, same for `/`, `style.css`, the 404) and close item 1. Then `/next-task` takes item 2, Phase 2.

## NEXT STEPS (pick up here)
1. ⏳ Kerem: Email Address Obfuscation off on the `nepsis.day` zone; then Claude diffs the live pages against the repo, and writes the live diff into `README.md` as a release step (`check.py` sees the repo, not what the host adds). Also review the 404 text and the placeholder favicon.
2. Phase 2: `content/emergency-numbers.json` (D-2026-09-12-9, TR, US, GB, EU with sources), then `withdrawal.html` from the JSON with one `id="<CC>"` block per country, the `.suggestion-note` mark shown by `:target` with the VPN warning, and `docs/cloudflare-rules.md` (D-2026-09-12-11); Kerem reviews, Turkish of the warning ⏳. Every merge now goes live: Kerem approves the page before the merge.
3. ⏳ Kerem: the four redirect rules from `docs/cloudflare-rules.md` in the dashboard; confirm the geolocation field and the `#fragment` target are accepted on Free (D-2026-09-12-11 names the fallback).
4. ⏳ Kerem: Turkish of `/`, `/privacy` (the app's pass), `404`; the structure session; the email-list provider.

## Infra
- Hosting: Cloudflare Pages project `nepsis-day` on `kdemirtas/nepsis-day`, branch `main`, no build command, created 2026-09-26; merges to `main` publish. Web Analytics must stay off (it injects a script); ⏳ Email Address Obfuscation to turn off. Kerem's Cloudflare account, 2FA on.
- Domain: `nepsis.day`, Cloudflare Registrar since 2026-09-06; custom domain on the Pages project (2026-09-26); auto-renew and transfer lock set by Kerem the same day. `nepsis.dev` is unregistered as of 2026-09-12 (dropped for `.day` on 2026-09-06); `.com` is a US wealth-management firm, `.app` a fasting app, `.io` a security firm: not ours, never will be.
- Repo: `kdemirtas/nepsis-day`, public, created 2026-09-12; `main` carries the docs, the check and the copies. Every git and gh call: `GH_TOKEN=$(gh auth token --user kdemirtas)`.
- Toolchain: none in the repo. `python3` stdlib for `scripts/check.py` and its test; Lighthouse through `npx` with the Node 22 at `~/.local/node` (not on PATH), command in `README.md`. Local preview `python3 -m http.server 8080`.
- Sources of copied text: `~/code/personal/mobile-app/nepsis/` (`PRIVACY.md`, `sources/withdrawal-*.json`); byte-identical copies in `content/`, origin commit and rendering pages in `content/MANIFEST.md`.
