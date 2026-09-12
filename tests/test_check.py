"""Plants every fault scripts/check.py must catch in a temporary site and expects the FAIL line."""

from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check  # noqa: E402

SOURCE_REPO = "kdemirtas/nepsis"
PRIVACY_MD = (
    "# Privacy\n\nYour data lives on your phone.\n\n"
    "- **A log** of every message, so you can see it.\n"
)
WITHDRAWAL_JSON = {
    "version": 1,
    "reviewedBy": None,
    "sources": [{"name": "NICE CG100", "url": "https://nice.org.uk"}],
    "timeline": [
        {
            "fromHours": 6,
            "toHours": 12,
            "title": "Early symptoms",
            "symptoms": ["Anxiety", "Shaking"],
        }
    ],
    "erNow": ["A seizure"],
    "highRisk": "Higher risk if you had one before.",
    "closing": "Call now.",
}
NUMBERS = [
    {
        "country": "TR",
        "number": "112",
        "source": "https://example.org/tr",
        "checked_on": "2026-09-12",
    },
    {
        "country": "US",
        "number": "911",
        "source": "https://example.org/us",
        "checked_on": "2026-09-12",
    },
]
STYLE = (
    ".suggestion-note { display: none; }\n.country:target .suggestion-note { display: block; }\n"
)
RULES = "TR -> https://nepsis.day/withdrawal?c=TR#TR\nUS -> https://nepsis.day/withdrawal?c=US#US\n"


def html_page(lang: str, hreflang: str, twin_href: str, body: str) -> str:
    return (
        f'<!doctype html><html lang="{lang}"><head><title>t</title>'
        '<link rel="stylesheet" href="/style.css">'
        f'<link rel="alternate" hreflang="{hreflang}" href="{twin_href}"></head>'
        f"<body>{body}</body></html>"
    )


def country_block(code: str, name: str, number: str) -> str:
    return (
        f'<section id="{code}" class="country"><h2>{name}</h2><p class="big">{number}</p>'
        f'<a href="tel:{number}">Call</a>'
        '<p class="suggestion-note">We guessed this from your connection.</p>'
        f'<a href="?c={code}#{code}">Pick</a></section>'
    )


PRIVACY_BODY = (
    "<h1>Privacy</h1><p>Your data lives on your phone.</p>"
    "<ul><li><strong>A log</strong> of every message, so you can see it.</li></ul>"
)
WITHDRAWAL_BODY = (
    "<h1>Early symptoms</h1><p>Anxiety<br>Shaking</p><p>A seizure</p>"
    "<p>Higher risk if you had one before.</p>"
    "<p>Call now.</p><p>Source: <abbr>NICE CG100</abbr></p>"
    + country_block("TR", "Türkiye", "112")
    + country_block("US", "United States", "911")
)


