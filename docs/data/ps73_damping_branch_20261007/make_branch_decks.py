#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ps73 감쇠 가지 실험 (DEMP-01) — r8 재개 덱 꼴에서 덱 다섯 개를 만든다 (덱을 손으로 고치지 말 것).

    python3 docs/data/ps73_damping_branch_20261007/make_branch_decks.py             # 덱 · 판 STL · deck_diffs.txt · SHA256SUMS 다시 쓰기
    python3 docs/data/ps73_damping_branch_20261007/make_branch_decks.py --check     # 커밋본 = 생성 결과 · SHA256SUMS 일치 (다르면 rc 1)
    python3 docs/data/ps73_damping_branch_20261007/make_branch_decks.py --selftest  # 구조 검사 + r8 원 덱 (리포 tgz) 부분열 대조

왜 생성기인가
  다섯 덱 (t0 · A · B · C1 · C2) 이 r8 머리 · 압축 고리 · 가드 · 스냅숏 · 서보 블록을 **같은 글자로** 나눠 쓴다.
  0 단계 문법 시험 (t0) 이 그 블록을 한 번씩 다 지나가므로, WSL 에서 t0 가 통과하면 arm 덱의 같은 블록도 LIGGGHTS 가 읽는다.
  손으로 다섯 벌을 고치면 이 보증이 깨진다 → 블록을 고칠 때는 이 파일을 고치고 다시 만든다 (`--check` 가 어긋남을 잡는다).

r8 = `input_ps_7_3_r45_r8.liggghts` — ibb 에서 compress_2650000 에서 이어 압축 끝 (3,125,000) · 이완 (100,000 step) 까지 완주한 재개 덱.
  원자료 = docs/data/ps73_compaction_curve_20261006/raw/ps73_logs.tgz (sha256 은 그 폴더 README).  tgz 는 **글자 데이터로만** 읽는다.

LIGGGHTS 문법 근거 (LIGGGHTS-PUBLIC 3d5c00f20519e6bb6eb6756f51f1ad36564e649d — ibb · WSL 소스 트리 HEAD 와 같다,
docs/data/liggghts_add_pair_pin.json) — README §8 에 줄 번호와 함께 적었다:
  · mesh/surface/stress/servo = 메시 모듈 (src/mesh_module_stress_servo.cpp): sp = −target_val · 오차 = sp − F·axis ·
    판 속도 = −vel_max·kp·오차/|sp| (axis 방향 · |v| ≤ vel_max) · 전역 벡터 = stress 9 (힘 3 · 토크 3 · 기준점 3) + servo 3 (질량중심)
    → f_ID[3] = 판이 받는 z 힘 (위 = +) · f_ID[12] = 판 z.  move/mesh 와 같은 메시에 둘 수 없다.
  · `$` 는 따옴표 안에서 줄 읽을 때 치환되지 않는다 — if 는 조건을, print 는 글을 스스로 치환한다 (src/input.cpp).
  · if 조건 = 숫자 · 비교 · && || ! · 괄호뿐 (산술 · inf · nan 없음 · src/variable.cpp evaluate_boolean) → 문턱은 변수로 미리 계산.
  · equal · string 변수는 다시 정의할 수 있다 · index 변수는 첫 정의 (명령행 -var 포함) 가 이긴다.
  · dump_modify ID first yes = 만든 뒤 첫 run 의 setup 에서 한 장 쓴다 (src/output.cpp) · run 0 = setup 만 (적분 없음).
  · 각 run 의 init 에서 모든 시간 의존 compute 에 현재 step 을 건다 (src/modify.cpp addstep_compute_all) → setup 덤프의 c_strs 유효.
  · thermo_modify lost 기본 = ignore (src/thermo.cpp) → 원자를 잃어도 런이 멈추지 않는다 → 원자 수 가드가 필요하다.
  · write_restart = lmp->init() → compute 의 invoked 를 지운다 → 그 뒤 run 전까지 thermo ke 를 읽으면 ERROR
    (10-07 WSL t0 1 회 FAIL · README §12) · run 0 은 메시 응력 합을 지우지 않고 wall/gran setup 몫을 더한다 → run 0 뒤 판 힘 =
    직전 합 + rank 몫 (직렬 2 배).  ⇒ run 뒤 읽는 값은 정의 바로 다음 줄에서 얼린다 · selftest ⑭ 가 모든 경로를 본다.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import io
import os
import re
import subprocess
import sys
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
CURVE_DIR = os.path.normpath(os.path.join(HERE, '..', 'ps73_compaction_curve_20261006'))
R8_TGZ = os.path.join(CURVE_DIR, 'raw', 'ps73_logs.tgz')
R8_MEMBER = 'home/yonghoon/dem_test/ps45/ps_7_3_r45/input_ps_7_3_r45_r8.liggghts'
MESH_TGZ = os.path.join(CURVE_DIR, 'raw', 'ps73_curve_1.tgz')
MESH_MEMBER = 'post_ps_7_3_r45/mesh_3100000.stl'

# ── 출발점 (README §1 · 숫자마다 근거) ─────────────────────────────────────────
CKPT_SHA256 = '82234bea543ae369043f54d4379c6451cdab5a404213c0ecf0a698638bf4b3ee'   # 1저자 10-07 ibb = WSL
CKPT_SIZE = 80807696
STEP_BRANCH = 3100000
PZ_BRANCH = '0.111302'        # mesh_3100000.stl (= 1,650,000 의 0.125802 − 1e-8 × 1,450,000)
KE_REF = '1.695918e-05'       # r8 로그 3,100,000 정규 줄 = 같은 step setup 줄
P_REF_3105000 = '0.29712724'  # r8 로그 3,105,000 (덱 MPa) — t0 가 한 덩어리 뒤 대조
P_REF_3101000 = '0.29635467'  # r8 로그 3,101,000 (덱 MPa) — run_branch.sh 의 G3 (첫 정규 줄)
PZ_T0_STOP = '0.111252'       # t0 멈춤 (3,105,000) 판 높이 = 0.111302 − 0.01 × 1e-6 × 5000
N_ATOMS_BRANCH = 160420

ATOM_COLS = 'id type x y z radius vx vy vz c_strs[1] c_strs[2] c_strs[3] c_ke'
CPL_COLS = ('    c_cpl[1] c_cpl[2] c_cpl[3] c_cpl[4] c_cpl[5] c_cpl[6] c_cpl[7] c_cpl[8] &\n'
            '    c_cpl[9] c_cpl[10] c_cpl[11] c_cpl[12] c_cpl[13] c_cpl[14] c_cpl[15] c_cpl[16] &\n'
            '    c_cpl[17] c_cpl[18] c_cpl[19] c_cpl[20] c_cpl[21] c_cpl[22] c_cpl[23] c_cpl[24] &\n'
            '    c_cpl[25] c_cpl[26]')

DECKS = {
    't0': 'in.branch_t0_syntax.liggghts',
    'A': 'in.branch_A.liggghts',
    'B': 'in.branch_B.liggghts',
    'C1': 'in.branch_C1.liggghts',
    'C2': 'in.branch_C2.liggghts',
}
PLATE_STL = 'plate_branch3100000.stl'
DIFF_TXT = 'deck_diffs.txt'
SUMS = 'SHA256SUMS'
SBATCH = 'run_branch_ibb.sbatch'   # ibb 제출 래퍼 (1저자 10-08 "10 코어로") — 손으로 쓴 파일 · 생성하지 않는다 (⑮ 가 짝을 본다)
SUMMED = list(DECKS.values()) + [PLATE_STL, 'run_branch.sh', 'make_branch_decks.py', 'analyze_branch.py', SBATCH]
SBATCH_NP = 10
# 10-07 WSL t0 1 회에 돈 덱 그대로 (FAIL · README §12) — ⑭c 가 검사기로 다시 잡는다 (덱 묶음 SHA256SUMS 에는 넣지 않는다)
RUN1_DECK = os.path.join('t0_run1_20261007', 'in.branch_t0_syntax.liggghts')
RUN1_SHA = 'c0130fd0a5019ca916f6135bb18f97b1e37ef292bc3b681985af43c0beafdf42'

# arm 별 등록값 (README §2 · §3) — 여기 말고 덱을 고치지 말 것
#   comp_win = 감쇠를 바꾼 뒤 KE 10 배 규칙을 쉬는 덩어리 수 (그동안은 0.1 J 상한만) — C 만 8 (README §7:
#   γ 0.5 → 0.05 로 내리면 저항이 받치던 늦음이 과감쇠로 풀려 첫 덩어리 끝 KE 가 어림 20–30 배 뛴다 · 터짐이 아니다)
ARMS = {
    'A': dict(gamma='0.5', atom_every=5000, restart_every=50000, comp_max=40, comp_win=0, post='relax',
              relax_steps=100000, relax_contact_every=10000),
    'B': dict(gamma='0.5', atom_every=5000, restart_every=50000, comp_max=40, comp_win=0, post='servo'),
    'C1': dict(gamma='0.15', atom_every=50000, restart_every=100000, comp_max=400, comp_win=8, post='relax',
               relax_steps=100000, relax_contact_every=50000),
    'C2': dict(gamma='0.05', atom_every=50000, restart_every=100000, comp_max=400, comp_win=8, post='relax',
               relax_steps=100000, relax_contact_every=50000),
}

NOTES = {
    't0': ('#   t0 = 0 단계 문법 시험 (수 분 · 판정에 쓰지 않는다): r8 머리 → G1 (run 0) → 압축 고리 한 덩어리 (목표를 0 으로 두어 5000 step 뒤 나온다)\n'
           '#        → 멈춤 스냅숏 → 이완 블록 200 step → 끝 스냅숏 (top_mesh) → 서보 전환 → 서보 유지 500 step × 2 → 끝 스냅숏 (서보)\n'
           '#        → 요약 → 서보 점검 → 가드 정지 경로를 일부러 탄다.  arm 덱의 블록을 **같은 글자로** 다 지나간다 (make_branch_decks.py --selftest).'),
    'A': ('#   arm A (선택 · 재현) = 원 프로토콜 그대로: 판 0.01 · viscous 0.5 · 5000 step 마다 압력 판정 0.30 (덱 MPa) → 판 고정 · viscous 1e-5 ·\n'
          '#        100,000 step 이완.  r8 와 다른 줄 = 경로 (-var) · 가드 · 기록 · 멈춤/끝 스냅숏 (run 0) — 역학 줄은 r8 와 같다.'),
    'B': ('#   arm B (주 측정 · DEMP-01 공극률 질문의 답) = 압축은 A 와 같은 줄 → 멈춘 step 스냅숏 (= A 의 판 고정 상태와 같은 두께) →\n'
          '#        판을 서보로 (mesh/surface/stress/servo · 목표 750 N = 0.30 덱 MPa × 0.0025 m² · vel_max 0.01 = press_speed · kp 30) ·\n'
          '#        viscous 1e-5 (이완과 같다) · 수렴 (|F/750 − 1| ≤ 1 % · 5000 step 당 판 이동 ≤ 5e-6 m · 4 연속 · 10 덩어리 뒤) 또는\n'
          '#        300 덩어리 (1.5 M step) 까지 → 끝 스냅숏.'),
    'C1': ('#   arm C1 (선택 · A · B 뒤) = 체크포인트부터 압축 감쇠만 viscous 0.15 (저항 어림 17 %) · 판 · 판정 · 이완은 A 와 같다.\n'
           '#        출력 간격만 다르다 (원자 50,000 · restart 100,000 · 이완 접촉 50,000) — 역학 불변.  KE 10 배 규칙은 첫 8 덩어리 쉰다 (0.1 J 상한).'),
    'C2': ('#   arm C2 (선택 · A · B 뒤) = 체크포인트부터 압축 감쇠만 viscous 0.05 (저항 어림 6 %) · 판 · 판정 · 이완은 A 와 같다.\n'
           '#        출력 간격만 다르다 (원자 50,000 · restart 100,000 · 이완 접촉 50,000) — 역학 불변.  KE 10 배 규칙은 첫 8 덩어리 쉰다 (0.1 J 상한).'),
}

