#!/usr/bin/env python3
"""사전등록 v2 판정기 — `docs/reviews/sdcp_gain_prereg_v2_20260816.md` §5 순서를 **코드로** 박는다.

★ 왜 별도 스크립트인가: 판정선을 사람이 눈으로 보고 적용하면 결과를 본 뒤 창이 움직인다
  (Codex CDX-13 이 지적한 실사고).  판정 순서·문턱을 **런 전에 코드로 고정**해 두면
  결과가 무엇이든 같은 함수가 같은 답을 낸다.

★ 판정 순서 (prereg §5, 여기서 바꾸면 사전등록 위반):
  1. 미수렴 팔(cg_info ≠ 0)이 하나라도 → **판정 보류**
  2. 8 팔 origin-위상 산포 > 1.17 %p → **판정 보류**, origin 16 으로
     ⚠ 이 양은 `sd/√n` 이지만 **표준오차가 아니다** — 8 위상은 한 침대의 완전 {0,½}³
       factorial 이라 복제 오차 자유도가 0 이다 (R8 Q1).  게이트로서의 뜻(산포가 크면
       판정을 미룬다)은 그대로이고, **이름만** 고쳤다.  문턱·변수명·판정 로직 불변.
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

#  ★★★ 실행 계약의 단일 출처 (R3-CX-01/05/06).  자리·수렴·backend·required 를 여기서
#    가져온다 — 사본을 두면 갈라지고, 실제로 네 번 갈라졌다.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_contract as _RC                                              # noqa: E402

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
    'vox':                  dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-12'),
    'bridge_um':            dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-20'),
    'fibre_stamp':          dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-12'),
    'sdcp_stamp':           dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-16'),
    'sdcp_sphere_d_um':     dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-16'),
    'sigma_vgcf_S_cm':      dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-20'),
    'sigma_sdcp_S_cm':      dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-20'),
    'sdcp_yield_to_vgcf':   dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-18'),
    #  ★ SELF-11 / Q-B2 판별 노브 — σ 침대를 바꾼다 (브리지가 셀을 새로 채운다)
    'sdcp_bridge_um':       dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-25'),
    #  ★ G2 (D13 원장 ②) — PTFE 이온 차단 노브.  SE(6)→SE_blk(9) 로 σ 침대를 바꾼다.
    'ptfe_block_um':        dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-25'),
    'sigma_ptfe_S_cm':      dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-20'),
    'ptfe_stamp':           dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-24'),
    'ptfe_zero_dof':        dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-24'),
    'backend':              dict(scope='numeric', across_dir=True, required=True,
                            required_since='2026-08-20'),
    #  ★★★ 2026-08-25 (A2 가 적발) — **규약 축인데 이 레지스트리에 없던 일곱.**
    #    `PROTOCOL_FIELDS` 에는 있어서 해시에는 들어갔지만, `compare_dirs` 는
    #    `_XDIR_FIELDS`(= 이 레지스트리) 만 보므로 **두 디렉터리 사이에서 자유롭게
    #    달라져도 `measured`** 였다.  `periodic_xy`·`plate_rule` 은 R4 때 규약 축이 됐고
    #    나머지 다섯은 A1 에서 새로 축이 됐는데, 둘 다 여기 등재를 잊었다.
    #    ⇒ 아래 ㊹ 가 `PROTOCOL_FIELDS ⊆ FIELD_CONTRACT` 를 **상시 강제**한다.
    'periodic_xy':          dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-25'),
    'plate_rule':           dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-25'),
    'sigma_superp_S_cm':    dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-25'),
    'sigma_swcnt_S_cm':     dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-25'),
    'swcnt_ion_block':      dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-25'),
    'dilate_z':             dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-25'),
    'se_source':            dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-25'),
    # ── 세대 인자 (옛 `_GEN_FIELDS`) — 전부 physics 다.  섞이면 다른 실험이다. ──
    'sigma_ion_se_S_cm':    dict(scope='physics', across_dir=True, generation=True),
    'sigma_ion_sdcp_S_cm':  dict(scope='physics', across_dir=True, generation=True),
    'sigma_am_s_S_cm':      dict(scope='physics', across_dir=True, generation=True),
    'sigma_am_p_S_cm':      dict(scope='physics', across_dir=True, generation=True),
    'cam':                  dict(scope='physics', across_dir=True, generation=True),
    'temp_c':               dict(scope='physics', across_dir=True, generation=True),
    'ea_ion_ev':            dict(scope='physics', across_dir=True, generation=True),
    'se_E_GPa':             dict(scope='physics', across_dir=True, generation=True),
    'se_nu':                dict(scope='physics', across_dir=True, generation=True),
    'se_sigma_y_GPa':       dict(scope='physics', across_dir=True, generation=True),
    'mpm_seed':             dict(scope='physics', across_dir=True, generation=True),
    # ── 침대 정체성 — 침대 **안**에서만 고정 (FA-06: SBE 에 SDCP 가 없는 것은 정상) ──
    'additive_E_GPa':       dict(scope='bed', across_dir=True, generation=True),
    'input_digest':         dict(scope='bed', across_dir=True, generation=True),
    # ── 코드 정체성 — 침대와 무관하지만 **섞이면 다른 실험**이다 (CDXIJ-10 ③). ──
    'code_sha':             dict(scope='numeric', across_dir=True, generation=True),
    #  ★★ 2026-08-25 (CDXR3-3) — **물리 규약 정체성**.  적용된 인자들에서 파생된 해시라
    #    개별 필드가 하나라도 다르면 이것도 달라진다 = 요약 봉인.  required 로 둔다 —
    #    기록이 없으면 어느 규약인지 확정할 수 없다.
    #  ★★★ 2026-08-25 (R3-CX-06, Codex 3차) — **파생 필드**다.  raw 축들의 해시이므로
    #    독립 실험 축이 아니다.  두 가지를 강제한다:
    #      ⓐ cross-dir 에서 이 필드의 차이는 **등록된 raw 축 변화로 설명되면 허용**한다.
    #         옛 판은 `sdcp_yield_to_vgcf` 한 축만 바꾼 정상 A/B 를 "id 도 다르다" 는
    #         이유로 HOLD 했다 = 과잉차단 (Codex 실측).
    #      ⓑ `--expect-differ physics_protocol_id` 는 **거부**한다.  raw 축은 그대로 두고
    #         id 만 바꿔 `measured` 를 얻는 경로가 있었다 (Codex 실측).
    'physics_protocol_id':  dict(scope='physics', across_dir=True, required=True,
                            required_since='2026-08-25', derived_from='PROTOCOL_FIELDS'),
    #  요청↔적용 불일치 (payload 가 기록).  False 면 그 팔은 요청과 다른 규약으로 돌았다.
    'physics_protocol_match': dict(scope='physics', across_dir=True),
}


def contract_fields(scope=None, across_dir=None, required=None, generation=None):
    """레지스트리에서 필드 이름을 뽑는다 — **모든 게이트의 유일한 출처**.

    ★ `required` (Codex 의 `required_since`) — **있어야 하는가** 와 **달라지면 안 되는가**
      는 다른 축이다.  세대 인자(σ_AM·온도·침대 E)는 *섞이면 HOLD, 전부 없으면 통과* 다
      (옛 payload 를 죽이지 않는다, 회귀 ⑲).  규약 인자는 *없으면 HOLD* 다 (H5)."""
    return tuple(k for k, v in FIELD_CONTRACT.items()
                 if (scope is None or v['scope'] in (scope if isinstance(scope, (tuple, list))
                                                     else (scope,)))
                 and (across_dir is None or v.get('across_dir') is across_dir)
                 and (required is None or bool(v.get('required', False)) is required)
                 and (generation is None or bool(v.get('generation', False)) is generation))



#: ★★★ **A2 (2026-08-25) — 선언 밖 매니페스트 키 훑기.**
#   `FIELD_CONTRACT` 는 손으로 유지된다.  producer 가 새 키를 실으면 그 키는 **아무
#   게이트도 안 지나고** 팔 사이에서 자유롭게 달라질 수 있다.  R3·R4 가 반복해 잡은
#   "선언은 있는데 거동이 없다" 의 거울상이다 — 여기서는 **선언조차 없다**.
#   실제 증거: 이번 A1 에서 producer 에 `dilate_z`·`se_source` 를 새로 실었는데,
#   `FIELD_CONTRACT` 에 안 넣었다면 두 팔이 다른 z-늘림으로 돌아도 판정은 초록이었다.
#   ⇒ 매니페스트 키를 **전수**로 대조하고, 아래 두 종류만 면제한다.
#     · `MANIFEST_RESULT_KEYS` — 런의 **결과·기록**이다.  다르면 그것이 실험의 결과다.
#     · `MANIFEST_DERIVED_OF`  — 다른 축의 그림자.  그 축이 등록되면 같이 움직이는 것이 정상.
#   ⚠ 새 키를 추가하면 셋 중 하나를 골라야 한다 (`FIELD_CONTRACT` · RESULT · DERIVED_OF).
#     고르지 않으면 아래 ⑥ 이 이름을 대며 HOLD 한다 — **fail-closed 가 기본값**이다.
MANIFEST_RESULT_KEYS = {
    'status': '런 결과 (component 상태 요약)',
    'expected': '상수 목록 (`STEP3_EXPECTED`)',
    'missing': '런 결과', 'failed': '런 결과',
    'components': '런 결과 — component 별 수렴 반복수·잔차가 들어 있다',
    'backend_last_solve': '런 결과 (하위호환 요약; 정본은 `backend`)',
    'mesh_unavailable': '런 결과',
    'plate_z_grid_um': '래스터화 **결과** (침대·vox 가 정하는 값이지 입력이 아니다)',
    'ptfe_cells_observed': '침대 **측정치** — 스탬프 규약이 바뀌면 따라 바뀐다',
    'input_files': '경로는 디렉터리마다 다르다.  **내용**은 `input_digest` 가 덮는다',
    'schema_version': '세대 표시.  세대 계약은 `schema_of` 가 따로 본다',
    #  ★ 2026-08-27 (Codex R7 Q4a) — 실행 환경 기록.  **게이트 아님**: 기계·venv 가
    #    다르면 당연히 다르고 그 사실 자체가 정보다.  `code_sha` 가 못 덮는 축
    #    (sitecustomize·PYTHONPATH·repo 전역 untracked code-like·로드된 모듈 해시)을
    #    리뷰어가 볼 수 있게 남긴다.  ⚠ 옛 팔에는 이 키가 **없다** — 필수가 아니다.
    'exec_env': '실행 환경 기록 (Q4a) — code_sha 가 못 덮는 축.  판정을 막지 않는다',
    'component_plan': '무엇을 돌렸나 — LEAN 팔과 전량 팔이 섞이면 `_XDIR_FIELDS` 밖의 '
                      '증거 계약이 잡는다 (여기서 고정하면 정상 LEAN 대조가 막힌다)',
}

#: 다른 축의 **그림자**.  값 = 그것을 설명하는 raw 축 이름.
MANIFEST_DERIVED_OF = {
    'fibre_stamp_requested': 'fibre_stamp',
    'fibre_stamp_applied': 'fibre_stamp',
    'ptfe_stamp_requested': 'ptfe_stamp',
    'bridge_um_explicit': 'bridge_um',
    'sigma_ion_se_ref_S_cm': 'sigma_ion_se_S_cm',   # 온도 재척도 **이전** 값
    'physics_protocol_expected': 'physics_protocol_id',
}


#: 사전등록 origin factorial — prereg §4 `{0, vox/2}³` (8점).
#  ★★★ 2026-08-25 (R5-CX-04, Codex 5차) — 옛 게이트는 **존재·유일성·집합일치·개수**만 봤다.
#    그래서 z-only 8점 `[0,0,0.00] … [0,0,0.07]` 이 `require_arms=8` 에서 `h0` 였다.
#    ⚠⚠ 게다가 **내 픽스처가 바로 그 z-only 패턴**이라 이 오류를 "정상 증인" 으로 고정하고
#      있었다 (이 세션에서 네 번째 — 픽스처가 결함을 인코딩한 사례).  ⇒ 픽스처를 먼저 고치고
#      게이트를 세웠다.  순서를 반대로 하면 새 게이트가 옛 픽스처를 통과시켜 또 초록이 난다.
def expected_origins(vox):
    """`vox` → 사전등록 origin 집합 (정렬된 8튜플).  vox 를 모르면 None.

    ★ 정의는 `run_contract.expected_origins_for` **하나**다 — 러너도 그것을 쓴다.
      사본을 두면 갈라지고, 갈라지면 러너가 찍은 origin 과 판정기가 기대하는 origin 이
      조용히 달라진다 (이 리포가 반복해 겪은 사고 부류)."""
    try:
        _e = _RC.expected_origins_for(vox)
    except (TypeError, ValueError):
        return None
    return _e or None


def manifest_unswept_keys(man_a, man_b):
    """→ 두 매니페스트에서 **아무 계약도 안 지나는** 키 목록 (정렬).

    ★ 값이 같든 다르든 상관없이 **분류되지 않은 키**를 돌려준다 — 분류를 강제하는 것이
      목적이다.  "지금은 우연히 같다" 는 계약이 아니다."""
    _known = (set(FIELD_CONTRACT) | set(MANIFEST_RESULT_KEYS) | set(MANIFEST_DERIVED_OF)
              #  `vox_um` 은 레지스트리에서 `vox` 라는 짧은 이름을 쓴다 (리더가 접는다).
              | {'vox_um', 'origin_shift_um'})
    return sorted(k for k in (set(man_a or {}) | set(man_b or {})) if k not in _known)


def manifest_raw_diff(man_a, man_b, expect_differ):
    """→ 등록 축으로 설명되지 **않는** 매니페스트 차이 목록 (정렬).

    파생 키는 그 부모 축이 `expect_differ` 에 있으면 면제한다."""
    _exp = set(expect_differ or ())
    out = []
    for k in sorted(set(man_a or {}) | set(man_b or {})):
        if k in MANIFEST_RESULT_KEYS or k in _exp:
            continue
        #  ★ 레지스트리가 **파생**이라고 선언한 필드는 위 `_XDIR_FIELDS` 루프가 이미
        #    정확히 다룬다 (등록 축이 실제로 달라졌을 때만 허용).  여기서 다시 세면
        #    정상 한-축 실험이 HOLD 된다 = R3-CX-06 과잉차단의 재발.
        if FIELD_CONTRACT.get(k, {}).get('derived_from'):
            continue
        #  ★ 그림자 필드 — 부모 축이 등록됐거나 **실제로 달라졌으면** 따라 움직이는 것이 정상.
        #    부모가 같은데 그림자만 다르면 그것은 기록이 손으로 바뀐 것이다 → 아래로 떨어진다.
        _par = MANIFEST_DERIVED_OF.get(k)
        if _par and (_par in _exp
                     or _canon((man_a or {}).get(_par)) != _canon((man_b or {}).get(_par))):
            continue
        #  `vox` ↔ `vox_um` 이름 접기 — 레지스트리 이름으로도 등록할 수 있게 한다.
        if k == 'vox_um' and 'vox' in _exp:
            continue
        if _canon((man_a or {}).get(k)) != _canon((man_b or {}).get(k)):
            out.append(k)
    return out

#: 팔 간 고정 인자 (같은 디렉터리) — physics + numeric.  bed 는 제외 (침대끼리 다르다).
_FIXED_FIELDS = contract_fields(scope=('physics', 'numeric'))
#: 그중 **기록이 없으면 HOLD** 인 것 (규약 인자).  세대 인자는 여기 없다 — 회귀 ⑲ 참조.
_REQUIRED_FIELDS = contract_fields(required=True)
#: 침대 정체성 — 침대 안에서만 고정.
_BED_FIELDS_C = contract_fields(scope='bed')
#: cross-directory 대조에서 고정할 축 — **세대 인자와 침대까지** 포함한다.
_XDIR_FIELDS = contract_fields(across_dir=True)

#  ★★★ 2026-08-25 (R3-CX-06, Codex 3차) — **이 목록도 레지스트리에서 파생한다.**
#    사본으로 두니 갈라졌고, Codex 가 세 pass-mutant 로 증명했다: `required` 를 뒤집어도
#    `across_dir` 을 뒤집어도 이 목록에서 `temp_c` 를 지워도 **selftest 126/126 초록**이었다
#    (선언만 있고 거동이 시험되지 않았다).  ⇒ ⓐ 목록을 파생시키고 ⓑ 아래 ㊷ 가
#    **레지스트리를 읽어 거동을 생성**한다 (선언을 바꾸면 시험이 따라 바뀐다).
_GEN_FIELDS = contract_fields(generation=True)

#: (역사) 옛 하드코딩 목록 — ㊷i 가 레지스트리 파생과 **같은 집합**임을 강제한다.
_GEN_FIELDS_LEGACY = ('sigma_ion_se_S_cm', 'sigma_ion_sdcp_S_cm',
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
    row = {'file': os.path.basename(path),
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
            #  ★★ 2026-08-25 (R3-CX-04) — 기록만 되고 **소비되지 않던** 둘.
            'component_plan': man.get('component_plan'),
            'ptfe_cells_observed': man.get('ptfe_cells_observed'),
            'components': man.get('components'),
            #  ★★★ 2026-08-25 (R3-CX-03) — **raw manifest 를 들고 다닌다.**  저장된
            #    `physics_protocol_id` 만 읽으면 stale·손으로 쓴 값·축 키 부재를 못 잡는다
            #    (Codex 가 셋 다 통과시켰다).  재계산하려면 원본이 있어야 한다.
            '_manifest': man,
            #  ★ R4-CX-02 — component 별 증거는 step3 **전체**를 봐야 한다 (thermal·pore
            #    블록이 top-level 이 아니다).  리더가 골라 담으면 그 목록이 또 갈라진다.
            '_step3': s,
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
    #  ★★★ A2 (2026-08-25) — **레지스트리 필드는 자동으로 채운다.**  옛 판은 리더가 필드를
    #    손으로 골라 담았고, 그래서 `FIELD_CONTRACT` 에 축을 추가해도 리더가 안 담으면
    #    게이트가 `None` 만 봐서 **원리적으로 발화하지 못했다** (H5·CDX-IJ-01 과 같은 부류의
    #    가짜 보증).  실제로 `periodic_xy`·`plate_rule`·σ_SuperP·σ_SWCNT·`swcnt_ion_block`·
    #    `dilate_z`·`se_source` 일곱이 그 상태였다.  ⇒ 목록을 두 곳에 두지 않는다.
    #    ⚠ 위에서 **명시적으로 정규화한 값**(bool 접기 등)은 덮지 않는다 (None 일 때만 채운다).
    for _f in FIELD_CONTRACT:
        if row.get(_f) is None:
            row[_f] = man.get(_f)
    return row


def collect(d):
    rows = [_read(p) for p in sorted(glob.glob(os.path.join(d, 'p2_*.json')))]
    #  ★★★ 2026-08-25 (R5-CX-08, Codex 5차) — **기각 receipt 가 판정에 안 읽혔다.**
    #    러너는 봉인이 깨지면 `.rejected_<UTC>` 를 쓰는데 `collect()` 는 `p2_*.json` 만
    #    글롭했다.  실측: 정상 16팔 디렉터리에 receipt 를 넣기 **전후가 둘 다 `h0`**.
    #    ⇒ 기각 기록을 남기고 그것을 아무도 안 보면 그 기록은 장식이다.
    #    기각된 tree 는 **즉시 격리**한다 — 무엇이 왜 기각됐는지는 그 파일이 말한다.
    _rej = sorted(glob.glob(os.path.join(d, '.rejected_*')))
    if _rej:
        rows = [dict(r, _rejected=[os.path.basename(x) for x in _rej]) for r in rows] or [
            {'file': '<none>', '_rejected': [os.path.basename(x) for x in _rej]}]
    #  ★★★ 2026-08-31 — **진단 tree 는 이 판정기의 대상이 아니다.**
    #    `reduce_arm_payloads.py --diagnostic` 이 만든 패키지는 팔 수를 줄인 단일-origin
    #    런이고 소비자는 `ion_r_verdict.py` 다.  그런데 축소본 파일명이 `p2_*.json` 이고
    #    이 판정기는 아래 factorial 게이트 주석대로 *"팔 수를 줄인 진단 런은 막지 않는다"*
    #    ⇒ 표지가 없으면 부분 cohort 에 **판정이 난다**.  표지를 읽고 격리한다.
    #    ⚠ 표지가 **둘**인 이유: 트리 파일만 보면 `p2_*.json` 만 복사해 간 순간 표지가
    #      사라진다 — `.rejected_*` 가 정확히 그렇게 유실됐다 (R5-CX-08 위 주석).
    _dgf = sorted(os.path.basename(x) for x in glob.glob(os.path.join(d, '.diagnostic_*')))
    _rows = []
    for r in rows:
        _marks = list(_dgf)
        if ((r.get('_step3') or {}).get('_reduced') or {}).get('diagnostic'):
            _marks.append(f'payload:{r["file"]}')
        _rows.append(dict(r, _diagnostic=sorted(set(_marks))) if _marks else r)
    rows = _rows
    if _dgf and not rows:
        rows = [{'file': '<none>', '_diagnostic': _dgf}]
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


#: 솔버가 수렴이라고 부르는 문턱.  ★ 값은 `run_contract` 가 정본이고 여기는 별칭이다
#  (사본을 두면 갈라진다 — 이 파일의 `_conv_ok` 가 정확히 그렇게 갈라졌다).
CG_RESID_MAX = _RC.CG_RESID_MAX


def _conv_ok(ci, un, rs):
    """(cg_info, unconverged, resid) → (통과?, 사유코드).  전자·이온 **공통** 검사.

    ★★★ 2026-08-25 (R3-CX-05/06, Codex 3차) — **본문을 `run_contract` 로 옮겼다.**
      여기 사본이 있던 동안 `check_arm` 의 것과 미묘하게 달라졌고, 둘 다
      `isinstance(ci, (int, float))` + `int(ci)` 라 **`cg_info = 0.5` 가 절삭돼 통과**했다
      (Codex 실측: `_conv_ok(0.5, False, 1e-9) → (True, '')`).
      ⇒ 계약은 한 곳에만 산다.  이 함수는 얇은 별칭이다 (호출부를 안 건드리려고 남긴다).
    """
    return _RC.conv_ok(ci, un, rs)


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


def validate_contract(arms, seed_ensemble=False, require_arms=None,
                      require_ionic=False, require_digest=False, where=''):
    """`_validate_contract_raw` 에 **어디서 깨졌는지** 접두사를 붙인다.

    ⚠ 얇은 껍질인 이유: 사유 문자열이 21곳에서 만들어지므로 각 자리에 접두사를 심으면
      또 갈라진다.  한 자리에서 붙인다."""
    _h, _info = _validate_contract_raw(arms, seed_ensemble=seed_ensemble,
                                       require_arms=require_arms,
                                       require_ionic=require_ionic,
                                       require_digest=require_digest)
    if _h and where and _h.get('reason'):
        _h = dict(_h, reason=f'[{where}] ' + _h['reason'])
    return _h, _info


def _validate_contract_raw(arms, seed_ensemble=False, require_arms=None,
                           require_ionic=False, require_digest=False):
    """한 디렉터리의 **실행 계약 검증**.  통과면 `(None, info)` · 위반이면 `(hold, info)`.

    ★★★ 왜 떼어냈나 (2026-08-25, Codex 재리뷰 조건 5): 이 검사들이 `verdict()` 안에
      인라인이라 **`compare_dirs()` 는 하나도 돌리지 않았다**.  두 디렉터리를 빼는 실험은
      각 디렉터리가 먼저 계약을 만족해야 하는데, 옛 판은 origin 짝·digest·`_XDIR_FIELDS`
      만 보고 **미수렴·세대혼합·규약 불명·필수 필드 부재를 전부 통과**시켰다.
      ⇒ `verdict` 와 `compare_dirs` 가 **같은 함수**를 부른다.  검사 목록이 갈라질 자리가
        없어진다 (`_FIXED_FIELDS` 가 세 곳에 하드코딩돼 있던 것과 같은 부류의 결함).

    ⚠ 순서는 prereg §5 의 전제 집행 순서 그대로다 — **바꾸지 말 것**.
    ⚠ `where` 는 사유 문자열의 접두사다 (어느 디렉터리가 깼는지 말해 준다).
    """
    #  ★★★★ 2026-08-31 — **진단 패키지는 이 판정기의 대상이 아니다 (가장 먼저 본다).**
    #    이것은 데이터 결함이 아니라 **범주 오류**다 — "이 tree 로는 cohort 판정을 내지
    #    않는다".  그래서 다른 어떤 게이트보다 먼저 답한다.  뒤에 두면 최소 픽스처처럼
    #    다른 사유가 먼저 물어 **표지가 가려지고**, 그러면 "표지를 박았다" 는 주장 자체가
    #    검증되지 않는다 (실측: selftest 에서 그 상태가 났다).
    #    표지 ① `.diagnostic_*` 트리 파일 · ② payload 의 `step3._reduced.diagnostic`
    #    — 둘 중 하나만 남아도 문다 (`p2_*.json` 만 복사해 가면 ① 이 사라진다).
    _dg = sorted({x for k in arms for r in arms[k] for x in (r.get('_diagnostic') or ())})
    if _dg:
        return dict(decision='HOLD', hold_code='DIAGNOSTIC_TREE',
                    reason=f'이 디렉터리는 **진단 패키지** 다 ({_dg[:2]}) — '
                           f'`reduce_arm_payloads.py --diagnostic` 이 팔 수를 줄여 만든 '
                           f'단일-origin tree 이고, 소비자는 `ion_r_verdict.py` 다.  '
                           f'cohort 판정은 8팔 factorial 을 전제하므로 여기서 내지 않는다'), {}

    info = {}
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
        return dict(decision='HOLD',
                    reason=f'미수렴 팔 {len(unconv)}개 — prereg §5-1 (판정 보류)',
                    unconverged=unconv), info
    if unknown:
        return dict(decision='HOLD',
                    reason=f'수렴 정보 없는 팔 {len(unknown)}개 — 확인 못 한 것을 통과시키지 '
                           f'않는다 (fail-closed).  payload 가 cg_info/cg_resid 를 싣도록 '
                           f'고치고 다시 돌릴 것',
                    no_convergence_info=unknown), info
    # ── 데이터 무결성 게이트 (2026-08-16, 심층 리뷰 ③) ────────────────────────────────
    #   ⚠ 이것은 §5 판정 순서의 **변경이 아니라 전제 집행**이다.  §5 는 "8 팔 factorial" 과
    #     "그 외 모든 인자 고정" 을 stipulate 한다 — 그 전제가 깨진 데이터는 §5 가 말하는
    #     그 데이터가 아니므로 판정 대상이 아니다.  (같은 origin 8 벌은 가짜 정밀도를 낳는다.)
    for k in ('SBE', 'DBE'):
        _sh = [tuple(r['origin_shift_um']) for r in arms[k] if r.get('origin_shift_um')]
        if _sh and len(set(_sh)) != len(_sh):
            return dict(decision='HOLD',
                        reason=f'{k} 에 **중복 origin** 이 있다 ({len(_sh) - len(set(_sh))}건) — '
                               f'같은 위상을 여러 번 세면 표준오차가 가짜로 작아진다'), info
    #  ★★ 2026-08-19 (A5) — 세대 혼합 게이트.  **고정-인자 검사보다 먼저** 돈다: 기록이 있는
    #    팔과 없는 팔이 섞이면 아래 "다르면 HOLD" 는 None 을 건너뛰어 **통과시켜 버리기** 때문이다.
    _gen_ex = {_SEED_FIELD} if seed_ensemble else set()
    if seed_ensemble:
        info['seed_ensemble'] = True          # 면제를 판정 출력에 남긴다 (조용한 완화 금지)
    for fld in _GEN_FIELDS:
        if fld in _gen_ex:
            continue
        _has = [r['file'] for k in ('SBE', 'DBE') for r in arms[k] if r.get(fld) is not None]
        _non = [r['file'] for k in ('SBE', 'DBE') for r in arms[k] if r.get(fld) is None]
        if _has and _non:
            return dict(decision='HOLD',
                        reason=f'세대 혼합 — `{fld}` 를 기록한 팔 {len(_has)}개와 기록이 **없는** '
                               f'팔 {len(_non)}개가 한 디렉터리에 있다 ({_non[0]} …).  '
                               f'옛 payload 는 이 인자로 무슨 값을 썼는지 추정할 수 없으므로 '
                               f'(σ_ion 은 --temp-c 로도 움직인다) 비교 불가다.  옛 팔을 다시 돌릴 것'), info
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
                return dict(decision='HOLD',
                            reason=f'{k} **안에서** `{fld}` 가 팔마다 다르다 '
                                   f'({sorted(map(str, _v))}) — 한 침대의 팔들은 같은 입력·같은 '
                                   f'물성이어야 한다 (CL-56 축)'), info
    #  ★ 침대 **사이**: digest 는 달라야 하고(같으면 같은 침대다), additive 는 **공통 키**만 같아야 한다.
    _ds = {r.get('input_digest') for r in arms['SBE'] if r.get('input_digest')}
    _dd = {r.get('input_digest') for r in arms['DBE'] if r.get('input_digest')}
    if _ds and _dd and _ds == _dd:
        return dict(decision='HOLD',
                    reason=f'SBE 와 DBE 의 `input_digest` 가 **같다** ({sorted(_ds)[0]}) — 두 팔이 '
                           f'같은 침대를 읽고 있다.  비 1.0 은 물리가 아니라 배선 실수다'), info
    _as = next((r['additive_E_GPa'] for r in arms['SBE'] if r.get('additive_E_GPa')), None)
    _ad = next((r['additive_E_GPa'] for r in arms['DBE'] if r.get('additive_E_GPa')), None)
    if isinstance(_as, dict) and isinstance(_ad, dict):
        _diff = {k for k in set(_as) & set(_ad) if _as[k] != _ad[k]}
        if _diff:
            return dict(decision='HOLD',
                        reason=f'두 침대가 `additive_E_GPa` 의 **공통 상**에서 다르다 ({sorted(_diff)}: '
                               f'{ {k: (_as[k], _ad[k]) for k in sorted(_diff)} }) — 세대가 섞였다 '
                               f'(CL-56).  SDCP 처럼 한쪽에만 있는 상은 정상이다'), info
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
            return dict(decision='HOLD',
                        reason=f'고정 인자 `{fld}` 가 팔마다 다르다 ({sorted(map(str, _v))}) — '
                               f'prereg §5 는 그 외 모든 인자 고정을 요구한다'), info
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
    #  ★★ 2026-08-25 (M-R3-04) — **전자축도 같은 문턱을 쓴다.**  Codex 가 전자
    #    `cg_info=0 · unconverged=False · residual=NaN` 으로 producer→check_arm→final seal
    #    **전 구간**을 통과시켰다 (payload 의 finite 벨트가 NaN 을 null 로 바꾸면 리더가
    #    None 을 보고 넘어간다).  ⇒ 이온과 **같은 `_conv_ok`** 로 건다.
    _eb = []
    for _k in arms:
        for _r in arms[_k]:
            _ok, _why = _conv_ok(_r.get('cg_info'), _r.get('unconverged'), _r.get('cg_resid'))
            if not _ok:
                _eb.append((_r['file'], _why))
    if _eb:
        return dict(decision='HOLD', hold_code='ELECTRONIC_CONV',
                    reason=f'전자 수렴이 확인되지 않는 팔 {len(_eb)}개 '
                           f'({_eb[0][0]}: {_eb[0][1]}) — cg_info=0 ∧ unconverged=False ∧ '
                           f'0 ≤ resid ≤ {CG_RESID_MAX:g} 를 모두 만족해야 한다 (M-R3-04)'), info
    #  ★★★ 2026-08-25 (R3-CX-04, Codex 3차) — **계획과 관측을 소비한다.**
    #    옛 판은 `component_plan` 과 `ptfe_cells_observed` 를 매니페스트에 적기만 하고
    #    아무도 읽지 않았다 = 증거가 아니라 장식.  Codex 가 둘 다 통과시켰다:
    #      · `component_plan.ionic=False` + ionic disabled + σ_ion 없음  → rc 0
    #      · `ptfe_stamp=centerline` + `ptfe_cells_observed=0`           → rc 0
    #    ⇒ ⓐ 계획한 component 가 complete 인가 ⓑ 도장이 실제 효과를 냈는가.
    _pl = []
    for _k in arms:
        for _r in arms[_k]:
            _plan = _r.get('component_plan')
            if not isinstance(_plan, dict) or not _plan:
                continue                       # 옛 세대는 계획이 없다 (아래 필수 게이트 소관)
            _cmp = _r.get('components') or {}
            for _c in _RC.required_components(plan=_plan):
                _st = (_cmp.get(_c) or {}).get('status') if isinstance(_cmp, dict) else None
                if _st != 'complete':
                    _pl.append((_r['file'], _c, _st))
    if _pl:
        return dict(decision='HOLD', hold_code='PLAN_NOT_MET',
                    reason=f'계획한 component 가 완료되지 않은 팔 {len(_pl)}개 '
                           f'({_pl[0][0]}: `{_pl[0][1]}` = {_pl[0][2]!r}) — '
                           f'`component_plan` 은 무엇을 돌리기로 했는지의 기록이다.  '
                           f'계획과 결과가 다르면 그 팔은 계획한 실험이 아니다 (R3-CX-04)'), info
    #  ★★★ 2026-08-25 (R4-CX-02/05) — 세 소비자가 **같은 계약**을 쓴다.
    _cb = []
    for _k in arms:
        for _r in arms[_k]:
            _man = _r.get('_manifest') or {}
            _s3r = _r.get('_step3') or {}
            for _fn, _lbl in ((lambda: _RC.strict_type_ok(_man), '타입'),
                              (lambda: _RC.plan_required(_man), '계획 존재'),
                              (lambda: _RC.ptfe_record_ok(_man), 'PTFE 기록'),
                              (lambda: (_RC.plan_ok(_man['component_plan'])
                                        if _man.get('component_plan') is not None
                                        else (True, None)), '계획 스키마'),
                              #  ⚠ 계획이 **없으면** 무엇을 돌리기로 했는지 알 수 없다.
                              #    그때 run-mode 기본(다섯 전부)을 요구하면 옛 팔이 통째로
                              #    막힌다 = 과잉차단.  전자축은 `numeric_ok` 가 이미 본다.
                              (lambda: (_RC.component_evidence_ok(
                                  _s3r, _RC.required_components(
                                      plan=_man['component_plan']))
                                  if _man.get('component_plan') is not None
                                  else (True, None)), 'component 증거')):
                _o, _w = _fn()
                if not _o:
                    _cb.append((_r['file'], _lbl, _w))
                    break
    if _cb:
        return dict(decision='HOLD',
                    hold_code=str(_cb[0][2]).split('|', 1)[0],
                    reason=f'{_cb[0][1]} 계약을 만족하지 않는 팔 {len(_cb)}개 — '
                           f'{_cb[0][0]}: {_cb[0][2]}'), info
    #  ★ R4-CX-02 — 이 검사는 위 `ptfe_record_ok` 로 옮겼다 (부재·음수·오타입까지 본다).
    _pm = [r['file'] for k in arms for r in arms[k] if r.get('physics_protocol_match') is False]
    if _pm:
        return dict(decision='HOLD', hold_code='PROTOCOL_MISMATCH',
                    reason=f'요청한 규약과 **적용된 규약이 다른** 팔이 {len(_pm)}개 '
                           f'({_pm[0]} …) — 러너가 요청한 것과 payload 가 실제로 한 것이 '
                           f'갈렸다.  다시 돌릴 것 (CDXR3-3)'), info
    #  ★★★ 2026-08-25 (R3-CX-03, Codex 3차) — **저장된 id 를 믿지 않고 재계산한다.**
    #    옛 판은 문자열을 읽어 `unknown:` 접두만 봤다.  Codex 가 셋을 통과시켰다:
    #      · 16 팔 전부 `periodic_xy`/`plate_rule` 키가 **없는데** stored 는 `p1-…`
    #      · 팔마다 `periodic_xy` 를 True/False 로 바꿔 놓고 stored 만 같게
    #      · 모든 팔에 `physics_protocol_id = "garbage"`
    #    셋 다 "서로 같으니 통과" 였다.  **문자열 일치는 규약 일치가 아니다.**
    _pu = []
    for _k in arms:
        for _r in arms[_k]:
            _ok3, _why3 = _RC.protocol_ok(_r.get('_manifest') or {})
            if not _ok3:
                _pu.append((_r['file'], _why3))
    if _pu:
        return dict(decision='HOLD',
                    hold_code=str(_pu[0][1]).split('|', 1)[0],
                    reason=f'규약 기록을 신뢰할 수 없는 팔 {len(_pu)}개 — '
                           f'{_pu[0][0]}: {_pu[0][1].split("| ", 1)[-1]}'), info
    #  ★ 2026-08-25 (Codex 재리뷰 조건 5) — **`required_since` 를 사유에 싣는다.**
    #    "없으면 HOLD" 만 말하면 운영자는 이것이 *버그* 인지 *옛 세대* 인지 모른다.
    #    producer 가 그 필드를 쓰기 시작한 날짜를 같이 말해 주면 "그 이전 payload 를
    #    다시 돌려라" 가 **행동 가능한 지시**가 된다.  게이트는 그대로 fail-closed 다 —
    #    `required_since` 는 **완화 스위치가 아니라 라벨**이다 (완화하면 H5 가 재발한다).
    for fld in _REQUIRED_FIELDS:
        _miss = [r['file'] for k in arms for r in arms[k] if r.get(fld) is None]
        if _miss:
            _since = FIELD_CONTRACT[fld].get('required_since')
            return dict(decision='HOLD', hold_code='REQUIRED_FIELD_MISSING',
                        missing_field=fld, required_since=_since,
                        reason=f'고정 인자 `{fld}` 가 매니페스트에 **없는** 팔이 {len(_miss)}개 '
                               f'({_miss[0]} …) — 기록되지 않은 인자는 고정을 확인할 수 없다.  '
                               f'현행 payload 는 {_since} 부터 이것을 항상 적는다 ⇒ 그 이전 '
                               f'세대로 돈 팔이다.  다시 돌릴 것'), info
    #  ★★★ 2026-08-25 (A1 이 드러낸 것) — **합성 침대는 물리 주장을 못 받친다.**
    #    payload 의 `if a.se_proxy or not a.se:` 분기는 `--se` 를 **빠뜨리기만 해도** 열리고,
    #    그 합성 구름이 `se_pts=` 로 rasterize 에 들어간다.  `input_digest` 는 읽은 파일이
    #    없으므로 그것을 못 덮는다.  ⇒ 기록을 신설한 김에 **판정에서 막는다** (생산 경로를
    #    막지 않는다 — 만드는 것은 자유고, 그것으로 σ 를 주장하는 것만 막는다).
    #  ★ R5-CX-08 — 기각 receipt 가 있는 tree 는 **판정하지 않는다** (격리).
    _rj = sorted({x for k in arms for r in arms[k] for x in (r.get('_rejected') or ())})
    if _rj:
        return dict(decision='HOLD', hold_code='REJECTED_TREE',
                    reason=f'이 디렉터리에 **기각 receipt** 가 있다 ({_rj[:2]}) — 러너가 '
                           f'봉인 실패를 기록한 tree 다.  그 안의 팔로는 판정하지 않는다 '
                           f'(무엇이 왜 기각됐는지는 그 파일이 말한다)'), info
    _px = sorted({r['file'] for k in arms for r in arms[k]
                  if isinstance(r.get('se_source'), str)
                  and r['se_source'].startswith('proxy:')})
    if _px:
        return dict(decision='HOLD', hold_code='SE_PROXY',
                    reason=f'SE 점구름이 **합성**인 팔이 {len(_px)}개 ({_px[0]} …) — '
                           f'`--se-proxy` 이거나 `--se` 를 빠뜨린 런이다.  합성 구름은 '
                           f'`input_digest` 가 못 덮고 실침대가 아니므로 σ 주장을 못 받친다'), info
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
            return dict(decision='HOLD',
                        reason=f'{k} 에 origin 기록이 **없는** 팔이 {len(_miss_o)}개 '
                               f'({_miss_o[0]} …) — origin 없이는 쌍을 지을 수 없다 (CDXIJ-10 ①)'), info
        _org[k] = [tuple(round(float(x), 9) for x in r['origin_shift_um']) for r in arms[k]]
        if len(set(_org[k])) != len(_org[k]):
            return dict(decision='HOLD',
                        reason=f'{k} 에 **중복 origin** — 같은 위상을 여러 번 세면 SE 가 가짜로 작아진다'), info
    if set(_org['SBE']) != set(_org['DBE']):
        _only_s = sorted(set(_org['SBE']) - set(_org['DBE']))
        _only_d = sorted(set(_org['DBE']) - set(_org['SBE']))
        return dict(decision='HOLD',
                    reason=f'두 침대의 **origin 집합이 다르다** — SBE 전용 {len(_only_s)}개 · '
                           f'DBE 전용 {len(_only_d)}개 (예: {(_only_s or _only_d)[:1]}).  '
                           f'짝이 없는 팔로는 비를 정의할 수 없다 (CDXIJ-10 ①)'), info
    if require_arms is not None and len(_org['SBE']) != int(require_arms):
        return dict(decision='HOLD',
                    reason=f'사전등록은 침대당 정확히 {int(require_arms)} origin 을 요구한다 — '
                           f'받은 것은 {len(_org["SBE"])}개 (CDXIJ-10 ①)'), info
    info['n_origin'] = len(_org['SBE'])

    #  ★★★ 2026-08-25 (R5-CX-04) — **개수가 아니라 어떤 점인지**를 본다.
    #    사전등록은 `{0, vox/2}³` 8팔 factorial 이다.  개수·유일성만 보면 한 축으로 늘어선
    #    8점(z-only)도 통과하고, 그것은 **격자 위상 앙상블이 아니다** (한 축의 편향만 잰다).
    #  ⚠ 팔 수를 줄인 진단 런(ARMS<8)은 막지 않는다 — 다만 **점 자체는 factorial 위**에
    #    있어야 한다 (부분집합).  전량 런은 **정확한 일치**를 요구한다.
    _vox = next((r.get('vox') for k in arms for r in arms[k] if r.get('vox') is not None), None)
    _exp_o = expected_origins(_vox)
    if _exp_o is None:
        return dict(decision='HOLD', hold_code='ORIGIN_VOX',
                    reason='origin factorial 을 확인할 `vox` 기록이 없다 — '
                           '어떤 위상 집합이어야 하는지 계산할 수 없다 (R5-CX-04)'), info
    _got_o, _expset = set(_org['SBE']), set(_exp_o)
    _alien = sorted(_got_o - _expset)
    if _alien:
        return dict(decision='HOLD', hold_code='ORIGIN_SET',
                    reason=f'사전등록 밖 origin {len(_alien)}개 (예: {_alien[0]}) — '
                           f'vox={_vox:g} 의 factorial 은 {{0, {_vox / 2:g}}}³ 다.  '
                           f'개수만 맞는 임의의 점 8개는 위상 앙상블이 아니다 (R5-CX-04)'), info
    if require_arms is not None and int(require_arms) == len(_exp_o) and _got_o != _expset:
        _miss_f = sorted(_expset - _got_o)
        return dict(decision='HOLD', hold_code='ORIGIN_SET',
                    reason=f'전량 런인데 factorial 이 **덜 찼다** — 빠진 점 {len(_miss_f)}개 '
                           f'(예: {_miss_f[0]}).  `{{0, {_vox / 2:g}}}³` 8점이 전부 있어야 '
                           f'한다 (R5-CX-04)'), info

    #  ★ CDXIJ-10 ③ — `require_digest` 면 **입력 digest·code SHA 가 있어야** 한다.
    #    기본은 끔 (옛 격자 팔 호환).  도핑 트랙은 켠다 — 그 실험의 전제가
    #    "pair 간 σ_ion 만 달랐다" 이고, 그것은 digest 없이는 확인할 수 없다.
    if require_digest:
        for _f in ('input_digest', 'code_sha'):
            _nd = [r['file'] for k in arms for r in arms[k] if not r.get(_f)]
            if _nd:
                return dict(decision='HOLD',
                            reason=f'`{_f}` 가 없는 팔 {len(_nd)}개 ({_nd[0]} …) — 같은 '
                                   f'디렉터리는 같은 입력·같은 코드의 증거가 아니다 '
                                   f'(CDXIJ-10 ③).  현행 payload 로 다시 돌릴 것'), info
        _dirty = [r['file'] for k in arms for r in arms[k]
                  if str(r.get('code_sha') or '').endswith('+dirty')]
        if _dirty:
            return dict(decision='HOLD',
                        reason=f'커밋 안 된 코드로 돈 팔 {len(_dirty)}개 ({_dirty[0]} …) — '
                               f'`code_sha` 가 `+dirty` 다.  재현 불가한 런은 판정 대상이 아니다'), info

    #  ★ 결과 seal (CDXIJ-10 ④) — `require_ionic` 이면 σ_ion 이 실제로 있어야 한다.
    #    도핑 트랙은 이온축이 결론이므로 `--no-ion`(LEAN=2) 산출물로 판정하면 안 된다.
    if require_ionic:
        _no_i = [r['file'] for k in arms for r in arms[k]
                 if not (isinstance(r.get('sigma_ion'), (int, float))
                         and r['sigma_ion'] == r['sigma_ion'] and r['sigma_ion'] > 0)]
        if _no_i:
            return dict(decision='HOLD',
                        reason=f'σ_ion 이 없는/비정상인 팔 {len(_no_i)}개 ({_no_i[0]} …) — '
                               f'도핑 판정은 이온축이 결론이다.  `--no-ion` 산출물로 판정 불가 '
                               f'(CDXIJ-10 ④)'), info
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
        #  ★★ 2026-08-25 (M-R3-05/06) — **솔버 규약과 같은 문턱을 쓴다.**
        #    `step3_sigma.py:590` 은 `unconv = bool(info) or resid > 1e-6` 이다.
        #    초판은 residual 이 **있을 때만** 유한성을 봤고 문턱은 안 썼다 ⇒ `None` 과
        #    `1e100` 이 둘 다 `h0` 로 통과했다 (Codex 실측).  residual 은 **필수**다.
        def _ion_ok(r):
            return _conv_ok(r.get('ion_cg_info'), r.get('ion_unconverged'), r.get('ion_resid'))
        _ion_bad, _ion_blind = [], []
        for _k in arms:
            for _r in arms[_k]:
                _ok, _why = _ion_ok(_r)
                if not _ok:
                    (_ion_blind if _why == 'blind' else _ion_bad).append(_r['file'])
        if _ion_bad:
            return dict(decision='HOLD', hold_code='IONIC_UNCONVERGED',
                        ion_unconverged_arms=len(_ion_bad),
                        reason=f'이온 솔브가 **미수렴**인 팔 {len(_ion_bad)}개 ({_ion_bad[0]} …) — '
                               f'prereg §5-1 대로 숫자를 내지 않는다'), info
        if _ion_blind:
            return dict(decision='HOLD', hold_code='IONIC_BLIND',
                        ion_no_convergence_info=len(_ion_blind),
                        reason=f'이온 수렴 정보가 **없는** 팔 {len(_ion_blind)}개 '
                               f'({_ion_blind[0]} …) — 봉인 이전 세대 payload 다 (CDXR2-4).  '
                               f'이온축이 결론이면 재실행할 것; σ_e 만 보려면 '
                               f'`--require-ionic` 을 끄면 된다'), info

    return None, info


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
    #  ★ 2026-08-25 (Codex 재리뷰 조건 5) — 계약 검증은 **공용 함수**다.
    #    `compare_dirs()` 도 같은 것을 부른다 (옛 판은 하나도 안 돌렸다).
    _hold, _info = validate_contract(arms, seed_ensemble=seed_ensemble,
                                     require_arms=require_arms,
                                     require_ionic=require_ionic,
                                     require_digest=require_digest)
    out.update(_info)
    if _hold:
        return dict(out, **_hold)
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
                    reason=f'비의 상대 origin-위상 산포 {se_ratio_rel_pct:.2f} % > '
                           f'{SE_MAX_REL_PCT} % — '
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
                #  ★ 2026-08-25 (SELF-11) — SDCP 접촉 브리지도 규약 축이다 (0 = 생산).
                sdcp_bridge_um=0.0,
                #  ★ 2026-08-25 (G2) — PTFE 이온 차단 노브 (0 = 생산 = off).
                ptfe_block_um=0.0,
                #  ★ 2026-08-24 (CDXR2-6) — PTFE 규약.  σ_PTFE 만으로는 exact-zero 와
                #    미스탬프가 구분되지 않으므로 규약 자체가 고정 인자다.
                ptfe_stamp='off', ptfe_zero_dof=False,
                #  ★ 2026-08-25 (CDXR3-3) — 현행 세대는 규약 id 를 항상 기록한다.
                #  ★★★ R3-CX-03: id 는 **손으로 적지 않는다**.  아래에서 raw manifest 로
                #    계산해 넣는다 — 임의 문자열을 넣으면 그것이 곧 Codex 가 통과시킨
                #    "garbage id" 상태이고, 픽스처가 그 구멍을 지키게 된다.
                physics_protocol_match=True,
                periodic_xy=False, plate_rule='p2-occupied-surface-first',
                # ★ 2026-08-19 (A5) — 세대 인자도 픽스처에 싣는다.  안 실으면 위와 같은
                #   이유로 새 게이트가 selftest 에서 **검증된 적 없는 코드**가 된다.
                additive_E_GPa={'VGCF': 10.0, 'PTFE': 0.3, 'SDCP': 23.6},
                sigma_ion_se_S_cm=0.003, sigma_ion_sdcp_S_cm=0.001,
                sigma_am_s_S_cm=0.010, sigma_am_p_S_cm=0.005, cam='nmc811',
                temp_c=25.0, ea_ion_ev=0.29, mpm_seed=3,
                se_E_GPa=1.53, se_nu=0.49, se_sigma_y_GPa=0.30,
                #  ★ 2026-08-25 (A1) — σ 표에 들어가는 셋 (규약 축)
                sigma_superp_S_cm=5.0, sigma_swcnt_S_cm=0.0, swcnt_ion_block=False,
                #  ★ 2026-08-25 (A1 2차) — 침대 기하·SE 출처 (규약 축)
                dilate_z=1.0, se_source='npy',
                #  ★ 2026-08-25 (R3-CX-06, ㊷ 가 잡음) — 현행 팔은 이 둘도 항상 싣는다.
                #    픽스처에 없으면 "전부 없음" 이라 세대-혼합 게이트가 발화하지 않아
                #    생성된 거동 시험이 **거짓 통과**한다.
                code_sha='abc1234')
    #  ⚠ `input_digest` 는 **침대마다 달라야** 한다 (같으면 같은 침대를 읽는 것이다,
    #    FA-06/㉙d) — 그래서 `_FIX` 공통이 아니라 `mk()` 가 침대별로 넣는다.

    #  ★★★ 2026-08-25 (R3-CX-03) — 픽스처의 **raw manifest** 를 만들고 id 를 그것에서
    #    계산한다.  판정기는 저장값을 믿지 않고 재계산해 대조하므로, 픽스처도 실제
    #    payload 처럼 원본을 갖고 있어야 한다 (그렇지 않으면 정상 팔이 전부 HOLD 다).
    def _stamp_pid(man):
        """raw manifest 에 **계산된** `physics_protocol_id` 를 박아 돌려준다.

        ★ R3-CX-03: 판정기가 저장값을 믿지 않고 재계산해 대조하므로, 픽스처도 실제
          payload 처럼 계산값을 실어야 한다.  손으로 적으면 그것이 곧 Codex 가
          통과시킨 stale/garbage 상태이고, 픽스처가 그 구멍을 지킨다."""
        #  현행 producer 는 **19 축을 전부** 적는다.  픽스처가 일부만 적으면 재계산이
        #  `unknown:` 이 되고, 그 상태는 "옛 세대" 지 "현행 팔" 이 아니다.  ⇒ 빠진 축을
        #  현행 기본값으로 채워 **완비된 현행 팔**을 흉내낸다 (옛 세대 시험은 따로 있다).
        _DEF = {'periodic_xy': False, 'plate_rule': 'p2-occupied-surface-first',
                'sigma_superp_S_cm': 5.0, 'sigma_swcnt_S_cm': 0.0, 'swcnt_ion_block': False,
                'sigma_ion_se_S_cm': 0.003, 'sigma_ion_sdcp_S_cm': 0.001,
                'sigma_am_s_S_cm': 0.010, 'sigma_am_p_S_cm': 0.005,
                'cam': 'nmc811', 'temp_c': 25.0,
                'dilate_z': 1.0, 'se_source': 'npy',
                'sdcp_bridge_um': 0.0, 'ptfe_block_um': 0.0}
        for _k, _v in _DEF.items():
            man.setdefault(_k, _v)
        #  ★ 2026-08-25 (R4-CX-02) — 파일 픽스처는 전부 이 함수를 지난다.  **현행 세대**로
        #    만드는 것도 여기서 한다 (각 픽스처가 따로 적으면 또 갈라진다 = R3 의 뿌리).
        man.setdefault('schema_version', _RC.SCHEMA_VERSION)
        man.setdefault('component_plan', {'electronic': True, 'ionic': False,
                                          'thermal': False, 'pore': False,
                                          'collector': False})
        man.setdefault('components', {'electronic': {'status': 'complete',
                                                     'backend': {'used': 'gpu'}}})
        man.setdefault('ptfe_cells_observed', 0)      # 도장 off = PTFE 0개 침대 (정상)
        man['physics_protocol_id'] = _RC.physics_protocol_id(man)
        return man

    _FIX_MAN = {k: _FIX[k] for k in _RC.PROTOCOL_FIELDS if k in _FIX}
    _FIX_MAN['vox_um'] = _FIX['vox']
    #  ★ 2026-08-25 (R4-CX-02) — 픽스처는 **현행 세대**다 (schema 3 + 계획).  안 그러면
    #    새 계약이 픽스처에서 한 번도 안 돈다 = 또 "선언만 있고 시험 안 됨".
    #    ⚠ 옛 세대(schema 2)를 시험하는 회귀는 스스로 그 상태를 만든다.
    _FIX_MAN['schema_version'] = _RC.SCHEMA_VERSION
    _FIX_MAN['component_plan'] = {'electronic': True, 'ionic': False, 'thermal': False,
                                  'pore': False, 'collector': False}
    _FIX_MAN['components'] = {'electronic': {'status': 'complete',
                                             'backend': {'used': 'gpu'}}}
    _FIX_MAN['ptfe_cells_observed'] = 0           # ptfe_stamp='off' 와 일관 (정상 침대)
    _FIX['physics_protocol_id'] = _RC.physics_protocol_id(_FIX_MAN)
    _FIX_MAN['physics_protocol_id'] = _FIX['physics_protocol_id']
    _FIX['_manifest'] = _FIX_MAN

    #  ★ 2026-08-20 (CDXIJ-10 ①) — 픽스처가 **origin 을 갖는다**.  팔 계약이 origin 기록·
    #    unique·두 침대 집합 동일을 요구하므로, 없는 픽스처는 (옳게) 전부 HOLD 가 된다.
    #  ★★ R5-CX-04 — 픽스처를 **사전등록 factorial** 로 바꿨다.  옛 판은 z-only 라
    #    "임의의 8점이 통과한다" 는 결함을 정상 증인으로 고정하고 있었다 (Codex 지적).
    _FIX_VOX = _FIX['vox']
    def _ori(i):
        _e = expected_origins(_FIX_VOX)
        return list(_e[i % len(_e)])

    def mk(sbe, dbe, cg=0, resid=1e-8, **over):
        f = dict(_FIX, **over)
        #  ★ R4-CX-02 — 행마다 `_step3` 도 만든다 (component 증거 계약이 그것을 본다).
        #    ⚠ 실제 payload 처럼 **행의 값과 일치**시킨다 — 안 그러면 계약이 픽스처의
        #      다른 수를 보고 통과/실패해 시험이 뜻을 잃는다.
        def _mk_row(bed, i, v, dig):
            _m = dict(f.get('_manifest') or {})
            _r = dict(f, file=f'p2_{bed}_a{i}.json', sigma_e=v, cg_info=cg,
                      cg_resid=resid, unconverged=False, origin_shift_um=_ori(i),
                      **({} if 'input_digest' in over else {'input_digest': dig}))
            _r['_step3'] = {'manifest': _r.get('_manifest') or _m,
                            'sigma_e_eff_S_cm': v, 'n_dof': 5000,
                            'cg_info': cg, 'cg_resid': resid, 'unconverged': False}
            return _r
        return {'SBE': [_mk_row('SBE', i, v, 'AA') for i, v in enumerate(sbe)],
                'DBE': [_mk_row('DBE', i, v, 'BB') for i, v in enumerate(dbe)]}

    base = [1.0000, 1.0020, 0.9980, 1.0010, 0.9990, 1.0005, 0.9995, 1.0000]
    chk('① 미수렴이 하나라도 있으면 HOLD (숫자를 내지 않는다)',
        verdict(mk(base, base, cg=1))['decision'] == 'HOLD')
    chk('② 비 1.08 → h0', verdict(mk(base, [v * 1.08 for v in base]))['decision'] == 'h0')
    v1 = verdict(mk(base, [v * 1.015 for v in base]))
    chk(f'③ 비 1.015 → h1 ({v1["ratio"]})', v1['decision'] == 'h1')
    chk('④ 비 1.035 (중간대) → 둘 다 기각',
        verdict(mk(base, [v * 1.035 for v in base]))['decision'] == 'BOTH_REJECTED')
    noisy = [1.0, 1.10, 0.90, 1.08, 0.92, 1.06, 0.94, 1.0]      # 산포 큼
    chk('⑤ origin-위상 산포가 크면 판정 보류 (origin 을 늘리라고 말한다)',
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
    import glob as _gl22
    import json as _js22
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
              #  ★ R3-CX-03: id 는 손으로 적지 않는다 — 아래 `_stamp_pid` 가 raw manifest 에서
              #    계산해 넣는다 (손으로 적은 값 = Codex 가 통과시킨 'garbage id' 상태).
              'physics_protocol_match': True,
              'backend_last_solve': {'requested': 'gpu', 'used': 'gpu',
                                     'fallback_reason': None, 'precond': 'jacobi'},
              'components': _comps(),
              #  ★ R4-CX-02 — 파일 픽스처도 **현행 세대**다 (schema 3 + 계획).
              'schema_version': _RC.SCHEMA_VERSION,
              #  ⚠ 이 픽스처는 **전자축 전용**이다 (thermal 수치를 안 싣는다).  계획을
              #    거기에 맞춘다 — 안 그러면 픽스처가 자기모순이고, 그 모순을 계약이
              #    옳게 잡는데 시험이 "기준선 실패" 로 읽는다.
              'component_plan': {'electronic': True, 'ionic': False, 'thermal': False,
                                 'pore': False, 'collector': False}}
    _stamp_pid(_man22)

    def _write_dir(_d, drop=None):
        """8팔 × 2침대를 **실제 payload JSON** 으로 쓴다.  `drop` 키는 매니페스트에서 뺀다."""
        for _k, _vals in (('SBE', base), ('DBE', [v * 1.12 for v in base])):
            for _i, _v in enumerate(_vals):
                _m = {kk: vv for kk, vv in _man22.items() if kk != drop}
                #  ★ R3-CX-03: 규약 축을 지우면 **재계산이 unknown** 이 되므로 저장된
                #    id 도 같이 지운다 (그래야 "옛 세대 payload" 를 정직하게 흉내낸다 —
                #    축은 없는데 id 만 최신인 것이 곧 Codex 의 stale mutant 다).
                if drop in _RC.PROTOCOL_FIELDS:
                    _m.pop('physics_protocol_id', None)
                if drop == 'backend':
                    #  ★ 2026-08-25 (R4-CX-02) — **backend 기록만** 지운다.  `components` 를
                    #    통째로 지우면 "계획한 component 가 없다" 로 먼저 걸려 이 시험이
                    #    다른 것을 재게 된다 (needle 이 `backend` 인데 사유는 plan 이었다).
                    _m.pop('backend_last_solve', None)
                    _m['components'] = {_c: {_k2: _v2 for _k2, _v2 in (_cv or {}).items()
                                             if _k2 != 'backend'}
                                        for _c, _cv in (_m.get('components') or {}).items()}
                _m['origin_shift_um'] = list(expected_origins(_m.get('vox_um', 0.15))[_i % 8])
                with open(os.path.join(_d, f'p2_{_k}_sph_a{_i}.json'), 'w',
                          encoding='utf-8') as _f:
                    json.dump({'mpm_metrics': {'step3': {
                        'sigma_e_eff_S_cm': _v, 'cg_info': 0, 'cg_resid': 1e-8,
                        'unconverged': False, 'manifest': _m}}}, _f)

    with _tf22.TemporaryDirectory() as _d22:
        _write_dir(_d22)
        _v22ok = verdict(collect(_d22)[1])
        chk(f'㉒ 기준선 — 기록 완비 파일 16개는 판정이 난다 ({_v22ok["decision"]}: '
            f'{(_v22ok.get("reason") or "")[:110]})',
            _v22ok['decision'] in ('h0', 'h1', 'BOTH_REJECTED'))
    for _f in ('sigma_vgcf_S_cm', 'sigma_sdcp_S_cm', 'sdcp_sphere_d_um',
               'backend', 'sdcp_yield_to_vgcf', 'sigma_ptfe_S_cm'):
        with _tf22.TemporaryDirectory() as _d22:
            _write_dir(_d22, drop=_f)
            _v22 = verdict(collect(_d22)[1])
        chk(f'㉒ **실제 JSON** 에서 `{_f}` 키를 지우면 HOLD ({_v22["decision"]}: '
            f'{(_v22.get("reason") or "")[:80]})',
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
              #  ★ R3-CX-03: id 는 손으로 적지 않는다 — 아래 `_stamp_pid` 가 raw manifest 에서
              #    계산해 넣는다 (손으로 적은 값 = Codex 가 통과시킨 'garbage id' 상태).
              'physics_protocol_match': True,
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
                          origin_shift_um=list(expected_origins(_FIX['vox'])[_i % 8]))
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
        #  ⚠ 일부러 factorial **밖** — '집합이 다르다' 시험용 (그 게이트가 먼저 문다)
        _r['origin_shift_um'] = [0.0, 0.0, round(1.0 + 0.01 * _i, 9)]
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
    _ig = dict(sigma_ion=5.6e-4, ion_cg_info=0, ion_unconverged=False, ion_resid=1e-9)     # 봉인된 정상 팔
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
    #  ★ R3-CX-03: 판정기는 **raw manifest 로 재계산**하므로 평탄 키만 바꾸면 안 된다.
    #    실제 옛 payload 는 축 자체가 없다 ⇒ 매니페스트에서 축을 뺀다.
    _m36b = {k: v for k, v in _FIX_MAN.items() if k not in ('vox_um', 'bridge_um')}
    _m36b['physics_protocol_id'] = 'unknown:bridge_um,vox_um'
    _v36b = verdict(mk(base, [v * 1.12 for v in base],
                       physics_protocol_id=_m36b['physics_protocol_id'],
                       _manifest=_m36b))
    chk(f'㊱b ★ 규약을 **확정할 수 없으면** HOLD (필드가 빠졌다) '
        f'{_v36b["decision"]}/{_v36b.get("hold_code")}',
        _v36b['decision'] == 'HOLD' and _v36b.get('hold_code') == 'PROTOCOL_UNKNOWN')
    _mix36 = mk(base, [v * 1.12 for v in base])
    #  ★ 규약이 실제로 갈린 팔 = **raw 축이 다른** 팔 (id 만 손으로 바꾼 것은 R3-CX-03 의
    #    stale mutant 이고 그것은 ㊱h 가 따로 본다).
    _m36c = _stamp_pid(dict(_FIX_MAN, vox_um=0.125))
    for _r36 in _mix36['DBE']:
        _r36['physics_protocol_id'] = _m36c['physics_protocol_id']
        _r36['_manifest'] = _m36c
        _r36['vox'] = 0.125
    _v36c = verdict(_mix36)
    chk(f'㊱c ★ 규약이 갈린 팔이 섞이면 HOLD ({_v36c["decision"]}: '
        f'{(_v36c.get("reason") or "")[:60]})',
        _v36c['decision'] == 'HOLD'
        and any(_t in (_v36c.get('reason') or '')
                for _t in ('physics_protocol_id', 'vox')))
    #  ★★★ ㊱h (R3-CX-03) — **stored id 만 손으로 바꾼** 팔.  raw 축은 그대로다.
    #    Codex 실측: 옛 판은 "서로 같으니 통과" 였고, 전부 `"garbage"` 여도 통과했다.
    for _lbl36, _bad36 in (('손으로 쓴 값', 'p2-handwritten00'), ('쓰레기', 'garbage')):
        _mh = mk(base, [v * 1.12 for v in base])
        for _k36 in _mh:
            for _r36h in _mh[_k36]:
                _r36h['physics_protocol_id'] = _bad36
                _r36h['_manifest'] = dict(_FIX_MAN, physics_protocol_id=_bad36)
        _vh = verdict(_mh)
        chk(f'㊱h ★★ stored id 가 {_lbl36} 이면 HOLD — **팔끼리 같아도**.  '
            f'문자열 일치는 규약 일치가 아니다 ({_vh["decision"]}/{_vh.get("hold_code")})',
            _vh['decision'] == 'HOLD' and _vh.get('hold_code') == 'PROTOCOL_ID_STALE')
    #  ★ 축 키가 아예 없는 옛 세대 (Codex 의 16-팔 mutant)
    _mo = mk(base, [v * 1.12 for v in base])
    _mano = {k: v for k, v in _FIX_MAN.items() if k not in ('periodic_xy', 'plate_rule')}
    _mano['physics_protocol_id'] = 'p1-old17fieldhash0'
    for _k36 in _mo:
        for _r36o in _mo[_k36]:
            _r36o['physics_protocol_id'] = _mano['physics_protocol_id']
            _r36o['_manifest'] = _mano
    _vo = verdict(_mo)
    chk(f'㊱i ★★ 축 키가 **없는** 옛 세대는 HOLD (stored 가 `p1-…` 라도) '
        f'({_vo["decision"]}/{_vo.get("hold_code")})',
        _vo['decision'] == 'HOLD' and _vo.get('hold_code') == 'PROTOCOL_UNKNOWN')
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
        _id1 != _id2 and _id1.startswith(_RC.PROTOCOL_SCHEMA + '-'))
    chk('㊱f ★ 같은 인자면 같은 id (결정론)',
        _p36.physics_protocol_id(dict(_man36)) == _id1)
    _man36b = dict(_man36)
    _man36b.pop('vox_um')
    chk('㊱g ★★ 인자가 **빠지면** `unknown:` 을 낸다 (임의 기본값으로 채우지 않는다)',
        _p36.physics_protocol_id(_man36b).startswith('unknown:vox_um'))

    #  ★★★ ㉟ 2026-08-24 (CDXR3-1/4) — **Codex 가 재현한 false-green 을 상주 회귀로**.
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
                                         'origin_shift_um': list(expected_origins(0.15)[_i % 8]),
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
            _rc != 0 and '모드는 하나만' in _o)
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
    _ig2 = dict(sigma_ion=5.6e-4, ion_resid=1e-9)
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
    #  ★★★ ㊲ 2026-08-25 (Codex 재리뷰 M-R3-01/05/06) — 재리뷰가 통과시킨 mutant.
    with _tf.TemporaryDirectory() as _d37:
        _write_arms(_d37)
        for _combo in (('--seal-only', '--compare-dir', _d37),
                       ('--seal-only', '--scan', _d37),
                       ('--collect-only', '--compare-dir', _d37)):
            _rc37, _o37 = _cli(_d37, *_combo, '--expect-differ', 'sdcp_yield_to_vgcf')
            chk(f'㊲a[{_combo[1]}] ★★ 모드 조합은 **거부**된다 — 초판은 배타 검사보다 위의 '
                f'분기로 빠져 결과를 출력하고 exit 0 이었다 (rc={_rc37})',
                _rc37 != 0 and '모드는 하나만' in _o37)
    _rbase = dict(sigma_ion=5.6e-4, ion_cg_info=0, ion_unconverged=False)
    for _lbl, _rs, _want in (('None', None, 'HOLD'), ('1e100', 1e100, 'HOLD'),
                             ('NaN', float('nan'), 'HOLD'), ('음수', -1e-9, 'HOLD'),
                             ('1e-9', 1e-9, 'h0'), ('문턱 1e-6', 1e-6, 'h0'),
                             ('문턱 초과 2e-6', 2e-6, 'HOLD')):
        _kw = dict(_rbase)
        if _rs is not None:
            _kw['ion_resid'] = _rs
        _v37 = verdict(mk(base, [v * 1.12 for v in base], **_kw), require_ionic=True)
        chk(f'㊲b[{_lbl}] 이온 residual — 기대 {_want}, 실제 {_v37["decision"]}',
            _v37['decision'] == _want)
    chk('㊲c ★ 판정기 문턱이 솔버 규약과 **같은 값**이다 (step3_sigma:590 = 1e-6)',
        CG_RESID_MAX == 1e-6)
    #  ★★★ ㉟ 2026-08-25 (CDXR3-1/4) — **Codex 가 재현한 false-green 을 상주 회귀로**.
    #    초판의 ㉜c 는 `seal_lines()` 반환 문자열만 검사해서 CLI preamble·옵션 우선순위·
    #    SE 역산을 전부 놓쳤다 = 이 리포가 여러 번 겪은 "실제 경로를 안 타는 테스트".
    #    ⇒ 여기서는 **CLI 를 subprocess 로 실제 실행**하고 stdout·exit code 를 본다.
    import subprocess as _sp, tempfile as _tf, json as _js, os as _os3, sys as _sys3
    _me = _os3.path.abspath(__file__)

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
    #  ★ 2026-08-25: `_FIX` 가 이제 digest 를 싣는다 (현행 팔) ⇒ "기록이 없는 옛 payload"
    #    는 **명시적으로** 비워야 한다.  픽스처가 현행이 된 만큼 옛 세대 시험은 스스로
    #    옛 상태를 만들어야 한다 (기본값에 기대면 이 시험이 조용히 무력해진다).
    _c6d = mk(base, [v * 1.12 for v in base])
    for _k6 in _c6d:
        for _r6 in _c6d[_k6]:
            _r6['input_digest'] = None
            _r6['code_sha'] = None
    _v26d = verdict(_c6d, require_digest=True)
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
    def _mk2(d, *, yvgcf, sig_vgcf=11.0447, dig=('AA', 'BB'), n=2, dbe_mul=1.42,
                s3=None, **_gen):
        _m0 = {'vox_um': 0.4, 'bridge_um': 0.48, 'fibre_stamp': 'segment',
               'sdcp_stamp': 'point', 'sdcp_sphere_d_um': 0.0,
               'sigma_vgcf_S_cm': sig_vgcf, 'sigma_sdcp_S_cm': 250.0,
               'sdcp_yield_to_vgcf': yvgcf, 'sigma_ptfe_S_cm': 0.0,
               'ptfe_stamp': 'off', 'ptfe_zero_dof': False,
               #  ★ R3-CX-03: id 는 손으로 적지 않는다 — 아래 `_stamp_pid` 가 raw manifest 에서
              #    계산해 넣는다 (손으로 적은 값 = Codex 가 통과시킨 'garbage id' 상태).
              'physics_protocol_match': True,
               'code_sha': 'abc1234', 'components': _comps()}
        _m0.update(_gen)                        # 세대 인자 노브 (㉗e/f 용)
        #  ★ R3-CX-03: 노브를 반영한 **뒤에** id 를 계산한다 (그래야 축이 바뀌면 id 도
        #    바뀌는 실제 거동을 픽스처가 재현한다 — 손으로 적으면 그 결합이 사라진다).
        #  ★ 세대 필드는 **id 를 덮어도** 싣는다 — 안 그러면 "규약 불명" 시험이
        #    schema 부재로 먼저 걸려 **다른 이유로** HOLD 하고, 그 시험이 뜻을 잃는다.
        _pid_over = _gen.get('physics_protocol_id')
        _stamp_pid(_m0)
        if _pid_over is not None:
            _m0['physics_protocol_id'] = _pid_over
        for _k, _mul, _dg in (('SBE', 1.0, dig[0]), ('DBE', dbe_mul, dig[1])):
            for _i in range(n):
                _m = dict(_m0, origin_shift_um=list(expected_origins(_m0['vox_um'])[_i % 8]),
                          input_digest=_dg)
                with open(os.path.join(d, f'p2_{_k}_a{_i}.json'), 'w', encoding='utf-8') as _f:
                    _s3d = {'sigma_e_eff_S_cm': 0.4448190919120597 * _mul, 'cg_info': 0,
                            'cg_resid': 1e-8, 'unconverged': False, 'manifest': _m}
                    _s3d.update(s3 or {})       # ㊳ 용 — step3 수준 노브 (수렴·규약)
                    json.dump({'mpm_metrics': {'step3': _s3d}}, _f)

    _EXP = {'sdcp_yield_to_vgcf'}
    with _tf22.TemporaryDirectory() as _A, _tf22.TemporaryDirectory() as _B:
        _mk2(_A, yvgcf=False, dbe_mul=1.42)          # 대조 = 생산 규약
        _mk2(_B, yvgcf=True, dbe_mul=1.29)           # 실험 = σ-치환 OFF
        _c = compare_dirs(_A, _B, _EXP)
        chk(f'㉗a 정상 증인 — 한 축만 다르면 measured ({_c["decision"]}: '
            f'{(_c.get("reason") or "")[:90]})',
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

    import ast as _ast38
    #  ── ㊳ 2026-08-25 (Codex 재리뷰 조건 5) — **`compare_dirs` 도 계약을 건다** ──────
    #     옛 판은 origin 짝·digest·`_XDIR_FIELDS` 만 봤다.  그래서 `verdict()` 이 HOLD 를
    #     냈을 데이터(미수렴 · `unknown:` 규약 · 필수 필드 부재)에 `measured` 를 냈다.
    #     ⇒ 같은 `validate_contract` 를 부르는지 **행동으로** 확인한다 (구조 검사는 ㊳e).
    for _tag, _s3, _needle in (
            ('㊳a 미수렴 팔이 A 에 있으면 HOLD', {'cg_info': 30000}, '미수렴'),
            ('㊳b 수렴 정보가 없으면 HOLD (blind)',
             {'cg_info': None, 'cg_resid': None, 'unconverged': None}, '수렴 정보'),
            ('㊳c resid 가 문턱을 넘으면 HOLD', {'cg_resid': 2e-6}, '전자 수렴')):
        with _tf22.TemporaryDirectory() as _A, _tf22.TemporaryDirectory() as _B:
            _mk2(_A, yvgcf=False, dbe_mul=1.42, s3=_s3)
            _mk2(_B, yvgcf=True, dbe_mul=1.29)
            _c = compare_dirs(_A, _B, _EXP)
            chk(f'{_tag} ({_c["decision"]})',
                _c['decision'] == 'HOLD' and _needle in (_c.get('reason') or ''))
            chk(f'{_tag[:3]}′ 사유가 **어느 디렉터리**인지 말한다',
                (_c.get('reason') or '').startswith('[디렉터리 A]'))
    #  ★ `unknown:` 규약 — SELF-01 이 실제로 만든 상태다 (모든 런이 그랬다)
    with _tf22.TemporaryDirectory() as _A, _tf22.TemporaryDirectory() as _B:
        _mk2(_A, yvgcf=False, dbe_mul=1.42)
        _mk2(_B, yvgcf=True, dbe_mul=1.29, physics_protocol_id='unknown:vox_um')
        _c = compare_dirs(_A, _B, _EXP)
        chk(f'㊳d ★ `unknown:` 규약이 B 에 있으면 HOLD (SELF-01 이 만든 상태) '
            f'({_c["decision"]}/{_c.get("hold_code")})',
            _c['decision'] == 'HOLD'
            and _c.get('hold_code') in ('PROTOCOL_UNKNOWN', 'PROTOCOL_ID_STALE')
            and (_c.get('reason') or '').startswith('[디렉터리 B]'))
    #  ★ 구조 — 두 게이트가 **같은 함수**를 부른다.  인라인 사본이 다시 생기면 여기서 걸린다.
    #  ⚠ 함수 본문은 **AST 로** 잘라낸다.  문자열 `.index('def verdict(')` 로 자르면
    #    그 리터럴이 **이 시험 자신의 소스**에 있어 자기를 먼저 찾는다 — 실제로 초판이
    #    그래서 ㊳f 가 돌연변이를 놓쳤다 (`ptfe-gate-split` 과 같은 self-referential needle).
    _tree38 = _ast38.parse(_self)
    def _fnsrc(name):
        _f = [x for x in _tree38.body
              if isinstance(x, _ast38.FunctionDef) and x.name == name]
        return _ast38.get_source_segment(_self, _f[0]) if _f else ''
    _vsrc, _csrc = _fnsrc('verdict'), _fnsrc('compare_dirs')
    chk(f'㊳e ★★ `verdict` 가 validate_contract 를 부른다 (인라인 사본 아님, {len(_vsrc)}B)',
        bool(_vsrc) and 'validate_contract(arms,' in _vsrc
        and 'for fld in _GEN_FIELDS:' not in _vsrc)
    chk(f'㊳f ★★ `compare_dirs` 가 같은 validate_contract 를 부른다 ({len(_csrc)}B)',
        bool(_csrc) and 'validate_contract(_ar,' in _csrc)
    def _own_returns(fn):
        """`fn` **자신의** return 노드만 (중첩 def 의 것은 그 함수 소관이다)."""
        out38 = []
        def _w(node, top=False):
            for _ch in _ast38.iter_child_nodes(node):
                if isinstance(_ch, (_ast38.FunctionDef, _ast38.AsyncFunctionDef,
                                    _ast38.Lambda)) and not top:
                    continue
                if isinstance(_ch, _ast38.Return):
                    out38.append(_ch)
                if not isinstance(_ch, (_ast38.FunctionDef, _ast38.AsyncFunctionDef,
                                        _ast38.Lambda)):
                    _w(_ch)
        _w(fn, top=True)
        return out38
    _vcr = [_f for _f in _ast38.parse(_self).body
            if isinstance(_f, _ast38.FunctionDef) and _f.name == '_validate_contract_raw'][0]
    _rets = _own_returns(_vcr)
    #  ── ㊵ 2026-08-25 (R3-CX-04, Codex 3차) — **계획·관측을 소비하는가** ──────────────
    #    Codex 가 통과시킨 두 payload 를 그대로 상주 회귀로 만든다.
    #  ⓐ 계획은 ionic 을 켰는데 component 는 disabled
    _c40 = (mk(base, [v * 1.12 for v in base],
                      component_plan={'electronic': True, 'ionic': True, 'thermal': False,
                                      'pore': False, 'collector': False},
                      components={'electronic': {'status': 'complete'},
                                  'ionic': {'status': 'disabled'}}))
    _v40 = verdict(_c40)
    chk(f'㊵a ★★ 계획한 `ionic` 이 disabled 면 HOLD — 옛 판은 기록만 하고 안 읽어 rc 0 '
        f'이었다 ({_v40["decision"]})',
        _v40['decision'] == 'HOLD' and _v40.get('hold_code') == 'PLAN_NOT_MET')
    #  ⓑ 계획대로 다 complete → 통과 (과잉차단 아님)
    _c40b = (mk(base, [v * 1.12 for v in base],
                       component_plan={'electronic': True, 'ionic': False, 'thermal': False,
                                       'pore': False, 'collector': False},
                       components={'electronic': {'status': 'complete'},
                                   'ionic': {'status': 'disabled'}}))
    chk(f'㊵b ★ 계획이 ionic 을 **끄고** disabled 면 통과 (LEAN=2 생산 경로)',
        verdict(_c40b)['decision'] != 'HOLD'
        or verdict(_c40b).get('hold_code') != 'PLAN_NOT_MET')
    #  ⓒ 도장은 centerline 인데 관측 셀 0
    _c40c = (mk(base, [v * 1.12 for v in base],
                       ptfe_stamp='centerline', ptfe_zero_dof=True, ptfe_cells_observed=0,
                       _manifest=_stamp_pid(dict(_FIX_MAN, ptfe_stamp='centerline',
                                                 ptfe_zero_dof=True,
                                                 ptfe_cells_observed=0))))
    _v40c = verdict(_c40c)
    chk(f'㊵c ★★ PTFE 도장 + 관측 셀 0 이면 HOLD — 미스탬프와 구분되지 않는다 '
        f'({_v40c["decision"]})',
        _v40c['decision'] == 'HOLD' and _v40c.get('hold_code') == 'PTFE')
    _c40d = (mk(base, [v * 1.12 for v in base],
                       ptfe_stamp='centerline', ptfe_zero_dof=True, ptfe_cells_observed=41234,
                       _manifest=_stamp_pid(dict(_FIX_MAN, ptfe_stamp='centerline',
                                                 ptfe_zero_dof=True,
                                                 ptfe_cells_observed=41234))))
    chk('㊵d ★ 관측 셀이 있으면 통과 (과잉차단 아님)',
        verdict(_c40d).get('hold_code') != 'PTFE')
    #  ★ R4-CX-02 — **부재·음수·오타입도** 잡는다 (옛 판은 `==0` 만 봐서 삭제로 꺼졌다)
    for _pv, _pl in ((None, '키 삭제'), (-1, '음수'), (3.0, 'float'), ('7', '문자열')):
        _mp = dict(_FIX_MAN, ptfe_stamp='centerline', ptfe_zero_dof=True)
        if _pv is None:
            _mp.pop('ptfe_cells_observed', None)
        else:
            _mp['ptfe_cells_observed'] = _pv
        _vp = verdict(mk(base, [v * 1.12 for v in base], ptfe_stamp='centerline',
                         ptfe_zero_dof=True, _manifest=_stamp_pid(_mp)))
        #  ⚠ 타입 위반은 `TYPE` 게이트가 **먼저** 문다 (그것이 더 이른 계약이다) —
        #    둘 중 하나로 HOLD 하면 이 부류는 닫힌 것이다.
        chk(f'㊵e ★★ ptfe_cells_observed {_pl} → HOLD ({_vp["decision"]}/'
            f'{_vp.get("hold_code")})',
            _vp['decision'] == 'HOLD' and _vp.get('hold_code') in ('PTFE', 'TYPE'))

    #  ── ㊶ 2026-08-25 (R3-CX-06) — **파생 id 는 축이 아니다** (과잉·누락 양방향) ────────
    #    Codex 실측 두 건:
    #      ⓐ 과잉차단 — `sdcp_yield_to_vgcf` 한 축만 바꾼 **정상** A/B 를, 파생 id 도
    #         달라졌다는 이유로 별도 고정축 불일치로 세어 HOLD 했다.
    #      ⓑ 누락차단 — raw 축은 그대로 두고 stored id 만 바꿔
    #         `--expect-differ physics_protocol_id` 로 주면 `measured` 가 났다.
    with _tf22.TemporaryDirectory() as _A, _tf22.TemporaryDirectory() as _B:
        _mk2(_A, yvgcf=False, dbe_mul=1.42)
        _mk2(_B, yvgcf=True, dbe_mul=1.29)
        _c41 = compare_dirs(_A, _B, {'sdcp_yield_to_vgcf'})
        chk(f'㊶a ★★ 등록 축이 실제로 바뀌면 **파생 id 변화는 결과**다 → measured '
            f'({_c41["decision"]}: {(_c41.get("reason") or "")[:60]})',
            _c41['decision'] == 'measured')
    #  ⓑ raw 축은 같은데 id 만 다르다 = 기록이 손으로 바뀐 것
    with _tf22.TemporaryDirectory() as _A, _tf22.TemporaryDirectory() as _B:
        _mk2(_A, yvgcf=False, dbe_mul=1.42)
        _mk2(_B, yvgcf=False, dbe_mul=1.29, physics_protocol_id='p2-handedited00000')
        _c41b = compare_dirs(_A, _B, {'sdcp_yield_to_vgcf'})
        chk(f'㊶b ★★ raw 축은 같은데 id 만 다르면 HOLD ({_c41b["decision"]})',
            _c41b['decision'] == 'HOLD')


    #  ── ㊹ 2026-08-25 (A2) — **선언 밖 매니페스트 키 훑기** ────────────────────────────
    #    A1 에서 producer 에 새 축을 실었더니, `PROTOCOL_FIELDS` 에는 들어가는데
    #    `FIELD_CONTRACT` 에는 안 들어가 **cross-dir 에서 자유롭게 달라져도 measured** 인
    #    상태가 드러났다 (`periodic_xy`·`plate_rule` 은 R4 부터, σ_SuperP·σ_SWCNT·
    #    `swcnt_ion_block`·`dilate_z`·`se_source` 는 A1 부터 그 상태였다).
    #    ⇒ ⓐ 구조 불변식으로 재발을 막고 ⓑ 거동을 두 방향으로 문다.
    _ALIAS = {'vox_um': 'vox'}          # 리더가 접는 이름 (레지스트리는 짧은 이름을 쓴다)
    _pf_miss = sorted(f for f in _RC.PROTOCOL_FIELDS
                      if _ALIAS.get(f, f) not in FIELD_CONTRACT)
    chk(f'㊹a ★★ 규약 축은 **전부** `FIELD_CONTRACT` 에 있다 (누락: {_pf_miss})',
        not _pf_miss)
    #  ⓑ-1 분류되지 않은 키 — **값이 같아도** HOLD 다 ("지금은 우연히 같다" 는 계약이 아니다)
    #  ⚠ 두 디렉터리를 **완전히 같게** 둔다 — 등록 축을 같이 바꾸면 파생 id 차이를 다루는
    #    앞 루프가 먼저 물어(다른 이유로 HOLD) 이 시험이 뜻을 잃는다 (배터리가 '과잉' 으로
    #    잡았다: `CX-06 파생 필드 자동 허용 제거` 가 여기까지 물었다).
    with _tf22.TemporaryDirectory() as _A, _tf22.TemporaryDirectory() as _B:
        _mk2(_A, yvgcf=False, dbe_mul=1.42, brand_new_axis=7)
        _mk2(_B, yvgcf=False, dbe_mul=1.42, brand_new_axis=7)
        _c42 = compare_dirs(_A, _B, _EXP)
        chk(f'㊹b ★★ 분류 안 된 매니페스트 키는 **같아도** HOLD ({_c42["decision"]})',
            _c42['decision'] == 'HOLD' and 'brand_new_axis' in (_c42.get('reason') or ''))
    #  ⓑ-2 R4 이후 규약 축이 된 `periodic_xy` — 등록 없이 달라지면 HOLD
    with _tf22.TemporaryDirectory() as _A, _tf22.TemporaryDirectory() as _B:
        _mk2(_A, yvgcf=False, dbe_mul=1.42, periodic_xy=False)
        _mk2(_B, yvgcf=True, dbe_mul=1.29, periodic_xy=True)
        _c43 = compare_dirs(_A, _B, _EXP)
        chk(f'㊹c ★★ `periodic_xy` 가 등록 없이 두 디렉터리에서 다르면 HOLD '
            f'({_c43["decision"]})',
            _c43['decision'] == 'HOLD' and 'periodic_xy' in (_c43.get('reason') or ''))
    #  ⓒ 리더가 레지스트리 축을 **자동으로** 담는가 (손으로 고르면 또 갈라진다)
    with _tf22.TemporaryDirectory() as _A:
        _mk2(_A, yvgcf=False, periodic_xy=True, dilate_z=1.25, se_source='npy')
        _row = _read(os.path.join(_A, 'p2_SBE_a0.json'))
        chk('㊹d ★★ 리더가 레지스트리 축을 자동으로 담는다 (H5 부류 재발 차단)',
            _row.get('periodic_xy') is True and _row.get('dilate_z') == 1.25
            and _row.get('se_source') == 'npy'
            and all(_row.get(f) is not None for f in ('plate_rule', 'sigma_superp_S_cm')))
    #  ⓓ **그림자 필드**가 부모 없이 혼자 다르면 잡는다 — 이것이 전수 훑기(`_rawd`)의
    #    고유 사정권이다 (레지스트리 축은 앞 루프가 이미 본다).  요청↔적용 기록이
    #    두 디렉터리에서 갈리면 한쪽 팔이 요청과 다른 규약으로 돈 것이다.
    with _tf22.TemporaryDirectory() as _A, _tf22.TemporaryDirectory() as _B:
        _mk2(_A, yvgcf=False, dbe_mul=1.42, fibre_stamp_requested='segment')
        _mk2(_B, yvgcf=False, dbe_mul=1.42, fibre_stamp_requested='point')
        _c44 = compare_dirs(_A, _B, _EXP)
        chk(f'㊹e ★★ 그림자 필드가 부모 없이 다르면 HOLD ({_c44["decision"]})',
            _c44['decision'] == 'HOLD'
            and 'fibre_stamp_requested' in (_c44.get('reason') or ''))
    #  ⓔ **구조 불변식** — 계약된 축을 면제 목록으로 옮기는 길을 막는다.  면제의 사정권은
    #    분류 안 된 키뿐이어야 하고, 계약 ∩ 면제 ≠ ∅ 이면 그 축은 두 규칙 중 느슨한 쪽으로
    #    샌다 (배터리가 이 구멍을 알려 줬다: σ_VGCF 를 '런 결과' 로 적어도 아무 시험도 안 물었다).
    _ovl = sorted((set(MANIFEST_RESULT_KEYS) | set(MANIFEST_DERIVED_OF)) & set(FIELD_CONTRACT))
    chk(f'㊹f ★★ 계약된 축은 면제 목록에 **없다** (겹침: {_ovl})', not _ovl)
    #  ⓕ 합성 SE 구름 — 만드는 것은 자유지만 그것으로 σ 를 주장할 수는 없다

    #  ── ㊺ 2026-08-25 (R5-CX-04) — **origin 은 개수가 아니라 어떤 점인가** ──────────────
    #    Codex 실측: z-only 8점 `[0,0,0.00]…[0,0,0.07]` 이 `require_arms=8` 에서 `h0`.
    #    ⚠ 그리고 **내 픽스처가 바로 그 패턴**이라 결함을 정상 증인으로 고정하고 있었다.
    #      ⇒ 픽스처를 먼저 factorial 로 고치고 게이트를 세웠다 (반대 순서면 또 초록이 난다).
    _hv = _FIX['vox'] / 2.0
    _e8 = expected_origins(_FIX['vox'])
    chk('㊺a factorial 이 8점이고 {0, vox/2}^3 다',
        len(_e8) == 8 and set(_e8) == {(x, y, z) for x in (0.0, _hv)
                                       for y in (0.0, _hv) for z in (0.0, _hv)})
    chk('㊺b 정상 증인 — factorial 픽스처는 통과한다',
        verdict(mk(base, [v * 1.12 for v in base]),
                require_arms=8).get('hold_code') != 'ORIGIN_SET')

    def _mk_ori(oris):
        #  주어진 origin 목록으로 8팔을 만든다 (다른 축은 전부 정상)
        _a = mk(base, [v * 1.12 for v in base])
        for _k in _a:
            for _i, _r in enumerate(_a[_k]):
                _r['origin_shift_um'] = list(oris[_i])
        return _a

    #  ⓐ Codex 가 통과시킨 그 패턴 — 한 축으로 늘어선 8점
    _zonly = [(0.0, 0.0, round(0.01 * i, 9)) for i in range(8)]
    _vz = verdict(_mk_ori(_zonly), require_arms=8)
    chk(f'㊺c ★★ z-only 8점을 **거부**한다 ({_vz["decision"]}/{_vz.get("hold_code")}) — '
        f'개수만 맞는 임의의 점은 위상 앙상블이 아니다 (R5-CX-04)',
        _vz['decision'] == 'HOLD' and _vz.get('hold_code') == 'ORIGIN_SET')
    #  ⓑ 한 점을 factorial **밖** 값으로 대체
    _sub = list(_e8); _sub[3] = (0.0, 0.0, 0.999)
    _vs = verdict(_mk_ori(_sub), require_arms=8)
    chk(f'㊺d ★★ 한 점만 factorial 밖이어도 거부 ({_vs.get("hold_code")})',
        _vs.get('hold_code') == 'ORIGIN_SET')
    #  ⓒ factorial 위이지만 **덜 찬** 경우 (한 점을 중복) — 전량 런은 거부
    _dup = list(_e8); _dup[7] = _e8[0]
    _vd = verdict(_mk_ori(_dup), require_arms=8)
    chk(f'㊺e ★★ factorial 위여도 **덜 차면** 전량 런은 거부 ({_vd.get("hold_code")})',
        _vd['decision'] == 'HOLD')
    #  ⓓ ⚠ 정상 증인 — 팔 수를 줄인 진단 런은 막지 않는다 (부분집합이면 통과)
    _a2 = mk(base[:2], [v * 1.12 for v in base[:2]])
    for _k in _a2:
        for _i, _r in enumerate(_a2[_k]):
            _r['origin_shift_um'] = list(_e8[_i])
    chk('㊺f ★ 정상 증인 — ARMS<8 진단 런은 부분집합이면 통과 (과잉차단 없음)',
        verdict(_a2).get('hold_code') not in ('ORIGIN_SET', 'ORIGIN_VOX'))

    #  ── ㊻ 2026-08-25 (R5-CX-08) — **기각 receipt 는 판정을 멈춘다** ────────────────────
    #    옛 판: 러너가 `.rejected_*` 를 쓰는데 `collect()` 는 `p2_*.json` 만 글롭했다.
    #    실측 — 정상 16팔 디렉터리에 receipt 를 넣기 **전후가 둘 다 `h0`** (Codex).
    #    기록을 남기고 아무도 안 보면 그 기록은 장식이다.
    with _tf22.TemporaryDirectory() as _A:
        _mk2(_A, yvgcf=False, dbe_mul=1.12, n=8)
        _r0, _a0 = collect(_A)
        _v0 = verdict(_a0)
        chk(f'㊻a 정상 증인 — receipt 없으면 판정이 난다 ({_v0["decision"]})',
            _v0.get('hold_code') != 'REJECTED_TREE')
        with open(os.path.join(_A, '.rejected_20260825T000000Z'), 'w', encoding='utf-8') as _rf:
            _rf.write('reason=seal_broken\n')
        _r1, _a1 = collect(_A)
        _v1 = verdict(_a1)
        chk(f'㊻b ★★ 기각 receipt 가 있으면 **판정하지 않는다** '
            f'({_v1["decision"]}/{_v1.get("hold_code")})',
            _v1['decision'] == 'HOLD' and _v1.get('hold_code') == 'REJECTED_TREE')

    #  ── ㊼ 2026-08-31 — **진단 패키지는 판정 대상이 아니다** ────────────────────────────
    #    `reduce_arm_payloads.py --diagnostic` 산출물은 팔 수를 줄인 단일-origin tree 이고
    #    소비자는 `ion_r_verdict.py` 다.  그런데 축소본 파일명이 `p2_*.json` 이라 이 판정기가
    #    **그대로 읽는다** (㊺f 대로 ARMS<8 은 막지 않는다) ⇒ 표지 없이는 부분 cohort 에
    #    판정이 난다.  표지 **둘**을 각각 단독으로 시험한다 — 하나만 남아도 물어야 한다.
    with _tf22.TemporaryDirectory() as _D:
        _mk2(_D, yvgcf=False, dbe_mul=1.12, n=8)
        _rd0, _ad0 = collect(_D)
        chk(f'㊼a 정상 증인 — 표지가 없으면 판정이 난다',
            verdict(_ad0).get('hold_code') != 'DIAGNOSTIC_TREE')
        #  ⓐ 표지 ① 트리 파일만
        with open(os.path.join(_D, '.diagnostic_arms2'), 'w', encoding='utf-8') as _df:
            _df.write('{"arms": 2}\n')
        _vd1 = verdict(collect(_D)[1])
        chk(f'㊼b ★★ 트리 표지만 있어도 거부 ({_vd1.get("hold_code")})',
            _vd1['decision'] == 'HOLD' and _vd1.get('hold_code') == 'DIAGNOSTIC_TREE')
        os.remove(os.path.join(_D, '.diagnostic_arms2'))
        #  ⓑ 표지 ② payload 내부만 (`p2_*.json` 만 복사해 간 경로 = 트리 표지 유실)
        _pq = sorted(_gl22.glob(os.path.join(_D, 'p2_*.json')))[0]
        _pj = _js22.load(open(_pq, encoding='utf-8'))
        _pj.setdefault('step3', {}).setdefault('_reduced', {})['diagnostic'] = {'arms': 2}
        _js22.dump(_pj, open(_pq, 'w'))
        _vd2 = verdict(collect(_D)[1])
        chk(f'㊼c ★★ 트리 표지가 없어도 payload 표지로 거부 ({_vd2.get("hold_code")})',
            _vd2['decision'] == 'HOLD' and _vd2.get('hold_code') == 'DIAGNOSTIC_TREE')
    #  ⚠ 행의 값과 매니페스트를 **둘 다** 합성으로 둔다 — 실제 `_read` 는 매니페스트에서
    #    행 필드를 채우므로, 하나만 바꾸면 픽스처가 실제 경로와 어긋난다.
    _vpx = verdict(mk(base, [v * 1.12 for v in base], se_source='proxy:0.27@192',
                      _manifest=_stamp_pid(dict(_FIX_MAN, se_source='proxy:0.27@192'))))
    chk(f'㊹g ★★ 합성 SE 구름(proxy) 팔은 HOLD ({_vpx["decision"]}/{_vpx.get("hold_code")})',
        _vpx['decision'] == 'HOLD' and _vpx.get('hold_code') == 'SE_PROXY')
    #  ⚠ 정상 증인 — 실 점구름(`npy`)은 막히지 않는다 (과잉차단 확인)
    _vnp = verdict(mk(base, [v * 1.12 for v in base]))
    chk(f'㊹h 정상 증인 — `se_source=npy` 는 통과 ({_vnp["decision"]})',
        _vnp.get('hold_code') != 'SE_PROXY')

    #  ── ㊷ 2026-08-25 (R3-CX-06, Codex 3차) — **레지스트리에서 거동을 생성한다** ────────
    #    Codex 가 독립 pass-mutant 셋으로 증명했다 — `physics_protocol_id.required` 를
    #    뒤집어도, `temp_c.across_dir` 을 뒤집어도, `_GEN_FIELDS` 에서 `temp_c` 를 지워도
    #    **selftest 126/126 이 초록**이었다.  선언만 있고 **거동이 시험되지 않았다**.
    #    ⇒ 목록을 하나로 파생시키고(`generation=True`), 여기서 레지스트리를 **읽어**
    #      필드마다 선언대로 무는지 확인한다.  선언을 바꾸면 시험이 따라 바뀐다 =
    #      "선언과 거동" 이 갈라질 자리가 없어진다.
    _sw_bad = []

    def _one_arm_missing(fld):
        """DBE 팔 하나에서 `fld` 를 뺀 8팔 (평탄 + 매니페스트 둘 다)."""
        _c = mk(base, [v * 1.12 for v in base])
        _c['DBE'][0] = dict(_c['DBE'][0])
        _c['DBE'][0][fld] = None
        _mm = {k: v for k, v in _FIX_MAN.items() if k != fld}
        _c['DBE'][0]['_manifest'] = _mm if fld in _RC.PROTOCOL_FIELDS else _FIX_MAN
        return _c

    def _one_arm_differs(fld, alt):
        _c = mk(base, [v * 1.12 for v in base])
        _c['DBE'][0] = dict(_c['DBE'][0], **{fld: alt})
        if fld in _RC.PROTOCOL_FIELDS:
            _c['DBE'][0]['_manifest'] = _stamp_pid(dict(_FIX_MAN, **{fld: alt}))
        return _c

    _ALT = {str: 'ALT', float: 9.75, int: 4321, bool: True, dict: {'ZZ': 1.0}, type(None): 'ALT'}
    for _f, _d in sorted(FIELD_CONTRACT.items()):
        _cur = _FIX.get(_f)
        _alt = _ALT.get(type(_cur), 'ALT')
        if isinstance(_cur, bool):
            _alt = not _cur
        #  ⓐ `required=True` → 그 필드가 **없는** 팔이 있으면 HOLD
        if _d.get('required'):
            _v = verdict(_one_arm_missing(_f))
            if _v['decision'] != 'HOLD':
                _sw_bad.append(f'{_f}: required 선언인데 부재가 통과 ({_v["decision"]})')
        #  ⓑ 같은 디렉터리 안에서 **달라지면** HOLD (scope 별로 범위가 다르다)
        if _d.get('scope') in ('physics', 'numeric', 'bed') and _cur is not None:
            _v = verdict(_one_arm_differs(_f, _alt))
            if _v['decision'] != 'HOLD':
                _sw_bad.append(f'{_f}: scope={_d["scope"]} 인데 팔간 차이가 통과 '
                               f'({_v["decision"]})')
        #  ⓒ `generation=True` → 기록이 **섞이면** HOLD (전부 없으면 통과 = ⑲ 규약)
        if _d.get('generation'):
            _v = verdict(_one_arm_missing(_f))
            if _v['decision'] != 'HOLD':
                _sw_bad.append(f'{_f}: generation 선언인데 혼합이 통과 ({_v["decision"]})')
    chk(f'㊷a ★★★ 레지스트리 {len(FIELD_CONTRACT)} 필드의 **선언대로** 무는가 '
        f'(위반: {_sw_bad[:2]}{"…" if len(_sw_bad) > 2 else ""})',
        not _sw_bad)
    #  ⓓ cross-dir: `across_dir=True` 인 필드가 두 디렉터리에서 다르면 HOLD
    #  ⚠ 주입이 **판정기의 리더에 실제로 보이는지** 먼저 확인한다.  안 보이는 축을
    #    조용히 건너뛰면 "시험했다" 가 거짓이 된다 (이 파일이 여러 번 겪은 부류).
    #    보이지 않으면 그것 자체를 위반으로 보고한다 — 픽스처를 고치라는 뜻이다.
    _XAXIS = 'sdcp_yield_to_vgcf'         # 등록 축 (여기서 다른 것이 **정상**이다)
    #    필드 → 매니페스트에 어떻게 써야 `_read` 가 보는가 (평탄 키가 아닌 것만)
    #  ⚠ 리더가 **평탄 키와 다른 이름**으로 읽는 축은 여기 적는다.  안 적으면 위 가드가
    #    "주입이 안 보인다" 로 **실패**시킨다 — 조용히 건너뛰지 않는다 (그것이 이 sweep 의
    #    요점이다: 시험하지 못한 축은 통과가 아니다).
    _INJ = {'backend': lambda v: {'backend_last_solve': {'requested': 'gpu', 'used': v,
                                                        'precond': 'jacobi'},
                                  'components': {'electronic': {
                                      'status': 'complete',
                                      'backend': {'used': v, 'precond': 'jacobi'}}}},
            'vox': lambda v: {'vox_um': v},          # 리더: `man['vox_um'] → r['vox']`
            }
    _xd_bad = []
    for _f in sorted(_XDIR_FIELDS):
        if _f == _XAXIS or FIELD_CONTRACT[_f].get('derived_from'):
            continue          # 등록 축은 달라야 정상 · 파생은 ㊶ 소관
        if _f == 'input_digest':
            continue          # 두 침대는 **반드시** 다르다 (FA-06) — ㉗d 가 짝별로 본다
        _cur = _FIX.get(_f)
        _alt = (not _cur) if isinstance(_cur, bool) else _ALT.get(type(_cur), 'ALT')
        if _f == 'vox':
            _alt = 0.125                       # 숫자 축은 숫자로 (규약 해시에도 들어간다)
        _kw = _INJ[_f](_alt) if _f in _INJ else {_f: _alt}
        with _tf22.TemporaryDirectory() as _A, _tf22.TemporaryDirectory() as _B:
            _mk2(_A, yvgcf=False, dbe_mul=1.42)
            _mk2(_B, yvgcf=True, dbe_mul=1.29, **_kw)
            #  주입이 리더에 보이는가 (안 보이면 이 시험은 아무것도 안 한 것이다)
            #  ⚠ 기준은 **A 디렉터리**다.  `_FIX` 와 비교하면 두 픽스처의 기본값이 다른
            #    축(`vox` 0.15 vs 0.4)에서 "주입이 보였다" 고 **잘못** 판정한다.
            #    실제로 그래서 `vox` 축이 조용히 안 시험되고 있었다 (이 sweep 이 잡았다).
            _sA = {_canon(_r.get(_f)) for _r in collect(_A)[1]['SBE']}
            _sB = {_canon(_r.get(_f)) for _r in collect(_B)[1]['SBE']}
            if _sA == _sB:
                _xd_bad.append(f'{_f}: 주입이 리더에 **안 보인다** (A={_sA} B={_sB}) — '
                               f'픽스처가 이 축을 시험하지 못한다.  `_INJ` 에 이 축의 '
                               f'매니페스트 표기를 추가할 것')
                continue
            _c = compare_dirs(_A, _B, {_XAXIS})
            if _c['decision'] != 'HOLD':
                _xd_bad.append(f'{_f} ({_c["decision"]})')
    chk(f'㊷b ★★ `across_dir` 선언 {len(_XDIR_FIELDS)} 필드가 cross-dir 에서 정말 고정인가 '
        f'(위반: {_xd_bad[:2]}{"…" if len(_xd_bad) > 2 else ""})', not _xd_bad)
    #  ★★★ ㊷d/e — **선언 자체를 뒤집는 mutant** 를 잡는다.  ⓐ~ⓓ 는 선언에서 시험을
    #    생성하므로, 선언을 뒤집으면 그 필드가 **시험 대상에서 빠져** 조용히 초록이 된다
    #    (Codex 실측: `required=True→False` · `across_dir=True→False` 둘 다 126/126 PASS).
    #    ⇒ 선언과 **무관한** 불변식을 따로 건다.
    #  ⓓ **거동으로** 건다 (플래그가 아니라).  규약 축이 매니페스트에서 빠진 팔은
    #    `protocol_ok` 의 재계산이 `unknown:` 을 내므로 HOLD 여야 한다 — 이 경로는
    #    `required`/`across_dir` 선언과 **무관**하다.  그래서 선언을 뒤집어도 안 뚫린다.
    #    ⚠ 세대 축(σ_AM·temp_c…)은 일부러 `required` 가 아니다 (옛 팔 호환, ⑲/㉖f).
    #      그렇다고 규약이 느슨해지는 것은 아니다 — 규약 재계산이 따로 잡는다.
    _pf_bad = []
    for _f in _RC.PROTOCOL_FIELDS:
        _cD = mk(base, [v * 1.12 for v in base])
        _mD = {k: v for k, v in _FIX_MAN.items() if k != _f}
        _mD['physics_protocol_id'] = _FIX['physics_protocol_id']   # stored 는 그대로 (stale)
        for _kD in _cD:
            for _rD in _cD[_kD]:
                _rD['_manifest'] = _mD
        _vD = verdict(_cD)
        if _vD['decision'] != 'HOLD':
            _pf_bad.append(f'{_f} ({_vD["decision"]})')
    chk(f'㊷d ★★★ 규약 축 {len(_RC.PROTOCOL_FIELDS)} 개가 매니페스트에서 빠지면 **전부** '
        f'HOLD (선언과 무관한 재계산 경로) — 위반: {_pf_bad[:2]}',
        not _pf_bad)
    #  ★★★ 2026-08-25 (R5-CX-07, Codex 5차) — 옛 판은 **세대 축 ∪ 규약 축**만 봤다.
    #    `backend` 는 `scope='numeric'` 이라 그 밖이었고, 그래서 `backend.across_dir` 을
    #    True→False 로 뒤집어도 **selftest 146 PASS / FAIL 0** 이었다 (Codex 실측).
    #    그 상태에서는 GPU↔CPU cross-directory 차이가 비교축에서 **사라진다**.
    #  ⇒ 불변량을 **레지스트리 전체**로 넓힌다.  근거: 축이 두 디렉터리에서 달라지는 것은
    #    런마다 `expect_differ` 로 **허가**하는 것이지, 계약에 영구히 적어 두는 것이 아니다.
    #    ⇒ `FIELD_CONTRACT` 의 모든 항목은 `across_dir` 이어야 한다 (예외를 두려면 왜
    #      그 축만 영구히 자유로운지 여기 적어야 한다).
    _nx = sorted(f for f, v in FIELD_CONTRACT.items() if not v.get('across_dir'))
    #  ★ ㊷f — `physics_protocol_id.required` 는 **중복 방어**다.  이 플래그를 꺼도
    #    `protocol_ok` 의 재계산이 저장값 부재를 HOLD 로 잡는다 (아래에서 실측한다).
    #    Codex 가 "이 플래그를 뒤집어도 selftest 가 초록" 이라고 지적한 것은 사실이고,
    #    그 이유가 **구멍이 아니라 중복**임을 여기서 명시한다 — 다만 두 겹을 유지하려면
    #    플래그가 켜져 있어야 하므로 그것도 같이 못 박는다 (조용히 한 겹이 되지 않게).
    _cF = mk(base, [v * 1.12 for v in base])
    _mF = {k: v for k, v in _FIX_MAN.items() if k != 'physics_protocol_id'}
    for _kF in _cF:
        for _rF in _cF[_kF]:
            _rF['physics_protocol_id'] = None
            _rF['_manifest'] = _mF
    _vF = verdict(_cF)
    chk(f'㊷f ★★ 저장된 규약 id 가 **없으면** HOLD — `required` 플래그와 무관한 '
        f'재계산 경로 ({_vF["decision"]}/{_vF.get("hold_code")})',
        _vF['decision'] == 'HOLD' and _vF.get('hold_code') == 'PROTOCOL_ID_MISSING')
    chk('㊷g ★ 그래도 `required` 플래그는 켜 둔다 (두 겹 유지 — 한 겹이 조용히 사라지지 '
        '않게).  이 시험이 플래그 뒤집기를 잡는 유일한 자리다',
        FIELD_CONTRACT['physics_protocol_id'].get('required') is True)

    chk(f'㊷e ★★★ **레지스트리 전 축**이 `across_dir` 다 (아닌 것: {_nx}) — 선언을 '
        f'뒤집으면 그 축이 cross-dir 비교에서 조용히 빠진다 (R5-CX-07: `backend` 가 '
        f'바로 그 상태였다)',
        not _nx)

    chk(f'㊷c ★★ `_GEN_FIELDS` 가 레지스트리 파생과 **같은 집합**이다 '
        f'(차이: {sorted(set(_GEN_FIELDS) ^ set(_GEN_FIELDS_LEGACY))})',
        set(_GEN_FIELDS) == set(_GEN_FIELDS_LEGACY))

    #  ── ㊸ 2026-08-25 (R4, 배터리가 잡은 구멍) — **각 계약이 홀로 물리는가** ────────────
    #    강화한 배터리가 셋을 `★놓침★` 으로 냈다: 엄격 타입·계획 스키마·PTFE 기록 검사를
    #    각각 꺼도 rc=0 이었다 — **다른 게이트가 대신 물어** 회귀가 그 검사를 인증하지
    #    못했다 (R3-CX-08 에서 `B2` 가 겪은 것과 같은 부류, 이번엔 셋).
    #    ⇒ **그 검사만** 물 수 있는 입력을 준다.
    #  ⓐ 타입 — `periodic_xy` 를 문자열로.  PTFE·계획은 정상이라 `TYPE` 밖에 물 수 없다.
    _v43a = verdict(mk(base, [v * 1.12 for v in base],
                       _manifest=dict(_FIX_MAN, periodic_xy='False')))
    chk(f'㊸a ★★ `periodic_xy="False"`(문자열) → **`TYPE`** 으로 HOLD '
        f'({_v43a["decision"]}/{_v43a.get("hold_code")})',
        _v43a['decision'] == 'HOLD' and _v43a.get('hold_code') == 'TYPE')
    #  ⓑ 계획 스키마 — 키가 **빠진** 계획.  타입·PTFE 는 정상이다.
    _v43b = verdict(mk(base, [v * 1.12 for v in base],
                       _manifest=_stamp_pid(dict(_FIX_MAN,
                                                 component_plan={'electronic': True}))))
    chk(f'㊸b ★★ 계획에 키가 빠지면 **`PLAN`** 으로 HOLD (`plan_ok` 만 물 수 있다) '
        f'({_v43b["decision"]}/{_v43b.get("hold_code")})',
        _v43b['decision'] == 'HOLD' and _v43b.get('hold_code') == 'PLAN')
    #  ⓒ PTFE 기록 — 키를 **지운다**.  타입 검사는 부재를 건너뛰므로 `PTFE` 밖에 없다.
    #  ⚠ `_stamp_pid` 가 `setdefault` 로 다시 채우므로 **찍은 뒤에** 지운다.
    _m43c = _stamp_pid(dict(_FIX_MAN))
    _m43c.pop('ptfe_cells_observed', None)
    _v43c = verdict(mk(base, [v * 1.12 for v in base], _manifest=_m43c))
    chk(f'㊸c ★★ `ptfe_cells_observed` 키 부재 → **`PTFE`** 로 HOLD (타입 검사는 부재를 '
        f'건너뛴다) ({_v43c["decision"]}/{_v43c.get("hold_code")})',
        _v43c['decision'] == 'HOLD' and _v43c.get('hold_code') == 'PTFE')

    #  ── ㊴ 2026-08-25 (Codex 재리뷰 조건 4) — **새 규약 축 둘** ────────────────────────
    #    `periodic_xy` (seam 면이 회로에 드는가) 와 `plate_rule` (CDXR3-6 이 바꾼 결합 규약,
    #    σ_e **절대값**이 달라진다) 이 `PROTOCOL_FIELDS` 에 들어갔다.  판정기는 해시로만
    #    보므로 축이 갈리면 자동으로 잡히지만, **그 성질 자체를 회귀로 못 박는다**.
    _p39 = _p36
    _man39 = {k: 1.0 for k in _p39.PROTOCOL_FIELDS}
    _base39 = _p39.physics_protocol_id(_man39)
    for _ax, _alt in (('periodic_xy', True), ('plate_rule', 'p1-cond-first')):
        chk(f'㊴a ★★ `{_ax}` 이 규약 해시를 가른다 (섞이면 다른 실험이다)',
            _p39.physics_protocol_id(dict(_man39, **{_ax: _alt})) != _base39)
    chk('㊴b ★ 두 축이 PROTOCOL_FIELDS 에 실제로 있다',
        {'periodic_xy', 'plate_rule'} <= set(_p39.PROTOCOL_FIELDS))
    #  ★ plate_rule 은 **솔버가 선언한 값**이어야 한다 (payload 가 지어내면 안 된다)
    _sp39 = _iu36.spec_from_file_location(
        's39', _os36.path.join(_os36.path.dirname(_os36.path.abspath(__file__)),
                               'step3_sigma.py'))
    _s39 = _iu36.module_from_spec(_sp39)
    #  ★★★ 2026-08-25 (R5 잔여, kgy·Codex 양쪽에서 실측) — **환경 부족을 결함처럼 보이게
    #    하지 않는다.**  `step3_sigma` 는 scipy 를 import 하는데, 그것이 없는 인터프리터에서는
    #    이 줄이 **traceback 으로 죽어** `PASS 154 / FAIL 0 / rc=1` 이 됐다.  Codex 5차도 같은
    #    것을 겪고 "environment limitation, not counted as a target failure" 라고 손으로
    #    판단해야 했다 — 그 판단은 **검사기가** 해야 한다.  받는 쪽이 크래시를 보고
    #    "환경 탓인가 결함인가" 를 고민하게 만들면 그 영수증은 증거로 못 쓴다.
    #  ⚠ 건너뛰되 **조용히 통과시키지 않는다** — 무엇을 못 봤는지 이름을 대고 남긴다.
    try:
        _sp39.loader.exec_module(_s39)
        _s39_why = None
    except ImportError as _e39:
        _s39, _s39_why = None, str(_e39)
    if _s39_why:
        chk(f'㊴c (건너뜀 — 이 인터프리터에 solver 의존이 없다: {_s39_why}).  '
            f'⚠ `PLATE_RULE_VERSION` 을 **확인하지 못했다**', True)
    else:
        chk(f'㊴c ★★ `PLATE_RULE_VERSION` 이 솔버에 있고 현행 규약을 가리킨다 '
            f'({getattr(_s39, "PLATE_RULE_VERSION", None)!r})',
            str(getattr(_s39, 'PLATE_RULE_VERSION', '')).startswith('p2-'))

    _nosince = sorted(k for k, _d in FIELD_CONTRACT.items()
                      if _d.get('required') and not _d.get('required_since'))
    chk(f'㊳h ★★ `required` 인 필드는 전부 `required_since` 를 선언한다 (누락: {_nosince})',
        not _nosince)
    chk(f'㊳g ★ 계약 함수의 모든 반환이 (hold, info) 2-튜플이다 (n={len(_rets)})',
        len(_rets) >= 20
        and all(isinstance(_n.value, _ast38.Tuple) and len(_n.value.elts) == 2
                for _n in _rets))

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
               #  ★ R3-CX-03: id 는 손으로 적지 않는다 — 아래 `_stamp_pid` 가 raw manifest 에서
              #    계산해 넣는다 (손으로 적은 값 = Codex 가 통과시킨 'garbage id' 상태).
              'physics_protocol_match': True,
               'code_sha': 'abc1234', 'components': _comps()}
        _stamp_pid(_m0)                       # ★ R3-CX-03: 재계산 대조를 통과하는 현행 팔
        for _k, _mul, _ad, _ad2, _dg in (('SBE', 1.0, s_add, s_add2, s_dig),
                                         ('DBE', 1.12, d_add, d_add2, d_dig)):
            for _i in range(n):
                _m = dict(_m0, origin_shift_um=[0.0, 0.0, _i * 0.075],
                          input_digest=_dg,          # ← additive 와 **분리** (한 번에 하나만)
                          additive_E_GPa=(_ad if _i == 0 or _ad2 is None else _ad2))
                with open(os.path.join(d, f'p2_{_k}_sph_a{_i}.json'), 'w', encoding='utf-8') as _f:
                    json.dump({'mpm_metrics': {'step3': {
                        'sigma_e_eff_S_cm': 0.073 * _mul, 'cg_info': 0, 'cg_resid': 1e-8,
                        'n_dof': 5000, 'unconverged': False, 'manifest': _m}}}, _f)

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
    #  ★★★ 2026-08-25 (Codex 재리뷰 조건 5) — **두 디렉터리 각각이 먼저 계약을 만족해야 한다.**
    #    옛 판은 origin 짝·`input_digest`·`_XDIR_FIELDS` 만 봤다.  그래서 미수렴 팔·세대
    #    혼합·`unknown:` 규약·필수 필드 부재가 **한 건도 안 걸리고** `measured` 가 났다 —
    #    `verdict()` 이 같은 데이터에 HOLD 를 냈을 상황인데도.  ⇒ 같은 `validate_contract`
    #    를 부른다.  검사 목록이 두 곳으로 갈라질 자리가 없다.
    #    ⚠ `require_arms` 는 걸지 않는다 — 감소율 실험은 8팔 사전등록이 아니다 (짝만 맞으면 된다).
    for _tag, _ar in (('A', arms_a), ('B', arms_b)):
        _h, _ = validate_contract(_ar, where=f'디렉터리 {_tag}')
        if _h:
            return dict(out, **_h)
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
                #  ★★★ 2026-08-25 (R3-CX-06) — **파생 필드는 스스로 축이 아니다.**
                #    `physics_protocol_id` 는 raw 축들의 해시다.  등록 축이 정말 달라졌다면
                #    id 가 달라지는 것은 **결과**이지 위반이 아니다.  옛 판은 그것을 별도
                #    고정축 불일치로 세어 정상 한-축 실험을 HOLD 했다 (Codex 실측 과잉차단).
                #    ⇒ 등록 축이 실제로 달라진 경우에만 id 차이를 자동 허용한다.
                #      (등록 축이 안 달라졌는데 id 만 다르면 그것은 여전히 위반이다.)
                if FIELD_CONTRACT.get(fld, {}).get('derived_from') and not same:
                    if any(_canon(ra.get(_x)) != _canon(rb.get(_x)) for _x in expect_differ):
                        continue
                    return dict(out, decision='HOLD',
                                reason=f'{bed} {key} 에서 파생 필드 `{fld}` 가 다른데 등록 축 '
                                       f'{sorted(expect_differ)} 는 **같다** — id 는 raw 축의 '
                                       f'해시이므로 이런 조합은 기록이 손으로 바뀐 것이다 '
                                       f'(R3-CX-06)')
                if fld in expect_differ:
                    if not same:
                        differed.add(fld)
                elif not same:
                    return dict(out, decision='HOLD',
                                reason=f'{bed} {key} 에서 고정 인자 `{fld}` 가 두 디렉터리 사이에 '
                                       f'다르다 ({ra.get(fld)} vs {rb.get(fld)}) — 대조쌍은 '
                                       f'`{sorted(expect_differ)}` **하나만** 달라야 한다.  '
                                       f'prereg v3 STEP 5 가 정확히 이것으로 거짓 경보를 냈다')
            #  ★★★ A2 (2026-08-25) — **선언 밖 키까지** 훑는다.  위 루프는 `_XDIR_FIELDS`
            #    (= 손으로 유지되는 레지스트리)만 본다.  producer 가 새 키를 실었는데
            #    레지스트리에 안 넣으면 그 축은 두 디렉터리 사이에서 **자유롭게 달라져도**
            #    `measured` 가 난다 — R3·R4 가 반복해 잡은 "선언은 있는데 거동이 없다" 의
            #    거울상(선언조차 없다).  ⇒ 매니페스트 전수 대조 + **분류 강제**.
            _ma, _mb = ra.get('_manifest') or {}, rb.get('_manifest') or {}
            _uns = manifest_unswept_keys(_ma, _mb)
            if _uns:
                return dict(out, decision='HOLD',
                            reason=f'{bed} {key} 의 매니페스트에 **아무 계약도 안 지나는** 키가 '
                                   f'있다 {_uns[:8]} — `FIELD_CONTRACT` · `MANIFEST_RESULT_KEYS` · '
                                   f'`MANIFEST_DERIVED_OF` 중 하나로 분류할 것.  분류 없는 축은 '
                                   f'두 디렉터리 사이에서 조용히 달라진다 (A2)')
            _rawd = manifest_raw_diff(_ma, _mb, expect_differ)
            if _rawd:
                return dict(out, decision='HOLD',
                            reason=f'{bed} {key} 에서 등록 밖 축 {_rawd[:8]} 이 두 디렉터리 사이에 '
                                   f'다르다 — 대조쌍은 `{sorted(expect_differ)}` **만** 달라야 한다 '
                                   f'(A2: 레지스트리가 아니라 매니페스트 전수로 본다)')
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
    #  ★★★ 2026-08-25 (M-R3-01, Codex 재리뷰) — **네 모드가 배타다.**  초판은 seal/collect
    #    만 배타로 만들었는데, `--seal-only --compare-dir` 은 배타 검사보다 **위**의 compare
    #    분기로 빠져 ratio·gain·reduction 을 출력하고 exit 0 으로 끝났다 (Codex 실측).
    #    ⇒ 어떤 조합도 결과 분기로 먼저 빠지지 못하게 **첫 줄에서** 막는다.
    _modes = [n for n, v in (('--scan', bool(a.scan)), ('--compare-dir', bool(a.compare_dir)),
                             ('--collect-only', a.collect_only), ('--seal-only', a.seal_only))
              if v]
    if len(_modes) > 1:
        raise SystemExit(f'모드는 하나만 쓸 수 있다 (받은 것: {" ".join(_modes)}).  '
                         f'봉인은 결과를 보지 않는 검사이고 나머지는 결과를 내는 것이다 — '
                         f'섞으면 봉인이 우회된다 (M-R3-01)')
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
        #  ★★★ 2026-08-25 (R3-CX-06) — **파생 필드는 실험 축이 아니다.**  Codex 실측:
        #    raw 축은 그대로 두고 stored id 만 바꿔 `--expect-differ physics_protocol_id`
        #    로 주면 `measured` 가 났다.  id 는 raw 축의 해시이므로 그것을 "바꾼" 실험은
        #    물리 실험이 아니라 **기록 조작**이다.
        _der = sorted(f for f in _exp if FIELD_CONTRACT.get(f, {}).get('derived_from'))
        if _der:
            raise SystemExit(f'`--expect-differ` 에 파생 필드 {_der} 는 쓸 수 없다 — '
                             f'raw 축의 해시이지 독립 축이 아니다.  바꾸려는 raw 축을 '
                             f'직접 등록할 것 (R3-CX-06)')
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
    #  ★ 2026-08-31 — `hold_code` 를 **출력에 싣는다.**  이전에는 사람이 읽는 `reason` 만
    #    나가서, 기계(축약기·패키지 검사기)가 "어느 사유로 막혔는지" 를 stdout 에서
    #    **읽을 수 없었다** — 실측: 진단 tree 격리를 확인하려는 두 검사가 사유 문자열을
    #    못 찾아 둘 다 거짓 실패를 냈다.  코드가 계약이면 코드가 나가야 한다.
    print(f'\n══ 판정 (prereg §5) ══\n  결정: **{v["decision"]}**'
          + (f'  [{v["hold_code"]}]' if v.get('hold_code') else '')
          + f'\n  근거: {v["reason"]}')
    if 'ratio' in v:
        print(f'  σ_e 비 = {v["ratio"]}   (h0 ≥ {H0_MIN_RATIO} · h1 = {H1_RATIO})')
    _rel = v.get('se_ratio_rel_pct', v.get('se_ratio_pct'))     # 옛 payload 호환
    if _rel is not None:
        _abs = v.get('se_ratio_abs_pp')
        _abs_s = f' = 절대 {_abs} %p' if _abs is not None else ''
        print(f'  비의 상대 origin-위상 산포 = {_rel} % (문턱 {SE_MAX_REL_PCT} %, 비대응 = '
              f'게이트 규약){_abs_s}')
    _prel = v.get('se_ratio_paired_rel_pct', v.get('se_ratio_paired_pct'))
    if _prel is not None:
        print(f'  쌍대응(origin-key join) 평균 = {v.get("ratio_paired_mean")} · '
              f'산포 {_prel} % · n = {v.get("n_origin")} 위상')
        print('  ⚠ 이 산포는 **표준오차가 아니다** — 8 위상은 한 침대의 완전 {0,½}³ '
              'factorial 이라 복제 오차 자유도가 0 이다 (R8 Q1).  신뢰구간을 함의하지 않는다.')
    if a.out:
        json.dump({'rows': rows, 'verdict': v}, open(a.out, 'w'), ensure_ascii=False, indent=1)
        print(f'\n  → {a.out}')
    raise SystemExit(0 if v['decision'] in ('h0', 'h1') else 1)
