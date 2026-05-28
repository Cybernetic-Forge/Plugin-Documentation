from __future__ import annotations

import shutil
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
PLUGINS_SRC = ROOT / "plugins"
WIKI_SOURCE = ROOT / "wiki-source"
WIKI_CONTENT = ROOT / "wiki-content"

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

        if "#" in url:
            base, anchor = url.split("#", 1)
            anchor = f"#{anchor}"
        else:
            base, anchor = url, ""

        normalized = base.replace("\\", "/").strip()

        if normalized.endswith(".md"):
            normalized = normalized[:-3]

        if plugin:
            normalized = normalized.removeprefix("./")
            if normalized in ("README", "home"):
                return f"[{label}](/plugins/{plugin}{anchor})"
            if "/" not in normalized and normalized:
                return f"[{label}](/plugins/{plugin}/{normalized}{anchor})"

        normalized = normalized.removeprefix("./")
        if normalized.endswith("/README"):
            normalized = normalized[: -len("/README")]
        elif normalized == "README":
            normalized = "home"

        if not normalized.startswith("/"):
            normalized = "/" + normalized

        normalized = normalized.replace("/home", "", 1) if normalized == "/home" else normalized
        return f"[{label}]({normalized}{anchor})"

    return MARKDOWN_LINK_RE.sub(repl, text)


def write_page(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def build_home(plugin_dirs: list[Path]) -> str:
    template = (WIKI_SOURCE / "home.md").read_text(encoding="utf-8")
    cards = []
    for directory in plugin_dirs:
        slug = directory.name
        title = plugin_title(directory)
        cards.append(
            "\n".join(
                [
                    f"### {title}",
                    "",
                    f"Start here: [{title} Overview](/plugins/{slug})",
                    "",
                    "| Section | Description |",
                    "| --- | --- |",
                    f"| [Commands](/plugins/{slug}/commands) | Command reference for {title} |",
                    f"| [Configuration](/plugins/{slug}/configuration) | Config, tuning, and file structure for {title} |",
                    f"| [API Information](/plugins/{slug}/api_information) | Integration and runtime notes for {title} |",
                ]
            )
        )
    return template.replace("{{PLUGIN_CATALOG}}", "\n\n".join(cards))


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
                f"## [{title}](/plugins/{slug})",
                "",
                f"- [Overview](/plugins/{slug})",
                f"- [Commands](/plugins/{slug}/commands)",
                f"- [Configuration](/plugins/{slug}/configuration)",
                f"- [API Information](/plugins/{slug}/api_information)",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    if WIKI_CONTENT.exists():
        shutil.rmtree(WIKI_CONTENT)
    WIKI_CONTENT.mkdir(parents=True, exist_ok=True)

    plugin_dirs = sorted([path for path in PLUGINS_SRC.iterdir() if path.is_dir()])

    home_text = build_home(plugin_dirs)
    write_page(WIKI_CONTENT / "home.md", rewrite_links(home_text))
    write_page(WIKI_CONTENT / "plugins" / "home.md", build_plugins_index(plugin_dirs))

    for plugin_dir in plugin_dirs:
        slug = plugin_dir.name
        for file in sorted(plugin_dir.glob("*.md")):
            raw = strip_front_matter(file.read_text(encoding="utf-8"))
            cleaned = rewrite_links(raw, plugin=slug)
            target_name = "home.md" if file.name.lower() == "readme.md" else file.name
            write_page(WIKI_CONTENT / "plugins" / slug / target_name, cleaned)


if __name__ == "__main__":
    main()

