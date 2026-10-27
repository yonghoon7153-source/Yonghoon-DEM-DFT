#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SE 입도 · 해석 영역만 다른 압밀 덱 시리즈 (50kg/batch 과제 · 4차년도 조건) — 이종기술 6 mAh 덱 (`in.real_4`) 계열.

    python3 scripts/make_se_size_decks.py --preset kg50y4 --out <빈 폴더> \\
        --ibb-runner docs/data/pure_se_r075_20260927/run_pse_r075_a_r30.sh --ntasks kg50_d07_b40:56,kg50_d1_b40:20
    python3 scripts/make_se_size_decks.py --preset kg50y4 --fallback50 --out <빈 폴더>   # 40×40 불합격일 때만
    python3 scripts/make_se_size_decks.py --selftest

계기 (1저자 10-26 · `docs/50kg/dem_plan_20261026.md`):
  4차년도 조건 (활물질 85 wt% · 6.5 mAh/cm²) 에서 SE D50 0.7 · 1 · 2 · 3 µm 를 같은 조건으로 비교한다.
  활물질 = D6 단일 (반지름 3 µm · 1저자 *"D6으로 하면 될듯"* · *"활물질"*) · SE 진밀도 1.64 (랩 세대 `lab20261014`
  · 같은 세대의 NCM 4.85) · 시드 1 · 해석 영역 40 × 40 µm 은 D3 (가장 큰 SE) 로 50 × 50 과 먼저 비교 ·
  언로딩 없음 (1저자 — 빠르게).

★ 새로 만들지 않고 이미 돈 덱을 따른다 — 기준 = `docs/data/phase_a_6mah/in.real_4.liggghts` (sha256 고정).
  같은 계열에서 `make_ps_sweep_decks.py` 가 ps45 10:0 덱 (AM_S 가중 0) 을 찍었고, 그 덱이 ibb 에서 정확한 개수로
  삽입됐다 (원장 `PS-01`).  여기서 바꾸는 자리는 아래 목록뿐이고, 자리마다 **정확히 한 번** (판 꼭짓점은 네 줄)
  맞히지 못하면 덱을 내지 않는다 (반쯤 바뀐 덱이 최악이다).

바꾸는 것 (덱 머리에 같은 목록을 적는다):
  ① 조성 = 단일 활물질 (AM_P 자리 · `pts2` 는 정의만 남김) · 질량분율 AM 0.85 · SE 0.15
  ② 반지름 r_AM_P = 3 µm · r_SE = 0.35 · 0.5 · 1.0 · 1.5 µm
  ③ 진밀도 = 밀도 세대 (`additives.dens`) — AM 템플릿 둘 · SE 템플릿 하나
  ④ 해석 영역 x · y = 40 또는 50 µm — `reg_box` · `reg_mix` · 판 STL 꼭짓점 네 줄 · 압력 면적 두 곳 (0.0025 → 0.0016)
  ⑤ 삽입 영역 위끝 (reg_mix z1) — volumefraction 은 템플릿 값 그대로 두고 높이로 면용량을 맞춘다
     (고체 두께 = (L / C) / ρ_AM + (L / C)·(1−w)/w / ρ_SE · 높이 = 고체 두께 / volumefraction)
  ⑥ 시드 다섯 (템플릿 셋 · 분포 · 삽입) = 8 자리 소수 · 케이스마다 독립
  ⑦ 태그 `real_4` → 케이스명 (출력 폴더 · 판 STL · print) — 덱 머리 주석에도 기준 덱 파일 이름 · 태그를 쓰지 않는다
     (기준 덱 = sha256 전체 · 폴더 · 경로 전체는 manifest.json · 10-27 ibb `dem_restart.py` 가 v2 덱을 머리 주석 두 줄 때문에
     "다른 케이스명 혼입: ['real_4']" 로 거부) · build 가 생성 파일 어느 줄에든 (주석 포함) 다른 케이스명이 있으면 쓰지 않고 멈춘다
  ⑧ `maxattempt` = int32 상한 아래 (`ninsert_this_local × maxattempt` 가 int 곱셈 · 1 proc 최악 · 여유 1.3 · 원장 `PS-01`)
  ⑨ `processors * * 1` (x · y 분할 · `PS-01` 둘째 원인 · a6 · hit 재개 스크립트와 같은 분할)
  ⑩ 삽입 자기검사 (`count(all)` < 99 % 면 `quit 1` · `make_ps_sweep_decks.insert_gate` 그대로)
  ⑪ 압축 체크포인트 `restart 200000 restart_<case>/restart_compress_*.bin` (`fix move_press` 바로 뒤 — LHS 계열 덱 ·
     heckel 덱과 같은 자리) — 1저자 ibb `a6_resume.sh` · hit `hit_resume.sh` 가 압축 · 이완 중간에서 코어를 바꿔
     이어받으려면 이 줄이 있어야 한다 (원 `in.real_4` 에는 없다 → 압축 중 체크포인트 이름이 `restart_settling_*` 로 남는다)
     · 간격 200,000 (1저자 10-26 Q4 권고대로 — 50,000 이면 D0.7 파일 ≈ 120 개 · 15–19 GB)
  ⑫ atom 덤프 간격 50,000 (1저자 10-26 Q3 · 템플릿 5,000 이면 D0.7-40 ≈ 60 GB · 압축 곡선 = mesh 덤프 + thermo)
  ⑬ 삽입 직후 (step 1) `write_restart restart_<case>/restart_settling_1.bin` — 모든 덱 (1저자 10-26 Q1)
     + 삽입 전용 덱 `input_<case>_insert.liggghts` = 본 덱의 ⑬ 줄까지 그대로 + `run 2000` (끝) — NP 1 로 돌려
     상별 수를 계획대로 넣고, `resume_ckpt.sh` (settling 모드 · G1–G3 시험) 로 코어를 늘려 이어받는다
  ⑭ 삽입 직후 활물질 수 검사 — 계획 ±0.5 % 밖이면 `quit 1` (SELF-70 = 소수 상이 랭크마다 잘려 체계적으로 부족)
  ⑮ (속도 시험 덱만) 이웃 skin — 템플릿 0.002 (= 2 µm) · 0.0005 (= 0.5 µm) 둘을 같은 시드 · 같은 코어로 짧게
     (1저자 10-26 Q2 — 결과 = 시간만 · 구조 쓰지 않음 · 본 덱은 skin 그대로)
  케이스 = 40×40 본 비교 넷 (시드 슬롯 0–3) + D3 칸 비교 (50×50 시드 1 · 40 · 50 시드 2 · 3 · Q5) · 50×50 의
  D0.7 · D1 · D2 는 `--fallback50` 으로만 (40×40 불합격 때 · D0.7-50 은 1저자 10-26 철회)

바꾸지 않는 것: 재료 (property/global 전부 — E_SE 0.135e7 = 1.35 GPa 연화값 포함) · 접촉법칙 · dt · 이웃 목록 ·
  바닥 벽 · 중력 · 감쇠 · 정착 200,000 · 안정화 200,000 · 판 속도 0.01 · 목표 0.30 (= 300 MPa) · 압축 판정 루프 ·
  이완 100,000 · 접촉 덤프 · mesh 덤프 · volumefraction.
  ⚠ 소성 깊이 행렬에도 `0.05` 가 있다 (68–69 줄) — ④ 는 정해진 자리만 바꾸고, 재료 블록은 바이트 그대로인지 시험한다.

⚠ 상별 입자 수: 총수는 정확하고, 상별 수는 MPI 랭크마다 템플릿 절삭 · 분배가 갈라져 ±(템플릿 수 − 1)·NP 흔들린다
  (원장 `SELF-70` · Codex 10 차 Q4 = 이 덱 계열 한정 동의).  여기는 템플릿 2 → 활물질 ±NP.  덱 머리에 적고, 런 뒤
  덤프에서 실현 조성 (wt% · 면용량) 을 다시 센다.
⚠ 계산량 · 시간은 **추정**이다 (기준 = lhs00_000 · 45,030 입자 · 2.42 M step · 43 h · 1 코어).
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import additives as ADD            # noqa: E402  (밀도 세대 정본 — dens · dens_record)
import make_ps_sweep_decks as PS    # noqa: E402  (read_deck · compose · predict_counts · insert_gate · 규약 상수)

TEMPLATE = os.path.join(ROOT, 'docs', 'data', 'phase_a_6mah', 'in.real_4.liggghts')
TEMPLATE_SHA256 = '900ae9c8f1fde02e83ac86dcee7cca55a10df9ac73e59f15a1ae1516903bfda7'
TAG_OLD = 'real_4'
UM_PER_SIM = 1000.0                 # 덱 길이 × 1000 = µm (Scale r×1000)

#: 50kg/batch 4차년도 — 1저자 10-26 결정 (`docs/50kg/dem_plan_20261026.md` §4 · 이 커밋의 기록)
PRESET_KG50Y4 = dict(
    r_am_um=3.0,                    # 활물질 D6 단일
    am_mass=0.85,                   # 킥오프 4 장 4차년도
    loading_mah_cm2=6.5,            # 킥오프 4 장 4차년도
    cap_mah_g=200.0,                # 랩 표준 비용량 (1저자 10-08 Q3 · network_current.py)
    dens_gen='lab20261014',         # SE 1.64 · NCM 4.85 (1저자 10-14 · 10-26 *"확정된 1.64"*)
    maxattempt=3000,                # D0.7 · 50 µm (예상 ≈ 49 만 개) 가 int32 상한 3,38x 아래 — 모든 덱 같은 값
    atom_dump_every=50000,          # ⑫ 1저자 10-26 Q3 권고대로
    compress_restart_every=200000,  # ⑪ 1저자 10-26 Q4 권고대로
    insert_restart=False,           # ⑬ 본 덱에는 step 1 체크포인트 없음 (10-26 밤 Q1 — 삽입 전용 덱만 · KG50-10)
    am_gate_tol=0.005,              # ⑭ 삽입 직후 활물질 수 ±0.5 % (정수 구간 = ceil · floor · KG50-08)
    se_gate_tol=0.005,              # ⑭ 삽입 직후 SE 수 ±0.5 % (KG50-13)
    end_frames=True,                # ⑯ 끝 step 의 restart · atom · contact · mesh + 이완 중 체크포인트 끔 (KG50-03 · 11)
    insert_settle_steps=20000,      # ⑬ 삽입 전용 덱 = 정착 20,000 step 뒤 restart_settling_20001 (첫 바닥 접촉 ≈ 3,500 뒤)
    insert_tail_steps=3000,         # ⑬ 그 뒤 3,000 step = 재개 시험 G3 의 비교 줄 (21,000 · 22,000 · 23,000)
    #: 삽입 전용 덱을 만드는 케이스 (NP 1 삽입 → 코어 늘려 재개) — D3 칸 비교는 처음부터 끝까지 NP 1 (재개 없음)
    insert_cases=('kg50_d07_b40', 'kg50_d1_b40', 'kg50_d2_b40', 'kg50_d07_b50', 'kg50_d1_b50', 'kg50_d2_b50'),
    #: (케이스, r_SE µm, 영역 µm, 시드 슬롯) — 슬롯이 시드를 정한다 (바꾸면 다른 침대)
    cases=[('kg50_d07_b40', 0.35, 40, 0), ('kg50_d1_b40', 0.5, 40, 1), ('kg50_d2_b40', 1.0, 40, 2),
           ('kg50_d3_b40_s1', 1.5, 40, 3),
           ('kg50_d3_b50_s1', 1.5, 50, 4),                                # 칸 비교 시드 1 짝 (이름 _s1 · KG50-14)
           ('kg50_d3_b40_s2', 1.5, 40, 5), ('kg50_d3_b40_s3', 1.5, 40, 6),
           ('kg50_d3_b50_s2', 1.5, 50, 7), ('kg50_d3_b50_s3', 1.5, 50, 8)],
    #: 40×40 이 D3 칸 비교에서 불합격일 때만 (`--fallback50`) — D0.7-50 은 1저자 10-26 철회 (미리 돌리지 않는다)
    fallback50=[('kg50_d07_b50', 0.35, 50, 9), ('kg50_d1_b50', 0.5, 50, 10), ('kg50_d2_b50', 1.0, 50, 11)],
)

#: 시드 — make_ps_sweep 의 20M–53M 대역 · LHS 의 5 자리와 겹치지 않는 8 자리 대역.  바꾸면 다른 침대가 된다.
#: 슬롯 16 개 (0–15) → 최대 ≈ 18.9 M · 한 슬롯 안 다섯 시드 간격 100,000 < 슬롯 간격 500,000 (겹침 없음)
SEED_BASE, SEED_STEP, SEED_SUB = 11_000_000, 500_000, 100_000
DECK_KW = ('r_am_um', 'am_mass', 'loading_mah_cm2', 'cap_mah_g', 'dens_gen', 'maxattempt', 'atom_dump_every',
           'compress_restart_every', 'insert_restart', 'am_gate_tol', 'se_gate_tol', 'end_frames')

