from __future__ import annotations

import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLUGINS_SRC = ROOT / "plugins"
DOCS_SOURCE = ROOT / "docs-source"
DOCS_DIR = ROOT / "docs"

FRONT_MATTER_RE = re.compile(r"^---\r?\n.*?\r?\n---\r?\n+", re.DOTALL)
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def strip_front_matter(text: str) -> str:
    return FRONT_MATTER_RE.sub("", text, count=1)


def plugin_title(plugin_dir: Path) -> str:
    readme = plugin_dir / "README.md"
    text = strip_front_matter(readme.read_text(encoding="utf-8"))
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return plugin_dir.name


def rewrite_links(text: str, plugin: str | None = None) -> str:
    def repl(match: re.Match[str]) -> str:
        label = match.group(1)
        url = match.group(2)
        if url.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)

        anchor = ""
        base = url
        if "#" in url:
          base, fragment = url.split("#", 1)
          anchor = f"#{fragment}"

        normalized = base.replace("\\", "/").strip().removeprefix("./")
        if normalized.endswith(".md"):
            normalized = normalized[:-3]

        if plugin:
            if normalized in ("README", "index", ""):
                return f"[{label}](./{anchor})" if anchor else f"[{label}](./)"
            if "/" not in normalized:
                return f"[{label}](./{normalized}/{anchor})" if anchor else f"[{label}](./{normalized}/)"

        if normalized.endswith("/README"):
            normalized = normalized[: -len("/README")]
        elif normalized == "README":
            normalized = "."

        if normalized == ".":
            return f"[{label}](./{anchor})" if anchor else f"[{label}](./)"
        if not normalized.startswith("/"):
            normalized = "/" + normalized
        return f"[{label}]({normalized}/{anchor})" if anchor and not normalized.endswith("/") else f"[{label}]({normalized}{anchor})"

    rewritten = MARKDOWN_LINK_RE.sub(repl, text)
    return rewritten.replace("](./api_information/)", "](./api_information/)")  # no-op for stable output


