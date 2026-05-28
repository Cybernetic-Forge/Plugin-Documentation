# Cybernetic-Forge Plugin Documentation

Welcome to the official **Cybernetic-Forge** documentation hub.

This knowledge base now runs on **Wiki.js**, giving the project a real documentation workflow with:

- self-hosted search and navigation
- structured page trees for every plugin
- Git-backed content sync
- a branded Cybernetic-Forge dark theme with optional light mode

## Available Plugins

{{PLUGIN_CATALOG}}

## Editing Model

- Plugin-specific source markdown lives under `plugins/`
- Shared landing pages live under `wiki-source/`
- Generated Wiki.js content lives under `wiki-content/`

If you are working inside the repo, rebuild the generated content with:

```powershell
python scripts/build_wikijs_content.py
```

## Notes

This documentation is actively evolving alongside the plugins themselves. If something looks incomplete or outdated, it is usually because the plugin moved faster than the written docs and simply needs another pass.

