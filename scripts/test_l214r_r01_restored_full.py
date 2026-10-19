#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L214R-R01 (Codex 표기 L214RR-01) — 보류된 이온 FULL (raw q > 1.5) 를 게시 상태로 되돌린 레코드를 공용 증서 판정이 거부 (시험 먼저).

  python3 scripts/test_l214r_r01_restored_full.py          # 종료코드 0 = 전부 PASS

근거 = Codex 재확인 판정 `docs/reviews/codex_review_lhs214r_fix_recheck_20261017.md` §1 (최소 해결 증거 1–4) · 보충 판정
`docs/reviews/codex_lhs214r_evidence_supplement_20261017.md` §3 (HOLD 이유 = 이 항목) · 수정 계획 `docs/reviews/lhs214rr_fix_plan_20261018.md`
(1저자 10-18 Q1–Q5 권고대로) · 탐침 `docs/reviews/codex_lhs214r_fix_recheck_evidence_20261017/probes/numeric_adversarial.py` ·
`consumer_h0_resurrection.py` (실행하지 않았다 — 같은 편집을 우리 시험으로 옮겼다).

복원 = Codex 탐침의 편집 그대로: 값 둘 (sigma_full = round(q, 8) · sigma_full_mScm = round(q·σ₀·1000, 6)) · 상태 넷 (sigma_full_status computed ·
sigma_full_reason None · ionic_status computed · ionic_status_reason None) · 증서 상태 둘 (status computed · reason None) = 8 leaf.  증서의 전류 · ΔV ·
기하 · 방법 · 채택 시도 · 내부 잔차 · 보존 · 가드 진단 (q_withheld · q_guard_max · guard_policy · sum_g) 은 그대로.  전체 경로는 + 이온 협착 전력 몫과
상태 2 leaf (그 레코드의 열 몫 — Codex 와 같은 출처 · 정지 계약 ④ 가 보는 주 Hertz · Physics 만).

★ 시험 먼저 — 고치기 전 코드 (`60ba39e22` ~ `96b7d5ae9`) 에서 빨갛다: 게시 증서 판정 (`tau_flux._cert_published_problem`) 은 증서 전류 · 기하로 q 를
  재구성해 저장 값과 대조하지만, 이온 FULL 의 그 q 가 생산자 고정 정책 (`network_conductivity.FULL_Q_GUARD_MAX` · 엄격 >) 을 넘는데 게시 상태인지는
  안 본다 → 복원 레코드가 정지 · 다시 읽기 · 인계 · 배포까지 지난다 (Codex §1 표 · 우리 10-18 실측 18 칸 수용).
  R  레코드 단 — test_l214r02 의 12 침대 (띠 L0 · L1 · L2 · 실 생산자) 에서 모형 한계 모드 18 칸 (침대마다 보류된 모드 전부 — H0 · Physics · H12 ×
     L0 · L1 · L2 포함) 을 하나씩 복원: 공용 증서 판정 (`certificate_binding_problems`) 거부 (사유 = 반올림 전 재구성 q · 생산자 정책 이름) · 세대 계약
     invalid · τ 행 그 모드 값 공란 (NOT OK) · 레코드 판정 (`network_record_verdict`) 거부.  변이: 가드 진단 넷을 지움 (자기 신고를 읽지 않는다 —
     같은 판정) · 협착 전력 몫 2 leaf 더함 (Codex 10 leaf)
  E  경계 — 실 생산자 사슬 (면적 0.500000001 · 상자 0.7281737983374794 × box_y) 의 H0 raw q 1.5000000000000002 (생산자 보류) · 1.5 ·
     1.4999999999999998 (게시) — 저장 q 셋 다 1.5 (8 자리): 앞 둘 = 게시 그대로 통과 · 셋째 복원 = 거부.
     ★ 10-19 L214R-S02 (Codex 재확인 2 판정 §2 · 1저자 Q5) — 실 사슬 풀이의 끝자리가 환경마다 다르다 (Codex Windows Py3.12 NumPy 2.5.3 = 등록 입력에서
       17–19 ULP 아래 · 이 컨테이너 = Codex 정확 입력에서 18–19 ULP 위) → box_y 를 등록 입력 (…881 / …882 / …883) 에서 **ULP 한 걸음씩** 옮겨 이 환경에서
       raw q 가 세 경계와 **정확히** 같은 입력을 먼저 찾는다 (E0 · 허용 폭 없음 · 엄격 > 그대로).  못 찾으면 E1–E4 = 전제 불성립 FAIL (KeyError 로 끊기지 않음).
       E′ = 출발 입력을 ±18 ULP 옮겨 (Codex 환경 꼴 · 반대 꼴) 같은 판정이 나오는지 · 복원 helper 는 보류 증서가 아니면 명시 오류.
  E5 Codex 함수 단 (3 노드 증서 · 결합 정보를 붙여 게시 상태로) q 1.4999999999999998 · 1.5 = 통과 · 1.5000000000000002 · 2.0 = 거부 — ★ 10-19 독립 묶음
     (실 사슬 E 의 실패 · 예외와 상관없이 돈다 · 옛 판은 E4 KeyError 뒤라 Codex 환경에서 안 돌았다)
  C  대조 (그대로) — 12 침대 원 레코드 (computed · 적법한 보류) 결합 [] · CF · 협착-only model_over_conduction (q > 1.5 게시 값) 결합 [] · 열 FULL
     (q > 1.5 게시 · 병렬 상한) 채널 판정 ok · 진짜 비관통 (valid_zero) 결합 [] · NOT_PERCOLATING
  B  실 사슬 (9 변이 = 띠 L0 · L1 · L2 의 H0 모형 한계 침대 × 복원 모드 H0 · Physics · H12) — 생산자 CLI → 정지 경로 게시 (L0 = Codex 반례 침대:
     SE 21 노드 · 상자 0.7 · 두께 20) → 게시 폴더를 복원 (dual · 모드 파일 · legacy · full_metrics 투영 · 배치 CSV) → 레코드 판정 · 정지 계약 (⑨) 거부 ·
     case_row 그 모드 NOT OK · 다시 읽기 K2 실패 · load_tau_results 거부 · 실제 배포 빌더 (build_v13 · 다시 읽기 관문 = 이 원천의 실제 다시 읽기) 거부 ·
     배포 관문 셋 각각 독립 (배치 관문 `v13_batch_gate_problems` = check_v13 이 다시 부르는 같은 함수 · 세대 관문 · τ 다시 읽기)