RE_REGION = re.compile(r'^([ \t]*region[ \t]+(reg_box|reg_mix)[ \t]+block)((?:[ \t]+\S+){6})([ \t]+units[ \t]+box[ \t]*)$', re.M)
RE_VERTEX = re.compile(r'^([ \t]*print[ \t]+"vertex[ \t]+)(\S+)([ \t]+)(\S+)([ \t]+\$\{plate_z\}".*)$', re.M)
RE_AREA = re.compile(r'(abs\(f_top_mesh\[3\]\)[ \t]*/[ \t]*)([0-9.eE+-]+)([ \t]*/[ \t]*1000000)')
RE_MOVE = re.compile(r'^[ \t]*fix[ \t]+move_press[ \t]+all[ \t]+move/mesh[^\n]*$', re.M)
RE_LOOP = re.compile(r'^[ \t]*label[ \t]+loop_press[ \t]*$', re.M)
RE_DUMP_ATOM = re.compile(r'^([ \t]*dump[ \t]+dmp_atom[ \t]+all[ \t]+custom[ \t]+)(\d+)(\s)', re.M)
RE_NEIGHBOR = re.compile(r'^([ \t]*neighbor[ \t]+)([0-9.eE+-]+)([ \t]+bin[ \t]*)$', re.M)
RE_PROPERTY = re.compile(r'^[ \t]*fix[ \t]+m\d+[ \t]+all[ \t]+property/global.*?(?=^[ \t]*fix[ \t]+m\d+|^#[ \t]*---)', re.M | re.S)


def _die(msg):
    raise SystemExit('⛔ ' + msg)


def _fmt_sim(v: float) -> str:
    """덱 길이 표기 — 0.05 · 0.04 · 0.32270 처럼 짧게 (불필요한 0 없음)."""
    s = f'{v:.6f}'.rstrip('0').rstrip('.')
    return s if s not in ('', '-0') else '0'


def seeds_for(idx: int, n: int = 5):
    if not (0 <= int(idx) <= 15) or n > 5:
        _die(f'시드 슬롯 {idx} — 0..15 (16 이상이면 ps45 시드 대역 20M+ 을 침범한다)')
    return [PS.next_prime(SEED_BASE + idx * SEED_STEP + j * SEED_SUB) for j in range(n)]


def solid_thickness_um(loading, cap, w_am, rho_am, rho_se):
    """면용량 → 영 기공 고체 두께 (µm).  AM 면적질량 = L/C (g/cm²) · SE = AM·(1−w)/w."""
    m_am = loading / cap
    m_se = m_am * (1.0 - w_am) / w_am
    return (m_am / rho_am + m_se / rho_se) * 1e4


def material_block(text: str) -> str:
    """재료 property/global 블록 전체 (m1–m9) — 바이트 그대로여야 한다."""
    a = text.find('fix m1 all property/global')
    b = text.find('# --- 4. Contact Model')
    if a < 0 or b < 0 or b <= a:
        _die('재료 블록 (fix m1 … # --- 4.) 을 못 찾았다 — 템플릿 구조가 바뀌었다')
    return text[a:b]


def _sub_exact(text, pattern, repl, n_expect, what, flags=re.M):
    new, n = re.subn(pattern, repl, text, flags=flags)
    if n != n_expect:
        _die(f'{what}: {n} 곳을 맞혔다 (기대 {n_expect}) — 템플릿 구조가 바뀌었다')
    return new


