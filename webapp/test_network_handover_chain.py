"""망 정지 사슬 끝-끝 회귀 — 실 생산자 → 실 정지 helper → 실 τ 소비자 → 실 배치 기록 → 실 인계 생성기 (SELF-86 · Codex 10-05 §7 ② ③).

  ① `network_conductivity.py` CLI 그대로 (test_pipeline_provenance._CLIRunner — runpy) 를 `app._network_and_stage_e(stop_before_stage_e=True)`
     에 넣어 세 침대를 돈다: 관통 · 정상 비관통 · 관통인데 풀이 실패 (spsolve 예외 주입) → done · done · failed (RGL-02 · 04 · 08).
  ② 같은 결과를 `tau_flux.case_row` 가 OK · NOT_PERCOLATING · NOT_COMPUTED 로 소비한다.
  ③ 세 상태를 실 LHS 배치 (`docs/data/lhs_webapp_contact_d1ec42fba` · 130 · 접촉 단계 생산본) 의 세 케이스 기록에 얹고
     `lhs_webapp_batch.write_outputs` 로 network 배치 (stop_after=network) 를 쓴 뒤 `load_webapp` → `build_handover` (⑤⑥⑦ 다섯 묶음):
     done 두 행 = 접촉 단계 판과 같은 값 · failed 행 = wa_status failed · 웹앱 열 빈칸 · 인계 거부 없음 (RGL-03).
  ⚠ ③ 의 행 값은 접촉 단계 생산본이다 — 합성 침대는 정지 **상태**만 넘긴다 (인계 생성기는 아직 망 단계 고유 열을 싣지 않는다).
     옛 코드: ① 의 정상 비관통이 failed (RGL-02) · ③ 은 network 배치를 거부 (RGL-03)."""
import csv
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCRIPTS = ROOT / 'scripts'
for _p in (str(HERE), str(SCRIPTS)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import pipeline_service as ps            # noqa: E402
import test_pipeline_provenance as TP    # noqa: E402  (침대 · 실 CLI 대역 — 같은 도구를 쓴다)

PASS = FAIL = 0


def chk(label, ok, detail=''):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f'  PASS {label}')
    else:
        FAIL += 1
        print(f'  FAIL {label}' + (f' — {detail}' if detail else ''))


def _run_bed(app, bed, break_solver=False):
    d = tempfile.mkdtemp(prefix='chain_')
    a, c = TP._write_bed(d, bed)
    with open(os.path.join(d, 'full_metrics.json'), 'w') as f:
        json.dump(TP._bed_ledger(bed), f)
    stages, rid = app._network_and_stage_e(d, str(SCRIPTS), a, c, '1:SE', 1, [],
                                           runner=TP._CLIRunner(break_solver=break_solver), stop_before_stage_e=True)
    st, failed = ps.summarize(stages)
    return d, st, [s.get('step', '') for s in failed]


