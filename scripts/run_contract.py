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

#: CG 수렴 문턱.  `step3_sigma.py` 의 `unconv = bool(info) or not isfinite(resid) or resid > 1e-6` 과 **같은 값**
#  (비유한 잔차 항은 RGL-01 · 10-05 — `conv_ok` 는 처음부터 비유한을 거부했다).
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
    #  ★ 2026-08-25 (SELF-11 / Q-B2) — SDCP 접촉 브리지.  **σ 침대를 바꾸므로 규약 축이다**
    #    (등재를 빠뜨리면 SELF-04 와 같은 결함: 해시에는 없고 cross-dir 검사도 안 지난다).
    '--step3-sdcp-bridge': ('protocol', ('sdcp_bridge_um',)),
    #  ★ 2026-08-25 (G2, D13 원장 ②) — PTFE 이온 차단.  σ 침대(sid 6→9)를 바꾸므로 규약 축.
    '--step3-ptfe-block-um': ('protocol', ('ptfe_block_um',)),
    #  ★★ 2026-08-31 (Codex R16 Q6) — 차단이 **무엇을** 끊는가.  기본 'se' = 옛 거동 비트 동일,
    #    'ion' 은 SDCP(sid 5)도 끊는다 (⇒ 전자 no-op 이 아니다).
    #  ⚠⚠ **물리적으로는 protocol 축인데 `record` 로 둔다 — 그 이유를 여기 남긴다.**
    #    `PROTOCOL_FIELDS` 에 넣으면 위 주석의 규칙대로 `PROTOCOL_SCHEMA` 를 p2 → p3 로
    #    올려야 하고, 그러면 **봉인된 p2 코호트 32팔**(`docs/data/w4_ptfe_centerline_20260827`
    #    · `w4b_ptfe_off_20260827`, Fig 4b 전자값의 감사 근거)이 전부 다른 규약 id 가 된다.
    #    이 축은 `ptfe_block_um = 0`(생산 기본)에서 **무의미**하므로 생산 규약을 바꾸지 않는다.
    #  ⇒ 대신 두 겹으로 막는다: ⓐ `RECEIPT_AXES` 가 코호트 안에서 값이 갈리면 거부하고
    #    ⓑ 매니페스트가 `ptfe_block_cells` 로 **상별 실제 차단 셀 수**를 싣는다 (도장≠실물).
    #  ⛔ **이 축을 생산 규약으로 채택하려면 그때 p3 로 올린다** — 그것이 이 항목의 청구서다.
    '--step3-ptfe-block-scope': ('record', ('ptfe_block_scope',)),
    #  ★ 2026-10-02 (①, CL-81) — 상 경계 계면 저항 (전자 · 이온).  **물리 축**인데 `record` 로 둔다 —
    #    위 `--step3-ptfe-block-scope` 와 같은 이유·같은 청구서: 생산 기본(없음)에서 옛 조립과
    #    비트 동일이라 p2 봉인 코호트의 규약 id 를 바꾸지 않는다.  섞임은 판정기
    #    `FIELD_CONTRACT` (generation 축) 와 `RECEIPT_AXES_NODIGEST` 가 막는다.
    #  ⛔ **생산 규약으로 채택하는 날 p3 로 올린다** (④ 입력 σ 규약 · ⑤ 검증 뒤 · 1저자 결정).
    '--step3-rint-e': ('record', ('interface_rint_e_ohm_cm2',)),
    '--step3-rint-i': ('record', ('interface_rint_i_ohm_cm2',)),
    #  ★ 2026-10-20 (Rint ② S1 · 설계 v1 §7 회계) — 다음 세대 블록 `ca_ext` 의 **물리 칸**.  `PROTOCOL_FIELDS` 밖 (p2 봉인 코호트
    #    32 팔의 id 보존 — `--step3-ptfe-block-scope` 와 같은 청구서) · 블록이 있으면 id 가 `p3ca-` 로 갈린다 (`physics_protocol_id`).
    #    범주 `protocol_ext` = 필드명 'ca_ext.<하위 블록>.<protocol 키>' — 규칙 M 이 그 키가 하위 블록 protocol 정본에 있는지 센다.
    '--step3-face-alpha-channel': ('protocol_ext', ('ca_ext.ptfe_face.channels',)),
    '--step3-face-alpha-dia-law': ('protocol_ext', ('ca_ext.ptfe_face.dia_law',)),
    #  ★ 2026-10-20 (Rint ② B6 · 설계 v1 §4-2 · §5-2 · §7) — S2 탄소 접합 · S3 SDCP 접합 수정자 (`ca_ext.cjunc` · `ca_ext.sdcp_mod`).
    #    켜는 플래그 = 블록의 모델 판 · 값 플래그 = 그 protocol 칸 (정본 = `ca_ext_cjunc` 의 protocol 키) · PROTOCOL_FIELDS 는 그대로.
    '--step3-cjunc': ('protocol_ext', ('ca_ext.cjunc.model',)),
    '--step3-cjunc-rj': ('protocol_ext', ('ca_ext.cjunc.R_j_ohm',)),
    '--step3-cjunc-len-law': ('protocol_ext', ('ca_ext.cjunc.len_law',)),
    '--step3-cjunc-unreg-law': ('protocol_ext', ('ca_ext.cjunc.unreg_law',)),
    '--step3-cjunc-s-min-um': ('protocol_ext', ('ca_ext.cjunc.s_min_um',)),
    #  tol_ff 하나가 tol_P · tol_sj 를 같이 정한다 (설계 §4-1 — 한 숫자 · SBE 에 SDCP 가 없다)
    '--step3-cjunc-tol-ff-um': ('protocol_ext', ('ca_ext.cjunc.tol_ff_um', 'ca_ext.cjunc.tol_P_um', 'ca_ext.cjunc.tol_sj_um',
                                                 'ca_ext.sdcp_mod.tol_sj_um')),
    '--step3-cjunc-ptfe-jlaw': ('protocol_ext', ('ca_ext.cjunc.ptfe_jlaw',)),
    #  ★ Z3 (10-20 · 등록 R §3-1) — 극한 런 표지 (inf 바닥 · zero 천장 · `--step3-cjunc-rj` 과 짝 · 사다리 진단)
    '--step3-cjunc-rj-limit': ('protocol_ext', ('ca_ext.cjunc.rj_limit',)),
    '--step3-sdcp-mod-c': ('protocol_ext', ('ca_ext.sdcp_mod.c',)),
    #  ★ 2026-10-21 (D · 등록 R §5-6 SV 행 · Codex RCA-06 · 1저자 Q4 (가)) — SV 반사실 대조 (같은 침대 · 같은 R_j 에서 SV 융합 면을 끊은
    #    판의 단자 G 비 · 같은 런 안 추가 풀이).  주 σ_e 해를 바꾸지 않는다 (노브 켬 = 주 결과 · 출처 비트 같음 · 시험 SP6) → 규약 id 밖
    #    (`protocol_ext` 아님 · p3ca id 그대로) · 추가 솔브 = `solve` · 요청 = 증거 `ca_ext.cjunc.evidence.sv_counterfactual_request` ·
    #    영수증 선택 칸 `sv_counterfactual` (대조 = `_receipt_ext_problem`) · 문턱 = 사슬 계획 (등록 R §5-6 · producer 는 비만 낸다).
    '--step3-cjunc-sv-cf': ('solve', None),
    #  ★ `ptfe_zero_dof` = (스탬프 ON) ∧ (σ_PTFE == 0) — 두 옵션이 함께 정한다.
    '--ptfe-stamp': ('protocol', ('ptfe_stamp', 'ptfe_zero_dof')),
    '--sigma-ptfe': ('protocol', ('sigma_ptfe_S_cm', 'ptfe_zero_dof')),
    '--sigma-vgcf': ('protocol', ('sigma_vgcf_S_cm',)),
    #  ★ 2026-10-20 (Rint ② Z1 · 설계 v1 §1-2 #1 · #2) — σ_VGCF 를 bulk 에서 **직경 보존 식**으로 만들었다는 기록 (bulk 값 · 식 이름).
    #    σ 자체는 `--sigma-vgcf` (규약 축) 가 정한다 — 이것은 출처 기록이라 `record` (p2 id 불변) · payload 가 같은 식으로 다시 계산해
    #    `--sigma-vgcf` 와 대조한다 (어긋나면 입구 거부) · 섞임은 판정기 `FIELD_CONTRACT` (generation) · 영수증 선택 칸이 본다.
    '--sigma-vgcf-bulk': ('record', ('sigma_vgcf_bulk_S_cm', 'sigma_vgcf_rule')),
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
    #  ★ 2026-10-20 (Rint ② 설계 v1 §6 · N15) — 정지 rtol + 수렴 증서.  해에 영향 (수렴 정도) · 규약 아님 → numeric.
    #    값은 LAST_BACKEND['rtol'] (노브를 켰을 때만) · 증서는 step3['conv_cert'] 로 매니페스트에 남는다.
    '--step3-rtol': ('numeric', None),
    #  ★ `--step3-require-gpu` = **numeric** 이다 (규약 아님).  근거는 "backend 가 σ 를 안
    #    바꾼다" 가 **아니라** — 그것은 미측정이다 (Codex R7 Q4c) — backend 를 **고르는**
    #    플래그가 `--step3-gpu` 이고 이 플래그는 **성공한 GPU 계산을 바꾸지 않기** 때문이다.
    #    GPU 가 죽었을 때 어차피 backend 봉인이 거부할 CPU 결과를 미리 중단할 뿐이다.
    #    ⇒ physics hash 에 넣지 않고, 실제 component backend 는 계속 봉인한다.
    #    ⚠ CPU/GPU σ parity 는 이 리포에서 **측정된 적이 없다** ⇒ 두 backend 를 섞은 cohort
    #      는 금지 (섞으려면 허용오차를 사전등록해야 한다).
    #    ⇒ 규약 해시에 들어가면 안 된다 (넣으면 같은 물리가 두 규약으로 갈린다).
    '--step3-require-gpu': ('numeric', None),
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
    '--selftest-provenance': ('mode', None),
    '--selftest-contract': ('mode', None),
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
                  'input', 'report', 'mode', 'record', 'protocol_ext')

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
                'sdcp_yield_to_vgcf', 'sdcp_bridge_um', 'ptfe_stamp', 'sigma_ptfe_S_cm',
                'sigma_vgcf_S_cm', 'periodic_xy',
                #  ★ 2026-08-30 (R13 C-7 ⓒ/ⓑ) — 두 이온 σ.  물리 축이므로 digest 에 들어간다
                #    (다른 σ = 다른 실험 = 다른 디렉터리).  매니페스트가 이미 같은 이름으로 적는다.
                #  ⚠ SE 는 **기준(T_ref) 키**로 대조한다 — 러너가 선언하는 것이 기준값이고
                #    적용값은 payload 가 온도로 만든다.  적용값 키로 대조하면 25 °C 밖에서
                #    거짓 불일치가 난다 (R14 D-1).  SDCP 는 온도 스케일링을 안 받으므로
                #    (§F1: SDCP Eₐ 앵커 없음) 적용값 = 기준값이라 키가 하나다.
                'sigma_ion_sdcp_S_cm', 'sigma_ion_se_ref_S_cm',
                'ptfe_block_um', 'ptfe_block_scope')
#: 영수증이 담지만 **매니페스트 축이 아닌** 것 (따로 대조한다).
RECEIPT_META = ('code_sha', 'origins', 'arms', 'expect_backend')

#: ★★★ 2026-08-30 — **대조는 하되 digest 에는 안 넣는 축.**
#    왜 따로 두나: `receipt_digest` 는 `RECEIPT_AXES | RECEIPT_META` 를 통째로 해시하므로
#    거기에 키를 하나만 더해도 **모든 기존 설정의 digest 가 바뀐다** → OUTDIR 이름이 바뀌고
#    → 이미 완주한 팔을 못 찾아 **전부 재실행**된다 (이 리포가 `_lean` 접미사를 못 바꾼 이유와
#    같은 제약).  그런데 대조는 필요하다 ⇒ **해시 밖 + 검사 안**.
#  ⚠ `field_requested` 가 첫 사례다.  `--no-field` 는 `component_plan` 에 **없고**
#    (`plan_ok` 이 모르는 키를 거부하므로 거기에 못 넣는다 — 기존 매니페스트가 다 깨진다)
#    러너 접미사 `_lean3`/`_lean4` 로만 갈렸다.  즉 `OUTDIR=` 을 명시하면 **필드 없는
#    lean3 팔이 lean4 요청에 SKIP 으로 통과**한다 (코드리뷰 2026-08-30 지적 1).
#  ⚠ **선언한 축만 검사한다** — 러너가 안 적으면 건너뛴다 (`RECEIPT_AXES` 와 같은 규약).
#    그래야 이 키를 모르는 옛 팔이 통째로 무효가 되지 않는다.
#  ★★ 2026-09-02 — closure 스윕의 두 대비 축 (`σ_AM_S/σ_VGCF` · `σ_SDCP/σ_VGCF`).
#    **왜 여기(해시 밖)인가**: `receipt_digest` 는 `RECEIPT_AXES` 를 `rec.get(k)` 로 훑어
#    **없는 키도 `null` 로 해시 본문에 넣는다** ⇒ 목록에 이름 하나만 더해도 기존 설정의
#    digest 가 전부 바뀌고 `docs/data/cohorts/` 의 **커밋된 디렉터리 이름**까지 어긋난다.
#  ⇒ 디렉터리를 가르는 일은 러너의 **무손실 태그**(`_as…`·`_sd…`)가 하고, 여기서는 팔마다
#    영수증↔매니페스트를 대조해 *"러너가 의도한 σ 로 돌았는가"* 를 증명한다.
#  ⚠ 안전 조건 확인함 — payload 가 이미 두 키를 매니페스트에 적으므로
#    (`mpm_webapp_payload.py`: `sigma_am_s_S_cm` · `sigma_sdcp_S_cm`) 기존 팔이
#    `RCPT|missing` 으로 무너지지 않는다.  그래도 **러너가 선언한 팔만** 검사한다.
#  ★ 2026-10-02 (①, CL-81) — 계면 저항 표 둘.  해시 밖 (OUTDIR 보존) · 러너가 선언하면 대조
#    (`_canon_num` 은 dict 를 그대로 비교한다).  선언 안 한 옛 러너는 건너뛴다.
RECEIPT_AXES_NODIGEST = ('field_requested', 'sigma_am_s_S_cm', 'sigma_sdcp_S_cm',
                         'interface_rint_e_ohm_cm2', 'interface_rint_i_ohm_cm2')
#: ★ 2026-10-20 (Rint ② B6 · 설계 v1 §7 러너) — 영수증의 **선택 칸** = 다음 세대 요청 (`ca_ext_request` = 접합 · 수정자의 선언 값) ·
#   정지 rtol (`step3_rtol`).  **있을 때만** digest 본문에 들어간다 — 옛 영수증 (칸 없음) 의 digest = 비트 같음 (커밋된 OUTDIR ·
#   코호트 디렉터리 이름 보존 · `RECEIPT_AXES` 에 넣으면 `rec.get(k) = None` 이 본문에 들어가 옛 digest 가 전부 바뀐다).
#   대조는 `receipt_match` 가 매니페스트 블록 (`ca_ext.<하위>.protocol`) · `backend.rtol` 과 한다 (요청 없는 블록 · rtol 도 거부).
#  ★ 2026-10-20 (Rint ② Z1) — VGCF bulk σ (`SIGMA_FIBRE_BULK`) 와 그 식 이름 · 같은 규칙 (있을 때만 digest · 매니페스트 기록과 대조).
RECEIPT_OPTIONAL = ('ca_ext_request', 'step3_rtol', 'sigma_vgcf_bulk_S_cm', 'sigma_vgcf_rule',
                    #  ★ Z3 (10-20) — 러너 팔 고르기 `ARM_LIST` (있을 때만 · 고른 팔 번호 = origin 일정의 자리 · 진단 런)
                    'arm_list',
                    #  ★ 10-21 (D · 등록 R §5-6) — SV 반사실 대조 노브 `CJUNC_SV_CF` (있을 때만 = True · 끔 = 칸 없음 = 옛 digest)
                    'sv_counterfactual')


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
    for _k in RECEIPT_OPTIONAL:                     # ★ B6 — 있을 때만 (옛 영수증 digest 비트 같음)
        if _k in rec:
            _body[_k] = rec[_k]
    return _h.sha256(_j.dumps(_body, sort_keys=True, ensure_ascii=False,
                              separators=(',', ':')).encode()).hexdigest()[:12]