def int_band(n_plan: int, tol) -> tuple:
    """계획 수 ±tol 안의 정수 구간 (lower = ceil · upper = floor · 정수 산술 — KG50-08)."""
    tp = round(float(tol) * 1_000_000)
    if not (0 < tp < 50_000) or int(n_plan) <= 0:
        _die(f'개수 검사 허용폭 {tol} — (0, 0.05) · 계획 수 {n_plan}')
    n = int(n_plan)
    lo = -((-n * (1_000_000 - tp)) // 1_000_000)
    hi = (n * (1_000_000 + tp)) // 1_000_000
    if not (lo <= n <= hi):
        _die(f'정수 구간 {lo}–{hi} 이 계획 {n} 을 안 품는다')
    return lo, hi


def make_deck(text: str, case: str, r_se_um: float, box_um: float, idx: int, *, r_am_um, am_mass,
              loading_mah_cm2, cap_mah_g, dens_gen, maxattempt, atom_dump_every=None, insert_restart=False,
              compress_restart_every=50000, am_gate_tol=None, skin_um=None, se_gate_tol=None, end_frames=False):
    """템플릿 → 덱 한 장.  돌려주는 것 = (덱 텍스트, 기록 dict)."""
    if TAG_OLD not in text:
        _die(f'템플릿에 태그 {TAG_OLD} 가 없다')
    if not (0 < r_se_um < r_am_um):
        _die(f'r_SE {r_se_um} µm 는 (0, r_AM {r_am_um}) 밖')
    if not (10 <= box_um <= 200):
        _die(f'영역 {box_um} µm 는 10–200 밖')
    dens = ADD.dens(dens_gen)
    rho_am, rho_se = dens['AM'], dens['SE']
    tpl, ent = PS.read_deck(text)
    by_type = {v['atype']: k for k, v in tpl.items()}
    if set(by_type) != {1, 2, 3}:
        _die(f'atom_type 구성이 1=AM_P · 2=AM_S · 3=SE 가 아니다: {sorted(by_type)}')
    mat0 = material_block(text)
    out = text

    # ── ② 반지름 ──
    for var, um in (('r_AM_P', r_am_um), ('r_SE', r_se_um)):
        rx = re.compile(PS.RE_VAR.pattern.format(var), re.M)
        if len(rx.findall(out)) != 1:
            _die(f'variable {var} 줄이 정확히 하나가 아니다')
        out = rx.sub(lambda m, um=um, var=var: (f'{m.group(1)}{um:g}e-3'
                                                 f'            # {var[2:]} r={um:g}μm → Sim {um:g}mm'), out, count=1)

    # ── ③ 진밀도 (템플릿 줄의 density constant) ──
    def _dens_line(m):
        line = m.group(0)
        atype = int(m.group(5))
        rho = rho_se if atype == 3 else rho_am
        return re.sub(r'(density\s+constant\s+)[0-9.eE+-]+', lambda d: f'{d.group(1)}{int(round(rho * 1000))}', line, count=1)
    n_pts = len(PS.RE_PTS.findall(out))
    if n_pts != 3:
        _die(f'particletemplate/sphere 줄 {n_pts} (기대 3)')
    out = PS.RE_PTS.sub(_dens_line, out)

    # ── ④ 해석 영역 · ⑤ 삽입 높이 ──
    box = box_um / UM_PER_SIM
    vf_m = PS.RE_VF.search(out)
    if not vf_m:
        _die('volumefraction_region 을 못 찾았다')
    vf = float(vf_m.group(1))
    t_solid_um = solid_thickness_um(loading_mah_cm2, cap_mah_g, am_mass, rho_am, rho_se)
    regs = {m.group(2): m for m in RE_REGION.finditer(out)}
    if set(regs) != {'reg_box', 'reg_mix'} or len(RE_REGION.findall(out)) != 2:
        _die('region reg_box · reg_mix block 줄이 각각 정확히 하나가 아니다')
    z0_mix = float(regs['reg_mix'].group(3).split()[4])
    z_top = z0_mix + (t_solid_um / UM_PER_SIM) / vf
    z_box = float(regs['reg_box'].group(3).split()[5])
    if z_top > 0.9 * z_box:
        _die(f'삽입 위끝 {z_top:.4f} 이 상자 위끝 {z_box} 의 90 % 를 넘는다')

    def _region(m):
        v = m.group(3).split()
        v[1] = v[3] = _fmt_sim(box)
        if m.group(2) == 'reg_mix':
            v[5] = f'{z_top:.6f}'
        return m.group(1) + ' ' + ' '.join(v) + m.group(4)
    out = RE_REGION.sub(_region, out)
    old_box = None
    vert = RE_VERTEX.findall(out)
    if len(vert) != 6:
        _die(f'판 STL vertex print 줄 {len(vert)} (기대 6)')
    toks = [t for v in vert for t in (v[1], v[3]) if t not in ('0.0', '0')]
    if len(toks) != 6 or len(set(toks)) != 1:
        _die(f'판 꼭짓점의 0 아닌 좌표가 한 값 여섯 자리가 아니다: {toks}')
    old_box = toks[0]

    def _vertex(m):
        x = _fmt_sim(box) if m.group(2) == old_box else m.group(2)
        y = _fmt_sim(box) if m.group(4) == old_box else m.group(4)
        return f'{m.group(1)}{x}{m.group(3)}{y}{m.group(5)}'
    out = RE_VERTEX.sub(_vertex, out)
    area = box * box
    out = _sub_exact(out, RE_AREA.pattern, lambda m: f'{m.group(1)}{_fmt_sim(area)}{m.group(3)}', 2, '압력 면적 식')

    # ── ⑥ 시드 · ① 조성 ──
    seeds = seeds_for(idx)
    it = iter(seeds)
    out = PS.RE_PTS.sub(lambda m: f'{m.group(1)}{next(it)}{m.group(4)}', out)
    pdd_seed, ins_seed = next(it), next(it)
    fr = PS.compose(1, 0, am_mass)                          # P:S = 1:0 → AM_P 만
    want = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
    keep = [(n, fr[want[tpl[n]['atype']]]) for n, _ in ent if fr[want[tpl[n]['atype']]] > 0]
    body = ' '.join(f'{n} {PS.fmt_frac(f)}' for n, f in keep)
    if len(PS.RE_PDD.findall(out)) != 1:
        _die('particledistribution/discrete 줄이 정확히 하나가 아니다')
    out = PS.RE_PDD.sub(lambda m: f'{m.group(1)}{pdd_seed} {len(keep)} {body}', out, count=1)
    if len(PS.RE_INS.findall(out)) != 1:
        _die('insert/pack 줄이 정확히 하나가 아니다')
    out = PS.RE_INS.sub(lambda m: f'{m.group(1)}{ins_seed}{m.group(3)}', out, count=1)
    drop = [n for n, _ in ent if n not in dict(keep)]
    for n in drop:
        out = _sub_exact(out, rf'^(\s*fix\s+{re.escape(n)}\s+all\s+particletemplate/sphere.*)$',
                         lambda m: f'{m.group(1)}   # (이 케이스 질량분율 0 — 분포에서 제외)', 1, f'{n} 표지')

    # ── ⑦ 태그 ──
    n_tag_lo, n_tag_up = out.count(TAG_OLD), out.count(TAG_OLD.upper())       # 머리 ⑦ 줄에 적는다 (태그 이름은 안 적는다)
    out = out.replace(TAG_OLD, case).replace(TAG_OLD.upper(), case.upper())
    if TAG_OLD in out or TAG_OLD.upper() in out:
        _die('태그가 남았다')

    # ── ⑨ processors · ⑧ maxattempt (int32) ──
    if re.search(r'^[ \t]*processors\s', out, re.M):
        _die('템플릿에 processors 줄이 이미 있다 — 이 생성기의 가정과 다르다')
    m_rb = PS.RE_REGBOX.search(out)
    if not m_rb:
        _die('region reg_box 를 못 찾아 processors 줄을 넣을 자리가 없다')
    out = out[:m_rb.start()] + PS.PROC_GRID + '\n' + out[m_rb.start():]
    radii = {'r_AM_P': r_am_um / UM_PER_SIM, 'r_AM_S': None, 'r_SE': r_se_um / UM_PER_SIM}
    rs = re.compile(PS.RE_VAR.pattern.format('r_AM_S'), re.M).search(out)
    radii['r_AM_S'] = float(rs.group(2)) if rs else 0.0
    tpl2, _ = PS.read_deck(out)
    cnt = PS.predict_counts(out, tpl2, keep, radii)
    n_tot = sum(cnt.values())
    if n_tot <= 0:
        _die('예상 입자 수를 못 냈다')
    att = int(maxattempt)
    if n_tot * att * PS.MAXATT_INT32_MARGIN >= PS.INT32_MAX:
        _die(f'maxattempt {att:,} × 예상 {n_tot:,} × 여유 {PS.MAXATT_INT32_MARGIN:g} ≥ 2^31 — '
             f'{int(PS.INT32_MAX / (n_tot * PS.MAXATT_INT32_MARGIN)):,} 이하로 (원장 PS-01)')
    m_old = PS.RE_MAXATT.search(out)
    if not m_old or len(PS.RE_MAXATT.findall(out)) != 1:
        _die('maxattempt 가 정확히 하나가 아니다')
    att_old = int(m_old.group(2))
    out = PS.RE_MAXATT.sub(lambda m: f'{m.group(1)}{att}', out, count=1)

    # ── ⑩ 삽입 자기검사 ──
    m_un = PS.RE_UNFIX_INS.search(out)
    if not m_un:
        _die('unfix ins_mix 를 못 찾았다')
    n_am_plan = cnt.get('pts1', 0)
    n_se_plan = cnt.get('pts3', 0)
    am_gate = se_gate = None
    gate_txt = PS.insert_gate(n_tot)
    for tag, grp, atype, n_plan, tol_in in (('AM', 'g_am_ins', 1, n_am_plan, am_gate_tol),
                                            ('SE', 'g_se_ins', 3, n_se_plan, se_gate_tol)):
        if tol_in is None:
            continue
        lo, hi = int_band(n_plan, tol_in)
        if tag == 'AM':
            am_gate = (lo, hi)
        else:
            se_gate = (lo, hi)
        var = 'n_am_ins' if tag == 'AM' else 'n_se_ins'
        gate_txt += (f'\n# ⑭ 삽입 직후 {tag} 수 — 계획 {n_plan:,} · 정수 구간 {lo}–{hi} (±{float(tol_in) * 100:g} % 안 · ceil/floor) · '
                     f'상별 수는 MPI 랭크 · 시드에 따라 흔들린다 (부족 또는 초과 · SELF-70 · KG50-07) → 삽입은 NP 1\n'
                     f'group {grp} type {atype}\n'
                     f'variable {var} equal count({grp})\n'
                     f'print "====== {tag} ${{{var}}} / {n_plan} (gate {lo}-{hi}) ======"\n'
                     f'if "${{{var}}} < {lo} || ${{{var}}} > {hi}" then &\n'
                     f'    "print \'FATAL: {tag} count off plan (SELF-70) - insert at NP 1. aborting.\'" &\n'
                     f'    "quit 1"\n')
    out = out[:m_un.end()] + gate_txt + out[m_un.end():]

    # ── ⑪ 압축 체크포인트 ──
    mv = list(RE_MOVE.finditer(out))
    if len(mv) != 1 or not RE_LOOP.search(out) or RE_LOOP.search(out).start() < mv[0].end():
        _die('fix move_press 줄 (하나) 과 그 뒤 label loop_press 를 못 찾았다')
    if 'restart_compress' in out:
        _die('템플릿에 이미 restart_compress 가 있다 — 이 생성기의 가정과 다르다')
    cre = int(compress_restart_every)
    if cre <= 0 or cre % 50000 != 0:
        _die('압축 체크포인트 간격은 50,000 의 배수 (정착 체크포인트와 같은 격자)')
    rc = f'restart {cre} restart_{case}/restart_compress_*.bin'
    out = out[:mv[0].end()] + '\n' + rc + out[mv[0].end():]

    # ── ⑫ atom 덤프 간격 (선택) ──
    md = list(RE_DUMP_ATOM.finditer(out))
    if len(md) != 1:
        _die('dump dmp_atom 줄이 정확히 하나가 아니다')
    dump_old = int(md[0].group(2))
    if atom_dump_every:
        n = int(atom_dump_every)
        if n <= 0 or n % 10000 != 0:
            _die('--atom-dump-every 는 접촉 덤프 간격 10,000 의 배수여야 한다 (같은 step 에 atom · contact)')
        out = RE_DUMP_ATOM.sub(lambda m: f'{m.group(1)}{n}{m.group(3)}', out, count=1)

    # ── ⑬ (선택) 삽입 직후 체크포인트 — NP 1 로 삽입만 하고 재개 스크립트로 코어를 바꾸는 길 (상별 수 = 계획) ──
    ir = f'write_restart restart_{case}/restart_settling_1.bin'
    if insert_restart:
        rx = re.compile(rf'^(restart 50000 restart_{re.escape(case)}/restart_settling_\*\.bin)$', re.M)
        if len(rx.findall(out)) != 1:
            _die('Phase 1 의 restart … restart_settling_*.bin 줄이 정확히 하나가 아니다')
        out = rx.sub(lambda m: m.group(1) + '\n' + ir + '   # 삽입 직후 (step 1) — 재개 스크립트의 settling 모드 = 남은 200,000', out, count=1)

    # ── ⑯ 끝 상태 · 이완 중 체크포인트 (KG50-03 · 11) ──
    if end_frames:
        m_um = re.search(r'^unfix[ \t]+move_press[ \t]*$', out, re.M)
        if not m_um or len(re.findall(r'^unfix[ \t]+move_press[ \t]*$', out, re.M)) != 1:
            _die('unfix move_press 줄이 정확히 하나가 아니다')
        out = (out[:m_um.end()] + '\nrestart 0   # ⑯ 이완 중 체크포인트 끔 (이름이 restart_compress_* 라 재개하면 압축을 다시 탄다 · KG50-11)'
               + out[m_um.end():])
        da = re.search(r'^dump[ \t]+dmp_atom[ \t]+all[ \t]+custom[ \t]+\d+[ \t]+(\S+)atom_\*\.liggghts(.*)$', out, re.M)
        dc = re.search(r'^dump[ \t]+dmp_contact[ \t]+all[ \t]+local[ \t]+\d+[ \t]+(\S+)contact_\*\.liggghts[ \t]*&\n((?:[ \t]+.*&\n)*[ \t]+.*)$', out, re.M)
        dm = re.search(r'^dump[ \t]+dmp_mesh[ \t]+all[ \t]+mesh/stl[ \t]+\d+[ \t]+(\S+)mesh_\*\.stl[ \t]+(\S+)[ \t]*$', out, re.M)
        fin = list(re.finditer(r'^print "====== Simulation Finished!.*$', out, re.M))
        if not (da and dc and dm) or len(fin) != 1:
            _die('끝 상태 출력을 만들 dmp_atom · dmp_contact · dmp_mesh · Finished 줄을 못 찾았다')
        cols = dc.group(2)
        end_blk = ('# ⑯ 끝 상태 (마지막 step) — 최종 restart 먼저 · atom · contact · mesh 한 장씩 (출력만 · 물리 같음 · KG50-03)\n'
                   f'write_restart restart_{case}/restart_end.bin\n'
                   f'dump dmp_atom_end all custom 1 {da.group(1)}atom_end_*.liggghts{da.group(2)}\n'
                   f'dump dmp_contact_end all local 1 {dc.group(1)}contact_end_*.liggghts &\n{cols}\n'
                   f'dump dmp_mesh_end all mesh/stl 1 {dm.group(1)}mesh_end_*.stl {dm.group(2)}\n'
                   'run 0\n'
                   'undump dmp_atom_end\n'
                   'undump dmp_contact_end\n'
                   'undump dmp_mesh_end\n')
        out = out[:fin[0].start()] + end_blk + out[fin[0].start():]

    # ── ⑮ 이웃 skin (본 덱 = 템플릿 그대로 · 1저자 10-26 밤 Q3 (나)) ──
    mn = list(RE_NEIGHBOR.finditer(out))
    if len(mn) != 1:
        _die('neighbor … bin 줄이 정확히 하나가 아니다')
    skin_old = float(mn[0].group(2)) * UM_PER_SIM
    if skin_um is not None:
        if not (0.05 <= float(skin_um) <= 5.0):
            _die(f'skin {skin_um} µm — 0.05..5')
        out = RE_NEIGHBOR.sub(lambda m: f'{m.group(1)}{_fmt_sim(float(skin_um) / UM_PER_SIM)}{m.group(3)}', out, count=1)

    # ── 주석 · print 의 조성 표기 (거짓말하지 않게) ──
    desc = (f'mono AM D{2 * r_am_um:g}, AM:SE={am_mass * 100:g}:{(1 - am_mass) * 100:g} wt%, '
            f'SE D50 {2 * r_se_um:g}um, {loading_mah_cm2:g}mAh/cm2, {box_um:g}x{box_um:g}um')
    out = _sub_exact(out, r'^print "====== INSERTING PARTICLES \(.*\) =====.*$',
                     f'print "====== INSERTING PARTICLES ({case.upper()}: {desc}) ====="', 1, 'INSERTING print')
    out = _sub_exact(out, r'^print "====== Simulation Finished! \(.*\) ======"$',
                     f'print "====== Simulation Finished! ({case.upper()}: {desc}) ======"', 1, 'Finished print')
    out = re.sub(r'^#\s*질량비:.*$', '# 질량비: ' + ', '.join(f'{want[tpl[n]["atype"]]}:{PS.fmt_frac(f)}' for n, f in keep),
                 out, count=1, flags=re.M)
    #   옛 머리 블록 (Real Condition 4 · 바이모달 · 6 mAh · RVE 50) 은 지우고 새 머리로 갈음한다
    a = out.find('# Real Condition 4')
    b = out.find('# ============================================================', a)
    if a < 0 or b < 0:
        _die('템플릿 머리 블록을 못 찾았다')
    out = (out[:a] + f'# {case}: SE 입도 비교 (50kg/batch 4차년도 · make_se_size_decks.py)\n'
           + '# Scale: r×1000, E×0.001, P×0.001\n' + out[b:])
    for old, new in (('# RVE: 50×50 μm → Sim 0.05×0.05 m', f'# RVE: {box_um:g}×{box_um:g} μm → Sim {_fmt_sim(box)}×{_fmt_sim(box)} m'),
                     ('# 동적 plate STL (RVE 50×50 μm → Sim 0.05×0.05 m)',
                      f'# 동적 plate STL (RVE {box_um:g}×{box_um:g} μm → Sim {_fmt_sim(box)}×{_fmt_sim(box)} m)'),
                     ('# RVE 면적: 0.05 × 0.05 = 0.0025 m²',
                      f'# RVE 면적: {_fmt_sim(box)} × {_fmt_sim(box)} = {_fmt_sim(area)} m²'),
                     ('# Type 1: AM_P (NCM811, ρ=4800 kg/m³, r=6μm)',
                      f'# Type 1: AM   (NCM811, ρ={int(round(rho_am * 1000))} kg/m³, r={r_am_um:g}μm) — 단일 활물질'),
                     ('# Type 2: AM_S (NCM811, ρ=4800 kg/m³, r=2μm)',
                      f'# Type 2: AM_S (정의만 · 분포 가중 0 · ρ={int(round(rho_am * 1000))} kg/m³)'),
                     ('# Type 3: SE   (LPSCl,  ρ=2000 kg/m³, r=0.5μm)',
                      f'# Type 3: SE   (LPSCl,  ρ={int(round(rho_se * 1000))} kg/m³, r={r_se_um:g}μm)')):
        if out.count(old) != 1:
            _die(f'주석 줄을 정확히 한 번 못 찾았다: {old}')
        out = out.replace(old, new)

    if material_block(out) != mat0:
        _die('재료 블록이 바뀌었다 — 치환이 정해진 자리 밖을 건드렸다')

    # ── 기록 · 머리 ──
    v_am = 4.0 / 3.0 * math.pi * r_am_um ** 3
    n_am = cnt.get('pts1', 0)
    area_cm2 = (box_um * 1e-4) ** 2
    load_pred = n_am * v_am * 1e-12 * rho_am / area_cm2 * cap_mah_g
    rec = dict(case=case, r_am_um=r_am_um, r_se_um=r_se_um, d50_se_um=2 * r_se_um, box_um=box_um,
               am_mass=am_mass, loading_target_mah_cm2=loading_mah_cm2, cap_mah_g=cap_mah_g,
               loading_pred_mah_cm2=round(load_pred, 4), solid_thickness_um=round(t_solid_um, 4),
               volumefraction=vf, reg_mix_z_top=round(z_top, 6), insert_height_um=round((z_top - z0_mix) * UM_PER_SIM, 3),
               counts_pred={want[tpl[n]['atype']]: cnt.get(n, 0) for n, _ in keep}, n_total_pred=n_tot,
               maxattempt=att, maxattempt_template=att_old, int32_product=n_tot * att,
               seeds=seeds, atom_dump_every=int(atom_dump_every) if atom_dump_every else dump_old,
               atom_dump_every_template=dump_old, insert_restart=bool(insert_restart), area_sim=area,
               compress_restart_every=cre, am_gate=list(am_gate) if am_gate else None, n_am_plan=n_am_plan,
               se_gate=list(se_gate) if se_gate else None, n_se_plan=n_se_plan, end_frames=bool(end_frames),
               skin_um=float(skin_um) if skin_um is not None else skin_old, skin_um_template=skin_old,
               **ADD.dens_record(dens_gen))
    #   머리 주석에 기준 덱 파일 이름 · 태그를 쓰지 않는다 — ibb dem_restart.py 가 덱 어느 줄에든 (주석 포함) 다른
    #   케이스명이 있으면 재개 계획을 내지 않는다 (10-27 "다른 케이스명 혼입: ['real_4']").  기준 덱 신원 = 실제로 바꾼
    #   텍스트의 sha256 전체 + 폴더 (경로 전체는 manifest.json "template").
    tpl_sha = hashlib.sha256(text.encode('utf-8')).hexdigest()
    tpl_dir = os.path.relpath(os.path.dirname(TEMPLATE), ROOT).replace(os.sep, '/')
    tpl_desc = (f'phase_a 6 mAh 템플릿 ({tpl_dir}/ · sha256 {tpl_sha} · 파일 경로 = manifest.json "template")'
                if tpl_sha == TEMPLATE_SHA256 else f'고정 템플릿과 다른 텍스트 (sha256 {tpl_sha})')
    head = [
        '# ===== SE 입도 비교 생성본 (make_se_size_decks.py · 50kg/batch 4차년도) =====',
        f'#   {case}: {desc}',
        f'#   기준 덱 = {tpl_desc} — 바꾼 자리 = 아래뿐',
        f'#   ① 조성 단일 활물질 (AM_P 자리 · pts2 정의만) · 질량분율 AM {PS.fmt_frac(am_mass)} · SE {PS.fmt_frac(1 - am_mass)}',
        f'#   ② r_AM_P {r_am_um:g} µm · r_SE {r_se_um:g} µm   ③ 진밀도 세대 {dens_gen}: AM {rho_am:g} · SE {rho_se:g} g/cm³',
        f'#   ④ 영역 {box_um:g}×{box_um:g} µm (reg_box · reg_mix · 판 꼭짓점 · 압력 면적 {_fmt_sim(area)})',
        f'#   ⑤ 삽입 위끝 z {z_top:.6f} (높이 {(z_top - z0_mix) * UM_PER_SIM:.1f} µm · volumefraction {vf:g} 그대로) '
        f'= 고체 두께 {t_solid_um:.2f} µm = {loading_mah_cm2:g} mAh/cm² @ {cap_mah_g:g} mAh/g',
        '#   ⑥ 시드 (큰 소수 · 케이스마다 독립): ' + ', '.join(str(s) for s in seeds),
        f'#   ⑦ 태그 = 기준 덱의 케이스 태그 (소문자 {n_tag_lo} 곳 · 대문자 {n_tag_up} 곳) → {case} · {case.upper()}'
        f'   ⑧ maxattempt {att_old:,} → {att:,} (예상 {n_tot:,} × {att:,} = '
        f'{n_tot * att:.3g} < 2^31/1.3 · 원장 PS-01)',
        f'#   ⑨ {PS.PROC_GRID} (x·y 분할)   ⑩ 삽입 자기검사 (99 %)   ⑪ {rc} (간격 {cre:,})',
        (f'#   ⑫ atom 덤프 간격 {dump_old:,} → {int(atom_dump_every):,}' if atom_dump_every
         else f'#   ⑫ atom 덤프 간격 그대로 ({dump_old:,})'),
        (f'#   ⑬ 삽입 직후 체크포인트 {ir} (NP 1 삽입 → 재개 스크립트로 코어 변경)' if insert_restart
         else '#   ⑬ 삽입 직후 체크포인트 없음 (첫 체크포인트 = step 50,000)'),
        (f'#   ⑭ 삽입 직후 정수 구간 — AM {am_gate[0]}–{am_gate[1]} (계획 {n_am_plan:,})'
         + (f' · SE {se_gate[0]}–{se_gate[1]} (계획 {n_se_plan:,})' if se_gate else '') + ' 밖이면 quit 1 — 삽입은 NP 1'
         if am_gate else '#   ⑭ 개수 검사 없음'),
        ('#   ⑯ 끝 상태 = 최종 restart_end · atom · contact · mesh 한 장씩 (run 0) · 이완 중 체크포인트 끔 (restart 0)'
         if end_frames else '#   ⑯ 끝 상태 출력 없음'),
        '#   ⑬ (D0.7 · D1 · D2) 삽입 전용 덱 = 이 덱의 정착 run 앞까지 그대로 + run 20000 + write_restart restart_settling_20001 + run 3000 (NP 1)',
        (f'#   ⑮ 이웃 skin {skin_old:g} → {float(skin_um):g} µm (속도 시험 · 물리 같음 · 궤적만 다름)'
         if skin_um is not None else f'#   ⑮ 이웃 skin 그대로 ({skin_old:g} µm)'),
        '#   그대로: 재료 property/global 전부 (E_SE 0.135e7 = 1.35 GPa 연화값) · 접촉법칙 · dt · 이웃 · 벽 · 중력 · 감쇠 ·',
        '#     정착 200,000 · 안정화 200,000 · 판 속도 0.01 · 목표 0.30 (300 MPa) · 이완 100,000 · 접촉 · mesh 덤프',
        '#   예상 입자 수 (질량분율 규약): ' + ' · '.join(f'{k} {v:,}' for k, v in rec['counts_pred'].items())
        + f' (합 {n_tot:,}) · 예상 면용량 {load_pred:.3f} mAh/cm²',
        '#   ⚠ 상별 수는 MPI 랭크 · 시드에 따라 흔들린다 (부족 또는 초과 · SELF-70 · KG50-07) — 삽입은 NP 1 · 런 뒤 덤프로 실현 조성을 센다.',
        '#   ⚠ 감쇠 fix damp all viscous 0.5 = 모든 입자에 같은 γ — γ/m 이 SE 크기에 따라 다르다 (D0.7 ↔ D3 ≈ 79 배 · KG50-04 · 대조 = 등록 뒤).',
        '#   ⚠ 언로딩 없음 — 끝 상태 = 판 고정 이완 (가압 상태) · 실험 (하중 제거) 과 바로 비교하지 않는다.',
    ]
    full = '\n'.join(head) + '\n' + out
    if TAG_OLD.lower() in full.lower():
        _die(f'{case}: 기준 덱 태그가 덱에 남았다 (주석 포함 — ibb dem_restart.py 가 "다른 케이스명 혼입" 으로 거부한다)')
    return full, rec


def roundtrip(deck: str, rec: dict) -> list:
    """생성한 덱을 다시 읽어 기록과 대조한다.  → 불일치 목록 (빈 목록 = 통과)."""
    bad = []
    body = '\n'.join(ln for ln in deck.split('\n') if not ln.lstrip().startswith('#'))   # 실행 줄만 (머리 주석 제외)
    tpl, ent = PS.read_deck(body)
    dens = {v['atype']: v['dens'] for v in tpl.values()}
    if dens.get(1) != round(rec['dens_g_cm3']['AM'] * 1000) or dens.get(3) != round(rec['dens_g_cm3']['SE'] * 1000):
        bad.append(f'밀도 {dens}')
    ent_d = dict(ent)
    if abs(ent_d.get('pts1', -1) - rec['am_mass']) > 1e-12 or abs(ent_d.get('pts3', -1) - (1 - rec['am_mass'])) > 1e-12 \
            or 'pts2' in ent_d:
        bad.append(f'분포 {ent}')
    for var, um in (('r_AM_P', rec['r_am_um']), ('r_SE', rec['r_se_um'])):
        m = re.compile(PS.RE_VAR.pattern.format(var), re.M).search(deck)
        if not m or abs(float(m.group(2)) * UM_PER_SIM - um) > 1e-9:
            bad.append(f'{var} {m.group(2) if m else None}')
    box = rec['box_um'] / UM_PER_SIM
    for m in RE_REGION.finditer(deck):
        v = [float(x) for x in m.group(3).split()]
        if abs(v[1] - box) > 1e-12 or abs(v[3] - box) > 1e-12:
            bad.append(f'{m.group(2)} x·y {v[1]} {v[3]}')
        if m.group(2) == 'reg_mix' and abs(v[5] - rec['reg_mix_z_top']) > 1e-9:
            bad.append(f'reg_mix z1 {v[5]}')
    for m in RE_VERTEX.finditer(deck):
        for t in (m.group(2), m.group(4)):
            if float(t) not in (0.0,) and abs(float(t) - box) > 1e-12:
                bad.append(f'판 꼭짓점 {t}')
    ar = [float(m.group(2)) for m in RE_AREA.finditer(deck)]
    if len(ar) != 2 or any(abs(a - box * box) > 1e-15 for a in ar):
        bad.append(f'압력 면적 {ar}')
    seeds = [int(m.group(3)) for m in PS.RE_PTS.finditer(deck)]
    mp = PS.RE_PDD.search(deck)
    mi = PS.RE_INS.search(deck)
    seeds += [int(mp.group(2)) if mp else -1, int(mi.group(2)) if mi else -1]
    if seeds != rec['seeds'] or not all(PS.is_prime(s) for s in seeds) or len(set(seeds)) != 5:
        bad.append(f'시드 {seeds}')
    ma = PS.RE_MAXATT.findall(body)
    if [int(x[1]) for x in ma] != [rec['maxattempt']]:
        bad.append(f'maxattempt {ma}')
    if TAG_OLD.lower() in deck.lower():                    # 주석 줄 포함 (dem_restart.py "다른 케이스명 혼입" · 10-27)
        bad.append('옛 태그 (주석 포함)')
    if body.count('processors * * 1') != 1 or body.find('processors * * 1') > body.find('region reg_box'):
        bad.append('processors')
    case = rec['case']
    rc = f'restart {rec["compress_restart_every"]} restart_{case}/restart_compress_*.bin'
    i_mv, i_rc, i_lp = body.find('fix move_press'), body.find(rc), body.find('label loop_press')
    if body.count(rc) != 1 or not (0 <= i_mv < i_rc < i_lp):
        bad.append('restart_compress 자리')
    i_un, i_gate, i_set = body.find('unfix ins_mix'), body.find('count(all)'), body.find('run 200000')
    if not (0 <= i_un < i_gate < i_set) or 'quit 1' not in body:
        bad.append('삽입 자기검사 자리')
    if f'post_{case}/atom_' not in body or f'post_{case}/contact_' not in body or f'plate_{case}.stl' not in body:
        bad.append('출력 경로 태그')
    ir = f'write_restart restart_{case}/restart_settling_1.bin'
    i_ir, i_set2 = body.find(ir), body.find('run 200000')
    if rec.get('insert_restart'):
        if body.count(ir) != 1 or not (body.find('restart 50000 restart_' + case + '/restart_settling_') < i_ir < i_set2):
            bad.append('삽입 직후 체크포인트 자리')
    elif ir in body:
        bad.append('삽입 직후 체크포인트가 요청 없이 있다')
    md = RE_DUMP_ATOM.search(deck)
    if not md or int(md.group(2)) != rec['atom_dump_every']:
        bad.append(f'atom 덤프 간격 {md.group(2) if md else None}')
    if len(re.findall(r'^[ \t]*restart[ \t]+\d+[ \t]+restart_\S+/restart_compress_', body, re.M)) != 1:
        bad.append('압축 체크포인트 줄 수')
    g = rec.get('am_gate')
    i_grp = body.find('group g_am_ins type 1')
    if g:
        lo, hi = g
        want_if = f'if "${{n_am_ins}} < {lo} || ${{n_am_ins}} > {hi}" then'
        if (body.count('group g_am_ins type 1') != 1 or body.count(want_if) != 1
                or 'variable n_am_ins equal count(g_am_ins)' not in body
                or not (0 <= i_gate < i_grp < i_set)
                or (rec.get('insert_restart') and not (i_grp < i_ir))):
            bad.append('활물질 수 검사 (자리 · 문턱)')
    elif i_grp >= 0 or 'g_am_ins' in body:
        bad.append('활물질 수 검사가 요청 없이 있다')
    gs = rec.get('se_gate')
    if gs:
        lo, hi = gs
        want_if = f'if "${{n_se_ins}} < {lo} || ${{n_se_ins}} > {hi}" then'
        i_sg = body.find('group g_se_ins type 3')
        if (body.count('group g_se_ins type 3') != 1 or body.count(want_if) != 1
                or 'variable n_se_ins equal count(g_se_ins)' not in body or not (0 <= i_gate < i_sg < i_set)):
            bad.append('SE 수 검사 (자리 · 문턱)')
    elif 'g_se_ins' in body:
        bad.append('SE 수 검사가 요청 없이 있다')
    if rec.get('end_frames'):
        i_um = body.find('unfix move_press')
        i_r0 = body.find('restart 0')
        i_p4 = body.find('PHASE 4: RELAXATION')
        i_last = body.rfind('run 100000')
        i_end = body.find(f'write_restart restart_{case}/restart_end.bin')
        i_r00 = body.find('run 0\n')
        if not (0 <= i_um < i_r0 < i_p4 < i_last < i_end < i_r00) or body.count('restart 0') != 1:
            bad.append('끝 상태 · 이완 체크포인트 자리')
        for nm in ('dmp_atom_end all custom 1 ', 'dmp_contact_end all local 1 ', 'dmp_mesh_end all mesh/stl 1 '):
            if body.count('dump ' + nm) != 1:
                bad.append(f'끝 상태 덤프 {nm.split()[0]}')
        if body.count('undump dmp_') != 3:
            bad.append('끝 상태 undump')
    elif 'restart_end.bin' in body or 'restart 0' in body:
        bad.append('끝 상태 출력이 요청 없이 있다')
    mn = RE_NEIGHBOR.findall(body)
    if len(mn) != 1 or abs(float(mn[0][1]) * UM_PER_SIM - rec['skin_um']) > 1e-9:
        bad.append(f'이웃 skin {mn}')
    return bad


def _insert_cut(prod: str, case: str) -> int:
    """본 덱의 정착 run (`restart 50000 …restart_settling_*` 뒤 첫 `run 200000`) 줄의 시작 위치."""
    m = re.search(rf'^restart[ \t]+50000[ \t]+restart_{re.escape(case)}/restart_settling_\*\.bin[^\n]*$', prod, re.M)
    if not m:
        _die(f'{case}: 정착 체크포인트 줄을 못 찾았다 — 삽입 전용 덱을 만들 수 없다')
    r = re.compile(r'^run[ \t]+200000[ \t]*$', re.M).search(prod, m.end())
    if not r:
        _die(f'{case}: 정착 run 200000 줄을 못 찾았다')
    return r.start()


def insert_tail(case: str, settle_steps: int, tail_steps: int) -> list:
    return [f'run {int(settle_steps)}', f'write_restart restart_{case}/restart_settling_{int(settle_steps) + 1}.bin',
            f'run {int(tail_steps)}']


def insert_deck(prod: str, rec: dict, settle_steps: int = 20000, tail_steps: int = 3000) -> str:
    """⑬ 삽입 전용 덱 = 본 덱의 정착 run 줄 앞까지 바이트 그대로 + `run S` + `write_restart …settling_<S+1>` + `run T` — 끝.

    NP 1 로 돌려 상별 수를 계획대로 넣고 (SELF-70 · KG50-01 · 09), `resume_ckpt.sh` (settling 모드) 가 step S+1 에서
    코어를 늘려 이어받는다.  재개 체크포인트가 첫 바닥 접촉 (≈ 3,500 step) 뒤라 재개 시험의 비교 줄 (S+1,000 …) 이
    접촉 · 재료 정의를 지난다 (KG50-10).  끝 run T 는 그 비교 줄을 원 로그에 남기려는 것 — 결과로 쓰지 않는다.
    """
    if not (5000 <= int(settle_steps) <= 199000) or not (1000 <= int(tail_steps) <= 10000):
        _die('삽입 전용 덱: 정착 5,000–199,000 step · 끝 run 1,000–10,000 step')
    cut = _insert_cut(prod, rec['case'])
    return (prod[:cut] + '\n'.join(insert_tail(rec['case'], settle_steps, tail_steps)) + '\n'
            + f'# ⑬ 삽입 전용 덱 끝 — NP 1 로 돌린 뒤 resume_ckpt.sh (settling 모드 · step {int(settle_steps) + 1}) 로 '
            + f'본 덱 ({rec["case"]}) 을 이어받는다\n')


def insert_check(prod: str, ins: str, rec: dict, settle_steps: int = 20000, tail_steps: int = 3000) -> list:
    bad = []
    try:
        cut = _insert_cut(prod, rec['case'])
    except SystemExit as e:
        return [str(e)]
    if not ins.startswith(prod[:cut]):
        bad.append('삽입 전용 덱 앞부분 ≠ 본 덱')
    tail = [ln.strip() for ln in ins[cut:].split('\n') if ln.strip() and not ln.lstrip().startswith('#')]
    if tail != insert_tail(rec['case'], settle_steps, tail_steps):
        bad.append(f'삽입 전용 덱 끝 실행 줄 {tail}')
    if 'fix move_press' in ins or ins.count('run 200000') != prod[:cut].count('run 200000'):
        bad.append('삽입 전용 덱에 정착 본 run 또는 압축')
    return bad


#: 기준 덱 대비 바뀌어도 되는 실행 줄 (선언 자리 ①–⑯) — 그 밖의 변경 = 문제 (KG50-12)
DECLARED_LINE_PATTERNS = [re.compile(p) for p in (
    r'^variable\s+r_(AM_P|SE)\s+equal\s+',
    r'^fix\s+pts[123]\s+all\s+particletemplate/sphere\s+\d+\s+atom_type\s+[123]\s+density\s+constant\s+\d+\s+radius\s+constant\s+\$\{r_\w+\}',
    r'^fix\s+pdd_mix\s+all\s+particledistribution/discrete\s+\d+\s+\d+\s+',
    r'^fix\s+ins_mix\s+all\s+insert/pack\s+seed\s+\d+\s+distributiontemplate\s+pdd_mix\s+&$',
    r'^\s+maxattempt\s+\d+\s+insert_every\s+once\s+overlapcheck\s+yes\s+all_in\s+no\s+&$',
    r'^region\s+(reg_box|reg_mix)\s+block\s+',
    r'^print\s+"vertex\s+',
    r'abs\(f_top_mesh\[3\]\)\s*/\s*[0-9.]+\s*/\s*1000000',
    r'^processors \* \* 1$',
    r'^variable n_ins equal count\(all\)$', r'^print "====== INSERTED ', r'^if "\$\{n_ins\} < \d+" then &$',
    r"^\s+\"print 'FATAL: (partial insertion|AM count off plan|SE count off plan)", r'^\s+"quit 1"$',
    r'^group g_(am|se)_ins type [13]$', r'^variable n_(am|se)_ins equal count\(g_(am|se)_ins\)$',
    r'^print "====== (AM|SE) \$\{n_(am|se)_ins\}', r'^if "\$\{n_(am|se)_ins\} < \d+ \|\| \$\{n_(am|se)_ins\} > \d+" then &$',
    r'^restart \d+ restart_\S+/restart_compress_\*\.bin$',
    r'^dump\s+dmp_atom\s+all\s+custom\s+\d+\s+',
    r'^write_restart restart_\S+/restart_settling_1\.bin',
    r'^restart 0\b', r'^write_restart restart_\S+/restart_end\.bin$', r'^dump dmp_(atom|contact|mesh)_end ',
    r'^run 0$', r'^undump dmp_(atom|contact|mesh)_end$', r'^\s+(c_cpl\[\d+\]\s*)+&?$',
    r'^print "====== INSERTING PARTICLES \(', r'^print "====== Simulation Finished! \(',
    r'^neighbor\s+[0-9.eE+-]+\s+bin$',
)]


def template_diff(deck: str, text: str, case: str) -> list:
    """기준 덱 (태그만 케이스명으로) 과 실행 줄을 줄 단위로 대조 — 선언 자리 밖의 변경 목록 (빈 목록 = 통과 · KG50-12)."""
    def exe(t):
        return [ln.rstrip() for ln in t.split('\n') if ln.strip() and not ln.lstrip().startswith('#')]
    base = exe(text.replace(TAG_OLD, case).replace(TAG_OLD.upper(), case.upper()))
    new = exe(deck)
    bad = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=base, b=new, autojunk=False).get_opcodes():
        if op == 'equal':
            continue
        bad += ['+ ' + ln for ln in new[j1:j2] if not any(r.search(ln) for r in DECLARED_LINE_PATTERNS)]
        bad += ['- ' + ln for ln in base[i1:i2] if not any(r.search(ln) for r in DECLARED_LINE_PATTERNS)]
    return bad


