# HANDOVER: nepsis.day
Type: webpage
Resume point. Full detail in `STATUS.md` (top blockquote); shape of the code in `ARCHITECTURE.md`.

## CURRENT: the proof is complete for Phase 1, no HTML yet (2026-09-26)
The repo is live (`kdemirtas/nepsis-day`, PRs #1 to #4 and this one merged). Phase 1a is done: `scripts/check.py` with 11 tests and 115 planted faults, the three copies from the app at `19a1857`, the manifest. The residue pass (D-2026-09-26-1) closed the six gaps of the last review; the next ring is BACKLOG 7, due at Phase 1b's first real page. Decisions so far: D-2026-09-12-1 to -20, D-2026-09-26-1.
**RESUME:** `/next-task` takes NEXT item 1, Phase 1b: `style.css` from the app's `DESIGN.md` tokens, then `index.html`, `privacy.html` (fill `rendered_in` for `PRIVACY.md`), `404.html`; `check.py` green; judge BACKLOG 7 when the first page lands.

## NEXT STEPS (pick up here)
1. Phase 1b: `style.css` from the app's `DESIGN.md` tokens, `index.html`, `privacy.html` (from `content/PRIVACY.md`, fill its `rendered_in`), `404.html`; local preview; `check.py` green.
2. ⏳ Kerem: Cloudflare Pages project on the repo, `nepsis.day` DNS onto it, confirm auto-renew and transfer lock.
3. Phase 2: `content/emergency-numbers.json` (D-2026-09-12-9, TR, US, GB, EU with sources), then `withdrawal.html` from the JSON with one `id="<CC>"` block per country, the `.suggestion-note` mark shown by `:target` with the VPN warning, and `docs/cloudflare-rules.md` (D-2026-09-12-11); Kerem reviews, Turkish of the warning ⏳.
4. ⏳ Kerem: the four redirect rules from `docs/cloudflare-rules.md` in the dashboard; confirm the geolocation field and the `#fragment` target are accepted on Free (D-2026-09-12-11 names the fallback).
5. ⏳ Kerem: the structure session (what else the site carries), the email-list provider.

## Infra
- Hosting: Cloudflare Pages, ⏳ project to create on `kdemirtas/nepsis-day`, branch `main`, no build command, output `/`. Kerem's Cloudflare account, 2FA on.
- Domain: `nepsis.day`, Cloudflare Registrar since 2026-09-06; ⏳ DNS `CNAME` onto the Pages project; ⏳ auto-renew and transfer lock confirmed. `nepsis.dev` is unregistered as of 2026-09-12 (dropped for `.day` on 2026-09-06); `.com` is a US wealth-management firm, `.app` a fasting app, `.io` a security firm: not ours, never will be.
- Repo: `kdemirtas/nepsis-day`, public, created 2026-09-12; `main` carries the docs, the check and the copies. Every git and gh call: `GH_TOKEN=$(gh auth token --user kdemirtas)`.
- Toolchain: none. `python3` stdlib for `scripts/check.py` and its test. Local preview `python3 -m http.server 8080`.
- Sources of copied text: `~/code/personal/mobile-app/nepsis/` (`PRIVACY.md`, `sources/withdrawal-*.json`); byte-identical copies in `content/`, origin commit and rendering pages in `content/MANIFEST.md`.
