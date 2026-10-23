#!/usr/bin/env python3
"""Offline QA for local Andaz multi-phase planning; reports flaws, no execution."""
import argparse
import json
from pathlib import Path
import re

STAGES=("01-audit-research","02-ux-content","03-engineering-booking","04-qa-security","05-red-team-signoff")
MANDATORY={
 "brand":r"andaz",
 "mobile":r"mobile|responsive|viewport",
 "rooms":r"dorm|private.rooms|room.inventory",
 "pms":r"\bpms\b",
 "booking":r"booking|reservation",
 "whatsapp":r"whatsapp",
 "real_photos":r"authentic.photo|real.photo|photo.rights|photo.source|photo.ownership|verified.photo",
 "moksha_partner":r"moksha",
 "seo":r"\bseo\b|canonical|schema.org",
 "accessibility":r"accessib|keyboard|screen.reader|a11y",
 "rollback":r"rollback|restore|backups?",
 "qa":r"\bqa\b|independent.test|regression",
 "security":r"secur|threat.model|privacy",
 "approval":r"owner.approval|human.approval|owner.review",
 "unknowns":r"unknowns?|unverified|verify|not.confirmed",
}
BLOCKERS={
 "unjustified_booking_consistency_below_100pct":r"(?:at.least|minimum)\s+(?:[0-9]{1,2}(?:\.[0-9]+)?)\s*%\s+of.{0,110}(?:availability|pricing|inventory).{0,80}(?:consistent|match)",
 "fake_completed_live_inspection":r"(?:we.have|i.have|already)\s+(?:audited|inspected|accessed|verified)\s+the\s+(?:live\s+)?(?:andaz|wordpress|pms|website)",
 "unapproved_release":r"(?:publish|deploy).{0,45}(?:automatically|without.owner.approval)",
}
def analyze(directory):
 if not isinstance(directory,Path) or not directory.is_dir():raise ValueError("staging_directory_missing")
 parts={p:(directory/(p+".md")).read_text(encoding="utf8") if (directory/(p+".md")).is_file() else "" for p in STAGES}
 whole="\n".join(parts.values())
 match={k:bool(re.search(reg,whole,re.I|re.S)) for k,reg in MANDATORY.items()}
 blockers={k:bool(re.search(reg,whole,re.I|re.S)) for k,reg in BLOCKERS.items()}
 issues=[]
 for phase,txt in parts.items():
  if len(txt)<350:issues.append("missing_or_short_phase:"+phase)
  if txt and ("deliverable" not in txt.lower() or "acceptance" not in txt.lower()):
   issues.append("missing_delivery_or_acceptance:"+phase)
 for k,v in match.items():
  if not v:issues.append("missing_coverage:"+k)
 for k,v in blockers.items():
  if v:issues.append("unsafe_or_unjustified:"+k)
 progress=directory/"progress.json"
 if not progress.is_file():issues.append("missing_terminal_progress")
 else:
  st=json.loads(progress.read_text())
  if st.get("state")!="completed":issues.append("model_run_not_complete")
  if len(st.get("phases",[]))!=5:issues.append("incomplete_phase_receipts")
  if any(p.get("status")!="completed" for p in st.get("phases",[])):
   issues.append("truncated_or_failed_model_phase")
 return {"decision":"REVIEW_READY" if not issues else "NEEDS_REVISION",
     "issues":issues,"semantic_keyword_coverage":match,
     "critical_patterns":blockers,"phases_with_text":sum(bool(x) for x in parts.values()),
     "note":"This automated rule-based check does NOT certify correctness or source evidence. Human reviewer required.",
     "production_changed":False}
def main():
 parser=argparse.ArgumentParser()
 parser.add_argument("--staging",required=True)
 opts=parser.parse_args()
 p=Path(opts.staging).resolve()
 result=analyze(p)
 (p/"independent-quality-review.json").write_text(json.dumps(result,indent=2))
 print(json.dumps(result,indent=2))
 return 0 if result["decision"]=="REVIEW_READY" else 2
if __name__=="__main__":raise SystemExit(main())
