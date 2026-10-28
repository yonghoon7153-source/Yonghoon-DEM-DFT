#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""50kg Q5 가지 덱 생성기 — 정착 끝 (after_settling) 체크포인트에서 dt ↔ dt/2 · 감쇠 가지 (등록 Q11 · 창 W1) +
창 W2 (등록 §12-2 = 개정 초안 · 비준 전) + D3 로컬 직렬 러너 (등록 §12-3 · 1저자 10-28).

등록 = `docs/50kg/kg50_q5_dt_damping_registration_draft_20261027.md` (1저자 10-27 밤 비준 · Q1–Q12 = 머리 비준 표 · §12 = 10-28 개정).
  §2 침대 · 지점 — kg50_d07_b50 (v3 덱 · ibb) · kg50_d3_b50_s1 (v2 덱 · hit) · 체크포인트 restart_<case>/restart_after_settling.bin
       (step 200001 · 본 덱 170 행 write_restart)
  §3 가지 — A 본 덱 그대로 · B dt 1 µs → 0.5 µs (step 으로 센 수 ×2) · C 안정화 감쇠의 SE 몫만 γ_SE = 0.5·s
       (Q2 (가) AM 기준 s = m_SE/m_AM) · F = A 덱 그대로 · NP 만 다름 · D3 = A3 · C3 · F3 (같은 꼴 · B3 없음)
  Q5 NP — A · B · C 56 · F 28 · A3 · C3 1 · F3 2
  §4 덱 줄 — 뼈대 §4-1 · B §4-2 · C §4-3 · 출력 줄 §4-5 (덤프 간격 Q12 = W1 atom 66,667 · contact 200,001)
  창 W2 — §12-2 (⬜ 개정 초안 · 비준 전) 대로: D0.7-50 만 · 본 런 압축 체크포인트 restart_compress_<N>.bin 에서 고정 길이
       run (A · C · F 300,000 · B 600,000) · N = 본 런 로그에서 계산 (§12-2 (라) · `--main-log` · 사람이 고르지 않는다) ·
       덤프 atom 10,000 · contact 100,000 · 판 STL = 200 행 그대로 (파일 = 본 런 mesh_<N>.stl 사본) · 비준 전이면 덱 머리 ·
       manifest · 화면에 "개정 초안 · 비준 전" + 운영자 제출 줄을 막는다 (판독기는 비준 전 판으로 만든 W2 가지를 거부한다).
  host — §12-3 (1저자 10-28): D3 A3 · C3 만 `--host wsl` = 로컬 WSL 직렬 LIGGGHTS 1 코어 (mpirun · MPI 빌드를 쓰지 않는다 ·
       바이너리 = 환경 변수 LMP_SERIAL · 없으면 $HOME/src/LIGGGHTS-PUBLIC/src/lmp_serial · 그것도 없으면 PATH 의 lmp_serial) ·
       덱 = hit 덱과 바이트 같음 · 러너만 다름 · F3 = hit NP 2 · D1 끝난 뒤 (로컬은 거부).

하는 일 (본 덱 · 체크포인트 · 원 폴더는 읽기만 · 바꾸지 않는다):
  ⓪ 등록 문서의 고정 줄 (§2 · §4 표 · 머리 비준 표 · §8 · §12) = 이 파일의 상수 — 다르면 거부 (결과 뒤 등록 이동 차단)
  ① 본 덱 sha256 = 그 덱 묶음 manifest.json 의 deck_sha256 (v3 · v2) — 다르면 거부
  ② 본 덱의 고정 줄 (행 번호 + 내용) · 뺄 구역의 명령 꼴 · 끝 구역 명령 꼴 확인 — 다르면 거부 (어느 행 · 어느 § 인지 적는다)
  ③ 가지 덱 = 본 덱을 줄 단위로 그대로 옮기고 등록된 줄만 바꿈 (§4-1 · §4-2 · §4-3 · §4-5 · W2 = §12-2 (가))
  ④ 허용 목록 대조 — 가지 덱 명령 (LIGGGHTS 줄 규칙 · resume_ckpt.sh 의 deck() 와 같음) ↔ 본 덱 명령에 등록 바꿈만
       적용한 목록 · 줄 단위로도 본 덱 줄 그대로인지 — 한 글자라도 다르면 거부 (파일을 하나도 쓰지 않는다)
  ⑤ A · F · A3 · F3 = `resume_ckpt.sh -C` 정적 대조 문제가 정확히 하나 (§8-1: 재개 지점 뒤 순서 줄 수 12 ↔ 0 · rc 1) ·
       W2 A · F = 정확히 둘 (§12-2 (마))
  ⑥ 러너 = 리포 러너 렌더 (`make_se_size_decks.render_ibb_runner` · `hit_command`) — ibb 러너는 본 러너와
       job-name · output · -n · cd · mpirun 다섯 줄만 다르다 · `#SBATCH -n N` ↔ `mpirun … -np N` 짝 (N = Q5) ·
       로컬 (§12-3) = 생성기 글자 그대로 (직렬 · 검사 · 바이너리 기록 q5_binary.txt)
  ⑦ 쓰기 = 새 폴더 하나 (<out>/q5_<case>_<가지>/ · W2 q5w2_… · 로컬 …_wsl · 이미 있으면 거부) · 가지 덱 · 러너 · 본 덱 사본 ·
       (W2 = 본 런 로그 사본) · q5_manifest.json (입력 · 출력 sha256) · SHA256SUMS — 임시 폴더에 다 쓴 뒤 이름 바꾸기 (거부 = 파일 0)
  ⑧ 체크포인트 (W2 = + 판 STL) 복사 · sha256 = 운영자 몫 — 정확한 cp · sha256sum 줄을 화면 · manifest 에 낸다 (같아야 제출)

물리 숫자는 새로 만들지 않는다 — 바뀌는 값 (dt 5.0e-7 · run 2 · 400000 · thermo 2 · 2000 · mesh 10000 · s 5.3696e-4 ·
  4.2268e-2 · 덤프 간격 66667 · 200001 · NP · W2 run 300000 · 600000 · dmp_atom 100000 · 덤프 10000 · 100000) 은 전부 등록
  문서 그대로이고, 본 덱 값 (dt 1.0e-6 · 밀도 · 반지름 · run 길이) 으로 맞는지 다시 센다 (dt/2 · step ×2 · s 다섯 자리).
자리 표시 둘의 읽기: §4-1 `read_restart <가지 폴더>/…` = 러너가 cd 하는 가지 폴더 기준 상대 경로 · §4-5 덤프 `<폴더>` =
  본 덱 153 행이 만드는 `post_<case>/` (따로 `shell mkdir` 줄을 더하지 않으려고).
★ B 의 dt 줄 (43 행) 은 read_restart 앞에 있다 — LIGGGHTS 3d5c00f 의 restart 머리에는 dt 가 없고 units 가 같으면
  재설정하지 않는다 (Codex 증거 사본 upstream_src_write_restart.cpp · upstream_src_read_restart.cpp · selftest ⓪b 가 본다)
  → 43 행 바꿈이 살아 있다.  판독기는 로그의 `timestep 5e-07` 치환 줄로 다시 확인한다.

사용 (WSL · 리포 안 · 아무것도 띄우지 않는다)
    python3 scripts/kg50_q5_branches.py --case kg50_d07_b50 --branch A --np 56 --out ~/q5_build
    python3 scripts/kg50_q5_branches.py --case kg50_d3_b50_s1 --branch A3 --np 1 --host wsl --out ~/q5_local
    python3 scripts/kg50_q5_branches.py --case kg50_d07_b50 --branch A --np 56 --window W2 --main-log <본 런 log> --out ~/q5_build
    python3 scripts/kg50_q5_branches.py --verify ~/q5_build/q5_kg50_d07_b50_A
    python3 scripts/kg50_q5_branches.py --selftest
웹앱 화면 없음 (일회성 등록 대조 도구 · 판정은 scripts/kg50_q5_verdict.py).
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SCHEMA = 'kg50_q5_branch/v1'
REGISTRATION = 'docs/50kg/kg50_q5_dt_damping_registration_draft_20261027.md'
RESUME_TOOL = 'scripts/resume_ckpt.sh'
RUNNER_TEMPLATE = 'docs/data/pure_se_r075_20260927/run_pse_r075_a_r30.sh'
RUNNER_TEMPLATE_CASE = 'pse_r075_a'
EVIDENCE_DIR = 'docs/reviews/codex_kg50_decks_review_20261026/evidence/kg50_restart'

#: §2 침대 · 지점 — 이 둘뿐 (본 비교의 D3 자리 = v2 kg50_d3_b50_s1 · v3 README · 새 결정 아님)
CASES = {
    'kg50_d07_b50': dict(
        bed='D0.7-50', host='ibb', branches=('A', 'B', 'C', 'F'),
        deck='docs/data/kg50_decks_20261027_v3_b50/kg50_d07_b50/input_kg50_d07_b50.liggghts',
        deck_manifest='docs/data/kg50_decks_20261027_v3_b50/manifest.json',
        main_runner='docs/data/kg50_decks_20261027_v3_b50/kg50_d07_b50/run_kg50_d07_b50.sh',
        run_root='~/dem_test', main_folder='~/dem_test/kg50_d07_b50', s='5.3696e-4'),
    'kg50_d3_b50_s1': dict(
        bed='D3-50 s1', host='hit', branches=('A3', 'C3', 'F3'),
        deck='docs/data/kg50_decks_20261026_v2/kg50_d3_b50_s1/input_kg50_d3_b50_s1.liggghts',
        deck_manifest='docs/data/kg50_decks_20261026_v2/manifest.json',
        main_runner=None,
        run_root='~/simulation', main_folder='~/simulation/kg50_d3_b50_s1', s='4.2268e-2'),
}
#: Q5 — NP (A · B · C 56 · F 28 · D3 A3 · C3 1 · F3 2)
NP = {'A': 56, 'B': 56, 'C': 56, 'F': 28, 'A3': 1, 'C3': 1, 'F3': 2}
#: §3 가지 꼴 — base (본 덱 그대로) · dt_half (§4-2) · damp (§4-3) · floor (= base 덱 · NP 만 다름)
KIND = {'A': 'base', 'B': 'dt_half', 'C': 'damp', 'F': 'floor', 'A3': 'base', 'C3': 'damp', 'F3': 'floor'}
KIND_KO = {'base': '본 덱 그대로 (A · F 같은 덱 · F = NP 만 다름)', 'floor': '본 덱 그대로 (A · F 같은 덱 · F = NP 만 다름)',
           'dt_half': 'dt 1 µs → 0.5 µs · step 으로 센 수 ×2 (§4-2)',
           'damp': '안정화 감쇠의 SE 몫만 γ_SE = 0.5·s (§4-3 · Q2 (가) AM 기준)'}

S0 = 200001                       # §2 체크포인트 step (본 덱 run 1 + run 200000 · 170 행 write_restart)
MAIN_NLINES = 257                 # 두 본 덱의 행 수 (§2 "두 덱은 이 문서가 쓰는 줄의 번호가 같다")
ATOM_EVERY, CONTACT_EVERY = 66667, 200001          # Q12 · §4-5 (W1)
ATOM_COLS = ('id', 'type', 'x', 'y', 'z', 'radius', 'vx', 'vy', 'vz')
CONTACT_COLS = tuple('c_cpl[%d]' % i for i in range(1, 27))
TYPE_MAP = {1: 'AM', 2: 'AM', 3: 'SE'}             # 본 덱 55 행 (Type 1:AM_P, 2:AM_S, 3:SE) · §4-3 "type 3 = SE" · "AM (type 1)"
SE_TYPE = 3
WINDOW_S = {'W1': '0.200001', 'W2': '0.3'}         # Q3 (나) — W1 = 판 높이 1 µs + 안정화 0.2 s · W2 = 0.3 s (판 3 µm)
DT_HALF = '5.0e-7'                                 # §4-2 43 행
EXPECTED_STATIC_PROBLEM = '재개 지점 뒤 순서 줄 수 다름: 본 덱 12 ↔ 재개 덱 0'    # §8-1 (옛 도구 출력 · 10-28 밤 §12-4 가 앞선다 · 역사)
HEADER_END = '# ===== (q5 머리 끝) ====='

#: §4-1 뼈대 — 본 덱 행 → 가지에서.  뺄 행 · 바꿀 행 · 넣을 자리 (행 뒤)
DROP_LINES = frozenset([50] + list(range(116, 151)) + [167, 170] + list(range(214, MAIN_NLINES + 1)))
READ_RESTART_LINE = 49
RESTART0_LINE = 165
INSERT_DUMPS_AFTER = 171          # §4-5 "read_restart 뒤 · 172 행 앞"
INSERT_UNDUMPS_AFTER = 213        # §4-5 "213 행 뒤"
#: §4-2 B — (행, A 명령, B 명령) · 203 행 = dump dmp_mesh … 5000 … → … 10000 …
B_EDITS = (
    (43, 'variable dt equal 1.0e-6', 'variable dt equal 5.0e-7'),
    (173, 'thermo 1', 'thermo 2'),
    (174, 'run 1', 'run 2'),
    (203, 'dump dmp_mesh all mesh/stl 5000 post_{case}/mesh_*.stl top_mesh',
     'dump dmp_mesh all mesh/stl 10000 post_{case}/mesh_*.stl top_mesh'),
    (212, 'thermo 1000', 'thermo 2000'),
    (213, 'run 200000', 'run 400000'),
)
#: §4-3 C — 208 행
C_EDIT = (208, 'fix damp all viscous 0.5', 'fix damp all viscous 0.5 scale 3 {s}')

#: ── §12-2 창 W2 (⬜ 개정 초안 · 비준 전) — §4-1 뼈대에서 (가) 표만 다르다 ──
W2_CASES = ('kg50_d07_b50',)      # §5 W2 표 = D0.7 넷 (질문 W2-6)
W2_DROP = frozenset([50] + list(range(116, 151)) + [167, 170] + list(range(172, 198)) + [213]
                    + list(range(225, MAIN_NLINES + 1)))
W2_RESTART0_LINES = (RESTART0_LINE, 222)                       # 165 · 222 → restart 0 (가지는 restart 파일을 안 쓴다)
W2_RUN_LINE = 224                                               # label loop_press → run 300000 (B 600000) · 225–228 뺌
W2_RUN = {'base': 300000, 'floor': 300000, 'damp': 300000, 'dt_half': 600000}
W2_THERMO = {'base': 1000, 'floor': 1000, 'damp': 1000, 'dt_half': 2000}
W2_ATOM_EVERY, W2_CONTACT_EVERY = 10000, 100000                # Q12 (atom) · §12-2 (나) (contact · ⬜ W2-2)
#: §12-2 B — W2 A 에서 바뀌는 줄 (W1 의 173 · 174 · 213 은 W2 덱에 없다 · run 줄은 224 자리)
W2_B_EDITS = (
    (43, 'variable dt equal 1.0e-6', 'variable dt equal 5.0e-7'),
    (203, 'dump dmp_mesh all mesh/stl 5000 post_{case}/mesh_*.stl top_mesh',
     'dump dmp_mesh all mesh/stl 10000 post_{case}/mesh_*.stl top_mesh'),
    (212, 'thermo 1000', 'thermo 2000'),
    (217, 'dump dmp_atom all custom 50000 post_{case}/atom_*.liggghts id type x y z radius vx vy vz c_strs[1] c_strs[2] c_strs[3] c_ke',
     'dump dmp_atom all custom 100000 post_{case}/atom_*.liggghts id type x y z radius vx vy vz c_strs[1] c_strs[2] c_strs[3] c_ke'),
)
W2_CKPT_EVERY = 200000            # 본 덱 222 행 restart 간격
W2_N_MIN = 600000                 # 압축 시작 400,002 (= 200,001 + 1 + 200,000) 뒤 첫 restart_compress
W2_LOG_FIRST, W2_LOG_EVERY = 201000, 1000                      # §12-2 (라) 5 — 201,000 … N 의 1,000 배수 줄
W2_LOG_ECHO = ('timestep 1e-06', 'fix damp all viscous 0.5', 'fix move_press all move/mesh mesh top_mesh linear 0.0 0.0 -0.01',
               'restart 200000 restart_{case}/restart_compress_*.bin', '====== PHASE 3: COMPRESSION (Speed 0.01) ======')
W2_PREFIX = 'q5w2_'
#: §12-2 (마) — W2 A · F 정적 대조 문제 = 정확히 이 둘 (실제 도구 출력 · rc 1)
EXPECTED_STATIC_PROBLEMS_W2 = (
    '루프 몸 run 다름 (반복 안 restart 체크포인트 · 10-28 KG50-19): 본 덱 [label loop_press] [run 5000] ↔ 재개 덱 read_restart 뒤 '
    '[run 300000]',
    '재개 지점 뒤 순서 줄 수 다름: 본 덱 8 ↔ 재개 덱 0')
#: §12-4 (1저자 10-28 밤 Q5-S1) — 고친 재개 도구 (KG50R-01–05 · 전체 프로그램 대조 · 압축 체크포인트 거부) 의 `-C` 출력 = 정확히 이 줄 · 이 순서 (rc 1).
#   <case> = 케이스 이름 · <N> = W2 시작 step.  §8-1 의 한 줄 · §12-2 (마) 의 둘 (위 두 상수) = 옛 도구 출력 (역사 · 이 절이 앞선다).
EXPECTED_STATIC_W1 = (
    '체크포인트 뒤 ~ 첫 긴 run 앞 명령 다름 (10-28 KG50R-03 · 명령 하나하나): 본 덱 35 개 ↔ 재개 덱 37 개 — 재개 덱에만 [dump dq5a all custom 66667 post_<case>/q5atom_*.liggghts id type x y z radius vx vy vz] [dump dq5c all local 200001 post_<case>/q5contact_*.liggghts c_cpl[1] c_cpl[2] c_cpl[3] c_cpl[4] c_cpl[5] c_cpl[6] c_cpl[7] c_cpl[8] c_cpl[9] c_cpl[10] c_cpl[11] c_cpl[12] c_cpl[13] c_cpl[14] c_cpl[15] c_cpl[16] c_cpl[17] c_cpl[18] c_cpl[19] c_cpl[20] c_cpl[21] c_cpl[22] c_cpl[23] c_cpl[24] c_cpl[25] c_cpl[26]]',
    '첫 긴 run 뒤 명령 다름 (10-28 KG50R-03 · 명령 하나하나): 본 덱 27 개 ↔ 재개 덱 2 개 — 바뀜 [print "====== PHASE 3: COMPRESSION (Speed 0.01) ======"] [dump dmp_atom all custom 50000 post_<case>/atom_*.liggghts id type x y z radius vx vy vz c_strs[1] c_strs[2] c_strs[3] c_ke] → [undump dq5a] [undump dq5c]',
    '재개 지점 restart 다름: 본 덱 [restart 50000 restart_<case>/restart_settling_*.bin] ↔ 재개 덱 [restart 0]',
)
EXPECTED_STATIC_W2 = (
    '압축 체크포인트 재개 = 지원 안 함 (KG50R-01 · 1저자 10-28 Q3 (가)) — 체크포인트 restart_compress_<N>.bin (이름 restart_compress_*)',
    '첫 긴 run 다름 (반복 안 restart 체크포인트 · 10-28 KG50R-01): 본 덱 [run 5000] ↔ 재개 덱 [run 300000]',
    '재개 덱에 본 덱 체크포인트 뒤 첫 명령 [label loop_press] 이 없음 — 준비 구간 경계를 못 정함 (10-28 KG50R-03 · 준비 구간 · 상태 대조 건너뜀)',
    '첫 긴 run 뒤 명령 다름 (10-28 KG50R-03 · 명령 하나하나): 본 덱 19 개 ↔ 재개 덱 2 개 — 바뀜 [variable current_press equal "abs(f_top_mesh[3]) / 0.0025 / 1000000"] [print "Current Pressure: ${current_press} MPa (Target: ${target_press})"] → [undump dq5a] [undump dq5c]',
)


def expected_static(window, case, n=None):
    """등록 §12-4 의 정적 대조 기대 (W1 셋 · W2 넷) — 자리 채움."""
    if window == 'W2':
        return [t.replace('<N>', str(n)) for t in EXPECTED_STATIC_W2]
    return [t.replace('<case>', case) for t in EXPECTED_STATIC_W1]


W2_STATUS_DRAFT = '> **§12-2 상태: ⬜ 개정 초안 · 비준 전**'
W2_STATUS_RATIFIED_RE = re.compile(r'^> \*\*§12-2 상태: ✅ 1저자 비준 \([^)\n]+\)\*\*', re.M)
STATUS_DRAFT, STATUS_RATIFIED = '개정 초안 · 비준 전', '비준'
PLATE_RECORD = 'plate_sha256.txt'

#: ── §12-3 D3 로컬 직렬 (✅ 1저자 10-28) — A3 · C3 만 · mpirun · MPI 빌드 없음 · F3 = hit NP 2 (D1 끝난 뒤) ──
LOCAL = dict(host='wsl', root='~/q5_local', suffix='_wsl', env='LMP_SERIAL', default='$HOME/src/LIGGGHTS-PUBLIC/src/lmp_serial',
             fallback='lmp_serial', case='kg50_d3_b50_s1', branches=('A3', 'C3'))
BINARY_RECORD = 'q5_binary.txt'
#: 등록 머리 Q1 기록 — hit 원본 restart_after_settling.bin sha256 (로컬 사본이 이 값이어야)
D3_CKPT_SHA256 = '1bf24069bb3876089adb6c7521d46c27f162de4e57ab6379d042913339607ea8'
F3_LOCAL_REFUSAL = ('F3 = hit NP 2 · D1 끝난 뒤 (1저자 10-28 · 등록 §12-3) — 로컬 직렬 1 코어는 A3 와 합산 순서가 같아 '
                    '바닥이 0 (같은 계산) · 로컬로 만들지 않는다')
LOCAL_DEVIATION = ('등록 §12-3 (1저자 10-28) — D3 A3 · C3 = 로컬 WSL 직렬 LIGGGHTS 1 코어 (MPI 실행기 · MPI 빌드 없음) · '
                   '등록 = hit · 덱 = hit 덱 바이트 같음 · 러너만 다름')

