"""우리 트리 재현 대조 (10-18) — Codex LHS214 수정 재확인 (코드 핀 60ba39e22) 탐침 다섯의 판정값.

입력: 우리 실행 출력 폴더 (OURS = 재현 작업 사본의 evidence/) ↔ Codex 출력 (CODEX = 이 리포 반입 폴더의 evidence/).
판정값 = rc · 실패 칸 · 상태 · 표지 · HOLD 문구 · 다시 읽기 ok · build 파일 수 · 경고 · check 결과.
수치 끝자리 (q · τ² · φ) 와 실행 ID · 경로는 판정값이 아니라 따로 적는다 (Linux ↔ Windows 부동소수).
읽기만 한다 — 두 폴더의 어느 파일도 고치지 않는다.
"""
import hashlib
import json
import os
import sys

OURS, CODEX, OUT = sys.argv[1:4]


def load(base, rel):
    with open(os.path.join(base, rel), encoding='utf-8') as fh:
        return json.load(fh)


def j(x):
    return json.dumps(x, sort_keys=True, ensure_ascii=False)


def sha(base, rel):
    return hashlib.sha256(open(os.path.join(base, rel), 'rb').read()).hexdigest()


res = {'ours_dir_files': {}, 'probes': {}}
for rel in ('receipt_fences/results.json', 'numeric_adversarial.json', 'display_fresh_source.json',
            'display_fresh_base.json', 'consumers_probe.json', 'consumer_h0_resurrection.json'):
    res['ours_dir_files'][rel] = sha(OURS, rel)

# 1 영수증 울타리 (L214R-R03)
a, b = load(OURS, 'receipt_fences/results.json'), load(CODEX, 'receipt_fences/results.json')
res['probes']['receipt_fences'] = {k: dict(ours=[a[k]['rc'], a[k]['bad']], codex=[b[k]['rc'], b[k]['bad']],
                                         same=(a[k]['rc'], a[k]['bad'], a[k]['section'], a[k]['section_problem'], a[k]['read_code_fp']) ==
                                              (b[k]['rc'], b[k]['bad'], b[k]['section'], b[k]['section_problem'], b[k]['read_code_fp']))
                                   for k in sorted(set(a) | set(b))}

# 2 수치 (L214R-R01 함수 수준 · 경계 · 같은 부류 대조)
a, b = load(OURS, 'numeric_adversarial.json'), load(CODEX, 'numeric_adversarial.json')
def h0(d):
    h = d['restored_primary_H0']
    bt, at = h['before']['tau']['value'], h['after']['tau']['value']
    return dict(before=[bt['ion_net_status_hertz'], bt['ion_net_status_reason_hertz'], bt['full_model_limit_hertz']],
                after=[at['ion_net_status_hertz'], at['f_ion_hertz'], at['full_model_limit_hertz']],
                content=h['after']['content']['value'], record=h['after']['record']['value'],
                ion={m: v['value'] for m, v in h['after']['ion'].items()},
                binding={m: v['value'] for m, v in h['after']['binding'].items()},
                hold_before=h['before_release_hold'], hold_after=h['after_release_hold'])
ha, hb = h0(a), h0(b)
edges = lambda d: [(e['label'], e['raw_q'], e['published_q'], e['producer_status'], e['published_check']) for e in d['full_guard_rounding_boundary']]
phys = lambda d: [d['restored_withheld_full']['q_withheld'], d['restored_withheld_full']['result']['tau']['value'].get('ion_net_status_physics'),
                  d['restored_withheld_full']['result']['tau']['value'].get('f_ion_physics')]
res['probes']['numeric_adversarial'] = dict(
    restored_primary_H0=dict(same=j(ha) == j(hb), ours=ha),
    q_withheld=dict(ours=a['restored_primary_H0']['q_withheld'], codex=b['restored_primary_H0']['q_withheld'],
                    note='판정값 아님 — Linux ↔ Windows 부동소수 끝자리 · 8 자리 반올림 (게시 칸) 같음'),
    tau2_after=dict(ours=a['restored_primary_H0']['after']['tau']['value']['tau2_ion_hertz'], codex=b['restored_primary_H0']['after']['tau']['value']['tau2_ion_hertz']),
    restored_physics=dict(same=phys(a) == phys(b), ours=phys(a)),
    full_guard_rounding_boundary=dict(same=edges(a) == edges(b), ours=edges(a)),
    adopted_attempt_sweep=dict(ours=[a['adopted_attempt_sweep']['count'], len(a['adopted_attempt_sweep']['accepted']), len(a['adopted_attempt_sweep']['exceptions'])],
                               codex=[b['adopted_attempt_sweep']['count'], len(b['adopted_attempt_sweep']['accepted']), len(b['adopted_attempt_sweep']['exceptions'])]),
    ledger_sweep=dict(ours=[a['ledger_sweep']['count'], len(a['ledger_sweep']['failures'])], codex=[b['ledger_sweep']['count'], len(b['ledger_sweep']['failures'])]),
    known_K=dict(same=j({k: v for k, v in a['known_K'].items() if k != 'K3_legacy_zero_meta'}) == j({k: v for k, v in b['known_K'].items() if k != 'K3_legacy_zero_meta'})))

