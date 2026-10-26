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
  ⑦ 태그 `real_4` → 케이스명 (출력 폴더 · 판 STL · print)
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
    insert_restart=True,            # ⑬ 1저자 10-26 Q1 권고대로 (모든 덱 · 삽입 전용 덱과 짝)
    am_gate_tol=0.005,              # ⑭ 1저자 10-26 Q1 — 삽입 직후 활물질 수 ±0.5 %
    insert_extra_steps=2000,        # ⑬ 삽입 전용 덱의 끝 run — 재개 시험 G3 의 비교 줄 (thermo 1000)
    #: (케이스, r_SE µm, 영역 µm, 시드 슬롯) — 슬롯이 시드를 정한다 (바꾸면 다른 침대)
    cases=[('kg50_d07_b40', 0.35, 40, 0), ('kg50_d1_b40', 0.5, 40, 1), ('kg50_d2_b40', 1.0, 40, 2),
           ('kg50_d3_b40', 1.5, 40, 3),
           ('kg50_d3_b50', 1.5, 50, 4),                                   # Q5 칸 비교 — 시드 1 짝
           ('kg50_d3_b40_s2', 1.5, 40, 5), ('kg50_d3_b40_s3', 1.5, 40, 6),
           ('kg50_d3_b50_s2', 1.5, 50, 7), ('kg50_d3_b50_s3', 1.5, 50, 8)],
    #: 40×40 이 D3 칸 비교에서 불합격일 때만 (`--fallback50`) — D0.7-50 은 1저자 10-26 철회 (미리 돌리지 않는다)
    fallback50=[('kg50_d07_b50', 0.35, 50, 9), ('kg50_d1_b50', 0.5, 50, 10), ('kg50_d2_b50', 1.0, 50, 11)],
    #: ⑮ 속도 시험 (1저자 10-26 Q2) — 본 덱 kg50_d07_b40 와 같은 시드 · skin 둘 × 코어 둘 · 정착 20,000 step 만
    speed=dict(base='kg50_d07_b40', steps=20000, skins_um=(2.0, 0.5), nps=(28, 56)),
)

#: 시드 — make_ps_sweep 의 20M–53M 대역 · LHS 의 5 자리와 겹치지 않는 8 자리 대역.  바꾸면 다른 침대가 된다.
#: 슬롯 16 개 (0–15) → 최대 ≈ 18.9 M · 한 슬롯 안 다섯 시드 간격 100,000 < 슬롯 간격 500,000 (겹침 없음)
SEED_BASE, SEED_STEP, SEED_SUB = 11_000_000, 500_000, 100_000
DECK_KW = ('r_am_um', 'am_mass', 'loading_mah_cm2', 'cap_mah_g', 'dens_gen', 'maxattempt', 'atom_dump_every',
           'compress_restart_every', 'insert_restart', 'am_gate_tol')

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


