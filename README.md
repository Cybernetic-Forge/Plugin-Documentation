# Cybernetic-Forge Plugin Documentation

This repository now targets a **Wiki.js** deployment instead of GitHub Pages / Jekyll.

The authoritative documentation source remains the markdown in this repository on `main`. Wiki.js is the published presentation, search, and navigation layer.

## Architecture

- `plugins/`: source markdown for plugin documentation
- `wiki-source/`: hand-authored Wiki.js landing pages and shared content
- `wiki-content/`: generated Wiki.js Git-storage content branch payload
- `deploy/`: Docker + Nginx reverse-proxy assets, including the Cybernetic-Forge dark/light theme layer
- `.github/workflows/publish-wikijs-content.yml`: publishes the generated `wikijs-content` branch
- `.github/workflows/deploy-wikijs.yml`: deploys the Wiki.js stack to a Linux host over SSH
- `ops/WIKIJS_SETUP.md`: first-run setup guide for connecting Wiki.js to the generated content branch

## Why this layout

Wiki.js stores pages in its database and can sync them to a **dedicated Git repository**. The official Git storage docs note that the target repository cannot be limited to a subfolder, so this repo uses a dedicated branch named `wikijs-content` for the synced page tree while keeping infrastructure and authoring sources on `main`.

## Local workflow

1. Edit plugin docs in `plugins/` or shared wiki pages in `wiki-source/`.
2. Rebuild the Wiki.js page tree:

   ```powershell
   python scripts/build_wikijs_content.py
   ```

3. Review the generated files in `wiki-content/`.
4. Push to `main`.

The `publish-wikijs-content.yml` workflow force-publishes `wiki-content/` to the `wikijs-content` branch for Wiki.js Git sync/import.

Because `wikijs-content` is generated output, direct in-app Wiki.js edits should only be used if you also copy those edits back into the source markdown on `main`.

## Deployment model

The deployment workflow assumes:

- a Linux VPS or server with Docker Engine and Docker Compose Plugin installed
- SSH access from GitHub Actions
- a reverse-proxied or directly exposed HTTP endpoint for the Wiki.js stack
- Git storage in Wiki.js pointed at this repository's `wikijs-content` branch

The Docker stack includes:

- `postgres:15-alpine`
- `ghcr.io/requarks/wiki:2`
- `nginx:alpine` as a branded reverse proxy with CSS / JS injection

## Required GitHub Secrets

For `.github/workflows/deploy-wikijs.yml`:

- `DEPLOY_HOST`
- `DEPLOY_PORT`
- `DEPLOY_USER`
- `DEPLOY_SSH_KEY`
- `DEPLOY_PATH`
- `POSTGRES_PASSWORD`
- `WIKI_CONTENT_SSH_PRIVATE_KEY`

Optional:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `HTTP_PORT`

## Theme

The Cybernetic-Forge theme is applied by the Nginx layer in `deploy/nginx/nginx.conf`, which injects:

- `/theme/cybernetic-forge.css`
- `/theme/cybernetic-forge.js`

This keeps branding under version control instead of relying on manual admin-only CSS overrides.

## First-time Wiki.js setup

After the first deployment:

1. Open the site and complete the Wiki.js setup wizard.
2. Follow [ops/WIKIJS_SETUP.md](ops/WIKIJS_SETUP.md).
3. Configure Git storage to sync against the `wikijs-content` branch.
4. Run **Import Everything** once from the Git storage screen.
