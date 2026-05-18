---
title: Tebex Integration
parent: McMMOParties
nav_order: 4
has_toc: true
---

# McMMOParties Tebex Integration

This guide provides a production-safe Tebex setup where you only add your own values through environment variables.

## Security Requirements

- Never hardcode API tokens, secret keys, package IDs, or category IDs in code or committed config files.
- Store credentials in environment variables on your host (or secret manager).
- Keep a committed template file with placeholders only.

## 1) Environment Variables

Define these on your server/proxy/container:

```bash
MCMMOPARTIES_TEBEX_PUBLIC_KEY=your_public_key
MCMMOPARTIES_TEBEX_PRIVATE_KEY=your_private_key
MCMMOPARTIES_TEBEX_WEBHOOK_SECRET=your_webhook_secret
MCMMOPARTIES_TEBEX_CATEGORY_PARTY_RANKS=123456
MCMMOPARTIES_TEBEX_PACKAGE_VIP_PARTY=234567
MCMMOPARTIES_TEBEX_PACKAGE_ELITE_PARTY=345678
```

## 2) Committable Template (Safe)

Create and commit a template file such as `tebex-config.template.yml`:

```yaml
Tebex:
  Enabled: true
  Api:
    PublicKey: ${MCMMOPARTIES_TEBEX_PUBLIC_KEY}
    PrivateKey: ${MCMMOPARTIES_TEBEX_PRIVATE_KEY}
  Webhook:
    Secret: ${MCMMOPARTIES_TEBEX_WEBHOOK_SECRET}
  CategoryIds:
    PartyRanks: ${MCMMOPARTIES_TEBEX_CATEGORY_PARTY_RANKS}
  PackageIds:
    VipParty: ${MCMMOPARTIES_TEBEX_PACKAGE_VIP_PARTY}
    EliteParty: ${MCMMOPARTIES_TEBEX_PACKAGE_ELITE_PARTY}
```

Commit the template only. Keep real values out of git.

## 3) Runtime File (Not Committed)

Create your real runtime `tebex-config.yml` on the host by injecting environment variables.

If you use container deployment, supply the variables through your orchestrator secret mechanism (for example GitHub Actions Secrets, Docker secrets, or host-level secret files).

## 4) Webhook Flow for McMMOParties

Recommended flow:

1. Customer completes checkout on Tebex.
2. Tebex calls your secure webhook endpoint.
3. Verify webhook signature/secret before processing.
4. Resolve purchased package ID and map it to McMMOParties action.
5. Execute server command (or queue command) for the target player.

Example command mapping:

- `MCMMOPARTIES_TEBEX_PACKAGE_VIP_PARTY` -> grant VIP party perks
- `MCMMOPARTIES_TEBEX_PACKAGE_ELITE_PARTY` -> grant elite party perks

## 5) Validation Checklist

- [ ] No token or ID appears in repository files.
- [ ] All secrets are provided through environment variables only.
- [ ] Webhook verification is enabled.
- [ ] Tebex package/category IDs are configured and resolved correctly.
- [ ] A test purchase triggers the expected McMMOParties command path.
