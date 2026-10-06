#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""194 건 (LHS 130 + lhsx 64) 망 배치 병렬 실행기 — 동적 큐 · 레인 K (기본 20) · 레인당 1 코어.

1저자 10-05 밤 지시: *"1코어 20개로 20개"* — 하나씩이 아니라 20 건을 동시에, 케이스마다 단일 스레드.

무엇을 하나
───────────────────────────────────────────────────────────────────────────────
  • 케이스마다 **기존 배치 CLI 를 그대로 한 번** 부른다 (규율 ① — 새 계산 경로 없음):
        python3 scripts/lhs_webapp_batch.py --stop-after network --case <c> --harvest-dir <수확> --cohort <코호트>
                --work <ROOT>/cases/<c>/work --out-dir <ROOT>/cases/<c>/out
    같은 프레임 관문 (sha · 프레임 1 · 중복 · type_map) 과 망 정지 계약은 전부 그 배치 · 웹앱 쪽 그대로다.
  • 동적 큐 — 비용 (수확 JSON `contact_scan.n_rows_last` = 접촉 행 수 · 10-01 coverage 배치 경과와 상관 0.97) 큰 순.
    빈 레인이 다음 케이스를 집는다 (정적 분할이 아니다 — 느린 케이스가 다른 레인을 놀리지 않는다).
  • 케이스마다 경과 (s) · 최대 RSS (`os.wait4` — 그 케이스 프로세스와 기다린 자식 프로세스 중 **가장 큰 하나**) · user/sys CPU 를
    `cases/<c>/worker.json` 과 `cases/<c>/log.txt` 끝 줄에 남긴다 (시도마다 · 다시 돌려도 기록이 쌓인다).
  • merge — 케이스별 `out/status.json` · `out/metrics_flat.csv` → 코호트별 한 폴더 `<ROOT>/merged/{lhs,lhsx}/`.
    **배치 자신의 writer** (`lhs_webapp_batch.write_outputs`) 로 쓴다 ⇒ 순차 배치 한 번과 같은 모양 (selftest ⑧ 이 바이트로 대조) ·
    인계 생성기 `lhs_design_dataset.load_webapp` 이 그대로 읽는다 (selftest ⑨).  τ 관문 (`tau_flux.py`) 용 `results/<case>` 링크 —
    결과가 없는 케이스도 빈 폴더로 둔다 (τ 표에서 행이 빠지지 않는다 · NOT_COMPUTED 로 남는다).
  • 실패는 숨기지 않는다 — 워커가 죽어 케이스 기록이 없으면 merge 가 status 'failed' 기록 (사유 = 워커 rc · 신호 · 로그 경로) 을 만든다.
    done · partial 이 아닌 케이스가 하나라도 있으면 rc 1 · 구조 이상 (다른 케이스 기록 · 세대 섞임 · 스키마) 이면 rc 2 (merged 를 쓰지 않는다).
  • 발사 봉인 (RGLR3-01 · Codex 10-05 4차 재검증 §3 — 같은 HEAD 의 dirty retry 가 발사와 다른 코드로 돌고도 merge 성공이었다)
      봉인 = manifest `code_hashes` (CODE_FILES sha256 — 10-05 판 19 · ★ 10-07 판 29 = 전이 의존 ⓖ) · 지문 `code_fp` = 정렬한 해시 지도의 sha256.  재는 곳 = **워커가 실제로 도는
      체크아웃** (manifest `repo_root`) — 실행기 파일 위치가 아니다 (새 실행기를 다른 체크아웃에서 돌려도 봉인은 워커 쪽에서 잰다).
    ⓐ retry 시작 관문 — 워커 체크아웃의 HEAD · 봉인 파일 (CODE_FILES) 해시 · dirty · 기대 망 세대 (ⓕ) 를 발사 봉인과 대조한다.  같은 HEAD 여도 코드가 다르거나 · 해시가 빠졌거나
       (파일 없음 · manifest 에 없음) · 추적 파일이 바뀐 트리면 rc 2 (아무것도 띄우지 않는다 · 아무 파일도 안 쓴다).  넘김 = `--allow-mixed-generation`
       (코드 · HEAD) · `--allow-dirty` (트리만 — 코드 해시는 봉인과 같아야 한다) · 둘 다 manifest retries[] · runs/ · 시도 기록에 남는다.
    ⓑ 시도 증거 — `worker.json` attempts[].seal (attempt_seal/v1) = 띄우기 직전 · 거둔 직후의 코드 지문 (fp_start · fp_end) · 바뀐 파일 ·
       git sha · dirty · 이 시도가 쓴 케이스 기록의 sha256 (record_sha) · 그 실행의 워커 runs[] 항목 (워커 자신이 잰 git sha · dirty).
       실행 중 지문이 봉인과 달라지거나 (넘김 없이) 트리가 dirty 가 되면 새 케이스 입장을 멈춘다 (도는 것은 끝까지 · 자동 merge 없이 rc 2).
    ⓒ 케이스 판정 (`case_seal` — merge · audit · retry 가 같은 함수) — 지금 케이스 기록을 쓴 시도 (record_sha 가 같은 마지막 시도) 로 판정한다:
         SEALED               fp_start = fp_end = 발사 지문 · 시작 · 끝 git sha = 워커 sha = 발사 sha · dirty 아님
         SEALED_DIRTY_ALLOWED 위와 같은데 dirty — 그 실행이 `--allow-dirty` 로 시작돼 기록됐을 때만 (merge 보고 dirty_allowed 에 남는다)
         SEALED_LEGACY        옛 형식 (시도 지문이 없던 실행기 · ★ 10-07 G2RR2-01: 등록된 역사 형식 ROOT 의 역사 모드에서만 — 새 실행 형식 ROOT 의
                              지문 없는 시도 = UNSEALED) — 첫 `run` 의 유일한 시도 (그 시도의 결과 = 기록 상태 · run id 같음 =
                              그 시도가 이 기록을 썼다) · 깨끗한 사전 점검 (manifest git.dirty false, 또는
                              기록이 없고 --allow-dirty 도 아님 — 그때 사전 점검은 dirty 를 거부했다) · runs/run_001 의 code_changed_during_run = []
                              (h0 = h1 · h0 은 manifest 해시와 같은 프로세스에서 곧바로 잰 값) · 워커 runs[] 1 건 (발사 sha · dirty false)
         UNSEALED             그 밖 — 옛 형식 재시도 (발사 봉인과 대조한 적 없다) · 지문 불일치 · dirty 미허용 · 기록이 시도 뒤에 바뀜 · 증거 없음
         NO_RECORD            케이스 기록 없음 (계산 안 됨 — merge 는 failed 로 싣는다)
       UNSEALED 가 하나라도 있으면 merge 는 rc 2 (merged 를 안 쓴다) · `--allow-mixed-generation` 이면 rc 1 + 보고에 기록.  지금 트리가 봉인과
       다른지 (code_changed_since_launch) 는 정보다 — 끝난 뒤 트리만 바뀐 배치를 기각하지 않는다 (판정은 기록된 시도 증거로만).
    ⓓ retry 는 done · partial 이어도 UNSEALED 인 케이스를 `--force` 로 다시 돌린다 (입증 못 한 케이스만 — 봉인된 케이스는 그대로).
    ⓔ `audit --root R` = 읽기 전용 판정표 (케이스마다 판정 · 근거 · merged 기록 = 케이스 폴더 기록인가) · rc 0 = 기록 전부 봉인 안 · 1 = 아님.
  • ★ 10-07 기대 망 세대 · 전이 의존 (Codex 세대 2 재검증 `docs/reviews/codex_review_gen2_network_reverify_20261006.md` §2 · §7-3 · G2RR-01)
    ⓕ manifest `expected_network_generation` (+ 같은 값을 seal 안에) = 워커 체크아웃의 봉인 코드에서 **유도**한 세대 (`derive_generation` — 생산자
       `_run_all_networks` 를 망 CLI 기본값으로 21 구 사슬에 · 같은 체크아웃의 세대 계약) — 세대 2 · 문제 0 이 아니면 발사하지 않는다.  인계 생성기
       `lhs_design_dataset.py --tau-batch-manifest <ROOT>/manifest.json` 이 이 값과 케이스마다 레코드 세대를 교차 대조한다 (없으면 거부).
       retry = 값 ≠ 봉인 사본 · 워커 체크아웃 코드로 다시 유도한 세대 ≠ 값이면 rc 2 (넘김 불가) · audit = 같은 대조 + done · partial 케이스마다 레코드 세대
       = 선언 (아니면 rc 1).  옛 manifest (선언 없음 — 194 v1.2) 는 그대로 읽는다 (세대 대조 없이 · 표지만).
    ⓖ CODE_FILES = 워커의 망 정지 경로가 import 하는 리포 모듈 전부 (정적 닫힘 `code_dependency_closure` ⊆ CODE_FILES 를 발사 사전 점검이 확인 —
       새 import 가 생기면 발사하지 않는다) · 인계 단계 코드 (생성기 · 다시 읽기 도구) 는 `handover_code_hashes` 로 기록 (봉인 판정 밖 · 후속 명령이 대조).
    ⓗ manifest `input_digest` = 계획 큐 ID · 코호트 · 원자료 sha256 (수확 JSON raw — 워커 같은 프레임 관문의 대조값) 지문 · audit 가 다시 계산해 대조.
  • ★ 10-07 Codex 세대 2 재검증 2 (`docs/reviews/codex_review_gen2_network_reverify2_20261007.md` · 1저자 "해결해놔")
    ⓘ G2RR2-01 — 한 자격 검사 `launch_eligibility` (run · retry · audit · merge 가 같은 함수): 새 실행 형식 (`launch_format` · seal v3) 은 기대 세대 (값 ·
       봉인 사본 · 유도 탐침) · 입력 지문 · 코드 해시 · 전이 닫힘 · 인계 코드 지문 · 계획 꼴을 **필수**로 요구한다 — 선언을 지운 새 manifest 를 옛 형식으로
       추론하지 않는다 (옛 판: 키가 없으면 "옛 manifest" 로 면제 → input_digest 삭제 · null · 기대 세대 두 키 삭제가 audit rc 0 · retry 세대 관문 []).
       역사 형식 = 등록된 옛 실행 (`HISTORICAL_LAUNCHES` — 형식 + 발사 출처가 정확히) 만 · 역사 모드 (`audit --historical` · `merge --historical`) 에서만 ·
       retry 불가.  ⚠ 같은 JSON 안의 사본 (값 · 봉인 사본 · 형식 사본) 은 **누락 검사**이지 독립 증거가 아니다 (함께 바꾼 위조는 다른 층 — git · 시도 지문).
    ⓙ G2RR2-03 — CODE_FILES 32 (= 29 + 실제 생산 경로의 지연 import 셋: fracture_model · lhs_union_webapp (dem_analysis_core.run_full_analysis →
       calc_fracture_stages · calc_porosity_union_exact — τ 의 L_mc · φ_mc 를 낸다) · ml_design_structure (structure_predictor 가 모듈 수준에서 부르는
       `_restricted()` 안 — app 을 읽을 때마다 돈다)) · `DEP_LAZY` = 경로 위 지연 import 전부 · 봉인 파일의 함수 안 import 중 봉인 밖 모듈은
       `DEP_LAZY_OFFPATH` 에 사유와 함께 분류 (`lazy_import_census` — 분류 밖이 있으면 발사하지 않는다) · 정적 검사는 보조 — selftest ㉟d 가 실제 생산 경로를
       돌려 모든 프로세스의 import 를 관측한다 (봉인 ⊇ 관측).

설정 (전부 `manifest.json` 에 남는다)
───────────────────────────────────────────────────────────────────────────────
  ① 스레드 — OMP · MKL · OPENBLAS · NUMEXPR · VECLIB_MAXIMUM = 1 (지시 "1 코어").  BLAS 스레드 수는 합산 순서를 바꿔 마지막 자리가
     달라질 수 있다 — 예전 순차 배치 (스레드 기본값) 와 비트 대조할 때 이것을 같이 적는다.
  ② network lock — 웹앱은 network solver 를 **기계 전체에서 하나씩** 돌린다 (`pipeline_service.network_lock` · 파일 lock 이
     `tempfile.gettempdir()` = TMPDIR 에 있다 · OOM 방지 · CB-03).  그대로 두면 20 레인이어도 망 단계는 하나씩 돈다 (지시와 어긋난다)
     ⇒ 기본 `--network-lock per-case` = 케이스마다 TMPDIR 을 따로 준다 (lock 이 케이스 안에서만 잡힌다).  OOM 방지는 대신
     메모리 예산 입장 관문 (아래 ⑤) 이 맡는다.  `--network-lock shared` = 웹앱 직렬화 그대로 (망 단계가 하나씩).
  ③ cwd = 케이스 폴더 — 피복 단계가 **실행 위치 기준** 추적 파일
     (`docs/figures/physics_regime/coverage_hertz_vs_physics_summary.csv` · 원장 LHS-27) 을 덮어쓴다.  20 개가 같은 파일을 동시에
     쓰지 않게 · 리포가 더러워져 runs[].dirty 가 거짓 신호가 되지 않게 케이스 폴더에서 돌린다 (그 줄 말고는 망 경로에 실행 위치 상대
     경로가 없다 — 10-05 grep: parse · analyze_contacts[_bimodal] · coverage · network_conductivity · dem_analysis_core ·
     plastic_coverage · se_material · 웹앱 모듈).  경로 인자는 전부 절대 경로로 넘긴다.
  ④ pyc — `app.run_pipeline` 은 부를 때마다 `scripts/__pycache__/*.pyc` 를 지운다.  여럿이 동시에 지우면 한쪽이 FileNotFoundError 로
     죽는다 ⇒ 워커는 PYTHONDONTWRITEBYTECODE=1 로 띄우고 (새 pyc 를 안 만든다) 발사 전에 한 번 지운다.
  ⑤ 메모리 — 케이스 추정 = MEM_BASE_MB + MEM_PER_KCONTACT_MB × 접촉 천 개 (real_14 · 106,563 접촉 실측 최대 RSS 549 MB 에서 잡은
     **보수 추정** · WSL 실측으로 고칠 것 — 끝에 실측/추정 비를 찍는다).  예산 (`--mem-budget-gb`, 기본 = 발사 시 MemAvailable − 2 GB) 안에서만
     새 케이스를 띄운다 (돌고 있는 것이 없으면 늘 하나는 띄운다) · 앞 케이스가 예산에 안 맞으면 뒤에서 맞는 것을 먼저 띄우되 (backfill)
     앞 케이스가 레인 수만큼 완료를 기다렸으면 backfill 을 멈춘다 (굶김 방지).  `--min-free-gb` = 실측 MemAvailable 바닥 (두 번째 관문).
     `--mem-budget-gb 0` = 예산 끔 (순수 K 레인).

사용 (WSL · 리포 체크아웃 · 봉인 커밋 detached — 예전 배치와 같은 `~/dem-audit`)
───────────────────────────────────────────────────────────────────────────────
  P=~/Yonghoon-DEM-DFT/venv/bin/python
  $P scripts/run_network_194_parallel.py run --root ~/net194_<sha> --dry-run       # 사전 점검 · 계획만 (아무것도 안 쓴다)
  $P scripts/run_network_194_parallel.py run --root ~/net194_pilot -j 2 --case lhsx_040 --case lhs00_055   # 시범 (가장 큰 + 작은)
  $P scripts/run_network_194_parallel.py run --root ~/net194_<sha>                 # 194 건 · 20 레인
  $P scripts/run_network_194_parallel.py status --root ~/net194_<sha>              # 진행 (다른 터미널)
  $P scripts/run_network_194_parallel.py audit --root ~/net194_<sha>               # 봉인 감사 — 케이스마다 어느 코드로 계산됐나 (읽기 전용)
  $P scripts/run_network_194_parallel.py audit --root ~/net194_11fcf91e8 --historical   # 등록된 옛 실행 (10-05 v1.2) 만 — 역사 모드 (G2RR2-01)
  $P scripts/run_network_194_parallel.py retry --root ~/net194_<sha> -j 8          # done · partial 아닌 + 봉인 밖 (UNSEALED) 케이스만 다시
                                                                                   #   (시작 전 발사 봉인 대조 · 기록 보존)
  $P scripts/run_network_194_parallel.py merge --root ~/net194_<sha>               # run · retry 끝에 자동 — 다시 묶기
  $P scripts/run_network_194_parallel.py --selftest