def make_deck(text: str, case: str, r_se_um: float, box_um: float, idx: int, *, r_am_um, am_mass,
              loading_mah_cm2, cap_mah_g, dens_gen, maxattempt, atom_dump_every=None, insert_restart=False,
              compress_restart_every=50000, am_gate_tol=None, skin_um=None):
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
    am_gate = None
    gate_txt = PS.insert_gate(n_tot)
    if am_gate_tol is not None:
        tol = float(am_gate_tol)
        if not (0 < tol < 0.05) or n_am_plan <= 0:
            _die(f'활물질 수 검사 허용폭 {am_gate_tol} — (0, 0.05) · 계획 수 {n_am_plan}')
        lo, hi = math.floor(n_am_plan * (1 - tol)), math.ceil(n_am_plan * (1 + tol))
        am_gate = (lo, hi)
        gate_txt += (f'\n# ⑭ 삽입 직후 활물질 수 — 계획 {n_am_plan:,} ±{tol * 100:g} % (SELF-70: NP 가 크면 소수 상이 체계적으로 '
                     f'부족 → 삽입은 NP 1)\n'
                     f'group g_am_ins type 1\n'
                     f'variable n_am_ins equal count(g_am_ins)\n'
                     f'print "====== AM ${{n_am_ins}} / {n_am_plan} (gate {lo}-{hi}) ======"\n'
                     f'if "${{n_am_ins}} < {lo} || ${{n_am_ins}} > {hi}" then &\n'
                     f'    "print \'FATAL: AM count off plan (SELF-70) - insert at NP 1. aborting.\'" &\n'
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

    # ── ⑮ (속도 시험 덱만) 이웃 skin ──
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
               skin_um=float(skin_um) if skin_um is not None else skin_old, skin_um_template=skin_old,
               **ADD.dens_record(dens_gen))
    head = [
        '# ===== SE 입도 비교 생성본 (make_se_size_decks.py · 50kg/batch 4차년도) =====',
        f'#   {case}: {desc}',
        f'#   기준 덱 docs/data/phase_a_6mah/in.real_4.liggghts (sha256 {TEMPLATE_SHA256[:16]}…) — 바꾼 자리 = 아래뿐',
        f'#   ① 조성 단일 활물질 (AM_P 자리 · pts2 정의만) · 질량분율 AM {PS.fmt_frac(am_mass)} · SE {PS.fmt_frac(1 - am_mass)}',
        f'#   ② r_AM_P {r_am_um:g} µm · r_SE {r_se_um:g} µm   ③ 진밀도 세대 {dens_gen}: AM {rho_am:g} · SE {rho_se:g} g/cm³',
        f'#   ④ 영역 {box_um:g}×{box_um:g} µm (reg_box · reg_mix · 판 꼭짓점 · 압력 면적 {_fmt_sim(area)})',
        f'#   ⑤ 삽입 위끝 z {z_top:.6f} (높이 {(z_top - z0_mix) * UM_PER_SIM:.1f} µm · volumefraction {vf:g} 그대로) '
        f'= 고체 두께 {t_solid_um:.2f} µm = {loading_mah_cm2:g} mAh/cm² @ {cap_mah_g:g} mAh/g',
        '#   ⑥ 시드 (큰 소수 · 케이스마다 독립): ' + ', '.join(str(s) for s in seeds),
        f'#   ⑦ 태그 {TAG_OLD} → {case}   ⑧ maxattempt {att_old:,} → {att:,} (예상 {n_tot:,} × {att:,} = '
        f'{n_tot * att:.3g} < 2^31/1.3 · 원장 PS-01)',
        f'#   ⑨ {PS.PROC_GRID} (x·y 분할)   ⑩ 삽입 자기검사 (99 %)   ⑪ {rc} (간격 {cre:,})',
        (f'#   ⑫ atom 덤프 간격 {dump_old:,} → {int(atom_dump_every):,}' if atom_dump_every
         else f'#   ⑫ atom 덤프 간격 그대로 ({dump_old:,})'),
        (f'#   ⑬ 삽입 직후 체크포인트 {ir} (NP 1 삽입 → 재개 스크립트로 코어 변경)' if insert_restart
         else '#   ⑬ 삽입 직후 체크포인트 없음 (첫 체크포인트 = step 50,000)'),
        (f'#   ⑭ 삽입 직후 활물질 수 {am_gate[0]}–{am_gate[1]} (계획 {n_am_plan:,}) 밖이면 quit 1 — 삽입은 NP 1 (SELF-70)'
         if am_gate else '#   ⑭ 활물질 수 검사 없음'),
        (f'#   ⑮ 이웃 skin {skin_old:g} → {float(skin_um):g} µm (속도 시험 · 물리 같음 · 궤적만 다름)'
         if skin_um is not None else f'#   ⑮ 이웃 skin 그대로 ({skin_old:g} µm)'),
        '#   그대로: 재료 property/global 전부 (E_SE 0.135e7 = 1.35 GPa 연화값) · 접촉법칙 · dt · 이웃 · 벽 · 중력 · 감쇠 ·',
        '#     정착 200,000 · 안정화 200,000 · 판 속도 0.01 · 목표 0.30 (300 MPa) · 이완 100,000 · 접촉 · mesh 덤프',
        '#   예상 입자 수 (질량분율 규약): ' + ' · '.join(f'{k} {v:,}' for k, v in rec['counts_pred'].items())
        + f' (합 {n_tot:,}) · 예상 면용량 {load_pred:.3f} mAh/cm²',
        '#   ⚠ 상별 수는 MPI 랭크 수 NP 만큼 흔들린다 (소수 상 = 활물질이 체계적으로 부족 · 원장 SELF-70) — 삽입은 NP 1 ·',
        '#     런 뒤 덤프로 실현 조성을 센다.',
        '#   ⚠ 언로딩 없음 — 끝 상태 = 판 고정 이완 (가압 상태) · 실험 (하중 제거) 과 바로 비교하지 않는다.',
    ]
    return '\n'.join(head) + '\n' + out, rec


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
    if TAG_OLD in body or TAG_OLD.upper() in body:
        bad.append('옛 태그')
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
    mn = RE_NEIGHBOR.findall(body)
    if len(mn) != 1 or abs(float(mn[0][1]) * UM_PER_SIM - rec['skin_um']) > 1e-9:
        bad.append(f'이웃 skin {mn}')
    return bad


