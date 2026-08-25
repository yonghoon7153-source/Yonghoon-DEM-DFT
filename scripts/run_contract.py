"""**실행 계약의 단일 출처** — producer · `check_arm` · 판정기가 **같은 함수**를 쓴다.

★★★ 왜 (2026-08-25, Codex 3차 R3-CX-01/05/06): 같은 계약이 세 곳에 따로 적혀 있었고
  세 곳 다 조금씩 달랐다.  실제로 난 사고:

  · **payload 자리**가 두 목록에 따로 있었고 한쪽이 `metrics` **오타**였다 →
    `check_arm` 이 **모든 실제 팔을 거부**했다 (생산 전면 차단).  selftest 75/75 는
    초록이었다 — 픽스처가 같은 오타를 쓰고 있었기 때문이다.
  · **수렴 계약**이 `cg_info == 0` 만 봐서 `cg_info = 0.5` 가 통과했다 (`int(ci)` 절삭).
  · **backend** 가 component 를 못 찾으면 다른 component → last-solve 로 내려앉아,
    전자 backend 가 **없는데** ionic 의 gpu 도장으로 통과했다.
  · **수치 증거**를 producer validator 가 안 봐서 `sigma_e=None` · `cg_resid=NaN` ·
    `cg_info=99` 인 payload 가 전부 게시됐다.

⚠ 규칙: 이 파일 밖에서 이 계약을 **다시 적지 않는다**.  새 소비자가 생기면 여기서 import 한다.
  (그 중복이 위 네 사고의 공통 뿌리다.)
"""
from __future__ import annotations

import math

#: payload 안에서 STEP3 결과가 사는 자리.  producer 는 `mpm_metrics['step3']` 에 쓴다
#  (`mpm_webapp_payload.py`, `mpm_metrics['step3'] = step3`).
#  ⚠ `metrics` 는 **의도적으로 없다** — 그 자리에 쓰는 producer 가 없고, 관대하게 받아
#    주면 "자리를 못 찾아 조용히 통과" 와 구분되지 않는다 (R3-CX-01 이 그 상태였다).
STEP3_PATHS = (('mpm_metrics', 'step3'), ('step3',))

#: CG 수렴 문턱.  `step3_sigma.py` 의 `unconv = bool(info) or resid > 1e-6` 과 **같은 값**.
CG_RESID_MAX = 1e-6

#: 항상 필요한 component.  나머지는 run mode 가 정한다 (`required_components`).
ALWAYS_REQUIRED = ('electronic',)


def dig(obj, path):
    for k in path:
        if not isinstance(obj, dict) or k not in obj:
            return None
        obj = obj[k]
    return obj


def step3_of(payload):
    """payload dict → step3 dict.  자리를 못 찾으면 None (조용히 0 을 만들지 않는다)."""
    for p in STEP3_PATHS:
        got = dig(payload, p)
        if isinstance(got, dict):
            return got
    return None


#: ★★★ **CLI 회계** (A1, R4-CX-03 잔여) — payload 의 CLI 옵션이 **어디서 설명되는가**.
#   값은 `(범주, 대응 규약 필드들|None)` 이다.
#
#     'protocol' — `PROTOCOL_FIELDS` 축으로 기록된다 (규약 해시에 들어간다).
#                  필드명을 **직접** 적는다 — 이름 규칙 추측 금지.  한 옵션이 여러 축을
#                  움직이면 (`--ptfe-stamp` → `ptfe_stamp` + `ptfe_zero_dof`) 전부 적는다.
#     'derived'  — 물리를 바꾸지만 그 효과가 **다른 규약 축에 흡수**된다.  흡수하는 축을
#                  적는다.  예: `--ea-ion-ev` 는 `sigma_ion_se_S_cm` 을 그 자리에서
#                  재척도해 기록하므로, 별도 축이 없어도 규약이 그것을 말한다.
#     'plan'     — `component_plan` 이 담는다 (무엇을 돌리기로 했는가)
#     'numeric'  — 수치 방법 (backend/precond/maxiter — 해에 영향, 규약은 아님).
#                  매니페스트의 `backend` 기록이 담는다.
#     'solve'    — σ_e/σ_ion **밖 채널**의 solve 를 바꾼다 (thermal k · STEP4 i0 · Joule).
#                  이득 판정이 비교하지 않는 축이라 해시에 없다 — 대신 **여기 적혀야** 한다.
#     'input'    — 입력 데이터.  내용은 `input_digest`(실제로 읽은 파일들의 해시)가 덮는다.
#     'report'   — 보고 스칼라만 바꾼다 (porosity/thickness/coverage 권위값).  해에 영향 없음.
#     'mode'     — 산출물 **형태**만 바꾼다 (미리보기 해상도·rasterize-only·selftest).
#     'record'   — 값이 기록으로만 남는다 (origin 처럼 별도 게이트가 본다)
#
#  ⚠ 새 옵션을 추가하면 여기 **반드시** 한 줄 적어야 한다 — 규칙 M 이 **실제 파서**를
#    잡아 미등재 옵션을 오류로 낸다.
#  ★★ 2026-08-25 (A1 2차) — 초판은 ⓐ payload 파일만 AST 로 훑고 ⓑ 이름 조각
#    (`CLI_PHYSICS_HINT`) 으로 "물리 후보" 를 골랐다.  **둘 다 새는 필터**였다:
#    ⓐ `--temp-c`·`--ea-ion-ev` 는 `se_material.temperature_argparse(ap)` 가 **다른 모듈**
#      에서 등록해 AST 에 안 보였고 (그래서 `--temp-c` 가 M_STALE 로 나왔다),
#    ⓑ `--k-carbon`·`--i0-a-m2`·`--joule-heat`·`--dilate-z` 는 이름에 조각이 없어
#      "후보" 조차 아니었다.  ⇒ 초판의 초록은 **가짜 보증**이었다.
#    지금은 파서를 **실행해서** 잡고(부분집합 필터 없음), `--help` 를 뺀 **전 옵션**이
#    등재를 요구한다.
CLI_ACCOUNTING = {
    # ── protocol (규약 해시 축) ─────────────────────────────────────────────
    '--step3-vox': ('protocol', ('vox_um',)),
    '--step3-bridge-um': ('protocol', ('bridge_um',)),
    '--step3-fibre-stamp': ('protocol', ('fibre_stamp',)),
    #  ★ 한 옵션이 두 축을 움직인다 — 지름을 주면 도장이 sphere 로 바뀐다.
    '--step3-sdcp-sphere-d': ('protocol', ('sdcp_sphere_d_um', 'sdcp_stamp')),
    '--step3-sdcp-yield-to-vgcf': ('protocol', ('sdcp_yield_to_vgcf',)),
    #  ★ `ptfe_zero_dof` = (스탬프 ON) ∧ (σ_PTFE == 0) — 두 옵션이 함께 정한다.
    '--ptfe-stamp': ('protocol', ('ptfe_stamp', 'ptfe_zero_dof')),
    '--sigma-ptfe': ('protocol', ('sigma_ptfe_S_cm', 'ptfe_zero_dof')),
    '--sigma-vgcf': ('protocol', ('sigma_vgcf_S_cm',)),
    '--sigma-sdcp': ('protocol', ('sigma_sdcp_S_cm',)),
    '--sigma-superp': ('protocol', ('sigma_superp_S_cm',)),
    '--sigma-swcnt': ('protocol', ('sigma_swcnt_S_cm',)),
    '--swcnt-ion-block': ('protocol', ('swcnt_ion_block',)),
    '--sigma-ion-se': ('protocol', ('sigma_ion_se_S_cm',)),
    '--sigma-ion-sdcp': ('protocol', ('sigma_ion_sdcp_S_cm',)),
    '--sigma-am-s': ('protocol', ('sigma_am_s_S_cm',)),
    '--sigma-am-p': ('protocol', ('sigma_am_p_S_cm',)),
    '--cam': ('protocol', ('cam',)),
    #  ★ 온도는 자기 축으로도 남고 (혼합-T 게이트가 본다) σ_ion(SE) 도 재척도한다.
    '--temp-c': ('protocol', ('temp_c', 'sigma_ion_se_S_cm')),
    '--periodic': ('protocol', ('periodic_xy',)),
    #  ★★ 2026-08-25 (A1 2차, 신규 적발) — **침대 기하를 바꾸는데 규약에 없었다.**
    #    `vc.load_am(a.scaffold, dz=a.dilate_z)` 의 결과가 그대로 `_s3.rasterize` 로
    #    들어간다 (payload:988 → :1403).  `input_digest` 는 **파일 내용**만 덮으므로
    #    같은 scaffold 를 다른 dz 로 늘린 두 팔이 digest 동일로 통과한다.
    '--dilate-z': ('protocol', ('dilate_z',)),
    #  ★★ 같은 부류 — SE 점구름이 **합성**일 수 있다.  `if a.se_proxy or not a.se:` 라
    #    `--se` 를 **빠뜨리기만 해도** 조용히 proxy 로 내려앉는다 (payload:991).
    #    그 구름이 `se_pts=` 로 rasterize 에 들어가므로 σ 침대 자체가 달라진다.
    #    ⇒ `se_source` 하나로 출처를 적고, 합성일 때만 그 모양(frac@n_vox)을 싣는다
    #      (항상 싣지 않는 이유 = 실침대 팔이 안 쓰는 인자로 거짓 HOLD 되지 않게).
    '--se-proxy': ('protocol', ('se_source',)),
    '--se-frac': ('protocol', ('se_source',)),
    '--n-vox': ('protocol', ('se_source',)),
    # ── derived (효과가 다른 규약 축에 흡수된다) ────────────────────────────
    #  σ_ion(SE) 는 매니페스트에 실릴 때 **이미 아레니우스 재척도된 값**이다
    #  (`a.sigma_ion_se = se_material.scale_sigma_ion(a.sigma_ion_se, a.temp_c, a.ea_ion_ev)`).
    '--ea-ion-ev': ('derived', ('sigma_ion_se_S_cm',)),
    # ── plan (무엇을 돌리기로 했는가 — `component_plan`) ────────────────────
    '--no-ion': ('plan', None), '--no-thermal': ('plan', None),
    '--no-pore': ('plan', None), '--no-collector': ('plan', None),
    '--no-step3': ('plan', None),
    # ── numeric (수치 방법.  해에 영향은 있으나 규약은 아니다) ──────────────
    '--step3-gpu': ('numeric', None), '--step3-amg': ('numeric', None),
    '--step3-maxiter': ('numeric', None),
    # ── solve (σ_e/σ_ion 밖 채널) ───────────────────────────────────────────
    '--k-carbon': ('solve', None),        # thermal k 표 (`_s3.thermal_k_table`)
    '--i0-a-m2': ('solve', None),         # STEP4 교환전류 (σ_e 를 다시 풀지 않는다)
    '--joule-heat': ('solve', None),      # #29 발열맵 — σ 해 뒤의 후처리
    '--no-step4': ('solve', None),
    '--no-trackb': ('solve', None),       # τ_geo 추가 솔브 1회 (σ_e 와 별개)
    # ── input (내용은 `input_digest` 가 덮는다) ─────────────────────────────
    '--scaffold': ('input', None), '--se': ('input', None),
    '--se-dump': ('input', None), '--phase': ('input', None),
    '--dg': ('input', None), '--eps': ('input', None),
    '--metrics-json': ('input', None),
    #  ★ 입력 데이터.  적용 결과는 `fibre_stamp` 가 말하고, 내용은 `input_digest` 가 덮는다.
    #    (파일 경로 자체는 규약이 아니다 — 같은 이름으로 다른 침대를 놓을 수 있으므로
    #     digest 가 정본이다.)
    '--fibre': ('input', None), '--fibre-dia': ('input', None),
    # ── report (보고 스칼라만) ──────────────────────────────────────────────
    '--porosity': ('report', None), '--thickness': ('report', None),
    '--cov-p': ('report', None), '--cov-s': ('report', None),
    '--coverage-um': ('report', None), '--cov-tabor-um': ('report', None),
    '--cov-sub': ('report', None), '--case': ('report', None),
    # ── mode (산출물 형태만.  σ 해에 영향 없음) ────────────────────────────
    '--out': ('mode', None), '--step3-rasterize-only': ('mode', None),
    '--fibre-max': ('mode', None), '--selftest-temperature': ('mode', None),
    '--show-results': ('mode', None), '--allow-partial-step3': ('mode', None),
    '--expect-protocol': ('mode', None), '--expect-physics': ('mode', None),
    '--void-max': ('mode', None), '--tri-step': ('mode', None),
    '--target-porosity': ('mode', None), '--target-coverage': ('mode', None),
    '--se-min-count': ('mode', None), '--denoise': ('mode', None),
    '--smooth': ('mode', None), '--strain-pts': ('mode', None),
    '--additive-pts': ('mode', None), '--field-max-points': ('mode', None),
    '--no-field': ('mode', None), '--save-step4-grid': ('mode', None),
    #  ★ collector 는 **후처리 진단**이다 (σ_e 를 다시 풀지 않는다 — R_int 시나리오 대입).
    '--collector-name': ('mode', None), '--collector-rint': ('mode', None),
    '--collector-scenario': ('mode', None),
    # ── record (기록으로만 남고 **별도 게이트**가 본다) ─────────────────────
    '--step3-origin-shift': ('record', None),
    #  ★ 온도 혼합 허용 = **게이트를 여는 플래그**다.  물리값이 아니라 허가라서 protocol
    #    축이 아니지만, 열면 서로 다른 T 의 σ_ion 이 섞일 수 있으므로 기록으로 남는다.
    '--allow-mixed-t-ionic': ('record', None),
}