def write_page(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def build_home(plugin_dirs: list[Path]) -> str:
    template = (DOCS_SOURCE / "index.md").read_text(encoding="utf-8")
    blocks = []
    for directory in plugin_dirs:
        slug = directory.name
        title = plugin_title(directory)
        blocks.append(
            "\n".join(
                [
                    f"### [{title}](plugins/{slug}/index.md)",
                    "",
                    "| Section | Description |",
                    "| --- | --- |",
                    f"| [Overview](plugins/{slug}/index.md) | Start here for the {title} overview |",
                    f"| [Commands](plugins/{slug}/commands.md) | Command reference for {title} |",
                    f"| [Configuration](plugins/{slug}/configuration.md) | Config, tuning, and file structure for {title} |",
                    f"| [API Information](plugins/{slug}/api_information.md) | Integration and runtime notes for {title} |",
                ]
            )
        )
    return template.replace("{{PLUGIN_CATALOG}}", "\n\n".join(blocks))


def build_plugins_index(plugin_dirs: list[Path]) -> str:
    lines = [
        "# Plugins",
        "",
        "Browse the Cybernetic-Forge plugin catalog below.",
        "",
    ]
    for directory in plugin_dirs:
        slug = directory.name
        title = plugin_title(directory)
        lines.extend(
            [
                f"## [{title}]({slug}/index.md)",
                "",
                f"- [Overview]({slug}/index.md)",
                f"- [Commands]({slug}/commands.md)",
                f"- [Configuration]({slug}/configuration.md)",
                f"- [API Information]({slug}/api_information.md)",
                "",
            ]
        )
    return "\n".join(lines)


def build_assets() -> None:
    css = ROOT / "docs" / "assets" / "stylesheets" / "extra.css"
    css.parent.mkdir(parents=True, exist_ok=True)
    css.write_text(EXTRA_CSS.strip() + "\n", encoding="utf-8")


EXTRA_CSS = r"""
:root {
  --cf-accent: #00c8ff;
  --cf-accent-2: #61d3ff;
  --cf-accent-3: #6a7cff;
  --cf-dark: #071018;
  --cf-dark-soft: #0d1823;
  --cf-card: rgba(13, 24, 35, 0.82);
  --cf-light: #f4f8fc;
}

[data-md-color-scheme="slate"] {
  --md-default-bg-color: #071018;
  --md-default-bg-color--light: #0d1823;
  --md-default-bg-color--lighter: #132232;
  --md-default-fg-color: #ecf5ff;
  --md-default-fg-color--light: #9eb0c2;
  --md-primary-fg-color: #071018;
  --md-accent-fg-color: var(--cf-accent);
}

[data-md-color-scheme="default"] {
  --md-primary-fg-color: #12314c;
  --md-accent-fg-color: #007cc2;
}

.md-header {
  background:
    linear-gradient(90deg, rgba(0, 200, 255, 0.16), rgba(106, 124, 255, 0.16)),
    linear-gradient(180deg, rgba(7, 16, 24, 0.92), rgba(7, 16, 24, 0.96));
  border-bottom: 1px solid rgba(97, 211, 255, 0.12);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.22);
}

.md-tabs {
  background: rgba(8, 17, 27, 0.78);
  border-bottom: 1px solid rgba(97, 211, 255, 0.08);
}

.md-main {
  background:
    radial-gradient(circle at top left, rgba(0, 200, 255, 0.1), transparent 24%),
    radial-gradient(circle at top right, rgba(106, 124, 255, 0.08), transparent 22%),
    linear-gradient(180deg, rgba(7, 16, 24, 1), rgba(7, 16, 24, 0.96));
}

[data-md-color-scheme="default"] .md-main {
  background:
    radial-gradient(circle at top left, rgba(0, 124, 194, 0.08), transparent 22%),
    radial-gradient(circle at top right, rgba(106, 124, 255, 0.06), transparent 20%),
    linear-gradient(180deg, #edf4fb, #f7fbff);
}

.md-content__inner,
.md-sidebar__scrollwrap,
.md-search__form,
.md-search__output,
.md-typeset table:not([class]) {
  border-radius: 18px;
}

.md-content__inner {
  padding-top: 1.2rem;
}

.md-typeset h1,
.md-typeset h2,
.md-typeset h3 {
  letter-spacing: 0.02em;
}

.md-typeset a {
  color: var(--cf-accent-2);
}

[data-md-color-scheme="default"] .md-typeset a {
  color: #006fb0;
}

.md-typeset table:not([class]),
.md-typeset pre > code,
.md-sidebar,
.md-search__scrollwrap,
.md-nav--lifted > .md-nav__list > .md-nav__item > .md-nav__link,
.hero-panel {
  background: var(--cf-card);
  backdrop-filter: blur(14px);
  box-shadow: 0 18px 36px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(97, 211, 255, 0.12);
}

[data-md-color-scheme="default"] .md-typeset table:not([class]),
[data-md-color-scheme="default"] .md-typeset pre > code,
[data-md-color-scheme="default"] .md-sidebar,
[data-md-color-scheme="default"] .md-search__scrollwrap,
[data-md-color-scheme="default"] .md-nav--lifted > .md-nav__list > .md-nav__item > .md-nav__link,
[data-md-color-scheme="default"] .hero-panel {
  background: rgba(255, 255, 255, 0.82);
  border-color: rgba(18, 49, 76, 0.08);
}

.md-typeset table:not([class]) {
  overflow: hidden;
}

.hero-panel {
  padding: 1.4rem 1.5rem;
  margin-bottom: 1.5rem;
  border-radius: 24px;
}

.hero-panel__badge {
  display: inline-block;
  margin-bottom: 0.8rem;
  padding: 0.35rem 0.7rem;
  border-radius: 999px;
  background: linear-gradient(135deg, var(--cf-accent), var(--cf-accent-3));
  color: white;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.hero-panel h1 {
  margin-top: 0;
}

.md-typeset code {
  border-radius: 8px;
}

.md-top {
  background: linear-gradient(135deg, var(--cf-accent), var(--cf-accent-3));
}
"""


def main() -> None:
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    build_assets()

    plugin_dirs = sorted([p for p in PLUGINS_SRC.iterdir() if p.is_dir()])
    write_page(DOCS_DIR / "index.md", build_home(plugin_dirs))
    write_page(DOCS_DIR / "plugins" / "index.md", build_plugins_index(plugin_dirs))

    for plugin_dir in plugin_dirs:
        slug = plugin_dir.name
        for file in sorted(plugin_dir.glob("*.md")):
            raw = strip_front_matter(file.read_text(encoding="utf-8"))
            cleaned = rewrite_links(raw, plugin=slug)
            target_name = "index.md" if file.name.lower() == "readme.md" else file.name
            write_page(DOCS_DIR / "plugins" / slug / target_name, cleaned)


if __name__ == "__main__":
    main()

