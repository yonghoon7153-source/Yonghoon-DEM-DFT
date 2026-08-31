#!/usr/bin/env python3
"""STEP B 판정기 — σ_ion 비가 `r = σ_ion(SDCP)/σ_ion(SE)` 에 얼마나 의존하는가.

사전등록: `docs/reviews/ion_r_sensitivity_prereg_20260831.md` §4 (**런 전 커밋**).
이 파일은 그 문턱을 **바꾸지 않는다** — 읽기만 한다.

    R(r) = σ_ion_eff(DBE) / σ_ion_eff(SBE)      (같은 침대·같은 origin, arm 0 쌍대응)
    W    = (max R − min R) / mean R             ← 시나리오 폭.  ⚠ 불확실성이 아니다.

    h1  세 R 이 같은 부호 ∧ W ≤ 0.10   → 비식별성이 비로 전파되지 않는다
    h0  W ≥ 0.30 ∨ 부호가 갈림          → Fig 4b 전자 전용 (Codex ⓑ 확정)
    —   그 사이                          → INDETERMINATE

★ 자기 신고를 읽지 않는다 (규율 §7-4).  payload 가 적어 둔 비·이득을 쓰지 않고
  `sigma_ion_eff_S_cm` **원자료 두 개에서 매번 다시 나눈다**.

★ fail-closed 셋:
  ① 이온 미수렴 팔이 하나라도 있으면 HOLD (`ion_cg_info ≠ 0` · `ion_unconverged`)
  ② `sigma_ion_eff_S_cm` 이 없으면 HOLD — LEAN=2 는 이온을 아예 안 푼다
  ③ **등록 밖 축이 시나리오 사이에서 움직이면 HOLD** — 이 런의 유일한 자유축은
     `sigma_ion_sdcp` 하나다.  vox·스탬프·bridge·PTFE·origin·σ_ion(SE) 는 고정.

사용:
    python3 scripts/ion_r_verdict.py DIR_MG DIR_RSA DIR_PROD
    python3 scripts/ion_r_verdict.py --selftest
"""
import argparse
import glob
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_contract as _RC                                        # noqa: E402

#  ── 사전등록 §4 문턱 — **동결**.  이 파일은 이것을 바꾸지 않는다. ──
H1_W_MAX = 0.10
H0_W_MIN = 0.30

#  ── 축 회계 (규칙 M 의 정신: 후보를 고르는 코드가 곧 사각지대다) ──
#  ① 두 침대 사이에서도, 시나리오 사이에서도 **같아야** 하는 규약 축.
SHARED_AXES = ('vox_um', 'bridge_um', 'sdcp_bridge_um', 'ptfe_block_um',
               'sdcp_stamp', 'sdcp_sphere_d_um', 'sdcp_yield_to_vgcf',
               'ptfe_stamp', 'fibre_stamp', 'periodic_xy', 'plate_rule',
               'sigma_vgcf_S_cm', 'sigma_sdcp_S_cm',
               #  ★ 2026-08-31 (Codex R17 P1-2) — **결론을 바꾸는데 빠져 있던 다섯.**
               #    이들을 시나리오 사이에서 흔들어도 판정이 통과했다 (실측).
               'swcnt_ion_block', 'ptfe_block_scope', 'dilate_z', 'se_source', 'temp_c')

