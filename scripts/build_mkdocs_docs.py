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
    raw = readme.read_text(encoding="utf-8")
    front_matter = FRONT_MATTER_RE.match(raw)
    if front_matter:
        title_match = re.search(r"(?m)^title:\s*(.+?)\s*$", front_matter.group(0))
        if title_match:
            return title_match.group(1).strip().strip("'\"")

    text = strip_front_matter(raw)
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


def build_plugin_card(slug: str, title: str, base_path: str) -> str:
    root = f"{base_path}{slug}/"
    return "\n".join(
        [
            '<article class="plugin-card">',
            f'  <h3><a href="{root}">{title}</a></h3>',
            f'  <p>Setup, commands, configuration, and API information for {title}.</p>',
            '  <div class="plugin-card__links">',
            f'    <a href="{root}">Overview</a>',
            f'    <a href="{root}commands/">Commands</a>',
            f'    <a href="{root}configuration/">Configuration</a>',
            f'    <a href="{root}api_information/">API</a>',
            '  </div>',
            '</article>',
        ]
    )


def build_home(plugin_dirs: list[Path]) -> str:
    template = (DOCS_SOURCE / "index.md").read_text(encoding="utf-8")
    cards = [
        build_plugin_card(directory.name, plugin_title(directory), "plugins/")
        for directory in plugin_dirs
    ]
    catalog = '<div class="plugin-grid">\n' + "\n\n".join(cards) + "\n</div>"
    return template.replace("{{PLUGIN_CATALOG}}", catalog)



def build_plugins_index(plugin_dirs: list[Path]) -> str:
    lines = [
        "# Plugins",
        "",
        "Choose a plugin to open its operating guide, configuration, and API reference.",
        "",
        '<div class="plugin-grid">',
    ]
    for directory in plugin_dirs:
        slug = directory.name
        title = plugin_title(directory)
        lines.extend([build_plugin_card(slug, title, ""), ""])
    lines.append("</div>")
    return "\n".join(lines)


def build_assets() -> None:
    css = ROOT / "docs" / "assets" / "stylesheets" / "extra.css"
    css.parent.mkdir(parents=True, exist_ok=True)
    css.write_text(EXTRA_CSS.strip() + "\n", encoding="utf-8")
    javascript = ROOT / "docs" / "assets" / "javascripts" / "arcane-background.js"
    javascript.parent.mkdir(parents=True, exist_ok=True)
    javascript.write_text(EXTRA_JAVASCRIPT.strip() + "\n", encoding="utf-8")


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

/* Animated documentation chrome inspired by the Cybernetic-Forge visual language. */
:root {
  --cf-accent-warm: #f0b35b;
  --cf-line: rgba(97, 211, 255, 0.16);
  --cf-line-strong: rgba(97, 211, 255, 0.34);
  --cf-panel: rgba(10, 20, 26, 0.78);
}

[data-md-color-scheme="slate"] {
  --md-default-bg-color: #070d10;
  --md-default-bg-color--light: #0b1519;
  --md-default-bg-color--lighter: #102127;
  --md-default-fg-color: #e8f2f4;
  --md-default-fg-color--light: #9eb5ba;
  --md-code-bg-color: #081114;
}

.md-header {
  overflow: visible;
  background:
    linear-gradient(115deg, transparent 0 47%, rgba(97, 211, 255, 0.12) 48%, transparent 49%),
    linear-gradient(25deg, transparent 0 47%, rgba(240, 179, 91, 0.09) 48%, transparent 49%),
    linear-gradient(90deg, rgba(4, 11, 14, 0.96), rgba(10, 31, 37, 0.88), rgba(4, 11, 14, 0.96)),
    linear-gradient(135deg, rgba(0, 200, 255, 0.18), rgba(240, 179, 91, 0.08));
  background-size: 180px 110px, 240px 140px, auto, auto;
  border-top: 2px solid var(--cf-accent-warm);
  border-bottom: 1px solid var(--cf-line-strong);
  box-shadow: 0 14px 34px rgba(0, 0, 0, 0.32);
  animation: cf-header-background 22s linear infinite;
}

