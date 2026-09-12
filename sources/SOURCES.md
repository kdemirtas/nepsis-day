# Sources: nepsis-day

Rule: never store URLs containing auth tokens or credentials; record sanitized references only
(repo@commit+path, workspace+object-id, sheet id).

| # | Source | Provenance | Retrieval | Fetched | Notes |
|---|--------|-----------|-----------|---------|-------|
| 1 | The app's privacy policy | `kdemirtas/nepsis` `PRIVACY.md` (private repo; local checkout `~/code/personal/mobile-app/nepsis/`), last updated 2026-09-10 | local copy at a named commit into `content/PRIVACY.md` | ⏳ | hosted verbatim at `/privacy`; Turkish ⏳ the app's Turkish pass |
| 2 | The app's withdrawal text | `kdemirtas/nepsis` `sources/withdrawal-en.json`, `withdrawal-tr.json`: 6 sources, 5 timeline bands, 8 ER criteria (NICE CG100, NHS, NIAAA 1998, SAMHSA TIP 45) | local copy at a named commit into `content/` | ⏳ | `/withdrawal`; Kerem reviews the Turkish before it ships |
| 3 | Lessons from the origin night | `kdemirtas/nepsis` `sources/origin-night-lessons.md`, items 3 (timeline countdown), 7 (medical card, triage sentence, bag list), 8 (reasons-not-to-go cards) | read in the app checkout; not copied | 2026-09-12 | the shape of `/withdrawal`; pattern level, no health record |
| 4 | Plain and warm design tokens | `kdemirtas/nepsis` `DESIGN.md` Visual direction (paper ground, coral, Manrope and Nunito, 22 dp corners; Emergency on a dark warm ground with one red) | read in the app checkout | 2026-09-12 | `style.css`; dp becomes px |
| 5 | Emergency numbers by country | ⏳ source to pick, shared with the app's `MODEL.md` table (Turkey 112, US 911 first) | web | ⏳ | `content/emergency-numbers.json`; a wrong number here is the worst bug the site can have, so the source is cited per row |
| 6 | Cloudflare Pages docs | developers.cloudflare.com: Pages from a GitHub repo, custom domains, no-build deploys; `serving-pages` (clean URLs, nested `404.html` resolved up the tree) | web | 2026-09-12 | Phase 1 setup |
| 7 | Cloudflare Single Redirects and rules fields | developers.cloudflare.com `rules/url-forwarding/` (Free plan: 10 rules, no regex), `single-redirects/settings/` (static and dynamic targets, preserve query string off by default), `ruleset-engine/rules-language/fields/reference/` (`ip.src.country`, `http.request.uri.query`) | web | 2026-09-12 | D-2026-09-12-10 and -11; ⏳ not stated in the docs: geolocation fields in redirect expressions on Free, `#fragment` accepted in a target |
