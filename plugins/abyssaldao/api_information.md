# AbyssalDao API Information

AbyssalDao does **not** currently expose a dedicated, stable public API package in the same style as some larger Bukkit plugins.

What it does expose today is:

- a main plugin entry point
- public model/config records
- an internal storage contract
- built-in config-driven hooks for MythicMobs and Fabled

The practical takeaway is:

- supported integration is mainly **configuration-driven**
- there are **no custom Bukkit events** defined in source
- internal services are **not** exposed through public getters or Bukkit's `ServicesManager`

## Main Entry Point

The Bukkit plugin main class is `net.cyberneticforge.AbyssalDao`.

Useful public entry points:

- `AbyssalDao.getInstance()`
- `AbyssalDao.reloadAll()`

Example:

```java
import net.cyberneticforge.AbyssalDao;

AbyssalDao plugin = AbyssalDao.getInstance();
boolean ok = plugin != null && plugin.reloadAll();
```

Important note:

- `reloadAll()` hot-reloads the YAML-backed runtime systems, but the storage backend itself is not swapped live. Changes to `storage.yml` still require a restart.

## Supported Integration Model

### MythicMobs

If MythicMobs is installed, AbyssalDao reads `mythicmobs.yml` and exposes those configured entries as external Dao skills.

Those skills can then:

- appear in the skills GUI
- be cast through `/dao cast <skill>`
- be bound with `/dao cast bind <skill> <combo>`
- be recorded as external recording steps

### Fabled

If Fabled is installed, AbyssalDao reads `fabled.yml` and exposes those configured entries the same way.

Additional Fabled note:

- `required-class` can be used to gate the external skill to a specific Fabled class.

## `SkillProvider` and Registry

Internally, the plugin uses:

- `SkillProvider`
- `SkillProviderRegistry`
- `DaoSkill`

`SkillProvider` defines:

- `providerId()`
- `getSkills()`
- `execute(DaoSkill skill, Player caster, PlayerDaoProfile profile)`

`SkillProviderRegistry` supports:

- `register(SkillProvider provider)`
- `provider(String providerId)`
- `externalSkills()`
- `findExternalSkillById(String skillId)`

Important limitation:

- although these classes are public, the plugin's live `SkillProviderRegistry` instance is a **private field** inside `AbyssalDao` and is not exposed by a public getter.
- that means third-party plugins do **not** currently have a clean supported way to register their own provider at runtime without modifying AbyssalDao or using reflection.
- in practice, the supported path today is the shipped MythicMobs/Fabled config integration rather than arbitrary provider injection.

## Persistence Contract

The persistence abstraction is `StorageProvider`.

It defines:

- `initialize()`
- `loadProfile(UUID playerId)`
- `saveProfile(PlayerDaoProfileSnapshot snapshot)`
- `close()`

Bundled implementations:

- `SqliteStorageProvider`
- `MySqlStorageProvider`
- `MariaDbStorageProvider`

The serialized snapshot shape is `PlayerDaoProfileSnapshot`.

It stores:

- `playerId`
- `affinity`
- `progressionLevel`
- `cultivationExperience`
- `cultivationInsight`
- `activeCultivationMethodId`
- `cultivationFocus`
- `cultivationFocusUpdatedAt`
- `instabilityUntil`
- `lastBreakthroughAttemptAt`
- `recordedSkills`
- `skillBindings`
- `methodMasteryExperience`
- `unlockedSkillTreeNodes`
- `skillProgressions`

Important note:

- this storage interface is internal to the plugin. There is no public runtime setter for swapping providers after startup.

## Main Runtime Models

Public model types that are useful to understand when reading or extending the code:

| Type | Purpose |
| --- | --- |
| `PlayerDaoProfile` | Main in-memory player state: affinity, level, cultivation resources, recorded skills, bindings, mastery, instability, and unlocked tree nodes. |
| `RecordedSkill` | A saved player technique built from recorded combo or external skill steps. |
| `SkillBinding` | A player-defined combo binding that maps an `L`/`R` sequence to a skill. |
| `DaoSkill` | General skill descriptor used for native, recorded, and external skills. |
| `SkillProgression` | Evolution data for a recorded skill. |
| `TaoCreatureProfile` | Element and Tao level data attached to a Tao creature. |
| `InfusionState` | Current Tao infusion state for a player. |

## Public Config and Math Records

The plugin also exposes many public records that mirror loaded config:

- `DaoConfiguration`
- `DaoSettings`
- `ElementDefinition`
- `ComboDefinition`
- `CultivationConfiguration`
- `CultivationGlobalSettings`
- `BreakthroughSettings`
- `CultivationMethodDefinition`
- `RealmDefinition`
- `SkillTreeConfiguration`
- `SkillTreeNodeDefinition`
- `SkillTreeNodeRequirement`
- `SkillTreeNodeBonuses`
- `FocusEnvironmentConfiguration`
- `SynergyDefinition`
- `TaoCreatureSettings`

Useful public helper classes:

- `CultivationMath`
- `SkillTreeMath`

These are helpful for understanding how values are derived, but they are still part of the plugin's own internal architecture rather than a documented compatibility contract.

## Events

There are currently **no custom Bukkit events** in the source tree for:

- casts
- breakthroughs
- recordings
- skill tree unlocks
- Tao Sense state changes
- Tao creature kills

That means external integrations cannot subscribe to a formal AbyssalDao event bus today. If you need to react to plugin behavior, you currently have to:

- listen to normal Paper/Bukkit events yourself
- inspect player state indirectly
- or modify/fork the plugin

## Practical Integration Notes

- The safest supported integration surface is the config-based external skill system through `mythicmobs.yml` and `fabled.yml`.
- `AbyssalDao.reloadAll()` is the main public runtime control surface.
- Internal services like `ProfileService`, `DaoCombatService`, `CultivationService`, `SkillTreeService`, and `TaoSenseService` are not published through getters.
- There is no Bukkit `ServicesManager` registration for AbyssalDao services.
- If you need a hard API for third-party plugins, the current codebase would need explicit new public accessors and probably custom Bukkit events.