# ── 블록 (LIGGGHTS 글자 · @이름@ = 생성기가 채우는 자리) ────────────────────────────

T_HEADER = """\
# ============================================================
# ps_7_3_r45 DEMP-01 감쇠 가지 실험 — @ARM_TITLE@
#   생성: make_branch_decks.py (손으로 고치지 말 것 — 생성기를 고치고 다시 만든다 · SHA256SUMS)
#   출발: read_restart ${ckpt} = restart_compress_3100000.bin (ibb 원 런 · 압축 중 마지막 체크포인트 · step 3100000)
#         sha256 82234bea543ae369043f54d4379c6451cdab5a404213c0ecf0a698638bf4b3ee · 80,807,696 B
#   꼴  : r8 재개 덱 (input_ps_7_3_r45_r8.liggghts) 그대로 + 표지 블록 (# >>> block … / # <<< block …) = r8 에 없는 줄
#   변수: run_branch.sh 가 -var 로 준다 — ckpt (체크포인트) · out (이 런의 새 폴더) · plate_stl (판 STL · 자료는 restart 에서 온다)
@ARM_NOTE@
# ============================================================

"""

T_HEAD = """\
# --- 1. General Settings ---
atom_style      granular
atom_modify     map array sort 0 0
boundary        p p f
newton          off
soft_particles  yes
communicate     single vel yes
units           si

# --- 2. Variables & Domain ---
variable target_press equal 0.30          # 300 MPa × 0.001
variable r_AM_P  equal 4.5e-3            # AM_P r=4.5μm → Sim 4.5mm
variable r_AM_S  equal 2.0e-3            # AM_S r=2μm → Sim 2mm
variable r_SE    equal 0.5e-3            # SE r=0.5μm → Sim 0.5mm
variable dt      equal 1.0e-6
variable plate_margin equal 0.003
timestep        ${dt}

# RVE: 50×50 μm → Sim 0.05×0.05 m
processors * * 1

read_restart    ${ckpt}

neighbor        0.002 bin
neigh_modify    delay 0 check yes

# --- 3. Material Properties (Type 1:AM_P, 2:AM_S, 3:SE) ---
# AM: E=140 GPa → Sim 1.4e8 Pa, ν=0.25
# SE: E=1.35 GPa → Sim 0.135e7 Pa (소성변형 보정), ν=0.30
fix m1 all property/global youngsModulus peratomtype 1.4e8 1.4e8 0.135e7
fix m2 all property/global poissonsRatio peratomtype 0.25 0.25 0.30

fix m3 all property/global coefficientRestitution peratomtypepair 3 &
    0.3 0.3 0.3 &
    0.3 0.3 0.3 &
    0.3 0.3 0.3

fix m4 all property/global coefficientFriction peratomtypepair 3 &
    0.5 0.5 0.5 &
    0.5 0.5 0.5 &
    0.5 0.5 0.5

fix m5 all property/global coefficientRollingFriction peratomtypepair 3 &
    0.2 0.2 0.1 &
    0.2 0.2 0.1 &
    0.1 0.1 0.1

fix m6 all property/global coefficientMaxElasticStiffness peratomtypepair 3 &
    1.5 1.5 3.0 &
    1.5 1.5 3.0 &
    3.0 3.0 5.0

fix m7 all property/global coefficientAdhesionStiffness peratomtypepair 3 &
    1.0e5 1.0e5 2.0e5 &
    1.0e5 1.0e5 2.0e5 &
    2.0e5 2.0e5 1.0e6

fix m8 all property/global coefficientPlasticityDepth peratomtypepair 3 &
    0.05 0.05 0.01 &
    0.05 0.05 0.01 &
    0.01 0.01 0.005

fix m9 all property/global characteristicVelocity scalar 2.0

# --- 4. Contact Model ---
pair_style      gran model hooke/hysteresis tangential history rolling_friction cdt
pair_coeff      * *

compute strs all stress/atom
compute ke   all ke/atom
compute cpl all pair/gran/local pos id force force_normal force_tangential torque contactArea delta contactPoint

# --- 5. Wall (Bottom) ---
fix zwall_bot all wall/gran model hooke/hysteresis tangential history rolling_friction cdt primitive type 1 zplane 0.0

# --- 6. Templates & Distribution --- (r8 와 같이 생략: compress 체크포인트에는 type 1 · 2 · 3 원자가 다 있다)

"""

T_SETUP = """\
# --- 8. Output ---
# (r8 의 `shell mkdir -p post_ps_7_3_r45` 는 뺐다 — 출력 폴더는 run_branch.sh 가 만든다 · LIGGGHTS shell mkdir 는 -p 도 폴더 이름으로 만든다)
thermo_style    custom step atoms ke cpu
thermo          1000

# --- 9. 압축 단계 fix 재선언 (r8 그대로 · r8 주석의 "Phase 1: Settling" 은 원 덱에서 따온 이름일 뿐) ---
fix integr all nve/sphere
fix gravi all gravity 9.81 vector 0.0 0.0 -1.0
fix damp all viscous @GAMMA@

fix top_mesh all mesh/surface/stress file ${plate_stl} type 1 scale 1.0 reference_point 0 0 0
fix zwall_top all wall/gran model hooke/hysteresis tangential history rolling_friction cdt mesh n_meshes 1 meshes top_mesh

dump dmp_mesh all mesh/stl 5000 ${out}/post/mesh_*.stl top_mesh

variable pressMPa equal abs(f_top_mesh[3])/0.0025/1000000
thermo_style    custom step atoms ke cpu v_pressMPa
thermo 1000

print "====== PHASE 3: COMPRESSION (Speed 0.01) ======"
dump dmp_atom all custom @ATOM_EVERY@ ${out}/post/atom_*.liggghts @ATOM_COLS@
fix_modify      zwall_top energy yes

variable press_speed equal 0.01
fix move_press all move/mesh mesh top_mesh linear 0.0 0.0 -${press_speed}

restart @RESTART_EVERY@ ${out}/restart/restart_compress_*.bin
"""

T_GUARD_INIT = """\
# >>> block guard_init — 가지 기준값 · 기록 (r8 에 없음 · 읽기 · 판정 전용 · 역학 불변)
variable br_arm string @ARM@
variable gamma_comp string @GAMMA@
variable summary_file string ${out}/branch_summary.txt
# equal 변수는 쓸 때마다 다시 계산된다 — 가지 시작 값은 즉시 치환으로 숫자를 박아 얼린다 (br_step0 · br_n0v)
variable br_step_now equal step
variable br_step0 equal ${br_step_now}
if "${br_step0} != @STEP_BRANCH@" then "print 'BRANCH_ABORT step=${br_step0} — 기대 @STEP_BRANCH@ (체크포인트가 다르다)'" "quit"
variable br_atoms_now equal atoms
variable br_n0v equal ${br_atoms_now}
variable g_amin equal ${br_n0v}-50
variable pz_branch equal @PZ_BRANCH@
variable F_target equal 750.0
region rg_below block INF INF INF INF INF 0.0 units box
region rg_above block INF INF INF INF ${pz_branch} INF units box
variable g_leak equal count(all,rg_below)+count(all,rg_above)
variable br_leak0 equal ${g_leak}
variable ke_ref equal @KE_REF@
variable ke_prev equal ${ke_ref}
variable ke_abs_comp equal 100*${ke_ref}
variable ke_floor_comp equal 10*${ke_ref}
variable comp_win equal @COMP_WIN@
variable ke_abs_comp_win equal 0.1
variable comp_n equal 0
variable comp_max equal @COMP_MAX@
variable g_reason string none
variable g_step equal ${br_step0}
variable g_atoms equal ${br_n0v}
variable g_pz equal ${pz_branch}
variable g_F equal 0.0
variable g_ke equal ${ke_ref}
variable g_leakd equal 0
variable current_press equal 0.0
print "BRANCH_START arm=${br_arm} step=${br_step0} atoms=${br_n0v} leak0=${br_leak0} gamma_comp=${gamma_comp} plate_z_deck=${pz_branch}"
print "step,phase,plate_z_deck,press_deckMPa,force_N,ke_J,atoms,leak_delta" file ${out}/branch_trace.csv screen no
# <<< block guard_init

"""

T_COMP_GUARD = """\
    variable g_step equal step
    variable g_step equal ${g_step}
    variable g_atoms equal atoms
    variable g_atoms equal ${g_atoms}
    variable g_ke equal ke
    variable g_ke equal ${g_ke}
    variable g_F equal abs(f_top_mesh[3])
    variable g_F equal ${g_F}
    variable g_pz equal ${pz_branch}-${press_speed}*${dt}*(${g_step}-${br_step0})
    region rg_above delete
    region rg_above block INF INF INF INF ${g_pz} INF units box
    variable g_leakd equal ${g_leak}-${br_leak0}
    variable g_kelim equal 10*${ke_prev}
    print "${g_step},comp,${g_pz},${current_press},${g_F},${g_ke},${g_atoms},${g_leakd}" append ${out}/branch_trace.csv screen no
    if "${g_atoms} < ${g_amin}" then "variable g_reason string atoms_lost" "jump SELF guard_stop"
    if "${g_leakd} > 100" then "variable g_reason string leak" "jump SELF guard_stop"
    if "(${comp_n} <= ${comp_win}) && (${g_ke} > ${ke_abs_comp_win})" then "variable g_reason string ke_abs_win" "jump SELF guard_stop"
    if "(${comp_n} > ${comp_win}) && (${g_ke} > ${ke_abs_comp})" then "variable g_reason string ke_abs" "jump SELF guard_stop"
    if "(${comp_n} > ${comp_win}) && (${g_ke} > ${g_kelim}) && (${g_ke} > ${ke_floor_comp})" then "variable g_reason string ke_jump" "jump SELF guard_stop"
    if "${comp_n} >= ${comp_max}" then "variable g_reason string comp_budget" "jump SELF guard_stop"
    variable ke_prev equal ${g_ke}
"""

T_COMP_LOOP = """\
# >>> block comp_loop — r8 압축 고리 그대로 (run 5000 · 압력 판정 0.30) + 덩어리마다 가드 · 기록 (run 사이 · 역학 불변)
#   run 뒤에 읽는 값은 정의 바로 다음 줄에서 같은 이름의 즉시 치환으로 얼린다 (같은 step 의 값을 숫자로 박는다) — 뒤의 write_restart 는
#   ke 를 '현재 아님' 으로 (ERROR) · run 0 은 판 힘을 '직전 합 + rank 몫' 으로 바꾼다 (README §8 · §12 · make_branch_decks.py ⑭)
label loop_press
    run 5000
    variable current_press equal "abs(f_top_mesh[3]) / 0.0025 / 1000000"
    variable current_press equal ${current_press}
    print "Current Pressure: ${current_press} MPa (Target: ${target_press})"
    variable comp_n equal ${comp_n}+1
@COMP_GUARD@\
    if "${current_press} < ${target_press}" then "jump SELF loop_press"
# <<< block comp_loop

"""