#: 회계 범주 어휘.  이 밖의 값은 오타다 (규칙 M 이 거부한다).
CLI_CATEGORIES = ('protocol', 'derived', 'plan', 'numeric', 'solve',
                  'input', 'report', 'mode', 'record')

#: 규약 축인데 **CLI 로 못 바꾸는** 것 = 코드 상수.  여기 적힌 것만 고아 검사에서 빠진다.
PROTOCOL_CODE_CONST = ('plate_rule',)


def cli_protocol_coverage():
    """→ `protocol`/`derived` 회계가 **이름을 대는** 규약 필드 집합."""
    out = set()
    for cat, flds in CLI_ACCOUNTING.values():
        if cat in ('protocol', 'derived') and flds:
            out.update(flds)
    return out


#: 매니페스트 **스키마 세대**.  ★ 3 = component 별 증거(수렴 3필드·backend `used`)와
#  `component_plan` 을 **항상** 싣는 세대.  2 = 그 이전 (전자 top-level 만 실었다).
#  ⚠ 새 필드를 **과거 결과에 소급 필수화하면 과잉차단**이다 (Codex R4 §5).  그래서
#    계약은 세대별로 적용한다 — 옛 세대는 옛 계약(required·protocol·전자 numeric)만 받고,
#    **모르는 세대**(미래 값·비정수)는 HOLD 한다 (fail-closed).
SCHEMA_VERSION = 3
#: 이 계약이 적용되기 시작하는 세대.
EVIDENCE_SINCE_SCHEMA = 3


#: ★★★ **런 영수증** (R5-CX-03, Codex 5차).  러너가 **무엇으로 돌라고 했는지**를 한 곳에
#  적고, cache/fresh/final 세 지점이 전부 그 값을 요구한다.
#
#  ⚠ 왜 필요한가 — Codex 실측: HEAD 가 `edec17a2`, 러너 기본 vox 가 0.15 인데 모든 팔에
#    `vox_um=0.20` · `code_sha=deadbeef` · 임의 digest 를 넣어도 producer·`check_arm`·final 이
#    전부 `None/None/h0` 였다.  러너는 `check_arm` 에 stamp/backend 만 넘기고, final 은
#    digest 의 **존재와 팔 사이 일관성**만 봤다.  ⇒ "팔들이 서로 일치한다" 는 **같이 낡았어도**
#    성립한다 (H4 가 이미 같은 부류였다).  일치는 옳음이 아니다.
#
#  ★ 영수증은 **선언**이고 매니페스트는 **결과**다.  둘을 필드별로 대조하면 어느 축이
#    갈렸는지까지 말할 수 있다 (해시 하나만 비교하면 "다르다" 밖에 못 말한다).
RECEIPT_AXES = ('vox_um', 'bridge_um', 'fibre_stamp', 'sdcp_stamp', 'sdcp_sphere_d_um',
                'sdcp_yield_to_vgcf', 'ptfe_stamp', 'sigma_ptfe_S_cm', 'sigma_vgcf_S_cm',
                'periodic_xy')
#: 영수증이 담지만 **매니페스트 축이 아닌** 것 (따로 대조한다).
RECEIPT_META = ('code_sha', 'origins', 'arms', 'expect_backend')