def receipt_match(rec, man, origin=None):
    """영수증 ↔ 매니페스트 대조 → `(ok, reason|None)`.

    ⚠ **없는 것은 통과가 아니다** — 영수증이 축을 선언했는데 매니페스트에 그 축이 없으면
      그 팔은 무슨 규약으로 돌았는지 확정할 수 없다 = HOLD (H5 와 같은 논리).
    """
    if not isinstance(rec, dict) or not isinstance(man, dict):
        return False, 'RCPT|shape| 영수증이나 매니페스트가 dict 가 아니다'
    for k in tuple(RECEIPT_AXES) + RECEIPT_AXES_NODIGEST:
        if k not in rec:
            continue                       # 러너가 그 축을 안 정했다 (킷 기본값을 쓴다)
        if k not in man:
            return False, (f'RCPT|{k}|missing| 러너는 이 축을 `{rec[k]!r}` 로 정했는데 '
                           f'매니페스트에 **기록이 없다** — 확인 불가')
        if _canon_num(man[k]) != _canon_num(rec[k]):
            return False, (f'RCPT|{k}|differ| 러너 선언 `{rec[k]!r}` ≠ 결과 `{man[k]!r}` — '
                           f'이 팔은 러너가 의도한 규약으로 돌지 않았다')
    #  ★★★ 2026-08-30 (Codex R13 C-3) — **요청 플래그는 증거가 아니다.**
    #    `field_requested` 는 `--no-field` 의 반대일 뿐이라, `--field-max-points 0` 이면
    #    빈 필드를 정상 반환하면서도 True 다.  ⇒ 러너가 필드를 요구했으면 **실물 점 수**를
    #    본다.  ⚠ 매니페스트에 그 키가 없으면 통과가 아니라 **거부**다 (옛 팔은 증명 불가).
    if rec.get('field_requested') is True:
        _n = man.get('electronic_field_pts')
        if not isinstance(_n, int) or isinstance(_n, bool) or _n <= 0:
            return False, (f'RCPT|electronic_field_pts|{"missing" if _n is None else "empty"}| '
                           f'러너가 필드를 요구했는데 전자 필드 점이 `{_n!r}` 이다 — '
                           f'요청 플래그만으로는 필드가 있다고 말할 수 없다 (R13 C-3)')
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
    #  ★ Z3 (10-20) — 팔 고르기 (`ARM_LIST`) 영수증: 팔 번호 = origin 일정 (정렬 = 러너 SHIFTS 순서) 의 자리 → 이 팔의 origin 이 **고른 팔**의
    #    origin 이어야 한다 (같은 OUTDIR 에 고르지 않은 팔 · 옛 a0 가 섞이지 않게).  칸이 없으면 옛 거동 (검사 없음).
    if 'arm_list' in rec:
        _al, _og = rec.get('arm_list'), rec.get('origins')
        if (not isinstance(_al, list) or not _al or any(type(i) is not int or i < 0 for i in _al)      # noqa: E721
                or _al != sorted(set(_al)) or not isinstance(_og, list) or max(_al) >= len(_og) or rec.get('arms') != len(_al)):
            return False, (f'RCPT|arm_list|shape| arm_list = {_al!r} (정렬 · 중복 없음 · 0 ≤ i < origin 수 · arms = 길이 '
                           f'{rec.get("arms")!r})')
        if origin is not None:
            _o = tuple(round(float(x), 9) for x in origin)
            _sel = {tuple(round(float(x), 9) for x in _og[i]) for i in _al}
            if _o not in _sel:
                return False, (f'RCPT|arm_list|unselected| origin {_o} 는 고른 팔 {_al} 의 origin 이 아니다 — 이 OUTDIR 의 런이 '
                               f'만든 팔이 아니다')
    _xp = _receipt_ext_problem(rec, man)              # ★ B6 — 다음 세대 요청 · rtol (선택 칸 · 없으면 옛 거동)
    if _xp:
        return False, _xp
    return True, None


def _same_num(a, b):
    """선언 ↔ 기록 값 대조 — 수는 **상대** 1e-12 (rtol 1e-12 를 소수 9 자리로 반올림하면 1e-10 과 같아진다) · 그 밖은 같음."""
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        fa, fb = float(a), float(b)
        if not (math.isfinite(fa) and math.isfinite(fb)):
            return False
        return fa == fb or abs(fa - fb) <= 1e-12 * max(abs(fa), abs(fb))
    return a == b


def _receipt_ext_problem(rec, man):
    """★ 2026-10-20 (Rint ② B6) — 영수증의 다음 세대 요청 (`ca_ext_request`) ↔ 매니페스트 블록 · `step3_rtol` ↔ `backend.rtol`.
    선언 없는 영수증인데 팔에 접합 · 수정자 기록 · rtol 이 있으면 거부 (러너가 요청하지 않은 실험 · SKIP 캐시 함정)."""
    req = rec.get('ca_ext_request')
    mreq = man.get(CA_EXT_REQUEST_FIELD)
    _blk = man.get('ca_ext') if isinstance(man.get('ca_ext'), dict) else {}
    if req is None:
        if mreq is not None or any(k in _blk for k in CA_EXT_REQUESTABLE):
            return (f'RCPT|ca_ext|unrequested| 러너는 접합 · 수정자를 요청하지 않았는데 이 팔에는 그 기록이 있다 '
                    f'({mreq!r}) — 지금 요청한 런의 것이 아니다')
    else:
        if not isinstance(req, dict) or not req:
            return f'RCPT|ca_ext|shape| 영수증의 ca_ext_request = {req!r} (비지 않은 dict)'
        if mreq != sorted(req):
            return f'RCPT|ca_ext|differ| 러너 요청 {sorted(req)} ≠ 팔의 요청 칸 {mreq!r}'
        for sub, kv in sorted(req.items()):
            prot = (_blk.get(sub) or {}).get('protocol') if isinstance(_blk.get(sub), dict) else None
            if not isinstance(prot, dict):
                return f'RCPT|ca_ext.{sub}|missing| 러너가 {sub} 를 요청했는데 매니페스트에 그 블록이 없다'
            for k, v in sorted((kv or {}).items()):
                if k not in prot:
                    return f'RCPT|ca_ext.{sub}.{k}|missing| 블록 protocol 에 칸이 없다'
                if not _same_num(prot[k], v):
                    return (f'RCPT|ca_ext.{sub}.{k}|differ| 러너 선언 {v!r} ≠ 결과 {prot[k]!r} — 이 팔은 러너가 의도한 '
                            f'접합 규약으로 돌지 않았다')
    #  ★ 2026-10-21 (D · 등록 R §5-6 SV 행) — SV 반사실 요청: 영수증 `sv_counterfactual` True ⟺ 증거 `sv_counterfactual_request` 있음
    #    (요청 없는 기록 · 기록 없는 요청 = 지금 요청한 런의 것이 아니다 · SKIP 캐시 함정 — rtol 과 같은 꼴).
    _cjev = ((_blk.get('cjunc') or {}).get('evidence') or {}) if isinstance(_blk.get('cjunc'), dict) else {}
    _sv_r = rec.get('sv_counterfactual')
    if _sv_r is not None and _sv_r is not True:
        return f'RCPT|sv_counterfactual|shape| 영수증의 sv_counterfactual = {_sv_r!r} (True 또는 칸 없음)'
    if (_sv_r is True) != ('sv_counterfactual_request' in _cjev):
        return (f'RCPT|sv_counterfactual|{"missing" if _sv_r else "unrequested"}| 러너 SV 반사실 요청 {bool(_sv_r)} ↔ 팔의 증거 요청 '
                f'{"있음" if "sv_counterfactual_request" in _cjev else "없음"} — 지금 요청한 런의 것이 아니다')
    rt = rec.get('step3_rtol')
    _bk = man.get('backend') if isinstance(man.get('backend'), dict) else {}
    mrt = _bk.get('rtol')
    if rt is None:
        if mrt is not None:
            return (f'RCPT|step3_rtol|unrequested| 러너는 정지 rtol 을 정하지 않았는데 팔의 backend.rtol = {mrt!r} '
                    f'(수렴 증서 세대가 다른 팔)')
    elif mrt is None:
        #  ★ 2026-10-21 (D · 등록 R §5-0) — 솔브가 하나도 안 돈 팔 (조기 반환 = 영값 위상 · 단락 · 판 접촉 없음) 은 rtol 을 결합할 CG 가 없다
        #    (`_solve_cg` 만 backend.rtol 을 적는다) → 그 팔만 받는다.  상태 자체는 증서 (`next_gen_state`) 가 따로 본다.
        if not _no_solve_ran(man):
            return f'RCPT|step3_rtol|missing| 러너는 rtol {rt!r} 로 돌라고 했는데 팔에 backend.rtol 이 없다 (증서 없는 옛 꼴)'
    elif not _same_num(mrt, rt):
        return f'RCPT|step3_rtol|differ| 러너 {rt!r} ≠ 결과 {mrt!r}'
    #  ★ 2026-10-20 (Rint ② Z1) — VGCF bulk σ · 식 이름 (`SIGMA_FIBRE_BULK` ↔ payload `--sigma-vgcf-bulk` 기록).  요청 없는 기록도 거부 —
    #    bulk 팔이 끈 OUTDIR (또는 옛 팔이 bulk OUTDIR) 의 SKIP 캐시로 들어오지 못하게 (rtol 과 같은 꼴).
    for k in ('sigma_vgcf_bulk_S_cm', 'sigma_vgcf_rule'):
        rv, mv = rec.get(k), man.get(k)
        if rv is None:
            if mv is not None:
                return (f'RCPT|{k}|unrequested| 러너는 VGCF bulk σ 를 정하지 않았는데 팔에 {k} = {mv!r} 가 있다 '
                        f'(SIGMA_FIBRE_BULK 런의 팔 · 지금 요청한 런의 것이 아니다)')
        elif mv is None:
            return f'RCPT|{k}|missing| 러너는 {k} = {rv!r} 로 돌라고 했는데 팔에 그 기록이 없다 (bulk 없이 돈 팔)'
        elif not _same_num(mv, rv):
            return f'RCPT|{k}|differ| 러너 {rv!r} ≠ 결과 {mv!r}'
    return None


#: ★ 2026-10-21 (D) — 솔브가 돈 component 상태 (`_s3mark` 어휘) — 이 중 하나라도 있으면 CG 가 돌았다 (backend 기록이 있어야 한다)
_SOLVED_STATUSES = ('complete', 'unconverged')


