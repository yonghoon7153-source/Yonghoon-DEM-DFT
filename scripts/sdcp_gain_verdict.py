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
#  ⚠⚠ 2026-08-24 (CDXR2-3) — 이 문턱과 그 짝 `se_ratio_rel_pct` 는 **비의 상대 RSE(%)**
#    다.  절대 percentage-point 가 아니다 (`SE_abs(%p) = R · SE_rel(%)`).  prereg 본문이
#    유도는 상대 % 로 하고(§ '팔 SE 0.58 % · 비 SE 0.82 %') 문턱만 `%p` 로 적어 두어
#    라벨이 어긋나 있었다.  **게이트는 상대끼리 비교라 처음부터 자기일관**했고 다섯 기록
#    전부 절대 %p 로 다시 읽어도 통과한다 ⇒ 재판정 없음.  이름만 바로잡는다.
SE_MAX_REL_PCT = 1.17        # 비의 **상대** RSE 문턱 [%].  넘으면 판정 보류하고 origin 을 늘린다
SE_MAX_PCT = SE_MAX_REL_PCT  # ⚠ deprecated 별칭 — 옛 호출부/픽스처 호환용.  새 코드는 위를 쓸 것
PREREG = 'docs/reviews/sdcp_gain_prereg_v2_20260816.md'

#  ★★ 2026-08-19 (코팅·도핑 코드리뷰 A5) — 세대(generation) 인자.
#  이 필드들은 **매니페스트에 방금 추가된 것**이라 그 이전 payload 에는 없다.  두 극단이 다
#  틀렸다 — "없으면 무시" 로 두면 옛(기본 σ) 팔과 새(도핑) 팔이 섞여도 안 잡히고(= H5 no-op
#  재발), "없으면 HOLD" 로 하면 **진행 중인 스윕이 통째로 멈춘다**(vox 0.125 팔들이 옛 payload).
#  ⇒ 정확한 판정은 **섞이면 HOLD** 다: 한 디렉터리 안에서 어떤 팔은 기록이 있고 어떤 팔은
#  없다면, 그것이 바로 세대가 갈렸다는 신호이므로 비교할 수 없다.
#  ★★★ 2026-08-24 (CDXR2-6/CDXR2-7) — **고정 인자의 단일 소스**.
#    실사고: `ptfe_stamp` 를 목록에 넣었는데 게이트가 **발화하지 않았다**.  같은 목록이
#    세 곳에 **따로 하드코딩**돼 있었기 때문이다 — ⓐ 팔간-차이 루프 ⓑ 부재 검사 루프
#    ⓒ `compare_dirs` 용 튜플.  하나만 늘리면 나머지 둘은 그대로다.
#    ⇒ 셋이 **이것 하나를** 쓴다.  회귀 ㉞ 가 인라인 튜플의 재출현을 막는다.
#    ⚠ 여기에 필드를 더하면 그 필드를 기록하지 않는 **옛 세대 payload 는 HOLD** 가 된다.
#      그것이 규약이다 (H5 의 논리 — 기록되지 않은 인자는 고정을 확인할 수 없다).
#  · `ptfe_stamp`/`ptfe_zero_dof`: σ_PTFE 만 보면 **exact-zero(σ=0·스탬프 ON)와
#    미스탬프(σ=0·스탬프 OFF)가 구분되지 않는다** — 둘 다 sigma_ptfe_S_cm=0.0 이다.
#: ★★★ **필드 계약 레지스트리** (CDXR3-5, 종료조건 ⑧).  `scope` · 비교 규칙을 **한 곳에**
#   선언하고 아래 파생 튜플과 모든 게이트가 여기서 나온다.
#     scope 'physics' — 규약을 정하는 물리 인자.  `physics_protocol_id` 에 들어간다.
#     scope 'numeric' — 수치 방법 (규약은 아니나 팔 간 고정돼야 한다).
#     scope 'bed'     — 침대 정체성.  **침대 안에서만** 고정 (침대끼리는 달라야 정상, FA-06).
#   `across_dir` — cross-directory 대조(`compare_dirs`)에서도 고정인가.
#     ⚠ 옛 판은 `compare_dirs` 가 `_FIXED_FIELDS` 만 봐서 `_GEN_FIELDS`(σ_AM·σ_ion·온도·
#       침대 세대)가 **두 디렉터리 사이에서 자유롭게 달라져도 `measured` 를 냈다**
#       (Codex 실측: `sigma_am_s_S_cm` 0.010→0.020 이 통과).  ⇒ 여기서 한 번에 정한다.
FIELD_CONTRACT = {
    'vox':                  dict(scope='physics', across_dir=True, required=True),
    'bridge_um':            dict(scope='physics', across_dir=True, required=True),
    'fibre_stamp':          dict(scope='physics', across_dir=True, required=True),
    'sdcp_stamp':           dict(scope='physics', across_dir=True, required=True),
    'sdcp_sphere_d_um':     dict(scope='physics', across_dir=True, required=True),
    'sigma_vgcf_S_cm':      dict(scope='physics', across_dir=True, required=True),
    'sigma_sdcp_S_cm':      dict(scope='physics', across_dir=True, required=True),
    'sdcp_yield_to_vgcf':   dict(scope='physics', across_dir=True, required=True),
    'sigma_ptfe_S_cm':      dict(scope='physics', across_dir=True, required=True),
    'ptfe_stamp':           dict(scope='physics', across_dir=True, required=True),
    'ptfe_zero_dof':        dict(scope='physics', across_dir=True, required=True),
    'backend':              dict(scope='numeric', across_dir=True, required=True),
    # ── 세대 인자 (옛 `_GEN_FIELDS`) — 전부 physics 다.  섞이면 다른 실험이다. ──
    'sigma_ion_se_S_cm':    dict(scope='physics', across_dir=True),
    'sigma_ion_sdcp_S_cm':  dict(scope='physics', across_dir=True),
    'sigma_am_s_S_cm':      dict(scope='physics', across_dir=True),
    'sigma_am_p_S_cm':      dict(scope='physics', across_dir=True),
    'cam':                  dict(scope='physics', across_dir=True),
    'temp_c':               dict(scope='physics', across_dir=True),
    'ea_ion_ev':            dict(scope='physics', across_dir=True),
    'se_E_GPa':             dict(scope='physics', across_dir=True),
    'se_nu':                dict(scope='physics', across_dir=True),
    'se_sigma_y_GPa':       dict(scope='physics', across_dir=True),
    'mpm_seed':             dict(scope='physics', across_dir=True),
    # ── 침대 정체성 — 침대 **안**에서만 고정 (FA-06: SBE 에 SDCP 가 없는 것은 정상) ──
    'additive_E_GPa':       dict(scope='bed', across_dir=True),
    'input_digest':         dict(scope='bed', across_dir=True),
    # ── 코드 정체성 — 침대와 무관하지만 **섞이면 다른 실험**이다 (CDXIJ-10 ③). ──
    'code_sha':             dict(scope='numeric', across_dir=True),
    #  ★★ 2026-08-25 (CDXR3-3) — **물리 규약 정체성**.  적용된 인자들에서 파생된 해시라
    #    개별 필드가 하나라도 다르면 이것도 달라진다 = 요약 봉인.  required 로 둔다 —
    #    기록이 없으면 어느 규약인지 확정할 수 없다.
    'physics_protocol_id':  dict(scope='physics', across_dir=True, required=True),
    #  요청↔적용 불일치 (payload 가 기록).  False 면 그 팔은 요청과 다른 규약으로 돌았다.
    'physics_protocol_match': dict(scope='physics', across_dir=True),
}


def contract_fields(scope=None, across_dir=None, required=None):
    """레지스트리에서 필드 이름을 뽑는다 — **모든 게이트의 유일한 출처**.

    ★ `required` (Codex 의 `required_since`) — **있어야 하는가** 와 **달라지면 안 되는가**
      는 다른 축이다.  세대 인자(σ_AM·온도·침대 E)는 *섞이면 HOLD, 전부 없으면 통과* 다
      (옛 payload 를 죽이지 않는다, 회귀 ⑲).  규약 인자는 *없으면 HOLD* 다 (H5)."""
    return tuple(k for k, v in FIELD_CONTRACT.items()
                 if (scope is None or v['scope'] in (scope if isinstance(scope, (tuple, list))
                                                     else (scope,)))
                 and (across_dir is None or v.get('across_dir') is across_dir)
                 and (required is None or bool(v.get('required', False)) is required))


#: 팔 간 고정 인자 (같은 디렉터리) — physics + numeric.  bed 는 제외 (침대끼리 다르다).
_FIXED_FIELDS = contract_fields(scope=('physics', 'numeric'))
#: 그중 **기록이 없으면 HOLD** 인 것 (규약 인자).  세대 인자는 여기 없다 — 회귀 ⑲ 참조.
_REQUIRED_FIELDS = contract_fields(required=True)
#: 침대 정체성 — 침대 안에서만 고정.
_BED_FIELDS_C = contract_fields(scope='bed')
#: cross-directory 대조에서 고정할 축 — **세대 인자와 침대까지** 포함한다.
_XDIR_FIELDS = contract_fields(across_dir=True)

_GEN_FIELDS = ('sigma_ion_se_S_cm', 'sigma_ion_sdcp_S_cm',
               'sigma_am_s_S_cm', 'sigma_am_p_S_cm', 'cam',
               'temp_c', 'ea_ion_ev', 'mpm_seed',
               'se_E_GPa', 'se_nu', 'se_sigma_y_GPa',
               #  ★ fable 리뷰 ② F4 (2026-08-19) — CL-56 축.  SDCP E 23.6 ↔ 9.0 침대가
               #    섞여도 여태 게이트가 못 봤다.  dict 는 그대로 비교된다 (json 왕복 후
               #    같은 dict 면 ==; 다르면 아래 "다르면 HOLD" 가 발화).
               'additive_E_GPa',
               #  ★★ CDXIJ-10 ③ (2026-08-20) — 입력 artifact 내용 해시와 코드 커밋.
               #    같은 디렉터리라는 것은 같은 입력·같은 코드의 증거가 아니다 (Codex CDX-IJ-02).
               #    ⚠ 세대 필드로 둔다 = **섞이면 HOLD**, 전부 없으면(옛 런) 통과.
               #      존재 자체를 요구하려면 `--require-digest` (도핑 트랙이 쓴다).
               'input_digest', 'code_sha')

#  ⚠ `mpm_seed` 는 **팔마다 달라야 하는 축이 될 수도 있다** (코팅처럼 시딩 자체가 확률적인
#  경우 = seed 앙상블).  현행 origin 앙상블은 같은 압밀 산물을 재사용하므로 seed 가 고정이고,
#  그래서 지금은 고정 인자로 둔다.  seed 앙상블을 돌 때는 prereg 에 그렇게 등록하고
#  `--seed-ensemble` 로 이 하나만 면제한다 (아래 verdict 인자).
_SEED_FIELD = 'mpm_seed'



def _component_backends(man):
    """→ {component: used} (돌아간 component 만).  하나도 없으면 None → missing 게이트.

    ★ 정본은 `manifest['components'][c]['backend']` 다 (`mpm_webapp_payload._s3mark` 가
      component 별로 스냅샷한다).  `backend_last_solve` 는 **마지막 solve 하나**뿐이라
      component 사이의 폴백 차이를 접어 버린다 (2026-08-20 Codex 재현).
    """
    comps = (man.get('components') or {})
    out = {}
    for name, rec in comps.items():
        bk = (rec or {}).get('backend')
        if isinstance(bk, dict) and bk.get('used'):
            out[name] = bk['used']
    return out or None