.md-header::before {
  content: none;
}

.md-header::after {
  content: none;
}

.md-header__inner,
.md-tabs {
  position: relative;
  z-index: 1;
}

.md-header__title,
.md-header__button,
.md-tabs__link {
  text-shadow: 0 0 18px rgba(97, 211, 255, 0.18);
}

.md-tabs {
  background: rgba(3, 10, 13, 0.74);
  border-bottom: 1px solid rgba(97, 211, 255, 0.1);
}

.md-tabs__link {
  opacity: 0.78;
  transition: color 180ms ease, opacity 180ms ease, transform 180ms ease;
}

.md-tabs__link:hover,
.md-tabs__link--active {
  opacity: 1;
  color: #ffffff;
  transform: translateY(-1px);
}

.md-main {
  position: relative;
  isolation: isolate;
  background-color: #070d10;
  background-image:
    linear-gradient(rgba(97, 211, 255, 0.045) 1px, transparent 1px),
    linear-gradient(90deg, rgba(97, 211, 255, 0.045) 1px, transparent 1px),
    radial-gradient(circle at 78% 0%, rgba(0, 200, 255, 0.1), transparent 26%),
    radial-gradient(circle at 8% 18%, rgba(240, 179, 91, 0.07), transparent 22%);
  background-size: 46px 46px, 46px 46px, auto, auto;
}

.md-main__inner {
  position: relative;
  z-index: 1;
}

.cf-arcane-background {
  --cf-arcane-x: 0px;
  --cf-arcane-y: 0px;
  --cf-arcane-tilt: 0deg;
  position: fixed;
  top: 50%;
  left: 50%;
  z-index: 0;
  width: min(112vmin, 1180px);
  aspect-ratio: 1;
  color: #70dff4;
  opacity: 0.062;
  pointer-events: none;
  transform:
    translate3d(
      calc(-50% + var(--cf-arcane-x)),
      calc(-50% + var(--cf-arcane-y)),
      0
    )
    rotate(var(--cf-arcane-tilt))
    scale(1.025);
  transform-origin: center;
  will-change: transform;
}

[data-md-color-scheme="default"] .cf-arcane-background {
  color: #0d6281;
  opacity: 0.044;
  mix-blend-mode: multiply;
}

.cf-arcane-background svg {
  display: block;
  width: 100%;
  height: 100%;
  overflow: visible;
  filter: drop-shadow(0 0 10px currentColor);
}

.cf-arcane-background path,
.cf-arcane-background circle,
.cf-arcane-background ellipse,
.cf-arcane-background line,
.cf-arcane-background polygon,
.cf-arcane-background polyline {
  vector-effect: non-scaling-stroke;
}

.cf-arcane__orbit--outer {
  transform-origin: center;
  animation: cf-arcane-turn 180s linear infinite;
}

.cf-arcane__orbit--inner {
  transform-origin: center;
  animation: cf-arcane-turn-reverse 132s linear infinite;
}

.cf-arcane__pulse {
  transform-origin: center;
  animation: cf-arcane-breathe 12s ease-in-out infinite;
}

.md-content__inner {
  padding-top: 2rem;
  padding-bottom: 4rem;
}

.md-sidebar__scrollwrap {
  scrollbar-color: rgba(97, 211, 255, 0.35) transparent;
}

.md-nav__link {
  border-left: 1px solid transparent;
  transition: color 180ms ease, border-color 180ms ease, background 180ms ease, transform 180ms ease;
}

.md-nav__link:hover {
  border-left-color: var(--cf-accent-warm);
  background: rgba(97, 211, 255, 0.06);
  transform: translateX(2px);
}

.md-nav__link--active {
  border-left-color: var(--cf-accent-warm);
  background: linear-gradient(90deg, rgba(240, 179, 91, 0.11), transparent);
}

