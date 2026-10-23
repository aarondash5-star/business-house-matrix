# Matrix Cloud Multimodal Manager — Cloudflare Worker skeleton

**Status: configuration-only, no deployment or live inference.**

This scaffold is intentionally fail-closed. It does not send requests to any model or external provider. Cloudflare Workers AI is bound but cannot be invoked until a verified free-tier model registry, quotas, modality rules, authentication and quality benchmarks have been certified.

## Settings
- quality-first routing
- free-only spending
- automatic fallback after verified eligible providers are configured
- no default model
- no external credentials in repository

## Cloudflare setup after approval
Select the existing GitHub repository and set root directory to `cloud/model-manager`. Build command: `npm run typecheck`; deploy command: `npx wrangler deploy`. Do not activate automated deployments before explicit approval. Configure `MATRIX_GATEWAY_TOKEN` as a Cloudflare secret, never as a plaintext variable. Review Worker name, account, Workers AI availability, route, and free quotas.

`workers_dev: false` prevents a default workers.dev public route; do not change it without authorization. Authenticated API endpoints require the secret. /health reports only non-sensitive status.

## G0 blockers
Verify Cloudflare account and GitHub repository binding, Workers AI catalog/free allowance, existing Dell routing adapters, and permitted license/data handling. Mac inventory was unavailable. No provider should be enabled from a historical receipt alone.

Source of truth: docs/handoffs/CLOUD_MULTIMODAL_MANAGER_V1_SPEC_20261024.md and docs/handoffs/CLOUD_MULTIMODAL_MANAGER_G0_INVENTORY_20261024.md.
