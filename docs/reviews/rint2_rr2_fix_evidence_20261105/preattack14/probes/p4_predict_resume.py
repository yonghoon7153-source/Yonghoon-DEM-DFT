"""Honest predict-stage resume (RS05 flow) whose resume attempt stops AFTER the rerun (eligible) — false fail-closed check on the predict path
   (P prefix · SV graph-source runs during copies · DBE arms)."""
from pathlib import Path
from lib import RR, T, row

d, _rc, _so = T.led_new('PA14pr')
_r, n1, _s = T.led_add(d, 'ladder:P0')
l0 = T.lad_att('PA14pr_P0', T.world('PA14pr_P0'), d, n1)
_r, n2, _s = T.led_add(d, 'ladder:P1')
l1 = T.lad_att('PA14pr_P1', T.world('PA14pr_P1'), d, n2, law='P1')
_r, n3, _s = T.led_add(d, 'predict')
base = Path(T.TD) / 'runs' / 'PA14pr_pred'
p = T.pred_att('PA14pr_pred', T.world('PA14pr_pa', dict(T.PW, faults=[{'do': 'oom_after_mark', 'match': {'kit_has': 'DBE', 'min_n': 5}}])), d, n3,
               [l0['out'], l1['out']], base=base)
res = {}
for mn in (3, 6, 9):
    dd = T.led_clone(d, f'PA14pr_{mn}') if hasattr(T, 'led_clone') else None
    if dd is None:
        break
    import shutil
    b2 = Path(T.TD) / 'runs' / f'PA14pr_pred_{mn}'
    shutil.copytree(base, b2, symlinks=True)
    # attempt folders must sit in the same base as the ledger start record of attempt n3 — copy keeps attempt_<n3>; the start record base differs,
    # which matters only for recover (not used here)
    r4, n4, s4 = T.led_add(dd, 'predict', resume=n3)
    q = T.pred_att(f'PA14pr_q{mn}', T.world(f'PA14pr_pb{mn}', dict(T.PW, faults=[{'do': 'oom_after_mark', 'match': {'kit_has': 'DBE', 'min_n': mn}}])), dd, n4,
                   [l0['out'], l1['out']], base=b2)
    qs = q['sum'] or {}
    lr = T.led_result(dd, n4) or {}
    res[mn] = (q['rc'], (qs.get('stop') or {}).get('code'), (qs.get('stop') or {}).get('run'), qs.get('resume'), lr.get('cause'), lr.get('resume_ok'),
               row(q['out'], qs), RR.result_line_problem(n4, q['out'], lr) if lr else 'no ledger line')
ps = p['sum'] or {}
print('orig predict attempt:', p['rc'], (ps.get('stop') or {}).get('code'), (ps.get('stop') or {}).get('run'), (T.led_result(d, n3) or {}).get('resume_ok'))
for mn, v in res.items():
    print(f'resume world min_n {mn}:')
    for x in v:
        print('   ', str(x)[:400])