def _no_solve_ran(man):
    """매니페스트의 component 가 하나도 풀리지 않았는가 (전자 = not_solvable · 나머지 = 끔 · 계획 밖) — 조기 반환 팔.
    component 기록이 없거나 모양이 틀리면 False (모르는 것을 '안 돌았다' 로 읽지 않는다)."""
    comps = man.get('components') if isinstance(man, dict) else None
    if not isinstance(comps, dict) or not isinstance(comps.get('electronic'), dict):
        return False
    if comps['electronic'].get('status') != 'not_solvable':
        return False
    return not any(isinstance(v, dict) and v.get('status') in _SOLVED_STATUSES for v in comps.values())


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
    #  ★ 2026-10-20 (Rint ② · 설계 v1 §7) — 다음 세대 `p3ca-` 도 현행 세대다 (p2 축 전부 + ca_ext 블록).  안 세면 p3ca 매니페스트가
    #    `schema_version` 을 낮춰 신고해 증거 계약을 끄는 길 (R5-CX-02) 이 다시 열린다.
    if isinstance(pid, str) and pid.startswith(CA_EXT_PREFIX + '-'):
        return SCHEMA_VERSION
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
                   'sdcp_yield_to_vgcf', 'sdcp_bridge_um', 'ptfe_block_um',
                   'ptfe_stamp', 'ptfe_zero_dof',
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

    ★ 2026-10-20 (Rint ② · 설계 v1 §7) — **다음 세대 블록 `ca_ext`**.  블록이 없고 기능도 꺼져 있으면 옛 p2 함수 그대로
      (`_p2_protocol_id` · 코드 지문 칸을 뺀 매니페스트가 같으면 id 비트 같음) · 블록이 있으면 `p3ca-` + sha256(p2 id ∪ 하위
      블록들의 protocol 칸)[:16] · 블록 모양이 틀리거나 **기능을 켰는데 블록이 없으면** `unknown:ca_ext` (지금 p2 함수는
      `ptfe_stamp = face_alpha` 만으로 정상 p2 id 를 냈다 = 세대 섞임 구멍).  p2 축 결손이 먼저다 (그 사유를 숨기지 않는다).
    """
    _ca = _ca_ext_protocol_id(man)
    if _ca is not None:
        return _ca
    return _p2_protocol_id(man)


def _p2_protocol_id(man):
    """p2 규약 id — 옛 `physics_protocol_id` 본문 그대로 (ca_ext 블록 없는 매니페스트의 id 를 바꾸지 않는다)."""
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


#: ★ 2026-10-20 (Rint ② · 설계 v1 §7) — **다음 세대 블록 `ca_ext`** (S1 · S2 · S3 중 하나라도 켤 때만 매니페스트에 쓴다).
#   `PROTOCOL_FIELDS` 를 늘리지 않는다 — 전역 p3 승격은 봉인 p2 코호트 id 를 다 바꾼다 (`--step3-ptfe-block-scope` 와 같은 이유).
CA_EXT_SCHEMA = 'ca-ext-v1'
CA_EXT_PREFIX = 'p3ca'
CA_EXT_UNKNOWN = 'unknown:ca_ext'
#: 하위 블록 등록부 — 이름 → (요청 술어 (매니페스트 → bool), 검증기 모듈, 검증기 함수, protocol 정본 키 목록 이름).
#  ⚠ 모르는 하위 블록 = `unknown:ca_ext` (fail-closed).  S2 (`cjunc`) · S3 (`sdcp_mod`) 는 같은 꼴로 여기에 더한다.
#  ⚠ 블록 부재 = 끔 으로 읽는 것은 R3-CX-03 ("키 부재 = 모름") 의 예외다 → 켠 producer 가 블록을 빠뜨리는 길을 요청 술어 ·
#    `ca_ext_record_ok` · `unknown:ca_ext` 로 막는다 (설계 v1 §7 · Codex Q A10).
CA_EXT_SUBBLOCKS = {
    'ptfe_face': (lambda m: m.get('ptfe_stamp') == 'face_alpha', 'ptfe_face_alpha', 'ptfe_face_block_problem',
                  'PROTOCOL_KEYS'),
    #  ★ 2026-10-20 (Rint ② B6) — S2 탄소 접합 · S3 SDCP 접합 수정자.  요청 = 최상위 `ca_ext_requested` (켰을 때만 쓴다 · 끈 매니페스트는
    #    키 자체가 없다 = 옛 바이트).  검증기 · protocol 정본 = `ca_ext_cjunc` (payload 배선과 같은 모듈 · 사본 없음).
    'cjunc': (lambda m: 'cjunc' in _ca_ext_req(m), 'ca_ext_cjunc', 'cjunc_block_problem', 'CJUNC_PROTOCOL_KEYS'),
    'sdcp_mod': (lambda m: 'sdcp_mod' in _ca_ext_req(m), 'ca_ext_cjunc', 'sdcp_mod_block_problem', 'SDCP_MOD_PROTOCOL_KEYS'),
}
#: ★ B6 — S2 · S3 의 요청 칸 (최상위 · 정렬 목록 · 중복 없음 · 아래 이름만).  S1 (ptfe_face) 의 요청은 `ptfe_stamp = face_alpha` 그대로.
CA_EXT_REQUEST_FIELD = 'ca_ext_requested'
CA_EXT_REQUESTABLE = ('cjunc', 'sdcp_mod')


def _ca_ext_req(man):
    """요청 칸 → 이름 튜플 (모양이 틀리면 빈 튜플 — 그 경우는 `_ca_ext_shape_problem` 이 `unknown:ca_ext` 로 낸다)."""
    v = man.get(CA_EXT_REQUEST_FIELD) if isinstance(man, dict) else None
    return tuple(v) if isinstance(v, list) and all(isinstance(x, str) for x in v) else ()


def _ca_ext_requested(man):
    """기능 요청 (블록이 있어야 하는) 매니페스트인가 — 등록된 하위 블록의 요청 술어 중 하나라도 참 · ★ B6 — 요청 칸이 **있기만 해도**
    (모양이 틀려도) 요청으로 센다 (모양 틀린 칸 + 블록 없음이 옛 p2 id 로 조용히 내려가지 않게 — `unknown:ca_ext`)."""
    return isinstance(man, dict) and (any(pred(man) for pred, _m, _f, _k in CA_EXT_SUBBLOCKS.values())
                                      or CA_EXT_REQUEST_FIELD in man)


def _ca_ext_request_field_problem(man):
    if CA_EXT_REQUEST_FIELD not in man:
        return None
    v = man[CA_EXT_REQUEST_FIELD]
    if (not isinstance(v, list) or not v or any(not isinstance(x, str) for x in v) or v != sorted(set(v))
            or any(x not in CA_EXT_REQUESTABLE for x in v)):
        return (f'{CA_EXT_REQUEST_FIELD} = {v!r} — 비지 않은 정렬 목록 · 중복 없음 · {CA_EXT_REQUESTABLE} 안 '
                f'(S1 의 요청은 ptfe_stamp = face_alpha)')
    return None


def _ca_ext_shape_problem(man):
    _rq = _ca_ext_request_field_problem(man)
    if _rq:
        return _rq
    blk = man.get('ca_ext')
    if not isinstance(blk, dict):
        return 'ca_ext 가 dict 가 아니다'
    if blk.get('schema') != CA_EXT_SCHEMA:
        return f'schema {blk.get("schema")!r} ≠ {CA_EXT_SCHEMA!r}'
    subs = [k for k in blk if k != 'schema']
    if not subs:
        return '하위 블록이 없다'
    for k in subs:
        if k not in CA_EXT_SUBBLOCKS:
            return f'모르는 하위 블록 {k!r}'
        b = blk[k]
        if not isinstance(b, dict) or not isinstance(b.get('protocol'), dict) or not isinstance(b.get('evidence'), dict):
            return f'{k} = {{protocol, evidence}} dict 이어야 한다'
    for k, (pred, _m, _f, _kk) in CA_EXT_SUBBLOCKS.items():
        if bool(pred(man)) != (k in blk):
            return f'{k}: 기능 요청 {bool(pred(man))} ↔ 블록 {k in blk} 불일치'
    return None


def _ca_ext_protocol_id(man):
    """→ None (블록 없음 + 기능 끔 = 옛 p2 함수) | p2 축 결손 id | `unknown:ca_ext` | `p3ca-…`."""
    if not isinstance(man, dict) or ('ca_ext' not in man and not _ca_ext_requested(man)):
        return None
    base = _p2_protocol_id(man)
    if base.startswith('unknown:'):
        return base
    if 'ca_ext' not in man or _ca_ext_shape_problem(man):
        return CA_EXT_UNKNOWN
    import hashlib as _hl
    import json as _json
    blk = man['ca_ext']
    body = {'p2': base, 'schema': blk['schema'], 'protocol': {k: blk[k]['protocol'] for k in sorted(blk) if k != 'schema'}}
    try:
        canon = _json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
    except (TypeError, ValueError):
        return CA_EXT_UNKNOWN
    return f'{CA_EXT_PREFIX}-' + _hl.sha256(canon.encode('utf-8')).hexdigest()[:16]


def ca_ext_protocol_fields():
    """규칙 M — `protocol_ext` 회계가 이름 댈 수 있는 칸 {'ca_ext.<하위>.<키>'} (하위 블록 모듈의 protocol 정본 키 · 사본 없음)."""
    import importlib
    out = set()
    for k, (_p, mod, _f, keys) in CA_EXT_SUBBLOCKS.items():
        out |= {f'ca_ext.{k}.{x}' for x in getattr(importlib.import_module(mod), keys)}
    return out


def ca_ext_record_ok(man):
    """다음 세대 블록 `ca_ext` 계약 → `(ok, reason|None)` — producer (게시 전) · `check_arm` · 판정기가 같이 부른다 (설계 v1 §7).
    · 블록 없음 + 기능 끔 = 통과 (옛 세대 · 현 생산 그대로) · 기능 켬 + 블록 없음 = 위반 (`unknown:ca_ext`)
    · 블록 모양 · 하위 블록 등록 · 요청 ↔ 블록 · 하위 블록 검증기 (그 모듈이 정본 — 여기에 사본을 두지 않는다)"""
    m = man if isinstance(man, dict) else {}
    if 'ca_ext' not in m:
        if _ca_ext_requested(m):
            return False, ('CAEXT|absent| 기능 요청 (예: ptfe_stamp = face_alpha) 인데 ca_ext 블록이 없다 — 세대 '
                           f'{CA_EXT_UNKNOWN} (요청과 실행의 기록이 갈렸다)')
        return True, None
    why = _ca_ext_shape_problem(m)
    if why:
        return False, f'CAEXT|shape| {why}'
    import importlib
    for k in sorted(kk for kk in m['ca_ext'] if kk != 'schema'):
        _p, mod, fn, _keys = CA_EXT_SUBBLOCKS[k]
        try:
            prob = getattr(importlib.import_module(mod), fn)(m)
        except Exception as e:                                   # noqa: BLE001 — 확인 못 한 것을 통과시키지 않는다
            return False, f'CAEXT|{k}|unverifiable| {type(e).__name__}: {e}'
        if prob:
            return False, f'CAEXT|{k}| {prob}'
    #  ★ 2026-10-21 (D · 등록 R §5-6 SV 행) — SV 반사실 요청 ↔ 기록 (D 모듈 `ca_ext_svcf` · 접합 블록 검증기 뒤 · 끊는 면의 정의 무관 ·
    #    요청 없음 = 칸 없음 = 검사 없음 = 옛 판정 그대로)
    _cjb = m['ca_ext'].get('cjunc')
    if isinstance(_cjb, dict) and isinstance(_cjb.get('evidence'), dict):
        try:
            import ca_ext_svcf as _sv
            _ev = _cjb['evidence']
            _ms = ((_ev.get('receipts') or {}).get('electronic_main') or {}).get('status') \
                if isinstance(_ev.get('receipts'), dict) else None
            prob = _sv.sv_cf_problem(_ev, _ms in ('applied', 'absent_geometry'))
        except Exception as e:                                   # noqa: BLE001 — 확인 못 한 것을 통과시키지 않는다
            return False, f'CAEXT|cjunc|unverifiable| {type(e).__name__}: {e}'
        if prob:
            return False, f'CAEXT|cjunc| {prob}'
    return True, None


def ca_ext_request_problem(req, ptfe_stamp='off'):
    """★ 2026-10-20 (Rint ② B6 · 러너 발사 전 계약 검사) — 러너가 선언하는 다음 세대 요청 → 문제 | None.
    선언 축 = 매니페스트 축: 하위 블록 이름 · 칸 집합 (`ca_ext_cjunc.REQUEST_KEYS_*`) · 칸이 protocol 정본 (`ca_ext_protocol_fields`) 안 ·
    값 = 그 정본 함수로 다시 만들 수 있다 (정량 · c ∈ {0, 1}).  S3 만 = 거부 (S2 없이).
    ★ Z3 — `ptfe_stamp` (러너 · 영수증의 PTFE 규약 · 기본 off) 로 다시 만든다 → P1 = face_alpha 에서만 통과 · 접합 선언 칸에 극한 표지
      `rj_limit` ('inf' · 'zero' — 등록 R §3-1 바닥 · 천장 · 있을 때만) 를 받는다 (`R_j_ohm` null · 0.0 과 한 꼴)."""
    if not isinstance(req, dict) or not req:
        return f'요청이 비지 않은 dict 가 아니다 ({req!r})'
    _bad = sorted(k for k in req if k not in CA_EXT_REQUESTABLE)
    if _bad:
        return f'모르는 하위 블록 {_bad} (요청 가능: {CA_EXT_REQUESTABLE})'
    if 'sdcp_mod' in req and 'cjunc' not in req:
        return 'S3 SDCP 수정자는 S2 탄소 접합 없이 = 거부 (설계 §5-2)'
    try:
        import ca_ext_cjunc as _cw
        _fields = ca_ext_protocol_fields()
    except Exception as e:                                       # noqa: BLE001 — 확인 못 한 것을 통과시키지 않는다
        return f'정본을 못 읽었다 ({type(e).__name__}: {e})'
    for sub, kv in req.items():
        keys = _cw.REQUEST_KEYS_CJUNC if sub == 'cjunc' else _cw.REQUEST_KEYS_SDCP
        if sub == 'cjunc' and isinstance(kv, dict) and 'rj_limit' in kv:
            keys = tuple(keys) + ('rj_limit',)                   # ★ Z3 — 극한 런 표지 (있을 때만)
        if not isinstance(kv, dict) or set(kv) != set(keys):
            return f'{sub}: 선언 칸 {sorted(kv) if isinstance(kv, dict) else kv!r} ≠ {sorted(keys)}'
        _off = sorted(f'ca_ext.{sub}.{k}' for k in kv if f'ca_ext.{sub}.{k}' not in _fields)
        if _off:
            return f'{sub}: 선언 칸 {_off} 이 매니페스트 protocol 정본에 없다'
    try:
        _cw.cjunc_protocol_record(ptfe_stamp=ptfe_stamp, **req['cjunc'])
        if 'sdcp_mod' in req:
            _cw.sdcp_mod_protocol_record(c=req['sdcp_mod']['c'], tol_sj_um=req['cjunc']['tol_ff_um'])
    except (ValueError, TypeError) as e:
        return f'값| {e}'
    return None


def _fin_num(x):
    return not isinstance(x, bool) and isinstance(x, (int, float)) and math.isfinite(x)


def _zero_cert_problem(cert, sigma, _cc):
    """★ 2026-10-21 (Codex RCA-13 · 1저자 Q7 일부) — VALID_ZERO_TOPOLOGY 증서 (두 판을 잇는 성분이 없는 해 = σ 0 이 정상 결과) → 문제 | None.
    σ 0 을 **정확히** 요구 (증서 · 결과 둘 다 · bool 아님) · 관통 dof 0 · ok True · 출처 = 조기 반환 (영값 위상 사유 · 격자 지문 hex32) 또는
    행렬 그래프 (사유 없음 · 원장 일치 · 위상 'zero' · 게시 판 전류 정확히 0) · 봉인값 = 이 코드.  CG 실패를 0 으로 받는 길이 아니다."""
    if cert.get('ok') is not True:
        return f'CERT|zero| ok = {cert.get("ok")!r} (영값 위상 증서는 ok True 여야 한다)'
    for k, want in (('rtol_max', _cc.CERT_RTOL_MAX), ('eps_I', _cc.CERT_EPS_I), ('resolve_tol', _cc.CERT_RESOLVE_TOL),
                    ('target_tol', _cc.CERT_TARGET_TOL), ('target_version', _cc.TARGET_VERSION)):
        if cert.get(k) != want:
            return f'CERT|seal| {k} = {cert.get(k)!r} ≠ 이 코드의 봉인 {want!r}'
    src = cert.get('zero_source')
    if src == 'early_return':
        if _cc.classify_reason(cert.get('reason')) != _cc.STATUS_ZERO:
            return f'CERT|zero| 조기 반환 사유 {cert.get("reason")!r} 는 영값 위상 사유가 아니다 ({_cc.ZERO_REASONS})'
        for k in ('fp_sid', 'fp_sig'):
            v = cert.get(k)
            if not (isinstance(v, str) and len(v) == 32 and all(ch in '0123456789abcdef' for ch in v)):
                return f'CERT|zero| {k} = {v!r} (격자 지문 소문자 hex 32 — `step3_sigma._grid_fp`)'
    elif src == 'matrix_graph':
        if cert.get('reason') is not None or cert.get('target_topology') != 'zero' or cert.get('target_ledger_ok') is not True \
                or cert.get('zero_exact') is not True:
            return (f'CERT|zero| 행렬 그래프 출처인데 사유 {cert.get("reason")!r} · 위상 {cert.get("target_topology")!r} · '
                    f'원장 {cert.get("target_ledger_ok")!r} · 정확 0 {cert.get("zero_exact")!r}')
    else:
        return f'CERT|zero| 출처 {src!r} ∉ {_cc.ZERO_SOURCES}'
    ntd = cert.get('n_through_dof')
    if type(ntd) is not int or ntd != 0:                         # noqa: E721
        return f'CERT|zero| n_through_dof = {ntd!r} (관통 성분이 없어야 영값 위상)'
    s = cert.get('sigma')
    if not (_fin_num(s) and s == 0.0 and _fin_num(sigma) and sigma == 0.0):
        return f'CERT|zero| 증서 σ {s!r} · 결과 σ {sigma!r} — 영값 위상은 둘 다 정확히 0'
    return None


def conv_cert_problem(cert, sigma):
    """★ 2026-10-20 (Rint ② B6 · 설계 v1 §6 · N15) — 다음 세대 판정 해의 **수렴 증서** → 문제 | None.
    플래그를 믿지 않는다 — 기록된 수 (rtol · 불균형 · 이어 풀기 Δσ · info) 로 ⓐ ⓑ ⓒ 를 다시 판정 · 봉인값 = 이 코드의 상수
    (`step3_conv_cert`) · 증서 σ = 결과 σ (증서 ↔ 결과 결합 · 상대 1e-9).  칸 없음 = `--step3-rtol` 없이 돈 런 = 미게시.
    ★ 2026-10-21 (Codex RCA-07 · RCA-13 · 1저자 Q5 (가) · Q7 일부) — 증서 판 v2: **상태 먼저 분기** — VALID_ZERO_TOPOLOGY (σ 0 정상 ·
    `_zero_cert_problem`) · POSITIVE_SOLVED (아래 ⓐ ⓑ ⓒ + ⓓ 목표량 증서를 기록된 하한 · 상한 · 게시 판 전류로 **같은 판정 함수**
    `step3_conv_cert.target_judge` 에 다시 넣는다 · 게시 판 전류 × scale = 증서 σ) · 그 밖 상태 (단락 · 증서 못 세움 · 모름) = 미게시."""
    import step3_conv_cert as _cc
    if not isinstance(cert, dict):
        return 'CERT|absent| 수렴 증서 칸이 없다 (--step3-rtol 없이 돈 런 · 다음 세대 판정 = 미게시 팔)'
    if cert.get('version') != _cc.CERT_VERSION:
        return f'CERT|version| {cert.get("version")!r} ≠ {_cc.CERT_VERSION!r}'
    st = cert.get('status')
    if st == _cc.STATUS_ZERO:
        return _zero_cert_problem(cert, sigma, _cc)
    if st != _cc.STATUS_POSITIVE:
        return (f'CERT|status| {st!r} — 게시 가능한 상태는 {_cc.STATUS_POSITIVE} · {_cc.STATUS_ZERO} 뿐 '
                f'(단락 · 증서 못 세움 · 모르는 상태 = 미게시)')
    for k in ('ok', 'pass_a', 'pass_b', 'pass_c', 'pass_d'):
        if type(cert.get(k)) is not bool:                        # noqa: E721
            return f'CERT|type| {k} = {cert.get(k)!r} (bool 이어야 한다)'
    if cert['ok'] is not (cert['pass_a'] and cert['pass_b'] and cert['pass_c'] and cert['pass_d']):
        return 'CERT|inconsistent| ok ≠ ⓐ ∧ ⓑ ∧ ⓒ ∧ ⓓ'
    if not cert['ok']:
        return f"CERT|failed| ⓐ {cert['pass_a']} · ⓑ {cert['pass_b']} · ⓒ {cert['pass_c']} · ⓓ {cert['pass_d']}"
    #  ★ 10-21 (굳히기) — 부동소수 보수 규칙 (`target_fp`) 도 봉인: 다른 규칙 (옛 여유) 으로 만든 구간을 이 코드의 판정으로 받지 않는다
    for k, want in (('rtol_max', _cc.CERT_RTOL_MAX), ('eps_I', _cc.CERT_EPS_I), ('resolve_tol', _cc.CERT_RESOLVE_TOL),
                    ('target_tol', _cc.CERT_TARGET_TOL), ('target_version', _cc.TARGET_VERSION),
                    ('target_fp', _cc.TARGET_FP_RULE)):
        if cert.get(k) != want:
            return f'CERT|seal| {k} = {cert.get(k)!r} ≠ 이 코드의 봉인 {want!r}'

    _fin = _fin_num
    rt, rs = cert.get('rtol_used'), cert.get('resid')
    if not (_fin(rt) and 0.0 < rt <= _cc.CERT_RTOL_MAX) or type(cert.get('info')) is not int \
            or cert['info'] != 0 or not _fin(rs):                # noqa: E721
        return f'CERT|a| rtol {rt!r} · info {cert.get("info")!r} · resid {rs!r} — ⓐ 를 수로 다시 보면 실패'
    imb = cert.get('imbalance')
    if not (_fin(imb) and 0.0 <= imb <= _cc.CERT_EPS_I):
        return f'CERT|b| 판 전류 불균형 {imb!r} > ε_I {_cc.CERT_EPS_I!r} (또는 비유한) — ⓑ 를 수로 다시 보면 실패'
    ds = cert.get('dsigma_rel')
    if not (_fin(ds) and 0.0 <= ds <= _cc.CERT_RESOLVE_TOL) or type(cert.get('resolve_info')) is not int \
            or cert['resolve_info'] != 0:                        # noqa: E721
        return f'CERT|c| 이어 풀기 Δσ/σ {ds!r} · info {cert.get("resolve_info")!r} — ⓒ 를 수로 다시 보면 실패'
    s = cert.get('sigma')
    if not (_fin(s) and _fin(sigma) and sigma > 0.0 and abs(s - sigma) <= 1e-9 * abs(sigma)):
        return f'CERT|sigma| 증서 σ {s!r} ≠ 결과 σ {sigma!r} — 증서가 이 결과의 것이 아니다'
    #  ★ 10-21 — ⓓ 를 기록된 수로 다시 판정 (생산과 같은 함수 · 플래그를 믿지 않는다) + 구간 (코드 단위) ↔ 게시 σ 결합
    if cert.get('target_ledger_ok') is not True or cert.get('target_topology') != 'through':
        return (f'CERT|d| 원장 {cert.get("target_ledger_ok")!r} · 위상 {cert.get("target_topology")!r} — 양의 해 증서는 원장 일치 · '
                f'관통 위상이어야 한다')
    ib, sc = cert.get('I_bot'), cert.get('scale')
    if not (_fin(ib) and _fin(sc) and sc > 0.0 and abs(ib * sc - s) <= 1e-12 * abs(s)):
        return f'CERT|d| 게시 판 전류 {ib!r} × scale {sc!r} ≠ 증서 σ {s!r} — 구간이 이 게시값의 것이 아니다'
    jd = _cc.target_judge(cert.get('target_lo'), cert.get('target_hi'), ib)
    if jd['pass_d'] is not True:
        return f"CERT|d| 목표량 증서를 수로 다시 보면 실패 — {jd['target_why']}"
    return None


def next_gen_cert_ok(step3):
    """★ 2026-10-20 (Rint ② B6) — 다음 세대 (`ca_ext` 블록 · 요청이 있는) 팔의 **게시 조건** → `(ok, why)`.
    전자 증서 (`step3.conv_cert`) 필수 · 이온을 계획해 푼 팔은 이온 증서 (`step3.ion_conv_cert`) 도 · 옛 세대 (p2) = 이 규칙 밖 (통과).
    판정기가 팔 JSON 마다 부른다 — 실패 = 미게시 팔로 센다 (설계 §6 · 지금 생산 술어는 다음 세대 꼴에서 틀린 σ 를 수렴으로 인증한다)."""
    s = step3 if isinstance(step3, dict) else {}
    man = s.get('manifest') if isinstance(s.get('manifest'), dict) else {}
    if not ('ca_ext' in man or _ca_ext_requested(man)):
        return True, None
    why = conv_cert_problem(s.get('conv_cert'), s.get('sigma_e_eff_S_cm'))
    if why:
        return False, f'NEXTGEN|electronic| {why}'
    plan = man.get('component_plan') if isinstance(man.get('component_plan'), dict) else {}
    _ist = ((man.get('components') or {}).get('ionic') or {}).get('status') if isinstance(man.get('components'), dict) else None
    if plan.get('ionic') is True and _ist != 'not_solvable':
        why = conv_cert_problem(s.get('ion_conv_cert'), s.get('sigma_ion_eff_S_cm'))
        if why:
            return False, f'NEXTGEN|ionic| {why}'
    return True, None


#: ★ 2026-10-21 (D · 등록 R §5-0 · Codex RCA-13 · 1저자 Q7 ③) — 다음 세대 팔의 해 상태 (사슬 · check_arm 이 같은 함수로 본다).
#   positive = 양의 유한 σ (증서 ⓐ–ⓓ) · zero = VALID_ZERO_TOPOLOGY (σ 0 이 정상 결과) · short = ELECTRODE_SHORT (J11 · σ = +∞ ·
#   유한 σ 로 위장하지 않는다 → 결과 σ 칸 = None) — 그 밖 = (None, 사유) = 사슬에서 NOT_COMPUTED.
NG_STATES = ('positive', 'zero', 'short')


def _hex32(v):
    return isinstance(v, str) and len(v) == 32 and all(ch in '0123456789abcdef' for ch in v)


def next_gen_state(step3):
    """다음 세대 팔 (`ca_ext` 블록 · 요청) → `(상태, None)` | `(None, 사유)` · 옛 세대 = `('legacy', None)` (이 규칙 밖).
    플래그를 믿지 않는다 — 상태마다 증서 ↔ 결과 ↔ 매니페스트를 다시 결합한다:
      · positive — `next_gen_cert_ok` (ⓐ–ⓓ · 증서 σ = 결과 σ) · 결과 σ 유한 > 0
      · zero — 같은 함수 (`_zero_cert_problem` · σ 둘 다 정확히 0) + 출처별: 조기 반환 = 결과 사유 = 증서 사유 (영값 위상 사유) · 전자 component
        not_solvable / 행렬 그래프 = 사유 없음 · 전자 complete · 수렴 3 칸 (CG 가 돌았다)
      · short — 증서 판 · 상태 ELECTRODE_SHORT · ok False · 봉인 상수 · 격자 지문 · 결과 사유 = 증서 사유 (단락 사유) · 결과 σ = None (0 · 유한값 =
        위장 = 거부) · 전자 not_solvable · 접합 블록의 솔브 기록 short True · solved False · 축약 instance > 0 (단락은 축약에서만 생긴다)
    ⚠ 상태는 위상 사실이지 σ 값이 아니다 — 값 봉인 (사슬) 은 σ 숫자만 가린다."""
    import step3_conv_cert as _cc
    s = step3 if isinstance(step3, dict) else {}
    man = s.get('manifest') if isinstance(s.get('manifest'), dict) else {}
    if not ('ca_ext' in man or _ca_ext_requested(man)):
        return 'legacy', None
    cert = s.get('conv_cert')
    if not isinstance(cert, dict):
        return None, 'STATE|absent| 수렴 · 상태 증서가 없다 (--step3-rtol 없이 돈 런 · 조기 반환 σ 0 을 증서 없이 받지 않는다)'
    if cert.get('version') != _cc.CERT_VERSION:
        return None, f'STATE|version| {cert.get("version")!r} ≠ {_cc.CERT_VERSION!r}'
    st = cert.get('status')
    comp = ((man.get('components') or {}).get('electronic') or {}).get('status') if isinstance(man.get('components'), dict) else None
    sig = s.get('sigma_e_eff_S_cm')
    if st == _cc.STATUS_POSITIVE:
        ok, why = next_gen_cert_ok(s)
        if not ok:
            return None, f'STATE|positive| {why}'
        if not (_fin_num(sig) and sig > 0.0):
            return None, f'STATE|positive| 결과 σ {sig!r} (유한 양수여야 한다)'
        return 'positive', None
    if st == _cc.STATUS_ZERO:
        ok, why = next_gen_cert_ok(s)
        if not ok:
            return None, f'STATE|zero| {why}'
        src = cert.get('zero_source')
        if src == 'early_return':
            rs = s.get('reason')
            if not isinstance(rs, str) or rs != cert.get('reason') or _cc.classify_reason(rs) != _cc.STATUS_ZERO:
                return None, f'STATE|zero| 결과 사유 {rs!r} ↔ 증서 사유 {cert.get("reason")!r} (같은 영값 위상 사유여야 한다)'
            if comp != 'not_solvable':
                return None, f'STATE|zero| 조기 반환인데 전자 component = {comp!r} (not_solvable 이어야 — 솔브 완료로 적지 않는다)'
        else:                                                    # matrix_graph (`_zero_cert_problem` 이 출처를 이미 둘로 닫았다)
            if s.get('reason') is not None or comp != 'complete':
                return None, f'STATE|zero| 행렬 그래프 영값인데 사유 {s.get("reason")!r} · 전자 component {comp!r}'
            okc, whyc = conv_ok(s.get('cg_info'), s.get('unconverged'), s.get('cg_resid'))
            if not okc:
                return None, f'STATE|zero| 행렬 그래프 영값인데 수렴 계약 {whyc}'
        return 'zero', None
    if st == _cc.STATUS_SHORT:
        for k, want in (('rtol_max', _cc.CERT_RTOL_MAX), ('eps_I', _cc.CERT_EPS_I), ('resolve_tol', _cc.CERT_RESOLVE_TOL),
                        ('target_tol', _cc.CERT_TARGET_TOL), ('target_version', _cc.TARGET_VERSION)):
            if cert.get(k) != want:
                return None, f'STATE|short|seal| {k} = {cert.get(k)!r} ≠ 이 코드의 봉인 {want!r}'
        if cert.get('ok') is not False or cert.get('zero_source') != 'early_return':
            return None, f'STATE|short| 증서 ok {cert.get("ok")!r} · 출처 {cert.get("zero_source")!r} (False · early_return 이어야)'
        if not (_hex32(cert.get('fp_sid')) and _hex32(cert.get('fp_sig'))):
            return None, 'STATE|short| 증서 격자 지문 (fp_sid · fp_sig) 이 소문자 hex 32 가 아니다'
        rs = s.get('reason')
        if not isinstance(rs, str) or rs != cert.get('reason') or _cc.classify_reason(rs) != _cc.STATUS_SHORT:
            return None, f'STATE|short| 결과 사유 {rs!r} ↔ 증서 사유 {cert.get("reason")!r} (같은 단락 사유여야 한다)'
        if sig is not None:
            return None, f'STATE|short| 결과 σ {sig!r} — 단락 (σ = +∞) 을 유한 σ 로 위장하지 않는다 (None 이어야 · 등록 R §5-0)'
        if comp != 'not_solvable':
            return None, f'STATE|short| 전자 component = {comp!r} (not_solvable 이어야)'
        cj = ((man.get('ca_ext') or {}).get('cjunc') or {}) if isinstance(man.get('ca_ext'), dict) else {}
        ev = cj.get('evidence') if isinstance(cj.get('evidence'), dict) else {}
        sv = ev.get('solve') if isinstance(ev.get('solve'), dict) else {}
        cnt = ev.get('counts') if isinstance(ev.get('counts'), dict) else {}
        if sv.get('short') is not True or sv.get('solved') is not False or sv.get('reason') != rs:
            return None, (f'STATE|short| 접합 솔브 기록 short {sv.get("short")!r} · solved {sv.get("solved")!r} · 사유 {sv.get("reason")!r} '
                          f'(단락은 접합 축약의 기록이 있어야 한다)')
        nc = cnt.get('n_contract')
        if type(nc) is not int or nc <= 0:                       # noqa: E721
            return None, f'STATE|short| 축약 instance {nc!r} — 단락은 축약 무리에서만 생긴다 (J11)'
        plan = man.get('component_plan') if isinstance(man.get('component_plan'), dict) else {}
        _ist = ((man.get('components') or {}).get('ionic') or {}).get('status')
        if plan.get('ionic') is True and _ist != 'not_solvable':     # 이온을 푼 팔 = 이온 증서는 그대로 (전자 단락은 이온 해와 무관)
            why = conv_cert_problem(s.get('ion_conv_cert'), s.get('sigma_ion_eff_S_cm'))
            if why:
                return None, f'STATE|short|ionic| {why}'
        return 'short', None
    return None, (f'STATE|status| {st!r} — 받는 상태는 {_cc.STATUS_POSITIVE} · {_cc.STATUS_ZERO} · {_cc.STATUS_SHORT} '
                  f'(증서 못 세움 · 모르는 상태 = NOT_COMPUTED)')


#: ★ 2026-10-20 (Rint ② B6 · 설계 v1 §7 러너) — 러너 `scripts/sdcp_gain_vox015_8arm.sh` 의 **다음 세대 손잡이** = (env 이름, 하위 블록, 선언 칸).
#   러너 (영수증 조립) · 규율 검사기 (`check_method_discipline._RUNNER_AXES` — 규칙 L 탐침 격리) · 시험이 이 표 하나를 본다.
#   전부 비우면 (기본) 옛 영수증 · 옛 OUTDIR · 옛 팔 이름 · 옛 payload 인자 그대로.  S1 face_alpha 의 손잡이는 기존 `PTFE_STAMP` 축이다.
#   ⚠ `STEP3_RTOL` 은 러너 env 게이트의 이름꼴 (SIGMA_ · SDCP_ · PTFE_ · CJUNC) 밖이다 — 러너가 `STEP3_VOX` 를 하위 프로세스 env 로 쓰므로
#     `STEP3_` 를 통째로 넣으면 부모 셸의 그 이름이 거짓 거부를 낸다 ⇒ `STEP3_RTOL` 의 오타 (예: STEP3_RTOOL) 는 게이트가 못 잡는다 (한정어).
RUNNER_CA_EXT_ENV = (
    ('CJUNC', 'cjunc', None),                      # S2 켜기 — 비움 · 0 = 끔 · 1 = 켬
    ('CJUNC_RJ', 'cjunc', 'R_j_ohm'),
    ('CJUNC_LEN_LAW', 'cjunc', 'len_law'),
    ('CJUNC_UNREG_LAW', 'cjunc', 'unreg_law'),
    ('CJUNC_S_MIN_UM', 'cjunc', 's_min_um'),
    ('CJUNC_TOL_FF_UM', 'cjunc', 'tol_ff_um'),
    ('CJUNC_PTFE_JLAW', 'cjunc', 'ptfe_jlaw'),
    ('SDCP_MOD_C', 'sdcp_mod', 'c'),               # S3 — 0 · 1 (payload 선택지 그대로 · S2 와만)
    ('STEP3_RTOL', None, 'step3_rtol'),            # 정지 rtol + 수렴 증서 (numeric · 영수증 선택 칸)
    #  ★ 2026-10-20 (Rint ② Z1 · 설계 v1 §1-2 #1 · #2 · §7) — VGCF bulk σ [S/cm] → 직경 보존 복셀 σ_VGCF (팔마다 · 같은 함수
    #    `step3_sigma.vgcf_sigma_from_bulk` · 옛 기본 bulk 100 과 같은 자리) · `SIGMA_VGCF_OVERRIDE` 와 동시 = 거부 · 영수증 선택 칸.
    ('SIGMA_FIBRE_BULK', None, 'sigma_vgcf_bulk_S_cm'),
    #  ★ 2026-10-21 (D · 등록 R §5-6 SV 행 · Codex RCA-06 · 1저자 Q4 (가)) — SV 반사실 대조 (비움 · 0 = 끔 · 1 = 켬 · CJUNC=1 과만) ·
    #    영수증 선택 칸 (켬 = True) · payload `--step3-cjunc-sv-cf` · 팔 태그 `_svcf` · 선언 칸 아님 (protocol 밖 · 주 σ 그대로) ·
    #    문턱 = 사슬 계획 (producer 는 비만 낸다 — 판정 = 사슬 판정 계산기 · 등록 R §5-7).
    ('CJUNC_SV_CF', None, 'sv_counterfactual'),
)
#: 러너 수 칸 — ASCII 10 진 (부호 · 공백 · 밑줄 · 유니코드 숫자 · nan · inf 낱말 거부 · 넘침 (1e999) 은 유한성 검사가 잡는다)
_RUNNER_NUM_RE = r'(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?'
#: ★ Z3 — 글자 그대로 0 인 10 진 (가수의 숫자가 전부 0 · 지수는 아무것) — 천장 극한 R_j 0 의 표기 (언더플로로 0 이 된 글자와 가른다)
_RUNNER_ZERO_RE = r'(?:0+(?:\.0*)?|\.0+)(?:[eE][+-]?[0-9]+)?'
_RUNNER_TOKEN_RE = r'[A-Za-z0-9_]+'
_RUNNER_SAFE_RE = r'[A-Za-z0-9._=,+ -]*'          # 러너가 생성 스크립트에 박는 문자 (R5-CX-01 — `$` · 따옴표 · 구분자 · 개행 없음)
_RUNNER_CJ_NUM = ('R_j_ohm', 's_min_um', 'tol_ff_um')


def _runner_float(raw):
    """러너 env 문자열 → 유한 float | None (엄격 · 조용한 강제 없음)."""
    import re as _re
    if not isinstance(raw, str) or not _re.fullmatch(_RUNNER_NUM_RE, raw):
        return None
    x = float(raw)
    return x if math.isfinite(x) else None


def runner_ca_ext(env, *, ptfe_stamp='off', lean='0', fibre_stamp='segment', periodic=False, sdcp_bridge='',
                  sigma_vgcf_override='', sigma_ptfe='', ptfe_block_um='', ptfe_block_scope=''):
    """★ 2026-10-20 (Rint ② B6) — 러너 env (문자열 · 비움 = 끔) → `{'receipt': 영수증 선택 칸, 'problems': [구조화 사유]}` = **발사 전
    계약 검사** (설계 v1 §7 · §4-3 · §5-2 · §6).  러너의 영수증 조립 (heredoc) 이 부른다 — 문제가 하나라도 있으면 OUTDIR 을 만들기 전에 선다.
    · 값: 수 = ASCII 10 진 · 유한 (`_RUNNER_NUM_RE`) · 법칙 = 낱말 토큰 · c = '0' | '1' (payload 선택지)
    · 선언 칸 = 매니페스트 protocol 정본 (`ca_ext_request_problem` — 칸 집합 · 정본 함수로 다시 만들 수 있는 값 · P1 = 지금 거부)
    · 조합 = 러너가 가진 축만 (LEAN · 섬유 스탬프 · 주기 · SDCP 브리지 · σ_VGCF 고정 · PTFE σ · 차단) — payload 입구 거부의 **부분집합**
      (`scripts/test_ca_ext_runner.py` N6b 가 같은 조합을 payload 에 직접 넣어 거부를 확인한다 · 과잉차단 금지)
    · rtol = (0, 봉인 상한] (`step3_conv_cert.CERT_RTOL_MAX`) — 밖이면 증서 ⓐ 가 반드시 실패해 미게시 팔만 만든다 (계산 낭비 차단)
    payload 인자 · `--expect-physics` 선언 칸 · 이름 태그는 `runner_ca_ext_view` 가 **영수증에서** 만든다 (사본 없음)."""
    import re as _re
    probs = []

    def _p(code, why):
        probs.append(f'RUNNER_CA_EXT|{code}| {why}')

    def _gt0(v):
        try:
            return float(v) > 0.0
        except (TypeError, ValueError):
            return False
    env = env if isinstance(env, dict) else {}
    names = [n for n, _s, _k in RUNNER_CA_EXT_ENV]
    _unk = sorted(k for k in env if k not in names)
    if _unk:
        _p('UNKNOWN', f'모르는 손잡이 {_unk} (아는 것: {names})')
    raw = {n: (env.get(n) if isinstance(env.get(n), str) else '') for n in names}
    sw = raw['CJUNC']
    if sw not in ('', '0', '1'):
        _p('SWITCH', f'CJUNC = {sw!r} — 비움 · 0 (끔) · 1 (켬) 만')
    on = sw == '1'
    cj_named = [(n, k) for n, s, k in RUNNER_CA_EXT_ENV if s == 'cjunc' and k]
    req = {}
    if on:
        miss = [n for n, _k in cj_named if raw[n] == '']
        if miss:
            _p('MISSING', f'CJUNC=1 인데 {miss} 가 없다 — 기본값 없음 (결과 전 선언 · 숫자 = 등록 R §2-1 · S0 단계 1)')
        else:
            cj, bad = {}, []
            for n, k in cj_named:
                v = raw[n]
                if k == 'R_j_ohm' and v == 'inf':
                    #  ★ Z3 (등록 R §3-1) — 바닥 극한 = 낱말 `inf` 하나 (INF · Infinity · +inf · 1e999 넘침 = 아래 ASCII 10 진 규칙이 거부) →
                    #    요청 = R_j_ohm null + rj_limit 'inf' (JSON 은 inf 를 못 쓴다 · 매니페스트 protocol 과 한 꼴)
                    cj[k] = None
                    cj['rj_limit'] = 'inf'
                elif k in _RUNNER_CJ_NUM:
                    x = _runner_float(v)
                    if x is None:
                        bad.append(f'{n}={v!r} (ASCII 10 진 · 유한 · 부호 없음)')
                    elif k == 'R_j_ohm' and x == 0.0 and not _re.fullmatch(_RUNNER_ZERO_RE, v):
                        #  ★ Z3 — 0 이 아닌 글자가 float 에서 0 으로 떨어졌다 (언더플로 · 예 1e-400) — 천장 극한으로 바꾸지 않는다
                        bad.append(f'{n}={v!r} — 0 이 아닌 값이 float 에서 0 으로 떨어진다 (언더플로 · 천장 극한은 글자 그대로 0 만)')
                    else:
                        cj[k] = x
                        if k == 'R_j_ohm' and x == 0.0:           # ★ Z3 — 천장 극한 = 글자 그대로 0 인 10 진 (0 · 0.0 · 0e0 — 같은 물리 = 같은 요청)
                            cj['rj_limit'] = 'zero'
                elif _re.fullmatch(_RUNNER_TOKEN_RE, v):
                    cj[k] = v
                else:
                    bad.append(f'{n}={v!r} (낱말 토큰)')
            if bad:
                _p('VALUE', ' · '.join(bad))
            else:
                req['cjunc'] = cj
    else:
        given = [n for n, _k in cj_named if raw[n] != '']
        if given:
            _p('FLAG_WITHOUT_CJUNC', f'{given} 는 CJUNC=1 일 때만 뜻이 있다 (조용한 no-op 금지)')
    _svcf = raw['CJUNC_SV_CF']                                   # ★ 10-21 (D) — SV 반사실 대조 (비움 · 0 = 끔 · 1 = 켬)
    if _svcf not in ('', '0', '1'):
        _p('VALUE', f'CJUNC_SV_CF={_svcf!r} — 비움 · 0 (끔) · 1 (켬) 만 (등록 R §5-6 SV 반사실 대조 · 문턱 = 사슬 계획)')
    elif _svcf == '1' and not on:
        _p('FLAG_WITHOUT_CJUNC', 'CJUNC_SV_CF=1 은 CJUNC=1 일 때만 뜻이 있다 (SV 반사실 = 접합 원장의 SV 면 · 조용한 no-op 금지)')
    c = raw['SDCP_MOD_C']
    if c != '':
        if not on:
            _p('NO_CJUNC', f'SDCP_MOD_C={c!r} — S3 SDCP 수정자는 S2 탄소 접합 (CJUNC=1) 과만 (설계 §5-2)')
        elif c not in ('0', '1'):
            _p('VALUE', f'SDCP_MOD_C={c!r} — 0 · 1 만 (payload `--step3-sdcp-mod-c` 선택지 · 정량 시나리오 두 끝 · 설계 §5-2)')
        else:
            req['sdcp_mod'] = {'c': float(c)}
    if 'cjunc' in req:
        why = ca_ext_request_problem(req, ptfe_stamp=str(ptfe_stamp))   # ★ Z3 — 러너의 PTFE 규약으로 (P1 = face_alpha 에서만)
        if why:
            _p('REQUEST', why)
    if on and str(ptfe_stamp) == 'centerline':
        #  ★ 10-21 (D · 사전 리뷰 PRE-impl-03 ① · 코디네이터 Q-C) — centerline + 접합 = 발사 전 거부 (P0 도 · payload 입구 PTFE_CENTERLINE 과 같은 조합)
        _p('PTFE_CENTERLINE', 'CJUNC=1 + PTFE_STAMP=centerline — 덮인 접점 셀의 포트 옮김이 Rayleigh 를 깬다 (PRE-impl-03) · 접합은 off · '
                              'face_alpha 에서만')
    fa = str(ptfe_stamp) == 'face_alpha'
    for _lab, _on in (('CJUNC=1', on), ('PTFE_STAMP=face_alpha', fa)):
        if not _on:
            continue
        if str(lean) not in ('2', '3'):
            _p('LEAN', f'{_lab} 인데 LEAN={lean} — v0 = LEAN 2 · 3 만 (원장을 안 읽는 솔브 · 진단 · 필드 · 설계 §7 LEAN 표)')
        if str(fibre_stamp) != 'segment':
            _p('SEGMENT', f'{_lab} 인데 FIBRE_STAMP={fibre_stamp} — 선분 스탬프 (연속 중심선) 에서만')
        if periodic:
            _p('PERIODIC', f'{_lab} 인데 MPM_PERIODIC_SIGMA=1 — 정량 모드 거부 (주기 seam 미지원)')
    if on:
        #  ★ Z3 — PTFE_STAMP=face_alpha + CJUNC=1 = 받는다 (설계 §3 · §4 조합 규칙 · 등록 R §10 꼴 · B6 통합 때의 임시 거부를 뺐다)
        if _gt0(sdcp_bridge):
            _p('SDCP_BRIDGE', f'SDCP_BRIDGE={sdcp_bridge} — SDCP 브리지 진단 팔과 접합 동시 = 거부 (설계 §4-3)')
        if str(sigma_vgcf_override or '') != '' and not _gt0(sigma_vgcf_override):
            _p('VGCF_INSULATING', f'SIGMA_VGCF_OVERRIDE={sigma_vgcf_override} — 전자 채널에서 VGCF 가 절연이면 접합이 뜻을 잃는다')
    if fa:
        if _gt0(sigma_ptfe):
            _p('SIGMA_PTFE', f'SIGMA_PTFE={sigma_ptfe} — face_alpha 는 PTFE 셀이 없어 σ_PTFE 가 걸릴 자리가 없다 (조용한 no-op)')
        if _gt0(ptfe_block_um) or str(ptfe_block_scope or '') not in ('', 'se'):
            _p('PTFE_BLOCK', f'PTFE_BLOCK_UM={ptfe_block_um!r} · PTFE_BLOCK_SCOPE={ptfe_block_scope!r} — PTFE 셀이 없어 차단이 조용한 no-op')
    rec = {}
    rt = raw['STEP3_RTOL']
    if rt != '':
        x = _runner_float(rt)
        if x is None:
            _p('VALUE', f'STEP3_RTOL={rt!r} (ASCII 10 진 · 유한)')
        else:
            import step3_conv_cert as _cc
            if not (0.0 < x <= _cc.CERT_RTOL_MAX):
                _p('RTOL', f'STEP3_RTOL={rt} — (0, {_cc.CERT_RTOL_MAX:g}] 밖 — 수렴 증서 ⓐ 가 반드시 실패해 미게시 팔만 만든다 '
                           f'(봉인 상한 · 설계 §6)')
            else:
                rec['step3_rtol'] = x
    #  ★ 2026-10-20 (Rint ② Z1) — 다음 세대 노브 (S1 face_alpha · S2 접합 · S3 수정자) = `STEP3_RTOL` **필수** (팔 시작 전).
    #    옛 판은 계산을 다 한 뒤 판정기 · 봉인의 `next_gen_cert_ok` 에서 증서 없음 (`CERT|absent|`) 으로 HOLD 했다 = GPU 시간 낭비.
    #    기본값을 채우지 않는다 (결과 전 선언 원칙 — 값은 등록 R §3-5 의 봉인값을 사람이 · 사슬이 명시한다) · 옛 세대 (노브 끔) 는 그대로.
    _ng_on = [lab for lab, cond in (('CJUNC=1', on), ('PTFE_STAMP=face_alpha', fa), (f'SDCP_MOD_C={c!r}', c != '')) if cond]
    if _ng_on and rt == '':
        import step3_conv_cert as _cc2
        _p('RTOL_REQUIRED', f'{" · ".join(_ng_on)} 인데 STEP3_RTOL 이 없다 — 다음 세대 팔은 수렴 증서 (설계 §6 · N15) 없이 게시되지 '
                            f'않아 계산을 다 한 뒤 봉인에서 HOLD 된다 (GPU 시간 낭비) · 기본값 없음 — 값을 명시할 것 '
                            f'(봉인 상한 {_cc2.CERT_RTOL_MAX:g} · 등록 R §3-5)')
    #  ★ 2026-10-20 (Rint ② Z1 · 설계 v1 §1-2 #1 · #2 · §7) — VGCF bulk σ → 직경 보존 복셀 σ (러너 run_arm 이 팔마다 같은 함수로 계산).
    #    `SIGMA_VGCF_OVERRIDE` (복셀값 직접 · 재척도 우회) 와 동시 = 거부 — 둘 다 주면 어느 σ 가 쓰였는지 런이 말할 수 없다.
    fb = raw['SIGMA_FIBRE_BULK']
    if fb != '':
        if str(sigma_vgcf_override or '') != '':
            _p('SIGMA_VGCF_BOTH', f'SIGMA_FIBRE_BULK={fb!r} + SIGMA_VGCF_OVERRIDE={sigma_vgcf_override!r} — 하나만 (bulk = 직경 보존 식으로 '
                                  f'복셀 σ 를 만든다 · override = 복셀값 직접 · 다음 세대 판정 런은 override 를 쓰지 않는다 · 설계 §1-2 #2 · §7)')
        x = _runner_float(fb)
        if x is None or not x > 0.0:
            _p('VALUE', f'SIGMA_FIBRE_BULK={fb!r} (ASCII 10 진 · 유한 · > 0 [S/cm] — VGCF 단섬유 bulk σ · 예 1e4 = Endo 흑연화 · '
                        f'설계 §1-2 #1)')
        else:
            import step3_sigma as _s3r
            rec['sigma_vgcf_bulk_S_cm'] = x
            rec['sigma_vgcf_rule'] = _s3r.VGCF_SIGMA_RULE
    if req:
        rec['ca_ext_request'] = req
    if _svcf == '1' and on:
        rec['sv_counterfactual'] = True                          # ★ 10-21 (D) — 선택 칸 (켬일 때만 · 끔 = 칸 없음 = 옛 digest)
    return {'receipt': ({} if probs else rec), 'problems': probs}


def _runner_tag_num(x):
    """수 → 무손실 · 정규 이름 조각 (repr 최단 왕복 표기 · 끝 '.0' 떼기 · '.' → p · '-' → m · '+' 떼기 — `2.5` ↔ `25` 가 갈린다)."""
    s = repr(float(x))
    if s.endswith('.0'):
        s = s[:-2]
    return s.replace('+', '').replace('.', 'p').replace('-', 'm')


def _ca_ext_cli_flag(sub, key, *, switch=False):
    """선언 칸 → payload 플래그 — `CLI_ACCOUNTING` 의 protocol_ext 칸 (규칙 M 이 실물 파서와 대조하는 정본) 에서 거꾸로 찾는다 (사본 없음).
    `switch` = 켜는 플래그 (그 하위 블록의 모델 판 칸 하나만 내는 것)."""
    want = (f'ca_ext.{sub}.model',) if switch else None
    hit = [o for o, (cat, flds) in CLI_ACCOUNTING.items()
           if cat == 'protocol_ext' and flds and (tuple(flds) == want if switch else flds[0] == f'ca_ext.{sub}.{key}')]
    if len(hit) != 1:
        raise ValueError(f'ca_ext.{sub}.{key or "model"} 를 내는 payload 플래그가 {len(hit)} 개다 (정확히 1 개여야 · CLI_ACCOUNTING)')
    return hit[0]


def runner_ca_ext_view(rec):
    """★ 2026-10-20 (Rint ② B6) — 러너 영수증 → `{'flags', 'expect', 'tag', 'arm_tag'}` — payload 인자 · `--expect-physics` 선언 칸 · 이름
    태그를 **영수증 하나에서** 만든다 (선언한 축 = 넘긴 인자 = 영수증 = 매니페스트 축 · `receipt_match` 가 팔마다 대조).
    · flags   = ' --step3-cjunc --step3-cjunc-rj <repr> … --step3-sdcp-mod-c <0|1> --step3-rtol <repr>' (끔 = '')
    · expect  = ',ca_ext.cjunc.<칸>=<값> …' (러너의 선언 뒤에 붙인다 · payload 는 켠 블록의 칸이 다 선언돼야 돈다 · 끔 = '')
    · tag     = '_cj<R_j>_<요청 해시 8>' + '_c<0|1>' + '_rt<rtol>' + '_fb<VGCF bulk σ>' (무손실 정규 표기 · OUTDIR 과 팔 이름 · 같은 물리 = 같은 이름)
    · arm_tag = ('_fa' if face_alpha) + tag — 팔 이름 (옛 팔과 이름이 겹치지 않게 · 명시 OUTDIR 의 SKIP 캐시 함정)
    · vgcf_bulk = VGCF bulk σ 의 repr (run_arm 이 `step3_sigma.vgcf_sigma_from_bulk` 로 팔마다 복셀 σ 를 계산 · 끔 = '' = 옛 bulk 100)
    ⚠ 요청이 정본 검사를 못 지나거나 출력에 생성 스크립트 밖 문자가 있으면 ValueError (영수증이 손으로 바뀐 경우 · fail-closed)."""
    import hashlib as _hl
    import json as _json
    import re as _re
    rec = rec if isinstance(rec, dict) else {}
    req = rec.get('ca_ext_request')
    fl, xp, tg = [], [], []
    if req is not None:
        why = ca_ext_request_problem(req, ptfe_stamp=rec.get('ptfe_stamp', 'off'))   # ★ Z3 — 영수증의 PTFE 규약으로 (P1 = face_alpha 에서만)
        if why:
            raise ValueError(f'영수증의 ca_ext_request 가 정본 검사를 못 지난다 — {why}')
        import ca_ext_cjunc as _cw
        cj = req['cjunc']
        lim = cj.get('rj_limit')
        fl.append(_ca_ext_cli_flag('cjunc', None, switch=True))
        for k in _cw.REQUEST_KEYS_CJUNC:
            if k == 'R_j_ohm' and lim == 'inf':
                #  ★ Z3 — 바닥: payload 인자 = `inf` (float · 극한 표지와 짝) · 선언 = 매니페스트 protocol 값 (null → `None`)
                fl += [_ca_ext_cli_flag('cjunc', k), 'inf']
                xp.append(f'ca_ext.cjunc.{k}=None')
                continue
            sv = repr(float(cj[k])) if k in _RUNNER_CJ_NUM else str(cj[k])
            fl += [_ca_ext_cli_flag('cjunc', k), sv]
            xp.append(f'ca_ext.cjunc.{k}={sv}')
        if lim is not None:                                       # ★ Z3 — 극한 표지 (payload 플래그 · 선언 칸 = protocol `rj_limit`)
            fl += [_ca_ext_cli_flag('cjunc', 'rj_limit'), str(lim)]
            xp.append(f'ca_ext.cjunc.rj_limit={lim}')
        h8 = _hl.sha256(_json.dumps(cj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()[:8]
        tg.append(f'_cj{"inf" if lim == "inf" else _runner_tag_num(cj["R_j_ohm"])}_{h8}')
        if 'sdcp_mod' in req:
            cv = float(req['sdcp_mod']['c'])
            fl += [_ca_ext_cli_flag('sdcp_mod', 'c'), str(int(cv))]
            xp.append(f'ca_ext.sdcp_mod.c={cv!r}')
            tg.append(f'_c{int(cv)}')
    rt = rec.get('step3_rtol')
    if rt is not None:
        if '--step3-rtol' not in CLI_ACCOUNTING:
            raise ValueError('--step3-rtol 이 CLI_ACCOUNTING 에 없다 (payload 플래그 정본)')
        fl += ['--step3-rtol', repr(float(rt))]
        tg.append(f'_rt{_runner_tag_num(rt)}')
    #  ★ 2026-10-20 (Rint ② Z1) — VGCF bulk σ: payload 기록 플래그 (CLI 회계에서 그 칸을 내는 플래그를 찾는다 · 사본 없음) · 이름 태그 `_fb<값>`
    #    (OUTDIR · 팔 이름 — 명시 OUTDIR 의 옛 팔과 이름이 겹치면 check_arm 이 그 옛 팔을 "불완전" 으로 지운다) · 값 줄 (run_arm 이 직경 보존 σ 를 계산).
    fb = rec.get('sigma_vgcf_bulk_S_cm')
    vgcf_bulk = ''
    if fb is not None:
        _rl = rec.get('sigma_vgcf_rule')
        #  ⚠ 형을 먼저 본다 — `float(True)` = 1.0 · `float('1e4')` = 1e4 로 조용히 바뀌면 손으로 바뀐 영수증이 정상 태그를 얻는다
        if isinstance(fb, bool) or not isinstance(fb, (int, float)) or not (math.isfinite(float(fb)) and float(fb) > 0.0) \
                or not isinstance(_rl, str) or not _rl:
            raise ValueError(f'영수증의 sigma_vgcf_bulk_S_cm = {fb!r} · sigma_vgcf_rule = {_rl!r} — 유한 > 0 수 + 식 이름 문자열이어야 한다')
        _x = float(fb)
        _hit = [o for o, (_c, _f) in CLI_ACCOUNTING.items() if _f and 'sigma_vgcf_bulk_S_cm' in _f]
        if len(_hit) != 1:
            raise ValueError(f'sigma_vgcf_bulk_S_cm 를 내는 payload 플래그가 {len(_hit)} 개다 (정확히 1 개여야 · CLI_ACCOUNTING)')
        vgcf_bulk = repr(_x)
        fl += [_hit[0], vgcf_bulk]
        tg.append(f'_fb{_runner_tag_num(_x)}')
    #  ★ 2026-10-21 (D · 등록 R §5-6) — SV 반사실 대조: payload 켜기 플래그 (CLI 회계 정본에 있어야) · 이름 태그 `_svcf` (OUTDIR · 팔 이름 ·
    #    끈 팔과 이름이 겹치지 않게) · 선언 (--expect-physics) 없음 (protocol 밖).  접합 요청 없이 켬 = 손으로 바뀐 영수증 = 거부.
    _sv = rec.get('sv_counterfactual')
    if _sv is not None:
        if _sv is not True or req is None or 'cjunc' not in (req or {}):
            raise ValueError(f'영수증의 sv_counterfactual = {_sv!r} — True + 접합 요청 (ca_ext_request.cjunc) 과만')
        if '--step3-cjunc-sv-cf' not in CLI_ACCOUNTING:
            raise ValueError('--step3-cjunc-sv-cf 가 CLI_ACCOUNTING 에 없다 (payload 플래그 정본)')
        fl.append('--step3-cjunc-sv-cf')
        tg.append('_svcf')
    tag = ''.join(tg)
    out = {'flags': ''.join(' ' + x for x in fl), 'expect': ''.join(',' + x for x in xp), 'tag': tag,
           'arm_tag': ('_fa' if rec.get('ptfe_stamp') == 'face_alpha' else '') + tag, 'vgcf_bulk': vgcf_bulk}
    _bad = [k for k, v in out.items() if not _re.fullmatch(_RUNNER_SAFE_RE, v)]
    if _bad:
        raise ValueError(f'러너 인자 {_bad} 에 생성 스크립트 밖 문자가 있다 ({out})')
    return out


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
    'sdcp_bridge_um': float, 'ptfe_block_um': float,
    'sigma_vgcf_S_cm': float, 'sigma_sdcp_S_cm': float, 'sigma_ptfe_S_cm': float,
    'sigma_ion_se_S_cm': float, 'sigma_ion_sdcp_S_cm': float,
    'sigma_am_s_S_cm': float, 'sigma_am_p_S_cm': float,
    'fibre_stamp': str, 'sdcp_stamp': str, 'ptfe_stamp': str, 'cam': str,
    'se_source': str, 'dilate_z': float,
    'plate_rule': str, 'physics_protocol_id': str,
    'ptfe_cells_observed': int,
    'sigma_superp_S_cm': float, 'sigma_swcnt_S_cm': float, 'swcnt_ion_block': bool,
    'interface_model': str,                      # ① 계면 규약 표지 (None = 항 없음)
    #  ★ 2026-10-20 (Rint ② Z1) — σ_VGCF 출처 기록 (있을 때만 · 부재 = 끈 런)
    'sigma_vgcf_bulk_S_cm': float, 'sigma_vgcf_rule': str,
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
    #  ★ 2026-10-20 (Rint ② S1) — face_alpha 는 셀을 찍지 않는다 (sid 격자 = off 격자) ⇒ 관측 0 이 **정상**이고 > 0 이 위반이다
    #    (도장 ≠ 실물 — centerline 과 이중 계상).  아래 `!= off` 이진 분기에 face_alpha 를 넣으면 정상 런이 전부 거부된다.
    if man.get('ptfe_stamp') == 'face_alpha':
        if v != 0:
            return False, (f'PTFE|face_alpha_cells| `ptfe_stamp=face_alpha` 인데 관측 sid7 셀이 {v} 이다 — 면 개구율은 셀을 '
                           f'찍지 않는다 (sid 격자 = off 격자) · centerline 과 이중 계상')
        return True, None
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

#: 결과 블록 계약 (R5-CX-05) — 위치가 전자 · 이온 · 열 · 기공과 다른 component.  **무엇이 나왔는가**를 본다.
#  ⚠ 위치는 producer 안에 있다 — 몰랐던 것이 아니라 안 적었던 것이다 (`mpm_webapp_payload.py:2162` · `:1765`).
#  ★★ 2026-10-05 (Codex RGL-01 · P1) — 옛 주석은 *"collector 에는 CG 가 없다"* 였다.  **틀렸다** — collector 기하는
#    보조 σ_e 솔브 둘 (wetted · bare) 의 차다.  그 전제로 σ 부호만 봐서, 실물 producer 에서 wetted (또는 bare) 호출만
#    CG_MAXITER=1 로 제한해 보조 σ 가 정상의 7.57 배가 돼도 producer 게시 · complete · check-arm rc 0 이었다.
#    ⇒ `convs` = 보조 솔브마다 (cg_info, unconverged, resid) 키 — 주 솔브와 **같은** `conv_ok` conjunction 을 둘 다 채워야
#      한다.  없으면 blind (옛 세대 payload 도 — 보조 솔브가 수렴했는지 모르는 R_geom 을 받지 않는다 · CDXR2-4 와 같은 결).
#    ⚠ 이것은 **수렴 증거**다.  `interface_record_ok` 의 적용 영수증 (요청 표가 그 솔브에 걸렸나) 과 섞지 않는다.
COMPONENT_RESULT = {
    'pnm': dict(path=('pore', 'pnm'), ints=('n_pores', 'n_throats'),
                reason_means_incomplete=True),
    'collector_geom': dict(path=('collector_geometric',),
                           #  ⚠ `R_geom_ohm_cm2` 는 **정당하게 None** 일 수 있다
                           #    (bare/wetted 중 하나가 reason 을 냈을 때) ⇒ 요구하지 않는다.
                           positives=('wetted_sigma_S_cm', 'bare_sigma_S_cm'),
                           convs=(('wetted_cg_info', 'wetted_unconverged', 'wetted_cg_resid'),
                                  ('bare_cg_info', 'bare_unconverged', 'bare_cg_resid'))),
}


def component_evidence_ok(step3, required):
    """**계획된 component 마다** 수치·수렴·backend 증거가 있는가 → `(ok, reason|None)`.

    ★★★ 2026-08-25 (R4-CX-02, Codex 4차): `numeric_ok` 가 **전자 top-level 만** 봤다.
      그래서 Codex 가 통과시켰다 —
        · thermal/pore `resid=1e100` · `unconverged=True`  → producer None · final h0
        · 계획된 ionic 의 결과·CG·resid **전부 삭제**       → producer None · final h0
      계획했으면 그 축의 증거도 계획의 일부다.
    ⚠ pnm · collector_geom 은 `COMPONENT_RESULT` 의 결과 블록 계약으로 본다 (R5-CX-05) — collector 는 보조 솔브
      둘의 수렴 3필드까지 (RGL-01).  옛 주석 *"status 로만 본다"* 는 R5-CX-05 이후로 사실이 아니다.
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
        #  ⚠ 이 둘은 결과 위치 · 모양이 다르다 (pnm = 위상 결과 · CG 없음).  ⛔ 옛 문장 *"이 둘은 CG 수렴이 없다"* 는
        #    collector 에 대해 거짓이었다 — 보조 σ_e 솔브 둘의 차다 (RGL-01) → `convs` 로 수렴까지 본다.
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
            #  ★ RGL-01 — 결과가 CG 솔브의 산물이면 그 솔브들이 **각각** 수렴했어야 한다 (한 쪽만 봐도 안 된다)
            for (_ki, _ku, _kr) in _rspec.get('convs', ()):
                _cok, _cwhy = conv_ok(_blk.get(_ki), _blk.get(_ku), _blk.get(_kr))
                if not _cok:
                    return False, (f'EVID|{comp}|conv|{_cwhy}| {_ki}={_blk.get(_ki)!r} '
                                   f'{_ku}={_blk.get(_ku)!r} {_kr}={_blk.get(_kr)!r} — 이 결과를 만든 '
                                   f'보조 솔브의 수렴이 확인되지 않는다 (적용 영수증은 수렴 증거가 아니다 · RGL-01)')
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