def _insert_cut(prod: str, case: str) -> int:
    rx = re.compile(rf'^write_restart[ \t]+restart_{re.escape(case)}/restart_settling_1\.bin\b[^\n]*$', re.M)
    ms = list(rx.finditer(prod))                     # 실행 줄만 (머리 주석 '#   ⑬ …' 는 줄머리가 # 라 안 맞는다)
    if len(ms) != 1:
        _die(f'{case}: step 1 체크포인트 실행 줄이 정확히 하나가 아니다 ({len(ms)}) — 삽입 전용 덱을 만들 수 없다')
    return ms[0].end() + 1


def insert_deck(prod: str, rec: dict, extra_steps: int = 2000) -> str:
    """⑬ 삽입 전용 덱 = 본 덱의 step 1 체크포인트 줄까지 바이트 그대로 + `run <extra>` (정착의 첫 부분) — 끝.

    NP 1 로 돌려 상별 수를 계획대로 넣고 (SELF-70), 그 폴더를 `resume_ckpt.sh` (settling 모드) 가 이어받는다.
    끝 run 은 재개 시험 G3 (첫 정규 줄 = step 1000) 의 비교 줄을 원 로그에 남기려는 것 — 결과로 쓰지 않는다.
    """
    n = int(extra_steps)
    if not (1000 <= n <= 10000):
        _die('삽입 전용 덱 끝 run 은 1,000–10,000 (thermo 1,000 줄이 원 로그에 있어야 G3 를 비교한다)')
    cut = _insert_cut(prod, rec['case'])
    return (prod[:cut] + f'run {n}\n'
            + f'# ⑬ 삽입 전용 덱 끝 — NP 1 로 돌린 뒤 resume_ckpt.sh (settling 모드) 로 본 덱 ({rec["case"]}) 을 이어받는다\n')


def insert_check(prod: str, ins: str, rec: dict) -> list:
    bad = []
    try:
        cut = _insert_cut(prod, rec['case'])
    except SystemExit as e:
        return [str(e)]
    if not ins.startswith(prod[:cut]):
        bad.append('삽입 전용 덱 앞부분 ≠ 본 덱')
    tail = [ln for ln in ins[cut:].split('\n') if ln.strip() and not ln.lstrip().startswith('#')]
    if len(tail) != 1 or not re.fullmatch(r'run \d+', tail[0].strip()):
        bad.append(f'삽입 전용 덱 끝 실행 줄 {tail}')
    if 'run 200000' in ins or 'fix move_press' in ins:
        bad.append('삽입 전용 덱에 정착 본 run 또는 압축')
    return bad


def speed_decks(text: str, cfg: dict) -> dict:
    """⑮ 속도 시험 덱 (1저자 10-26 Q2) — 본 D0.7-40 과 같은 시드 · skin 둘 × 코어 둘.  결과 = 시간만.

    본 덱과 다른 점: skin · 활물질 수 검사 없음 (NP 28 · 56 삽입이라 SELF-70 으로 걸린다 · 구조를 쓰지 않으니 무관) ·
    step 1 체크포인트 뒤 `run <steps>` 에서 끝 (정착의 첫 부분 = 낙하 중 → 작은 skin 이 재구축을 더 하니 이득의 하한).
    """
    sp = cfg['speed']
    base = next(c for c in cfg['cases'] if c[0] == sp['base'])
    kw = {k: cfg[k] for k in DECK_KW if k in cfg}
    kw['am_gate_tol'] = None
    kw['insert_restart'] = True
    out = {}
    for skin in sp['skins_um']:
        for np_ in sp['nps']:
            name = f'kg50_spd_{sp["base"][5:]}_sk{int(round(skin * 10)):02d}_np{np_}'
            d, r = make_deck(text, name, base[1], base[2], base[3], skin_um=skin, **kw)
            cut = _insert_cut(d, name)
            d = (d[:cut].replace('# ===== SE 입도 비교 생성본', '# ===== ⚠ 속도 시험 전용 (결과 = 시간만 · 구조 쓰지 않음) · SE 입도 비교 생성본', 1)
                 + f'run {int(sp["steps"])}\n')
            r = dict(r, speed_test=dict(base=sp['base'], skin_um=skin, ntasks=np_, steps=int(sp['steps'])))
            out[name] = (d, r)
    return out