⚠ 범위 — 계약 시험 (작은 합성 사슬 · 상자를 줄인 φ_SE > 1 합성 기하 포함 — 물리 침대 아님 · 발생률 주장 아님).  배포의 나머지 행 · 감사 · 배치 기록은
  `test_lhs_release_v13` 합성 픽스처.  전자 채널 FULL 의 같은 복원 = 이번 범위 밖 (1저자 10-18 Q4 — v1.3 이온 τ 인계가 전자 σ 를 쓰지 않는다).
"""
import contextlib
import copy
import csv
import io
import json
import math
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for _p in (str(HERE), str(ROOT / 'webapp')):
    if _p not in sys.path:
        sys.path.insert(0, _p)

ML = 'full_over_conduction'
MODES = ('hertz', 'physics', 'hertz_h12')
GUARD_KEYS = ('q_withheld', 'q_guard_max', 'guard_policy', 'sum_g')
VALUE_OK = ('OK', 'MODEL_BELOW_CONTINUUM_BOUND')
#: 이온 협착 전력 몫 (정지 계약 ④ 가 보는 주 Hertz · Physics) — (이온 키, 같은 레코드의 열 키 = Codex 와 같은 출처)
POWER_KEY = {'hertz': ('constriction_power_share_ion_hertz', 'constriction_power_share_th_hertz'),
             'physics': ('constriction_power_share_ion_physics', 'constriction_power_share_th_physics')}
#: E 경계 — 실 생산자 사슬 (21 구 · 면적 0.500000001) 의 상자 (x 고정 · y 세 값) → H0 raw q (반올림 전)
E_AREA = 0.500000001
E_BX = 0.7281737983374794
E_BY = {'next': 0.7281737983374881, 'eq': 0.7281737983374882, 'prev': 0.7281737983374883}
E_Q = {'next': math.nextafter(1.5, 2.0), 'eq': 1.5, 'prev': math.nextafter(1.5, 0.0)}
#: ★ 10-19 L214R-S02 — 경계 입력 탐색 상한 (box_y ULP 걸음) · 이식성 시험의 출발 이동 (Codex 환경 = 등록 입력에서 raw q 17–19 ULP 아래)
E_SEARCH_ULP = 512
E_SHIFT_ULP = 18
_ok, _fail = 0, []


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'   {str(extra)[:500]}' if extra else ''))
    return cond


def _guard(label, fn):
    """묶음 하나가 예외로 죽어도 나머지를 센다."""
    try:
        fn()
    except Exception as e:                                       # noqa: BLE001
        import traceback
        traceback.print_exc()
        chk(f'{label} — 예외 없이 끝난다 ({type(e).__name__}: {e})', False)


def quiet(fn, *a, **kw):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*a, **kw)


def _call(fn, *a, **kw):
    """→ (값, '') | (None, '예외 이름: 내용')."""
    try:
        return fn(*a, **kw), ''
    except Exception as e:                                       # noqa: BLE001
        return None, f'{type(e).__name__}: {e}'


def _load(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def _save(p, obj):
    Path(p).write_text(json.dumps(obj, ensure_ascii=False), encoding='utf-8')


def mode_rec(dual, m):
    """dual → 그 모드의 레코드 (주 Hertz · Physics · Hertz 안 H12)."""
    return dual['physics'] if m == 'physics' else (dual['hertzian'] if m == 'hertz' else dual['hertzian']['hertz_h12'])


def restore(rec, m, power=False, drop_guard=False):
    """보류된 FULL → 게시 상태 (Codex 의 8 leaf) — 반환 = 증서의 q_withheld (반올림 전 · 지우기 전).  power = 협착 전력 몫 2 leaf (주 Hertz · Physics) ·
    drop_guard = 증서의 가드 진단 넷 지움."""
    c = rec['solve_certificate_full']
    if 'q_withheld' not in c:          # ★ 10-19 L214R-S02 — 게시된 (보류 아닌) 레코드에 부르면 KeyError 대신 사유 (Codex 환경의 E4 가 여기서 끊겼다)
        raise ValueError('복원 전제 불성립 — 보류 증서가 아니다 (q_withheld 없음 · 생산자가 게시한 레코드)')
    q = c['q_withheld']
    rec.update(sigma_full=round(q, 8), sigma_full_mScm=round(q * rec['sigma_grain_S_cm'] * 1000, 6), sigma_full_status='computed',
               sigma_full_reason=None, ionic_status='computed', ionic_status_reason=None)
    c.update(status='computed', reason=None)
    if isinstance(rec.get('channel_policy_status'), dict):
        rec['channel_policy_status']['ion'] = 'computed'
    if power and m in POWER_KEY:
        ik, tk = POWER_KEY[m]
        rec[ik], rec[ik + '_status'] = rec[tk], 'computed'
    if drop_guard:
        for k in GUARD_KEYS:
            c.pop(k, None)
    return q


def write_record_folder(folder, dual):
    """레코드 판정 · 내용 판정이 읽는 네 사본 (dual · 모드 파일 둘 · legacy = 주 Hertz)."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    _save(folder / 'network_conductivity_dual.json', dual)
    _save(folder / 'network_conductivity_hertzian.json', dual['hertzian'])
    _save(folder / 'network_conductivity_physics.json', dual['physics'])
    _save(folder / 'network_conductivity.json', dual['hertzian'])
    return folder


