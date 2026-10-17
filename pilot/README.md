# Open WebUI-first pilot — deployment handoff (NOT deployed)

**Scope:** Open WebUI first. **Excluded:** LibreChat, OpenClaw, external communication, paid model APIs, production systems and all Moksha Master connectivity.

The official Docker image is reused, not forked or rebuilt. No runtime installation has happened. A reviewed release tag/digest, a target host and permission to deploy are required before running.

## Host prerequisites

- Dedicated Linux/macOS Docker host with Compose, sufficient free storage/memory and a backed-up private data volume.
- App restricted to `127.0.0.1:3000`, accessible locally or through an authenticated SSH tunnel.
- Record exact image digest, image/source licence, server specs and security preflight result.

## UI-only bootstrap steps (operator on the selected host)

1. Copy this entire `pilot/` folder to a standalone Business House Matrix path (not any other project's directory).
2. `cp .env.example .env`; replace `OPEN_WEBUI_IMAGE` with a verified immutable digest (`ghcr.io/open-webui/open-webui@sha256:...`) or a reviewed version tag. Generate `WEBUI_SECRET_KEY` with `openssl rand -hex 32`, populate `.env`, restrict file permissions (`chmod 600 .env`). Never commit it.
3. Run `bash preflight.sh`. Review the rendered config (`docker compose --env-file .env config`); verify ONLY the UI on `127.0.0.1:3000`. Check Docker and port 3000 availability.
4. On first-time bootstrap only, set `ENABLE_SIGNUP=True` while the UI is reachable **only on loopback**, then `docker compose up -d`. Confirm with `docker compose ps`, container logs, and `curl -I http://127.0.0.1:3000/`.
5. In a trusted local browser visit `http://127.0.0.1:3000`; create the first admin account. Then immediately change `ENABLE_SIGNUP=False`, run `docker compose up -d --force-recreate` and verify that new signup is disabled while login still works. `WEBUI_AUTH` must remain enabled. If accessed from another machine, use `ssh -L 3000:127.0.0.1:3000 operator@host`.
6. Restart the service, verify the admin can log in and data persists, back up and restore a test copy of the data volume, and record results. Do not enable plugins or tool servers during this initial UI gate.

## Subsequent pilot gates (not included in this Compose file)

- **Local inference:** Add an independently reviewed Ollama service and model, reachable only on an authorized private interface. Configure the Open WebUI Ollama connection from Admin > Connections; explicitly enable `ENABLE_OLLAMA_API` after review. Do not publish Ollama's unauthenticated HTTP API. See https://docs.openwebui.com/getting-started/quick-start/connect-a-provider/ .
- **Central Brain:** Supply a separately authorized OpenAI-compatible adapter for LangGraph/Temporal; connect as an approved OpenAI-compatible provider, using a restricted key and authentication. It does not exist in the starter yet.
- **MCP:** Enable the plugin/tool-server controls **only after** the permissions and tool-authorization threat model is approved. Native MCP requires Streamable HTTP and supported Open WebUI version. Never import unreviewed Python Tools/Functions. See https://docs.openwebui.com/features/extensibility/mcp/ .
- **OpenClaw:** No installation, container, configuration or messaging channel until AFTER pilot acceptance and separate approval.

## Acceptance and costs

- Loopback-only access, login, signup closure, persistent data, tested restart/restore, no production tool access or unintended outgoing calls; collect evidence before progression.
- No mandatory paid API or hosting licence. Open WebUI's current licence is **source-available, not OSI-open-source** and protects branding. Preserve branding. See https://docs.openwebui.com/license/ .
- Exact machine capacity, model performance and container compatibility remain unverified. Do not claim a running deployment.

Official references: https://docs.openwebui.com/getting-started/quick-start/ ; https://docs.openwebui.com/reference/env-configuration/ ; https://docs.openwebui.com/getting-started/advanced-topics/hardening/ .
