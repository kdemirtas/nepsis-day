# nepsis-day

The public face of Nepsis (the recovery companion app, private repo `kdemirtas/nepsis`): what it is, the privacy policy the Play listing needs, and one page for someone alone in alcohol withdrawal tonight. Hand-written HTML and CSS, English and Turkish, served by Cloudflare Pages from this public repo.

## Layout

    HANDOVER.md        resume pointer, read this first
    STATUS.md          dated log
    PROJECT.md         spec
    ARCHITECTURE.md    shape of the work, proof strategy
    CLAUDE.md          working rules
    docs/              longer reference docs the spec links
    sources/           reference material, catalogued in `sources/SOURCES.md`

## How to preview and deploy

    python3 -m http.server 8080        # from the repo root, then http://localhost:8080/
    python3 scripts/check.py           # planned: the proof (parse, diff copied text, no <script>)
    GH_TOKEN=$(gh auth token --user kdemirtas) git push   # Cloudflare Pages deploys main, no build step
