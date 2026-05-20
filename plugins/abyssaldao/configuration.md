---
title: Configuration
parent: AbyssalDao
nav_order: 2
has_toc: true
---

# AbyssalDao Configuration

AbyssalDao ships with the following main configuration files:

- `config.yml`: combat input, Tao Sense, skill evolution, progression, transfer, and infusion settings
- `storage.yml`: SQLite/MySQL/MariaDB persistence backend settings
- `elements.yml`: display names, colors, and five-phase strengths/weaknesses
- `combos.yml`: built-in combo sequences and their base manifestation stats
- `messages.yml`: player-facing text and command feedback
- `help.yml`: in-game help GUI/page content
- `cultivation.yml`: focus, mastery tiers, realms, methods, and breakthrough rules
- `skill_trees.yml`: per-element node trees, unlock requirements, and permanent bonuses
- `focus-environments.yml`: favorable/hindering biome and environment tuning
- `synergies.yml`: cast-sequence synergy effects
- `tao-creatures.yml`: Tao creature tagging, AI, and kill rewards
- `mythicmobs.yml`: optional external skill entries exposed from MythicMobs
- `fabled.yml`: optional external skill entries exposed from Fabled

## Example `config.yml`

```yaml
combo-input:
  timeout-millis: 1200
  require-sneaking: true
  debug-action-bar: true
combat:
  allow-player-vs-player: true
  allow-player-vs-mob: true
  respect-scoreboard-teams: true
  default-cooldown-ticks: 20
  damage-scale: 1.0
  max-range: 12.0
  max-targets-per-cast: 4
  disabled-worlds: []
skill-casting:
  max-combo-length: 5
tao-sense:
  triple-sneak-window-millis: 1200
  update-interval-ticks: 10
  range: 24.0
  darkness-duration-ticks: 40
  weakness-offset-y: 0.95
  weakness-hit-radius: 0.55
  hindering-damage-multiplier: 1.25
  hindered-damage-multiplier: 0.80
  weakness-point-bonus-multiplier: 1.40
  signature-layers:
    level-layer:
      min-level: 3
      min-sense-tier: 1
    instability-layer:
      min-level: 5
      min-sense-tier: 2
    method-layer:
      min-level: 7
      min-sense-tier: 3
    focus-layer:
      min-level: 5
      min-sense-tier: 2
cultivation:
  meditate-interval-ticks: 40
  meditation-movement-threshold: 0.75
  meditation-xp-per-cycle: 6
  tao-sense-insight-per-signature: 2
  combat-xp-per-hit: 4
  advantage-insight-bonus: 2
  weakness-insight-bonus: 4
  breakthrough-base-xp: 24
  breakthrough-xp-scale: 16
  breakthrough-base-insight: 8
  breakthrough-insight-scale: 6
recording:
  max-combos-per-skill: 8
skill-evolution:
  xp-per-cast: 4
  xp-per-hit: 2
  level-thresholds: [50, 150, 350, 700, 1200]
  damage-bonus-per-level: 0.08
  cooldown-reduction-per-level: 0.05
  range-bonus-per-level: 0.40
  mutation-chance-per-level-up: 0.30
progression:
  default-level: 1
  max-level: 10
transfer:
  enabled: true
  max-copies-per-skill: 3
  cooldown-seconds: 3600
infusion:
  focus-cost: 10
  duration-ticks: 200
  drain-per-tick: 0
  weapon-damage-bonus: 2.0
  armor-damage-reduction: 0.15
  tool-haste-level: 1
```

## `config.yml` Reference

