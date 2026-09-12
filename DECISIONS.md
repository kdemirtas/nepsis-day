# DECISIONS: nepsis-day
> One entry per decision, newest first, never edited after the fact: a reversed decision gets a
> new entry that names the one it replaces. Ids are `D-YYYY-MM-DD-n`. Code that implements a
> decision cites the id; `/reviewer` checks the citation both ways.

| Id | Decided | What | Replaces |
|---|---|---|---|
| D-2026-09-12-20 | 2026-09-12 | The number rule reads every non-structural attribute and forbids digits in CSS `content:`; a block without a row and a page with blocks outside `rendered_in` fail; the pick link stays on the page's own path | none |
| D-2026-09-12-19 | 2026-09-12 | `alt` joins the attributes the country-block number rule reads | none |
| D-2026-09-12-18 | 2026-09-12 | Country block is a Core type: the `id="<CC>"` element with class `country`, its text, links and one note | none |
| D-2026-09-12-17 | 2026-09-12 | The proof's definitions made exact: page text breaks at block tags only, `number` is digits only, a content file is Markdown or JSON, a manifest commit is the full hash, the test imports the stdlib | none |
| D-2026-09-12-16 | 2026-09-12 | The two stylesheet rules sit at top level outside `@media`; grouped selectors and the `>` combinator are accepted | none |
| D-2026-09-12-15 | 2026-09-12 | `rendered_in` names built pages only, `-` until then; a named page that is missing is a FAIL | none |
| D-2026-09-12-14 | 2026-09-12 | Every element is closed explicitly on every page; the check fails optional end tags left out | none |
| D-2026-09-12-13 | 2026-09-12 | The country-block number rule covers `href`, `aria-label` and `title`; a `tel:` link dials exactly the row's number | none |
| D-2026-09-12-12 | 2026-09-12 | `content/MANIFEST.md` gains `rendered_in`: the pages that render each copy; the check reads it instead of a list in the script | D-2026-09-12-8 |
| D-2026-09-12-11 | 2026-09-12 | The country suggestion restated so the check can prove it: uppercase code in the anchor, the JSON and the redirect target; one note and one pick link inside each country block; the two CSS rules named | D-2026-09-12-10 |
| D-2026-09-12-10 | 2026-09-12 | The withdrawal page suggests the reader's country from the connection, by a Cloudflare redirect to `?c=<cc>#<cc>` and CSS `:target`; no script, no server code; the mark says it may be wrong | none |
| D-2026-09-12-9 | 2026-09-12 | `content/emergency-numbers.json` is authored in this repo, the one exception to the copy rule; the app copies it later | none |
| D-2026-09-12-8 | 2026-09-12 | `content/` holds byte-identical copies; provenance lives in `content/MANIFEST.md`, not in a header | none |
| D-2026-09-12-7 | 2026-09-12 | `scripts/check.py` is Phase 1 work, before the first page; run by hand and by `/reviewer`, no CI | none |
| D-2026-09-12-6 | 2026-09-12 | Type `webpage`: the site is the first project under the new init-project type | D-2026-09-12-2 |
| D-2026-09-12-5 | 2026-09-12 | Email list deferred: no form until a provider is chosen | none |
| D-2026-09-12-4 | 2026-09-12 | Hand-written HTML and CSS, no build step, no JavaScript needed to read | none |
| D-2026-09-12-3 | 2026-09-12 | Own public repo `kdemirtas/nepsis-day` at `~/code/personal/web/nepsis-day/` | none |
| D-2026-09-12-2 | 2026-09-12 | Type `generic` for the site, not `mobile-app` | none |
| D-2026-09-12-1 | 2026-09-12 | Project initialised under this doc set | none |

## D-2026-09-12-20: the number rule closes its remaining doors
**What.** Inside a country block every attribute value except the structural ones (`id`, `class`, `lang`, `dir`, `role`, `rel`, `type`, `style`, `hreflang`) joins the digit-run rule, so `value`, `placeholder` and `data-*` are read like `alt`. A `content:` rule in `style.css` may write no run of two or more digits. Every country block on a page must have a row in `emergency-numbers.json`, and every page carrying a country block must be in that row's `rendered_in`. The pick link is `?c=<CC>#<CC>` bare, on the page's own served path, or absolute on `nepsis.day`; a link elsewhere does not count. Script schemes are `javascript:`, `vbscript:` and `data:text/html`.
**Evidence.** `/reviewer`, fresh loop pass 2, 2026-09-12, correctness findings 1, 2, 3, 5, 6: an unsourced GB block passed, a Turkish page outside `rendered_in` was never inspected, a pick link to the preview domain counted, a `data:text/html` frame ran script, CSS `content: "(155)"` showed a number the rule never saw. Recorded under Kerem's standing instruction of 2026-09-12 that the architecture changes by a dated decision.
**Replaces.** Nothing; it extends D-2026-09-12-13 and D-2026-09-12-19.
**Cited by.** `ARCHITECTURE.md` Data contracts (`content/emergency-numbers.json`), Invariants; `scripts/check.py` attribute collection, `check_country_blocks`, `check_numbers`, `is_script_url`.