#: 생성 파일 (덱 · 삽입 덱 · 러너) 의 어느 줄에도 — 줄 전체 주석 포함 — 다른 케이스명을 쓰지 않는다 (10-27).
#:   ibb `dem_restart.py` 가 v2 덱을 "덱 검증 실패: 다른 케이스명 혼입: ['real_4']" 로 거부했다 (`plan_r56.txt`) —
#:   덱 머리 주석 두 줄 (3 · 9 행) 의 기준 덱 태그 때문 · 실행 줄에는 없다.  그 도구의 실제 이름 목록은 리포에 없다
#:   (미확인) → 여기서는 기준 덱 태그 · 프리셋의 다른 케이스 · 러너 원형 케이스 + 기준 덱 계열 이름 `real_<N>` 을 본다.
FOREIGN_NAME_PATTERNS = (re.compile(r'(?<![a-z0-9])real_\d+(?![0-9])', re.I),)


def foreign_name_list(cfg: dict, cases=(), runner_case=None) -> list:
    """다른 케이스명 후보 = 기준 덱 태그 + 프리셋 케이스 전부 (본 · 대비 50×50) + 이번 케이스 + 러너 원형 케이스."""
    names = {TAG_OLD}
    for key in ('cases', 'fallback50'):
        names |= {c[0] for c in cfg.get(key, ())}
    names |= {c[0] for c in cases}
    if runner_case:
        names.add(runner_case)
    return sorted(names)