def main():
    import app
    import tau_flux as tf
    import lhs_webapp_batch as LWB
    import lhs_design_dataset as LDD

    print('① 실 생산자 → 실 정지 helper (세 침대)')
    runs = {'through': _run_bed(app, 'through'), 'nonthrough': _run_bed(app, 'nonthrough'),
            'solve_failed': _run_bed(app, 'through', break_solver=True)}
    got = {k: v[1] for k, v in runs.items()}
    chk(f'관통 · 정상 비관통 · 수치 실패 = done · done · failed ({got})',
        got == {'through': 'done', 'nonthrough': 'done', 'solve_failed': 'failed'})
    _fs = runs['solve_failed'][2]
    chk(f'수치 실패는 정지 계약 단계에서 걸린다 ({_fs})', any('Network stop contract' in s for s in _fs))
    _d3 = runs['solve_failed'][0]
    _attp = os.path.join(_d3, ps.ATTEMPT_FILE)                     # 파일을 직접 읽는다 (옛 코드에서도 같은 시험이 돈다)
    _att = json.load(open(_attp)) if os.path.exists(_attp) else {}
    _prov = ps.read_network_provenance(_d3) or {}
    _left = sorted(n for n in os.listdir(_d3) if n.startswith('network_conductivity'))
    _fm3 = json.load(open(os.path.join(_d3, 'full_metrics.json')))
    chk(f"수치 실패 (첫 실행) → 활성 세대 없음 ({_prov.get('provenance_state')!r}) · 망 JSON 없음 {_left} · full_metrics = 장부 그대로 · "
        f"최근 시도 failed ({_att.get('solver_status')!r} · 단계 {_att.get('stage')!r})",
        _prov.get('solver_status') != 'success' and _prov.get('provenance_state') == 'missing' and not _left
        and _fm3 == json.loads(json.dumps(TP._bed_ledger('through')))
        and _att.get('solver_status') == 'failed' and 'Network stop contract' in str(_att.get('stage')))

    print('② 실 τ 소비자')
    tau = {k: tf.case_row(v[0]) for k, v in runs.items()}
    _ts = {k: (t.get('ion_net_status_hertz'), t.get('ion_net_status_physics')) for k, t in tau.items()}
    chk(f'τ 인계 상태 = OK · NOT_PERCOLATING · NOT_COMPUTED (두 모드) ({_ts})',
        _ts['through'] == ('OK', 'OK') and _ts['nonthrough'] == ('NOT_PERCOLATING', 'NOT_PERCOLATING')
        and all(s_ and s_.startswith('NOT_COMPUTED') for s_ in _ts['solve_failed']))
    chk('정상 비관통의 f = 0 · tau2 빈칸 (물리적 0 · 0 으로 채운 τ 아님)',
        tau['nonthrough'].get('f_ion_hertz') == 0.0 and tau['nonthrough'].get('tau2_ion_hertz') in (None, ''),
        str({k: tau['nonthrough'].get(k) for k in ('f_ion_hertz', 'tau2_ion_hertz')}))

    print('③ 실 배치 기록 (stop_after=network) → 실 인계 생성기')
    src = ROOT / 'docs/data/lhs_webapp_contact_d1ec42fba'
    st0 = json.loads((src / 'status.json').read_text(encoding='utf-8'))
    with open(src / 'metrics_flat.csv', encoding='utf-8', newline='') as fh:
        flat = {r['case']: {k: v for k, v in r.items() if v != ''} for r in csv.DictReader(fh)}
    done = sorted(c for c, r in st0['cases'].items() if r.get('status') == 'done' and c in flat)
    perc0 = [c for c in done if float(flat[c].get('percolation_pct', 'nan')) == 0.0]
    percp = [c for c in done if float(flat[c].get('percolation_pct', 'nan')) > 0.0]
    chk(f'실 배치에 관통 · 비관통 done 케이스가 있다 ({len(percp)} · {len(perc0)})', bool(perc0) and len(percp) >= 2)
    pick = {'through': percp[0], 'nonthrough': perc0[0], 'solve_failed': percp[1]}
    st = json.loads(json.dumps(st0))
    st['stop_after'] = 'network'
    for c, r in st['cases'].items():
        r.update(stop_after='network', network_run_id='RUN-CHAIN')
    for k, c in pick.items():
        st['cases'][c]['status'] = runs[k][1]
        st['cases'][c]['failed_stages'] = runs[k][2]
    tdir = Path(tempfile.mkdtemp(prefix='chain_batch_'))
    try:
        LWB.write_outputs(tdir, st, flat)
        lw = LDD.load_webapp(tdir)
        chk(f"load_webapp 이 배치의 stop_after 를 넘긴다 ({lw.get('stop_after')!r})", lw.get('stop_after') == 'network')
        with (ROOT / LDD.DESCRIPTOR_FILL_EXPECTED['path']).open(encoding='utf-8-sig') as fh:
            rows = list(csv.DictReader(fh))
        hv = LDD.load_harvest(ROOT / 'docs/data/lhs_descriptors_cov_1e09f661d')
        un = LDD.load_union(ROOT / LDD.DEFAULT_UNION_TSV)
        groups = 'contact,percolation,f1,fracture,area'
        o_c, c_c, _ = LDD.build_handover(rows, hv, union=un, webapp=LDD.load_webapp(src), webapp_groups=groups)
        try:
            o_n, c_n, r_n = LDD.build_handover(rows, hv, union=un, webapp=lw, webapp_groups=groups)
            err = ''
        except LDD.FillRefusal as e:
            o_n, c_n, r_n, err = [], [], {}, str(e)
        chk('network 배치를 ⑤⑥⑦ 다섯 묶음으로 받는다 (옛 코드 = 거부 · RGL-03)', not err and len(o_n) == len(o_c), err[:160])
        if not err:
            by_c = {r['case_id']: r for r in o_c}
            by_n = {r['case_id']: r for r in o_n}
            same = [c for c in by_c if c not in (pick['solve_failed'],) and by_c[c] == by_n.get(c)]
            chk(f'failed 로 바꾼 한 행 밖의 {len(same)}/{len(by_c) - 1} 행 = 접촉 단계 판과 같은 값 (관통 · 정상 비관통 done 포함)',
                len(same) == len(by_c) - 1 and pick['through'] in same and pick['nonthrough'] in same)
            rf, rc_ = by_n[pick['solve_failed']], by_c[pick['solve_failed']]
            #  접촉 단계 판 (done) 과 달라진 칸은 상태 두 칸이거나 **빈칸이 된** 웹앱 열뿐이어야 한다 (값이 바뀌거나 새로 생기면 안 된다)
            diff = [k for k in c_c if rf.get(k) != rc_.get(k)]
            bad = [k for k in diff if k not in ('wa_status', 'wa_failed_stages') and rf.get(k) not in (None, '')]
            cleared = [k for k in diff if k not in ('wa_status', 'wa_failed_stages') and rf.get(k) in (None, '')]
            chk(f"수치 실패 행 = wa_status failed ({rf.get('wa_status')!r}) · 웹앱 열 {len(cleared)} 칸 빈칸 · 다른 값으로 바뀐 칸 0",
                rf.get('wa_status') == 'failed' and len(cleared) > 20 and not bad and set(c_n) == set(c_c), str(bad[:5]))
    finally:
        shutil.rmtree(tdir, ignore_errors=True)
        for v in runs.values():
            shutil.rmtree(v[0], ignore_errors=True)

    print(f'\ntest_network_handover_chain: {PASS}/{PASS + FAIL} PASS')
    return 0 if FAIL == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