def speed_check(deck: str, rec: dict) -> list:
    bad = []
    st = rec.get('speed_test') or {}
    lines = [ln for ln in deck.split('\n') if ln.strip() and not ln.lstrip().startswith('#')]
    if not lines or lines[-1].strip() != f'run {st.get("steps")}':
        bad.append('속도 시험 덱 끝 run')
    if 'run 200000' in deck or 'g_am_ins' in deck or 'fix move_press' in deck:
        bad.append('속도 시험 덱에 정착 본 run · 활물질 검사 · 압축')
    mn = RE_NEIGHBOR.findall(deck)
    if len(mn) != 1 or abs(float(mn[0][1]) * UM_PER_SIM - float(st.get('skin_um', -1))) > 1e-9:
        bad.append(f'속도 시험 skin {mn}')
    if '속도 시험 전용' not in deck:
        bad.append('속도 시험 머리 표지')
    return bad


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
          ntasks=None, with_speed=True):
    """본 덱 (+ 삽입 전용 덱 · 러너) · 속도 시험 덱 · manifest.json.  cases = (케이스, r_SE µm, 영역 µm, 시드 슬롯)."""
    text, sha = load_template(template_path, expect_sha)
    if os.path.exists(out_dir) and os.listdir(out_dir):
        _die(f'{out_dir} 가 비어 있지 않다 — 덮어쓰지 않는다')
    names = [c[0] for c in cases]
    if len(set(names)) != len(names) or len({c[3] for c in cases}) != len(cases):
        _die('케이스명 또는 시드 슬롯 중복')
    os.makedirs(out_dir, exist_ok=True)
    kw = {k: cfg[k] for k in DECK_KW if k in cfg}
    recs = []
    for case, r_se, box, slot in cases:
        deck, rec = make_deck(text, case, r_se, box, slot, **kw)
        bad = roundtrip(deck, rec)
        if bad:
            _die(f'{case} 왕복검사 실패: {bad}')
        cdir = os.path.join(out_dir, case)
        os.makedirs(cdir)
        rec['seed_slot'] = slot
        rec['deck_sha256'] = _write(os.path.join(cdir, f'input_{case}.liggghts'), deck)
        if cfg.get('insert_restart'):
            ins = insert_deck(deck, rec, cfg.get('insert_extra_steps', 2000))
            bad = insert_check(deck, ins, rec)
            if bad:
                _die(f'{case} 삽입 전용 덱 검사 실패: {bad}')
            rec['insert_deck_sha256'] = _write(os.path.join(cdir, f'input_{case}_insert.liggghts'), ins)
        if runner_text is not None:
            if cfg.get('insert_restart'):
                rt = render_ibb_runner(runner_text, runner_case, case, 1, deck='insert')
                rec['ibb_runner_insert'] = dict(ntasks=1, sha256=_write(os.path.join(cdir, f'run_{case}_insert.sh'), rt))
            if ntasks and case in ntasks:
                rt = render_ibb_runner(runner_text, runner_case, case, int(ntasks[case]))
                rec['ibb_runner'] = dict(ntasks=int(ntasks[case]), sha256=_write(os.path.join(cdir, f'run_{case}.sh'), rt))
        recs.append(rec)
    spd = []
    if with_speed and cfg.get('speed'):
        for name, (d, r) in speed_decks(text, cfg).items():
            bad = speed_check(d, r)
            if bad:
                _die(f'{name} 속도 시험 덱 검사 실패: {bad}')
            cdir = os.path.join(out_dir, 'speed', name)
            os.makedirs(cdir)
            r['deck_sha256'] = _write(os.path.join(cdir, f'input_{name}.liggghts'), d)
            if runner_text is not None:
                rt = render_ibb_runner(runner_text, runner_case, name, r['speed_test']['ntasks'])
                r['ibb_runner'] = dict(ntasks=r['speed_test']['ntasks'], sha256=_write(os.path.join(cdir, f'run_{name}.sh'), rt))
            spd.append(r)
    me = open(os.path.abspath(__file__), 'rb').read()
    man = dict(generator='scripts/make_se_size_decks.py', generator_sha256=hashlib.sha256(me).hexdigest(),
               template='docs/data/phase_a_6mah/in.real_4.liggghts', template_sha256=sha,
               config={k: v for k, v in cfg.items() if k not in ('cases', 'fallback50')}, cases=recs, speed_tests=spd)
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
        'kg50_d07_b40', 'kg50_d1_b40', 'kg50_d2_b40', 'kg50_d3_b40', 'kg50_d3_b50',
        'kg50_d3_b40_s2', 'kg50_d3_b40_s3', 'kg50_d3_b50_s2', 'kg50_d3_b50_s3'])
    chk('P2 대비 50×50 셋 (D0.7 · D1 · D2) 은 따로 · 본 목록에 D0.7-50 없음',
        [c[0] for c in cfg.get('fallback50', [])] == ['kg50_d07_b50', 'kg50_d1_b50', 'kg50_d2_b50']
        and 'kg50_d07_b50' not in names)
    slots = [c[3] for c in cfg['cases']] + [c[3] for c in cfg.get('fallback50', [])]
    chk('P3 시드 슬롯 12 개 서로 다름 · 0–15', len(set(slots)) == len(slots) == 12 and all(0 <= s <= 15 for s in slots))
    decks = {c[0]: make_deck(text, c[0], c[1], c[2], c[3], **kw) for c in cfg['cases']}
    fb = {c[0]: make_deck(text, c[0], c[1], c[2], c[3], **kw) for c in cfg.get('fallback50', [])}
    d50, r50 = decks['kg50_d3_b50']
    d40, r40 = decks['kg50_d3_b40']
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
        roundtrip(d50.replace('restart 200000 restart_kg50_d3_b50/restart_compress_*.bin\n', ''), r50) != [])
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
        and 'dump dmp_atom all custom 5000 ' in make_deck(text, 'kg50_d3_b50', 1.5, 50, 4, **dict(kw, atom_dump_every=None))[0])
    chk('F7 접촉 덤프 10,000 의 배수 아니면 거부',
        raises(lambda: make_deck(text, 'kg50_d07_b50', 0.35, 50, 9, **dict(kw, atom_dump_every=25000))))
    chk('F8 모든 본 덱에 step 1 체크포인트 (Q1) · Phase 1 restart 뒤 · run 200000 앞',
        all(f'write_restart restart_{c}/restart_settling_1.bin' in d and roundtrip(d, r) == [] for c, (d, r) in decks.items()))
    d_no, r_no = make_deck(text, 'kg50_d07_b50', 0.35, 50, 9, **dict(kw, insert_restart=False))
    chk('F9 insert_restart 끔 = 체크포인트 없음 · 있는데 끔으로 기록하면 왕복이 잡는다',
        'restart_settling_1.bin' not in d_no and roundtrip(d07, dict(r07, insert_restart=False)) != [])
    # 재개 스크립트가 읽는 표지 (a6_resume.sh · hit_resume.sh 의 덱 마커)
    marks = ['PHASE 1: SETTLING', 'write_restart restart_kg50_d3_b50/restart_after_settling.bin', 'PHASE 2: STABILIZE',
             'PHASE 3: COMPRESSION', 'label loop_press', 'PHASE 4: RELAXATION', 'variable pressMPa', 'fix top_mesh',
             'dump dmp_mesh', 'unfix move_press', 'restart 50000 restart_kg50_d3_b50/restart_settling_*.bin',
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
        i_ir, i_run = d.find('write_restart restart_'), d.find('run 200000')
        return (0 <= i_cnt < i_grp < i_ir < i_run and 'variable n_am_ins equal count(g_am_ins)' in d
                and f'if "${{n_am_ins}} < {lo} || ${{n_am_ins}} > {hi}" then' in d)
    chk('I1 활물질 수 검사 40×40 = 943–953 (948 ±0.5 %) · 삽입 검사 뒤 · step 1 체크포인트 앞', _gate_ok(d40, 943, 953)
        and _gate_ok(p07, 943, 953))
    chk('I2 활물질 수 검사 50×50 = 1473–1489 (1,481 ±0.5 %)', _gate_ok(d50, 1473, 1489))
    chk('I3 반례: 검사 문턱을 바꾸거나 검사를 지우면 왕복이 잡는다',
        roundtrip(d40.replace('< 943 ||', '< 900 ||'), r40) != []
        and roundtrip(d40.replace('group g_am_ins type 1\n', ''), r40) != [])
    # ⑬ 삽입 전용 덱 (Q1)
    ins = insert_deck(p07, q07, cfg['insert_extra_steps'])
    _ln = p07.split('\n')
    _k = [i for i, ln in enumerate(_ln) if ln.startswith('write_restart restart_kg50_d07_b40/restart_settling_1.bin')]
    cut = len('\n'.join(_ln[:_k[0] + 1])) + 1 if len(_k) == 1 else -1
    chk('I4 삽입 전용 덱 = 본 덱의 step 1 체크포인트 줄까지 그대로 + run 2000', ins.startswith(p07[:cut])
        and ins[cut:].strip().split('\n')[0] == 'run 2000' and insert_check(p07, ins, q07) == [])
    chk('I5 삽입 전용 덱에 정착 200,000 · 압축 없음 · 두 삽입 검사 있음', 'run 200000' not in ins and 'fix move_press' not in ins
        and 'group g_am_ins type 1' in ins and 'count(all)' in ins)
    chk('I6 반례: 삽입 전용 덱에 줄을 더하거나 앞부분을 바꾸면 잡는다',
        insert_check(p07, ins + 'run 200000\n', q07) != [] and insert_check(p07, ins.replace('maxattempt 3000', 'maxattempt 2000'), q07) != [])
    # ⑮ 속도 시험 덱 (Q2)
    sp = speed_decks(text, cfg)
    chk('J1 속도 시험 덱 4 = skin 2 · 0.5 µm × 코어 28 · 56', sorted(sp) == sorted([
        'kg50_spd_d07_b40_sk20_np28', 'kg50_spd_d07_b40_sk20_np56', 'kg50_spd_d07_b40_sk05_np28', 'kg50_spd_d07_b40_sk05_np56']))
    chk('J2 속도 시험 덱: skin 줄 · 활물질 검사 없음 · 정착 20,000 에서 끝 · 시드 = 본 D0.7-40 · 머리 표지',
        all(('neighbor        0.002 bin' if '_sk20_' in n else 'neighbor        0.0005 bin') in d
            and 'g_am_ins' not in d and d.rstrip().split('\n')[-1].startswith('run 20000') and 'run 200000' not in d
            and r['seeds'] == q07['seeds'] and '속도 시험 전용' in d and speed_check(d, r) == []
            for n, (d, r) in sp.items()))
    chk('J3 본 덱 skin 은 템플릿 그대로 (0.002) · 바꾸면 왕복이 잡는다', all('neighbor        0.002 bin' in d for d, _ in decks.values())
        and roundtrip(d40.replace('neighbor        0.002 bin', 'neighbor        0.0005 bin'), r40) != [])
    dsp, rsp = sp['kg50_spd_d07_b40_sk05_np56']
    chk('J4 반례: 속도 시험 덱에 정착 200,000 을 붙이면 잡는다', speed_check(dsp + 'run 200000\n', rsp) != [])
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

    print(f'make_se_size_decks selftest: {ok}/{ok + len(fail)} PASS')
    for f in fail:
        print('  ✗', f)
    return 0 if not fail else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--preset', choices=['kg50y4'])
    ap.add_argument('--only', help='케이스명 쉼표 목록 (프리셋 안에서)')
    ap.add_argument('--fallback50', action='store_true', help='50×50 의 D0.7 · D1 · D2 도 (40×40 불합격일 때만)')
    ap.add_argument('--no-speed', action='store_true', help='속도 시험 덱을 만들지 않는다')
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
    man = build(a.out, cases, cfg, runner_text=rt, runner_case=rc, ntasks=nt, with_speed=not a.no_speed)
    for r in man['cases']:
        g = r.get('am_gate') or ['-', '-']
        print(f"{r['case']:16s} SE r {r['r_se_um']:<4g} 영역 {r['box_um']:g}  입자 {r['n_total_pred']:>8,}  "
              f"AM {r['counts_pred']['AM_P']:>5,} (검사 {g[0]}–{g[1]})  면용량 {r['loading_pred_mah_cm2']:.3f}  "
              f"시드 슬롯 {r['seed_slot']}")
    for r in man['speed_tests']:
        st = r['speed_test']
        print(f"{r['case']:28s} 속도 시험 skin {st['skin_um']:g} µm · NP {st['ntasks']} · {st['steps']:,} step")
    print(f'→ {a.out}/manifest.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
