#!/usr/bin/env python3
"""Q1 확정 도구 검증 (real_14) 의 보조 — 두 하위 명령 (읽기 = 리포 · 받은 manifest / 쓰기 = 검증 폴더 안의 사본만).

  prov    <V>                 : case · old · oldd 에 provenance 픽스처 (파이프라인과 같은 모양 · argv + input_digests = sha256 앞 16)
  forcedirect <py 파일>       : 옛 모듈 사본의 CG 문턱 줄 (`if n_nodes > 30000:`) 만 꺼서 직접해로 (검증 사본 · 리포 무수정)
  fixtures <V> <B7 manifest>  : 음성 대조 사본 (B7 기록 +3 칸 · v1.2 기록 +3 칸 · 입력 지문 0) + 기록 사슬 픽스처 (reread · manifest)
  collect <V> <out.json>      : 여덟 경우 결과를 한 JSON 으로 (기대 rc 와 대조)
"""
import hashlib
import json
import os
import sys

KEYS = ('sigma_full', 'sigma_bulk_net', 'sigma_constr_net')
WANT = {'cg': 4, 'inc': 0, 'negA': 3, 'negA0': 3, 'negB': 3, 'incfull': 0, 'negRun': 3, 'negCode': 3}
FIXTURE = {
    'cg': 'v1.2 기록 = 11fcf91e8 모듈 그대로 (real_14 관통 32,234 → CG 경로) — B 판정 안 함',
    'inc': 'v1.2 기록 = 같은 모듈의 CG 문턱만 끈 사본 (직접해) + --assume-v12-direct',
    'negA': 'B7 기록 sigma_full +3 칸 (사본)',
    'negA0': 'B7 provenance 의 contacts.csv 지문을 0 으로 (사본)',
    'negB': 'v1.2 기록 sigma_full +3 칸 (사본)',
    'incfull': 'inc + --b7-manifest (받은 B7 manifest 의 code_hashes) + --b7-reread (run id · 표 값 픽스처)',
    'negRun': 'incfull 에서 reread run id 만 다르게',
    'negCode': 'incfull 에서 manifest 의 network_conductivity.py 지문만 0 으로',
}


def jl(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def jw(p, d):
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)


def d16(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def prov(V):
    for sub in ('case', 'old', 'oldd'):
        jw(os.path.join(V, sub, 'network_provenance.json'),
           {'argv': {'type_map': '1:AM_P,2:AM_S,3:SE', 'scale': 1000, 'contact_mode': 'both'},
            'input_digests': {n: d16(os.path.join(V, sub, n)) for n in ('atoms.csv', 'contacts.csv')},
            'note': '검증 픽스처 — 파이프라인 provenance 와 같은 모양'})


def forcedirect(p):
    with open(p, encoding='utf-8') as f:
        s = f.read()
    old = '        if n_nodes > 30000:\n'
    if s.count(old) != 1:
        sys.exit(f'CG 문턱 줄이 {s.count(old)} 번 — 옛 모듈 판이 다르다')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s.replace(old, '        if n_nodes > 10**12:  # 검증 사본: 직접해만\n'))


def fixtures(V, man):
    def edit(rel, fn):
        p = os.path.join(V, rel)
        d = jl(p)
        fn(d)
        jw(p, d)
    edit('case_negA/network_conductivity_dual.json', lambda d: d['hertzian'].__setitem__('sigma_full', round(d['hertzian']['sigma_full'] + 3e-8, 8)))
    edit('oldd_negB/network_conductivity_dual.json', lambda d: d['hertzian'].__setitem__('sigma_full', round(d['hertzian']['sigma_full'] + 3e-8, 8)))
    edit('case_negA0/network_provenance.json', lambda d: d['input_digests'].__setitem__('contacts.csv', '0' * 16))
    edit('case_run/network_provenance.json', lambda d: d.__setitem__('network_run_id', 'FIXTURE-RUN-1'))
    dual = jl(os.path.join(V, 'case_run', 'network_conductivity_dual.json'))['hertzian']
    tb = {br: {'value': dual[k]} for br, k in zip(('full', 'bulk_only', 'constriction_only'), KEYS)}
    os.makedirs(os.path.join(V, 'fx'), exist_ok=True)
    jw(os.path.join(V, 'fx', 'reread_ok.json'), {'cases': [{'case': 'real14', 'run_id': 'FIXTURE-RUN-1', 'table': {'hertz': tb}}]})
    jw(os.path.join(V, 'fx', 'reread_badrun.json'), {'cases': [{'case': 'real14', 'run_id': 'FIXTURE-RUN-2', 'table': {'hertz': tb}}]})
    ch = jl(man)['code_hashes']
    jw(os.path.join(V, 'fx', 'manifest_ok.json'), {'code_hashes': ch})
    jw(os.path.join(V, 'fx', 'manifest_badcode.json'), {'code_hashes': dict(ch, **{'scripts/network_conductivity.py': '0' * 64})})


def collect(V, out):
    res = {'schema': 's5_q1_settle_validation/v1',
           'bed': 'real_14 (docs/data/real14_reference_20260928 — 커밋된 덤프 · type map 1:AM_P,2:AM_S,3:SE · scale 1000)', 'cases': {}}
    for nm, rc_want in WANT.items():
        d = jl(os.path.join(V, f'out_{nm}', 'settle_real14.json'))
        rc = {'INCLUDE': 0, 'HOLD': 3, 'INCONCLUSIVE': 4}[d['verdict']]
        res['cases'][nm] = dict(fixture=FIXTURE[nm], verdict=d['verdict'], rc=rc, rc_expected=rc_want, ok=(rc == rc_want), checks=d['checks'],
                                full={k: d['rows']['full'][k] for k in ('sigma_b7_inprocess', 'record_b7', 'sigma_adaptive', 'record_v12',
                                                                        'd_electrode', 'd_records', 'dirichlet_netsolve_vs_b7_rel')})
        if nm == 'incfull':
            res['code_seal_detail'] = d['code_seal_detail']
            res['rows_incfull'] = {br: {k: x[k] for k in ('d_electrode', 'd_records', 'g_boundary', 'sum_g', 'g_max', 'n_perc', 'n_bot', 'n_top',
                                                          'b7_method')} for br, x in d['rows'].items()}
    res['b7_cli_on_fixture'] = {k: jl(os.path.join(V, 'case', 'network_conductivity_dual.json'))['hertzian'][k] for k in KEYS}
    res['v12_module_on_fixture'] = {s: {k: jl(os.path.join(V, s, 'network_conductivity_dual.json'))['hertzian'][k] for k in KEYS}
                                    for s in ('old', 'oldd')}
    res['design_record_reference'] = ('docs/reviews/gen2_network_design_20261006.md §3 — Hertz H0 옛 전극 → Dirichlet 0.0210206 → 0.02102106 (×1.0000219) · '
                                      'docs/data/gen2_design_20261006/c1/net_beds_real14.json H0_full dirichlet_over_adaptive − 1 = 2.1488e-05')
    res['all_ok'] = all(c['ok'] for c in res['cases'].values())
    jw(out, res)
    print('all_ok', res['all_ok'], {k: (c['verdict'], c['rc']) for k, c in res['cases'].items()})
    return 0 if res['all_ok'] else 1


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'prov':
        prov(sys.argv[2])
    elif cmd == 'forcedirect':
        forcedirect(sys.argv[2])
    elif cmd == 'fixtures':
        fixtures(sys.argv[2], sys.argv[3])
    elif cmd == 'collect':
        sys.exit(collect(sys.argv[2], sys.argv[3]))
    else:
        sys.exit(f'모르는 명령 {cmd!r}')
