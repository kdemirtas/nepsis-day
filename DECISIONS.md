# DECISIONS: nepsis-day
> One entry per decision, newest first, never edited after the fact: a reversed decision gets a
> new entry that names the one it replaces. Ids are `D-YYYY-MM-DD-n`. Code that implements a
> decision cites the id; `/reviewer` checks the citation both ways.

| Id | Decided | What | Replaces |
|---|---|---|---|
| D-2026-09-12-6 | 2026-09-12 | Type `webpage`: the site is the first project under the new init-project type | D-2026-09-12-2 |
| D-2026-09-12-5 | 2026-09-12 | Email list deferred: no form until a provider is chosen | none |
| D-2026-09-12-4 | 2026-09-12 | Hand-written HTML and CSS, no build step, no JavaScript needed to read | none |
| D-2026-09-12-3 | 2026-09-12 | Own public repo `kdemirtas/nepsis-day` at `~/code/personal/web/nepsis-day/` | none |
| D-2026-09-12-2 | 2026-09-12 | Type `generic` for the site, not `mobile-app` | none |
| D-2026-09-12-1 | 2026-09-12 | Project initialised under this doc set | none |

## D-2026-09-12-1: project initialised under this doc set
**What.** nepsis-day starts with the common doc set plus the `generic` additions.
**Evidence.** `/init-project` run on 2026-09-12; scope agreed with Kerem in the init interview.
**Replaces.** Nothing.
**Cited by.** `HANDOVER.md` (the Type stamp).

## D-2026-09-12-6: type `webpage`
**What.** The `Type:` stamp becomes `webpage`, the static-site type added to `/init-project` on 2026-09-12 (`templates/web/`, `references/type-web.md`). The type encodes what this repo's docs already say: pages at the root, a language mirror, one `style.css`, `content/` with a `SOURCE:` commit per copied text, `scripts/check.py` as the proof, no scripts, no server. The existing docs are not re-rendered; they were the template's source.
**Evidence.** Kerem's call, 2026-09-12 evening: `/init-project webpage` in this repo, "add a webpage type to the skill, then re-stamp nepsis-day". `/pickup`, `/putdown` and `/architect` read the new stamp.
**Replaces.** D-2026-09-12-2 (type `generic`, chosen because no closer type existed).
**Cited by.** `HANDOVER.md` (the Type stamp), `CLAUDE.md`.

## D-2026-09-12-5: email list deferred
**What.** No sign-up form on the first cut; ⏳ the provider is undecided. Buttondown was the candidate; a Cloudflare Worker was rejected because a Worker is a server.
**Evidence.** Kerem's call in the `/init-project` interview, 2026-09-12 ("Defer, mark ⏳").
**Replaces.** Nothing.
**Cited by.** `PROJECT.md` design decision 6, phase 4.

## D-2026-09-12-4: hand-written HTML and CSS, no build step, no scripts
**What.** Every page is a hand-written HTML file sharing one `style.css`; no generator, no framework, no npm; no JavaScript is needed to read any page. A feature that needs a script is a `BACKLOG.md` row.
**Evidence.** Kerem's call in the init interview, 2026-09-12, over Astro or Eleventy and over a Python render script. The page for a bad night must load on a bad connection with scripts blocked.
**Replaces.** Nothing.
**Cited by.** `PROJECT.md` design decision 1, `ARCHITECTURE.md` invariant "No `<script>` on any page", `CLAUDE.md` rules.

## D-2026-09-12-3: own public repo under a new `web/` type folder
**What.** The site is `kdemirtas/nepsis-day`, public, at `~/code/personal/web/nepsis-day/`, separate from the private app repo, so Cloudflare Pages can deploy from it. `web/` is a new type folder beside `cli/` and `mobile-app/` (⏳ one line in `~/code/personal/CLAUDE.md`).
**Evidence.** Kerem's call in the init interview, 2026-09-12, over a folder beside the app under `mobile-app/` and over a `site/` directory inside the app repo.
**Replaces.** Nothing.
**Cited by.** `PROJECT.md` design decision 2, `HANDOVER.md` Infra.

## D-2026-09-12-2: type `generic`
**What.** The site takes the `generic` doc set (common docs plus `README.md`), not `mobile-app`.
**Evidence.** Kerem's call in the init interview, 2026-09-12: a static site is neither an app nor a CLI; the store and toolchain docs would be stubs.
**Replaces.** Nothing.
**Cited by.** `HANDOVER.md` (the Type stamp).