#  ★★ 2026-08-31 (Codex R17 P1-2) — **"서로 같다" 로는 부족하다.**
#    초판은 축이 시나리오 사이에서 일치하는지만 봤다.  그래서 전 시나리오에서 vox 0.125 ·
#    bridge 0.01 · origin (0.0625)³ · ptfe_stamp off · σ_SE 0.003 을 **함께** 바꾼 mutant 가
#    h1 로 통과했다 — "등록한 그 실험" 이라는 전제가 자동으로 증명되지 않았다.
#    ⇒ 사전등록이 고정한 값을 여기 박고 **정확히 그 값인지** 대조한다.
#  ⚠ 이 표를 고치는 것은 사전등록을 고치는 것이다.
PINNED_AXES = {
    'vox_um': 0.15,
    'bridge_um': 0.48,
    'sdcp_stamp': 'sphere',
    'sdcp_sphere_d_um': 0.30,
    'sdcp_yield_to_vgcf': False,
    'ptfe_stamp': 'centerline',
    'fibre_stamp': 'segment',
    'periodic_xy': False,
    'sigma_vgcf_S_cm': 78.5398,
    'sigma_sdcp_S_cm': 250.0,
    'origin_shift_um': (0.0, 0.0, 0.0),          # arm 0 (prereg §3)
}
PINNED_RTOL = 1e-9
#  ② **같은 침대끼리** 시나리오 사이에서 같아야 하는 축 (침대가 안 바뀌었다는 증거).
#     ⚠ 두 침대 사이에서는 당연히 다르다 — 그래서 ① 과 분리한다.
PER_BED_AXES = ('input_digest',)
#  ③ **코드가 안 바뀌었다는 증거.**  ⚠ 2026-08-31 실사고: 런 도중에 러너 워크트리를
#     체크아웃해 `code_sha` 가 시나리오 1 과 2·3 사이에서 갈렸다.  그때 바뀐 것은
#     argparse 도움말 문자열뿐이라 수치는 무관했지만, **그 판단은 사람이 사후에 한
#     것이고 검사에는 없었다.**  "무해했다" 와 "검사가 봤다" 는 다르다.
#     ⇒ 기본은 HOLD, 넘기려면 `--accept-code-drift 사유` 로 **사유를 남겨야** 한다.
CODE_AXES = ('code_sha',)
#  ③ 시나리오 사이에서 **달라야** 하는 축 (등록된 유일한 자유축).
SWEPT_AXIS = 'sigma_ion_sdcp_S_cm'
#  ★★ 2026-08-31 (Codex R16 P1-1) — **등록된 시나리오 집합을 정확히 요구한다.**
#    초판은 `len(scen) >= 2` 만 봤다.  같은 원자료에서 ['MG','RSA'] 두 팔만 넘기면
#    W = 0.01712 · 부호 같음 → **h1 로 뒤집힌다** (실측 재현).  즉 판정이 **호출자가 무엇을
#    넘기느냐**에 달려 있었다 = 규율 ⑤("후보를 고르는 코드가 곧 사각지대다")의 정확한 사례를
#    그 규율을 아는 채로 다시 저질렀다.  ⇒ σ_ion(SDCP) 값 집합을 여기 못 박고, 하나라도
#    빠지거나 더 들어오면 HOLD.  ⚠ 이 집합을 바꾸는 것은 사전등록을 바꾸는 것이다.
REGISTERED_SCENARIOS = {          # 이름 → σ_ion(SDCP) S/cm  (prereg §3, σ_ion(SE)=0.00357)
    'MG':   6.5688e-05,           # r = 0.018400  Maxwell–Garnett 역산
    'RSA':  6.20109e-04,          # r = 0.173700  RSA-RVE 역산
    'PROD': 1.19e-03,             # r = 0.333333  생산 규약
}
SCENARIO_RTOL = 1e-9
#  ④ σ_SE 는 전 시나리오 동일해야 한다 (prereg §3).  ref = 등록값, applied = T-스케일 후.
SE_AXIS = 'sigma_ion_se_ref_S_cm'
SE_APPLIED_AXIS = 'sigma_ion_se_S_cm'


def _step3(j):
    return j.get('step3') or (j.get('mpm_metrics') or {}).get('step3') or {}


def read_arm(path):
    """payload 하나 → dict.  σ_ion 은 **원자료 키에서만** 읽는다."""
    j = json.load(open(path, encoding='utf-8'))
    s = _step3(j)
    m = s.get('manifest') or {}
    name = os.path.basename(path)

    sig = s.get('sigma_ion_eff_S_cm')
    if sig is None:
        raise SystemExit(f'HOLD — {name} 에 sigma_ion_eff_S_cm 이 없다 '
                         '(LEAN=2 는 이온을 안 푼다 — LEAN=3 으로 다시 돌릴 것)')
    #  ①-a σ 값 자체가 물리적으로 유효한가.  ⚠ 2026-08-31 (Codex R17 P1-1) — 초판은
    #     `float(sig)` 만 하고 **음수·NaN·inf 를 그대로 통과**시켰다 (실측: 음수 σ 로
    #     verdict 가 나왔다).  판정기가 물리 검사를 안 하면 아무 숫자나 판정이 된다.
    sig = float(sig)
    if not math.isfinite(sig) or sig <= 0.0:
        raise SystemExit(f'HOLD — {name} 의 sigma_ion_eff_S_cm 이 유한 양수가 아니다: {sig!r}')

    #  ①-b 이온 수렴.  ⚠⚠ 2026-08-31 (Codex R17 P1-1) — 초판은 **자기 검사**를 썼고
    #     그것이 공용 계약보다 약했다: `cg_info = 0.5` 는 `int()` 절삭으로, `resid` 부재와
    #     `1e100` 은 아예 안 봐서, `unconverged = "False"`(문자열)는 `is True` 가 아니라
    #     전부 통과했다.  ⇒ **공용 계약 `run_contract.conv_ok` 를 그대로 부른다.**
    #     같은 계약을 두 곳에 따로 구현한 것 자체가 결함이었다 (작업규율 ① — 이미 있는가).
    ok_conv, why = _RC.conv_ok(s.get('ion_cg_info'), s.get('ion_unconverged'),
                               s.get('ion_resid'))
    if not ok_conv:
        raise SystemExit(
            f'HOLD — {name} 이온 수렴 계약 실패 ({why}) — '
            f'ion_cg_info={s.get("ion_cg_info")!r} · unconverged={s.get("ion_unconverged")!r} · '
            f'resid={s.get("ion_resid")!r}.  (run_contract.conv_ok 와 같은 계약을 쓴다)')

    axes = {k: m.get(k) for k in SHARED_AXES}
    axes['origin_shift_um'] = tuple(m.get('origin_shift_um') or ())
    return {'file': name,
            'bed': 'DBE' if '_DBE_' in name else ('SBE' if '_SBE_' in name else None),
            'sigma_ion': float(sig),
            'swept': m.get(SWEPT_AXIS, s.get(SWEPT_AXIS)),
            'se': m.get(SE_AXIS, s.get(SE_AXIS)),
            'se_applied': m.get(SE_APPLIED_AXIS, s.get(SE_APPLIED_AXIS)),
            'axes': axes,
            'bed_axes': {k: m.get(k) for k in PER_BED_AXES},
            'code_axes': {k: m.get(k) for k in CODE_AXES}}