.hero-panel {
  position: relative;
  overflow: hidden;
  isolation: isolate;
  min-height: 250px;
  padding: clamp(2rem, 5vw, 4rem);
  margin: 0 0 2.8rem;
  border: 1px solid var(--cf-line-strong);
  border-top: 2px solid var(--cf-accent-warm);
  border-radius: 4px;
  background:
    linear-gradient(115deg, rgba(9, 22, 27, 0.97), rgba(9, 29, 35, 0.82)),
    radial-gradient(circle at 75% 42%, rgba(0, 200, 255, 0.16), transparent 28%);
  box-shadow: 0 24px 58px rgba(0, 0, 0, 0.32), inset 0 0 0 1px rgba(255, 255, 255, 0.025);
}

[data-md-color-scheme="default"] .hero-panel {
  border-color: var(--cf-line-strong);
  border-top-color: var(--cf-accent-warm);
  background:
    linear-gradient(115deg, rgba(9, 22, 27, 0.98), rgba(9, 29, 35, 0.94)),
    radial-gradient(circle at 75% 42%, rgba(0, 200, 255, 0.16), transparent 28%);
}

[data-md-color-scheme="default"] .hero-panel h1 {
  color: #f5fbfc;
}

[data-md-color-scheme="default"] .hero-panel p {
  color: #b5c9cd;
}

[data-md-color-scheme="default"] .hero-panel__stat strong {
  color: #f5fbfc;
}

[data-md-color-scheme="default"] .hero-panel__stat span,
[data-md-color-scheme="default"] .hero-panel__meta {
  color: #82a1a7;
}

.hero-panel::before {
  content: "";
  position: absolute;
  inset: -35%;
  z-index: -2;
  opacity: 0.72;
  background-image:
    linear-gradient(135deg, transparent 0 48%, rgba(97, 211, 255, 0.18) 49%, transparent 50%),
    linear-gradient(45deg, transparent 0 48%, rgba(240, 179, 91, 0.12) 49%, transparent 50%);
  background-size: 170px 170px, 230px 230px;
  transform: rotate(-8deg);
  animation: cf-hero-grid 26s linear infinite;
  pointer-events: none;
}

.hero-panel::after {
  content: "";
  position: absolute;
  top: 10%;
  right: 8%;
  width: clamp(150px, 26vw, 310px);
  aspect-ratio: 1;
  z-index: -1;
  border: 1px solid rgba(97, 211, 255, 0.28);
  box-shadow: 0 0 0 20px rgba(97, 211, 255, 0.035), 0 0 70px rgba(0, 200, 255, 0.14);
  transform: rotate(45deg);
  animation: cf-hero-orbit 18s ease-in-out infinite;
  pointer-events: none;
}

.hero-panel > * {
  position: relative;
  z-index: 1;
}

.hero-panel__kicker,
.plugin-card__eyebrow {
  display: block;
  margin-bottom: 0.8rem;
  color: var(--cf-accent-warm);
  font-family: var(--md-code-font-family);
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.hero-panel__badge {
  margin-bottom: 1rem;
  padding: 0.34rem 0.68rem;
  border: 1px solid rgba(240, 179, 91, 0.5);
  border-radius: 2px;
  background: rgba(240, 179, 91, 0.1);
  color: #ffd995;
  font-family: var(--md-code-font-family);
  font-size: 0.7rem;
  letter-spacing: 0.12em;
}

.hero-panel h1 {
  max-width: 850px;
  margin: 0;
  color: #f5fbfc;
  font-size: clamp(2.4rem, 6vw, 5.2rem);
  font-weight: 800;
  line-height: 0.98;
  letter-spacing: -0.045em;
}

.hero-panel p {
  max-width: 760px;
  color: #b5c9cd;
  font-size: clamp(1rem, 1.5vw, 1.18rem);
}

.hero-panel__actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.8rem;
  margin-top: 1.4rem;
}

