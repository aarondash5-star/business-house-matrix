#!/usr/bin/env python3
"""Fixed, offline-only Shaadi authoring/QA recipes. Never accepts a shell command.

An installed toolkit is *not* permission to edit Claude's game or other projects.
This is a technical/QA executor; its outcome cannot authorize publication.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import shutil
import subprocess
import sys
import zipfile

TOOLKIT = Path("/var/lib/generic-linux-automator-exec/matrix-game-toolkit-20261025")
PROJECT = "shaadi_aunty_dodge"
LOCK_SHA256 = "1a74e11d480ce40924bb25b8fabed8c0ab1c22860c6a1f6da2fa80bff4efed37"
KENNEY_SHA256 = "cdad90853682499b94c9fda2f87678b24bfd8f3264e0ed323f6b6a27fd7c6f6f"
BLENDER_SHA256 = "0d2b8bb2efe97e6c8eb57de6b7322f8800e1984e3125b60decca5f6771e4773e"
MPFB_SOURCE_SHA = "d0a32e57a7f915cb2f2b95410e2117648c7bbb7e"
MPFB_EXTENSION_SHA256 = "beb73316dbf41e2ba600bb2fbf1bb4d3c6a74ec89a09ed60b81e9374e0092e10"
RUNS = {
    "shaadi_toolkit_verify_v1": "verify",
    "shaadi_toolkit_smoke_v1": "node_smoke",
    "shaadi_mpfb_verify_v1": "blender_import",
    "shaadi_kenney_inventory_v1": "asset_inventory",
    "shaadi_gltf_cli_v1": "gltf_cli",
}
SLUG = re.compile(r"^[a-z][a-z0-9_]{2,39}$")
BWRAP = Path("/usr/bin/bwrap")
NODE = Path("/usr/local/bin/node")
MAX_OUTPUT = 10000

class ToolkitDenied(ValueError):
    pass

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def validate(project: str, manifest: str, root: Path = TOOLKIT) -> dict:
    if project != PROJECT or not isinstance(manifest, str) or not SLUG.fullmatch(manifest) or manifest not in RUNS:
        raise ToolkitDenied("project_or_recipe_not_enrolled")
    if root.is_symlink() or not root.is_dir():
        raise ToolkitDenied("toolkit_missing_or_symlink")
    lock = root / "package-lock.json"
    metadata = root / "toolchain-manifest.json"
    if any(p.is_symlink() or not p.is_file() for p in (lock, metadata)):
        raise ToolkitDenied("pinned_manifest_missing_or_symlink")
    if lock.stat().st_size > 350000 or digest(lock) != LOCK_SHA256:
        raise ToolkitDenied("package_lock_drift")
    if metadata.stat().st_size > 12000:
        raise ToolkitDenied("toolchain_manifest_oversize")
    data = json.loads(metadata.read_text(encoding="utf-8"))
    if (data.get("schema_version") != 1 or data.get("name") != "matrix-shaadi-game-development-toolkit"
            or data.get("package_lock_sha256") != LOCK_SHA256):
        raise ToolkitDenied("toolchain_manifest_contract_drift")
    checks = {"lock_sha256": LOCK_SHA256, "source": "local_pinned_oss_toolkit",
              "project": project, "manifest": manifest, "installed": True}
    if RUNS[manifest] == "blender_import":
        extension = root / "third_party/downloads/mpfb2-v2.0.18-pinned.zip"
        config = root / "third_party/blender-xdg-config"
        exe = root / "third_party/blender/blender-4.5.15-linux-x64/blender"
        if any(p.is_symlink() for p in (extension, config, exe)) or not exe.is_file() or not config.is_dir():
            raise ToolkitDenied("mpfb_dependencies_missing")
        # Verify extension identity. The 378 MB official Blender archive was verified on installation.
        if digest(extension) != MPFB_EXTENSION_SHA256 or data.get("mpfb", {}).get("source_commit") != MPFB_SOURCE_SHA:
            raise ToolkitDenied("mpfb_source_drift")
        checks["mpfb_extension_sha256"] = MPFB_EXTENSION_SHA256
    if RUNS[manifest] == "asset_inventory":
        archive = root / "third_party/downloads/kenney_food-kit.zip"
        if archive.is_symlink() or not archive.is_file() or digest(archive) != KENNEY_SHA256:
            raise ToolkitDenied("cc0_asset_source_drift")
        checks["kenney_archive_sha256"] = KENNEY_SHA256
    if RUNS[manifest] in {"node_smoke", "gltf_cli"}:
        for f in (root / "node_modules", root / "tools/smoke.mjs"):
            if f.is_symlink() or not f.exists():
                raise ToolkitDenied("tool_binary_missing")
    return checks

def asset_inventory(root: Path) -> dict:
    archive = root / "third_party/downloads/kenney_food-kit.zip"
    with zipfile.ZipFile(archive) as z:
        if len(z.infolist()) > 3000:
            raise ToolkitDenied("asset_archive_too_large")
        names = [f.filename for f in z.infolist()]
        if any(n.startswith("/") or ".." in Path(n).parts or chr(92) in n for n in names):
            raise ToolkitDenied("asset_archive_path_not_safe")
        license_name = next((n for n in names if n == "License.txt"), None)
        if not license_name:
            raise ToolkitDenied("license_missing")
        license_text = z.read(license_name).decode("utf-8", "replace")
        if "Creative Commons Zero" not in license_text or "CC0" not in license_text:
            raise ToolkitDenied("rights_unverified")
        return {"asset_pack": "kenney_food_kit_2", "entry_count": len(names),
                "cc0_license_verified": True, "source_sha256": KENNEY_SHA256}

def _limits() -> None:
    resource.setrlimit(resource.RLIMIT_CPU, (65, 65))
    resource.setrlimit(resource.RLIMIT_NOFILE, (256, 256))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))

def _sandbox_command(recipe: str, root: Path) -> list[str]:
    """Completely static executable and args; network, other homes and projects hidden."""
    if not BWRAP.is_file():
        raise ToolkitDenied("bubblewrap_required")
    cmd = [str(BWRAP), "--unshare-all", "--new-session", "--die-with-parent"]
    for location in ("/usr", "/opt", "/bin", "/lib", "/lib64", "/etc"):
        if Path(location).exists():
            cmd += ["--ro-bind", location, location]
    cmd += ["--ro-bind", str(root), "/toolkit",
            "--dev", "/dev", "--proc", "/proc",
            "--tmpfs", "/tmp", "--dir", "/empty", "--chdir", "/toolkit",
            "--setenv", "HOME", "/empty",
            "--setenv", "XDG_CACHE_HOME", "/tmp/.cache",
            "--setenv", "PATH", "/usr/local/bin:/usr/bin:/bin"]
    if recipe == "node_smoke":
        return cmd + [str(NODE), "/toolkit/tools/smoke.mjs"]
    if recipe == "gltf_cli":
        return cmd + ["/toolkit/node_modules/.bin/gltf-transform", "--version"]
    if recipe == "blender_import":
        # Overlay only MPFB's log directory with disposable writable tmpfs.
        # The pinned extension and every other toolkit file remain read-only.
        cmd += ["--tmpfs", "/toolkit/third_party/blender-xdg-config/blender/4.5/mpfb/logs",
                "--setenv", "XDG_CONFIG_HOME", "/toolkit/third_party/blender-xdg-config",
                "--setenv", "BLENDER_USER_CONFIG", "/toolkit/third_party/blender-config"]
        blender = "/toolkit/third_party/blender/blender-4.5.15-linux-x64/blender"
        expr = ("import bpy,importlib; mod='bl_ext.user_default.mpfb'; "
                "importlib.import_module(mod); "
                "(bpy.ops.preferences.addon_enable(module=mod) if not bpy.context.preferences.addons.get(mod) else None); "
                "assert bpy.context.preferences.addons.get(mod), 'MPFB_NOT_REGISTERED'; "
                "print('MPFB_REGISTERED_OK',bpy.app.version_string)")
        return cmd + [blender, "-b", "--python-expr", expr]
    raise ToolkitDenied("unknown_sandbox_recipe")

def execute(project: str, manifest: str, root: Path = TOOLKIT) -> dict:
    base = validate(project, manifest, root)
    recipe = RUNS[manifest]
    result = {"project": project, "manifest": manifest, "recipe": recipe,
              "provider": "dell_isolated_toolkit", "technical_only": True,
              "qa_passed": False, "published": False, "spent": False,
              "game_repository_modified": False, "sandbox_network": "disabled"}
    result.update(base)
    if recipe == "verify":
        result["qa_passed"] = True
        result["test_kind"] = "pinned_manifest_read_only"
        return result
    if recipe == "asset_inventory":
        result.update(asset_inventory(root))
        result["qa_passed"] = True
        result["test_kind"] = "cc0_source_license_inventory"
        return result
    cmd = _sandbox_command(recipe, root)
    p = subprocess.run(cmd, cwd="/", stdin=subprocess.DEVNULL,
                       capture_output=True, text=True, timeout=95,
                       env={"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": "/nonexistent"},
                       preexec_fn=_limits)
    result["exit_code"] = p.returncode
    result["output_tail"] = p.stdout[-MAX_OUTPUT:]
    result["stderr_tail"] = p.stderr[-2000:]
    if p.returncode != 0:
        return result
    if recipe == "node_smoke":
        try:
            data = json.loads(p.stdout)
            result["checks_passed"] = data.get("passed")
            result["checks_failed"] = data.get("failed")
            result["qa_passed"] = data.get("passed") == 13 and data.get("failed") == 0
        except (ValueError,TypeError):
            result["qa_passed"] = False
    elif recipe == "gltf_cli":
        result["qa_passed"] = p.stdout.strip() == "4.5.1"
    elif recipe == "blender_import":
        result["qa_passed"] = (
            "MPFB_REGISTERED_OK 4.5.15 LTS" in p.stdout
            and "Exception in module register" not in p.stdout + p.stderr
            and "Traceback (most recent call last)" not in p.stdout + p.stderr
        )
    result["test_kind"] = "isolated_offline_tool_check"
    return result

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Fixed Shaadi Dev Matrix authoring/QA recipes")
    parser.add_argument("command", choices=("check", "run"))
    parser.add_argument("project")
    parser.add_argument("manifest")
    args = parser.parse_args()
    try:
        value = validate(args.project, args.manifest)
        if args.command == "run":
            value = execute(args.project, args.manifest)
        print(json.dumps(value, sort_keys=True))
        if args.command == "run" and not value.get("qa_passed", False):
            sys.exit(2)
    except (ToolkitDenied, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as err:
        print(json.dumps({"status": "blocked", "error": type(err).__name__,
                          "reason": str(err)[:250], "published": False,
                          "game_repository_modified": False}), file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