## D-2026-09-12-19: `alt` joins the number rule
**What.** The country-block number rule of D-2026-09-12-13 reads `alt` values too: a screen reader or an images-off connection gets the alt text, so a number there is a number the reader gets.
**Evidence.** `/reviewer`, fresh loop pass 1, 2026-09-12, correctness finding 1: an icon's stale `alt="155'yi ara"` inside the TR block passed. Recorded under Kerem's standing instruction of 2026-09-12 that the architecture changes by a dated decision.
**Replaces.** Nothing; it extends D-2026-09-12-13.
**Cited by.** `ARCHITECTURE.md` Data contracts (`content/emergency-numbers.json`), Invariants; `scripts/check.py` `NUMBER_ATTRIBUTES`.

## D-2026-09-12-18: the country block is a Core type
**What.** The element `id="<CC>"` with class `country` on a withdrawal page, with its text, its links and its one suggestion note, is a Core type. In code it is `check.py` `Block`, passed whole to the country-block checks.
**Evidence.** `/reviewer` pass 3, 2026-09-12, conformance finding 5: the code carried the type without a row. Kerem, "yes to all".
**Replaces.** Nothing; it names what D-2026-09-12-11 describes.
**Cited by.** `ARCHITECTURE.md` Core types; `scripts/check.py` `Block`.

## D-2026-09-12-17: the proof's definitions made exact
**What.** Page text is the HTML with tags removed, where block-level tags become a break and inline tags nothing, entities unescaped, whitespace collapsed. `number` in `emergency-numbers.json` is digits only. A `content/` file is Markdown or JSON. A manifest `commit` is the full 40-character hash unless the row is authored here. `tests/test_check.py` may import the whole Python stdlib.
**Evidence.** `/reviewer` pass 3, 2026-09-12: conformance findings 1 to 3 (rows lagging the code), correctness findings 6 and 8 (`1-1-2` could never match, a `.txt` copy would fail as JSON). Kerem, "yes to all".
**Replaces.** Nothing; it sharpens the Data contracts wording.
**Cited by.** `ARCHITECTURE.md` Data contracts (the page text paragraph, the manifest row, the numbers row), Boundaries (`tests/test_check.py`); `scripts/check.py`.

## D-2026-09-12-16: the stylesheet rules the check looks for
**What.** In `style.css`, at top level and outside any `@media`, a rule whose selector list contains `.suggestion-note` sets `display: none` and is the last such rule; a rule whose list contains `.country:target .suggestion-note`, as descendant or `>` child, sets a display other than `none`. Grouped selectors are ordinary CSS and accepted.
**Evidence.** `/reviewer` pass 3, 2026-09-12: correctness finding 2 (a hide rule inside `@media (min-width: 600px)` counted as global, so phones showed every note) and finding 5 (grouped selectors were a false FAIL). Kerem, "yes to all".
**Replaces.** Nothing; it sharpens D-2026-09-12-11's stylesheet clause.
**Cited by.** `ARCHITECTURE.md` Data contracts (the suggested country), Invariants ("The suggestion is never the answer"); `scripts/check.py` `check_stylesheet`.

## D-2026-09-12-15: `rendered_in` names built pages only
**What.** The `rendered_in` cell of a manifest row lists pages that exist; it is `-` until the first is built, and the PR that builds a page fills it. A page named there that does not exist is a FAIL, never a SKIP.
**Evidence.** `/reviewer` pass 3, 2026-09-12, correctness finding 7: a typo in the cell read as "not built yet" and the Turkish text would have shipped unverified. Kerem, "yes to all".
**Replaces.** Nothing; it amends the SKIP clause of D-2026-09-12-12.
**Cited by.** `ARCHITECTURE.md` Data contracts (`content/MANIFEST.md`), Proof strategy; `content/MANIFEST.md`; `scripts/check.py` `check_copies`.