T_STOP = """\
# >>> block stop_snap — 멈춘 step 의 상태 (원자 · 접촉 · 판) · run 0 = setup 만 (적분 없음 · 역학 불변) · restart
unfix move_press
variable br_S equal ${g_step}
variable br_pz_S equal ${g_pz}
variable br_P_S equal ${current_press}
variable br_F_S equal ${g_F}
variable br_h_S equal ${br_pz_S}*1000
print "BRANCH_STOP arm=${br_arm} step=${br_S} plate_z_deck=${br_pz_S} thickness_um=${br_h_S} press_deckMPa=${br_P_S} force_N=${br_F_S}"
print "${br_S},stop,${br_pz_S},${br_P_S},${br_F_S},${g_ke},${g_atoms},${g_leakd}" append ${out}/branch_trace.csv screen no
dump dmp_atom_stop all custom 5000 ${out}/stop/atom_*.liggghts @ATOM_COLS@
dump_modify dmp_atom_stop first yes
dump dmp_contact_stop all local 5000 ${out}/stop/contact_*.liggghts &
@CPL_COLS@
dump_modify dmp_contact_stop first yes
dump dmp_mesh_stop all mesh/stl 5000 ${out}/stop/mesh_*.stl top_mesh
dump_modify dmp_mesh_stop first yes
run 0
undump dmp_atom_stop
undump dmp_contact_stop
undump dmp_mesh_stop
write_restart ${out}/restart/restart_stop_${br_S}.bin
# <<< block stop_snap

"""

T_RELAX = """\
# >>> block relax — r8 PHASE 4 그대로 (판 고정 · viscous 1e-5) · 경로 · 접촉 간격만 표지
print "====== PHASE 4: RELAXATION ======"
unfix damp
fix damp all viscous 1.0e-5
dump dmp_contact all local @RELAX_CONTACT_EVERY@ ${out}/post/contact_*.liggghts &
@CPL_COLS@

run @RELAX_STEPS@
# <<< block relax

"""

T_END = """\
# >>> block end_snap_@MESH_FIX@ — 끝 상태 (원자 · 접촉 · 판) · run 0 · restart
#   값은 run 0 전에 읽어 얼린다 — run 0 뒤 f_@MESH_FIX@[3] 는 직전 step 합 + 이 rank 의 setup 몫 (직렬 2 배) · write_restart 뒤 ke 는 ERROR (README §12)
variable g_step equal step
variable g_step equal ${g_step}
variable g_atoms equal atoms
variable g_atoms equal ${g_atoms}
variable g_ke equal ke
variable g_ke equal ${g_ke}
variable g_Fz equal f_@MESH_FIX@[3]
variable g_Fz equal ${g_Fz}
variable g_F equal abs(f_@MESH_FIX@[3])
variable g_F equal ${g_F}
variable current_press equal "abs(f_@MESH_FIX@[3]) / 0.0025 / 1000000"
variable current_press equal ${current_press}
variable g_pz equal @PZ_EXPR@
variable g_pz equal ${g_pz}
region rg_above delete
region rg_above block INF INF INF INF ${g_pz} INF units box
variable g_leakd equal ${g_leak}-${br_leak0}
variable br_E equal ${g_step}
variable br_pz_E equal ${g_pz}
variable br_h_E equal ${br_pz_E}*1000
variable br_P_E equal ${current_press}
variable br_F_E equal ${g_F}
variable br_Fz_E equal ${g_Fz}
print "BRANCH_END_STATE arm=${br_arm} dir=@DIR@ step=${br_E} plate_z_deck=${br_pz_E} thickness_um=${br_h_E} press_deckMPa=${br_P_E} force_N=${br_F_E} atoms=${g_atoms} leak_delta=${g_leakd}"
print "${br_E},@DIR@,${br_pz_E},${br_P_E},${br_F_E},${g_ke},${g_atoms},${g_leakd}" append ${out}/branch_trace.csv screen no
dump dmp_atom_end all custom 5000 ${out}/@DIR@/atom_*.liggghts @ATOM_COLS@
dump_modify dmp_atom_end first yes
dump dmp_contact_end all local 5000 ${out}/@DIR@/contact_*.liggghts &
@CPL_COLS@
dump_modify dmp_contact_end first yes
dump dmp_mesh_end all mesh/stl 5000 ${out}/@DIR@/mesh_*.stl @MESH_FIX@
dump_modify dmp_mesh_end first yes
run 0
undump dmp_atom_end
undump dmp_contact_end
undump dmp_mesh_end
write_restart ${out}/restart/restart_@DIR@_${br_E}.bin
# <<< block end_snap_@MESH_FIX@

"""

T_SERVO_SWITCH = """\
# >>> block servo_switch — 판을 서보로 바꾼다 (r8 에 없음 · arm B)
#   src/mesh_module_stress_servo.cpp (3d5c00f): sp = −target_val · 오차 = sp − F·axis · 판 속도 = −vel_max·kp·오차/|sp| (axis 방향) ·
#   |속도| ≤ vel_max.  axis 0 0 −1 · target_val +750 → 판이 받는 위 방향 힘 F < 750 N 이면 −z (아래) 로 간다 · 넘으면 위로.
#   move/mesh 와 같은 메시에 둘 수 없다 → 옛 판 (top_mesh) 을 지우고 같은 높이 (${br_pz_S}) 에 새 판을 만든다.
#   ⚠ 판–입자 접촉 이력 (접선 · hysteresis) 은 여기서 새로 시작한다 (fix wall/gran 을 다시 만들기 때문 · README §10).
variable servo_kp index 30
variable servo_vmax index 0.01
print "====== PHASE 4B: SERVO HOLD (target ${F_target} N · vel_max ${servo_vmax} · kp ${servo_kp}) ======"
undump dmp_mesh
unfix zwall_top
unfix top_mesh
print "solid plate_servo" file ${out}/plate_servo_stop.stl screen no
print "facet normal 0 0 -1" append ${out}/plate_servo_stop.stl screen no
print "outer loop" append ${out}/plate_servo_stop.stl screen no
print "vertex 0.0 0.0 ${br_pz_S}" append ${out}/plate_servo_stop.stl screen no
print "vertex 0.05 0.05 ${br_pz_S}" append ${out}/plate_servo_stop.stl screen no
print "vertex 0.05 0.0 ${br_pz_S}" append ${out}/plate_servo_stop.stl screen no
print "endloop" append ${out}/plate_servo_stop.stl screen no
print "endfacet" append ${out}/plate_servo_stop.stl screen no
print "facet normal 0 0 -1" append ${out}/plate_servo_stop.stl screen no
print "outer loop" append ${out}/plate_servo_stop.stl screen no
print "vertex 0.0 0.0 ${br_pz_S}" append ${out}/plate_servo_stop.stl screen no
print "vertex 0.0 0.05 ${br_pz_S}" append ${out}/plate_servo_stop.stl screen no
print "vertex 0.05 0.05 ${br_pz_S}" append ${out}/plate_servo_stop.stl screen no
print "endloop" append ${out}/plate_servo_stop.stl screen no
print "endfacet" append ${out}/plate_servo_stop.stl screen no
print "endsolid plate_servo" append ${out}/plate_servo_stop.stl screen no
fix plate_servo all mesh/surface/stress/servo file ${out}/plate_servo_stop.stl type 1 scale 1.0 com 0.025 0.025 ${br_pz_S} ctrlPV force axis 0.0 0.0 -1.0 target_val ${F_target} vel_max ${servo_vmax} kp ${servo_kp}
fix zwall_top all wall/gran model hooke/hysteresis tangential history rolling_friction cdt mesh n_meshes 1 meshes plate_servo
fix_modify zwall_top energy yes
dump dmp_mesh all mesh/stl 5000 ${out}/post_hold/mesh_*.stl plate_servo
unfix damp
fix damp all viscous 1.0e-5
variable pressMPa equal abs(f_plate_servo[3])/0.0025/1000000
undump dmp_atom
dump dmp_atom all custom 50000 ${out}/post_hold/atom_*.liggghts @ATOM_COLS@
restart 100000 ${out}/restart/restart_hold_*.bin
# <<< block servo_switch

"""

T_HOLD = """\
# >>> block hold — 서보 유지 고리 (덩어리마다 가드 · 수렴 판정 · 기록)
#   수렴 = |F/750 − 1| ≤ conv_ferr 이고 덩어리 사이 판 이동 ≤ conv_dz (덱 m) 가 conv_need 번 이어짐 (hold_min 덩어리 뒤) · 아니면 hold_max 에서 멈춤
#   KE 가드: 처음 hold_win 덩어리는 판을 멈춘 원 런 이완과 같은 풀림 (원 런 최대 0.0764 J) 이 나오므로 1.0 J 만 본다 (README §7)
variable hold_chunk index 5000
variable hold_max index 300
variable hold_win equal 10
variable hold_min equal 10
variable ke_abs_win equal 1.0
variable ke_abs_hold equal 1.0e-2
variable ke_floor_hold equal 1.0e-3
variable F_max equal 2*${F_target}
variable conv_ferr equal 0.01
variable conv_dz equal 5.0e-6
variable conv_need equal 4
variable hold_n equal 0
variable conv_n equal 0
variable pz_prev equal ${br_pz_S}
variable hold_status string RUNNING
print "BRANCH_HOLD_PARAMS target_N=${F_target} vel_max=${servo_vmax} kp=${servo_kp} chunk=${hold_chunk} max_chunks=${hold_max} conv_ferr=${conv_ferr} conv_dz=${conv_dz} conv_need=${conv_need}"
label loop_hold
    run ${hold_chunk}
    variable hold_n equal ${hold_n}+1
    variable g_step equal step
    variable g_step equal ${g_step}
    variable g_atoms equal atoms
    variable g_atoms equal ${g_atoms}
    variable g_ke equal ke
    variable g_ke equal ${g_ke}
    variable g_F equal f_plate_servo[3]
    variable g_F equal ${g_F}
    variable g_pz equal f_plate_servo[12]
    variable g_pz equal ${g_pz}
    variable current_press equal "abs(f_plate_servo[3]) / 0.0025 / 1000000"
    variable current_press equal ${current_press}
    region rg_above delete
    region rg_above block INF INF INF INF ${g_pz} INF units box
    variable g_leakd equal ${g_leak}-${br_leak0}
    variable g_dz equal abs(${g_pz}-${pz_prev})
    variable g_ferr equal abs(${g_F}/${F_target}-1.0)
    variable g_kelim equal 10*${ke_prev}
    print "Hold ${hold_n}: step ${g_step} F ${g_F} N (target ${F_target}) plate_z ${g_pz} dz ${g_dz} KE ${g_ke}"
    print "${g_step},hold,${g_pz},${current_press},${g_F},${g_ke},${g_atoms},${g_leakd}" append ${out}/branch_trace.csv screen no
    if "${g_atoms} < ${g_amin}" then "variable g_reason string atoms_lost" "jump SELF guard_stop"
    if "${g_leakd} > 100" then "variable g_reason string leak" "jump SELF guard_stop"
    if "${g_ke} > ${ke_abs_win}" then "variable g_reason string ke_abs" "jump SELF guard_stop"
    if "(${hold_n} > ${hold_win}) && (${g_ke} > ${ke_abs_hold})" then "variable g_reason string ke_abs_late" "jump SELF guard_stop"
    if "(${hold_n} > ${hold_win}) && (${g_ke} > ${g_kelim}) && (${g_ke} > ${ke_floor_hold})" then "variable g_reason string ke_jump" "jump SELF guard_stop"
    if "${g_F} > ${F_max}" then "variable g_reason string servo_overshoot" "jump SELF guard_stop"
    if "(${g_ferr} <= ${conv_ferr}) && (${g_dz} <= ${conv_dz})" then "variable conv_n equal ${conv_n}+1" else "variable conv_n equal 0"
    variable pz_prev equal ${g_pz}
    variable ke_prev equal ${g_ke}
    if "(${conv_n} >= ${conv_need}) && (${hold_n} >= ${hold_min})" then "variable hold_status string CONVERGED" "jump SELF hold_done"
    if "${hold_n} >= ${hold_max}" then "variable hold_status string BUDGET_EXHAUSTED" "jump SELF hold_done"
    jump SELF loop_hold
label hold_done
print "BRANCH_HOLD_DONE arm=${br_arm} status=${hold_status} chunks=${hold_n} step=${g_step} F=${g_F} plate_z=${g_pz}"
# <<< block hold

"""

