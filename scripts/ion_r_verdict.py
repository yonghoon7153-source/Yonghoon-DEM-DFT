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
import os
import sys

#  ── 사전등록 §4 문턱 — **동결**.  이 파일은 이것을 바꾸지 않는다. ──
H1_W_MAX = 0.10
H0_W_MIN = 0.30

#  ── 축 회계 (규칙 M 의 정신: 후보를 고르는 코드가 곧 사각지대다) ──
#  ① 두 침대 사이에서도, 시나리오 사이에서도 **같아야** 하는 규약 축.
SHARED_AXES = ('vox_um', 'bridge_um', 'sdcp_bridge_um', 'ptfe_block_um',
               'sdcp_stamp', 'sdcp_sphere_d_um', 'sdcp_yield_to_vgcf',
               'ptfe_stamp', 'fibre_stamp', 'periodic_xy', 'plate_rule',
               'sigma_vgcf_S_cm', 'sigma_sdcp_S_cm')
#  ② **같은 침대끼리** 시나리오 사이에서 같아야 하는 축 (침대가 안 바뀌었다는 증거).
#     ⚠ 두 침대 사이에서는 당연히 다르다 — 그래서 ① 과 분리한다.
PER_BED_AXES = ('input_digest',)
#  ③ 시나리오 사이에서 **달라야** 하는 축 (등록된 유일한 자유축).
SWEPT_AXIS = 'sigma_ion_sdcp_S_cm'
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
    #  ① 이온 수렴.  `None` 은 통과시키지 않는다 — 그 세대 payload 가 안 실은 것이고,
    #     안 실은 것을 "수렴했다" 로 읽는 것이 정확히 CDX-IJ-01 의 실패다.
    ci, un = s.get('ion_cg_info'), s.get('ion_unconverged')
    if ci is None and un is None:
        raise SystemExit(f'HOLD — {name} 이 이온 수렴 기록을 안 싣는다 (fail-closed)')
    if un is True or (ci is not None and int(ci) != 0):
        raise SystemExit(f'HOLD — {name} 이온 미수렴 (ion_cg_info={ci}, unconverged={un})')

    axes = {k: m.get(k) for k in SHARED_AXES}
    axes['origin_shift_um'] = tuple(m.get('origin_shift_um') or ())
    return {'file': name,
            'bed': 'DBE' if '_DBE_' in name else ('SBE' if '_SBE_' in name else None),
            'sigma_ion': float(sig),
            'swept': m.get(SWEPT_AXIS, s.get(SWEPT_AXIS)),
            'se': m.get(SE_AXIS, s.get(SE_AXIS)),
            'se_applied': m.get(SE_APPLIED_AXIS, s.get(SE_APPLIED_AXIS)),
            'axes': axes,
            'bed_axes': {k: m.get(k) for k in PER_BED_AXES}}


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


