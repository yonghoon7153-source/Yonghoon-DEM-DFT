#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""50kg Q5 가지 덱 생성기 — 정착 끝 (after_settling) 체크포인트에서 dt ↔ dt/2 · 감쇠 가지 (등록 Q11 · 창 W1).

등록 = `docs/50kg/kg50_q5_dt_damping_registration_draft_20261027.md` (1저자 10-27 밤 비준 · Q1–Q12 = 머리 비준 표).
  §2 침대 · 지점 — kg50_d07_b50 (v3 덱 · ibb) · kg50_d3_b50_s1 (v2 덱 · hit) · 체크포인트 restart_<case>/restart_after_settling.bin
       (step 200001 · 본 덱 170 행 write_restart)
  §3 가지 — A 본 덱 그대로 · B dt 1 µs → 0.5 µs (step 으로 센 수 ×2) · C 안정화 감쇠의 SE 몫만 γ_SE = 0.5·s
       (Q2 (가) AM 기준 s = m_SE/m_AM) · F = A 덱 그대로 · NP 만 다름 · D3 = A3 · C3 · F3 (같은 꼴 · B3 없음)
  Q5 NP — A · B · C 56 · F 28 · A3 · C3 1 · F3 2
  §4 덱 줄 — 뼈대 §4-1 · B §4-2 · C §4-3 · 출력 줄 §4-5 (덤프 간격 Q12 = W1 atom 66,667 · contact 200,001)
  창 (Q3 (나) W1 + W2) — 이 생성기는 W1 만 만든다.  W2 는 거부한다: §5 가 W2 덱의 꼴 (압축 체크포인트 재개 + 고정 run) 만
       적고 줄 목록이 없다 (§4 = W1 줄만) · Q12 에 W2 contact 덤프 간격이 없다 · W2 시작 체크포인트 step 은 본 런 뒤에 정해진다.

하는 일 (본 덱 · 체크포인트 · 원 폴더는 읽기만 · 바꾸지 않는다):
  ⓪ 등록 문서의 고정 줄 (§2 · §4 표 · 머리 비준 표 · §8) = 이 파일의 상수 — 다르면 거부 (결과 뒤 등록 이동 차단)
  ① 본 덱 sha256 = 그 덱 묶음 manifest.json 의 deck_sha256 (v3 · v2) — 다르면 거부
  ② 본 덱의 고정 줄 (행 번호 + 내용) · 뺄 구역의 명령 꼴 · 끝 구역 명령 꼴 확인 — 다르면 거부 (어느 행 · 어느 § 인지 적는다)
  ③ 가지 덱 = 본 덱을 줄 단위로 그대로 옮기고 등록된 줄만 바꿈 (§4-1 · §4-2 · §4-3 · §4-5)
  ④ 허용 목록 대조 — 가지 덱 명령 (LIGGGHTS 줄 규칙 · resume_ckpt.sh 의 deck() 와 같음) ↔ 본 덱 명령에 등록 바꿈만
       적용한 목록 · 줄 단위로도 본 덱 줄 그대로인지 — 한 글자라도 다르면 거부 (파일을 하나도 쓰지 않는다)
  ⑤ A · F · A3 · F3 = `resume_ckpt.sh -C` 정적 대조 문제가 정확히 하나 (§8-1: 재개 지점 뒤 순서 줄 수 12 ↔ 0 · rc 1)
  ⑥ 러너 = 리포 러너 렌더 (`make_se_size_decks.render_ibb_runner` · `hit_command`) — ibb 러너는 본 러너와
       job-name · output · -n · cd · mpirun 다섯 줄만 다르다 · `#SBATCH -n N` ↔ `mpirun … -np N` 짝 (N = Q5)
  ⑦ 쓰기 = 새 폴더 하나 (<out>/q5_<case>_<가지>/ · 이미 있으면 거부) · 가지 덱 · 러너 · 본 덱 사본 · q5_manifest.json
       (입력 · 출력 sha256) · SHA256SUMS — 임시 폴더에 다 쓴 뒤 이름 바꾸기 (거부 = 파일 0)
  ⑧ 체크포인트 복사 · sha256 = 운영자 몫 — 정확한 cp · sha256sum 줄을 화면 · manifest 에 낸다 (같아야 제출)