def expected_origins_for(vox):
    """`vox` → 사전등록 origin factorial `{0, vox/2}³` (정렬된 8튜플).

    ★ 판정기(`sdcp_gain_verdict.expected_origins`)와 **같은 정의**다 — 러너·판정기가
      사본을 두면 갈라진다 (이 리포의 반복 사고).  판정기가 여기서 import 한다."""
    h = round(float(vox) / 2.0, 9)
    if not (h > 0):
        return []
    return sorted({(x, y, z) for x in (0.0, h) for y in (0.0, h) for z in (0.0, h)})


def receipt_digest(rec):
    """영수증 → 짧은 안정 해시.  OUTDIR 이름에 넣어 **캐시가 설정을 넘나들지 못하게** 한다."""
    import hashlib as _h
    import json as _j
    _body = {k: rec.get(k) for k in sorted(set(RECEIPT_AXES) | set(RECEIPT_META))}
    return _h.sha256(_j.dumps(_body, sort_keys=True, ensure_ascii=False,
                              separators=(',', ':')).encode()).hexdigest()[:12]


def receipt_match(rec, man, origin=None):
    """영수증 ↔ 매니페스트 대조 → `(ok, reason|None)`.

    ⚠ **없는 것은 통과가 아니다** — 영수증이 축을 선언했는데 매니페스트에 그 축이 없으면
      그 팔은 무슨 규약으로 돌았는지 확정할 수 없다 = HOLD (H5 와 같은 논리).
    """
    if not isinstance(rec, dict) or not isinstance(man, dict):
        return False, 'RCPT|shape| 영수증이나 매니페스트가 dict 가 아니다'
    for k in RECEIPT_AXES:
        if k not in rec:
            continue                       # 러너가 그 축을 안 정했다 (킷 기본값을 쓴다)
        if k not in man:
            return False, (f'RCPT|{k}|missing| 러너는 이 축을 `{rec[k]!r}` 로 정했는데 '
                           f'매니페스트에 **기록이 없다** — 확인 불가')
        if _canon_num(man[k]) != _canon_num(rec[k]):
            return False, (f'RCPT|{k}|differ| 러너 선언 `{rec[k]!r}` ≠ 결과 `{man[k]!r}` — '
                           f'이 팔은 러너가 의도한 규약으로 돌지 않았다')
    _rs, _ms = rec.get('code_sha'), man.get('code_sha')
    if _rs and _ms and not (str(_ms).startswith(str(_rs)) or str(_rs).startswith(str(_ms))):
        return False, (f'RCPT|code_sha|differ| 러너 `{_rs}` ≠ 결과 `{_ms}` — '
                       f'다른 코드로 돈 팔이 섞였다')
    if origin is not None and rec.get('origins'):
        _o = tuple(round(float(x), 9) for x in origin)
        _known = {tuple(round(float(x), 9) for x in o) for o in rec['origins']}
        if _o not in _known:
            return False, (f'RCPT|origin|alien| {_o} 는 영수증의 origin 일정에 없다 — '
                           f'{len(_known)}개 중 어느 것도 아니다')
    return True, None


def _canon_num(v):
    """수치는 부동소수 표기 차이를 흡수하고, 그 밖은 문자열로 비교한다."""
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return round(float(v), 9)
    return v



def observed_generation(man):
    """매니페스트가 **실제로 담고 있는 것**으로 판정한 세대 → `int|None`.

    ★★★ 2026-08-25 (R5-CX-02, Codex 5차) — **자기신고를 믿으면 안 된다.**
      옛 판은 `schema_version` 숫자 하나로 계약 강도를 정했고, Codex 가 같은 p2
      매니페스트에서 그 한 줄만 `3 → 2` 로 낮춰 ionic/thermal/pore 증거 누락을
      **HOLD → h0** 로 바꿨다 (regime id 는 그대로 `p2-…`).  payload 가 스스로
      validator 를 약하게 만들 수 있었던 것이다.
    ⇒ 세대를 **규약에 묶는다**.  현행 producer 는 `PROTOCOL_FIELDS` 24축을 **전부**
      적으므로, 재계산한 규약 id 가 `unknown:` 없이 깨끗한 `p2-` 면 그 매니페스트는
      **현행 세대**다.  축 하나라도 빼면 `unknown:` 이 되어 `protocol_ok` 가 잡는다
      (즉 이 판정을 피하려면 규약 검사를 대신 실패해야 한다 — 우회로가 아니다).
    """
    if not isinstance(man, dict):
        return None
    pid = physics_protocol_id(man)
    if isinstance(pid, str) and pid.startswith(PROTOCOL_SCHEMA + '-') and 'unknown' not in pid:
        return SCHEMA_VERSION
    return None


def schema_of(man):
    """매니페스트 세대 → `(version|None, reason|None)`.  모르는 모양이면 None.

    ★★ 2026-08-25 (R5-CX-02) — **신고와 관찰이 어긋나면 HOLD** 다.  거짓말은 둘 중
      어느 쪽보다도 강한 신호이므로 낮은 쪽을 채택하지 않는다 (fail-closed).
    """
    v = (man or {}).get('schema_version')
    if type(v) is not int or v < 1:                      # noqa: E721
        return None, f'SCHEMA|{v!r}| schema_version 이 없거나 정수가 아니다'
    if v > SCHEMA_VERSION:
        return None, (f'SCHEMA|{v}| 이 코드가 모르는 미래 세대다 (아는 최신 '
                      f'{SCHEMA_VERSION}) — 모르는 것을 통과시키지 않는다')
    _obs = observed_generation(man)
    if _obs is not None and v < _obs:
        return None, (f'SCHEMA|{v}| **신고({v}) 와 관찰({_obs}) 이 다르다** — 이 매니페스트는 '
                      f'규약 축 {len(PROTOCOL_FIELDS)} 개를 전부 담은 현행 세대인데 낮은 세대를 '
                      f'신고했다.  세대를 낮추면 증거 계약이 꺼지므로 이것은 우회다 (R5-CX-02)')
    return v, None


#: 물리 규약 스키마 판.  ★ 축 집합이 바뀌면 **이 접두사도 올린다** — 안 올리면 옛 팔과
#  새 팔의 id 가 같은 이름공간에 살아 "다른 축 집합인데 문자열만 같다" 를 구분할 수 없다
#  (R3-CX-03: 축을 17 → 19 로 늘렸는데 접두사는 `p1-` 그대로였다).
PROTOCOL_SCHEMA = 'p2'

#: 규약을 정하는 축.  ⚠ **producer 도 소비자도 이 목록 하나만 쓴다** (사본 금지).
PROTOCOL_FIELDS = ('vox_um', 'bridge_um', 'fibre_stamp', 'sdcp_stamp', 'sdcp_sphere_d_um',
                   'sdcp_yield_to_vgcf', 'ptfe_stamp', 'ptfe_zero_dof',
                   'sigma_vgcf_S_cm', 'sigma_sdcp_S_cm', 'sigma_ptfe_S_cm',
                   'sigma_ion_se_S_cm', 'sigma_ion_sdcp_S_cm',
                   'sigma_am_s_S_cm', 'sigma_am_p_S_cm', 'cam', 'temp_c',
                   'periodic_xy', 'plate_rule',
                   #  ★★ 2026-08-25 (A1, R4-CX-03 잔여) — **전자/이온 σ 표에 실제로 들어가는데
                   #    규약에 없던 셋**.  `_sig3` 는 SuperP·SWCNT 를 그대로 쓰고
                   #    (`mpm_webapp_payload.py` ELECTRONIC table), `swcnt_ion_block` 은
                   #    이온 σ 표의 SE 항을 0 으로 만든다.  Codex 가 superp 를 지목했고
                   #    파서 전수 대조로 나머지 둘이 같이 나왔다.
                   'sigma_superp_S_cm', 'sigma_swcnt_S_cm', 'swcnt_ion_block',
                   #  ★★ 2026-08-25 (A1 2차) — **침대 기하·SE 출처**.  둘 다 rasterize 로
                   #    들어가는데 규약에 없었다.  `input_digest` 는 파일 **내용**만 덮으므로
                   #    같은 scaffold 를 다른 `--dilate-z` 로 늘리거나, `--se` 를 빠뜨려
                   #    proxy 구름으로 내려앉은 팔이 digest 동일로 통과한다.
                   'dilate_z', 'se_source')

#: `None` 이 **명시적 OFF** 인 축 (값 부재가 아니다).
PROTOCOL_OFF_OK = ('temp_c',)


