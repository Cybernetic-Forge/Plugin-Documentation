# Taleweaver Commands

This reference covers release `1.2.2`. The development branch's inventory-based create and edit flow is described in **Create & Edit Preview**.

## Player Commands

| Command | Description | Permission |
| --- | --- | --- |
| `/journal help [topic]` | Shows journal help and examples. | Everyone |
| `/journal [all]` | Opens the journal and its type and category filters. | `taleweaver.journal` |
| `/journal unread` | Shows unread entries. | `taleweaver.journal` |
| `/journal favorites` | Shows entries marked as favourites. | `taleweaver.journal` |
| `/journal recent` | Shows recent discoveries first. | `taleweaver.journal` |
| `/journal search <text>` | Searches discovered entries. | `taleweaver.journal` |
| `/journal inspect` | Checks the item in your hand, targeted entity and current location for visible lore. If there are matches and no new discoveries, it attempts to open the first match. | `taleweaver.journal` |
| `/journal open <reference>` | Opens a specific visible entry you already discovered. | `taleweaver.journal` |

The journal detail dialog lets you mark a favourite or write a private note. With player suggestions enabled, it also offers a way to propose a new description. Only discovered and visible related entries appear in the journal.

While speaking to an AI NPC, `/lore ai npc-stop` stops the conversation for staff with `taleweaver.lore`. Players can also end the session by leaving its configured interaction range.

## Admin Commands

| Command | Description | Permission |
| --- | --- | --- |
| `/lore` or `/lore help [topic]` | Opens help for the lore commands and workflows. | Everyone |
| `/lore show [reference]` | Opens the library or focuses a selected entry. | `taleweaver.lore` |
| `/lore info [reference]` | Shows the name, type and UUID of a match. With no reference, inspects your held item, target and location. | `taleweaver.lore` |
| `/lore create category [name]` | Creates a category and opens its editor. | `taleweaver.lore` |
| `/lore create meta [name]` | Creates free-form lore and opens its editor. | `taleweaver.lore` |
| `/lore create <type> <value> [name]` | Creates an entry attached to a supported reference. | `taleweaver.lore` |
| `/lore edit <reference>` | Opens the detail editor for an existing entry. | `taleweaver.lore` |
| `/lore parent set <entry> <parent>` | Places an entry under another lore entry. | `taleweaver.lore` |
| `/lore parent remove <entry>` | Moves the entry to the top level. | `taleweaver.lore` |
| `/lore relation set <source> <target>` | Opens the relation preset dialog for a pair of entries. | `taleweaver.lore` |
| `/lore relation remove <source> <target>` | Removes the relationship in both directions. | `taleweaver.lore` |
| `/lore auto-create <hook> [hook...]` | Collects content from the selected integrations and processes entry and relation creation in batches. | `taleweaver.lore` |
| `/lore review` | Opens the queue for player suggestions and AI drafts. | `taleweaver.lore` and `taleweaver.review` |
| `/lore reload` | Reloads the main config, help, AI setup and lore cache. | `taleweaver.lore` |

Help also works as text in the server console. Operational commands require an in-game player. `/lore create` without arguments opens the create help topic in `1.2.2`. The older form `/lore create reference <type> <value> [name]` is also accepted in this release.

### Choosing a reference

Use a UUID, exact identifier, or exact title where the command resolves an existing entry. Use UUIDs for duplicate titles. Titles with spaces work in commands that take a single trailing reference. For commands with several arguments, use identifiers or UUIDs to keep each reference in one argument.

| Shortcut | Resolves to |
| --- | --- |
| `held`, `item` | Lore for the item in your main hand |
| `entity`, `target`, `look` | Lore for the targeted entity |
| `location`, `here` | Lore for your current location |

The create command offers active reference types and supported values through Tab completion. For example, `/lore create item @Vanilla:[compass] Wayfarer's Compass` creates a reference with a custom title. A reference can already have a lore entry. Use the edit command when it does.

### Browser, publishing and review

- Left-click an entry to browse its hierarchy or relations. Right-click opens relations when available. Shift-left-click opens the editor.
- **Technical details** reveals identifiers and UUIDs. Both **Published** and **Discoverable by Players** must be enabled for players to see and discover an entry.
- Publishing enables discovery through the appropriate mechanic. Each player earns their own discovery.
- With revisions enabled, use **Version history** on a focused entry to compare earlier versions. Restoration asks for confirmation and records a new revision.
- The review queue compares the current, original and proposed descriptions. Applying a suggestion rechecks its original base. Reviewers can reject an outdated or unsuitable proposal.

## AI Commands

These subcommands require both `taleweaver.lore` and `taleweaver.ai`, except `npc-stop` as noted above. See **AI & NPCs** for the provider and NPC setup workflow.

| Command | Description |
| --- | --- |
| `/lore ai status` | Shows the configured provider and availability. |
| `/lore ai usage` | Reports your recorded and estimated token usage for the last hour. |
| `/lore ai generate <kind> <reference> <prompt>` | Creates a reviewable draft. Kinds include `description`, `biography`, `relations`, `rumor`, `book`, and `dialogue`. |
| `/lore ai check [reference]` | Checks the configured lore context for possible consistency issues. |
| `/lore ai npc-setup` | Opens setup for the targeted supported NPC. |
| `/lore ai function-setup [function-id]` | Opens the NPC function editor. |
| `/lore ai npc-stop` | Ends your current NPC conversation. |

Use a single-token reference or the detail editor's AI button for generation. The command treats the remaining arguments as the prompt.

## Permission defaults

| Permission | Default | Purpose |
| --- | --- | --- |
| `taleweaver.lore` | Operator | Lore catalogue and staff commands |
| `taleweaver.journal` | Everyone | Discover and browse personal lore |
| `taleweaver.suggest` | Everyone | Propose descriptions when `Journal.PlayerSuggestionsEnabled` is enabled |
| `taleweaver.review` | Operator | Review player proposals and AI drafts |
| `taleweaver.ai` | Operator | AI authoring, usage, audits and NPC configuration |
| `taleweaver.ai.npc.interact` | Everyone | Speak to an enabled, configured AI NPC |
| `taleweaver.versions.view` | Operator | View revision history when enabled |
| `taleweaver.versions.restore` | Operator | Restore revisions when enabled |