#: ★ 2026-10-03 (Codex r_int 1단계 `RINT-02` · `13` · `14` · 1저자 비준 G1) — ① 계면 저항 **요청 ↔ 적용 영수증**.
#   요청 표 (`interface_rint_e_ohm_cm2` · `_i_`) 는 CLI 파서가 솔브와 **독립으로** 만든다.  영수증은 네 솔브 각각이
#   **실제로 받은** 표 · 모델 · 단위 · 면 수다.  주 솔브만 보면 wetted/bare 호출의 배선 삭제가 산다 (Codex 변이 탐침:
#   wetted 호출의 rint 만 지우면 주 σ · 면 · 표는 그대로인데 wetted σ 0.0009487 → 0.0009606 · R_geom 0 → 0.0544 Ω·cm²).
#   솔브 이름 → (채널 꼬리 'e'|'i', 그 솔브를 끄는 `component_plan` 키 | None = 끌 수 없음).
INTERFACE_SOLVES = {'electronic_main': ('e', None), 'electronic_wetted': ('e', 'collector'),
                    'electronic_bare': ('e', 'collector'), 'ionic': ('i', 'ionic')}
#: 정상 상태 — 면 0 을 하나로 덮지 않는다 (Codex Q4: absent geometry / disabled / unsupported identity / failed).
#   unsupported identity (같은 상 AM 쌍인데 pid 없음 · 절연 상 쌍) 는 솔버 · 파서가 **거부**하므로 상태가 아니다.
#   'missing' · 'applied_without_request' 는 생산자가 쓰는 **위반 표지**다 — 적히면 계약이 거부한다.
INTERFACE_OK_STATUSES = ('applied', 'absent_geometry', 'zero_table', 'failed', 'disabled', 'not_requested')
INTERFACE_UNIT = 'ohm_cm2'
_IFACE_REC_KEYS = ('model', 'unit', 'table', 'pid_used', 'n_faces_rint', 'faces_by_pair', 'solved')


