"""V1.3 controller execution gate. Local source-bound action preflight only.
Does not grant arbitrary CLI/SSH, external connectors or production release."""
import hashlib,json,stat
from pathlib import Path
from yard_auto_adapter_v1 import inherit, AdapterDenied

ROOT=Path(__file__).resolve().parent
LEDGER=ROOT/'yard_exec_bindings_v13.json'
VERSION='yard-execution-enforcement-v1.3.0-20261026'
ACTIVE={
 'research_search':['../matrix-searxng/local_search.py'],
 'dev_docs_fetch':['mcp_tool_router.py'],
 'dev_proposal':['../.local/share/matrix-dev-brain/brain.py'],
 'dev_scoped_build':['dev_autonomy_task_v4.py'],
 'dev_general_build':['general-dev-release-v4/agent_loop.py','general-dev-release-v5/agent_loop.py','general-dev-release-v6/agent_loop.py'],
 'dev_project_build':['reviewed_patch_runner.py'],
 'game_toolkit':['game_toolkit_runner.py'],
 'website_stage':['site_staging.py','project_static_stage.py'],
 'pine_chat_stage':['pine_chat_stage.py'],
 'sandbox_qa':['sandbox.py'],
 'repair_known_issue':['repair.py'],
}
CORE=['quality_admission.py','quality_gate.py','project_registry.py','toolyard_qa_standard_v1.py','yard_auto_adapter_v1.py']
MANAGER='manager_governance_v3.py'
class ExecutionDenied(AdapterDenied):pass

def digest(path):
    p=Path(path)
    if p.is_symlink() or not p.is_file() or p.stat().st_size>2_000_000:
        raise ExecutionDenied('invalid_source')
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read_ledger(path=LEDGER):
    p=Path(path)
    if p.is_symlink() or not p.is_file() or p.stat().st_size>30000 or p.stat().st_mode & (stat.S_IWGRP|stat.S_IWOTH):
        raise ExecutionDenied('invalid_execution_ledger')
    d=json.loads(p.read_text())
    if d.get('version')!=VERSION or d.get('production_live') is not False or d.get('external_paths_certified') is not False:
        raise ExecutionDenied('invalid_execution_policy')
    if set(d.get('bindings',{}))!=set(CORE+[MANAGER]+[x for xs in ACTIVE.values() for x in xs]):
        raise ExecutionDenied('incomplete_execution_binding')
    if not all(isinstance(x,str) and len(x)==64 for x in d['bindings'].values()):
        raise ExecutionDenied('invalid_source_hash')
    return d

def verify_sources(paths,ledger=LEDGER):
    bindings=read_ledger(ledger)['bindings']
    for name in paths:
        if name not in bindings:raise ExecutionDenied('unreviewed_execution_source')
        p=ROOT/name
        if digest(p)!=bindings[name]:
            raise ExecutionDenied('execution_source_hash_drift:'+name)
    return True

def preflight(project,action,manifest,ledger=LEDGER):
    # Unlike auto-adapter version/syntax probes, this is bounded to registered
    # controller routes. Owner intake and existing V6 controls remain separate.
    try:inherited=inherit(project,action,manifest)
    except AdapterDenied as err:raise ExecutionDenied(str(err)) from err
    if action not in ACTIVE:raise ExecutionDenied('non_executable_action')
    verify_sources(CORE+ACTIVE[action],ledger)
    return {'rule':VERSION,'project':project,'action':action,
            'qa_requirements':inherited['mandatory_checks'],
            'source_bound':True,'production_authorized':False,
            'unmanaged_ssh_or_connectors_certified':False}

def manager_preflight(ledger=LEDGER):
    return verify_sources(CORE+[MANAGER],ledger)