def restore_folder(cd, m):
    """게시 폴더 복원 — 그 모드의 8 leaf + 전력 몫 2 leaf (Codex consumer_h0_resurrection 과 같은 칸) 를 dual · 모드 파일 · legacy 세 사본에 ·
    full_metrics 의 망 소유 키 = 정지 계약 ⑥b 의 투영 규칙 그대로 (legacy 의 NET_MERGE_KEYS + dual physics 미러 `<키>_physics` + 꼬리 붙은 physics 키)."""
    import pipeline_service as ps
    cd = Path(cd)
    dual = _load(cd / 'network_conductivity_dual.json')
    q = restore(mode_rec(dual, m), m, power=True)
    write_record_folder(cd, dual)
    fm = _load(cd / 'full_metrics.json')
    leg, rP = dual['hertzian'], dual['physics']
    src = {k: leg[k] for k in ps.NET_MERGE_KEYS if leg.get(k) is not None}
    src.update({f'{k}_physics': rP[k] for k in ps.NET_PHYSICS_MIRROR_KEYS if rP.get(k) is not None})
    src.update({k: rP[k] for k in ps.NET_PHYSICS_TAILED_KEYS if rP.get(k) is not None})
    for k in ps.NET_MERGE_KEYS:
        if k in src:
            fm[k] = src[k]
        else:
            fm.pop(k, None)
    _save(cd / 'full_metrics.json', fm)
    return q


def _binding_reject(tf, nc, m, rec):
    """공용 증서 판정 → (거부했나, 사유 문자열) — 거부 = FULL 증서 자리 사유에 생산자 정책 이름이 있다."""
    probs = tf.certificate_binding_problems(m, rec)
    txt = ' | '.join(probs)
    full = [p for p in probs if p.startswith('solve_certificate_full')]
    return bool(full) and any(nc.MODEL_LIMIT_POLICY in p for p in full), txt


# ══ R. 레코드 단 — 모형 한계 모드 18 칸 ═════════════════════════════════════════════════════════════════════════════════════════════
def sec_R(state):
    import network_conductivity as nc
    import tau_flux as tf
    import pipeline_service as ps
    import dem_analysis_core as dac
    from test_l214r02_model_limit_flag import BEDS, bed, produce, ledger
    print('R  레코드 단 — 12 침대 (띠 L0 · L1 · L2) 의 모형 한계 모드 18 칸을 하나씩 게시 상태로 복원 (Codex 8 leaf)')
    duals = {}
    for name in BEDS:
        b = bed(name)
        led, pp = ledger(dac, b)
        duals[name] = (produce(nc, b), led, pp)
    state['R_duals'] = duals
    cells = [(name, m) for name in BEDS for m in BEDS[name][1]]
    bad0 = {}
    for name, m in cells:
        r = mode_rec(duals[name][0], m)
        c = r.get('solve_certificate_full') or {}
        if not (r.get('sigma_full_status') == 'not_computed' and r.get('sigma_full_reason') == ML
                and tf.full_model_limit_problem(r, 'ionic', m) is None and c.get('q_withheld', 0) > nc.FULL_Q_GUARD_MAX):
            bad0[(name, m)] = (r.get('sigma_full_status'), r.get('sigma_full_reason'), c.get('q_withheld'))
    bands = sorted({BEDS[n][0] for n, _m in cells})
    chk(f'R0 대상 = 모형 한계 모드 {len(cells)} 칸 (띠 {bands} × H0 · Physics · H12 포함) — 원 레코드 = 적법한 보류 (not_computed · full_over_conduction · '
        '공용 판정 통과 · 증서 q_withheld > 1.5)', len(cells) == 18 and bands == ['L0', 'L1', 'L2']
        and {m for _n, m in cells} == set(MODES) and not bad0, bad0)
    tmp = Path(tempfile.mkdtemp(prefix='l214rr01_R_'))
    state['tmp'].append(str(tmp))
    acc1, acc2, acc3, acc4, acc5, acc6, qtxt = {}, {}, {}, {}, {}, {}, {}
    for i, (name, m) in enumerate(cells):
        du0, led, pp = duals[name]
        du = copy.deepcopy(du0)
        q = restore(mode_rec(du, m), m)
        rej, txt = _binding_reject(tf, nc, m, mode_rec(du, m))
        if not rej:
            acc1[(name, m)] = txt[:160] or '[] (수용)'
        elif repr(q) not in txt:
            qtxt[(name, m)] = (q, txt[:200])
        con = tf.network_generation_contract(du)
        if not (con.get('generation') == 'invalid' and any(mm == m and kind == 'cert' for mm, kind, _d in con.get('problems') or [])):
            acc2[(name, m)] = (con.get('generation'), [(mm, kind) for mm, kind, _d in con.get('problems') or []])
        row = tf.ion_columns(du, led, pp)
        if row.get(f'ion_net_status_{m}') in VALUE_OK or any(row.get(k) is not None for k in (f'f_ion_{m}', f'tau2_ion_{m}', f'tau_ion_{m}')):
            acc3[(name, m)] = (row.get(f'ion_net_status_{m}'), row.get(f'f_ion_{m}'))
        ok_r, why_r = ps.network_record_verdict(str(write_record_folder(tmp / f'r{i}', du)))
        if ok_r or nc.MODEL_LIMIT_POLICY not in why_r:
            acc4[(name, m)] = (ok_r, why_r[:160])
        dg = copy.deepcopy(du0)
        restore(mode_rec(dg, m), m, drop_guard=True)
        if not _binding_reject(tf, nc, m, mode_rec(dg, m))[0]:
            acc5[(name, m)] = '가드 진단 지움 → 수용'
        dp = copy.deepcopy(du0)
        restore(mode_rec(dp, m), m, power=True)
        if not _binding_reject(tf, nc, m, mode_rec(dp, m))[0]:
            acc6[(name, m)] = '전력 몫 2 leaf 더함 → 수용'
    chk(f'R1 ★ 18 칸 복원 (8 leaf) → 공용 증서 판정 거부 · FULL 증서 자리 사유에 생산자 정책 {nc.MODEL_LIMIT_POLICY!r} (옛: 18/18 수용 = []) — 수용 {len(acc1)}',
        not acc1, acc1)
    chk('R2 ★ 사유의 q = 증서에서 재구성한 반올림 전 q (repr 그대로 — 저장 8 자리 값이 아니다)', not acc1 and not qtxt, qtxt)
    chk('R3 ★ 세대 계약 invalid · 그 모드에 cert 문제 (정지 계약 ⑨ · 다시 읽기 K2 · 인계 · 배포가 부르는 같은 함수)', not acc2, acc2)
    chk('R4 ★ τ 행 (ion_columns) — 복원한 모드 NOT OK · f · T · √T 공란 (옛: L0 = OK · f = 보류 q)', not acc3, acc3)
    chk('R5 ★ 레코드 판정 (network_record_verdict — 네 사본 · 세대 계약) 거부 · 사유에 정책 이름', not acc4, acc4)
    chk('R6 ★ 증서의 가드 진단 넷 (q_withheld · q_guard_max · guard_policy · sum_g) 을 지워도 같은 거부 — 자기 신고를 읽지 않는다', not acc5, acc5)
    chk('R7 ★ 협착 전력 몫 2 leaf 를 더한 복원 (Codex 전체 경로 10 leaf) 도 같은 거부', not acc6, acc6)


