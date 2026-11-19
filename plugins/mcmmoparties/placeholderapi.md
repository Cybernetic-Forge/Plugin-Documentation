# PlaceholderAPI

McMMOParties 0.3.0 includes a PlaceholderAPI expansion for Paper. Install [PlaceholderAPI](https://www.spigotmc.org/resources/placeholderapi.6245/) alongside McMMOParties on each Paper backend that resolves the placeholders, then restart the server. The expansion registers automatically.

For example, run `/papi parse me %mcmmoparties_party_name% (%mcmmoparties_party_level%)` in game, or add `Party: %mcmmoparties_party_name%` to a PlaceholderAPI-enabled scoreboard.

## Placeholder reference

Wrap each key below in `%mcmmoparties_` and `%`. For example, `party_name` becomes `%mcmmoparties_party_name%`.

| Key | Value |
| --- | --- |
| `party_count` | Number of loaded parties. Works without a player context. |
| `has_party` | Whether the player belongs to a party. |
| `player_party_count` | Number of parties the player belongs to. |
| `party_id` | Active party's internal ID. |
| `party_name` | Active party's display name. |
| `party_role` | Role identifier, such as `OWNER`, `CO_OWNER` or `MEMBER`. |
| `party_is_owner` | Whether the player owns the active party. |
| `party_owner_uuid` | Party owner's UUID. |
| `party_members` | Current member count. |
| `party_online_members` | Members online on this Paper backend. |
| `party_max_members` | Member capacity including buffs. |
| `party_free_slots` | Unused member slots. |
| `party_locked` | Whether the party is locked. |
| `party_level` | Current party level. |
| `party_level_cap` | Configured level cap, or `-1` for unlimited. |
| `party_level_capped` | Whether the party has reached its level cap. |
| `party_xp` | XP earned towards the next level. |
| `party_xp_total` | Lifetime party XP. |
| `party_xp_required` | XP required to complete the current level. |
| `party_xp_remaining` | XP still needed for the next level, or zero at the cap. |
| `party_xp_progress` | Progress towards the next level from 0 to 100, without a percent sign. A capped party returns 100. |
| `party_xp_sharing` | Whether skill XP sharing is enabled. |
| `party_xp_sharing_percent` | Configured XP share percentage. |
| `party_xp_sharing_radius` | Configured sharing radius in blocks. |
| `party_balance` | Party treasury balance. |
| `party_balance_limit` | Treasury limit, or `-1` for unlimited. |
| `party_buff_mode` | `LEVEL` or `SKILLPOINTS`. |
| `party_skill_points_total` | Total party skill points. |
| `party_skill_points_available` | Unspent party skill points. |
| `party_skill_points_spent` | Points spent on party buffs. |
| `party_dungeon_slots` | Dungeon capacity with MythicDungeons, or `-1` for unlimited. Empty when the integration is unavailable. |
| `party_can_use_waypoint` | Whether the player can access the party waypoint. |
| `party_can_use_treasury` | Whether the player can access the party treasury. |
| `party_can_use_chat` | Whether the player can access party chat. |
| `party_chat_mode` | Whether party chat mode is active for the player's active party on this backend. |

Party values follow the player's selected party. If the selection is unavailable, the first membership by party ID is used. Data refreshes every 20 server ticks. Boolean values are `true` or `false`. For a player without a party, the ownership and access flags, chat mode and `has_party` return `false`, `player_party_count` returns `0`, and party details return an empty string.

## Relational placeholder

`%rel_mcmmoparties_same_party%` returns `true` when the viewer and target have the same active party. Both players need a party. Use it in tools with relational PlaceholderAPI support, for example in a [TAB condition](https://github.com/NEZNAMY/TAB/wiki/Placeholders) that compares the value with `true` to mark party members.
