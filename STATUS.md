# nepsis-day: status
> Read `PROJECT.md` first (the spec). This file = where things stand and what to do next. Entries
> older than the current wave are in `STATUS_ARCHIVE.md`. Last updated **2026-09-26**.
> **Current wave:** init (since 2026-09-12)

> **PHASE 1b, ENGLISH PAGES (2026-09-26). Shipped as PR #6.** `style.css` (Plain and warm tokens; text colours darkened to 4.5:1, D-2026-09-26-2), `index.html` with the home text Kerem approved today (withdrawal banner left out until `/withdrawal` exists; "you"; no origin story), `privacy.html` rendered from `content/PRIVACY.md` (manifest `rendered_in` filled), `404.html`, placeholder `assets/favicon.svg` (a coral dot). Proof: `check.py` OK (every `PRIVACY.md` string on the page, Turkish twins pending by name); Lighthouse 12, accessibility 100 and best practices 100 on all three pages; screenshots at 400 and 1200 px read. `/reviewer` pass 1: numbering of the promises hidden by CSS and a stale page count, fixed; Lighthouse had not run, run in pass 2 with Node 22 from `~/.local/node`. ⏳ Kerem: the 404 text, the favicon, the Turkish of all three pages, the Pages project and DNS. Nothing is live.

> **PHASE 1a RESIDUE (2026-09-26). Shipped as PR #5.** `/orchestrate` ran HANDOVER NEXT item 4 unattended. `scripts/check.py` now reads inline `<style>` blocks like `style.css` (digit rule, hide and show rules read after the sheet), fails a country block hidden by `hidden`, `<template>`, a `style` attribute or any rule naming `.country` or `#<CC>` (`:is`, `:has` count, `:not` does not), and reads CSS as CSS: `;` ends `@import` and `@charset`, backslash escapes, `/*` inside strings, the `content` property only with escapes decoded. D-2026-09-26-1 records it; the ⏳ in ARCHITECTURE Invariants is closed. Proof: 11 tests, planted faults 93 to 115, each new check mutation-tested; `check.py` OK on the tree. `/reviewer`: pass 1 FIX FIRST (gate docstrings; two false PASSes in the selector reader, `:is(.country)` and `[data-note="a b"]`), pass 2 SHIP. Next ring of CSS gaps parked as BACKLOG 7 (trigger: Phase 1b, first real page).

> **ARCHITECT AND PHASE 1a (2026-09-12, late night). Staged.** `/architect` (greenfield) settled the residue in three answers (D-2026-09-12-7 check script in Phase 1, -8 byte-identical copies with `content/MANIFEST.md`, -9 the emergency-number table authored here) and, on Kerem's ask, designed the country suggestion for `/withdrawal` as a Cloudflare redirect to `?c=<CC>#<CC>` plus CSS `:target`, no script, no server (D-10, restated as D-11). `/next-task` built Phase 1a: `scripts/check.py` (the proof), `tests/test_check.py` (10 tests, 93 planted faults), `content/` with the three copies at app commit `19a1857` and the manifest. Two `/reviewer` loops of three passes each; Kerem's rule for the session: the docs move first by decision, code follows the rows, so D-12 to D-20 record what each pass sharpened (manifest `rendered_in`, uppercase codes, explicit closing of every element, attribute and CSS digit rules, top-level stylesheet rules). The shared web template was aligned with D-8 (`claude-shared` PR #8). Residue of the last pass is NEXT item 4 in `HANDOVER.md`. Still ⏳: Cloudflare Pages project and DNS, the redirect rules, the email-list provider, Kerem's structure session, Turkish of the suggestion note.

> **RE-STAMPED `webpage` (2026-09-12, night). Staged.** `/init-project webpage` here revealed no such type; Kerem's call: add it to the shared skill, then re-stamp this repo. `kdemirtas/claude-shared` PR #6 (merged) adds `templates/web/` (layout, rules, proof, infra fragments, `README.md`, dirs `assets/ content/ scripts/ docs/ sources/`), `references/type-web.md`, `render.py --type web`, and teaches `/pickup`, `/putdown`, `/architect` the stamp. This repo: `HANDOVER.md` and `CLAUDE.md` say `Type: webpage`, `DECISIONS.md` D-2026-09-12-6 replaces the `generic` choice; docs not re-rendered (they were the template's source). `~/code/personal/web/CLAUDE.md` Doc set points at the type (not in a repo). No HTML yet; RESUME unchanged.

