---
title: Commands
parent: AbyssalDao
nav_order: 1
has_toc: true
---

# AbyssalDao Commands

Primary command aliases:

- Main command: `/dao`
- Alias: `/tao`

## Player Commands

| Command | Description | Permission |
| --- | --- | --- |
| `/dao choose <element>` | Permanently chooses your elemental affinity if you have not chosen one yet. | None |
| `/dao info` | Shows your current affinity, Tao level, recorded skill count, and current realm. | None |
| `/dao help` | Opens the in-game help GUI on page 1. | None |
| `/dao help <page>` | Opens the configured help GUI on the requested page. | None |
| `/dao record start <name>` | Starts recording a new personal skill chain. | None |
| `/dao record stop` | Saves the current recording into a recorded skill if at least one step was captured. | None |
| `/dao record cancel` | Cancels the active recording session without saving it. | None |
| `/dao skills` | Opens the skills GUI for recorded skills and configured external skills. | None |
| `/dao cast <skill>` | Casts a recorded skill by name, or a configured external MythicMobs/Fabled skill by id. | None |
| `/dao cast bind <skill> <combo>` | Binds a recorded or external skill to a custom `L`/`R` combo. | None |
| `/dao cast unbind <combo>` | Removes a custom combo binding. | None |
| `/dao cast bindings` | Lists your currently saved custom skill bindings. | None |

## Cultivation Commands

| Command | Description | Permission |
| --- | --- | --- |
| `/dao cultivate status` | Shows realm, level, XP, insight, mastery, focus, instability, and breakthrough cooldown status. | None |
| `/dao cultivate methods` | Lists cultivation methods available for your current affinity and marks the active method. | None |
| `/dao cultivate method <id>` | Selects a cultivation method by id. | None |
| `/dao cultivate meditate` | Starts or stops meditation, depending on your current state and active method style. | None |
| `/dao cultivate stop` | Force-stops meditation. | None |
| `/dao cultivate breakthrough` | Attempts a breakthrough if all XP, insight, mastery, and cooldown requirements are met. | None |
| `/dao cultivate env` | Shows whether your current surroundings are favorable, neutral, or hindering, plus the matching environment lists. | None |

## Skill Tree Commands

| Command | Description | Permission |
| --- | --- | --- |
| `/dao tree` | Opens the current affinity skill tree GUI on page 1. | None |
| `/dao tree open` | Opens the current affinity skill tree GUI on page 1. | None |
| `/dao tree open <page>` | Opens the skill tree GUI on the requested page. | None |
| `/dao tree status` | Shows unlocked node count for your current elemental tree. | None |
| `/dao tree nodes` | Lists all nodes in your current tree with `Unlocked`, `Available`, or `Locked` status. | None |
| `/dao tree unlock <node>` | Attempts to unlock the named node and reopens the GUI on that node's page if successful. | None |

## Instability Commands

| Command | Description | Permission |
| --- | --- | --- |
| `/dao instability` | Shows current instability tier, remaining duration, and active instability mode. | None |
| `/dao instability status` | Shows current instability tier, remaining duration, and active instability mode. | None |
| `/dao instability suppress` | Switches instability into `SUPPRESSED` mode. | None |
| `/dao instability embrace` | Switches instability into `EMBRACED` mode. | None |
| `/dao instability reset` | Returns instability mode to `NEUTRAL`. | None |

## Admin Commands

| Command | Description | Permission |
| --- | --- | --- |
| `/dao admin reset <player>` | Resets a player's affinity and clears their active recording/combat state. | `abyssaldao.admin` |
| `/dao admin level <player> <level>` | Sets a player's Tao progression level, bounded by `progression.max-level`. | `abyssaldao.admin` |
| `/dao admin add-exp <player> <amount>` | Adds cultivation XP. | `abyssaldao.admin` |
| `/dao admin remove-exp <player> <amount>` | Removes cultivation XP, but never below `0`. | `abyssaldao.admin` |
| `/dao admin set-exp <player> <amount>` | Sets cultivation XP directly. | `abyssaldao.admin` |
| `/dao admin add-insight <player> <amount>` | Adds cultivation insight. | `abyssaldao.admin` |
| `/dao admin remove-insight <player> <amount>` | Removes cultivation insight, but never below `0`. | `abyssaldao.admin` |
| `/dao admin set-insight <player> <amount>` | Sets cultivation insight directly. | `abyssaldao.admin` |
| `/dao admin add-mastery <player> <amount> [method]` | Adds mastery XP to the specified cultivation method, or to the player's active/default method if omitted. | `abyssaldao.admin` |
| `/dao admin remove-mastery <player> <amount> [method]` | Removes mastery XP from the specified cultivation method, but never below `0`. | `abyssaldao.admin` |
| `/dao admin set-mastery <player> <amount> [method]` | Sets mastery XP for the specified cultivation method. | `abyssaldao.admin` |
| `/dao admin add-focus <player> <amount>` | Adds focus, capped by the player's effective focus maximum. | `abyssaldao.admin` |
| `/dao admin remove-focus <player> <amount>` | Removes focus, but never below `0`. | `abyssaldao.admin` |
| `/dao admin set-focus <player> <amount>` | Sets focus directly, capped by the player's effective focus maximum. | `abyssaldao.admin` |
| `/dao admin set-instability-minutes <player> <minutes>` | Applies instability for the given number of minutes. | `abyssaldao.admin` |
| `/dao admin clear-instability <player>` | Clears current instability completely. | `abyssaldao.admin` |
| `/dao admin reload` | Reloads YAML-backed configuration, messages, and config-driven services. | `abyssaldao.admin` |

## Notes

- All non-admin command branches are player-only. Console senders are rejected with the configured `general.players-only` message.
- `/dao admin reload` is the only admin action that does not require a player target, so it is also the only admin branch that is practically useful from console.
- Targeted admin commands only work on **online** players because the handler uses `Bukkit.getPlayerExact(...)`.
- `/dao choose <element>` can only be used once per player until an admin resets the profile with `/dao admin reset <player>`.
- `/dao cast bind <skill> <combo>` only accepts `L`/`R` sequences up to `skill-casting.max-combo-length`. Prefix-conflicting custom bindings are rejected, but an exact match with a built-in combo is allowed and intentionally overrides that combo for the player.
- `/dao cultivate meditate` only succeeds when the active cultivation method is meditative. `COMBAT` methods are not meditative.
- `/dao instability ...` only works while the player is currently unstable. If instability is inactive, the command reports that state instead of changing modes.
- `/dao admin reload` hot-reloads the YAML-driven systems, but changing `storage.yml` backend settings still requires a full restart.

