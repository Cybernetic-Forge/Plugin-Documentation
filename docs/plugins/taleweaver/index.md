# Taleweaver

Taleweaver lets you link Minecraft items, creatures, locations, and plugin content into a shared story. Players discover entries during play and revisit them in a personal journal.

| Section | Description |
| --- | --- |
| [Commands](./commands/) | Player and admin commands, permissions, and publishing |
| [Configuration](./configuration/) | MariaDB, journal settings, revisions, resource packs, and provider settings |
| [API Information](./api_information/) | Lore models, events, custom references, and extension lifecycle |
| [AI & NPCs](./ai_and_npcs/) | Lore drafting, consistency checks, NPC knowledge, and actions |
| [Create & Edit Preview](./wizard_preview/) | Guided inventory creation and management, free-form identifiers, and bStats in development |

## Requirements

| Requirement | Value |
| --- | --- |
| Release covered | `1.2.2` |
| Server | Paper compatible with API `26.1.1` |
| Java | Java 25 or newer |
| Database | MariaDB reachable from the Paper server |
| Additional plugins | Optional. Install only the integrations your server uses |

## Install

1. Put the Taleweaver JAR in the server's `plugins` directory.
2. Start the server to generate `plugins/Taleweaver/config.yml`.
3. Set the MariaDB host, database, account, and password. The account needs access to the target schema and must be able to create or migrate Taleweaver's tables.
4. Restart and check the console for database, lore-cache, or hook-loading errors. Run `/lore help` in game to open the staff guide.

## Create a first discovery

1. On `1.2.2`, find a valid vanilla item reference with Tab after `/lore create item`. For example, use `/lore create item @Vanilla:[compass] Wayfarer's Compass`.
2. Add a description in the editor and check that **Published** and **Discoverable by Players** are both enabled. Save the changes.
3. Hold a matching compass and run `/journal inspect`, or discover the item through normal play. Check the result in `/journal`.

## How lore fits together

| Concept | Use |
| --- | --- |
| Reference | Attaches lore to content, such as an item, region, quest or skill |
| Free-form lore | Stores an authored entry without a game-object reference |
| Category | Groups entries into a branch of the library |
| Parent | Gives an entry one place in the hierarchy |
| Relationship | Connects two entries with text for each direction, such as “drops” and “is dropped by” |
| Discovery | Adds a published and discoverable entry to one player's journal |

Players can search their discovered entries, filter by type or category, mark favourites and keep private notes. Suggestions, revision history, AI, NPC conversations and generated resource-pack icons are optional. Free-form lore and categories need a discovery path, such as an integration calling the journal API.

## Integrations

| Content | Examples |
| --- | --- |
| Items | CraftEngine, Divinity, EcoItems, ItemsAdder, MMOItems, MythicMobs, Nexo, Oraxen, Slimefun |
| Creatures and NPCs | Citizens, FancyNpcs, ModelEngine, MythicMobs |
| Regions and dungeons | WorldGuard, MythicDungeons |
| Quests | NotQuests, Quests |
| Classes, skills and recipes | AuraSkills, Fabled, Fusion, Jobs, mcMMO, MyPet |
| Icons | HeadDatabase, generated resource-pack icons |

Available references, discovery events and auto-create support vary by hook. Taleweaver logs the active hooks at startup.
