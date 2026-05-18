---
title: Configuration
parent: McMMOParties
nav_order: 3
has_toc: true
---

# McMMOParties Configuration

Below is placeholder configuration documentation for now.

## Example `config.yml`

```yaml
party:
  max-size: 8
  invite-timeout-seconds: 60
  friendly-fire: false

chat:
  party-chat-format: "[Party] {player}: {message}"

rewards:
  enabled: true
  bonus-xp-multiplier: 1.10
```

## Option Reference (Placeholder)

| Path | Type | Description |
| --- | --- | --- |
| `party.max-size` | integer | Maximum number of members per party |
| `party.invite-timeout-seconds` | integer | Time before pending invites expire |
| `party.friendly-fire` | boolean | Whether party members can damage each other |
| `chat.party-chat-format` | string | Chat format for party channel messages |
| `rewards.bonus-xp-multiplier` | decimal | Bonus multiplier for party-related XP |

> Replace this placeholder with the plugin's real config options and defaults.
