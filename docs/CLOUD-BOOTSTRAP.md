# Cloud CLI bootstrap checklist — authorization required

**State:** NOT CONNECTED TO CLOUD; NO RESOURCE CREATED.

## Oracle Cloud (preferred)

1. Confirm the Matrix's own Oracle tenancy ID, compartment, region, real Always Free Arm compute capacity and required service limits. Record IDs only after separate access verification; do not borrow another project's production cloud identity.
2. Verify a compliant supported authentication approach for GitHub OIDC token exchange or another explicitly approved narrowly scoped bootstrapping process.
3. Restrict rights to a dedicated compartment and safe resource types. Block provisioning of paid VM shapes and unreviewed public networking.
4. Before any apply/deploy, run read-only `oci iam region list` / relevant `oci limits` and compute queries using authenticated runner credentials.
5. Only after a separate review: provision OCI VM, persistent storage and restricted networking; attach an HTTPS reverse proxy to a reviewed, immutable Open WebUI image.
6. Verify durable app data, backup export/restore, signup-disabled authentication and update/rollback.

## Google Cloud (fallback)

1. Confirm the Matrix-specific GCP project and billing settings, Cloud Run availability, account permissions and free usage estimate; billing alerts are not hard caps.
2. Establish Workload Identity Federation for GitHub repository `aarondash5-star/business-house-matrix`, scoped to an approved environment/branch and limited service account.
3. Configure approved variables such as `GCP_PROJECT_ID`, `GCP_WIF_PROVIDER` and `GCP_SERVICE_ACCOUNT` in GitHub environment settings, not source.
4. Start with read-only `gcloud run services describe` and metadata checks; do not deploy before verifying the image architecture, model-backend plan and database persistence. Cloud Run is not a drop-in home for the full Matrix.
5. Create a manual, environment-gated deploy workflow only after IAM, cost, external database and backup are approved.

## Repository workflow policy

- Untrusted PRs may run compile, tests and offline scans only.
- Deployment workflow must require explicit `workflow_dispatch`, reviewed commit SHA and GitHub Environment approval; no automatic cloud provisioning.
- GitHub Actions orchestrates CLIs; it is not a permanent cloud worker. No SSH private keys, cloud access tokens or database connections in Git.
- No OpenClaw or LibreChat in the Open WebUI pilot. Do not activate the legacy Render blueprint.
