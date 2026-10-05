#!/usr/bin/env python3
"""웹앱 케이스 → 웹앱 파이프라인 **그대로** network 단계까지 (`run_pipeline(stop_after='network')`) · 격리 작업 폴더 · σ 표 (TSV + JSON).

계기 (2026-10-05 밤 · 10-06 09:00 보고): ps45 r4.5 침대 다섯 (PC:SC = 10:0 · 7:3 · 5:5 · 3:7 · 0:10 · 6 mAh/cm² · 약 16 만 입자) 의
접촉망 σ_ion (SE–SE 망) · σ_e (AM–AM 망) 를 **현재 코드**로 다시 낸다.  케이스 id = `docs/data/ps45_r45_union_20260929/r45_union_summary.tsv`.

규율 ① — 새로 계산하지 않는다
  • 계산 = 웹앱 `app.run_pipeline` 그대로.  호출 규약은 `lhs_webapp_batch` 와 같다 (figures=False · auto_db=False · stop_after='network'
    = 파싱 → 접촉 → 피복 → network solver → 머지 · 채널 판정 → 망 정지 계약 · Stage E 없음).  인자 (mode · type_map · scale) = 케이스
    자신의 meta.json — 웹앱 /analyze 라우트가 run_pipeline 에 넘기는 바로 그 값 (덱 판독 map 은 기록만 · 대조 표지).
  • 표의 값 = 생산된 파일.  망 값은 `network_conductivity_dual.json` (망 정본 — 정지 계약 docstring) 의 두 모드 레코드 키 그대로
    (+ 모드 꼬리 `_hertz` · `_physics`) · 장부는 `full_metrics.json` · τ 인계 열은 `tau_flux.ion_columns` (= `tau_flux.case_row` 의 함수) ·
    세대 · 최근 시도는 `pipeline_service.network_status_view`.  다시 셈하지 않는다 — 전자 CF σ 는 솔버가 비 (`electronic_R_brug` =
    CF/FULL · 4 자리) 로만 남기므로 비 그대로 싣는다.
  • `lhs_webapp_batch` 를 그대로 못 쓰는 이유: 그것은 수확 JSON (같은 프레임 sha · type_map · phase_counts) 과 봉인 코호트가 있는
    LHS 침대 전용이다 (임의의 웹앱 케이스 폴더를 받지 않는다).  여기서는 그 도구의 env 격리 (`prepare_env`) · 의존 적재 (`load_deps`) ·
    코드 출처 (`code_provenance`) 와 한 프레임 · 쌍마다 한 행 관문 (`lhs_descriptor_harvest.scan_contact_dump` · DESC-06) 을 그대로 쓴다.
    ⇒ 3-type 덱의 0 입자 상 (P:S 10:0 · 0:10) 에 `absent_types` 처리가 필요 없다 — 그것은 수확 JSON 의 3-type map 과 덱 판독을
    맞추는 관문이고, 여기의 기준인 meta.json 은 업로드 때 이미 덱 판독 (0 개 type 을 뺀 map) 으로 적혔다.

격리 (fail-closed)
  • 원본 업로드 폴더는 **읽기만** 한다 — 같은 step 의 atom · contact · mesh + 덱 + meta.json 만 `<out>/work/uploads/<id>/` 로 **복사**
    (심볼릭 링크 아님 · sha256 대조 — run_pipeline 은 폴더를 glob 하므로 다른 프레임 파일은 넣지 않는다, SELF-47) 하고, 실행 전후 원본의
    sha256 · 목록 (이름 · 크기 · mtime) 이 같아야 한다 (`source_unchanged` — 어기면 그 케이스 failed).
  • 실행 중 CWD = `<out>/work/cwd/<id>/` — 피복 단계가 요약 CSV 를 CWD 상대 `docs/figures/physics_regime/` 에 쓴다 (LHS-27 — 코드
    체크아웃을 더럽힌다).  단계 스크립트 import 폐포에서 CWD 상대 경로는 그 출력 하나뿐 (입력은 전부 절대 경로) ⇒ 값 불변 · 끝나면 되돌린다.
  • 웹앱 폴더 env (WEBAPP_*_FOLDER) · app.config 를 작업 폴더로 돌리고, 케이스 폴더 해석이 작업 폴더 안인지 실행 전에 본다.  `--out` 이
    서빙 중 폴더 (env · webapp/.env · 리포 안 webapp/uploads|results|archive · 원본 업로드 루트 · 그 옆 results|archive) 안이거나 원본이
    `--out` 안이면 rc 2 로 아무것도 안 한다.  원격 저장소 (Supabase) 는 끈다.  끝나면 env 를 되돌린다.
  • network solver 는 웹앱 파일 lock 으로 기계 전체에서 직렬이다 — 웹앱이 같은 기계에서 솔버를 돌리고 있으면 기다린다.

망 정지 계약 · 채널 판정에 걸린 케이스 (failed): 파이프라인은 그 후보를 게시하지 않고 치운다 (설계대로 · 첫 실행이면 망 JSON 이 없다).
  이 도구는 솔버가 쓴 직후의 네 JSON 을 `<out>/solver_output/<id>/` 에 **사본**으로 남기고 (`pipeline_service._RUNNER` 주입점에서
  위임 뒤 복사만 — 명령 · 판정 불변), 표에는 `values_source = solver_output_not_published` 로 표지해 싣는다 (게시값과 섞지 않는다).

사용 (저자 WSL — 리포 체크아웃 안의 이 스크립트를 웹앱 venv 의 python 으로)
    python3 scripts/webapp_network_batch.py --uploads-root ~/Yonghoon-DEM-DFT/webapp/uploads \\
        --from-tsv docs/data/ps45_r45_union_20260929/r45_union_summary.tsv --out ~/ps45_network_20261005
    … --check-only                     # 관문만 (복사 · 실행 없음 · 쓰기 없음)
    … --only 260925_000001_0bee25      # 한 건 먼저 (시간 확인)
    python3 scripts/webapp_network_batch.py --case <id>[=<P:S 라벨>] --case <업로드 폴더 경로> --out …
    python3 scripts/webapp_network_batch.py --selftest

산출 (`--out`)
  network_cases.tsv · network_cases.json (케이스당 한 행 · JSON 에 열 설명) · status.json (실행 기록 · 재개 근거) ·
  logs/<id>.stages.json (단계 로그 — 솔버 stdout 포함) · solver_output/<id>/ (솔버 출력 사본) · work/ (사본 · results — 크다, 보낼 필요 없음)
재개: done · partial 케이스는 건너뛴다 (`--force` 로 다시).
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import lhs_webapp_batch as LWB          # noqa: E402  (prepare_env · load_deps · code_provenance · Refuse — 같은 호출 규약)
import lhs_harvest_batch as HB          # noqa: E402  (sha256_of)
import lhs_descriptor_harvest as H      # noqa: E402  (한 프레임 · 쌍마다 한 행 관문 — DESC-06 · lhs_webapp_batch 와 같은 함수)
import type_map_resolve as TMR          # noqa: E402  (덤프 type 별 개수 · map 검사 · 덱 판독)
import tau_flux as TF                   # noqa: E402  (τ 인계 열 · 웹앱 τ 블록 tau2 — 같은 도우미)

SCHEMA = 'webapp_network_batch/v1'
STOP_AFTER = 'network'
KEEP_STATUS = ('done', 'partial')
ENV_KEYS = ('WEBAPP_UPLOAD_FOLDER', 'WEBAPP_RESULTS_FOLDER', 'WEBAPP_ARCHIVE_FOLDER', 'WEBAPP_MPM_LAB_FOLDER',
            'SUPABASE_URL', 'SUPABASE_KEY', 'PYTHONDONTWRITEBYTECODE')
SERVED_KEYS = ('WEBAPP_UPLOAD_FOLDER', 'WEBAPP_RESULTS_FOLDER', 'WEBAPP_ARCHIVE_FOLDER')
MODES = (('hertzian', 'hertz'), ('physics', 'physics'))           # (dual 키, 열 꼬리 — τ 규약 · tau_flux 와 같은 꼬리)
NET_JSON = ('network_conductivity.json', 'network_conductivity_hertzian.json', 'network_conductivity_physics.json',
            'network_conductivity_dual.json')
STOP_STEP = 'Network stop contract'                               # app._network_candidate_checks 의 단계 이름 앞머리
_RE_DUMP = re.compile(r'^(atom|contact)_(\d+)\.liggghts$')
_RE_MESH = re.compile(r'^mesh_(\d+)\.stl$')

#: 망 레코드 (dual 의 모드 하나) 에서 싣는 키 — 생산자 `network_conductivity.run_decomposition` · `_run_all_networks` 의 이름 그대로.
NET_KEYS = (
    # 이온 — SE–SE 망
    'sigma_full_mScm', 'sigma_full_status', 'sigma_full_reason',
    'sigma_bulk_net_mScm', 'sigma_bulk_net_status', 'sigma_bulk_net_reason',
    'sigma_constr_net_mScm', 'R_brug_over_full', 'percolating_fraction', 'active_fraction',
    'ionic_status', 'ionic_status_reason', 'phi_se', 'boundary_rule', 'boundary_band_frac',
    'n_nodes', 'n_edges', 'resistance_model', 'psi_placement',
    # 전자 — AM–AM 망
    'electronic_sigma_full_mScm', 'electronic_R_brug', 'electronic_percolating_fraction', 'electronic_active_fraction',
    'electronic_status', 'electronic_status_reason', 'electronic_boundary_rule', 'electronic_n_nodes', 'electronic_n_edges',
    # 열 — 전 접촉 망
    'thermal_sigma_full_mScm', 'thermal_R_brug', 'thermal_status', 'thermal_status_reason', 'thermal_boundary_rule',
)
#: full_metrics 에서 싣는 키 (접촉 분석 장부 · 게시 때 머지된 도장 · 채널 판정) — 이름 그대로.
FM_KEYS = ('phi_se', 'phi_se_mass_conserving', 'thickness_um', 'thickness_mass_conserving_um', 'percolation_pct', 'porosity',
           'network_run_id', 'network_solver_status', 'failed_channels',
           'ionic_channel_verdict', 'ionic_channel_reason', 'electronic_channel_verdict', 'electronic_channel_reason',
           'thermal_channel_verdict', 'thermal_channel_reason')
#: `pipeline_service.network_status_view` 의 키 이름 그대로 (활성 세대 ↔ 최근 시도 — 한 실패 어휘).
VIEW_KEYS = ('active_network_run_id', 'active_status', 'latest_attempt_run_id', 'latest_attempt_status', 'failure_kind',
             'latest_attempt_stage', 'latest_attempt_reason', 'stale')
#: TSV 앞쪽에 둘 열 (보고에 바로 쓰는 것) — 나머지는 뒤에 정해진 순서로.
LEAD = ['case_id', 'P_S', 'bed', 'webapp_name', 'meta_name', 'run_status', 'values_source',
        'sigma_full_mScm_hertz', 'sigma_full_mScm_physics', 'sigma_bulk_net_mScm_hertz', 'sigma_bulk_net_mScm_physics',
        'electronic_sigma_full_mScm_hertz', 'electronic_sigma_full_mScm_physics',
        'electronic_R_brug_hertz', 'electronic_R_brug_physics',
        'thermal_sigma_full_mScm_hertz', 'thermal_sigma_full_mScm_physics',
        'sigma_full_status_hertz', 'sigma_full_status_physics', 'electronic_status_hertz', 'electronic_status_physics',
        'percolating_fraction_hertz', 'percolating_fraction_physics',
        'electronic_percolating_fraction_hertz', 'electronic_percolating_fraction_physics',
        'tau2_ion_hertz', 'tau2_ion_physics', 'ion_net_status_hertz', 'ion_net_status_physics',
        'phi_se', 'phi_se_mass_conserving', 'sigma_grain_S_cm',
        'elapsed_network_solver_s', 'elapsed_pipeline_s', 'stop_contract_ok', 'why', 'failed_stages']
RUN_KEYS = ('stop_after', 'stopped_after', 'mode', 'type_map', 'scale', 'atom_step', 'dump_type_counts', 'type_map_deck',
            'type_map_deck_agrees', 'type_map_deck_errors', 'run_network_run_id', 'stop_contract_msg', 'source_unchanged',
            'not_copied', 'elapsed_case_s', 'when')

COLUMN_NOTES = {
    'case_id': '웹앱 케이스 id (업로드 폴더 이름)',
    'P_S': 'PC:SC 라벨 (AM_P : AM_S — 입력 표의 P_S 또는 --case id=라벨)',
    'run_status': 'done · partial (선택 단계만 실패 — 망 값 유효) · failed · REFUSED (관문 — 실행 안 함, why 참조)',
    'values_source': "published = 망 정지 계약을 통과해 게시된 세대 (work/results/<id>) · solver_output_not_published = 솔버 출력 "
                     "사본 (채널 판정 · 정지 계약 실패로 게시 안 됨 — 그대로 인용 금지, 사유는 latest_attempt_reason) · '' = 값 없음",
    'sigma_full_mScm_<m>': 'σ_ion FULL — SE–SE 접촉망 (bulk + 접촉당 협착) mS/cm.  m = hertz (Hertz 면적 · Maxwell 협착) · physics '
                           '(Tabor+부피 면적 · Mikic) — 망 정본 dual 의 그 모드 레코드 그대로',
    'sigma_bulk_net_mScm_<m>': 'σ_ion CONTACT_FREE — 같은 망 · 협착 0 (이상 접촉 상한 가지) mS/cm',
    'sigma_constr_net_mScm_<m>': 'σ_ion CONSTRICTION_ONLY (bulk 0) mS/cm',
    'R_brug_over_full_<m>': '⚠ 이름과 달리 CONTACT_FREE / FULL (이온 · L2-07 — Bruggeman 아님) · 모형 내부 협착 비',
    'electronic_sigma_full_mScm_<m>': 'σ_e FULL — AM–AM 접촉망 mS/cm (간선 σ_AM = 50 mS/cm 모델 기준값 — CL-92: 측정 NCM811 의 약 10 배)',
    'electronic_R_brug_<m>': 'σ_e CONTACT_FREE / FULL (솔버가 전자 CF σ 를 따로 저장하지 않는다 — 비 4 자리 그대로 · 곱해서 만들지 않았다)',
    'thermal_sigma_full_mScm_<m>': 'κ FULL — 전 접촉 망 (솔버 키 이름 그대로 — 수치 = 1000 × W/(cm·K) · 간선 K_SE 0.7e-2 W/(cm·K))',
    'sigma_full_status_<m>': '생산자 이온 σ 상태 — computed · valid_zero (증명된 비관통 · 사유 no_through_path) · not_computed (풀이 실패)',
    '<channel>_status_<m>': '채널 상태 (computed · valid_zero · valid_null (미퍼콜 — 물리적 답) · not_applicable · failed)',
    'percolating_fraction_<m>': 'SE 망 관통 노드 분율 (솔버 · 띠 규칙 boundary_rule_<m> — L0 기본 · L1/L2 = 기록된 폴백)',
    'electronic_percolating_fraction_<m>': 'AM 망 관통 노드 분율',
    'phi_se_<m>': '망 φ_SE (구 부피 합 / 판 간격 상자 · 4 자리 — 생산자)',
    'phi_se': '접촉 분석 φ_SE (full_metrics) — 웹앱 τ 블록 tau2 의 φ',
    'phi_se_mass_conserving': 'φ_SE,mc (질량 보존 두께 기준) — τ 인계 열 (tau2_ion_<m>) 의 φ',
    'sigma_grain_S_cm': 'σ₀ = 이온 간선 재료 σ (S/cm · 두 모드 같은 값일 때만 — 25 °C 3.0e-3 = 펠릿값 · CL-91)',
    'f_ion_<m> · tau2_ion_<m> · tau_ion_<m> · ion_net_*': 'τ 인계 열 (tau_flux.ion_columns · τ 판정 v2 §5).  tau2 = tortuosity factor = '
                                                         'φ_mc / f_mc · tau = √tau2 (COMSOL 입력 아님) · 상태 게이트 G1–G6 = ion_net_status_<m>',
    'webapp_tau2_ion_<m>': '웹앱 케이스 τ 블록의 tau2 행 (tau_flux.tau2_from_metrics — 게시된 full_metrics σ 6 자리 · φ_se · 짝 σ₀) — '
                           '인계 tau2 와 같은 양 · 반올림 경로만 다름 (TAU-25 ≤ 0.11 %) · 상태 게이트 없음 · 게시값만',
    'constriction_power_share_<ch>_<m>': '협착 저항 전력 몫 Σ I²R_c / Σ I²R_total (같은 FULL 해 · 관통 간선 · ④a) · _status = 사유',
    'active_network_run_id … stale': '세대 · 최근 시도 (pipeline_service.network_status_view — 키 이름 그대로)',
    'network_run_id · network_solver_status · <channel>_channel_verdict': 'full_metrics 의 게시 도장 · 채널 판정 (게시됐을 때만)',
    'stop_contract_ok · stop_contract_msg': '망 정지 계약 단계 (pipeline_service.network_stop_verdict ①–⑧) — None = 그 단계까지 못 감',
    'run_network_run_id': 'run_pipeline 반환값 (게시면 이번 실행 · 실패면 되돌린 옛 활성 세대 — 첫 실행이면 None)',
    'elapsed_network_solver_s': 'network solver 서브프로세스 벽시계 초 (두 모드 × 세 채널 · lock 대기 제외)',
    'elapsed_pipeline_s': 'run_pipeline 전체 초 (파싱 → 접촉 → 피복 → 망 → 계약)',
    'source_unchanged': '원본 업로드 폴더의 sha256 · 목록 (이름 · 크기 · mtime) 이 실행 전후 같다 (격리 증거)',
    'type_map_deck · type_map_deck_agrees': '덱 판독 map (type_map_resolve) — 기록 · 대조만 (실행 인자는 meta.json 의 type_map)',
}


# ───────────────────────────────── 격리 ─────────────────────────────────
def _real(p) -> Path:
    return Path(os.path.realpath(os.path.expanduser(str(p))))


def _inside(p: Path, root: Path) -> bool:
    return p == root or root in p.parents


def _dotenv_served() -> dict:
    """webapp/.env 의 서빙 폴더 값 {키: 값} — app.py 로더와 같은 해석 (KEY=VALUE · 첫 '=' · strip)."""
    out, p = {}, ROOT / 'webapp' / '.env'
    if p.is_file():
        for ln in p.read_text(encoding='utf-8', errors='replace').splitlines():
            ln = ln.strip()
            if ln and not ln.startswith('#') and '=' in ln:
                k, v = ln.split('=', 1)
                if k.strip() in SERVED_KEYS and v.strip():
                    out[k.strip()] = v.strip()
    return out


def served_roots(case_dirs) -> list:
    """쓰면 안 되는 자리 — 서빙 중 웹앱 폴더 (env · .env · 리포 안 기본값) + 원본 업로드 폴더 · 그 루트 · 루트 옆 results · archive."""
    roots = [os.environ.get(k) for k in SERVED_KEYS] + list(_dotenv_served().values())
    roots += [ROOT / 'webapp' / x for x in ('uploads', 'results', 'archive')]
    for cd in case_dirs:
        cd = _real(cd)
        roots += [cd, cd.parent, cd.parent.parent / 'results', cd.parent.parent / 'archive']
    seen, out = set(), []
    for r in roots:
        if r:
            rr = _real(r)
            if rr not in seen:
                seen.add(rr)
                out.append(rr)
    return out


def isolation_problems(out: Path, case_dirs) -> list:
    out_r = _real(out)
    work = [out_r / 'work' / x for x in ('uploads', 'results', 'archive')]
    bad = []
    for r in served_roots(case_dirs):
        if _inside(out_r, r):
            bad.append(f'--out {out_r} 이 서빙 · 원본 폴더 {r} 안이다')
        for w in work:
            if _inside(r, w):
                bad.append(f'서빙 · 원본 폴더 {r} 가 작업 폴더 {w} 안이다 (작업 폴더를 비우면 지워진다)')
    for cd in case_dirs:
        if _inside(_real(cd), out_r):
            bad.append(f'원본 업로드 폴더 {cd} 가 --out {out_r} 안이다')
    return bad


# ──────────────────────────────── 입력 관문 ────────────────────────────────
def locate(case_dir: Path, want_step=None) -> dict:
    """업로드 폴더 → 같은 step 의 atom · contact · mesh + 덱 + meta.json · 실행 인자 · 관문 기록.  하나라도 어기면 Refuse."""
    case_dir = Path(case_dir)
    if not case_dir.is_dir():
        raise LWB.Refuse(f'업로드 폴더 없음: {case_dir}')
    names = sorted(p.name for p in case_dir.iterdir() if p.is_file())
    dumps = {'atom': {}, 'contact': {}}
    for nm in names:
        m = _RE_DUMP.match(nm)
        if m:
            dumps[m.group(1)][int(m.group(2))] = nm
    meshes = {int(m.group(1)): nm for nm in names for m in [_RE_MESH.match(nm)] if m}
    trio = sorted(set(dumps['atom']) & set(dumps['contact']) & set(meshes))
    if not trio:
        raise LWB.Refuse(f"같은 step 의 atom · contact · mesh 세 파일이 없다 (atom {sorted(dumps['atom'])} · "
                         f"contact {sorted(dumps['contact'])} · mesh {sorted(meshes)}) — 이른 메시로 대신하지 않는다 (LHS-11)")
    want = None if want_step in (None, '') else int(want_step)
    step = want if want in trio else trio[-1]                 # 표가 step 을 주면 그 step (없으면 가장 늦은 세 파일)
    if want is not None and want != step:
        raise LWB.Refuse(f'표의 atom_step {want} 의 세 파일이 없다 (있는 step {trio}) — 다른 프레임이다')
    decks = [nm for nm in names if nm.startswith('input') and nm.endswith('.liggghts')]
    if len(decks) > 1:
        raise LWB.Refuse(f'덱 (input*.liggghts) 이 {len(decks)} 개 — run_pipeline 이 전부 파서에 넘긴다: {decks}')
    if 'meta.json' not in names:
        raise LWB.Refuse('meta.json 없음 — 웹앱 케이스의 mode · type_map · scale 을 알 수 없다')
    try:
        meta = json.loads((case_dir / 'meta.json').read_text(encoding='utf-8'))
    except (OSError, ValueError) as e:
        raise LWB.Refuse(f'meta.json 을 못 읽는다 ({type(e).__name__}: {e})')
    meta = meta if isinstance(meta, dict) else {}
    mode, tm = meta.get('mode'), meta.get('type_map')
    if mode not in ('standard', 'bimodal') or not isinstance(tm, str) or not tm.strip():
        raise LWB.Refuse(f'meta.json mode {mode!r} · type_map {tm!r} — /analyze 가 run_pipeline 에 넘길 값이 없다')
    try:
        scale = int(meta.get('scale', 1000))
    except (TypeError, ValueError):
        raise LWB.Refuse(f"meta.json scale {meta.get('scale')!r} — 정수가 아니다")
    atom, contact = case_dir / dumps['atom'][step], case_dir / dumps['contact'][step]
    #  J20-a ⓑ · DESC-06 — 웹앱 파서는 파일 안 모든 프레임을 이어 붙이고 행마다 CN +1 (lhs_webapp_batch.stage_case 와 같은 관문)
    n_af = H.count_blocks(str(atom), 'ITEM: TIMESTEP')
    if n_af != 1:
        raise LWB.Refuse(f'atom 프레임 {n_af} ≠ 1 — 웹앱 atoms.csv 에 같은 id 가 여러 번 들어간다 (DESC-06)')
    try:
        scan = H.scan_contact_dump(str(contact))
    except H.BedRefusal as e:
        raise LWB.Refuse(f'contact 덤프 점검 실패 — {e}')
    if scan['n_frames'] != 1:
        raise LWB.Refuse(f"contact 프레임 {scan['n_frames']} ≠ 1 — 웹앱 파서가 이어 붙여 CN · 접촉 수가 부푼다 (DESC-06)")
    if scan['n_dup_rows'] or scan['n_self_pairs']:
        raise LWB.Refuse(f"contact 중복 행 {scan['n_dup_rows']} · 자기쌍 {scan['n_self_pairs']} — 웹앱은 행마다 CN 을 +1 한다")
    dump = TMR.types_in_dump(str(atom))
    try:
        m_meta = TMR.parse_map(tm)
    except ValueError as e:
        raise LWB.Refuse(f'meta type_map {tm!r} 해석 실패 ({e})')
    errs, _notes = TMR.validate(m_meta, dump)
    if errs:
        raise LWB.Refuse('meta type_map 이 덤프와 맞지 않는다 — ' + ' · '.join(errs))
    deck = (case_dir / decks[0]) if decks else None
    deck_map, deck_err, agrees = '', '', None
    if deck is not None:
        try:
            m_deck, _n, e_deck = TMR.resolve(deck.read_text(encoding='utf-8', errors='replace'), dump)
            deck_map, deck_err = TMR.format_map(m_deck), '; '.join(e_deck)
            agrees = (m_deck == m_meta) if (m_deck and not e_deck) else None
        except Exception as e:                              # noqa: BLE001 — 기록만 (실행 인자는 meta)
            deck_err = f'{type(e).__name__}: {e}'
    files = [atom.name, contact.name, meshes[step]] + ([deck.name] if deck else []) + ['meta.json']
    return dict(dir=case_dir, files=files, mode=mode, type_map=tm, scale=scale, meta_name=meta.get('name'),
                record=dict(atom_step=step, mode=mode, type_map=tm, scale=scale, meta_name=meta.get('name'),
                            dump_type_counts=','.join(f'{t}:{dump[t]["n"]}' for t in sorted(dump)),
                            type_map_deck=deck_map, type_map_deck_agrees=agrees, type_map_deck_errors=deck_err,
                            deck=(deck.name if deck else None), atom_frames=int(n_af), contact_scan=scan,
                            not_copied=sorted(set(names) - set(files))))


def snapshot(case_dir: Path, files) -> dict:
    """원본 폴더의 목록 (이름 · 크기 · mtime_ns) + 읽은 파일의 sha256 — 실행 전후 대조용."""
    listing = {}
    with os.scandir(case_dir) as it:
        for e in it:
            st = e.stat(follow_symlinks=False)
            listing[e.name] = (st.st_size, st.st_mtime_ns, e.is_dir(follow_symlinks=False))
    return dict(listing=listing, sha={nm: HB.sha256_of(case_dir / nm) for nm in files})


def stage_copy(sel: dict, uploads: Path, case_id: str, sha: dict) -> Path:
    """고른 파일만 작업 폴더로 **복사** (원본 이름 그대로) — 사본 sha256 = 원본."""
    d = uploads / case_id
    if _real(d) == _real(sel['dir']) or _inside(_real(sel['dir']), _real(d)):
        raise LWB.Refuse(f'스테이징 {d} 가 원본 {sel["dir"]} 과 겹친다')
    if d.exists():
        shutil.rmtree(d)                # 옛 파일이 남으면 run_pipeline 의 glob 이 다른 프레임을 섞는다 (SELF-47)
    d.mkdir(parents=True)
    for nm in sel['files']:
        shutil.copy2(sel['dir'] / nm, d / nm)
        if HB.sha256_of(d / nm) != sha[nm]:
            raise LWB.Refuse(f'사본 {nm} 의 sha256 이 원본과 다르다')
    return d


class StageClock:
    """`pipeline_service._RUNNER` 주입점 (시험이 가짜 실행기를 끼우는 그 훅) 의 위임 래퍼 — 명령 · 인자 · 반환을 **그대로** 넘긴다.
    ① 단계 (스크립트) 별 벽시계 초를 재고 ② network solver 가 끝난 직후 그 네 JSON 을 `keep_dir` 에 사본으로 남긴다 (게시 여부와 무관 —
    채널 판정 · 정지 계약이 후보를 치워도 솔버가 낸 값을 볼 수 있게).  계산 · 판정 · 게시는 바꾸지 않는다."""

    def __init__(self, inner, keep_dir):
        self.inner, self.keep_dir, self.calls, self.keep_error = inner, Path(keep_dir), [], ''

    def __call__(self, cmd, **kw):
        script = os.path.basename(str(cmd[1])) if len(cmd) > 1 else str(cmd[0])
        t0, res = time.time(), None
        try:
            res = self.inner(cmd, **kw)
            return res
        finally:
            self.calls.append(dict(script=script, seconds=round(time.time() - t0, 3), rc=getattr(res, 'returncode', None)))
            if script == 'network_conductivity.py':
                self._keep(cmd)

    def _keep(self, cmd):
        try:
            c = [str(x) for x in cmd]
            o = Path(c[c.index('-o') + 1])
            self.keep_dir.mkdir(parents=True, exist_ok=True)
            for n in NET_JSON:
                if (o / n).is_file():
                    shutil.copy2(o / n, self.keep_dir / n)
        except Exception as e:                              # noqa: BLE001 — 사본은 증거일 뿐 (파이프라인을 세우지 않는다)
            self.keep_error = f'{type(e).__name__}: {e}'


# ──────────────────────────────── 한 케이스 ────────────────────────────────
def bind_folders(A, work: Path) -> None:
    """app.config 의 데이터 폴더를 작업 폴더로 (app 이 먼저 import 됐어도 — 같은 프로세스 재호출 포함)."""
    for key, sub in (('UPLOAD_FOLDER', 'uploads'), ('RESULTS_FOLDER', 'results'), ('ARCHIVE_FOLDER', 'archive')):
        A.app.config[key] = str(work / sub)


def run_case(c: dict, A, work: Path, out: Path) -> dict:
    rec = dict(case_id=c['id'], when=time.strftime('%Y-%m-%dT%H:%M:%S'), stop_after=STOP_AFTER)
    t0 = time.time()
    ps = A._ps
    rd, keep = work / 'results' / c['id'], out / 'solver_output' / c['id']
    try:
        for d in (rd, keep):
            if d.exists():
                shutil.rmtree(d)        # 옛 세대가 이번 기록 밑에 남지 않게 (거부돼도) — 첫 실행과 같은 빈 자리
        sel = locate(c['dir'], c.get('atom_step'))
        rec.update(sel['record'])
        before = snapshot(sel['dir'], sel['files'])
        rec['source_sha256'] = before['sha']
        stage_copy(sel, work / 'uploads', c['id'], before['sha'])
        cd_r, rd_r = _real(A.get_case_dir(c['id'])), _real(A.get_results_dir(c['id']))
        if cd_r != _real(work / 'uploads' / c['id']) or rd_r != _real(rd):
            raise LWB.Refuse(f'격리 실패 — 웹앱이 케이스를 {cd_r} · {rd_r} 로 해석한다 (작업 폴더 밖)')
        clock = StageClock(ps._RUNNER, keep)
        prev, prev_cwd = ps._RUNNER, os.getcwd()
        #  CWD = 작업 폴더 안 — 피복 단계가 요약 CSV 를 **CWD 상대** `docs/figures/physics_regime/` 에 쓴다 (LHS-27 · 코드 체크아웃을
        #  더럽힌다).  단계 스크립트의 import 폐포에서 CWD 상대 경로는 그 출력 하나뿐이다 (입력은 전부 절대 경로) ⇒ 값 불변.
        run_cwd = work / 'cwd' / c['id']
        if run_cwd.exists():
            shutil.rmtree(run_cwd)
        run_cwd.mkdir(parents=True)
        ps._RUNNER = clock
        try:
            os.chdir(run_cwd)
            t1 = time.time()
            res = A.run_pipeline(c['id'], sel['mode'], sel['type_map'], sel['scale'],
                                 figures=False, auto_db=False, stop_after=STOP_AFTER)
            rec['elapsed_pipeline_s'] = round(time.time() - t1, 1)
        finally:
            ps._RUNNER = prev
            os.chdir(prev_cwd)
        log = [s for s in (res.get('log') or []) if isinstance(s, dict)]
        stop = next((s for s in log if str(s.get('step', '')).startswith(STOP_STEP)), None)
        rec.update(status=res.get('status') or ('done' if res.get('success') else 'failed'),
                   failed_stages=[str(x) for x in (res.get('failed_stages') or [])],
                   stopped_after=res.get('stopped_after'), run_network_run_id=res.get('network_run_id'),
                   stop_contract_ok=(None if stop is None else bool(stop.get('ok'))),
                   stop_contract_msg=(None if stop is None else (stop.get('stdout') if stop.get('ok') else stop.get('stderr'))),
                   stage_seconds=clock.calls,
                   elapsed_network_solver_s=round(sum(x['seconds'] for x in clock.calls
                                                      if x['script'] == 'network_conductivity.py'), 3))
        if res.get('error') and not rec['failed_stages']:
            rec['why'] = str(res['error'])[:500]
        if clock.keep_error:
            rec['solver_output_copy_error'] = clock.keep_error
        (out / 'logs').mkdir(parents=True, exist_ok=True)
        (out / 'logs' / f"{c['id']}.stages.json").write_text(json.dumps(log, ensure_ascii=False, indent=1, default=str),
                                                             encoding='utf-8')
        after = snapshot(sel['dir'], sel['files'])
        rec['source_unchanged'] = (after == before)
        if not rec['source_unchanged']:
            rec.update(status='failed', why='⛔ 원본 업로드 폴더가 실행 전후로 달라졌다 (sha256 · 목록) — 격리 위반 '
                                            '(또는 웹앱이 같은 케이스를 동시에 건드렸다) · 값은 사본에서 낸 것이지만 확인할 것')
    except LWB.Refuse as e:
        rec.update(status='REFUSED', why=str(e))
    except Exception as e:                                  # noqa: BLE001 — 한 케이스가 배치를 세우지 않게
        rec.update(status='failed', why=f'{type(e).__name__}: {e}')
    rec['elapsed_case_s'] = round(time.time() - t0, 1)
    return rec


def _load(p: Path):
    try:
        with open(p, encoding='utf-8') as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def extract_row(c: dict, rec: dict, work: Path, out: Path, ps) -> dict:
    """한 행 — 값은 **생산된 파일**에서만 (게시 세대 = results/<id> · 아니면 솔버 출력 사본 · 표지)."""
    row = {'case_id': c['id'], 'P_S': c.get('P_S'), 'bed': c.get('bed'), 'webapp_name': c.get('webapp_name'),
           'meta_name': rec.get('meta_name'), 'run_status': rec.get('status'), 'why': rec.get('why'),
           'failed_stages': rec.get('failed_stages')}
    for k in RUN_KEYS + ('stop_contract_ok', 'elapsed_network_solver_s', 'elapsed_pipeline_s'):
        row[k] = rec.get(k)
    rd, keep = work / 'results' / c['id'], out / 'solver_output' / c['id']
    ran = rec.get('status') not in ('REFUSED', 'not_run') and rd.is_dir()     # 거부 · 미실행 행은 파일을 읽지 않는다
    fm = (_load(rd / 'full_metrics.json') if ran else None) or {}
    prov = ps.read_network_provenance(str(rd)) if ran else {}
    pub = _load(rd / 'network_conductivity_dual.json') if ran else None
    cand = _load(keep / 'network_conductivity_dual.json') if ran else None
    if isinstance(pub, dict) and prov.get('solver_status') == 'success':
        dual, src = pub, 'published'
    elif isinstance(cand, dict):
        dual, src = cand, 'solver_output_not_published'
    else:
        dual, src = None, ''
    row['values_source'] = src
    recs = {tail: ((dual or {}).get(dkey) if isinstance((dual or {}).get(dkey), dict) else {}) for dkey, tail in MODES}
    for tail, r in recs.items():
        for k in NET_KEYS:
            row[f'{k}_{tail}'] = r.get(k)
        for ch in ('ion', 'el', 'th'):
            k = f'constriction_power_share_{ch}_{tail}'
            row[k], row[k + '_status'] = r.get(k), r.get(k + '_status')
    s0 = [recs[t].get('sigma_grain_S_cm') for t in ('hertz', 'physics')]
    row['sigma_grain_S_cm'] = s0[0] if s0[0] == s0[1] else None
    row['sigma_grain_modes_agree'] = (s0[0] == s0[1]) if any(v is not None for v in s0) else None
    tp = recs['hertz'].get('temperature_provenance') if isinstance(recs['hertz'].get('temperature_provenance'), dict) else {}
    row['T_dependence'], row['T_C'], row['T_ref_C'] = tp.get('T_dependence'), tp.get('T_C'), tp.get('T_ref_C')
    for k in FM_KEYS:
        row[k] = fm.get(k)
    row.update(TF.ion_columns(dual, fm, fm.get('percolation_pct')))      # = tau_flux.case_row 의 함수 (같은 입력)
    s0w = None
    for m in ('hertz', 'physics'):                          # 웹앱 τ 블록 = 게시된 full_metrics 에서만 (아니면 기본 σ₀ 3.0 이 파일 밖에서 들어온다)
        t2, s0m = TF.tau2_from_metrics(fm, m) if src == 'published' else (None, None)
        row[f'webapp_tau2_ion_{m}'] = t2
        s0w = s0w if s0w is not None else s0m
    row['webapp_sigma0_mScm'] = s0w
    view = ps.network_status_view(str(rd)) if ran else {}
    for k in VIEW_KEYS:
        row[k] = view.get(k)
    row['network_code_sha'] = prov.get('code_sha')
    return row


def column_order(rows) -> list:
    cols = list(LEAD)
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    return cols


def _cell(v) -> str:
    if v is None:
        return ''
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, float):
        return repr(v)                  # 반올림하지 않는다 (파일 값 그대로)
    if isinstance(v, (list, tuple)):
        v = '; '.join(str(x) for x in v)
    elif isinstance(v, dict):
        v = json.dumps(v, ensure_ascii=False, sort_keys=True)
    return str(v).replace('\t', ' ').replace('\r', ' ').replace('\n', ' ')


def _atomic_text(p: Path, txt: str) -> None:
    tmp = p.with_name('.' + p.name + '.tmp')
    tmp.write_text(txt, encoding='utf-8')
    os.replace(tmp, p)


def write_outputs(out: Path, stem: str, status: dict, rows: list) -> None:
    out.mkdir(parents=True, exist_ok=True)
    _atomic_text(out / 'status.json', json.dumps(status, ensure_ascii=False, indent=1, default=str) + '\n')
    cols = column_order(rows)
    txt = '\t'.join(cols) + '\n' + ''.join('\t'.join(_cell(r.get(c)) for c in cols) + '\n' for r in rows)
    _atomic_text(out / f'{stem}.tsv', txt)
    doc = dict(schema=SCHEMA, generated=time.strftime('%Y-%m-%dT%H:%M:%S'), stop_after=STOP_AFTER,
               code=(status.get('runs') or [{}])[-1], columns=cols, column_notes=COLUMN_NOTES, rows=rows)
    _atomic_text(out / f'{stem}.json', json.dumps(doc, ensure_ascii=False, indent=1, default=str) + '\n')


# ──────────────────────────────── 배치 ────────────────────────────────
def default_uploads_root() -> Path:
    """웹앱이 쓰는 업로드 폴더 — env → webapp/.env → 리포 안 기본값 (app.py 와 같은 순서)."""
    v = os.environ.get('WEBAPP_UPLOAD_FOLDER') or _dotenv_served().get('WEBAPP_UPLOAD_FOLDER')
    return Path(v).expanduser() if v else ROOT / 'webapp' / 'uploads'


def load_cases(args) -> list:
    up = _real(args.uploads_root if args.uploads_root else default_uploads_root())   # 절대 경로 (실행 중 CWD 를 작업 폴더로 옮긴다)
    cases = []
    if args.from_tsv:
        with open(args.from_tsv, encoding='utf-8', newline='') as fh:
            rd = csv.DictReader((ln for ln in fh if not ln.startswith('#')), delimiter='\t')
            for r in rd:
                cid = (r.get('webapp_case_id') or '').strip()
                if cid:
                    cases.append(dict(id=cid, dir=up / cid, P_S=(r.get('P_S') or '').strip() or None,
                                      bed=(r.get('case') or '').strip() or None,
                                      webapp_name=(r.get('webapp_name') or '').strip() or None,
                                      atom_step=(r.get('atom_step') or '').strip() or None))
    for spec in args.case:
        key, _, lab = spec.partition('=')
        p = Path(key).expanduser()
        d = _real(p) if (os.sep in key or p.is_dir()) else up / key   # 경로면 실제 폴더 이름이 id (심볼릭 링크 'post' 가 id 가 되지 않게)
        cases.append(dict(id=d.name, dir=d, P_S=lab or None))
    if args.only:
        cases = [c for c in cases if c['id'] in set(args.only)]
    seen, uniq = set(), []
    for c in cases:
        if c['id'] not in seen:
            seen.add(c['id'])
            uniq.append(c)
    return uniq


def _versions() -> dict:
    v = dict(python=platform.python_version(), platform=platform.platform())
    for mod in ('numpy', 'scipy'):
        try:
            v[mod] = __import__(mod).__version__
        except Exception:                                   # noqa: BLE001
            v[mod] = None
    return v


def _fmt(v) -> str:
    return '—' if v is None or v == '' else (f'{v:.4g}' if isinstance(v, float) else str(v))


def print_summary(rows) -> None:
    print('\n케이스 · P:S · 상태 · 값 출처 | σ_ion FULL H / P | σ_ion CF H / P | σ_e FULL H / P | σ_e CF/FULL H | κ FULL H | '
          'tau2_ion H / P | 망 솔버 s')
    for r in rows:
        print(f"{r['case_id']} · {_fmt(r.get('P_S'))} · {r.get('run_status')} · {r.get('values_source') or '—'} | "
              f"{_fmt(r.get('sigma_full_mScm_hertz'))} / {_fmt(r.get('sigma_full_mScm_physics'))} | "
              f"{_fmt(r.get('sigma_bulk_net_mScm_hertz'))} / {_fmt(r.get('sigma_bulk_net_mScm_physics'))} | "
              f"{_fmt(r.get('electronic_sigma_full_mScm_hertz'))} / {_fmt(r.get('electronic_sigma_full_mScm_physics'))} | "
              f"{_fmt(r.get('electronic_R_brug_hertz'))} | {_fmt(r.get('thermal_sigma_full_mScm_hertz'))} | "
              f"{_fmt(r.get('tau2_ion_hertz'))} / {_fmt(r.get('tau2_ion_physics'))} | {_fmt(r.get('elapsed_network_solver_s'))}")


def run_batch(args) -> int:
    cases = load_cases(args)
    if not cases:
        print('⛔ 케이스가 없다 (--from-tsv · --case · --only 확인)', file=sys.stderr)
        return 2
    if args.check_only:
        bad = 0
        for c in cases:
            try:
                sel = locate(c['dir'], c.get('atom_step'))
                r = sel['record']
                print(f"[관문 통과] {c['id']} {c.get('P_S') or ''} — step {r['atom_step']} · mode {r['mode']} · type_map {r['type_map']} "
                      f"(덱 판독 {r['type_map_deck'] or '—'} · 일치 {r['type_map_deck_agrees']}) · scale {r['scale']} · "
                      f"type 개수 {r['dump_type_counts']} · 복사 {sel['files']} · 안 복사 {r['not_copied'] or '없음'}")
            except LWB.Refuse as e:
                bad += 1
                print(f"[REFUSED] {c['id']} {c.get('P_S') or ''} — {e}")
        return 1 if bad else 0
    out = Path(args.out).expanduser().resolve()
    bad = isolation_problems(out, [c['dir'] for c in cases])
    if bad:
        print('⛔ 격리 관문 — 아무것도 하지 않는다:\n  ' + '\n  '.join(bad), file=sys.stderr)
        return 2
    work = out / 'work'
    env_keep = {k: os.environ.get(k) for k in ENV_KEYS}
    try:
        LWB.prepare_env(work)                               # app import 전에 — 폴더 = 작업 폴더 · 원격 저장소 끔
        os.environ['WEBAPP_MPM_LAB_FOLDER'] = str(work / 'mpm_lab')
        A, _TMR, _EM = LWB.load_deps()
        bind_folders(A, work)
        prev = _load(out / 'status.json')
        status = prev if (isinstance(prev, dict) and prev.get('schema') == SCHEMA) else dict(schema=SCHEMA, cases={})
        status['stop_after'] = STOP_AFTER
        status.setdefault('runs', []).append(dict(started=time.strftime('%Y-%m-%dT%H:%M:%S'), argv=sys.argv[1:],
                                                  **LWB.code_provenance(), **_versions()))
        n_run, t_all = 0, time.time()
        for i, c in enumerate(cases, 1):
            old = status['cases'].get(c['id']) or {}
            if old.get('status') in KEEP_STATUS and not args.force:
                print(f"[{i}/{len(cases)}] {c['id']} {c.get('P_S') or ''} — 이미 {old['status']} · 건너뜀 (--force 로 다시)", flush=True)
                continue
            print(f"[{i}/{len(cases)}] {c['id']} {c.get('P_S') or ''} — 파싱 → 접촉 → 피복 → 망 (stop_after=network) 실행 중 … "
                  f"(웹앱이 같은 기계에서 솔버를 돌리면 lock 을 기다린다)", flush=True)
            rec = run_case(c, A, work, out)
            n_run += 1
            status['cases'][c['id']] = rec
            rows = [extract_row(x, status['cases'].get(x['id']) or {'status': 'not_run'}, work, out, A._ps) for x in cases]
            write_outputs(out, args.name, status, rows)
            print(f"[{i}/{len(cases)}] {c['id']} {rec['status']} · 망 솔버 {rec.get('elapsed_network_solver_s', '—')} s · "
                  f"파이프라인 {rec.get('elapsed_pipeline_s', '—')} s · 케이스 {rec['elapsed_case_s']} s"
                  + (f" · {rec.get('why')}" if rec.get('why') else '')
                  + (f" · 실패 단계 {rec.get('failed_stages')}" if rec.get('failed_stages') else ''), flush=True)
        rows = [extract_row(x, status['cases'].get(x['id']) or {'status': 'not_run'}, work, out, A._ps) for x in cases]
        write_outputs(out, args.name, status, rows)
        print_summary(rows)
        counts = {}
        for c in cases:
            s = (status['cases'].get(c['id']) or {}).get('status', 'not_run')
            counts[s] = counts.get(s, 0) + 1
        print(f'\n상태: {counts} · 이번 실행 {n_run} 건 · {time.time() - t_all:.0f} s → {out}/{args.name}.tsv · .json · status.json · logs/')
        return 0 if all(k in KEEP_STATUS for k in counts) else 1
    finally:
        for k, v in env_keep.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


# ───────────────────────────────── selftest ─────────────────────────────────
def _write_upload(d: Path, TP, bed: str, meta: dict, step=100, two_frames=False, dup_row=False, contact_step=None) -> None:
    """합성 웹앱 업로드 폴더 — 원자 · 접촉은 test_pipeline_provenance 의 침대 (`_bed`) 그대로 (LIGGGHTS 덤프 모양)."""
    A, C, plate, box = TP._bed(bed)
    d.mkdir(parents=True, exist_ok=True)
    head = (f'ITEM: TIMESTEP\n{step}\nITEM: NUMBER OF ATOMS\n{len(A)}\nITEM: BOX BOUNDS pp pp ff\n0 {box}\n0 {box}\n0 {plate}\n'
            'ITEM: ATOMS id type x y z radius\n')
    body = ''.join(f"{i} {a['type']} {a['x']!r} {a['y']!r} {a['z']!r} {a['radius']!r}\n" for i, a in A.items())
    (d / f'atom_{step}.liggghts').write_text(head + body + ((head + body) if two_frames else ''))
    rows = [(c['id1'], c['id2'], c['contact_area'], c['delta']) for c in C] + ([(C[0]['id2'], C[0]['id1'], 0.1, 0.05)] if dup_row else [])
    cs = contact_step if contact_step is not None else step
    (d / f'contact_{cs}.liggghts').write_text(
        f'ITEM: TIMESTEP\n{cs}\nITEM: NUMBER OF ENTRIES\n{len(rows)}\nITEM: ENTRIES c_cpl[7] c_cpl[8] c_cpl[9] c_cpl[22] c_cpl[23]\n'
        + ''.join(f'{a} {b} 0 {ar!r} {dl!r}\n' for a, b, ar, dl in rows))
    (d / f'mesh_{step}.stl').write_text('solid p\n' + ''.join(
        'facet normal 0 0 1\nouter loop\n' + ''.join(f'vertex {x} {y} {plate}\n' for x, y in tri) + 'endloop\nendfacet\n'
        for tri in (((0, 0), (box, 0), (box, box)), ((0, 0), (box, box), (0, box)))) + 'endsolid p\n')
    (d / 'input_wnb.liggghts').write_text(
        'variable r_SE equal 1.0\nvariable r_AM_P equal 1.0\n'
        'fix pts1 all particletemplate/sphere 15485863 atom_type 1 density constant 1800 radius constant ${r_SE}\n'
        'fix pts2 all particletemplate/sphere 15485867 atom_type 2 density constant 4800 radius constant ${r_AM_P}\n')
    if meta is not None:
        (d / 'meta.json').write_text(json.dumps(meta), encoding='utf-8')


def _selftest() -> int:
    fails = []

    def chk(name, ok, detail=''):
        print(('  ✓ ' if ok else '  ✗ ') + name + (f'  [{detail}]' if (detail and not ok) else ''))
        if not ok:
            fails.append(name)

    tmp = Path(tempfile.mkdtemp(prefix='wnb_'))
    env_keep = {k: os.environ.get(k) for k in ENV_KEYS}
    try:
        LWB.prepare_env(tmp / 'boot')                       # app import 전에 — 원격 저장소 끔 · 폴더 = 임시 (run_batch 가 다시 맞춘다)
        A, _TMR, _EM = LWB.load_deps()
        sys.path.insert(0, str(ROOT / 'webapp'))
        import test_pipeline_provenance as TP              # noqa: E402  실 생산자 대역 (_CLIRunner = network_conductivity CLI 그대로) · 침대
        ps = A._ps
        BED, TM = 'se_am', '1:SE,2:AM_P'                    # SE 사슬 + AM 사슬 — 이온 · 전자 · 열 세 채널 (test_pipeline_provenance T18)
        served = tmp / 'served'
        up = served / 'uploads'
        cid = 'wnb_selftest_ok'
        meta_ok = dict(name='selftest', mode='standard', type_map=TM, scale=1, status='done')
        _write_upload(up / cid, TP, BED, meta_ok)
        (served / 'results').mkdir(parents=True)
        calls = dict(pipeline=[], upstream=[])

        def _upstream(cmd, **kw):
            """파싱 · 접촉 · 피복 대역 — 결과 폴더에 그 침대의 CSV · 장부를 쓴다 (test_network_handover_chain · T12 와 같은 자리)."""
            c = [str(x) for x in cmd]
            script = os.path.basename(c[1])
            calls['upstream'].append(c)
            if script == 'parse_liggghts.py':
                TP._write_bed(c[c.index('-o') + 1], BED)
            elif script in ('analyze_contacts.py', 'analyze_contacts_bimodal.py'):
                o = c[c.index('-o') + 1]
                with open(os.path.join(o, 'full_metrics.json'), 'w') as f:
                    json.dump(TP._bed_ledger(BED), f)
                for n in ('atoms_analyzed.csv', 'contacts_analyzed.csv', 'network_summary.csv'):
                    with open(os.path.join(o, n), 'w') as f:
                        f.write('a\n')
            elif script == 'coverage_physics_vs_hertzian.py':
                calls.setdefault('cov_cwd', []).append(os.getcwd())     # 실 피복 단계는 CWD 상대로 요약 CSV 를 쓴다 (LHS-27)
            else:
                raise AssertionError(f'망 정지 경로에 없어야 할 단계: {script}')
            return subprocess.CompletedProcess(cmd, 0, f'stand-in {script}', '')

        orig_run = A.run_pipeline

        def _spy(*a, **k):
            calls['pipeline'].append((a, k))
            return orig_run(*a, **k)
        prev_runner = ps._RUNNER
        A.run_pipeline, ps._RUNNER = _spy, TP._CLIRunner(delegate=_upstream)
        try:
            out = tmp / 'out'
            base = ['--uploads-root', str(up), '--out', str(out)]
            before = snapshot(up / cid, sorted(p.name for p in (up / cid).iterdir()))
            cwd0 = os.getcwd()
            rc = run_batch(_parse(base + ['--case', f'{cid}=7:3']))
            st = json.loads((out / 'status.json').read_text(encoding='utf-8'))
            r0 = st['cases'].get(cid) or {}
            a0, k0 = calls['pipeline'][0] if calls['pipeline'] else ((), {})
            con = next((u for u in calls['upstream'] if os.path.basename(u[1]) == 'analyze_contacts.py'), [])
            scripts = [os.path.basename(u[1]) for u in calls['upstream']]
            chk('① 정상 — done · run_pipeline 1 회 · 인자 = meta 의 (mode · type_map · scale) + figures=False · auto_db=False · '
                "stop_after='network'", rc == 0 and r0.get('status') == 'done' and len(calls['pipeline']) == 1
                and a0 == (cid, 'standard', TM, 1) and k0 == dict(figures=False, auto_db=False, stop_after='network'), str((rc, r0.get('why'), a0, k0)))
            chk('① 접촉 단계에 meta type_map · scale 그대로 (-t 1:SE,2:AM_P -s 1) · 망 뒤 단계 (Stage E · 이중 공극률 · 고급 분석) 0 회',
                con[con.index('-t') + 1:con.index('-t') + 2] == [TM] and con[con.index('-s') + 1:con.index('-s') + 2] == ['1']
                and scripts == ['parse_liggghts.py', 'analyze_contacts.py', 'coverage_physics_vs_hertzian.py'], str(scripts))
            chk('① 망 정지 계약 통과 (stop_contract_ok) · 망 솔버 시간 > 0 · 단계별 시간에 network_conductivity.py',
                r0.get('stop_contract_ok') is True and (r0.get('elapsed_network_solver_s') or 0) > 0
                and any(x['script'] == 'network_conductivity.py' for x in r0.get('stage_seconds') or []))
            # ② 격리
            stg = out / 'work' / 'uploads' / cid
            chk('② ★ 원본 업로드 폴더 바이트 (sha256) · 목록 (이름 · 크기 · mtime) 그대로 · source_unchanged True',
                snapshot(up / cid, sorted(before['sha'])) == before and r0.get('source_unchanged') is True)
            chk('② ★ 스테이징 = 사본 (심볼릭 링크 아님 · 바이트 동일) · 같은 step 세 파일 + 덱 + meta.json 만',
                sorted(p.name for p in stg.iterdir()) == sorted(['atom_100.liggghts', 'contact_100.liggghts', 'mesh_100.stl',
                                                                 'input_wnb.liggghts', 'meta.json'])
                and not any(p.is_symlink() for p in stg.iterdir())
                and all(HB.sha256_of(stg / n) == before['sha'][n] for n in before['sha']))
            chk('② ★ 서빙 폴더 (원본 옆 results · 리포 안 webapp/uploads|results) 에 이 케이스가 생기지 않았다 · app.config = 작업 폴더',
                not (served / 'results' / cid).exists() and not (ROOT / 'webapp' / 'results' / cid).exists()
                and not (ROOT / 'webapp' / 'uploads' / cid).exists()
                and A.app.config['RESULTS_FOLDER'] == str(out.resolve() / 'work' / 'results'))
            chk('② env 되돌림 — run_batch 뒤 WEBAPP_RESULTS_FOLDER 가 실행 전 값',
                os.environ.get('WEBAPP_RESULTS_FOLDER') == str(tmp / 'boot' / 'results'))
            chk('② ★ 단계 CWD = 작업 폴더 안 (피복 단계의 CWD 상대 요약 CSV 가 코드 체크아웃에 안 쓰인다 · LHS-27) · 끝나면 CWD 되돌림',
                bool(calls.get('cov_cwd')) and all(_inside(_real(x), _real(out / 'work')) for x in calls['cov_cwd'])
                and os.getcwd() == cwd0, str(calls.get('cov_cwd')))
            # ③ 표 = 생산 파일
            rd = out / 'work' / 'results' / cid
            dual = json.loads((rd / 'network_conductivity_dual.json').read_text())
            fm = json.loads((rd / 'full_metrics.json').read_text())
            with open(out / 'network_cases.tsv', encoding='utf-8', newline='') as fh:
                trows = list(csv.DictReader(fh, delimiter='\t'))
            jrow = json.loads((out / 'network_cases.json').read_text(encoding='utf-8'))['rows'][0]
            t0 = trows[0] if trows else {}

            def _same(col, want):
                got = t0.get(col)
                return (got == '' and want is None) or (got == _cell(want))
            mism = []
            for dkey, tail in MODES:
                for k in ('sigma_full_mScm', 'sigma_bulk_net_mScm', 'sigma_constr_net_mScm', 'R_brug_over_full', 'percolating_fraction',
                          'sigma_full_status', 'electronic_sigma_full_mScm', 'electronic_R_brug', 'electronic_percolating_fraction',
                          'electronic_status', 'thermal_sigma_full_mScm', 'thermal_status', 'phi_se', 'boundary_rule'):
                    if not _same(f'{k}_{tail}', dual[dkey].get(k)):
                        mism.append(f'{k}_{tail}')
            for k in ('phi_se', 'phi_se_mass_conserving', 'thickness_um', 'percolation_pct', 'network_run_id'):
                if not _same(k, fm.get(k)):
                    mism.append(k)
            tau = TF.case_row(str(rd))
            mism += [k for k in TF.column_names() if not _same(k, tau.get(k))]
            view = ps.network_status_view(str(rd))
            mism += [k for k in VIEW_KEYS if not _same(k, view.get(k))]
            chk(f'③ ★ TSV 칸 = 생산 파일 (두 모드 σ_ion FULL · CF · σ_e · CF/FULL 비 · κ · 상태 · 관통 분율 = dual · 장부 = full_metrics · '
                f'τ 인계 = tau_flux.case_row · 세대 = network_status_view) {mism or ""}',
                len(trows) == 1 and not mism and t0.get('values_source') == 'published')
            chk('③ 값이 실제로 있다 (빈칸 비교로 통과하지 않게): σ_ion FULL · σ_e FULL 두 모드 양수 · computed · tau2 OK · 세 채널 computed',
                all(isinstance(dual[m].get(k), float) and dual[m][k] > 0 for m in ('hertzian', 'physics')
                    for k in ('sigma_full_mScm', 'sigma_bulk_net_mScm', 'electronic_sigma_full_mScm'))
                and t0.get('sigma_full_status_hertz') == 'computed' and t0.get('ion_net_status_hertz') == 'OK'
                and all(t0.get(f'{ch}_status_physics') == 'computed' for ch in ('ionic', 'electronic', 'thermal'))
                and float(t0.get('tau2_ion_hertz') or 0) > 0)
            chk('③ JSON 행 = TSV 행 (숫자 비트 동일 · 같은 열) · 열 설명 동봉',
                jrow.get('sigma_full_mScm_hertz') == dual['hertzian']['sigma_full_mScm']
                and jrow.get('electronic_sigma_full_mScm_physics') == dual['physics']['electronic_sigma_full_mScm']
                and 'column_notes' in json.loads((out / 'network_cases.json').read_text(encoding='utf-8')))
            chk('③ 세대 도장 일치 — run_pipeline 반환 = full_metrics network_run_id = 활성 도장',
                r0.get('run_network_run_id') and r0.get('run_network_run_id') == fm.get('network_run_id') == view.get('active_network_run_id'))
            # ④ 재개 · --force
            n1 = len(calls['pipeline'])
            run_batch(_parse(base + ['--case', f'{cid}=7:3']))
            chk('④ 재개: done 케이스는 다시 돌리지 않는다 (run_pipeline 0 회)', len(calls['pipeline']) == n1)
            # ⑤ 정지 계약 거부 — 생산자 출력 뒤 띠 규칙 'L9' 변이 (⑤ 위반).  앞 실행의 게시 세대가 남아 있어도 결과 폴더를 비우고 돈다.
            ps._RUNNER = TP._CLIRunner(delegate=_upstream, mutate=lambda o: TP._edit_net_records(
                o, lambda r, _n, _m: r.update(boundary_rule='L9')))
            run_batch(_parse(base + ['--case', f'{cid}=7:3', '--force']))
            ps._RUNNER = TP._CLIRunner(delegate=_upstream)
            st5 = json.loads((out / 'status.json').read_text(encoding='utf-8'))['cases'][cid]
            with open(out / 'network_cases.tsv', encoding='utf-8', newline='') as fh:
                t5 = list(csv.DictReader(fh, delimiter='\t'))[0]
            keep = out / 'solver_output' / cid
            cand = json.loads((keep / 'network_conductivity_dual.json').read_text()) if (keep / 'network_conductivity_dual.json').exists() else {}
            chk('⑤ ★ --force 로 다시 (run_pipeline +1) · 정지 계약 거부 → failed · 게시 dual 없음 (옛 게시 세대도 안 남음)',
                len(calls['pipeline']) == n1 + 1 and st5.get('status') == 'failed' and st5.get('stop_contract_ok') is False
                and not (rd / 'network_conductivity_dual.json').exists(), str(st5.get('failed_stages')))
            chk('⑤ ★ 표 = 솔버 출력 사본 (values_source = solver_output_not_published · boundary_rule L9 · σ = 사본 값) · '
                '최근 시도 failed · candidate_rejected · 단계 = 망 정지 계약',
                t5.get('values_source') == 'solver_output_not_published' and t5.get('boundary_rule_hertz') == 'L9'
                and t5.get('sigma_full_mScm_hertz') == _cell(cand.get('hertzian', {}).get('sigma_full_mScm'))
                and t5.get('latest_attempt_status') == 'failed' and t5.get('failure_kind') == 'candidate_rejected'
                and str(t5.get('latest_attempt_stage', '')).startswith(STOP_STEP) and t5.get('run_status') == 'failed', str(t5.get('values_source')))
            # ⑥ 입력 관문 — 실행 0 회
            bads = {'wnb_two_frames': dict(two_frames=True), 'wnb_dup_row': dict(dup_row=True),
                    'wnb_no_meta': dict(meta=None), 'wnb_step_gap': dict(contact_step=90),
                    'wnb_map_missing_type': dict(meta=dict(meta_ok, type_map='1:SE'))}
            for nm, kw in bads.items():
                _write_upload(up / nm, TP, BED, kw.pop('meta', meta_ok), **kw)
            tsv = tmp / 'cases.tsv'
            tsv.write_text('case\twebapp_case_id\tP_S\tatom_step\nps_x\t' + cid + '\t7:3\t999\n', encoding='utf-8')
            n6 = len(calls['pipeline'])
            out6 = tmp / 'out6'
            rc6 = run_batch(_parse(['--uploads-root', str(up), '--out', str(out6), '--from-tsv', str(tsv)]
                                   + sum((['--case', nm] for nm in bads), [])))
            s6 = json.loads((out6 / 'status.json').read_text(encoding='utf-8'))['cases']
            got6 = {k: (v.get('status'), (v.get('why') or '')[:40]) for k, v in s6.items()}
            chk(f'⑥ ★ atom 두 프레임 · 같은 쌍 두 행 · meta.json 없음 · 같은 step 세 파일 없음 · meta map 에 덤프 type 빠짐 · '
                f'표 atom_step ≠ 실제 → 전부 REFUSED · run_pipeline 0 회 · rc 1 {got6 if len(calls["pipeline"]) != n6 else ""}',
                rc6 == 1 and len(s6) == 6 and all(v.get('status') == 'REFUSED' for v in s6.values()) and len(calls['pipeline']) == n6,
                str(got6))
            # ⑦ 격리 관문 — --out 이 원본 업로드 루트 안 · 원본이 --out 안 → rc 2 · 아무것도 안 씀
            n7 = len(calls['pipeline'])
            rc7a = run_batch(_parse(['--uploads-root', str(up), '--out', str(up / 'x_out'), '--case', cid]))
            rc7b = run_batch(_parse(['--uploads-root', str(up), '--out', str(served), '--case', cid]))
            chk('⑦ ★ --out 이 원본 업로드 루트 안 · 원본을 품은 폴더 → rc 2 · 실행 0 · 폴더 미생성',
                rc7a == 2 and rc7b == 2 and len(calls['pipeline']) == n7 and not (up / 'x_out').exists())
            # ⑧ --check-only — 관문만 (복사 · 실행 · 쓰기 없음)
            out8 = tmp / 'out8'
            rc8 = run_batch(_parse(['--uploads-root', str(up), '--out', str(out8), '--case', cid, '--check-only']))
            rc8b = run_batch(_parse(['--uploads-root', str(up), '--out', str(out8), '--case', 'wnb_two_frames', '--check-only']))
            chk('⑧ --check-only: 정상 rc 0 · 거부 rc 1 · run_pipeline 0 회 · --out 미생성',
                rc8 == 0 and rc8b == 1 and len(calls['pipeline']) == n7 and not out8.exists())
        finally:
            A.run_pipeline, ps._RUNNER = orig_run, prev_runner
    finally:
        for k, v in env_keep.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'\n{"✓ 전부 통과" if not fails else f"✗ {len(fails)} 건 실패"}')
    return 0 if not fails else 1


def _parse(argv=None):
    ap = argparse.ArgumentParser(description='웹앱 케이스 → 웹앱 파이프라인 그대로 network 단계까지 (stop_after=network) · 격리 작업 폴더 · σ 표')
    ap.add_argument('--uploads-root', default='',
                    help='원본 웹앱 업로드 폴더 (케이스 id 를 찾는 곳 · 읽기만) — 기본 = env WEBAPP_UPLOAD_FOLDER → webapp/.env → 리포 안 webapp/uploads')
    ap.add_argument('--from-tsv', default='',
                    help='케이스 표 (탭) — 열 webapp_case_id (필수) · P_S · case · webapp_name · atom_step (있으면 고른 step 과 대조)')
    ap.add_argument('--case', action='append', default=[],
                    help='케이스 id (업로드 루트 아래) 또는 업로드 폴더 경로 · 뒤에 =라벨 (예: 260925_000001_0bee25=0:10) — 여러 번')
    ap.add_argument('--only', action='append', default=[], help='이 id 만 (여러 번 · 한 건 먼저 돌려 시간 확인)')
    ap.add_argument('--out', default='', help='산출 폴더 (work · logs · solver_output · 표) — 서빙 폴더 밖 (리포 밖 권장)')
    ap.add_argument('--name', default='network_cases', help='표 파일 이름 (기본 network_cases → .tsv · .json)')
    ap.add_argument('--force', action='store_true', help='done · partial 케이스도 다시 돌린다')
    ap.add_argument('--check-only', action='store_true', help='관문만 (파일 고르기 · 프레임 · 중복 쌍 · meta) — 복사 · 실행 · 쓰기 없음')
    ap.add_argument('--selftest', action='store_true')
    return ap.parse_args(argv)


def main(argv=None) -> int:
    args = _parse(argv)
    if args.selftest:
        return _selftest()
    if not args.out and not args.check_only:
        print('⛔ --out 을 주어야 한다', file=sys.stderr)
        return 2
    return run_batch(args)


if __name__ == '__main__':
    sys.exit(main())
