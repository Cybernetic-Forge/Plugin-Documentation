# AI & NPCs

Taleweaver can draft lore, report consistency issues, and run lore-aware NPC conversations. All AI features are opt-in. The main configuration page lists provider settings and defaults.

## Choose a provider

| Provider | Requirements |
| --- | --- |
| `openai` | An API token and a configured model |
| `ollama-cloud` | An Ollama Cloud API token |
| `ollama-local` | A reachable local Ollama server with the configured model |
| `huggingface-local` | The configured GGUF file and a locally installed `llama-cli`-compatible executable |

Set `AI.Enabled: true` and choose one `AI.Provider`. Keep tokens private. Reload with `/lore reload` and check `/lore ai status`. Taleweaver downloads the model for the Hugging Face local option on demand. Inference requires the separately installed runtime.

## Draft and review lore

1. Open the detail editor and choose **Generate with AI**, or run `/lore ai generate <kind> <reference> <prompt>`.
2. Describe what the draft should cover. Taleweaver supplies the entry, its parent chain and direct relationships, plus additional lore within the configured context limit.
3. Open `/lore review`. Compare the existing description with the draft before applying or rejecting it.

The same review queue accepts player proposals if those are enabled. Disabling player proposals leaves AI drafts available to reviewers. Even a draft of kind `relations` goes through the description review workflow.

Use `/lore ai check [reference]` to look for contradictions in lore facts, inherited context, or directional relations. Warnings appear in chat. The consistency check does not change lore.

## Set up an NPC

1. Enable both `AI.Enabled` and `AI.NPC.Enabled`.
2. Create a lore entry attached to a Citizens or FancyNpcs NPC.
3. Look at the NPC and run `/lore ai npc-setup`. Configure the system prompt, traits, active state and session action limit.
4. Use **Knowledge** to grant access to selected lore and **Assign actions** to allow specific configured functions.
5. Right-click with an account that has `taleweaver.ai.npc.interact` and test the conversation.

The NPC's own lore is its knowledge root. An entry can include direct relations and its parent chain. Configure any further relation expansion on the reached entry. Conversation memories are scoped to the player and NPC. Chatting with an NPC does not itself unlock journal entries.

During a session, chat messages go to the NPC. Walking out of range, inactivity, logout, reload or shutdown ends the session.

## Configure NPC actions

| Setting | Behavior |
| --- | --- |
| Function identifier and description | Identify the action and tell the model when to request it |
| Command templates | Define the console commands available through this function |
| `%placeholder%` fields | Become parameters after applying command changes |
| `%player%` | Always resolves to the interacting player on the server |
| Player approval | Shows the rendered action and waits for approval before dispatch |

Create or edit a function with `/lore ai function-setup [function-id]` or from **Assign actions**. Choose parameter types and allowed values. Consequential actions can require approval. Declining, timing out, disconnecting or ending the session prevents dispatch. Newly seeded example functions are unassigned until staff explicitly assign them.

## Usage and storage

- `/lore ai usage` shows the caller's rolling one-hour totals. `AI.Usage.PerPlayerHourlyTokenLimit` applies across generation, checks and NPC conversations. `0` means unlimited.
- Chat and embedding content can be sent to the configured remote provider. NPC conversation history and vector memory are stored in MariaDB. Keep provider access and database permissions limited to the people who operate the server.
- `AI.NPC.Vector.Provider: auto` uses supported provider embeddings and falls back to local hashing where needed. `local-hash` forces the local embedding option.