| Path | Type | Default | Description |
| --- | --- | --- | --- |
| `combo-input.timeout-millis` | integer | `1200` | Maximum time window for building an input combo before the buffer expires. |
| `combo-input.require-sneaking` | boolean | `true` | If `true`, combo input only counts while the player is sneaking. |
| `combo-input.debug-action-bar` | boolean | `true` | Shows combo buffer/debug information in the action bar. |
| `combat.allow-player-vs-player` | boolean | `true` | Enables Dao damage against players. |
| `combat.allow-player-vs-mob` | boolean | `true` | Enables Dao damage against mobs. |
| `combat.respect-scoreboard-teams` | boolean | `true` | Prevents friendly fire against same-team players when enabled. |
| `combat.default-cooldown-ticks` | integer | `20` | Fallback cooldown used by manifestations that do not override it. |
| `combat.damage-scale` | decimal | `1.0` | Global multiplier applied to Dao combat damage. |
| `combat.max-range` | decimal | `12.0` | Hard cap for cast range calculations. |
| `combat.max-targets-per-cast` | integer | `4` | Maximum entities a cast can hit. |
| `combat.disabled-worlds` | string list | `[]` | Lowercased world names where Dao combat is disabled. |
| `skill-casting.max-combo-length` | integer | `5` | Maximum custom binding length for `/dao cast bind`. |
| `tao-sense.triple-sneak-window-millis` | integer | `1200` | Time window used for Tao Sense triple-sneak toggling. |
| `tao-sense.update-interval-ticks` | integer | `10` | How often Tao Sense visual updates are recalculated. |
| `tao-sense.range` | decimal | `24.0` | Base Tao Sense detection range before realm, mastery, or skill tree bonuses. |
| `tao-sense.darkness-duration-ticks` | integer | `40` | Darkness effect duration refreshed while Tao Sense is active. |
| `tao-sense.weakness-offset-y` | decimal | `0.95` | Vertical offset used for weakness-point placement on sensed targets. |
| `tao-sense.weakness-hit-radius` | decimal | `0.55` | Hit radius used for weakness-point precision checks. |
| `tao-sense.hindering-damage-multiplier` | decimal | `1.25` | Damage multiplier when the caster's element hinders the target's element. |
| `tao-sense.hindered-damage-multiplier` | decimal | `0.80` | Damage multiplier when the target's element hinders the caster's element. |
| `tao-sense.weakness-point-bonus-multiplier` | decimal | `1.40` | Extra multiplier for precise weakness-point hits. |
| `tao-sense.signature-layers.level-layer.min-level` | integer | `3` | Minimum target Dao level before the level signature layer can show. |
| `tao-sense.signature-layers.level-layer.min-sense-tier` | integer | `1` | Required Tao Sense tier for the level signature layer. |
| `tao-sense.signature-layers.instability-layer.min-level` | integer | `5` | Minimum target Dao level before instability information can show. |
| `tao-sense.signature-layers.instability-layer.min-sense-tier` | integer | `2` | Required Tao Sense tier for the instability layer. |
| `tao-sense.signature-layers.method-layer.min-level` | integer | `7` | Minimum target Dao level before active method information can show. |
| `tao-sense.signature-layers.method-layer.min-sense-tier` | integer | `3` | Required Tao Sense tier for the method layer. |
| `tao-sense.signature-layers.focus-layer.min-level` | integer | `5` | Minimum target Dao level before focus information can show. |
| `tao-sense.signature-layers.focus-layer.min-sense-tier` | integer | `2` | Required Tao Sense tier for the focus layer. |
| `cultivation.meditate-interval-ticks` | integer | `40` | Legacy top-level cultivation timer setting still loaded into `DaoSettings`. The more detailed cultivation system is tuned from `cultivation.yml`. |
| `cultivation.meditation-movement-threshold` | decimal | `0.75` | Legacy top-level movement threshold loaded into `DaoSettings`. |
| `cultivation.meditation-xp-per-cycle` | integer | `6` | Legacy top-level meditation XP setting loaded into `DaoSettings`. |
| `cultivation.tao-sense-insight-per-signature` | integer | `2` | Legacy top-level Tao Sense insight setting loaded into `DaoSettings`. |
| `cultivation.combat-xp-per-hit` | integer | `4` | Legacy top-level combat XP setting loaded into `DaoSettings`. |
| `cultivation.advantage-insight-bonus` | integer | `2` | Legacy top-level elemental advantage insight bonus loaded into `DaoSettings`. |
| `cultivation.weakness-insight-bonus` | integer | `4` | Legacy top-level weakness insight bonus loaded into `DaoSettings`. |
| `cultivation.breakthrough-base-xp` | integer | `24` | Legacy top-level breakthrough XP tuning loaded into `DaoSettings`. |
| `cultivation.breakthrough-xp-scale` | integer | `16` | Legacy top-level breakthrough XP scaling loaded into `DaoSettings`. |
| `cultivation.breakthrough-base-insight` | integer | `8` | Legacy top-level breakthrough insight tuning loaded into `DaoSettings`. |
| `cultivation.breakthrough-insight-scale` | integer | `6` | Legacy top-level breakthrough insight scaling loaded into `DaoSettings`. |
| `recording.max-combos-per-skill` | integer | `8` | Maximum number of captured steps allowed in a recorded skill. |
| `skill-evolution.xp-per-cast` | integer | `4` | Skill evolution XP awarded when a recorded skill is cast. |
| `skill-evolution.xp-per-hit` | integer | `2` | Skill evolution XP awarded when a recorded skill hits a target. |
| `skill-evolution.level-thresholds` | integer list | `[50, 150, 350, 700, 1200]` | XP thresholds for recorded-skill evolution levels. |
| `skill-evolution.damage-bonus-per-level` | decimal | `0.08` | Damage bonus per recorded-skill evolution level. |
| `skill-evolution.cooldown-reduction-per-level` | decimal | `0.05` | Cooldown reduction per recorded-skill evolution level. |
| `skill-evolution.range-bonus-per-level` | decimal | `0.40` | Range bonus per recorded-skill evolution level. |
| `skill-evolution.mutation-chance-per-level-up` | decimal | `0.30` | Chance for a mutation trait to appear on skill level-up. |
| `progression.default-level` | integer | `1` | Starting Dao level for new profiles. |
| `progression.max-level` | integer | `10` | Hard cap for Tao progression level. |
| `transfer.enabled` | boolean | `true` | Present in config and loaded into settings, but the player-facing transfer command flow is not implemented yet. |
| `transfer.max-copies-per-skill` | integer | `3` | Reserved limit for future skill transfer/copying logic. |
| `transfer.cooldown-seconds` | integer | `3600` | Reserved cooldown for future skill transfer/copying logic. |
| `infusion.focus-cost` | integer | `10` | Focus cost to trigger Tao infusion. |
| `infusion.duration-ticks` | integer | `200` | Duration of Tao infusion effects. |
| `infusion.drain-per-tick` | integer | `0` | Additional focus drain per tick during infusion. |
| `infusion.weapon-damage-bonus` | decimal | `2.0` | Extra weapon damage while infused. |
| `infusion.armor-damage-reduction` | decimal | `0.15` | Incoming damage reduction while infused armor is active. |
| `infusion.tool-haste-level` | integer | `1` | Haste amplifier used for infused tools. |

