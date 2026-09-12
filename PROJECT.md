# nepsis.day: the public static site for Nepsis at `nepsis.day`, English and Turkish, no accounts, no server, no health data
> **Last updated 2026-09-12.** Read this first; `STATUS.md` says where things stand, `ARCHITECTURE.md`
> says how the code is shaped, `DECISIONS.md` says what was decided and why.

## Overview
Nepsis is a native Android recovery companion (Kotlin + Compose, `kdemirtas/nepsis`, private). It was born from one night alone in withdrawal abroad, with a laptop chat as the only companion; the app is that night, generalized. The site is the part of that night that belongs on the web: the person searching at 3am on a laptop is exactly who it serves, and the only things that helped were plain facts, red flags and a phone number. Everything else Nepsis does (the call button, the SMS cascade, noticing silence, the signals) needs a phone and cannot run in a browser, so the site never tries.

Four jobs, in priority order (Kerem's call, 2026-09-12):

1. **`/withdrawal`**: for someone alone in alcohol withdrawal tonight. The red flags that mean call now, the emergency number by country, the triage sentence to say at the door, the pre-visit bag list, the reasons people give for not going and the one-paragraph fact that answers each. Content from `nepsis` `sources/withdrawal-en.json`, `withdrawal-tr.json` and `sources/origin-night-lessons.md` items 3, 7 and 8. Medical text is Kerem's to approve; the site never diagnoses or doses.
2. **`/privacy`**: `PRIVACY.md` from the app repo, hosted verbatim. Required by the Play listing (`nepsis` `PUBLISHING.md` step 3).
3. **`/`**: what Nepsis is, in five sentences, and the three load-bearing promises (no fitted model, withdrawal treated as the emergency it is, emergency mode fully on the phone).
4. **An email list**: ⏳ provider undecided (deferred 2026-09-12); no form on the first cut.

English primary, Turkish secondary, mirrored paths (`/tr/withdrawal`). Emergency numbers key on country, not language, as in the app.

## What "done" means
`nepsis.day` serves `/`, `/withdrawal` and `/privacy` in English and Turkish from Cloudflare Pages, over HTTPS, with no JavaScript required to read any of them; the withdrawal page has been reviewed by Kerem in both languages and cites its sources; `PRIVACY.md` on the site is byte-identical to the app repo's copy at the tagged commit; the Play listing can point at `/privacy`. Lighthouse accessibility and best-practice scores of 100 on every page (Kerem's bar for a page a shaking hand has to read).

## Design decisions
1. **Static, hand-written HTML and CSS, no build step, no JavaScript needed to read.** Kerem's call, 2026-09-12, over a generator (Astro, Eleventy) and over a Python render script. Four pages in two languages do not earn a toolchain; a page for a bad night must load on a bad connection and render with scripts blocked. One shared stylesheet with the Plain and warm tokens from the app's `DESIGN.md` (paper ground, coral, Manrope and Nunito with system fallbacks, 22 px corners).
2. **Own public repo, `kdemirtas/nepsis-day`, at `~/code/personal/web/nepsis-day/`.** Kerem's call, 2026-09-12. Cloudflare Pages deploys from a public repo; the app repo stays private. A new type folder `web/` beside `cli/` and `mobile-app/` (listed there 2026-09-12, with `~/code/personal/web/CLAUDE.md` beside `cli/` and `mobile-app/`).
3. **No accounts, no server, no health data, ever, on the site.** Follows the app's decision 8 (the phone is the source of truth) and the Phase 5 rule (health data hosting waits for a real host). The site collects nothing; the email list, when it exists, is a third-party form and is said so on the page.
4. **Content is copied from the app repo, never rewritten here.** The withdrawal text and the privacy policy have one source each (`nepsis` `sources/withdrawal-*.json`, `nepsis` `PRIVACY.md`); the site carries a copy and the commit it came from. A wording change starts in the app repo.
5. **Emergency numbers key on country, not language.** Same rule as the app: a Turkish reader in Miami sees Turkish text and the US number. The country table is shared with the app's `MODEL.md` emergency-number table (⏳ source to pick there).
6. **Email list deferred.** Kerem's call, 2026-09-12: ⏳ provider (Buttondown was the candidate; a Cloudflare Worker crosses the no-server line). No form until then.