## D-2026-09-12-14: every element is closed explicitly
**What.** Pages omit no optional end tag: `</p>`, `</li>`, `</td>`, `</body>`, `</html>` are all written. The check fails a block tag opening inside an open `<p>`, an `<li>` opening inside an open `<li>`, an end tag that skips open elements, and any element still open at the end of the file. The parser therefore needs no browser-style implied closing.
**Evidence.** `/reviewer` pass 3, 2026-09-12, correctness finding 4: with implied closing absent, `<li>` blocks without `</li>` merged (false FAIL) and `<p id="TR">112<p class="suggestion-note">` passed while the browser put the note outside the block. Chosen over implementing implied closing in the parser (more code, more to get wrong). Kerem, "yes to all".
**Replaces.** Nothing.
**Cited by.** `CLAUDE.md` rules; `ARCHITECTURE.md` Invariants ("Every element is closed explicitly"); `scripts/check.py` `PageParser`.

## D-2026-09-12-13: the number rule covers attributes
**What.** Inside a country block, every run of two or more digits in the text and in every `href`, `aria-label` and `title` value equals the row's `number`, and a `tel:` link is exactly `tel:<number>`.
**Evidence.** `/reviewer` pass 3, 2026-09-12, correctness finding 1: a block showing 112 with a call button `href="tel:155"` passed, and the reader dials the button. Kerem, "yes to all".
**Replaces.** Nothing; it extends D-2026-09-12-11's number clause.
**Cited by.** `ARCHITECTURE.md` Data contracts (`content/emergency-numbers.json`), Invariants ("Every emergency number on a page comes from the table"); `scripts/check.py` `check_country_blocks`.

## D-2026-09-12-12: the manifest names the pages that render a copy
**What.** `content/MANIFEST.md` has one row per file with `file`, `repo`, `commit`, `path`, `copied_on` and `rendered_in`: the pages that render the copy, space-separated, `-` while none exists. `check.py` takes the page list from the row; a listed page that does not exist yet prints SKIP, and a row whose file the script does not know is impossible by construction. The rest of D-2026-09-12-8 stands: byte-identical copies, no header inside the file, verification against the local checkout when present.
**Evidence.** `/reviewer` on Phase 1a, 2026-09-12 (correctness finding 6): the script mapped four hard-coded file names to pages, so a fifth copied file would have had no copies check and no SKIP line, a green proof over an unverified text. Kerem, 2026-09-12: "update the docs so there are no contradictions for the reviewers; architecture changes by a decision".
**Replaces.** D-2026-09-12-8.
**Cited by.** `ARCHITECTURE.md` Boundaries (`content/`), Data contracts (`content/MANIFEST.md`), Core types (Copied text); `content/MANIFEST.md`; `scripts/check.py` `CopiedText`.

## D-2026-09-12-11: the country suggestion, restated so the check can prove it
**What.** As D-2026-09-12-10, with these made exact. The country code is the uppercase ISO 3166-1 alpha-2 code (`EU` for the 112 zone) in all three places that must agree: the `country` field of `content/emergency-numbers.json`, the `id` of the country block on the page, and the redirect target `?c=<CC>#<CC>` in `docs/cloudflare-rules.md` and the dashboard (`ip.src.country` is uppercase, so a future dynamic rule needs no case change). Each country block holds exactly one `.suggestion-note` element (the "likely yours" mark and its VPN warning) and one pick link `?c=<CC>#<CC>`; the number in the block is the only run of two or more digits in it. `style.css` hides `.suggestion-note` by default and shows it under `.country:target .suggestion-note`; the check looks for both selectors and fails when the stylesheet is missing once the JSON exists. The request allowlist is `nepsis.day` alone, no `www`. Everything else in D-2026-09-12-10 stands: the redirect rules, the fallback to the full table, the two ⏳ dashboard confirmations.
**Evidence.** `/reviewer` on Phase 1a, 2026-09-12: conformance findings 1 to 6 and correctness findings 1, 2, 7 showed the D-10 wording could be read two ways on case and on scope (page or block), and the "marked by anything but `:target`" clause could not be checked mechanically. Kerem, 2026-09-12: update the docs so there are no contradictions, by decision.
**Replaces.** D-2026-09-12-10.
**Cited by.** `ARCHITECTURE.md` Boundaries (the country redirect), Data contracts (`content/emergency-numbers.json`, the suggested country), Invariants ("Nothing collected", "The suggestion is never the answer"); `scripts/check.py` `check_country_blocks`; `docs/cloudflare-rules.md` and `style.css` when written.