def read_dir(d):
    """디렉터리 → {'SBE': arm, 'DBE': arm}.  arm 0 한 쌍만 기대한다."""
    if glob.glob(os.path.join(d, '.rejected_*')):
        raise SystemExit(f'HOLD — {d} 에 기각 receipt 가 있다.  판정 대상이 아니다')
    arms = [read_arm(p) for p in sorted(glob.glob(os.path.join(d, 'p2_*.json')))]
    if not arms:
        raise SystemExit(f'HOLD — {d} 에 p2_*.json 이 없다')
    beds = {}
    for a in arms:
        if a['bed'] is None:
            raise SystemExit(f'HOLD — {a["file"]} 의 침대를 파일명에서 못 읽는다')
        if a['bed'] in beds:
            raise SystemExit(f'HOLD — {d} 에 {a["bed"]} 가 둘 이상이다 '
                             '(이 판정은 arm 0 쌍대응 한 쌍만 받는다)')
        beds[a['bed']] = a
    if set(beds) != {'SBE', 'DBE'}:
        raise SystemExit(f'HOLD — {d} 에 침대 한 쪽이 없다 ({sorted(beds)})')
    if beds['SBE']['axes'] != beds['DBE']['axes']:
        diff = [k for k in beds['SBE']['axes']
                if beds['SBE']['axes'][k] != beds['DBE']['axes'][k]]
        raise SystemExit(f'HOLD — {d} 안에서 두 침대의 규약축이 다르다: {diff}')
    #  ⚠ `bed_axes`(input_digest) 는 **여기서 비교하지 않는다** — 두 침대는 원래 다르다.
    #    시나리오 사이에서 같은 침대끼리 비교하는 것이 옳고, 그것은 judge() 가 한다.
    return beds