물리 숫자는 새로 만들지 않는다 — 바뀌는 값 (dt 5.0e-7 · run 2 · 400000 · thermo 2 · 2000 · mesh 10000 · s 5.3696e-4 ·
  4.2268e-2 · 덤프 간격 66667 · 200001 · NP) 은 전부 등록 문서 그대로이고, 본 덱 값 (dt 1.0e-6 · 밀도 · 반지름 · run 길이)
  으로 맞는지 다시 센다 (dt/2 · step ×2 · s = ρ_SE r_SE³ / ρ_AM r_AM³ 다섯 자리).
자리 표시 둘의 읽기: §4-1 `read_restart <가지 폴더>/…` = 러너가 cd 하는 가지 폴더 기준 상대 경로 · §4-5 덤프 `<폴더>` =
  본 덱 153 행이 만드는 `post_<case>/` (따로 `shell mkdir` 줄을 더하지 않으려고).
★ B 의 dt 줄 (43 행) 은 read_restart 앞에 있다 — LIGGGHTS 3d5c00f 의 restart 머리에는 dt 가 없고 units 가 같으면
  재설정하지 않는다 (Codex 증거 사본 upstream_src_write_restart.cpp · upstream_src_read_restart.cpp · selftest ⓪b 가 본다)
  → 43 행 바꿈이 살아 있다.  판독기는 로그의 `timestep 5e-07` 치환 줄로 다시 확인한다.

사용 (WSL · 리포 안 · 아무것도 띄우지 않는다)
    python3 scripts/kg50_q5_branches.py --case kg50_d07_b50 --branch A --np 56 --out ~/q5_build
    python3 scripts/kg50_q5_branches.py --verify ~/q5_build/q5_kg50_d07_b50_A
    python3 scripts/kg50_q5_branches.py --selftest
웹앱 화면 없음 (일회성 등록 대조 도구 · 판정은 scripts/kg50_q5_verdict.py).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
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
WINDOW_S = {'W1': '0.200001'}                      # Q3 (나) — W1 = 판 높이 1 µs + 안정화 0.2 s
DT_HALF = '5.0e-7'                                 # §4-2 43 행
EXPECTED_STATIC_PROBLEM = '재개 지점 뒤 순서 줄 수 다름: 본 덱 12 ↔ 재개 덱 0'    # §8-1
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
)

#: 거부 관문 — selftest 변이 (하나를 끄면 그것을 겨눈 시험이 실패해야 한다).  생산에서는 늘 True.
GUARDS = {k: True for k in ('registration', 'case', 'branch', 'np', 'window', 'pin', 'anchors', 's_check', 'allowlist',
                            'static', 'runner', 'out_exists')}


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


# ───────────────────────── LIGGGHTS 줄 규칙 (resume_ckpt.sh deck() 와 같음) ─────────────────────────
def _uncomment(s):
    raise NotImplementedError('구현 전 (시험 먼저)')


def norm(s):
    """명령 한 줄 정리 — 주석 빼고 공백 하나로."""
    raise NotImplementedError('구현 전 (시험 먼저)')


def commands(text):
    """LIGGGHTS 명령 목록 [(명령, 첫 행, 끝 행)] — '&' 이어 붙이기 (원 줄 끝) → 주석 · 공백 정리 · 빈 명령 빼기 · 행 = 1 부터."""
    raise NotImplementedError('구현 전 (시험 먼저)')


# ───────────────────────── ⓪ 등록 문서 · LIGGGHTS 소스 전제 ─────────────────────────
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
    m = re.search(r'\| Q12 \| 덤프 간격 W1 atom ([0-9,]+) · contact ([0-9,]+) ·', txt)
    if not m or (int(m.group(1).replace(',', '')), int(m.group(2).replace(',', ''))) != (ATOM_EVERY, CONTACT_EVERY):
        probs.append(f'Q12 덤프 간격 ≠ 생성기 ({ATOM_EVERY} · {CONTACT_EVERY})')
    m = re.search(r'\| \(가\) AM 기준 \(권고\) \| [^|]+\| ([0-9.e+-]+) \| ([0-9.e+-]+) \|', txt)
    if not m or (m.group(1), m.group(2)) != (CASES['kg50_d07_b50']['s'], CASES['kg50_d3_b50_s1']['s']):
        probs.append('§4-3 s (가) ≠ 생성기 (%s · %s)' % (CASES['kg50_d07_b50']['s'], CASES['kg50_d3_b50_s1']['s']))
    for ln, a, b in B_EDITS:
        if ln == 203:
            continue                               # 표는 `dump dmp_mesh … 5000 …` 로 줄여 적었다 (위 고정 줄)
        if f'| {ln} | `{a}` | `{b}` |' not in txt:
            probs.append(f'§4-2 {ln} 행 표 ≠ 생성기 ({a} → {b})')
    if f'`{EXPECTED_STATIC_PROBLEM}` 하나 · 그 밖 문제 0 (rc 1)' not in txt:
        probs.append('§8-1 정적 대조 기대 문제 ≠ 생성기')
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


