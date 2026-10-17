# Business House AI Matrix — Open WebUI-first free/self-hosted pilot rollout

**Rollout decision:** 2026-10-18. **Target deployment:** Pending host selection; do not claim a live deployment until Docker smoke tests and access checks pass.

## New deployment order (supersedes previous phase order)

| Gate | Component | Outcome | Required evidence |
|---|---|---|---|
| P0 | Isolate and preflight host | Independent project directory, Docker Compose with validated rendered configuration, host resources, loopback-only exposure, storage/backups | Hardware and security preflight report |
| P1 | **Open WebUI first** | Reviewed upstream Docker image starts via standalone Compose on localhost with persistent application data; admin account is created over trusted loopback; disable sign-ups afterward | Compose config check, health/HTTP, UI screenshots, login, restart/persistence |
| P2 | Local inference | Add permitted local open-weight model via Ollama without paid API; ensure inference endpoint is not exposed on LAN | Successful streamed conversation, latency and model-license report |
| P3 | LangGraph Central Brain | Authenticated adapter to main Brain + one departmental subgraph; UI stays just the operator interface | Delegation trace and correctness tests |
| P4 | Temporal | Durable execution with safe task retries and long approval waits | Restart, timeout, recovery and idempotency tests |
| P5 | MCP tools | One read-only FastMCP capability and scoped authorization; ContextForge only when required | Access and denial audit |
| P6 | Pilot QA and EVOLUTION | QA evaluates real outcomes; EVOLUTION proposes tested corrections without deploying itself | Measured evaluation, rollback and review |
| P7 | Pilot acceptance then departmental expansion | Bring remaining brains online gradually | Signed pilot acceptance and performance metrics |
| P8 | **Optional OpenClaw evaluation** | Only after accepted pilot: independently assess messaging/device operations | Separate review and approval; no auto-install |

### Immediate delivery scope

The `pilot/` directory provides a **portable, source-reusing setup pack** for a local-only Open WebUI proof. There are no server credentials and no OpenClaw config in the pack. It does not install Open WebUI into this ChatGPT runtime. When a reachable host is selected, verify the official image version/digest, run the pilot Compose configuration preflight, and inspect published ports before starting services.

### Pilot security rules

- Use a standalone Compose file with an explicit `127.0.0.1:3000:8080` mapping, **not** an upstream overlay; verify `docker compose config` and container binding before access. Pin a reviewed image tag or digest, never a floating `main` tag in production.
- Keep the initial UI on loopback with SSH tunnelling for a remote host. Do not expose unencrypted HTTP directly to the internet. Protect the Docker socket.
- Open WebUI's first registered user becomes administrator. Temporarily allow signup on loopback during bootstrap only, then set `ENABLE_SIGNUP=false` in the configuration and verify it stays disabled; keep `WEBUI_AUTH=true` from day one. Back up its data volume and `WEBUI_SECRET_KEY` securely.
- Start with read-only actions and no autonomous publishing, payment, email, terminal access or machine control. Passwords and API keys must never be committed to Git.
- Avoid using rolling image tags for broader rollout. Record the upstream Git SHA and actual pulled image digests during pilot, then pin approved versions for subsequent environments.

## Cost and licence requirements

- **Software:** prefer self-hosted, OSI-open-source releases; **Open WebUI is an explicit free/source-available licence exception** with branding restrictions. Do not misrepresent it as OSI-open-source. No hosted plan is mandatory.
- **Model:** choose a specific permissively licensed open-weight model and pin version, weights and licence in the deployment manifest. "Works with Ollama" is not itself a licence clearance.
- **Infrastructure:** first reuse existing available machines after measured capacity; only propose paid compute/hosting if benchmarks show it is necessary.
- **Cloud free tiers:** optional for staging/off-site facilities; do not make auto-pausing/free databases an unexamined single point of failure for workflow history or memory.
- **Additional services:** No NATS, secondary observability platform or custom cron/heartbeats in the baseline unless proven necessary beyond Temporal's built-ins.

## Operational engineering safeguards

Temporal controls the durable outer workflow and worker retry lifecycle. LangGraph controls agent logic and local correction logic. MCP exposes external actions with server-side policies. For every side effect, define idempotency key, timeout, log identifier and approval policy. EVOLUTION feedback does not override security gates. Deploy departmental scopes incrementally, keeping high-risk Accounts and public-facing Support actions read-only until approved.

## Evidence required at each stage

Record: exact component version and licence, upstream repo/reuse decision, threat-model delta, resource measurement, test logs, failure/recovery test, permissions evidence, rollback plan, and the approver. Store these as independent Business House Matrix documentation only.

## Exclusions (until separately approved)

- No production deployment, external API credentials, publishing, payments or business record changes.
- No integration into the Moksha Master or shared master synchronization.
- No paid AI APIs, subscriptions, or hosted Temporal dependency in the base plan.
- No LibreChat deployment in the pilot. OpenClaw remains deferred until explicit acceptance of the Open WebUI pilot.