# ══ E. 경계 — 반올림 전 q 로만 가를 수 있는 세 수 ═════════════════════════════════════════════════════════════════════════════════════
def _e_raw_q(nc, A, C, plate, bx, by):
    """실 사슬 H0 증서의 반올림 전 q = (I_bottom/ΔV)·T/A (생산자와 같은 산술)."""
    du = quiet(lambda: nc._run_all_networks(A, C, [1], [], {1: 'SE'}, 1, plate, bx, by, None, contact_mode='hertzian'))
    c = du['solve_certificate_full']
    T, Ar, _w = nc._geometry_TA(c['geometry'])
    return (c['I_bottom'] / c['delta_V']) * T / Ar


def find_boundary_inputs(nc, A, C, plate, bx, by0, cap=E_SEARCH_ULP):
    """★ 10-19 L214R-S02 — 이 환경에서 실 사슬 H0 raw q 가 세 경계 (E_Q) 와 **정확히** 같아지는 box_y.  출발 = by0[k] · ULP 한 걸음씩 ·
    q = G·T/(bx·by) 는 by 에 단조 감소라 q < 목표면 by 를 줄이고 > 면 늘린다 · 허용 폭 없이 == 만 (건너뛰면 그 칸 문제).  → ({k: by}, {k: 걸음}, {k: 문제})."""
    found, steps, probs = {}, {}, {}
    for k, tgt in E_Q.items():
        by = by0[k]
        q = _e_raw_q(nc, A, C, plate, bx, by)
        down = q < tgt                                   # q 가 목표 아래 → by 를 줄인다
        n = 0
        while q != tgt and n < cap:
            by = math.nextafter(by, 0.0 if down else math.inf)
            q = _e_raw_q(nc, A, C, plate, bx, by)
            n += 1
            if q != tgt and (q < tgt) != down:
                break                                    # 목표를 건너뛰었다 — 이 걸음에 정확한 값이 없다
        if q == tgt:
            found[k], steps[k] = by, n
        else:
            probs[k] = f'출발 {by0[k]!r} 에서 {n} 걸음 · 마지막 raw q {q!r} ≠ 목표 {tgt!r} (상한 {cap} 또는 건너뜀)'
    return found, steps, probs


