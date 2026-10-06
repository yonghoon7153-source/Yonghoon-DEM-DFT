#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 분석 파이프라인의 **단계 계약 · provenance · 프로세스간 lock**.

`docs/codex_dem_webapp_code_review_20260807.md` Phase B (F-02 / F-03 / F-05) 대응.
app.py 의 라우트에서 분리해 **한 곳에서만** 정의한다 (리뷰 F-17: 같은 순서를 네 곳이
각자 구현해 drift 가 이미 발생했다).

═══ F-02: baseline 과 Stage E 의 계산 세대가 섞이던 문제 ════════════════════════
옛 흐름은 이랬다:
  ① network 산출물 백업 → ② results/ 통째로 삭제 → ③ run_pipeline() 이 network 를
  **다시 풀고** 그 새 결과로 **Stage E 를 만든다** → ④ 옛 network 파일을 그 위에 복원
  → ⑤ 옛 baseline 키를 full_metrics 에 머지하고 "network SKIPPED" 를 찍고 return.
결과: `full_metrics.json` 안에서 **baseline σ = 옛 network**, **Stage E = 방금 새로 푼
network 기준**.  수치가 우연히 같으면 숨지만 solver 를 고친 뒤 재분석하면 provenance 가
깨진다.  게다가 "생략" 이라면서 실제로는 매번 solver 를 돌려 OOM 위험도 그대로였다.

여기서 고정하는 계약:
  • preserve 경로 → **network subprocess 호출 0회**.
  • 보존 산출물을 **Stage E 보다 먼저** 복원한다 → Stage E 는 항상 화면에 실제로 남는
    baseline 을 보고 계산한다.
  • network 산출물에는 `network_provenance.json` 으로 run_id 를 새기고, Stage E 직후
    `stage_e_parent_network_run_id` 를 full_metrics 에 새겨 **둘의 일치를 검증**한다.

═══ F-05: parse 이후 실패가 전부 성공으로 보고되던 문제 ═════════════════════════
옛 run_pipeline 은 parse 만 검사하고 나머지는 rc 를 로그에 넣은 뒤 무조건 success 를
반환했다.  여기서는 단계마다 `required` 와 `expects` (기대 산출물)를 선언하고,
필수 단계가 nonzero 이거나 기대 산출물이 없으면 **failed**, 선택 단계만 실패하면
**partial** 로 내린다.  `done` 은 필수 단계가 전부 성공했을 때만이다.

