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
      (`ca_ext_record_ok` · `check_arm` · 수렴 증서) 통과 · 등록 결과 이름으로 끝남 (STOPPED 아님) · ★ 10-25 묶음 B (RCA2-02) E1c — 사슬 ·
      실제 러너 = git 고정물 체크아웃 (진짜 git 신원) · 사다리 뒤 체크아웃 git status 빈칸 · 요약 code = 깨끗 · 저장소 상대 경로 · 환경 지문
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
  E10 ★ 10-25 묶음 B (X6) 봉인 SV census (실제 S0 함수) = 실제 DBE SV 런의 census · 바꾼 봉인 = S0_REPORT_MISMATCH
  E11 ★ 10-26 B″ (Q4) 사슬이 러너에 MPM_NO_VENV=1 (러너 자리 미끼 venv 를 켜지 않음 · payload 환경 단위 = 사슬 환경 지문)
  E12 ★ 10-26 B″ (Q1 (가)) 생산 봉인 원천 실물 — DBE SV 모서리 + `RunnerGraphSource` (러너 조립만) → 귀속 verified · 주 계 지문 바꾼 꼴 =
      CA_EXT_RECORD · 환경 단위 다름 = 미확인 · 결합 칸 다름 = 원천 실패 · 비용 보고 (원천 런 초 · STEP3 · 조립 초 · 최대 RSS)
  E13 ★ 10-27 묶음 C2b 실물 kill — 러너만 SIGKILL (표지 앞 · 뒤) · 시간 초과 · 사슬 부모 SIGKILL (표지 앞 · 뒤) + --stage recover
  E14 ★ 10-27 묶음 C1b 실물 원장 시도 — --init · --add · 사다리 시도 → 결과 줄 · 폴더 요약 sha (독립 계산) · 런마다 표지
  E15 ★ 10-27 묶음 C1b-2 실물 재실행 — 바닥 런 표지 뒤 사슬 부모 SIGKILL → recover --ledger → --add --resume → 재실행 시도 → CALIBRATED
  E17 ★ 10-28 밤 PC5 §4 #5 시험 고정물 등록 사본 — 계획 숫자 블록 = §2-1 자리 · 표지 각 하나 · 봉인된 등록의 사본도 하나 (러너 없음 · 빠름)
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
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)
REG_DOC = os.path.join(ROOT, 'docs', 'reviews', 'rint_carbon_additive_registration_R_draft_20261020.md')

import rint_r_chain as RR                                  # noqa: E402
import test_ca_ext_runner as TR                           # noqa: E402 — 가짜 python3 (규율 관문 둘만 건너뛴다) · 사본 없음

#: ★ 10-25 묶음 B (RCA2-02 · 1저자 10-23 Q2 (가) (가-1)) — 사슬 · 실제 러너 = git 고정물 저장소 (이 리포 scripts/ 사본 · 러너 관문이 읽는 사전등록
#   문서 · .gitignore · 커밋 하나 · 작업 트리 깨끗) · git 신원 = 진짜 조회 (옛 = 이 리포 HEAD + dirty False 고정 — 엄격한 git 대조 (미확인 = 멈춤 ·
#   ignore 밖 untracked = dirty) 뒤에는 고쳐진 작업 트리에서 시험할 수 없다 → 고정물로 옮겼다 · 검사는 약하게 하지 않는다) · F5 계획 커밋 = 같은
#   저장소의 떠 있는 커밋
CODEREPO = {}
R_PLAN_REL = 'docs/data/rint2_s0_sbe_x/rint_r_plan.json'
PREREG_REL = 'docs/reviews/sdcp_gain_prereg_v2_20260816.md'      # 러너 관문 ($SCR/../docs/…) 이 읽는 문서
GIT_CFG = ('-c', 'user.email=t@t', '-c', 'user.name=t', '-c', 'commit.gpgsign=false', '-c', 'init.defaultBranch=main')


def _git(repo, *a, inp=None, env=None):
    r = subprocess.run(['git', '-C', str(repo), *GIT_CFG, *a], input=inp, capture_output=True, env=env)
    if r.returncode != 0:
        raise RuntimeError(f'git {a[:2]} rc {r.returncode}: {r.stderr.decode("utf-8", "replace")[:300]}')
    return r.stdout.decode('utf-8', 'replace').strip()


