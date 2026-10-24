#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② R 런 사슬 끝-끝 — 가짜 러너가 아니라 **실제 러너** (`scripts/sdcp_gain_vox015_8arm.sh`) · 실제 payload · 아주 작은 픽스처 킷
(CPU · GPU 없음 · 2026-10-20 Z3).  사슬 (`scripts/rint_r_chain.py --stage ladder`) 을 프로세스 안에서 부르고, 사슬이 러너를 부른다.

정본 = 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` §3-1 (바닥 R_j → ∞ · 천장 R_j → 0) · §3-2 (사다리) ·
§3-3 (origin arm 1 · 2) · §10 (명령 꼴 · 멈춤) · 설계 v1 §3 – §7.  픽스처 = `test_ca_ext_b6` · `test_ca_ext_runner` 꼴 (킷 run_mpm.sh 의 payload 줄 ·
가짜 python3 = 규율 관문 둘만 건너뛴다 · payload 는 진짜로 돈다) 을 **생산 단위** (vox 0.15 µm · 섬유 Ø0.15 · `um_box_um` 으로 1.5 µm 상자)
로 줄였다 — 사슬이 등록 값 (VOX 0.15 · BRIDGE 0.48 · SDCP 구 Ø0.30 · face_alpha · σ 고정 셋 · bulk 1e4) 을 그대로 쓴다.

  python3 scripts/test_rint_r_chain_e2e.py            # 전부 (실제 러너 수십 회 · 수 분)
  python3 scripts/test_rint_r_chain_e2e.py --keep     # 임시 폴더를 남긴다 (팔 JSON · 러너 로그를 본다)

묶음:
  E1  사다리 P0 (SBE 픽스처) — 바닥 (`CJUNC_RJ=inf`) → 천장 (`0`) → 사다리 점 (1e4 · 1e6 · 1e8 · …) 이 실제 러너로 rc 0 · 정본 계약
      (`ca_ext_record_ok` · `check_arm` · 수렴 증서) 통과 · 등록 결과 이름으로 끝남 (STOPPED 아님)
  E2  극한 런 기록 — 바닥 · 천장 팔의 protocol 표지 (`rj_limit` inf · zero · R_j null · 0.0 · quantitative False) · 영수증 요청 같은 꼴 ·
      접합 원장 수 (바닥 = 간선 0 · 극한 instance · 천장 = 축약)
  E3  σ 순서 (같은 그래프 · Rayleigh) — 바닥 < 사다리 점 (R_j 가 작을수록 높다) < 천장 · 팔 JSON 에서 직접 (사슬은 화면에 안 쓴다)
  E4  off 격자 sid 지문 = 접합 원장 sid · 같은 origin 런끼리 같은 지문 · CG 반복 수 기록 (주 · 이어 풀기)
  E5  origin 검사 (CALIBRATED 일 때) — ARM_LIST=1,2 한 런 · 팔 a1 · a2 만 · 영수증 arm_list
  E7  값 봉인 (실물) — 사슬 화면 · ladder_summary.json · 러너 로그에 팔 σ 숫자 없음 (가짜 러너 시험 X01 의 실물 짝)
  E6  (현재 꼴 기록) 생산 킷 꼴 payload 줄 (`--joule-heat` · `--save-step4-grid` — `mpm_input_from_case.py` 이 늘 싣는다) = 다음 세대 런
      거부 (payload 입구 JOULE · STEP4_GRID) → 사슬 RUNNER_RC (fail-closed) — 실제 런을 막는 것.  고치면 이 검사를 바꾼다.
  E8  ★ 3판 (10-21 · 등록 R §5-0) 바닥 VALID_ZERO_TOPOLOGY (실물) — AM 이 판에 안 닿는 침대 (접합을 끊으면 두 판을 잇는 성분이 없다) ·
      실제 payload 의 조기 반환 해 (σ 0 · 상태 증서) 가 정본 계약 · 사슬을 지나 사다리가 계속된다 (2판 = ARM_UNREADABLE · NOT_COMPUTED)
  E9  ★ 4판 (10-21 · 1저자 Q1 · 등록 R 4판 §5-0 ① ② · R4-Q5) 천장 ELECTRODE_SHORT (실물) — 두 층 엇갈림 침대 (`make_bed_thin_cross`) ·
      실제 payload 의 J11 단락 기록 (σ None · 증서 ELECTRODE_SHORT) 이 정본 check_arm 을 지나 러너 rc 0 · 사슬 = NOT_COMPUTED (사유
      ELECTRODE_SHORT · 천장 런) — RUNNER_RC · CA_EXT_RECORD 로 흐려지지 않는다 (3판 = σ +∞ 로 받아 사다리를 계속했다)
  ★ 3판 — 계획 `rint-r-plan-v2` (결과 전 등록 숫자 넷 = 시험 값) · S0 계획 (`ca_s0_census.make_plan` · 정준 바이트) · 등록 사본 두 줄 · `--s0-plan`
⚠ PASS 는 사슬 · 러너 · payload 배선이 실물로 이어진다는 증거이지 R_j 값 · 판정의 물리 검증이 아니다 (픽스처 σ 는 의미 없다).
"""
import argparse
import contextlib
import glob
import hashlib
import io
import json
import os
import re
import shutil
import sys
import tempfile
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)
RUNNER = os.path.join(SCRIPTS, 'sdcp_gain_vox015_8arm.sh')
REG_DOC = os.path.join(ROOT, 'docs', 'reviews', 'rint_carbon_additive_registration_R_draft_20261020.md')

import rint_r_chain as RR                                  # noqa: E402
import test_ca_ext_runner as TR                           # noqa: E402 — 가짜 python3 (규율 관문 둘만 건너뛴다) · 사본 없음

SBE_KIT, DBE_KIT = RR.SBE_KIT, RR.DBE_KIT
VOX = 0.15
L_LAT = 1.5                                                # µm — 상자 옆 길이 (vox 0.15 에서 10 칸)
SW0, FLOOR, WIDTH = 0.04, 0.05, 0.92                       # 뷰어 상자 규약 (`viz_mpm_continuum` SW · FLOOR) — payload 가 µm 로 바꾼다
UM = L_LAT / WIDTH                                         # µm per 상자 단위 (`--metrics-json` 의 um_box_um)
FX_XY = 1.08                                               # µm — 섬유 x · y (셀 경계에서 떨어지게: 1.08/0.15 = 7.2 · 이동 7.7)
Z_J = 0.78                                                 # µm — 접합 (섬유 A 위 끝 = 섬유 B 아래 끝 · 5.2 · 이동 5.7)

KIT_SH = r'''#!/usr/bin/env bash
# 시험 킷 (Rint ② Z3 사슬 끝-끝) — 생산 킷의 payload 호출부 꼴 (python3 … mpm_webapp_payload … --out mpm_payload.json) · 생산 단위 1.5 µm 상자
python3 "$SCR/mpm_webapp_payload.py" --scaffold am.csv --se se.npy --phase phase.npy --fibre fibre.npy \
  --fibre-dia fibre_dia.npy --metrics-json box.json --n-vox 24 "${PSIG[@]}" \
  --out mpm_payload.json
'''
#: 생산 킷 꼴 (`scripts/mpm_input_from_case.py` 의 payload 줄에서 이 시험에 걸리는 두 플래그) — E6
KIT_SH_PROD = KIT_SH.replace('--n-vox 24 "${PSIG[@]}"', '--n-vox 24 --joule-heat "${PSIG[@]}" --save-step4-grid step4_grid.npz')

ARGS = None
TD = None
_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({str(why)[:900]})' if why != '' else ''))
    return bool(cond)


# ═════════════════════════ 픽스처 (생산 단위 · 1.5 µm 상자) ═════════════════════════
def _box(P_um):
    P = np.asarray(P_um, np.float64).reshape(-1, 3)
    return np.column_stack([SW0 + P[:, 0] / UM, SW0 + P[:, 1] / UM, FLOOR + P[:, 2] / UM])


def _line(a, b, step=0.03):
    a, b = np.asarray(a, np.float64), np.asarray(b, np.float64)
    n = max(2, int(np.ceil(np.linalg.norm(b - a) / step)) + 1)
    return a[None] + np.linspace(0.0, 1.0, n)[:, None] * (b - a)[None]


def make_bed(d, sdcp=False, am_floating=False):
    """AM_S 기둥 (r 0.3 µm 구 셋 · 겹침 = 아래 판 ↔ 위 판 우회로 · 바닥 σ 의 몫) + SE 격자점 + **세로 VGCF 두 가닥이 Z_J 에서 끝을 맞댄다**
    (아래 판 ↔ 접합 ↔ 위 판 = 직렬 · 접합 instance 하나) + PTFE 줄 하나 (AM 목을 가로지른다 · face_alpha 행 > 0) + (sdcp) SDCP 점 하나.
    ★ 3판 — am_floating = AM 구 둘이 판에 안 닿는다 (가운데 · r 0.15 µm) → 바닥 (R_j → ∞) 에 관통 성분 없음 = VALID_ZERO_TOPOLOGY (E8)."""
    rows = ['# type,x,y,z,r  (Rint ② Z3 사슬 끝-끝 픽스처 · LIGGGHTS 단위 mm)']
    for z in ((0.6, 0.9) if am_floating else (0.3, 0.75, 1.2)):
        rows.append('2,%.9f,%.9f,%.9f,%.9f' % (0.45e-3, 0.45e-3, z * 1e-3, (0.15e-3 if am_floating else 0.3e-3)))
    with open(os.path.join(d, 'am.csv'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(rows) + '\n')
    g = np.arange(0.0375, L_LAT, 0.075)
    se = np.array([[x, y, z] for x in g for y in g for z in g], np.float64)
    blocks = [(_box(se), 1, -1, 0)]
    blocks.append((_box(_line((FX_XY, FX_XY, 0.02), (FX_XY, FX_XY, Z_J))), 2, 0, 1))        # VGCF A (아래 판 → 접합)
    blocks.append((_box(_line((FX_XY, FX_XY, Z_J), (FX_XY, FX_XY, 1.48))), 2, 1, 1))        # VGCF B (접합 → 위 판)
    blocks.append((_box(_line((0.48, 0.05, 0.555), (0.48, 1.45, 0.555))), 4, 2, 1))         # PTFE 줄 (AM 구 1 · 2 의 목 근처)
    if sdcp:
        blocks.append((_box(np.array([[FX_XY, FX_XY + 0.2, Z_J]])), 5, -1, 0))
    pts = np.vstack([b[0] for b in blocks])
    np.save(os.path.join(d, 'se.npy'), pts)
    np.save(os.path.join(d, 'phase.npy'), np.concatenate([np.full(len(b[0]), b[1], np.int32) for b in blocks]))
    np.save(os.path.join(d, 'fibre.npy'), np.concatenate([np.full(len(b[0]), b[2], np.int32) for b in blocks]))
    np.save(os.path.join(d, 'fibre_kind.npy'), np.concatenate([np.full(len(b[0]), b[3], np.int8) for b in blocks]))
    np.save(os.path.join(d, 'fibre_dia.npy'), np.ones(len(pts)))      # 상대 Ø (× 기준 0.15 µm = 생산 VGCF · 직경 보존 σ 7853.98)
    with open(os.path.join(d, 'box.json'), 'w', encoding='utf-8') as f:
        json.dump({'um_box_um': UM}, f)
    return d


THIN_UM = 0.3                                              # µm — ★ 4판 E9 단락 침대 두께 (vox 0.15 두 층)


def make_bed_thin_cross(d, sdcp=False):
    """★ 4판 (10-21 · 1저자 Q1) E9 단락 침대 — 두 층 (0–0.3 µm · vox 0.15) · VGCF A (x 방향 · 아래 층 z 0.075) 와 B (y 방향 · 위 층 z 0.225)
    가 (FX_XY, FX_XY) 기둥에서 엇갈린다 (중심선 거리 0.15 = r_A + r_B · 접합 instance 하나) · SE 격자가 두 층을 채운다 (A 기둥의 위 · B 기둥의
    아래 = 절연 고체 → A = 아래 판 접점 · B = 위 판 접점) → 천장 (R_j → 0 · 축약) = 축약 무리가 두 판에 다 닿음 = J11 단락 · 바닥 = 관통 성분
    없음.  AM = 격자에 안 찍히는 작은 구 둘 (판 · 섬유와 떨어짐) · PTFE 줄 (아래 층 · 섬유와 떨어짐) · 위 판 = metrics `thickness_um` 0.3."""
    rows = ['# type,x,y,z,r  (Rint ② 4판 E9 단락 침대 · LIGGGHTS 단위 mm)',
            '2,%.9f,%.9f,%.9f,%.9f' % (0.30e-3, 0.30e-3, 0.15e-3, 0.05e-3), '2,%.9f,%.9f,%.9f,%.9f' % (1.35e-3, 0.30e-3, 0.15e-3, 0.05e-3)]
    with open(os.path.join(d, 'am.csv'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(rows) + '\n')
    g = np.arange(0.0375, L_LAT, 0.075)
    se = np.array([[x, y, z] for x in g for y in g for z in (0.0375, 0.1125, 0.1875, 0.2625)], np.float64)
    blocks = [(_box(se), 1, -1, 0),
              (_box(_line((0.02, FX_XY, 0.075), (1.48, FX_XY, 0.075))), 2, 0, 1),     # VGCF A (아래 층 · x 방향)
              (_box(_line((FX_XY, 0.02, 0.225), (FX_XY, 1.48, 0.225))), 2, 1, 1),     # VGCF B (위 층 · y 방향)
              (_box(_line((0.05, 0.60, 0.075), (0.60, 0.60, 0.075))), 4, 2, 1)]       # PTFE 줄 (아래 층 · 섬유 · 엇갈림 · AM 과 떨어짐)
    if sdcp:
        blocks.append((_box(np.array([[0.30, 1.30, 0.225]])), 5, -1, 0))
    pts = np.vstack([b[0] for b in blocks])
    np.save(os.path.join(d, 'se.npy'), pts)
    np.save(os.path.join(d, 'phase.npy'), np.concatenate([np.full(len(b[0]), b[1], np.int32) for b in blocks]))
    np.save(os.path.join(d, 'fibre.npy'), np.concatenate([np.full(len(b[0]), b[2], np.int32) for b in blocks]))
    np.save(os.path.join(d, 'fibre_kind.npy'), np.concatenate([np.full(len(b[0]), b[3], np.int8) for b in blocks]))
    np.save(os.path.join(d, 'fibre_dia.npy'), np.ones(len(pts)))
    with open(os.path.join(d, 'box.json'), 'w', encoding='utf-8') as f:
        json.dump({'um_box_um': UM, 'thickness_um': THIN_UM}, f)
    return d


def make_root(name, kit_sh=KIT_SH, am_floating=False, thin_cross=False):
    ws = os.path.join(TD, name)
    os.makedirs(ws)
    for kit, sdcp in ((SBE_KIT, False), (DBE_KIT, True)):
        run = os.path.join(ws, kit, 'run_1')
        os.makedirs(run)
        if thin_cross:
            make_bed_thin_cross(run, sdcp=sdcp)
        else:
            make_bed(run, sdcp=sdcp, am_floating=am_floating)
        with open(os.path.join(ws, kit, 'run_mpm.sh'), 'w', encoding='utf-8') as f:
            f.write(kit_sh)
        os.symlink('run_1', os.path.join(ws, kit, 'latest_run'))
    os.makedirs(os.path.join(ws, '_shim'))
    return ws


def make_plan_and_reg():
    """★ 3판 — R 런 계획 v2 (결과 전 등록 숫자 넷 = 시험 값 · 등록 숫자 아님) · S0 단계 1 계획 (정본 make_plan · 정준 바이트) ·
    등록 사본 (| 계획 해시 | · | S0 계획 해시 | 두 줄)."""
    import ca_s0_census as S0
    plan = {'schema': 'rint-r-plan-v2', 'len_law': 'len_scaled_v0', 'unreg_law': 'cut', 's_min_um': 0.6, 'tol_ff_um': 0.05,
            'step3_rtol': 1e-12, 'p2_extra': '--step3-maxiter 60000', 'max_ladder_points': 12, 'calib_rj_ratio_max': 'none',
            'sv_cf_threshold': 2.0, 'sv_cf_scope': 'R_j0'}
    pp = os.path.join(TD, 'plan.json')
    with open(pp, 'w', encoding='utf-8') as f:
        json.dump(plan, f, indent=1, sort_keys=True)
    sha = hashlib.sha256(open(pp, 'rb').read()).hexdigest()
    _p, s0b, s0sha = S0.make_plan(0.05, S0.R_F_UM, S0.GAP_TOL_PRODUCTION, {'fixture': 'test_rint_r_chain_e2e'})
    sp = os.path.join(TD, 's0_plan.json')
    with open(sp, 'wb') as f:
        f.write(s0b)
    out = []
    for ln in open(REG_DOC, encoding='utf-8').read().splitlines():
        if ln.startswith('| 계획 해시 |') or ln.startswith('| S0 계획 해시 |'):
            cells = ln.split('|')
            cells[-2] = f' `{sha if ln.startswith("| 계획 해시 |") else s0sha}` '
            ln = '|'.join(cells)
        out.append(ln)
    rp = os.path.join(TD, 'reg_ok.md')
    with open(rp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out) + '\n')
    #  ★ PF2 B (10-22 · Q2) — S0 단계 2 보고 (가짜 · 꼴 = ca_s0_census 보고의 판정 칸) — 봉인 계획 해시 = 이 계획 둘
    #  ★ PF2 D (10-22 · PRE2-design-08) — 단계 1 · 2 보고의 census · registry 일곱 파일 지문 = 이 트리 실제 파일 (사슬 `S0_SAME_FILES` · 고치기 전 판 = 빈 목록)
    digests = [{'file': nm, 'sha256': hashlib.sha256(open(os.path.join(SCRIPTS, nm), 'rb').read()).hexdigest()}
               for nm in getattr(RR, 'S0_SAME_FILES', ())]
    code = {'git_head': 'b' * 40, 'git_dirty': False, 'file_digests': digests}
    s2 = {'schema': S0.SCHEMA, 'stage': 2, 'tool': S0.TOOL_VERSION, 'kit': {'name': DBE_KIT},
          'plan': {'sha256': s0sha, 'source': 'commit:' + 'a' * 40,
                   'r_plan': {'path': 'docs/data/rint2_s0_sbe_x/rint_r_plan.json', 'sha256': sha, 's_min_um': 0.6, 'tol_ff_um': 0.05,
                              'len_law': 'len_scaled_v0', 'unreg_law': 'cut', 'step3_rtol': 1e-12, 'checked': 'fixture'}},
          'code': code}
    s1 = {'schema': S0.SCHEMA, 'stage': 1, 'tool': S0.TOOL_VERSION, 'kit': {'name': SBE_KIT},
          'plan': {'sha256': s0sha, 'source': 'stage1_computed'}, 'code': code}
    for nm, rep in (('s0_stage2.json', s2), ('s0_stage1.json', s1)):
        with open(os.path.join(TD, nm), 'w', encoding='utf-8') as f:
            json.dump(rep, f, ensure_ascii=False, indent=1)
    return pp, sp, rp


def s0_args():
    """★ PF2 B · D — 사다리 인자에 S0 단계 2 · 1 보고 (사슬이 그 인자를 알 때만 · 고치기 전 판 = 옛 꼴)."""
    out = []
    for opt, nm in (('--s0-stage2-report', 's0_stage2.json'), ('--s0-stage1-report', 's0_stage1.json')):
        if opt in RR.main.__code__.co_consts:
            out += [opt, os.path.join(TD, nm)]
    return out


@contextlib.contextmanager
def chain_env(ws):
    """사슬 프로세스 env — 가짜 python3 (PATH 맨 앞) · 그 기록 폴더 · venv 끔 (러너 시험과 같은 꼴) · 러너 축 이름꼴은 걷어낸다."""
    keep = {k: os.environ.get(k) for k in list(os.environ)}
    try:
        for k in list(os.environ):
            if k.startswith(TR._AXIS_PREFIX) or k in TR._AXIS_EXACT:
                os.environ.pop(k)
        os.environ.update(PATH=TR.SHIMDIR + os.pathsep + keep.get('PATH', '/usr/bin:/bin'), MPM_NO_VENV='1',
                          PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', PYTHONIOENCODING='utf-8',
                          SHIM_LOG=os.path.join(ws, '_shim'))
        yield
    finally:
        os.environ.clear()
        os.environ.update({k: v for k, v in keep.items() if v is not None})


def run_ladder(ws, out, law='P0', max_hours='0.5'):
    pp, sp, rp = make_plan_and_reg()
    argv = ['--stage', 'ladder', '--law', law, '--target', str(RR.TARGET_SBE_MS), '--runner', RUNNER, '--root', ws, '--plan', pp,
            '--s0-plan', sp, '--registration', rp, '--max-hours', max_hours, '--out', out] + s0_args()
    buf = io.StringIO()
    t0 = time.time()
    had = hasattr(RR, 'EXPECT_BACKEND')
    old_bk = getattr(RR, 'EXPECT_BACKEND', None)
    RR.EXPECT_BACKEND = 'cpu'                              # GPU 없음 — 사슬이 러너 env · 정본 check_arm 에 같은 값을 넘긴다
    #  ★ PF2 D — 사슬 git 신원 = 진짜 HEAD · dirty False (고쳐진 작업 트리에서 돌려도 배선 시험이 dirty 로 멈추지 않게 · dirty 판정 자체 =
    #    가짜 러너 시험 D03 · D04 · D12) · 코드 파일 지문 = 실제 파일 (그대로)
    old_gi = RR.git_identity
    RR.git_identity = lambda path, _g=old_gi: dict(_g(path), dirty=False)
    try:
        with chain_env(ws), contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            try:
                rc = RR.main([str(a) for a in argv])
            except SystemExit as e:
                rc = e.code if isinstance(e.code, int) else 2
    finally:
        RR.git_identity = old_gi
        if had:
            RR.EXPECT_BACKEND = old_bk
        else:
            del RR.EXPECT_BACKEND
    sp = os.path.join(out, 'ladder_summary.json')
    s = json.load(open(sp, encoding='utf-8')) if os.path.exists(sp) else None
    return {'rc': rc, 'so': buf.getvalue(), 'sum': s, 'out': out, 'seconds': time.time() - t0}


def arm_doc(out, run, i=0):
    p = os.path.join(out, run['outdir'], run['arms_read'][i]['file'])
    d = json.load(open(p, encoding='utf-8'))
    s3 = d['mpm_metrics']['step3']
    return s3, s3['manifest'], json.load(open(os.path.join(out, run['outdir'], 'run_receipt.json'), encoding='utf-8'))


# ═════════════════════════ 시험 ═════════════════════════
def t_ladder():
    ws = make_root('e1')
    out = os.path.join(TD, 'runs', 'e1_P0')
    r = run_ladder(ws, out)
    s = r['sum'] or {}
    runs = s.get('runs') or []
    roles = [x.get('role') for x in runs]
    print(f'    보고 E1 — 사슬 rc {r["rc"]} · 상태 {s.get("status")} · 런 {len(runs)} ({roles}) · {r["seconds"]:.0f} s · '
          f'멈춤 {(s.get("stop") or {}).get("code")}')
    stop = (s.get('stop') or {})
    chk('E1a 실제 러너 — 바닥 · 천장 · 사다리 점 하나 이상이 rc 0 · 팔 계약 (정본 ca_ext_record_ok · check_arm · 수렴 증서) 통과',
        len(runs) >= 3 and roles[:3] == ['floor', 'ceiling', 'point'] and all(x.get('rc') == 0 and x.get('arms_read') for x in runs[:3]),
        (r['rc'], roles, stop, r['so'][-1500:]))
    chk('E1b 사다리가 등록 결과 이름으로 끝난다 (STOPPED · 계약 · 러너 멈춤 아님)',
        s.get('status') in RR.REGISTERED_OUTCOMES | {'CALIBRATED'} and stop.get('code') not in (
            'RUNNER_RC', 'ARM_CONTRACT', 'CA_EXT_RECORD', 'MANIFEST_MISMATCH', 'GENERATION', 'SID_GRID', 'RECEIPT_LEAN',
            'ARM_JSON_COUNT', 'ARM_UNREADABLE', 'TIME_LIMIT'), (s.get('status'), stop))
    if len(runs) < 2:
        return
    #  ── E2 극한 런 기록 ──
    got = []
    for run, lim, R in ((runs[0], 'inf', None), (runs[1], 'zero', 0.0)):
        s3, m, rc = arm_doc(out, run)
        cj = m['ca_ext']['cjunc']
        p, cnt = cj['protocol'], cj['evidence']['counts']
        rq = rc['ca_ext_request']['cjunc']
        got.append((p.get('rj_limit') == lim and p.get('R_j_ohm') == R and (R is not None or p.get('R_j_ohm') is None)
                    and p.get('quantitative') is False and p.get('allow_rj_limits') is True and rq.get('rj_limit') == lim
                    and rq.get('R_j_ohm') == R, cnt))
    c_f, c_c = got[0][1], got[1][1]
    chk('E2a 바닥 · 천장 팔 — protocol 표지 inf · zero (R_j null · 0.0 · quantitative False · allow_rj_limits True) · 영수증 요청 같은 꼴',
        got[0][0] and got[1][0], got)
    chk('E2b 원장 수 — 바닥 = 접합 간선 0 · 극한 instance = instance 수 · 천장 = 간선 0 · 축약 = instance 수 (S3 c 0 · 몫 0)',
        c_f.get('n_instances', 0) >= 1 and c_f.get('n_edge') == 0 and c_f.get('n_none_inf') == c_f.get('n_instances')
        and c_c.get('n_edge') == 0 and c_c.get('n_contract') == c_c.get('n_instances') and c_c.get('n_contracted_by_c') == 0,
        (c_f, c_c))
    #  ── E3 σ 순서 (팔 JSON 직접 · 같은 그래프) ──
    sig = {}
    for run in runs:
        if run.get('rc') == 0 and run.get('arms_read') and run.get('arm_list') is None and run.get('arms') == 1:
            sig[run['rj']] = arm_doc(out, run)[0]['sigma_e_eff_S_cm']
    fin = sorted((float(k), v) for k, v in sig.items() if k not in ('inf', '0'))
    order_ok = ('inf' in sig and '0' in sig and fin and sig['inf'] < min(v for _k, v in fin) and max(v for _k, v in fin) < sig['0']
                and all(a[1] >= b[1] * (1 - 1e-9) for a, b in zip(fin, fin[1:])))
    print(f'    보고 E3 (픽스처 · 의미 없음) — 바닥 {sig.get("inf")!r} · 천장 {sig.get("0")!r} · 점 {fin} S/cm · 표적 {RR.TARGET_SBE_MS} mS/cm')
    chk('E3 σ 순서 — 바닥 < 사다리 점 (R_j 가 작을수록 높다) < 천장 (같은 그래프 · Rayleigh)', order_ok, (sig,))
    #  ── E4 sid · 반복 수 ──
    sids, iters = {}, []
    ok_off = True
    for run in runs:
        for j, a in enumerate(run.get('arms_read') or []):
            s3, m, _rc = arm_doc(out, run, j)
            fpo = m['ca_ext']['ptfe_face']['evidence']['fp'].get('sid_off')
            fpc = m['ca_ext']['cjunc']['evidence']['fp'].get('sid')
            ok_off &= isinstance(fpc, str) and fpc == fpo == a.get('sid_fp')
            sids.setdefault(a['index'], set()).add(fpc)
            iters.append((a.get('cg_iters'), a.get('resolve_iters'), s3.get('cg_iters'), (s3.get('conv_cert') or {}).get('iters')))
    chk('E4a off 격자 sid 지문 = 접합 원장 sid = 사슬 기록 (팔마다) · 같은 origin 런끼리 한 지문', ok_off and all(len(v) == 1 for v in sids.values()),
        {k: sorted(v) for k, v in sids.items()})
    chk('E4b CG 반복 수 — 사슬 공개 기록 = 팔 step3.cg_iters = 증서 iters (int ≥ 1) · 이어 풀기 반복 수 int ≥ 0',
        iters and all(type(a) is int and a >= 1 and a == c == d and type(b) is int and b >= 0 for a, b, c, d in iters), iters[:4])
    #  ── E7 값 봉인 (실물) — 사슬 화면 · 요약 · 러너 로그에 팔 σ 숫자가 없다 (가짜 러너 시험 X01 의 실물 짝) ──
    from test_rint_r_chain import leaks
    vals = []
    for run in runs:
        for j, _a in enumerate(run.get('arms_read') or []):
            s3 = arm_doc(out, run, j)[0]
            cert = s3.get('conv_cert') or {}
            vals += [float(x) for x in (s3.get('sigma_e_eff_S_cm'), cert.get('sigma'), cert.get('sigma_resolve'))
                     if isinstance(x, (int, float)) and not isinstance(x, bool)]
    texts = [r['so'], open(os.path.join(out, 'ladder_summary.json'), encoding='utf-8').read()]
    texts += [open(p, encoding='utf-8', errors='replace').read() for p in sorted(glob.glob(os.path.join(out, 'logs', '*.log')))]
    bad = leaks('\n'.join(texts), vals)
    chk('E7 값 봉인 (실물) — 사슬 화면 · ladder_summary.json · 러너 로그에 팔 σ (결과 · 증서 · 이어 풀기) 숫자 없음', len(vals) >= 3 and not bad,
        (len(vals), bad[:6]))
    #  ── E5 origin ──
    org = [x for x in runs if x.get('role') == 'origin']
    if s.get('status') == 'CALIBRATED':
        ok = (len(org) == 1 and org[0].get('arm_list') == [1, 2] and [a['index'] for a in org[0].get('arms_read') or []] == [1, 2]
              and arm_doc(out, org[0])[2].get('arm_list') == [1, 2] and org[0]['outdir'].endswith('_arm2_arml1-2'))
        chk('E5 origin 검사 — ARM_LIST=1,2 한 런 · 팔 a1 · a2 만 · 영수증 arm_list [1, 2] · OUTDIR 접미사 _arm2_arml1-2', ok,
            [(x.get('arm_list'), x.get('outdir')) for x in org])
    else:
        print(f'    E5 건너뜀 — 사다리 상태 {s.get("status")} (origin 검사는 CALIBRATED 뒤에만 · 픽스처 σ 가 표적을 안 끼면 정상)')


def t_zero_floor():
    ws = make_root('e8', am_floating=True)
    out = os.path.join(TD, 'runs', 'e8_P0')
    r = run_ladder(ws, out)
    s = r['sum'] or {}
    runs = s.get('runs') or []
    roles = [x.get('role') for x in runs]
    stop = s.get('stop') or {}
    print(f'    보고 E8 — 사슬 rc {r["rc"]} · 상태 {s.get("status")} · 런 {len(runs)} ({roles}) · {r["seconds"]:.0f} s · 멈춤 {stop.get("code")} · '
          f'상태 기록 {(s.get("ladder") or {}).get("states")}')
    f0 = (runs[0].get('arms_read') or [{}])[0] if runs else {}
    chk('E8a 바닥 (CJUNC_RJ=inf · AM 이 판에 안 닿음) = 실제 payload 조기 반환 해 → 팔 상태 zero (σ 0 · 증서 VALID_ZERO_TOPOLOGY) · 정본 계약 통과 · '
        '사슬이 받아 다음 런 (천장) 으로',
        len(runs) >= 2 and roles[:2] == ['floor', 'ceiling'] and runs[0].get('rc') == 0 and f0.get('state') == 'zero',
        (r['rc'], roles, f0, stop, r['so'][-1500:]))
    if runs and runs[0].get('arms_read'):
        s3, m, _rc = arm_doc(out, runs[0])
        cc = s3.get('conv_cert') or {}
        chk('E8b 바닥 팔 — σ 정확히 0.0 · 증서 상태 VALID_ZERO_TOPOLOGY · 출처 early_return · 사유 = 결과 사유 (영값 위상) · 전자 not_solvable',
            s3.get('sigma_e_eff_S_cm') == 0.0 and cc.get('status') == 'VALID_ZERO_TOPOLOGY' and cc.get('zero_source') == 'early_return'
            and cc.get('reason') == s3.get('reason') and ((m.get('components') or {}).get('electronic') or {}).get('status') == 'not_solvable',
            (s3.get('sigma_e_eff_S_cm'), cc.get('status'), cc.get('zero_source'), s3.get('reason')))
    chk('E8c 사다리가 등록 결과 이름으로 끝난다 · 바닥에서 멈추지 않는다 (ARM_UNREADABLE · NOT_COMPUTED · 계약 · 러너 멈춤 아님)',
        s.get('status') in RR.REGISTERED_OUTCOMES | {'CALIBRATED'} and stop.get('run') != (runs[0].get('name') if runs else None)
        and stop.get('code') not in ('RUNNER_RC', 'ARM_CONTRACT', 'CA_EXT_RECORD', 'MANIFEST_MISMATCH', 'GENERATION', 'SID_GRID',
                                     'RECEIPT_LEAN', 'ARM_JSON_COUNT', 'ARM_UNREADABLE', 'TIME_LIMIT'), (s.get('status'), stop))


def t_short_ceiling():
    """★ 4판 (10-21 · 1저자 Q1 "권고대로" · 등록 R 4판 §5-0 ① ② · R4-Q5) — 천장 단락 실물: 실제 payload 가 J11 단락 기록 (σ None · 증서
    ELECTRODE_SHORT) 을 쓰고 · 실제 러너가 정본 check_arm 을 지나 옮기고 (rc 0) · 사슬이 그 런을 NOT_COMPUTED (사유 ELECTRODE_SHORT) 로 끝낸다 —
    RUNNER_RC · CA_EXT_RECORD · ARM_CONTRACT 같은 다른 멈춤 이름으로 흐려지지 않는다 · 사다리는 천장에서 멈춘다 (σ +∞ 로 계속하지 않는다)."""
    ws = make_root('e9', thin_cross=True)
    out = os.path.join(TD, 'runs', 'e9_P0')
    r = run_ladder(ws, out)
    s = r['sum'] or {}
    runs = s.get('runs') or []
    roles = [x.get('role') for x in runs]
    stop = s.get('stop') or {}
    print(f'    보고 E9 — 사슬 rc {r["rc"]} · 상태 {s.get("status")} · 런 {len(runs)} ({roles}) · {r["seconds"]:.0f} s · 멈춤 {stop.get("code")} · '
          f'사유 {stop.get("reason")} · 런 {stop.get("run")}')
    chk('E9a 바닥 (R_j → ∞) = 실제 payload 영값 위상 (팔 상태 zero) · 천장 (R_j → 0) 런 = 러너 rc 0 (정본 check_arm 이 단락 기록을 받아 옮겼다) · '
        '런 둘에서 멈춤',
        roles == ['floor', 'ceiling'] and runs[0].get('rc') == 0 and runs[1].get('rc') == 0
        and ((runs[0].get('arms_read') or [{}])[0]).get('state') == 'zero' and bool(runs[1].get('arms_read')),
        (r['rc'], roles, [x.get('rc') for x in runs], stop, r['so'][-1500:]))
    chk('E9b 사다리 = 등록 결과 NOT_COMPUTED · 멈춤 코드 NOT_COMPUTED · 사유 ELECTRODE_SHORT · 멈춘 런 = 천장 (RUNNER_RC · CA_EXT_RECORD · '
        'ARM_CONTRACT · MANIFEST_MISMATCH 아님) · rc 3',
        r['rc'] == 3 and s.get('status') == 'NOT_COMPUTED' and stop.get('code') == 'NOT_COMPUTED' and stop.get('reason') == 'ELECTRODE_SHORT'
        and len(runs) == 2 and stop.get('run') == runs[1].get('name'), (r['rc'], s.get('status'), stop))
    if len(runs) >= 2 and runs[1].get('arms_read'):
        s3, m, _rc = arm_doc(out, runs[1])
        cc = s3.get('conv_cert') or {}
        cnt = ((m.get('ca_ext') or {}).get('cjunc') or {}).get('evidence', {}).get('counts') or {}
        chk('E9c 천장 팔 (실물) — σ None · 사유 cjunc_electrode_short · 증서 ELECTRODE_SHORT (early_return · ok False) · 축약 instance ≥ 1 · '
            '전자 not_solvable',
            'sigma_e_eff_S_cm' in s3 and s3.get('sigma_e_eff_S_cm') is None and str(s3.get('reason', '')).startswith('cjunc_electrode_short')
            and cc.get('status') == 'ELECTRODE_SHORT' and cc.get('zero_source') == 'early_return' and cc.get('ok') is False
            and (cnt.get('n_contract') or 0) >= 1 and ((m.get('components') or {}).get('electronic') or {}).get('status') == 'not_solvable',
            (s3.get('sigma_e_eff_S_cm'), s3.get('reason'), cc.get('status'), cnt))


def t_prod_form():
    ws = make_root('e6', kit_sh=KIT_SH_PROD)
    out = os.path.join(TD, 'runs', 'e6_P0')
    r = run_ladder(ws, out)
    s = r['sum'] or {}
    runs = s.get('runs') or []
    logs = ''.join(open(p, encoding='utf-8', errors='replace').read()
                   for p in sorted(glob.glob(os.path.join(out, 'logs', '*.log'))))
    hit = sorted(set(re.findall(r'S[12]_(?:CJUNC|FACE_ALPHA)_REFUSED\|(JOULE|STEP4_GRID)\|', logs)))
    print(f'    보고 E6 — 사슬 rc {r["rc"]} · 상태 {s.get("status")} · 멈춤 {(s.get("stop") or {}).get("code")} · 런 {len(runs)} · '
          f'payload 거부 사유 {hit}')
    chk('E6 (현재 꼴 기록) 생산 킷 꼴 payload 줄 (--joule-heat · --save-step4-grid) = 첫 런 (바닥) 에서 payload 입구 거부 (JOULE · STEP4_GRID) → '
        '러너 rc ≠ 0 → 사슬 RUNNER_RC (fail-closed · 팔 없음) — 실제 런을 막는 것',
        r['rc'] == 3 and (s.get('stop') or {}).get('code') == 'RUNNER_RC' and len(runs) == 1 and set(hit) >= {'JOULE', 'STEP4_GRID'},
        (r['rc'], s.get('stop'), hit, logs[-800:]))


def main():
    global ARGS, TD
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--keep', action='store_true')
    ap.add_argument('--only', default='', help='E1 · E6 (쉼표)')
    ARGS = ap.parse_args()
    TD = tempfile.mkdtemp(prefix='rint_r_chain_e2e_')
    TR.TD = os.path.join(TD, 'tr')
    os.makedirs(TR.TD)
    TR.SHIMDIR = os.path.join(TR.TD, '_bin')
    os.makedirs(TR.SHIMDIR)
    with open(os.path.join(TR.SHIMDIR, 'python3'), 'w', encoding='utf-8') as f:
        f.write(TR.SHIM.replace('__REAL__', os.path.abspath(sys.executable)))   # realpath = venv 밖 (kgy dem-venv · 10-24)
    os.chmod(os.path.join(TR.SHIMDIR, 'python3'), 0o755)
    t0 = time.time()
    sel = [x for x in ARGS.only.split(',') if x]
    try:
        for tag, fn in (('E1', t_ladder), ('E6', t_prod_form), ('E8', t_zero_floor), ('E9', t_short_ceiling)):
            if sel and tag not in sel:
                continue
            print(f'\n── {tag}')
            try:
                fn()
            except Exception as e:                         # noqa: BLE001 — 시험 안의 예외 = 그 묶음 실패
                import traceback
                chk(f'{tag} 예외 없이', False, f'{type(e).__name__}: {e} @ {traceback.format_exc().splitlines()[-3].strip()[:300]}')
    finally:
        if ARGS.keep:
            print(f'  (임시 폴더 남김: {TD})')
        else:
            shutil.rmtree(TD, ignore_errors=True)
    print(f'\ntest_rint_r_chain_e2e: {_ok} PASS · {len(_fail)} FAIL ({time.time() - t0:.1f} s)')
    for n in _fail:
        print(f'  - {n}')
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