> **TYPE FOLDER REGISTERED (2026-09-12, evening). Shipped.** `web/` added to `~/code/personal/CLAUDE.md` Project types and `~/code/personal/web/CLAUDE.md` written (folder template, doc set, conventions: plain HTML and CSS, no scripts needed to read, no server code, public repo, EN and TR, kdemirtas push prefix). Neither file is in a repo (`~/code/personal` is not one). No HTML yet; RESUME unchanged.

> **REPO CREATED, DOCS SHIPPED (2026-09-12). Staged.** `git init` on `main`, `kdemirtas/nepsis-day` created public and empty, this PR is the first commit (the eleven docs). Same session: the app's `sources/origin-night-lessons.md` was distilled and feeds `/withdrawal` (items 3, 7, 8). Still ⏳: Cloudflare Pages project and DNS, the email-list provider, Kerem's structure session. Next: `/architect`.

> **PROJECT INITIALISED (2026-09-12). Staged.** Doc set created via `/init-project` (type
> `generic`); scope agreed with Kerem. ⏳ the GitHub repo, ⏳ the Cloudflare Pages project and DNS, ⏳ the email-list provider, ⏳ Kerem's structure session.

## TL;DR
The proof exists, no page yet. `scripts/check.py` and its test are in; `content/` holds the three copies from the app at `19a1857` with their manifest. The site is four pages in two languages, hand-written, no scripts, served by Cloudflare Pages from a public repo. Phase 1b (stylesheet, `/`, `/privacy`, `404`) is next; the withdrawal page waits on Kerem's review of the copied text; Turkish waits on the app's Turkish pass; the email list waits on a provider; the wider structure waits on Kerem's session.

## Status at a glance
| Phase | What | State | Deliverable |
|-------|------|-------|-------------|
| 1 | skeleton: repo, Pages, `/`, `/privacy`, stylesheet, DNS | 🟡 1a done (check, copies, manifest, residue pass); 1b pages built in English (`/`, `/privacy`, `404`), Pages and DNS ⏳ | `https://nepsis.day/`, `/privacy` |
| 2 | `/withdrawal` in English, sourced | 🟡 defined, not built | `/withdrawal`, Kerem-reviewed |
| 3 | Turkish mirror | ⏳ app's Turkish pass, Kerem's review | `/tr/*` |
| 4 | email list | ⏳ provider | a form on `/` or `/list` |
| 5 | structure review | ⏳ Kerem's session | an updated `PROJECT.md` Pages table |

## Current numbers
- Turkish twins, one row each so `check.py` lets the English page ship alone:
  - ⏳ `tr/index.html`: Kerem's Turkish of the approved home page text
  - ⏳ `tr/privacy.html`: the app's Turkish pass of `PRIVACY.md`
  - ⏳ `tr/404.html`: Kerem's Turkish of the not-found text
- Pages: 3 built in English (`/`, `/privacy`, `404`), 0 in Turkish; `/withdrawal` planned (Phase 2).
- Languages: 2 (`en`, `tr`).
- Dependencies: 0. Proof: 11 tests, 115 planted faults, `check.py` green on the tree.
- Sources copied: 3 files from `kdemirtas/nepsis` at `19a1857` (`PRIVACY.md`, `sources/withdrawal-en.json`, `sources/withdrawal-tr.json`), byte-identical, listed in `content/MANIFEST.md`.

## Next steps
The ordered list is `HANDOVER.md` NEXT. In short: Phase 1b (stylesheet and the four pages), ⏳ Kerem's Cloudflare Pages project and DNS, Phase 2 (`emergency-numbers.json`, `withdrawal.html`, `docs/cloudflare-rules.md`), ⏳ Kerem's redirect rules in the dashboard, ⏳ the structure session and the email-list provider.

## How to run
    cd ~/code/personal/web/nepsis-day
    python3 -m http.server 8080        # then open http://localhost:8080/
    python3 scripts/check.py           # the proof: pages parse, no <script>, copies match content/MANIFEST.md, twins resolve

Deploy: push to `main`; Cloudflare Pages publishes the repo root with no build step (⏳ project to create).
