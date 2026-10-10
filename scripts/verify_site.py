"""Check local links in the standalone artifact site."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from build_index import load_catalog, render

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "docs" / "artifact"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.anchors: set[str] = set()
        self.inline_styles = 0
        self.stylesheets = 0
        self.standalone = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "meta" and values.get("name") == "artifact-format":
            self.standalone = values.get("content") == "standalone"
        if tag == "style" or "style" in values:
            self.inline_styles += 1
        if tag == "link" and values.get("rel") == "stylesheet":
            self.stylesheets += 1
        for name in ("href", "src"):
            if values.get(name):
                self.links.append(values[name])
        for name in ("id", "name"):
            if values.get(name):
                self.anchors.add(values[name])


def parse(page: Path) -> PageParser:
    parser = PageParser()
    parser.feed(page.read_text(encoding="utf-8"))
    return parser


def main() -> None:
    pages = {page.resolve(): parse(page) for page in SITE.rglob("*.html")}
    failures: list[str] = []

    if (SITE / "index.html").read_text(encoding="utf-8") != render(load_catalog()):
        failures.append("index.html: stale catalog; run python3 scripts/build_index.py")

    for page, document in pages.items():
        if document.standalone and not document.inline_styles:
            failures.append(f"{page.relative_to(SITE)}: standalone artifact needs inline CSS")
        if document.inline_styles and not document.standalone:
            failures.append(f"{page.relative_to(SITE)}: CSS must be in a separate stylesheet")
        if not document.stylesheets and not document.standalone:
            failures.append(f"{page.relative_to(SITE)}: missing stylesheet link")
        for link in document.links:
            url = urlsplit(link)
            if url.scheme or url.netloc or link.startswith("//"):
                continue
            target = (page.parent / unquote(url.path)).resolve() if url.path else page
            if not target.is_relative_to(SITE.resolve()) or not target.is_file():
                failures.append(f"{page.relative_to(SITE)}: missing local target {link}")
                continue
            fragment = unquote(url.fragment)
            if fragment and target.suffix == ".html":
                target_document = pages.get(target)
                if target_document is None or fragment not in target_document.anchors:
                    failures.append(f"{page.relative_to(SITE)}: missing fragment {link}")

    if failures:
        raise SystemExit("\n".join(failures))
    print(f"Checked {len(pages)} HTML guides and their local links")


if __name__ == "__main__":
    main()