T_SUMMARY = """\
# >>> block summary_@SUMMARY_KIND@ — 요약 (key=value · run_branch.sh · analyze_branch.py 가 읽는다)
print "arm=${br_arm}" file ${summary_file} screen no
print "gamma_comp=${gamma_comp}" append ${summary_file} screen no
print "ckpt_step=${br_step0}" append ${summary_file} screen no
print "atoms_start=${br_n0v}" append ${summary_file} screen no
print "leak_start=${br_leak0}" append ${summary_file} screen no
print "stop_step=${br_S}" append ${summary_file} screen no
print "stop_plate_z_deck=${br_pz_S}" append ${summary_file} screen no
print "stop_thickness_um=${br_h_S}" append ${summary_file} screen no
print "stop_press_deckMPa=${br_P_S}" append ${summary_file} screen no
print "stop_force_N=${br_F_S}" append ${summary_file} screen no
@SUMMARY_EXTRA@\
print "end_step=${br_E}" append ${summary_file} screen no
print "end_plate_z_deck=${br_pz_E}" append ${summary_file} screen no
print "end_thickness_um=${br_h_E}" append ${summary_file} screen no
print "end_press_deckMPa=${br_P_E}" append ${summary_file} screen no
print "end_force_N=${br_F_E}" append ${summary_file} screen no
print "atoms_end=${g_atoms}" append ${summary_file} screen no
print "leak_delta_end=${g_leakd}" append ${summary_file} screen no
print "guard=none" append ${summary_file} screen no
print "result=DONE" append ${summary_file} screen no
print "BRANCH_DONE arm=${br_arm} stop_step=${br_S} stop_thickness_um=${br_h_S} end_step=${br_E} end_thickness_um=${br_h_E} end_press_deckMPa=${br_P_E}"
# <<< block summary_@SUMMARY_KIND@

"""

SUMMARY_EXTRA = {
    'servo': ('print "hold_status=${hold_status}" append ${summary_file} screen no\n'
              'print "hold_chunks=${hold_n}" append ${summary_file} screen no\n'
              'print "hold_chunk_steps=${hold_chunk}" append ${summary_file} screen no\n'
              'print "servo_kp=${servo_kp}" append ${summary_file} screen no\n'
              'print "servo_vmax=${servo_vmax}" append ${summary_file} screen no\n'),
    'relax': 'print "relax_steps=@RELAX_STEPS@" append ${summary_file} screen no\n',
}

T_FINISH = """\
print "====== Simulation Finished! (PS_7_3_R45: P:S=7:3, 81.6:18.4, 6mAh/cm2) ======"

"""

T_GUARD_STOP = """\
# >>> block guard_stop — 가드가 멈추면 여기로 온다 (restart + 요약 · 이어 돌리지 않는다)
jump SELF branch_end
label guard_stop
print "BRANCH_GUARD_TRIP arm=${br_arm} reason=${g_reason} step=${g_step} atoms=${g_atoms} ke=${g_ke} leak_delta=${g_leakd}"
print "${g_step},guard_${g_reason},${g_pz},${current_press},${g_F},${g_ke},${g_atoms},${g_leakd}" append ${out}/branch_trace.csv screen no
print "arm=${br_arm}" append ${summary_file} screen no
print "guard=${g_reason}" append ${summary_file} screen no
print "guard_step=${g_step}" append ${summary_file} screen no
print "result=GUARD_TRIP" append ${summary_file} screen no
write_restart ${out}/restart/restart_guard_${g_step}.bin
label branch_end
print "BRANCH_SCRIPT_END arm=${br_arm}"
# <<< block guard_stop
"""

# t0 전용 블록 ─────────────────────────────────────────────────────────────────
T_T0_G1 = """\
# >>> block t0_g1 — G1: 재개 첫 setup (step · 원자 수 정확 · KE 1e-6 · docs/resume_ckpt_procedure_20260927.md §3)
run 0
variable t0_n equal atoms
variable t0_n equal ${t0_n}
variable t0_ke0 equal ke
variable t0_ke0 equal ${t0_ke0}
variable t0_g1 equal abs(${t0_ke0}/${ke_ref}-1.0)
print "T0_G1 step=${br_step0} atoms=${t0_n} ke=${t0_ke0} rel=${t0_g1} (기준 r8 로그 3100000 KE @KE_REF@ · 원자 @N_ATOMS@)"
if "(${t0_g1} <= 1.0e-6) && (${t0_n} == @N_ATOMS@)" then "print 'T0_G1 PASS'" else "print 'T0_G1 FAIL'"
# t0 만: 목표를 0 으로 두어 압축 고리가 한 덩어리 (5000 step) 뒤 나오게 한다 — 고리 글자는 arm 과 같다
variable target_press equal 0.0
# <<< block t0_g1

"""

T_T0_G3 = """\
# >>> block t0_g3 — 한 덩어리 뒤 (3105000) 원자 수 · 판 압력 5 % (G3 의 첫 정규 줄 3101000 대조는 run_branch.sh 가 로그로 한다)
variable target_press equal 0.30
variable t0_p1 equal ${current_press}
variable t0_g3 equal abs(${t0_p1}/@P_REF_3105000@-1.0)
print "T0_G3 step=${g_step} atoms=${g_atoms} press_deckMPa=${t0_p1} rel=${t0_g3} (기준 r8 로그 3105000 @P_REF_3105000@)"
if "(${t0_g3} <= 0.05) && (${g_atoms} == @N_ATOMS@)" then "print 'T0_G3 PASS'" else "print 'T0_G3 FAIL'"
# 판 높이 공식 (가지 시작 값이 얼었는가): 3105000 = 0.111302 − 0.01 × 1e-6 × 5000 = @PZ_T0_STOP@ · run_branch.sh 가 stop 메시 덤프와도 대조한다
variable t0_pzerr equal abs(${g_pz}-@PZ_T0_STOP@)
print "T0_PZ plate_z_deck=${g_pz} expect=@PZ_T0_STOP@ err=${t0_pzerr}"
if "${t0_pzerr} <= 1.0e-12" then "print 'T0_PZ PASS'" else "print 'T0_PZ FAIL'"
# <<< block t0_g3

"""

T_T0_HOLD_PARAMS = """\
# >>> block t0_hold_params — t0 만: 서보 유지를 500 step × 2 덩어리로 줄인다 (hold 블록의 index 기본값보다 먼저)
variable hold_chunk index 500
variable hold_max index 2
# <<< block t0_hold_params

"""

T_T0_SERVO = """\
# >>> block t0_servo — 서보 점검: 판이 내려갔고 (vel_max 를 넘지 않았고) 힘 부호가 위 (+) 인가 · 그 뒤 가드 정지 경로를 일부러 탄다
variable t0_dz equal ${br_pz_S}-${br_pz_E}
variable t0_dzmax equal ${servo_vmax}*${dt}*${hold_n}*${hold_chunk}*1.000001
# 판 힘 = 끝 스냅숏이 run 0 전에 얼린 값 (br_Fz_E · 부호 그대로 · 위 = +).  10-07 t0 1 회 덱은 여기서 f_plate_servo[3] 를 새로 읽었다 —
#   run 0 뒤라 직전 step 합 + 이 rank 의 setup 몫 (직렬 ≈ 2 배 — 'F < 750' 판정이 틀어진다) · README §12 · make_branch_decks.py ⑭
print "T0_SERVO dz=${t0_dz} dzmax=${t0_dzmax} F_signed=${br_Fz_E} target=${F_target} status=${hold_status}"
if "(${t0_dz} > 0.0) && (${t0_dz} <= ${t0_dzmax}) && (${br_Fz_E} > 0.0) && (${br_Fz_E} < ${F_target})" then "print 'T0_SERVO PASS'" else "print 'T0_SERVO FAIL'"
print "T0_DONE"
variable g_reason string t0_forced
variable summary_file string ${out}/branch_summary_forced_trip.txt
jump SELF guard_stop
# <<< block t0_servo

"""


def fill(t: str, **kw) -> str:
    for k, v in kw.items():
        t = t.replace('@' + k + '@', str(v))
    left = re.findall(r'@[A-Z0-9_]+@', t)
    if left:
        raise SystemExit(f'⛔ 채우지 않은 자리: {sorted(set(left))}')
    return t


def comp_guard():
    return T_COMP_GUARD