# ───────────────────────── ① ② 본 덱 ─────────────────────────
def pinned_sha(case):
    """본 덱 sha256 = 덱 묶음 manifest.json 의 deck_sha256 (그 덱을 만든 생성기의 기록)."""
    raise NotImplementedError('구현 전 (시험 먼저)')


def check_anchors(text, case):
    """본 덱 고정 줄 · 구역 꼴 — 문제 목록."""
    raise NotImplementedError('구현 전 (시험 먼저)')


def derive(text, case):
    """본 덱에서 다시 세는 값 — dt · 체크포인트 step · 반지름 · 밀도 · 접촉 열 · 압력 면적."""
    raise NotImplementedError('구현 전 (시험 먼저)')


def s_from_deck(d):
    """Q2 (가) s = m_SE/m_AM = ρ_SE r_SE³ / (ρ_AM r_AM³) (본 덱 템플릿 · 변수 · type 3 ↔ type 1)."""
    raise NotImplementedError('구현 전 (시험 먼저)')


# ───────────────────────── ③ 가지 덱 · ④ 허용 목록 ─────────────────────────
def _lead(raw):
    raise NotImplementedError('구현 전 (시험 먼저)')


def _dump_lines(case):
    raise NotImplementedError('구현 전 (시험 먼저)')


UNDUMP_LINES = ['undump dq5a', 'undump dq5c']


def _edits(case, branch):
    """가지마다 바꾸는 행 → (A 명령, 가지 명령)."""
    raise NotImplementedError('구현 전 (시험 먼저)')


def header(case, branch, main_sha):
    raise NotImplementedError('구현 전 (시험 먼저)')


def build_text(main_text, case, branch, main_sha):
    """가지 덱 글자 — 본 덱 줄을 그대로 옮기고 등록 바꿈만 (§4-1 · §4-2 · §4-3 · §4-5)."""
    raise NotImplementedError('구현 전 (시험 먼저)')


def expected_commands(main_text, case, branch):
    """등록 바꿈을 본 덱 **명령** 에 적용한 가지 명령 목록 — 생성기 (줄 바꿈) 와 다른 길.  본 덱 바꿀 줄이 등록 A 값이 아니면 문제."""
    raise NotImplementedError('구현 전 (시험 먼저)')


def _strip_header(text):
    """생성기 머리 (주석 줄만 · & 로 끝나는 줄 없음 — LIGGGHTS 가 다음 줄을 주석에 이어 붙인다) 를 뗀 본문 · 아니면 None."""
    raise NotImplementedError('구현 전 (시험 먼저)')


def verify_branch_deck(main_text, branch_text, case, branch):
    """④ 허용 목록 대조 — 문제 목록 (빈 목록 = 통과).  명령 단위 + 줄 단위 (본 덱 줄 그대로 · 순서)."""
    raise NotImplementedError('구현 전 (시험 먼저)')


# ───────────────────────── ⑤ 정적 대조 ─────────────────────────
def static_check(main_path, deck_path, case, tool=None):
    """`resume_ckpt.sh -C` (재개 덱 정적 대조) — 출력 · 종료 코드 · 문제 줄."""
    raise NotImplementedError('구현 전 (시험 먼저)')


# ───────────────────────── ⑥ 러너 ─────────────────────────
RUNNER_DIFF_OK = (re.compile(r'^#SBATCH --job-name=\S+$'), re.compile(r'^#SBATCH --output=logs/output_\S+_%j\.out$'),
                  re.compile(r'^#SBATCH -n [0-9]+$'), re.compile(r'^cd \S+$'),
                  re.compile(r'^mpirun --oversubscribe --bind-to none -np [0-9]+ lmp_mpi -in \S+$'))


