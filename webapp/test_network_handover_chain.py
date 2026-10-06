"""망 정지 사슬 끝-끝 회귀 — 실 생산자 → 실 정지 helper → 실 τ 소비자 → 실 배치 기록 → 실 인계 생성기 (SELF-86 · Codex 10-05 §7 ② ③).

  ① `network_conductivity.py` CLI 그대로 (test_pipeline_provenance._CLIRunner — runpy) 를 `app._network_and_stage_e(stop_before_stage_e=True)`
     에 넣어 세 침대를 돈다: 관통 · 정상 비관통 · 관통인데 풀이 실패 (spsolve 예외 주입) → done · done · failed (RGL-02 · 04 · 08).
  ② 같은 결과를 `tau_flux.case_row` 가 OK · NOT_PERCOLATING · NOT_COMPUTED 로 소비한다.
  ③ 세 상태를 실 LHS 배치 (`docs/data/lhs_webapp_contact_d1ec42fba` · 130 · 접촉 단계 생산본) 의 세 케이스 기록에 얹고
     `lhs_webapp_batch.write_outputs` 로 network 배치 (stop_after=network) 를 쓴 뒤 `load_webapp` → `build_handover` (⑤⑥⑦ 다섯 묶음):
     done 두 행 = 접촉 단계 판과 같은 값 · failed 행 = wa_status failed · 웹앱 열 빈칸 · 인계 거부 없음 (RGL-03).
  ⚠ ③ 의 행 값은 접촉 단계 생산본이다 — 합성 침대는 정지 **상태**만 넘긴다 (③ 은 다섯 census 묶음만 — 망 단계 고유 열은 ④).
  ④ (v1.2 망 τ 묶음) ① 의 실 생산자 폴더를 배치 `--work/results/<case>` 모양으로 놓고 `load_tau_results` (출처 관문 P0–P4 — run id · 도장 ·
     입력 digest · metrics_flat 과 같은 세대 · 망 정지 계약 재검사) → `build_handover(webapp_groups='tau')`: 관통 OK · 비관통 NOT_PERCOLATING · 수치 실패 행 τ 빈칸 ·
     배치 뒤 다시 돌린 폴더 (새 run id) 는 거부.  ⚠ ④ 의 행은 실 배치 케이스 이름 + 합성 침대의 τ — 출처 관문 · 값 규칙 시험이지 그 케이스의 값이 아니다.
  ④c (10-05 RGLR3-02 · Codex 4차 재검증 probes/new_probes.py) — 같은 실 생산자 폴더에서 **dual 만** 바꾼 두 반례 (두 모드 띠 규칙 L0 → L1 · σ₀ ×2 와
     σ_dim 6 자리 재계산) 는 인계 때 망 정지 계약 재검사 (τ P4) 가 거부 · 기존 셋 (입력 바이트 P2 · σ_ratio ×4 P3 · run id P1) 그대로 · 정상 L0 · 비관통 ·
     띠 L1 · L2 는 옛 판과 같은 칸으로 받는다.
     옛 코드: ① 의 정상 비관통이 failed (RGL-02) · ③ 은 network 배치를 거부 (RGL-03) · ④ 는 묶음 tau · 로더가 없다 · ④c 의 dual 반례 둘을 받았다 (RGLR3-02)."""
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
    return d, st, [s.get('step', '') for s in failed], rid          # rid = 이번 실행의 망 세대 (배치가 케이스 기록에 남기는 network_run_id)


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
    #  ★ 10-05 WEB-03 Q1 — 생산자가 관통 풀이 실패를 채널 상태 failed 로 신고 → 망 솔버 단계의 내용 검증이 정지 계약보다 먼저 막는다
    #    (옛: 채널 valid_null 이라 정지 계약 ③ 에서 걸렸다 — ③ 은 두 번째 방어로 남는다).
    chk(f'수치 실패는 망 솔버 단계 (채널 failed → 내용 검증 · WEB-03 Q1) 에서 걸린다 ({_fs})', any(s.startswith('Network Solver') for s in _fs))
    _d3 = runs['solve_failed'][0]
    _attp = os.path.join(_d3, ps.ATTEMPT_FILE)                     # 파일을 직접 읽는다 (옛 코드에서도 같은 시험이 돈다)
    _att = json.load(open(_attp)) if os.path.exists(_attp) else {}
    _prov = ps.read_network_provenance(_d3) or {}
    _left = sorted(n for n in os.listdir(_d3) if n.startswith('network_conductivity'))
    _fm3 = json.load(open(os.path.join(_d3, 'full_metrics.json')))
    chk(f"수치 실패 (첫 실행) → 활성 세대 없음 ({_prov.get('provenance_state')!r}) · 망 JSON 없음 {_left} · full_metrics = 장부 그대로 · "
        f"최근 시도 failed ({_att.get('solver_status')!r} · 단계 {_att.get('stage')!r} · 종류 {_att.get('failure_kind')!r})",
        _prov.get('solver_status') != 'success' and _prov.get('provenance_state') == 'missing' and not _left
        and _fm3 == json.loads(json.dumps(TP._bed_ledger('through')))
        and _att.get('solver_status') == 'failed' and str(_att.get('stage')).startswith('Network Solver')
        and _att.get('failure_kind') == 'solver' and _att.get('active_status') == 'none')

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

        print('④ 실 생산자 폴더 → 망 τ 원천 (load_tau_results · 출처 관문 P0–P4) → 인계 생성기 묶음 tau (v1.2)')
        #  배치 기록 = 이번 실행의 run id · metrics_flat 행 = 실 배치 접촉 단계 행 + 폴더 full_metrics 의 τ 대조 키 (row_for 처럼 **있는** 키만 —
        #   합성 침대의 porosity 로 같은 프레임 QC 를 덮지 않는다 · 묶음 tau 만 부르니 ① ② 관문은 돌지 않는다)
        tie = tuple(ps.NETWORK_STOP_LEDGER_KEYS) + tuple(getattr(LDD, 'TAU_TIE_EXTRA', ()))
        res = tdir / 'results'
        res.mkdir()
        st4 = json.loads(json.dumps(st0))
        st4.update(stop_after='network', cases={})
        rows4 = {}
        for k, c in pick.items():
            d_, s_, f_, rid_ = runs[k]
            shutil.copytree(d_, res / c)                                  # 배치 --work/results/<case> 모양
            st4['cases'][c] = dict(st0['cases'][c], stop_after='network', status=s_, failed_stages=f_, network_run_id=rid_)
            fm_ = json.loads((res / c / 'full_metrics.json').read_text(encoding='utf-8'))
            rows4[c] = dict(flat[c], **{kk: fm_[kk] for kk in tie if kk in fm_})
        LWB.write_outputs(tdir / 'batch4', st4, rows4)
        lw4 = LDD.load_webapp(tdir / 'batch4')
        rows3 = [r for r in rows if r['case_id'] in set(pick.values())]
        tcols = list(tf.column_names())
        try:
            tv4 = LDD.load_tau_results(res, lw4)
            o4, _c4, r4 = LDD.build_handover(rows3, hv, union=un, webapp=lw4, webapp_groups='tau', tau=tv4)
            err4 = ''
        except Exception as e:                                            # noqa: BLE001 — 옛 코드 (로더 · tau= 없음) 도 실패로 센다
            o4, r4, err4 = [], {}, f'{type(e).__name__}: {e}'
        by4 = {r['case_id']: r for r in o4}
        want4 = {k: {cc: tf._cell(v) for cc, v in tf.case_row(str(res / pick[k])).items() if cc in tcols} for k in ('through', 'nonthrough')}
        _t4, _n4, _f4 = by4.get(pick['through'], {}), by4.get(pick['nonthrough'], {}), by4.get(pick['solve_failed'], {})
        chk('④ 실 생산자 폴더 → 묶음 tau: 관통 OK · 정상 비관통 NOT_PERCOLATING (f 0.0 · tau2 빈칸) · 칸 = tau_flux.case_row 그대로 · 수치 실패 행 '
            '(wa_status failed) τ 칸 전부 빈칸 · 출처 관문 2 행 · 빈칸 행 1',
            not err4 and all({cc: by4.get(pick[k], {}).get(cc) for cc in tcols} == want4[k] for k in want4)
            and _t4.get('ion_net_status_hertz') == _t4.get('ion_net_status_physics') == 'OK'
            and _n4.get('ion_net_status_hertz') == 'NOT_PERCOLATING' and _n4.get('f_ion_hertz') == '0.0' and _n4.get('tau2_ion_hertz') == ''
            and _f4.get('wa_status') == 'failed' and all(_f4.get(cc) == '' for cc in tcols)
            and r4.get('tau_checked') == 2 and r4.get('tau_blank_rows') == 1, err4[:200])
        d5 = _run_bed(app, 'through')                                     # 배치 뒤 같은 케이스를 다시 돌렸다 (새 run id · 새 도장 · 새 dual)
        try:
            shutil.rmtree(res / pick['through'])
            shutil.copytree(d5[0], res / pick['through'])
            try:
                LDD.load_tau_results(res, lw4)
                err5 = '거부하지 않았다'
            except Exception as e:                                        # noqa: BLE001
                err5 = f'{type(e).__name__}: {e}'
        finally:
            shutil.rmtree(d5[0], ignore_errors=True)
        chk('④b 배치 뒤 다시 돌린 폴더 (실 생산자 새 run id) 로는 τ 를 싣지 않는다 — FillRefusal τ P1 (낡은 세대)',
            err5.startswith('FillRefusal') and 'τ P1' in err5, err5[:200])

        print('④c Codex 4차 재검증 RGLR3-02 (probes/new_probes.py 그대로) — 실 생산자 폴더에서 dual 만 바꾼 반례 · 정상 L0 · L1 · L2 · 비관통 보존')
        #  입력 · 도장 · run id · full_metrics · 배치 metrics_flat · 모드 파일 · legacy 는 그대로 두고 **dual 만** 바꾼다 (Codex 표 두 줄).  옛 로더 (P0–P3) 는
        #   dual 의 σ_ratio · 상태 두 키만 full_metrics 와 맞대어 띠 규칙 L1 (BAND_FALLBACK) · σ₀ ×2 (σ₀ 6.0 mS/cm) 를 받았다.  인계 때 망 정지 계약
        #   (pipeline_service.network_stop_verdict — 전 사본 · 투영 · σ₀ 짝) 을 다시 부르면 거부된다 (τ P4).  기존 반례 셋 (P1 · P2 · P3) 은 그대로.
        runs.update({'band_l1': _run_bed(app, 'band_l1'), 'band_l2': _run_bed(app, 'band_l2')})
        chk(f"④c 실 생산자 침대 띠 L1 · L2 = done · done ({runs['band_l1'][1]} · {runs['band_l2'][1]})",
            runs['band_l1'][1] == runs['band_l2'][1] == 'done')

        def _tau_batch(tag, cases):
            """{케이스: 실 생산자 폴더} → (results 루트, load_webapp) — 배치 기록 = 그 폴더의 run id · metrics_flat 행 = full_metrics 스칼라 (row_for 처럼)."""
            root = tdir / f'tau_{tag}'
            res_ = root / 'results'
            res_.mkdir(parents=True)
            stx = json.loads(json.dumps(st0))
            stx.update(stop_after='network', cases={})
            rowsx = {}
            for c, d_ in cases.items():
                shutil.copytree(d_, res_ / c)
                fm_ = json.loads((res_ / c / 'full_metrics.json').read_text(encoding='utf-8'))
                stx['cases'][c] = dict(case=c, stop_after='network', status='done', failed_stages=[], network_run_id=fm_['network_run_id'])
                rowsx[c] = dict({k: v for k, v in fm_.items() if not isinstance(v, (dict, list))}, case=c)
            LWB.write_outputs(root / 'batch', stx, rowsx)
            return res_, LDD.load_webapp(root / 'batch')

        def _try_load(res_, lw_):
            try:
                return LDD.load_tau_results(res_, lw_), ''
            except Exception as e:                                        # noqa: BLE001
                return None, f'{type(e).__name__}: {e}'

        pos = {'L0_through': runs['through'][0], 'nonthrough': runs['nonthrough'][0], 'L1': runs['band_l1'][0], 'L2': runs['band_l2'][0]}
        res_p, lw_p = _tau_batch('pos', pos)
        tv_p, err_p = _try_load(res_p, lw_p)
        want_p = {c: {cc: tf._cell(v) for cc, v in tf.case_row(str(d_)).items() if cc in tcols} for c, d_ in pos.items()}
        got_p = {c: (tv_p or {}).get('cases', {}).get(c, {}).get('cells') for c in pos}
        _st_p = {c: ((got_p[c] or {}).get('ion_net_status_hertz'), (got_p[c] or {}).get('ion_net_band_rule_hertz')) for c in pos}
        chk(f'④c 정상 L0 · 비관통 · 띠 L1 · L2 = 받는다 · 칸 = tau_flux.case_row 그대로 (옛 판과 같다 · "L1 을 모두 거부" 하지 않는다) {_st_p}',
            not err_p and all(got_p[c] == want_p[c] for c in pos)
            and _st_p == {'L0_through': ('OK', 'L0'), 'nonthrough': ('NOT_PERCOLATING', 'L0'), 'L1': ('BAND_FALLBACK', 'L1'),
                          'L2': ('BAND_FALLBACK', 'L2')}, err_p[:200])

        def _dual_band(du):
            for m in ('hertzian', 'physics'):
                du[m]['boundary_rule'] = 'L1'

        def _dual_sigma0(du):
            for m in ('hertzian', 'physics'):
                du[m]['sigma_grain_S_cm'] *= 2
                du[m]['sigma_full_mScm'] = round(1000 * du[m]['sigma_grain_S_cm'] * du[m]['sigma_full'], 6)

        def _neg(key, label, tag, edit):
            res_, lw_ = _tau_batch(key, {'lhs00_000': runs['through'][0]})
            cd = res_ / 'lhs00_000'
            edit(cd)
            tv_, err_ = _try_load(res_, lw_)
            cells = (tv_ or {}).get('cases', {}).get('lhs00_000', {}).get('cells') or {}
            chk(f'④c {label} → 거부 ({tag})', err_.startswith('FillRefusal') and tag in err_,
                (err_ or f"받았다: {cells.get('ion_net_status_hertz')} · σ₀ {cells.get('ion_sigma0_mScm')} · 띠 {cells.get('ion_net_band_rule_hertz')}")[:240])

        def _edit_json(name, fn):
            def _e(cd):
                p = cd / name
                x = json.loads(p.read_text(encoding='utf-8'))
                fn(x)
                p.write_text(json.dumps(x, ensure_ascii=False, indent=2), encoding='utf-8')
            return _e

        def _atoms_append(cd):
            with (cd / 'atoms.csv').open('a', encoding='utf-8') as fh:
                fh.write('\n')
        _neg('dual_band', 'dual 만 두 모드 띠 규칙 L0 → L1 (Codex dual_band_only — 옛: BAND_FALLBACK 로 수용)', 'τ P4 — 망 정지 계약 재검사',
             _edit_json('network_conductivity_dual.json', _dual_band))
        #  ★ 10-07 G2RR2-04 — 이 반례는 이제 같은 τ P4 의 앞 관문 (세대 계약의 σ₀ 결합: 증서 σ₀ ≠ 부모 σ₀ · CF 차원값을 부모 σ₀ 로 재구성) 에서 먼저 걸린다
        #    (거부 지점은 그대로 인계 τ P4 · 정지 계약 재검사 ⑧ 도 같은 함수로 거부한다)
        _neg('dual_sigma0', 'dual 만 두 모드 σ₀ ×2 · σ_dim 6 자리 재계산 (Codex dual_sigma0_only — 옛: OK · σ₀ 6.0 으로 수용)', 'τ P4',
             _edit_json('network_conductivity_dual.json', _dual_sigma0))
        _neg('atom_input', 'atom 입력 바이트 변경 (Codex atom_input_mutation)', 'τ P2', _atoms_append)
        _neg('dual_ratio', 'dual σ_ratio 만 ×4 (Codex dual_sigma_ratio_only)', 'τ P3',
             _edit_json('network_conductivity_dual.json', lambda du: du['hertzian'].update(sigma_full=du['hertzian']['sigma_full'] * 4)))
        _neg('run_id', 'full_metrics run id 변경 (Codex run_id_mismatch)', 'τ P1',
             _edit_json('full_metrics.json', lambda fm: fm.update(network_run_id='other')))
    finally:
        shutil.rmtree(tdir, ignore_errors=True)
        for v in runs.values():
            shutil.rmtree(v[0], ignore_errors=True)

    print(f'\ntest_network_handover_chain: {PASS}/{PASS + FAIL} PASS')
    return 0 if FAIL == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
