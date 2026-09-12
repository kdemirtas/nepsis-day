# CLAUDE.md: nepsis-day

the public static site for Nepsis at `nepsis.day`, English and Turkish, no accounts, no server, no health data

Read `HANDOVER.md` first, then the top of `STATUS.md`, then `ARCHITECTURE.md` before touching
code. Type `generic`.

## Doc set

    HANDOVER.md        resume pointer, read first
    STATUS.md          session log, current wave; older entries in STATUS_ARCHIVE.md
    PROJECT.md         what and why, phases
    ARCHITECTURE.md    boundaries, contracts, types, invariants, proof; owned by /architect
    DECISIONS.md       dated D- ids: what was decided, the evidence, what it replaced
    CHANGELOG.md       one line per merged PR under its version or vintage
    BACKLOG.md         parked ideas: what, why, trigger
    sources/SOURCES.md reference material catalog

## Rules

- **Structure before code.** A change that adds a module, moves a boundary, or changes a
  contract or core type goes through `/architect` first and cites its `D-` id.
- **Code is the source of truth.** Docs describe what the code does today. A PR that changes
  behavior updates the spec `ARCHITECTURE.md` links in the same PR; a doc that disagrees with the
  code is a defect in the doc unless a `DECISIONS.md` entry says the code is wrong.
- **No history in code.** Comments say what the code does now. Why it changed lives in
  `DECISIONS.md`; when it shipped lives in `CHANGELOG.md`. A date in a comment is a review finding.
- **No switch without a decision.** A new flag, widget or mode names the `D-` id that needs it and
  the date it may be removed. A switch whose branches do the same thing is deleted, not kept.
- **Types, not tuples.** A concept in `ARCHITECTURE.md` Core types is passed as that type. A
  function over four parameters is a review finding.
- **Prove neutrality the project's way.** Every PR states which proof from `ARCHITECTURE.md`
  ran and its result; "tests pass" alone is not a proof of neutrality.
- **Numbers travel together.** A change that moves a quoted figure restates it everywhere it is
  quoted in the same PR.
- **No JavaScript on the pages.** A reader with scripts blocked, on a bad connection, at 3am, gets every word. A feature that needs a script goes in `BACKLOG.md` with the reason.
- **Copied texts are never edited here.** The withdrawal text and the privacy policy change in `kdemirtas/nepsis` first; this repo copies and records the commit.
- **Every user-facing string exists in English and Turkish, or the Turkish is a ⏳ row in `STATUS.md`.** Never invent Turkish; Kerem reviews all of it. Turkish needs ğüşıöç.
- **Never judging, never blunt, never medical beyond "get help, here is the number".** The app's never-say list (`nepsis` `DESIGN.md`) applies word for word. "Suggests", never "predict".
- **No 12-step content, no AA quotations** (AAWS copyright).
- **Plain HTML and CSS only.** No generator, no framework, no npm. The stylesheet is the only shared file; a page reads on its own.
- **Push as kdemirtas.** `GH_TOKEN=$(gh auth token --user kdemirtas)` on every push, pull and `gh` call; plain `git push` fails with "Repository not found" on this account.
- Descriptive snake_case names, no one-letter or cryptic names in anything Kerem reads.
- No em-dashes in anything written here. Colon, comma, parentheses, or split the sentence.

## Environment
- No toolchain. A browser and a text editor. `python3` (stdlib) for `scripts/check.py` when it exists.
- Cloudflare: Kerem's account (2FA on), registrar for `nepsis.day` since 2026-09-06 (⏳ auto-renew and transfer lock to confirm), ⏳ a Pages project pointed at `kdemirtas/nepsis-day`, DNS `CNAME` onto it. No API token in this repo, ever.
- GitHub: `kdemirtas/nepsis-day`, public, created 2026-09-12 (empty until the first `/putdown`).
- Local preview: `python3 -m http.server 8080` from the repo root, then `http://localhost:8080/`.

## Related
- `~/code/personal/mobile-app/nepsis/` (`kdemirtas/nepsis`, private): the app. Sources of every copied text (`PRIVACY.md`, `sources/withdrawal-*.json`), the design tokens (`DESIGN.md` Visual direction), the never-say list, the origin lessons (`sources/origin-night-lessons.md`). Separate repo, not a dependency.
- `~/code/personal/mobile-app/gaffer/` (`kdemirtas/gaffer`): `PRIVACY.md` voice; nothing else.