def interface_receipt(res, requested, disabled_why=None):
    """솔브 결과 1 건 → 영수증 dict.  `requested` = 그 채널의 **요청** 기록 (`rint_table_record` · 없으면 None).

    ⚠ 상태는 요청과 솔브 기록을 **따로** 보고 정한다 — 솔브 기록만 보고 정하면 배선이 지워진 호출이
      'not_requested' 로 둔갑한다 (Codex: *"model 이 None 이면 검사도 생략하는 구조는 금지"*)."""
    if disabled_why is not None:
        return ({'status': 'not_requested'} if requested is None
                else {'status': 'disabled', 'why': str(disabled_why)})
    rec = res.get('interface') if isinstance(res, dict) else None
    if requested is None:
        if isinstance(rec, dict):
            return {'status': 'applied_without_request', **{k: rec.get(k) for k in _IFACE_REC_KEYS}}
        return {'status': 'not_requested'}
    if not isinstance(res, dict):
        return {'status': 'missing', 'why': '솔브 결과가 없다'}
    if not isinstance(rec, dict):
        return {'status': 'missing',
                'why': '솔브 결과에 계면 기록이 없다 — 요청 표가 이 호출에 전달되지 않았다'}
    out = {k: rec.get(k) for k in _IFACE_REC_KEYS}
    if res.get('reason') or rec.get('solved') is not True:
        out.update(status='failed', why=str(res.get('reason') or 'unsolved'))
    elif type(out['n_faces_rint']) is int and out['n_faces_rint'] > 0:      # noqa: E721
        out['status'] = 'applied'
    elif isinstance(out['table'], dict) and out['table'] and all(v == 0 for v in out['table'].values()):
        out['status'] = 'zero_table'
    else:
        out['status'] = 'absent_geometry'
    return out