.hero-panel__action,
.plugin-card__links a {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.65rem 0.9rem;
  border: 1px solid rgba(240, 179, 91, 0.7);
  border-radius: 2px;
  background: linear-gradient(135deg, #f0b35b, #c88336);
  color: #071014 !important;
  font-weight: 800;
  text-decoration: none !important;
  transition: transform 180ms ease, box-shadow 180ms ease, filter 180ms ease;
}

.hero-panel__action:hover,
.plugin-card__links a:hover {
  filter: brightness(1.08);
  box-shadow: 0 8px 22px rgba(240, 179, 91, 0.22);
  transform: translateY(-2px);
}

.hero-panel__meta {
  color: #87a1a7;
  font-family: var(--md-code-font-family);
  font-size: 0.72rem;
}

.hero-panel__stats {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  max-width: 760px;
  margin-top: 2rem;
  border: 1px solid var(--cf-line-strong);
  background: rgba(3, 12, 15, 0.52);
}

.hero-panel__stat {
  padding: 0.9rem 1rem;
  border-right: 1px solid var(--cf-line);
}

.hero-panel__stat:last-child {
  border-right: 0;
}

.hero-panel__stat strong {
  display: block;
  color: #f5fbfc;
  font-size: 1.35rem;
}

.hero-panel__stat span {
  color: #82a1a7;
  font-family: var(--md-code-font-family);
  font-size: 0.62rem;
  letter-spacing: 0.07em;
  text-transform: uppercase;
}

.plugin-card {
  position: relative;
  min-height: 190px;
  padding: 1.4rem;
  margin: 0;
  border: 1px solid var(--cf-line);
  border-top: 2px solid rgba(97, 211, 255, 0.4);
  border-radius: 3px;
  background: linear-gradient(145deg, rgba(13, 27, 33, 0.86), rgba(8, 17, 21, 0.72));
  transition: border-color 180ms ease, transform 180ms ease, box-shadow 180ms ease;
}

.plugin-card:hover {
  border-color: var(--cf-accent-warm);
  box-shadow: 0 18px 34px rgba(0, 0, 0, 0.24), 0 0 26px rgba(0, 200, 255, 0.08);
  transform: translateY(-3px);
}

.plugin-card h3 {
  margin: 0;
  font-size: 1.45rem;
}

.plugin-card h3 a {
  color: #f5fbfc;
  text-decoration: none;
}

.plugin-card p {
  color: #9eb5ba;
  font-size: 0.9rem;
}

.plugin-card__links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  margin-top: 1rem;
}

.plugin-card__links a {
  padding: 0.36rem 0.55rem;
  border-color: var(--cf-line-strong);
  background: rgba(97, 211, 255, 0.08);
  color: #a8e9f8 !important;
  font-family: var(--md-code-font-family);
  font-size: 0.68rem;
  font-weight: 600;
}

.plugin-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 0.8rem;
  margin: 1.2rem 0 2rem;
}

.plugin-grid .plugin-card {
  min-height: 0;
  padding: 1rem 1.05rem;
}

.plugin-grid .plugin-card__eyebrow {
  margin-bottom: 0.4rem;
  font-size: 0.6rem;
}

.plugin-grid .plugin-card h3 {
  font-size: 1.2rem;
}

.plugin-grid .plugin-card p {
  margin: 0.45rem 0 0;
  font-size: 0.8rem;
  line-height: 1.45;
}

.plugin-grid .plugin-card__links {
  gap: 0.35rem;
  margin-top: 0.7rem;
}

.plugin-grid .plugin-card__links a {
  padding: 0.28rem 0.45rem;
  font-size: 0.61rem;
}

.md-header__inner {
  height: 2.65rem;
  min-height: 2.65rem;
  padding-top: 0;
  padding-bottom: 0;
}

.md-header__button {
  padding: 0.45rem;
}

.md-search__form {
  height: 1.95rem;
}

.md-tabs__list,
.md-tabs__item {
  height: 2.1rem;
}

.md-tabs__item {
  padding-left: 0.85rem;
  padding-right: 0.85rem;
}

.md-tabs__link {
  margin-top: 0.55rem;
  font-size: 0.68rem;
}

.md-content__inner {
  padding-top: 1.25rem;
  padding-bottom: 3rem;
}

.md-grid {
  width: 100%;
  max-width: none;
}

.md-header__inner,
.md-tabs__inner {
  padding-right: clamp(0.75rem, 2vw, 2rem);
  padding-left: clamp(0.75rem, 2vw, 2rem);
}