def _e_checks(nc, tf, A, C, plate, bx, bys):
    """찾은 입력 → E1–E4 판정 [(이름, 조건, 부가)] (옛 E 와 같은 단언 · 허용 폭 없음)."""
    recs, rows = {}, {}
    for k, by in bys.items():
        du = quiet(lambda: {cm: nc._run_all_networks(A, C, [1], [], {1: 'SE'}, 1, plate, bx, by, None, contact_mode=cm)
                            for cm in ('hertzian', 'physics')})
        du = json.loads(json.dumps(du))
        led = {'thickness_um': plate, 'thickness_mass_conserving_um': plate,
               'phi_se_mass_conserving': sum(4.0 / 3.0 * math.pi * a['radius'] ** 3 for a in A.values()) / (bx * by * plate)}
        recs[k], rows[k] = du, (led, 100.0)
    out = []
    raw = {}
    for k, du in recs.items():
        c = du['hertzian']['solve_certificate_full']
        T, Ar, _w = nc._geometry_TA(c['geometry'])
        raw[k] = (c['I_bottom'] / c['delta_V']) * T / Ar
    out.append((f'E1 실 생산자 H0 증서의 반올림 전 q = 1.5000000000000002 · 1.5 · 1.4999999999999998 (비트 그대로) {raw}',
                all(raw[k] == E_Q[k] for k in E_Q) and recs['next']['hertzian']['solve_certificate_full'].get('q_withheld') == E_Q['next'], ''))
    h = {k: recs[k]['hertzian'] for k in recs}
    pub = {k: (h[k]['sigma_full_status'], h[k]['sigma_full'], tf.certificate_binding_problems('hertz', h[k]),
               tf.ion_columns(recs[k], *rows[k]).get('ion_net_status_hertz')) for k in ('eq', 'prev')}
    out.append((f'E2 q = 1.5 · 1.4999999999999998 → 생산자 게시 (computed · 저장 1.5) · 공용 증서 판정 [] · τ OK — 그대로 (엄격 > · q = 1.5 는 computed) {pub}',
                all(v[0] == 'computed' and v[1] == 1.5 and v[2] == [] and v[3] == 'OK' for v in pub.values()), ''))
    rn = h['next']
    e3 = (rn['sigma_full_status'] == 'not_computed' and rn['sigma_full_reason'] == ML and tf.full_model_limit_problem(rn, 'ionic', 'hertz') is None
          and tf.full_model_limit_flag(rn, 'hertz') is True)
    out.append((f"E3 q = 1.5000000000000002 → 생산자 보류 (not_computed · full_over_conduction · 공용 판정 통과 · 표지 True) "
                f"({rn['sigma_full_status']!r} · {rn['sigma_full_reason']!r})", e3, ''))
    if e3:
        dn = copy.deepcopy(recs['next'])
        restore(dn['hertzian'], 'hertz')
        rej, txt = _binding_reject(tf, nc, 'hertz', dn['hertzian'])
        out.append((f"E4 ★ 그 보류 값을 복원 → 저장 q {dn['hertzian']['sigma_full']!r} = 게시된 두 레코드의 저장 q (8 자리 — 저장 값으로는 못 가른다) · "
                    f"공용 증서 판정 거부 (옛: []) — {txt[:200] or '[]'}",
                    dn['hertzian']['sigma_full'] == 1.5 == h['eq']['sigma_full'] == h['prev']['sigma_full'] and rej, ''))
    else:
        out.append(('E4 전제 불성립 (E3 — 보류 레코드가 없다) — 복원 · 판정하지 않는다', False, ''))
    return out


def sec_E(state):
    import network_conductivity as nc
    import tau_flux as tf
    from test_lhs214_model_limit import chain_bed
    print('E  경계 — 실 생산자 사슬 (box_y = 이 환경의 정확한 경계 입력) 의 H0 raw q 1.5000000000000002 · 1.5 · 1.4999999999999998')
    A, C, plate, _b = chain_bed(1.0, area=E_AREA)
    bys, steps, probs = find_boundary_inputs(nc, A, C, plate, E_BX, E_BY)
    if not chk(f'E0 ★ 전제 (10-19 L214R-S02) — 이 환경에서 세 경계 raw q 를 정확히 내는 box_y 를 등록 입력에서 찾았다 (걸음 {steps} · 상한 {E_SEARCH_ULP} '
               f'· 허용 폭 없음) {bys}', not probs, probs):
        for nm in ('E1', 'E2', 'E3', 'E4'):
            chk(f'{nm} 전제 불성립 (E0 — 이 환경의 경계 입력 없음) — 판정하지 않는다', False)
        return
    for name, cond, extra in _e_checks(nc, tf, A, C, plate, E_BX, bys):
        chk(name, cond, extra)


def sec_E_shift(state):
    """★ 10-19 L214R-S02 이식성 — 이 환경의 정확한 경계 입력 (E0 탐색) 에서 출발을 ±E_SHIFT_ULP 옮겨 (raw q 가 세 경계 모두 아래 = Codex 환경 꼴 ·
    모두 위 = 반대 꼴) 같은 E0–E4 판정.  ⚠ 기준 = 찾은 정확한 입력 (등록 입력이 아니다 — 등록 입력이 이미 어긋난 환경에서도 같은 시험이 되게)."""
    import network_conductivity as nc
    import tau_flux as tf
    from test_lhs214_model_limit import chain_bed
    print(f"E′ 이식성 — 이 환경의 정확한 경계 입력에서 출발 box_y ±{E_SHIFT_ULP} ULP (Codex 환경 꼴 · 반대 꼴) → 탐색이 경계를 다시 찾고 같은 판정")
    A, C, plate, _b = chain_bed(1.0, area=E_AREA)
    base, _st, bprobs = find_boundary_inputs(nc, A, C, plate, E_BX, E_BY)
    if bprobs:
        chk('E′ 전제 불성립 (E0 — 이 환경의 정확한 경계 입력 없음) — 이식성 판정하지 않는다', False, bprobs)
        return
    for sh in (E_SHIFT_ULP, -E_SHIFT_ULP):
        by0 = {}
        for k, v in base.items():
            b = v
            for _ in range(abs(sh)):
                b = math.nextafter(b, math.inf if sh > 0 else 0.0)
            by0[k] = b
        q0 = {k: _e_raw_q(nc, A, C, plate, E_BX, by0[k]) for k in E_Q}
        bys, steps, probs = find_boundary_inputs(nc, A, C, plate, E_BX, by0)
        res = _e_checks(nc, tf, A, C, plate, E_BX, bys) if not probs else []
        bad = [nm[:3] for nm, cond, _x in res if not cond]
        side = '아래' if all(q0[k] < E_Q[k] for k in E_Q) else ('위' if all(q0[k] > E_Q[k] for k in E_Q) else '섞임')
        chk(f'E′{sh:+d} 출발 raw q 가 세 경계의 {side} ({ {k: repr(v) for k, v in q0.items()} }) → 탐색 걸음 {steps} · E1–E4 전부 같은 판정',
            not probs and len(res) == 4 and not bad and side == ('아래' if sh > 0 else '위'), probs or bad)


