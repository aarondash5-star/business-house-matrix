# GitHub transfer — Aaron account

Target account: `aarondash5-star` (confirmed connected GitHub account).
Intended repository: **private** `business-house-matrix`.
Canonical source branch: `main`.

## Transfer rules
- This project is **independent from Moksha Master**, all business and other GitHub repositories.
- Preserve source history when possible. Do not commit credentials, local `.env` files, databases, logs, uploads or cloud identity material.
- New cloud deployment decision is `docs/ADR-0003-github-cloud-control.md` and its rollout plan. **Oracle Always Free primary**, **Google Cloud Run fallback**, **Open WebUI pilot first**, **OpenClaw deferred**.
- `render.yaml` and the earlier Render deployment documents are **historical / not approved for execution**. The repository has no approved executable Oracle/GCP production workflows yet.
- Repository import by itself does **not** deploy cloud services or create/transfer runtime databases.

## What was audited
- The 20 tracked files in the local Git starter were reviewed for file names and obvious embedded credential assignments. An `.env.example` is an illustrative template and does not contain real credentials.
- `git bundle` provides an offline Git history copy, including the latest documentation commit. Secret-scanning CI must be added prior to enabling deployments.

## After remote creation
- Create an **empty private** repository named `business-house-matrix` in the Aaron account (no auto-generated README, license, or gitignore).
- Push/import the prepared Git bundle via authenticated Git CLI, or write the prepared files through the connected GitHub interface. Validate commit and file count.
- Do not enable cloud workflows before separate approvals and actual provider credentials.
