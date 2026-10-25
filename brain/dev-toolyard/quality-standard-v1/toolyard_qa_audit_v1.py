"""Read-only QA coverage inventory. Never treats an installed executable as certified."""
import hashlib
import json
import shutil
from pathlib import Path
import controller
from toolyard_qa_standard_v1 import verify_coverage,VERSION
ROOT=Path(__file__).resolve().parent
TOOLS=("python3","node","npm","git","blender","ffmpeg","google-chrome","podman","npx","gh","vercel","pytest")
PROJECT_DIRS=("threejs-tool-yard","matrix-game-toolkit-20261025","delulu-site-v2-20261025","matrix-andaz-site-v2-20261023","wp-manager-oauth-gate-20261025","eccrm-wordpress-qa-20261025")
def report():
    state=controller.status(limit=0)
    covered=verify_coverage(controller.ALLOWED)
    source=(ROOT/"controller.py").read_text()
    plugged="output=universal_qa_receipt(" in source
    return {"policy":VERSION,"controller_version":state["controller_version"],
      "controller_sha256":hashlib.sha256((ROOT/"controller.py").read_bytes()).hexdigest(),
      "registered_actions":covered,
      "enforcement_status":"controller_mediated_actions_only" if plugged and covered["complete"] else "not_fully_installed",
      "owner_release_controls_unchanged":True,"automatic_publish_authorized":False,
      "standalone_tool_inventory":{x:{"installed":bool(shutil.which(x)),"controller_interception_certified":False} for x in TOOLS},
      "workspace_inventory":{x:{"present":(ROOT.parent/x).is_dir(),"standalone_hooks_certified":False} for x in PROJECT_DIRS},
      "legacy_jobs_recertified":False,"independent_human_qa_auto_granted":False,
      "unmediated_external_connectors_certified":False}
if __name__=="__main__":print(json.dumps(report(),indent=2))
