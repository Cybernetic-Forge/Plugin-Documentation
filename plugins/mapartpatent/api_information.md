---
title: API Information
parent: MapArtPatent
nav_order: 3
has_toc: true
---

# MapArtPatent API Information

MapArtPatent does **not** provide a dedicated public API package or custom Bukkit events.

What it does expose is a small set of helper classes and a clear persistent-metadata contract that other plugins can read if they want to detect patented maps.

## Main Entry Point

The main plugin class is `net.maksy.mapartpatent.MapArtPatent`.

Public static accessors:

- `MapArtPatent.getInstance()`
- `MapArtPatent.getConfigManager()`
- `MapArtPatent.getEco()`

Meaning:

- `getInstance()` returns the running plugin instance.
- `getConfigManager()` returns the singleton config helper.
- `getEco()` returns the Vault `Economy` provider resolved at startup.

Example:

```java
import net.maksy.mapartpatent.MapArtPatent;
import net.milkbowl.vault.economy.Economy;

Economy eco = MapArtPatent.getEco();
if (eco != null) {
    double balance = eco.getBalance(player);
}
```

## `ConfigManager`

`ConfigManager` is the main runtime helper for reading plugin configuration and building GUI/lore output.

Useful methods:

- `init()`
- `reload()`
- `getDisplay(String path)`
- `getLore(String path, String replacable, String replaceValue, boolean state)`
- `getPatentedMapArt(Player player, ItemStack mapArt, boolean craftable, boolean usable)`
- `getCosts(String path)`

Typical uses:

- turning configured strings into Adventure `Component`s
- building GUI lore with `<costs>` and `<state>` replacements
- stamping final patent lore onto the patented map item
- reloading config at runtime

## Persistent Metadata Contract

The most useful integration surface is `PersistentMetaData`.

Supported helper methods:

- `setNameSpace(ItemMeta meta, String key, String value)`
- `setNameSpace(ItemMeta meta, String key, int value)`
- `setNameSpace(ItemMeta meta, String key, byte[] value)`
- `getNameSpaceString(ItemMeta meta, String key)`
- `getNameSpaceInt(ItemMeta meta, String key)`
- `getNameSpaceBytes(ItemMeta meta, String key)`
- `hasNameSpaceString(ItemMeta meta, String key)`
- `hasNameSpaceInt(ItemMeta meta, String key)`
- `hasNameSpaceBytes(ItemMeta meta, String key)`

The current key contract used by gameplay code is:

| Key | Type | Meaning |
| --- | --- | --- |
| `owner` | string | Owning player's UUID as a string. This is the main marker that a map is patented. |
| `craftable` | integer | Set to `1` when copy/crafting restrictions are enabled. |
| `usable` | integer | Set to `1` when item-frame use restrictions are enabled. |
| `mapview` | byte array | Reserved image payload support. Helper code exists, but the current gameplay flow does not actively use it. |

Example patented-map check:

```java
import net.maksy.mapartpatent.persistence.PersistentMetaData;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;

ItemMeta meta = item.getItemMeta();
boolean patented = meta != null && PersistentMetaData.hasNameSpaceString(meta, "owner");

if (patented) {
    String ownerUuid = PersistentMetaData.getNameSpaceString(meta, "owner");
}
```

## Listener-Enforced Behavior

MapArtPatent enforces its restrictions through normal Paper/Bukkit listeners, not through exported events.

Current listener coverage:

| Listener path | What it blocks or handles |
| --- | --- |
| `CraftItemEvent` | Blocks crafting patent-protected maps for non-owner players when `craftable = 1`. |
| `InventoryClickEvent` in cartography tables | Blocks cartography-table interaction for non-owner players when `craftable = 1`. |
| `CrafterCraftEvent` | Blocks auto-crafter copying when `craftable = 1`. |
| `PlayerItemFrameChangeEvent` | Blocks item-frame use for non-owner players when `usable = 1`. |
| Patent GUI listeners | Build the patent flow, charge Vault costs, and apply metadata/lore to the finished map. |

Important note:

- operators and players with `mapartpatent.admin` bypass these restrictions, even though `mapartpatent.admin` is not declared in `plugin.yml`.

## GUI Registry

`PatentGuiRegistry` is an internal runtime cache of one `PatentGui` per player.

Available methods:

- `PatentGuiRegistry.get()`
- `getPatentGui(Player player)`
- `unregister(Player player)`

This is useful to know if you are reading the code, but it is not really a stable external API contract.

## Optional Hook: HeadDatabase

`HeadDatabaseHook` stores a static `HeadDatabaseAPI` reference when the optional HeadDatabase plugin is present.

Practical effect:

- the confirm button can use a HeadDatabase head if available
- otherwise the plugin falls back to a normal `PLAYER_HEAD`

## No custom plugin events

MapArtPatent does not define custom events for:

- map patent creation
- restriction denial
- GUI confirm/cancel
- ownership transfer

If another plugin needs to react to these actions, it currently has to:

- inspect item metadata directly
- listen to the same normal Paper/Bukkit events
- or modify/fork MapArtPatent

## Practical integration notes

- The safest way to detect a patented map is checking for the `owner` string key on the item's persistent data container.
- `craftable = 1` and `usable = 1` should be treated as boolean-style flags.
- `MapArtPatent.getEco()` may be `null` if Vault or an economy provider is missing, even though Vault is declared as a dependency in `plugin.yml`.
- There is no formal ownership-transfer API; patent ownership is simply the stored UUID in metadata.

