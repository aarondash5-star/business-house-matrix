# Dev Matrix NVIDIA integration — 23 October 2026 IST

## Current decision
KEY_ENROLLED / ADAPTER_TESTED / LIVE_INFERENCE_NOT_VERIFIED. Two public development GPT-OSS20 requests timed out (first 15-second socket bound, second 45-second socket bound with a 60-second total deadline). No successful authenticated NVIDIA completion or model-generated QA is claimed. NVIDIA routes are disabled; preserve Groq and local fallback. No automatic retry or production activation.

## Verified credential and transport
Owner completed existing secure browser entry. Receipt d5376c6f-fa31-46fb-b260-43e868d09e21 completed exit0: nvidia-oss20 credential exists, private permissions, not symlink. No secret printed, copied to another host, stored in repo, or used in shell arguments. No new gateway created.

No raw key is needed in subsequent chat. NVIDIA public /models is not an authentication check. Credential validity remains unproven until an authenticated completion succeeds.

## Bounded adapter and source
Extended existing router's text adapter, retaining groq_text compatibility and adding nvidia_text with fixed https://integrate.api.nvidia.com/v1/chat/completions. NVIDIA uses max_tokens1024, public input <=2048 bytes, no tools, no redirects, response <=65536 bytes, output <=8192 bytes, incomplete output rejected. NVIDIA final timeouts: socket45sec, total alarm60sec; Groq retains socket15sec/total30sec.

Every NVIDIA call requires BOTH --public-input and --development-test. Missing development flag rejects before an API reservation. Public tasks without --development-test exclude NVIDIA even if a slot is enabled. Only openai/gpt-oss-20b is accepted by this new NVIDIA path. Existing Nemotron license flag retained; no attempt to activate it. Trial/development-only scope preserved, no production service usage.

Separate NVIDIA token-reservation table avoids changing the historical Groq ledger. Local NVIDIA caps5/day,1/minute plus7600 reserved token units/minute and20000/day. Prompt bytes+1536 reserved conservatively before sending, including failed calls. These caps/owner Free-development attestation are not provider-confirmed billing or external usage audits.

Runtime source SHA25690cf35dd3dc3d8da48efdba62aa487f62feabcde47b4938beb2ebf64e4fa388c. Git source commit fedd9bd03c2f85ebb8bd69809dd5e2396955ab82, tests289097df9653e7660d3e761d34c28095e0441036, evaluator4bd378483c7eef2fa5aac7fdaf09b3074c605792 on feat/dev-groq-api-20261023. Source files brain/dev-router/matrix-route.py, test_api.py and smoke_nvidia.py. No merge.

## Executed QA and failures
- Initial candidate25/25 unittest cases PASS, Dell receipt dda6784a-010b-4e74-86a3-20328b1c7eff exit0. The suite includes inherited repeated Groq tests plus three NVIDIA-specific development, payload and license tests; 25 is executed case count, not25 independent new security properties.
- Final longer NVIDIA deadline candidate25/25 PASS on Dell, receipt2a52eb14-ebee-455b-988a-1424ef532e63 exit0. Same final source/tests independently executed in ChatGPT scratch25/25 exit0. No live credentials/network calls in those tests.
- First bounded live smoke5f18b40a-5feb-4970-893a-266606f495dc failed exit1 with NVIDIA_REQUEST_FAILED_TimeoutError. Model evaluator never ran because inference did not complete.
- Exactly one later bounded attempt after the1/minute guard: c3b68b43-4000-4392-9f03-e6edfbe99724 failed exit1 with same timeout after~45sec. No model QA PASS.
- Basic independent connectivity: f24f7903-d456-4ecd-9042-b5033260bfac exit0; IPv4 DNS resolution and TLS1.3 handshake succeeded in0.12sec to integrate.api.nvidia.com. This narrows the issue beyond basic DNS/TLS reachability; precise inference/server cause remains unverified. Do not assert it proves key authorization or provider health.
- Postflight12e247a3-6b66-4ef1-a59d-7fa89b54a359 exit0: Groq policy identical to pre-NVIDIA snapshot; Nemotron license gate true; v6 ACTIVE and protected controller checksum unchanged b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e. Read-only missing-development-flag check earlier2c1607e7-99b7-45ed-9390-05a9e00a079a exit0: CLI exit2 and reservation count unchanged.

## Paused state and rollback
After the two timeouts, disabled nvidia-oss20 using existing router CLI and retained nvidia-nemotron-ultra disabled. Added a900-second conservative local cooldown marker using existing simulate-429 command. The command name is historical; NVIDIA did NOT return429 here. This is local timeout backoff only and does not auto-enable a disabled slot. Pause/readback task d46de865-fcbd-4565-a1f8-e154ffa2e29a must have a terminal receipt before asserting its success.

Enrollment terminal was closed with its specific transient unit; existing browser profiles, relay, root/sudo rights and v6/SSH services preserved.

Pre-NVIDIA router/policy copies at ~/.local/share/matrix-dev-router/backup-nvidia-20261023 preserve the working Groq release. Keep all credential files, quota ledgers, failure receipts and staged snapshots. To revert this adapter, reconcile newer changes then restore those exact files with original modes; do not restore the older pre-Groq backup. No permissions, account plan, package installation, paid service or security bypass used.

Next: use provider status/account support or one separately authorized, quota-aware later development check to establish why this model request stalls; do not keep extending deadlines or loop retries. Then require an actual authenticated completion and six independent no-network Bubblewrap assertions before enabling NVIDIA. Public NVIDIA inventory alone is insufficient.

## Primary references and reuse/cost gate
Reuse existing stdlib/SQLite router and vault, secure relay and Bubblewrap evaluator; no new SDK/dependency installed. Official provider request schema https://docs.api.nvidia.com/nim/reference/openai-gpt-oss-20b-infer documents endpoint, max_tokens and low/medium/high reasoning. https://build.nvidia.com/openai/gpt-oss-20b advertises its free prototyping endpoint. GPT-OSS20 Apache2.0 license verified earlier from original publisher. Trial terms and billing account not independently audited. Nemotron OpenMDW1.1/OSI review remains unresolved; no license gate waived. Business House Matrix remains independent from Moksha Master; Gate E production certification unchanged.