def physics_protocol_id(man):
    """적용된 규약 dict → 안정 해시.  **선언이 아니라 결과**다.

    ★★★ 2026-08-25 (R3-CX-03, Codex 3차) — 두 가지를 고쳤다.

    ⓐ **키 부재와 명시적 OFF 를 구분한다.**  옛 판은 `man.get(k)` 라 둘 다 `None` 이었고,
       `temp_c=None (키 있음)` 과 `temp_c 키 없음` 이 **같은 해시**를 냈다 (Codex 실측).
       키가 아예 없으면 그 팔은 그 축을 기록하지 않은 옛 세대이고, 그것은 OFF 가 아니라
       **모름**이다.  ⇒ `in` 으로 존재를 먼저 본다.
    ⓑ **스키마 접두사를 올린다** (`p1-` → `p2-`).  축을 17 → 19 로 늘렸는데 접두사가
       그대로면 옛 id 와 새 id 가 같은 이름공간에 산다.

    ⚠ 값이 하나라도 없으면 `unknown:<빠진 필드>` 를 낸다 (임의 기본값으로 채우지 않는다).
    """
    import hashlib as _hl
    import json as _json
    _v, _miss = {}, []
    for k in PROTOCOL_FIELDS:
        if k not in man:
            _miss.append(k)                       # ★ 키 부재 = 모름 (OFF 가 아니다)
            continue
        val = man[k]
        if val is None:
            if k in PROTOCOL_OFF_OK:
                _v[k] = '__OFF__'                 # 명시적 OFF 는 유효값
            else:
                _miss.append(k)
        else:
            _v[k] = val
    if _miss:
        return 'unknown:' + ','.join(sorted(set(_miss)))
    _canon = _json.dumps(_v, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    return f'{PROTOCOL_SCHEMA}-' + _hl.sha256(_canon.encode('utf-8')).hexdigest()[:16]


def protocol_ok(man):
    """매니페스트 → `(ok, reason|None)`.  **저장된 id 를 믿지 않고 다시 계산한다.**

    ★★★ R3-CX-03: 소비자가 `manifest['physics_protocol_id']` 를 **읽기만** 했다.
      그래서 Codex 가 통과시켰다 —
        · 16 팔 전부 `periodic_xy`/`plate_rule` 키가 **없는데** stored id 는 `p1-…`
        · 팔마다 `periodic_xy` 를 True/False 로 바꿔 놓고 stored id 만 같게
        · 모든 팔에 `physics_protocol_id = "garbage"`
      셋 다 "서로 같으니 통과" 였다.  **문자열 일치는 규약 일치가 아니다.**
    ⇒ raw manifest 로 재계산해 저장값과 대조한다.  다르면 그 기록은 신뢰할 수 없다.
    """
    stored = (man or {}).get('physics_protocol_id')
    recomputed = physics_protocol_id(man or {})
    if not isinstance(stored, str) or not stored:
        return False, f'PROTOCOL_ID_MISSING| 저장된 id 가 없다 (재계산 = {recomputed})'
    if recomputed.startswith('unknown:'):
        return False, (f'PROTOCOL_UNKNOWN| 규약을 확정할 수 없다 — {recomputed} '
                       f'(저장값 {stored!r} 은 그 사실을 숨긴다)')
    if stored != recomputed:
        return False, (f'PROTOCOL_ID_STALE| 저장된 id {stored!r} 가 raw manifest 재계산 '
                       f'{recomputed!r} 와 다르다 — 옛 세대이거나 손으로 쓴 값이다.  '
                       f'문자열 일치는 규약 일치가 아니다 (R3-CX-03)')
    return True, None


#: 축별 **엄격 타입**.  ⚠ registry 가 강제하는 것이지 리더가 관대하게 바꾸는 것이 아니다.
#   R4-CX-05: 리더가 `bool(man.get(...))` 을 써서 JSON 문자열 `"false"` 가 **True** 가 됐고,
#   그 상태의 16팔이 `h0` 로 봉인됐다 (Codex 실측).  강제(coercion)는 기록을 **바꾸는** 것이다.
STRICT_TYPES = {
    'periodic_xy': bool, 'ptfe_zero_dof': bool, 'sdcp_yield_to_vgcf': bool,
    'physics_protocol_match': bool,
    'vox_um': float, 'bridge_um': float, 'sdcp_sphere_d_um': float,
    'sigma_vgcf_S_cm': float, 'sigma_sdcp_S_cm': float, 'sigma_ptfe_S_cm': float,
    'sigma_ion_se_S_cm': float, 'sigma_ion_sdcp_S_cm': float,
    'sigma_am_s_S_cm': float, 'sigma_am_p_S_cm': float,
    'fibre_stamp': str, 'sdcp_stamp': str, 'ptfe_stamp': str, 'cam': str,
    'se_source': str, 'dilate_z': float,
    'plate_rule': str, 'physics_protocol_id': str,
    'ptfe_cells_observed': int,
    'sigma_superp_S_cm': float, 'sigma_swcnt_S_cm': float, 'swcnt_ion_block': bool,
}


def strict_type_ok(man):
    """매니페스트의 축 타입이 선언과 맞는가 → `(ok, reason|None)`.

    ⚠ **강제하지 않고 거부한다.**  `bool("false") == True` 라서 강제는 기록을 바꾼다.
      JSON 왕복에서 타입이 뒤틀린 payload 는 "그 값이었다" 를 증언하지 못한다.
    ⚠ `int` 는 `bool` 을 배제한다 (bool 은 int 의 하위형).
    """
    for k, t in STRICT_TYPES.items():
        if k not in man or man[k] is None:
            continue                     # 부재는 다른 게이트 소관 (required / protocol_ok)
        v = man[k]
        if t is bool:
            if type(v) is not bool:      # noqa: E721
                return False, f'TYPE|{k}| bool 이어야 하는데 {type(v).__name__} ({v!r})'
        elif t is int:
            if type(v) is not int:       # noqa: E721
                return False, f'TYPE|{k}| int 이어야 하는데 {type(v).__name__} ({v!r})'
        elif t is float:
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                return False, f'TYPE|{k}| 수여야 하는데 {type(v).__name__} ({v!r})'
        elif t is str:
            if not isinstance(v, str):
                return False, f'TYPE|{k}| str 이어야 하는데 {type(v).__name__} ({v!r})'
    return True, None


#: `component_plan` 의 정확한 스키마.  ⚠ nonempty 라고 정본으로 믿으면 안 된다 —
#  `{'electronic': True}` 만 적어도 required 가 하나로 줄고, `{'electronic': False}` 면
#  **빈 집합**이 된다 (Codex R4-CX-02 실측: 둘 다 `h0`).
PLAN_KEYS = ('electronic', 'ionic', 'thermal', 'pore', 'collector')


def ptfe_record_ok(man):
    """PTFE 도장 기록 계약 → `(ok, reason|None)`.

    ★★★ 2026-08-25 (R4-CX-02, Codex 4차): 옛 게이트는 `observed == 0` **만** 거부했다.
      그래서 키를 **지우면** 통과했다 (Codex 실측: stamp=centerline + observed 삭제 → h0).
      `== 0` 검사는 값이 있을 때만 도는데, 없애면 그 검사가 안 돈다 = 삭제로 게이트 끄기.
    ⚠ 그렇다고 `observed > 0` 을 무조건 요구하면 **PTFE 가 진짜 0개인 침대**가 막힌다
      (Codex 자신의 §5 과잉차단 경고).  ⇒ 조건부 불변량으로 나눈다:
        · 현행 세대는 이 필드를 **항상 싣는다** (부재 = 위반)
        · 값은 음이 아닌 정수여야 한다 (음수·문자열·float = 위반)
        · 도장이 켜졌는데 0 = "그렸다는 기록은 있는데 격자에는 없다" = 위반
        · 도장이 꺼졌는데 0 = **정상** (PTFE 없는 침대)
    """
    sv, why = schema_of(man)
    if sv is None:
        return False, why
    v = man.get('ptfe_cells_observed')
    if sv >= EVIDENCE_SINCE_SCHEMA and v is None:
        return False, ('PTFE|absent| schema %d 세대는 `ptfe_cells_observed` 를 항상 싣는다 — '
                       '없으면 도장과 실제 효과를 가를 근거가 사라진다 (삭제로 게이트를 '
                       '끄는 경로)' % sv)
    if v is None:
        return True, None                       # 옛 세대는 면제
    if type(v) is not int or v < 0:             # noqa: E721
        return False, f'PTFE|domain| ptfe_cells_observed={v!r} (음이 아닌 정수여야 한다)'
    if man.get('ptfe_stamp') not in (None, '', 'off') and v == 0:
        return False, (f'PTFE|no_effect| `ptfe_stamp={man.get("ptfe_stamp")}` 인데 관측 '
                       f'sid7 셀이 0 이다 — 격자에 아무것도 안 그려졌다.  그 팔의 PTFE '
                       f'규약은 미스탬프와 구분되지 않는다')
    return True, None


def plan_required(man):
    """이 세대는 `component_plan` 을 **반드시** 실어야 하는가 → `(ok, reason|None)`.

    ★ R4-CX-02: 계획을 **지우면** required 를 파생할 수 없어 검사가 통째로 비활성화됐다
      (Codex 실측: plan 삭제 → final `h0`).  "없으면 건너뛴다" 는 삭제로 무력화된다.
      ⇒ 현행 세대는 계획이 **없는 것 자체가 위반**이다.  옛 세대는 면제된다.
    """
    sv, why = schema_of(man)
    if sv is None:
        return False, why
    if sv >= EVIDENCE_SINCE_SCHEMA and man.get('component_plan') is None:
        return False, (f'PLAN|absent| schema {sv} 세대는 `component_plan` 을 항상 싣는다 — '
                       f'없으면 무엇을 돌리기로 했는지 알 수 없고, 그러면 required 검사가 '
                       f'통째로 꺼진다 (삭제로 게이트를 끄는 경로)')
    return True, None


def plan_ok(plan):
    """`component_plan` 스키마 → `(ok, reason|None)`.  키 완비 · bool · electronic 필수."""
    if not isinstance(plan, dict):
        return False, f'PLAN|shape| dict 이어야 하는데 {type(plan).__name__}'
    _miss = [k for k in PLAN_KEYS if k not in plan]
    if _miss:
        return False, f'PLAN|missing| 키가 빠졌다 {sorted(_miss)} (필요: {list(PLAN_KEYS)})'
    _extra = [k for k in plan if k not in PLAN_KEYS]
    if _extra:
        return False, f'PLAN|extra| 모르는 키 {sorted(_extra)}'
    #  ⚠ `.get` — 앞 검사가 꺼져도 **터지지 않는다**.  검사기가 터지면 소비자는
    #    "계약 위반" 이 아니라 "확인 못 함" 을 얻고, 그 둘은 다른 결론이다.
    _bad = [k for k in PLAN_KEYS if type(plan.get(k)) is not bool]   # noqa: E721
    if _bad:
        return False, f'PLAN|type| bool 이 아닌 키 {sorted(_bad)}'
    if plan['electronic'] is not True:
        return False, ('PLAN|electronic| `electronic` 은 **항상** True 다 — 전자축이 이 '
                       '실험의 결론이고, False 로 적으면 required 가 빈 집합이 된다')
    if plan['pore'] and not plan.get('_pnm_implied', True):
        return False, 'PLAN|pore| pore 를 켜면 pnm 도 따라온다'
    return True, None


def conv_ok(cg_info, unconverged, resid):
    """수렴 계약 → `(ok, why)`.  모르는 것·모순·타입 오류는 전부 실패다 (fail-closed).

    ⚠ `type(cg_info) is int` 를 요구한다 — `bool` 은 `int` 의 하위형이라 `isinstance` 로는
      `True` 가 통과하고, `float` 는 `int(0.5) == 0` 으로 **절삭**돼 통과한다.
      Codex 실측: `conv_ok(0.5, False, 1e-9)` 이 옛 판에서 `(True, '')` 였다.
    ⚠ residual 은 **필수**다.  없으면 수렴했는지 모르는 것이고, 모르는 것은 통과가 아니다.
    """
    if cg_info is None or unconverged is None or resid is None:
        return False, 'blind'
    if type(cg_info) is not int:                       # noqa: E721 — bool/float 를 막는 것이 목적
        return False, 'type'
    if type(unconverged) is not bool:                  # noqa: E721
        return False, 'type'
    if isinstance(resid, bool) or not isinstance(resid, (int, float)):
        return False, 'type'
    if unconverged or cg_info != 0:
        return False, 'unconv'
    if not math.isfinite(resid) or resid < 0 or resid > CG_RESID_MAX:
        return False, 'resid'
    return True, ''


def required_components(no_ion=False, no_thermal=False, no_pore=False,
                        no_collector=False, plan=None):
    """run mode → **완료돼야 하는** component 이름들.

    ★ `plan` (매니페스트의 `component_plan`) 이 있으면 **그것이 정본**이다 —
      소비자는 실행 인자를 모르고 매니페스트만 보기 때문이다 (R3-CX-04).
    ⚠ 계획 키 `collector` ↔ component 이름 `collector_geom` 의 불일치를 여기서 흡수한다.
    """
    _MAP = {'electronic': 'electronic', 'ionic': 'ionic', 'thermal': 'thermal',
            'pore': 'pore', 'collector': 'collector_geom'}
    #  ★★★ 2026-08-25 (R4-CX-02) — 계획은 **검증한 뒤** 정본이 된다.  옛 판은 nonempty
    #    면 그대로 믿어 `{'electronic': True}` 가 required 를 하나로 줄였다 (Codex 실측).
    #    스키마가 틀린 계획은 정본이 아니므로 **run mode 로 내려간다** (그리고 호출자가
    #    `plan_ok` 로 따로 거부한다 — 여기서 조용히 통과시키지 않는다).
    #  ★ `pore ⇒ pnm` — pnm 은 계획 키가 아니지만 pore 의 산출물이라 같이 요구한다
    #    (Codex 실측: PNM 이 missing/exception 이어도 최종이 h0 였다).
    if isinstance(plan, dict) and plan and plan_ok(plan)[0]:
        _req = [_MAP[k] for k in _MAP if plan.get(k)]
        if plan.get('pore'):
            _req.append('pnm')
        return tuple(_req)
    req = list(ALWAYS_REQUIRED)
    if not no_ion:
        req.append('ionic')
    if not no_thermal:
        req.append('thermal')
    if not no_pore:
        req.append('pore')
    if not no_collector:
        req.append('collector_geom')
    return tuple(req)


def component_backend(step3, comp):
    """`comp` 자신의 backend.  **폴백하지 않는다** — 없으면 None.

    ⚠ 옛 판은 component 를 못 찾으면 다른 component → last-solve 로 내려갔다.  그래서
      전자 backend 가 **없는데** ionic 의 `gpu` 도장으로 `expect_backend='gpu'` 를
      통과했고, 전자 cpu + ionic gpu 도 통과했다 (Codex 실측 3건).
      다른 component 의 backend 는 이 component 에 대한 증거가 아니다.
    """
    c = ((step3 or {}).get('manifest') or {}).get('components') or {}
    v = c.get(comp)
    if not isinstance(v, dict):
        return None
    b = v.get('backend')
    if isinstance(b, dict):
        #  ★★★ 2026-08-25 (R4-CX-04, Codex 4차) — **`requested` 는 증거가 아니다.**
        #    옛 판은 `b.get('used') or b.get('requested')` 라 `used` 만 지우고
        #    `requested='cpu'` 를 남기면 **실제 사용값으로 위장**됐다 (Codex 실측:
        #    component_backend → 'cpu' · producer reject None · check_arm None · 16팔 h0).
        #    요청은 요청이고 사용은 사용이다 — 폴백이 아니라 **다른 사실**이다.
        b = b.get('used')
    return b if isinstance(b, str) and b else None


def numeric_ok(step3):
    """**계산이 실제로 일어났다는 수치 증거** → `(ok, reason|None)`.

    status 문자열만 보면 계산 없는 자가보고가 통과한다.  Codex 실측: `sigma_e=None` ·
    `cg_resid=NaN` · `cg_info=99` 인 payload 가 전부 `reject_reason = None` 이었다.

    ⚠ 사유는 **안정된 진단 코드**로 시작한다 (`SIGMA_E|` `N_DOF|` `CONV|`).  회귀가
      느슨한 부분문자열이 아니라 코드로 짝지어야 "정확히 그 검사가 물었다" 를 말할 수
      있다 (Codex R3-CX-08).
    """
    s = step3 or {}
    sig, dof = s.get('sigma_e_eff_S_cm'), s.get('n_dof')
    if isinstance(sig, bool) or not isinstance(sig, (int, float)) \
            or not math.isfinite(sig) or sig <= 0:
        return False, f'SIGMA_E| sigma_e_eff_S_cm={sig!r} (유한한 양수여야 한다)'
    if type(dof) is not int or dof <= 0:               # noqa: E721
        return False, f'N_DOF| n_dof={dof!r} (양의 정수여야 한다)'
    ok, why = conv_ok(s.get('cg_info'), s.get('unconverged'), s.get('cg_resid'))
    if not ok:
        return False, (f'CONV|{why}| 전자 수렴 미확인 cg_info={s.get("cg_info")!r} '
                       f'unconverged={s.get("unconverged")!r} cg_resid={s.get("cg_resid")!r}')
    return True, None


#: component → step3 안의 (수렴 필드 3개, 결과 필드) 위치.  ⚠ 전자만 top-level 이다.
#  ⚠ 키 이름은 **producer 실물**에서 확인한 것이다 (추측 금지 — 틀리면 생산 과잉차단).
#    전자만 top-level 이고 thermal/pore 는 자기 블록 안에 있다.
COMPONENT_EVIDENCE = {
    'electronic':     (('cg_info', 'unconverged', 'cg_resid'), 'sigma_e_eff_S_cm', None),
    'ionic':          (('ion_cg_info', 'ion_unconverged', 'ion_resid'),
                       'sigma_ion_eff_S_cm', None),
    'thermal':        (('cg_info', 'unconverged', 'cg_resid'), 'k_eff_W_mK', 'thermal'),
    'pore':           (('cg_info', 'unconverged', 'resid'), 'tau', 'pore'),
}

#: CG 수렴이 없는 component 의 **결과 계약** (R5-CX-05).  기하·위상 산출물이라 수렴이
#  아니라 **무엇이 나왔는가**로 본다.  ⚠ 위치는 producer 안에 있다 — 몰랐던 것이 아니라
#  안 적었던 것이다 (`mpm_webapp_payload.py:2162` · `:1765`).
COMPONENT_RESULT = {
    'pnm': dict(path=('pore', 'pnm'), ints=('n_pores', 'n_throats'),
                reason_means_incomplete=True),
    'collector_geom': dict(path=('collector_geometric',),
                           #  ⚠ `R_geom_ohm_cm2` 는 **정당하게 None** 일 수 있다
                           #    (bare/wetted 중 하나가 reason 을 냈을 때) ⇒ 요구하지 않는다.
                           positives=('wetted_sigma_S_cm', 'bare_sigma_S_cm')),
}


def component_evidence_ok(step3, required):
    """**계획된 component 마다** 수치·수렴·backend 증거가 있는가 → `(ok, reason|None)`.

    ★★★ 2026-08-25 (R4-CX-02, Codex 4차): `numeric_ok` 가 **전자 top-level 만** 봤다.
      그래서 Codex 가 통과시켰다 —
        · thermal/pore `resid=1e100` · `unconverged=True`  → producer None · final h0
        · 계획된 ionic 의 결과·CG·resid **전부 삭제**       → producer None · final h0
      계획했으면 그 축의 증거도 계획의 일부다.
    ⚠ 증거 위치를 모르는 component(pnm·collector_geom)는 **status 로만** 본다 —
      모르는 것을 지어내지 않는다.  그 대신 status 는 위에서 `complete` 를 요구한다.
    """
    s = step3 or {}
    _man = (s.get('manifest') or {})
    _sv, _swhy = schema_of(_man)
    if _sv is None:
        return False, _swhy                       # 모르는 세대 = HOLD
    if _sv < EVIDENCE_SINCE_SCHEMA:
        #  ★ 옛 세대는 이 필드를 **애초에 안 실었다**.  소급 요구는 과잉차단이다
        #    (Codex R4 §5).  전자축은 `numeric_ok` 가, 규약은 `protocol_ok` 가 본다.
        return True, None
    _cmp = (_man.get('components') or {})
    for comp in required:
        #  ★ `not_solvable` = 물리적으로 정의 안 됨 (SE 비퍼콜 등).  **숫자가 없는 것이
        #    정상**이므로 증거를 요구하지 않는다.  대신 그 축으로 결론을 낼 수 없다는 것은
        #    호출자(`--require-ionic` 등)가 따로 본다.
        if (_cmp.get(comp) or {}).get('status') == 'not_solvable':
            continue
        #  ★★★ 2026-08-25 (R5-CX-05, Codex 5차) — **PNM·collector 는 status 만 봤다.**
        #    schema 3 full plan 에서 `step3.pore.pnm` 과 `step3.collector_geometric` 을
        #    **둘 다 지워도** producer/check_arm/final = `None/None/h0` 였다.
        #    "증거 위치를 모른다" 는 것이 옛 주석의 이유였는데, 위치는 producer 안에 있다
        #    (`payload:2162` · `:1765`) — 몰랐던 것이 아니라 **안 적었던** 것이다.
        #  ⚠ 이 둘은 CG 수렴이 없다 (기하·위상 결과) ⇒ 계약 모양이 다르다.
        _rspec = COMPONENT_RESULT.get(comp)
        if _rspec is not None:
            _blk = s
            for _k in _rspec['path']:
                _blk = (_blk or {}).get(_k) if isinstance(_blk, dict) else None
            if not isinstance(_blk, dict):
                return False, (f'EVID|{comp}|block| `step3.' + '.'.join(_rspec['path'])
                               + '` 결과 블록이 없다 — status 만으로는 무엇이 나왔는지 모른다')
            #  ★ 이유만 담아 돌아온 것은 `complete` 가 아니다 (실패를 완료로 적지 않는다)
            if _rspec.get('reason_means_incomplete') and _blk.get('reason'):
                return False, (f'EVID|{comp}|reason| 결과가 이유만 담고 있다 '
                               f'({_blk.get("reason")!r}) — 그것은 `complete` 가 아니다')
            for _kf in _rspec.get('ints', ()):
                _v = _blk.get(_kf)
                if isinstance(_v, bool) or not isinstance(_v, int) or _v < 0:
                    return False, f'EVID|{comp}|result| {_kf}={_v!r} (음이 아닌 정수여야 한다)'
            for _kf in _rspec.get('positives', ()):
                _v = _blk.get(_kf)
                if isinstance(_v, bool) or not isinstance(_v, (int, float)) \
                        or not math.isfinite(_v) or _v <= 0:
                    return False, f'EVID|{comp}|result| {_kf}={_v!r} (유한한 양수여야 한다)'
            continue
        spec = COMPONENT_EVIDENCE.get(comp)
        if spec is None:
            return False, (f'EVID|{comp}|unregistered| 이 component 의 증거 계약이 '
                           f'등록되지 않았다 — 계획했는데 무엇을 확인해야 하는지 모른다면 '
                           f'그것은 통과가 아니라 HOLD 다 (R5-CX-05)')
        (ki, ku, kr), kres, sub = spec
        blk = (s.get(sub) or {}) if sub else s
        if not isinstance(blk, dict):
            return False, f'EVID|{comp}|block| `{sub}` 블록이 없다'
        res = blk.get(kres) if sub else s.get(kres)
        if isinstance(res, bool) or not isinstance(res, (int, float)) \
                or not math.isfinite(res) or res <= 0:
            return False, f'EVID|{comp}|result| {kres}={res!r} (유한한 양수여야 한다)'
        ci = blk.get(ki) if ki else 0
        ok, why = conv_ok(ci, blk.get(ku), blk.get(kr))
        if not ok:
            return False, (f'EVID|{comp}|conv|{why}| {ki}={blk.get(ki)!r} '
                           f'{ku}={blk.get(ku)!r} {kr}={blk.get(kr)!r}')
        if component_backend(s, comp) is None:
            return False, (f'EVID|{comp}|backend| 이 component 의 `used` backend 기록이 '
                           f'없다 — 무엇으로 돌았는지 모르는 결과다')
    return True, None


def _selftest():
    ok = fail = 0

    def chk(c, m):
        nonlocal ok, fail
        ok, fail = (ok + 1, fail) if c else (ok, fail + 1)
        print(('  PASS  ' if c else '  FAIL  ') + m)

    #  ── 자리 ────────────────────────────────────────────────────────────────────
    chk(step3_of({'mpm_metrics': {'step3': {'a': 1}}}) == {'a': 1},
        'A1 producer 자리(`mpm_metrics.step3`)를 읽는다')
    chk(step3_of({'step3': {'a': 1}}) == {'a': 1}, 'A2 평평한 자리도 읽는다')
    chk(step3_of({'metrics': {'step3': {'a': 1}}}) is None,
        'A3 ★★ 옛 오타 자리(`metrics.step3`)는 **읽지 않는다** — 관대하면 R3-CX-01 이 '
        '숨는다')
    chk(step3_of({'mpm_metrics': {}}) is None, 'A4 없으면 None (0 을 만들지 않는다)')

    #  ── 수렴 ────────────────────────────────────────────────────────────────────
    chk(conv_ok(0, False, 1e-9) == (True, ''), 'B1 정상 증인')
    #  ⚠ **코드까지** 본다 (Codex R3-CX-08).  `[0] is False` 만 보면, 타입 검사를 옛
    #    `isinstance` 로 되돌려도 `0.5 != 0` 이 `unconv` 로 대신 물어 **초록**이다 —
    #    그러면 이 시험은 타입 검사를 인증하지 못한다 (실측으로 그랬다).
    for _v, _code, _lbl in ((0.5, 'type', 'float 0.5 (옛 판은 int() 절삭으로 통과시켰다)'),
                            (True, 'type', 'bool True (bool 은 int 의 하위형)'),
                            (None, 'blind', 'None')):
        _o, _w = conv_ok(_v, False, 1e-9)
        chk(_o is False and _w == _code,
            f'B2 cg_info={_lbl} → `{_code}` 로 거부 (받은 것: {_w!r})')
    chk(conv_ok(0, 0, 1e-9)[0] is False, 'B3 unconverged 가 bool 이 아니면 거부')
    for _r, _lbl in ((None, 'None'), (float('nan'), 'NaN'), (float('inf'), 'inf'),
                     (-1e-9, '음수'), (2e-6, '문턱 초과')):
        chk(conv_ok(0, False, _r)[0] is False, f'B4 resid={_lbl} → 거부')
    chk(conv_ok(0, False, CG_RESID_MAX) == (True, ''), 'B5 문턱 **경계값**은 통과')
    chk(conv_ok(30000, False, 1e-9)[1] == 'unconv',
        'B6 ★ cg_info≠0 인데 unconverged=False (모순) → unconv')

    #  ── 수치 증거 ────────────────────────────────────────────────────────────────
    _good = {'sigma_e_eff_S_cm': 0.01, 'n_dof': 5000, 'cg_info': 0,
             'cg_resid': 1e-9, 'unconverged': False}
    chk(numeric_ok(_good) == (True, None), 'C1 정상 증인')
    #  ⚠ **정확한 진단 코드**로 짝짓는다 (Codex R3-CX-08) — 느슨한 부분문자열이면
    #    "다른 검사가 대신 물어서" 통과해도 초록이라 그 검사가 인증되지 않는다.
    for _k, _v, _code, _lbl in (
            ('sigma_e_eff_S_cm', None, 'SIGMA_E|', 'σ_e=None'),
            ('sigma_e_eff_S_cm', float('nan'), 'SIGMA_E|', 'σ_e=NaN'),
            ('sigma_e_eff_S_cm', float('inf'), 'SIGMA_E|', 'σ_e=inf'),
            ('sigma_e_eff_S_cm', 0.0, 'SIGMA_E|', 'σ_e=0'),
            ('sigma_e_eff_S_cm', -1.0, 'SIGMA_E|', 'σ_e<0'),
            ('n_dof', 0, 'N_DOF|', 'dof=0'), ('n_dof', None, 'N_DOF|', 'dof=None'),
            ('n_dof', 5000.0, 'N_DOF|', 'dof 가 float'),
            ('cg_resid', None, 'CONV|blind|', 'resid=None'),
            ('cg_resid', float('nan'), 'CONV|resid|', 'resid=NaN (비유한)'),
            ('cg_resid', 2e-6, 'CONV|resid|', 'resid 문턱 초과'),
            ('cg_info', 99, 'CONV|unconv|', 'cg_info=99'),
            ('cg_info', 0.5, 'CONV|type|', 'cg_info=0.5 (float 절삭)'),
            ('unconverged', True, 'CONV|unconv|', 'unconverged=True')):
        _o, _w = numeric_ok(dict(_good, **{_k: _v}))
        chk(_o is False and str(_w).startswith(_code),
            f'C2 {_lbl} → `{_code}` 로 거부 (옛 producer validator 는 전부 통과시켰다)')

    #  ── backend (폴백 금지) ───────────────────────────────────────────────────────
    def _p(**comps):
        return {'manifest': {'components': comps}}
    chk(component_backend(_p(electronic={'status': 'complete', 'backend': 'gpu'}),
                          'electronic') == 'gpu', 'D1 자기 backend 를 읽는다')
    chk(component_backend(_p(electronic={'status': 'complete'},
                             ionic={'status': 'complete', 'backend': 'gpu'}),
                          'electronic') is None,
        'D2 ★★ 전자 backend 가 없으면 **ionic 의 gpu 를 빌려오지 않는다**')
    chk(component_backend(_p(electronic={'status': 'complete',
                                         'backend': {'used': 'cpu', 'requested': 'gpu'}}),
                          'electronic') == 'cpu',
        'D3 dict backend 는 **실제로 쓴 것**(used)을 읽는다')
    chk(component_backend(_p(electronic={'status': 'complete',
                                         'backend': {'requested': 'cpu'}}),
                          'electronic') is None,
        'D3b ★★ `requested` 만 있고 `used` 가 없으면 None — 요청은 사용의 증거가 아니다 '
        '(R4-CX-04: 옛 판은 requested 로 폴백해 위장을 통과시켰다)')
    chk(component_backend(_p(electronic={'status': 'complete',
                                         'backend': {'used': None, 'requested': 'gpu'}}),
                          'electronic') is None,
        'D3c ★ `used=null` 도 None (JSON 왕복에서 흔한 모양)')
    chk(component_backend({}, 'electronic') is None, 'D4 매니페스트가 없으면 None')

    #  ── required (계획이 정본) ────────────────────────────────────────────────────
    chk(required_components(no_ion=True, no_thermal=True, no_pore=True,
                            no_collector=True) == ('electronic',),
        'E1 LEAN=2 는 전자만 필수')
    chk(set(required_components()) == {'electronic', 'ionic', 'thermal', 'pore',
                                       'collector_geom'}, 'E2 기본은 다섯 전부')
    chk(set(required_components(plan={'electronic': True, 'ionic': False, 'thermal': True,
                                      'pore': False, 'collector': True}))
        == {'electronic', 'thermal', 'collector_geom'},
        'E3 ★ `component_plan` 이 있으면 그것이 정본 (소비자는 실행 인자를 모른다)')
    chk('collector_geom' in required_components(plan={'collector': True}),
        'E4 ★ 계획 키 `collector` ↔ component 이름 `collector_geom` 불일치를 흡수한다')

    #  ── F: 세대 신고 우회 (R5-CX-02, Codex 5차 실측) ────────────────────────────────
    #    같은 p2 매니페스트에서 `schema_version` **한 줄만** 3 → 2 로 낮추면 증거 계약이
    #    통째로 꺼져 `HOLD → h0` 가 됐다.  regime id 는 그대로였다 = payload 가 스스로
    #    validator 를 약하게 만들 수 있었다.
    _fman = {'schema_version': SCHEMA_VERSION}
    _fman.update({k: (0.15 if k == 'vox_um' else 0.48 if k == 'bridge_um'
                      else 0.30 if k == 'sdcp_sphere_d_um'
                      else 1.0 if k == 'dilate_z'
                      else False if k in ('sdcp_yield_to_vgcf', 'ptfe_zero_dof',
                                          'periodic_xy', 'swcnt_ion_block')
                      else 'segment' if k == 'fibre_stamp'
                      else 'sphere' if k == 'sdcp_stamp'
                      else 'off' if k == 'ptfe_stamp'
                      else 'nmc811' if k == 'cam'
                      else 'npy' if k == 'se_source'
                      else 'p2-occupied-surface-first' if k == 'plate_rule'
                      else 25.0 if k == 'temp_c' else 1.0)
                  for k in PROTOCOL_FIELDS})
    chk(physics_protocol_id(_fman).startswith('p2-')
        and 'unknown' not in physics_protocol_id(_fman),
        'F1 픽스처가 **완비된 현행 규약**이다 (그래야 아래 시험이 뜻을 가진다)')
    chk(observed_generation(_fman) == SCHEMA_VERSION,
        'F2 ★ 세대를 **규약 완비**로 관찰한다 (자기신고가 아니라)')
    chk(schema_of(_fman)[0] == SCHEMA_VERSION, 'F3 정상 증인 — 신고=관찰이면 통과')
    for _v in (1, 2):
        _sv, _swhy = schema_of(dict(_fman, schema_version=_v))
        chk(_sv is None and '신고' in (_swhy or ''),
            f'F4({_v}) ★★ 세대를 낮춰 증거 계약을 끄는 우회를 잡는다 (R5-CX-02)')
    #  ⚠ 정상 증인 — **진짜** 옛 세대(새 축이 애초에 없다)는 계속 통과해야 한다.
    #    이것이 없으면 위 게이트가 옛 payload 를 소급 차단한다 (R4 §5 가 경고한 과잉차단).
    _old = {k: v for k, v in _fman.items()
            if k not in ('dilate_z', 'se_source', 'sigma_superp_S_cm',
                         'sigma_swcnt_S_cm', 'swcnt_ion_block')}
    _old['schema_version'] = 2
    chk(schema_of(_old)[0] == 2,
        'F5 ★ 정상 증인 — 진짜 옛 세대는 통과한다 (소급 과잉차단 없음)')

    #  ── G: PNM·collector 결과 계약 (R5-CX-05, Codex 5차 실측) ──────────────────────
    #    schema 3 full plan 에서 `step3.pore.pnm` 과 `step3.collector_geometric` 을
    #    **둘 다 지워도** producer/check_arm/final 이 `None/None/h0` 였다.
    #    옛 주석은 "증거 위치를 모른다" 였는데 위치는 producer 안에 있었다 —
    #    몰랐던 것이 아니라 **안 적었던** 것이다.
    def _g_full():
        _m = dict(_fman)
        _m['component_plan'] = {'electronic': True, 'ionic': True, 'thermal': True,
                                'pore': True, 'collector': True}
        _m['components'] = {c: {'status': 'complete', 'backend': {'used': 'cpu'}}
                            for c in ('electronic', 'ionic', 'thermal', 'pore',
                                      'pnm', 'collector_geom')}
        return {'manifest': _m, 'sigma_e_eff_S_cm': 0.073, 'cg_info': 0,
                'unconverged': False, 'cg_resid': 1e-8,
                'sigma_ion_eff_S_cm': 2e-4, 'ion_cg_info': 0,
                'ion_unconverged': False, 'ion_resid': 1e-8,
                'thermal': {'k_eff_W_mK': 0.5, 'cg_info': 0,
                            'unconverged': False, 'cg_resid': 1e-8},
                'pore': {'tau': 3.1, 'cg_info': 0, 'unconverged': False, 'resid': 1e-8,
                         'pnm': {'n_pores': 1200, 'n_throats': 3400}},
                'collector_geometric': {'wetted_sigma_S_cm': 0.08,
                                        'bare_sigma_S_cm': 0.05}}

    _greq = required_components(plan={'electronic': True, 'ionic': True, 'thermal': True,
                                      'pore': True, 'collector': True})
    chk({'pnm', 'collector_geom'} <= set(_greq), 'G1 전량 계획에 pnm·collector 가 들어간다')
    chk(component_evidence_ok(_g_full(), _greq)[0],
        'G2 정상 증인 — 완비된 결과는 통과한다')
    _gs = _g_full(); _gs['pore'].pop('pnm')
    chk(not component_evidence_ok(_gs, _greq)[0],
        'G3 ★★ `step3.pore.pnm` 을 지우면 잡는다 (Codex 통과 변형)')
    _gs = _g_full(); _gs.pop('collector_geometric')
    chk(not component_evidence_ok(_gs, _greq)[0],
        'G4 ★★ `step3.collector_geometric` 을 지우면 잡는다 (Codex 통과 변형)')
    _gs = _g_full(); _gs['pore']['pnm'] = {'reason': 'no pores found'}
    chk('reason' in (component_evidence_ok(_gs, _greq)[1] or ''),
        'G5 ★ PNM 이 **이유만** 담으면 `complete` 가 아니다')
    _gs = _g_full(); _gs['collector_geometric']['bare_sigma_S_cm'] = 0.0
    chk(not component_evidence_ok(_gs, _greq)[0],
        'G6 ★ collector σ 가 0 이면 잡는다 (유한 양수여야 한다)')
    #  ★★ 그리고 **모르는 component 를 조용히 통과시키지 않는다** — 계획했는데 계약이
    #    없으면 그것은 통과가 아니라 HOLD 다 (이 구멍이 pnm·collector 를 열어 뒀다).
    chk(not component_evidence_ok(_g_full(), tuple(_greq) + ('brand_new_comp',))[0],
        'G7 ★★ 계약이 **등록 안 된** component 를 계획하면 HOLD (조용한 통과 금지)')

    #  ── H: 런 영수증 (R5-CX-03, Codex 5차 실측) ────────────────────────────────────
    #    HEAD 가 `edec17a2`, 러너 기본 vox 0.15 인데 모든 팔에 `vox_um=0.20` ·
    #    `code_sha=deadbeef` · 임의 digest 를 넣어도 producer/check_arm/final 이
    #    `None/None/h0` 였다.  러너의 **의도**가 결과와 대조된 적이 없었다.
    _h8 = [list(o) for o in sorted({(x, y, z) for x in (0.0, 0.075)
                                    for y in (0.0, 0.075) for z in (0.0, 0.075)})]
    _hrec = {'vox_um': 0.15, 'bridge_um': 0.48, 'fibre_stamp': 'segment',
             'sdcp_stamp': 'sphere', 'sdcp_sphere_d_um': 0.30,
             'sdcp_yield_to_vgcf': False, 'ptfe_stamp': 'off', 'sigma_ptfe_S_cm': 0.0,
             'sigma_vgcf_S_cm': 78.54, 'periodic_xy': False,
             'code_sha': 'edec17a2', 'arms': 8, 'expect_backend': 'gpu',
             'origins': _h8}
    _hman = {k: _hrec[k] for k in RECEIPT_AXES}
    _hman['code_sha'] = 'edec17a2'
    chk(receipt_match(_hrec, _hman, origin=_h8[3])[0],
        'H1 정상 증인 — 러너 선언과 결과가 같으면 통과')
    for _k, _v in (('vox_um', 0.20), ('code_sha', 'deadbeef'),
                   ('sdcp_sphere_d_um', 0.40), ('periodic_xy', True),
                   ('sigma_vgcf_S_cm', 100.0), ('fibre_stamp', 'point')):
        _hm = dict(_hman); _hm[_k] = _v
        chk(not receipt_match(_hrec, _hm, origin=_h8[3])[0],
            f'H2({_k}) ★★ 러너 의도와 다른 결과를 **잡는다** (Codex 통과 변형)')
    _hm = dict(_hman); del _hm['vox_um']
    chk('missing' in (receipt_match(_hrec, _hm)[1] or ''),
        'H3 ★ 선언한 축의 기록이 **없으면** HOLD (부재는 통과가 아니다)')
    chk('alien' in (receipt_match(_hrec, _hman, origin=[0.0, 0.0, 0.03])[1] or ''),
        'H4 ★★ 영수증 일정 밖 origin 을 잡는다 (z-only 우회, R5-CX-04 와 두 겹)')
    #  ★ 설정이 다르면 digest 가 다르다 — OUTDIR 이 갈려 캐시가 섞이지 않는다
    chk(receipt_digest(_hrec) != receipt_digest(dict(_hrec, vox_um=0.20)),
        'H5 ★★ 설정이 다르면 영수증 digest 가 다르다 (캐시가 설정을 넘나들지 못한다)')
    chk(receipt_digest(_hrec) != receipt_digest(dict(_hrec, sdcp_sphere_d_um=0.40)),
        'H6 ★ 구 직경만 달라도 digest 가 갈린다 (`.30`/`.40` 이 같은 `_sph` 를 쓰던 구멍)')
    chk(receipt_digest(_hrec) == receipt_digest(dict(_hrec)),
        'H7 digest 는 같은 입력에 안정하다')
    #  ⚠ 정상 증인 — 러너가 **안 정한** 축은 요구하지 않는다 (킷 기본값 경로를 막지 않는다)
    chk(receipt_match({'vox_um': 0.15}, {'vox_um': 0.15, 'bridge_um': 0.9})[0],
        'H8 ★ 영수증이 선언하지 않은 축은 자유다 (과잉차단 없음)')

    print(f'\nrun_contract selftest: {ok}/{ok + fail} PASS'
          + ('' if not fail else '   ✗ 실패 있음'))
    return 0 if not fail else 1


if __name__ == '__main__':
    import sys
    sys.exit(_selftest() if '--selftest' in sys.argv else
             print('사용: python3 scripts/run_contract.py --selftest') or 0)