def _read(path):
    d = json.load(open(path, encoding='utf-8'))
    s = d.get('step3') or (d.get('mpm_metrics') or {}).get('step3') or {}
    man = s.get('manifest') or {}
    return {'file': os.path.basename(path),
            'sigma_e': s.get('sigma_e_eff_S_cm'),
            'sigma_ion': s.get('sigma_ion_eff_S_cm'),
            #  ★ 2026-08-24 (CDXR2-4) — 이온 수렴 봉인.  `None` = 그 세대 payload 가
            #    아예 안 실었다는 뜻이고, 아래 `require_ionic` 게이트가 fail-closed 로 잡는다.
            'ion_cg_info': s.get('ion_cg_info'),
            'ion_unconverged': s.get('ion_unconverged'),
            'ion_resid': s.get('ion_resid'),
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
            #  ★ 2026-08-24 (CDXR2-6) — 부재는 `None` 으로 보존한다 (CDX-IJ-01 의 교훈:
            #    기본값으로 접으면 missing 게이트가 원리적으로 발화하지 못한다).
            'ptfe_stamp': man.get('ptfe_stamp'),
            'physics_protocol_id': man.get('physics_protocol_id'),
            'physics_protocol_match': (None if man.get('physics_protocol_match') is None
                                       else bool(man.get('physics_protocol_match'))),
            'ptfe_zero_dof': (None if man.get('ptfe_zero_dof') is None
                              else bool(man.get('ptfe_zero_dof'))),
            'sdcp_sphere_d_um': man.get('sdcp_sphere_d_um'),
            #  ★★ 2026-08-20 정정 (Codex CDX-IJ-01) — **부재를 기본값으로 접지 않는다.**
            #    옛 판은 `bool(man.get(..., False))` · `float(man.get(..., 0.0) or 0.0)` 이라
            #    기록이 **없어도 False/0.0** 이 나왔다.  missing 게이트는 `None` 만 보므로
            #    이 두 필드에서는 **원리적으로 발화할 수 없었다** — FA-02 의 6필드 수정 중
            #    4/6 만 실제로 닫혔고 이 둘은 계속 `h0` 였다 (Codex 가 실제 JSON 16개에서
            #    키를 지워 재현).  ⚠ 내 회귀 ㉒ 는 `_read()` 를 **건너뛰고** 내부 row 에 None 을
            #    직접 넣어서 이것을 놓쳤다 = "실제 경로를 안 타는 테스트" 부류의 재발.
            #    ⇒ 부재는 `None` 으로 보존하고 판단은 게이트가 한다 (fail-closed).
            #    ⚠ 대가: 플래그 이전 세대(08-18 이전) payload 는 이제 HOLD 다.  현행 payload 는
            #      두 필드를 **항상** 기록하므로(`mpm_webapp_payload` 매니페스트) 실사용엔 영향 없다.
            'sdcp_yield_to_vgcf': (None if man.get('sdcp_yield_to_vgcf') is None
                                   else bool(man.get('sdcp_yield_to_vgcf'))),
            'sigma_ptfe_S_cm': (None if man.get('sigma_ptfe_S_cm') is None
                                else float(man.get('sigma_ptfe_S_cm'))),
            'sigma_vgcf_S_cm': man.get('sigma_vgcf_S_cm'),
            'sigma_sdcp_S_cm': man.get('sigma_sdcp_S_cm'),
            #  ★★ 2026-08-19 (코팅·도핑 리뷰 A5) — 도핑 축과 침대 세대.  **정규화하지 않는다**:
            #    `sdcp_yield_to_vgcf`(False)·`sigma_ptfe`(0.0) 는 "플래그 이전 = 정의상 생산 규약"
            #    이라 기본값이 정답이었지만, σ_ion·σ_AM·E_SE·seed 는 옛 payload 가 무슨 값으로
            #    돌았는지 **추정할 수 없다** (--temp-c 로도 움직인다).  None 으로 두고 아래
            #    _GEN_FIELDS 세대-혼합 게이트가 잡는다.
            **{f: man.get(f) for f in _GEN_FIELDS},
            #  ⚠⚠ 2026-08-20 — 옛 판은 `.get('backend')` 를 읽었는데 그 키는 **존재하지 않는다**.
            #    `step3_sigma.LAST_BACKEND` 는 `{requested, used, fallback_reason, precond}` 이고
            #    payload 는 그것을 그대로 싣는다 ⇒ 이 필드는 **모든 런에서 항상 None** 이었다.
            #    · 오늘 이전: 고정-인자 루프가 None 을 skip 해서 아무 일도 안 일어났다 —
            #      :74 주석이 "CuPy 실패 시 조용한 CPU 폴백을 잡는다" 고 적어 둔 그 검사가
            #      **한 번도 발화한 적이 없다** (H5 부류의 세 번째 재발, 이번엔 내가 08-18 에 만든 것).
            #    · 오늘 이후: missing 게이트가 걸려 **모든 디렉터리가 거짓 HOLD** 를 냈다
            #      (vox 0.115 실측 — 그 덕에 드러났다).
            #    ⇒ 실제 값 `used` 를 읽는다.  하위호환 별칭 `backend` 도 같은 dict 라 폴백으로 둔다.
            #    ⚠ `precond`(jacobi/amg)는 **게이트하지 않는다** — σ_eff 는 전처리에 불변이다
            #      (rtol 1e-8 에서 ≤0.014 %, step3_sigma docstring).  가르는 것은 gpu↔cpu 다.
            #  ⚠⚠⚠ 2026-08-20 재수정 (Codex 재검증 NEW-DEFECT P1) — `backend_last_solve` 는
            #    **마지막 solve 하나**다.  payload 주석 자신이 ":1834 components[c]['backend'] 가
            #    정본이고 여기는 하위호환 요약" 이라고 적어 뒀는데 내가 요약을 읽고 있었다.
            #    Codex 재현: SBE electronic=gpu · DBE electronic=**cpu** 인데 양쪽
            #    `backend_last_solve`(마지막=thermal)가 gpu 라 파싱값이 ['gpu'] 하나로 접혀 **h0**.
            #    = 이 필드가 잡으라고 만들어진 "조용한 CPU 폴백" 이 정확히 통과한다.
            #    ⇒ **component 별 `used` 를 전부** 읽어 dict 로 비교한다 (고정-인자 루프가
            #      json 정규화로 dict 를 비교할 수 있다).  하나도 없으면 None → missing 게이트.
            'backend': _component_backends(man),
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


def seal_lines(v):
    """판정 dict → (봉인 통과?, 출력 줄들).  **h0/h1 과 비를 누설하지 않는다.**

    러너가 이것을 돌린다.  봉인 = 데이터가 쓸 만한가(팔 수·origin 집합·수렴·digest·
    고정인자), 판정 = 그것이 뭐라고 말하는가(h0/h1/비).  둘을 가르는 것이 요점이다 —
    러너가 판정을 보면 사전등록이 깨진다 (결과를 보고 창을 옮길 수 있게 된다).
    ⇒ HOLD 사유는 **데이터 상태**에 관한 말이라 실어도 되고, `decision`·`ratio`·
      `ratio_paired_mean`·`ratio_arms` 는 **절대** 싣지 않는다."""
    ok = v.get('decision') != 'HOLD'
    out = ['', '══ 계약 봉인 (판정 아님) ══',
           f'  봉인: {"통과" if ok else "**깨짐**"}']
    if not ok:
        out.append(f'  근거: {v.get("reason")}')
    out.append('  ⚠ h0/h1 과 비는 출력하지 않는다 — 판정은 prereg §5 순서로 따로 돈다')
    return ok, out


def verdict(arms, seed_ensemble=False, require_arms=None, require_ionic=False,
            require_digest=False):
    """prereg §5 판정.  **순서를 바꾸지 말 것.**

    `seed_ensemble=True` 는 **`mpm_seed` 하나만** 고정 인자에서 면제한다 (코팅처럼 시딩
    자체가 확률적인 축을 잴 때).  ⚠ prereg 에 그렇게 등록한 경우에만 쓸 것 — 나머지
    인자는 그대로 고정이고, 면제 사실은 판정 출력에 남는다.
    """
    out = {'prereg': PREREG, 'thresholds': {
        'h0_min_ratio': H0_MIN_RATIO, 'h1_ratio': H1_RATIO,
        'undecided': [UNDECIDED_LO, UNDECIDED_HI],
                  'se_max_rel_pct': SE_MAX_REL_PCT, 'se_max_pct': SE_MAX_REL_PCT}}
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
    #  ★★★ 2026-08-20 (FA-06) — **침대 정체성 필드는 침대 사이에서 비교하면 안 된다.**
    #    실사고: 도핑 baseline 8팔이 `additive_E_GPa` 로 HOLD 를 맞았다 —
    #      SBE `{PTFE, VGCF}` vs DBE `{PTFE, SDCP, VGCF}`.
    #    SBE 에 SDCP 항목이 없는 것은 **위반이 아니라 이 실험의 독립변수 그 자체**다.
    #    `input_digest` 도 같다 (내가 어제 넣은 것) — 두 침대는 **반드시** 다른 파일이다.
    #    ⇒ 두 필드는 **침대 안에서** 고정을 본다.  그러면 CL-56 이 겨냥한 것(DBE 안에서
    #      SDCP E 23.6 ↔ 9.0 섞임)은 그대로 잡히고, 침대 사이 공통 키(PTFE·VGCF)는 아래에서
    #      따로 대조해 세대 혼합도 계속 잡는다.
    #  ★ 2026-08-25 (CDXR3-5) — 레지스트리 파생.  지역 튜플을 따로 두면 또 갈라진다.
    _BED_FIELDS = _BED_FIELDS_C
    for fld in _BED_FIELDS:
        for k in ('SBE', 'DBE'):
            _v = {_canon(r.get(fld)) for r in arms[k] if r.get(fld) is not None}
            if len(_v) > 1:
                return dict(out, decision='HOLD',
                            reason=f'{k} **안에서** `{fld}` 가 팔마다 다르다 '
                                   f'({sorted(map(str, _v))}) — 한 침대의 팔들은 같은 입력·같은 '
                                   f'물성이어야 한다 (CL-56 축)')
    #  ★ 침대 **사이**: digest 는 달라야 하고(같으면 같은 침대다), additive 는 **공통 키**만 같아야 한다.
    _ds = {r.get('input_digest') for r in arms['SBE'] if r.get('input_digest')}
    _dd = {r.get('input_digest') for r in arms['DBE'] if r.get('input_digest')}
    if _ds and _dd and _ds == _dd:
        return dict(out, decision='HOLD',
                    reason=f'SBE 와 DBE 의 `input_digest` 가 **같다** ({sorted(_ds)[0]}) — 두 팔이 '
                           f'같은 침대를 읽고 있다.  비 1.0 은 물리가 아니라 배선 실수다')
    _as = next((r['additive_E_GPa'] for r in arms['SBE'] if r.get('additive_E_GPa')), None)
    _ad = next((r['additive_E_GPa'] for r in arms['DBE'] if r.get('additive_E_GPa')), None)
    if isinstance(_as, dict) and isinstance(_ad, dict):
        _diff = {k for k in set(_as) & set(_ad) if _as[k] != _ad[k]}
        if _diff:
            return dict(out, decision='HOLD',
                        reason=f'두 침대가 `additive_E_GPa` 의 **공통 상**에서 다르다 ({sorted(_diff)}: '
                               f'{ {k: (_as[k], _ad[k]) for k in sorted(_diff)} }) — 세대가 섞였다 '
                               f'(CL-56).  SDCP 처럼 한쪽에만 있는 상은 정상이다')
    #  ★ A5: σ_ion 축(도핑)과 σ_AM·CAM·T — σ_AM 은 σ_e 솔브에 직접 들어가고,
    #    σ_ion 은 도핑 트랙의 **유일한** 노브다.  둘 다 여태 미게이트였다.
    #  ★ 2026-08-25 (CDXR3-5) — 레지스트리가 세대 인자까지 담으므로 목록이 하나다.
    #    면제(`_gen_ex`, --seed-ensemble)는 **전체에 균일하게** 적용한다 — 옛 판은
    #    세대 목록에만 걸어서, 같은 필드가 `_FIXED_FIELDS` 에도 있으면 면제가 무시됐다.
    for fld in (f for f in _FIXED_FIELDS if f not in _gen_ex):
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
    #  ★★ 2026-08-25 (CDXR3-3) — 요청↔적용 불일치는 **그 자체로** HOLD 다.
    #    (규약 id 가 팔끼리 같아도, 러너가 요청한 것과 다르면 다른 실험이다.)
    _pm = [r['file'] for k in arms for r in arms[k] if r.get('physics_protocol_match') is False]
    if _pm:
        return dict(out, decision='HOLD', hold_code='PROTOCOL_MISMATCH',
                    reason=f'요청한 규약과 **적용된 규약이 다른** 팔이 {len(_pm)}개 '
                           f'({_pm[0]} …) — 러너가 요청한 것과 payload 가 실제로 한 것이 '
                           f'갈렸다.  다시 돌릴 것 (CDXR3-3)')
    #  ★ `unknown:` 접두 = 규약을 확정할 수 없다 (필드가 빠졌다).  통과시키지 않는다.
    _pu = [r['file'] for k in arms for r in arms[k]
           if isinstance(r.get('physics_protocol_id'), str)
           and r['physics_protocol_id'].startswith('unknown:')]
    if _pu:
        return dict(out, decision='HOLD', hold_code='PROTOCOL_UNKNOWN',
                    reason=f'규약을 확정할 수 없는 팔이 {len(_pu)}개 ({_pu[0]} …) — '
                           f'payload 가 규약 인자를 다 싣지 않았다.  현행 payload 로 다시 돌릴 것')
    for fld in _REQUIRED_FIELDS:
        _miss = [r['file'] for k in arms for r in arms[k] if r.get(fld) is None]
        if _miss:
            return dict(out, decision='HOLD',
                        reason=f'고정 인자 `{fld}` 가 매니페스트에 **없는** 팔이 {len(_miss)}개 '
                               f'({_miss[0]} …) — 기록되지 않은 인자는 고정을 확인할 수 없다.  '
                               f'옛 payload 로 돈 팔이면 다시 돌릴 것')
    # ── ★★ 팔 계약 (CDXIJ-10 ①, Codex 재검증 §③) ─────────────────────────────────────
    #   Codex 실측으로 드러난 것: **2팔씩만 있어도** 판정 · origin 이 전부 없어도 통과 ·
    #   SBE origins 0..7 과 DBE origins 100..107 처럼 **완전히 다른 집합**이어도 h0 였다.
    #   ⇒ 짝을 지을 수 없는 데이터는 §5 가 말하는 그 데이터가 아니다.  세 가지를 강제한다:
    #     ⓐ 모든 팔이 origin 을 기록했다  ⓑ 침대 안에서 unique  ⓒ **두 침대의 origin 집합이 같다**
    #   `require_arms` 를 주면 정확한 개수까지 본다 (사전등록 8팔 factorial 용).
    _org = {}
    for k in ('SBE', 'DBE'):
        _miss_o = [r['file'] for r in arms[k] if not r.get('origin_shift_um')]
        if _miss_o:
            return dict(out, decision='HOLD',
                        reason=f'{k} 에 origin 기록이 **없는** 팔이 {len(_miss_o)}개 '
                               f'({_miss_o[0]} …) — origin 없이는 쌍을 지을 수 없다 (CDXIJ-10 ①)')
        _org[k] = [tuple(round(float(x), 9) for x in r['origin_shift_um']) for r in arms[k]]
        if len(set(_org[k])) != len(_org[k]):
            return dict(out, decision='HOLD',
                        reason=f'{k} 에 **중복 origin** — 같은 위상을 여러 번 세면 SE 가 가짜로 작아진다')
    if set(_org['SBE']) != set(_org['DBE']):
        _only_s = sorted(set(_org['SBE']) - set(_org['DBE']))
        _only_d = sorted(set(_org['DBE']) - set(_org['SBE']))
        return dict(out, decision='HOLD',
                    reason=f'두 침대의 **origin 집합이 다르다** — SBE 전용 {len(_only_s)}개 · '
                           f'DBE 전용 {len(_only_d)}개 (예: {(_only_s or _only_d)[:1]}).  '
                           f'짝이 없는 팔로는 비를 정의할 수 없다 (CDXIJ-10 ①)')
    if require_arms is not None and len(_org['SBE']) != int(require_arms):
        return dict(out, decision='HOLD',
                    reason=f'사전등록은 침대당 정확히 {int(require_arms)} origin 을 요구한다 — '
                           f'받은 것은 {len(_org["SBE"])}개 (CDXIJ-10 ①)')
    out['n_origin'] = len(_org['SBE'])

    #  ★ CDXIJ-10 ③ — `require_digest` 면 **입력 digest·code SHA 가 있어야** 한다.
    #    기본은 끔 (옛 격자 팔 호환).  도핑 트랙은 켠다 — 그 실험의 전제가
    #    "pair 간 σ_ion 만 달랐다" 이고, 그것은 digest 없이는 확인할 수 없다.
    if require_digest:
        for _f in ('input_digest', 'code_sha'):
            _nd = [r['file'] for k in arms for r in arms[k] if not r.get(_f)]
            if _nd:
                return dict(out, decision='HOLD',
                            reason=f'`{_f}` 가 없는 팔 {len(_nd)}개 ({_nd[0]} …) — 같은 '
                                   f'디렉터리는 같은 입력·같은 코드의 증거가 아니다 '
                                   f'(CDXIJ-10 ③).  현행 payload 로 다시 돌릴 것')
        _dirty = [r['file'] for k in arms for r in arms[k]
                  if str(r.get('code_sha') or '').endswith('+dirty')]
        if _dirty:
            return dict(out, decision='HOLD',
                        reason=f'커밋 안 된 코드로 돈 팔 {len(_dirty)}개 ({_dirty[0]} …) — '
                               f'`code_sha` 가 `+dirty` 다.  재현 불가한 런은 판정 대상이 아니다')

    #  ★ 결과 seal (CDXIJ-10 ④) — `require_ionic` 이면 σ_ion 이 실제로 있어야 한다.
    #    도핑 트랙은 이온축이 결론이므로 `--no-ion`(LEAN=2) 산출물로 판정하면 안 된다.
    if require_ionic:
        _no_i = [r['file'] for k in arms for r in arms[k]
                 if not (isinstance(r.get('sigma_ion'), (int, float))
                         and r['sigma_ion'] == r['sigma_ion'] and r['sigma_ion'] > 0)]
        if _no_i:
            return dict(out, decision='HOLD',
                        reason=f'σ_ion 이 없는/비정상인 팔 {len(_no_i)}개 ({_no_i[0]} …) — '
                               f'도핑 판정은 이온축이 결론이다.  `--no-ion` 산출물로 판정 불가 '
                               f'(CDXIJ-10 ④)')
        #  ★★ 2026-08-24 (CDXR2-4) — **σ_ion 이 있다는 것과 수렴했다는 것은 다르다.**
        #    옛 게이트는 양의 σ_ion 존재만 봤고, payload 는 이온 미수렴도 `complete` 로
        #    적었다 ⇒ 이온축 결론이 **false-green** 이 될 수 있었다.  전자축은 이미
        #    fail-closed 다 (`no_convergence_info`) — 이온을 같은 규약으로 맞춘다.
        #    ⚠ 봉인 이전 세대 payload 는 필드가 **없어** HOLD 가 된다.  그것이 옳다 —
        #      수렴했는지 모르는 값으로 이온축 결론을 내지 않는다.  σ_e 만 볼 때는
        #      `--require-ionic` 을 켜지 않으면 되고, 이온축이 결론이면 재실행해야 한다.
        #  ★★ 2026-08-24 (CDXR3-4) — 초판은 `ion_unconverged` 가 truthy 일 때만 실패하고
        #    **둘 다** None 일 때만 blind 로 봤다.  그 사이 상태공간이 통째로 뚫려 있었다
        #    (실측): `cg_info=30000` 인데 `unconverged=False` (모순) → h0 · 한쪽만 있고
        #    다른 쪽이 좋아 보임 (반쪽) → h0.
        #    ⇒ **conjunction 을 요구한다**: cg_info == 0 ∧ unconverged is False ∧ resid 유한.
        #      모르는 것·모순·타입 오류는 전부 HOLD (fail-closed).
        def _ion_ok(r):
            ci, un, rs = r.get('ion_cg_info'), r.get('ion_unconverged'), r.get('ion_resid')
            if ci is None or un is None:
                return False, 'blind'
            if not isinstance(un, bool) or isinstance(ci, bool) or not isinstance(ci, (int, float)):
                return False, 'type'
            if bool(un) or int(ci) != 0:
                return False, 'unconv'
            if rs is not None and not (isinstance(rs, (int, float)) and rs == rs
                                       and abs(rs) != float('inf')):
                return False, 'resid'
            return True, ''
        _ion_bad, _ion_blind = [], []
        for _k in arms:
            for _r in arms[_k]:
                _ok, _why = _ion_ok(_r)
                if not _ok:
                    (_ion_blind if _why == 'blind' else _ion_bad).append(_r['file'])
        if _ion_bad:
            return dict(out, decision='HOLD', hold_code='IONIC_UNCONVERGED',
                        ion_unconverged_arms=len(_ion_bad),
                        reason=f'이온 솔브가 **미수렴**인 팔 {len(_ion_bad)}개 ({_ion_bad[0]} …) — '
                               f'prereg §5-1 대로 숫자를 내지 않는다')
        if _ion_blind:
            return dict(out, decision='HOLD', hold_code='IONIC_BLIND',
                        ion_no_convergence_info=len(_ion_blind),
                        reason=f'이온 수렴 정보가 **없는** 팔 {len(_ion_blind)}개 '
                               f'({_ion_blind[0]} …) — 봉인 이전 세대 payload 다 (CDXR2-4).  '
                               f'이온축이 결론이면 재실행할 것; σ_e 만 보려면 '
                               f'`--require-ionic` 을 끄면 된다')

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
    se_ratio_rel_pct = 100.0 * math.hypot(st['SBE']['se'] / st['SBE']['mean'],
                                          st['DBE']['se'] / st['DBE']['mean'])
    out['se_ratio_rel_pct'] = round(se_ratio_rel_pct, 4)
    out['se_ratio_pct'] = out['se_ratio_rel_pct']       # ⚠ deprecated 별칭 (CDXR2-3)
    #  ★ 절대 percentage-point 는 **파생**이다: SE_abs = R · SE_rel.  R > 1 이면 상대값을
    #    그대로 %p 로 읽는 것이 불확도를 **과소**보고한다 (반보수적) — 그래서 따로 낸다.
    #    ⚠ **게이트에는 쓰지 않는다**.  게이트 입력은 런 전에 커밋된 상대 % 그대로다.
    out['se_ratio_abs_pp'] = round(ratio * se_ratio_rel_pct, 4)
    #  ── 보조 통계: **쌍대응** SE (심층 리뷰 ③④) ───────────────────────────────────────
    #    팔은 origin 으로 쌍이 맞고 두 침대가 강한 공통모드를 갖는다 (실측 r = +0.963).
    #    위 hypot 은 두 팔을 독립으로 보므로 비의 SE 를 **5.1 배 과대**평가한다 (보수 방향).
    #    ⚠ **게이트는 그대로 hypot 을 쓴다** — 그것이 런 전에 커밋된 조작적 정의다 (prereg §4).
    #      쌍별 값은 **보조 출력**일 뿐이고, 게이트 승격은 v3 prereg 에서 등록한다.
    #  ⚠⚠ 2026-08-20 (Codex 재검증 CDXIJ-10 ②) — 옛 판은 **파일명 정렬 뒤 zip()** 이었다.
    #    파일명 순서가 origin 순서와 다르면 **엉뚱한 짝**이 지어지고, Codex 실측에서 그 상태로
    #    paired SE 가 0.0 % 로 보고됐다 (참값 0.8511 %).  ⇒ **origin 을 키로 join** 한다.
    #    (위 계약이 이미 두 집합의 동일성을 강제하므로 여기서 키가 빠질 일은 없다.)
    _sm = {tuple(round(float(x), 9) for x in r['origin_shift_um']): r for r in arms['SBE']}
    _dm = {tuple(round(float(x), 9) for x in r['origin_shift_um']): r for r in arms['DBE']}
    _pa = [_dm[k2]['sigma_e'] / _sm[k2]['sigma_e'] for k2 in sorted(_sm)
           if _sm[k2].get('sigma_e') and _dm[k2].get('sigma_e')]
    if len(_pa) > 1:
        _m = sum(_pa) / len(_pa)
        _sd = math.sqrt(sum((v - _m) ** 2 for v in _pa) / (len(_pa) - 1))
        out['ratio_paired_mean'] = round(_m, 6)
        out['se_ratio_paired_rel_pct'] = round(100.0 * _sd / math.sqrt(len(_pa)) / _m, 4)
        out['se_ratio_paired_pct'] = out['se_ratio_paired_rel_pct']   # ⚠ deprecated 별칭
        out['se_ratio_paired_abs_pp'] = round(_m * 100.0 * _sd / math.sqrt(len(_pa)) / _m, 4)
        out['ratio_arms'] = [round(v, 6) for v in _pa]
        out['se_note'] = ('게이트는 prereg §4 의 hypot 을 쓴다 (보수적).  쌍별 SE 는 참고용 — '
                          '점예측 일치 서술에 쓰지 말 것')
    if se_ratio_rel_pct > SE_MAX_REL_PCT:
        #  ⚠⚠ 2026-08-24 (CDXR3-1) — **절대 %p 를 사유에 적지 않는다.**
        #    `SE_abs = R · SE_rel` 이라 둘을 나란히 내면 **몫으로 R 이 복원된다**.
        #    초판이 정확히 그것을 했다 — 같은 커밋에서 '누설 없음' 을 주장하면서.
        #    절대값은 `out['se_ratio_abs_pp']` 로 JSON 에 남는다 (비-blind 소비자용).
        return dict(out, decision='HOLD', hold_code='SE_EXCEEDED',
                    reason=f'비의 상대 표준오차 {se_ratio_rel_pct:.2f} % > {SE_MAX_REL_PCT} % — '
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
                #  ★ 2026-08-24 (CDXR2-6) — PTFE 규약.  σ_PTFE 만으로는 exact-zero 와
                #    미스탬프가 구분되지 않으므로 규약 자체가 고정 인자다.
                ptfe_stamp='off', ptfe_zero_dof=False,
                #  ★ 2026-08-25 (CDXR3-3) — 현행 세대는 규약 id 를 항상 기록한다.
                physics_protocol_id='p1-testfixture0001', physics_protocol_match=True,
                # ★ 2026-08-19 (A5) — 세대 인자도 픽스처에 싣는다.  안 실으면 위와 같은
                #   이유로 새 게이트가 selftest 에서 **검증된 적 없는 코드**가 된다.
                additive_E_GPa={'VGCF': 10.0, 'PTFE': 0.3, 'SDCP': 23.6},
                sigma_ion_se_S_cm=0.003, sigma_ion_sdcp_S_cm=0.001,
                sigma_am_s_S_cm=0.010, sigma_am_p_S_cm=0.005, cam='nmc811',
                temp_c=25.0, ea_ion_ev=0.29, mpm_seed=3,
                se_E_GPa=1.53, se_nu=0.49, se_sigma_y_GPa=0.30)

    #  ★ 2026-08-20 (CDXIJ-10 ①) — 픽스처가 **origin 을 갖는다**.  팔 계약이 origin 기록·
    #    unique·두 침대 집합 동일을 요구하므로, 없는 픽스처는 (옳게) 전부 HOLD 가 된다.
    def _ori(i):
        return [0.0, 0.0, round(0.01 * i, 9)]

    def mk(sbe, dbe, cg=0, resid=1e-8, **over):
        f = dict(_FIX, **over)
        return {'SBE': [dict(f, file=f'p2_SBE_a{i}.json', sigma_e=v, cg_info=cg,
                             cg_resid=resid, unconverged=False, origin_shift_um=_ori(i))
                        for i, v in enumerate(sbe)],
                'DBE': [dict(f, file=f'p2_DBE_a{i}.json', sigma_e=v, cg_info=cg,
                             cg_resid=resid, unconverged=False, origin_shift_um=_ori(i))
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
        (H0_MIN_RATIO, H1_RATIO, SE_MAX_REL_PCT) == (1.05, 1.015, 1.17)
        and SE_MAX_PCT == SE_MAX_REL_PCT)
    #  ★★ 2026-08-24 (CDXR2-3) — SE 단위.  게이트 입력은 **상대 RSE(%)** 여야 하고
    #    절대 %p 는 파생일 뿐이다.  픽스처를 **판별 구간**에 둔다: 상대 1.12 % 는 문턱
    #    1.17 을 통과하는데 절대 1.2096 %p 는 넘는다 ⇒ 누가 게이트 입력을 절대값으로
    #    바꾸면 이 팔의 판정이 h0 → HOLD 로 **뒤집혀** 검사가 발화한다.
    _ua = 0.0112
    _ub = [1 - 3 * _ua, 1 - 2 * _ua, 1 - _ua, 1.0, 1.0, 1 + _ua, 1 + 2 * _ua, 1 + 3 * _ua]
    _uv = verdict(mk(_ub, [v * 1.08 for v in _ub]))
    chk(f'㉚a ★ 게이트는 **상대 %** 를 쓴다 — 상대 {_uv.get("se_ratio_rel_pct")} % < '
        f'{SE_MAX_REL_PCT} 라 통과 (절대 {_uv.get("se_ratio_abs_pp")} %p 였다면 HOLD): '
        f'{_uv["decision"]}',
        _uv['decision'] == 'h0' and _uv['se_ratio_rel_pct'] < SE_MAX_REL_PCT
        and _uv['se_ratio_abs_pp'] > SE_MAX_REL_PCT)
    chk('㉚b ★ 절대 %p 는 파생 항등식 SE_abs = R · SE_rel 을 만족한다',
        _uv['se_ratio_abs_pp'] == round(_uv['ratio'] * _uv['se_ratio_rel_pct'], 4))
    chk('㉚c deprecated 별칭이 새 키와 같은 값이다 (옛 픽스처·비교기 호환)',
        _uv['se_ratio_pct'] == _uv['se_ratio_rel_pct']
        and _uv.get('se_ratio_paired_pct') == _uv.get('se_ratio_paired_rel_pct'))
    chk('㉚d R < 1 이면 절대 %p 가 상대 % 보다 **작다** (CL-58 이온비가 유일한 보수 사례)',
        (lambda _w: _w['se_ratio_abs_pp'] < _w['se_ratio_rel_pct'])(
            verdict(mk(_ub, [v * 0.9927 for v in _ub]))))
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
    #  ⚠ 2026-08-20 (CDX-IJ-01) — 계약이 **뒤집혔다**.  옛 계약("없으면 False")은 missing
    #    게이트를 원리적으로 무력화했다.  이제 부재는 `None` 으로 보존한다.
    chk(f'⑬ 옛 payload 의 없는 필드는 None 으로 **보존** ({_old["sdcp_yield_to_vgcf"]!r})',
        _old['sdcp_yield_to_vgcf'] is None)
    #  ⑭ PTFE 스탬프 팔(CL-49)이 생산 팔과 섞이면 잡는다 + 옛 payload 는 0.0 정규화
    _mix4 = mk(base, [v * 1.08 for v in base])
    for _r in _mix4['DBE']:
        _r['sigma_ptfe_S_cm'] = 1e-16
    v14 = verdict(_mix4)
    chk(f'⑭ PTFE 스탬프 팔 × 생산 팔 혼합은 HOLD ({v14["decision"]})',
        v14['decision'] == 'HOLD' and 'sigma_ptfe_S_cm' in (v14.get('reason') or ''))
    chk(f'⑭b 옛 payload 의 없는 sigma_ptfe 는 None 으로 **보존** ({_old["sigma_ptfe_S_cm"]!r})',
        _old['sigma_ptfe_S_cm'] is None)
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
    #     ⚠⚠ 2026-08-20 (Codex CDX-IJ-01) — **이 검사를 다시 짰다.**  옛 판은 내부 row 에
    #     `None` 을 직접 넣어 `_read()` 를 **건너뛰었고**, 그래서 `_read` 가 부재를 기본값으로
    #     접던 두 필드(`sdcp_yield_to_vgcf`→False · `sigma_ptfe_S_cm`→0.0)에서 결함을 놓쳤다
    #     (6필드 중 4개만 실제로 닫혀 있었다).  ⇒ 이제 **실제 JSON 파일을 쓰고 collect() 를 거쳐**
    #     한 키씩 지운다 = 생산과 같은 경로.  ("실제 경로를 안 타는 테스트" 부류의 재발 차단.)
    import tempfile as _tf22
    #  ★ 2026-08-20 (Codex 재검증) — 픽스처가 **실제 payload 모양**이어야 한다.
    #    정본 backend 는 `components[c]['backend']` 이고, 이것이 없는 픽스처로는 그 게이트가
    #    검증되지 않는다 (앞선 두 사고와 같은 뿌리 = 실제 경로를 안 타는 픽스처).
    def _comps(elec='gpu', therm='gpu'):
        _bk = lambda u: {'requested': 'gpu', 'used': u,
                         'fallback_reason': None, 'precond': 'jacobi'}
        return {'electronic': {'status': 'complete', 'backend': _bk(elec)},
                'thermal': {'status': 'complete', 'backend': _bk(therm)},
                'ionic': {'status': 'disabled'}}

    _man22 = {'vox_um': 0.15, 'bridge_um': 0.48, 'fibre_stamp': 'segment',
              'sdcp_stamp': 'sphere', 'sdcp_sphere_d_um': 0.30,
              'sigma_vgcf_S_cm': 78.5398, 'sigma_sdcp_S_cm': 250.0,
              'sdcp_yield_to_vgcf': False, 'sigma_ptfe_S_cm': 0.0,
              #  ★ 2026-08-24 (CDXR2-6) — 현행 세대 payload 는 PTFE 규약을 항상 기록한다.
              'ptfe_stamp': 'off', 'ptfe_zero_dof': False,
              'physics_protocol_id': 'p1-testfixture0001', 'physics_protocol_match': True,
              'backend_last_solve': {'requested': 'gpu', 'used': 'gpu',
                                     'fallback_reason': None, 'precond': 'jacobi'},
              'components': _comps()}

    def _write_dir(_d, drop=None):
        """8팔 × 2침대를 **실제 payload JSON** 으로 쓴다.  `drop` 키는 매니페스트에서 뺀다."""
        for _k, _vals in (('SBE', base), ('DBE', [v * 1.12 for v in base])):
            for _i, _v in enumerate(_vals):
                _m = {kk: vv for kk, vv in _man22.items() if kk != drop}
                if drop == 'backend':
                    _m.pop('backend_last_solve', None)
                    _m.pop('components', None)          # 정본을 지워야 진짜 "기록 없음" 이다
                _m['origin_shift_um'] = [0.0, 0.0, _i * 0.01]
                with open(os.path.join(_d, f'p2_{_k}_sph_a{_i}.json'), 'w',
                          encoding='utf-8') as _f:
                    json.dump({'mpm_metrics': {'step3': {
                        'sigma_e_eff_S_cm': _v, 'cg_info': 0, 'cg_resid': 1e-8,
                        'unconverged': False, 'manifest': _m}}}, _f)

    with _tf22.TemporaryDirectory() as _d22:
        _write_dir(_d22)
        _v22ok = verdict(collect(_d22)[1])
        chk(f'㉒ 기준선 — 기록 완비 파일 16개는 판정이 난다 ({_v22ok["decision"]})',
            _v22ok['decision'] in ('h0', 'h1', 'BOTH_REJECTED'))
    for _f in ('sigma_vgcf_S_cm', 'sigma_sdcp_S_cm', 'sdcp_sphere_d_um',
               'backend', 'sdcp_yield_to_vgcf', 'sigma_ptfe_S_cm'):
        with _tf22.TemporaryDirectory() as _d22:
            _write_dir(_d22, drop=_f)
            _v22 = verdict(collect(_d22)[1])
        chk(f'㉒ **실제 JSON** 에서 `{_f}` 키를 지우면 HOLD ({_v22["decision"]})',
            _v22['decision'] == 'HOLD' and _f in (_v22.get('reason') or ''))

    #  ㉓ ★★ 2026-08-20 — `_read` 가 **매니페스트에 실제로 있는 키**를 읽는가.
    #     실사고: `backend` 를 `LAST_BACKEND['backend']` 로 읽었는데 그런 키는 없다
    #     ({requested, used, fallback_reason, precond}) ⇒ 모든 런에서 항상 None →
    #     고정-인자 루프가 skip → **"CuPy 조용한 CPU 폴백을 잡는다" 는 검사가 무발화**.
    #     ⚠ 픽스처를 손으로 짜면 같은 오해를 반복하므로, **payload 가 싣는 dict 모양 그대로**
    #       (`step3_sigma.LAST_BACKEND` 의 키 집합) 쓴다.
    import tempfile as _tf23
    _man23 = {'vox_um': 0.115, 'bridge_um': 0.48, 'fibre_stamp': 'point',
              'sdcp_stamp': 'sphere', 'sdcp_sphere_d_um': 0.30,
              'sigma_vgcf_S_cm': 133.622, 'sigma_sdcp_S_cm': 250.0,
              'sdcp_yield_to_vgcf': False, 'sigma_ptfe_S_cm': 0.0,
              #  ★ 2026-08-24 (CDXR2-6) — 현행 세대 payload 는 PTFE 규약을 항상 기록한다.
              'ptfe_stamp': 'off', 'ptfe_zero_dof': False,
              'physics_protocol_id': 'p1-testfixture0001', 'physics_protocol_match': True,
              'backend_last_solve': {'requested': 'gpu', 'used': 'gpu',
                                     'fallback_reason': None, 'precond': 'jacobi'},
              'components': _comps()}
    with _tf23.TemporaryDirectory() as _d23:
        def _mkp(name, man):
            _p = os.path.join(_d23, name)
            with open(_p, 'w', encoding='utf-8') as _f:
                json.dump({'mpm_metrics': {'step3': {
                    'sigma_e_eff_S_cm': 0.05, 'cg_info': 0, 'cg_resid': 1e-8,
                    'unconverged': False, 'manifest': man}}}, _f)
            return _p
        _r23 = _read(_mkp('p2_DBE_sph_a0.json', _man23))
        chk(f"㉓ `backend` 를 **component 정본**에서 읽는다 ({_r23['backend']!r})",
            _r23['backend'] == {'electronic': 'gpu', 'thermal': 'gpu'})
        #  ★ 음성 대조 — 기록이 **정말** 없으면 여전히 None 이어야 한다 (게이트가 살아야 하므로).
        _r23b = _read(_mkp('p2_DBE_sph_a1.json',
                           {k: v for k, v in _man23.items()
                            if k not in ('backend_last_solve', 'backend', 'components')}))
        chk('㉓ 음성 대조 — 기록이 없으면 None (게이트가 살아 있다)',
            _r23b['backend'] is None)
        #  ★ 그리고 그 None 이 **HOLD 로 이어지는지** — 필드만 읽고 게이트가 안 물면 무의미하다.
        _v23 = verdict(mk(base, [v * 1.08 for v in base], backend=None))
        chk(f"㉓ 그 None 이 HOLD 로 이어진다 ({_v23['decision']})",
            _v23['decision'] == 'HOLD' and 'backend' in (_v23.get('reason') or ''))

    #  ㉔ ★★ 2026-08-20 (Codex 재검증 NEW-DEFECT P1) — **component 별 backend 차이**.
    #     옛 판은 `backend_last_solve`(마지막 solve = thermal) 하나만 읽어, SBE electronic=gpu 인데
    #     DBE electronic=**cpu** 인 경우를 ['gpu'] 로 접고 **h0** 를 냈다.  이 필드가 잡으라고
    #     만들어진 "조용한 CPU 폴백" 이 정확히 그 형태다.
    with _tf22.TemporaryDirectory() as _d24:
        for _k, _vals, _elec in (('SBE', base, 'gpu'),
                                 ('DBE', [v * 1.12 for v in base], 'cpu')):
            for _i, _v in enumerate(_vals):
                _m = dict(_man22, components=_comps(elec=_elec),
                          origin_shift_um=[0.0, 0.0, _i * 0.01])
                with open(os.path.join(_d24, f'p2_{_k}_sph_a{_i}.json'), 'w',
                          encoding='utf-8') as _f:
                    json.dump({'mpm_metrics': {'step3': {
                        'sigma_e_eff_S_cm': _v, 'cg_info': 0, 'cg_resid': 1e-8,
                        'unconverged': False, 'manifest': _m}}}, _f)
        _v24 = verdict(collect(_d24)[1])
    chk(f'㉔ ★ SBE electronic=gpu · DBE electronic=cpu (양쪽 last_solve=gpu) 는 HOLD '
        f'({_v24["decision"]})',
        _v24['decision'] == 'HOLD' and 'backend' in (_v24.get('reason') or ''))

    #  ㉕ ★★ 2026-08-20 (CDXIJ-10, Codex 재검증 §③) — **팔 계약**.  세 mutation 을 그대로.
    _c1 = mk(base[:2], [v * 1.12 for v in base[:2]])
    for _r in _c1['SBE'] + _c1['DBE']:
        _r['origin_shift_um'] = None
    _v25a = verdict(_c1)
    chk(f'㉕a origin 기록이 없으면 HOLD ({_v25a["decision"]})',
        _v25a['decision'] == 'HOLD' and 'origin' in (_v25a.get('reason') or ''))
    _c2 = mk(base, [v * 1.12 for v in base])
    for _i, _r in enumerate(_c2['DBE']):
        _r['origin_shift_um'] = [0.0, 0.0, round(1.0 + 0.01 * _i, 9)]   # disjoint 집합
    _v25b = verdict(_c2)
    chk(f'㉕b ★ 두 침대의 origin 집합이 다르면 HOLD (Codex: 옛 판은 h0) ({_v25b["decision"]})',
        _v25b['decision'] == 'HOLD' and 'origin 집합' in (_v25b.get('reason') or ''))
    _v25c = verdict(mk(base[:2], [v * 1.12 for v in base[:2]]), require_arms=8)
    chk(f'㉕c ★ 2팔뿐인데 8팔을 요구하면 HOLD (Codex: 옛 판은 판정했다) ({_v25c["decision"]})',
        _v25c['decision'] == 'HOLD' and '정확히 8' in (_v25c.get('reason') or ''))
    #  ㉕d ★ 쌍대응을 **origin 으로** 짝짓는가 — 파일명 순서를 뒤집어도 같은 답이어야 한다.
    #  ⚠ 비가 **팔마다 달라야** 판별력이 있다 (상수 비면 SE 가 0 이라 뒤집어도 0).
    _dvar = [v * (1.10 + 0.004 * _i) for _i, v in enumerate(base)]
    _c4 = mk(base, _dvar)
    for _i, _r in enumerate(_c4['DBE']):          # 파일명만 역순, origin 은 그대로
        _r['file'] = f'p2_DBE_z{7 - _i}.json'
    _v25d = verdict(_c4)
    _v25ref = verdict(mk(base, _dvar))
    chk(f'㉕d ★ 파일명 순서를 뒤집어도 쌍대응 SE 가 같다 (파일명 zip 폐기) '
        f'({_v25d.get("se_ratio_paired_pct")} vs {_v25ref.get("se_ratio_paired_pct")})',
        _v25d.get('se_ratio_paired_pct') == _v25ref.get('se_ratio_paired_pct'))
    #  ㉕e ★ 결과 seal — 도핑 판정은 σ_ion 없이 못 낸다 (LEAN=2 산출물 거부).
    _v25e = verdict(mk(base, [v * 1.12 for v in base]), require_ionic=True)
    chk(f'㉕e ★ --require-ionic 인데 σ_ion 이 없으면 HOLD ({_v25e["decision"]})',
        _v25e['decision'] == 'HOLD' and 'σ_ion' in (_v25e.get('reason') or ''))
    #  ★★ ㉛ 2026-08-24 (CDXR2-4) — **이온 수렴 봉인**.  σ_ion 이 *있다*는 것과
    #    *수렴했다*는 것은 다르다.  payload 가 이온 미수렴도 `complete` 로 적었고
    #    (전자 경로만 2026-08-20 에 고쳐졌다 = 같은 결함의 3회차) 게이트는 양의 σ_ion
    #    존재만 봤다 ⇒ 이온축 결론이 false-green 이 될 수 있었다.
    _ig = dict(sigma_ion=5.6e-4, ion_cg_info=0, ion_unconverged=False)     # 봉인된 정상 팔
    _v31a = verdict(mk(base, [v * 1.12 for v in base], **_ig), require_ionic=True)
    chk(f'㉛a 봉인된 수렴 팔은 --require-ionic 을 통과한다 ({_v31a["decision"]})',
        _v31a['decision'] == 'h0')
    _v31b = verdict(mk(base, [v * 1.12 for v in base],
                       **dict(_ig, ion_cg_info=30000, ion_unconverged=True)),
                    require_ionic=True)
    chk(f'㉛b ★ σ_ion 은 있는데 **이온이 미수렴**이면 HOLD (옛 게이트는 통과시켰다): '
        f'{_v31b["decision"]}',
        _v31b['decision'] == 'HOLD' and _v31b.get('ion_unconverged_arms') == 16)
    _v31c = verdict(mk(base, [v * 1.12 for v in base], sigma_ion=5.6e-4), require_ionic=True)
    chk(f'㉛c ★ 봉인 이전 세대(이온 수렴 정보 없음)는 HOLD — fail-open 금지: '
        f'{_v31c["decision"]}',
        _v31c['decision'] == 'HOLD' and _v31c.get('ion_no_convergence_info') == 16)
    #  ★ 음성 대조 — 이온축이 결론이 아니면(플래그 없음) 이온 미수렴이 σ_e 판정을 막지 않는다.
    _v31d = verdict(mk(base, [v * 1.12 for v in base],
                       **dict(_ig, ion_cg_info=30000, ion_unconverged=True)))
    chk(f'㉛d 음성 대조 — --require-ionic 없이는 이온 미수렴이 σ_e 판정을 막지 않는다 '
        f'({_v31d["decision"]})', _v31d['decision'] == 'h0')
    #  ★★ ㉜ 2026-08-24 (CDXR2-5) — **봉인과 판정의 분리**.  러너의 마지막 줄이
    #    `--collect-only` 라 항상 exit 0 이었다.  그렇다고 러너가 판정을 돌리면 이 파일
    #    헤더의 규약("결과를 보고 창을 옮길 수 없게")이 깨진다.  `--seal-only` 는
    #    데이터 상태만 말하고 답은 말하지 않는다 — 그 성질을 여기서 강제한다.
    _sv_ok = verdict(mk(base, [v * 1.12 for v in base]))
    _o1, _l1 = seal_lines(_sv_ok)
    chk(f'㉜a 봉인 통과 시 ok=True ({_sv_ok["decision"]})', _o1 is True)
    _sv_bad = verdict(mk(base, base[:4]))                     # 팔 수 불일치
    _o2, _l2 = seal_lines(_sv_bad)
    chk(f'㉜b 봉인이 깨지면 ok=False ({_sv_bad["decision"]})', _o2 is False)
    _blob = '\n'.join(_l1 + _l2)
    _leak = [t for t in ('h0', 'h1', str(_sv_ok.get('ratio')),
                         str(_sv_ok.get('ratio_paired_mean')))
             if t and t != 'None' and t in _blob.replace(
                 '⚠ h0/h1 과 비는 출력하지 않는다 — 판정은 prereg §5 순서로 따로 돈다', '')]
    chk(f'㉜c ★★ 봉인 출력이 **판정도 비도 누설하지 않는다** (누설: {_leak})', not _leak)
    chk('㉜d 봉인이 깨진 이유는 싣는다 (데이터 상태는 답이 아니다)',
        any('근거' in x for x in _l2) and not any('근거' in x for x in _l1))
    #  ★★ ㉝ 2026-08-24 (CDXR2-6) — **PTFE 규약이 고정 인자다.**  σ_PTFE 만 보던 옛
    #    목록은 exact-zero(σ=0·스탬프 ON)와 미스탬프(σ=0·스탬프 OFF)를 **구분하지 못한다**
    #    — 둘 다 sigma_ptfe_S_cm=0.0 이다.  규약이 갈렸는데 게이트가 통과시키는 형태.
    _pf = dict(ptfe_stamp='off', ptfe_zero_dof=False)
    _v33a = verdict(mk(base, [v * 1.12 for v in base], **_pf))
    chk(f'㉝a 같은 PTFE 규약이면 통과 ({_v33a["decision"]})', _v33a['decision'] == 'h0')
    _mix = mk(base, [v * 1.12 for v in base], **_pf)
    for _r in _mix['DBE']:                                  # DBE 만 exact-zero 로 (규약 혼합)
        _r['ptfe_stamp'] = 'centerline'; _r['ptfe_zero_dof'] = True
    _v33b = verdict(_mix)
    chk(f'㉝b ★★ σ_PTFE 는 같은데 **스탬프 규약이 다르면** HOLD (둘 다 σ=0 이라 옛 '
        f'게이트는 통과시켰다): {_v33b["decision"]}',
        _v33b['decision'] == 'HOLD' and 'ptfe_stamp' in (_v33b.get('reason') or ''))
    _mix2 = mk(base, [v * 1.12 for v in base], **_pf)
    for _r in _mix2['DBE']:
        _r.pop('ptfe_stamp')                                 # 옛 세대 payload (필드 부재)
    _v33c = verdict(_mix2)
    chk(f'㉝c ★ 규약 기록이 **없는** 팔은 HOLD — 부재를 기본값으로 접지 않는다 '
        f'(CDX-IJ-01 의 교훈): {_v33c["decision"]}',
        _v33c['decision'] == 'HOLD')
    #  ★★★ ㉞ 2026-08-24 (CDXR2-7) — **고정 인자의 단일 소스를 강제한다.**
    #    이번 결함의 근본 원인: 같은 목록이 세 곳에 따로 하드코딩돼 있어 `_FIXED_FIELDS` 에
    #    `ptfe_stamp` 를 넣어도 **팔간-차이 루프와 부재 검사 루프는 그대로**였다 —
    #    ㉝b/㉝c 가 그것을 잡았다.  개별 필드 테스트로는 다음 번 추가를 못 막으므로
    #    **구조**를 건다: 두 루프가 `_FIXED_FIELDS` 를 참조해야 하고, 필드 목록 리터럴이
    #    파일에 두 번 나오면 안 된다.
    import os as _os2
    _self = open(_os2.path.abspath(__file__), encoding='utf-8').read()
    chk('㉞a 부재 검사 루프가 _FIXED_FIELDS 를 쓴다 (인라인 튜플 아님)',
        'for fld in _FIXED_FIELDS:' in _self)
    chk('㉞b 팔간-차이 루프가 _FIXED_FIELDS 를 쓴다',
        'for fld in (*_FIXED_FIELDS,' in _self)
    #  ⚠ needle 을 쪼개 만든다 — 통짜로 적으면 이 줄 자신이 두 번째 출현이 된다 (자기참조).
    #  ★★ 2026-08-25 (CDXR3-5) — 이제 **레지스트리 하나**가 정본이므로 구조를 그것으로 건다.
    chk('㉞c ★★ 모든 게이트 목록이 FIELD_CONTRACT 에서 파생된다 (인라인 튜플 없음)',
        'contract_fields(' in _self
        and all(set(_t) <= set(FIELD_CONTRACT)
                for _t in (_FIXED_FIELDS, _REQUIRED_FIELDS, _XDIR_FIELDS, _BED_FIELDS_C)))
    chk('㉞d ★★ cross-dir 이 **세대·침대 인자까지** 본다 (옛 판은 _FIXED_FIELDS 만 봐서 '
        'σ_AM 을 바꿔도 measured 였다)',
        'sigma_am_s_S_cm' in _XDIR_FIELDS and 'additive_E_GPa' in _XDIR_FIELDS
        and 'input_digest' in _XDIR_FIELDS)
    chk('㉞e ★ required 와 across_dir 은 **다른 축**이다 (세대 인자는 없어도 통과, '
        '섞이면 HOLD — 회귀 ⑲ 가 그 계약이다)',
        'sigma_am_s_S_cm' not in _REQUIRED_FIELDS and 'vox' in _REQUIRED_FIELDS)
    chk('㉞f ★ 침대 인자는 팔-간 고정에서 **빠진다** (FA-06: SBE 에 SDCP 가 없는 것은 정상)',
        not (set(_BED_FIELDS_C) & set(_FIXED_FIELDS)))
    #  ★★ 2026-08-25 — **레지스트리가 옛 목록을 전부 담는가**.  이 검사가 없었으면
    #    `code_sha` 누락을 회귀 ㉖c 가 우연히 잡은 것으로 끝났다 (실제로 그랬다).
    #    옛 튜플이 사라진 뒤에도 이 대조는 남는다 — 레지스트리가 **덮개**임을 강제한다.
    chk(f'㉞g ★★ FIELD_CONTRACT 가 옛 _GEN_FIELDS 를 **전부** 담는다 '
        f'(누락: {sorted(set(_GEN_FIELDS) - set(FIELD_CONTRACT))})',
        set(_GEN_FIELDS) <= set(FIELD_CONTRACT))
    #  ★★★ ㊱ 2026-08-25 (CDXR3-3, 종료조건 ③④) — **요청↔적용 규약 봉인**.
    #    Codex: "`_ptscenterline` OUTDIR 에서 모든 arm 이 조용히 `off` 로 실행돼도
    #    서로만 같으면 초록이 될 수 있다."  규약 id 를 팔끼리 비교하는 것만으로는
    #    **러너가 무엇을 요청했는지** 모른다.
    _v36a = verdict(mk(base, [v * 1.12 for v in base], physics_protocol_match=False))
    chk(f'㊱a ★★ 요청↔적용 규약이 **다른** 팔이 있으면 HOLD (팔끼리는 같아도) '
        f'{_v36a["decision"]}/{_v36a.get("hold_code")}',
        _v36a['decision'] == 'HOLD' and _v36a.get('hold_code') == 'PROTOCOL_MISMATCH')
    _v36b = verdict(mk(base, [v * 1.12 for v in base],
                       physics_protocol_id='unknown:vox_um,bridge_um'))
    chk(f'㊱b ★ 규약을 **확정할 수 없으면** HOLD (필드가 빠졌다) '
        f'{_v36b["decision"]}/{_v36b.get("hold_code")}',
        _v36b['decision'] == 'HOLD' and _v36b.get('hold_code') == 'PROTOCOL_UNKNOWN')
    _mix36 = mk(base, [v * 1.12 for v in base])
    for _r36 in _mix36['DBE']:
        _r36['physics_protocol_id'] = 'p1-otherprotocol01'    # 규약이 갈린 팔
    _v36c = verdict(_mix36)
    chk(f'㊱c ★ 규약 id 가 팔마다 다르면 HOLD ({_v36c["decision"]})',
        _v36c['decision'] == 'HOLD' and 'physics_protocol_id' in (_v36c.get('reason') or ''))
    _v36d = verdict(mk(base, [v * 1.12 for v in base]))
    chk(f'㊱d 음성 대조 — 규약이 일치하면 통과 ({_v36d["decision"]})',
        _v36d['decision'] == 'h0')
    #  ★ payload 쪽 파생이 **결정론적이고 값에 반응하는가** (선언 라벨이 아니라 결과).
    import importlib.util as _iu36, os as _os36
    _sp36 = _iu36.spec_from_file_location(
        'p36', _os36.path.join(_os36.path.dirname(_os36.path.abspath(__file__)),
                               'mpm_webapp_payload.py'))
    _p36 = _iu36.module_from_spec(_sp36)
    _sp36.loader.exec_module(_p36)
    _man36 = {k: 1.0 for k in _p36.PROTOCOL_FIELDS}
    _id1 = _p36.physics_protocol_id(_man36)
    _id2 = _p36.physics_protocol_id(dict(_man36, vox_um=0.125))
    chk(f'㊱e ★ 규약 id 가 인자에 **반응한다** (vox 만 바꿔도 달라진다) {_id1[:10]} vs {_id2[:10]}',
        _id1 != _id2 and _id1.startswith('p1-'))
    chk('㊱f ★ 같은 인자면 같은 id (결정론)',
        _p36.physics_protocol_id(dict(_man36)) == _id1)
    _man36b = dict(_man36)
    _man36b.pop('vox_um')
    chk('㊱g ★★ 인자가 **빠지면** `unknown:` 을 낸다 (임의 기본값으로 채우지 않는다)',
        _p36.physics_protocol_id(_man36b).startswith('unknown:vox_um'))
    #  ★★★ ㉟ 2026-08-25 (CDXR3-1/4) — **Codex 가 재현한 false-green 을 상주 회귀로**.
    #    초판의 ㉜c 는 `seal_lines()` 반환 문자열만 검사해서 CLI preamble·옵션 우선순위·
    #    SE 역산을 전부 놓쳤다 = 이 리포가 여러 번 겪은 "실제 경로를 안 타는 테스트".
    #    ⇒ 여기서는 **CLI 를 subprocess 로 실제 실행**하고 stdout·exit code 를 본다.
    import subprocess as _sp, tempfile as _tf, json as _js, os as _os3, sys as _sys3
    _me = _os3.path.abspath(__file__)

    def _write_arms(_d, n=8, mul=1.12, **s3over):
        _man = {k: v for k, v in _FIX.items()
                if k not in ('sigma_e_eff_S_cm',)}
        for _b, _m in (('SBE', 1.0), ('DBE', mul)):
            for _i in range(n):
                _s3 = {'sigma_e_eff_S_cm': 0.073 * _m * (1 + 0.001 * _i),
                       'cg_info': 0, 'cg_resid': 1e-9, 'unconverged': False,
                       'status': 'complete',
                       'manifest': dict({'vox_um': _FIX['vox'],
                                         'origin_shift_um': [0.0, 0.0, round(0.01 * _i, 9)],
                                         'components': {'electronic': {'status': 'complete'}}},
                                        **{k: v for k, v in _FIX.items() if k != 'vox'})}
                _s3.update(s3over)
                with open(_os3.path.join(_d, f'p2_{_b}_a{_i}.json'), 'w', encoding='utf-8') as _f:
                    _js.dump({'step3': _s3}, _f)

    def _cli(_d, *args):
        _r = _sp.run([_sys3.executable, _me, '--dir', _d, *args],
                     capture_output=True, text=True)
        return _r.returncode, _r.stdout + _r.stderr

    with _tf.TemporaryDirectory() as _d35:
        _write_arms(_d35)
        _rc, _o = _cli(_d35, '--seal-only', '--collect-only', '--require-arms', '8')
        chk(f'㉟a ★★ `--seal-only --collect-only` 는 **거부**된다 (옛 판은 collect 가 먼저 '
            f'돌아 exit 0 + raw 출력 + 봉인 미실행이었다): rc={_rc}',
            _rc != 0 and '같이 못 쓴다' in _o)
        _rc2, _o2 = _cli(_d35, '--seal-only', '--require-arms', '8')
        _leak = [t for t in ('0.073', '0.0817', 'σ_e', 'h0', 'h1')
                 if t in _o2.replace('h0/h1 과 비는 출력하지 않는다', '')]
        chk(f'㉟b ★★ 봉인 모드 CLI stdout 에 **팔 표·σ 원값이 없다** (누설: {_leak}) rc={_rc2}',
            not _leak)
        _rc3, _o3 = _cli(_d35, '--collect-only')
        chk('㉟c 음성 대조 — collect 모드는 여전히 표를 찍는다 (과잉차단 아님)',
            _rc3 == 0 and 'σ_e' in _o3)

    #  ── SE HOLD 사유의 역산 누설 (SE_abs = R · SE_rel) ──
    _ua2 = 0.02                                              # 상대 SE 를 문턱 위로
    _ub2 = [1 - 3 * _ua2, 1 - 2 * _ua2, 1 - _ua2, 1.0, 1.0, 1 + _ua2, 1 + 2 * _ua2, 1 + 3 * _ua2]
    _vse = verdict(mk(_ub2, [v * 1.08 for v in _ub2]))
    chk(f'㉟d SE 초과가 HOLD 이고 코드가 붙는다 ({_vse.get("hold_code")})',
        _vse['decision'] == 'HOLD' and _vse.get('hold_code') == 'SE_EXCEEDED')
    chk('㉟e ★★ HOLD 사유에 **절대 %p 가 없다** — 상대와 나란히 내면 몫으로 R 이 복원된다',
        '%p' not in (_vse.get('reason') or '')
        and _vse.get('se_ratio_abs_pp') is not None)      # JSON 에는 남는다

    #  ── 이온 수렴 쌍의 모순·반쪽 (Codex 실측 재현) ──
    _ig2 = dict(sigma_ion=5.6e-4)
    _v35f = verdict(mk(base, [v * 1.12 for v in base],
                       **dict(_ig2, ion_cg_info=30000, ion_unconverged=False)),
                    require_ionic=True)
    chk(f'㉟f ★★ `cg_info=30000` 인데 `unconverged=False` = **모순** → HOLD '
        f'(옛 판은 h0): {_v35f["decision"]}/{_v35f.get("hold_code")}',
        _v35f['decision'] == 'HOLD' and _v35f.get('hold_code') == 'IONIC_UNCONVERGED')
    _half = mk(base, [v * 1.12 for v in base], **dict(_ig2, ion_cg_info=0))
    for _k2 in _half:
        for _r2 in _half[_k2]:
            _r2['ion_unconverged'] = None                     # 반쪽
    _v35g = verdict(_half, require_ionic=True)
    chk(f'㉟g ★ 한쪽만 있는 쌍(반쪽)도 HOLD (옛 판은 h0): {_v35g["decision"]}',
        _v35g['decision'] == 'HOLD')
    _v35h = verdict(mk(base, [v * 1.12 for v in base],
                       **dict(_ig2, ion_cg_info=0, ion_unconverged=False, ion_resid=float('nan'))),
                    require_ionic=True)
    chk(f'㉟h ★ residual 이 비유한이면 HOLD: {_v35h["decision"]}',
        _v35h['decision'] == 'HOLD')
    _v35i = verdict(mk(base, [v * 1.12 for v in base],
                       **dict(_ig2, ion_cg_info=0, ion_unconverged=False, ion_resid=2.2e-9)),
                    require_ionic=True)
    chk(f'㉟i 음성 대조 — 일관된 좋은 쌍은 통과 ({_v35i["decision"]})',
        _v35i['decision'] == 'h0')

    #  ㉖ ★★ CDXIJ-10 ③ — 입력 digest · code SHA.
    _dig = dict(input_digest='abc123def4567890', code_sha='1da6cbd')
    _c6 = mk(base, [v * 1.12 for v in base], **_dig)
    #  ⚠⚠ 2026-08-20 (FA-06) — **이 블록의 전제가 틀려 있었다.**  어제 판은 두 침대에 **같은**
    #    digest 를 주고 "통과", 침대끼리 **다르면** "HOLD" 를 기대했다.  그런데 SBE 와 DBE 는
    #    서로 다른 침대이므로 digest 가 **다른 것이 정상**이고 같은 것이 배선 실수다.
    #    ⇒ 어제의 테스트가 오히려 결함을 박제하고 있었다 (실런이 드러냈다: 도핑 baseline HOLD).
    #    올바른 계약: **침대 안에서는 같고, 침대 사이에서는 다르다.**
    def _perbed(c, s='aaa1111111111111', d='bbb2222222222222'):
        for _r in c['SBE']:
            _r['input_digest'] = s
        for _r in c['DBE']:
            _r['input_digest'] = d
        return c

    _c6 = _perbed(_c6)
    chk(f'㉖a 침대별 digest 가 침대 안에서 일정하면 통과 '
        f'({verdict(_c6, require_digest=True)["decision"]})',
        verdict(_c6, require_digest=True)['decision'] in ('h0', 'h1', 'BOTH_REJECTED'))
    _c6b = _perbed(mk(base, [v * 1.12 for v in base], **_dig))
    _c6b['DBE'][3]['input_digest'] = 'ffffffffffffffff'   # 한 팔만 다른 침대를 읽었다
    _v26b = verdict(_c6b)
    chk(f'㉖b ★ **한 침대 안에서** digest 가 갈리면 HOLD ({_v26b["decision"]})',
        _v26b['decision'] == 'HOLD' and 'input_digest' in (_v26b.get('reason') or ''))
    _v26b2 = verdict(_perbed(mk(base, [v * 1.12 for v in base], **_dig),
                             s='same0000same0000', d='same0000same0000'))
    chk(f'㉖b2 ★ 두 침대의 digest 가 **같으면** HOLD (같은 침대다) ({_v26b2["decision"]})',
        _v26b2['decision'] == 'HOLD' and 'input_digest' in (_v26b2.get('reason') or ''))
    _c6c = _perbed(mk(base, [v * 1.12 for v in base], **_dig))
    for _r in _c6c['SBE']:
        _r['code_sha'] = 'deadbee'                   # 다른 코드로 돈 팔
    _v26c = verdict(_c6c)
    chk(f'㉖c ★ code SHA 가 다르면 HOLD ({_v26c["decision"]})',
        _v26c['decision'] == 'HOLD' and 'code_sha' in (_v26c.get('reason') or ''))
    _v26d = verdict(mk(base, [v * 1.12 for v in base]), require_digest=True)
    chk(f'㉖d ★ --require-digest 인데 기록이 없으면 HOLD (옛 payload) ({_v26d["decision"]})',
        _v26d['decision'] == 'HOLD' and 'input_digest' in (_v26d.get('reason') or ''))
    _c6e = _perbed(mk(base, [v * 1.12 for v in base], code_sha='1da6cbd+dirty'))
    _v26e = verdict(_c6e, require_digest=True)
    chk(f'㉖e ★ 커밋 안 된 코드(+dirty)로 돈 런은 HOLD ({_v26e["decision"]})',
        _v26e['decision'] == 'HOLD' and 'dirty' in (_v26e.get('reason') or ''))
    #  ── ㉗ 대조쌍 검증 (CL-45) — **두 디렉터리를 빼는** 실험의 최소 계약 ────────────────
    #     prereg v3 STEP 5 에서 실제로 일어난 일: 대조가 **다른 σ_VGCF** 로 돈 디렉터리였고
    #     아무 게이트도 안 걸려 **거짓 경보**가 났다.  판정기의 고정-인자 검사가 *한 디렉터리
    #     안*만 봤기 때문이다.  ⇒ 그 검사를 도구로 만들고 음성 대조를 상주시킨다.
    def _mk2(d, *, yvgcf, sig_vgcf=11.0447, dig=('AA', 'BB'), n=2, dbe_mul=1.42, **_gen):
        _m0 = {'vox_um': 0.4, 'bridge_um': 0.48, 'fibre_stamp': 'segment',
               'sdcp_stamp': 'point', 'sdcp_sphere_d_um': 0.0,
               'sigma_vgcf_S_cm': sig_vgcf, 'sigma_sdcp_S_cm': 250.0,
               'sdcp_yield_to_vgcf': yvgcf, 'sigma_ptfe_S_cm': 0.0,
               'ptfe_stamp': 'off', 'ptfe_zero_dof': False,
               'physics_protocol_id': 'p1-testfixture0001', 'physics_protocol_match': True,
               'code_sha': 'abc1234', 'components': _comps()}
        _m0.update(_gen)                        # 세대 인자 노브 (㉗e/f 용)
        for _k, _mul, _dg in (('SBE', 1.0, dig[0]), ('DBE', dbe_mul, dig[1])):
            for _i in range(n):
                _m = dict(_m0, origin_shift_um=[0.0, 0.0, _i * 0.01], input_digest=_dg)
                with open(os.path.join(d, f'p2_{_k}_a{_i}.json'), 'w', encoding='utf-8') as _f:
                    json.dump({'mpm_metrics': {'step3': {
                        'sigma_e_eff_S_cm': 0.4448190919120597 * _mul, 'cg_info': 0,
                        'cg_resid': 1e-8, 'unconverged': False, 'manifest': _m}}}, _f)

    _EXP = {'sdcp_yield_to_vgcf'}
    with _tf22.TemporaryDirectory() as _A, _tf22.TemporaryDirectory() as _B:
        _mk2(_A, yvgcf=False, dbe_mul=1.42)          # 대조 = 생산 규약
        _mk2(_B, yvgcf=True, dbe_mul=1.29)           # 실험 = σ-치환 OFF
        _c = compare_dirs(_A, _B, _EXP)
        chk(f'㉗a 정상 증인 — 한 축만 다르면 measured ({_c["decision"]})',
            _c['decision'] == 'measured')
        chk(f'㉗a 감소율 산술이 맞다 ({_c.get("reduction_pct")})',
            _c['decision'] == 'measured'
            and abs(_c['reduction_pct'] - (0.42 - 0.29) / 0.42 * 100) < 0.5)
    #  ★ STEP 5 거짓 경보 재현 — 대조가 다른 σ_VGCF 로 돌았다
    with _tf22.TemporaryDirectory() as _A, _tf22.TemporaryDirectory() as _B:
        _mk2(_A, yvgcf=False, sig_vgcf=11.0447)
        _mk2(_B, yvgcf=True, sig_vgcf=78.5398)
        _c = compare_dirs(_A, _B, _EXP)
        chk(f'㉗b ★ 등록 밖 인자(σ_VGCF)가 다르면 HOLD — STEP 5 거짓 경보 재현 ({_c["decision"]})',
            _c['decision'] == 'HOLD' and 'sigma_vgcf_S_cm' in (_c.get('reason') or ''))
    #  ★ 노브가 안 걸린 경우 — "감소율 0 %" 는 물리가 아니다
    with _tf22.TemporaryDirectory() as _A, _tf22.TemporaryDirectory() as _B:
        _mk2(_A, yvgcf=False)
        _mk2(_B, yvgcf=False)
        _c = compare_dirs(_A, _B, _EXP)
        chk(f'㉗c ★ 등록 축이 두 디렉터리에서 **같으면** HOLD (실험이 안 일어났다) ({_c["decision"]})',
            _c['decision'] == 'HOLD' and 'sdcp_yield_to_vgcf' in (_c.get('reason') or ''))
    #  ★★★ ㉗e/f 2026-08-25 (CDXR3-5) — **Codex 가 통과시킨 cross-dir mutant**.
    #    옛 `compare_dirs` 는 `_FIXED_FIELDS` 만 봐서 **세대 인자가 두 디렉터리 사이에서
    #    자유롭게 달라져도 `measured`** 를 냈다 (Codex 실측: σ_AM 0.010 → 0.020).
    with _tf22.TemporaryDirectory() as _A, _tf22.TemporaryDirectory() as _B:
        _mk2(_A, yvgcf=False, dbe_mul=1.42, sigma_am_s_S_cm=0.010)
        _mk2(_B, yvgcf=True, dbe_mul=1.29, sigma_am_s_S_cm=0.020)   # 등록 밖 세대 인자
        _c = compare_dirs(_A, _B, _EXP)
        chk(f'㉗e ★★ 세대 인자(σ_AM)가 cross-dir 로 다르면 HOLD — 옛 판은 measured '
            f'({_c["decision"]})',
            _c['decision'] == 'HOLD' and 'sigma_am_s_S_cm' in (_c.get('reason') or ''))
    with _tf22.TemporaryDirectory() as _A, _tf22.TemporaryDirectory() as _B:
        _mk2(_A, yvgcf=False, dbe_mul=1.42, additive_E_GPa={'SDCP': 23.6})
        _mk2(_B, yvgcf=True, dbe_mul=1.29, additive_E_GPa={'SDCP': 9.0})   # CL-56 세대
        _c = compare_dirs(_A, _B, _EXP)
        chk(f'㉗f ★★ 침대 세대(additive_E_GPa, CL-56)가 cross-dir 로 다르면 HOLD '
            f'({_c["decision"]})',
            _c['decision'] == 'HOLD' and 'additive_E_GPa' in (_c.get('reason') or ''))
    #  ★ 침대가 다르다 — 경로·이름은 증거가 아니다
    with _tf22.TemporaryDirectory() as _A, _tf22.TemporaryDirectory() as _B:
        _mk2(_A, yvgcf=False, dig=('AA', 'BB'))
        _mk2(_B, yvgcf=True, dig=('AA', 'ZZ'))
        _c = compare_dirs(_A, _B, _EXP)
        chk(f'㉗d ★ `input_digest` 가 다르면 HOLD (같은 침대가 아니다) ({_c["decision"]})',
            _c['decision'] == 'HOLD' and 'input_digest' in (_c.get('reason') or ''))
    #  ★ 짝이 안 맞는다
    with _tf22.TemporaryDirectory() as _A, _tf22.TemporaryDirectory() as _B:
        _mk2(_A, yvgcf=False, n=2)
        _mk2(_B, yvgcf=True, n=3)
        _c = compare_dirs(_A, _B, _EXP)
        chk(f'㉗e ★ origin 집합이 다르면 HOLD (짝 없이 못 뺀다) ({_c["decision"]})',
            _c['decision'] == 'HOLD' and 'origin' in (_c.get('reason') or ''))

    #  ── ㉘ `--scan` — 디렉터리 이름을 **짓지 말고 찾는다** ──────────────────────────
    #     실사고 3회: 이름이 인자에서 조립되는데(`vox{V}{_sph}{_bNNN}{_sgN}{_lean}`) 사람이
    #     손으로 재조립해 `--dir` 에 넣었고, 셋 다 "0 팔 → HOLD" 로 끝났다.  그 HOLD 는
    #     **데이터가 나쁘다는 뜻으로 읽힌다** = 존재하지 않는 경로가 실패로 위장한다.
    with _tf22.TemporaryDirectory() as _sr:
        os.makedirs(os.path.join(_sr, 'prereg_v2_vox015_sph_b048_lean'))
        os.makedirs(os.path.join(_sr, 'noise_dir'))          # p2_*.json 없음 → 안 잡혀야
        _mk2(os.path.join(_sr, 'prereg_v2_vox015_sph_b048_lean'), yvgcf=False, n=2)
        _sc = scan(_sr)
        chk(f'㉘a `--scan` 이 결과 디렉터리만 찾는다 ({len(_sc)}개)',
            len(_sc) == 1 and _sc[0][0] == 'prereg_v2_vox015_sph_b048_lean')
        chk(f'㉘b 팔 수를 보고한다 ({_sc[0][1]})', _sc[0][1] == '2/2')
        chk('㉘c ★ 빈/무관 디렉터리는 목록에 안 뜬다 (없는 경로를 고르게 두지 않는다)',
            all(r[0] != 'noise_dir' for r in _sc))

    #  ── ㉙ FA-06 — **침대 정체성 필드**를 침대 사이에서 비교하면 안 된다 ────────────────
    #     실사고 (2026-08-20): 도핑 baseline 8팔이 `additive_E_GPa` 로 HOLD 를 맞았다.
    #     SBE `{PTFE, VGCF}` vs DBE `{PTFE, SDCP, VGCF}` — SBE 에 SDCP 가 없는 것은
    #     **위반이 아니라 이 실험의 독립변수 그 자체**다.  게이트가 실험을 결함으로 신고했다.
    def _mk3(d, *, s_add, d_add, s_dig='AA', d_dig='BB', n=2, s_add2=None, d_add2=None):
        _m0 = {'vox_um': 0.15, 'bridge_um': 0.48, 'fibre_stamp': 'segment',
               'sdcp_stamp': 'sphere', 'sdcp_sphere_d_um': 0.30,
               'sigma_vgcf_S_cm': 78.5398, 'sigma_sdcp_S_cm': 250.0,
               'sdcp_yield_to_vgcf': False, 'sigma_ptfe_S_cm': 0.0,
               #  ★ 2026-08-24 (CDXR2-6) — 현행 세대 payload 는 PTFE 규약을 항상 기록한다.
               'ptfe_stamp': 'off', 'ptfe_zero_dof': False,
               'physics_protocol_id': 'p1-testfixture0001', 'physics_protocol_match': True,
               'code_sha': 'abc1234', 'components': _comps()}
        for _k, _mul, _ad, _ad2, _dg in (('SBE', 1.0, s_add, s_add2, s_dig),
                                         ('DBE', 1.12, d_add, d_add2, d_dig)):
            for _i in range(n):
                _m = dict(_m0, origin_shift_um=[0.0, 0.0, _i * 0.075],
                          input_digest=_dg,          # ← additive 와 **분리** (한 번에 하나만)
                          additive_E_GPa=(_ad if _i == 0 or _ad2 is None else _ad2))
                with open(os.path.join(d, f'p2_{_k}_sph_a{_i}.json'), 'w', encoding='utf-8') as _f:
                    json.dump({'mpm_metrics': {'step3': {
                        'sigma_e_eff_S_cm': 0.073 * _mul, 'cg_info': 0, 'cg_resid': 1e-8,
                        'unconverged': False, 'manifest': _m}}}, _f)

    _SB = {'PTFE': 0.3, 'VGCF': 10.0}
    _DB = {'PTFE': 0.3, 'SDCP': 23.6, 'VGCF': 10.0}
    with _tf22.TemporaryDirectory() as _d29:
        _mk3(_d29, s_add=_SB, d_add=_DB)
        _v = verdict(collect(_d29)[1])
        chk(f'㉙a ★ 정상 증인 — SBE 에 SDCP 항목이 없는 것은 **정상**이다 ({_v["decision"]})',
            _v['decision'] != 'HOLD')
    with _tf22.TemporaryDirectory() as _d29:                       # DBE 안에서 SDCP E 가 섞임
        _mk3(_d29, s_add=_SB, d_add=_DB, d_add2={'PTFE': 0.3, 'SDCP': 9.0, 'VGCF': 10.0})
        _v = verdict(collect(_d29)[1])
        chk(f'㉙b ★ 침대 **안에서** SDCP E 23.6↔9.0 이 섞이면 HOLD (CL-56 축 보존) ({_v["decision"]})',
            _v['decision'] == 'HOLD' and 'additive_E_GPa' in (_v.get('reason') or ''))
    with _tf22.TemporaryDirectory() as _d29:                       # 공통 상의 물성이 다름
        _mk3(_d29, s_add=_SB, d_add={'PTFE': 0.3, 'SDCP': 23.6, 'VGCF': 12.0})
        _v = verdict(collect(_d29)[1])
        chk(f'㉙c ★ 두 침대의 **공통 상**(VGCF) 물성이 다르면 HOLD (세대 혼합) ({_v["decision"]})',
            _v['decision'] == 'HOLD' and '공통 상' in (_v.get('reason') or ''))
    with _tf22.TemporaryDirectory() as _d29:                       # 두 침대가 같은 파일
        _mk3(_d29, s_add=_SB, d_add=_DB, s_dig='SAME', d_dig='SAME')
        _v = verdict(collect(_d29)[1])
        chk(f'㉙d ★ 두 침대의 digest 가 **같으면** HOLD (같은 침대를 읽고 있다) ({_v["decision"]})',
            _v['decision'] == 'HOLD' and 'input_digest' in (_v.get('reason') or ''))

    #  ㉖f 음성 대조 — 옛 격자 팔(전부 없음)은 **기본 모드에서 통과해야** 한다.
    chk('㉖f 옛 팔(digest 전부 없음)은 기본 모드에서 통과 (진행 중 스윕을 안 죽인다)',
        verdict(mk(base, [v * 1.12 for v in base]))['decision'] == 'h0')

    print(f'\nsdcp_gain_verdict selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


#: 두 팔이 **고정**이어야 하는 인자 (한 디렉터리 안에서도, 두 디렉터리 사이에서도).


def _canon(v):
    return json.dumps(v, sort_keys=True) if isinstance(v, (dict, list)) else v


def compare_dirs(dir_a, dir_b, expect_differ):
    """두 디렉터리를 **한 축만 다른 대조쌍**으로 검증하고 이득 감소율을 낸다.

    ★★ 왜 (2026-08-20, CL-45): 감소율은 **두 디렉터리를 빼서** 나오는데, 판정기의 고정-인자
      게이트는 여태 *한 디렉터리 안*만 봤다.  그래서 다른 σ_VGCF 로 돈 디렉터리를 대조로 삼아도
      아무도 안 막았다 — 실제로 prereg v3 STEP 5 에서 그 일이 일어나 **거짓 경보**가 났다
      (CLAUDE.md "잡은 결함 2건").  ⇒ 그 검사를 도구로 만든다.

    강제하는 것 넷:
      ⓐ 두 디렉터리의 (침대, origin) 집합이 같다 — 짝이 없으면 뺄 수 없다
      ⓑ 짝마다 `input_digest` 가 같다 = **같은 침대**라는 기계 증거 (경로·이름은 증거가 아니다)
      ⓒ `expect_differ` 밖의 모든 고정 인자가 같다 — 하나라도 다르면 HOLD (STEP 5 재발 방지)
      ⓓ `expect_differ` 가 **실제로 다르다** — 같으면 노브가 안 걸린 것이고, 그때 나오는
         "감소율 0 %" 는 물리가 아니라 **실험이 안 일어났다**는 뜻이다 (fail-closed)
    """
    out = {'dir_a': dir_a, 'dir_b': dir_b, 'expect_differ': sorted(expect_differ)}
    _, arms_a = collect(dir_a)
    _, arms_b = collect(dir_b)
    pairs, differed = [], set()
    for bed in ('SBE', 'DBE'):
        ka = {tuple(round(float(x), 9) for x in (r.get('origin_shift_um') or [])): r
              for r in arms_a[bed] if r.get('origin_shift_um')}
        kb = {tuple(round(float(x), 9) for x in (r.get('origin_shift_um') or [])): r
              for r in arms_b[bed] if r.get('origin_shift_um')}
        if not ka or not kb:
            return dict(out, decision='HOLD',
                        reason=f'{bed} 팔이 한쪽 디렉터리에 없다 (A {len(ka)} · B {len(kb)}) — '
                               f'origin 기록이 없는 옛 팔이면 다시 돌릴 것')
        if set(ka) != set(kb):
            return dict(out, decision='HOLD',
                        reason=f'{bed} 의 origin 집합이 두 디렉터리에서 다르다 — '
                               f'A 전용 {len(set(ka) - set(kb))}개 · B 전용 {len(set(kb) - set(ka))}개.  '
                               f'짝이 없는 팔로는 감소율을 정의할 수 없다')
        for key in sorted(ka):
            ra, rb = ka[key], kb[key]
            for fld in ('input_digest',):
                if ra.get(fld) is None or rb.get(fld) is None:
                    return dict(out, decision='HOLD',
                                reason=f'`{fld}` 가 없는 팔이 있다 ({ra["file"]} / {rb["file"]}) — '
                                       f'같은 침대라는 증거가 없다.  현행 payload 로 다시 돌릴 것 '
                                       f'(CDXIJ-10 ③)')
                if _canon(ra[fld]) != _canon(rb[fld]):
                    return dict(out, decision='HOLD',
                                reason=f'{bed} {key} 의 `{fld}` 가 두 디렉터리에서 다르다 '
                                       f'({ra[fld]} vs {rb[fld]}) — **같은 침대가 아니다**.  '
                                       f'감소율은 침대가 같을 때만 뜻이 있다')
            #  ★★ 2026-08-25 (CDXR3-5) — **`_XDIR_FIELDS`** 를 쓴다.  옛 판은
            #    `_FIXED_FIELDS` 만 봐서 세대 인자(σ_AM·σ_ion·온도·침대 E)가 두 디렉터리
            #    사이에서 **자유롭게 달라져도 `measured`** 를 냈다 (Codex 실측).
            for fld in _XDIR_FIELDS:
                same = _canon(ra.get(fld)) == _canon(rb.get(fld))
                if fld in expect_differ:
                    if not same:
                        differed.add(fld)
                elif not same:
                    return dict(out, decision='HOLD',
                                reason=f'{bed} {key} 에서 고정 인자 `{fld}` 가 두 디렉터리 사이에 '
                                       f'다르다 ({ra.get(fld)} vs {rb.get(fld)}) — 대조쌍은 '
                                       f'`{sorted(expect_differ)}` **하나만** 달라야 한다.  '
                                       f'prereg v3 STEP 5 가 정확히 이것으로 거짓 경보를 냈다')
        pairs.append((bed, ka, kb))
    _no = sorted(set(expect_differ) - differed)
    if _no:
        return dict(out, decision='HOLD',
                    reason=f'`{_no}` 가 두 디렉터리에서 **같다** — 노브가 안 걸렸다.  '
                           f'이때 나오는 감소율 0 % 는 물리가 아니라 실험이 일어나지 않았다는 뜻이다')

    def _ratio(arms_x):
        sm = {tuple(round(float(x), 9) for x in r['origin_shift_um']): r for r in arms_x['SBE']}
        dm = {tuple(round(float(x), 9) for x in r['origin_shift_um']): r for r in arms_x['DBE']}
        rs = [dm[k]['sigma_e'] / sm[k]['sigma_e'] for k in sorted(sm)
              if sm[k].get('sigma_e') and dm[k].get('sigma_e')]
        return (sum(rs) / len(rs), len(rs)) if rs else (None, 0)

    (ra_, na), (rb_, nb) = _ratio(arms_a), _ratio(arms_b)
    if not ra_ or not rb_:
        return dict(out, decision='HOLD', reason='σ_e 가 없는 팔이 있어 비를 낼 수 없다')
    ga, gb = ra_ - 1.0, rb_ - 1.0
    out.update({'n_pair': na, 'ratio_a': ra_, 'ratio_b': rb_, 'gain_a': ga, 'gain_b': gb,
                'reduction_pct': (ga - gb) / ga * 100.0 if ga else None,
                'decision': 'measured',
                'reason': f'대조쌍 검증 통과 — `{sorted(differed)}` 만 다르고 나머지 고정 인자와 '
                          f'침대 digest 는 짝마다 동일 ({na} 쌍)'})
    return out


def scan(root):
    """`root` 아래의 결과 디렉터리를 전부 훑어 **무엇이 어디 있는지** 표로 낸다.

    ★★ 왜 (2026-08-20): 디렉터리 이름이 `prereg_v2_vox{V}{_sph}{_bNNN}{_sgN}{_yvgcf}{_ptfeN}{_leanN}`
      로 **인자에서 조립**되는데, 사람이 그것을 손으로 재조립해 `--dir` 에 넣고 있었다.  세 번
      틀렸고 세 번 다 "0 팔" 로 조용히 끝났다 — 존재하지 않는 경로에 대고 판정을 요청하면
      HOLD 가 나오는데, 그 HOLD 는 **데이터가 나쁘다는 뜻으로 읽힌다**.  ⇒ 이름을 짓지 말고 **찾는다**.
    """
    import glob as _g
    rows = []
    for d in sorted(_g.glob(os.path.join(root, '*'))):
        if not os.path.isdir(d) or not _g.glob(os.path.join(d, 'p2_*.json')):
            continue
        try:
            _, arms = collect(d)
        except Exception:                                          # noqa: BLE001
            rows.append((os.path.basename(d), '읽기 실패', '', '', '', '', '', ''))
            continue
        allr = arms['SBE'] + arms['DBE']
        _u = lambda f: sorted({str(r.get(f)) for r in allr if r.get(f) is not None}) or ['—']
        bad = sum(1 for r in allr if r.get('unconverged') or r.get('cg_info'))
        ion = sum(1 for r in allr if isinstance(r.get('sigma_ion'), (int, float)))
        #  ⚠ 2026-08-20 — 초판은 `sdcp_stamp` 만 보여줬고, 내가 그것을 게이트 ⑤ 의 축
        #    (`fibre_stamp` = VGCF 섬유 점↔선분)으로 **오독**했다.  둘 다 보여준다.
        rows.append((os.path.basename(d), f"{len(arms['SBE'])}/{len(arms['DBE'])}",
                     '/'.join(_u('vox')), '/'.join(_u('fibre_stamp')),
                     '/'.join(_u('sdcp_stamp')), '/'.join(_u('sigma_vgcf_S_cm')),
                     f'{ion}/{len(allr)}', f'{bad} 미수렴' if bad else '✓'))
    return rows


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--scan', default='',
                    help='이 디렉터리 아래의 결과 폴더를 전부 찾아 표로 낸다 — '
                         '이름을 손으로 짓지 말 것 (예: --scan ~/sdcp)')
    ap.add_argument('--dir', default='')
    ap.add_argument('--collect-only', action='store_true')
    #  ★★ 2026-08-24 (CDXR2-5) — 러너의 마지막 줄이 `--collect-only` 라 **항상 exit 0** 이었다.
    #    팔이 모자라도·미수렴이어도·고정인자가 어긋나도 러너가 초록으로 끝났다.
    #    그렇다고 러너가 판정을 돌리면 안 된다 — 이 스크립트 헤더가 못박은 대로
    #    "결과를 보고 창을 옮길 수 없게" 판정은 따로 돌아야 한다.
    #    ⇒ **봉인과 판정을 가른다**: 봉인 = 데이터가 쓸 만한가(팔 수·origin 집합·수렴·
    #      digest·고정인자), 판정 = 그것이 뭐라고 말하는가(h0/h1/비).  봉인은 답을 누설하지
    #      않으므로 러너가 돌려도 사전등록이 안 깨진다.
    ap.add_argument('--seal-only', action='store_true',
                    help='계약 **봉인만** 검사한다 (팔 수·origin 집합·수렴·digest·고정인자). '
                         'h0/h1 과 비는 **출력하지 않는다** — 판정은 prereg §5 순서로 따로 '
                         '돈다.  봉인이 깨지면 nonzero.  ⚠ 팔이 1개면 표준오차를 못 내 봉인이 '
                         '깨진 것으로 나온다 — 단일팔 진단에는 쓰지 말 것 (러너가 ARMS≥2 에서만 건다)')
    ap.add_argument('--out', default='')
    ap.add_argument('--selftest', action='store_true')
    #  ★ 2026-08-19 (A5) — seed 앙상블 축.  `mpm_seed` **하나만** 고정 인자에서 면제한다.
    #    ⚠ prereg 에 그렇게 등록한 경우에만 쓸 것 — 면제는 판정 출력에 남는다.
    ap.add_argument('--seed-ensemble', action='store_true',
                    help='mpm_seed 를 고정 인자에서 면제 (시딩이 확률적인 축을 잴 때). '
                         'prereg 에 등록한 경우에만.')
    #  ★ CDXIJ-10 (도핑 런 전 최소 계약) — 사전등록이 요구하는 **정확한 팔 수**와
    #    **이온 산출물**을 명시적으로 강제한다.  기본은 끔 (진단 팔·1팔 프로브 호환).
    ap.add_argument('--require-arms', type=int, default=None,
                    help='침대당 정확히 N origin 을 요구한다 (사전등록 8팔 factorial: 8)')
    ap.add_argument('--require-digest', action='store_true',
                    help='입력 artifact digest 와 code SHA 가 모든 팔에 있어야 한다 '
                         '(도핑 트랙 — "σ_ion 만 바꿨다" 의 유일한 기계 증거)')
    ap.add_argument('--require-ionic', action='store_true',
                    help='σ_ion 이 모든 팔에 있어야 한다 (도핑 트랙 — 이온축이 결론)')
    ap.add_argument('--compare-dir', default='',
                    help='두 번째 디렉터리 — 한 축만 다른 **대조쌍**으로 검증하고 이득 감소율을 낸다 '
                         '(CL-44/CL-45 류).  `--expect-differ` 로 다를 축을 명시해야 한다')
    ap.add_argument('--expect-differ', default='',
                    help='대조쌍에서 **다를 것으로 등록된** 인자, 쉼표 구분 '
                         '(예: sdcp_yield_to_vgcf).  그 밖이 다르면 HOLD, 그것이 같아도 HOLD')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if a.scan:
        _rows = scan(os.path.expanduser(a.scan))
        if not _rows:
            raise SystemExit(f'{a.scan} 아래에 p2_*.json 을 가진 디렉터리가 없다')
        _w = max(len(r[0]) for r in _rows)
        print(f'{"디렉터리":{_w}} {"SBE/DBE":>8} {"vox":>7} {"섬유":>8} {"SDCP":>7} '
              f'{"σ_VGCF":>10} {"σ_ion":>7} {"수렴":>9}')
        for r in _rows:
            print(f'{r[0]:{_w}} {r[1]:>8} {r[2]:>7} {r[3]:>8} {r[4]:>7} '
                  f'{r[5]:>10} {r[6]:>7} {r[7]:>9}')
        print('\n  σ_ion 열 = 이온값이 있는 팔 / 전체 (LEAN=2 는 0/N 이 정상)')
        print('  → 판정: --dir <위 이름 중 하나>   ·  대조쌍: --dir A --compare-dir B --expect-differ <필드>')
        raise SystemExit(0)
    if a.compare_dir:
        if not a.dir:
            raise SystemExit('사용: --dir <대조> --compare-dir <실험> --expect-differ <필드>')
        _exp = {s.strip() for s in a.expect_differ.split(',') if s.strip()}
        if not _exp:
            raise SystemExit('`--expect-differ` 가 비었다 — 무엇이 달라야 하는지 **먼저 등록**해야 '
                             '"그 밖은 같다" 를 검사할 수 있다 (fail-closed)')
        _bad = _exp - set(_FIXED_FIELDS)
        if _bad:
            raise SystemExit(f'알 수 없는 인자 {sorted(_bad)} — 가능: {list(_FIXED_FIELDS)}')
        c = compare_dirs(a.dir, a.compare_dir, _exp)
        print(f'\n══ 대조쌍 검증 ══\n  결정: **{c["decision"]}**\n  근거: {c["reason"]}')
        if c['decision'] == 'measured':
            print(f'\n  A (대조)   비 = {c["ratio_a"]:.6f}   G = {c["gain_a"]:+.5f}  '
                  f'= {c["gain_a"] * 100:+.2f} %')
            print(f'  B (실험)   비 = {c["ratio_b"]:.6f}   G = {c["gain_b"]:+.5f}  '
                  f'= {c["gain_b"] * 100:+.2f} %')
            print(f'  ▸ 이득 감소율 = **{c["reduction_pct"]:.2f} %**   ({c["n_pair"]} 쌍)')
            print('  ⚠ 판정선 대입은 prereg 등록값으로 따로 — 이 도구는 **측정만** 한다')
        if a.out:
            json.dump(c, open(a.out, 'w'), ensure_ascii=False, indent=1)
            print(f'\n  → {a.out}')
        raise SystemExit(0 if c['decision'] == 'measured' else 1)
    if not a.dir:
        raise SystemExit('사용: --dir <결과 디렉터리>')
    #  ★★ 2026-08-24 (CDXR3-1) — **모드는 배타다.**  옛 판은 두 옵션을 같이 주면
    #    collect 분기가 **먼저** 실행돼 raw 결과를 찍고 exit 0 으로 끝났다 = 봉인 미실행
    #    (실측 재현).  봉인이 "결과를 안 보고" 를 뜻하려면 조합 자체가 불가능해야 한다.
    if a.seal_only and a.collect_only:
        raise SystemExit('--seal-only 와 --collect-only 는 **같이 못 쓴다**.  봉인은 결과를 '
                         '보지 않는 검사이고 수집은 결과를 찍는 것이다 (CDXR3-1)')
    rows, arms = collect(a.dir)
    #  ⚠⚠ 봉인 모드에서는 **팔 표를 찍지 않는다**.  옛 판은 이 표가 분기보다 위에 있어
    #    σ_e 원값 16개가 봉인 전에 그대로 노출됐다 — 회귀 ㉜c 는 `seal_lines()` 반환만
    #    검사해서 이 preamble 을 못 봤다 ("실제 경로를 안 타는 테스트" 의 재발).
    if not a.seal_only:
        print(f'{"파일":<28} {"σ_e":>12} {"σ_ion":>12} {"dof":>12} {"origin shift":>22} {"cg":>4}')
        for r in rows:
            print(f'{r["file"]:<28} {str(r["sigma_e"]):>12} {str(r["sigma_ion"]):>12} '
                  f'{str(r["n_dof"]):>12} {str(r["origin_shift_um"]):>22} {str(r["cg_info"]):>4}')
    print(f'\n  수집: SBE {len(arms["SBE"])} 팔 · DBE {len(arms["DBE"])} 팔')
    if a.collect_only:
        print('  (--collect-only — 판정하지 않는다)')
        raise SystemExit(0)
    if a.seal_only:
        _v = verdict(arms, seed_ensemble=a.seed_ensemble, require_arms=a.require_arms,
                     require_ionic=a.require_ionic, require_digest=a.require_digest)
        _ok, _lines = seal_lines(_v)
        print('\n'.join(_lines))
        raise SystemExit(0 if _ok else 1)
    v = verdict(arms, seed_ensemble=a.seed_ensemble,
                require_arms=a.require_arms, require_ionic=a.require_ionic,
                require_digest=a.require_digest)
    print(f'\n══ 판정 (prereg §5) ══\n  결정: **{v["decision"]}**\n  근거: {v["reason"]}')
    if 'ratio' in v:
        print(f'  σ_e 비 = {v["ratio"]}   (h0 ≥ {H0_MIN_RATIO} · h1 = {H1_RATIO})')
    _rel = v.get('se_ratio_rel_pct', v.get('se_ratio_pct'))     # 옛 payload 호환
    if _rel is not None:
        _abs = v.get('se_ratio_abs_pp')
        _abs_s = f' = 절대 {_abs} %p' if _abs is not None else ''
        print(f'  비의 상대 표준오차 = {_rel} % (문턱 {SE_MAX_REL_PCT} %, 비대응 = 게이트 '
              f'규약){_abs_s}')
    _prel = v.get('se_ratio_paired_rel_pct', v.get('se_ratio_paired_pct'))
    if _prel is not None:
        print(f'  쌍대응(origin-key join) 평균 = {v.get("ratio_paired_mean")} · '
              f'SE = {_prel} % · n = {v.get("n_origin")}')
    if a.out:
        json.dump({'rows': rows, 'verdict': v}, open(a.out, 'w'), ensure_ascii=False, indent=1)
        print(f'\n  → {a.out}')
    raise SystemExit(0 if v['decision'] in ('h0', 'h1') else 1)
