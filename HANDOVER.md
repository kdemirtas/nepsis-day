# HANDOVER: nepsis.day
Type: webpage
Resume point. Full detail in `STATUS.md` (top blockquote); shape of the code in `ARCHITECTURE.md`.

## CURRENT: English pages built, nothing live yet (2026-09-26)
`/`, `/privacy` and `404` exist in English with `style.css`; Lighthouse 100 and 100 on each; `check.py` green. Turkish twins are ⏳ rows in `STATUS.md`. The site goes live only when Kerem creates the Pages project (item 1). BACKLOG 7 (the next ring of CSS gaps) had the trigger "Phase 1b, first real page", now true: Kerem promotes or re-parks it. Decisions so far: D-2026-09-12-1 to -20, D-2026-09-26-1 and -2.
**RESUME:** Kerem: review the 404 text and the placeholder favicon, create the Cloudflare Pages project (Lighthouse is already run). Then `/next-task` takes item 2, Phase 2: `content/emergency-numbers.json` with a cited source per row, then `withdrawal.html`.

## NEXT STEPS (pick up here)
1. ⏳ Kerem: Cloudflare Pages project on the repo, `nepsis.day` DNS onto it, confirm auto-renew and transfer lock; then check `/privacy` resolves and `tr/404.html` behaviour on the first deploy.
2. Phase 2: `content/emergency-numbers.json` (D-2026-09-12-9, TR, US, GB, EU with sources), then `withdrawal.html` from the JSON with one `id="<CC>"` block per country, the `.suggestion-note` mark shown by `:target` with the VPN warning, and `docs/cloudflare-rules.md` (D-2026-09-12-11); Kerem reviews, Turkish of the warning ⏳.
3. ⏳ Kerem: the four redirect rules from `docs/cloudflare-rules.md` in the dashboard; confirm the geolocation field and the `#fragment` target are accepted on Free (D-2026-09-12-11 names the fallback).
4. ⏳ Kerem: Turkish of `/`, `/privacy` (the app's pass), `404`; the structure session; the email-list provider.

## Infra
- Hosting: Cloudflare Pages, ⏳ project to create on `kdemirtas/nepsis-day`, branch `main`, no build command, output `/`. Kerem's Cloudflare account, 2FA on.
- Domain: `nepsis.day`, Cloudflare Registrar since 2026-09-06; ⏳ DNS `CNAME` onto the Pages project; ⏳ auto-renew and transfer lock confirmed. `nepsis.dev` is unregistered as of 2026-09-12 (dropped for `.day` on 2026-09-06); `.com` is a US wealth-management firm, `.app` a fasting app, `.io` a security firm: not ours, never will be.
- Repo: `kdemirtas/nepsis-day`, public, created 2026-09-12; `main` carries the docs, the check and the copies. Every git and gh call: `GH_TOKEN=$(gh auth token --user kdemirtas)`.
- Toolchain: none in the repo. `python3` stdlib for `scripts/check.py` and its test; Lighthouse through `npx` with the Node 22 at `~/.local/node` (not on PATH), command in `README.md`. Local preview `python3 -m http.server 8080`.
- Sources of copied text: `~/code/personal/mobile-app/nepsis/` (`PRIVACY.md`, `sources/withdrawal-*.json`); byte-identical copies in `content/`, origin commit and rendering pages in `content/MANIFEST.md`.
