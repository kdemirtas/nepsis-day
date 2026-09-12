# ARCHITECTURE: nepsis-day
> **Owned by `/architect`. Two pages max. Last updated 2026-09-12.** Code follows this file; when
> they disagree, either the code is wrong or this file is, and a `DECISIONS.md` entry says which.

## Purpose
Serve three static pages in two languages with no server, no scripts required, and no data collected, and keep their text identical to the app repo's sources. The proof of the site is that it renders with JavaScript off and that its copied texts match their sources, both checked by `scripts/check.py` (D-2026-09-12-7), which has its own test under `tests/`.

## Boundaries
Modules, what each owns, and what it may import. A module not listed here does not exist yet;
`/architect` adds it before code does.

| Module | Owns | May import | Never imports |
|---|---|---|---|
| the pages (`index.html`, `withdrawal.html`, `privacy.html`, `404.html` at the root, and their `tr/` mirrors) | the HTML, one file per page and language; the header, footer and language switch repeated in each file | `style.css`, `assets/` | any script; any other page's markup (no includes without a build step); any host but its own |
| `style.css` | every visual token and rule, Plain and warm from the app's `DESIGN.md` (dp becomes px) | nothing | page-specific selectors (a page that needs its own rule gets a class here, named after the component) |
| `assets/` | the wordmark, the favicon; fonts only if BACKLOG 4 is promoted | nothing | anything larger than 200 KB |
| `content/` | byte-identical copies of the app repo's texts (`PRIVACY.md`, `withdrawal-en.json`, `withdrawal-tr.json`), the one text this repo authors (`emergency-numbers.json`, D-2026-09-12-9), and `MANIFEST.md` naming the origin of every file and the pages that render it (D-2026-09-12-12) | nothing | edits to a copied file: a change starts in the app repo and arrives as a new copy with a new manifest row |
| the country redirect (Cloudflare Single Redirects, Kerem's dashboard, not in this repo; D-2026-09-12-11) | one rule per country group: `/withdrawal` and `/tr/withdrawal` with no `c=` in the query redirect to the same path with `?c=<CC>#<CC>`, `<CC>` the uppercase code of `emergency-numbers.json` (`ip.src.country` is uppercase too); the rule text is `docs/cloudflare-rules.md` | nothing | code of any kind (a Worker, a Pages Function, a Snippet); any path but the two withdrawal pages |
| `scripts/check.py` | the proof: every page parses, no `<script>`, every copied text appears in its page, every twin resolves, every `content/` file matches its manifest row, every fault prints a FAIL line and never a traceback (D-2026-09-12-7) | Python stdlib; the local app checkout, read-only, when present | anything installed; the network |
| `tests/test_check.py` | the check's own proof: builds a temporary site with each fault planted and expects the FAIL line, and a clean one that passes | `scripts/check.py`, the Python stdlib | the real pages or `content/` |

## Layout

    index.html           `/`
    withdrawal.html      `/withdrawal`
    privacy.html         `/privacy`
    404.html             the not-found page; `tr/404.html` for `/tr/*` (⏳ confirm Pages resolves the nested one on the first deploy)
    tr/                  the Turkish mirror, same file names
    style.css            one stylesheet, Plain and warm tokens
    assets/              wordmark, favicon
    content/             copies and the manifest (`MANIFEST.md`)
    scripts/check.py     the proof, stdlib only
    tests/test_check.py  the proof's own test, `python3 -m unittest discover tests`
    docs/                longer reference docs the spec links; `cloudflare-rules.md` holds the redirect rules verbatim
    sources/             reference material, catalogued in `sources/SOURCES.md`

Cloudflare Pages serves the repo root; no build command, output directory `/`.

## Data contracts
Every artifact that crosses a module boundary or leaves the project: its grain, its writer, its
readers, and where the contract is asserted. "Nowhere" is a legal entry and a backlog item.

| Artifact | Grain (key) | Written by | Read by | Asserted in |
|---|---|---|---|---|
| `content/MANIFEST.md` | one row per file in `content/`: `file`, `repo`, `commit`, `path`, `copied_on`, `rendered_in` (the built pages that render it, space-separated, `-` until the first is built; the PR that builds a page fills the cell); `commit` is the full 40-character hash unless `repo` is this repo; a file is Markdown or JSON (D-2026-09-12-12, D-2026-09-12-15, D-2026-09-12-17) | the session that copies a text | `scripts/check.py`, the reviewer | `check.py`: every `content/` file has a row and every row a file; when `~/code/personal/mobile-app/nepsis/` is present, `git show <commit>:<path>` there equals the file byte for byte, else the row prints SKIP; a page named in `rendered_in` that does not exist is a FAIL |
| `content/withdrawal-en.json`, `-tr.json` | one object: `version`, `reviewedBy`, `sources[] {name, url}`, `timeline[] {fromHours, toHours, title, symptoms[]}`, `erNow[]`, `highRisk`, `closing` (the app's shape, unchanged) | copied from `kdemirtas/nepsis` `sources/` at the manifest commit | the pages its `rendered_in` names (by hand), `check.py` | `check.py`: every string leaf (each title, symptom, `erNow` line, `highRisk`, `closing`, source name) occurs in the page text |
| `content/PRIVACY.md` | one Markdown document | copied from `kdemirtas/nepsis` `PRIVACY.md` at the manifest commit | the pages its `rendered_in` names (by hand), `check.py` | `check.py`: every heading, paragraph and list item, Markdown markup stripped, occurs in the page text |
| `content/emergency-numbers.json` | one row per country: `country` (uppercase ISO 3166-1 alpha-2, `EU` for the 112 zone), `number`, `source` (URL), `checked_on`, nothing else | this repo (D-2026-09-12-9); the app copies it later | the pages its `rendered_in` names, `check.py` | `check.py`: every row has an `http(s)` `source` and a `number` of digits only; on each rendering page the element `id="<CC>"` exists and, inside it, the only run of two or more digits, in the text and in every attribute value except the structural ones (`id`, `class`, `lang`, `dir`, `role`, `rel`, `type`, `style`, `hreflang`), is that row's `number`; a `tel:` link in the block dials exactly `tel:<number>`; a `content:` rule in `style.css` writes no digits; every country block on a page has a row, and every page with a country block is in the row's `rendered_in`; the pick link is `?c=<CC>#<CC>` on the page's own path (D-2026-09-12-13, D-2026-09-12-19, D-2026-09-12-20) |
| the suggested country | one redirect per country group (TR, US, GB, the EU 112 zone), target `?c=<CC>#<CC>` in the uppercase code; a reader who arrives with any `c=` is never redirected, so a manual pick on the page sticks (D-2026-09-12-11) | Kerem, in the dashboard, from `docs/cloudflare-rules.md` | the browser; the page's CSS through `:target` | `check.py`: inside each `id="<CC>"` block on every rendering page, exactly one element of class `suggestion-note` and a link to `?c=<CC>#<CC>`; `docs/cloudflare-rules.md` contains `?c=<CC>#<CC>` for every row of the JSON; `style.css` carries, at top level outside any `@media`, a rule whose selector list contains `.suggestion-note` with `display: none` as its last such rule, and one whose list contains `.country:target .suggestion-note` (descendant or `>` child) with a display other than `none` (D-2026-09-12-16). The live redirect is checked by hand per release (`curl -sI https://nepsis.day/withdrawal` shows `Location` from a Turkish connection, nothing from an unlisted country) |
| the served site | one URL per page and language | Cloudflare Pages from `main` | anyone | nowhere; `check.py` runs before every push, Pages has no build step |

Page text, for every assertion above, is the HTML with tags removed, entities unescaped and whitespace collapsed, where a block-level tag (`p`, `li`, `h1` to `h6`, `div`, `section`, `td`, `br` and their kin) becomes a break and an inline tag (`strong`, `em`, `a`, `span`, `abbr`, `sup`) becomes nothing; a source string must occur in it verbatim after the same collapse (D-2026-09-12-17). The pages close every element explicitly, optional end tags included, so the check needs no browser-style implied closing (D-2026-09-12-14).

## Core types
The concepts the code passes around. Each has one definition; functions take the type, not its
fields.

| Type | Meaning | Defined in |
|---|---|---|
| Page | one HTML file, one language, one path; its Turkish twin has the same file name under `tr/`, and `<link rel="alternate" hreflang>` pairs them both ways | the file itself; `check.py` builds it from the path |
| Copied text | a `content/` file plus its manifest row (`repo`, `commit`, `path`, `rendered_in`); a block on a page is a copied text's rendering | `content/MANIFEST.md`; in code `check.py` `CopiedText`, passed whole |
| Emergency number | `country` (uppercase code), `number` (digits only), `source`, `checked_on` | `content/emergency-numbers.json`; in code `check.py` `EmergencyNumber` |
| Country block | the element `id="<CC>"` with class `country` on a withdrawal page: its text, its links, its one suggestion note (D-2026-09-12-18) | the page; in code `check.py` `Block` |
| Red flag | one `erNow` string, sourced by the JSON's `sources[]` | `content/withdrawal-*.json` |
| Timeline band | `fromHours`, `toHours`, `title`, `symptoms[]` | `content/withdrawal-*.json` |

## Invariants
What must hold after every run, each with the check that proves it.

- **No `<script>` on any page.** Check: `check.py` fails on any `<script` tag, any `on*` attribute, any `srcdoc` and any `javascript:`, `vbscript:` or `data:text/html` URL in any `.html`; `grep -rl "<script" *.html tr/` says the same for the tag. A future form embeds by `<form action>` only.
- **Every copied text matches its source.** Check: `check.py` asserts the manifest rows and the page text as the Data contracts say. No hand diff counts as the proof once the script exists.
- **Every page has its twin.** Check: `check.py` pairs each root `*.html` with `tr/*.html` of the same name; each carries `<link rel="alternate" hreflang>` to the other, whose `href` is the twin's served path (`/tr/withdrawal`, `/tr/` for the index) either root-relative or absolute on `nepsis.day`; a missing twin passes only if a ⏳ row in `STATUS.md` names it. `x-default` is optional.
- **Every medical claim cites a source on the page.** Check: the sources block at the bottom of `withdrawal.html` lists every entry of the JSON's `sources[]` by name; `check.py` covers it through the string-leaf rule.
- **Nothing collected, nothing fetched elsewhere.** Request allowlist: the page's own origin (`nepsis.day`, no `www`) only; fonts are the system stack. The country redirect reads a value Cloudflare computes for every request anyway and stores nothing (D-2026-09-12-11). Check: `check.py` fails on any URL to another host in `src`, `srcset`, `poster`, `data`, `action`, `formaction`, `ping`, `xlink:href`, the `href` of `<link>`, `<base>`, `<use>` and `<image>`, a `<meta http-equiv="refresh">` target, and in every `url()`, `image-set()` or `@import` of `style.css`, of a `<style>` block or of a `style` attribute, whatever the scheme's case; a `javascript:` value anywhere in those is a script; the browser's network panel confirms before each release. The deferred form's provider joins the allowlist by a `D-` id when D-2026-09-12-5 is replaced.
- **The suggestion is never the answer.** Every country block is on the page whatever the redirect does; the block the redirect targets is marked "likely yours" by CSS `:target` only, and the mark is the `.suggestion-note` element inside that block, carrying the warning that a VPN, a roaming SIM or a proxy can make it wrong. Without the redirect, or with a target the dashboard rejects, the page is the full table and nothing is missing. Check: `check.py` finds exactly one `.suggestion-note` inside every country block and the two top-level rules D-2026-09-12-16 names in `style.css`; a missing `style.css` fails the check once the JSON exists and prints SKIP before (D-2026-09-12-11, D-2026-09-12-16). A country block is rendered for every reader: it may not carry `hidden`, sit inside `<template>`, or be hidden by a `.country` rule without `:target`; inline `<style>` blocks are held to the same rules as `style.css` (⏳ the check for this sentence is NEXT item 4 in `HANDOVER.md`).
- **Every emergency number on a page comes from the table.** Check: `check.py`, as the Data contracts say: inside each country block the only digit run of two or more, in text and in every non-structural attribute value, is that country's number, a `tel:` link dials exactly it, no CSS `content:` rule writes digits, and a block without a row or a page with blocks outside `rendered_in` fails (D-2026-09-12-13, D-2026-09-12-19, D-2026-09-12-20). A wrong number is the worst bug the site can have.
- **Every element is closed explicitly.** No optional end tag is omitted, `</p>`, `</li>`, `</body>`, `</html>` included. Check: `check.py` fails a block tag opening inside an open `<p>`, an `<li>` opening inside an open `<li>`, an end tag that skips open elements, and any element still open at the end of the file (D-2026-09-12-14).

## Proof strategy
How a change is shown to be neutral, and how a change that is meant to move a number is shown
to move only that number.

`python3 scripts/check.py` passes, run by hand before every push and by `/reviewer` on every PR (D-2026-09-12-7); no CI. The check's own proof is `python3 -m unittest discover tests`: every FAIL path fires on a planted fault and a clean site passes. A subject that does not exist yet (a page, the stylesheet, the numbers file) prints SKIP, never silence; a subject that is named and missing (a `rendered_in` page) is a FAIL. A change is neutral if the check passes and the changed page, viewed with JavaScript disabled at 400 px and at 1200 px, reads the same as before except where the PR says it changes; a style change shows both screenshots. A content change is a new copy in `content/`, a new manifest row and the page edit in one PR; the diff that matters is `content/` old against new, never the page. Lighthouse accessibility and best practices 100 on the changed page.

## Longer material
What does not fit in two pages lives under `docs/` and is linked from the row or section it
supports; a doc no row links is a candidate for deletion.

- `docs/cloudflare-rules.md` (Phase 2): the redirect rules as text, one block per rule (expression, target `https://nepsis.day/withdrawal?c=<CC>#<CC>` and its `tr/` twin, preserve query string off), so the dashboard can be rebuilt from the repo. Candidates: the emergency-number sourcing notes per country, the Cloudflare Pages setup as done (screenshots of the dashboard steps), the Lighthouse runs per release.

## Change protocol
A structural change (a new module, a moved boundary, a changed contract or type) starts with
`/architect`, cites a `D-` id from `DECISIONS.md` in its commit, and is reviewed by `/reviewer`
against this file. A behavior change cites the decision that moved the number and updates every
place the number is quoted in the same PR.
