"""3-attempt honest chain (real chain · fake runner · real git ledger):
   a1 = OOM at ceiling (L02) · a2 = resume of 1 (src a1) — L02 rerun ok, L03 runner done but group unconfirmed (payload left) → recover ·
   a3 = resume of 1 (src a2 = chain end) — copies L01 L02 (copied_from 2), L03 rerun vs a2/L03 leftovers.
   variant 'elig': a3 world same σ → L03 compare same → L04 OOM → resource (honest, lo=1 · from=2 · n=3)
   variant 'mm'  : a3 world σ×(1+1e-12) at L03 → RESUME_MISMATCH (honest) → forge from=1 (+copied_from, compared [], assumed)."""
import copy, json
from pathlib import Path
from lib import RR, T, row


def chain(tag, w3):
    d, _rc, _so = T.led_new(tag)
    _r, n1, _s = T.led_add(d, 'ladder:P0')
    base = Path(T.TD) / 'runs' / f'{tag}_lad'
    a = T.lad_att(tag, T.world(f'{tag}_a', dict(T.PW, faults=[{'do': 'oom_after_mark', 'match': {'rj': '0'}}])), d, n1, base=base)
    _r, n2, _s = T.led_add(d, 'ladder:P0', resume=n1)
    old = RR.group_settle
    calls = []

    def gs(token, limit=None):
        calls.append(1)
        if len(calls) == 2:
            return False, [999993], 0
        return old(token, limit)
    RR.group_settle = gs
    try:
        b = T.lad_att(tag, T.world(f'{tag}_b'), d, n2, base=base)
    finally:
        RR.group_settle = old
    rc_rec, so_rec = T.call(['--stage', 'recover', '--out', str(b['out']), '--ledger', str(d)])
    add3 = T.led_add(d, 'ladder:P0', resume=n1)
    c = T.lad_att(tag, T.world(f'{tag}_c', w3), d, add3[1], base=base) if add3[1] else None
    return {'d': d, 'a': a, 'b': b, 'c': c, 'rec': rc_rec, 'add3': add3[:2], 'add3_so': add3[2][-300:]}


def show(lab, r):
    for k in ('a', 'b', 'c'):
        x = r[k]
        if x is None:
            print(f'  {lab}.{k}: NONE (add3 {r["add3"]} {r["add3_so"]})')
            continue
        s = x['sum'] or {}
        print(f'  {lab}.{k}: rc {x["rc"]} stop {(s.get("stop") or {}).get("code")} run {(s.get("stop") or {}).get("run")} resume {s.get("resume")} '
              f'runs {[(q.get("name"), q.get("copied_from")) for q in s.get("runs") or []]}')
        n = int(Path(x['out']).name.split('_')[1])
        print(f'     ledger result {n}: {T.led_result(r["d"], n)}')
        print(f'     row (result_fields · stop_record_problem): {row(x["out"], s)}')
        print(f'     result_line_problem: {RR.result_line_problem(n, x["out"], T.led_result(r["d"], n) or {})}')


L3 = '10000.0'
el = chain('PA14c3el', dict(T.PW, faults=[{'do': 'oom_after_mark', 'match': {'rj': '1000000.0'}}]))
print('== elig (honest 3-chain · a3 stop after rerun) ==')
show('el', el)
mm = chain('PA14c3mm', dict(T.PW, faults=[{'do': 'sigma_scale', 'f': 1.0 + 1e-12, 'match': {'rj': L3}}]))
print('== mm (honest 3-chain · a3 RESUME_MISMATCH) ==')
show('mm', mm)
c = mm['c']
s0 = c['sum']
if s0 and (s0.get('stop') or {}).get('code') == 'RESUME_MISMATCH':
    nxt = 'L04_point'
    def forge(s, frm, cmp_, det, cf):
        s = copy.deepcopy(s)
        s['stop'].update(code='TIME_LIMIT', run=nxt, reason=None)
        s['resume'].update(**{'from': frm, 'compared': cmp_, 'determinism': det})
        if cf is not None:
            for r in s['runs']:
                if 'copied_from' in r:
                    r['copied_from'] = cf
        return s
    print('\n== forgeries of honest a3 RESUME_MISMATCH ==')
    rows = [('f_from2_assumed (3+2 fields)', forge(s0, 2, [], 'assumed', None)),
            ('f_from2_sameTrue', forge(s0, 2, [dict(x, same=True) for x in s0['resume']['compared']], 'compared', None)),
            ('f_from1_assumed_no_cf (from rebinding only)', forge(s0, 1, [], 'assumed', None)),
            ('f_from1_assumed_cf1 (from rebinding + copied_from)', forge(s0, 1, [], 'assumed', 1))]
    for nm, s in rows:
        print(f'  {nm:52s} {row(c["out"], s)}')
    # ledger-aware: what would presolve of a4 see if a3's result line had been written (by recover) from the forged summary?
    fs = rows[-1][1]
    tmp = Path(T.TD) / 'pa14_forge' / 'base'
    import shutil
    shutil.copytree(Path(c['out']).parent, tmp, symlinks=True)
    (tmp / 'attempt_3' / 'ladder_summary.json').write_bytes(RR.canon_bytes(fs))
    res3 = RR.attempt_result_line(3, tmp / 'attempt_3', fs, 'recover')
    print('  forged a3 result line (recover would write):', {k: res3[k] for k in ('status', 'cause', 'resume_ok', 'stop')})
