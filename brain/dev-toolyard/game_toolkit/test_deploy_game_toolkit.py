"""Fail-closed integration patch tests, without contacting Dell or restarting a service."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("deploy_game_toolkit",HERE/"deploy_game_toolkit.py")
d=importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)

FAKE_CONTROLLER = '''
ALLOWED={
 "dev_project_build":{"department":"Development","mode":"manifest_enrolled_isolated_reviewed_patch_qa"},
}
def submit(project,action,brief):
    if action=="dev_docs_fetch":
        pass
def tick(t):
    try:
        if t["action"]=="research_search":
            pass
        elif t["action"]=="dev_general_build":
            pass
    except Exception:
        pass
def status():
    return {"controller_version":"0.2.2-global-intake-governed",
            "quality_policy":{"prebuild_owner_admission_required":True}}
'''
FAKE_REGISTRY = '''ENGINES = {
    "website_stage": {"legacy_moksha", "static_v1"},
    "dev_project_build": {"reviewed_patch_v1"},
}
'''
FAKE_ADMISSION = '''RUN_ACTIONS=frozenset(("website_stage","dev_project_build","dev_general_build",
                        "dev_scoped_build","pine_chat_stage","video_preview",
                        "repair_known_issue"))
'''

class PatchTests(unittest.TestCase):
    def test_controller_restricts_added_action(self):
        code = d.controller_patch(FAKE_CONTROLLER)
        self.assertIn('"game_toolkit":{"department":"Development","mode":"owner_admitted_fixed_offline_qa"}',code)
        self.assertIn('enroll_check(project,"game_toolkit",brief.strip())',code)
        self.assertIn('enroll_check(project,"game_toolkit",manifest)',code)
        self.assertIn('from quality_gate import annotate',code)
        self.assertIn('"0.2.3-shaadi-toolkit-governed"',code)
        self.assertIn('"technical_only"',code)
        self.assertIn('release_authorized":False',code)
        self.assertIn('dev_general_build',code)
        self.assertNotIn('shell=True',code)
        compile(code, "staged_controller.py", "exec")

    def test_controller_patch_is_not_reentrant(self):
        code=d.controller_patch(FAKE_CONTROLLER)
        with self.assertRaises(RuntimeError):
            d.controller_patch(code)

    def test_controller_requires_exact_old_version(self):
        with self.assertRaises(RuntimeError):
            d.controller_patch(FAKE_CONTROLLER.replace(
                "0.2.2-global-intake-governed", "0.2.4-something-else"))

    def test_quality_intake_action_added_without_removal(self):
        text=d.admission_patch(FAKE_ADMISSION)
        self.assertIn('"game_toolkit"',text)
        for old in ("dev_project_build","website_stage","video_preview",
                    "repair_known_issue"):
            self.assertIn(old,text)
        with self.assertRaises(RuntimeError):
            d.admission_patch(text)

    def test_registry_engine_is_exact(self):
        text=d.registry_patch(FAKE_REGISTRY)
        self.assertIn('"game_toolkit": {"fixed_shaadi_recipe_v1"}',text)
        self.assertIn('"reviewed_patch_v1"',text)

    def test_registry_preserves_other_projects(self):
        prior={"schema_version":1,"projects":[
            {"project":"moksha_overhaul","approved":True,
             "actions":{"website_stage":{"moksha_overhaul_v1":"legacy_moksha"}}}]}
        after=json.loads(d.registry_json_patch(json.dumps(prior)))
        self.assertEqual(after["projects"][0],prior["projects"][0])
        ours=after["projects"][1]
        self.assertEqual(ours["project"],d.PROJECT)
        self.assertEqual(set(ours["actions"]["game_toolkit"]),set(d.RECIPES))
        self.assertTrue(all(v==d.ENGINE for v in ours["actions"]["game_toolkit"].values()))
        with self.assertRaises(RuntimeError):
            d.registry_json_patch(json.dumps(after))

    def test_release_script_refuses_missing_live_sha(self):
        with self.assertRaisesRegex(RuntimeError,"exact_controller_sha256_required"):
            d.preflight("",Path("/does-not-exist"))

    def test_release_script_refuses_nonexistent_target(self):
        with self.assertRaisesRegex(RuntimeError,"runtime_target_missing_or_symlink"):
            d.preflight("a"*64,Path("/does-not-exist"))

    def test_release_script_refuses_symlinked_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); target=root/"linked"; target.symlink_to(root)
            with self.assertRaisesRegex(RuntimeError,"symlink"):
                d.preflight("a"*64,target)

    def test_missing_controller_fingerprint_cannot_be_auto_guessed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in d.MANAGED:
                (root/name).write_text(FAKE_CONTROLLER if name=="controller.py" else "x")
            with self.assertRaisesRegex(RuntimeError,"live_controller_hash_drift"):
                d.preflight("a"*64,root)

if __name__ == "__main__":
    unittest.main(verbosity=2)