def judge(scen):
    """scen = [(name, beds), …] → 판정 dict.  문턱은 동결.

    `beds` = `read_dir()` 의 반환 (`{'SBE': arm, 'DBE': arm}`).  **비는 여기서 나눈다** —
    호출자가 계산해 넘긴 비를 받지 않는다 (자기 신고 금지의 코드 수준 강제).
    """
    if len(scen) < 2:
        raise SystemExit('HOLD — 시나리오가 2개 미만이면 폭을 정의할 수 없다')

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
         'origin_shift_um': [0, 0, 0],
         'input_digest': f'digest-{bed}',
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
    MG, RSA, PROD = 6.5688e-05, 6.20109e-04, 1.19e-03

    def scen_of(*pairs):
        return [(n, read_dir(d)) for n, d in pairs]

    # ① 문턱이 동결값 그대로인가 (사전등록 §4).
    chk('h1 문턱 0.10 · h0 문턱 0.30 동결', (H1_W_MAX, H0_W_MIN) == (0.10, 0.30))

    # ② h1 — 세 R 이 전부 >1 이고 폭이 좁다.
    a = _mk(tmp, 'mg', MG, SE, 1.000, 1.100)
    b = _mk(tmp, 'rsa', RSA, SE, 1.000, 1.120)
    c = _mk(tmp, 'prod', PROD, SE, 1.000, 1.140)
    r = judge(scen_of(('MG', a), ('RSA', b), ('PROD', c)))
    chk('h1 — 같은 부호 ∧ 좁은 폭', r['verdict'] == 'h1', f"W={r['W']:.4f}")

    # ③ h0 (a) — 폭이 크다.
    cw = _mk(tmp, 'prod_wide', PROD, SE, 1.000, 1.600)
    jw = judge(scen_of(('MG', a), ('RSA', b), ('PROD', cw)))
    chk('h0 — 폭이 0.30 이상', jw['verdict'] == 'h0', f"W={jw['W']:.4f}")

    # ④ h0 (b) — **부호가 갈리면 폭이 좁아도 h0** (이 갈래가 없으면 h1 이 샌다).
    a2 = _mk(tmp, 'mg_flip', MG, SE, 1.000, 1.010)
    b2 = _mk(tmp, 'rsa_flip', RSA, SE, 1.000, 1.005)
    c2 = _mk(tmp, 'prod_flip', PROD, SE, 1.000, 0.990)
    jf = judge(scen_of(('MG', a2), ('RSA', b2), ('PROD', c2)))
    chk('h0 — 부호가 갈리면 폭이 좁아도 h0',
        jf['verdict'] == 'h0' and jf['W'] < H0_W_MIN, f"W={jf['W']:.4f}")

    # ⑤ INDETERMINATE — 두 문턱 사이.
    cm = _mk(tmp, 'mid', PROD, SE, 1.000, 1.250)
    jm = judge(scen_of(('MG', a), ('RSA', b), ('PROD', cm)))
    chk('INDETERMINATE — 두 문턱 사이', jm['verdict'] == 'INDETERMINATE', f"W={jm['W']:.4f}")

    # ⑥ 자기 신고를 안 읽는다 — payload 가 거짓 비를 실어도 무시한다.
    lie = _mk(tmp, 'lie', MG, SE, 1.0, 1.1,
              step3={'sigma_ion_ratio': 99.0, 'gain_pct': 9900.0})
    bd = read_dir(lie)
    chk('자기 신고 무시 — 원자료에서 다시 나눈다',
        abs(bd['DBE']['sigma_ion'] / bd['SBE']['sigma_ion'] - 1.1) < 1e-12)

    # ── 음성 경로 (fail-closed) ──
    ok, why = raises(lambda: read_dir(_mk(tmp, 'noion', MG, SE, 1.0, 1.1,
                                          step3={'sigma_ion_eff_S_cm': None})),
                     'sigma_ion_eff_S_cm 이 없다')
    chk('음성 — σ_ion 미기재는 HOLD (LEAN=2 는 이온을 안 푼다)', ok, why)

    ok, why = raises(lambda: read_dir(_mk(tmp, 'unconv', MG, SE, 1.0, 1.1,
                                          step3={'ion_cg_info': 30000,
                                                 'ion_unconverged': True})),
                     '이온 미수렴')
    chk('음성 — 이온 미수렴은 HOLD', ok, why)

    ok, why = raises(lambda: read_dir(_mk(tmp, 'silent', MG, SE, 1.0, 1.1,
                                          step3={'ion_cg_info': None,
                                                 'ion_unconverged': None})),
                     '수렴 기록을 안 싣는다')
    chk('음성 — 수렴 기록 부재는 통과가 아니라 HOLD', ok, why)

    #  ★ 규약 축 전수 — 하나씩 흔들어 **전부** 잡히는지 본다 (필터가 사각지대다, 규율 ⑤).
    probe = {'vox_um': 0.125, 'bridge_um': 0.36, 'sdcp_bridge_um': 0.01,
             'ptfe_block_um': 0.12, 'sdcp_stamp': 'point', 'sdcp_sphere_d_um': 0.0,
             'sdcp_yield_to_vgcf': True, 'ptfe_stamp': 'off',
             'fibre_stamp': 'point', 'periodic_xy': True, 'plate_rule': 'p2',
             'sigma_vgcf_S_cm': 113.097, 'sigma_sdcp_S_cm': 150.0,
             'origin_shift_um': [0.075, 0, 0]}
    missed = []
    for k, v in probe.items():
        d = _mk(tmp, f'ax_{k}', PROD, SE, 1.0, 1.1, man={k: v})
        got, _ = raises(lambda d=d: judge(scen_of(('MG', a), ('X', d))),
                        '등록 밖 축이 움직였다')
        if not got:
            missed.append(k)
    chk(f'음성 — 규약 축 {len(probe)}개가 **전부** 잡힌다', not missed, f'놓친 축: {missed}')

    #  ★ 침대 교체 — input_digest 는 **같은 침대끼리** 비교해야 잡힌다.
    swapped = _mk(tmp, 'bedswap', PROD, SE, 1.0, 1.1,
                  per_bed={'DBE': {'input_digest': 'digest-OTHER'}})
    ok, why = raises(lambda: judge(scen_of(('MG', a), ('X', swapped))),
                     'DBE 침대가 시나리오 사이에서 바뀌었다')
    chk('음성 — 침대가 바뀌면 HOLD', ok, why)
    #    ⚠ 회귀 — 두 침대의 digest 가 원래 다른 것을 오탐하면 안 된다.
    chk('회귀 — 두 침대 digest 가 다른 것 자체는 통과',
        judge(scen_of(('MG', a), ('RSA', b)))['verdict'] in ('h1', 'h0', 'INDETERMINATE'))

    for key, frag in ((SE_AXIS, 'σ_ion(SE) 등록값'), (SE_APPLIED_AXIS, 'σ_ion(SE) 적용값')):
        d = _mk(tmp, f'se_{key}', PROD, SE, 1.0, 1.1, man={key: 0.003})
        ok, why = raises(lambda d=d: judge(scen_of(('MG', a), ('X', d))), frag)
        chk(f'음성 — {frag} 이 갈리면 HOLD', ok, why)

    ok, why = raises(lambda: judge(scen_of(('MG', a), ('MG2', _mk(tmp, 'same', MG, SE, 1.0, 1.2)))),
                     '안 갈렸다')
    chk('음성 — 자유축이 실제로 안 갈리면 HOLD', ok, why)

    half = _mk(tmp, 'half', PROD, SE, 1.0, 1.1, per_bed={'DBE': {SWEPT_AXIS: MG}})
    ok, why = raises(lambda: judge(scen_of(('MG', a), ('X', half))),
                     '서로 다른 σ_ion(SDCP)')
    chk('음성 — 한 침대만 σ 가 바뀌면 HOLD', ok, why)

    d_two = _mk(tmp, 'two', MG, SE, 1.0, 1.1)
    json.dump({'step3': {'sigma_ion_eff_S_cm': 1.0, 'ion_cg_info': 0,
                         'ion_unconverged': False, 'manifest': _man(MG, SE, 'SBE')}},
              open(os.path.join(d_two, 'p2_SBE_sph_a1.json'), 'w', encoding='utf-8'))
    ok, why = raises(lambda: read_dir(d_two), 'SBE 가 둘 이상이다')
    chk('음성 — arm 이 둘 이상이면 HOLD (이 판정은 쌍 하나만 받는다)', ok, why)

    d_one = os.path.join(tmp, 'onebed')
    os.makedirs(d_one, exist_ok=True)
    json.dump({'step3': {'sigma_ion_eff_S_cm': 1.0, 'ion_cg_info': 0,
                         'ion_unconverged': False, 'manifest': _man(MG, SE, 'SBE')}},
              open(os.path.join(d_one, 'p2_SBE_sph_a0.json'), 'w', encoding='utf-8'))
    ok, why = raises(lambda: read_dir(d_one), '침대 한 쪽이 없다')
    chk('음성 — 침대 한 쪽만 있으면 HOLD', ok, why)

    d_rej = _mk(tmp, 'rej', MG, SE, 1.0, 1.1)
    open(os.path.join(d_rej, '.rejected_x'), 'w').close()
    ok, why = raises(lambda: read_dir(d_rej), '기각 receipt')
    chk('음성 — 기각 receipt 있으면 HOLD', ok, why)

    ok, why = raises(lambda: judge(scen_of(('MG', a))), '2개 미만')
    chk('음성 — 시나리오 하나면 폭이 정의되지 않는다', ok, why)

    print(f'\n{len(fails)} failure(s)')
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(
        description='STEP B 판정기 — σ_ion 비의 r-민감도 (사전등록 문턱 동결)')
    ap.add_argument('dirs', nargs='*', help='시나리오 OUTDIR (MG RSA PROD 순)')
    ap.add_argument('--names', default='MG,RSA,PROD', help='시나리오 이름 (쉼표)')
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
    res = judge(scen)
    _report(scen, res)
    return 0


if __name__ == '__main__':
    sys.exit(main())
