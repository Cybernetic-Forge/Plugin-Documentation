# MapArtPatent Commands

Primary command roots:

- `/mapart`
- `/mapinfo`

## User Commands

| Command | Description | Permission |
| --- | --- | --- |
| `/mapart` | Opens the patent GUI, where a player can insert a filled map and optionally enable anti-copy or anti-use restrictions. | `mapart.use` |
| `/mapinfo` | Shows the lore of the patented filled map in the item frame the player is currently looking at. | None |

## Admin Commands

| Command | Description | Permission |
| --- | --- | --- |
| `/mapart reload` | Reloads `config.yml` from disk. | `mapart.reload` |

## Notes

- Both commands are player-only. Console senders are ignored.
- `/mapinfo` checks the entity the player is targeting within `5` blocks and only works on an item frame holding a patented filled map.
- `/mapinfo` has no explicit permission check in code.
- The runtime restriction bypass checks for operator status **or** the permission `mapartpatent.admin`, but that permission is not declared in `plugin.yml`.
- Operators and `mapartpatent.admin` holders bypass map restrictions on crafting, cartography-table use, and item-frame use.