class SiteBuilder:
    """A temporary site plus a temporary git repo standing in for the app checkout."""

    def __init__(self, root: Path):
        self.root = root
        self.source = root / "source-repo"
        self.source.mkdir()
        (self.source / "sources").mkdir()
        (self.source / "PRIVACY.md").write_text(PRIVACY_MD, encoding="utf-8")
        (self.source / "sources/withdrawal-en.json").write_text(
            json.dumps(WITHDRAWAL_JSON), encoding="utf-8"
        )
        for command in (
            ["init", "-q"],
            ["add", "-A"],
            ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "s"],
        ):
            subprocess.run(
                ["git", "-C", str(self.source)] + command, check=True, capture_output=True
            )
        self.commit = subprocess.run(
            ["git", "-C", str(self.source), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    def write(self, relative_path: str, text: str) -> None:
        target = self.root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def clean_site(self) -> None:
        self.write("index.html", html_page("en", "tr", "/tr/", "<h1>Nepsis</h1>"))
        self.write("tr/index.html", html_page("tr", "en", "https://nepsis.day/", "<h1>Nepsis</h1>"))
        self.write("privacy.html", html_page("en", "tr", "/tr/privacy", PRIVACY_BODY))
        self.write("STATUS.md", "- ⏳ tr/privacy.html: the app's Turkish pass\n")
        self.write("withdrawal.html", html_page("en", "tr", "/tr/withdrawal", WITHDRAWAL_BODY))
        self.write("tr/withdrawal.html", html_page("tr", "en", "/withdrawal", WITHDRAWAL_BODY))
        self.write("style.css", STYLE)
        self.write("docs/cloudflare-rules.md", RULES)
        self.write("content/PRIVACY.md", PRIVACY_MD)
        self.write("content/withdrawal-en.json", json.dumps(WITHDRAWAL_JSON))
        self.write("content/emergency-numbers.json", json.dumps(NUMBERS))
        self.write("content/MANIFEST.md", self.manifest())

    def manifest(self, extra_rows: str = "") -> str:
        return (
            "| file | repo | commit | path | copied_on | rendered_in |\n|---|---|---|---|---|---|\n"
            f"| `PRIVACY.md` | `{SOURCE_REPO}` | `{self.commit}` | `PRIVACY.md` "
            "| 2026-09-12 | `privacy.html` |\n"
            f"| `withdrawal-en.json` | `{SOURCE_REPO}` | `{self.commit}` "
            "| `sources/withdrawal-en.json` | 2026-09-12 | `withdrawal.html tr/withdrawal.html` |\n"
            "| `emergency-numbers.json` | `kdemirtas/nepsis-day` | `-` "
            "| `content/emergency-numbers.json` | 2026-09-12 "
            "| `withdrawal.html tr/withdrawal.html` |\n" + extra_rows
        )

    def run(self) -> tuple[int, str]:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = check.Checker(self.root, {SOURCE_REPO: self.source}).run()
        return exit_code, buffer.getvalue()


FAULTS = [
    (
        "script tag",
        lambda site: site.write(
            "index.html", html_page("en", "tr", "/tr/", '<script src="/a.js"></script>')
        ),
        "<script> tag",
    ),
    (
        "inline handler",
        lambda site: site.write(
            "index.html", html_page("en", "tr", "/tr/", '<a href="#" onclick="t()">x</a>')
        ),
        "onclick attribute",
    ),
    (
        "javascript url",
        lambda site: site.write(
            "index.html", html_page("en", "tr", "/tr/", '<a href="JavaScript:void(0)">x</a>')
        ),
        "javascript: URL",
    ),
    (
        "foreign img",
        lambda site: site.write(
            "index.html", html_page("en", "tr", "/tr/", '<img src="HTTPS://cdn.example/x.png">')
        ),
        "fetches outside the allowlist: HTTPS://cdn.example/x.png",
    ),
    (
        "foreign srcset",
        lambda site: site.write(
            "index.html",
            html_page(
                "en",
                "tr",
                "/tr/",
                '<img src="/a.png" srcset="/a.png 1x, https://cdn.example/b.png 2x">',
            ),
        ),
        "fetches outside the allowlist: https://cdn.example/b.png",
    ),
    (
        "foreign formaction",
        lambda site: site.write(
            "index.html",
            html_page(
                "en",
                "tr",
                "/tr/",
                '<form><button formaction="https://buttondown.email/x">go</button></form>',
            ),
        ),
        "fetches outside the allowlist: https://buttondown.email/x",
    ),
    (
        "foreign style block",
        lambda site: site.write(
            "index.html",
            html_page(
                "en",
                "tr",
                "/tr/",
                '<style>@import url("https://fonts.googleapis.com/css2");</style>',
            ),
        ),
        "fetches outside the allowlist: https://fonts.googleapis.com/css2",
    ),
    (
        "foreign style attribute",
        lambda site: site.write(
            "index.html",
            html_page(
                "en", "tr", "/tr/", '<p style="background:url(//tracker.example/p.gif)">x</p>'
            ),
        ),
        "fetches outside the allowlist: //tracker.example/p.gif",
    ),
    (
        "www is not own host",
        lambda site: site.write(
            "index.html", html_page("en", "tr", "/tr/", '<img src="https://www.nepsis.day/x.png">')
        ),
        "fetches outside the allowlist",
    ),
    (
        "missing twin",
        lambda site: (site.root / "tr/index.html").unlink(),
        "index.html: twin tr/index.html missing",
    ),
    (
        "absent hreflang on index twin",
        lambda site: site.write("tr/index.html", "<html><head></head><body>x</body></html>"),
        "tr/index.html: hreflang 'en' is '', expected /",
    ),
    (
        "self hreflang",
        lambda site: site.write(
            "tr/withdrawal.html", html_page("tr", "en", "/tr/withdrawal", WITHDRAWAL_BODY)
        ),
        "tr/withdrawal.html: hreflang 'en' is '/tr/withdrawal', expected /withdrawal",
    ),
    (
        "wrong hreflang",
        lambda site: site.write(
            "withdrawal.html", html_page("en", "tr", "/about", WITHDRAWAL_BODY)
        ),
        "withdrawal.html: hreflang 'tr' is '/about', expected /tr/withdrawal",
    ),
    (
        "unlisted content file",
        lambda site: site.write("content/stray.txt", "x"),
        "stray.txt: in content/ but has no manifest row",
    ),
    (
        "row without file",
        lambda site: site.write(
            "content/MANIFEST.md",
            site.manifest(
                f"| `TERMS.md` | `kdemirtas/nepsis` | `{'a' * 40}` | `TERMS.md` "
                "| 2026-09-12 | - |\n"
            ),
        ),
        "TERMS.md: manifest row but no file",
    ),
    (
        "malformed manifest line",
        lambda site: site.write("content/MANIFEST.md", site.manifest("| `x` | `y` |\n")),
        "MANIFEST.md line 6: 2 cells, expected 6",
    ),
    (
        "tampered copy",
        lambda site: site.write("content/PRIVACY.md", PRIVACY_MD.replace("phone", "laptop")),
        "PRIVACY.md: differs from kdemirtas/nepsis@",
    ),
    (
        "unknown commit",
        lambda site: site.write(
            "content/MANIFEST.md", site.manifest().replace(site.commit, "0" * 40)
        ),
        "PRIVACY.md: 0000000:PRIVACY.md not found",
    ),
    (
        "dropped paragraph",
        lambda site: site.write(
            "privacy.html", html_page("en", "tr", "/tr/privacy", "<h1>Privacy</h1>")
        ),
        "PRIVACY.md: 2 string(s) absent from privacy.html",
    ),
    (
        "bad json copy",
        lambda site: (
            site.write("content/withdrawal-en.json", "{oops"),
            site.write("content/MANIFEST.md", site.manifest().replace(site.commit, "0" * 40)),
        ),
        "withdrawal-en.json: cannot read",
    ),
    (
        "number without source",
        lambda site: site.write(
            "content/emergency-numbers.json",
            json.dumps([dict(NUMBERS[0], source="")] + NUMBERS[1:]),
        ),
        "TR: no source URL",
    ),
    (
        "lowercase country code",
        lambda site: site.write(
            "content/emergency-numbers.json",
            json.dumps([dict(NUMBERS[0], country="tr")] + NUMBERS[1:]),
        ),
        "tr: country code is not uppercase",
    ),
    (
        "extra json field",
        lambda site: site.write(
            "content/emergency-numbers.json", json.dumps([dict(NUMBERS[0], note="x")] + NUMBERS[1:])
        ),
        "emergency-numbers.json: cannot read",
    ),
    (
        "wrong number beside country",
        lambda site: site.write(
            "withdrawal.html",
            html_page(
                "en",
                "tr",
                "/tr/withdrawal",
                WITHDRAWAL_BODY.replace('<p class="big">112</p>', '<p class="big">155</p>'),
            ),
        ),
        "TR block shows ['112', '155'], table says 112",
    ),
    (
        "second number in block",
        lambda site: site.write(
            "withdrawal.html",
            html_page(
                "en",
                "tr",
                "/tr/withdrawal",
                WITHDRAWAL_BODY.replace('<p class="big">112</p>', '<p class="big">112 or 155</p>'),
            ),
        ),
        "TR block shows ['112', '155'], table says 112",
    ),
    (
        "lowercase anchor",
        lambda site: site.write(
            "withdrawal.html",
            html_page("en", "tr", "/tr/withdrawal", WITHDRAWAL_BODY.replace('id="TR"', 'id="tr"')),
        ),
        "no element id=TR",
    ),
    (
        "note outside block",
        lambda site: site.write(
            "withdrawal.html",
            html_page(
                "en",
                "tr",
                "/tr/withdrawal",
                WITHDRAWAL_BODY.replace(
                    '<p class="suggestion-note">We guessed this from your connection.</p>'
                    '<a href="?c=TR#TR">',
                    '<a href="?c=TR#TR">',
                )
                + '<p class="suggestion-note">footer note</p>',
            ),
        ),
        "TR block has 0 .suggestion-note, expected 1",
    ),
    (
        "pick link outside block",
        lambda site: site.write(
            "withdrawal.html",
            html_page(
                "en",
                "tr",
                "/tr/withdrawal",
                WITHDRAWAL_BODY.replace('<a href="?c=US#US">Pick</a>', "")
                + '<a href="?c=US#US">Pick</a>',
            ),
        ),
        "US block has no pick link ?c=US#US",
    ),
    (
        "block without country class",
        lambda site: site.write(
            "withdrawal.html",
            html_page(
                "en",
                "tr",
                "/tr/withdrawal",
                WITHDRAWAL_BODY.replace('id="US" class="country"', 'id="US"'),
            ),
        ),
        "US block lacks class country",
    ),
    (
        "rules doc misses a country",
        lambda site: site.write("docs/cloudflare-rules.md", RULES.splitlines()[0]),
        "docs/cloudflare-rules.md has no target for US",
    ),
    (
        "stylesheet without target rule",
        lambda site: site.write("style.css", ".country {}"),
        "style.css must hide .suggestion-note",
    ),
    (
        "stylesheet missing",
        lambda site: (site.root / "style.css").unlink(),
        "style.css missing while emergency-numbers.json exists",
    ),
    (
        "foreign url in style.css",
        lambda site: site.write(
            "style.css", STYLE + "body { background: url(//tracker.example/p.gif) }"
        ),
        "style.css: fetches outside the allowlist: //tracker.example/p.gif",
    ),
    (
        "foreign import in style.css",
        lambda site: site.write(
            "style.css", '@import url("https://fonts.googleapis.com/css2");' + STYLE
        ),
        "style.css: fetches outside the allowlist: https://fonts.googleapis.com/css2",
    ),
    (
        "base href to another host",
        lambda site: site.write(
            "index.html", html_page("en", "tr", "/tr/", '<base href="https://nepsis.pages.dev/">')
        ),
        "fetches outside the allowlist: https://nepsis.pages.dev/",
    ),
    (
        "meta refresh to another host",
        lambda site: site.write(
            "index.html",
            html_page(
                "en",
                "tr",
                "/tr/",
                '<meta http-equiv="refresh" content="0; url=https://elsewhere.example">',
            ),
        ),
        "fetches outside the allowlist: https://elsewhere.example",
    ),
    (
        "ping attribute",
        lambda site: site.write(
            "index.html",
            html_page("en", "tr", "/tr/", '<a href="/x" ping="https://tracker.example/ping">x</a>'),
        ),
        "fetches outside the allowlist: https://tracker.example/ping",
    ),
    (
        "srcdoc iframe",
        lambda site: site.write(
            "index.html",
            html_page(
                "en", "tr", "/tr/", '<iframe srcdoc="&lt;script&gt;x()&lt;/script&gt;"></iframe>'
            ),
        ),
        "srcdoc attribute",
    ),
    (
        "alternate link to another host",
        lambda site: site.write(
            "index.html",
            html_page(
                "en",
                "tr",
                "/tr/",
                '<link rel="alternate" type="application/rss+xml" href="https://feeds.example/x">',
            ),
        ),
        "fetches outside the allowlist: https://feeds.example/x",
    ),
    (
        "duplicate country id",
        lambda site: site.write(
            "withdrawal.html",
            html_page(
                "en",
                "tr",
                "/tr/withdrawal",
                country_block("TR", "Türkiye", "155") + WITHDRAWAL_BODY,
            ),
        ),
        "withdrawal.html: duplicate id=TR",
    ),
    (
        "number split by br",
        lambda site: site.write(
            "withdrawal.html",
            html_page(
                "en",
                "tr",
                "/tr/withdrawal",
                WITHDRAWAL_BODY.replace('<p class="big">112</p>', '<p class="big">1<br>12</p>'),
            ),
        ),
        "TR block shows ['112', '12'], table says 112",
    ),
    (
        "hide rule only in a comment",
        lambda site: site.write(
            "style.css",
            "/* .suggestion-note { display: none; } */\n"
            ".country:target .suggestion-note { display: block; }",
        ),
        "style.css must hide .suggestion-note",
    ),
    (
        "hide rule overridden later",
        lambda site: site.write("style.css", STYLE + ".suggestion-note { display: block; }"),
        "style.css must hide .suggestion-note",
    ),
    (
        "show rule with none important",
        lambda site: site.write(
            "style.css",
            ".suggestion-note { display: none; }\n"
            ".country:target .suggestion-note { display: none !important; }",
        ),
        "style.css must hide .suggestion-note",
    ),
    (
        "empty commit cell",
        lambda site: site.write(
            "content/MANIFEST.md",
            site.manifest().replace(f"`{site.commit}` | `PRIVACY.md`", "`` | `PRIVACY.md`"),
        ),
        "PRIVACY.md: commit '' is not a full 40-character hash",
    ),
    (
        "symbolic commit cell",
        lambda site: site.write(
            "content/MANIFEST.md",
            site.manifest().replace(f"`{site.commit}` | `PRIVACY.md`", "`HEAD` | `PRIVACY.md`"),
        ),
        "PRIVACY.md: commit 'HEAD' is not a full 40-character hash",
    ),
    (
        "pending row names a different file",
        lambda site: (
            (site.root / "privacy.html").unlink(),
            site.write("tr/privacy.html", html_page("tr", "en", "/privacy", PRIVACY_BODY)),
        ),
        "tr/privacy.html: twin privacy.html missing",
    ),
    (
        "manifest missing",
        lambda site: (site.root / "content/MANIFEST.md").unlink(),
        "content/MANIFEST.md missing",
    ),
    (
        "page that is not utf-8",
        lambda site: (site.root / "index.html").write_bytes(b"<html>\xff\xfe</html>"),
        "index.html: does not parse",
    ),
    (
        "content entry that is a directory",
        lambda site: (
            (site.root / "content/PRIVACY.md").unlink(),
            (site.root / "content/PRIVACY.md").mkdir(),
        ),
        "PRIVACY.md: not a regular file",
    ),
    (
        "tel link dials another number",
        lambda site: site.write(
            "withdrawal.html",
            html_page(
                "en",
                "tr",
                "/tr/withdrawal",
                WITHDRAWAL_BODY.replace(
                    '<p class="big">112</p>', '<p class="big">112</p><a href="tel:155">Call</a>'
                ),
            ),
        ),
        "TR block shows ['112', '155'], table says 112",
    ),
    (
        "aria-label carries another number",
        lambda site: site.write(
            "withdrawal.html",
            html_page(
                "en",
                "tr",
                "/tr/withdrawal",
                WITHDRAWAL_BODY.replace(
                    '<p class="big">112</p>', '<p class="big" aria-label="Call 155">112</p>'
                ),
            ),
        ),
        "TR block shows ['112', '155'], table says 112",
    ),
    (
        "tel link with formatting dials right digits but not exactly",
        lambda site: site.write(
            "withdrawal.html",
            html_page(
                "en",
                "tr",
                "/tr/withdrawal",
                WITHDRAWAL_BODY.replace(
                    '<p class="big">112</p>', '<p class="big">112</p><a href="tel:+90112">Call</a>'
                ),
            ),
        ),
        "TR block shows ['112', '90112'], table says 112",
    ),
    (
        "hide rule only inside a media query",
        lambda site: site.write(
            "style.css",
            "@media (min-width: 600px) { .suggestion-note { display: none; } }\n"
            ".country:target .suggestion-note { display: block; }",
        ),
        "style.css must hide .suggestion-note",
    ),
    (
        "hide rule only for print at the end",
        lambda site: site.write(
            "style.css",
            ".suggestion-note { display: block; }\n"
            ".country:target .suggestion-note { display: block; }\n"
            "@media print { .suggestion-note { display: none; } }",
        ),
        "style.css must hide .suggestion-note",
    ),
    (
        "svg use fetches from another host",
        lambda site: site.write(
            "index.html",
            html_page(
                "en", "tr", "/tr/", '<svg><use href="https://cdn.example/sprite.svg#w"></use></svg>'
            ),
        ),
        "fetches outside the allowlist: https://cdn.example/sprite.svg#w",
    ),
    (
        "xlink href javascript",
        lambda site: site.write(
            "index.html",
            html_page("en", "tr", "/tr/", '<svg><a xlink:href="javascript:t()">x</a></svg>'),
        ),
        "javascript: URL",
    ),
    (
        "javascript in meta refresh",
        lambda site: site.write(
            "index.html",
            html_page(
                "en", "tr", "/tr/", '<meta http-equiv="refresh" content="0;url=javascript:t()">'
            ),
        ),
        "javascript: URL",
    ),
    (
        "image-set in style.css",
        lambda site: site.write(
            "style.css", STYLE + 'body { background: image-set("https://cdn.example/bg.png" 1x) }'
        ),
        "style.css: fetches outside the allowlist: https://cdn.example/bg.png",
    ),
    (
        "block tag inside an open p",
        lambda site: site.write("index.html", html_page("en", "tr", "/tr/", "<p>one<p>two</p>")),
        "unclosed <p> before <p>",
    ),
    (
        "li without end tag",
        lambda site: site.write(
            "index.html", html_page("en", "tr", "/tr/", "<ul><li>one<li>two</li></ul>")
        ),
        "unclosed <li> before <li>",
    ),
    (
        "end tag skipping an open element",
        lambda site: site.write("index.html", html_page("en", "tr", "/tr/", "<div><span>x</div>")),
        "unclosed <span> inside </div>",
    ),
    (
        "stray end tag",
        lambda site: site.write("index.html", html_page("en", "tr", "/tr/", "x</span>")),
        "stray </span>",
    ),
    (
        "element open at end of file",
        lambda site: site.write("index.html", '<html lang="en"><head></head><body><p>x</p>'),
        "unclosed <html> at end of file",
    ),
    (
        "rendered_in names a page that does not exist",
        lambda site: site.write(
            "content/MANIFEST.md", site.manifest().replace("`privacy.html`", "`privcy.html`")
        ),
        "PRIVACY.md: rendered_in names privcy.html, which does not exist",
    ),
    (
        "number with separators",
        lambda site: site.write(
            "content/emergency-numbers.json",
            json.dumps([dict(NUMBERS[0], number="1-1-2")] + NUMBERS[1:]),
        ),
        "TR: number '1-1-2' is not digits only",
    ),
    (
        "content file of another type",
        lambda site: (
            site.write("content/never-say.txt", "x"),
            site.write(
                "content/MANIFEST.md",
                site.manifest(
                    "| `never-say.txt` | `kdemirtas/nepsis-day` | `-` | `never-say.txt` "
                    "| 2026-09-12 | `index.html` |\n"
                ),
            ),
        ),
        "never-say.txt: unsupported type, Markdown or JSON only",
    ),
    (
        "alt text carries another number",
        lambda site: site.write(
            "withdrawal.html",
            html_page(
                "en",
                "tr",
                "/tr/withdrawal",
                WITHDRAWAL_BODY.replace(
                    '<p class="big">112</p>',
                    '<p class="big">112</p><img src="/i.svg" alt="155 ara">',
                ),
            ),
        ),
        "TR block shows ['112', '155'], table says 112",
    ),
    (
        "tel link with an extension",
        lambda site: site.write(
            "withdrawal.html",
            html_page(
                "en",
                "tr",
                "/tr/withdrawal",
                WITHDRAWAL_BODY.replace(
                    '<p class="big">112</p>',
                    '<p class="big">112</p><a href="tel:112;ext=9">Call</a>',
                ),
            ),
        ),
        "TR block dials tel:112;ext=9, table says 112",
    ),
    (
        "empty numbers table",
        lambda site: site.write("content/emergency-numbers.json", "[]"),
        "emergency-numbers.json: no rows, nothing to check",
    ),
    (
        "last display declaration wins",
        lambda site: site.write(
            "style.css",
            ".suggestion-note { display: none; display: block; }\n"
            ".country:target .suggestion-note { display: block; }",
        ),
        "style.css must hide .suggestion-note",
    ),
    (
        "show rule with uppercase none",
        lambda site: site.write(
            "style.css",
            ".suggestion-note { display: none; }\n"
            ".country:target .suggestion-note { display: NONE; }",
        ),
        "style.css must hide .suggestion-note",
    ),
    (
        "javascript with an embedded newline",
        lambda site: site.write(
            "index.html", html_page("en", "tr", "/tr/", '<a href="java&#10;script:alert(1)">x</a>')
        ),
        "javascript: URL",
    ),
    (
        "javascript in a style block url",
        lambda site: site.write(
            "index.html",
            html_page("en", "tr", "/tr/", "<style>body{background:url(javascript:t())}</style>"),
        ),
        "javascript: URL",
    ),
    (
        "javascript in style.css",
        lambda site: site.write("style.css", STYLE + '@import url("javascript:t()");'),
        "style.css: javascript: URL",
    ),
    (
        "source name starting with http is still required",
        lambda site: (
            site.write(
                "content/withdrawal-en.json",
                json.dumps(
                    dict(WITHDRAWAL_JSON, sources=[{"name": "http guidance", "url": "https://x"}])
                ),
            ),
            site.write("content/MANIFEST.md", site.manifest().replace(site.commit, "0" * 40)),
        ),
        "withdrawal-en.json: 1 string(s) absent from withdrawal.html, first: 'http guidance'",
    ),
    (
        "country block without a table row",
        lambda site: site.write(
            "withdrawal.html",
            html_page(
                "en", "tr", "/tr/withdrawal", WITHDRAWAL_BODY + country_block("GB", "UK", "999")
            ),
        ),
        "block id=GB has no row in emergency-numbers.json",
    ),
    (
        "page with country blocks outside rendered_in",
        lambda site: site.write(
            "content/MANIFEST.md",
            site.manifest().replace(
                "| `content/emergency-numbers.json` | 2026-09-12 "
                "| `withdrawal.html tr/withdrawal.html` |",
                "| `content/emergency-numbers.json` | 2026-09-12 | `withdrawal.html` |",
            ),
        ),
        "tr/withdrawal.html has country blocks but is not in rendered_in",
    ),
    (
        "country blocks with no table at all",
        lambda site: (
            (site.root / "content/emergency-numbers.json").unlink(),
            site.write(
                "content/MANIFEST.md",
                "\n".join(line for line in site.manifest().splitlines() if "emergency" not in line)
                + "\n",
            ),
        ),
        "withdrawal.html has country blocks but no table",
    ),
    (
        "pick link to another host",
        lambda site: site.write(
            "withdrawal.html",
            html_page(
                "en",
                "tr",
                "/tr/withdrawal",
                WITHDRAWAL_BODY.replace(
                    '<a href="?c=TR#TR">', '<a href="https://nepsis.pages.dev/withdrawal?c=TR#TR">'
                ),
            ),
        ),
        "TR block has no pick link ?c=TR#TR",
    ),
    (
        "pick link to the other language",
        lambda site: site.write(
            "withdrawal.html",
            html_page(
                "en",
                "tr",
                "/tr/withdrawal",
                WITHDRAWAL_BODY.replace('<a href="?c=TR#TR">', '<a href="/tr/withdrawal?c=TR#TR">'),
            ),
        ),
        "TR block has no pick link ?c=TR#TR",
    ),
    (
        "brace inside a css string hides a later override",
        lambda site: site.write(
            "style.css",
            STYLE + '.big::after { content: "}"; }\n.suggestion-note { display: block; }',
        ),
        "style.css must hide .suggestion-note",
    ),
    (
        "data text html frame",
        lambda site: site.write(
            "index.html",
            html_page(
                "en", "tr", "/tr/", '<iframe src="data:text/html,<script>x()</script>"></iframe>'
            ),
        ),
        "javascript: URL",
    ),
    (
        "vbscript link",
        lambda site: site.write(
            "index.html", html_page("en", "tr", "/tr/", '<a href="vbscript:x">x</a>')
        ),
        "javascript: URL",
    ),
    (
        "css content writes a number",
        lambda site: site.write("style.css", STYLE + '#TR .big::after { content: " (155)"; }'),
        "style.css writes 155 through a content: rule",
    ),
    (
        "input value carries another number",
        lambda site: site.write(
            "withdrawal.html",
            html_page(
                "en",
                "tr",
                "/tr/withdrawal",
                WITHDRAWAL_BODY.replace(
                    '<p class="big">112</p>', '<p class="big">112</p><input value="155" readonly>'
                ),
            ),
        ),
        "TR block shows ['112', '155'], table says 112",
    ),
    (
        "title attribute carries another number",
        lambda site: site.write(
            "withdrawal.html",
            html_page(
                "en",
                "tr",
                "/tr/withdrawal",
                WITHDRAWAL_BODY.replace(
                    '<p class="big">112</p>', '<p class="big" title="155">112</p>'
                ),
            ),
        ),
        "TR block shows ['112', '155'], table says 112",
    ),
    (
        "number as a json integer",
        lambda site: site.write(
            "content/emergency-numbers.json",
            json.dumps([dict(NUMBERS[0], number=112)] + NUMBERS[1:]),
        ),
        "emergency-numbers.json: cannot read",
    ),
    (
        "foreign poster",
        lambda site: site.write(
            "index.html",
            html_page("en", "tr", "/tr/", '<video poster="https://cdn.example/p.jpg"></video>'),
        ),
        "fetches outside the allowlist: https://cdn.example/p.jpg",
    ),
    (
        "foreign object data",
        lambda site: site.write(
            "index.html",
            html_page("en", "tr", "/tr/", '<object data="https://cdn.example/o.svg"></object>'),
        ),
        "fetches outside the allowlist: https://cdn.example/o.svg",
    ),
    (
        "foreign form action",
        lambda site: site.write(
            "index.html",
            html_page("en", "tr", "/tr/", '<form action="https://buttondown.email/x"></form>'),
        ),
        "fetches outside the allowlist: https://buttondown.email/x",
    ),
    (
        "foreign svg image href",
        lambda site: site.write(
            "index.html",
            html_page(
                "en", "tr", "/tr/", '<svg><image href="https://cdn.example/i.png"></image></svg>'
            ),
        ),
        "fetches outside the allowlist: https://cdn.example/i.png",
    ),
    (
        "javascript in a style attribute url",
        lambda site: site.write(
            "index.html",
            html_page("en", "tr", "/tr/", '<p style="background:url(javascript:t())">x</p>'),
        ),
        "javascript: URL",
    ),
]


class CheckTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.site = SiteBuilder(Path(self.temp.name))
        self.site.clean_site()

    def tearDown(self):
        self.temp.cleanup()

    def test_clean_site_passes(self):
        exit_code, output = self.site.run()
        self.assertEqual(exit_code, 0, output)
        self.assertNotIn("FAIL", output)
        self.assertIn(
            "twins     privacy.html: twin tr/privacy.html missing, ⏳ row in STATUS.md names it",
            output,
        )
        self.assertIn("PASS numbers   withdrawal.html: every country block", output)

    def test_bare_tree_skips_not_silence(self):
        for path in list(self.site.root.glob("*.html")) + list(self.site.root.glob("tr/*.html")):
            path.unlink()
        (self.site.root / "style.css").unlink()
        (self.site.root / "content/emergency-numbers.json").unlink()
        manifest = self.site.manifest()
        for cell in ("`privacy.html`", "`withdrawal.html tr/withdrawal.html`"):
            manifest = manifest.replace(cell, "-")
        manifest = "\n".join(line for line in manifest.splitlines() if "emergency" not in line)
        self.site.write("content/MANIFEST.md", manifest + "\n")
        exit_code, output = self.site.run()
        self.assertEqual(exit_code, 0, output)
        for expected in (
            "SKIP pages     no page built yet",
            "SKIP pages     style.css not written yet",
            "SKIP twins     no page built yet",
            "SKIP copies    PRIVACY.md: no rendering page yet",
            "SKIP numbers   content/emergency-numbers.json not written yet",
        ):
            self.assertIn(expected, output)

    def test_numbers_without_rendering_page_skips(self):
        (self.site.root / "withdrawal.html").unlink()
        (self.site.root / "tr/withdrawal.html").unlink()
        manifest = self.site.manifest().replace(
            "| `withdrawal.html tr/withdrawal.html` |\n", "| - |\n"
        )
        self.site.write("content/MANIFEST.md", manifest)
        exit_code, output = self.site.run()
        self.assertEqual(exit_code, 0, output)
        self.assertIn("SKIP numbers   emergency-numbers.json: no rendering page yet", output)
        self.assertIn("SKIP copies    withdrawal-en.json: no rendering page yet", output)

    def test_grouped_selectors_and_alignment_separator_pass(self):
        self.site.write(
            "style.css",
            ".suggestion-note,\n.pending-note { display: none; }\n"
            ".country:target > .suggestion-note { display: block; }\n",
        )
        self.site.write(
            "content/MANIFEST.md",
            self.site.manifest().replace(
                "|---|---|---|---|---|---|", "|:---|:---|:---|:---|:---|:---|"
            ),
        )
        exit_code, output = self.site.run()
        self.assertEqual(exit_code, 0, output)

    def test_each_fault_fails(self):
        for name, plant, expected in FAULTS:
            with self.subTest(fault=name):
                self.tearDown()
                self.setUp()
                plant(self.site)
                exit_code, output = self.site.run()
                self.assertEqual(exit_code, 1, output)
                self.assertIn(expected, output)
                self.assertNotIn("Traceback", output)

    def test_crash_becomes_fail_line(self):
        checker = check.Checker(self.site.root, {SOURCE_REPO: self.site.source})
        checker.check_twins = lambda: 1 / 0
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = checker.run()
        self.assertEqual(exit_code, 1)
        self.assertIn("FAIL twins     crashed: ZeroDivisionError", buffer.getvalue())
        self.assertNotIn("Traceback", buffer.getvalue())

    def test_git_absent_and_no_checkout_skip(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            no_checkout_exit = check.Checker(self.site.root, {}).run()
        self.assertEqual(no_checkout_exit, 0)
        self.assertIn(
            "SKIP manifest  PRIVACY.md: no local checkout of kdemirtas/nepsis", buffer.getvalue()
        )
        original_run = check.subprocess.run

        def missing_git(*args, **kwargs):
            raise FileNotFoundError("git")

        check.subprocess.run = missing_git
        try:
            exit_code, output = self.site.run()
        finally:
            check.subprocess.run = original_run
        self.assertEqual(exit_code, 0, output)
        self.assertIn("SKIP manifest  PRIVACY.md: git not installed", output)

    def test_hreflang_case_and_region_pass(self):
        self.site.write("withdrawal.html", html_page("en", "TR", "/tr/withdrawal", WITHDRAWAL_BODY))
        self.site.write(
            "tr/withdrawal.html", html_page("tr", "en-US", "/withdrawal", WITHDRAWAL_BODY)
        )
        exit_code, output = self.site.run()
        self.assertEqual(exit_code, 0, output)

    def test_valid_markup_variants_pass(self):
        self.site.write(
            "index.html",
            html_page(
                "en",
                "tr",
                "/tr/",
                '<p>Call <svg aria-hidden="true"><title>Phone</title>'
                '<use href="/assets/i.svg#phone"></use></svg> now.</p>'
                "<style>/* url(https://fonts.gstatic.com/x.woff2) rejected */</style>",
            ),
        )
        self.site.write(
            "style.css",
            ".suggestion-note { DISPLAY: none; }\n"
            ".country:target .suggestion-note { display: block; }",
        )
        manifest = self.site.manifest().replace(
            "`withdrawal.html tr/withdrawal.html`", "`withdrawal.html` `tr/withdrawal.html`"
        )
        self.site.write("content/MANIFEST.md", manifest)
        exit_code, output = self.site.run()
        self.assertEqual(exit_code, 0, output)

    def test_empty_manifest_skips(self):
        for path in (self.site.root / "content").iterdir():
            if path.name != "MANIFEST.md":
                path.unlink()
        self.site.write("content/MANIFEST.md", self.site.manifest().split("\n|---")[0] + "\n")
        for path in list(self.site.root.glob("*.html")) + list(self.site.root.glob("tr/*.html")):
            path.unlink()
        exit_code, output = self.site.run()
        self.assertEqual(exit_code, 0, output)
        self.assertIn("SKIP manifest  no content copied yet", output)
        self.assertIn("SKIP copies    no content copied yet", output)


if __name__ == "__main__":
    unittest.main()