def judge(scen, accept_code_drift=None):
    """scen = [(name, beds), …] → 판정 dict.  문턱은 동결.

    `beds` = `read_dir()` 의 반환 (`{'SBE': arm, 'DBE': arm}`).  **비는 여기서 나눈다** —
    호출자가 계산해 넘긴 비를 받지 않는다 (자기 신고 금지의 코드 수준 강제).
    """
    #  ⓪ 등록된 시나리오 집합을 **정확히** 받았는가 (부분집합·초과 둘 다 거부).
    got = {nm: bd['SBE']['swept'] for nm, bd in scen}
    if set(got) != set(REGISTERED_SCENARIOS):
        raise SystemExit(
            f'HOLD — 등록된 시나리오 집합이 아니다.  받음 {sorted(got)} · '
            f'등록 {sorted(REGISTERED_SCENARIOS)}\n'
            '  ⚠ 부분집합으로 부르면 같은 원자료가 다른 판정을 낸다 '
            '(MG+RSA 두 팔이면 h1 이 된다).  사전등록 §3 의 셋을 모두 넘길 것.')
    for nm, v in got.items():
        want = REGISTERED_SCENARIOS[nm]
        if v is None or abs(float(v) - want) > SCENARIO_RTOL * max(abs(want), 1e-30):
            raise SystemExit(f'HOLD — 시나리오 {nm} 의 σ_ion(SDCP) 가 등록값과 다르다: '
                             f'{v} vs {want}')
    if len(scen) < 2:
        raise SystemExit('HOLD — 시나리오가 2개 미만이면 폭을 정의할 수 없다')

    #  ③-0 ★ 고정축이 **등록값 그대로**인가 (서로 같은 것으로는 부족하다).
    for nm, bd in scen:
        for bed in ('SBE', 'DBE'):
            ax = dict(bd[bed]['axes'])
            for k, want in PINNED_AXES.items():
                got = ax.get(k)
                if isinstance(want, float):
                    bad = (got is None or isinstance(got, bool)
                           or not isinstance(got, (int, float))
                           or abs(float(got) - want) > PINNED_RTOL * max(abs(want), 1e-30))
                else:
                    bad = (got != want)
                if bad:
                    raise SystemExit(
                        f'HOLD — {nm}/{bed} 의 `{k}` 가 사전등록값과 다르다: {got!r} vs {want!r}.\n'
                        '  ⚠ 시나리오끼리 일치하는 것만으로는 "등록한 그 실험" 이 증명되지 않는다.')

    #  ③-1 규약 축은 **모든 시나리오·양 침대**에서 같아야 한다.
    base = scen[0][1]['SBE']['axes']
    for nm, bd in scen[1:]:
        diff = [k for k in base if base[k] != bd['SBE']['axes'].get(k)]
        if diff:
            raise SystemExit(f'HOLD — 시나리오 사이에서 등록 밖 축이 움직였다 '
                             f'({scen[0][0]} vs {nm}): {diff}')
    #  ③-2 침대가 안 바뀌었는가 — **같은 침대끼리** input_digest 비교.
    for bed in ('SBE', 'DBE'):
        b0 = scen[0][1][bed]['bed_axes']
        for nm, bd in scen[1:]:
            diff = [k for k in b0 if b0[k] != bd[bed]['bed_axes'].get(k)]
            if diff:
                raise SystemExit(f'HOLD — {bed} 침대가 시나리오 사이에서 바뀌었다 '
                                 f'({scen[0][0]} vs {nm}): {diff}')
    #  ③-2b 코드가 안 바뀌었는가.  ⚠ 침대 사이에서도 같아야 한다 — 한 시나리오 안에서
    #      SBE 와 DBE 가 다른 코드로 돌았다면 그 쌍대응 자체가 성립하지 않는다.
    codes = {}
    for nm, bd in scen:
        for bed in ('SBE', 'DBE'):
            for k, v in bd[bed]['code_axes'].items():
                codes.setdefault(k, {}).setdefault(v, []).append(f'{nm}/{bed}')
    drift = {k: v for k, v in codes.items() if len(v) > 1}
    if drift and not accept_code_drift:
        det = '; '.join(f'{k}: ' + ' vs '.join(f'{val!s:.12}…({",".join(w)})'
                                               for val, w in sorted(v.items(), key=str))
                        for k, v in drift.items())
        raise SystemExit(
            f'HOLD — 시나리오 사이에서 코드가 바뀌었다: {det}\n'
            '  런 도중에 러너 워크트리를 체크아웃하면 이렇게 된다.  같은 코드로 다시 돌리거나,\n'
            '  바뀐 것이 수치와 무관함을 확인했다면 --accept-code-drift "사유" 로 사유를 남길 것.')
    if drift:
        print(f'  ⚠ code drift 를 사유와 함께 통과시킨다: {accept_code_drift}')
        for k, v in drift.items():
            for val, w in sorted(v.items(), key=str):
                print(f'      {k} = {val} ← {", ".join(w)}')

    #  ④ σ_SE 고정 — 등록값과 실제 적용값 **둘 다**.
    for key, label in (('se', 'σ_ion(SE) 등록값'), ('se_applied', 'σ_ion(SE) 적용값')):
        vals = {bd[b][key] for _, bd in scen for b in ('SBE', 'DBE')}
        if len(vals) != 1:
            raise SystemExit(f'HOLD — {label} 이 갈렸다: {sorted(vals, key=str)}')
    #  ③-3 등록된 자유축이 **실제로** 달라야 한다 (전부 같으면 스윕이 안 걸린 것).
    sw = [bd['SBE']['swept'] for _, bd in scen]
    if any(v is None for v in sw):
        raise SystemExit('HOLD — payload 가 sigma_ion_sdcp 를 안 싣는다 (fail-closed)')
    for nm, bd in scen:
        if bd['SBE']['swept'] != bd['DBE']['swept']:
            raise SystemExit(f'HOLD — {nm} 의 두 침대가 서로 다른 σ_ion(SDCP) 를 썼다')
    if len(set(sw)) != len(sw):
        raise SystemExit(f'HOLD — sigma_ion_sdcp 가 시나리오 사이에서 안 갈렸다: {sw}')

    R = [bd['DBE']['sigma_ion'] / bd['SBE']['sigma_ion'] for _, bd in scen]
    mean = sum(R) / len(R)
    if mean == 0:
        raise SystemExit('HOLD — 평균 R 이 0 이다')
    W = (max(R) - min(R)) / mean
    same_sign = all(x > 1.0 for x in R) or all(x < 1.0 for x in R)

    if same_sign and W <= H1_W_MAX:
        v = 'h1'
    elif (W >= H0_W_MIN) or (not same_sign):
        v = 'h0'
    else:
        v = 'INDETERMINATE'
    return {'R': R, 'mean': mean, 'W': W, 'same_sign': same_sign, 'verdict': v}