## `storage.yml`

The persistence backend is configured in `storage.yml`.

```yaml
type: SQLITE
sqlite:
  file: dao-data.db
mysql:
  host: localhost
  port: 3306
  database: abyssaldao
  username: root
  password: change-me
  parameters: "useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC"
```

| Path | Type | Default | Description |
| --- | --- | --- | --- |
| `type` | string | `SQLITE` | Storage backend. Valid values are `SQLITE`, `MYSQL`, and `MARIADB`. |
| `sqlite.file` | string | `dao-data.db` | SQLite file name placed inside the plugin data folder. |
| `mysql.host` | string | `localhost` | Hostname used for MySQL or MariaDB. |
| `mysql.port` | integer | `3306` | Port used for MySQL or MariaDB. |
| `mysql.database` | string | `abyssaldao` | Database/schema name. |
| `mysql.username` | string | `root` | SQL username. |
| `mysql.password` | string | `change-me` | SQL password. |
| `mysql.parameters` | string | `useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC` | Extra JDBC query parameters appended to the connection string. |

Notes:

- Changing `storage.yml` is **not** hot-swapped by `/dao admin reload`; a full restart is required.
- The plugin ships built-in SQLite, MySQL, and MariaDB providers.

## `messages.yml` and `help.yml`

- `messages.yml` contains almost all player-facing text: command responses, cultivation feedback, recording notices, skill tree unlock text, instability text, and admin messages.
- `help.yml` drives the `/dao help [page]` GUI and lets you rewrite the built-in onboarding/help flow without code changes.
- Both files are reloaded by `/dao admin reload`.