def blocks_for(arm: str):
    """→ [(블록 이름, 글자)] — 덱은 이 순서로 잇는다."""
    common = dict(ATOM_COLS=ATOM_COLS, CPL_COLS=CPL_COLS)
    if arm == 't0':
        p = dict(gamma='0.5', atom_every=5000, restart_every=50000, comp_max=40, comp_win=0)
    else:
        p = ARMS[arm]
    out = [
        ('header', fill(T_HEADER, ARM_TITLE=('0 단계 문법 시험 (t0)' if arm == 't0' else f'arm {arm}'),
                        ARM_NOTE=NOTES[arm])),
        ('head', T_HEAD),
        ('setup', fill(T_SETUP, GAMMA=p['gamma'], ATOM_EVERY=p['atom_every'],
                       RESTART_EVERY=p['restart_every'], **common)),
        ('guard_init', fill(T_GUARD_INIT, ARM=arm, GAMMA=p['gamma'], STEP_BRANCH=STEP_BRANCH,
                            PZ_BRANCH=PZ_BRANCH, KE_REF=KE_REF, COMP_MAX=p['comp_max'], COMP_WIN=p['comp_win'])),
    ]
    if arm == 't0':
        out.append(('t0_g1', fill(T_T0_G1, KE_REF=KE_REF, N_ATOMS=N_ATOMS_BRANCH)))
    out.append(('comp_loop', fill(T_COMP_LOOP, COMP_GUARD=comp_guard())))
    if arm == 't0':
        out.append(('t0_g3', fill(T_T0_G3, P_REF_3105000=P_REF_3105000, N_ATOMS=N_ATOMS_BRANCH,
                                  PZ_T0_STOP=PZ_T0_STOP)))
    out.append(('stop_snap', fill(T_STOP, **common)))
    end_fixed = fill(T_END, MESH_FIX='top_mesh', PZ_EXPR='${br_pz_S}', DIR='end', **common)
    end_servo = fill(T_END, MESH_FIX='plate_servo', PZ_EXPR='f_plate_servo[12]', DIR='end', **common)
    if arm == 't0':
        out += [
            ('relax', fill(T_RELAX, RELAX_STEPS=200, RELAX_CONTACT_EVERY=10000, **common)),
            ('end_snap_top_mesh', fill(T_END, MESH_FIX='top_mesh', PZ_EXPR='${br_pz_S}', DIR='end_relax', **common)),
            ('servo_switch', fill(T_SERVO_SWITCH, **common)),
            ('t0_hold_params', T_T0_HOLD_PARAMS),
            ('hold', T_HOLD),
            ('end_snap_plate_servo', end_servo),
            ('summary_servo', fill(T_SUMMARY, SUMMARY_KIND='servo', SUMMARY_EXTRA=SUMMARY_EXTRA['servo'])),
            ('t0_servo', T_T0_SERVO),
            ('guard_stop', T_GUARD_STOP),
        ]
    elif p['post'] == 'servo':
        out += [
            ('servo_switch', fill(T_SERVO_SWITCH, **common)),
            ('hold', T_HOLD),
            ('end_snap_plate_servo', end_servo),
            ('summary_servo', fill(T_SUMMARY, SUMMARY_KIND='servo', SUMMARY_EXTRA=SUMMARY_EXTRA['servo'])),
            ('finish', T_FINISH),
            ('guard_stop', T_GUARD_STOP),
        ]
    else:
        out += [
            ('relax', fill(T_RELAX, RELAX_STEPS=p['relax_steps'], RELAX_CONTACT_EVERY=p['relax_contact_every'],
                           **common)),
            ('end_snap_top_mesh', end_fixed),
            ('summary_relax', fill(T_SUMMARY, SUMMARY_KIND='relax',
                                   SUMMARY_EXTRA=fill(SUMMARY_EXTRA['relax'], RELAX_STEPS=p['relax_steps']))),
            ('finish', T_FINISH),
            ('guard_stop', T_GUARD_STOP),
        ]
    return out


def render(arm: str) -> str:
    return ''.join(t for _, t in blocks_for(arm))


def plate_stl() -> str:
    z = PZ_BRANCH
    rows = ['solid plate', 'facet normal 0 0 -1', 'outer loop',
            f'vertex 0.0 0.0 {z}', f'vertex 0.05 0.05 {z}', f'vertex 0.05 0.0 {z}',
            'endloop', 'endfacet', 'facet normal 0 0 -1', 'outer loop',
            f'vertex 0.0 0.0 {z}', f'vertex 0.0 0.05 {z}', f'vertex 0.05 0.05 {z}',
            'endloop', 'endfacet', 'endsolid plate']
    return '\n'.join(rows) + '\n'


def deck_diffs() -> str:
    buf = io.StringIO()
    buf.write('# make_branch_decks.py 가 만든다 — arm 덱 사이의 차이 (unified diff · 머리 주석 줄 제외)\n')
    base = [ln for ln in render('A').splitlines(keepends=True) if not ln.startswith('#   ')]
    for arm in ('B', 'C1', 'C2'):
        other = [ln for ln in render(arm).splitlines(keepends=True) if not ln.startswith('#   ')]
        buf.writelines(difflib.unified_diff(base, other, fromfile='in.branch_A.liggghts',
                                            tofile=DECKS[arm], n=1))
        buf.write('\n')
    return buf.getvalue()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def generated_files() -> dict:
    out = {name: render(arm) for arm, name in DECKS.items()}
    out[PLATE_STL] = plate_stl()
    out[DIFF_TXT] = deck_diffs()
    return out


def write_all():
    for name, text in generated_files().items():
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
    write_sums()
    print('✓ 덱 · 판 STL · deck_diffs.txt · SHA256SUMS 를 다시 썼다')


def sums_text() -> str:
    lines = []
    for name in SUMMED:
        p = os.path.join(HERE, name)
        if not os.path.exists(p):
            raise SystemExit(f'⛔ SHA256SUMS 대상이 없다: {name}')
        lines.append(f'{sha256_file(p)}  {name}')
    return '\n'.join(lines) + '\n'


def write_sums():
    with open(os.path.join(HERE, SUMS), 'w', encoding='utf-8', newline='\n') as f:
        f.write(sums_text())


def check() -> int:
    bad = []
    for name, text in generated_files().items():
        p = os.path.join(HERE, name)
        if not os.path.exists(p) or open(p, encoding='utf-8').read() != text:
            bad.append(f'{name}: 커밋본 ≠ 생성 결과 (make_branch_decks.py 로 다시 만들 것)')
    sp = os.path.join(HERE, SUMS)
    if not os.path.exists(sp) or open(sp, encoding='utf-8').read() != sums_text():
        bad.append(f'{SUMS}: 현재 파일 해시와 다르다')
    for b in bad:
        print('✗', b)
    if not bad:
        print(f'✓ check: 덱 다섯 · 판 STL · deck_diffs.txt = 생성 결과 · SHA256SUMS 일치 ({len(SUMMED)} 파일 · ibb 래퍼 포함)')
    return 1 if bad else 0


# ── selftest ─────────────────────────────────────────────────────────────────

def logical_lines(text: str):
    """주석 · 빈 줄 빼고 `&` 이음을 붙인 명령 줄 (LIGGGHTS 읽기와 같게 · 공백은 하나로)."""
    out, cur = [], ''
    for raw in text.splitlines():
        s = raw.rstrip()
        cont = s.endswith('&')
        if cont:
            s = s[:-1]
        cur += ' ' + s
        if cont:
            continue
        line = strip_comment(cur).strip()
        cur = ''
        if line:
            out.append(' '.join(line.split()))
    return out


def strip_comment(s: str) -> str:
    q = ''
    for i, ch in enumerate(s):
        if ch == '#' and not q:
            return s[:i]
        if q and ch == q:
            q = ''
        elif not q and ch in '"\'':
            q = ch
    return s


def words(line: str):
    """LIGGGHTS nextword 와 같게 — 따옴표 묶음은 한 낱말 (따옴표 뒤는 공백이어야 한다)."""
    out, i, n = [], 0, len(line)
    while i < n:
        while i < n and line[i].isspace():
            i += 1
        if i >= n:
            break
        if line[i] in '"\'':
            j = line.find(line[i], i + 1)
            if j < 0:
                raise ValueError(f'따옴표가 닫히지 않는다: {line}')
            if j + 1 < n and not line[j + 1].isspace():
                raise ValueError(f'따옴표 뒤가 공백이 아니다: {line}')
            out.append(line[i + 1:j])
            i = j + 1
        else:
            j = i
            while j < n and not line[j].isspace():
                j += 1
            out.append(line[i:j])
            i = j
    return out


def commands_with_nested(lines):
    """if 의 then / else 명령도 풀어서 함께 돌려준다."""
    for ln in lines:
        yield ln
        w = words(ln)
        if w and w[0] == 'if':
            for k in w[2:]:
                if k not in ('then', 'else', 'elif'):
                    yield ' '.join(k.split())


def r8_text() -> str:
    with tarfile.open(R8_TGZ, 'r:gz') as t:
        m = t.getmember(R8_MEMBER)
        if not m.isfile():
            raise SystemExit('⛔ r8 원 덱이 tgz 안의 보통 파일이 아니다')
        return t.extractfile(m).read().decode('utf-8')


def r8_expected(arm: str, r8_lines):
    """r8 명령 줄에 등록된 바꿈만 적용한 목록 — arm 덱에 이 순서로 다 있어야 한다 (부분열)."""
    p = ARMS[arm]
    rep = {
        'read_restart restart_ps_7_3_r45/restart_compress_2650000.bin': 'read_restart ${ckpt}',
        'shell mkdir -p post_ps_7_3_r45': None,
        'fix damp all viscous 0.5': f'fix damp all viscous {p["gamma"]}',
        'fix top_mesh all mesh/surface/stress file plate_ps_7_3_r45_r8.stl type 1 scale 1.0 reference_point 0 0 0':
            'fix top_mesh all mesh/surface/stress file ${plate_stl} type 1 scale 1.0 reference_point 0 0 0',
        'dump dmp_mesh all mesh/stl 5000 post_ps_7_3_r45/mesh_*.stl top_mesh':
            'dump dmp_mesh all mesh/stl 5000 ${out}/post/mesh_*.stl top_mesh',
        f'dump dmp_atom all custom 5000 post_ps_7_3_r45/atom_*.liggghts {ATOM_COLS}':
            f'dump dmp_atom all custom {p["atom_every"]} ${{out}}/post/atom_*.liggghts {ATOM_COLS}',
        'restart 50000 restart_ps_7_3_r45/restart_compress_*.bin':
            f'restart {p["restart_every"]} ${{out}}/restart/restart_compress_*.bin',
    }
    cpl = ' '.join(f'c_cpl[{i}]' for i in range(1, 27))
    contact_r8 = f'dump dmp_contact all local 10000 post_ps_7_3_r45/contact_*.liggghts {cpl}'
    if p['post'] == 'servo':
        rep[contact_r8] = None
        rep['print "====== PHASE 4: RELAXATION ======"'] = None
        rep['run 100000'] = None
    else:
        rep[contact_r8] = (f'dump dmp_contact all local {p["relax_contact_every"]} '
                           f'${{out}}/post/contact_*.liggghts {cpl}')
        rep['run 100000'] = f'run {p["relax_steps"]}'
    seen = set()
    out = []
    for ln in r8_lines:
        if ln in rep:
            seen.add(ln)
            if rep[ln] is not None:
                out.append(rep[ln])
        else:
            out.append(ln)
    missing = [k for k in rep if k not in seen]
    return out, missing


def is_subsequence(needle, hay):
    it = iter(hay)
    miss = []
    for x in needle:
        for y in it:
            if y == x:
                break
        else:
            miss.append(x)
            break
    return miss


# ── ⑭ run 사이에 읽는 값 (10-08 · WSL t0 1 회 FAIL 의 부류 · README §8 · §12) ─────────────────────
#  LIGGGHTS-PUBLIC 3d5c00f 소스:
#   ㉮ write_restart = lmp->init() (src/write_restart.cpp 171) → Modify::init 이 모든 compute 의 invoked 를 −1 로 (src/modify.cpp 271–277)
#      → 다음 run 전까지 thermo 키워드 ke 를 읽으면 ERROR "Compute used in variable thermo keyword between runs is not current"
#      (src/thermo.cpp 972–985 · t0 1 회의 ERROR 줄 978).  run (0 포함) 은 thermo 줄을 찍으며 ke 를 다시 현재로 만든다.
#   ㉯ run 0 (setup 만) 은 메시 응력 합을 지우지 않는다 — 지우는 곳은 step 안의 pre_force 뿐 (src/mesh_module_stress.cpp 249–258) —
#      그 위에 fix wall/gran 의 setup 이 이 rank 의 접촉 힘을 더하고 (src/fix_wall_gran.cpp 681–687 · src/verlet.cpp Verlet::setup)
#      compute_vector 는 그 합을 돌려준다 (mesh_module_stress.cpp 432–437) ⇒ run 0 뒤 f_<메시>[1–6] = 직전 step 의 MPI 합 + 이 rank 의 몫
#      (직렬 = 2 배 — t0 1 회 끝 스냅숏 setup 줄 0.37551816 = 정규 줄 0.1877583 × 2.0000083 · r8 (24 rank) 이완 setup 줄 × 1.0265).
#      run 사이의 f_ 읽기에는 시점 검사가 없다 (src/variable.cpp 1184 = run 중일 때만) → 오류 없이 틀린 값.
#      [7–9] 기준점 · 서보 [10–12] 질량중심은 setup 이 바꾸지 않는다.  새로 만든 메시 fix 도 첫 step 전에는 0 (같은 부류로 본다).
#   ㉰ unfix 한 fix · 아직 없는 fix 를 읽으면 ERROR.
#  ⇒ 덩어리마다 읽는 값 (g_* · current_press · t0_*) 은 정의 바로 다음 줄에서 `variable X equal ${X}` 로 얼린다 (⑭b) ·
#     덱의 모든 경로 (jump · if 포함) 에서 위 ㉮ ㉯ ㉰ 상태로 읽는 곳이 없어야 한다 (⑭a).
THERMO_COMPUTE = frozenset({'ke', 'pe', 'etotal', 'enthalpy', 'temp', 'press', 'evdwl', 'ecoul', 'epair', 'ebond', 'eangle',
                            'edihed', 'eimp', 'emol', 'elong', 'etail', 'erotate', 'pxx', 'pyy', 'pzz', 'pxy', 'pxz', 'pyz'})