## Out of scope
- Anything that needs the phone: calls, SMS, the cascade, the sobriety record, signals, the AI Companion. The site links to the app and says what it cannot do.
- Accounts, logins, a web version of the app, any server-side code (Workers included).
- Analytics, cookies, tracking pixels, third-party scripts. Cloudflare's aggregate traffic counters are the only numbers.
- Medical advice beyond "get help, here is the number". No dosing, no diagnosis, no symptom checker.
- 12-step programme content and AA literature quotations (AAWS copyright); Step-1 ideas paraphrased only, as in the app.
- A blog, a press page, a store badge before the Play listing exists.

## Pages

| Path | Purpose | Source of the text | Languages |
|---|---|---|---|
| `/` | what Nepsis is, three promises, link to the app when it exists | this repo, Kerem approves | `en`, `tr` |
| `/withdrawal` | alone in withdrawal tonight: red flags, number by country, triage sentence, bag list, reasons-not-to-go answered | `nepsis` `sources/withdrawal-en.json`, `withdrawal-tr.json`, `origin-night-lessons.md` items 3, 7, 8 | `en`, `tr` |
| `/privacy` | the app's privacy policy, verbatim | `nepsis` `PRIVACY.md` at a named commit | `en`, ⏳ `tr` (the app's Turkish pass is pending) |
| ⏳ `/list` or a block on `/` | email list | ⏳ provider | `en`, `tr` |

Turkish pages live under `/tr/` with the same paths.

## Phases
| Phase | What | State |
|---|---|---|
| 1 | skeleton: repo, Pages, `/` and `/privacy` in English, stylesheet, domain wired | 🟡 defined, not built |
| 2 | `/withdrawal` in English, sourced, reviewed by Kerem | 🟡 defined, not built |
| 3 | Turkish mirror of every page | ⏳ awaiting the app's Turkish pass and Kerem's review |
| 4 | email list | ⏳ awaiting the provider decision |
| 5 | structure review with Kerem: what else the site carries | ⏳ Kerem's session, "we'll discuss the structure later" (2026-09-12) |

## Phase 1: skeleton

Repo `kdemirtas/nepsis-day` public; Cloudflare Pages project pointed at it; `nepsis.day` DNS moved onto the Pages project (⏳ Kerem: Cloudflare dashboard; the registrar is already Cloudflare); `index.html`, `privacy.html`, `style.css`, `404.html`; `PRIVACY.md` converted to HTML by hand with the source commit noted in a comment. **Deliverable.** `https://nepsis.day/` and `/privacy` live over HTTPS. **Blocked on.** Nothing on the code side; ⏳ the DNS switch is Kerem's.

## Phase 2: the withdrawal page

`withdrawal.html` from the app's JSON: the five timeline bands, the eight ER criteria, the number by country (Turkey and the US first), the triage sentence, the bag list, the reasons-not-to-go cards (`origin-night-lessons.md` item 8, country-keyed where the fact is national). Every medical claim cites its source at the bottom, the same six sources as the app. **Deliverable.** `/withdrawal` reviewed and approved by Kerem. **Blocked on.** Kerem's review; ⏳ the emergency-number source (shared with the app's `MODEL.md`).

## Phase 3: Turkish

`/tr/` mirror of every page; `<link rel="alternate" hreflang>` both ways; a language switch in the header, no auto-redirect (a Turk abroad chooses). **Deliverable.** Every page in both languages. **Blocked on.** ⏳ the app's Turkish pass over `PRIVACY.md` and the withdrawal JSON; Kerem reviews all Turkish.

## Phase 4: email list

⏳ Provider. A plain HTML form posting to the provider, a one-line notice of who receives the address, no script. **Blocked on.** Kerem's provider decision.

## Phase 5: structure review

Kerem's session on what else the site carries (screens, a store badge, a page for companions, a page for clinicians). Nothing is planned until then. **Blocked on.** Kerem.