#: 본 덱 고정 줄 — (종류, 기대) · 종류 cmd = 그 행에서 시작하는 명령 (정리 뒤) · re = 그 명령 정규식 · raw = 행 글자 그대로
ANCHORS = {
    40: ('re', r'variable r_AM_P equal [0-9.eE+-]+'),
    41: ('re', r'variable r_AM_S equal [0-9.eE+-]+'),
    42: ('re', r'variable r_SE equal [0-9.eE+-]+'),
    43: ('cmd', 'variable dt equal 1.0e-6'),
    45: ('cmd', 'timestep ${dt}'),
    48: ('cmd', 'processors * * 1'),
    49: ('cmd', 'region reg_box block 0.0 0.05 0.0 0.05 -0.01 1.0 units box'),
    50: ('cmd', 'create_box 3 reg_box'),
    52: ('cmd', 'neighbor 0.002 bin'),
    55: ('raw', '# --- 3. Material Properties (Type 1:AM_P, 2:AM_S, 3:SE) ---'),
    99: ('cmd', 'compute cpl all pair/gran/local pos id force force_normal force_tangential torque contactArea delta contactPoint'),
    104: ('raw', '# --- 6. Templates & Distribution ---'),
    108: ('re', r'fix pts1 all particletemplate/sphere [0-9]+ atom_type 1 density constant 4850 radius constant \$\{r_AM_P\}'),
    109: ('re', r'fix pts2 all particletemplate/sphere [0-9]+ atom_type 2 density constant 4850 radius constant \$\{r_AM_S\}'),
    110: ('re', r'fix pts3 all particletemplate/sphere [0-9]+ atom_type 3 density constant 1640 radius constant \$\{r_SE\}'),
    114: ('re', r'fix pdd_mix all particledistribution/discrete [0-9]+ 2 pts1 0\.85 pts3 0\.15'),
    116: ('raw', '# --- 7. Particle Insertion ---'),
    125: ('cmd', 'run 1'),
    126: ('cmd', 'unfix ins_mix'),
    152: ('raw', '# --- 8. Output ---'),
    153: ('cmd', 'shell mkdir post_{case}'),
    159: ('cmd', 'fix integr all nve/sphere'),
    160: ('cmd', 'fix gravi all gravity 98.1 vector 0.0 0.0 -1.0'),
    161: ('cmd', 'fix damp all viscous 1.0e-5'),
    163: ('cmd', 'compute zmax all reduce max z'),
    164: ('cmd', 'shell mkdir restart_{case}'),
    165: ('cmd', 'restart 50000 restart_{case}/restart_settling_*.bin'),
    167: ('cmd', 'run 200000'),
    170: ('cmd', 'write_restart restart_{case}/restart_after_settling.bin'),
    171: ('cmd', 'print "====== RESTART SAVED ======"'),
    172: ('cmd', 'thermo_style custom step atoms c_zmax'),
    173: ('cmd', 'thermo 1'),
    174: ('cmd', 'run 1'),
    175: ('cmd', 'variable z_max equal c_zmax'),
    176: ('cmd', 'variable plate_z equal ${z_max}+${r_AM_P}+${plate_margin}'),
    200: ('cmd', 'fix top_mesh all mesh/surface/stress file plate_{case}.stl type 1 scale 1.0 reference_point 0 0 0'),
    201: ('cmd', 'fix zwall_top all wall/gran model hooke/hysteresis tangential history rolling_friction cdt mesh n_meshes 1 '
                 'meshes top_mesh'),
    203: ('cmd', 'dump dmp_mesh all mesh/stl 5000 post_{case}/mesh_*.stl top_mesh'),
    206: ('cmd', 'fix gravi all gravity 9.81 vector 0.0 0.0 -1.0'),
    207: ('cmd', 'unfix damp'),
    208: ('cmd', 'fix damp all viscous 0.5'),
    210: ('cmd', 'variable pressMPa equal abs(f_top_mesh[3])/0.0025/1000000'),
    211: ('cmd', 'thermo_style custom step atoms ke cpu v_pressMPa'),
    212: ('cmd', 'thermo 1000'),
    213: ('cmd', 'run 200000'),
    215: ('raw', '# --- 11. Phase 3: Compression ---'),
    216: ('cmd', 'print "====== PHASE 3: COMPRESSION (Speed 0.01) ======"'),
    217: ('cmd', 'dump dmp_atom all custom 50000 post_{case}/atom_*.liggghts id type x y z radius vx vy vz c_strs[1] c_strs[2] '
                 'c_strs[3] c_ke'),
    218: ('cmd', 'fix_modify zwall_top energy yes'),
    220: ('cmd', 'variable press_speed equal 0.01'),
    221: ('cmd', 'fix move_press all move/mesh mesh top_mesh linear 0.0 0.0 -${press_speed}'),
    222: ('cmd', 'restart 200000 restart_{case}/restart_compress_*.bin'),
    224: ('cmd', 'label loop_press'),
    225: ('cmd', 'run 5000'),
    228: ('cmd', 'if "${current_press} < ${target_press}" then "jump SELF loop_press"'),
    230: ('cmd', 'unfix move_press'),
    237: ('re', r'dump dmp_contact all local 10000 post_{case}/contact_\*\.liggghts' + ''.join(r' c_cpl\[%d\]' % i for i in range(1, 27))),
}
#: 뺄 구역의 명령 첫 낱말 (§4-1 116–150 = 삽입 · 삽입 검사) · 끝 구역 (214–) — 다른 명령이 섞이면 조용히 빼지 않는다
INSERT_BLOCK_WORDS = ('region', 'print', 'fix', 'run', 'unfix', 'variable', 'print', 'if', 'group', 'variable', 'print', 'if',
                      'group', 'variable', 'print', 'if')
TAIL_WORDS = ('print', 'dump', 'fix_modify', 'variable', 'fix', 'restart', 'label', 'run', 'variable', 'print', 'if', 'unfix',
              'restart', 'print', 'unfix', 'fix', 'dump', 'run', 'write_restart', 'dump', 'dump', 'dump', 'run', 'undump', 'undump',
              'undump', 'print')

#: ⓪ 등록 문서 고정 줄 — (무엇, 글자 그대로) · 결과를 본 뒤 등록을 옮기면 여기서 터진다
REGISTRATION_ANCHORS = (
    ('비준 기록', '**결과 0 건 · 실행 전 · ✅ 1저자 비준 10-27 밤 (KST) — §10 Q1–Q12 전부 권고대로**'),
    ('Q2', '> | Q2 | (가) AM 기준 s (감쇠 가지 C · C3) |'),
    ('Q3', '> | Q3 | (나) W1 0.200001 s + W2 0.3 s |'),
    ('Q5', '> | Q5 | NP: A · B · C 56 · F 28 · D3 A3 · C3 1 · F3 2 |'),
    ('Q11', '> | Q11 | 리포의 작은 가지 덱 생성기 · 판독기 (시험 먼저 · 허용 목록 대조 · 판정 순서 selftest) |'),
    ('Q12', '> | Q12 | 덤프 간격 W1 atom 66,667 · contact 200,001 · W2 atom 10,000 · ibb 할당량 확인 |'),
    ('§2 D0.7', '| D0.7-50 `kg50_d07_b50` | v3 `docs/data/kg50_decks_20261027_v3_b50/kg50_d07_b50/input_kg50_d07_b50.liggghts` | '
                '`restart_kg50_d07_b50/restart_after_settling.bin` (step 200001 · 덱 170 행 `write_restart`)'),
    ('§2 D3', '| D3-50 s1 `kg50_d3_b50_s1` | v2 `docs/data/kg50_decks_20261026_v2/kg50_d3_b50_s1/input_kg50_d3_b50_s1.liggghts` | '
              '같은 이름 · 같은 step (덱 170 행)'),
    ('§2 원 폴더', '**원 폴더는 읽기만** — D0.7 삽입 원본 `~/dem_test/kg50_d07_b50.ins1` · 재개 본 런 폴더 `~/dem_test/kg50_d07_b50` · '
                 'D3 hit `~/simulation/kg50_d3_b50_s1`.'),
    ('§3 F', '| F | D0.7 | 없음 — A 와 같은 덱 · NP 만 다름 (⬜ Q5 · 권고 28) |'),
    ('§3 C3', '| C3 | D3 | C 와 같은 꼴 — Q2 가 (가) AM 기준일 때만 (D3 기준이면 C3 = A3) | (b) |'),
    ('§4-1 1–48', '| 1–48 (머리 주석 · 설정 · 변수 · `timestep` · `processors`) | 그대로 (주석은 빼도 됨) |'),
    ('§4-1 49–50', '| 49–50 (`region reg_box` · `create_box`) | `read_restart <가지 폴더>/restart_kg50_d07_b50/restart_after_settling.bin` '
                   '한 줄로 |'),
    ('§4-1 52–102', '| 52–102 (이웃 · 재료 m1–m9 · 쌍 · `compute` 셋 · 바닥 벽) | 그대로 |'),
    ('§4-1 104–114', '| 104–114 (템플릿 · 분포 정의) | 그대로 — `scripts/resume_ckpt.sh` 가 after_settling 재개에 하는 것과 같게 정의만 '
                     '(삽입 fix 없음) |'),
    ('§4-1 116–150', '| 116–150 (`reg_mix` · 삽입 · `run 1` · `unfix ins_mix` · 삽입 검사) | 뺌 |'),
    ('§4-1 152–165', '| 152–165 (출력 · Phase 1 fix · `compute zmax` · `restart 50000 …settling_*`) | 그대로 — 단 165 행은 가지에서 '
                     '`restart 0` (가지는 restart 파일을 안 쓴다 · 출력만) |'),
    ('§4-1 167 · 170', '| 167 (정착 `run 200000`) · 170 (`write_restart …after_settling`) | 뺌 (체크포인트 앞) |'),
    ('§4-1 171–213', '| 171–213 (`run 1` 판 높이 · 판 STL · Phase 2 안정화 · `run 200000`) | 그대로 — **창 W1 끝 = 213 행 끝** |'),
    ('§4-1 214–', '| 214– (압축 · 이완 · 끝 상태) | W1 가지에는 없음 (213 행 뒤 `undump` 로 끝) |'),
    ('§4-2 43', '| 43 | `variable dt equal 1.0e-6` | `variable dt equal 5.0e-7` |'),
    ('§4-2 173', '| 173 | `thermo 1` | `thermo 2` |'),
    ('§4-2 174', '| 174 | `run 1` | `run 2` |'),
    ('§4-2 203', '| 203 | `dump dmp_mesh … 5000 …` | `… 10000 …` |'),
    ('§4-2 212', '| 212 | `thermo 1000` | `thermo 2000` |'),
    ('§4-2 213', '| 213 | `run 200000` | `run 400000` |'),
    ('§4-2 규칙', '- 규칙 = dt 를 반으로 · step 으로 센 수는 모두 두 배.  155 행 `thermo 1000` 은 창 안에서 쓰이지 않는다 (172 · 211 행이 다시 '
                 '정한다) → 그대로.'),
    ('§4-2 창 끝', '- 창 끝 = A step 400,002 · B step 600,003 — 둘 다 체크포인트 뒤 덱 시간 0.200001 s'),
    ('§4-3 208', '| 208 | `fix damp all viscous 0.5` | `fix damp all viscous 0.5 scale 3 <s>` (type 3 = SE) |'),
    ('§4-3 s (가)', '| (가) AM 기준 (권고) | 모든 입자의 γ/m = AM 의 911.5 /s (s = m_SE/m_AM) | 5.3696e-4 | 4.2268e-2 | '
                   '1.5655e-3 · 1.2524e-2 |'),
    ('§4-4 F', '- F = A 덱 그대로 · 러너의 NP 만 (`#SBATCH -n` 과 `mpirun -np` 짝 · ⬜ Q5).'),
    ('§4-5 atom', '| `read_restart` 뒤 · 172 행 앞 | `dump dq5a all custom 66667 <폴더>/q5atom_*.liggghts id type x y z radius vx vy vz` |'),
    ('§4-5 contact', '| 같은 자리 | `dump dq5c all local 200001 <폴더>/q5contact_*.liggghts c_cpl[1] … c_cpl[26]` (덱 237 행과 같은 26 열) |'),
    ('§4-5 undump', '| 213 행 뒤 | `undump dq5a` · `undump dq5c` | 끝 |'),
    ('§4-5 step', 'A · C · F = step 200001 · 266668 · 333335 · 400002 (t 0 · 0.066667 · 0.133334 · 0.200001 s) · B = 같은 시각이 step '
                  '200001 · 333335 · 466669 · 600003 (+ 그 사이 셋).  contact = A · C · F 시작 · 끝 두 장 · B 세 장.'),
    ('§5 W2', '| **W2** | 판 첫 접촉 (본 런 thermo `pressMPa` > 0 첫 줄) 뒤 본 런의 첫 `restart_compress_*.bin` (200,000 배수 step) | '
              '**0.3 s** (판 3 µm) |'),
    ('§8-1 -C', '`재개 지점 뒤 순서 줄 수 다름: 본 덱 12 ↔ 재개 덱 0` 하나 · 그 밖 문제 0 (rc 1).'),
    ('§8-2 폴더', '- 가지마다 새 폴더 (예: `~/dem_test/q5_kg50_d07_b50_<A|B|C|F>/` · hit `~/simulation/q5_kg50_d3_b50_s1_<A3|F3|C3>/` · '
                 '⬜ 이름) — 체크포인트 · 본 덱 · 가지 덱 · 러너를 복사 · 원본 · 사본 sha256 기록.'),
    ('§8-2 잡 이름', '- 잡 이름은 재개 도구의 큐 검사 이름 (`<case>` · `_ins` · `_r<N>[t]` · `_<SFX>[t]`) 과 겹치지 않게.'),
    # ── §12 (10-28 개정) ──
    ('Q1 sha256', '`restart_after_settling.bin` 3,207,824 B (Oct 26 20:31) · sha256 '
                  '`1bf24069bb3876089adb6c7521d46c27f162de4e57ab6379d042913339607ea8`'),
    ('§12 머리', '- **개정 (10-28 · 결과 0 건 · 런 0) = §12** — §12-1 판독기가 채운 세 자리 (✅ 1저자 10-28 결정) · §12-2 W2 줄 목록 · '
                '덤프 간격 · 시작 step 규칙 (⬜ 개정 초안 · 비준 전 — W1 결과를 읽기 전에 비준)'),
    ('§12-2 침대', '- 침대 = D0.7-50 만 (§5 W2 표 = A · B · C · F · NP 56 · 56 · 56 · 28)'),
    ('§12-2 49–50', '| 49–50 | `read_restart …/restart_after_settling.bin` | `read_restart restart_kg50_d07_b50/restart_compress_<N>.bin` '
                    '(N = (라)) | §5 |'),
    ('§12-2 덤프', '| 171 뒤 q5 덤프 둘 | atom 66,667 · contact 200,001 | atom 10,000 · contact 100,000 ((나)) | Q12 · ⬜ W2-2 |'),
    ('§12-2 172–197', '| 172–197 (판 높이 `run 1` · z_max · plate_z · print · 판 STL print) | 그대로 | 뺌 |'),
    ('§12-2 213', '| 213 (안정화 `run 200000`) | 그대로 (W1 창 끝) | 뺌 |'),
    ('§12-2 214–221', '| 214–221 (압축 print · `dmp_atom` 50,000 · `fix_modify` · 판 속도 · `fix move_press`) | 없음 | 그대로 |'),
    ('§12-2 222', '| 222 (`restart 200000 …compress_*`) | 없음 | `restart 0` |'),
    ('§12-2 224–228', '| 224–228 (압축 루프 `label` · `run 5000` · 압력 판정 · `jump`) | 없음 | 224 자리에 `run 300000` 한 줄 · '
                      '225–228 뺌 |'),
    ('§12-2 undump', '| `undump dq5a` · `undump dq5c` | 213 뒤 | `run 300000` 뒤 (끝) | §4-5 |'),
    ('§12-2 B', '— W2 A 에서 바뀌는 줄: 43 `variable dt equal 5.0e-7` · 203 `dump dmp_mesh … 10000 …` · 212 `thermo 2000` · '
                '217 `dump dmp_atom … 100000 …` · 224 `run 600000`.'),
    ('§12-2 C · F', '- C = 208 행 `fix damp all viscous 0.5 scale 3 5.3696e-4` (§4-3 · W1 과 같음) · F = A 덱 그대로 · NP 28 (Q5).'),
    ('§12-2 atom', '| atom `dq5a` (§4-5 와 같은 9 열) | 10,000 | Q12 · §5 | 31 / 61 |'),
    ('§12-2 contact', '| contact `dq5c` (§4-5 와 같은 26 열) | **100,000** — ⬜ W2-2 |'),
    ('§12-2 판 STL', '(다) 판 STL — 200 행 `fix top_mesh … file plate_kg50_d07_b50.stl …` 은 그대로 두고 그 파일 = 본 런 '
                    '`post_kg50_d07_b50/mesh_<N>.stl` 의 사본 (운영자 cp · 원본 · 사본 sha256 = `plate_sha256.txt`'),
    ('§12-2 (라) 1', '1. 입력 = D0.7-50 본 런의 log.liggghts **한 파일** (정착 끝 재개 (Q6 (가)) 뒤 그 런의 로그) — 생성기가 사본을 '
                    'W2 가지 폴더 (`main_log_kg50_d07_b50.liggghts`) 에 두고 sha256 을 manifest 에 적는다.'),
    ('§12-2 (라) 2', '2. 줄 = pressMPa 열이 있는 thermo 묶음의 행 중 **묶음 첫 줄 (run 시작 setup 줄) 을 뺀 것**'),
    ('§12-2 (라) 3', '3. S_c = 그 줄 중 pressMPa > 0 인 가장 작은 step (정착 끝 step 200,001 뒤).'),
    ('§12-2 (라) 4', '4. **N = 200,000 × ⌈S_c / 200,000⌉** (S_c 가 200,000 배수면 N = S_c — 그 step 의 체크포인트 상태가 이미 접촉을 '
                    '담는다) · 600,000 보다 작으면 N = 600,000'),
    ('§12-2 (라) 5', '5. 거부 (W2 가지 안 냄 · 1저자): 그 로그에 201,000 … N 의 1,000 배수 step 이 setup 아닌 줄로 하나씩 다 있지 않다'),
    ('§12-2 (라) 5 echo', '로그 echo 에 본 덱의 `timestep 1e-06` 치환 줄 · `fix damp all viscous 0.5` · '
                         '`fix move_press all move/mesh mesh top_mesh linear 0.0 0.0 -0.01` · '
                         '`restart 200000 restart_kg50_d07_b50/restart_compress_*.bin` · PHASE 3 print 중 하나라도 없다'),
    ('§12-2 (라) 6', '6. 생성기가 계산한다 (사람이 고르지 않는다 · `--main-log` 만 받는다)'),
    ('§12-2 (마)', '(마) 정적 대조 — W2 A · F 에 `resume_ckpt.sh -C` 를 걸면 문제 = 정확히 둘 (rc 1'),
    ('§12-2 (바)', '(바) 폴더 · 운영 — 가지 폴더 `q5w2_kg50_d07_b50_<A|B|C|F>/`'),
    ('§12-3 결정', '- 결정 (1저자 10-28): A3 · C3 = 1저자 로컬 WSL 에서 직렬 LIGGGHTS 1 코어 — mpirun · MPI 빌드를 쓰지 않는다 · '
                  'NP 1 = Q5 와 같음.  F3 = hit NP 2 (Q5 그대로) · D1-50 이 끝난 뒤.'),
    ('§12-3 바이너리', '- 바이너리 — 환경 변수 `LMP_SERIAL` (⬜ L-1 이름) · 없으면 `$HOME/src/LIGGGHTS-PUBLIC/src/lmp_serial` · '
                     '그것도 없으면 PATH 의 `lmp_serial` · MPI 빌드 (`ldd` 에 libmpi) = 러너가 거부.'),
    ('§12-3 폴더', '- 폴더 · 경로 (⬜ L-2 이름): 로컬 루트 `~/q5_local` · 가지 `q5_kg50_d3_b50_s1_<A3|C3>_wsl` · 체크포인트 원본 = '
                  'hit 파일을 가져온 사본 `~/q5_local/kg50_d3_b50_s1/restart_kg50_d3_b50_s1/restart_after_settling.bin`'),
)

#: 거부 관문 — selftest 변이 (하나를 끄면 그것을 겨눈 시험이 실패해야 한다).  생산에서는 늘 True.
GUARDS = {k: True for k in ('registration', 'case', 'branch', 'np', 'window', 'pin', 'anchors', 's_check', 'allowlist',
                            'static', 'runner', 'out_exists', 'host', 'w2_case', 'w2_log', 'w2_status')}


class Refused(Exception):
    """등록 밖 · 입력 결함 — 가지를 만들지 않는다 (rc 2 · 파일 0)."""


def _on(name):
    return GUARDS.get(name, True)


def _sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def _sha256_file(path):
    with open(path, 'rb') as f:
        return _sha256_bytes(f.read())


def _read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def _rel(path):
    a = os.path.abspath(path)
    return os.path.relpath(a, ROOT) if a.startswith(ROOT + os.sep) else a


def _tok_finite(t):
    """로그 글자 하나 — ASCII 숫자 글자 (float() 은 유니코드 숫자도 받는다) 이고 유한."""
    if not t.isascii():
        return False
    try:
        return math.isfinite(float(t))
    except ValueError:
        return False


# ───────────────────────── LIGGGHTS 줄 규칙 (resume_ckpt.sh deck() 와 같음) ─────────────────────────
def _uncomment(s):
    out, q = [], None
    for ch in s:
        if q:
            out.append(ch)
            if ch == q:
                q = None
        elif ch in '"\'':
            q = ch
            out.append(ch)
        elif ch == '#':
            break
        else:
            out.append(ch)
    return ''.join(out)


def norm(s):
    """명령 한 줄 정리 — 주석 빼고 공백 하나로."""
    return ' '.join(_uncomment(s).split())


def commands(text):
    """LIGGGHTS 명령 목록 [(명령, 첫 행, 끝 행)] — '&' 이어 붙이기 (원 줄 끝) → 주석 · 공백 정리 · 빈 명령 빼기 · 행 = 1 부터."""
    res, buf, b0 = [], '', None
    raw = text.split('\n')
    for i, line in enumerate(raw, 1):
        r = line.rstrip()
        if b0 is None:
            b0 = i
        if r.endswith('&'):
            buf += r[:-1] + ' '
            continue
        s = norm(buf + r)
        buf = ''
        if s:
            res.append((s, b0, i))
        b0 = None
    if buf.strip():
        s = norm(buf)
        if s:
            res.append((s, b0, len(raw)))
    return res


# ───────────────────────── ⓪ 등록 문서 · LIGGGHTS 소스 전제 ─────────────────────────
def amendment_status(txt):
    """§12-2 상태 줄 — '개정 초안 · 비준 전' · '비준' · None (둘 다 있음 · 둘 다 없음 = 정할 수 없음)."""
    draft = any(ln.startswith(W2_STATUS_DRAFT) for ln in txt.split('\n'))
    ratified = bool(W2_STATUS_RATIFIED_RE.search(txt))
    if draft == ratified:
        return None
    return STATUS_DRAFT if draft else STATUS_RATIFIED