.md-main__inner {
  width: 100%;
  max-width: none;
  margin-right: 0;
  margin-left: 0;
  padding-right: clamp(0.75rem, 1.5vw, 1.5rem);
  padding-left: clamp(0.75rem, 1.5vw, 1.5rem);
}

.md-content {
  min-width: 0;
  max-width: none;
}

.md-content__inner {
  max-width: none;
}

body:has(.hero-panel--home) .md-sidebar--primary,
body:has(.hero-panel--home) .md-sidebar--secondary {
  display: none;
}

body:has(.hero-panel--home) .md-content {
  margin-right: 0;
  margin-left: 0;
}

body:has(.hero-panel--home) .md-content__inner {
  margin: 0;
}

body:has(.hero-panel--home) .md-typeset > h2 {
  margin-top: 1.6rem;
}

.md-typeset > p,
.md-typeset > ul,
.md-typeset > ol {
  max-width: 88ch;
}

.hero-panel,
.plugin-grid,
.md-typeset table:not([class]),
.md-typeset pre {
  width: 100%;
  max-width: none;
}

.hero-panel {
  min-height: 0;
  padding: clamp(1.5rem, 3.6vw, 2.8rem);
  margin-bottom: 1.8rem;
}

.hero-panel h1 {
  font-size: clamp(2.35rem, 5vw, 4.35rem);
}

.hero-panel p {
  margin: 0.8rem 0 0;
  font-size: clamp(0.92rem, 1.35vw, 1.08rem);
}

.hero-panel__actions {
  margin-top: 1rem;
}

.hero-panel__stats {
  margin-top: 1.25rem;
}

.hero-panel__stat {
  padding: 0.62rem 0.75rem;
}

.hero-panel__stat strong {
  font-size: 1.1rem;
}

.hero-panel__stat span {
  font-size: 0.55rem;
}

.md-typeset h1,
.md-typeset h2,
.md-typeset h3 {
  font-weight: 800;
  letter-spacing: -0.025em;
}

.md-typeset h2 {
  margin-top: 3.4rem;
  padding-top: 1.3rem;
  border-top: 1px solid var(--cf-line);
}

.md-typeset h2::before {
  content: "//";
  display: block;
  margin-bottom: 0.35rem;
  color: var(--cf-accent-warm);
  font-family: var(--md-code-font-family);
  font-size: 0.66rem;
  letter-spacing: 0.15em;
}

.md-typeset table:not([class]) {
  border-color: var(--cf-line);
  background: var(--cf-panel);
}