THERMO_NOT_BETWEEN = frozenset({'elapsed', 'elaplong', 'cpu', 'cu', 'tpcpu', 'spcpu', 'cpuremain'})   # thermo.cpp 914–961
THERMO_PLAIN = frozenset({'step', 'atoms', 'dt', 'time', 'part', 'vol', 'lx', 'ly', 'lz', 'xlo', 'xhi', 'ylo', 'yhi', 'zlo', 'zhi',
                          'xy', 'xz', 'yz', 'xlat', 'ylat', 'zlat', 'nbuild', 'ndanger'})
GROUP_FUNCS = frozenset({'count', 'mass', 'charge', 'xcm', 'vcm', 'fcm', 'bound', 'gyration', 'ke', 'angmom', 'torque',
                         'inertia', 'omega'})
# 일부러 살아 있게 두는 equal 변수 (⑭b 면제) — 이유를 함께 적는다
LAZY_OK = {
    'pressMPa': 'thermo_style 의 v_pressMPa — run 동안 thermo 가 읽는다 (살아 있어야 한다)',
    'g_leak': 'count(group,region) 공식 — 덩어리마다 영역을 다시 만들고 ${g_leak} 로 바로 읽는다 (compute 아님 · run 사이에도 맞다)',
    'br_step_now': '다음 줄 br_step0 가 즉시 치환으로 얼린다 (step · compute 없음)',
    'br_atoms_now': '다음 줄 br_n0v 가 즉시 치환으로 얼린다 (atoms · compute 없음)',
}


def expr_deps(expr: str) -> frozenset:
    """equal 공식이 run 사이에 무엇에 기대나 — ${…} 는 정의 때 숫자로 바뀌므로 빼고 본다.
    원소 = (종류, 이름, 첨자): k = compute 를 쓰는 thermo 키워드 · x = run 사이 금지 키워드 · t = compute 없는 thermo 키워드 ·
    g = 그룹 함수 · c / f / v = compute · fix · 변수 참조."""
    e = re.sub(r'\$\{\w+\}', '0', expr)
    deps = set()
    for kind in 'cfv':
        for m in re.finditer(r'\b' + kind + r'_(\w+)(?:\[(\d+)\])?', e):
            deps.add((kind, m.group(1), int(m.group(2) or 0)))
    e = re.sub(r'\b[cfv]_\w+(?:\[\d+\])?', '0', e)
    for m in re.finditer(r'(?<![\w.])([A-Za-z_]\w*)(\s*\()?', e):
        name, call = m.group(1), m.group(2)
        if call:
            if name in GROUP_FUNCS:
                deps.add(('g', name, 0))
        elif name in THERMO_COMPUTE:
            deps.add(('k', name, 0))
        elif name in THERMO_NOT_BETWEEN:
            deps.add(('x', name, 0))
        elif name in THERMO_PLAIN:
            deps.add(('t', name, 0))
    return frozenset(deps)


def _st_new():
    """run 사이 상태 하나 (경로마다 따로 — 서로 다른 경로를 섞지 않는다):
    ke = compute 가 현재가 아니다 (시작 · read_restart · write_restart 뒤 run 전) · fix ID → ok | polluted | gone ·
    env = 변수 → 공식 의존 (expr_deps) · thermo = thermo_style 의 v_ 이름."""
    return {'ke': True, 'fix': {}, 'env': {}, 'thermo': frozenset()}


def _st_copy(s):
    return {'ke': s['ke'], 'fix': dict(s['fix']), 'env': dict(s['env']), 'thermo': s['thermo']}


def _st_key(s):
    return (s['ke'], tuple(sorted(s['fix'].items())), tuple(sorted(s['env'].items(), key=lambda kv: kv[0])), s['thermo'])


def _resolve(name, env, seen=frozenset()):
    leaves = set()
    for d in env.get(name, frozenset()):
        if d[0] == 'v':
            if d[1] not in seen:
                leaves |= _resolve(d[1], env, seen | {name})
        else:
            leaves.add(d)
    return leaves


def _read_hazards(name, s, mesh_ids):
    out = []
    for kind, ident, idx in sorted(_resolve(name, s['env'])):
        if kind in ('k', 'c') and s['ke']:
            out.append(('stale', f'{ident if kind == "k" else "c_" + ident} 가 현재가 아니다 (write_restart · read_restart 뒤 · run 전 — ㉮)'))
        elif kind == 'x':
            out.append(('between', f'{ident} 는 run 사이에 못 읽는다 (thermo.cpp 914–961)'))
        elif kind == 'f':
            st = s['fix'].get(ident, 'absent')
            if st in ('gone', 'absent'):
                out.append(('nofix', f'f_{ident} 가 없다 (unfix 뒤 · 만들기 전 — ㉰)'))
            elif st == 'polluted' and ident in mesh_ids and (idx == 0 or 1 <= idx <= 6):
                out.append(('setup', f'f_{ident}[{idx}] 가 run 0 · 새 fix 뒤라 직전 합 + rank 몫이다 (㉯)'))
    return out


def _apply_cmd(w, s, mesh_ids):
    """명령 하나 (낱말 목록) 가 run 사이 상태를 바꾸는 몫 — s 를 고친다."""
    if not w:
        return
    c = w[0]
    if c == 'variable' and len(w) >= 3:
        s['env'][w[1]] = expr_deps(w[3]) if (w[2] == 'equal' and len(w) == 4) else frozenset()
    elif c == 'run' and len(w) >= 2:
        s['ke'] = False
        for fid, st in list(s['fix'].items()):
            if fid in mesh_ids and st != 'gone':
                s['fix'][fid] = 'polluted' if w[1] == '0' else 'ok'
    elif c in ('write_restart', 'read_restart'):
        s['ke'] = True
    elif c == 'fix' and len(w) >= 4:
        s['fix'][w[1]] = 'polluted' if w[1] in mesh_ids else 'ok'
    elif c == 'unfix' and len(w) >= 2:
        s['fix'][w[1]] = 'gone'
    elif c == 'thermo_style':
        s['thermo'] = frozenset(re.findall(r'\bv_(\w+)', ' '.join(w)))


def _if_branches(w):
    """if 낱말 → [가지 명령 목록] · else 가 있나 (LAMMPS 꼴: if b then t… elif b f… else e…)."""
    branches, cur, has_else, k = [], [], False, 3
    while k < len(w):
        t = w[k]
        if t == 'elif':
            branches.append(cur)
            cur, k = [], k + 2          # elif 다음 낱말 = 조건
            continue
        if t == 'else':
            branches.append(cur)
            cur, has_else = [], True
        else:
            cur.append(' '.join(t.split()))
        k += 1
    branches.append(cur)
    return branches, has_else


def scan_between_runs(text: str):
    """덱의 모든 경로에서 run 사이에 위험한 읽기 (㉮ ㉯ ㉰) → [(줄 번호, 변수, 종류, 설명, 명령)].
    경로마다 상태를 따로 들고 간다 (줄마다 상태 집합 — 덱의 고리는 같은 상태로 돌아오므로 유한하다).
    줄 번호 = logical_lines 의 순번 (주석 · 빈 줄 · & 이음 처리 뒤)."""
    lines = logical_lines(text)
    n = len(lines)
    W = [words(ln) for ln in lines]
    labels = {w[1]: i for i, w in enumerate(W) if len(w) >= 2 and w[0] == 'label'}
    mesh_ids = {w[1] for w in W if len(w) >= 4 and w[0] == 'fix' and 'mesh/surface/stress' in w[3]}
    found = {}
    seen = [set() for _ in range(n)]
    work = [(0, _st_new())]
    while work:
        i, s = work.pop()
        k = _st_key(s)
        if k in seen[i]:
            continue
        seen[i].add(k)
        w = W[i]
        for name in re.findall(r'\$\{(\w+)\}', lines[i]):
            for kind, why in _read_hazards(name, s, mesh_ids):
                found[(i, name, kind)] = (i, name, kind, why, lines[i])
        succ = []
        if w[0] == 'run':
            for name in sorted(s['thermo']):
                for kind, why in _read_hazards(name, s, mesh_ids):
                    if kind == 'nofix':
                        found[(i, 'v_' + name, kind)] = (i, 'v_' + name, kind, 'thermo_style 의 ' + why, lines[i])
        if w[0] == 'jump' and len(w) >= 3 and w[1] == 'SELF':
            succ.append((labels[w[2]], s))
        elif w[0] == 'quit':
            pass
        elif w[0] == 'if':
            branches, has_else = _if_branches(w)
            if not has_else:
                succ.append((i + 1, s))
            for br in branches:
                b = _st_copy(s)
                ended = False
                for cmd in br:
                    cw = words(cmd)
                    if cw[:2] == ['jump', 'SELF']:
                        succ.append((labels[cw[2]], b))
                        ended = True
                        break
                    if cw[:1] == ['quit']:
                        ended = True
                        break
                    _apply_cmd(cw, b, mesh_ids)
                if not ended:
                    succ.append((i + 1, b))
        else:
            t = _st_copy(s)
            _apply_cmd(w, t, mesh_ids)
            succ.append((i + 1, t))
        for j, s2 in succ:
            if j < n:
                work.append((j, s2))
    return sorted(found.values())


def unfrozen_lazy(text: str):
    """⑭b — 살아 있는 (run 사이에 값이 바뀌는) equal 정의 바로 다음 줄이 `variable X equal ${X}` 가 아닌 곳 (LAZY_OK 빼고)."""
    lines = logical_lines(text)
    bad = []
    for i, ln in enumerate(lines):
        w = words(ln)
        if len(w) == 4 and w[0] == 'variable' and w[2] == 'equal' and w[1] not in LAZY_OK and expr_deps(w[3]):
            nxt = lines[i + 1] if i + 1 < len(lines) else ''
            if nxt != f'variable {w[1]} equal ${{{w[1]}}}':
                bad.append(ln)
    return bad