def code_repo():
    """git 고정물 저장소 (한 번) → scripts 폴더 (사슬 폴더 = RR.HERE · 러너 = 그 안 실제 러너)."""
    if 'sd' not in CODEREPO:
        repo = os.path.join(TD, 'coderepo')
        shutil.copytree(SCRIPTS, os.path.join(repo, 'scripts'), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        os.makedirs(os.path.join(repo, os.path.dirname(PREREG_REL)))
        shutil.copy2(os.path.join(ROOT, PREREG_REL), os.path.join(repo, PREREG_REL))
        shutil.copy2(os.path.join(ROOT, '.gitignore'), os.path.join(repo, '.gitignore'))
        _git(repo, 'init', '-q')
        _git(repo, 'add', '-A')
        _git(repo, 'commit', '-q', '-m', 'fixture')
        CODEREPO.update(repo=repo, sd=os.path.join(repo, 'scripts'))
    return CODEREPO['sd']


def plan_commit(pb):
    """F5 (판정문 §9) — R 계획 바이트를 R_PLAN_REL 에 담은 커밋 (고정물 저장소의 떠 있는 커밋 · 작업 트리 · HEAD 그대로) → 40-hex."""
    key = hashlib.sha256(pb).hexdigest()
    if key not in CODEREPO:
        repo = CODEREPO['repo']
        blob = _git(repo, 'hash-object', '-w', '--stdin', inp=pb)
        idx = os.path.join(TD, f'_index_{len(CODEREPO)}')
        env = dict(os.environ, GIT_INDEX_FILE=idx)
        _git(repo, 'update-index', '--add', '--cacheinfo', f'100644,{blob},{R_PLAN_REL}', env=env)
        tree = _git(repo, 'write-tree', env=env)
        CODEREPO[key] = _git(repo, 'commit-tree', tree, '-m', 'plan (시험 F5)')
        os.unlink(idx)
    return CODEREPO[key]

SBE_KIT, DBE_KIT = RR.SBE_KIT, RR.DBE_KIT
VOX = 0.15
L_LAT = 1.5                                                # µm — 상자 옆 길이 (vox 0.15 에서 10 칸)
SW0, FLOOR, WIDTH = 0.04, 0.05, 0.92                       # 뷰어 상자 규약 (`viz_mpm_continuum` SW · FLOOR) — payload 가 µm 로 바꾼다
UM = L_LAT / WIDTH                                         # µm per 상자 단위 (`--metrics-json` 의 um_box_um)
FX_XY = 1.08                                               # µm — 섬유 x · y (셀 경계에서 떨어지게: 1.08/0.15 = 7.2 · 이동 7.7)
Z_J = 0.78                                                 # µm — 접합 (섬유 A 위 끝 = 섬유 B 아래 끝 · 5.2 · 이동 5.7)

KIT_SH = r'''#!/usr/bin/env bash
# 시험 킷 (Rint ② Z3 사슬 끝-끝) — 생산 킷의 payload 호출부 꼴 (python3 … mpm_webapp_payload … --out mpm_payload.json) · 생산 단위 1.5 µm 상자
python3 "$SCR/mpm_webapp_payload.py" --scaffold am.csv --se se_dump.npy --phase phase.npy --fibre fibre.npy \
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
    np.save(os.path.join(d, 'se_dump.npy'), pts)       # ★ 10-25 묶음 B — S0 발견 함수 (find_run_dir) 이름 · 옛 se.npy
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
    np.save(os.path.join(d, 'se_dump.npy'), pts)       # ★ 10-25 묶음 B — S0 발견 함수 이름 · 옛 se.npy
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


def reg_text(text, sha, s0sha, plan):
    """등록 사본 글 — 해시 두 줄 (| 계획 해시 | · | S0 계획 해시 |) + ★ 10-27 묶음 C1 (판정문 C6 #30) 계획 숫자 블록 (사슬 생성기 · 정확 대조 = 사슬이 본다 ·
    생성기 꼴 자체 = test_rint_r_chain EP06).  text = 등록 R 글 (★ 10-28 밤 PC5 §4 #5 — 봉인된 글 흉내도 받는다)."""
    out = []
    for ln in text.splitlines():
        if ln.startswith('| 계획 해시 |') or ln.startswith('| S0 계획 해시 |'):
            cells = ln.split('|')
            cells[-2] = f' `{sha if ln.startswith("| 계획 해시 |") else s0sha}` '
            ln = '|'.join(cells)
        out.append(ln)
    t = '\n'.join(out) + '\n'
    if not callable(getattr(RR, 'plan_doc_block', None)):
        return t
    #  ★ 10-28 밤 PC5 봉인 전 남은 #5 — 블록 자리 = §2-1 자리 줄 ("계획 숫자 블록 = 이 줄 바로 아래") 바로 아래 (봉인 커밋과 같은 자리 · 옛 = 글 끝에
    #    덧붙임 → 봉인된 글이면 표지 둘 = PLAN_DOC_MISMATCH) · 이미 블록이 있으면 (봉인된 글) 그 블록을 바꾼다
    b, e, blk = RR.PLAN_DOC_BEGIN, RR.PLAN_DOC_END, RR.plan_doc_block(plan)
    if t.count(b) or t.count(e):
        assert t.count(b) == t.count(e) == 1 and t.index(b) < t.index(e), '등록 글의 계획 숫자 블록 표지'
        return t[:t.index(b)] + blk + t[t.index(e) + len(e):]
    lines = t.split('\n')
    hit = [i for i, ln in enumerate(lines) if '계획 숫자 블록 = 이 줄 바로 아래' in ln]
    assert len(hit) == 1, f'등록 글의 §2-1 블록 자리 줄 {len(hit)} 개'
    return '\n'.join(lines[:hit[0] + 1] + ['', blk] + lines[hit[0] + 1:])


def make_plan_and_reg(ws=None):
    """★ 3판 — R 런 계획 v2 (결과 전 등록 숫자 넷 = 시험 값 · 등록 숫자 아님) · S0 단계 1 계획 (정본 make_plan · 정준 바이트) ·
    등록 사본 (| 계획 해시 | · | S0 계획 해시 | 두 줄)."""
    import ca_s0_census as S0
    plan = {'schema': 'rint-r-plan-v2', 'len_law': 'len_scaled_v0', 'unreg_law': 'cut', 's_min_um': 0.6, 'tol_ff_um': 0.05,
            'step3_rtol': 1e-12, 'p2_extra': '--step3-maxiter 60000', 'max_ladder_points': 12, 'calib_rj_ratio_max': 'none',
            'sv_cf_threshold': 2.0, 'sv_cf_scope': 'R_j0'}
    #  ★ 10-27 묶음 C1 (RCA2-05 · author 10-27 approved bundle C) — 사슬 계획 v3 (실행 정책 칸) 이면 시험 값으로 봉인 (등록 숫자 아님 · 시간 상한 =
    #    run_ladder 의 --max-hours · 판 = 이 프로세스 환경 같음 단위 · 규칙 칸 = 사슬 이름) · 고치기 전 판 = v2 그대로
    if chain_c1():
        plan['schema'] = RR.PLAN_SCHEMA
        plan['exec_policy'] = {'max_hours': float(E2E_MAXH), 'max_attempts': 3, 'allowed_machines': ['gabia', E2E_MACH, 'v100'],
                               'env_unit': RR.env_unit(RR.env_record()), 'retry_rule': 'pre_result_only_v1',
                               'same_config': 'plan_code_bed_env_v1', 'adoption': 'first_not_pre_result_v1', 'attempt_dir': 'attempt_<n>'}
    pp = os.path.join(TD, 'plan.json')
    with open(pp, 'w', encoding='utf-8') as f:
        json.dump(plan, f, indent=1, sort_keys=True)
    sha = hashlib.sha256(open(pp, 'rb').read()).hexdigest()
    _p, s0b, s0sha = S0.make_plan(0.05, S0.R_F_UM, S0.GAP_TOL_PRODUCTION, {'fixture': 'test_rint_r_chain_e2e'})
    sp = os.path.join(TD, 's0_plan.json')
    with open(sp, 'wb') as f:
        f.write(s0b)
    rp = os.path.join(TD, 'reg_ok.md')
    with open(rp, 'w', encoding='utf-8') as f:
        f.write(reg_text(open(REG_DOC, encoding='utf-8').read(), sha, s0sha, plan))
    #  ★ PF2 B (10-22 · Q2) — S0 단계 2 보고 (가짜 · 꼴 = ca_s0_census 보고의 판정 칸) — 봉인 계획 해시 = 이 계획 둘
    #  ★ PF2 D (10-22 · PRE2-design-08) — 단계 1 · 2 보고의 census · registry 일곱 파일 지문 = 이 트리 실제 파일 (사슬 `S0_SAME_FILES` · 고치기 전 판 = 빈 목록)
    digests = [{'file': nm, 'sha256': hashlib.sha256(open(os.path.join(SCRIPTS, nm), 'rb').read()).hexdigest()}
               for nm in getattr(RR, 'S0_SAME_FILES', ())]
    code = {'git_head': 'b' * 40, 'git_dirty': False, 'file_digests': digests}
    #  ★ 10-25 묶음 B (F5) — 계획 출처 = 이 계획 바이트를 R_PLAN_REL 에 담은 고정물 커밋 (옛 = 'commit:' + 'a' * 40 · 커밋 없음)
    code_repo()
    s2 = {'schema': S0.SCHEMA, 'stage': 2, 'tool': S0.TOOL_VERSION, 'kit': {'name': DBE_KIT},
          'plan': {'sha256': s0sha, 'source': 'commit:' + plan_commit(open(pp, 'rb').read()),
                   'r_plan': {'path': R_PLAN_REL, 'sha256': sha, 's_min_um': 0.6, 'tol_ff_um': 0.05,
                              'len_law': 'len_scaled_v0', 'unreg_law': 'cut', 'step3_rtol': 1e-12, 'checked': 'fixture'}},
          'code': code}
    s1 = {'schema': S0.SCHEMA, 'stage': 1, 'tool': S0.TOOL_VERSION, 'kit': {'name': SBE_KIT},
          'plan': {'sha256': s0sha, 'source': 'stage1_computed'}, 'code': code}
    #  ★ 10-25 묶음 B (RCA2-03 · Q3 (가)) — 같은 침대 칸 = 실제 S0 함수 (원 입력 = kit_input_record · off 격자 지문 = 가로챈 입력의 off 격자 ·
    #    carbon_junction._grid_fp) 로 이 킷에서 (가짜 보고의 그 칸만 진짜 · 실제 러너 arm 0 sid 지문과 같아야 사다리가 돈다)
    if ws is not None:
        s1.update(s0_bed(ws, SBE_KIT))
        s2.update(s0_bed(ws, DBE_KIT))
        #  ★ 10-25 묶음 B (X6 · Q20 (가)) — 단계 2 봉인 SV census = 실제 S0 함수 (`sv_census_sealed` · 같은 격자 · R 계획의 s_min · tol_ff) ·
        #    단계 1 = null · 고치기 전 판 (함수 없음) = 칸 없음
        sv = s0_sv(ws, DBE_KIT, plan['s_min_um'], plan['tol_ff_um'])
        if sv is not None:
            s2['sv_census'] = sv
            s1['sv_census'] = None
    for nm, rep in (('s0_stage2.json', s2), ('s0_stage1.json', s1)):
        with open(os.path.join(TD, nm), 'w', encoding='utf-8') as f:
            json.dump(rep, f, ensure_ascii=False, indent=1)
    return pp, sp, rp


def s0_bed(ws, kit):
    """S0 보고의 inputs · raster 칸 — census_kit 과 같은 S0 함수 (kit_input_record · resolve_payload_argv · capture_raster_inputs ·
    _check_captured · _raster (PTFE 행 뺌 = off 격자) · carbon_junction._grid_fp) · 규약 = 사슬 고정값 (vox 0.15 · 브리지 0.48 · SDCP 구 0.30 ·
    origin 0 · 선분 스탬프).  고치기 전 판 (kit_input_record 없음) = 칸 없음.  (validate_kit_arrays 는 부르지 않는다 — 이 픽스처 metrics 에
    thickness_um 이 없다 · 사슬 대조 칸은 파일 지문 · 설정 · 격자 지문)."""
    import ca_s0_census as S0
    import carbon_junction as CJ
    key = ('bed', ws, kit)
    if key in CODEREPO:
        return CODEREPO[key]
    out = {}
    f = getattr(S0, 'kit_input_record', None)
    if not callable(f):
        CODEREPO[key] = out
        return out
    kp = os.path.join(ws, kit)
    out['inputs'] = f(kp, vox=VOX, bridge_um=0.48, sdcp_sphere_d=0.30)
    rd = S0.find_run_dir(kp)
    with tempfile.TemporaryDirectory(dir=TD) as td:
        argv = S0.resolve_payload_argv(kp, rd, td, vox=VOX, bridge_um=0.48, sdcp_sphere_d=0.30)
        kw = S0.capture_raster_inputs(argv, rd, log_path=os.path.join(td, 'cap.log'))
        S0._check_captured(kw, VOX, 0.48, 0.30)
        st = S0._s3_state()
        try:
            off, _pid = S0._raster(kw, drop=(S0.PTFE,), with_pid=True)
        finally:
            S0._s3_restore(st)
    out['raster'] = {'convention': {'vox_um': VOX, 'bridge_um': 0.48, 'sdcp_sphere_d_um': 0.30, 'ptfe_stamp_captured': 'centerline',
                                    'fibre_stamp': 'segment', 'origin_shift_um': [0.0, 0.0, 0.0], 'fid_gap_tol': float(kw['fid_gap_tol']),
                                    'off_grid': 'captured inputs minus PTFE rows (test_rint_r_chain_e2e)'},
                     'grid_shape': [int(x) for x in off.shape], 'box_lo_um': [float(x) for x in kw['box_lo']],
                     'box_hi_um': [float(x) for x in kw['box_hi']], 'cells_by_sid': {'off': S0._hist(off)},
                     'sid_off_fp': CJ._grid_fp(off)}
    CODEREPO[key] = out
    return out


def s0_sv(ws, kit, s_min_um, tol_ff_um):
    """S0 단계 2 봉인 SV census 블록 — 실제 S0 함수 (`ca_s0_census.sv_census_sealed` · 가로챈 입력 · off 격자 · 봉인 s_min · tol_ff) → dict |
    None (고치기 전 판)."""
    import ca_s0_census as S0
    f = getattr(S0, 'sv_census_sealed', None)
    if not callable(f):
        return None
    key = ('sv', ws, kit, s_min_um, tol_ff_um)
    if key in CODEREPO:
        return CODEREPO[key]
    kp = os.path.join(ws, kit)
    rd = S0.find_run_dir(kp)
    with tempfile.TemporaryDirectory(dir=TD) as td:
        argv = S0.resolve_payload_argv(kp, rd, td, vox=VOX, bridge_um=0.48, sdcp_sphere_d=0.30)
        kw = S0.capture_raster_inputs(argv, rd, log_path=os.path.join(td, 'cap.log'))
        S0._check_captured(kw, VOX, 0.48, 0.30)
        st = S0._s3_state()
        try:
            off, _pid = S0._raster(kw, drop=(S0.PTFE,), with_pid=True)
        finally:
            S0._s3_restore(st)
    CODEREPO[key] = json.loads(json.dumps(f(kw, off, s_min_um=s_min_um, tol_ff_um=tol_ff_um)))
    return CODEREPO[key]


def s0_args():
    """★ PF2 B · D — 사다리 인자에 S0 단계 2 · 1 보고 (사슬이 그 인자를 알 때만 · 고치기 전 판 = 옛 꼴)."""
    out = []
    for opt, nm in (('--s0-stage2-report', 's0_stage2.json'), ('--s0-stage1-report', 's0_stage1.json')):
        if opt in RR.main.__code__.co_consts:
            out += [opt, os.path.join(TD, nm)]
    return out


@contextlib.contextmanager
def chain_env(ws, no_venv=True):
    """사슬 프로세스 env — 가짜 python3 (PATH 맨 앞) · 그 기록 폴더 · venv 끔 (러너 시험과 같은 꼴) · 러너 축 이름꼴은 걷어낸다.
    ★ 10-26 B″ (Q4) no_venv=False = 사슬 프로세스 env 에 MPM_NO_VENV 를 두지 않는다 (VIRTUAL_ENV 도 없음 — 사슬이 러너에 주는지 보는 시험 E11)."""
    keep = {k: os.environ.get(k) for k in list(os.environ)}
    try:
        for k in list(os.environ):
            if k.startswith(TR._AXIS_PREFIX) or k in TR._AXIS_EXACT:
                os.environ.pop(k)
        os.environ.update(PATH=TR.SHIMDIR + os.pathsep + keep.get('PATH', '/usr/bin:/bin'), MPM_NO_VENV='1',
                          PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', PYTHONIOENCODING='utf-8',
                          SHIM_LOG=os.path.join(ws, '_shim'))
        if not no_venv:
            os.environ.pop('MPM_NO_VENV', None)
            os.environ.pop('VIRTUAL_ENV', None)
        yield
    finally:
        os.environ.clear()
        os.environ.update({k: v for k, v in keep.items() if v is not None})


def chain_c1():
    """★ 10-27 묶음 C1 — 사슬 계획에 실행 정책 칸이 있나 (있으면 v3 계획 · --machine · 숫자 블록)."""
    return 'exec_policy' in (getattr(RR, 'PLAN_KEYS', ()) or ())


E2E_MAXH, E2E_MACH = '0.5', 'kgy'                          # 시험 값 (등록 숫자 아님) — 계획 exec_policy.max_hours = --max-hours


def run_ladder(ws, out, law='P0', max_hours=E2E_MAXH):
    pp, sp, rp = make_plan_and_reg(ws)
    #  ★ 10-25 묶음 B — 사슬 폴더 (RR.HERE) · 러너 = git 고정물 저장소의 scripts (옛 = 이 리포 scripts + git 신원 dirty False 고정)
    sd = code_repo()
    runner = os.path.join(sd, 'sdcp_gain_vox015_8arm.sh')
    argv = ['--stage', 'ladder', '--law', law, '--target', str(RR.TARGET_SBE_MS), '--runner', runner, '--root', ws, '--plan', pp,
            '--s0-plan', sp, '--registration', rp, '--max-hours', max_hours, '--out', out] + s0_args()
    if chain_c1():
        argv += ['--machine', E2E_MACH]
    buf = io.StringIO()
    t0 = time.time()
    had = hasattr(RR, 'EXPECT_BACKEND')
    old_bk = getattr(RR, 'EXPECT_BACKEND', None)
    RR.EXPECT_BACKEND = 'cpu'                              # GPU 없음 — 사슬이 러너 env · 정본 check_arm 에 같은 값을 넘긴다
    old_here = RR.HERE
    RR.HERE = Path(sd)
    try:
        with chain_env(ws), contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            try:
                rc = RR.main([str(a) for a in argv])
            except SystemExit as e:
                rc = e.code if isinstance(e.code, int) else 2
    finally:
        RR.HERE = old_here
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
            'ARM_JSON_COUNT', 'ARM_UNREADABLE', 'TIME_LIMIT', 'CODE_PIN_MISMATCH'), (s.get('status'), stop))
    #  ── ★ 10-25 묶음 B (RCA2-02 · Q2 (가) ② (가-1)) — 실제 러너 · payload 가 체크아웃 안에 ignore 밖 파일을 만들지 않는다 (만들면 다음 단계의
    #     지금 코드 = dirty 로 멈춘다) · 요약 code = 진짜 git 신원 (깨끗 · 저장소 상대 경로 · 사슬 = 러너 HEAD) · 환경 지문 같음 단위 ──
    st = _git(CODEREPO['repo'], 'status', '--porcelain', '--untracked-files=normal')
    c = s.get('code') or {}
    ch, ru, unit = c.get('chain') or {}, c.get('runner') or {}, (c.get('env') or {}).get('unit') or {}
    chk('E1c 사다리 뒤 고정물 체크아웃 git status 빈칸 (러너 · payload 가 작업 트리 안 ignore 밖 파일을 안 만든다) · 요약 code = 깨끗 · rel = '
        'scripts/rint_r_chain.py · scripts/sdcp_gain_vox015_8arm.sh · 사슬 HEAD = 러너 HEAD · 환경 지문 단위 셋',
        st == '' and ch.get('dirty') is False and ru.get('dirty') is False and ch.get('rel') == 'scripts/rint_r_chain.py'
        and ru.get('rel') == 'scripts/sdcp_gain_vox015_8arm.sh' and ch.get('head') == ru.get('head') and len(str(ch.get('head'))) == 40
        and sorted(unit) == ['numpy', 'python_minor', 'scipy'] and all(isinstance(v, str) and v for v in unit.values()),
        (st[:300], ch, ru, unit))
    #  ── ★ 10-25 묶음 B (RCA2-03 · Q3 (가)) — 같은 침대 (실물): 사다리 요약의 침대 다시 해시 (SBE · 경로 없는 지문) = S0 단계 1 기록의 원 입력 ·
    #     실제 러너 arm 0 의 sid 지문 = S0 함수로 낸 off 격자 지문 (같은 규약 · 파생 격자 지문 대조가 실물에서 성립) ──
    rec1 = (s.get('s0_reports') or {}).get('stage1') or {}
    want = {r: {'sha256': x.get('sha256'), 'bytes': x.get('bytes')} for r, x in ((rec1.get('inputs') or {}).get('files') or {}).items()}
    bed = ((s.get('bed') or {}).get(SBE_KIT) or {})
    a0 = [a for x in runs for a in (x.get('arms_read') or []) if a.get('index') == 0]
    chk('E1d 같은 침대 (실물) — 요약 bed (SBE · 경로 없음) = S0 단계 1 기록 원 입력 · 설정 · arm 0 sid 지문 (런마다) = S0 off 격자 지문',
        bool(want) and bed.get('files') == want and bed.get('settings_sha256') == (rec1.get('inputs') or {}).get('settings_sha256')
        and a0 and all(a.get('sid_fp') == (rec1.get('raster') or {}).get('sid_off_fp') for a in a0),
        (sorted(want), bed, [a.get('sid_fp') for a in a0][:3], (rec1.get('raster') or {}).get('sid_off_fp')))
    #  ── ★ 10-27 묶음 C1 (판정문 C6 #15 · Q11 · author 10-27 approved bundle C) — 실물 사다리 요약 · 런 기록마다 기계 이름 = --machine (계획 허용
    #     목록 안 · 빈 이름 없음) · 계획 = v3 (실행 정책 칸) ──
    chk('E1m 실물 사다리 — 요약 machine · 런 기록 machine (런마다) = --machine kgy · 계획 실행 정책 봉인 (v3)',
        chain_c1() and s.get('machine') == E2E_MACH and bool(runs) and all(x.get('machine') == E2E_MACH for x in runs),
        (chain_c1(), s.get('machine'), [x.get('machine') for x in runs][:4]))
    #  ── ★ 10-27 묶음 C2b (R4-02 ⓐ ⓑ ⓒ) — 실물 그룹 기록 · 시도 꼴 (payload = 런 폴더 안 .unchecked/ → 검사 뒤 옮김 · 감싸개 표지 팔마다) ──
    gbad, ubad = [], []
    for x in runs:
        lp, ep = (os.path.join(out, 'groups', f'{x["name"]}.{k}.json') for k in ('launch', 'end'))
        er = json.load(open(ep, encoding='utf-8')) if os.path.exists(ep) else {}
        if not (os.path.exists(lp) and er.get('confirmed') is True and er.get('cause') is None and er.get('rc') == 0):
            gbad.append((x['name'], er))
        unc = os.path.join(out, x['outdir'], '.unchecked')
        marks = sorted(os.path.basename(m) for m in glob.glob(os.path.join(unc, '*.first_result.json')))
        left = [m for m in glob.glob(os.path.join(unc, 'p2_*')) if not m.endswith('.first_result.json')]
        want = sorted(a['file'] + '.first_result.json' for a in x.get('arms_read') or [])
        if not (marks == want and not left):
            ubad.append((x['name'], marks, want, left))
    kitp = glob.glob(os.path.join(ws, SBE_KIT, '*', 'p2_*.json*'))
    chk('E1g 실물 그룹 기록 — 런마다 groups/<런>.launch.json · .end.json (확인 True · 원인 None · rc 0)', bool(runs) and not gbad, gbad[:3])
    chk('E1u 실물 시도 꼴 — 런마다 .unchecked/ 의 첫 풀이 끝 표지 = 그 런의 팔마다 하나 (진짜 감싸개 · 진짜 payload) · .unchecked/ 에 payload 남지 않음 · '
        '킷 런 폴더에 payload 없음', bool(runs) and not ubad and kitp == [], (ubad[:3], kitp[:3]))
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
    #  ★ 10-27 묶음 C2b (R4-02 ⓒ) — CG 없는 조기 반환 해 (σ 0) 도 첫 풀이 끝 표지 (감싸개 solve_return 자리 · 결과 전 · 뒤 판정의 입력)
    mk = []
    if runs and runs[0].get('arms_read'):
        mk = [json.load(open(x, encoding='utf-8')) for x in glob.glob(os.path.join(out, runs[0]['outdir'], '.unchecked', '*.first_result.json'))]
    chk('E8u 바닥 조기 반환 해 (σ 0 · CG 없음) → 표지 하나 (kind solve_return · 진짜 감싸개)', len(mk) == 1 and mk[0].get('kind') == 'solve_return', mk)


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


def t_sv_census_dbe():
    """★ 10-25 묶음 B (X6 · 1저자 10-23 Q20 (가)) — 실물 (실제 러너 · payload · 합성 DBE 킷 · SDCP 있음 · CPU): S0 단계 2 봉인 SV census (실제 S0
    함수) = DBE arm 0 SV 런의 증거 census · 기록 census 사본 (모서리 둘 · 법칙 · c 다름 = 같은 census) · 사슬 read_run (S0 off 격자 지문 · 봉인 census
    대조) 통과 · 봉인 census 를 바꾼 기록이면 read_run 이 S0_REPORT_MISMATCH.  (사슬 사다리 · 예측을 다 돌리지 않는다 — 사슬 Runner 로 모서리 런만)"""
    ws = make_root('e10')
    pp, _sp, _rp = make_plan_and_reg(ws)
    plan = json.load(open(pp, encoding='utf-8'))
    if not callable(getattr(RR, 's0_census_seed', None)):
        chk('E10 사슬 s0_census_seed · S0 sv_census_sealed 가 있다 (봉인 SV census 대조)', False)
        return
    recs = {'stage2': RR.read_s0_report(os.path.join(TD, 's0_stage2.json'), 2), 'stage1': RR.read_s0_report(os.path.join(TD, 's0_stage1.json'), 1)}
    seed_g, seed_c = RR.s0_grid_seed(recs), RR.s0_census_seed(recs)
    key = RR.sid_group(DBE_KIT, None, 0)
    sd = code_repo()
    runner = os.path.join(sd, 'sdcp_gain_vox015_8arm.sh')
    out = os.path.join(TD, 'runs', 'e10')
    old_bk, old_here = RR.EXPECT_BACKEND, RR.HERE
    RR.EXPECT_BACKEND, RR.HERE = 'cpu', Path(sd)
    buf = io.StringIO()
    res, stop = [], None
    try:
        with chain_env(ws), contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            rn = RR.Runner(runner, ws, out, plan, None, time.time() + 1800, RR.RealContract(), prefix='Q')
            rn.s0_grid, rn.s0_census = seed_g, seed_c
            for law, c in (('P0', '0'), ('P1', '1')):
                res.append(rn.run(DBE_KIT, 'corner', law, c, RR.rj_key(1e6), 1, True))
            bad = {k: {kk: (vv + 1 if kk == 'n_unsplit_bridging_components' else vv) for kk, vv in v.items()} for k, v in seed_c.items()}
            rn2 = RR.Runner(runner, ws, out + '_b', plan, None, time.time() + 1800, RR.RealContract(), prefix='Q')
            rn2.s0_grid, rn2.s0_census = seed_g, bad
            try:
                rn2.run(DBE_KIT, 'corner', 'P0', '1', RR.rj_key(1e6), 1, True)
            except RR.Stop as e:
                stop = e
    except RR.Stop as e:
        chk('E10 실물 DBE SV 모서리 둘이 사슬 read_run 을 지난다', False, f'{e.code}: {e.cause} · {buf.getvalue()[-600:]}')
        return
    finally:
        RR.EXPECT_BACKEND, RR.HERE = old_bk, old_here
    sealed = (recs['stage2'].get('sv_census') or {}).get('census')
    evs = []
    for r in rn.records:
        d = json.load(open(os.path.join(out, r['outdir'], r['arms_read'][0]['file']), encoding='utf-8'))
        ev = d['mpm_metrics']['step3']['manifest']['ca_ext']['cjunc']['evidence']
        svr = (ev.get('solve') or {}).get('sv_counterfactual') or {}
        evs.append(({k: ev['census'].get(k) for k in sealed or {}}, {k: svr.get(k) for k in sealed or {}}))
    chk('E10a 봉인 SV census (실제 S0 함수 · off 격자 · 봉인 s_min 0.6) = 실제 DBE arm 0 SV 런 (P0 c 0 · P1 c 1) 의 증거 census = 기록 census 사본 · '
        '사슬 대조 무리 키 = 주 래스터 origin 0 · read_run 통과 (러너 rc 0 · 둘)',
        bool(sealed) and key in seed_c and key in seed_g and len(res) == 2 and all(e == sealed and s == sealed for e, s in evs),
        (sealed, evs, sorted(seed_c)))
    chk('E10b 봉인 census 의 못 가른 수를 +1 한 대조 → 같은 실제 런 꼴 (P0 c 1) 의 read_run = S0_REPORT_MISMATCH (사유 census)',
        stop is not None and stop.code == 'S0_REPORT_MISMATCH' and 'census' in str(stop.cause), (stop and stop.code, stop and str(stop.cause)[:300]))


def t_no_venv():
    """★ 10-26 B″ (1저자 Q4 · 묶음 B 보고 결정 4) — 사슬이 실제 러너에 MPM_NO_VENV=1 을 준다: 사슬 프로세스 env 에 MPM_NO_VENV · VIRTUAL_ENV 가 없고
    러너가 찾는 venv 자리 (`$SCR/../venv` = 고정물 저장소 뿌리 · .gitignore 의 venv/ = 깨끗함 그대로) 에 미끼 venv (activate = 표지 파일만 씀) 가
    있어도 러너가 venv 를 켜지 않는다 (러너 로그에 `[p2] venv` 줄 없음 · 표지 파일 없음) · payload 의 실행 인터프리터 (팔 매니페스트 exec_env.python)
    의 같음 단위 (python 부 판 · numpy · scipy) = 사슬이 단계 요약에 적는 환경 지문 (`env_record` unit) · python 전체 판 같음.
    ⚠ 판별 = 미끼 (옛 사슬 = 부모 셸 그대로 → 러너가 미끼 · $HOME/dem-venv 를 켠다) · 환경 지문 같음 = 이 시험 틀에서는 구성상 같다 (가짜 python3 심이
    시험 인터프리터를 부른다 — 확인 칸이지 판별 칸이 아니다)."""
    import platform
    import shlex
    ws = make_root('e11')
    pp, _sp, _rp = make_plan_and_reg(ws)
    plan = json.load(open(pp, encoding='utf-8'))
    sd = code_repo()
    runner = os.path.join(sd, 'sdcp_gain_vox015_8arm.sh')
    decoy = os.path.join(CODEREPO['repo'], 'venv')
    mark = os.path.join(TD, 'e11_decoy_sourced')
    os.makedirs(os.path.join(decoy, 'bin'))
    with open(os.path.join(decoy, 'bin', 'activate'), 'w', encoding='utf-8') as f:
        f.write(f'# 미끼 venv (시험 E11 · 켜면 표지 파일을 쓴다)\necho sourced >> {shlex.quote(mark)}\n')
    out = os.path.join(TD, 'runs', 'e11')
    old_bk, old_here = RR.EXPECT_BACKEND, RR.HERE
    RR.EXPECT_BACKEND, RR.HERE = 'cpu', Path(sd)
    buf = io.StringIO()
    rn, stop, dirty = None, None, None
    try:
        with chain_env(ws, no_venv=False), contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            dirty = _git(CODEREPO['repo'], 'status', '--porcelain', '--untracked-files=normal')
            rn = RR.Runner(runner, ws, out, plan, None, time.time() + 1800, RR.RealContract(), prefix='V')
            try:
                rn.run(SBE_KIT, 'floor', 'P0', '0', 'inf', 1)
            except RR.Stop as e:
                stop = e
    finally:
        RR.EXPECT_BACKEND, RR.HERE = old_bk, old_here
        shutil.rmtree(decoy, ignore_errors=True)
    rec = rn.records[0] if (rn is not None and rn.records) else {}
    logs = ''.join(open(p, encoding='utf-8', errors='replace').read() for p in sorted(glob.glob(os.path.join(out, 'logs', '*.log'))))
    ee, unit = {}, None
    if rec.get('arms_read'):
        d = json.load(open(os.path.join(out, rec['outdir'], rec['arms_read'][0]['file']), encoding='utf-8'))
        ee = d['mpm_metrics']['step3']['manifest'].get('exec_env') or {}
        r = subprocess.run([str(ee.get('python')), '-I', '-c',
                            'import json, sys, numpy, scipy; print(json.dumps({"python_minor": "%d.%d" % sys.version_info[:2], '
                            '"numpy": numpy.__version__, "scipy": scipy.__version__}))'], capture_output=True, text=True)
        unit = json.loads(r.stdout) if r.returncode == 0 else r.stderr[-300:]
    want = RR.env_record()['unit']
    chk('E11a 사슬 env 에 MPM_NO_VENV · VIRTUAL_ENV 없음 + 러너 자리의 미끼 venv → 러너 rc 0 · 팔 계약 통과 · 미끼를 켜지 않음 (표지 파일 없음 · 러너 '
        '로그에 `[p2] venv` 줄 없음) · 고정물 체크아웃 깨끗 (venv/ = ignore 안)',
        dirty == '' and stop is None and rec.get('rc') == 0 and bool(rec.get('arms_read')) and not os.path.exists(mark)
        and '[p2] venv' not in logs,
        (dirty[:200], stop and (stop.code, stop.cause[:300]), rec.get('rc'), os.path.exists(mark),
         [ln for ln in logs.splitlines() if '[p2] venv' in ln][:2], buf.getvalue()[-400:]))
    chk('E11b payload 실행 인터프리터 (exec_env.python) 의 같음 단위 (python 부 판 · numpy · scipy) = 사슬 환경 지문 env_record unit · python 전체 판 '
        '같음 (구성상 같음 = 확인 칸 · 판별 = E11a)',
        unit == want and ee.get('py_version') == platform.python_version(), (unit, want, ee.get('python'), ee.get('py_version')))


def t_graph_source():
    """★ 10-26 B″ (1저자 10-26 Q1 (가) · 묶음 B 보고 §13 결정 1) — 실물 생산 봉인 원천 (실제 러너 · 실제 payload · 합성 DBE 킷 · SDCP · CPU): 사슬 기본
    `SV_GRAPH_SOURCE` = `RUNNER_GRAPH_SOURCE` · DBE arm 0 SV 모서리 런 (P1 · c 1 · R_j 1e6) 에 `RunnerGraphSource` (같은 러너 · 같은 env + CJUNC_GRAPH_ONLY=1
    · 조립만 · CG 없음) → 그 런 SV 기록의 끝 그래프 귀속 = verified (증서 구간 기록 · 비를 싣는 끝 있음 = 대조가 뜻이 있다) · 원천 출력 = 조립만 기록
    하나 (팔 JSON 없음) · 원천이 돌려준 주 계 지문만 바꾼 꼴 = read_run 멈춤 CA_EXT_RECORD (RR1-01) · 사슬 환경 단위가 다른 꼴 (numpy 판 바꿔 끼움) =
    원천 실패 → 미확인 (멈춤 아님 · clear 아님) · 결합 칸 하나 (fp_sid) 다른 ctx = GraphSourceError (결합 · 그 칸 이름) · 비용 (원천 런 초 · payload 가
    잰 STEP3 · 조립 초 · 최대 RSS) 보고.  (사슬 사다리 · 예측을 다 돌리지 않는다 — 단계 배선 = 가짜 러너 시험 RG08–RG13)"""
    ws = make_root('e12')
    pp, _sp, _rp = make_plan_and_reg(ws)
    plan = json.load(open(pp, encoding='utf-8'))
    cls = getattr(RR, 'RunnerGraphSource', None)
    if cls is None or getattr(RR, 'SV_GRAPH_SOURCE', None) != getattr(RR, 'RUNNER_GRAPH_SOURCE', '<없음>'):
        chk('E12 사슬 생산 봉인 원천 (RunnerGraphSource · 기본 SV_GRAPH_SOURCE = RUNNER_GRAPH_SOURCE) 이 있다', False,
            (cls, getattr(RR, 'SV_GRAPH_SOURCE', None)))
        return
    import ca_ext_svcf as SVCF
    recs = {'stage2': RR.read_s0_report(os.path.join(TD, 's0_stage2.json'), 2), 'stage1': RR.read_s0_report(os.path.join(TD, 's0_stage1.json'), 1)}
    seed_g, seed_c = RR.s0_grid_seed(recs), RR.s0_census_seed(recs)
    sd = code_repo()
    runner = os.path.join(sd, 'sdcp_gain_vox015_8arm.sh')
    out = os.path.join(TD, 'runs', 'e12')

    class Keep(cls):
        def __call__(self, ctx):
            self.last_ctx = json.loads(json.dumps(ctx, default=str))
            return super().__call__(ctx)

    class TamperMain(cls):
        def __call__(self, ctx):
            g = super().__call__(ctx)
            return dict(g, main=('0' * 64 if g.get('main') != '0' * 64 else '1' * 64))

    def runner_(o, src_cls, prefix):
        rn_ = RR.Runner(runner, ws, o, plan, None, time.time() + 1800, RR.RealContract(), prefix=prefix)
        rn_.s0_grid, rn_.s0_census = seed_g, seed_c
        rn_.graph_src = src_cls(runner, ws, os.path.join(o, 'graph_src'), deadline=rn_.deadline)
        return rn_

    old_bk, old_here, old_env = RR.EXPECT_BACKEND, RR.HERE, RR.env_record
    RR.EXPECT_BACKEND, RR.HERE = 'cpu', Path(sd)
    buf = io.StringIO()
    rn, arms, stop_t, arms_e, err_b, gs, gs_e, t_sv = None, None, None, None, None, None, None, None
    try:
        with chain_env(ws), contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            rn = runner_(out, Keep, 'G')
            t0 = time.time()
            arms = rn.run(DBE_KIT, 'corner', 'P1', '1', RR.rj_key(1e6), 1, True)
            t_sv = time.time() - t0
            gs = rn.graph_src
            rn_t = runner_(out + '_t', TamperMain, 'G')
            try:
                rn_t.run(DBE_KIT, 'corner', 'P1', '1', RR.rj_key(1e6), 1, True)
            except RR.Stop as e:
                stop_t = e
            rec0 = old_env()
            RR.env_record = lambda: dict(rec0, unit=dict(rec0['unit'], numpy='0.0.0-e12'))
            try:
                rn_e = runner_(out + '_e', cls, 'G')
                arms_e = rn_e.run(DBE_KIT, 'corner', 'P1', '1', RR.rj_key(1e6), 1, True)
                gs_e = rn_e.graph_src
            finally:
                RR.env_record = old_env
            ctx_b = dict(gs.last_ctx, bind=dict(gs.last_ctx['bind'], fp_sid='0' * 64))
            gs_b = cls(runner, ws, os.path.join(out + '_b', 'graph_src'))
            try:
                gs_b(ctx_b)
            except RR.GraphSourceError as e:
                err_b = e
    except RR.Stop as e:
        chk('E12 실물 DBE SV 모서리 + 봉인 원천 런이 사슬 read_run 을 지난다', False, f'{e.code}: {e.cause} · {buf.getvalue()[-900:]}')
        return
    finally:
        RR.EXPECT_BACKEND, RR.HERE, RR.env_record = old_bk, old_here, old_env
    a0 = (arms or [{}])[0]
    svr_file = os.path.join(out, rn.records[0]['outdir'], rn.records[0]['arms_read'][0]['file'])
    d = json.load(open(svr_file, encoding='utf-8'))
    svr = ((d['mpm_metrics']['step3']['manifest']['ca_ext']['cjunc']['evidence'].get('solve') or {}).get('sv_counterfactual') or {})
    runs = gs.public()['runs']
    g0 = runs[0] if runs else {}
    gdir = os.path.join(out, 'graph_src')
    #  ★ 10-27 묶음 C2b — 원천 폴더의 groups/ (러너 프로세스 그룹 기록) 는 원천 런 폴더가 아니다
    gdirs = sorted(x for x in os.listdir(gdir) if x not in ('logs', 'groups')) if os.path.isdir(gdir) else []
    gjson = sorted(os.path.basename(x) for x in glob.glob(os.path.join(gdir, '*', '*.json')))
    gfiles = [x for x in gjson if x.startswith('cjgraph_')]       # 러너 영수증 (run_receipt.json · 조립만 표지 = 팔 증명 불가) 은 따로
    grcpt = [json.load(open(x, encoding='utf-8')) for x in glob.glob(os.path.join(gdir, '*', 'run_receipt.json'))]
    cost = g0.get('cost') or {}
    print(f'    보고 E12 — SV 런 {t_sv and round(t_sv, 1)} s (그 안 원천 런 {g0.get("seconds")} s) · 원천 payload STEP3 {cost.get("seconds_step3")} s · '
          f'조립 {cost.get("seconds_assemble")} s · 최대 RSS {cost.get("peak_rss_kb")} kB · SV 상태 {svr.get("status")} · 증서 구간 '
          f'{svr.get("standing")} · 귀속 {a0.get("sv_graph")}')
    chk('E12a 생산 기본 원천 (러너 조립만 · 실제 payload) — DBE arm 0 SV 모서리 (P1 · c 1 · R_j 1e6) 의 SV 기록 = 증서 구간 · 비를 싣는 끝 있음 '
        '(graph_applicable) · 끝 그래프 귀속 verified · 원천 런 하나 (상태 ok · rc 0 · 환경 단위 = 사슬 · 비용 칸 셋) · 원천 폴더 = 조립만 출력 하나 '
        '(cjgraph_p2_…_a0.json · 팔 JSON p2_* 없음 · 러너 영수증 cjunc_graph_only True = 팔 증명 불가 · N11i)',
        SVCF.graph_applicable(svr) and (a0.get('sv_graph') or {}).get('state') == 'verified' and len(runs) == 1 and g0.get('status') == 'ok'
        and g0.get('rc') == 0 and g0.get('env_unit') == RR.env_unit(old_env())
        and set(cost) == {'seconds_step3', 'seconds_assemble', 'peak_rss_kb'} and len(gdirs) == 1 and len(gfiles) == 1
        and gfiles[0].startswith('cjgraph_p2_') and gfiles[0].endswith('_a0.json') and not glob.glob(os.path.join(gdir, '*', 'p2_*.json'))
        and len(grcpt) == 1 and grcpt[0].get('cjunc_graph_only') is True,
        (svr.get('standing'), svr.get('status'), a0.get('sv_graph'), runs, gdirs, gjson, [r.get('cjunc_graph_only') for r in grcpt],
         buf.getvalue()[-500:]))
    gends = [json.load(open(x, encoding='utf-8')) for x in glob.glob(os.path.join(gdir, 'groups', '*.end.json'))]
    chk('E12g ★ 10-27 묶음 C2b — 원천 런 (러너 조립만) 도 러너 프로세스 그룹 · 끝 기록 확인 True · 원인 None · rc 0 (원천 런마다)',
        len(gends) == len(runs) >= 1 and all(e.get('confirmed') is True and e.get('cause') is None and e.get('rc') == 0 for e in gends),
        (len(gends), len(runs), gends[:1]))
    chk('E12b 원천이 돌려준 주 계 지문만 바꾼 꼴 (같은 실제 원천 런 · 반환 dict 의 main 만) → read_run 멈춤 CA_EXT_RECORD (사유 fp_cjunc_graph · RR1-01)',
        stop_t is not None and stop_t.code == 'CA_EXT_RECORD' and 'fp_cjunc_graph' in str(stop_t.cause) and 'RR1-01' in str(stop_t.cause),
        (stop_t and stop_t.code, stop_t and str(stop_t.cause)[-300:]))
    ge = (gs_e.public()['runs'] if gs_e is not None else [])
    sg_e = (arms_e[0].get('sv_graph') or {}) if arms_e else {}
    chk('E12c 사슬 환경 단위가 원천 런과 다른 꼴 (사슬 env_record 의 numpy 판을 바꿔 끼움) → 원천 실패 (사유 환경 단위) → 그 SV 기록 귀속 = unverified '
        '(source_failed · 런 멈춤 아님 · verified 아님)',
        (sg_e.get('state'), sg_e.get('kind')) == ('unverified', 'source_failed')
        and len(ge) == 1 and ge[0].get('status') == 'failed' and '환경 단위' in str(ge[0].get('why')),
        (sg_e, ge))
    chk('E12d 같은 실제 원천 런 ctx 의 결합 칸 하나 (fp_sid) 만 다르게 → GraphSourceError (원천 조립 결합 ≠ 그 런 주 증서 결합 · 칸 fp_sid)',
        err_b is not None and '결합' in str(err_b) and 'fp_sid' in str(err_b), (err_b and str(err_b)[:300]))


#  ═════════════ ★ 10-27 묶음 C2b (Q9 설계 개정 4 Q2 · R4-02 ⓐ ⓑ ⓒ · Codex 회차 ① ② · 개정 5 ② · author 10-27 approved bundle C) 실경로 ═════════════
#  실제 러너 · 실제 payload (감싸개 `rint_first_result.py` 가 같은 프로세스에서 첫 σ 직후 표지) · 실제 프로세스 그룹 — 러너만 죽이기 · 시간 초과 · 사슬 부모
#  죽이기 (따로 프로세스) + recover · 표지 앞 · 뒤.  지연 = 시험 심 (가짜 python3) 이 감싸개 대신 지연 구동기를 부른다 (생산 코드에 지연 없음).
DELAY_DRIVER = r'''
import os, runpy, sys, time
mode, secs = os.environ.get('E2E_DELAY_MODE', ''), float(os.environ.get('E2E_DELAY_S', '0'))
wrapper = sys.argv[1]
sys.path.insert(0, os.path.dirname(os.path.abspath(wrapper)))
import step3_sigma as S3
if mode == 'before':                                 # 첫 CG 앞 (표지 앞)
    _o = S3._solve_cg
    def _slow(*a, **k):
        time.sleep(secs)
        return _o(*a, **k)
    S3._solve_cg = _slow
elif mode == 'after':                                # 증서 (주 CG · 표지 뒤)
    import step3_conv_cert as CC
    _c = CC.certify
    def _slowc(*a, **k):
        time.sleep(secs)
        return _c(*a, **k)
    CC.certify = _slowc
sys.argv = [wrapper] + sys.argv[2:]
runpy.run_path(wrapper, run_name='__main__')
'''

RUN_DRIVER = r'''
import json, os, sys, time
from pathlib import Path
cfg = json.load(open(sys.argv[1], encoding='utf-8'))
sys.path.insert(0, cfg['scripts'])
import rint_r_chain as RR
RR.HERE = Path(cfg['here'])
RR.EXPECT_BACKEND = 'cpu'
os.environ.clear()
os.environ.update(cfg['env'])
plan = json.load(open(cfg['plan'], encoding='utf-8'))
rn = RR.Runner(cfg['runner'], cfg['ws'], cfg['out'], plan, None, time.time() + 1800, RR.RealContract(), prefix='K', machine='kgy')
try:
    rn.run(RR.SBE_KIT, 'floor', 'P0', '0', 'inf', 1)
    print('RUN DONE')
except RR.Stop as e:
    print('STOP', e.code, e.cause)
'''


def e13_env(ws, mode, secs):
    """사슬 프로세스 env (chain_env 꼴 · 따로 프로세스용 dict) + 지연 구동기."""
    drv = os.path.join(TD, 'e13_delay_driver.py')
    if not os.path.exists(drv):
        with open(drv, 'w', encoding='utf-8') as f:
            f.write(DELAY_DRIVER)
    env = {k: v for k, v in os.environ.items() if not (k.startswith(TR._AXIS_PREFIX) or k in TR._AXIS_EXACT)}
    env.update(PATH=TR.SHIMDIR + os.pathsep + os.environ.get('PATH', '/usr/bin:/bin'), MPM_NO_VENV='1', PYTHONDONTWRITEBYTECODE='1',
               PYTHONUTF8='1', PYTHONIOENCODING='utf-8', SHIM_LOG=os.path.join(ws, '_shim'), SHIM_DELAY_DRIVER=drv,
               E2E_DELAY_MODE=mode, E2E_DELAY_S=str(secs))
    return env


def e13_alive(token):
    """시험 쪽 독립 대조 — 살아 있는 (zombie 뺌) 프로세스 중 environ 에 RINT_RUN_TOKEN=token."""
    out, needle = [], f'RINT_RUN_TOKEN={token}'.encode()
    for e in os.listdir('/proc'):
        if not e.isdigit():
            continue
        try:
            st = open(f'/proc/{e}/stat', 'rb').read()
            if st[st.rfind(b')') + 2:].split()[0] in (b'Z', b'X'):
                continue
            if needle in open(f'/proc/{e}/environ', 'rb').read().split(b'\0'):
                out.append(int(e))
        except (OSError, IndexError):
            continue
    return out


def e13_cmdlines(pids):
    """프로세스 명령줄 — 전체 (자르지 않는다).  ★ 10-27 kgy 판 1 회차 — 옛 판은 160 자로 자른 뒤 감싸개 이름을 찾았다: 시험 심이 진짜 인터프리터 절대 경로로
    exec 하므로 (이 컨테이너 3.11 = 22 자 · uv 3.8 = 74 자) 3.8 에서는 이름이 잘려 죽이는 손이 '표지 앞 · payload 떠 있음' 창을 못 봤다 (E13b · E13e)."""
    out = []
    for p in pids:
        try:
            out.append(open(f'/proc/{p}/cmdline', 'rb').read().replace(b'\0', b' ').decode('utf-8', 'replace'))
        except OSError:
            pass
    return out


def e13_launch(out, name, t_end):
    lp = os.path.join(out, 'groups', f'{name}.launch.json')
    while time.time() < t_end:
        if os.path.exists(lp):
            try:
                j = json.load(open(lp, encoding='utf-8'))
                if j.get('pid'):
                    return j
            except ValueError:
                pass
        time.sleep(0.05)
    return None


def e13_files(out):
    """런 폴더 (· .unchecked) 의 팔 payload · 표지 이름 (시도 폴더 판정의 입력과 같은 꼴)."""
    got = []
    for p in sorted(glob.glob(os.path.join(out, '**', '*'), recursive=True) + glob.glob(os.path.join(out, '**', '.*'), recursive=True)
                    + glob.glob(os.path.join(out, '**', '.unchecked', '*'), recursive=True)):
        b = os.path.basename(p)
        if (b.startswith('p2_') and '.json' in b) or b.endswith('.first_result.json'):
            got.append(os.path.relpath(p, out))
    return sorted(set(got))


def e13_kit_payloads(ws):
    return sorted(glob.glob(os.path.join(ws, SBE_KIT, '*', 'p2_*.json*')))


def e13_runner_kill(tag, mode, secs, when_marker):
    """러너 (bash) 하나만 SIGKILL — 사슬은 이 프로세스 · 죽이는 손 = 실 (표지 앞 = payload 프로세스가 뜨면 · 뒤 = 표지가 생기면)."""
    import threading
    ws = make_root(tag)
    pp, _sp, _rp = make_plan_and_reg(ws)
    plan = json.load(open(pp, encoding='utf-8'))
    sd = code_repo()
    runner = os.path.join(sd, 'sdcp_gain_vox015_8arm.sh')
    out = os.path.join(TD, 'runs', tag)
    seen = {}

    def killer():
        t_end = time.time() + 120
        j = e13_launch(out, 'K01_floor', t_end)
        if j is None:
            seen['err'] = 'launch 기록 없음'
            return
        seen['token'] = j['token']
        seen['saw_window'] = False                       # ★ 10-27 kgy 판 1 회차 — 죽일 창을 실제로 봤는지 (검사 칸 · 못 보면 실패 이유가 남는다)
        while time.time() < t_end:
            marks = glob.glob(os.path.join(out, 'K01_floor_arm1', '.unchecked', '*.first_result.json'))
            pay = [c for c in e13_cmdlines(e13_alive(j['token'])) if 'rint_first_result.py' in c]
            if (when_marker and marks) or (not when_marker and pay and not marks):
                seen['saw_window'] = True
                break
            time.sleep(0.05)
        time.sleep(0.3)
        seen['marks_at_kill'] = len(glob.glob(os.path.join(out, 'K01_floor_arm1', '.unchecked', '*.first_result.json')))
        seen['alive_at_kill'] = e13_cmdlines(e13_alive(j['token']))
        try:
            os.kill(int(j['pid']), signal.SIGKILL)
        except ProcessLookupError:                       # 러너가 이미 끝났다 (창을 놓친 꼴) — 실 예외 대신 기록 (검사가 실패를 보고한다)
            seen['kill_err'] = 'ProcessLookupError'
    th = threading.Thread(target=killer)
    old_bk, old_here = RR.EXPECT_BACKEND, RR.HERE
    RR.EXPECT_BACKEND, RR.HERE = 'cpu', Path(sd)
    buf = io.StringIO()
    stop = None
    keep = {k: os.environ.get(k) for k in ('SHIM_DELAY_DRIVER', 'E2E_DELAY_MODE', 'E2E_DELAY_S')}
    t0 = time.time()
    try:
        with chain_env(ws), contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            os.environ.update({k: v for k, v in e13_env(ws, mode, secs).items() if k.startswith(('SHIM_DELAY', 'E2E_DELAY'))})
            rn = RR.Runner(runner, ws, out, plan, None, time.time() + 1800, RR.RealContract(), prefix='K', machine='kgy')
            th.start()
            try:
                rn.run(SBE_KIT, 'floor', 'P0', '0', 'inf', 1)
            except RR.Stop as e:
                stop = e
            th.join()
    finally:
        RR.EXPECT_BACKEND, RR.HERE = old_bk, old_here
        for k, v in keep.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    t_ret = time.time()
    tok = seen.get('token')
    alive_after = e13_alive(tok) if tok else None
    files_ret = e13_files(out)
    time.sleep(max(0.0, t0 + secs + 6.0 - time.time()))           # 지연이 끝났을 시간까지 — 살아 있었다면 이제 썼다
    files_late = e13_files(out)
    endp = os.path.join(out, 'groups', 'K01_floor.end.json')
    er = json.load(open(endp, encoding='utf-8')) if os.path.exists(endp) else None
    return {'stop': stop, 'seen': seen, 'alive_after': alive_after, 'files_ret': files_ret, 'files_late': files_late, 'end': er,
            'kit_payloads': e13_kit_payloads(ws), 'so': buf.getvalue(), 'secs_ret': t_ret - t0}


def t_runner_kill():
    if not callable(getattr(RR, 'host_ident', None)):
        chk('E13b/E13c 사슬에 러너 프로세스 그룹 (그룹 기록 · host_ident · recover) 이 있다', False, '고치기 전 판 — 그룹 기록 없음 (기다리지 않는다)')
        return
    a = e13_runner_kill('e13b', 'before', 12, when_marker=False)
    er = a['end'] or {}
    chk('E13b 실물 러너만 SIGKILL (표지 앞 · payload 프로세스가 떠 있음) → 사슬 = 러너 rc −9 · 그룹 (payload) 을 죽이고 종료 확인 (끝 기록 확인 True · rc −9) · '
        'RUNNER_RC · 돌아온 뒤 표지 프로세스 0 · 표지 · 팔 payload 없음 (지연이 끝날 시간 뒤에도) · 킷 런 폴더에 payload 없음',
        a['stop'] is not None and a['stop'].code == 'RUNNER_RC' and er.get('confirmed') is True and er.get('rc') == -9
        and a['seen'].get('saw_window') is True
        and a['seen'].get('marks_at_kill') == 0 and any('rint_first_result.py' in c for c in a['seen'].get('alive_at_kill') or [])
        and a['alive_after'] == [] and a['files_ret'] == [] and a['files_late'] == [] and a['kit_payloads'] == [],
        (a['stop'] and (a['stop'].code, a['stop'].cause[:200]), a['seen'], er, a['alive_after'], a['files_ret'], a['files_late'],
         a['kit_payloads'], a['so'][-600:]))
    b = e13_runner_kill('e13c', 'after', 12, when_marker=True)
    er = b['end'] or {}
    marks = [f for f in b['files_late'] if f.endswith('.first_result.json')]
    pays = [f for f in b['files_late'] if os.path.basename(f).startswith('p2_') and not f.endswith('.first_result.json')]   # 표지 이름도 p2_ 로 시작한다
    chk('E13c 실물 러너만 SIGKILL (표지 뒤 · 증서 풀이 중) → 사슬 = 그룹을 죽이고 확인 · RUNNER_RC · 표지 하나 (.unchecked/ · 결과 뒤 판정의 입력) · '
        '팔 payload 없음 (지연이 끝날 시간 뒤에도 = payload 프로세스가 죽었다) · 표지 프로세스 0',
        b['stop'] is not None and b['stop'].code == 'RUNNER_RC' and er.get('confirmed') is True and b['seen'].get('saw_window') is True
        and b['seen'].get('marks_at_kill') == 1
        and len(marks) == 1 and '.unchecked' in marks[0] and pays == [] and b['alive_after'] == [] and b['kit_payloads'] == [],
        (b['stop'] and (b['stop'].code, b['stop'].cause[:200]), b['seen'], er, b['files_late'], b['alive_after']))


def t_timeout_kill():
    """시간 초과 — 러너 deadline 6 s · 표지 앞 지연 20 s → TIME_LIMIT · 그룹 죽임 · 확인 · 표지 · payload 없음."""
    if not callable(getattr(RR, 'host_ident', None)):
        chk('E13d 사슬에 러너 프로세스 그룹 (그룹 기록 · host_ident · recover) 이 있다', False, '고치기 전 판 — 그룹 기록 없음 (기다리지 않는다)')
        return
    ws = make_root('e13d')
    pp, _sp, _rp = make_plan_and_reg(ws)
    plan = json.load(open(pp, encoding='utf-8'))
    sd = code_repo()
    runner = os.path.join(sd, 'sdcp_gain_vox015_8arm.sh')
    out = os.path.join(TD, 'runs', 'e13d')
    old_bk, old_here = RR.EXPECT_BACKEND, RR.HERE
    RR.EXPECT_BACKEND, RR.HERE = 'cpu', Path(sd)
    buf = io.StringIO()
    stop = None
    keep = {k: os.environ.get(k) for k in ('SHIM_DELAY_DRIVER', 'E2E_DELAY_MODE', 'E2E_DELAY_S')}
    t0 = time.time()
    try:
        with chain_env(ws), contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            os.environ.update({k: v for k, v in e13_env(ws, 'before', 20).items() if k.startswith(('SHIM_DELAY', 'E2E_DELAY'))})
            rn = RR.Runner(runner, ws, out, plan, None, time.time() + 6.0, RR.RealContract(), prefix='K', machine='kgy')
            try:
                rn.run(SBE_KIT, 'floor', 'P0', '0', 'inf', 1)
            except RR.Stop as e:
                stop = e
    finally:
        RR.EXPECT_BACKEND, RR.HERE = old_bk, old_here
        for k, v in keep.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    endp = os.path.join(out, 'groups', 'K01_floor.end.json')
    er = json.load(open(endp, encoding='utf-8')) if os.path.exists(endp) else {}
    lp = os.path.join(out, 'groups', 'K01_floor.launch.json')
    tok = json.load(open(lp, encoding='utf-8')).get('token') if os.path.exists(lp) else None
    alive = e13_alive(tok) if tok else None
    time.sleep(max(0.0, t0 + 26.0 - time.time()))
    files = e13_files(out)
    chk('E13d 실물 시간 초과 (deadline 6 s · 표지 앞 지연 20 s) → TIME_LIMIT · 끝 기록 원인 timeout · 확인 True · 표지 프로세스 0 · 표지 · 팔 payload 없음 '
        '(지연이 끝날 시간 뒤에도) · 킷 런 폴더에 payload 없음',
        stop is not None and stop.code == 'TIME_LIMIT' and er.get('cause') == 'timeout' and er.get('confirmed') is True and alive == []
        and files == [] and e13_kit_payloads(ws) == [],
        (stop and (stop.code, stop.cause[:200]), er, alive, files, buf.getvalue()[-500:]))


def e13_parent_kill(tag, mode, secs, when_marker):
    """사슬 부모를 따로 프로세스로 · 그 프로세스를 SIGKILL → 그룹이 살아 있는지 · recover → 그룹 종료 확인 · 지연 뒤 파일."""
    ws = make_root(tag)
    pp, _sp, _rp = make_plan_and_reg(ws)
    sd = code_repo()
    runner = os.path.join(sd, 'sdcp_gain_vox015_8arm.sh')
    out = os.path.join(TD, 'runs', tag)
    drv = os.path.join(TD, 'e13_run_driver.py')
    if not os.path.exists(drv):
        with open(drv, 'w', encoding='utf-8') as f:
            f.write(RUN_DRIVER)
    cfg = os.path.join(TD, f'{tag}_cfg.json')
    with open(cfg, 'w', encoding='utf-8') as f:
        json.dump({'scripts': SCRIPTS, 'here': sd, 'env': e13_env(ws, mode, secs), 'plan': pp, 'runner': runner, 'ws': ws, 'out': out}, f)
    t0 = time.time()
    log = open(os.path.join(TD, f'{tag}_driver.log'), 'w', encoding='utf-8')
    pr = subprocess.Popen([sys.executable, '-I', drv, cfg], cwd=ws, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    j = e13_launch(out, 'K01_floor', time.time() + 120)
    seen = {'token': (j or {}).get('token'), 'saw_window': False}     # ★ 10-27 kgy 판 1 회차 — 죽일 창을 실제로 봤는지 (검사 칸)
    while j is not None and time.time() < t0 + 120:
        marks = glob.glob(os.path.join(out, 'K01_floor_arm1', '.unchecked', '*.first_result.json'))
        pay = [c for c in e13_cmdlines(e13_alive(j['token'])) if 'rint_first_result.py' in c]
        if (when_marker and marks) or (not when_marker and pay and not marks):
            seen['saw_window'] = True
            break
        time.sleep(0.05)
    time.sleep(0.3)
    os.kill(pr.pid, signal.SIGKILL)
    pr.wait()
    tok = seen['token']
    seen['alive_after_parent'] = e13_cmdlines(e13_alive(tok)) if tok else None
    seen['end_before'] = os.path.exists(os.path.join(out, 'groups', 'K01_floor.end.json'))
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        try:
            rc = RR.main(['--stage', 'recover', '--out', out])
        except SystemExit as e:
            rc = e.code
    seen['recover_rc'], seen['recover_so'] = rc, buf.getvalue()[-400:]
    seen['alive_after_recover'] = e13_alive(tok) if tok else None
    time.sleep(max(0.0, t0 + secs + 6.0 - time.time()))
    seen['files_late'] = e13_files(out)
    endp = os.path.join(out, 'groups', 'K01_floor.end.json')
    seen['end'] = json.load(open(endp, encoding='utf-8')) if os.path.exists(endp) else None
    seen['kit_payloads'] = e13_kit_payloads(ws)
    return seen


def t_parent_kill():
    if not callable(getattr(RR, 'host_ident', None)):
        chk('E13e/E13f 사슬에 러너 프로세스 그룹 (그룹 기록 · host_ident · recover) 이 있다', False, '고치기 전 판 — 그룹 기록 없음 (기다리지 않는다)')
        return
    a = e13_parent_kill('e13e', 'before', 12, when_marker=False)
    er = a.get('end') or {}
    chk('E13e 실물 사슬 부모 SIGKILL (따로 프로세스 · 표지 앞) → 러너 그룹은 살아 있다 (payload 프로세스 · 끝 기록 없음 — 부모 사망 + 지금 표지 없음 ≠ 종료 증거) · '
        '--stage recover → 그룹을 죽이고 확인 (끝 기록 by recover · 원인 parent_dead · rc 0) · 표지 프로세스 0 · 표지 · 팔 payload 없음 (지연 끝 뒤에도)',
        a.get('saw_window') is True
        and any('rint_first_result.py' in c for c in a.get('alive_after_parent') or []) and a.get('end_before') is False and a.get('recover_rc') == 0
        and er.get('by') == 'recover' and er.get('cause') == 'parent_dead' and er.get('confirmed') is True and a.get('alive_after_recover') == []
        and a.get('files_late') == [] and a.get('kit_payloads') == [], a)
    b = e13_parent_kill('e13f', 'after', 12, when_marker=True)
    er = b.get('end') or {}
    marks = [f for f in b.get('files_late') or [] if f.endswith('.first_result.json')]
    pays = [f for f in b.get('files_late') or [] if os.path.basename(f).startswith('p2_') and not f.endswith('.first_result.json')]
    chk('E13f 실물 사슬 부모 SIGKILL (표지 뒤) → recover 가 그룹을 죽이고 확인 · 표지 하나 (결과 뒤 판정의 입력) · 팔 payload 없음 (지연 끝 뒤에도) · 표지 프로세스 0',
        b.get('saw_window') is True
        and bool(b.get('alive_after_parent')) and b.get('recover_rc') == 0 and er.get('by') == 'recover' and er.get('confirmed') is True
        and len(marks) == 1 and pays == [] and b.get('alive_after_recover') == [], b)


def e2e_call(ws, sd, argv):
    """사슬 main 을 프로세스 안에서 (실물 러너 · 고정물 저장소 사슬 폴더 · CPU) → (rc, 화면)."""
    buf = io.StringIO()
    old_bk, old_here = getattr(RR, 'EXPECT_BACKEND', None), RR.HERE
    RR.EXPECT_BACKEND, RR.HERE = 'cpu', Path(sd)
    try:
        with chain_env(ws), contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            try:
                rc = RR.main([str(a) for a in argv])
            except SystemExit as e:
                rc = e.code if isinstance(e.code, int) else 2
    finally:
        RR.EXPECT_BACKEND, RR.HERE = old_bk, old_here
    return rc, buf.getvalue()


def tree_digest(p):
    """시험 쪽 독립 폴더 요약 (`sha256sum` 꼴 줄을 상대 경로 차례로 · 그 글의 sha256) — 사슬 함수와 따로."""
    rows = sorted((os.path.relpath(os.path.join(r, f), p).replace(os.sep, '/'), hashlib.sha256(open(os.path.join(r, f), 'rb').read()).hexdigest())
                  for r, _ds, fs in os.walk(p) for f in fs)
    return hashlib.sha256(''.join(f'{h}  {rel}\n' for rel, h in rows).encode('utf-8')).hexdigest()


E14_LADDER = {}                                            # E14 의 끊김 없는 실물 원장 사다리 칸 (E15 재실행과 대조)


def t_ledger():
    """★ 10-27 묶음 C1b — 실물 러너 · payload 의 원장 시도 (사다리 P0) → 결과 줄 (completed · 결과 뒤 · 폴더 요약 sha = 독립 계산) · 런마다 표지 ·
    .unchecked 에 payload 없음 (검사 통과 뒤 옮김) · 킷 런 폴더에 payload 없음."""
    if '--ledger' not in RR.main.__code__.co_consts:
        chk('E14 사슬에 시도 원장 (--ledger) 이 있다', False, '고치기 전 판 — --ledger 없음 (기다리지 않는다)')
        return
    ws = make_root('e14')
    pp, sp, rp = make_plan_and_reg(ws)
    sd = code_repo()
    runner = os.path.join(sd, 'sdcp_gain_vox015_8arm.sh')
    led = os.path.join(TD, 'ledger_e14')
    os.makedirs(led)
    subprocess.run(['git', 'init', '-q', led], check=True, capture_output=True)
    rc0, so0 = e2e_call(ws, sd, ['--stage', 'ledger', '--ledger', led, '--init', '--plan', pp])
    rc1, so1 = e2e_call(ws, sd, ['--stage', 'ledger', '--ledger', led, '--add', '--ledger-target', 'ladder:P0', '--machine', E2E_MACH, '--plan', pp,
                                 '--runner', runner, '--root', ws])
    m = re.search(r'ATTEMPT_ADDED n=(\d+)', so1)
    n = int(m.group(1)) if m else None
    base = os.path.join(TD, 'runs', 'e14')
    argv = ['--stage', 'ladder', '--law', 'P0', '--target', str(RR.TARGET_SBE_MS), '--runner', runner, '--root', ws, '--plan', pp,
            '--s0-plan', sp, '--registration', rp, '--max-hours', E2E_MAXH, '--out', base, '--machine', E2E_MACH] + s0_args() \
        + ['--ledger', led, '--attempt', str(n)]
    rc2, so2 = e2e_call(ws, sd, argv)
    folder = os.path.join(base, f'attempt_{n}')
    lines = [json.loads(x) for x in open(os.path.join(led, 'rint_r_attempts.jsonl'), encoding='utf-8').read().splitlines()]
    res = [x for x in lines if x.get('kind') == 'result' and x.get('n') == n]
    s = json.load(open(os.path.join(folder, 'ladder_summary.json'), encoding='utf-8')) if os.path.exists(os.path.join(folder, 'ladder_summary.json')) else {}
    runs = s.get('runs') or []
    marks = [os.path.join(folder, r['outdir']) for r in runs if not glob.glob(os.path.join(folder, r['outdir'], '.unchecked', '*' + '.first_result.json'))]
    left = [x for x in glob.glob(os.path.join(folder, '*', '.unchecked', 'p2_*.json*')) if not x.endswith('.first_result.json')]   # 표지 이름도 p2_ 로 시작한다
    r1 = res[0] if len(res) == 1 else {}
    E14_LADDER['ladder'] = s.get('ladder')
    chk('E14 ★ 10-27 묶음 C1b 실물 원장 시도 (사다리 P0 · 실물 러너 · payload) → --init · --add rc 0 · 사다리 CALIBRATED · 결과 줄 하나 (completed · 결과 뒤 · '
        'by chain · 폴더 요약 sha = 독립 계산) · 런마다 .unchecked/ 에 표지 · .unchecked/ 에 payload 없음 · 킷 런 폴더에 payload 없음',
        rc0 == 0 and rc1 == 0 and rc2 == 0 and s.get('status') == 'CALIBRATED' and r1.get('status') == 'completed' and r1.get('side') == 'post'
        and r1.get('by') == 'chain' and r1.get('folder_sha256') == tree_digest(folder) and runs and marks == [] and left == []
        and e13_kit_payloads(ws) == [],
        (rc0, rc1, rc2, s.get('status'), r1, len(runs), marks[:3], left[:3], e13_kit_payloads(ws)[:3], so2[-400:]))

STAGE_DRIVER = r'''
import json, os, sys
from pathlib import Path
cfg = json.load(open(sys.argv[1], encoding='utf-8'))
sys.path.insert(0, cfg['scripts'])
import rint_r_chain as RR
RR.HERE = Path(cfg['here'])
RR.EXPECT_BACKEND = 'cpu'
os.environ.clear()
os.environ.update(cfg['env'])
sys.exit(RR.main(cfg['argv']))
'''


def t_resume_real():
    """★ 10-27 묶음 C1b-2 실물 재실행 — 원장 사다리 시도 (사슬 = 따로 프로세스 · 실물 러너 · payload) 의 바닥 런 첫 풀이 끝 표지 뒤 사슬 부모 SIGKILL →
    --stage recover --ledger (그룹을 죽이고 확인 · 결과 줄 interrupted · parent_dead · 결과 뒤 · 재실행 자격) → --add --resume 1 → 재실행 시도 (실물 · 프로세스
    안) = 바닥 런부터 새로 (남은 payload 없음 = 결정성 가정) → CALIBRATED · 사다리 칸 = 끊김 없는 실물 원장 사다리 (E14) 와 같다."""
    if getattr(RR, 'ResumeRunner', None) is None:
        chk('E15 사슬에 재실행 실행 (ResumeRunner) 이 있다', False, '고치기 전 판 — 재실행 없음 (기다리지 않는다)')
        return
    ws = make_root('e15')
    pp, sp, rp = make_plan_and_reg(ws)
    sd = code_repo()
    runner = os.path.join(sd, 'sdcp_gain_vox015_8arm.sh')
    led = os.path.join(TD, 'ledger_e15')
    os.makedirs(led)
    subprocess.run(['git', 'init', '-q', led], check=True, capture_output=True)
    e2e_call(ws, sd, ['--stage', 'ledger', '--ledger', led, '--init', '--plan', pp])
    rc1, so1 = e2e_call(ws, sd, ['--stage', 'ledger', '--ledger', led, '--add', '--ledger-target', 'ladder:P0', '--machine', E2E_MACH, '--plan', pp,
                                 '--runner', runner, '--root', ws])
    base = os.path.join(TD, 'runs', 'e15')
    lad_argv = ['--stage', 'ladder', '--law', 'P0', '--target', str(RR.TARGET_SBE_MS), '--runner', runner, '--root', ws, '--plan', pp,
                '--s0-plan', sp, '--registration', rp, '--max-hours', E2E_MAXH, '--out', base, '--machine', E2E_MACH] + s0_args() + ['--ledger', led]
    drv = os.path.join(TD, 'e15_stage_driver.py')
    with open(drv, 'w', encoding='utf-8') as f:
        f.write(STAGE_DRIVER)
    cfg = os.path.join(TD, 'e15_cfg.json')
    with open(cfg, 'w', encoding='utf-8') as f:
        json.dump({'scripts': SCRIPTS, 'here': sd, 'env': e13_env(ws, 'after', 30), 'argv': [str(x) for x in lad_argv + ['--attempt', '1']]}, f)
    log = open(os.path.join(TD, 'e15_driver.log'), 'w', encoding='utf-8')
    pr = subprocess.Popen([sys.executable, '-I', drv, cfg], cwd=ws, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    folder = os.path.join(base, 'attempt_1')
    t0 = time.time()
    while time.time() < t0 + 120 and not glob.glob(os.path.join(folder, 'L01_floor_arm1', '.unchecked', '*.first_result.json')):
        time.sleep(0.05)
    time.sleep(0.3)
    os.kill(pr.pid, signal.SIGKILL)
    pr.wait()
    res0 = [json.loads(x) for x in open(os.path.join(led, 'rint_r_attempts.jsonl'), encoding='utf-8').read().splitlines() if '"result"' in x]
    rc3, so3 = e2e_call(ws, sd, ['--stage', 'recover', '--out', folder, '--ledger', led])
    lines = [json.loads(x) for x in open(os.path.join(led, 'rint_r_attempts.jsonl'), encoding='utf-8').read().splitlines()]
    r1 = ([x for x in lines if x.get('kind') == 'result' and x.get('n') == 1] or [{}])[0]
    rc4, so4 = e2e_call(ws, sd, ['--stage', 'ledger', '--ledger', led, '--add', '--ledger-target', 'ladder:P0', '--machine', E2E_MACH, '--plan', pp,
                                 '--runner', runner, '--root', ws, '--resume', '1'])
    rc5, so5 = e2e_call(ws, sd, lad_argv + ['--attempt', '2'])
    s = json.load(open(os.path.join(base, 'attempt_2', 'ladder_summary.json'), encoding='utf-8')) \
        if os.path.exists(os.path.join(base, 'attempt_2', 'ladder_summary.json')) else {}
    rs = s.get('resume') or {}
    lines = [json.loads(x) for x in open(os.path.join(led, 'rint_r_attempts.jsonl'), encoding='utf-8').read().splitlines()]
    r2 = ([x for x in lines if x.get('kind') == 'result' and x.get('n') == 2] or [{}])[0]
    ref = E14_LADDER.get('ladder')
    chk('E15 ★ 10-27 묶음 C1b-2 실물 재실행 — 바닥 런 표지 뒤 사슬 부모 SIGKILL → 결과 줄 없음 · recover --ledger rc 0 (interrupted · parent_dead · 결과 뒤 · '
        '재실행 자격) · --add --resume 1 rc 0 · 재실행 시도 rc 0 · CALIBRATED · resume 칸 (원 시도 1 · 복사 0 · 새로 = 바닥 · 결정성 가정) · 결과 줄 completed · '
        '사다리 칸 = 끊김 없는 실물 원장 사다리 (E14)',
        res0 == [] and rc1 == 0 and rc3 == 0 and r1.get('status') == 'interrupted' and r1.get('cause') == 'parent_dead' and r1.get('side') == 'post'
        and r1.get('resume_ok') is True and rc4 == 0 and rc5 == 0 and s.get('status') == 'CALIBRATED' and rs.get('from') == 1
        and rs.get('copied') == [] and rs.get('rerun') == 'L01_floor' and rs.get('determinism') == 'assumed' and r2.get('status') == 'completed'
        and (ref is None or s.get('ladder') == ref),
        (res0, rc1, rc3, r1, rc4, so4[-200:], rc5, s.get('status'), rs, r2, ref is None, so5[-300:]))


def _json_diff(a, b, pre=''):
    """두 JSON 값의 다른 자리 (경로 목록 · 보고용)."""
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            out += _json_diff(a.get(k), b.get(k), f'{pre}{k}.')
        return out
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out += _json_diff(x, y, f'{pre}{i}.')
        return out
    return [] if a == b else [pre.rstrip('.')]


def t_merge_fetch_real():
    """★ 10-27 묶음 C2d (Q9 §3-2 fetch · §4 같음의 근거 · author 10-27 approved bundle C) 실물 — 합치기 fetch 가 기대는 바이트 가정을 실제 러너 · 실제 payload ·
    합성 DBE 킷 (SDCP) · CPU 로 본다: 같은 요청 (DBE arm 0 SV 모서리 P0 · c 0 · R_j 1e6) 을 한 기계 사슬 이름 (P05_corner · 폴더 A) 과 단위 시도 이름
    (U01_corner · 폴더 B) 로 두 번 → 팔 JSON 바이트 · σ 같음 (다르면 다른 칸 보고) · B 의 런 폴더를 다른 자리 (C/units/unit-P0_c0_R_j0/attempt_7/) 로 통째로
    복사 → 사슬 read_run (합친 런 이름 · 실물 봉인 원천 = 러너 조립만 · 사본 경로) 통과 · SV 끝 그래프 귀속 verified · 팔 sha256 = B 의 기록.
    (12 단위 · 합치기 단계 배선 = 가짜 러너 시험 UM01–UM16 · 이 시험 = 실물 바이트 가정 · 구현과 함께 · 고치기 전 판에서도 돈다)"""
    ws = make_root('e16')
    pp, _sp, _rp = make_plan_and_reg(ws)
    plan = json.load(open(pp, encoding='utf-8'))
    recs = {'stage2': RR.read_s0_report(os.path.join(TD, 's0_stage2.json'), 2), 'stage1': RR.read_s0_report(os.path.join(TD, 's0_stage1.json'), 1)}
    seed_g, seed_c = RR.s0_grid_seed(recs), RR.s0_census_seed(recs)
    sd = code_repo()
    runner = os.path.join(sd, 'sdcp_gain_vox015_8arm.sh')
    oa, ob = os.path.join(TD, 'runs', 'e16_a'), os.path.join(TD, 'runs', 'e16_b')
    cdir = os.path.join(TD, 'runs', 'e16_c')
    old_bk, old_here = RR.EXPECT_BACKEND, RR.HERE
    RR.EXPECT_BACKEND, RR.HERE = 'cpu', Path(sd)
    buf = io.StringIO()
    got = {}
    try:
        with chain_env(ws), contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            for tag, o, prefix, n0 in (('a', oa, 'P', 4), ('b', ob, 'U', 0)):
                rn = RR.Runner(runner, ws, o, plan, None, time.time() + 1800, RR.RealContract(), prefix=prefix, machine=E2E_MACH)
                rn.s0_grid, rn.s0_census = seed_g, seed_c
                rn.graph_src = RR.RunnerGraphSource(runner, ws, os.path.join(o, 'graph_src'), deadline=rn.deadline)
                rn.n = n0
                got[tag] = (rn.run(DBE_KIT, 'corner', 'P0', '0', RR.rj_key(1e6), 1, True), rn.records[0])
            recb = got['b'][1]
            dst = os.path.join(cdir, 'units', 'unit-P0_c0_R_j0', 'attempt_7', recb['outdir'])
            shutil.copytree(os.path.join(ob, recb['outdir']), dst, symlinks=True)
            req = {k: recb.get(k) for k in RR.REQ_KEYS}
            req['name'] = 'P05_corner'
            gs = RR.RunnerGraphSource(runner, ws, os.path.join(cdir, 'graph_src'))
            got['c'] = RR.read_run(dst, req, plan, RR.RealContract(), {}, want_sha=[x['sha256'] for x in recb['arms_read']], s0_grid=seed_g,
                                   s0_census=seed_c, graph_src=gs)
    except RR.Stop as e:
        chk('E16 실물 DBE SV 모서리 두 이름 · 사본 다시 읽기가 사슬 read_run 을 지난다', False, f'{e.code}: {e.cause} · {buf.getvalue()[-900:]}')
        return
    finally:
        RR.EXPECT_BACKEND, RR.HERE = old_bk, old_here
    (aa, ra), (ab, rb), ac = got['a'], got['b'], got['c']
    fa = os.path.join(oa, ra['outdir'], ra['arms_read'][0]['file'])
    fb = os.path.join(ob, rb['outdir'], rb['arms_read'][0]['file'])
    same_bytes = open(fa, 'rb').read() == open(fb, 'rb').read()
    diff = [] if same_bytes else _json_diff(json.load(open(fa, encoding='utf-8')), json.load(open(fb, encoding='utf-8')))
    print(f'    보고 E16 — 이름 {ra["name"]} ↔ {rb["name"]} · 폴더 {ra["outdir"]} ↔ {rb["outdir"]} · 팔 JSON 바이트 같음 {same_bytes} · 다른 칸 {diff[:8]} · '
          f'사본 다시 읽기 SV 귀속 {(ac[0].get("sv_graph") or {}).get("state")}')
    chk('E16 ★ 10-27 묶음 C2d 실물 합치기 fetch 가정 — 같은 요청 · 다른 런 이름 (P05_corner · U01_corner) · 다른 폴더 = 팔 JSON 바이트 같음 · σ 같음 · SV 귀속 '
        'verified 둘 다 · 단위 폴더 사본 (다른 자리) 의 read_run (합친 이름 · 실물 봉인 원천) 통과 · σ · 팔 sha256 = 단위 런 기록 · SV 귀속 verified',
        same_bytes and aa[0]['sigma'] == ab[0]['sigma'] == ac[0]['sigma'] and ac[0]['sha256'] == rb['arms_read'][0]['sha256']
        and all((x[0].get('sv_graph') or {}).get('state') == 'verified' for x in (aa, ab, ac)),
        (same_bytes, diff[:8], [(x[0].get('sv_graph') or {}).get('state') for x in (aa, ab, ac)], buf.getvalue()[-400:]))


def t_reg_fixture():
    """★ 10-28 밤 PC5 봉인 전 남은 #5 (REPORT_C_decisions §4) — 시험 고정물 등록 사본의 계획 숫자 블록 = §2-1 자리 (§2-1 머리와 §2-1b 머리 사이) · 표지 각
    하나 · 봉인된 등록 (블록이 §2-1 에 이미 있는 글) 의 사본도 표지 각 하나 · 블록 = 이 계획 (사슬 plan_doc_problem None) — 옛 = 사본 끝에 덧붙임."""
    pp, _sp, rp = make_plan_and_reg()
    plan = json.load(open(pp, encoding='utf-8'))
    sha = hashlib.sha256(open(pp, 'rb').read()).hexdigest()
    b, e = RR.PLAN_DOC_BEGIN, RR.PLAN_DOC_END
    t = open(rp, encoding='utf-8').read()
    first = (t.count(b), t.count(e), 0 <= t.find('### 2-1. ') < t.find(b) < t.find('### 2-1b.'))
    lines = open(REG_DOC, encoding='utf-8').read().splitlines()
    hit = [i for i, ln in enumerate(lines) if '계획 숫자 블록 = 이 줄 바로 아래' in ln]
    sealed = ('\n'.join(lines[:hit[0] + 1] + ['', RR.plan_doc_block(dict(plan, max_ladder_points=15))] + lines[hit[0] + 1:]) + '\n'
              if len(hit) == 1 else '')
    q = os.path.join(TD, 'reg_sealed_e17.md')
    with open(q, 'w', encoding='utf-8') as f:
        f.write(reg_text(sealed, sha, '0' * 64, plan))
    s2 = open(q, encoding='utf-8').read()
    second = (len(hit), s2.count(b), s2.count(e), 0 <= s2.find('### 2-1. ') < s2.find(b) < s2.find('### 2-1b.'), RR.plan_doc_problem(q, plan))
    chk('E17 ★ 10-28 밤 PC5 §4 #5 시험 고정물 (make_plan_and_reg) 등록 사본 — 계획 숫자 블록 = §2-1 자리 · 표지 각 하나 · 봉인된 등록 (§2-1 에 블록) 의 사본도 표지 '
        '각 하나 · 블록 = 이 계획 (plan_doc_problem None)', first == (1, 1, True) and second == (1, 1, 1, True, None), (first, second))


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
        for tag, fn in (('E1', t_ladder), ('E6', t_prod_form), ('E8', t_zero_floor), ('E9', t_short_ceiling), ('E10', t_sv_census_dbe),
                        ('E11', t_no_venv), ('E12', t_graph_source), ('E13', t_runner_kill), ('E13t', t_timeout_kill),
                        ('E13p', t_parent_kill), ('E14', t_ledger), ('E15', t_resume_real), ('E16', t_merge_fetch_real),
                        ('E17', t_reg_fixture)):
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
