#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""세대 2 망 게시 다시 읽기 (읽기 전용) — Codex 세대 2 재검증 §7-4 · §7 끝 (`docs/reviews/codex_review_gen2_network_reverify_20261006.md`).

§7-4: *"real14 · case15 와 정상 비관통 사례를 새 러너에서 생산 → 후보 검사 → 게시 → 인계까지 통과시킨다.  raw 숫자만 비교하지 말고 게시된 증서 · 도장 ·
진단 상태 · 열 역할을 재독한다."*  §7 끝: *"194 완료 뒤 전체 상태 · ID · 증서와 값의 다시 읽기까지 끝나기 전에는 v1.3 의 최종 학습 인계 GO 로 표현하지 않는다."*
⇒ 게시가 끝난 폴더를 **그대로** 다시 읽어 아래를 판정한다 (아무 파일도 쓰지 않는다 · 계산 경로 없음 — 전부 생산 · 게시 · 인계가 쓰는 **같은 함수**를 부른다 · 규율 ①).

입력 (셋 중 하나):
  --smoke-root S     `scripts/wsl_network_smoke.py` ROOT — smoke_report.json 의 망 정지 (stop_after=network) 케이스 · 폴더 S/work/results/<id>
                     (★ 10-07 G2RR4-03 → ★ 10-08 G2RR5-03 — **등록** 음성 대조 (표지 · case15_network · kind case15 · 망 정지 = `case15_negctl_registered`)
                     만 S0 에서 빼고 S0b = 게시 없음 ∧ 기록된 검사 = 등록 안정 ID 일곱 (각 1 회 · 전부 PASS) ∧ 공용 판정 `case15_negctl_verdicts` 를 보고 상세 ·
                     timings 에 다시 돌린 판정 = 기록.  미등록 truthy 표지 = S0 실패 + S0b 문제.  그 판정 술어 · 등록 표 (`CASE15_NEGCTL`) 의 정본 = 이 파일 —
                     스모크 생산자가 import 해 검사를 만든다 (이 파일은 하네스를 import 하지 않는다))
  --launcher-root R  `scripts/run_network_194_parallel.py` ROOT — manifest 의 기대 세대 (expected_network_generation · 없으면 FAIL) · merged/<코호트>
                     (진짜 배치 기록 status.json · metrics_flat.csv) · merged/<코호트>/results/<case>
                     ★ 10-07 G2RR2-02 — **등록 모드 필수**: --expect-set production194 (등록 ID 지문 194) | pilot3 (시범 세 케이스) · 또는 --expect-case 코호트:케이스
                     (여러 번).  계획 큐 (고칠 수 있는 manifest) 를 자기 자신의 유일한 기대 집합으로 쓰지 않는다.
  --case-dir D       케이스 폴더 하나 (여러 번)

케이스마다 (게시 = 배치 · 스모크 기록이 done 인 폴더):
  K1 게시 — full_metrics network_solver_status success · 도장 (network_provenance.json) valid · success · run id 셋 (도장 · full_metrics · active) 같음
  K2 세대 계약 + 증서 결합 — `tau_flux.network_generation_contract(dual)` → 기대 세대 · 문제 0.  세대 2 계약은 모드 셋 (H0 · H12 · physics) × 가지 셋
     (FULL · CF · 협착-only) 의 수치 증서 결합까지 본다 (가지 · 채널 · 역할 · 전극 · ΔV · 봉인된 기하 · 발행 σ_ratio · σ_dim 재구성 · G2RR-02)
  K3 도장 ↔ 레코드 — `pipeline_service.provenance_generation_problem(도장, dual, 세대)` = [] (네 세대 값 = 레코드에서 유도한 기대값 · G2RR-01)
  K4 망 정지 계약 다시 — `pipeline_service.network_stop_verdict(폴더, run id)` (게시 때 계약 ①–⑨ · legacy_ok False)
  K5 열 역할 — `tau_flux.case_row` 의 ion_net_generation = 기대 세대 · `tau_flux.row_generation_problems(행)` = (세대, []) (모드마다 협착 · ψ · 면적 규칙 ·
     전극 · bulk 칸 = 세대 2 표 — 주 hertz = H0 · hertz_h12 = H12 민감도 · physics)
  K6 관통 일치 — 생산자 FULL 상태 (세 모드) ↔ τ 상태: computed → OK 또는 등록된 과학적 HOLD (NOT_COMPUTED · NOT_PERCOLATING 아님) /
     valid_zero → NOT_PERCOLATING
  K7 가지 표 — ★ 10-07 G2RR2-05: 공용 계약의 결과 그대로 (`tau_flux.branch_table_problems` — 숫자 있음 ⇔ 게시 상태 / 숫자 없음 ⇒ 비게시 상태 + 사유 /
     상태 기록 결손 = 거부 · 별도 자격 없음 · 증서 가지 · 역할 결합은 K2)
  H1 인계 출처 관문 — `lhs_design_dataset.load_tau_results(…, expected_generation=기대 세대)` (P0–P4 · 도장 대조 · 배치 기대 세대 교차 대조) 통과 · 칸 = case_row
     launcher-root = 진짜 배치 기록 · smoke-root · case-dir = 그 폴더에서 만든 한 케이스 배치 기록 (⚠ P1 · P3 은 자기 대조가 된다 — 표지 synth_batch)
  M  (launcher-root) — M0 manifest 기대 세대 선언 · ★ G2RR2-02: M-plan 루프 **전** plan · cohorts · queue 꼴 (비지 않음 · 중복 · 코호트 소속 — 실행기
     `plan_problems`) · M-reg 계획 큐 = 등록 집합 · M1 계획 큐 = 배치 기록 · M2 done/partial 아닌 케이스 = FAIL · M3 루프 **밖** 읽은 고유 집합 = 등록 집합
     (기대 수 · 읽은 수 · 빠진 · 남는 — JSON expected_n · read_n · set_equal).  옛 판은 루프 안에서만 봐서 plan · cohorts 삭제 · 빈 cohorts = 0 케이스 PASS.

판정: rc 0 = 전부 PASS · 1 = FAIL 있음 · 2 = 사용 오류.  --json 이면 케이스마다 판정 · 상태표를 남긴다 (붙여 넣을 것 = 화면 요약).
  JSON 스키마 v2 (10-07) = 등록 집합 필드 (expected_set · expected_n · read_n · set_equal · missing · extra) — v1.3 생성기 (`lhs_release_build`) 는
  expected_set production194 · 기대 = 읽음 = 194 · 같음 True 인 기록만 받는다 (옛 v1 기록 · 일부 · pilot3 = 거부).
  ★ JSON 스키마 v3 (10-07 G2RR3-01 · Codex 세대 2 재검증 3 §3 "reread 는 … 이번 ROOT/봉인에 대한 증거인지 결합") = 실행 신원 (--launcher-root 일 때 ·
  그 밖 = null): launcher_root (읽은 ROOT · resolve) · manifest_sha256 (판정에 쓴 manifest **바이트** 의 sha256 — 같은 바이트를 해석했다) · seal_fp
  (그 manifest 의 seal.code_fp) · launch_sha (git.sha).  v1.3 배포 관문 (`lhs_release_build.v13_reread_problems`) 이 배치 뿌리 · 지금 manifest · 발사 봉인과
  맞댄다 — 다른 ROOT · 봉인 · 읽은 뒤 바뀐 manifest 의 기록 = 거부 (옛 v2 기록 = 실행 신원 없음 = 진단 모드에서만).
  ★ 10-07 G2RR4-01 (Codex 세대 2 재검증 4 §2) — 상세 계약 (`CASE_CHECK_IDS` · `LAUNCHER_META_IDS` · `LAUNCHER_COHORT_META_IDS` · `launcher_detail_problems`):
  배포 관문이 같은 함수로 상세 (meta · cases · checks) ↔ 요약 (n_fail · read_n · M3) 을 다시 센다 (스키마 v3 그대로 — 기록 꼴은 바뀌지 않았다 · 검사가 늘었다).
⚠ 한계 — 도장 · 레코드 · 모든 사본 · 증서를 한 실행 안에서 일관되게 함께 바꾼 전면 위조는 재계산 없이 못 잡는다 (TAU_SAME_GEN_BASIS · Codex §3 의 "보증 아님" 그대로).
   이 도구의 PASS 는 게시 · 인계가 쓰는 계약을 **지금 파일에** 다시 부른 결과다 — 숫자의 물리적 정확성 · 실험 대조가 아니다.

사용 (WSL · 리포 루트)
  P=~/Yonghoon-DEM-DFT/venv/bin/python
  $P scripts/g2_network_reread.py --smoke-root ~/g2pre_smoke_<sha> --json ~/g2pre_smoke_<sha>/reread.json
  $P scripts/g2_network_reread.py --launcher-root ~/g2pre_pilot_<sha> --expect-set pilot3 --json ~/g2pre_pilot_<sha>/reread.json
  $P scripts/g2_network_reread.py --launcher-root ~/net194_<sha> --expect-set production194 --json ~/net194_<sha>/reread.json
  $P scripts/g2_network_reread.py --selftest
