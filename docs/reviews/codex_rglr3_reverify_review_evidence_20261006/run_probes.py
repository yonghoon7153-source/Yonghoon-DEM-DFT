"""Reproduce reviewer probes in an isolated source copy. No production/campaign runs."""
import json,sys
from pathlib import Path
from run_tests import run
R=Path(__file__).resolve().parent
PROBES={'network':'network_adversarial.py','lw':'lw_replay.py','vm':'vm_boundary.py',
        'precision':'precision_boundary.py','raw18':'raw18.py','handover':'handover_replay.py','handover_diff':'handover_before_after.py'}
if __name__=='__main__':
 names=sys.argv[1:] or list(PROBES)
 results=[run(('ind_'+n,['../probes/'+PROBES[n]])) for n in names]
 (R/'evidence/probe_summary.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
 raise SystemExit(any(r['rc'] for r in results))
