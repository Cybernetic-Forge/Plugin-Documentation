---
title: Configuration
parent: Taleweaver
nav_order: 2
has_toc: true
---

# Taleweaver Configuration

Taleweaver creates these files in `plugins/Taleweaver`:

| File | Purpose |
| --- | --- |
| `config.yml` | SQL, startup, journal, revisions, AI, NPC, and resource-pack settings |
| `relations.yml` | Directional relation presets, auto-create mappings, and relation-dialog text |
| `translations.yml` | Player messages, GUI labels, placeholders, and formatting |
| `gui.yml` | Materials, layouts, browser icons, and GUI presentation |
| `npc-traits.yml` | Trait choices available in the NPC profile editor |

The plugin adds missing defaults on startup. Keep local edits in these files and back them up before upgrades.

## SQL

```yaml
SQL:
  Host: 127.0.0.1
  Database: database
  Username: root
  Password: password
  Port: 3306
  ConnectTimeoutMillis: 10000
  SocketTimeoutMillis: 30000
```

Taleweaver uses MariaDB and creates the following tables:

- `Taleweaver_Lore`
- `Taleweaver_LoreRelations`
- `Taleweaver_PlayerLore`
- `Taleweaver_LoreSuggestions`
- `Taleweaver_LoreRevisions`
- `Taleweaver_LoreRevisionHeads`
- AI usage, NPC profile, conversation, vector, and function tables when those features are used

The SQL values are loaded when the process starts. `/lore reload` reloads lore/configuration but does not rebind an already-created SQL connection manager.

`ConnectTimeoutMillis` bounds connection establishment. `SocketTimeoutMillis` bounds network reads and writes. For production, use a dedicated MariaDB user with only the required database privileges and never keep the default password.

## Startup and vanilla registries

```yaml
Startup:
  ParallelLoreSql: true
  ProgressLogIntervalSeconds: 15

VanillaRegistries:
  art: false
  attribute: true
  banner_pattern: false
  biome: true
  enchantment: true
  effect: true
  particle: true
  potion: true
  structure: true
  structure_type: false
```

`ParallelLoreSql` loads lore and relation rows concurrently during startup. `ProgressLogIntervalSeconds` controls diagnostic progress messages while a large cache is loading.

Each `VanillaRegistries` key controls whether that Bukkit registry is exposed to auto-create and identifier resolution. The full file also contains `art`, `cat_variant`, `instrument`, `statistic`, `sound`, trim registries, villager registries, fluids, variants, game events, and other Paper registries. Leave a registry disabled when it would create noise that is not part of the server's lore design.

## Journal and revisions

```yaml
Journal:
  LocationCheckIntervalMillis: 500
  Notifications:
    Enabled: true
    ClickableMessage: true

Revisions:
  Enabled: true
  BackfillExistingLore: true
  Retention:
    MaxPerLore: 100
    MaxAgeDays: 0
    CleanupIntervalMinutes: 60
```

Journal discovery state is per player. `LocationCheckIntervalMillis` controls how often location-based discovery checks run. Notifications can be disabled without disabling journal persistence.

Revision behavior:

| Setting | Meaning |
| --- | --- |
| `Enabled` | Store immutable lore versions and expose history controls |
| `BackfillExistingLore` | Create an initial `MIGRATED` version for lore without history |
| `MaxPerLore` | Keep at most this many newest versions; `0` means unlimited |
| `MaxAgeDays` | Remove versions older than this age; `0` means unlimited |
| `CleanupIntervalMinutes` | Scheduled cleanup interval; `0` disables the scheduled task |

The newest revision is always retained. Version numbers are never reused. Restoring a version writes a new version with a restore change kind.

## Resource-pack and custom model data

```yaml
LoadCustomModelData: false
CustomModelData:
  Namespace: taleweaver
  Pack:
    Folder: TaleweaverRP
    Description: Taleweaver generated lore icon pack
    PackFormat: 0
    Prompt: "<gray>Loading Taleweaver icon pack..."
    Force: false
  Delivery:
    Enabled: true
    BindAddress: 0.0.0.0
    Port: 8123
    Path: /TaleweaverRP.zip
    PublicHost: ""
    PublicUrl: ""
```

When enabled, Taleweaver generates icons from `src/main/resources/icons`, creates `TaleweaverRP.zip`, and can serve it from the embedded HTTP endpoint. `PublicUrl` should be the URL Minecraft clients can reach, not merely the server's bind address. If a reverse proxy terminates TLS or maps a different path, set `PublicUrl` explicitly.

Icon lookup prefers an identifier-specific icon, then the lore/reference type, then generic type fallbacks, and finally `default`. External plugins can register a resource-pack icon through the Java API.

## AI authoring

AI is opt-in:

```yaml
AI:
  Enabled: false
  Provider: ""
```