def foreign_name_lines(text: str, own: str, names, patterns=FOREIGN_NAME_PATTERNS) -> list:
    """text 의 줄 가운데 자기 케이스 (own) 가 아닌 이름을 담은 줄 → [(줄 번호, 이름, 줄)] · 빈 목록 = 통과.

    대소문자를 가리지 않는다 (print 의 대문자 태그도).  자기 이름 안에 통째로 든 다른 이름은 세지 않는다 —
    거꾸로 다른 이름 안에 자기 이름이 들어 있으면 그 다른 이름은 센다 (덮는 쪽만 면제).
    """
    own_l = own.lower()
    foreign = sorted({n.lower() for n in names if n and n.lower() != own_l})
    hits = []
    for i, ln in enumerate(text.split('\n'), 1):
        low = ln.lower()
        cover = [(m.start(), m.end()) for m in re.finditer(re.escape(own_l), low)] if own_l else []

        def _covered(a, b, cover=cover):
            return any(s <= a and b <= e for s, e in cover)
        found = set()
        for n in foreign:
            j = low.find(n)
            while j >= 0:
                if not _covered(j, j + len(n)):
                    found.add(n)
                    break
                j = low.find(n, j + 1)
        for rx in patterns:
            for m in rx.finditer(low):
                if m.group(0) != own_l and not _covered(m.start(), m.end()):
                    found.add(m.group(0))
        hits += [(i, n, ln) for n in sorted(found)]
    return hits


