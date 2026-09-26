# BACKLOG: nepsis-day

Parked ideas and decisions, not committed work. One entry each: what, why, and the trigger that
promotes it to HANDOVER's NEXT list. Committed and ordered work lives in `HANDOVER.md`; what was
decided lives in `DECISIONS.md`; what shipped lives in `CHANGELOG.md`. Promotion is Kerem's call
at `/pickup`, which lists the entries whose trigger is now true.

| # | what | why | trigger | parked |
|---|---|---|---|---|
| 1 | a page for Human Companions (what the invite means, what the cascade will ask of them) | the companion is the second reader of the site; the app's P7 invite SMS could link here | P7 merged in the app and Kerem's structure session | 2026-09-12 |
| 2 | a page for clinicians (what the app records, what it never does, the medical card format) | a psychiatrist or transplant team asked what the app is | Phase 5 of the app (a clinician on board) | 2026-09-12 |
| 3 | a store badge and screenshots on `/` | the listing exists | the app's first Play upload (P10) | 2026-09-12 |
| 4 | self-hosted Manrope and Nunito | the system stack looks off on some phones | Kerem sees it and says so; 200 KB budget | 2026-09-12 |
| 5 | ~~`scripts/check.py`, the automated proof~~ promoted to Phase 1 by D-2026-09-12-7 on 2026-09-12 | hand diffs of copied text will drift | closed | 2026-09-12 |
| 6 | a redirect from `nepsis.dev` if Kerem registers it | he remembered `.dev` as the domain on 2026-09-12 | Kerem registers it | 2026-09-12 |
| 7 | the check's remaining CSS blind spots: a rule that re-shows `.suggestion-note` without being `.suggestion-note` itself (`body .suggestion-note`, a nested rule, higher specificity), `!important` weighed against source order, `counter()` in a `content:` value, other ways to hide a country block (`opacity: 0`, `height: 0` with `overflow: hidden`, `content-visibility`, `clip-path`, a closed `<details>`, an ancestor hidden by a class rule), and the document order of a `<style>` block against the `style.css` link (read after it today, the worst case) | the residue pass (D-2026-09-26-1) closed the six named gaps; these are the next ring, none reachable by the pages as specified, each a way a hand edit could still hide the suggestion or a number | Phase 1b, first real page | 2026-09-26 |