def _iface_table_ok(tb):
    """요청 표 기록 모양 → `(ok, why)`.  키 'A|B' (sid 오름차순 · 정본 이름) · 값 유한 0 이상 실수 (bool 금지) ·
    같은 상 쌍은 pid 소유 상 (AM) 만.  이름 · 소유 상의 정본은 `step3_sigma` 다 (사본을 두지 않는다)."""
    if not isinstance(tb, dict) or not tb:
        return False, f'비지 않은 dict 이어야 한다 ({tb!r})'
    try:
        from step3_sigma import SID_NAME, PID_OWNER_SIDS
    except Exception as e:                                       # noqa: BLE001
        return False, (f'step3_sigma 를 불러 표를 확인할 수 없다 ({type(e).__name__}) — '
                       f'확인 못 한 것을 통과시키지 않는다')
    _sid = {v: k for k, v in SID_NAME.items()}
    for k, v in tb.items():
        if not isinstance(k, str) or k.count('|') != 1:
            return False, f'키 {k!r} 가 "A|B" 가 아니다'
        a, b = k.split('|')
        if a not in _sid or b not in _sid:
            return False, f'키 {k!r} 에 모르는 상'
        if _sid[a] > _sid[b]:
            return False, f'키 {k!r} 가 정본 순서 (sid 오름차순) 가 아니다'
        if a == b and _sid[a] not in PID_OWNER_SIDS:
            return False, f'같은 상 쌍 {k} 은 pid 소유 상 (AM) 만 (RINT-01)'
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v < 0:
            return False, f'{k} = {v!r} (유한한 0 이상 실수여야 한다)'
    return True, None