Valid built-in providers are `openai`, `ollama-cloud`, `ollama-local`, and `huggingface-local`.

```yaml
  Usage:
    PerPlayerHourlyTokenLimit: 0
  Async:
    Threads: 2
    TimeoutSeconds: 60
  Generation:
    Temperature: 0.4
    MaxOutputTokens: 700
  Consistency:
    Temperature: 0.0
  Context:
    MaxEntries: 200
```

`PerPlayerHourlyTokenLimit: 0` means unlimited. A non-zero value is shared by generation, consistency checks, and NPC chat. Taleweaver reserves estimated input plus configured maximum output before dispatching concurrent requests.

### Provider settings

```yaml
  OpenAI:
    BaseUrl: https://api.openai.com
    Model: gpt-5.6-terra
    ReasoningEffort: none
    ApiToken: ""
  OllamaCloud:
    BaseUrl: https://ollama.com
    Model: gpt-oss:120b
    ApiToken: ""
  OllamaLocal:
    BaseUrl: http://localhost:11434
    Model: llama3.2:3b
  HuggingFaceLocal:
    Repository: lmstudio-community/Qwen2.5-0.5B-Instruct-GGUF
    Revision: main
    ModelFile: Qwen2.5-0.5B-Instruct-Q4_K_M.gguf
    RuntimeExecutable: llama-cli
    RuntimeArguments:
      - --no-display-prompt
    ContextSize: 2048
    DownloadBaseUrl: https://huggingface.co
```

OpenAI, Ollama Cloud, and Hugging Face credentials must not be committed. Hugging Face local inference downloads the GGUF file lazily under `plugins/Taleweaver/models`; install `llama.cpp` separately or point `RuntimeExecutable` to another `llama-cli`-compatible binary.

### NPC AI

```yaml
  NPC:
    Enabled: false
    SetupTargetDistance: 8.0
    ConversationDistance: 10.0
    IdleTimeoutSeconds: 300
    MaxHistoryMessages: 20
    Conversation:
      Temperature: 0.5
      MaxOutputTokens: 500
    Functions:
      DefaultMaxPerSession: 5
      AbsoluteMaxPerSession: 25
    Vector:
      Provider: auto
      OpenAIModel: text-embedding-3-small
      OllamaModel: nomic-embed-text
      LocalHashDimensions: 384
      RetrievalChunks: 6
      MinimumScore: 0.08
```

NPC AI is gated by both `AI.Enabled` and `AI.NPC.Enabled`. Conversations are supported for Citizens and FancyNpcs profiles. A session ends when the player uses `/lore ai npc-stop`, logs out, idles, reloads/shuts down the plugin, or leaves the configured conversation distance.

`Provider: auto` uses the selected chat provider's embedding endpoint where supported. `local-hash` is dependency-free and is the fallback for Hugging Face local chat and unsupported external providers. `RetrievalChunks` and `MinimumScore` control how much lore/private memory is retrieved for a reply.

NPC functions are administrator-defined console command templates. `%placeholder%` tokens become validated parameters; `%player%` is always server-bound to the interacting player. Functions can require explicit player approval before the exact rendered commands run.

## `relations.yml`

Relation presets have a source-side text, target-side text, and description. The default presets include:

| Preset | Source side | Target side |
| --- | --- | --- |
| `drops` | drops | is dropped by |
| `spawns` | spawns | spawns in |
| `uses` | uses | is used by |
| `grants` | grants | is granted by |
| `teaches` | teaches | is taught by |
| `crafts` | crafts | is crafted by |
| `creates` | creates | is created by |
| `invokes` | invokes | is invoked by |
| `belongs_to` | belongs to | contains |
| `selectable_by` | can be selected by | can select |

`AutoCreateDefaults` maps hook-produced pairs such as `entity_to_item`, `class_to_skill`, `class_to_recipe`, and `recipe_to_item` to a preset. Add or replace mappings only when the resulting sentence remains correct in both directions.

## `translations.yml`, `gui.yml`, and traits

`translations.yml` is the supported place to change player-facing wording, colours, GUI titles, placeholders, and clickable messages. `gui.yml` controls materials, slots, widths, and icon presentation. `npc-traits.yml` supplies trait options shown by the NPC profile editor.

Do not rename placeholder keys unless the corresponding Java message supplies the new key. After editing YAML, run `/lore reload` and check the affected GUI or command path.

## Recommended production profile

- Use a dedicated MariaDB schema and user.
- Enable revisions and keep a database backup before imports.
- Start with only the vanilla registries and integrations needed by the server.
- Keep AI disabled until provider credentials, token limits, and review permissions are tested.
- If using resource-pack delivery, expose a stable HTTPS `PublicUrl` through the server's normal web edge.
- Test `/lore auto-create` on a staging database before importing a large content pack.
