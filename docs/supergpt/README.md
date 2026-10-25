# SuperGPT — canonical project index

**Project ID:** BHM-SUPERGPT | **Owner:** Business House Matrix | **Version:** 1.0 | **Date:** 2026-10-25

**THIS FILE IS THE SUPERGPT SOURCE-OF-TRUTH ENTRYPOINT.** SuperGPT is a distinct mobile/desktop-facing product within Business House Matrix, not a replacement for the Matrix governance system and not an extension of Moksha or Andaz.

## Read in this order

1. [Project plan and execution backlog](PROJECT_PLAN.md) — product scope, architecture, work packages, current facts and acceptance criteria.
2. [Release policy and branch controls](RELEASE_POLICY.md) — dev/test/production gates, reviewer requirements, promotion procedure, rollback.
3. [Verified release-gate checkpoint](RELEASE_GATE_STATUS_2026-10-25.md) — real CI receipts and outstanding GitHub administrator enforcement ([Issue #23](https://github.com/aarondash5-star/business-house-matrix/issues/23)).
4. [Release QA evidence record](qa/RELEASE_EVIDENCE.json) — machine-readable candidate status; **pending means not certified**.
5. [QA procedure](qa/EVIDENCE_GUIDE.md) — collection and independent-verification protocol.
6. [CI policy gate](../../scripts/supergpt/release_gate.py) and [CI workflow](../../.github/workflows/supergpt-release-gates.yml).
7. [Android prototype build workflow](../../.github/workflows/supergpt-android-debug.yml).

## Authority and inheritance

Global Business House Matrix governance is authoritative for SuperGPT too:
- [Super Brain operating charter](../governance/SUPER_BRAIN_OPERATING_CHARTER.md)
- [Department routing and handoff](../governance/DEPARTMENT_ROUTING_AND_HANDOFF.md)
- [Approved task envelope schema](../../brain/governance/task-envelope-v1.schema.json)

Precedence: platform/security constraints > specific latest owner approvals > Matrix governance > this project plan > implementation notes. A GitHub commit, CI pass, prepared task or artifact does not prove that the departmental Brain executed or that runtime QA passed.

## Branches and source-of-truth rule

- `super-gpt/dev`: **editable canonical product plan and implementation work**.
- `super-gpt/test`: promotion candidates for independent QA; do not treat as production.
- `super-gpt/production`: accepted release source only; a branch existing does not mean a production deployment occurred.
- `main`: shared Matrix governance and discoverability; project-specific working specification is this index on `super-gpt/dev`.

Change project requirements on `super-gpt/dev` with explicit decision records. Promote through pull requests only after applicable checks. If any branch copy differs, **the approved plan on dev is the latest working specification**, but a production release is governed by the frozen plan/evidence in that release commit. Never rewrite release history to match later plans.

## Actual baseline as of 2026-10-25

The existing `supergpt-android-debug.yml` workflow produced a successful **standalone PocketPal-derived prototype** artifact from [GitHub Actions run 40080604622](https://github.com/aarondash5-star/business-house-matrix/actions/runs/40080604622). This is NOT proof of integration with the Matrix Brain or a finished SuperGPT app. The earlier APK build problems involved Google Services configuration and Firebase App Check linking; the revised workflow compiled. The artifact is a ZIP from Actions containing the APK, not an independently approved production package.

Dell has virtualization support and the KVM device exists; the generic SSH execution identity reported `KVM_ACCESS_DENIED`. Lightweight emulator installation and Android installation/cold-start/crash-free certification remain **unverified**. Do not promote the product to production on CI compilation alone.

**Operational status: planning/branch bootstrap; prototype build passing; end-to-end runtime, Brain integration, security review and production acceptance pending.**