# 3 화면 (L214R-R02) — 수정 트리 · 기준 트리
for tree in ('source', 'base'):
    a, b = load(OURS, f'display_fresh_{tree}.json'), load(CODEX, f'display_fresh_{tree}.json')
    norm = lambda cs: [(c.get('case'), c.get('check'), c.get('label'), j(c.get('got')), c.get('passed')) for c in cs]
    res['probes'][f'display_fresh_{tree}'] = dict(
        checks=dict(n=len(a['checks']), failed_ours=sum(1 for c in a['checks'] if not c.get('passed')),
                    failed_codex=sum(1 for c in b['checks'] if not c.get('passed')), same=norm(a['checks']) == norm(b['checks'])),
        cases=dict(n=len(a['cases']), differing=sorted(k for k in set(a['cases']) | set(b['cases']) if j(a['cases'].get(k)) != j(b['cases'].get(k)))),
        failed_ours=[(c.get('case'), c.get('check'), c.get('label'), c.get('got')) for c in a['checks'] if not c.get('passed')])

# 4 소비자 사슬 (생산자 fixture 를 우리 기계에서 다시 만듦)
a, b = load(OURS, 'consumers_probe.json'), load(CODEX, 'consumers_probe.json')
cp = {}
for name in sorted(a['cases']):
    x, y = a['cases'][name], b['cases'][name]
    rc = lambda c: [(r.get('name', '').split()[0], r.get('ok')) for r in c.get('reread_checks', [])]
    cp[name] = dict(status=[x['status'], y['status']], tau_same=x.get('tau') == y.get('tau'), hold_same=x.get('release_primary_hold') == y.get('release_primary_hold'),
                    full_model_limit_same=x.get('full_model_limit') == y.get('full_model_limit'), reread_ok_same=rc(x) == rc(y),
                    reread_all_ok=all(ok for _, ok in rc(x)), q_ours=x.get('q'), q_codex=y.get('q'))
res['probes']['consumers_probe'] = cp

# 5 H0 복원 전체 경로 (L214R-R01)
a, b = load(OURS, 'consumer_h0_resurrection.json'), load(CODEX, 'consumer_h0_resurrection.json')
af = lambda d: {k: d['after'][k]['value'] for k in ('content', 'record', 'stop')}
rbv = lambda d: {k: v for k, v in d['release_baseline']['value'].items() if k != 'out_dir'}
row_diff = sorted(c for c in set(a['after']['row']) | set(b['after']['row']) if a['after']['row'].get(c) != b['after']['row'].get(c))
res['probes']['consumer_h0_resurrection'] = dict(
    numeric_only_stop_same=j(a['numeric_only_stop']) == j(b['numeric_only_stop']), numeric_only_stop=a['numeric_only_stop']['value'],
    after_same=j(af(a)) == j(af(b)), after=af(a),
    certificate_numeric_unchanged=[a['after']['certificate_numeric_unchanged'], b['after']['certificate_numeric_unchanged']],
    mutation_leaves=dict(ours={n: len(v) for n, v in a['mutations'].items()}, codex={n: len(v) for n, v in b['mutations'].items()}),
    build_same_except_out_dir=j(rbv(a)) == j(rbv(b)), build=rbv(a),
    check=[a['release_baseline_check'], b['release_baseline_check']],
    selected=dict(ours=a['selected'], codex=b['selected']),
    after_row_differing_columns=row_diff,
    note='after_row · selected 의 차이 = tau2 끝자리 (φ 8.975979010256552 ↔ …554 · Linux ↔ Windows) 뿐')
with open(OUT, 'w', encoding='utf-8') as fh:
    json.dump(res, fh, ensure_ascii=False, indent=2)
print(json.dumps({k: (v if k != 'ours_dir_files' else len(v)) for k, v in res.items()}, ensure_ascii=False)[:3000])