def sec_E5(state):
    """★ 10-19 독립 묶음 — Codex 함수 단 (3 노드 실제 풀이 증서) 경계 넷.  옛 판은 sec_E 끝이라 실 사슬 E4 예외 뒤에 안 돌았다."""
    import network_conductivity as nc
    import tau_flux as tf
    from test_lhs214_model_limit import net3
    print('E5 경계 — Codex 함수 단 (3 노드 증서 · 결합 정보를 붙여 게시 상태로) · 실 사슬 E 와 독립')
    out = {}
    for lab, pz in (('prev', math.nextafter(0.75, 0.0)), ('eq', 0.75), ('next', math.nextafter(0.75, 1.0)), ('q2', 1.0)):
        n = net3(plate_z=pz)
        quiet(nc.solve_network, n, mode='full')
        cert = copy.deepcopy(n['solve_info']['full'])
        qraw = cert.get('q_withheld') if cert.get('q_withheld') is not None else (cert['I_bottom'] / cert['delta_V']) * pz / 1.0
        cert.update(status='computed', reason=None, channel='ionic', role='H0', contact_mode='hertzian', sigma_bulk_S_cm=.003)
        out[lab] = (qraw, tf._cert_published_problem('hertz', 'full', {'sigma_grain_S_cm': .003}, round(qraw, 8), round(qraw * .003 * 1000, 6),
                                                     'computed', cert))
    chk(f"E5 ★ Codex 함수 단 (3 노드 실제 풀이 증서 · 결합 정보를 붙여 게시 상태로) — q 1.4999999999999998 · 1.5 = None (통과) · 1.5000000000000002 · 2.0 = 사유 "
        f"(옛: 넷 다 None) { {k: (v[0], (v[1] or '')[:60]) for k, v in out.items()} }",
        out['prev'][0] == E_Q['prev'] and out['eq'][0] == 1.5 and out['next'][0] == E_Q['next'] and out['q2'][0] == 2.0
        and out['prev'][1] is None and out['eq'][1] is None
        and all(isinstance(out[k][1], str) and nc.MODEL_LIMIT_POLICY in out[k][1] for k in ('next', 'q2')))


# ══ C. 대조 — 그대로여야 ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
def sec_C(state):
    import network_conductivity as nc
    import tau_flux as tf
    import pipeline_service as ps
    from test_lhs214_model_limit import chain_bed, ledger_of
    print('C  대조 — 원 레코드 (computed · 적법한 보류) · CF · 협착-only 과전도 진단 값 · 열 FULL · 진짜 비관통')
    duals = state.get('R_duals')
    if not duals:
        chk('C — R 의 생산자 레코드가 없다 (R 실패)', False)
        return
    bad1 = {(n, m): tf.certificate_binding_problems(m, mode_rec(du, m)) for n, (du, _l, _p) in duals.items() for m in MODES}
    bad1 = {k: v for k, v in bad1.items() if v}
    chk(f'C1 12 침대 원 레코드 × 세 모드 (computed 18 · 적법한 보류 18) → 공용 증서 판정 [] (그대로)', not bad1, bad1)
    n_moc, bad2 = 0, {}
    for n, (du, _l, _p) in duals.items():
        for m in MODES:
            r = mode_rec(du, m)
            for branch, qk, dk, sk, _rk, ck in tf.CERT_BRANCH_KEYS[1:]:
                if r.get(sk) == 'model_over_conduction':
                    n_moc += 1
                    if not (r.get(qk) is not None and r[qk] > nc.FULL_Q_GUARD_MAX):
                        bad2[(n, m, branch)] = ('q ≤ 1.5 인데 model_over_conduction', r.get(qk))
                    why = tf._cert_published_problem(m, branch, r, r.get(qk), r.get(dk), r.get(sk), r.get(ck))
                    if why is not None:
                        bad2[(n, m, branch)] = why[:160]
    chk(f'C2 CF · 협착-only 의 q > 1.5 게시 진단 값 (model_over_conduction · {n_moc} 가지) → 게시 증서 판정 None (이온 FULL 정책을 진단 가지에 걸지 않는다)',
        n_moc >= 20 and not bad2, bad2)
    th = [(n, m) for n, (du, _l, _p) in duals.items() for m in ('hertz', 'physics')
          if mode_rec(du, m).get('thermal_sigma_full_status') == 'computed' and (mode_rec(du, m).get('thermal_sigma_full') or 0) > nc.FULL_Q_GUARD_MAX]
    bad3 = {k: ps.channel_verdict(mode_rec(duals[k[0]][0], k[1]), 'thermal', k[1]) for k in th}
    bad3 = {k: v for k, v in bad3.items() if v[0] != 'ok'}
    chk(f'C3 열 FULL 의 q > 1.5 게시 값 ({len(th)} 레코드 · 병렬 상한 · 다상 망) → 채널 판정 ok (그대로)', len(th) >= 6 and not bad3, bad3)
    A, C_, plate, box = chain_bed(1.0)
    C_ = [c for c in C_ if c['id1'] != 10]                       # 10–11 접촉 없음 → 관통 경로 없음
    du = quiet(lambda: {cm: nc._run_all_networks(A, C_, [1], [], {1: 'SE'}, 1, plate, box, box, None, contact_mode=cm) for cm in ('hertzian', 'physics')})
    du = json.loads(json.dumps(du))
    st = {m: (mode_rec(du, m).get('sigma_full_status'), tf.certificate_binding_problems(m, mode_rec(du, m))) for m in MODES}
    row = tf.ion_columns(du, ledger_of((A, C_, plate, box)), 0.0)
    chk(f"C4 진짜 비관통 (10–11 접촉 없음) → 세 모드 valid_zero · 공용 증서 판정 [] · τ NOT_PERCOLATING (그대로) {st} · {row.get('ion_net_status_hertz')!r}",
        all(v[0] == 'valid_zero' and v[1] == [] for v in st.values()) and all(row.get(f'ion_net_status_{m}') == 'NOT_PERCOLATING' for m in MODES))


