#!/usr/bin/env python3
"""The proof of nepsis-day (D-2026-09-12-7): stdlib only, exit 1 on any FAIL, never a traceback.

Checks, in the order they print:
  pages      every page parses, carries no <script> tag, on* attribute or javascript: URL, and
             fetches from its own origin only (attributes and CSS alike)
  twins      every root page has its tr/ twin (or a ⏳ row in STATUS.md names it) and each page's
             hreflang link is the twin's served path, root-relative or absolute on nepsis.day
  manifest   every content/ file has a row in content/MANIFEST.md and every row a file; a copied
             file equals `git show <commit>:<path>` in the local source checkout when present
  copies     every string of a copied text occurs in each page its manifest row names
  numbers    every row of emergency-numbers.json has a source and, on each rendering page, a
             country block whose only number is that row's, with one suggestion note and one pick
             link; the rules doc and the stylesheet carry their side (D-2026-09-12-11)
A check whose subject does not exist yet prints SKIP. `python3 -m unittest discover tests` plants
every fault this file must catch.
"""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

LANGUAGE_DIRS = ("tr",)
OWN_HOSTS = {"nepsis.day"}
SOURCE_CHECKOUTS = {"kdemirtas/nepsis": Path.home() / "code/personal/mobile-app/nepsis"}
THIS_REPO = "kdemirtas/nepsis-day"
NUMBERS_FILE = "emergency-numbers.json"
SUGGESTION_NOTE_CLASS = "suggestion-note"
COUNTRY_BLOCK_CLASS = "country"
URL_ATTRIBUTES = {"src", "poster", "data", "action", "formaction", "href", "ping", "xlink:href"}
HREF_FETCHING_TAGS = {"link", "base", "use", "image"}
STRUCTURAL_ATTRIBUTES = {"id", "class", "lang", "dir", "role", "rel", "type", "style", "hreflang"}
SCRIPT_SCHEMES = ("javascript:", "vbscript:", "data:text/html")
FULL_COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
SEPARATOR_CELL_PATTERN = re.compile(r"^:?-+:?$")
META_REFRESH_PATTERN = re.compile(r"^\s*\d+\s*;\s*url\s*=\s*['\"]?([^'\"\s]+)", re.I)
CSS_COMMENT_PATTERN = re.compile(r"/\*.*?\*/", re.S)
VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}
BLOCK_TAGS = {
    "p",
    "li",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "div",
    "section",
    "article",
    "aside",
    "header",
    "footer",
    "nav",
    "main",
    "blockquote",
    "ul",
    "ol",
    "dl",
    "dt",
    "dd",
    "td",
    "th",
    "tr",
    "br",
    "hr",
    "figcaption",
    "summary",
    "details",
    "html",
    "head",
    "body",
    "address",
    "pre",
}
CSS_URL_PATTERN = re.compile(
    r"""(?:url|src)\(\s*['"]?([^'")\s]+)|@import\s+['"]([^'"]+)|image-set\(\s*['"]([^'"]+)""", re.I
)
HOST_PATTERN = re.compile(r"^\s*(?:[a-z][a-z0-9+.\-]*:)?//([^/?#]+)", re.I)


@dataclass
class Block:
    """An element with an id and everything rendered inside it: Country block, D-2026-09-12-18."""

    element_id: str
    own_classes: set[str]
    text_parts: list[str] = field(default_factory=list)
    link_targets: list[str] = field(default_factory=list)
    attribute_values: list[str] = field(default_factory=list)
    note_count: int = 0

    @property
    def text(self) -> str:
        return normalise("".join(self.text_parts))

    @property
    def digit_runs(self) -> set[str]:
        """Every run of two or more digits a reader could see or dial inside the block."""
        return set(re.findall(r"\d{2,}", " ".join([self.text] + self.attribute_values)))

    @property
    def tel_links(self) -> list[str]:
        return [link for link in self.link_targets if link.strip().lower().startswith("tel:")]


