# nepsis-day: status
> Read `PROJECT.md` first (the spec). This file = where things stand and what to do next. Entries
> older than the current wave are in `STATUS_ARCHIVE.md`. Last updated **2026-09-12**.
> **Current wave:** init (since 2026-09-12)

> **TYPE FOLDER REGISTERED (2026-09-12, evening). Shipped.** `web/` added to `~/code/personal/CLAUDE.md` Project types and `~/code/personal/web/CLAUDE.md` written (folder template, doc set, conventions: plain HTML and CSS, no scripts needed to read, no server code, public repo, EN and TR, kdemirtas push prefix). Neither file is in a repo (`~/code/personal` is not one). No HTML yet; RESUME unchanged.

> **REPO CREATED, DOCS SHIPPED (2026-09-12). Staged.** `git init` on `main`, `kdemirtas/nepsis-day` created public and empty, this PR is the first commit (the eleven docs). Same session: the app's `sources/origin-night-lessons.md` was distilled and feeds `/withdrawal` (items 3, 7, 8). Still ⏳: Cloudflare Pages project and DNS, the email-list provider, Kerem's structure session. Next: `/architect`.

> **PROJECT INITIALISED (2026-09-12). Staged.** Doc set created via `/init-project` (type
> `generic`); scope agreed with Kerem. ⏳ the GitHub repo, ⏳ the Cloudflare Pages project and DNS, ⏳ the email-list provider, ⏳ Kerem's structure session.

## TL;DR
Docs only; no HTML written yet. The site is four pages in two languages, hand-written, no scripts, served by Cloudflare Pages from a public repo. Phase 1 (skeleton, `/` and `/privacy`) is workable now once the repo exists; the withdrawal page waits on Kerem's review of the copied text; Turkish waits on the app's Turkish pass; the email list waits on a provider; the wider structure waits on Kerem's session.

## Status at a glance
| Phase | What | State | Deliverable |
|-------|------|-------|-------------|
| 1 | skeleton: repo, Pages, `/`, `/privacy`, stylesheet, DNS | 🟡 defined, not built | `https://nepsis.day/`, `/privacy` |
| 2 | `/withdrawal` in English, sourced | 🟡 defined, not built | `/withdrawal`, Kerem-reviewed |
| 3 | Turkish mirror | ⏳ app's Turkish pass, Kerem's review | `/tr/*` |
| 4 | email list | ⏳ provider | a form on `/` or `/list` |
| 5 | structure review | ⏳ Kerem's session | an updated `PROJECT.md` Pages table |

## Current numbers
- Pages: 0 built, 3 planned per language (`/`, `/withdrawal`, `/privacy`), plus `404`.
- Languages: 2 (`en`, `tr`).
- Dependencies: 0.
- Sources to copy: 3 files from `kdemirtas/nepsis` (`PRIVACY.md`, `sources/withdrawal-en.json`, `sources/withdrawal-tr.json`).

## Next steps
1. `git init`, `gh repo create kdemirtas/nepsis-day --public` (kdemirtas token), first `/putdown`.
2. `/architect` (greenfield): confirm the `content/` and `scripts/check.py` boundaries and write the first real `DECISIONS.md` entries.
3. Phase 1: `style.css` from the app's `DESIGN.md` tokens, `index.html`, `privacy.html` (from `PRIVACY.md` at a named commit), `404.html`; local preview.
4. ⏳ Kerem: Cloudflare Pages project on the repo, `nepsis.day` DNS onto it, confirm auto-renew and transfer lock.
5. Phase 2: `withdrawal.html` from the app's JSON; Kerem reviews.
6. ⏳ Kerem: the structure session (what else the site carries), the email-list provider.
7. ⏳ One line for `web/` in `~/code/personal/CLAUDE.md` Project types.

## How to run
    cd ~/code/personal/web/nepsis-day
    python3 -m http.server 8080        # then open http://localhost:8080/
    python3 scripts/check.py           # planned: parses every page, diffs copied text, asserts no <script>

Deploy: push to `main`; Cloudflare Pages publishes the repo root with no build step (⏳ project to create).