"""
from __future__ import annotations

import argparse
import collections
import contextlib
import hashlib
import io
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
for _p in (str(ROOT / 'scripts'), str(ROOT / 'webapp')):
    if _p not in sys.path:
        sys.path.insert(0, _p)

SCHEMA = 'g2_network_reread/v3'     # v2 (10-07 G2RR2-02) = 등록 집합 필드 (expected_set · expected_n · read_n · set_equal · missing · extra) ·
#                                     v3 (10-07 G2RR3-01) = 실행 신원 (launcher_root · manifest_sha256 · seal_fp · launch_sha — run_launcher 가 읽은 바이트에서)
IDENTITY_KEYS = ('launcher_root', 'manifest_sha256', 'seal_fp', 'launch_sha')
BRANCHES = (('full', 'sigma_full', 'sigma_full_status', 'sigma_full_reason', 'solve_certificate_full'),
            ('bulk_only', 'sigma_bulk_net', 'sigma_bulk_net_status', 'sigma_bulk_net_reason', 'solve_certificate_bulk_net'),
            ('constriction_only', 'sigma_constr_net', 'sigma_constr_net_status', 'sigma_constr_net_reason', 'solve_certificate_constr_net'))
#: ★ 10-07 G2RR4-01 (Codex 세대 2 재검증 4 §2) — launcher-root 판정 JSON 의 **상세 계약** — 생산자 (`run_launcher` · `reread_case`) 가 내는 검사 ID (이름의 첫 낱말) 를
#:   한곳에 둔다.  v1.3 배포 관문 (`lhs_release_build.v13_reread_problems`) 이 `launcher_detail_problems` (같은 함수) 로 상세를 다시 센다 — 옛 배포 관문은 요약
#:   (n_fail · 집합 칸 · 신원) 만 읽어 meta[].ok=false (n_fail 0 유지) · cases=[] · meta=[] (read_n 194 유지) 를 받았다.  생산자가 검사를 더하거나 이름을 바꾸면
#:   이 표를 같이 고친다 (selftest 가 실 생산자 JSON 을 이 계약에 넣는다).
CASE_CHECK_IDS = ('K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'K7')       # reread_case — 케이스마다 한 번씩
CASE_CHECK_EXTRA = ('K1b',)                                       # run_launcher — 배치 기록 run id ≠ 폴더 run id 일 때만 붙는다 (붙으면 그 케이스는 실패)
LAUNCHER_META_IDS = ('M0', 'M-plan', 'M-reg', 'M3')               # run_launcher — 코호트 무관 · 한 번씩
LAUNCHER_COHORT_META_IDS = ('M1', 'M2', 'H1')                     # run_launcher — 코호트마다 한 번씩 ('<ID> <코호트> …')
M3_SUMMARY_KEYS = ('expected_n', 'read_n', 'set_equal', 'missing', 'extra')   # main 이 M3 항목에서 판정 JSON 최상위로 옮겨 적는 칸


# ─────────────────── ★ 10-08 G2RR5-02 · 03 — case15 음성 대조의 한 곳 (생산자 = 스모크 evaluate · 소비자 = S0b) ───────────────────
#: ★ 10-08 G2RR5-03 (Codex 세대 2 재검증 5 §3 최소 해결) — 등록 표지 · 케이스 신원 · 필수 검사 안정 ID 표 · 판정 술어를 **인계 도구 한 곳**에 둔다.
#:   생산자 (`scripts/wsl_network_smoke.py` evaluate) 가 이 함수로 case15 검사 일곱을 만들고 (검사 dict 에 id) · 소비자 (이 파일 `--smoke-root` S0b) 는 보고
#:   상세에 **같은 함수를 다시 돌려** 기록된 판정과 맞댄다 (상세 결손 · 수치 모순 = 실패).  방향은 하네스 → 인계 도구 하나뿐 — 인계 도구 (발사 때 지문을 기록하는
#:   HANDOVER_FILES) 는 하네스 (스모크 — 관측 · 지문 밖) 를 import 하지 않는다.
#:   값 = 10-07 G2RR4-03 의 스모크 CASE15_NEGCTL 그대로 옮김 (원인 · 이온 참고값) + 10-08 케이스 신원 (case_id · kind · stop_after) + ⑤ 실제 망 시도 표 (G2RR5-02 —
#:   10-08 이 컨테이너 실제 case15 (커밋된 원자료) 첫 실행으로 고정: 실패 상태 'failed' = `pipeline_service._CHANNEL_FAIL_STATES` · 겹침 사유 = 생산자
#:   `_channel_solve_failure` 가 `network_conductivity.BOUNDARY_OVERLAP_REASON` 을 괄호로 싣는 꼴 · Physics 열 = 솔버 ValueError 그대로 (원자료 탐침 오류와 같은
#:   바이트 · WSL 10-07 기록도 같다) · 이온 두 모드 = 'computed' (사유 칸 없음)).
CASE15_NEGCTL = dict(
    tag='case15_publication_blocked', case_id='case15_network', kind='case15', stop_after='network',
    b_and_t_ids=(24, 40, 57, 103), negative_rows=((31, 29241), (38, 29241)),
    ionic_ref8={'hertzian': 0.00032635, 'physics': 0.00036225}, cert_max=1e-6,
    overlap_channels=('electronic_hertzian', 'electronic_physics', 'thermal_hertzian'), refuse_channel='thermal_physics',
    refuse_text='ligg_area < 0', solver_step='Network Solver (both modes)',
    attempt_modes=('hertzian', 'physics'), attempt_channels=('ionic', 'electronic', 'thermal'),
    attempt_ok_status='computed', attempt_fail_status='failed', overlap_token='(boundary_overlap)', overlap_reason='boundary_overlap',
    refuse_prefix='ValueError: ',
    attempt_table={'hertzian.ionic': 'computed', 'physics.ionic': 'computed',
                   'hertzian.electronic': 'boundary_overlap', 'physics.electronic': 'boundary_overlap',
                   'hertzian.thermal': 'boundary_overlap', 'physics.thermal': 'ligg_area_negative'})
#: 필수 검사 = (안정 ID, 이름 꼬리) — 차례 그대로.  생산자 검사 dict 의 id · 소비자 S0b 는 그 케이스의 기록이 이 집합과 **정확히** 같기를 (각 1 회 · 모르는 ID ·
#:   id 없는 행 거부) 요구한다 — 접두어 '[음성 대조]' PASS 행 수 (옛 '넷 이상') 를 세지 않는다.
CASE15_NEGCTL_CHECKS = (
    ('case15.proc', '자식 프로세스 정상 종료 · 보고서 있음'),
    ('case15.raw_sha', '원자료 sha256 = README 표 (압축 푼 바이트)'),
    ('case15.nc1_blocked', f'[음성 대조] 게시 차단 — failed · 실패 단계 {CASE15_NEGCTL["solver_step"]} · Stage E 안 돌았다 · 반환 run id 없음 '
                           '(옛 성공 산출물 재사용 없음)'),
    ('case15.nc2_tau', '[음성 대조] 인계 숫자 비노출 — τ 세 모드 NOT_COMPUTED · 숫자 칸 없음'),
    ('case15.nc3_cause', f'[음성 대조] 원인 발화 (원덤프 직접 6 조합) — 전자 두 모드 · Hertz 열 boundary_overlap · B∩T = 입자 ID '
                         f'{list(CASE15_NEGCTL["b_and_t_ids"])} · Physics 열 음수 원자료 면적 거부 · 음수 행 {len(CASE15_NEGCTL["negative_rows"])}'),
    ('case15.nc4_ionic', f'[음성 대조] 이온 정상 — 두 모드 computed · σ_ratio 참고 8 자리 {CASE15_NEGCTL["ionic_ref8"]} · 증서 보존 · 잔차 '
                         f'0 이상 {CASE15_NEGCTL["cert_max"]} 미만'),
    ('case15.nc5_attempt', '[음성 대조] 실제 망 시도 — 이번 시도의 망 CLI 1 회 · 예외 없음 · rc 0 · per-mode 둘 · 실패 채널 = 등록 넷 (전자 두 모드 · Hertz 열 '
                           'boundary_overlap · Physics 열 음수 면적 거부) · 이온 computed · 단계 rc 0 · 결손 0 · 내용 검증 거부 · 시도 기록 = 기록기 digest · '
                           '원자료 탐침과 같은 원인 (실행 실패 = TECH)'),
)
CASE15_NEGCTL_IDS = tuple(i for i, _n in CASE15_NEGCTL_CHECKS)
CASE15_NEGCTL_ID_PREFIX = 'case15.'


def _c15_d(x):
    return x if isinstance(x, dict) else {}


def _c15_int0(v):
    """정수 0 (bool 아님)."""
    return isinstance(v, int) and not isinstance(v, bool) and v == 0


def _c15_cert(x, cap):
    """증서 수치 — 실수 (bool 아님) · 유한 · 0 이상 · cap 미만 (Codex 재검증 5 §5 "유한 · 비음수 잔차 / 보존 오차를 엄격히")."""
    return isinstance(x, (int, float)) and not isinstance(x, bool) and 0 <= x < cap


def _c15_hex64(s):
    return isinstance(s, str) and len(s) == 64 and all(c in '0123456789abcdef' for c in s)


def _c15_attempt_class(st, ng):
    """기록기가 읽은 per-mode 채널 기록 dict(status, reason) → 등록 표의 분류 (computed · boundary_overlap · ligg_area_negative) · 그 밖 = 그대로 적은 문자열."""
    if not isinstance(st, dict):
        return 'missing'
    s, rs = st.get('status'), ('' if st.get('reason') is None else str(st.get('reason')))
    if s == ng['attempt_ok_status']:
        return 'computed'
    if s == ng['attempt_fail_status'] and ng['overlap_token'] in rs:
        return 'boundary_overlap'
    if s == ng['attempt_fail_status'] and rs.startswith(ng['refuse_prefix']) and ng['refuse_text'] in rs:
        return 'ligg_area_negative'
    return f'{s}: {rs[:80]}'


def _c15_raw_class(d, ng):
    """원자료 탐침 (스모크 `case15_channel_probe`) 의 채널 결과 → 같은 분류."""
    if not isinstance(d, dict):
        return 'missing'
    if d.get('error') is not None:
        e = str(d['error'])
        return 'ligg_area_negative' if (e.startswith(ng['refuse_prefix']) and ng['refuse_text'] in e) else f'error: {e[:80]}'
    if d.get('status') == 'computed':
        return 'computed'
    if d.get('reason') == ng['overlap_reason']:
        return 'boundary_overlap'
    return f'{d.get("status")}/{d.get("reason")}'


def case15_attempt_verdict(r, ng=None):
    """★ 10-08 G2RR5-02 (Codex 세대 2 재검증 5 §2) — case15 음성 대조 ⑤ 실제 망 시도 → (판정, 세부).  판정 = PASS · TECH · FAIL.
      TECH (실행 실패 — 지정한 내용 거부가 아니다): 망 CLI 호출 0 회 · 예외 (PermissionError · FileNotFoundError · TimeoutExpired …) · rc ≠ 0 · per-mode 산출물 없음 · 못 읽음 ·
           망 솔버 단계 rc ≠ 0 · 산출 결손 (missing_outputs) · stale
      FAIL: 실제 시도 증거 없음 (기록기 없는 옛 기록) · 호출 2 회 이상 · 단계 기록 결손 · 내용 검증 거부가 아님 · 실패 채널 집합 ≠ 등록 넷 (+ 이온 computed 둘) ·
           Physics 열 거부 문자열 ≠ 원자료 탐침 오류 · 시도 기록 (단계 · 상태 · input_digests) ↔ 기록기 어긋남 · 원자료 탐침과 다른 원인
    300 자 err · 시도 사유 문자열은 보지 않는다 — 기록기 (스모크 `network_cli_recorder`) 의 구조 증거와 단계 구조 필드로만 판정한다."""
    ng = ng or CASE15_NEGCTL
    ev = r.get('attempt_evidence')
    if not isinstance(ev, dict) or not isinstance(ev.get('calls'), list):
        return 'FAIL', '실제 시도 증거 없음 (attempt_evidence) — 이번 망 CLI 시도를 확인할 수 없다 (G2RR5-02 이전 기록 · 기록기 없음)'
    calls = ev['calls']
    if not calls:
        return 'TECH', '망 CLI 호출 0 회 — 솔버가 실행되지 않았다 (lock · 흔적 격리 · 실행 경계) — 지정한 내용 거부가 아니다'
    if len(calls) != 1 or not isinstance(calls[0], dict):
        return 'FAIL', f'망 CLI 호출 {len(calls)} 회 — 정확히 1 회여야'
    c = calls[0]
    if c.get('exception') is not None:
        return 'TECH', f'망 CLI 실행 예외 {c.get("exception")} ({str(c.get("exception_text"))[:120]}) — 실행 실패 (지정한 내용 거부 아님)'
    if not _c15_int0(c.get('returncode')):
        return 'TECH', f'망 CLI rc {c.get("returncode")!r} — 실행 실패 (지정한 내용 거부 아님)'
    pm = c.get('per_mode') if isinstance(c.get('per_mode'), dict) else {}
    miss = [m for m in ng['attempt_modes']
            if not (isinstance(pm.get(m), dict) and _c15_hex64(pm[m].get('sha256')) and isinstance(pm[m].get('channels'), dict))]
    if miss:
        return 'TECH', f'per-mode 산출물 없음 · 못 읽음 {miss} — 실행 실패 (지정한 내용 거부 아님)'
    sv = [s for s in (r.get('stages') or []) if isinstance(s, dict) and s.get('step') == ng['solver_step']]
    if len(sv) != 1:
        return 'FAIL', f'망 솔버 단계 기록 {len(sv)} 개 — 하나여야'
    s = sv[0]
    if not _c15_int0(s.get('rc')) or s.get('missing_outputs') != [] or s.get('stale_outputs') != []:
        return 'TECH', (f'망 솔버 단계 rc {s.get("rc")!r} · 산출 결손 {s.get("missing_outputs")!r} · stale {s.get("stale_outputs")!r} — 실행 실패 '
                        '(지정한 내용 거부 아님)')
    if s.get('verify_failed') is not True or s.get('ok') is not False:
        return 'FAIL', f'망 솔버 단계가 내용 검증 거부가 아니다 (verify_failed {s.get("verify_failed")!r} · ok {s.get("ok")!r})'
    got = {f'{m}.{ch}': _c15_attempt_class(_c15_d(pm[m].get('channels')).get(ch), ng) for m in ng['attempt_modes'] for ch in ng['attempt_channels']}
    if got != ng['attempt_table']:
        return 'FAIL', f'실패 채널 집합 ≠ 등록 — 다름 {({k: (v, ng["attempt_table"].get(k)) for k, v in got.items() if v != ng["attempt_table"].get(k)})}'
    raw = _c15_d(_c15_d(r.get('negctl')).get('channels'))
    for k, cls in ng['attempt_table'].items():
        m, ch = k.split('.')
        mine, theirs = _c15_d(_c15_d(pm[m].get('channels')).get(ch)).get('reason'), _c15_d(raw.get(f'{ch}_{m}')).get('error')
        if cls == 'ligg_area_negative' and mine != theirs:
            return 'FAIL', f'{k} 거부 문자열 ≠ 원자료 탐침 오류 — {mine!r} ↔ {theirs!r}'
    att = _c15_d(r.get('attempt'))
    dg = c.get('input_digests')
    if not (isinstance(dg, dict) and len(dg) == 2 and all(isinstance(v, str) and v for v in dg.values())) or att.get('input_digests') != dg:
        return 'FAIL', f'시도 기록 input_digests {att.get("input_digests")!r} ≠ 기록기 {dg!r} — 이 시도의 입력이 아니다'
    if att.get('stage') != ng['solver_step'] or att.get('latest_attempt_status') != 'failed':
        return 'FAIL', f'시도 기록 단계 {att.get("stage")!r} · 상태 {att.get("latest_attempt_status")!r} — 망 솔버 단계 · failed 여야'
    rawc = {k: _c15_raw_class(raw.get(f'{k.split(".")[1]}_{k.split(".")[0]}'), ng) for k in ng['attempt_table']}
    if rawc != got:
        return 'FAIL', f'원자료 탐침의 원인 ≠ 이번 시도 — 다름 {({k: (got.get(k), v) for k, v in rawc.items() if v != got.get(k)})}'
    return 'PASS', (f'망 CLI 1 회 · rc 0 · per-mode 둘 (sha256 {pm["hertzian"]["sha256"][:12]} · {pm["physics"]["sha256"][:12]}) · 실패 = 등록 넷 · '
                    f'이온 computed 둘 · 단계 rc 0 · 결손 0 · 내용 검증 거부 · 시도 기록 = 망 솔버 단계 · digest {dg} · 원자료 탐침과 같은 원인')


def case15_negctl_registered(cid, r) -> bool:
    """등록된 음성 대조인가 — 표지 = 등록 표지 ∧ 케이스 id = case15_network ∧ kind = case15 ∧ stop_after = network.  그 밖 truthy 표지 = **미등록**
    (생산자: FAIL 행 · 소비자: S0 에서 빼지 않는다 + S0b 문제)."""
    ng = CASE15_NEGCTL
    return (isinstance(r, dict) and r.get('negative_control') == ng['tag'] and cid == ng['case_id'] and r.get('kind') == ng['kind']
            and r.get('stop_after') == ng['stop_after'])


def case15_negctl_verdicts(r, timing, cid=None) -> list:
    """★ 10-08 G2RR5-03 — case15 음성 대조 보고 (스모크 `reports[cid]`) + 자식 프로세스 기록 (스모크 `timings[cid]`) → [(id, 이름, 판정, 세부)]
    (`CASE15_NEGCTL_CHECKS` 차례 그대로 · 일곱).  순수 함수 — 파일 · 환경을 읽지 않는다 (생산자 · 소비자가 같은 입력에 같은 판정) · 꼴이 깨진 상세 = FAIL
    (예외로 새지 않는다).
      proc      자식 프로세스 정상 종료 (rc = 정수 0) · 보고서 id = 케이스 id
      raw_sha   원자료 sha256 = README 표 (raw_sha_ok is True)
      nc1 ~ nc4 게시 차단 · τ 비노출 · 원인 발화 (원자료 탐침 — 보조 증거) · 이온 정상  (10-07 G2RR4-03 판정을 옮김 · 증서 수치 = 0 이상 · 유한 · bool 아님)
      nc5       실제 망 시도 (10-08 G2RR5-02 — `case15_attempt_verdict` · 실행 실패 = TECH)"""
    ng = CASE15_NEGCTL
    cid = cid or ng['case_id']
    r, t = _c15_d(r), _c15_d(timing)
    names = dict(CASE15_NEGCTL_CHECKS)
    out = []

    def ok(b):
        return 'PASS' if b else 'FAIL'

    def put(i, fn):
        try:
            v, d = fn()
        except Exception as e:                                   # noqa: BLE001 — 꼴이 깨진 상세 = 판정 FAIL
            v, d = 'FAIL', f'판정 예외 {type(e).__name__}: {e}'
        out.append((i, f'{cid}: {names[i]}', v, d))

    put('case15.proc', lambda: (ok(_c15_int0(t.get('rc')) and r.get('id') == cid),
                                f'rc {t.get("rc")!r} {t.get("signal") or ""} · 보고서 id {r.get("id")!r}'))
    put('case15.raw_sha', lambda: (ok(r.get('raw_sha_ok') is True), r.get('raw_sha')))

    def nc1():
        fs = r.get('failed_stages')
        return (ok(r.get('status') == 'failed' and isinstance(fs, list) and ng['solver_step'] in fs and r.get('stage_e_ran') is False
                   and not r.get('returned_network_run_id')),
                f'status {r.get("status")} · 실패 단계 {fs} · Stage E {r.get("stage_e_ran")} · run id {r.get("returned_network_run_id")}')

    def nc2():
        tau = _c15_d(r.get('tau'))
        sts = {m: tau.get(f'ion_net_status_{m}') for m in ('hertz', 'physics', 'hertz_h12')}
        nums = {k: v for k, v in tau.items() if str(k).startswith(('f_ion_', 'tau2_ion_', 'tau_ion_')) and v not in (None, '')}
        return ok(set(sts.values()) == {'NOT_COMPUTED'} and not nums), f'{sts} · 숫자 {nums}'

    def nc3():
        neg = _c15_d(r.get('negctl'))
        ch = _c15_d(neg.get('channels'))
        ids = list(ng['b_and_t_ids'])
        ov = {k: (_c15_d(ch.get(k)).get('reason'), _c15_d(ch.get(k)).get('intersection')) for k in ng['overlap_channels']}
        refuse = str(_c15_d(ch.get(ng['refuse_channel'])).get('error') or '')
        rows = sorted(tuple(int(v) for v in x[:2]) for x in (neg.get('negative_area') or []) if isinstance(x, (list, tuple)) and len(x) >= 2)
        return (ok(bool(ch) and all(v == (ng['overlap_reason'], ids) for v in ov.values()) and ng['refuse_text'] in refuse
                   and rows == sorted(ng['negative_rows'])),
                f'겹침 {ov} · Physics 열 {refuse[:120]!r} · 음수 행 {rows} · 증거 오류 {neg.get("error")}')

    def nc4():
        ch = _c15_d(_c15_d(r.get('negctl')).get('channels'))
        ion = {}
        for m in ng['ionic_ref8']:
            d = _c15_d(ch.get(f'ionic_{m}'))
            v = d.get('value') or [None, None]
            q = v[1] if isinstance(v, (list, tuple)) and len(v) > 1 else None
            ion[m] = (d.get('status'), round(q, 8) if isinstance(q, (int, float)) and not isinstance(q, bool) else None,
                      d.get('conservation_rel'), d.get('residual_rel'))
        return (ok(all(s == 'computed' and q == ng['ionic_ref8'][m] and _c15_cert(c, ng['cert_max']) and _c15_cert(e, ng['cert_max'])
                       for m, (s, q, c, e) in ion.items())), ion)

    put('case15.nc1_blocked', nc1)
    put('case15.nc2_tau', nc2)
    put('case15.nc3_cause', nc3)
    put('case15.nc4_ionic', nc4)
    put('case15.nc5_attempt', lambda: case15_attempt_verdict(r, ng))
    return out


def case15_negctl_s0b_problems(cid, r, checks, timing) -> list:
    """★ 10-08 G2RR5-03 — 등록된 음성 대조 케이스 하나의 S0b 문제 목록 ([] = 통과).  (등록 여부 = `case15_negctl_registered` — 부르는 쪽이 먼저 가른다.)
      ① 게시 없음 (status done 아님 · 반환 run id 없음)
      ② 그 케이스의 기록된 검사 (이름 '<cid>:' 또는 id 'case15.') = 등록 안정 ID 집합 정확히 — 각 1 회 · id 없는 행 · 모르는 ID = 거부 · 전부 PASS
      ③ 공용 판정 `case15_negctl_verdicts` 를 보고 상세 (reports[cid]) · 자식 프로세스 기록 (timings[cid]) 에 **다시** 돌린 판정 = 기록된 판정 (상세 결손 · 수치 모순 = 다름)
    '[음성 대조] PASS 넷 이상' 같은 접두어 계수를 하지 않는다 (Codex 재검증 5 §3 — 한 행 네 번 · 미등록 표지 · 상세 결손 · 실제 SHA FAIL 이 통과했다)."""
    r = _c15_d(r)
    why = []
    if r.get('status') == 'done' or r.get('returned_network_run_id'):
        why.append(f'게시됨 (status {r.get("status")!r} · run id {r.get("returned_network_run_id")!r}) — 음성 대조가 발화하지 않았다')
    rows = [c for c in (checks if isinstance(checks, list) else []) if isinstance(c, dict)
            and (str(c.get('name', '')).startswith(f'{cid}:') or str(c.get('id', '')).startswith(CASE15_NEGCTL_ID_PREFIX))]
    cnt = collections.Counter(c.get('id') for c in rows)
    unknown = sorted(repr(i) for i in cnt if i not in CASE15_NEGCTL_IDS)
    off = {i: cnt[i] for i in CASE15_NEGCTL_IDS if cnt[i] != 1}
    if unknown or off:
        why.append(f'기록된 {cid} 검사 ≠ 등록 안정 ID 집합 — id 없음 · 모르는 {unknown} · 한 번이 아님 {off} (등록 {list(CASE15_NEGCTL_IDS)} · 각 1 회)')
    notpass = [(c.get('id'), c.get('verdict')) for c in rows if c.get('verdict') != 'PASS']
    if notpass:
        why.append(f'기록된 판정이 PASS 아님 {notpass}')
    rec = {c.get('id'): c.get('verdict') for c in rows if c.get('id') in CASE15_NEGCTL_IDS}
    diff = {i: (rec.get(i), v, str(d)[:160]) for i, _n, v, d in case15_negctl_verdicts(r, timing, cid) if rec.get(i) != v}
    if diff:
        why.append(f'공용 판정 재계산 ≠ 기록 {diff} — 보고 상세가 기록된 판정을 뒷받침하지 않는다 (상세 결손 · 수치 모순 · 실행 실패)')
    return why


def _read_json(p):
    try:
        return json.loads(Path(p).read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None


def _mods():
    import pipeline_service as ps
    import tau_flux as tf
    import lhs_design_dataset as LDD
    import lhs_webapp_batch as LWB
    return ps, tf, LDD, LWB


def branch_table(tf, dual):
    """모드 × 가지 표 (읽기만) → {모드: {가지: dict(status, reason, value, cert_branch, cert_role, cert_reason)}}."""
    out = {}
    for m in tf.MODES:
        rec = tf.mode_record(dual, m)
        if rec is None:
            out[m] = None
            continue
        row = {}
        for b, qk, sk, rk, ck in BRANCHES:
            c = rec.get(ck) if isinstance(rec.get(ck), dict) else None
            row[b] = dict(status=rec.get(sk), reason=rec.get(rk), value=rec.get(qk),
                          cert=(None if c is None else dict(branch=c.get('branch'), role=c.get('role'), status=c.get('status'),
                                                            method=c.get('method'), reason=c.get('reason'))))
        out[m] = row
    return out


def _k7_problems(tf, dual):
    """K7 — 가지 표 = **공용 계약의 결과 그대로** (`tau_flux.branch_table_problems` — 세대 2 계약 · 정지 계약 ⑨ · 공용 기록 검사 · τ 소비자 · 인계 P4 가
    싣는 같은 결과: 숫자 있음 ⇔ 게시 상태 / 숫자 없음 ⇒ 비게시 상태 + 사유 / 상태 기록 결손 = 거부).  ★ 10-07 G2RR2-05 (Codex 세대 2 재검증 2 §6) — 옛 K7 은
    별도 자격 (숫자 없음 ↔ 상태 None) 을 더했고 공용 계약은 그 결손을 받았다 (진단 가지 다섯 키 삭제 = 게시 done · 인계 통과 · K7 만 거부).  증서 가지 ·
    역할 결합은 K2 (같은 계약의 증서 결합) 가 본다."""
    out = []
    for m in tf.MODES:
        rec = tf.mode_record(dual, m)
        if rec is not None:
            out += [f'{m}.{p}' for p in tf.branch_table_problems(m, rec)]
    return out


def reread_case(cd, expected, ps, tf):
    """케이스 폴더 하나 → dict(case, checks[{name, ok, detail}], generation, statuses, table, row_cells)."""
    cd = Path(cd)
    checks = []

    def ck(name, ok, detail=''):
        checks.append(dict(name=name, ok=bool(ok), detail=str(detail)[:900]))
    fm = _read_json(cd / 'full_metrics.json') or {}
    dual = _read_json(cd / 'network_conductivity_dual.json')
    prov = ps.read_network_provenance(str(cd)) or {}
    rid = fm.get('network_run_id')
    ck('K1 게시 — solver success · 도장 valid/success · run id (도장 = full_metrics = active)',
       fm.get('network_solver_status') == 'success' and prov.get('provenance_state') == 'valid' and prov.get('solver_status') == 'success'
       and isinstance(rid, str) and rid and prov.get('network_run_id') == rid == fm.get('active_network_run_id'),
       f"solver {fm.get('network_solver_status')!r} · 도장 {prov.get('provenance_state')!r}/{prov.get('solver_status')!r} · "
       f"run id {prov.get('network_run_id')!r} · {rid!r} · {fm.get('active_network_run_id')!r}")
    if not isinstance(dual, dict):
        ck('K2 세대 계약 + 증서 결합', False, 'network_conductivity_dual.json 없음 · 못 읽음')
        return dict(case=cd.name, folder=str(cd), checks=checks, generation=None)
    con = tf.network_generation_contract(dual)
    gen = con.get('generation')
    ck(f'K2 세대 계약 + 증서 결합 — 세대 {expected!r} · 문제 0 (모드 셋 × 가지 셋 증서 · G2R-01 · 02 · G2RR-02)',
       gen == expected and not con.get('problems'), f'세대 {gen!r} · {tf.generation_contract_text(con)[:700]}')
    sp = ps.provenance_generation_problem(prov, dual, gen)
    ck('K3 도장 ↔ 레코드 — 네 세대 값 = 레코드에서 유도한 기대값 (G2RR-01)', not sp,
       ' · '.join(sp) or {k: prov.get(k, 'ABSENT') for k in ps.PROVENANCE_GENERATION_KEYS})
    try:
        ok4, why4 = ps.network_stop_verdict(str(cd), rid)
    except Exception as e:                                       # noqa: BLE001 — 판정을 못 내면 통과로 치지 않는다
        ok4, why4 = False, f'{type(e).__name__}: {e}'
    ck('K4 망 정지 계약 다시 (①–⑨ · legacy_ok False)', ok4, why4)
    row = tf.case_row(str(cd))
    rg, rprob = tf.row_generation_problems(row)
    ck(f'K5 열 역할 — ion_net_generation {expected!r} · 행 세대 계약 문제 0 (모드별 협착 · ψ · 면적 · 전극 · bulk 칸)',
       row.get(tf.ROW_GENERATION_COL) == expected and rg == expected and not rprob,
       f'칸 {row.get(tf.ROW_GENERATION_COL)!r} · 행 판정 {rg!r} · {rprob[:3]}')
    statuses = {m: (row.get(f'ion_net_status_{m}'), row.get(f'ion_net_status_reason_{m}')) for m in tf.MODES}
    table = branch_table(tf, dual)
    bad6 = []
    for m in tf.MODES:
        st_full = ((table.get(m) or {}).get('full') or {}).get('status')
        s, r_ = statuses[m]
        if st_full == 'computed' and s in ('NOT_COMPUTED', 'NOT_PERCOLATING', None):
            bad6.append(f'{m}: 생산자 computed ↔ τ {s} ({r_})')
        elif st_full == 'valid_zero' and s != 'NOT_PERCOLATING':
            bad6.append(f'{m}: 생산자 valid_zero ↔ τ {s} ({r_})')
        elif st_full not in ('computed', 'valid_zero'):
            bad6.append(f'{m}: 생산자 FULL 상태 {st_full!r} (게시된 레코드에 있을 수 없는 상태)')
    ck('K6 관통 일치 — 생산자 FULL 상태 ↔ τ 상태 (세 모드)', not bad6, ' · '.join(bad6) or statuses)
    bad7 = _k7_problems(tf, dual)
    ck('K7 가지 표 — 공용 계약 (tau_flux.branch_table_problems) 그대로: 숫자 ⇔ 게시 상태 / 숫자 없음 ⇒ 비게시 상태 + 사유 / 상태 기록 결손 = 거부',
       not bad7, ' · '.join(bad7[:6]))
    return dict(case=cd.name, folder=str(cd), run_id=rid, checks=checks, generation=gen, statuses=statuses, table=table,
                stamp={k: prov.get(k, 'ABSENT') for k in ps.PROVENANCE_GENERATION_KEYS},
                sigma_ratio={m: ((table.get(m) or {}).get('full') or {}).get('value') for m in tf.MODES},
                row_cells={c: tf._cell(row.get(c)) for c in tf.column_names()})


def handover_gate(results_dir, wv, expected, LDD):
    """H1 — 인계 출처 관문 (P0–P4 · 도장 대조 · 배치 기대 세대) → (ok, 사유 · 케이스별 칸)."""
    try:
        tv = LDD.load_tau_results(results_dir, wv, expected_generation=expected)
    except Exception as e:                                       # noqa: BLE001 — FillRefusal · 예외 둘 다 실패
        return False, f'{type(e).__name__}: {e}', {}
    return True, f'{len(tv["cases"])} 케이스 · 기대 세대 {tv.get("expected_generation")!r} · 검사 {tv.get("same_generation_checks")}', \
        {c: r['cells'] for c, r in tv['cases'].items()}


def _link_dir(src, dst):
    """폴더 링크 — symlink · 안 되면 (Windows 권한 WinError 1314 등) 하드링크 사본 · 그것도 안 되면 사본.  읽기 전용 대조라 셋 다 같은 바이트를 본다
    (Codex 재검증 2 §11 — Windows 에서 symlink fixture 가 selftest 를 세웠다)."""
    try:
        os.symlink(src, dst)
        return 'symlink'
    except (OSError, NotImplementedError):
        pass
    try:
        shutil.copytree(src, dst, copy_function=os.link)
        return 'hardlink'
    except OSError:
        shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst)
    return 'copy'


def synth_batch(cd, LWB, tmp: Path):
    """폴더 하나 → 한 케이스 배치 기록 (status.json · metrics_flat.csv) + results/<case> 링크 — smoke · case-dir 의 H1 용 (⚠ P1 · P3 자기 대조)."""
    cd = Path(cd).resolve()
    fm = _read_json(cd / 'full_metrics.json') or {}
    res = tmp / 'results'
    res.mkdir(parents=True, exist_ok=True)
    link = res / cd.name
    if not link.exists():
        _link_dir(cd, link)
    st = dict(schema=LWB.SCHEMA, stop_after='network', harvest_dir='', cohort='', runs=[],
              cases={cd.name: dict(case=cd.name, stop_after='network', status='done', failed_stages=[], network_run_id=fm.get('network_run_id'))})
    rows = {cd.name: dict({k: v for k, v in fm.items() if not isinstance(v, (dict, list))}, case=cd.name)}
    LWB.write_outputs(tmp / 'batch', st, rows)
    return res, tmp / 'batch'


def _cells_match(rc, cells):
    return bool(cells) and rc == cells


def run_smoke_or_dirs(folders, expected, *, out=print):
    ps, tf, LDD, LWB = _mods()
    reports = []
    for cd in folders:
        rep = reread_case(cd, expected, ps, tf)
        tmp = Path(tempfile.mkdtemp(prefix='g2rr_'))
        try:
            res, bdir = synth_batch(cd, LWB, tmp)
            ok, why, cells = handover_gate(res, LDD.load_webapp(bdir), expected, LDD)
            same = _cells_match(rep.get('row_cells'), cells.get(Path(cd).resolve().name))
            rep['checks'].append(dict(name='H1 인계 출처 관문 (load_tau_results · 기대 세대 · 폴더에서 만든 한 케이스 배치 기록 = synth_batch · P1 · P3 자기 대조)',
                                      ok=ok and same, detail=(why if not ok else f'{why} · 칸 = case_row {same}')[:900]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        rep['batch'] = 'synth_batch'
        reports.append(rep)
    return reports


def _np():
    """194 실행기 모듈 (계획 꼴 · ID 지문 · 등록 집합 — 같은 함수 · 사본 금지)."""
    import run_network_194_parallel as NP
    return NP


def registered_expected(name):
    """★ 10-07 G2RR2-02 — 등록 집합 이름 → dict(name, pairs, source) (`run_network_194_parallel.registered_id_set` — production194 = 등록 ID 지문 ·
    pilot3 = 시범 세 케이스)."""
    return _np().registered_id_set(name)


def explicit_expected(specs):
    """'코호트:케이스' 목록 → 명시 등록 집합 (중복 · 꼴 오류 = ValueError)."""
    pairs = []
    for s in specs:
        coh, _, case = str(s).partition(':')
        if not coh or not case:
            raise ValueError(f'--expect-case {s!r} — 코호트:케이스 꼴이어야')
        pairs.append((case, coh))
    if len(set(pairs)) != len(pairs):
        raise ValueError(f'--expect-case 중복 {sorted({p for p in pairs if pairs.count(p) > 1})}')
    return dict(name='explicit', pairs=frozenset(pairs), source='CLI --expect-case')


def launcher_identity(root: Path, raw, man) -> dict:
    """★ 10-07 G2RR3-01 — 판정 JSON 의 실행 신원 (IDENTITY_KEYS): 읽은 ROOT (resolve) · 판정에 쓴 manifest 바이트의 sha256 · 그 manifest 의 발사 봉인 지문
    (seal.code_fp) · 발사 sha (git.sha).  못 읽은 값 = None (기록만 — 판정은 v1.3 배포 관문이 배치 뿌리와 맞대어 한다)."""
    m = man if isinstance(man, dict) else {}
    s = m.get('seal') if isinstance(m.get('seal'), dict) else {}
    g = m.get('git') if isinstance(m.get('git'), dict) else {}
    return dict(launcher_root=str(Path(root).resolve()), manifest_sha256=(hashlib.sha256(raw).hexdigest() if raw is not None else None),
                seal_fp=s.get('code_fp'), launch_sha=g.get('sha'))


def run_launcher(root: Path, *, expected=None, out=print, identity=None):
    """launcher-root — manifest 기대 세대 · ★ 등록 집합 (G2RR2-02) · 코호트별 진짜 배치 기록 · 케이스별 K1–K7 · 코호트별 H1.
    ★ 10-07 G2RR2-02 (Codex 세대 2 재검증 2 §3) — 옛 판은 `cohorts or []` 루프 안에서만 M1 을 봐서 plan · cohorts 를 지우거나 비우면 0 케이스를 읽고 실패 0 =
    rc 0 이었다.  이제 ① 루프 **전에** manifest · plan · cohorts · queue 의 꼴 (비지 않음 · 중복 · 코호트 소속 — 실행기와 같은 `plan_problems`) ②
    계획 큐 = **등록 집합** (expected — 고칠 수 있는 큐를 자기 자신의 기대 집합으로 쓰지 않는다) ③ 루프 **밖에서** 실제로 읽은 고유 (케이스, 코호트)
    집합 = 등록 집합 (M3 · 기대 수 · 읽은 수 · 빠진 · 남는).  expected 가 없으면 FAIL (등록 모드 필수).
    ★ 10-07 G2RR3-01 — identity (dict · 주면 채운다) = `launcher_identity` — manifest 를 **한 번** 바이트로 읽어 그 바이트를 해시하고 해석한다 (판정에 쓴
    manifest 와 기록한 sha256 이 같은 바이트)."""
    ps, tf, LDD, LWB = _mods()
    try:
        raw = (root / 'manifest.json').read_bytes()
    except OSError:
        raw = None
    try:
        man = json.loads(raw.decode('utf-8')) if raw is not None else None
    except ValueError:                                           # UnicodeDecodeError · JSONDecodeError
        man = None
    if identity is not None:
        identity.update(launcher_identity(root, raw, man))
    meta = []
    if not isinstance(man, dict):
        return [], [dict(name='M0 manifest', ok=False, detail=f'{root}/manifest.json 없음 · 못 읽음')], None
    try:
        exp = LDD.tau_manifest_expected_generation(man)
        meta.append(dict(name=f'M0 manifest 기대 세대 선언 ({LDD.TAU_MANIFEST_GENERATION_KEY})', ok=True, detail=exp))
    except Exception as e:                                       # noqa: BLE001
        exp = None
        meta.append(dict(name=f'M0 manifest 기대 세대 선언 ({LDD.TAU_MANIFEST_GENERATION_KEY})', ok=False, detail=f'{type(e).__name__}: {e}'))
    want = exp or tf.NET_GEN_G2                                  # 케이스 판정은 g2 로 계속 (정보) — H1 은 선언이 있어야 통과
    exp_pairs = frozenset((expected or {}).get('pairs') or ())
    exp_name = (expected or {}).get('name')
    if not exp_pairs:
        meta.append(dict(name='M-reg 등록 집합', ok=False, detail='등록 집합이 없다 (--expect-set · --expect-case) — 계획 큐를 자기 자신의 기대 집합으로 쓰지 않는다'))
    #  ① 루프 전 — 꼴 (실행기와 같은 함수)
    pp = _np().plan_problems(man.get('plan'))
    meta.append(dict(name='M-plan manifest plan · cohorts · queue 꼴 (비지 않음 · 중복 · 코호트 소속 — 루프 전)', ok=not pp, detail=' · '.join(pp)[:900]))
    reports = []
    read = set()
    if not pp:
        plan = man['plan']
        planned_pairs = frozenset((e['case'], e['cohort']) for e in plan['queue'])
        if exp_pairs:
            ec = {h for _c, h in exp_pairs}
            meta.append(dict(name=f'M-reg 계획 큐 = 등록 집합 {exp_name} ({len(exp_pairs)})', ok=planned_pairs == exp_pairs,
                             detail=(f'등록에만 {sorted(exp_pairs - planned_pairs)[:5]} · 계획에만 {sorted(planned_pairs - exp_pairs)[:5]} · '
                                     f'등록 밖 코호트 {sorted({c["name"] for c in plan["cohorts"]} - ec)}')))
        for cs in plan['cohorts']:
            name = cs['name']
            mdir = root / 'merged' / name
            planned = sorted(e['case'] for e in plan['queue'] if e['cohort'] == name)
            try:
                wv = LDD.load_webapp(mdir)
            except Exception as e:                               # noqa: BLE001
                meta.append(dict(name=f'M1 {name} 배치 기록', ok=False, detail=f'{type(e).__name__}: {e}'))
                continue
            st = wv.get('status') or {}
            meta.append(dict(name=f'M1 {name} 케이스 집합 — 계획 큐 = 배치 기록 ({len(planned)})', ok=sorted(st) == planned,
                             detail=f'계획에만 {sorted(set(planned) - set(st))[:5]} · 기록에만 {sorted(set(st) - set(planned))[:5]}'))
            notdone = {c: (r or {}).get('status') for c, r in st.items() if (r or {}).get('status') not in LDD.WA_OK_STATUS}
            meta.append(dict(name=f'M2 {name} 전 케이스 done · partial', ok=not notdone, detail=notdone))
            for c in sorted(st):
                if c in notdone:
                    continue
                rep = reread_case(mdir / 'results' / c, want, ps, tf)
                rep['cohort'] = name
                rep['batch'] = 'launcher'
                read.add((c, name))
                if (st[c] or {}).get('network_run_id') != rep.get('run_id'):
                    rep['checks'].append(dict(name='K1b 배치 기록 run id = 폴더 run id', ok=False,
                                              detail=f"{(st[c] or {}).get('network_run_id')!r} ≠ {rep.get('run_id')!r}"))
                reports.append(rep)
            if exp is None:
                meta.append(dict(name=f'H1 {name} 인계 출처 관문 (기대 세대 교차 대조)', ok=False, detail='manifest 에 기대 세대 선언이 없어 교차 대조를 못 한다'))
                continue
            ok, why, cells = handover_gate(mdir / 'results', wv, exp, LDD)
            bad = [r['case'] for r in reports if r.get('cohort') == name and not _cells_match(r.get('row_cells'), cells.get(r['case']))] if ok else []
            meta.append(dict(name=f'H1 {name} 인계 출처 관문 (load_tau_results · P0–P4 · manifest 기대 세대 {exp!r}) · 칸 = case_row', ok=ok and not bad,
                             detail=(why if not ok else f'{why} · 칸 다름 {bad[:5]}')[:900]))
    #  ③ 루프 밖 — 실제로 읽은 고유 집합 = 등록 집합 (0 케이스 · 일부 코호트만 읽은 성공을 막는다)
    meta.append(dict(name=f'M3 읽은 고유 (케이스, 코호트) = 등록 집합 {exp_name} — 기대 {len(exp_pairs)} · 읽음 {len(read)}',
                     ok=bool(exp_pairs) and read == exp_pairs,
                     detail=f'빠진 {sorted(exp_pairs - read)[:5]} · 남는 {sorted(read - exp_pairs)[:5]}',
                     expected_n=len(exp_pairs), read_n=len(read), set_equal=bool(exp_pairs) and read == exp_pairs,
                     missing=sorted(exp_pairs - read), extra=sorted(read - exp_pairs)))
    return reports, meta, exp


def check_id(name):
    """검사 이름 → ID (첫 낱말) — 'K1 게시 — …' → 'K1' · 'M1 lhs 케이스 집합 …' → 'M1'.  비지 않은 문자열이 아니면 None."""
    return name.split(' ', 1)[0] if isinstance(name, str) and name.strip() else None


def _entry_ok_shape(e):
    """검사 항목 꼴 — dict · name 비지 않은 문자열 · ok **bool** (정수 1 · 문자열 'True' 를 통과로 읽지 않는다)."""
    return isinstance(e, dict) and isinstance(e.get('name'), str) and bool(e['name'].strip()) and isinstance(e.get('ok'), bool)


def launcher_detail_problems(rec, expected_pairs) -> list:
    """★ 10-07 G2RR4-01 (Codex 세대 2 재검증 4 §2 최소 해결 ① ②) — launcher-root 판정 JSON 의 상세 (meta · cases · checks) ↔ 요약 (n_fail · read_n · M3 칸) 대조
    → 문제 목록 ([] = 통과).  expected_pairs = 등록 집합 {(케이스, 코호트)} (`registered_expected(name)['pairs']`).  v1.3 배포 관문이 이 함수를 부른다 (사본 금지).
      ① meta = 목록 · 항목마다 name 문자열 · ok bool · LAUNCHER_META_IDS 각 한 번 · 등록 코호트마다 LAUNCHER_COHORT_META_IDS 각 한 번 · 그 밖 ID · 코호트 = 모르는 검사
      ② cases = 목록 · 항목마다 case · cohort 문자열 · checks 목록 · 검사마다 name 문자열 · ok bool · CASE_CHECK_IDS 각 한 번 (빈 checks 의 공집합 PASS 금지) ·
         CASE_CHECK_EXTRA 는 한 번까지 · 그 밖 ID = 모르는 검사
      ③ 상세 실패 (ok 가 True 가 아닌 meta · 케이스 검사 — 꼴이 깨진 것 포함) 재계수 = n_fail · 상세 실패가 있으면 문제 (전부 통과여야)
      ④ 상세 (케이스, 코호트) 중복 없음 · 고유 집합 = 등록 집합 · 상세 케이스 수 = read_n · M3 항목의 기대 · 읽은 수 · 같음 · 빠진 · 남는 = 최상위 칸
    한정: 같은 JSON 안의 상세 ↔ 요약 대조다 — 상세 · 요약 · 사본을 함께 바꾼 전면 위조는 재계산 없이 못 잡는다 (모듈 docstring '한계' 그대로)."""
    if not isinstance(rec, dict):
        return [f'판정 JSON 이 객체가 아니다 ({type(rec).__name__})']
    exp = {(str(c), str(h)) for c, h in (expected_pairs or ())}
    if not exp:
        return ['등록 집합이 비었다 — 상세를 대조할 기준이 없다']
    cohorts = sorted({h for _c, h in exp})
    p, fails = [], []
    meta = rec.get('meta')
    if not isinstance(meta, list):
        p.append(f'meta {type(meta).__name__} — 목록이 아니다 (상세 결손)')
        meta = []
    cnt, bad_shape, unknown = collections.Counter(), [], []
    for i, m in enumerate(meta):
        if not (isinstance(m, dict) and m.get('ok') is True):
            fails.append(str((m or {}).get('name') if isinstance(m, dict) else m)[:80])
        if not _entry_ok_shape(m):
            bad_shape.append(f'meta[{i}] {str(m)[:100]}')
            continue
        mid = check_id(m['name'])
        if mid in LAUNCHER_META_IDS:
            cnt[(mid, None)] += 1
        elif mid in LAUNCHER_COHORT_META_IDS:
            parts = m['name'].split(' ', 2)
            coh = parts[1] if len(parts) > 1 else None
            if coh not in cohorts:
                unknown.append(f'{mid} 코호트 {coh!r} (등록 코호트 {cohorts} 밖)')
            cnt[(mid, coh)] += 1
        else:
            unknown.append(f'{mid!r} ({m["name"][:50]!r})')
    want = [(mid, None) for mid in LAUNCHER_META_IDS] + [(mid, coh) for coh in cohorts for mid in LAUNCHER_COHORT_META_IDS]
    off = {(f'{mid} {coh}' if coh else mid): cnt[(mid, coh)] for mid, coh in want if cnt[(mid, coh)] != 1}
    if off:
        p.append(f'meta 검사 ID 가 한 번씩이 아니다 {off} — 상세 계약: {" · ".join(LAUNCHER_META_IDS)} 한 번 + 코호트 {cohorts} 마다 '
                 f'{" · ".join(LAUNCHER_COHORT_META_IDS)} 한 번')
    cases = rec.get('cases')
    if not isinstance(cases, list):
        p.append(f'cases {type(cases).__name__} — 목록이 아니다 (상세 결손)')
        cases = []
    pairs, bad_ids = [], []
    for i, c in enumerate(cases):
        if not (isinstance(c, dict) and isinstance(c.get('case'), str) and isinstance(c.get('cohort'), str) and isinstance(c.get('checks'), list)):
            bad_shape.append(f'cases[{i}] {str(c)[:100]}')
            fails.append(f'cases[{i}] (꼴)')
            continue
        pairs.append((c['case'], c['cohort']))
        cc = collections.Counter()
        for j, k in enumerate(c['checks']):
            if not (isinstance(k, dict) and k.get('ok') is True):
                fails.append(f'{c["case"]}: {str(k.get("name") if isinstance(k, dict) else k)[:60]}')
            if not _entry_ok_shape(k):
                bad_shape.append(f'{c["case"]} checks[{j}] {str(k)[:80]}')
                continue
            kid = check_id(k['name'])
            if kid not in CASE_CHECK_IDS + CASE_CHECK_EXTRA:
                unknown.append(f'{c["case"]} {kid!r}')
            cc[kid] += 1
        miss = {x: cc[x] for x in CASE_CHECK_IDS if cc[x] != 1}
        miss.update({x: cc[x] for x in CASE_CHECK_EXTRA if cc[x] > 1})
        if miss:
            bad_ids.append((c['case'], miss))
    if bad_shape:
        p.append(f'검사 항목 꼴 {len(bad_shape)} — name 문자열 · ok bool (정수 · 문자열 ok 를 통과로 읽지 않는다) · cases 는 case · cohort · checks 목록 · 첫 {bad_shape[:3]}')
    if unknown:
        p.append(f'모르는 검사 {len(unknown)} — 상세 계약 (LAUNCHER_META_IDS · LAUNCHER_COHORT_META_IDS · CASE_CHECK_IDS) 밖 · 첫 {unknown[:3]}')
    if bad_ids:
        p.append(f'케이스 {len(bad_ids)} 에서 검사 ID 가 한 번씩이 아니다 — 케이스마다 {"·".join(CASE_CHECK_IDS)} 한 번씩 (빈 checks = 공집합 PASS 금지) · 첫 {bad_ids[:3]}')
    nf = rec.get('n_fail')
    if isinstance(nf, int) and not isinstance(nf, bool) and nf != len(fails):
        p.append(f'상세 실패 재계수 {len(fails)} ≠ n_fail {nf} — 요약이 상세를 덮는다 (또는 상세가 요약을 뒷받침하지 않는다)')
    if fails:
        p.append(f'상세 실패 {len(fails)} — 첫 {fails[:4]} (전부 통과여야)')
    pc = collections.Counter(pairs)
    dup = sorted(x for x, n in pc.items() if n > 1)
    if dup:
        p.append(f'상세 (케이스, 코호트) 중복 {len(dup)} — 첫 {dup[:3]} (한 번씩이어야)')
    got = set(pc)
    if got != exp:
        p.append(f'상세 (케이스, 코호트) 고유 {len(got)} ≠ 등록 집합 {rec.get("expected_set")!r} ({len(exp)}) — 빠진 {sorted(exp - got)[:3]} · 남는 {sorted(got - exp)[:3]}')
    if len(cases) != rec.get('read_n'):
        p.append(f'상세 케이스 {len(cases)} ≠ read_n {rec.get("read_n")!r} — 읽었다는 수를 상세가 뒷받침하지 않는다')
    m3 = [m for m in meta if _entry_ok_shape(m) and check_id(m['name']) == 'M3']
    if len(m3) == 1:
        d3 = {k: (m3[0].get(k), rec.get(k)) for k in M3_SUMMARY_KEYS if m3[0].get(k) != rec.get(k)}
        if d3:
            p.append(f'M3 항목 ↔ 최상위 요약 다름 {str(d3)[:200]} — 요약이 M3 상세와 어긋난다')
    return p


def summarize(reports, meta, *, out=print):
    n_bad = 0
    for m_ in meta:
        out(f'  {"✓" if m_["ok"] else "✗"} {m_["name"]}' + ('' if m_['ok'] else f'  — {m_["detail"]}'))
        n_bad += not m_['ok']
    for r in reports:
        bad = [c for c in r['checks'] if not c['ok']]
        n_bad += len(bad)
        st = r.get('statuses') or {}
        tb = r.get('table') or {}
        diag = {m: {b: ((tb.get(m) or {}).get(b) or {}).get('status') for b in ('bulk_only', 'constriction_only')} for m in tb if tb.get(m)}
        out(f'  {"✓" if not bad else "✗"} {r.get("cohort", "")} {r["case"]} — 세대 {r.get("generation")!r} · '
            f'τ {({m: v[0] for m, v in st.items()})} · σ_ratio {r.get("sigma_ratio")} · CF/협착 {diag}')
        for c in bad:
            out(f'      ✗ {c["name"]} — {c["detail"][:400]}')
    return n_bad


def _parse(argv=None):
    ap = argparse.ArgumentParser(description='세대 2 망 게시 다시 읽기 (읽기 전용 · Codex 세대 2 재검증 §7-4)')
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--smoke-root', default='', help='wsl_network_smoke.py ROOT (망 정지 케이스)')
    g.add_argument('--launcher-root', default='', help='run_network_194_parallel.py ROOT (manifest 기대 세대 · merged 배치 기록)')
    g.add_argument('--case-dir', action='append', default=[], help='케이스 폴더 (여러 번)')
    g.add_argument('--selftest', action='store_true', help='합성 침대 (실 생산자 CLI 게시) 로 양성 · 음성 대조')
    ap.add_argument('--expect-generation', default='g2', help='smoke-root · case-dir 의 기대 세대 (기본 g2 · launcher-root 는 manifest 선언)')
    ap.add_argument('--expect-set', default='', help='launcher-root 의 등록 집합 이름 (production194 · pilot3 — G2RR2-02 · 등록 모드 필수)')
    ap.add_argument('--expect-case', action='append', default=[],
                    help='launcher-root 의 명시 등록 집합 — 코호트:케이스 (여러 번 · --expect-set 대신)')
    ap.add_argument('--json', default='', help='판정 JSON 을 쓸 곳')
    return ap.parse_args(argv)


def main(argv=None) -> int:
    a = _parse(argv)
    if a.selftest:
        return _selftest()
    meta, exp = [], a.expect_generation
    expected = None
    ident = dict.fromkeys(IDENTITY_KEYS)                         # ★ G2RR3-01 — launcher-root 일 때만 채운다 (그 밖 = null · 배포 관문이 받지 않는다)
    if a.launcher_root:
        #  ★ 10-07 G2RR2-02 — 등록 모드 필수 (생산 194 · 시범의 정확한 ID) — 계획 큐를 자기 자신의 기대 집합으로 쓰지 않는다
        if bool(a.expect_set) == bool(a.expect_case):
            print('⛔ --launcher-root 는 등록 집합이 필요하다 — --expect-set (production194 · pilot3) 또는 --expect-case 코호트:케이스 (여러 번) 중 하나만',
                  file=sys.stderr)
            return 2
        try:
            expected = registered_expected(a.expect_set) if a.expect_set else explicit_expected(a.expect_case)
        except Exception as e:                                   # noqa: BLE001 — 등록 집합을 못 세우면 판정하지 않는다
            print(f'⛔ 등록 집합 — {type(e).__name__}: {e}', file=sys.stderr)
            return 2
    elif a.expect_set or a.expect_case:
        print('⛔ --expect-set · --expect-case 는 --launcher-root 에만', file=sys.stderr)
        return 2
    if a.smoke_root:
        sr = Path(a.smoke_root).expanduser().resolve()
        rep = _read_json(sr / 'smoke_report.json') or {}
        reps = rep.get('reports') if isinstance(rep.get('reports'), dict) else {}
        ids_all = [cid for cid, r in reps.items() if isinstance(r, dict) and r.get('stop_after') == 'network']
        #  ★ 10-07 G2RR4-03 (Codex 세대 2 재검증 4 §6-3(b)) — 스모크 음성 대조 (case15 게시 차단 기대) 는 S0 (게시 done) 에서 빼고 S0b 로 · 음성 대조 폴더는 K1–K7 로
        #    다시 읽지 않는다 (게시가 없다) · 표지 없는 failed 는 S0 실패 그대로 (이름으로 면제하지 않는다).
        #  ★ 10-08 G2RR5-03 (Codex 세대 2 재검증 5 §3) — 옛 판은 truthy 표지면 종류를 가리지 않고 빼고 '<id>: [음성 대조]' 접두어 PASS 행 넷 이상만 셌다 (한 행 네 번 ·
        #    미등록 표지 · 상세 결손 · 실제 원자료 SHA FAIL 이 통과).  이제 ① **등록** 표지 ∧ 케이스 신원 (`case15_negctl_registered` — case15_network · kind
        #    case15 · 망 정지) 일 때만 뺀다 — 그 밖 truthy 표지 = 미등록 → S0 실패 + S0b 문제 ② 기록된 그 케이스 검사 = 등록 안정 ID 집합 정확히 (각 1 회 · 모르는 ·
        #    id 없는 행 거부) · 전부 PASS ③ 공용 판정 (`case15_negctl_verdicts`) 을 보고 상세 · 자식 프로세스 기록 (timings) 에 다시 돌린 판정 = 기록 ④ 필수 ID 에
        #    자식 프로세스 · 원자료 sha256 · 실제 망 시도 (G2RR5-02) ⑤ 게시 없음 — `case15_negctl_s0b_problems`.  숫자 넷을 바꾸거나 실패 케이스를 면제하지 않는다.
        marked = sorted(cid for cid, r in reps.items() if isinstance(r, dict) and r.get('negative_control'))
        neg = [cid for cid in marked if case15_negctl_registered(cid, reps[cid])]
        unreg = [cid for cid in marked if cid not in neg]
        ids = [cid for cid in ids_all if cid not in neg]
        notdone = {cid: reps[cid].get('status') for cid in ids if reps[cid].get('status') != 'done'}
        meta.append(dict(name=f'S0 스모크 망 정지 케이스 전부 done ({len(ids)} · 등록 음성 대조 {len(neg)} 제외 · 미등록 음성 대조 표지 {len(unreg)})',
                         ok=bool(ids) and not notdone and not unreg,
                         detail=(dict(notdone, **({'미등록 음성 대조 표지': unreg} if unreg else {})) or ids)))
        if marked:
            ng = CASE15_NEGCTL
            tm = rep.get('timings') if isinstance(rep.get('timings'), dict) else {}
            nbad = {cid: [f'미등록 음성 대조 표지 {reps[cid].get("negative_control")!r} (kind {reps[cid].get("kind")!r} · stop_after {reps[cid].get("stop_after")!r}) — '
                          f'S0 에서 빼지 않는다 (등록 = 표지 {ng["tag"]!r} · {ng["case_id"]} · kind {ng["kind"]} · stop_after {ng["stop_after"]})']
                    for cid in unreg}
            for cid in neg:
                why = case15_negctl_s0b_problems(cid, reps[cid], rep.get('checks'), tm.get(cid))
                if why:
                    nbad[cid] = why
            meta.append(dict(name=f'S0b 스모크 음성 대조 (등록 {len(neg)} · 미등록 {len(unreg)}) = 게시 없음 · 기록된 검사 = 등록 안정 ID {len(CASE15_NEGCTL_IDS)} 개 '
                                  '(각 1 회 · 전부 PASS) · 공용 판정 재계산 = 기록 (자식 프로세스 · 원자료 sha256 · 원인 · 이온 · 실제 망 시도 — G2RR5-02 · 03)',
                             ok=not nbad, detail=nbad or neg))
        folders = [sr / 'work' / 'results' / cid for cid in ids if cid not in notdone]
        reports = run_smoke_or_dirs(folders, exp)
    elif a.launcher_root:
        reports, meta, exp = run_launcher(Path(a.launcher_root).expanduser().resolve(), expected=expected, identity=ident)
    elif a.case_dir:
        reports = run_smoke_or_dirs([Path(p).expanduser().resolve() for p in a.case_dir], exp)
    else:
        print('⛔ --smoke-root · --launcher-root · --case-dir · --selftest 중 하나', file=sys.stderr)
        return 2
    m3 = next((m_ for m_ in meta if m_.get('name', '').startswith('M3')), {})
    print(f'══ 세대 2 망 게시 다시 읽기 — 기대 세대 {exp!r} · 케이스 {len(reports)}'
          + (f' · 등록 집합 {expected["name"]} 기대 {m3.get("expected_n")} · 읽음 {m3.get("read_n")} · 같음 {m3.get("set_equal")}' if expected else ''))
    n_bad = summarize(reports, meta)
    print(f'  {"✓ 전부 통과" if not n_bad else f"✗ {n_bad} 건 실패"}')
    if a.json:
        p = Path(a.json).expanduser()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(dict(schema=SCHEMA, expected_generation=exp, meta=meta, cases=reports, n_fail=n_bad,
                                     expected_set=(expected or {}).get('name'), expected_source=(expected or {}).get('source'),
                                     expected_n=m3.get('expected_n'), read_n=m3.get('read_n'), set_equal=m3.get('set_equal'),
                                     missing=m3.get('missing'), extra=m3.get('extra'), **ident),
                                ensure_ascii=False, indent=1, default=str) + '\n', encoding='utf-8')
    return 0 if not n_bad else 1


# ─────────────────────────────── selftest (합성 침대 · 실 생산자 CLI 게시) ───────────────────────────────
def _selftest() -> int:
    """실 생산자 → 게시 (`test_gen2_publication_handover._publish` — 실 network CLI · 실 `_network_and_stage_e`) 로 만든 폴더를 다시 읽는다.
      양성: 관통 (through) · 정상 비관통 (nonthrough) · GEN2-01 (clamp — physics · H12 협착-only not_computed) · launcher-root 모양 (manifest 선언 g2)
      음성: 증서 자리 바꿔치기 (CF → FULL · 강제 폴더) → K2 · H1 · 도장 네 값 null → K3 · H1 · manifest 기대 세대 없음 → M0 · H1 · 기대 세대 inferred_legacy → H1"""
    fails = []

    def chk(name, ok, why=''):
        print(('  ✓ ' if ok else '  ✗ ') + name + ('' if ok or not why else f'  — {str(why)[:300]}'))
        if not ok:
            fails.append(name)
    sys.path.insert(0, str(ROOT / 'webapp'))
    import app                                                   # noqa: E402
    import test_gen2_publication_handover as PH                  # noqa: E402  (실 생산자 게시 · 강제 폴더 — 같은 도구)
    ps, tf, LDD, LWB = _mods()
    made, tmp = [], Path(tempfile.mkdtemp(prefix='g2rr_st_')).resolve()
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            pub = {bed: PH._publish(app, 'baseline', bed=bed) for bed in ('through', 'nonthrough', 'clamp')}
        made += [v[0] for v in pub.values()]
        chk('게시 셋 done (실 생산자 CLI → 정지 계약 → 게시)', all(v[1] == 'done' for v in pub.values()), {k: (v[1], v[2]) for k, v in pub.items()})
        res = {}
        for bed, (d, _st, _f, _rid) in pub.items():
            dst = tmp / f'case_{bed}'
            shutil.copytree(d, dst)
            res[bed] = run_smoke_or_dirs([dst], 'g2')[0]
        okp = {bed: all(c['ok'] for c in r['checks']) for bed, r in res.items()}
        chk(f'양성 — 관통 · 비관통 · GEN2-01 폴더 K1–K7 · H1 전부 통과 {okp}', all(okp.values()),
            {b: [c for c in r['checks'] if not c['ok']][:2] for b, r in res.items()})
        st_nt = res['nonthrough']['statuses']
        chk('비관통 — τ 세 모드 NOT_PERCOLATING · 가지 셋 valid_zero (숫자 없음)',
            all(v[0] == 'NOT_PERCOLATING' for v in st_nt.values())
            and all(d['status'] == 'valid_zero' and d['value'] is None for m in res['nonthrough']['table'].values() if m for d in m.values()), st_nt)
        tc = res['clamp']['table']
        chk('GEN2-01 — physics · H12 협착-only = not_computed zero_resistance_requires_contraction · FULL · CF computed (숫자 · 증서)',
            all(tc[m]['constriction_only']['status'] == 'not_computed'
                and tc[m]['constriction_only']['reason'] == 'zero_resistance_requires_contraction' for m in ('physics', 'hertz_h12'))
            and all(tc[m][b]['status'] == 'computed' and (tc[m][b]['cert'] or {}).get('branch') == b for m in tc for b in ('full', 'bulk_only')),
            {m: {b: (d['status'], d['reason']) for b, d in r.items()} for m, r in tc.items()})
        base, rid = pub['through'][0], pub['through'][3]
        f_cf = PH._force(app, base, rid, 'full_cert_from_cf', tmp / 'forced_cf', stamp='keep')
        r_cf = run_smoke_or_dirs([f_cf], 'g2')[0]
        bad_cf = {c['name'][:2] for c in r_cf['checks'] if not c['ok']}
        chk(f'음성 — 증서 자리 바꿔치기 (CF → FULL · 네 사본 · 도장 그대로) → K2 · H1 실패 {sorted(bad_cf)}', {'K2', 'H1'} <= bad_cf)
        f_null = tmp / 'stamp_null'
        shutil.copytree(base, f_null)
        pv = json.loads((f_null / ps.PROVENANCE_FILE).read_text(encoding='utf-8'))
        pv.update({k: None for k in ps.PROVENANCE_GENERATION_KEYS})
        (f_null / ps.PROVENANCE_FILE).write_text(json.dumps(pv), encoding='utf-8')
        r_null = run_smoke_or_dirs([f_null], 'g2')[0]
        bad_null = {c['name'][:2] for c in r_null['checks'] if not c['ok']}
        chk(f'음성 — 도장 네 세대 값 null (Codex all_null) → K3 · H1 실패 {sorted(bad_null)}', {'K3', 'H1'} <= bad_null)
        r_leg = run_smoke_or_dirs([tmp / 'case_through'], 'inferred_legacy')[0]
        bad_leg = {c['name'][:2] for c in r_leg['checks'] if not c['ok']}
        chk(f'음성 — 기대 세대 inferred_legacy 로 g2 폴더를 읽으면 K2 · K5 · H1 실패 {sorted(bad_leg)}', {'K2', 'K5', 'H1'} <= bad_leg)
        #  launcher-root 모양 — manifest (기대 세대 선언 · 계획) + merged/<코호트> (진짜 배치 기록 모양) + results 링크 (link=True 면 같은 게시 폴더로 symlink)
        def _lroot(name, cohort_cases, decl=None, link=False):
            lr = tmp / f'lroot_{name}'
            plan_q, cohorts = [], []
            for coh, cl in cohort_cases.items():
                mres = lr / 'merged' / coh / 'results'
                mres.mkdir(parents=True)
                cases, rows = {}, {}
                for c, bed in cl:
                    if link:
                        _link_dir(tmp / f'case_{bed}', mres / c)
                    else:
                        shutil.copytree(tmp / f'case_{bed}', mres / c)
                    fm = _read_json(mres / c / 'full_metrics.json') or {}
                    cases[c] = dict(case=c, stop_after='network', status='done', failed_stages=[], network_run_id=fm.get('network_run_id'))
                    rows[c] = dict({k: v for k, v in fm.items() if not isinstance(v, (dict, list))}, case=c)
                    plan_q.append(dict(case=c, cohort=coh))
                LWB.write_outputs(lr / 'merged' / coh, dict(schema=LWB.SCHEMA, stop_after='network', harvest_dir='', cohort='', runs=[], cases=cases), rows)
                cohorts.append(dict(name=coh))
            #  실행 신원 (★ G2RR3-01) — 발사 봉인 지문 = code_hashes 의 지문 (실행기 code_fp) · 발사 sha (합성)
            ch_ = {'scripts/tau_flux.py': hashlib.sha256((ROOT / 'scripts' / 'tau_flux.py').read_bytes()).hexdigest()}
            man = dict(schema='network_parallel_launcher/v1', plan=dict(cohorts=cohorts, queue=plan_q), code_hashes=ch_,
                       seal=dict(schema='launch_seal/v3', code_fp=_np().code_fp(ch_)), git=dict(sha='ab' * 20),
                       **({'expected_network_generation': 'g2'} if decl is None else decl))
            (lr / 'manifest.json').write_text(json.dumps(man), encoding='utf-8')
            return lr, man

        def _run_l(lr, expected):
            """run_launcher(lr, expected=…) — ★ G2RR2-02 등록 모드.  옛 코드 (expected 인자 없음) 는 등록 없이 돈다 (반례가 옛 판에서 어떻게 통과하는지 본다)."""
            try:
                return run_launcher(lr, expected=expected)
            except TypeError:
                return run_launcher(lr)

        def _ok_all(reps, meta):
            return all(m_['ok'] for m_ in meta) and all(c['ok'] for r in reps for c in r['checks'])
        _rid = getattr(sys.modules.get(__name__), 'registered_expected', None)
        two = {'lhs': [('lhs99_through', 'through'), ('lhs99_nonthrough', 'nonthrough')]}
        exp_two = dict(name='explicit', pairs=frozenset({('lhs99_through', 'lhs'), ('lhs99_nonthrough', 'lhs')}), source='selftest')
        for label, decl in (('declared', None), ('undeclared', {})):
            lr, _m = _lroot(label, two, decl)
            reps, meta, exp = _run_l(lr, exp_two)
            okl = _ok_all(reps, meta)
            if label == 'declared':
                chk(f'launcher-root 양성 — manifest 선언 g2 · 두 케이스 K1–K7 · 코호트 H1 통과 (exp {exp!r})', okl and exp == 'g2' and len(reps) == 2,
                    [m_ for m_ in meta if not m_['ok']] + [c for r in reps for c in r['checks'] if not c['ok']])
            else:
                badm = {m_['name'][:2] for m_ in meta if not m_['ok']}
                chk(f'launcher-root 음성 — manifest 기대 세대 선언 없음 (194 v1.2 런처 모양) → M0 · H1 실패 {sorted(badm)}', {'M0', 'H1'} <= badm)

        #  ★ 10-07 G2RR2-02 (Codex 세대 2 재검증 2 §3) — 0 케이스 PASS · 등록 집합 · 루프 전 꼴 검사 · 루프 밖 집합 대조 (반례 먼저)
        p3 = {'lhs': [('lhs00_055', 'through'), ('lhs00_128', 'nonthrough')], 'lhsx': [('lhsx_007', 'clamp')]}
        try:
            exp_p3 = _rid('pilot3') if _rid else None
        except Exception as e:                                   # noqa: BLE001
            exp_p3 = None
            print(f'  (등록 집합 pilot3 못 읽음: {type(e).__name__}: {e})')
        lr_p3, m_p3 = _lroot('pilot3', p3)
        reps, meta, exp = _run_l(lr_p3, exp_p3)
        m3 = next((m_ for m_ in meta if m_['name'].startswith('M3')), {})
        chk(f'★ 등록 집합 양성 pilot3 (lhs00_055 · lhs00_128 · lhsx_007) — 두 코호트 · 세 케이스 K1–K7 · H1 통과 · 기대 3 = 읽음 3 (M3 집합 대조) {m3.get("detail", "")[:160]}',
            exp_p3 is not None and _ok_all(reps, meta) and len(reps) == 3 and m3.get('ok') is True and '3' in m3.get('name', ''),
            [m_ for m_ in meta if not m_['ok']][:3])
        bad = {}
        for nm, ed in (('plan 삭제', lambda m_: m_.pop('plan')),
                       ('cohorts=[] (queue 유지)', lambda m_: m_['plan'].update(cohorts=[])),
                       ('cohorts 삭제 (queue 유지)', lambda m_: m_['plan'].pop('cohorts')),
                       ('queue 삭제', lambda m_: m_['plan'].pop('queue')),
                       ('코호트 하나 누락 (lhsx · 그 큐 항목도)', lambda m_: m_['plan'].update(cohorts=[c_ for c_ in m_['plan']['cohorts'] if c_['name'] != 'lhsx'],
                                                                                  queue=[e_ for e_ in m_['plan']['queue'] if e_['cohort'] != 'lhsx'])),
                       ('중복 ID', lambda m_: m_['plan']['queue'].append(dict(m_['plan']['queue'][0]))),
                       ('등록 밖 코호트 (lhsz · 케이스 하나)', lambda m_: (m_['plan']['cohorts'].append(dict(name='lhsz')),
                                                                   m_['plan']['queue'].append(dict(case='lhsz_000', cohort='lhsz')))),
                       ('등록 밖 케이스 (lhs00_999 · 큐에만)', lambda m_: m_['plan']['queue'].append(dict(case='lhs00_999', cohort='lhs')))):
            m2 = json.loads(json.dumps(m_p3))
            ed(m2)
            (lr_p3 / 'manifest.json').write_text(json.dumps(m2), encoding='utf-8')
            reps, meta, exp = _run_l(lr_p3, exp_p3)
            nf = summarize(reps, meta, out=lambda *a, **k: None)
            if nf == 0:
                bad[nm] = (len(reps), [m_['name'][:30] for m_ in meta])
        (lr_p3 / 'manifest.json').write_text(json.dumps(m_p3), encoding='utf-8')
        chk(f'★ G2RR2-02 반례 — plan 삭제 · cohorts=[] · cohorts 삭제 · queue 삭제 · 코호트 하나 누락 · 중복 ID · 등록 밖 코호트 · 등록 밖 케이스 → 전부 FAIL '
            f'(옛: plan · cohorts 셋 · 누락 = 0 케이스 · n_fail 0 · rc 0) {bad or ""}', not bad, repr(bad))
        def _main_rc(argv):
            try:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    return main(argv)
            except SystemExit as e:                              # argparse 거부 (옛 코드에 없는 인자) 도 rc 로
                return e.code if isinstance(e.code, int) else 2
        rc_u = _main_rc(['--launcher-root', str(lr_p3)])
        chk('★ launcher-root 는 등록 모드가 필수 — --expect-set · --expect-case 없이 부르면 사용 오류 rc 2 (mutable 큐를 자기 기대 집합으로 쓰지 않는다)', rc_u == 2, rc_u)
        jp = tmp / 'p3.json'
        rc_j = _main_rc(['--launcher-root', str(lr_p3), '--expect-set', 'pilot3', '--json', str(jp)])
        jj = _read_json(jp) or {}
        chk('★ 판정 JSON 이 기대 수 · 읽은 수 · 집합 대조를 싣는다 (n_fail 만이 아니다) — 기대 3 · 읽음 3 · 같음 · CLI rc 0',
            rc_j == 0 and jj.get('expected_n') == 3 and jj.get('read_n') == 3 and jj.get('set_equal') is True and jj.get('expected_set') == 'pilot3',
            {k: jj.get(k) for k in ('expected_n', 'read_n', 'set_equal', 'expected_set', 'n_fail')})
        #  ★ 10-07 G2RR3-01 (Codex 세대 2 재검증 3 §3 최소 해결 3) — 판정 JSON 이 **이번 ROOT · 봉인** 의 증거: 읽은 배치 뿌리 (resolve) · 읽은 manifest 바이트의
        #    sha256 · 발사 봉인 지문 (seal.code_fp) · 발사 sha (git.sha) · 스키마 v3 — v1.3 배포 관문 (`lhs_release_build.v13_reread_problems`) 이 배치 뿌리와 맞댄다
        mp3 = lr_p3 / 'manifest.json'
        chk('★ G2RR3-01 — 판정 JSON 스키마 v3 · launcher_root = 읽은 ROOT (resolve) · manifest_sha256 = 읽은 manifest 바이트 · seal_fp = seal.code_fp · '
            'launch_sha = git.sha (옛 v2: 어느 ROOT · 봉인의 기록인지 없다)',
            jj.get('schema') == 'g2_network_reread/v3' and jj.get('launcher_root') == str(lr_p3.resolve())
            and jj.get('manifest_sha256') == hashlib.sha256(mp3.read_bytes()).hexdigest()
            and jj.get('seal_fp') == m_p3['seal']['code_fp'] and jj.get('launch_sha') == m_p3['git']['sha'],
            {k: jj.get(k) for k in ('schema', 'launcher_root', 'manifest_sha256', 'seal_fp', 'launch_sha')})
        try:
            import lhs_release_build as _LRB                     # noqa: E402  (v1.3 배포 관문 — 같은 판정 함수)
            _vrp = getattr(_LRB, 'v13_reread_problems', None)
            if _vrp is None:
                p_same = p_other = ['(배포 관문의 다시 읽기 판정 함수 없음 — 옛 코드)']
            else:
                p_same = _vrp(jj, str(lr_p3), expect_set='pilot3')
                p_other = _vrp(jj, str(tmp / 'lroot_declared'), expect_set='pilot3')
        except Exception as e:                                   # noqa: BLE001
            p_same = p_other = [f'{type(e).__name__}: {e}']
        chk('★ G2RR3-01 — 실 생산자 JSON 을 v1.3 배포 관문의 다시 읽기 판정 (lhs_release_build.v13_reread_problems · 등록 집합 pilot3) 에 이 ROOT 로 넣으면 '
            '문제 0 · 다른 ROOT 로 대조하면 결합 문제 (배치 뿌리 · manifest sha256)',
            p_same == [] and any('launcher_root' in p_ for p_ in p_other) and any('manifest_sha256' in p_ for p_ in p_other), (p_same, p_other))
        #  ★ 10-07 G2RR4-01 (Codex 세대 2 재검증 4 §2) — 실 생산자 JSON 의 상세 (meta · cases · checks) = 상세 계약 (`launcher_detail_problems` — v1.3 배포 관문이
        #    부르는 같은 함수) 통과 · 상세 명시 실패 (n_fail 0 유지) · cases=[] · meta=[] · 빈 checks 변이 = 문제 (옛: 배포 관문이 상세를 읽지 않았다)
        _ldp = globals().get('launcher_detail_problems')

        def _mut(fn):
            j_ = json.loads(json.dumps(jj))
            fn(j_)
            return j_
        if _ldp is None or exp_p3 is None:
            d_ok, d_bad = ['(상세 계약 함수 없음 — 옛 코드)'], {}
        else:
            d_ok = _ldp(jj, exp_p3['pairs'])
            d_bad = {nm_: _ldp(_mut(fn_), exp_p3['pairs']) for nm_, fn_ in (
                ('M2 lhs ok=false', lambda j_: next(m_ for m_ in j_['meta'] if m_['name'].startswith('M2 lhs')).update(ok=False)),
                ('cases=[] · meta=[]', lambda j_: j_.update(cases=[], meta=[])),
                ('빈 checks', lambda j_: [c_.update(checks=[]) for c_ in j_['cases']]),
                ('K4 빠짐', lambda j_: j_['cases'][0].update(checks=[c_ for c_ in j_['cases'][0]['checks'] if not c_['name'].startswith('K4 ')])))}
        chk('★ G2RR4-01 — 실 생산자 JSON (pilot3) 의 상세 = 상세 계약 통과 (meta 열 ID · 코호트마다 M1 · M2 · H1 · 케이스마다 K1–K7 · 상세 실패 재계수 = n_fail · '
            '(케이스, 코호트) = 등록 집합 · M3 = 최상위) · M2 ok=false · cases=[] · 빈 checks · K4 빠짐 = 전부 문제',
            d_ok == [] and len(d_bad) == 4 and all(d_bad.values()), (d_ok[:3], {k: v[:2] for k, v in d_bad.items()}))
        #  폴더 링크 — symlink 가 막힌 환경 (Windows WinError 1314 · Codex 재검증 2 §11) 에서도 fixture 가 선다 (하드링크 · 사본)
        _sym = os.symlink

        def _deny(*a, **k):
            raise OSError(1314, '권한 없음 (selftest 흉내)')
        os.symlink = _deny
        try:
            kind_ = _link_dir(tmp / 'case_through', tmp / 'link_fallback')
        finally:
            os.symlink = _sym
        r_lf = run_smoke_or_dirs([tmp / 'link_fallback'], 'g2')[0]
        chk(f'symlink 거부 환경 — 폴더 링크가 {kind_} 로 대체되고 그 폴더가 K1–K7 · H1 통과',
            kind_ in ('hardlink', 'copy') and all(c['ok'] for c in r_lf['checks']), [c for c in r_lf['checks'] if not c['ok']][:2])
        #  생산 194 (합성) — 등록 지문의 194 ID (커밋된 수확 폴더) · 두 코호트 · 케이스 폴더 = 같은 게시 폴더 링크 (K1–K7 · H1 은 폴더마다)
        try:
            exp_194 = _rid('production194') if _rid else None
        except Exception as e:                                   # noqa: BLE001
            exp_194 = None
            print(f'  (등록 집합 production194 못 읽음: {type(e).__name__}: {e})')
        if exp_194 is not None:
            p194 = {}
            for c, h in sorted(exp_194['pairs']):
                p194.setdefault(h, []).append((c, 'through'))
            lr_194, _m194 = _lroot('prod194', p194, link=True)
            reps, meta, exp = _run_l(lr_194, exp_194)
            m3 = next((m_ for m_ in meta if m_['name'].startswith('M3')), {})
            chk('★ 등록 집합 양성 production194 (합성 — 등록 ID 지문 194 · lhs 130 · lhsx 64) — 194 케이스 K1–K7 · 코호트 H1 둘 통과 · M3 기대 194 = 읽음 194',
                _ok_all(reps, meta) and len(reps) == 194 and m3.get('ok') is True, [m_ for m_ in meta if not m_['ok']][:3])
            #  ★ G2RR4-01 — 같은 실행의 판정 JSON 꼴 (main 이 쓰는 키 그대로 · JSON 왕복) 이 production194 상세 계약을 통과 (생산자 ↔ 배포 관문의 같은 표)
            _ldp2 = globals().get('launcher_detail_problems')
            rec194 = json.loads(json.dumps(dict(schema=SCHEMA, expected_generation=exp, meta=meta, cases=reps,
                                                n_fail=summarize(reps, meta, out=lambda *a, **k: None), expected_set=exp_194['name'],
                                                expected_n=m3.get('expected_n'), read_n=m3.get('read_n'), set_equal=m3.get('set_equal'),
                                                missing=m3.get('missing'), extra=m3.get('extra')), default=str))
            d194 = _ldp2(rec194, exp_194['pairs']) if _ldp2 else ['(상세 계약 함수 없음 — 옛 코드)']
            chk('★ G2RR4-01 — 생산 194 (합성) 판정 JSON 의 상세 = 상세 계약 통과 (194 케이스 × K1–K7 · meta 열 · 재계수 0 = n_fail 0)', d194 == [], d194[:3])
        else:
            chk('★ 등록 집합 양성 production194 (등록 집합 함수 없음 — 옛 코드)', False)
        #  ★ 10-07 G2RR4-03 → ★ 10-08 G2RR5-03 (Codex 세대 2 재검증 5 §3) — 스모크 음성 대조 (case15) S0b 반례 먼저 (Codex r5_case15 변이 그대로) ·
        #    정상 관통 · 비관통 · clamp 게시 폴더 = 위 실 생산자 게시 (K1–K7 · H1 통과가 계속 보여야).  S0b = 등록 표지 ∧ 케이스 신원 (case15_network · kind case15 ·
        #    망 정지) 일 때만 S0 에서 뺀다 (그 밖 truthy 표지 = S0 실패 + "미등록 음성 대조 표지") · 그 케이스의 기록된 검사 = 등록 안정 ID 집합 정확히 (각 1 회 ·
        #    id 없음 · 모르는 ID 거부) · 전부 PASS · 공용 판정 (`case15_negctl_verdicts`) 을 보고 상세에 다시 돌린 판정 = 기록 (상세 결손 · 수치 모순 = 실패) ·
        #    필수 ID 에 자식 프로세스 · 원자료 sha256 · 실제 망 시도 · 게시 없음.  옛 판 (S0b = '<id>: [음성 대조]' 접두어 PASS ≥ 4 · truthy 표지 면제):
        #    marker_unknown · one_check_repeated_four · negctl_missing · tau_numeric · ionic_residual_bad · raw_sha_fail · unexpected_failure_record = rc 0 (Codex 핀).
        #    양성 case15 = 실제 case15 값 (10-08 컨테이너 첫 실행 · 고정 토큰 · WSL 10-07 기록과 같은 digest) 상세 + **고친 스모크 생산자 evaluate** (하위 프로세스 —
        #    이 도구는 하네스를 import 하지 않는다) 가 낸 검사 일곱 · timings rc 0.  실제 파이프라인 판 (≈ 120 s) 은 스모크 selftest 마지막 묶음 (b) 이 이 도구의
        #    --smoke-root 에 넣는다 (이 selftest 는 게이트의 fast 예산 안).
        import subprocess
        _vfn = globals().get('case15_negctl_verdicts')
        _ng = globals().get('CASE15_NEGCTL') or {}
        _ids_reg = globals().get('CASE15_NEGCTL_IDS') or ()
        sm = tmp / 'smoke_neg'
        (sm / 'work' / 'results').mkdir(parents=True)
        normal = {}
        for bed in ('through', 'nonthrough', 'clamp'):
            shutil.copytree(tmp / f'case_{bed}', sm / 'work' / 'results' / f'syn_{bed}')
            normal[f'syn_{bed}'] = dict(stop_after='network', status='done')
        solver = 'Network Solver (both modes)'
        dig = {'atoms.csv': 'e140e28d3daf3ad7', 'contacts.csv': 'bcb53e13d2cc69be'}
        ovr = '관통 성분은 있는데 {s} 을 풀지 못했다 (boundary_overlap) — 미퍼콜이 아니다 · 수치 실패 = 게시 차단 (WEB-03 Q1 — 일반 · 정지 경로 모두)'
        ref = 'ValueError: physics_g2: 간선 (31, 29241) — ligg_area < 0 (-0.186036)'
        b_t = [24, 40, 57, 103]

        def _chs(m):
            return dict(ionic=dict(status='computed', reason=None), electronic=dict(status='failed', reason=ovr.format(s='σ_e')),
                        thermal=dict(status='failed', reason=(ovr.format(s='κ') if m == 'hertzian' else ref)))
        c15 = dict(
            id='case15_network', kind='case15', stop_after='network', negative_control='case15_publication_blocked', status='failed', success=False,
            failed_stages=[solver], stage_e_ran=False, returned_network_run_id=None, raw_sha_ok=True,
            raw_sha={k: ('ab' * 6, 'ab' * 6) for k in ('atom_v4_1710000.liggghts', 'contact_v4_1710000.liggghts', 'mesh_v4_1710000.stl', 'input_case15.liggghts')},
            stages=[dict(step=s, rc=0, ok=True, required=s != 'Coverage Physics vs Hertzian', missing_outputs=[], stale_outputs=[], verify_failed=False, err='')
                    for s in ('Parse', 'Contact Analysis', 'Coverage Physics vs Hertzian')]
            + [dict(step=solver, rc=0, ok=False, required=True, missing_outputs=[], stale_outputs=[], verify_failed=True, err=f'… physics.thermal=fail ({ref})'),
               dict(step='Network Merge / Stage E', rc=1, ok=None, required=None, missing_outputs=None, stale_outputs=None, verify_failed=None, err='…')],
            attempt=dict(schema='network_attempt/v2', solver_status='failed', latest_attempt_status='failed', failure_kind='solver', stage=solver,
                         input_digests=dict(dig), reason=f'… physics.thermal=fail ({ref})'),
            attempt_evidence=dict(schema='wsl_network_smoke/attempt_evidence/v1', hook='pipeline_service._RUNNER',
                                  calls=[dict(n=1, script='network_conductivity.py', input_digests=dict(dig), exception=None, exception_text=None, returncode=0,
                                              per_mode={m: dict(sha256=h * 64, bytes=1000, channels=_chs(m), read_error=None)
                                                        for m, h in (('hertzian', '1'), ('physics', '2'))})]),
            tau=dict({f'ion_net_status_{m}': 'NOT_COMPUTED' for m in ('hertz', 'physics', 'hertz_h12')},
                     **{f'{p}_ion_{m}': None for p in ('f', 'tau2', 'tau') for m in ('hertz', 'physics', 'hertz_h12')}),
            negctl=dict(atoms=65970, contacts=182995, plate_um=19.1455, box_um=[100.0, 100.0],
                        negative_area=[[31, 29241, -0.186036, 1.05114], [38, 29241, -0.186264, 1.0512]],
                        channels=dict(ionic_hertzian=dict(value=[0.1704582411149847, 0.00032635082552669387], status='computed', reason=None,
                                                          conservation_rel=1.899983684231436e-09, residual_rel=9.825340313851229e-11, intersection=[]),
                                      ionic_physics=dict(value=[0.1892075130340654, 0.00036224724407936984], status='computed', reason=None,
                                                         conservation_rel=5.087356705432166e-09, residual_rel=9.411786725961204e-11, intersection=[]),
                                      **{k: dict(value=[None, None], status='not_computed', reason='boundary_overlap', conservation_rel=None, residual_rel=None,
                                                 intersection=list(b_t)) for k in ('electronic_hertzian', 'electronic_physics', 'thermal_hertzian')},
                                      thermal_physics=dict(error=ref))))

        def _smoke_eval(reps):
            """고친 스모크 생산자의 evaluate (하위 프로세스) → {이름: 검사 목록} — 인계 도구는 하네스를 import 하지 않는다."""
            k_ = len(list(tmp.glob('eval_in_*.json')))
            src, dst = tmp / f'eval_in_{k_}.json', tmp / f'eval_out_{k_}.json'
            src.write_text(json.dumps(reps, ensure_ascii=False), encoding='utf-8')
            boot = ('import json, sys\n'
                    'sys.path[:0] = [sys.argv[1]]\n'
                    'import wsl_network_smoke as S\n'
                    'd = json.load(open(sys.argv[2], encoding="utf-8"))\n'
                    'o = {k: S.evaluate({v["report"]["id"]: v["report"]}, {v["report"]["id"]: v["timing"]}) for k, v in d.items()}\n'
                    'open(sys.argv[3], "w", encoding="utf-8").write(json.dumps(o, ensure_ascii=False))\n')
            p_ = subprocess.run([sys.executable, '-c', boot, str(ROOT / 'scripts'), str(src), str(dst)], capture_output=True, text=True, timeout=300,
                                env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
            return (_read_json(dst) or {}), (p_.returncode, (p_.stdout + p_.stderr)[-300:])
        r_sha = json.loads(json.dumps(c15))
        r_sha['raw_sha_ok'] = False
        r_uf = json.loads(json.dumps(c15))
        r_uf['attempt']['reason'] = 'PermissionError: solver executable denied'
        for s_ in r_uf['stages']:
            if s_['step'] == solver:
                s_.update(rc=1, err='PermissionError: solver executable denied')
        ev_, why_ev = _smoke_eval({'positive': dict(report=c15, timing=dict(rc=0)), 'raw_sha_fail': dict(report=r_sha, timing=dict(rc=0)),
                                   'unexpected_failure_record': dict(report=r_uf, timing=dict(rc=0))})
        chk15 = [c for c in ev_.get('positive') or [] if str(c.get('name', '')).startswith('case15_network:')]
        base = dict(reports=dict(normal, case15_network=c15), checks=chk15, timings={'case15_network': dict(rc=0)}, rc=0)

        def _sm(doc, label):
            (sm / 'smoke_report.json').write_text(json.dumps(doc, ensure_ascii=False), encoding='utf-8')
            jp_ = tmp / f'sm_{label}.json'
            rc_ = _main_rc(['--smoke-root', str(sm), '--json', str(jp_)])
            j_ = _read_json(jp_) or {}
            return rc_, {('S0b' if m_['name'].startswith('S0b') else m_['name'][:2]): m_['ok'] for m_ in j_.get('meta') or []}, j_

        def _mut(fn):
            d_ = json.loads(json.dumps(base))
            fn(d_)
            return d_

        def _r(d_):
            return d_['reports']['case15_network']

        def _negs(d_):
            return [c for c in d_['checks'] if '[음성 대조]' in str(c.get('name', ''))]

        def _legacy(d_):
            r_ = _r(d_)
            r_.pop('attempt_evidence', None)
            for s_ in r_['stages']:
                for k_ in ('missing_outputs', 'stale_outputs', 'verify_failed'):
                    s_.pop(k_, None)
            d_['checks'] = [{k_: v_ for k_, v_ in c.items() if k_ != 'id'} for c in d_['checks'] if '실제 망 시도' not in str(c.get('name', ''))]
        V = {'marker_missing': _mut(lambda d_: _r(d_).pop('negative_control')),
             'marker_unknown': _mut(lambda d_: _r(d_).update(negative_control='unregistered_future_control')),
             'checks_missing': _mut(lambda d_: d_.update(checks=[])),
             'checks_three': _mut(lambda d_: d_.update(checks=_negs(d_)[:3])),
             'check_fail': _mut(lambda d_: _negs(d_)[-1].update(verdict='FAIL')),
             'one_check_repeated_four': _mut(lambda d_: d_.update(checks=[dict(_negs(d_)[0]) for _ in range(4)])),
             'negctl_missing': _mut(lambda d_: _r(d_).pop('negctl')),
             'tau_numeric': _mut(lambda d_: _r(d_)['tau'].update(tau_ion_hertz=1.0)),
             'ionic_residual_bad': _mut(lambda d_: _r(d_)['negctl']['channels']['ionic_physics'].update(residual_rel=0.1)),
             'raw_sha_fail': _mut(lambda d_: (d_['reports'].update(case15_network=r_sha), d_.update(rc=1, checks=[
                 c for c in ev_.get('raw_sha_fail') or [] if str(c.get('name', '')).startswith('case15_network:')]))),
             'unexpected_failure_record': _mut(lambda d_: (d_['reports'].update(case15_network=r_uf), d_.update(checks=[
                 c for c in ev_.get('unexpected_failure_record') or [] if str(c.get('name', '')).startswith('case15_network:')]))),
             'published': _mut(lambda d_: _r(d_).update(status='done', returned_network_run_id='RUN-x')),
             'identity_kind': _mut(lambda d_: _r(d_).update(kind='real14')),
             'unknown_id': _mut(lambda d_: d_['checks'].append(dict(group='A', id='case15.extra', name='case15_network: [음성 대조] 등록 밖 검사',
                                                                     verdict='PASS', detail=''))),
             'timing_missing': _mut(lambda d_: d_.pop('timings')),
             'legacy_record': _mut(_legacy)}
        rc_p, meta_p, j_p = _sm(base, 'positive')
        res = {nm: _sm(doc, nm)[:2] for nm, doc in V.items()}
        WANT = {'marker_missing': {'S0': False}, 'marker_unknown': {'S0': False, 'S0b': False}, 'identity_kind': {'S0': False, 'S0b': False}}

        def _bad(names):
            return {nm: res[nm] for nm in names if res[nm] != (1, WANT.get(nm, {'S0': True, 'S0b': False}))}
        try:
            _fs = ps._CHANNEL_FAIL_STATES == frozenset({_ng.get('attempt_fail_status')})
        except Exception:                                        # noqa: BLE001
            _fs = False
        again = _vfn(c15, dict(rc=0)) if _vfn else []
        chk(f'★ G2RR5-03 양성 — 실제 case15 값의 기록 + 고친 스모크 생산자 evaluate (하위 프로세스) 의 검사 일곱 = 등록 안정 ID (차례 · id 키) 전부 PASS · '
            f'공용 판정 (case15_negctl_verdicts) 재계산 일곱 PASS · S0 · S0b 통과 rc 0 · 정상 관통 · 비관통 · clamp 게시 폴더 K1–K7 · H1 통과 · '
            f'실패 상태 토큰 = pipeline_service._CHANNEL_FAIL_STATES {meta_p} rc {rc_p}',
            rc_p == 0 and meta_p == {'S0': True, 'S0b': True} and j_p.get('n_fail') == 0 and len(j_p.get('cases') or []) == 3
            and all(c['ok'] for r_ in j_p.get('cases') or [] for c in r_['checks'])
            and bool(_ids_reg) and [c.get('id') for c in chk15] == list(_ids_reg) and all(c.get('verdict') == 'PASS' for c in chk15)
            and [(i, v) for i, _n, v, _d in again] == [(i, 'PASS') for i in _ids_reg] and _fs,
            repr((why_ev, [(c.get('id'), c.get('verdict'), str(c.get('detail'))[:80]) for c in chk15], again[:2], meta_p, _fs))[:900])
        codex7 = ('marker_unknown', 'one_check_repeated_four', 'negctl_missing', 'tau_numeric', 'ionic_residual_bad', 'raw_sha_fail', 'unexpected_failure_record')
        chk(f'★ G2RR5-03 반례 (Codex r5_case15 변이 일곱 — 옛 판 rc 0) → 전부 rc 1 (미등록 표지 = S0 · S0b 실패 · 그 밖 = S0b 실패) {_bad(codex7) or ""}',
            not _bad(codex7), repr({nm: res[nm] for nm in codex7}))
        reg5 = ('marker_missing', 'checks_missing', 'checks_three', 'check_fail', 'published')
        chk(f'회귀 — 표지 없음 (이름 면제 없음 = S0 실패) · 검사 없음 · 셋만 · 하나 FAIL · 게시됨 → rc 1 (옛 판도 rc 1 · 과잉차단 아님 = 위 양성) {_bad(reg5) or ""}',
            not _bad(reg5), repr({nm: res[nm] for nm in reg5}))
        ext4 = ('identity_kind', 'unknown_id', 'timing_missing', 'legacy_record')
        chk(f'★ G2RR5-03 신원 · ID 계약 — 등록 표지 + kind 다름 (= 미등록) · 모르는 ID 하나 더 · 자식 프로세스 기록 (timings) 없음 · 옛 형식 기록 (실제 시도 증거 · 검사 '
            f'id 없음 = G2RR5-02 이전 생산자 · 제출 WSL 10-07 기록과 같은 꼴 — 그 기록은 고친 스모크로 다시 만들어야) → rc 1 {_bad(ext4) or ""}',
            not _bad(ext4), repr({nm: res[nm] for nm in ext4}))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        for d in made:
            shutil.rmtree(d, ignore_errors=True)
    print(f'\n{"✓ 전부 통과" if not fails else f"✗ {len(fails)} 건 실패"}')
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main())