def registration_check(path=None):
    """등록 문서의 고정 줄이 이 파일의 상수와 같은가.  반환 (ok, 문제 목록)."""
    p = path or os.path.join(ROOT, REGISTRATION)
    try:
        txt = _read(p)
    except OSError as e:
        return False, ['등록 문서 못 읽음 (%s)' % e]
    probs = [f'§ 고정 줄 없음 — {what}: {s[:90]}…' for what, s in REGISTRATION_ANCHORS if s not in txt]
    # Q5 줄 → NP 표 (글자 → 숫자 · 이 파일의 NP 와 같아야)
    m = re.search(r'\| Q5 \| NP: (.+?) \|', txt)
    if not m:
        probs.append('Q5 NP 줄 없음')
    else:
        got, names = {}, []
        for tok in m.group(1).replace('D3 ', '').split(' · '):
            parts = tok.split()
            if parts and re.fullmatch(r'[0-9]+', parts[-1]):
                names.append(' '.join(parts[:-1]))
                for n in names:
                    got[n] = int(parts[-1])
                names = []
            else:
                names.append(tok)
        if got != NP or names:
            probs.append(f'Q5 NP {got} ≠ 생성기 {NP}')
    m = re.search(r'\| Q12 \| 덤프 간격 W1 atom ([0-9,]+) · contact ([0-9,]+) · W2 atom ([0-9,]+) ·', txt)
    if not m or (int(m.group(1).replace(',', '')), int(m.group(2).replace(',', '')), int(m.group(3).replace(',', ''))) != (
            ATOM_EVERY, CONTACT_EVERY, W2_ATOM_EVERY):
        probs.append(f'Q12 덤프 간격 ≠ 생성기 ({ATOM_EVERY} · {CONTACT_EVERY} · W2 {W2_ATOM_EVERY})')
    m = re.search(r'\| contact `dq5c` \(§4-5 와 같은 26 열\) \| \*\*([0-9,]+)\*\*', txt)
    if not m or int(m.group(1).replace(',', '')) != W2_CONTACT_EVERY:
        probs.append(f'§12-2 (나) contact 간격 ≠ 생성기 {W2_CONTACT_EVERY}')
    m = re.search(r'sha256 `([0-9a-f]{64})` → D3 가지 A3 · C3 · F3 = 이 파일', txt)
    if not m or m.group(1) != D3_CKPT_SHA256:
        probs.append('머리 Q1 기록 sha256 ≠ 생성기 D3_CKPT_SHA256')
    m = re.search(r'\| \(가\) AM 기준 \(권고\) \| [^|]+\| ([0-9.e+-]+) \| ([0-9.e+-]+) \|', txt)
    if not m or (m.group(1), m.group(2)) != (CASES['kg50_d07_b50']['s'], CASES['kg50_d3_b50_s1']['s']):
        probs.append('§4-3 s (가) ≠ 생성기 (%s · %s)' % (CASES['kg50_d07_b50']['s'], CASES['kg50_d3_b50_s1']['s']))
    for ln, a, b in B_EDITS:
        if ln == 203:
            continue                               # 표는 `dump dmp_mesh … 5000 …` 로 줄여 적었다 (위 고정 줄)
        if f'| {ln} | `{a}` | `{b}` |' not in txt:
            probs.append(f'§4-2 {ln} 행 표 ≠ 생성기 ({a} → {b})')
    sec = txt.split('### 12-4.', 1)[1].split('\n### ', 1)[0] if '### 12-4.' in txt else ''
    for head, ts in (('W1 —', EXPECTED_STATIC_W1), ('W2 —', EXPECTED_STATIC_W2)):
        part = sec.split('\n' + head, 1)[1] if ('\n' + head) in sec else ''
        got = []
        for ln in part.split('\n')[1:]:
            m = re.match(r'^[0-9]+\. `(.+)`$', ln)
            if m:
                got.append(m.group(1))
            elif got and ln.strip():
                break
        if got != list(ts):
            probs.append(f'§12-4 {head[:2]} 정적 대조 기대 (줄 · 순서) ≠ 생성기')
    return (not probs), probs


def source_premise_check(evidence_dir=None):
    """B 의 dt 줄 (read_restart 앞) 이 살아남는가 — LIGGGHTS 3d5c00f 원문 사본 (Codex 증거) 판독.
    ① write_restart 머리에 update->dt 쓰기 없음 · ② read_restart 머리에 update->dt 읽기 없음 · ③ UNITS 는 다를 때만 재설정."""
    d = evidence_dir or os.path.join(ROOT, EVIDENCE_DIR)
    probs = []
    try:
        w = _read(os.path.join(d, 'upstream_src_write_restart.cpp'))
        r = _read(os.path.join(d, 'upstream_src_read_restart.cpp'))
        src = json.loads(_read(os.path.join(d, 'upstream_sources.json')))
    except (OSError, ValueError) as e:
        return False, ['LIGGGHTS 원문 사본 못 읽음 (%s)' % e]
    pins = {x.get('path'): x.get('commit') for x in src if isinstance(x, dict)}
    for f in ('src/read_restart.cpp', 'src/write_restart.cpp'):
        if pins.get(f) != '3d5c00f20519e6bb6eb6756f51f1ad36564e649d':
            probs.append(f'{f} 가 3d5c00f 사본이 아니다 ({pins.get(f)})')
    hdr = w[w.find('void WriteRestart::header()'):w.find('void WriteRestart::type_arrays()')] if 'void WriteRestart::type_arrays()' in w \
        else w[w.find('void WriteRestart::header()'):]
    if 'void WriteRestart::header()' not in w or 'update->ntimestep' not in hdr or 'update->dt' in hdr:
        probs.append('write_restart 머리에 dt 쓰기가 있다 (또는 머리를 못 찾음)')
    if 'update->dt' in r:
        probs.append('read_restart 가 update->dt 를 건드린다')
    if 'if (strcmp(style,update->unit_style) != 0) update->set_units(style);' not in r:
        probs.append('read_restart UNITS 처리 줄이 다르다 (다를 때만 재설정이 아님)')
    if re.search(r'\bTIMESTEP\b', w + r):
        probs.append('restart 머리 열거에 TIMESTEP (dt) 가 있다')
    return (not probs), probs


# ───────────────────────── §12-2 (라) W2 시작 step — 본 런 로그 ─────────────────────────
RE_LOOP = re.compile(r'^Loop time of (\S+) on ([0-9]+) procs.*? for ([0-9]+) steps with ([0-9]+) atoms')
RE_HEADER = re.compile(r'^\s*Step\s+Atoms\b')
RE_ERROR = re.compile(r'^\s*ERROR\b')


def _w2_rows(lines):
    """thermo 묶음 (pressMPa 열) 의 setup 아닌 줄 → {step: (pressMPa, 줄)} · 같은 step 둘 · 꼴이 다른 줄."""
    rows, dup, bad, cur = {}, [], [], None
    for ln in lines:
        if RE_LOOP.match(ln):
            cur = None
            continue
        if RE_HEADER.match(ln):
            h = ln.split()
            cur = dict(n=len(h), k=next((h.index(c) for c in ('pressMPa', 'v_pressMPa') if c in h), None), first=True)
            continue
        if cur is None:
            continue
        t = ln.split()
        if not t or not re.fullmatch(r'[0-9]+', t[0]):
            continue
        if len(t) != cur['n']:
            bad.append(ln.strip()[:60])
            continue
        if cur['first']:
            cur['first'] = False                   # run 시작 setup 줄 — 판 압력을 믿을 수 없다 (§12-2 (라) 2)
            continue
        if cur['k'] is None:
            continue
        s, v = int(t[0]), t[cur['k']]
        if not _tok_finite(v) or float(v) < 0:
            bad.append(ln.strip()[:60])
            continue
        if s in rows:
            dup.append(s)
            continue
        rows[s] = (float(v), ' '.join(t))
    return rows, dup, bad