## `elements.yml`

`elements.yml` defines the five fixed affinities and the core five-phase relationship table:

| Element | Display name | Strong against | Weak against |
| --- | --- | --- | --- |
| `WOOD` | `&aWood` | `EARTH` | `METAL` |
| `FIRE` | `&cFire` | `METAL` | `WATER` |
| `EARTH` | `&6Earth` | `WATER` | `WOOD` |
| `METAL` | `&7Metal` | `WOOD` | `FIRE` |
| `WATER` | `&bWater` | `FIRE` | `EARTH` |

Each element entry also contains:

- `display-name`
- `primary-color`
- `secondary-color`
- `strong-against`
- `weak-against`

## `combos.yml`

`combos.yml` defines the built-in castable manifestations. Default combos:

| Id | Sequence | Min level | Form | Cooldown | Base damage | Range | Radius |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `pulse` | `LLL` | `1` | `BURST` | `18` ticks | `4.0` | `5.0` | `2.5` |
| `helix` | `RRL` | `1` | `PROJECTILE` | `24` ticks | `4.5` | `10.0` | `0.9` |
| `tide_break` | `LRRL` | `2` | `WAVE` | `30` ticks | `5.0` | `7.5` | `3.0` |
| `mirrored_arc` | `RLLR` | `3` | `LINE` | `34` ticks | `5.5` | `11.0` | `1.2` |
| `tao_infuse` | `RRR` | `2` | `INFUSE` | `100` ticks | `0.0` | `0.0` | `0.0` |

Important rules enforced by the loader:

- Sequences must be unique.
- Sequences may only contain `L` and `R`.
- Built-in combos cannot prefix-conflict with each other.
- `min-level` is clamped between `1` and `progression.max-level`.

## `cultivation.yml`

`cultivation.yml` is the main long-term progression file. It defines:

- `global`: focus economy, instability system, and generic cultivation pacing
- `mastery-tiers`: named thresholds like `Seed`, `Tempered`, and `Transcendent`
- `style-bonuses`: passive bonuses granted per mastery tier for `STILLNESS`, `SENSE`, `COMBAT`, and `FLOW`
- `realms`: named Tao realms unlocked by minimum level
- `breakthrough`: formulas, chance clamps, penalties, and cooldowns
- `methods`: per-element cultivation methods with cycle rewards and combat rewards

### Global settings

Notable defaults from `global`:

| Path | Default | Meaning |
| --- | --- | --- |
| `meditate-interval-ticks` | `80` | Meditation cycle timing. |
| `meditation-movement-threshold` | `0.55` | Max movement for stillness/sense meditation. |
| `flow-movement-minimum` | `0.12` | Minimum movement expected for `FLOW` methods. |
| `flow-movement-maximum` | `1.45` | Maximum movement expected for `FLOW` methods. |
| `environment-radius` | `4.0` | Radius used for cultivation environment checks. |
| `focus-max` | `960` | Base maximum focus before skill tree bonuses. |
| `focus-regen-per-hour` | `90` | Base hourly focus regeneration before modifiers. |
| `low-focus-floor-multiplier` | `0.04` | Minimum cultivation efficiency when focus is depleted. |
| `generic-combat-xp-per-hit` | `1` | Baseline cultivation XP from successful Dao combat hits. |
| `generic-advantage-insight` | `1` | Baseline insight from advantageous elemental hits. |
| `generic-weakness-insight` | `2` | Baseline insight from weakness-point hits. |
| `generic-focus-cost-per-hit` | `3` | Baseline focus cost per successful Dao combat hit. |
| `instability-gain-multiplier` | `0.65` | Multiplier applied when instability penalties are converted into gain/penalty outcomes. |
| `instability-cooldown-penalty` | `0.15` | Extra breakthrough penalty while unstable. |
| `instability-tao-sense-range-penalty` | `2.5` | Tao Sense range penalty while unstable. |
| `instability-bonuses-enabled` | `true` | Enables the risk/reward instability tier system. |
| `instability-low-threshold-minutes` | `1` | Start of the low instability tier. |
| `instability-moderate-threshold-minutes` | `20` | Start of the moderate instability tier. |
| `instability-high-threshold-minutes` | `50` | Start of the high instability tier. |
| `instability-suppress-modifier` | `0.50` | Multiplier used by `/dao instability suppress`. |
| `instability-embrace-modifier` | `1.50` | Multiplier used by `/dao instability embrace`. |

### Mastery tiers

Default mastery thresholds:

| Tier id | Display name | Threshold |
| --- | --- | --- |
| `seed` | `Seed` | `0` |
| `tempered` | `Tempered` | `140` |
| `flowing` | `Flowing` | `380` |
| `resonant` | `Resonant` | `760` |
| `transcendent` | `Transcendent` | `1320` |

### Realms

Default realm progression:

| Realm id | Display name | Min level |
| --- | --- | --- |
| `awakened-breath` | `Awakened Breath` | `1` |
| `meridian-flow` | `Meridian Flow` | `3` |
| `hindering-core` | `Hindering Core` | `5` |
| `manifest-current` | `Manifest Current` | `7` |
| `abyssal-dao` | `Abyssal Dao` | `9` |

Each realm also grants passive numeric bonuses to:

- Tao Sense range
- weakness radius
- combat damage
- cooldown reduction
- cast range
- insight gain
- breakthrough stability

### Breakthrough tuning

Default breakthrough rules:

| Path | Default | Description |
| --- | --- | --- |
| `xp-base` | `1400` | Base XP needed for the next breakthrough. |
| `xp-linear-scale` | `650` | Linear XP growth per level offset. |
| `xp-quadratic-scale` | `150` | Quadratic XP growth per level offset. |
| `insight-base` | `120` | Base insight needed for the next breakthrough. |
| `insight-linear-scale` | `45` | Linear insight growth per level offset. |
| `total-mastery-base` | `150` | Base total mastery requirement. |
| `total-mastery-scale` | `120` | Mastery growth per level offset. |
| `attempt-cooldown-seconds` | `1200` | Cooldown after each breakthrough attempt. |
| `success-base-chance` | `0.42` | Starting breakthrough success chance. |
| `minimum-success-chance` | `0.12` | Lower clamp for success chance. |
| `maximum-success-chance` | `0.95` | Upper clamp for success chance. |
| `active-method-mastery-weight` | `0.00028` | Weight applied to active method mastery. |
| `total-mastery-weight` | `0.00011` | Weight applied to combined mastery. |
| `insight-overcap-weight` | `0.0012` | Bonus from insight above the requirement. |
| `xp-overcap-weight` | `0.00035` | Bonus from XP above the requirement. |
| `instability-active-penalty` | `0.14` | Chance penalty while instability is active. |
| `failure-xp-loss-percent` | `0.32` | XP lost on a normal failure. |
| `failure-insight-loss-percent` | `0.26` | Insight lost on a normal failure. |
| `failure-instability-minutes` | `30` | Instability applied on a normal failure. |
| `severe-failure-threshold` | `0.40` | Severe-failure check threshold. |
| `severe-extra-xp-loss-percent` | `0.18` | Extra XP loss on severe failure. |
| `severe-extra-insight-loss-percent` | `0.18` | Extra insight loss on severe failure. |
| `severe-extra-instability-minutes` | `45` | Extra instability on severe failure. |

