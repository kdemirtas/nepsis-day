# HANDOVER: nepsis.day
Type: generic
Resume point. Full detail in `STATUS.md` (top blockquote); shape of the code in `ARCHITECTURE.md`.

## CURRENT: docs shipped, repo live, no HTML yet (2026-09-12)
Doc set rendered by `/init-project` (type `generic`) on 2026-09-12, in the same session that distilled `nepsis` `sources/origin-night-lessons.md`. Kerem's calls today: generic type; own public repo at `~/code/personal/web/nepsis-day/`; hand-written HTML and CSS, no build step, no scripts; email list deferred. Structure beyond the three pages is his session, later. No HTML exists yet; no repo yet.
**RESUME:** run `/architect` (greenfield) in `~/code/personal/web/nepsis-day/`: confirm the `content/` and `scripts/check.py` boundaries and the copied-text contracts, then Phase 1 (`style.css`, `index.html`, `privacy.html`, `404.html`).

## NEXT STEPS (pick up here)
1. ✅ `git init`, `kdemirtas/nepsis-day` public, docs shipped (PR #1).
2. `/architect` (greenfield): confirm the `content/` and `scripts/check.py` boundaries and write the first real `DECISIONS.md` entries.
3. Phase 1: `style.css` from the app's `DESIGN.md` tokens, `index.html`, `privacy.html` (from `PRIVACY.md` at a named commit), `404.html`; local preview.
4. ⏳ Kerem: Cloudflare Pages project on the repo, `nepsis.day` DNS onto it, confirm auto-renew and transfer lock.
5. Phase 2: `withdrawal.html` from the app's JSON; Kerem reviews.
6. ⏳ Kerem: the structure session (what else the site carries), the email-list provider.
7. ⏳ One line for `web/` in `~/code/personal/CLAUDE.md` Project types.

## Infra
- Hosting: Cloudflare Pages, ⏳ project to create on `kdemirtas/nepsis-day`, branch `main`, no build command, output `/`. Kerem's Cloudflare account, 2FA on.
- Domain: `nepsis.day`, Cloudflare Registrar since 2026-09-06; ⏳ DNS `CNAME` onto the Pages project; ⏳ auto-renew and transfer lock confirmed. `nepsis.dev` is unregistered as of 2026-09-12 (dropped for `.day` on 2026-09-06); `.com` is a US wealth-management firm, `.app` a fasting app, `.io` a security firm: not ours, never will be.
- Repo: `kdemirtas/nepsis-day`, public, created 2026-09-12; local `main` initialised, nothing committed yet. Every git and gh call: `GH_TOKEN=$(gh auth token --user kdemirtas)`.
- Toolchain: none. `python3` stdlib for the planned check. Local preview `python3 -m http.server 8080`.
- Sources of copied text: `~/code/personal/mobile-app/nepsis/` (`PRIVACY.md`, `sources/withdrawal-*.json`); record the commit in each `content/` file.
