from pathlib import Path
import sys,concurrent.futures
import run_tests as rt
R=Path(__file__).resolve().parent
jobs={
 'new_network':[str(R/'probes/network_adversarial.py')],
 'original_g1':[str(R/'evidence_g1/probe_adversarial.py')],
 'original_g4':[str(R/'evidence_g4/probe_g4.py')],
 'independent_lw':[str(R/'probes/lw_replay.py')],
 'raw18':[str(R/'probes/raw18.py')],
 'handover':[str(R/'probes/handover_replay.py')],
}
if __name__=='__main__':
 names=sys.argv[1:] or list(jobs)
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as p:
  list(p.map(rt.run,[(n,jobs[n]) for n in names]))