def load_template(path=None, expect=TEMPLATE_SHA256):
    raw = open(path or TEMPLATE, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    if expect and sha != expect:
        _die(f'기준 덱 sha256 {sha[:16]}… ≠ 고정값 {expect[:16]}… — 다른 템플릿이다')
    return raw.decode('utf-8'), sha


def _write(path, txt):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(txt)
    return hashlib.sha256(txt.encode('utf-8')).hexdigest()


def build(out_dir, cases, cfg, template_path=None, expect_sha=TEMPLATE_SHA256, runner_text=None, runner_case=None,
          ntasks=None):
    """본 덱 (+ 삽입 전용 덱 · 러너) · manifest.json.  cases = (케이스, r_SE µm, 영역 µm, 시드 슬롯)."""
    text, sha = load_template(template_path, expect_sha)
    if os.path.exists(out_dir) and os.listdir(out_dir):
        _die(f'{out_dir} 가 비어 있지 않다 — 덮어쓰지 않는다')
    names = [c[0] for c in cases]
    if len(set(names)) != len(names) or len({c[3] for c in cases}) != len(cases):
        _die('케이스명 또는 시드 슬롯 중복')
    os.makedirs(out_dir, exist_ok=True)
    kw = {k: cfg[k] for k in DECK_KW if k in cfg}
    recs = []
    fnames = foreign_name_list(cfg, cases, runner_case)

    def _put(case, path, txt):
        """쓰기 전 검사 — 생성 파일 어느 줄에도 (주석 포함) 다른 케이스명이 있으면 쓰지 않고 멈춘다 (10-27)."""
        hits = foreign_name_lines(txt, case, fnames)
        if hits:
            _die(f'{case}: {os.path.basename(path)} 에 다른 케이스명 {sorted({h[1] for h in hits})} ({len(hits)} 줄 · 첫 줄 '
                 f'{hits[0][0]} 행) — ibb dem_restart.py 가 "다른 케이스명 혼입" 으로 거부한다 · 쓰지 않는다')
        return _write(path, txt)
    for case, r_se, box, slot in cases:
        deck, rec = make_deck(text, case, r_se, box, slot, **kw)
        bad = roundtrip(deck, rec) + template_diff(deck, text, case)
        if bad:
            _die(f'{case} 왕복 · 기준 덱 대조 실패: {bad}')
        cdir = os.path.join(out_dir, case)
        os.makedirs(cdir)
        rec['seed_slot'] = slot
        rec['deck_sha256'] = _put(case, os.path.join(cdir, f'input_{case}.liggghts'), deck)
        do_ins = case in cfg.get('insert_cases', ())
        st, tt = cfg.get('insert_settle_steps', 20000), cfg.get('insert_tail_steps', 3000)
        if do_ins:
            ins = insert_deck(deck, rec, st, tt)
            bad = insert_check(deck, ins, rec, st, tt)
            if bad:
                _die(f'{case} 삽입 전용 덱 검사 실패: {bad}')
            rec['insert_deck_sha256'] = _put(case, os.path.join(cdir, f'input_{case}_insert.liggghts'), ins)
        if runner_text is not None:
            if do_ins:
                rt = render_ibb_runner(runner_text, runner_case, case, 1, deck='insert')
                rec['ibb_runner_insert'] = dict(ntasks=1, sha256=_put(case, os.path.join(cdir, f'run_{case}_insert.sh'), rt))
            if ntasks and case in ntasks:
                rt = render_ibb_runner(runner_text, runner_case, case, int(ntasks[case]))
                rec['ibb_runner'] = dict(ntasks=int(ntasks[case]),
                                         sha256=_put(case, os.path.join(cdir, f'run_{case}.sh'), rt))
        recs.append(rec)
    me = open(os.path.abspath(__file__), 'rb').read()
    man = dict(generator='scripts/make_se_size_decks.py', generator_sha256=hashlib.sha256(me).hexdigest(),
               template='docs/data/phase_a_6mah/in.real_4.liggghts', template_sha256=sha,
               config={k: v for k, v in cfg.items() if k not in ('cases', 'fallback50')}, cases=recs)
    _write(os.path.join(out_dir, 'manifest.json'), json.dumps(man, ensure_ascii=False, indent=2) + '\n')
    return man


def render_ibb_runner(template: str, tmpl_case: str, case: str, ntasks: int, deck: str = 'main') -> str:
    """ibb 러너 = 리포의 실물 러너 (`run_pse_r075_a_r30.sh`) 에서 케이스 · 코어 두 자리 · cd · -in 을 갈아끼운다.

    ★ 코어는 `#SBATCH -n N` 과 `mpirun --oversubscribe --bind-to none -np N` 이 짝 (2026-09-27 실패 ①② · LHS 러너 규약).
    ★ 케이스 폴더 = `$HOME/dem_test/<case>` — 1저자 `a6_resume.sh` 의 DT0/<case> 와 같은 자리 (나중에 코어를 바꿔 이어받기).
    """
    if not (1 <= ntasks <= 60):
        _die(f'ntasks {ntasks} — 1..60 (qos cpu-60)')
    if deck not in ('main', 'insert'):
        _die(f'러너 덱 종류 {deck}')
    job = case + ('_ins' if deck == 'insert' else '')
    inp = f'input_{case}_insert.liggghts' if deck == 'insert' else f'input_{case}.liggghts'
    t = template
    t = _sub_exact(t, r'^(#SBATCH\s+--job-name=)\S+$', rf'\g<1>{job}', 1, '러너 job-name')
    t = _sub_exact(t, r'^(#SBATCH\s+--output=logs/output_)\S+?(_%j\.out)$', rf'\g<1>{job}\g<2>', 1, '러너 output')
    t = _sub_exact(t, r'^(#SBATCH\s+-n\s+)\d+$', rf'\g<1>{ntasks}', 1, '러너 -n')
    t = _sub_exact(t, r'^cd\s+\S+$', f'cd $HOME/dem_test/{case}', 1, '러너 cd')
    t = _sub_exact(t, r'^mpirun\s+--oversubscribe\s+--bind-to\s+none\s+-np\s+\d+\s+lmp_mpi\s+-in\s+\S+$',
                   f'mpirun --oversubscribe --bind-to none -np {ntasks} lmp_mpi -in {inp}', 1, '러너 mpirun')
    if tmpl_case in t:
        _die('러너에 템플릿 케이스명이 남았다')
    return t


def hit_command(case: str, ntasks: int, tag: str = 'v1', deck: str = 'main') -> str:
    """hit (SLURM 없음) — 1저자 `hit_resume.sh` 와 같은 꼴 (setsid nohup · lmp_auto · log_<case>_*.out)."""
    if not (1 <= ntasks <= 20):
        _die(f'hit ntasks {ntasks} — 1..20')
    if deck not in ('main', 'insert'):
        _die(f'hit 덱 종류 {deck}')
    inp = f'input_{case}_insert.liggghts' if deck == 'insert' else f'input_{case}.liggghts'
    return (f'cd $HOME/simulation/{case} && setsid nohup mpirun --oversubscribe --bind-to none -np {ntasks} '
            f'$HOME/LIGGGHTS-PUBLIC/src/lmp_auto -in {inp} > log_{case}_{tag}.out 2>&1 < /dev/null &')


# ───────────────────────────── selftest ─────────────────────────────

def _selftest() -> int:
    ok, fail = 0, []

    def chk(name, cond):
        """cond = 값 또는 함수 — 함수가 예외를 내면 (기능이 없으면 · 고치기 전) 실패로 센다."""
        nonlocal ok
        try:
            v = cond() if callable(cond) else cond
        except Exception:                                  # noqa: BLE001  (SystemExit 는 raises 로만)
            v = False
        if v:
            ok += 1
        else:
            fail.append(name)

    def raises(fn, needle=None):
        try:
            fn()
        except SystemExit as e:
            return needle is None or needle in str(e)
        except Exception:                                  # noqa: BLE001
            return False
        return False

    text, sha = load_template()
    cfg = dict(PRESET_KG50Y4)
    kw = {k: cfg[k] for k in DECK_KW if k in cfg}
    names = [c[0] for c in cfg['cases']]
    chk('P1 본 케이스 9 = 40×40 넷 + D3 칸 비교 다섯', names == [
        'kg50_d07_b40', 'kg50_d1_b40', 'kg50_d2_b40', 'kg50_d3_b40_s1', 'kg50_d3_b50_s1',
        'kg50_d3_b40_s2', 'kg50_d3_b40_s3', 'kg50_d3_b50_s2', 'kg50_d3_b50_s3'])
    chk('P2 대비 50×50 셋 (D0.7 · D1 · D2) 은 따로 · 본 목록에 D0.7-50 없음',
        [c[0] for c in cfg.get('fallback50', [])] == ['kg50_d07_b50', 'kg50_d1_b50', 'kg50_d2_b50']
        and 'kg50_d07_b50' not in names)
    slots = [c[3] for c in cfg['cases']] + [c[3] for c in cfg.get('fallback50', [])]
    chk('P3 시드 슬롯 12 개 서로 다름 · 0–15', len(set(slots)) == len(slots) == 12 and all(0 <= s <= 15 for s in slots))
    decks = {c[0]: make_deck(text, c[0], c[1], c[2], c[3], **kw) for c in cfg['cases']}
    fb = {c[0]: make_deck(text, c[0], c[1], c[2], c[3], **kw) for c in cfg.get('fallback50', [])}
    d50, r50 = decks['kg50_d3_b50_s1']
    d40, r40 = decks['kg50_d3_b40_s1']
    d07, r07 = fb['kg50_d07_b50']
    p07, q07 = decks['kg50_d07_b40']

    # 고체 두께 · 면용량 (손 산술)
    t = (0.0325 / 4.85 + 0.0325 * 0.15 / 0.85 / 1.64) * 1e4
    chk('A1 고체 두께 = (L/C)/ρ_AM + SE 몫 (101.98 µm)', abs(r50['solid_thickness_um'] - t) < 1e-4 and abs(t - 101.981) < 0.01)
    chk('A2 삽입 높이 = 고체 두께 / 0.321', abs(r50['insert_height_um'] - t / 0.321) < 1e-3)
    chk('A3 높이는 영역과 무관 (40 = 50)', r40['reg_mix_z_top'] == r50['reg_mix_z_top'])
    chk('A4 예상 면용량 6.5 ± 0.5 % (50)', abs(r50['loading_pred_mah_cm2'] - 6.5) / 6.5 < 0.005)
    chk('A5 예상 면용량 6.5 ± 0.5 % (40)', abs(r40['loading_pred_mah_cm2'] - 6.5) / 6.5 < 0.005)
    chk('A6 활물질 개수 비 40/50 ≈ 0.64', abs(r40['counts_pred']['AM_P'] / r50['counts_pred']['AM_P'] - 0.64) < 0.005)
    n_se_07 = r07['counts_pred']['SE']
    chk('A7 D0.7 · 50 SE ≈ 48.7 만 (손 산술 87,425 µm³ / 0.17959)', abs(n_se_07 - 87425 / (4 / 3 * math.pi * 0.35 ** 3)) / n_se_07 < 0.01)
    chk('A8 D0.7 · 50 int32 곱 < 2^31/1.3', r07['int32_product'] * 1.3 < 2 ** 31 - 1)
    chk('A9 활물질 계획 수 40×40 = 948 · 50×50 = 1,481', r40['counts_pred']['AM_P'] == 948 and r50['counts_pred']['AM_P'] == 1481
        and q07['counts_pred']['AM_P'] == 948)
    # 재료 블록 · 소성 깊이 0.05
    for case, (d, r) in list(decks.items()) + list(fb.items()):
        chk(f'B1 {case} 재료 블록 바이트 그대로', material_block(d) == material_block(text))
    chk('B2 소성 깊이 행렬의 0.05 는 40 덱에도 남는다', '0.05 0.05 0.01 &' in d40)
    body40 = '\n'.join(ln for ln in d40.split('\n') if not ln.lstrip().startswith('#') and 'property/global' not in ln
                       and not re.match(r'^\s+[0-9.e+-]+\s+[0-9.e+-]+\s+[0-9.e+-]+\s*&?\s*$', ln))
    chk('B3 40 덱 실행 줄에 영역 0.05 · 면적 0.0025 없음', re.search(r'(?<![0-9.])0\.05(?![0-9])', body40) is None
        and '0.0025' not in body40)
    chk('B4 40 덱 면적 0.0016 두 곳', d40.count('/0.0016/') + d40.count('/ 0.0016 /') == 2)
    chk('B5 50 덱 면적 0.0025 두 곳', d50.count('/0.0025/') + d50.count('/ 0.0025 /') == 2)
    chk('B6 반례: 0.05 를 전체 치환하면 재료 블록 (소성 깊이) 이 바뀐다 = 자리 제한이 필요하다',
        material_block(text.replace('0.05', '0.04')) != material_block(text))
    # 왕복
    for case, (d, r) in list(decks.items()) + list(fb.items()):
        chk(f'C1 {case} 왕복검사 통과', roundtrip(d, r) == [])
    # 반례 (왕복검사가 실제로 잡는가)
    chk('D1 판 꼭짓점 하나만 0.05 로 되돌리면 잡는다', roundtrip(d40.replace('vertex 0.0 0.04', 'vertex 0.0 0.05', 1), r40) != [])
    chk('D2 면적 하나만 되돌리면 잡는다', roundtrip(d40.replace('/0.0016/', '/0.0025/', 1), r40) != [])
    chk('D3 SE 밀도를 2000 으로 되돌리면 잡는다', roundtrip(re.sub(r'(atom_type 3 density constant )1640', r'\g<1>2000', d50), r50) != [])
    chk('D4 restart_compress 를 지우면 잡는다',
        roundtrip(d50.replace('restart 200000 restart_kg50_d3_b50_s1/restart_compress_*.bin\n', ''), r50) != [])
    chk('D5 분포에 pts2 를 되살리면 잡는다', roundtrip(d50.replace(' 2 pts1 0.85 pts3 0.15', ' 3 pts1 0.6 pts2 0.25 pts3 0.15'), r50) != [])
    chk('D6 maxattempt 를 10000 으로 되돌리면 잡는다', roundtrip(d50.replace('maxattempt 3000', 'maxattempt 10000'), r50) != [])
    chk('D7 reg_mix 위끝을 0.30 으로 되돌리면 잡는다',
        roundtrip(d50.replace(f'0.005 {r50["reg_mix_z_top"]:.6f}', '0.005 0.30'), r50) != [])
    # int32 거부 · 입력 거부
    chk('E1 D0.7 · maxattempt 10000 = int32 초과 거부',
        raises(lambda: make_deck(text, 'x_d07', 0.35, 50, 0, **dict(kw, maxattempt=10000)), 'PS-01'))
    for bad_args, nm in (((0.0, 50), 'r_SE 0'), ((3.0, 50), 'r_SE = r_AM'), ((1.5, 5), '영역 5 µm')):
        chk(f'E2 {nm} 거부', raises(lambda b=bad_args: make_deck(text, 'x', b[0], b[1], 0, **kw)))
    chk('E3 다른 템플릿 sha 거부', raises(lambda: load_template(None, '0' * 64)))
    chk('E4 시드 슬롯 16 이상 거부 (ps45 대역 침범)', raises(lambda: seeds_for(16)))
    # 시드 · 태그 · 자리
    allseeds = [s for _, r in list(decks.values()) + list(fb.values()) for s in r['seeds']]
    chk('F1 시드 60 개 서로 다름 · 8 자리 소수', len(allseeds) == 60 and len(set(allseeds)) == 60
        and all(10 ** 7 <= s < 10 ** 8 and PS.is_prime(s) for s in allseeds))
    chk('F2 ps45 시드 대역 (20M–53.2M) 과 안 겹침', all(not (20_000_000 <= s <= 53_200_009) for s in allseeds))
    chk('F3 머리에 SELF-70 · 언로딩 없음 표지', 'SELF-70' in d50 and '언로딩 없음' in d50)
    chk('F4 옛 머리 (Real Condition 4 · Bimodal · 6 mAh) 없음', 'Real Condition 4' not in d50 and 'Bimodal' not in d50
        and '6 mAh/cm²' not in d50)
    chk('F5 atom 덤프 간격 = 50,000 (Q3) · 지정 없으면 템플릿 5,000', r50['atom_dump_every'] == 50000
        and 'dump dmp_atom all custom 50000 ' in d50
        and 'dump dmp_atom all custom 5000 ' in make_deck(text, 'kg50_d3_b50_s1', 1.5, 50, 4, **dict(kw, atom_dump_every=None))[0])
    chk('F7 접촉 덤프 10,000 의 배수 아니면 거부',
        raises(lambda: make_deck(text, 'kg50_d07_b50', 0.35, 50, 9, **dict(kw, atom_dump_every=25000))))
    chk('F8 본 덱에는 step 1 체크포인트 없음 (삽입 전용 덱만 · KG50-10)',
        all('restart_settling_1.bin' not in d and roundtrip(d, r) == [] for d, r in decks.values()))
    d_ir, r_ir = make_deck(text, 'kg50_d07_b50', 0.35, 50, 9, **dict(kw, insert_restart=True))
    chk('F9 insert_restart 켬 = step 1 체크포인트 · 끔으로 기록하면 왕복이 잡는다',
        'write_restart restart_kg50_d07_b50/restart_settling_1.bin' in d_ir and roundtrip(d_ir, dict(r_ir, insert_restart=False)) != [])
    # 재개 스크립트가 읽는 표지 (a6_resume.sh · hit_resume.sh 의 덱 마커)
    marks = ['PHASE 1: SETTLING', 'write_restart restart_kg50_d3_b50_s1/restart_after_settling.bin', 'PHASE 2: STABILIZE',
             'PHASE 3: COMPRESSION', 'label loop_press', 'PHASE 4: RELAXATION', 'variable pressMPa', 'fix top_mesh',
             'dump dmp_mesh', 'unfix move_press', 'restart 50000 restart_kg50_d3_b50_s1/restart_settling_*.bin',
             'variable press_speed equal 0.01', 'variable dt      equal 1.0e-6']
    chk('G1 재개 스크립트 덱 마커 13 개 그대로', all(m in d50 for m in marks))
    def _exe(d):                                       # 실행 줄만 (머리 주석에도 같은 문자열이 있다)
        return '\n'.join(ln for ln in d.split('\n') if not ln.lstrip().startswith('#'))
    # ⑪ 압축 체크포인트 간격 (Q4)
    chk('K1 본 덱 압축 체크포인트 = 200,000 · move_press 바로 뒤 · 정착 체크포인트 50,000 그대로',
        all(f'restart 200000 restart_{c}/restart_compress_*.bin' in d and 'restart_compress' in d
            and f'restart 50000 restart_{c}/restart_settling_*.bin' in d
            and _exe(d).find('fix move_press') < _exe(d).find(f'restart 200000 restart_{c}/restart_compress_')
            < _exe(d).find('label loop_press')
            for c, (d, r) in decks.items()))
    # ⑭ 활물질 수 검사 (Q1 · SELF-70)
    def _gate_ok(d, lo, hi):
        d = _exe(d)
        i_cnt, i_grp = d.find('count(all)'), d.find('group g_am_ins type 1')
        i_run = d.find('run 200000')
        return (0 <= i_cnt < i_grp < i_run and 'variable n_am_ins equal count(g_am_ins)' in d
                and f'if "${{n_am_ins}} < {lo} || ${{n_am_ins}} > {hi}" then' in d)
    chk('I1 활물질 정수 구간 40×40 = 944–952 (948 · ceil/floor · KG50-08)', _gate_ok(d40, 944, 952) and _gate_ok(p07, 944, 952))
    chk('I2 활물질 정수 구간 50×50 = 1474–1488 (1,481)', _gate_ok(d50, 1474, 1488))
    chk('I2b 정수 구간 = 손 산술 (948·0.995 = 943.26 → 944 · 948·1.005 = 952.74 → 952 · 1481 → 1474–1488)',
        int_band(948, 0.005) == (944, 952) and int_band(1481, 0.005) == (1474, 1488) and int_band(200, 0.005) == (199, 201))
    n_se40 = r40['counts_pred']['SE']
    lo_se, hi_se = -((-n_se40 * 995) // 1000), (n_se40 * 1005) // 1000
    chk('I2c SE 수 검사 = 계획 SE ±0.5 % 정수 구간 · 삽입 검사 뒤 (KG50-13)', r40['se_gate'] == [lo_se, hi_se]
        and f'if "${{n_se_ins}} < {lo_se} || ${{n_se_ins}} > {hi_se}" then' in d40 and 'group g_se_ins type 3' in d40)
    chk('I3 반례: 검사 문턱을 바꾸거나 검사를 지우면 왕복이 잡는다',
        roundtrip(d40.replace('< 944 ||', '< 900 ||'), r40) != []
        and roundtrip(d40.replace('group g_am_ins type 1\n', ''), r40) != [])
    # ⑬ 삽입 전용 덱 (Q1 · KG50-01 · 09 · 10)
    st, tt = cfg['insert_settle_steps'], cfg['insert_tail_steps']
    ins = insert_deck(p07, q07, st, tt)
    _ln = p07.split('\n')
    _k = [i for i, ln in enumerate(_ln) if ln.strip() == 'run 200000']
    cut = len('\n'.join(_ln[:_k[0]])) + 1 if _k else -1
    chk('I4 삽입 전용 덱 = 본 덱의 정착 run 앞까지 그대로 + run 20000 · write_restart …settling_20001 · run 3000',
        cut > 0 and ins.startswith(p07[:cut]) and [ln for ln in ins[cut:].split('\n') if ln.strip() and not ln.startswith('#')]
        == ['run 20000', 'write_restart restart_kg50_d07_b40/restart_settling_20001.bin', 'run 3000']
        and insert_check(p07, ins, q07, st, tt) == [])
    _exe_ins = '\n'.join(ln for ln in ins.split('\n') if not ln.lstrip().startswith('#'))
    chk('I5 삽입 전용 덱 = 압축 없음 · 정착 본 run 없음 · 세 삽입 검사 있음 · 끝 상태 출력 없음', 'fix move_press' not in ins
        and ins.count('run 200000') == 0 and 'group g_am_ins type 1' in ins and 'group g_se_ins type 3' in ins
        and 'count(all)' in ins and 'restart_end' not in _exe_ins)
    chk('I6 반례: 삽입 전용 덱에 줄을 더하거나 앞부분을 바꾸면 잡는다',
        insert_check(p07, ins + 'run 200000\n', q07, st, tt) != []
        and insert_check(p07, ins.replace('maxattempt 3000', 'maxattempt 2000'), q07, st, tt) != [])
    chk('I7 삽입 전용 덱을 만드는 케이스 = D0.7 · D1 · D2 (40 · 50) · D3 칸 비교는 없음 (처음부터 끝까지 NP 1)',
        set(cfg['insert_cases']) == {'kg50_d07_b40', 'kg50_d1_b40', 'kg50_d2_b40', 'kg50_d07_b50', 'kg50_d1_b50', 'kg50_d2_b50'}
        and not any(c.startswith('kg50_d3') for c in cfg['insert_cases']))
    # ⑯ 끝 상태 (Q4 · KG50-03 · 11)
    body40 = '\n'.join(ln for ln in d40.split('\n') if not ln.lstrip().startswith('#'))
    chk('L1 restart 0 = unfix move_press 바로 뒤 · 이완 앞', body40.find('unfix move_press') < body40.find('restart 0')
        < body40.find('PHASE 4: RELAXATION') and body40.count('restart 0') == 1)
    i_last = body40.rfind('run 100000')
    tail40 = body40[i_last:]
    chk('L2 끝 상태 = 마지막 run 100000 뒤 · restart_end 먼저 · 덤프 셋 간격 1 · run 0 · undump 셋',
        tail40.find('write_restart restart_kg50_d3_b40_s1/restart_end.bin') < tail40.find('dump dmp_atom_end all custom 1 ')
        < tail40.find('run 0\n') and 'dump dmp_contact_end all local 1 post_kg50_d3_b40_s1/contact_end_*.liggghts &' in tail40
        and 'dump dmp_mesh_end all mesh/stl 1 post_kg50_d3_b40_s1/mesh_end_*.stl top_mesh' in tail40
        and tail40.count('undump dmp_') == 3 and tail40.count('c_cpl[26]') == 1)
    chk('L3 반례: 끝 상태 덤프를 지우거나 restart 0 을 지우면 왕복이 잡는다',
        roundtrip(d40.replace('undump dmp_mesh_end\n', ''), r40) != [] and roundtrip(d40.replace('restart 0   #', '#', 1), r40) != [])
    # 기준 덱 줄 대조 (Q7 · KG50-12)
    chk('M1 본 덱 아홉 · 대비 셋 = 기준 덱 대비 선언 자리 밖 변경 0', all(template_diff(d, text, c) == []
        for c, (d, r) in list(decks.items()) + list(fb.items())))
    muts = [('variable press_speed equal 0.01', 'variable press_speed equal 0.02'),
            ('fix damp all viscous 0.5', 'fix damp all viscous 0.4'),
            ('variable dt      equal 1.0e-6', 'variable dt      equal 2.0e-6'),
            ('fix gravi all gravity 9.81 vector 0.0 0.0 -1.0', 'fix gravi all gravity 9.8 vector 0.0 0.0 -1.0'),
            ('neigh_modify    delay 0 check yes', 'neigh_modify    delay 10 check yes'),
            ('volumefraction_region 0.321', 'volumefraction_region 0.33'),
            ('variable target_press equal 0.30', 'variable target_press equal 0.31')]
    caught = [old for old, new in muts                       # 실행 줄 (줄머리) 만 바꾼다 — 머리 주석에도 같은 문자열이 있다
              if re.search(r'^([ \t]*)' + re.escape(old), d40, re.M)
              and template_diff(re.sub(r'^([ \t]*)' + re.escape(old), lambda m, n=new: m.group(1) + n, d40, count=1, flags=re.M),
                                text, 'kg50_d3_b40_s1') != []]
    chk(f'M2 반례 일곱 (판 속도 · 감쇠 · dt · 중력 · 이웃 재구축 · 체적분율 · 목표 압력) = 기준 덱 대조가 전부 잡는다 ({len(caught)}/7)',
        len(caught) == 7)
    chk('M3 반례: 선언 밖 줄을 하나 더하면 잡는다', template_diff(d40 + 'fix extra all viscous 0.1\n', text, 'kg50_d3_b40_s1') != [])
    # 이름 (KG50-14)
    allnames = [c[0] for c in cfg['cases']] + [c[0] for c in cfg['fallback50']]
    chk('N1 케이스 이름 중 다른 이름의 접두어인 것 없음 (resume_ckpt.sh 큐 접두어 대조 겹침 방지)',
        not any(a != b and b.startswith(a) for a in allnames for b in allnames))
    # 러너
    rt0 = open(os.path.join(ROOT, 'docs', 'data', 'pure_se_r075_20260927', 'run_pse_r075_a_r30.sh'), encoding='utf-8').read()
    rt = render_ibb_runner(rt0, 'pse_r075_a', 'kg50_d07_b40', 30)
    chk('H1 러너 -n 30 · -np 30 짝 · --bind-to none', '#SBATCH -n 30' in rt
        and 'mpirun --oversubscribe --bind-to none -np 30 lmp_mpi -in input_kg50_d07_b40.liggghts' in rt)
    chk('H2 러너 job-name · output · cd', '--job-name=kg50_d07_b40' in rt and 'logs/output_kg50_d07_b40_%j.out' in rt
        and 'cd $HOME/dem_test/kg50_d07_b40' in rt)
    chk('H3 러너 qos · time · OMP 1 그대로', '--qos=cpu-60' in rt and '--time=5-00:00:00' in rt and 'OMP_NUM_THREADS=1' in rt)
    chk('H4 ntasks 61 거부', raises(lambda: render_ibb_runner(rt0, 'pse_r075_a', 'x', 61)))
    hc = hit_command('kg50_d3_b40', 4)
    chk('H5 hit 명령 = setsid nohup · lmp_auto · log_<case>_v1.out', 'setsid nohup mpirun --oversubscribe --bind-to none -np 4' in hc
        and 'lmp_auto -in input_kg50_d3_b40.liggghts > log_kg50_d3_b40_v1.out' in hc)
    ri = render_ibb_runner(rt0, 'pse_r075_a', 'kg50_d07_b40', 1, deck='insert')
    chk('H6 삽입 러너 = -n 1 · -np 1 · input_<case>_insert · job/로그 <case>_ins · 같은 폴더', '#SBATCH -n 1' in ri
        and 'mpirun --oversubscribe --bind-to none -np 1 lmp_mpi -in input_kg50_d07_b40_insert.liggghts' in ri
        and '--job-name=kg50_d07_b40_ins' in ri and 'logs/output_kg50_d07_b40_ins_%j.out' in ri
        and 'cd $HOME/dem_test/kg50_d07_b40' in ri)
    hi = hit_command('kg50_d1_b40', 1, tag='ins', deck='insert')
    chk('H7 hit 삽입 명령 = -np 1 · input_<case>_insert · log_<case>_ins.out',
        '-np 1 ' in hi and 'lmp_auto -in input_kg50_d1_b40_insert.liggghts > log_kg50_d1_b40_ins.out' in hi)

    # ── R: 생성 파일의 다른 케이스명 (10-27 ibb dem_restart.py "다른 케이스명 혼입: ['real_4']") · v2 대비 주석만 ──
    import tempfile
    rt_case = re.sub(r'_r\d+t?$', '', re.search(r'^#SBATCH\s+--job-name=(\S+)$', rt0, re.M).group(1))
    all12 = list(cfg['cases']) + list(cfg['fallback50'])
    nt12 = {'kg50_d07_b40': 56, 'kg50_d2_b40': 4, 'kg50_d07_b50': 56, 'kg50_d2_b50': 4}   # v2 · v3 (50×50) 같은 NP 뜻
    fnames = foreign_name_list(cfg, all12, rt_case)
    files, texts, man_g, build_err = {}, {}, None, None
    with tempfile.TemporaryDirectory() as td:
        gen = os.path.join(td, 'gen')
        try:
            man_g = build(gen, all12, cfg, runner_text=rt0, runner_case=rt_case, ntasks=nt12)
        except SystemExit as e:
            build_err = str(e)
        for c, *_ in all12:
            cd = os.path.join(gen, c)
            files[c] = sorted(os.listdir(cd)) if os.path.isdir(cd) else []
            for f in files[c]:
                with open(os.path.join(cd, f), encoding='utf-8') as fh:
                    texts[(c, f)] = fh.read()
    chk('R0 12 케이스 build (v2 러너 원형 · NP 56 · 4) 성공' + (f' — {build_err[:160]}' if build_err else ''), build_err is None)
    n_files = sum(len(v) for v in files.values())
    chk(f'R1a 생성 파일 = 본 덱 12 + 삽입 덱 6 + 삽입 러너 6 + 본 러너 4 = 28 ({n_files} · 빈 검사로 초록 방지)', n_files == 28
        and all(f'input_{c}.liggghts' in files[c] for c, *_ in all12))
    for c, *_ in all12:
        hits = [(f, h) for f in files[c] for h in foreign_name_lines(texts[(c, f)], c, fnames)]
        chk(f'R1 {c} 생성 파일 {len(files[c])} 개 (덱 · 삽입 덱 · 러너) 어느 줄에도 (주석 포함) 다른 케이스명 없음 — 위반 {len(hits)} 줄'
            + (f' (예: {hits[0][0]} {hits[0][1][0]} 행 {hits[0][1][1]!r})' if hits else ''), files[c] and not hits)
    base = '\n'.join(ln for ln in d40.split('\n') if not ln.lstrip().startswith('#'))      # 실행 줄만 (옛 · 새 같음)
    nb = len(base.split('\n'))
    chk('R1b 반례: 깨끗한 덱 (실행 줄) 에 기준 덱 파일 이름 주석 한 줄을 넣으면 잡는다 (줄 번호 · 이름 real_4)',
        foreign_name_lines(base, 'kg50_d3_b40_s1', fnames) == []
        and [h[:2] for h in foreign_name_lines(base + '\n#   기준 덱 docs/data/phase_a_6mah/in.real_4.liggghts', 'kg50_d3_b40_s1', fnames)]
        == [(nb + 1, 'real_4')])
    inj = [('#   kg50_d2_b40 과 같은 시드', 'kg50_d2_b40'), ('print "====== X (REAL_4) ======"', 'real_4'),
           ('#   러너 원형 pse_r075_a', 'pse_r075_a'), ('#   real_14 스캐폴드', 'real_14'), ('#   ⑦ 태그 real_4 → kg50_d3_b40_s1', 'real_4')]
    chk('R1c 반례 다섯: 다른 생성 케이스 · 대문자 REAL_4 · 러너 원형 케이스 · 같은 계열 real_14 · v2 의 ⑦ 줄 = 전부 잡는다',
        all([h[1] for h in foreign_name_lines(base + '\n' + ln, 'kg50_d3_b40_s1', fnames)] == [nm] for ln, nm in inj))
    chk('R1d 자기 이름 (소문자 · 대문자) 은 안 잡는다 · 자기 이름 안의 짧은 이름은 면제 · 다른 이름 안의 자기 이름은 면제 안 함',
        foreign_name_lines(base + '\n# kg50_d3_b40_s1 · KG50_D3_B40_S1', 'kg50_d3_b40_s1', fnames) == []
        and foreign_name_lines('abc_long x', 'abc_long', ['abc'], patterns=()) == []
        and [h[1] for h in foreign_name_lines('abc_long', 'abc', ['abc_long'], patterns=())] == ['abc_long'])
    # v2 대비 = 주석만 바뀐다 (커밋된 v2 와 실행 줄 바이트 같음 · 러너 · 기록 그대로)
    V2 = os.path.join(ROOT, 'docs', 'data', 'kg50_decks_20261026_v2')
    v2_cases = [c[0] for c in cfg['cases']]
    v2_files = {c: (sorted(os.listdir(os.path.join(V2, c))) if os.path.isdir(os.path.join(V2, c)) else None) for c in v2_cases}

    def _nc(t):
        return [ln for ln in t.split('\n') if not ln.lstrip().startswith('#')]
    chk('R2a v2 아홉 케이스 파일 목록 = 재생성 파일 목록 (17 개)', all(v2_files[c] == files.get(c) for c in v2_cases)
        and sum(len(v2_files[c] or []) for c in v2_cases) == 17)
    for c in v2_cases:
        same = []
        for f in (v2_files[c] or []):
            with open(os.path.join(V2, c, f), encoding='utf-8') as fh:
                old = fh.read()
            new = texts.get((c, f))
            same.append(new is not None and (_nc(new) == _nc(old) if f.endswith('.liggghts') else new == old))
        chk(f'R2 {c} 재생성 = 커밋된 v2 (덱 · 삽입 덱 = 주석 아닌 줄 바이트 같음 · 러너 = 파일 전체 같음 · {len(same)} 파일)',
            bool(same) and all(same))
    try:
        with open(os.path.join(V2, 'manifest.json'), encoding='utf-8') as fh:
            man_v2 = json.load(fh)
    except (OSError, ValueError):
        man_v2 = None

    def _strip(m, keep):
        m = json.loads(json.dumps(m))
        m.pop('generator_sha256', None)
        m['cases'] = [{k: v for k, v in r.items() if k not in ('deck_sha256', 'insert_deck_sha256')}
                      for r in m['cases'] if r['case'] in keep]
        return m
    chk('R2b manifest = v2 (생성기 · 덱 sha256 값만 다를 수 있음 · 러너 sha256 · 기록 · 설정 같음)',
        man_g is not None and man_v2 is not None and _strip(man_g, set(v2_cases)) == _strip(man_v2, set(v2_cases)))
    tdir = os.path.relpath(os.path.dirname(TEMPLATE), ROOT).replace(os.sep, '/') + '/'
    decks_g = [(c, f) for (c, f) in texts if f.endswith('.liggghts')]

    def _head_ok(c, t):
        cm = [ln for ln in t.split('\n') if ln.lstrip().startswith('#')]
        return (any('기준 덱' in ln and TEMPLATE_SHA256 in ln and tdir in ln for ln in cm)
                and any(ln.startswith('#   ⑦ 태그') and f'→ {c}' in ln for ln in cm))
    chk(f'R3 덱 머리 = 기준 덱 sha256 64 자 전체 · 폴더 {tdir} · ⑦ 태그 바꿈 줄 (→ 케이스명) ({len(decks_g)} 덱) · '
        'manifest template 경로 · sha256 그대로', len(decks_g) == 18 and all(_head_ok(c, texts[(c, f)]) for c, f in decks_g)
        and man_g is not None and man_g['template'] == 'docs/data/phase_a_6mah/in.real_4.liggghts'
        and man_g['template_sha256'] == TEMPLATE_SHA256)
    chk('R4 반례: 왕복검사가 주석 줄의 기준 덱 태그도 잡는다 (머리 주석 · 대문자)',
        roundtrip(d40 + '#   기준 덱 in.real_4.liggghts\n', r40) != [] and roundtrip(d40 + '# REAL_4\n', r40) != [])
    with tempfile.TemporaryDirectory() as td:
        out5 = os.path.join(td, 'g')
        bad_rt = rt0.rstrip('\n') + '\n# 원형 메모: real_4 덱에서 옮김\n'
        r5 = raises(lambda: build(out5, [cfg['cases'][0]], cfg, runner_text=bad_rt, runner_case=rt_case,
                                  ntasks={'kg50_d07_b40': 56}), '다른 케이스명')
        leaked = []
        for dp, _dn, fs in os.walk(out5):
            for f in fs:
                with open(os.path.join(dp, f), encoding='utf-8') as fh:
                    if f != 'manifest.json' and 'real_4' in fh.read().lower():
                        leaked.append(f)
    chk(f'R5 반례: 생성 파일에 다른 케이스명이 들어가면 build 가 거부 · 그 파일을 쓰지 않는다 (러너 원형 주석의 기준 덱 태그 · '
        f'쓴 위반 파일 {len(leaked)})', r5 and not leaked)

    print(f'make_se_size_decks selftest: {ok}/{ok + len(fail)} PASS')
    for f in fail:
        print('  ✗', f)
    return 0 if not fail else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--preset', choices=['kg50y4'])
    ap.add_argument('--only', help='케이스명 쉼표 목록 (프리셋 안에서)')
    ap.add_argument('--fallback50', action='store_true', help='50×50 의 D0.7 · D1 · D2 도 (40×40 불합격일 때만)')
    ap.add_argument('--out')
    ap.add_argument('--ibb-runner', help='ibb 러너 원형 (예: docs/data/pure_se_r075_20260927/run_pse_r075_a_r30.sh)')
    ap.add_argument('--ntasks', help='case:N 쉼표 목록 — 본 덱 ibb 러너 코어 수 (삽입 러너는 늘 1)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if not a.preset or not a.out:
        ap.error('--preset 과 --out 이 필요하다 (또는 --selftest)')
    cfg = dict(PRESET_KG50Y4)
    cases = list(cfg['cases']) + (list(cfg['fallback50']) if a.fallback50 else [])
    if a.only:
        want = [s.strip() for s in a.only.split(',') if s.strip()]
        miss = [w for w in want if w not in {c[0] for c in cases}]
        if miss:
            ap.error(f'목록에 없는 케이스: {miss}')
        cases = [c for c in cases if c[0] in want]
    nt = None
    rt = rc = None
    if a.ntasks:
        nt = dict((k, int(v)) for k, v in (t.split(':') for t in a.ntasks.split(',')))
        if not a.ibb_runner:
            ap.error('--ntasks 는 --ibb-runner 와 같이')
    if a.ibb_runner:
        rt = open(a.ibb_runner, encoding='utf-8').read()
        m = re.search(r'^#SBATCH\s+--job-name=(\S+)$', rt, re.M)
        if not m:
            ap.error('러너 원형에 --job-name 이 없다')
        rc = re.sub(r'_r\d+t?$', '', m.group(1))
    man = build(a.out, cases, cfg, runner_text=rt, runner_case=rc, ntasks=nt)
    for r in man['cases']:
        g = r.get('am_gate') or ['-', '-']
        h = r.get('se_gate') or ['-', '-']
        print(f"{r['case']:16s} SE r {r['r_se_um']:<4g} 영역 {r['box_um']:g}  입자 {r['n_total_pred']:>8,}  "
              f"AM {r['counts_pred']['AM_P']:>5,} ({g[0]}–{g[1]})  SE ({h[0]}–{h[1]})  면용량 {r['loading_pred_mah_cm2']:.3f}  "
              f"시드 슬롯 {r['seed_slot']}  삽입 덱 {'예' if r.get('insert_deck_sha256') else '-'}")
    print(f'→ {a.out}/manifest.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