@dataclass
class Page:
    """One HTML file, one language, one path (ARCHITECTURE.md Core types)."""

    relative_path: str
    text: str = ""
    script_faults: list[str] = field(default_factory=list)
    foreign_fetches: list[str] = field(default_factory=list)
    hreflang_targets: dict[str, str] = field(default_factory=dict)
    blocks: dict[str, Block] = field(default_factory=dict)
    duplicate_ids: list[str] = field(default_factory=list)
    parse_error: str = ""

    def country_blocks(self) -> list[Block]:
        return [block for block in self.blocks.values() if COUNTRY_BLOCK_CLASS in block.own_classes]

    @property
    def language(self) -> str:
        first_dir = self.relative_path.split("/")[0]
        return first_dir if first_dir in LANGUAGE_DIRS else "en"

    @property
    def twin_path(self) -> str:
        file_name = self.relative_path.split("/")[-1]
        return file_name if self.language != "en" else f"{LANGUAGE_DIRS[0]}/{file_name}"

    @property
    def served_path(self) -> str:
        path = "/" + self.relative_path.removesuffix(".html")
        return path.removesuffix("index") if path.endswith("/index") else path


@dataclass
class ManifestRow:
    file: str
    repo: str
    commit: str
    path: str
    copied_on: str
    rendered_in: list[str]


@dataclass
class CopiedText:
    """A content/ file plus its manifest row (ARCHITECTURE.md Core types, D-2026-09-12-12)."""

    row: ManifestRow
    local_file: Path


@dataclass
class EmergencyNumber:
    country: str
    number: str
    source: str
    checked_on: str


class PageParser(HTMLParser):
    def __init__(self, page: Page):
        super().__init__(convert_charrefs=True)
        self.page = page
        self.text_parts: list[str] = []
        self.open_elements: list[tuple[str, Block | None]] = []
        self.inside_style = False

    def open_blocks(self) -> list[Block]:
        return [block for _, block in self.open_elements if block is not None]

    def open_tags(self) -> list[str]:
        return [open_tag for open_tag, _ in self.open_elements]

    def note_implied_close(self, tag: str) -> None:
        """D-2026-09-12-14: a tag a browser would close for us is a fault here."""
        if tag in BLOCK_TAGS and tag not in VOID_TAGS and "p" in self.open_tags():
            self.page.script_faults.append(f"unclosed <p> before <{tag}>")
        if tag == "li":
            enclosing = [
                open_tag for open_tag in self.open_tags() if open_tag in ("li", "ul", "ol")
            ]
            if enclosing and enclosing[-1] == "li":
                self.page.script_faults.append("unclosed <li> before <li>")

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name.lower(): (value or "") for name, value in attrs}
        classes = set(attributes.get("class", "").split())
        self.note_implied_close(tag)
        if tag in BLOCK_TAGS:
            self.break_text()
        if tag == "script":
            self.page.script_faults.append("<script> tag")
        if "srcdoc" in attributes:
            self.page.script_faults.append(
                "srcdoc attribute, an inline document the check cannot read"
            )
        if tag == "style":
            self.inside_style = True
        if (
            tag == "link"
            and attributes.get("rel", "").lower() == "alternate"
            and "hreflang" in attributes
        ):
            language = attributes["hreflang"].lower().split("-")[0]
            self.page.hreflang_targets[language] = attributes.get("href", "")
        fetches = self.fetch_candidates(tag, attributes)
        self.note_scripts_in(attributes, fetches + [attributes.get("href", "")])
        self.page.foreign_fetches += [url for url in fetches if is_foreign(url)]
        block = Block(attributes["id"], classes) if "id" in attributes else None
        if block is not None and block.element_id in self.page.blocks:
            self.page.duplicate_ids.append(block.element_id)
            block = None
        elif block is not None:
            self.page.blocks[block.element_id] = block
        for open_block in self.open_blocks() + ([block] if block else []):
            if tag == "a" and "href" in attributes:
                open_block.link_targets.append(attributes["href"])
            if SUGGESTION_NOTE_CLASS in classes:
                open_block.note_count += 1
            open_block.attribute_values += [
                value for name, value in attributes.items() if name not in STRUCTURAL_ATTRIBUTES
            ]  # D-2026-09-12-13, D-2026-09-12-19, D-2026-09-12-20
        if tag not in VOID_TAGS:
            self.open_elements.append((tag, block))

    def note_scripts_in(self, attributes: dict[str, str], urls: list[str]) -> None:
        for name in attributes:
            if name.startswith("on"):
                self.page.script_faults.append(f"{name} attribute")
        for url in urls:
            if is_script_url(url):
                self.page.script_faults.append(f"javascript: URL in {url.strip()[:40]!r}")

    def fetch_candidates(self, tag: str, attributes: dict[str, str]) -> list[str]:
        """Every URL the browser would fetch for this tag (a plain <a href> is a navigation)."""
        candidates = [
            value for name, value in attributes.items() if name in URL_ATTRIBUTES - {"href", "ping"}
        ]
        candidates += attributes.get("ping", "").split()
        if tag in HREF_FETCHING_TAGS:
            candidates.append(attributes.get("href", ""))
        if tag == "meta" and attributes.get("http-equiv", "").lower() == "refresh":
            refresh = META_REFRESH_PATTERN.match(attributes.get("content", ""))
            candidates.append(refresh.group(1) if refresh else "")
        candidates += [
            candidate.split()[0]
            for candidate in attributes.get("srcset", "").split(",")
            if candidate.split()
        ]
        candidates += css_urls(attributes.get("style", ""))
        return candidates

    def break_text(self) -> None:
        """A block boundary: text on either side never joins into one word or number."""
        self.text_parts.append("\n")
        for block in self.open_blocks():
            block.text_parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in BLOCK_TAGS:
            self.break_text()
        if tag == "style":
            self.inside_style = False
        if tag in VOID_TAGS:
            return
        for index in range(len(self.open_elements) - 1, -1, -1):
            if self.open_elements[index][0] == tag:
                for skipped, _ in self.open_elements[index + 1 :]:
                    self.page.script_faults.append(f"unclosed <{skipped}> inside </{tag}>")
                del self.open_elements[index:]
                return
        self.page.script_faults.append(f"stray </{tag}>")

    def close(self) -> None:
        super().close()
        for open_tag, _ in self.open_elements:
            self.page.script_faults.append(f"unclosed <{open_tag}> at end of file")

    def handle_data(self, data: str) -> None:
        if self.inside_style:
            urls = css_urls(CSS_COMMENT_PATTERN.sub("", data))
            self.page.foreign_fetches += [url for url in urls if is_foreign(url)]
            self.note_scripts_in({}, urls)
            return
        self.text_parts.append(data)
        for block in self.open_blocks():
            block.text_parts.append(data)


