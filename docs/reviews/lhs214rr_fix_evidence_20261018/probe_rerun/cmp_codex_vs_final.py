"""읽기 전용 — Codex 재확인 탐침 출력 (고치기 전 코드 핀 60ba39e22) ↔ 우리 최종 코드 (f8871224b) 재실행 출력의 판정값 대조.

  python3 -I cmp_codex_vs_final.py <codex evidence/> <final evidence/> <final capture json> <out.json>
"""
import json
import sys
from pathlib import Path

C, F, CAP, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])


def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def first(v, n=160):
    if isinstance(v, list):
        return [str(x)[:n] for x in v[:2]]
    return str(v)[:n] if v is not None else None


res = {}
# R03 — receipt_fences
rc_, rf_ = load(C / 'receipt_fences/results.json'), load(F / 'receipt_fences/results.json')
res['receipt_fences'] = {k: {'codex': {x: rc_[k][x] for x in ('rc', 'bad', 'read_code_fp')}, 'final': {x: rf_[k][x] for x in ('rc', 'bad', 'read_code_fp')}}
                         for k in rc_}
# R01 — numeric_adversarial
nc_, nf_ = load(C / 'numeric_adversarial.json'), load(F / 'numeric_adversarial.json')


def h0(n):
    h = n['restored_primary_H0']
    a = h['after']
    row = a['tau']['value'] or {}
    return {'q_withheld': h['q_withheld'], 'binding_hertzian': first(a['binding']['hertzian']['value']), 'generation': (a['generation']['value'] or {}).get('generation'),
            'tau_status_hertz': row.get('ion_net_status_hertz'), 'f_ion_hertz': row.get('f_ion_hertz'), 'flag_hertz': row.get('full_model_limit_hertz'),
            'content': a['content']['value'], 'record_ok': (a['record']['value'] or [None])[0], 'release_hold_after': h['after_release_hold']['value']}


def phys(n):
    r = n['restored_withheld_full']['result']
    row = r['tau']['value'] or {}
    return {'binding_physics': first(r['binding']['physics']['value']), 'tau_status_physics': row.get('ion_net_status_physics'), 'f_ion_physics': row.get('f_ion_physics')}


res['numeric_H0_restored'] = {'codex': h0(nc_), 'final': h0(nf_)}
res['numeric_physics_restored'] = {'codex': phys(nc_), 'final': phys(nf_)}
res['numeric_boundary'] = {e['label']: {'raw_q': e['raw_q'], 'producer': e['producer_status'],
                                        'codex': first(e['published_check']['value']), 'final': first(f['published_check']['value'])}
                           for e, f in zip(nc_['full_guard_rounding_boundary'], nf_['full_guard_rounding_boundary'])}
res['numeric_sweeps'] = {k: {'codex': (len(nc_['adopted_attempt_sweep']['accepted']), len(nc_['adopted_attempt_sweep']['exceptions']), len(nc_['ledger_sweep']['failures'])),
                             'final': (len(nf_['adopted_attempt_sweep']['accepted']), len(nf_['adopted_attempt_sweep']['exceptions']), len(nf_['ledger_sweep']['failures']))}
                         for k in ('accepted_exceptions_ledgerfailures',)}
# R02 — display_fresh
for tree in ('source', 'base'):
    dc, df = load(C / f'display_fresh_{tree}.json'), load(F / f'display_fresh_{tree}.json')
    fail = lambda d: [(c['case'], c.get('label'), c['got']) for c in d['checks'] if not c['passed']]
    res[f'display_fresh_{tree}'] = {'codex_failed': fail(dc), 'final_failed': fail(df), 'checks': (len(dc['checks']), len(df['checks']))}
# consumer chain (생산자 fixture 를 우리 기계에서 다시 만듦) — 다섯 사례 상태
pc, pf = load(C / 'consumers_probe.json'), load(F / 'consumers_probe.json')


def chain(p):
    out = {}
    for k, v in (p.get('handover', {}).get('cases') or {}).items():
        out[k] = {x: v.get(x) for x in ('status', 'tau_status_hertz', 'tau_status_physics', 'flag_hertz', 'flag_physics', 'primary_hold') if x in v}
    return out


res['consumer_chain_cases'] = {'codex': chain(pc), 'final': chain(pf)}
# consumer_h0_resurrection — Codex 원 출력 ↔ 우리 파생 래퍼 (탐침 무변경 · 예외까지의 report)
hc, cap = load(C / 'consumer_h0_resurrection.json'), load(CAP)
hf = cap['report']


def resur(r):
    a = r.get('after', {})
    row = a.get('row')
    row = row.get('value') if isinstance(row, dict) and 'value' in row else row
    row = row or {}
    return {'numeric_only_stop_ok': ((r.get('numeric_only_stop') or {}).get('value') or [None])[0],
            'content_ok': ((a.get('content') or {}).get('value') or [None])[0], 'record_ok': ((a.get('record') or {}).get('value') or [None])[0],
            'stop_ok': ((a.get('stop') or {}).get('value') or [None])[0], 'stop_why': first(((a.get('stop') or {}).get('value') or [None, None])[1], 200),
            'row_hertz': row.get('ion_net_status_hertz'), 'row_generation': row.get('ion_net_generation'), 'f_ion_hertz': row.get('f_ion_hertz'),
            'certificate_numeric_unchanged': a.get('certificate_numeric_unchanged'),
            'release_baseline': first((r.get('release_baseline') or {}).get('value') if isinstance(r.get('release_baseline'), dict) else r.get('release_baseline'), 120),
            'release_baseline_check': (r.get('release_baseline_check') or {}).get('value') if isinstance(r.get('release_baseline_check'), dict) else r.get('release_baseline_check')}


res['consumer_h0_resurrection'] = {'codex': resur(hc), 'final': resur(hf), 'final_exception_tail': (cap.get('exception') or '')[-600:],
                                   'probe_sha256': cap.get('probe_sha256')}
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
print(json.dumps({k: (v if k in ('numeric_boundary', 'numeric_sweeps') else '…') for k, v in res.items()}, ensure_ascii=False)[:2500])