### Cultivation methods

Each method entry under `methods.<ELEMENT>.<id>` supports:

- `display-name`
- `description`
- `style`
- `environment`
- `requires-tao-sense`
- `min-nearby-tao-signatures`
- `xp-per-cycle`
- `insight-per-cycle`
- `mastery-per-cycle`
- `focus-cost-per-cycle`
- `xp-per-hit`
- `insight-per-advantage`
- `insight-per-weakness`
- `mastery-per-hit`
- `focus-cost-per-hit`

Default method ids by element:

| Element | Method ids |
| --- | --- |
| `WOOD` | `rooted-grove`, `pollen-listening`, `bramble-hunt` |
| `FIRE` | `cinder-furnace`, `sun-devouring`, `ashen-assault` |
| `EARTH` | `mountain-posture`, `vein-listening`, `crushing-domain` |
| `METAL` | `resonant-anvil`, `echo-discipline`, `edge-tempering` |
| `WATER` | `deep-current`, `mist-listening`, `undertow-flow` |

### Practical note

`cultivation.yml` is the main place to rebalance progression speed, risk, and pacing. In practice:

- edit `global` for focus economy and instability behavior
- edit `breakthrough` for progression wall hardness
- edit `style-bonuses` and `realms` for passive power curves
- edit `methods` for element-specific cultivation identity

## `skill_trees.yml`

`skill_trees.yml` defines one tree per element under `skill-trees.<ELEMENT>`.

Each tree contains:

- `root.icon`
- `root.title`
- `root.description`
- `root.background`
- `nodes.<id>.parent`
- `nodes.<id>.icon`
- `nodes.<id>.title`
- `nodes.<id>.description`
- `nodes.<id>.frame`
- `nodes.<id>.requirements`
- `nodes.<id>.bonuses`

Example structure:

```yaml
skill-trees:
  WOOD:
    root:
      title: "&aWood Dao"
      background: "minecraft:textures/gui/advancements/backgrounds/husbandry.png"
    nodes:
      living-bark:
        parent:
        frame: task
        requirements:
          min-level: 2
          min-total-mastery: 40
          xp-cost: 180
          insight-cost: 18
          requires: []
        bonuses:
          focus-max-bonus: 60
          cultivation-gain-bonus: 0.03
```

Important behavior:

- Node ids must be globally unique across **all** element trees.
- Parent references are validated and cycles are rejected at load time.
- `root.background` accepts full texture-style paths and is normalized internally.
- Unlock costs come from XP, insight, level, total mastery, and prerequisite node ids.
- Bonuses can grant focus max, focus regen, combat damage, cooldown reduction, cast range, Tao Sense range, weakness radius, cultivation gain, and breakthrough stability.

## `focus-environments.yml`

This file controls how surroundings modify focus economy and combat output.

Top-level structure:

- `focus-environments.enabled`
- `focus-environments.biome-influence-enabled`
- `focus-environments.block-influence-enabled`
- `focus-environments.evaluation-interval-ticks`
- `focus-environments.favorable.*`
- `focus-environments.hindering.*`
- `focus-environments.elements.<ELEMENT>.favorable.environments`
- `focus-environments.elements.<ELEMENT>.favorable.biomes`
- `focus-environments.elements.<ELEMENT>.hindering.environments`
- `focus-environments.elements.<ELEMENT>.hindering.biomes`

Behavior:

- Favorable environments reduce focus costs, improve regeneration, and slightly improve combat.
- Hindering environments increase focus costs, reduce regeneration, and slightly penalize combat.
- Priority order is `hindering > favorable > neutral`.

