#!/usr/bin/env bash
set -euo pipefail
THIRD_PARTY="${HOME}/matrix-game-toolkit-20261025/third_party"
BLENDER="${THIRD_PARTY}/blender/blender-4.5.15-linux-x64/blender"
if [[ ! -x "${BLENDER}" ]]; then echo "Blender LTS missing" >&2; exit 20; fi
export XDG_CONFIG_HOME="${THIRD_PARTY}/blender-xdg-config"
exec "${BLENDER}" -b -noaudio "$@"