def w2_watch(text, case):
    """운영 — 본 런을 멈춰도 되는가 (같은 §12-2 (라) 규칙 · 사람이 고르지 않는다).
    ready = N 까지 줄이 다 있고 규칙 통과 (restart_compress_<N>.bin 확인 뒤 멈춤) · wait = 첫 접촉 뒤인데 로그가 아직 N 전 ·
    no_contact = pressMPa > 0 줄 없음 · refused = N 을 지났는데 규칙 거부 (빠짐 · 겹침 · echo …) — 1저자."""
    try:
        st = w2_start_from_log(text, case)
        return dict(status='ready', **st)
    except Refused as e:
        why = str(e)
    rows, _dup, _bad = _w2_rows(text.split('\n'))
    last = max(rows) if rows else None
    contact = sorted(s for s, (v, _r) in rows.items() if v > 0 and s > S0)
    if not contact:
        return dict(status='no_contact', last=last, why=why)
    sc = contact[0]
    n = max(W2_N_MIN, -(-sc // W2_CKPT_EVERY) * W2_CKPT_EVERY)
    return dict(status='wait' if (last is None or last < n) else 'refused', first_contact_step=sc, n=n, last=last, why=why)


def w2_start_from_log(text, case):
    """§12-2 (라) — 본 런 로그 한 파일 → dict(n · first_contact_step · first_contact_row · rows).  못 정하면 Refused.
    줄 = pressMPa 열이 있는 thermo 묶음의 행 중 묶음 첫 줄 (setup) 을 뺀 것 · S_c = pressMPa > 0 인 가장 작은 step (> 정착 끝) ·
    N = 200,000 × ⌈S_c / 200,000⌉ (최소 600,000) · 201,000 … N 의 1,000 배수 줄이 하나씩 다 있어야."""
    lines = text.split('\n')
    probs = []
    if any(RE_ERROR.match(x) for x in lines):
        probs.append('ERROR 줄이 있다')
    normed = {norm(x) for x in lines}
    for e in W2_LOG_ECHO:
        e = e.replace('{case}', case)
        if e not in normed:
            probs.append(f'로그 echo 에 [{e}] 가 없다 (다른 덱 · 다른 런)')
    rows, dup, bad = _w2_rows(lines)
    contact = sorted(s for s, (v, _r) in rows.items() if v > 0 and s > S0)
    if not contact:
        raise Refused('본 런 로그에 pressMPa > 0 인 줄이 없다 (setup 줄 빼고 · 정착 끝 뒤) — 아직 접촉 전 (§12-2 (라) 3)')
    sc = contact[0]
    n = max(W2_N_MIN, -(-sc // W2_CKPT_EVERY) * W2_CKPT_EVERY)
    miss = [s for s in range(W2_LOG_FIRST, n + 1, W2_LOG_EVERY) if s not in rows]
    if miss:
        probs.append(f'1,000 배수 줄 빠짐 {len(miss)} ({miss[:4]} …) — 버퍼 유실 · 잘림 · 다른 런')
    if dup:
        probs.append(f'같은 step 줄 둘 {sorted(set(dup))[:4]} — 로그 이어 붙이기')
    if bad:
        probs.append(f'열 수 · pressMPa 글자가 다른 줄 {len(bad)} ([{bad[0]}])')
    if probs and _on('w2_log'):
        raise Refused('본 런 로그로 W2 시작 step 을 정할 수 없다 (§12-2 (라) 5) — ' + ' | '.join(probs[:5]))
    return dict(n=n, first_contact_step=sc, first_contact_row=rows[sc][1], rows=len(rows), rule='§12-2 (라)')


def synth_main_log(case, first_contact, last, *, np_=56, setup_spike=None, stab_contact=None, drop=(), dup=(), bad=None,
                   error=False, echo_drop=None, dt_echo='1e-06', extra_col=None, atoms=12):
    """selftest 합성 본 런 로그 (정착 끝 재개 뒤 · step 200,001 부터 · 본 덱 압축 루프 꼴) — §12-2 (라) 시험용.
    pressMPa = 0 (first_contact 앞) · 그 뒤 양수 · setup_spike = 그 step 에서 시작하는 run 의 setup 줄만 양수 ·
    stab_contact = 안정화 중 그 정규 줄만 양수 · drop · dup = 정규 줄 빼기 · 두 번 · bad = (step, 글자) · echo_drop = 그 echo 줄
    빼기 (정리 뒤 글자) · extra_col = 그 step 정규 줄에 열 하나 더."""
    hdr = '    Step    Atoms         KinEng            CPU       pressMPa '

    def p(s, setup):
        if setup and setup_spike is not None and s == setup_spike:
            return 0.0123
        if not setup and stab_contact is not None and s == stab_contact:
            return 0.0007
        return 0.0 if s < first_contact else 1e-4 * (s - first_contact + 1000) / 1000.0

    def row(s, setup=False):
        v = bad[1] if (bad and bad[0] == s and not setup) else '%.8g' % p(s, setup)
        return f'  {s} {atoms} 2e-09 1.5 {v}' + (' 7' if (extra_col == s and not setup) else '')

    def block(start, n):
        out = [hdr, row(start, True)]
        for s in range(((start // 1000) + 1) * 1000, start + n + 1, 1000):
            if s in drop:
                continue
            out.append(row(s))
            if s in dup:
                out.append(row(s))
        if (start + n) % 1000:
            out.append(row(start + n))
        return out + [f'Loop time of 1.5 on {np_} procs for {n} steps with {atoms} atoms, finish time Tue Oct 28 10:00:00 2026']

    L = ['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, compiled 2025-08-25)', 'units           si', 'variable dt      equal 1.0e-6',
         'timestep        ${dt}', 'timestep        ' + dt_echo, f'read_restart    restart_{case}/restart_after_settling.bin',
         '  8 by 7 by 1 MPI processor grid', 'fix damp all viscous 1.0e-5', 'thermo_style    custom step atoms c_zmax',
         'thermo          1', 'run 1', '    Step    Atoms         zmax ', f'  {S0} {atoms} 0.1 ', f'  {S0 + 1} {atoms} 0.1 ',
         f'Loop time of 1 on {np_} procs for 1 steps with {atoms} atoms, finish time Tue Oct 28 09:00:00 2026',
         '====== PLATE HEIGHT: 0.11 ======', 'fix gravi all gravity 9.81 vector 0.0 0.0 -1.0', 'unfix damp', 'fix damp all viscous 0.5',
         'variable pressMPa equal abs(f_top_mesh[3])/0.0025/1000000', 'thermo_style    custom step atoms ke cpu v_pressMPa',
         'thermo 1000', 'run 200000']
    L += block(S0 + 1, 200000)
    L += ['print "====== PHASE 3: COMPRESSION (Speed 0.01) ======"', '====== PHASE 3: COMPRESSION (Speed 0.01) ======',
          'fix_modify      zwall_top energy yes', 'variable press_speed equal 0.01',
          'fix move_press all move/mesh mesh top_mesh linear 0.0 0.0 -${press_speed}',
          'fix move_press all move/mesh mesh top_mesh linear 0.0 0.0 -0.01', f'restart 200000 restart_{case}/restart_compress_*.bin',
          'label loop_press']
    s = S0 + 1 + 200000
    while s < last:
        L += ['run 5000'] + block(s, 5000) + ['Current Pressure: 0 MPa (Target: 0.3)']
        s += 5000
    if error:
        L.append('ERROR: Lost atoms: original 12 current 11 (../thermo.cpp:389)')
    if echo_drop is not None:
        L = [x for x in L if norm(x) != echo_drop]
    return '\n'.join(L) + '\n'


# ───────────────────────── ① ② 본 덱 ─────────────────────────
def pinned_sha(case):
    """본 덱 sha256 = 덱 묶음 manifest.json 의 deck_sha256 (그 덱을 만든 생성기의 기록)."""
    man = json.loads(_read(os.path.join(ROOT, CASES[case]['deck_manifest'])))
    hits = [c.get('deck_sha256') for c in man.get('cases', []) if c.get('case') == case]
    if len(hits) != 1 or not re.fullmatch(r'[0-9a-f]{64}', str(hits[0])):
        raise Refused(f'{CASES[case]["deck_manifest"]} 에 {case} deck_sha256 이 하나가 아니다')
    return hits[0]


def check_anchors(text, case):
    """본 덱 고정 줄 · 구역 꼴 — 문제 목록."""
    lines = text.split('\n')
    probs = []
    if len(lines) != MAIN_NLINES + 1 or lines[-1] != '':
        probs.append(f'본 덱 행 수 {len(lines) - (1 if lines[-1] == "" else 0)} ≠ {MAIN_NLINES} (§2 두 덱 같은 행 번호)')
        return probs
    cmds = commands(text)
    first = {c[1]: c[0] for c in cmds}
    for ln, (kind, exp) in sorted(ANCHORS.items()):
        e = exp.replace('{case}', case)
        if kind == 'raw':
            if lines[ln - 1] != e:
                probs.append(f'본 덱 {ln} 행 ≠ [{e}] (실제 [{lines[ln - 1]}])')
        elif kind == 'cmd':
            if first.get(ln) != e:
                probs.append(f'본 덱 {ln} 행 명령 ≠ [{e}] (실제 [{first.get(ln)}])')
        elif not (first.get(ln) is not None and re.fullmatch(e, first[ln])):
            probs.append(f'본 덱 {ln} 행 명령이 등록 꼴이 아니다 (실제 [{first.get(ln)}])')
    words = tuple(c[0].split()[0] for c in cmds if 116 <= c[1] <= 150)
    if words != INSERT_BLOCK_WORDS:
        probs.append(f'본 덱 116–150 (뺄 구역) 명령 꼴 ≠ 삽입 · 삽입 검사 ({words})')
    tail = tuple(c[0].split()[0] for c in cmds if c[1] >= 214)
    if tail != TAIL_WORDS:
        probs.append(f'본 덱 214– (뺄 구역) 명령 꼴 ≠ 압축 · 이완 · 끝 상태 ({tail})')
    for c, l0, l1 in cmds:
        for what, drop in (('W1', DROP_LINES), ('W2', W2_DROP)):
            a = l0 in drop
            if any((k in drop) != a for k in range(l0, l1 + 1)):
                probs.append(f'본 덱 {l0}–{l1} 행 명령이 {what} 뺄 구역 경계를 걸친다')
        if l0 in (167, 170) and l1 != l0:
            probs.append(f'본 덱 {l0} 행 명령이 한 줄이 아니다')
    for ln in sorted(set([x for x, _a, _b in B_EDITS] + [x for x, _a, _b in W2_B_EDITS]
                         + [C_EDIT[0], RESTART0_LINE, READ_RESTART_LINE, W2_RUN_LINE] + list(W2_RESTART0_LINES))):
        if _uncomment(lines[ln - 1]).rstrip() != lines[ln - 1].rstrip() or lines[ln - 1].rstrip().endswith('&'):
            probs.append(f'본 덱 {ln} 행 (바꿀 줄) 에 주석 · 이어 붙이기가 있다')
    return probs


def derive(text, case):
    """본 덱에서 다시 세는 값 — dt · 체크포인트 step · 반지름 · 밀도 · 접촉 열 · 압력 면적."""
    cmds = commands(text)
    first = {c[1]: c[0] for c in cmds}
    var = {}
    for c, _l0, _l1 in cmds:
        m = re.fullmatch(r'variable (\w+) equal ([0-9.eE+-]+)', c)
        if m:
            var[m.group(1)] = m.group(2)
    s0 = 0
    for c, l0, _l1 in cmds:
        if l0 >= 170:
            break
        m = re.fullmatch(r'run ([0-9]+)', c)
        if m:
            s0 += int(m.group(1))
    dens, rad = {}, {}
    for ln in (108, 109, 110):
        m = re.fullmatch(r'fix pts[0-9] all particletemplate/sphere [0-9]+ atom_type ([0-9]) density constant ([0-9.]+) radius constant '
                         r'\$\{(\w+)\}', first[ln])
        t = int(m.group(1))
        dens[t] = float(m.group(2))
        rad[t] = float(var[m.group(3)])
    cols = tuple(first[237].split()[6:])
    m = re.fullmatch(r'variable pressMPa equal abs\(f_top_mesh\[3\]\)/([0-9.]+)/1000000', first[210])
    return dict(dt_token=var['dt'], dt=float(var['dt']), s0=s0, density=dens, radius=rad, contact_cols=cols,
                area=float(m.group(1)), runs=[int(first[174].split()[1]), int(first[213].split()[1])])


def s_from_deck(d):
    """Q2 (가) s = m_SE/m_AM = ρ_SE r_SE³ / (ρ_AM r_AM³) (본 덱 템플릿 · 변수 · type 3 ↔ type 1)."""
    return (d['density'][SE_TYPE] * d['radius'][SE_TYPE] ** 3) / (d['density'][1] * d['radius'][1] ** 3)


# ───────────────────────── ③ 가지 덱 · ④ 허용 목록 ─────────────────────────
def _lead(raw):
    return raw[:len(raw) - len(raw.lstrip())]


def _dump_lines(case, window='W1'):
    a, c = (W2_ATOM_EVERY, W2_CONTACT_EVERY) if window == 'W2' else (ATOM_EVERY, CONTACT_EVERY)
    return ['dump dq5a all custom %d post_%s/q5atom_*.liggghts %s' % (a, case, ' '.join(ATOM_COLS)),
            'dump dq5c all local %d post_%s/q5contact_*.liggghts %s' % (c, case, ' '.join(CONTACT_COLS))]


UNDUMP_LINES = ['undump dq5a', 'undump dq5c']


def _edits(case, branch, window='W1'):
    """가지마다 바꾸는 행 → (A 명령, 가지 명령)."""
    kind = KIND[branch]
    ed = {}
    if kind == 'dt_half':
        for ln, a, b in (W2_B_EDITS if window == 'W2' else B_EDITS):
            ed[ln] = (a.replace('{case}', case), b.replace('{case}', case))
    elif kind == 'damp':
        ln, a, b = C_EDIT
        ed[ln] = (a, b.replace('{s}', CASES[case]['s']))
    return ed


def header(case, branch, main_sha):
    kind = KIND[branch]
    who = {'base': 'A · F' if case == 'kg50_d07_b50' else 'A3 · F3', 'floor': 'A · F' if case == 'kg50_d07_b50' else 'A3 · F3',
           'dt_half': 'B', 'damp': 'C' if case == 'kg50_d07_b50' else 'C3'}[kind]
    extra = ''
    if kind == 'dt_half':
        extra = ' · B: 43 dt 5.0e-7 · 173 thermo 2 · 174 run 2 · 203 mesh 10000 · 212 thermo 2000 · 213 run 400000'
    elif kind == 'damp':
        extra = f' · {who}: 208 fix damp all viscous 0.5 scale 3 {CASES[case]["s"]}'
    return [f'# ===== 50kg Q5 가지 {who} — {KIND_KO[kind]} · 창 W1 · scripts/kg50_q5_branches.py 생성 (손으로 고치지 말 것) =====',
            f'#   등록 {REGISTRATION} §3 · §4 (1저자 10-27 밤 비준 · Q1–Q12)',
            f'#   본 덱 {CASES[case]["deck"]} · sha256 {main_sha}',
            '#   = 본 덱을 줄 단위로 옮기고 등록된 줄만 바꿈: 49–50 → read_restart · 116–150 · 167 · 170 · 214– 뺌 · 165 → restart 0 ·',
            f'#     172 앞 q5 덤프 둘 (atom {ATOM_EVERY} · contact {CONTACT_EVERY}) · 213 뒤 undump 둘{extra}',
            f'#   체크포인트 restart_{case}/restart_after_settling.bin (step {S0}) = 운영자가 복사 · sha256 (ckpt_sha256.txt) · '
            'NP = 러너 (Q5)',
            HEADER_END]


def build_text(main_text, case, branch, main_sha, window='W1', n=None, status=None, start=None):
    """가지 덱 글자 — 본 덱 줄을 그대로 옮기고 등록 바꿈만 (§4-1 · §4-2 · §4-3 · §4-5 · W2 = §12-2 (가))."""
    if window == 'W2':
        return _w2_text(main_text, case, branch, main_sha, n, status, start)
    lines = main_text.split('\n')
    ed = _edits(case, branch)
    out = header(case, branch, main_sha)
    for k in range(1, MAIN_NLINES + 1):
        raw = lines[k - 1]
        if k in DROP_LINES:
            continue
        if k == READ_RESTART_LINE:
            out.append(f'read_restart restart_{case}/restart_after_settling.bin')
        elif k == RESTART0_LINE:
            out.append(_lead(raw) + 'restart 0')
        elif k in ed:
            out.append(_lead(raw) + ed[k][1])
        else:
            out.append(raw)
        if k == INSERT_DUMPS_AFTER:
            out += _dump_lines(case)
        if k == INSERT_UNDUMPS_AFTER:
            out += UNDUMP_LINES
    return '\n'.join(out) + '\n'


def expected_commands(main_text, case, branch, window='W1', n=None):
    """등록 바꿈을 본 덱 **명령** 에 적용한 가지 명령 목록 — 생성기 (줄 바꿈) 와 다른 길.  본 덱 바꿀 줄이 등록 A 값이 아니면 문제."""
    if window == 'W2':
        return _w2_expected(main_text, case, branch, n)
    ed = _edits(case, branch)
    exp, probs = [], []
    for c, l0, _l1 in commands(main_text):
        if l0 in DROP_LINES:
            continue
        if l0 == READ_RESTART_LINE:
            exp.append(f'read_restart restart_{case}/restart_after_settling.bin')
        elif l0 == RESTART0_LINE:
            exp.append('restart 0')
        elif l0 in ed:
            if c != ed[l0][0]:
                probs.append(f'본 덱 {l0} 행 [{c}] ≠ 등록 A 값 [{ed[l0][0]}]')
            exp.append(ed[l0][1])
        else:
            exp.append(c)
        if l0 == INSERT_DUMPS_AFTER:
            exp += _dump_lines(case)
        if l0 == INSERT_UNDUMPS_AFTER:
            exp += list(UNDUMP_LINES)
    return exp, probs


def _new_lines(case, branch, window='W1', n=None):
    """줄 단위 대조에서 본 덱 줄이 아니어도 되는 등록 새 줄."""
    if window == 'W2':
        return _w2_new_lines(case, branch, n)
    return set(_dump_lines(case) + UNDUMP_LINES + [f'read_restart restart_{case}/restart_after_settling.bin', 'restart 0'] +
               [b for _a, b in _edits(case, branch).values()])


# ───────────────────────── §12-2 W2 (⬜ 개정 초안 · 비준 전) ─────────────────────────
def _w2_text(main_text, case, branch, main_sha, n, status, start):
    """W2 가지 덱 글자 — §4-1 뼈대에서 §12-2 (가) 표만 다름."""
    kind = KIND[branch]
    who = {'base': 'A · F', 'floor': 'A · F', 'dt_half': 'B', 'damp': 'C'}[kind]
    extra = ''
    if kind == 'dt_half':
        extra = ' · B: 43 dt 5.0e-7 · 203 mesh 10000 · 212 thermo 2000 · 217 dmp_atom 100000 · 224 run 600000'
    elif kind == 'damp':
        extra = f' · C: 208 fix damp all viscous 0.5 scale 3 {CASES[case]["s"]}'
    out = [f'# ===== 50kg Q5 가지 {who} — {KIND_KO[kind]} · 창 W2 (§12-2) · scripts/kg50_q5_branches.py 생성 (손으로 고치지 말 것) =====',
           f'#   등록 {REGISTRATION} §12-2 (W2 줄 목록 · 10-28 개정) · §3 · §4 (1저자 10-27 밤 비준 · Q1–Q12)',
           f'#   §12-2 상태: {status}',
           f'#   본 덱 {CASES[case]["deck"]} · sha256 {main_sha}',
           '#   = §4-1 뼈대에서 §12-2 (가) 만 다름: 49–50 → read_restart …compress · 172–197 · 213 뺌 · 214–221 그대로 · 222 → restart 0 ·',
           f'#     224–228 → run {W2_RUN[kind]} · 171 뒤 q5 덤프 둘 (atom {W2_ATOM_EVERY} · contact {W2_CONTACT_EVERY}) · run 뒤 undump 둘'
           f'{extra}',
           f'#   시작 step N = {n} (본 런 첫 접촉 step {start["first_contact_step"]} · §12-2 (라) · 본 런 로그 사본 main_log_{case}.liggghts '
           f'sha256 {start["log_sha256"]})',
           f'#   체크포인트 restart_{case}/restart_compress_{n}.bin · 판 STL plate_{case}.stl (= 본 런 post_{case}/mesh_{n}.stl) = 운영자가 '
           '복사 · sha256 · NP = 러너 (Q5)',
           HEADER_END]
    lines = main_text.split('\n')
    ed = _edits(case, branch, 'W2')
    for k in range(1, MAIN_NLINES + 1):
        raw = lines[k - 1]
        if k in W2_DROP:
            continue
        if k == READ_RESTART_LINE:
            out.append(f'read_restart restart_{case}/restart_compress_{n}.bin')
        elif k in W2_RESTART0_LINES:
            out.append(_lead(raw) + 'restart 0')
        elif k == W2_RUN_LINE:
            out.append(_lead(raw) + f'run {W2_RUN[kind]}')
        elif k in ed:
            out.append(_lead(raw) + ed[k][1])
        else:
            out.append(raw)
        if k == INSERT_DUMPS_AFTER:
            out += _dump_lines(case, 'W2')
        if k == W2_RUN_LINE:
            out += UNDUMP_LINES
    return '\n'.join(out) + '\n'


def _w2_expected(main_text, case, branch, n):
    ed = _edits(case, branch, 'W2')
    exp, probs = [], []
    for c, l0, _l1 in commands(main_text):
        if l0 in W2_DROP:
            continue
        if l0 == READ_RESTART_LINE:
            exp.append(f'read_restart restart_{case}/restart_compress_{n}.bin')
        elif l0 in W2_RESTART0_LINES:
            exp.append('restart 0')
        elif l0 == W2_RUN_LINE:
            exp.append(f'run {W2_RUN[KIND[branch]]}')
        elif l0 in ed:
            if c != ed[l0][0]:
                probs.append(f'본 덱 {l0} 행 [{c}] ≠ 등록 A 값 [{ed[l0][0]}]')
            exp.append(ed[l0][1])
        else:
            exp.append(c)
        if l0 == INSERT_DUMPS_AFTER:
            exp += _dump_lines(case, 'W2')
        if l0 == W2_RUN_LINE:
            exp += list(UNDUMP_LINES)
    return exp, probs


def _w2_new_lines(case, branch, n):
    return set(_dump_lines(case, 'W2') + UNDUMP_LINES + [f'read_restart restart_{case}/restart_compress_{n}.bin', 'restart 0',
                                                          f'run {W2_RUN[KIND[branch]]}'] +
               [b for _a, b in _edits(case, branch, 'W2').values()])


def _strip_header(text):
    """생성기 머리 (주석 줄만 · & 로 끝나는 줄 없음 — LIGGGHTS 가 다음 줄을 주석에 이어 붙인다) 를 뗀 본문 · 아니면 None."""
    lines = text.split('\n')
    if HEADER_END not in lines:
        return None
    k = lines.index(HEADER_END)
    if not all(x.startswith('#') and not x.rstrip().endswith('&') for x in lines[:k + 1]):
        return None
    return '\n'.join(lines[k + 1:])


def verify_branch_deck(main_text, branch_text, case, branch, window='W1', n=None):
    """④ 허용 목록 대조 — 문제 목록 (빈 목록 = 통과).  명령 단위 + 줄 단위 (본 덱 줄 그대로 · 순서)."""
    probs = []
    if case not in CASES or branch not in KIND or (_on('branch') and branch not in CASES[case]['branches']):
        return [f'가지 {branch} 는 {case} 의 등록 가지가 아니다']
    if window == 'W2' and not (isinstance(n, int) and n > 0):
        return ['W2 시작 step N 이 없다']
    body = _strip_header(branch_text)
    if body is None:
        return ['가지 덱 머리 (생성기 표지) 가 없다 · 머리에 주석 아닌 줄이 있다']
    exp, p0 = expected_commands(main_text, case, branch, window, n)
    probs += p0
    got = [c for c, _a, _b in commands(body)]
    if got != exp:
        sm = difflib.SequenceMatcher(a=exp, b=got, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != 'equal':
                probs.append(f'허용 목록 밖 ({tag}): 기대 {exp[i1:i2][:3]} ↔ 가지 {got[j1:j2][:3]}')
    # 줄 단위 — 머리 뒤 줄 = 본 덱 줄 그대로 (순서대로) 또는 등록 새 줄 (명령이 기대와 같을 때)
    new_ok = _new_lines(case, branch, window, n)
    mlines = main_text.split('\n')
    j = 0
    for raw in body.split('\n')[:-1] if body.endswith('\n') else body.split('\n'):
        if norm(raw) in new_ok and raw.strip() == norm(raw):
            continue
        while j < len(mlines) and mlines[j] != raw:
            j += 1
        if j >= len(mlines):
            probs.append(f'가지 덱 줄이 본 덱에 (그 순서로) 없다: [{raw[:100]}]')
            break
        j += 1
    return probs


# ───────────────────────── ⑤ 정적 대조 ─────────────────────────
def static_check(main_path, deck_path, case, tool=None, ckpt=None, s0=S0):
    """`resume_ckpt.sh -C` (재개 덱 정적 대조) — 출력 · 종료 코드 · 문제 줄."""
    tool = tool or os.path.join(ROOT, RESUME_TOOL)
    ckpt = ckpt or f'restart_{case}/restart_after_settling.bin'
    with tempfile.TemporaryDirectory(prefix='q5W_') as w:
        r = subprocess.run(['bash', tool, '-C', main_path, deck_path, ckpt, str(s0), w],
                           capture_output=True, text=True, timeout=120)
    lines = r.stdout.splitlines()
    return dict(rc=r.returncode, problems=[x[4:] for x in lines if x.startswith('  ✗ ')],
                notes=[x[4:] for x in lines if x.startswith('  · ')], tool=_rel(tool), tool_sha256=_sha256_file(tool),
                stdout=r.stdout, stderr=r.stderr[-2000:])


# ───────────────────────── ⑥ 러너 ─────────────────────────
RUNNER_DIFF_OK = (re.compile(r'^#SBATCH --job-name=\S+$'), re.compile(r'^#SBATCH --output=logs/output_\S+_%j\.out$'),
                  re.compile(r'^#SBATCH -n [0-9]+$'), re.compile(r'^cd \S+$'),
                  re.compile(r'^mpirun --oversubscribe --bind-to none -np [0-9]+ lmp_mpi -in \S+$'))


def folder_name(case, branch, window='W1', host=None):
    """가지 폴더 = q5_<case>_<가지> (W1) · q5w2_<case>_<가지> (W2 · §12-2 (바)) · 로컬 (§12-3) = 꼬리 _wsl."""
    return f'{W2_PREFIX if window == "W2" else "q5_"}{case}_{branch}{LOCAL["suffix"] if host == LOCAL["host"] else ""}'


def _local_runner(case, branch, np_, fol, q1):
    """§12-3 로컬 직렬 러너 글자 — mpirun 없음 · 검사 하나라도 실패하면 실행 안 함 (rc 2) · 바이너리 경로 · sha256 기록."""
    root = LOCAL['root'].replace('~', '$HOME', 1)
    env, dflt, fb = LOCAL['env'], LOCAL['default'], LOCAL['fallback']
    ck = f'restart_{case}/restart_after_settling.bin'
    deck, log = f'input_{fol}.liggghts', f'log_{fol}_v1.out'
    return '\n'.join([
        '#!/bin/bash',
        f'# 50kg Q5 가지 {branch} — 로컬 WSL · 직렬 LIGGGHTS 1 코어 · MPI 실행기 없음 · NP {np_} (Q5) · 등록 §12-3 이탈 (등록 = hit) · '
        'scripts/kg50_q5_branches.py 생성 (손으로 고치지 말 것)',
        f'# 바이너리 = 환경 변수 {env} · 없으면 {dflt} · 그것도 없으면 PATH 의 {fb} · MPI 빌드 (ldd 에 libmpi) = 거부',
        '# 검사 하나라도 실패 = 실행 안 함 (rc 2): 폴더 SHA256SUMS · ckpt_sha256.txt 두 줄 = 등록 Q1 sha256 · 체크포인트 sha256 · '
        'log.liggghts 없음 · 바이너리',
        'set -u',
        f'cd "{root}/{fol}" || {{ echo "⛔ 가지 폴더 없음 — 실행 안 함"; exit 2; }}',
        'sha256sum -c --quiet SHA256SUMS || { echo "⛔ SHA256SUMS 다름 — 실행 안 함"; exit 2; }',
        f'Q1={q1}',
        '[ -f ckpt_sha256.txt ] && [ "$(wc -l < ckpt_sha256.txt)" = 2 ] && [ "$(cut -d" " -f1 ckpt_sha256.txt | sort -u)" = "$Q1" ] '
        '|| { echo "⛔ ckpt_sha256.txt 가 두 줄 · 같은 값 · 등록 Q1 sha256 이 아니다 — 실행 안 함"; exit 2; }',
        f'[ "$(sha256sum {ck} 2>/dev/null | cut -d" " -f1)" = "$Q1" ] || {{ echo "⛔ 체크포인트 {ck} sha256 ≠ 등록 Q1 — 실행 안 함"; '
        'exit 2; }',
        '[ ! -e log.liggghts ] || { echo "⛔ log.liggghts 이미 있음 (덮어쓰지 않는다) — 실행 안 함"; exit 2; }',
        f'if [ -n "${{{env}:-}}" ]; then L="${env}"; elif [ -x "{dflt}" ]; then L="{dflt}"; else L={fb}; fi',
        'B=$(command -v "$L") || { echo "⛔ 직렬 바이너리 없음 ($L) — 실행 안 함"; exit 2; }',
        '! ldd "$B" 2>/dev/null | grep -q libmpi || { echo "⛔ $B = MPI 빌드 (libmpi) — 로컬은 직렬만 (등록 §12-3) · 실행 안 함"; exit 2; }',
        f'printf "mode serial\\nnp {np_}\\nbinary %s\\nsha256 %s\\nlibmpi none\\nhost %s\\n" "$B" "$(sha256sum "$B" | cut -d" " -f1)" '
        f'"$(uname -n)" > {BINARY_RECORD}',
        f'setsid nohup "$B" -in {deck} > {log} 2>&1 < /dev/null &',
        f'echo "▶ {fol}: $B (pid $!) · log.liggghts · {log} · {BINARY_RECORD}"',
        ''])


def render_runner(case, branch, np_, template_path=None, window='W1', host=None, q1=None):
    """러너 글자 — ibb = 리포 러너 렌더 (본 러너와 같은 틀) · hit = hit_command (SLURM 없음) · 로컬 = §12-3 직렬."""
    fol = folder_name(case, branch, window, host)
    if host == LOCAL['host']:
        return _local_runner(case, branch, np_, fol, q1 or D3_CKPT_SHA256)
    import make_se_size_decks as MSD          # 덱 생성기의 러너 규약 (render_ibb_runner · hit_command) 을 그대로 쓴다
    try:
        if CASES[case]['host'] == 'ibb':
            tmpl = _read(template_path or os.path.join(ROOT, RUNNER_TEMPLATE))
            return MSD.render_ibb_runner(tmpl, RUNNER_TEMPLATE_CASE, fol, int(np_))
        cmd = MSD.hit_command(fol, int(np_))
    except SystemExit as e:                    # make_se_size_decks._die
        raise Refused(f'러너 렌더 실패: {e}')
    return ('#!/bin/bash\n'
            f'# 50kg Q5 가지 {branch} (hit · SLURM 없음 · make_se_size_decks.hit_command 꼴) · NP {np_} (Q5) · '
            'scripts/kg50_q5_branches.py 생성\n'
            f'# 체크포인트 복사 · sha256 (ckpt_sha256.txt) 뒤에만 실행\n{cmd}\n')


def runner_check(case, branch, np_, text, window='W1', host=None, q1=None):
    """러너 대조 — 문제 목록.  ibb: 본 러너와 다섯 줄만 다름 · -n N ↔ -np N · cd · -in.  hit: 명령 한 줄 = hit_command.
    로컬: 생성기 글자 그대로 (§12-3)."""
    fol = folder_name(case, branch, window, host)
    lines = text.split('\n')
    probs = []
    if host == LOCAL['host']:
        want = _local_runner(case, branch, np_, fol, q1 or D3_CKPT_SHA256)
        if text != want:
            d = [f'{a!r} ↔ {b!r}' for a, b in zip(want.split('\n'), lines) if a != b][:2]
            probs.append(f'로컬 러너 ≠ 생성기 글자 (§12-3) — {d or "줄 수 다름"}')
        return probs
    if CASES[case]['host'] == 'ibb':
        main = _read(os.path.join(ROOT, CASES[case]['main_runner'])).split('\n')
        if len(main) != len(lines):
            probs.append(f'러너 줄 수 {len(lines)} ≠ 본 러너 {len(main)}')
        for a, b in zip(main, lines):
            if a != b and not any(p.match(a) and p.match(b) for p in RUNNER_DIFF_OK):
                probs.append(f'러너가 본 러너와 허용 밖 줄에서 다르다: [{a}] ↔ [{b}]')
        need = (f'#SBATCH --job-name={fol}', f'#SBATCH --output=logs/output_{fol}_%j.out', f'#SBATCH -n {np_}',
                f'cd $HOME/dem_test/{fol}', f'mpirun --oversubscribe --bind-to none -np {np_} lmp_mpi -in input_{fol}.liggghts')
        for n in need:
            if lines.count(n) != 1:
                probs.append(f'러너에 [{n}] 이 한 번 있어야 한다')
    else:
        body = [x for x in lines if x.strip() and not x.startswith('#')]
        want = (f'cd $HOME/simulation/{fol} && setsid nohup mpirun --oversubscribe --bind-to none -np {np_} '
                f'$HOME/LIGGGHTS-PUBLIC/src/lmp_auto -in input_{fol}.liggghts > log_{fol}_v1.out 2>&1 < /dev/null &')
        if body != [want] or not lines[0] == '#!/bin/bash':
            probs.append(f'hit 러너 명령 ≠ [{want}]')
    return probs


# ───────────────────────── ⑦ ⑧ 쓰기 · 운영자 명령 ─────────────────────────
def expected_steps(s0, end, every):
    return [s for s in range(((s0 + every - 1) // every) * every, end + 1, every)]


def _gate(rec):
    return f'[ "$(wc -l < {rec})" = 2 ] && [ "$(cut -d" " -f1 {rec} | sort -u | wc -l)" = 1 ]'


def operator_commands(man):
    """체크포인트 복사 · sha256 · 제출 — 운영자가 붙여 넣을 줄 (아무것도 띄우지 않는다)."""
    if man.get('host') == LOCAL['host']:
        return _operator_local(man)
    if man.get('window') == 'W2':
        return _operator_w2(man)
    case, fol, br, np_ = man['case'], man['folder'], man['branch'], man['np']
    c = CASES[case]
    root = c['run_root']
    src = f'{c["main_folder"]}/restart_{case}/restart_after_settling.bin'
    dst = f'{root}/{fol}/restart_{case}/restart_after_settling.bin'
    out = [f'# ── {c["host"]} · {fol} (가지 {br} · NP {np_}) ──']
    if c['host'] == 'ibb':
        out.append('# 본 런 (kg50_d07_b50) 이 restart_after_settling.bin 을 쓴 뒤 멈춘 (scancel) 뒤에만 (§8-3 2 · Q6 (가)) · '
                   'cpu-60 = 가지는 차례로')
    else:
        out.append(f'ls -l {src}   # Q1 — 없으면 멈춤 (1저자 · (가) D3 를 정착 끝까지 다시 · NP 1 · 같은 덱)')
    out += [f'cd {root}/{fol} && sha256sum -c SHA256SUMS',
            f'mkdir -p {root}/{fol}/restart_{case} && cp {src} {root}/{fol}/restart_{case}/',
            f'sha256sum {src} {dst} > {root}/{fol}/ckpt_sha256.txt && cat {root}/{fol}/ckpt_sha256.txt']
    rec = f'{root}/{fol}/ckpt_sha256.txt'
    gate = _gate(rec)
    if c['host'] == 'ibb':
        out.append(f'{gate} && (cd {root} && mkdir -p logs && sbatch {fol}/run_{fol}.sh) || echo "⛔ 체크포인트 sha256 다름 · 없음 — '
                   '제출 안 함"')
    else:
        out.append(f'{gate} && bash {root}/{fol}/run_{fol}.sh || echo "⛔ 체크포인트 sha256 다름 · 없음 — 실행 안 함"')
    return out


def _operator_w2(man):
    """§12-2 (바) — W2: 본 런 압축 체크포인트 · 판 STL (mesh_<N>.stl → plate_<case>.stl) 복사 · sha256 둘 · 비준 전이면 제출 줄 막음."""
    case, fol, br, np_, n = man['case'], man['folder'], man['branch'], man['np'], man['s0']
    c = CASES[case]
    root, mf = c['run_root'], c['main_folder']
    src, dst = f'{mf}/restart_{case}/restart_compress_{n}.bin', f'{root}/{fol}/restart_{case}/restart_compress_{n}.bin'
    msrc, mdst = f'{mf}/post_{case}/mesh_{n}.stl', f'{root}/{fol}/plate_{case}.stl'
    rec, prec = f'{root}/{fol}/ckpt_sha256.txt', f'{root}/{fol}/{PLATE_RECORD}'
    draft = (man.get('amendment') or {}).get('status') != STATUS_RATIFIED
    out = [f'# ── {c["host"]} · {fol} (가지 {br} · 창 W2 · NP {np_} · 시작 step {n} = 본 런 첫 접촉 step '
           f'{man["w2_start"]["first_contact_step"]} 뒤 첫 restart_compress · §12-2 (라)) ──']
    if draft:
        out.append('# ⛔ §12-2 = 개정 초안 · 비준 전 — 실행 금지 (비준 뒤 생성기로 다시 만든다 · 아래 제출 줄은 막혀 있다)')
    out += [f'# 본 런 (kg50_d07_b50) 이 restart_compress_{n}.bin 을 쓴 뒤 멈춘 (scancel) 뒤에만 (§8-3 5) · cpu-60 = 가지는 차례로',
            f'cd {root}/{fol} && sha256sum -c SHA256SUMS',
            f'mkdir -p {root}/{fol}/restart_{case} && cp {src} {root}/{fol}/restart_{case}/',
            f'sha256sum {src} {dst} > {rec} && cat {rec}',
            f'cp {msrc} {mdst}',
            f'sha256sum {msrc} {mdst} > {prec} && cat {prec}']
    gate = _gate(rec) + ' && ' + _gate(prec)
    if draft:
        out.append('echo "⛔ §12-2 개정 초안 · 비준 전 — 제출 안 함 (비준 뒤 생성기로 다시 만든다)"')
    elif c['host'] == 'ibb':
        out.append(f'{gate} && (cd {root} && mkdir -p logs && sbatch {fol}/run_{fol}.sh) || echo "⛔ 체크포인트 · 판 STL sha256 다름 · '
                   '없음 — 제출 안 함"')
    else:
        out.append(f'{gate} && bash {root}/{fol}/run_{fol}.sh || echo "⛔ 체크포인트 · 판 STL sha256 다름 · 없음 — 실행 안 함"')
    return out


def _operator_local(man):
    """§12-3 — 로컬: hit 원본을 가져온 사본 (등록 Q1 sha256 대조) → 가지 폴더 cp · sha256 둘 → 러너 (직렬 · 자체 검사)."""
    case, fol, br, np_ = man['case'], man['folder'], man['branch'], man['np']
    root = LOCAL['root']
    rel = f'restart_{case}/restart_after_settling.bin'
    stage, hit_src = f'{root}/{case}/{rel}', f'{CASES[case]["main_folder"]}/{rel}'
    dst, rec = f'{root}/{fol}/{rel}', f'{root}/{fol}/ckpt_sha256.txt'
    stage_h = stage.replace('~', '$HOME', 1)
    return [f'# ── wsl · {fol} (가지 {br} · 로컬 직렬 1 코어 · MPI 실행기 없음 · NP {np_} · 등록 §12-3 이탈) ──',
            '# D3 정착 끝 체크포인트 = hit 원본을 가져온 사본 (A3 · C3 같은 사본 · hit 원본은 읽기만) — 등록 Q1 sha256 과 다르면 멈춤',
            f'mkdir -p {root}/{case}/restart_{case} && [ -s {stage} ] || scp <사용자>@<hit>:{hit_src} {root}/{case}/restart_{case}/',
            f'echo "{D3_CKPT_SHA256}  {stage_h}" | sha256sum -c || echo "⛔ 등록 Q1 sha256 아님 — 멈춤"',
            f'cd {root}/{fol} && sha256sum -c SHA256SUMS',
            f'mkdir -p {root}/{fol}/restart_{case} && cp {stage} {root}/{fol}/restart_{case}/',
            f'sha256sum {stage} {dst} > {rec} && cat {rec}',
            f'{_gate(rec)} && bash {root}/{fol}/run_{fol}.sh || echo "⛔ 체크포인트 sha256 다름 · 없음 — 실행 안 함"']


def _check_request(case, branch, np_, window, host=None, main_log=None):
    if _on('case') and case not in CASES:
        raise Refused(f'케이스 {case!r} 는 등록 침대가 아니다 (§2 · Q2: kg50_d07_b50 · kg50_d3_b50_s1 만)')
    if _on('branch') and (branch not in KIND or branch not in CASES[case]['branches']):
        raise Refused(f'가지 {branch!r} 는 {case} 의 등록 가지가 아니다 (§3 · {CASES[case]["branches"]} · B3 없음)')
    if _on('np') and NP.get(branch) != np_:
        raise Refused(f'가지 {branch} NP {np_} ≠ 등록 {NP.get(branch)} (Q5)')
    if _on('window') and window not in WINDOW_S:
        raise Refused(f'창 {window!r} — W1 (§4) · W2 (§12-2) 만')
    if _on('host'):
        if host not in (None, LOCAL['host']):
            raise Refused(f'host {host!r} — 등록 host (ibb · hit) 또는 wsl (§12-3 로컬 직렬) 만')
        if host == LOCAL['host']:
            if branch == 'F3':
                raise Refused(F3_LOCAL_REFUSAL)
            if case != LOCAL['case'] or branch not in LOCAL['branches']:
                raise Refused(f'로컬 직렬 (§12-3 · 1저자 10-28) = D3 A3 · C3 만 — {case} {branch} 는 등록 host ({CASES[case]["host"]})')
            if window != 'W1':
                raise Refused('로컬 직렬 (§12-3) = 창 W1 만 (W2 = D0.7 · §12-2)')
    if window == 'W2':
        if _on('w2_case') and case not in W2_CASES:
            raise Refused(f'W2 = D0.7-50 만 (§5 W2 표 · §12-2 · 질문 W2-6) — {case} 는 W2 가지가 없다')
        if not main_log:
            raise Refused('W2 = --main-log (D0.7-50 본 런 log.liggghts) 가 있어야 시작 step N 을 정한다 (§12-2 (라))')


def build_branch(case, branch, np_, out_parent, window='W1', main_deck=None, *, host=None, main_log=None, pinned=None,
                 runner_template=None, resume_tool=None, registration=None, tamper=None, q1=None):
    """가지 폴더 하나 — 반환 manifest.  거부 = Refused (파일 0).  pinned · runner_template · resume_tool · registration · tamper · q1 =
    selftest 이음새 (생산 CLI 에 없음)."""
    reg_path = registration or os.path.join(ROOT, REGISTRATION)
    if _on('registration'):
        ok, why = registration_check(reg_path)
        if not ok:
            raise Refused('등록 문서 고정 줄 ≠ 생성기 — ' + ' | '.join(why[:5]))
    _check_request(case, branch, np_, window, host, main_log)
    c = CASES[case]
    hsel = LOCAL['host'] if host == LOCAL['host'] else None
    status = None
    if window == 'W2':
        try:
            status = amendment_status(_read(reg_path))
        except OSError as e:
            raise Refused(f'등록 문서 못 읽음 ({e})')
        if status is None:
            if _on('w2_status'):
                raise Refused('§12-2 상태 줄을 정할 수 없다 (초안 · 비준 줄이 둘 다 있거나 둘 다 없다)')
            status = STATUS_DRAFT
    fol = folder_name(case, branch, window, hsel)
    dst = os.path.join(out_parent, fol)
    if _on('out_exists') and os.path.lexists(dst):
        raise Refused(f'{dst} 가 이미 있다 — 덮어쓰지 않는다')
    mpath = main_deck or os.path.join(ROOT, c['deck'])
    try:
        mbytes = open(mpath, 'rb').read()
        mtext = mbytes.decode('utf-8')
    except (OSError, UnicodeDecodeError) as e:
        raise Refused(f'본 덱 못 읽음 ({e})')
    msha = _sha256_bytes(mbytes)
    pin = pinned or pinned_sha(case)
    if _on('pin') and msha != pin:
        raise Refused(f'본 덱 sha256 {msha[:16]}… ≠ 등록 덱 {pin[:16]}… ({c["deck_manifest"]}) — 다른 덱이다')
    if _on('anchors'):
        p = check_anchors(mtext, case)
        if p:
            raise Refused('본 덱 고정 줄 (§4 행 번호) 다름 — ' + ' | '.join(p[:5]))
    d = derive(mtext, case)
    if d['s0'] != S0:
        raise Refused(f'본 덱 체크포인트 step {d["s0"]} ≠ 등록 {S0} (§2)')
    if (d['dt_token'], d['dt'] / 2) != ('1.0e-6', float(DT_HALF)) or d['runs'] != [1, 200000]:
        raise Refused(f'본 덱 dt · 안정화 run {d["dt_token"]} · {d["runs"]} ≠ 등록 (§4-2)')
    if d['contact_cols'] != CONTACT_COLS:
        raise Refused('본 덱 237 행 접촉 열 ≠ c_cpl[1] … c_cpl[26] (§4-5)')
    s_deck = s_from_deck(d)
    if _on('s_check') and KIND[branch] == 'damp' and '%.4e' % s_deck != '%.4e' % float(c['s']):
        raise Refused(f's (본 덱 ρ · r) {s_deck:.6e} ≠ 등록 {c["s"]} (§4-3 Q2 (가) · 다섯 자리)')
    kind = KIND[branch]
    n, start, lbytes = None, None, None
    if window == 'W2':
        try:
            lbytes = open(main_log, 'rb').read()
            ltext = lbytes.decode('utf-8')
        except (OSError, UnicodeDecodeError) as e:
            raise Refused(f'본 런 로그 못 읽음 ({e})')
        start = w2_start_from_log(ltext, case)
        start['log_sha256'] = _sha256_bytes(lbytes)
        n = start['n']
    text = build_text(mtext, case, branch, msha, window, n, status, start)
    if tamper is not None:
        text = tamper(text)
    if _on('allowlist'):
        p = verify_branch_deck(mtext, text, case, branch, window, n)
        if p:
            raise Refused('허용 목록 대조 실패 — ' + ' | '.join(p[:5]))
    rtext = render_runner(case, branch, np_, runner_template, window, hsel, q1)
    if _on('runner'):
        p = runner_check(case, branch, np_, rtext, window, hsel, q1)
        if p:
            raise Refused('러너 대조 실패 — ' + ' | '.join(p[:5]))
    dname, rname, mname = f'input_{fol}.liggghts', f'run_{fol}.sh', f'main_deck_{case}.liggghts'
    lname = f'main_log_{case}.liggghts'
    if window == 'W2':
        runs, s0 = [W2_RUN[kind]], n
        thermo = [W2_THERMO[kind]]
        every_a, every_c = W2_ATOM_EVERY, W2_CONTACT_EVERY
        ck_rel = f'restart_{case}/restart_compress_{n}.bin'
        exp_static = expected_static('W2', case, n)
    else:
        runs, s0 = ([2, 400000] if kind == 'dt_half' else list(d['runs'])), S0
        thermo = [2, 2000] if kind == 'dt_half' else [1, 1000]
        every_a, every_c = ATOM_EVERY, CONTACT_EVERY
        ck_rel = f'restart_{case}/restart_after_settling.bin'
        exp_static = expected_static('W1', case)
    dt = d['dt'] / 2 if kind == 'dt_half' else d['dt']
    end = s0 + sum(runs)
    with tempfile.TemporaryDirectory(prefix='q5chk_') as td:
        dp, mp = os.path.join(td, dname), os.path.join(td, mname)
        with open(dp, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
        with open(mp, 'wb') as f:
            f.write(mbytes)
        st = None
        if kind in ('base', 'floor'):
            st = static_check(mp, dp, case, resume_tool, ck_rel, s0)
            if _on('static') and (st['rc'] != 1 or st['problems'] != exp_static):
                raise Refused(f'resume_ckpt.sh -C 정적 대조 = rc {st["rc"]} · 문제 {st["problems"]} ≠ 등록 '
                              f'§12-4 {"W2 넷" if window == "W2" else "W1 셋"}')
    ed = _edits(case, branch, window)
    if window == 'W2':
        changes = [f'49–50 → read_restart restart_{case}/restart_compress_{n}.bin', '116–150 뺌 (삽입 · 삽입 검사)', '165 → restart 0',
                   '167 · 170 뺌 (정착 run · write_restart)', '171 뒤 → q5 덤프 둘 (atom 10000 · contact 100000)',
                   '172–197 뺌 (판 높이 run 1 · 판 STL print)', '213 뺌 (안정화 run)', '214–221 그대로 (압축 준비)', '222 → restart 0',
                   f'224–228 → run {W2_RUN[kind]} · 뒤 undump 둘 · 229–257 뺌']
    else:
        changes = ['49–50 → read_restart restart_%s/restart_after_settling.bin' % case, '116–150 뺌 (삽입 · 삽입 검사)',
                   '165 → restart 0', '167 · 170 뺌 (정착 run · write_restart)', '171 뒤 → q5 덤프 둘',
                   '213 뒤 → undump 둘 · 214–257 뺌']
    changes += [f'{ln} [{a}] → [{b}]' for ln, (a, b) in sorted(ed.items())]
    if hsel:
        site = dict(host=LOCAL['host'], launcher='serial', run_root=LOCAL['root'], main_folder=f'{LOCAL["root"]}/{case}',
                    binary=dict(env=LOCAL['env'], default=LOCAL['default'], fallback=LOCAL['fallback'], record=BINARY_RECORD,
                                mpi='거부 (ldd 에 libmpi)'),
                    deviation=dict(section='§12-3', text=LOCAL_DEVIATION))
    else:
        site = dict(host=c['host'], launcher='sbatch · mpirun' if c['host'] == 'ibb' else 'mpirun', run_root=c['run_root'],
                    main_folder=c['main_folder'], binary=None, deviation=None)
    man = dict(
        schema=SCHEMA, registration=REGISTRATION, registration_sha256=_sha256_file(reg_path),
        generator='scripts/kg50_q5_branches.py', generator_sha256=_sha256_file(os.path.abspath(__file__)),
        case=case, bed=c['bed'], branch=branch, kind=kind, window=window, np=np_, host=site['host'], launcher=site['launcher'],
        binary=site['binary'], deviation=site['deviation'], folder=fol, job_name=fol,
        main_deck=dict(repo_path=c['deck'], sha256=msha, pinned_by=c['deck_manifest'], copy=mname),
        deck=dict(file=dname, sha256=_sha256_bytes(text.encode('utf-8')), commands=len(commands(text))),
        runner=dict(file=rname, sha256=_sha256_bytes(rtext.encode('utf-8')), template=_rel(runner_template) if runner_template
                    else (None if hsel else RUNNER_TEMPLATE), main_runner=None if hsel else c['main_runner']),
        checkpoint=dict(rel_path=ck_rel, step=s0, source=f'{site["main_folder"]}/{ck_rel}', sha256_record='ckpt_sha256.txt',
                        registered_sha256=(q1 or D3_CKPT_SHA256) if hsel else None),
        dt=dt, dt_echo='%.15g' % dt, s0=s0, runs=runs, end_step=end, window_s=WINDOW_S['W2' if window == 'W2' else 'W1'],
        compare_step=end, thermo_every=thermo,
        atom_dump=dict(id='dq5a', every=every_a, dir=f'post_{case}', prefix='q5atom_', columns=list(ATOM_COLS),
                       steps=expected_steps(s0, end, every_a)),
        contact_dump=dict(id='dq5c', every=every_c, dir=f'post_{case}', prefix='q5contact_', columns=list(CONTACT_COLS),
                          steps=expected_steps(s0, end, every_c)),
        type_map={str(k): v for k, v in TYPE_MAP.items()}, density={str(k): v for k, v in d['density'].items()},
        radius_sim={str(k): v for k, v in d['radius'].items()}, area_sim=d['area'],
        damp=dict(gamma=0.5, scale=(dict(type=SE_TYPE, s=c['s'], s_from_deck='%.6e' % s_deck) if kind == 'damp' else None)),
        changes=changes, static_check=(None if st is None else {k: st[k] for k in ('rc', 'problems', 'notes', 'tool', 'tool_sha256')}),
        static_expected=exp_static if kind in ('base', 'floor') else None,
    )
    if window == 'W2':
        man['amendment'] = dict(section='§12-2', status=status)
        man['w2_start'] = dict(rule=start['rule'], n=n, first_contact_step=start['first_contact_step'],
                               first_contact_row=start['first_contact_row'], rows=start['rows'],
                               main_log=dict(copy=lname, sha256=start['log_sha256'], source=os.path.abspath(main_log)))
        man['plate'] = dict(rel_path=f'plate_{case}.stl', source=f'{c["main_folder"]}/post_{case}/mesh_{n}.stl',
                            sha256_record=PLATE_RECORD)
    man['operator_commands'] = operator_commands(man)
    mjson = json.dumps(man, ensure_ascii=False, indent=1) + '\n'
    files = {dname: text.encode('utf-8'), rname: rtext.encode('utf-8'), mname: mbytes, 'q5_manifest.json': mjson.encode('utf-8')}
    if window == 'W2':
        files[lname] = lbytes
    sums = ''.join(f'{_sha256_bytes(b)}  {nm}\n' for nm, b in sorted(files.items()))
    files['SHA256SUMS'] = sums.encode('utf-8')
    os.makedirs(out_parent, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix=f'.{fol}.tmp', dir=out_parent)
    try:
        for nm, b in files.items():
            with open(os.path.join(tmp, nm), 'wb') as f:
                f.write(b)
        os.rename(tmp, dst)
    finally:
        if os.path.isdir(tmp):
            shutil.rmtree(tmp)
    return man


def _manifest_expected(man, case, branch, window, n):
    """manifest 의 판정용 칸 (run · step · 덤프 간격 · 체크포인트) — 등록 상수로 다시 센 값과 같은가 · 문제 목록."""
    kind = KIND[branch]
    if window == 'W2':
        runs, s0, thermo, ea, ec = [W2_RUN[kind]], n, [W2_THERMO[kind]], W2_ATOM_EVERY, W2_CONTACT_EVERY
        ck = f'restart_{case}/restart_compress_{n}.bin'
    else:
        runs, s0 = ([2, 400000] if kind == 'dt_half' else [1, 200000]), S0
        thermo, ea, ec = ([2, 2000] if kind == 'dt_half' else [1, 1000]), ATOM_EVERY, CONTACT_EVERY
        ck = f'restart_{case}/restart_after_settling.bin'
    end = s0 + sum(runs)
    dt = 5e-07 if kind == 'dt_half' else 1e-06
    want = dict(runs=runs, s0=s0, end_step=end, compare_step=end, thermo_every=thermo, dt=dt, dt_echo='%.15g' % dt,
                window_s=WINDOW_S['W2' if window == 'W2' else 'W1'])
    probs = [f'manifest {k} {man.get(k)!r} ≠ 등록 {v!r}' for k, v in want.items() if man.get(k) != v]
    for key, ev in (('atom_dump', ea), ('contact_dump', ec)):
        dd = man.get(key) or {}
        if dd.get('every') != ev or dd.get('steps') != expected_steps(s0, end, ev):
            probs.append(f'manifest {key} 간격 · step ≠ 등록 ({ev})')
    if (man.get('checkpoint') or {}).get('rel_path') != ck or (man.get('checkpoint') or {}).get('step') != s0:
        probs.append(f'manifest 체크포인트 ≠ [{ck}] (step {s0})')
    return probs


def _verify_w2(folder, man, db):
    """W2 폴더 — 본 런 로그 사본 sha256 · 시작 step 다시 계산 (§12-2 (라)) · 개정 상태 = 덱 머리 · 반환 (문제, N 또는 None)."""
    probs = []
    st = (man.get('amendment') or {}).get('status')
    if st not in (STATUS_DRAFT, STATUS_RATIFIED):
        probs.append(f'manifest §12-2 상태 {st!r} 를 모른다')
    elif f'#   §12-2 상태: {st}' not in db.decode('utf-8', 'replace').split('\n'):
        probs.append('덱 머리의 §12-2 상태 ≠ manifest')
    ws = man.get('w2_start') or {}
    ml = ws.get('main_log') or {}
    try:
        lb = open(os.path.join(folder, ml.get('copy') or ''), 'rb').read()
    except (OSError, TypeError) as e:
        return probs + [f'본 런 로그 사본 못 읽음 ({e})'], None
    if _sha256_bytes(lb) != ml.get('sha256'):
        probs.append('본 런 로그 사본 sha256 ≠ manifest')
    try:
        start = w2_start_from_log(lb.decode('utf-8'), man['case'])
    except (Refused, UnicodeDecodeError) as e:
        return probs + [f'본 런 로그 사본으로 시작 step 을 다시 못 정함 ({e})'], None
    if (start['n'], start['first_contact_step']) != (man.get('s0'), ws.get('first_contact_step')) or ws.get('n') != start['n']:
        probs.append(f'시작 step 다시 계산 {start["n"]} (첫 접촉 {start["first_contact_step"]}) ≠ manifest {man.get("s0")} '
                     f'(첫 접촉 {ws.get("first_contact_step")})')
    return probs, start['n']


def verify_folder(folder):
    """만든 가지 폴더 다시 대조 (판독기 · 운영자) — 문제 목록.  manifest · 본 덱 사본 sha256 = 등록 덱 · 가지 덱 허용 목록 · 러너 ·
    판정용 칸 (run · step · 덤프) · W2 = 본 런 로그로 시작 step 다시 계산."""
    probs = []
    try:
        man = json.loads(_read(os.path.join(folder, 'q5_manifest.json')))
    except (OSError, ValueError) as e:
        return [f'q5_manifest.json 못 읽음 ({e})']
    if man.get('schema') != SCHEMA:
        return [f'manifest schema {man.get("schema")!r} ≠ {SCHEMA}']
    case, branch, window = man.get('case'), man.get('branch'), man.get('window')
    reg_host = CASES[case]['host'] if case in CASES else None
    host = man.get('host', reg_host)
    hsel = LOCAL['host'] if host == LOCAL['host'] else None
    if (case not in CASES or branch not in CASES[case]['branches'] or window not in WINDOW_S or host not in (reg_host, LOCAL['host'])
            or (window == 'W2' and case not in W2_CASES)
            or (hsel and (case != LOCAL['case'] or branch not in LOCAL['branches'] or window != 'W1'))):
        return [f'manifest 의 케이스 · 가지 · 창 · host ({case} · {branch} · {window} · {host}) 가 등록 가지가 아니다 (§3 · §12-2 · §12-3)']
    if man.get('folder') != folder_name(case, branch, window, hsel):
        probs.append(f'manifest 폴더 이름 {man.get("folder")!r} ≠ {folder_name(case, branch, window, hsel)!r}')
    try:
        mb = open(os.path.join(folder, man['main_deck']['copy']), 'rb').read()
        db = open(os.path.join(folder, man['deck']['file']), 'rb').read()
        rb = open(os.path.join(folder, man['runner']['file']), 'rb').read()
    except (OSError, KeyError, TypeError) as e:
        return [f'폴더 파일 못 읽음 ({e})']
    pin = pinned_sha(case)
    if _sha256_bytes(mb) != pin or man['main_deck'].get('sha256') != pin:
        probs.append('본 덱 사본 sha256 ≠ 등록 덱 (manifest · 덱 묶음)')
    if _sha256_bytes(db) != man['deck'].get('sha256'):
        probs.append('가지 덱 sha256 ≠ manifest')
    if _sha256_bytes(rb) != man['runner'].get('sha256'):
        probs.append('러너 sha256 ≠ manifest')
    n = None
    if window == 'W2':
        p, n = _verify_w2(folder, man, db)
        probs += p
        if n is None:
            return probs
    probs += _manifest_expected(man, case, branch, window, n)
    probs += verify_branch_deck(mb.decode('utf-8'), db.decode('utf-8'), case, branch, window, n)
    probs += runner_check(case, branch, man.get('np'), rb.decode('utf-8'), window, hsel)
    if type(man.get('np')) is not int or NP.get(branch) != man.get('np'):     # JSON true 는 1 과 같다고 나온다
        probs.append(f'manifest NP {man.get("np")!r} ≠ 등록 {NP.get(branch)} (Q5)')
    return probs


def main(argv=None):
    ap = argparse.ArgumentParser(description='50kg Q5 가지 덱 생성기 (등록 Q11 · W1 · W2 = §12-2 개정 초안 · 로컬 직렬 = §12-3)')
    ap.add_argument('--case', choices=sorted(CASES), help='본 덱 케이스 (등록 §2)')
    ap.add_argument('--branch', help='가지 (D0.7: A B C F · D3: A3 C3 F3)')
    ap.add_argument('--np', type=int, help='MPI 수 (등록 Q5 와 같아야 한다 · 로컬 직렬 = 1)')
    ap.add_argument('--out', help='가지 폴더를 만들 상위 폴더 (그 안에 q5_<case>_<가지>/ · 이미 있으면 거부 · 로컬 = ~/q5_local)')
    ap.add_argument('--window', default='W1', help='창 (W1 · W2 = 등록 §12-2 개정 초안 · --main-log 필요)')
    ap.add_argument('--main-log', default=None, help='W2 — D0.7-50 본 런 log.liggghts (시작 step N 을 이 로그에서 계산 · §12-2 (라))')
    ap.add_argument('--host', default=None, help='wsl = D3 A3 · C3 로컬 직렬 1 코어 (등록 §12-3) · 없으면 등록 host (ibb · hit)')
    ap.add_argument('--main-deck', default=None, help='본 덱 경로 (기본 = 리포 덱 · sha256 이 등록 덱과 같아야)')
    ap.add_argument('--verify', default=None, metavar='FOLDER', help='만든 가지 폴더를 다시 대조 (rc 0 = 통과)')
    ap.add_argument('--w2-start', default=None, metavar='LOG',
                    help='운영 — 본 런 log.liggghts 로 W2 시작 step 판단 (§12-2 (라) · 본 런을 멈춰도 되는가) · rc 0 ready · 3 기다림 · 2 거부')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.w2_start:
        case = a.case or W2_CASES[0]
        try:
            with open(os.path.expanduser(a.w2_start), encoding='utf-8') as f:
                r = w2_watch(f.read(), case)
        except (OSError, UnicodeDecodeError) as e:
            print(f'⛔ 본 런 로그 못 읽음 ({e})')
            return 2
        if r['status'] == 'ready':
            print(f'✓ ready — 첫 접촉 step {r["first_contact_step"]} · N = {r["n"]} · 로그가 N 까지 다 있다 (§12-2 (라)) → 본 런 '
                  f'restart_{case}/restart_compress_{r["n"]}.bin 이 있으면 본 런을 멈추고 (scancel) 생성기 --window W2 --main-log')
            return 0
        if r['status'] == 'no_contact':
            print(f'… 접촉 전 — pressMPa > 0 줄 없음 (setup 줄 빼고 · 로그 마지막 step {r["last"]}) → 기다림')
            return 3
        if r['status'] == 'wait':
            print(f'… 첫 접촉 step {r["first_contact_step"]} · N = {r["n"]} · 로그 마지막 step {r["last"]} < N → 기다림 (멈추지 않는다)')
            return 3
        print(f'⛔ N = {r["n"]} 을 지났는데 규칙 거부 (첫 접촉 step {r["first_contact_step"]}) — {r["why"]} → 1저자')
        return 2
    if a.verify:
        p = verify_folder(a.verify)
        for x in p:
            print('  ✗ ' + x)
        print(f'가지 폴더 대조: {"통과" if not p else "실패"} (문제 {len(p)})')
        return 0 if not p else 2
    if not (a.case and a.branch and a.np is not None and a.out):
        print('⛔ --case · --branch · --np · --out 이 다 필요하다 (또는 --verify · --selftest)')
        return 2
    try:
        man = build_branch(a.case, a.branch, a.np, os.path.expanduser(a.out), a.window, a.main_deck, host=a.host,
                           main_log=os.path.expanduser(a.main_log) if a.main_log else None)
    except Refused as e:
        print(f'⛔ 거부 — 가지 덱 안 냄 (파일 0): {e}')
        return 2
    dst = os.path.join(os.path.expanduser(a.out), man['folder'])
    print(f'✓ {dst}/  가지 {man["branch"]} ({man["kind"]}) · NP {man["np"]} · {man["host"]} ({man["launcher"]}) · 창 {man["window"]} · '
          f'끝 step {man["end_step"]} · atom 덤프 {len(man["atom_dump"]["steps"])} · contact {len(man["contact_dump"]["steps"])}')
    if man['window'] == 'W2':
        print(f'  W2 시작 step N = {man["s0"]} (본 런 첫 접촉 step {man["w2_start"]["first_contact_step"]} · §12-2 (라)) · '
              f'§12-2 상태 = {man["amendment"]["status"]}')
        if man['amendment']['status'] != STATUS_RATIFIED:
            print('  ⚠ §12-2 = 개정 초안 · 비준 전 — 실행 금지 (비준 뒤 다시 만든다 · 운영자 제출 줄 막힘 · 판독기 거부)')
    if man['deviation']:
        print(f'  ⚠ 이탈 기록: {man["deviation"]["text"]}')
    for x in man['changes']:
        print('    · ' + x)
    if man['static_check'] is not None:
        print(f'  resume_ckpt.sh -C = rc {man["static_check"]["rc"]} · 문제 {man["static_check"]["problems"]} (등록 '
              f'{"§12-2 (마) 둘" if man["window"] == "W2" else "§8-1 하나"} = 통과)')
    print('\n# 운영자 (복사 · sha256 · 제출 — 1저자):')
    if man['host'] == LOCAL['host']:
        if os.path.realpath(os.path.expanduser(a.out)) != os.path.realpath(os.path.expanduser(LOCAL['root'])):
            print(f'# 러너는 {LOCAL["root"]}/{man["folder"]} 로 cd 한다 — --out 이 {LOCAL["root"]} 가 아니면 폴더를 그리로 옮긴다')
    elif man['host'] == 'ibb':
        print(f'scp -P <포트> -r {dst} <사용자>@<ibb>:{CASES[man["case"]]["run_root"]}/')
    else:
        print(f'scp -r {dst} <사용자>@<hit>:{CASES[man["case"]]["run_root"]}/')
    for x in man['operator_commands']:
        print(x)
    return 0


# ───────────────────────────── selftest ─────────────────────────────
def selftest():
    import io
    import time
    from contextlib import redirect_stdout
    tally = [0, 0]

    def chk(label, cond, extra=''):
        tally[1] += 1
        tally[0] += bool(cond)
        print(f'  {"✓" if cond else "✗"} {label}{(" — " + str(extra)[:300]) if extra and not cond else ""}')

    def run(label, fn):
        try:
            fn()
        except (Exception, SystemExit) as e:    # noqa: BLE001 — 구현 전 · 예외 (모르는 CLI 인자 = argparse SystemExit) = 그 묶음 실패
            chk(f'{label} (예외)', False, f'{type(e).__name__}: {e}')

    def refused(fn, needle=None):
        try:
            fn()
        except Refused as e:
            return needle is None or needle in str(e)
        except Exception:               # noqa: BLE001
            return False
        return False

    print('kg50_q5_branches selftest')
    ok, why = registration_check()
    chk('⓪ 등록 문서 고정 줄 (§2 · §3 · §4-1 · §4-2 · §4-3 · §4-5 · §5 · §8 · §12 · Q1 · Q2 · Q3 · Q5 · Q11 · Q12) = 생성기 상수', ok, why)
    ok, why = source_premise_check()
    chk('⓪b LIGGGHTS 3d5c00f 원문 사본 — restart 머리에 dt 없음 · units 같으면 재설정 안 함 → B 의 43 행 dt 가 살아남는다', ok, why)
    D07, D3 = 'kg50_d07_b50', 'kg50_d3_b50_s1'
    repo_before = {c: _sha256_file(os.path.join(ROOT, CASES[c]['deck'])) for c in CASES}
    reg_txt = _read(os.path.join(ROOT, REGISTRATION))

    def reg_static(window, case, n=None):
        """등록 §12-4 (1저자 10-28 밤 Q5-S1) 의 정적 대조 기대 — 등록 글자에서 직접 읽는다 (생성기 상수와 따로)."""
        sec = reg_txt.split('### 12-4.', 1)[1].split('\n### ', 1)[0]
        part = sec.split('\n' + ('W1 —' if window == 'W1' else 'W2 —'), 1)[1]
        out = []
        for ln in part.split('\n')[1:]:
            m_ = re.match(r'^[0-9]+\. `(.+)`$', ln)
            if m_:
                out.append(m_.group(1).replace('<case>', case).replace('<N>', str(n)))
            elif out and ln.strip():
                break
        return out
    tmp = tempfile.mkdtemp(prefix='q5st_')
    built, w2, loc = {}, {}, {}
    try:
        def status_tests():
            rat = reg_txt.replace(W2_STATUS_DRAFT, '> **§12-2 상태: ✅ 1저자 비준 (10-29)**', 1)
            both = reg_txt.replace(W2_STATUS_DRAFT, W2_STATUS_DRAFT + '\n> **§12-2 상태: ✅ 1저자 비준 (10-29)**', 1)
            none = reg_txt.replace(W2_STATUS_DRAFT, '> **§12-2 상태: ?**', 1)
            chk('⓪c §12-2 상태 — 지금 등록 = 개정 초안 · 비준 전 · ✅ 줄로 바꾸면 비준 · 둘 다 · 둘 다 없음 = 정할 수 없음 (None)',
                [amendment_status(x) for x in (reg_txt, rat, both, none)] == [STATUS_DRAFT, STATUS_RATIFIED, None, None])
        run('⓪c 상태', status_tests)
        chk('⓪d 등록 §12-4 정적 대조 기대 = W1 셋 · W2 넷 (등록 글자 · <case> · <N> 자리)',
            len(reg_static('W1', D07)) == 3 and len(reg_static('W2', D07, 800000)) == 4
            and all('kg50_d07_b50' in x for x in reg_static('W1', D07)[:1])
            and reg_static('W2', D07, 800000)[0].endswith('restart_compress_800000.bin (이름 restart_compress_*)'))

        def g_build():
            for case in (D07, D3):
                for br in CASES[case]['branches']:
                    built[br] = build_branch(case, br, NP[br], os.path.join(tmp, 'out'))
        run('G0 일곱 가지 만들기', g_build)

        def rd(br, which='deck', b=None, sub='out'):
            m = (b or built)[br]
            return _read(os.path.join(tmp, sub, m['folder'], m[which]['file']))

        def g1():
            m = built['A']
            fol = os.path.join(tmp, 'out', 'q5_kg50_d07_b50_A')
            chk('G1 A 폴더 = 가지 덱 · 러너 · 본 덱 사본 · manifest · SHA256SUMS (다섯 파일)',
                sorted(os.listdir(fol)) == sorted(['input_q5_kg50_d07_b50_A.liggghts', 'run_q5_kg50_d07_b50_A.sh',
                                                   'main_deck_kg50_d07_b50.liggghts', 'q5_manifest.json', 'SHA256SUMS']),
                os.listdir(fol))
            chk('G1b A manifest — 체크포인트 step 200001 · 끝 400002 · atom 덤프 4 (200001 · 266668 · 333335 · 400002) · contact 2',
                m['s0'] == 200001 and m['end_step'] == 400002 and m['atom_dump']['steps'] == [200001, 266668, 333335, 400002]
                and m['contact_dump']['steps'] == [200001, 400002] and m['compare_step'] == 400002, m.get('atom_dump'))
            chk('G1c A 정적 대조 (resume_ckpt.sh -C) = rc 1 · 문제 셋 = 등록 §12-4 W1 글자 (10-28 밤 개정 · §8-1 앞섬)',
                m['static_check']['rc'] == 1 and m['static_check']['problems'] == reg_static('W1', D07), m['static_check'])
            cmds = [x for x, _a, _b in commands(_strip_header(rd('A')))]
            chk('G1d A 덱 명령 — read_restart 한 번 (49 행 자리) · 삽입 fix 0 · write_restart 0 · restart 0 · run 1 · run 200000 만',
                cmds.count('read_restart restart_kg50_d07_b50/restart_after_settling.bin') == 1
                and not any(' insert/' in x for x in cmds) and not any(x.startswith('write_restart') for x in cmds)
                and [x for x in cmds if x.startswith('run ')] == ['run 1', 'run 200000'] and 'restart 0' in cmds
                and cmds.index('read_restart restart_kg50_d07_b50/restart_after_settling.bin') == 15
                and cmds[14] == 'processors * * 1' and cmds[13] == 'timestep ${dt}', cmds[:16])
            dumps = _dump_lines(D07)
            chk('G1e q5 덤프 둘 = §4-5 글자 (<폴더> = post_kg50_d07_b50) · 172 행 앞 · undump 둘 = 213 행 run 뒤 끝',
                cmds[cmds.index('print "====== RESTART SAVED ======"') + 1: cmds.index('print "====== RESTART SAVED ======"') + 3] == dumps
                and cmds[-3:] == ['run 200000', 'undump dq5a', 'undump dq5c']
                and dumps[0] == 'dump dq5a all custom 66667 post_kg50_d07_b50/q5atom_*.liggghts id type x y z radius vx vy vz'
                and dumps[1].startswith('dump dq5c all local 200001 post_kg50_d07_b50/q5contact_*.liggghts c_cpl[1] c_cpl[2] ')
                and dumps[1].endswith(' c_cpl[26]') and len(dumps[1].split()) == 6 + 26, cmds[-4:])
            mtext = _read(os.path.join(ROOT, CASES[D07]['deck']))
            mlines = mtext.split('\n')
            body = _strip_header(rd('A')).split('\n')
            kept = [x for x in body if x not in dumps + UNDUMP_LINES and x not in ('read_restart restart_kg50_d07_b50/restart_after_settling.bin',
                                                                                     'restart 0')]
            want = [mlines[k - 1] for k in range(1, MAIN_NLINES + 1) if k not in DROP_LINES and k not in (READ_RESTART_LINE, RESTART0_LINE)]
            chk('G1f A 의 나머지 줄 = 본 덱 줄 바이트 그대로 (뺀 행 · 바꾼 행 밖 · 순서 그대로)', kept[:-1] == want and kept[-1] == '',
                (len(kept), len(want)))
            rtext = rd('A', 'runner')
            chk('G1g A 러너 = #SBATCH -n 56 ↔ mpirun -np 56 · cd $HOME/dem_test/q5_kg50_d07_b50_A · 잡 이름 q5_ (재개 도구 큐 이름과 안 겹침)',
                '#SBATCH -n 56' in rtext and 'mpirun --oversubscribe --bind-to none -np 56 lmp_mpi -in input_q5_kg50_d07_b50_A.liggghts' in rtext
                and 'cd $HOME/dem_test/q5_kg50_d07_b50_A' in rtext and '#SBATCH --job-name=q5_kg50_d07_b50_A' in rtext
                and runner_check(D07, 'A', 56, rtext) == [], rtext)
            main_r = _read(os.path.join(ROOT, CASES[D07]['main_runner'])).split('\n')

            def rdiff(t):
                return [main_r[i].split('=')[0].split(' ')[0] + ('' if not main_r[i].startswith('#SBATCH') else ' ' + main_r[i].split()[1].split('=')[0])
                        for i, (x, y) in enumerate(zip(main_r, t.split('\n'))) if x != y]
            chk('G1h 러너 ↔ 본 러너 run_kg50_d07_b50.sh — A = 넷만 다름 (job-name · output · cd · mpirun · -n 56 은 같다) · '
                'F = 다섯 (-n 28 더)', len(main_r) == len(rtext.split('\n'))
                and rdiff(rtext) == ['#SBATCH --job-name', '#SBATCH --output', 'cd', 'mpirun']
                and rdiff(rd('F', 'runner')) == ['#SBATCH --job-name', '#SBATCH --output', '#SBATCH -n', 'cd', 'mpirun'],
                (rdiff(rtext), rdiff(rd('F', 'runner'))))
            head = rd('A').split('\n')[:rd('A').split('\n').index(HEADER_END) + 1]
            chk('G1j 가지 덱 머리 = 주석 줄만 · & 로 끝나는 줄 없음 (LIGGGHTS 이어 붙이기) · ERROR 낱말 없음 (판독기 로그 ERROR 검사)',
                all(x.startswith('#') and not x.rstrip().endswith('&') and 'ERROR' not in x for x in head)
                and not any('ERROR' in x for x in rd('B').split('\n') + rd('C').split('\n')), head)
            sums = _read(os.path.join(fol, 'SHA256SUMS')).split('\n')
            chk('G1i SHA256SUMS = 네 파일 sha256 (sha256sum -c 꼴) · manifest 의 가지 덱 · 본 덱 sha256 과 같음',
                len([x for x in sums if x]) == 4 and all(_sha256_file(os.path.join(fol, x.split('  ')[1])) == x.split('  ')[0]
                                                         for x in sums if x)
                and m['deck']['sha256'] == _sha256_file(os.path.join(fol, m['deck']['file']))
                and m['main_deck']['sha256'] == repo_before[D07], sums)
        run('G1 A', g1)

        def g2():
            ca = [x for x, _a, _b in commands(_strip_header(rd('A')))]
            cb = [x for x, _a, _b in commands(_strip_header(rd('B')))]
            dif = [(x, y) for x, y in zip(ca, cb) if x != y]
            chk('G2 B ↔ A = 명령 여섯만 다름 (§4-2: dt 5.0e-7 · thermo 2 · run 2 · mesh 10000 · thermo 2000 · run 400000)',
                len(ca) == len(cb) and dif == [('variable dt equal 1.0e-6', 'variable dt equal 5.0e-7'), ('thermo 1', 'thermo 2'),
                                               ('run 1', 'run 2'),
                                               ('dump dmp_mesh all mesh/stl 5000 post_kg50_d07_b50/mesh_*.stl top_mesh',
                                                'dump dmp_mesh all mesh/stl 10000 post_kg50_d07_b50/mesh_*.stl top_mesh'),
                                               ('thermo 1000', 'thermo 2000'), ('run 200000', 'run 400000')], dif)
            m = built['B']
            chk('G2b B manifest — dt 5e-07 (로그 치환 글자 5e-07) · 끝 600003 · atom 덤프 7 · contact 3 (200001 · 400002 · 600003) · 간격 그대로',
                m['dt'] == 5e-07 and m['dt_echo'] == '5e-07' and m['end_step'] == 600003 and len(m['atom_dump']['steps']) == 7
                and m['contact_dump']['steps'] == [200001, 400002, 600003] and m['atom_dump']['every'] == 66667
                and m['runs'] == [2, 400000] and m['thermo_every'] == [2, 2000], m)
            chk('G2c B 의 같은 시각 = A 시각 ×2 (A 400002 ↔ B 600003 · 333335 ↔ 466669) · 창 0.200001 s',
                (600003 - S0) * 5e-07 == (400002 - S0) * 1e-06 and 466669 in m['atom_dump']['steps'] and m['window_s'] == '0.200001')
            chk('G2d B 는 정적 대조를 판정하지 않는다 (허용 목록 대조만 · §8-1) · NP 56', m['static_check'] is None and m['np'] == 56)
        run('G2 B', g2)

        def g3():
            ca = [x for x, _a, _b in commands(_strip_header(rd('A')))]
            cc = [x for x, _a, _b in commands(_strip_header(rd('C')))]
            dif = [(x, y) for x, y in zip(ca, cc) if x != y]
            chk('G3 C ↔ A = 명령 하나 (208 행 fix damp all viscous 0.5 scale 3 5.3696e-4)',
                len(ca) == len(cc) and dif == [('fix damp all viscous 0.5', 'fix damp all viscous 0.5 scale 3 5.3696e-4')], dif)
            c3a = [x for x, _a, _b in commands(_strip_header(rd('A3')))]
            c3c = [x for x, _a, _b in commands(_strip_header(rd('C3')))]
            dif3 = [(x, y) for x, y in zip(c3a, c3c) if x != y]
            chk('G3b C3 ↔ A3 = 명령 하나 (scale 3 4.2268e-2)',
                dif3 == [('fix damp all viscous 0.5', 'fix damp all viscous 0.5 scale 3 4.2268e-2')], dif3)
            chk('G3c s = 본 덱 ρ · r 로 다시 센 값의 다섯 자리 (5.369607e-04 · 4.226804e-02)',
                built['C']['damp']['scale']['s_from_deck'] == '5.369607e-04'
                and built['C3']['damp']['scale']['s_from_deck'] == '4.226804e-02', (built['C']['damp'], built['C3']['damp']))
            chk('G3d 정착 감쇠 161 행 1.0e-5 · AM (type 1) 은 C 에서도 그대로',
                'fix damp all viscous 1.0e-5' in cc and cc.count('fix damp all viscous 0.5 scale 3 5.3696e-4') == 1)
        run('G3 C', g3)

        def g4():
            chk('G4 F 덱 = A 덱 바이트 그대로 · F3 = A3 (§4-4)', rd('F') == rd('A') and rd('F3') == rd('A3'))
            chk('G4b F 러너 -n 28 ↔ -np 28 · F3 hit 명령 -np 2 · A3 · C3 -np 1',
                '#SBATCH -n 28' in rd('F', 'runner') and '-np 28 lmp_mpi' in rd('F', 'runner')
                and '-np 2 $HOME/LIGGGHTS-PUBLIC/src/lmp_auto -in input_q5_kg50_d3_b50_s1_F3.liggghts' in rd('F3', 'runner')
                and '-np 1 $HOME/LIGGGHTS-PUBLIC/src/lmp_auto' in rd('A3', 'runner') and '-np 1 ' in rd('C3', 'runner'))
            chk('G4c F · F3 · A3 정적 대조 = 등록 §12-4 W1 셋 (케이스 이름 자리)', built['F']['static_check']['problems'] == reg_static('W1', D07)
                and built['F3']['static_check']['problems'] == reg_static('W1', D3)
                and built['A3']['static_check']['problems'] == reg_static('W1', D3))
        run('G4 F', g4)

        def g5():
            m = built['A3']
            chk('G5 D3 — hit · ~/simulation/q5_kg50_d3_b50_s1_<X> · read_restart restart_kg50_d3_b50_s1/… · post_kg50_d3_b50_s1 덤프',
                m['host'] == 'hit' and m['folder'] == 'q5_kg50_d3_b50_s1_A3'
                and 'read_restart restart_kg50_d3_b50_s1/restart_after_settling.bin' in rd('A3')
                and 'post_kg50_d3_b50_s1/q5atom_*.liggghts' in rd('A3') and m['end_step'] == 400002)
            chk('G5b 가지 일곱의 폴더 이름 = §8-2 예 그대로', sorted(x['folder'] for x in built.values()) ==
                sorted(['q5_kg50_d07_b50_A', 'q5_kg50_d07_b50_B', 'q5_kg50_d07_b50_C', 'q5_kg50_d07_b50_F',
                        'q5_kg50_d3_b50_s1_A3', 'q5_kg50_d3_b50_s1_C3', 'q5_kg50_d3_b50_s1_F3']))
        run('G5 D3', g5)

        def g6():
            oa = built['A']['operator_commands']
            src = '~/dem_test/kg50_d07_b50/restart_kg50_d07_b50/restart_after_settling.bin'
            dst = '~/dem_test/q5_kg50_d07_b50_A/restart_kg50_d07_b50/restart_after_settling.bin'
            chk('G6 운영자 명령 (ibb A) — 원 체크포인트는 cp 로 읽기만 · 두 sha256 → ckpt_sha256.txt · 같을 때만 sbatch (logs/ 제출 폴더)',
                f'mkdir -p ~/dem_test/q5_kg50_d07_b50_A/restart_kg50_d07_b50 && cp {src} ~/dem_test/q5_kg50_d07_b50_A/restart_kg50_d07_b50/' in oa
                and f'sha256sum {src} {dst} > ~/dem_test/q5_kg50_d07_b50_A/ckpt_sha256.txt && cat ~/dem_test/q5_kg50_d07_b50_A/ckpt_sha256.txt' in oa
                and any('sbatch q5_kg50_d07_b50_A/run_q5_kg50_d07_b50_A.sh' in x and 'mkdir -p logs' in x and 'sort -u | wc -l' in x
                        and '[ "$(wc -l < ~/dem_test/q5_kg50_d07_b50_A/ckpt_sha256.txt)" = 2 ]' in x for x in oa)
                and not any(' > ' + src in x or 'rm ' in x or 'mv ' in x for x in oa), oa)
            o3 = built['C3']['operator_commands']
            chk('G6b 운영자 명령 (hit C3) — Q1 ls -l 확인 줄 · ~/simulation/kg50_d3_b50_s1 원본 cp · 같을 때만 bash run_…sh',
                any(x.startswith('ls -l ~/simulation/kg50_d3_b50_s1/restart_kg50_d3_b50_s1/restart_after_settling.bin') for x in o3)
                and any('bash ~/simulation/q5_kg50_d3_b50_s1_C3/run_q5_kg50_d3_b50_s1_C3.sh' in x for x in o3), o3)
        run('G6 운영자 명령', g6)

        def g7():
            chk('G7 리포 본 덱 두 개 바이트 그대로 (원본 안 고침)',
                all(_sha256_file(os.path.join(ROOT, CASES[c]['deck'])) == repo_before[c] for c in CASES))
            fol = os.path.join(tmp, 'out', 'q5_kg50_d07_b50_C')
            chk('G7b --verify (만든 폴더 다시 대조) = 문제 0 (일곱 다)',
                all(verify_folder(os.path.join(tmp, 'out', m['folder'])) == [] for m in built.values()), verify_folder(fol))
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = main(['--verify', fol])
            chk('G7c CLI --verify rc 0', rc == 0, buf.getvalue()[-300:])
            chk('G7d W1 manifest — host · 실행 방식 기록 (ibb sbatch · mpirun · hit mpirun) · 이탈 없음 (등록 host)',
                (built['A']['host'], built['A']['launcher'], built['A3']['host'], built['A3']['launcher'], built['A']['deviation'],
                 built['C3']['binary']) == ('ibb', 'sbatch · mpirun', 'hit', 'mpirun', None, None))
        run('G7 원본 · 다시 대조', g7)

        # ── §12-2 (라) W2 시작 step — 본 런 로그 규칙 ──
        logs = {}

        def l_all():
            def n_of(**kw):
                return w2_start_from_log(synth_main_log(D07, **kw), D07)
            r = n_of(first_contact=712000, last=820000)
            chk('L1 첫 접촉 712,000 (setup 아닌 줄) → N 800,000 · 근거 줄 = 712000 행 · 정규 줄 수',
                (r['n'], r['first_contact_step'], r['first_contact_row'].split()[0]) == (800000, 712000, '712000') and r['rows'] > 600, r)
            chk('L1b S_c 가 200,000 배수 (800,000) → N = S_c', n_of(first_contact=800000, last=820000)['n'] == 800000)
            chk('L1c 안정화 중 한 줄만 > 0 (250,000) → S_c 250,000 · N 600,000 (압축 뒤 첫 restart_compress)',
                (lambda x: (x['first_contact_step'], x['n']))(n_of(first_contact=712000, last=820000, stab_contact=250000))
                == (250000, 600000))
            r = n_of(first_contact=712000, last=820000, setup_spike=595002)
            chk('L1d setup 줄만 > 0 (595,002 · run 시작 줄) 은 뺀다 → S_c 712,000 · N 800,000 (그 줄을 셌다면 N 600,000)',
                (r['first_contact_step'], r['n']) == (712000, 800000), r)
            bad = [('L2 1,000 배수 줄 하나 빠짐 (750,000)', dict(drop=(750000,)), '빠짐'),
                   ('L2b 같은 step 줄 둘 (750,000)', dict(dup=(750000,)), '둘'),
                   ('L2c pressMPa nan', dict(bad=(750000, 'nan')), '글자'),
                   ('L2d pressMPa 음수', dict(bad=(750000, '-0.5')), '글자'),
                   ('L2e pressMPa 유니코드 숫자', dict(bad=(750000, '١')), '글자'),
                   ('L2f 열 수 다른 줄', dict(extra_col=750000), '열 수'),
                   ('L2g ERROR 줄', dict(error=True), 'ERROR'),
                   ('L2h dt 치환 5e-07 (바뀐 덱 · Q7)', dict(dt_echo='5e-07'), 'timestep 1e-06'),
                   ('L2i 감쇠 줄 없음 (바뀐 규약 · Q8)', dict(echo_drop='fix damp all viscous 0.5'), 'fix damp all viscous 0.5'),
                   ('L2j restart_compress echo 없음 (다른 런)', dict(echo_drop='restart 200000 restart_kg50_d07_b50/restart_compress_*.bin'),
                    'restart_compress'),
                   ('L2k 로그가 N 에 못 미침 (790,000 까지)', dict(last=790000), '빠짐')]
            for label, kw, needle in bad:
                kw = dict(dict(first_contact=712000, last=820000), **kw)
                chk(f'{label} → 거부', refused(lambda kw=kw: n_of(**kw), needle))
            chk('L2l pressMPa > 0 줄 없음 (접촉 전) → 거부', refused(lambda: n_of(first_contact=900000, last=820000), '접촉 전'))
            chk('L2m 다른 케이스 로그 (D3 echo) → 거부 (D0.7 로 읽으면 restart_compress echo 없음)',
                refused(lambda: w2_start_from_log(synth_main_log(D3, 712000, 820000), D07), 'restart_compress'))
            ws = [w2_watch(synth_main_log(D07, *a, **kw), D07)['status'] for a, kw in
                  (((712000, 820000), {}), ((712000, 790000), {}), ((900000, 820000), {}), ((712000, 820000), dict(drop=(750000,))))]
            chk('L3 운영 판단 (같은 규칙) — N 까지 있음 = ready · 첫 접촉 뒤 N 전 = wait · 접촉 전 = no_contact · N 지났는데 빠짐 = refused',
                ws == ['ready', 'wait', 'no_contact', 'refused'], ws)
            rcs = []
            for k, (a, kw) in enumerate((((712000, 820000), {}), ((712000, 790000), {}), ((712000, 820000), dict(drop=(750000,))))):
                p = os.path.join(tmp, f'watch_{k}.liggghts')
                with open(p, 'w', encoding='utf-8') as f:
                    f.write(synth_main_log(D07, *a, **kw))
                with redirect_stdout(io.StringIO()):
                    rcs.append(main(['--w2-start', p]))
            chk('L3b CLI --w2-start rc = ready 0 · 기다림 3 · 거부 2', rcs == [0, 3, 2], rcs)
            for k, kw in (('ok', {}), ('drop', dict(drop=(750000,))), ('d3', {})):
                p = os.path.join(tmp, f'main_log_{k}.liggghts')
                with open(p, 'w', encoding='utf-8') as f:
                    f.write(synth_main_log(D3 if k == 'd3' else D07, 712000, 820000, **kw))
                logs[k] = p
        run('L W2 시작 step 규칙', l_all)

        # ── §12-2 W2 가지 ──
        def w_build():
            for br in ('A', 'B', 'C', 'F'):
                w2[br] = build_branch(D07, br, NP[br], os.path.join(tmp, 'w2'), 'W2', main_log=logs['ok'])
        run('W0 W2 가지 넷 만들기', w_build)

        def w1():
            m = w2['A']
            fol = os.path.join(tmp, 'w2', 'q5w2_kg50_d07_b50_A')
            chk('W1 W2 A 폴더 = 가지 덱 · 러너 · 본 덱 사본 · 본 런 로그 사본 · manifest · SHA256SUMS (여섯)',
                sorted(os.listdir(fol)) == sorted(['input_q5w2_kg50_d07_b50_A.liggghts', 'run_q5w2_kg50_d07_b50_A.sh',
                                                   'main_deck_kg50_d07_b50.liggghts', 'main_log_kg50_d07_b50.liggghts',
                                                   'q5_manifest.json', 'SHA256SUMS']), os.listdir(fol))
            chk('W1b W2 A manifest — 창 W2 · s0 = N 800000 (첫 접촉 712000) · 끝 1100000 · run [300000] · thermo [1000] · atom 31 (10,000) · '
                'contact 4 (100,000) · window_s 0.3 · 체크포인트 …restart_compress_800000.bin · 판 plate_kg50_d07_b50.stl ← '
                'post_kg50_d07_b50/mesh_800000.stl · 로그 사본 sha256',
                (m['window'], m['s0'], m['end_step'], m['runs'], m['thermo_every'], len(m['atom_dump']['steps']),
                 m['contact_dump']['steps'], m['window_s'], m['checkpoint']['rel_path'], m['plate']['rel_path'], m['plate']['source'],
                 m['w2_start']['first_contact_step'], m['w2_start']['main_log']['sha256'])
                == ('W2', 800000, 1100000, [300000], [1000], 31, [800000, 900000, 1000000, 1100000], '0.3',
                    'restart_kg50_d07_b50/restart_compress_800000.bin', 'plate_kg50_d07_b50.stl',
                    '~/dem_test/kg50_d07_b50/post_kg50_d07_b50/mesh_800000.stl', 712000, _sha256_file(logs['ok'])), m)
            chk('W1c §12-2 상태 = 개정 초안 · 비준 전 (지금 등록) — manifest · 덱 머리 줄 같음',
                m['amendment'] == dict(section='§12-2', status=STATUS_DRAFT)
                and '#   §12-2 상태: 개정 초안 · 비준 전' in rd('A', b=w2, sub='w2').split('\n'), m.get('amendment'))
            chk('W1d W2 A 정적 대조 = 등록 §12-4 W2 넷 (rc 1 · 실제 도구 · 10-28 밤 개정 · §12-2 (마) 앞섬)',
                m['static_check']['rc'] == 1 and m['static_check']['problems'] == reg_static('W2', D07, m['s0']), m['static_check'])
            cmds = [x for x, _a, _b in commands(_strip_header(rd('A', b=w2, sub='w2')))]
            rs = 'read_restart restart_kg50_d07_b50/restart_compress_800000.bin'
            ia = cmds.index('print "====== RESTART SAVED ======"')
            chk('W1e W2 A 명령 — read_restart …compress_800000 (processors 뒤 자리) · run = run 300000 하나 · label · jump · '
                'write_restart · 판 높이 · 안정화 run 없음 · restart 0 둘 · fix move_press · dmp_atom 50000 있음 · q5 덤프 둘 = '
                'RESTART SAVED print 뒤 · 끝 = run 300000 · undump 둘',
                cmds.count(rs) == 1 and cmds.index(rs) == 15 and cmds[14] == 'processors * * 1'
                and [x for x in cmds if x.startswith('run ')] == ['run 300000']
                and not any(x.split()[0] in ('label', 'jump', 'write_restart') or x.startswith('if ') for x in cmds)
                and 'variable z_max equal c_zmax' not in cmds and cmds.count('restart 0') == 2
                and 'fix move_press all move/mesh mesh top_mesh linear 0.0 0.0 -${press_speed}' in cmds
                and any(x.startswith('dump dmp_atom all custom 50000 ') for x in cmds)
                and cmds[ia + 1: ia + 3] == _dump_lines(D07, 'W2') and cmds[-3:] == ['run 300000', 'undump dq5a', 'undump dq5c']
                and _dump_lines(D07, 'W2')[0].startswith('dump dq5a all custom 10000 ')
                and _dump_lines(D07, 'W2')[1].startswith('dump dq5c all local 100000 '), cmds[-6:])
            mlines = _read(os.path.join(ROOT, CASES[D07]['deck'])).split('\n')
            body = _strip_header(rd('A', b=w2, sub='w2')).split('\n')
            new = set(_dump_lines(D07, 'W2') + UNDUMP_LINES + [rs, 'restart 0', 'run 300000'])
            kept = [x for x in body if x not in new]
            want = [mlines[k - 1] for k in range(1, MAIN_NLINES + 1)
                    if k not in W2_DROP and k not in (READ_RESTART_LINE, W2_RUN_LINE) + W2_RESTART0_LINES]
            chk('W1f W2 A 의 나머지 줄 = 본 덱 줄 바이트 그대로 (뺀 행 · 바꾼 행 밖 · 순서 그대로)', kept[:-1] == want and kept[-1] == '',
                (len(kept), len(want)))
            r = rd('A', 'runner', b=w2, sub='w2')
            chk('W1g W2 러너 = ibb 본 러너 틀 · 잡 · 폴더 q5w2_kg50_d07_b50_A · -n 56 ↔ -np 56',
                '#SBATCH --job-name=q5w2_kg50_d07_b50_A' in r and 'cd $HOME/dem_test/q5w2_kg50_d07_b50_A' in r
                and '-np 56 lmp_mpi -in input_q5w2_kg50_d07_b50_A.liggghts' in r and runner_check(D07, 'A', 56, r, 'W2') == [], r)
        run('W1 W2 A', w1)

        def w2b():
            ca = [x for x, _a, _b in commands(_strip_header(rd('A', b=w2, sub='w2')))]
            cb = [x for x, _a, _b in commands(_strip_header(rd('B', b=w2, sub='w2')))]
            dif = [(x, y) for x, y in zip(ca, cb) if x != y]
            chk('W2 W2 B ↔ A = 명령 다섯만 다름 (§12-2: 43 dt · 203 mesh 10000 · 212 thermo 2000 · 217 dmp_atom 100000 · run 600000)',
                len(ca) == len(cb) and [x for x, _y in dif] == ['variable dt equal 1.0e-6',
                                                                'dump dmp_mesh all mesh/stl 5000 post_kg50_d07_b50/mesh_*.stl top_mesh',
                                                                'thermo 1000', ca[[i for i, x in enumerate(ca)
                                                                                   if x.startswith('dump dmp_atom ')][0]], 'run 300000']
                and [y for _x, y in dif][0] == 'variable dt equal 5.0e-7' and [y for _x, y in dif][-1] == 'run 600000'
                and [y for _x, y in dif][3].startswith('dump dmp_atom all custom 100000 '), dif)
            m = w2['B']
            ta = [round((s - 800000) * 1e-06, 9) for s in range(1100000 - 50000, 1100001, 1000)]
            tb = [round((s - 800000) * 5e-07, 9) for s in range(1400000 - 100000, 1400001, 2000)]
            chk('W2b W2 B manifest — dt 5e-07 · run [600000] · 끝 1400000 · thermo [2000] · atom 61 · contact 7 (A 덤프 시각 다 포함) · '
                'O3 마지막 0.05 s 표본 51 = A 와 같은 시각',
                (m['dt'], m['runs'], m['end_step'], m['thermo_every'], len(m['atom_dump']['steps']), len(m['contact_dump']['steps']))
                == (5e-07, [600000], 1400000, [2000], 61, 7)
                and all(800000 + 2 * (s - 800000) in m['contact_dump']['steps'] for s in w2['A']['contact_dump']['steps'])
                and ta == tb and len(ta) == 51, m)
            chk('W2c W2 B 정적 대조 안 함 (허용 목록만 · §12-2 (마))', m['static_check'] is None)
        run('W2 W2 B', w2b)

        def w3():
            ca = [x for x, _a, _b in commands(_strip_header(rd('A', b=w2, sub='w2')))]
            cc = [x for x, _a, _b in commands(_strip_header(rd('C', b=w2, sub='w2')))]
            dif = [(x, y) for x, y in zip(ca, cc) if x != y]
            chk('W3 W2 C ↔ A = 명령 하나 (208 scale 3 5.3696e-4)', len(ca) == len(cc)
                and dif == [('fix damp all viscous 0.5', 'fix damp all viscous 0.5 scale 3 5.3696e-4')], dif)
            chk('W3b W2 F 덱 = A 덱 바이트 · F 러너 -n 28 · F 정적 대조 = 둘', rd('F', b=w2, sub='w2') == rd('A', b=w2, sub='w2')
                and '#SBATCH -n 28' in rd('F', 'runner', b=w2, sub='w2')
                and w2['F']['static_check']['problems'] == reg_static('W2', D07, w2['F']['s0']))
        run('W3 W2 C · F', w3)

        def w4():
            oa = w2['A']['operator_commands']
            chk('W4 W2 운영자 명령 (초안) — 체크포인트 …restart_compress_800000.bin cp · ckpt_sha256.txt · mesh_800000.stl → '
                'plate_kg50_d07_b50.stl · plate_sha256.txt · ⛔ 개정 초안 줄 · sbatch 없음',
                any('cp ~/dem_test/kg50_d07_b50/restart_kg50_d07_b50/restart_compress_800000.bin ~/dem_test/q5w2_kg50_d07_b50_A/'
                    'restart_kg50_d07_b50/' in x for x in oa)
                and 'cp ~/dem_test/kg50_d07_b50/post_kg50_d07_b50/mesh_800000.stl ~/dem_test/q5w2_kg50_d07_b50_A/plate_kg50_d07_b50.stl' in oa
                and any('plate_sha256.txt' in x for x in oa) and any('개정 초안 · 비준 전' in x for x in oa)
                and not any('sbatch' in x for x in oa), oa)
            reg = os.path.join(tmp, 'reg_ratified.md')
            with open(reg, 'w', encoding='utf-8') as f:
                f.write(reg_txt.replace(W2_STATUS_DRAFT, '> **§12-2 상태: ✅ 1저자 비준 (10-29)**', 1))
            m = build_branch(D07, 'A', 56, os.path.join(tmp, 'w2r'), 'W2', main_log=logs['ok'], registration=reg)
            o = m['operator_commands']
            d = _read(os.path.join(tmp, 'w2r', m['folder'], m['deck']['file']))
            chk('W4b 비준 판 등록 (✅ 줄) → manifest · 덱 머리 = 비준 · 운영자 sbatch 줄 · 체크포인트 · 판 STL gate 둘 · 덱 명령은 초안 판과 같음',
                m['amendment']['status'] == STATUS_RATIFIED and '#   §12-2 상태: 비준' in d.split('\n')
                and any('sbatch q5w2_kg50_d07_b50_A/run_q5w2_kg50_d07_b50_A.sh' in x and x.count('sort -u | wc -l') == 2 for x in o)
                and [x for x, _a, _b in commands(_strip_header(d))] == [x for x, _a, _b in commands(_strip_header(rd('A', b=w2, sub='w2')))]
                and verify_folder(os.path.join(tmp, 'w2r', m['folder'])) == [], o)
        run('W4 운영자 · 비준 판', w4)

        def w5():
            chk('W5 --verify W2 폴더 넷 = 문제 0', all(verify_folder(os.path.join(tmp, 'w2', m['folder'])) == [] for m in w2.values()),
                verify_folder(os.path.join(tmp, 'w2', w2['C']['folder'])))
            src = os.path.join(tmp, 'w2', w2['A']['folder'])

            def cp(tag):
                d = os.path.join(tmp, 'w2v', tag, w2['A']['folder'])
                shutil.copytree(src, d)
                return d
            d1 = cp('log')
            with open(os.path.join(d1, 'main_log_kg50_d07_b50.liggghts'), 'a', encoding='utf-8') as f:
                f.write('# 한 줄 더\n')
            d2 = cp('n')
            lp = os.path.join(d2, 'main_log_kg50_d07_b50.liggghts')
            with open(lp, 'w', encoding='utf-8') as f:
                f.write(synth_main_log(D07, 512000, 820000))
            mp = os.path.join(d2, 'q5_manifest.json')
            mm = json.loads(_read(mp))
            mm['w2_start']['main_log']['sha256'] = _sha256_file(lp)
            with open(mp, 'w', encoding='utf-8') as f:
                json.dump(mm, f)
            d3 = cp('every')
            mp3 = os.path.join(d3, 'q5_manifest.json')
            m3 = json.loads(_read(mp3))
            m3['contact_dump']['every'] = 50000
            m3['contact_dump']['steps'] = expected_steps(800000, 1100000, 50000)
            with open(mp3, 'w', encoding='utf-8') as f:
                json.dump(m3, f)
            chk('W5b 로그 사본 한 줄 더 (sha256 다름) → 문제', any('로그 사본 sha256' in x for x in verify_folder(d1)), verify_folder(d1))
            chk('W5c 로그 사본 = 첫 접촉 512,000 꼴 (sha256 맞춤) → 다시 센 N 600,000 ≠ manifest 800,000 → 문제',
                any('시작 step 다시 계산 600000' in x for x in verify_folder(d2)), verify_folder(d2))
            chk('W5d manifest contact 간격 50,000 (step 맞춤 · 판독기 내부 일관성은 통과하는 꼴) → 문제',
                any('contact_dump' in x for x in verify_folder(d3)), verify_folder(d3))
        run('W5 W2 다시 대조', w5)

        def w6():
            mt = _read(os.path.join(ROOT, CASES[D07]['deck']))
            a, b = rd('A', b=w2, sub='w2'), rd('B', b=w2, sub='w2')
            bad = [
                ('W6 루프 남김 (run 300000 → label · run 5000)', a.replace('\nrun 300000\n', '\nlabel loop_press\n    run 5000\n'), 'A'),
                ('W6b run 300001', a.replace('\nrun 300000\n', '\nrun 300001\n'), 'A'),
                ('W6c 222 행 restart 200000 남김', a.replace('restart 0\n\nrun 300000',
                                                            'restart 200000 restart_kg50_d07_b50/restart_compress_*.bin\n\nrun 300000'), 'A'),
                ('W6d undump 하나 빠짐', a.replace('undump dq5c\n', ''), 'A'),
                ('W6e 판 높이 run 1 남김', a.replace('print "====== RESTART SAVED ======"\n',
                                                   'print "====== RESTART SAVED ======"\nthermo_style    custom step atoms c_zmax\nrun 1\n'), 'A'),
                ('W6f B 에 thermo 1000 (212 행 바꿈 빠짐)', b.replace('thermo 2000', 'thermo 1000'), 'B'),
                ('W6g read_restart …compress_600000 (N 다름)', a.replace('restart_compress_800000.bin', 'restart_compress_600000.bin'), 'A'),
                ('W6h contact 덤프 50000', a.replace('local 100000 ', 'local 50000 '), 'A'),
                ('W6i W1 덱을 W2 로 대조', rd('A'), 'A'),
            ]
            for label, txt, br in bad:
                p = verify_branch_deck(mt, txt, D07, br, 'W2', 800000)
                chk(f'{label} → 문제', bool(p), p)
            chk('W6j 정상 W2 A · B · C = 문제 0', all(verify_branch_deck(mt, rd(x, b=w2, sub='w2'), D07, x, 'W2', 800000) == []
                                                   for x in ('A', 'B', 'C')))
        run('W6 W2 허용 목록', w6)

        # ── §12-3 로컬 직렬 (A3 · C3) ──
        def h_build():
            for br in ('A3', 'C3'):
                loc[br] = build_branch(D3, br, 1, os.path.join(tmp, 'wsl'), host='wsl')
        run('H0 로컬 A3 · C3 만들기', h_build)

        def h1():
            m = loc['A3']
            chk('H1 로컬 A3 manifest — 폴더 q5_kg50_d3_b50_s1_A3_wsl · host wsl · serial · NP 1 · 바이너리 (환경 변수 LMP_SERIAL · 기본 '
                '$HOME/src/LIGGGHTS-PUBLIC/src/lmp_serial · PATH lmp_serial · 기록 q5_binary.txt) · 이탈 §12-3 · 체크포인트 원본 '
                '~/q5_local/kg50_d3_b50_s1/… · Q1 sha256',
                (m['folder'], m['host'], m['launcher'], m['np'], m['binary']['env'], m['binary']['default'], m['binary']['fallback'],
                 m['binary']['record'], m['deviation']['section'], m['checkpoint']['source'], m['checkpoint']['registered_sha256'])
                == ('q5_kg50_d3_b50_s1_A3_wsl', 'wsl', 'serial', 1, 'LMP_SERIAL', '$HOME/src/LIGGGHTS-PUBLIC/src/lmp_serial',
                    'lmp_serial', 'q5_binary.txt', '§12-3', '~/q5_local/kg50_d3_b50_s1/restart_kg50_d3_b50_s1/restart_after_settling.bin',
                    D3_CKPT_SHA256), m)
            chk('H1b 로컬 A3 · C3 덱 = hit A3 · C3 덱 바이트 같음 (러너만 다름)',
                rd('A3', b=loc, sub='wsl') == rd('A3') and rd('C3', b=loc, sub='wsl') == rd('C3'))
            r = rd('A3', 'runner', b=loc, sub='wsl')
            chk('H1c 로컬 러너 — mpirun · lmp_auto · sbatch 없음 · cd "$HOME/q5_local/q5_kg50_d3_b50_s1_A3_wsl" · LMP_SERIAL → 기본 경로 → '
                'PATH lmp_serial · ldd libmpi 거부 · Q1 sha256 · setsid nohup "$B" -in input_…A3_wsl.liggghts > log_…A3_wsl_v1.out',
                not any(w in r for w in ('mpirun', 'lmp_auto', 'sbatch', 'srun'))
                and 'cd "$HOME/q5_local/q5_kg50_d3_b50_s1_A3_wsl"' in r and '${LMP_SERIAL:-}' in r
                and '[ -x "$HOME/src/LIGGGHTS-PUBLIC/src/lmp_serial" ]' in r and 'else L=lmp_serial; fi' in r
                and 'grep -q libmpi' in r and f'Q1={D3_CKPT_SHA256}' in r
                and 'setsid nohup "$B" -in input_q5_kg50_d3_b50_s1_A3_wsl.liggghts > log_q5_kg50_d3_b50_s1_A3_wsl_v1.out 2>&1 < /dev/null &' in r
                and runner_check(D3, 'A3', 1, r, 'W1', 'wsl') == [], r)
            chk('H1d 로컬 A3 정적 대조 = 등록 §12-4 W1 셋 (덱이 hit A3 와 같다)', m['static_check']['problems'] == reg_static('W1', D3))
            o = m['operator_commands']
            stage = '~/q5_local/kg50_d3_b50_s1/restart_kg50_d3_b50_s1/restart_after_settling.bin'
            chk('H1e 운영자 명령 (로컬) — hit 원본 scp (읽기만) → 같은 사본 · 등록 Q1 sha256 -c · SHA256SUMS -c · cp · ckpt_sha256.txt · '
                'gate → bash ~/q5_local/<폴더>/run_<폴더>.sh',
                any('scp <사용자>@<hit>:~/simulation/kg50_d3_b50_s1/restart_kg50_d3_b50_s1/restart_after_settling.bin' in x for x in o)
                and any(x.startswith(f'echo "{D3_CKPT_SHA256}  $HOME/q5_local/kg50_d3_b50_s1/') and '| sha256sum -c' in x for x in o)
                and f'mkdir -p ~/q5_local/q5_kg50_d3_b50_s1_A3_wsl/restart_kg50_d3_b50_s1 && cp {stage} '
                    '~/q5_local/q5_kg50_d3_b50_s1_A3_wsl/restart_kg50_d3_b50_s1/' in o
                and any('bash ~/q5_local/q5_kg50_d3_b50_s1_A3_wsl/run_q5_kg50_d3_b50_s1_A3_wsl.sh' in x and 'sort -u | wc -l' in x for x in o)
                and not any('mpirun' in x or 'sbatch' in x or ' rm ' in x for x in o), o)
            chk('H1f --verify 로컬 폴더 둘 = 문제 0 · 러너 한 글자 바꾸면 문제',
                all(verify_folder(os.path.join(tmp, 'wsl', x['folder'])) == [] for x in loc.values())
                and bool(runner_check(D3, 'A3', 1, r.replace('exit 2', 'exit 3', 1), 'W1', 'wsl')))
        run('H1 로컬', h1)

        def h2():
            out = os.path.join(tmp, 'wslref')
            os.makedirs(out)
            chk('H2 F3 로컬 → 거부 ("F3 = hit NP 2 · D1 끝난 뒤")', refused(lambda: build_branch(D3, 'F3', 2, out, host='wsl'),
                                                                     'F3 = hit NP 2 · D1 끝난 뒤'))
            chk('H2b D0.7 가지 A · B · C · F 로컬 → 거부 (§12-3 = D3 A3 · C3 만)',
                all(refused(lambda x=x: build_branch(D07, x, NP[x], out, host='wsl'), '로컬 직렬') for x in ('A', 'B', 'C', 'F')))
            chk('H2c 로컬 A3 NP 2 → 거부 (Q5 = 1)', refused(lambda: build_branch(D3, 'A3', 2, out, host='wsl'), 'Q5'))
            chk('H2d 모르는 host (hit2) → 거부', refused(lambda: build_branch(D3, 'A3', 1, out, host='hit2'), 'host'))
            chk('H2e 로컬 + W2 → 거부', refused(lambda: build_branch(D3, 'A3', 1, out, 'W2', host='wsl', main_log=logs['d3']), 'W1 만'))
            chk('H2f 거부 뒤 파일 0', os.listdir(out) == [], os.listdir(out))
        run('H2 로컬 거부', h2)

        def hr():
            home = os.path.join(tmp, 'home')
            root = os.path.join(home, 'q5_local')
            q1 = hashlib.sha256(b'q5-local-ckpt').hexdigest()
            m = build_branch(D3, 'A3', 1, root, host='wsl', q1=q1)          # selftest 이음새 — Q1 값만 시험 값
            fol = os.path.join(root, m['folder'])
            os.makedirs(os.path.join(fol, 'restart_kg50_d3_b50_s1'))
            with open(os.path.join(fol, 'restart_kg50_d3_b50_s1', 'restart_after_settling.bin'), 'wb') as f:
                f.write(b'q5-local-ckpt')
            with open(os.path.join(fol, 'ckpt_sha256.txt'), 'w') as f:
                f.write(f'{q1}  {home}/q5_local/kg50_d3_b50_s1/restart_kg50_d3_b50_s1/restart_after_settling.bin\n'
                        f'{q1}  {fol}/restart_kg50_d3_b50_s1/restart_after_settling.bin\n')
            src_dir = os.path.join(home, 'src', 'LIGGGHTS-PUBLIC', 'src')
            os.makedirs(src_dir)
            fake = ('#!/bin/bash\nprintf "%s\\n" "$PWD" "$@" > "$HOME/fake_called.txt"\n'
                    'echo "LIGGGHTS (fake serial)" > log.liggghts\n')
            for p in (os.path.join(src_dir, 'lmp_serial'), os.path.join(home, 'pathbin', 'lmp_serial'),
                      os.path.join(home, 'mpibin', 'ldd')):
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(p, 'w') as f:
                    f.write(fake if not p.endswith('ldd') else '#!/bin/bash\necho "\tlibmpi.so.40 => /usr/lib/libmpi.so.40"\n')
                os.chmod(p, 0o755)
            pristine = os.path.join(tmp, 'pristine')
            shutil.copytree(fol, pristine)

            def go(env_extra=None, path_pre=None, mut=None):
                if os.path.isdir(fol):
                    shutil.rmtree(fol)
                shutil.copytree(pristine, fol)
                for x in ('fake_called.txt',):
                    if os.path.exists(os.path.join(home, x)):
                        os.remove(os.path.join(home, x))
                if mut:
                    mut()
                env = {'HOME': home, 'PATH': (path_pre + ':' if path_pre else '') + os.environ.get('PATH', '/usr/bin:/bin'),
                       'LANG': 'C.UTF-8'}
                env.update(env_extra or {})
                r = subprocess.run(['bash', os.path.join(fol, m['runner']['file'])], env=env, capture_output=True, text=True, timeout=60)
                called = None
                for _ in range(200):
                    p = os.path.join(home, 'fake_called.txt')
                    if os.path.exists(p) and os.path.exists(os.path.join(fol, 'log.liggghts')):
                        time.sleep(0.05)
                        called = _read(p).split('\n')
                        break
                    if r.returncode != 0:
                        break
                    time.sleep(0.05)
                return r, called

            r, called = go()
            chk('HR1 로컬 러너 실행 (가짜 직렬 바이너리 · LMP_SERIAL 없음 → $HOME/src/LIGGGHTS-PUBLIC/src/lmp_serial) — rc 0 · 가지 폴더에서 '
                '-in input_<폴더>.liggghts 만 · mpirun 없음',
                r.returncode == 0 and called is not None and called[:3] == [fol, '-in', f'input_{m["folder"]}.liggghts']
                and called[3:] == [''], (r.returncode, r.stdout[-300:], r.stderr[-300:], called))
            rec = _read(os.path.join(fol, BINARY_RECORD)).split('\n') if os.path.exists(os.path.join(fol, BINARY_RECORD)) else []
            chk('HR1b q5_binary.txt = mode serial · np 1 · binary <기본 경로> · sha256 = 가짜 바이너리 sha256 · libmpi none · host',
                rec[:5] == ['mode serial', 'np 1', f'binary {src_dir}/lmp_serial',
                            f'sha256 {_sha256_file(os.path.join(src_dir, "lmp_serial"))}', 'libmpi none']
                and rec[5].startswith('host ') and len(rec[5]) > 5, rec)
            r2 = subprocess.run(['bash', os.path.join(fol, m['runner']['file'])], env={'HOME': home, 'PATH': os.environ.get('PATH', '')},
                                capture_output=True, text=True, timeout=60)
            chk('HR2 log.liggghts 이미 있음 (다시 실행) → rc 2 · 덮어쓰지 않음', r2.returncode == 2 and 'log.liggghts' in r2.stdout, r2.stdout)

            def bad_rec():
                with open(os.path.join(fol, 'ckpt_sha256.txt'), 'w') as f:
                    f.write(f'{"0" * 64}  /a/kg50_d3_b50_s1/restart_kg50_d3_b50_s1/restart_after_settling.bin\n'
                            f'{"0" * 64}  {fol}/restart_kg50_d3_b50_s1/restart_after_settling.bin\n')

            def bad_ckpt():
                with open(os.path.join(fol, 'restart_kg50_d3_b50_s1', 'restart_after_settling.bin'), 'wb') as f:
                    f.write(b'other')

            def bad_sums():
                p = os.path.join(fol, m['deck']['file'])
                with open(p, 'a') as f:
                    f.write('# 한 줄\n')
            cases = [('HR3 ckpt_sha256.txt 값 ≠ 등록 Q1', dict(mut=bad_rec), '등록 Q1 sha256 이 아니다'),
                     ('HR4 체크포인트 내용 sha256 ≠ 등록 Q1 (기록은 Q1 그대로)', dict(mut=bad_ckpt), 'sha256 ≠ 등록 Q1'),
                     ('HR5 LMP_SERIAL = 없는 경로', dict(env_extra={'LMP_SERIAL': os.path.join(home, 'nope', 'lmp_serial')}),
                      '직렬 바이너리 없음'),
                     ('HR6 ldd 가 libmpi 를 보임 (MPI 빌드)', dict(path_pre=os.path.join(home, 'mpibin')), 'MPI 빌드'),
                     ('HR7 SHA256SUMS 다름 (가지 덱 한 줄 더)', dict(mut=bad_sums), 'SHA256SUMS 다름')]
            for label, kw, needle in cases:
                rr, cc = go(**kw)
                chk(f'{label} → rc 2 · 그 거부 글 · 바이너리 안 부름 · q5_binary.txt 없음',
                    rr.returncode == 2 and needle in rr.stdout and cc is None and not os.path.exists(os.path.join(fol, BINARY_RECORD)),
                    (rr.returncode, rr.stdout[-200:]))

            def no_default():
                os.rename(os.path.join(src_dir, 'lmp_serial'), os.path.join(src_dir, 'lmp_serial.off'))
            rr, cc = go(path_pre=os.path.join(home, 'pathbin'), mut=no_default)
            os.rename(os.path.join(src_dir, 'lmp_serial.off'), os.path.join(src_dir, 'lmp_serial'))
            rec2 = _read(os.path.join(fol, BINARY_RECORD)).split('\n') if os.path.exists(os.path.join(fol, BINARY_RECORD)) else []
            rr3, cc3 = go(env_extra={'LMP_SERIAL': os.path.join(home, 'pathbin', 'lmp_serial')})
            rec3 = _read(os.path.join(fol, BINARY_RECORD)).split('\n') if os.path.exists(os.path.join(fol, BINARY_RECORD)) else []
            chk('HR8 기본 경로 없음 → PATH 의 lmp_serial · LMP_SERIAL 있으면 그것 (기록 binary 줄)',
                rr.returncode == 0 and cc is not None and f'binary {home}/pathbin/lmp_serial' in rec2
                and rr3.returncode == 0 and cc3 is not None and f'binary {home}/pathbin/lmp_serial' in rec3, (rec2, rec3))
        run('HR 로컬 러너 실행', hr)

        # ── 거부 (rc 2 · 파일 0) ──
        def r_all():
            out = os.path.join(tmp, 'ref')
            os.makedirs(out)
            cases = [
                ('R1 A NP 28 (Q5 = 56)', lambda: build_branch(D07, 'A', 28, out), 'Q5'),
                ('R1b F NP 56 (Q5 = 28 — F 가 A 와 같은 분할이면 바닥이 0)', lambda: build_branch(D07, 'F', 56, out), 'Q5'),
                ('R1c A3 NP 2 (Q5 = 1)', lambda: build_branch(D3, 'A3', 2, out), 'Q5'),
                ('R2 B3 (등록 가지 아님 · (a) 는 D0.7 만)', lambda: build_branch(D3, 'B3', 1, out), '등록 가지'),
                ('R2b D0.7 에 A3', lambda: build_branch(D07, 'A3', 1, out), '등록 가지'),
                ('R2c 소문자 a', lambda: build_branch(D07, 'a', 56, out), '등록 가지'),
                ('R3 등록 밖 침대 kg50_d1_b50', lambda: build_branch('kg50_d1_b50', 'A', 56, out), '등록 침대'),
                ('R4 모르는 창 W3', lambda: build_branch(D07, 'A', 56, out, 'W3'), '창'),
                ('R4b W2 인데 --main-log 없음', lambda: build_branch(D07, 'A', 56, out, 'W2'), '--main-log'),
                ('R4c W2 를 D3 에 (§5 W2 표 = D0.7 만 · 질문 W2-6)', lambda: build_branch(D3, 'A3', 1, out, 'W2', main_log=logs['d3']),
                 'D0.7-50 만'),
                ('R4d W2 본 런 로그 = 1,000 배수 줄 빠짐', lambda: build_branch(D07, 'A', 56, out, 'W2', main_log=logs['drop']), '빠짐'),
            ]
            for label, fn, needle in cases:
                chk(f'{label} → 거부', refused(fn, needle))
            chk('R* 거부 뒤 파일 0 (상위 폴더 비었음)', os.listdir(out) == [], os.listdir(out))
            mut = os.path.join(tmp, 'mut.liggghts')
            mt = _read(os.path.join(ROOT, CASES[D07]['deck']))
            with open(mut, 'w', encoding='utf-8', newline='\n') as f:
                f.write(mt.replace('youngsModulus peratomtype 1.4e8 1.4e8 0.135e7', 'youngsModulus peratomtype 1.4e8 1.4e8 0.136e7'))
            chk('R5 본 덱 sha256 다름 (재료 줄 한 글자) → 거부', refused(lambda: build_branch(D07, 'B', 56, out, main_deck=mut), 'sha256'))
            pre = os.path.join(out, 'q5_kg50_d07_b50_B')
            os.makedirs(pre)
            chk('R6 가지 폴더가 이미 있음 (빈 폴더라도) → 거부 · 그대로', refused(lambda: build_branch(D07, 'B', 56, out), '이미')
                and os.listdir(pre) == [])
            os.rmdir(pre)
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = main(['--case', D07, '--branch', 'A', '--np', '28', '--out', out])
            chk('R7 CLI 거부 = rc 2 · 파일 0', rc == 2 and os.listdir(out) == [], buf.getvalue()[-200:])
            with redirect_stdout(io.StringIO()):
                rc = main(['--case', D07, '--branch', 'B', '--np', '56', '--out', out])
            chk('R7b CLI 정상 = rc 0 · 폴더 하나', rc == 0 and os.listdir(out) == ['q5_kg50_d07_b50_B'])
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = main(['--case', D07, '--branch', 'C', '--np', '56', '--window', 'W2', '--main-log', logs['ok'], '--out', out])
            chk('R7c CLI W2 (초안) = rc 0 · 화면에 시작 step · ⚠ 개정 초안 · 비준 전 · 실행 금지',
                rc == 0 and 'W2 시작 step N = 800000' in buf.getvalue() and '실행 금지' in buf.getvalue(), buf.getvalue()[-400:])
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = main(['--case', D3, '--branch', 'F3', '--np', '2', '--host', 'wsl', '--out', out])
            chk('R7d CLI 로컬 F3 = rc 2 · 거부 글 (F3 = hit NP 2 · D1 끝난 뒤)', rc == 2 and 'F3 = hit NP 2 · D1 끝난 뒤' in buf.getvalue(),
                buf.getvalue()[-300:])
        run('R 거부', r_all)

        # ── 허용 목록 대조 (가지 덱을 손댄 꼴 → 문제) ──
        def v_all():
            mt = _read(os.path.join(ROOT, CASES[D07]['deck']))
            a, b, c = rd('A'), rd('B'), rd('C')
            chk('V0 정상 A · B · C · A3 · C3 = 문제 0', verify_branch_deck(mt, a, D07, 'A') == [] and verify_branch_deck(mt, b, D07, 'B') == []
                and verify_branch_deck(mt, c, D07, 'C') == [])
            bad = [
                ('V1 물리 줄 한 글자 (안정화 중력 9.81 → 9.80)', a.replace('gravity 9.81 vector', 'gravity 9.80 vector'), 'A'),
                ('V2 명령 하나 더 (fix 줄)', a.replace('fix integr all nve/sphere\n', 'fix integr all nve/sphere\nfix extra all enforce2d\n'), 'A'),
                ('V3 명령 하나 빠짐 (unfix damp)', a.replace('unfix damp\n', ''), 'A'),
                ('V4 q5 atom 덤프 간격 66667 → 66666', a.replace('custom 66667', 'custom 66666'), 'A'),
                ('V5 두 명령 순서 바뀜', a.replace('fix gravi all gravity 9.81 vector 0.0 0.0 -1.0\nunfix damp',
                                                   'unfix damp\nfix gravi all gravity 9.81 vector 0.0 0.0 -1.0'), 'A'),
                ('V6 restart 0 → restart 50000 …', a.replace('\nrestart 0\n', '\nrestart 50000 restart_kg50_d07_b50/restart_settling_*.bin\n'), 'A'),
                ('V7 B 에 일곱째 바꿈 (155 행 thermo 1000 → 2000)', b.replace('thermo          1000', 'thermo          2000', 1), 'B'),
                ('V8 C 의 s 한 자리 (5.3696e-4 → 5.3697e-4)', c.replace('scale 3 5.3696e-4', 'scale 3 5.3697e-4'), 'C'),
                ('V9 C 의 scale 을 주석으로 숨김 (# scale 3 …)', c.replace(' scale 3 5.3696e-4', ' # scale 3 5.3696e-4'), 'C'),
                ('V10 A 덱을 B 로 대조 (바꿈 없음)', a, 'B'),
                ('V11 머리 표지 없음', a.replace(HEADER_END + '\n', ''), 'A'),
                ('V12 본 덱 주석 줄 하나 바뀜 (줄 단위)', a.replace('# --- 8. Output ---', '# --- 8. 출력 ---'), 'A'),
                ('V13 read_restart 두 번', a.replace('read_restart restart_kg50_d07_b50/restart_after_settling.bin\n',
                                                     'read_restart restart_kg50_d07_b50/restart_after_settling.bin\n'
                                                     'read_restart restart_kg50_d07_b50/restart_after_settling.bin\n'), 'A'),
                ('V14 머리 주석 줄이 & 로 끝남 (다음 줄을 삼킨다)', a.replace(' NP = 러너 (Q5)', ' NP = 러너 (Q5) &', 1), 'A'),
                ('V15 머리 안에 명령 줄', a.replace(HEADER_END, 'fix extra all enforce2d\n' + HEADER_END, 1), 'A'),
            ]
            for label, txt, br in bad:
                p = verify_branch_deck(mt, txt, D07, br)
                chk(f'{label} → 문제', bool(p), p)
        run('V 허용 목록', v_all)

        # ── 변이: 관문 하나를 끄면 그것을 겨눈 시험이 실패해야 한다 ──
        def m_all():
            mt = _read(os.path.join(ROOT, CASES[D07]['deck']))
            mdir = os.path.join(tmp, 'mutation')
            os.makedirs(mdir)
            k = [0]

            def fresh():
                k[0] += 1
                return os.path.join(mdir, 'o%d' % k[0])

            def mutated(old, new):
                p = os.path.join(mdir, 'deck%d.liggghts' % (k[0] + 1000))
                k[0] += 1
                t = mt.replace(old, new, 1)
                with open(p, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(t)
                return p, _sha256_bytes(t.encode('utf-8'))

            reg = os.path.join(mdir, 'reg.md')
            with open(reg, 'w', encoding='utf-8') as f:
                f.write(reg_txt.replace('| 213 | `run 200000` | `run 400000` |', '| 213 | `run 200000` | `run 400001` |'))
            reg_both = os.path.join(mdir, 'reg_both.md')
            with open(reg_both, 'w', encoding='utf-8') as f:
                f.write(reg_txt.replace(W2_STATUS_DRAFT, W2_STATUS_DRAFT + '\n> **§12-2 상태: ✅ 1저자 비준 (10-29)**', 1))
            fake = os.path.join(mdir, 'fake_resume.sh')
            with open(fake, 'w', encoding='utf-8') as f:
                f.write('echo "  ✗ %s"\necho "  ✗ 다른 문제"\nexit 1\n' % EXPECTED_STATIC_W1[2])
            tmpl = os.path.join(mdir, 'runner_tmpl.sh')
            with open(tmpl, 'w', encoding='utf-8') as f:
                f.write(_read(os.path.join(ROOT, RUNNER_TEMPLATE)).replace('#SBATCH --qos=cpu-60', '#SBATCH --qos=cpu-30'))
            p_pin, _ = mutated('youngsModulus peratomtype 1.4e8 1.4e8 0.135e7', 'youngsModulus peratomtype 1.4e8 1.4e8 0.136e7')
            p_anc, s_anc = mutated('fix damp all viscous 0.5\n', 'fix damp all viscous 0.6\n')
            p_s, s_s = mutated('variable r_SE    equal 0.35e-3', 'variable r_SE    equal 0.36e-3')
            pre = fresh()
            os.makedirs(os.path.join(pre, 'q5_kg50_d07_b50_B'))
            targeted = {
                'registration': lambda: build_branch(D07, 'B', 56, fresh(), registration=reg),
                'case': lambda: build_branch('kg50_d1_b50', 'A', 56, fresh()),
                'branch': lambda: build_branch(D07, 'A3', 1, fresh()),
                'np': lambda: build_branch(D07, 'B', 28, fresh()),
                'window': lambda: build_branch(D07, 'B', 56, fresh(), 'W3'),
                'pin': lambda: build_branch(D07, 'B', 56, fresh(), main_deck=p_pin),
                'anchors': lambda: build_branch(D07, 'B', 56, fresh(), main_deck=p_anc, pinned=s_anc),
                's_check': lambda: build_branch(D07, 'C', 56, fresh(), main_deck=p_s, pinned=s_s),
                'allowlist': lambda: build_branch(D07, 'B', 56, fresh(),
                                                  tamper=lambda t: t.replace('gravity 9.81 vector', 'gravity 9.80 vector')),
                'static': lambda: build_branch(D07, 'A', 56, fresh(), resume_tool=fake),
                'runner': lambda: build_branch(D07, 'B', 56, fresh(), runner_template=tmpl),
                'out_exists': lambda: build_branch(D07, 'B', 56, pre),
                'host': lambda: build_branch(D3, 'F3', 2, fresh(), host='wsl'),
                'w2_case': lambda: build_branch(D3, 'A3', 1, fresh(), 'W2', main_log=logs['d3']),
                'w2_log': lambda: build_branch(D07, 'B', 56, fresh(), 'W2', main_log=logs['drop']),
                'w2_status': lambda: build_branch(D07, 'B', 56, fresh(), 'W2', main_log=logs['ok'], registration=reg_both),
            }
            for g in GUARDS:
                fn = targeted.get(g)
                if fn is None:
                    chk(f'M {g}: 겨눈 시험 있음', False)
                    continue
                on = refused(fn)
                GUARDS[g] = False
                try:
                    off = refused(fn)
                finally:
                    GUARDS[g] = True
                chk(f'M {g}: 켜면 거부 · 끄면 통과 (그 관문이 실제로 막는다)', on and not off, (on, off))
        run('M 변이', m_all)
    finally:
        for g in GUARDS:
            GUARDS[g] = True
        shutil.rmtree(tmp, ignore_errors=True)
    n, N = tally
    print(f'kg50_q5_branches selftest: {"PASS" if n == N else "FAIL"} ({n}/{N})')
    return 0 if n == N else 1


if __name__ == '__main__':
    sys.exit(main())