"""
from __future__ import annotations

import argparse
import collections
import contextlib
import csv
import hashlib
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True          # ④ — 이 프로세스도 scripts/__pycache__ 에 pyc 를 만들지 않는다
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import lhs_harvest_batch as HB          # noqa: E402  (코호트 · 경로 치환 · 같은 step 메시 — 배치와 같은 함수)
import lhs_webapp_batch as LWB          # noqa: E402  (KEEP_STATUS · SCHEMA · write_outputs — merge 는 배치의 writer 로 쓴다)

SCHEMA = 'network_parallel_launcher/v1'
WORKER_SCHEMA = 'network_parallel_worker/v1'
BATCH = ROOT / 'scripts' / 'lhs_webapp_batch.py'
KEEP = tuple(LWB.KEEP_STATUS)           # ('done', 'partial') — 배치 · 인계 생성기 (WA_OK_STATUS) 와 같은 집합
STOP = 'network'

#: 코호트 — 10-01 접촉 단계 배치 (`d1ec42fba`) · 5번 coverage 배치 (`1e09f661d`) 와 같은 수확 · 코호트 (같은 프레임 sha 의 기준).
#:   union · design 은 인계표 생성기 후속 명령에만 쓴다 (v1.1 README 와 같은 인자).
COHORT_SPECS = {
    'lhs': dict(harvest='docs/data/lhs_descriptors_cov_1e09f661d', cohort='docs/data/area_s2_cohort.tsv', expect_n=130,
                union='docs/data/lhs_union_20260927/lhs130_union.tsv', design=''),
    'lhsx': dict(harvest='docs/data/lhsx_descriptors_cov_1e09f661d', cohort='docs/data/lhsx_descriptors_20260925/_cohort.tsv',
                 expect_n=64, union='docs/data/lhs_union_20260927/lhsx64_union.tsv',
                 design='docs/data/lhsx_design_adapted_20260929.csv'),
}
#: 인계 v1.2 의 웹앱 묶음 — network 배치는 다섯 묶음 + 망 τ 묶음 tau 를 낸다 (`lhs_design_dataset.WA_STAGE_GROUPS['network']` · RGL-03).
#:   tau 는 `--tau-results <ROOT>/merged/<코호트>/results` (출처 관문 P0–P3 · 출처 부록 <표>_tau_provenance.tsv) 와 짝이다 — τ TSV 를 case 열로
#:   손으로 잇지 않는다 (그 길은 출처 관문을 건너뛴다 · RGLR3-03).  selftest ㉕ 가 생성기의 WA_STAGE_GROUPS['network'] 와 같은지 본다.
HANDOVER_GROUPS = 'contact,percolation,f1,fracture,area,tau'

THREAD_ENV = {'OMP_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1',
              'NUMEXPR_NUM_THREADS': '1', 'VECLIB_MAXIMUM_THREADS': '1'}

#: ⑤ 메모리 · 시간 추정 — real_14 (접촉 106,563 · 원자 33,289) 를 `stop_after='network'` 로 돌린 실측 (10-05 · 이 세션 컨테이너):
#:   `wsl_network_smoke.py` 자식 (단일 스레드 env) = 경과 73.4 s · 최대 RSS 550 MB · 결과 폴더 67 MB
#:   (같은 날 BLAS 기본 스레드 · 다른 작업과 경쟁한 실행 = 294 s · 549 MB — 시간은 경쟁 탓 · 메모리는 같다).
#:   ⚠ 추정은 입장 관문과 계획 출력에만 쓴다 (값에 영향 없음) — WSL 실측 (worker.json · progress.tsv) 으로 고칠 것.
MEM_BASE_MB = 150.0
MEM_PER_KCONTACT_MB = 4.5               # 150 + 4.5 × 106.6 = 630 MB (실측 550 — 15 % 여유)
TIME_PER_KCONTACT_S = 0.7               # 73.4 s / 106.6 k (컨테이너 · 단일 스레드 · 경쟁 없음 — WSL 실측으로 고칠 것)
DISK_PER_CONTACT_B = 700                # 67 MB / 106.6 k ≈ 630 B (atoms.csv · contacts.csv · *_analyzed.csv 가 대부분)

#: 해시로 남기는 코드 — σ 를 바꿀 수 있는 모듈 (`seal_s3_prerun.NUMERIC_MODULES`) + 망 경로 · 배치 · 소비자.
#: ★ 10-07 (Codex 세대 2 재검증 §7-3 "전체 전이 코드 의존성 … 러너가 재검사") — 10-05 판 19 에 워커의 망 정지 경로가 실제로 import 하는 모듈 10 을 더했다
#:   (`code_dependency_closure` 의 정적 닫힘 = 모듈 수준 import + 경로 위 지연 import): lens_geometry (plastic_coverage 가 모듈 수준에서 import —
#:   physics g2 면적의 원판 floor `intersection_disc_area` · σ 에 닿는다) · lhs_perc_extract (lhs_descriptor_harvest) · press_units (app · 목표 압력 단위) ·
#:   grade_engine (predictor_engine) · app 이 모듈 수준에서 import 하는 웹앱 모듈 여섯.  발사 사전 점검이 닫힘 ⊆ CODE_FILES 를 확인한다 (새 import 가 생기면
#:   목록을 먼저 고친다).  ⚠ 옛 ROOT (19 파일 봉인) 는 이 실행기로 retry 하면 봉인이 달라 거부된다 — 그 ROOT 의 커밋 실행기로 (감사는 그대로 읽는다).
#: ★ 10-07 G2RR2-03 (Codex 세대 2 재검증 2 §4) — + 셋 (32): fracture_model · lhs_union_webapp (dem_analysis_core 의 함수 안 import — 접촉 분석 단계가
#:   full_metrics 에 싣는 파괴 단계 · 정확 union porosity · 질량 보존 두께 · φ (τ 인계의 L_mc · φ_mc)) · ml_design_structure (structure_predictor 가 모듈
#:   수준에서 `_restricted()` 를 불러 그 안의 import 가 app 을 읽을 때마다 돈다 — selftest ㉟d 실제 import 관측이 찾았다 · 정적 닫힘이 못 보는 꼴).
CODE_FILES = (
    'scripts/network_conductivity.py', 'scripts/plastic_coverage.py', 'scripts/audit_constriction_deleted.py',
    'scripts/extract_se_network_diagnostics.py', 'scripts/dem_analysis_core.py', 'scripts/analyze_contacts.py',
    'scripts/analyze_contacts_bimodal.py', 'scripts/coverage_physics_vs_hertzian.py', 'scripts/parse_liggghts.py',
    'scripts/se_material.py', 'scripts/metrics_json.py', 'scripts/tau_flux.py', 'scripts/lhs_webapp_batch.py',
    'scripts/lhs_harvest_batch.py', 'scripts/lhs_descriptor_harvest.py', 'webapp/app.py', 'webapp/pipeline_service.py',
    'scripts/export_master_csv.py', 'scripts/type_map_resolve.py',
    'scripts/lens_geometry.py', 'scripts/lhs_perc_extract.py', 'scripts/press_units.py', 'scripts/grade_engine.py',
    'webapp/ledger_view.py', 'webapp/mpm_lab_register.py', 'webapp/predictor_engine.py', 'webapp/security.py',
    'webapp/storage_sync.py', 'webapp/structure_predictor.py',
    'scripts/fracture_model.py', 'scripts/lhs_union_webapp.py', 'scripts/ml_design_structure.py')
LHS27_FILE = 'docs/figures/physics_regime/coverage_hertz_vs_physics_summary.csv'
#: ★ 10-07 §7-3 전이 의존 — 닫힘의 시작점 (워커 · 단계 하위 프로세스 스크립트) 과 경로 위 지연 import (함수 안 import — 정적 닫힘이 모듈 수준만 보므로 적는다):
#:   lhs_webapp_batch.run_batch → app · type_map_resolve · export_master_csv / pipeline_service → tau_flux (`_scripts_import` — 정지 계약 · 기록 검사) /
#:   tau_flux → network_conductivity (`_nc_mod` — 증서 판정).  하위 프로세스 = app.run_pipeline (stop_after='network') 이 띄우는 parse → 접촉 분석
#:   (bimodal · standard) → 피복 → 망 CLI.
DEP_ENTRY = ('scripts/lhs_webapp_batch.py', 'scripts/parse_liggghts.py', 'scripts/analyze_contacts.py', 'scripts/analyze_contacts_bimodal.py',
             'scripts/coverage_physics_vs_hertzian.py', 'scripts/network_conductivity.py')
#: ★ 10-07 G2RR2-03 — 경로 위 지연 import 를 실행 경로마다 완성: 접촉 분석 (analyze_contacts · _bimodal → dem_analysis_core.run_full_analysis →
#:   calc_fracture_stages → fracture_model · calc_porosity_union_exact → lhs_union_webapp — 결과가 full_metrics 에 병합된다 · 인계 fracture 묶음 · τ 장부) ·
#:   app 읽기 (structure_predictor 모듈 수준 `_restricted()` → ml_design_structure) · τ 도우미 (tau_flux → se_material — tau2_from_metrics 짝 σ₀ ·
#:   G2RR2-04 온도 규약).
DEP_LAZY = (('scripts/lhs_webapp_batch.py', 'app'), ('scripts/lhs_webapp_batch.py', 'type_map_resolve'),
            ('scripts/lhs_webapp_batch.py', 'export_master_csv'), ('webapp/pipeline_service.py', 'tau_flux'),
            ('scripts/tau_flux.py', 'network_conductivity'), ('scripts/tau_flux.py', 'se_material'),
            ('scripts/dem_analysis_core.py', 'fracture_model'), ('scripts/dem_analysis_core.py', 'lhs_union_webapp'),
            ('webapp/structure_predictor.py', 'ml_design_structure'))
#: ★ 10-07 G2RR2-03 — 봉인 파일의 함수 안 import 중 **봉인 밖** 모듈 = 워커의 망 정지 경로 밖이라고 판단한 것 (사유와 함께 · `lazy_import_census` 가 분류 밖을
#:   잡는다).  판단이 틀렸으면 (실제로 경로 위면) selftest ㉟d 의 실제 import 관측이 봉인 밖 모듈로 잡는다 — 이 표는 그 관측을 대신하지 않는다.
_ROUTE = '웹앱 화면 · 라우트 전용 (run_pipeline(stop_after=network) 이 부르지 않는다)'
DEP_LAZY_OFFPATH = {
    ('scripts/extract_se_network_diagnostics.py', 'viewer3d_data'): 'analyze_case() — S3 진단 · 3D 뷰어 캐시 (워커 경로 밖 · 이 모듈은 S3 수치 모듈이라 봉인만)',
    ('scripts/grade_engine.py', 'additives'): 'whatif_additives() — 첨가제 what-if 라우트 (등급 계산은 그 함수를 안 부른다)',
    ('webapp/structure_predictor.py', 'ml_shap_pareto'): 'pareto() · shap_importance() — 예측기 화면 (모듈 수준 `_restricted()` 는 ml_design_structure 만 읽는다)',
    ('webapp/app.py', 'viewer3d_data'): _ROUTE + ' — 3D 뷰어 · AM 접촉 확대',
    ('webapp/app.py', 'plot_brittle_z_distribution'): _ROUTE + ' — 취성 z 분포 그림',
    ('webapp/app.py', 'plot_combined_z_distribution'): _ROUTE + ' — 결합 z 분포 그림',
    ('webapp/app.py', 'plot_coverage_z_distribution'): _ROUTE + ' — 피복 z 분포 그림',
    ('webapp/app.py', 'plot_stress_z_distribution'): _ROUTE + ' — 응력 z 분포 그림',
    ('webapp/app.py', 'eis_drt_ica'): _ROUTE + ' — EIS · DRT · ICA',
    ('webapp/app.py', 'cam_kinetics'): _ROUTE + ' — MPM 킷 온도',
    ('webapp/app.py', 'network_current'): _ROUTE + ' — ⚡ 전류 흐름 (게시 뒤 덤프 도구)',
    ('webapp/app.py', 'rint_cycle_traj'): _ROUTE + ' — R_int 사이클',
    ('webapp/app.py', 'backfill_am_metrics'): _ROUTE + ' — /retry-network 의 AM–AM 보충 (배치 워커는 부르지 않는다)',
    ('webapp/app.py', 'extract_2d_microstructure'): _ROUTE + ' — 2D 합성 · 내보내기',
    ('webapp/app.py', 'export_comsol_2d'): _ROUTE + ' — COMSOL 2D 내보내기',
    ('webapp/app.py', 'hetero_transcript'): _ROUTE + ' — 이종기술 회의록',
    ('webapp/app.py', 'mixer_bed'): _ROUTE + ' — /mixer 침대 보기',
    ('webapp/app.py', 'b1_chem_fade'): _ROUTE + ' — STEP5 열화',
    ('webapp/app.py', 'coating_presets'): _ROUTE + ' — STEP5 코팅 프리셋',
    ('webapp/app.py', 'mech_reaction_correlation'): _ROUTE + ' — MPM lab 상관',
    ('webapp/app.py', 'litdb_sync'): _ROUTE + ' — litdb (importlib.import_module)',
}
#: 인계 단계 코드 (워커가 돌리지 않는다 — 봉인 판정 밖) — 발사 때 지문을 기록해 후속 명령이 "인계는 발사 때 생성기 · 다시 읽기 도구로" 를 대조한다.
HANDOVER_FILES = ('scripts/lhs_design_dataset.py', 'scripts/g2_network_reread.py')

#: ★ 10-07 G2RR2-03 — 실제 import 관측 훅 (sitecustomize · PYTHONPATH — 워커와 단계 하위 프로세스가 환경을 물려받는다).  끝날 때 sys.modules 의 파일 +
#:   경로로 읽은 모듈 (spec_from_file_location) 중 NP194_IMPORT_ROOT 아래 것을 프로세스마다 한 줄씩 적는다 — selftest ㉟d (합성 침대) 와
#:   `run --observe-imports` (시범 — 진짜 LHS 침대 · 워커 · parse · bimodal) 가 같은 훅을 쓴다.  값에 닿지 않는다 (기록만) · 시범 전용 (manifest 에 남는다).
IMPORT_OBS_DIR = 'import_obs'
IMPORT_OBS_HOOK = (
    'import atexit, os, sys\n'
    '_L, _R = os.environ.get("NP194_IMPORT_LOG"), os.environ.get("NP194_IMPORT_ROOT")\n'
    '_P = set()\n'
    'def _dump():\n'
    '    try:\n'
    '        fs = {os.path.realpath(getattr(m, "__file__", None) or "") for m in list(sys.modules.values())} | _P\n'
    '        fs.discard(os.path.realpath(""))\n'
    '        with open(os.path.join(_L, "%d.txt" % os.getpid()), "w", encoding="utf-8") as fh:\n'
    '            fh.write("\\n".join(sorted(f for f in fs if f.startswith(_R + os.sep))))\n'
    '    except Exception:\n'
    '        pass\n'
    'if _L and _R:\n'
    '    import importlib.util as _u\n'
    '    _sf = _u.spec_from_file_location\n'
    '    def _spec(name, location=None, *a, **k):\n'
    '        if location is not None:\n'
    '            _P.add(os.path.realpath(str(location)))\n'
    '        return _sf(name, location, *a, **k)\n'
    '    _u.spec_from_file_location = _spec\n'
    '    atexit.register(_dump)\n')
#: 관측에서 빼는 시험 도구 (생산 경로가 아니다) — selftest 의 합성 침대 자식 (wsl_network_smoke --_child) 과 침대 도구.
IMPORT_OBS_HARNESS = ('scripts/wsl_network_smoke.py', 'webapp/test_pipeline_provenance.py')


def import_obs_env(obs_dir: Path, code_root) -> dict:
    """관측 훅을 켜는 환경 변수 (obs_dir/hook 의 sitecustomize · obs_dir/log 에 기록 · code_root 아래 파일만)."""
    hook, log = Path(obs_dir) / 'hook', Path(obs_dir) / 'log'
    hook.mkdir(parents=True, exist_ok=True)
    log.mkdir(parents=True, exist_ok=True)
    (hook / 'sitecustomize.py').write_text(IMPORT_OBS_HOOK, encoding='utf-8')
    return dict(NP194_IMPORT_LOG=str(log), NP194_IMPORT_ROOT=str(Path(code_root).resolve()),
                PYTHONPATH=os.pathsep.join([str(hook)] + [p for p in (os.environ.get('PYTHONPATH') or '').split(os.pathsep) if p]))


def import_observation(obs_dir: Path, code_root) -> dict:
    """관측 기록 → dict(n_processes, files (리포 상대 · 정렬), observed (scripts · webapp 의 .py · 시험 도구 제외), outside (그중 CODE_FILES 밖))."""
    r = Path(code_root).resolve()
    logs = sorted((Path(obs_dir) / 'log').glob('*.txt'))
    seen = set()
    for lf in logs:
        for ln in lf.read_text(encoding='utf-8').splitlines():
            if ln.strip():
                try:
                    seen.add(Path(ln.strip()).resolve().relative_to(r).as_posix())
                except ValueError:
                    continue
    obs = sorted(f for f in seen if f.endswith('.py') and f.startswith(('scripts/', 'webapp/')) and f not in IMPORT_OBS_HARNESS)
    return dict(n_processes=len(logs), files=sorted(seen), observed=obs, outside=[f for f in obs if f not in CODE_FILES])

#: ★ 10-07 G2RR-01 · §7-3 — 발사 봉인의 기대 망 세대.  키 = 인계 생성기 `lhs_design_dataset.TAU_MANIFEST_GENERATION_KEY` (`tau_manifest_expected_generation` ·
#:   CLI `--tau-batch-manifest` 가 읽는다 · 없으면 거부) · 같은 값을 manifest.seal 안에도 둔다 (retry · audit 가 둘을 대조).  값은 손으로 적지 않는다 —
#:   워커 체크아웃의 봉인 코드로 유도한다 (`derive_generation`: 생산자 `network_conductivity._run_all_networks` 를 망 CLI 와 같은 기본값 (hertzian · physics) 으로
#:   21 구 사슬에 한 번 → 같은 체크아웃의 `tau_flux.network_generation_contract`).  현행 게시는 세대 2 만 받는다 (pipeline_service.network_record_verdict ·
#:   정지 계약 ⑨ legacy_ok False) ⇒ 유도 세대가 그 계약의 g2 (문제 0) 가 아니면 발사하지 않는다.
GEN_KEY = 'expected_network_generation'
GEN_PROBE_METHOD = ('chain21 — network_conductivity._run_all_networks (망 CLI 기본값 · hertzian + physics · 21 구 SE 사슬 · 판 20 · 상자 10 · 척도 1) → '
                    'tau_flux.network_generation_contract (같은 워커 체크아웃 · python -I -B)')
GEN_PROBE = r'''
import contextlib, io, json, os, sys
root = sys.argv[1]
sys.path[:0] = [os.path.join(root, 'scripts'), os.path.join(root, 'webapp')]
sys.dont_write_bytecode = True
import network_conductivity as nc
import tau_flux as tf
A = {i: dict(type=1, x=0.0, y=0.0, z=float(i), radius=1.0) for i in range(21)}
C = [dict(id1=i, id2=i + 1, contact_area=0.01, delta=0.05) for i in range(20)]
with contextlib.redirect_stdout(io.StringIO()):
    dual = {cm: nc._run_all_networks(A, C, [1], [], {1: 'SE'}, 1.0, 20.0, 10.0, 10.0, None, contact_mode=cm) for cm in ('hertzian', 'physics')}
con = tf.network_generation_contract(dual)
if len(sys.argv) > 2 and sys.argv[2]:
    with open(sys.argv[2], 'w', encoding='utf-8') as fh:
        json.dump(dual, fh)
print('GEN_PROBE ' + json.dumps(dict(generation=con.get('generation'), g2_name=tf.NET_GEN_G2,
                                     problems=[list(p) for p in con.get('problems') or []],
                                     modes=[m for m in tf.MODES if tf.mode_record(dual, m) is not None],
                                     nc_file=os.path.abspath(nc.__file__), tf_file=os.path.abspath(tf.__file__))))
'''

#: 발사 봉인 (RGLR3-01) — 스키마 · 판정 이름.  판정 규칙은 모듈 docstring '발사 봉인' ⓒ (case_seal 이 그대로 구현한다).
#:   v2 (10-07 새벽) = seal 안에 기대 망 세대 (GEN_KEY) · CODE_FILES 29.  ★ v3 (10-07 G2RR2-01 · 03) = 새 실행 형식 `LAUNCH_FORMAT` (manifest 와 seal 에) ·
#:   필수 선언 (`launch_eligibility`) · CODE_FILES 32.  v2 manifest (9d25757dc – 이 수정 전 실행기) 는 이 실행기의 형식이 아니다 — 그 ROOT 는 그 커밋의 실행기로.
#:   역사 형식 = 등록된 옛 실행 (`HISTORICAL_LAUNCHES`) 만 (역사 모드에서만 읽는다).
LAUNCH_SEAL_SCHEMA = 'launch_seal/v3'       # manifest.seal
LAUNCH_FORMAT = 'network_parallel_launch/v3'     # manifest.launch_format (+ seal 사본 — 같은 JSON 의 사본 = 누락 검사 · 독립 증거 아님)
CURRENT_GENERATION = 'g2'                   # 현행 게시가 받는 유일한 세대 (`tau_flux.NET_GEN_G2` — 사전 점검의 유도 탐침이 같은지 본다)
ATTEMPT_SEAL_SCHEMA = 'attempt_seal/v1'     # worker.json attempts[].seal
SEAL_OK = ('SEALED', 'SEALED_DIRTY_ALLOWED', 'SEALED_LEGACY')
#: 새 실행 형식의 표지 — 하나라도 있으면 역사 형식이 아니다 (필수 선언 전부를 요구한다 · 지운 것을 옛 형식으로 추론하지 않는다).
NEW_FORMAT_KEYS = ('seal', 'launch_format', GEN_KEY, 'input_digest', 'generation_probe', 'code_dependency_closure', 'handover_code_hashes')
INPUT_DIGEST_KEYS = ('n', 'ids_sha256', 'raw_sha256_table_sha256', 'missing_raw_sha', 'cohort_tsv_sha256')
_HEX64 = re.compile(r'^[0-9a-f]{64}$')
_HEX40 = re.compile(r'^[0-9a-f]{40}$')
#: ★ 10-07 G2RR2-01 — 확인된 옛 실행 (역사 허용 = 이 표와 형식 · 발사 출처가 **정확히** 같을 때만 · 역사 모드에서만).  값은 커밋된 증거 manifest
#:   (`evidence`) 에서 잰 것 — selftest ㉞ 가 그 파일로 다시 대조한다.  계획 큐 (입력) 는 고정하지 않는다 — 꼴만 본다 (그 형식에는 입력 지문이 없었다 ·
#:   역사 모드 판정은 "입력 대조 없음" 표지를 단다).
HISTORICAL_LAUNCHES = {
    'net194_v12_11fcf91e8': dict(
        evidence='docs/data/lhs_network194_11fcf91e8/manifest.json',
        registration='docs/reviews/lhs_network_batch_registration_20261005.md',
        schema='network_parallel_launcher/v1',
        git_sha='11fcf91e8a1f4837b83892b7e4a81125eaeee4e5',
        code_fp='3bc0a116ddab109c01f6ab1e1f0cf0d3abf67c5cf6c6336d058315c6189eb0b5',
        code_files=('scripts/analyze_contacts.py', 'scripts/analyze_contacts_bimodal.py', 'scripts/audit_constriction_deleted.py',
                    'scripts/coverage_physics_vs_hertzian.py', 'scripts/dem_analysis_core.py', 'scripts/export_master_csv.py',
                    'scripts/extract_se_network_diagnostics.py', 'scripts/lhs_descriptor_harvest.py', 'scripts/lhs_harvest_batch.py',
                    'scripts/lhs_webapp_batch.py', 'scripts/metrics_json.py', 'scripts/network_conductivity.py', 'scripts/parse_liggghts.py',
                    'scripts/plastic_coverage.py', 'scripts/se_material.py', 'scripts/tau_flux.py', 'scripts/type_map_resolve.py',
                    'webapp/app.py', 'webapp/pipeline_service.py'),
        keys=('allow_dirty', 'allow_missing_raw', 'argv', 'code_hashes', 'created', 'git', 'lanes', 'mem_budget_mb', 'mem_model',
              'mem_reserve_gb', 'min_free_gb', 'network_lock', 'plan', 'preflight', 'pyc_purged', 'python', 'python_versions', 'repo_root',
              'retries', 'root_from', 'root_to', 'schema', 'stop_after', 'thread_env', 'worker_override', 'worker_script'),
        cohorts=('lhs', 'lhsx')),
}


class LaunchError(RuntimeError):
    """사전 점검 · 계획 실패 — 아무것도 띄우지 않는다."""


# ─────────────────────────────────── 작은 도구 ───────────────────────────────────
def now_iso():
    return time.strftime('%Y-%m-%dT%H:%M:%S')


def _abs(p) -> Path:
    p = Path(str(p)).expanduser()
    return (p if p.is_absolute() else ROOT / p).resolve()


def write_json(path: Path, obj) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name('.' + path.name + '.tmp')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    os.replace(tmp, path)


def read_json(path: Path):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None


def sha256_file(p: Path):
    try:
        h = hashlib.sha256()
        with open(p, 'rb') as fh:
            for b in iter(lambda: fh.read(1 << 20), b''):
                h.update(b)
        return h.hexdigest()
    except OSError:
        return None


def code_hashes(root=None):
    r = Path(root) if root is not None else ROOT
    return {rel: sha256_file(r / rel) for rel in CODE_FILES}


def code_dependency_closure(root=None) -> dict:
    """★ 10-07 §7-3 — 워커의 망 정지 경로가 import 하는 리포 모듈의 정적 닫힘 → dict(files (리포 상대 · 정렬), errors, entry, lazy).
    시작점 DEP_ENTRY · 모듈 수준 import (if · try · with · class 본문 포함 · 함수 본문 제외) + 경로 위 지연 import DEP_LAZY ·
    이름은 <root>/scripts · <root>/webapp 의 .py 로 푼다 (표준 · 외부 패키지는 밖).  못 읽는 시작점 · 구문 오류 = errors (사전 점검 중단 사유)."""
    import ast
    r = Path(root) if root is not None else ROOT
    search = (r / 'scripts', r / 'webapp')

    def resolve(name):
        top = name.split('.')[0]
        for d in search:
            if (d / f'{top}.py').is_file():
                return d / f'{top}.py'
        return None

    def toplevel(p):
        names = set()

        def visit(stmts):
            for s in stmts:
                if isinstance(s, ast.Import):
                    names.update(a.name for a in s.names)
                elif isinstance(s, ast.ImportFrom) and s.module and s.level == 0:
                    names.add(s.module)
                elif isinstance(s, (ast.If, ast.Try, ast.With, ast.For, ast.While)):
                    for fld in ('body', 'orelse', 'finalbody'):
                        visit(getattr(s, fld, None) or [])
                    for h in getattr(s, 'handlers', None) or []:
                        visit(h.body)
                elif isinstance(s, ast.ClassDef):
                    visit([b for b in s.body if not isinstance(b, (ast.FunctionDef, ast.AsyncFunctionDef))])
        visit(ast.parse(p.read_text(encoding='utf-8')).body)
        return names
    lazy = {}
    for imp, mod in DEP_LAZY:
        lazy.setdefault(imp, set()).add(mod)
    seen, errors, todo = set(), [], [r / e for e in DEP_ENTRY]
    while todo:
        p = todo.pop()
        rel = p.relative_to(r).as_posix()
        if rel in seen:
            continue
        try:
            names = toplevel(p) | lazy.get(rel, set())
        except (OSError, SyntaxError, ValueError, UnicodeDecodeError) as e:
            errors.append(f'{rel}: {type(e).__name__}: {e}')
            continue
        seen.add(rel)
        for n in sorted(names):
            q = resolve(n)
            if q is not None and q.relative_to(r).as_posix() not in seen:
                todo.append(q)
    return dict(files=sorted(seen), errors=errors, entry=list(DEP_ENTRY), lazy=[list(x) for x in DEP_LAZY])


def derive_generation(code_root, python=None, dual_out=None) -> dict:
    """★ 10-07 G2RR-01 · §7-3 — 워커 체크아웃 code_root 의 봉인 코드가 내는 망 세대를 유도한다 (GEN_PROBE · 하위 프로세스 `python -I -B` — 환경의
    PYTHONPATH · 사용자 site 가 다른 사본을 끌어오지 않게) → dict(generation, g2_name, problems, modes, error, method, python, code_root).
    dual_out = 탐침이 낸 dual 을 쓸 곳 (선택 · selftest 의 가짜 워커가 쓴다)."""
    py = str(python or sys.executable)
    base = dict(generation=None, g2_name=None, problems=[], modes=[], method=GEN_PROBE_METHOD, python=py, code_root=str(code_root))
    try:
        r = subprocess.run([py, '-I', '-B', '-c', GEN_PROBE, str(code_root), str(dual_out or '')], capture_output=True, text=True, timeout=600,
                           cwd=str(code_root), env=dict(os.environ, **THREAD_ENV, PYTHONDONTWRITEBYTECODE='1'))
    except Exception as e:                                  # noqa: BLE001 — 유도를 못 하면 세대를 모른다 (fail-closed)
        return dict(base, error=f'{type(e).__name__}: {e}')
    line = next((ln for ln in reversed(r.stdout.splitlines()) if ln.startswith('GEN_PROBE ')), None)
    if r.returncode != 0 or line is None:
        return dict(base, error=f'탐침 rc {r.returncode} · {((r.stderr or "") + (r.stdout or ""))[-500:]}')
    try:
        d = json.loads(line[len('GEN_PROBE '):])
    except ValueError as e:
        return dict(base, error=f'탐침 출력 해석 실패 ({e})')
    return dict(base, error='', **{k: d.get(k) for k in ('generation', 'g2_name', 'problems', 'modes', 'nc_file', 'tf_file')})


def generation_probe_problem(gp: dict) -> str:
    """유도 결과 → '' (발사 가능: 세대 = 그 계약의 g2 · 문제 0) | 사유."""
    if gp.get('error'):
        return f'세대 유도 실패 — {gp["error"]}'
    if gp.get('problems'):
        return f'유도 탐침의 세대 계약 문제 {gp["problems"][:3]}'
    if not gp.get('generation') or gp.get('generation') != gp.get('g2_name'):
        return (f'봉인 코드가 내는 세대 {gp.get("generation")!r} ≠ 세대 2 ({gp.get("g2_name")!r}) — 현행 게시는 세대 2 만 받는다 '
                '(network_record_verdict · 정지 계약 ⑨) · 이 코드로는 게시될 케이스가 없다')
    return ''


def _plan_problems(plan, cohort_names=None) -> list:
    """계획 (manifest plan) 의 꼴 — cohorts (비지 않은 목록 · 이름 문자열 · 중복 없음 · cohort_names 가 주어지면 그 집합 안) · queue (비지 않은 목록 ·
    case · cohort 문자열 · 케이스 중복 없음 · 코호트 소속).  ⚠ 케이스가 0 인 코호트는 정당하다 (`--case` 시범이 한 코호트만 고를 때 — build_plan 이
    요청한 코호트를 다 싣는다) — 등록 집합과의 대조는 다시 읽기 (`g2_network_reread` 등록 모드) 의 몫."""
    if not isinstance(plan, dict):
        return [f'plan 이 객체가 아니다 ({type(plan).__name__})']
    cs, q = plan.get('cohorts'), plan.get('queue')
    out = []
    if not isinstance(cs, list) or not cs or not all(isinstance(c, dict) and isinstance(c.get('name'), str) and c.get('name') for c in cs):
        return out + [f'plan.cohorts 가 비지 않은 코호트 목록이 아니다 ({cs!r:.120})']
    names = [c['name'] for c in cs]
    if len(set(names)) != len(names):
        out.append(f'plan.cohorts 이름 중복 {names}')
    if cohort_names is not None and set(names) - set(cohort_names):
        out.append(f'plan.cohorts 에 등록 밖 코호트 {sorted(set(names) - set(cohort_names))} (등록 {sorted(cohort_names)})')
    if not isinstance(q, list) or not q or not all(isinstance(e, dict) and isinstance(e.get('case'), str) and isinstance(e.get('cohort'), str)
                                                   for e in q):
        return out + [f'plan.queue 가 비지 않은 (case, cohort) 목록이 아니다 ({q!r:.120})']
    cases = [e['case'] for e in q]
    dup = sorted({c for c in cases if cases.count(c) > 1})
    if dup:
        out.append(f'plan.queue 케이스 중복 {dup[:5]}')
    stray = sorted({e['cohort'] for e in q} - set(names))
    if stray:
        out.append(f'plan.queue 의 코호트 {stray} 가 plan.cohorts 에 없다')
    return out


def ids_digest(pairs) -> str:
    """(케이스, 코호트) 쌍 → 'case\\tcohort' 줄 ((코호트, 케이스) 순 · 줄마다 끝 개행) 의 sha256 — manifest input_digest.ids_sha256 · 등록 문서 §2 ·
    다시 읽기 (`g2_network_reread` 등록 집합) 가 같은 식."""
    lines = [f'{c}\t{h}' for c, h in sorted(pairs, key=lambda x: (x[1], x[0]))]
    return hashlib.sha256(('\n'.join(lines) + '\n').encode('utf-8')).hexdigest()


def _historical_match(m) -> tuple:
    """manifest → (등록 이름 | None, [어긋남]) — 등록된 옛 실행 (`HISTORICAL_LAUNCHES`) 과 형식 · 발사 출처가 정확히 같은가."""
    best = (None, ['등록된 옛 실행이 없다'])
    for name, h in HISTORICAL_LAUNCHES.items():
        why = []
        if m.get('schema') != h['schema']:
            why.append(f'schema {m.get("schema")!r} ≠ {h["schema"]!r}')
        if sorted(m) != sorted(h['keys']):
            why.append(f'키 집합 ≠ 등록 (남는 키 {sorted(set(m) - set(h["keys"]))} · 없는 키 {sorted(set(h["keys"]) - set(m))})')
        g = m.get('git') if isinstance(m.get('git'), dict) else {}
        if g.get('sha') != h['git_sha'] or g.get('dirty') is not False:
            why.append(f'발사 git {str(g.get("sha"))[:12]} · dirty {g.get("dirty")!r} ≠ 등록 {h["git_sha"][:12]} · False')
        ch = m.get('code_hashes') if isinstance(m.get('code_hashes'), dict) else {}
        if sorted(ch) != sorted(h['code_files']) or code_fp(ch) != h['code_fp']:
            why.append(f'코드 해시 {len(ch)} 파일 · 지문 {str(code_fp(ch))[:12]} ≠ 등록 {len(h["code_files"])} · {h["code_fp"][:12]}')
        if m.get('stop_after') != STOP or m.get('worker_override') is not False:
            why.append(f'stop_after {m.get("stop_after")!r} · worker_override {m.get("worker_override")!r}')
        why += _plan_problems(m.get('plan'), h['cohorts'])
        if not why:
            return name, []
        best = (None, [f'{name}: ' + ' · '.join(why)])
    return best


def launch_eligibility(man) -> dict:
    """★ 10-07 G2RR2-01 (Codex 세대 2 재검증 2 §2) — manifest 의 실행 형식 자격.  run (쓴 뒤 자기 대조) · retry · audit · merge 가 **이 한 함수**를 쓴다.
    → dict(kind='current' | 'historical' | 'invalid', problems=[…], historical=등록 이름 | None, note=…)
      current    — 새 실행 형식: launch_format · seal (schema v3 · 형식 사본 · code_fp = code_hashes 지문 · 파일 수) · 기대 세대 (값 = 봉인 사본 = g2 ·
                   유도 탐침 기록이 같은 세대 · 문제 0) · input_digest (꼴 · 케이스 수 = 계획 · ids 지문 = 계획 큐에서 다시 잰 값 · 원자료 결손 0) ·
                   code_hashes (CODE_FILES 정확히) · 전이 닫힘 ⊆ 봉인 · 인계 코드 지문 · git sha · 계획 꼴 — **전부 필수**
      historical — 새 형식 표지 (NEW_FORMAT_KEYS) 가 하나도 없고 등록된 옛 실행과 형식 · 발사 출처가 정확히 같다 (역사 모드에서만 읽는다)
      invalid    — 그 밖 (새 형식 표지가 있는데 선언이 빠졌거나 · 표지가 없는데 등록된 옛 실행이 아니다 — 필드가 없다는 것으로 옛 형식을 추론하지 않는다)
    ⚠ 같은 JSON 의 사본 (값 · 봉인 사본 · 형식 사본) 은 누락 검사다 — 독립 증거가 아니다 (함께 바꾼 위조는 git · 시도 지문 · 기록 sha 층의 몫)."""
    if not isinstance(man, dict):
        return dict(kind='invalid', problems=[f'manifest 가 객체가 아니다 ({type(man).__name__})'], historical=None, note='')
    if man.get('schema') != SCHEMA:
        return dict(kind='invalid', problems=[f'schema {man.get("schema")!r} ≠ {SCHEMA!r} — 이 실행기의 manifest 가 아니다'], historical=None, note='')
    if not any(k in man for k in NEW_FORMAT_KEYS):
        name, why = _historical_match(man)
        if name:
            return dict(kind='historical', problems=[], historical=name,
                        note=(f'역사 형식 {name} (등록된 옛 실행 · {HISTORICAL_LAUNCHES[name]["registration"]}) — 기대 세대 · 입력 지문 선언이 없는 형식이라 '
                              '세대 · 입력 대조 없이 코드 봉인 판정만 · 역사 모드에서만 읽는다 · retry 는 그 커밋의 실행기로'))
        return dict(kind='invalid', historical=None, note='',
                    problems=['새 실행 형식의 표지가 하나도 없는데 등록된 옛 실행도 아니다 — 필드가 없다는 것으로 옛 형식을 추론하지 않는다: ' + ' ; '.join(why)])
    p = []
    s = man.get('seal')
    if not isinstance(s, dict):
        p.append(f'seal 이 없다 · 객체가 아니다 ({type(s).__name__}) — 새 실행 형식은 발사 봉인을 싣는다')
        s = {}
    if man.get('launch_format') != LAUNCH_FORMAT or s.get('launch_format') != LAUNCH_FORMAT:
        p.append(f'launch_format {man.get("launch_format")!r} · 봉인 사본 {s.get("launch_format")!r} ≠ {LAUNCH_FORMAT!r}')
    if s and s.get('schema') != LAUNCH_SEAL_SCHEMA:
        p.append(f'seal.schema {s.get("schema")!r} ≠ {LAUNCH_SEAL_SCHEMA!r} (다른 판 실행기의 봉인 — 그 커밋의 실행기로)')
    if man.get(GEN_KEY) != CURRENT_GENERATION or s.get(GEN_KEY) != CURRENT_GENERATION:
        p.append(f'기대 망 세대 {GEN_KEY} {man.get(GEN_KEY, "ABSENT")!r} · 봉인 사본 {s.get(GEN_KEY, "ABSENT")!r} ≠ {CURRENT_GENERATION!r} (둘 다 필수 · 같아야)')
    gp = man.get('generation_probe')
    if not isinstance(gp, dict) or gp.get('generation') != man.get(GEN_KEY) or gp.get('problems') or gp.get('error'):
        p.append(f'generation_probe (봉인 코드에서 기대 세대를 유도한 기록) 없음 · 다름 · 문제 ({(gp or {}).get("generation") if isinstance(gp, dict) else gp!r})')
    ch = man.get('code_hashes')
    if not isinstance(ch, dict) or sorted(ch) != sorted(CODE_FILES) or not all(isinstance(v, str) and _HEX64.match(v) for v in ch.values()):
        p.append(f'code_hashes 가 봉인 대상 CODE_FILES {len(CODE_FILES)} 파일의 sha256 지도가 아니다 '
                 f'(있는 {len(ch) if isinstance(ch, dict) else ch!r} · 빠진 {sorted(set(CODE_FILES) - set(ch or {}))[:4]})')
    elif s and (s.get('code_fp') != code_fp(ch) or s.get('files') != len(CODE_FILES)):
        p.append(f'seal.code_fp · files ({str(s.get("code_fp"))[:12]} · {s.get("files")}) ≠ code_hashes 지문 · 파일 수 ({str(code_fp(ch))[:12]} · {len(CODE_FILES)})')
    clo = man.get('code_dependency_closure')
    if not isinstance(clo, list) or not clo or [f for f in clo if f not in CODE_FILES]:
        p.append(f'code_dependency_closure (전이 닫힘) 없음 · 봉인 밖 파일 {[f for f in clo or [] if f not in CODE_FILES][:4] if isinstance(clo, list) else clo!r}')
    hh = man.get('handover_code_hashes')
    if not isinstance(hh, dict) or sorted(hh) != sorted(HANDOVER_FILES) or not all(isinstance(v, str) and _HEX64.match(v) for v in hh.values()):
        p.append(f'handover_code_hashes (인계 도구 지문) 없음 · 꼴이 다르다 ({sorted(hh) if isinstance(hh, dict) else hh!r})')
    g = man.get('git') if isinstance(man.get('git'), dict) else {}
    if not (isinstance(g.get('sha'), str) and _HEX40.match(g['sha'])):
        p.append(f'git.sha {g.get("sha")!r} — 발사 커밋 신원이 없다')
    pp = _plan_problems(man.get('plan'))
    p += pp
    dg = man.get('input_digest')
    if not isinstance(dg, dict):
        p.append(f'input_digest (194 ID · 코호트 · 원자료 sha256 지문) 없음 · 객체 아님 ({type(dg).__name__}) — 새 실행 형식의 필수 선언')
    else:
        miss = [k for k in INPUT_DIGEST_KEYS if k not in dg]
        if miss:
            p.append(f'input_digest 키 결손 {miss}')
        q = (man.get('plan') or {}).get('queue') if isinstance(man.get('plan'), dict) else None
        if not pp and isinstance(q, list):
            if dg.get('n') != len(q):
                p.append(f'input_digest.n {dg.get("n")!r} ≠ 계획 큐 {len(q)}')
            if dg.get('ids_sha256') != ids_digest((e['case'], e['cohort']) for e in q):
                p.append('input_digest.ids_sha256 ≠ 계획 큐 (case, cohort) 에서 다시 잰 지문 — 발사 뒤 계획 또는 지문이 바뀌었다')
            names = sorted(c['name'] for c in man['plan']['cohorts'])
            cts = dg.get('cohort_tsv_sha256')
            if not isinstance(cts, dict) or sorted(cts) != names or not all(isinstance(v, str) and _HEX64.match(v) for v in cts.values()):
                p.append(f'input_digest.cohort_tsv_sha256 꼴 ({cts!r:.120}) ≠ 코호트 {names} 의 sha256')
        if not (isinstance(dg.get('raw_sha256_table_sha256'), str) and _HEX64.match(dg['raw_sha256_table_sha256'])):
            p.append(f'input_digest.raw_sha256_table_sha256 {dg.get("raw_sha256_table_sha256")!r} — 원자료 sha256 표 지문이 없다')
        if dg.get('missing_raw_sha') != []:
            p.append(f'input_digest.missing_raw_sha {dg.get("missing_raw_sha")!r} (빈 목록이어야 — 원자료 sha 결손이 있으면 발사하지 않았다)')
    return dict(kind=('invalid' if p else 'current'), problems=p, historical=None, note='')


def lazy_import_census(root=None) -> dict:
    """★ 10-07 G2RR2-03 — 봉인 파일 (CODE_FILES) 의 **함수 안** import (Import · ImportFrom · `importlib.import_module` · `_scripts_import` · `__import__` 의
    문자열 인자) 중 리포 모듈 (<root>/scripts · webapp) 로 풀리는 것 → dict(lazy=[(importer, 함수, 대상 파일, 이름)], unclassified=[…], stale=[…]).
      unclassified = 봉인 밖 대상인데 DEP_LAZY (경로 위 — 대상은 봉인돼야) 에도 DEP_LAZY_OFFPATH (경로 밖 · 사유) 에도 없는 것 → 발사 사전 점검 중단
      stale        = 분류표에 있는데 지금 코드에 없는 (importer, 이름) — 정보 (표 정리)
    ⚠ 경로를 변수로 읽는 동적 적재 (spec_from_file_location 등) 는 정적으로 풀지 않는다 — selftest ㉟d 의 실제 import 관측이 생산 경로를 본다."""
    import ast
    r = Path(root) if root is not None else ROOT
    search = (r / 'scripts', r / 'webapp')

    def resolve(name):
        top = name.split('.')[0]
        for d in search:
            if (d / f'{top}.py').is_file():
                return (d / f'{top}.py').relative_to(r).as_posix()
        return None
    dyn = {'import_module', '_scripts_import', '__import__'}
    found = []
    for rel in CODE_FILES:
        p = r / rel
        try:
            tree = ast.parse(p.read_text(encoding='utf-8'))
        except (OSError, SyntaxError, ValueError, UnicodeDecodeError):
            continue                                            # 못 읽는 봉인 파일 = 사전 점검의 해시 · 닫힘 검사가 따로 잡는다
        for fn in ast.walk(tree):
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for s in ast.walk(fn):
                names = []
                if isinstance(s, ast.Import):
                    names = [a.name for a in s.names]
                elif isinstance(s, ast.ImportFrom) and s.module and s.level == 0:
                    names = [s.module]
                elif isinstance(s, ast.Call) and s.args and isinstance(s.args[0], ast.Constant) and isinstance(s.args[0].value, str):
                    f_ = s.func
                    nm = f_.attr if isinstance(f_, ast.Attribute) else (f_.id if isinstance(f_, ast.Name) else '')
                    if nm in dyn:
                        names = [s.args[0].value]
                for n in names:
                    q = resolve(n)
                    if q is not None:
                        found.append((rel, fn.name, q, n.split('.')[0]))
    lazy_on = {(a, b) for a, b in DEP_LAZY}
    seen = {(a, n) for a, _f, _q, n in found}
    unclassified = sorted({(a, f, q, n) for a, f, q, n in found if q not in CODE_FILES and (a, n) not in DEP_LAZY_OFFPATH})
    stale = sorted(k for k in DEP_LAZY_OFFPATH if k not in seen) + sorted(k for k in lazy_on if k not in seen)
    return dict(lazy=sorted(set(found)), unclassified=unclassified, stale=stale)


def generation_gate(man, root=None) -> tuple:
    """★ 10-07 G2RR-01 · ★ G2RR2-01 — retry 시작 관문의 실행 형식 · 기대 망 세대 대조 → (막는 사유 목록, 표지).  넘김 (--allow-*) 으로 못 넘긴다.
    · 실행 형식 자격 (`launch_eligibility`) 이 current 가 아니면 막는다 — 역사 형식 (그 ROOT 의 커밋 실행기로) · 선언을 지운 manifest (옛 판: 두 키가
      없으면 "옛 manifest" 로 면제 → 막는 사유 [] · Codex 세대 2 재검증 2 §2)
    · 워커 체크아웃 코드로 다시 유도한 세대 ≠ 봉인 기대 세대 → 막는다"""
    m = man if isinstance(man, dict) else {}
    el = launch_eligibility(m)
    if el['kind'] == 'historical':
        return [f'역사 형식 ROOT ({el["historical"]}) — 이 실행기로 retry 하지 않는다 (그 ROOT 의 커밋 실행기로 · 넘김 불가) · {el["note"]}'], ''
    if el['kind'] != 'current':
        return [f'실행 형식 자격 없음 (G2RR2-01): {p}' for p in el['problems'][:8]], ''
    top = m.get(GEN_KEY)
    gp = derive_generation(root if root is not None else code_root(m), m.get('python'))
    if gp.get('error') or gp.get('problems') or gp.get('generation') != top:
        return [f'봉인 기대 망 세대 {top!r} ≠ 워커 체크아웃 ({root if root is not None else code_root(m)}) 코드가 지금 내는 세대 '
                f'{gp.get("generation")!r} ({gp.get("error") or gp.get("problems") or "다른 세대"})'], ''
    return [], ''


def case_record_generation(root: Path, case: str):
    """케이스 결과 폴더의 망 레코드 (dual) 세대 — `tau_flux.network_generation_contract` (인계 · 게시와 같은 함수).  dual 없음 · 못 읽음 = 'missing'."""
    import tau_flux as _tf
    dual = read_json(case_dir(Path(root), case) / 'work' / 'results' / case / 'network_conductivity_dual.json')
    if not isinstance(dual, dict):
        return 'missing'
    return _tf.network_generation_contract(dual).get('generation') or 'none'


def plan_input_digest(plan) -> dict:
    """★ 10-07 §7-3 "194 ID · cohort · 원 dump 의 해시" — 계획 큐의 (케이스, 코호트) 와 원자료 sha256 (수확 JSON raw.{atom,contact,mesh,deck}.sha256 —
    워커 (`lhs_webapp_batch` 같은 프레임 관문) 가 실제 파일과 대조하는 값) 의 지문.  줄 = 'case\\tcohort[\\tatom\\tcontact\\tmesh\\tdeck]' · (코호트, 케이스) 순 ·
    줄마다 끝 개행 · sha256.  → dict(n, ids_sha256, raw_sha256_table_sha256, missing_raw_sha, cohort_tsv_sha256)."""
    hdirs = {c['name']: Path(c['harvest_dir']) for c in (plan or {}).get('cohorts') or []}
    pairs, rows, missing = [], [], []
    for e in sorted((plan or {}).get('queue') or [], key=lambda x: (x['cohort'], x['case'])):
        raw = (read_json(hdirs.get(e['cohort'], Path('/nonexistent')) / f"{e['case']}.json") or {}).get('raw') or {}
        shas = [str((raw.get(k) or {}).get('sha256') or '') for k in ('atom', 'contact', 'mesh', 'deck')]
        if '' in shas:
            missing.append(e['case'])
        pairs.append((e['case'], e['cohort']))
        rows.append('\t'.join([e['case'], e['cohort'], *shas]))
    return dict(n=len(pairs), ids_sha256=ids_digest(pairs), raw_sha256_table_sha256=hashlib.sha256(('\n'.join(rows) + '\n').encode('utf-8')).hexdigest(),
                missing_raw_sha=missing, cohort_tsv_sha256={c['name']: sha256_file(Path(c['cohort'])) for c in (plan or {}).get('cohorts') or []})


def code_fp(hashes):
    """봉인 지문 — 코드 해시 지도 (정렬) 의 sha256.  비었거나 빠진 파일 (None · 빈 값) 이 있으면 None (봉인 불가 — 무엇과도 같지 않다)."""
    if not isinstance(hashes, dict) or not hashes or any(not v for v in hashes.values()):
        return None
    return hashlib.sha256(json.dumps(sorted(hashes.items()), separators=(',', ':')).encode('utf-8')).hexdigest()


def seal_diff(now, sealed) -> list:
    """발사 봉인 (manifest code_hashes) 과 다른 파일 — 값이 다르거나 · 어느 쪽이든 없거나 비었으면 다르다 (빠진 해시 = 다름)."""
    now, sealed = now or {}, sealed or {}
    return sorted(k for k in set(CODE_FILES) | set(now) | set(sealed) if not now.get(k) or now.get(k) != sealed.get(k))


def code_root(man) -> Path:
    """워커가 실제로 도는 체크아웃 = 발사 때의 리포 (manifest repo_root · 옛 manifest 면 이 실행기의 리포).  봉인은 여기서 잰다."""
    rr = (man or {}).get('repo_root')
    return Path(rr) if rr else ROOT


def _same_root(root) -> bool:
    try:
        return Path(root).resolve() == ROOT
    except OSError:
        return False


def _hashes_at(root) -> dict:
    #  이 실행기 자신의 체크아웃이면 인자 없이 부른다 — 외부 탐침 (Codex new_probes) 이 code_hashes · git_info 를 인자 없는 대역으로 바꿔 끼운다
    return code_hashes() if _same_root(root) else code_hashes(root)


def _git_at(root) -> dict:
    return git_info() if _same_root(root) else git_info(root)


def git_info(root=None):
    r = Path(root) if root is not None else ROOT

    def g(*a):
        try:
            return subprocess.run(['git', '-C', str(r), *a], capture_output=True, text=True, timeout=30).stdout
        except Exception:                                   # noqa: BLE001
            return ''
    sha = g('rev-parse', 'HEAD').strip()
    #  ⚠ strip() 을 먼저 하면 첫 줄의 선행 공백 (상태 칸) 이 지워져 경로 첫 글자를 먹는다 (seal_s3_prerun 의 같은 결함) — 줄만 나눈다
    porcelain = [ln for ln in g('status', '--porcelain', '--untracked-files=no').splitlines() if ln.strip()]
    return dict(sha=sha, short=sha[:9], branch=g('rev-parse', '--abbrev-ref', 'HEAD').strip(),
                dirty=bool(porcelain), porcelain=porcelain)


def _rec_sha(rec):
    """케이스 기록 (dict) 의 sha256 — 정렬 키 JSON.  기록이 아니면 None."""
    if not isinstance(rec, dict):
        return None
    return hashlib.sha256(json.dumps(rec, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode('utf-8')).hexdigest()


def _status_view(cdir: Path, case: str):
    """케이스 폴더 `out/status.json` → (그 케이스 기록 | None, runs 목록).  배치는 케이스 기록과 그 실행의 runs[] 항목을 같이 쓴다."""
    st = read_json(Path(cdir) / 'out' / 'status.json')
    if not isinstance(st, dict):
        return None, []
    rec = (st.get('cases') or {}).get(case)
    runs = st.get('runs') if isinstance(st.get('runs'), list) else []
    return (rec if isinstance(rec, dict) else None), runs


# ─────────────────────────────────── 발사 봉인 (RGLR3-01) ───────────────────────────────────
def seal_context(man, *, dirty_allowed=False, mixed_allowed=False) -> dict:
    """이번 실행 (run · retry) 이 대조할 발사 봉인 — manifest code_hashes · 지문 · 워커 체크아웃 · 발사 sha · 넘김 (기록된다)."""
    hashes = dict((man or {}).get('code_hashes') or {})
    fp = code_fp(hashes)
    s = (man or {}).get('seal') or {}
    if s.get('code_fp') and s.get('code_fp') != fp:          # manifest 안에서 지문 ↔ 해시 지도가 어긋난다 — 봉인 불가
        fp = None
    return dict(fp=fp, hashes=hashes, root=code_root(man), sha=((man or {}).get('git') or {}).get('sha') or '',
                dirty_allowed=bool(dirty_allowed), mixed_allowed=bool(mixed_allowed))


def seal_gate(man) -> dict:
    """retry 시작 관문 — 워커 체크아웃의 HEAD · 봉인 파일 해시 · dirty 를 발사 봉인과 대조.  mixed (코드 · HEAD · 빠진 해시) · dirty · 기대 망 세대 (넘김 불가) 사유 목록."""
    seal = seal_context(man)
    g = _git_at(seal['root'])
    h = _hashes_at(seal['root'])
    changed = seal_diff(h, seal['hashes'])
    mixed = []
    if seal['fp'] is None:
        mixed.append('발사 봉인이 불완전하다 (manifest code_hashes 에 빠진 파일 · 지문 불일치) — 대조할 기준이 없다')
    if changed:
        mixed.append(f'코드가 발사 봉인과 다르다 (HEAD 가 같아도) — 바뀐 · 빠진 파일 {changed}')
    if (g.get('sha') or '') != seal['sha']:
        mixed.append(f'HEAD {str(g.get("sha") or "?")[:9]} ≠ 발사 {seal["sha"][:9] or "?"} (워커 체크아웃 {seal["root"]})')
    dirty = [f'추적 파일이 바뀐 트리 (워커 체크아웃 {seal["root"]}) {list(g.get("porcelain") or [])[:5]}'] if g.get('dirty') else []
    #  ★ 10-07 G2RR-01 — 기대 망 세대 (manifest = 봉인 사본 = 지금 워커 체크아웃 코드가 내는 세대) · 넘김 불가
    gen_bad, gen_note = generation_gate(man, seal['root'])
    return dict(seal=seal, git=g, hashes=h, fp=code_fp(h), changed=changed, mixed=mixed, dirty=dirty,
                generation_bad=gen_bad, generation_note=gen_note)


def _evidence_start(seal, cdir: Path, case: str) -> dict:
    """시도 증거 앞 절반 — 띄우기 직전의 코드 지문 · git · 케이스 기록 위치 (이 시도가 기록을 썼는지 가르는 기준)."""
    h = _hashes_at(seal['root'])
    g = _git_at(seal['root'])
    rec, runs = _status_view(cdir, case)
    return dict(schema=ATTEMPT_SEAL_SCHEMA, launch_fp=seal['fp'], fp_start=code_fp(h), changed_start=seal_diff(h, seal['hashes']),
                git_sha_start=g.get('sha') or '', dirty_start=bool(g.get('dirty')), porcelain_start=list(g.get('porcelain') or [])[:10],
                dirty_allowed=seal['dirty_allowed'], mixed_allowed=seal['mixed_allowed'], code_root=str(seal['root']),
                runs_before=len(runs), record_sha_before=_rec_sha(rec), t_start=now_iso())


def _evidence_end(seal, ev: dict, cdir: Path, case: str):
    """시도 증거 뒤 절반 — 거둔 직후의 지문 · git · 이 시도가 쓴 기록 (runs[] 가 늘었거나 기록이 바뀌었으면 이 시도가 썼다).
    → (증거 dict, 이 시도가 쓴 기록 | None)."""
    h = _hashes_at(seal['root'])
    g = _git_at(seal['root'])
    rec, runs = _status_view(cdir, case)
    rsha = _rec_sha(rec)
    wrote = rec is not None and (len(runs) > ev.get('runs_before', 0) or rsha != ev.get('record_sha_before'))
    out = dict(ev, fp_end=code_fp(h), changed_end=seal_diff(h, seal['hashes']), git_sha_end=g.get('sha') or '',
               dirty_end=bool(g.get('dirty')), porcelain_end=list(g.get('porcelain') or [])[:10], runs_after=len(runs),
               record_sha=rsha, record_written=bool(wrote), worker_run=(runs[-1] if wrote and runs else None), t_end=now_iso())
    return out, (rec if wrote else None)


def _runs_by_no(root: Path) -> dict:
    out = {}
    for p in (Path(root) / 'runs').glob('run_*.json'):
        m = re.match(r'run_(\d+)\.json$', p.name)
        if m:
            out[int(m.group(1))] = read_json(p) or {}
    return out


def _judge_attempt(seal_fp, launch_sha, s: dict, st_runs: list):
    """새 형식 시도 (attempt_seal) 판정 → (판정, 사유)."""
    probs = []
    if s.get('launch_fp') != seal_fp:
        probs.append('시도 기록의 발사 지문 ≠ manifest 봉인')
    if s.get('fp_start') != seal_fp:
        probs.append(f'시작 지문 ≠ 발사 봉인 (바뀐 · 빠진 파일 {s.get("changed_start")})')
    if s.get('fp_end') != seal_fp:
        probs.append(f'끝 지문 ≠ 발사 봉인 (바뀐 · 빠진 파일 {s.get("changed_end")})')
    wr = s.get('worker_run')
    if not isinstance(wr, dict) or wr not in st_runs:
        probs.append('이 시도의 워커 runs[] 항목이 status.json 에 없다')
    elif launch_sha and wr.get('git_sha') != launch_sha:
        probs.append(f'워커 코드 sha {str(wr.get("git_sha"))[:9]} ≠ 발사 {launch_sha[:9]}')
    for k in ('git_sha_start', 'git_sha_end'):
        if launch_sha and s.get(k) is not None and s.get(k) != launch_sha:
            probs.append(f'{k} {str(s.get(k))[:9]} ≠ 발사 {launch_sha[:9]}')
    src = [n for n, v in (('실행기 시작', s.get('dirty_start')), ('실행기 끝', s.get('dirty_end')),
                          ('워커 기록', (wr or {}).get('dirty') if isinstance(wr, dict) else None)) if v]
    if src and not s.get('dirty_allowed'):
        probs.append(f'추적 파일이 바뀐 트리 (dirty — {" · ".join(src)}) 에서 돌았는데 그 실행은 --allow-dirty 가 아니었다')
    if probs:
        return 'UNSEALED', '; '.join(probs)
    if src:
        return 'SEALED_DIRTY_ALLOWED', f'지문 = 봉인 · dirty ({" · ".join(src)}) — 그 실행의 --allow-dirty 로 기록됨'
    return 'SEALED', '시작 · 끝 지문 = 발사 봉인 · git sha = 발사 · dirty 아님'


def _judge_legacy(man, legacy: list, rec: dict, st_runs: list, runs_by_no: dict, launch_sha: str):
    """옛 형식 시도 (attempt_seal 없음 — 이 수정 전 실행기) 판정 → (판정, 사유).  입증되는 것은 첫 `run` 의 유일한 시도뿐 (docstring ⓒ)."""
    if len(legacy) != 1:
        return 'UNSEALED', (f'옛 형식 시도 {len(legacy)} 번 (재시도 포함) — 옛 retry 는 발사 봉인과 코드를 대조하지 않았고 시도별 지문이 없다 '
                            '(RGLR3-01) — 다시 돌릴 대상')
    a = legacy[0]
    if a.get('run') != 1 or a.get('attempt') not in (1, None):
        return 'UNSEALED', f'옛 형식 시도가 첫 run 이 아니다 (run {a.get("run")} · 시도 {a.get("attempt")}) — 옛 retry 는 입증 못 한다 (RGLR3-01)'
    probs = []
    #  그 시도가 이 기록을 썼나 — 옛 실행기는 시도 결과 (outcome) 를 끝난 직후의 기록 상태로 · network_run_id 를 그 기록에서 옮겨 적었다
    if a.get('outcome') != rec.get('status'):
        probs.append(f'유일한 시도의 결과 {a.get("outcome")!r} ≠ 기록 상태 {rec.get("status")!r} — 그 시도가 이 기록을 쓰지 않았다')
    if a.get('network_run_id') is not None and a.get('network_run_id') != rec.get('network_run_id'):
        probs.append(f'시도의 network_run_id {a.get("network_run_id")!r} ≠ 기록 {rec.get("network_run_id")!r}')
    r1 = runs_by_no.get(1)
    if not isinstance(r1, dict) or not r1:
        probs.append('runs/run_001.json 없음')
    else:
        if r1.get('kind') not in (None, 'run'):
            probs.append(f'run_001 의 종류 {r1.get("kind")!r} ≠ run')
        if 'code_changed_during_run' not in r1:
            probs.append('run_001 에 실행 중 코드 변화 기록이 없다')
        elif r1.get('code_changed_during_run'):
            probs.append(f'첫 실행 중 코드가 바뀌었다 (h0 ≠ h1) {r1.get("code_changed_during_run")}')
    g = man.get('git') or {}
    if not (g.get('dirty') is False or (g.get('dirty') is None and not man.get('allow_dirty'))):
        probs.append('발사 사전 점검이 깨끗한 트리가 아니었다 (git dirty · --allow-dirty)')
    if len(st_runs) != 1:
        probs.append(f'status.json runs[] {len(st_runs)} 건 — 기록을 쓴 실행이 첫 run 하나가 아니다')
    else:
        wr = st_runs[0] if isinstance(st_runs[0], dict) else {}
        if launch_sha and wr.get('git_sha') != launch_sha:
            probs.append(f'워커 코드 sha {str(wr.get("git_sha"))[:9]} ≠ 발사 {launch_sha[:9]}')
        if wr.get('dirty') is not False:
            probs.append(f'워커 기록 dirty={wr.get("dirty")!r}')
    if probs:
        return 'UNSEALED', '옛 형식 첫 run — ' + '; '.join(probs)
    return 'SEALED_LEGACY', ('옛 형식 — 첫 run 의 유일한 시도 · 깨끗한 사전 점검 · run_001 실행 중 코드 변화 0 (h0 = h1 · h0 은 manifest 해시와 '
                             '같은 프로세스에서 곧바로 잰 값) · 워커 runs 1 건 (발사 sha · dirty false)')


def case_seal(root: Path, man: dict, case: str, runs_by_no=None, history=False) -> dict:
    """케이스 판정 (docstring '발사 봉인' ⓒ) — 지금 케이스 기록을 쓴 시도의 증거로.  → dict(case · verdict · why · attempt · run · form …).
    ★ 10-07 G2RR2-01 — 옛 형식 시도 (시도 지문 없음) 판정은 history (manifest 자격 = 등록된 역사 형식 · 역사 모드) 일 때만.  새 실행 형식 ROOT 의 시도 지문
    없는 기록 = UNSEALED (지문이 없다는 것으로 옛 형식을 추론하지 않는다)."""
    if runs_by_no is None:
        runs_by_no = _runs_by_no(root)
    seal = seal_context(man)
    cdir = case_dir(Path(root), case)
    atts = [a for a in ((read_json(cdir / 'worker.json') or {}).get('attempts') or []) if isinstance(a, dict)]
    rec, st_runs = _status_view(cdir, case)
    out = dict(case=case, record_status=(rec or {}).get('status'), n_attempts=len(atts), attempt=None, run=None, form=None,
               verdict=None, why='', record_sha=_rec_sha(rec))
    if rec is None:
        out.update(verdict='NO_RECORD', why='케이스 기록 없음 — 계산되지 않았다 (merge 는 failed 로 싣는다 · retry 대상)')
        return out
    if seal['fp'] is None:
        out.update(verdict='UNSEALED', why='발사 봉인이 불완전하다 (manifest code_hashes 에 빠진 파일 · 지문 불일치) — 대조할 기준이 없다')
        return out
    for a in reversed(atts):
        s = a.get('seal')
        if isinstance(s, dict) and s.get('record_written') and s.get('record_sha') == out['record_sha']:
            v, why = _judge_attempt(seal['fp'], seal['sha'], s, st_runs)
            out.update(verdict=v, why=why, attempt=a.get('attempt'), run=a.get('run'), form='attempt_seal',
                       fp_start=s.get('fp_start'), fp_end=s.get('fp_end'), git_sha=(s.get('worker_run') or {}).get('git_sha'))
            return out
    if any(isinstance(a.get('seal'), dict) and a['seal'].get('record_written') for a in atts):
        out.update(verdict='UNSEALED', form='attempt_seal',
                   why='지금 케이스 기록이 어느 시도가 쓴 기록과도 같지 않다 (시도 뒤에 바뀌었다 · 실행기 밖에서 썼다)')
        return out
    legacy = [a for a in atts if not isinstance(a.get('seal'), dict)]
    if not legacy:
        out.update(verdict='UNSEALED', why='기록을 쓴 시도 증거가 없다 (worker.json 시도 없음 · 실행기 밖에서 쓴 기록)')
        return out
    if not history:
        out.update(verdict='UNSEALED', form='legacy',
                   why='시도 지문 (attempt_seal) 없는 옛 형식 시도 — 새 실행 형식 ROOT 에서는 옛 형식으로 추론하지 않는다 (역사 형식 = 등록된 옛 실행 · 역사 모드만 · '
                       'G2RR2-01)')
        return out
    v, why = _judge_legacy(man, legacy, rec, st_runs, runs_by_no, seal['sha'])
    out.update(verdict=v, why=why, attempt=legacy[-1].get('attempt'), run=legacy[-1].get('run'), form='legacy',
               git_sha=(st_runs[-1] if st_runs and isinstance(st_runs[-1], dict) else {}).get('git_sha'))
    return out


def meminfo():
    """/proc/meminfo → 바이트 (Linux · WSL).  없으면 빈 dict."""
    d = {}
    try:
        with open('/proc/meminfo', encoding='ascii', errors='replace') as fh:
            for ln in fh:
                k, _, v = ln.partition(':')
                parts = v.split()
                if parts and parts[0].isdigit():
                    d[k.strip()] = int(parts[0]) * (1024 if len(parts) > 1 and parts[1].lower() == 'kb' else 1)
    except OSError:
        pass
    return d


def gib(b):
    return None if b is None else round(b / 2 ** 30, 2)


def cpu_info():
    n = os.cpu_count()
    try:
        aff = len(os.sched_getaffinity(0))
    except (AttributeError, OSError):
        aff = n
    return dict(cpu_count=n, cpu_affinity=aff)


def est_mem_mb(contacts: int) -> float:
    return MEM_BASE_MB + MEM_PER_KCONTACT_MB * contacts / 1000.0


def est_time_s(contacts: int) -> float:
    return TIME_PER_KCONTACT_S * contacts / 1000.0


def worker_env(case_dir: Path, lock_mode: str) -> dict:
    env = dict(os.environ)
    env.update(THREAD_ENV)
    env['PYTHONDONTWRITEBYTECODE'] = '1'                 # ④
    env['PYTHONUNBUFFERED'] = '1'                        # 로그가 바로 보이게
    env.setdefault('MPLBACKEND', 'Agg')
    if lock_mode == 'per-case':
        env['TMPDIR'] = str(case_dir / 'tmp')            # ② — network lock 파일이 이 케이스 안에 생긴다
    return env


def purge_pyc(scripts_dir: Path, dry=False) -> int:
    """④ — run_pipeline 이 지우는 것과 같은 glob (`scripts/__pycache__/*.pyc`) 을 발사 전에 한 번 지운다."""
    hits = sorted((scripts_dir / '__pycache__').glob('*.pyc'))
    if not dry:
        for p in hits:
            with contextlib.suppress(FileNotFoundError):
                p.unlink()
    return len(hits)


@contextlib.contextmanager
def root_lock(root: Path):
    """같은 ROOT 에 실행기 둘이 붙지 않게 (run · retry · merge)."""
    import fcntl
    root.mkdir(parents=True, exist_ok=True)
    fh = open(root / '.launcher.lock', 'a+')
    try:
        try:
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise LaunchError(f'{root} 를 다른 실행기가 쓰고 있다 (.launcher.lock) — 끝난 뒤 다시')
        yield
    finally:
        with contextlib.suppress(OSError):
            import fcntl as _f
            _f.flock(fh.fileno(), _f.LOCK_UN)
        fh.close()


def pid_alive(pid: int, case: str) -> bool:
    """그 pid 가 살아 있고 명령줄에 케이스 이름이 있는가 (retry 가 아직 도는 고아 워커를 다시 띄우지 않게)."""
    try:
        os.kill(int(pid), 0)
    except (ProcessLookupError, ValueError, TypeError):
        return False
    except PermissionError:
        return True
    try:
        cmd = Path(f'/proc/{int(pid)}/cmdline').read_bytes().replace(b'\0', b' ').decode('utf-8', 'replace')
        return case in cmd
    except OSError:
        return True


# ─────────────────────────────────── 계획 ───────────────────────────────────
def cohort_specs(args) -> dict:
    specs = {k: dict(v) for k, v in COHORT_SPECS.items()}
    for name in specs:
        for key in ('harvest', 'cohort'):
            v = getattr(args, f'{name}_{key}', None)
            if v:
                specs[name][key] = v
    return specs


def build_plan(cohorts, specs, case_filter=(), order='cost') -> dict:
    """→ {'cohorts': [...], 'queue': [{case, cohort, contacts, est_mem_mb, est_time_s}, …]} — 결정적 (같은 입력 = 같은 순서)."""
    out_c, queue, seen = [], [], {}
    want = set(case_filter or ())
    for name in cohorts:
        if name not in specs:
            raise LaunchError(f'모르는 코호트 {name!r} — {sorted(specs)}')
        sp = specs[name]
        hdir, coh = _abs(sp['harvest']), _abs(sp['cohort'])
        if not hdir.is_dir():
            raise LaunchError(f'{name}: 수확 폴더가 없다 — {hdir}')
        if not coh.is_file():
            raise LaunchError(f'{name}: 코호트 TSV 가 없다 — {coh}')
        #  케이스 목록 = 배치와 같은 규칙 (`lhs_webapp_batch.run_batch` — 수확 폴더의 *.json · '_' 로 시작하면 케이스가 아니다)
        cases = sorted(p.stem for p in hdir.glob('*.json') if not p.name.startswith('_'))
        n_sel = 0
        for c in cases:
            if want and c not in want:
                continue
            if c in seen:
                raise LaunchError(f'케이스 {c} 가 두 코호트에 있다 ({seen[c]} · {name})')
            seen[c] = name
            h = read_json(hdir / f'{c}.json') or {}
            k = (h.get('contact_scan') or {}).get('n_rows_last')
            if not isinstance(k, int) or k <= 0:              # 옛 수확 — 입자 수로 대신 (비용 순서에만 쓴다)
                k = int(sum((h.get('phase_counts') or {}).values()) or 0)
            queue.append(dict(case=c, cohort=name, contacts=int(k),
                              est_mem_mb=round(est_mem_mb(k), 1), est_time_s=round(est_time_s(k), 1)))
            n_sel += 1
        out_c.append(dict(name=name, harvest_dir=str(hdir), cohort=str(coh), n_harvest=len(cases), n_selected=n_sel,
                          expect_n=sp.get('expect_n'), union=sp.get('union', ''), design=sp.get('design', '')))
    miss = sorted(want - set(seen))
    if miss:
        raise LaunchError(f'--case 가 어느 수확 폴더에도 없다: {miss}')
    if not queue:
        raise LaunchError('돌릴 케이스가 없다')
    if order == 'cost':
        queue.sort(key=lambda e: (-e['contacts'], e['case']))
    else:
        queue.sort(key=lambda e: e['case'])
    return dict(cohorts=out_c, queue=queue, order=order)


def case_dir(root: Path, case: str) -> Path:
    return root / 'cases' / case


def case_cmd(python, worker_script, cspec, case, cdir: Path, root_from='', root_to='', force=False) -> list:
    cmd = [str(python), str(worker_script), '--stop-after', STOP, '--case', case,
           '--harvest-dir', cspec['harvest_dir'], '--cohort', cspec['cohort'],
           '--work', str(cdir / 'work'), '--out-dir', str(cdir / 'out')]
    if root_from:
        cmd += ['--root-from', root_from, '--root-to', root_to or '']
    if force:                       # retry — done · partial 이지만 봉인 밖 (UNSEALED) 기록을 다시 계산한다 (배치는 --force 없이는 건너뛴다)
        cmd += ['--force']
    return cmd


def raw_problems(plan, root_from='', root_to='') -> list:
    """원자료 실재 · 같은 step 메시 — 배치가 케이스마다 REFUSED 로 남길 것을 발사 전에 센다 (sha 는 배치가 본다 · 비싸다)."""
    out = []
    for cs in plan['cohorts']:
        rows = {r['case']: r for r in HB.read_cohort(Path(cs['cohort']))}
        for e in plan['queue']:
            if e['cohort'] != cs['name']:
                continue
            r = rows.get(e['case'])
            if r is None:
                out.append((e['case'], '봉인 코호트에 없다'))
                continue
            for k, col in (('atom', 'atom_file'), ('contact', 'contact_file'), ('deck', 'deck')):
                p = HB.remap((r.get(col) or '').strip(), root_from, root_to)
                if not (r.get(col) or '').strip() or not p.is_file():
                    out.append((e['case'], f'{k} 파일 없음: {p}'))
            a = HB.remap((r.get('atom_file') or '').strip(), root_from, root_to)
            if a.is_file():
                mesh, _pick, why = HB.pick_mesh(a)
                if mesh is None:
                    out.append((e['case'], f'같은 step 메시 없음 — {why}'))
    return out


def python_versions(python) -> dict:
    code = ('import json, sys\nv = {"python": sys.version.split()[0], "executable": sys.executable}\n'
            'for m in ("numpy", "scipy", "pandas"):\n'
            '    try:\n        v[m] = __import__(m).__version__\n'
            '    except Exception as e:\n        v[m] = "MISSING " + type(e).__name__\n'
            'print(json.dumps(v))')
    try:
        r = subprocess.run([str(python), '-c', code], capture_output=True, text=True, timeout=120,
                           env=dict(os.environ, **THREAD_ENV, PYTHONDONTWRITEBYTECODE='1'))
        return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception as e:                                  # noqa: BLE001
        return dict(error=f'{type(e).__name__}: {e}')


def app_supports_network() -> bool:
    """정적 확인 — 웹앱 `PIPELINE_STOP_AFTER` 에 'network' 가 있는가 (없으면 194 건이 전부 ValueError 로 failed)."""
    try:
        src = (ROOT / 'webapp' / 'app.py').read_text(encoding='utf-8')
    except OSError:
        return False
    m = re.search(r'^PIPELINE_STOP_AFTER\s*=\s*\(([^)]*)\)', src, re.M)
    return bool(m and "'network'" in m.group(1))


def preflight(args, plan, root: Path, budget_mb) -> dict:
    """CPU · 메모리 · 디스크 · git · 원자료 · 의존 — 경고 (warn) 와 중단 (stop) 을 나눠 돌려준다."""
    warn, stop = [], []
    #  봉인 대상 코드가 디스크에 다 있어야 한다 — 없는 경로는 해시가 None 으로 조용히 빠진다 (10-05 · 두 경로가 webapp/ 로 잘못 적혀 있었다)
    _miss = sorted(k for k, v in code_hashes().items() if v is None)
    if _miss:
        stop.append(f'봉인 대상 코드 파일이 없다: {_miss}')
    #  ★ 10-07 §7-3 — 워커가 import 하는 리포 모듈 (전이 닫힘) 이 전부 봉인 대상인가 (새 import 가 생겼는데 목록이 그대로면 봉인이 새는 것)
    clo = code_dependency_closure()
    _outside = [f for f in clo['files'] if f not in CODE_FILES]
    if _outside or clo['errors']:
        stop.append(f'봉인 밖 의존 모듈 {_outside} · 닫힘 해석 오류 {clo["errors"][:3]} — CODE_FILES 를 먼저 고칠 것 (Codex 세대 2 재검증 §7-3 전이 의존)')
    #  ★ 10-07 G2RR2-03 — 봉인 파일의 함수 안 import 중 봉인 밖 모듈은 전부 경로 밖으로 분류돼 있어야 한다 (새 지연 import 가 생기면 발사하지 않는다)
    cen = lazy_import_census()
    if cen['unclassified']:
        stop.append(f'분류 밖 지연 import {[(a, f, q) for a, f, q, _n in cen["unclassified"][:5]]} — 경로 위면 CODE_FILES · DEP_LAZY 에, 경로 밖이면 '
                    'DEP_LAZY_OFFPATH 에 사유와 함께 (Codex 세대 2 재검증 2 §4 G2RR2-03)')
    if cen['stale']:
        warn.append(f'지연 import 분류표의 낡은 항목 (지금 코드에 없음) {cen["stale"][:5]} — 표 정리')
    #  ★ 10-07 G2RR-01 — 기대 망 세대 = 이 체크아웃 (워커 체크아웃) 의 봉인 코드에서 유도 (손으로 적지 않는다)
    gp = derive_generation(ROOT, args.python)
    _gwhy = generation_probe_problem(gp)
    if _gwhy:
        stop.append(f'기대 망 세대 — {_gwhy}')
    #  ★ 10-07 §7-3 — 입력 지문 (ID · 코호트 · 원자료 sha256) · 원자료 sha 가 없는 수확 JSON 은 워커가 대조할 수 없다
    idg = plan_input_digest(plan)
    if idg['missing_raw_sha']:
        stop.append(f'수확 JSON 에 원자료 sha256 (raw.atom · contact · mesh · deck) 이 없는 케이스 {idg["missing_raw_sha"][:5]} — 입력 지문을 봉인할 수 없다')
    cpu = cpu_info()
    mi = meminfo()
    lanes = args.lanes
    q = plan['queue']
    first = q[:lanes]
    if cpu['cpu_affinity'] and lanes > cpu['cpu_affinity']:
        warn.append(f'레인 {lanes} > 쓸 수 있는 CPU {cpu["cpu_affinity"]} — 레인당 1 코어가 아니다 (과다 구독)')
    avail = mi.get('MemAvailable')
    first_mb = sum(e['est_mem_mb'] for e in first)
    if avail is not None and first_mb > avail / 2 ** 20:
        warn.append(f'처음 {len(first)} 건 (큐 앞 = 가장 큰 침대) 의 메모리 추정 합 {first_mb / 1024:.1f} GB > MemAvailable '
                    f'{gib(avail)} GB — 예산 관문이 동시 수를 줄인다 (추정은 real_14 기준 · WSL 시범으로 고칠 것)')
    if args.mem_budget_gb is not None and args.mem_budget_gb <= 0:
        warn.append('메모리 예산 끔 (--mem-budget-gb 0) — 큰 침대 20 개가 한꺼번에 돌 수 있다 (OOM 이면 그 케이스는 failed · 다시 retry)')
    git = git_info()
    if git['dirty'] and not args.allow_dirty:
        hint = ' (LHS-27 부산물 — `git checkout -- ' + LHS27_FILE + '` 로 되돌린다)' if any(
            ln[3:].strip() == LHS27_FILE for ln in git['porcelain']) else ''
        stop.append(f'추적 파일이 바뀌어 있다 {git["porcelain"][:5]}{hint} — 봉인 커밋에서 돌릴 것 (진짜 의도면 --allow-dirty · 기록된다)')
    if not git['sha']:
        warn.append('git sha 를 못 읽었다 — 세대 대조 (merge) 가 약해진다')
    for cs in plan['cohorts']:
        if not args.case and cs['expect_n'] and cs['n_harvest'] != cs['expect_n']:
            warn.append(f'{cs["name"]}: 수확 JSON {cs["n_harvest"]} 건 ≠ 기대 {cs["expect_n"]} 건')
    if not app_supports_network():
        stop.append("webapp/app.py 의 PIPELINE_STOP_AFTER 에 'network' 가 없다 — 이 코드로는 망 정지 배치를 돌릴 수 없다")
    probs = raw_problems(plan, args.root_from, args.root_to)
    if probs and not args.allow_missing_raw:
        stop.append(f'원자료 · 메시 문제 {len(probs)} 건 (예: {probs[:3]}) — 경로 치환 (--root-from/--root-to) 확인 · '
                    '그래도 돌리려면 --allow-missing-raw (그 케이스는 배치가 REFUSED 로 남긴다)')
    elif probs:
        warn.append(f'원자료 · 메시 문제 {len(probs)} 건 — 그 케이스는 REFUSED 로 남는다 (--allow-missing-raw)')
    disk_need = sum(e['contacts'] for e in q) * DISK_PER_CONTACT_B
    probe = root if root.exists() else root.parent
    while not probe.exists() and probe != probe.parent:
        probe = probe.parent
    try:
        free = shutil.disk_usage(probe).free
    except OSError:
        free = None
    if free is not None and disk_need * 1.2 > free:
        warn.append(f'디스크 여유 {gib(free)} GB < 결과 추정 {gib(disk_need)} GB × 1.2 (케이스 결과 폴더 ≈ {DISK_PER_CONTACT_B} B/접촉)')
    if args.network_lock == 'shared' and lanes > 1:
        warn.append('--network-lock shared — 망 단계는 기계 전체에서 하나씩 돈다 (레인은 접촉 · 피복 단계만 겹친다)')
    tot_s = sum(e['est_time_s'] for e in q)
    eff = max(1, min(lanes, cpu['cpu_affinity'] or lanes))
    return dict(cpu=cpu, mem=dict(MemTotal_GB=gib(mi.get('MemTotal')), MemAvailable_GB=gib(avail),
                                  SwapTotal_GB=gib(mi.get('SwapTotal')), SwapFree_GB=gib(mi.get('SwapFree'))),
                lanes=lanes, mem_budget_mb=budget_mb, first_lanes_est_mem_GB=round(first_mb / 1024, 2),
                est_mem_largest_mb=max(e['est_mem_mb'] for e in q), disk_free_GB=gib(free), disk_need_GB=gib(disk_need),
                est_serial_h=round(tot_s / 3600, 2), est_makespan_h=round(max(tot_s / eff, max(e['est_time_s'] for e in q)) / 3600, 2),
                git=git, raw_problems=probs[:50], n_raw_problems=len(probs), warn=warn, stop=stop, generation=gp, dependency_closure=clo,
                input_digest=idg, lazy_census=dict(n_lazy=len(cen['lazy']), unclassified=cen['unclassified'], stale=cen['stale']))


def print_preflight(pf, plan, args, root):
    p = print
    p(f'══ 사전 점검 — ROOT {root}')
    p(f'  CPU {pf["cpu"]["cpu_count"]} (쓸 수 있는 {pf["cpu"]["cpu_affinity"]}) · 레인 {pf["lanes"]} · 스레드/레인 1 '
      f'({", ".join(f"{k}=1" for k in THREAD_ENV)})')
    m = pf['mem']
    p(f'  메모리 MemTotal {m["MemTotal_GB"]} GB · MemAvailable {m["MemAvailable_GB"]} GB · Swap {m["SwapFree_GB"]}/{m["SwapTotal_GB"]} GB')
    bud = pf['mem_budget_mb']
    p(f'  메모리 예산 {"끔" if not bud else f"{bud / 1024:.1f} GB"} · 실측 바닥 --min-free-gb {args.min_free_gb} · '
      f'큐 앞 {min(pf["lanes"], len(plan["queue"]))} 건 추정 합 {pf["first_lanes_est_mem_GB"]} GB · 가장 큰 침대 추정 '
      f'{pf["est_mem_largest_mb"] / 1024:.2f} GB  (⚠ 케이스 최대 메모리는 아직 모른다 — real_14 549 MB @ 106,563 접촉에서 잡은 추정 · '
      f'시범 · 본 실행의 worker.json 실측으로 고칠 것)')
    p(f'  디스크 여유 {pf["disk_free_GB"]} GB · 결과 추정 {pf["disk_need_GB"]} GB')
    p(f'  시간 추정 (컨테이너 real_14 기준 · 거칠다): 직렬 {pf["est_serial_h"]} h · 이 레인 수 {pf["est_makespan_h"]} h — 케이스별 실측 초는 progress.tsv')
    g = pf['git']
    p(f'  코드 {g["short"]} ({g["branch"]}) dirty={g["dirty"]}' + (f' {g["porcelain"][:3]}' if g['dirty'] else '')
      + f' · 봉인 지문 code_fp {code_fp(code_hashes())} (CODE_FILES {len(CODE_FILES)})')
    p(f'  network lock = {args.network_lock}  (per-case = 케이스마다 TMPDIR — 망 단계도 동시에 · shared = 웹앱처럼 하나씩)')
    for cs in plan['cohorts']:
        p(f'  코호트 {cs["name"]}: 수확 {cs["n_harvest"]} 건 (선택 {cs["n_selected"]}) · {cs["harvest_dir"]} · 코호트 {cs["cohort"]}')
    p(f'  원자료 · 메시 문제 {pf["n_raw_problems"]} 건')
    gp, clo = pf.get('generation') or {}, pf.get('dependency_closure') or {}
    p(f'  기대 망 세대 ({GEN_KEY} — 이 체크아웃의 봉인 코드에서 유도): {gp.get("generation")!r} · 세대 계약 문제 {len(gp.get("problems") or [])} · '
      f'모드 {gp.get("modes")}' + (f' · ⛔ {gp.get("error")[:200]}' if gp.get('error') else ''))
    _out = [f for f in clo.get('files') or [] if f not in CODE_FILES]
    p(f'  전이 의존 닫힘 {len(clo.get("files") or [])} 모듈 ⊆ 봉인 CODE_FILES {len(CODE_FILES)} — ' + ('✓' if not _out and not clo.get('errors')
                                                                                           else f'✗ 밖 {_out} · 오류 {clo.get("errors")}'))
    lc = pf.get('lazy_census') or {}
    p(f'  지연 import 분류 — 봉인 파일의 함수 안 리포 import {lc.get("n_lazy")} · 분류 밖 {len(lc.get("unclassified") or [])} — '
      + ('✓' if not lc.get('unclassified') else f'✗ {[(a, q) for a, _f, q, _n in lc.get("unclassified")][:5]}'))
    idg = pf.get('input_digest') or {}
    p(f'  입력 지문 (ID · 코호트 · 원자료 sha256 = 수확 JSON raw) — 케이스 {idg.get("n")} · ids_sha256 {idg.get("ids_sha256")} · '
      f'raw_sha256_table_sha256 {idg.get("raw_sha256_table_sha256")} · 원자료 sha 결손 {len(idg.get("missing_raw_sha") or [])}')
    p('  ⚠ Codex 세대 2 재검증 2 (10-07) = HOLD — 새 194 생산 · v1.3 인계는 Codex GO · 1저자 발사 승인 뒤 (등록 docs/reviews/lhs_network_batch_registration_20261007_g2.md).  '
      '이 실행기는 그 판정을 대신하지 않는다 — 어느 코드 · 세대로 돌았는지는 manifest.json 이 증명한다.')
    for w in pf['warn']:
        p(f'  ⚠ {w}')
    for s in pf['stop']:
        p(f'  ⛔ {s}')


# ─────────────────────────────────── 실행 (동적 큐) ───────────────────────────────────
class _Lane:
    __slots__ = ('entry', 'case', 'cdir', 'popen', 'pid', 't0', 'start_iso', 'log', 'cmd', 'attempt', 'env_note', 'ev')


def _attempt_no(cdir: Path) -> int:
    w = read_json(cdir / 'worker.json') or {}
    return len(w.get('attempts') or []) + 1


def _case_outcome(cdir: Path, case: str):
    st = read_json(cdir / 'out' / 'status.json')
    if not isinstance(st, dict):
        return None, None
    rec = (st.get('cases') or {}).get(case)
    return (rec or {}).get('status'), rec


def _sig_name(rc):
    if rc is None or rc >= 0:
        return None
    try:
        return signal.Signals(-rc).name
    except ValueError:
        return f'SIG{-rc}'


def run_queue(root: Path, manifest: dict, todo: list, lanes: int, run_no: int, *, budget_mb=None, min_free_gb=0.0,
              poll=0.5, out=print, seal=None) -> dict:
    """동적 큐 — 빈 레인이 다음 케이스를 집는다 (예산 · 실측 바닥 관문 · 봉인 관문).  → 이번 실행 요약 dict.

    seal (seal_context) — 시도마다 띄우기 직전 · 거둔 직후 증거를 worker.json attempts[].seal 에 남기고, 띄우기 직전 지문이 발사 봉인과
    다르거나 (넘김 없이) 트리가 dirty 면 그 케이스를 띄우지 않고 새 입장을 멈춘다 (도는 것은 끝까지 · 남은 케이스 = not_started)."""
    seal = seal or seal_context(manifest)
    seal_broken = []
    python, wscript = manifest['python'], manifest['worker_script']
    lock_mode = manifest['network_lock']
    #  ★ 10-07 G2RR2-03 — 시범의 실제 import 관측 (`run --observe-imports` · manifest 에 남는다 · 값에 닿지 않는다)
    obs_env = import_obs_env(root / IMPORT_OBS_DIR, code_root(manifest)) if manifest.get('observe_imports') else {}
    rf, rt = manifest.get('root_from') or '', manifest.get('root_to') or ''
    cspec = {c['name']: c for c in manifest['plan']['cohorts']}
    t_launch = time.monotonic()
    pending = collections.deque(todo)
    running: dict = {}
    done_n, n_total = 0, len(todo)
    counts = collections.Counter()
    throttle = dict(events=0, budget_events=0, backfills=0, max_concurrent=0)
    throttled = [False]
    head_wait = [0]
    cost_total = sum(e['contacts'] for e in todo) or 1
    cost_done = [0]
    progress = root / 'progress.tsv'
    if not progress.exists():
        progress.write_text('\t'.join(('case', 'cohort', 'attempt', 'run', 'outcome', 'rc', 'signal', 'wall_s', 'peak_rss_mb',
                                       'est_mem_mb', 'user_s', 'sys_s', 'contacts', 'start', 'end')) + '\n', encoding='utf-8')

    def est_running():
        return sum(l.entry['est_mem_mb'] for l in running.values())

    def start(e):
        nonlocal done_n
        ln = _Lane()
        ln.entry, ln.case = e, e['case']
        ln.cdir = case_dir(root, e['case'])
        #  RGLR3-01 ⓑ — 띄우기 직전 증거 · 봉인 관문 (지문이 봉인과 다르거나 넘김 없는 dirty 면 띄우지 않고 입장을 멈춘다)
        ln.ev = _evidence_start(seal, ln.cdir, ln.case)
        stop_why = []
        if not seal['mixed_allowed'] and ln.ev['fp_start'] != seal['fp']:
            stop_why.append(f'코드 지문 ≠ 발사 봉인 (바뀐 · 빠진 파일 {ln.ev["changed_start"]})')
        if not seal['dirty_allowed'] and ln.ev['dirty_start']:
            stop_why.append(f'추적 파일이 바뀐 트리 {ln.ev["porcelain_start"][:3]}')
        if stop_why:
            seal_broken.append(dict(case=ln.case, at=now_iso(), why=stop_why, fp=ln.ev['fp_start'], changed=ln.ev['changed_start']))
            pending.appendleft(e)
            out(f'⛔ 발사 봉인 관문 — {ln.case} 를 띄우지 않는다: {" · ".join(stop_why)} — 새 케이스 입장을 멈춘다 (도는 케이스는 끝까지)',
                flush=True)
            return
        for sub in ('work', 'out', 'tmp'):
            (ln.cdir / sub).mkdir(parents=True, exist_ok=True)
        ln.attempt = _attempt_no(ln.cdir)
        ln.cmd = case_cmd(python, wscript, cspec[e['cohort']], e['case'], ln.cdir, rf, rt, force=bool(e.get('force')))
        env = worker_env(ln.cdir, lock_mode)
        env.update(obs_env)
        ln.env_note = {k: env.get(k) for k in (*THREAD_ENV, 'TMPDIR', 'PYTHONDONTWRITEBYTECODE', *(('NP194_IMPORT_LOG',) if obs_env else ()))}
        ln.log = open(ln.cdir / 'log.txt', 'ab')
        ln.start_iso = now_iso()
        ln.log.write((f'===== attempt {ln.attempt} (run {run_no}) start {ln.start_iso} · cwd {ln.cdir} · lock {lock_mode}\n'
                      f'===== cmd: {shlex.join(ln.cmd)}\n').encode('utf-8'))
        ln.log.flush()
        ln.t0 = time.monotonic()
        #  ③ cwd = 케이스 폴더 · 새 세션 (중단 시 그 케이스의 프로세스 묶음을 통째로 끈다 — 솔버 자식 포함)
        try:
            ln.popen = subprocess.Popen(ln.cmd, cwd=str(ln.cdir), env=env, stdin=subprocess.DEVNULL, stdout=ln.log,
                                        stderr=subprocess.STDOUT, start_new_session=True)
        except OSError as e:                                 # 워커를 못 띄웠다 — 기록하고 다음 케이스로 (실행기는 서지 않는다)
            ln.log.write(f'===== LAUNCH_ERROR {type(e).__name__}: {e}\n'.encode('utf-8'))
            ln.log.close()
            ev_end, _rec = _evidence_end(seal, ln.ev, ln.cdir, ln.case)
            w = read_json(ln.cdir / 'worker.json') or dict(schema=WORKER_SCHEMA, case=ln.case, cohort=ln.entry['cohort'], attempts=[])
            w.setdefault('attempts', []).append(dict(attempt=ln.attempt, run=run_no, cmd=ln.cmd, cwd=str(ln.cdir), start=ln.start_iso,
                                                     end=now_iso(), rc=None, signal=None, outcome='LAUNCH_ERROR',
                                                     why=f'{type(e).__name__}: {e}', est_mem_mb=ln.entry['est_mem_mb'],
                                                     contacts=ln.entry['contacts'], seal=ev_end))
            write_json(ln.cdir / 'worker.json', w)
            done_n += 1
            counts['LAUNCH_ERROR'] += 1
            out(f'[{done_n}/{n_total}] {ln.case} LAUNCH_ERROR — {type(e).__name__}: {e}', flush=True)
            return
        ln.pid = ln.popen.pid
        write_json(ln.cdir / 'worker.pid.json', dict(pid=ln.pid, case=ln.case, attempt=ln.attempt, run=run_no, start=ln.start_iso))
        running[ln.case] = ln
        throttle['max_concurrent'] = max(throttle['max_concurrent'], len(running))

    def finalize(ln, status, ru, interrupted=False):
        nonlocal done_n
        rc = os.waitstatus_to_exitcode(status)
        ln.popen.returncode = rc                     # Popen 이 다시 기다리지 않게 (wait4 로 이미 거뒀다)
        t1 = time.monotonic()
        wall = round(t1 - ln.t0, 2)
        peak_kb = int(ru.ru_maxrss)                  # Linux = KB · 이 프로세스와 기다린 자식 중 최대 (트리 합이 아니다)
        #  RGLR3-01 ⓑ — 거둔 직후 증거.  결과는 **이 시도가 쓴** 기록으로만 읽는다 (옛 시도의 기록을 이 시도 결과로 읽지 않는다)
        ev, rec = _evidence_end(seal, ln.ev, ln.cdir, ln.case)
        if interrupted:
            outcome_s = 'interrupted'
        elif rec is None or not rec.get('status'):
            outcome_s = 'NO_RECORD'                  # 워커가 이 시도의 케이스 기록을 못 쓰고 끝났다 (죽음 · 신호 · 관문 전 예외)
        else:
            outcome_s = rec['status']
        att = dict(attempt=ln.attempt, run=run_no, cmd=ln.cmd, cwd=str(ln.cdir), lock_mode=lock_mode, env=ln.env_note,
                   start=ln.start_iso, end=now_iso(), t_start_s=round(ln.t0 - t_launch, 3), t_end_s=round(t1 - t_launch, 3),
                   wall_s=wall, rc=rc, signal=_sig_name(rc), peak_rss_kb=peak_kb, peak_rss_mb=round(peak_kb / 1024, 1),
                   est_mem_mb=ln.entry['est_mem_mb'], contacts=ln.entry['contacts'],
                   user_s=round(ru.ru_utime, 2), sys_s=round(ru.ru_stime, 2), outcome=outcome_s,
                   batch_elapsed_s=(rec or {}).get('elapsed_s'), why=(rec or {}).get('why'),
                   failed_stages=(rec or {}).get('failed_stages'), network_run_id=(rec or {}).get('network_run_id'), seal=ev)
        w = read_json(ln.cdir / 'worker.json') or dict(schema=WORKER_SCHEMA, case=ln.case, cohort=ln.entry['cohort'], attempts=[])
        w.setdefault('attempts', []).append(att)
        write_json(ln.cdir / 'worker.json', w)
        try:
            ln.log.write((f'===== attempt {ln.attempt} end {att["end"]} · outcome {outcome_s} · rc {rc}'
                          f'{" (" + att["signal"] + ")" if att["signal"] else ""} · wall {wall:.1f} s · peak RSS {peak_kb / 1024:.0f} MB · '
                          f'user {att["user_s"]:.1f} s · sys {att["sys_s"]:.1f} s\n').encode('utf-8'))
        finally:
            ln.log.close()
        with contextlib.suppress(FileNotFoundError):
            (ln.cdir / 'worker.pid.json').unlink()
        with open(progress, 'a', encoding='utf-8') as fh:
            fh.write('\t'.join(str(x) for x in (ln.case, ln.entry['cohort'], ln.attempt, run_no, outcome_s, rc, att['signal'] or '',
                                                wall, att['peak_rss_mb'], ln.entry['est_mem_mb'], att['user_s'], att['sys_s'],
                                                ln.entry['contacts'], att['start'], att['end'])) + '\n')
        done_n += 1
        counts[outcome_s] += 1
        cost_done[0] += ln.entry['contacts']
        el = time.monotonic() - t_launch
        eta = (el / cost_done[0] * (cost_total - cost_done[0])) if cost_done[0] else 0
        out(f'[{done_n}/{n_total}] {ln.case} {outcome_s} rc={rc}{" (" + att["signal"] + ")" if att["signal"] else ""} · '
            f'{wall:.0f} s · RSS {peak_kb / 1024:.0f} MB (추정 {ln.entry["est_mem_mb"]:.0f}) · 도는 중 {len(running)} · '
            f'경과 {el / 3600:.2f} h · 남은 추정 ≈ {eta / 3600:.2f} h (접촉 수 비례)'
            + (f' · {att["why"]}' if att['why'] and outcome_s not in KEEP else ''), flush=True)

    def admit():
        if not pending:
            return None
        if running and min_free_gb > 0:
            av = meminfo().get('MemAvailable')
            if av is not None and av < min_free_gb * 2 ** 30:
                if not throttled[0]:
                    throttle['events'] += 1
                    out(f'  ⏸ MemAvailable {gib(av)} GB < --min-free-gb {min_free_gb} — 새 케이스를 기다린다 (도는 중 {len(running)})',
                        flush=True)
                throttled[0] = True
                return None
        throttled[0] = False
        if not running or not budget_mb:
            return pending.popleft()
        if est_running() + pending[0]['est_mem_mb'] <= budget_mb:
            head_wait[0] = 0
            return pending.popleft()
        if head_wait[0] < lanes:                                 # backfill — 앞 케이스가 레인 수만큼 기다리기 전까지만
            for i, e in enumerate(pending):
                if est_running() + e['est_mem_mb'] <= budget_mb:
                    del pending[i]
                    throttle['backfills'] += 1
                    return e
        throttle['budget_events'] += 1
        return None

    def kill_all(why):
        out(f'⛔ {why} — 도는 케이스 {len(running)} 개를 끈다 (프로세스 묶음 SIGTERM → 20 s → SIGKILL)', flush=True)
        for ln in running.values():
            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.killpg(ln.pid, signal.SIGTERM)
        deadline = time.monotonic() + 20
        while running and time.monotonic() < deadline:
            for case, ln in list(running.items()):
                pid, st, ru = os.wait4(ln.pid, os.WNOHANG)
                if pid:
                    del running[case]
                    finalize(ln, st, ru, interrupted=True)
            time.sleep(0.2)
        for case, ln in list(running.items()):
            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.killpg(ln.pid, signal.SIGKILL)
            _pid, st, ru = os.wait4(ln.pid, 0)
            del running[case]
            finalize(ln, st, ru, interrupted=True)

    def _term(_s, _f):
        raise KeyboardInterrupt
    old_term = signal.signal(signal.SIGTERM, _term)
    interrupted = False
    try:
        while (pending and not seal_broken) or running:
            while len(running) < lanes and not seal_broken:
                e = admit()
                if e is None:
                    break
                start(e)
            reaped = False
            for case, ln in list(running.items()):
                pid, st, ru = os.wait4(ln.pid, os.WNOHANG)
                if pid:
                    del running[case]
                    finalize(ln, st, ru)
                    reaped = True
                    if pending and budget_mb and est_running() + pending[0]['est_mem_mb'] > budget_mb:
                        head_wait[0] += 1
            if not reaped:
                time.sleep(poll)
    except KeyboardInterrupt:
        interrupted = True
        kill_all('중단 (Ctrl-C · SIGTERM)')
    finally:
        signal.signal(signal.SIGTERM, old_term)
    return dict(run=run_no, n=n_total, finished=done_n, not_started=[e['case'] for e in pending], outcomes=dict(counts),
                interrupted=interrupted, wall_h=round((time.monotonic() - t_launch) / 3600, 3), seal_broken=seal_broken, **throttle)


# ─────────────────────────────────── merge ───────────────────────────────────
def _synth_failed(case, cdir: Path, wrec: dict | None, why0: str) -> dict:
    """워커가 케이스 기록을 못 남겼다 — 조용히 빠지지 않게 'failed' 기록을 만든다 (배치 어휘 그대로)."""
    att = ((wrec or {}).get('attempts') or [None])[-1] or {}
    why = why0
    if att:
        why = (f'워커가 케이스 기록 없이 끝났다 — rc {att.get("rc")}'
               + (f' ({att.get("signal")})' if att.get('signal') else '')
               + f' · 경과 {att.get("wall_s")} s · 최대 RSS {att.get("peak_rss_mb")} MB · 로그 {cdir / "log.txt"}')
    return dict(case=case, when=att.get('start') or '', stop_after=STOP, status='failed', failed_stages=['worker: no case record'],
                why=why, elapsed_s=att.get('wall_s'), parallel_synthesized=True)


def merge(root: Path, *, allow_mixed=False, out=print, historical=False) -> int:
    """케이스별 산출 → `<root>/merged/<코호트>/` (status.json · metrics_flat.csv · results/ · parallel_cases.tsv) + merge_report.json.

    rc 0 = 전 케이스 done · partial · 이상 없음 / 1 = 실패 · 이상 있음 (merged 는 쓴다 — 실패는 기록으로 남는다) /
    2 = 구조 이상 (남의 케이스 기록 · 스키마 · 정지점 · 세대 섞임) · **봉인 밖 기록** (case_seal = UNSEALED · RGLR3-01) → merged 를 바꾸지 않는다.
    allow_mixed (--allow-mixed-generation) = 세대 섞임 · 봉인 밖 기록을 알고도 묶는다 → rc 1 + 보고 (allow_mixed_generation · seal.unsealed).
    ★ 10-07 G2RR2-01 — 실행 형식 자격 (`launch_eligibility`) 이 current 여야 한다 · 역사 형식은 historical (--historical) 일 때만 · invalid = rc 2.
    """
    man = read_json(root / 'manifest.json')
    if not isinstance(man, dict) or man.get('schema') != SCHEMA:
        out(f'⛔ {root}/manifest.json 이 없거나 스키마가 다르다 — 이 실행기가 만든 ROOT 가 아니다')
        return 2
    el = launch_eligibility(man)
    if el['kind'] == 'invalid' or (el['kind'] == 'historical' and not historical):
        out('⛔ merge 거부 — 실행 형식 자격 (G2RR2-01): ' + ('; '.join(el['problems'][:6]) if el['kind'] == 'invalid' else
                                                         f'역사 형식 ROOT ({el["historical"]}) — 역사 모드 (--historical) 로만 다시 묶는다'))
        return 2
    history = el['kind'] == 'historical'
    git_sha = (man.get('git') or {}).get('sha') or ''
    structural, mixed, anomalies, failures = [], [], [], []
    unsealed, dirty_ok, seal_cnt = [], [], collections.Counter()
    seal = seal_context(man)
    tmp_root = root / '.merged_tmp'
    if tmp_root.exists():
        shutil.rmtree(tmp_root)
    #  지금 트리 (워커 체크아웃) 가 봉인과 다른지 = 정보 — 판정은 시도별 증거로 (끝난 뒤 트리만 바뀐 배치를 기각하지 않는다 · Codex 4차 §3)
    report = dict(schema=SCHEMA + '#merge', merged_at=now_iso(), git_sha=git_sha, cohorts={},
                  code_changed_since_launch=seal_diff(_hashes_at(seal['root']), seal['hashes']),
                  **{GEN_KEY: man.get(GEN_KEY)},        # ★ 10-07 — 정보 (세대 대조 = audit · 인계 --tau-batch-manifest)
                  eligibility=dict(kind=el['kind'], historical=el['historical'], note=el['note']))
    runs_by_no = _runs_by_no(root)
    #  실행 중 코드 변화 (run 의 h0 ≠ h1) = 정보.  옛 형식 시도는 case_seal 이 run_001 의 이 기록으로 판정하고, 새 형식 시도는 시도별 지문으로
    #   가른다 (그 실행 안에서 어느 케이스가 바뀐 코드로 돌았는지) — 옛 판은 이것 하나로 배치 전체를 영원히 거부했다 (다시 돌려도 안 풀렸다).
    report['runs_code_changed_during'] = {str(k): v.get('code_changed_during_run') for k, v in sorted(runs_by_no.items())
                                          if v.get('code_changed_during_run')}
    for cs in man['plan']['cohorts']:
        name = cs['name']
        cases = sorted(e['case'] for e in man['plan']['queue'] if e['cohort'] == name)
        md = tmp_root / name
        (md / 'results').mkdir(parents=True)
        status = dict(schema=LWB.SCHEMA, cases={}, stop_after=STOP, harvest_dir=cs['harvest_dir'], cohort=cs['cohort'], runs=[])
        rows, tsv = {}, []
        cnt = collections.Counter()
        for c in cases:
            cdir = case_dir(root, c)
            wrec = read_json(cdir / 'worker.json')
            st = read_json(cdir / 'out' / 'status.json')
            rec = None
            if isinstance(st, dict):
                if st.get('schema') != LWB.SCHEMA:
                    structural.append(f'{c}: out/status.json schema {st.get("schema")!r} ≠ {LWB.SCHEMA}')
                if st.get('stop_after') != STOP:
                    structural.append(f'{c}: out/status.json stop_after {st.get("stop_after")!r} ≠ {STOP!r}')
                if str(st.get('harvest_dir')) != cs['harvest_dir'] or str(st.get('cohort')) != cs['cohort']:
                    structural.append(f'{c}: 수확 · 코호트 경로가 계획과 다르다 ({st.get("harvest_dir")} · {st.get("cohort")})')
                foreign = sorted(set(st.get('cases') or {}) - {c})
                if foreign:
                    structural.append(f'{c}: 케이스 폴더의 status.json 에 다른 케이스 기록 {foreign} — 두 번 셀 수 있다')
                rec = (st.get('cases') or {}).get(c)
                for r in st.get('runs') or []:
                    r2 = dict(r)
                    r2['case'] = c
                    status['runs'].append(r2)
                    if git_sha and r.get('git_sha') != git_sha:
                        mixed.append(f'{c}: 워커 코드 {str(r.get("git_sha"))[:9]} ≠ 발사 코드 {git_sha[:9]}')
            elif (cdir / 'out' / 'status.json').exists():
                anomalies.append(f'{c}: out/status.json 을 읽을 수 없다 (깨짐)')
            #  RGLR3-01 ⓒ — 이 기록을 쓴 시도가 발사 봉인 코드였나 (기록 없음 = NO_RECORD → 아래에서 failed 로 합성)
            sv = case_seal(root, man, c, runs_by_no, history=history)
            seal_cnt[sv['verdict']] += 1
            if sv['verdict'] == 'UNSEALED':
                unsealed.append(f'{c}: {sv["why"]}')
            elif sv['verdict'] == 'SEALED_DIRTY_ALLOWED':
                dirty_ok.append(c)
            if rec is None:
                why0 = '발사되지 않았다 (중단 · 예산 대기 · 봉인 관문으로 끝남)' if not wrec else ''
                rec = _synth_failed(c, cdir, wrec, why0)
                anomalies.append(f'{c}: 케이스 기록 없음 → failed 로 기록 ({rec["why"][:120]})')
            status['cases'][c] = rec
            s = rec.get('status') or 'UNKNOWN'
            cnt[s] += 1
            att = ((wrec or {}).get('attempts') or [None])[-1] or {}
            if att and s in KEEP and att.get('rc') not in (0, None):
                anomalies.append(f'{c}: 케이스는 {s} 인데 워커 rc {att.get("rc")} — 기록 뒤에 죽었다 (값은 기록 그대로)')
            if s not in KEEP:
                failures.append(dict(case=c, cohort=name, status=s, why=(rec.get('why') or '')[:300],
                                     failed_stages=rec.get('failed_stages') or []))
            mf = cdir / 'out' / 'metrics_flat.csv'
            if mf.exists():
                with open(mf, encoding='utf-8', newline='') as fh:
                    rr = list(csv.DictReader(fh))
                if len(rr) > 1 or any(r.get('case') != c for r in rr):
                    structural.append(f'{c}: out/metrics_flat.csv 에 다른 행 {[r.get("case") for r in rr]}')
                elif rr:
                    rows[c] = dict(rr[0])          # 빈 칸 ('') 도 그대로 — 머리 열 집합이 순차 배치와 같게 (selftest ⑧)
            #  τ 관문용 링크 — 결과가 없는 케이스도 빈 폴더 (tau_flux 가 NOT_COMPUTED 행을 낸다 · 빠지지 않는다)
            src = cdir / 'work' / 'results' / c
            dst = md / 'results' / c
            if src.is_dir():
                os.symlink(os.path.relpath(src, md / 'results'), dst)
            else:
                dst.mkdir()
                (dst / '_NO_RESULTS.txt').write_text(f'{c}: 케이스 결과 폴더가 없다 ({src}) — 상태 {s}\n', encoding='utf-8')
            tsv.append((c, name, s, '|'.join(map(str, rec.get('failed_stages') or [])), rec.get('network_run_id') or '',
                        len((wrec or {}).get('attempts') or []), att.get('rc', ''), att.get('signal') or '', att.get('wall_s', ''),
                        rec.get('elapsed_s', ''), att.get('peak_rss_mb', ''), att.get('est_mem_mb', ''), att.get('user_s', ''),
                        att.get('sys_s', ''), att.get('contacts', ''), str(cdir / 'log.txt'), sv['verdict'],
                        sv.get('attempt') if sv.get('attempt') is not None else ''))
        status['parallel'] = dict(launcher=SCHEMA, manifest=str(root / 'manifest.json'), git_sha=git_sha,
                                  lanes=man.get('lanes'), network_lock=man.get('network_lock'), thread_env=THREAD_ENV,
                                  merged_at=report['merged_at'], n_cases=len(cases), counts=dict(cnt), seal_fp=seal['fp'],
                                  seal_verdicts=dict(collections.Counter(t[16] for t in tsv)))
        LWB.write_outputs(md, status, rows)                     # 배치 자신의 writer (같은 직렬화 · 같은 열 규칙)
        with open(md / 'parallel_cases.tsv', 'w', encoding='utf-8', newline='') as fh:
            w = csv.writer(fh, delimiter='\t', lineterminator='\n')
            w.writerow(('case', 'cohort', 'status', 'failed_stages', 'network_run_id', 'attempts', 'rc', 'signal', 'wall_s',
                        'batch_elapsed_s', 'peak_rss_mb', 'est_mem_mb', 'user_s', 'sys_s', 'contacts', 'log', 'seal', 'seal_attempt'))
            w.writerows(tsv)
        walls = sorted(float(t[8]) for t in tsv if t[8] not in ('', None))
        rss = sorted(float(t[10]) for t in tsv if t[10] not in ('', None))
        ratio = sorted(float(t[10]) / float(t[11]) for t in tsv if t[10] not in ('', None) and t[11] not in ('', None, 0))

        def q(v, f):
            return round(v[min(len(v) - 1, int(f * len(v)))], 1) if v else None
        report['cohorts'][name] = dict(n=len(cases), counts=dict(cnt), n_rows=len(rows), wall_s=dict(median=q(walls, .5), p90=q(walls, .9),
                                       max=(walls[-1] if walls else None), sum=round(sum(walls), 1)),
                                       peak_rss_mb=dict(median=q(rss, .5), max=(rss[-1] if rss else None)),
                                       rss_over_est=dict(median=(round(q(ratio, .5), 3) if ratio else None),
                                                         max=(round(ratio[-1], 3) if ratio else None)))
    report.update(structural=structural, mixed_generation=mixed, anomalies=anomalies, failures=failures,
                  seal=dict(schema=LAUNCH_SEAL_SCHEMA, fp=seal['fp'], code_root=str(seal['root']), launch_sha=seal['sha'],
                            verdicts=dict(seal_cnt), unsealed=unsealed, dirty_allowed=dirty_ok,
                            rule='case_seal — 지금 기록을 쓴 시도의 시작 · 끝 지문 = 발사 지문 · git sha = 발사 · dirty 는 기록된 --allow-dirty 만 · '
                                 '옛 형식은 첫 run 의 유일한 시도만 (run_001 실행 중 변화 0 · 깨끗한 사전 점검 · 워커 runs 1 건)'))
    if structural or ((mixed or unsealed) and not allow_mixed):
        shutil.rmtree(tmp_root, ignore_errors=True)
        write_json(root / 'merge_report_REFUSED.json', report)
        out('⛔ merge 거부 — merged/ 를 바꾸지 않았다 (merge_report_REFUSED.json)')
        for s in structural[:20]:
            out(f'   구조: {s}')
        for s in mixed[:20]:
            out(f'   세대: {s}' + ('' if allow_mixed else '  (진짜 의도면 --allow-mixed-generation · 기록된다)'))
        for s in unsealed[:20]:
            out(f'   발사 봉인 밖: {s}')
        if unsealed and not allow_mixed:
            out(f'   ⇒ 봉인 밖 기록 {len(unsealed)} 건 — 워커 체크아웃 {seal["root"]} 을 발사 코드 ({seal["sha"][:9]}) 로 둔 채 retry 가 그 케이스만 '
                '--force 로 다시 돌린다 (audit 로 확인 · 알고도 묶으려면 --allow-mixed-generation · 기록된다)')
        return 2
    report['allow_mixed_generation'] = bool(allow_mixed and (mixed or unsealed))
    write_json(tmp_root / 'merge_report.json', report)
    final = root / 'merged'
    if final.exists():
        shutil.rmtree(final)
    os.replace(tmp_root, final)
    with contextlib.suppress(FileNotFoundError):
        (root / 'merge_report_REFUSED.json').unlink()
    print_merge_summary(root, report, man, out=out)
    return 0 if not failures and not anomalies and not mixed and not unsealed else 1


def print_merge_summary(root: Path, report: dict, man: dict, out=print):
    out(f'══ merge — {root / "merged"}')
    for name, r in report['cohorts'].items():
        out(f'  {name}: {r["n"]} 건 {r["counts"]} · 행 {r["n_rows"]} · 경과 중앙 {r["wall_s"]["median"]} s · p90 {r["wall_s"]["p90"]} s · '
            f'최대 {r["wall_s"]["max"]} s · 합 {r["wall_s"]["sum"]} s · 최대 RSS 중앙 {r["peak_rss_mb"]["median"]} MB · '
            f'최대 {r["peak_rss_mb"]["max"]} MB · 실측/추정 중앙 {r["rss_over_est"]["median"]} · 최대 {r["rss_over_est"]["max"]}')
    mi = meminfo()
    mx = max((r['peak_rss_mb']['max'] or 0) for r in report['cohorts'].values()) if report['cohorts'] else 0
    if mx and mi.get('MemTotal'):
        k = int(max(1, (mi['MemTotal'] / 2 ** 20 - 2048) // (mx + 100)))
        out(f'  메모리로 본 동시 상한 ≈ {k} 레인 (MemTotal {gib(mi["MemTotal"])} GB − 2 GB · 최대 케이스 {mx:.0f} MB + 부모 100 MB 가정)')
    for f in report['failures'][:40]:
        out(f'  ✗ {f["case"]} ({f["cohort"]}) {f["status"]} · {f["failed_stages"]} · {f["why"][:160]}')
    for a in report['anomalies'][:40]:
        out(f'  ⚠ {a}')
    for m in report['mixed_generation'][:10]:
        out(f'  ⚠ 세대: {m}')
    sl = report.get('seal') or {}
    out(f'  발사 봉인 (RGLR3-01) — 지문 {str(sl.get("fp") or "없음")[:12]} · 판정 {sl.get("verdicts")}'
        + (f' · ⚠ 봉인 밖 {len(sl.get("unsealed") or [])} 건 (--allow-mixed-generation 으로 묶음)' if sl.get('unsealed') else ''))
    for u in (sl.get('unsealed') or [])[:20]:
        out(f'  ⚠ 봉인 밖: {u}')
    if sl.get('dirty_allowed'):
        out(f'  ⚠ dirty 트리에서 돈 케이스 {len(sl["dirty_allowed"])} 건 — 그 실행의 --allow-dirty 로 기록됨 (지문은 봉인과 같다): '
            f'{sl["dirty_allowed"][:10]}')
    if report.get('runs_code_changed_during'):
        out(f'  ⚠ 실행 중 코드가 바뀐 실행 (정보 — 판정은 시도별 지문): {report["runs_code_changed_during"]}')
    if report['code_changed_since_launch']:
        out(f'  ⚠ 지금 워커 체크아웃이 발사 봉인과 다른 파일 (정보 — 판정은 기록된 시도 증거로): {report["code_changed_since_launch"]}')
    print_followups(root, man, out=out)


def print_followups(root: Path, man: dict, out=print):
    """후속 명령 — ⓪ 봉인 감사 · ① τ 진단 표 · ②a 완료 압력 기록 (DESC-06) · ② 인계 생성기 한 번 (τ 묶음 + --tau-results · RGLR3-03 ·
    --pressure-record) · ③ 포장."""
    q = shlex.quote
    sha = ((man.get('git') or {}).get('short')) or 'SHA'
    d = time.strftime('%Y%m%d')
    names = [c['name'] for c in man['plan']['cohorts']]
    by = {c['name']: c for c in man['plan']['cohorts']}
    #  ★ 10-07 G2RR-01 — manifest 가 기대 망 세대를 선언했으면 인계 생성기가 그 값과 케이스마다 교차 대조한다 (--tau-batch-manifest) · 세대 2 = 인계 v1.3
    declared = man.get(GEN_KEY)
    ver = 'v13' if declared == 'g2' else 'v12'
    tbm = f' --tau-batch-manifest {q(str(root / "manifest.json"))}' if declared else ''
    out('━━ 다음 명령 (리포 루트에서 · 그대로 복사) ━━')
    out(f'cd {q(str(ROOT))}')
    tf = 'scripts/tau_flux.py'
    same = (code_hashes() or {}).get(tf) == (man.get('code_hashes') or {}).get(tf)
    out(f'# 인계 생성기 · τ 관문은 이 체크아웃의 것을 쓴다 — {tf} 지문 = 발사 봉인 '
        + ('✓ 같다' if same else '✗ 다르다 (τ 관문이 봉인 밖 코드 — 발사 체크아웃에서 돌릴 것)'))
    if man.get('handover_code_hashes'):
        _hd = [rel for rel, h in (man.get('handover_code_hashes') or {}).items() if sha256_file(ROOT / rel) != h]
        out('# 인계 생성기 · 다시 읽기 도구 지문 = 발사 기록 (handover_code_hashes) ' + ('✓ 같다' if not _hd else f'✗ 다르다 {_hd} — 발사 커밋의 도구로 돌릴 것'))
    out(f'mkdir -p {q(str(root / "tau"))} {q(str(root / "handover"))} {q(str(root / "pressure"))}')
    out('# ⓪ 봉인 감사 (RGLR3-01 · 기대 망 세대 G2RR-01) — 케이스마다 어느 코드 · 세대로 계산됐나 (시도별 지문 · 옛 형식은 첫 run 규칙).  '
        'UNSEALED · 세대 문제가 있으면 인계하지 않는다 (retry)')
    out(f'python3 scripts/run_network_194_parallel.py audit --root {q(str(root))} --tsv {q(str(root / "seal_audit.tsv"))} '
        f'--json {q(str(root / "seal_audit.json"))}')
    if declared:
        out('# ⓪b 게시 다시 읽기 (Codex 세대 2 재검증 §7 끝 — 전체 상태 · ID · 증서 · 도장 · 열 역할 · 인계 출처 관문 · 읽기 전용) — rc 0 이 아니면 인계하지 않는다')
        out(f'python3 scripts/g2_network_reread.py --launcher-root {q(str(root))} --json {q(str(root / "reread.json"))}')
    out('# ① τ 관문 진단 표 — 모든 케이스 폴더 (실패 케이스도 NOT_COMPUTED 행).  진단 전용: 인계표에 손으로 잇지 않는다 (인계 τ = ② 의 --tau-results 경로)')
    for n in names:
        out(f'python3 scripts/tau_flux.py {q(str(root / "merged" / n / "results"))}/* '
            f'--tsv {q(str(root / "tau" / f"{n}_tau_flux.tsv"))} --json {q(str(root / "tau" / f"{n}_tau_flux.json"))}')
    out('# ②a 완료 압력 기록 (DESC-06 · 10-06) — 침대마다 LIGGGHTS 로그의 압밀 루프 판정 줄 (마지막 줄 current ≥ 목표) · 덱 sha = 수확 raw.deck.')
    out('#    로그가 덱 폴더의 log* 가 아니면 --log-glob 으로 (rc 1 = OK 아닌 침대가 있다 — 그 침대가 있으면 ② 생성기가 거부한다)')
    rmap = (f' --root-from {q(man.get("root_from"))} --root-to {q(man.get("root_to") or "")}' if man.get('root_from') else '')
    for n in names:
        c = by[n]
        out(f'python3 scripts/lhs_pressure_record.py --cohort {q(c["cohort"])} --harvest-dir {q(c["harvest_dir"])}{rmap} '
            f'--out {q(str(root / "pressure" / f"{n}_pressure_record.tsv"))}')
    out(f'# ② 인계 {ver[0]}{ver[1]}.{ver[2]} — 생성기 한 번 (망 배치 묶음 {HANDOVER_GROUPS} · RGL-03 · RGLR3-03).  τ 열 (f · f_gap · tau2 · tau · 상태 · 사유 · 메타) 은')
    out('#    --tau-results 의 출처 관문 P0–P4 (배치 status.json run id · 입력 digest · metrics_flat 세대 · 정지 계약 재검사 · 도장 ↔ 레코드) 를 지난 값만 표 끝에 싣는다 ·'
        + (' --tau-batch-manifest = manifest 기대 망 세대와 케이스마다 교차 대조 (G2RR-01) ·' if declared else ''))
    out('#    열 사전 <표>_columns.tsv · τ 출처 부록 <표>_tau_provenance.tsv · 제외 노트 <표>_excluded.tsv (LW ④b = frame_unverified 명시 제외).')
    for n in names:
        c = by[n]
        extra = (f' --design {q(c["design"])}' if c.get('design') else '')
        out(f'python3 scripts/lhs_design_dataset.py --export-handover {q(str(root / "handover" / f"{n}_handover_{ver}_{d}.csv"))}'
            f'{extra} --harvest {q(c["harvest_dir"])} --union {q(c.get("union") or "")} '
            f'--webapp {q(str(root / "merged" / n))} --webapp-groups {HANDOVER_GROUPS} --tau-results {q(str(root / "merged" / n / "results"))}'
            f'{tbm} --pressure-record {q(str(root / "pressure" / f"{n}_pressure_record.tsv"))}')
    hand = ' '.join(f'handover/{n}_handover_{ver}_{d}{suf}' for n in names
                    for suf in ('.csv', '_columns.tsv', '_tau_provenance.tsv', '_excluded.tsv'))
    out('# ③ 보낼 묶음 — 인계표 · 열 사전 · τ 출처 부록 · 제외 노트 · 봉인 감사 · manifest · 실행 · 시도 기록 (케이스 결과 원본 · 작업 폴더는 빼고)')
    out(f'(cd {q(str(root))} && tar czf ~/net194_{sha}_{d}.tar.gz manifest.json runs progress.tsv seal_audit.tsv merged/merge_report.json '
        + ('seal_audit.json reread.json ' if declared else '')
        + f'merged/*/status.json merged/*/metrics_flat.csv merged/*/parallel_cases.tsv tau pressure {hand} cases/*/worker.json cases/*/log.txt)')
    out('# ③b (선택 · 받는 쪽 독립 재검증용) τ 원천 canonical 파일 — 출처 부록의 sha256 을 다시 잴 수 있게 (dual · full_metrics · 망 도장)')
    out(f'(cd {q(str(root))} && tar czf ~/net194_{sha}_{d}_tau_sources.tar.gz cases/*/work/results/*/network_conductivity_dual.json '
        'cases/*/work/results/*/full_metrics.json cases/*/work/results/*/network_provenance.json)')


# ─────────────────────────────────── 명령 ───────────────────────────────────
def _guard_posix():
    if os.name != 'posix' or not hasattr(os, 'wait4'):
        raise LaunchError('이 실행기는 Linux/WSL 전용이다 (os.wait4 · 프로세스 묶음)')


def cmd_run(args) -> int:
    _guard_posix()
    root = Path(args.root).expanduser().resolve()
    if root.exists() and any(root.iterdir()):
        print(f'⛔ ROOT {root} 가 비어 있지 않다 — 새 ROOT 를 쓸 것 (이어서 돌리려면 retry · 다시 묶으려면 merge)', file=sys.stderr)
        return 2
    worker = Path(args.worker_script).resolve() if args.worker_script else BATCH
    plan = build_plan(args.cohorts.split(','), cohort_specs(args), args.case, args.order)
    mi = meminfo()
    if args.mem_budget_gb is None:
        budget_mb = (max(1.0, mi['MemAvailable'] / 2 ** 20 - args.mem_reserve_gb * 1024) if mi.get('MemAvailable') else None)
    else:
        budget_mb = args.mem_budget_gb * 1024 if args.mem_budget_gb > 0 else None
    pf = preflight(args, plan, root, budget_mb)
    print_preflight(pf, plan, args, root)
    q = plan['queue']
    print(f'══ 계획 — {len(q)} 건 · 순서 {plan["order"]} (접촉 수 큰 순 · 같으면 이름) · 레인 {args.lanes}')
    for i, e in enumerate(q[:5] + (q[-2:] if len(q) > 7 else [])):
        print(f'  {e["case"]:>10s} ({e["cohort"]}) 접촉 {e["contacts"]:>7d} · 추정 {e["est_mem_mb"]:.0f} MB · {e["est_time_s"]:.0f} s')
    cs0 = {c['name']: c for c in plan['cohorts']}
    ex = q[0]
    print('  케이스 명령 예:', shlex.join(case_cmd(args.python, worker, cs0[ex['cohort']], ex['case'], case_dir(root, ex['case']),
                                                args.root_from, args.root_to)))
    print(f'  cwd = 케이스 폴더 · env + {THREAD_ENV} · PYTHONDONTWRITEBYTECODE=1'
          + (' · TMPDIR = <케이스>/tmp' if args.network_lock == 'per-case' else ''))
    if worker != BATCH:
        print(f'  ⚠ 워커 대체 (시험용) — {worker}')
    if pf['stop']:
        print('⛔ 사전 점검 중단 — 위 ⛔ 를 해결할 것 (아무것도 띄우지 않았다)', file=sys.stderr)
        return 2
    n_pyc = purge_pyc(ROOT / 'scripts', dry=args.dry_run)
    if args.dry_run:
        print(f'══ --dry-run — 아무것도 쓰지 않았다 (scripts/__pycache__ pyc {n_pyc} 개는 본 실행 때 지운다)')
        return 0
    if not args.skip_batch_selftest:
        r = subprocess.run([str(args.python), str(BATCH), '--selftest'], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
        if r.returncode != 0:
            print('⛔ lhs_webapp_batch --selftest 실패 — 띄우지 않는다\n' + (r.stdout or '')[-2000:], file=sys.stderr)
            return 2
        print('  lhs_webapp_batch --selftest 통과')
    root.mkdir(parents=True, exist_ok=True)
    with root_lock(root):
        hashes = code_hashes()
        gen = pf['generation']['generation']                     # ★ 10-07 G2RR-01 — 봉인 코드에서 유도 (사전 점검이 g2 · 문제 0 을 확인했다)
        man = dict(schema=SCHEMA, launch_format=LAUNCH_FORMAT, created=now_iso(), argv=sys.argv, repo_root=str(ROOT), python=str(args.python),
                   python_versions=python_versions(args.python), worker_script=str(worker), worker_override=(worker != BATCH),
                   stop_after=STOP, lanes=args.lanes, network_lock=args.network_lock, thread_env=THREAD_ENV,
                   mem_budget_mb=budget_mb, mem_reserve_gb=args.mem_reserve_gb, min_free_gb=args.min_free_gb,
                   mem_model=dict(base_mb=MEM_BASE_MB, per_kcontact_mb=MEM_PER_KCONTACT_MB, time_per_kcontact_s=TIME_PER_KCONTACT_S),
                   root_from=args.root_from, root_to=args.root_to, allow_dirty=args.allow_dirty,
                   observe_imports=bool(args.observe_imports),
                   allow_missing_raw=args.allow_missing_raw, pyc_purged=n_pyc, git=pf['git'], code_hashes=hashes,
                   **{GEN_KEY: gen}, generation_probe=pf['generation'], code_dependency_closure=pf['dependency_closure']['files'],
                   handover_code_hashes={rel: sha256_file(ROOT / rel) for rel in HANDOVER_FILES}, input_digest=pf['input_digest'],
                   seal=dict(schema=LAUNCH_SEAL_SCHEMA, launch_format=LAUNCH_FORMAT, code_fp=code_fp(hashes), code_root=str(ROOT), files=len(hashes),
                             dirty=bool(pf['git'].get('dirty')), allow_dirty=bool(args.allow_dirty), **{GEN_KEY: gen}),
                   preflight={k: v for k, v in pf.items() if k not in ('git', 'generation', 'dependency_closure', 'input_digest')}, plan=plan,
                   retries=[])
        #  ★ 10-07 G2RR2-01 — 쓰기 전에 같은 자격 검사 (run · retry · audit · merge 가 쓰는 함수) 로 자기 대조 — 새 형식 필수 선언이 하나라도 빠진 manifest 로는
        #    발사하지 않는다 (실행기 결함이면 여기서 멈춘다)
        _el = launch_eligibility(json.loads(json.dumps(man, ensure_ascii=False)))
        if _el['kind'] != 'current':
            print(f'⛔ 발사 manifest 가 자기 자격 검사를 통과하지 않는다 (G2RR2-01) — {_el["problems"][:5]} · 아무것도 띄우지 않았다', file=sys.stderr)
            return 2
        write_json(root / 'manifest.json', man)
        rc = _run_and_merge(root, man, plan['queue'], args.lanes, budget_mb, args.min_free_gb, args.no_merge, run_label='run',
                            allow_dirty=args.allow_dirty)
    return rc


def _run_and_merge(root, man, todo, lanes, budget_mb, min_free_gb, no_merge, run_label, allow_mixed=False, allow_dirty=False) -> int:
    run_no = len(list((root / 'runs').glob('run_*.json'))) + 1
    seal = seal_context(man, dirty_allowed=allow_dirty, mixed_allowed=allow_mixed)
    h0 = _hashes_at(seal['root'])
    t0 = now_iso()
    res = run_queue(root, man, todo, lanes, run_no, budget_mb=budget_mb, min_free_gb=min_free_gb, seal=seal)
    h1 = _hashes_at(seal['root'])
    res.update(kind=run_label, started=t0, ended=now_iso(), lanes=lanes, mem_budget_mb=budget_mb, min_free_gb=min_free_gb,
               code_changed_during_run=sorted(k for k in h1 if h1[k] != h0.get(k)), git_sha_end=_git_at(seal['root']).get('sha'),
               seal_fp=seal['fp'], code_fp_start=code_fp(h0), code_fp_end=code_fp(h1),
               code_changed_vs_seal_start=seal_diff(h0, seal['hashes']), code_root=str(seal['root']),
               dirty_allowed=bool(allow_dirty), mixed_allowed=bool(allow_mixed))
    write_json(root / 'runs' / f'run_{run_no:03d}.json', res)
    print(f'══ 실행 {run_no} 끝 — {res.get("outcomes")} · {res.get("wall_h")} h · 최대 동시 {res.get("max_concurrent")} · '
          f'예산 대기 {res.get("budget_events")} · backfill {res.get("backfills")} · 메모리 바닥 대기 {res.get("events")}'
          + (' · ⛔ 중단됨' if res.get('interrupted') else '') + (' · ⛔ 발사 봉인 관문으로 입장 멈춤' if res.get('seal_broken') else ''))
    if res['code_changed_during_run']:
        print(f'⚠ 실행 중 코드 파일이 바뀌었다: {res["code_changed_during_run"]} — 어느 케이스가 바뀐 코드로 돌았는지는 시도별 지문이 가른다 '
              '(merge · audit 판정 UNSEALED)')
    if res.get('seal_broken'):
        print(f'⛔ 발사 봉인 관문 — {res["seal_broken"][0]["why"]} · 띄우지 않은 케이스 {len(res.get("not_started") or [])} 건 — 자동 merge 하지 않는다.  '
              f'워커 체크아웃 {seal["root"]} 을 발사 코드로 되돌린 뒤 retry (audit 로 봉인 밖 케이스 확인)')
        return 2
    if no_merge or res.get('interrupted'):
        if res.get('interrupted'):
            print('  중단된 실행은 자동 merge 하지 않는다 — retry 로 마저 돌리거나 merge 로 지금 상태를 묶는다')
        return 130 if res.get('interrupted') else (0 if all(k in KEEP for k in (res.get('outcomes') or {})) else 1)
    return merge(root, allow_mixed=allow_mixed)


def _load_root(root: Path) -> dict:
    man = read_json(root / 'manifest.json')
    if not isinstance(man, dict) or man.get('schema') != SCHEMA:
        raise LaunchError(f'{root}/manifest.json 이 없거나 이 실행기의 것이 아니다')
    return man


def retry_todo(root: Path, man: dict, want=(), force_unsealed=True):
    """retry 대상 → (todo, forced, skip).  done · partial 아닌 케이스 + (force_unsealed) done · partial 이지만 봉인 밖 (UNSEALED) 기록 —
    후자는 `--force` 로 다시 돌린다 (입증 못 한 케이스만 · 봉인된 케이스는 그대로).  아직 도는 워커는 건너뛴다."""
    want = set(want or ())
    runs_by_no = _runs_by_no(root)
    todo, forced, skip = [], [], []
    for e in man['plan']['queue']:
        if want and e['case'] not in want:
            continue
        cdir = case_dir(root, e['case'])
        pidrec = read_json(cdir / 'worker.pid.json')
        if pidrec and pid_alive(pidrec.get('pid'), e['case']):
            skip.append((e['case'], f'아직 도는 워커 pid {pidrec.get("pid")}'))
            continue
        s, _rec = _case_outcome(cdir, e['case'])
        if s in KEEP:
            if not force_unsealed:
                continue
            sv = case_seal(root, man, e['case'], runs_by_no)
            if sv['verdict'] in SEAL_OK:
                continue
            todo.append(dict(e, force=True))
            forced.append((e['case'], sv['why']))
            continue
        todo.append(e)
    return todo, forced, skip


def cmd_retry(args) -> int:
    _guard_posix()
    root = Path(args.root).expanduser().resolve()
    man = _load_root(root)
    #  ★ 10-07 G2RR2-01 — 실행 형식 자격 먼저 (run · audit · merge 와 같은 함수) — 역사 형식 · 선언을 지운 manifest 는 retry 하지 않는다 (넘김 불가)
    el = launch_eligibility(man)
    if el['kind'] != 'current':
        print('⛔ retry 거부 — 실행 형식 자격 (G2RR2-01) · 아무것도 띄우지 않았다 · 아무 파일도 쓰지 않았다', file=sys.stderr)
        for p in ([f'역사 형식 ROOT ({el["historical"]}) — 이 실행기로 retry 하지 않는다 (그 ROOT 의 커밋 실행기로 · 넘김 불가)']
                  if el['kind'] == 'historical' else el['problems'][:10]):
            print(f'   형식: {p}', file=sys.stderr)
        return 2
    #  RGLR3-01 ⓐ — 시작 관문: 워커 체크아웃의 HEAD · 봉인 파일 해시 · dirty · 기대 망 세대 를 발사 봉인과 대조 (같은 HEAD 여도 코드가 다르면 거부)
    gate = seal_gate(man)
    g = gate['git']
    blocked = bool(gate['generation_bad'] or (gate['mixed'] and not args.allow_mixed_generation) or (gate['dirty'] and not args.allow_dirty))
    if blocked:
        print('⛔ retry 거부 — 발사 봉인과 대조 (RGLR3-01 · 기대 망 세대 G2RR-01) · 아무것도 띄우지 않았다 · 아무 파일도 쓰지 않았다', file=sys.stderr)
        for p in gate['generation_bad']:
            print(f'   기대 망 세대: {p}  (넘김 없음 — 다른 세대로 계산한 기록은 인계 (--tau-batch-manifest) 가 거부한다)', file=sys.stderr)
        for p in gate['mixed']:
            print(f'   세대: {p}' + ('' if args.allow_mixed_generation else '  (진짜 의도면 --allow-mixed-generation · 기록된다 · merge 는 봉인 밖으로 표시)'),
                  file=sys.stderr)
        for p in gate['dirty']:
            print(f'   dirty: {p}' + ('' if args.allow_dirty else '  (진짜 의도면 --allow-dirty · 기록된다 · 코드 해시는 봉인과 같아야 한다)'),
                  file=sys.stderr)
        return 2
    for p in gate['mixed'] + gate['dirty']:
        print(f'⚠ 넘김 (기록된다): {p}')
    if gate.get('generation_note'):
        print(f'  ⓘ {gate["generation_note"]}')
    else:
        print(f'  기대 망 세대 {man.get(GEN_KEY)!r} = 봉인 사본 = 워커 체크아웃 코드가 지금 내는 세대 (다시 유도)')
    #  봉인 밖 done · partial 을 --force 로 다시 — 지금 코드가 봉인과 같을 때만 (아니면 다시 돌려도 또 봉인 밖이다)
    todo, forced, skip = retry_todo(root, man, args.case, force_unsealed=not gate['mixed'])
    for c, why in skip:
        print(f'  건너뜀 {c}: {why}')
    for c, why in forced:
        print(f'  봉인 밖 기록 → --force 로 다시: {c} — {why[:200]}')
    print(f'══ retry — 다시 돌릴 케이스 {len(todo)} 건 (done · partial 아닌 것 + 봉인 밖 기록 {len(forced)}) · 레인 {args.lanes}')
    if not todo:
        return merge(root, allow_mixed=args.allow_mixed_generation) if not args.no_merge else 0
    mi = meminfo()
    if args.mem_budget_gb is None:
        budget_mb = (max(1.0, mi['MemAvailable'] / 2 ** 20 - args.mem_reserve_gb * 1024) if mi.get('MemAvailable') else None)
    else:
        budget_mb = args.mem_budget_gb * 1024 if args.mem_budget_gb > 0 else None
    print(f'  CPU {cpu_info()} · MemAvailable {gib(mi.get("MemAvailable"))} GB · 예산 {budget_mb and round(budget_mb / 1024, 1)} GB')
    purge_pyc(gate['seal']['root'] / 'scripts')
    with root_lock(root):
        man.setdefault('retries', []).append(dict(
            at=now_iso(), argv=sys.argv, lanes=args.lanes, cases=[e['case'] for e in todo], forced=[c for c, _ in forced],
            git_sha=g.get('sha'), dirty=bool(g.get('dirty')), porcelain=list(g.get('porcelain') or [])[:10], code_root=str(gate['seal']['root']),
            code_fp=gate['fp'], seal_fp=gate['seal']['fp'], code_changed_vs_seal=gate['changed'],
            allow_dirty=bool(args.allow_dirty), allow_mixed_generation=bool(args.allow_mixed_generation),
            seal_overrides=gate['mixed'] + gate['dirty'], expected_network_generation=man.get(GEN_KEY),
            generation_note=gate.get('generation_note') or ''))
        write_json(root / 'manifest.json', man)
        rc = _run_and_merge(root, man, todo, args.lanes, budget_mb, args.min_free_gb, args.no_merge, run_label='retry',
                            allow_mixed=args.allow_mixed_generation, allow_dirty=args.allow_dirty)
    return rc


def seal_audit(root: Path, man: dict, history=False) -> list:
    """케이스마다 case_seal 판정 + merged 기록이 케이스 폴더 기록과 같은가 (읽기 전용).
    ★ 10-07 G2RR-01 · G2RR2-01 — 새 실행 형식 (자격 current) 이면 done · partial 케이스마다 레코드 세대 (`case_record_generation`) 를 싣는다 · 역사 형식 (history) = None ·
    옛 형식 시도 판정은 history 일 때만."""
    runs_by_no = _runs_by_no(root)
    declared = not history
    merged = {}
    out = []
    for e in sorted(man['plan']['queue'], key=lambda x: (x['cohort'], x['case'])):
        sv = dict(case_seal(root, man, e['case'], runs_by_no, history=history), cohort=e['cohort'])
        sv['generation'] = case_record_generation(root, e['case']) if declared and sv.get('record_status') in KEEP else None
        if e['cohort'] not in merged:
            merged[e['cohort']] = read_json(root / 'merged' / e['cohort'] / 'status.json')
        ms = merged[e['cohort']]
        mrec = ((ms.get('cases') or {}).get(e['case'])) if isinstance(ms, dict) else None
        if not isinstance(ms, dict):
            sv['merged'] = 'not_merged'
        elif not isinstance(mrec, dict):
            sv['merged'] = 'missing'
        elif sv.get('record_sha') is None:
            sv['merged'] = 'synthesized_failed' if mrec.get('parallel_synthesized') else 'differs'
        else:
            sv['merged'] = 'same' if _rec_sha(mrec) == sv['record_sha'] else 'differs'
        out.append(sv)
    return out


def cmd_audit(args) -> int:
    """봉인 감사 (읽기 전용) — 케이스마다 어느 코드로 계산됐나.  rc 0 = 기록 전부 봉인 안 (SEALED · SEALED_DIRTY_ALLOWED · SEALED_LEGACY) ·
    merged 가 있으면 케이스 폴더 기록과 같다 / 1 = 봉인 밖 (UNSEALED) 또는 merged 와 다름 · 세대 · 입력 지문 문제 / 2 = 이 실행기의 ROOT 가 아님 ·
    ★ 10-07 G2RR2-01 실행 형식 자격 invalid (선언을 지운 새 manifest 등) · 역사 형식인데 --historical 이 아님."""
    root = Path(args.root).expanduser().resolve()
    man = _load_root(root)
    #  ★ 10-07 G2RR2-01 — 실행 형식 자격 (run · retry · merge 와 같은 함수).  invalid = rc 2 (판정표 없음 — 그 manifest 의 봉인은 대조 기준이 못 된다) ·
    #    역사 형식 = --historical 일 때만 (아니면 rc 2)
    el = launch_eligibility(man)
    if el['kind'] == 'invalid' or (el['kind'] == 'historical' and not getattr(args, 'historical', False)):
        why = (el['problems'] if el['kind'] == 'invalid' else
               [f'역사 형식 ROOT ({el["historical"]}) — 역사 모드 (--historical) 에서만 읽는다 · {el["note"]}'])
        print(f'⛔ 봉인 감사 거부 — 실행 형식 자격 {el["kind"]} (G2RR2-01) — {root}')
        for p_ in why[:12]:
            print(f'  ✗ 형식: {p_}')
        if args.json:
            write_json(Path(args.json).expanduser(), dict(schema=LAUNCH_SEAL_SCHEMA + '#audit', root=str(root), audited_at=now_iso(),
                                                          eligibility=dict(kind=el['kind'], historical=el['historical'], problems=why, note=el['note']),
                                                          refused=True))
        return 2
    history = el['kind'] == 'historical'
    seal = seal_context(man)
    rows = seal_audit(root, man, history=history)
    now = _hashes_at(seal['root'])
    cnt = collections.Counter(r['verdict'] for r in rows)
    mcnt = collections.Counter(r['merged'] for r in rows)
    print(f'══ 봉인 감사 — {root}')
    print(f'  실행 형식 자격 {el["kind"]}' + (f' · {el["note"]}' if el['note'] else ' (새 실행 형식 — 필수 선언 전부 · G2RR2-01)'))
    print(f'  발사 git {seal["sha"][:9] or "?"} · 지문 {str(seal["fp"] or "없음 (봉인 불완전)")[:16]} · 워커 체크아웃 {seal["root"]} '
          f'(지금 그 체크아웃 = 봉인 {"✓" if not seal_diff(now, seal["hashes"]) else "✗ " + str(seal_diff(now, seal["hashes"]))} — 정보 · 판정과 무관)')
    print('  case\tcohort\tstatus\tverdict\tattempt(run)\tmerged\twhy')
    for r in rows:
        print(f'  {r["case"]}\t{r["cohort"]}\t{r.get("record_status") or "-"}\t{r["verdict"]}\t'
              f'{r.get("attempt") if r.get("attempt") is not None else "-"}({r.get("run") if r.get("run") is not None else "-"})\t'
              f'{r["merged"]}\t{r["why"][:220]}')
    print(f'  판정 {dict(cnt)} · merged {dict(mcnt)}')
    #  ★ 10-07 G2RR-01 · G2RR2-01 — 기대 망 세대: 새 실행 형식은 선언이 필수 (자격 검사가 값 = 봉인 사본 = g2 를 이미 봤다) · 케이스 레코드 세대 = 선언 ·
    #    역사 형식 = 선언 없는 형식 (세대 대조 안 함 · 표지)
    declared = not history
    gen_problems = []
    if declared:
        gen_problems += [f'{r["case"]}: 레코드 세대 {r["generation"]!r} ≠ manifest 기대 세대 {man.get(GEN_KEY)!r}'
                         for r in rows if r.get('generation') is not None and r['generation'] != man.get(GEN_KEY)]
    gcnt = collections.Counter(r.get('generation') for r in rows if r.get('generation') is not None)
    print(f'  기대 망 세대 ({GEN_KEY}) {man.get(GEN_KEY)!r} · 봉인 사본 {(man.get("seal") or {}).get(GEN_KEY)!r} · 케이스 레코드 세대 {dict(gcnt)}'
          if declared else '  기대 망 세대 — 역사 형식 (선언 없는 형식 · 등록된 옛 실행) — 세대 대조 안 함')
    for p_ in gen_problems[:20]:
        print(f'  ✗ 세대: {p_}')
    #  ★ 10-07 §7-3 — 입력 지문 (ID · 코호트 · 원자료 sha256) 을 지금 수확 JSON 으로 다시 계산해 대조 (새 실행 형식 = 필수 · 역사 형식 = 기록 없음 · 대조 안 함)
    input_problems = []
    if declared:
        now_d = plan_input_digest(man.get('plan') or {})
        input_problems = [f'입력 지문 {k}: 발사 {man["input_digest"].get(k)!r} ≠ 지금 {now_d.get(k)!r}'
                          for k in ('n', 'ids_sha256', 'raw_sha256_table_sha256', 'cohort_tsv_sha256') if man['input_digest'].get(k) != now_d.get(k)]
        print('  입력 지문 (ID · 코호트 · 원자료 sha256) = 발사 기록 ' + ('✓' if not input_problems else '✗'))
        for p_ in input_problems:
            print(f'  ✗ {p_}')
    #  ★ 10-07 G2RR2-03 — 시범의 실제 import 관측 (`run --observe-imports`) — 워커 · 단계 하위 프로세스가 읽은 리포 모듈 ⊆ 봉인 CODE_FILES
    import_obs, obs_problems = None, []
    if man.get('observe_imports') or (root / IMPORT_OBS_DIR / 'log').is_dir():
        import_obs = import_observation(root / IMPORT_OBS_DIR, code_root(man))
        if man.get('observe_imports') and not import_obs['n_processes']:
            obs_problems.append('manifest 는 import 관측을 켰는데 관측 기록이 하나도 없다 (훅이 돌지 않았다)')
        obs_problems += [f'봉인 밖 모듈을 실제로 읽었다: {f}' for f in import_obs['outside']]
        print(f'  실제 import 관측 (run --observe-imports · G2RR2-03) — 프로세스 {import_obs["n_processes"]} · 리포 모듈 {len(import_obs["observed"])} ⊆ 봉인 '
              f'CODE_FILES {len(CODE_FILES)} ' + ('✓' if not obs_problems else '✗'))
        for p_ in obs_problems[:20]:
            print(f'  ✗ 관측: {p_}')
    bad = cnt.get('UNSEALED', 0) + mcnt.get('differs', 0) + mcnt.get('missing', 0) + len(gen_problems) + len(input_problems) + len(obs_problems)
    print('  ✓ 기록 전부 발사 봉인 코드에서 나왔다' + (' · merged = 케이스 폴더' if mcnt.get('same') else '')
          + (' · 레코드 세대 = 기대 세대' if declared else '') if not bad else
          f'  ✗ 봉인 밖 {cnt.get("UNSEALED", 0)} 건 · merged 와 다름 {mcnt.get("differs", 0) + mcnt.get("missing", 0)} 건 · 세대 문제 {len(gen_problems)} 건 — '
          '봉인 밖은 retry (발사 코드 그대로 둔 워커 체크아웃) 가 --force 로 다시 · merged 다름은 merge 를 다시 · 세대 문제는 그 기록을 인계하지 않는다')
    if cnt.get('NO_RECORD'):
        print(f'  ⚠ 기록 없음 {cnt["NO_RECORD"]} 건 — 계산되지 않았다 (merge 는 failed 로 싣는다 · retry 대상)')
    payload = dict(schema=LAUNCH_SEAL_SCHEMA + '#audit', root=str(root), audited_at=now_iso(), launch_sha=seal['sha'], seal_fp=seal['fp'],
                   code_root=str(seal['root']), code_root_changed_now=seal_diff(now, seal['hashes']), verdicts=dict(cnt),
                   merged=dict(mcnt), cases=rows, **{GEN_KEY: man.get(GEN_KEY)}, generation_declared=declared,
                   generation_problems=gen_problems, input_problems=input_problems,
                   eligibility=dict(kind=el['kind'], historical=el['historical'], problems=el['problems'], note=el['note']),
                   import_observation=import_obs, import_observation_problems=obs_problems)
    if args.json:
        write_json(Path(args.json).expanduser(), payload)
    if args.tsv:
        p = Path(args.tsv).expanduser()
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, 'w', encoding='utf-8', newline='') as fh:
            w = csv.writer(fh, delimiter='\t', lineterminator='\n')
            w.writerow(('case', 'cohort', 'record_status', 'verdict', 'attempt', 'run', 'form', 'merged', 'record_sha256', 'why'))
            for r in rows:
                w.writerow((r['case'], r['cohort'], r.get('record_status') or '', r['verdict'], r.get('attempt') or '', r.get('run') or '',
                            r.get('form') or '', r['merged'], r.get('record_sha') or '', r['why']))
    return 1 if bad else 0


def cmd_merge(args) -> int:
    root = Path(args.root).expanduser().resolve()
    _load_root(root)
    with root_lock(root):
        return merge(root, allow_mixed=args.allow_mixed_generation, historical=args.historical)


def cmd_status(args) -> int:
    root = Path(args.root).expanduser().resolve()
    man = _load_root(root)
    _el = launch_eligibility(man)
    print(f'  실행 형식 자격 {_el["kind"]}' + (f' ({_el["historical"]})' if _el['historical'] else '')
          + (f' — {_el["problems"][:3]}' if _el['problems'] else ''))
    cnt, running = collections.Counter(), []
    for e in man['plan']['queue']:
        cdir = case_dir(root, e['case'])
        pidrec = read_json(cdir / 'worker.pid.json')
        if pidrec and pid_alive(pidrec.get('pid'), e['case']):
            running.append(e['case'])
            cnt['running'] += 1
            continue
        s, _rec = _case_outcome(cdir, e['case'])
        w = read_json(cdir / 'worker.json')
        cnt[s or ('NO_RECORD' if w else 'pending')] += 1
    mi = meminfo()
    print(f'{root}: {dict(cnt)} · 도는 중 {running[:20]} · MemAvailable {gib(mi.get("MemAvailable"))} GB')
    return 0


def _parse(argv=None):
    ap = argparse.ArgumentParser(description='194 건 망 배치 병렬 실행기 (동적 큐 · 레인당 1 코어)')
    ap.add_argument('--selftest', action='store_true', help='가짜 워커로 계획 · 큐 · 기록 · merge 를 시험한다 (실제 파이프라인 없음)')
    sub = ap.add_subparsers(dest='cmd')

    def common_run(p):
        p.add_argument('-j', '--lanes', type=int, default=20, help='동시 케이스 수 (기본 20 · 1저자 "1코어 20개")')
        p.add_argument('--mem-budget-gb', type=float, default=None,
                       help='메모리 예산 (GB) — 추정 합이 넘으면 새 케이스를 기다린다 (기본 = MemAvailable − --mem-reserve-gb · 0 = 끔)')
        p.add_argument('--mem-reserve-gb', type=float, default=2.0, help='기본 예산에서 남겨 둘 메모리 (GB)')
        p.add_argument('--min-free-gb', type=float, default=1.0, help='실측 MemAvailable 이 이보다 작으면 새 케이스를 띄우지 않는다 (0 = 끔)')
        p.add_argument('--no-merge', action='store_true', help='끝나도 merge 하지 않는다')

    r = sub.add_parser('run', help='새 ROOT 에서 실행 (비어 있지 않으면 거부)')
    r.add_argument('--root', required=True)
    common_run(r)
    r.add_argument('--cohorts', default='lhs,lhsx', help='코호트 (쉼표) — lhs = 130 · lhsx = 64')
    r.add_argument('--case', action='append', default=[], help='이 케이스만 (여러 번 · 시범)')
    r.add_argument('--order', choices=['cost', 'name'], default='cost', help='큐 순서 — cost = 접촉 수 큰 순 (기본)')
    r.add_argument('--network-lock', choices=['per-case', 'shared'], default='per-case',
                   help='per-case = 케이스마다 TMPDIR (망 단계도 동시에 · 기본) · shared = 웹앱 lock 그대로 (망 단계는 하나씩)')
    r.add_argument('--python', default=sys.executable, help='워커 인터프리터 (기본 = 이 실행기를 돌린 것)')
    r.add_argument('--root-from', default='', help='코호트 경로 접두사 (lhs_webapp_batch 와 같은 뜻)')
    r.add_argument('--root-to', default='', help='실제 경로 접두사')
    for n in COHORT_SPECS:
        r.add_argument(f'--{n}-harvest', default='', help=f'{n} 수확 폴더 (기본 {COHORT_SPECS[n]["harvest"]})')
        r.add_argument(f'--{n}-cohort', default='', help=f'{n} 코호트 TSV (기본 {COHORT_SPECS[n]["cohort"]})')
    r.add_argument('--dry-run', action='store_true', help='사전 점검 · 계획 · 명령만 찍는다 (아무것도 안 쓴다)')
    r.add_argument('--allow-dirty', action='store_true', help='추적 파일이 바뀐 트리에서도 돈다 (manifest 에 남는다)')
    r.add_argument('--allow-missing-raw', action='store_true', help='원자료 · 메시가 없는 케이스가 있어도 돈다 (REFUSED 로 남는다)')
    r.add_argument('--skip-batch-selftest', action='store_true', help='발사 전 lhs_webapp_batch --selftest 를 건너뛴다')
    r.add_argument('--observe-imports', action='store_true',
                   help='시범 전용 — 워커 · 단계 하위 프로세스의 실제 import 를 <ROOT>/import_obs 에 적는다 (sitecustomize 훅 · 값에 닿지 않는다 · audit 가 봉인 ⊇ 관측을 '
                        '본다 · G2RR2-03 · manifest 에 남는다)')
    r.add_argument('--worker-script', default='', help=argparse.SUPPRESS)        # selftest 전용 (manifest 에 남는다)

    t = sub.add_parser('retry', help='done · partial 아닌 케이스 + 봉인 밖 (UNSEALED) 기록만 같은 ROOT 에서 다시 (시작 전 발사 봉인 대조 · 기록 보존)')
    t.add_argument('--root', required=True)
    common_run(t)
    t.add_argument('--case', action='append', default=[], help='이 케이스만')
    t.add_argument('--allow-mixed-generation', action='store_true',
                   help='워커 체크아웃의 코드 (HEAD · 봉인 파일 해시 · 빠진 해시) 가 발사 때와 달라도 돈다 (manifest retries[] · 실행 · 시도 기록에 남고 '
                        'merge 는 그 기록을 봉인 밖으로 판정한다)')
    t.add_argument('--allow-dirty', action='store_true',
                   help='추적 파일이 바뀐 트리에서도 돈다 — 코드 해시는 발사 봉인과 같아야 한다 (기록된다 · 그 시도 판정 SEALED_DIRTY_ALLOWED)')

    m = sub.add_parser('merge', help='케이스별 산출을 코호트별 한 폴더로 (다시) 묶는다')
    m.add_argument('--root', required=True)
    m.add_argument('--allow-mixed-generation', action='store_true',
                   help='워커 코드 sha 가 섞이거나 발사 봉인 밖 기록 (UNSEALED) 이 있어도 묶는다 (보고에 기록 · rc 1)')
    m.add_argument('--historical', action='store_true',
                   help='역사 모드 — 등록된 옛 실행 (HISTORICAL_LAUNCHES) 의 ROOT 만 (옛 형식 첫 run 규칙 · 세대 · 입력 대조 없음 표지 · G2RR2-01)')

    s = sub.add_parser('status', help='진행 상황')
    s.add_argument('--root', required=True)

    u = sub.add_parser('audit', help='발사 봉인 감사 (읽기 전용) — 케이스마다 어느 코드로 계산됐나 · merged 기록 = 케이스 폴더 기록인가')
    u.add_argument('--root', required=True)
    u.add_argument('--tsv', default='', help='판정표 TSV 를 쓸 곳 (주지 않으면 아무 파일도 안 쓴다)')
    u.add_argument('--json', default='', help='판정 JSON 을 쓸 곳')
    u.add_argument('--historical', action='store_true',
                   help='역사 모드 — 등록된 옛 실행 (HISTORICAL_LAUNCHES — 형식 + 발사 출처가 정확히) 의 ROOT 만 읽는다 (그 밖 = rc 2 · G2RR2-01)')
    return ap.parse_args(argv)


def main(argv=None) -> int:
    a = _parse(argv)
    if a.selftest:
        return _selftest()
    try:
        if a.cmd == 'run':
            return cmd_run(a)
        if a.cmd == 'retry':
            return cmd_retry(a)
        if a.cmd == 'merge':
            return cmd_merge(a)
        if a.cmd == 'status':
            return cmd_status(a)
        if a.cmd == 'audit':
            return cmd_audit(a)
    except LaunchError as e:
        print(f'⛔ {e}', file=sys.stderr)
        return 2
    _parse(['-h'])
    return 2


# ─────────────────────────────────── selftest ───────────────────────────────────
#: 가짜 워커 — **진짜 `lhs_webapp_batch.run_batch`** (스테이징 · sha · 프레임 관문 · status · metrics writer) 에 가짜 웹앱 의존만 넣는다.
#:   케이스마다 동작은 NP194_FAKE_PLAN (JSON) 이 정한다: ok · fail · crash (SIGKILL) · hang · sleep · alloc_mb · child_alloc_mb · extra · none_key.
FAKE_WORKER = r'''
import json, os, shutil, signal, subprocess, sys, time
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.environ['NP194_REPO'], 'scripts'))
import lhs_webapp_batch as LWB
PLAN = json.load(open(os.environ['NP194_FAKE_PLAN']))
if os.environ.get('NP194_FAKE_EXTRA_IMPORT'):          # ★ 10-07 G2RR2-03 import 관측 시험 — 워커가 봉인 밖 모듈을 읽는 대역
    __import__(os.environ['NP194_FAKE_EXTRA_IMPORT'])
ENVK = ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
        'TMPDIR', 'PYTHONDONTWRITEBYTECODE')
if os.environ.get('NP194_FAKE_DIRTY') in ('0', '1'):     # 봉인 시험 대역 — 워커 자신의 runs[] dirty 표지만 바꾼다 (git sha 는 진짜)
    _prov0 = LWB.code_provenance
    def _prov():
        p = _prov0()
        p['dirty'] = os.environ['NP194_FAKE_DIRTY'] == '1'
        return p
    LWB.code_provenance = _prov
def touch(n):
    b = bytearray(n << 20)
    for i in range(0, len(b), 4096):
        b[i] = 1
    return b
class FakeA:
    @staticmethod
    def detect_mode(case_dir):
        return 'bimodal'
    @staticmethod
    def run_pipeline(case, mode, tm, scale, figures=True, auto_db=True, **kw):
        b = PLAN.get(case) or {}
        rd = os.path.join(os.environ['WEBAPP_RESULTS_FOLDER'], case)
        os.makedirs(rd, exist_ok=True)
        e = {k: os.environ.get(k) for k in ENVK}
        e.update(cwd=os.getcwd(), stop_after=kw.get('stop_after'), figures=figures, auto_db=auto_db)
        json.dump(e, open(os.path.join(rd, '_env.json'), 'w'))
        if b.get('touch'):                                   # 봉인 시험 — 이 시도 중에 표지 파일을 만든다 (실행기 대역 해시가 그때부터 바뀐다)
            open(b['touch'], 'w').close()
        if b.get('sleep'):
            time.sleep(b['sleep'])
        keep = touch(b['alloc_mb']) if b.get('alloc_mb') else None
        if b.get('child_alloc_mb'):
            subprocess.run([sys.executable, '-c', 'b = bytearray(%d << 20)\nfor i in range(0, len(b), 4096): b[i] = 1\n'
                            % b['child_alloc_mb']], check=True)
        if b.get('mode') == 'crash':
            os.kill(os.getpid(), signal.SIGKILL)
        if b.get('mode') == 'hang':
            time.sleep(3600)
        fm = {'se_se_cn': b.get('cn', 4.25), 'percolation_pct': b.get('perc', 97.0), 'porosity': 12.5}
        fm.update(b.get('extra') or {})
        if b.get('none_key'):
            fm['nullable_key'] = None
        json.dump(fm, open(os.path.join(rd, 'full_metrics.json'), 'w'))
        #  ★ 10-07 — 망 레코드 모양: NP194_FAKE_DUAL = 실 생산자가 낸 세대 2 dual (selftest 가 봉인 코드의 세대 유도 탐침으로 만든다 · 감사의 케이스별 세대) ·
        #    legacy_dual = 세대 2 표지 없는 옛 모양 (세대 대조 반례) · 둘 다 없으면 옛 가짜 (σ 만)
        if b.get('legacy_dual'):
            json.dump({'hertzian': {'resistance_model': 'maxwell', 'sigma_full': 0.004}, 'physics': {'resistance_model': 'mikic', 'sigma_full': 0.004}},
                      open(os.path.join(rd, 'network_conductivity_dual.json'), 'w'))
        elif os.environ.get('NP194_FAKE_DUAL'):
            shutil.copyfile(os.environ['NP194_FAKE_DUAL'], os.path.join(rd, 'network_conductivity_dual.json'))
        else:
            json.dump({'hertzian': {'sigma_full': 0.004}, 'physics': {'sigma_full': 0.004}},
                      open(os.path.join(rd, 'network_conductivity_dual.json'), 'w'))
        del keep
        st = 'failed' if b.get('mode') == 'fail' else 'done'
        return {'status': st, 'success': st != 'failed',
                'failed_stages': (['Network stop contract (stop_after=network)'] if st == 'failed' else []),
                'network_run_id': (None if st == 'failed' else 'RUN-' + case), 'log': [{'step': 'Parse', 'rc': 0, 'ok': True}]}
class FakeTMR:
    @staticmethod
    def resolve_from_files(deck_p, atom_p):
        return {1: 'AM_P', 2: 'AM_S', 3: 'SE'}, [], []
    @staticmethod
    def format_map(m):
        return ','.join(f'{t}:{m[t]}' for t in sorted(m))
class FakeEM:
    @staticmethod
    def row_for(rd):
        d = json.load(open(os.path.join(rd, 'full_metrics.json')))
        return {'case': os.path.basename(rd), **d}
sys.exit(LWB.run_batch(LWB._parse(sys.argv[1:]), (FakeA, FakeTMR, FakeEM)))
'''


def _selftest() -> int:
    fails = []

    def chk(name, ok, why=''):
        print(('  ✓ ' if ok else '  ✗ ') + name + ('' if ok or not why else f'  — {why}'))
        if not ok:
            fails.append(name)

    tmp = Path(tempfile.mkdtemp(prefix='np194_')).resolve()
    env_keep = {k: os.environ.get(k) for k in ('NP194_REPO', 'NP194_FAKE_PLAN', 'TMPDIR', 'NP194_FAKE_DIRTY', 'NP194_FAKE_DUAL', 'NP194_FAKE_EXTRA_IMPORT')}
    os.environ.pop('NP194_FAKE_DIRTY', None)
    os.environ.pop('NP194_FAKE_DUAL', None)
    try:
        # ⓪ (★ 10-07) 봉인 코드의 세대 유도 탐침이 남긴 세대 2 dual — 가짜 워커가 케이스 결과에 쓴다 (감사의 케이스별 세대 대조 · ㉗–㉘).
        #    옛 코드 = 탐침 없음 → 옛 가짜 dual (σ 만) — 그때 ㉗ 이후는 ✗ 로 남는다
        _dg0 = globals().get('derive_generation')
        _tpl_dual = tmp / 'g2_probe_dual.json'
        _probe0 = _dg0(ROOT, sys.executable, dual_out=_tpl_dual) if _dg0 else {}
        if _tpl_dual.is_file():
            os.environ['NP194_FAKE_DUAL'] = str(_tpl_dual)
        # ── 합성 코호트 두 개 (lhs · lhsx) — 진짜 배치 관문을 통과하는 원자료 · 수확 JSON (lhs_webapp_batch selftest 와 같은 모양) ──
        _CHD = 'ITEM: ENTRIES c_cpl[7] c_cpl[8] c_cpl[9] c_cpl[22] c_cpl[23]\n'
        C_OK = 'ITEM: TIMESTEP\n100\nITEM: NUMBER OF ENTRIES\n2\n' + _CHD + '1 2 0 0.1 0.01\n2 3 1 0.1 0.02\n'
        A_OK = 'ITEM: TIMESTEP\n100\nITEM: ATOMS id type\n1 1\n2 2\n3 3\n'
        cases = {'lhs': ['lhs99_000', 'lhs99_001', 'lhs99_002', 'lhs99_003', 'lhs99_004', 'lhs99_005'],
                 'lhsx': ['lhsx_900', 'lhsx_901', 'lhsx_902']}
        contacts = {'lhs99_000': 500, 'lhs99_001': 900, 'lhs99_002': 300, 'lhs99_003': 700, 'lhs99_004': 900, 'lhs99_005': 100,
                    'lhsx_900': 800, 'lhsx_901': 50, 'lhsx_902': 600}
        specs = {}
        for fam, cl in cases.items():
            hd = tmp / 'data' / f'{fam}_harvest'
            hd.mkdir(parents=True)
            rows = []
            for c in cl:
                post = tmp / 'raw' / c / 'post'
                post.mkdir(parents=True)
                (post / 'atom_100.liggghts').write_text(A_OK)
                (post / 'contact_100.liggghts').write_text(C_OK)
                (post / 'mesh_100.stl').write_text(f'solid {c}\nendsolid\n')
                deck = tmp / 'raw' / c / f'input_{c}.liggghts'
                deck.write_text(f'# deck {c}\n')
                hj = dict(case=c, timestep=100, type_map={'1': 'AM_P', '2': 'AM_S', '3': 'SE'},
                          contact_scan=dict(n_rows_last=contacts[c]),
                          raw={k: dict(path=p.name, sha256=HB.sha256_of(p)) for k, p in
                               (('atom', post / 'atom_100.liggghts'), ('contact', post / 'contact_100.liggghts'),
                                ('mesh', post / 'mesh_100.stl'), ('deck', deck))})
                (hd / f'{c}.json').write_text(json.dumps(hj), encoding='utf-8')
                rows.append(f'{c}\tRAW_OK\t3\t{deck}\t{post / "atom_100.liggghts"}\t{post / "contact_100.liggghts"}\n')
            (hd / '_batch_summary.json').write_text('{}', encoding='utf-8')
            coh = tmp / 'data' / f'{fam}_cohort.tsv'
            coh.write_text('# 합성 코호트 (selftest)\ncase\tstatus\tn_types\tdeck\tatom_file\tcontact_file\n' + ''.join(rows),
                           encoding='utf-8')
            specs[fam] = dict(harvest=str(hd), cohort=str(coh), expect_n=len(cl), union='', design='')
        fake = tmp / 'fake_worker.py'
        fake.write_text(FAKE_WORKER, encoding='utf-8')
        plan_p = tmp / 'fake_plan.json'

        def set_plan(p):
            plan_p.write_text(json.dumps(p), encoding='utf-8')
        behav = {'lhs99_000': dict(sleep=0.6), 'lhs99_001': dict(mode='crash'), 'lhs99_002': dict(mode='fail'),
                 'lhs99_003': dict(alloc_mb=160, extra={'only_here': 1.5}), 'lhs99_004': dict(child_alloc_mb=220, none_key=True),
                 'lhs99_005': dict(sleep=0.3), 'lhsx_900': dict(sleep=0.5, extra={'x_only': 'a,b "q"'}), 'lhsx_901': {},
                 'lhsx_902': dict(sleep=0.2)}
        set_plan(behav)
        os.environ['NP194_REPO'] = str(ROOT)
        os.environ['NP194_FAKE_PLAN'] = str(plan_p)

        def args_for(root, *extra, allow_dirty=True):
            argv = ['run', '--root', str(root), '--worker-script', str(fake), *(['--allow-dirty'] if allow_dirty else []),
                    '--skip-batch-selftest',
                    '--lhs-harvest', specs['lhs']['harvest'], '--lhs-cohort', specs['lhs']['cohort'],
                    '--lhsx-harvest', specs['lhsx']['harvest'], '--lhsx-cohort', specs['lhsx']['cohort'], *extra]
            return argv

        # ① 계획 — 결정적 · 전수 한 번 · 비용 큰 순 (같으면 이름)
        a1 = _parse(args_for(tmp / 'r_plan'))
        p1 = build_plan(['lhs', 'lhsx'], cohort_specs(a1))
        p2 = build_plan(['lhs', 'lhsx'], cohort_specs(a1))
        names = [e['case'] for e in p1['queue']]
        allc = sorted(c for cl in cases.values() for c in cl)
        chk('① 계획이 결정적 (두 번 같다) · 전 케이스 정확히 한 번 · 접촉 큰 순 (같으면 이름)',
            p1 == p2 and sorted(names) == allc and len(names) == len(set(names))
            and names[:3] == ['lhs99_001', 'lhs99_004', 'lhsx_900'], repr(names))
        chk('① --case 필터 · 없는 케이스는 계획 거부', _raises(lambda: build_plan(['lhs'], cohort_specs(a1), ['nope_000']), LaunchError)
            and [e['case'] for e in build_plan(['lhs', 'lhsx'], cohort_specs(a1), ['lhsx_901'])['queue']] == ['lhsx_901'])

        # ② 비어 있지 않은 ROOT 는 거부 (아무것도 안 쓴다)
        busy = tmp / 'busy'
        busy.mkdir()
        (busy / 'old.txt').write_text('x')
        rc2 = main(args_for(busy))
        chk('② 비어 있지 않은 ROOT → rc 2 · manifest 없음', rc2 == 2 and not (busy / 'manifest.json').exists())

        # ③ --dry-run — ROOT 를 만들지 않는다
        dry = tmp / 'dry'
        rc3 = main(args_for(dry, '--dry-run'))
        chk('③ --dry-run → rc 0 · ROOT 를 만들지 않는다', rc3 == 0 and not dry.exists())

        # ④–⑦ 본 실행 — 레인 3 · 가짜 워커 (crash 1 · fail 1 · 메모리 둘)
        R = tmp / 'run1'
        t0 = time.monotonic()
        rc4 = main(args_for(R, '-j', '3', '--mem-budget-gb', '0', '--min-free-gb', '0'))
        wall = time.monotonic() - t0
        man = read_json(R / 'manifest.json') or {}
        wk = {c: read_json(case_dir(R, c) / 'worker.json') or {} for c in allc}
        last = {c: ((w.get('attempts') or [{}])[-1]) for c, w in wk.items()}
        chk(f'④ 실패가 있으면 rc 1 (조용히 초록이 아니다) · 실행 {wall:.1f} s', rc4 == 1, f'rc={rc4}')
        chk('④ 케이스마다 worker.json — rc · 경과 · 최대 RSS (KB) · user/sys',
            all(isinstance(l.get('rc'), int) and l.get('wall_s', -1) > 0 and l.get('peak_rss_kb', 0) > 0
                and 'user_s' in l and 'sys_s' in l for l in last.values()), repr({c: (l.get('rc'), l.get('peak_rss_kb')) for c, l in last.items()}))
        chk('④ crash (SIGKILL) 케이스 = rc −9 · signal SIGKILL · outcome NO_RECORD',
            last['lhs99_001'].get('rc') == -9 and last['lhs99_001'].get('signal') == 'SIGKILL'
            and last['lhs99_001'].get('outcome') == 'NO_RECORD', repr(last['lhs99_001']))
        rss = {c: l.get('peak_rss_mb', 0) for c, l in last.items()}
        base = max(v for c, v in rss.items() if c not in ('lhs99_003', 'lhs99_004'))
        chk(f'④ 최대 RSS 는 케이스별 (누적 아님) — 160 MB 할당 {rss["lhs99_003"]:.0f} · 자식 220 MB {rss["lhs99_004"]:.0f} · 나머지 최대 {base:.0f}',
            rss['lhs99_003'] >= 150 and rss['lhs99_004'] >= 210 and base < 140)
        iv = sorted((l['t_start_s'], l['t_end_s']) for l in last.values())
        mx = max(sum(1 for s, e in iv if s <= t < e) for t, _ in iv)
        chk(f'⑤ 동적 큐 — 동시 실행 최대 {mx} (≥ 2 · ≤ 레인 3)', 2 <= mx <= 3)
        envs = {c: read_json(case_dir(R, c) / 'work' / 'results' / c / '_env.json') for c in allc if c != 'lhs99_001'}
        ok6 = all(e and all(e.get(k) == '1' for k in THREAD_ENV) and e.get('PYTHONDONTWRITEBYTECODE') == '1'
                  and e.get('TMPDIR') == str(case_dir(R, c) / 'tmp') and e.get('cwd') == str(case_dir(R, c))
                  and e.get('stop_after') == 'network' and e.get('figures') is False and e.get('auto_db') is False
                  for c, e in envs.items())
        chk('⑥ 워커 환경 — 스레드 다섯 = 1 · PYTHONDONTWRITEBYTECODE · TMPDIR = 케이스/tmp · cwd = 케이스 폴더 · stop_after network · 그림/DB 끔',
            ok6, repr(next(iter(envs.values()))))
        ms = {f: read_json(R / 'merged' / f / 'status.json') or {} for f in cases}
        chk('⑦ merged 코호트별 status — schema · stop_after network · 케이스 집합 = 계획 (정확히)',
            all(ms[f].get('schema') == LWB.SCHEMA and ms[f].get('stop_after') == 'network'
                and sorted(ms[f].get('cases') or {}) == sorted(cases[f]) for f in cases))
        r_crash = (ms['lhs'].get('cases') or {}).get('lhs99_001') or {}
        chk('⑦ ★ 죽은 워커 케이스가 빠지지 않는다 — status failed · 사유에 rc −9 (SIGKILL) · 합성 표지',
            r_crash.get('status') == 'failed' and 'SIGKILL' in str(r_crash.get('why')) and r_crash.get('parallel_synthesized') is True,
            repr(r_crash))
        rep = read_json(R / 'merged' / 'merge_report.json') or {}
        chk('⑦ merge_report — 실패 둘 (crash · fail) 이 실패 목록에 · 구조 이상 0',
            sorted(f['case'] for f in rep.get('failures') or []) == ['lhs99_001', 'lhs99_002'] and not rep.get('structural'),
            repr(rep.get('failures')))

        # ⑧ 같은 케이스를 순차 배치 한 번 (같은 가짜 워커 · crash 제외) 으로 돌린 산출과 바이트 대조
        seq_out, seq_work = tmp / 'seq_out', tmp / 'seq_work'
        argv = [sys.executable, str(fake), '--stop-after', 'network', '--harvest-dir', specs['lhs']['harvest'],
                '--cohort', specs['lhs']['cohort'], '--work', str(seq_work), '--out-dir', str(seq_out)]
        for c in cases['lhs']:
            if c != 'lhs99_001':
                argv += ['--case', c]
        subprocess.run(argv, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'), capture_output=True, text=True)
        a_csv = (R / 'merged' / 'lhs' / 'metrics_flat.csv').read_bytes()
        b_csv = (seq_out / 'metrics_flat.csv').read_bytes() if (seq_out / 'metrics_flat.csv').exists() else b''
        chk('⑧ ★ merged metrics_flat.csv = 순차 배치 한 번의 metrics_flat.csv (바이트 · 열 순서 · 빈 칸 · 따옴표)', a_csv == b_csv and len(a_csv) > 0,
            f'{len(a_csv)} B vs {len(b_csv)} B')
        seq_st = read_json(seq_out / 'status.json') or {}

        def strip_t(rec):
            return {k: v for k, v in (rec or {}).items() if k not in ('when', 'elapsed_s')}
        same_rec = all(strip_t(ms['lhs']['cases'][c]) == strip_t((seq_st.get('cases') or {}).get(c))
                       for c in cases['lhs'] if c != 'lhs99_001')
        chk('⑧ status 케이스 기록 = 순차 배치 (시각 · 경과 빼고)', same_rec)

        # ⑨ 인계 생성기의 실제 읽기 함수가 merged 를 받는다
        import lhs_design_dataset as LDD
        try:
            wv = LDD.load_webapp(R / 'merged' / 'lhs')
            ok9 = (wv.get('stop_after') == 'network' and sorted(wv['status']) == sorted(cases['lhs'])
                   and sorted(wv['rows']) == sorted(c for c in cases['lhs'] if c != 'lhs99_001'))
            why9 = f"{wv.get('stop_after')} · {sorted(wv['rows'])}"
        except Exception as e:                              # noqa: BLE001
            ok9, why9 = False, f'{type(e).__name__}: {e}'
        chk('⑨ lhs_design_dataset.load_webapp(merged) — 거부 없음 · stop_after network · 상태 전 케이스 · 행 = 기록 있는 케이스', ok9, why9)

        # ⑩ τ 관문 입력 — results/<case> 가 전 케이스에 있다 (없는 케이스 = 빈 폴더 → NOT_COMPUTED 행)
        import tau_flux as TF
        trs = {c: TF.case_row(str(R / 'merged' / 'lhs' / 'results' / c)) for c in cases['lhs']}
        chk('⑩ τ 관문 — merged/lhs/results/<case> 전 케이스 · case 이름 = 폴더 이름 · 죽은 케이스도 행 (NOT_COMPUTED)',
            all(trs[c]['case'] == c for c in trs) and trs['lhs99_001'].get('ion_net_status_hertz') == 'NOT_COMPUTED'
            and (R / 'merged' / 'lhs' / 'results' / 'lhs99_000').is_symlink(), repr(trs['lhs99_001'].get('ion_net_status_hertz')))

        # ⑪ 세대 섞임 — 한 케이스의 워커 코드 sha 를 바꾸면 merge 거부 (rc 2 · merged 그대로) · 허용하면 rc 1 + 기록
        stp = case_dir(R, 'lhs99_000') / 'out' / 'status.json'
        st0 = stp.read_text(encoding='utf-8')
        st = json.loads(st0)
        st['runs'][-1]['git_sha'] = 'f' * 40
        stp.write_text(json.dumps(st), encoding='utf-8')
        before = (R / 'merged' / 'lhs' / 'status.json').read_bytes()
        rc11 = merge(R, out=lambda *a, **k: None)
        chk('⑪ ★ 워커 코드 sha 가 다르면 merge 거부 (rc 2) · merged 는 그대로 · 거부 보고 파일',
            rc11 == 2 and (R / 'merged' / 'lhs' / 'status.json').read_bytes() == before and (R / 'merge_report_REFUSED.json').exists())
        rc11b = merge(R, allow_mixed=True, out=lambda *a, **k: None)
        rep11 = read_json(R / 'merged' / 'merge_report.json') or {}
        chk('⑪ --allow-mixed-generation → rc 1 · 섞임이 보고에 남는다', rc11b == 1 and rep11.get('mixed_generation')
            and rep11.get('allow_mixed_generation') is True)
        stp.write_text(st0, encoding='utf-8')

        # ⑫ 남의 케이스 기록 — 케이스 폴더 status.json 에 다른 케이스가 있으면 구조 이상 (rc 2)
        st = json.loads(st0)
        st['cases']['lhs99_005'] = dict(case='lhs99_005', status='done')
        stp.write_text(json.dumps(st), encoding='utf-8')
        rc12 = merge(R, out=lambda *a, **k: None)
        rep12 = read_json(R / 'merge_report_REFUSED.json') or {}
        chk('⑫ ★ 케이스 폴더에 다른 케이스 기록 → merge 거부 (두 번 세지 않는다)', rc12 == 2
            and any('다른 케이스' in s for s in rep12.get('structural') or []))
        stp.write_text(st0, encoding='utf-8')

        # ⑬ retry — 실패 · 죽은 케이스만 다시 (기록이 쌓인다) → 전부 done · merge rc 0
        behav2 = dict(behav)
        behav2['lhs99_001'] = {}
        behav2['lhs99_002'] = {}
        set_plan(behav2)
        #  --allow-dirty — 이 ROOT 는 --allow-dirty 로 발사했다 (작업 중 트리일 수 있다) · retry 는 dirty 트리를 넘김 없이 거부한다 (RGLR3-01 · ⑳a)
        rc13 = main(['retry', '--root', str(R), '-j', '2', '--mem-budget-gb', '0', '--min-free-gb', '0', '--allow-dirty'])
        wk13 = {c: read_json(case_dir(R, c) / 'worker.json') or {} for c in allc}
        n_att = {c: len(w.get('attempts') or []) for c, w in wk13.items()}
        ms13 = read_json(R / 'merged' / 'lhs' / 'status.json') or {}
        chk('⑬ retry — 실패 둘만 다시 (시도 2) · 나머지 그대로 (시도 1) · merge rc 0 · 전부 done',
            rc13 == 0 and n_att['lhs99_001'] == 2 and n_att['lhs99_002'] == 2
            and all(n_att[c] == 1 for c in allc if c not in ('lhs99_001', 'lhs99_002'))
            and all((ms13.get('cases') or {}).get(c, {}).get('status') == 'done' for c in cases['lhs']), repr((rc13, n_att)))
        set_plan(behav)

        # ⑭ shared lock — TMPDIR 을 바꾸지 않는다
        os.environ['TMPDIR'] = str(tmp / 'shared_tmp')
        (tmp / 'shared_tmp').mkdir()
        R14 = tmp / 'run_shared'
        main(args_for(R14, '-j', '2', '--case', 'lhsx_901', '--network-lock', 'shared', '--mem-budget-gb', '0', '--min-free-gb', '0'))
        e14 = read_json(case_dir(R14, 'lhsx_901') / 'work' / 'results' / 'lhsx_901' / '_env.json') or {}
        chk('⑭ --network-lock shared → 워커 TMPDIR = 실행기의 TMPDIR (웹앱 lock 공유)', e14.get('TMPDIR') == str(tmp / 'shared_tmp'),
            repr(e14.get('TMPDIR')))
        if env_keep['TMPDIR'] is None:
            os.environ.pop('TMPDIR', None)
        else:
            os.environ['TMPDIR'] = env_keep['TMPDIR']

        # ⑮ 중단 — 실행기에 SIGINT → 도는 워커 (프로세스 묶음) 를 끄고 'interrupted' 로 기록 · 고아 없음 · merge 는 그 케이스를 failed 로
        set_plan({'lhsx_900': dict(mode='hang'), 'lhsx_902': dict(mode='hang')})
        R15 = tmp / 'run_int'
        p = subprocess.Popen([sys.executable, str(Path(__file__).resolve())] + args_for(
            R15, '-j', '2', '--cohorts', 'lhsx', '--case', 'lhsx_900', '--case', 'lhsx_902', '--mem-budget-gb', '0', '--min-free-gb', '0'),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
        pids, deadline = {}, time.monotonic() + 60
        while time.monotonic() < deadline and len(pids) < 2:
            for c in ('lhsx_900', 'lhsx_902'):
                pr = read_json(case_dir(R15, c) / 'worker.pid.json')
                if pr and (case_dir(R15, c) / 'work' / 'results' / c / '_env.json').exists():
                    pids[c] = pr['pid']
            time.sleep(0.2)
        os.kill(p.pid, signal.SIGINT)
        rc15 = p.wait(timeout=90)
        alive = [c for c, pid in pids.items() if pid_alive(pid, c)]
        o15 = {c: ((read_json(case_dir(R15, c) / 'worker.json') or {}).get('attempts') or [{}])[-1].get('outcome') for c in pids}
        chk(f'⑮ ★ 중단 — rc 130 · 두 워커 interrupted · 살아 있는 워커 0 ({len(pids)} 개 관측)',
            rc15 == 130 and len(pids) == 2 and not alive and set(o15.values()) == {'interrupted'}, repr((rc15, o15, alive)))
        rc15m = merge(R15, out=lambda *a, **k: None)
        ms15 = read_json(R15 / 'merged' / 'lhsx' / 'status.json') or {}
        chk('⑮ 중단 뒤 merge → rc 1 · 두 케이스 failed (빠지지 않는다)', rc15m == 1
            and all((ms15.get('cases') or {}).get(c, {}).get('status') == 'failed' for c in ('lhsx_900', 'lhsx_902')))
        set_plan(behav)

        # ⑯ 메모리 관문 — 실측 바닥을 터무니없이 높이면 한 번에 하나 (돌고 있는 게 없으면 늘 하나는 띄운다) · 대기 기록
        R16 = tmp / 'run_mem'
        main(args_for(R16, '-j', '3', '--cohorts', 'lhsx', '--mem-budget-gb', '0', '--min-free-gb', '1000000'))
        run16 = read_json(R16 / 'runs' / 'run_001.json') or {}
        chk('⑯ --min-free-gb 바닥 → 최대 동시 1 · 대기 기록 · 전부 끝남',
            run16.get('max_concurrent') == 1 and run16.get('events', 0) >= 1 and run16.get('finished') == 3, repr(run16))
        # ⑰ 메모리 예산 — 추정 합이 예산을 넘으면 기다린다 (backfill 은 작은 것 먼저 · 앞 케이스 굶김 방지)
        R17 = tmp / 'run_budget'
        budget_gb = (est_mem_mb(800) + est_mem_mb(600)) / 1024 * 0.999          # lhsx_900 + lhsx_902 는 함께 못 든다
        main(args_for(R17, '-j', '3', '--cohorts', 'lhsx', '--mem-budget-gb', f'{budget_gb:.6f}', '--min-free-gb', '0'))
        w17 = {c: ((read_json(case_dir(R17, c) / 'worker.json') or {}).get('attempts') or [{}])[-1] for c in cases['lhsx']}
        a, b = w17['lhsx_900'], w17['lhsx_902']
        overlap = a.get('t_start_s', 0) < b.get('t_end_s', 0) and b.get('t_start_s', 0) < a.get('t_end_s', 0)
        run17 = read_json(R17 / 'runs' / 'run_001.json') or {}
        chk('⑰ 메모리 예산 — 함께 못 드는 두 케이스는 겹치지 않는다 · 작은 케이스는 backfill · 전부 끝남',
            not overlap and run17.get('finished') == 3 and run17.get('backfills', 0) >= 1, repr((overlap, run17)))

        # ⑱ pyc 정리 — 같은 glob (scripts/__pycache__/*.pyc) 만 지운다 · dry 는 세기만
        sd = tmp / 'fake_scripts'
        (sd / '__pycache__').mkdir(parents=True)
        for n in ('a.cpython-311.pyc', 'b.cpython-311.pyc'):
            (sd / '__pycache__' / n).write_bytes(b'x')
        (sd / '__pycache__' / 'keep.txt').write_text('x')
        n_dry = purge_pyc(sd, dry=True)
        n_real = purge_pyc(sd)
        chk('⑱ pyc 정리 — dry 는 세기만 (2) · 본 정리 2 개 · 다른 파일은 그대로',
            n_dry == 2 and n_real == 2 and not list((sd / '__pycache__').glob('*.pyc')) and (sd / '__pycache__' / 'keep.txt').exists())
        # ⑲ manifest — 재현에 필요한 것
        chk('⑲ manifest — git · 코드 해시 · 스레드 · lock · 레인 · 계획 큐 · 워커 대체 표지',
            man.get('schema') == SCHEMA and man.get('git', {}).get('sha') and man.get('code_hashes', {}).get('webapp/app.py')
            and man.get('thread_env') == THREAD_ENV and man.get('network_lock') == 'per-case' and man.get('lanes') == 3
            and len(man.get('plan', {}).get('queue') or []) == len(allc) and man.get('worker_override') is True)

        # ═══ ⑳–㉕ RGLR3-01 (발사 봉인 · retry 관문 · 시도별 지문 · merge 판정) · RGLR3-03 (후속 명령) — 반례 먼저 ═══════════════════════
        #   Codex 10-05 4차 재검증 (`codex_review_rglr2_reverify_20261005.md` §3): 같은 HEAD 의 dirty retry 가 발사 봉인과 다른 코드로 돌고도
        #   retry rc 0 · merge 성공이었다 (HEAD 만 대조 · dirty 는 기록만 · code_changed_since_launch 는 정보뿐 · 워커는 git sha 만).
        #   대역 = 실행기 프로세스 안의 git_info · code_hashes (실제 트리는 건드리지 않는다) + 가짜 워커의 runs[] dirty 표지 (NP194_FAKE_DIRTY).
        #   케이스 실행 (진짜 lhs_webapp_batch.run_batch) · 기록 · merge 는 전부 진짜 경로.  옛 코드에 없는 명령 · 인자는 rc 로 받는다 (✗ 로 남게).
        import io
        _G = globals()
        _g_real = git_info()
        _sha_real = _g_real.get('sha') or ''
        _h_real = code_hashes()
        _NCF = 'scripts/network_conductivity.py'
        _cf = _G.get('code_fp')

        def _fp(h):
            return _cf(h) if _cf else None

        def _git_fake(dirty=False, sha=None):
            s_ = _sha_real if sha is None else sha

            def f(*_a, **_k):
                return dict(sha=s_, short=s_[:9], branch='selftest', dirty=dirty, porcelain=([' M ' + _NCF] if dirty else []))
            return f

        def _hashes_fake(mutate=None, sentinel=None):
            def f(*_a, **_k):
                h_ = dict(_h_real)
                if mutate and (sentinel is None or sentinel.exists()):
                    h_.update(mutate)
                return h_
            return f

        @contextlib.contextmanager
        def _patch(**kw):
            old_ = {k_: _G[k_] for k_ in kw}
            _G.update(kw)
            try:
                yield
            finally:
                _G.update(old_)

        def _main_rc(argv):
            """main → (rc, 화면).  argparse 거부 (옛 코드에 없는 명령 · 인자) 도 rc 로 받는다 — selftest 가 서지 않게."""
            buf_ = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf_), contextlib.redirect_stderr(buf_):
                    rc_ = main(argv)
            except SystemExit as e:
                rc_ = e.code if isinstance(e.code, int) else 2
            return rc_, buf_.getvalue()

        def _snap(root_):
            """아무것도 안 돌았나 — manifest · 케이스 worker.json · status.json 바이트 + runs/ 목록."""
            fs_ = [root_ / 'manifest.json'] + sorted((root_ / 'cases').glob('*/worker.json')) + sorted((root_ / 'cases').glob('*/out/status.json'))
            return {str(p_): p_.read_bytes() for p_ in fs_ if p_.exists()}, sorted(p_.name for p_ in (root_ / 'runs').glob('run_*.json'))

        def _audit_json(root_):
            jp_ = tmp / f'audit_{root_.name}_{time.monotonic_ns()}.json'
            rc_, o_ = _main_rc(['audit', '--root', str(root_), '--json', str(jp_)])
            return rc_, read_json(jp_) or {}, o_

        def _verdicts(aj_):
            return {r_.get('case'): r_.get('verdict') for r_ in (aj_.get('cases') or [])}

        def _scenario(name, fn):
            try:
                fn()
            except Exception as e:                          # noqa: BLE001 — 옛 코드 (함수 · 필드 없음) 도 ✗ 로 남긴다
                chk(name, False, f'{type(e).__name__}: {e}')

        L20 = ['-j', '2', '--mem-budget-gb', '0', '--min-free-gb', '0']

        # ⑳ (i)(a)(b)(d) — 대역 트리는 깨끗 · lhsx 세 케이스 · lhsx_901 은 실패 → retry 관문 · 시도별 지문
        R20 = tmp / 'run_seal'

        def _s20():
            set_plan({'lhsx_901': dict(mode='fail')})
            os.environ['NP194_FAKE_DIRTY'] = '0'
            with _patch(git_info=_git_fake()):
                rc_, _o = _main_rc(args_for(R20, '--cohorts', 'lhsx', *L20, allow_dirty=False))
            man_ = read_json(R20 / 'manifest.json') or {}
            fp_ = _fp(man_.get('code_hashes'))
            s_ = {c: (((read_json(case_dir(R20, c) / 'worker.json') or {}).get('attempts') or [{}])[-1].get('seal') or {})
                  for c in cases['lhsx']}
            chk('⑳i ★ 시도마다 봉인 증거 (worker.json attempts[].seal) — 띄우기 직전 · 거둔 직후 코드 지문 = manifest 지문 · git sha · dirty · '
                '이 시도가 쓴 기록 sha256 · 워커 runs 항목',
                rc_ == 1 and bool(fp_) and all(
                    v.get('fp_start') == fp_ and v.get('fp_end') == fp_ and v.get('launch_fp') == fp_ and v.get('git_sha_start') == _sha_real
                    and v.get('dirty_start') is False and v.get('record_written') is True and len(v.get('record_sha') or '') == 64
                    and (v.get('worker_run') or {}).get('git_sha') == _sha_real for v in s_.values()),
                repr((rc_, {c: sorted(v) for c, v in s_.items()})))
            snap0 = _snap(R20)
            with _patch(git_info=_git_fake(), code_hashes=_hashes_fake({_NCF: '0' * 64})):
                rc_a, o_a = _main_rc(['retry', '--root', str(R20), *L20])
            chk('⑳a ★ RGLR3-01 반례 — 같은 HEAD · 깨끗한 트리인데 봉인 코드 (network_conductivity.py) 가 바뀐 채 retry → rc 2 · 아무것도 안 돈다 '
                '(manifest · worker.json · status.json 바이트 · runs/ 그대로)',
                rc_a == 2 and _snap(R20) == snap0 and '발사 봉인' in o_a, repr((rc_a, o_a[-300:])))
            bad = []
            for nm_, pt_, ex_ in (('dirty 트리 (코드 같음 · --allow-dirty 없음)', dict(git_info=_git_fake(dirty=True)), []),
                                  ('HEAD 다름', dict(git_info=_git_fake(sha='f' * 40)), []),
                                  ('해시 빠짐 (봉인 파일 없음)', dict(git_info=_git_fake(), code_hashes=_hashes_fake({_NCF: None})), []),
                                  ('--allow-dirty 로는 코드 변경을 못 넘긴다', dict(git_info=_git_fake(dirty=True),
                                                                          code_hashes=_hashes_fake({_NCF: '0' * 64})), ['--allow-dirty'])):
                with _patch(**pt_):
                    rc_v, o_v = _main_rc(['retry', '--root', str(R20), *L20, *ex_])
                if not (rc_v == 2 and _snap(R20) == snap0 and '발사 봉인' in o_v):
                    bad.append((nm_, rc_v, o_v[-160:]))
            chk('⑳a ★ retry 시작 관문 — dirty 트리 · HEAD 다름 · 해시 빠짐 · (--allow-dirty 로 코드 변경 넘기기) 전부 rc 2 · 아무것도 안 돈다', not bad, repr(bad))
            with _patch(git_info=_git_fake()):
                rc_d, _o = _main_rc(['retry', '--root', str(R20), *L20])
            w901 = (read_json(case_dir(R20, 'lhsx_901') / 'worker.json') or {}).get('attempts') or []
            run2 = read_json(R20 / 'runs' / 'run_002.json') or {}
            chk('⑳d 양성 대조 — 코드 그대로 retry 는 돈다 (lhsx_901 시도 2 · 아직 실패라 rc 1) · 실행 기록에 봉인 지문 (발사 = 시작 = 끝)',
                rc_d == 1 and len(w901) == 2 and (w901[-1].get('seal') or {}).get('fp_start') == fp_
                and bool(fp_) and run2.get('seal_fp') == fp_ and run2.get('code_fp_start') == fp_ and run2.get('code_fp_end') == fp_,
                repr((rc_d, len(w901), run2.get('seal_fp'), fp_)))
            snap1 = _snap(R20)
            with _patch(git_info=_git_fake(), code_hashes=_hashes_fake({_NCF: '1' * 64})):
                rc_b, o_b = _main_rc(['retry', '--root', str(R20), *L20])
            chk('⑳b ★ 반례 — 두 retry 사이에 코드가 바뀌면 다음 retry 는 rc 2 · 아무것도 안 돈다', rc_b == 2 and _snap(R20) == snap1 and '발사 봉인' in o_b,
                repr((rc_b, o_b[-300:])))
            set_plan({})
            with _patch(git_info=_git_fake()):
                rc_e, _o = _main_rc(['retry', '--root', str(R20), *L20])
            rep_ = read_json(R20 / 'merged' / 'merge_report.json') or {}
            nat = {c: len((read_json(case_dir(R20, c) / 'worker.json') or {}).get('attempts') or []) for c in cases['lhsx']}
            chk('⑳d 양성 대조 — 코드 그대로 · 실패 케이스만 다시 (봉인된 done 은 그대로) → merge rc 0 · 봉인 판정 전부 SEALED · 봉인 밖 0',
                rc_e == 0 and nat == {'lhsx_900': 1, 'lhsx_901': 3, 'lhsx_902': 1}
                and (rep_.get('seal') or {}).get('verdicts') == {'SEALED': 3} and not (rep_.get('seal') or {}).get('unsealed'),
                repr((rc_e, nat, rep_.get('seal'))))
        _scenario('⑳ 봉인 시나리오', _s20)

        # ㉑ (c) 워커 dirty=True — 실행기는 깨끗하다고 봤는데 워커 자신이 runs[] 에 dirty 를 적었다 (그 실행은 --allow-dirty 아님)
        Rc = tmp / 'run_wdirty'

        def _s21():
            set_plan({})
            os.environ['NP194_FAKE_DIRTY'] = '1'
            with _patch(git_info=_git_fake()):
                rc_, _o = _main_rc(args_for(Rc, '--cohorts', 'lhsx', '-j', '3', '--mem-budget-gb', '0', '--min-free-gb', '0', allow_dirty=False))
            ref_ = read_json(Rc / 'merge_report_REFUSED.json') or {}
            un_ = (ref_.get('seal') or {}).get('unsealed') or []
            chk('㉑c ★ 반례 — 워커 기록 dirty=True (그 실행은 --allow-dirty 아님) → merge 거부 (rc 2 · merged 없음) · 세 케이스 봉인 밖 (사유 dirty)',
                rc_ == 2 and not (Rc / 'merged').exists() and len(un_) == 3 and all('dirty' in u for u in un_), repr((rc_, un_)))
            rc_a, aj_, _o = _audit_json(Rc)
            chk('㉑c audit (읽기 전용) — rc 1 · 세 케이스 UNSEALED · 판정 근거에 dirty',
                rc_a == 1 and _verdicts(aj_) == {c: 'UNSEALED' for c in cases['lhsx']}
                and all('dirty' in (r_.get('why') or '') for r_ in aj_.get('cases') or []), repr((rc_a, _verdicts(aj_))))
            os.environ['NP194_FAKE_DIRTY'] = '0'
            with _patch(git_info=_git_fake()):
                rc_r, _o = _main_rc(['retry', '--root', str(Rc), '-j', '3', '--mem-budget-gb', '0', '--min-free-gb', '0'])
            at_ = {c: (read_json(case_dir(Rc, c) / 'worker.json') or {}).get('attempts') or [] for c in cases['lhsx']}
            rep_ = read_json(Rc / 'merged' / 'merge_report.json') or {}
            chk('㉑c ★ retry — done 이어도 봉인 밖이면 --force 로 다시 (입증 못 한 케이스만) → merge rc 0 · 전부 SEALED',
                rc_r == 0 and all(len(v) == 2 and '--force' in (v[-1].get('cmd') or []) and '--force' not in (v[0].get('cmd') or [])
                                  for v in at_.values()) and (rep_.get('seal') or {}).get('verdicts') == {'SEALED': 3},
                repr((rc_r, {c: len(v) for c, v in at_.items()}, rep_.get('seal'))))
            rc_b, aj_b, _o = _audit_json(Rc)
            chk('㉑c audit 뒤 — rc 0 · 전부 SEALED · merged 기록 = 케이스 폴더 기록 (same)',
                rc_b == 0 and _verdicts(aj_b) == {c: 'SEALED' for c in cases['lhsx']}
                and all(r_.get('merged') == 'same' for r_ in aj_b.get('cases') or []), repr((rc_b, aj_b.get('cases'))))
        _scenario('㉑ 워커 dirty 시나리오', _s21)

        # ㉒ 실행 중 코드 변경 — 시도별 지문이 어느 케이스가 봉인 밖인지 가른다 · 입장 관문이 멈춘다 · retry 는 그 케이스만
        Rj = tmp / 'run_midchange'
        sent = tmp / 'code_changed.flag'

        def _s22():
            set_plan({'lhsx_901': dict(touch=str(sent))})
            os.environ['NP194_FAKE_DIRTY'] = '0'
            with _patch(git_info=_git_fake(), code_hashes=_hashes_fake({_NCF: '2' * 64}, sentinel=sent)):
                rc_, _o = _main_rc(args_for(Rj, '--cohorts', 'lhsx', '--order', 'name', '-j', '1', '--mem-budget-gb', '0', '--min-free-gb', '0',
                                            allow_dirty=False))
                rc_a, aj_, _o2 = _audit_json(Rj)
            fp_ = _fp((read_json(Rj / 'manifest.json') or {}).get('code_hashes'))
            s_ = {c: [a_.get('seal') or {} for a_ in (read_json(case_dir(Rj, c) / 'worker.json') or {}).get('attempts') or []] for c in cases['lhsx']}
            r1_ = read_json(Rj / 'runs' / 'run_001.json') or {}
            chk('㉒ ★ 실행 중 코드 변경 — lhsx_900 (변경 전) 지문 시작 = 끝 = 봉인 · lhsx_901 (그 시도 중 변경) 끝 지문 ≠ 봉인 · '
                'lhsx_902 는 띄우지 않는다 (입장 관문) · 자동 merge 없이 rc 2',
                rc_ == 2 and bool(fp_) and [(v.get('fp_start'), v.get('fp_end')) for v in s_['lhsx_900']] == [(fp_, fp_)]
                and len(s_['lhsx_901']) == 1 and s_['lhsx_901'][0].get('fp_start') == fp_ and s_['lhsx_901'][0].get('fp_end') not in (None, fp_)
                and _NCF in (s_['lhsx_901'][0].get('changed_end') or []) and not s_['lhsx_902']
                and r1_.get('not_started') == ['lhsx_902'] and bool(r1_.get('seal_broken')) and not (Rj / 'merged').exists(),
                repr((rc_, {c: [(v.get('fp_start'), v.get('fp_end')) for v in vs] for c, vs in s_.items()}, r1_.get('not_started'))))
            chk('㉒ audit — lhsx_900 SEALED · lhsx_901 UNSEALED (끝 지문) · lhsx_902 NO_RECORD · rc 1',
                rc_a == 1 and _verdicts(aj_) == {'lhsx_900': 'SEALED', 'lhsx_901': 'UNSEALED', 'lhsx_902': 'NO_RECORD'}, repr((rc_a, _verdicts(aj_))))
            sent.unlink()
            set_plan({})
            with _patch(git_info=_git_fake()):
                rc_r, _o = _main_rc(['retry', '--root', str(Rj), '-j', '1', '--mem-budget-gb', '0', '--min-free-gb', '0'])
            nat = {c: len((read_json(case_dir(Rj, c) / 'worker.json') or {}).get('attempts') or []) for c in cases['lhsx']}
            rep_ = read_json(Rj / 'merged' / 'merge_report.json') or {}
            chk('㉒ ★ 코드를 되돌린 뒤 retry — 봉인 밖 (lhsx_901 · --force) 과 안 돈 케이스 (lhsx_902) 만 → merge rc 0 · 전부 SEALED '
                '(run_001 의 실행 중 변경은 정보 — 판정은 시도별 지문)',
                rc_r == 0 and nat == {'lhsx_900': 1, 'lhsx_901': 2, 'lhsx_902': 1}
                and (rep_.get('seal') or {}).get('verdicts') == {'SEALED': 3}, repr((rc_r, nat, rep_.get('seal'))))
        _scenario('㉒ 실행 중 코드 변경 시나리오', _s22)

        # ㉓ (e) Codex new_probes.py 반례 그대로 — 실제 cmd_retry → _run_and_merge → merge · OS 잠금 · 환경 조회 · 워커만 대역
        #   ★ 10-07 G2RR2-01 — 옛 형식 ROOT 픽스처 = 등록된 옛 실행의 manifest 바이트 (형식 · 발사 출처 그대로 · 계획만 이 케이스) — 손으로 줄인 manifest 는
        #     이제 어느 형식도 아니다 (invalid · 옛 형식으로 추론하지 않는다)
        rr = tmp / 'codex_rglr3'
        case_ = 'lhs00_000'
        cs_ = dict(name='lhs', harvest_dir='sealed_harvest', cohort='sealed_cohort', expect_n=1, union='', design='')
        q_ = dict(case=case_, cohort='lhs', contacts=100, est_mem_mb=150.5)
        gh_ = '11fcf91e8a1f4837b83892b7e4a81125eaeee4e5'
        _hm = json.loads((ROOT / 'docs' / 'data' / 'lhs_network194_11fcf91e8' / 'manifest.json').read_text(encoding='utf-8'))
        man_c = dict(_hm, plan=dict(cohorts=[cs_], queue=[q_], order='cost'))
        _h_hist = dict(_hm['code_hashes'])
        changed_ = dict(_h_hist)
        changed_[_NCF] = '0' * 64

        def _legacy_root(root_, *, attempts, runs, st_runs, status='done'):
            write_json(root_ / 'manifest.json', man_c)
            cd_ = case_dir(root_, case_)
            st_ = dict(schema=LWB.SCHEMA, stop_after='network', harvest_dir=cs_['harvest_dir'], cohort=cs_['cohort'],
                       cases={case_: dict(case=case_, status=status, network_run_id='r1')}, runs=st_runs)
            LWB.write_outputs(cd_ / 'out', st_, {case_: dict(case=case_)})
            write_json(cd_ / 'worker.json', dict(attempts=attempts))
            for no_, rec_ in runs.items():
                write_json(root_ / 'runs' / f'run_{no_:03d}.json', rec_)
            return cd_, st_

        def _s23():
            cd_, st_ = _legacy_root(rr, attempts=[dict(rc=0, outcome='done', run=1, attempt=1)], runs={1: dict(code_changed_during_run=[])},
                                    st_runs=[dict(git_sha=gh_, dirty=False)])
            with _patch(code_hashes=lambda *a, **k: changed_):
                rc_m0 = merge(rr, out=lambda *a, **k: None)
                rc_m = merge(rr, out=lambda *a, **k: None, historical=True)
            rep_ = read_json(rr / 'merged' / 'merge_report.json') or {}
            chk('㉓e Codex 반례 앞 절반 — 끝난 뒤 지금 트리만 바뀐 배치는 기각하지 않는다 (옛 형식 첫 run = SEALED_LEGACY · ★ 역사 모드 merge --historical 에서만 · '
                '기본 merge = rc 2) · 바뀐 파일은 정보로 남는다',
                rc_m0 == 2 and rc_m == 0 and _NCF in (rep_.get('code_changed_since_launch') or []) and not rep_.get('mixed_generation')
                and (rep_.get('seal') or {}).get('verdicts') == {'SEALED_LEGACY': 1}
                and (rep_.get('eligibility') or {}).get('kind') == 'historical', repr((rc_m0, rc_m, rep_.get('seal'))))
            st_['cases'][case_]['status'] = 'failed'
            LWB.write_outputs(cd_ / 'out', st_, {case_: dict(case=case_)})
            called_ = []

            def synthetic_worker(*a, **kw):
                called_.append(True)
                st_['cases'][case_]['status'] = 'done'
                st_['runs'].append(dict(git_sha=gh_, dirty=True))
                LWB.write_outputs(cd_ / 'out', st_, {case_: dict(case=case_)})
                return dict(outcomes={'done': 1}, wall_h=0, max_concurrent=1, budget_events=0, backfills=0, events=0, interrupted=False)
            mocks_ = dict(_guard_posix=lambda: None, root_lock=lambda *a: contextlib.nullcontext(), purge_pyc=lambda *a, **k: 0,
                          git_info=lambda *a, **k: dict(sha=gh_, short=gh_[:9], dirty=True, porcelain=[' M ' + _NCF]),
                          code_hashes=lambda *a, **k: changed_, run_queue=synthetic_worker, meminfo=lambda: {'MemAvailable': 8 * 2 ** 30})
            rep_b = (rr / 'merged' / 'merge_report.json').read_bytes()

            def _retry(argv):
                buf_ = io.StringIO()
                try:
                    with _patch(**mocks_), contextlib.redirect_stdout(buf_), contextlib.redirect_stderr(buf_):
                        return cmd_retry(_parse(argv)), buf_.getvalue()
                except SystemExit as e:
                    return (e.code if isinstance(e.code, int) else 2), buf_.getvalue()
            rc_r, o_r = _retry(['retry', '--root', str(rr)])
            rc_o, o_o = _retry(['retry', '--root', str(rr), '--allow-dirty', '--allow-mixed-generation'])
            chk('㉓e ★ Codex new_probes.py 반례 그대로 — 같은 HEAD · dirty · 발사 뒤 바뀐 network_conductivity.py 지문으로 옛 형식 ROOT retry → rc 2 · '
                '워커 안 부름 · runs/run_002 없음 · merged 그대로 (옛 코드: retry_rc 0) · ★ G2RR2-01 — 역사 형식 ROOT 는 넘김 (--allow-dirty · '
                '--allow-mixed-generation) 으로도 이 실행기로 retry 하지 않는다 (그 커밋의 실행기로)',
                rc_r == 2 and rc_o == 2 and not called_ and not (rr / 'runs' / 'run_002.json').exists()
                and (rr / 'merged' / 'merge_report.json').read_bytes() == rep_b and '역사' in o_r and '역사' in o_o,
                repr((rc_r, rc_o, bool(called_), o_r[-300:])))
            #  넘김은 조용하지 않다 — 새 실행 형식 ROOT (⑳ 의 진짜 run ROOT 사본) 에서: 코드 · HEAD · dirty 가 발사와 다른 채 넘김 둘로 retry 하면 돌지만 그 기록은
            #   봉인 밖 · merge rc 1 · allow_mixed_generation · manifest retries[] 에 두 넘김 · 바뀐 파일
            rc_ = tmp / 'override_current'
            shutil.copytree(R20, rc_, symlinks=True)
            stp_ = case_dir(rc_, 'lhsx_901') / 'out' / 'status.json'
            st2_ = json.loads(stp_.read_text(encoding='utf-8'))
            st2_['cases']['lhsx_901']['status'] = 'failed'
            stp_.write_text(json.dumps(st2_), encoding='utf-8')
            called2_ = []

            def synthetic_worker2(*a, **kw):
                called2_.append(True)
                st2_['cases']['lhsx_901'].update(status='done', network_run_id='RUN-lhsx_901-override')    # 이 시도가 쓴 새 기록 (시도 지문 없음 — 대역)
                st2_['runs'].append(dict(git_sha=gh_, dirty=True))
                stp_.write_text(json.dumps(st2_), encoding='utf-8')
                return dict(outcomes={'done': 1}, wall_h=0, max_concurrent=1, budget_events=0, backfills=0, events=0, interrupted=False)
            changed_cur = dict(_h_real)
            changed_cur[_NCF] = '0' * 64
            mocks2_ = dict(mocks_, code_hashes=lambda *a, **k: changed_cur, run_queue=synthetic_worker2)
            buf2_ = io.StringIO()
            with _patch(**mocks2_), contextlib.redirect_stdout(buf2_), contextlib.redirect_stderr(buf2_):
                rc_o2 = cmd_retry(_parse(['retry', '--root', str(rc_), '--allow-dirty', '--allow-mixed-generation']))
            rep_o = read_json(rc_ / 'merged' / 'merge_report.json') or {}
            last_ = ((read_json(rc_ / 'manifest.json') or {}).get('retries') or [{}])[-1]
            chk('㉓e 넘김은 조용하지 않다 (새 실행 형식 ROOT) — --allow-dirty --allow-mixed-generation 이면 돌지만 그 기록은 봉인 밖 · '
                'merge rc 1 · allow_mixed_generation · manifest retries[] 에 두 넘김 · 바뀐 파일',
                rc_o2 == 1 and bool(called2_) and rep_o.get('allow_mixed_generation') is True and bool((rep_o.get('seal') or {}).get('unsealed'))
                and last_.get('allow_dirty') is True and last_.get('allow_mixed_generation') is True
                and _NCF in (last_.get('code_changed_vs_seal') or []), repr((rc_o2, rep_o.get('seal'), last_, buf2_.getvalue()[-300:])))
        _scenario('㉓ Codex 반례 시나리오', _s23)

        # ㉔ 옛 형식 (시도 지문 없는 실행기) 판정 규칙 — 첫 run 의 유일한 시도만 입증된다
        def _s24():
            _cs = _G.get('case_seal')
            _rt = _G.get('retry_todo')
            rl = tmp / 'legacy_retry'
            _legacy_root(rl, attempts=[dict(rc=-9, outcome='NO_RECORD', run=1, attempt=1), dict(rc=0, outcome='done', run=2, attempt=2)],
                         runs={1: dict(kind='run', code_changed_during_run=[]), 2: dict(kind='retry', code_changed_during_run=[])},
                         st_runs=[dict(git_sha=gh_, dirty=False)])
            v_ = _cs(rl, man_c, case_, history=True) if _cs else {}
            t_ = _rt(rl, man_c)[0] if _rt else []
            rc_ = merge(rl, out=lambda *a, **k: None, historical=True)
            chk('㉔ ★ 옛 형식 재시도 (run 2) 가 쓴 기록 — 시도 지문이 없어 입증 못 한다 → UNSEALED · merge (역사 모드) rc 2 · retry 목록은 done 이어도 --force 로 '
                '다시 고른다 (그 ROOT 의 retry 는 그 커밋의 실행기 몫)',
                v_.get('verdict') == 'UNSEALED' and rc_ == 2 and [e.get('case') for e in t_] == [case_] and t_[0].get('force') is True,
                repr((v_, rc_, t_)))
            rok = tmp / 'legacy_ok_first_run'
            _legacy_root(rok, attempts=[dict(rc=0, outcome='done', run=1, attempt=1)], runs={1: dict(kind='run', code_changed_during_run=[])},
                         st_runs=[dict(git_sha=gh_, dirty=False)])
            vh_, vn_ = _cs(rok, man_c, case_, history=True), _cs(rok, man_c, case_)
            chk('㉔ ★ G2RR2-01 — 같은 옛 형식 첫 run 기록: 역사 모드 = SEALED_LEGACY · 역사 모드가 아니면 (새 실행 형식 판정) UNSEALED — 시도 지문이 없다는 것으로 '
                '옛 형식을 추론하지 않는다', vh_.get('verdict') == 'SEALED_LEGACY' and vn_.get('verdict') == 'UNSEALED' and 'G2RR2-01' in vn_.get('why', ''),
                repr((vh_.get('verdict'), vn_.get('verdict'), vn_.get('why'))))
            bad = []
            for nm_, kw_ in (('첫 run 중 코드 변경 (h0 ≠ h1)', dict(runs={1: dict(kind='run', code_changed_during_run=[_NCF])})),
                             ('워커 dirty', dict(st_runs=[dict(git_sha=gh_, dirty=True)])),
                             ('워커 sha ≠ 발사', dict(st_runs=[dict(git_sha='e' * 40, dirty=False)])),
                             ('기록 두 번 (runs 2 건)', dict(st_runs=[dict(git_sha=gh_, dirty=False)] * 2)),
                             ('유일한 시도가 기록을 안 썼다 (LAUNCH_ERROR)', dict(attempts=[dict(rc=None, outcome='LAUNCH_ERROR', run=1, attempt=1)])),
                             ('시도의 run id ≠ 기록', dict(attempts=[dict(rc=0, outcome='done', run=1, attempt=1, network_run_id='r9')]))):
                rv = tmp / f'legacy_{len(bad)}_{time.monotonic_ns()}'
                base_ = dict(attempts=[dict(rc=0, outcome='done', run=1, attempt=1)], runs={1: dict(kind='run', code_changed_during_run=[])},
                             st_runs=[dict(git_sha=gh_, dirty=False)])
                base_.update(kw_)
                _legacy_root(rv, **base_)
                vv = _cs(rv, man_c, case_, history=True) if _cs else {}
                if vv.get('verdict') != 'UNSEALED':
                    bad.append((nm_, vv.get('verdict')))
            chk('㉔ 옛 형식 첫 run 도 — 실행 중 코드 변경 · 워커 dirty · 워커 sha 다름 · 기록 두 번이면 UNSEALED', not bad and bool(_cs), repr(bad))
        _scenario('㉔ 옛 형식 판정 시나리오', _s24)

        # ㉕ RGLR3-03 — 후속 명령: 인계 생성기 한 번에 τ 묶음 + --tau-results · 손 case 잇기 안내 없음 · 포장에 인계표 · 열 사전 · τ 출처 부록 · 제외 노트
        def _s25():
            Rf = tmp / 'fu_root'
            pl_ = dict(cohorts=[dict(name=n, harvest_dir=str(_abs(COHORT_SPECS[n]['harvest'])), cohort=str(_abs(COHORT_SPECS[n]['cohort'])),
                                     union=COHORT_SPECS[n]['union'], design=COHORT_SPECS[n]['design']) for n in ('lhs', 'lhsx')], queue=[])
            mf_ = dict(schema=SCHEMA, git=dict(sha='a' * 40, short='a' * 9), code_hashes=dict(_h_real), plan=pl_)
            d0 = time.strftime('%Y%m%d')
            ln_ = []
            print_followups(Rf, mf_, out=lambda *a, **k: ln_.append(' '.join(map(str, a))))
            d1 = time.strftime('%Y%m%d')
            txt = '\n'.join(ln_)
            Q = shlex.quote
            gen = {n: next((l_ for l_ in ln_ if l_.startswith('python3 scripts/lhs_design_dataset.py') and f'{n}_handover_v12_' in l_), '')
                   for n in ('lhs', 'lhsx')}
            want = {n: (f' --harvest {Q(str(_abs(COHORT_SPECS[n]["harvest"])))} --union {Q(COHORT_SPECS[n]["union"])} '
                        f'--webapp {Q(str(Rf / "merged" / n))} --webapp-groups contact,percolation,f1,fracture,area,tau '
                        f'--tau-results {Q(str(Rf / "merged" / n / "results"))} '
                        f'--pressure-record {Q(str(Rf / "pressure" / f"{n}_pressure_record.tsv"))}') for n in ('lhs', 'lhsx')}
            chk('㉕ ★ RGLR3-03 — 인계 명령 = --webapp <ROOT>/merged/<코호트> --webapp-groups contact,percolation,f1,fracture,area,tau '
                '--tau-results <ROOT>/merged/<코호트>/results · 수확 = 절대 경로 · union = lhs130 / lhsx64 · lhsx 만 --design · 손 case 잇기 안내 없음',
                all(gen[n].endswith(want[n]) for n in gen)
                and ' --design docs/data/lhsx_design_adapted_20260929.csv --harvest ' in gen['lhsx'] and '--design' not in gen['lhs']
                and 'case 열로 잇기' not in txt and '아직 생성기 묶음이 아니다' not in txt, repr(gen))
            prs_ = {n: next((l_ for l_ in ln_ if l_.startswith('python3 scripts/lhs_pressure_record.py') and f'{n}_pressure_record.tsv' in l_), '')
                    for n in ('lhs', 'lhsx')}
            chk('㉕ ★ DESC-06 — 완료 압력 기록 명령 (코호트 · 수확 = 인계 명령과 같은 수확 · 산출 = 생성기 --pressure-record 가 읽는 그 파일) · 생성기 명령에 --pressure-record',
                all(f'--cohort {Q(str(_abs(COHORT_SPECS[n]["cohort"])))}' in prs_[n] and f'--harvest-dir {Q(str(_abs(COHORT_SPECS[n]["harvest"])))}' in prs_[n]
                    and prs_[n].endswith(f'--out {Q(str(Rf / "pressure" / f"{n}_pressure_record.tsv"))}') and '--pressure-record' in gen[n]
                    for n in prs_), repr(prs_))
            tar_ = next((l_ for l_ in ln_ if 'tar czf' in l_ and '_tau_sources' not in l_), '')

            def _need(dd):
                return [f'handover/{n}_handover_v12_{dd}{suf}' for n in ('lhs', 'lhsx')
                        for suf in ('.csv', '_columns.tsv', '_tau_provenance.tsv', '_excluded.tsv')]
            chk('㉕ ★ 포장 (tar) — 인계표 · 열 사전 (_columns.tsv) · τ 출처 부록 (_tau_provenance.tsv) · 제외 노트 (_excluded.tsv) · 봉인 감사 · '
                'manifest · runs · 시도 기록',
                any(all(x_ in tar_.split() for x_ in _need(dd)) for dd in {d0, d1})
                and all(x_ in tar_.split() for x_ in ('seal_audit.tsv', 'manifest.json', 'runs', 'cases/*/worker.json')), repr(tar_))
            import lhs_design_dataset as LDD2
            hp = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'lhs_design_dataset.py'), '--help'], capture_output=True, text=True,
                                timeout=300, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
            flags = sorted({t_ for g_ in gen.values() for t_ in shlex.split(g_) if t_.startswith('--')})
            chk('㉕ 생성기와 짝 — 찍는 묶음 = lhs_design_dataset.WA_STAGE_GROUPS["network"] (tau 포함) · 찍는 인자 전부가 생성기 파서에 있다 '
                '(28 τ 열을 실제로 내는 CLI 왕복은 생성기 selftest ㉙i — 이 실행기의 가짜 워커 결과는 생산자 레코드가 아니라 거기서 못 돌린다)',
                HANDOVER_GROUPS == ','.join(LDD2.WA_STAGE_GROUPS.get('network', ())) and 'tau' in HANDOVER_GROUPS.split(',')
                and hp.returncode == 0 and bool(flags) and all(f_ in hp.stdout for f_ in flags), repr((HANDOVER_GROUPS, flags, hp.returncode)))
            ln2 = []
            print_followups(R, read_json(R / 'manifest.json') or {}, out=lambda *a, **k: ln2.append(' '.join(map(str, a))))
            tr_ = [t_ for l_ in ln2 if l_.startswith('python3 scripts/lhs_design_dataset.py') for t_ in [shlex.split(l_)]]
            res_ = [Path(t_[t_.index('--tau-results') + 1]) for t_ in tr_ if '--tau-results' in t_]
            chk('㉕ 찍힌 --tau-results 폴더 = merge 가 만든 merged/<코호트>/results (케이스마다 한 항목 · 결과 없는 케이스도)',
                len(res_) == 2 and all(p_.is_dir() and sorted(x_.name for x_ in p_.iterdir()) == sorted(cases[p_.parent.name]) for p_ in res_),
                repr(res_))
        _scenario('㉕ 후속 명령 시나리오', _s25)

        # ㉖ 봉인은 워커 체크아웃 (manifest repo_root) 에서 잰다 — 새 실행기를 다른 체크아웃에서 돌려 옛 ROOT 를 retry · audit 할 때 (WSL)
        def _s26():
            alt = tmp / 'alt_checkout'
            for rel in CODE_FILES:
                (alt / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / rel, alt / rel)
            man_a = dict(man_c, code_hashes=dict(_h_real), repo_root=str(alt))      # 봉인 = 지금 코드 (형식 자격은 이 시험 밖 — 해시 대조만 본다)
            seen = []

            def g_alt(root=None):
                seen.append(None if root is None else str(root))
                return dict(sha=gh_, short=gh_[:9], dirty=False, porcelain=[])
            with _patch(git_info=g_alt):
                ok_ = seal_gate(man_a)
                (alt / _NCF).write_text('# 워커 체크아웃에서만 바뀜\n', encoding='utf-8')
                bad_ = seal_gate(man_a)
            chk('㉖ 봉인은 워커 체크아웃에서 잰다 — repo_root = 다른 체크아웃이면 그 파일 · 그 git 으로 대조 (같으면 통과 · 그 체크아웃의 봉인 파일이 '
                '바뀌면 거부 · 이 실행기 체크아웃의 파일은 보지 않는다)',
                not ok_['mixed'] and not ok_['dirty'] and bad_['changed'] == [_NCF] and bool(bad_['mixed']) and str(alt) in seen
                and None not in seen, repr((ok_['mixed'], bad_['changed'], seen)))
        _scenario('㉖ 워커 체크아웃 시나리오', _s26)

        # ═══ ㉗–㉛ ★ 10-07 Codex 세대 2 재검증 §7-3 · G2RR-01 (manifest 기대 세대 · 전이 의존 봉인) — 반례 먼저 (옛 코드에서 ✗) ═════════════════
        #   인계 생성기 (`lhs_design_dataset.load_tau_results(expected_generation=)` · CLI `--tau-batch-manifest`) 는 manifest 의 expected_network_generation 을
        #   읽고 없으면 거부한다 — 이 실행기가 그 값을 쓰지 않았다 (소비자 쪽 hook 만 있었다 · e1dab4265).  값은 손으로 적지 않고 워커 체크아웃의 봉인 코드로
        #   유도한다 (생산자 _run_all_networks 를 CLI 기본값으로 작은 사슬에 한 번 → 같은 체크아웃의 세대 계약).
        GK = _G.get('GEN_KEY', 'expected_network_generation')

        def _s27():
            set_plan({})
            os.environ['NP194_FAKE_DIRTY'] = '0'
            with _patch(git_info=_git_fake()):
                rc_d, o_d = _main_rc(args_for(tmp / 'dry_gen', '--cohorts', 'lhsx', '--dry-run', allow_dirty=False))
                rc_, _o = _main_rc(args_for(tmp / 'run_gen', '--cohorts', 'lhsx', *L20, allow_dirty=False))
            man_ = read_json(tmp / 'run_gen' / 'manifest.json') or {}
            pr_ = man_.get('generation_probe') or {}
            import lhs_design_dataset as LDD3
            try:
                consumer = LDD3.tau_manifest_expected_generation(man_)
            except Exception as e:                          # noqa: BLE001
                consumer = f'{type(e).__name__}'
            chk('㉗ ★ G2RR-01 · §7-3 — 발사 manifest 에 기대 망 세대 (expected_network_generation) = 봉인 코드에서 유도한 g2 · 봉인 사본 seal 안 같은 값 · '
                '유도 탐침 기록 (세대 계약 문제 0) · 인계 생성기 (tau_manifest_expected_generation) 가 그 값을 읽는다',
                rc_ == 0 and man_.get(GK) == 'g2' and (man_.get('seal') or {}).get(GK) == 'g2' and pr_.get('generation') == 'g2'
                and pr_.get('problems') == [] and consumer == 'g2',
                repr((rc_, man_.get(GK), (man_.get('seal') or {}).get(GK), pr_, consumer)))
            chk('㉗ --dry-run 도 유도한 기대 망 세대를 찍는다 (아무것도 안 쓴다)',
                rc_d == 0 and '기대 망 세대' in o_d and 'g2' in o_d and not (tmp / 'dry_gen').exists(), o_d[-400:])
            rc_a, aj_, _o = _audit_json(tmp / 'run_gen')
            gens_ = [r_.get('generation') for r_ in aj_.get('cases') or []]
            chk('㉗ audit — 선언 g2 · 케이스마다 레코드 세대 = g2 (세 케이스) · 세대 문제 0 · rc 0',
                rc_a == 0 and aj_.get(GK) == 'g2' and not aj_.get('generation_problems') and gens_ == ['g2'] * 3,
                repr((rc_a, aj_.get(GK), aj_.get('generation_problems'), gens_)))
        _scenario('㉗ 기대 세대 발사 시나리오', _s27)

        def _s28():
            src_ = tmp / 'run_gen'
            bad = []
            variants = {'값만 바꿈 (inferred_legacy)': lambda m: m.update({GK: 'inferred_legacy'}),
                        '값 · 봉인 사본 둘 다 바꿈': lambda m: (m.update({GK: 'inferred_legacy'}), m.setdefault('seal', {}).update({GK: 'inferred_legacy'})),
                        '봉인 사본 삭제': lambda m: m.setdefault('seal', {}).pop(GK, None),
                        '값 삭제 (봉인 사본만 남음)': lambda m: m.pop(GK, None)}
            for i_, (nm_, ed_) in enumerate(variants.items()):
                r_ = tmp / f'gen_var{i_}'
                shutil.copytree(src_, r_, symlinks=True)
                m_ = read_json(r_ / 'manifest.json') or {}
                ed_(m_)
                write_json(r_ / 'manifest.json', m_)
                snap_ = _snap(r_)
                with _patch(git_info=_git_fake()):
                    rc_v, o_v = _main_rc(['retry', '--root', str(r_), *L20, '--allow-mixed-generation', '--allow-dirty'])
                if not (rc_v == 2 and _snap(r_) == snap_ and '기대 망 세대' in o_v):
                    bad.append((nm_, rc_v, o_v[-200:]))
            chk('㉘ ★ retry — manifest 기대 세대 변조 (값만 · 값과 봉인 사본 · 봉인 사본 삭제 · 값 삭제) → rc 2 · 아무것도 안 돈다 · '
                '--allow-mixed-generation · --allow-dirty 로도 못 넘긴다', not bad, repr(bad))
            r_ = tmp / 'gen_code_other'
            shutil.copytree(src_, r_, symlinks=True)
            snap_ = _snap(r_)
            with _patch(git_info=_git_fake(), derive_generation=lambda *a, **k: dict(generation='inferred_legacy', g2_name='g2', problems=[], error='')):
                rc_c, o_c = _main_rc(['retry', '--root', str(r_), *L20, '--allow-mixed-generation', '--allow-dirty'])
            chk('㉘ ★ retry — 워커 체크아웃 코드가 지금 내는 세대 (다시 유도) ≠ 봉인 기대 세대 → rc 2 · 아무것도 안 돈다 (넘김 불가)',
                rc_c == 2 and _snap(r_) == snap_ and '기대 망 세대' in o_c, o_c[-300:])
            r_ = tmp / 'gen_ok'
            shutil.copytree(src_, r_, symlinks=True)
            with _patch(git_info=_git_fake()):
                rc_p, o_p = _main_rc(['retry', '--root', str(r_), *L20])
            chk('㉘ 양성 — manifest · 코드 그대로면 retry 가 세대 관문을 지난다 (할 일 없음 → merge rc 0)', rc_p == 0, o_p[-300:])
            rc_a, aj_, _o = _audit_json(tmp / 'gen_var0')
            chk('㉘ audit — manifest 기대 세대 ≠ 봉인 사본 → 비영 (★ G2RR2-01: 실행 형식 자격 invalid = rc 2 · 판정표 없음 · 사유 = 기대 망 세대)',
                rc_a == 2 and (aj_.get('eligibility') or {}).get('kind') == 'invalid'
                and any('기대 망 세대' in p_ for p_ in (aj_.get('eligibility') or {}).get('problems') or []),
                repr((rc_a, aj_.get('eligibility'))))
            set_plan({'lhsx_901': dict(legacy_dual=True)})
            with _patch(git_info=_git_fake()):
                _main_rc(args_for(tmp / 'run_gen_legacy_case', '--cohorts', 'lhsx', *L20, allow_dirty=False))
                rc_l, aj_l, _o = _audit_json(tmp / 'run_gen_legacy_case')
            set_plan({})
            gens_ = {r_['case']: r_.get('generation') for r_ in aj_l.get('cases') or []}
            chk('㉘ ★ audit — 한 케이스의 레코드 세대 (세대 2 표지 없는 옛 모양 dual) ≠ manifest 기대 세대 → rc 1 · 그 케이스만 다른 세대 표지',
                rc_l == 1 and gens_.get('lhsx_901') not in ('g2', None) and gens_.get('lhsx_900') == 'g2' and gens_.get('lhsx_902') == 'g2',
                repr((rc_l, gens_)))
        _scenario('㉘ 기대 세대 변조 · 불일치 시나리오', _s28)

        def _s29():
            sg_ = _G.get('seal_gate')
            with _patch(git_info=lambda *a, **k: dict(sha=gh_, short=gh_[:9], dirty=False, porcelain=[])):
                g_old = sg_(dict(man_c))
            chk('㉙ ★ G2RR2-01 — 옛 manifest (등록된 옛 실행 · 기대 세대 선언 없는 형식) 의 retry 세대 관문 = 막는다 (역사 형식 · 그 커밋의 실행기로 · 넘김 불가) '
                '(옛 판: 막지 않았다 — 선언이 없다는 것만으로 면제)',
                bool(g_old.get('generation_bad')) and '역사' in str(g_old.get('generation_bad')),
                repr((g_old.get('generation_bad'), g_old.get('generation_note'), g_old.get('mixed'))))
            rl_ = tmp / 'legacy_gen_audit'
            _legacy_root(rl_, attempts=[dict(rc=0, outcome='done', run=1, attempt=1)], runs={1: dict(kind='run', code_changed_during_run=[])},
                         st_runs=[dict(git_sha=gh_, dirty=False)])
            rc_n, _aj_n, _o_n = _audit_json(rl_)
            jp_ = tmp / f'audit_hist_{time.monotonic_ns()}.json'
            rc_a, _o = _main_rc(['audit', '--root', str(rl_), '--historical', '--json', str(jp_)])
            aj_ = read_json(jp_) or {}
            chk('㉙ 옛 manifest 감사 — 기본 = rc 2 (역사 형식) · 역사 모드 (--historical) = rc 0 · SEALED_LEGACY · 기대 세대 None (선언 없음 표지) · 세대 문제 0 · '
                '케이스 세대 대조 안 함',
                rc_n == 2 and rc_a == 0 and _verdicts(aj_) == {case_: 'SEALED_LEGACY'} and GK in aj_ and aj_.get(GK) is None
                and not aj_.get('generation_problems') and all(r_.get('generation') is None for r_ in aj_.get('cases') or []),
                repr((rc_n, rc_a, _verdicts(aj_), aj_.get(GK, 'KEY_ABSENT'), aj_.get('generation_problems'))))
        _scenario('㉙ 옛 manifest 시나리오', _s29)

        def _s30():
            cdc = _G.get('code_dependency_closure')
            clo = cdc(ROOT) if cdc else {}
            files_ = clo.get('files') or []
            miss_ = [f for f in files_ if f not in CODE_FILES]
            chk('㉚ ★ §7-3 전이 의존 — 워커 망 정지 경로의 정적 import 닫힘 ⊆ 봉인 CODE_FILES (lens_geometry — plastic_coverage 가 import · physics g2 원판 floor — 포함) · '
                '해석 오류 0', bool(files_) and not miss_ and 'scripts/lens_geometry.py' in files_ and 'scripts/lens_geometry.py' in CODE_FILES
                and not clo.get('errors'), repr((miss_, clo.get('errors'))))
            alt = tmp / 'dep_alt'
            for rel in set(CODE_FILES) | {'scripts/step3_sigma.py'}:
                (alt / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / rel, alt / rel)
            p_ = alt / 'scripts' / 'network_conductivity.py'
            p_.write_text('import step3_sigma  # selftest — 새 의존\n' + p_.read_text(encoding='utf-8'), encoding='utf-8')
            clo2 = cdc(alt) if cdc else {}
            chk('㉚ 반례 — 봉인 모듈에 새 import (network_conductivity → step3_sigma) 를 넣으면 닫힘에 잡힌다 (봉인 밖 의존)',
                'scripts/step3_sigma.py' in (clo2.get('files') or []) and 'scripts/step3_sigma.py' not in CODE_FILES, repr(clo2.get('files')))
            with _patch(code_dependency_closure=lambda *a, **k: dict(files=sorted(set(CODE_FILES) | {'scripts/step3_sigma.py'}), errors=[])):
                rc_, o_ = _main_rc(args_for(tmp / 'dry_dep', '--cohorts', 'lhsx', '--dry-run'))
            chk('㉚ 발사 사전 점검 — 봉인 밖 의존 모듈이 있으면 중단 (rc 2 · 아무것도 안 쓴다)',
                rc_ == 2 and 'step3_sigma' in o_ and not (tmp / 'dry_dep').exists(), o_[-300:])
        _scenario('㉚ 전이 의존 시나리오', _s30)

        def _s31():
            Rf = tmp / 'fu_gen'
            pl_ = dict(cohorts=[dict(name=n, harvest_dir=str(_abs(COHORT_SPECS[n]['harvest'])), cohort=str(_abs(COHORT_SPECS[n]['cohort'])),
                                     union=COHORT_SPECS[n]['union'], design=COHORT_SPECS[n]['design']) for n in ('lhs', 'lhsx')], queue=[])
            mf_ = dict(schema=SCHEMA, git=dict(sha='a' * 40, short='a' * 9), code_hashes=dict(_h_real), plan=pl_, **{GK: 'g2'},
                       seal={GK: 'g2'})
            ln_ = []
            print_followups(Rf, mf_, out=lambda *a, **k: ln_.append(' '.join(map(str, a))))
            gen_ = [l_ for l_ in ln_ if l_.startswith('python3 scripts/lhs_design_dataset.py')]
            rr_ = [l_ for l_ in ln_ if l_.startswith('python3 scripts/g2_network_reread.py')]
            chk('㉛ ★ 후속 명령 — 기대 세대 선언 manifest 면 인계 생성기 둘 다 --tau-batch-manifest <ROOT>/manifest.json · 이름 v13 · '
                '다시 읽기 (g2_network_reread --launcher-root <ROOT>) 명령',
                len(gen_) == 2 and all(f'--tau-batch-manifest {shlex.quote(str(Rf / "manifest.json"))}' in g_ and '_handover_v13_' in g_ for g_ in gen_)
                and len(rr_) == 1 and f'--launcher-root {shlex.quote(str(Rf))}' in rr_[0], repr((gen_, rr_)))
        _scenario('㉛ 후속 명령 시나리오', _s31)

        # ㉜ ★ §7-3 "194 ID · cohort · 원 dump 의 해시" — manifest 입력 지문 (계획 큐 ID · 코호트 · 수확 JSON raw sha256 = 워커 같은 프레임 관문의 대조값) ·
        #   audit 가 다시 계산해 대조한다 (발사 뒤 수확 JSON 의 원자료 sha 가 바뀌면 rc 1)
        def _s32():
            pid = _G.get('plan_input_digest')
            man_ = read_json(tmp / 'run_gen' / 'manifest.json') or {}
            dg_ = man_.get('input_digest') or {}
            chk('㉜ ★ manifest 입력 지문 — 케이스 3 · ID · 원자료 sha256 표 지문 = 계획에서 다시 계산한 값 · 원자료 sha 결손 0',
                bool(pid) and dg_.get('n') == 3 and dg_ == pid(man_.get('plan') or {}) and not dg_.get('missing_raw_sha')
                and len(dg_.get('raw_sha256_table_sha256') or '') == 64, repr(dg_))
            hj = Path(specs['lhsx']['harvest']) / 'lhsx_901.json'
            orig = hj.read_text(encoding='utf-8')
            try:
                j_ = json.loads(orig)
                j_['raw']['atom']['sha256'] = '0' * 64
                hj.write_text(json.dumps(j_), encoding='utf-8')
                rc_a, aj_, _o = _audit_json(tmp / 'run_gen')
            finally:
                hj.write_text(orig, encoding='utf-8')
            rc_b, aj_b, _o = _audit_json(tmp / 'run_gen')
            chk('㉜ ★ audit — 발사 뒤 수확 JSON 의 원자료 sha256 이 바뀌면 rc 1 · input_problems · 되돌리면 rc 0',
                rc_a == 1 and bool(aj_.get('input_problems')) and rc_b == 0 and not aj_b.get('input_problems'),
                repr((rc_a, aj_.get('input_problems'), rc_b, aj_b.get('input_problems'))))
        _scenario('㉜ 입력 지문 시나리오', _s32)

        # ═══ ㉝–㉟ ★ 10-07 Codex 세대 2 재검증 2 (`docs/reviews/codex_review_gen2_network_reverify2_20261007.md`) — 반례 먼저 (옛 코드에서 ✗) ═══════════
        #   ㉝ G2RR2-01 §2 표 — 새 29+ 파일 봉인 · 시도 영수증 · generation_probe 는 남기고 선언만 지운 manifest 가 옛 형식 면제로 통과 (audit rc 0 · retry 세대 관문 []).
        #   ㉞ 역사 형식 = 등록된 옛 실행 (HISTORICAL_LAUNCHES — 형식 + 발사 출처) 만 · 역사 모드 (--historical) 에서만 읽힌다 · retry 불가.
        #   ㉟ G2RR2-03 §4 — 실제 접촉 생산 경로 (analyze_contacts → run_full_analysis → calc_fracture_stages → fracture_model · calc_porosity_union_exact →
        #      lhs_union_webapp) 의 지연 import 가 봉인 밖 · 정적 닫힘 · 지연 import 분류 · 누락 모듈 변이 · 실제 import 관측.
        HL = _G.get('HISTORICAL_LAUNCHES') or {}
        HIST_MAN = ROOT / 'docs' / 'data' / 'lhs_network194_11fcf91e8' / 'manifest.json'

        def _legacy_case_dual(r_, case='lhsx_901'):
            p_ = case_dir(r_, case) / 'work' / 'results' / case / 'network_conductivity_dual.json'
            p_.write_text(json.dumps({'hertzian': {'resistance_model': 'maxwell', 'sigma_full': 0.004},
                                      'physics': {'resistance_model': 'mikic', 'sigma_full': 0.004}}), encoding='utf-8')

        def _s33():
            src_ = tmp / 'run_gen'
            hj = Path(specs['lhsx']['harvest']) / 'lhsx_901.json'
            orig = hj.read_text(encoding='utf-8')

            def _variant(name, edit, atom=False):
                r_ = tmp / f'g2rr2_01_{name}'
                shutil.copytree(src_, r_, symlinks=True)
                m_ = read_json(r_ / 'manifest.json') or {}
                edit(m_, r_)
                write_json(r_ / 'manifest.json', m_)
                try:
                    if atom:
                        j_ = json.loads(orig)
                        j_['raw']['atom']['sha256'] = '0' * 64
                        hj.write_text(json.dumps(j_), encoding='utf-8')
                    rc_, aj_, o_ = _audit_json(r_)
                finally:
                    hj.write_text(orig, encoding='utf-8')
                return r_, rc_, aj_, o_

            def _del_gen(m_):
                m_.pop(GK, None)
                (m_.get('seal') or {}).pop(GK, None)
            rows = {
                '양성 control': (_variant('ctrl', lambda m_, r_: None), 0),
                '수확 JSON atom SHA 만 변경': (_variant('atom', lambda m_, r_: None, atom=True), 1),
                '같은 변경 + input_digest 삭제': (_variant('atom_del', lambda m_, r_: m_.pop('input_digest', None), atom=True), 'nz'),
                '같은 변경 + input_digest=null': (_variant('atom_null', lambda m_, r_: m_.update(input_digest=None), atom=True), 'nz'),
                '케이스 dual 옛 모양 · 기대 세대 g2 유지': (_variant('legacy', lambda m_, r_: _legacy_case_dual(r_)), 1),
                '같은 옛 레코드 + top/seal 기대 세대 두 키 삭제': (_variant('legacy_gen_del', lambda m_, r_: (_legacy_case_dual(r_), _del_gen(m_))), 'nz'),
                'seal 통째 삭제 (generation_probe · 새 해시 · input_digest 남김)': (_variant('seal_del', lambda m_, r_: m_.pop('seal', None)), 'nz'),
                'generation_probe 삭제': (_variant('probe_del', lambda m_, r_: m_.pop('generation_probe', None)), 'nz'),
                'launch_format 삭제': (_variant('fmt_del', lambda m_, r_: m_.pop('launch_format', None)), 'nz'),
                'input_digest 의 raw 표 지문 키 삭제': (_variant('raw_key_del', lambda m_, r_: (m_.get('input_digest') or {}).pop('raw_sha256_table_sha256', None)), 'nz'),
            }
            bad = {k: (v[0][1], v[1]) for k, v in rows.items() if not (v[0][1] != 0 if v[1] == 'nz' else v[0][1] == v[1])}
            chk('㉝ ★ G2RR2-01 Codex §2 표 — 새 manifest 의 필수 선언 (input_digest · 기대 세대 · seal · generation_probe · 형식) 삭제 · null = audit 비영 · '
                '양성 control rc 0 · 원래 반례 (atom SHA · 옛 레코드) rc 1 유지 (옛: 삭제 · null · 두 키 삭제 = rc 0)', not bad, repr(bad))
            elig = {k: (v[0][2].get('eligibility') or {}).get('kind') for k, v in rows.items()}
            chk('㉝ audit JSON 의 자격 — control · 원래 반례 = current · 선언을 지운 것 = invalid (옛 형식으로 추론하지 않는다)',
                all(elig[k] == 'current' for k in ('양성 control', '수확 JSON atom SHA 만 변경', '케이스 dual 옛 모양 · 기대 세대 g2 유지'))
                and all(elig[k] == 'invalid' for k, v in rows.items() if v[1] == 'nz'), repr(elig))
            r_del = rows['같은 옛 레코드 + top/seal 기대 세대 두 키 삭제'][0][0]
            gb_, _gn = generation_gate(read_json(r_del / 'manifest.json'), ROOT)
            snap_ = _snap(r_del)
            with _patch(git_info=_git_fake()):
                rc_r, o_r = _main_rc(['retry', '--root', str(r_del), *L20, '--allow-mixed-generation', '--allow-dirty'])
            chk('㉝ ★ retry 세대 관문 — 같은 manifest (기대 세대 두 키 삭제) 를 generation_gate 에 넣으면 막는 사유가 있다 · 실제 retry rc 2 · 아무것도 안 돈다 '
                '(넘김으로도 못 넘긴다 · 옛: 막는 사유 [])', bool(gb_) and rc_r == 2 and _snap(r_del) == snap_, repr((gb_, rc_r, o_r[-200:])))

        _scenario('㉝ G2RR2-01 필수 선언 시나리오', _s33)

        def _hist_root(name, *, cases=(), edit=None, plan=None):
            """등록된 옛 실행 (10-05 · 11fcf91e8) 의 manifest 바이트 그대로 + (선택) 케이스 기록 — 옛 실행기가 남긴 모양 (worker.json · out/status.json ·
            runs/run_001.json).  plan = 계획만 바꿀 때 (등록 형식 · 발사 출처는 그대로)."""
            r_ = tmp / name
            r_.mkdir()
            m_ = json.loads(HIST_MAN.read_text(encoding='utf-8'))
            if plan is not None:
                m_['plan'] = plan
            if edit:
                edit(m_)
            write_json(r_ / 'manifest.json', m_)
            shutil.copytree(HIST_MAN.parent / 'runs', r_ / 'runs')
            gsha = (m_.get('git') or {}).get('sha')
            for c in cases:
                e_ = next(x for x in m_['plan']['queue'] if x['case'] == c)
                cs_ = next(x for x in m_['plan']['cohorts'] if x['name'] == e_['cohort'])
                w_ = read_json(HIST_MAN.parent / 'cases' / c / 'worker.json') or {}
                write_json(case_dir(r_, c) / 'worker.json', w_)
                at_ = (w_.get('attempts') or [{}])[-1]
                st_ = dict(schema=LWB.SCHEMA, stop_after='network', harvest_dir=cs_['harvest_dir'], cohort=cs_['cohort'],
                           cases={c: dict(case=c, stop_after='network', status=at_.get('outcome'), failed_stages=[],
                                          network_run_id=at_.get('network_run_id'))}, runs=[dict(git_sha=gsha, dirty=False)])
                LWB.write_outputs(case_dir(r_, c) / 'out', st_, {c: dict(case=c)})
            return r_

        def _s34():
            hv_ = _G.get('launch_eligibility')
            m0 = json.loads(HIST_MAN.read_text(encoding='utf-8'))
            e0 = hv_(m0) if hv_ else {}
            chk('㉞ 등록된 옛 실행 — 커밋된 10-05 manifest (11fcf91e8 · 19 파일 · seal 없음) = 역사 형식 (historical) · 등록 이름 · 문제 0',
                e0.get('kind') == 'historical' and e0.get('historical') in HL and not e0.get('problems'), repr(e0))
            rh_ = _hist_root('hist_ok', cases=('lhs00_000', 'lhsx_061'))
            rc_n, aj_n, o_n = _audit_json(rh_)
            jp_ = tmp / 'audit_hist_mode.json'
            rc_h, o_h = _main_rc(['audit', '--root', str(rh_), '--historical', '--json', str(jp_)])
            aj_h = read_json(jp_) or {}
            vh_ = collections.Counter(r_.get('verdict') for r_ in aj_h.get('cases') or [])
            chk('㉞ ★ 진짜 역사 ROOT — audit (기본) = 비영 (역사 형식은 역사 모드에서만) · audit --historical = rc 0 · 기록 둘 SEALED_LEGACY · 나머지 NO_RECORD · '
                '자격 historical (세대 · 입력 지문 대조 없음 표지)',
                rc_n != 0 and '역사' in o_n and rc_h == 0 and vh_.get('SEALED_LEGACY') == 2 and vh_.get('NO_RECORD') == len(m0['plan']['queue']) - 2
                and (aj_h.get('eligibility') or {}).get('kind') == 'historical', repr((rc_n, o_n[-160:], rc_h, dict(vh_), o_h[-200:])))
            bad = {}
            for nm_, ed_ in (('코드 해시 하나 바뀜', lambda m_: m_['code_hashes'].update({'scripts/network_conductivity.py': '0' * 64})),
                             ('발사 git sha 다름', lambda m_: m_['git'].update(sha='f' * 40)),
                             ('기대 세대 키 하나 덧붙임', lambda m_: m_.update({GK: 'g2'})),
                             ('input_digest 덧붙임 (null)', lambda m_: m_.update(input_digest=None)),
                             ('키 하나 삭제 (preflight)', lambda m_: m_.pop('preflight', None)),
                             ('세 번째 코호트', lambda m_: m_['plan']['cohorts'].append(dict(m_['plan']['cohorts'][0], name='lhsz')))):
                r_ = _hist_root(f'hist_bad_{len(bad)}_{time.monotonic_ns()}', edit=ed_)
                rc_v, _o = _main_rc(['audit', '--root', str(r_), '--historical'])
                if rc_v == 0:
                    bad[nm_] = rc_v
            chk('㉞ ★ 등록과 다른 옛 모양 — 코드 해시 · 발사 sha · 새 형식 키 덧붙임 · 키 삭제 · 모르는 코호트 → audit --historical 도 비영 (필드 모양으로 역사를 추론하지 않는다)',
                not bad and len(HL) >= 1, repr(bad))
            snap_ = _snap(rh_)
            with _patch(git_info=lambda *a, **k: dict(sha=m0['git']['sha'], short=m0['git']['sha'][:9], dirty=False, porcelain=[])):
                rc_r, o_r = _main_rc(['retry', '--root', str(rh_), *L20, '--allow-mixed-generation', '--allow-dirty'])
            chk('㉞ 역사 ROOT 의 retry = rc 2 · 아무것도 안 돈다 (그 ROOT 의 커밋 실행기로 — 넘김 불가)', rc_r == 2 and _snap(rh_) == snap_ and '역사' in o_r,
                repr((rc_r, o_r[-200:])))

        _scenario('㉞ 역사 형식 시나리오', _s34)

        def _s35():
            FM, LU = 'scripts/fracture_model.py', 'scripts/lhs_union_webapp.py'
            cdc = _G.get('code_dependency_closure')
            clo = cdc(ROOT) if cdc else {}
            chk('㉟a ★ G2RR2-03 — 정적 닫힘에 실제 접촉 생산 경로의 지연 import (dem_analysis_core → fracture_model · lhs_union_webapp) 가 있다 · 닫힘 ⊆ CODE_FILES '
                '(옛: 닫힘 27 ⊆ 29 — fracture_model 이 목록 밖)',
                FM in (clo.get('files') or []) and LU in (clo.get('files') or []) and FM in CODE_FILES and LU in CODE_FILES
                and not [f for f in clo.get('files') or [] if f not in CODE_FILES] and not clo.get('errors'),
                repr((sorted(set(clo.get('files') or []) - set(CODE_FILES)), clo.get('errors'))))
            lic = _G.get('lazy_import_census')
            cen = lic(ROOT) if lic else {'unclassified': ['(분류 함수 없음)']}
            alt = tmp / 'census_alt'
            for rel in set(CODE_FILES) | {FM, LU}:
                (alt / rel).parent.mkdir(parents=True, exist_ok=True)
                if (ROOT / rel).is_file():
                    shutil.copyfile(ROOT / rel, alt / rel)
            (alt / 'scripts' / 'viewer3d_data.py').write_text('# 봉인 밖 모듈 (selftest)\n', encoding='utf-8')
            p_ = alt / 'scripts' / 'dem_analysis_core.py'
            p_.write_text(p_.read_text(encoding='utf-8') + '\n\ndef _selftest_new_lazy():\n    import viewer3d_data  # selftest — 새 지연 import\n',
                          encoding='utf-8')
            cen2 = lic(alt) if lic else {'unclassified': []}
            chk('㉟b ★ 지연 import 분류 — 봉인 파일의 함수 안 import 중 봉인 밖 모듈은 전부 경로 밖 (DEP_LAZY_OFFPATH · 사유) 으로 분류됐다 · 새 지연 import '
                '(dem_analysis_core → viewer3d_data) 는 분류 밖으로 잡힌다 (발사 사전 점검 중단 사유)',
                not cen.get('unclassified') and any(u[0] == 'scripts/dem_analysis_core.py' and u[2] == 'scripts/viewer3d_data.py'
                                                    for u in cen2.get('unclassified') or []),
                repr((cen.get('unclassified'), cen2.get('unclassified'))))
            # 누락 모듈 변이 (Codex dependency_gap) — 워커 체크아웃 사본의 fracture_model K_IC_AM_P 0.3 → 30 MPa·m^0.5
            altc = tmp / 'frac_alt'
            for rel in set(CODE_FILES) | {FM, LU}:
                (altc / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / rel, altc / rel)
            fp0 = code_fp(code_hashes(altc))
            q_ = altc / FM
            q_.write_text(q_.read_text(encoding='utf-8').replace('K_IC_AM_P = 0.3e6', 'K_IC_AM_P = 30e6', 1), encoding='utf-8')
            fp1 = code_fp(code_hashes(altc))
            man_f = dict(read_json(tmp / 'run_gen' / 'manifest.json') or {}, repo_root=str(altc))
            with _patch(git_info=lambda *a, **k: dict(sha=(man_f.get('git') or {}).get('sha'), short='x', dirty=False, porcelain=[])):
                sg_ = seal_gate(man_f)
            import importlib.util as _ilu

            def _frac(path):
                spec_ = _ilu.spec_from_file_location(f'_fm_{time.monotonic_ns()}', path)
                mod_ = _ilu.module_from_spec(spec_)
                spec_.loader.exec_module(mod_)
                import dem_analysis_core as _dac
                saved_ = sys.modules.get('fracture_model')
                sys.modules['fracture_model'] = mod_
                try:
                    A_ = {1: dict(type=1, x=0.0, y=0.0, z=0.0, radius=0.006), 2: dict(type=1, x=0.0, y=0.0, z=0.0118, radius=0.006)}
                    return _dac.calc_fracture_stages(A_, [dict(id1=1, id2=2, delta=0.0002)], {1: 'AM_P'}, scale=1000.0)
                finally:
                    if saved_ is None:
                        sys.modules.pop('fracture_model', None)
                    else:
                        sys.modules['fracture_model'] = saved_
            f0, f1 = _frac(ROOT / FM), _frac(q_)
            chk('㉟c ★ 누락 모듈 변이 (Codex dependency_gap) — 사본의 K_IC_AM_P 0.3 → 30: 실제 calc_fracture_stages frac_multicrack_pct 100 → 0 (의존 연결) · '
                '지문 code_fp 가 바뀐다 · 그 체크아웃으로 retry 시작 관문 = 봉인과 다른 파일 fracture_model (옛: 지문 그대로 f3f54951…) · 정상 모듈 값 보존',
                f0.get('frac_multicrack_pct') == 100.0 and f0.get('frac_intact_pct') == 0.0 and f1.get('frac_multicrack_pct') == 0.0
                and f1.get('frac_intact_pct') == 100.0 and fp0 and fp1 and fp0 != fp1 and FM in (sg_.get('changed') or []) and bool(sg_.get('mixed')),
                repr((f0.get('frac_multicrack_pct'), f1.get('frac_multicrack_pct'), fp0 == fp1, sg_.get('changed'))))
            # 실제 import 관측 — 생산 경로 (합성 침대 se_am · 실제 웹앱 run_pipeline(stop_after='network') · 단계 하위 프로세스 전부) 의 모든 Python 프로세스가
            #   끝날 때 sys.modules 의 리포 파일을 적는다 (sitecustomize · PYTHONPATH — 하위 프로세스도 환경을 물려받는다)
            obs = tmp / 'import_obs'
            _ioe, _ioo = _G.get('import_obs_env'), _G.get('import_observation')
            spec_c = dict(id='obs_network', kind='synthetic', bed='se_am', type_map='1:SE,2:AM_P', scale=1, stop='network', root=str(obs / 'root'))
            (obs / 'root' / 'cases' / 'obs_network').mkdir(parents=True)
            spec_p = obs / 'spec.json'
            write_json(spec_p, spec_c)
            env_ = dict(os.environ, **THREAD_ENV, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(obs), MPLBACKEND='Agg', **(_ioe(obs, ROOT) if _ioe else {}))
            rp_ = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'wsl_network_smoke.py'), '--_child', str(spec_p)], cwd=str(obs / 'root'),
                                 env=env_, capture_output=True, text=True, timeout=900)
            rep_ = read_json(obs / 'root' / 'cases' / 'obs_network' / 'report.json') or {}
            io_ = _ioo(obs, ROOT) if _ioo else dict(files=[], observed=[], outside=['(관측 함수 없음)'])
            seen, outside, _obs_py = set(io_['files']), io_['outside'], io_['observed']
            stages_ = [s_.get('step') for s_ in rep_.get('stages') or []]
            chk(f'㉟d ★ 실제 import 관측 — 생산 → 게시 경로 (합성 se_am · run_pipeline stop_after network = {rep_.get("status")!r} · 단계 {len(stages_)} · 프로세스 '
                f'{len(list((obs / "log").glob("*.txt")))}) 가 읽은 리포 모듈 {len(_obs_py)} ⊆ 봉인 CODE_FILES {len(CODE_FILES)} (시험 도구 둘 제외) · fracture_model · '
                f'lhs_union_webapp 이 실제로 읽혔다 (경로가 돌았다) (옛: 봉인 밖 fracture_model · lhs_union_webapp · ml_design_structure) {outside or ""}',
                rp_.returncode == 0 and rep_.get('status') == 'done' and not outside and FM in seen and LU in seen
                and 'scripts/network_conductivity.py' in seen and 'scripts/lens_geometry.py' in seen,
                repr((rp_.returncode, rep_.get('status'), outside, sorted(seen)[:40], (rp_.stderr or '')[-300:])))

        _scenario('㉟ G2RR2-03 전이 의존 시나리오', _s35)

        def _s35e():
            # 시범의 실제 import 관측 (`run --observe-imports`) — 진짜 실행기 · 진짜 lhs_webapp_batch (가짜 웹앱 의존) 의 모든 프로세스 · audit 가 봉인 ⊇ 관측을 본다
            set_plan({})
            os.environ['NP194_FAKE_DIRTY'] = '0'
            Ro, Rx = tmp / 'run_obs', tmp / 'run_obs_extra'
            with _patch(git_info=_git_fake()):
                rc_o, o_o = _main_rc(args_for(Ro, '--cohorts', 'lhsx', '--case', 'lhsx_900', *L20, '--observe-imports', allow_dirty=False))
                rc_a, aj_, _o = _audit_json(Ro)
                os.environ['NP194_FAKE_EXTRA_IMPORT'] = 'coating_presets'
                try:
                    rc_x, _ox = _main_rc(args_for(Rx, '--cohorts', 'lhsx', '--case', 'lhsx_900', *L20, '--observe-imports', allow_dirty=False))
                finally:
                    os.environ.pop('NP194_FAKE_EXTRA_IMPORT', None)
                rc_ax, ajx_, _o = _audit_json(Rx)
            io_ = aj_.get('import_observation') or {}
            iox_ = ajx_.get('import_observation') or {}
            chk('㉟e ★ 시범 import 관측 (run --observe-imports) — 진짜 워커 (lhs_webapp_batch) 프로세스의 리포 import 가 적힌다 · audit rc 0 · 봉인 밖 0 / '
                '워커가 봉인 밖 모듈 (coating_presets) 을 읽으면 audit rc 1 · 그 파일이 관측 문제로 남는다',
                rc_o == 0 and rc_a == 0 and io_.get('n_processes', 0) >= 1 and 'scripts/lhs_webapp_batch.py' in (io_.get('observed') or [])
                and not io_.get('outside') and (read_json(Ro / 'manifest.json') or {}).get('observe_imports') is True
                and rc_x == 0 and rc_ax == 1 and iox_.get('outside') == ['scripts/coating_presets.py'],
                repr((rc_o, rc_a, io_.get('n_processes'), io_.get('outside'), rc_x, rc_ax, iox_.get('outside'), o_o[-200:])))

        _scenario('㉟e 시범 import 관측 시나리오', _s35e)
    finally:
        for k, v in env_keep.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'\n{"✓ 전부 통과" if not fails else f"✗ {len(fails)} 건 실패"}')
    return 0 if not fails else 1


def _raises(fn, exc) -> bool:
    try:
        fn()
    except exc:
        return True
    except Exception:                                       # noqa: BLE001
        return False
    return False


if __name__ == '__main__':
    sys.exit(main())
