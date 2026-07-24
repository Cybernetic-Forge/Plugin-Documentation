from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self.links.append(href)


def target_path(site_dir: Path, source: Path, href: str) -> Path | None:
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc or href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None

    source_route = "/" + source.relative_to(site_dir).as_posix()
    resolved = urlparse(urljoin(f"https://docs.invalid{source_route}", href))
    route = unquote(resolved.path).lstrip("/")
    candidate = site_dir / route

    if resolved.path.endswith("/"):
        return candidate / "index.html"
    if candidate.is_dir():
        return candidate / "index.html"
    return candidate


def validate(site_dir: Path) -> list[str]:
    failures: list[str] = []
    for page in sorted(site_dir.rglob("*.html")):
        parser = LinkParser()
        parser.feed(page.read_text(encoding="utf-8"))
        for href in parser.links:
            target = target_path(site_dir, page, href)
            if target is not None and not target.exists():
                relative_page = page.relative_to(site_dir).as_posix()
                failures.append(f"{relative_page} -> {href} ({target.relative_to(site_dir).as_posix()})")
    return failures


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate internal links in a built MkDocs site.")
    parser.add_argument("site_dir", nargs="?", default="site", type=Path)
    args = parser.parse_args()

    site_dir = args.site_dir.resolve()
    if not site_dir.is_dir():
        raise SystemExit(f"Site directory does not exist: {site_dir}")

    failures = validate(site_dir)
    if failures:
        print("Broken internal links:")
        for failure in failures:
            print(f"  - {failure}")
        raise SystemExit(1)

    page_count = sum(1 for _ in site_dir.rglob("*.html"))
    print(f"Validated {page_count} HTML pages: all internal links resolve.")


if __name__ == "__main__":
    main()
