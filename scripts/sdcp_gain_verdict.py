#!/usr/bin/env python3
"""사전등록 v2 판정기 — `docs/reviews/sdcp_gain_prereg_v2_20260816.md` §5 순서를 **코드로** 박는다.

★ 왜 별도 스크립트인가: 판정선을 사람이 눈으로 보고 적용하면 결과를 본 뒤 창이 움직인다
  (Codex CDX-13 이 지적한 실사고).  판정 순서·문턱을 **런 전에 코드로 고정**해 두면
  결과가 무엇이든 같은 함수가 같은 답을 낸다.

★ 판정 순서 (prereg §5, 여기서 바꾸면 사전등록 위반):
  1. 미수렴 팔(cg_info ≠ 0)이 하나라도 → **판정 보류**
  2. 8 팔 표준오차 > 1.17 %p       → **판정 보류**, origin 16 으로
  3. 비 ≥ 1.05                      → h0 채택
  4. 비 ≤ 1.025                     → h1 채택 ⇒ SDCP 전자 이득 원고에서 철회
  5. 그 사이                        → 둘 다 기각, 제3 기전

사용:
  python3 scripts/sdcp_gain_verdict.py --dir prereg_v2_vox015
  python3 scripts/sdcp_gain_verdict.py --dir ... --collect-only   # 수집만, 판정 안 함
  python3 scripts/sdcp_gain_verdict.py --selftest
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import os
import sys

# ── prereg §3/§4 에서 **런 전에** 고정된 상수.  바꾸면 사전등록이 무효다 ─────────────
H0_MIN_RATIO = 1.05          # h0 (이득은 물리)
H1_RATIO = 1.015             # h1 (SDCP 부피 인공물)
UNDECIDED_LO, UNDECIDED_HI = 1.025, 1.05
SE_MAX_PCT = 1.17            # 이보다 크면 판정 보류하고 origin 을 늘린다
PREREG = 'docs/reviews/sdcp_gain_prereg_v2_20260816.md'

#  ★★ 2026-08-19 (코팅·도핑 코드리뷰 A5) — 세대(generation) 인자.
#  이 필드들은 **매니페스트에 방금 추가된 것**이라 그 이전 payload 에는 없다.  두 극단이 다
#  틀렸다 — "없으면 무시" 로 두면 옛(기본 σ) 팔과 새(도핑) 팔이 섞여도 안 잡히고(= H5 no-op
#  재발), "없으면 HOLD" 로 하면 **진행 중인 스윕이 통째로 멈춘다**(vox 0.125 팔들이 옛 payload).
#  ⇒ 정확한 판정은 **섞이면 HOLD** 다: 한 디렉터리 안에서 어떤 팔은 기록이 있고 어떤 팔은
#  없다면, 그것이 바로 세대가 갈렸다는 신호이므로 비교할 수 없다.
_GEN_FIELDS = ('sigma_ion_se_S_cm', 'sigma_ion_sdcp_S_cm',
               'sigma_am_s_S_cm', 'sigma_am_p_S_cm', 'cam',
               'temp_c', 'ea_ion_ev', 'mpm_seed',
               'se_E_GPa', 'se_nu', 'se_sigma_y_GPa',
               #  ★ fable 리뷰 ② F4 (2026-08-19) — CL-56 축.  SDCP E 23.6 ↔ 9.0 침대가
               #    섞여도 여태 게이트가 못 봤다.  dict 는 그대로 비교된다 (json 왕복 후
               #    같은 dict 면 ==; 다르면 아래 "다르면 HOLD" 가 발화).
               'additive_E_GPa')

#  ⚠ `mpm_seed` 는 **팔마다 달라야 하는 축이 될 수도 있다** (코팅처럼 시딩 자체가 확률적인
#  경우 = seed 앙상블).  현행 origin 앙상블은 같은 압밀 산물을 재사용하므로 seed 가 고정이고,
#  그래서 지금은 고정 인자로 둔다.  seed 앙상블을 돌 때는 prereg 에 그렇게 등록하고
#  `--seed-ensemble` 로 이 하나만 면제한다 (아래 verdict 인자).
_SEED_FIELD = 'mpm_seed'


def _read(path):
    d = json.load(open(path, encoding='utf-8'))
    s = d.get('step3') or (d.get('mpm_metrics') or {}).get('step3') or {}
    man = s.get('manifest') or {}
    return {'file': os.path.basename(path),
            'sigma_e': s.get('sigma_e_eff_S_cm'),
            'sigma_ion': s.get('sigma_ion_eff_S_cm'),
            'n_dof': s.get('n_dof'),
            'cg_info': s.get('cg_info'),
            'cg_resid': s.get('cg_resid'),
            'unconverged': s.get('unconverged'),
            'origin_shift_um': man.get('origin_shift_um'),
            'vox': man.get('vox_um') or s.get('vox_um'),
            'bridge_um': man.get('bridge_um'),
            #  ★ 2026-08-18 (리뷰 ① H5/M1) — 고정 인자를 넓힌다.  `bridge_um` 은 매니페스트에
            #    없어서 게이트가 no-op 이었고(payload 에서 이번에 추가), 스탬프 규약과 재료
            #    계수는 애초에 검사 대상이 아니었다.  `backend` 는 CuPy 실패 시 조용한 CPU
            #    폴백을 잡는다 (step3_sigma._solve_cg 는 print 만 하고 내려간다).
            'sdcp_stamp': man.get('sdcp_stamp'),
            'sdcp_sphere_d_um': man.get('sdcp_sphere_d_um'),
            #  ★ 2026-08-18 (CL-43) — σ-치환 진단 팔.  **없으면 False 로 정규화**한다
            #    (플래그 이전 payload 는 정의상 생산 규약이므로).  None 으로 두면 아래 게이트가
            #    None 을 건너뛰어 진단 팔과 생산 팔이 **섞여도 안 잡힌다** = H5 와 같은 no-op.
            'sdcp_yield_to_vgcf': bool(man.get('sdcp_yield_to_vgcf', False)),
            #  ★ 2026-08-18 (CL-49) — PTFE 스탬프 팔.  같은 정규화 규칙 (없으면 0.0 = 생산).
            'sigma_ptfe_S_cm': float(man.get('sigma_ptfe_S_cm', 0.0) or 0.0),
            'sigma_vgcf_S_cm': man.get('sigma_vgcf_S_cm'),
            'sigma_sdcp_S_cm': man.get('sigma_sdcp_S_cm'),
            #  ★★ 2026-08-19 (코팅·도핑 리뷰 A5) — 도핑 축과 침대 세대.  **정규화하지 않는다**:
            #    `sdcp_yield_to_vgcf`(False)·`sigma_ptfe`(0.0) 는 "플래그 이전 = 정의상 생산 규약"
            #    이라 기본값이 정답이었지만, σ_ion·σ_AM·E_SE·seed 는 옛 payload 가 무슨 값으로
            #    돌았는지 **추정할 수 없다** (--temp-c 로도 움직인다).  None 으로 두고 아래
            #    _GEN_FIELDS 세대-혼합 게이트가 잡는다.
            **{f: man.get(f) for f in _GEN_FIELDS},
            'backend': (man.get('backend_last_solve') or {}).get('backend'),
            'fibre_stamp': man.get('fibre_stamp')}


def collect(d):
    rows = [_read(p) for p in sorted(glob.glob(os.path.join(d, 'p2_*.json')))]
    #  ★ 2026-08-18 (리뷰 ① M1) — 옛 판은 `_SBE_`/`_DBE_` 로만 갈랐다.  구 팔 파일명
    #    `p2_DBE_sph_a0` 도 `_DBE_` 를 포함하므로 점 팔과 구 팔이 **한 디렉터리에 섞이면
    #    조용히 합쳐진다**.  매니페스트의 `sdcp_stamp` 가 정본이므로 그것도 고정 인자에
    #    넣었지만(아래 게이트), 애초에 섞이지 않게 파일명 축도 본다.
    arms = {'SBE': [r for r in rows if '_SBE_' in r['file']],
            'DBE': [r for r in rows if '_DBE_' in r['file']]}
    return rows, arms


def _stats(vals):
    n = len(vals)
    if n == 0:
        return None
    m = sum(vals) / n
    if n == 1:
        return {'n': 1, 'mean': m, 'sd': None, 'se': None}
    sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (n - 1))
    return {'n': n, 'mean': m, 'sd': sd, 'se': sd / math.sqrt(n)}


def verdict(arms, seed_ensemble=False):
    """prereg §5 판정.  **순서를 바꾸지 말 것.**

    `seed_ensemble=True` 는 **`mpm_seed` 하나만** 고정 인자에서 면제한다 (코팅처럼 시딩
    자체가 확률적인 축을 잴 때).  ⚠ prereg 에 그렇게 등록한 경우에만 쓸 것 — 나머지
    인자는 그대로 고정이고, 면제 사실은 판정 출력에 남는다.
    """
    out = {'prereg': PREREG, 'thresholds': {
        'h0_min_ratio': H0_MIN_RATIO, 'h1_ratio': H1_RATIO,
        'undecided': [UNDECIDED_LO, UNDECIDED_HI], 'se_max_pct': SE_MAX_PCT}}
    # ① 미수렴 — 하나라도 있으면 보류.  ★ **fail-closed**: 수렴 정보가 **없어도** 보류한다.
    #   실사고 2026-08-16: `cg_info` 를 안 싣는 payload 를 None 으로 읽고 통과시켰다 =
    #   fail-open.  "확인 못 했다" 와 "확인했고 괜찮다" 는 다르다.
    unconv, unknown = [], []
    for k in arms:
        for r in arms[k]:
            if r.get('unconverged') is True or (r.get('cg_info') not in (0, None)):
                unconv.append(r['file'])
            elif r.get('cg_info') is None and r.get('cg_resid') is None:
                unknown.append(r['file'])
    if unconv:
        return dict(out, decision='HOLD',
                    reason=f'미수렴 팔 {len(unconv)}개 — prereg §5-1 (판정 보류)',
                    unconverged=unconv)
    if unknown:
        return dict(out, decision='HOLD',
                    reason=f'수렴 정보 없는 팔 {len(unknown)}개 — 확인 못 한 것을 통과시키지 '
                           f'않는다 (fail-closed).  payload 가 cg_info/cg_resid 를 싣도록 '
                           f'고치고 다시 돌릴 것',
                    no_convergence_info=unknown)
    # ── 데이터 무결성 게이트 (2026-08-16, 심층 리뷰 ③) ────────────────────────────────
    #   ⚠ 이것은 §5 판정 순서의 **변경이 아니라 전제 집행**이다.  §5 는 "8 팔 factorial" 과
    #     "그 외 모든 인자 고정" 을 stipulate 한다 — 그 전제가 깨진 데이터는 §5 가 말하는
    #     그 데이터가 아니므로 판정 대상이 아니다.  (같은 origin 8 벌은 가짜 정밀도를 낳는다.)
    for k in ('SBE', 'DBE'):
        _sh = [tuple(r['origin_shift_um']) for r in arms[k] if r.get('origin_shift_um')]
        if _sh and len(set(_sh)) != len(_sh):
            return dict(out, decision='HOLD',
                        reason=f'{k} 에 **중복 origin** 이 있다 ({len(_sh) - len(set(_sh))}건) — '
                               f'같은 위상을 여러 번 세면 표준오차가 가짜로 작아진다')
    #  ★★ 2026-08-19 (A5) — 세대 혼합 게이트.  **고정-인자 검사보다 먼저** 돈다: 기록이 있는
    #    팔과 없는 팔이 섞이면 아래 "다르면 HOLD" 는 None 을 건너뛰어 **통과시켜 버리기** 때문이다.
    _gen_ex = {_SEED_FIELD} if seed_ensemble else set()
    if seed_ensemble:
        out['seed_ensemble'] = True          # 면제를 판정 출력에 남긴다 (조용한 완화 금지)
    for fld in _GEN_FIELDS:
        if fld in _gen_ex:
            continue
        _has = [r['file'] for k in ('SBE', 'DBE') for r in arms[k] if r.get(fld) is not None]
        _non = [r['file'] for k in ('SBE', 'DBE') for r in arms[k] if r.get(fld) is None]
        if _has and _non:
            return dict(out, decision='HOLD',
                        reason=f'세대 혼합 — `{fld}` 를 기록한 팔 {len(_has)}개와 기록이 **없는** '
                               f'팔 {len(_non)}개가 한 디렉터리에 있다 ({_non[0]} …).  '
                               f'옛 payload 는 이 인자로 무슨 값을 썼는지 추정할 수 없으므로 '
                               f'(σ_ion 은 --temp-c 로도 움직인다) 비교 불가다.  옛 팔을 다시 돌릴 것')
    for fld in ('vox', 'bridge_um', 'fibre_stamp', 'sdcp_stamp', 'sdcp_sphere_d_um',
                'sigma_vgcf_S_cm', 'sigma_sdcp_S_cm', 'backend', 'sdcp_yield_to_vgcf',
                'sigma_ptfe_S_cm',
                # ★ A5: σ_ion 축(도핑)과 σ_AM·CAM·T — σ_AM 은 σ_e 솔브에 직접 들어가고,
                #   σ_ion 은 도핑 트랙의 **유일한** 노브다.  둘 다 여태 미게이트였다.
                *(f for f in _GEN_FIELDS if f not in _gen_ex)):
        #  ★ F4: dict 값(additive_E_GPa)은 set 에 못 들어간다 — 정규 직렬화로 비교.
        _v = {(json.dumps(r.get(fld), sort_keys=True)
               if isinstance(r.get(fld), (dict, list)) else r.get(fld))
              for k in arms for r in arms[k] if r.get(fld) is not None}
        if len(_v) > 1:
            return dict(out, decision='HOLD',
                        reason=f'고정 인자 `{fld}` 가 팔마다 다르다 ({sorted(map(str, _v))}) — '
                               f'prereg §5 는 그 외 모든 인자 고정을 요구한다')
    #  ★ 그리고 **없는 것**도 잡는다 (리뷰 ① H5): `bridge_um` 이 매니페스트에 없던 시절에는
    #    위 루프가 항상 빈 집합을 봐서 **한 번도 발화하지 않았다** = 가짜 보증.  prereg §5 가
    #    명시적으로 못 박으라고 한 인자가 기록조차 안 됐다면 그것은 통과가 아니라 HOLD 다.
    #    ★★ 2026-08-20 (전수 감사 코드 #2) — 이 목록이 4개뿐이라 **구멍이 6개** 있었다:
    #      `sigma_vgcf_S_cm`·`sigma_sdcp_S_cm`·`sdcp_sphere_d_um`·`backend`·
    #      `sdcp_yield_to_vgcf`·`sigma_ptfe_S_cm` 는 위 고정-인자 루프에는 있지만 (None 은
    #      skip) 여기에도 `_GEN_FIELDS` 에도 없어, **양쪽 침대 8팔이 전부 기록 없는 세대**면
    #      그대로 판정이 났다 (실측: 8팔 전부 None → HOLD 가 아니라 `h0`).  게다가 앞 넷은
    #      `_GEN_FIELDS` 밖이라 **섞여 있어도** 통과했다.  러너 자신이 "옛 팔은 OUTDIR= 로
    #      이어 쓰라" 고 안내하므로 이 경로는 가정이 아니라 권장 시나리오다.
    #      ⇒ 현행 payload 는 이 여섯을 **항상** 기록한다 (`mpm_webapp_payload.py` 매니페스트)
    #        — 없으면 옛 세대이고, 옛 세대는 고정을 확인할 수 없으므로 HOLD 다 (H5 와 같은 논리).
    for fld in ('vox', 'bridge_um', 'fibre_stamp', 'sdcp_stamp',
                'sigma_vgcf_S_cm', 'sigma_sdcp_S_cm', 'sdcp_sphere_d_um',
                'backend', 'sdcp_yield_to_vgcf', 'sigma_ptfe_S_cm'):
        _miss = [r['file'] for k in arms for r in arms[k] if r.get(fld) is None]
        if _miss:
            return dict(out, decision='HOLD',
                        reason=f'고정 인자 `{fld}` 가 매니페스트에 **없는** 팔이 {len(_miss)}개 '
                               f'({_miss[0]} …) — 기록되지 않은 인자는 고정을 확인할 수 없다.  '
                               f'옛 payload 로 돈 팔이면 다시 돌릴 것')
    st = {k: _stats([r['sigma_e'] for r in arms[k] if r['sigma_e']]) for k in ('SBE', 'DBE')}
    out['arms'] = st
    if not st['SBE'] or not st['DBE'] or st['SBE']['n'] != st['DBE']['n']:
        return dict(out, decision='HOLD',
                    reason=f'팔 수 불일치/부족 (SBE {st["SBE"] and st["SBE"]["n"]} · '
                           f'DBE {st["DBE"] and st["DBE"]["n"]}) — 판정 불가')
    ratio = st['DBE']['mean'] / st['SBE']['mean']
    out['ratio'] = round(ratio, 6)
    # ② 표준오차 게이트
    if st['SBE']['se'] is None:
        return dict(out, decision='HOLD', reason='팔이 1 개 — 표준오차를 못 낸다')
    se_ratio_pct = 100.0 * math.hypot(st['SBE']['se'] / st['SBE']['mean'],
                                      st['DBE']['se'] / st['DBE']['mean'])
    out['se_ratio_pct'] = round(se_ratio_pct, 4)
    #  ── 보조 통계: **쌍대응** SE (심층 리뷰 ③④) ───────────────────────────────────────
    #    팔은 origin 으로 쌍이 맞고 두 침대가 강한 공통모드를 갖는다 (실측 r = +0.963).
    #    위 hypot 은 두 팔을 독립으로 보므로 비의 SE 를 **5.1 배 과대**평가한다 (보수 방향).
    #    ⚠ **게이트는 그대로 hypot 을 쓴다** — 그것이 런 전에 커밋된 조작적 정의다 (prereg §4).
    #      쌍별 값은 **보조 출력**일 뿐이고, 게이트 승격은 v3 prereg 에서 등록한다.
    _pa = [d['sigma_e'] / s['sigma_e']
           for s, d in zip(sorted(arms['SBE'], key=lambda r: r['file']),
                           sorted(arms['DBE'], key=lambda r: r['file']))
           if s.get('sigma_e') and d.get('sigma_e')]
    if len(_pa) > 1:
        _m = sum(_pa) / len(_pa)
        _sd = math.sqrt(sum((v - _m) ** 2 for v in _pa) / (len(_pa) - 1))
        out['ratio_paired_mean'] = round(_m, 6)
        out['se_ratio_paired_pct'] = round(100.0 * _sd / math.sqrt(len(_pa)) / _m, 4)
        out['ratio_arms'] = [round(v, 6) for v in _pa]
        out['se_note'] = ('게이트는 prereg §4 의 hypot 을 쓴다 (보수적).  쌍별 SE 는 참고용 — '
                          '점예측 일치 서술에 쓰지 말 것')
    if se_ratio_pct > SE_MAX_PCT:
        return dict(out, decision='HOLD',
                    reason=f'비의 표준오차 {se_ratio_pct:.2f} %p > {SE_MAX_PCT} — '
                           f'prereg §5-2 (origin 16 으로 늘릴 것)')
    # ③④⑤ 본 판정
    if ratio >= H0_MIN_RATIO:
        return dict(out, decision='h0', reason=f'비 {ratio:.4f} ≥ {H0_MIN_RATIO} — 이득은 물리')
    if ratio <= UNDECIDED_LO:
        return dict(out, decision='h1',
                    reason=f'비 {ratio:.4f} ≤ {UNDECIDED_LO} — SDCP 부피 인공물.  '
                           f'⇒ **원고에서 SDCP 전자 이득 철회**')
    return dict(out, decision='BOTH_REJECTED',
                reason=f'비 {ratio:.4f} 가 중간대 ({UNDECIDED_LO}, {UNDECIDED_HI}) — '
                       f'둘 다 기각, 제3 기전 조사 (prereg §5-5)')


def _selftest():
    ok, fail = 0, []

    def chk(n, c):
        nonlocal ok
        (ok := ok + 1) if c else fail.append(n)
        print(('  PASS  ' if c else '  FAIL  ') + n)

    #  ★ 픽스처는 **실제 매니페스트가 싣는 필드를 전부** 가져야 한다 (2026-08-18, 리뷰 ① H5).
    #    옛 픽스처는 고정-인자 필드를 아예 안 실었고, 그래서 그 게이트가 픽스처에서
    #    검증된 적이 없었다 — 프로덕션에서 `bridge_um` 이 no-op 이었던 것과 같은 뿌리다.
    _FIX = dict(vox=0.15, bridge_um=0.48, fibre_stamp='segment', sdcp_stamp='point',
                sdcp_sphere_d_um=0.0, sigma_vgcf_S_cm=78.5398, sigma_sdcp_S_cm=250.0,
                backend='gpu', sdcp_yield_to_vgcf=False, sigma_ptfe_S_cm=0.0,
                # ★ 2026-08-19 (A5) — 세대 인자도 픽스처에 싣는다.  안 실으면 위와 같은
                #   이유로 새 게이트가 selftest 에서 **검증된 적 없는 코드**가 된다.
                additive_E_GPa={'VGCF': 10.0, 'PTFE': 0.3, 'SDCP': 23.6},
                sigma_ion_se_S_cm=0.003, sigma_ion_sdcp_S_cm=0.001,
                sigma_am_s_S_cm=0.010, sigma_am_p_S_cm=0.005, cam='nmc811',
                temp_c=25.0, ea_ion_ev=0.29, mpm_seed=3,
                se_E_GPa=1.53, se_nu=0.49, se_sigma_y_GPa=0.30)

    def mk(sbe, dbe, cg=0, resid=1e-8, **over):
        f = dict(_FIX, **over)
        return {'SBE': [dict(f, file=f'p2_SBE_a{i}.json', sigma_e=v, cg_info=cg,
                             cg_resid=resid, unconverged=False)
                        for i, v in enumerate(sbe)],
                'DBE': [dict(f, file=f'p2_DBE_a{i}.json', sigma_e=v, cg_info=cg,
                             cg_resid=resid, unconverged=False)
                        for i, v in enumerate(dbe)]}

    base = [1.0000, 1.0020, 0.9980, 1.0010, 0.9990, 1.0005, 0.9995, 1.0000]
    chk('① 미수렴이 하나라도 있으면 HOLD (숫자를 내지 않는다)',
        verdict(mk(base, base, cg=1))['decision'] == 'HOLD')
    chk('② 비 1.08 → h0', verdict(mk(base, [v * 1.08 for v in base]))['decision'] == 'h0')
    v1 = verdict(mk(base, [v * 1.015 for v in base]))
    chk(f'③ 비 1.015 → h1 ({v1["ratio"]})', v1['decision'] == 'h1')
    chk('④ 비 1.035 (중간대) → 둘 다 기각',
        verdict(mk(base, [v * 1.035 for v in base]))['decision'] == 'BOTH_REJECTED')
    noisy = [1.0, 1.10, 0.90, 1.08, 0.92, 1.06, 0.94, 1.0]      # SE 큼
    chk('⑤ 표준오차가 크면 판정 보류 (origin 을 늘리라고 말한다)',
        verdict(mk(noisy, [v * 1.08 for v in noisy]))['decision'] == 'HOLD')
    chk('⑥ 팔 수가 다르면 HOLD',
        verdict(mk(base, base[:4]))['decision'] == 'HOLD')
    #  ★ fail-closed — 수렴 정보가 **없으면** 통과시키지 않는다 (실사고 2026-08-16)
    blind = {'SBE': [{'file': 'x', 'sigma_e': 1.0, 'cg_info': None, 'cg_resid': None}] * 8,
             'DBE': [{'file': 'y', 'sigma_e': 1.08, 'cg_info': None, 'cg_resid': None}] * 8}
    vb = verdict(blind)
    chk(f'⑧ ★ 수렴 정보 없는 팔은 HOLD (옛 판은 통과시켰다): {vb["decision"]}',
        vb['decision'] == 'HOLD' and 'no_convergence_info' in vb)
    chk('⑦ 문턱이 prereg 값과 같다 (코드가 사전등록이다)',
        (H0_MIN_RATIO, H1_RATIO, SE_MAX_PCT) == (1.05, 1.015, 1.17))
    #  ★★ 2026-08-18 (리뷰 ① H5) — 고정-인자 게이트의 **회귀**.  프로덕션에서 `bridge_um`
    #    이 매니페스트에 없어 이 게이트가 한 번도 발화하지 않았는데, 옛 픽스처가 그 필드를
    #    아예 안 실어 selftest 도 그 사실을 못 봤다.  두 방향을 다 건다.
    _mix = mk(base, [v * 1.08 for v in base])
    _mix['DBE'][3]['bridge_um'] = 0.30                       # 한 팔만 다른 브리지
    v9 = verdict(_mix)
    chk(f'⑨ 고정 인자가 팔마다 다르면 HOLD ({v9["decision"]})',
        v9['decision'] == 'HOLD' and 'bridge_um' in (v9.get('reason') or ''))
    _drop = mk(base, [v * 1.08 for v in base])
    for _r in _drop['SBE'] + _drop['DBE']:
        _r['bridge_um'] = None                               # 옛 payload = 기록 자체가 없음
    v10 = verdict(_drop)
    chk(f'⑩ ★ 고정 인자가 매니페스트에 **없으면** HOLD (가짜 보증 재발 방지): {v10["decision"]}',
        v10['decision'] == 'HOLD' and 'bridge_um' in (v10.get('reason') or ''))
    #  ⑪ 점 팔과 구 팔이 한 디렉터리에 섞이면 잡는다 (리뷰 ① M1)
    _mix2 = mk(base, [v * 1.08 for v in base])
    for _r in _mix2['DBE']:
        _r['sdcp_stamp'], _r['sdcp_sphere_d_um'] = 'sphere', 0.30
    v11 = verdict(_mix2)
    chk(f'⑪ 점 팔 × 구 팔 혼합은 HOLD ({v11["decision"]})',
        v11['decision'] == 'HOLD' and 'sdcp_stamp' in (v11.get('reason') or ''))
    #  ⑫ σ-치환 진단 팔(CL-43)이 생산 팔과 섞이면 잡는다 — **DBE 만** 켠 것이 전형적 실수다
    _mix3 = mk(base, [v * 1.08 for v in base])
    for _r in _mix3['DBE']:
        _r['sdcp_yield_to_vgcf'] = True
    v12 = verdict(_mix3)
    chk(f'⑫ σ-치환 진단 팔 × 생산 팔 혼합은 HOLD ({v12["decision"]})',
        v12['decision'] == 'HOLD' and 'sdcp_yield_to_vgcf' in (v12.get('reason') or ''))
    #  ⑬ ★ 정규화 회귀 — 옛 payload 는 이 필드가 **없다**.  없음을 None 으로 두면 위 게이트가
    #     건너뛰어 ⑫ 가 통과해 버린다.  없음 → False 로 읽는지 `_read` 로 직접 확인한다.
    import tempfile as _tf
    with _tf.TemporaryDirectory() as _td:
        _p = os.path.join(_td, 'p2_SBE_old.json')
        json.dump({'step3': {'sigma_e_S_cm': 1.0, 'n_dof': 1, 'cg_info': 0},
                   'manifest': {'vox_um': 0.15}}, open(_p, 'w'))
        _old = _read(_p)
    chk(f'⑬ 옛 payload 의 없는 필드는 False 로 정규화 ({_old["sdcp_yield_to_vgcf"]!r})',
        _old['sdcp_yield_to_vgcf'] is False)
    #  ⑭ PTFE 스탬프 팔(CL-49)이 생산 팔과 섞이면 잡는다 + 옛 payload 는 0.0 정규화
    _mix4 = mk(base, [v * 1.08 for v in base])
    for _r in _mix4['DBE']:
        _r['sigma_ptfe_S_cm'] = 1e-16
    v14 = verdict(_mix4)
    chk(f'⑭ PTFE 스탬프 팔 × 생산 팔 혼합은 HOLD ({v14["decision"]})',
        v14['decision'] == 'HOLD' and 'sigma_ptfe_S_cm' in (v14.get('reason') or ''))
    chk(f'⑭b 옛 payload 의 없는 sigma_ptfe 는 0.0 정규화 ({_old["sigma_ptfe_S_cm"]!r})',
        _old['sigma_ptfe_S_cm'] == 0.0)
    #  ── 2026-08-19 (코팅·도핑 코드리뷰 A5) — 도핑 축 · 침대 세대 ───────────────────────
    #  ⑮ 도펀트 팔(σ_ion 만 다름)이 생산 팔과 섞이면 잡는다.  ⚠ 이것이 리뷰가 지목한
    #     "CL-43/CL-49 에서 두 번 고친 no-op 이 σ_ion 축에는 아직 살아 있다" 의 회귀다.
    _mix5 = mk(base, [v * 1.08 for v in base])
    for _r in _mix5['DBE']:
        _r['sigma_ion_se_S_cm'] = 0.003 * 1.94              # Cu/Br 이중도핑 ×1.94
    v15 = verdict(_mix5)
    chk(f'⑮ ★ 도펀트 팔 × 생산 팔 혼합은 HOLD ({v15["decision"]})',
        v15['decision'] == 'HOLD' and 'sigma_ion_se_S_cm' in (v15.get('reason') or ''))
    #  ⑯ σ_AM 은 σ_e 솔브에 **직접** 들어가는데 여태 미게이트였다.
    _mix6 = mk(base, [v * 1.08 for v in base])
    for _r in _mix6['DBE']:
        _r['sigma_am_s_S_cm'] = 5e-5                        # Alabdali 문헌값으로 바꿔 본 팔
    v16 = verdict(_mix6)
    chk(f'⑯ ★ σ_AM 이 다른 팔이 섞이면 HOLD ({v16["decision"]})',
        v16['decision'] == 'HOLD' and 'sigma_am_s_S_cm' in (v16.get('reason') or ''))
    #  ⑰ SE 본체 압밀 물성이 다르면 **침대 세대가 다르다** (CL-42 의 SE 축 재현 경로).
    _mix7 = mk(base, [v * 1.08 for v in base])
    for _r in _mix7['DBE']:
        _r['se_E_GPa'] = 1.60
    v17 = verdict(_mix7)
    chk(f'⑰ ★ SE 압밀 물성이 다르면 HOLD (침대 세대 분리) ({v17["decision"]})',
        v17['decision'] == 'HOLD' and 'se_E_GPa' in (v17.get('reason') or ''))
    #  ⑱ ★★ 세대 **혼합** — 옛 payload(기록 없음) + 새 payload(기록 있음).  정규화가 불가능한
    #     축이라 "없으면 무시" 로 두면 ⑮ 가 통과해 버린다.  섞이면 HOLD 여야 한다.
    _mix8 = mk(base, [v * 1.08 for v in base])
    for _r in _mix8['SBE']:
        for _f in _GEN_FIELDS:
            _r[_f] = None                                    # 옛 payload
    v18 = verdict(_mix8)
    chk(f'⑱ ★★ 세대 혼합(옛 payload + 새 payload)은 HOLD ({v18["decision"]})',
        v18['decision'] == 'HOLD' and '세대 혼합' in (v18.get('reason') or ''))
    #  ⑲ 전부 옛 payload 면 **멈추지 않는다** — 진행 중인 vox 0.125 스윕을 죽이지 않기 위해서다.
    #     (그 디렉터리 안에서는 세대가 하나뿐이므로 비교 자체는 유효하다.)
    _old_all = mk(base, [v * 1.08 for v in base])
    for _r in _old_all['SBE'] + _old_all['DBE']:
        for _f in _GEN_FIELDS:
            _r[_f] = None
    chk(f'⑲ 전부 옛 payload 면 판정은 계속된다 ({verdict(_old_all)["decision"]})',
        verdict(_old_all)['decision'] != 'HOLD')
    #  ⑳ seed 앙상블 면제는 **seed 하나만** 푼다 — 다른 인자는 그대로 잡혀야 한다.
    _se1 = mk(base, [v * 1.08 for v in base])
    for _i, _r in enumerate(_se1['SBE'] + _se1['DBE']):
        _r['mpm_seed'] = _i                                  # 팔마다 다른 seed
    chk(f'⑳ seed 가 다르면 기본은 HOLD ({verdict(_se1)["decision"]})',
        verdict(_se1)['decision'] == 'HOLD' and 'mpm_seed' in (verdict(_se1).get('reason') or ''))
    v20b = verdict(_se1, seed_ensemble=True)
    chk(f'⑳b --seed-ensemble 이면 seed 만 면제되고 판정이 난다 ({v20b["decision"]})',
        v20b['decision'] != 'HOLD' and v20b.get('seed_ensemble') is True)
    _se2 = mk(base, [v * 1.08 for v in base])
    for _i, _r in enumerate(_se2['SBE'] + _se2['DBE']):
        _r['mpm_seed'] = _i
    for _r in _se2['DBE']:
        _r['sigma_ion_se_S_cm'] = 0.006                      # seed 면제를 틈타 σ 도 바꿈
    v20c = verdict(_se2, seed_ensemble=True)
    chk(f'⑳c --seed-ensemble 이어도 σ_ion 이 다르면 HOLD ({v20c["decision"]})',
        v20c['decision'] == 'HOLD' and 'sigma_ion_se_S_cm' in (v20c.get('reason') or ''))
    #  ㉑ ★ fable F4 — 첨가제 E 세대(CL-56 축).  SDCP 23.6 침대와 9.0 침대가 섞이면 HOLD.
    #     (dict 값이라 set 정규화 경로도 함께 검증된다.)
    _mixE = mk(base, [v * 1.08 for v in base])
    for _r in _mixE['DBE']:
        _r['additive_E_GPa'] = {'VGCF': 10.0, 'PTFE': 0.3, 'SDCP': 9.0}
    v21 = verdict(_mixE)
    chk(f'㉑ ★ 첨가제 E 가 다른 침대 혼합은 HOLD (SDCP 23.6 vs 9.0) ({v21["decision"]})',
        v21['decision'] == 'HOLD' and 'additive_E_GPa' in (v21.get('reason') or ''))
    #  ㉒ ★★ 2026-08-20 (전수 감사 코드 #2) — **기록이 없으면 게이트가 no-op** 부류의 잔존.
    #     고정-인자 루프는 None 을 skip 하므로, 그 인자를 **아무 팔도 기록하지 않은 세대**면
    #     검사가 통과해 버린다.  실측으로 여섯 필드가 전부 그랬다 (HOLD 가 아니라 h0).
    #     한 필드씩 지워 **전부** HOLD 가 되는지 본다 — 목록에서 하나가 빠지면 이 검사가 죽는다.
    for _f in ('sigma_vgcf_S_cm', 'sigma_sdcp_S_cm', 'sdcp_sphere_d_um',
               'backend', 'sdcp_yield_to_vgcf', 'sigma_ptfe_S_cm'):
        _v22 = verdict(mk(base, [v * 1.08 for v in base], **{_f: None}))
        chk(f'㉒ 기록 없는 고정 인자 `{_f}` 는 HOLD ({_v22["decision"]})',
            _v22['decision'] == 'HOLD' and _f in (_v22.get('reason') or ''))

    print(f'\nsdcp_gain_verdict selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', default='')
    ap.add_argument('--collect-only', action='store_true')
    ap.add_argument('--out', default='')
    ap.add_argument('--selftest', action='store_true')
    #  ★ 2026-08-19 (A5) — seed 앙상블 축.  `mpm_seed` **하나만** 고정 인자에서 면제한다.
    #    ⚠ prereg 에 그렇게 등록한 경우에만 쓸 것 — 면제는 판정 출력에 남는다.
    ap.add_argument('--seed-ensemble', action='store_true',
                    help='mpm_seed 를 고정 인자에서 면제 (시딩이 확률적인 축을 잴 때). '
                         'prereg 에 등록한 경우에만.')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if not a.dir:
        raise SystemExit('사용: --dir <결과 디렉터리>')
    rows, arms = collect(a.dir)
    print(f'{"파일":<28} {"σ_e":>12} {"σ_ion":>12} {"dof":>12} {"origin shift":>22} {"cg":>4}')
    for r in rows:
        print(f'{r["file"]:<28} {str(r["sigma_e"]):>12} {str(r["sigma_ion"]):>12} '
              f'{str(r["n_dof"]):>12} {str(r["origin_shift_um"]):>22} {str(r["cg_info"]):>4}')
    print(f'\n  수집: SBE {len(arms["SBE"])} 팔 · DBE {len(arms["DBE"])} 팔')
    if a.collect_only:
        print('  (--collect-only — 판정하지 않는다)')
        raise SystemExit(0)
    v = verdict(arms, seed_ensemble=a.seed_ensemble)
    print(f'\n══ 판정 (prereg §5) ══\n  결정: **{v["decision"]}**\n  근거: {v["reason"]}')
    if 'ratio' in v:
        print(f'  σ_e 비 = {v["ratio"]}   (h0 ≥ {H0_MIN_RATIO} · h1 = {H1_RATIO})')
    if 'se_ratio_pct' in v:
        print(f'  비의 표준오차 = {v["se_ratio_pct"]} %p (문턱 {SE_MAX_PCT})')
    if a.out:
        json.dump({'rows': rows, 'verdict': v}, open(a.out, 'w'), ensure_ascii=False, indent=1)
        print(f'\n  → {a.out}')
    raise SystemExit(0 if v['decision'] in ('h0', 'h1') else 1)
