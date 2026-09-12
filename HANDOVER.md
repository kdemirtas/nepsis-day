# HANDOVER: nepsis.day
Type: webpage
Resume point. Full detail in `STATUS.md` (top blockquote); shape of the code in `ARCHITECTURE.md`.

## CURRENT: architecture written, the proof and the copies in, no HTML yet (2026-09-12)
Doc set rendered by `/init-project` (type `generic`, re-stamped `webpage` the same night once the type existed: `claude-shared` PR #6, D-2026-09-12-6) on 2026-09-12, in the same session that distilled `nepsis` `sources/origin-night-lessons.md`. Kerem's calls today: generic type; own public repo at `~/code/personal/web/nepsis-day/`; hand-written HTML and CSS, no build step, no scripts; email list deferred. Structure beyond the three pages is his session, later. No HTML exists yet; no repo yet.
**RESUME:** `/next-task` takes NEXT item 4, the Phase 1a residue pass on `scripts/check.py` (six code fixes with planted faults, then `/reviewer` as the ship gate); then Phase 1b (`style.css`, `index.html`, `privacy.html`, `404.html`). Decisions so far: D-2026-09-12-1 to -20.

## NEXT STEPS (pick up here)
1. ✅ `git init`, `kdemirtas/nepsis-day` public, docs shipped (PR #1).
2. ✅ `/architect` (greenfield, 2026-09-12): boundaries and contracts written, D-2026-09-12-7, -8, -9.
3. ✅ Phase 1a (2026-09-12): `scripts/check.py`, `tests/test_check.py` (10 tests, 93 planted faults), `content/MANIFEST.md` with the three copies at app commit `19a1857`; two `/reviewer` loops, D-2026-09-12-11 to -20 written along the way.
4. Phase 1a residue, one code pass with a planted fault for each, then `/reviewer` as the ship gate; leftovers go to `BACKLOG.md` with the trigger "Phase 1b, first real page": (a) inline `<style>` blocks held to the `content:` digit rule and the display rules like `style.css`; (b) a country block that is `hidden`, inside `<template>`, or hidden by a `.country` rule without `:target` is a FAIL; (c) a top-level at-statement ending in `;` (`@charset`, `@import`) ends the selector instead of gluing to the next rule; (d) escaped quotes inside CSS strings; (e) the `content:` regex matches the property only, not `.content:hover`, and ignores `\201C`-style escapes; (f) faults for the numbers row naming a missing page and for comment stripping in `read_css`.
5. Phase 1b: `style.css` from the app's `DESIGN.md` tokens, `index.html`, `privacy.html` (from `content/PRIVACY.md`, fill its `rendered_in`), `404.html`; local preview; `check.py` green.
6. ⏳ Kerem: Cloudflare Pages project on the repo, `nepsis.day` DNS onto it, confirm auto-renew and transfer lock.
7. Phase 2: `content/emergency-numbers.json` (D-2026-09-12-9, TR, US, GB, EU with sources), then `withdrawal.html` from the JSON with one `id="<CC>"` block per country, the `.suggestion-note` mark shown by `:target` with the VPN warning, and `docs/cloudflare-rules.md` (D-2026-09-12-11); Kerem reviews, Turkish of the warning ⏳.
8. ⏳ Kerem: the four redirect rules from `docs/cloudflare-rules.md` in the dashboard; confirm the geolocation field and the `#fragment` target are accepted on Free (D-2026-09-12-11 names the fallback).
9. ⏳ Kerem: the structure session (what else the site carries), the email-list provider.
10. ✅ `web/` listed in `~/code/personal/CLAUDE.md` Project types and `~/code/personal/web/CLAUDE.md` written (2026-09-12).
11. ✅ `webpage` type in `/init-project`; this repo stamped with it (2026-09-12).

## Infra
- Hosting: Cloudflare Pages, ⏳ project to create on `kdemirtas/nepsis-day`, branch `main`, no build command, output `/`. Kerem's Cloudflare account, 2FA on.
- Domain: `nepsis.day`, Cloudflare Registrar since 2026-09-06; ⏳ DNS `CNAME` onto the Pages project; ⏳ auto-renew and transfer lock confirmed. `nepsis.dev` is unregistered as of 2026-09-12 (dropped for `.day` on 2026-09-06); `.com` is a US wealth-management firm, `.app` a fasting app, `.io` a security firm: not ours, never will be.
- Repo: `kdemirtas/nepsis-day`, public, created 2026-09-12; local `main` initialised, nothing committed yet. Every git and gh call: `GH_TOKEN=$(gh auth token --user kdemirtas)`.
- Toolchain: none. `python3` stdlib for `scripts/check.py` and its test. Local preview `python3 -m http.server 8080`.
- Sources of copied text: `~/code/personal/mobile-app/nepsis/` (`PRIVACY.md`, `sources/withdrawal-*.json`); byte-identical copies in `content/`, origin commit and rendering pages in `content/MANIFEST.md`.
