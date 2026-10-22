#!/usr/bin/env python3
"""Second exact-scope autonomous build: reuses the independently reviewed V3 runner.

No runtime enrollment, parameterized path input, external Git write or private tenant.
The model controls only a static synthetic HTML content field.
"""
import importlib.util
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
TASK="dev_matrix_synthetic_release_v1"

def run():
    spec=importlib.util.spec_from_file_location("reviewed_content_agent",HERE/"strict_content_agent_v3.py")
    pilot=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pilot)
    pilot.TASK=TASK
    pilot.APP="frontend/dev-autonomy-validated-v1.html"
    pilot.TEST="tests/test_dev_autonomy_validated_v1.py"
    pilot.STATE=HERE/"autonomous-code-state"/TASK
    pilot.TEST_SOURCE=pilot.TEST_SOURCE.replace("pine-chat-a11y.html","dev-autonomy-validated-v1.html")
    return pilot.run()

if __name__=="__main__":
    if len(sys.argv)!=2 or sys.argv[1]!=TASK:
        print(json.dumps({"status":"blocked","reason":"manifest_not_enrolled"}))
        sys.exit(2)
    result=run()
    print(json.dumps({"task":TASK,"status":result["status"],
                      "passed":result.get("qa",{}).get("passed"),
                      "local_review_commit":result.get("review",{}).get("commit"),
                      "published":False}))
    sys.exit(0 if result["status"]=="verified_local_review" else 2)
