"""Use: python -m visual_yard_v2 run --reference target.png --output ./review [--freeze /path/to/freeze.json]."""
import argparse,json,sys
from .worker import run

def main():
    p=argparse.ArgumentParser()
    p.add_argument('command',choices=['run'])
    p.add_argument('--reference',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--freeze',required=True,help='Verified owner-frozen art lanes record; required for any yard command')
    p.add_argument('--engine',choices=['auto','vtracer','opencv'],default='auto')
    a=p.parse_args()
    result=run(a.reference,a.output,a.freeze,a.engine)
    print(json.dumps(result,indent=2))
    return 0 if result['qa_outcome']=='OWNER_VISUAL_REVIEW_REQUIRED' else 2
if __name__=='__main__':sys.exit(main())
