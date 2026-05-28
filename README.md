# Cybernetic-Forge Plugin Documentation

This repository is now structured for **GitHub Pages** using **MkDocs** with the **Material for MkDocs** theme.

That keeps the site fully static and GitHub Pages-compatible while still giving you:

- fast search
- a documentation sidebar and tabbed navigation
- a polished dark-first plugin aesthetic
- built-in light and dark mode toggle
- automated deployment through GitHub Actions

## Architecture

- `plugins/`: source markdown for each plugin
- `docs-source/`: shared top-level templates and landing-page content
- `docs/`: generated MkDocs-ready pages
- `scripts/build_mkdocs_docs.py`: converts the source markdown into the `docs/` tree
- `mkdocs.yml`: site configuration, navigation, theme, and markdown extensions
- `docs/assets/stylesheets/extra.css`: Cybernetic-Forge visual theme overrides
- `.github/workflows/deploy-pages.yml`: GitHub Pages build and deployment workflow

## Authoring workflow

1. Edit plugin docs in `plugins/`.
2. Edit the landing page template in `docs-source/index.md` if needed.
3. Regenerate the MkDocs content tree:

   ```powershell
   python scripts/build_mkdocs_docs.py
   ```

4. Commit both the source changes and the regenerated `docs/` output.

## Local build

Install the documentation dependencies:

```powershell
pip install -r requirements.txt
```

Then build or preview the site:

```powershell
python scripts/build_mkdocs_docs.py
mkdocs serve
```

Or for a production build:

```powershell
python scripts/build_mkdocs_docs.py
mkdocs build
```

## GitHub Pages

The repository uses a custom GitHub Actions workflow based on the official GitHub Pages actions:

- `actions/configure-pages`
- `actions/upload-pages-artifact`
- `actions/deploy-pages`

No external server, SSH access, or runtime secrets are required.

## Theme direction

The site uses a Cybernetic-Forge look:

- dark steel / obsidian backgrounds
- electric cyan and blue accents
- elevated glass-style surfaces
- built-in light mode for accessibility and daytime reading

## Important note

Wiki.js is not compatible with plain GitHub Pages hosting, because Wiki.js requires a running application server and database. This repo now uses the closest static alternative that still feels modern and wiki-like on GitHub Pages.