.md-typeset table:not([class]) th {
  background: rgba(97, 211, 255, 0.08);
  color: #b9eff8;
  font-family: var(--md-code-font-family);
  font-size: 0.72rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.md-typeset table:not([class]) tr:hover td {
  background: rgba(97, 211, 255, 0.045);
}

.md-typeset pre > code {
  border-color: var(--cf-line);
  background: rgba(4, 13, 16, 0.9);
}

.md-typeset code {
  border: 1px solid rgba(97, 211, 255, 0.12);
  background: rgba(97, 211, 255, 0.07);
  color: #b2eef8;
}

.md-footer {
  border-top: 1px solid var(--cf-line);
  background: #060c0f;
}

@keyframes cf-header-background {
  0% {
    background-position: 0 0, 0 0, 0 0, 0 0;
  }
  100% {
    background-position: 180px 0, -240px 0, 0 0, 0 0;
  }
}

@keyframes cf-arcane-turn {
  to { transform: rotate(360deg); }
}

@keyframes cf-arcane-turn-reverse {
  to { transform: rotate(-360deg); }
}

@keyframes cf-arcane-breathe {
  0%, 100% { opacity: 0.62; transform: scale(0.995); }
  50% { opacity: 1; transform: scale(1.008); }
}

@keyframes cf-hero-grid {
  from { transform: translate3d(-3%, -2%, 0) rotate(-8deg); }
  to { transform: translate3d(3%, 2%, 0) rotate(-8deg); }
}

@keyframes cf-hero-orbit {
  0%, 100% { transform: rotate(45deg) scale(0.94); opacity: 0.5; }
  50% { transform: rotate(135deg) scale(1.04); opacity: 0.9; }
}

@media (max-width: 700px) {
  .plugin-grid {
    grid-template-columns: 1fr;
  }

  .hero-panel {
    min-height: 0;
    padding: 1.5rem;
  }

  .hero-panel::after {
    right: -80px;
    opacity: 0.45;
  }

  .hero-panel__stats {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .hero-panel__stat:nth-child(2) {
    border-right: 0;
  }

  .hero-panel__stat:nth-child(-n + 2) {
    border-bottom: 1px solid var(--cf-line);
  }
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.001ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: 0.001ms !important;
  }
}
"""


EXTRA_JAVASCRIPT = r"""
(() => {
  "use strict";

  if (document.querySelector(".cf-arcane-background")) {
    return;
  }

  const main = document.querySelector(".md-main");
  if (!main) {
    return;
  }

  const polar = (radius, angle) => {
    const radians = (angle - 90) * Math.PI / 180;
    return [
      (radius * Math.cos(radians)).toFixed(2),
      (radius * Math.sin(radians)).toFixed(2),
    ];
  };

  const polygon = (sides, radius, offset = 0) =>
    Array.from({ length: sides }, (_, index) =>
      polar(radius, offset + index * 360 / sides).join(",")
    ).join(" ");

  const ticks = Array.from({ length: 72 }, (_, index) => {
    const major = index % 6 === 0;
    const medium = index % 3 === 0;
    const outer = polar(458, index * 5);
    const inner = polar(major ? 428 : medium ? 438 : 445, index * 5);
    return `<line x1="${inner[0]}" y1="${inner[1]}" x2="${outer[0]}" y2="${outer[1]}" stroke-width="${major ? 2 : 0.8}" opacity="${major ? 0.95 : medium ? 0.72 : 0.42}" />`;
  }).join("");

  const spokes = Array.from({ length: 24 }, (_, index) => {
    const outer = polar(index % 2 ? 355 : 375, index * 15);
    const inner = polar(index % 2 ? 182 : 206, index * 15);
    return `<line x1="${inner[0]}" y1="${inner[1]}" x2="${outer[0]}" y2="${outer[1]}" stroke-width="0.8" opacity="${index % 2 ? 0.36 : 0.62}" />`;
  }).join("");

  const nodes = Array.from({ length: 12 }, (_, index) => {
    const point = polar(394, index * 30);
    const rotation = index * 30;
    return `
      <g transform="translate(${point[0]} ${point[1]}) rotate(${rotation})">
        <circle r="18" stroke-width="1" />
        <circle r="12" stroke-dasharray="2 4" stroke-width="0.8" />
        <path d="M 0 -11 L 7 0 L 0 11 L -7 0 Z M -11 0 H 11 M 0 -15 V 15" stroke-width="0.9" />
        <circle r="2.2" fill="currentColor" stroke="none" />
      </g>`;
  }).join("");

  const petals = Array.from({ length: 16 }, (_, index) =>
    `<ellipse cx="0" cy="-117" rx="26" ry="104" transform="rotate(${index * 22.5})" stroke-width="0.75" opacity="0.48" />`
  ).join("");

  const layer = document.createElement("div");
  layer.className = "cf-arcane-background";
  layer.setAttribute("aria-hidden", "true");
  layer.innerHTML = `
    <svg viewBox="-520 -520 1040 1040" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
      <g class="cf-arcane__pulse">
        <circle r="486" stroke-width="0.7" opacity="0.22" />
        <circle r="472" stroke-width="1.1" stroke-dasharray="1 9" opacity="0.62" />
        <circle r="458" stroke-width="0.9" />
        ${ticks}
      </g>

      <g class="cf-arcane__orbit--outer">
        <circle r="423" stroke-width="1.1" stroke-dasharray="94 13 4 13" />
        <circle r="410" stroke-width="0.65" stroke-dasharray="2 7" />
        <polygon points="${polygon(12, 394, 15)}" stroke-width="0.8" opacity="0.54" />
        <polygon points="${polygon(6, 380)}" stroke-width="1.15" />
        <polygon points="${polygon(6, 380, 30)}" stroke-width="1.15" />
        ${nodes}
      </g>

      <g opacity="0.72">
        <circle r="362" stroke-width="0.8" />
        <circle r="345" stroke-width="1" stroke-dasharray="18 6 2 6" />
        ${spokes}
        <polygon points="${polygon(8, 318, 22.5)}" stroke-width="0.75" />
        <polygon points="${polygon(4, 304, 45)}" stroke-width="1.05" />
        <polygon points="${polygon(4, 304)}" stroke-width="1.05" />
      </g>

      <g class="cf-arcane__orbit--inner">
        <circle r="278" stroke-width="1" stroke-dasharray="54 7 3 7" />
        <circle r="254" stroke-width="0.75" stroke-dasharray="2 8" />
        <polygon points="${polygon(12, 246)}" stroke-width="0.7" opacity="0.65" />
        <polygon points="${polygon(3, 232)}" stroke-width="1.25" />
        <polygon points="${polygon(3, 232, 60)}" stroke-width="1.25" />
        <polygon points="${polygon(3, 232, 30)}" stroke-width="0.65" opacity="0.56" />
        <polygon points="${polygon(3, 232, 90)}" stroke-width="0.65" opacity="0.56" />
      </g>

      <g opacity="0.68">
        ${petals}
        <circle r="174" stroke-width="0.8" />
        <circle r="146" stroke-width="1.1" stroke-dasharray="5 7" />
        <polygon points="${polygon(8, 132, 22.5)}" stroke-width="0.9" />
        <polygon points="${polygon(4, 112, 45)}" stroke-width="1.2" />
        <circle r="92" stroke-width="0.75" />
        <path d="M 0 -82 L 22 -22 L 82 0 L 22 22 L 0 82 L -22 22 L -82 0 L -22 -22 Z" stroke-width="1.1" />
        <circle r="50" stroke-width="0.8" stroke-dasharray="1 5" />
        <path d="M 0 -42 L 36 21 L -36 21 Z M 0 42 L 36 -21 L -36 -21 Z" stroke-width="1.1" />
        <circle r="13" stroke-width="1.2" />
        <circle r="4" fill="currentColor" stroke="none" />
      </g>

      <g stroke-width="0.7" opacity="0.38">
        <path d="M -472 0 H -362 M 362 0 H 472 M 0 -472 V -362 M 0 362 V 472" />
        <path d="M -334 -334 L -265 -265 M 265 265 L 334 334 M 334 -334 L 265 -265 M -265 265 L -334 334" />
        <circle cx="-334" cy="-334" r="8" />
        <circle cx="334" cy="-334" r="8" />
        <circle cx="334" cy="334" r="8" />
        <circle cx="-334" cy="334" r="8" />
      </g>
    </svg>`;
  main.prepend(layer);

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (reducedMotion.matches) {
    return;
  }

  let targetX = 0;
  let targetY = 0;
  let currentX = 0;
  let currentY = 0;
  let frame = 0;

  const render = () => {
    currentX += (targetX - currentX) * 0.065;
    currentY += (targetY - currentY) * 0.065;
    layer.style.setProperty("--cf-arcane-x", `${currentX.toFixed(2)}px`);
    layer.style.setProperty("--cf-arcane-y", `${currentY.toFixed(2)}px`);
    layer.style.setProperty("--cf-arcane-tilt", `${(currentX * -0.018).toFixed(3)}deg`);

    if (Math.abs(targetX - currentX) > 0.02 || Math.abs(targetY - currentY) > 0.02) {
      frame = requestAnimationFrame(render);
    } else {
      frame = 0;
    }
  };

  const moveTo = (x, y) => {
    targetX = -((x / window.innerWidth) - 0.5) * 34;
    targetY = -((y / window.innerHeight) - 0.5) * 26;
    if (!frame) {
      frame = requestAnimationFrame(render);
    }
  };

  window.addEventListener("pointermove", (event) => moveTo(event.clientX, event.clientY), { passive: true });
  document.documentElement.addEventListener("mouseleave", () => moveTo(window.innerWidth / 2, window.innerHeight / 2));
})();
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