def interface_record_ok(man):
    """① 계면 저항 **요청 ↔ 적용** 계약 → `(ok, reason|None)`.  producer (게시 전) · `check_arm` · 판정기가
    같이 쓴다 (RINT-02 · 13 · 14).

    · 요청 표 · 모델 · 영수증이 **전부 없으면** 항 없음 (옛 세대 포함) = 통과
    · 모델 ⇔ 요청 — 요청이 있는데 모델 None 이면 위반 (검사를 끄는 경로) · 요청 없는데 모델만 있어도 위반
    · 요청이 있으면 네 솔브 영수증이 정확히 있어야 한다.  채널 요청이 있는데 `not_requested` = 배선 삭제 ·
      채널 요청이 없는데 적용 = 요청 밖 적용
    · applied · absent_geometry · zero_table · failed — 솔브 기록의 model · unit · 표가 요청과 **같고**, 면 수는
      쌍별 합과 같고, 쌍은 표 안 · 양의 r 쌍에만 면이 있다.  같은 상 AM 쌍이면 pid 를 썼어야 한다
    · disabled — 그 솔브를 끄는 계획 키가 False 일 때만 (주 전자 솔브는 끌 수 없다)
    """
    m = man if isinstance(man, dict) else {}
    req = {'e': m.get('interface_rint_e_ohm_cm2'), 'i': m.get('interface_rint_i_ohm_cm2')}
    model = m.get('interface_model')
    rc = m.get('interface_receipts')
    any_req = any(v is not None for v in req.values())
    for ch, tb in req.items():
        if tb is not None:
            _ok, _why = _iface_table_ok(tb)
            if not _ok:
                return False, f'IFACE|table|{ch}| 요청 표 {_why}'
    if any_req:
        try:
            from step3_sigma import INTERFACE_MODEL_VERSION as _MV
        except Exception as e:                                   # noqa: BLE001
            return False, f'IFACE|model|unverifiable| step3_sigma 를 불러올 수 없다 ({type(e).__name__})'
        if model is None:
            return False, ('IFACE|model|absent| 요청 표가 있는데 interface_model 이 None — '
                           '"model 이 없으면 검사 생략" 경로는 금지 (Codex Q4)')
        if model != _MV:
            return False, f'IFACE|model|unknown| {model!r} ≠ 이 코드의 {_MV!r}'
    elif model is not None:
        return False, f'IFACE|model|orphan| 요청 표가 없는데 interface_model={model!r}'
    if rc is None:
        if any_req:
            return False, ('IFACE|receipts|absent| 요청 표가 있는데 솔브 영수증이 없다 — 네 솔브가 표를 '
                           '실제로 받았는지 확인할 수 없다 (RINT-02)')
        return True, None
    if not isinstance(rc, dict):
        return False, f'IFACE|receipts|shape| dict 이어야 하는데 {type(rc).__name__}'
    if set(rc) != set(INTERFACE_SOLVES):
        return False, f'IFACE|receipts|keys| {sorted(rc)} ≠ {sorted(INTERFACE_SOLVES)}'
    plan = m.get('component_plan') if isinstance(m.get('component_plan'), dict) else None
    for name, (ch, plan_key) in INTERFACE_SOLVES.items():
        r = rc[name]
        if not isinstance(r, dict):
            return False, f'IFACE|{name}|shape| 영수증이 dict 가 아니다'
        st = r.get('status')
        tb = req[ch]
        if st == 'missing':
            return False, f'IFACE|{name}|missing| 요청 표가 이 솔브에 전달되지 않았다 ({r.get("why")})'
        if st == 'applied_without_request':
            return False, f'IFACE|{name}|unrequested| 요청 없는 계면 표가 이 솔브에 적용됐다'
        if st not in INTERFACE_OK_STATUSES:
            return False, f'IFACE|{name}|status| 모르는 상태 {st!r}'
        if st == 'not_requested':
            if tb is not None:
                return False, (f'IFACE|{name}|dropped| 채널 {ch} 표가 요청됐는데 영수증은 not_requested — '
                               f'배선이 빠졌다')
            continue
        if tb is None:
            return False, f'IFACE|{name}|unrequested| 채널 {ch} 요청이 없는데 상태 {st}'
        if st == 'disabled':
            if plan_key is None:
                return False, f'IFACE|{name}|disabled| 이 솔브는 끌 수 없다'
            if plan is None or plan.get(plan_key) is not False:
                return False, (f'IFACE|{name}|disabled| 계획 `{plan_key}` = '
                               f'{None if plan is None else plan.get(plan_key)!r} 인데 disabled')
            continue
        if r.get('model') != model:
            return False, f'IFACE|{name}|model| 솔브 {r.get("model")!r} ≠ 매니페스트 {model!r}'
        if r.get('unit') != INTERFACE_UNIT:
            return False, f'IFACE|{name}|unit| {r.get("unit")!r} ≠ {INTERFACE_UNIT!r}'
        if r.get('table') != tb:
            return False, f'IFACE|{name}|table| 솔브가 받은 표 {r.get("table")!r} ≠ 요청 {tb!r}'
        if type(r.get('pid_used')) is not bool:                  # noqa: E721
            return False, f'IFACE|{name}|pid| pid_used={r.get("pid_used")!r} (bool 이어야 한다)'
        if any(k.split('|')[0] == k.split('|')[1] and v > 0 for k, v in tb.items()) and r['pid_used'] is not True:
            return False, f'IFACE|{name}|pid| 같은 상 AM 쌍이 있는데 pid 를 안 썼다 (unsupported identity)'
        n, fb = r.get('n_faces_rint'), r.get('faces_by_pair')
        if type(n) is not int or n < 0:                          # noqa: E721
            return False, f'IFACE|{name}|faces| n_faces_rint={n!r} (음이 아닌 정수)'
        if not isinstance(fb, dict) or any(type(c) is not int or c < 0 for c in fb.values()):  # noqa: E721
            return False, f'IFACE|{name}|faces| faces_by_pair={fb!r}'
        if any(k not in tb for k in fb):
            return False, f'IFACE|{name}|faces| 표 밖 쌍에 면 {sorted(set(fb) - set(tb))}'
        if any(c > 0 and tb[k] <= 0 for k, c in fb.items()):
            return False, f'IFACE|{name}|faces| r = 0 쌍에 면이 있다'
        if sum(fb.values()) != n:
            return False, f'IFACE|{name}|faces| 쌍별 합 {sum(fb.values())} ≠ n_faces_rint {n}'
        if st == 'failed':
            if not r.get('why') or n != 0:
                return False, f'IFACE|{name}|failed| 사유 없음 또는 면 {n} (실패한 솔브는 면 0)'
            continue
        if r.get('solved') is not True:
            return False, f'IFACE|{name}|solved| 상태 {st} 인데 solved={r.get("solved")!r}'
        if st == 'applied' and n <= 0:
            return False, f'IFACE|{name}|applied| 면 0 인데 applied'
        _zero = all(v == 0 for v in tb.values())
        if st == 'absent_geometry' and (n != 0 or _zero):
            return False, f'IFACE|{name}|absent| 면 {n} · 표 전부 0={_zero}'
        if st == 'zero_table' and (n != 0 or not _zero):
            return False, f'IFACE|{name}|zero| 면 {n} · 표 전부 0={_zero}'
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
                #  ★ RGL-01 — 보조 두 솔브의 수렴 3필드 (producer 가 싣는 그 키 · 이름).
                'collector_geometric': {'wetted_sigma_S_cm': 0.08,
                                        'bare_sigma_S_cm': 0.05,
                                        'wetted_cg_info': 0, 'wetted_unconverged': False,
                                        'wetted_cg_resid': 1e-8,
                                        'bare_cg_info': 0, 'bare_unconverged': False,
                                        'bare_cg_resid': 1e-8}}

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
    #  ── G8–G15: RGL-01 (Codex 10-05 · P1) — 보조 (wetted · bare) collector 솔브의 **수렴** ──────────────
    #    옛 계약은 "collector 에는 CG 가 없다" 는 전제로 σ 부호만 봤다 → 실물 producer 에서 wetted (또는 bare)
    #    호출만 CG_MAXITER=1 로 제한해 보조 σ 가 7.57 배가 돼도 complete · check-arm rc 0 이었다 (적용 영수증 ≠ 수렴).
    #    둘 다 주 솔브와 **같은** conv_ok conjunction 을 채워야 한다.  각 변이는 한 쪽만 건드린다 (독립 실패).
    def _g_cg(**over):
        _gs = _g_full()
        for _k, _v in over.items():
            if _v == '__pop__':
                _gs['collector_geometric'].pop(_k, None)
            else:
                _gs['collector_geometric'][_k] = _v
        return component_evidence_ok(_gs, _greq)
    _g8 = _g_cg(wetted_cg_info=1, wetted_unconverged=True, wetted_cg_resid=0.3464101615137754)
    chk(not _g8[0] and str(_g8[1]).startswith('EVID|collector_geom|conv|') and 'wetted' in str(_g8[1]),
        f'G8 ★★ wetted **만** 미수렴 (Codex 반례 수치) → 잡는다 ({str(_g8[1])[:60]})')
    _g9 = _g_cg(bare_cg_info=1, bare_unconverged=True, bare_cg_resid=0.3464101615137754)
    chk(not _g9[0] and str(_g9[1]).startswith('EVID|collector_geom|conv|') and 'bare' in str(_g9[1]),
        f'G9 ★★ bare **만** 미수렴 → 잡는다 (R_geom 0 clip 뒤에 가려지던 쪽) ({str(_g9[1])[:60]})')
    _g10 = _g_cg(bare_cg_resid='__pop__')
    chk(not _g10[0] and '|blind|' in str(_g10[1]), 'G10 ★ 보조 잔차 **누락** → blind (모르는 것은 통과가 아니다)')
    _g11 = _g_cg(wetted_cg_info='__pop__', wetted_unconverged='__pop__', wetted_cg_resid='__pop__')
    chk(not _g11[0] and '|blind|' in str(_g11[1]), 'G11 ★ wetted 3필드 **통째 누락** (옛 세대 모양) → blind')
    _g12 = _g_cg(bare_cg_info=3)
    chk(not _g12[0] and '|unconv|' in str(_g12[1]), 'G12 ★ **상충** — cg_info 3 인데 unconverged False → 잡는다')
    _g12b = _g_cg(wetted_unconverged=True)
    chk(not _g12b[0] and '|unconv|' in str(_g12b[1]), 'G12b ★ **상충** — cg_info 0 인데 unconverged True → 잡는다')
    for _bad in (float('nan'), float('inf'), -1e-9, 1e-3):
        _g13 = _g_cg(wetted_cg_resid=_bad)
        chk(not _g13[0] and '|resid|' in str(_g13[1]),
            f'G13({_bad!r}) ★ 보조 잔차가 비유한 · 음수 · 문턱 위 → 잡는다 (플래그는 수렴이어도)')
    _g14 = _g_cg(bare_cg_info=False)
    chk(not _g14[0] and '|type|' in str(_g14[1]), 'G14 ★ cg_info 가 bool → 잡는다 (주 솔브와 같은 타입 계약)')
    _g15 = _g_cg(wetted_cg_resid=CG_RESID_MAX, bare_cg_resid=0.0)
    chk(_g15 == (True, None), 'G15 정상 증인 — 문턱 **경계값** · 0 잔차는 통과 (과잉차단 없음)')

    #  ── H: 런 영수증 (R5-CX-03, Codex 5차 실측) ────────────────────────────────────
    #    HEAD 가 `edec17a2`, 러너 기본 vox 0.15 인데 모든 팔에 `vox_um=0.20` ·
    #    `code_sha=deadbeef` · 임의 digest 를 넣어도 producer/check_arm/final 이
    #    `None/None/h0` 였다.  러너의 **의도**가 결과와 대조된 적이 없었다.
    _h8 = [list(o) for o in sorted({(x, y, z) for x in (0.0, 0.075)
                                    for y in (0.0, 0.075) for z in (0.0, 0.075)})]
    _hrec = {'vox_um': 0.15, 'bridge_um': 0.48, 'fibre_stamp': 'segment',
             'sdcp_stamp': 'sphere', 'sdcp_sphere_d_um': 0.30,
             'sdcp_yield_to_vgcf': False, 'sdcp_bridge_um': 0.0,
             'ptfe_stamp': 'off', 'sigma_ptfe_S_cm': 0.0,
             'sigma_vgcf_S_cm': 78.54, 'periodic_xy': False,
             'code_sha': 'edec17a2', 'arms': 8, 'expect_backend': 'gpu',
             'origins': _h8}
    #  ⚠ 영수증은 **러너가 정한 축만** 담는다 — 전 축을 강제로 미러링하면
    #    새 축이 생길 때마다 픽스처가 KeyError 로 죽는다 (2026-08-30 실사고).
    _hman = {k: _hrec[k] for k in RECEIPT_AXES if k in _hrec}
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

    #  ── RCPT-sha — `_code_sha` 의 dirty **정의** (2026-08-25 kgy 실측 사고 회귀) ─────
    #    옛 정의는 porcelain 전체(untracked 포함)라, kgy 상주 로컬 디렉터리(anchor_params/
    #    db/ tools/)만으로 **모든 생산 런이 `+dirty` → 판정기 무조건 HOLD** 였다.
    #    정의: tracked 수정 = dirty · scripts/ 안 untracked = dirty (import shadowing) ·
    #    그 밖의 untracked = **dirty 아님** (코드를 못 바꾸는 파일은 재현성 딱지를 못 바꾼다).
    import importlib as _il
    import os
    import shutil as _sl
    import subprocess as _sp
    import sys as _sy
    import tempfile as _tf
    _sy.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    _pay = _il.import_module('mpm_webapp_payload')
    _git_ok = _sp.run(['git', '--version'], capture_output=True).returncode == 0
    if not _git_ok:
        print('  SKIP  RCPT-sha-* — git 없음 (이 환경에선 _code_sha 가 None 을 낸다)')
    else:
        _d = _tf.mkdtemp()
        _sd = os.path.join(_d, 'scripts')
        os.mkdir(_sd)
        with open(os.path.join(_sd, 'x.py'), 'w') as _f:
            _f.write('A = 1\n')
        for _c in (['git', 'init', '-q'], ['git', 'add', '-A'],
                   ['git', '-c', 'user.email=t@t', '-c', 'user.name=t',
                    'commit', '-qm', 'i']):
            _sp.run(_c, cwd=_d, capture_output=True)
        _s0 = _pay._code_sha(_sd)
        chk(bool(_s0) and '+dirty' not in _s0, 'RCPT-sha-clean 갓 커밋한 트리는 clean')
        with open(os.path.join(_d, 'stray_data.txt'), 'w') as _f:
            _f.write('x')
        os.mkdir(os.path.join(_d, 'outputs_local'))
        _s1 = _pay._code_sha(_sd)
        chk(bool(_s1) and '+dirty' not in _s1,
            'RCPT-sha-untracked ★★ scripts/ 밖 untracked 는 dirty 가 아니다 '
            '(kgy 상주 디렉터리가 생산 전체를 HOLD 시키던 정의 결함)')
        with open(os.path.join(_sd, 'shadow.py'), 'w') as _f:
            _f.write('B = 2\n')
        _s2 = _pay._code_sha(_sd)
        chk(bool(_s2) and _s2.endswith('+dirty'),
            'RCPT-sha-shadow ★ scripts/ 안 untracked 는 dirty (import shadowing 위험)')
        os.remove(os.path.join(_sd, 'shadow.py'))
        with open(os.path.join(_sd, 'x.py'), 'w') as _f:
            _f.write('A = 3\n')
        _s3 = _pay._code_sha(_sd)
        chk(bool(_s3) and _s3.endswith('+dirty'), 'RCPT-sha-modified tracked 수정은 dirty')
        _sl.rmtree(_d, ignore_errors=True)

    #  ── ★★ 2026-09-02 — `receipt_digest` 가 **무엇인지** 를 시험으로 박는다 ────────────
    #    계기: NODIGEST 에 두 축을 더한 뒤 커밋된 영수증 17건을 재계산했더니 **전부 불일치**
    #    했다.  5분간 오염으로 읽었는데, 원인은 내 변경이 아니라 08-30/08-31 에 늘어난
    #    `RECEIPT_AXES` 4개였다 (그 넷을 빼면 옛 digest 가 정확히 재현된다).
    #  ⇒ digest 는 **런타임 캐시 키**이지 내용 해시가 아니다.  코드 버전을 넘어 재현되지
    #    않는 것이 **설계**다 (새 축 = 새 디렉터리 = 낡은 팔 재사용 차단).  그런데 값이
    #    커밋된 디렉터리 이름에 박혀 있어 **내용 해시처럼 보인다** ⇒ 다음 사람이 같은
    #    오독을 한다.  두 성질을 각각 고정한다.
    _rc_fix = {'vox_um': 0.15, 'bridge_um': 0.48, 'fibre_stamp': 'segment',
               'sdcp_stamp': 'sphere', 'sdcp_sphere_d_um': 0.30, 'ptfe_stamp': 'centerline',
               'arms': 8, 'expect_backend': 'gpu', 'code_sha': 'deadbeef', 'origins': []}
    _d_before = receipt_digest(_rc_fix)
    _saved_nd = globals()['RECEIPT_AXES_NODIGEST']
    try:
        globals()['RECEIPT_AXES_NODIGEST'] = _saved_nd + ('zz_new_nodigest_axis',)
        chk(receipt_digest(_rc_fix) == _d_before,
            'RCPT-nodigest ★★ `RECEIPT_AXES_NODIGEST` 에 축을 더해도 digest 는 **안 움직인다** '
            '— 이것이 그 목록의 존재 이유다 (움직이면 커밋된 코호트 디렉터리 이름이 어긋난다)')
    finally:
        globals()['RECEIPT_AXES_NODIGEST'] = _saved_nd
    _saved_ax = globals()['RECEIPT_AXES']
    try:
        globals()['RECEIPT_AXES'] = _saved_ax + ('zz_new_hashed_axis',)
        chk(receipt_digest(_rc_fix) != _d_before,
            'RCPT-axes ★★ 반대로 `RECEIPT_AXES` 에 더하면 digest 가 **반드시 움직인다** — '
            '없는 키도 `rec.get(k)=None` 으로 해시 본문에 들어가기 때문이다.  ⇒ digest 는 '
            '런타임 캐시 키이지 내용 해시가 아니고, **옛 영수증의 digest 는 재계산으로 '
            '재현되지 않는 것이 정상**이다 (오염이 아니다)')
    finally:
        globals()['RECEIPT_AXES'] = _saved_ax
    chk(len(set(RECEIPT_AXES) & set(RECEIPT_AXES_NODIGEST)) == 0,
        'RCPT-disjoint ★ 두 목록이 겹치지 않는다 (겹치면 NODIGEST 의 약속이 거짓이 된다)')

    #  ── ① 계면 저항 요청 ↔ 적용 영수증 (2026-10-03 · Codex r_int 1단계 RINT-02 · 13 · 14) ──────────
    #  반례를 먼저 옮긴 것: 배선 삭제 (영수증 not_requested / missing) · 요청 밖 적용 · model None 생략 ·
    #  표 · 단위 · 모델 · 면 수 위조 · 계획과 어긋난 disabled.  정상 증인: 항 없음 · 전자 ON · 이온 실패.
    import sys as _sys_if
    import os as _os_if
    _here_if = _os_if.path.dirname(_os_if.path.abspath(__file__))
    if _here_if not in _sys_if.path:
        _sys_if.path.insert(0, _here_if)
    try:
        from step3_sigma import INTERFACE_MODEL_VERSION as _MVif
    except Exception:                                            # noqa: BLE001
        _MVif = None
    chk(_MVif is not None, 'IF-0 step3_sigma 의 INTERFACE_MODEL_VERSION 을 읽는다 (계약의 정본 출처)')
    _te_if = {'AM_S|AM_S': 0.001, 'AM_S|VGCF': 0.002}
    _ti_if = {'SDCP|SE': 0.001}

    def _rec_if(tb, n_by_pair, solved=True, pid=True):
        return {'model': _MVif, 'unit': 'ohm_cm2', 'table': dict(tb), 'pid_used': pid,
                'n_faces_rint': int(sum(n_by_pair.values())), 'faces_by_pair': dict(n_by_pair), 'solved': solved}
    _res_e = {'interface': _rec_if(_te_if, {'AM_S|AM_S': 30, 'AM_S|VGCF': 4})}
    _res_fail = {'reason': 'no_plate_contact(bot=0,top=3)', 'interface': _rec_if(_ti_if, {}, solved=False)}
    _res_nofaces = {'interface': _rec_if(_ti_if, {})}
    _plan_full = {'electronic': True, 'ionic': True, 'thermal': False, 'pore': False, 'collector': True}

    def _man_if(e=_te_if, i=None, receipts=None, model='auto', plan=None):
        m = {'interface_rint_e_ohm_cm2': e, 'interface_rint_i_ohm_cm2': i,
             'interface_model': (_MVif if (e or i) else None) if model == 'auto' else model,
             'component_plan': dict(plan or _plan_full)}
        if receipts is not None:
            m['interface_receipts'] = receipts
        return m
    _rc_e = {'electronic_main': interface_receipt(_res_e, _te_if),
             'electronic_wetted': interface_receipt(_res_e, _te_if),
             'electronic_bare': interface_receipt(_res_e, _te_if),
             'ionic': interface_receipt({'interface': None}, None)}
    chk([r['status'] for r in _rc_e.values()] == ['applied', 'applied', 'applied', 'not_requested'],
        'IF-1 영수증 생산자: 면 > 0 = applied · 요청 없는 채널 = not_requested')
    chk(interface_record_ok(_man_if(receipts=_rc_e)) == (True, None), 'IF-2 정상 증인 (전자 ON · 네 영수증)')
    chk(interface_record_ok({'interface_model': None, 'interface_rint_e_ohm_cm2': None,
                             'interface_rint_i_ohm_cm2': None}) == (True, None)
        and interface_record_ok({}) == (True, None), 'IF-3 항 없음 · 옛 세대 (키 없음) = 통과')
    _rc_off = {k: {'status': 'not_requested'} for k in INTERFACE_SOLVES}
    chk(interface_record_ok(_man_if(e=None, receipts=_rc_off)) == (True, None),
        'IF-3b 항 없음 + 영수증 전부 not_requested = 통과')
    #  배선 삭제 — 솔브 결과에 계면 기록이 없다 → 생산자가 missing 을 쓰고 계약이 거부
    _miss = interface_receipt({'sigma_eff': 1.0}, _te_if)
    chk(_miss['status'] == 'missing', 'IF-4 생산자: 요청이 있는데 솔브 기록 없음 → missing (not_requested 로 둔갑 금지)')
    for _nm in INTERFACE_SOLVES:
        if _nm == 'ionic':
            continue
        _r = dict(_rc_e); _r[_nm] = _miss
        _o, _w = interface_record_ok(_man_if(receipts=_r))
        chk(not _o and 'missing' in (_w or '') and _nm in (_w or ''), f'IF-5 {_nm} 배선 삭제 (missing) → 거부')
        _r2 = dict(_rc_e); _r2[_nm] = {'status': 'not_requested'}
        _o2, _w2 = interface_record_ok(_man_if(receipts=_r2))
        chk(not _o2 and 'dropped' in (_w2 or ''), f'IF-6 {_nm} 요청 있는데 not_requested → 거부')
    _o, _w = interface_record_ok(_man_if(receipts=_rc_e, model=None))
    chk(not _o and 'model|absent' in (_w or ''), 'IF-7 표는 있는데 model None → 거부 ("model 없으면 검사 생략" 금지)')
    _o, _w = interface_record_ok(_man_if(e=None, receipts=_rc_off, model=_MVif))
    chk(not _o and 'orphan' in (_w or ''), 'IF-8 요청 없는데 model 만 있음 → 거부')
    _o, _w = interface_record_ok(_man_if(e=None, receipts={**_rc_off, 'electronic_main': interface_receipt(_res_e, None)}))
    chk(not _o and 'unrequested' in (_w or ''), 'IF-9 요청 없는 표가 적용됨 (applied_without_request) → 거부')
    _o, _w = interface_record_ok(_man_if(receipts=None))
    chk(not _o and 'receipts|absent' in (_w or ''), 'IF-10 요청이 있는데 영수증 통째로 없음 → 거부')
    _bad_tab = dict(_rc_e); _bad_tab['electronic_bare'] = dict(_rc_e['electronic_bare'], table={'AM_S|AM_S': 0.001})
    _o, _w = interface_record_ok(_man_if(receipts=_bad_tab))
    chk(not _o and '|table|' in (_w or ''), 'IF-11 솔브가 받은 표 ≠ 요청 → 거부')
    for _lbl, _patch in (('unit', {'unit': 'ohm'}), ('model', {'model': 'r0'}),
                         ('면 수 합 모순', {'n_faces_rint': 0}), ('표 밖 쌍 면', {'faces_by_pair': {'AM_S|SE': 34}}),
                         ('pid_used 비 bool', {'pid_used': 1}), ('pid 없이 같은 상 쌍', {'pid_used': False}),
                         ('solved False 인데 applied', {'solved': False})):
        _r = dict(_rc_e); _r['electronic_main'] = dict(_rc_e['electronic_main'], **_patch)
        _o, _w = interface_record_ok(_man_if(receipts=_r))
        chk(not _o, f'IF-12 주 영수증 {_lbl} → 거부', )
    #  disabled 는 계획이 그 솔브를 끈 경우에만
    _dis = interface_receipt(None, _te_if, disabled_why='--no-collector')
    _r = dict(_rc_e); _r['electronic_wetted'] = _dis; _r['electronic_bare'] = _dis
    chk(interface_record_ok(_man_if(receipts=_r, plan=dict(_plan_full, collector=False))) == (True, None),
        'IF-13 --no-collector (계획 collector False) + wetted/bare disabled = 통과')
    _o, _w = interface_record_ok(_man_if(receipts=_r))
    chk(not _o and 'disabled' in (_w or ''), 'IF-14 계획은 collector True 인데 disabled → 거부')
    _r = dict(_rc_e); _r['electronic_main'] = _dis
    _o, _w = interface_record_ok(_man_if(receipts=_r))
    chk(not _o and 'disabled' in (_w or ''), 'IF-15 주 전자 솔브는 disabled 불가')
    #  이온: 실패한 솔브도 표를 받았는지 안다 (조기 반환 기록) · 면 0 = absent_geometry
    _rc_i = dict(_rc_e); _rc_i['ionic'] = interface_receipt(_res_fail, _ti_if)
    chk(_rc_i['ionic']['status'] == 'failed' and interface_record_ok(_man_if(i=_ti_if, receipts=_rc_i)) == (True, None),
        'IF-16 이온 솔브 실패 (사유) + 표 수신 = failed · 통과')
    _rc_i2 = dict(_rc_e); _rc_i2['ionic'] = interface_receipt(_res_nofaces, _ti_if)
    chk(_rc_i2['ionic']['status'] == 'absent_geometry'
        and interface_record_ok(_man_if(i=_ti_if, receipts=_rc_i2)) == (True, None),
        'IF-17 이온 표의 쌍이 격자에 없음 = absent_geometry · 통과')
    _rc_i3 = dict(_rc_e); _rc_i3['ionic'] = interface_receipt({'reason': 'no_plate_contact'}, _ti_if)
    chk(_rc_i3['ionic']['status'] == 'missing' and not interface_record_ok(_man_if(i=_ti_if, receipts=_rc_i3))[0],
        'IF-18 실패한 솔브인데 계면 기록도 없음 (배선 삭제) = missing → 거부')
    _zt = {'AM_S|VGCF': 0.0}
    _rc_z = {'electronic_main': interface_receipt({'interface': _rec_if(_zt, {})}, _zt),
             'electronic_wetted': interface_receipt({'interface': _rec_if(_zt, {})}, _zt),
             'electronic_bare': interface_receipt({'interface': _rec_if(_zt, {})}, _zt),
             'ionic': {'status': 'not_requested'}}
    chk(_rc_z['electronic_main']['status'] == 'zero_table' and interface_record_ok(_man_if(e=_zt, receipts=_rc_z)) == (True, None),
        'IF-19 명시 r = 0 표 = zero_table (absent 와 구분) · 통과')
    for _lbl, _tb in (('같은 상 비-AM', {'VGCF|VGCF': 1e-3}), ('모르는 상', {'AM_X|VGCF': 1e-3}),
                      ('역순 키', {'VGCF|AM_S': 1e-3}), ('bool 값', {'AM_S|VGCF': True}), ('음수', {'AM_S|VGCF': -1.0})):
        _o, _w = interface_record_ok(_man_if(e=_tb, receipts=None))
        chk(not _o and '|table|' in (_w or ''), f'IF-20 요청 표 모양 {_lbl} → 거부')
    _o, _w = interface_record_ok(_man_if(receipts={k: v for k, v in _rc_e.items() if k != 'ionic'}))
    chk(not _o and 'keys' in (_w or ''), 'IF-21 영수증 키 누락 → 거부')
    _o, _w = interface_record_ok(_man_if(receipts=dict(_rc_e, electronic_main={'status': 'mystery'})))
    chk(not _o and 'status' in (_w or ''), 'IF-22 모르는 상태 → 거부')

    print(f'\nrun_contract selftest: {ok}/{ok + fail} PASS'
          + ('' if not fail else '   ✗ 실패 있음'))
    return 0 if not fail else 1


if __name__ == '__main__':
    import sys
    sys.exit(_selftest() if '--selftest' in sys.argv else
             print('사용: python3 scripts/run_contract.py --selftest') or 0)
