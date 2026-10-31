# MAD Mac — Official ChatGPT Linux Desktop Preview Installation Receipt

Date: 2026-10-31 (Asia/Kolkata). Host: `KARAN` (MacBook Air running Linux Mint 22.3 Zena, Ubuntu 24.04 Noble base; amd64).  
**Status:** VERIFIED INSTALLED, **not launched or sign-in tested**, thermal A/B pilot pending.

## Source and installation
- Official OpenAI Linux preview install documentation: https://learn.chatgpt.com/docs/linux/linux-app.md
- Official OpenAI CDN package: https://persistent.oaistatic.com/codex-app-prod/linux/deb/latest/chatgpt_amd64.deb
- Exact downloaded size: 534,538,410 bytes; source HTTP 200 and TLS verification success; Last-Modified 2026-10-29.
- Downloaded file SHA-256: `4e139a44f7c917a643f2dd014ad32298dd30aec6d324d323524b190f7667684c`.
- Dpkg identity: `chatgpt 26.1027.30824 amd64`, Maintainer `OpenAI <support@openai.com>`.
- Preflight APT simulation: 0 upgraded, **1 newly installed**, 0 removed.
- Command: `sudo apt-get -y -o Dpkg::Use-Pty=0 --no-install-recommends install /var/lib/generic-linux-automator-exec/.cache/chatgpt-official/chatgpt_amd64.deb`.
- Verified: `chatgpt 26.1027.30824 install ok installed`, binary `/usr/bin/chatgpt` (launcher `/usr/lib/chatgpt/codex-launcher`), desktop menu `/usr/share/applications/chatgpt.desktop`.
- Installer configured official signed APT repository `https://persistent.oaistatic.com/codex-app-prod/linux/deb` with keyring `/usr/share/keyrings/chatgpt-archive-keyring.gpg`.
- Repository/package is OpenAI proprietary; **no open-source attribution or copying of third-party code**. Software installation free, account service entitlements separate. Linux Mint is **not** listed as formally supported (Ubuntu 24.04 is). No paid calls.
- Existing Firefox profile, MAD services and on-demand video editor remained unchanged. Editor verified inactive.

## Thermal safety
- Initial preflight CPU sensor TC0F approximately 74.8°C, later cooled to 70.5°C before installation.
- Package decompression briefly caused approximately **95°C** and fan ~6500 RPM. A separate monitoring sample recorded ~94.5°C during unpack; installation then finished successfully and CPU temperature dropped to ~85.5°C. Final postinstallation TC0F **77.5°C**; fan ~6197 RPM.
- **The desktop app was not launched.** Do not declare lower heat vs Firefox until controlled separate-workload A/B thermal test passes; avoid running browser and desktop concurrently during test.
- Do not start additional resident services or local inference while thermal headroom is unsafe.

## Verification and rollback
- Install tool receipt ID `3e3fc486431646e8bbc2379fd8821742` completed with exit 0; postinstall verification `b216dd0cde244fefb9d04759277a4a11` completed with exit 0.
- To uninstall only on owner's explicit follow-up: `sudo apt remove chatgpt`; review package-created repository/keyring before separately removing them. Do not use `autoremove` blindly.
- No user login, OAuth, desktop application smoke, web workload or 24/7 reliability certification performed.
- No unrelated projects, user browser tabs, tenant credentials, WordPress sites or cloud accounts modified.
