"""Read a fixed author return without invoking the simulation."""
from pathlib import Path
from bisect import bisect_left
from fractions import Fraction
import csv
import hashlib
import io
import json
import math
import sys
import tarfile

sha = lambda b: hashlib.sha256(b).hexdigest()
root=Path(sys.argv[1])
outer={}
for line in (root/'SHA256SUMS').read_text().splitlines():
    digest,filename=line.split(None,1)
    file=root/filename.strip()
    assert file.is_file() and file.parent==root and sha(file.read_bytes())==digest
    outer[file.name]=digest
assert sorted(outer)==['screen.txt','suyoung_setting2_contact_result.tar.gz']
assert outer['suyoung_setting2_contact_result.tar.gz']=='fc8e3d67a775eef6c67f171b64e382aba589949d5c8ece82e6a32c6d6546e669'
assert outer['screen.txt']=='56b52d23a531baafc8ab93e8615a56039d6cddbd2769fd866d0b9f3308b6835d'
with tarfile.open(root/'suyoung_setting2_contact_result.tar.gz') as tf:
    collect={}
    for member in tf:
        assert member.isfile() or member.isdir()
        if member.isfile():
            assert member.name.startswith('run/') and '..' not in member.name.split('/') and member.name not in collect
            collect[member.name]=tf.extractfile(member).read()
inner={}
for line in collect['run/SHA256SUMS'].decode().splitlines():
    digest,name=line.split(None,1)
    key='run/'+name.strip().removeprefix('./')
    assert key not in inner and sha(collect[key])==digest
    inner[key]=digest
assert set(collect)==set(inner)|{'run/SHA256SUMS'}
assert collect['run/screen.txt']==(root/'screen.txt').read_bytes()
assert collect['run/RELEASE'].decode().strip()=='182be9d50d5838e1dbfeb246eaf6e9c13dab4bc2'
summ=json.loads(collect['run/summary.json'])
geom={}
curves={}
for k in [8,12,16,24]:
    d=f'run/F{k}/'
    raw=collect[d+'trace.csv']
    rec=json.loads(collect[d+'target_receipt.json'])
    assert rec['trace_sha256']==sha(raw) and rec['result_sha256']==sha(collect[d+'result.json']) and rec['observation_sha256']==sha(collect[d+'observation.json'])
    rows=list(csv.DictReader(io.StringIO(raw.decode())))
    h=[float(r['height']) for r in rows]
    p=[float(r['bottom_pressure_E']) for r in rows]
    phi=[float(r['phi_m']) for r in rows]
    t=[float(r['time_code']) for r in rows]
    assert [int(r['step']) for r in rows]==list(range(len(rows)))
    assert all(math.isclose(h_i*phi_i,h[0]*phi[0],rel_tol=1e-12) for h_i,phi_i in zip(h,phi))
    assert all(time==i*rec['dt'] and H==h[0]-time*rec['wall_speed'] for i,(time,H) in enumerate(zip(t,h)))
    assert max(p[:-1])<.12<=p[-1] and rec['status']=='TARGET_BRACKETED'
    H=h[-2]+(h[-1]-h[-2])*(.12-p[-2])/(p[-1]-p[-2])
    f=h[0]*phi[0]/H
    assert math.isclose(rec['phi_m'],f,rel_tol=1e-14)
    geom[k]={'phi':f,'seconds':rec['elapsed_seconds'],'steps':len(rows)-1}
    curves[k]=([h[0]-x for x in h],[v*10 for v in p])

def linear(curve,u):
    x,y=curve
    j=bisect_left(x,u)
    if x[j]==u: return y[j]
    return y[j-1]+(y[j]-y[j-1])*(u-x[j-1])/(x[j]-x[j-1])

pairs={}
for n in (8,12):
    m=2*n
    end=min(curves[n][0][-1], curves[m][0][-1])
    x=sorted(set(u for k in [n,m] for u in curves[k][0] if u<=end))
    low=[linear(curves[n],u) for u in x]; high=[linear(curves[m],u) for u in x]
    d=[a-b for a,b in zip(low,high)]
    ref=max(abs(v) for v in high)
    i=max(range(len(x)),key=lambda j:abs(d[j]))
    bad=[u for u,v in zip(x,d) if 20*Fraction(abs(v))>Fraction(ref)]
    registered=summ['pair_results'][f'F{n}_F{m}']
    assert math.isclose(abs(d[i])/ref,registered['ratio'],abs_tol=1e-12) and len(bad)==registered['exceeding_knots']
    pairs[f'F{n}_F{m}']=dict(coarse_minus_fine=d[i], max_abs_difference=abs(d[i]),denominator=ref,ratio=abs(d[i])/ref,n=len(x),exceeding=len(bad),first_exceedance_u=bad[0],max_u=x[i])
result=dict(outer=outer,inner_verified=len(inner),arms=geom,delta=abs(geom[12]['phi']-geom[16]['phi']),pairs=pairs,operator=collect['run/arm_status.tsv'].decode())
print(json.dumps(result,indent=2))
