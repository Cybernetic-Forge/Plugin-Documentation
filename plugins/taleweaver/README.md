---
title: Taleweaver
nav_order: 5
has_children: true
has_toc: true
---

# Taleweaver

Taleweaver is a Paper plugin for turning a server's items, entities, locations, quests, skills, recipes, and other gameplay objects into a persistent, discoverable lore graph.

It combines:

- a MariaDB-backed lore catalogue;
- an in-game lore browser and editor;
- player journals with discovery, unread, favourite, search, and private-note state;
- player suggestions with administrator review and stale-change protection;
- parent/child inheritance and directional relations;
- revision history with comparison and restore;
- optional integrations for common content, item, quest, skill, NPC, and protection plugins;
- optional AI-assisted drafting, consistency checks, and lore-aware NPC conversations;
- optional generated resource-pack icons and custom model data.

## Compatibility and requirements

| Requirement | Supported value |
| --- | --- |
| Server | Paper API `26.1.x` (the plugin descriptor targets `26.1.1`) |
| Database | MariaDB, reachable by JDBC |
| Java | Use the Java runtime required by the installed Paper release |
| Plugin version covered here | `1.2.0` |

Taleweaver starts its database schema automatically. Create the database and grant the configured user access before first startup; the tables are created by the plugin when it connects.

## Installation

1. Install Paper and a working MariaDB server.
2. Copy `Taleweaver.jar` into the server's `plugins` directory.
3. Start the server once so Taleweaver creates its data folder and default files.
4. Edit `plugins/Taleweaver/config.yml` with the MariaDB host, database, credentials, and port.
5. Restart the server. A reload is not enough when changing SQL connection settings.
6. Grant administrators `taleweaver.lore`, `taleweaver.review`, `taleweaver.ai`, and the version permissions as needed.
7. Run `/lore info` and `/journal inspect` in-game to verify the installation.

The plugin soft-depends on integrations rather than requiring them. Install only the integrations used by the server; Taleweaver detects enabled plugins at runtime and registers the matching handlers.

## First-use workflow

### Administrators

1. Configure SQL and restart.
2. Run `/lore auto-create Vanilla` to seed vanilla registries enabled in `config.yml`.
3. Install supported content plugins, restart, then run `/lore auto-create <HookName>` for the integrations you want to import.
4. Use `/lore show` to browse the catalogue and `/lore edit <reference>` to write descriptions.
5. Use `/lore parent set <child> <parent>` for inheritance and `/lore relation set <source> <target>` for directional relations.
6. Enable revisions before a production content pass so edits and restores remain auditable.

### Players

Players discover lore through configured discovery events, `/journal inspect`, and supported integration bridges. They can open `/journal`, filter unread or recent entries, favourite entries, write private notes, and submit description suggestions when permitted.

## How the lore graph works

Every entry has a UUID, display name, description, normalized identifier, visibility flags, optional localized content, an optional parent, and zero or more relations.

| Entry type | Typical use | Example identifier |
| --- | --- | --- |
| Category | Organize a story or content branch | `@Category:[main_story]` |
| Item | A Bukkit item stack | `@Vanilla:[diamond_sword]` |
| Entity | A Bukkit entity type or hooked mob | `@Vanilla:[zombie]` |
| Location | A world and coordinate | resolved by the location hook |
| Executable | A skill or command-like target | `@Vanilla:[command_spawn]` |
| Reference | A typed external object | `@Reference:[faction:iron_legion]` |
| Meta | Generic lore metadata | generated UUID / editor entry |

Parents are a single inheritance link. Relations are explicit, bidirectional graph edges with separate source-side and target-side text, for example `drops` / `is dropped by`.

Identifiers are the stable integration boundary. Names are for display and may change; commands, hooks, journal entries, and API consumers should prefer identifiers or UUIDs.

## Visibility and progression

The editor exposes `published` and `discoverable` flags. A player journal only accepts player-visible lore, and discovery is idempotent: discovering the same lore again does not create duplicate journal rows or fire another discovery pair.

An unpublished or non-discoverable entry can still be used by administrators and by configured AI context, but it should not be treated as player-facing content.

## Optional features

### Revisions

Revisions are enabled by default. Each meaningful save creates an immutable version, existing lore can receive a `MIGRATED` version during startup, and restoring an old version appends a new version rather than rewriting history. See [Configuration](configuration.md) and [API Information](api_information.md).

### AI authoring and NPCs

AI is disabled by default and requires both `AI.Enabled: true` and an explicit provider. Generated text enters the suggestion queue; it never becomes live lore automatically. NPC conversations additionally require `AI.NPC.Enabled: true` and a supported Citizens or FancyNpcs NPC profile. See [Commands](commands.md) and [Configuration](configuration.md).

### Resource-pack icons

When custom model data is enabled, Taleweaver generates `TaleweaverRP.zip`, assigns custom model data to lore icons, and can serve the pack from its embedded HTTP endpoint. Configure the delivery URL carefully if the server is behind a proxy or external host.

## Supported integrations

The current hook surface includes vanilla registries plus HeadDatabase, ModelEngine, Citizens, CraftEngine, Divinity, EcoItems, Fabled, FancyNpcs, Fusion, AuraSkills, Jobs, mcMMO, MyPet, MythicMobs, ItemsAdder, MMOItems, NotQuests, Nexo, Oraxen, Quests, Slimefun, MythicDungeons, and WorldGuard.

Integration availability is capability-based. A missing optional plugin does not prevent Taleweaver from loading; its handlers and discovery bridges are simply absent.

## Documentation map

| Section | Use it for |
| --- | --- |
| [Commands](commands.md) | Player and administrator command syntax, permissions, and workflows |
| [Configuration](configuration.md) | SQL, startup, journal, revisions, AI, resource packs, relations, and translations |
| [API Information](api_information.md) | Java integration, events, hooks, models, persistence behavior, and extension guidance |

## Operational boundaries

- SQL credentials are read at startup; restart after changing connection settings.
- Lore mutations should be performed on the server thread when called from another plugin.
- AI providers are lazy, but enabling Hugging Face local inference may download a model on the first request.
- Relation add/remove currently expose cancellable pre-events, not post-events.
- `LoreMeta<T>.value` is not persisted by the current editor metadata contract.
- Back up the MariaDB database before large imports, retention changes, or restores.