def is_script_url(url: str) -> bool:
    """A script-bearing scheme, after the whitespace a browser drops inside a scheme."""
    return re.sub(r"\s", "", url).lower().startswith(SCRIPT_SCHEMES)


def css_urls(css_text: str) -> list[str]:
    return [
        next(group for group in groups if group) for groups in CSS_URL_PATTERN.findall(css_text)
    ]


def top_level_css_rules(css_text: str) -> list[tuple[str, str]]:
    """(selector, body) for every rule at depth 0; at-rules and what nests in them are skipped."""
    rules, depth, selector, body, quote = [], 0, "", "", ""
    for character in css_text:
        if quote:
            if character == quote:
                quote = ""
        elif character in "'\"":
            quote = character
        elif character == "{":
            depth += 1
            if depth == 1:
                body = ""
                continue
        elif character == "}":
            depth = max(depth - 1, 0)
            if depth == 0:
                if not selector.strip().startswith("@"):
                    rules.append((selector.strip(), body))
                selector = ""
                continue
        if depth == 0:
            selector += character
        elif depth == 1:
            body += character
    return rules


def selector_list(selector: str) -> set[str]:
    return {
        re.sub(r"\s*>\s*", " > ", re.sub(r"\s+", " ", part.strip())) for part in selector.split(",")
    }


def is_foreign(url: str) -> bool:
    match = HOST_PATTERN.match(url)
    return bool(match) and match.group(1).lower() not in OWN_HOSTS


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def markdown_blocks(markdown: str) -> list[str]:
    """Headings, paragraphs and list items of a Markdown file as plain text."""
    blocks = []
    for line in markdown.splitlines():
        line = re.sub(r"^\s*(#{1,6}\s+|[-*]\s+|\d+\.\s+)", "", line)
        line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
        line = re.sub(r"(\*\*|__|`)", "", line)
        if normalise(line):
            blocks.append(normalise(line))
    return blocks


def string_leaves(value) -> list[str]:
    if isinstance(value, str):
        return [normalise(value)] if normalise(value) else []
    if isinstance(value, dict):
        return [leaf for key, item in value.items() if key != "url" for leaf in string_leaves(item)]
    if isinstance(value, list):
        return [leaf for item in value for leaf in string_leaves(item)]
    return []


