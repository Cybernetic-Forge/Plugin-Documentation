---
title: Commands
parent: Taleweaver
nav_order: 1
has_toc: true
---

# Taleweaver Commands

Commands are player-facing and open the plugin's GUIs where an operation needs structured input. All references accept a lore identifier, a lore name, or a UUID where resolution is supported. Several commands also accept contextual aliases such as `held`, `entity`, and `location`.

## Permissions

| Permission | Default | Purpose |
| --- | --- | --- |
| `taleweaver.lore` | Operator | Open and manage the lore catalogue |
| `taleweaver.journal` | Everyone | Use the personal journal |
| `taleweaver.suggest` | Everyone | Submit player description suggestions |
| `taleweaver.review` | Operator | Review and apply/reject suggestions |
| `taleweaver.ai` | Operator | Use AI authoring, audits, and NPC setup |
| `taleweaver.ai.npc.interact` | Everyone | Talk to configured AI NPCs |
| `taleweaver.versions.view` | Operator | View revision history and comparisons |
| `taleweaver.versions.restore` | Operator | Restore a previous revision |

The command declarations themselves gate `/lore` with `taleweaver.lore` and `/journal` with `taleweaver.journal`. AI NPC interaction is separately checked at interaction time.

## `/lore`

### Open and inspect lore

```text
/lore show
/lore show <reference>
/lore info
/lore info <reference>
```

`show` opens the icon-first lore browser. Without a reference it opens the catalogue; with a reference it opens the corresponding branch. Shift-left-clicking an entry opens its editor. The browser separates hierarchy from explicit relations and can reveal technical details such as identifiers and UUIDs.

`info` prints compact information for the held item, targeted entity, and current location when no reference is supplied. With a reference it prints information for that entry.

Supported contextual references include:

| Alias | Resolution |
| --- | --- |
| `held` / `item` | Lore for the item in the main hand |
| `entity` / `target` / `look` | Lore for the entity being looked at |
| `location` / `here` | Lore for the current location |

### Create lore

```text
/lore create category <name>
/lore create meta <name>
/lore create <reference-type> <reference-value> <name>
/lore create reference <reference-type> <reference-value> <name>
```

The short form is preferred for registered reference types. The `reference` form is retained for compatibility. After creation, Taleweaver opens the editor so the author can set description, visibility, localized content, and other available fields.

Examples:

```text
/lore create category Main Story
/lore create quest ancient_ruins Ancient Ruins
/lore create faction iron_legion Iron Legion
```

Reference values are validated by the registered handler. A duplicate resolved identifier is rejected.

### Edit and reload

```text
/lore edit <reference>
/lore reload
```

`edit` opens the editor for an existing entry. `reload` reloads configuration, AI providers, lore rows, relations, and the in-memory cache. SQL host, database, username, password, and port are read when the SQL manager starts; restart after changing those settings.

### Parent / inheritance

```text
/lore parent set <child> <parent>
/lore parent remove <child>
```

A child inherits context from one parent. A lore entry cannot be its own parent. Removing a lore entry also clears its parent link and removes child links pointing at it.

### Directional relations

```text
/lore relation set <source> <target>
/lore relation remove <source> <target>
```

`set` opens the relation-text dialog. Choose a source-side sentence and a target-side sentence, such as `drops` / `is dropped by`. `remove` deletes both directions of the stored edge. Relation text presets and auto-create defaults are configured in `relations.yml`.

### Auto-create

```text
/lore auto-create Vanilla
/lore auto-create MythicMobs ItemsAdder MMOItems
```

Auto-create imports lore and relation candidates from the selected enabled hooks. The operation runs in two phases:

1. handlers gather work asynchronously;
2. creation and relation writes execute in main-thread batches of 25.

Progress, skipped operations, and failures are reported in chat and logged. Use only hooks that are installed and enabled; invalid names are ignored with feedback.

### Suggestions and review

```text
/lore review
```

Players submit suggestions from a discovered journal entry when they have `taleweaver.suggest`. Operators open the review queue with `/lore review` and can compare the original-at-submission description, the current live description, and the proposed text.

Applying a suggestion checks the base description captured at submission time. If an administrator changed the live description meanwhile, the suggestion becomes `STALE` and cannot overwrite the newer edit.

### AI commands

AI commands require `taleweaver.ai`, `AI.Enabled: true`, and a valid configured provider except for `status` and `usage`, which are useful for diagnosing setup.

```text
/lore ai status
/lore ai usage
/lore ai generate <kind> <reference> <prompt>
/lore ai check
/lore ai check <reference>
/lore ai npc-setup
/lore ai npc-stop
/lore ai function-setup [function-id]
```

Generation kinds:

```text
description | biography | relations | rumor | book | dialogue
```

Generated content is submitted as a reviewable suggestion; it is not saved directly to the lore table. `check` audits either the complete catalogue or one target and reports semantic, factual, inheritance, and relation conflicts. Warnings are not persisted.

`npc-setup` configures the NPC you are looking at. `function-setup` edits a reusable NPC function. `npc-stop` is available to end the current conversation and is handled before the administrator permission check so an interacting player can stop their own session.

## `/journal`

```text
/journal
/journal all
/journal unread
/journal favorites
/journal recent
/journal search <text>
/journal open <reference>
/journal inspect
```

| Subcommand | Behavior |
| --- | --- |
| no argument / `all` | Open all discovered, player-visible entries |
| `unread` | Show entries not yet opened |
| `favorites` | Show entries marked as favourites |
| `recent` | Show newest discoveries first |
| `search <text>` | Search names, descriptions, identifiers, and private notes |
| `open <reference>` | Open one discovered entry by identifier, name, or UUID |
| `inspect` | Discover lore for the held item, targeted entity, and current location |

Opening an entry marks it read once. The entry dialog supports favourite toggling, private notes, relation browsing, and a description suggestion action. Notes are stored per player and are never visible to other players.

`inspect` uses a ten-block entity target range and the current location. It discovers matching player-visible lore with source `journal:inspect`; if the lore is already known, it opens the known entry instead.

## Typical content-authoring session

```text
/lore auto-create MythicMobs
/lore show
/lore edit @MythicMobs:ancient_guardian
/lore parent set @MythicMobs:ancient_guardian @Category:[main_story]
/lore relation set @MythicMobs:ancient_guardian @Reference:[quest:ancient_ruins]
/lore ai generate description @MythicMobs:ancient_guardian Write a concise in-world description.
/lore review
```

Use the AI command only when the provider is configured. The final `/lore review` step is always required for generated text.
