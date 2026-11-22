---
title: API Information
parent: Taleweaver
nav_order: 3
has_toc: true
---

# Taleweaver API Information

Taleweaver exposes a Java API for integrations that want to create lore, resolve hooked objects, listen to lifecycle events, add custom reference namespaces, or provide AI chat backends.

The main packages are:

```text
net.maksy.taleweaver.taleweaver.api
net.maksy.taleweaver.taleweaver.api.events
net.maksy.taleweaver.taleweaver.core.models
net.maksy.taleweaver.taleweaver.core.models.ontologies
net.maksy.taleweaver.taleweaver.hooks
net.maksy.taleweaver.taleweaver.config.ai
net.maksy.taleweaver.taleweaver.modules.ai
net.maksy.taleweaver.taleweaver.modules.journal
net.maksy.taleweaver.taleweaver.modules.revisions
net.maksy.taleweaver.taleweaver.modules.suggestions
```

Add `Taleweaver` as a soft dependency in the integrating plugin and guard calls with a runtime enabled check. Do not load Taleweaver-only classes during plugin construction if Taleweaver is optional.

Use the Taleweaver JAR as a compile-time dependency and let Paper load the installed plugin at runtime. Since the package refactor, types moved out of the old `ai`, `journal`, `revisions`, and `suggestions` packages. Update imports and recompile integrations that reference those types. The public manager entry point class names remain available.

## Core access points

The plugin currently uses singleton-style accessors:

```java
Taleweaver.lore();
Taleweaver.hooks();
Taleweaver.journal();
Taleweaver.gui();
Taleweaver.ai();
Taleweaver.npcAi();
Taleweaver.sql();
Taleweaver.resourcePack();
```

`LoreManager` is the central API. Common operations include:

```java
LoreManager lore = Taleweaver.lore();

LoreCategory category = lore.createCategory("Main Story", LoreEventContext.of(this));
LoreReference reference = lore.createReference(
        "Iron Legion", "faction", "iron_legion", LoreEventContext.of(this)
);

Loreable entry = lore.findLore("@Reference:[faction:iron_legion]");
lore.setParent(reference, category, LoreEventContext.of(this));
lore.addRelation(reference, category, "belongs to", "contains", LoreEventContext.of(this));
```

Mutation methods fire the corresponding events, update the in-memory cache, persist the change, and request resource-pack regeneration when relevant. Prefer these methods over writing directly to the database.

## Lore model

All concrete entries extend `Loreable`:

| Class | Use | Editor fields |
| --- | --- | --- |
| `LoreCategory` | Organizational grouping | common fields |
| `LoreItem` | Bukkit `ItemStack` | `item` |
| `LoreEntity` | Bukkit `EntityType` | `entityType` |
| `LoreLocation` | World/coordinates/server | `server`, `world`, `x`, `y`, `z` |
| `LoreExecutable` | Skills or commands | `executable` |
| `LoreReference` | Typed external object | `referenceType`, `referenceValue` |
| `LoreMeta<T>` | Generic metadata | value is currently runtime-only |

Shared content includes name, description, normalized identifier, parent, relations, `published`, `discoverable`, and localized name/description overrides. Locale keys normalize to lowercase hyphenated tags, for example `de_DE` becomes `de-de`.

Use `getEditorValues()` / `applyEditorValues(...)` as the serialization contract for subtype fields. If adding a subtype, persistence also needs type handling in the lore table materializer.

## Identifier resolution

Identifiers are normalized by replacing whitespace with underscores. Built-in forms include:

```text
@Vanilla:[diamond_sword]
@Vanilla:[zombie]
@Category:[main_story]
@Reference:[faction:iron_legion]
```

The `quest`, `skill`, and `command` reference types have special resolution paths. Other reference types first consult registered handlers and then fall back to `@Reference:[type:value]` when applicable.

Useful resolution methods:

```java
lore.findLore("@Reference:[faction:iron_legion]");
lore.findLore(uuid);
lore.getByIdentifier(identifier);
lore.getReferenceIdentifier("faction", "iron_legion");
lore.getLoreByItem(itemStack, null);
lore.getLoreByEntity(entity);
lore.getLoreByLocation(location, null);
```

Names are not stable identifiers. Persist identifiers or UUIDs in integration data.

## Custom reference namespaces

Use `LoreReferenceBuilder` for a new namespace that does not need a full low-level hook:

```java
new LoreReferenceBuilder()
        .plugin(this)
        .referenceType("faction")
        .identifierPrefix("@MyFactions")
        .availableReferenceValues(() -> factionService.ids())
        .iconMaterialResolver((identifier, value) -> Material.WHITE_BANNER)
        .resourcePackIcon("icons/faction.png")
        .register();
```

The builder requires `referenceType` and either `identifierPrefix(...)` or `identifierResolver(...)`. Optional suppliers provide tab completion and icon resolution. A `resourcePackIcon` path must point to a PNG available through the registering plugin's resources.

Register after both plugins are enabled. The custom type then participates in `/lore create`, reference resolution, icons, and resource-pack regeneration.

On the Create & Edit preview branch, the wizard groups builder hooks by the plugin passed to `plugin(...)` and then by type. Supply `availableReferenceValues(...)` for browsing. A builder can also provide editable defaults via `creationDefaults((identifier, value) -> new IHookedReference.CreationDefaults(title, description))`.

## Low-level hooks

Implement `IHookedReference` when identifier detection depends on runtime Bukkit objects or custom auto-create behavior:

```java
public final class FactionHook implements IHookedReference {
    @Override
    public String getReferenceType() { return "faction"; }

    @Override
    public String getIdentifier(String value) {
        return "@MyFactions:" + value.trim().replace(' ', '_');
    }

    @Override
    public void autoCreate(HookType... hooks) {
        // Queue create/relation candidates through the integration's data source.
    }
}

FactionHook hook = new FactionHook();
LoreManager.registerReferenceHandler(hook);
```

The interface can resolve strings, `ItemStack`, `Entity`, and `Location` values, expose available values, and provide icon items/materials. Register through the specific `registerItemHandler`, `registerEntityHandler`, `registerLocationHandler`, or `registerReferenceHandler` method when the intent is clear.

Supply `getAvailableReferenceValues()` for a low-level hook that exposes a catalogue. On the preview branch, low-level hooks can override `getCreationSource()`, `resolveCreationIdentifier(String)`, `getCreationDefaults(String, String)`, and `isAvailableForCreation()`. Keep your registered handler instance and unregister it with `LoreManager.unregisterHandler(hook)` when your integration is disabled.

For integrations that know cross-object relationships, implement `IAutoCreateRelationsHook` and provide `autoCreateRelations(HookType... hooks)`. Use `HookAutoCreateUtil` helpers to create item, entity, location, reference, skill, and relation operations consistently.

## Events

Events live in `net.maksy.taleweaver.taleweaver.api.events`.

### Cancellable pre-events

```text
LoreCreateEvent
LoreUpdateEvent
LoreDeleteEvent
LoreRelationAddEvent
LoreRelationRemoveEvent
LoreDiscoverEvent
LoreRevisionRestoreEvent
```

### Post-events and notifications

```text
LoreCreatedEvent
LoreUpdatedEvent
LoreDeletedEvent
LoreReloadEvent
LoreDiscoveredEvent
LoreReadEvent
LoreRevisionCreatedEvent
LoreRevisionRestoredEvent
```

Relation add/remove currently expose cancellable pre-events only.

Example:

```java
@EventHandler
public void onLoreUpdated(LoreUpdatedEvent event) {
    LoreSnapshot before = event.getPreviousLore();
    LoreSnapshot after = event.getLore();
    if (before != null && after != null) {
        getLogger().info(before.getIdentifier() + " -> " + after.getIdentifier());
    }
}
```

Pre-create and pre-update events expose a live mutable lore object. Post-events expose immutable `LoreSnapshot` values. A snapshot contains UUID, name, description, identifier, lore type, parent identifier, relation identifiers, editor values, and a detached copy.

Every event exposes `LoreEventContext`:

```java
event.getContext().sourcePlugin();
event.getContext().actorUniqueId();
event.getContext().actorName();
```

The context identifies the source plugin and actor where the operation came from. Use snapshots for audit data; do not retain live lore instances beyond the operation without understanding cache mutation.

## Journal API and discovery

Use `JournalManager#discover(player, loreable, source)` for player progression. Discovery is idempotent and flows through `LoreDiscoverEvent` before persistence and `LoreDiscoveredEvent` after acceptance.

```java
if (Taleweaver.journal().discover(player, entry, "myplugin:quest-complete")) {
    // This was a first discovery for this player.
}
```

Do not call discovery to populate NPC knowledge. NPC retrieval uses configured lore and private vector memory and does not grant journal discovery.

## AI provider extension

Implement `AiChatProvider` and register a factory after Taleweaver enables:

```java
Taleweaver.ai().registerProvider("my-provider", () -> request ->
        myClient.complete(request.systemPrompt(), request.messages()));
```

Then configure:

```yaml
AI:
  Enabled: true
  Provider: my-provider
```

Providers receive prompt DTOs, not SQL tables. `LoreAiManager` returns drafts and consistency warnings; it does not grant an external provider permission to persist lore. Keep the normal suggestion/review boundary in place.

## Threading and lifecycle

- Perform lore mutations on the Bukkit primary thread unless the API explicitly documents asynchronous behavior.
- Journal and suggestion persistence use dedicated executors; return to the main thread before touching players, GUIs, or Bukkit state.
- AI operations are asynchronous and complete exceptionally on timeout, provider error, malformed output, or quota failure.
- `LoreManager#reload(...)` reconstructs the cache and then fires `LoreReloadEvent`.
- Optional discovery bridges are registered only while their dependency is enabled and are removed when it disables.
- Resource-pack regeneration is scheduled synchronously.

Use Bukkit's scheduler to bridge between asynchronous external work and synchronous Taleweaver/Bukkit mutations.

## Persistence and integration boundaries

The database is an implementation detail of the core API. Relations are stored in both directions with directional text. Adding a relation updates both in-memory sides and persists both rows; removing it removes both.

Revision snapshots include core fields, editor metadata, parent, and directional relation state. A restore therefore replaces the selected lore's relation set and then saves the resulting live state as a new auditable revision.

There is no cross-table transaction boundary covering every multi-object lore operation. For large imports, use staging data and backups, then call the centralized `LoreManager` operations in controlled batches.

## Integration checklist

1. Declare Taleweaver as a soft dependency and avoid hard class loading when absent.
2. Choose `LoreReferenceBuilder` unless object-specific detection or auto-create is required.
3. Normalize and persist identifiers, not display names.
4. Use `LoreEventContext.of(plugin, sender)` for user-driven mutations.
5. Listen to pre-events for vetoes and post-events for audit/index updates.
6. Run Bukkit mutations on the primary thread.
7. Make auto-create idempotent and tolerate missing optional dependencies.
8. Keep external AI providers within the draft/review boundary.
9. Register/unregister hooks during plugin enable/disable.
10. Test against a backup or staging database before importing production-scale content.
