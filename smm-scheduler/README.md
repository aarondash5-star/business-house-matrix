# SMM Scheduler V1 (read-only safety baseline)

Minimal, zero-dependency Python scheduler with GitHub Actions. The engine controls timing independently of the provider. No media, UI, Cloudflare or database needed.

## Implemented
- Strictly read-only FanSMM v2 adapter: services, balance, status.
- Internal due-time queue with configurable interval for each job.
- Persisted state.json, atomic writes, dry-run preview, disabled jobs.
- Sanitized errors and bounded retries, 14 mock-based unit tests.
- A GitHub cron/manual workflow. No billable order creation.

## Run on Dell or locally
Run: python3 -m unittest discover -s tests -v
Preview: python3 scheduler.py
Execute read-only: python3 scheduler.py --execute-read-only

## Job schema
jobs.json initially contains an empty jobs array. To add a read-only balance check:
  {"jobs":[{"id":"balance-monitor","provider":"fansmm","action":"balance","interval_minutes":60,"enabled":false}]}
For status monitoring use action=status and params={"order":"23501"} with an existing authorized order ID.
Set FANSMM_API_KEY as a GitHub Actions secret, never in the repository.

## Operating limits
GitHub scheduled workflows are best effort; 15-minute workflow cron.
Individual intervals are enforced by scheduler.py, not provider drip parameters.
GitHub state.json pushes may be blocked by branch protection. This design is suitable for read-only polling, NOT safe non-idempotent paid operations. Chargeable actions require a transactional ledger, proven idempotency, explicit approval, and anti-abuse checks.
An empty job list is an inert live deployment.

## Additional adapters
New providers can implement the same call(action, params) interface; schedule semantics stay unchanged.

## Aarondash GitHub credential handoff

1. Open https://github.com/aarondash5-star/business-house-matrix/settings/secrets/actions
2. Add a new repository secret named `FANSMM_API_KEY` (paste the key only in GitHub).
3. Open https://github.com/aarondash5-star/business-house-matrix/actions/workflows/smm-scheduler-certify.yml
4. Run the workflow manually on the default branch.

The certification flow runs synthetic tests, verifies that the empty queue executes without orders, then invokes the FanSMM `services` and `balance` endpoints. It displays only a pass/fail status and service count, never the key or the account balance.

The recurring scheduler workflow is `.github/workflows/smm-scheduler.yml`. It has no enabled jobs by default. Do not store secrets in configuration files, issues, or workflow dispatch inputs.

## Production read-only monitoring (enabled)

The default job queue now includes:
- `fansmm-services`: retrieve the current catalogue once every 1440 minutes (24 hours).
- `fansmm-balance`: verify account balance once every 60 minutes.

The GitHub scheduler wakes up every 15 minutes, uses its own due-time state, and records only success/failure metadata, never prices, key, or account balances.

For an existing order, manually open the **SMM Scheduler V1 - Certification** GitHub Actions workflow, select **Run workflow**, and optionally supply a numeric `order_id`. This invokes only `status`, without creating or modifying an order.

**Not enabled:** any `add` requests or purchased follower, view, comment, or like orders. The scheduler does not try to disguise inauthentic engagement as organic.
