# Dell Dev Tool Yard — mandatory quality standard entrypoint (2026-10-25)
Read `/var/lib/generic-linux-automator-exec/matrix-controller/docs/QA_UNIVERSAL_STANDARD_V1_20261025.md`
before accepting, building, testing or attempting to release work for ANY project
(Moksha, Andaz, Delulu, Shaadi Aunty, Pine, CRM, WP Manager, or future work).

For each controller-mediated action, the shared standard V1 is automatically
attached on task completion. For **standalone CLI and external connector work**,
execution is **NOT yet technically intercepted**; follow the same profile-based
checklist, capture genuine SHA-pinned evidence, and use the existing owner
release preflight. Never assume 10/10, independent human signoff or
production permission from a successful build.

Audit actual coverage:
`python3 /var/lib/generic-linux-automator-exec/matrix-controller/toolyard_qa_audit_v1.py`
Record gaps as pending, not certified. Never bypass host/project security controls.
Git source: aarondash5-star/business-house-matrix,
brain/dev-toolyard/quality-standard-v1/ (feature branch pending review).
