---
title: Configuration
parent: MapArtPatent
nav_order: 2
has_toc: true
---

# MapArtPatent Configuration

MapArtPatent uses a single main configuration file:

- `config.yml`: GUI titles, button text, patent costs, patented-map lore, and language strings

## Example `config.yml`

```yaml
Gui:
  Title: "MapArt Patenting"

  States:
    Active: "&7[&aActivated&7]"
    Unactive: "&7[&cDeactivated&7]"

  Buttons:
    Confirm:
      Display: "&7[&aConfirm&7]"
      Lore:
        - "&7Total costs: &a<costs>"
    Insert:
      Display: "&aInsert MapArt"
      Lore: []
    Craftability:
      Costs: 2000
      Display: "&9Prevent Copy"
      Lore:
        - "<state>"
        - " "
        - "&7Costs: &a<costs>"
    Usability:
      Costs: 1000
      Display: "&9Prevent Usage"
      Lore:
        - "<state>"
        - " "
        - "&7Costs: &a<costs>"
    Exit:
      Display: "&cCancel"
      Lore: []

MapArt:
  Lore:
    - " "
    - "&8Creator: &a<player>"
    - "&8Copyable: <craft_state>"
    - "&8Usable: <use_state>"
    - " "

Language:
  no_permission: "&4&lX &cYou don't have permission to perform that command"
  no_mapart: "&4&lX &cThis is not a filled Map"
  not_allowed: "&4&lX &cYou aren't allowed to use this map"
  not_enough_money: "&4&lX &cYou don't have enough money"
  already_patented: "&4&lX &cThis map is already protected!"
  inventory_full: "&4&lX &cYour inventory was full"
  finish: "&bYou successfully patented your map!"
```

## `config.yml` Reference

| Path | Type | Default | Description |
| --- | --- | --- | --- |
| `Gui.Title` | string | `MapArt Patenting` | Inventory title shown for the patent GUI. |
| `Gui.States.Active` | string | `&7[&aActivated&7]` | Text substituted when a toggle is active. |
| `Gui.States.Unactive` | string | `&7[&cDeactivated&7]` | Text substituted when a toggle is inactive. |
| `Gui.Buttons.Confirm.Display` | string | `&7[&aConfirm&7]` | Confirm button display name. |
| `Gui.Buttons.Confirm.Lore` | string list | `["&7Total costs: &a<costs>"]` | Confirm button lore. Supports `<costs>`. |
| `Gui.Buttons.Insert.Display` | string | `&aInsert MapArt` | Insert slot button display name. |
| `Gui.Buttons.Insert.Lore` | string list | `[]` | Insert slot lore. |
| `Gui.Buttons.Craftability.Costs` | decimal | `2000` | Extra Vault cost to apply the anti-copy restriction. |
| `Gui.Buttons.Craftability.Display` | string | `&9Prevent Copy` | Anti-copy toggle display name. |
| `Gui.Buttons.Craftability.Lore` | string list | see file | Lore for the anti-copy toggle. Supports `<state>` and `<costs>`. |
| `Gui.Buttons.Usability.Costs` | decimal | `1000` | Extra Vault cost to apply the anti-use restriction. |
| `Gui.Buttons.Usability.Display` | string | `&9Prevent Usage` | Anti-use toggle display name. |
| `Gui.Buttons.Usability.Lore` | string list | see file | Lore for the anti-use toggle. Supports `<state>` and `<costs>`. |
| `Gui.Buttons.Exit.Display` | string | `&cCancel` | Exit button display name. |
| `Gui.Buttons.Exit.Lore` | string list | `[]` | Exit button lore. |
| `MapArt.Lore` | string list | see file | Lore applied to the patented filled map. Supports `<player>`, `<craft_state>`, and `<use_state>`. |
| `Language.no_permission` | string | configured text | Sent when the player lacks `/mapart` or `/mapart reload` permission. |
| `Language.no_mapart` | string | configured text | Sent when the item is not a valid filled map target. |
| `Language.not_allowed` | string | configured text | Sent when a restricted map action is blocked. |
| `Language.not_enough_money` | string | configured text | Sent when the player cannot afford the selected patent options. |
| `Language.already_patented` | string | configured text | Sent when a player tries to patent a map that already has an owner marker. |
| `Language.inventory_full` | string | configured text | Sent when the patented map must be dropped because the inventory is full. |
| `Language.finish` | string | configured text | Sent after a successful patenting operation. |

## Placeholder Support

The plugin replaces the following placeholders:

| Placeholder | Used in | Meaning |
| --- | --- | --- |
| `<costs>` | Confirm, Craftability, and Usability lore | Total or per-toggle Vault price shown to the player. |
| `<state>` | Craftability and Usability lore | Active or inactive marker from `Gui.States.*`. |
| `<player>` | `MapArt.Lore` | Patenting player's name. |
| `<craft_state>` | `MapArt.Lore` | Final copy restriction state text. |
| `<use_state>` | `MapArt.Lore` | Final use restriction state text. |

## Restriction Flags

MapArtPatent stores patent data inside the filled map's persistent data container and uses two optional restriction flags:

| GUI toggle | Stored marker | Effect |
| --- | --- | --- |
| `Prevent Copy` | `craftable = 1` | Blocks copying/patent bypass through normal crafting, cartography table interaction, and auto-crafter crafting for non-owner players. |
| `Prevent Usage` | `usable = 1` | Blocks non-owner players from using the patented map in item frames. |

The owner itself is stored as:

- `owner = <player UUID>`

## GUI Behavior

The patent GUI is a fixed 27-slot inventory with these important slots:

- slot `10`: confirm
- slot `11`: inserted map
- slot `13`: anti-copy toggle
- slot `14`: anti-use toggle
- slot `16`: exit

Behavior notes:

- The inserted map must be a `FILLED_MAP`.
- Already patented maps are rejected.
- The map is cloned, tagged, and returned to the player on confirm.
- If the player's inventory is full, the finished map is dropped at the player's location.
- Vault is used for balance checks and withdrawals.

## Dependencies and practical notes

- `Vault` is a hard dependency and is used for all balance checks and charging.
- `HeadDatabase` is optional and is only used for custom GUI heads. Without it, the GUI falls back to a normal player head item.
- Color codes use `&` in the config and are converted into in-game section-sign formatting by the plugin.
- `/mapart reload` only reloads this one config file; there are no separate language or GUI files.