def folder_name(case, branch):
    raise NotImplementedError('구현 전 (시험 먼저)')


def render_runner(case, branch, np_, template_path=None):
    """러너 글자 — ibb = 리포 러너 렌더 (본 러너와 같은 틀) · hit = hit_command (SLURM 없음)."""
    raise NotImplementedError('구현 전 (시험 먼저)')


def runner_check(case, branch, np_, text):
    """러너 대조 — 문제 목록.  ibb: 본 러너와 다섯 줄만 다름 · -n N ↔ -np N · cd · -in.  hit: 명령 한 줄 = hit_command."""
    raise NotImplementedError('구현 전 (시험 먼저)')


# ───────────────────────── ⑦ ⑧ 쓰기 · 운영자 명령 ─────────────────────────
def expected_steps(s0, end, every):
    raise NotImplementedError('구현 전 (시험 먼저)')


def operator_commands(man):
    """체크포인트 복사 · sha256 · 제출 — 운영자가 붙여 넣을 줄 (아무것도 띄우지 않는다)."""
    raise NotImplementedError('구현 전 (시험 먼저)')


def _check_request(case, branch, np_, window):
    raise NotImplementedError('구현 전 (시험 먼저)')


def build_branch(case, branch, np_, out_parent, window='W1', main_deck=None, *, pinned=None, runner_template=None,
                 resume_tool=None, registration=None, tamper=None):
    """가지 폴더 하나 — 반환 manifest.  거부 = Refused (파일 0).  pinned · runner_template · resume_tool · registration · tamper =
    selftest 이음새 (생산 CLI 에 없음)."""
    raise NotImplementedError('구현 전 (시험 먼저)')


def verify_folder(folder):
    """만든 가지 폴더 다시 대조 (판독기 · 운영자) — 문제 목록.  manifest · 본 덱 사본 sha256 = 등록 덱 · 가지 덱 허용 목록 · 러너."""
    raise NotImplementedError('구현 전 (시험 먼저)')


