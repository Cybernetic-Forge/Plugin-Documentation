# Create & Edit Preview

These workflows describe the [create/edit development branch](https://github.com/Cybernetic-Forge/Taleweaver/tree/f720f1bbc59fe900a2bc0c825c964d6add82d652). Release `1.2.2` uses the text-based create commands described in **Commands**.

## Create an entry

Run `/lore create` as an in-game player with `taleweaver.lore`.

| Step | Action |
| --- | --- |
| Choose lore | Select Item, Entity, Location, Free-form lore, or Plugin & server content. Free-form lore offers an entry or a category. |
| Choose a source | Choose Vanilla or an active hook. If the provider exposes multiple matching types, choose the type. Registered Dev API hooks appear automatically. |
| Choose content | Search or page through the catalog. The wizard can use the captured held item, compatible inventory items, targeted entity or position. Hooks with a resolver can also offer manual reference entry. |
| Edit details | Adjust the title, description, and visibility. Items and hooks can prefill content. Selecting a reference that already has lore opens the existing detail editor. |
| Review & connect | Choose an optional parent and any related lore. Search connection candidates and filter the relationship list to selected entries. Select **Create lore** to persist the entry. |

Taleweaver captures your inventory, target and position when the wizard opens. Hold or face the intended object before entering the command. Until confirmation, the entry remains a draft. Existing scripts that previously passed type and value arguments to `/lore create` now open the wizard and should use the Java API for programmatic creation.

## Manage existing lore

| Entry point | Result |
| --- | --- |
| `/lore edit` | Opens the picker with context shortcuts and **Browse lore**. |
| `/lore edit <reference>` | Opens **Manage lore** for the matching entry. |
| **Manage lore** in the browser | Opens the same view for the focused entry. |
| Shift-left-click an entry in the browser | Opens the text editor directly. |

**Manage lore** shows the entry's title, visibility, parent and number of relationships. **Edit details** opens the text editor. **Change hierarchy** lets you select or remove a parent and prevents cycles. **Manage relationships** lists connections and supports adding a relation with the configured presets or removing it with confirmation.

## Find free-form entries

Free-form entries without a custom identifier use `@Lore:<UUID>`, including older entries. Their identifier survives a rename.

- Type `/lore edit @Lore` and press Tab to see matching identifiers.
- Open **Browse lore** to search by title, type, or identifier.
- Use **Technical details** in the browser to see an entry's UUID and identifier.

## bStats

This branch includes standard bStats metrics for Taleweaver under plugin ID `35524`. Collection follows the shared server setting in `plugins/bStats/config.yml`. Set `enabled: false` there to disable bStats server-wide.