## `synergies.yml`

The default synergy definitions are:

| Id | Name | Sequence | Effect | Window |
| --- | --- | --- | --- | --- |
| `fire-metal-explosion` | `Forging Blast` | `FIRE -> METAL` | `EXPLOSION` with `power 2.0`, `radius 4.0` | `5s` |
| `water-wood-root` | `Entangling Torrent` | `WATER -> WOOD` | `ROOT` for `80` ticks in `5.0` blocks | `5s` |
| `earth-earth-amplify` | `Tectonic Surge` | `EARTH -> EARTH` | `AMPLIFY` next cast by `1.4x` | `4s` |
| `fire-burst-burst-slow` | `Scorching Blaze` | `FIRE/BURST -> FIRE/BURST` | `SLOW` for `80` ticks in `5.0` blocks | `5s` |
| `metal-earth-amplify` | `Iron Mountain` | `METAL -> EARTH` | `AMPLIFY` next cast by `1.3x` | `5s` |
| `wood-fire-explosion` | `Blazing Grove` | `WOOD -> FIRE` | `EXPLOSION` with `power 1.5`, `radius 4.5` | `5s` |

Each synergy entry supports:

- `name`
- `sequence`
- `effect.type`
- `effect.power`
- `effect.radius`
- `effect.duration-ticks`
- `effect.multiplier`
- `window-seconds`

## `tao-creatures.yml`

This file controls the Tao creature system:

- `auto-tag-on-spawn`: automatically assigns Tao creature profiles to configured entities
- `combat-ai.*`: cast range, cooldowns, mutation chance, and cooperative range for creature casting AI
- `kill-bonuses.*`: XP and insight rewards awarded when players kill Tao creatures
- `entity-types.*`: default Bukkit entity mappings to element and Tao level
- `mythicmobs.*`: optional MythicMobs id mappings to element and Tao level

Default highlights:

- AI is enabled with a `20` tick update interval.
- Default AI cast range is `12.0`.
- Kill rewards start at `8` XP and `2` insight, plus per-level bonuses.
- The shipped `entity-types` section maps mobs such as `ZOMBIE`, `BLAZE`, `GUARDIAN`, `IRON_GOLEM`, `WARDEN`, and `PIGLIN_BRUTE`.

## `mythicmobs.yml` and `fabled.yml`

These two files expose external skills in the AbyssalDao skill GUI and casting flow when their backing plugin is installed.

### `mythicmobs.yml`

Structure:

```yaml
mythicmobs:
  SomeSkillId:
    element: FIRE
    level: 0
    display-name: "Some Skill"
    description: "Shown in the Dao skills GUI."
    target: LOOK_ENTITY
```

Supported fields:

- `element`
- `level`
- `display-name`
- `description`
- `target`

Supported target values:

- `SELF`
- `ENTITY`
- `NEAREST_ENTITY`
- `LOOK_ENTITY`
- `LOOK_LOCATION`
- `LOOK_BLOCK`

### `fabled.yml`

Structure:

```yaml
fabled:
  some_skill:
    element: WATER
    level: 0
    display-name: "Some Skill"
    description: "Shown in the Dao skills GUI."
    required-class: "SomeClass"
```

Supported fields:

- `element`
- `level`
- `display-name`
- `description`
- `required-class`

## Practical editing tips

- Use `config.yml` for quick balance changes to combo input, global combat caps, recording limits, skill evolution, and infusion.
- Use `cultivation.yml` for progression pacing, breakthrough difficulty, mastery identity, and instability behavior.
- Use `skill_trees.yml` for long-term specialization and permanent stat growth.
- Use `focus-environments.yml` when you want the world itself to matter more to each affinity.
- Use `mythicmobs.yml` or `fabled.yml` if you want external skills to appear in `/dao skills` and to be bindable with `/dao cast bind`.
- After editing any YAML except `storage.yml`, `/dao admin reload` is the intended refresh path.