def _report(scen, res):
    print('── σ_ion 비의 r-민감도 (사전등록 §4, 문턱 동결) ──')
    for (nm, bd), R in zip(scen, res['R']):
        sw, se = bd['SBE']['swept'], bd['SBE']['se']
        print(f'  {nm:<6s} σ_ion(SDCP)={sw:.6e}  r={sw / se:.6f}  '
              f'σ_ion_eff SBE={bd["SBE"]["sigma_ion"]:.6e} '
              f'DBE={bd["DBE"]["sigma_ion"]:.6e}  R={R:.6f}')
    print(f'\n  mean R = {res["mean"]:.6f}   W = {res["W"]:.4f}   '
          f'같은 부호 = {res["same_sign"]}')
    print(f'  문턱: h1 ⇔ 같은 부호 ∧ W ≤ {H1_W_MAX} · h0 ⇔ W ≥ {H0_W_MIN} ∨ 부호 갈림')
    print(f'\n  ⇒ 판정 = **{res["verdict"]}**')
    if res['verdict'] == 'h1':
        print('    Fig 4b 에 σ_ion 게재 가능.  ⚠ W 는 "model-form sensitivity scenarios; '
              'not bounds" 로 명기하고, r 을 식별했다고 쓰지 않는다 (prereg §5).')
    elif res['verdict'] == 'h0':
        print('    Fig 4b 전자 전용 (Codex ⓑ 확정).  D13·8팔은 원고에 불필요해진다.')
    else:
        print('    판정 없음.  시나리오를 늘려야 한다 — 문턱은 바꾸지 않는다.')


# ───────────────────────────── selftest ─────────────────────────────
def _man(sdcp, se, bed, **over):
    """실물 매니페스트 키 이름 그대로 만든 픽스처 (이름이 틀리면 검사가 no-op 이 된다)."""
    m = {'vox_um': 0.15, 'bridge_um': 0.48, 'sdcp_bridge_um': 0.0,
         'ptfe_block_um': 0.0, 'sdcp_stamp': 'sphere', 'sdcp_sphere_d_um': 0.30,
         'sdcp_yield_to_vgcf': False, 'ptfe_stamp': 'centerline',
         'fibre_stamp': 'segment', 'periodic_xy': False, 'plate_rule': 'p1',
         'sigma_vgcf_S_cm': 78.5398, 'sigma_sdcp_S_cm': 250.0,
         'swcnt_ion_block': False, 'ptfe_block_scope': 'se', 'dilate_z': 1.0719,
         'se_source': 'se_dump', 'temp_c': 25.0,
         'origin_shift_um': [0, 0, 0],
         'input_digest': f'digest-{bed}', 'code_sha': 'abc123',
         SWEPT_AXIS: sdcp, SE_AXIS: se, SE_APPLIED_AXIS: se}
    m.update(over)
    return m


def _mk(tmp, name, sdcp, se, sig_sbe, sig_dbe, man=None, step3=None, per_bed=None):
    d = os.path.join(tmp, name)
    os.makedirs(d, exist_ok=True)
    for bed, sig in (('SBE', sig_sbe), ('DBE', sig_dbe)):
        m = _man(sdcp, se, bed, **(man or {}))
        m.update((per_bed or {}).get(bed, {}))
        st = {'sigma_ion_eff_S_cm': sig, 'ion_cg_info': 0,
              'ion_unconverged': False, 'ion_resid': 1e-9, 'manifest': m}
        st.update(step3 or {})
        json.dump({'step3': st},
                  open(os.path.join(d, f'p2_{bed}_sph_a0.json'), 'w', encoding='utf-8'))
    return d