## D-2026-09-12-10: the country suggestion is a redirect and a CSS target
**What.** `/withdrawal` and `/tr/withdrawal` suggest the reader's country. A Cloudflare Single Redirect per country group (TR, US, GB, the EU 112 zone; Free plan allows 10) matches `ip.src.country` on a request whose query has no `c=` and redirects to the same path with `?c=<cc>#<cc>`. The page marks the row `id="<cc>"` through CSS `:target` as "likely yours" and shows, in the same mark, the warning: "We guessed this from your connection. A VPN, a roaming SIM or a proxy can make it wrong: check the country before you call." (Turkish ⏳, Kerem's review.) Every country row stays on the page; a link `?c=<cc>#<cc>` inside each row lets the reader pick another, and the rule never fires on a request that already has `c=`. The rules live as text in `docs/cloudflare-rules.md`; Kerem creates them in the dashboard.
**Evidence.** Kerem, 2026-09-12: "Withdrawal page can detect the country from the IP and suggest a number. However should warn it may not be exact due to VPN and other possible issues." Cloudflare docs, read 2026-09-12: Single Redirects on Free, 10 rules; `ip.src.country` and `http.request.uri.query` are expression fields; Pages serves nested `404.html`. Rejected: a Pages Function or Worker reading `request.cf.country` (server-side code, the line D-2026-09-12-5 drew); a script calling a geolocation API (needs JavaScript and sends the reader's address to a third party, on a page that promises to collect nothing). ⏳ two things the docs do not state: that the geolocation field is allowed in redirect expressions on Free, and that the dashboard accepts a `#fragment` in a static target. If either fails, the fallback is no suggestion: the page is the full table, which it is anyway; a path per country is not an option (pages multiply by language).
**Replaces.** Nothing; it adds to Phase 2 without touching D-2026-09-12-4 (no script) or the no-server rule.
**Cited by.** `ARCHITECTURE.md` Boundaries (the country redirect), Data contracts (the suggested country), Invariants ("The suggestion is never the answer"); `docs/cloudflare-rules.md` and the `:target` rule in `style.css` (when written).

## D-2026-09-12-9: the emergency-number table is authored here
**What.** `content/emergency-numbers.json` (one row per country: `country`, `number`, `source` URL, `checked_on`) is written in this repo, starting with TR 112, US 911, UK 999 and EU 112. It is the one text `content/` holds that is not a copy from the app repo; the app's `MODEL.md` table copies from it when the app's P3 lands. Every row cites its source because a wrong number is the worst bug the site can have.
**Evidence.** Kerem's call in the `/architect` interview, 2026-09-12, over waiting for the app's table (app `PROJECT.md` line 172, ⏳ P3) and over prose without a table.
**Replaces.** Nothing; it carves the exception out of `PROJECT.md` design decision 4.
**Cited by.** `ARCHITECTURE.md` Boundaries (`content/`) and Data contracts; `content/emergency-numbers.json` (when written, via its manifest row).

## D-2026-09-12-8: byte-identical copies, provenance in a manifest
**What.** A file in `content/` is an exact copy of its source; `content/MANIFEST.md` carries one row per file with `file`, `repo`, `commit`, `path`, `copied_on`. No `SOURCE:` header inside the copied file. `check.py` verifies each row against the local app checkout when it is present.
**Evidence.** Kerem's call in the `/architect` interview, 2026-09-12. `PROJECT.md` "done" requires `PRIVACY.md` byte-identical to the app's copy, which a header breaks, and JSON cannot carry a comment at all. Chosen over a header in every file and over dropping `content/` for a commit comment in the page.
**Replaces.** Nothing as a decision; it settles the `SOURCE` header wording `ARCHITECTURE.md` and `CLAUDE.md` carried from the web template (the template still says header: a `/init-project` follow-up, not this repo's).
**Cited by.** `ARCHITECTURE.md` Boundaries (`content/`), Data contracts (`content/MANIFEST.md`), Core types (Copied text); `CLAUDE.md`; `scripts/check.py` (when written).

## D-2026-09-12-7: the check script is Phase 1 work
**What.** `scripts/check.py` (stdlib only) is written before the first page and is the proof every PR names: every page parses, no `<script>`, every copied text appears in its page, every twin resolves, every `content/` file matches its manifest row, no request leaves the site's origin. It runs by hand before every push and inside `/reviewer`; no GitHub Action.
**Evidence.** Kerem's call in the `/architect` interview, 2026-09-12, over a GitHub Action and over keeping it parked (BACKLOG row 5, "the second content update"). `ARCHITECTURE.md` rested every proof on a script that did not exist.
**Replaces.** Nothing; BACKLOG row 5 is promoted and closed by it.
**Cited by.** `ARCHITECTURE.md` Purpose, Boundaries, Proof strategy; `scripts/check.py` module docstring (when written).

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