def selftest() -> int:
    fails = []

    def chk(name, ok, detail=''):
        print(('  ✓ ' if ok else '  ✗ ') + name + ('' if ok else f'  — {detail}'))
        if not ok:
            fails.append(name)

    decks = {arm: render(arm) for arm in DECKS}
    defined_by_cli = {'ckpt', 'out', 'plate_stl'}
    for arm, text in decks.items():
        lines = logical_lines(text)
        cmds = list(commands_with_nested(lines))
        # ① 따옴표 · 낱말 (LIGGGHTS nextword 규칙)
        bad_q = []
        for ln in cmds:
            try:
                words(ln)
            except ValueError as e:
                bad_q.append(str(e))
        chk(f'{arm}: 따옴표가 닫히고 따옴표 뒤가 공백', not bad_q, bad_q[:2])
        # ② variable equal / string 은 낱말 셋 (공백 든 공식은 따옴표로)
        bad_v = []
        defined = set(defined_by_cli)
        for ln in cmds:
            w = words(ln)
            if w and w[0] == 'variable' and len(w) >= 3:
                defined.add(w[1])
                if w[2] in ('equal', 'string') and len(w) != 4:
                    bad_v.append(ln)
        chk(f'{arm}: variable equal · string = 값 한 낱말', not bad_v, bad_v[:2])
        # ③ 쓰인 ${이름} 이 다 정의돼 있다 (덱 안 · 또는 run_branch.sh 의 -var)
        used = set(re.findall(r'\$\{([A-Za-z0-9_]+)\}', text))
        chk(f'{arm}: ${{…}} 가 다 정의됨', used <= defined, sorted(used - defined))
        # ④ jump SELF X ↔ label X (한 번)
        jumps = set(re.findall(r'jump SELF (\w+)', text))
        labels = re.findall(r'^\s*label (\w+)', text, re.M)
        chk(f'{arm}: jump 의 label 이 하나씩 있다', all(labels.count(j) == 1 for j in jumps),
            [j for j in jumps if labels.count(j) != 1])
        # ⑤ if 꼴: 조건 · then · 명령 …
        bad_if = [ln for ln in lines if words(ln)[:1] == ['if'] and (len(words(ln)) < 4 or words(ln)[2] != 'then')]
        chk(f'{arm}: if = 조건 then 명령', not bad_if, bad_if[:2])
        # ⑥ if 조건에 산술 · 함수가 없다 (evaluate_boolean 은 숫자 · 비교 · 논리뿐)
        bad_b = []
        for ln in lines:
            w = words(ln)
            if w[:1] == ['if']:
                cond = re.sub(r'\$\{\w+\}', '1', w[1])
                cond = re.sub(r'\d+\.?\d*(?:[eE][-+]?\d+)?', '1', cond)     # 숫자 (지수 꼴 포함) 는 evaluate_boolean 이 읽는다
                if re.search(r'[A-Za-z_]|[+*/]', cond) or re.search(r'\d\s*-\s*\d', cond):
                    bad_b.append(ln)
        chk(f'{arm}: if 조건 = 숫자 · 비교 · 논리만', not bad_b, bad_b[:2])
        # ⑦ 탭 · 자리 표지 · 줄 끝 & 뒤 공백 · 호스트 주소 없음
        chk(f'{arm}: 탭 문자 없음', '\t' not in text)
        chk(f'{arm}: 채우지 않은 @…@ 없음', not re.search(r'@[A-Z0-9_]+@', text))
        chk(f'{arm}: & 이음 뒤 공백 없음', not re.search(r'&[ \t]+$', text, re.M))
        chk(f'{arm}: 주소 · 포트 · ibb 경로 없음',
            not re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b|lustre|/home/yonghoon|-P\s*\d{2,5}\b', text))
        # ⑦b 얼려야 하는 값 (가지 시작 · 멈춤 · 끝 · 앞 덩어리) 은 상수나 즉시 치환으로만 정의한다 — equal 은 쓸 때마다 다시 계산된다
        #     (실사고 10-07 초판: `variable br_step0 equal step` → 판 높이 공식이 늘 0.111302 를 냈다)
        frozen = {'br_step0', 'br_n0v', 'br_leak0', 'br_S', 'br_pz_S', 'br_P_S', 'br_F_S', 'br_h_S', 'br_E', 'br_pz_E',
                  'br_P_E', 'br_F_E', 'br_Fz_E', 'br_h_E', 'pz_prev', 'ke_prev', 'g_amin', 'pz_branch', 'F_target', 't0_p1',
                  't0_dz'}
        bad_f = []
        for ln in cmds:
            w = words(ln)
            if len(w) == 4 and w[0] == 'variable' and w[1] in frozen and w[2] == 'equal':
                bare = re.sub(r'\$\{\w+\}', '', w[3])
                if re.search(r'\b(step|atoms|ke)\b|\bf_|\bc_|\bv_|count\(', bare):
                    bad_f.append(ln)
        chk(f'{arm}: 얼려야 하는 변수가 즉시 치환 · 상수로만 정의된다', not bad_f, bad_f[:2])
        # ⑧ 한 장 덤프 (stop · end) 마다 first yes
        for d in re.findall(r'^dump (dmp_\w+_(?:stop|end)) ', text, re.M):
            chk(f'{arm}: {d} 에 dump_modify first yes', f'dump_modify {d} first yes' in text)
        # ⑨ 서보 줄의 낱말 순서 (FixMesh → stress → servo 모듈 순으로 읽힌다)
        for ln in lines:
            if 'mesh/surface/stress/servo' in ln:
                w = words(ln)
                order = [k for k in ('file', 'type', 'scale', 'com', 'ctrlPV', 'axis', 'target_val', 'vel_max', 'kp') if k in w]
                idx = [w.index(k) for k in order]
                chk(f'{arm}: 서보 낱말 순서 · 빠짐 없음', len(order) == 9 and idx == sorted(idx), order)
                chk(f'{arm}: 서보 axis 0 0 −1 · target_val = ${{F_target}} (750)',
                    w[w.index('axis') + 1:w.index('axis') + 4] == ['0.0', '0.0', '-1.0']
                    and w[w.index('target_val') + 1] == '${F_target}')
        # ⑭a run 사이 위험한 읽기 — 덱의 모든 경로 (jump · if 포함): ㉮ write_restart 뒤 ke · ㉯ run 0 뒤 메시 힘 · ㉰ 없는 fix
        #     (10-07 WSL t0 1 회: 가드 정지 print 의 ${g_ke} 가 write_restart 뒤라 ERROR — README §12)
        try:
            hz = scan_between_runs(text)
        except Exception as e:  # noqa: BLE001 — 검사기가 덱을 못 읽는 것도 실패다
            hz = [('-', '-', 'scan', repr(e), '')]
        chk(f'{arm}: run 사이 위험한 읽기 없음 (⑭a · write_restart 뒤 ke · run 0 뒤 메시 힘 · 없는 fix)', not hz,
            [f'L{h[0]} {h[1]} {h[2]}: {h[4][:90]}' for h in hz[:4]])
        # ⑭b 덩어리마다 읽는 값 (살아 있는 equal) 은 정의 바로 다음 줄에서 `variable X equal ${X}` 로 얼린다 (면제 = LAZY_OK)
        uf = unfrozen_lazy(text)
        chk(f'{arm}: 살아 있는 equal 정의 다음 줄 = 얼림 (⑭b · 면제 {len(LAZY_OK)} 개)', not uf, uf[:3])
        # ⑭d `$` 는 늘 ${…} 꼴 (한 글자 $x 치환을 쓰지 않는다 — ⑭a 가 보는 꼴과 같게)
        chk(f'{arm}: $ 뒤는 늘 {{', not re.search(r'\$(?!\{)', text), re.findall(r'.{0,20}\$(?!\{).{0,10}', text)[:2])

    # ⑭0 검사기 자신 — 합성 덱으로 ㉮ ㉯ ㉰ 를 잡고 (반례) · 얼리면 놓아 준다 (양성)
    syn = ('read_restart ${ckpt}\nthermo_style custom step atoms ke\n'
           'fix top_mesh all mesh/surface/stress file x type 1\n')
    cases = [
        ('㉮ write_restart 뒤 살아 있는 ke (10-07 t0 의 꼴)',
         syn + 'run 5000\nvariable g_ke equal ke\nwrite_restart a.bin\nprint "ke=${g_ke}"\n', {'stale'}),
        ('㉮ 정의 다음 줄에서 얼리면 통과',
         syn + 'run 5000\nvariable g_ke equal ke\nvariable g_ke equal ${g_ke}\nwrite_restart a.bin\nprint "ke=${g_ke}"\n', set()),
        ('㉮ jump 로 간 가드 경로도 본다',
         syn + 'run 5000\nvariable g_ke equal ke\nwrite_restart a.bin\njump SELF gs\nprint "x"\nlabel gs\nprint "${g_ke}"\n', {'stale'}),
        ('㉮ if 의 jump 가지도 본다',
         syn + 'run 5000\nvariable g_ke equal ke\nwrite_restart a.bin\nif "1 > 0" then "jump SELF gs"\nquit\n'
               'label gs\nprint "${g_ke}"\n', {'stale'}),
        ('㉮ if 의 quit 가지는 끝나고 거짓 경로는 이어진다 (run 직후라 통과)',
         syn + 'run 5000\nvariable g_ke equal ke\nif "1 > 0" then "quit"\nprint "${g_ke}"\n', set()),
        ('㉮ run 0 은 ke 를 현재로 만든다 (T0_G1 꼴 통과)', syn + 'run 0\nvariable k0 equal ke\nprint "${k0}"\n', set()),
        ('㉮ read_restart 뒤 run 전 ke', syn + 'variable k0 equal ke\nprint "${k0}"\n', {'stale'}),
        ('㉮ v_ 를 거쳐도 본다',
         syn + 'run 5000\nvariable a equal ke\nvariable b equal v_a*2\nwrite_restart a.bin\nprint "${b}"\n', {'stale'}),
        ('㉯ run 0 뒤 메시 힘 (10-07 T0_SERVO 의 꼴)', syn + 'run 5000\nrun 0\nvariable F equal f_top_mesh[3]\nprint "${F}"\n',
         {'setup'}),
        ('㉯ run 0 전에 얼린 힘은 통과',
         syn + 'run 5000\nvariable F equal f_top_mesh[3]\nvariable F equal ${F}\nrun 0\nprint "${F}"\n', set()),
        ('㉯ run N>0 뒤 힘은 통과', syn + 'run 0\nrun 500\nvariable F equal abs(f_top_mesh[3])\nprint "${F}"\n', set()),
        ('㉯ 서보 질량중심 [12] 는 run 0 이 안 바꾼다', syn + 'run 5000\nrun 0\nvariable z equal f_top_mesh[12]\nprint "${z}"\n', set()),
        ('㉯ 새 메시 fix 는 첫 step 전',
         syn + 'run 5000\nfix s2 all mesh/surface/stress/servo file y type 1\nvariable F equal f_s2[3]\nprint "${F}"\n', {'setup'}),
        ('㉰ unfix 뒤 읽기', syn + 'run 5000\nvariable F equal f_top_mesh[3]\nunfix top_mesh\nprint "${F}"\n', {'nofix'}),
        ('㉰ thermo_style 의 v_ 가 지운 fix 를 가리킨 채 run',
         syn + 'variable p equal f_top_mesh[3]\nthermo_style custom step v_p\nunfix top_mesh\nrun 10\n', {'nofix'}),
        ('run 사이 금지 키워드 (cpu)', syn + 'run 10\nvariable c equal cpu\nprint "${c}"\n', {'between'}),
        ('그룹 함수 count 는 run 사이에도 맞다', syn + 'write_restart a.bin\nvariable n equal count(all)\nprint "${n}"\n', set()),
    ]
    for name, deck, want in cases:
        got = {h[2] for h in scan_between_runs(deck)}
        chk(f'⑭0 검사기: {name}', got == want, f'잡음 {sorted(got)} · 기대 {sorted(want)}')
    chk('⑭0 검사기: ⑭b 가 얼리지 않은 정의를 잡는다',
        unfrozen_lazy('run 5\nvariable g_ke equal ke\nprint "${g_ke}"\n') == ['variable g_ke equal ke'])
    chk('⑭0 검사기: ⑭b 가 얼린 정의 · 면제 · 즉시 치환 상수는 놓아 준다',
        unfrozen_lazy('variable g_ke equal ke\nvariable g_ke equal ${g_ke}\n'
                      'variable pressMPa equal abs(f_top_mesh[3])/0.0025/1000000\nvariable c equal 2*${g_ke}\n') == [])
    # ⑭c 10-07 WSL t0 1 회 덱 (그때 kit · sha256 c0130fd0…) 을 검사기가 다시 잡는다 — ERROR 가 난 자리와 T0_SERVO 의 판 힘
    run1 = os.path.join(HERE, RUN1_DECK)
    if os.path.exists(run1):
        t1 = open(run1, encoding='utf-8').read()
        chk('⑭c t0 1 회 덱 사본 = 그때 sha256', sha256_file(run1) == RUN1_SHA, sha256_file(run1))
        keys = {(h[1], h[2]) for h in scan_between_runs(t1)}
        chk('⑭c 1 회 ERROR 자리를 잡는다 — 가드 정지 print 의 ${g_ke} (write_restart 뒤 ke · thermo.cpp 978)',
            ('g_ke', 'stale') in keys, sorted(keys))
        chk('⑭c T0_SERVO 의 판 힘도 잡는다 — run 0 뒤 f_plate_servo[3] (직렬 2 배)', ('t0_Fs', 'setup') in keys, sorted(keys))
        chk('⑭c 그 덱은 ⑭b 도 어긴다', bool(unfrozen_lazy(t1)))
    else:
        chk('⑭c t0 1 회 덱 사본이 있다', False, RUN1_DECK)

    # ⑩ r8 부분열 — 등록된 바꿈 말고는 r8 명령 줄이 arm 덱에 같은 순서로 다 있다
    try:
        r8 = logical_lines(r8_text())
    except (FileNotFoundError, KeyError) as e:
        chk('r8 원 덱을 리포 tgz 에서 읽는다', False, repr(e))
        r8 = None
    if r8 is not None:
        chk('r8 원 덱 명령 줄 수 (read_restart … run 100000)', len(r8) > 40 and r8[-1].startswith('print'), len(r8))
        for arm in ('A', 'B', 'C1', 'C2'):
            exp, missing = r8_expected(arm, r8)
            chk(f'{arm}: 등록된 바꿈 대상이 r8 에 다 있다', not missing, missing)
            miss = is_subsequence(exp, logical_lines(decks[arm]))
            chk(f'{arm}: r8 명령 줄 (바꿈 적용) 이 같은 순서로 다 있다', not miss, miss)
    # ⑪ t0 가 arm 블록을 다 지나간다 (같은 이름의 블록 = 같은 글자 · 숫자 자리만 다름)
    names = {arm: [n for n, _ in blocks_for(arm)] for arm in DECKS}
    arm_blocks = set().union(*(set(names[a]) for a in ('A', 'B', 'C1', 'C2')))
    skip = {'header', 'finish', 'summary_relax'}
    chk('t0 가 arm 블록을 다 지나간다 (머리 주석 · 끝 print · relax 요약 줄 빼고)',
        arm_blocks - skip <= set(names['t0']), sorted(arm_blocks - skip - set(names['t0'])))
    tb, bb = dict(blocks_for('t0')), dict(blocks_for('B'))
    for n in ('head', 'setup', 'comp_loop', 'stop_snap', 'servo_switch', 'hold', 'end_snap_plate_servo',
              'summary_servo', 'guard_stop'):
        chk(f't0 · B 의 {n} 블록 글자가 같다', tb[n] == bb[n])
    chk('t0 · B 의 guard_init 블록 = arm 이름만 다르다',
        tb['guard_init'].replace('variable br_arm string t0', 'variable br_arm string B') == bb['guard_init'])
    ab = dict(blocks_for('A'))
    for arm in ('C1', 'C2'):
        cb = dict(blocks_for(arm))
        chk(f'A · {arm} 의 comp_loop · stop_snap · end_snap 글자가 같다',
            all(ab[n] == cb[n] for n in ('comp_loop', 'stop_snap', 'end_snap_top_mesh', 'guard_stop')))
    # ⑫ 판 STL = 원 덱 판 STL 꼴 · 높이 = mesh_3100000.stl
    try:
        with tarfile.open(MESH_TGZ, 'r:gz') as t:
            mesh = t.extractfile(t.getmember(MESH_MEMBER)).read().decode()
        zs = sorted(set(re.findall(r'vertex\s+\S+\s+\S+\s+(\S+)', mesh)))
        chk('mesh_3100000.stl 의 판 높이 = PZ_BRANCH', zs == [PZ_BRANCH], zs)
    except (FileNotFoundError, KeyError) as e:
        chk('mesh_3100000.stl 을 리포 tgz 에서 읽는다', False, repr(e))
    chk('판 STL 꼭짓점 6 개 · 높이 하나', plate_stl().count('vertex') == 6
        and set(re.findall(r'vertex \S+ \S+ (\S+)', plate_stl())) == {PZ_BRANCH})
    # ⑬ 등록값
    chk('C1 · C2 감쇠 = 0.15 · 0.05 (1저자 10-07)', ARMS['C1']['gamma'] == '0.15' and ARMS['C2']['gamma'] == '0.05')
    chk('KE 창: A · B = 0 (감쇠를 안 바꾼다) · C1 · C2 = 8 덩어리',
        [ARMS[a]['comp_win'] for a in ('A', 'B', 'C1', 'C2')] == [0, 0, 8, 8]
        and 'variable comp_win equal 8' in decks['C2'] and 'variable comp_win equal 0' in decks['B'])
    chk('B 서보 vel_max = press_speed 0.01 (1저자 10-07)', 'variable servo_vmax index 0.01' in decks['B']
        and 'variable press_speed equal 0.01' in decks['B'])
    chk('B 서보 유지 감쇠 = 1e-5 (이완과 같다)', 'fix damp all viscous 1.0e-5' in dict(blocks_for('B'))['servo_switch'])
    # ⑮ ibb 래퍼 · 러너 짝 (1저자 10-08 "10 코어로" · CLAUDE.md 재개 체크리스트 ④: #SBATCH -n N ↔ mpirun --oversubscribe --bind-to none -np N)
    sb_path, rb_path = os.path.join(HERE, SBATCH), os.path.join(HERE, 'run_branch.sh')
    sb = open(sb_path, encoding='utf-8').read() if os.path.exists(sb_path) else ''
    rb = open(rb_path, encoding='utf-8').read() if os.path.exists(rb_path) else ''
    sbl = sb.splitlines()
    chk('⑮ ibb 래퍼가 있다', bool(sb), SBATCH)
    for want in ('#SBATCH --job-name=ps73B', '#SBATCH --output=logs/%x_%j.out', '#SBATCH --qos=cpu-60', '#SBATCH --partition=cpu',
                 f'#SBATCH -n {SBATCH_NP}', '#SBATCH --time=3-00:00:00', 'source ~/.bashrc', 'conda activate myenv',
                 f'NP={SBATCH_NP}', 'LMP=${LMP:-/lustre/home/yonghoon/LIGGGHTS-PUBLIC/src/lmp_mpi}',
                 'WORK_ROOT=${WORK_ROOT:-$HOME/ps73_branch_20261007_ibb}'):
        chk(f'⑮ 래퍼 줄: {want}', want in sbl)
    chk('⑮ #SBATCH -n 은 하나 · NP 와 같다', [ln for ln in sbl if ln.startswith('#SBATCH -n ')] == [f'#SBATCH -n {SBATCH_NP}'])
    chk('⑮ 래퍼가 SLURM_NTASKS = NP 를 대조하고 run_branch.sh 에 NP · LMP · WORK_ROOT 를 넘긴다',
        '"${SLURM_NTASKS:-}" != "$NP"' in sb and sb.count('WORK_ROOT="$WORK_ROOT" NP="$NP" LMP="$LMP" ALLOW_CONCURRENT=1') == 2)
    chk('⑮ 래퍼: SLURM 밖이면 사전 점검만 (--preflight-only)', 'run_branch.sh" --preflight-only' in sb)
    chk('⑮ 래퍼: 주소 · 포트 · 접속 명령 없음', not re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b|-P\s*\d{2,5}\b|\bssh\b|\bscp\b', sb))
    chk('⑮ 러너 mpirun 줄 = "$MPIRUN" $MPIRUN_FLAGS -np "$NP" · 기본 플래그 --oversubscribe --bind-to none',
        '"$MPIRUN" $MPIRUN_FLAGS -np "$NP" "$LMP"' in rb and 'MPIRUN_FLAGS=${MPIRUN_FLAGS:---oversubscribe --bind-to none}' in rb)
    m = re.search(r'for f in (in\.branch_t0_syntax\.liggghts.*?); do', rb, re.S)
    kit_list = set(m.group(1).replace('\\\n', ' ').split()) if m else set()
    chk('⑮ 러너의 kit 사본 목록 = SHA256SUMS 대상 + SHA256SUMS (빠지면 kit 의 sha256sum -c 가 런 직전에 멈춘다)',
        kit_list == set(SUMMED) | {SUMS}, sorted(kit_list ^ (set(SUMMED) | {SUMS})))
    chk("⑮ 러너 t0 점검이 MPI 프로세스 수 (Loop time … on N procs 의 N = NP) 를 본다", "awk -v np=\"$NP\" '$6 != np'" in rb)
    chk('⑮ 러너: --preflight-only 는 사전 점검 뒤 런 없이 끝난다', 'if [ "$PREFLIGHT_ONLY" = 1 ]; then' in rb
        and re.search(r'^preflight\nif \[ "\$PREFLIGHT_ONLY" = 1 \]; then\n.*\n  exit 0\nfi', rb, re.M) is not None)
    for p in (sb_path, rb_path):
        try:
            rc = subprocess.run(['bash', '-n', p], capture_output=True, text=True)
            chk(f'⑮ bash -n {os.path.basename(p)}', rc.returncode == 0, rc.stderr[:200])
        except FileNotFoundError:
            chk(f'⑮ bash -n {os.path.basename(p)} (bash 없음 — 건너뜀)', True)
    print(f'selftest: {"PASS" if not fails else "FAIL"} ({len(fails)} 실패)')
    return 1 if fails else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='ps73 감쇠 가지 실험 덱 생성기 (DEMP-01)')
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--check', action='store_true', help='커밋본 = 생성 결과 · SHA256SUMS 일치인지 (다르면 rc 1)')
    g.add_argument('--selftest', action='store_true', help='구조 검사 + r8 원 덱 부분열 대조')
    a = ap.parse_args(argv)
    if a.check:
        return check()
    if a.selftest:
        return selftest()
    write_all()
    return 0


if __name__ == '__main__':
    sys.exit(main())
