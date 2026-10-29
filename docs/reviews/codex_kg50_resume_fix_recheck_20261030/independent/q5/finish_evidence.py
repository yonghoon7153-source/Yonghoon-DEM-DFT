"""Add direct D2 trial and Q5 arithmetic checks to existing read-only review."""
from pathlib import Path
from decimal import Decimal
import hashlib
import json
import subprocess
import sys

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent/'repo'
data=json.loads((OUT/'results.json').read_text(encoding='utf-8'))
d2=ROOT/'docs/data/kg50_resume_tests_20261027/d2_main_1028_0942'
target=OUT/'d2_trial_cut_by_current_python.liggghts'
r=subprocess.run([sys.executable,'-X','utf8','-B',str(OUT/'pinned_embedded_cli.py'),'--cut-trial',
    str(d2/'input_kg50_d2_b50_r4.liggghts'),'2000',str(target)],capture_output=True,text=True,encoding='utf-8')
data['d2']['current_producer_cut']=dict(rc=r.returncode,stdout=r.stdout,stderr=r.stderr,
    byte_equal_to_received_trial=target.exists() and target.read_bytes()==(d2/'input_kg50_d2_b50_r4t.liggghts').read_bytes(),
    sha256=hashlib.sha256(target.read_bytes()).hexdigest() if target.exists() else None)
arithmetic={}
for w,s0,na,nb,dt,atom,contact,thermoa,thermob in [
    ('W1',200001,200001,400002,Decimal('0.000001'),66667,200001,1000,2000),
    ('W2',800000,300000,600000,Decimal('0.000001'),10000,100000,1000,2000)]:
    a=[s for s in range(s0,s0+na+1) if s%atom==0]
    b=[s for s in range(s0,s0+nb+1) if s%atom==0]
    ca=[s for s in range(s0,s0+na+1) if s%contact==0]
    cb=[s for s in range(s0,s0+nb+1) if s%contact==0]
    timesa=[str((s-s0)*dt) for s in a]
    timesb=[str((s-s0)*dt/2) for s in b]
    arithmetic[w]=dict(start=s0,end_a=s0+na,end_b=s0+nb,window_a=str(na*dt),window_b=str(nb*dt/2),
        atom_count_a=len(a),atom_count_b=len(b),contact_count_a=len(ca),contact_count_b=len(cb),
        a_atom_times_subset_of_b=all(Decimal(x) in list(map(Decimal,timesb)) for x in timesa))
    if w=='W2':
        oa=[(s-s0)*dt for s in range(s0+na-50000,s0+na+1,thermoa)]
        ob=[(s-s0)*dt/2 for s in range(s0+nb-100000,s0+nb+1,thermob)]
        arithmetic[w]['O3']=dict(count_a=len(oa),count_b=len(ob),times_equal=oa==ob,first=str(oa[0]),last=str(oa[-1]))
data['independent_arithmetic']=arithmetic
mutated=OUT/'syn/extra_runtime_command/q5_kg50_d07_b50_A/log.liggghts'
base=mutated.read_text(encoding='utf-8').replace('velocity all set 1.0 0.0 0.0\nrun 200000\n','run 200000\n')
(OUT/'provenance_baseline_A.log').write_text(base,encoding='utf-8')
data['extra_echo_provenance']['input_delta']='One added line before run 200000 in A/log.liggghts: velocity all set 1.0 0.0 0.0. Deck/manifest/dump files unchanged.'
data['extra_echo_provenance']['baseline_A_log_sha256']=hashlib.sha256(base.encode()).hexdigest()
data['extra_echo_provenance']['mutated_A_log_sha256']=hashlib.sha256(mutated.read_bytes()).hexdigest()
(OUT/'results.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'d2_cut':data['d2']['current_producer_cut'],'arithmetic':arithmetic},ensure_ascii=False,indent=2))
