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
     옛 코드: ① 의 정상 비관통이 failed (RGL-02) · ③ 은 network 배치를 거부 (RGL-03) · ④ 는 묶음 tau · 로더가 없다 · ④c 의 dual 반례 둘을 받았다 (RGLR3-02).
  ⑤ ★ 10-15 L214 (Codex LHS214 판정 §2 · §4 A3 · 수정 계획 §3 A3 — 1저자 10-14 비준 Q1–Q5 권고대로) — FULL 모형 한계 (수치 인증 통과 · q > 1.5 출력 채택 거부)
     를 **실 생산자 CLI** (침대 ml_physics · ml_hertz · ml_el — test_pipeline_provenance._bed) 로 내고 실제 소비 경로 끝까지: 정지 · 일반 경로 게시 (done) ·
     활성 세대 · 모형 한계 + 열 채널 진짜 실패 = 차단 (첫 실행 활성 없음 · 다시 돌리면 옛 세대 보존) · τ (정확한 사유 · 값 빈칸) · 다시 읽기 K1–K7 + 위조 폴더 거부 ·
     인계 (load_tau_results · build_handover 묶음 tau) · 배포 (빈칸 뜻 NA_MODEL_LIMIT · 주 타깃 Hertz 모형 한계 = HOLD) · 화면 (L214-03 — Physics σ 가 없으면
     Hertz 를 복사하지 않는다 · Δ — + 사유 · 새 표 · 기존 CSV 표 · 이온 · 전자 · 원 결과 (Codex 합성 metrics) · 병합 결과 (게시 폴더 → _load_case_tables =
     케이스 · 보고서 · 보관함 라우트가 같이 쓰는 함수)).  옛 코드: 모형 한계 침대 셋이 failed (WEB-03 Q1 이 Hertz 포함 레코드 전체를 막음) · 화면 복사."""
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


def _run_ml(app, bed, tm='1:SE', stop=True, d=None, **rk):
    """⑤ L214 — 실 생산자 CLI 로 침대 하나 (`TP._bed` 이름) · d 가 있으면 그 폴더에서 다시 (옛 세대 보존 시험) · rk = `_CLIRunner` 인자 (break_channel …) ·
    일반 경로 (stop False) 의 Stage E = `TP._fake_stage_e` 대역 (같은 도구)."""
    d = d or tempfile.mkdtemp(prefix='chain_ml_')
    a, c = TP._write_bed(d, bed)
    fmp = os.path.join(d, 'full_metrics.json')
    if not os.path.exists(fmp):
        with open(fmp, 'w') as f:
            json.dump(TP._bed_ledger(bed), f)
    stages, rid = app._network_and_stage_e(d, str(SCRIPTS), a, c, tm, 1, [], runner=TP._CLIRunner(delegate=TP._fake_stage_e, **rk),
                                           stop_before_stage_e=stop)
    st, failed = ps.summarize(stages)
    return d, st, [s.get('step', '') for s in failed], rid


def _jload(d, n):
    p = os.path.join(str(d), n)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}


def _l214_chain(app, tf, LWB, LDD, tdir, st0, flat, rows, hv, un, percp, tcols):
    """⑤ L214 — FULL 모형 한계의 실제 소비 경로 끝-끝 (모듈 머리 ⑤)."""
    import g2_network_reread as RR
    import lhs_release_build as LRB
    ML, CH = 'full_over_conduction', 'model_limit'
    print('⑤ L214 — FULL 모형 한계 (수치 인증 통과 · q > 1.5 출력 채택 거부) · 실 생산자 CLI → 게시 → 활성 세대 → τ → 다시 읽기 → 인계 → 배포 → 화면')
    runs, extra = {}, []
    try:
        runs['ml_physics'] = _run_ml(app, 'ml_physics')
        runs['ml_hertz'] = _run_ml(app, 'ml_hertz')
        runs['ml_el'] = _run_ml(app, 'ml_el', tm='1:SE,2:AM_P')
        runs['ml_general'] = _run_ml(app, 'ml_physics', stop=False)
        runs['ml_th_fail'] = _run_ml(app, 'ml_physics', break_channel='thermal')
        got = {k: v[1] for k, v in runs.items()}
        chk(f'⑤a 정지 경로 physics 모형 한계 · 주 타깃 Hertz 모형 한계 · 전자 모형 한계 = done (레코드 게시) · 일반 경로 (Stage E 대역) = done · '
            f'모형 한계 + 열 채널 진짜 실패 = failed (옛: 넷 다 failed — WEB-03 Q1 이 레코드 전체 차단) {got}',
            got == {'ml_physics': 'done', 'ml_hertz': 'done', 'ml_el': 'done', 'ml_general': 'done', 'ml_th_fail': 'failed'})
        dP = runs['ml_physics'][0]
        du, fm, prov = _jload(dP, 'network_conductivity_dual.json'), _jload(dP, 'full_metrics.json'), ps.read_network_provenance(dP)
        p_, h_ = du.get('physics') or {}, du.get('hertzian') or {}
        chk('⑤b 게시된 physics = 모형 한계 레코드 (not_computed · full_over_conduction · 채널 model_limit · 증서 q_withheld > 1.5) · full_metrics 투영 (physics σ None · '
            '상태 · 사유 꼬리) · 도장 success = 이번 run id · Hertz 값 · 상태 그대로',
            p_.get('sigma_full_reason') == ML and p_.get('ionic_status') == CH and (p_.get('solve_certificate_full') or {}).get('q_withheld', 0) > 1.5
            and fm.get('sigma_full_status_physics') == 'not_computed' and fm.get('sigma_full_reason_physics') == ML and fm.get('sigma_full_mScm_physics') is None
            and fm.get('network_solver_status') == 'success' and prov.get('solver_status') == 'success' and prov.get('network_run_id') == runs['ml_physics'][3]
            and fm.get('sigma_full_mScm') is not None and fm.get('sigma_full_mScm') == h_.get('sigma_full_mScm') and h_.get('ionic_status') == 'computed',
            repr({k: fm.get(k) for k in ('sigma_full_status_physics', 'sigma_full_reason_physics', 'network_solver_status')}))
        dE = runs['ml_el'][0]
        duE, fmE = _jload(dE, 'network_conductivity_dual.json'), _jload(dE, 'full_metrics.json')
        chk('⑤b2 전자 모형 한계 — dual physics 전자 채널 model_limit · full_metrics 에 electronic_sigma_full_status · _reason 이 physics 꼬리까지 투영 '
            '(Codex §2 끝 문단 — 출력까지 전파) · Hertz 전자 computed · 열 상태 · 사유도 실린다',
            (duE.get('physics') or {}).get('electronic_status') == CH and fmE.get('electronic_sigma_full_status_physics') == 'not_computed'
            and fmE.get('electronic_sigma_full_reason_physics') == ML and fmE.get('electronic_sigma_full_mScm_physics') is None
            and fmE.get('electronic_sigma_full_status') == 'computed' and fmE.get('electronic_sigma_full_mScm') is not None
            and fmE.get('thermal_sigma_full_status') == 'computed',
            repr({k: fmE.get(k) for k in ('electronic_sigma_full_status_physics', 'electronic_sigma_full_reason_physics', 'electronic_sigma_full_status')}))
        dF = runs['ml_th_fail'][0]
        attF, provF = _jload(dF, ps.ATTEMPT_FILE), ps.read_network_provenance(dF)
        leftF = sorted(n for n in os.listdir(dF) if n.startswith('network_conductivity'))
        chk(f"⑤c 모형 한계 + 같은 실행 열 채널 진짜 실패 → failed (진짜 실패 우선 · 망 솔버 단계 내용 검증) · 첫 실행 = 활성 세대 없음 · 망 JSON 없음 · 최근 시도 failed "
            f"({runs['ml_th_fail'][2]} · {provF.get('provenance_state')!r} · {attF.get('failure_kind')!r})",
            any(s.startswith('Network Solver') for s in runs['ml_th_fail'][2]) and provF.get('provenance_state') == 'missing' and not leftF
            and attF.get('solver_status') == 'failed' and attF.get('failure_kind') == 'solver' and attF.get('active_status') == 'none'
            and 'thermal' in str(attF.get('reason')))
        dK = tempfile.mkdtemp(prefix='chain_mlk_')
        extra.append(dK)
        shutil.rmtree(dK)
        shutil.copytree(dP, dK)
        h0 = {n: ps.file_digest(os.path.join(dK, n)) for n in TP._NET_FOUR}
        rK = _run_ml(app, 'ml_physics', d=dK, break_channel='thermal')
        h1 = {n: ps.file_digest(os.path.join(dK, n)) for n in TP._NET_FOUR}
        provK, attK = ps.read_network_provenance(dK), _jload(dK, ps.ATTEMPT_FILE)
        chk(f"⑤d 게시된 모형 한계 세대 위에서 다시 돈 실행이 진짜 실패 → failed · 옛 세대 네 JSON sha256 그대로 · 활성 id = 옛 run id · previous_generation_kept "
            f"({rK[1]} · {provK.get('network_run_id') == runs['ml_physics'][3]} · {attK.get('previous_generation_kept')!r})",
            rK[1] == 'failed' and h0 == h1 and all(h0.values()) and provK.get('network_run_id') == runs['ml_physics'][3]
            and attK.get('previous_generation_kept') is True)
        tP, tH, tE = (tf.case_row(runs[k][0]) for k in ('ml_physics', 'ml_hertz', 'ml_el'))
        chk('⑤e τ — physics NOT_COMPUTED · 사유 정확히 full_over_conduction · f · tau2 · tau 빈칸 · Hertz OK · H12 OK / 주 타깃 모형 한계 = 세 모드 NOT_COMPUTED '
            'full_over_conduction / 전자 모형 한계 = 이온 두 모드 OK (이온 τ 와 무관)',
            tP.get('ion_net_status_physics') == 'NOT_COMPUTED' and tP.get('ion_net_status_reason_physics') == ML
            and all(tP.get(k) is None for k in ('f_ion_physics', 'tau2_ion_physics', 'tau_ion_physics'))
            and tP.get('ion_net_status_hertz') == 'OK' and tP.get('ion_net_status_hertz_h12') == 'OK'
            and all(tH.get(f'ion_net_status_{m}') == 'NOT_COMPUTED' and tH.get(f'ion_net_status_reason_{m}') == ML for m in ('hertz', 'hertz_h12', 'physics'))
            and tE.get('ion_net_status_hertz') == 'OK' and tE.get('ion_net_status_physics') == 'OK',
            repr({k: (t.get('ion_net_status_physics'), t.get('ion_net_status_reason_physics')) for k, t in (('P', tP), ('H', tH), ('E', tE))}))
        rep = {k: RR.reread_case(runs[k][0], 'g2', ps, tf) for k in ('ml_physics', 'ml_hertz', 'ml_el')}
        bad = {k: [c['name'][:2] + ': ' + c['detail'][:120] for c in r['checks'] if not c['ok']] for k, r in rep.items()}
        chk('⑤f 다시 읽기 K1–K7 (게시 · 세대 계약 + 증서 결합 · 도장 · 정지 계약 다시 · 열 역할 · 관통 일치 K6 (모형 한계 = τ NOT_COMPUTED full_over_conduction) · '
            '가지 표) — 세 폴더 전부 통과', not any(bad.values()) and all(len(r['checks']) == 7 for r in rep.values()), bad)
        dX = tempfile.mkdtemp(prefix='chain_mlx_')
        extra.append(dX)
        shutil.rmtree(dX)
        shutil.copytree(dP, dX)

        def _q101(rec, _n, m):
            if m == 'physics' and isinstance(rec.get('solve_certificate_full'), dict):
                rec['solve_certificate_full']['q_withheld'] = rec['solve_certificate_full'].get('q_withheld', 2.0) * 1.01
        TP._edit_net_records(dX, _q101, files=('network_conductivity_physics.json', 'network_conductivity_dual.json'))
        repX = RR.reread_case(dX, 'g2', ps, tf)
        badX = {c['name'][:2] for c in repX['checks'] if not c['ok']}
        #  (K2 세대 계약은 0b 공용 기술 검사를 못 넘은 레코드를 그 검사에 맡긴다 — G2RR-02 이후 설계 `certificate_binding_problems` · 같은 결함을 두 번
        #   보고하지 않는다.  위조 q 는 0b (`ion_record_problem` → 공용 판정) 가 거부 → 정지 계약 다시 (K4) · 관통 일치 (K6) 두 길이 각각 잡는다)
        chk(f'⑤f2 위조 폴더 (physics 증서 q_withheld ×1.01 · dual · 모드 파일 같이) → K4 (정지 계약 다시) · K6 (관통 일치 — 공용 판정) 거부 {sorted(badX)}',
            {'K4', 'K6'} <= badX)
        cid = {'ml_physics': percp[2], 'ml_el': percp[3], 'ml_hertz': percp[4]}
        res5 = tdir / 'results_l214'
        res5.mkdir()
        st5 = json.loads(json.dumps(st0))
        st5.update(stop_after='network', cases={})
        rows5 = {}
        tie = tuple(ps.NETWORK_STOP_LEDGER_KEYS) + tuple(getattr(LDD, 'TAU_TIE_EXTRA', ()))
        for k, c in cid.items():
            d_, s_, f_, rid_ = runs[k]
            shutil.copytree(d_, res5 / c)
            st5['cases'][c] = dict(st0['cases'][c], stop_after='network', status=s_, failed_stages=f_, network_run_id=rid_)
            fm_ = json.loads((res5 / c / 'full_metrics.json').read_text(encoding='utf-8'))
            rows5[c] = dict(flat[c], **{kk: fm_[kk] for kk in tie if kk in fm_})
        LWB.write_outputs(tdir / 'batch_l214', st5, rows5)
        lw5 = LDD.load_webapp(tdir / 'batch_l214')
        try:
            tv5 = LDD.load_tau_results(res5, lw5)
            o5, _c5, r5 = LDD.build_handover([r for r in rows if r['case_id'] in set(cid.values())], hv, union=un, webapp=lw5, webapp_groups='tau', tau=tv5)
            err5 = ''
        except Exception as e:                                            # noqa: BLE001 — 옛 코드 (τ P4 정지 계약 재검사가 모형 한계를 거부) 도 실패로 센다
            o5, r5, err5 = [], {}, f'{type(e).__name__}: {e}'
        by5 = {r['case_id']: r for r in o5}
        want5 = {k: {cc: tf._cell(v) for cc, v in tf.case_row(str(res5 / c)).items() if cc in tcols} for k, c in cid.items()}
        rP5 = by5.get(cid['ml_physics'], {})
        chk('⑤g 인계 — load_tau_results (P0–P4 · τ P4 정지 계약 재검사 = 모형 한계 수용) → build_handover 묶음 tau: 칸 = tau_flux.case_row 그대로 · physics '
            'NOT_COMPUTED full_over_conduction · 값 빈칸 · 출처 관문 3 행 (주 타깃 Hertz 모형 한계 행도 레코드로는 인계 — 배포 관문이 막는다)',
            not err5 and all({cc: by5.get(cid[k], {}).get(cc) for cc in tcols} == want5[k] for k in cid)
            and rP5.get('ion_net_status_physics') == 'NOT_COMPUTED' and rP5.get('ion_net_status_reason_physics') == ML
            and rP5.get('f_ion_physics') == '' and r5.get('tau_checked') == 3, err5[:300])
        pcols = ['case_id', 'f_ion_physics', 'tau2_ion_physics', 'tau_ion_physics', 'ion_net_status_physics', 'ion_net_status_reason_physics']
        gate = getattr(LRB, 'v13_primary_model_limit_problems', None)
        chk('⑤h 배포 — physics 부록 칸 (모형 한계 행) 빈칸 일관성 통과 · 빈칸 코드 NA_MODEL_LIMIT · 주 타깃 관문: 주 Hertz 모형 한계 행 = HOLD (문제) · physics · 전자 '
            '모형 한계 행 = 통과 (행 삭제 · 대체 없음)',
            bool(rP5) and LRB.v13_blank_problems([rP5], pcols) == [] and LRB.v13_blank_reason(rP5, 'f_ion_physics') == 'NA_MODEL_LIMIT'
            and gate is not None and bool(gate([by5.get(cid['ml_hertz'], {})])) and gate([rP5, by5.get(cid['ml_el'], {})]) == [])

        PL = app._PAPER_LABEL_MAP

        def _rows_of(tables):
            return {str(r[0]).strip(): r for r in (tables.get('network_summary') or {}).get('data') or [] if isinstance(r, list) and r}

        def _view(d, csv_rows):
            """게시 폴더 사본 + network_summary.csv (접촉 분석 꼴 두 열) → `_load_case_tables` (케이스 · 보고서 · 보관함 라우트가 같이 쓰는 함수) 의 행."""
            dd = tempfile.mkdtemp(prefix='chain_view_')
            extra.append(dd)
            shutil.rmtree(dd)
            shutil.copytree(d, dd)
            fm_ = _jload(dd, 'full_metrics.json')
            fm_.update(sigma_ratio=0.5, tortuosity_mean=1.2)       # 접촉 분석이 싣는 두 키 (합성 침대 장부에는 없다) — σ_brug / σ_ionic · τ 비 행을 세운다
            with open(os.path.join(dd, 'full_metrics.json'), 'w', encoding='utf-8') as f:
                json.dump(fm_, f)
            with open(os.path.join(dd, 'network_summary.csv'), 'w', encoding='utf-8') as f:
                f.write('지표,값\n' + ''.join(f'{a},{b}\n' for a, b in csv_rows))
            tables, metrics, _ip = app._load_case_tables(dd, {})
            return _rows_of(tables), metrics

        def _cells(rws, lab):
            r = rws.get(PL.get(lab, lab)) or rws.get(lab)
            return (r[1], r[2], r[3]) if r and len(r) >= 4 else None
        fmP = _jload(dP, 'full_metrics.json')
        sh = round(fmP.get('sigma_full_mScm') or 0.0, 4)                 # 고치기 전 = 게시 안 됨 (값 없음 — 아래 검사가 FAIL 로 센다)
        v_new, _m1 = _view(dP, [('SE Volume Fraction', 0.5)])
        v_old, _m2 = _view(dP, [('── Network Solver (Hertzian DEM-native) ──', ''), ('σ_ionic (mS/cm)', sh),
                                ('R_brug (과대추정 배수)', f"{fmP.get('R_brug_over_full') or 1.0:.1f}×")])
        bad_v = {}
        for tag, v_ in (('새 표', v_new), ('기존 CSV 표', v_old)):
            for lab in ('σ_ionic (mS/cm)', 'σ_brug / σ_ionic', 'Contact-free / Full', 'R_brug (과대추정 배수)'):
                c_ = _cells(v_, lab)
                if c_ is None:
                    if lab in ('σ_ionic (mS/cm)', 'σ_brug / σ_ionic'):
                        bad_v[(tag, lab)] = '행 없음'
                    continue
                if not (str(c_[1]).startswith('—') and str(c_[2]).startswith('—')) or str(c_[1]) == str(c_[0]):
                    bad_v[(tag, lab)] = c_
            c_i = _cells(v_, 'σ_ionic (mS/cm)')
            if c_i is not None and (str(c_i[0]) != str(sh) or ML not in str(c_i[1])):
                bad_v[(tag, 'σ_ionic 값 · 사유')] = c_i
        chk(f'⑤i ★ 화면 (L214-03 · 병합 결과 = 게시 폴더 → _load_case_tables) — Physics σ 가 없으면 Physics 칸 · Δ = — (+ 사유 full_over_conduction) · Hertz 를 복사하지 않는다 · '
            f'가짜 Δ 0 % 없음 — σ_ionic · σ_brug/σ_ionic · CF/FULL · R_brug (새 표 · 기존 CSV 표) {bad_v}', not bad_v)
        vE, _m3 = _view(dE, [('── Network Solver (Hertzian DEM-native) ──', ''), ('σ_electronic (mS/cm)', round(fmE.get('electronic_sigma_full_mScm') or 0.0, 2))])
        cE = _cells(vE, 'σ_electronic (mS/cm)')
        chk(f'⑤i2 전자 — Physics σ_e 가 없으면 Physics · Δ = — (+ 사유) · Hertz 값 그대로 (기존 CSV 표 · Pass D 기준 행) {cE}',
            cE is not None and str(cE[1]).startswith('—') and str(cE[2]).startswith('—') and str(cE[0]) not in ('', '—'))
        st_rows = [r for k, r in v_new.items() if 'network state' in k or k.startswith('σ_ionic 망 상태')]
        ho_rows = [r for k, r in v_new.items() if k.startswith('tau2 handover status') or k.startswith('tau2 인계 상태')]
        chk('⑤i3 상태 행 — 망 상태 Physics = 미계산 · FULL 모형 한계 (기술 실패 아님) · τ 인계 상태 Physics = NOT_COMPUTED (full_over_conduction) — 모형 한계 (기술적 실패 문구 아님)',
            bool(st_rows) and '모형 한계' in str(st_rows[0][2]) and bool(ho_rows) and '모형 한계' in str(ho_rows[0][2])
            and '기술적 실패' not in str(ho_rows[0][2]) and ML in str(ho_rows[0][2]), repr((st_rows[:1], ho_rows[:1]))[:400])
        #  원 결과 — Codex 합성 metrics 그대로 (판정문 §2 L214-03 표 · probes/consumer_contracts.py 의 입력 — 실행하지 않고 값만 옮겼다)
        mx = {'sigma_full_mScm': 0.6, 'sigma_full_mScm_physics': None, 'sigma_full_status': 'computed', 'sigma_full_status_physics': 'not_computed',
              'sigma_full_reason_physics': ML, 'network_solver_status': 'success', 'sigma_ratio': 0.4, 'phi_se': 0.5, 'sigma_bulk_net_mScm': 1.0,
              'electronic_sigma_full_mScm': 2.0, 'electronic_sigma_full_mScm_physics': None}
        bad_x = {}
        for tag, tbl in (('새 표', {'network_summary': {'data': []}}),
                         ('기존 표', {'network_summary': {'data': [['── Network Solver (old CSV) ──', '', '', '']]}})):
            app.transform_network_summary_4col(tbl, dict(mx), {})
            rx = _rows_of(tbl)
            for lab in (('σ_ionic (mS/cm)', 'σ_brug / σ_ionic', 'σ_electronic (mS/cm)') if tag == '새 표' else ('σ_brug / σ_ionic',)):
                r = rx.get(lab)
                if r is None or not (str(r[2]).startswith('—') and str(r[3]).startswith('—')) or r[3] == '0%':
                    bad_x[(tag, lab)] = r
        chk(f'⑤j ★ 원 결과 (Codex 합성 metrics — Hertz 0.6 · Physics None · full_over_conduction · 전자 2.0 / None) — transform 의 새 표 · 기존 표 어디에도 '
            f'Physics = Hertz 복사 · Δ 0 % 가 없다 (옛: 0.6 · 2.0× · 2.0 · 0 %) {bad_x}', not bad_x)
        import ast
        src = open(os.path.join(str(HERE), 'app.py'), encoding='utf-8').read()
        tree = ast.parse(src)
        users = sorted(n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)
                       and any(isinstance(c, ast.Call) and getattr(c.func, 'id', None) == '_load_case_tables' for c in ast.walk(n)))
        chk(f'⑤k 실제 화면 경로 — 케이스 (single) · 보고서 (serve_report) · 보관함 (archive_view) 라우트가 같은 _load_case_tables 를 부른다 {users}',
            {'single', 'serve_report', 'archive_view'} <= set(users))
    finally:
        for v in runs.values():
            shutil.rmtree(v[0], ignore_errors=True)
        for d_ in extra:
            shutil.rmtree(d_, ignore_errors=True)


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

        try:                                                              # ⑤ L214 — 한 묶음이 예외로 죽어도 위 결과는 남긴다 (옛 코드 = 그 묶음 FAIL)
            _l214_chain(app, tf, LWB, LDD, tdir, st0, flat, rows, hv, un, percp, tcols)
        except Exception as e:                                            # noqa: BLE001
            import traceback
            traceback.print_exc()
            chk(f'⑤ L214 — 예외 없이 끝난다 ({type(e).__name__}: {e})', False)
    finally:
        shutil.rmtree(tdir, ignore_errors=True)
        for v in runs.values():
            shutil.rmtree(v[0], ignore_errors=True)

    print(f'\ntest_network_handover_chain: {PASS}/{PASS + FAIL} PASS')
    return 0 if FAIL == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
