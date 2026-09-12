# ARCHITECTURE: nepsis-day
> **Owned by `/architect`. Two pages max. Last updated 2026-09-12.** Code follows this file; when
> they disagree, either the code is wrong or this file is, and a `DECISIONS.md` entry says which.

## Purpose
Serve three static pages in two languages with no server, no scripts required, and no data collected, and keep their text identical to the app repo's sources. The proof of the site is that it renders with JavaScript off and that its copied texts match their sources.

## Boundaries
Modules, what each owns, and what it may import. A module not listed here does not exist yet;
`/architect` adds it before code does.

| Module | Owns | May import | Never imports |
|---|---|---|---|
| the pages (`index.html`, `withdrawal.html`, `privacy.html`, `404.html` at the root, and their `tr/` mirrors) | the HTML, one file per page and language | `style.css`, `assets/` | any script; any other page's markup (no includes without a build step) |
| `style.css` | every visual token and rule, Plain and warm from the app's `DESIGN.md` | nothing | page-specific selectors (a page that needs its own rule gets a class here, named after the component) |
| `assets/` | the wordmark, the favicon, the fonts if self-hosted | nothing | anything larger than 200 KB (⏳ fonts: system stack first, self-host only if Kerem asks) |
| `content/` (planned) | the copied sources: `withdrawal-en.json`, `withdrawal-tr.json`, `PRIVACY.md`, each with `SOURCE` (repo, commit, path) at the top | nothing | edits: a change starts in the app repo |
| `scripts/check.py` (planned) | the proof: every page parses, every copied text matches `content/`, no `<script>` tag, every `hreflang` pair resolves | stdlib only | anything outside this repo |

## Layout

    index.html         `/`
    withdrawal.html    `/withdrawal`
    privacy.html       `/privacy`
    404.html
    tr/                the Turkish mirror, same file names
    style.css          one stylesheet, Plain and warm tokens
    assets/            wordmark, favicon
    content/           copied sources with their origin commit (planned)
    scripts/check.py   the proof (planned)
    docs/              longer reference docs the spec links
    sources/           reference material, catalogued in `sources/SOURCES.md`

Cloudflare Pages serves the repo root; no build command, output directory `/`.

## Data contracts
Every artifact that crosses a module boundary or leaves the project: its grain, its writer, its
readers, and where the contract is asserted. "Nowhere" is a legal entry and a backlog item.

| Artifact | Grain (key) | Written by | Read by | Asserted in |
|---|---|---|---|---|
| `content/withdrawal-en.json`, `-tr.json` | one object: `bands[]`, `criteria[]`, `sources[]` (the app's shape) | copied from `kdemirtas/nepsis` `sources/` at a named commit | `withdrawal.html` (by hand), `scripts/check.py` | `scripts/check.py` (planned): every band and criterion string appears in the page |
| `content/PRIVACY.md` | one document | copied from `kdemirtas/nepsis` `PRIVACY.md` at a named commit | `privacy.html` (by hand) | `scripts/check.py` (planned): every paragraph of the Markdown appears in the page |
| `content/emergency-numbers.json` (planned) | one row per country: `country`, `number`, `note` | ⏳ shared source with the app's `MODEL.md` table | `withdrawal.html` | nowhere yet (backlog) |
| the served site | one URL per page and language | Cloudflare Pages from `main` | anyone | nowhere; `check.py` runs before push, Pages has no build step |

## Core types
The concepts the code passes around. Each has one definition; functions take the type, not its
fields.

| Type | Meaning | Defined in |
|---|---|---|
| Page | one HTML file, one language, one path; its Turkish twin has the same file name under `tr/` | the file itself; `hreflang` links pair them |
| Copied text | a block on a page whose source is a file in `content/` with an origin commit | `content/*` header comment `SOURCE:` |
| Emergency number | `country`, `number`, `note` | `content/emergency-numbers.json` (planned) |
| Red flag | one ER criterion string, sourced | `content/withdrawal-*.json` `criteria[]` |

## Invariants
What must hold after every run, each with the check that proves it.

- **No `<script>` on any page.** Check: `grep -rl "<script" *.html tr/` is empty. A future form embeds by `<form action>` only.
- **Every copied text matches its source.** Check: `scripts/check.py` (planned) diffs page text against `content/`; until it exists, the reviewer diffs by hand and says so in the PR.
- **Every page has its twin.** Check: for each `*.html` at the root there is `tr/*.html` with a matching name, or a ⏳ row in `STATUS.md` naming it.
- **Every medical claim cites a source on the page.** Check: the sources block at the bottom of `withdrawal.html` lists the same six entries as the app's JSON `sources[]`.
- **Nothing collected.** Check: no cookie header, no third-party request except the deferred form's `action` URL; verified in the browser's network panel before each release.

## Proof strategy
How a change is shown to be neutral, and how a change that is meant to move a number is shown
to move only that number.

A change is neutral if `scripts/check.py` (planned; until then, the hand diff described in the PR) passes and the rendered page, viewed with JavaScript disabled at 400 px and at 1200 px, reads the same as before except where the PR says it changes. A content change names the app-repo commit it copies and the diff is against the previous `content/` copy. A style change shows the two screenshots. Lighthouse accessibility 100 on the changed page.

## Longer material
What does not fit in two pages lives under `docs/` and is linked from the row or section it
supports; a doc no row links is a candidate for deletion.

- `docs/` is empty at init. Candidates: the country table's sourcing notes, the Cloudflare Pages setup as done (screenshots of the dashboard steps), the Lighthouse runs per release.

## Change protocol
A structural change (a new module, a moved boundary, a changed contract or type) starts with
`/architect`, cites a `D-` id from `DECISIONS.md` in its commit, and is reviewed by `/reviewer`
against this file. A behavior change cites the decision that moved the number and updates every
place the number is quoted in the same PR.
