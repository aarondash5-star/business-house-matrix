# Dell Dev Matrix: private static website staging (2026-10-22)

## Capability
A live, narrowly gated `website_stage` action now exists in the existing Dell central controller, with no new daemon, paid service, WordPress access, external staging hostname, or browser installation.

Versioned source:
- `brain/mvp-controller/site_staging.py`
- `brain/mvp-controller/manifests/moksha_overhaul_v1.json`
- `brain/mvp-controller/test_site_staging.py`
- `brain/mvp-controller/controller.py` (`website_stage` allowlist + queue fairness)

## Scope and security
- Approved `project=moksha_overhaul`, `brief=moksha_overhaul_v1` **only**. All other project/manifest values are rejected by the controller; do not silently expand.
- A manifest is strictly validated as bounded plain text, known page slugs and sections, internal local CTA links and a limited image role vocabulary.
- No arbitrary HTML, template rendering from untrusted input, JS execution, remote URLs, contact forms, payments, external resources or WordPress writes. Input text is HTML-escaped. CSS is fixed/versioned. No subprocess shell is selected by any model.
- Real local images require named allowed filenames, file signature/size and explicit rights/provenance fields. The current initial manifest contains **no photo assets**: all image positions display labeled visual placeholders. Treat final authentic photos and image licensing as pending—not complete.
- Builds are content-addressed and idempotent (SHA-256 manifest prefix), stored in a 0700-owned private folder; files default to owner read/write. `robots.txt` and `noindex,nofollow` supplement **filesystem access isolation**, not a substitute for auth.
- Preview has **no listening web server, no public URL**. A later remote viewing method needs its own explicit owner authentication and QA. Do not link to an unauthorized public URL.
- Live Moksha 24-Oct retreat page, WooCommerce checkout, PMS, WordPress theme, production analytics, SEO, assets and customer orders remain untouched.
- Mac↔Dell encrypted research relay, Mac Marketing Brain and other Dell projects unchanged.
- Existing Dell controller service `bhm-autonomy-controller.service` is boot-enabled and active; queue processes preview build without letting unrelated delegated proposals indefinitely block bounded safe tasks.

## Verified release receipts
- GitHub source commits: compiler `5161ac896f9d2a848f7590294db4a8d71bca64e4`, manifest `bc5afe5128b037d225b7f4fd6b6be6ba96d91a06`, controller route `391381de535103d0055025934a9d1e51a02a3004`, tests `f0fdf9648a1ce87f05d0869d00ed2e244106d753`, fairness `c32df0b66cf62278407e18e139c626f69f941bdb`.
- Dell isolated safety tests: **7/7** PASS, stdlib only. Controller `selftest` PASS. Preview fixture validation accepted 9 pages.
- Dell production-controller installation service active and readback includes `website_stage: private_static_staging_only`.
- Autonomous queued build job `fe6f8507-da1a-4feb-bee0-8ddf02e6a038`: **completed**, attempt 1, QA `private_static_preview_qa`, `private_preview_ready`, **9 local HTML pages**, `nonindexed=true`, `publication=false`, `spend=false`.
- Source manifest digest `31e9344592a08813`. Actual private path:
  `/var/lib/generic-linux-automator-exec/matrix-controller/staging-private/moksha_overhaul/31e9344592a08813`.
- A real headless Firefox screenshot for 390×820 mobile viewport was produced and saved privately as `preview-mobile-firefox.png` (94KB). Screenshot existence confirms headless rendering, **not a completed human visual review**.
- Playwright's npm package is installed but its standalone browser executable is absent; the first Playwright smoke attempt failed, and existing MPL-licensed Firefox was used instead. Do not install a heavy proprietary browser or mark Playwright screenshots PASS without actual evidence.
- No cloud/production screenshots were made publicly visible or pushed to GitHub.
- Initial Dev proposal `9392c6ee-ce40-4457-9e5d-acf7d646402b` returned `needs_review` and remains *proposal-only*. The private 9-page preview was produced by the separately verified static manifest builder, not generated from that incomplete Dev proposal.
- Marketing research was separately verified via Mac receipts `49b32b3c-3c57-4ca1-b35e-686df61ec7f4` and `7951f864-ba06-41ce-9260-7d15579b5257`. No automatic cross-host creative-to-staging manifest transfer is yet proven.

## Operator commands
Via authenticated Dell Generic Linux SSH nonroot shell:
```bash
D=/var/lib/generic-linux-automator-exec/matrix-controller
python3 "$D/site_staging.py" validate moksha_overhaul moksha_overhaul_v1
python3 "$D/controller.py" submit moksha_overhaul website_stage moksha_overhaul_v1 --key moksha-website-private-staging-20261022-v1
python3 "$D/controller.py" show fe6f8507-da1a-4feb-bee0-8ddf02e6a038
python3 "$D/controller.py" status
```

## Current blockers for finished owner review
1. Marketing Brain's design brief and research evidence need synthesis into a reviewed second manifest, then automatically/explicitly routed through validation. Current fixed manifest is a functional baseline, not evidence of an end-to-end autonomous creative iteration.
2. Replace labeled gradient placeholders with verified real Moksha photos or properly attributed rights-cleared placeholder photographs; never imply synthetic imagery is onsite.
3. Human visual review, multiple mobile breakpoints, accessibility and realistic WordPress staging integration remain unfinished. **No public authenticated staging link exists**. Do not call the site production-ready.
4. Preserve user approval gate before production changes, live booking functionality, public preview or advertising spend.

## Rollback
Retained live backups:
- `controller.py.pre-private-staging-20261022`
- `controller.py.pre-fairness-20261022`

To roll back just this route, restore the first backup through owner-authorized SSH, run `selftest`, restart only `bhm-autonomy-controller.service` and check `is-active`; do not remove unrelated queues or prior receipts. Leave photo/manifest/input files isolated as needed.