def main(argv=None):
    ap = argparse.ArgumentParser(description='50kg Q5 가지 덱 생성기 (등록 Q11 · W1 · 허용 목록 대조)')
    ap.add_argument('--case', choices=sorted(CASES), help='본 덱 케이스 (등록 §2)')
    ap.add_argument('--branch', help='가지 (D0.7: A B C F · D3: A3 C3 F3)')
    ap.add_argument('--np', type=int, help='MPI 수 (등록 Q5 와 같아야 한다)')
    ap.add_argument('--out', help='가지 폴더를 만들 상위 폴더 (그 안에 q5_<case>_<가지>/ · 이미 있으면 거부)')
    ap.add_argument('--window', default='W1', help='창 (W1 만 · W2 는 등록 개정 뒤)')
    ap.add_argument('--main-deck', default=None, help='본 덱 경로 (기본 = 리포 덱 · sha256 이 등록 덱과 같아야)')
    ap.add_argument('--verify', default=None, metavar='FOLDER', help='만든 가지 폴더를 다시 대조 (rc 0 = 통과)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
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
        man = build_branch(a.case, a.branch, a.np, os.path.expanduser(a.out), a.window, a.main_deck)
    except Refused as e:
        print(f'⛔ 거부 — 가지 덱 안 냄 (파일 0): {e}')
        return 2
    dst = os.path.join(os.path.expanduser(a.out), man['folder'])
    print(f'✓ {dst}/  가지 {man["branch"]} ({man["kind"]}) · NP {man["np"]} · {man["host"]} · 창 W1 · 끝 step {man["end_step"]} · '
          f'atom 덤프 {len(man["atom_dump"]["steps"])} · contact {len(man["contact_dump"]["steps"])}')
    for x in man['changes']:
        print('    · ' + x)
    if man['static_check'] is not None:
        print(f'  resume_ckpt.sh -C = rc {man["static_check"]["rc"]} · 문제 {man["static_check"]["problems"]} (등록 §8-1 하나 = 통과)')
    print('\n# 운영자 (복사 · sha256 · 제출 — 1저자):')
    print(f'scp -P <포트> -r {dst} <사용자>@<{man["host"]}>:{CASES[man["case"]]["run_root"]}/' if man['host'] == 'ibb'
          else f'scp -r {dst} <사용자>@<hit>:{CASES[man["case"]]["run_root"]}/')
    for x in man['operator_commands']:
        print(x)
    return 0


# ───────────────────────────── selftest ─────────────────────────────
def selftest():
    import io
    from contextlib import redirect_stdout
    tally = [0, 0]

    def chk(label, cond, extra=''):
        tally[1] += 1
        tally[0] += bool(cond)
        print(f'  {"✓" if cond else "✗"} {label}{(" — " + str(extra)[:300]) if extra and not cond else ""}')

    def run(label, fn):
        try:
            fn()
        except Exception as e:          # noqa: BLE001 — 구현 전 · 예외 = 그 묶음 실패로 센다
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
    chk('⓪ 등록 문서 고정 줄 (§2 · §3 · §4-1 · §4-2 · §4-3 · §4-5 · §5 · §8 · Q2 · Q3 · Q5 · Q11 · Q12) = 생성기 상수', ok, why)
    ok, why = source_premise_check()
    chk('⓪b LIGGGHTS 3d5c00f 원문 사본 — restart 머리에 dt 없음 · units 같으면 재설정 안 함 → B 의 43 행 dt 가 살아남는다', ok, why)
    D07, D3 = 'kg50_d07_b50', 'kg50_d3_b50_s1'
    repo_before = {c: _sha256_file(os.path.join(ROOT, CASES[c]['deck'])) for c in CASES}
    tmp = tempfile.mkdtemp(prefix='q5st_')
    built = {}
    try:
        def g_build():
            for case in (D07, D3):
                for br in CASES[case]['branches']:
                    built[br] = build_branch(case, br, NP[br], os.path.join(tmp, 'out'))
        run('G0 일곱 가지 만들기', g_build)

        def rd(br, which='deck'):
            m = built[br]
            return _read(os.path.join(tmp, 'out', m['folder'], m[which]['file']))

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
            chk('G1c A 정적 대조 (resume_ckpt.sh -C) = rc 1 · 문제 하나 = 등록 §8-1 글자',
                m['static_check']['rc'] == 1 and m['static_check']['problems'] == [EXPECTED_STATIC_PROBLEM], m['static_check'])
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
            chk('G4c F · F3 정적 대조 = 등록 하나', built['F']['static_check']['problems'] == [EXPECTED_STATIC_PROBLEM]
                and built['F3']['static_check']['problems'] == [EXPECTED_STATIC_PROBLEM]
                and built['A3']['static_check']['problems'] == [EXPECTED_STATIC_PROBLEM])
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
        run('G7 원본 · 다시 대조', g7)

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
                ('R4 창 W2 (§5 줄 목록 없음 · Q12 contact 간격 없음)', lambda: build_branch(D07, 'A', 56, out, 'W2'), '§5'),
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
                f.write(_read(os.path.join(ROOT, REGISTRATION)).replace('| 213 | `run 200000` | `run 400000` |',
                                                                        '| 213 | `run 200000` | `run 400001` |'))
            fake = os.path.join(mdir, 'fake_resume.sh')
            with open(fake, 'w', encoding='utf-8') as f:
                f.write('echo "  ✗ %s"\necho "  ✗ 다른 문제"\nexit 1\n' % EXPECTED_STATIC_PROBLEM)
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
                'window': lambda: build_branch(D07, 'B', 56, fresh(), 'W2'),
                'pin': lambda: build_branch(D07, 'B', 56, fresh(), main_deck=p_pin),
                'anchors': lambda: build_branch(D07, 'B', 56, fresh(), main_deck=p_anc, pinned=s_anc),
                's_check': lambda: build_branch(D07, 'C', 56, fresh(), main_deck=p_s, pinned=s_s),
                'allowlist': lambda: build_branch(D07, 'B', 56, fresh(),
                                                  tamper=lambda t: t.replace('gravity 9.81 vector', 'gravity 9.80 vector')),
                'static': lambda: build_branch(D07, 'A', 56, fresh(), resume_tool=fake),
                'runner': lambda: build_branch(D07, 'B', 56, fresh(), runner_template=tmpl),
                'out_exists': lambda: build_branch(D07, 'B', 56, pre),
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