def source_strings(copied_text: CopiedText) -> list[str]:
    """Every string the rendering page must contain (D-2026-09-12-17); ValueError if unreadable."""
    try:
        raw = copied_text.local_file.read_text(encoding="utf-8")
        if copied_text.local_file.suffix == ".md":
            return markdown_blocks(raw)
        if copied_text.local_file.suffix != ".json":
            raise ValueError(f"{copied_text.row.file}: unsupported type, Markdown or JSON only")
        return string_leaves(json.loads(raw))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{copied_text.row.file}: cannot read: {error}") from error


class Report:
    def __init__(self):
        self.failures = 0
        self.lines: list[str] = []

    def result(self, check: str, status: str, detail: str) -> None:
        if status == "FAIL":
            self.failures += 1
        line = f"{status:<4} {check:<9} {detail}"
        self.lines.append(line)
        print(line)


class Checker:
    """Runs every check against one site root; the test points it at a temporary site."""

    def __init__(self, root: Path, source_checkouts: dict[str, Path] | None = None):
        self.root = root
        self.source_checkouts = SOURCE_CHECKOUTS if source_checkouts is None else source_checkouts
        self.report = Report()
        self.pages: dict[str, Page] = {}
        self.copies: list[CopiedText] = []

    def run(self) -> int:
        for name in ("pages", "twins", "manifest", "copies", "numbers"):
            try:
                getattr(self, f"check_{name}")()
            except Exception as error:  # a crash is a finding, not a traceback
                self.report.result(name, "FAIL", f"crashed: {error!r}")
        print(f"{'FAIL' if self.report.failures else 'OK'}: {self.report.failures} failure(s)")
        return 1 if self.report.failures else 0

    def parse_page(self, relative_path: str) -> Page:
        page = Page(relative_path)
        parser = PageParser(page)
        try:
            parser.feed((self.root / relative_path).read_text(encoding="utf-8"))
            parser.close()
        except (UnicodeDecodeError, AssertionError) as error:
            page.parse_error = str(error)
        page.text = normalise("".join(parser.text_parts))
        return page

    def check_pages(self) -> None:
        paths = sorted(self.root.glob("*.html"))
        for language_dir in LANGUAGE_DIRS:
            paths += sorted((self.root / language_dir).glob("*.html"))
        relative_paths = [str(path.relative_to(self.root)) for path in paths]
        self.pages = {relative: self.parse_page(relative) for relative in relative_paths}
        if not self.pages:
            self.report.result("pages", "SKIP", "no page built yet")
        for page in self.pages.values():
            faults = []
            if page.parse_error:
                faults.append(f"does not parse: {page.parse_error}")
            faults += page.script_faults
            faults += [f"duplicate id={element_id}" for element_id in page.duplicate_ids]
            faults += [f"fetches outside the allowlist: {url}" for url in page.foreign_fetches]
            for fault in faults:
                self.report.result("pages", "FAIL", f"{page.relative_path}: {fault}")
            if not faults:
                self.report.result(
                    "pages", "PASS", f"{page.relative_path}: parses, no script, own origin only"
                )
        self.check_stylesheet_fetches()

    def check_stylesheet_fetches(self) -> None:
        stylesheet = self.root / "style.css"
        if not stylesheet.exists():
            self.report.result("pages", "SKIP", "style.css not written yet")
            return
        urls = css_urls(self.read_css())
        foreign = [url for url in urls if is_foreign(url)]
        for url in foreign:
            self.report.result("pages", "FAIL", f"style.css: fetches outside the allowlist: {url}")
        for url in urls:
            if is_script_url(url):
                self.report.result("pages", "FAIL", f"style.css: javascript: URL in {url[:40]!r}")
        if not foreign:
            self.report.result("pages", "PASS", "style.css: own origin only")

    def read_css(self) -> str:
        return CSS_COMMENT_PATTERN.sub("", (self.root / "style.css").read_text(encoding="utf-8"))

    def pending_in_status(self, name: str) -> bool:
        status_file = self.root / "STATUS.md"
        if not status_file.exists():
            return False
        as_whole_token = re.compile(rf"(?<![\w/]){re.escape(name)}(?!\w)")
        return any(
            "⏳" in line and as_whole_token.search(line)
            for line in status_file.read_text(encoding="utf-8").splitlines()
        )

    def check_twins(self) -> None:
        if not self.pages:
            self.report.result("twins", "SKIP", "no page built yet")
        for page in self.pages.values():
            twin = self.pages.get(page.twin_path)
            if twin is None:
                pending = self.pending_in_status(page.twin_path)
                detail = f"{page.relative_path}: twin {page.twin_path} missing" + (
                    ", ⏳ row in STATUS.md names it" if pending else ""
                )
                self.report.result("twins", "PASS" if pending else "FAIL", detail)
                continue
            accepted = {twin.served_path} | {
                f"https://{host}{twin.served_path}" for host in OWN_HOSTS
            }
            target = page.hreflang_targets.get(twin.language, "")
            if target in accepted:
                self.report.result(
                    "twins",
                    "PASS",
                    f"{page.relative_path}: hreflang {twin.language!r} is {twin.served_path}",
                )
            else:
                self.report.result(
                    "twins",
                    "FAIL",
                    f"{page.relative_path}: hreflang {twin.language!r} is {target!r}, "
                    f"expected {twin.served_path}",
                )

    def read_manifest(self) -> list[ManifestRow]:
        rows = []
        for number, line in enumerate(
            (self.root / "content/MANIFEST.md").read_text(encoding="utf-8").splitlines(), 1
        ):
            if not line.strip().startswith("|"):
                continue
            cells = [cell.replace("`", "").strip() for cell in line.strip().strip("|").split("|")]
            if cells[0] == "file" or all(SEPARATOR_CELL_PATTERN.match(cell) for cell in cells):
                continue
            if len(cells) != 6:
                self.report.result(
                    "manifest", "FAIL", f"MANIFEST.md line {number}: {len(cells)} cells, expected 6"
                )
                continue
            rendered_in = [] if cells[5] in ("", "-") else cells[5].split()
            if cells[1] != THIS_REPO and not FULL_COMMIT_PATTERN.match(cells[2]):
                self.report.result(
                    "manifest",
                    "FAIL",
                    f"{cells[0]}: commit {cells[2]!r} is not a full 40-character hash",
                )
                continue
            rows.append(ManifestRow(*cells[:5], rendered_in))
        return rows

    def verify_copy(self, copied_text: CopiedText) -> None:
        row = copied_text.row
        if row.repo == THIS_REPO:
            self.report.result("manifest", "PASS", f"{row.file}: authored here, nothing to compare")
            return
        checkout = self.source_checkouts.get(row.repo)
        if checkout is None or not (checkout / ".git").exists():
            self.report.result(
                "manifest", "SKIP", f"{row.file}: no local checkout of {row.repo}, row unverified"
            )
            return
        try:
            shown = subprocess.run(
                ["git", "-C", str(checkout), "show", f"{row.commit}:{row.path}"],
                capture_output=True,
            )
        except FileNotFoundError:
            self.report.result("manifest", "SKIP", f"{row.file}: git not installed, row unverified")
            return
        if shown.returncode != 0:
            self.report.result(
                "manifest",
                "FAIL",
                f"{row.file}: {row.commit[:7]}:{row.path} not found in {checkout}",
            )
        elif shown.stdout != copied_text.local_file.read_bytes():
            self.report.result(
                "manifest",
                "FAIL",
                f"{row.file}: differs from {row.repo}@{row.commit[:7]} {row.path}",
            )
        else:
            self.report.result(
                "manifest",
                "PASS",
                f"{row.file}: byte-identical to {row.repo}@{row.commit[:7]} {row.path}",
            )

    def check_manifest(self) -> None:
        content_dir = self.root / "content"
        if not (content_dir / "MANIFEST.md").exists():
            self.report.result("manifest", "FAIL", "content/MANIFEST.md missing")
            return
        rows = self.read_manifest()
        files_present = {path.name for path in content_dir.iterdir() if path.name != "MANIFEST.md"}
        if not rows and not files_present:
            self.report.result("manifest", "SKIP", "no content copied yet")
        for unlisted in sorted(files_present - {row.file for row in rows}):
            self.report.result(
                "manifest", "FAIL", f"{unlisted}: in content/ but has no manifest row"
            )
        for row in rows:
            if row.file not in files_present:
                self.report.result("manifest", "FAIL", f"{row.file}: manifest row but no file")
                continue
            copied_text = CopiedText(row, content_dir / row.file)
            if not copied_text.local_file.is_file():
                self.report.result("manifest", "FAIL", f"{row.file}: not a regular file")
                continue
            self.copies.append(copied_text)
            self.verify_copy(copied_text)

    def check_copies(self) -> None:
        """Every string of a copy occurs in each page its rendered_in names (D-2026-09-12-15)."""
        if not self.copies:
            self.report.result("copies", "SKIP", "no content copied yet")
        for copied_text in self.copies:
            if copied_text.row.file == NUMBERS_FILE:
                continue
            if not copied_text.row.rendered_in:
                self.report.result(
                    "copies", "SKIP", f"{copied_text.row.file}: no rendering page yet"
                )
            for page_path in copied_text.row.rendered_in:
                page = self.pages.get(page_path)
                if page is None:
                    self.report.result(
                        "copies",
                        "FAIL",
                        f"{copied_text.row.file}: rendered_in names {page_path}, "
                        "which does not exist",
                    )
                    continue
                try:
                    missing = [
                        text for text in source_strings(copied_text) if text not in page.text
                    ]
                except ValueError as error:
                    self.report.result("copies", "FAIL", str(error))
                    continue
                if missing:
                    self.report.result(
                        "copies",
                        "FAIL",
                        f"{copied_text.row.file}: {len(missing)} string(s) absent from "
                        f"{page_path}, first: {missing[0][:70]!r}",
                    )
                else:
                    self.report.result(
                        "copies",
                        "PASS",
                        f"{copied_text.row.file}: every string occurs in {page_path}",
                    )

    def load_numbers(self, copied_text: CopiedText) -> list[EmergencyNumber]:
        rows = json.loads(copied_text.local_file.read_text(encoding="utf-8"))
        expected_keys = {"country", "number", "source", "checked_on"}
        if not isinstance(rows, list) or any(
            not isinstance(row, dict)
            or set(row) != expected_keys
            or not all(isinstance(value, str) for value in row.values())
            for row in rows
        ):
            raise ValueError(
                f"{NUMBERS_FILE}: expected a list of rows with exactly {sorted(expected_keys)}"
            )
        return [EmergencyNumber(**row) for row in rows]

    def check_numbers(self) -> None:
        numbers_copy = next((copy for copy in self.copies if copy.row.file == NUMBERS_FILE), None)
        if numbers_copy is None:
            self.report.result("numbers", "SKIP", f"content/{NUMBERS_FILE} not written yet")
            for page in self.pages.values():
                if page.country_blocks():
                    self.report.result(
                        "numbers", "FAIL", f"{page.relative_path} has country blocks but no table"
                    )
            return
        try:
            numbers = self.load_numbers(numbers_copy)
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as error:
            self.report.result("numbers", "FAIL", f"{NUMBERS_FILE}: cannot read: {error}")
            return
        if not numbers:
            self.report.result("numbers", "FAIL", f"{NUMBERS_FILE}: no rows, nothing to check")
            return
        for number in numbers:
            if not re.match(r"^https?://", number.source):
                self.report.result("numbers", "FAIL", f"{number.country}: no source URL")
            if number.country != number.country.upper():
                self.report.result(
                    "numbers", "FAIL", f"{number.country}: country code is not uppercase"
                )
            if not number.number.isdigit():
                self.report.result(
                    "numbers",
                    "FAIL",
                    f"{number.country}: number {number.number!r} is not digits only",
                )
        if not numbers_copy.row.rendered_in:
            self.report.result("numbers", "SKIP", f"{NUMBERS_FILE}: no rendering page yet")
        for page in self.pages.values():
            if page.country_blocks() and page.relative_path not in numbers_copy.row.rendered_in:
                self.report.result(
                    "numbers",
                    "FAIL",
                    f"{page.relative_path} has country blocks but is not in rendered_in",
                )
        for page_path in numbers_copy.row.rendered_in:
            page = self.pages.get(page_path)
            if page is None:
                self.report.result(
                    "numbers", "FAIL", f"rendered_in names {page_path}, which does not exist"
                )
                continue
            self.check_country_blocks(numbers, page)
        self.check_rules_doc(numbers)
        self.check_stylesheet()

    def check_country_blocks(self, numbers: list[EmergencyNumber], page: Page) -> None:
        """Number, note and pick link inside each block, text and attributes (D-2026-09-12-13)."""
        problems = []
        countries = {number.country for number in numbers}
        for block in page.country_blocks():
            if block.element_id not in countries:
                problems.append(f"block id={block.element_id} has no row in {NUMBERS_FILE}")
        for number in numbers:
            block = page.blocks.get(number.country)
            if block is None:
                problems.append(f"no element id={number.country}")
                continue
            if block.digit_runs != {number.number}:
                problems.append(
                    f"{number.country} block shows {sorted(block.digit_runs)}, "
                    f"table says {number.number}"
                )
            for tel_link in block.tel_links:
                if tel_link.strip().lower() != f"tel:{number.number}":
                    problems.append(
                        f"{number.country} block dials {tel_link}, table says {number.number}"
                    )
            if COUNTRY_BLOCK_CLASS not in block.own_classes:
                problems.append(f"{number.country} block lacks class {COUNTRY_BLOCK_CLASS}")
            if block.note_count != 1:
                problems.append(
                    f"{number.country} block has {block.note_count} "
                    f".{SUGGESTION_NOTE_CLASS}, expected 1"
                )
            pick = f"?c={number.country}#{number.country}"
            accepted_links = {pick, page.served_path + pick} | {
                f"https://{host}{page.served_path}{pick}" for host in OWN_HOSTS
            }
            if not any(link.strip() in accepted_links for link in block.link_targets):
                problems.append(
                    f"{number.country} block has no pick link ?c={number.country}#{number.country}"
                )
        for problem in problems:
            self.report.result("numbers", "FAIL", f"{page.relative_path}: {problem}")
        if not problems:
            self.report.result(
                "numbers",
                "PASS",
                f"{page.relative_path}: every country block has its number, note and pick link",
            )

    def check_rules_doc(self, numbers: list[EmergencyNumber]) -> None:
        rules_doc = self.root / "docs/cloudflare-rules.md"
        if not rules_doc.exists():
            self.report.result("numbers", "SKIP", "docs/cloudflare-rules.md not written yet")
            return
        rules_text = rules_doc.read_text(encoding="utf-8")
        missing = [
            number.country
            for number in numbers
            if f"?c={number.country}#{number.country}" not in rules_text
        ]
        if missing:
            self.report.result(
                "numbers",
                "FAIL",
                f"docs/cloudflare-rules.md has no target for {', '.join(missing)}",
            )
        else:
            self.report.result("numbers", "PASS", "docs/cloudflare-rules.md targets every country")

    def check_stylesheet(self) -> None:
        """The hide and show rules at top level, grouped selectors accepted (D-2026-09-12-16)."""
        stylesheet = self.root / "style.css"
        if not stylesheet.exists():
            self.report.result(
                "numbers", "FAIL", "style.css missing while emergency-numbers.json exists"
            )
            return
        css = self.read_css()
        note_displays = []
        target_displays = []
        note_selector = f".{SUGGESTION_NOTE_CLASS}"
        show_selectors = {
            f".{COUNTRY_BLOCK_CLASS}:target .{SUGGESTION_NOTE_CLASS}",
            f".{COUNTRY_BLOCK_CLASS}:target > .{SUGGESTION_NOTE_CLASS}",
        }
        for digits in re.findall(r"content\s*:[^;}]*?(\d{2,})", css, re.I):
            self.report.result(
                "numbers", "FAIL", f"style.css writes {digits} through a content: rule"
            )
        for selector, body in top_level_css_rules(css):
            displays = re.findall(r"display\s*:\s*([^;!]+)", body, re.I)
            value = displays[-1].strip().lower() if displays else None
            selectors = selector_list(selector)
            if note_selector in selectors:
                note_displays.append(value)
            if selectors & show_selectors:
                target_displays.append(value)
        hides = bool(note_displays) and note_displays[-1] == "none"
        shows = bool(target_displays) and target_displays[-1] not in (None, "none")
        if hides and shows:
            self.report.result(
                "numbers",
                "PASS",
                "style.css hides .suggestion-note and shows it under .country:target",
            )
        else:
            self.report.result(
                "numbers",
                "FAIL",
                "style.css must hide .suggestion-note and show it under "
                ".country:target .suggestion-note",
            )


def main() -> int:
    return Checker(Path(__file__).resolve().parent.parent).run()


if __name__ == "__main__":
    sys.exit(main())