def selftest():
    import tempfile
    fails = []

    def chk(msg, cond, extra=''):
        print(('  ok   ' if cond else '  FAIL ') + msg
              + (f'  [{extra}]' if extra and not cond else ''))
        if not cond:
            fails.append(msg)

    def raises(fn, frag):
        try:
            fn()
        except SystemExit as e:
            return frag in str(e), str(e)[:140]
        except Exception as e:                                   # noqa: BLE001
            return False, f'{type(e).__name__}: {e}'
        return False, '예외가 안 났다'

    tmp = tempfile.mkdtemp()
    SE = 0.00357
    MG, RSA, PROD = (REGISTERED_SCENARIOS['MG'], REGISTERED_SCENARIOS['RSA'],
                     REGISTERED_SCENARIOS['PROD'])

    def scen_of(*pairs):
        return [(n, read_dir(d)) for n, d in pairs]

    def full(mg, rsa, prod):
        """등록된 셋을 항상 갖춰 넘긴다 — 이제 judge() 가 그것을 요구한다."""
        return scen_of(('MG', mg), ('RSA', rsa), ('PROD', prod))

    # ① 문턱이 동결값 그대로인가 (사전등록 §4).
    chk('h1 문턱 0.10 · h0 문턱 0.30 동결', (H1_W_MAX, H0_W_MIN) == (0.10, 0.30))
    chk('등록 시나리오 셋이 동결값 그대로',
        REGISTERED_SCENARIOS == {'MG': 6.5688e-05, 'RSA': 6.20109e-04, 'PROD': 1.19e-03})

    #  기준 팔 셋 (h1 형태: 전부 >1, 좁은 폭)
    a = _mk(tmp, 'mg', MG, SE, 1.000, 1.100)
    b = _mk(tmp, 'rsa', RSA, SE, 1.000, 1.120)
    c = _mk(tmp, 'prod', PROD, SE, 1.000, 1.140)

    # ② h1 경로
    r = judge(full(a, b, c))
    chk('h1 — 같은 부호 ∧ 좁은 폭', r['verdict'] == 'h1', f"W={r['W']:.4f}")

    # ③ h0 (a) — 폭이 크다.
    cw = _mk(tmp, 'prod_wide', PROD, SE, 1.000, 1.600)
    jw = judge(full(a, b, cw))
    chk('h0 — 폭이 0.30 이상', jw['verdict'] == 'h0', f"W={jw['W']:.4f}")

    # ④ h0 (b) — **부호가 갈리면 폭이 좁아도 h0** (실제 STEP B 가 이 갈래였다).
    a2 = _mk(tmp, 'mg_flip', MG, SE, 6.585636e-04, 6.455487e-04)
    b2 = _mk(tmp, 'rsa_flip', RSA, SE, 6.585636e-04, 6.566943e-04)
    c2 = _mk(tmp, 'prod_flip', PROD, SE, 6.585636e-04, 6.640011e-04)
    jf = judge(full(a2, b2, c2))
    chk('h0 — 부호가 갈리면 폭이 좁아도 h0 (STEP B 실측 재현)',
        jf['verdict'] == 'h0' and jf['W'] < H0_W_MIN
        and abs(jf['W'] - 0.0281538) < 1e-6, f"W={jf['W']:.7f}")

    # ⑤ INDETERMINATE — 두 문턱 사이.
    cm = _mk(tmp, 'mid', PROD, SE, 1.000, 1.250)
    jm = judge(full(a, b, cm))
    chk('INDETERMINATE — 두 문턱 사이', jm['verdict'] == 'INDETERMINATE', f"W={jm['W']:.4f}")

    # ⑥ 자기 신고를 안 읽는다.
    lie = _mk(tmp, 'lie', MG, SE, 1.0, 1.1,
              step3={'sigma_ion_ratio': 99.0, 'gain_pct': 9900.0})
    bd = read_dir(lie)
    chk('자기 신고 무시 — 원자료에서 다시 나눈다',
        abs(bd['DBE']['sigma_ion'] / bd['SBE']['sigma_ion'] - 1.1) < 1e-12)

    # ── ★★ Codex R16 P1-1 회귀 — **부분집합으로 부르면 판정이 뒤집혔다** ──
    ok, why = raises(lambda: judge(scen_of(('MG', a2), ('RSA', b2))),
                     '등록된 시나리오 집합이 아니다')
    chk('★ 음성 — 부분집합(MG+RSA)은 HOLD (초판은 여기서 h1 을 냈다)', ok, why)
    ok, why = raises(lambda: judge(scen_of(('RSA', b2), ('PROD', c2))),
                     '등록된 시나리오 집합이 아니다')
    chk('★ 음성 — 다른 부분집합(RSA+PROD)도 HOLD', ok, why)
    x4 = _mk(tmp, 'extra', 5.0e-4, SE, 1.0, 1.1)
    ok, why = raises(lambda: judge(scen_of(('MG', a), ('RSA', b), ('PROD', c), ('X', x4))),
                     '등록된 시나리오 집합이 아니다')
    chk('★ 음성 — 등록 밖 시나리오를 더해도 HOLD', ok, why)
    wrong = _mk(tmp, 'wrongval', 7.0e-4, SE, 1.0, 1.1)
    ok, why = raises(lambda: judge(scen_of(('MG', a), ('RSA', b), ('PROD', wrong))),
                     '등록값과 다르다')
    chk('★ 음성 — 이름은 맞는데 σ 값이 등록과 다르면 HOLD', ok, why)

    # ── 음성 경로 (fail-closed) ──
    ok, why = raises(lambda: read_dir(_mk(tmp, 'noion', MG, SE, 1.0, 1.1,
                                          step3={'sigma_ion_eff_S_cm': None})),
                     'sigma_ion_eff_S_cm 이 없다')
    chk('음성 — σ_ion 미기재는 HOLD (LEAN=2 는 이온을 안 푼다)', ok, why)

    ok, why = raises(lambda: read_dir(_mk(tmp, 'unconv', MG, SE, 1.0, 1.1,
                                          step3={'ion_cg_info': 30000,
                                                 'ion_unconverged': True})),
                     '이온 수렴 계약 실패')
    chk('음성 — 이온 미수렴은 HOLD (공용 계약)', ok, why)

    ok, why = raises(lambda: read_dir(_mk(tmp, 'silent', MG, SE, 1.0, 1.1,
                                          step3={'ion_cg_info': None,
                                                 'ion_unconverged': None})),
                     '이온 수렴 계약 실패')
    chk('음성 — 수렴 기록 부재는 통과가 아니라 HOLD (blind)', ok, why)

    #  ★ 규약 축 전수 — 하나씩 흔들어 **전부** 잡히는지 (규율 ⑤).
    probe = {'vox_um': 0.125, 'bridge_um': 0.36, 'sdcp_bridge_um': 0.01,
             'ptfe_block_um': 0.12, 'sdcp_stamp': 'point', 'sdcp_sphere_d_um': 0.0,
             'sdcp_yield_to_vgcf': True, 'ptfe_stamp': 'off',
             'fibre_stamp': 'point', 'periodic_xy': True, 'plate_rule': 'p2',
             'sigma_vgcf_S_cm': 113.097, 'sigma_sdcp_S_cm': 150.0,
             'origin_shift_um': [0.075, 0, 0]}
    missed = []
    for k, v in probe.items():
        d = _mk(tmp, f'ax_{k}', PROD, SE, 1.0, 1.1, man={k: v})
        g1, _ = raises(lambda d=d: judge(full(a, b, d)), '등록 밖 축이 움직였다')
        g2, _ = raises(lambda d=d: judge(full(a, b, d)), '사전등록값과 다르다')
        if not (g1 or g2):           # 둘 중 어느 게이트가 잡아도 정답
            missed.append(k)
    chk(f'음성 — 규약 축 {len(probe)}개가 **전부** 잡힌다', not missed, f'놓친 축: {missed}')

    #  ★ 침대 교체 — input_digest 는 **같은 침대끼리** 비교해야 잡힌다.
    swapped = _mk(tmp, 'bedswap', PROD, SE, 1.0, 1.1,
                  per_bed={'DBE': {'input_digest': 'digest-OTHER'}})
    ok, why = raises(lambda: judge(full(a, b, swapped)),
                     'DBE 침대가 시나리오 사이에서 바뀌었다')
    chk('음성 — 침대가 바뀌면 HOLD', ok, why)
    chk('회귀 — 두 침대 digest 가 다른 것 자체는 통과',
        judge(full(a, b, c))['verdict'] in ('h1', 'h0', 'INDETERMINATE'))

    for key, frag in ((SE_AXIS, 'σ_ion(SE) 등록값'), (SE_APPLIED_AXIS, 'σ_ion(SE) 적용값')):
        d = _mk(tmp, f'se_{key}', PROD, SE, 1.0, 1.1, man={key: 0.003})
        ok, why = raises(lambda d=d: judge(full(a, b, d)), frag)
        chk(f'음성 — {frag} 이 갈리면 HOLD', ok, why)

    half = _mk(tmp, 'half', PROD, SE, 1.0, 1.1, per_bed={'DBE': {SWEPT_AXIS: MG}})
    ok, why = raises(lambda: judge(full(a, b, half)), '서로 다른 σ_ion(SDCP)')
    chk('음성 — 한 침대만 σ 가 바뀌면 HOLD', ok, why)

    d_two = _mk(tmp, 'two', MG, SE, 1.0, 1.1)
    json.dump({'step3': {'sigma_ion_eff_S_cm': 1.0, 'ion_cg_info': 0, 'ion_resid': 1e-9,
                         'ion_unconverged': False, 'manifest': _man(MG, SE, 'SBE')}},
              open(os.path.join(d_two, 'p2_SBE_sph_a1.json'), 'w', encoding='utf-8'))
    ok, why = raises(lambda: read_dir(d_two), 'SBE 가 둘 이상이다')
    chk('음성 — arm 이 둘 이상이면 HOLD (이 판정은 쌍 하나만 받는다)', ok, why)

    d_one = os.path.join(tmp, 'onebed')
    os.makedirs(d_one, exist_ok=True)
    json.dump({'step3': {'sigma_ion_eff_S_cm': 1.0, 'ion_cg_info': 0, 'ion_resid': 1e-9,
                         'ion_unconverged': False, 'manifest': _man(MG, SE, 'SBE')}},
              open(os.path.join(d_one, 'p2_SBE_sph_a0.json'), 'w', encoding='utf-8'))
    ok, why = raises(lambda: read_dir(d_one), '침대 한 쪽이 없다')
    chk('음성 — 침대 한 쪽만 있으면 HOLD', ok, why)

    d_rej = _mk(tmp, 'rej', MG, SE, 1.0, 1.1)
    open(os.path.join(d_rej, '.rejected_x'), 'w').close()
    ok, why = raises(lambda: read_dir(d_rej), '기각 receipt')
    chk('음성 — 기각 receipt 있으면 HOLD', ok, why)

    #  ★ 2026-08-31 실사고 회귀 — 런 도중 워크트리 체크아웃으로 code_sha 가 갈렸다.
    drift = _mk(tmp, 'codedrift', PROD, SE, 1.0, 1.1, man={'code_sha': 'def456'})
    ok, why = raises(lambda: judge(full(a, b, drift)), '코드가 바뀌었다')
    chk('음성 — 시나리오 사이 code_sha 가 갈리면 HOLD', ok, why)
    half_code = _mk(tmp, 'codehalf', PROD, SE, 1.0, 1.1,
                    per_bed={'DBE': {'code_sha': 'def456'}})
    ok, why = raises(lambda: judge(full(a, b, half_code)), '코드가 바뀌었다')
    chk('음성 — 한 시나리오 안에서 침대끼리 코드가 갈려도 HOLD', ok, why)
    jd = judge(full(a, b, drift), accept_code_drift='도움말 문자열만 바뀜')
    chk('사유를 주면 통과한다 (조용한 통과 경로는 없다)',
        jd['verdict'] in ('h1', 'h0', 'INDETERMINATE'))

    # ── ★★ Codex R17 P1-1/P1-2 회귀 — 전부 실측으로 통과했던 mutant 들이다 ──
    #    (초판은 아래 여섯을 **전부** 판정으로 통과시켰고 selftest 는 26/26 초록이었다)
    import math as _m
    for nm, sb, db, st in (
            ('음수 σ_ion',            1.0, -1.1, None),
            ('NaN σ_ion',             1.0, _m.nan, None),
            ('inf σ_ion',             1.0, _m.inf, None),
            ('cg_info = 0.5 (절삭)',   1.0, 1.1, {'ion_cg_info': 0.5}),
            ('resid = 1e100',         1.0, 1.1, {'ion_resid': 1e100}),
            ('unconverged = "False"', 1.0, 1.1, {'ion_unconverged': 'False'}),
            ('resid 부재',             1.0, 1.1, {'ion_resid': None}),
            ('cg_info = True (bool)', 1.0, 1.1, {'ion_cg_info': True}),
    ):
        d = _mk(tmp, f'r17_{abs(hash(nm))%10**6}', PROD, SE, sb, db, step3=st)
        ok, why = raises(lambda d=d: read_dir(d), 'HOLD')
        chk(f'★ 음성(R17) — {nm}', ok, why)

    #  ★ 고정축이 **등록값 그대로**인가 — 시나리오끼리 일치해도 거부해야 한다.
    for k, v in (('vox_um', 0.125), ('bridge_um', 0.01), ('ptfe_stamp', 'off'),
                 ('sdcp_stamp', 'point'), ('origin_shift_um', [0.075, 0.075, 0.075]),
                 ('sigma_vgcf_S_cm', 113.097), ('periodic_xy', True)):
        dd = {kk: _mk(tmp, f'pin{k}{kk}', REGISTERED_SCENARIOS[kk], SE, 1.0, 1.1, man={k: v})
              for kk in REGISTERED_SCENARIOS}
        ok, why = raises(lambda dd=dd: judge([(kk, read_dir(dd[kk]))
                                              for kk in ('MG', 'RSA', 'PROD')]),
                         '사전등록값과 다르다')
        chk(f'★ 음성(R17) — 전 시나리오에서 `{k}` 를 함께 바꿔도 HOLD', ok, why)

    print(f'\n{len(fails)} failure(s)')
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(
        description='STEP B 판정기 — σ_ion 비의 r-민감도 (사전등록 문턱 동결)')
    ap.add_argument('dirs', nargs='*', help='시나리오 OUTDIR (MG RSA PROD 순)')
    ap.add_argument('--names', default='MG,RSA,PROD', help='시나리오 이름 (쉼표)')
    ap.add_argument('--accept-code-drift', metavar='REASON', default=None,
                    help='시나리오 사이에서 code_sha 가 갈린 것을 **사유와 함께** 통과시킨다. '
                         '사유는 보고에 그대로 찍힌다.  기본은 HOLD.')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.dirs:
        ap.error('디렉터리를 주거나 --selftest')
    names = a.names.split(',')
    if len(names) < len(a.dirs):
        names += [f'S{i}' for i in range(len(names), len(a.dirs))]
    scen = [(nm, read_dir(d)) for nm, d in zip(names, a.dirs)]
    res = judge(scen, accept_code_drift=a.accept_code_drift)
    _report(scen, res)
    return 0


if __name__ == '__main__':
    sys.exit(main())