═══ F-03: OOM 방지 lock 이 프로세스 로컬이던 문제 ═══════════════════════════════
`threading.Semaphore(1)` 은 module-global 이라 Gunicorn workers=2 에서 서로를 모른다.
게다가 정상 경로의 solver 호출은 애초에 그 lock 밖이었다 (force 여부와 무관하게
run_pipeline 안에서 돌고, wrapper 의 lock 블록은 solver 가 파일을 못 썼을 때만 도달하는
사실상 죽은 코드였다).  여기서는 **파일 lock** 으로 바꿔 worker 를 가로질러 직렬화한다.
⚠ 이것은 한 호스트 안에서만 유효하다 — 다중 호스트로 가면 Redis/DB lease 가 필요하다.
"""
from __future__ import annotations

import contextlib
import errno
import glob
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

#: network solver 가 만드는 산출물 일체 (하나라도 빠지면 Physics 컬럼이 사라진다).
NETWORK_ARTIFACT_GLOBS = (
    'network_conductivity.json',
    'network_conductivity_dual.json',
    'network_conductivity_hertzian.json',
    'network_conductivity_physics.json',
    # ★ RC4-03 (Codex 4회차): 'network_summary.csv' 는 여기 **있으면 안 된다** —
    #   그 파일은 network solver 가 아니라 **analyze_contacts.py 가** 쓴다
    #   (analyze_contacts.py:295, 무조건 실행되는 경로).  glob 에 들어 있으면
    #     ① stash 경로: contact 가 쓴 새 summary 를 치웠다가 solver 가 안 만드니
    #        성공 시 drop_stash 로 **지워버린다** (내가 stash 를 넣으며 만든 실데이터 손상)
    #     ② preserve 경로: snapshot 의 **옛** summary 가 새 contact summary 를 덮는다
    #   → contact 단계의 필수 산출물로 옮겼다.
    'network_raw_*',
    'network_provenance.json',
)

#: ★ 보존이 **의미를 가지려면 반드시 있어야 하는** baseline 산출물 (CB-02).
#:   옛 구현은 NETWORK_ARTIFACT_GLOBS 중 **하나라도** 있으면 스냅샷을 만들었는데,
#:   force 경로가 solver 실패에도 도장(`network_provenance.json`)을 남기므로
#:   **실패 도장 하나만으로 스냅샷이 생겨** 다음 기본 재분석이 preserve 를 골랐다.
#:   → solver 0회 + baseline 없음 + status='done' 으로 **영구 false-done**.
#:   (Codex 교차검증 CB-02 에서 동적 재현됨.)
NETWORK_BASELINE_REQUIRED = 'network_conductivity.json'

#: ★ RC6-Q7: merge 키 정의를 **여기 한 곳**에 둔다.  app.py 와 preflight 스캐너가 각자
#:   목록을 들고 있으면 스캔 결과가 production 과 어긋나 오히려 오도한다 (오늘 fixture-drift
#:   를 여섯 번 겪었다 — 같은 실수를 정의 수준에서 막는다).
NET_MERGE_KEYS = (
    'sigma_full', 'sigma_full_mScm', 'sigma_bulk_net',
    'sigma_bulk_net_mScm', 'R_brug_over_full', 'bulk_resistance_fraction',
    'electronic_sigma_full_mScm', 'electronic_R_brug',
    'electronic_active_fraction', 'electronic_percolating_fraction',
    'thermal_sigma_full_mScm', 'thermal_R_brug',
    'sigma_bruggeman', 'sigma_bruggeman_mScm', 'R_bruggeman_over_full',
    # Physics-mode baselines — Stage E Physics 컬럼에 필요.
    'sigma_full_physics', 'sigma_full_mScm_physics',
    'sigma_bulk_net_physics', 'sigma_bulk_net_mScm_physics',
    'electronic_sigma_full_mScm_physics',
    'thermal_sigma_full_mScm_physics',
    'bulk_resistance_fraction_physics',
    'R_brug_over_full_physics',
    #  ★ 10-04 ④a (J20-s · LHS-30) — 협착 저항 전력 몫 Σ I²R_c / Σ I²R_total (같은 FULL 해 · 관통 간선).  키에 채널 · 모드 꼬리.
    #    hertz = legacy JSON (network_conductivity.json = hertzian 결과) 에서 · physics = dual 에서 **이름 그대로** (NET_PHYSICS_TAILED_KEYS).
    #    여기 둔 것은 세대마다 먼저 걷어내기 위해서다 (옛 세대 값이 새 도장 밑에 남지 않게 — RC5-03).
    'constriction_power_share_ion_hertz', 'constriction_power_share_ion_hertz_status',
    'constriction_power_share_el_hertz', 'constriction_power_share_el_hertz_status',
    'constriction_power_share_th_hertz', 'constriction_power_share_th_hertz_status',
    'constriction_power_share_ion_physics', 'constriction_power_share_ion_physics_status',
    'constriction_power_share_el_physics', 'constriction_power_share_el_physics_status',
    'constriction_power_share_th_physics', 'constriction_power_share_th_physics_status',
    #  ★ 10-05 RGL-02 — 생산자의 이온 σ 상태 · 사유 (증명된 비관통 = valid_zero + no_through_path · 관통인데 못 풂 = not_computed +
    #    solve_failed).  hertz = legacy · physics = dual 미러 (`<key>_physics`).  세대마다 σ 와 함께 걷어내고 다시 채운다.
    'sigma_full_status', 'sigma_full_reason', 'sigma_full_status_physics', 'sigma_full_reason_physics',
    #  ★ 10-05 RGL-07 — 망 σ 와 **짝**인 σ₀ · 온도 (생산자가 모드마다 쓴다 · `NET_SIGMA0_KEYS`).  옛 목록은 이 둘을 소유하지 않아 새 σ 를
    #    머지해도 옛 온도 factor 가 남았고, 공용 τ 도우미 (`tau_flux.tau2_from_metrics` · `se_material.sigma_grain_context`) 가 옛 σ₀ 와
    #    새 σ 를 짝지었다 (재시도에서 τ 2×).  ⇒ σ 키와 **한 소유 단위**로 지우고 채운다 · 두 모드 짝은 `network_sigma0_problem` 이 대조한다.
    'temperature_provenance', 'sigma_grain_S_cm',
    #  ★ 10-06 (`L2-01` 세대 2 · 1저자 개정 — 계약 개정 노트) — Physics σ 의 ψ 배치 세대 표기 (multiply = 세대 2 · legacy_divide = 세대 1 ·
    #    없음 = 09-15 깃발 전 산출물).  dual physics 의 `psi_placement` 미러 (NET_PHYSICS_MIRROR_KEYS) 로 채우고 σ 와 한 소유 단위로 지운다 —
    #    옛 세대 표기가 새 σ 밑에 남거나 (그 반대로) 새 표기가 옛 σ 위에 붙지 않게 (RC5-03).
    'psi_placement_physics',
)

#: ★ 10-05 RGL-07 — 망 σ 와 짝인 σ₀ · 온도 기록 (모드마다 같은 값이어야 한다 — full_metrics 에는 한 벌만 싣는다).
NET_SIGMA0_KEYS = ('sigma_grain_S_cm', 'temperature_provenance')

#: ★ 10-04 ④a — dual 파일의 physics 결과에서 **이름 그대로** 옮기는 키 (이미 `_physics` 꼬리가 있다 → 아래 미러처럼
#:   `<key>_physics` 를 또 붙이지 않는다).  `_merge_dual_into_metrics` 와 스캐너 (`network_projection_preflight`) 가 같이 쓴다.
NET_PHYSICS_TAILED_KEYS = (
    'constriction_power_share_ion_physics', 'constriction_power_share_ion_physics_status',
    'constriction_power_share_el_physics', 'constriction_power_share_el_physics_status',
    'constriction_power_share_th_physics', 'constriction_power_share_th_physics_status',
)

#: ⚠ physics 키는 `network_conductivity_physics.json` 이 아니라 **dual 파일**에서
#:   `<key>_physics` 로 미러링된다 (`_merge_dual_into_metrics`).  스캐너도 같은 경로를 밟아야 한다.
NET_PHYSICS_MIRROR_KEYS = ('sigma_full', 'sigma_full_mScm',
                           'sigma_bulk_net', 'sigma_bulk_net_mScm',
                           'electronic_sigma_full_mScm', 'thermal_sigma_full_mScm',
                           'R_brug_over_full', 'bulk_resistance_fraction',
                           'sigma_full_status', 'sigma_full_reason',     # ★ 10-05 RGL-02 — 상태 · 사유도 physics 꼬리로
                           'psi_placement')                              # ★ 10-06 L2-01 — ψ 배치 세대 표기 → psi_placement_physics


def _canon(v):
    """대조용 정규 JSON — NaN 도 같은 토큰 ('NaN') 이라 NaN ≠ NaN 으로 거짓 불일치가 나지 않는다 · 키 순서 무관."""
    return json.dumps(v, sort_keys=True, default=str)


def network_sigma0_problem(dual, legacy=None, fm=None):
    """★ 10-05 RGL-07 — 망 σ 와 짝인 (σ₀, 온도) 기록의 정합 → '' (정합) | 사유.

      · dual 의 두 모드 기록이 같아야 한다 (full_metrics 에는 한 벌만 싣고 τ 도우미가 두 모드에 같은 σ₀ 를 쓴다)
      · legacy (= Hertz 사본 · full_metrics 머지 원천) 가 있으면 dual Hertz 와 같아야 한다
      · fm 이 있으면 (머지 뒤 투영) 그 기록이 이번 세대의 것이어야 한다 — 옛 세대 짝이 남으면 거부
    두 모드 모두 기록이 없으면 (옛 모양 산출물 · 시험 대역) 대조할 것이 없다 → '' (머지 쪽은 옛 값을 이미 걷어냈다)."""
    recs = {m: dual.get(m) for m in ('hertzian', 'physics')} if isinstance(dual, dict) else {}
    pairs = {m: tuple(r.get(k) for k in NET_SIGMA0_KEYS) for m, r in recs.items() if isinstance(r, dict)}
    if not pairs or all(all(v is None for v in p) for p in pairs.values()):
        return ''
    if len({_canon(p) for p in pairs.values()}) > 1 or any(v is None for p in pairs.values() for v in p):
        return 'σ₀ · 온도 짝: 두 모드 기록이 다르거나 일부가 없다 ' + '; '.join(
            f'{m}=(σ₀ {p[0]!r}, T {(p[1] or {}).get("T_C") if isinstance(p[1], dict) else p[1]!r})' for m, p in pairs.items())
    ref = pairs.get('hertzian') or next(iter(pairs.values()))
    if isinstance(legacy, dict) and _canon(tuple(legacy.get(k) for k in NET_SIGMA0_KEYS)) != _canon(ref):
        return 'σ₀ · 온도 짝: legacy (network_conductivity.json) 기록 ≠ dual Hertz'
    if isinstance(fm, dict) and _canon(tuple(fm.get(k) for k in NET_SIGMA0_KEYS)) != _canon(ref):
        return 'σ₀ · 온도 짝: full_metrics 의 기록이 이번 망 세대의 것이 아니다 (옛 세대 짝이 남았다 — RGL-07)'
    return ''

#: network 산출물의 세대를 식별하는 파일 (**게시된 active baseline** 을 가리킨다).
PROVENANCE_FILE = 'network_provenance.json'

#: 가장 최근 **시도** (성공/실패 모두).  active 와 분리한다 — RR2-01.
ATTEMPT_FILE = 'network_attempt.json'

_LOCK_NAME = 'dem_network_solver.lock'

#: ★ RC4-02 (Codex 4회차): Stage E 가 `full_metrics.json` 에 쓰는 **관리 대상 키 전부**.
#:   옛 격리는 이름에 `_stage_e` 가 들어간 키만 걷어내서, 아래 비격리 키들이 남아
#:   partial 실행(보정값 하나만 쓰고 끝)이 옛 metadata 와 섞인 채 성공이 됐다.
#:   실측 예: 25 ℃ 재실행 뒤에도 옛 60 ℃ `stage_e_temperature_provenance` 가 남았다.
#:
#:   ⚠ `thermal_sigma_full_mScm[_physics]` 는 **격리하지 않는다** — Stage E 가 치유하긴
#:     하지만 baseline network 산출물이기도 해서, 걷어내면 baseline 을 지우게 된다.
#:     (그 이중 소유 자체가 최종형 manifest 에서 정리해야 할 대상이다.)
#: Stage E 가 소유하지만 **이름 규칙(`_stage_e` / `stage_e_`)에 안 걸리는** 키들.
#:   ★ RC7-06 (Codex 7회차): `thermal_baseline_estimate_provenance` 가 여기 없어서
#:     Stage E purge/재실행 때 **값(…_stage_e_estimate)만 걷히고 provenance 는 남았다**
#:     → 새 세대의 payload 가 **없어진 추정치를 설명하는 옛 세대 provenance** 를 달고 있었다
#:     (값과 도장이 다른 세대를 가리키는 것 = 이 작업 전체가 막으려던 바로 그 상태).
#:   ⚠ 이 명시 목록은 **drift 자석**이다 — run_one 이 이름 규칙 밖의 키를 새로 쓰면 조용히
#:     같은 결함이 재발한다.  그래서 회귀가 run_network_full_corrections.py 의 `fm[...] =`
#:     대입을 전수 스캔해 소유되지 않은 키가 생기면 실패한다
#:     (test_pipeline_provenance RC7-06c).
STAGE_E_EXTRA_OWNED_KEYS = (
    'fracture_aware_method_full',
    'validation_flags',
    'thermal_baseline_estimate_provenance',
)


def is_stage_e_key(k: str) -> bool:
    return ('_stage_e' in k or k.startswith('stage_e_')
            or k in STAGE_E_EXTRA_OWNED_KEYS)


#: ★ RC5-01 (Codex 5회차): Stage E 성공 판정이 `any('_stage_e' in k)` 였다.  그래서
#:   `garbage_stage_e: null` **한 개**만 있어도 새 parent/run/code-SHA 가 success 로
#:   도장됐다 (Codex 동적 재현: garbage/null 둘 다 success, partial 실행이 안 닫힘).
#:
#:   → **exact schema** 로 바꾼다.  아래는 `run_network_full_corrections.run_one()` 이
#:   정상 종료마다 **무조건** 쓰는 최소 집합이다 (전부 함수 최상위 4칸 들여쓰기 =
#:   조건부 아님을 코드에서 확인).  loss 3필드·temperature provenance·thermal baseline
#:   heal 은 조건부라 여기 넣지 않는다.
#:
#:   ⚠ 이것은 **중간형**이다.  최종형은 Stage E 스크립트가 per-run manifest(schema
#:   version + 6-record 행렬 + digest)를 쓰고 앱이 그것을 검증하는 것 — 지금처럼 앱이
#:   키 목록을 추측하면 스크립트가 바뀔 때 drift 한다.  그 전까지는 이 집합을 정본으로
#:   두고, `run_one` 이 키를 늘리면 여기도 같이 늘린다.
STAGE_E_REQUIRED_KEYS = (
    'sigma_full_mScm_stage_e',
    'sigma_full_mScm_stage_e_physics',
    'electronic_sigma_full_mScm_stage_e',
    'electronic_sigma_full_mScm_stage_e_physics',
    'thermal_sigma_full_mScm_stage_e',
    'thermal_sigma_full_mScm_stage_e_physics',
    'stage_e_source',
    'stage_e_factors_used',
    'stage_e_fracture_stage_counts',
    'fracture_aware_method_full',
    'validation_flags',
)


#: 11-키 중 **유한한 수** 이어야 하는 여섯 (H/P × ionic/electronic/thermal).
STAGE_E_NUMERIC_KEYS = STAGE_E_REQUIRED_KEYS[:6]

#: **매핑(dict)** 이어야 하는 것들.  `stage_e_source='not-a-map'` 같은 손상을 잡는다.
STAGE_E_MAPPING_KEYS = ('stage_e_source', 'stage_e_factors_used',
                        'stage_e_fracture_stage_counts', 'validation_flags')

#: 비어 있지 않은 **문자열** 이어야 하는 것.
STAGE_E_STRING_KEYS = ('fracture_aware_method_full',)


def stage_e_missing_keys(full_metrics, null_ok_keys=()):
    """정상 Stage E 레코드의 **결손·손상** 목록 (빈 튜플이면 건전).

    ⚠ 값이 `None` 이면 **없는 것으로 본다** — 키 존재만 보면 partial 이 안 닫힌다.
      (진짜 0 은 `0.0` 이라 통과한다.)

    ★ RC6-01 (Codex 6회차): 옛 구현은 `is None` 만 봐서 **손상 레코드를 완전으로**
      판정했다.  Codex 재현 그대로:
          sigma_full_mScm_stage_e = NaN      → 통과했다
          stage_e_source = 'not-a-map'       → 통과했다
          validation_flags = []              → 통과했다
      → 타입·유한성까지 본다.  숫자 여섯은 **finite number**, 매핑 넷은 **dict**,
        method 는 **비어 있지 않은 문자열**.  (bool 은 int 의 서브클래스라 명시 배제 —
        `sigma=True` 가 숫자로 통과하면 안 된다.)

    ★ `null_ok_keys`: network 가 **정당하게** `valid_null/valid_zero` 를 낸 채널
      (열망 미퍼콜 등).  그 채널의 Stage E 값이 None 인 것은 **결손이 아니라 정합**이다.
      이것이 Codex 가 지적한 "network 는 valid_null 을 정상으로 보는데 Stage E 는 결손으로
      본다" 는 계약 충돌의 해소다 — 상류 상태를 알고 있을 때만 완화한다.
    """
    if not isinstance(full_metrics, dict):
        return STAGE_E_REQUIRED_KEYS
    bad, ok_null = [], set(null_ok_keys or ())
    for k in STAGE_E_REQUIRED_KEYS:
        v = full_metrics.get(k)
        if v is None:
            if k not in ok_null:
                bad.append(k)
            continue
        if k in STAGE_E_NUMERIC_KEYS:
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                bad.append(f'{k}:타입({type(v).__name__})')
            elif not math.isfinite(v):
                bad.append(f'{k}:비유한({v})')
        elif k in STAGE_E_MAPPING_KEYS:
            if not isinstance(v, dict):
                bad.append(f'{k}:매핑아님({type(v).__name__})')
        elif k in STAGE_E_STRING_KEYS:
            if not isinstance(v, str) or not v.strip():
                bad.append(f'{k}:빈문자열/타입')
    return tuple(bad)



def new_run_id() -> str:
    """세대 ID.  시간 접두사를 붙여 정렬하면 시간순이 된다."""
    return time.strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:8]


def code_sha(root=None) -> str:
    """현재 코드의 git SHA (없으면 'unknown').  결과가 어느 코드에서 나왔는지 고정용."""
    root = root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        out = subprocess.run(['git', '-C', root, 'rev-parse', 'HEAD'],
                             capture_output=True, text=True, timeout=10)
        return out.stdout.strip() if out.returncode == 0 else 'unknown'
    except Exception:
        return 'unknown'


def file_digest(path, chunk=1 << 20) -> str:
    """입력 파일 해시 — 같은 입력인지 판정용 (재현성 계약)."""
    h = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            while True:
                b = f.read(chunk)
                if not b:
                    break
                h.update(b)
        return h.hexdigest()[:16]
    except OSError:
        return ''


# ─────────────────────────────── 프로세스간 lock ───────────────────────────────

class LockUnavailable(RuntimeError):
    """network lock 을 못 잡았다 — solver 를 **실행하지 않는다** (CB-03)."""


class NetworkRecoveryFailed(RuntimeError):
    """★ 10-05 RGLR2-02 — 중단된 게시 흔적의 격리 (`quarantine_network_leftovers`) 가 실패했다 — solver 를 **실행하지 않는다** (흔적 그대로 · 읽는 쪽 무효)."""


@contextlib.contextmanager
def network_lock(timeout=None, lock_dir=None, require=True):
    """network solver 직렬화 — **프로세스를 가로질러** 동작하는 파일 lock.

    threading.Semaphore 는 Gunicorn workers=2 에서 서로를 모른다 (F-03).
    POSIX 는 fcntl.flock, Windows 는 msvcrt.locking 을 쓴다.

    ★ CB-03 (Codex 교차검증): 옛 구현은 lock 을 **못 잡아도 그냥 yield** 했고 호출부가
      그 값을 무시해 solver 를 그대로 돌렸다 = **fail-open**.  OOM 방지라는 목적 자체가
      무너진다.  이제 기본이 `require=True` 이고 **획득 실패 시 LockUnavailable 을
      던진다** — 호출부는 그것을 단계 실패로 기록하고 solver 를 실행하지 않는다.
      (Windows msvcrt 는 무기한 대기가 없으므로 non-blocking 재시도 + 실제 timeout.)
      `require=False` 는 진단·테스트 전용.
    """
    path = os.path.join(lock_dir or tempfile.gettempdir(), _LOCK_NAME)
    fh = open(path, 'a+b')
    acquired = False
    mode = None
    try:
        try:
            import fcntl
            mode = 'flock'
            if timeout is None:
                fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
                acquired = True
            else:
                deadline = time.time() + timeout
                while True:
                    try:
                        fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                        acquired = True
                        break
                    except OSError:
                        if time.time() >= deadline:
                            break
                        time.sleep(0.5)
        except ImportError:
            try:
                import msvcrt
                mode = 'msvcrt'
                deadline = time.time() + (timeout if timeout is not None else 3600.0)
                while True:
                    try:
                        msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)
                        acquired = True
                        break
                    except OSError:
                        if time.time() >= deadline:
                            break
                        time.sleep(0.5)
            except ImportError:
                mode = None
        if not acquired and require:
            raise LockUnavailable(
                f'network lock 미획득 (backend={mode or "없음"}, path={path}). '
                'solver 를 실행하지 않는다 — 동시 실행은 OOM 위험이다.')
        yield acquired
    finally:
        if acquired:
            try:
                import fcntl
                fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
            except ImportError:
                try:
                    import msvcrt
                    fh.seek(0)
                    msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 1)
                except Exception:
                    pass
        fh.close()


# ───────────────────────────── network 산출물 세대 ─────────────────────────────

def snapshot_network(results_dir, case_id=''):
    """보존할 **성공한** network 세대를 임시 디렉터리로 스냅샷.  없으면 None.

    results_dir 을 지우기 **전에** 호출한다.  복원은 Stage E **전에** 한다 —
    그래야 Stage E 가 실제로 남을 baseline 을 보고 계산한다 (F-02).

    ★ CB-02 (Codex 교차검증에서 동적 재현): 보존 자격을 **두 가지로 좁힌다**.
      ① baseline 파일(`network_conductivity.json`)이 실제로 있어야 한다.
      ② 도장이 있으면 `solver_status == 'success'` 여야 한다.
    옛 구현은 glob 중 하나만 맞아도 스냅샷을 만들었고, force 경로가 **실패에도 도장을
    남기므로** 실패 도장 하나로 스냅샷이 생겨 다음 기본 재분석이 preserve 를 골랐다
    → solver 0회 · baseline 없음 · status='done' 인 **영구 false-done**.
    (도장 이전 legacy 산출물은 ①만 만족하면 보존을 허용한다 — 그 시절엔 성공한
     산출물만 남았으므로.)
    """
    if not os.path.exists(os.path.join(results_dir, NETWORK_BASELINE_REQUIRED)):
        return None
    prov = read_network_provenance(results_dir)
    if prov.get('provenance_state') == 'invalid':
        return None                       # ★ RV-06: 검증 불가 → fail-closed (legacy 아님)
    if prov.get('network_run_id') and prov.get('solver_status') != 'success':
        return None                       # 실패한 세대는 보존하지 않는다 → solver 재실행
    if network_generation_problem(results_dir):
        return None                       # ★ 10-05 RGLR2-02 · Codex Q2 ③ — 확정되지 않은 세대 (full_metrics ↔ 도장 불일치 · 되돌림 실패 ·
        #                                   중단된 게시 흔적) 는 보존 (재사용) 하지 않는다 → solver 재실행 (사유는 호출부가 남긴다)
    items = []
    for pat in NETWORK_ARTIFACT_GLOBS:
        items += glob.glob(os.path.join(results_dir, pat))
    if not items:
        return None
    tmp = tempfile.mkdtemp(prefix=f'net_bk_{case_id}_')
    for src in items:
        dst = os.path.join(tmp, os.path.relpath(src, results_dir))
        os.makedirs(os.path.dirname(dst) or tmp, exist_ok=True)
        (shutil.copytree if os.path.isdir(src) else shutil.copy2)(src, dst)
    return tmp


def restore_network(snapshot_dir, results_dir):
    """스냅샷을 되돌린다.  → 복원한 항목 수."""
    if not snapshot_dir or not os.path.isdir(snapshot_dir):
        return 0
    os.makedirs(results_dir, exist_ok=True)
    n = 0
    for name in os.listdir(snapshot_dir):
        src, dst = os.path.join(snapshot_dir, name), os.path.join(results_dir, name)
        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        n += 1
    return n


def stamp_network_provenance(results_dir, run_id, inputs=None, solver_status='success',
                             argv=None):
    """network 산출물에 세대 도장을 찍는다.

    ★ CB-07 (Codex): 결과를 **실제로 바꾸는** 인자가 빠져 있었다 — `type_map`, `scale`,
      `contact_mode`.  code_sha 와 입력 digest 만으로는 같은 결과를 재현할 수 없다.
      argv 로 받아 함께 남긴다.
    ★ 10-06 (`L2-01` 세대 2 · 1저자 개정) — Physics σ 를 바꾸는 ψ 배치는 argv 가 아니라 **솔버 기본값**이 정한다 (CLI 깃발 없음) ⇒
      솔버가 이번 산출물에 실제로 남긴 값 (dual physics `psi_placement`) 을 `psi_placement_physics` 로 도장에 남긴다 (모듈 기본값을
      베끼지 않는다 · 기록 없음 = None — 09-15 깃발 전 산출물 · dual 없음 · 못 읽음).
    """
    prov = {'network_run_id': run_id, 'code_sha': code_sha(),
            'stamped_at': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'solver_status': solver_status,
            'solver': 'network_conductivity.py',
            'argv': dict(argv or {}),
            'units_contract': 'sim_to_real_v1',
            'input_digests': inputs or {},
            'psi_placement_physics': solver_psi_placement(results_dir)}
    atomic_write_json(os.path.join(results_dir, PROVENANCE_FILE), prov)
    return prov


def solver_psi_placement(results_dir, mode='physics'):
    """★ 10-06 (`L2-01` 세대 2) — 그 폴더 망 산출물의 ψ 배치 (솔버가 dual 의 그 모드 결과에 남긴 `psi_placement`) → 문자열 | None.
    None = 기록 없음 (09-15 깃발 전 산출물) · dual 없음 · 못 읽음 — 짐작하지 않는다."""
    d = _read_json_or_none(os.path.join(results_dir, 'network_conductivity_dual.json'))
    rec = d.get(mode) if isinstance(d, dict) else None
    v = rec.get('psi_placement') if isinstance(rec, dict) else None
    return v if isinstance(v, str) and v else None


def read_network_provenance(results_dir):
    """network 산출물의 세대.  도장이 없으면(옛 산출물) run_id=None."""
    path = os.path.join(results_dir, PROVENANCE_FILE)
    if not os.path.exists(path):
        return {'network_run_id': None, 'code_sha': None, 'solver_status': 'unknown',
                'provenance_state': 'missing',
                'note': 'pre-provenance artifact (도장 이전 세대)'}
    try:
        d = json.load(open(path))
        d.setdefault('provenance_state', 'valid')
        return d
    except (OSError, ValueError) as e:
        # ★ RV-06: 파일이 **있는데 못 읽는** 것은 '도장 이전' 이 아니라 **검증 불가**다.
        #   옛 코드는 둘을 같은 fallback 으로 돌려 손상 도장을 legacy 로 오인 → preserve.
        return {'network_run_id': None, 'code_sha': None, 'solver_status': 'unreadable',
                'provenance_state': 'invalid', 'note': f'provenance 손상: {e}'}


#: 단계 산출물을 치워두는 디렉터리 이름 앞머리.  results_dir **안**에 만든다 —
#:   같은 파일시스템이라 move 가 atomic rename 이 되고, 부모가 죽어도 케이스 옆에
#:   남아 복구할 수 있다 (/tmp 에 두면 copy+delete + 재부팅 시 소실).
STAGE_STASH_PREFIX = '.stage_stash_'
#: ★ 10-05 RGLR2-02 — **망** stash 의 앞머리 (`stash_network` 의 tag 'net_…').  남아 있으면 망 풀이 · 게시가 진행 중이거나 중단된 것이다 —
#:   자동 복구 (`recover_stale_stashes`) 로 되살리지 않고 읽는 쪽이 무효로 본다 (`tau_flux.NETWORK_STASH_PREFIX` 와 같은 값 · T23a).
NETWORK_STASH_PREFIX = STAGE_STASH_PREFIX + 'net_'
#: ★ 10-05 RGLR2-02 · Codex Q2 ③ — 중단된 게시의 흔적 (망 stash · full_metrics 사본) 을 다음 망 실행이 **격리**하는 곳 (복구 자료 보존 · 재사용 안 함).
#:   `.network_recovery/<run_id>/` + `recovery_note.json` (왜).  점 접두 — 어떤 산출물 glob · 흔적 검사에도 안 걸린다.
NETWORK_RECOVERY_DIR = '.network_recovery'


def stash_outputs(results_dir, patterns, tag=''):
    """지정 산출물을 **옆으로 치운다** → 단계가 빈 자리에 쓴다.  → stash dir | None

    ★ RR2-02 (Codex 2회차): `fresh=(mtime_ns, size)` 는 인과 증거가 아니다.
      metadata-only touch 만으로 통과하고(내용 불변인데 success), 반대로 결정론적 solver 가
      byte-identical 결과를 다시 써도 stale 로 **거부**한다(가용성 문제).
      해시도 단독으로는 안 된다 — 정상 재계산이 같은 해시를 내면 구별할 수 없다.

    그래서 판정을 stat/해시 비교가 아니라 **인과**로 바꾼다: 기존 산출물을 치우고 빈 자리에
    실행시키면, 실행 후 파일이 **존재한다는 사실 자체**가 "이번 실행이 만들었다" 는 증거다.
    실패하면 치워둔 것을 되돌려 **이전 성공 세대를 그대로 보존**한다.

    ★ RC7-03 (Codex 7회차): network 는 이 인과 판정을 쓰고 있었지만 **contact 네 경로는
      지문 비교(fresh)에 머물러 있었다** — 그 자리의 주석이 스스로 "최종형은 빈 candidate
      에서만 실행하는 것" 이라고 적어놓고 배선하지 않은 채였다.  그래서 network 전용이던
      stash 를 여기서 일반화해 contact 에도 같은 계약을 건다.
    """
    items = []
    for pat in patterns:
        items += glob.glob(os.path.join(results_dir, pat))
    if not items:
        return None
    st = tempfile.mkdtemp(prefix=f'{STAGE_STASH_PREFIX}{tag}_', dir=results_dir)
    for src in items:
        shutil.move(src, os.path.join(st, os.path.basename(src)))
    return st


def stash_network(results_dir, case_id=''):
    """기존 network 산출물을 옆으로 치운다 → solver 가 빈 자리에 쓴다.  → stash dir | None"""
    return stash_outputs(results_dir, NETWORK_ARTIFACT_GLOBS, tag=f'net_{case_id}')


def restore_stash(stash_dir, results_dir):
    """치워둔 산출물을 되돌린다 (실행 실패 시).  → 되돌린 개수."""
    if not stash_dir or not os.path.isdir(stash_dir):
        return 0
    n = 0
    for name in os.listdir(stash_dir):
        dst = os.path.join(results_dir, name)
        if os.path.exists(dst):
            (shutil.rmtree if os.path.isdir(dst) else os.remove)(dst)
        shutil.move(os.path.join(stash_dir, name), dst)
        n += 1
    shutil.rmtree(stash_dir, ignore_errors=True)
    return n


def drop_stash(stash_dir):
    """치워둔 것을 버린다 (실행 성공 시)."""
    if stash_dir:
        shutil.rmtree(stash_dir, ignore_errors=True)


def discard_network_candidate(results_dir, stash_dir):
    """★ 10-05 RGL-04 — 승격하지 않은 network 후보를 **치우고** 옛 세대를 되돌린다 → 되돌린 개수.

    `restore_stash` 는 이름이 겹치는 것만 덮어써서, **첫 실행** (stash 없음) 이면 후보의 네 JSON 이 그대로 남았다 — provenance 도장이
    없으니 `read_network_provenance` 가 '도장 이전 세대' 로 읽고 `snapshot_network` 의 보존 자격까지 생긴다 (실패 후보가 활성처럼).
    ⇒ 후보의 network 산출물 (`NETWORK_ARTIFACT_GLOBS`) 을 먼저 전부 걷어내고, stash (옛 네 JSON · 옛 provenance) 를 되돌린다.
    첫 실행이면 빈 자리 = 활성 세대 없음."""
    for pat in NETWORK_ARTIFACT_GLOBS:
        for p in glob.glob(os.path.join(results_dir, pat)):
            with contextlib.suppress(OSError):
                (shutil.rmtree if os.path.isdir(p) else os.remove)(p)
    return restore_stash(stash_dir, results_dir)


def recover_stale_stashes(results_dir, max_age_s=6 * 3600):
    """부모가 죽어 남은 stash 를 **복구**한다 → (복구한 파일 수, 치운 stash 수).

    ★ candidate(=사본) 와 달리 stash 는 **원본을 들고 있다** — 그래서 청소기가 지우면
      마지막 성공 세대가 사라진다.  그러므로 stash 는 지우는 게 아니라 복구한다:
        · results_dir 에 그 이름이 **없으면** → 이번 실행이 못 만든 것 → 되돌린다
        · 이미 **있으면** → 더 새 세대가 자리를 잡았다 → stash 쪽을 버린다
      (restore_stash 는 무조건 덮어쓰므로 크래시 복구에는 쓸 수 없다.)
    ★ 10-05 RGLR2-02 · Codex Q2 ③ — **망 stash (`NETWORK_STASH_PREFIX`) 는 건너뛴다.**  이름이 없을 때만 옛 파일을 되돌리는 규칙은 원자성 증명이
      아니다 — 중단된 망 게시 · 풀이 뒤에는 옛 네 JSON · 도장과 (일부 남은) 후보 · 새 full_metrics 가 섞여 **조용히 유효 세대로 재사용**된다.
      망 흔적은 그대로 두고 (복구 자료) 읽는 쪽이 무효 · 재실행 필요로 보며 (`network_generation_problem`), 다음 망 실행이 격리하고 왜를 남긴다
      (`quarantine_network_leftovers`).  접촉 등 다른 단계의 stash 는 옛 규칙 그대로.
    """
    restored = swept = 0
    try:
        names = os.listdir(results_dir)
    except OSError:
        return 0, 0
    for name in names:
        if not name.startswith(STAGE_STASH_PREFIX) or name.startswith(NETWORK_STASH_PREFIX):
            continue
        p = os.path.join(results_dir, name)
        try:
            if not os.path.isdir(p) or time.time() - os.path.getmtime(p) <= max_age_s:
                continue
            for fn in os.listdir(p):
                dst = os.path.join(results_dir, fn)
                if os.path.exists(dst):
                    continue                       # 더 새 세대가 있다 → stash 는 버린다
                shutil.move(os.path.join(p, fn), dst)
                restored += 1
            shutil.rmtree(p, ignore_errors=True)
            swept += 1
        except OSError:
            pass
    return restored, swept


#: Stage E 실패 시도 기록 — active 필드가 아니라 별도 파일 (RC5-02, network 와 같은 규약).
STAGE_E_ATTEMPT_FILE = 'stage_e_attempt.json'

#: ★ raw thermal 은 `is_stage_e_key()` 가 **일부러 제외**한다 — Stage E 가 baseline 으로
#:   읽기 때문에 실행 전에 걷어내면 입력을 지우게 된다.  그런데 Stage E 는 그 값을
#:   heal(덮어쓰기)하기도 해서, 실패했을 때 **되돌리지 않으면 network 산출물이 오염된 채
#:   남는다** (Codex RC5-02 실측: thermal 777 로 바뀐 것이 실패 후에도 남았다).
#:   ⇒ 격리는 안 하되 **snapshot/rollback 대상에는 넣는다**.
RAW_THERMAL_KEYS = ('thermal_sigma_full_mScm', 'thermal_sigma_full_mScm_physics')


#: thermal 채널 상태 → 이것이 **네트워크 단계 실패**인가.
#:   ★ RC5-03 근본수정: "값이 없다" 를 한 덩어리로 보면 안 된다.  열망이 퍼콜하지 않아
#:     κ 가 없는 것은 **물리적으로 옳은 답**이고, 솔버가 예외로 죽은 것은 **실패**다.
#:     옛 코드는 둘을 구분할 수 없어 (둘 다 "키 없음") 상위가 판단할 근거가 없었다.
#:     이제 solver 가 `thermal_status` 를 항상 남기므로 여기서 갈라 준다.
_THERMAL_OK_STATES = frozenset({'computed', 'valid_zero', 'valid_null'})
_THERMAL_FAIL_STATES = frozenset({'failed'})

#: network solver 의 세 채널.  ★ RC7-02 (Codex 7회차): 게시 게이트가 **thermal 하나만**
#:   검사했다 — electronic solver 는 예외를 잡아 print 만 하고 넘어가(RC5-03 이 thermal 에
#:   대해 고친 바로 그 결함이 electronic 에 그대로 남아 있었다) σ_e 키가 통째로 빠진 채
#:   provenance=success 로 게시됐다.  세 채널을 다 본다.
NETWORK_CHANNELS = ('ionic', 'electronic', 'thermal')

#: ★ '값이 없다' 의 의미는 **채널마다 다르다** — 한 집합으로 묶으면 안 된다.
#:   · electronic 의 no_result = AM 망 미퍼콜 = **물리적으로 옳은 답**
#:     (CLAUDE.md Tier2: σ_e=0 AM-no-perc 1mAh_100_4·1mAh_8_S1~S4 = "—" 가 정답)
#:   · ionic 의 no_result 도 마찬가지 (σ_i=0 SE-no-perc: 2mAh_real_16·8mAh_real_11)
#:   · thermal 은 **전 접촉**을 쓰므로 망이 안 서면 거의 언제나 의심스럽다 → OK 로 두지 않는다
#:     (기존 판정 유지 — 소급 변경 없음)
_CHANNEL_OK_STATES = {
    'ionic':      frozenset({'computed', 'valid_zero', 'valid_null', 'no_result'}),
    'electronic': frozenset({'computed', 'valid_zero', 'valid_null', 'no_result',
                             'not_applicable'}),
    'thermal':    _THERMAL_OK_STATES,
}
_CHANNEL_FAIL_STATES = frozenset({'failed'})


def channel_verdict(net_data, channel='thermal'):
    """→ ('ok'|'fail'|'unknown', reason).  network JSON 의 한 채널 판정.

    'unknown' = 옛 산출물(상태 필드가 없는 세대).  **실패로 취급하지 않는다** — 옛
    데이터를 소급해서 실패로 만들면 재분석 없이는 못 고치는 케이스가 무더기로 생긴다.
    대신 그 사실을 그대로 돌려주어 호출부가 라벨을 붙일 수 있게 한다.
    """
    if channel not in _CHANNEL_OK_STATES:
        raise ValueError(f'알 수 없는 채널: {channel}')
    if not isinstance(net_data, dict):
        return 'unknown', 'network 결과 없음'
    st = net_data.get(f'{channel}_status')
    if st is None:
        return 'unknown', f'옛 세대 산출물 ({channel}_status 이전)'
    if st in _CHANNEL_FAIL_STATES:
        return 'fail', net_data.get(f'{channel}_status_reason') or st
    if st in _CHANNEL_OK_STATES[channel]:
        return 'ok', net_data.get(f'{channel}_status_reason') or st
    return 'unknown', f'알 수 없는 상태: {st}'


def thermal_channel_verdict(net_data):
    """→ ('ok'|'fail'|'unknown', reason).  channel_verdict 의 thermal 별칭 (하위호환)."""
    return channel_verdict(net_data, 'thermal')


def network_content_verdict(results_dir, modes=('hertzian', 'physics'), strict=True):
    """새로 만든 network 산출물의 **내용**을 판정한다 → (ok, reason).

    ★ RC6-02 (Codex 6회차): 옛 게이트는 `run_stage` 의 **파일 존재**만 보고 stash 를
      버린 뒤 active 를 success 로 찍었고, thermal 판정은 **그 뒤에** 했다.  그래서
      required 단계가 실패했는데도 active provenance 는 success 이고 **옛 완전 세대는
      이미 버려진** 상태가 재현됐다 (실측: σ 999 게시 · stash 없음).
      → 내용 검증을 `run_stage(verify=…)` 로 **게이트 안**으로 옮긴다.  실패하면
        기존 `restore_stash` 경로가 그대로 옛 세대를 되살린다.

    ★ RC6-03: legacy(=hertzian 복사본) 하나만 보면 **Physics 실패가 H 성공에 가린다**.
      두 mode 파일을 각각 본다.

    strict=True (새로 만든 파일) 면 `unknown` 도 실패로 본다 — 방금 우리 solver 가
    만든 파일에 상태가 없다는 것은 schema 위반이다.  옛 세대를 읽을 때(preserve)는
    strict=False 로 두어 **소급 실패**를 만들지 않는다.

    ★ RC7-02 (Codex 7회차): 이 게이트는 **thermal 하나만** 봤다.  electronic solver 는
      예외를 잡아 print 만 하고 넘어가므로 (RC5-03 이 thermal 에 대해 고친 결함이 그대로
      남아 있었다) σ_e 키가 통째로 빠진 채 rc=0·파일 4개·thermal ok 로 **게시**됐다.
      → `NETWORK_CHANNELS` 셋을 전부 본다.  단 '값이 없다' 의 의미가 채널마다 달라
        OK 집합은 `_CHANNEL_OK_STATES` 로 채널별로 둔다 (AM/SE 미퍼콜은 정답이다).
    """
    bad, seen = [], []
    for mode in modes:
        p = os.path.join(results_dir, f'network_conductivity_{mode}.json')
        if not os.path.exists(p):
            bad.append(f'{mode}: 파일 없음')
            continue
        try:
            with open(p) as f:
                data = json.load(f)
        except (OSError, ValueError) as e:
            bad.append(f'{mode}: 읽기 실패 ({type(e).__name__})')
            continue
        seen.append(mode)
        for ch in NETWORK_CHANNELS:
            v, why = channel_verdict(data, ch)
            if v == 'fail' or (strict and v == 'unknown'):
                bad.append(f'{mode}.{ch}={v} ({why})')
    if not seen:
        bad.append('per-mode 산출물이 하나도 없다')
    return (not bad), ('; '.join(bad) if bad else 'ok: ' + ', '.join(seen))


#: ── `run_pipeline(stop_after='network')` 의 망 정지 계약 (Codex 요청서 §5-2 · 1저자 10-05 *"먼저 구현하고 같이 요청서로"*) ──
#:   τ 인계 (tau2 · f — `scripts/tau_flux.py`) 와 ④a 협착 전력 몫이 쓰는 망 산출물이 **이번 실행의 것으로 다 있는가**.
#:   (dual 의 모드 키, 모드 꼬리, full_metrics 의 σ 키) — σ 키 = `tau_flux.METRIC_SIGMA_KEY` 와 같은 원 솔버 σ (Stage-E 아님).
NETWORK_STOP_MODES = (('hertzian', 'hertz', 'sigma_full_mScm'), ('physics', 'physics', 'sigma_full_mScm_physics'))
#: 생산자 `network_conductivity._net_sigma_status` 의 값 중 계약이 받는 것 — `not_computed` (관통인데 풀지 못함 · 미실행) 는 거부한다
#:   (그 경우 이온 채널 판정은 옛 규약대로 `valid_null` 로 통과하므로 채널 판정만으로는 '비관통' 과 '못 풂' 을 못 가른다 — 상태로 가른다).
#:   ★ 10-05 RGL-02: valid_zero 는 생산자가 **증명된 비관통** (같은 그래프의 bottom ↔ top 관통 성분 0) 에만 사유 `no_through_path` 와 함께 낸다.
NETWORK_STOP_SIGMA_OK = ('computed', 'valid_zero')
#: 생산자 `network_conductivity.BOUNDARY_RULES` 와 같아야 한다 (L1 · L2 = 기록된 폴백 — 막지 않는다 · tau_flux G1 이 표지).
NETWORK_STOP_BOUNDARY_RULES = ('L0', 'L1', 'L2')
#: ★ 10-05 RGL-02 — 생산자가 비관통을 증명했을 때만 내는 사유 (`network_conductivity.NO_THROUGH_REASON` 과 같은 값).
NETWORK_NO_THROUGH_REASON = 'no_through_path'
#: ★ 10-05 RGL-08 — 협착 전력 몫 None 의 **등록된 물리 사유** → 그 사유가 맞는 σ 상태.  여기 없는 사유 (내부 예외 · 관통인데 FULL 풀이 실패
#:   · 빈 문자열 …) 는 거부한다 — 옛 계약 (요청서 §5-2④ "비지 않은 사유 상태면 통과") 은 기술적 결손과 과학적 null 을 못 갈랐다.
#:   비관통 = 0/0 미정의 (0 % 가 아니다 · Codex Q4) · 생산자 `network_conductivity.CPS_NO_THROUGH_STATUS`.
#:   ⚠ 생산자의 'not_computed (zero or non-finite dissipation)' 은 **등록하지 않는다** — 0 과 비유한 (수치 실패) 을 한 문자열에 묶었고,
#:     관통 σ > 0 인 FULL 해에서 Σ I²R_total = 0 은 나올 수 없으며 비관통이면 생산자는 위 비관통 문자열을 낸다 (두 받는 상태 어디에도 맞지 않는다).
#:     관통인데 FULL 풀이 실패 = `network_conductivity.CPS_SOLVE_FAILED_STATUS` (실패 · 거부).
NETWORK_POWER_NULL_REASONS = {'not_computed (no percolating FULL solution)': 'valid_zero'}
#: ★ 10-05 RGL-08 — 정지 계약이 받는 τ 인계 상태 (`tau_flux.STATUSES` 중 OK + 등록된 과학적 HOLD).  NOT_COMPUTED (입력 결손 · 솔버 관문 ·
#:   온도 짝 · 관통 불일치) 는 **기술적 결손**이라 거부한다 — network 완료 = τ 인계 입력이 다 있고 서로 맞다는 증서.
NETWORK_STOP_TAU_OK = ('OK', 'MODEL_BELOW_CONTINUUM_BOUND', 'BAND_FALLBACK', 'NOT_PERCOLATING')
#: τ 인계가 게이트에 쓰는 망 레코드 키 (`tau_flux.ion_columns` · `_sigma0`) — 두 모드 다 **키가** 있어야 한다 (값 None 은 상태가 정한다).
NETWORK_STOP_TAU_KEYS = ('sigma_full', 'percolating_fraction', 'boundary_rule', 'temperature_provenance', 'sigma_grain_S_cm')
#: τ 인계가 읽는 장부 (full_metrics — 접촉 분석이 쓴다): L_gap · L_mc · φ_mc (양수) · calc_percolation (≥ 0).
NETWORK_STOP_LEDGER_KEYS = ('thickness_um', 'thickness_mass_conserving_um', 'phi_se_mass_conserving', 'percolation_pct')


def _stop_num(v):
    """유한 실수 (bool · 문자열 · NaN · ±inf 아님)."""
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def _scripts_import(name):
    """scripts/ 모듈 지연 임포트 — pipeline_service 를 단독으로 불러도 (시험 · 스캐너) 정지 계약이 실 소비자 (tau_flux) 를 부른다."""
    import importlib
    sd = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')
    if sd not in sys.path:
        sys.path.insert(0, sd)
    return importlib.import_module(name)


def _read_json_or_none(path):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def network_stop_verdict(results_dir, run_id, fm=None):
    """`stop_after='network'` 로 멈춘 결과 폴더 → (ok, reason).  fail-closed — 읽기 실패 · 키 없음 · 모순은 전부 False.

    fm = 승격 **전** 후보의 full_metrics 투영 (10-05 RGL-04 — 아직 디스크에 쓰지 않은 것).  None 이면 디스크의 full_metrics.json.
    정본 (canonical) = **dual** (`network_conductivity_dual.json` — 두 모드를 한 파일에 · τ 인계 도우미가 읽는 것).  모드 파일 · legacy 는
    그 사본이어야 하고 full_metrics 는 그 투영이다 (값 일치는 복사 검산 · 세대 증거는 ② 도장 + stash 인과 계약이 진다).

      ① `network_content_verdict(strict=True)` — 네 JSON · 두 모드 · 세 채널
      ② full_metrics 의 `network_run_id` · `active_network_run_id` = 이번 실행 (`run_id`) · `network_solver_status` = success
      ③ ★ 10-05 RGLR-01 · 02 — 두 모드 dual 레코드의 **공용 기술 검사** (`tau_flux.ion_record_problem` — τ 인계 소비자와 같은 함수 · 띠 규칙과
         무관 · 과학적 HOLD 앞): computed = σ 두 표현 유한 양수 · 관통 분율 (0, 1] · 두 표현 항등식 (저장 정밀도 경계) · valid_zero = RGL-02 의
         증명된 비관통 조합 · not_computed · 그 밖 = 거부.  그 위에 이 계약만의 대조: full_metrics 상태 · 사유 = dual · computed 면 full_metrics σ = dual ·
         calc_percolation > 0 (관통 일치) · valid_zero 면 full_metrics σ None · 독립 calc_percolation 0
      ④ 두 모드 `constriction_power_share_ion_<꼬리>` (+ `_status`) — full_metrics = dual · computed σ 면 (0–1 · 'computed') ·
         valid_zero 면 (None · 등록된 물리 사유 `NETWORK_POWER_NULL_REASONS`) — 다른 사유 (내부 예외 · 풀이 실패) 는 거부 (RGL-08)
      ⑤ dual 두 모드 `boundary_rule` ∈ `NETWORK_STOP_BOUNDARY_RULES` · `boundary_band_frac` 유한 양수
      ⑥ 파일 대조 (RGL-08) — 모드 파일 두 개 · legacy 가 dual 의 그 모드와 같다 (전 레코드 · NaN 안전)
      ⑦ τ 인계 입력 (RGL-08) — 두 모드 `NETWORK_STOP_TAU_KEYS` 키 · 장부 `NETWORK_STOP_LEDGER_KEYS` 가 있고, **실 소비자**
         `tau_flux.ion_columns` 의 두 모드 상태가 `NETWORK_STOP_TAU_OK` (OK · 등록된 과학적 HOLD) 이며 생산자 상태와 맞는다
      ⑧ σ₀ · 온도 짝 (RGL-07) — 두 모드 · legacy · full_metrics 의 (σ₀, 온도) 가 이번 세대의 같은 값이고, 등급 · 웹앱 τ 가 쓰는 짝 σ₀
         (`tau_flux.tau2_from_metrics` = `se_material.sigma_grain_context(full_metrics)`) = 인계 σ₀ (망 기록)
    """
    ok_c, why_c = network_content_verdict(results_dir, strict=True)
    bad = [] if ok_c else [f'① {why_c}']
    try:
        tf = _scripts_import('tau_flux')                       # 공용 기술 검사 (③) · 실 소비자 (⑦) — 못 부르면 증서를 못 낸다 (fail-closed)
    except Exception as e:                                     # noqa: BLE001
        return False, '; '.join(bad + [f'τ 인계 도우미 (tau_flux) 를 못 불러왔다 ({type(e).__name__}: {e}) — 공용 기술 검사 불가'])
    try:
        if fm is None:
            with open(os.path.join(results_dir, 'full_metrics.json'), encoding='utf-8') as f:
                fm = json.load(f)
        with open(os.path.join(results_dir, 'network_conductivity_dual.json'), encoding='utf-8') as f:
            dual = json.load(f)
    except (OSError, ValueError) as e:
        return False, '; '.join(bad + [f'읽기 실패 ({type(e).__name__})'])
    if not isinstance(fm, dict) or not isinstance(dual, dict):
        return False, '; '.join(bad + ['full_metrics · dual 이 객체가 아니다'])
    if not run_id or fm.get('network_run_id') != run_id or fm.get('active_network_run_id') != run_id:
        bad.append(f'② 도장 network_run_id={fm.get("network_run_id")!r} · active={fm.get("active_network_run_id")!r} ≠ 이번 실행 {run_id!r}')
    if fm.get('network_solver_status') != 'success':
        bad.append(f'② network_solver_status={fm.get("network_solver_status")!r}')
    # ⑥ 파일 대조 — 정본 = dual
    files = {n: _read_json_or_none(os.path.join(results_dir, n))
             for n in ('network_conductivity_hertzian.json', 'network_conductivity_physics.json', 'network_conductivity.json')}
    for dkey, fname in (('hertzian', 'network_conductivity_hertzian.json'), ('physics', 'network_conductivity_physics.json'),
                        ('hertzian', 'network_conductivity.json')):
        if not isinstance(files[fname], dict) or not isinstance(dual.get(dkey), dict) or _canon(files[fname]) != _canon(dual[dkey]):
            bad.append(f'⑥ {fname} ≠ dual[{dkey}] (정본 = dual · 모드 파일 · legacy 는 그 사본이어야 한다)')
    #   ⑥b full_metrics 의 망 소유 키 (`NET_MERGE_KEYS` — σ · 상태 · 협착 몫 · σ₀ · 온도) = 이번 세대의 투영 (legacy · dual physics 미러 ·
    #       꼬리 키) — 옛 세대 값이 새 도장 밑에 남지 않았다 (RC5-03 · RGL-07 의 일반형 · 복사 검산이지 독립 세대 증명은 아니다)
    _leg = files['network_conductivity.json'] if isinstance(files['network_conductivity.json'], dict) else {}
    _rP = dual.get('physics') if isinstance(dual.get('physics'), dict) else {}
    _src = {k: _leg[k] for k in NET_MERGE_KEYS if _leg.get(k) is not None}
    _src.update({f'{k}_physics': _rP[k] for k in NET_PHYSICS_MIRROR_KEYS if _rP.get(k) is not None})
    _src.update({k: _rP[k] for k in NET_PHYSICS_TAILED_KEYS if _rP.get(k) is not None})
    _stale = [k for k in NET_MERGE_KEYS if _canon(fm.get(k)) != _canon(_src.get(k))]
    if _stale:
        bad.append(f'⑥ full_metrics 의 망 소유 키가 이번 세대 투영과 다르다 (옛 세대 값 · 복사 어긋남): {_stale[:8]}')
    # ⑦ 장부 (접촉 분석 — τ 인계의 L_gap · L_mc · φ_mc · calc_percolation)
    pct = fm.get('percolation_pct')
    led_bad = [k for k in NETWORK_STOP_LEDGER_KEYS
               if not (_stop_num(fm.get(k)) and (fm.get(k) >= 0 if k == 'percolation_pct' else fm.get(k) > 0))]
    if led_bad:
        bad.append(f'⑦ τ 인계 장부 (full_metrics) 없음 · 비유한 · 범위 밖: {led_bad}')
    for dkey, tail, fkey in NETWORK_STOP_MODES:
        rec = dual.get(dkey)
        if not isinstance(rec, dict):
            bad.append(f'{dkey}: dual 레코드 없음')
            continue
        miss = [k for k in NETWORK_STOP_TAU_KEYS if k not in rec]
        if miss:
            bad.append(f'⑦ {dkey}: τ 인계 입력 키 없음 {miss}')
        sfx = '' if tail == 'hertz' else '_physics'
        st, sv, fv = rec.get('sigma_full_status'), rec.get('sigma_full_mScm'), fm.get(fkey)
        rsn = rec.get('sigma_full_reason')
        #  ③ 공용 기술 검사 (RGLR-01 · 02) — 상태 ↔ 값 · 관통 분율 · 두 σ 표현 항등식 · 증명된 비관통 조합.  τ 인계 소비자와 **같은 함수**다
        #    (옛 판은 여기서 σ_dim 양수 · 관통 분율 > 0 만 보고 σ_ratio 는 소비자에 맡겼는데, 소비자는 L1/L2 에서 BAND_FALLBACK 로 먼저 돌아갔다).
        prob = tf.ion_record_problem(rec)
        if st not in NETWORK_STOP_SIGMA_OK or prob is not None:
            bad.append(f'③ {dkey}: 기술적 입력 무효 — {prob[0] if prob else "invalid_input"}: '
                       f'{prob[1] if prob else f"sigma_full_status={st!r} (사유 {rsn!r})"}')
        elif fm.get('sigma_full_status' + sfx) != st or fm.get('sigma_full_reason' + sfx) != rsn:
            bad.append(f'③ {dkey}: full_metrics 상태 ({fm.get("sigma_full_status" + sfx)!r}, {fm.get("sigma_full_reason" + sfx)!r}) '
                       f'≠ dual ({st!r}, {rsn!r})')
        elif st == 'computed':
            if not (_stop_num(fv) and fv == sv):
                bad.append(f'③ {dkey}: computed 인데 full_metrics {fkey}={fv!r} ≠ dual σ {sv!r} (같은 세대의 값이어야)')
            elif _stop_num(pct) and pct == 0:
                bad.append(f'③ {dkey}: 솔버는 관통인데 독립 calc_percolation 0 % (관통 불일치)')
        else:                                                  # valid_zero — 레코드 조합은 공용 검사가 봤다 · 여기는 full_metrics · 장부 대조
            if fv is not None:
                bad.append(f'③ {dkey}: valid_zero 인데 full_metrics {fkey}={fv!r} (None 이어야 — F-12)')
            if _stop_num(pct) and pct != 0:
                bad.append(f'③ {dkey}: valid_zero 인데 독립 calc_percolation {pct!r} % (0 이어야)')
        ck = f'constriction_power_share_ion_{tail}'
        cv, cs = fm.get(ck), fm.get(ck + '_status')
        if cv != rec.get(ck) or cs != rec.get(ck + '_status'):
            bad.append(f'④ {ck}: full_metrics ({cv!r}, {cs!r}) ≠ dual ({rec.get(ck)!r}, {rec.get(ck + "_status")!r})')
        elif st == 'computed' and not (_stop_num(cv) and 0.0 <= cv <= 1.0 and cs == 'computed'):
            bad.append(f'④ {ck}: 관통 해인데 값 {cv!r} · 상태 {cs!r} (0–1 · computed 여야 — 내부 예외 · 풀이 실패는 거부)')
        elif st == 'valid_zero' and not (cv is None and NETWORK_POWER_NULL_REASONS.get(cs) == 'valid_zero'):
            bad.append(f'④ {ck}: 비관통인데 값 {cv!r} · 사유 {cs!r} — 등록된 물리 사유 {sorted(NETWORK_POWER_NULL_REASONS)} 만 받는다')
        br, bf = rec.get('boundary_rule'), rec.get('boundary_band_frac')
        if br not in NETWORK_STOP_BOUNDARY_RULES or not (_stop_num(bf) and bf > 0):
            bad.append(f'⑤ {dkey}: boundary_rule={br!r} · boundary_band_frac={bf!r}')
    # ⑧ σ₀ · 온도 짝 (RGL-07)
    p0 = network_sigma0_problem(dual, files.get('network_conductivity.json'), fm)
    if p0:
        bad.append('⑧ ' + p0)
    # ⑦ τ 인계 — 실 소비자 (tau_flux) 가 이 후보로 무엇을 내는가 (계약 사본이 아니라 소비자 자신 · 공용 기술 검사를 다시 거친다)
    try:
        row = tf.ion_columns(dual, fm, pct)
        for dkey, tail, _f in NETWORK_STOP_MODES:
            s, r = row.get(f'ion_net_status_{tail}'), row.get(f'ion_net_status_reason_{tail}')
            pst = (dual.get(dkey) or {}).get('sigma_full_status')
            if s not in NETWORK_STOP_TAU_OK:
                bad.append(f'⑦ τ 인계 {tail}: {s} ({r}) — 기술적 결손 (등록된 과학적 HOLD 아님)')
            elif pst == 'valid_zero' and s not in ('NOT_PERCOLATING', 'BAND_FALLBACK'):
                bad.append(f'⑦ τ 인계 {tail}: 생산자 비관통인데 τ 상태 {s}')
            elif pst == 'computed' and s == 'NOT_PERCOLATING':
                bad.append(f'⑦ τ 인계 {tail}: 생산자 관통인데 τ 상태 NOT_PERCOLATING')
        s0_net = row.get('ion_sigma0_mScm')
        s0_fm = tf.tau2_from_metrics(fm)[1]
        if _stop_num(s0_net) and not (_stop_num(s0_fm) and abs(s0_fm - s0_net) <= 1e-9 * max(1.0, abs(s0_net))):
            bad.append(f'⑧ 짝 σ₀: 등급 · 웹앱 τ 가 쓰는 σ₀ {s0_fm!r} mS/cm (full_metrics) ≠ 인계 σ₀ {s0_net!r} (망 기록)')
    except Exception as e:                                     # noqa: BLE001 — 소비자를 못 부르면 증서를 못 낸다 (fail-closed)
        bad.append(f'⑦ τ 인계 도우미 실패 ({type(e).__name__}: {e})')
    return (not bad), ('; '.join(bad) if bad else 'ok')


#: ★ 10-05 RGLR2-01 (Codex 3차 재검증 §2 · Q1) — 일반 · 정지 경로 **공통**의 승격 전 기술 검사 단계 이름 (웹앱 단계 로그 · 최근 시도 stage).
NETWORK_RECORD_CHECK_STEP = 'Network ionic record check (승격 전 공용 기술 검사 · RGLR2-01)'
#: 검사하는 레코드 = 소비자가 읽는 사본 전부 — dual 두 모드 (τ 인계 · physics 투영) · legacy (full_metrics Hertz 투영) · 모드 파일 둘.
_RECORD_CHECK_SOURCES = (('network_conductivity_dual.json', 'hertzian'), ('network_conductivity_dual.json', 'physics'),
                         ('network_conductivity.json', None), ('network_conductivity_hertzian.json', None),
                         ('network_conductivity_physics.json', None))


def network_record_verdict(results_dir):
    """★ 10-05 RGLR2-01 — 후보 망 레코드의 **기술적 입력 유효성** (일반 · 정지 경로 공통 · 승격 전) → (ok, 사유).

    정지 계약 ③ · τ 인계 소비자와 **같은 함수** (`tau_flux.ion_record_problem`) 를 두 모드 · 소비자가 읽는 사본 전부에 부른다: computed = σ 두 표현
    유한 양수 · 관통 분율 (0, 1] · σ₀ · 두 표현 항등식 (저장 정밀도) / valid_zero = 증명된 비관통 조합 / not_computed · 그 밖 = 거부.
    ⚠ 정지 계약의 **과학적 HOLD 조건은 옮기지 않는다** — 띠 폴백 L1 · L2 · 정상 비관통 (valid_zero) · 연속체 하한 · 온도 변환 σ₀ 는 통과한다 (그 판정은
    τ 인계 소비자 · 정지 계약의 몫).  옛 판은 일반 경로 (Stage E 앞 승격) 가 이 검사를 건너뛰어 σ_ratio 만 ×4 · 띠 L1 의 σ_ratio None 이 done 으로
    게시됐다 (Codex general_ratio_times4 · general_band_ratio_missing).  읽기 실패 · 레코드 없음 · 도우미를 못 부름 = 거부 (fail-closed)."""
    try:
        tf = _scripts_import('tau_flux')
    except Exception as e:                                     # noqa: BLE001
        return False, f'τ 인계 도우미 (tau_flux) 를 못 불러왔다 ({type(e).__name__}: {e}) — 공용 기술 검사 불가'
    bad, files = [], {}
    for fname, mode in _RECORD_CHECK_SOURCES:
        if fname not in files:
            files[fname] = _read_json_or_none(os.path.join(results_dir, fname))
        doc = files[fname]
        rec = doc.get(mode) if (mode and isinstance(doc, dict)) else doc
        prob = tf.ion_record_problem(rec)
        if prob is not None:
            bad.append(f'{fname}{f"[{mode}]" if mode else ""}: {prob[0]}: {prob[1]}')
    return (not bad), ('; '.join(bad) if bad else 'ok')


#: ★ RC6-07 (Codex 6회차, Windows 실측): 자식 프로세스의 출력 인코딩을 계약하지 않으면
#:   **Windows 기본 CP949 에서 solver 가 첫 non-ASCII 로그에 죽는다**.
#:     UnicodeEncodeError: 'cp949' codec can't encode character '\u2014'
#:     network_conductivity.py:1092  →  rc=1, network JSON 0개
#:   같은 입력을 `PYTHONUTF8=1` 로 돌리면 rc=0 에 네 파일이 다 나온다.  우리 solver 는
#:   212 종의 non-ASCII (─ ★ ⚠ σ …) 를 21 곳에서 print 한다 — ASCII 로 줄이는 것은
#:   현실적이지 않으므로 **인코딩을 계약**한다.
#:   ⚠ 자식만 UTF-8 로 바꾸고 부모 decode 를 기본값(CP949)으로 두면 안 된다 — 양쪽을 함께.
def utf8_subprocess_kwargs(env=None):
    """subprocess 공통 인자 — 자식 stdio 를 UTF-8 로, 부모 decode 도 UTF-8 로 고정한다."""
    e = dict(env if env is not None else os.environ)
    e['PYTHONUTF8'] = '1'
    e['PYTHONIOENCODING'] = 'utf-8'
    return {'text': True, 'encoding': 'utf-8', 'errors': 'replace', 'env': e}


#: Stage E candidate 작업 디렉터리 접두어 (results 안에 두어 같은 파일시스템 = rename 원자성).
STAGE_E_CANDIDATE_PREFIX = '.stage_e_candidate_'


@contextlib.contextmanager
def stage_e_candidate(results_dir):
    """Stage E 를 **candidate 에서** 돌리고, 통과한 것만 active 로 원자 게시한다 (RC6-04b).

    ★ 왜 필요한가 (Codex 6회차, 실측 재현): 옛 흐름은 subprocess 전에 **active 위치의**
      `full_metrics.json` 에서 Stage E 키를 지워 게시했다.  그래서
        · 정상 실행 중에도 reader 가 Stage E 키가 없는 중간 상태를 본다
        · **부모가 purge 와 복원 사이에 죽으면 그 상태가 영구 active** 가 된다
        · child 실패 rollback 은 그 parent crash 를 복구하지 못한다
      (RR3-03 과 같은 뿌리.)

    새 흐름 — **active 를 끝까지 건드리지 않는다**:
        ① candidate 디렉터리를 만들고 active full_metrics 를 **복사**
        ② candidate 안에서만 Stage E 키를 걷어낸다 (active 는 그대로)
        ③ Stage E 를 `--case-dir <candidate>` 로 실행
        ④ 검증 통과 → candidate 를 active 로 **원자 rename**
           실패/예외/크래시 → active 는 처음부터 안 건드렸으므로 **그대로**

    사용:
        with stage_e_candidate(results_dir) as cand:
            run_stage(..., cmd + ['--case-dir', cand.dir], ...)
            if ok: cand.publish()          # 통과했을 때만
        # publish 안 하면 candidate 는 버려지고 active 는 옛 세대 그대로

    ⚠ candidate 는 `results_dir` **안에** 만든다 — `os.replace` 가 원자적이려면 같은
      파일시스템이어야 한다 (/tmp 는 다른 마운트일 수 있다).
    """
    cand_dir = tempfile.mkdtemp(prefix=STAGE_E_CANDIDATE_PREFIX, dir=results_dir)
    fm_src = os.path.join(results_dir, 'full_metrics.json')
    fm_cand = os.path.join(cand_dir, 'full_metrics.json')

    class _Cand:
        dir = cand_dir
        published = False

        def purge_stage_e(self):
            """candidate 안에서만 관리 키를 걷어낸다 → 걷어낸 것을 돌려준다."""
            try:
                with open(fm_cand) as f:
                    d = json.load(f)
            except (OSError, ValueError):
                return {}
            saved = {k: v for k, v in d.items() if is_stage_e_key(k)}
            for k in saved:
                d.pop(k, None)
            atomic_write_json(fm_cand, d)
            return saved

        def publish(self):
            """candidate 의 full_metrics 를 active 로 **원자적으로** 옮긴다."""
            _replace_retry(fm_cand, fm_src)
            self.published = True

    try:
        if os.path.exists(fm_src):
            shutil.copy2(fm_src, fm_cand)
        # candidate 에서도 Stage E 가 읽어야 하는 입력을 곁들인다 (읽기 전용 참조).
        for aux in ('network_conductivity.json', 'network_conductivity_hertzian.json',
                    'network_conductivity_physics.json', 'network_conductivity_dual.json',
                    'atoms.csv', 'contacts.csv', 'input_params.json', 'meta.json',
                    'mesh_info.json', 'contacts_analyzed.csv', 'atoms_analyzed.csv'):
            src = os.path.join(results_dir, aux)
            if os.path.exists(src):
                with contextlib.suppress(OSError):
                    os.symlink(os.path.abspath(src), os.path.join(cand_dir, aux))
        yield _Cand()
    finally:
        shutil.rmtree(cand_dir, ignore_errors=True)


def sweep_stale_candidates(results_dir, max_age_s=6 * 3600):
    """부모가 죽어 남은 candidate 를 치운다 → 치운 개수.

    ★ candidate 는 active 를 건드리지 않으므로 **남아 있어도 안전**하다 — 이 청소는
      디스크 위생일 뿐 정합성 문제가 아니다 (그것이 이 설계의 요점이다).
    """
    n = 0
    try:
        for name in os.listdir(results_dir):
            if not name.startswith(STAGE_E_CANDIDATE_PREFIX):
                continue
            p = os.path.join(results_dir, name)
            try:
                if time.time() - os.path.getmtime(p) > max_age_s:
                    shutil.rmtree(p, ignore_errors=True)
                    n += 1
            except OSError:
                pass
    except OSError:
        pass
    return n


def snapshot_keys(d, keys):
    """{key: {'present': bool, 'value': v}} — **없었다는 사실**까지 보존한다.

    단순히 값만 저장하면 "원래 없던 키" 를 복원할 때 `None` 으로 되살려 놓게 된다.
    없던 것은 없는 상태로 되돌려야 정확한 rollback 이다.
    """
    d = d if isinstance(d, dict) else {}
    return {k: ({'present': True, 'value': d[k]} if k in d else {'present': False})
            for k in keys}


def restore_keys(d, snap):
    """`snapshot_keys` 의 기록대로 정확히 되돌린다 (없었으면 삭제)."""
    for k, rec in (snap or {}).items():
        if rec.get('present'):
            d[k] = rec.get('value')
        else:
            d.pop(k, None)
    return d


def record_stage_e_attempt(results_dir, parent_run_id, reason='', restored=True):
    """Stage E **실패 시도**를 active 필드와 분리해 남긴다 (RC5-02).

    옛 코드는 `stage_e_status` / `stage_e_attempt_parent_network_run_id` 를 active
    full_metrics 에 썼다.  실패 시도의 흔적이 게시된 세대의 필드를 차지하는 것은
    network 쪽에서 이미 RR2-01 로 고친 것과 같은 문제다.
    """
    atomic_write_json(os.path.join(results_dir, STAGE_E_ATTEMPT_FILE), {
        'stage_e_attempt_parent_network_run_id': parent_run_id,
        'status': 'failed', 'reason': reason,
        'previous_generation_restored': bool(restored),
        'code_sha': code_sha(),
        'attempted_at': time.strftime('%Y-%m-%dT%H:%M:%S'),
    })


#: ★ 10-05 WEB-03 Q2 (Codex 재검증 Q2 · 1저자 비준) — **한 실패 어휘**: 활성 (마지막 유효) 세대 ↔ 최근 시도.
#:   활성 세대 = 네 망 JSON + `network_provenance.json` + full_metrics (승격했을 때만 바뀐다 · 실패 시도는 바이트 하나 건드리지 않는다).
#:   최근 시도 = `network_attempt.json` (성공 · 실패 모두) — 실패면 어느 종류 (`failure_kind`) · 어느 단계 · 왜 · 그 뒤에도 활성 세대가 무엇인가.
#:   옛 판은 솔버 rc 실패만 full_metrics 에 network_solver_status=failed 를 쓰고 (승격 전 검사 거부는 바이트 보존) 소비자가 실패 종류마다 다른 곳을
#:   봐야 했다.  소비자는 이 이름들 (`network_status_view`) 로 읽는다 — 추측하지 않는다.
ATTEMPT_SCHEMA = 'network_attempt/v2'
#: 실패 종류 — solver (lock 뒤 솔버 rc · 기대 산출물 · 내용 검증 = 채널 failed 포함) · lock (lock 미획득 = 솔버 미실행) ·
#:   candidate_rejected (승격 전 검사: 투영 · 채널 판정 · σ₀ 짝 · 망 정지 계약 · 공용 기술 검사 RGLR2-01) · publish_exception (승격 쓰기 중 동기
#:   예외 → 되돌림 · 검산 통과) · ★ 10-05 RGLR2-02: rollback_failed (그 되돌림 **자체**가 실패하거나 검산이 승격 전 디스크와 다르다 → 활성 무효 ·
#:   값 인용 금지 · 재실행 필요) · interrupted_publish (중단된 게시 흔적을 다음 실행이 격리 — 그 실행이 승격에 성공할 때까지 활성 무효).
NETWORK_FAILURE_KINDS = ('solver', 'lock', 'candidate_rejected', 'publish_exception', 'rollback_failed', 'interrupted_publish')


def network_generation_problem(results_dir, fm=None):
    """★ 10-05 RGLR2-02 (Codex 3차 재검증 §2 · Q2) — 그 폴더의 망 활성 세대가 **확정되었는가** (읽는 쪽 fail-closed) → '' | 사유.
    정본 = `tau_flux.network_generation_problem` (τ 인계 CLI 와 같은 함수 — 도장 손상 · 중단된 게시 흔적 · full_metrics ↔ 도장 불일치 ·
    활성을 무효로 남긴 최근 시도).  최근 시도 기록을 못 썼어도 디스크만 보고 가른다.  도우미를 못 부르면 확인 불가 = 무효."""
    try:
        tf = _scripts_import('tau_flux')
    except Exception as e:                                     # noqa: BLE001
        return f'세대 검사 도우미 (tau_flux) 를 못 불러왔다 ({type(e).__name__}) — 활성 세대를 확인할 수 없다'
    return tf.network_generation_problem(results_dir, fm=fm)


def _active_generation(results_dir):
    """지금 디스크의 활성 세대 → (run_id | None, 상태).  상태 = 도장의 solver_status ('success') · 도장 없는 옛 망 산출물 'legacy_unstamped' ·
    망 산출물 없음 'none' · 도장 손상 'invalid'."""
    prov = read_network_provenance(results_dir)
    if prov.get('provenance_state') == 'invalid':
        return None, 'invalid'
    rid = prov.get('network_run_id')
    if rid:
        return rid, prov.get('solver_status') or 'unknown'
    if os.path.exists(os.path.join(results_dir, NETWORK_BASELINE_REQUIRED)):
        return None, 'legacy_unstamped'
    return None, 'none'


def record_network_attempt(results_dir, run_id, status, reason='', argv=None, stage='', failure_kind='', inputs=None,
                           active_problem=''):
    """**실패 시도**를 active provenance 와 **분리해** 기록한다 (RR2-01).

    옛 코드는 실패에도 `network_provenance.json` 을 새 run_id 로 덮어써서, 실패 시도의 ID 가
    `full_metrics.network_run_id` 와 `stage_e_parent_network_run_id` 까지 차지했다 —
    게시된 baseline 은 옛 성공 세대인데 ID 는 실패 시도를 가리키는 모순.
    이제 active 도장은 **성공했을 때만** 갱신하고, 시도는 이 별도 파일에 남긴다.
    stage = 실패한 단계 이름 (10-05 RGL-04 — 솔버 · 채널 판정 · 망 정지 계약 · 승격 전 투영 중 어디서 막혔나 · 성공이면 '').
    ★ 10-05 WEB-03 Q2 — 스키마 v2 (옛 키 `network_attempt_run_id` · `solver_status` · `reason` · `stage` 는 그대로 — 옛 소비자 하위호환):
      latest_attempt_status (= solver_status) · failure_kind (`NETWORK_FAILURE_KINDS` · 성공이면 '') · input_digests (입력 id) ·
      active_network_run_id · active_status (**기록 시점** 활성 세대 — 승격이면 이번 실행 · 실패면 되돌린 옛 세대 · 없으면 None/'none') ·
      previous_generation_kept (실패 시도 뒤에도 옛 활성 세대가 그대로 활성인가 · 성공이면 None).
    호출자는 활성 세대를 확정한 **뒤** (승격 또는 되돌림 뒤) 부른다.
    ★ 10-05 RGLR2-02 (Codex 3차 재검증) — 실패 기록의 활성 판정을 도장 하나로 하지 않는다: active_problem (호출자가 아는 무효 사유 — 되돌림 실패 ·
      격리) 이 있거나 디스크가 확정되지 않은 세대면 (`network_generation_problem` — full_metrics ↔ 도장 불일치 · 중단된 게시 흔적 · 앞선 무효 기록)
      active_status = 'invalid' · previous_generation_kept = False · active_problem = 사유.  옛 판은 provenance 만 읽어, full_metrics 되돌림이
      실패해 새 세대가 남았는데도 kept=True · active success 라고 썼다 (Codex rollback_destination_failure).  성공 기록은 그대로 (방금 승격한 세대).
    """
    act_id, act_st = _active_generation(results_dir)
    failed = status != 'success'
    prob = ''
    if failed:
        prob = active_problem or network_generation_problem(results_dir)
        if prob:
            act_st = 'invalid'
    rec = {
        'schema': ATTEMPT_SCHEMA,
        'network_attempt_run_id': run_id, 'solver_status': status,
        'latest_attempt_status': status,
        'failure_kind': (failure_kind or 'solver') if failed else '',
        'reason': reason, 'stage': stage,
        'active_network_run_id': act_id, 'active_status': act_st,
        'previous_generation_kept': (act_st not in ('none', 'invalid') and act_id != run_id) if failed else None,
        'input_digests': dict(inputs or {}),
        'code_sha': code_sha(),
        'attempted_at': time.strftime('%Y-%m-%dT%H:%M:%S'), 'argv': dict(argv or {}),
    }
    if prob:
        rec['active_problem'] = str(prob)[:1000]
    atomic_write_json(os.path.join(results_dir, ATTEMPT_FILE), rec)


def read_network_attempt(results_dir):
    """가장 최근 network 시도 기록 (`ATTEMPT_FILE`) → dict | None (없음 · 손상).  표시용 (웹앱 망 세대 행 · RGL-04)."""
    try:
        with open(os.path.join(results_dir, ATTEMPT_FILE), encoding='utf-8') as f:
            d = json.load(f)
        return d if isinstance(d, dict) else None
    except (OSError, ValueError):
        return None


def network_status_view(results_dir):
    """★ 10-05 WEB-03 Q2 — 한 실패 어휘로 읽는다: 활성 (마지막 유효) 세대 ↔ 최근 시도.  소비자 (웹앱 케이스 페이지 · 목록) 는 이것만 보면 된다.

    → {'active_network_run_id', 'active_status' ('success' · 'none' · 'legacy_unstamped' · 'invalid' · …),
       'latest_attempt_run_id', 'latest_attempt_status' ('success' · 'failed' · None = 기록 없음), 'failure_kind', 'latest_attempt_stage',
       'latest_attempt_reason', 'stale' (최근 시도가 failed 인데 활성 세대가 있다 = 화면 값은 이전 성공 세대 — '최근 재계산 실패')}
    활성 쪽은 늘 디스크의 도장에서 다시 읽는다 (시도 기록의 사본을 믿지 않는다) · v1 시도 기록 (latest_attempt_status 없음) 은 solver_status 로 읽는다.
    ★ 10-05 RGLR2-02 — 도장만으로 활성을 말하지 않는다: 디스크가 확정되지 않은 세대면 (`network_generation_problem` — full_metrics ↔ 도장 불일치 ·
      되돌림 실패 · 중단된 게시 흔적 · 도장 손상 — 최근 시도 기록을 못 썼어도) active_status 'invalid' · active_problem = 사유 · stale False
      (화면 값을 "이전 성공 세대" 라고 하지 않는다)."""
    act_id, act_st = _active_generation(results_dir)
    prob = network_generation_problem(results_dir)
    if prob:
        act_st = 'invalid'
    att = read_network_attempt(results_dir) or {}
    last = att.get('latest_attempt_status', att.get('solver_status'))
    kind = att.get('failure_kind')
    if last == 'failed' and not kind:                          # v1 기록 — 종류 칸이 없다 → 남긴 단계 이름으로 (표시용 · 옛 단계 이름 그대로)
        st_ = str(att.get('stage') or '')
        kind = ('lock' if 'LOCK' in st_ else
                'candidate_rejected' if st_.startswith(('Network stop contract', 'Network channel verdict', 'Network σ₀',
                                                         'Network projection')) else
                'publish_exception' if st_.startswith('Network publication') else 'solver')
    return {'active_network_run_id': act_id, 'active_status': act_st, 'active_problem': prob,
            'latest_attempt_run_id': att.get('network_attempt_run_id'), 'latest_attempt_status': last,
            'failure_kind': kind or '', 'latest_attempt_stage': att.get('stage') or '', 'latest_attempt_reason': att.get('reason') or '',
            'stale': bool(last == 'failed' and act_st not in ('none', 'invalid'))}


#: ★ 10-05 RGLR2-02 · Codex Q2 ③ — 회수 규약 단계 이름 (웹앱 단계 로그 · 최근 시도 stage).
NETWORK_RECOVERY_STEP = 'Network recovery (중단된 게시 흔적 격리 · RGLR2-02)'


def quarantine_network_leftovers(results_dir, run_id, argv=None, inputs=None):
    """★ 10-05 RGLR2-02 · Codex Q2 ③ 회수 규약 — 새 망 실행이 lock 안 · stash **전**에 부른다 → 격리한 흔적 이름 목록 ([] = 흔적 없음).

    중단된 게시 · 풀이의 흔적 (`tau_flux.generation_leftovers` — `.publish_backup_*` 사본 · `.stage_stash_net_*`) 이 있으면 그 폴더의 활성 세대는
    **확정되지 않은** 것이다 (`recover_stale_stashes` 의 "이름이 없을 때만 되돌림" 은 원자성 증명이 아니다).  그래서 되살려 재사용하지 않는다:
      ① 그 시점의 판정 (`network_generation_problem` — 흔적 · 세대 불일치 · 손상) 으로 최근 시도에 failed · failure_kind interrupted_publish ·
         active invalid (재실행 필요) 를 **먼저** 기록한다 — 이번 실행이 승격에 성공해야 덮이고, 실패하면 그 실패 기록이 무효를 이어받는다
         (옛 세대를 조용히 유효로 되살리지 않는다).  기록을 못 쓰면 아무것도 옮기지 않고 올린다 (흔적이 남아 읽는 쪽은 계속 무효).
      ② 흔적을 `.network_recovery/<run_id>/` 로 옮겨 **복구 자료로 보존**한다 (지우지 않는다).
      ③ 왜 (사유 · 흔적 이름 · 그 시점 도장) 를 그 안의 `recovery_note.json` 에 남긴다.
    ⚠ 옮기기 · 기록 실패 (OSError 등) 는 호출자에게 올린다 — 호출자는 솔버를 돌리지 않고 망 단계를 실패로 기록한다."""
    tf = _scripts_import('tau_flux')
    names = tf.generation_leftovers(results_dir)
    if not names:
        return []
    why = network_generation_problem(results_dir) or f'중단된 게시 · 풀이 흔적 {names}'
    prov = read_network_provenance(results_dir)
    sub = re.sub(r'[^0-9A-Za-z_-]', '_', str(run_id))
    record_network_attempt(results_dir, run_id, 'failed',
                           reason=(f'중단된 게시 흔적 {names} 을 재사용하지 않고 {NETWORK_RECOVERY_DIR}/{sub}/ 로 격리 — 이 실행이 승격에 성공해야 '
                                   f'활성 세대가 다시 유효 ({why})')[:2000],
                           argv=argv, stage=NETWORK_RECOVERY_STEP, failure_kind='interrupted_publish', inputs=inputs,
                           active_problem=why)
    dst = os.path.join(results_dir, NETWORK_RECOVERY_DIR, sub)
    os.makedirs(dst, exist_ok=True)
    moved = []
    for n in names:
        shutil.move(os.path.join(results_dir, n), os.path.join(dst, n))
        moved.append(n)
    atomic_write_json(os.path.join(dst, 'recovery_note.json'), {
        'schema': 'network_recovery/v1', 'quarantined_by_run_id': run_id,
        'quarantined_at': time.strftime('%Y-%m-%dT%H:%M:%S'), 'leftovers': moved, 'reason': why,
        'provenance_at_quarantine': {k: prov.get(k) for k in ('network_run_id', 'solver_status', 'provenance_state')},
        'rule': ('중단된 게시 · 풀이 흔적은 유효 세대로 재사용하지 않는다 — 복구 자료로 보존 · 활성 세대는 이 실행 (또는 다음 실행) 이 승격에 '
                 '성공할 때까지 무효 (RGLR2-02 · Codex 3차 재검증 Q2 ③)'),
    })
    return moved


#: 승격 중 예외에 대비한 full_metrics 사본의 이름 앞머리 — results 안 (같은 파일시스템 = os.replace 원자성) · 점 접두 (어떤 산출물 glob 에도 안 걸린다).
PUBLISH_BACKUP_PREFIX = '.publish_backup_'
#: 승격 (게시) 단계 이름 — 웹앱 단계 로그 (`app.NETWORK_PUBLISH_STEP`) 와 최근 시도 기록의 stage 가 같은 이름이다.
NETWORK_PUBLISH_STEP = 'Network publication (승격 · 실패 시 되돌림)'


def _content_digest(path):
    """되돌림 검산용 내용 해시 — 파일 = sha256 · 디렉터리 = (상대 경로 · 파일 해시) 정렬 목록의 sha256 · 없으면 None (메타데이터는 보지 않는다)."""
    if not os.path.exists(path):
        return None
    h = hashlib.sha256()
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            dirs.sort()
            for fn in sorted(files):
                p = os.path.join(root, fn)
                h.update(os.path.relpath(p, path).encode('utf-8') + b'\0' + str(_content_digest(p)).encode() + b'\n')
        return 'dir:' + h.hexdigest()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def _rollback_target(results_dir, stash_dir, fm_path):
    """승격 **전**의 디스크 = 되돌림이 만들어야 하는 상태 → {'fm': full_metrics 해시 | None, 'net': {망 산출물 이름: 해시}}.
    옛 망 산출물은 이 시점에 stash 안에 있다 (`stash_network` 가 `NETWORK_ARTIFACT_GLOBS` 전부를 옮겼다 · 첫 실행이면 없음 = {})."""
    net = {}
    if stash_dir and os.path.isdir(stash_dir):
        net = {n: _content_digest(os.path.join(stash_dir, n)) for n in os.listdir(stash_dir)}
    return {'fm': _content_digest(fm_path), 'net': net}


def _rollback_check(results_dir, target, fm_path):
    """★ 10-05 RGLR2-02 — 되돌림의 **실제 결과**를 승격 전 디스크와 대조 → 문제 목록 ([] = 승격 전과 같다).  내용 해시로 본다 (예외가 안 났다는
    사실만으로 복원됐다고 하지 않는다 — Codex rollback_destination_failure)."""
    if target is None:
        return ['승격 전 디스크를 재지 못해 되돌림을 검산할 수 없다']
    try:
        fm_now = _content_digest(fm_path)
        net_now = {os.path.basename(p): _content_digest(p)
                   for pat in NETWORK_ARTIFACT_GLOBS for p in glob.glob(os.path.join(results_dir, pat))}
    except OSError as e:
        return [f'되돌림 검산 중 읽기 실패 ({type(e).__name__}: {e})']
    probs = []
    if fm_now != target['fm']:
        probs.append('full_metrics 가 승격 전과 다르다 (되돌림 결과 불일치)')
    if net_now != target['net']:
        diff = sorted(n for n in set(net_now) | set(target['net']) if net_now.get(n) != target['net'].get(n))
        probs.append(f'망 산출물이 승격 전 세대와 다르다 ({diff[:6]})')
    return probs


def publish_network_candidate(results_dir, stash_dir, run_id, fm=None, inputs=None, argv=None):
    """★ 10-05 WEB-03 Q2a (Codex 재검증 Q2 · 1저자 비준) — 검사를 다 통과한 network 후보를 활성 세대로 **한 번에** 승격 → (ok, 사유, 실패 종류).

    순서: ① full_metrics 사본 (shutil.copy2 — 쓰기 함수를 거치지 않는다) → ② 활성 도장 (provenance) → ③ full_metrics (`atomic_write_json` —
    실패할 수 있는 바로 그 쓰기) → ④ 최근 시도 success → ⑤ 옛 stash · 사본 버림 (= 확정).
    ②–④ 어디서든 동기 예외가 나면 **되돌린다**:
      · full_metrics 를 사본에서 `os.replace` 로 되돌린다 (방금 실패한 쓰기 함수를 다시 부르지 않는다)
      · 후보 망 산출물 (네 JSON · 새 도장 · raw) 을 치우고 옛 세대를 stash 에서 되돌린다 (`discard_network_candidate` — 첫 실행이면 활성 세대 없음)
      · 최근 시도에 failed + failure_kind publish_exception + 단계 · 예외 종류 · 입력 id 를 남긴다 (그 기록마저 못 쓰면 단계 로그에만 남는다)
    → (False, 사유, 'publish_exception' | 'rollback_failed') — 호출자는 **필수 단계 실패**로 기록하고 Stage E 로 가지 않는다 (파이프라인은 failed ·
    예외로 새지 않는다) · 성공이면 (True, '', '').
    왜 다시 던지지 않는가: 되돌린 뒤 디스크는 일관된 상태 (활성 = 옛 세대 · 또는 없음) 이고 실패의 전부가 단계 · 시도 기록에 있다.  예외로 올리면
    run_pipeline 의 단계 로그 · 배치 (`lhs_webapp_batch` — 예외를 그 케이스 failed 로 받기는 한다) · 백그라운드 라우트가 각자 다르게 받아 같은 실패가
    여러 이름이 된다 (한 실패 어휘 위반).  ⚠ BaseException (KeyboardInterrupt · SystemExit) 은 되돌린 뒤 **다시 던진다** (삼키지 않는다).
    ⚠ 이것은 **동기 예외**의 되돌림이다 — 프로세스가 죽는 크래시 (kill -9 · 정전) 의 다중 파일 원자성은 아니다 (세대별 후보 디렉터리 + 단일 활성
    포인터 · 복구 가능한 commit 프로토콜이 필요 — 미구현 · Codex Q2).  크래시 뒤 남은 사본 (`PUBLISH_BACKUP_PREFIX`) · 망 stash 는 **흔적**이다 —
    읽는 쪽이 그 폴더를 무효로 보고 (`network_generation_problem`) 다음 망 실행이 격리한다 (`quarantine_network_leftovers` · RGLR2-02 · Q2 ③).
    ★ 10-05 RGLR2-02 (Codex 3차 재검증) — 되돌림의 **결과를 검산**한다 (`_rollback_check` — 승격 전에 잰 full_metrics · 옛 망 산출물 내용 해시와
      대조).  되돌림 단계가 실패했거나 결과가 승격 전과 다르면 실패 종류 'rollback_failed' — 최근 시도에 active invalid · previous_generation_kept
      False · active_problem 을 남기고 (실패 기록마저 못 쓰면 읽는 쪽이 full_metrics ↔ 도장 불일치 · 남은 사본으로 가른다) 사본은 복구 자료로 둔다.
      옛 판은 되돌림 실패를 사유 문자열에만 적고 kept=True · active success 를 기록해 화면이 "이전 성공 세대 그대로" 라고 했다.
      검산을 통과해야 'publish_exception' (활성 = 옛 세대 · 또는 첫 실행이면 없음).
    """
    fm_path = os.path.join(results_dir, 'full_metrics.json')
    fm_existed = os.path.exists(fm_path)
    bk, bk_ok, fm_touched, step = None, False, False, ''
    try:
        target = _rollback_target(results_dir, stash_dir, fm_path)   # 되돌림 검산 기준 — 승격 쓰기 **전**에 잰다
    except OSError:
        target = None                                          # 못 재면 되돌림을 증명할 수 없다 → 실패 시 rollback_failed (fail-closed)
    try:
        if fm is not None and fm_existed:
            step = 'full_metrics 사본'
            bk = os.path.join(results_dir, f'{PUBLISH_BACKUP_PREFIX}{re.sub(r"[^0-9A-Za-z_-]", "_", str(run_id))}_full_metrics.json')
            shutil.copy2(fm_path, bk)
            bk_ok = True                                       # 사본이 온전히 쓰였다 — 되돌림에 써도 된다
        step = '활성 도장 (network_provenance.json)'
        stamp_network_provenance(results_dir, run_id, inputs, 'success', argv=argv)
        if fm is not None:
            step = 'full_metrics.json'
            fm_touched = True
            atomic_write_json(fm_path, fm)
        step = '최근 시도 success (network_attempt.json)'
        record_network_attempt(results_dir, run_id, 'success', argv=argv, inputs=inputs)
    except BaseException as e:                                 # noqa: BLE001 — 되돌림이 먼저 (KeyboardInterrupt 도 되돌린 뒤 다시 던진다)
        why = f'{step} 쓰기 중 {type(e).__name__}: {e}'
        rb = []
        try:
            if bk_ok:
                _replace_retry(bk, fm_path)                    # 사본 → 제자리 (os.replace · atomic_write_json 을 다시 부르지 않는다)
            else:
                if bk is not None:                             # 사본 자체가 반쯤 쓰였다 — full_metrics 는 아직 안 건드렸다 (사본만 치운다)
                    with contextlib.suppress(OSError):
                        os.remove(bk)
                if fm_touched and not fm_existed and os.path.exists(fm_path):
                    os.remove(fm_path)                         # 없던 full_metrics 를 이번 승격이 만들었다 → 없던 상태로
        except OSError as e2:
            rb.append(f'full_metrics 되돌림 실패 ({type(e2).__name__}: {e2})')
        try:
            discard_network_candidate(results_dir, stash_dir)  # 후보 네 JSON · 새 도장을 치우고 옛 세대를 stash 에서 (첫 실행이면 활성 없음)
        except OSError as e2:
            rb.append(f'망 산출물 되돌림 실패 ({type(e2).__name__}: {e2})')
        if not rb:
            rb = _rollback_check(results_dir, target, fm_path)  # ★ RGLR2-02 — 되돌림 결과 검산 (예외가 없었다는 것만으로 복원을 주장하지 않는다)
        kind = 'rollback_failed' if rb else 'publish_exception'
        if rb:
            left = [n for n in (os.path.basename(bk) if bk else '',) if n and os.path.exists(os.path.join(results_dir, n))]
            why += (' · ⚠ ' + ' · '.join(rb) + ' → 활성 세대 무효 (되돌림 실패 — 값 인용 금지 · 재실행 필요'
                    + (f' · 복구 자료 {left}' if left else '') + ')')
        with contextlib.suppress(Exception):
            record_network_attempt(results_dir, run_id, 'failed', reason=why[:2000], argv=argv,
                                   stage=NETWORK_PUBLISH_STEP, failure_kind=kind, inputs=inputs,
                                   active_problem=(why[:1000] if rb else ''))
        if not isinstance(e, Exception):
            raise
        return False, why, kind
    drop_stash(stash_dir)                                      # 확정 — 옛 세대를 버린다 (여기부터는 되돌리지 않는다)
    if bk is not None:
        with contextlib.suppress(OSError):
            os.remove(bk)
    return True, '', ''


#: `os.replace` 재시도 (Windows).  대기시간 0.02·0.04·0.08·0.16·0.32 s = 총 0.62 s.
_REPLACE_RETRIES = 5
_REPLACE_BACKOFF = 0.02


def _replace_retry(tmp, path, retries=_REPLACE_RETRIES, sleep=None):
    """`os.replace` — Windows 의 일시적 대상파일 점유에만 제한 재시도한다.

    ★ Codex 가 **다른 워크스트림(DFT 대시보드)에서 실측**한 것을 이쪽에 옮긴 것이다:
      Windows 12 프로세스 × 100 건 × 10 회에서 `os.replace()` 가
      `PermissionError [WinError 5]` 로 간헐 실패해 **992/1000** 만 저장됐다.
      락은 정상이었다(임계구역 동시성 1) — 백신·인덱서 같은 **외부 handle** 이 대상
      파일을 잠깐 여는 것이라 우리 락으로는 막을 수 없다.  POSIX 의 rename 은 이런
      이유로 실패하지 않으므로 이 재시도는 리눅스에선 사실상 no-op 이다.

    ⚠ 재시도는 **PermissionError/EACCES 에만** 건다.  다른 OSError(경로 없음, 다른
      파일시스템 등)는 재시도해도 낫지 않고 진짜 버그를 숨기므로 즉시 올린다.
    """
    for attempt in range(retries + 1):
        try:
            os.replace(tmp, path)
            return attempt
        except PermissionError:
            if attempt >= retries:
                raise
        except OSError as e:
            if e.errno != errno.EACCES or attempt >= retries:
                raise
        (sleep or time.sleep)(_REPLACE_BACKOFF * (2 ** attempt))
    raise AssertionError('unreachable')            # pragma: no cover


def atomic_write_json(path, obj):
    """같은 디렉터리 temp → fsync → os.replace(재시도).  부분 쓰기/truncate 를 막는다 (F-10)."""
    d = os.path.dirname(path) or '.'
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix='.tmp_', suffix='.json')
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(obj, f, indent=2, default=str)
            f.flush()
            os.fsync(f.fileno())
        _replace_retry(tmp, path)
    except Exception:
        with contextlib.suppress(OSError):
            os.unlink(tmp)
        raise


# ─────────────────────────────── 단계 계약 ───────────────────────────────

class StageOutcome(dict):
    """한 단계의 결과.  dict 이므로 기존 analysis_log 소비자와 그대로 호환된다."""

    @property
    def ok(self):
        return bool(self.get('ok'))


#: 기본 실행기.  ★ 모듈 속성으로 두는 이유: 기본값을 def 시점에 바인딩하면 테스트가
#: 파이프라인 **전체**(run_pipeline)를 가짜 subprocess 로 돌릴 수 없다 — Codex 요청 T1
#: ("contact rc=1 이면 pipeline failed")은 개별 단계가 아니라 전체 경로를 태워야 한다.
_RUNNER = subprocess.run


def _stat_sig(results_dir, patterns):
    """기대 산출물들의 (경로 → (mtime_ns, size)) 지문.  신선도 판정용."""
    sig = {}
    for rel in patterns:
        for p in glob.glob(os.path.join(results_dir, rel)):
            try:
                s = os.stat(p)
                sig[p] = (s.st_mtime_ns, s.st_size)
            except OSError:
                pass
    return sig


def run_stage(name, cmd, *, cwd=None, required=False, expects=(), results_dir=None,
              runner=None, fresh=False, causal=False, verify=None):
    """subprocess 한 단계를 계약과 함께 실행한다.

    required : 실패하면 파이프라인 전체가 failed
    expects  : 이 단계가 만들어야 하는 파일들 (results_dir 기준 상대경로).
               rc 가 0 이어도 이게 없으면 실패로 본다 — network CLI 는 물리망이
               없을 때 **파일을 안 쓰고도 exit 0** 이 될 수 있다 (리뷰 F-05/F-12).
    causal   : ★ RC7-03 (Codex 7회차).  **권장 형태.**  실행 전에 expects 를 stash 로
               치워 **빈 자리**에서 실행한다 → 실행 후 존재한다는 사실 자체가 "이번 실행이
               만들었다" 는 인과 증거다.  실패하면 되돌려 이전 성공 세대를 보존한다.
               fresh 의 지문 비교와 달리 **metadata-only touch 로 통과할 수 없고**,
               결정론적 재실행이 byte-identical 결과를 내도 거짓 실패가 나지 않는다.
               (causal 이 켜지면 fresh 지문 비교는 하지 않는다 — 더 약한 판정이고
                byte-identical 재계산에서 거짓 실패를 낼 수 있다.)
    fresh    : ★ RV-02.  causal 을 쓸 수 없는 자리(산출물을 치우면 그것이 곧 입력인 단계)의
               약한 대체재.  실행 전후의 (mtime_ns, size) 지문을 비교한다.
               ⚠ metadata-only touch 로 통과한다 — 인과 증거가 아니다.
    verify   : ★ RV-01.  파일 존재만으로는 증거가 안 되는 단계용 (Stage E 는 별도 파일이
               아니라 full_metrics.json **안의 키**를 만든다).  `verify(results_dir)` 가
               False 를 돌리면 실패로 본다.
    runner   : 테스트에서 가짜 실행기를 주입하기 위한 훅.
    """
    stash = None
    if causal and results_dir and expects:
        stash = stash_outputs(results_dir, expects, tag=re.sub(r'\W+', '', name)[:24])
        fresh = False                       # 빈 자리에서 도니 지문 비교는 무의미하다
    before = _stat_sig(results_dir, expects) if (fresh and results_dir) else None
    try:
        res = (runner or _RUNNER)(cmd, capture_output=True, timeout=None, cwd=cwd,
                                  **utf8_subprocess_kwargs())
        rc, out, err = res.returncode, res.stdout, res.stderr
    except Exception as e:                       # noqa: BLE001 — 실행 자체 실패도 단계 실패
        rc, out, err = 1, '', f'{type(e).__name__}: {e}'
    missing, stale, verify_failed = [], [], False
    if results_dir:
        for rel in expects:
            hits = glob.glob(os.path.join(results_dir, rel))
            if not hits:
                missing.append(rel)
        if fresh and before is not None:
            after = _stat_sig(results_dir, expects)
            # ★ RC6-05 (Codex 6회차): 옛 판정은 **전체 dict** 를 한 번에 비교해서
            #   `after == before` 일 때만 stale 로 봤다 → 네 산출물 중 **하나만** 새로
            #   써도 통과하고, 나머지 셋은 옛 것인 채로 새 성공 세대로 도장됐다
            #   (Codex 동적 재현: ok=True, unchanged_old 3개).
            #   → **파일별**로 본다: 실행 전에 있던 파일 중 지문이 그대로인 것은 전부
            #     stale 이다.  (실행 전에 없던 파일은 새로 생긴 것이므로 신선하다.)
            stale = sorted(os.path.basename(k) for k, v in before.items()
                           if after.get(k) == v)
    if verify is not None:
        try:
            verify_failed = not bool(verify(results_dir))
        except Exception:                                   # noqa: BLE001
            verify_failed = True
    ok = (rc == 0) and not missing and not stale and not verify_failed
    if stash is not None:
        # 성공이면 옛 세대를 버리고, 실패면 **부분 산출물을 걷어내고** 되돌린다.
        #   (restore_stash 가 이름별로 덮어쓰므로, 이번 실행이 만든 부분 파일은
        #    같은 이름이면 교체되고 다른 이름이면 남는다 — 계약 파일은 전부 교체된다.)
        drop_stash(stash) if ok else restore_stash(stash, results_dir)
    return StageOutcome(step=name, stdout=out, stderr=err, rc=rc, ok=ok,
                        required=required, missing_outputs=missing,
                        stale_outputs=stale, verify_failed=verify_failed)


def summarize(stages):
    """단계들 → (status, 실패 목록).  status ∈ {done, partial, failed}.

    옛 코드는 무조건 success 였다 (F-05): full_metrics 가 없어도 케이스가 done 이 됐다.
    """
    hard = [s for s in stages if s.get('required') and not s.get('ok')]
    soft = [s for s in stages if not s.get('required') and not s.get('ok')]
    if hard:
        return 'failed', hard
    return ('partial' if soft else 'done'), soft