# ══ B. 실 사슬 — 9 변이 (띠 L0 · L1 · L2 × H0 · Physics · H12 복원) ════════════════════════════════════════════════════════════════
def sec_B(state):
    import app
    import pipeline_service as ps
    import tau_flux as tf
    import network_conductivity as nc
    import test_pipeline_provenance as TP
    import test_network_handover_chain as CH
    import lhs_design_dataset as LDD
    import lhs_webapp_batch as LWB
    import lhs_release_build as LRB
    import g2_network_reread as RR
    import logging
    from test_l214r02_model_limit_flag import BEDS, H0_BEDS, bed, _release_helpers
    logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)
    print('B  실 사슬 — 생산자 CLI → 정지 경로 게시 → 게시 폴더 복원 (9 변이) → 레코드 · 정지 · τ · 다시 읽기 · 인계 · 배포')
    orig = TP._bed
    TP._bed = lambda n: bed(n) if n in BEDS else orig(n)
    runs = {}
    try:
        for name in H0_BEDS:
            runs[name] = quiet(CH._run_ml, app, name)
            state['tmp'].append(runs[name][0])
    finally:
        TP._bed = orig
    st = {k: v[1] for k, v in runs.items()}
    chk(f'B0 H0 모형 한계 침대 셋 (L0 = Codex 반례 침대 · L1 · L2) 게시 = done (적법한 보류 그대로) {st}', all(v == 'done' for v in st.values()))
    src = ROOT / 'docs/data/lhs_webapp_contact_d1ec42fba'
    st0 = json.loads((src / 'status.json').read_text(encoding='utf-8'))
    with (src / 'metrics_flat.csv').open(encoding='utf-8', newline='') as fh:
        flat = {r['case']: {k: v for k, v in r.items() if v != ''} for r in csv.DictReader(fh)}
    cands = sorted(c for c, s in st0['cases'].items() if s.get('status') == 'done' and float(flat.get(c, {}).get('percolation_pct') or 0) > 0)
    variants = [(name, m) for name in H0_BEDS for m in MODES]
    mapping = dict(zip(variants, cands))
    tie = tuple(ps.NETWORK_STOP_LEDGER_KEYS) + tuple(LDD.TAU_TIE_EXTRA)
    tcols = list(tf.column_names())
    env = _release_helpers()
    orig_rr = LRB.v13_reread_tau
    res = {k: {} for k in ('rec', 'stop', 'row', 'k2', 'load', 'build', 'gate', 'gen', 'tau')}
    for (name, m), cid in mapping.items():
        key = (name, m)
        work = Path(tempfile.mkdtemp(prefix=f'l214rr01_{name}_{m}_'))
        state['tmp'].append(str(work))
        results = work / 'results'
        results.mkdir()
        d_, s_, f_, rid_ = runs[name]
        cd = results / cid
        shutil.copytree(d_, cd)
        q = restore_folder(cd, m)
        fm = _load(cd / 'full_metrics.json')
        bstate = copy.deepcopy(st0)
        bstate.update(stop_after='network', cases={cid: dict(st0['cases'][cid], stop_after='network', status=s_, failed_stages=f_, network_run_id=rid_)})
        LWB.write_outputs(work / 'batch', bstate, {cid: dict(flat[cid], **{k: fm[k] for k in tie if k in fm})})
        web = LDD.load_webapp(work / 'batch')
        ok_r, why_r = ps.network_record_verdict(str(cd))
        res['rec'][key] = (not ok_r and nc.MODEL_LIMIT_POLICY in why_r, why_r[:160])
        ok_s, why_s = ps.network_stop_verdict(str(cd), rid_)
        other = [t for t in ('①', '②', '③', '④', '⑤', '⑥', '⑧') if t in why_s]
        res['stop'][key] = (not ok_s and '⑨' in why_s and nc.MODEL_LIMIT_POLICY in why_s and not other, (q, other, why_s[:200]))
        row = tf.case_row(str(cd))
        res['row'][key] = (row.get(f'ion_net_status_{m}') not in VALUE_OK and row.get(tf.ROW_GENERATION_COL) == 'invalid'
                           and tf.reason_code(row.get(f'ion_net_status_reason_{m}')) == 'invalid_input'
                           and all(row.get(k) is None for k in (f'f_ion_{m}', f'tau2_ion_{m}', f'tau_ion_{m}')),
                           (row.get(f'ion_net_status_{m}'), tf.reason_code(row.get(f'ion_net_status_reason_{m}')), row.get(tf.ROW_GENERATION_COL),
                            row.get(f'f_ion_{m}')))
        actual = RR.reread_case(cd, 'g2', ps, tf)
        k2 = next((c for c in actual['checks'] if c['name'].startswith('K2')), {})
        k1 = next((c for c in actual['checks'] if c['name'].startswith('K1')), {})
        res['k2'][key] = (k2.get('ok') is False and nc.MODEL_LIMIT_POLICY in k2.get('detail', '') and k1.get('ok') is True,
                          (k1.get('ok'), k2.get('ok'), k2.get('detail', '')[:120]))
        tau, err = _call(LDD.load_tau_results, results, web, expected_generation='g2')
        res['load'][key] = (tau is None and err.startswith('FillRefusal') and cid in err, err[:160] or '인계 통과')
        cells = {c: tf._cell(v) for c, v in row.items() if c in tcols}

        def mutate(ds, head, rows, cid=cid, cells=cells):
            if ds == 'lhs':
                next(r for r in rows if r['case_id'] == cid).update(cells)
        croot = work / 'release'
        handover = quiet(env['make_g2_handover_dir'], str(croot / 'handover'), mutate=mutate)
        batch = quiet(env['make_batch_root'], str(croot / 'batch'))
        gp = Path(batch) / 'reread.json'
        gate_fixture = gp.read_text(encoding='utf-8')
        gate_rec = json.loads(gate_fixture)
        for r in gate_rec['cases']:
            if r['case'] == cid:
                r.update(checks=actual['checks'], statuses=actual['statuses'], row_cells=actual['row_cells'])
        gp.write_text(json.dumps(gate_rec, ensure_ascii=False), encoding='utf-8')
        verdict = croot / 'fixture_verdict.txt'
        verdict.write_text('TEST ONLY — 합성 픽스처 판정문 (배포 승인 아님)\n', encoding='utf-8')

        def rr_adapter(ds, batch_root, rows, expected, cid=cid, results=results, web=web):
            """τ 다시 읽기 — 비교 함수 (v13_reread_tau) 그대로 · 원천 공급만: 선택 행 = 이 복원 원천을 실제 load_tau_results 로 매번 다시 읽음 · 나머지 = 인계표 칸."""
            o_load, o_web = LDD.load_tau_results, LDD.load_webapp

            def provision(*a, **kw):
                cs = {r['case_id']: {'cells': {c: r.get(c, '') for c in tcols}} for r in rows}
                if ds == 'lhs':
                    cs[cid] = o_load(results, web, expected_generation='g2')['cases'][cid]
                return {'schema': LDD.TAU_NET_SCHEMA, 'cases': cs}
            LDD.load_tau_results, LDD.load_webapp = provision, (lambda *a, **kw: {'stop_after': 'network'})
            try:
                return orig_rr(ds, batch_root, rows, expected)
            finally:
                LDD.load_tau_results, LDD.load_webapp = o_load, o_web
        LRB.v13_reread_tau = rr_adapter
        try:
            out = croot / 'out'
            rep, err = _call(quiet, env['build13'], out_dir=str(out), handover_dir=handover, batch_root=batch, date='20991231', codex_verdict=str(verdict))
            res['build'][key] = (rep is None and err.startswith('ReleaseError') and '배치 관문' in err and 'K2' in err and not out.exists(),
                                 err[:200] or f'만들었다 ({(rep or {}).get("n_files")} 파일)')
            gprob = LRB.v13_batch_gate_problems(batch)[1]                 # (기록, 문제 목록)
            res['gate'][key] = (any('K2' in p for p in gprob), [p[:120] for p in gprob][:2])
            hrow = next(r for r in env['_read_csv'](LRB._v13_handover(handover, 'lhs'))[1] if r['case_id'] == cid)
            gen2, gprob2 = LRB.v13_generation_problems([hrow])              # (세대, 문제 목록)
            res['gen'][key] = (gen2 == 'invalid' and any('세대 계약 위반' in p for p in gprob2), (gen2, [p[:120] for p in gprob2][:2]))
            gp.write_text(gate_fixture, encoding='utf-8')                  # 다시 읽기 관문 = 픽스처 그대로 (전부 통과) — τ 다시 읽기만 따로
            hrows = env['_read_csv'](LRB._v13_handover(handover, 'lhs'))[1]
            tprob = LRB.v13_reread_tau('lhs', batch, hrows, 'g2')
            res['tau'][key] = (any('τ 다시 읽기 거부' in p and cid in p for p in tprob), [p[:160] for p in tprob][:2])
        finally:
            LRB.v13_reread_tau = orig_rr
    lab = {'rec': 'B1 ★ 레코드 판정 거부 (세대 계약 · 정책 이름)',
           'stop': 'B2 ★ 정지 계약 거부 = ⑨ (세대 계약 · 증서) · ①–⑥ · ⑧ 은 통과 (복원이 완결 — 옛 코드에서 정지 계약 전부 통과하던 꼴)',
           'row': 'B3 ★ case_row — 행 세대 invalid · 복원한 모드 NOT_COMPUTED invalid_input · f · T · √T 공란 (옛: 세대 g2 · L0 = OK · f = 보류 q · L1/L2 = BAND_FALLBACK + 표지 False)',
           'k2': 'B4 ★ 다시 읽기 (reread_case) — K1 게시 통과 · K2 세대 계약 + 증서 결합 실패 (사유에 정책 이름)',
           'load': 'B5 ★ 인계 원천 관문 (load_tau_results P0–P4) 거부 (FillRefusal · 케이스 이름)',
           'build': 'B6 ★ 실제 배포 빌더 (build_v13 · dry_run False · diagnostic False — 다시 읽기 관문 = 이 원천의 실제 다시 읽기) 거부 = 배치 관문 (다시 읽기 K2) · 산출 폴더 없음 (옛: H0 복원 = 27 파일 · Physics · H12 복원 = H0 보류의 주 타깃 HOLD 로만 거부)',
           'gate': 'B7 ★ 배치 관문 함수 (v13_batch_gate_problems — check_v13 이 다시 부르는 같은 함수) 문제 = 다시 읽기 상세 K2',
           'gen': 'B8 ★ 세대 관문 (v13_generation_problems — 인계 행 = 지금 case_row) 세대 invalid · 세대 계약 위반 (옛: g2 · 문제 0)',
           'tau': 'B9 ★ τ 다시 읽기 (v13_reread_tau — 다시 읽기 관문은 픽스처 그대로 통과 · 원천만 복원) 거부 = load_tau_results FillRefusal 전파'}
    for k, (txt) in lab.items():
        bad = {v: r[1] for v, r in res[k].items() if not r[0]}
        chk(f'{txt} — 9 변이 중 실패 {len(bad)}', len(res[k]) == 9 and not bad, bad)


def main():
    state = {'tmp': []}
    try:
        _guard('R', lambda: sec_R(state))
        _guard('E', lambda: sec_E(state))
        _guard('E′', lambda: sec_E_shift(state))
        _guard('E5', lambda: sec_E5(state))
        _guard('C', lambda: sec_C(state))
        _guard('B', lambda: sec_B(state))
    finally:
        for d in state['tmp']:
            shutil.rmtree(d, ignore_errors=True)
    print(f'\ntest_l214r_r01_restored_full: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
