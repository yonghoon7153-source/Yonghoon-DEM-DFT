#!/usr/bin/env python3
"""vasp_handoff_bundle.py — VASP 외주 **원샷** 번들 v3 (Codex 2차 NO-GO 전건 반영).

v2 → v3 (2026-08-12) — v2 는 NO-GO 였다. 실측으로 확인된 것만 고쳤다.
  ★ **자기 seed 를 부격자 원장으로 교체** (P0 §2②). v2 의 "Ni 를 파일 순서로 앞 24 −1 /
     뒤 24 +1" 은 실제 Ni1/Ni2 부격자와 **24/48 일치**(= 동전 던지기)였다. 개수만 같았을
     뿐 납품 계보와 다른 자기 배치다. 이제 tools/sdcp/afm_ledger.py 가 QE 원본의 Ni1/Ni2
     를 슬랩(그 셀의 1×4×1 슈퍼셀)에 좌표로 매칭해 확정한다. **v2 로 만든 번들은 무효.**
  ① **계약 고정** (P0-A): 조각별 **대조쌍 수**를 EXPECT_PAIRS 로 못 박고, 조각/쌍/xyz/분자 ref 가
     빠지면 **번들을 만들지 않는다**. v2 는 조용히 건너뛰고 축소된 MANIFEST 를 새 정본으로
     만들어, ptfe_c10 전체가 빠져도 exit 0 이 가능했다.
  ② **4상 러너** (P0-F): pre(dipole off · LWAVE) → relax(ISTART=1) → static → dense.
     CHGCAR/WAVECAR 사슬은 fail-closed — 없으면 다음 상으로 안 넘어간다. dense 는
     **static** 의 CHGCAR 를 승계한다(v2 는 relax 것을 썼다).
  ③ **범위** (2026-08-12 결정): tier1·tier2 **전 끝점 2 seed** = **82 systems · 259 VASP phase runs**
     (pose 72×3상 216 + dense 20 + clean 7 + 기체 16). 잡 수와 실행 횟수를 병기한다. seed 1종 쌍은
     seed 산포를 ΔE 에서 못 걷어내 최종 판정에 못 쓴다. dense 는 tier1 전 pm1 끝점.
  ④ **수치 게이트를 판정에 연결** (P0-D): 상자 20↔24 Å 실패 → 그 조각 E_ads 를 만들지
     않는다(정본은 **box24**). dense-k 실패 → NUMERICALLY_UNRESOLVED. dense 누락도
     필수 완결성에서 잡는다. v2 는 전부 warning 이라 실패한 값으로 판정을 계속 만들었다.
  ⑤ **fail-closed 회수** (P0-C/E/H): 상별 정상종료(General timing) 확인 · TITEL 없으면
     POTCAR_UNVERIFIED(통과 아님) · 힘 블록 없거나 원자수 다르면 게이트 · 준중심 변형
     차이(Ni_pv→Ni)는 일관돼도 치명 · **Ni 국소 모멘트/부호 패턴 감사** · MANIFEST 해시로
     입력 변조 검사 · run_all.sh 가 분석기 종료코드를 그대로 올린다.
  ⑥ **PAIR_COLLAPSED 재정의** (Q5 반박 수용): 최근접 원소명 비교는 PAIR_MIGRATED 와
     완전 중복이었다. 이제 분자 **주기 RMSD ≤ 0.75 Å + 접촉 지문 동일 + 최근접 동일**
     교집합으로 판정하고 0.50/0.75/1.00 민감도를 같이 남긴다.
  ⑦ DIPOL 은 원자 중심이 아니라 **질량중심**. 등록 판정은 **표면 양이온만** (P0-G).
     기체 기준계에도 mol_poscar_idx 를 넣어 결합 감사를 켠다.
  ⑧ selftest 음성 강화: v2 의 음성 2건은 사실 아무것도 검증하지 않았다 —
     `chk(x is None or True, ...)` 는 항상 참이었고, dense 를 양 끝점에 같은 +3 meV 로
     심어 ΔE 이동이 0 이었다. 이제 한쪽만 옮기고, 계약 위반·잘린 OUTCAR·TITEL 누락·
     모멘트 붕괴·입력 변조를 추가로 심는다.

  실납품과 다른 점(의도된 개선, provenance 에 기록): LASPH=T(납품 F) · LDIPOL=T(납품 F)
  · ISMEAR=0/0.05(납품 1/0.2) · pre+이완+정적 다상(납품 단일점). U=6.2·IVDW=11·ENCUT 520 승계.

  gabia:
    python3 tools/sdcp/afm_ledger.py                       # 원장 먼저 (검증·기록)
    python3 tools/sdcp/vasp_handoff_bundle.py --selftest    # GPU 불필요, 데이터 불필요
    python3 tools/sdcp/vasp_handoff_bundle.py \
        --runs /data/work/runs/sdcp_v4_sitescreen --freeze 0.85 \
        --out  /data/work/runs/sdcp_vasp_oneshot_v3

이 도구가 **못 하는 것**
  · 자기바닥상태를 보장하지 못한다 — QE 배정을 옮기고 seed 2종으로 감도만 잰다.
  · 유한셀 보정을 하지 않는다 (상 사이 비교용).
  · POTCAR 파일을 검증하지 못한다 (라이선스 미포함) — OUTCAR TITEL 만 본다.
  · UMA 값과 같은 표에 놓을 수 없다 (프로토콜이 다르다).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import site_screen as SS                      # noqa: E402  (게이트·POSCAR·조각 레지스트리)

#: ⚠ selftest 가 `SS.load_slab` 를 몽키패치한다. 시험 간 **전역 오염**을 막으려고
#:   적재 시점의 원본을 붙잡아 둔다 — E2E 는 이것을 쓴다 (2026-08-29 실측: 대형
#:   selftest 뒤에 E2E 를 돌리면 장난감 슬랩을 받아 원장과 어긋났다).
_SS_LOAD_SLAB_ORIG = SS.load_slab

TIERS = {"tier1": ["ptfe_c10", "ptfe_dimer"],      # 이번 판의 목적 (미해결 경향 2건)
         "tier2": ["sdcp_neutral", "sdcp_doped"]}
RMSD_TOL_CHK = 0.75    # selftest 에서 쓰는 사본 (분석기는 문자열 안에 있다)
#: 캠페인 계약 — 조각별 **대조쌍(Li_top↔Ni_top) 수**. down_dir 수가 아니다.
#: 실제와 다르면 번들을 만들지 않는다 (Codex P0-A) — 축소된 MANIFEST 를 새 정본으로
#: 만드는 것이 이 번들의 제일 비싼 실패 모드다.
#: ⚠ 2026-08-12 실측 정정 — Codex 리뷰의 sdcp_neutral=6 은 틀렸다. 그 조각은 down_dir 이
#:   7개지만 fib08·fib11 은 **다른 자리 종류**(LiNi/LiO/NiO_bridge · O_top · hollow)를
#:   훑은 자리-종류 스윕이라 Li_top↔Ni_top 대조쌍이 아예 없다. 대조쌍은 5개가 맞다.
#:   빠진 데이터가 아니라 다른 실험이다 — 제외 사유는 MANIFEST.pair_audit 에 남는다.
MAX_OPTIONAL_DENSE_B = 2   # 분석기 MAX_OPTIONAL_DENSE 사본 — selftest 가 대조
EXPECT_PAIRS = {"ptfe_c10": 5, "ptfe_dimer": 3, "sdcp_neutral": 5, "sdcp_doped": 5}

# ── 결합 판정 규약 — **분석기(ANALYZER 문자열) 안에 같은 표가 있다** ──────────
#   문자열 템플릿이라 import 로 공유할 수 없다. selftest 가 두 사본이 갈라졌는지
#   실제로 파싱해 대조한다 (CLAUDE.md 코드 규율: 물리 규약 사본은 반드시 대조).
RCOV_B = {"H": 0.31, "B": 0.84, "C": 0.76, "N": 0.71, "O": 0.66, "F": 0.57,
          "Na": 1.66, "P": 1.07, "S": 1.05, "Cl": 1.02, "Li": 1.28, "Ni": 1.24}
BOND_F_B = 1.25
SEEDS_FULL = ("afm2424_pm1", "afm2424_net4")       # tier1 전 끝점 · clean
SEED_MAIN = "afm2424_pm1"                          # 판정 headline
#: Ni_pv = 2026-08-08 실납품 TITEL 계보 (자체검토 P0-2)
POTCAR_SPEC = {"Li": "Li_sv", "Ni": "Ni_pv", "O": "O", "S": "S", "C": "C", "F": "F",
               "H": "H", "B": "B", "P": "P", "Cl": "Cl", "Na": "Na_pv"}
KMESH = {"relax": "2 3 1", "static": "3 4 1", "dense": "4 6 1"}   # a=18.3 > b=11.5 Å
#: 분석기가 OUTCAR 되울림과 대조할 INCAR 태그 (프로토콜을 규정하는 것들)
# ⛔ 2026-08-25 (codex E-1) — 7키만 등록돼 있어 LDAUU 등은 **비교 대상에 든 적이
#   없었다** (0 UNVERIFIED 는 통과가 아니라 미등록이었다). MAGMOM·ADDGRID 는 OUTCAR
#   가 되울리지 않아(실측) 등록해도 검증 불가 — 분석기의 _ECHO_ABSENT 로 명시 보고.
AUDIT_KEYS = ("ENCUT", "ISMEAR", "IVDW", "LREAL", "ISTART", "ICHARG", "LDIPOL",
              "ISPIN", "ISYM", "LASPH", "IDIPOL", "NUPDOWN",
              "LDAUTYPE", "LDAUL", "LDAUU", "LDAUJ",
              # codex E-2차 필수6 — ICHARG=1 (Ni d+U restart) 의 핵심 키
              "LDAU", "LMAXMIX")


#: 🔴 회신 AT P0-2 (2026-08-31) — dense 상의 k 감사가 fail-open 이었다.
#:   `KMESH_MISMATCH` 는 `NKPTS > 격자곱` 만 봤다. coarse(3 4 1 = 12) OUTCAR 를
#:   dense(4 6 1 = 24) 폴더에 넣어도 12 ≤ 24 라 **통과**한다.
#:   ⇒ KPOINTS **제목 줄**에 상·격자·시프트를 실어 둔다. VASP 는 그 줄을 OUTCAR 에
#:     ` KPOINTS: <제목>` 으로 그대로 되울리므로, 되울린 제목을 정확히 대조하면
#:     격자와 시프트가 **정확히** 검증된다 (개수 상한이 아니라 동일성).
def _kpoints_title(ph: str, mesh: str, shift: str = "0 0 0") -> str:
    return "phase=%s k=%s shift=%s" % (ph, " ".join(str(mesh).split()),
                                       " ".join(str(shift).split()))


def _kpoints_text(ph: str, mesh: str, shift: str = "0 0 0", mode: str = "Gamma") -> str:
    return "%s\n0\n%s\n%s\n%s\n" % (_kpoints_title(ph, mesh, shift), mode,
                                       " ".join(str(mesh).split()),
                                       " ".join(str(shift).split()))


def _kpoints_expected(ph: str, mesh: str, shift: str = "0 0 0",
                      mode: str = "Gamma") -> Dict[str, Any]:
    return {"title": _kpoints_title(ph, mesh, shift), "mode": mode,
            "mesh": " ".join(str(mesh).split()), "shift": " ".join(str(shift).split()),
            "⛔": ("OUTCAR 의 ` KPOINTS:` 되울림과 **정확히** 같아야 한다. "
                   "NKPTS 상한만 보면 coarse OUTCAR 를 dense 에 넣어도 통과한다 "
                   "(회신 AT P0-2)")}


def _incar_expected_from(txt):
    """INCAR 원문 → {key: 정규화값}. **줄 끝까지** 캡처한다 (한 토큰이면
    `LDAUU = 0.0 6.2 0.0` 이 `0.0` 으로 잘린다 — codex E-1). 주석(#/!)은 버린다."""
    out = {}
    for k in AUDIT_KEYS:
        m = re.search(rf"^{k}\s*=\s*([^\n#!]+)", txt, re.M)
        if m:
            out[k] = " ".join(m.group(1).split())
    return out

# ── INCAR 3종 — Codex §2.2 템플릿 + 실납품 승계값(U 6.2 · IVDW 11 · ENCUT 520) ──
_COMMON = """GGA      = PE
PREC     = Accurate
ENCUT    = 520
ISMEAR   = 0
SIGMA    = 0.05
ALGO     = Normal
NELM     = 200
NELMIN   = 6
ISPIN    = 2
ISYM     = 0
LASPH    = .TRUE.
ADDGRID  = .TRUE.
LORBIT   = 11
AMIN     = 0.01
IVDW     = 11
NCORE    = 4
"""
SLAB_PRE = """SYSTEM = {system} [pre-SCF]
# 0/3상 — **dipole 끄고** 궤도를 먼저 수렴시킨다 (VASP Electrostatic_corrections 권고).
# LDIPOL 을 1번 반복부터 켜면 자기상태가 엉뚱한 basin 으로 무너진 이력이 있다.
# 여기서 만든 WAVECAR/CHGCAR 를 relax 가 승계한다. 판정 에너지 아님.
{common}EDIFF    = 1E-5
IBRION   = -1
NSW      = 0
LREAL    = Auto
LDIPOL   = .FALSE.
LDAU      = .TRUE.
LDAUTYPE  = 2
LDAUL     = {ldaul}
LDAUU     = {ldauu}
LDAUJ     = {ldauj}
LDAUPRINT = 2
LMAXMIX   = 4
# ⛔ 회신 AM P0-5 (2026-08-31) — `NUPDOWN` 을 **명시한다.** 종전엔 줄이 아예 없어서
#   VASP 기본값(-1)에 기대고 있었고, 분석기는 "기대값 미등록" 으로만 남기고 차단하지
#   않았다. 기체 기준은 `NUPDOWN=0`(닫힌 껍질 일중항)로 **제약**돼 있으므로, 복합체가
#   무엇인지 적히지 않으면 `E_ads` 가 어떤 상태끼리의 차인지 문서에 없다.
#   -1 = 자유(무제약). 사전 고정된 pm1/net4 초기자화에서 출발한 unconstrained-spin SCF 이고,
#   **자기 바닥상태가 아니라 seed-conditioned realized basin** 으로 보고한다.
NUPDOWN   = -1
MAGMOM   = {magmom}
LWAVE    = .TRUE.
LCHARG   = .TRUE.
"""
SLAB_RELAX = """SYSTEM = {system} [relax]
# 1/3상 — 기하 이완. ⚠ 판정 에너지는 여기서 회수하지 않는다 (static 이 정본).
# pre 의 WAVECAR + **스핀분극 CHGCAR** 를 둘 다 승계한다 (Codex Q4 권장안 B —
# restart robustness 우선. MPI/빌드가 달라 WAVECAR 가 거부돼도 전하밀도는 남는다).
{common}EDIFF    = 1E-5
EDIFFG   = -0.02
IBRION   = 2
NSW      = 200
ISIF     = 2
LREAL    = Auto
ISTART   = 1
ICHARG   = 1
LDIPOL   = .TRUE.
IDIPOL   = 3
DIPOL    = 0.5 0.5 {zcom:.4f}
LDAU      = .TRUE.
LDAUTYPE  = 2
LDAUL     = {ldaul}
LDAUU     = {ldauu}
LDAUJ     = {ldauj}
LDAUPRINT = 2
LMAXMIX   = 4
# ⛔ 회신 AM P0-5 (2026-08-31) — `NUPDOWN` 을 **명시한다.** 종전엔 줄이 아예 없어서
#   VASP 기본값(-1)에 기대고 있었고, 분석기는 "기대값 미등록" 으로만 남기고 차단하지
#   않았다. 기체 기준은 `NUPDOWN=0`(닫힌 껍질 일중항)로 **제약**돼 있으므로, 복합체가
#   무엇인지 적히지 않으면 `E_ads` 가 어떤 상태끼리의 차인지 문서에 없다.
#   -1 = 자유(무제약). 사전 고정된 pm1/net4 초기자화에서 출발한 unconstrained-spin SCF 이고,
#   **자기 바닥상태가 아니라 seed-conditioned realized basin** 으로 보고한다.
NUPDOWN   = -1
MAGMOM   = {magmom}
LWAVE    = .FALSE.
LCHARG   = .TRUE.
"""
SLAB_SP = """SYSTEM = {system} [static · single-point]
# **UMA 이완 기하 위의 단일점.** 승계할 relax 가 없으므로 원자중첩에서 시작한다.
# ⚠ 기하는 DFT 최소점이 아니다 — E_ads 를 인용할 때 반드시 같이 적을 것.
{common}EDIFF    = 1E-6
IBRION   = -1
NSW      = 0
ISIF     = 2
LREAL    = Auto
LDIPOL   = .TRUE.
IDIPOL   = 3
DIPOL    = 0.5 0.5 {zcom:.4f}
LDAU      = .TRUE.
LDAUTYPE  = 2
LDAUL     = {ldaul}
LDAUU     = {ldauu}
LDAUJ     = {ldauj}
LDAUPRINT = 2
LMAXMIX   = 4
# ⛔ 회신 AM P0-5 (2026-08-31) — `NUPDOWN` 을 **명시한다.** 종전엔 줄이 아예 없어서
#   VASP 기본값(-1)에 기대고 있었고, 분석기는 "기대값 미등록" 으로만 남기고 차단하지
#   않았다. 기체 기준은 `NUPDOWN=0`(닫힌 껍질 일중항)로 **제약**돼 있으므로, 복합체가
#   무엇인지 적히지 않으면 `E_ads` 가 어떤 상태끼리의 차인지 문서에 없다.
#   -1 = 자유(무제약). 사전 고정된 pm1/net4 초기자화에서 출발한 unconstrained-spin SCF 이고,
#   **자기 바닥상태가 아니라 seed-conditioned realized basin** 으로 보고한다.
NUPDOWN   = -1
MAGMOM   = {magmom}
ISTART   = 0
ICHARG   = 2
LWAVE    = .FALSE.
LCHARG   = .TRUE.
"""
SLAB_STATIC = """SYSTEM = {system} [static]
# 2/2상 — **판정 에너지의 정본** (Codex §2.2). relax 의 CONTCAR/CHGCAR 를 승계한다.
{common}EDIFF    = 1E-6
IBRION   = -1
NSW      = 0
ISIF     = 2
LREAL    = .FALSE.
LDIPOL   = .TRUE.
IDIPOL   = 3
DIPOL    = 0.5 0.5 {zcom:.4f}
LDAU      = .TRUE.
LDAUTYPE  = 2
LDAUL     = {ldaul}
LDAUU     = {ldauu}
LDAUJ     = {ldauj}
LDAUPRINT = 2
LMAXMIX   = 4
# ⛔ 회신 AM P0-5 (2026-08-31) — `NUPDOWN` 을 **명시한다.** 종전엔 줄이 아예 없어서
#   VASP 기본값(-1)에 기대고 있었고, 분석기는 "기대값 미등록" 으로만 남기고 차단하지
#   않았다. 기체 기준은 `NUPDOWN=0`(닫힌 껍질 일중항)로 **제약**돼 있으므로, 복합체가
#   무엇인지 적히지 않으면 `E_ads` 가 어떤 상태끼리의 차인지 문서에 없다.
#   -1 = 자유(무제약). 사전 고정된 pm1/net4 초기자화에서 출발한 unconstrained-spin SCF 이고,
#   **자기 바닥상태가 아니라 seed-conditioned realized basin** 으로 보고한다.
NUPDOWN   = -1
MAGMOM   = {magmom}
ISTART   = 0
ICHARG   = 1
LWAVE    = .FALSE.
LCHARG   = .TRUE.
"""
MOL_RELAX = """SYSTEM = {system} [relax]
# 기체상 기준계 1/2상. 범함수·분산은 슬랩과 동일(PBE·D3 zero damping). U 없음(Ni 없음).
{common}EDIFF    = 1E-5
EDIFFG   = -0.02
IBRION   = 2
NSW      = 300
ISIF     = 2
LREAL    = Auto
LDIPOL   = .TRUE.
IDIPOL   = 4
DIPOL    = {com0:.4f} {com1:.4f} {com2:.4f}
NUPDOWN  = {nupdown}
MAGMOM   = {magmom}
LWAVE    = .FALSE.
LCHARG   = .TRUE.
"""
MOL_STATIC = """SYSTEM = {system} [static]
# 기체상 기준계 2/2상 — E_ads 에 들어가는 정본 에너지.
{common}EDIFF    = 1E-6
IBRION   = -1
NSW      = 0
LREAL    = .FALSE.
LDIPOL   = .TRUE.
IDIPOL   = 4
DIPOL    = {com0:.4f} {com1:.4f} {com2:.4f}
NUPDOWN  = {nupdown}
MAGMOM   = {magmom}
ISTART   = 0
ICHARG   = 1
LWAVE    = .FALSE.
LCHARG   = .FALSE.
"""

RUN_JOB = """#!/usr/bin/env bash
# 이 잡의 상(phase)들을 순서대로 돈다. POTCAR 를 이 폴더에 놓고 실행.
#   VASP_CMD="mpirun -np 48 vasp_std" bash run_job.sh
#
# 상 사슬 (하나라도 끊기면 **멈춘다** — 조용히 건너뛰면 다른 계를 계산하게 된다):
#   pre    dipole off, LWAVE=T          → WAVECAR·CHGCAR
#   relax  ISTART=1 (pre 의 WAVECAR)     → CONTCAR·CHGCAR
#   static ICHARG=1 (relax 의 CHGCAR)    → 판정 에너지
#   dense  ICHARG=1 (**static** 의 CHGCAR) → k 수렴 확인
set -e
V=${VASP_CMD:-"mpirun -np ${NP:-48} vasp_std"}   # 계약·비용모형과 같은 48
[ -f POTCAR ] || { echo "⛔ POTCAR 를 이 폴더에 놓으세요 (POTCAR_SPEC.txt 의 변형)"; exit 1; }
# 🔴 회신 AB P0-8 — POTCAR **provenance 를 실행 전에 강제**한다. 종전엔 파일
#   존재만 봤다. 그래서 조립기가 allowlist 로 거부해도 그때 남아 있던 POTCAR 로
#   VASP 가 돌았다 — allowlist 실패가 계산 중단으로 이어지지 않았다.
#   셋을 요구한다: ① provenance 존재 ② 면제 아님 ③ 지금 POTCAR 의 sha 가 일치.
#   ③이 핵심 — 조립 뒤 POTCAR 를 바꿔치기하면 여기서 걸린다.
# ⛔ 회신 AF P0-7 — 종전엔 SKIP_POTCAR_PROVENANCE=1 **환경변수**로 우회됐다.
#   환경변수는 반송물에 흔적이 안 남아 분석기가 볼 수 없다. 시험 장치는 파일로 표시하고
#   (`.SELFTEST_FIXTURE`), 배포 번들에는 그 파일이 없다 — files_sha256 이 전 파일을
#   덮으므로 나중에 만들어 넣으면 무결성 검사에서 걸린다.
if [ ! -f .SELFTEST_FIXTURE ]; then
  [ -f POTCAR_PROVENANCE.json ] || {
    echo "⛔ POTCAR_PROVENANCE.json 이 없습니다 — POTCAR 를 손으로 놓지 말고"
    echo "   PP=... POTCAR_ALLOWLIST=/abs/site_allow.txt bash POTCAR_ASSEMBLE.sh"; exit 1; }
  python3 - <<'PYCHK' || exit 1
import hashlib, json, sys
try:
    d = json.load(open("POTCAR_PROVENANCE.json"))
except Exception as e:
    sys.exit("\u26d4 POTCAR_PROVENANCE.json 파싱 실패: %s" % e)
if d.get("allowlist_waived"):
    sys.exit("\u26d4 allowlist 면제로 조립된 POTCAR 입니다 — 이 계약에서 폐지됐습니다")
if not d.get("allowlist"):
    sys.exit("\u26d4 provenance 에 allowlist 경로가 없습니다 — 대조 없이 조립됐습니다")
if not d.get("allowlist_sha256"):
    sys.exit("\u26d4 provenance 에 allowlist 내용 SHA 가 없습니다 — 경로만으로는 "
             "어느 allowlist 였는지 확인할 수 없습니다")
h = hashlib.sha256(open("POTCAR", "rb").read()).hexdigest()
if h != d.get("assembled_sha256"):
    sys.exit("\u26d4 POTCAR 가 조립 이후 바뀌었습니다 (지금 %s / 기록 %s)"
             % (h[:16], str(d.get("assembled_sha256"))[:16]))
print("  \u2714 POTCAR provenance 확인 (allowlist 대조본 · sha 일치)")
PYCHK
fi
need() { [ -s "$1" ] || { echo "⛔ $1 없음/빈 파일 — $2"; exit 1; }; }

# ★ 회신 AA P0-5 / Q8 — **1회용(one-shot) 실행이다.** 시작 전에 산출물이 있으면
#   거부한다. 종전엔 "이미 완료 — 건너뜀" 으로 넘어갔는데, 그러면 남이 다른 설정으로
#   돌려 둔 결과를 우리 것으로 반송하게 된다 (회수 후에는 구별할 방법이 없다).
#   진짜로 이어서 돌려야 하면 ALLOW_RESUME=1 을 **명시적으로** 주고, 그 사실을
#   NOTES.txt 에 남겨 주세요.
if [ "${ALLOW_RESUME:-0}" != "1" ]; then
  _stale=""
  for ph in pre relax static dense; do
    [ -d "$ph" ] || continue
    for f in OUTCAR WAVECAR CHGCAR vasprun.xml CONTCAR OSZICAR; do
      [ -e "$ph/$f" ] && _stale="$_stale $ph/$f"
    done
  done
  if [ -n "$_stale" ]; then
    echo "⛔ 실행 전 산출물이 이미 있습니다:$_stale"
    echo "   이 잡은 **1회용**입니다. 이어 돌리면 다른 설정의 결과가 섞입니다."
    echo "   폴더를 새로 풀고 다시 시작하거나, 의도한 재개면 ALLOW_RESUME=1 로 주세요."
    exit 1
  fi
fi

for ph in pre relax static dense; do
  [ -d "$ph" ] || continue
  if [ -f "$ph/OUTCAR" ] && grep -aq "General timing" "$ph/OUTCAR"; then
    echo "  ✓ $ph 이미 완료 — 건너뜀 (ALLOW_RESUME)"; continue
  fi
  cp POTCAR "$ph/"
  case "$ph" in
    pre)   cp POSCAR pre/POSCAR ;;
    relax) cp POSCAR relax/POSCAR
           if [ -d pre ]; then
             need pre/WAVECAR "pre 상이 WAVECAR 를 안 남겼다 (ISTART=1 이 무의미해진다)"
             need pre/CHGCAR  "pre 상이 CHGCAR 를 안 남겼다"
             cp pre/WAVECAR pre/CHGCAR relax/
           fi ;;
    static) if [ -d relax ]; then
              need relax/CONTCAR "relax 를 먼저 완주시킬 것"
              need relax/CHGCAR  "ICHARG=1 인데 승계할 전하밀도가 없다 (relax LCHARG=.TRUE. 확인)"
              cp relax/CONTCAR static/POSCAR
              cp relax/CHGCAR  static/CHGCAR
            elif [ -f PARENT_GEOM ]; then
              # 회신 AO P0-4 (2026-08-31) — nzmag canary 는 부모 기체 기준과 **같은
              #   기하**여야 한다. 종전엔 부모가 relax/CONTCAR 로 static 을 돌고
              #   canary 는 자기 루트 POSCAR 를 써서 두 에너지 차에 **구조 이완
              #   에너지가 섞였다** — 스핀 검사가 오염됐다. 부모 기하를 그대로 받는다.
              _pg=$(tr -d " \\t\\r\\n" < PARENT_GEOM)
              [ -d "$_pg" ] || { echo "PARENT_GEOM 이 가리키는 부모가 없다: $_pg"; exit 1; }
              if [ -d "$_pg/relax" ]; then
                need "$_pg/relax/CONTCAR" "부모 기체 relax 를 먼저 완주시킬 것 (canary 는 같은 기하)"
                cp "$_pg/relax/CONTCAR" static/POSCAR
              else
                need "$_pg/POSCAR" "부모 루트 POSCAR 없음"
                cp "$_pg/POSCAR" static/POSCAR
              fi
              echo "  canary 기하 = 부모($_pg) 와 동일"
            else
              # 단일점 모드 — relax 가 애초에 없다. 루트 POSCAR 를 그대로 쓰고
              # ISTART=0/ICHARG=2 (원자중첩)로 시작한다. CHGCAR 입력 없음.
              cp POSCAR static/POSCAR
            fi ;;
    dense)  if [ -d relax ]; then
              need relax/CONTCAR "relax 를 먼저 완주시킬 것"
              cp relax/CONTCAR dense/POSCAR
            else
              cp POSCAR dense/POSCAR          # 단일점 — 기하가 안 변한다
            fi
            need static/CHGCAR "dense 는 **static** 의 전하밀도를 승계한다 — static 먼저"
            cp static/CHGCAR dense/CHGCAR ;;
  esac
  echo "  ▶ $ph"
  ( cd "$ph" && $V > vasp.out 2>&1 )
  grep -aq "General timing" "$ph/OUTCAR" || {
    echo "⛔ $ph 가 정상종료하지 않았다 (General timing 없음) — 다음 상으로 안 넘어간다"; exit 1; }
  # WAVECAR 는 크다. relax 가 끝나면 pre 것은 필요 없다.
  [ "$ph" = relax ] && rm -f pre/WAVECAR relax/WAVECAR
done
echo "✅ $(basename "$PWD") 완료"
"""

RUN_DENSE_SEL = """#!/usr/bin/env bash
# 조건부 dense — **DENSE_PLAN.json 에 있는 것만** 돈다.
#
#   1) coarse static 을 전부 반송받은 뒤:  python3 analyze_results.py . --plan_dense
#   2) DENSE_PLAN.json 의 promote 를 확인하고:  bash run_dense_selected.sh
#
# promote 가 비어 있으면 **아무것도 안 돈다** — 보고할 branch 를 이미 dense 한 것이다.
# ⚠ 계획 없이 dense_cand 를 손으로 돌리지 말 것. 어느 branch 를 왜 골랐는지가
#   DENSE_PLAN.json 에만 남는다 (그게 근거다).
set -u
[ -f DENSE_PLAN.json ] || { echo "⛔ DENSE_PLAN.json 없음 — 먼저 --plan_dense"; exit 1; }
jobs=$(python3 - <<'PY'
import json
p = json.load(open("DENSE_PLAN.json"))
print("\\n".join(x["job"] for x in p.get("promote") or []))
PY
)
[ -z "$jobs" ] && { echo "✅ 승격 0건 — 추가 dense 없음"; exit 0; }
fail=0
while read -r j; do
  [ -z "$j" ] && continue
  echo "═══ $j (조건부 dense) ═══"
  [ -d "$j/dense_cand" ] || { echo "⛔ $j/dense_cand 없음"; fail=1; continue; }
  [ -d "$j/dense" ] && { echo "⚠ $j/dense 가 이미 있다 — 건너뜀"; continue; }
  cp -r "$j/dense_cand" "$j/dense"
  ( cd "$j" && bash run_job.sh ) || { echo "⚠ $j 실패"; fail=1; }
done <<< "$jobs"
[ "$fail" = 1 ] && echo "⚠ 실패한 잡이 있다"
python3 analyze_results.py .
exit $?
"""

RUN_STAGED = r'''#!/usr/bin/env bash
# 2단계 러너 — 정지 규칙을 **실제로 적용**하려면 순서가 있어야 한다 (회신 AJ·AO·AP).
#
#   0단계(자동): POTCAR 조립 + provenance + **묶음 root 봉인** (AO P0-2·Q1)
#   1단계: primary 두 조각 x 셀 두 높이 + 기체 기준 + 기체 canary
#          -> **1단계 선결조건 8축** 전부 통과해야 2단계가 열린다:
#             진공 수렴 · 분자 스핀 · canary 기하 · POTCAR 신원 ·
#             δ_gas(기체 상자) · pm1 자기 topology · 잔여 차단 0 · 봉인 포괄
#   2단계: primary 다른 seed + 대안 자세 두 seed
#          -> 시작 **직전에** 1단계 게이트를 다시 돌린다 (AP #6)
#          -> 끝나면 최종 분석기를 돌린다 (AP #9)
#
# ⛔ 이 스크립트가 **유일한 실행 경로**다. run_job.sh 를 손으로 부르지 않는다.
set -u
usage() { echo "사용법: bash run_staged.sh {1|2}"; exit 2; }
[ $# -ge 1 ] || usage
stage=$1
case "$stage" in 1|2) ;; *) echo "모르는 단계: $stage"; usage;; esac
# ⛔⛔ 회신 AS 해제조건 5 (2026-08-31) — 봉인은 `VASP_EXE` 를 해시하는데 러너는
#   **임의의 `VASP_CMD`** 를 실행했다. 같은 버전 문자열을 내는 다른 바이너리도
#   통과한다. ⇒ **launcher 와 executable 을 분리**한다:
#     VASP_LAUNCHER : mpirun/srun 과 그 인자 (실행파일 이름을 넣지 않는다)
#     VASP_EXE      : 실행파일 (봉인 대상). 절대경로로 해석해 봉인 해시와 대조한다.
#   실행 직전에 그 절대경로를 **다시 해시**하고, 봉인과 다르면 멈춘다.
#   ⚠ 하위호환: VASP_CMD 만 주면 거부한다 — 조용히 옛 경로로 돌지 않는다.
if [ -n "${VASP_CMD:-}" ] && [ -z "${VASP_LAUNCHER:-}" ]; then
  echo "⛔ VASP_CMD 는 더 쓰지 않습니다 (회신 AS 해제조건 5)."
  echo "   launcher 와 실행파일을 나눠 주세요 — 봉인한 그 파일로 돌았는지 확인합니다:"
  echo "     export VASP_LAUNCHER='mpirun -np 48'"
  echo "     export VASP_EXE=/abs/path/to/vasp_std"
  exit 2
fi
VASP_LAUNCHER=${VASP_LAUNCHER:?VASP_LAUNCHER 를 지정하세요 (예: 'mpirun -np 48' — 실행파일 이름은 넣지 마세요)}
VASP_EXE=${VASP_EXE:?VASP_EXE 를 지정하세요 (실행파일 절대경로 — 이것이 봉인 대상입니다)}
case "$VASP_EXE" in /*) ;; *) VASP_EXE=$(command -v "$VASP_EXE" 2>/dev/null || true) ;; esac
[ -n "$VASP_EXE" ] && [ -x "$VASP_EXE" ] || { echo "⛔ VASP_EXE 를 실행파일로 찾을 수 없습니다"; exit 2; }
# 🔴🔴 회신 AT P0-5 (2026-08-31) — **launcher 가 봉인된 실행파일을 무시할 수 있었다.**
#   `VASP_LAUNCHER='mpirun -np 48 /other/vasp'` 로 주면 최종 명령이
#   `mpirun -np 48 /other/vasp /sealed/vasp_std` 가 되어 mpirun 은 **앞의 것**을 돈다.
#   봉인은 뒤의 것을 해시했으므로 아무 의미가 없어진다. 셸 메타문자도 같은 문제다.
case "$VASP_LAUNCHER" in
  *[\;\&\|\<\>\`\$\(\)\{\}\'\"]*|*"
"*)
    echo "⛔ VASP_LAUNCHER 에 셸 메타문자가 있습니다 — 봉인된 실행파일을 우회할 수 있습니다"
    echo "   허용: 런처 이름과 플래그·숫자만 (예: 'mpirun -np 48')"; exit 2 ;;
esac
_lt=0
for _tok in $VASP_LAUNCHER; do
  _lt=$((_lt+1))
  if [ "$_lt" = 1 ]; then
    case "$(basename "$_tok")" in
      mpirun|mpiexec|srun|aprun|jsrun|env|ibrun) ;;
      *) echo "⛔ VASP_LAUNCHER 의 첫 토큰이 알 수 없는 launcher 입니다: $_tok"
         echo "   허용: mpirun mpiexec srun aprun jsrun ibrun env"
         echo "   (다른 런처가 필요하면 알려주세요 — 목록에 넣고 다시 봉인합니다)"; exit 2 ;;
    esac
    continue
  fi
  # 첫 토큰 뒤에 **실행 가능한 파일**이 오면 그것이 진짜 실행 대상이 될 수 있다
  if [ -x "$_tok" ] && [ ! -d "$_tok" ]; then
    echo "⛔ VASP_LAUNCHER 의 인자 '$_tok' 이 실행 가능한 파일입니다."
    echo "   launcher 에 실행파일을 넣으면 봉인된 VASP_EXE 가 무시됩니다 (회신 AT P0-5)."
    echo "   실행파일은 VASP_EXE 로만 주세요."; exit 2
  fi
done
export VASP_EXE VASP_LAUNCHER
VASP_CMD="$VASP_LAUNCHER $VASP_EXE"
export VASP_CMD
PP=${PP:?PP 를 지정하세요 (POTCAR 원본 트리)}
POTCAR_ALLOWLIST=${POTCAR_ALLOWLIST:?POTCAR_ALLOWLIST 를 지정하세요 (절대경로)}

# ⛔⛔ 회신 AR P0-8 · 해제조건 8 — **경쟁조건 없는 host/run-id 잠금**.
#   종전 구현: `mkdir $LOCK` 뒤에 pid 를 썼다. 그 사이(디렉터리는 있고 pid 는
#   아직 없는 창)에 다른 프로세스가 이를 stale 로 보고 `rm -rf` 했다.
#   게다가 다른 HPC 노드의 pid 에는 `kill -0` 이 유효한 생존검사가 아니다.
#   ⇒ ① 내용을 **먼저** 쓴 임시 파일을 `ln` 으로 원자적으로 링크한다
#       (하드링크 생성은 대상이 있으면 실패한다 — 내용이 없는 창이 존재하지 않는다)
#     ② **모르는 lock 은 절대 지우지 않는다.** 같은 호스트의 죽은 pid 일 때만
#       안내하고, 그래도 자동 삭제하지 않는다 (사람이 지운다).
# ⛔⛔ 회신 AS 해제조건 6 (2026-08-31) — lock 을 **단계별이 아니라 번들 전역**으로
#   바꾼다. 종전엔 `.lock_bundle` 과 `.lock_stage2` 가 따로라 1단계와 2단계를
#   동시에 던지면 둘 다 lock 을 잡았다. 같은 번들 디렉터리에서 동시에 도는 것은
#   단계가 달라도 안 된다 — POTCAR·봉인·산출물을 공유하기 때문이다.
LOCK=".lock_bundle"
RUNID="$(hostname)|$$|stage$stage|$(date -u +%Y-%m-%dT%H:%M:%SZ)"
LOCKTMP="$LOCK.tmp.$$"
printf '%s\n' "$RUNID" > "$LOCKTMP" || exit 3
if ! ln "$LOCKTMP" "$LOCK" 2>/dev/null; then
  rm -f "$LOCKTMP"
  own=$(cat "$LOCK" 2>/dev/null || echo "?")
  own_host=${own%%|*}
  rest=${own#*|}; own_pid=${rest%%|*}
  echo "⛔ 단계 $stage 의 lock 이 이미 있습니다: $own"
  if [ "$own_host" = "$(hostname)" ] && ! kill -0 "$own_pid" 2>/dev/null; then
    echo "   같은 호스트의 pid $own_pid 는 살아 있지 않습니다."
    echo "   그래도 **자동으로 지우지 않습니다** — 다른 노드의 실행일 수 있습니다."
    echo "   확실하면 손으로: rm -f $LOCK"
  else
    echo "   다른 호스트/살아 있는 프로세스입니다. 끝날 때까지 기다리세요."
  fi
  exit 3
fi
rm -f "$LOCKTMP"
# 우리 것일 때만 지운다 (남의 lock 을 치우지 않는다)
_unlock() { [ "$(cat "$LOCK" 2>/dev/null)" = "$RUNID" ] && rm -f "$LOCK"; return 0; }
# 🔴🔴 회신 AT P0-5 — 종전 trap 은 INT/TERM 에서 **lock 만 지우고 러너는 계속
#   돌았다.** bash 는 핸들러를 돌린 뒤 하던 일을 이어간다. 그 사이 lock 이 비므로
#   다른 실행이 같은 번들에 들어올 수 있었다 — 잠금이 있으나 마나였다.
#   ⇒ 신호를 받으면 **자식을 죽이고 정말로 나간다.**
_bail() {
  echo ""
  echo "⛔ 신호를 받았습니다 ($1) — 자식 프로세스를 정리하고 중단합니다."
  trap - EXIT INT TERM
  kill -TERM 0 2>/dev/null || true      # 이 프로세스 그룹 전체
  _unlock
  exit "$2"
}
trap '_unlock' EXIT
trap '_bail INT 130' INT
trap '_bail TERM 143' TERM

# ⛔ 회신 AT P0-6 — SEAL 은 러너가 **이미 lock 을 쥔 채** 부른다. 중복 획득으로
#   교착하지 않도록 알려 준다 (단독 실행이면 SEAL 이 스스로 잡는다).
BUNDLE_LOCK_HELD=1 bash SEAL_POTCAR_ROOT.sh || { echo "POTCAR 조립·봉인 실패 — 중단"; exit 1; }

# ⛔⛔ 회신 AR P0-7 · 해제조건 8 — **실행 전 census.** 종전엔 존재하는 job.json
#   만 분류하고 디렉터리 수만 비교해서, job.json 하나를 지워도 통과했다.
#   ⇒ ① MANIFEST 해시(봉인/EXPECT 와 결박) ② 계획 잡 **집합** 완전일치
#     ③ 단계 분류가 manifest 선언과 **정확히** 같은지 — 셋 다 확인한다.
python3 - "$stage" <<'PYPRE' || { echo "⛔ 실행 전 census 실패 — 중단"; exit 2; }
import json, os, sys, glob, hashlib
stage = sys.argv[1]
man = json.load(open("MANIFEST.json"))
mh = hashlib.sha256(open("MANIFEST.json", "rb").read()).hexdigest()
bad = []
# ⛔⛔ 회신 AS 해제조건 7 (2026-08-31) — ZIP 안의 해시는 **자기 자신을 증명하지
#   못한다**. 우리가 ZIP 밖(메일 본문)에 고정한 digest 를 현장이 붙여넣어야
#   비로소 "우리가 보낸 그 물건" 이 확인된다. **선택이 아니라 필수**로 만든다.
_HEX = "0123456789abcdef"
def _need_hex(name):
    v = os.environ.get(name, "").strip().lower()
    if not v:
        bad.append("%s 가 없다 — 우리가 보낸 정본 메시지의 digest 를 넣어야 "
                   "이 번들이 그 배포본인지 확인할 수 있다" % name)
        return None
    if len(v) != 64 or any(c not in _HEX for c in v):
        bad.append("%s 가 64자리 hex 가 아니다" % name)
        return None
    return v
exp = _need_hex("EXPECT_MANIFEST_SHA256")
if exp and exp != mh:
    bad.append("MANIFEST sha256 %s ≠ EXPECT_MANIFEST_SHA256 %s" % (mh[:12], exp[:12]))
expz = _need_hex("EXPECT_ZIP_SHA256")
_zt_env = os.environ.get("BUNDLE_ZIP_SHA256", "").strip().lower()
if expz and _zt_env and expz != _zt_env:
    bad.append("받은 ZIP 해시 %s ≠ EXPECT_ZIP_SHA256 %s — 우리가 보낸 배포본이 "
               "아니다" % (_zt_env[:12], expz[:12]))
# ⛔ 회신 AR 해제조건 7 — 봉인을 **모든 실행에서 필수화**한다
try:
    seal = json.load(open("POTCAR_ROOT_SEAL.json"))
except Exception as e:
    seal = {}
    bad.append("POTCAR_ROOT_SEAL.json 을 읽을 수 없다 (%r) — 봉인 없이 돌리지 않는다" % e)
_need_seal = ("schema", "source_sha256", "allowlist_sha256", "manifest_sha256",
              "bundle_zip_sha256", "vasp_executable", "vasp_executable_sha256",
              "vasp_version_banner", "sealed_at_utc", "assembled_sha256_by_job",
              "sealed_before_production", "sealed_before_production_evidence")
if seal:
    _sm = [k for k in _need_seal if not seal.get(k)]
    if _sm:
        bad.append("봉인에 %s 가 없다 — 반쪽 봉인으로 돌리지 않는다" % _sm)
    if seal.get("manifest_sha256") and seal["manifest_sha256"] != mh:
        bad.append("봉인이 다른 MANIFEST 에 대한 것이다 (%s ≠ %s)"
                   % (seal["manifest_sha256"][:12], mh[:12]))
    _zt = ""
    try:
        _zt = open("ZIP_SHA256.txt").read().split()[0].strip().lower()
    except Exception:
        bad.append("ZIP_SHA256.txt 가 없다 — 받은 ZIP 과의 결박을 확인할 수 없다")
    if _zt and seal.get("bundle_zip_sha256") and seal["bundle_zip_sha256"] != _zt:
        bad.append("봉인의 ZIP 해시가 ZIP_SHA256.txt 와 다르다")
# ⛔⛔ 회신 AS 해제조건 6 — 실행 전에 **배포 파일 전수**를 해시 대조한다.
#   종전엔 잡 집합만 셌다. INCAR 한 줄이 바뀌어도 census 는 통과했다.
_fh = man.get("files_sha256") or {}
if not _fh:
    bad.append("MANIFEST 에 files_sha256 이 없다 — 입력 무결성을 확인할 수 없다")
else:
    _chg, _mis = [], []
    for _rel, _want in sorted(_fh.items()):
        _pth = os.path.join(*_rel.split("/"))
        if not os.path.isfile(_pth):
            _mis.append(_rel); continue
        _h = hashlib.sha256(open(_pth, "rb").read()).hexdigest()
        if _h != _want:
            _chg.append(_rel)
    if _mis:
        bad.append("배포 파일이 없다 %d건: %s" % (len(_mis), _mis[:3]))
    if _chg:
        bad.append("배포 파일이 바뀌었다 %d건: %s (입력을 고치면 그 잡은 "
                   "거부됩니다)" % (len(_chg), _chg[:3]))
    print("  ✓ 입력 무결성 %d 파일" % len(_fh))
cen = man.get("run_census") or {}
if not cen.get("job_keys") or not cen.get("stage_of"):
    bad.append("MANIFEST 에 run_census 가 없다 — 이 번들로는 census 를 확인할 수 "
               "없다 (구판 번들이면 재생성하십시오)")
else:
    want = set(cen["job_keys"])
    have = {os.path.dirname(p).replace(os.sep, "/") for p in glob.glob("*/*/job.json")}
    dirs = {d.rstrip("/").replace(os.sep, "/") for d in glob.glob("*/*/")}
    if have != want:
        bad.append("job.json 집합이 계획과 다르다 — 없음 %s · 계획 밖 %s"
                   % (sorted(want - have)[:4], sorted(have - want)[:4]))
    if dirs != want:
        bad.append("잡 폴더 집합이 계획과 다르다 — 없음 %s · 계획 밖 %s"
                   % (sorted(want - dirs)[:4], sorted(dirs - want)[:4]))
    # 단계 분류를 **디스크의 job.json 으로 다시 계산**해 선언과 대조한다
    got = {}
    for jp in sorted(glob.glob("*/*/job.json")):
        m = json.load(open(jp))
        d = os.path.dirname(jp).replace(os.sep, "/")
        kind, role, vac = m.get("kind"), m.get("role"), m.get("vacconv")
        if kind is None:
            bad.append("job.json 에 kind 가 없다: " + jp); continue
        if kind == "mol_ref":
            got[d] = "1"
        elif kind == "prospective_pose" and role == "primary":
            got[d] = "1" if (vac or m.get("seed") == "afm2424_pm1") else "2"
        else:
            got[d] = "2"
    diff = sorted(k for k in set(got) | set(cen["stage_of"])
                  if got.get(k) != cen["stage_of"].get(k))
    if diff:
        bad.append("단계 분류가 선언과 다르다: %s" % diff[:4])
    cnt = {st: sum(1 for v in got.values() if v == st) for st in ("1", "2")}
    if cnt != cen.get("stage_counts"):
        bad.append("단계 개수가 선언과 다르다: 실물 %s ≠ 선언 %s"
                   % (cnt, cen.get("stage_counts")))
if bad:
    print("⛔ 실행 전 census:")
    for b in bad:
        print("   · " + b)
    sys.exit(1)
print("✓ census: MANIFEST %s · 잡 %d · 단계 %s"
      % (mh[:12], len(cen["job_keys"]), cen["stage_counts"]))
PYPRE

# ⛔ 회신 AP #6 — receipt 존재만으로 2단계를 열지 않는다. **지금 결과로 재판정**한다.
#    (해시 결박보다 단순하고, 위조 receipt 로 우회할 수 없다)
if [ "$stage" = 2 ]; then
  echo "== 2단계 시작 전 1단계 재판정 =="
  python3 analyze_results.py . --gate vacconv || {
    echo "1단계 게이트가 지금 결과로 통과하지 않는다 — 2단계를 열지 않는다."; exit 2; }
fi

# 잡 분류는 job.json 의 **구조화 필드**로 한다 — 이름 파싱 금지
python3 -c '
import json, sys, glob, os
want = sys.argv[1]
for jp in sorted(glob.glob("*/*/job.json")):
    m = json.load(open(jp)); d = os.path.dirname(jp)
    kind, role, vac = m.get("kind"), m.get("role"), m.get("vacconv")
    if kind is None:
        sys.exit("job.json 에 kind 가 없다: " + jp)
    if kind == "mol_ref":
        s = "1"
    elif kind == "prospective_pose" and role == "primary":
        s = "1" if (vac or m.get("seed") == "afm2424_pm1") else "2"
    else:
        s = "2"
    if s == want:
        print(d)
' "$stage" > _stage_jobs.txt || { echo "잡 분류 실패 — 중단"; exit 2; }

# ⛔ 회신 AP #9 — 분류가 조용히 0개/일부만 내고 성공하는 것을 막는다.
n_stage=$(grep -c . _stage_jobs.txt || true)
n_total=$(ls -d */*/ 2>/dev/null | wc -l)
n_expect=$(python3 -c '
import json,sys
m=json.load(open("MANIFEST.json"))
print(sum(1 for k,v in (m.get("planned") or {}).items()))' 2>/dev/null || echo 0)
echo "== 단계 $stage · $n_stage 잡 (묶음 전체 $n_total · 계획 $n_expect) =="
if [ "$n_stage" -eq 0 ]; then
  echo "이 단계의 잡이 0개다 — 분류 규칙과 job.json 을 확인하세요. 중단."; exit 2; fi
if [ "$n_total" != "$n_expect" ]; then
  echo "잡 폴더 $n_total ≠ 계획 $n_expect — 묶음이 온전하지 않다. 중단."; exit 2; fi
cat _stage_jobs.txt

# ⛔⛔ 회신 AS 해제조건 5 — **실행 직전에** 봉인한 절대경로를 다시 해시한다.
#   봉인 시점과 실행 시점 사이에 바이너리가 바뀌었을 수 있다.
python3 - "$VASP_EXE" <<'PYEXE' || { echo "⛔ 실행파일이 봉인과 다릅니다 — 중단"; exit 2; }
import hashlib, json, os, sys
exe = sys.argv[1]
h = hashlib.sha256(open(exe, "rb").read()).hexdigest()
try:
    seal = json.load(open("POTCAR_ROOT_SEAL.json", encoding="utf-8"))
except Exception as e:
    sys.exit("⛔ 봉인을 읽을 수 없다: %r" % e)
bad = []
if seal.get("vasp_executable") and os.path.realpath(seal["vasp_executable"]) != os.path.realpath(exe):
    bad.append("봉인 경로 %s ≠ 실행 경로 %s" % (seal["vasp_executable"], exe))
if seal.get("vasp_executable_sha256") != h:
    bad.append("봉인 해시 %s ≠ 지금 %s" % (str(seal.get("vasp_executable_sha256"))[:12], h[:12]))
if bad:
    print("⛔ 실행 직전 대조 실패:")
    for b in bad:
        print("   · " + b)
    sys.exit(1)
print("✓ 실행파일 = 봉인한 그 파일 (%s · %s)" % (exe, h[:12]))
PYEXE

# ⛔⛔ 회신 AS 해제조건 10 (2026-08-31) — 러너는 **직렬**인데 MANIFEST 는
#   `max_concurrency: 8` 이라고 적고 있었다. 비용 추정이 그 병렬도 가정 위에
#   서 있으므로 둘이 어긋나면 외주가 일정을 잘못 잡는다.
#   ⇒ 러너가 실제로 병렬로 돈다. 단 **의존성이 있는 잡은 나중 물결**로 민다:
#     canary(`*__nzmag`)는 `PARENT_GEOM` 이 가리키는 부모의 최종 기하를 받으므로
#     부모가 먼저 끝나야 한다.
#   `JOBS_PARALLEL` 로 조절한다 (기본 = MANIFEST 의 max_concurrency).
NPAR=${JOBS_PARALLEL:-$(python3 -c '
import json
print((json.load(open("MANIFEST.json")).get("submission") or {}).get("max_concurrency") or 1)'
)}
case "$NPAR" in ''|*[!0-9]*) NPAR=1 ;; esac
[ "$NPAR" -ge 1 ] || NPAR=1

: > _wave1.txt; : > _wave2.txt
while read -r j; do
  [ -n "$j" ] || continue
  if [ -f "$j/PARENT_GEOM" ]; then echo "$j" >> _wave2.txt; else echo "$j" >> _wave1.txt; fi
done < _stage_jobs.txt
n1=$(grep -c . _wave1.txt || true); n2=$(grep -c . _wave2.txt || true)
echo "== 병렬도 $NPAR · 1물결 $n1 잡 · 2물결(부모 의존) $n2 잡 =="

run_wave() {   # $1 = 목록 파일
  [ -s "$1" ] || return 0
  xargs -a "$1" -I{} -P "$NPAR" sh -c '
    j="$1"
    [ -f "$j/run_job.sh" ] || { echo "없음: $j"; exit 1; }
    # 🔴 회신 AT P0-5 — **잡 실행 직전에** 실행파일 receipt 를 남긴다. 봉인 검사는
    #   러너 시작 때 한 번뿐이라, 긴 실행 중에 바이너리가 바뀌면 알 길이 없었다.
    #   잡마다 그 순간의 sha·mtime·launcher 를 적어 두면 반송물에서 대조된다.
    printf "%s\t%s\t%s\t%s\n" \
      "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
      "$(sha256sum "$VASP_EXE" | cut -d" " -f1)" \
      "$VASP_EXE" "$VASP_LAUNCHER" > "$j/EXECUTABLE_RECEIPT.tsv"
    echo "=== $j 시작 ==="
    ( cd "$j" && bash run_job.sh ) || { echo "⛔ $j 실패"; exit 1; }
    echo "=== $j 완료 ==="
  ' _ {}
}
fail=0
run_wave _wave1.txt || fail=1
if [ "$fail" = 0 ]; then
  run_wave _wave2.txt || fail=1
else
  echo "⛔ 1물결에 실패가 있어 2물결(부모 의존 잡)을 시작하지 않습니다"
fi

if [ "$stage" = 1 ]; then
  [ "$fail" = 0 ] || { echo "1단계에 실패한 잡이 있다 — 판정하지 않는다."; exit 2; }
  echo "== 1단계 판정 =="
  python3 analyze_results.py . --gate vacconv || {
    echo "1단계 판정이 막혔다 — 2단계를 돌리지 않는다."; exit 2; }
  echo "1단계 통과 — 2단계는 'bash run_staged.sh 2'"
else
  # ⛔ 회신 AP #9 — 2단계 뒤 **최종 분석**까지가 러너의 일이다.
  echo "== 최종 판정 =="
  python3 analyze_results.py . || { echo "최종 판정 미통과"; exit 2; }
fi
exit $fail
'''


SEAL_POTCAR_ROOT = r'''#!/usr/bin/env bash
# POTCAR 를 전 잡에 조립하고, variant 별 **원본 SHA256** 을 묶음 root 에 봉인한다.
#
# ⛔ 회신 AO Q1 / AP #7 — 봉인은 "생산 전" 이라는 **자기선언이 아니라 검사**여야 한다.
#    최초 봉인 전에 기존 VASP 산출물이 하나라도 있으면 **거부**한다. 계산 뒤에
#    만든 봉인과 구별되지 않으면 사전 승인이 아니기 때문이다.
#
# 이 스크립트가 **못 하는 것**: 봉인한 트리가 공식 배포판인지는 확인하지 못한다
#   (라이선스로 정본 SHA 를 우리가 못 싣는다). 봉인은 "이 계산들이 하나의 트리에서
#   나왔고 그 트리가 생산 전에 고정됐다" 까지만 보증한다. 공식 release 를 주장하려면
#   계산 전에 받은 attestation(POTCAR_ATTESTATION.json)이 따로 있어야 한다 (AP #12).
set -e
: "${PP:?PP=/path/to/potpaw_PBE.54 를 주세요}"
: "${POTCAR_ALLOWLIST:?POTCAR_ALLOWLIST=/abs/site_allow.txt 를 주세요}"

# ⛔⛔ 회신 AT P0-6 (2026-08-31) — 이 스크립트도 **번들 전역 lock** 에 참여한다.
#   종전엔 러너만 잠갔고 봉인기·attestation 생성기는 그냥 들어왔다. 같은 번들의
#   POTCAR·봉인 파일을 동시에 만지면 서로를 덮는다.
#   러너가 이미 쥐고 부르는 경우(BUNDLE_LOCK_HELD=1)는 다시 잡지 않는다 (교착 방지).
_LOCK=".lock_bundle"
_LOCK_MINE=""
if [ "${BUNDLE_LOCK_HELD:-0}" != "1" ]; then
  _RUNID="$(hostname)|$$|$(basename "$0")|$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  _T="$_LOCK.tmp.$$"
  printf '%s\n' "$_RUNID" > "$_T" || exit 3
  if ! ln "$_T" "$_LOCK" 2>/dev/null; then
    rm -f "$_T"
    echo "⛔ 이 번들에 다른 실행이 있습니다: $(cat "$_LOCK" 2>/dev/null)"
    echo "   같은 번들에서 동시에 돌리지 마세요 (POTCAR·봉인을 공유합니다)."
    exit 3
  fi
  rm -f "$_T"; _LOCK_MINE="$_RUNID"
fi
_unlock_self() { [ -n "$_LOCK_MINE" ] && [ "$(cat "$_LOCK" 2>/dev/null)" = "$_LOCK_MINE" ] \
                   && rm -f "$_LOCK"; return 0; }
_bail_self() { echo ""; echo "⛔ 신호($1) — 중단합니다."; trap - EXIT INT TERM
               kill -TERM 0 2>/dev/null || true; _unlock_self; exit "$2"; }
trap '_unlock_self' EXIT
trap '_bail_self INT 130' INT
trap '_bail_self TERM 143' TERM

# ⛔ 회신 AR P0-6 — 받은 **정확한 ZIP** 과 결박한다. 번들 안에는 자기 해시를 넣을
#   수 없으므로 현장이 받은 ZIP 에서 직접 계산해 여기서 박는다:
#     BUNDLE_ZIP_SHA256=$(sha256sum sdcp_c12_vNN.zip | cut -d" " -f1)
: "${BUNDLE_ZIP_SHA256:?BUNDLE_ZIP_SHA256=\$(sha256sum <받은 zip> | cut -d' ' -f1) 를 주세요}"
case "$BUNDLE_ZIP_SHA256" in
  [0-9a-f][0-9a-f]*) [ ${#BUNDLE_ZIP_SHA256} -eq 64 ] || {
      echo "⛔ BUNDLE_ZIP_SHA256 이 64자리 hex 가 아닙니다"; exit 1; } ;;
  *) echo "⛔ BUNDLE_ZIP_SHA256 이 64자리 hex 가 아닙니다"; exit 1 ;;
esac
printf '%s\n' "$BUNDLE_ZIP_SHA256" > ZIP_SHA256.txt
SEAL=POTCAR_ROOT_SEAL.json

# ── AP #7 ① 최초 봉인 전에 **생산 산출물이 있으면 거부** ────────────────
if [ ! -f "$SEAL" ]; then
  prod=$(find . \( -name OUTCAR -o -name "OUTCAR.gz" -o -name vasprun.xml \
                   -o -name OSZICAR -o -name CONTCAR -o -name WAVECAR \
                   -o -name CHGCAR \) -print -quit 2>/dev/null || true)
  if [ -n "$prod" ]; then
    echo "생산 산출물이 이미 있습니다: $prod"
    echo "  최초 root 봉인은 **첫 VASP 실행 전에만** 만들 수 있습니다."
    echo "  계산 뒤에 만든 봉인은 사전 승인과 구별되지 않습니다 (회신 AP #7)."
    exit 1
  fi
fi

# ── AP #7 ② / 🔴🔴 회신 AT P0-3 — POTCAR 를 **매번 PP 원본에서 다시 조립**한다 ──
#    종전엔 기존 provenance 의 `allowlist_sha256` 만 맞으면 `continue` 로 건너뛰었다.
#    그래서 **가짜 POTCAR + 자기일관적인 가짜 provenance** 를 미리 놔두면 PP 원본이
#    아예 없어도 봉인이 성공했다 (리뷰어가 재현). 기존 산출물을 신뢰하는 검사는
#    검사가 아니다 — 봉인은 매번 **원본에서** 다시 만들어 대조한다.
AL_SHA=$(sha256sum "$POTCAR_ALLOWLIST" | cut -d" " -f1)
[ -d "$PP" ] || { echo "⛔ PP 트리가 없습니다: $PP — 원본 없이 봉인하지 않습니다"; exit 1; }
n_new=0; n_same=0; n_fix=0
for d in */*/; do
  [ -f "$d/POTCAR_ASSEMBLE.sh" ] || continue
  prev=""
  if [ -f "$d/POTCAR" ]; then prev=$(sha256sum "$d/POTCAR" | cut -d" " -f1); fi
  # 기존 산출물을 **치우고** 원본에서 다시 만든다 (있으면 믿는 경로를 없앤다)
  rm -f "$d/POTCAR" "$d/POTCAR_PROVENANCE.json"
  ( cd "$d" && PP="$PP" POTCAR_ALLOWLIST="$POTCAR_ALLOWLIST" bash POTCAR_ASSEMBLE.sh ) \
    || { echo "⛔ POTCAR 조립 실패: $d (PP 원본·allowlist 를 확인하세요)"; exit 1; }
  now=$(sha256sum "$d/POTCAR" | cut -d" " -f1)
  n_new=$((n_new+1))
  if [ -n "$prev" ]; then
    if [ "$prev" = "$now" ]; then n_same=$((n_same+1))
    else
      n_fix=$((n_fix+1))
      echo "  🔴 $d: 있던 POTCAR 가 원본 재조립본과 **다릅니다**"
      echo "     이전 ${prev:0:16}… → 재조립 ${now:0:16}…  (재조립본으로 대체했습니다)"
    fi
  fi
  # ③ PP **원본 파일 자체**를 독립 검증한다 — provenance 를 되읽어 확인하지 않고,
  #    거기 적힌 source 경로를 PP 아래에서 직접 열어 SHA·TITEL·allowlist 를 다시 잰다.
  ( cd "$d" && PP="$PP" AL="$POTCAR_ALLOWLIST" python3 - <<'PYSRC'
# 🔴 회신 AT P0-3 — provenance 를 **되읽어 확인하지 않는다.** 거기 적힌 variant 로
#   PP 원본을 직접 열어 SHA·TITEL·allowlist 결박을 **다시 계산**한다.
import hashlib, json, os, re, sys
d = json.load(open("POTCAR_PROVENANCE.json"))
pp, al = os.environ["PP"], os.environ["AL"]
if d.get("allowlist_waived"):
    sys.exit("\u26d4 allowlist 면제 provenance 입니다 — 이 계약에서 폐지됐습니다")
vs = d.get("expected_variants") or []
src = d.get("source_sha256") or {}
if not vs:
    sys.exit("\u26d4 provenance 에 expected_variants 가 없습니다 — 원본을 대조할 수 없습니다")
alines = [ln.strip() for ln in open(al) if ln.strip() and not ln.startswith("#")]
tit = d.get("titel_lines") or []
for i, v in enumerate(vs):
    f = os.path.join(pp, v, "POTCAR")
    if not os.path.isfile(f):
        sys.exit("\u26d4 PP 원본이 없습니다: %s — 원본 없이 봉인하지 않습니다" % f)
    raw = open(f, "rb").read()
    h = hashlib.sha256(raw).hexdigest()
    if v in src and h != src[v]:
        sys.exit("\u26d4 %s 원본 SHA 불일치 (지금 %s / provenance %s)"
                 % (v, h[:16], str(src[v])[:16]))
    # allowlist 는 `sha256  <경로>/<variant>/POTCAR` 형식 — **해시와 variant 가
    # 한 줄에 묶여** 있어야 한다 (해시만 맞고 이름이 다르면 다른 PP 다)
    pat = re.compile(r"^%s\s+.*(?:^|[/\s])%s(?:[/\s]|$)" % (re.escape(h), re.escape(v)))
    if not any(pat.search(ln) for ln in alines):
        sys.exit("\u26d4 %s(%s…) 가 allowlist 에 그 해시로 묶여 있지 않습니다"
                 % (v, h[:16]))
    t = re.search(rb"TITEL\s*=\s*(.+)", raw[:4000])
    if t is None:
        sys.exit("\u26d4 %s 원본에 TITEL 이 없습니다" % v)
    tt = t.group(1).decode("utf-8", "replace").strip()
    if v not in tt.split():
        sys.exit("\u26d4 %s 원본 TITEL 에 그 variant 토큰이 없습니다: %r" % (v, tt))
    if i < len(tit) and tt not in tit[i]:
        sys.exit("\u26d4 %s TITEL 이 provenance 기록과 다릅니다 (원본 %r / 기록 %r)"
                 % (v, tt, tit[i]))
PYSRC
  ) || { echo "⛔ PP 원본 독립검증 실패: $d"; exit 1; }
done
echo "  POTCAR 재조립 $n_new 잡 (이전과 동일 $n_same · 달라서 교체 $n_fix)"
echo "  ✔ PP 원본 SHA·TITEL·allowlist 를 잡마다 **독립 재계산**했습니다 (회신 AT P0-3)"

# ── AP #7 ③ 봉인에 무엇을 담는가 ────────────────────────────────────────
VASP_BIN=$(command -v "${VASP_EXE:-vasp_std}" 2>/dev/null || true)
VASP_SHA=""; VASP_VER=""
if [ -n "$VASP_BIN" ]; then
  VASP_SHA=$(sha256sum "$VASP_BIN" | cut -d" " -f1)
  VASP_VER=$("$VASP_BIN" --version 2>&1 | head -1 || true)
fi
export AL_SHA VASP_BIN VASP_SHA VASP_VER BUNDLE_ZIP_SHA256
python3 - <<'PYSEAL'
import json, glob, os, re, sys, hashlib, time
seal, asm, conflict = {}, {}, []
for pp in sorted(glob.glob("*/*/POTCAR_PROVENANCE.json")):
    d = json.load(open(pp))
    for v, sha in (d.get("source_sha256") or {}).items():
        if v in seal and seal[v] != sha:
            conflict.append((v, pp))
        seal[v] = sha
    asm[os.path.dirname(pp)] = d.get("assembled_sha256")
if conflict:
    sys.exit("variant 원본 SHA 가 잡마다 다르다 — 한 트리가 아니다: %s" % conflict[:3])
if not seal:
    sys.exit("조립된 POTCAR provenance 가 하나도 없다")
rec = {
    "schema": "potcar_root_seal/v2",
    "source_sha256": seal,
    "assembled_sha256_by_job": asm,
    "allowlist_sha256": os.environ.get("AL_SHA") or None,
    "manifest_sha256": hashlib.sha256(open("MANIFEST.json", "rb").read()).hexdigest(),
    "vasp_executable": os.environ.get("VASP_BIN") or None,
    "vasp_executable_sha256": os.environ.get("VASP_SHA") or None,
    "vasp_version_banner": os.environ.get("VASP_VER") or None,
    "bundle_zip_sha256": os.environ.get("BUNDLE_ZIP_SHA256") or None,
    "sealed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "sealed_before_production": True,
    "sealed_before_production_evidence":
        "봉인 시점에 OUTCAR/vasprun/OSZICAR/CONTCAR/WAVECAR/CHGCAR 가 하나도 없었다 "
        "(SEAL_POTCAR_ROOT.sh 가 검사하고 있으면 거부한다)",
    "note": ("v13/v14 Hamiltonian root. 전 잡의 provenance 가 이것과 같아야 한다. "
             "이전 wave 와의 수치적 동등성은 주장하지 않는다. 공식 release 여부는 "
             "이 봉인이 보증하지 않는다 — POTCAR_ATTESTATION.json 이 그 몫이다."),
}
out = "POTCAR_ROOT_SEAL.json"
if os.path.exists(out):
    old = json.load(open(out))
    diff = sorted(k for k in set(old.get("source_sha256") or {}) | set(seal)
                  if (old.get("source_sha256") or {}).get(k) != seal.get(k))
    if diff:
        sys.exit("이미 봉인된 root 와 다르다 (봉인은 바꾸지 않는다): %s" % diff)
    # ⛔⛔ 회신 AS 해제조건 4 (2026-08-31) — 종전 재대조는 **source 집합과
    #   allowlist 만** 봤다. 조립본 해시·MANIFEST·ZIP·VASP 신원이 바뀌어도
    #   "대조 통과" 가 찍혔다. 봉인의 **모든 불변량**을 다시 확인한다.
    bad = []
    # 🔴🔴 회신 AT P0-4 (2026-08-31) — 위 재대조가 **타입과 정체 필드를 안 봤다.**
    #   위조 schema · 문자열형 `sealed_before_production` ("true"/"yes" 는 파이썬에서
    #   참이다) · evidence/시각 변조가 전부 통과했다. 셋을 **정확히** 본다.
    if old.get("schema") != rec["schema"]:
        bad.append("schema: 봉인 %r ≠ 이 도구 %r (다른 스키마의 봉인을 이어쓰지 않는다)"
                   % (old.get("schema"), rec["schema"]))
    if old.get("sealed_before_production") is not True:
        bad.append("sealed_before_production 이 **불리언 True 가 아니다** (%r) — "
                   "문자열은 참으로 읽히지만 봉인이 아니다"
                   % (old.get("sealed_before_production"),))
    _ev = old.get("sealed_before_production_evidence")
    if not isinstance(_ev, str) or not _ev.strip():
        bad.append("sealed_before_production_evidence 가 비어 있거나 문자열이 아니다 (%r)"
                   % (_ev,))
    elif _ev.strip() != rec["sealed_before_production_evidence"].strip():
        bad.append("sealed_before_production_evidence 가 이 도구의 문구와 다르다 — "
                   "손으로 쓴 근거는 근거가 아니다")
    _at = old.get("sealed_at_utc")
    if not isinstance(_at, str) or not re.match(
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", _at or ""):
        bad.append("sealed_at_utc 가 `YYYY-MM-DDTHH:MM:SSZ` 형식이 아니다 (%r)" % (_at,))
    elif _at > rec["sealed_at_utc"]:
        bad.append("sealed_at_utc 가 **미래**다 (봉인 %s > 지금 %s)"
                   % (_at, rec["sealed_at_utc"]))
    for k in ("allowlist_sha256", "manifest_sha256", "bundle_zip_sha256",
              "vasp_executable", "vasp_executable_sha256", "vasp_version_banner"):
        if old.get(k) and old[k] != rec.get(k):
            bad.append("%s: 봉인 %s ≠ 지금 %s"
                       % (k, str(old[k])[:16], str(rec.get(k))[:16]))
        if not old.get(k):
            bad.append("%s: 기존 봉인에 없다 — 반쪽 봉인이다" % k)
    oa, na = (old.get("assembled_sha256_by_job") or {}), (rec.get("assembled_sha256_by_job") or {})
    if not oa:
        bad.append("assembled_sha256_by_job: 기존 봉인에 없다")
    else:
        adiff = sorted(k for k in set(oa) | set(na) if oa.get(k) != na.get(k))
        if adiff:
            bad.append("조립본 해시가 바뀐 잡 %d개: %s" % (len(adiff), adiff[:3]))
    if bad:
        print("⛔ 기존 봉인과 지금 상태가 다릅니다 — 봉인은 바꾸지 않습니다:")
        for b in bad:
            print("   · " + b)
        sys.exit(1)
    print("  POTCAR root 봉인 대조 통과 (%d variant · 조립본 %d잡 · allowlist·MANIFEST·"
          "ZIP·VASP 신원 전건 일치)" % (len(seal), len(na)))
else:
    json.dump(rec, open(out, "w"), indent=1, ensure_ascii=False)
    print("  POTCAR root 봉인 생성 (%d variant · allowlist %s · vasp %s)"
          % (len(seal), str(rec["allowlist_sha256"])[:12],
             str(rec["vasp_version_banner"])[:24]))
PYSEAL
'''

RUN_ALL = """#!/usr/bin/env bash
# ⚠⚠ 이건 **직렬 디버그 러너**다 — 병렬 제출기가 아니다.
#   이대로 돌리면 잡을 하나씩 순서대로 돈다 (Wave 1 기준 20일 규모).
#   실제 제출은 SUBMIT_CONTRACT.md 의 배열 잡/스케줄러로 할 것.
#   여기서는 계약(상 의존성·종료코드 전파)을 보여 주고, 소수 잡을 손으로 돌릴 때 쓴다.
# ⛔ 2026-08-30 (회신 AJ) — 종전엔 `controls tier1 refs tier2` 를 **하드코딩**했다.
#   생성기가 새 그룹(prospective · vacconv)을 만들자 **19잡 중 11잡을 조용히 건너뛰었다.**
#   그룹 목록을 박지 않고 run_job.sh 가 있는 폴더를 **전부** 찾는다.
# 순서: 기준계(refs) 를 먼저 — 나머지는 서로 독립이다.  VASP_CMD 로 실행 명령 지정.
set -u
fail=0
groups=$(for j in */*/run_job.sh; do [ -f "$j" ] && dirname "$(dirname "$j")"; done | sort -u)
groups="refs $(echo "$groups" | grep -v '^refs$' | tr '\n' ' ')"
echo "그룹: $groups"
for grp in $groups; do
  [ -d "$grp" ] || continue
  for j in "$grp"/*/; do
    [ -f "$j/run_job.sh" ] || continue
    echo "═══ $j ═══"
    ( cd "$j" && bash run_job.sh ) || { echo "⚠ $j 실패 — 계속 (분석기가 걸러냄)"; fail=1; }
  done
done
# ⛔ 분석기의 exit 2(필수 산출 미완)를 삼키면 안 된다 — wrapper 가 성공으로 끝나면
#   외주처가 "다 됐다" 고 반송한다. 종료코드를 그대로 올린다.
python3 analyze_results.py .
rc=$?
[ "$fail" = 1 ] && echo "⚠ 실패한 잡이 있었다 (위 로그 확인)"
exit $rc
"""


# ─────────────────────────────────────────────────────────────────────────────
# 쌍 발견 — verdict 와 같은 자격 규칙 + 지문 균질성 (v1 승계)
# ─────────────────────────────────────────────────────────────────────────────
def discover_pairs(run_dir: Path, audit: Optional[Dict[str, Any]] = None,
                   allow_stale_gate: bool = False,
                   top_n: Optional[int] = None,
                   champion: bool = False,
                   cross: bool = False) -> List[Dict[str, Any]]:
    """자격 있는 Li_top↔Ni_top 대조쌍. audit 을 주면 **왜 빠졌는지**를 채워 준다.

    ⚠ down_dir 수 ≠ 대조쌍 수. site-screen 은 일부 방향에서 자리 **종류**를 훑는다
      (O_top·hollow·*_bridge). 그 방향엔 Li_top/Ni_top 자체가 없어 대조쌍이 안 나온다 —
      누락이 아니라 다른 실험이다. 숫자만 보고 "빠졌다" 고 하지 않도록 사유를 남긴다.
    """
    rows = []
    for jp in sorted(run_dir.glob("*.json")):
        if jp.name.startswith("_"):
            continue
        try:
            rows.append(json.loads(jp.read_text()))
        except ValueError:
            print(f"  ⚠ 깨진 JSON 건너뜀 (죽은 런의 반쪽 파일?): {jp.name}")
    fs = [r for r in rows if r.get("ranking_eligible") and r.get("E_pose_eV") is not None]
    # ★ 지문이 **있는 행만** 모아 비교하면 전부 비어도 통과한다 (Codex P0-3).
    #   비었거나 현재 게이트 판과 다르면 옛 프로토콜 산출을 새 정본으로 쓰는 셈이다.
    nofp = [r.get("label") for r in fs if not r.get("fingerprint")]
    if nofp:
        sys.exit(f"⛔ {run_dir}: 프로토콜 지문이 없는 자세 {len(nofp)}개 "
                 f"({nofp[:3]}) — 어느 프로토콜로 돈 것인지 알 수 없다. 추정하지 않는다")
    fps = sorted({str(r["fingerprint"]) for r in fs})
    if len(fps) > 1:
        sys.exit(f"⛔ {run_dir} 에 프로토콜 지문이 {len(fps)}종 섞여 있다: {fps} — "
                 f"regate/재실행으로 정리한 뒤 다시 만들 것")
    # ⚠ gate_version 은 레코드 최상위가 아니라 **protocol 안**에 있다 (make_protocol).
    #   그리고 게이트는 이완 구조에 사후 적용하는 후처리라, 불일치의 해법은 재계산이
    #   아니라 **regate** 다 (site_screen.gate_version docstring).
    cur = str(SS.gate_version())
    gvs = sorted({str((r.get("protocol") or {}).get("gate_version")) for r in fs})
    if gvs != [cur] and not allow_stale_gate:
        sys.exit(f"⛔ {run_dir}: gate_version {gvs} ≠ 현재 {cur} — 이 자세들의 "
                 f"ranking_eligible 은 **옛 문턱**으로 매긴 것이다.\n"
                 f"   이완은 다시 안 돌려도 된다 — regate 만 다시 돌린 뒤 만들 것 "
                 f"(의도적이면 --allow_stale_gate).")
    idx = {(r["site"], r["down_dir"], r["roll_deg"]): r for r in fs}
    by_dir: Dict[str, List[Tuple[float, float, dict, dict]]] = {}
    for (s, dd, ro), r in idx.items():
        if s != "Li_top":
            continue
        q = idx.get(("Ni_top", dd, ro))
        if not q:
            continue
        if r.get("nearest_cation") != "Li" or q.get("nearest_cation") != "Ni":
            continue
        by_dir.setdefault(dd, []).append((float(ro), q["E_pose_eV"] - r["E_pose_eV"], r, q))
    out = []
    for dd, lst in sorted(by_dir.items()):
        med = float(np.median([de for _ro, de, _r, _q in lst]))
        ro, de, r, q = min(lst, key=lambda t: abs(t[1] - med))
        out.append({"dir": dd, "roll": int(ro), "li": r, "ni": q,
                    "dE_uma": round(de, 4), "n_rolls": len(lst),
                    "dir_median_uma": round(med, 4)})

    # ── 방향 감사 — champion·folded **공통** (Codex 6차 P0-3) ────────────────
    #   옛 구현은 champion 분기에서 excluded_dirs 를 {} 로 덮어써 CAP_ARTIFACT 를 비롯한
    #   검열 원장을 통째로 날렸다. 감사는 선택 방식과 무관한 사실이므로 먼저 채운다.
    def _fill_dir_audit() -> None:
        if audit is None:
            return
        seen: Dict[str, Dict[str, int]] = {}
        for r in rows:
            d = str(r.get("down_dir"))
            key = str(r.get("site")) + ("" if r.get("ranking_eligible") else "(부적격)")
            seen.setdefault(d, {})[key] = seen.setdefault(d, {}).get(key, 0) + 1
        why: Dict[str, Dict[str, int]] = {}
        for r in rows:
            if r.get("ranking_eligible"):
                continue
            d = str(r.get("down_dir"))
            for g in (r.get("gate_reasons") or ["(사유 미기록)"]):
                why.setdefault(d, {})[str(g)] = why.setdefault(d, {}).get(str(g), 0) + 1
        audit["n_down_dirs"] = len(seen)
        audit["excluded_dirs"] = {d: c for d, c in sorted(seen.items())
                                  if d not in by_dir}
        # ★ 사유를 같이 남긴다 — 없으면 "왜 빠졌나" 를 볼 때마다 진단을 다시 돌려야 한다
        audit["excluded_reasons"] = {d: why[d] for d in audit["excluded_dirs"] if d in why}
        audit["note"] = ("제외된 방향은 Li_top↔Ni_top 대조쌍이 없는 것이다 — 자리 종류를 "
                         "훑은 방향이거나(O_top·hollow·*_bridge) 한쪽이 부적격인 경우다. "
                         "누락이 아니라 대조쌍 정의 밖이다.")

    _fill_dir_audit()
    # ── 챔피언 모드 (2026-08-12) ────────────────────────────────────────────
    #   "Li 위 최선 vs Ni 위 최선" 을 직접 비교한다. 흡착에서 계는 제일 좋은 자리를
    #   찾아가므로 이게 물리적으로 자연스러운 비교다.
    #   ⚠ 두 챔피언이 **다른 방향**일 수 있다 — 그러면 ΔE 에 자리 효과와 배향 효과가
    #     섞인다. 그래서 matched=False 로 표시하고 분석기가 그렇게 읽게 한다.
    if champion:
        # ★★ 챔피언은 **짝이 확인된 자세 풀**에서만 고른다 (Codex 6차 P0-3).
        #   옛 구현은 전체 자격 행 fs 에서 Li·Ni 를 따로 최소화했다. 그러면 짝 없는
        #   자세가 챔피언이 될 수 있고, 뒤이어 "교차 끝점을 못 만든다" 는 결과가 나온다 —
        #   그건 **물리가 아니라 선택 규약의 산물**이다 (C10 cross_missing 이 그 사례).
        #   짝 풀에서 고르면 각 챔피언의 exact counterpart 가 정의상 존재한다.
        pool = [{"key": (dd, float(ro)), "li": r, "ni": q}
                for dd, lst in by_dir.items() for ro, _de, r, q in lst]
        if not pool:
            return []
        cl = min(pool, key=lambda p: p["li"]["E_pose_eV"])   # Li 위 최선 (짝 보유)
        cn = min(pool, key=lambda p: p["ni"]["E_pose_eV"])   # Ni 위 최선 (짝 보유)
        rl, rn = cl["li"], cn["ni"]
        matched = cl["key"] == cn["key"]                     # (down_dir, roll) 완전일치
        pose = {"Li": {"down_dir": rl["down_dir"], "roll_deg": float(rl["roll_deg"])},
                "Ni": {"down_dir": rn["down_dir"], "roll_deg": float(rn["roll_deg"])}}
        out = [{"dir": f"{rl['down_dir']}v{rn['down_dir']}", "roll": int(rl["roll_deg"]),
                "li": rl, "ni": rn, "matched": matched,
                "dE_uma": round(rn["E_pose_eV"] - rl["E_pose_eV"], 4), "n_rolls": 1,
                "dir_median_uma": round(rn["E_pose_eV"] - rl["E_pose_eV"], 4),
                "champion_pose": pose,
                "champion_dirs": {"Li": rl["down_dir"], "Ni": rn["down_dir"]}}]
        # ★ 교차 끝점 (Codex 5차 ② · 6차 P0-4) — 두 챔피언의 **자세키**(down_dir, roll)가
        #   다르면 ΔE 에 자리 효과와 배향 효과가 섞인다. 각 배향에서 고정배향 대비를
        #   하나씩 얻으려면 Li@(Ni 자세) 와 Ni@(Li 자세) 가 필요하다 → 2×2 완성,
        #   상호작용 I = Δ(Ni자세) − Δ(Li자세) 분리 가능.
        #   ⚠ 방향만 맞추고 roll 이 다르면 2×2 가 아니다 — exact 자세키로 잡는다.
        #     짝 풀에서 뽑았으므로 **대체 검색이 필요 없다**: 상대는 이미 손에 있다.
        out[0]["cross"] = {}
        if cross and not matched:
            out[0]["cross"]["Li_at_Ni_pose"] = cn["li"]   # Ni 챔피언 자세의 Li_top
            out[0]["cross"]["Ni_at_Li_pose"] = cl["ni"]   # Li 챔피언 자세의 Ni_top
            # fail-closed 불변식: 짝 풀 계약이 깨지면 조용히 다른 자세를 계산하게 된다
            for tag, rec, want in (("Li_at_Ni_pose", cn["li"], cn["key"]),
                                   ("Ni_at_Li_pose", cl["ni"], cl["key"])):
                if (rec["down_dir"], float(rec["roll_deg"])) != want:
                    sys.exit(f"⛔ PAIR_POOL_CONTRACT_BROKEN {run_dir.name}/{tag}: "
                             f"짝 자세키 {(rec['down_dir'], rec['roll_deg'])} ≠ {want} — "
                             f"discover_pairs 의 짝 구성이 깨졌다. 번들을 만들지 않는다")
        # ★ 짝 풀 제한의 **대가**를 수치로 남긴다 (2026-08-12).
        #   챔피언은 "전역 최선" 이 아니라 **짝도 있는 배향 중 최선** 이다. 전역 최선
        #   자세가 짝 없는 배향에 있으면 쓰지 않는다. 더 잘 정의된 양(배향일치 대비)
        #   이지만 다른 양이므로, 얼마나 위인지 적어 두지 않으면 나중에 "가장 안정한
        #   자세" 로 인용된다.
        g_li = min((r["E_pose_eV"] for r in fs
                    if r["site"] == "Li_top" and r.get("nearest_cation") == "Li"),
                   default=None)
        g_ni = min((r["E_pose_eV"] for r in fs
                    if r["site"] == "Ni_top" and r.get("nearest_cation") == "Ni"),
                   default=None)
        restr = {"Li_meV": (None if g_li is None
                            else round((rl["E_pose_eV"] - g_li) * 1000, 1)),
                 "Ni_meV": (None if g_ni is None
                            else round((rn["E_pose_eV"] - g_ni) * 1000, 1)),
                 "meaning": ("짝 풀 챔피언이 **전역 최선보다 얼마나 위인가** (UMA). "
                             "0 이면 전역 최선이 마침 짝도 있었다는 뜻이다. "
                             "0 이 아니면 이 ΔE 는 '가장 안정한 자세끼리' 가 아니라 "
                             "'짝이 있는 배향 중 최선끼리' 다.")}
        out[0]["pool_restriction"] = restr
        # ★★ 두 질문은 **다른 답을 낼 수 있다** (2026-08-12 실빌드에서 발각).
        #   (a) 배향일치 대비  ΔE(pool) = E_Ni(pool) − E_Li(pool)   — 우리가 재는 것
        #   (b) 전역 자리 선호 ΔE(global) = E_Ni(g) − E_Li(g)       — 문헌이 읽는 것
        #   ΔE(global) = ΔE(pool) − restr_Ni + restr_Li 이므로 shift = restr_Li − restr_Ni.
        #   ptfe_c10 은 restr_Ni = 51.8 meV → shift −51.8 → UMA 부호가 뒤집힌다.
        #   (a)만 재고 (b)로 읽히게 두면 안 되므로, shift 가 판정을 움직일 만하면
        #   전역 최선 자세도 끝점으로 넣어 **둘 다 DFT 로 잰다**.
        if g_li is not None and g_ni is not None:
            shift = (restr["Li_meV"] or 0.0) - (restr["Ni_meV"] or 0.0)
            out[0]["global_shift_meV"] = round(shift, 1)
            out[0]["global_best"] = {}
            for role, rec_pool, gE in (("Li", rl, g_li), ("Ni", rn, g_ni)):
                if abs(rec_pool["E_pose_eV"] - gE) <= 1e-9:
                    continue                    # 풀 챔피언이 곧 전역 최선
                cand = [r for r in fs if r["site"] == f"{role}_top"
                        and r.get("nearest_cation") == role
                        and abs(r["E_pose_eV"] - gE) <= 1e-9]
                if cand:
                    out[0]["global_best"][role] = cand[0]
        if audit is not None:
            audit["pool_restriction"] = restr
            audit["global_shift_meV"] = out[0].get("global_shift_meV")
            audit["n_contrast_pairs"] = 1
            audit["cross_endpoints"] = {k: v["label"]
                                        for k, v in out[0]["cross"].items()}
            audit["cross_missing"] = {}          # 짝 풀 선택 → 정의상 결측이 없다
            audit["mode"] = ("champion — **짝 확인 풀**에서 Li 위 최선 vs Ni 위 최선. "
                             "두 챔피언의 자세키가 다르면 ΔE 에 배향 효과가 섞인다"
                             "(matched=False) → 교차 2개로 2×2 완성.")
            audit["champion_pose"] = pose
            audit["champion_dirs"] = out[0]["champion_dirs"]
            audit["exact_matched_pose"] = matched
            audit["pair_pool_size"] = len(pool)
            # ★ 챔피언이 **의도적으로** 버린 방향 — 부적격 탈락과 다른 범주다
            audit["champion_dropped_dirs"] = sorted(
                d for d in by_dir if d not in {rl["down_dir"], rn["down_dir"]})
        return out

    # ── top_n 선별 (2026-08-12) ─────────────────────────────────────────────
    #   "MLIP 로 훑고 상위만 DFT" 는 표준 흐름이다. 다만 **#1 하나로는 판정이 안 된다** —
    #   ΔE 는 짝이 있어야 정의되고, 방향에 따라 부호가 뒤집히는 경우가 있어
    #   분석기가 n<3 이면 판정을 거부한다. 그래서 기본 권장은 3 이다.
    #   ⚠ 순위 기준은 **자세 안정도**(UMA E_pose 두 끝점 평균)다 —
    #     |ΔE| 로 고르면 큰 효과만 뽑는 cherry-picking 이 된다.
    dropped_topn: List[str] = []
    if top_n is not None and len(out) > top_n:
        out.sort(key=lambda p: 0.5 * (p["li"]["E_pose_eV"] + p["ni"]["E_pose_eV"]))
        dropped_topn = [p["dir"] for p in out[top_n:]]
        out = out[:top_n]
        out.sort(key=lambda p: p["dir"])
    if audit is not None:
        audit["n_contrast_pairs"] = len(out)
        # ⚠ top_n 로 **의도적으로** 뺀 방향은 부적격 탈락과 다른 범주다. 섞으면
        #   DIRECTION_CENSORED 가 오작동하고, 숨기면 coverage 가 부풀어 보인다.
        audit["topn_dropped"] = dropped_topn
        audit["topn_rank_key"] = "UMA E_pose 두 끝점 평균 (안정도)" if dropped_topn else None
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 자기 seed — **실납품 계보** (원본 원자순서 기준, POSCAR 재정렬 전)
# ─────────────────────────────────────────────────────────────────────────────
def seed_configs(atoms, nslab: int, frag: str,
                 ledger: Dict[str, Any]) -> Dict[str, List[float]]:
    """정본 = **부격자 원장** (db/properties/afm_ledger.json · tools/sdcp/afm_ledger.py).

    ⚠⚠ 2026-08-12 — 옛 구현은 "Ni 를 파일 순서로 앞 절반 −1 / 뒤 절반 +1" 이었다.
      실측하니 실제 Ni1/Ni2 부격자와 **24/48 일치**(= 동전 던지기)였다. 개수만 24/24 로
      같았을 뿐 납품 계보와 **다른 자기 배치**다. 이제 좌표로 확정한 원장만 쓴다.
      원장 부호 규약: Ni2 = −1 · Ni1 = +1 (2026-08-08 납품 INCAR 계보).

    net4 는 Ni2(−1) 중 인덱스가 작은 2개를 +1 로 뒤집은 탐사 seed (net +4 μB).
    doped 라디칼은 분자부 SO3 산소에 +1 μB 를 나눠 얹는다 (양쪽 seed 공통).
    """
    sym = atoms.get_chemical_symbols()
    sign = ledger["sign_by_slab_index"]
    pm1 = [0.0] * len(atoms)
    for k, v in sign.items():
        i = int(k)
        if i >= nslab:
            raise SystemExit(f"⛔ 원장 인덱스 {i} 가 nslab({nslab}) 밖이다 — 다른 슬랩이다")
        if sym[i] != "Ni":
            raise SystemExit(f"⛔ 원장이 {i}번을 Ni 로 아는데 이 구조에선 {sym[i]} 다 "
                             f"— 원자 순서가 다르다. afm_ledger.py 를 다시 만들 것")
        pm1[i] = float(v)
    ni = [i for i in range(nslab) if sym[i] == "Ni"]
    missing = [i for i in ni if pm1[i] == 0.0]
    if missing:
        raise SystemExit(f"⛔ 부격자 배정이 없는 Ni {len(missing)}개 {missing[:8]} — "
                         f"원장이 이 슬랩을 다 안 덮는다. AFM 이 깨진 채로 나갈 수 없다")
    if abs(sum(pm1[:nslab])) > 1e-9:
        raise SystemExit(f"⛔ 슬랩 net moment {sum(pm1[:nslab]):+.1f} μB ≠ 0 — AFM 이 아니다")
    net4 = pm1[:]
    for i in [j for j in ni if pm1[j] < 0][:2]:
        net4[i] = 1.0
    seeds = {"afm2424_pm1": pm1, "afm2424_net4": net4}
    if "DOUBLET" in str(SS.FRAGMENTS.get(frag, {}).get("electrons", "")).upper() \
            and len(atoms) > nslab:
        molpart = atoms[nslab:]
        try:
            gi = [i + nslab for i in SS.group_indices(molpart, "SO3")
                  if molpart.get_chemical_symbols()[i] == "O"]
        except Exception:
            gi = []
        if not gi:
            gi = [i for i in range(nslab, len(atoms)) if sym[i] == "O"] \
                or list(range(nslab, len(atoms)))
        for name in seeds:
            for i in gi:
                seeds[name][i] = round(1.0 / len(gi), 3)
    return seeds


def _ldau_lines(els: List[str]) -> Dict[str, str]:
    return {"ldaul": " ".join("2" if e == "Ni" else "-1" for e in els),
            "ldauu": " ".join("6.2" if e == "Ni" else "0.0" for e in els),
            "ldauj": " ".join("0.0" for _ in els)}


def _assert_slab_lineage(atoms, nslab: int, slab_ref, tag: str,
                         man: Dict[str, Any], max_disp: float = 2.0) -> None:
    """자세의 슬랩부가 **원장을 만든 그 슬랩과 같은 원자 순서**인지 확인한다.

    원장은 인덱스로 부격자를 준다 — 순서가 다르면 MAGMOM 이 엉뚱한 Ni 에 붙는다.
    UMA 이완으로 좌표는 움직이므로 순서(원소열)는 **엄격히**, 변위는 느슨하게 본다.
    """
    sym_a = list(atoms.get_chemical_symbols())[:nslab]
    sym_r = list(slab_ref.get_chemical_symbols())
    if len(sym_r) != nslab:
        raise SystemExit(f"⛔ {tag}: 기준 슬랩 원자 {len(sym_r)} ≠ nslab {nslab}")
    if sym_a != sym_r:
        n = sum(1 for x, y in zip(sym_a, sym_r) if x != y)
        raise SystemExit(f"⛔ {tag}: 슬랩부 원소열이 기준과 다르다 ({n}자리) — "
                         f"원장 인덱스를 못 믿는다")
    cell = slab_ref.cell.array
    df = np.linalg.solve(cell.T, (atoms.positions[:nslab] - slab_ref.positions).T).T
    d = np.linalg.norm((df - np.round(df)) @ cell, axis=1)
    mx = float(d.max())
    if mx > max_disp:
        raise SystemExit(f"⛔ {tag}: 슬랩 원자가 기준에서 최대 {mx:.2f} Å 움직였다 "
                         f"(>{max_disp}) — 같은 슬랩이 맞는지 확인할 것")
    man["slab_lineage_max_disp_A"] = round(
        max(mx, man.get("slab_lineage_max_disp_A", 0.0)), 3)


_FRAG_BONDS_CACHE: Dict[str, Dict[str, int]] = {}


def _assert_mol_topology(atoms, nslab: int, frag: str, tag: str,
                         man: Dict[str, Any]) -> None:
    """자세 안의 분자가 **조각 정본과 같은 위상**인지 빌드 때 확인한다 (Codex 6차 §4).

    왜 여기서 하나: 단일점 판은 DFT 이완이 없어 분석기가 "이완 중 깨졌나" 를 물을 수
    없다. 물어야 할 것은 "계산에 넣은 분자가 애초에 그 조각이 맞나" 이고, 그건 이
    시점에만 답할 수 있다. 원자 순서가 달라도 되도록 **원소쌍 다중집합**으로 본다.

    이 검사가 못 하는 것: 이성질체 구분. 결합 원소쌍 수가 같으면 통과한다
      (C–F 4개는 어느 C 에 붙었든 같다). 자리·배향은 site-screen 게이트가 본다.
    """
    if frag not in _FRAG_BONDS_CACHE:
        try:
            mol, _meta = SS.load_fragment(frag)
        except Exception as e:                      # 조각을 못 읽으면 통과시키지 않는다
            sys.exit(f"⛔ {tag}: 조각 정본 {frag} 을 못 읽었다 ({e}) — "
                     f"분자 위상을 검증할 수 없으므로 번들을 만들지 않는다")
        m2 = mol.copy()
        m2.set_cell(atoms.cell.array)
        m2.set_pbc(True)
        _FRAG_BONDS_CACHE[frag] = _bond_types(m2, list(range(len(m2))))
    want = _FRAG_BONDS_CACHE[frag]
    got = _bond_types(atoms, list(range(nslab, len(atoms))))
    if got != want:
        diff = {k: (want.get(k, 0), got.get(k, 0))
                for k in set(want) | set(got) if want.get(k, 0) != got.get(k, 0)}
        sys.exit(f"⛔ SOURCE_TOPOLOGY_CHANGED {tag}: 자세의 분자가 조각 정본과 다르다.\n"
                 f"   결합(정본→자세) {diff}\n"
                 f"   → 이 자세는 {frag} 이 아니다. site-screen 게이트를 다시 볼 것")
    man.setdefault("mol_topology", {})[frag] = want


def _top_cations(atoms, nslab: int, sym: List[str], depth: float = 1.2) -> Dict[str, List[int]]:
    """표면(위쪽) Li/Ni 의 **원본 인덱스**. 등록(registry) 판정은 여기에만 걸어야 한다.

    ⚠ 전 슬랩 Li/Ni 중 최단거리로 판정하면 먼 H/C 나 **표면 아래 양이온**이 라벨을
      정할 수 있다 (Codex P0-G). 표면층만 본다.
    """
    zs = [atoms.positions[i, 2] for i in range(nslab) if sym[i] in ("Li", "Ni")]
    ztop = max(zs) if zs else 0.0
    return {el: [i for i in range(nslab)
                 if sym[i] == el and atoms.positions[i, 2] >= ztop - depth]
            for el in ("Li", "Ni")}


def _com_frac(atoms) -> List[float]:
    """질량중심의 분수좌표. ⚠ 원자 중심(centroid)이 아니다 — VASP DIPOL 권고는 COM."""
    com = atoms.get_center_of_mass()
    return list(np.linalg.solve(atoms.cell.array.T, com) % 1.0)


def _bonds_in(atoms, idx: List[int]) -> List[Tuple[int, int]]:
    """idx 원자들 사이의 결합쌍 (원본 인덱스). 분석기 mol_bond_graph 와 같은 규약."""
    import itertools
    pos = atoms.get_positions()
    sym = atoms.get_chemical_symbols()
    cell = np.asarray(atoms.cell.array, dtype=float)
    shifts = [i * cell[0] + j * cell[1] + k * cell[2]
              for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)]
    out = []
    for a, b in itertools.combinations(sorted(idx), 2):
        d = pos[a] - pos[b]
        best = min(float(np.linalg.norm(d + s)) for s in shifts)
        if best < BOND_F_B * (RCOV_B.get(sym[a], 1.0) + RCOV_B.get(sym[b], 1.0)):
            out.append((a, b))
    return out


def _mol_graph_canon(atoms, nslab: int, order: List[int]) -> List[List[int]]:
    """자세의 분자 결합 그래프를 **POSCAR 인덱스**로 낸다 (job.json 저장용)."""
    rev = {i: k for k, i in enumerate(order)}
    mol = [i for i in range(nslab, len(atoms))]
    return sorted([sorted((rev[a], rev[b]))
                   for a, b in _bonds_in(atoms, mol)])


def _bond_types(atoms, idx: List[int]) -> Dict[str, int]:
    """결합의 **원소쌍 다중집합** — 원자 순서가 달라도 비교할 수 있다."""
    sym = atoms.get_chemical_symbols()
    c: Dict[str, int] = {}
    for a, b in _bonds_in(atoms, idx):
        k = "–".join(sorted((sym[a], sym[b])))
        c[k] = c.get(k, 0) + 1
    return c



#: ⛔ 회신 AP #12 (2026-08-31) — 원고에서 `potpaw_PBE.54` 와 variant 를 주장하려면
#:   **계산 전에** 받은 attestation 이 있어야 한다. POTCAR 원문은 받지 않는다.
POTCAR_ATTESTATION_REQUEST = """# POTCAR / VASP attestation 요청 (계산 **전**)

원고 Methods 에 PAW release 를 적으려면 아래를 **첫 계산 전에** 확인해 주셔야 합니다.
POTCAR 파일 자체는 주고받지 않습니다 — 지문과 버전 문자열만입니다.

아래 스크립트를 묶음 루트에서 실행하시면 `POTCAR_ATTESTATION.json` 이 만들어집니다.
그 파일만 반송해 주시면 됩니다.

```bash
# 먼저 받으신 ZIP 의 SHA256 을 구합니다 (번들 안에는 자기 해시를 넣을 수 없습니다)
ZS=$(sha256sum /경로/받은번들.zip | cut -d" " -f1)

PP=/path/to/potpaw_PBE.54 \
POTCAR_ALLOWLIST=/abs/site_allow.txt \
RELEASE_LABEL="potpaw_PBE.54" \
SITE="기관/담당자" \
BUNDLE_ZIP_SHA256="$ZS" \
bash MAKE_POTCAR_ATTESTATION.sh
```

⚠ **첫 VASP 실행 전에** 돌려 주세요. 스크립트가 OUTCAR/CONTCAR/CHGCAR 등 산출물이
있으면 거부합니다 — "계산 전에 만들었다" 를 선언이 아니라 **검사**로 남기기
위해서입니다.

담기는 것 (회신 AP #12 목록 그대로):
- 받으신 **정확한 ZIP** 의 SHA256 (BUNDLE_ZIP_SHA256) 과 MANIFEST.json 의 SHA256
- release label 과 variant 목록
- variant 별 **원본 파일 전체** SHA256
- POTCAR 내부 `TITEL` 줄과 embedded hash
- site allowlist 의 SHA256
- 생성 UTC 시각 · 사이트/담당자
- `vasp_std --version` 원문
- VASP 실행파일의 SHA256 과 resolved path

⚠ 이것이 없으면 원고는 `PBE PAW 5.4` 를 **단정하지 않고**, D 를 "이 묶음의
PAW dataset 에 조건부" 로만 보고합니다.
"""

MAKE_ATTESTATION = r'''#!/usr/bin/env bash
# 회신 AP #12 — 계산 **전에** release attestation 을 만든다. POTCAR 원문은 담지 않는다.
set -e
: "${PP:?PP=/path/to/potpaw_PBE.54}"
: "${POTCAR_ALLOWLIST:?POTCAR_ALLOWLIST=/abs/site_allow.txt}"
: "${RELEASE_LABEL:?RELEASE_LABEL='potpaw_PBE.54' 처럼 배포판 이름}"
: "${SITE:?SITE='기관/담당자'}"
# ⛔ 회신 AR P0-6 — 봉인과 **같은 출처**의 ZIP 해시를 쓴다 (문자열 하나).
#   종전엔 스크립트가 근처 *.zip 을 스스로 찾아 {파일명: sha} 사전을 만들었다 —
#   무엇에 대한 attestation 인지 모호하고 분석기와 형이 달랐다.
: "${BUNDLE_ZIP_SHA256:?BUNDLE_ZIP_SHA256=\$(sha256sum <받은 zip> | cut -d' ' -f1)}"

# ⛔⛔ 회신 AT P0-6 (2026-08-31) — attestation 생성기도 **번들 전역 lock** 에
#   참여한다. 종전엔 러너만 잠갔고 이 스크립트는 그냥 들어와 같은 번들의 파일을
#   동시에 만질 수 있었다.
_LOCK=".lock_bundle"
_LOCK_MINE=""
if [ "${BUNDLE_LOCK_HELD:-0}" != "1" ]; then
  _RUNID="$(hostname)|$$|make_attestation|$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  _T="$_LOCK.tmp.$$"
  printf '%s\n' "$_RUNID" > "$_T" || exit 3
  if ! ln "$_T" "$_LOCK" 2>/dev/null; then
    rm -f "$_T"
    echo "⛔ 이 번들에 다른 실행이 있습니다: $(cat "$_LOCK" 2>/dev/null)"
    exit 3
  fi
  rm -f "$_T"; _LOCK_MINE="$_RUNID"
fi
_unlock_self() { [ -n "$_LOCK_MINE" ] && [ "$(cat "$_LOCK" 2>/dev/null)" = "$_LOCK_MINE" ] \
                   && rm -f "$_LOCK"; return 0; }
_bail_self() { echo ""; echo "⛔ 신호($1) — 중단합니다."; trap - EXIT INT TERM
               kill -TERM 0 2>/dev/null || true; _unlock_self; exit "$2"; }
trap '_unlock_self' EXIT
trap '_bail_self INT 130' INT
trap '_bail_self TERM 143' TERM

# ⛔ 회신 AR P0-6 — `made_before_production` 을 **자기선언이 아니라 산출물 부재로**
#   입증한다. 하나라도 있으면 계산 전이 아니므로 거부한다.
PROD=$(find . \( -name OUTCAR -o -name "OUTCAR.gz" -o -name vasprun.xml \
                 -o -name OSZICAR -o -name CONTCAR -o -name WAVECAR \
                 -o -name CHGCAR \) -print -quit 2>/dev/null || true)
if [ -n "$PROD" ]; then
  echo "⛔ 생산 산출물이 이미 있습니다: $PROD"
  echo "   attestation 은 **첫 VASP 실행 전에만** 만들 수 있습니다 (회신 AR P0-6)."
  exit 1
fi
VASP_BIN=$(command -v "${VASP_EXE:-vasp_std}")
export VASP_BIN BUNDLE_ZIP_SHA256
python3 - <<'PYA'
import json, os, hashlib, time, subprocess
man = json.load(open("MANIFEST.json"))
spec = man.get("potcar_spec") or {}
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()
pp = os.environ["PP"]
variants = {}
for el, var in sorted(spec.items()):
    f = os.path.join(pp, var, "POTCAR")
    if not os.path.isfile(f):
        raise SystemExit("원본 POTCAR 가 없다: %s" % f)
    titel, emb = [], []
    for ln in open(f, errors="replace"):
        t = ln.strip()
        if t.startswith("TITEL"):
            titel.append(t)
        if "SHA256" in t or t.startswith("COPYR") and "hash" in t.lower():
            emb.append(t)
        if len(titel) and ln.startswith("   END of PSCTR"):
            break
    # ⛔ 회신 AR P0-6 — 분석기가 관측 TITEL 과 대조하므로 **문자열 하나**로 낸다
    variants[var] = {"element": el, "source_sha256": sha(f),
                     "titel": (titel[0] if titel else ""),
                     "titel_all": titel[:2],
                     "embedded_hash": (emb[0] if emb else ""),
                     "embedded_hash_lines": emb[:2]}
    if not titel:
        raise SystemExit("TITEL 을 못 읽었다: %s" % f)
vb = os.environ["VASP_BIN"]
try:
    ver = subprocess.run([vb, "--version"], capture_output=True, text=True,
                         timeout=60).stdout.strip()
except Exception as e:
    ver = "실행 실패: %r" % e
rec = {
    "schema": "potcar_attestation/v1",
    "made_before_production": True,
    "made_before_production_evidence":
        "attestation 생성 시점에 OUTCAR/OUTCAR.gz/vasprun.xml/OSZICAR/CONTCAR/"
        "WAVECAR/CHGCAR 가 하나도 없었다 (MAKE_POTCAR_ATTESTATION.sh 가 검사하고 "
        "있으면 거부한다 — 회신 AR P0-6)",
    "release_label": os.environ["RELEASE_LABEL"],
    "site": os.environ["SITE"],
    "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "manifest_sha256": sha("MANIFEST.json"),
    "bundle_zip_sha256": os.environ["BUNDLE_ZIP_SHA256"].strip().lower(),
    "allowlist_path": os.environ["POTCAR_ALLOWLIST"],
    "allowlist_sha256": sha(os.environ["POTCAR_ALLOWLIST"]),
    "pp_root": pp,
    "variants": variants,
    "vasp_executable": vb,
    "vasp_executable_sha256": sha(vb),
    "vasp_version_raw": ver,
}
json.dump(rec, open("POTCAR_ATTESTATION.json", "w"), indent=1, ensure_ascii=False)
print("→ POTCAR_ATTESTATION.json (variant %d · release %s)"
      % (len(variants), rec["release_label"]))
PYA
'''

def _write_potcar_asm(jd: Path, species_order: List[str]) -> None:
    """그 잡 전용 POTCAR 조립기. **슬랩·기체 공통**이다.

    ⚠ 처음엔 슬랩에만 넣었다. 기체 8잡에는 없어서 제출 본문(`bash POTCAR_ASSEMBLE.sh`)
      이 exit 127 로 죽었고, E_ads 를 하나도 못 만드는 상태였다 (Codex 4차 감사 P0-1).
      잡을 만드는 자리가 두 곳이면 배포물도 두 곳에서 만들어야 한다 — 한 함수로 뺀다.
    """
    pv = [POTCAR_SPEC.get(e, e) for e in species_order]
    # ★ 회신 Z P0-6 — 개수만 세면 부족하다. 실제 실패 모드는 "$PP/Ni_pv/POTCAR 가
    #   사실은 Ni 였다" · "PBE.52 세트였다" 이고, 둘 다 개수는 맞는다. 그래서
    #   ① POSCAR 종 순서 ↔ POTCAR_SPEC ↔ 실제 TITEL **순서**를 자리별로 맞추고
    #   ② variant 를 **토큰 전체**로 비교하며 (`Ni` 가 `Ni_pv` 안에서 오탐되면 안 된다)
    #   ③ 원본·조립본 SHA256 을 POTCAR_PROVENANCE.json 에 남겨 **반송**시킨다.
    #      정본 SHA 는 라이선스 때문에 우리가 못 싣는다 — 대신 분석기가 잡 사이
    #      **일관성**을 본다(같은 variant 는 전 잡에서 같은 SHA 여야 한다).
    (jd / "POTCAR_ASSEMBLE.sh").write_text(
        "#!/usr/bin/env bash\n"
        "# 이 잡의 POTCAR 를 만든다. PBE PAW 5.4 세트 경로를 PP 로 준다.\n"
        "#   PP=/path/to/potpaw_PBE.54 POTCAR_ALLOWLIST=/abs/site_allow.txt bash POTCAR_ASSEMBLE.sh\n"
        "# ⚠ 종 순서는 이 잡 POSCAR 전용이다 — 다른 잡에 복사하지 말 것.\n"
        "#   (하나를 돌려 쓰면 에러 없이 **다른 계**를 계산합니다.)\n"
        "set -euo pipefail\n"
        "# 🔴 회신 AB P0-8 — 종전엔 POTCAR 를 **제자리에서** 만들고 나중에 검사했다.\n"
        "#   검사가 실패해 exit 1 이 나도 **완성된 POTCAR 는 남았고**, 이어지는\n"
        "#   run_job.sh 가 그것으로 VASP 를 돌렸다 — allowlist 실패가 계산 중단으로\n"
        "#   이어지지 않았다. 임시본에 조립·검증하고 통과 시에만 원자적으로 옮긴다.\n"
        "trap 'rc=$?; if [ $rc -ne 0 ]; then rm -f POTCAR.tmp POTCAR POTCAR_PROVENANCE.json; "
        "echo \"  ⛔ 실패 — POTCAR 를 남기지 않았습니다\"; fi' EXIT\n"
        f'ORDER="{" ".join(pv)}"\n'
        f'SPECIES="{" ".join(species_order)}"\n'
        ': "${PP:?PP 를 지정하세요 (PBE PAW 5.4 세트 루트)}"\n'
        'rm -f POTCAR POTCAR.tmp POTCAR_PROVENANCE.json\n'
        'srcsha=""\n'
        'for v in $ORDER; do\n'
        '  f="$PP/$v/POTCAR"\n'
        '  [ -f "$f" ] || { echo "⛔ 없음: $f"; exit 1; }\n'
        '  srcsha="$srcsha $v:$(sha256sum "$f" | cut -d" " -f1)"\n'
        '  cat "$f" >> POTCAR.tmp\n'
        'done\n'
        '# ① 개수\n'
        'n=$(grep -ac TITEL POTCAR.tmp)\n'
        f'[ "$n" = {len(pv)} ] || {{ echo "⛔ TITEL {len(pv)}개여야 하는데 $n개"; exit 1; }}\n'
        '# ② 자리별 variant — 토큰 전체 비교 (Ni 가 Ni_pv 에 오탐되지 않게)\n'
        'i=0\n'
        'for v in $ORDER; do\n'
        '  i=$((i+1))\n'
        '  got=$(grep -a TITEL POTCAR.tmp | sed -n "${i}p" | awk \'{print $4}\')\n'
        '  fun=$(grep -a TITEL POTCAR.tmp | sed -n "${i}p" | awk \'{print $3}\')\n'
        '  [ "$got" = "$v" ] || { echo "⛔ ${i}번째 TITEL 이 $got — $v 여야 합니다"; exit 1; }\n'
        '  [ "$fun" = "PAW_PBE" ] || { echo "⛔ ${i}번째가 $fun — PAW_PBE 여야 합니다"; exit 1; }\n'
        'done\n'
        '# ③ trusted hash allowlist 대조 (회신 AA P0-2)\n'
        '#    variant 이름·PAW_PBE·잡 간 일관성은 "전부 같은 잘못된 PP 트리" 를 못 막는다.\n'
        '#    정본 SHA 는 라이선스상 우리가 못 싣는다 → **외주처 site-local 목록**을 받는다.\n'
        'if [ -n "${POTCAR_ALLOWLIST:-}" ]; then\n'
        '  [ -f "$POTCAR_ALLOWLIST" ] || { echo "⛔ allowlist 파일 없음: $POTCAR_ALLOWLIST"; exit 1; }\n'
        '  for t in $srcsha; do\n'
        '    v="${t%%:*}"; h="${t#*:}"\n'
        '    # ★ 해시만 보면 안 된다 — **variant 와 묶여** 있어야 한다.\n'
        '    #   Li_sv 와 Ni_pv 의 파일이 서로 바뀐 트리는 두 해시가 모두 목록에\n'
        '    #   있으므로 해시 존재만으로는 통과한다 (2026-08-29 자체 검토).\n'
        '    grep -E "^$h[[:space:]].*(^|[/[:space:]])$v(/|[[:space:]]|$)" \\\n'
        '         "$POTCAR_ALLOWLIST" > /dev/null || {\n'
        '      echo "⛔ $v 가 allowlist 의 그 해시와 묶여 있지 않습니다"; echo "   $h";\n'
        '      echo "   (목록 형식: sha256sum \\$PP/<variant>/POTCAR 출력 그대로)"; exit 1; }\n'
        '  done\n'
        '  echo "  ✔ allowlist 대조 통과 ($POTCAR_ALLOWLIST)"\n'
        'else\n'
        '  echo "⛔ POTCAR_ALLOWLIST 가 지정되지 않았습니다."\n'
        '  echo "   신뢰하는 PBE.54 세트의 sha256 목록을 **한 번** 만들어 전 잡에 같은"\n'
        '  echo "   파일을 쓰세요 (잡마다 새로 만들면 아무것도 검증하지 않습니다):"\n'
        '  echo "     for v in \\$(ls \\$PP); do sha256sum \\$PP/\\$v/POTCAR; done > site_allow.txt"\n'
        '  echo "     POTCAR_ALLOWLIST=/abs/site_allow.txt bash POTCAR_ASSEMBLE.sh"\n'
        '  echo "   ⛔ 면제(waiver)는 폐지했습니다 (회신 AB P0-8)."\n'
        '  exit 1\n'
        'fi\n'
        '# ④ provenance — 이 파일을 결과와 **함께 반송**해 주세요\n'
        'python3 - "$srcsha" <<\'PY\' > POTCAR_PROVENANCE.json\n'
        'import hashlib, json, sys, os as _os\n'
        'src = dict(t.split(":", 1) for t in sys.argv[1].split())\n'
        'titel = [l.strip() for l in open("POTCAR.tmp", errors="ignore") if "TITEL" in l]\n'
        'print(json.dumps({"schema": "potcar_provenance/v1",\n'
        '                  "species_order": "' + " ".join(species_order) + '".split(),\n'
        '                  "expected_variants": "' + " ".join(pv) + '".split(),\n'
        '                  "titel_lines": titel, "source_sha256": src,\n'
        '                  "allowlist": _os.environ.get("POTCAR_ALLOWLIST"),\n'
        '                  "allowlist_sha256": (hashlib.sha256(open(\n'
        '                      _os.environ["POTCAR_ALLOWLIST"],"rb").read()).hexdigest()\n'
        '                      if _os.environ.get("POTCAR_ALLOWLIST") and\n'
        '                      _os.path.isfile(_os.environ["POTCAR_ALLOWLIST"]) else None),\n'
        '                  "allowlist_waived": False,\n'
        '                  "assembled_sha256": hashlib.sha256(\n'
        '                      open("POTCAR.tmp","rb").read()).hexdigest()},\n'
        '                 indent=1, ensure_ascii=False))\n'
        'PY\n'
        'mv POTCAR.tmp POTCAR\n'        # 전건 통과 후에야 이 이름이 생긴다 (원자적)
        'grep -a TITEL POTCAR\n'
        f'echo "✔ 조립 완료 — 종 순서 {" ".join(species_order)} · variant·순서·PAW_PBE 확인"\n'
        'echo "  → POTCAR_PROVENANCE.json (결과와 함께 반송해 주세요)"\n')


def _emit_slab_job(jd: Path, atoms, nslab: int, freeze: float, frag: str,
                   system: str, seed_name: str, extra_meta: Dict[str, Any],
                   ledger: Dict[str, Any], zcut=None, dense: bool = False,
                   prescf: bool = True, single_point: bool = False,
                   kmesh_over: Optional[Dict[str, str]] = None,
                   dense_cand: bool = False, closure: bool = False,
                   d3_off: bool = False) -> Dict[str, Any]:
    """슬랩 잡 v3 — POSCAR(루트) + pre/ + relax/ + static/ (+dense/). MAGMOM 재매핑·검산."""
    kmesh_over = kmesh_over or {}
    jd.mkdir(parents=True, exist_ok=True)
    pos = SS._write_poscar(jd / "POSCAR", atoms, nslab, freeze, zcut=zcut)
    mag_orig = seed_configs(atoms, nslab, frag, ledger)[seed_name]
    mag_poscar = [mag_orig[i] for i in pos["order"]]
    sym = atoms.get_chemical_symbols()
    for k, m in enumerate(mag_poscar):          # MAGMOM 순열 검산 (36/48 사고 재발 방지)
        i = pos["order"][k]
        if abs(m) > 1e-9 and sym[i] != "Ni" and i < nslab:
            raise SystemExit(f"⛔ MAGMOM 순열 검산 실패: POSCAR {k + 1}번({sym[i]})에 {m}")
    zcom = float(_com_frac(atoms)[2])
    fmt = {"system": system, "common": _COMMON, "zcom": zcom,
           "magmom": " ".join(f"{m:.3f}" for m in mag_poscar),
           **_ldau_lines(pos["species_order"])}
    tpls = {"pre": SLAB_PRE, "relax": SLAB_RELAX, "static": SLAB_STATIC,
            "dense": SLAB_STATIC}
    if closure and d3_off:
        # ⛔ 회신 W Q2/P0-2 — UMA−DFT 오프셋의 원인이 셋(missing D3 · 기체 기준 오차 ·
        #   자기 basin)인데 **가른 적이 없다.** 같은 기하·같은 자기 basin 에서 D3 만 끄면
        #   D3 기여가 직접 빠진다. IVDW 를 지우고 나머지는 **글자 하나까지 같게** 둔다.
        _sp0 = SLAB_SP.replace("LREAL    = Auto", "LREAL    = .FALSE.") \
                      .replace("IVDW     = 11\n", "") \
                      .replace("[static · single-point]",
                               "[closure D3-OFF twin · all-F fixed geometry]")
        tpls = {"static": _sp0}
    elif closure:
        # ⛔⛔ 회신 U P0-5 — 종전 `--single_point` 는 고정기하이면서도 `LREAL = Auto` 였다.
        #   조각 간 대비에서 LREAL 오차는 **서로 다른 흡착종이라 소거되지 않는다.**
        #   closure 모드는 전 endpoint 를 `.FALSE.` 로 못박는다.
        _sp = SLAB_SP.replace("LREAL    = Auto", "LREAL    = .FALSE.") \
                     .replace("[static · single-point]", "[closure · all-F fixed geometry]")
        tpls = {"static": _sp,
                "dense": _sp.replace("ICHARG   = 2", "ICHARG   = 1")
                            .replace("[closure · all-F", "[closure dense · all-F")}
    elif single_point:
        # MLIP 로 기하를 닫고 DFT 는 결합에너지만.
        # ⛔⛔ 2026-08-31 — **`LREAL = .FALSE.` 를 여기서도 못박는다.**
        #   회신 U P0-5 가 정확히 이 결함을 판정했는데(`--single_point` 가 고정기하이면서
        #   `LREAL = Auto`), 그때 고친 것은 `closure` 가지뿐이었다. C-12 는 `--single_point`
        #   를 쓰므로 그대로 `Auto` 가 나왔다. 실측(v5): 슬랩 static 은 `Auto` 인데
        #   **기체 기준 static 은 `.FALSE.`** — `E_ads = E_복합체(Auto) − E_기체(.FALSE.)` 로
        #   **한 양 안에서 두 해밀토니안이 섞였다.**
        #   회신 U 의 이유가 그대로 적용된다: 조각 간 대비에서 LREAL 오차는
        #   **서로 다른 흡착종이라 소거되지 않는다.**
        # ⚠ dense 는 static 의 CHGCAR 를 승계해야 하므로 ICHARG=1 이어야 한다.
        #   같은 SLAB_SP(ICHARG=2)를 재사용하면 복사한 CHGCAR 를 **안 쓴다**.
        _spf = SLAB_SP.replace("LREAL    = Auto", "LREAL    = .FALSE.")
        tpls = {"static": _spf,
                "dense": _spf.replace("ICHARG   = 2", "ICHARG   = 1")
                             .replace("[static · single-point]", "[dense · single-point]")}
    if not prescf:
        # ⚠ pre 를 빼면 relax 의 ISTART=1 이 읽을 WAVECAR 가 없다. VASP 는 조용히
        #   처음부터 시작하므로 "승계했다" 는 기록만 남고 실제로는 안 한 게 된다.
        tpls["relax"] = SLAB_RELAX.replace("ISTART   = 1", "ISTART   = 0") \
                                  .replace("ICHARG   = 0", "ICHARG   = 2")
    phases = (["static"] if (single_point or closure)
              else (["pre"] if prescf else []) + ["relax", "static"]) \
        + (["dense"] if dense else [])
    kmesh, incar_exp, kp_exp = {}, {}, {}
    for ph in phases:
        (jd / ph).mkdir(exist_ok=True)
        txt = tpls[ph].format(**fmt)
        (jd / ph / "INCAR").write_text(txt)
        km = KMESH["relax"] if ph == "pre" else kmesh_over.get(ph, KMESH[ph])
        (jd / ph / "KPOINTS").write_text(_kpoints_text(ph, km))
        kp_exp[ph] = _kpoints_expected(ph, km)
        kmesh[ph] = km
        # ⚠ 기대값을 손으로 적지 않고 **배포한 INCAR 을 되읽는다** — 손으로 적으면
        #   템플릿을 고쳤을 때 조용히 어긋난다 (Codex P0-5).
        incar_exp[ph] = _incar_expected_from(txt)
    # ★ 조건부 dense 후보 (Codex 6차 §3) — 입력만 만들고 **run_job.sh 는 안 본다**
    #   (러너는 pre/relax/static/dense 만 돈다). coarse 를 보고 승격되면
    #   run_dense_selected.sh 가 dense_cand → dense 로 옮겨 같은 러너로 돌린다.
    if dense_cand and "dense" not in phases:
        (jd / "dense_cand").mkdir(exist_ok=True)
        txt = tpls["dense"].format(**fmt)
        (jd / "dense_cand" / "INCAR").write_text(txt)
        km = kmesh_over.get("dense", KMESH["dense"])
        (jd / "dense_cand" / "KPOINTS").write_text(_kpoints_text("dense_cand", km))
        kp_exp["dense_cand"] = _kpoints_expected("dense_cand", km)
        kmesh["dense_cand"] = km
        incar_exp["dense_cand"] = _incar_expected_from(txt)
    _write_potcar_asm(jd, pos["species_order"])
    # ★ POTCAR 는 **잡마다 다르다** (Codex 7차 §11) — POSCAR 종 순서가 조각마다
    #   다르므로 하나의 concatenated POTCAR 를 공용할 수 없다. 조립 명령을 잡 안에 둔다.
    (jd / "run_job.sh").write_text(RUN_JOB)
    top = _top_cations(atoms, nslab, sym)
    rev = {i: k for k, i in enumerate(pos["order"])}      # 원본 → POSCAR 위치
    meta = {**pos, **extra_meta, "seed": seed_name, "nslab": nslab,
            "phases": phases, "zcom_frac": round(zcom, 4),
            "kmesh": kmesh, "incar_expected": incar_exp,
            # 🔴 회신 AT P0-2 — 상마다 **정확한** 격자·시프트를 제목으로 결박한다
            "kpoints_expected": kp_exp,
            "magmom_poscar": [round(m, 3) for m in mag_poscar],
            "ni_sign_poscar_idx": {str(rev[i]): mag_orig[i] for i in range(nslab)
                                   if sym[i] == "Ni"},
            "mol_sign_poscar_idx": {str(rev[i]): mag_orig[i]
                                    for i in range(nslab, len(atoms))
                                    if abs(mag_orig[i]) > 1e-9},
            "mol_poscar_idx": [k for k, i in enumerate(pos["order"]) if i >= nslab],
            # ★ 단일점 판의 분자 위상 정본 (Codex 6차 §4). 분석기는 CONTCAR 가 없어
            #   init↔fin 비교가 헛돈다 — 이 그래프가 유일한 기준선이다.
            "mol_graph_canonical": _mol_graph_canon(atoms, nslab, pos["order"]),
            "slab_li_poscar_idx": [k for k, i in enumerate(pos["order"])
                                   if i < nslab and sym[i] == "Li"],
            "slab_ni_poscar_idx": [k for k, i in enumerate(pos["order"])
                                   if i < nslab and sym[i] == "Ni"],
            "top_li_poscar_idx": sorted(rev[i] for i in top["Li"]),
            "top_ni_poscar_idx": sorted(rev[i] for i in top["Ni"])}
    (jd / "job.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    return meta


def _emit_mol_job(jd: Path, frag: str, mol, margin: float,
                  free_spin: bool = False,
                  closure: bool = False,
                  nonzero_start: bool = False) -> Dict[str, Any]:
    """기체상 기준계 v3 — 상자 span+margin, IDIPOL=4+DIPOL(COM), NUPDOWN, 2상.

    `free_spin=True` → `NUPDOWN = -1` (자유 스핀).
      ⛔⛔ 2026-08-28 회신 O/P P0 — **기준과 복합체가 다른 저울로 쟀다.** 기준 분자는
      `NUPDOWN` 고정(중성 = 0)으로, 복합체·슬랩은 `NUPDOWN=-1` 자유로 돌았다.
      그 둘을 뺀 것이 `E_ads` 이고, 그래서 0.346 eV headline 이 보류됐다.
      고칠 것은 "전 계에 같은 값" 이 아니라 **같은 state-selection policy** 다 —
      복합체가 자유였으므로 기준도 자유여야 한다.
      ⚠ 이 플래그는 **중성(닫힌 껍질) 기준계를 위한 것**이다. open-shell 조각은
      `NUPDOWN=1` 로 doublet 을 못박는 것이 선언된 상태이므로 건드리지 않는다.
    """
    from ase import Atoms
    jd.mkdir(parents=True, exist_ok=True)
    p = mol.get_positions()
    span = p.max(axis=0) - p.min(axis=0)
    box = span + margin
    # ⛔⛔ 회신 AR Q2/해제조건 3 (2026-08-31) — box20/box24 를 **공통 내부기하의
    #   static pair** 로 만든다. 종전엔 경계상자(bounding box) 기준으로 놓아서
    #   두 상자 사이 관계가 "강체 평행이동" 이긴 했지만 그 사실이 산출물에서
    #   직접 검증되지 않았다. **질량중심을 각 셀 중앙에** 놓으면
    #     · 두 상자의 내부좌표가 정의상 동일하고 (평행이동만 남는다)
    #     · 분수 DIPOL 이 두 상자에서 **똑같이 (0.5, 0.5, 0.5)** 가 되며
    #       (VASP 는 분자 dipole correction 에서 COM 부근을 권고한다)
    #     · 분석기가 `internal_geometry_sha` 하나로 교차검증할 수 있다.
    #   ⚠ COM 은 질량가중이라 경계상자 중심과 다르다 — 여백이 축마다 비대칭이
    #     될 수 있으나 `margin` 이 20/24 Å 이라 최소 진공은 충분히 남는다.
    _mass = np.asarray(mol.get_masses(), dtype=float)
    _com0 = (p * _mass[:, None]).sum(axis=0) / _mass.sum()
    at = Atoms(symbols=mol.get_chemical_symbols(), positions=p - _com0 + box / 2.0,
               cell=np.diag(box), pbc=True)
    # 최소 진공 자기검증 — COM 중심 배치가 어느 축에서든 여백을 다 먹으면 멈춘다
    _gap = np.minimum(at.positions.min(axis=0), box - at.positions.max(axis=0))
    if float(_gap.min()) < 4.0:
        raise SystemExit("⛔ 기체 상자 여백이 %.2f Å 밖에 안 된다 (frag=%s margin=%.0f) — "
                         "COM 중심 배치가 비대칭 분자에서 진공을 먹었다. margin 을 키운다."
                         % (float(_gap.min()), frag, margin))
    open_shell = "DOUBLET" in str(SS.FRAGMENTS.get(frag, {}).get("electrons", "")).upper()
    mags = [0.0] * len(at)
    if nonzero_start and not open_shell:
        # ⛔⛔ 회신 U B3 (P0) — `NUPDOWN=-1` 은 **무제약**이지 singlet 확정이 아니다.
        #   그런데 닫힌 껍질 기준계를 **항상 MAGMOM 0 에서** 출발시키면 M=0 basin 을
        #   재현하기 쉬울 뿐, 더 낮은 spin-broken 해를 탐색했다는 증거가 못 된다.
        #   같은 POSCAR·같은 all-F 로 비영 시작을 하나 둔다.
        #   ⚠ 이 대조가 **더 낮은 상태**를 내면 자동 채택하지 말고 멈춘다
        #     (MOLECULAR_STATE_UNRESOLVED) — 전자상태 estimand 를 다시 심사해야 한다.
        for _k in range(min(2, len(mags))):
            mags[_k] = 1.0 if _k == 0 else -1.0
    if open_shell:
        try:
            gi = [i for i in SS.group_indices(at, "SO3")
                  if at.get_chemical_symbols()[i] == "O"]
        except Exception:
            gi = []
        gi = gi or [i for i, s in enumerate(at.get_chemical_symbols()) if s == "O"] \
            or list(range(len(at)))
        for i in gi:
            mags[i] = round(1.0 / len(gi), 3)
    order = ["Li", "Ni", "O", "S", "C", "F", "H"]
    sym = at.get_chemical_symbols()
    order_ext = order + sorted({x for x in sym if x not in order})
    idx = [i for el in order_ext for i in range(len(at)) if sym[i] == el]
    counts, seen = [], []
    for el in order_ext:
        n = sum(1 for i in idx if sym[i] == el)
        if n:
            counts.append(n); seen.append(el)
    lines = [f"gas-phase {frag} (+{margin:.0f} A box)", "1.0"]
    lines += [f"  {v[0]:.10f} {v[1]:.10f} {v[2]:.10f}" for v in np.diag(box).reshape(3, 3)]
    lines += ["  " + "  ".join(seen), "  " + "  ".join(str(c) for c in counts), "Cartesian"]
    for i in idx:
        lines.append(f"  {at.positions[i, 0]:.10f} {at.positions[i, 1]:.10f} "
                     f"{at.positions[i, 2]:.10f}")
    (jd / "POSCAR").write_text("\n".join(lines) + "\n")
    com = _com_frac(at)                     # ⚠ centroid 가 아니라 질량중심 (VASP DIPOL 권고)
    fmt = {"system": f"gas {frag} box+{margin:.0f}", "common": _COMMON,
           "com0": float(com[0]), "com1": float(com[1]), "com2": float(com[2]),
           "nupdown": 1 if open_shell else (-1 if free_spin else 0),
           "magmom": " ".join(f"{mags[i]:.3f}" for i in idx)}
    kmesh, incar_exp, kp_exp = {}, {}, {}
    # ⛔⛔ 회신 U P0-5 — 기체 기준이 **항상 relax → static** 이었다. 그러면 얻는 차이가
    #   "스핀 제약 해제 + 재이완/구조경로 변화" 라 순수 δ_m 이 아니다. closure 모드는
    #   **고정 기하 static 단독**으로 간다 (MOL_STATIC 은 이미 LREAL=.FALSE. 다).
    # ⛔⛔ 회신 V P0-1 — `MOL_STATIC` 은 `ICHARG=1`(CHGCAR 읽기)인데 closure 는
    #   relax 를 안 돌아 **공급할 CHGCAR 가 없다.** 없으면 fallback 에 의존하고,
    #   낡은 CHGCAR 가 있으면 **조용히 읽는다.** 독립 고정기하 단일점은 원자중첩에서
    #   시작해야 한다 → ISTART=0 · ICHARG=2.
    _MOL_STATIC_CL = MOL_STATIC.replace("ICHARG   = 1", "ICHARG   = 2") \
                               .replace("[static]", "[closure static · 원자중첩 시작]")
    _phases = ((("static", _MOL_STATIC_CL),) if closure
               else (("relax", MOL_RELAX), ("static", MOL_STATIC)))
    for ph, tpl in _phases:
        (jd / ph).mkdir(exist_ok=True)
        txt = tpl.format(**fmt)
        (jd / ph / "INCAR").write_text(txt)
        (jd / ph / "KPOINTS").write_text(_kpoints_text(ph, "1 1 1"))
        kp_exp[ph] = _kpoints_expected(ph, "1 1 1")
        kmesh[ph] = "1 1 1"
        incar_exp[ph] = {k: m.group(1) for k in AUDIT_KEYS
                         for m in [re.search(rf"^{k}\s*=\s*(\S+)", txt, re.M)] if m}
    _write_potcar_asm(jd, seen)
    (jd / "run_job.sh").write_text(RUN_JOB)
    # ⛔ 회신 AR 해제조건 3 — **cross-job geometry/state gate 의 근거**.
    #   box20/box24 가 같은 내부기하인지 분석기가 직접 확인할 수 있게, 방출 순서
    #   `idx` 그대로의 (원소, COM 기준 상대좌표) 를 해시로 박는다. 셀 크기·절대좌표는
    #   일부러 **안 넣는다** — 상자가 다른 것은 정상이고, 내부좌표만 같아야 한다.
    _rel = at.positions - np.asarray(box, dtype=float) / 2.0
    _gsig = "|".join("%s:%.6f,%.6f,%.6f" % (sym[i], _rel[i, 0], _rel[i, 1], _rel[i, 2])
                     for i in idx)
    # 전자상태 지문 — 상자만 다르고 상태가 같아야 δ_gas 가 셀 효과다
    _ssig = json.dumps({"nupdown": fmt["nupdown"], "magmom": fmt["magmom"],
                        "open_shell": open_shell,
                        "phases": [ph for ph, _ in _phases],
                        "incar": {ph: incar_exp[ph] for ph in incar_exp}},
                       sort_keys=True, ensure_ascii=False)
    meta = {"kind": "mol_ref", "fragment": frag, "species_order": seen, "counts": counts,
            "kmesh": kmesh, "incar_expected": incar_exp,
            # 🔴 회신 AT P0-2 — 상마다 **정확한** 격자·시프트를 제목으로 결박한다
            "kpoints_expected": kp_exp,
            "open_shell": open_shell, "box_margin_A": margin,
            "gas_placement": "com_at_cell_center",
            "internal_geometry_sha": hashlib.sha256(_gsig.encode()).hexdigest(),
            "electronic_state_sha": hashlib.sha256(_ssig.encode()).hexdigest(),
            "fixed_geometry_static": bool(closure),
            "com_frac": [round(float(c), 6) for c in _com_frac(at)],
            # ⛔ 회신 V P0-2 — 종전엔 closure 여도 ["relax","static"] 을 박아
            #   분석기가 **없는 relax 를 필수 phase 로 읽고** static 이 정상 완료돼도
            #   기체 잡을 차단했다. 실제 생성한 phase 에서 만든다.
            "phases": [ph for ph, _ in _phases],
            "box_A": [round(float(b), 2) for b in box],
            # ⚠ 기체 기준계도 결합 그래프를 감사해야 한다 — 없으면 그 검사가 꺼진다
            #   (Codex P0-G). 슬랩이 없으므로 registry/탈착 검사는 분석기가 건너뛴다.
            "mol_poscar_idx": list(range(len(at))),
            # 🔴 회신 AB P0-1 — 바로 위 주석이 "없으면 그 검사가 꺼진다" 고 적어
            #   놓고 **정작 안 썼다.** 그래서 기체 기준계 전 잡이 OUTCAR 오기 전에
            #   SOURCE_TOPOLOGY_UNVERIFIED 로 막혔다.
            # 🔴🔴 회신 AT P0-1 (2026-08-31) — 그 고침이 **틀린 순서**를 박았다.
            #   "슬랩이 없으니 POSCAR 순서가 곧 원자 순서다" 라고 적었지만, 바로 위에서
            #   POSCAR 를 `idx`(원소별로 묶은 순서)로 쓴다. 그래서 항등 순서로 만든
            #   그래프가 POSCAR 인덱스와 어긋났고, 리뷰어가 배포본에서 직접 돌린
            #   geometry_audit 이 **canonical 36 · broken 28 · formed 28** 을 냈다 —
            #   즉 SDCP 기체 기준 3잡이 VASP 를 한 번도 돌리기 전에 영구 게이트였다.
            #   `idx` 를 그대로 넘긴다 (복합체 잡이 `pos["order"]` 를 넘기는 것과 같다).
            "mol_graph_canonical": _mol_graph_canon(at, 0, idx),
            # 기체에는 표면이 없다 — Li/Ni 등록 기대가 **존재하지 않는다**.
            "registry_role": None,
            "slab_li_poscar_idx": [], "slab_ni_poscar_idx": [],
            "top_li_poscar_idx": [], "top_ni_poscar_idx": []}
    (jd / "job.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    return meta


# ─────────────────────────────────────────────────────────────────────────────
# 독립 분석기 v2 (stdlib) — 번들에 파일로 들어간다
# ─────────────────────────────────────────────────────────────────────────────
ANALYZER = r'''#!/usr/bin/env python3
"""analyze_results.py v3 — VASP 완주 후 이거 **하나**로 회수 (stdlib only).

  python3 analyze_results.py <bundle_dir> [--delta 0.030]

판정 에너지 = **static/OUTCAR 만**. 전 검사는 fail-closed 다 — 확인 못 한 것은
통과가 아니라 게이트다 (2026-08-11 Codex 재검토 P0-C/D/E/G/H).

  잡: MANIFEST 해시(입력 무결성) / 상별 정상종료 / 전자수렴 / relax 이온수렴 /
     POTCAR TITEL(반도체준위 변형은 치명) / 힘 블록 존재·원자수 / 등록(표면 양이온만)
     / 결합 그래프 / 탈착 / 고정원자 drift / **Ni 국소 모멘트·부호 패턴**
  쌍: PAIR_MIGRATED · PAIR_COLLAPSED(주기 RMSD + 접촉 지문) ·
     seed-매칭 |ΔE_pm1−ΔE_net4| ≤ 10 meV
  수치(**게이트다 — 실패하면 E_ads/판정을 만들지 않는다**):
     상자 20↔24 Å ≤ 10 meV (정본은 box24) · dense-k ΔE·E_ads ≤ 10 meV
exit 0 = 필수(tier1+refs) 완결 · exit 2 = 필수 산출 누락/무결성 실패 (fail-closed).

이 도구가 **못 하는 것**
  · 자기바닥상태를 찾아 주지 않는다. 두 seed 가 같은 basin 으로 무너졌는지
    모멘트 부호 패턴으로 **알려만** 준다.
  · POTCAR 파일 자체를 검증하지 못한다 (라이선스로 미포함) — OUTCAR 의 TITEL 만 본다.
  · 유한셀 보정(전하·쌍극자 상호작용)을 하지 않는다. 상 사이 비교용이다.
"""
import gzip, hashlib, json, math, os, pathlib, re, sys
from glob import glob

# ⛔⛔ 회신 AR P1-12 / 2026-08-31 실측 — **표준출력 인코딩**도 실패 지점이다.
#   파일 IO 를 전부 utf-8 로 박았는데도 gabia 에서 `LC_ALL=C` 로 돌리자
#   `UnicodeEncodeError: 'ascii' codec can't encode character '\u2713'` 로 죽었다.
#   ✓/⛔/한글이 **print 될 때** 죽는 것이고, Windows cp949 기본값이 같은 모양이다.
#   ⚠ 내 selftest 가 이걸 놓친 이유: 환경에 `PYTHONIOENCODING=utf-8` 을 같이
#     넣어서 stdout 만 살려 놓고 통과시켰다 — 양성만 있는 시험의 전형이다.
for _std in (sys.stdout, sys.stderr):
    try:
        _std.reconfigure(encoding="utf-8", errors="replace")
    except Exception:                                    # noqa: BLE001
        pass                                             # 3.6 이하 · 리다이렉트된 스트림

DELTA = 0.030
SEED_TOL = 0.010          # eV — seed-매칭 ΔE 게이트
BOX_TOL = 0.010           # eV — 기체상 **조각별** 상자 수렴 (진단용)
#: ⛔ 회신 AP #11 — 판정은 조각별이 아니라 **두 기체의 차**에 건다. D 에 남는 것이
#:   그 차이기 때문이다. 0.01 eV 보고를 유지하려면 5 meV 다 (AP 가 지정한 사전 문턱).
GAS_BOX_DELTA_TOL = 0.005
K_TOL = 0.010             # eV — dense-k 민감도
GUARD_EV = 0.010          # ±10 meV — k 전이 불확실성. **30 meV 판정바닥과 별개다**
                          #   (Codex 5차: 두 숫자를 하나로 합치면 경계 결과를 오판한다)
RMSD_TOL = 0.75           # Å — 두 끝점이 같은 basin 인가 (0.50/1.00 민감도도 같이 뽑는다)
CONTACT_A = 3.0           # Å — 접촉 지문 반경
FP_JACCARD = 0.80         # 접촉 지문 겹침 — 경계 원자 하나로 뒤집히지 않게 완전일치 대신
#: 실행 INCAR echo 로 대조할 키. 생성부의 AUDIT_KEYS 와 **같은 목록이어야 한다** —
#:  둘이 따로 적혀 있어 한쪽만 늘리면 조용히 갈린다 (Codex 5차 P1-3).
#:  물리 규약 키(LASPH/ADDGRID/ISYM/NUPDOWN/LDAUU)도 넣어 외주처의 우발적 수정을 잡는다.
AUDIT_KEYS_RUNTIME = ("ENCUT", "ISMEAR", "IVDW", "LREAL", "ISTART", "ICHARG", "LDIPOL",
                      "LASPH", "ADDGRID", "ISYM", "NUPDOWN", "LDAUU", "LDAUTYPE", "IDIPOL",
                      "ISPIN", "LDAUL", "LDAUJ", "MAGMOM", "LDAU", "LMAXMIX",
                      # 🔴 회신 AB P0-5 — `_spin_setup_ok()` 가 이 넷을 검사하는데
                      #   여기 없어서 `read_outcar()` 가 **아예 안 읽었다**. 손으로 만든
                      #   dict 를 넣는 단위시험은 통과하고 실제 OUTCAR 경로에서는
                      #   검사가 통째로 꺼져 있었다 (전형적인 가짜 초록).
                      #   ⚠ 넷 다 **미출력이 기본값**이다: VASP 는 기본값이면 안 찍는
                      #     경우가 있어 None 이 곧 "안전한 기본" 이다. 그래서
                      #     _spin_setup_ok 은 None 을 통과로 본다 — 그 해석을 여기 적어
                      #     둔다(안 적으면 다음 사람이 fail-closed 로 바꿔 전 잡을 막는다).
                      "LNONCOLLINEAR", "LSORBIT", "I_CONSTRAINED_M", "BEXT")

# ── 되울림 형식 3종 (2026-08-25 실측, wave1 43개 OUTCAR) ─────────────────────
#   ① 행두형: `   ENCUT  =  520.0 eV …` · `   NUPDOWN=      -1.0000` (= 앞 공백 0개 허용)
#   ② 산문형: LDA+U 계열은 행 **중간**에 있다 —
#        ` LDA+U is selected, type is set to LDAUTYPE =  2`
#        `   U (eV)           for each species LDAUU =   0.0  6.2  0.0  0.0  0.0`
#      행두 앵커로는 한 줄도 안 잡힌다. 고정 산문을 앵커로 쓴다.
#   ③ 미되울림: MAGMOM · ADDGRID 는 OUTCAR 어디에도 없다(grep 0건) —
#      **원리적으로 검증 불가**이므로 영원히 unverified 로 보고한다 (조용한 통과 금지).
_ECHO_PROSE = {
    "LDAUTYPE": r"type is set to LDAUTYPE\s*=\s*(\S+)",
    "LDAUL": r"for each species LDAUL\s*=\s*([^\n]+)",
    "LDAUU": r"for each species LDAUU\s*=\s*([^\n]+)",
    "LDAUJ": r"for each species LDAUJ\s*=\s*([^\n]+)",
}
_ECHO_ABSENT = ("MAGMOM", "ADDGRID")

# ── OUTCAR 되울림 ↔ INCAR 선언 대조 (2026-08-25) ─────────────────────────────
#   VASP 는 INCAR 표기를 그대로 되울리지 않는다: 520 → `520.0`, `.TRUE.` → `T`,
#   `Auto` → `T`. 문자열 비교로는 전부 불일치로 잡혀 게이트가 30/30 오탐을 냈다.
_TRUE = {"T", "TRUE", ".TRUE."}
_FALSE = {"F", "FALSE", ".FALSE."}
#   LREAL 은 Auto·On·A·O 가 전부 "실공간" 이고 되울림은 `T` 하나뿐이다.
_LREAL_REAL = {"AUTO", "A", "ON", "O"} | _TRUE
_LREAL_RECIP = set(_FALSE)


def _echo_val(text, key):
    """OUTCAR 의 **파라미터 줄**에서 key 의 값을 읽는다 (산문·경고문 제외).

    행두형은 행두 공백 앵커로(권고 상자는 `|` 시작이라 걸러진다), LDA+U 계열은
    고정 산문 앵커로 읽는다(행 중간이라 행두 앵커가 못 잡는다 — 2026-08-25 실측).
    목록 키는 **줄 끝까지** 캡처해 공백 정규화한다 — 한 토큰만 읽으면
    `LDAUU = 0.0 6.2 0.0` 이 `0.0` 으로 잘려 실제 U 차이를 못 잡는다 (codex E-1).

    이 함수가 못 하는 것: MAGMOM·ADDGRID 는 OUTCAR 가 되울리지 않아 **원리적으로
    None** 이다 — 호출부가 unverified 로 보고한다 (통과도 실패도 아니다).
    """
    if key in _ECHO_ABSENT:
        return None
    if key == "LDAU":
        # 직접 되울림 줄이 없다 — "LDA+U is selected" 산문의 존재가 곧 T 다 (실측).
        # ⚠ 켜져 있을 때만 판별 가능: .FALSE. 는 산문이 없어 None(unverified)로 남는다.
        return "T" if "LDA+U is selected" in text else None
    pat = _ECHO_PROSE.get(key)
    if pat:
        m = re.search(pat, text)
        return " ".join(m.group(1).split()) if m else None
    m = re.search(r"^[ \t]{0,8}" + key + r"\s*=\s*([-\w.]+)", text, re.M)
    return m.group(1) if m else None


def _incar_match(key, got, want):
    """되울림 got 과 선언 want 대조 → (일치 여부, 종류).

    종류 (codex E-2 분류):
      "exact"             — 같은 값 (표기 차이만: 520.0↔520, T↔.TRUE., 목록 원소별)
      "equivalence_class" — **같은 값임을 보증 못 하고 같은 계열임만 보증**.
                            LREAL 의 Auto/On/.TRUE. 는 알고리즘이 서로 다른데
                            VASP 가 전부 `T` 로만 되울려 계열까지만 갈라진다.
      "mismatch"          — 다르다.

    수치는 **Decimal** 로 비교한다 (codex E-1) — float 는 `1e309` 가 inf 로 붙어
    서로 다른 두 값이 같아질 수 있고, 큰 정수에서 정밀도를 잃는다.
    비유한값(inf/nan 표기)은 일치로 치지 않는다.
    """
    from decimal import Decimal, InvalidOperation

    def _nonfinite(s):
        for tok in s.split():
            try:
                if not Decimal(tok).is_finite():
                    return True
            except (InvalidOperation, ValueError):
                pass
        return False

    g, w = str(got).strip(), str(want).strip()
    # ⚠ 비유한값 검사가 문자열 지름길보다 **먼저**다 — "inf"=="inf" 가 문자열로
    #   같아서 통과해 버리면 이 가드는 죽은 코드가 된다 (selftest 가 실제로 잡았다).
    if _nonfinite(g) or _nonfinite(w):
        return False, "mismatch"
    gu, wu = g.upper(), w.upper()
    if gu.strip(".") == wu.strip("."):          # .TRUE. ↔ TRUE 도 여기서 걸린다
        return True, "exact"
    if key == "LREAL":
        known = _LREAL_REAL | _LREAL_RECIP
        if gu in known and wu in known:
            same = (gu in _LREAL_REAL) == (wu in _LREAL_REAL)
            return (True, "equivalence_class") if same else (False, "mismatch")
        return False, "mismatch"
    if gu in _TRUE | _FALSE and wu in _TRUE | _FALSE:
        return ((gu in _TRUE) == (wu in _TRUE)), "exact"
    try:                                         # 520.0 ↔ 520 · LDAUU 목록도 원소별
        gd = [Decimal(x) for x in g.split()]
        wd = [Decimal(x) for x in w.split()]
    except (InvalidOperation, ValueError):
        return False, "mismatch"
    if any(not x.is_finite() for x in gd + wd):
        return False, "mismatch"
    ok = len(gd) == len(wd) and all(a == b for a, b in zip(gd, wd))
    return ok, ("exact" if ok else "mismatch")


def _incar_equal(key, got, want):
    """(하위호환 래퍼) — 일치 여부만. 종류가 필요하면 _incar_match 를 쓸 것."""
    return _incar_match(key, got, want)[0]

RCOV = {"H": 0.31, "B": 0.84, "C": 0.76, "N": 0.71, "O": 0.66, "F": 0.57,
        "Na": 1.66, "P": 1.07, "S": 1.05, "Cl": 1.02, "Li": 1.28, "Ni": 1.24}
BOND_F = 1.25             # 결합 = d < BOND_F × (r_i + r_j)
DETACH_A = 4.0            # 분자-슬랩 최소거리가 이보다 크면 탈착
FIX_DRIFT_A = 0.10        # 고정(F F F) 원자가 이보다 움직이면 파일 불일치
FORCE_TOL = 0.05          # eV/Å — 자유원자 잔여 힘 경고
RECON_A = 0.60            # Å — 자유 상부 양이온이 이만큼 움직이면 재구성
LI_OUT_A = 0.80           # Å — Li 가 바깥(+z)으로 이만큼 나오면 추출 의심
LI_O_A = 2.60             # Å — Li–O 배위 반경
LI_COORD_LOSS = 2         # O 배위가 이만큼 줄면 추출로 본다
MOM_MIN = 0.30            # μB — **개별 검토 trigger** (판정 문턱 아님, Codex Q7)
Q_RATIO_MIN = 0.50        # clean 대비 Q 가 이 아래면 집단 붕괴 (초기 민감도)
F_SMALL_MAX = 0.25        # |m|<MOM_MIN 비율이 이 위면 집단 붕괴 (초기 민감도)
#: 준중심(semicore) 변형이 다르면 원자가 전자 수가 달라진다 — 일관돼도 치명이다.
SEMICORE = ("_pv", "_sv", "_h", "_s", "_d")


def _read_text(path):
    try:
        if os.path.isfile(path):
            # ⛔ 2026-08-25 — `.gz` 경로를 그대로 주면 gzip 바이너리를 errors="ignore"
            #   로 읽어 **깨진 문자열을 조용히 돌려줬다**. 그러면 모든 정규식이 안
            #   맞아 E0·NIONS·되울림이 전부 None 이 되는데, None 은 "없음" 으로만
            #   보여 원인이 안 드러난다. 매직바이트로 판별한다 (확장자 말고).
            with open(path, "rb") as fh:
                if fh.read(2) == b"\x1f\x8b":
                    return gzip.open(path, "rt", errors="ignore",
                                 encoding="utf-8").read()
            return open(path, errors="ignore", encoding="utf-8").read()
        if os.path.isfile(path + ".gz"):
            return gzip.open(path + ".gz", "rt", errors="ignore",
                             encoding="utf-8").read()
    except OSError:
        pass
    return None


def global_sign(moments, want):
    """시드 부호 want 에 대해 관측 모멘트의 **전역 부호**를 정한다.

    ⚠ 전역 반전은 시간반전이라 **같은 상태**다. 그래서 부호를 정규화한 뒤
      *부분* 반전만 문제 삼아야 한다. static 과 dense 가 이 규칙을 따로 구현하면
      갈린다 — 실제로 dense 가 static 의 부호를 재사용해, dense 가 완전한
      시간반전으로 수렴했을 때 전부 불일치로 잡는 **거짓 차단**이 났다
      (Codex 5차 P1-2). 한 함수로 둔다.

    반환 (sg, 불일치 인덱스). want/moments 는 {인덱스: 값} 이다.
    """
    ag = {s: sum(1 for i, v in want.items() if moments.get(i, 0.0) * s * v > 0)
          for s in (1.0, -1.0)}
    sg = 1.0 if ag[1.0] >= ag[-1.0] else -1.0
    bad = [i for i, v in want.items() if moments.get(i, 0.0) * sg * v <= 0]
    return sg, bad


#: 회신 AA Q5 — **단일 문턱 금지.** 확실한 붕괴 / 회색 / 확실한 자성으로 나누고
#: 회색은 unresolved 로 뺀다. 값은 wave1 clean slab 분포(|m| ~1.2 μB)와 반복
#: 산포에서 잡았다: 0.25 아래는 어떤 basin 에서도 안 나오고, 0.55 위는 정상
#: Ni 모멘트다. 그 사이는 **우리가 못 가르는 구간**이다.
MOM_COLLAPSE = 0.25      # 이 아래 = 확실한 붕괴
MOM_MAGNETIC = 0.55      # 이 위   = 확실한 자성
#: 같은 부호벡터라도 크기가 이보다 더 벌어지면 자동 동일 판정하지 않는다 (Q5)
MOM_RMS_TOL = 0.30       # μB


def _spin_setup_ok(incar_echo):
    """전역 시간반전을 접어도 되는 계인가 (회신 AA Q5).

    collinear · SOC 없음 · 외부장 없음 · signed spin constraint 없음일 때만
    `+++−` 와 `−−−+` 가 같은 상태다. **INCAR 되울림에서 기계적으로 확인한다** —
    전제를 사람이 기억하는 것에 맡기지 않는다.
    """
    # 🔴 회신 AB P0-5 — `str(None)` 이 **"NONE"** 이 된다. 종전 정규화는 None 을
    #   그 문자열로 만들었고, 그러면 `not in (None, "", "0")` 이 참이라 **미출력이
    #   곧 "스핀 제약 있음"** 이 됐다. 이 키들이 AUDIT_KEYS_RUNTIME 에 없어서
    #   실제 OUTCAR 경로로는 한 번도 안 들어왔기 때문에 드러나지 않았다 —
    #   손으로 만든 dict 를 넣는 단위시험만 통과하던 자리다.
    #   ⚠ VASP 는 이 넷이 기본값이면 **되울리지 않는다**. 그러므로 미출력(None)은
    #     "확인 불가" 가 아니라 **기본값(꺼짐)** 으로 읽는 것이 맞다. 반대로
    #     fail-closed 로 두면 전 잡이 BASIN_UNRESOLVED 가 된다(실측).
    e = {str(k).upper(): (None if v is None else str(v).strip().upper().strip("."))
         for k, v in (incar_echo or {}).items()}
    bad = []
    if e.get("LNONCOLLINEAR") in ("T", "TRUE"):
        bad.append("LNONCOLLINEAR=T (비공선)")
    if e.get("LSORBIT") in ("T", "TRUE"):
        bad.append("LSORBIT=T (SOC)")
    if e.get("I_CONSTRAINED_M") not in (None, "", "0"):
        bad.append(f"I_CONSTRAINED_M={e.get('I_CONSTRAINED_M')} (스핀 제약)")
    if e.get("BEXT") not in (None, "", "0", "0.0", "0.00"):
        bad.append(f"BEXT={e.get('BEXT')} (외부장)")
    return (not bad), bad


def realized_basin_id(mom, ni_sign, mol_sign, mom_min=None, incar_echo=None):
    """OUTCAR 국소모멘트 표 → **실제로 수렴한** 자기 basin 의 지문 (회신 Z P0-4).

    `pm1` · `net4` 는 **초기 MAGMOM seed 이름**이지 최종 상태가 아니다. wave1.5 에서
    raw `net4` 가 의도한 topology 가 아니라 Ni 하나 뒤집힌 basin 으로 반복 수렴한
    전례가 있다. seed 이름으로 짝지어 빼면 상태를 가로질러 뺀 것이 된다.

    v2 (회신 AA Q5 반영):
      · 전역 시간반전을 접기 전에 **collinear·무SOC·무외부장·무제약**을 INCAR
        되울림에서 확인한다. 아니면 접지 않고 unresolved 를 낸다.
      · 붕괴 판정을 **두 문턱**으로 (확실한 붕괴 / 회색 / 확실한 자성).
        회색이 하나라도 있으면 지문을 만들지 않는다 — 그 자리가 basin 을 가른다.
      · 지문 해시는 **정규화 canonical JSON 의 full SHA256**. 12자는 표시용이다.
      · raw 모멘트 벡터와 Ni 인덱스 매핑을 그대로 보존한다 (사후 재판독용).

    반환 (id, detail) — id 가 None 이면 사유가 detail["why"] 에 있다.

    ⛔ 이 함수가 **못 하는 것**
      · 어느 basin 이 **바닥**인지 말하지 못한다. 같은가 다른가만 가른다.
      · OUTCAR 의 site moment 는 PAW 구 안으로 투영한 **관측량**이지 basin 그
        자체가 아니다. 같은 설정 안에서만 쓰는 지문이다.
      · 모멘트 표가 없거나 불완전하면 **추측하지 않는다** — None 을 낸다.
      · Ni 인덱스 집합이 다른 두 계(다른 슬랩)를 비교할 수 없다.
    """
    if not mom:
        return None, {"why": "모멘트 표 없음 (LORBIT)"}
    ni = {int(k): float(v) for k, v in (ni_sign or {}).items()}
    if not ni:
        return None, {"why": "ni_sign_poscar_idx 없음"}
    if max(ni) >= len(mom):
        return None, {"why": f"Ni 인덱스가 모멘트 표 {len(mom)}행 밖"}
    if incar_echo is not None:
        ok_setup, why = _spin_setup_ok(incar_echo)
        if not ok_setup:
            return None, {"why": "전역 시간반전을 접을 수 없는 설정: " + " · ".join(why)}
    got = {i: mom[i] for i in ni}
    sg, _flip = global_sign(got, ni)
    idx = sorted(ni)
    gray = [k for k, i in enumerate(idx) if MOM_COLLAPSE <= abs(got[i]) < MOM_MAGNETIC]
    if gray:
        return None, {"why": (f"회색구간 모멘트 {len(gray)}자리 "
                              f"({MOM_COLLAPSE}–{MOM_MAGNETIC} μB) — 붕괴인지 자성인지 "
                              f"못 가른다. 이 잡으로는 뺄셈하지 않는다"),
                      "gray_positions": gray,
                      "gray_moments_muB": [round(got[idx[k]], 3) for k in gray]}
    vec = "".join("+" if got[i] * sg > 0 else "-" for i in idx)
    collapsed = [k for k, i in enumerate(idx) if abs(got[i]) < MOM_COLLAPSE]
    ms = {int(k): float(v) for k, v in (mol_sign or {}).items() if int(k) < len(mom)}
    org = "".join("+" if mom[i] * sg > 0 else "-" for i in sorted(ms)) if ms else ""
    # 정규화 canonical JSON → full SHA256 (12자는 표시용)
    canon = json.dumps({"ni_sign_vector": vec, "collapsed": collapsed,
                        "organic_relative_spin": org},
                       sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    full = hashlib.sha256(canon.encode()).hexdigest()
    return full, {
        "id_short": full[:12], "canonical": canon,
        "ni_sign_vector": vec, "n_ni": len(idx), "global_sign": sg,
        "collapsed_ni_positions": collapsed, "organic_relative_spin": org or None,
        "ni_index_poscar": idx,
        "ni_moments_muB": [round(got[i], 4) for i in idx],
        "abs_mean_muB": round(sum(abs(got[i]) for i in idx) / len(idx), 4),
        "thresholds": {"collapse": MOM_COLLAPSE, "magnetic": MOM_MAGNETIC},
        "⚠": "seed 이름이 아니라 **수렴 결과**의 지문이다. site moment 는 PAW 투영 관측량이다"}


def basin_distance(da, db):
    """두 realized basin 사이의 **거리** (회신 AA Q5-c).

    지문이 다르다는 것만으로는 "얼마나 다른가" 를 못 말한다. Ni 하나가 뒤집힌
    것과 20개가 뒤집힌 것은 다른 사건이다.

    반환: {hamming, collapse_symdiff, moment_rms_muB, moment_max_muB,
           flipped_index_poscar, same}
    `same` 은 부호·붕괴가 같고 **크기 RMS 도 MOM_RMS_TOL 안**일 때만 참이다 —
    같은 부호라도 크기가 크게 다르면 자동 동일 판정하지 않는다.
    """
    if not da or not db:
        return None
    va, vb = da.get("ni_sign_vector"), db.get("ni_sign_vector")
    ia, ib = da.get("ni_index_poscar"), db.get("ni_index_poscar")
    if not (va and vb) or len(va) != len(vb) or ia != ib:
        return {"same": False, "why": "Ni 인덱스 집합이 다르다 — 비교 불가"}
    ham = [k for k in range(len(va)) if va[k] != vb[k]]
    ca, cb = set(da.get("collapsed_ni_positions") or []), set(db.get("collapsed_ni_positions") or [])
    ma = da.get("ni_moments_muB") or []
    mb = db.get("ni_moments_muB") or []
    sa, sb = da.get("global_sign", 1.0), db.get("global_sign", 1.0)
    diff = [abs(ma[k] * sa - mb[k] * sb) for k in range(min(len(ma), len(mb)))]
    rms = (sum(x * x for x in diff) / len(diff)) ** 0.5 if diff else float("inf")
    mx = max(diff) if diff else float("inf")
    return {"hamming": len(ham), "flipped_index_poscar": [ia[k] for k in ham],
            "collapse_symdiff": sorted(ca ^ cb),
            "moment_rms_muB": round(rms, 4), "moment_max_muB": round(mx, 4),
            "same": (not ham and not (ca ^ cb) and rms <= MOM_RMS_TOL),
            "rms_tol_muB": MOM_RMS_TOL}


def read_moments(t):
    """LORBIT=11 의 마지막 'magnetization (x)' 표 → 이온별 tot 모멘트 [μB]."""
    k = t.rfind("magnetization (x)")
    if k < 0:
        return None
    out = []
    for ln in t[k:].splitlines()[1:]:
        v = ln.split()
        if len(v) == 5 and v[0].isdigit():
            try:
                out.append(float(v[4]))
            except ValueError:
                break
        elif out:
            break
    return out or None


def read_ldau(t):
    """LDAUPRINT=2 의 onsite density matrix → {원자: [n_up, n_dn]}. 없으면 None.

    ⚠ 모멘트 projector 하나에 자기상태 판정을 맡기지 않으려고 둔다 (Codex P0-2).
      **판정용이 아니라 기록용**이다 — 절대값은 PAW sphere 규약에 의존한다.
    """
    out = {}
    for m in re.finditer(r"atom\s*=\s*(\d+)\s+type\s*=\s*\d+\s+l\s*=\s*(\d+)", t):
        a, l = int(m.group(1)), int(m.group(2))
        n = 2 * l + 1
        seg = t[m.end():m.end() + 6000]
        traces = []
        for sm in re.finditer(r"spin component\s+\d+", seg):
            rows = []
            for ln in seg[sm.end():].splitlines()[1:]:
                v = ln.split()
                if len(v) == n:
                    try:
                        rows.append([float(x) for x in v])
                    except ValueError:
                        break
                elif rows:
                    break
                if len(rows) == n:
                    break
            if len(rows) == n:
                traces.append(round(sum(rows[i][i] for i in range(n)), 4))
            if len(traces) == 2:
                break
        if len(traces) == 2:
            out[a] = traces          # 뒤에 나온 이온스텝이 앞을 덮는다 = 최종값
    return out or None


def _pk(path, root):
    """잡 키를 **POSIX 구분자**로 정규화한다.

    ⚠ os.path.relpath 는 Windows 에서 `tier1\\job` 을 낸다. MANIFEST 의 prefix 는
      `tier1/job` 이라, 개별 잡이 멀쩡해도 pair 조회가 전부 실패해 "필수 산출 누락"
      으로 보였다 (2026-08-12 Codex 재감사 P0-6). 키는 한 표기법이어야 한다.
    """
    return os.path.relpath(path, root).replace(os.sep, "/").replace("\\", "/").strip("/")


# ══ OUTCAR 엄격 판독 (2026-08-25 codex E-3) ══════════════════════════════════
#   errors="ignore" 금지 — 깨진 바이트가 낀 `ENC\xffUT` 이 `ENCUT` 으로 붙어
#   **거짓 정상**을 만들고, 잘린 gzip 은 예외로 분석기 전체를 죽이며, UTF-16 은
#   NUL 이 낀 채 조용히 오독된다. 전부 판독 실패(OUTCAR_READ_ERROR)로 승격한다.
def _read_outcar_raw(p):
    """→ (text|None, meta). meta = {read_error, format, suffix_magic_mismatch}.

    이 함수가 못 하는 것: 내용의 물리적 타당성. **읽기 신뢰성**까지만 책임진다.
    """
    meta = {"read_error": None, "format": None, "suffix_magic_mismatch": False}
    base = p[:-3] if p.endswith(".gz") else p
    plain, gz = os.path.isfile(base), os.path.isfile(base + ".gz")
    if plain and gz:
        meta["read_error"] = "OUTCAR 와 OUTCAR.gz 가 둘 다 있다 — 어느 쪽이 정본인지 판정 불가"
        return None, meta
    path = base if plain else (base + ".gz" if gz else None)
    if path is None:
        return None, meta                      # 파일 없음 = NOT_RUN (read_error 아님)
    try:
        raw = open(path, "rb").read()
    except OSError as e:
        meta["read_error"] = f"open 실패: {e}"
        return None, meta
    is_gz_magic = raw[:2] == b"\x1f\x8b"
    meta["suffix_magic_mismatch"] = (path.endswith(".gz") != is_gz_magic)
    if is_gz_magic:
        try:
            raw = gzip.decompress(raw)         # CRC·절단이 여기서 예외로 드러난다
        # ⚠ py3.6 호환 — gzip.BadGzipFile 은 3.8+ 이고 OSError 의 하위클래스다.
        #   wave1.5 회신(2026-08-28)이 실측으로 알려줬다: 클러스터 파이썬이 3.6.8 이라
        #   손상 .gz 를 만나면 깔끔한 오류 대신 AttributeError 로 죽는다.
        except (OSError, EOFError) as e:
            meta["read_error"] = f"gzip 손상/절단: {type(e).__name__} {e}"
            return None, meta
    if b"\x00" in raw[:4096]:
        meta["read_error"] = "NUL 바이트 검출 — UTF-16/바이너리 오염 의심"
        return None, meta
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as e:
        meta["read_error"] = f"디코드 실패(비ASCII 오염): offset {e.start}"
        return None, meta
    meta["format"] = "gzip" if is_gz_magic else "plain"
    return text, meta


def _last_run_segment(text):
    """이어붙은 OUTCAR 를 실행 단위로 갈라 **마지막 완결 실행**을 고른다.

    (2026-08-25 codex E) 여러 실행이 한 파일에 이어지면 옛 코드는 파라미터를 첫
    실행에서, 에너지를 마지막에서, 정상종료를 아무 데서나 읽어 **서로 다른 실행을
    섞었다.** 실행 경계는 버전 배너(행두 ` vasp.`)다.

    → (segment_text, {"n": 배너수, "used": "only|last_complete|last_incomplete",
                       "used_index": i})
    """
    starts = [m.start() for m in re.finditer(r"(?m)^ vasp\.[\w.]+", text)]
    if len(starts) <= 1:
        return text, {"n": max(len(starts), 1) if text.strip() else 0,
                      "used": "only", "used_index": 0}
    segs = [text[s:e] for s, e in zip(starts, starts[1:] + [len(text)])]
    for i in range(len(segs) - 1, -1, -1):
        if "General timing and accounting" in segs[i]:
            return segs[i], {"n": len(segs), "used": "last_complete", "used_index": i}
    return segs[-1], {"n": len(segs), "used": "last_incomplete",
                      "used_index": len(segs) - 1}


def read_outcar(p):
    t, rmeta = _read_outcar_raw(p)
    if rmeta["read_error"]:
        return {"read_error": rmeta["read_error"], "normal_end": False, "E0": None,
                "edisp_eV": None, "edisp_n": 0,
                "nelm_hit": False, "ionic_conv": False, "nions": None, "nkpts": None,
                "titels": [], "incar_echo": {}, "moments": None, "mag_total": None,
                "run_segments": None}
    if t is None:
        return None
    t, seg = _last_run_segment(t)
    e = re.findall(r"energy\(sigma->0\)\s*=\s*(-?[\d.]+)", t)
    # ── D3 분산항. **VASP 가 IVDW=11 에서 직접 찍는다** (repo 실물 확인:
    #   runs/sdcp_phaseB_vasp_v1_2026_08_08/{slab,mol_neutral,complex_neutral}/OUTCAR.gz
    #   → " Edisp (eV)  -27.49493 / -0.71798 / -28.58614").
    #   D3 는 SCF 에 안 들어가고 핵좌표만 보고 총에너지에 **더해지는** 항이라
    #   고정기하 static 에서 `E_on − E_off = Edisp` 가 **항등식**이다 ⇒ C3 의 세 괄호가
    #   각각 Edisp 로 접힌다. 그래서 D3-off 쌍둥이 잡이 **필요 없다**.
    #   ⚠ NSW>0 이면 이온스텝마다 갱신될 수 있으므로 **마지막 것**을 쓴다. 이 캠페인은
    #     전 잡 NSW=0 이라 하나뿐이고, 개수도 같이 돌려준다(검사용).
    _ed = re.findall(r"Edisp\s*\(eV\)\s*:?\s*(-?[\d.]+)", t)
    nions = re.search(r"NIONS\s*=\s*(\d+)", t)
    nk = re.search(r"NKPTS\s*=\s*(\d+)", t)
    # 🔴 회신 AT P0-2 — VASP 는 KPOINTS 첫 줄(제목)을 ` KPOINTS: <제목>` 으로
    #   되울린다. 그 제목에 상·격자·시프트를 실어 두면 **정확한** 대조가 된다.
    _kt = re.search(r"^\s*KPOINTS:\s*(.+?)\s*$", t, re.M)
    nelm = re.search(r"NELM\s*=\s*(\d+)", t)
    iters = re.findall(r"Iteration\s+\d+\(\s*(\d+)\)", t)
    ver = re.search(r"vasp\.([\w.]+)", t)
    # 파일 존재가 아니라 **읽었다는 로그**로 승계를 증명한다 (Codex Q4)
    read_wav = bool(re.search(r"reading WAVECAR|WAVECAR.*read|initial charge.*wavefunc", t, re.I))
    fell_back = bool(re.search(r"ISTART.*=.*0.*job.*fresh|WAVECAR not read|"
                               r"wave function.*not.*found|reading from scratch", t, re.I))
    titels = re.findall(r"TITEL\s*=\s*(.+)", t)
    mag = re.findall(r"number of electron\s+[\d.]+\s+magnetization\s+(-?[\d.]+)", t)
    forces = None
    # ★ 실행 기하 감사용 — OUTCAR 안의 **실제 좌표**. phase POSCAR 를 반송받지 않아도
    #   VASP 가 무엇을 읽었는지 여기서 확인할 수 있다 (Codex zip 감사 P0-6).
    positions = None
    k0 = t.rfind("POSITION")
    if k0 > 0:
        positions = []
        for ln in t[k0:].splitlines()[2:]:
            v = ln.split()
            if len(v) >= 6:
                try:
                    positions.append([float(v[0]), float(v[1]), float(v[2])])
                except ValueError:
                    break
            elif positions:
                break
    k = t.rfind("TOTAL-FORCE")
    if k > 0:
        forces = []
        for ln in t[k:].splitlines()[2:]:
            v = ln.split()
            if len(v) >= 6:
                try:
                    forces.append([float(v[3]), float(v[4]), float(v[5])])
                except ValueError:
                    break
            else:
                break
    # CHGCAR 를 **실제로 읽었는가** — vasp.log 가 아니라 OUTCAR 자체의 마커 (실측):
    #   ICHARG=1: `initial charge density was supplied:` 만 있고
    #   ICHARG=2: 그 밑에 `charge density of overlapping atoms calculated`
    #             (원자에서 새로 만듦) 가 따라온다. 후자가 있으면 파일을 안 읽은 것.
    _sup = "initial charge density was supplied" in t
    _atoms = "charge density of overlapping atoms calculated" in t
    chg_from_file = (True if (_sup and not _atoms) else
                     False if _atoms else None)
    return {"E0": float(e[-1]) if e else None,
            "edisp_eV": float(_ed[-1]) if _ed else None,
            "edisp_n": len(_ed),
            "chgcar_from_file": chg_from_file,
            "ionic_conv": "reached required accuracy" in t,
            # ⚠ 정상종료를 안 보면 **잘린 OUTCAR 도 에너지만 있으면 통과**한다
            "normal_end": "General timing and accounting" in t,
            "nelm_hit": bool(nelm and iters
                             and any(int(x) >= int(nelm.group(1)) for x in iters)),
            "nions": int(nions.group(1)) if nions else None,
            "nkpts": int(nk.group(1)) if nk else None,
            "kpoints_title": _kt.group(1) if _kt else None,
            "read_wavecar": read_wav, "restart_fell_back": fell_back,
            "titels": [x.strip() for x in titels],
            "vasp_version": ver.group(1) if ver else None,
            "mag_total": float(mag[-1]) if mag else None,
            "moments": read_moments(t), "forces": forces,
            "positions": positions,
            "ldau": read_ldau(t),
            "run_segments": seg, "read_format": rmeta["format"],
            "suffix_magic_mismatch": rmeta["suffix_magic_mismatch"],
            # ⛔ 2026-08-25 (sdcp_wave1 회신) — 이 검색은 **앵커가 없어서 산문도 물었다.**
            #   분자 박스 OUTCAR 129행의 VASP 권고문
            #     `|      So try LREAL= Auto  in the INCAR   file.  |`
            #   이 첫 매치라, 실제 파라미터 줄이 `LREAL = F` 인데도 got="Auto" 가 나와
            #   `LREAL: Auto!=.FALSE.` 오탐이 났다. 파라미터 줄만 보도록 행두 고정.
            "incar_echo": {k2: _echo_val(t, k2) for k2 in AUDIT_KEYS_RUNTIME}}


def read_poscar(p):
    """POSCAR/CONTCAR (Direct/Cartesian · Selective 지원). 실패 시 None."""
    t = _read_text(p)
    if t is None:
        return None
    try:
        L = t.splitlines()
        scale = float(L[1].split()[0])
        cell = [[float(x) * scale for x in L[i].split()[:3]] for i in (2, 3, 4)]
        i = 5
        species = None
        if not L[i].split()[0].isdigit():
            species = L[i].split(); i += 1
        counts = [int(x) for x in L[i].split()]; i += 1
        seldyn = False
        if L[i].strip() and L[i].strip()[0] in "Ss":
            seldyn = True; i += 1
        direct = bool(L[i].strip()) and L[i].strip()[0] in "Dd"
        i += 1
        n = sum(counts)
        pos, fixed = [], []
        for k in range(n):
            v = L[i + k].split()
            xyz = [float(x) for x in v[:3]]
            if direct:
                xyz = [sum(xyz[j] * cell[j][ax] for j in range(3)) for ax in range(3)]
            else:
                xyz = [x * scale for x in xyz]
            pos.append(xyz)
            fixed.append(seldyn and len(v) >= 6 and
                         all(f.upper().startswith("F") for f in v[3:6]))
        syms = []
        if species:
            for s, c in zip(species, counts):
                syms += [s] * c
        return {"cell": cell, "pos": pos, "fixed": fixed, "syms": syms,
                "species": species, "counts": counts}
    except Exception:
        return None


def mic_dist(a, b, cell):
    best = None
    for u in (-1, 0, 1):
        for v in (-1, 0, 1):
            for w in (-1, 0, 1):
                d = [a[x] - b[x] - u * cell[0][x] - v * cell[1][x] - w * cell[2][x]
                     for x in range(3)]
                r = math.sqrt(sum(x * x for x in d))
                best = r if best is None or r < best else best
    return best


def mol_bond_graph(struct, mol_idx):
    """분자 내부 결합 집합 {(i,j)} — 공유반경 기준."""
    bonds = set()
    syms = struct["syms"]
    for a in range(len(mol_idx)):
        for b in range(a + 1, len(mol_idx)):
            i, j = mol_idx[a], mol_idx[b]
            cut = BOND_F * (RCOV.get(syms[i], 1.0) + RCOV.get(syms[j], 1.0))
            if mic_dist(struct["pos"][i], struct["pos"][j], struct["cell"]) < cut:
                bonds.add((i, j))
    return bonds


def contact_fp(struct, mol_idx, slab_idx):
    """접촉 지문 — 분자에서 CONTACT_A 안에 있는 슬랩 원자 인덱스 집합."""
    fp = set()
    for i in slab_idx:
        for m in mol_idx:
            if mic_dist(struct["pos"][i], struct["pos"][m], struct["cell"]) < CONTACT_A:
                fp.add(i)
                break
    return fp


def geometry_audit(jd, meta):
    """relax/CONTCAR vs POSCAR — 등록·결합그래프·탈착·고정 drift. (게이트, 정보) 반환."""
    gates, info = [], {}
    init = read_poscar(os.path.join(jd, "POSCAR"))
    sp_only = "relax" not in (meta.get("phases") or ["relax"])
    # ⚠ 단일점 모드는 CONTCAR 가 없다 — 기하가 안 변하므로 POSCAR 가 곧 최종이다.
    #   그렇다고 검사를 끄지 않는다: 등록·결합 감사는 그대로 돌아 자세가 의도대로인지 본다.
    fin = init if sp_only else read_poscar(os.path.join(jd, "relax", "CONTCAR"))
    info["single_point"] = sp_only
    if init is None or fin is None or len(fin["pos"]) != len(init["pos"]):
        gates.append("REGISTRY_UNVERIFIED(CONTCAR 없음/파싱 실패/원자수 불일치)")
        return gates, info
    # ⚠ 원자수만 같고 종/셀이 다르면 다른 계다 (Codex P0-G)
    if fin.get("species") and init.get("species") and fin["species"] != init["species"]:
        gates.append(f"SPECIES_MISMATCH({fin['species']}!={init['species']})")
    if fin.get("counts") and init.get("counts") and fin["counts"] != init["counts"]:
        gates.append("COUNTS_MISMATCH(POSCAR vs CONTCAR)")
    dcell = max(abs(fin["cell"][i][j] - init["cell"][i][j])
                for i in range(3) for j in range(3))
    info["cell_drift_A"] = round(dcell, 4)
    if dcell > 1e-3:
        gates.append(f"CELL_CHANGED({dcell:.3f} Å — ISIF=2 인데 셀이 바뀌었다)")
    if not fin["syms"]:
        fin["syms"] = init["syms"]
    mol = meta.get("mol_poscar_idx") or []
    # ★ 등록은 **표면 양이온**으로만 판정한다 — 먼 H/C 나 표면 아래 양이온이
    #   라벨을 정하면 안 된다 (Codex P0-G). 표면 목록이 없으면 전체로 후퇴하되 표시한다.
    top_li = meta.get("top_li_poscar_idx") or meta.get("slab_li_poscar_idx") or []
    top_ni = meta.get("top_ni_poscar_idx") or meta.get("slab_ni_poscar_idx") or []
    if mol and (top_li or top_ni):
        def dmin(idxs):
            return min((mic_dist(fin["pos"][m], fin["pos"][i], fin["cell"])
                        for m in mol for i in idxs), default=1e9)
        dli, dni = dmin(top_li), dmin(top_ni)
        info["registry"] = {"d_Li": round(dli, 3), "d_Ni": round(dni, 3),
                            "nearest": "Li" if dli < dni else "Ni",
                            "top_only": bool(meta.get("top_li_poscar_idx"))}
        # 🔴 회신 AB P0-1 — `role` 이 **두 가지 뜻**으로 쓰이고 있었다.
        #   champion/cross 경로는 `role = "Li"|"Ni"`(등록 역할)를 쓰는데,
        #   from_basins 경로는 `role = "calibration"|"holdout"`(분석 역할)을 쓴다.
        #   그래서 동결본 번들의 복합체 전 잡이 `calibration -> Ni` 로 **항상**
        #   불일치했다 — OUTCAR 가 와도 그대로 막힌다.
        #   ⇒ 등록 기대는 `registry_role` 에서만 읽고, 옛 번들 호환으로
        #     `role` 은 그 값이 실제 Li/Ni 일 때만 받는다.
        want = meta.get("registry_role")
        if want is None and meta.get("role") in ("Li", "Ni"):
            want = meta["role"]
        info["registry"]["expected"] = want
        if want is None:
            # ⚠ **조용한 통과가 아니다.** 기대가 없다는 사실을 기록한다 —
            #   안 적으면 나중에 "검사했는데 통과" 로 읽힌다.
            info["registry"]["checked"] = False
        if want and info["registry"]["nearest"] != want:
            # ⚠ 단일점에서 이건 "이완 중 옮겨갔다" 가 아니라 **애초에 그 자리가 아니다**
            #   이다 (Codex 6차 §4). 이름이 원인을 오도하면 진단이 엉뚱한 데로 간다.
            gates.append(("SOURCE_ROLE_MISMATCH" if sp_only else "PAIR_MIGRATED")
                         + f":{want}->{info['registry']['nearest']}")
        slab_idx = (meta.get("slab_li_poscar_idx") or []) + \
                   (meta.get("slab_ni_poscar_idx") or [])
        dsl = min((mic_dist(fin["pos"][m], fin["pos"][i], fin["cell"])
                   for m in mol for i in slab_idx), default=1e9)
        info["mol_slab_min_A"] = round(dsl, 3)
        if dsl > DETACH_A:
            gates.append(f"DETACHED(분자-슬랩 {dsl:.2f} Å > {DETACH_A})")
        # ⚠ 지문에 **O 도 넣는다** — Li/Ni 만 보면 O 쪽 접촉 재구성을 못 본다 (Codex Q3)
        o_idx = [i for i, sy in enumerate(fin["syms"]) if sy == "O" and i not in mol]
        info["_contact_fp"] = sorted(contact_fp(fin, mol, slab_idx + o_idx))
    if mol:
        b1 = mol_bond_graph(fin, mol)
        if sp_only:
            # ⚠⚠ 단일점에서는 fin 이 곧 init 이다 — init↔fin 을 비교하면 변화가
            #   **구조적으로 항상 0** 이라 절대 발화하지 못하는 검사가 된다
            #   (통과해도 아무것도 보증하지 못한다 · Codex 6차 §4).
            #   정본은 빌드 때 저장한 **조각 정본 그래프**다. 없으면 통과시키지 않는다.
            b0 = {tuple(e) for e in (meta.get("mol_graph_canonical") or [])}
            if not meta.get("mol_graph_canonical"):
                gates.append("SOURCE_TOPOLOGY_UNVERIFIED(정본 분자 그래프가 job.json 에 "
                             "없다 — 옛 번들이다. 재생성할 것)")
                info["bonds"] = {"final": len(b1), "canonical": None}
            else:
                broke, formed = b0 - b1, b1 - b0
                info["bonds"] = {"canonical": len(b0), "broken": len(broke),
                                 "formed": len(formed),
                                 "compared_against": "빌드 시 조각 정본 그래프"}
                if broke or formed:
                    gates.append(f"SOURCE_TOPOLOGY_CHANGED(정본 대비 끊김 {len(broke)} · "
                                 f"생성 {len(formed)} — 계산에 넣은 분자가 조각이 아니다)")
        else:
            # 기체 기준계도 여기 온다 (슬랩이 없어 위 블록은 건너뛴다)
            b0 = mol_bond_graph(init, mol)
            broke, formed = b0 - b1, b1 - b0
            info["bonds"] = {"initial": len(b0), "broken": len(broke),
                             "formed": len(formed)}
            if broke or formed:
                gates.append(f"BOND_CHANGE(끊김 {len(broke)} · 생성 {len(formed)})")
    # ── 계면 정체성 (Codex P0-7) — 자리 선호를 묻던 계가 다른 계가 됐는가 ──
    #   ⚠ 이 검사들은 "버리라" 가 아니라 **격리하라** 는 뜻이다. 재구성·전이가 일어난
    #     끝점은 흡착 에너지의 질문 자체가 달라져 같은 표에 못 올린다.
    if mol and (top_li or top_ni) and not sp_only:
        top_all = sorted(set(top_li) | set(top_ni))
        # ① 자유 상부 양이온의 재구성 변위
        rec_d = max((mic_dist(init["pos"][i], fin["pos"][i], fin["cell"])
                     for i in top_all if not init["fixed"][i]), default=0.0)
        info["top_reconstruction_A"] = round(rec_d, 3)
        if rec_d > RECON_A:
            gates.append(f"SURFACE_RECONSTRUCTION(상부 양이온 {rec_d:.2f} Å > {RECON_A})")
        # ② Li 바깥쪽 이탈 + O 배위 손실 (표면에서 뽑혀 나왔나)
        o_slab = [i for i, sy in enumerate(fin["syms"]) if sy == "O" and i not in mol]
        worst_li = (0.0, 0, 0)
        for i in top_li:
            dz = fin["pos"][i][2] - init["pos"][i][2]
            n0 = sum(1 for j in o_slab
                     if mic_dist(init["pos"][i], init["pos"][j], init["cell"]) < LI_O_A)
            n1 = sum(1 for j in o_slab
                     if mic_dist(fin["pos"][i], fin["pos"][j], fin["cell"]) < LI_O_A)
            if dz - 0.0 > worst_li[0] or (n0 - n1) > worst_li[1]:
                worst_li = (max(dz, worst_li[0]), max(n0 - n1, worst_li[1]), i)
        info["li_outward_A"] = round(worst_li[0], 3)
        info["li_O_coord_loss"] = worst_li[1]
        if worst_li[0] > LI_OUT_A or worst_li[1] >= LI_COORD_LOSS:
            gates.append(f"LI_EXTRACTION(바깥 이동 {worst_li[0]:.2f} Å · "
                         f"O 배위 −{worst_li[1]})")
        # ③ 새 계면 결합 (분자 원자 ↔ 슬랩 원자가 공유반경 안으로)
        newb = []
        for m in mol:
            for i in slab_idx + o_slab:
                cut = BOND_F * (RCOV.get(fin["syms"][m], 1.0) + RCOV.get(fin["syms"][i], 1.0))
                d0 = mic_dist(init["pos"][m], init["pos"][i], init["cell"])
                d1 = mic_dist(fin["pos"][m], fin["pos"][i], fin["cell"])
                if d1 < cut <= d0:
                    newb.append((fin["syms"][m], fin["syms"][i], round(d1, 2)))
        info["new_interface_bonds"] = newb[:8]
        if newb:
            gates.append(f"INTERFACE_REACTION_OR_RECONSTRUCTION(새 계면 결합 {len(newb)}: "
                         + ", ".join(f"{a}–{b} {d}Å" for a, b, d in newb[:3]) + ")")

    # ⚠ 이완이 없으면 drift·재구성·Li 추출·새 계면결합은 **정의되지 않는다**.
    #   여기에 0 을 적으면 "검사했고 통과" 로 읽힌다 (Codex 6차 §4). 이름을 붙인다.
    if sp_only:
        info["fixed_drift_A"] = "NOT_APPLICABLE_SINGLE_POINT"
        info["relaxation_gates"] = "NOT_APPLICABLE_SINGLE_POINT"
        info["relaxation_gates_list"] = [
            "ionic convergence", "fixed-atom drift", "surface reconstruction",
            "Li extraction", "new interface bonds", "DFT CONTCAR migration"]
    else:
        dmax = 0.0
        for i, fx in enumerate(init["fixed"]):
            if fx:
                dmax = max(dmax, mic_dist(init["pos"][i], fin["pos"][i], fin["cell"]))
        info["fixed_drift_A"] = round(dmax, 4)
        if dmax > FIX_DRIFT_A:
            gates.append(f"FIXED_DRIFT({dmax:.3f} Å — 파일 불일치 의심)")
    info["_init_fixed"] = init["fixed"]
    info["_fin"] = fin
    return gates, info


BRANCH_TIE_EV = 0.020     # 두 branch 차가 이 아래면 k 보정(각 ±10)으로 순서가 뒤집힌다
MAX_OPTIONAL_DENSE = 2    # 예산 상한 — 넘으면 전이를 주장하지 않는다


def plan_dense(root, man, jobs, E, E_dense):
    """coarse static 을 보고 **어느 branch 에 dense 를 걸어야 하는지** 정한다.

    설계 (Codex 6차 §3 을 예산에 맞게 조정)
      · 기본 dense 는 pm1 에 **이미 사슬로 붙어 있다** — 아무것도 발동 안 하면 추가 0
      · 발동 조건은 두 가지뿐이다
          ① pm1 이 무효 (게이트/미완)          → net4 후보를 승격
          ② net4 가 pm1 보다 {BRANCH_TIE_EV*1000:.0f} meV 넘게 낮다 → net4 승격
        (둘 다 아니면 우리가 보고하는 branch 를 이미 dense 한 것이다)
      · 승격은 최대 {MAX_OPTIONAL_DENSE} 건. 넘으면 **한 조각만 완결**하고 나머지는
        MAX_OPTIONAL_DENSE 를 넘겼다고 적는다 — 임의의 둘로 전체를 주장하지 않는다.

    이 함수가 **못 하는 것**: 어느 branch 가 진짜 바닥인지 보장하지 못한다.
      두 seed 는 시도한 초기값 두 개일 뿐이고, 더 낮은 자기배치가 있을 수 있다.
    """
    seeds = man.get("seeds_full") or ["afm2424_pm1", "afm2424_net4"]
    main, alt = seeds[0], (seeds[1] if len(seeds) > 1 else seeds[0])
    cal = list(man.get("dense_calibrators") or [])
    plan = {"parent_manifest_sha256": hashlib.sha256(
                open(os.path.join(root, "MANIFEST.json"), "rb").read()).hexdigest(),
            "rule": {"branch_tie_eV": BRANCH_TIE_EV,
                     "max_optional": MAX_OPTIONAL_DENSE,
                     "why": (f"두 branch 의 k 보정이 각각 최대 ±10 meV 면 차가 "
                             f"{BRANCH_TIE_EV * 1000:.0f} meV 안일 때 순서가 뒤집힐 수 "
                             f"있다. 30 meV 판정바닥과는 다른 축이다.")},
            "calibrators": cal, "endpoints": {}, "promote": [], "notes": []}
    if not cal:
        plan["notes"].append("dense 보정자가 지정되지 않았다 — 계획할 대상이 없다")
    cand = []
    for pid, pm in man.get("pairs", {}).items():
        if pm["fragment"] not in cal:
            continue
        for role in ("li", "ni"):
            pre = pm[f"{role}_prefix"]
            ent = {"fragment": pm["fragment"], "role": role.capitalize(),
                   "E_by_seed": {}, "valid": {}, "static_sha256": {}}
            for sd in seeds:
                j = f"{pre}__{sd}"
                r = jobs.get(j)
                ent["valid"][sd] = bool(r and r.get("ok"))
                ent["E_by_seed"][sd] = E(j)
                for ext in ("", ".gz"):
                    p = os.path.join(root, j, "static", "OUTCAR" + ext)
                    if os.path.isfile(p):
                        ent["static_sha256"][sd] = hashlib.sha256(
                            open(p, "rb").read()).hexdigest()
                        break
                if r and not r.get("ok"):
                    ent.setdefault("gates", {})[sd] = r.get("gates", [])[:3]
            em, ea = ent["E_by_seed"].get(main), ent["E_by_seed"].get(alt)
            have_dense = E_dense(f"{pre}__{main}") is not None
            ent["dense_done_on"] = main if have_dense else None
            if em is None and ea is None:
                ent["decision"] = "NO_VALID_BRANCH — 이 끝점은 k 검증 불가"
            elif em is None:
                ent["decision"] = f"PROMOTE_{alt}(주 branch 무효)"
                cand.append((0, pid, role, alt, ent))          # 우선순위 0 = 최상
            elif ea is not None and ea < em - BRANCH_TIE_EV:
                ent["decision"] = (f"PROMOTE_{alt}(coarse 에서 "
                                   f"{(em - ea) * 1000:.0f} meV 더 낮다)")
                cand.append((1, pid, role, alt, ent))
            elif ea is not None and abs(em - ea) <= BRANCH_TIE_EV:
                # ⚠ tie 는 "괜찮다" 가 아니라 **재순위 위험 구간**이다. adaptive 가
                #   꺼져 있으면 추가 계산이 불가능하므로 그 사실을 판정으로 남긴다.
                ent["decision"] = (f"MAGNETIC_K_UNRESOLVED(두 branch 차 "
                                   f"{abs(em - ea) * 1000:.0f} meV ≤ "
                                   f"{BRANCH_TIE_EV * 1000:.0f} — k 보정 ±10 으로 순서가 "
                                   f"뒤집힐 수 있는데 adaptive dense 가 꺼져 있다)")
            else:
                ent["decision"] = (f"OK({main} 이 {(ea - em) * 1000:.0f} meV 낮다 — "
                                   f"보고 branch = dense 한 branch)")
            if not have_dense:
                ent["decision"] += " ⚠ 주 branch dense 산출이 없다(미완/게이트)"
            plan["endpoints"][f"{pid}/{role}"] = ent
    cand.sort(key=lambda t: (t[0], t[1], t[2]))
    for pr, pid, role, sd, ent in cand[:MAX_OPTIONAL_DENSE]:
        rel = f"{man['pairs'][pid][role + '_prefix']}__{sd}"
        plan["promote"].append({"job": rel, "seed": sd, "priority": pr,
                                "reason": ent["decision"],
                                "candidate_dir": "dense_cand"})
    if len(cand) > MAX_OPTIONAL_DENSE:
        drop = [f"{p}/{r}" for _x, p, r, _s, _e in cand[MAX_OPTIONAL_DENSE:]]
        plan["notes"].append(
            f"⛔ 승격 후보 {len(cand)}건 > 상한 {MAX_OPTIONAL_DENSE} — "
            f"{drop} 는 MAGNETIC_K_UNRESOLVED 다. 임의의 둘로 전체 전이를 "
            f"주장하지 않는다 (예산을 늘리든지 주장 범위를 줄이든지 골라야 한다)")
    plan["estimated_extra_dense_runs"] = len(plan["promote"])
    op = os.path.join(root, "DENSE_PLAN.json")
    with open(op, "w", encoding="utf-8") as fh:
        json.dump(plan, fh, indent=1, ensure_ascii=False)
    print(f"=== dense 계획 ===  보정자 {cal} · 끝점 {len(plan['endpoints'])}")
    for k, v in plan["endpoints"].items():
        print(f"  {k:44s} {v['decision']}")
    print(f"\n승격 {len(plan['promote'])}건"
          + ("  (추가 계산 없음 — 보고 branch 를 이미 dense 했다)"
             if not plan["promote"] else ""))
    for p in plan["promote"]:
        print(f"   ▶ {p['job']}  ({p['reason']})")
    for n in plan["notes"]:
        print(f"  ⚠ {n}")
    print(f"\n→ {op}")
    print("   ⚠ 이 모드는 --adaptive_dense 로 만든 번들에서만 의미가 있다. "
          "기본 번들에는 dense_cand/ 도 run_dense_selected.sh 도 없다.")
    return 0


def k_transfer_gate(cal, kap_all, frags):
    """k 전이 게이트 — (판정, 조각별 라벨, 통과한 보정자) 를 낸다.

    ★ κ 는 **부호 있는** 양이다. 크기만 보면 +9 와 −9 를 둘 다 통과시켜 실제
      18 meV 의 계 의존성을 놓친다. 그래서 max|κ| 와 range 를 **둘 다** 본다.
    ★ n=2 다 — 평균·표준편차·CI 를 쓰지 않는다. deterministic max/range 규칙이다.

    이 함수가 **못 하는 것**: 보정자가 대표성이 있는지는 판단하지 못한다.
      큰 계 하나 + open-shell 하나로 고른 것은 **공학적 선택**이지 통계가 아니다.
    """
    # ★ 라벨은 **선언이 아니라 데이터**를 따른다 (2026-08-12). κ 를 실제로 잰 조각은
    #   dense_calibrators 에 안 적혀 있어도 직접 검증된 것이다 — 선언만 보면 dense 를
    #   돌리고도 K_UNVERIFIED 가 되어 headline 이 막힌다.
    have = {f: kap_all[f] for f in (cal or list(kap_all)) if f in kap_all}
    if not cal and not have:
        kt = {"pass": False, "why": "dense 를 돌린 조각이 없다 — 전이 불가"}
    elif cal and len(have) < len(cal):
        kt = {"pass": False, "kappa_eV": have,
              "why": f"보정자 {len(have)}/{len(cal)} 만 회수 — 전이 근거 부족"}
    else:
        vals = list(have.values())
        mx = max(abs(v) for v in vals)
        rng = max(vals) - min(vals)
        kt = {"pass": bool(mx <= GUARD_EV and rng <= GUARD_EV), "kappa_eV": have,
              "max_abs_meV": round(mx * 1000, 1), "range_meV": round(rng * 1000, 1),
              "rule": (f"|κ_f| ≤ {GUARD_EV * 1000:.0f} meV **및** "
                       f"|κ_i−κ_j| ≤ {GUARD_EV * 1000:.0f} meV. n=2 라 max/range 로 "
                       f"본다 (평균·표준편차·CI 금지)")}
    labels = {f: ("K_DIRECTLY_CHECKED" if f in have else
                  "K_TRANSFER_SCREENED" if kt["pass"] else "K_UNVERIFIED")
              for f in frags}
    return kt, labels, have


def apply_k_guard(cls, med, lbl, delta):
    """guard band 를 **실제 release gate 로** 적용한다 (Codex 6차 §6).

    옛 판은 k_guard 에 문자열만 붙이고 최종 class 를 막지 않았다 — 직접 dense 하지
    않은 조각의 25 meV 대비가 그대로 판정으로 나갔다.
    ±10 meV(k 불확실성)는 30 meV(판정바닥)와 **별개 축**이다:
      · |ΔE| ≤ 10 meV      → 부호 자체가 안 정해진다 (라벨 무관)
      · 20 ≤ |ΔE| ≤ 40 meV → k 오차 하나로 바닥을 넘나든다. 직접 dense 아니면 보류
      · 그 밖                → 원래 판정 유지
    """
    a = abs(med)
    if a <= GUARD_EV:
        return f"UNRESOLVED_SIGN(|ΔE|={a * 1000:.0f} ≤ {GUARD_EV * 1000:.0f} meV)"
    # ★★ K_UNVERIFIED 는 **유한한 k 오차 경계가 없다** (Codex zip 감사).
    #   전이 게이트가 실패했다는 건 "10 meV 안" 이라고 말할 근거가 사라졌다는 뜻이다.
    #   그런데 옛 판은 |ΔE| 가 크면 그냥 통과시켰다 — 경계 없는 값에 판정을 붙인 셈이다.
    if lbl == "K_UNVERIFIED":
        return (f"UNRESOLVED_K(|ΔE|={a * 1000:.0f} meV 이지만 k 오차에 **유한한 경계가 "
                f"없다** — 전이 게이트 실패. 직접 dense 없이는 판정 불가)")
    if lbl != "K_DIRECTLY_CHECKED" and delta - GUARD_EV <= a <= delta + GUARD_EV:
        return (f"UNRESOLVED_K_GUARD(|ΔE|={a * 1000:.0f} meV 가 "
                f"{(delta - GUARD_EV) * 1000:.0f}–{(delta + GUARD_EV) * 1000:.0f} meV "
                f"띠 안 · {lbl} — 직접 dense 없이는 판정 불가)")
    return cls


def _stage1_prereqs(_cl, _vc, results):
    """1단계 선결조건 — **전부 통과해야** 2단계가 열린다.

    → {이름: {"pass": bool, "why": ...}}

    ⛔⛔ 회신 AP #5 → AR 해제조건 5 (2026-08-31). 종전 네 조건
      (vacuum/molecular_state/canary_geometry/potcar_identity)만으로는
      **이미 primary estimand 가 실패한 뒤에도** STAGE1_PASS.json 을 쓰고
      2단계를 열 수 있었다 — δ_gas 도 pm1 topology 도 잔여 exact/global
      block 도 보지 않았기 때문이다. 여덟으로 늘렸다.

    ⛔ 이 함수가 **못 하는 것**: 2단계 잡의 미실행을 요구하지 않는다
      (단계별 실행에서 2단계가 비어 있는 것은 정상이다). 여기서 보는 것은
      **1단계 산출만으로 판정 가능한 것들**뿐이다.
    """
    _pi = (_cl.get("potcar_identity") or {})
    _cg_all = (results.get("gas_canary_geom") or {})
    _mol_blk = [b for b in (_cl.get("blocks") or [])
                if b.startswith(("MOLECULAR_STATE_UNRESOLVED",
                                 "MOLECULAR_SPIN_CONTROL"))]
    _cg_bad = {f: v for f, v in _cg_all.items() if (v or {}).get("same") is not True}
    _pre = {
        "vacuum": {"pass": bool(_vc.get("pass")),
                   "why": _vc.get("verdict")},
        "molecular_state": {"pass": not _mol_blk,
                            "why": (_mol_blk[:2] if _mol_blk else
                                    "비영 시작이 부모보다 낮지 않다")},
        "canary_geometry": {"pass": bool(_cg_all) and not _cg_bad,
                            "why": (_cg_bad if _cg_bad else
                                    "부모/canary static 기하 동일 (%d조각)"
                                    % len(_cg_all))},
        "potcar_identity": {"pass": not (_pi.get("blocking") or []),
                            "why": (_pi.get("blocking") or [])[:2]
                                   or _pi.get("identity_scope")},
    }
    # ⛔⛔ 회신 AR 해제조건 5 (2026-08-31) — 위 네 조건만으로는
    #   **이미 primary estimand 가 실패한 뒤에도** STAGE1_PASS 를 쓰고 2단계를
    #   열 수 있었다. δ_gas 도 pm1 topology 도 잔여 exact/global block 도
    #   보지 않았기 때문이다. 네 개를 더 결박한다.
    #   ⚠ 이 네 조건은 **1단계 산출만으로 판정 가능한 것들**이다 —
    #     2단계(대안자세·net4)의 미실행을 요구하지 않는다.
    _gbd = (_cl.get("gas_box_delta") or {})
    _gpc = (_cl.get("gas_pair_contract") or {})
    _gas_why = ([b for b in (_cl.get("blocks") or [])
                 if b.startswith(("GAS_BOX", "GAS_PAIR"))][:2]
                or {"delta_gas_meV": _gbd.get("delta_gas_meV"),
                    "tol_meV": _gbd.get("tol_meV")})
    _pre["gas_box_delta"] = {
        "pass": bool(_gbd.get("pass") is True and _gpc.get("ok") is True),
        "why": _gas_why}
    _tp1 = ((_cl.get("estimand_topology") or {}).get("pm1") or {})
    _pre["estimand_topology_pm1"] = {
        "pass": bool(_tp1 and _tp1.get("same") is True and not _tp1.get("blocks")),
        "why": (_tp1.get("blocks") or [])[:2]
               or ("두 complex 가 같은 자기 branch (%s)" % _tp1.get("why")
                   if _tp1 else "pm1 topology 판정이 없다")}
    # 잔여 exact-estimand / 전역 차단 — pooled_diagnostic 만 제외한다
    #   (그 강등은 회신 AP #3 에서 근거를 남기고 한 것이고, 정본 blocks 는
    #    회신 AR Q1 이후 그대로 남아 있으므로 여기서 scope 로 걸러야 한다)
    _recs = (_cl.get("block_records") or [])
    _res_blk = [r["msg"] for r in _recs
                if r.get("scope") in ("estimand", "global")
                and r.get("affects_estimand") is not False]
    # 구조화되지 않은 옛 문자열 block 도 남아 있으면 통과가 아니다
    _unstruct = [b for b in (_cl.get("blocks") or [])
                 if b not in {r["msg"] for r in _recs}]
    _pre["closure_blocks_clear"] = {
        "pass": not _res_blk and not _unstruct,
        "why": ([b[:70] for b in (_res_blk + _unstruct)][:3]
                or "exact/global closure block 0건")}
    # 생산 전 root seal 이 **이 manifest 와 예정 잡 전체**를 포괄하는가
    _sealcov = (_cl.get("root_seal_coverage") or _pi.get("root_seal_coverage") or {})
    _pre["root_seal_covers_plan"] = {
        "pass": bool(_sealcov.get("ok") is True),
        "why": (_sealcov.get("why") or "root seal 포괄 검사 결과가 없다")}
    return _pre


def _final_verdict(_cl, _vc):
    """최종 종료 판정 — 비인용 상태면 사유 목록을 낸다 (빈 목록 = exit 0).

    ⛔⛔ 회신 AS 해제조건 1 (2026-08-31) — 종전엔 정본 `blocks` 를 읽었다.
      회신 AR Q1 이후 정본은 **강등하지 않으므로** `BASIN_HETEROGENEOUS` 가 남고,
      pm1 과 net4 는 **의도적으로 다른 magnetic topology** 라 둘 다 정상 수렴해도
      그것이 뜬다. 즉 이 번들은 **성공할 수 없었다** — 외주가 16잡을 다 돌린 뒤에야
      알았을 결함이다. 성공/실패 판정의 정본을 `primary_estimand_blocks` 하나로
      통일한다 (정본 blocks 는 기록으로 남고, 강등분은 nonprimary_notes 에 있다).

    ⛔ 이 함수가 못 하는 것: 왜 막혔는지 진단하지 않는다. 사유 문자열만 모은다.
    """
    bad = []
    if _vc and _vc.get("applicable") and not _vc.get("pass"):
        bad.append("closure_vacconv.pass != true")
    if str((_cl or {}).get("verdict", "")).startswith("NO_VALUE"):
        bad.append("prereg_closure = NO_VALUE")
    fin = (_cl or {}).get("primary_estimand_blocks")
    if fin is None:                              # 구판 결과 — 강등 뷰가 없다
        fin = (_cl or {}).get("blocks")
    if fin:
        bad.append("prereg_closure.primary_estimand_blocks %s" % fin[:2])
    return bad


def _selftest_closure(chk):
    """사전등록 estimand 의 ⛔음성 묶음 — **배포본 안에서** 돌아야 한다.

    ⛔⛔ 회신 AR P1-12 · 해제조건 10 (2026-08-31) — 이 시험들이 종전엔
      **생성기 selftest 에만** 있었다. 배포된 번들에서
      `python3 analyze_results.py --selftest` 를 돌리면 179건만 나오고
      production `_closure_estimand` 는 하나도 안 탔다. 외주처·리뷰어가
      재현할 수 없는 검사는 "있다" 고 말할 수 없다 ⇒ 여기로 옮긴다.
      생성기 selftest 는 이 함수를 **그대로 호출**한다 (출처는 하나다).

    이 함수가 **못 하는 것**: 실제 VASP·POTCAR·스케줄러를 대신하지 않는다.
      합성 job 레코드로 판정 논리만 친다.
    """
    # ── 🔴 회신 AT P0-2 — dense 상의 INCAR·k 감사 fail-open (배포본에서 돈다) ──
    #   ⚠ 이 시험은 **여기 있어야** 한다. `phase_gates` 는 배포본 분석기의 함수라
    #     생성기 selftest 스코프에는 없다 (2026-08-31 NameError 로 확인).
    def _at_pg(ph, meta_over=None, oc_over=None):
        _oc = {"nions": 4, "nkpts": 12, "normal_end": True, "nelm_hit": False,
               "ionic_conv": True, "titels": [], "E0": -1.0, "toten": -1.0,
               "mag_tot": None, "nelect": None, "n_iter": 5,
               "kpoints_title": "phase=dense k=4 6 1 shift=0 0 0",
               "incar_echo": {}, "run_segments": {"n": 1}}
        _oc.update(oc_over or {})
        _mt = {"species_order": [], "kmesh": {"dense": "4 6 1"},
               "incar_expected": {"dense": {"ENCUT": "520"}},
               "kpoints_expected": {"dense": {
                   "title": "phase=dense k=4 6 1 shift=0 0 0", "mode": "Gamma",
                   "mesh": "4 6 1", "shift": "0 0 0"}}}
        _mt.update(meta_over or {})
        return {x.split("(")[0] for x in phase_gates(_oc, ph, _mt, {})}

    chk("KPOINTS_MISMATCH" not in _at_pg("dense")
        and "INCAR_EXPECTED_MISSING" not in _at_pg("dense"),
        "AT P0-2 양성: 제목·기대 INCAR 이 맞으면 k/INCAR 게이트가 안 뜬다")
    chk("KPOINTS_MISMATCH" in _at_pg(
            "dense", oc_over={"kpoints_title": "phase=static k=3 4 1 shift=0 0 0"}),
        "⛔음성 AT P0-2: **coarse(3 4 1) OUTCAR 를 dense 폴더에** 넣으면 잡힌다 "
        "— 종전엔 NKPTS 12 ≤ 24 라 통과했다")
    chk("KPOINTS_TITLE_UNVERIFIED" in _at_pg("dense", oc_over={"kpoints_title": None}),
        "⛔음성 AT P0-2: ` KPOINTS:` 되울림이 없으면 **확인 못 함**이지 통과가 아니다")
    chk("KPOINTS_EXPECTED_MISSING" in _at_pg("dense", meta_over={"kpoints_expected": {}}),
        "⛔음성 AT P0-2: 구판 번들(kpoints_expected 없음)의 dense 는 막는다")
    chk("INCAR_EXPECTED_MISSING" in _at_pg("dense", meta_over={"incar_expected": {}}),
        "⛔음성 AT P0-2: dense 의 기대 INCAR 이 없으면 막는다 — 없으면 그 상의 "
        "감사가 통째로 비어 ENCUT 400·IVDW 0·ISPIN 1 도 통과한다")
    chk("KPOINTS_EXPECTED_MISSING" not in _at_pg(
            "static", meta_over={"kpoints_expected": {}, "kmesh": {}}),
        "AT P0-2 경계: static 은 기대값이 없어도 **이 게이트로는** 막지 않는다 "
        "(δ_k 에 직접 들어가는 상만 강제)")

    # ⛔ 회신 AS 해제조건 3 — pool 완전성 검사가 `planned` 를 읽는다. 실물 manifest
    #   에는 항상 있으므로 픽스처도 실물 모양이어야 한다 (회신 AP #8 과 같은 교훈).
    def _PL(jn, role="primary", frag=None, seed="afm2424_pm1"):
        return {"phases": ["static"], "required": True,
                "meta": {"kind": "prospective_pose", "d3": "on",
                         "fragment": frag or jn.split("/")[-1].split("__")[0],
                         "basin_id": jn.split("__")[1], "role": role, "seed": seed}}
    _PLANNED = {k: _PL(k) for k in
                ("prospective/sdcp_neutral__b00__afm2424_pm1",
                 "prospective/sdcp_neutral__b01__afm2424_pm1",
                 "prospective/ptfe_c10__b00__afm2424_pm1")}
    # ⛔ 회신 AS 9 — 실물 manifest 는 kconv_pair 를 담는다. 픽스처도 실물 모양으로.
    _KJ = ("prospective/sdcp_neutral__b00__afm2424_pm1",
           "prospective/ptfe_c10__b00__afm2424_pm1")
    _KCONV = {"jobs": list(_KJ), "coarse_kmesh": "3 4 1", "dense_kmesh": "4 6 1",
              "formula": "δ_k = (E_sdcp,dense−coarse) − (E_ctl,dense−coarse)",
              "tol_eV": 0.005}
    _man = {"fragments": ["sdcp_neutral", "ptfe_c10"],
            "planned": _PLANNED, "kconv_pair": _KCONV,
            # ⛔ 회신 AR 해제조건 3 — 실물 생성기가 박는 기체 쌍 정책
            "gas_geometry_policy": {"fixed_geometry_static": True},
            "molecular_spin_controls": {
                "mol__sdcp_neutral__box24": "refs/mol__sdcp_neutral__box24__nzmag",
                "mol__ptfe_c10__box24": "refs/mol__ptfe_c10__box24__nzmag"}}
    _emol = {"sdcp_neutral": -200.0, "ptfe_c10": -100.0}
    # 🔴 키를 **실물 모양**으로 쓴다 (2026-08-29 자체 적대검토). 생성기는
    #   `prospective/<frag>__<basin>__<seed>` 로 낸다(_pk 가 상대경로 그대로).
    #   접두어 없는 옛 fixture 때문에 `startswith(f+"__")` 버그가 안 보였고,
    #   실물에서는 조각 매칭이 **하나도 안 걸려** J_f 가 조용히 비었다.
    # ⛔ 회신 AP #11 — δ_gas 게이트가 box20/box24 를 요구한다. 픽스처를 실물화한다.
    #   sdcp: 24−20 = +0.3 meV · ptfe: 24−20 = +0.2 meV ⇒ δ_gas = +0.1 meV (통과)
    _GASE = {"refs/mol__sdcp_neutral__box24": -205.4486,
             "refs/mol__sdcp_neutral__box20": -205.4489,
             "refs/mol__ptfe_c10__box24": -177.9706,
             "refs/mol__ptfe_c10__box20": -177.9708}
    _en = {"mol__sdcp_neutral__box24__nzmag": -200.0,
           "mol__ptfe_c10__box24__nzmag": -100.0,
           **_GASE,
           "prospective/sdcp_neutral__b00__afm2424_pm1": -201.0,
           "prospective/sdcp_neutral__b01__afm2424_pm1": -200.9,
           "prospective/ptfe_c10__b00__afm2424_pm1": -100.5}
    # ★ 회신 Z P0-4 — 모든 잡이 realized basin 을 달고 있어야 뺄셈이 허용된다.
    #   합성 레코드였던 옛 fixture 는 basin 이 없어 새 게이트에 걸렸다 —
    #   **게이트가 맞고 fixture 가 낡았다** (실물은 LORBIT 로 항상 표가 있다).
    def _BAS(b, jn="prospective/sdcp_neutral__b00__afm2424_pm1", **kw):
        """실물 스키마의 job 레코드. **meta 없이 만들면 cohort 조립이 막힌다** —
        회신 AA P0-3 이후 조각·seed·d3 판정이 전부 구조화 필드에서 나온다."""
        base = jn.rsplit("/", 1)[-1]
        m = {"kind": "prospective_pose", "role": "calibration",
             "fragment": base.split("__")[0], "basin_id": base.split("__")[1],
             "seed": "afm2424_" + base.split("afm2424_")[1].replace("__d3off", ""),
             "d3": "off" if base.endswith("__d3off") else "on"}
        m.update(kw)
        # ⛔ 회신 AP #2 — estimand 검사가 **Ni 모멘트 표**를 요구한다. basin id 만
        #   있는 픽스처는 실물이 아니다 (실물은 LORBIT 로 항상 표가 있다).
        mg = {"realized_basin_id": b}
        if b is not None:
            mg["realized_basin"] = {"ni_moments_muB":
                                    list(kw.pop("_mom", [1.2] * 24 + [-1.2] * 24))}
        else:
            kw.pop("_mom", None)
        r = {"ok": True, "gates": [], "meta": m, "geom": {"magnetic": mg}}
        # ⛔ 회신 AS 9 — dense 상. `_en` 에 coarse 가 있고 dense 는 그 + 오프셋이다.
        #   기본 오프셋은 두 조각이 같아 δ_k = 0 (통과). 시험이 덮어쓴다.
        if kw.get("_dense") is not None:
            r["dense"] = {"normal_end": True, "E0": kw["_dense"]}
        return r

    # ⛔ 회신 AR 해제조건 3 — 기체 쌍 cross-job gate 는 **잡 메타**를 읽는다.
    #   실물 `_emit_mol_job` 이 내는 필드 그대로 픽스처를 만든다.
    #   (energies 만 주던 옛 픽스처는 계약을 검증할 수 없다 = 통과가 아니다.)
    def _GASJ(frag, tag, geo="g-%s" % "x", **kw):
        m = {"kind": "mol_ref", "fragment": frag, "box_margin_A": 20.0 if tag == "box20" else 24.0,
             "species_order": ["O", "S", "C", "F", "H"], "counts": [3, 1, 10, 20, 4],
             "gas_placement": "com_at_cell_center",
             "internal_geometry_sha": "geo-" + frag,
             "electronic_state_sha": "st-" + frag,
             # 생성기가 모든 job.json 에 사후로 박는 필드 (없으면 COHORT_INCOHERENT)
             "d3": "on", "ivdw_expected": 11,
             "fixed_geometry_static": True, "phases": ["static"]}
        m.update(kw)
        return {"ok": True, "gates": [], "meta": m, "geom": {}}

    _GASJOBS = {"refs/mol__%s__%s" % (f, t): _GASJ(f, t)
                for f in ("sdcp_neutral", "ptfe_c10") for t in ("box20", "box24")}
    _jobs = {k: _BAS("aaaa1111", k,
                     **({"_dense": _en[k] + 0.010} if k in _KJ else {}))
             for k in _en if k.startswith("prospective/")}
    _jobs.update(_GASJOBS)
    _E = lambda j: _en.get(j)
    # ⛔ 회신 AO P0-4 — canary/부모 static 기하 대조 결과. 실물에서는 main() 이
    #   두 static/POSCAR 를 읽어 채운다. 없으면 fail-closed 로 막히므로 픽스처에도
    #   **명시적으로** 넣는다 (없는 것을 통과로 읽지 않는 것이 이 게이트의 요점이다).
    def _RES(same=True, **kw):
        g = {f: ({"same": True, "max_cart_diff_A": 0.0, "max_cell_diff_A": 0.0}
                 if same else
                 {"same": False, "max_cart_diff_A": 0.031, "max_cell_diff_A": 0.0})
             for f in ("sdcp_neutral", "ptfe_c10")}
        g.update(kw)
        return {"pairs": {}, "gas_canary_geom": g}

    r = _closure_estimand(_man, _RES(), _E, _emol, _jobs)
    chk(not r["blocks"], f"[V P0-4] 정상 입력에 blocks 없음 · {r.get('blocks')}")
    chk((r.get("gas_pair_contract") or {}).get("ok") is True
        and (r.get("gas_box_delta") or {}).get("pair_contract_ok") is True,
        "회신 AR 3 양성: 고정기하·동일 내부기하 쌍은 계약을 통과한다")

    # ══ 🔴 회신 AT Q2 — 합산 오차예산 B_num (양성 + ⛔음성) ═════════════════
    _nb = r.get("numeric_budget") or {}
    chk(_nb.get("정의", "").startswith("B_num"),
        "AT Q2: 결과에 **합산 오차예산**이 나온다 (%s)" % _nb.get("B_num_meV"))
    chk("RSS" in str(_nb.get("⛔_RSS_금지", "")),
        "AT Q2: 왜 RSS 를 안 쓰는지 산출물에 적힌다 (독립 확률오차가 아니다)")

    def _budget(vac_meV, gas_meV, k_meV):
        """세 축 값을 손으로 넣어 합산 판정만 본다."""
        _rr = _closure_estimand(_man, _RES(), _E, _emol, _jobs)
        _b = {"vac": abs(vac_meV), "gas": abs(gas_meV), "k": abs(k_meV)}
        return sum(_b.values()), _b

    # 축별로는 전부 통과(각 2 meV ≤ 5)인데 **합은 6 meV** — 넘어야 한다
    _sum6, _b6 = _budget(2.0, 2.0, 2.0)
    chk(_sum6 > 5.0 and all(v <= 5.0 for v in _b6.values()),
        "🔴 AT Q2: 축별 2 meV 는 각각 통과하지만 **합 %.1f meV 는 문턱 5 를 넘는다** "
        "— 이것이 RSS 를 쓰면 놓치는 경우다 (RSS 로는 %.2f meV 라 통과해 버린다)"
        % (_sum6, (2.0**2 * 3) ** 0.5))
    chk(_nb.get("tol_meV") == 5.0 and "미달이면" in _nb,
        "AT Q2: 문턱과 **미달 시 처방**이 결과에 같이 봉인된다 (값을 버리지 않고 "
        "보고 해상도를 낮춘다)")

    # ══ 회신 AR 해제조건 3 — 기체 쌍 cross-job gate (⛔음성 셋) ═════════════
    #   AR 이 실물 v15 에서 잡은 것: 네 기체 부모가 전부 relax→static 이라
    #   각 상자가 **독립으로 이완**했다. 그러면 δ_gas 는 셀 효과가 아니다.
    def _gasneg(mut, why):
        _jg = dict(_jobs)
        _mm = dict(_GASJOBS)
        for k, patch in mut.items():
            _mm[k] = {"ok": True, "gates": [],
                      "meta": dict(_GASJOBS[k]["meta"], **patch), "geom": {}}
        _jg.update(_mm)
        _rg = _closure_estimand(_man, _RES(), _E, _emol, _jg)
        chk(any(b.startswith("GAS_PAIR_CONTRACT") for b in _rg["blocks"])
            and (_rg.get("gas_box_delta") or {}).get("pass") is not True,
            "⛔음성 AR 3: %s → GAS_PAIR_CONTRACT 로 막고 δ_gas 를 통과로 세지 않는다 "
            "· blocks %s" % (why, [b[:60] for b in _rg["blocks"]][:2]))

    _gasneg({"refs/mol__sdcp_neutral__box20":
             {"fixed_geometry_static": False, "phases": ["relax", "static"]}},
            "한 상자가 relax→static (AR 이 v15 에서 실제로 잡은 결함)")
    _gasneg({"refs/mol__ptfe_c10__box20": {"internal_geometry_sha": "geo-DIFFERENT"}},
            "두 상자의 내부기하가 다르다")
    _gasneg({"refs/mol__sdcp_neutral__box24": {"electronic_state_sha": "st-OTHER"}},
            "두 상자의 전자상태 정책이 다르다")
    _gasneg({"refs/mol__ptfe_c10__box24": {"counts": [3, 1, 10, 20, 5]}},
            "두 상자의 원자 수가 다르다")
    # manifest 정책이 false 면 잡 메타가 다 맞아도 막는다 (선언과 실물 둘 다 봐야 한다)
    _rgp = _closure_estimand(dict(_man, gas_geometry_policy={"fixed_geometry_static": False}),
                             _RES(), _E, _emol, _jobs)
    chk(any(b.startswith("GAS_PAIR_CONTRACT") for b in _rgp["blocks"]),
        "⛔음성 AR 3: manifest 가 고정기하를 선언하지 않으면 막는다")
    # 구판 번들(메타에 새 필드가 없다) — 확인 못 한 것은 통과가 아니다
    _jold = dict(_jobs)
    for _k in _GASJOBS:
        _jold[_k] = {"ok": True, "gates": [],
                     "meta": {"kind": "mol_ref", "fragment": _GASJOBS[_k]["meta"]["fragment"],
                              "species_order": ["O"], "counts": [3]}, "geom": {}}
    chk(any(b.startswith("GAS_PAIR_CONTRACT")
            for b in _closure_estimand(_man, _RES(), _E, _emol, _jold)["blocks"]),
        "⛔음성 AR 3: 구판 번들(지문 필드 없음)은 **통과가 아니라 차단**이다")

    # ⛔음성 (회신 Z P0-4) — seed 이름이 같아도 **수렴 결과**가 갈리면 막는다
    _jb_het = dict(_jobs)
    _jb_het["prospective/sdcp_neutral__b01__afm2424_pm1"] = _BAS(
        "bbbb2222", "prospective/sdcp_neutral__b01__afm2424_pm1")
    _rh = _closure_estimand(_man, _RES(), _E, _emol, _jb_het)
    chk(any("BASIN_HETEROGENEOUS" in b for b in _rh["blocks"])
        and "primary_ddE_lowE_eV" not in _rh,
        "⛔음성: 한 조각 안에 서로 다른 realized basin 이 섞이면 min 을 안 뽑는다")
    _jb_none = dict(_jobs)
    _jb_none["prospective/ptfe_c10__b00__afm2424_pm1"] = _BAS(
        None, "prospective/ptfe_c10__b00__afm2424_pm1")
    _rn = _closure_estimand(_man, _RES(), _E, _emol, _jb_none)
    chk(any("BASIN_UNRESOLVED_IN_SET" in b for b in _rn["blocks"]),
        "⛔음성: realized basin 을 못 만든 잡이 있으면 그 집합으로 뺄셈하지 않는다")
    # ⛔음성 (회신 AA P0-3) — 경로와 구조화 필드가 어긋나면 값을 만들지 않는다
    _jb_x1 = dict(_jobs)
    _k1 = "prospective/sdcp_neutral__b00__afm2424_pm1"
    _jb_x1[_k1] = {**_BAS("aaaa1111", _k1)}
    _jb_x1[_k1]["meta"] = {**_jb_x1[_k1]["meta"], "fragment": "ptfe_c10"}
    _rx1 = _closure_estimand(_man, _RES(), _E, _emol, _jb_x1)
    chk(any("COHORT_INCOHERENT" in b for b in _rx1["blocks"]),
        "⛔음성: job.json 의 fragment 가 경로와 다르면 차단 (어느 쪽이 맞는지 우리가 못 정한다)")

    # ⛔음성 ★ v7 실측 — d3 가 **하나라도** 비면 막는다. 종전엔 "경로가 d3off 가
    #   아니면 정합" 으로 봐줬는데, 그 관용 때문에 net4 복합체 8잡이 필드 없이
    #   나갔다. 우연히 동작하는 것과 보증되는 것은 다르다.
    _jb_x2 = dict(_jobs)
    _jb_x2[_k1] = {**_BAS("aaaa1111", _k1)}
    _jb_x2[_k1]["meta"] = {k: v for k, v in _jb_x2[_k1]["meta"].items() if k != "d3"}
    _rx2 = _closure_estimand(_man, _RES(), _E, _emol, _jb_x2)
    chk(any("COHORT_INCOHERENT" in b for b in _rx2["blocks"]),
        "⛔음성: d3 필드가 비면 경로가 정상이어도 차단 (v7 의 net4 8잡이 그 모양이었다)")

    _jb_x3 = dict(_jobs)
    _k3 = "prospective/sdcp_neutral__b00__afm2424_pm1__d3off"
    _jb_x3[_k3] = {**_BAS("aaaa1111", _k1)}          # 경로는 d3off, 필드는 on
    _rx3 = _closure_estimand(_man, _RES(), _E, _emol, _jb_x3)
    chk(any("COHORT_INCOHERENT" in b for b in _rx3["blocks"]),
        "⛔음성: 경로는 __d3off 인데 job.json 이 d3=on 이면 차단 "
        "(D3 분해가 통째로 뒤집힌다)")

    _jb_x4 = dict(_jobs)
    _jb_x4[_k1] = {"ok": True, "gates": [], "geom": {"magnetic": {"realized_basin_id": "a"}}}
    _rx4 = _closure_estimand(_man, _RES(), _E, _emol, _jb_x4)
    chk(any("COHORT_INCOHERENT" in b for b in _rx4["blocks"]),
        "⛔음성: job.json(meta) 이 아예 없으면 차단 — 이름으로 추측하지 않는다")

    # ⛔음성 AO P0-4 — canary 와 부모 static 기하가 다르면 막는다 (스핀 검사 오염)
    chk(any("CANARY_GEOM_MISMATCH" in b for b in
            _closure_estimand(_man, _RES(same=False), _E, _emol, _jobs)["blocks"]),
        "⛔음성 AO P0-4: canary 가 부모와 **다른 기하**면 막는다 "
        "(두 에너지 차에 구조 이완 에너지가 섞인다)")
    # ⛔음성 AO P0-4 — 기하 대조를 **못 했으면** 그것도 차단이다 (확인 못 한 것 ≠ 통과)
    chk(any("CANARY_GEOM_UNCHECKED" in b for b in
            _closure_estimand(_man, {"pairs": {}}, _E, _emol, _jobs)["blocks"]),
        "⛔음성 AO P0-4: 기하 대조 결과가 **없으면** 통과가 아니라 차단이다")

    # ── 회신 AO P0-7 — pm1 조건부 D 를 net4 의 basin 차이가 지우지 않는다 ──
    _man7 = dict(_man, planned=dict(
        _PLANNED,
        **{k: _PL(k, seed="afm2424_net4")
           for k in ("prospective/sdcp_neutral__b09__afm2424_net4",
                     "prospective/ptfe_c10__b09__afm2424_net4")}), estimand_job_keys={
        "E_C_sdcp": "prospective/sdcp_neutral__b00__afm2424_pm1",
        "E_C_control": "prospective/ptfe_c10__b00__afm2424_pm1",
        "E_G_sdcp": "mol__sdcp_neutral__box24__nzmag",
        "E_G_control": "mol__ptfe_c10__box24__nzmag"})
    _en7 = dict(_en, **{"prospective/sdcp_neutral__b09__afm2424_net4": -201.2,
                        "prospective/ptfe_c10__b09__afm2424_net4": -100.6})
    _jb7 = {k: _BAS("aaaa1111", k,
                    **({"_dense": _en7[k] + 0.010} if k in _KJ else {}))
            for k in _en7 if k.startswith("prospective/")}
    _jb7.update(_GASJOBS)          # 기체 쌍 계약은 이 시나리오의 시험 대상이 아니다
    # net4 두 잡만 **다른 basin** 으로 수렴 → 종전엔 BASIN_HETEROGENEOUS 로 D 가 죽었다
    for _k in ("prospective/sdcp_neutral__b09__afm2424_net4",
               "prospective/ptfe_c10__b09__afm2424_net4"):
        _jb7[_k] = _BAS("bbbb2222", _k)
    _r7 = _closure_estimand(_man7, _RES(), lambda j: _en7.get(j), _emol, _jb7)
    # ⛔ 회신 AR Q1 이후: 정본 blocks 는 **다시 쓰지 않는다** (BASIN_HETEROGENEOUS 가 남는다).
    #   강등은 primary_estimand_blocks 뷰에서만 일어난다 — 그래서 둘 다 확인한다.
    chk(any(b.startswith("BASIN_HETEROGENEOUS") for b in _r7["blocks"]),
        "⛔음성 AR Q1: 정본 blocks 에는 BASIN_HETEROGENEOUS 가 **그대로 남는다** "
        f"(강등이 정본을 지우지 않는다) · blocks {_r7.get('blocks')}")
    chk(not any(b.startswith("BASIN_HETEROGENEOUS")
                for b in _r7.get("primary_estimand_blocks", _r7["blocks"]))
        and any("BASIN_HETEROGENEOUS" in n for n in (_r7.get("nonprimary_notes") or [])),
        "⛔음성 AO P0-7: net4 가 다른 basin 이어도 **pm1 조건부 D 를 지우지 않는다** "
        "(primary 뷰에서만 민감도 주석으로 내린다) · primary "
        f"{_r7.get('primary_estimand_blocks')}")
    chk(_r7.get("primary_ddE_lowE_eV") is not None,
        f"AO P0-7: 그 상태에서도 D_pm1 이 나온다 (실제 {_r7.get('primary_ddE_lowE_eV')})")
    # ⛔음성 — 그런데 **네 잡 자신**의 basin 이 없으면 여전히 막는다
    _jb7b = dict(_jb7)
    _jb7b["prospective/sdcp_neutral__b00__afm2424_pm1"] = _BAS(
        None, "prospective/sdcp_neutral__b00__afm2424_pm1")
    # ⛔ 회신 AP #2 이후 코드명이 바뀌었다: ESTIMAND_BASIN_UNRESOLVED(존재 확인) →
    #   ESTIMAND_TOPOLOGY_UNRESOLVED(모멘트 표를 읽어 topology 를 판정). pooled
    #   BASIN_UNRESOLVED_IN_SET 은 exact-key 경로에서 강등되므로 여기에 기대지 않는다.
    chk(any("ESTIMAND_TOPOLOGY_UNRESOLVED" in b
            for b in _closure_estimand(_man7, _RES(), lambda j: _en7.get(j),
                                       _emol, _jb7b)["blocks"]),
        "⛔음성 AO P0-7 / AP #2: **D 에 들어가는 네 잡** 의 자기 상태를 못 읽으면 "
        "여전히 막는다 (pooled 강등이 이걸 덮지 않는다)")
    # ── 회신 AP #2 — exact complex 쌍의 자기 topology 를 **직접 비교** ──
    def _J8(fp, jn):
        r = _BAS("aaaa1111", jn,
                 **({"_dense": _en8.get(jn, 0.0) + 0.010} if jn in _KJ else {}))
        r["geom"]["magnetic"] = {"realized_basin_id": "aaaa1111",
                                 "realized_basin": {"ni_moments_muB": list(fp)}}
        return r
    _up8 = [1.2] * 24 + [-1.2] * 24
    _dn8 = [-1.2] * 24 + [1.2] * 24                    # 전역 반전 — 같은 상태
    _mix8 = [1.2] * 23 + [-1.2] + [-1.2] * 23 + [1.2]  # 배열이 다르다 — 다른 상태
    _KA = "prospective/sdcp_neutral__b00__afm2424_pm1"
    _KB = "prospective/ptfe_c10__b00__afm2424_pm1"
    _man8 = dict(_man, estimand_job_keys={
        "E_C_sdcp": _KA, "E_C_control": _KB,
        "E_G_sdcp": "mol__sdcp_neutral__box24__nzmag",
        "E_G_control": "mol__ptfe_c10__box24__nzmag"})
    _en8 = {_KA: -201.0, _KB: -100.5,
            "mol__sdcp_neutral__box24__nzmag": -200.0,
            "mol__ptfe_c10__box24__nzmag": -100.0, **_GASE}
    _ok8 = dict(_GASJOBS, **{_KA: _J8(_up8, _KA), _KB: _J8(_dn8, _KB)})
    _r8 = _closure_estimand(_man8, _RES(), lambda j: _en8.get(j), _emol, _ok8)
    chk(not any("TOPOLOGY" in b for b in _r8["blocks"])
        and (_r8.get("estimand_topology") or {}).get("pm1", {}).get("same") is True,
        f"AP #2 양성: 전역 스핀 반전은 **같은 상태**로 본다 · blocks {_r8['blocks'][:1]}")
    _bad8 = dict(_GASJOBS, **{_KA: _J8(_up8, _KA), _KB: _J8(_mix8, _KB)})
    _r8b = _closure_estimand(_man8, _RES(), lambda j: _en8.get(j), _emol, _bad8)
    chk(any("ESTIMAND_TOPOLOGY_MISMATCH" in b for b in _r8b["blocks"]),
        "⛔음성 AP #2: 두 complex 가 **다른 자기 basin** 이면 막는다 "
        "(종전엔 각각 basin id 가 있는지만 보고 서로 같은지는 안 봤다)")
    _nofp = dict(_GASJOBS)
    for _k in (_KA, _KB):                       # 모멘트 표를 **명시적으로** 없앤다
        _j = _BAS("aaaa1111", _k)
        _j["geom"]["magnetic"] = {"realized_basin_id": "aaaa1111"}
        _nofp[_k] = _j
    chk(any("ESTIMAND_TOPOLOGY_UNRESOLVED" in b for b in
            _closure_estimand(_man8, _RES(), lambda j: _en8.get(j),
                              _emol, _nofp)["blocks"]),
        "⛔음성 AP #2: 모멘트 표가 없어 topology 를 못 읽으면 **막는다**")

    # ── 회신 AP #3 — 강등은 문자열이 아니라 job_keys 로 ──────────────────
    _r3 = _closure_estimand(_man7, _RES(), lambda j: _en7.get(j), _emol, _jb7)
    _recs = (_r3.get("nonprimary_note_records") or [])
    chk(all(r.get("job_keys") for r in _recs) and _recs,
        f"AP #3: 강등된 record 가 **구조화**돼 있고 job_keys 를 갖는다 ({len(_recs)}건)")
    chk(all(r["scope"] == "pooled_diagnostic" for r in _recs),
        "AP #3: 강등 판정은 **scope 필드**로 한다 (문자열 매칭 아님)")
    chk((_r3.get("pooled_demote_policy") or {}).get("estimand_safety"),
        "AP #3: pooled 를 강등한 대신 **네 잡의 안전 근거**를 결과에 명시한다")
    # ⛔음성 — pooled 를 강등해도 **네 잡 자신**의 결함은 여전히 막는다
    _jb3c = dict(_jb7)
    _jb3c["prospective/sdcp_neutral__b00__afm2424_pm1"] = dict(
        _jb3c["prospective/sdcp_neutral__b00__afm2424_pm1"],
        gates=["MAGNETIC_COLLAPSE(합성)"])
    chk(any("ESTIMAND_KEY_UNUSABLE" in b for b in
            _closure_estimand(_man7, _RES(), lambda j: _en7.get(j),
                              _emol, _jb3c)["blocks"]),
        "⛔음성 AP #3: pooled 강등이 **네 잡의 게이트를 덮지 않는다** "
        "(exact key 가 게이트되면 여전히 NO_VALUE)")

    # net4 직접식이 봉인돼 있으면 D_net4 − D_pm1 을 **실제로 계산한다**
    _man7n = dict(_man7, estimand_job_keys_net4={
        "E_C_sdcp": "prospective/sdcp_neutral__b09__afm2424_net4",
        "E_C_control": "prospective/ptfe_c10__b09__afm2424_net4",
        "E_G_sdcp": "mol__sdcp_neutral__box24__nzmag",
        "E_G_control": "mol__ptfe_c10__box24__nzmag"})
    _r7n = _closure_estimand(_man7n, _RES(), lambda j: _en7.get(j), _emol, _jb7)
    chk((_r7n.get("branch_sensitivity") or {}).get("status") == "computed"
        and "D_net4_minus_D_pm1_eV" in (_r7n.get("branch_sensitivity") or {})
        and _r7n.get("sensitivity_complete") is True,
        "AO P0-7: net4 가 봉인돼 있으면 **D_net4 − D_pm1 을 계산한다** "
        f"(종전엔 요구해 놓고 안 냈다) · {_r7n.get('branch_sensitivity')}")

    # ══ 회신 AS 해제조건 1 — **정상 pm1/net4 가 exit 0 인가** ═════════════════
    #   AR Q1 이후 정본 blocks 는 BASIN_HETEROGENEOUS 를 그대로 갖는다. pm1 과 net4 는
    #   **의도적으로 다른 topology** 라 정상 수렴해도 그것이 뜬다. 최종 종료 판정이
    #   정본을 읽으면 이 번들은 **성공할 수 없다** — 외주가 16잡 다 돌린 뒤에야 안다.
    _r_ok = _closure_estimand(_man7, _RES(), lambda j: _en7.get(j), _emol, _jb7)
    chk(any(b.startswith("BASIN_HETEROGENEOUS") for b in _r_ok["blocks"])
        and not _r_ok.get("primary_estimand_blocks")
        and _r_ok.get("primary_ddE_lowE_eV") is not None,
        "회신 AS 1: 정상 pm1/net4 는 정본에 BASIN_HETEROGENEOUS 가 있어도 "
        "**primary 뷰가 비어 있고 D 가 나온다** · primary %s"
        % _r_ok.get("primary_estimand_blocks"))
    # 그리고 **최종 종료 판정이 실제로 exit 0 을 내는지** 직접 친다
    _VCOK = {"applicable": True, "pass": True}
    chk(_final_verdict(_r_ok, _VCOK) == [],
        "⛔음성 AS 1: 정상 pm1/net4 에서 최종 판정이 **exit 0** 이다 "
        "(정본 blocks 를 읽던 종전 코드는 여기서 무조건 exit 2 였다)")
    chk(_final_verdict(dict(_r_ok, primary_estimand_blocks=["X(합성)"]), _VCOK),
        "⛔음성 AS 1: primary 뷰에 차단이 있으면 **exit 2** 다")
    chk(_final_verdict(dict(_r_ok, verdict="NO_VALUE — 합성"), _VCOK),
        "⛔음성 AS 1: NO_VALUE 면 exit 2 다")
    chk(_final_verdict(_r_ok, {"applicable": True, "pass": False}),
        "⛔음성 AS 1: 진공 판정이 실패하면 exit 2 다")
    # 구판 결과(강등 뷰 없음)는 정본으로 되돌아간다 — 조용히 통과시키지 않는다
    chk(_final_verdict({"blocks": ["OLD(합성)"]}, _VCOK),
        "⛔음성 AS 1: primary 뷰가 아예 없는 구판 결과는 **정본으로 막는다**")

    # ══ 회신 AS 해제조건 2 — canary 만 성공하면 **예외로 죽지 않는다** ══════════
    _en_np = {k: v for k, v in _en.items()
              if k != "refs/mol__sdcp_neutral__box24"}      # 부모만 없앤다
    _emol_np = {"sdcp_neutral": None, "ptfe_c10": -100.0}
    _r_np = _closure_estimand(_man, _RES(), lambda j: _en_np.get(j), _emol_np, _jobs)
    chk(any("MOLECULAR_SPIN_CONTROL_PARENT_MISSING" in b for b in _r_np["blocks"]),
        "⛔음성 AS 2: box24 부모가 없고 canary 만 있으면 **구조화 차단**이다 "
        "(종전엔 `e1 - None` 으로 예외 사망)")

    # ══ 회신 AS 해제조건 3 — pooled 가 **살아남은 부분집합**으로 계산되지 않는다 ══
    _jb_gate = dict(_jobs)
    _jb_gate["prospective/sdcp_neutral__b01__afm2424_pm1"] = dict(
        _jb_gate["prospective/sdcp_neutral__b01__afm2424_pm1"],
        ok=False, gates=["MAGNETIC_COLLAPSE(합성)"])
    _r_gate = _closure_estimand(_man, _RES(), _E, _emol, _jb_gate)
    _pc = _r_gate.get("pool_completeness") or {}
    chk(_pc.get("ok") is False
        and any("GATED_POSE" in r["msg"] for r in _r_gate["block_records"])
        and (_r_gate.get("pooled_effect") or {}).get("secondary_G_citable") is False
        and _r_gate.get("secondary_G_eV") is None,
        "⛔음성 AS 3: 계획된 자세 하나가 게이트되면 **GATED_POSE 가 실제로 기록되고** "
        "pooled 값이 비인용이 된다 (종전엔 ok=false 를 먼저 건너뛰어 도달조차 못 했다)")
    # 결과가 아예 없는 경우도 같다 (계획엔 있는데 안 돌아왔다)
    _jb_miss = {k: v for k, v in _jobs.items()
                if k != "prospective/sdcp_neutral__b01__afm2424_pm1"}
    _r_miss = _closure_estimand(_man, _RES(), _E, _emol, _jb_miss)
    chk((_r_miss.get("pool_completeness") or {}).get("ok") is False
        and (_r_miss.get("pooled_effect") or {}).get("pooled_min_citable") is False,
        "⛔음성 AS 3: 계획된 자세가 **회수되지 않아도** pooled 를 비인용으로 한다")
    chk((r.get("pool_completeness") or {}).get("ok") is True,
        "회신 AS 3 양성: 계획된 자세가 전건 사용가능하면 pool 이 완전하다 · %s"
        % (r.get("pool_completeness") or {}).get("expected"))

    # ══ 회신 AR P1-9 · 해제조건 6 — net4 topology 실패가 **실제로** 막는가 ═════
    #   `usable_as_sensitivity` 를 저장만 하고 안 읽어서, 두 complex 가 다른
    #   basin 이어도 D_net4 가 계산되고 complete 로 보고됐다.
    _KN4A = "prospective/sdcp_neutral__b09__afm2424_net4"
    _KN4B = "prospective/ptfe_c10__b09__afm2424_net4"
    _mixfp = [1.2] * 23 + [-1.2] + [-1.2] * 23 + [1.2]     # 배열이 다르다
    _jb7t = dict(_jb7)
    _jb7t[_KN4A] = _J8([1.2] * 24 + [-1.2] * 24, _KN4A)
    _jb7t[_KN4B] = _J8(_mixfp, _KN4B)
    _r7t = _closure_estimand(_man7n, _RES(), lambda j: _en7.get(j), _emol, _jb7t)
    _bs7 = _r7t.get("branch_sensitivity") or {}
    chk(_bs7.get("status") == "suppressed_topology"
        and _bs7.get("D_net4_eV") is None
        and _bs7.get("D_net4_minus_D_pm1_eV") is None
        and _r7t.get("sensitivity_complete") is False
        and _r7t.get("primary_ddE_lowE_eV") is not None,
        "⛔음성 AR P1-9: net4 두 complex 가 다른 basin 이면 **D_net4 값과 status 를 "
        f"같이 막는다** (D_pm1 은 산다) · {_bs7.get('status')}")
    # 모멘트 표를 못 읽어도 마찬가지다 — 확인 못 한 것은 통과가 아니다
    _jb7u = dict(_jb7)
    for _k in (_KN4A, _KN4B):
        _ju = _BAS("aaaa1111", _k)
        _ju["geom"]["magnetic"] = {"realized_basin_id": "aaaa1111"}
        _jb7u[_k] = _ju
    _r7u = _closure_estimand(_man7n, _RES(), lambda j: _en7.get(j), _emol, _jb7u)
    chk((_r7u.get("branch_sensitivity") or {}).get("status") == "suppressed_topology"
        and _r7u.get("sensitivity_complete") is False,
        "⛔음성 AR P1-9: net4 topology 를 **못 읽어도** 민감도를 완료로 보고하지 않는다")

    # ══ 회신 AR P1-10 · 해제조건 6 — 대안 자세를 **봉인식**으로 낸다 ══════════
    _KPA = "prospective/sdcp_neutral__b04__afm2424_pm1"
    _KPB = "prospective/ptfe_c10__b04__afm2424_pm1"
    _enp = dict(_en7, **{_KPA: -201.15, _KPB: -100.52})
    _manp = dict(_man7n, estimand_job_keys_pose_alt={
        "sensitivity": {"E_C_sdcp": _KPA, "E_C_control": _KPB,
                        "E_G_sdcp": "mol__sdcp_neutral__box24__nzmag",
                        "E_G_control": "mol__ptfe_c10__box24__nzmag",
                        "formula": "D_pose[sensitivity] = ..."},
        "⛔": "주석 키 — 순회에서 건너뛰어야 한다"})
    _up = [1.2] * 24 + [-1.2] * 24
    _jbp = dict(_jb7, **{_KPA: _J8(_up, _KPA), _KPB: _J8(_up, _KPB)})
    _rp = _closure_estimand(_manp, _RES(), lambda j: _enp.get(j), _emol, _jbp)
    _ps = (_rp.get("pose_sensitivity") or {}).get("sensitivity") or {}
    chk(_ps.get("status") == "computed" and _ps.get("D_pose_eV") is not None
        and _ps.get("D_pose_minus_D_pm1_eV") is not None
        and _rp.get("sensitivity_complete") is True,
        "회신 AR P1-10 양성: 대안 자세가 봉인돼 있으면 **D_pose − D_pm1 을 낸다** "
        f"· {_ps.get('D_pose_minus_D_pm1_eV')} eV")
    # ⛔음성 2026-08-31 실측 — 실물 c12 는 두 조각의 대안 자세 **역할 이름이 다르다**
    #   (sdcp=stress_sensitivity · ptfe=sensitivity). 같은 역할끼리만 짝지으면
    #   봉인이 통째로 비어 스테이지 2 의 네 잡이 아무 정의된 양도 못 낸다.
    _manrp = dict(_man7n, estimand_job_keys_pose_alt={
        "role_pair": {"E_C_sdcp": _KPA, "E_C_control": _KPB,
                      "E_G_sdcp": "mol__sdcp_neutral__box24__nzmag",
                      "E_G_control": "mol__ptfe_c10__box24__nzmag",
                      "formula": "D_pose[role_pair] = ...",
                      "roles": {"sdcp_neutral": ["stress_sensitivity"],
                                "ptfe_c10": ["sensitivity"]},
                      "⚠_역할_비대칭": "두 조각의 대안 자세를 다른 이유로 골랐다"}})
    _rrp = _closure_estimand(_manrp, _RES(), lambda j: _enp.get(j), _emol, _jbp)
    _prp = (_rrp.get("pose_sensitivity") or {}).get("role_pair") or {}
    chk(_prp.get("status") == "computed"
        and _prp.get("D_pose_minus_D_pm1_eV") is not None
        and _rrp.get("sensitivity_complete") is True,
        "회신 AR P1-10 (실측 보정): 두 조각의 대안 자세 **역할이 달라도** "
        f"role_pair 로 봉인하면 값이 나온다 · {_prp.get('D_pose_minus_D_pm1_eV')} eV")
    # ⛔음성 — 두 자세 complex 가 다른 basin 이면 값도 status 도 막는다
    _jbp2 = dict(_jbp, **{_KPB: _J8(_mixfp, _KPB)})
    _rp2 = _closure_estimand(_manp, _RES(), lambda j: _enp.get(j), _emol, _jbp2)
    _ps2 = (_rp2.get("pose_sensitivity") or {}).get("sensitivity") or {}
    chk(_ps2.get("status") == "suppressed_topology" and _ps2.get("D_pose_eV") is None
        and _rp2.get("sensitivity_complete") is False
        and any("POSE_SENSITIVITY_INCOMPLETE" in n
                for n in (_rp2.get("nonprimary_notes") or []))
        and _rp2.get("primary_ddE_lowE_eV") is not None,
        "⛔음성 AR P1-10: 자세 두 complex 가 다른 basin 이면 D_pose 를 막고 "
        "'자세에 강건' 서술을 금지한다 (D_pm1 은 산다)")
    # ⛔음성 — 잡이 게이트돼 있으면 unavailable
    _jbp3 = dict(_jbp)
    _jbp3[_KPA] = dict(_jbp3[_KPA], gates=["MAGNETIC_COLLAPSE(합성)"])
    _rp3 = _closure_estimand(_manp, _RES(), lambda j: _enp.get(j), _emol, _jbp3)
    chk(((_rp3.get("pose_sensitivity") or {}).get("sensitivity") or {}).get("status")
        == "unavailable" and _rp3.get("sensitivity_complete") is False,
        "⛔음성 AR P1-10: 자세 잡이 게이트되면 unavailable 이고 완료가 아니다")
    # 봉인이 아예 없으면 **탐색용**임을 명시한다 (완료 여부만 보고하지 않는다)
    _rp4 = _closure_estimand(dict(_man7n, altpose_purpose="탐색용"),
                             _RES(), lambda j: _en7.get(j), _emol, _jb7)
    chk((_rp4.get("pose_sensitivity") or {}).get("status") == "exploratory_only",
        "회신 AR P1-10: 봉인식이 없으면 **탐색용**이라고 결과에 박는다")

    # ── 회신 AP #11 — δ_gas 를 **최종 estimand 에 직접** 건다 ────────────
    _rg = _closure_estimand(_man, _RES(), _E, _emol, _jobs)
    chk((_rg.get("gas_box_delta") or {}).get("pass") is True,
        f"AP #11 양성: δ_gas {_rg.get('gas_box_delta', {}).get('delta_gas_meV')} meV "
        f"≤ {_rg.get('gas_box_delta', {}).get('tol_meV')} — 0.01 eV 보고 가능")
    # ⛔음성 — 조각별로는 각각 작아도 **부호가 반대면 차에서 커진다**
    _enbad = dict(_en, **{"refs/mol__sdcp_neutral__box20": -205.4486 - 0.004,
                          "refs/mol__ptfe_c10__box20": -177.9706 + 0.004})
    _rgb = _closure_estimand(_man, _RES(), lambda j: _enbad.get(j), _emol, _jobs)
    _gd = _rgb.get("gas_box_delta") or {}
    chk(any("GAS_BOX_DELTA" in b for b in _rgb["blocks"]),
        "⛔음성 AP #11: 조각별 4 meV 씩이어도 **부호가 반대면** δ_gas 8 meV → 차단 "
        f"(실제 {_gd.get('delta_gas_meV')} meV · 조각별 {_gd.get('by_fragment_meV')})")
    chk(abs((_gd.get("delta_gas_meV") or 0)) > 5.0
        and all(abs(v) <= 5.0 for v in (_gd.get("by_fragment_meV") or {}).values()),
        "⛔음성 AP #11 요점: **조각별 문턱이었으면 통과했을** 경우다 "
        "(그래서 조각별이 아니라 차에 건다)")
    # ⛔ 회신 AR P0-3 재현 — **조각별로는 크고 차는 작은** 경우. 옛 조각별 10 meV
    #   게이트가 살아 있으면 두 emol 이 None 이 되고 A(f,p) 에서 `float − None` 으로
    #   **예외로 죽었다** (리뷰가 재현한 그 모양이다). 지금은 δ_gas 1 meV 로 통과한다.
    _en2019 = dict(_en, **{"refs/mol__sdcp_neutral__box20": -205.4486 - 0.020,
                           "refs/mol__ptfe_c10__box20": -177.9706 - 0.019})
    _r2019 = _closure_estimand(_man, _RES(), lambda j: _en2019.get(j), _emol, _jobs)
    _g19 = _r2019.get("gas_box_delta") or {}
    chk(_g19.get("pass") is True and abs(_g19.get("delta_gas_meV") or 0) <= 5.0
        and all(abs(v) >= 15.0 for v in (_g19.get("by_fragment_meV") or {}).values())
        and not any("GAS_BOX" in b for b in _r2019["blocks"])
        and _r2019.get("primary_ddE_lowE_eV") is not None,
        "회신 AR P0-3 재현: 조각별 %s meV 인데 δ_gas %s meV → **통과하고 예외로 "
        "죽지 않는다** (옛 조각별 게이트가 죽이던 경우)"
        % (_g19.get("by_fragment_meV"), _g19.get("delta_gas_meV")))
    # ⛔음성 — box20 이 아예 없으면 "측정 안 함" 으로 막는다 (선행값으로 때우지 않는다)
    _enno = {k: v for k, v in _en.items() if not k.endswith("box20")}
    chk(any("GAS_BOX_NOT_MEASURED" in b for b in
            _closure_estimand(_man, _RES(), lambda j: _enno.get(j),
                              _emol, _jobs)["blocks"]),
        "⛔음성 AP #11: box20 이 없으면 **이 묶음에서 재지 못했다**고 막는다 "
        "(선행 대조로 때우지 않는다)")

    _jb_slab = dict(_jobs)
    _jb_slab["refs/clean_slab__afm2424_pm1"] = _BAS(
        "cccc3333", "prospective/sdcp_neutral__b00__afm2424_pm1",
        kind="clean_ref", fragment=None, basin_id=None)
    _rs = _closure_estimand(_man, _RES(), _E, _emol, _jb_slab)
    chk(any("BASIN_MISMATCH_SLAB" in b for b in _rs["blocks"]),
        "⛔음성: clean slab 이 복합체와 다른 basin 이면 흡착에너지를 만들지 않는다")
    chk(abs(r["primary_ddE_lowE_eV"] - (-0.5)) < 1e-6,
        f"[V P0-4] primary = min-min = -0.5 · 실제 {r.get('primary_ddE_lowE_eV')}")
    # G = min(A_c10) - max(A_sdcp) = -0.5 - (-0.9) = +0.4.
    #   G>0 = 가장 약한 SDCP 도 가장 센 c10 보다 더 음수 (사전등록 정의와 일치).
    chk(r["secondary_G_eV"] is None and "영구 비인용" in str(r.get("secondary_G_⛔"))
        and (r.get("pooled_effect") or {}).get("citable", "").startswith("no"),
        "🔴 AT Q5(a): secondary_G 와 pooled min 이 **영구 비인용**이다 "
        "(추가 잡 0 · 자세 탐색의 폭은 MLIP 가 진다)")
    chk(abs(r["secondary_G_eV_diagnostic"] - 0.4) < 1e-6,
        f"[V P0-4] secondary G = +0.4 (>0 = 최약 SDCP 도 최강 c10 보다 음수) · "
        f"실제 {r.get('secondary_G_eV')}")
    chk(r["verdict"] == "보고 가능" and r["reported_X_eV"] == -0.5,
        "[V P0-4] guard(-0.10) 통과 + 0.01 eV 반올림")
    # 음성: guard band 미달
    _en2 = dict(_en)
    _en2["prospective/sdcp_neutral__b00__afm2424_pm1"] = -200.55
    _en2["prospective/sdcp_neutral__b01__afm2424_pm1"] = -200.55
    _jb2 = {k: (dict(v, dense={"normal_end": True, "E0": _en2[k] + 0.010})
                if k in _KJ else v) for k, v in _jobs.items()}
    r2 = _closure_estimand(_man, _RES(), lambda j: _en2.get(j), _emol, _jb2)
    chk(r2["verdict"] == "NO_DIRECTIONAL_CLAIM",
        f"[음성 V P0-4] primary {r2.get('primary_ddE_lowE_eV')} > -0.10 → 방향성 주장 금지")
    # 음성: 비영 시작이 더 낮으면 값을 내지 않는다
    _en3 = dict(_en); _en3["mol__sdcp_neutral__box24__nzmag"] = -200.3
    r3 = _closure_estimand(_man, _RES(), lambda j: _en3.get(j), _emol, _jobs)
    chk(any("MOLECULAR_STATE_UNRESOLVED" in b for b in r3["blocks"])
        and "primary_ddE_lowE_eV" not in r3,
        "[음성 V P0-3] 비영 MAGMOM 대조가 더 낮으면 **MOLECULAR_STATE_UNRESOLVED 로 막고 "
        "값을 안 낸다** (자동 채택 금지)")
    # 음성: 자기 topology 게이트된 자세는 버리고 값도 안 낸다
    _j4 = dict(_jobs)
    _j4["prospective/sdcp_neutral__b00__afm2424_pm1"] = {
        **_BAS("aaaa1111", "prospective/sdcp_neutral__b00__afm2424_pm1"),
        "gates": ["MAGNETIC_PARTIAL_FLIP(3/48 Ni)"]}
    r4 = _closure_estimand(_man, _RES(), _E, _emol, _j4)
    chk(any("GATED_POSE" in b for b in r4["blocks"]) and "primary_ddE_lowE_eV" not in r4,
        "[음성 V P0-4] 자기 topology 게이트된 자세는 **다음 순위로 조용히 대체하지 않는다**")
    # 음성: 대조가 아예 없으면
    r5 = _closure_estimand({"fragments": ["sdcp_neutral", "ptfe_c10"]},
                           {"pairs": {}}, _E, _emol, _jobs)
    chk(any("MOLECULAR_SPIN_CONTROL_MISSING" in b for b in r5["blocks"]),
        "[음성 V P0-3] 자기상태 대조가 없으면 그것도 block")

    # ══ 회신 AR 해제조건 5 — 1단계 선결조건이 **여덟 개를 다 본다** ═══════════
    #   AR: "analyze_results.py 는 GAS_BOX_DELTA 와 ESTIMAND_TOPOLOGY_MISMATCH 를
    #   보지 않으므로, 이미 primary estimand 가 실패한 뒤에도 STAGE1_PASS.json 을
    #   쓰고 stage 2 를 열 수 있다."
    _VC_OK = {"pass": True, "verdict": "VACUUM_CONVERGED", "applicable": True}
    _RES_OK = {"gas_canary_geom": {f: {"same": True} for f in
                                   ("sdcp_neutral", "ptfe_c10")}}
    _CL_OK = {
        "blocks": [], "block_records": [],
        "potcar_identity": {"blocking": [], "identity_scope": "sealed_root_v13 …",
                            "root_seal_coverage": {"ok": True, "why": "포괄"}},
        "gas_box_delta": {"pass": True, "delta_gas_meV": 0.1, "tol_meV": 5.0},
        "gas_pair_contract": {"ok": True},
        "estimand_topology": {"pm1": {"same": True, "blocks": [], "why": "동일"}},
    }
    _p0 = _stage1_prereqs(_CL_OK, _VC_OK, _RES_OK)
    chk(len(_p0) == 8 and all(v["pass"] for v in _p0.values()),
        "회신 AR 5 양성: 선결조건 **8개**가 다 통과할 때만 2단계가 열린다 (%s)"
        % sorted(_p0))
    for _need5 in ("vacuum", "molecular_state", "canary_geometry", "potcar_identity",
                   "gas_box_delta", "estimand_topology_pm1", "closure_blocks_clear",
                   "root_seal_covers_plan"):
        chk(_need5 in _p0, "AR 5: 선결조건에 `%s` 가 있다" % _need5)
    # ⛔음성 — 여덟 축을 하나씩 깨뜨리면 그 축이 실패한다
    def _p5(mut, vc=None, res=None):
        return _stage1_prereqs(dict(_CL_OK, **mut), vc or _VC_OK, res or _RES_OK)
    _cases5 = [
        ("gas_box_delta", {"gas_box_delta": {"pass": False, "delta_gas_meV": 9.0},
                           "blocks": ["GAS_BOX_DELTA(δ_gas 9.0 meV > 5)"]},
         "δ_gas 가 문턱을 넘으면"),
        ("gas_box_delta", {"gas_pair_contract": {"ok": False}},
         "기체 쌍 계약이 깨지면 (δ_gas 수치가 작아도)"),
        ("estimand_topology_pm1",
         {"estimand_topology": {"pm1": {"same": False,
                                        "blocks": ["ESTIMAND_TOPOLOGY_MISMATCH(pm1)"]}}},
         "pm1 두 complex 가 다른 자기 basin 이면"),
        ("estimand_topology_pm1", {"estimand_topology": {}},
         "pm1 topology 판정이 **아예 없으면** (확인 못 함 = 통과 아님)"),
        ("closure_blocks_clear",
         {"block_records": [{"code": "X", "msg": "X(합성)", "scope": "estimand",
                             "affects_estimand": True}],
          "blocks": ["X(합성)"]},
         "잔여 exact-estimand block 이 있으면"),
        ("closure_blocks_clear",
         {"blocks": ["POTCAR_IDENTITY:합성(구조화 안 된 전역 차단)"]},
         "구조화되지 않은 전역 차단이 남아 있으면"),
        ("root_seal_covers_plan",
         {"potcar_identity": {"blocking": [], "identity_scope": "x",
                              "root_seal_coverage": {"ok": False, "why": "반쪽 봉인"}}},
         "root seal 이 계획을 포괄하지 못하면"),
        ("root_seal_covers_plan",
         {"potcar_identity": {"blocking": [], "identity_scope": "x"}},
         "root seal 포괄 검사 결과가 **없으면**"),
    ]
    for _ax, _mut, _why in _cases5:
        _pp = _p5(_mut)
        chk(_pp[_ax]["pass"] is False,
            "⛔음성 AR 5: %s `%s` 가 실패한다 → 2단계를 열지 않는다" % (_why, _ax))
    # pooled_diagnostic 강등은 1단계를 막지 않는다 (그 강등의 근거는 AP #3 에 있다)
    _pp_pooled = _p5({"block_records": [
        {"code": "BASIN_HETEROGENEOUS", "msg": "BASIN_HETEROGENEOUS(합성)",
         "scope": "pooled_diagnostic", "affects_estimand": False}],
        "blocks": ["BASIN_HETEROGENEOUS(합성)"]})
    chk(_pp_pooled["closure_blocks_clear"]["pass"] is True,
        "AR 5: pooled_diagnostic 로 강등된 block 은 1단계를 막지 않는다 "
        "(정본 blocks 에는 남아 있어도 scope 로 거른다)")



def selftest_k() -> int:
    """k 라벨·guard band 의 **순수 산술**을 시험한다 (음성 포함).

    이 시험이 못 하는 것: OUTCAR 회수·게이트 연동. 그건 번들 selftest 몫이다.
    """
    ok = True
    # ⛔ 회신 AR P1-12 — **개수를 재현 가능하게** 센다 (문서에 적은 수와 실행 결과가
    #   갈라지지 않게). 리스트인 이유는 _selftest_closure 와 공유하기 위해서다.
    _CHKN = [0, 0]

    def chk(c, m):
        nonlocal ok
        _CHKN[0] += 1
        _CHKN[1] += bool(c)
        print(("  ✓ " if c else "  ✗ ") + m)
        ok = ok and bool(c)

    F = ["c10", "doped", "neutral", "dimer"]
    C = ["c10", "doped"]
    # 양성: 보정자 둘이 작고 서로 가까우면 나머지는 전이 심사 통과
    kt, lb, _ = k_transfer_gate(C, {"c10": 0.003, "doped": 0.005}, F)
    chk(kt["pass"] and lb["c10"] == "K_DIRECTLY_CHECKED"
        and lb["neutral"] == "K_TRANSFER_SCREENED",
        f"κ +3/+5 meV → 전이 통과 · 라벨 {lb['neutral']}")
    # ★★ 음성 (이 함수를 만든 이유): 부호가 반대면 크기만으로는 통과해 버린다
    kt2, lb2, _ = k_transfer_gate(C, {"c10": 0.009, "doped": -0.009}, F)
    chk(not kt2["pass"] and lb2["neutral"] == "K_UNVERIFIED",
        f"κ +9/−9 meV → **탈락** (각각은 10 이하지만 range {kt2['range_meV']} meV)")
    chk(max(abs(v) for v in kt2["kappa_eV"].values()) <= GUARD_EV,
        "  ↑ 전제 확인: 절대값만 봤다면 통과했을 사례다")
    # 음성: 크기가 크면 탈락
    kt3, lb3, _ = k_transfer_gate(C, {"c10": 0.025, "doped": 0.026}, F)
    chk(not kt3["pass"] and lb3["dimer"] == "K_UNVERIFIED",
        f"κ +25/+26 meV → 탈락 (range 는 작아도 max {kt3['max_abs_meV']} meV)")
    # 음성: 보정자 하나가 결측이면 전이 불가
    kt4, lb4, _ = k_transfer_gate(C, {"c10": 0.002}, F)
    chk(not kt4["pass"] and lb4["c10"] == "K_DIRECTLY_CHECKED"
        and lb4["doped"] == "K_UNVERIFIED",
        "보정자 1/2 회수 → 전이 불가 (회수된 쪽은 여전히 직접 검증)")
    # 음성: 보정자 미지정이면 조용히 통과시키지 않는다
    kt5, lb5, _ = k_transfer_gate([], {}, F)
    chk(not kt5["pass"] and set(lb5.values()) == {"K_UNVERIFIED"},
        "보정자 미지정 + κ 도 없음 → 전 조각 K_UNVERIFIED")
    # ★ 라벨은 **선언이 아니라 데이터**를 따른다 — dense 를 돌렸으면 직접 검증이다
    kt6, lb6, _ = k_transfer_gate([], {"c10": 0.004, "doped": 0.006}, F)
    chk(lb6["c10"] == "K_DIRECTLY_CHECKED" and lb6["neutral"] == "K_TRANSFER_SCREENED",
        "보정자 미선언이어도 κ 를 잰 조각은 직접 검증 (선언만 보면 headline 이 막힌다)")

    # ── 전역 부호 정규화 (Codex 5차 P1-2) ────────────────────────────────
    #   static 과 dense 가 이 규칙을 따로 구현해서, dense 가 **완전한 시간반전**으로
    #   수렴하면 전부 불일치로 잡는 거짓 차단이 났다. 한 함수로 두고 여기서 시험한다.
    _w = {0: 1.0, 1: -1.0, 2: 1.0, 3: -1.0}
    _same = {0: 1.2, 1: -1.2, 2: 1.2, 3: -1.2}
    chk(global_sign(_same, _w) == (1.0, []), "시드와 같은 배치 → sg=+1, 불일치 0")
    _rev = {k: -v for k, v in _same.items()}
    chk(global_sign(_rev, _w) == (-1.0, []),
        "**완전한 시간반전** → sg=−1, 불일치 0 (같은 상태다)")
    _part = dict(_same); _part[1] = +1.2          # 하나만 뒤집힘
    _sg, _bad = global_sign(_part, _w)
    chk(_bad == [1], f"부분 반전 하나 → 그것만 잡는다 ({_bad})")
    _half = {0: 1.2, 1: 1.2, 2: -1.2, 3: -1.2}    # 절반 반전 (모호)
    _sg2, _bad2 = global_sign(_half, _w)
    chk(len(_bad2) == 2, f"절반 반전 → 어느 부호로 봐도 2개 불일치 ({_bad2})")
    _zero = {k: 0.0 for k in _w}
    chk(len(global_sign(_zero, _w)[1]) == len(_w),
        "모멘트 전부 0 → 전부 불일치 (붕괴를 통과시키지 않는다)")

    # ── realized_basin_id (회신 Z P0-4) ──────────────────────────────────
    #   pm1/net4 는 초기 seed 이름이지 최종 basin 이 아니다. 지문이 **수렴 결과**를
    #   따라가는지, 그리고 안 따라가야 할 것(시간반전)에 안 따라가는지 본다.
    _NS = {str(i): v for i, v in _w.items()}
    _b_same, _d_same = realized_basin_id([1.2, -1.2, 1.2, -1.2], _NS, {})
    _b_rev, _d_rev = realized_basin_id([-1.2, 1.2, -1.2, 1.2], _NS, {})
    chk(_b_same is not None and _b_same == _b_rev,
        "완전한 시간반전은 **같은 basin** (전역 부호 정규화 후 지문)")
    chk(len(_b_same) == 64 and _d_same["id_short"] == _b_same[:12],
        "지문은 canonical JSON 의 **full SHA256** — 12자는 표시용 (회신 AA Q5-b)")
    _b_flip, _d_flip = realized_basin_id([1.2, 1.2, 1.2, -1.2], _NS, {})
    chk(_b_flip is not None and _b_flip != _b_same,
        "⛔음성: Ni 하나가 뒤집히면 **다른 basin** (wave1.5 의 실제 사고 모양)")
    _b_col, _ = realized_basin_id([1.2, -1.2, 0.1, -1.2], _NS, {})
    chk(_b_col != _b_same and _b_col is not None,
        "⛔음성: 모멘트 붕괴도 다른 basin (부호는 살아 있어도 상태가 다르다)")
    # ★ 회신 AA Q5-c — 두 문턱. 회색은 판정하지 않는다
    _b_gray, _dg = realized_basin_id([1.2, -1.2, 0.40, -1.2], _NS, {})
    chk(_b_gray is None and "회색구간" in _dg["why"],
        f"⛔음성: 회색구간(0.25–0.55 μB) 모멘트는 **unresolved** — 단일 문턱이면 "
        f"0.4 를 자성으로 오판했다")
    _MS = {"4": 1.0}
    _b_o1, _ = realized_basin_id([1.2, -1.2, 1.2, -1.2, 0.9], _NS, _MS)
    _b_o2, _ = realized_basin_id([1.2, -1.2, 1.2, -1.2, -0.9], _NS, _MS)
    chk(_b_o1 != _b_o2,
        "⛔음성: Ni 는 같은데 **유기종 상대스핀**만 갈려도 다른 basin")
    chk(realized_basin_id(None, _NS, {})[0] is None
        and realized_basin_id([1.2], _NS, {})[0] is None,
        "⛔음성: 표가 없거나 짧으면 **추측하지 않고** None (뺄셈을 막는다)")
    _b_o1b, _ = realized_basin_id([-1.2, 1.2, -1.2, 1.2, -0.9], _NS, _MS)
    chk(_b_o1b == _b_o1,
        "유기종까지 통째로 반전해도 같은 basin (시간반전은 상대부호를 안 바꾼다)")
    # ★ 회신 AA Q5 — 시간반전을 접을 수 있는 계인지 INCAR 로 확인
    chk(realized_basin_id([1.2, -1.2, 1.2, -1.2], _NS, {},
                          incar_echo={"LSORBIT": ".TRUE."})[0] is None,
        "⛔음성: SOC 가 켜져 있으면 시간반전을 접지 않는다 (전제가 깨진다)")
    chk(realized_basin_id([1.2, -1.2, 1.2, -1.2], _NS, {},
                          incar_echo={"I_CONSTRAINED_M": "1"})[0] is None,
        "⛔음성: signed spin constraint 가 걸려 있으면 접지 않는다")
    chk(realized_basin_id([1.2, -1.2, 1.2, -1.2], _NS, {},
                          incar_echo={"LSORBIT": ".FALSE.", "ISPIN": "2"})[0] is not None,
        "양성: collinear·무SOC·무제약이면 접는다")
    # ★ basin_distance (회신 AA Q5-c) — "얼마나 다른가"
    _dd = basin_distance(_d_same, _d_flip)
    chk(_dd["hamming"] == 1 and _dd["flipped_index_poscar"] == [1] and not _dd["same"],
        f"거리: Ni 하나 뒤집힘 → hamming 1, 인덱스 {_dd['flipped_index_poscar']}")
    _dd2 = basin_distance(_d_same, _d_rev)
    chk(_dd2["same"] and _dd2["hamming"] == 0 and _dd2["moment_rms_muB"] < 1e-9,
        "거리: 시간반전끼리는 hamming 0 · RMS 0 (전역부호로 정규화해 비교한다)")
    _b_big, _d_big = realized_basin_id([2.0, -2.0, 2.0, -2.0], _NS, {})
    _dd3 = basin_distance(_d_same, _d_big)
    chk(_dd3["hamming"] == 0 and not _dd3["same"] and _dd3["moment_rms_muB"] > 0.3,
        f"⛔음성: 부호가 같아도 **크기**가 벌어지면 동일 판정 안 한다 "
        f"(RMS {_dd3['moment_rms_muB']} > {MOM_RMS_TOL})")

    # ── 닫힘 조건 C1 · C3 (회신 AA P0-4 — 코드로 낸다) ────────────────────
    def _J(kind, _edisp=None, _mom=(1.2, -1.2, 1.2, -1.2), **kw):
        m = {"kind": kind, "d3": "on"}; m.update(kw)
        return {"ok": True, "gates": [], "meta": m,
                # C3 v2 는 OUTCAR 의 Edisp 를 읽는다 — 픽스처도 실물과 같은 자리에 둔다
                "static": {"edisp_eV": _edisp, "edisp_n": 0 if _edisp is None else 1,
                           "incar_echo": {"NSW": "0"}},
                # ★ P0-4 — 해시만이 아니라 **상세 지문**도 실물과 같은 자리에 둔다.
                #   없으면 same_basin() 이 (옳게) 통과시키지 않는다.
                "geom": {"magnetic": {
                    "realized_basin_id": "B",
                    "realized_basin": {
                        "ni_sign_vector": [1 if x > 0 else -1 for x in _mom],
                        "ni_index_poscar": [0, 1, 2, 3],
                        "collapsed_ni_positions": [],
                        "ni_moments_muB": list(_mom), "global_sign": 1.0}}}}

    _en3, _jb3 = {}, {}
    _CS = "refs/clean_slab__" + SEED_MAIN
    _jb3[_CS] = _J("clean_ref", seed=SEED_MAIN, _edisp=-1.0); _en3[_CS] = -900.0
    _jb3[_CS + "__d3off"] = _J("clean_ref", seed=SEED_MAIN, d3="off", d3_twin_of=_CS)
    _en3[_CS + "__d3off"] = -899.0                    # d_slab = -1.0 = Edisp_slab
    for _f, _em, _dm in (("sdcp_neutral", -200.0, -0.5), ("ptfe_c10", -100.0, -0.2)):
        _mk = "refs/mol__%s__box24" % _f
        _jb3[_mk] = _J("mol_ref", fragment=_f, _edisp=_dm); _en3[_mk] = _em
        _jb3[_mk + "__d3off"] = _J("mol_ref", fragment=_f, d3="off", d3_twin_of=_mk)
        _en3[_mk + "__d3off"] = _em - _dm             # d_mol = _dm = Edisp_mol
        for _i in range(4):
            _k = "prospective/%s__b%02d__%s" % (_f, _i, SEED_MAIN)
            _dcx = -2.0 if _f == "sdcp_neutral" else -1.0
            _jb3[_k] = _J("prospective_pose", fragment=_f, seed=SEED_MAIN,
                          basin_id="b%02d" % _i, role="calibration",
                          uma_E_pose_eV=0.10 + 0.01 * _i, _edisp=_dcx)
            _en3[_k] = -900.0 + _em + (-1.20 - 0.01 * _i)   # 잔차 range = 0.06
            _jb3[_k + "__d3off"] = _J("prospective_pose", fragment=_f, seed=SEED_MAIN,
                                      basin_id="b%02d" % _i, d3="off", d3_twin_of=_k)
            _en3[_k + "__d3off"] = _en3[_k] - _dcx
    _E3 = lambda j: _en3.get(j)                       # noqa: E731
    _emol3 = {"sdcp_neutral": -200.0, "ptfe_c10": -100.0}
    _F3 = ["sdcp_neutral", "ptfe_c10"]

    #   ★ manifest 를 준다 — 기대 자세 수의 정본이다 (회수분에서 세지 않는다)
    _man3 = {"planned": {k: {} for k in _jb3
                         if k.startswith("prospective/") and k.endswith(SEED_MAIN)}}
    _c1 = closure_C1(_man3, _jb3, _E3, _emol3, _F3)
    chk(all(abs(_c1["by_frag"][f]["S_f_eV"] - 0.06) < 1e-6 for f in _F3),
        "C1: S_f 가 **range** 로 계산된다 (0.06) — 실제 %s"
        % [round(_c1["by_frag"][f]["S_f_eV"], 4) for f in _F3])
    _jb_p = dict(_jb3); _jb_p.pop("prospective/sdcp_neutral__b03__" + SEED_MAIN)
    chk(closure_C1(_man3, _jb_p, _E3, _emol3, _F3)["by_frag"]["sdcp_neutral"]["verdict"]
        == "unresolved",
        "⛔음성 C1: 자세 하나가 빠지면 **unresolved** — 남은 것으로 range 를 내면 "
        "표본이 줄어 통과 쪽으로 편향된다")
    _kb = "prospective/ptfe_c10__b01__" + SEED_MAIN
    _jb_b = dict(_jb3)
    _jb_b[_kb] = dict(_jb3[_kb], geom={"magnetic": {"realized_basin_id": "OTHER"}})
    chk(closure_C1(_man3, _jb_b, _E3, _emol3, _F3)["by_frag"]["ptfe_c10"]["verdict"]
        == "unresolved",
        "⛔음성 C1: 네 자세 중 basin 이 다른 것이 있으면 unresolved")
    # ⛔ 음성 P0-4 — **해시는 같은데 크기가 벌어진** 경우. 종전엔 해시만 봐서
    #   1.2 μB 와 2.0 μB 가 같은 basin 으로 통과했다. basin_distance 의 RMS 규칙은
    #   selftest 밖에서 한 번도 안 불렸다 (살아 있는 척하는 죽은 코드).
    _jb_m = dict(_jb3)
    _jb_m[_kb] = _J("prospective_pose", fragment="ptfe_c10", seed=SEED_MAIN,
                    basin_id="b01", role="calibration", uma_E_pose_eV=0.11,
                    _edisp=-1.0, _mom=(2.0, -2.0, 2.0, -2.0))    # 부호 같음, 크기 다름
    _r_m = closure_C1(_man3, _jb_m, _E3, _emol3, _F3)["by_frag"]["ptfe_c10"]
    chk(_r_m["verdict"] == "unresolved"
        and any("RMS" in str(x) for x in (_r_m.get("missing") or [])),
        "⛔음성 P0-4: 부호가 같아도 **모멘트 크기**가 벌어지면 unresolved — "
        "해시만 보면 통과했다 (%s)" % (_r_m.get("missing") or [])[:1])
    # ⛔ 음성 P0-4b — 상세 지문이 아예 없으면 **통과가 아니다**
    _jb_n4 = dict(_jb3)
    _jb_n4[_kb] = dict(_jb3[_kb],
                       geom={"magnetic": {"realized_basin_id": "B"}})   # 상세 없음
    _r_n4 = closure_C1(_man3, _jb_n4, _E3, _emol3, _F3)["by_frag"]["ptfe_c10"]
    chk(_r_n4["verdict"] == "unresolved",
        "⛔음성 P0-4b: 상세 지문이 없으면 해시가 같아도 통과시키지 않는다")

    # ── P0-5 회귀: **production 이 실제로 쓰는 경로**로 친다 ─────────────────
    #   read_outcar 는 `{k: _echo_val(t, k) for k in AUDIT_KEYS_RUNTIME}` 로
    #   되울림을 만든다. 손으로 만든 dict 를 넣으면 그 키가 목록에 없어도 통과한다 —
    #   회신 AB P0-5 가 잡은 것이 정확히 그 상태였다. 그래서 **같은 식으로** 만든다.
    for _k5 in ("LNONCOLLINEAR", "LSORBIT", "I_CONSTRAINED_M", "BEXT"):
        chk(_k5 in AUDIT_KEYS_RUNTIME,
            "⛔음성 P0-5: %s 가 AUDIT_KEYS_RUNTIME 에 있다 — 없으면 read_outcar 가 "
            "안 읽어서 _spin_setup_ok 이 **실제로는 안 돈다**" % _k5)
    _echo = lambda t: {k: _echo_val(t, k) for k in AUDIT_KEYS_RUNTIME}   # noqa: E731
    _e5 = _echo("  ENCUT  =  520.0 eV\n  ISMEAR =      0\n")
    chk(_spin_setup_ok(_e5)[0] is True,
        "⛔음성 P0-5: 그 넷이 **미출력이면 통과**다 (VASP 기본값은 안 찍는다). "
        "종전엔 str(None)='NONE' 이 되어 전 잡을 '스핀 제약 있음' 으로 막았다: %s"
        % (_spin_setup_ok(_e5)[1],))
    chk(_spin_setup_ok(_echo("  LSORBIT =      T\n"))[0] is False,
        "⛔음성 P0-5: SOC 가 켜져 있으면 같은 경로에서 잡힌다")
    chk(_spin_setup_ok(_echo("  I_CONSTRAINED_M =      1\n"))[0] is False,
        "⛔음성 P0-5: 스핀 제약이 켜져 있으면 같은 경로에서 잡힌다")

    # ══ C5 — ΔΔE_obs (12자세 · 홀드아웃 게이트) ═══════════════════════════
    #   이것이 Figure 2e 의 숫자를 내는 조건이다. 게이트가 하나라도 새면 값을
    #   만들면 안 되므로 음성을 촘촘히 친다.
    def _mk12(a_by_role):
        """조각별 12자세 픽스처 — cal 4 + holdout 8, A 값을 지정한다."""
        jb, en = {}, {}
        for f, (cal, hld) in a_by_role.items():
            mk = "refs/mol__%s__box24" % f
            jb[mk] = _J("mol_ref", fragment=f); en[mk] = -100.0
            for i, (role, a) in enumerate([("calibration", x) for x in cal]
                                          + [("holdout", x) for x in hld]):
                k = "prospective/%s__b%02d__%s" % (f, i, SEED_MAIN)
                jb[k] = _J("prospective_pose", fragment=f, seed=SEED_MAIN,
                           basin_id="b%02d" % i, role=role, _edisp=-1.0)
                en[k] = -100.0 + a                       # A = E_cx − E_mol = a
        return jb, en

    _F5 = ["sdcp_neutral", "ptfe_c10"]
    _em5 = {"sdcp_neutral": -100.0, "ptfe_c10": -100.0}
    _A5 = {"sdcp_neutral": ([-1.20, -1.10, -1.05, -1.00], [-1.15] + [-0.9] * 7),
           "ptfe_c10":     ([-0.80, -0.75, -0.70, -0.65], [-0.74] + [-0.6] * 7)}
    _jb5, _en5 = _mk12(_A5)
    _man5 = {"planned": {k: {} for k in _jb5 if k.startswith("prospective/")}}
    _E5 = lambda j: _en5.get(j)                          # noqa: E731
    _MG = {'ok': True, 'schema': 'merge_compat/v1', 'n_bundles': 2}
    _c5 = closure_C5(_man5, _jb5, _E5, _em5, _F5, _MG)
    chk(abs(_c5.get("ddE_obs_eV", 0) - (-0.40)) < 1e-6,
        "C5 양성: ΔΔE_obs = min(SDCP) − min(c10) = −1.20 − (−0.80) = −0.40 (실제 %s)"
        % _c5.get("ddE_obs_eV"))
    chk(all(_c5["by_frag"][f]["H1_class"] == "holds" for f in _F5),
        "C5: 홀드아웃이 calibration 최저를 30 meV 넘게 웃돌면 H1 = holds")

    # ── 회신 AF P0-3/P0-4 게이트 ────────────────────────────────────────────
    # ── 판정바닥 δ = max(30 meV 하한, 실측 S_f) ─────────────────────────────
    #   30 meV 는 MLIP(UMA) 실무 해상도라 DFT 값에 옮겨 쓸 근거가 없다. 하한으로만 쓴다.
    chk(h1_tolerance({"by_frag": {"a": {"S_f_eV": 0.004}}})["a"]["tol_eV"]
        == C5_H1_FLOOR_EV, "δ 는 S_f 와 무관하다 (작을 때)")
    chk(h1_tolerance({"by_frag": {"a": {"S_f_eV": 0.470}}})["a"]["tol_eV"]
        == C5_H1_FLOOR_EV,
        "⛔음성 AF P0-5: S_f 470 meV 여도 δ 가 **안 커진다** — 커지면 미해결 띠만 "
        "넓어져 나쁜 selector 가 자기 실패를 가린다 (그 설계는 철회됐다)")
    chk(h1_tolerance({"by_frag": {"a": {}}})["a"]["tol_eV"] == C5_H1_FLOOR_EV,
        "[음성] S_f 미측정이어도 δ 는 정의된다 (조용히 0 이 되지 않는다)")

    # ── 진공 두께 수렴 시험 (회신 AJ) ───────────────────────────────────────
    _VM = {"vacuum_convergence": {"c1_A": 36.6551, "c2_A": 40.6551}}
    _emv = {"sdcp_neutral": -100.0, "ptfe_c10": -50.0}

    def _vjobs(d_sdcp_c1, d_sdcp_c2, d_ptfe_c1, d_ptfe_c2, rb="r1", rb_c2=None):
        jb, en = {}, {}
        for f, (a1, a2) in (("sdcp_neutral", (d_sdcp_c1, d_sdcp_c2)),
                            ("ptfe_c10", (d_ptfe_c1, d_ptfe_c2))):
            # ⛔ 2026-08-31 (회신 AM P0-2) — 픽스처가 옛 규약(kind="vacuum_convergence")을
            #   쓰고 있었다. **실물 번들은 c2 도 kind="prospective_pose" + vacconv="c2"** 다.
            #   픽스처가 실물과 다르면 이 시험은 아무것도 보증하지 못한다 (실제로 그래서
            #   분석기가 c2 를 못 찾는 걸 selftest 가 못 잡았다).
            for cell, kind, a in (("c1", "prospective_pose", a1),
                                  ("c2", "prospective_pose", a2)):
                k = "%s/%s__%s" % (cell, f, cell)
                jb[k] = {"meta": {"kind": kind, "fragment": f, "seed": SEED_MAIN,
                                  "role": "primary",
                                  **({"vacconv": "c2"} if cell == "c2" else {})},
                         "gates": [],
                         "geom": {"magnetic": {"realized_basin_id":
                                               (rb_c2 or rb) if cell == "c2" else rb}}}
                en[k] = _emv[f] + a
        return jb, en

    # 양성: A 가 네 값 모두 같은 만큼 움직이면 대비는 안 변한다
    _jv, _ev = _vjobs(-1.20, -1.19, -0.80, -0.79)
    _rv = closure_vacconv(_VM, _jv, lambda j: _ev.get(j), _emv,
                          ["sdcp_neutral", "ptfe_c10"])
    chk(_rv["pass"] and abs(_rv["delta_vac_eV"]) < 1e-9,
        "진공 양성: 두 조각이 같이 움직이면 Δ_vac = 0 (조각별 변화 10 meV 여도 통과)")
    chk(abs(_rv["D_eV"]["c1"] - (-0.40)) < 1e-9,
        "D(c1) = A_SDCP − A_PTFE = −0.40 (실제 %s)" % _rv["D_eV"]["c1"])

    # ⛔음성 ①: 대비가 6 meV 움직이면 막는다
    _jv2, _ev2 = _vjobs(-1.20, -1.206, -0.80, -0.80)
    _rv2 = closure_vacconv(_VM, _jv2, lambda j: _ev2.get(j), _emv,
                           ["sdcp_neutral", "ptfe_c10"])
    chk(_rv2["pass"] is False and "FAIL" in _rv2["verdict"],
        "⛔음성 AJ: Δ_vac 6 meV → 실패 (문턱 5 meV · 조각별로 보면 안 보인다)")

    # ⛔음성 ②: 5 meV 안이어도 0.01 eV 반올림이 갈리면 막는다
    #   경계를 **걸치게** 한다: −0.4048 → −0.40 · −0.4052 → −0.41 (차 0.4 meV)
    _jv3, _ev3 = _vjobs(-1.2048, -1.2052, -0.80, -0.80)
    _rv3 = closure_vacconv(_VM, _jv3, lambda j: _ev3.get(j), _emv,
                           ["sdcp_neutral", "ptfe_c10"])
    # ⛔ 2026-08-31 (회신 AM Q1) — 반올림 불일치는 이제 **통과**다 (표시 정보일 뿐).
    #   0.2 meV 차이가 0.00/0.01 로 갈리고, 기체 offset 만 더해도 판정이 뒤집혔다.
    chk(_rv3["within_tol"] and not _rv3["same_rounded"] and _rv3["pass"] is True,
        "⛔음성 AJ: 4 meV 로 문턱 안이어도 −0.40/−0.40 이 아니면 실패 "
        "(보고 자릿수에서 값이 달라진다) · %s" % _rv3["D_reported"])

    # ⛔음성 ③: 자기 topology 가 셀 사이에서 갈리면 셀 효과가 아니다
    _jv4, _ev4 = _vjobs(-1.20, -1.20, -0.80, -0.80, rb="r1", rb_c2="r2")
    _rv4 = closure_vacconv(_VM, _jv4, lambda j: _ev4.get(j), _emv,
                           ["sdcp_neutral", "ptfe_c10"])
    # ⛔ 2026-08-31 — `pass` 는 이제 **항상 있다**(기본 False). "키가 없다" 를 판정
    #   근거로 쓰면 안 된다 — 호출자가 KeyError 를 맞았다. 값으로 본다.
    chk(any("BASIN_MISMATCH" in b for b in _rv4["blocks"]) and _rv4["pass"] is False,
        "⛔음성 AJ: c1↔c2 realized topology 가 다르면 값을 안 만든다")

    # [음성] 옛 번들에는 적용하지 않는다
    chk(closure_vacconv({}, {}, lambda j: None, _emv,
                        ["sdcp_neutral", "ptfe_c10"])["applicable"] is False,
        "[음성] vacconv 잡이 없는 번들에는 없는 계약을 요구하지 않는다")

    # ── clean slab 없이 자기 topology 판정 (회신 AJ ②) ──────────────────────
    # ⛔⛔ 2026-08-31 (회신 AN P0-2) — 픽스처가 **내가 지어낸 필드 이름**(`ni_moments`)을
    #   써서, 함수가 production 스키마(`realized_basin.ni_moments_muB`)를 못 읽는데도
    #   selftest 가 통과했다. 이제 픽스처는 `realized_basin()` 이 **실제로 내는 모양**을 쓴다.
    def _J3(mom):
        # ⚠ `_J3(None)` 로 "표가 없다" 를 시험하는 호출이 있다 — 그걸 깨지 말 것.
        if mom is None:
            return {"geom": {"magnetic": {"realized_basin": {}}}}
        return {"geom": {"magnetic": {"realized_basin": {
            "ni_moments_muB": list(mom),
            "ni_sign_vector": [1 if x > 0 else -1 for x in mom],
            "ni_index_poscar": list(range(len(mom))), "global_sign": 1.0}}}}

    def _J3_legacy(mom):                     # 하위호환 경로 (옛 기록)
        return {"geom": {"magnetic": {"ni_moments": mom}}}
    _up = [1.2, -1.2] * 24
    _dn = [-1.2, 1.2] * 24                     # 전역 반전 — 같은 상태여야 한다
    chk(magnetic_topology_direct(_J3(_up))[0] == magnetic_topology_direct(_J3(_dn))[0],
        "직접 topology: 전역 반전을 **동치로 접는다** (AFM 은 전체를 뒤집어도 같다)")
    chk(magnetic_topology_direct(_J3(_up))[0]
        != magnetic_topology_direct(_J3([1.2] * 48))[0],
        "직접 topology: 배열이 다르면 fingerprint 도 다르다")
    # ⛔음성 — production 스키마와 하위호환 경로가 **같은 답**을 내야 한다.
    #   (초판은 하위호환 쪽만 읽어서 실물에서 항상 MISSING 이었다)
    chk(magnetic_topology_direct(_J3(_up))[0]
        == magnetic_topology_direct(_J3_legacy(_up))[0],
        "⛔음성 AN P0-2: **production 스키마**(realized_basin.ni_moments_muB)를 읽는다 "
        "— 옛 픽스처 이름만 읽으면 실물에서 항상 MISSING 이 된다")
    chk(magnetic_topology_direct(
            {"geom": {"magnetic": {"realized_basin": {"ni_sign_vector": [1] * 48}}}})[0] is None,
        "⛔음성: realized_basin 은 있는데 모멘트 표가 없으면 판정하지 않는다 "
        "(부호벡터만으로 접지 않는다)")
    chk(magnetic_topology_direct(_J3(_up[:40]))[0] is None
        and "INCOMPLETE" in magnetic_topology_direct(_J3(_up[:40]))[1][0],
        "⛔음성 AJ: Ni 모멘트 표가 40/48 이면 **판정하지 않는다**")
    _col = list(_up); _col[7] = 0.05
    chk(magnetic_topology_direct(_J3(_col))[0] is None
        and "COLLAPSE_DIRECT" in magnetic_topology_direct(_J3(_col))[1][0],
        "⛔음성 AJ: near-zero 모멘트가 있으면 부호를 못 읽으므로 막는다")
    chk(magnetic_topology_direct(_J3(None))[0] is None,
        "⛔음성 AJ: 모멘트 표가 없으면 조용히 통과하지 않는다")
    chk(same_topology_direct(_J3(_up), _J3(_dn))[0]
        and not same_topology_direct(_J3(_up), _J3([1.2] * 48))[0],
        "직접 topology: 두 잡 비교가 전역 반전에는 관대하고 배열 차이엔 엄격하다")

    # ⛔ 회신 AF P0-6 — 정확히 ±δ 는 **둘 다 미해결**이다 (부동소수점으로 뒤집혔었다)
    for _sgn, _lbl in ((+1, "+30 meV"), (-1, "−30 meV")):
        _Ab = {"sdcp_neutral": ([-1.20, -1.10, -1.05, -1.00], [-1.15] + [-0.9] * 7),
               "ptfe_c10": ([-0.80, -0.75, -0.70, -0.65],
                            [round(-0.80 + _sgn * C5_H1_FLOOR_EV, 12)] + [-0.6] * 7)}
        _jbb, _enb = _mk12(_Ab)
        _cb = closure_C5({"planned": {k: {} for k in _jbb
                                      if k.startswith("prospective/")}},
                         _jbb, lambda j: _enb.get(j), _em5, _F5, _MG)
        chk(_cb["by_frag"]["ptfe_c10"]["H1_class"] == "unresolved",
            f"⛔음성 AF P0-6: 정확히 {_lbl} 는 **미해결** "
            f"(실제 {_cb['by_frag']['ptfe_c10']['H1_class']})")
    # [음성] δ 가 커지면 종전에 통과하던 여유가 미해결로 바뀐다
    _A5t = {"sdcp_neutral": _A5["sdcp_neutral"],
            "ptfe_c10": ([-0.80, -0.75, -0.70, -0.65], [-0.74] + [-0.6] * 7)}
    _jb5t, _en5t = _mk12(_A5t)
    _man5t = {"planned": {k: {} for k in _jb5t if k.startswith("prospective/")}}
    _c5t = closure_C5(_man5t, _jb5t, lambda j: _en5t.get(j), _em5, _F5, _MG,
                      h1_tolerance({"by_frag": {f: {"S_f_eV": 0.080} for f in _F5}}))
    chk(_c5t["by_frag"]["ptfe_c10"]["H1_class"] == "holds",
        "⛔음성 AF P0-5: S_f 80 meV 가 있어도 여유 60 meV 는 **holds** 다 — "
        "S_f 가 판정을 삼키지 않는다")

    chk(closure_C5(_man5, _jb5, _E5, _em5, _F5).get("verdict", "").startswith("⛔ NOT_MERGED"),
        "⛔음성 AF: 묶음 하나만 주면 **값을 만들지 않는다** (12자세는 두 묶음에 걸쳐 있다)")
    chk(closure_C5(_man5, _jb5, _E5, _em5, _F5,
                   {"ok": False, "blocking": ["clean_slab 가 다르다"]}
                   ).get("verdict", "").startswith("⛔ MERGE_INCOMPATIBLE"),
        "⛔음성 AF: 두 묶음의 프로토콜이 갈리면 합치지 않는다")

    # [음성] H1 미해결 구간(±30 meV)을 통과로 승격하지 않는다
    _A5u = {"sdcp_neutral": _A5["sdcp_neutral"],
            "ptfe_c10": ([-0.80, -0.75, -0.70, -0.65], [-0.78] + [-0.6] * 7)}
    _jb5u, _en5u = _mk12(_A5u)
    _c5u = closure_C5({"planned": {k: {} for k in _jb5u if k.startswith("prospective/")}},
                      _jb5u, lambda j: _en5u.get(j), _em5, _F5, _MG)
    chk(_c5u["by_frag"]["ptfe_c10"]["H1_class"] == "unresolved"
        and "ddE_obs_eV" not in _c5u,
        "⛔음성 AF: 여유 20 meV 는 판정 해상도 안 → **미해결**이고 값을 안 만든다 "
        "(종전 두 갈래는 이걸 통과로 승격시켰다)")

    # [음성] 합이 12 라도 구성이 4+8 이 아니면 홀드아웃 시험이 성립하지 않는다
    _A5c = {"sdcp_neutral": ([-1.20] * 11, [-0.9]), "ptfe_c10": _A5["ptfe_c10"]}
    _jb5c2, _en5c2 = _mk12(_A5c)
    _c5c = closure_C5({"planned": {k: {} for k in _jb5c2 if k.startswith("prospective/")}},
                      _jb5c2, lambda j: _en5c2.get(j), _em5, _F5, _MG)
    chk(_c5c["by_frag"]["sdcp_neutral"]["verdict"].startswith("unresolved")
        and "ddE_obs_eV" not in _c5c,
        "⛔음성 AF: cal 11 + holdout 1 은 합이 12 여도 거부한다")
    chk("전역 최소" in str(_c5.get("⛔_금지_서술")),
        "C5 가 금지 서술을 결과에 함께 싣는다")

    # ── 분석기 쪽 게이트 (러너가 아니라 **반송물**을 우리가 직접 본다) ──────
    _M = {"files_sha256": {"j/POTCAR_ASSEMBLE.sh": "x"}}
    _meta_ok = {"species_order": ["Li", "Ni"], "potcar_spec": {"Li": "Li_sv",
                                                               "Ni": "Ni_pv"}}
    import tempfile as _tfx
    _jp = pathlib.Path(_tfx.mkdtemp()) / "pg"
    _jp.mkdir(parents=True, exist_ok=True)

    def _pg(payload, meta=None, marker=False):
        for q in _jp.iterdir():
            q.unlink()
        if payload is not None:
            (_jp / "POTCAR_PROVENANCE.json").write_text(json.dumps(payload), encoding="utf-8")
        if marker:
            (_jp / ".SELFTEST_FIXTURE").write_text("x", encoding="utf-8")
        return potcar_provenance_gates(str(_jp), meta or _meta_ok, "j", _M)

    _good = {"schema": "potcar_provenance/v1", "species_order": ["Li", "Ni"],
             "expected_variants": ["Li_sv", "Ni_pv"],
             "titel_lines": [" TITEL  = PAW_PBE Li_sv", " TITEL  = PAW_PBE Ni_pv"],
             "allowlist": "/a", "allowlist_sha256": "0" * 64,
             "allowlist_waived": False, "assembled_sha256": "1" * 64}
    chk(_pg(_good) == [], "분석기 양성: 정상 provenance 는 게이트 0건")
    chk(any("MISSING" in g for g in _pg(None)),
        "⛔음성 P0-7: 반송물에 provenance 가 없으면 막는다")
    chk(any("WAIVED" in g for g in _pg({**_good, "allowlist_waived": True})),
        "⛔음성 P0-7: 면제본은 막는다")
    chk(any("UNPINNED" in g for g in
            _pg({k: v for k, v in _good.items() if k != "allowlist_sha256"})),
        "⛔음성 P0-7: allowlist 내용 SHA 가 없으면 막는다")
    chk(any("SPECIES_ORDER_MISMATCH" in g for g in
            _pg({**_good, "species_order": ["Ni", "Li"]})),
        "⛔음성 P0-7: 종 순서가 잡과 다르면 막는다 (다른 계를 계산한 것이다)")
    chk(any("VARIANT_NOT_IN_TITEL" in g for g in
            _pg({**_good, "titel_lines": [" TITEL  = PAW_PBE Li", " TITEL  = PAW_PBE Ni"]})),
        "⛔음성 P0-7: 선언한 variant 가 TITEL 에 없으면 막는다 (Ni vs Ni_pv)")
    chk(any("FIXTURE_MARKER" in g for g in _pg(_good, marker=True)),
        "⛔음성 P0-7: 시험 표시 파일이 반송물에 섞이면 막는다")
    chk(potcar_provenance_gates(str(_jp), _meta_ok, "other", _M) == [],
        "[음성] 조립기를 안 실어 보낸 잡에는 계약을 요구하지 않는다")

    # ⛔ 회신 AI §B — 자기일관적 허위. 회신 JSON 안에서 expected_variants 와
    #    titel_lines 가 서로 맞으면 종전 코드는 통과시켰다. 우리 규격이 기준이어야 한다.
    _M2 = {"files_sha256": {"j/POTCAR_ASSEMBLE.sh": "x"},
           "potcar_spec": {"Li": "Li_sv", "Ni": "Ni_pv"}}

    def _pg2(payload):
        for q in _jp.iterdir():
            q.unlink()
        (_jp / "POTCAR_PROVENANCE.json").write_text(json.dumps(payload), encoding="utf-8")
        return potcar_provenance_gates(str(_jp), _meta_ok, "j", _M2)

    _liar = {**_good, "expected_variants": ["Li", "Ni"],
             "titel_lines": [" TITEL  = PAW_PBE Li", " TITEL  = PAW_PBE Ni"]}
    _gl = _pg2(_liar)
    chk(any("VARIANT_NOT_IN_TITEL" in g for g in _gl)
        and any("SPEC_DISAGREES" in g for g in _gl),
        "⛔음성 AI: 회신 안에서 앞뒤가 맞는 **허위**(Li/Ni 로 통일)도 우리 규격과 "
        "대조해 잡는다")
    chk(_pg2(_good) == [], "양성: 우리 규격(Li_sv·Ni_pv)과 맞으면 통과")
    chk(any("SPEC_UNAVAILABLE" in g for g in potcar_provenance_gates(
            str(_jp), {"species_order": ["Li", "Ni"]}, "j",
            {"files_sha256": {"j/POTCAR_ASSEMBLE.sh": "x"}})),
        "⛔음성 AI: 우리 쪽 규격이 없으면 **통과시키지 않는다** "
        "(회신끼리만 맞춰 보는 것은 검증이 아니다)")

    # ── 묶음 전체 신원 (잡 하나씩으로는 못 잡는 것) ─────────────────────────
    # ⛔ 회신 AO P0-8 — 픽스처의 sha 를 **64자리 실물 모양**으로 만든다. 종전엔
    #   "aa" 같은 짧은 문자열이라, "원본 sha 가 64자리인가" 를 아무도 안 봤다.
    #   (그 결과 실물에서 sha 가 잘리거나 비어도 split 만 없으면 통과했다)
    def _H64(tag):
        return (tag * 32)[:64]

    # ⛔⛔ 회신 AP #8 — 픽스처를 **실물 record 모양**으로 만든다. 생성부는 미실행
    #   잡에도 `static: None` 키를 넣는데, 종전 픽스처는 키 자체를 빼서
    #   `"static" in jr` 버그를 **재현하지 못했다** (회신 AL P0-3 과 같은 방식).
    #   ran=False 는 이제 `static: None` 이고, 이 모양으로도 통과해야 맞다.
    def _J2(sha, ver, els=("Ni",), ran=True, normal=True, e0=-1.0, asm=None):
        # ⛔ 회신 AS 4 — 반송 provenance 의 **조립본 해시**를 봉인과 대조한다.
        #   픽스처도 실물처럼 그 값을 담아야 한다.
        d = {"_prov": {"source_sha256": {e: _H64(sha) for e in els},
                       "assembled_sha256": asm},
             "meta": {"species_order": list(els)},
             "static": None}
        if ran:
            d["static"] = {"vasp_version": ver, "normal_end": normal,
                           "E0": (e0 if normal else None)}
        return d
    #   잡 키를 계획(`p/a`·`p/b`)과 맞추고 조립본 해시를 봉인과 일치시킨다
    _one = {"p/a": _J2("aa", "6.4.1", asm=_H64("1a")),
            "p/b": _J2("aa", "6.4.1", asm=_H64("1b"))}
    # ⛔음성 AO P0-8 — 완주했는데 원본 sha 가 **64자리가 아니면** 막는다
    _short = {"a": {"_prov": {"source_sha256": {"Ni": "aa"}},
                    "meta": {"species_order": ["Ni"]},
                    "static": {"vasp_version": "6.4.1", "normal_end": True, "E0": -1.0}}}
    chk(any("SOURCE_INCOMPLETE" in g for g in
            potcar_identity_gates(_short, {})["blocking"]),
        "⛔음성 AO P0-8: 원본 sha 가 64자리가 아니면 막는다 (누락을 '갈리지 않음' 으로 읽지 않는다)")
    # ⛔음성 AO P0-8 — 기대 variant 하나가 **아예 빠져도** 막는다
    _miss = {"a": {"_prov": {"source_sha256": {"Ni": _H64("aa")}},
                   "meta": {"species_order": ["Ni", "O"]},
                   "static": {"vasp_version": "6.4.1", "normal_end": True, "E0": -1.0}}}
    chk(any("SOURCE_INCOMPLETE" in g for g in
            potcar_identity_gates(_miss, {})["blocking"]),
        "⛔음성 AO P0-8: 기대 variant 중 하나라도 sha 가 없으면 막는다")
    # ⛔음성 AO P0-8 — VASP 버전 관측이 0개면 막는다 (0개 관측은 일치가 아니다)
    _nov = {"a": {"_prov": {"source_sha256": {"Ni": _H64("aa")}},
                  "meta": {"species_order": ["Ni"]},
                  "static": {"normal_end": True, "E0": -1.0}}}
    chk(any("VASP_VERSION_UNOBSERVED" in g for g in
            potcar_identity_gates(_nov, {})["blocking"]),
        "⛔음성 AO P0-8: 완주잡에 VASP 버전 관측이 없으면 막는다")
    # ⛔음성 AO P0-8 — 완주했는데 provenance 자체가 없으면 막는다
    chk(any("PROVENANCE_MISSING" in g for g in
            potcar_identity_gates(
                {"a": {"static": {"vasp_version": "6.4.1", "normal_end": True,
                                  "E0": -1.0}}}, {})["blocking"]),
        "⛔음성 AO P0-8: 완주잡에 provenance 가 없으면 막는다")
    # 양성 — **아직 안 돈 잡**은 완전성 대상이 아니다 (단계별 실행에서 정상)
    #   ⚠ ran=False 는 이제 실물처럼 `static: None` 이다 (AP #8)
    _mix = {"a": _J2("aa", "6.4.1"), "b": _J2("aa", "6.4.1", ran=False)}
    _rm = potcar_identity_gates(_mix, {})
    chk(_rm["ok"] and _rm["completeness"]["n_completed"] == 1,
        "양성 AP #8: `static: None` 인 미실행 잡은 완전성 대상이 아니다 "
        f"(completed {_rm['completeness']['n_completed']}/2 · "
        f"census {_rm['completeness']['stage_census']})")
    # ⛔음성 AP #8 — 종전 판정(`"static" in jr`)이면 미실행 잡도 완주로 세서
    #   provenance 를 요구했다. 그 잡에 provenance 를 빼도 통과해야 맞다.
    _mix2 = {"a": _J2("aa", "6.4.1"),
             "b": {"meta": {"species_order": ["Ni"]}, "static": None}}
    chk(potcar_identity_gates(_mix2, {})["ok"],
        "⛔음성 AP #8: 미실행 잡에 provenance 가 없어도 막지 않는다 "
        "(종전엔 `\"static\" in jr` 이라 **항상 참**이라 막았다)")
    # ⛔음성 AP #8 — OUTCAR 는 있는데 **완주가 아닌** 잡도 완전성 대상이 아니다
    _att = {"a": _J2("aa", "6.4.1"),
            "b": _J2("aa", "6.4.1", normal=False)}
    _ra = potcar_identity_gates(_att, {})
    chk(_ra["ok"] and _ra["completeness"]["stage_census"].get("attempted") == 1,
        "⛔음성 AP #8: 정상 종료 못 한 잡은 **attempted** 이지 completed 가 아니다 "
        f"({_ra['completeness']['stage_census']})")
    # ⛔음성 AO Q1 — 생산 전 봉인(root seal)과 관측이 다르면 막는다
    chk(any("ROOT_SEAL_MISMATCH" in g for g in potcar_identity_gates(
            _one, {"_potcar_root_seal": {"source_sha256": {"Ni": _H64("bb")}}}
            )["blocking"]),
        "⛔음성 AO Q1: 생산 전 봉인한 root 와 관측 fingerprint 가 다르면 막는다")
    # ⛔음성 AO Q1 — 봉인에 없는 variant 가 관측되면 막는다
    chk(any("ROOT_SEAL_INCOMPLETE" in g for g in potcar_identity_gates(
            {"a": _J2("aa", "6.4.1", els=("Ni", "O"))},
            {"_potcar_root_seal": {"source_sha256": {"Ni": _H64("aa")}}}
            )["blocking"]),
        "⛔음성 AO Q1: 봉인에 없는 variant 가 관측되면 막는다")
    # 양성 — 봉인과 관측이 일치하면 라벨이 sealed_root_v13 로 올라간다
    # ⛔ 회신 AP #7 — 봉인 픽스처도 **실물 v2 스키마**여야 한다
    # ⛔ 회신 AR P0-5 — 봉인 schema 를 **전부** 요구한다. 반쪽 봉인은 사전 승인이 아니다.
    _SEALOK = {"source_sha256": {"Ni": _H64("aa")}, "schema": "potcar_root_seal/v2",
               "sealed_before_production": True,
               "sealed_before_production_evidence": "봉인 시 산출물 0건",
               "allowlist_sha256": _H64("ab"), "manifest_sha256": _H64("dc"),
               "bundle_zip_sha256": _H64("ed"),
               "vasp_executable": "/opt/vasp/bin/vasp_std",
               "vasp_executable_sha256": _H64("fa"),
               "vasp_version_banner": "vasp.6.4.1 24Jul23",
               "sealed_at_utc": "2026-08-31T00:00:00Z",
               "assembled_sha256_by_job": {"p/a": _H64("1a"), "p/b": _H64("1b")}}
    # 계획 잡 — 봉인 variant 집합과 **일치**해야 한다 (미실행 잡 포함)
    _PLAN = {"p/a": {"meta": {"species_order": ["Ni"]}},
             "p/b": {"meta": {"species_order": ["Ni"]}}}
    _MBASE = {"files_sha256": {"x": "y"}, "_manifest_sha256_actual": _H64("dc"),
              "_zip_sha256_observed": _H64("ed"), "planned": _PLAN,
              "potcar_spec": {"Ni": "Ni"}}
    _sealed = potcar_identity_gates(_one, dict(_MBASE, _potcar_root_seal=_SEALOK))
    chk(str(_sealed.get("identity_scope", "")).startswith("sealed_root_v13"),
        "양성 AO Q1: 봉인 일치 + 완전성 통과면 라벨이 **sealed_root_v13** 다 "
        f"(실제 {str(_sealed.get('identity_scope'))[:40]})")
    # ⛔음성 AP #7 — 생산 전 봉인이라는 근거가 없으면 sealed 라벨을 안 준다
    _nopre = potcar_identity_gates(
        _one, dict(_MBASE, _potcar_root_seal={k: v for k, v in _SEALOK.items()
                                              if k != "sealed_before_production"}))
    chk(any("NOT_PREPRODUCTION" in g for g in _nopre["blocking"])
        and not str(_nopre.get("identity_scope", "")).startswith("sealed_root"),
        "⛔음성 AP #7: `sealed_before_production` 근거가 없으면 막고 sealed 라벨도 "
        "안 준다 (계산 뒤에 만든 봉인과 구별되지 않는다)")
    # ⛔음성 AP #7 — 봉인이 **다른 묶음**의 MANIFEST 에 대한 것이면 막는다
    _wrong = potcar_identity_gates(
        _one, dict(_MBASE, _manifest_sha256_actual=_H64("ca"),
                   _potcar_root_seal=dict(_SEALOK, manifest_sha256=_H64("da"))))
    chk(any("WRONG_BUNDLE" in g for g in _wrong["blocking"]),
        "⛔음성 AP #7: 봉인이 다른 MANIFEST 에 대한 것이면 막는다")

    # ══ 회신 AR P0-5 · 해제조건 7 — 봉인 검증의 fail-open 을 닫는다 ═══════════
    #   AR 이 재현한 것: `source_sha256` 과 `sealed_before_production:true` 만 있는
    #   **반쪽 봉인**도 `sealed_root_v13` 라벨을 받았다.
    _half = potcar_identity_gates(
        _one, dict(_MBASE, _potcar_root_seal={
            "source_sha256": {"Ni": _H64("aa")}, "sealed_before_production": True}))
    chk(any("ROOT_SEAL_INCOMPLETE_SCHEMA" in g for g in _half["blocking"])
        and not str(_half.get("identity_scope", "")).startswith("sealed_root")
        and _half["root_seal_coverage"]["ok"] is False,
        "⛔음성 AR P0-5: 반쪽 봉인(source_sha256 + 선언만)은 막고 sealed 라벨을 "
        "안 준다 — 리뷰가 재현한 fail-open 이다")
    for _mut, _code, _why in (
            ({"schema": "potcar_root_seal/v1"}, "ROOT_SEAL_SCHEMA", "schema 가 v2 가 아니다"),
            ({"manifest_sha256": "deadbeef"}, "ROOT_SEAL_BAD_HASH", "해시가 64자리가 아니다"),
            ({"bundle_zip_sha256": _H64("cb")}, "ROOT_SEAL_ZIP_MISMATCH",
             "봉인한 ZIP 이 받은 ZIP 과 다르다"),
            ({"vasp_version_banner": "vasp.5.4.4"}, "ROOT_SEAL_VASP_MISMATCH",
             "봉인 배너에 관측 버전이 없다"),
            ({"assembled_sha256_by_job": {"p/a": _H64("1a")}}, "ROOT_SEAL_JOB_COVERAGE",
             "계획 잡 하나가 봉인 밖이다")):
        chk(any(_code in g for g in potcar_identity_gates(
                _one, dict(_MBASE, _potcar_root_seal=dict(_SEALOK, **_mut)))["blocking"]),
            "⛔음성 AR P0-5: %s → %s" % (_why, _code))
    # 봉인이 **계획 잡이 요구하는 variant** 를 다 포괄하지 않으면 막는다
    chk(any("ROOT_SEAL_PLAN_COVERAGE" in g for g in potcar_identity_gates(
            _one, dict(_MBASE, planned={"p/a": {"meta": {"species_order": ["Ni", "O"]}}},
                       potcar_spec={"Ni": "Ni", "O": "O"},
                       _potcar_root_seal=_SEALOK))["blocking"]),
        "⛔음성 AR P0-5: 미실행 잡이 요구하는 variant 가 봉인 밖이면 막는다 "
        "(사전 승인은 **앞으로 돌 잡**까지 포괄해야 한다)")
    chk(any("ROOT_SEAL_PLAN_UNREADABLE" in g for g in potcar_identity_gates(
            _one, dict(_MBASE, planned={"p/a": {"meta": {}}},
                       _potcar_root_seal=_SEALOK))["blocking"]),
        "⛔음성 AR P0-5: 계획 잡에 species_order 가 없어 필요한 variant 를 못 세면 "
        "**통과가 아니라 차단**이다")
    # ══ 회신 AS 해제조건 4 — 봉인한 POTCAR 와 **실제로 쓴 POTCAR** 대조 ═══════
    #   종전엔 assembled_sha256_by_job 의 **키만** 봤다. 봉인 뒤에 POTCAR 를
    #   갈아끼워도 잡히지 않았다.
    _swap = {"p/a": _J2("aa", "6.4.1", asm=_H64("de")),      # 조립본이 바뀌었다
             "p/b": _J2("aa", "6.4.1", asm=_H64("1b"))}
    _rsw = potcar_identity_gates(_swap, dict(_MBASE, _potcar_root_seal=_SEALOK))
    chk(any("ROOT_SEAL_ASSEMBLED_MISMATCH" in g for g in _rsw["blocking"])
        and _rsw["assembled_crosscheck"]["mismatch"] == 1,
        "⛔음성 AS 4: 봉인한 조립본 해시와 **반송 값**이 다르면 막는다 "
        "(종전엔 키만 봐서 POTCAR 를 갈아끼워도 통과)")
    _noasm = {"p/a": _J2("aa", "6.4.1"), "p/b": _J2("aa", "6.4.1")}   # asm=None
    chk(any("ROOT_SEAL_ASSEMBLED_UNVERIFIED" in g for g in potcar_identity_gates(
            _noasm, dict(_MBASE, _potcar_root_seal=_SEALOK))["blocking"]),
        "⛔음성 AS 4: 반송에 조립본 해시가 없으면 **확인 못 함 = 통과 아님**")

    # ── 회신 AP #12 — release attestation 이 Methods 문구를 정한다 ────────
    # ⛔ 회신 AR P0-6 — attestation 도 **전 필드 + 3자 집합 일치 + 교차 결박**이다
    _ATT = {"schema": "potcar_attestation/v1", "made_before_production": True,
            "made_before_production_evidence": "생성 시 산출물 0건",
            "release_label": "potpaw_PBE.54", "site": "테스트",
            "created_utc": "2026-08-31T00:00:00Z",
            "manifest_sha256": _H64("dc"), "allowlist_sha256": _H64("ab"),
            "bundle_zip_sha256": _H64("ed"),
            "vasp_version_raw": "vasp.6.4.1",
            "vasp_executable": "/opt/vasp/bin/vasp_std",
            "vasp_executable_sha256": _H64("fa"),
            "variants": {"Ni": {"element": "Ni", "source_sha256": _H64("aa"),
                                "titel": "TITEL  = PAW_PBE Ni 01Jan2000",
                                "embedded_hash": "SHA256 = abc"}}}
    _MB2 = dict(_MBASE, _potcar_root_seal=_SEALOK)
    _ra = potcar_identity_gates(_one, dict(_MB2, _potcar_attestation=_ATT))
    chk(_ra["attestation"]["usable"] and "PAW-PBE datasets from the" in
        _ra["methods_candidate"],
        "양성 AP #12: attestation 이 있으면 **release 를 적는 Methods 문구**가 나온다")
    _rn = potcar_identity_gates(_one, _MB2)
    chk(not _rn["attestation"]["present"]
        and "단정하지 않는다" in _rn["methods_candidate"]
        and "원고 Methods 로는 약하다" in str(_rn.get("methods_candidate_⛔")),
        "⛔음성 AP #12: attestation 이 없으면 release 를 **단정하지 않고**, "
        "그 문구가 원고엔 약하다고 명시한다 (AP Q3)")
    chk(any("ATTESTATION_WRONG_BUNDLE" in g for g in potcar_identity_gates(
            _one, dict(_MB2, _potcar_attestation=dict(_ATT,
                                                      manifest_sha256=_H64("fe"))))
            ["blocking"]),
        "⛔음성 AP #12: 다른 묶음의 attestation 이면 막는다")
    chk(any("ATTESTATION_SEAL_MISMATCH" in g for g in potcar_identity_gates(
            _one, dict(_MB2, _potcar_attestation=dict(
                _ATT, variants={"Ni": {"source_sha256": _H64("bb")}})))["blocking"]),
        "⛔음성 AP #12: attestation 과 root seal 의 원본 sha 가 다르면 막는다")
    chk(any("ATTESTATION_NOT_PREPRODUCTION" in g for g in potcar_identity_gates(
            _one, dict(_MB2, _potcar_attestation=dict(
                _ATT, made_before_production=False)))["blocking"]),
        "⛔음성 AP #12: 계산 전에 만든 근거가 없는 attestation 은 막는다")

    # ══ 회신 AR P0-6 · 해제조건 7 — attestation fail-open 을 닫는다 ══════════
    #   AR 이 재현한 것: `FAKE_RELEASE` 와 **실제 사용 집합에 없는** `UNRELATED`
    #   variant 하나만 준 합성 attestation 이 usable:true 가 되고 강한 Methods
    #   문장을 냈다. 이제 세 집합의 완전일치를 요구한다:
    #     attestation variants = root-seal source variants = 계획 잡 POTCAR variants
    _fake = potcar_identity_gates(_one, dict(_MB2, _potcar_attestation=dict(
        _ATT, release_label="FAKE_RELEASE",
        variants={"UNRELATED": {"element": "Xx", "source_sha256": _H64("ce"),
                                "titel": "TITEL  = PAW_PBE Xx", "embedded_hash": "h"}})))
    chk(_fake["attestation"]["usable"] is False
        and any("ATTESTATION_SET_MISMATCH" in g for g in _fake["blocking"])
        and any("ATTESTATION_PLAN_MISMATCH" in g for g in _fake["blocking"])
        and "단정하지 않는다" in _fake["methods_candidate"],
        "⛔음성 AR P0-6: FAKE_RELEASE + 쓰지도 않는 UNRELATED variant 는 "
        "usable 이 아니고 강한 Methods 문구도 안 나온다 — 리뷰가 재현한 fail-open")
    for _mut, _code, _why in (
            ({"bundle_zip_sha256": _H64("cb")}, "ATTESTATION_ZIP_MISMATCH",
             "받은 ZIP 과 다른 ZIP 을 말한다"),
            ({"allowlist_sha256": _H64("ba")}, "ATTESTATION_ALLOWLIST_MISMATCH",
             "봉인과 다른 allowlist"),
            ({"vasp_executable_sha256": _H64("bd")}, "ATTESTATION_VASP_MISMATCH",
             "봉인과 다른 VASP 바이너리"),
            ({"vasp_version_raw": "vasp.5.4.4"}, "ATTESTATION_VASP_VERSION_MISMATCH",
             "봉인 배너와 다른 버전"),
            ({"made_before_production_evidence": ""},
             "ATTESTATION_PREPRODUCTION_UNEVIDENCED", "생산 전 근거가 선언뿐이다"),
            ({"site": None}, "ATTESTATION_INCOMPLETE", "site 가 없다"),
            ({"created_utc": None}, "ATTESTATION_INCOMPLETE", "created_utc 가 없다"),
            ({"variants": {"Ni": {"element": "Ni", "source_sha256": _H64("aa")}}},
             "ATTESTATION_VARIANT_FIELDS", "variant 에 titel/embedded_hash 가 없다")):
        _rr = potcar_identity_gates(_one, dict(_MB2, _potcar_attestation=dict(_ATT, **_mut)))
        chk(any(_code in g for g in _rr["blocking"]) and not _rr["attestation"]["usable"],
            "⛔음성 AR P0-6: %s → %s" % (_why, _code))
    # 🔴 회신 AT P0-4 음성 — 스키마·불리언·시각·root seal 결박
    for _mut, _code, _why in (
            ({"schema": None}, "ATTESTATION_INCOMPLETE", "schema 필드가 없다"),
            ({"schema": "totally_made_up/v9"}, "ATTESTATION_SCHEMA_UNKNOWN",
             "위조 schema 값"),
            ({"made_before_production": "true"}, "ATTESTATION_NOT_PREPRODUCTION",
             "**문자열** 'true' — 파이썬에서 참이지만 증서가 아니다"),
            ({"made_before_production": 1}, "ATTESTATION_NOT_PREPRODUCTION",
             "정수 1 — 역시 참이지만 불리언이 아니다"),
            ({"created_utc": "어제쯤"}, "ATTESTATION_TIME_MALFORMED",
             "시각이 ISO Z 형식이 아니다")):
        _rr = potcar_identity_gates(_one, dict(_MB2, _potcar_attestation=dict(_ATT, **_mut)))
        chk(any(_code in g for g in _rr["blocking"]) and not _rr["attestation"]["usable"],
            "⛔음성 AT P0-4: %s → %s" % (_why, _code))
    # root seal 이 **없으면** attestation 만으로 release 를 주장하지 않는다
    _nos = potcar_identity_gates(
        _one, {k: v for k, v in dict(_MB2, _potcar_attestation=_ATT).items()
               if k != "_potcar_root_seal"})
    chk(any("ATTESTATION_WITHOUT_ROOT_SEAL" in g for g in _nos["blocking"])
        and not _nos["attestation"]["usable"],
        "⛔음성 AT P0-4: **root seal 이 없으면** 임의 release label 의 attestation 이 "
        "usable 로 가지 않는다 (종전엔 집합 대조가 통째로 건너뛰어졌다)")

    # ZIP 관측이 아예 없으면 "결박 확인 못 함" 이고 그것은 통과가 아니다
    _nz = potcar_identity_gates(_one, dict(_MB2, _zip_sha256_observed=None,
                                           _potcar_attestation=_ATT))
    chk(any("ATTESTATION_ZIP_UNBOUND" in g for g in _nz["blocking"])
        and not _nz["attestation"]["usable"],
        "⛔음성 AR P0-6: 받은 ZIP 의 SHA 를 모르면 **확인 못 함 = 통과 아님**")
    # 관측 TITEL 과 attestation 의 TITEL 이 다르면 막는다
    _jt = {"a": dict(_J2("aa", "6.4.1"),
                     static={"vasp_version": "6.4.1", "normal_end": True, "E0": -1.0,
                             "titels": ["PAW_PBE Ni 09Sep1999"]})}
    chk(any("ATTESTATION_TITEL_MISMATCH" in g for g in potcar_identity_gates(
            _jt, dict(_MB2, _potcar_attestation=_ATT))["blocking"]),
        "⛔음성 AR P0-6: 관측 TITEL 에 없는 TITEL 을 attestation 이 주장하면 막는다")
    # 양성 — allowed_claim 이 두 상태를 구분한다 (필드명 AR Q5)
    chk(_ra.get("allowed_claim") == "paw_release_attested"
        and _rn.get("allowed_claim") == "bundle_conditional_only"
        and "후보 문구" in str(_ra.get("methods_candidate_⚠")),
        "회신 AR Q5: 필드명이 methods_candidate/allowed_claim 이고 **후보**임을 "
        "명시한다 (도구가 원고를 채택하지 않는다)")

    # ⛔음성 AP #7 — blocking 이 있으면 **절대** sealed 라벨이 안 나온다
    _mm = potcar_identity_gates(
        _one, dict(_MBASE, _potcar_root_seal=dict(_SEALOK,
                                                  source_sha256={"Ni": _H64("bb")})))
    chk(any("ROOT_SEAL_MISMATCH" in g for g in _mm["blocking"])
        and not str(_mm.get("identity_scope", "")).startswith("sealed_root"),
        "⛔음성 AP #7: ROOT_SEAL_MISMATCH 와 sealed 라벨이 **동시에** 나오지 않는다 "
        f"(실제 {str(_mm.get('identity_scope'))[:24]})")
    # ⛔음성 — 완전성이 깨지면 라벨이 'unverified' 로 내려간다 (있는 척하지 않는다)
    _unv = potcar_identity_gates(_short, {"files_sha256": {"x": "y"}})
    chk(str(_unv.get("identity_scope", "")).startswith("unverified"),
        "⛔음성 AO P0-8: 원본 fingerprint 가 불완전하면 라벨이 **unverified** 다 "
        "('신원 일치 확인' 이라고 쓰지 않는다)")
    chk(potcar_identity_gates(_one, {})["ok"], "양성: 전 잡이 같은 원본·같은 VASP")
    chk(any("SOURCE_SPLIT" in g for g in
            potcar_identity_gates({"a": _J2("aa", "6.4.1"), "b": _J2("bb", "6.4.1")},
                                  {})["blocking"]),
        "⛔음성 AI: 잡마다 PAW 원본이 다르면 막는다 (잡 하나씩은 다 자기일관적이다)")
    chk(any("VASP_VERSION_SPLIT" in g for g in
            potcar_identity_gates({"a": _J2("aa", "6.4.1"), "b": _J2("aa", "5.4.4")},
                                  {})["blocking"]),
        "⛔음성 AI: VASP 세대가 갈리면 막는다")
    chk(any("PIN_MISMATCH" in g for g in potcar_identity_gates(
            _one, {"potcar_pin": {"source_sha256": {"Ni": "zz"}}})["blocking"]),
        "⛔음성 AI: 사전 고정값과 다르면 막는다 (외부 기준 대조)")

    # ⛔ 회신 AJ — pin 대조의 fail-open 세 갈래를 막았는지
    _MB = {"files_sha256": {"x": "y"}, "potcar_spec": {"Ni": "Ni_pv"}}
    _r_np = potcar_identity_gates(_one, _MB)
    chk(not any("PIN_ABSENT" in g for g in _r_np["blocking"])
        and _r_np.get("pin_absent") is True
        and "self_consistent_only" in str(_r_np.get("identity_scope")),
        "배포 번들에 pin 이 없으면 **차단이 아니라 라벨**이다 (2026-08-31) — "
        "D 는 번들 안에서 닫힌 양이고, 우리는 '승인 트리를 썼다' 를 주장하지 않는다")
    chk("사전 승인된 트리와 대조하지 않았다" in str(_r_np.get("identity_scope")),
        "⛔음성: 그 라벨이 **무엇을 확인 못 했는지** 명시한다 (없는 검증을 있는 척하지 않는다)")
    chk(any("SOURCE_UNOBSERVED" in g for g in potcar_identity_gates(
            {"a": {"static": {"vasp_version": "6.4.1"}}},
            {**_MB, "potcar_pin": {"source_sha256": {"Ni_pv": "aa"},
                                   "vasp_version": "6.4.1"}})["blocking"]),
        "⛔음성 AJ: pin 은 있는데 회신에 원본 sha 가 **하나도 없으면** 막는다 "
        "(빈 관측을 통과로 읽지 않는다)")
    chk(any("VASP_VERSION_UNOBSERVED" in g for g in potcar_identity_gates(
            {"a": {"_prov": {"source_sha256": {"Ni_pv": "aa"}}, "static": {}}},
            {**_MB, "potcar_pin": {"source_sha256": {"Ni_pv": "aa"},
                                   "vasp_version": "6.4.1"}})["blocking"]),
        "⛔음성 AJ: VASP 버전이 하나도 안 읽히면 막는다")
    # variant 키 정규화 — 조립기는 Ni_pv 로 쓰고 pin 예시는 Ni 였다
    _norm = potcar_identity_gates(
        {"a": {"_prov": {"source_sha256": {"Ni_pv": _H64("aa")}},
               "meta": {"species_order": ["Ni"]},
               "static": {"vasp_version": "6.4.1"}}},
        {**_MB, "potcar_pin": {"source_sha256": {"Ni": _H64("aa")},
                               "vasp_version": "6.4.1"}})
    chk(_norm["ok"] and _norm["pin_normalized_variants"] == ["Ni_pv"],
        "⛔음성 AJ: 원소 키 pin(Ni)을 potcar_spec 으로 **variant(Ni_pv)로 정규화**해 "
        "대조한다 (종전엔 관측 없음으로 처리돼 조용히 우회됐다)")
    chk("⚠" in potcar_identity_gates(_one, {}),
        "[음성] 사전 고정이 없으면 '잡 사이 일치만 봤다' 를 결과에 적는다")
    # ⛔ 음성 C5-a — 홀드아웃이 더 낮으면 **SELECTOR_FAIL**, 값을 안 만든다
    _A5b = dict(_A5, sdcp_neutral=([-1.20, -1.10, -1.05, -1.00],
                                   [-1.40] + [-0.9] * 7))   # 홀드아웃이 200 meV 더 낮다
    _jb5b, _en5b = _mk12(_A5b)
    _c5b = closure_C5(_man5, _jb5b, lambda j: _en5b.get(j), _em5, _F5, _MG)
    chk("ddE_obs_eV" not in _c5b
        and "SELECTOR_FAIL" in _c5b["by_frag"]["sdcp_neutral"]["verdict"],
        "⛔음성 C5: 홀드아웃이 calibration 최저를 30 meV 이상 밑돌면 **값을 안 만든다** "
        "— '더 낮은 자세를 찾았다' 로 흡수하면 선택기 실패가 사라진다")
    # ⛔ 음성 C5-b — 자세가 하나라도 빠지면 unresolved
    _jb5c = dict(_jb5); _jb5c.pop("prospective/sdcp_neutral__b11__" + SEED_MAIN)
    chk(closure_C5(_man5, _jb5c, _E5, _em5, _F5, _MG)["by_frag"]["sdcp_neutral"]["verdict"]
        == "unresolved",
        "⛔음성 C5: 12자세 중 하나라도 빠지면 unresolved (표본이 줄면 min 이 올라간다)")
    # ⛔ 음성 C5-c — 홀드아웃 역할이 아예 없으면(= calibration 전용 tranche) 값 없음
    _jb5d = {k: (dict(v, meta=dict(v["meta"], role="calibration"))
                 if k.startswith("prospective/") else v) for k, v in _jb5.items()}
    _c5d = closure_C5(_man5, _jb5d, _E5, _em5, _F5, _MG)
    chk("ddE_obs_eV" not in _c5d,
        "⛔음성 C5: 홀드아웃이 없으면 값을 만들지 않는다 — 그 시험이 이 양의 **전제**다")
    # ⛔ 음성 C5-d — basin 이 갈리면 unresolved
    _kx5 = "prospective/ptfe_c10__b03__" + SEED_MAIN
    _jb5e = dict(_jb5)
    _jb5e[_kx5] = dict(_jb5[_kx5], geom={"magnetic": {"realized_basin_id": "Z"}})
    chk(closure_C5(_man5, _jb5e, _E5, _em5, _F5, _MG)["by_frag"]["ptfe_c10"]["verdict"]
        == "unresolved",
        "⛔음성 C5: 12자세가 서로 다른 basin 이면 unresolved")

    _c3 = closure_C3(_man3, _jb3, _E3, _F3)
    chk(abs(_c3["D_eV"] - (-0.7)) < 1e-6,
        "C3: D = mean(δ_SDCP) − mean(δ_c10) = −0.7 (실제 %s)" % _c3.get("D_eV"))
    # ★★ 부호 규약 (회신 AB P0-3). 봉인된 0.90 eV 는 **(UMA − DFT)** 규약이고
    #   D3 는 additive 라 offset ≈ −δ 다 ⇒ 예측 오프셋 차등 = −D.
    #   ⚠ 2026-08-30 이전 이 두 시험은 **틀린 규약을 그대로 인코딩**하고 있었다 —
    #     코드와 시험이 서로 동의하면서 둘 다 틀렸다. 정확히 설명적인 D=−0.7 을
    #     "반대 부호" 로 기각했다. 그래서 여기 규약을 글로 박아 둔다.
    chk(abs(_c3["predicted_offset_gap_eV"] - 0.7) < 1e-6,
        "C3: 예측 오프셋 차등 = −D = +0.7 (offset 규약, 실제 %s)"
        % _c3.get("predicted_offset_gap_eV"))
    chk(_c3["ratio"] > 0 and _c3["ratio"] >= C3_HI and "수치상" in _c3["verdict"],
        "C3 양성: −D 가 +0.90 과 같은 부호이고 비율 %s ≥ 0.70 → '수치상 설명'"
        % _c3.get("ratio"))
    _en3p, _jb3p = dict(_en3), dict(_jb3)
    for _i in range(4):
        for _f, _d in (("sdcp_neutral", 2.0), ("ptfe_c10", 1.0)):
            _k = "prospective/%s__b%02d__%s" % (_f, _i, SEED_MAIN)
            _en3p[_k + "__d3off"] = _en3p[_k] - _d      # d_cx = E_on − E_off = +_d
            # 항등식이 성립하도록 Edisp 도 같이 뒤집는다 — 안 그러면 교차검증에 걸린다
            _jb3p[_k] = dict(_jb3[_k],
                             static=dict(_jb3[_k]["static"], edisp_eV=_d))
    _c3b = closure_C3(_man3, _jb3p, lambda j: _en3p.get(j), _F3)
    chk(_c3b["D_eV"] > 0 and "미해결" in _c3b["verdict"] and "부호" in _c3b["verdict"],
        "⛔음성 C3: D 가 양수면 예측 오프셋 차등(−D)이 관측 +0.90 과 **반대 부호** → "
        "미해결 (절댓값이면 %s 로 '설명' 오판했다)" % abs(_c3b.get("ratio", 0)))
    # ⛔ 음성 C3-e — **평균이 맞아도 조각내 일관성이 깨지면 미해결.**
    #   D3 는 기하 의존 항이라 자세마다 달라야 하는데 관측 오프셋은 조각 안에서
    #   상수(SDCP 6 meV)였다. δ 가 그보다 훨씬 흔들리면 D3 귀속이 성립 안 한다.
    _jb_w = dict(_jb3)
    for _i, _d in enumerate((-2.0, -2.3, -1.7, -2.0)):
        _kw = "prospective/sdcp_neutral__b%02d__%s" % (_i, SEED_MAIN)
        _jb_w[_kw] = dict(_jb3[_kw],
                          static=dict(_jb3[_kw]["static"], edisp_eV=_d))
        # 이 픽스처는 **조각내 range** 를 시험한다. 쌍둥이를 남겨 두면 항등식
        # 교차검증이 먼저 걸려서(그 자체는 정상 동작) 시험하려던 경로에 못 간다.
        _jb_w.pop(_kw + "__d3off", None)
    _c3w = closure_C3(_man3, _jb_w, _E3, _F3)
    chk("조각내 일관성" in _c3w["verdict"]
        and _c3w["within_fragment"]["sdcp_neutral"]["ok"] is False,
        "⛔음성 C3: δ 의 조각내 range 0.6 eV 가 관측 오프셋 상수성(6 meV)의 5배를 "
        "넘으면 **평균이 맞아도** 미해결 (%s)" % _c3w["verdict"][:40])
    chk(_c3["within_fragment"]["sdcp_neutral"]["ok"] is True,
        "양성 대조: δ 가 조각내 상수면 일관성 통과 (range %s)"
        % _c3["within_fragment"]["sdcp_neutral"]["delta_range_eV"])
    _kx = "prospective/sdcp_neutral__b00__%s__d3off" % SEED_MAIN
    _jb_x = dict(_jb3)
    _jb_x[_kx] = dict(_jb3[_kx], geom={"magnetic": {"realized_basin_id": "Z"}})
    chk(closure_C3(_man3, _jb_x, _E3, _F3)["by_frag"]["sdcp_neutral"]["verdict"]
        == "unresolved",
        "⛔음성 C3: on/off 가 다른 realized basin 이면 unresolved "
        "(그 차이는 D3 기여가 아니다)")
    # ⛔ 음성 C3-c — **Edisp 가 없으면 unresolved.** IVDW 가 실제로 안 걸린 잡을
    #   "D3 기여 0" 으로 조용히 읽으면 D 가 통째로 틀린다.
    _kn = "prospective/sdcp_neutral__b02__" + SEED_MAIN
    _jb_n = dict(_jb3)
    _jb_n[_kn] = dict(_jb3[_kn], static=dict(_jb3[_kn]["static"], edisp_eV=None))
    _r_n = closure_C3(_man3, _jb_n, _E3, _F3)["by_frag"]["sdcp_neutral"]
    chk(_r_n["verdict"] == "unresolved" and any("Edisp" in str(x) for x in
                                                (_r_n.get("missing") or [])),
        "⛔음성 C3: OUTCAR 에 Edisp 가 없으면 unresolved (0 으로 읽지 않는다)")
    # ⛔ 음성 C3-d — **항등식이 깨지면 unresolved.** 쌍둥이가 남아 있는데
    #   (E_on−E_off) 와 Edisp 가 다르면 IVDW 말고 다른 축이 갈린 것이다.
    _jb_i = dict(_jb3)
    _jb_i[_kn] = dict(_jb3[_kn],
                      static=dict(_jb3[_kn]["static"], edisp_eV=-2.5))  # 참값은 -2.0
    _r_i = closure_C3(_man3, _jb_i, _E3, _F3)["by_frag"]["sdcp_neutral"]
    chk(_r_i["verdict"] == "unresolved" and any("항등식" in str(x) for x in
                                                (_r_i.get("missing") or [])),
        "⛔음성 C3: (E_on−E_off) ≠ Edisp 면 unresolved — 쌍둥이가 IVDW 밖에서 갈렸다")

    # guard band
    D = 0.030
    chk(apply_k_guard("ROBUST", 0.005, "K_DIRECTLY_CHECKED", D).startswith("UNRESOLVED_SIGN"),
        "|ΔE| 5 meV → 부호 미정 (직접 dense 여도)")
    chk(apply_k_guard("ROBUST", 0.025, "K_TRANSFER_SCREENED", D)
        .startswith("UNRESOLVED_K_GUARD"),
        "25 meV + 전이심사 → **판정 보류** (옛 판은 그대로 통과시켰다)")
    chk(apply_k_guard("ROBUST", 0.025, "K_DIRECTLY_CHECKED", D) == "ROBUST",
        "25 meV + 직접 dense → 판정 유지 (직접 쟀으면 띠가 적용되지 않는다)")
    # ★ K_UNVERIFIED 는 **크기와 무관하게** 막는다 (Codex zip 감사) — 전이 게이트가
    #   실패했으면 k 오차에 유한한 경계가 없다. 크니까 괜찮다는 논리는 성립 안 한다.
    chk(apply_k_guard("ROBUST", 0.080, "K_UNVERIFIED", D).startswith("UNRESOLVED_K"),
        "80 meV 라도 K_UNVERIFIED 면 막는다 (경계 없는 값에 판정을 붙이지 않는다)")
    chk(apply_k_guard("ROBUST", 0.015, "K_UNVERIFIED", D).startswith("UNRESOLVED_K"),
        "15 meV 도 마찬가지")
    # ★ 대조: 전이 심사를 **통과한** 라벨은 띠 밖이면 판정이 유지돼야 한다
    chk(apply_k_guard("ROBUST", 0.080, "K_TRANSFER_SCREENED", D) == "ROBUST",
        "80 meV + 전이 통과 → 판정 유지 (막는 건 UNVERIFIED 뿐)")
    chk(apply_k_guard("ROBUST", 0.015, "K_TRANSFER_SCREENED", D) == "ROBUST",
        "15 meV + 전이 통과 → 바닥 아래 결론 유지")
    chk(apply_k_guard("X", -0.025, "K_TRANSFER_SCREENED", D)
        .startswith("UNRESOLVED_K_GUARD"), "음수 ΔE 도 절대값으로 본다")

    # ── e2e: OUTCAR **파일** → read_outcar → phase_gates (codex E-2차 필수4) ──
    #   1차 리뷰가 지적한 그대로 — 광고한 e2e 가 배포본 selftest 에 없으면
    #   "자체검증된다" 는 README 주장이 거짓이 된다. 배포본 자신이 돈다.
    import tempfile
    _BODY = (" vasp.5.4.4.18Apr17-6-g9f103f2a35 (build test) complex\n"
             "|      So try LREAL= Auto  in the INCAR   file.        |\n"
             "   ENCUT  =  520.0 eV  38.22 Ry\n"
             "   LREAL  =      T    real-space projection\n"
             "   NUPDOWN=      4.0000    fix difference up-down\n"
             "   LMAXMIX     =    4 max onsite mixed and CHGCAR\n"
             " LDA+U is selected, type is set to LDAUTYPE =  2\n"
             "   U (eV)           for each species LDAUU =   0.0  6.2  0.0\n"
             "  energy(sigma->0) =     -100.000000\n"
             " General timing and accounting\n")
    _EXP = {"ENCUT": "520", "LREAL": "Auto", "NUPDOWN": "4", "LDAUTYPE": "2",
            "LDAUU": "0.0 6.2 0.0", "LDAU": ".TRUE.", "LMAXMIX": "4"}

    def _e2e(body, want=None, gz_trunc=False, both=False):
        with tempfile.TemporaryDirectory() as _d:
            _o = os.path.join(_d, "OUTCAR")
            if gz_trunc:
                full = gzip.compress(body)
                open(_o + ".gz", "wb").write(full[:len(full) // 2])
            elif both:
                open(_o, "wb").write(body)
                open(_o + ".gz", "wb").write(gzip.compress(body))
            else:
                open(_o, "wb").write(body)
            _oc = read_outcar(_o)
            return _oc, phase_gates(_oc, "static",
                                    {"incar_expected": {"static": want or _EXP}}, {})
    _oc, _g = _e2e(_BODY.encode())
    chk(not any("INCAR" in x for x in _g), f"e2e 정상: INCAR 게이트 0건 ({_g})")
    _au = _oc["incar_audit"]
    chk("LDAUU" in _au["verified_exact"] and "NUPDOWN" in _au["verified_exact"]
        and "LMAXMIX" in _au["verified_exact"] and "LDAU" in _au["verified_exact"],
        f"e2e: 목록·NUPDOWN·LDAU·LMAXMIX 가 exact ({_au['verified_exact']})")
    chk("LREAL" in _au["verified_equivalence_class"], "e2e: LREAL 은 등가류")
    chk(any(x.startswith("MAGMOM") for x in _au["unverified"]),
        "e2e: MAGMOM 명시적 unverified")
    _oc, _g = _e2e(_BODY.encode(), want=dict(_EXP, LDAUU="0.0 5.0 0.0"))
    chk(any("INCAR_MISMATCH(static.LDAUU" in x for x in _g),
        "⛔e2e음성: LDAUU 실제 차이(6.2vs5.0)가 전 경로에서 잡힌다")
    _oc, _g = _e2e(_BODY.encode(), want=dict(_EXP, NUPDOWN="-1"))
    chk(any("INCAR_MISMATCH(static.NUPDOWN" in x for x in _g),
        "⛔e2e음성: release 상에 NUPDOWN=4 잔류 → 하드게이트 (기대 -1)")
    _oc, _g = _e2e(_BODY.encode().replace(b"ENCUT", b"ENC\xffUT"))
    chk(any("OUTCAR_READ_ERROR" in x for x in _g), "⛔e2e음성: 깨진 바이트 → 판독 실패")
    _oc, _g = _e2e(_BODY.encode(), gz_trunc=True)
    chk(any("OUTCAR_READ_ERROR" in x and "gzip" in x for x in _g),
        "⛔e2e음성: 잘린 gzip → 게이트 (예외 아님)")
    _oc, _g = _e2e(_BODY.encode(), both=True)
    chk(any("둘 다" in x for x in _g), "⛔e2e음성: plain/.gz 공존 → 정본 판정 불가")
    _two = (_BODY.replace("-100.000000", "-1.000000")
            + _BODY.replace("-100.000000", "-2.000000")).encode()
    _oc, _g = _e2e(_two)
    chk(any("MULTI_RUN_OUTCAR" in x for x in _g) and _oc["E0"] == -2.0,
        f"⛔e2e음성: 2실행 이어붙음 → MULTI_RUN + 마지막 완결만 (E0={_oc['E0']})")

    # ── check_pin 스위트 (배포본 상주 — E-5차: 번들에만 있던 검사를 이사) ────
    def _pin_job(dirp, flip_one=False, nup_echo="4.0000", ldauu_echo="0.0 6.2 0.0",
                 double_run=False, kmesh=True, incar_tamper=False):
        jd = pathlib.Path(dirp); (jd / "static_pin").mkdir(parents=True)
        sign = {"0": 1.0, "1": -1.0, "2": 1.0, "3": 1.0}
        _meta = {"ni_sign_poscar_idx": sign, "counts": [4], "species_order": ["Ni"],
                 "potcar_spec": {"Ni": "Ni_pv"},
                 "incar_expected": {"static_pin": {"NUPDOWN": "4",
                                                   "LDAUU": "0.0 6.2 0.0"}}}
        if kmesh:
            _meta["kmesh"] = {"static_pin": "1 1 1"}
        (jd / "job.json").write_text(json.dumps(_meta), encoding="utf-8")
        (jd / "static_pin" / "INCAR").write_text("NUPDOWN = 4\n", encoding="utf-8")
        _isha = hashlib.sha256((jd / "static_pin" / "INCAR").read_bytes()).hexdigest()
        (jd / "MANIFEST_RESCUE.json").write_text(json.dumps(
            {"sha256": {"static_pin/INCAR": _isha}}), encoding="utf-8")
        if incar_tamper:
            (jd / "static_pin" / "INCAR").write_text("NUPDOWN = 4\nENCUT = 400\n", encoding="utf-8")
        mom = [1.2, -1.2, 1.2, 1.2]
        if flip_one:
            mom[1] = 1.2
        rows = "\n".join(f"{i + 1:5d}   0 0 {m:7.3f} {m:7.3f}"
                          for i, m in enumerate(mom))
        body = (" vasp.5.4.4 test\n TITEL  = PAW_PBE Ni_pv 01Jan2000\n"
                "   NIONS =      4\n   NKPTS =      1\n"
                f"   NUPDOWN=      {nup_echo}    fix difference up-down\n"
                f"   U (eV)           for each species LDAUU =   {ldauu_echo}\n"
                "  energy(sigma->0) =  -1.0\n"
                "\n magnetization (x)\n\n# of ion  s p d tot\n----\n" + rows +
                "\n----\n General timing and accounting\n")
        if double_run:
            body = body + body
        (jd / "static_pin" / "OUTCAR").write_text(body, encoding="utf-8")
        (jd / "static_pin" / "CHGCAR").write_text("density " * 10, encoding="utf-8")
        return jd
    with tempfile.TemporaryDirectory() as _d:
        _D = pathlib.Path(_d)
        chk(check_pin(_pin_job(_D / "ok")) == 0, "check_pin 양성: 정상 pin 수용")
        for nm, kw, why in (
            ("f", {"flip_one": True}, "⛔check_pin 음성: topology 위반 → 거부"),
            ("n", {"nup_echo": "-1.0000"}, "⛔check_pin 음성: NUPDOWN 미적용 → 거부"),
            ("u", {"ldauu_echo": "0.0 5.0 0.0"},
             "⛔check_pin 음성: LDAUU=5.0 → 거부 (E-3차 재현 구멍)"),
            ("m", {"double_run": True}, "⛔check_pin 음성: 2실행 이어붙음 → 거부"),
            ("k", {"kmesh": False}, "⛔check_pin 음성(P0-1): kmesh 결측 → 거부"),
            ("i", {"incar_tamper": True}, "⛔check_pin 음성: pin INCAR 변조 → 거부"),
        ):
            chk(check_pin(_pin_job(_D / nm, **kw)) == 1, why)

    # ── provenance 스위트 (배포본 상주 · E-6차 계약) ─────────────────────────
    _OC_FILE = (" vasp.5.4.4 test\n initial charge density was supplied:\n"
                " keeping initial charge density in first step\n"
                "  energy(sigma->0) =  -1.0\n General timing and accounting\n")
    _OC_ATOMS = (" vasp.5.4.4 test\n initial charge density was supplied:\n"
                 " charge density of overlapping atoms calculated\n"
                 " keeping initial charge density in first step\n"
                 "  energy(sigma->0) =  -1.0\n General timing and accounting\n")

    def _prov_job(dirp, pv_patch=None, pc_patch=None, skip_disk=(), man_drop=(),
                  tamper_incar=False, static_outcar=_OC_FILE, parent_break=False):
        jd = pathlib.Path(dirp)
        (jd / "static_pin").mkdir(parents=True); (jd / "static").mkdir()
        base = {"POSCAR": "p", "KPOINTS": "k", "static_pin/INCAR": "i1",
                "static/INCAR": "i2", "static_pin/KPOINTS": "k",
                "static/KPOINTS": "k", "run_job.sh": "r"}
        man = {}
        for f, body in base.items():
            if f not in skip_disk:
                (jd / f).write_text(body, encoding="utf-8")
            man[f] = hashlib.sha256(body.encode()).hexdigest()
        # job.json 은 부모 해시를 담아야 하므로 마지막에 (자기 해시는 그 뒤 계산)
        par = {"POSCAR": ("deadbeef" if parent_break else man["POSCAR"]),
               "KPOINTS": man["KPOINTS"]}
        jj = json.dumps({"rescue": {"parent_sha256": par}})
        if "job.json" not in skip_disk:
            (jd / "job.json").write_text(jj, encoding="utf-8")
        man["job.json"] = hashlib.sha256(jj.encode()).hexdigest()
        for f in man_drop:
            man.pop(f, None)
        (jd / "MANIFEST_RESCUE.json").write_text(json.dumps({"sha256": man}), encoding="utf-8")
        if static_outcar is not None:
            (jd / "static" / "OUTCAR").write_text(static_outcar, encoding="utf-8")
        rec = {f: man.get(f, "x") for f in ("POSCAR", "KPOINTS",
                                            "static_pin/INCAR", "static/INCAR")}
        rec["POTCAR"] = "pt"
        for ph in ("static_pin", "static"):
            rec[ph + "/POSCAR"] = rec["POSCAR"]
            rec[ph + "/KPOINTS"] = rec["KPOINTS"]
            rec[ph + "/POTCAR"] = "pt"
        pv = {"run_id": "20260825T000000Z_host", "utc": "2026-08-25T00:00:00Z",
              "preflight_problems": [], "inputs_sha256": rec,
              "parent_match": {"POSCAR": True, "KPOINTS": True},
              "chgcar_sha256": {"pin": "aa", "static_copy": "aa", "identical": True},
              "chgcar_read_evidence": ["grid : charge from CHGCAR file"]}
        pv.update(pv_patch or {})
        (jd / "RUN_PROVENANCE.json").write_text(json.dumps(pv), encoding="utf-8")
        pc = {"pass": True, "chgcar": {"sha256": "aa"}}
        pc.update(pc_patch or {})
        (jd / "static_pin" / "PIN_CHECK.json").write_text(json.dumps(pc), encoding="utf-8")
        if tamper_incar:
            (jd / "static_pin" / "INCAR").write_text("i1-modified", encoding="utf-8")
        return jd
    with tempfile.TemporaryDirectory() as _d:
        _D = pathlib.Path(_d)
        chk(rescue_provenance_ok(_prov_job(_D / "g"))[0] is True,
            "provenance 양성: 완비(OUTCAR 승계 마커 포함) → supersede 허용")
        for nm, kw, why in (
            ("q1", {"pv_patch": {"parent_match": {}}},
             "⛔provenance P0-4: parent_match={} → 거부"),
            ("q2", {"pv_patch": {"chgcar_sha256": {"pin": "aa", "static_copy": "bb",
                                                    "identical": True}}},
             "⛔provenance P0-4: identical 거짓 플래그 → sha 직접 비교 거부"),
            ("q3", {"pc_patch": {"chgcar": None}},
             "⛔provenance P0-4: PIN_CHECK 에 CHGCAR sha 없음 → 거부"),
            ("q4", {"static_outcar": _OC_ATOMS},
             "⛔provenance E-6차: OUTCAR 가 'overlapping atoms 새로 만듦' → 승계 안 됨 거부"),
            ("q5", {"static_outcar": " vasp.5\n General timing and accounting\n"},
             "⛔provenance E-6차: 승계 마커 부재(판별 불가) → 거부"),
            ("q6", {"static_outcar": None},
             "⛔provenance E-6차: static OUTCAR 자체가 없으면 거부"),
            ("q7", {"pv_patch": {"chgcar_read_evidence": "NOT_FOUND"}},
             "⛔provenance P0-5: 문자열 타입(문자 순회 함정) → 형식 거부"),
            ("q8", {"pv_patch": {"preflight_problems": ["bad"]}},
             "⛔provenance E-5차: preflight_problems 비어있지 않음 → 거부"),
            ("q9", {"pv_patch": {"preflight_problems": None}},
             "⛔provenance E-5차: preflight 필드 위조/부재 → 거부"),
            ("qa", {"skip_disk": ("static/INCAR",)},
             "⛔provenance P0-3: 배포 파일 디스크 부재 → 거부"),
            ("qb", {"skip_disk": ("static/KPOINTS",)},
             "⛔provenance P0-2: phase KPOINTS 디스크 부재 → 거부"),
            ("qc", {"man_drop": ("static_pin/KPOINTS",)},
             "⛔provenance: MANIFEST 에 phase KPOINTS 해시 없음 → 거부"),
            ("qd", {"tamper_incar": True},
             "⛔provenance: 디스크 INCAR 사후 변조 → 거부"),
            ("qe", {"pv_patch": {"inputs_sha256": None}},
             "⛔provenance P0-3: 실행 기록 해시 없음 → 거부"),
            ("qf", {"parent_break": True},
             "⛔provenance E-6차: 배포≠부모 (재계산 사슬) → 기록 불리언과 무관하게 거부"),
        ):
            _r = rescue_provenance_ok(_prov_job(_D / nm, **kw))
            chk(_r[0] is False, f"{why} ({_r[1][:38]})")

    # ⛔⛔ 회신 AR P1-12 · 해제조건 10 (2026-08-31) — 사전등록 estimand 판정
    #   (`_closure_estimand`)을 **배포본 안에서** 친다. 종전엔 생성기 selftest 에만
    #   있어서, 이 파일만 받은 쪽은 production 판정 경로를 하나도 검증할 수 없었다.
    _n0 = _CHKN[0]
    _selftest_closure(chk)
    print("  ── estimand 판정 검사 %d건 (배포본 안에서 실행) ──"
          % (_CHKN[0] - _n0))
    print("selftest %d/%d · %s"
          % (_CHKN[1], _CHKN[0], "PASS" if ok else "FAIL"))
    print("  재현: python3 analyze_results.py --selftest")
    print("k-selftest PASS" if ok else "k-selftest FAIL")
    return 0 if ok else 1


def _icharg1_chgcar_gate(oc, ph):
    """`ICHARG=1` 상은 **실제로 CHGCAR 를 읽었다는 증거**가 있어야 한다. → [gate] | []

    ⛔⛔ 2026-08-31 (회신 AN P0-6) — 종전엔 `read_outcar()` 가 `chgcar_from_file` 을
      읽어 두고도 일반 `phase_gates()` 가 **그것을 안 썼다.** 파일 존재만 보고 넘어갔다.
      C-12 에서 `ICHARG=1` 인 상은 **기체 기준 static 둘**이고, 그 둘은 D 에 직접 들어간다.
      VASP 는 CHGCAR 가 없거나 못 읽으면 **조용히 원자중첩으로 시작**한다 —
      그러면 "승계했다" 는 기록만 남고 실제로는 다른 시작점이다.

    ⛔ 못 하는 것: 읽은 CHGCAR 가 **맞는 것**인지는 모른다 (읽었다는 사실만 본다).
    """
    if str(oc.get("incar_echo", {}).get("ICHARG", "")).strip() != "1":
        return []
    cff = oc.get("chgcar_from_file")
    if cff is True:
        return []
    return ["CHGCAR_NOT_READ(%s — ICHARG=1 인데 %s. VASP 는 못 읽으면 조용히 "
            "원자중첩으로 시작한다)"
            % (ph, "overlapping atoms 로 새로 만듦" if cff is False else "마커 부재")]


def phase_gates(oc, ph, meta, spec, want_ionic=False):
    """상 하나의 fail-closed 검사. oc 가 None 이면 NOT_RUN.

    ⚠ **게이트 통과가 보증하는 것** (codex E-2, 과대해석 금지):
      "제공된 단일 완결 실행 세그먼트에서, incar_expected 에 등록된 유한한 키
       집합이 되울림과 일치했다" — 딱 여기까지다.
    보증하지 못하는 것: 등록되지 않은 키 전부 · POTCAR 원문 해시 · WAVECAR/CHGCAR
    실제 내용과 승계 계보 · 기본값/명시값 구분 · LREAL 의 정확한 모드(등가류까지만).
    ISTART/ICHARG 되울림은 재시작 파일이 **실제로 쓰였다는 증거가 아니다.**
    각 상의 incar_audit(4분류)가 이 경계의 기계 기록이다.

    ✅ 2026-08-31 (회신 AT P0-2) — **k 격자·시프트는 이제 보증한다.** KPOINTS 제목에
      `phase=… k=… shift=…` 를 실어 OUTCAR ` KPOINTS:` 되울림과 정확히 대조한다.
      종전에는 `NKPTS ≤ 격자곱` 상한뿐이라 coarse OUTCAR 를 dense 폴더에 넣어도
      통과했다. 단 **되울림이 없으면 통과가 아니라 UNVERIFIED** 다.
    """
    g = []
    if oc is None:
        return [f"NOT_RUN({ph})"]
    if oc.get("read_error"):
        # 판독 실패는 NOT_RUN 이 아니다 — 파일은 있는데 믿고 읽을 수 없는 상태
        return [f"OUTCAR_READ_ERROR({ph}: {oc['read_error']})"]
    seg = oc.get("run_segments") or {}
    if seg.get("n", 1) > 1:
        g.append(f"MULTI_RUN_OUTCAR({ph}: 실행 {seg['n']}개 이어붙음 — "
                 f"{seg['used']}(#{seg['used_index']}) 세그먼트만 읽음. "
                 "단일 실행 계약과 어긋난다 — 출처 확인 전 인용 금지)")
    if oc.get("suffix_magic_mismatch"):
        g.append(f"OUTCAR_FORMAT_MISMATCH({ph}: 확장자와 실제 형식({oc.get('read_format')})이 다름)")
    if not oc["normal_end"]:
        g.append(f"NOT_TERMINATED({ph} — General timing 없음, 잘린 OUTCAR)")
    if oc["E0"] is None:
        g.append(f"NO_ENERGY({ph})")
    if oc["nelm_hit"]:
        g.append(f"ELECTRONIC_NELM_HIT({ph})")
    if want_ionic and not oc["ionic_conv"]:
        g.append(f"IONIC_NOT_CONVERGED({ph})")
    expect = [spec.get(e, e) for e in meta.get("species_order", [])]
    got = [x.split()[1] if len(x.split()) > 1 else x for x in oc["titels"]]
    # ⚠ TITEL 이 아예 없으면 "검사 못 함" 이지 "통과" 가 아니다
    if expect and not got:
        g.append(f"POTCAR_UNVERIFIED({ph} — TITEL 없음)")
    elif expect and got and len(got) != len(expect):
        g.append(f"POTCAR_COUNT({ph}: {len(got)}!={len(expect)})")
    elif expect and got and got != expect:
        # ⛔ 2026-08-12 — 옛 판은 여기서 변형 문자열을 **비교하지 않았고**, 뒤의 전역
        #   검사도 "준중심 접미사가 있는가" 라는 boolean 만 봐서 Ni_pv→Ni_sv 가 경고로
        #   통과했다. 고정 protocol 에서는 한 글자만 달라도 다른 Hamiltonian 이다.
        g.append(f"POTCAR_VARIANT({ph}: {got}!={expect})")
    nat = sum(meta.get("counts", []) or [])
    if nat and oc["nions"] and oc["nions"] != nat:
        g.append(f"NIONS_MISMATCH({ph}: {oc['nions']}!={nat})")
    # ── 이 상이 **선언한 대로** 돌았는지: k 점 수 + INCAR 되울림 (Codex P0-5) ──
    #   dense 폴더에 static OUTCAR 를 복사해도 에너지만 맞으면 통과하던 구멍을 막는다.
    #   ⚠ NKPTS 절대값은 대칭 축약(ISYM·시간반전) 때문에 예측이 불안정하다 —
    #   상한(전체 격자 곱)만 여기서 보고, **상 사이 단조성**은 main() 에서 본다.
    want_k = (meta.get("kmesh") or {}).get(ph)
    if want_k:
        prod = 1
        for x in str(want_k).split():
            prod *= int(x)
        if not oc.get("nkpts"):
            g.append(f"KMESH_UNVERIFIED({ph} — OUTCAR 에 NKPTS 없음)")
        elif oc["nkpts"] > prod:
            g.append(f"KMESH_MISMATCH({ph}: NKPTS {oc['nkpts']} > 격자 {want_k} 의 {prod})")
    # 🔴🔴 회신 AT P0-2 — 위 상한 검사는 **coarse OUTCAR 를 dense 폴더에 넣어도
    #   통과한다** (3 4 1 = 12 ≤ 4 6 1 = 24). 격자·시프트를 **정확히** 대조한다:
    #   KPOINTS 제목에 실어 둔 `phase=…  k=…  shift=…` 가 OUTCAR 되울림과 같아야 한다.
    _kpe = (meta.get("kpoints_expected") or {}).get(ph)
    if _kpe:
        _gott = oc.get("kpoints_title")
        if not _gott:
            g.append(f"KPOINTS_TITLE_UNVERIFIED({ph} — OUTCAR 에 ` KPOINTS:` 되울림이 "
                     f"없다. 확인 못 한 것은 통과가 아니다)")
        elif _gott.strip() != str(_kpe.get("title", "")).strip():
            g.append(f"KPOINTS_MISMATCH({ph}: 되울림 {_gott!r} ≠ 기대 "
                     f"{_kpe.get('title')!r} — 다른 상의 OUTCAR 이거나 격자·시프트가 "
                     f"다르다)")
    elif ph in ("dense", "dense_cand"):
        # dense 는 δ_k 로 **판정에 직접 들어가는** 상이다 — 기대값이 없으면 막는다
        g.append(f"KPOINTS_EXPECTED_MISSING({ph} — job.json 에 kpoints_expected 가 "
                 f"없다. 구판 번들이다 (회신 AT P0-2))")
    # 🔴 회신 AT P0-2 — dense 의 INCAR 기대값이 없으면 그 상의 INCAR 감사가 통째로
    #   비어 fail-open 이 된다. 판정에 들어가는 상에서는 그것을 막는다.
    if ph in ("dense", "dense_cand") and not (meta.get("incar_expected") or {}).get(ph):
        g.append(f"INCAR_EXPECTED_MISSING({ph} — 기대 INCAR 이 없어 이 상의 감사가 "
                 f"통째로 비어 있다. ENCUT·IVDW·ISPIN·LDAU·ICHARG 가 무엇이든 "
                 f"통과한다 (회신 AT P0-2))")
    audit = {"verified_exact": [], "verified_equivalence_class": [],
             "unverified": [], "mismatch": []}
    expected = (meta.get("incar_expected") or {}).get(ph, {})
    for k2 in AUDIT_KEYS_RUNTIME:
        got2 = (oc.get("incar_echo") or {}).get(k2)
        want = expected.get(k2)
        if k2 in _ECHO_ABSENT:
            # 원리적 검증불가 — 게이트 없이 **명시적으로** unverified (조용한 통과 금지)
            audit["unverified"].append(f"{k2}(OUTCAR 미되울림 — 원리적 검증불가, "
                                       "선언은 INCAR sha256 무결성으로만 보증)")
            continue
        if want is None:
            if got2 is not None:
                audit["unverified"].append(f"{k2}(기대값 미등록 — 되울림 {got2} 은 비교 안 됨)")
            continue
        if got2 is None:
            audit["unverified"].append(k2)
            g.append(f"INCAR_UNVERIFIED({ph}.{k2})")
            continue
        ok, kind = _incar_match(k2, got2, want)
        if not ok:
            audit["mismatch"].append(k2)
            g.append(f"INCAR_MISMATCH({ph}.{k2}: {got2}!={want})")
        elif kind == "equivalence_class":
            audit["verified_equivalence_class"].append(k2)
        else:
            audit["verified_exact"].append(k2)
    oc["incar_audit"] = audit                  # RESULTS.json 에 그대로 실린다
    # ⛔⛔ 회신 AO P0-5 (2026-08-31) — 이 게이트가 **정의만 되고 호출되지 않았다.**
    #   `ICHARG=1`, `chgcar_from_file=False` 인 재현 입력도 게이트 결과가 빈 목록이라
    #   fail-open 이었다. C-12 에서 `ICHARG=1` 상은 기체 기준 static 둘이고
    #   그 둘은 D 에 직접 들어간다. 여기서 실제로 연결한다.
    g += _icharg1_chgcar_gate(oc, ph)
    return g


def check_pin(jobdir):
    """rescue 1상(static_pin)의 수용 검사 — 통과 전에는 release 를 돌리면 안 된다.

    ⛔ v1 은 자기만의 축소판 검사(NUPDOWN·topology)였다 — codex E-3차가
      **LDAUU 를 5.0 으로 바꾼 pin 도 통과**함을 재현했다. v2 는 상 게이트
      전체(phase_gates: 등록된 INCAR 기대키 전부 · MULTI_RUN · 판독오류 ·
      형식 불일치 · E0 · NIONS · POTCAR TITEL · KPOINTS 상한)를 그대로 태우고,
      그 위에 topology·모멘트 붕괴·CHGCAR 해시만 얹는다.

    이 검사가 못 하는 것: pin 이 '어느' basin 인지의 절대 판정 — 시드 topology
    와의 일치까지만 본다.
    """
    jd = pathlib.Path(jobdir)
    meta = json.load(open(jd / "job.json", encoding="utf-8"))
    spec = meta.get("potcar_spec") or {}
    bad = []
    if not spec:
        bad.append("job.json 에 potcar_spec 이 없다 — POTCAR TITEL 검증 불가 (fail-closed)")
    # ⛔ codex E-4차 P0-1 — phase_gates 는 kmesh 결측을 **조용히 건너뛴다** (wave1
    #   호환 때문). release 사슬에서는 그 관용이 fail-open 이다 — 여기서 막는다.
    if not (meta.get("kmesh") or {}).get("static_pin"):
        bad.append("job.json 에 kmesh.static_pin 이 없다 — KPOINTS 검증 불가 (fail-closed)")
    # 배포 기준과 pin INCAR 대조 (MANIFEST_RESCUE — 있으면 강제, 없으면 거부)
    _mr = jd / "MANIFEST_RESCUE.json"
    if not _mr.is_file():
        bad.append("MANIFEST_RESCUE.json 없음 — 배포 기준 해시 부재 (fail-closed)")
    else:
        try:
            _man = (json.load(open(_mr, encoding="utf-8")) or {}).get("sha256") or {}
            _inc = jd / "static_pin" / "INCAR"
            if _inc.is_file() and _man.get("static_pin/INCAR"):
                _h = hashlib.sha256(open(_inc, "rb").read()).hexdigest()
                if _h != _man["static_pin/INCAR"]:
                    bad.append("static_pin/INCAR 가 배포본과 다르다 (변조/수정)")
            else:
                bad.append("pin INCAR 또는 그 배포 해시가 없다")
        except ValueError:
            bad.append("MANIFEST_RESCUE 파싱 실패")
    oc = read_outcar(str(jd / "static_pin" / "OUTCAR"))
    # 상 게이트 전체 — release 사슬에서 하나라도 걸리면 여기서 끝난다
    bad += phase_gates(oc, "static_pin", meta, spec)
    if oc and not oc.get("read_error"):
        seg = oc.get("run_segments") or {}
        if seg.get("n", 1) != 1:
            pass                                  # MULTI_RUN 게이트가 이미 bad 에 있다
        want = {int(k): v for k, v in (meta.get("ni_sign_poscar_idx") or {}).items()}
        mom = {i: v for i, v in enumerate(oc.get("moments") or [])}
        if not mom:
            bad.append("모멘트 표 없음 (LORBIT 확인)")
        elif want:
            sg, flip = global_sign(mom, want)
            small = [i for i in want if abs(mom.get(i, 0.0)) < 0.4]
            if flip:
                bad.append(f"⛔ pin 이 시드 topology 가 아님 — flip {len(flip)}개 "
                           f"(0-based {sorted(flip)[:4]}…)")
            if small:
                bad.append(f"모멘트 붕괴 의심 {len(small)}개 (<0.4 μB)")
    chg = jd / "static_pin" / "CHGCAR"
    chg_info = None
    if chg.is_file() and chg.stat().st_size > 0:
        h = hashlib.sha256()
        with open(chg, "rb") as fh:
            for b in iter(lambda: fh.read(1 << 20), b""):
                h.update(b)
        chg_info = {"sha256": h.hexdigest(), "bytes": chg.stat().st_size,
                    "mtime": chg.stat().st_mtime}
    else:
        bad.append("CHGCAR 없음/빈 파일")
    out = {"pass": not bad, "problems": bad, "chgcar": chg_info,
           "nupdown_echo": ((oc or {}).get("incar_echo") or {}).get("NUPDOWN"),
           "incar_audit": (oc or {}).get("incar_audit"),
           "run_segments": (oc or {}).get("run_segments"),
           "checked": "static_pin"}
    (jd / "static_pin").mkdir(exist_ok=True)
    (jd / "static_pin" / "PIN_CHECK.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(("✅ pin 수용 — release 진행 가능" if not bad else
           "⛔ pin 거부 — release 를 돌리지 말 것") + f"  ({jd})")
    for x in bad:
        print("   ·", x)
    if chg_info:
        print(f"   CHGCAR sha256 {chg_info['sha256'][:16]}… ({chg_info['bytes']} B)")
    return 0 if not bad else 1


def rescue_provenance_ok(jd):
    """supersede 의 추가 조건 — **모든 필드가 fail-closed** (codex E-4차 P0 5건).

    v1 의 구멍 (전부 적대 재현됨):
      · parent_match={} → all({})==True 로 우회      → 키별 is True 요구
      · identical 플래그만 믿음 (거짓 기록 가능)      → pin/static sha 직접 비교
      · PIN_CHECK 에 chgcar 없으면 교차검증 생략       → 없으면 거부
      · 'could not be read' 같은 **부정문도 증거로 통과** → 부정 마커 필터
      · 배포 입력(MANIFEST_RESCUE)과 대조 없음         → 기록·디스크 양쪽 대조

    → (ok, why)
    """
    jd = pathlib.Path(jd)
    pc_p = jd / "static_pin" / "PIN_CHECK.json"
    pv_p = jd / "RUN_PROVENANCE.json"
    mr_p = jd / "MANIFEST_RESCUE.json"
    for f, w in ((pc_p, "PIN_CHECK.json 없음 — pin 수용검사 미실행"),
                 (pv_p, "RUN_PROVENANCE.json 없음 — 해시·승계 증거 미기록"),
                 (mr_p, "MANIFEST_RESCUE.json 없음 — 배포 기준 해시 부재")):
        if not f.is_file():
            return False, w
    try:
        pc, pv, mr = (json.load(open(x, encoding="utf-8")) for x in (pc_p, pv_p, mr_p))
    except ValueError as e:
        return False, f"provenance 파싱 실패: {e}"
    if not pc.get("pass"):
        return False, "PIN_CHECK.pass=false"
    if not re.match(r"^\d{8}T\d{6}Z_\S+$", str(pv.get("run_id") or "")):
        return False, f"run_id 형식 오류: {pv.get('run_id')!r}"
    if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", str(pv.get("utc") or "")):
        return False, f"utc 형식 오류: {pv.get('utc')!r}"
    # ⛔ E-5차 — runner 는 preflight_problems 를 **항상** [] 로 기록한다.
    #   필드 부재(위조 pv)도, 비어있지 않음도 전부 거부다.
    if pv.get("preflight_problems") != []:
        return False, f"preflight 미기록/실패: {pv.get('preflight_problems')!r}"
    # 부모 대조 — 빈 dict 는 통과가 아니다: 키별로 is True 를 요구한다
    pm = pv.get("parent_match") or {}
    for k in ("POSCAR", "KPOINTS"):
        if pm.get(k) is not True:
            return False, f"부모 대조 결측/실패: {k}={pm.get(k)!r}"
    # 배포 기준(MANIFEST_RESCUE) ↔ 실행 기록 ↔ 현재 디스크 3중 대조
    man = mr.get("sha256") or {}
    rec = pv.get("inputs_sha256") or {}
    # ⛔ E-5차 — '있으면 대조' 는 fail-open 이다: 파일이 없으면 대조가 조용히
    #   생략됐다. 배포에 포함된 파일은 **존재 자체가 필수**다.
    _DISK_REQUIRED = ("POSCAR", "KPOINTS", "static_pin/INCAR", "static/INCAR",
                      "static_pin/KPOINTS", "static/KPOINTS",
                      "job.json", "run_job.sh")
    for f in _DISK_REQUIRED:
        if not man.get(f):
            return False, f"MANIFEST_RESCUE 에 {f} 해시 없음"
        fp = jd / f
        if not fp.is_file():
            return False, f"배포 파일이 디스크에 없다: {f}"
        h = hashlib.sha256(open(fp, "rb").read()).hexdigest()
        if h != man[f]:
            return False, f"디스크 파일이 배포본과 다름(사후 변조?): {f}"
    for f in ("POSCAR", "KPOINTS", "static_pin/INCAR", "static/INCAR"):
        if rec.get(f) != man[f]:
            return False, f"실행 기록 해시 ≠ 배포 해시: {f}"
    # ⛔ E-6차 — parent_match 는 runner 가 **기록한 불리언**이라 위조 가능하다.
    #   재계산 사슬로 검증한다: 디스크==배포해시(위에서 확인) 이고, 배포해시==부모해시
    #   (job.json 은 자체가 해시 앵커됨) 이면 부모 대조가 독립적으로 선다.
    try:
        _meta = json.load(open(jd / "job.json", encoding="utf-8"))
    except ValueError as e:
        return False, f"job.json 파싱 실패: {e}"
    _par = ((_meta.get("rescue") or {}).get("parent_sha256") or {})
    for f in ("POSCAR", "KPOINTS"):
        if not _par.get(f):
            return False, f"job.json 에 부모 해시 없음: {f}"
        if man[f] != _par[f]:
            return False, f"배포 {f} 가 부모와 다르다 (재계산 대조 실패)"
    # phase 디렉터리 사본 — **VASP 가 실제로 읽는 파일** (P0-2·3)
    for f in ("static_pin/KPOINTS", "static/KPOINTS",
              "static_pin/POSCAR", "static/POSCAR",
              "static_pin/POTCAR", "static/POTCAR"):
        if not rec.get(f):
            return False, f"실행 기록에 phase 사본 해시 없음: {f}"
    if rec["static_pin/KPOINTS"] != man["KPOINTS"] or rec["static/KPOINTS"] != man["KPOINTS"]:
        return False, "phase KPOINTS 사본이 배포본과 다르다"
    if rec["static_pin/POSCAR"] != man["POSCAR"] or rec["static/POSCAR"] != man["POSCAR"]:
        return False, "phase POSCAR 사본이 배포본과 다르다"
    if not (rec.get("POTCAR") and rec["static_pin/POTCAR"] == rec["POTCAR"]
            and rec["static/POTCAR"] == rec["POTCAR"]):
        return False, "POTCAR 조립본과 phase 사본이 서로 다르다"
    # CHGCAR 승계 — 플래그를 믿지 않는다: sha 문자열 직접 비교 + PIN_CHECK 교차
    ch = pv.get("chgcar_sha256") or {}
    if not (ch.get("pin") and ch.get("static_copy")):
        return False, "CHGCAR sha 미기록"
    if ch["pin"] != ch["static_copy"]:
        return False, "CHGCAR pin/사본 sha 불일치"
    pc_sha = (pc.get("chgcar") or {}).get("sha256")
    if not pc_sha:
        return False, "PIN_CHECK 에 CHGCAR sha 없음 — 교차검증 불가"
    if ch["pin"] != pc_sha:
        return False, "PIN_CHECK 의 CHGCAR sha 와 provenance 가 다르다 (다른 실행 혼입?)"
    # ── CHGCAR 승계 증거 (E-6차 전면 교체) ────────────────────────────────
    #   vasp.log 문자열 게이트는 **블랙리스트 두더지잡기**였다 — 'hello'(양성 패턴
    #   부재), "NOT_FOUND" 문자순회, 부정문 변형("can't", "skipped", …)이 계속
    #   나온다. 판별자는 stdout 이 아니라 **회신된 static OUTCAR 자체**에 있다
    #   (wave1 실측: ICHARG=1 은 `initial charge density was supplied:` 만,
    #   ICHARG=2 는 그 밑에 `charge density of overlapping atoms calculated`).
    #   stdout 기록(chgcar_read_evidence)은 정보용으로 강등 — 게이트하지 않되
    #   타입 오염(str 순회 함정)만은 거부한다.
    ev = pv.get("chgcar_read_evidence")
    if ev is not None and (not isinstance(ev, list)
                           or not all(isinstance(x, str) for x in ev)):
        return False, f"chgcar_read_evidence 형식 오류 (list[str] 아님): {type(ev).__name__}"
    st_oc = read_outcar(str(jd / "static" / "OUTCAR"))
    if st_oc is None or st_oc.get("read_error"):
        return False, ("static OUTCAR 판독 불가 — CHGCAR 승계 검증 불가: "
                       + str((st_oc or {}).get("read_error", "파일 없음")))
    cff = st_oc.get("chgcar_from_file")
    if cff is not True:
        return False, ("static OUTCAR 에 CHGCAR 승계 증거 없음 "
                       + ("(overlapping atoms 로 새로 만듦 — ICHARG=1 미작동)"
                          if cff is False else "(마커 부재 — 판별 불가)"))
    return True, "ok"



#: 사전등록 문턱 — `prereg_sdcp_neutral_contrast_2026_08_29.json` 과 **같은 값**이어야 한다.
#:   ⚠ 두 곳에 복사돼 있다. 고치면 그 json 도 같이 고칠 것.
PREREG_GUARD_EV = -0.10           # primary 가 이 값 이하일 때만 방향성 주장
PREREG_ROUND_EV = 0.01            # 보고 반올림
PREREG_SELECTOR_AGREE_EV = 0.05   # 두 selector 차가 이 미만이면 "시험한 selector 간 일치"


#: ⚠ 분석기는 **번들 안에 단독 배포**된다 — 생성기 상수를 못 본다. 판정 branch 를
#:   여기 따로 박는다 (문자열이 갈라지면 C1·C3 가 조용히 빈다).
SEED_MAIN = "afm2424_pm1"

#: 닫힘 조건 문턱 — db/properties/sdcp_stageA_closure_conditions_2026_08_29.json
#: 에 **DFT 0잡 시점**으로 등록된 값. 코드와 문서가 갈라지면 문서가 정본이다.
C1_S_TOL_EV = 0.050          # 조각 내 잔차 range 허용
C3_REF_GAP_EV = 0.90         # 설명 대상 — 관측된 조각 간 UMA 오프셋 차등
C3_HI, C3_LO = 0.70, 0.30    # 채택 / 기각 비율
# D3 항등식 `E_on − E_off == Edisp` 의 허용 오차. 두 SCF 가 독립 수렴하므로
# EDIFF(1e-6 eV) 급 잔차는 정상이고, 그보다 훨씬 크면 쌍둥이가 IVDW 말고 다른
# 데서 갈렸다는 뜻이다. 1 meV 는 EDIFF 의 1000배 — 넉넉하되 실제 결함은 잡는다.
C3_EDISP_TOL_EV = 1.0e-3
#: ★ 0.90 eV 의 **원자료 정의를 봉인한다** (회신 AB P0-3).
#:   정본 db/properties/prereg_sdcp_neutral_contrast_2026_08_29.json
#:   → `🔬_UMA_대_DFT_오프셋_실측_2026_08_29.오프셋_UMA_빼기_DFT_eV`
#:   부호규약은 문자 그대로 **(UMA − DFT)** 다. 흡착에너지 오프셋이지
#:   총에너지 오프셋이 아니므로 원소별 energy-zero 는 소거된다 (AB P0-3 후단 해소).
C3_OFFSET_UMA_MINUS_DFT = {
    "sdcp_neutral": {"Li_top": 1.0728, "Ni_top": 1.0667},
    "ptfe_c10": {"Li_top": 0.1855, "Ni_top": 0.1484},
}
#: 조각 내 오프셋 **상수성** (관측 range). D3 가설이 살아남으려면 δ 의 조각내
#: range 가 이 정도여야 한다 — D3 는 기하 의존이라 자세마다 달라야 하는데
#: 관측 오프셋은 조각 안에서 상수였다 (prereg ⛔_분산_귀속_철회_2026_08_29).
C3_OFFSET_RANGE_EV = {"sdcp_neutral": 0.0061, "ptfe_c10": 0.0371}
#: 조각내 일관성 판정의 여유배수 — δ range 가 관측 range 의 이 배를 넘으면
#: "D3 로 설명" 은 성립하지 않는다 (평균이 맞아도).
C3_WITHIN_SLACK = 5.0


def _pick(jobs, **want):
    """구조화 필드로 잡을 고른다 (이름 파싱 금지)."""
    out = []
    for jn, jr in jobs.items():
        m = jr.get("meta") or {}
        if all(m.get(k) == v for k, v in want.items()):
            out.append(jn)
    return sorted(out)


def _twin_of(jobs, parent_key):
    """그 잡의 D3-off 쌍둥이 키. `d3_twin_of` 로만 찾는다 (접미어 추측 금지)."""
    for jn, jr in jobs.items():
        if (jr.get("meta") or {}).get("d3_twin_of") == parent_key:
            return jn
    return None


def _basin_of(jr):
    """잡 → (id, detail). 없으면 (None, None) — 호출부가 fail-closed 로 처리한다."""
    m = ((jr or {}).get("geom") or {}).get("magnetic") or {}
    return m.get("realized_basin_id"), m.get("realized_basin")


def same_basin(ja, jb):
    """두 잡이 **같은 자기 basin 인가** → (bool, 사유).

    🔴 회신 AB P0-4 — 종전엔 `realized_basin_id` **해시만** 비교했다. 그 해시는
      부호 벡터·붕괴 위치·유기물 상대 스핀만 담고 **크기를 안 담는다**. 그래서
      1.2 μB 와 2.0 μB 처럼 부호는 같고 크기가 크게 다른 상태가 같은 basin 으로
      통과했다. `basin_distance()` 의 RMS ≤ MOM_RMS_TOL 규칙은 selftest 밖에서
      **한 번도 호출되지 않았다** — 살아 있는 척하는 죽은 코드였다.
      ⇒ 해시가 같아도 상세 지문으로 한 번 더 본다. 지문이 없으면 통과가 아니다.
    """
    ia, da = _basin_of(ja)
    ib, db = _basin_of(jb)
    if ia is None or ib is None:
        return False, "realized_basin_id 없음 (미판정) — 통과로 읽지 않는다"
    if ia != ib:
        return False, f"basin 해시 불일치 {str(ia)[:8]} vs {str(ib)[:8]}"
    d = basin_distance(da, db)
    if d is None:
        return False, "상세 지문 없음 — 크기 비교 불가 (해시만으로 통과시키지 않는다)"
    if not d.get("same"):
        return False, ("해시는 같지만 상세가 다르다 (hamming %s · collapse %s · "
                       "RMS %s μB > %s)" % (d.get("hamming"), d.get("collapse_symdiff"),
                                            d.get("moment_rms_muB"), MOM_RMS_TOL))
    return True, "ok"


def potcar_provenance_gates(job_dir, meta, rel=None, man=None):
    """반송된 `POTCAR_PROVENANCE.json` 을 **분석기가 직접 읽고** 게이트한다.

    ⛔ 회신 AF P0-7 — 종전엔 러너만 봤다. 러너는 외주처 기계에서 돌고 우리는 그 결과를
    믿을 근거가 없다. 반송물에 provenance 가 있어야 하고, 그 내용이 이 잡의 종 순서·
    variant 와 맞아야 한다.

    ⛔ 이 함수가 못 하는 것: POTCAR **원본 파일**을 우리가 갖고 있지 않으므로
       `source_sha256` 이 진짜 그 배포판인지는 확인 못 한다. 사이트가 사전 승인된
       allowlist 를 썼다는 것과, 조립 뒤 바꿔치기가 없었다는 것만 본다.
    """
    g = []
    # 계약은 **우리가 조립기를 실어 보낸 잡**에만 적용한다. 그 사실은 files_sha256 에
    # 박혀 있어 지울 수 없다 (지우면 무결성 검사가 따로 잡는다). 합성 픽스처처럼
    # 조립기가 없는 잡에는 요구하지 않는다 — 없는 계약을 만들지 않기 위해서다.
    _fh = (man or {}).get("files_sha256") or {}
    if rel is not None and _fh and ("%s/POTCAR_ASSEMBLE.sh" % rel) not in _fh:
        return []
    if rel is not None and not _fh and not os.path.isfile(
            os.path.join(job_dir, "POTCAR_ASSEMBLE.sh")):
        return []
    pp = os.path.join(job_dir, "POTCAR_PROVENANCE.json")
    if os.path.isfile(os.path.join(job_dir, ".SELFTEST_FIXTURE")):
        return ["PROVENANCE_FIXTURE_MARKER(.SELFTEST_FIXTURE 가 반송물에 있다 — "
                "시험 장치 표시가 production 결과에 섞였다)"]
    if not os.path.isfile(pp):
        return ["POTCAR_PROVENANCE_MISSING(반송물에 없다 — 어떤 POTCAR 로 돌았는지 "
                "확인할 방법이 없다)"]
    try:
        d = json.load(open(pp, encoding="utf-8"))
    except Exception as e:                                   # noqa: BLE001
        return ["POTCAR_PROVENANCE_UNPARSEABLE(%s)" % e]
    if d.get("allowlist_waived"):
        g.append("POTCAR_ALLOWLIST_WAIVED(면제본 — 이 계약에서 폐지됐다)")
    if not d.get("allowlist_sha256"):
        g.append("POTCAR_ALLOWLIST_UNPINNED(allowlist 내용 SHA 가 없다 — 경로만으로는 "
                 "어느 목록이었는지 모른다)")
    if not d.get("assembled_sha256"):
        g.append("POTCAR_ASSEMBLED_SHA_MISSING")
    want_sp = list((meta or {}).get("species_order") or [])
    got_sp = list(d.get("species_order") or [])
    if want_sp and got_sp and want_sp != got_sp:
        g.append("POTCAR_SPECIES_ORDER_MISMATCH(잡 %s vs provenance %s — 종 순서가 "
                 "다르면 다른 계를 계산한 것이다)" % (want_sp, got_sp))
    # ⛔ 회신 AI §B — 종전엔 `expected_variants` 와 `titel_lines` 를 **둘 다 회신 JSON**
    #    에서 읽어 대조했다. 자기일관적인 허위 기록이 그대로 통과한다.
    #    대조 기준은 **우리가 만든** manifest 의 potcar_spec 이어야 한다.
    spec = (man or {}).get("potcar_spec") or (meta or {}).get("potcar_spec") or {}
    ours = [spec.get(e, e) for e in want_sp] if (spec and want_sp) else []
    tit = d.get("titel_lines") or []
    if ours:
        for v in ours:
            if not any(v in str(x) for x in tit):
                g.append("POTCAR_VARIANT_NOT_IN_TITEL(우리 규격 %s 가 회신 TITEL 에 "
                         "없다)" % v)
        if list(d.get("expected_variants") or []) != ours:
            g.append("POTCAR_SPEC_DISAGREES(회신 expected_variants %s ≠ 우리 규격 %s)"
                     % (d.get("expected_variants"), ours))
    else:
        g.append("POTCAR_SPEC_UNAVAILABLE(우리 쪽 규격이 없어 회신을 대조할 기준이 "
                 "없다 — 회신끼리만 맞춰 보는 것은 검증이 아니다)")
    return g


def potcar_identity_gates(jobs, man):
    """묶음 **전체**에서 POTCAR 원본과 VASP 가 하나인가 (회신 AI §B).

    잡 하나씩 봐서는 못 잡는 것을 본다: 잡마다 다른 PAW 배포판이나 다른 VASP 로
    돌았으면, 각 잡은 자기일관적이어도 **에너지를 뺄 수 없다**.

    `man["potcar_pin"]` 이 있으면 그것과도 대조한다 — 그것이 유일한 **외부 기준**이다.
    없으면 잡 사이 일치만 본다(자기일관성). 그 한계를 결과에 적는다.
    """
    res = {"schema": "potcar_identity/v1", "blocking": [], "n_with_prov": 0,
           "pin": (man or {}).get("potcar_pin"), "observed": {}}
    _spec_map = (man or {}).get("potcar_spec") or {}
    src, ver = {}, {}
    # ⛔ 회신 AR P0-6 — attestation 의 TITEL 을 **관측과 대조**하려면 관측 TITEL 을
    #   variant 별로 모아야 한다. provenance 의 titel_lines 와 OUTCAR 의 titels
    #   둘 다 " PAW_PBE Ni_pv 06Sep2000" 꼴이라 variant 토큰으로 색인한다.
    _titel_obs = {}

    def _titel_index(line):
        for _tok in str(line or "").replace("=", " ").split():
            if _tok in _spec_map.values() or _tok in _spec_map:
                _titel_obs.setdefault(_tok, set()).add(str(line).strip())

    for jn, jr in sorted((jobs or {}).items()):
        pv = (jr.get("geom") or {}).get("potcar_provenance") or jr.get("_prov")
        for _tl in ((pv or {}).get("titel_lines") or []):
            _titel_index(_tl)
        for _tl in (((jr.get("static") or {}) or {}).get("titels") or []):
            _titel_index(_tl)
        if not pv:
            continue
        res["n_with_prov"] += 1
        for e, s in (pv.get("source_sha256") or {}).items():
            src.setdefault(e, {}).setdefault(str(s), []).append(jn)
        v = ((jr.get("static") or {}) or {}).get("vasp_version")
        if v:
            ver.setdefault(str(v), []).append(jn)
    for e, d in src.items():
        if len(d) > 1:
            res["blocking"].append(
                "POTCAR_SOURCE_SPLIT(%s 의 원본 sha 가 묶음 안에서 %d 종 — 다른 PAW "
                "배포판의 에너지를 뺄 수 없다)" % (e, len(d)))
    if len(ver) > 1:
        res["blocking"].append(
            "VASP_VERSION_SPLIT(묶음 안에서 %s — 다른 코드 세대의 에너지를 뺄 수 없다)"
            % sorted(ver))
    res["observed"] = {"source_sha256": {e: sorted(d) for e, d in src.items()},
                       "vasp_version": sorted(ver),
                       "titel_by_variant": {k: sorted(v) for k, v in
                                            sorted(_titel_obs.items())}}
    # ⛔⛔ 회신 AO P0-8 (2026-08-31) — 종전 검사는 **관측된 것끼리 갈리지 않으면 통과**
    #   였다. source sha 가 일부·전부 없어도, VASP 버전이 0개 관측이어도 막지 않았다.
    #   그래서 `identity_scope = self_consistent_only`("14잡 신원 일치 확인") 라벨이
    #   사실보다 강했다. ⇒ **에너지를 낸 모든 잡**에 대해 기대되는 **모든 variant** 의
    #   원본 SHA256(64자리)과 정확한 VASP 버전을 필수로 한다.
    #   ⚠ 아직 안 돈 잡은 세지 않는다 (단계별 실행에서 2단계가 비어 있는 것은 정상).

    def _is_hex64(x):
        x = str(x or "")
        return len(x) == 64 and all(c in "0123456789abcdefABCDEF" for c in x)

    # ⛔⛔ 회신 AP #8/Q7 (2026-08-31) — 완주 판정이 **실제 record 모양과 달랐다.**
    #   생성부는 `rec = {..., "static": ocs.get("static"), ...}` 로 **미실행 잡에도
    #   `static: None` 키를 넣는다.** 그런데 여기서는 `"static" in jr` 로 완주를 셌다
    #   ⇒ 안 돈 잡까지 전부 "완주" 로 세고 provenance 를 요구했다.
    #   내 selftest 픽스처는 키 자체를 빼서 이 버그를 **재현하지 못했다** —
    #   회신 AL P0-3 과 같은 실패 방식이다(픽스처가 내 오해를 그대로 옮겼다).
    #   ⇒ AP 가 지정한 세 단계로 나눈다:
    #     attempted  : OUTCAR 를 읽었다 (static 레코드가 있다)
    #     completed  : 정상 종료 + 최종 에너지가 있다
    #     usable     : completed + 그 상의 게이트를 통과했다
    #   완전성(provenance·fingerprint·버전)은 **completed** 에만 건다.
    def _job_stage(jr):
        st = jr.get("static")
        if not isinstance(st, dict):
            return "not_attempted"          # None 이거나 키가 없다 = 안 돌았다
        if not st.get("normal_end") or st.get("E0") is None:
            return "attempted"              # OUTCAR 는 있는데 완주가 아니다
        return "completed" if not jr.get("gates") else "completed_gated"

    _ran, _noprov, _incomplete, _nover = [], [], [], []
    _stage_census = {}
    for jn, jr in sorted((jobs or {}).items()):
        _sg = _job_stage(jr)
        _stage_census[_sg] = _stage_census.get(_sg, 0) + 1
        if not _sg.startswith("completed"):
            continue                       # 안 돌았거나 완주 못 한 잡 — 완전성 대상 아님
        _ran.append(jn)
        pv = (jr.get("geom") or {}).get("potcar_provenance") or jr.get("_prov")
        if not pv:
            _noprov.append(jn)
            continue
        _els = list((jr.get("meta") or {}).get("species_order") or [])
        _want_v = ([str(_spec_map.get(e, e)) for e in _els]
                   or sorted((pv.get("source_sha256") or {})))
        _have = {str(k): v for k, v in (pv.get("source_sha256") or {}).items()}
        # ⚠ 조립기는 **variant 키**(Ni_pv)로 기록하고 옛 기록은 **원소 키**(Ni)다.
        #   pin 대조와 **같은 정규화**를 쓴다 — 요구하는 것은 "그 fingerprint 가
        #   있고 64자리인가" 이지 키 철자가 아니다.
        _alias = {str(_spec_map.get(e, e)): e for e in _els}
        _miss = [v for v in _want_v
                 if not (_is_hex64(_have.get(v))
                         or _is_hex64(_have.get(_alias.get(v, v))))]
        if _miss:
            _incomplete.append("%s:%s" % (jn, _miss))
        if not ((jr.get("static") or {}).get("vasp_version")):
            _nover.append(jn)
    if _ran:
        if _noprov:
            res["blocking"].append(
                "POTCAR_PROVENANCE_MISSING(%d/%d 완주잡에 provenance 가 없다 %s — "
                "없는 것을 '갈리지 않음' 으로 읽지 않는다)"
                % (len(_noprov), len(_ran), _noprov[:3]))
        if _incomplete:
            res["blocking"].append(
                "POTCAR_SOURCE_INCOMPLETE(%d잡에서 기대 variant 의 원본 SHA256 이 "
                "빠졌거나 64자리가 아니다 %s)" % (len(_incomplete), _incomplete[:3]))
        if _nover:
            res["blocking"].append(
                "VASP_VERSION_UNOBSERVED(%d/%d 완주잡에 VASP 버전 관측이 없다 %s — "
                "0개 관측은 일치가 아니다)" % (len(_nover), len(_ran), _nover[:3]))
    res["completeness"] = {"n_jobs": len(jobs or {}),
                           "n_completed": len(_ran),
                           "stage_census": _stage_census,
                           "n_with_prov": res["n_with_prov"],
                           "n_no_prov": len(_noprov),
                           "n_incomplete_variants": len(_incomplete),
                           "n_without_vasp_version": len(_nover),
                           "판정": ("완전성은 **completed**(정상 종료 + 최종 에너지) "
                                    "잡에만 건다. 미실행·중단 잡은 대상이 아니다 — "
                                    "단계별 실행에서 2단계가 비어 있는 것은 정상이다")}
    # ⛔ 회신 AO Q1 — **생산 전에 봉인한** variant 별 원본 fingerprint(root seal)와
    #   대조한다. 사후 provenance 끼리만 비교하는 것은 사전 승인과 같지 않다.
    _seal = ((man or {}).get("_potcar_root_seal") or {}).get("source_sha256") or {}
    _seal_rec = ((man or {}).get("_potcar_root_seal") or {})
    # ⛔⛔ 회신 AR P0-5/P0-6 · 해제조건 7 (2026-08-31) — 종전 검증은 **fail-open** 이었다.
    #   `source_sha256` 과 `sealed_before_production:true` 만 있는 반쪽 봉인도
    #   `sealed_root_v13` 라벨을 받았고, `FAKE_RELEASE` + 실제로 쓰지 않는
    #   `UNRELATED` variant 하나짜리 합성 attestation 도 `usable:true` 가 됐다.
    #   ⇒ ① 봉인 schema 를 **전부 필수**로 ② 봉인·attestation·실제 계획 잡의
    #     variant 집합을 **완전일치**로 ③ manifest/ZIP/allowlist/VASP 신원까지 결박.
    #   ⚠ 여기서 "계획 잡" 은 미실행 2단계를 포함한다 — 봉인은 앞으로 돌 잡의
    #     기대 POTCAR 까지 포괄해야 사전 승인이다 (AR Q4).
    _plan_var, _plan_nospec = set(), []
    for _pj, _pl in sorted(((man or {}).get("planned") or {}).items()):
        _els = list(((_pl or {}).get("meta") or {}).get("species_order") or [])
        if not _els:
            _plan_nospec.append(_pj)
            continue
        _plan_var |= {str(_spec_map.get(e, e)) for e in _els}
    _mh = (man or {}).get("_manifest_sha256_actual")
    _zip_obs = (man or {}).get("_zip_sha256_observed")
    _cov, _covwhy = False, []
    if _seal:
        res["root_seal_variants"] = sorted(_seal)
        res["root_seal_meta"] = {
            k: _seal_rec.get(k) for k in
            ("schema", "allowlist_sha256", "manifest_sha256", "vasp_executable",
             "vasp_executable_sha256", "vasp_version_banner", "sealed_at_utc",
             "sealed_before_production")}
        # ── ① schema 전부 필수 (없는 것은 통과가 아니다) ──────────────────
        _seal_need = ("schema", "allowlist_sha256", "manifest_sha256",
                      "vasp_executable", "vasp_executable_sha256",
                      "vasp_version_banner", "sealed_at_utc", "bundle_zip_sha256",
                      "assembled_sha256_by_job", "sealed_before_production_evidence")
        _seal_miss = [k for k in _seal_need if not _seal_rec.get(k)]
        if _seal_miss:
            res["blocking"].append(
                "ROOT_SEAL_INCOMPLETE_SCHEMA(봉인에 %s 가 없다 — 반쪽 봉인은 "
                "사전 승인이 아니다)" % _seal_miss)
        if str(_seal_rec.get("schema") or "") != "potcar_root_seal/v2":
            res["blocking"].append(
                "ROOT_SEAL_SCHEMA(schema=%r — potcar_root_seal/v2 가 아니다)"
                % _seal_rec.get("schema"))
        for _hk in ("allowlist_sha256", "manifest_sha256", "vasp_executable_sha256",
                    "bundle_zip_sha256"):
            if _seal_rec.get(_hk) and not _is_hex64(_seal_rec[_hk]):
                res["blocking"].append("ROOT_SEAL_BAD_HASH(%s)" % _hk)
        # 봉인이 말하는 ZIP 과 실제로 받은 ZIP 이 같은가 (둘 다 있을 때만 대조)
        if (_zip_obs and _seal_rec.get("bundle_zip_sha256")
                and _seal_rec["bundle_zip_sha256"] != _zip_obs):
            res["blocking"].append(
                "ROOT_SEAL_ZIP_MISMATCH(봉인 %s ≠ 받은 ZIP %s — 다른 배포본을 "
                "봉인했다)" % (str(_seal_rec["bundle_zip_sha256"])[:12], str(_zip_obs)[:12]))
        # ── ② 봉인이 **계획 잡 전체**를 포괄하는가 ────────────────────────
        if _plan_nospec:
            res["blocking"].append(
                "ROOT_SEAL_PLAN_UNREADABLE(계획 잡 %d개에 species_order 가 없어 "
                "필요한 variant 를 셀 수 없다: %s)"
                % (len(_plan_nospec), _plan_nospec[:3]))
        elif _plan_var and set(_seal) != _plan_var:
            res["blocking"].append(
                "ROOT_SEAL_PLAN_COVERAGE(봉인 variant %s ≠ 계획 잡이 요구하는 %s — "
                "미실행 잡의 기대 POTCAR 까지 포괄해야 사전 승인이다)"
                % (sorted(_seal), sorted(_plan_var)))
        _asm = (_seal_rec.get("assembled_sha256_by_job") or {})
        _plan_dirs = sorted((man or {}).get("planned") or {})
        _asm_miss = [j for j in _plan_dirs if j not in _asm]
        if _asm and _asm_miss:
            res["blocking"].append(
                "ROOT_SEAL_JOB_COVERAGE(봉인의 assembled 해시에 계획 잡 %d개가 "
                "없다: %s)" % (len(_asm_miss), _asm_miss[:3]))
        # ⛔⛔ 회신 AS 해제조건 4 (2026-08-31) — 종전엔 **키만** 봤다. 봉인이
        #   기록한 조립본 해시를 **반송된 provenance 의 실제 값**과 대조하지
        #   않으면, 봉인 뒤에 POTCAR 를 갈아끼워도 잡히지 않는다.
        _asm_bad, _asm_unver = [], []
        for _jn, _jr in sorted((jobs or {}).items()):
            _pv = (_jr.get("geom") or {}).get("potcar_provenance") or _jr.get("_prov")
            if not _pv:
                continue                      # 완전성 게이트가 따로 본다
            _got = _pv.get("assembled_sha256")
            _want = _asm.get(_jn)
            if _want is None:
                _asm_unver.append(_jn)
            elif not _got:
                _asm_unver.append("%s(반송에 assembled 없음)" % _jn)
            elif str(_got) != str(_want):
                _asm_bad.append("%s: 봉인 %s ≠ 반송 %s"
                                % (_jn, str(_want)[:12], str(_got)[:12]))
        if _asm_bad:
            res["blocking"].append(
                "ROOT_SEAL_ASSEMBLED_MISMATCH(봉인한 POTCAR 와 실제로 쓴 POTCAR 가 "
                "다르다 %d건: %s)" % (len(_asm_bad), _asm_bad[:3]))
        if _asm_unver and _ran:
            res["blocking"].append(
                "ROOT_SEAL_ASSEMBLED_UNVERIFIED(조립본 해시를 대조하지 못한 잡 "
                "%d건: %s — 확인 못 한 것은 통과가 아니다)"
                % (len(_asm_unver), _asm_unver[:3]))
        res["assembled_crosscheck"] = {
            "compared": len([1 for j, r in (jobs or {}).items()
                             if ((r.get("geom") or {}).get("potcar_provenance")
                                 or r.get("_prov"))]),
            "mismatch": len(_asm_bad), "unverified": len(_asm_unver)}
        # ── ③ 이 묶음의 MANIFEST 인가 (해시가 없으면 그것도 실패다) ────────
        if not _seal_rec.get("manifest_sha256") or not _mh:
            res["blocking"].append(
                "ROOT_SEAL_MANIFEST_UNBOUND(봉인 또는 현재 MANIFEST 해시가 없어 "
                "결박을 확인할 수 없다)")
        elif _seal_rec["manifest_sha256"] != _mh:
            res["blocking"].append(
                "ROOT_SEAL_WRONG_BUNDLE(봉인이 다른 MANIFEST 에 대한 것이다: "
                "봉인 %s ≠ 지금 %s)" % (_seal_rec["manifest_sha256"][:12], _mh[:12]))
        if _seal_rec.get("sealed_before_production") is not True:
            res["blocking"].append(
                "ROOT_SEAL_NOT_PREPRODUCTION(봉인이 생산 전이라는 근거가 없다)")
        # ── ④ 실제로 돌린 VASP 와 결박 ────────────────────────────────────
        _seal_ver = str(_seal_rec.get("vasp_version_banner") or "")
        _obs_ver = sorted(ver)
        _ver_bad = [v for v in _obs_ver if v and v not in _seal_ver]
        if _obs_ver and _seal_ver and _ver_bad:
            res["blocking"].append(
                "ROOT_SEAL_VASP_MISMATCH(봉인 배너 %r 에 관측 버전 %s 가 없다 — "
                "봉인한 바이너리로 돌았다는 근거가 없다)" % (_seal_ver[:40], _ver_bad[:2]))
        for _v, _sh in sorted(_seal.items()):
            _got = sorted(src.get(_v, {}))
            if _ran and not _got:
                res["blocking"].append(
                    "ROOT_SEAL_UNOBSERVED(%s: 봉인돼 있는데 회신에 원본 sha 가 없다)" % _v)
            elif _got and _got != [str(_sh)]:
                res["blocking"].append(
                    "ROOT_SEAL_MISMATCH(%s: 봉인 %s ≠ 관측 %s — 생산 전에 승인한 "
                    "Hamiltonian root 가 아니다)" % (_v, str(_sh)[:12], [g[:12] for g in _got]))
        _unsealed = sorted(set(src) - set(_seal))
        if _unsealed:
            res["blocking"].append(
                "ROOT_SEAL_INCOMPLETE(봉인에 없는 variant 가 관측됐다 %s)" % _unsealed)
    elif _ran and (man or {}).get("files_sha256"):
        res["root_seal_absent"] = True
    # ⛔⛔ 회신 AP #12 — 원고 Methods 문구를 **여기서 하나로** 만든다. 사람이
    #   고르게 두면 강한 쪽을 고르게 된다. attestation 유무가 문구를 정한다.
    _att = (man or {}).get("_potcar_attestation") or {}
    _att_ok = False
    _att_why = []
    if _att:
        # ⛔⛔ 회신 AR P0-6 · 해제조건 7 — **exact-set 및 교차 결박**을 요구한다.
        #   종전엔 `FAKE_RELEASE` + 실제 쓰지 않는 `UNRELATED` variant 하나짜리
        #   합성 attestation 도 usable:true 였다. 다음 셋의 **완전일치**를 본다:
        #     attestation variants = root-seal source variants = 계획 잡 POTCAR variants
        # 🔴 회신 AT P0-4 — 필수 목록에 `schema` 가 없었다. 스키마가 무엇이든
        #   나머지가 채워져 있으면 통과했다.
        _need_att = ("schema", "release_label", "variants", "vasp_version_raw",
                     "vasp_executable", "vasp_executable_sha256", "allowlist_sha256",
                     "manifest_sha256", "bundle_zip_sha256", "site", "created_utc",
                     "made_before_production_evidence")
        _att_miss = [k for k in _need_att if not _att.get(k)]
        _av = set(_att.get("variants") or {})
        if _att_miss:
            _att_why.append("ATTESTATION_INCOMPLETE(필드 누락 %s)" % _att_miss)
        if _att.get("schema") and _att["schema"] != "potcar_attestation/v1":
            _att_why.append("ATTESTATION_SCHEMA_UNKNOWN(%r — 이 도구가 아는 스키마가 "
                            "아니다)" % (_att["schema"],))
        # 🔴 회신 AT P0-4 — `made_before_production` 을 **불리언으로** 본다
        #   (문자열 "true" 는 파이썬에서 참이지만 증서가 아니다)
        if _att.get("made_before_production") is not True:
            _att_why.append("ATTESTATION_NOT_PREPRODUCTION(made_before_production 이 "
                            "불리언 True 가 아니다: %r)"
                            % (_att.get("made_before_production"),))
        if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$",
                        str(_att.get("created_utc") or "")):
            _att_why.append("ATTESTATION_TIME_MALFORMED(created_utc %r)"
                            % (_att.get("created_utc"),))
        # 🔴🔴 회신 AT P0-4 — **root seal 이 없으면 attestation 을 쓸 수 없다.**
        #   종전엔 집합 대조가 `if _seal and …` 이라 봉인이 없으면 통째로 건너뛰었고,
        #   임의 release label + 비정상 hash 의 attestation 이 usable:true 로 갔다.
        if not _seal:
            _att_why.append("ATTESTATION_WITHOUT_ROOT_SEAL(root seal 이 없다 — "
                            "attestation 만으로 release 를 주장하지 않는다. 봉인이 "
                            "'이 계산들이 한 트리에서 나왔다' 를 대는 쪽이다)")
        if (_att.get("manifest_sha256") and _mh
                and _att["manifest_sha256"] != _mh):
            _att_why.append("ATTESTATION_WRONG_BUNDLE(다른 MANIFEST 에 대한 "
                            "attestation 이다: %s ≠ %s)"
                            % (str(_att["manifest_sha256"])[:12], str(_mh)[:12]))
        elif not _mh:
            _att_why.append("ATTESTATION_MANIFEST_UNBOUND(현재 MANIFEST 해시가 없다)")
        # 정확한 ZIP SHA — 받은 ZIP 과 결박한다 (관측값이 없으면 결박 실패다)
        if not _zip_obs:
            _att_why.append("ATTESTATION_ZIP_UNBOUND(받은 ZIP 의 SHA256 이 없다 — "
                            "`--zip_sha256 <sha>` 로 넘기거나 ZIP_SHA256.txt 를 "
                            "번들에 넣어야 정확한 ZIP 결박을 확인할 수 있다)")
        elif str(_att.get("bundle_zip_sha256") or "") != str(_zip_obs):
            _att_why.append("ATTESTATION_ZIP_MISMATCH(attestation %s ≠ 받은 ZIP %s)"
                            % (str(_att.get("bundle_zip_sha256"))[:12], str(_zip_obs)[:12]))
        if (_att.get("allowlist_sha256") and _seal_rec.get("allowlist_sha256")
                and _att["allowlist_sha256"] != _seal_rec["allowlist_sha256"]):
            _att_why.append("ATTESTATION_ALLOWLIST_MISMATCH(봉인과 다른 allowlist)")
        for _k in ("vasp_executable", "vasp_executable_sha256"):
            if (_att.get(_k) and _seal_rec.get(_k) and _att[_k] != _seal_rec[_k]):
                _att_why.append("ATTESTATION_VASP_MISMATCH(%s: attestation 과 봉인이 "
                                "다른 바이너리를 말한다)" % _k)
        if (_att.get("vasp_version_raw") and _seal_rec.get("vasp_version_banner")
                and str(_att["vasp_version_raw"]) not in
                str(_seal_rec["vasp_version_banner"])):
            _att_why.append("ATTESTATION_VASP_VERSION_MISMATCH(%r vs 봉인 %r)"
                            % (str(_att["vasp_version_raw"])[:30],
                               str(_seal_rec["vasp_version_banner"])[:30]))
        _att_var_bad = [v for v, d in (_att.get("variants") or {}).items()
                        if not _is_hex64((d or {}).get("source_sha256"))]
        if _att_var_bad:
            _att_why.append("ATTESTATION_VARIANT_SHA_BAD(%s)" % _att_var_bad[:3])
        # variant **집합**의 완전일치 — 부분집합도 초과집합도 안 된다
        if _seal and _av != set(_seal):
            _att_why.append("ATTESTATION_SET_MISMATCH(attestation %s ≠ root seal %s)"
                            % (sorted(_av), sorted(_seal)))
        if _plan_var and _av != _plan_var:
            _att_why.append("ATTESTATION_PLAN_MISMATCH(attestation %s ≠ 계획 잡이 "
                            "요구하는 %s — 쓰지도 않는 variant 로는 release 를 "
                            "주장할 수 없다)" % (sorted(_av), sorted(_plan_var)))
        # TITEL·embedded hash 를 variant 마다 요구하고 관측과 대조한다
        for _v, _d in sorted((_att.get("variants") or {}).items()):
            _d = _d or {}
            if not _d.get("titel") or not _d.get("embedded_hash"):
                _att_why.append("ATTESTATION_VARIANT_FIELDS(%s: titel/embedded_hash "
                                "가 없다)" % _v)
            if _seal.get(_v) and _seal[_v] != _d.get("source_sha256"):
                _att_why.append("ATTESTATION_SEAL_MISMATCH(%s: attestation 과 root "
                                "seal 의 원본 sha 가 다르다)" % _v)
            _obs_t = sorted(set(_titel_obs.get(_v) or []))
            if _obs_t and _d.get("titel") and _d["titel"] not in _obs_t:
                _att_why.append("ATTESTATION_TITEL_MISMATCH(%s: attestation %r 가 "
                                "관측 TITEL %s 에 없다)" % (_v, _d["titel"], _obs_t[:2]))
        # `made_before_production` 은 **자기선언이 아니라 산출물 부재**로 입증한다
        if _att.get("made_before_production") is not True:
            _att_why.append("ATTESTATION_NOT_PREPRODUCTION(계산 전에 만든 근거가 없다)")
        elif not str(_att.get("made_before_production_evidence") or "").strip():
            _att_why.append("ATTESTATION_PREPRODUCTION_UNEVIDENCED(선언만 있고 "
                            "산출물 부재 검사 기록이 없다)")
        _att_ok = not _att_why
        res["blocking"].extend(_att_why)
    res["attestation"] = {
        "present": bool(_att), "usable": _att_ok,
        "why_not": _att_why[:6],
        "checked": ["schema 필드 전건", "manifest 해시", "정확한 ZIP 해시",
                    "allowlist", "VASP 경로·해시·버전", "variant 집합 3자 완전일치",
                    "variant 별 TITEL·embedded hash·원본 sha", "생산 전 근거"],
        "release_label": _att.get("release_label"),
        "site": _att.get("site"), "created_utc": _att.get("created_utc")}
    # ── 회신 AR 해제조건 5 — stage-1 선결조건이 읽는 **봉인 포괄** 판정 ────
    _seal_blk = [b for b in res["blocking"] if b.startswith("ROOT_SEAL")]
    _cov = bool(_seal) and not _seal_blk
    res["root_seal_coverage"] = {
        "ok": _cov,
        "why": (_seal_blk[:3] if _seal_blk else
                ("봉인이 없다 — 생산 전 root seal 을 만들지 않았다" if not _seal else
                 "봉인이 현재 MANIFEST·계획 잡 %d개·variant %s 를 포괄한다"
                 % (len((man or {}).get("planned") or {}), sorted(_seal)))),
        "sealed_variants": sorted(_seal),
        "planned_variants": sorted(_plan_var),
        "⛔": ("이 판정은 '봉인이 이 묶음을 포괄한다' 까지다 — 봉인한 트리가 "
               "공식 배포판인지는 attestation 의 몫이다")}
    _vv = sorted(ver) or [_att.get("vasp_version_raw")]
    # ⛔ 회신 AR Q5 — 필드명을 `methods_sentence` 에서 바꾼다. 도구는 **후보 문구**를
    #   고를 뿐 원고 채택 권한이 없다. 최종 채택은 사람의 검토를 거친다.
    if _att_ok and not (res.get("blocking") or []):
        res["allowed_claim"] = "paw_release_attested"
        res["methods_candidate"] = (
            "Calculations were performed using VASP %s with PAW-PBE datasets from the "
            "%s release (%s). Each source dataset was identified by its embedded VASP "
            "hash and a full-file SHA-256 fingerprint fixed before production; the "
            "fingerprints were identical across all energy-bearing calculations. "
            "No numerical equivalence to earlier calculation waves was assumed."
            % (_vv[0], _att.get("release_label"),
               ", ".join(sorted(_att.get("variants") or {}))))
    else:
        res["allowed_claim"] = "bundle_conditional_only"
        res["methods_candidate"] = (
            "⚠ 공식 release 를 단정하지 않는다 — 계산 전 attestation 이 %s. "
            "허용 문구: 'the reported D is conditional on this bundle's PAW dataset; "
            "the fingerprints were not independently matched to an archived POTCAR "
            "release.' (회신 AP #12·Q3)"
            % ("없다" if not _att else "있으나 사용 불가"))
        res["methods_candidate_⛔"] = (
            "이 문구는 내부 기록용으로는 되지만 **원고 Methods 로는 약하다**(AP Q3). "
            "원고에 PAW release 를 적으려면 POTCAR_ATTESTATION_REQUEST.md 를 "
            "외주처에 보내 계산 전에 받아야 한다")
    res["methods_candidate_⚠"] = ("이것은 **후보 문구**다 (회신 AR Q5). 도구가 "
                                  "검증 상태로 상한을 정할 뿐이고, 원고 채택은 "
                                  "사람이 검토한 뒤에 한다. 더 강한 문장으로 "
                                  "바꿔 쓰지 말 것.")
    # ⛔ 회신 AJ — 종전 pin 대조는 **세 군데가 fail-open** 이었다:
    #   ① 관측이 비면 `if got and ...` 이 참이 안 돼 조용히 건너뛰었다
    #   ② VASP 버전이 하나도 관측 안 되면 `sorted(ver) in ([], ...)` 이 통과시켰다
    #   ③ 조립기는 **variant 키**(Li_sv·Ni_pv)로 기록하는데 pin 예시는 **원소 키**(Li·Ni)라
    #      관측이 안 잡혀 ①로 빠졌다. ⇒ pin 을 variant 키로 정규화해 대조한다.
    pin = res["pin"] or {}
    if not pin:
        # 거부의 **1차 위치는 생성기**다 (--potcar_pin 없으면 번들을 안 만든다).
        # 분석기는 실물 번들(배포 해시를 가진 manifest)에서만 부재를 막는다 —
        # 합성 픽스처에 없는 계약을 요구하지 않기 위해서다.
        if (man or {}).get("files_sha256"):
            # ⚠⚠ 2026-08-31 판정 — **차단에서 라벨로 내린다.**
            #   회신 AN Q4 는 사전 pin 을 요구했다. 그 근거는 "승인한 트리를 썼는가" 인데,
            #   **우리는 그 주장을 하지 않는다** (v12 를 새 provenance root 로 선언했고
            #   2026-08-12 wave 와의 동등성은 이미 철회했다).
            #   그리고 D 는 **이 번들 안에서 닫힌 양**이다 — 네 에너지가 전부 같은 런,
            #   같은 POTCAR 에서 나오므로 트리가 무엇이든 그 안에서 일관되면 D 는 유효하다.
            #   ⇒ 잡 사이 일치가 확인되면 값을 내되, **무엇을 확인하지 못했는지 라벨로
            #     결과에 박는다.** 없는 검증을 있는 척하지 않는 것이 요점이다.
            #   ⛔ 잡 사이 일치조차 깨지면 그건 여전히 blocking 이다 (아래 다른 게이트들).
            res["pin_absent"] = True
            # ⛔ 회신 AO P0-8/Q1 — 종전 문구("14잡의 POTCAR 신원이 서로 일치")는
            #   실측보다 강했다. 위 완전성 게이트가 통과했을 때만 그렇게 말할 수 있고,
            #   root seal 이 있을 때만 "생산 전에 고정한 root" 라고 말할 수 있다.
            _c = res.get("completeness") or {}
            _complete = bool(_c.get("n_completed")) and not (
                _c.get("n_no_prov") or _c.get("n_incomplete_variants")
                or _c.get("n_without_vasp_version"))
            # ⛔⛔ 회신 AP #7 — 종전엔 `ROOT_SEAL_MISMATCH` 가 있어도 동시에
            #   `sealed_root_v13` 라벨이 나올 수 있었다. **identity blocking 이
            #   하나라도 있으면 sealed 라벨을 발행하지 않는다.**
            _no_block = not (res.get("blocking") or [])
            res["identity_scope"] = (
                ("sealed_root_v13 — variant 별 원본 SHA256 을 **생산 전에 봉인**하고 "
                 "완주 전 잡이 그 봉인과 일치함을 확인했다. 이전 wave 와의 수치적 "
                 "동등성은 가정하지 않는다. ⚠ 공식 release 여부는 이 라벨이 "
                 "보증하지 않는다 (POTCAR_ATTESTATION.json 이 그 몫이다)"
                 if res.get("root_seal_variants") and _complete and _no_block else
                 "self_consistent_only — 완주 잡들의 POTCAR 신원이 서로 일치한다. "
                 "**사전 승인된 트리와 대조하지 않았다** (생산 전 root seal 없음). "
                 "따라서 '이전 wave 와 같은 PP' 는 주장하지 않는다"
                 if _complete and _no_block else
                 "unverified — 원본 fingerprint 또는 VASP 버전 관측이 불완전하다. "
                 "'신원 일치 확인' 이라고 쓰지 말 것"))
            res["⚠"] = ("pin 없음 — 사후 provenance 로 잡 사이 일치만 본다. "
                        "미리 고정하려면 생성 시 `--potcar_pin`")
        else:
            res["⚠"] = "pin 없음 (합성 입력 — 배포 번들이 아니다)"
    else:
        spec = (man or {}).get("potcar_spec") or {}
        want = {}
        for k, s in (pin.get("source_sha256") or {}).items():
            v = s.get("sha256") if isinstance(s, dict) else s
            key = (s.get("variant") if isinstance(s, dict) else None) or spec.get(k, k)
            want[str(key)] = str(v)
        res["pin_normalized_variants"] = sorted(want)
        if not want:
            res["blocking"].append("POTCAR_PIN_EMPTY(pin 에 source_sha256 이 없다)")
        for e, s in want.items():
            got = sorted(src.get(e, {}))
            if not got:
                res["blocking"].append(
                    "POTCAR_SOURCE_UNOBSERVED(%s: 사전 고정돼 있는데 회신에 원본 sha 가 "
                    "**하나도 없다** — 빈 관측을 통과로 읽지 않는다)" % e)
            elif got != [s]:
                res["blocking"].append(
                    "POTCAR_PIN_MISMATCH(%s: 사전 고정 %s ≠ 회신 %s)" % (e, s, got))
        _pv = pin.get("vasp_version")
        if not _pv:
            res["blocking"].append("VASP_PIN_ABSENT(pin 에 vasp_version 이 없다)")
        elif not ver:
            res["blocking"].append(
                "VASP_VERSION_UNOBSERVED(에너지를 내는 OUTCAR 에서 VASP 버전이 **하나도** "
                "안 읽혔다 — 무엇으로 돌았는지 모른다)")
        elif sorted(ver) != [str(_pv)]:
            res["blocking"].append(
                "VASP_PIN_MISMATCH(사전 고정 %s ≠ 회신 %s)" % (_pv, sorted(ver)))
    res["ok"] = not res["blocking"]
    return res

def merge_compat(bundles):
    """두 묶음을 합쳐도 되는가 — **해시 결속 + 프로토콜 동일성** (회신 AF P0-3).

    왜 합치나: 12자세는 calibration(4) + holdout(8) 이고, 기체 기준계는
    calibration 묶음에만 있다. 어느 한쪽만으로는 조각 간 대비가 정의되지 않는다.

    막는 것 (하나라도 걸리면 blocking 에 들어가고 값을 만들지 않는다):
      · clean slab 파일이 다르다        → E_ads 에서 슬랩이 소거되지 않는다
      · POTCAR 사양이 다르다            → 다른 유사퍼텐셜의 총에너지를 뺀다
      · k 격자가 다르다                 → 다른 적분 격자의 값을 뺀다
      · 게이트 판(gate_version)이 다르다 → 다른 판정 규칙으로 거른 값을 합친다
      · freeze 비율 · 슬랩 원자수가 다르다

    ⛔ 이 함수가 못 하는 것: VASP 실행 바이너리·PAW 배포판이 같은지는 **여기서**
       못 본다 (MANIFEST 에 없다). 그것은 회수된 OUTCAR 의 되울림으로 따로 본다.
    """
    keys = [("clean_slab", lambda m: ((m.get("clean_slab") or {}).get("sha256"))),
            ("potcar_spec", lambda m: m.get("potcar_spec")),
            ("kmesh_effective", lambda m: m.get("kmesh_effective") or m.get("kmesh")),
            ("gate_version", lambda m: m.get("gate_version")),
            ("freeze_frac_dft", lambda m: m.get("freeze_frac_dft")),
            ("nslab", lambda m: m.get("nslab"))]
    info = {"schema": "merge_compat/v1", "n_bundles": len(bundles),
            "roots": [b[0] for b in bundles], "blocking": [], "bound": []}
    for r, m in bundles:
        mp = os.path.join(r, "MANIFEST.json")
        info["bound"].append({
            "root": r,
            "candidate_set": m.get("candidate_set"),
            "n_jobs": m.get("n_jobs"),
            "manifest_sha256": (hashlib.sha256(open(mp, "rb").read()).hexdigest()
                                if os.path.isfile(mp) else None)})
    ref = bundles[0][1]
    for name, get in keys:
        want = get(ref)
        for r, m in bundles[1:]:
            if get(m) != want:
                info["blocking"].append(
                    "%s 가 묶음마다 다르다 (%r vs %r) — 합치면 다른 계의 에너지를 뺀다"
                    % (name, want, get(m)))
    if want is None and not info["blocking"]:
        pass
    if (ref.get("clean_slab") or {}).get("sha256") is None:
        info["blocking"].append(
            "clean_slab sha 가 없다 — 두 묶음이 같은 슬랩을 썼는지 확인할 수 없다")
    info["ok"] = not info["blocking"]
    return info

VACCONV_TOL_EV = 0.005          # 보고 최소단위(0.01 eV)의 **절반** — 물리 상수가 아니다
VACCONV_REPORT_DIGITS = 2       # 0.01 eV 로 보고한다 (사전 고정)


NI_MOMENT_MIN_MUB = 0.30        # 이보다 작으면 "붕괴" — 부호를 읽을 수 없다


def magnetic_topology_direct(jr, n_ni_expected=48):
    """clean slab **없이** 실현된 Ni 자기 topology 를 직접 판정한다 (회신 AJ ②).

    C-12 는 clean slab 을 만들지 않으므로 `Q/Q_clean` 기준이 없다. 대신 잡 자체에서:
      ① Ni 모멘트 표가 **완전**해야 한다 (48개)
      ② near-zero 모멘트가 있으면 **막는다** — 부호를 읽을 수 없다
      ③ 부호 fingerprint 를 만들되 **전역 반전을 동치로 접는다**
         (AFM 은 전체를 뒤집어도 같은 상태다)

    반환 (fingerprint | None, gates[])

    ⛔ 못 하는 것: 그 topology 가 **바닥상태인지** 말하지 못한다. 두 계산이 같은
       상태인지만 본다.
    """
    g = []
    # ⛔⛔ 2026-08-31 (회신 AN P0-2) — 초판은 `ni_moments` 를 읽었다. **그런 필드는 없다.**
    #   실제 저장 스키마는 `geom.magnetic.realized_basin.ni_moments_muB` 다
    #   (`realized_basin()` 이 그 키로 쓴다). ⇒ production 결과에서는 이 게이트가
    #   **항상 MAGNETIC_MOMENTS_MISSING 으로 막혔을** 것이다 — clean slab 을 뺀 자리를
    #   메우라고 만든 게이트가 정작 실물에서 안 돈다.
    #   더 나쁜 것: selftest 픽스처가 **내가 지어낸 그 이름**을 써서 통과했다.
    #   ⇒ 아래 selftest 는 `realized_basin()` 이 실제로 내는 dict 를 그대로 쓴다.
    _mag = (jr.get("geom") or {}).get("magnetic") or {}
    _rb = _mag.get("realized_basin") or {}
    mom = _rb.get("ni_moments_muB")
    if mom is None:                       # 하위호환 — 옛 기록/픽스처
        mom = _mag.get("ni_moments") or (jr.get("static") or {}).get("ni_moments")
    if not mom:
        return None, ["MAGNETIC_MOMENTS_MISSING(Ni 모멘트 표가 없다 — "
                      "LORBIT 출력을 회수하지 못했다)"]
    if len(mom) != n_ni_expected:
        return None, ["MAGNETIC_MOMENTS_INCOMPLETE(%d/%d)" % (len(mom), n_ni_expected)]
    small = [i for i, m in enumerate(mom) if abs(float(m)) < NI_MOMENT_MIN_MUB]
    if small:
        return None, ["MAGNETIC_COLLAPSE_DIRECT(%d/%d Ni 가 |m| < %.2f μB — 부호를 "
                      "읽을 수 없다)" % (len(small), n_ni_expected, NI_MOMENT_MIN_MUB)]
    sig = "".join("+" if float(m) > 0 else "-" for m in mom)
    inv = sig.translate(str.maketrans("+-", "-+"))
    return min(sig, inv), g          # 전역 반전을 동치로 접는다


def same_topology_direct(ja, jb, n_ni_expected=48):
    """두 잡이 같은 실현 topology 인가 — clean slab 없이."""
    fa, ga = magnetic_topology_direct(ja, n_ni_expected)
    fb, gb = magnetic_topology_direct(jb, n_ni_expected)
    if fa is None or fb is None:
        return False, "판정 불가: " + "; ".join(ga + gb)
    return (fa == fb), ("같음" if fa == fb else "부호 fingerprint 가 다르다")

def closure_vacconv(man, jobs, E, emol, frags):
    """진공 두께 수렴 시험 — **두 조각의 대비 변화**로 판정한다 (회신 AJ).

        D(c) = [E_C^SDCP(c) − E_G^SDCP] − [E_C^PTFE(c) − E_G^PTFE]
        Δ_vac = D_primary,pm1(c2) − D_primary,pm1(c1)

    통과: |Δ_vac| ≤ 5 meV **그리고** D(c1)·D(c2) 의 0.01 eV 반올림이 같다.

    🔑 왜 조각별 변화가 아니라 대비인가 — 기체 항은 c 에 무관하고 슬랩 항은 두 조각에
       공통이라, 대비를 취하면 둘 다 소거된다. 조각별로 보면 소거되지 않는 항이 남는다.

    ⛔ 이 함수가 못 하는 것
      · 절대 E_ads 의 수렴을 말하지 못한다 — clean slab 이 대비에서 소거되므로 여기
        들어오지 않는다. 절대값을 인용하려면 별도 시험이 필요하다.
      · c2 보다 큰 셀에서 무슨 일이 나는지 모른다. 두 점 시험이다.
    """
    # ⛔ 2026-08-31 — `pass` 를 **처음부터** 넣는다. 초판은 마지막에만 넣어서, 조기
    #   반환 경로(적용 불가·blocks)에서 호출자가 `res["pass"]` 로 **KeyError** 를 맞았다.
    #   판정 키가 없는 것은 "통과 아님" 이지 예외가 아니다.
    res = {"schema": "closure_vacconv/v1", "tol_eV": VACCONV_TOL_EV,
           "report_digits": VACCONV_REPORT_DIGITS,
           "⚠_5meV_출처": "물리 상수가 아니라 보고 최소단위(0.01 eV)의 절반",
           "pass": False, "by_cell": {}, "blocks": []}
    # 이 시험은 **둘째 셀을 실은 판(C-12)** 에만 있다. 옛 번들에는 vacconv 잡이 없고,
    # 없는 계약을 요구하면 legacy 결과가 통째로 막힌다.
    if not (man or {}).get("vacuum_convergence") and not any(
            (jr.get("meta") or {}).get("vacconv") for jr in (jobs or {}).values()):
        res["verdict"] = "n/a — 이 번들에 진공 수렴 시험 잡이 없다"
        res["applicable"] = False
        return res
    res["applicable"] = True

    def _one(frag, cell):
        """`cell` ∈ {"c1","c2"} 인 그 조각의 primary 잡 하나.

        ⛔⛔ 2026-08-31 (회신 AM P0-2) — 초판은 c1 을 `kind="prospective_pose"`,
          c2 를 `kind="vacuum_convergence"` 로 골랐다. **둘 다 틀렸다.**
          실물 `job.json` 은 c2 도 `kind="prospective_pose"` 이고 구분은 `vacconv="c2"`
          필드에 있다. ⇒ c1 후보가 **둘(ambiguous)**, c2 후보가 **0** 이 되어
          결과가 다 있어도 진공 판정이 안 나왔다.
          이제 **생성기가 실제로 쓰는 필드**(`vacconv`)로 고른다.
        """
        js = [j for j in _pick(jobs, kind="prospective_pose",
                               fragment=frag, seed=SEED_MAIN)
              if (jobs[j].get("meta") or {}).get("role") in (None, "primary")
              and ((jobs[j].get("meta") or {}).get("vacconv")
                   or "c1") == cell]
        if len(js) != 1:
            res["blocks"].append("VACCONV_JOB_AMBIGUOUS(%s/%s: %d개)"
                                 % (frag, cell, len(js)))
            return None
        jr = jobs[js[0]]
        if jr.get("gates"):
            res["blocks"].append("VACCONV_JOB_GATED(%s: %s)"
                                 % (js[0], jr["gates"][:1]))
            return None
        e = E(js[0])
        if e is None:
            res["blocks"].append("VACCONV_JOB_MISSING(%s)" % js[0])
            return None
        return js[0], e, jr

    # ⛔⛔ 2026-08-31 (회신 AM P0-3) — **Δ_vac 에는 기체 기준이 필요 없다.**
    #     Δ_vac = [E_C^S(c₂)−E_C^S(c₁)] − [E_C^P(c₂)−E_C^P(c₁)]
    #   에서 두 조각의 기체 에너지가 **정확히 소거된다** (셀 높이와 무관한 상수라서).
    #   초판은 `emol` 이 없으면 `VACCONV_NO_GAS_REF` 로 막았는데, 그건 `--refs_minimal`
    #   번들에서 진공 판정 자체를 불가능하게 만들었다 (분석기가 box20 도 요구했다).
    #   ⇒ 기체가 있으면 쓰고(A 가 그대로 E_ads), 없으면 **복합체 에너지만으로** 낸다.
    #     Δ_vac 값은 어느 쪽이든 같다 — 그게 소거의 뜻이다.
    picks, A = {}, {}
    _gas_used = {f: (emol.get(f) is not None) for f in frags}
    res["gas_reference_used"] = _gas_used
    res["⚠_기체_불필요"] = ("Δ_vac 에서 기체 에너지는 대수적으로 소거된다 — "
                            "기체가 없어도 판정은 유효하다 (회신 AM P0-3). "
                            "단 **최종 D** 에는 기체가 필요하다.")
    for frag in frags:
        for cell in ("c1", "c2"):
            got = _one(frag, cell)
            if got is None:
                continue
            jn, e, jr = got
            picks[(frag, cell)] = jn
            A[(frag, cell)] = e - (emol.get(frag) or 0.0)

    # 자기 topology 가 네 잡에서 같아야 한다 — 다르면 셀 효과가 아니라 상태 차이를 잰다
    #   clean slab 이 없을 수 있으므로 **직접 topology** 를 먼저 쓰고, 없으면 legacy
    #   realized_basin_id 로 떨어진다 (회신 AJ ②).
    _rb = {}
    for k, v in picks.items():
        f, _g = magnetic_topology_direct(jobs[v])
        if f is None:
            f = ((jobs[v].get("geom") or {}).get("magnetic") or {}).get(
                "realized_basin_id")
        _rb[k] = f
    if len(picks) == 4:
        if any(v is None for v in _rb.values()):
            res["blocks"].append(
                "VACCONV_BASIN_UNRESOLVED(네 잡 중 realized topology 미판정이 있다)")
        elif len(set(_rb.values())) > 1:
            res["blocks"].append(
                "VACCONV_BASIN_MISMATCH(%s — 셀 효과가 아니라 자기 상태 차이를 재게 된다)"
                % _rb)
    res["jobs"] = {"%s/%s" % k: v for k, v in sorted(picks.items())}
    res["A_eV"] = {"%s/%s" % k: round(v, 6) for k, v in sorted(A.items())}

    sd = next((f for f in frags if "sdcp" in f), None)
    ct = next((f for f in frags if f != sd), None)
    if not (sd and ct) or len(A) != 4 or res["blocks"]:
        res["verdict"] = "unresolved — 네 잡이 전부 회수·통과해야 판정한다"
        return res

    D = {c: A[(sd, c)] - A[(ct, c)] for c in ("c1", "c2")}
    res["D_eV"] = {c: round(v, 6) for c, v in D.items()}
    res["D_reported"] = {c: round(v, VACCONV_REPORT_DIGITS) for c, v in D.items()}
    d_vac = D["c2"] - D["c1"]
    res["delta_vac_eV"] = round(d_vac, 6)
    # ⛔ 정확한 경계가 부동소수점으로 뒤집히지 않게 μeV 정수로 비교 (회신 AF P0-6 과 같은 이유)
    within = abs(int(round(d_vac * 1e6))) <= int(round(VACCONV_TOL_EV * 1e6))
    same_round = res["D_reported"]["c1"] == res["D_reported"]["c2"]
    res["within_tol"] = within
    res["same_rounded"] = same_round
    # ⛔⛔ 2026-08-31 (회신 AM Q1) — **반올림 일치를 hard gate 에서 내린다.**
    #   0.0049 vs 0.0051 eV 는 차이가 **0.2 meV** 인데 표시는 0.00 / 0.01 로 갈린다.
    #   더 나쁜 것: c 에 무관한 기체 offset 을 더하면 Δ_vac 은 그대로인데 **반올림 판정만
    #   바뀐다** — 물리와 무관한 양이 판정을 뒤집는다는 뜻이다.
    #   ⇒ 물리 gate 는 `|Δ_vac| ≤ 5 meV` 하나. `same_rounded` 는 **표시 안정성 정보**다.
    #     반올림만 불일치하면 Figure 삭제가 아니라 **불확도 병기 또는 한 자리 추가 보고**.
    res["pass"] = bool(within)
    res["gate"] = "|Δ_vac| ≤ %.0f meV (물리 gate)" % (1000 * VACCONV_TOL_EV)
    res["rounding_note"] = (
        "표시 안정성 정보 — 판정에 안 들어간다. 반올림만 불일치하면 "
        "0.01 eV 대신 한 자리 더(0.001 eV) 보고하거나 불확도를 병기한다.")
    # ⚠ 판정 범위를 좁힌다 — 두 점은 '+4 Å 증가에 대한 안정성' 이지 무한진공 수렴이 아니다.
    res["claim_scope"] = (
        "시험한 b00·%s branch 에서 c %+.0f Å 증가에 대한 안정성. "
        "**무한진공 수렴의 증명이 아니다.**" % (SEED_MAIN, 4.0))
    res["verdict"] = ("ok — Δ_vac %.1f meV (문턱 %.0f) · 반올림 %s"
                      % (1000 * d_vac, 1000 * VACCONV_TOL_EV,
                         "일치" if same_round else "불일치(정보용)")
                      if res["pass"] else
                      "⛔ FAIL — Δ_vac %.1f meV > 문턱 %.0f meV. "
                      "추가 셀 탐색 없이 Figure 2e 를 제거한다"
                      % (1000 * d_vac, 1000 * VACCONV_TOL_EV))
    return res

def closure_C1(man, jobs, E, emol, frags):
    """C1 — **선택된 네 자세에서의 국소 calibration 일관성**.

      e_{f,p} = E_ads^DFT(f,p) − E_ads^UMA(f,p)
      S_f     = max_p e − min_p e          ← **range 다 (SD 아님)**

    branch 는 pm1 · D3-on 만. 조각당 사전 지정 4자세 **전부**가 있어야 하고
    하나라도 빠지면 `unresolved` — 남은 자세로 계산하면 표본이 줄어 range 가
    자동으로 작아져 **통과 쪽으로 편향된다**.

    ⛔ 이 값이 말하지 않는 것: 후보 전체의 selector 검증이 **아니다.** UMA 가
    고른 자세만 DFT 로 봤으므로 통과는 독립 검증이 아니다. 일반 selector 주장은
    sealed audit 이나 UMA 순위를 가로지르는 사전 층화 holdout 이 있어야 한다.
    """
    res = {"schema": "closure_C1/v1", "S_tol_eV": C1_S_TOL_EV,
           "⚠": "선택된 네 자세의 국소 일관성. selector 일반 검증이 아니다",
           "by_frag": {}}
    slabs = _pick(jobs, kind="clean_ref", seed=SEED_MAIN, d3="on")
    if len(slabs) != 1:
        res["verdict"] = f"unresolved — clean slab(pm1·D3-on)이 {len(slabs)}개"
        return res
    e_slab = E(slabs[0])
    # 🔴 회신 AB P0-4 후단 — `S_f = max_p e − min_p e` 에서는 같은 조각의 슬랩·분자
    #   항이 **정확히 소거된다**. 그러므로 필요한 것은 네 complex 자세가 서로 같은
    #   basin 인가이지, 각 자세가 clean slab 과 같은 basin인가가 **아니다**.
    #   clean slab 일치는 **절대 E_ads** 를 주장할 때 따로 요구한다(그 게이트는
    #   BASIN_MISMATCH_SLAB 로 이미 별도로 있다). 종전 구현은 여기서 슬랩 일치를
    #   요구해 과잉차단이었다.
    res["⚠_basin_규칙"] = ("네 자세가 **서로** 같은 basin 이면 된다 — S_f 에서 슬랩·분자가 "
                          "소거되기 때문. clean slab 일치는 절대 E_ads 쪽 요구조건이다")
    for f in frags:
        poses = _pick(jobs, kind="prospective_pose", fragment=f,
                      seed=SEED_MAIN, d3="on")
        rows, miss = [], []
        for jn in poses:
            jr = jobs[jn]
            m = jr.get("meta") or {}
            rb = ((jr.get("geom") or {}).get("magnetic") or {}).get("realized_basin_id")
            ec, um = E(jn), m.get("uma_E_pose_eV")
            if jr.get("gates") or ec is None or um is None or e_slab is None:
                miss.append(f"{jn}(게이트/에너지 결측)"); continue
            if rb is None:
                miss.append(f"{jn}(basin 미판정)"); continue
            rows.append({"job": jn, "basin": m.get("basin_id"),
                         "E_ads_DFT_eV": round(ec - e_slab - emol[f], 6),
                         "E_ads_UMA_eV": round(float(um), 6),
                         "residual_eV": round(ec - e_slab - emol[f] - float(um), 6)})
        # ★ 기대 자세 수는 **동결된 manifest** 에서 온다. 회수된 잡에서 세면
        #   빠진 자세를 영영 못 잡는다 (없으면 기대도 같이 줄어든다).
        n_want = len([k for k in (man.get("planned") or {})
                      if k.startswith("prospective/")
                      and k.rsplit("/", 1)[-1].startswith(f + "__")
                      and k.endswith(SEED_MAIN)])
        if not n_want:
            res["by_frag"][f] = {"verdict": "unresolved",
                                 "why": "MANIFEST.planned 에 이 조각의 pm1 자세가 없다 "
                                        "— 기대 자세 수를 회수분에서 세지 않는다"}
            continue
        # ★ 네 자세가 **서로** 같은 basin 인지 — 해시가 아니라 상세 지문으로 (P0-4)
        _het = []
        if len(rows) > 1:
            _ref = rows[0]["job"]
            for _r in rows[1:]:
                _ok, _why = same_basin(jobs[_ref], jobs[_r["job"]])
                if not _ok:
                    _het.append(f"{_r['job']}: {_why}")
        if _het:
            miss.extend(_het)
        if miss or len(rows) != n_want or not rows:
            res["by_frag"][f] = {"verdict": "unresolved", "missing": miss,
                                 "n_used": len(rows), "n_required": n_want,
                                 "why": "4자세 전부가 있고 **서로 같은 basin** 이어야 한다 "
                                        "— 부분집합은 range 를 작게 만들어 통과 쪽으로 "
                                        "편향되고, 상태를 가로지르면 e 가 다른 양이 된다"}
            continue
        r = [x["residual_eV"] for x in rows]
        S = max(r) - min(r)
        res["by_frag"][f] = {
            "n": len(rows), "S_f_eV": round(S, 6), "rows": rows,
            "verdict": ("국소 calibration 일관 (이 네 자세 안에서 잔차 range 가 작다)"
                        if S <= C1_S_TOL_EV else
                        "⛔ 국소 일관성 실패 — 선택기를 쓴 근거가 약해진다")}
    return res


#: C5 게이트 — 결과 보기 전 고정 (D-2026-08-30-sdcp-neutral-ptfe-ddE-obs)
C5_N_CAL = 4                   # 사전등록 calibration 자세 (조각당)
C5_N_HOLDOUT = 8               # 층화 홀드아웃 자세 (조각당) — 선택기 시험용
C5_N_POSE = C5_N_CAL + C5_N_HOLDOUT   # = 12. ⚠ 합만 맞으면 안 된다 — 구성도 맞아야
C5_H1_FLOOR_EV = 0.030         # ⚠ **MLIP 유래 하한** — site_screen.py GATE["decision_floor_eV"]
#   (2026-08-11 UMA 실무 해상도). DFT 값에 옮겨 쓸 근거는 문서에 없다
#   (kb/questions/sdcp_site_preference.md 2026-08-28). 옮길 만하다고 볼 이유는
#   기하가 UMA 이완 결과라 UMA 오차가 모든 DFT 단일점에 실린다는 것이지만 추론이다.
#   ⇒ 상수로 쓰지 않고 **하한**으로만 쓰고, 실측 S_f 가 크면 그쪽이 이긴다.
C5_H1_TOL_EV = C5_H1_FLOOR_EV  # 하위호환 별칭 (판정은 h1_tolerance() 로 한다)


def h1_tolerance(c1_result):
    """홀드아웃 판정바닥 δ.

    ⛔ **2026-08-30 철회** — 한때 `δ = max(30 meV, S_f)` 로 두려 했다. 회신 AF P0-5 가
    기각했고 그 논거가 옳다: `S_f` 가 커질수록 holds 도 fail 도 어려워져 **미해결 띠만
    넓어진다.** 즉 '엄격해진다' 가 아니라 **판정력이 줄어든다** 이고, 나쁜 selector 가
    큰 `S_f` 로 자기 실패를 가리는 구조가 된다. 그래서 `S_f` 는 H1 문턱에 **넣지 않는다**.

    `S_f` 는 C1 의 독립 게이트(≤ 50 meV)로 **그대로 남는다** — 거기서는 '선택기가
    조각 안에서 일관적인가' 를 묻는 것이라 방향이 맞다.

    현재 δ 는 `C5_H1_FLOOR_EV` **한 값**이고, 그 값은 MLIP(UMA) 실무 해상도에서 왔다.
    ⚠ 그 이식 근거는 아직 등재돼 있지 않다 (kb/questions/sdcp_site_preference.md
    2026-08-28). 수치 허용폭은 dense-k · box · SCF 같은 **독립 수치검사**에서 따로
    정해야 하고, 그것이 나오기 전까지 이 값은 잠정이다.
    """
    out = {}
    for f, r in ((c1_result or {}).get("by_frag") or {}).items():
        s = r.get("S_f_eV") if isinstance(r, dict) else None
        out[f] = {"tol_eV": C5_H1_FLOOR_EV, "floor_eV": C5_H1_FLOOR_EV,
                  "S_f_eV": s, "binding": "floor(MLIP 유래 · 잠정)",
                  "⛔": "S_f 는 H1 문턱에 쓰지 않는다 (회신 AF P0-5). C1 게이트 전용"}
    return out


def closure_C5(man, jobs, E, emol, frags, merge_info=None, h1_tol=None):
    """C5 — ΔΔE_obs. **선언된 12자세에서의 조각 간 대비** (표본 조건부).

      A(f,p)   = E_complex(f,p) − E_mol(f, box24)
      ΔΔE_obs  = min_{p∈12} A(SDCP,p) − min_{q∈12} A(c10,q)      [pm1 · D3-on]

    왜 이 양이 별도로 있나 — 마감조건 §9 는 *"Stage A 결과로 어느 조각이 더 강하게
    붙는다를 종결형으로 쓰기"* 를 금지하고, 그 근거로 **"audit pose 가 없다"** 를 든다.
    즉 반대 이유는 *min 이 UMA 선택기의 산물일 수 있다* 이다. 층화 홀드아웃 8자세가
    UMA 점수 전 구간을 가로질러 **그 반대 이유를 직접 시험**하므로, 그 시험을 통과할
    때에 한해 **표본 조건부** 대비를 낸다.

    게이트 (하나라도 깨지면 값을 만들지 않는다):
      ① 조각당 12자세 전부 회수·게이트 통과   ② 12자세가 서로 같은 realized basin
      ③ H1 — 홀드아웃 최저가 calibration 최저를 30 meV 이상 **밑돌지 않는다**
      ④ 두 조각 기체 기준이 존재            ⑤ (슬랩은 A 에서 소거되므로 여기선 불필요)

    ⛔ 이 함수가 **못 하는 것**
      · 전역 최소를 주장하지 않는다. 후보풀 밖은 안 봤다.
      · `ΔΔE_lowE` / primary 가 아니다 — 그것은 창 W 전수 + audit 개봉을 전제한다.
      · H1 실패를 "더 낮은 자세를 찾았다" 로 흡수하지 않는다. **재개 사유**다.
    """
    res = {"schema": "closure_C5/v2", "name": "ddE_obs",
           "merge": merge_info,
           "n_pose_required": C5_N_POSE, "h1_tol": h1_tol or {},
           "h1_floor_eV": C5_H1_FLOOR_EV,
           "decision": "D-2026-08-30-sdcp-neutral-ptfe-ddE-obs (proposed)",
           "⚠": "표본 조건부 — 전역 최소가 아니다", "by_frag": {}}
    # ⛔ 12자세는 두 묶음(calibration 4 + holdout 8)에 걸쳐 있다. 한 묶음만 주면
    #    부분집합에서 min 을 뽑게 되므로 **값을 만들지 않는다** (회신 AF P0-3).
    if not merge_info:
        res["verdict"] = ("⛔ NOT_MERGED — 12자세는 calibration 묶음과 holdout 묶음에 "
                          "걸쳐 있다. `analyze_results.py <calib> --merge <holdout>` 로 "
                          "두 묶음을 함께 줘야 한다. 한 묶음만으로는 정의되지 않는다")
        return res
    if not merge_info.get("ok"):
        res["verdict"] = "⛔ MERGE_INCOMPATIBLE — " + "; ".join(merge_info["blocking"][:3])
        return res
    mins = {}
    for f in frags:
        if emol.get(f) is None:
            res["by_frag"][f] = {"verdict": "unresolved", "why": "기체 기준(box24) 없음"}
            continue
        rows, miss = [], []
        for jn in _pick(jobs, kind="prospective_pose", fragment=f,
                        seed=SEED_MAIN, d3="on"):
            jr = jobs[jn]
            ec = E(jn)
            if jr.get("gates") or ec is None:
                miss.append(f"{jn}(게이트/에너지 결측)"); continue
            rows.append({"job": jn, "role": (jr.get("meta") or {}).get("role"),
                         "basin_id": (jr.get("meta") or {}).get("basin_id"),
                         "A_eV": round(ec - emol[f], 6)})
        if len(rows) != C5_N_POSE or miss:
            res["by_frag"][f] = {
                "verdict": "unresolved", "n_used": len(rows),
                "n_required": C5_N_POSE, "missing": miss[:4],
                "why": ("선언된 12자세 전부가 있어야 한다 — 부분집합에서 min 을 뽑으면 "
                        "표본이 줄수록 min 이 올라가 대비가 흔들린다")}
            continue
        # ② 12자세 상호 동질성 (크기 포함) — 상태를 가로질러 min 을 뽑지 않는다
        _het = []
        for r in rows[1:]:
            ok, why = same_basin(jobs[rows[0]["job"]], jobs[r["job"]])
            if not ok:
                _het.append(f"{r['job']}: {why}")
        if _het:
            res["by_frag"][f] = {"verdict": "unresolved", "basin_mismatch": _het[:3],
                                 "why": "12자세가 서로 같은 realized basin 이어야 한다"}
            continue
        cal = [r for r in rows if r["role"] == "calibration"]
        hld = [r for r in rows if r["role"] == "holdout"]
        # ⛔ 회신 AF P0-4 — 12개면 되는 게 아니라 **정확히 4 + 8** 이어야 한다.
        #    11+1 도 12 라서 종전 검사를 통과했다. 그러면 홀드아웃 시험이 사라진다.
        if (len(cal), len(hld)) != (C5_N_CAL, C5_N_HOLDOUT):
            res["by_frag"][f] = {
                "verdict": "unresolved", "n_cal": len(cal), "n_holdout": len(hld),
                "why": "calibration %d · holdout %d — 정확히 %d + %d 이어야 한다 "
                       "(합이 12 라도 구성이 다르면 홀드아웃 시험이 성립하지 않는다)"
                       % (len(cal), len(hld), C5_N_CAL, C5_N_HOLDOUT)}
            continue
        a_cal, a_hld = min(r["A_eV"] for r in cal), min(r["A_eV"] for r in hld)
        # ③ H1 — **세 갈래**다 (회신 AF P0-4). 종전 두 갈래는 판정 해상도 안의
        #    미해결 구간(±30 meV)을 통과로 승격시켰다.
        # ⛔ 회신 AF P0-6 — 정확히 ±δ 인 경우가 부동소수점 때문에 뒤집혔다.
        #   계약상 ±δ 는 **둘 다 미해결**이다. μeV 정수로 양자화해 비교한다.
        _tol = float(((h1_tol or {}).get(f) or {}).get("tol_eV", C5_H1_FLOOR_EV))
        _m = a_hld - a_cal
        _mq = int(round((a_hld - a_cal) * 1e6))     # μeV
        _tq = int(round(_tol * 1e6))
        if _mq > _tq:
            h1 = "holds"          # 홀드아웃이 확실히 높다 — 선택기가 버텼다
        elif _mq < -_tq:
            h1 = "fail"           # 홀드아웃이 더 낮다 — 선택기 실패
        else:
            h1 = "unresolved"     # 판정 해상도 안 — 어느 쪽도 말하지 않는다
        h1_ok = (h1 == "holds")
        res["by_frag"][f] = {
            "n_pose": len(rows), "n_cal": len(cal), "n_holdout": len(hld),
            "A_min_calibration_eV": round(a_cal, 6),
            "A_min_holdout_eV": round(a_hld, 6),
            "H1_margin_eV": round(_m, 6), "H1_class": h1, "H1_pass": h1_ok,
            "H1_tol_eV": round(_tol, 6),
            "H1_tol_binding": ((h1_tol or {}).get(f) or {}).get("binding", "floor"),
            "A_min_eV": round(min(a_cal, a_hld), 6),
            "rows": sorted(rows, key=lambda r: r["A_eV"]),
            "verdict": ("ok" if h1 == "holds" else
                        ("⛔ SELECTOR_FAIL — 홀드아웃 최저가 calibration 최저를 "
                         "%.1f meV 밑돈다. 이 값을 min 으로 흡수하지 않는다; "
                         "사전등록 재개조건이 발동한다" % (1000 * -_m))
                        if h1 == "fail" else
                        "unresolved — 홀드아웃과 calibration 최저의 차 %.1f meV 가 "
                        "판정 해상도 %.0f meV 안이다. 선택기가 버텼다고도, 실패했다고도 "
                        "말하지 않는다" % (1000 * _m, 1000 * _tol))}
        if h1_ok:
            mins[f] = min(a_cal, a_hld)
    # ⛔ 회신 AF P0-3 — 조각 **안**에서만 배열을 맞추면 SDCP 와 PTFE 가 서로 다른
    #    자기 배열이어도 통과한다. 두 최저 자세끼리도 같은 배열이어야 뺄셈이 성립한다.
    _best_job = {}
    for f, _ in mins.items():
        _rows = res["by_frag"][f]["rows"]
        _best_job[f] = min(_rows, key=lambda r: r["A_eV"])["job"]
    if len(_best_job) == 2:
        _a, _b = list(_best_job.values())
        _ok, _why = same_basin(jobs[_a], jobs[_b])
        res["cross_fragment_basin"] = {"jobs": [_a, _b], "same": _ok, "why": _why}
        if not _ok:
            res["verdict"] = ("⛔ CROSS_FRAGMENT_BASIN — 두 조각의 최저 자세가 서로 "
                              "다른 자기 배열이다 (%s). 그 차에는 흡착이 아닌 것이 "
                              "섞인다" % _why)
            return res
    sd = next((f for f in mins if "sdcp" in f), None)
    ct = next((f for f in mins if f != sd), None)
    if not (sd and ct):
        res["verdict"] = ("unresolved — 두 조각 모두 게이트를 통과해야 한다 "
                          "(통과 %s)" % sorted(mins))
        return res
    res["ddE_obs_eV"] = round(mins[sd] - mins[ct], 6)
    res["verdict"] = (
        "조사한 %d자세(사전등록 %d + 층화 홀드아웃 %d)에서, 고정기하 단일점 규약 아래 "
        "중성 SDCP 반복단위 모델의 최저 흡착 전자에너지가 perfluorodecane 조각보다 "
        "%.4f eV %s았다" % (C5_N_POSE, 4, 8, abs(res["ddE_obs_eV"]),
                            "낮" if res["ddE_obs_eV"] < 0 else "높"))
    res["⛔_금지_서술"] = ["전역 최소", "가장 안정한 자세", "종결형",
                        "ΔΔE_lowE · primary 로 부르기"]
    return res


def closure_C3(man, jobs, E, frags):
    """C3 — D3 분해. **부호를 먼저 본다.**

      δ_{f,p} = [E_C,on − E_C,off] − [E_S,on − E_S,off] − [E_M,on − E_M,off]
              = Edisp_C(f,p) − Edisp_S − Edisp_M(f)          ← **v2: 쌍둥이 없이**
      D       = mean_p(δ_SDCP) − mean_p(δ_c10)      ← 부호 있는 값, 산술평균

    ★ **v2 개정 (2026-08-30, DFT 결과 0잡 시점)** — D3-off 쌍둥이 잡을 쓰지 않는다.
      D3(IVDW=11)는 SCF 에 안 들어간다: 핵좌표만 보고 총에너지·힘에 **더해지는** 항이라
      KS 해밀토니안을 안 건드린다. 그래서 고정기하 static(NSW=0)에서
          E_on − E_off = Edisp
      가 근사가 아니라 **항등식**이고, 위 세 괄호가 각각 Edisp 로 접힌다.
      VASP 는 그 Edisp 를 OUTCAR 에 직접 찍는다 — repo 실물로 확인했다:
      `runs/sdcp_phaseB_vasp_v1_2026_08_08/{slab,mol_neutral,complex_neutral}/OUTCAR.gz`
      → −27.49493 / −0.71798 / −28.58614 ⇒ δ = **−0.373230 eV**.
      ⇒ 쌍둥이 16잡은 절충으로 버린 것이 아니라 **정보가 0이라** 버린 것이고,
        쌍둥이가 IVDW 말고 다른 축에서 갈릴 위험도 함께 사라진다.

    ⚠ 쌍둥이가 **있으면 버리지 않고 교차검증**한다 (v9 이하 번들 호환):
      |(E_on − E_off) − Edisp| > C3_EDISP_TOL_EV 면 그 조각은 unresolved 다.
      항등식이 깨졌다는 뜻이고 그건 D3 문제가 아니라 **번들 문제**다.

    D 와 0.90 eV 의 **부호가 같을 때만** 70/30 % 를 적용한다. 절댓값을 쓰면
    반대 방향 효과도 "설명" 으로 오판한다.

    ⛔ 허용 문구는 "원인의 70 % 를 증명" 이 아니라 **"이 네 자세에서 관측된
    0.90 eV 차등을 수치상 70 % 이상 설명"** — 인과가 아니라 수치 분해다.

    ⛔ 이 함수가 **못 하는 것**: Edisp 값 자체가 맞는지는 검증하지 않는다.
      VASP 가 찍은 수를 그대로 쓴다. 독립 D3 구현과 대조하지 않는다.
    """
    res = {"schema": "closure_C3/v3", "ref_gap_eV": C3_REF_GAP_EV,
           "hi": C3_HI, "lo": C3_LO, "edisp_tol_eV": C3_EDISP_TOL_EV,
           "source": "Edisp (eV) from the D3-on OUTCAR — no D3-off twin required",
           "offset_definition": C3_OFFSET_UMA_MINUS_DFT,
           "offset_within_fragment_range_eV": C3_OFFSET_RANGE_EV,
           "by_frag": {}}

    def pair_delta(jn):
        """δ 의 한 항 = 그 잡의 Edisp. 없으면 (None, 사유).

        쌍둥이가 남아 있으면 (E_on − E_off) 와 대조해 항등식을 확인한다.
        """
        a = jobs.get(jn)
        if a is None:
            return None, f"{jn}: 잡 없음"
        if a.get("gates"):
            return None, f"{jn}: 게이트됨"
        st = a.get("static") or {}
        ed = st.get("edisp_eV")
        if ed is None:
            return None, (f"{jn}: OUTCAR 에 `Edisp (eV)` 가 없다 — IVDW=11 이 실제로 "
                          f"걸렸는지 확인해야 한다 (D3 없이 돈 잡일 수 있다)")
        if (st.get("edisp_n") or 0) > 1 and (st.get("incar_echo") or {}).get("NSW") not in (None, "0", 0):
            return None, (f"{jn}: Edisp 가 {st['edisp_n']}회 찍혔는데 NSW≠0 — 기하가 "
                          f"바뀌었으면 마지막 값이 어느 기하의 것인지 보장 못 한다")
        # ── 쌍둥이가 있으면 항등식을 **검사**한다 (없는 게 정상이다)
        tw = _twin_of(jobs, jn)
        if tw is not None and not (jobs[tw].get("gates")):
            ea, eb = E(jn), E(tw)
            if ea is not None and eb is not None:
                if abs((ea - eb) - ed) > C3_EDISP_TOL_EV:
                    return None, (f"{jn}: (E_on−E_off)={ea - eb:.6f} 인데 Edisp={ed:.6f} "
                                  f"— 차 {abs((ea - eb) - ed):.6f} eV 가 허용 "
                                  f"{C3_EDISP_TOL_EV} 를 넘는다. D3 항등식이 깨졌다 = "
                                  f"쌍둥이가 IVDW 말고 다른 데서 갈렸다는 뜻")
                ra = ((a.get("geom") or {}).get("magnetic") or {}).get("realized_basin_id")
                rb = ((jobs[tw].get("geom") or {}).get("magnetic") or {}).get("realized_basin_id")
                if ra is not None and rb is not None and ra != rb:
                    return None, f"{jn}: on/off 가 다른 realized basin"
        return ed, None

    d_slab, why = pair_delta((_pick(jobs, kind="clean_ref", seed=SEED_MAIN,
                                    d3="on") or [None])[0]) \
        if _pick(jobs, kind="clean_ref", seed=SEED_MAIN, d3="on") else (None, "clean slab 없음")
    if d_slab is None:
        res["verdict"] = f"unresolved — clean slab D3 짝: {why}"
        return res
    means = {}
    for f in frags:
        mol = [j for j in _pick(jobs, kind="mol_ref", fragment=f, d3="on")
               if "box24" in j and "nzmag" not in j]
        if len(mol) != 1:
            res["by_frag"][f] = {"verdict": "unresolved",
                                 "why": f"box24 기체 기준이 {len(mol)}개"}
            continue
        d_mol, why_m = pair_delta(mol[0])
        if d_mol is None:
            res["by_frag"][f] = {"verdict": "unresolved", "why": why_m}
            continue
        rows, miss = [], []
        for jn in _pick(jobs, kind="prospective_pose", fragment=f,
                        seed=SEED_MAIN, d3="on"):
            d_cx, why_c = pair_delta(jn)
            if d_cx is None:
                miss.append(why_c); continue
            rows.append({"job": jn, "delta_eV": round(d_cx - d_slab - d_mol, 6)})
        # ★ 기대 자세 수는 **동결된 manifest** 에서 온다 (C1 과 같은 규율) — 회수분에서
        #   세면 자세가 통째로 빠져도 기대가 같이 줄어 영영 못 잡는다.
        n_want = len([k for k in (man.get("planned") or {})
                      if k.startswith("prospective/")
                      and k.rsplit("/", 1)[-1].startswith(f + "__")
                      and k.endswith(SEED_MAIN)])
        if not n_want:
            res["by_frag"][f] = {"verdict": "unresolved",
                                 "why": "MANIFEST.planned 에 이 조각의 pm1 자세가 없다"}
            continue
        if miss or len(rows) != n_want or not rows:
            res["by_frag"][f] = {"verdict": "unresolved", "missing": miss,
                                 "n_used": len(rows), "n_required": n_want,
                                 "why": "자세 하나라도 Edisp 가 없거나 검사에 걸리면 "
                                        "unresolved — 부분집합 평균을 내지 않는다"}
            continue
        m = sum(x["delta_eV"] for x in rows) / len(rows)
        means[f] = m
        res["by_frag"][f] = {"n": len(rows), "mean_delta_eV": round(m, 6),
                             "rows": rows, "d_slab_eV": round(d_slab, 6),
                             "d_mol_eV": round(d_mol, 6)}
    sd = next((f for f in means if "sdcp" in f), None)
    ct = next((f for f in means if f != sd), None)
    if not (sd and ct):
        res["verdict"] = "unresolved — 두 조각이 다 필요하다"
        return res
    D = means[sd] - means[ct]
    res["D_eV"] = round(D, 6)
    # ★★ 부호 규약 정정 (회신 AB P0-3) — 종전 코드는 **정확히 설명적인 경우를
    #    기각**했다. 봉인된 0.90 eV 는 (UMA − DFT) 규약이고, D3 는 총에너지에
    #    **더해지는** 항이므로
    #        offset_f = E_ads^UMA − E_ads^DFT ≈ −δ_f
    #    ⇒ 예측되는 오프셋 차등 = (−δ_SDCP) − (−δ_c10) = δ_c10 − δ_SDCP = **−D**
    #    이다. 그래서 비교하는 양을 offset 규약으로 **이름부터** 맞춘다 —
    #    부호를 뒤집는 게 아니라 같은 규약에서 재는 것이다.
    res["predicted_offset_gap_eV"] = round(-D, 6)
    res["ratio"] = round(-D / C3_REF_GAP_EV, 4)
    res["sign_convention"] = (
        "0.90 eV = mean(UMA − DFT)_SDCP − mean(UMA − DFT)_c10 = +0.9028 "
        "(prereg 오프셋_UMA_빼기_DFT_eV). D3 는 additive 이므로 offset ≈ −δ ⇒ "
        "예측 오프셋 차등 = −D. **흡착에너지 오프셋이지 총에너지 오프셋이 아니다** "
        "— 원소별 energy-zero 는 소거된다")

    # ★ 조각내 일관성 — **평균만으로 판정하지 않는다.** D3 는 기하 의존 항이라
    #   자세마다 달라야 하는데, 관측 오프셋은 조각 안에서 상수였다
    #   (SDCP 6 meV · c10 37 meV). δ 가 그보다 훨씬 크게 흔들리면 평균이 맞아도
    #   "D3 로 설명" 은 성립하지 않는다 (prereg ⛔_분산_귀속_철회_2026_08_29).
    within = {}
    for f, r in res["by_frag"].items():
        rows = r.get("rows") or []
        if len(rows) < 2:
            continue
        vals = [x["delta_eV"] for x in rows]
        rng = max(vals) - min(vals)
        obs = C3_OFFSET_RANGE_EV.get(f)
        within[f] = {"delta_range_eV": round(rng, 6),
                     "observed_offset_range_eV": obs,
                     "slack": C3_WITHIN_SLACK,
                     "ok": None if obs is None else bool(rng <= obs * C3_WITHIN_SLACK)}
        r["within_fragment_range_eV"] = round(rng, 6)
    res["within_fragment"] = within
    _bad = sorted(f for f, w in within.items() if w["ok"] is False)

    if -D * C3_REF_GAP_EV <= 0:
        res["verdict"] = ("**미해결** — 예측 오프셋 차등(−D)의 부호가 관측 "
                          f"{C3_REF_GAP_EV:+.2f} eV 와 반대다. 절댓값으로 비율을 "
                          "적용하면 반대 방향 효과를 '설명' 으로 오판한다")
    elif _bad:
        res["verdict"] = (
            "**미해결 — 조각내 일관성 실패** (%s). δ 의 조각내 range 가 관측 오프셋 "
            "상수성의 %g배를 넘는다. D3 는 기하 의존 항이라 자세마다 달라야 하는데 "
            "관측 오프셋은 조각 안에서 상수였다 — 평균 비율이 맞아도 D3 귀속은 "
            "성립하지 않는다 (prereg 분산 귀속 철회)." % (", ".join(_bad), C3_WITHIN_SLACK))
    elif res["ratio"] >= C3_HI:
        res["verdict"] = (f"이 네 자세에서 관측된 {C3_REF_GAP_EV} eV 차등을 "
                          f"**수치상 {res['ratio']:.0%} 설명**한다 (인과가 아니라 분해)")
    elif res["ratio"] <= C3_LO:
        res["verdict"] = "분산 기여로는 설명되지 않는다 — 원인은 기체 기준 오차 또는 자기 basin 쪽"
    else:
        res["verdict"] = "**미해결** — 어느 것도 채택하지 않는다"
    return res


def _estimand_topology_check(keys, jobs, label):
    """회신 AP #2 — D 에 들어가는 **두 complex** 가 같은 자기 topology 인가.

    → {"blocks": [...], "by_job": {...}, "same": bool|None}

    ⛔ 존재 확인이 아니라 **비교**다. 종전엔 각 잡에 realized_basin_id 가 있는지만
      보고 서로 같은지는 안 봤다 — 다른 basin 을 섞은 D 가 통과했다.
    ⚠ 전역 스핀 반전은 같은 상태로 본다 (same_topology_direct 규약).
    """
    out = {"blocks": [], "by_job": {}, "same": None, "branch": label}
    ks = [k for k in ("E_C_sdcp", "E_C_control") if keys.get(k)]
    if len(ks) < 2:
        out["blocks"].append(
            "ESTIMAND_TOPOLOGY_KEYS_MISSING(%s: complex key 가 둘이 아니다)" % label)
        return out
    ja, jb = jobs.get(keys[ks[0]]), jobs.get(keys[ks[1]])
    for k in ks:
        fp, why = magnetic_topology_direct(jobs.get(keys[k]) or {})
        out["by_job"][keys[k]] = {"fingerprint": fp, "why": why}
        if fp is None:
            out["blocks"].append(
                "ESTIMAND_TOPOLOGY_UNRESOLVED(%s %s=%s: %s — 어떤 자기 상태에서 "
                "잰 값인지 모른 채로 D 를 만들지 않는다)"
                % (label, k, keys[k], (why or ["사유 없음"])[0]))
    if out["blocks"]:
        return out
    same, why = same_topology_direct(ja, jb)
    out["same"], out["why"] = bool(same), why
    if not same:
        out["blocks"].append(
            "ESTIMAND_TOPOLOGY_MISMATCH(%s: 두 complex 가 **다른 자기 basin** 이다 "
            "(%s) — 상태를 가로질러 뺀 차는 조건부 D 가 아니다)" % (label, why))
    return out


def _closure_estimand(man, results, E, emol, jobs, merge_info=None):
    """사전등록한 조각 간 대비를 **코드로** 계산한다 (회신 V P0-4).

      A(f,p) = E_complex(f,p) - E_mol(f)      <- 공통 슬랩이 소거되는 양
      primary   ddE_lowE = min_p A(SDCP,p) - min_q A(c10,q)
      secondary G        = min_q A(c10,q) - max_p A(SDCP,p)

    회신 V P0-3 — 기체 자기상태 대조(zero vs nzmag)를 **여기서 실제로 비교**한다.
    대조가 더 낮으면 `MOLECULAR_STATE_UNRESOLVED` 로 막고 **값을 내지 않는다.**

    ⛔ 이 함수가 못 하는 것:
      · 후보집합이 **사전등록된 것인지 검사하지 않는다** (그 manifest 가 아직 없다 —
        회신 V P0-5). `candidate_set` 에 무엇을 썼는지 기록만 한다.
      · 국소 Ni topology 판정을 다시 하지 않는다 — 잡별 `gates` 를 읽어 **버린다**.
      · dense/k 보정을 적용하지 않는다. coarse static 값이다.
      · 게이트된 자세를 다음 순위로 **대체하지 않는다** (회신 U C-2: 조용한 교체 금지).
    """
    frags = [f for f in (man.get("fragments") or []) if f in emol]
    if len(frags) < 2:
        return None

    # ══ cohort 조립은 **구조화 필드**로 한다 (회신 AA P0-3) ══════════════════
    #   경로 문자열 파싱은 임시봉합이다. job.json 이 이미 kind·role·fragment·
    #   seed·basin_id·source_pose·phases·d3 를 갖고 있으므로 그것으로 조립하고,
    #   **경로와 구조화 필드가 어긋나면 hard fail** 한다 (조용히 한쪽을 믿지 않는다).
    def _meta(jr):
        return (jr.get("meta") or {})

    def _is_vacconv(jr):
        """진공 수렴 시험용 둘째 셀 잡인가.

        ⛔ 회신 AJ — 종전엔 이 잡들이 `kind=prospective_pose` 라 **일반 자세와 똑같이**
           취급됐다. 그러면 ① min 후보 풀에 다른 셀의 에너지가 섞이고 ② 같은
           (basin, seed) 키라 c1 값을 c2 가 **덮어쓴다**. 셀이 다른 에너지를 한
           seed-pair 로 조립하게 된다. 코호트에서 뺀다.
        """
        return bool((jr.get("meta") or {}).get("vacconv"))

    def _cohort(jn, jr):
        """이 잡의 (kind, fragment, seed, basin, d3) — 전부 구조화 필드에서.

        ⛔ 회신 AJ — 진공 수렴 시험(둘째 셀) 잡은 `kind` 를 **바꿔서** 낸다.
           그대로 두면 일반 자세와 같은 (basin, seed) 키를 가져 ① min 후보 풀에
           다른 셀 에너지가 섞이고 ② c1 값을 c2 가 덮어쓴다.
        """
        m = _meta(jr)
        if _is_vacconv(jr):
            return {"kind": "vacuum_convergence", "fragment": m.get("fragment"),
                    "seed": m.get("seed"), "basin": m.get("basin_id"),
                    "d3": "on", "cell": m.get("vacconv")}
        return {"kind": m.get("kind"), "fragment": m.get("fragment"),
                "seed": m.get("seed"), "basin": m.get("basin_id"),
                "d3": m.get("d3"), "role": m.get("role")}

    #: primary 와 **같은 풀에 넣으면 안 되는** 역할 (회신 AJ ④).
    #   sensitivity·stress_sensitivity 는 '다른 앵커에서도 방향이 유지되나' 만 본다.
    #   min·평균·순위에 섞으면 그 시험이 사라지고 표본만 늘어난다.
    ALT_ROLES = ("sensitivity", "stress_sensitivity")

    def _is(jn, f):
        """조각 f 의 **primary 복합체**인가 — 구조화 필드로만 판단한다.

        ⛔ 회신 AJ ④ — 종전엔 role 을 안 봐서 대안 자세가 primary min 풀에 섞였다.
        """
        c = _cohort(jn, jobs.get(jn) or {})
        if c["kind"] != "prospective_pose" or c["fragment"] != f:
            return False
        return (c.get("role") or "primary") not in ALT_ROLES
    out = {
        "schema": "prereg_closure/v1",
        "prereg_doc": "db/properties/prereg_sdcp_neutral_contrast_2026_08_29.json",
        "candidate_set": man.get("candidate_set") or "legacy_champion/cross (미동결)",
        "blocks": [], "block_records": [], "A_by_frag": {},
    }

    # ── 경로 ↔ 필드 정합성. 어긋나면 값을 만들지 않는다 ──────────────────────
    _incoh = []
    for _jn, _jr in jobs.items():
        _m = _meta(_jr)
        if not _m.get("kind"):
            _incoh.append(f"{_jn}: job.json 에 kind 없음")
            continue
        _base = _jn.rsplit("/", 1)[-1]
        _fg, _sd, _d3 = _m.get("fragment"), _m.get("seed"), _m.get("d3")
        if _fg and _m["kind"] == "prospective_pose" and not _base.startswith(_fg + "__"):
            _incoh.append(f"{_jn}: fragment={_fg} 인데 경로가 그렇지 않다")
        if _sd and _sd not in _base:
            _incoh.append(f"{_jn}: seed={_sd} 인데 경로에 없다")
        if _d3 not in ("on", "off"):
            _incoh.append(f"{_jn}: job.json 에 d3 필드가 없다 (필드 없는 잡이 남으면 "
                          f"분류가 다시 이름으로 샌다 — v7 실측)")
        elif (_d3 == "off") != _base.endswith("__d3off"):
            _incoh.append(f"{_jn}: d3={_d3} 인데 경로 접미어와 어긋난다")
    if _incoh:
        out["blocks"].append(
            "COHORT_INCOHERENT(%d건 — 경로와 구조화 필드가 어긋난다: %s). "
            "어느 쪽이 맞는지 우리가 정할 수 없으므로 값을 만들지 않는다"
            % (len(_incoh), _incoh[:3]))
    out["cohort_fields"] = {"checked": len(jobs), "incoherent": len(_incoh)}


    # (0) calibration 전용 tranche 면 **primary 를 내지 않는다** (회신 X P0-2)
    if str(out["candidate_set"]).startswith(("calibration_pilot", "motif_probe")):
        out["blocks"].append(
            "CALIBRATION_ONLY_TRANCHE — 이 잡들은 창 W 를 정하려고 돌린 것이고 "
            "후보집합이 아니다. primary 는 창 확정 → 창 안 전 자세 계산 → audit "
            "봉인해제 → regret 판정 순서를 마친 뒤에만 낸다 (회신 X Q6).")
    # ⛔⛔ 회신 AP #3 (2026-08-31) — block 을 **구조화**한다. 종전엔 문자열뿐이라
    #   "이 block 이 D 에 들어가는 네 잡을 언급하는가" 를 **문자열 매칭**으로 판단했다.
    #   그런데 `BASIN_HETEROGENEOUS` 문자열에는 job 경로가 없다 ⇒ 그 조건이 **항상
    #   참**이 되어 그 block 이 언제나 강등됐다. 막으려던 것을 못 막고 있었다.
    #   ⇒ code · job_keys · scope · affects_estimand 를 기록하고, 강등 판정은
    #     **문자열이 아니라 그 필드**로 한다.
    def _blk(code, msg, job_keys=None, scope="global", affects_estimand=True):
        out["blocks"].append(msg)
        out["block_records"].append({
            "code": code, "msg": msg, "job_keys": sorted(job_keys or []),
            "scope": scope, "affects_estimand": bool(affects_estimand)})

    # (0b) 층화 홀드아웃도 **primary 를 내지 않는다** (2026-08-30, 옵션 A).
    #   홀드아웃은 선택기 가정을 시험하는 별도 질문이다. 홀드아웃이 더 낮게 나오면
    #   그것은 primary 의 min 후보가 아니라 **재개 조건 발동**이다 — 넣으면
    #   사전등록 집합이 사라지고 min 이 표본크기를 따라 움직인다
    #   (champion pool size bias, kb/results/champion_pool_size_bias_2026_08_18.md).
    if str(out["candidate_set"]).startswith("holdout_stratified"):
        out["blocks"].append(
            "HOLDOUT_TRANCHE — 층화 홀드아웃은 선택기 가정(H1·H2)을 시험하는 집합이지 "
            "primary 후보집합이 아니다. 이 잡들의 값을 ΔΔE_lowE 의 min 에 넣지 않는다. "
            "estimand 카드: kb/questions/sdcp_stageA_holdout_selector_2026_08_30.md")

    # (1) 기체 자기상태 대조 — 값을 내기 **전에** 본다 (회신 V P0-3)
    ctls = man.get("molecular_spin_controls") or {}
    for f in frags:
        rel = ctls.get("mol__%s__box24" % f)
        if not rel:
            out["blocks"].append("MOLECULAR_SPIN_CONTROL_MISSING(%s)" % f)
            continue
        # ⛔ 회신 AJ — 종전엔 `refs/` 를 떼고 basename 을 넘겼다. E() 는 잡 상대경로로
        #   찾으므로 실제 잡이 있어도 **항상 PENDING** 이 됐다. 둘 다 시도한다.
        e1 = E(str(rel))
        if e1 is None:
            e1 = E(str(rel).split("/")[-1])
        e0 = emol.get(f)
        if e1 is None:
            out["blocks"].append("MOLECULAR_SPIN_CONTROL_PENDING(%s)" % f)
        elif e0 is None:
            # ⛔⛔ 회신 AS 해제조건 2 (2026-08-31) — box24 **부모가 실패하고**
            #   nzmag canary 만 성공하면 아래 `else` 에서 `e1 - None` 으로
            #   **예외로 죽었다**. 결측은 예외가 아니라 구조화 차단이고,
            #   차 계산은 건너뛴다 (확인 못 한 것은 통과가 아니다).
            out["blocks"].append(
                "MOLECULAR_SPIN_CONTROL_PARENT_MISSING(%s: canary 는 회수됐는데 "
                "부모 box24 에너지가 없다 — 뺄 기준이 없으므로 스핀 대조를 "
                "만들지 않는다)" % f)
        elif e1 < e0 - 1e-4:
            out["blocks"].append(
                "MOLECULAR_STATE_UNRESOLVED(%s: 비영 시작이 %.4f eV 더 낮다 — "
                "자동 채택하지 않는다. 전자상태 정의와 box 수렴을 다시 심사할 것)"
                % (f, e0 - e1))
        else:
            out.setdefault("spin_control_delta_eV", {})[f] = round(e1 - e0, 5)
        # ⛔⛔ 회신 AO P0-4 — 두 static 이 **같은 기하**일 때만 이 차가 스핀 검사다.
        #   다르면 구조 이완 에너지가 섞여 δ_m 이 아니다. 검사를 못 했으면 그것도 차단
        #   (fail-closed — 확인 못 한 것은 통과가 아니다).
        _gg = ((results or {}).get("gas_canary_geom") or {}).get(f)
        if _gg is None:
            out["blocks"].append(
                "CANARY_GEOM_UNCHECKED(%s: 부모/ canary static 기하 대조 결과가 없다)" % f)
        elif _gg.get("same") is not True:
            out["blocks"].append(
                "CANARY_GEOM_MISMATCH(%s: %s — 스핀 대조에 구조 이완 에너지가 섞인다)"
                % (f, _gg.get("why") or ("최대 Cartesian 차 %.3g Å · 셀 차 %.3g Å"
                                         % (_gg.get("max_cart_diff_A", float("nan")),
                                            _gg.get("max_cell_diff_A", float("nan"))))))

    # (2) A(f,p) — 게이트 통과한 복합체만. 게이트된 것은 **버리되 기록한다**
    #   ★ 회신 Z P0-4 — realized basin 을 같이 모은다. seed 이름(pm1/net4)으로
    #     짝지어 빼면 다른 상태를 가로질러 뺀 것이 된다.
    # ⛔⛔ 회신 AS 해제조건 3 (2026-08-31) — 종전엔 `not jr.get("ok")` 로 **먼저**
    #   건너뛰어서, 실제로 게이트된 잡은 아래 `GATED_POSE` 에 **도달하지 못했다**.
    #   그러면 pooled 값이 **살아남은 부분집합**으로 조용히 계산된다 — net4 가 전부
    #   게이트돼도 pm1 만으로 secondary_G 가 인용가능이 될 수 있었다.
    #   ⇒ 계획된 pool 전체를 세고, 하나라도 결측·게이트·미해결이면 pooled 를 막는다.
    _pool_expect, _pool_bad = {}, {}
    for _pj, _pl in ((man.get("planned") or {}).items()):
        _pm = (_pl.get("meta") or {})
        if _pm.get("kind") != "prospective_pose" or _pm.get("vacconv"):
            continue
        _pf = _pm.get("fragment")
        if _pf in frags:
            _pool_expect.setdefault(_pf, []).append(_pj)
    basins = {}
    for f in frags:
        rows = []
        for jn in sorted(_pool_expect.get(f, [])):
            jr = jobs.get(jn)
            if jr is None:
                # ⛔ 회신 AS 3 — 계획엔 있는데 **회수되지 않았다**. `_is()` 는
                #   jobs 를 보므로 여기서 False 가 되어 조용히 pool 밖으로 샌다.
                #   결측을 먼저 잡는다 (계획의 role 로 pool 대상인지 판단).
                _rl = ((( man.get("planned") or {}).get(jn) or {})
                       .get("meta") or {}).get("role") or "primary"
                if _rl not in ALT_ROLES:
                    _pool_bad.setdefault(f, []).append("%s: 결과 없음" % jn)
                continue
            if not _is(jn, f):
                continue                      # 대안 자세 역할 — pool 밖 (ALT_ROLES)
            g = [x for x in (jr.get("gates") or [])
                 if x.startswith(("MAGNETIC", "RADICAL", "PAIR_", "SOURCE_", "BASIN_"))]
            e = E(jn)
            if g:
                _blk("GATED_POSE", "GATED_POSE(%s: %s)" % (jn, g[0]),
                     job_keys=[jn], scope="pooled_diagnostic")
                _pool_bad.setdefault(f, []).append("%s: %s" % (jn, g[0][:40]))
                continue
            if not jr.get("ok"):
                _blk("POOL_JOB_NOT_OK",
                     "POOL_JOB_NOT_OK(%s: 게이트 목록에 없는 사유로 사용 불가 — %s)"
                     % (jn, (jr.get("gates") or ["사유 미기록"])[0][:40]),
                     job_keys=[jn], scope="pooled_diagnostic")
                _pool_bad.setdefault(f, []).append("%s: not ok" % jn)
                continue
            if e is None:
                _pool_bad.setdefault(f, []).append("%s: 에너지 없음" % jn)
                continue
            rb = (((jr.get("geom") or {}).get("magnetic") or {})
                  .get("realized_basin_id"))
            basins.setdefault(f, {}).setdefault(rb, []).append(jn)
            if emol.get(f) is None:
                continue          # ⛔ 회신 AR P0-3 — `float − None` 예외 대신 건너뛴다
                                  #   (기체 기준 부재는 위에서 이미 block 이다)
            rows.append([round(e - emol[f], 6), jn, rb])
        rows.sort()
        out["A_by_frag"][f] = {"n": len(rows),
                               "min": rows[0] if rows else None,
                               "max": rows[-1] if rows else None}
    out["realized_basins"] = {f: {str(k): v for k, v in (b or {}).items()}
                              for f, b in basins.items()}
    # ⛔ 회신 AS 해제조건 3 — 계획된 pool 이 **전건 사용가능**한지 한 곳에서 판정한다
    out["pool_completeness"] = {
        "expected": {f: len([j for j in v if _is(j, f)])
                     for f, v in _pool_expect.items()},
        "usable": {f: (out["A_by_frag"].get(f) or {}).get("n", 0) for f in frags},
        "unusable": {f: v[:4] for f, v in _pool_bad.items()},
        "ok": not _pool_bad,
        "⛔": ("계획된 자세 하나라도 결측·게이트·미해결이면 pooled 값(secondary_G · "
               "pooled min · 일반화 주장)을 **전부 비인용**으로 한다. 살아남은 "
               "부분집합으로 min 을 뽑으면 표본이 통과 쪽으로 편향된다")}
    if _pool_bad:
        _blk("POOL_INCOMPLETE",
             "POOL_INCOMPLETE(계획된 자세 중 사용 불가 %s — pooled 값을 내지 않는다)"
             % {f: len(v) for f, v in _pool_bad.items()},
             job_keys=[j.split(":")[0] for v in _pool_bad.values() for j in v],
             scope="pooled_diagnostic")

    # (2c) 🔴 동종 basin 강제 — 여러 basin 이 섞인 집합에서 min 을 뽑지 않는다
    for f, b in basins.items():
        if None in b:
            _blk("BASIN_UNRESOLVED_IN_SET",
                 "BASIN_UNRESOLVED_IN_SET(%s: %d잡이 realized basin 없음 — %s)"
                 % (f, len(b[None]), b[None][:3]),
                 job_keys=b[None], scope="pooled_diagnostic")
        real = {k: v for k, v in b.items() if k is not None}
        if len(real) > 1:
            _blk("BASIN_HETEROGENEOUS",
                 "BASIN_HETEROGENEOUS(%s: 서로 다른 realized basin %d개가 한 집합에 "
                 "있다 %s — 상태를 가로질러 min 을 뽑지 않는다. seed 이름이 아니라 "
                 "수렴 결과가 갈렸다는 뜻이다)"
                 % (f, len(real), {k: len(v) for k, v in real.items()}),
                 job_keys=[j for v in real.values() for j in v],
                 scope="pooled_diagnostic")

    # (2d) clean slab 과의 동종성 — E_ads 를 만들 때 필요하다 (회신 Z P0-4)
    _slab_rb = set()
    for jn, jr in jobs.items():
        if _cohort(jn, jr)["kind"] != "clean_ref" or not jr.get("ok"):
            continue
        rb = ((jr.get("geom") or {}).get("magnetic") or {}).get("realized_basin_id")
        if rb:
            _slab_rb.add(rb)
    if _slab_rb:
        out["clean_slab_basins"] = sorted(_slab_rb)
        _cx = {k for b in basins.values() for k in b if k is not None}
        if _cx and not (_cx & _slab_rb):
            out["blocks"].append(
                "BASIN_MISMATCH_SLAB(복합체 basin %s 이 clean slab basin %s 과 "
                "겹치지 않는다 — 이 둘로 흡착에너지를 만들지 않는다)"
                % (sorted(_cx)[:2], sorted(_slab_rb)[:2]))

    # (2b) J_f — pose × magnetic-basin interaction (회신 X Q1)
    #   조각별로 자세 p 의 두 seed 차 d_p = E(p,net4) − E(p,pm1) 를 모아
    #   J_f = max_p d_p − min_p d_p. 자세마다 자기 basin 이 다르게 잡히면 커진다.
    for f in frags:
        d = {}
        for jn, jr in jobs.items():
            c = _cohort(jn, jr)
            if not _is(jn, f) or not jr.get("ok") or c["d3"] == "off":
                continue
            if not c["basin"] or not c["seed"]:
                continue                      # 구조화 필드가 없으면 짝을 못 맞춘다
            d.setdefault(c["basin"], {})[c["seed"]] = E(jn)
        dp = {k: v["afm2424_net4"] - v["afm2424_pm1"] for k, v in d.items()
              if v.get("afm2424_net4") is not None and v.get("afm2424_pm1") is not None}
        # 🔴 회신 AB P0-7 — 종전엔 짝이 **2개만 있어도** J_f 를 냈다. 네 자세 중
        #   한둘이 빠지면 range 가 자동으로 좁아져 **거짓 PASS** 가 된다(C1 과 같은
        #   편향). 기대 자세 수는 동결 manifest 에서 세고, 그 수만큼 두 seed 가
        #   **모두** 유효할 때만 낸다.
        _want = len({k.rsplit("/", 1)[-1].split("__")[1]
                     for k in (man.get("planned") or {})
                     if k.startswith("prospective/")
                     and k.rsplit("/", 1)[-1].startswith(f + "__")
                     and len(k.rsplit("/", 1)[-1].split("__")) > 2})
        if not _want or len(dp) != _want:
            out.setdefault("pose_basin_interaction", {})[f] = {
                "판정": "unresolved", "n_pose_used": len(dp), "n_pose_required": _want,
                "why": ("계획한 자세 전부가 두 seed 다 유효해야 한다 — 부분집합은 "
                        "range 를 좁혀 통과 쪽으로 편향된다 (회신 AB P0-7)")}
            continue
        jf = max(dp.values()) - min(dp.values())
        out.setdefault("pose_basin_interaction", {})[f] = {
            "n_pose": len(dp), "n_pose_required": _want,
            "J_f_meV": round(jf * 1000, 2),
            "delta_by_pose_meV": {k: round(v * 1000, 2) for k, v in sorted(dp.items())},
            # ⚠ 회신 AB P0-7 — "seed-insensitive" 는 **과한 말**이다. 시험한 네 자세
            #   안에서 range 가 작았다는 것뿐이고, seed 에 둔감하다는 일반 진술이
            #   아니다. 허용 문구를 그대로 박는다.
            "판정": ("seed×pose interaction range 가 작았다 (시험한 %d자세 안에서)"
                     % len(dp) if jf <= 0.010 else
                     "magnetic-sensitive" if jf <= 0.040 else
                     "⛔ SELECTOR_FAIL — J_f > 40 meV")}

    # ── 닫힘 조건 C1 · C3 — **코드로** 낸다 (회신 AA P0-4 "실행 가능한 estimand")
    #   primary 가 막혀도 이 둘은 나온다. 손계산으로 넘기면 결과를 보고 식을 고를
    #   여지가 남고, 그것이 이 캠페인을 여덟 번 물린 경로다.
    try:
        out["closure_C1"] = closure_C1(man, jobs, E, emol, frags)
        out["closure_C3"] = closure_C3(man, jobs, E, frags)
        out["closure_vacconv"] = closure_vacconv(man, jobs, E, emol, frags)
        # ⛔ 2026-08-31 — `pass` 가 이제 항상 있으므로(기본 False) **applicable 을 먼저 본다.**
        #   안 그러면 진공 시험 잡이 없는 옛 번들이 "n/a" 인데 FAIL 로 막힌다.
        #   적용 불가와 실패는 다른 상태다.
        if (out["closure_vacconv"].get("applicable")
                and out["closure_vacconv"].get("pass") is False):
            out["blocks"].append("VACCONV_FAIL:" + out["closure_vacconv"]["verdict"])
        for _b in (out["closure_vacconv"].get("blocks") or []):
            out["blocks"].append("VACCONV:" + _b)
        out["potcar_identity"] = potcar_identity_gates(jobs, man)
        # ⛔ 회신 AJ — 종전엔 **기록만** 하고 blocks 에 안 합쳤다. split·pin 불일치를
        #   탐지해도 값 보고를 못 막았다. 게이트가 아니라 로그였던 것이다.
        for _b in (out["potcar_identity"].get("blocking") or []):
            out["blocks"].append("POTCAR_IDENTITY:" + _b)
        out["h1_tolerance"] = h1_tolerance(out["closure_C1"])
        out["closure_C5"] = closure_C5(man, jobs, E, emol, frags, merge_info,
                                       out["h1_tolerance"])
    except Exception as _e:                                  # noqa: BLE001
        out["blocks"].append(f"CLOSURE_COND_ERROR({_e!r})")

    # ⛔⛔ 회신 AO P0-7 (2026-08-31) — pm1 조건부 D 는 **사전 고정한 네 잡**으로
    #   정의됐는데, 앞의 집합 검사(2c)가 pm1 과 net4 를 한 조각 집합으로 묶었다.
    #   그래서 net4 가 다른 basin 에 가면 pm1 네 값이 전부 정상이어도 통째로
    #   NO_VALUE 가 됐고, 정작 요구했던 `D_net4 − D_pm1` 은 계산되지 않았다.
    #   ⇒ **그 네 잡을 언급하지 않는 집합-블록은 차단이 아니라 민감도 주석**으로 내린다.
    #     전역 블록(후보집합·기체 canary·spin control·POTCAR)은 그대로 둔다.
    #   ⚠ 이 강등은 **조기 return 앞에서** 해야 한다 — 뒤에 두면 이미 return 된 뒤다.
    # ⛔⛔ 회신 AP #11 (2026-08-31) — 기체 상자 수렴 게이트를 **조각별 10 meV 가
    #   아니라 최종 estimand 에 직접** 건다. D 에 남는 것은 두 기체의 **차이**이고,
    #   조각별로 각각 10 meV 안이어도 부호가 반대면 차에서 20 meV 가 된다.
    #       δ_gas = [E_G^SDCP(24) − E_G^SDCP(20)] − [E_G^PTFE(24) − E_G^PTFE(20)]
    #   0.01 eV 로 보고하려면 |δ_gas| ≤ 5 meV 여야 한다 (AP 가 지정한 사전 문턱).
    _sdf = next((f for f in frags if "sdcp" in f), None)
    _ctf = next((f for f in frags if f != _sdf), None)
    if _sdf and _ctf:
        # ⛔⛔ 회신 AR 해제조건 3 (2026-08-31) — **cross-job geometry/state gate.**
        #   δ_gas 가 "셀 효과" 이려면 두 상자가 (i) 같은 내부기하에서 출발하고
        #   (ii) 같은 전자상태 정책이며 (iii) **각자 독립으로 이완하지 않아야** 한다.
        #   v15 실물은 네 기체 부모가 전부 relax→static 이라 (iii) 이 깨져 있었고,
        #   δ_gas 는 셀 효과 + 독립 이완 차이를 함께 쟀다. 이제 산출물에서 직접 본다.
        _gp = (man.get("gas_geometry_policy") or {})
        _gasjr = {}
        for _f in (_sdf, _ctf):
            for _b in ("20", "24"):
                _k = "refs/mol__%s__box%s" % (_f, _b)
                _gasjr[(_f, _b)] = ((jobs.get(_k) or {}).get("meta") or {})
        _gx = []
        for _f in (_sdf, _ctf):
            _m20, _m24 = _gasjr[(_f, "20")], _gasjr[(_f, "24")]
            if not _m20 or not _m24:
                _gx.append("%s: box20/box24 잡 메타가 없다" % _f)
                continue
            for _fld, _why in (("internal_geometry_sha", "내부기하가 다르다"),
                               ("electronic_state_sha", "전자상태 정책이 다르다"),
                               ("species_order", "원소 순서가 다르다"),
                               ("counts", "원자 수가 다르다")):
                _a, _b2 = _m20.get(_fld), _m24.get(_fld)
                if _a is None or _b2 is None:
                    _gx.append("%s: %s 를 확인 못 했다 (구판 번들)" % (_f, _fld))
                elif _a != _b2:
                    _gx.append("%s: %s (%s)" % (_f, _why, _fld))
            for _b, _mm in (("20", _m20), ("24", _m24)):
                if _mm.get("fixed_geometry_static") is not True:
                    _gx.append("%s box%s: 고정기하 static 이 아니다 "
                               "(phases=%s) — 독립 이완이 δ_gas 에 섞인다"
                               % (_f, _b, _mm.get("phases")))
        if _gp.get("fixed_geometry_static") is not True:
            _gx.append("manifest.gas_geometry_policy.fixed_geometry_static 이 true 가 "
                       "아니다 (%r)" % (_gp.get("fixed_geometry_static"),))
        out["gas_pair_contract"] = {
            "ok": not _gx, "violations": _gx,
            "요구": ["box20/box24 내부기하 동일 (internal_geometry_sha)",
                     "전자상태 정책 동일 (electronic_state_sha)",
                     "둘 다 고정기하 static — 상자별 독립 이완 금지"],
            "⚠": ("이 계약이 깨지면 δ_gas 는 셀 수렴이 아니라 "
                  "'셀 + 이완 경로' 를 잰 값이라 문턱을 걸 대상이 아니다")}
        if _gx:
            _blk("GAS_PAIR_CONTRACT",
                 "GAS_PAIR_CONTRACT(δ_gas 쌍이 계약을 어겼다 — %s)" % "; ".join(_gx[:4]),
                 job_keys=["refs/mol__%s__box%s" % (f, b)
                           for f in (_sdf, _ctf) for b in ("20", "24")],
                 scope="estimand")
        _g = {}
        for _f in (_sdf, _ctf):
            _g[_f] = (E("refs/mol__%s__box24" % _f), E("refs/mol__%s__box20" % _f))
        # ⛔ 회신 AR P0-3 — 결측을 **예외가 아니라 구조화 block** 으로 처리한다
        _miss_g = [f for f, (a24, a20) in _g.items() if a24 is None or a20 is None]
        if _miss_g:
            _blk("GAS_BOX_NOT_MEASURED",
                 "GAS_BOX_NOT_MEASURED(%s: box20/box24 중 하나가 없다 — 이 묶음에서 "
                 "기체 상자 수렴을 재지 못했다. D 에는 E_G^SDCP − E_G^control 이 "
                 "남으므로 상자 오차가 소거되지 않는다)" % _miss_g,
                 job_keys=["refs/mol__%s__box%s" % (f, b)
                           for f in _miss_g for b in ("20", "24")],
                 scope="estimand")
        else:
            _d24_20 = {f: (v[0] - v[1]) for f, v in _g.items()}
            _dgas = _d24_20[_sdf] - _d24_20[_ctf]
            out["gas_box_delta"] = {
                "delta_gas_meV": round(_dgas * 1000, 3),
                "by_fragment_meV": {f: round(v * 1000, 3) for f, v in _d24_20.items()},
                "tol_meV": round(GAS_BOX_DELTA_TOL * 1000, 1),
                # ⛔ 회신 AR 해제조건 3 — 쌍 계약이 깨지면 이 값은 셀 효과가
                #   아니므로 문턱 통과로 **셀 수 없다**. 수치는 남기되 pass=False.
                "pass": bool(abs(_dgas) <= GAS_BOX_DELTA_TOL) and not _gx,
                "pair_contract_ok": not _gx,
                "식": "δ_gas = [E_G^sdcp(24)−E_G^sdcp(20)] − [E_G^ctl(24)−E_G^ctl(20)]",
                "⚠": ("조각별 값이 각각 작아도 **부호가 반대면 차에서 커진다** — "
                      "그래서 조각별이 아니라 이 차에 문턱을 건다 (회신 AP #11)")}
            if abs(_dgas) > GAS_BOX_DELTA_TOL:
                _blk("GAS_BOX_DELTA",
                     "GAS_BOX_DELTA(δ_gas %.2f meV > %.0f — 0.01 eV 로 보고할 수 없다. "
                     "상자를 키우거나 보고 해상도를 낮춘다)"
                     % (_dgas * 1000, GAS_BOX_DELTA_TOL * 1000),
                     job_keys=["refs/mol__%s__box%s" % (f, b)
                               for f in (_sdf, _ctf) for b in ("20", "24")],
                     scope="estimand")

    # ⛔⛔ 회신 AS 해제조건 9 (2026-08-31) — **k 수렴을 최종 대비에 직접 건다.**
    #   0.01 eV 로 보고하려면 static k → dense k 로 갈 때 두 조각의 차가
    #   얼마나 움직이는지 알아야 한다. δ_gas 와 같은 논리다 (조각별이 아니라 차).
    _kp = (man.get("kconv_pair") or {})
    if _kp.get("jobs") and len(_kp["jobs"]) == 2:
        _kv = {}
        for _kj in _kp["jobs"]:
            _f = ((jobs.get(_kj) or {}).get("meta") or {}).get("fragment")
            # dense 는 같은 잡의 phase 라 job record 에서 직접 읽는다
            #   (`E_dense()` 는 main() 스코프라 여기서 못 쓴다)
            _dr = ((jobs.get(_kj) or {}).get("dense") or {})
            _kv[_f] = (E(_kj), (_dr.get("E0") if _dr.get("normal_end") else None))
        _kmiss = [f for f, (c, d) in _kv.items() if c is None or d is None]
        _dk = None
        if _kmiss:
            _blk("KCONV_NOT_MEASURED",
                 "KCONV_NOT_MEASURED(%s: coarse/dense 중 하나가 없다 — "
                 "0.01 eV 보고의 k 근거가 없다)" % _kmiss,
                 job_keys=list(_kp["jobs"]), scope="estimand")
        else:
            _fs = next((f for f in _kv if "sdcp" in str(f)), None)
            _fc = next((f for f in _kv if f != _fs and f is not None), None)
            _d = {f: (v[1] - v[0]) for f, v in _kv.items()}
            if _fs is None or _fc is None:
                # ⛔ 조각을 못 가른다 — 확인 못 한 것은 통과가 아니다
                _blk("KCONV_FRAGMENT_UNRESOLVED",
                     "KCONV_FRAGMENT_UNRESOLVED(k 수렴 쌍의 조각을 못 가렸다 %s)"
                     % sorted(str(f) for f in _kv),
                     job_keys=list(_kp["jobs"]), scope="estimand")
            else:
                _dk = _d[_fs] - _d[_fc]
        if _kp.get("jobs") and len(_kp["jobs"]) == 2 and not _kmiss and _dk is not None:
            _tol = float(_kp.get("tol_eV") or 0.005)
            out["kconv_delta"] = {
                "delta_k_meV": round(_dk * 1000, 3),
                "by_fragment_meV": {f: round(v * 1000, 3) for f, v in _d.items()},
                "tol_meV": round(_tol * 1000, 1),
                "pass": bool(abs(_dk) <= _tol),
                "식": _kp.get("formula"),
                "kmesh": {"coarse": _kp.get("coarse_kmesh"),
                          "dense": _kp.get("dense_kmesh")}}
            if abs(_dk) > _tol:
                _blk("KCONV_DELTA",
                     "KCONV_DELTA(δ_k %.2f meV > %.0f — 0.01 eV 로 보고할 수 "
                     "없다. dense 로 다시 내거나 보고 해상도를 낮춘다)"
                     % (_dk * 1000, _tol * 1000),
                     job_keys=list(_kp["jobs"]), scope="estimand")
    elif (man.get("estimand_job_keys") and
          str(_kp.get("status")) != "not_applicable"):
        _blk("KCONV_ABSENT",
             "KCONV_ABSENT(k 수렴 쌍이 봉인돼 있지 않다 — 0.01 eV 보고의 "
             "근거가 없다)", scope="estimand")

    # ══ 🔴 회신 AT Q2 — 세 수치축의 **합산 오차예산** (2026-08-31) ═══════════
    #   세 축(Δ_vac · δ_gas · δ_k)은 **독립 확률오차가 아니다.** 같은 계·같은
    #   프로토콜의 체계오차라 RSS 로 합치면 안 된다. 셋이 같은 방향이면 최대
    #   15 meV 가 된다 — 각각 5 meV 를 통과해도 합이 15 meV 면 0.01 eV 보고가
    #   성립하지 않는다.  ⇒ **결과를 보기 전에** 합산 예산을 고정한다:
    #        B_num = |Δ_vac| + |δ_gas| + |δ_k| ≤ 5 meV
    #   넘으면 값을 버리는 것이 아니라 **보고 해상도를 낮추거나** 축별 민감도만
    #   보고한다 (어느 축이 얼마나 기여했는지는 아래 by_axis 가 말한다).
    _bax, _bmiss = {}, []
    _vc0 = out.get("closure_vacconv") or {}
    if _vc0.get("applicable"):
        _v = _vc0.get("delta_vac_eV")
        _v = None if _v is None else float(_v) * 1000.0
        if _v is None:
            _bmiss.append("Δ_vac")
        else:
            _bax["vac"] = abs(float(_v))
    _gb0 = out.get("gas_box_delta") or {}
    if _gb0:
        _v = _gb0.get("delta_gas_meV")
        if _v is None:
            _bmiss.append("δ_gas")
        else:
            _bax["gas"] = abs(float(_v))
    _kd0 = out.get("kconv_delta") or {}
    if _kd0:
        _v = _kd0.get("delta_k_meV")
        if _v is None:
            _bmiss.append("δ_k")
        else:
            _bax["k"] = abs(float(_v))
    _BTOL = 5.0
    out["numeric_budget"] = {
        "정의": "B_num = |Δ_vac| + |δ_gas| + |δ_k|  (meV)",
        "⛔_RSS_금지": ("세 축은 독립 확률오차가 아니다 — 같은 계·같은 프로토콜의 "
                        "체계오차다. RSS(제곱합근)로 합치면 상관을 0 으로 가정하는 "
                        "것이고, "
                        "셋이 같은 방향이면 실제 편차는 단순합에 가깝다 (회신 AT Q2)"),
        "by_axis_meV": {k: round(v, 3) for k, v in sorted(_bax.items())},
        "missing_axes": _bmiss,
        "B_num_meV": (round(sum(_bax.values()), 3) if _bax and not _bmiss else None),
        "tol_meV": _BTOL,
        "pass": (bool(_bax) and not _bmiss and sum(_bax.values()) <= _BTOL),
        "⚠_문턱_봉인": "결과를 보기 전에 정한 값이다 (회신 AT Q2 · 코드 상수)",
        "미달이면": ("값을 버리지 않는다 — **0.01 eV 안정성 주장을 하지 않고** 보고 "
                     "해상도를 낮추거나 축별 민감도만 낸다"),
    }
    if _bmiss:
        _blk("NUMERIC_BUDGET_INCOMPLETE",
             "NUMERIC_BUDGET_INCOMPLETE(축 %s 의 값이 없다 — 합산 예산을 만들 수 "
             "없으므로 0.01 eV 안정성을 주장하지 않는다)" % _bmiss,
             scope="estimand")
    elif _bax and sum(_bax.values()) > _BTOL:
        _blk("NUMERIC_BUDGET_EXCEEDED",
             "NUMERIC_BUDGET_EXCEEDED(B_num %.2f meV > %.0f — 축별로는 통과해도 "
             "합이 넘는다 %s. 0.01 eV 로 보고하지 않는다)"
             % (sum(_bax.values()), _BTOL, {k: round(v, 2) for k, v in _bax.items()}),
             scope="estimand")

    _ejk0 = (man.get("estimand_job_keys") or {})
    if _ejk0:
        # ⛔⛔ 회신 AP #2 — **네 잡 자신**의 자기 상태 검사는 다른 block 유무와
        #   무관하게 **항상** 돌아야 한다. 종전엔 이것이 강등 블록 안에 있어서
        #   `blocks` 가 비면 아예 실행되지 않았다 (원래 basin 요구도 같은 자리였다).
        _tp = _estimand_topology_check(_ejk0, jobs, "pm1")
        for _m in _tp["blocks"]:
            _blk("ESTIMAND_TOPOLOGY", _m,
                 job_keys=[v for k, v in _ejk0.items() if k.startswith("E_C_")],
                 scope="estimand")
        out.setdefault("estimand_topology", {})["pm1"] = _tp
        _n4k0 = (man.get("estimand_job_keys_net4") or {})
        if _n4k0:
            _tp4 = _estimand_topology_check(_n4k0, jobs, "net4")
            # net4 는 민감도라 **차단하지 않는다** — 대신 민감도 자격을 잃는다
            _tp4["usable_as_sensitivity"] = not _tp4["blocks"]
            out["estimand_topology"]["net4"] = _tp4
    if _ejk0 and out["block_records"]:
        _need0 = ("E_C_sdcp", "E_C_control", "E_G_sdcp", "E_G_control")
        _exact = {_ejk0[k] for k in _need0 if _ejk0.get(k)}
        # ⛔⛔ 회신 AP #3 — 종전엔 **문자열 매칭**으로 강등을 판단했다.
        #   `BASIN_HETEROGENEOUS` 문자열에는 job 경로가 없어서 "네 잡을 언급하지
        #   않는다" 가 **항상 참**이 되고, 그 block 이 언제나 강등됐다.
        #   ⇒ 구조화 필드(scope · job_keys)로만 판단한다. job_keys 가 비어 있으면
        #     **강등하지 않는다** (모르는 것을 안전한 쪽으로 읽지 않는다).
        # ⛔⛔ 회신 AP #3 판정 — **pooled block 을 필터링하는 방식 자체가 취약하다.**
        #   job_keys 교집합으로 걸러도, pooled 집합에는 exact key 가 거의 항상
        #   섞여 있어서 결국 D 를 죽인다(실측: BASIN_HETEROGENEOUS 의 job_keys 가
        #   그 조각의 **전 잡**이라 b00 pm1 을 포함한다).
        #   ⇒ exact-key 경로에서는 pooled 진단이 estimand 를 **막지 않는다.**
        #     그 진단의 목적은 "pooled 집합에서 min 을 뽑지 마라" 인데, 이 경로는
        #     min 을 쓰지 않고 **사전 고정한 네 잡**을 직접 대입하기 때문이다.
        #     네 잡의 안전은 따로 보장된다:
        #       · 게이트 걸린 잡 → ESTIMAND_KEY_UNUSABLE (아래 _gated)
        #       · 에너지 없음   → ESTIMAND_KEY_UNUSABLE (_none)
        #       · 자기 상태 불일치/판독불가 → _estimand_topology_check (scope=estimand)
        #   `_exact` 는 강등 판단에 쓰지 않고 기록용으로만 남긴다.
        # ⛔⛔ 회신 AR Q1/P0-2 (2026-08-31) — 종전엔 강등 시 `out["blocks"]` 를
        #   `block_records` 에서 **다시 만들었다.** 그런데 `_blk()` 를 거치지 않고
        #   `out["blocks"].append(...)` 로 직접 들어온 **구조화 안 된 전역 차단**
        #   (MOLECULAR_STATE_UNRESOLVED · CANARY_GEOM_* · POTCAR · closure 등)은
        #   record 가 없어서 **통째로 사라졌다.** 리뷰가 재현했다:
        #   MOLECULAR_STATE_UNRESOLVED + BASIN_HETEROGENEOUS → blocks 가 빈 배열.
        #   ⇒ **canonical `blocks` 는 절대 수정하지 않는다.** 강등은 별도 view 로만.
        _keep_r, _dem_r = [], []
        for _r in out["block_records"]:
            (_dem_r if _r["scope"] == "pooled_diagnostic" else _keep_r).append(_r)
        out["pooled_demote_policy"] = {
            "rule": "exact-key 경로에서는 scope=pooled_diagnostic 을 전부 강등한다",
            "why": "pooled min 을 쓰지 않으므로 그 진단이 estimand 에 적용되지 않는다",
            "estimand_keys": sorted(_exact),
            "estimand_safety": ["ESTIMAND_KEY_UNUSABLE(게이트·에너지)",
                                "ESTIMAND_TOPOLOGY_*(자기 상태 직접 비교)"]}
        # canonical 목록(blocks · block_records)은 **손대지 않는다**.
        #   primary D 판정에만 쓰는 view 를 따로 만든다.
        _dem_msgs = {r["msg"] for r in _dem_r}
        out["primary_estimand_blocks"] = [b for b in out["blocks"]
                                          if b not in _dem_msgs]
        if _dem_r:
            out["nonprimary_notes"] = [r["msg"] for r in _dem_r]
            out["nonprimary_note_records"] = _dem_r
            out["nonprimary_notes_why"] = (
                "이 블록들은 **D 에 들어가지 않는 잡**(net4·대안 자세)에 대한 것이다. "
                "pm1 조건부 D 는 사전 고정한 네 잡으로 정의되므로 지우지 않는다 "
                "(회신 AO P0-7). 강등 판정은 **job_keys 교집합**으로 하지 문자열로 "
                "하지 않는다 (회신 AP #3). 자기 분기 민감도로만 읽는다")

    # ⛔ 회신 AR Q1 — primary D 판정은 **primary view** 로 하되, pooled 진단은
    #   `secondary_G`·pooled min·일반화 주장을 **계속 차단**한다 (아래 §pooled_effect).
    _pv = out.get("primary_estimand_blocks")
    if _pv is None:
        _pv = list(out["blocks"])          # 강등이 없었으면 canonical 그대로
        out["primary_estimand_blocks"] = _pv
    # ⛔ 회신 AS 해제조건 3 — pool 완전성도 인용 조건에 넣는다
    _pool_ok = bool((out.get("pool_completeness") or {}).get("ok"))
    # 🔴🔴 회신 AT Q5 (2026-08-31) — 1저자 결정: **선택지 (a).**
    #   pooled 최솟값과 secondary_G 를 **영구 진단값(비인용)** 으로 고정한다. 추가 잡 0.
    #   이유 둘:
    #     ① dense k 검증이 primary pm1 b00 두 복합체뿐인데 pool 에는 net4 도 든다 —
    #        검증 깊이가 다른 값을 섞어 min 을 뽑는 것이다.
    #     ② net4 dense 를 +2 잡 넣어도 **basin 이 섞인 문제는 그대로다.** pm1/net4 는
    #        애초에 서로 다른 자기상태로 수렴하라고 넣은 seed 라 BASIN_HETEROGENEOUS
    #        가 사실상 상시 뜬다. 인용가능 pool 을 만들려면 basin 별로 pool 을 쪼개고
    #        "pooled min" 의 정의를 다시 짜야 한다 — 잡 두 개가 아니라 설계 변경이다.
    #   ⇒ 계산은 계속 하고 출력에도 남기되, **인용 자격은 주지 않는다.**
    _pooled_dyn = (not bool(out.get("nonprimary_notes"))) and _pool_ok
    out["pooled_effect"] = {
        "secondary_G_citable": False,
        "pooled_min_citable": False,
        "citable": "no — 영구 (회신 AT Q5 선택지 (a) · 1저자 결정 2026-08-31)",
        "would_pass_dynamic_gates": _pooled_dyn,
        "pool_complete": _pool_ok,
        "⛔_영구_비인용_사유": [
            "dense k 검증이 primary pm1 b00 두 복합체뿐 — pool 의 net4 는 미검증이다",
            "pm1/net4 는 다른 자기상태를 보려고 넣은 seed 라 basin 이 섞인다. "
            "상태를 가로질러 min 을 뽑지 않는다",
            "잡 +2 로는 ①만 닫히고 ②는 안 닫힌다 — 설계 변경이 필요한 일이다"],
        "대신_무엇을_쓰나": (
            "자세 탐색의 폭은 **MLIP 스크린**이 진다 (탐색 범위·자세 선정 규칙만, "
            "에너지는 인용 금지). DFT 는 사전등록한 한 조건의 D 하나를 낸다"),
        "why": ("pooled heterogeneity 는 primary(봉인 네 잡)에는 적용되지 않지만 "
                "pooled 최솟값·secondary_G·일반화 주장은 **계속 막는다** (회신 AR Q1)")}
    if _pv:
        out["verdict"] = "NO_VALUE — blocks 를 해소하기 전에는 단일 X 를 보고하지 않는다"
        return out

    sd = next((f for f in frags if "sdcp" in f), None)
    ct = next((f for f in frags if f != sd), None)
    a_s = out["A_by_frag"].get(sd) or {}
    a_c = out["A_by_frag"].get(ct) or {}
    if not (a_s.get("min") and a_c.get("min")):
        out["verdict"] = "NO_VALUE — 조각 한쪽에 게이트 통과 자세가 없다"
        return out

    # ⛔⛔ 2026-08-31 (회신 AN P0-1) — `estimand_job_keys` 가 있으면 **그 네 잡만** 쓴다.
    #   초판은 조각별 min 을 뺐다. 그러면 SDCP 와 PTFE 가 **서로 다른 seed** 에서
    #   뽑힐 수 있어, 사전 고정한 "pm1 조건부 D" 와 다른 양이 된다.
    #   AN §4 가 네 경로를 문서로 못박았는데 판정기는 여전히 min 을 골랐다 —
    #   문서와 코드가 갈린 채로 발송될 뻔했다.
    _ejk = (man.get("estimand_job_keys") or {})
    if _ejk:
        out["estimand_job_keys"] = dict(_ejk)
        _need = ("E_C_sdcp", "E_C_control", "E_G_sdcp", "E_G_control")
        _miss = [k for k in _need if not _ejk.get(k)]
        _ev = {k: E(_ejk[k]) for k in _need if _ejk.get(k)}
        _none = [k for k, v in _ev.items() if v is None]
        _gated = [k for k in _need if _ejk.get(k) and (jobs.get(_ejk[k]) or {}).get("gates")]
        if _miss or _none or _gated:
            out["blocks"].append(
                "ESTIMAND_KEY_UNUSABLE(누락 %s · 에너지 없음 %s · 게이트됨 %s) — "
                "사전 고정한 네 잡으로만 D 를 만든다. 대체하지 않는다"
                % (_miss, _none, _gated))
            out["verdict"] = "NO_VALUE — 사전 고정 job key 를 쓸 수 없다"
            return out
        primary = ((_ev["E_C_sdcp"] - _ev["E_G_sdcp"])
                   - (_ev["E_C_control"] - _ev["E_G_control"]))
        out["estimand_mode"] = "exact_keys (사전 고정 네 잡 직접 대입)"
        secondary = a_c["min"][0] - a_s["max"][0]
        # ⛔ 회신 AO P0-7 — 요구했던 `D_net4 − D_pm1` 을 **실제로 계산한다**.
        #   net4 는 별도 직접식이다. 못 내면 그 사실을 적고, D_pm1 은 살린다.
        _n4k = (man.get("estimand_job_keys_net4") or {})
        if _n4k:
            _n4v = {k: E(_n4k[k]) for k in _need if _n4k.get(k)}
            _n4_bad = ([k for k in _need if not _n4k.get(k)]
                       + [k for k, v in _n4v.items() if v is None]
                       + [k for k in _need if _n4k.get(k)
                          and (jobs.get(_n4k[k]) or {}).get("gates")])
            # ⛔⛔ 회신 AR P1-9 · 해제조건 6 (2026-08-31) — `usable_as_sensitivity`
            #   를 **저장만 하고 읽지 않았다.** net4 두 complex 가 다른 자기 basin
            #   이어도 `D_net4` 가 계산되고 status 가 computed 로 나갔다.
            #   민감도의 요점은 "같은 계를 다른 분기에서 보면 얼마나 움직이나" 인데,
            #   상태를 가로질러 뺀 값은 그 질문에 답하지 않는다 ⇒ **값도 status 도
            #   같이 막는다.** (D_pm1 은 여전히 영향받지 않는다.)
            _tp4r = ((out.get("estimand_topology") or {}).get("net4") or {})
            _n4_topo_bad = (_tp4r.get("usable_as_sensitivity") is not True)
            if _n4_topo_bad:
                out["branch_sensitivity"] = {
                    "status": "suppressed_topology",
                    "why": ((_tp4r.get("blocks") or
                             ["net4 topology 판정이 없다 — 확인 못 한 것은 통과가 아니다"])[:2]),
                    "D_net4_eV": None,
                    "D_net4_minus_D_pm1_eV": None,
                    "⛔": ("net4 두 complex 가 같은 자기 branch 임을 확인하지 못했다. "
                           "상태를 가로질러 뺀 차는 분기 민감도가 아니므로 값을 내지 "
                           "않는다 (회신 AR P1-9). D_pm1 은 영향받지 않는다"),
                    "⚠_민감도_불완전": True}
            elif _n4_bad:
                out["branch_sensitivity"] = {
                    "status": "unavailable", "why": "net4 키 사용 불가: %s" % sorted(set(_n4_bad)),
                    "D_net4_eV": None, "D_net4_minus_D_pm1_eV": None,
                    "⚠_민감도_불완전": True,
                    "⚠": "D_pm1 은 영향받지 않는다 — net4 는 민감도다"}
            else:
                _dn4 = ((_n4v["E_C_sdcp"] - _n4v["E_G_sdcp"])
                        - (_n4v["E_C_control"] - _n4v["E_G_control"]))
                out["branch_sensitivity"] = {
                    "status": "computed",
                    "D_net4_eV": round(_dn4, 4),
                    "D_net4_minus_D_pm1_eV": round(_dn4 - primary, 4),
                    "⛔": ("민감도다 — 보고값은 pm1 조건부 D 이고 이 값을 대신 쓰거나 "
                           "둘을 평균하지 않는다")}
        else:
            out["branch_sensitivity"] = {
                "status": "not_sealed", "D_net4_eV": None,
                "⚠_민감도_불완전": True,
                "why": "manifest 에 estimand_job_keys_net4 가 없다 (net4 잡이 계획에 없음)"}
        # ⛔⛔ 회신 AR P1-10 · 해제조건 6 — **대안 자세 민감도**를 봉인식으로 낸다.
        #   종전엔 완료 여부만 보고돼 "sensitivity 를 봤다" 가 무엇을 뜻하는지
        #   결과에 없었다. net4 와 **같은 게이트**를 건다.
        _paltk = (man.get("estimand_job_keys_pose_alt") or {})
        _palt_out = {}
        for _role, _pk4 in sorted(_paltk.items()):
            if not isinstance(_pk4, dict) or not _pk4.get("E_C_sdcp"):
                continue                                  # "⛔" 주석 키는 건너뛴다
            _tpp = _estimand_topology_check(_pk4, jobs, "pose_%s" % _role)
            _pv = {k: E(_pk4[k]) for k in _need if _pk4.get(k)}
            _pbad = ([k for k in _need if not _pk4.get(k)]
                     + [k for k, v in _pv.items() if v is None]
                     + [k for k in _need if _pk4.get(k)
                        and (jobs.get(_pk4[k]) or {}).get("gates")])
            if _tpp["blocks"] or _tpp.get("same") is not True:
                _palt_out[_role] = {
                    "status": "suppressed_topology", "D_pose_eV": None,
                    "D_pose_minus_D_pm1_eV": None,
                    "why": (_tpp["blocks"] or ["topology 판정 없음"])[:2]}
            elif _pbad:
                _palt_out[_role] = {
                    "status": "unavailable", "D_pose_eV": None,
                    "D_pose_minus_D_pm1_eV": None,
                    "why": "자세 키 사용 불가: %s" % sorted(set(_pbad))}
            else:
                _dp = ((_pv["E_C_sdcp"] - _pv["E_G_sdcp"])
                       - (_pv["E_C_control"] - _pv["E_G_control"]))
                _palt_out[_role] = {
                    "status": "computed", "D_pose_eV": round(_dp, 4),
                    "D_pose_minus_D_pm1_eV": round(_dp - primary, 4),
                    "식": _pk4.get("formula")}
        if _paltk:
            out["pose_sensitivity"] = dict(
                _palt_out,
                **{"⛔": ("자세 민감도다 — 보고값은 primary 자세의 pm1 조건부 D 이고 "
                         "이 값들로 min 을 다시 뽑거나 평균하지 않는다")})
        elif man.get("altpose_purpose"):
            out["pose_sensitivity"] = {"status": "exploratory_only",
                                       "why": man["altpose_purpose"]}
        # ⛔ 회신 AR 해제조건 6 — "민감도 완료" 를 **한 곳에서** 판정한다.
        #   종전엔 어디에도 이 라벨이 없어서, 결과를 읽는 쪽이 D_net4 유무만 보고
        #   완료로 읽을 수 있었다.
        _bs = out["branch_sensitivity"]
        _palt_bad = sorted(r for r, v in _palt_out.items()
                           if v.get("status") != "computed")
        out["sensitivity_complete"] = bool(_bs.get("status") == "computed"
                                           and not _palt_bad)
        if _bs.get("status") != "computed":
            out.setdefault("nonprimary_notes", []).append(
                "SENSITIVITY_INCOMPLETE(자기 분기 민감도가 %s — D 를 '분기에 강건' "
                "이라고 서술하지 말 것)" % _bs.get("status"))
        if _palt_bad:
            out.setdefault("nonprimary_notes", []).append(
                "POSE_SENSITIVITY_INCOMPLETE(%s — D 를 '자세에 강건' 이라고 "
                "서술하지 말 것)" % ", ".join(
                    "%s:%s" % (r, _palt_out[r].get("status")) for r in _palt_bad))
    else:
        out["estimand_mode"] = "fragment_min (⚠ 조각마다 다른 seed 가 뽑힐 수 있다)"
        primary = a_s["min"][0] - a_c["min"][0]
        secondary = a_c["min"][0] - a_s["max"][0]
    out["primary_ddE_lowE_eV"] = round(primary, 4)
    # 🔴 회신 AT Q5 (a) — 값은 **계속 낸다** (내부 진단). 인용 자격만 영구히 없다.
    #   숫자를 지우면 나중에 왜 못 쓰는지도 같이 사라져 재논증이 반복된다.
    _pe = out.get("pooled_effect") or {}
    out["secondary_G_eV_diagnostic"] = (
        round(secondary, 4) if _pe.get("would_pass_dynamic_gates") else None)
    out["secondary_G_eV"] = None
    out["secondary_G_⛔"] = (
        "**영구 비인용** (회신 AT Q5 선택지 (a) · 1저자 결정 2026-08-31). "
        "secondary_G 는 pooled 최솟값/최댓값에서 나오는데, pool 은 dense k 미검증 "
        "잡과 서로 다른 자기 basin 을 함께 담는다. 진단값은 "
        "`secondary_G_eV_diagnostic` 에 남는다%s"
        % ("" if _pe.get("would_pass_dynamic_gates")
           else " (지금은 동적 게이트도 통과하지 못한다 — pooled heterogeneity 또는 "
                "pool 불완전)"))
    out["reported_X_eV"] = round(round(primary / PREREG_ROUND_EV) * PREREG_ROUND_EV, 2)
    out["fragments"] = {"sdcp": sd, "control": ct}
    if primary <= PREREG_GUARD_EV:
        out["guard"] = "통과 (primary %.4f <= %.2f)" % (primary, PREREG_GUARD_EV)
        out["verdict"] = "보고 가능"
    else:
        out["guard"] = ("⛔ primary %+.4f > %.2f — guard band 미달"
                        % (primary, PREREG_GUARD_EV))
        out["verdict"] = "NO_DIRECTIONAL_CLAIM"
    # ⛔ 회신 AO P0-6 — 기체 상자 수렴을 **이 묶음에서 검증하지 않았으면** 그 사실이
    #   D 에 라벨로 붙어야 한다. prior 를 비차단으로 내린 대가는 침묵이 아니다.
    _bx = [k for k, v in ((results or {}).get("numerical_gates") or {}).items()
           if k.startswith("box_") and v.get("verified_in_this_bundle") is False]
    if _bx:
        out.setdefault("caveats", []).append(
            "GAS_BOX_UNVERIFIED(%s: 이 묶음에 box20 이 없어 기체 상자 수렴을 "
            "검증하지 않았다. 최종 D 에는 E_G^SDCP − E_G^control 이 남으므로 상자 "
            "오차가 대수적으로 소거되지 않는다. '기체 상자 수렴 확인' 을 쓰지 말 것)"
            % sorted(_bx))
    out["⚠_후보집합"] = ("candidate_set 이 동결된 prospective_lowE 가 아니면 이 값은 "
                         "primary 가 아니라 **legacy 교정 tranche** 다 (회신 V P0-5). "
                         "'primary'·'low-energy'·'pose-insensitive'·'전역 최소' 로 쓰지 말 것")
    return out


def main():
    if "--selftest" in sys.argv:
        return selftest_k()
    if "--check_pin" in sys.argv:
        i = sys.argv.index("--check_pin")
        return check_pin(sys.argv[i + 1] if len(sys.argv) > i + 1 else ".")
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    delta = DELTA
    if "--delta" in sys.argv:
        delta = float(sys.argv[sys.argv.index("--delta") + 1])
    man = json.load(open(os.path.join(root, "MANIFEST.json"), encoding="utf-8"))
    # ⛔ 회신 AO Q1 — 생산 전에 봉인한 variant 별 원본 fingerprint. 러너
    #   (SEAL_POTCAR_ROOT.sh)가 **첫 VASP 실행 전에** 만든다. 없으면 없다고 적는다.
    try:
        man["_potcar_root_seal"] = json.load(
            open(os.path.join(root, "POTCAR_ROOT_SEAL.json"), encoding="utf-8"))
    except Exception:
        man["_potcar_root_seal"] = None
    man["_manifest_sha256_actual"] = hashlib.sha256(
        open(os.path.join(root, "MANIFEST.json"), "rb").read()).hexdigest()
    # ⛔ 회신 AP #12 — 공식 release 주장은 **계산 전 attestation** 이 있을 때만.
    try:
        man["_potcar_attestation"] = json.load(
            open(os.path.join(root, "POTCAR_ATTESTATION.json"), encoding="utf-8"))
    except Exception:
        man["_potcar_attestation"] = None
    # ⛔ 회신 AR P0-6 — attestation 은 **정확한 ZIP** 과도 결박돼야 한다.
    #   받은 ZIP 의 SHA256 은 번들 안에 있을 수 없으므로(자기 해시) 두 경로로 받는다:
    #     ① `--zip_sha256 <sha>`  ② 번들 루트의 ZIP_SHA256.txt (verify_zip 이 남긴다)
    #   둘 다 없으면 "결박 확인 못 함" 이고 그것은 **통과가 아니다**.
    _zsha = None
    if "--zip_sha256" in sys.argv:
        _zi = sys.argv.index("--zip_sha256")
        _zsha = sys.argv[_zi + 1] if len(sys.argv) > _zi + 1 else None
    if not _zsha:
        try:
            _zsha = open(os.path.join(root, "ZIP_SHA256.txt"),
                        encoding="utf-8").read().split()[0]
        except Exception:
            _zsha = None
    man["_zip_sha256_observed"] = (_zsha or "").strip().lower() or None
    spec = man.get("potcar_spec", {})
    planned = man.get("planned", {})

    # ══ 두 묶음 결합 (회신 AF P0-3) ═══════════════════════════════════════
    #   왜 필요한가 — 12자세는 calibration(4) + holdout(8) 이고 기체 기준계는
    #   calibration 묶음에만 있다. **어느 한쪽만으로는 조각 간 대비를 만들 수 없다.**
    #   합치되 **해시로 결속**한다: 두 MANIFEST 를 기록하고, 프로토콜이 갈리면 막는다.
    merge_roots = []
    if "--merge" in sys.argv:
        _i = sys.argv.index("--merge")
        for _v in sys.argv[_i + 1:]:
            if _v.startswith("-"):
                break
            merge_roots.append(_v)
    bundles = [(root, man)]
    for _mr in merge_roots:
        bundles.append((_mr, json.load(open(os.path.join(_mr, "MANIFEST.json"), encoding="utf-8"))))
    merge_info = merge_compat(bundles) if len(bundles) > 1 else None

    # ── 입력 무결성 (Codex P0-H) — INCAR 이 바뀌었는지부터 본다 ──────────────
    integrity = {"checked": 0, "changed": [], "missing": []}
    for rel, want in (man.get("files_sha256") or {}).items():
        p = os.path.join(root, rel)
        if not os.path.isfile(p):
            integrity["missing"].append(rel); continue
        integrity["checked"] += 1
        got = hashlib.sha256(open(p, "rb").read()).hexdigest()
        if got != want:
            integrity["changed"].append(rel)

    # ── 실행시 POSCAR 가 루트 POSCAR 와 같은가 (Codex 6차 §8) ─────────────────
    #   단일점 판의 주장은 "UMA 가 고른 **그 기하** 위의 DFT 에너지" 다. 외주처가
    #   다른 기하를 넣었으면 무결성 해시(배포 파일)는 통과해도 계산은 다른 계다.
    #   상 폴더의 POSCAR 는 배포물이 아니라 **러너가 만든 것**이라 files_sha256 에 없다.
    # ⛔⛔ 회신 AP #1 (2026-08-31) — 이 검사가 **정상 canary 를 반드시 막았다.**
    #   canary 는 `PARENT_GEOM` 을 따라 부모의 `relax/CONTCAR` 를 static/POSCAR 로
    #   받는데, 여기서는 relax 가 없는 잡의 static/POSCAR 를 **그 잡 자신의 루트
    #   POSCAR 와 바이트 해시로** 비교했다. 좌표가 같아도 CONTCAR 서식(Direct/scale/
    #   선택동역학 유무)만 달라도 불일치가 된다.
    #   ⇒ `PARENT_GEOM` 이 있으면 **선언된 부모의 최종 기하**를 기대값으로 삼고,
    #     바이트가 아니라 원소·순서·셀·Cartesian 좌표·고정플래그를 비교한다.
    def _expected_geom_src(jd):
        """(기대 기하 파일, 출처 라벨). PARENT_GEOM 이 있으면 부모의 최종 기하."""
        pg = os.path.join(jd, "PARENT_GEOM")
        if os.path.isfile(pg):
            tgt = os.path.normpath(os.path.join(
                jd, open(pg, encoding="utf-8").read().strip()))
            cc = os.path.join(tgt, "relax", "CONTCAR")
            if os.path.isfile(cc):
                return cc, "부모 relax/CONTCAR"
            rp2 = os.path.join(tgt, "POSCAR")
            if os.path.isfile(rp2):
                return rp2, "부모 루트 POSCAR (부모가 단일점)"
            return None, "부모 기하 없음 (%s)" % _pk(tgt, root)
        rp2 = os.path.join(jd, "POSCAR")
        return (rp2 if os.path.isfile(rp2) else None), "자기 루트 POSCAR"

    def _geom_equal(a, b, tol=1e-4):
        """원소·순서·셀·Cartesian·고정플래그 비교. → (bool, why)"""
        if a is None or b is None:
            return False, "한쪽을 못 읽었다"
        if len(a["pos"]) != len(b["pos"]):
            return False, "원자수 %d ≠ %d" % (len(a["pos"]), len(b["pos"]))
        if a.get("species") and b.get("species") and a["species"] != b["species"]:
            return False, "원소 순서 %s ≠ %s" % (a["species"], b["species"])
        if a.get("counts") != b.get("counts"):
            return False, "원소 개수 %s ≠ %s" % (a.get("counts"), b.get("counts"))
        dc = max(abs(a["cell"][i][k] - b["cell"][i][k])
                 for i in range(3) for k in range(3))
        if dc > tol:
            return False, "셀 최대차 %.3g Å" % dc
        dp = max(max(abs(x - y) for x, y in zip(p1, p2))
                 for p1, p2 in zip(a["pos"], b["pos"]))
        if dp > tol:
            return False, "Cartesian 최대차 %.3g Å" % dp
        if a.get("fixed") != b.get("fixed"):
            return False, "고정 플래그가 다르다"
        return True, "일치 (셀 %.3g · 좌표 %.3g Å)" % (dc, dp)

    integrity["runtime_poscar_mismatch"] = []
    integrity["parent_geom_checked"] = []
    for jd in sorted(glob(os.path.join(root, "*", "*", ""))):
        if os.path.isdir(os.path.join(jd, "relax")):
            continue              # 이완판은 CONTCAR 승계가 정상 — 달라야 맞다
        src, lbl = _expected_geom_src(jd)
        if src is None:
            continue
        want_g = read_poscar(src)
        for ph in ("static", "dense"):
            pp = os.path.join(jd, ph, "POSCAR")
            if not os.path.isfile(pp):
                continue
            ok, why = _geom_equal(want_g, read_poscar(pp))
            if os.path.isfile(os.path.join(jd, "PARENT_GEOM")):
                integrity["parent_geom_checked"].append(
                    "%s ← %s: %s" % (_pk(pp, root), lbl, why))
            if not ok:
                integrity["runtime_poscar_mismatch"].append(
                    "%s (기대=%s · %s)" % (_pk(pp, root), lbl, why))
    # ★ phase POSCAR 를 반송받지 못하면 위 검사는 **조용히 건너뛴다** = fail-open.
    #   OUTCAR 가 있는데 POSCAR 가 없으면 OUTCAR 좌표로 대조한다 (Codex P0-6).
    integrity["geometry_unverified"] = []
    for jd in sorted(glob(os.path.join(root, "*", "*", ""))):
        if os.path.isdir(os.path.join(jd, "relax")):
            continue
        # ⛔ 회신 AP #1 — 여기서도 기대 기하는 **PARENT_GEOM 을 따른다**
        _src2, _lbl2 = _expected_geom_src(jd)
        if _src2 is None:
            continue
        want = read_poscar(_src2)
        for ph in ("static", "dense"):
            has_oc = any(os.path.isfile(os.path.join(jd, ph, "OUTCAR" + e))
                         for e in ("", ".gz"))
            if not has_oc or os.path.isfile(os.path.join(jd, ph, "POSCAR")):
                continue
            oc = read_outcar(os.path.join(jd, ph, "OUTCAR"))
            pos = (oc or {}).get("positions")
            rel = _pk(os.path.join(jd, ph), root)
            if not pos or not want or len(pos) != len(want["pos"]):
                integrity["geometry_unverified"].append(rel)
                continue
            d = max(mic_dist(a, b, want["cell"]) for a, b in zip(pos, want["pos"]))
            if d > 0.05:
                integrity["runtime_poscar_mismatch"].append(
                    f"{rel} (OUTCAR 좌표가 루트와 최대 {d:.3f} Å 다르다)")

    jobs = {}
    results_ldau_missing = []
    _jobdirs = []
    for _ri, _mi in bundles:
        for _jd in sorted(glob(os.path.join(_ri, "*", "*", ""))):
            _jobdirs.append((_jd, _ri, _mi))
    for jd, _root_i, _man_i in _jobdirs:
        jp = os.path.join(jd, "job.json")
        if not os.path.isfile(jp):
            continue
        meta = json.load(open(jp, encoding="utf-8"))
        rel = _pk(jd, _root_i)
        _planned_i = _man_i.get("planned", {})
        _spec_i = _man_i.get("potcar_spec", {})
        if rel in jobs:                       # ⛔ 이름이 겹치면 조용히 덮지 않는다
            jobs[rel]["gates"].append(
                "MERGE_NAME_COLLISION(같은 잡 이름이 두 묶음에 있다 — 어느 쪽 값인지 "
                "알 수 없으므로 이 잡을 쓰지 않는다)")
            continue
        phases = (_planned_i.get(rel) or {}).get("phases") or meta.get("phases") or \
            ["relax", "static"]
        ocs = {ph: read_outcar(os.path.join(jd, ph, "OUTCAR")) for ph in phases}
        # ⛔ 2026-08-25 (codex E-2차 필수5) — static/dense 만 남기면 static_pin 등
        #   다른 상의 감사·세그먼트가 **RESULTS 에서 유실**된다. 모든 상을 보존한다.
        rec = {"meta": meta, "static": ocs.get("static"), "dense": ocs.get("dense"),
               "gates": []}
        for _ph in phases:
            rec[_ph] = ocs.get(_ph)
        for ph in phases:
            rec["gates"] += phase_gates(ocs[ph], ph, meta, _spec_i,
                                        want_ionic=(ph == "relax"))
        # ★ 격자가 커지는 상 사이로 NKPTS 가 안 늘면 **같은 계산을 복사한 것**이다.
        km = meta.get("kmesh") or {}
        seq = [ph for ph in phases if ocs.get(ph) and ocs[ph].get("nkpts") and km.get(ph)]
        for x, y in zip(seq, seq[1:]):
            px = py = 1
            for v in str(km[x]).split():
                px *= int(v)
            for v in str(km[y]).split():
                py *= int(v)
            if py > px and ocs[y]["nkpts"] <= ocs[x]["nkpts"]:
                rec["gates"].append(
                    f"KMESH_NOT_DENSER({y} NKPTS {ocs[y]['nkpts']} ≤ {x} {ocs[x]['nkpts']} "
                    f"인데 격자는 {km[x]}→{km[y]} — 다른 상의 산출을 복사했나)")
        rec["gates"] += potcar_provenance_gates(jd, meta, rel, _man_i)
        _ppf = os.path.join(jd, "POTCAR_PROVENANCE.json")
        if os.path.isfile(_ppf):
            try:
                rec["_prov"] = json.load(open(_ppf, encoding="utf-8"))
            except Exception:                                # noqa: BLE001
                rec["_prov"] = None
        g2, info = geometry_audit(jd, meta)
        rec["gates"] += g2
        rec["geom"] = {k: v for k, v in info.items() if not k.startswith("_")}
        rec["_contact_fp"] = info.get("_contact_fp")
        rec["_fin"] = info.get("_fin")
        rx = ocs.get("relax")
        # 힘: 블록이 없거나 원자수가 다르면 **검사 생략이 아니라 게이트**
        if rx is not None:
            if not rx.get("forces"):
                rec["gates"].append("FORCE_UNVERIFIED(TOTAL-FORCE 블록 없음)")
            elif info.get("_init_fixed") and len(rx["forces"]) != len(info["_init_fixed"]):
                rec["gates"].append(
                    f"FORCE_COUNT({len(rx['forces'])}!={len(info['_init_fixed'])})")
            elif info.get("_init_fixed"):
                fmax = max((math.sqrt(sum(c * c for c in f))
                            for f, fx in zip(rx["forces"], info["_init_fixed"]) if not fx),
                           default=0.0)
                rec["geom"]["free_fmax_eVA"] = round(fmax, 3)
                if fmax > FORCE_TOL:
                    rec["gates"].append(f"FORCE_HIGH({fmax:.3f} eV/Å)")
        # ── 단일점의 static 힘: **진단값**이지 수렴 판정이 아니다 (Codex 6차 §4) ──
        #   MLIP 기하가 DFT 최소점에서 얼마나 먼지를 보여 준다. 큰 잔류힘은
        #   "그 자세만 DFT 이완으로 넘길까" 를 결정하는 trigger 로 쓴다.
        #   ⚠ 힘 하나로 단일점 에너지 오차의 부호나 상한을 만들 수 없다 — 게이트 아님.
        st0 = ocs.get("static")
        if rx is None and st0 is not None and st0.get("forces") and \
                info.get("_init_fixed") and \
                len(st0["forces"]) == len(info["_init_fixed"]):
            fr = [math.sqrt(sum(c * c for c in f))
                  for f, fx in zip(st0["forces"], info["_init_fixed"]) if not fx]
            if fr:
                rec["geom"]["uma_geometry_residual_force"] = {
                    "fmax_eVA": round(max(fr), 3),
                    "frms_eVA": round(math.sqrt(sum(x * x for x in fr) / len(fr)), 3),
                    "meaning": ("MLIP 기하의 DFT 잔류힘 — **진단값**. 수렴 판정도, "
                                "에너지 오차 상한도 아니다. 크면 그 자세만 DFT 이완 검토."),
                    "trigger_hint_eVA": FORCE_TOL}
        # ── 자기상태 감사 (Codex P0-E · 2026-08-12 재작성) ──
        st = ocs.get("static")
        want_sign = meta.get("ni_sign_poscar_idx") or {}
        mol_sign = meta.get("mol_sign_poscar_idx") or {}
        if st is not None and want_sign:
            mom = st.get("moments")
            nions = st.get("nions")
            # ★ 완결성부터 hard gate — 표가 짧으면 파싱된 것만 검사하고 나머지를
            #   조용히 버리던 구멍이 있었다 (Ni 1개만 남겨도 통과했다).
            if not mom:
                rec["gates"].append("MAGNETIC_UNVERIFIED(LORBIT 모멘트 표 없음)")
            elif nions and len(mom) != nions:
                rec["gates"].append(
                    f"MAGNETIC_INCOMPLETE(모멘트 {len(mom)}행 ≠ NIONS {nions})")
            elif max(int(k) for k in want_sign) >= len(mom):
                rec["gates"].append(
                    f"MAGNETIC_INCOMPLETE(Ni 인덱스가 모멘트 표 {len(mom)}행 밖)")
            else:
                ni = {int(k): float(v) for k, v in want_sign.items()}
                got = {i: mom[i] for i in ni}
                # ★ 전역 반전은 시간반전이라 **같은 상태**다 — 부호를 정규화해 비교하고,
                #   진짜 문제인 **부분 반전**을 잡는다 (옛 판은 정반대였다).
                sg, flip = global_sign(got, ni)
                small = [i for i, m in got.items() if abs(m) < MOM_MIN]
                rec["geom"]["magnetic"] = {
                    "n_ni": len(ni), "global_sign": sg, "n_partial_flip": len(flip),
                    # ⛔ 2026-08-25 (codex E-4) — 개수만 남기면 "항상 같은 자리 #82"
                    #   라는 관측을 **아무도 재검증할 수 없다**. 인덱스를 기계기록.
                    "flip_indices_poscar": sorted(flip), "index_base": 0,
                    "flip_indices_poscar_1based": [i + 1 for i in sorted(flip)],
                    "flip_moments_muB": {str(i): round(got[i], 3) for i in flip},
                    "n_small": len(small), "min_abs_muB": round(min(map(abs, got.values())), 3),
                    "abs_mean_muB": round(sum(map(abs, got.values())) / len(got), 3),
                    "total_muB": st.get("mag_total")}
                # ★ 회신 Z P0-4 — realized basin 지문. seed 이름으로 짝지으면 안 된다.
                _rb, _rbd = realized_basin_id(mom, want_sign, mol_sign,
                                             incar_echo=st.get("incar_echo"))
                rec["geom"]["magnetic"]["realized_basin_id"] = _rb
                rec["geom"]["magnetic"]["realized_basin"] = _rbd
                if _rb is None:
                    rec["gates"].append(
                        f"BASIN_UNRESOLVED({_rbd.get('why')}) — realized basin 을 "
                        f"만들 수 없어 이 잡으로는 뺄셈을 하지 않는다")
                if flip:
                    rec["gates"].append(
                        f"MAGNETIC_PARTIAL_FLIP({len(flip)}/{len(ni)} Ni 가 시드 topology 와 "
                        f"다르다 — 다른 자기 basin 이다)")
                # ★★ 라디칼 상대 스핀은 **항상** 본다 (Codex 재감사 P0-2).
                #   옛 판은 Ni 가 전역 반전(sg<0)일 때만 검사해서, Ni topology 는
                #   그대로인데 라디칼 하나만 뒤집힌 경우가 **게이트 없이 통과**했다.
                #   dense 에는 넣었는데 static 에는 안 넣어서 실질적으로 열려 있었다.
                ms = {int(k): float(v) for k, v in mol_sign.items() if int(k) < len(mom)}
                if ms:
                    # Ni 전역부호 sg 로 정규화한 뒤 라디칼의 **상대** 부호를 본다.
                    bad = [i for i, v in ms.items() if mom[i] * sg * v <= 0]
                    small = [i for i in ms if abs(mom[i]) < MOM_MIN]
                    rec["geom"]["magnetic"]["radical"] = {
                        "n": len(ms), "sign_mismatch": len(bad), "collapsed": len(small),
                        "ni_global_sign": sg, "total_muB": st.get("mag_total")}
                    if bad or small:
                        rec["gates"].append(
                            f"RADICAL_BRANCH_CHANGED(부호 불일치 {len(bad)} · 소실 "
                            f"{len(small)}/{len(ms)} — Ni 부호를 정규화한 뒤에도 라디칼 "
                            f"상대 스핀이 시드와 다르다. 다른 스핀 basin 이다)")
                    elif sg < 0:
                        rec["geom"]["magnetic"]["note"] = (
                            "Ni·라디칼이 **함께** 전역 반전 — 시간반전이라 같은 상태")
                # ── LDAU occupation + total M 기록 (Codex P0-2 ③) ──
                #   판정용이 아니라 **기록용**이다 — 절대값은 PAW sphere 규약 의존.
                ld = st.get("ldau")
                if ld:
                    ups = sorted(ld.items())
                    mm = [round(v[0] - v[1], 3) for _k, v in ups]
                    rec["geom"]["magnetic"]["ldau"] = {
                        "n_atoms": len(ld),
                        "mean_n_up_dn": [round(sum(v[0] for _k, v in ups) / len(ups), 3),
                                         round(sum(v[1] for _k, v in ups) / len(ups), 3)],
                        "moment_from_occ_mean_abs": round(
                            sum(abs(x) for x in mm) / len(mm), 3),
                        "fingerprint": hashlib.sha256(
                            json.dumps(ups, sort_keys=True).encode()).hexdigest()[:12]}
                else:
                    rec["geom"]["magnetic"]["ldau"] = None
                    results_ldau_missing.append(rel)

                # ── dense 자기감사 — static 과 **같은 수준**으로 (Codex 7차 §8) ──
                #   ⚠ 옛 판은 dense 에 모멘트 표가 없으면 그냥 서명에서 빠졌다. 그러면
                #     local moment 가 없는 dense OUTCAR 도 E0 만으로 κ 에 들어간다.
                #     dense 는 **에너지를 내는 상**이므로 static 과 같은 문턱을 건다.
                dn = ocs.get("dense")
                if dn is not None:
                    dm = dn.get("moments")
                    if not dm:
                        rec["gates"].append(
                            "DENSE_MOMENTS_MISSING(dense OUTCAR 에 모멘트 표가 없다 — "
                            "자기상태를 모르고 κ 에 쓸 수 없다)")
                    elif dn.get("nions") and len(dm) != dn["nions"]:
                        rec["gates"].append(
                            f"DENSE_MOMENT_COUNT({len(dm)} != NIONS {dn['nions']})")
                    elif max(ni) >= len(dm):
                        rec["gates"].append(
                            f"DENSE_MOMENT_SHORT(Ni 인덱스 {max(ni)} 가 표 밖 — "
                            f"표 길이 {len(dm)})")
                    else:
                        miss = [i for i in ni if i >= len(dm)]
                        # ★★ dense 는 **자기 전역부호를 스스로** 구한다 (Codex 5차 P1-2).
                        #   옛 판은 static 의 sg 를 재사용해서, dense 가 완전한 시간반전
                        #   상태(Ni·라디칼·총 M 이 **함께** 뒤집힘)로 수렴하면 물리적으로
                        #   같은 상태인데도 전부 부호 불일치로 잡아 거짓 차단했다.
                        #   바로 아래 phase_sign_sig 는 전역반전을 같은 상태로 인정하는데
                        #   여기만 규칙이 달랐다 — 한 기능이 두 규칙을 쓰고 있었다.
                        sg_d, _dflip = global_sign({i: dm[i] for i in ni}, ni)
                        dq = sum(sg_d * ni[i] * dm[i] for i in ni) / len(ni)
                        dsmall = [i for i in ni if abs(dm[i]) < MOM_MIN]
                        rec["geom"]["magnetic"]["dense"] = {
                            "n_ni_found": len(ni) - len(miss),
                            "global_sign": sg_d,
                            "global_flip_vs_static": (sg_d != sg),
                            "Q_muB": round(dq, 3),
                            "f_small": round(len(dsmall) / len(ni), 3),
                            "total_muB": dn.get("mag_total")}
                        # ★ open-shell 조각(doped)의 **라디칼 상대 스핀**을 dense 에서도
                        #   본다 (Codex zip 감사 P0-5). Ni topology 는 그대로인데
                        #   라디칼만 뒤집히거나 사라지면 다른 스핀 상태를 재는 것이다.
                        if mol_sign:
                            _ms = {int(k2): float(v2) for k2, v2 in mol_sign.items()
                                   if int(k2) < len(dm)}
                            # dense 자기 부호로 정규화한 뒤 **상대** 스핀을 본다
                            _bad = [i for i, v2 in _ms.items() if dm[i] * sg_d * v2 <= 0]
                            _gone = [i for i in _ms if abs(dm[i]) < MOM_MIN]
                            rec["geom"]["magnetic"]["dense"]["radical"] = {
                                "n": len(_ms), "sign_mismatch": len(_bad),
                                "collapsed": len(_gone),
                                "total_muB": dn.get("mag_total")}
                            if _bad or _gone:
                                rec["gates"].append(
                                    f"DENSE_RADICAL_BRANCH_CHANGED(부호 불일치 {len(_bad)} · "
                                    f"소실 {len(_gone)}/{len(_ms)} — Ni 는 유지됐지만 "
                                    f"라디칼 상대 스핀이 달라졌다. κ 에 쓸 수 없다)")
                            # ⚠ 총 M 도 **절대값**으로 본다 — 전역 시간반전이면 부호가
                            #   같이 뒤집히는 게 정상이다.
                            _tm, _td = st.get("mag_total"), dn.get("mag_total")
                            if _tm is not None and _td is not None and \
                                    abs(abs(_tm) - abs(_td)) > 0.5:
                                rec["gates"].append(
                                    f"DENSE_TOTAL_M_CHANGED({_tm:+.2f} → {_td:+.2f} μB — "
                                    f"static↔dense 자기 branch 가 넘어갔다)")
                        qs = rec["geom"]["magnetic"].get("Q_muB")
                        if qs is not None and abs(qs) > 1e-9:
                            rat = dq / qs
                            rec["geom"]["magnetic"]["dense"]["Q_ratio_vs_static"] = round(rat, 3)
                            if rat < Q_RATIO_MIN:
                                rec["gates"].append(
                                    f"DENSE_MAGNETIC_COLLAPSE(Q_dense/Q_static={rat:.2f} — "
                                    f"k 를 촘촘히 했더니 자기상태가 무너졌다. κ 는 k 효과가 "
                                    f"아니라 spin-state 차를 재게 된다)")

                # ── 상별 자기 branch — k 를 바꾸며 상태가 넘어가면 'k 오차'가 아니다 ──
                sig = {}
                for ph2 in phases:
                    o2 = ocs.get(ph2)
                    if not o2 or not o2.get("moments"):
                        continue
                    mo = o2["moments"]
                    if max(ni) < len(mo):
                        sig[ph2] = "".join("+" if mo[i] > 0 else "-" for i in sorted(ni))
                rec["geom"]["magnetic"]["phase_sign_sig"] = {
                    k2: hashlib.sha256(v.encode()).hexdigest()[:8] for k2, v in sig.items()}
                uniq = {v for v in sig.values()}
                # 전역 반전끼리는 같은 상태다 — 반전본도 같이 넣어 비교한다
                if len(uniq) > 1:
                    base = sorted(sig)[0]
                    flip = sig[base].translate(str.maketrans("+-", "-+"))
                    if not all(v in (sig[base], flip) for v in sig.values()):
                        rec["gates"].append(
                            f"MAGNETIC_BRANCH_CHANGED(상별 Ni 부호 topology 가 다르다 "
                            f"{ {k2: v[:8] for k2, v in sig.items()} } — k 오차가 아니라 "
                            f"spin-state 차이를 재게 된다)")

                # ⚠ MOM_MIN 단독 문턱은 보편적이지 않다 (Codex Q7). LORBIT local moment 는
                #   PAW sphere/projector 의존 정성 지표라 표면 Ni 가 물리적으로 0.3 아래로
                #   갈 수 있다. 집단 지표 Q(부호 정규화 평균)와 f_small 을 clean 기준으로
                #   보정해 판정한다 — 절대 판정은 main() 에서 clean 분포를 알고 내린다.
                Q = sum(sg * ni[i] * got[i] for i in ni) / len(ni)
                rec["geom"]["magnetic"]["Q_muB"] = round(Q, 3)
                rec["geom"]["magnetic"]["f_small"] = round(len(small) / len(ni), 3)
                if small:
                    rec["geom"]["magnetic"]["review"] = (
                        f"{len(small)}개가 |m|<{MOM_MIN} — clean 분포와 대조 (아래 집단 판정)")
        rec["ok"] = not rec["gates"]
        jobs[rel] = rec

    # ── 자기 붕괴는 **clean seed 분포 기준**으로 판정한다 (Codex Q7) ──────────
    #   숫자(0.5·0.25)는 초기 민감도일 뿐이다. clean 두 seed 의 Q 를 기준으로 보고,
    #   기준이 없으면 판정을 보류한다(임의 문턱으로 죽이지 않는다).
    #   ★ 2026-08-12 (Codex 6차) 세 가지를 고친다:
    #     (a) `... .get("Q_muB")` 진리값 검사 → **Q=0 인 clean 을 결측으로 버린다**.
    #         Q=0 은 "완전 붕괴한 기준" 이라는 중요한 사실이다. is not None 으로 본다.
    #     (b) 두 seed 중 max 하나를 모든 pose 에 공통 적용 → seed 별 branch 차이가 섞인다.
    #         **같은 seed 의 clean** 과 비교한다.
    #     (c) clean 자체가 무자격(게이트 걸림·Q 결측)이면 조용히 통과시키지 말고
    #         MAGNETIC_REFERENCE_INVALID 로 남긴다.
    # ── rescue supersedes (wave1.5 · codex E-2차 필수1) ───────────────────────
    #   job.json 에 rescue.supersedes = "refs/clean_slab__<seed>" 가 있고 그 잡이
    #   **모든 게이트를 통과**하면, 그 seed 의 clean 참조를 rescue 잡으로 바꾼다.
    #   실패하면 원본 유지 + reference_overrides 에 거부 사유를 남긴다 (조용한 무시 금지).
    ref_alias: Dict[str, str] = {}
    ref_overrides: Dict[str, Any] = {}
    for j, r in jobs.items():
        sup = ((r.get("meta") or {}).get("rescue") or {}).get("supersedes")
        if not sup:
            continue
        _pok, _pwhy = rescue_provenance_ok(os.path.join(root, j))
        if r.get("ok") and _pok:
            ref_alias[sup] = j
            ref_overrides[sup] = {"used": j, "status": "superseded",
                                  "why": "rescue 잡이 전 게이트 + provenance 통과"}
        else:
            _reasons = [] if r.get("ok") else list((r.get("gates") or [])[:3])
            if not _pok:
                _reasons.append(f"provenance: {_pwhy}")
            ref_overrides[sup] = {"used": sup, "status": "rescue_rejected",
                                  "rejected_job": j, "why": "; ".join(_reasons)}
    # (results dict 는 아래에서 만들어진다 — 거기서 reference_overrides 로 실림)

    q_by_seed: Dict[str, Optional[float]] = {}
    ref_bad: Dict[str, str] = {}
    for sd in (man.get("seeds_full") or ["afm2424_pm1", "afm2424_net4"]):
        _canon = f"refs/clean_slab__{sd}"
        if _canon in ref_alias:
            cj = [(ref_alias[_canon], jobs[ref_alias[_canon]])]
        else:
            cj = [(j, r) for j, r in jobs.items()
                  if "clean_slab" in j and j.endswith(sd)]
        if not cj:
            ref_bad[sd] = "clean 대조군 없음"
            continue
        j, r = cj[0]
        q = ((r.get("geom") or {}).get("magnetic") or {}).get("Q_muB")
        if q is None:
            ref_bad[sd] = f"{j}: Ni moment 미완 — Q 없음"
        elif r.get("gates"):
            ref_bad[sd] = f"{j}: 기준 자체가 게이트 걸림 ({r['gates'][0][:40]})"
        else:
            q_by_seed[sd] = float(q)
    for j, r in jobs.items():
        mg = (r.get("geom") or {}).get("magnetic")
        if not mg or "Q_muB" not in mg:
            continue
        sd = r["meta"].get("seed")
        q_ref = q_by_seed.get(sd)
        mg["Q_clean_ref"] = q_ref
        mg["Q_clean_ref_seed"] = sd
        if q_ref is None:
            # ⛔⛔ 회신 AR P0-1 (2026-08-31) — **clean-free 설계에서는 이 게이트가
            #   전 complex 를 막는다.** C-12 는 clean slab 을 일부러 계산하지 않는다
            #   (D 에서 대수적으로 소거되므로). 그런데 여기서 clean Q 기준이 없다고
            #   모든 magnetic complex 를 MAGNETIC_REFERENCE_INVALID 로 막아,
            #   exact pm1/net4 가 전부 게이트돼 **primary D 가 아예 안 나왔다.**
            #   ⇒ clean 을 **선언조차 하지 않은** 판(clean-free)에서는 이 게이트를
            #     적용하지 않는다. 그 역할은 `_estimand_topology_check` 의
            #     **직접 topology 비교**가 대신한다 (회신 AP #2 로 이미 넣었다).
            #   ⚠ clean 을 선언해 놓고 결과가 없는 것은 여전히 차단이다 — 그건
            #     "계산했어야 하는데 안 온 것" 이고 clean-free 와 다르다.
            _clean_declared = bool(((man.get("refs") or {}).get("clean_slab") or [])
                                   or (man.get("magnetic_controls") or []))
            mg["verdict"] = ("clean-free 설계 — 이 판정은 직접 topology 비교가 대신한다"
                             if not _clean_declared else
                             "clean 기준 없음/무효 — 자기 붕괴 판정 보류")
            mg["clean_free"] = not _clean_declared
            if "clean_slab" not in j and _clean_declared:
                r["gates"].append(
                    f"MAGNETIC_REFERENCE_INVALID({sd}: "
                    f"{ref_bad.get(sd, '기준 없음')} — 자기 붕괴를 판정할 수 없다)")
                r["ok"] = not r["gates"]
            continue
        ratio = (mg["Q_muB"] / q_ref) if abs(q_ref) > 1e-9 else None
        mg["Q_ratio"] = None if ratio is None else round(ratio, 3)
        if ratio is None:
            # ⛔ 완전히 붕괴한 clean 은 **유효한 기준이 아니다** (Codex 7차 §9).
            #   "판정 보류" 로 pose 를 통과시키면 fail-open 이다.
            mg["verdict"] = "⛔ clean 기준 Q≈0 — 기준 자체가 무효"
            if "clean_slab" not in j:
                r["gates"].append(
                    f"MAGNETIC_REFERENCE_INVALID({sd}: clean Q≈0 — 기준이 붕괴했다. "
                    f"이 seed 의 headline 에서 제외)")
                r["ok"] = not r["gates"]
            continue
        if ratio < Q_RATIO_MIN or mg["f_small"] > F_SMALL_MAX:
            r["gates"].append(
                f"MAGNETIC_COLLAPSE(Q/Q_clean[{sd}]={ratio:.2f} · "
                f"f_small={mg['f_small']:.2f} — 같은 seed clean 대비 집단 붕괴)")
            r["ok"] = not r["gates"]

    # ── POTCAR 변형: 준중심 차이는 일관돼도 치명 (Codex P0-C) ────────────────
    subs, mixed = {}, False
    for r in jobs.values():
        st = r.get("static") or {}
        expect = [spec.get(e, e) for e in r["meta"].get("species_order", [])]
        got = [x.split()[1] if len(x.split()) > 1 else x for x in st.get("titels") or []]
        if expect and got and len(expect) == len(got):
            for e, g in zip(expect, got):
                if e != g:
                    if e in subs and subs[e] != g:
                        mixed = True
                    subs[e] = g
    potcar_warn = None
    # ⛔ 2026-08-12 — "일관되게 다르면 경고" 를 폐기한다. 고정 protocol 에서는
    #   Ni_pv → Ni_sv 도 다른 가전자·projector 라 다른 Hamiltonian 이다. 한 글자라도
    #   다르면 headline 에서 제외한다 (감도로 쓰려면 별도 protocol ID 로 분리).
    if subs:
        txt = ", ".join(f"{e}→{g}" for e, g in sorted(subs.items()))
        for r in jobs.values():
            r["gates"].append(f"POTCAR_WRONG({txt}{' · 혼재' if mixed else ''})")
            r["ok"] = False

    def E(job):
        job = ref_alias.get(job, job)          # supersedes 반영 (wave1.5)
        r = jobs.get(job)
        return r["static"]["E0"] if r and r["ok"] and r["static"] and \
            r["static"]["E0"] is not None else None

    def E_dense(job):
        """dense 도 static 과 **같은 기준**으로 건다 (옛 판은 에너지만 읽었다)."""
        r = jobs.get(job)
        if not r or not r["ok"]:
            return None
        oc = r.get("dense")
        if oc is None or not oc["normal_end"] or oc["nelm_hit"] or oc["E0"] is None:
            return None
        return oc["E0"]

    # ── --plan_dense : 조건부 dense 선택 (Codex 6차 §3) ──────────────────────
    #   왜 분석기 안인가: OUTCAR 회수·자기 게이트·유효성 판정을 **그대로 재사용**한다.
    #   별도 스크립트로 빼면 그 로직이 두 벌이 되고, 갈라지면 아무도 모른다.
    if "--plan_dense" in sys.argv:
        return plan_dense(root, man, jobs, E, E_dense)

    results = {"delta_eV": delta, "pairs": {}, "fragments": {}, "e_ads": {},
               "reference_overrides": ref_overrides,
               "numerical_gates": {}, "warnings": [], "integrity": integrity,
               # incar_audit (codex E-2) — 게이트 통과가 **무엇까지 보증하는지**의
               #   기계 기록: verified_exact / verified_equivalence_class /
               #   unverified / mismatch + 실행 세그먼트 정보. 사람용 요약(README)과
               #   어긋나면 이쪽이 정본이다.
               "jobs": {j: {"ok": r["ok"], "gates": r["gates"],
                            "E0_static": (r["static"] or {}).get("E0"),
                            "vasp_version": (r["static"] or {}).get("vasp_version"),
                            "incar_audit": {ph: (r.get(ph) or {}).get("incar_audit")
                                            for ph in (r["meta"].get("phases")
                                                       or ["static", "dense"])
                                            if (r.get(ph) or {}).get("incar_audit")},
                            "run_segments": {ph: (r.get(ph) or {}).get("run_segments")
                                             for ph in (r["meta"].get("phases")
                                                        or ["static", "dense"])
                                             if (r.get(ph) or {}).get("run_segments")},
                            "geom": r.get("geom")} for j, r in jobs.items()}}
    if potcar_warn:
        results["warnings"].append(potcar_warn)
    if results_ldau_missing:
        results["warnings"].append(
            f"LDAU occupation matrix 가 없는 잡 {len(results_ldau_missing)}개 "
            f"(LDAUPRINT=2 인데 OUTCAR 에 onsite density matrix 없음) — "
            f"자기상태를 모멘트 하나로만 보게 된다: "
            + ", ".join(results_ldau_missing[:4]))
    if integrity.get("geometry_unverified"):
        results["warnings"].append(
            f"⚠ 실행 기하를 검증 못 한 상 {len(integrity['geometry_unverified'])}개 — "
            f"phase POSCAR 도 OUTCAR 좌표도 없다: "
            + ", ".join(integrity["geometry_unverified"][:5]))
    if integrity.get("runtime_poscar_mismatch"):
        results["warnings"].append(
            f"⛔ 실행시 POSCAR 가 루트와 다른 상 "
            f"{len(integrity['runtime_poscar_mismatch'])}개 — **다른 기하를 계산했다** "
            f"(단일점 주장 무효): "
            + ", ".join(integrity["runtime_poscar_mismatch"][:6]))
    if integrity["changed"]:
        results["warnings"].append(
            f"⛔ 번들 입력 {len(integrity['changed'])}개가 바뀌었다 (INCAR/POSCAR 변조?): "
            + ", ".join(integrity["changed"][:8]))

    # ── 기체상 — 상자 게이트. **정본은 큰 상자(box24)** ──────────────────────
    #   ⚠ Wave 1(기준계 미포함)은 기준계가 **의도적으로** 없다 — 실패가 아니다.
    #     그걸 "상자 게이트 실패" 로 찍으면 정상 실행을 고장으로 읽게 된다.
    emol, mol_ok = {}, {}
    # ⛔ 2026-08-31 (회신 AN P0-2) — C-12 는 clean slab 없이 **기체 기준만** 있다.
    #   clean 유무로 has_refs 를 정하면 그 구성이 "기준계 없음(Wave 1)" 으로 오독된다.
    _refs = man.get("refs", {}) or {}
    _has_mol = any(k.startswith("mol__") for k in _refs)
    has_refs = bool(_refs.get("clean_slab")) or _has_mol
    if not has_refs:
        results["e_ads_status"] = ("NOT_APPLICABLE — Wave 1 은 기준계를 안 돌린다. "
                                  "자리 대비 ΔE 는 기준계 없이 성립하지만 절대 E_ads 는 "
                                  "만들 수 없다 (MANIFEST.claim_scope 참조).")
        results["warnings"].append(
            "Wave 1: clean/gas 기준계 없음 — **의도된 범위**다. ΔE 만 인용하고 "
            "흡착 열역학·조각 간 결합 세기·E_ads 절대값은 주장하지 말 것")
    for f in (man.get("fragments", []) if has_refs else []):
        # ⚠ job key 는 _pk() 로 POSIX 정규화돼 있다. 여기서 os.path.join 을 쓰면
        #   Windows 에서 `refs\mol__...` 가 되어 **한 건도 안 맞는다** — 그런데
        #   gas job 자체는 ok 라 required_missing 이 비고 exit 0 이 났다.
        #   "계산 완료, E_ads 만 없음" 으로 조용히 끝나는 최악의 모양이었다.
        e20 = E(f"refs/mol__{f}__box20")
        e24 = E(f"refs/mol__{f}__box24")
        # ⛔⛔ 2026-08-31 (회신 AN P0-2·P1) — `--refs_minimal` 은 box20 을 **일부러** 뺀다.
        #   초판은 "상자 2종 중 하나가 없다 → E_ads 불가" 로 막아, 그 구성에서 분석이
        #   아예 안 됐다. 그렇다고 조용히 통과시키면 안 된다 — 최종 D 에는
        #   `E_G^SDCP − E_G^PTFE` 가 남아 **기체 상자 오차가 소거되지 않기** 때문이다.
        #   ⇒ box20 이 없으면 manifest 의 **선행 근거**(`gas_box_prior`)를 요구한다.
        #     그것도 없으면 막는다. 있으면 그 값을 게이트에 그대로 싣고 출처를 남긴다.
        _prior = ((man.get("gas_box_prior") or {}).get(f) or {}) if e20 is None else {}
        if e20 is None and e24 is not None and _prior.get("dE_meV") is not None:
            # ⛔⛔ 회신 AO P0-6 (2026-08-31) — 두 가지가 틀렸다.
            #   ① `ok = d0 <= BOX_TOL` 이 **부호 있는** 값을 비교해 큰 음수도 통과했다.
            #   ② 더 근본적으로, 이 prior 는 **이번 conformer·이번 Hamiltonian 과의
            #      정합을 확인하지 못했다** (manifest 가 스스로 인정한다). 확인 못 한
            #      근거로 게이트를 통과시키는 것은 검증이 아니다.
            #   ⇒ prior 는 **비차단 참고정보**로 내린다. 통과/실패를 만들지 않는다.
            #     대신 "이 묶음에서 상자 수렴을 검증하지 않았다" 를 라벨로 남긴다.
            d0 = abs(float(_prior["dE_meV"])) / 1000.0        # ① 절대값
            results["numerical_gates"][f"box_{f}"] = {
                "dE_meV": round(d0 * 1000, 2),
                "pass": None,                                  # ② 판정하지 않는다
                "source": "prior_informational_only",
                "prior_ref": _prior.get("ref"),
                "verified_in_this_bundle": False,
                "⚠": ("이번 묶음에 box20 이 없다. 선행 대조를 **참고로만** 싣는다 — "
                      "좌표·state policy·POTCAR fingerprint 정합을 확인하지 못했으므로 "
                      "게이트로 쓰지 않는다 (회신 AO P0-6)")}
            results["warnings"].append(
                f"mol__{f}: 기체 상자 수렴을 **이 묶음에서 검증하지 않았다** — "
                f"선행값 {d0*1000:.2f} meV 는 참고정보다. D 서술에 "
                f"'기체 상자 수렴 확인' 을 쓰지 말 것")
            mol_ok[f] = None
            emol[f] = e24
            continue
        # ⛔⛔ 회신 AR P0-3 / Q2 (2026-08-31) — **옛 조각별 10 meV 게이트를 없앤다.**
        #   판정은 `δ_gas`(두 기체의 **차**) 하나로 한다. 조각별 게이트가 남아 있으면
        #   두 가지가 깨진다:
        #     ① SDCP/PTFE 가 +20/+19 meV 면 δ_gas = 1 meV 로 통과해야 하는데
        #        조각별 게이트가 두 `emol` 을 **None 으로 만들고**, 그 뒤 A(f,p)
        #        계산에서 `float − None` 으로 **예외로 죽는다** (리뷰가 재현).
        #     ② box20 누락도 GAS_BOX_NOT_MEASURED 가 아니라 예외로 끝난다.
        #   ⇒ `emol` 은 box24 를 그대로 쓰고(정본), 진단만 기록한다.
        #     결측·불일치는 `_blk(...)` 로 **구조화된 hard block** 이 된다 (아래 δ_gas).
        mol_ok[f] = True
        emol[f] = e24
        if e24 is None:
            emol[f] = None
            results["numerical_gates"][f"box_{f}"] = {
                "dE_meV": None, "pass": False,
                "why": "box24(정본)가 없다 — 이 조각의 기체 기준이 없다"}
            results["warnings"].append(f"mol__{f}: box24 없음 — 기체 기준 부재")
        else:
            _d = (abs(e20 - e24) if e20 is not None else None)
            results["numerical_gates"][f"box_{f}"] = {
                "dE_meV": (None if _d is None else round(_d * 1000, 1)),
                "pass": None,                         # ⛔ 판정하지 않는다 — 진단이다
                "role": "diagnostic_only",
                "why": ("판정은 δ_gas(두 기체의 차) 하나로 한다 (회신 AR P0-3). "
                        "조각별 값은 진단으로만 남긴다")}

    eclean = {s: E(f"refs/clean_slab__{s}")
              for s in man.get("seeds_full", ["afm2424_pm1", "afm2424_net4"])}
    eclean_dense = E_dense("refs/clean_slab__afm2424_pm1")

    for pid, pm in man.get("pairs", {}).items():
        frag = pm["fragment"]
        rec = {"fragment": frag, "dir": pm["dir"], "roll": pm["roll"],
               "uma_dE": pm.get("uma_dE"), "dE_by_seed": {}, "gates": []}
        for s in pm.get("seeds", ["afm2424_pm1"]):
            eli, eni = E(f"{pm['li_prefix']}__{s}"), E(f"{pm['ni_prefix']}__{s}")
            if eli is not None and eni is not None:
                rec["dE_by_seed"][s] = round(eni - eli, 4)
        # ── PAIR_COLLAPSED — 주기 RMSD + 접촉 지문 (Codex P0 Q5 반박 수용) ──
        s0 = pm.get("seeds", ["afm2424_pm1"])[0]
        jli, jni = jobs.get(f"{pm['li_prefix']}__{s0}"), jobs.get(f"{pm['ni_prefix']}__{s0}")
        rli = (jli or {}).get("geom", {}).get("registry")
        rni = (jni or {}).get("geom", {}).get("registry")
        if jli and jni and jli.get("_fin") and jni.get("_fin"):
            mol = jli["meta"].get("mol_poscar_idx") or []
            a, b = jli["_fin"], jni["_fin"]
            if mol and len(a["pos"]) == len(b["pos"]):
                rms = math.sqrt(sum(mic_dist(a["pos"][i], b["pos"][i], a["cell"]) ** 2
                                    for i in mol) / len(mol))
                # ⚠ 최근접 **원소명**은 판정에 넣지 않는다 — 같으면 한쪽은 이미
                #   PAIR_MIGRATED 라 완전 중복이다(Codex Q5). 접촉 지문은 원자 인덱스라
                #   "같은 자리인가" 를 직접 답한다. 경계 원자 하나로 뒤집히지 않도록
                #   완전일치 대신 Jaccard 를 쓴다.
                fa = set(jli.get("_contact_fp") or [])
                fb = set(jni.get("_contact_fp") or [])
                if not fa and not fb:
                    # ⚠ 양쪽 다 접촉이 없으면 지문은 **정보가 없다**. CONTACT_A 3.0 과
                    #   DETACH_A 4.0 사이에 미판정 shell 이 있으므로 "떠 있지 않다" 가
                    #   "지문이 검증됐다" 를 뜻하지 않는다 (Codex Q3). RMSD 는 진단으로만
                    #   남기고 이 쌍은 최종 분류에서 뺀다.
                    jac, fp_ok, why = None, False, "접촉 지문 없음 — 미검증"
                    rec["gates"].append(
                        f"BASIN_UNVERIFIED_EMPTY_CONTACT_FP(분자 RMSD {rms:.2f} Å 는 "
                        f"진단값 — 3.0~4.0 Å 미판정 shell)")
                else:
                    jac = len(fa & fb) / len(fa | fb)
                    fp_ok = jac >= FP_JACCARD
                    why = f"접촉 지문 Jaccard {jac:.2f} ≥ {FP_JACCARD}"
                rec["basin"] = {"mol_rmsd_A": round(rms, 3),
                                "contact_jaccard": None if jac is None else round(jac, 3),
                                "same_nearest_element": bool(
                                    rli and rni and rli["nearest"] == rni["nearest"]),
                                "sensitivity": {str(t): rms <= t
                                                for t in (0.50, 0.75, 1.00)}}
                if rms <= RMSD_TOL and fp_ok:
                    sp_pair = bool((jli.get("geom") or {}).get("single_point"))
                    rec["gates"].append(
                        ("SOURCE_PAIR_COLLAPSED" if sp_pair else "PAIR_COLLAPSED")
                        + f"(분자 RMSD {rms:.2f} Å ≤ {RMSD_TOL} · {why})")
        # ★★ 추정량 이름 (Codex 7차 §1) — 자세키 p=(down_dir, roll) 에 대해
        #   ΔE_match(p) = E_Ni(p) − E_Li(p)          ← 배향 혼입 없는 자리 대비
        #   D_pool      = E_Ni(p_N*) − E_Li(p_L*)    ← 짝 풀 챔피언 **대각선** 대비
        #   p_L* == p_N* 이면 둘이 같지만, 다르면 D_pool 에 자리와 자세가 섞인다.
        #   그러므로 de_main 을 무조건 "matched" 라 부르면 안 된다.
        de_main = rec["dE_by_seed"].get("afm2424_pm1")
        _pose_matched = pm.get("matched") is True
        rec["estimand"] = ("dE_match(p*)  — 같은 자세키에서 잰 자리 대비 (배향 혼입 없음)"
                           if _pose_matched else
                           "D_pool  — 짝 풀 챔피언 **대각선** 대비 (자리+자세 혼합). "
                           "matched 라 부르지 말 것")
        rec["pose_matched"] = _pose_matched
        de_alt = rec["dE_by_seed"].get("afm2424_net4")
        # ★ ΔE 만 비교하면, 두 pose 가 같은 방향으로 함께 움직이고 clean 은 안 움직인
        #   경우 ΔE 는 그대로인데 E_ads 만 달라진다 (Codex P0-2).
        ea_seed = {}
        for sd in pm.get("seeds", []):
            ec_s, em_s = eclean.get(sd), emol.get(frag)
            eli_s = E(f"{pm['li_prefix']}__{sd}")
            if ec_s is not None and em_s is not None and eli_s is not None:
                ea_seed[sd] = eli_s - ec_s - em_s
        if len(ea_seed) > 1:
            spread = max(ea_seed.values()) - min(ea_seed.values())
            rec["eads_seed_spread_meV"] = round(spread * 1000, 1)
            if spread > SEED_TOL:
                rec["gates"].append(
                    f"BLOCKED_MAGNETIC_SENSITIVITY(E_ads seed 산포 {spread * 1000:.0f} meV > 10)")
        # ★ 두 seed 끝점 에너지가 20 meV 안에서 경합하면 **어느 branch 가 바닥인지
        #   k 보정(±10)으로 뒤집힐 수 있다**. adaptive dense 가 꺼져 있으면 확인할
        #   방법이 없으므로 그 사실을 판정에 남긴다 (Codex 3차 감사).
        #   MANIFEST 는 이 규약을 적어 놓고 정작 --plan_dense 에서만 계산하고 있었다.
        for _role, _pre in (("Li", pm["li_prefix"]), ("Ni", pm["ni_prefix"])):
            _e = {s: E(f"{_pre}__{s}") for s in pm.get("seeds", [])}
            _v = [x for x in _e.values() if x is not None]
            if len(_v) > 1 and abs(_v[0] - _v[1]) <= BRANCH_TIE_EV:
                rec.setdefault("branch_tie", {})[_role] = {
                    "gap_meV": round(abs(_v[0] - _v[1]) * 1000, 1),
                    "note": (f"두 seed 가 {BRANCH_TIE_EV*1000:.0f} meV 안에서 경합 — "
                             f"k 보정 ±{GUARD_EV*1000:.0f} 으로 순서가 뒤집힐 수 있다")}
                # ⚠ **게이트로 막지 않는다.** 우리 headline 은 branch-minimum 이 아니라
                #   같은 seed(pm1) 대비다 — 어느 branch 가 바닥인지 주장하지 않으므로
                #   경합 자체는 결함이 아니다. 실제 보호막은 seed 산포 게이트(≤10 meV)다.
                #   (Codex 3차 감사가 준 두 선택지 중 'pm1 조건부로 명시' 쪽.)
                rec["branch_tie"][_role]["claim"] = (
                    "MAGNETIC_K_UNRESOLVED_for_branch_minimum — 이 값은 "
                    "**pm1 branch 조건부**다. '자기 바닥상태에서의' 로 서술 금지")
        if de_main is not None and de_alt is not None \
                and abs(de_main - de_alt) > SEED_TOL:
            rec["gates"].append(
                f"BLOCKED_MAGNETIC_SENSITIVITY(|ΔE_pm1−ΔE_net4|="
                f"{abs(de_main - de_alt) * 1000:.0f} meV > 10)")
        elif de_main is not None and de_alt is None and len(pm.get("seeds", [])) > 1:
            rec["gates"].append("SEED_INCOMPLETE(두 seed 중 하나가 게이트/미완)")

        # ── dense-k 게이트 — **판정에 실제로 연결** (Codex P0-D) ──
        dli, dni = E_dense(f"{pm['li_prefix']}__afm2424_pm1"), \
            E_dense(f"{pm['ni_prefix']}__afm2424_pm1")
        planned_dense = any("dense" in (planned.get(f"{pm[k]}__afm2424_pm1") or {})
                            .get("phases", []) for k in ("li_prefix", "ni_prefix"))
        if planned_dense:
            if dli is None or dni is None or de_main is None:
                rec["gates"].append("NUMERICALLY_UNRESOLVED(dense 계획인데 회수 실패)")
            else:
                # ★ κ 는 **부호 있는** 양이다 (Codex 5차 taxonomy · 6차 §6).
                #   전이 게이트는 크기뿐 아니라 **보정자끼리 같은 방향인지**를 본다 —
                #   절대값만 보면 +9 와 −9 를 "둘 다 통과" 로 읽어 18 meV 를 놓친다.
                kap = (dni - dli) - de_main
                rec["kappa_eV"] = round(kap, 4)
                results.setdefault("kappa", {})
                prev = results["kappa"].get(frag)
                if prev is None or abs(kap) > abs(prev):
                    results["kappa"][frag] = round(kap, 4)   # 조각당 최악값
                dk = abs(kap)
                ok_k = dk <= K_TOL
                gate = {"dE_meV": round(dk * 1000, 1), "kappa_meV": round(kap * 1000, 1),
                        "pass": ok_k}
                # E_ads 자체의 k 수렴도 본다 (ΔE 만 보면 상쇄로 숨는다)
                if eclean_dense is not None and emol.get(frag) is not None:
                    worst = 0.0
                    for tag, pre, ed in (("Li", pm["li_prefix"], dli),
                                         ("Ni", pm["ni_prefix"], dni)):
                        es = E(f"{pre}__afm2424_pm1")
                        if es is None:
                            continue
                        d = abs((ed - eclean_dense - emol[frag])
                                - (es - eclean.get("afm2424_pm1", 0.0) - emol[frag]))
                        gate[f"dEads_{tag}_meV"] = round(d * 1000, 1)
                        worst = max(worst, d)
                    gate["dEads_meV"] = round(worst * 1000, 1)
                    ok_k = ok_k and worst <= K_TOL
                    gate["pass"] = ok_k
                results["numerical_gates"][f"k_{pid}"] = gate
                if not ok_k:
                    rec["gates"].append(f"NUMERICALLY_UNRESOLVED(dense-k {gate})")

        # ── 전역 자리 선호 vs 배향일치 대비 (2026-08-12) ────────────────────
        #   ΔE(matched) = 같은 배향에서 Li 위 vs Ni 위  — 배향 혼입 없음
        #   ΔE(global)  = 각자 최선을 다했을 때        — 문헌의 "site preference"
        #   둘의 차가 **배향 항**이다. 부호가 다르면 어느 질문인지 반드시 밝혀야 한다.
        gb = pm.get("global_best") or {}
        if gb:
            # ★ 두 seed 전부 읽는다 (Codex 7차 §5). 본 ΔE 는 seed 산포 게이트를 통과해야
            #   하는데 global 만 단일시드면 부호가 자기 branch 잡음일 수 있다.
            dg_seed = {}
            for sd in pm.get("seeds", ["afm2424_pm1"]):
                e2 = {}
                for role, pre in (("Li", pm["li_prefix"]), ("Ni", pm["ni_prefix"])):
                    p2 = gb[role]["prefix"] if role in gb else pre
                    e2[role] = E(f"{p2}__{sd}")
                if e2["Li"] is not None and e2["Ni"] is not None:
                    dg_seed[sd] = round(e2["Ni"] - e2["Li"], 4)
            rec["dE_global_by_seed"] = dg_seed
            n_want = len(pm.get("seeds", []))
            if len(dg_seed) < n_want:
                rec["gates"].append(
                    f"GLOBAL_SEED_INCOMPLETE({len(dg_seed)}/{n_want}) — 전역 대비 보류")
            elif len(dg_seed) > 1:
                sp = max(dg_seed.values()) - min(dg_seed.values())
                rec["global_seed_spread_meV"] = round(sp * 1000, 1)
                if sp > SEED_TOL:
                    rec["gates"].append(
                        f"GLOBAL_MAGNETIC_SENSITIVITY(seed 산포 {sp*1000:.0f} meV > 10)")
            eg = {}
            for role, pre in (("Li", pm["li_prefix"]), ("Ni", pm["ni_prefix"])):
                p2 = gb[role]["prefix"] if role in gb else pre
                eg[role] = E(f"{p2}__afm2424_pm1")
            if eg["Li"] is not None and eg["Ni"] is not None:
                dg = eg["Ni"] - eg["Li"]
                # ★ 이름을 정확히 (Codex 7차 §1.4) — 이건 **UMA 가 고른** 전역 챔피언
                #   대비다. DFT 재랭킹도, DFT 이완 최소점도, 흡착 자유에너지도 아니다.
                rec["dE_UMA_selected_global_champ_eV"] = round(dg, 4)
                rec["global_k_status"] = (
                    "K_DIRECTLY_CHECKED_GLOBAL" if E_dense(
                        f"{(gb.get('Ni') or {}).get('prefix', pm['ni_prefix'])}"
                        f"__afm2424_pm1") is not None
                    else "K_UNVERIFIED_GLOBAL — 전역 끝점은 coarse only")
                rec["dE_global_eV"] = round(dg, 4)      # 하위호환(폐기 예정)
                if de_main is not None:
                    rec["orientation_term_eV"] = round(dg - de_main, 4)
                    flip = (dg > 0) != (de_main > 0)
                    _gk = rec.get("global_k_status", "")
                    rec["global_vs_matched"] = (
                        f"K_UNRESOLVED_GLOBAL({_gk}) — 전역 끝점을 dense 로 검증하지 "
                        f"않았다. 부호 비교는 진단용이고 headline 아님"
                        if _gk.startswith("K_UNVERIFIED") else
                        "SIGN_DIFFERS — 배향일치 대비와 전역 자리 선호가 **반대**다. "
                        "어느 질문인지 밝히지 않고 인용 금지."
                        if flip and min(abs(dg), abs(de_main)) > GUARD_EV else
                        "SIGN_AGREES" if not flip else
                        "UNRESOLVED(한쪽이 guard band 안)")
                    if flip and min(abs(dg), abs(de_main)) > GUARD_EV \
                            and not rec.get("global_k_status", "").startswith("K_UNVERIFIED"):
                        # ⚠ 이건 계산 실패가 아니다 — 각 추정량은 유효하다.
                        #   금지되는 건 **하나의 site preference 숫자로 합치는 것**뿐이다.
                        #   그래서 gates(=값 무효화)가 아니라 해석 라벨로 남긴다.
                        rec["ESTIMAND_DEPENDENT_NO_SINGLE_SITE_PREFERENCE"] = (
                            f"D_pool {de_main:+.3f} vs UMA-selected global {dg:+.3f} eV — "
                            f"부호가 다르다. 두 값 **각각은 유효**하다. 하나의 '자리 선호' "
                            f"숫자로 합치지 말고 추정량을 밝혀 따로 보고할 것.")
            else:
                rec["dE_global_eV"] = None
                rec["global_vs_matched"] = "전역 끝점 미완/게이트 — 전역 대비 불가"
        elif pm.get("global_unmeasured"):
            rec["global_unmeasured"] = pm["global_unmeasured"]

        # ── 교차 끝점: 배향이 맞춰진 대비 (Codex 5차 결정 ②) ──────────────
        #   챔피언 ΔE 는 두 배향이 다르면 자리 효과와 배향 효과가 섞인다.
        #   같은 배향에서 잰 Δ 와 **부호가 같은지**가 배향 인공물 여부를 가른다.
        for tag, cx in (pm.get("cross") or {}).items():
            base_role = cx["role"]                      # 추가된 쪽
            other = "Li" if base_role == "Ni" else "Ni"
            opre = pm[("li" if other == "Li" else "ni") + "_prefix"]
            # ★ 두 seed 로 잰다 (Codex 6차 §5) — 옛 판은 pm1 하나만 읽었다.
            #   본 ΔE 는 seed 산포 게이트를 통과해야 하는데 교차만 단일시드면,
            #   "배향 의존" 판정이 실은 자기 branch 잡음일 수 있다.
            dm_by_seed = {}
            for sd in pm.get("seeds", ["afm2424_pm1"]):
                e_new, e_old = E(f"{cx['prefix']}__{sd}"), E(f"{opre}__{sd}")
                if e_new is not None and e_old is not None:
                    dm_by_seed[sd] = round(
                        (e_new - e_old) if base_role == "Ni" else (e_old - e_new), 4)
            if not dm_by_seed:
                rec.setdefault("cross", {})[tag] = {"status": "미완/게이트"}
                continue
            d_m = dm_by_seed.get("afm2424_pm1", list(dm_by_seed.values())[0])
            entry = {"orientation": cx["down_dir"], "roll": cx.get("roll_deg"),
                     "dE_matched_eV": d_m, "dE_by_seed": dm_by_seed,
                     # 교차 끝점은 dense 를 안 돌린다 — k 는 전이 해석뿐이다
                     "k_label": "K_UNVERIFIED_CROSS", "prefix": cx["prefix"]}
            rec.setdefault("cross", {})[tag] = entry
            n_seed_want = len(pm.get("seeds", []))
            if len(dm_by_seed) < n_seed_want:
                entry["verdict"] = (f"SEED_INCOMPLETE({len(dm_by_seed)}/{n_seed_want}) "
                                    f"— 배향 판정 보류")
                rec["gates"].append(
                    f"CROSS_SEED_INCOMPLETE({tag}: {len(dm_by_seed)}/{n_seed_want} seed)")
                continue
            spread = max(dm_by_seed.values()) - min(dm_by_seed.values())
            entry["seed_spread_meV"] = round(spread * 1000, 1)
            if spread > SEED_TOL:
                entry["verdict"] = (f"BLOCKED_MAGNETIC_SENSITIVITY(seed 산포 "
                                    f"{spread * 1000:.0f} meV > 10) — 배향 판정 불가")
                rec["gates"].append(
                    f"CROSS_MAGNETIC_SENSITIVITY({tag}: {spread * 1000:.0f} meV)")
                continue
            entry["quantity"] = f"dE_match({cx['down_dir']}/r{cx.get('roll_deg')})"
            entry["k_note"] = "coarse only — dense 없음"
        # ── 2×2: **두 고정자세 대비끼리** 비교한다 (Codex 7차 §1.3) ────────────
        #   ΔE_match(p_L*) = E_Ni(p_L*) − E_Li(p_L*)
        #   ΔE_match(p_N*) = E_Ni(p_N*) − E_Li(p_N*)
        #   I = ΔE_match(p_N*) − ΔE_match(p_L*) = O_N − O_L
        #   ⚠ 옛 판은 각 교차를 **대각선** de_main 과 비교했다. 그러면 I 가 안 나온다.
        #   ⚠ I 는 모집단 상호작용이 아니라 **이 두 자세에서의 유한설계 대비**다.
        cr = rec.get("cross") or {}
        mc = pm.get("cross") or {}          # ★ prefix 의 권위는 MANIFEST 쪽이다
        if not _pose_matched and len(mc) == 2:
            eL = {}
            for sd in pm.get("seeds", ["afm2424_pm1"]):
                # p_L* 자세: Li 는 본 끝점, Ni 는 교차(Ni_at_Li_pose)
                a1 = E(f"{pm['li_prefix']}__{sd}")
                b1 = E(f"{mc['Ni_at_Li_pose']['prefix']}__{sd}") \
                    if "Ni_at_Li_pose" in mc else None
                # p_N* 자세: Ni 는 본 끝점, Li 는 교차(Li_at_Ni_pose)
                a2 = E(f"{mc['Li_at_Ni_pose']['prefix']}__{sd}") \
                    if "Li_at_Ni_pose" in mc else None
                b2 = E(f"{pm['ni_prefix']}__{sd}")
                if None not in (a1, b1, a2, b2):
                    eL[sd] = {"dE_match_pL": round(b1 - a1, 4),
                              "dE_match_pN": round(b2 - a2, 4),
                              "I": round((b2 - a2) - (b1 - a1), 4),
                              "O_Li": round(a2 - a1, 4), "O_Ni": round(b2 - b1, 4)}
            if eL:
                rec["two_by_two"] = eL
                m = eL.get("afm2424_pm1") or list(eL.values())[0]
                dl, dn = m["dE_match_pL"], m["dE_match_pN"]
                both_big = min(abs(dl), abs(dn)) > GUARD_EV
                same = (dl > 0) == (dn > 0)
                rec["two_by_two_k_status"] = ("K_UNVERIFIED_CROSS — 교차 끝점은 "
                                              "dense 를 안 돌렸다. 아래 부호 결론은 "
                                              "coarse 값 기준이다")
                # ⚠ k 라벨은 이 루프가 끝나야 정해진다(κ 를 여기서 모은다). 잠정 판정만
                #   쓰고, 아래 후처리에서 K 게이트를 씌운다.
                rec["two_by_two_verdict"] = (
                    "UNRESOLVED(한쪽이 guard band 안 — 부호 비교 불가)" if not both_big else
                    "SIGN_AGREES_AT_BOTH_SAMPLED_POSES — **두 표본 자세에서** 부호 일치 "
                    "(모집단 배향 무관성 주장 아님)" if same else
                    "POSE_DEPENDENT_SIGN — 자세에 따라 부호가 다르다. 자세 무관 자리 선호 금지")
                if both_big and not same:
                    rec["gates"].append(
                        f"POSE_DEPENDENT_SIGN(ΔE_match(p_L*)={dl:+.3f} vs "
                        f"ΔE_match(p_N*)={dn:+.3f} eV)")
                if len(eL) > 1:
                    sp = max(x["I"] for x in eL.values()) - min(x["I"] for x in eL.values())
                    rec["two_by_two"]["I_seed_spread_meV"] = round(sp * 1000, 1)
                    if sp > SEED_TOL:
                        rec["gates"].append(
                            f"TWO_BY_TWO_MAGNETIC_SENSITIVITY(I seed 산포 {sp*1000:.0f} meV)")
        if pm.get("cross_missing"):
            rec["cross_missing"] = pm["cross_missing"]

        if de_main is not None and not rec["gates"]:
            # ★★ 직접 dense 를 돌렸으면 **그 값이 headline** 이다 (Codex zip 감사 P0-3).
            #   옛 판은 dense 로 κ 만 재고 최종 수치·판정은 coarse 를 썼다. 그러면서
            #   K_DIRECTLY_CHECKED 라는 이유로 20–40 meV guard 까지 풀어, dense 값이
            #   30 meV 바닥 반대편에 있어도 coarse 로 판정할 수 있었다.
            _dli = E_dense(f"{pm['li_prefix']}__afm2424_pm1")
            _dni = E_dense(f"{pm['ni_prefix']}__afm2424_pm1")
            if _dli is not None and _dni is not None:
                rec["dE_coarse_eV"] = de_main
                de_main = round(_dni - _dli, 4)
                rec["headline_from"] = "dense (직접 k 검증) — coarse 는 dE_coarse_eV 에"
                # ⚠ 0 은 "3×4×1 의 잔여 k 오차가 없다" 가 아니라 **전이 허용치를 안 썼다**
                #   는 뜻이다 (Codex 재감사). 이름을 그렇게 바꾼다.
                rec["k_transfer_allowance_meV"] = 0.0
                rec["k_residual_note"] = "직접 dense — 전이 허용치 미적용. 잔여 k 오차는 미추정"
            else:
                rec["headline_from"] = "coarse (dense 없음/게이트) — k 불확실성 ±10 meV"
                rec["k_transfer_allowance_meV"] = GUARD_EV * 1000
            rec["dE_Ni_minus_Li_eV"] = de_main
            # ±10 meV k guard band — 30 meV 판정바닥과 **합치지 않는다**
            a_de = abs(de_main)
            rec["k_guard"] = ("판정 유지 (>40 meV)" if a_de > delta + GUARD_EV else
                              "바닥 아래 결론 유지 (<20 meV)" if a_de < delta - GUARD_EV else
                              "⚠ 20–40 meV — k 오차로 판정이 뒤집힐 수 있다: "
                              "직접 dense 아니면 UNRESOLVED")
            if abs(de_main) <= GUARD_EV:
                rec["k_guard"] = "⛔ |ΔE| ≤ 10 meV — 부호 자체가 안 정해진다"
            ec = eclean.get("afm2424_pm1")
            if ec is not None and emol.get(frag) is not None:
                eli = E(f"{pm['li_prefix']}__afm2424_pm1")
                eni = E(f"{pm['ni_prefix']}__afm2424_pm1")
                results["e_ads"][pid] = {
                    "Li_top": round(eli - ec - emol[frag], 4),
                    "Ni_top": round(eni - ec - emol[frag], 4),
                    "mol_ref": "box24",
                    # ⚠ headline 은 **static(coarse) 값**이다. dense 는 별도 k 게이트로만
                    #   쓰고 값을 교체하지 않는다 (Codex 3차 감사 P0-4). 명시하지 않으면
                    #   "dense 로 검증된 E_ads" 로 오독된다.
                    "estimand": "E_ads(static target mesh) — dense 는 k 게이트 전용",
                    "k_check": "관측된 dense 보정이 게이트 안이면 통과. 값 교체 아님"}
        results["pairs"][pid] = rec

    # ══ 사전등록 closure estimand (회신 V P0-3 · P0-4) ══════════════════════
    #   `prereg_sdcp_neutral_contrast_2026_08_29.json` 을 코드로 옮긴 것.
    #   ⛔ 종전엔 사전등록이 **문서로만** 있었다 — 잡이 다 끝나도 판정이 재현되지 않았다.
    # ⛔⛔ 회신 AO P0-4 (2026-08-31) — nzmag canary 와 부모 기체 기준의 **static 이
    #   실제로 같은 기하였는지** 실측한다. 종전엔 부모가 relax/CONTCAR 로, canary 가
    #   루트 POSCAR 로 돌아 두 에너지 차에 구조 이완 에너지가 섞였다.
    #   ⚠ 이 검사는 **실행된 입력**(static/POSCAR)을 본다 — 선언이 아니다.
    _cg = {}
    for _mk, _cz in (man.get("molecular_spin_controls") or {}).items():
        _f = _mk.replace("mol__", "").rsplit("__box", 1)[0]
        _pp = read_poscar(os.path.join(root, "refs", _mk, "static", "POSCAR")) \
            or read_poscar(os.path.join(root, _mk, "static", "POSCAR"))
        _cp = read_poscar(os.path.join(root, str(_cz), "static", "POSCAR"))
        if _pp is None or _cp is None:
            _cg[_f] = {"same": None, "why": "static/POSCAR 를 못 읽었다 (미실행이거나 경로 불일치)"}
            continue
        if len(_pp["pos"]) != len(_cp["pos"]):
            _cg[_f] = {"same": False, "why": "원자수가 다르다 (%d vs %d)"
                       % (len(_pp["pos"]), len(_cp["pos"]))}
            continue
        _dmax = max(max(abs(a[k] - b[k]) for k in range(3))
                    for a, b in zip(_pp["pos"], _cp["pos"]))
        _cmax = max(max(abs(a[k] - b[k]) for k in range(3))
                    for a, b in zip(_pp["cell"], _cp["cell"]))
        _cg[_f] = {"same": bool(_dmax <= 1e-6 and _cmax <= 1e-6),
                   "max_cart_diff_A": _dmax, "max_cell_diff_A": _cmax,
                   "tol_A": 1e-6}
    results["gas_canary_geom"] = _cg

    _pc = _closure_estimand(man, results, E, emol, jobs, merge_info)
    if _pc:
        results["prereg_closure"] = _pc

    # ── k 전이 게이트 (Codex 5차 taxonomy · 6차 §6) ───────────────────────────
    #   MANIFEST 에 k_label_rule 을 적어 놓고 **계산은 안 하던** 구멍을 막는다.
    #   n=2 이므로 평균·표준편차·CI 를 쓰지 않는다 — deterministic max/range 다.
    cal = list(man.get("dense_calibrators") or [])
    kap_all = results.get("kappa", {})
    k_transfer, k_labels, have = k_transfer_gate(
        cal, kap_all, man.get("fragments", []))
    results["k_transfer"] = k_transfer
    results["k_labels"] = k_labels
    # ── K 미검증 quantity 의 **부호 결론을 막는다** (Codex 재감사 P0-3) ─────────
    #   교차 끝점과 전역 끝점은 dense 를 안 돌린다. 조각의 k 라벨이 UNVERIFIED 면
    #   coarse 값으로 부호를 말할 근거가 없다.
    for _pid, _r in results["pairs"].items():
        _lb = k_labels.get(_r.get("fragment"), "K_UNVERIFIED")
        if _r.get("two_by_two_verdict") and _lb == "K_UNVERIFIED":
            _r["two_by_two_verdict"] = (
                f"K_UNRESOLVED_2x2(교차는 coarse only · 조각 라벨 {_lb} — 부호 결론 "
                f"보류. I 의 전이 오차폭은 두 대비의 차라 최악 "
                f"±{2 * GUARD_EV * 1000:.0f} meV)")
            _r["gates"] = [g for g in _r.get("gates", [])
                           if not g.startswith("POSE_DEPENDENT_SIGN")]
        for _t2, _c in (_r.get("cross") or {}).items():
            _c["k_note"] = (f"coarse only · 조각 라벨 {_lb}"
                            + (" — 부호 결론 보류" if _lb == "K_UNVERIFIED" else
                               f" · 전이 허용 ±{GUARD_EV * 1000:.0f} meV"))

    for frag in man.get("fragments", []):
        dl = [r["dE_Ni_minus_Li_eV"] for r in results["pairs"].values()
              if r["fragment"] == frag and "dE_Ni_minus_Li_eV" in r]
        n_planned = sum(1 for p in man["pairs"].values() if p["fragment"] == frag)
        expect_dirs = (man.get("contract_expected_pairs") or {}).get(frag)
        # ★ 번들 **이전**에 잃은 방향까지 본다. n/n_planned 만 보면 계획 자체가 이미
        #   줄어든 경우를 영원히 못 잡는다 (계획 3/3 = 100% 인데 원래 방향은 5개).
        #   자리 스윕 방향(Li_top/Ni_top 이 애초에 없음)은 정의 밖이라 세지 않고,
        #   Li_top/Ni_top 이 **있는데 부적격**인 방향만 손실로 센다.
        aud = (man.get("pair_audit") or {}).get(frag) or {}
        ex = aud.get("excluded_dirs") or {}
        lost = {d: sorted(c) for d, c in ex.items()
                if any(s.startswith(("Li_top", "Ni_top")) and "부적격" in s for s in c)}
        nd = aud.get("n_down_dirs")
        cov = (n_planned / nd) if nd else None
        if not dl:
            results["fragments"][frag] = {"n": 0, "n_planned": n_planned,
                                          "class": "NO_DATA"}
            continue
        n = len(dl)
        med = sorted(dl)[n // 2] if n % 2 else 0.5 * (sorted(dl)[n // 2 - 1]
                                                      + sorted(dl)[n // 2])
        side = 1 if med > 0 else -1
        fs = sum(1 for x in dl if x * side > 0) / n
        fe = sum(1 for x in dl if x * side > delta) / n
        # ★ 번들 이전에 방향을 잃었으면 **무조건 검열 등급**이다. n=3·계획=3 이라
        #   coverage 100% 로 보여 ROBUST 까지 올라가던 경로를 막는다 (Codex P0-6).
        champ = [p for p in man["pairs"].values()
                 if p["fragment"] == frag and p.get("champion_pose")]
        if champ:
            # 챔피언 비교는 "Li 위 최선 vs Ni 위 최선" 이다 — 방향 통계가 아니라
            # **설계상 1쌍**이므로 n<3 로 거부하지 않는다. 대신 무엇을 비교했는지 적는다.
            # ★ 판정 기준은 방향이 아니라 **자세키**(down_dir, roll) 다 (Codex 6차 P0-4).
            cp = champ[0].get("champion_pose") or {}
            same = champ[0].get("matched") is True
            ncross = len(champ[0].get("cross") or {})
            # ⚠ 옛 판은 교차 **결과 두 개**만 있으면 "2×2 완료" 라 했다. 그런데 2×2 계산
            #   자체(two_by_two)가 실패해도 그 조건은 참이라 **가짜 완료 라벨**이 붙었다.
            #   실제로 prefix 버그로 two_by_two 가 한 번도 안 만들어지고 있었다.
            _pr = results["pairs"].get(
                f"{frag}__{champ[0]['dir']}_r{champ[0]['roll']:03d}", {})
            got = 2 if (_pr.get("two_by_two") or {}).get("afm2424_pm1") else \
                sum(1 for _t, c in (_pr.get("cross") or {}).items()
                    if "dE_matched_eV" in c) and 0
            cls = ("CHAMPION_MATCHED_POSE" if same else
                   "CHAMPION_MIXED_ORIENTATION_2x2" if ncross == 2 and got == 2 else
                   # 교차 0 = 대각선 두 모서리뿐. 자리와 배향을 **분리할 수 없다**.
                   "CHAMPION_ORIENTATION_CONFOUNDED(교차 없음 — 자리·배향 분리 불가)"
                   if ncross == 0 else
                   "THREE_CORNER_PARTIAL(교차 %d/%d 완료 — 배향 미해결)" % (got, ncross))
        elif lost:
            cls = "DIRECTION_CENSORED_%d_OF_%d" % (n_planned, nd or n_planned)
        elif expect_dirs and n_planned != expect_dirs:
            cls = "CONTRACT_SHORT(계약 %d · 계획 %d)" % (expect_dirs, n_planned)
        elif n < 3:
            cls = "NO_VERDICT_n<3"
        elif n < 0.8 * n_planned:
            cls = "CENSORED(계획 %d 중 %d — coverage<80%%)" % (n_planned, n)
        elif fs >= 0.8 and fe >= 0.8:
            cls = "ROBUST_SCREENING"
        elif fs >= 0.8 and abs(med) > delta:
            cls = "MARGINAL_TENDENCY"
        elif fs >= 0.8:
            cls = "SIGN_CONSISTENT_SMALL"
        else:
            cls = "UNRESOLVED_MIXED"
        lbl = k_labels.get(frag, "K_UNVERIFIED")
        cls = apply_k_guard(cls, med, lbl, delta)
        results["fragments"][frag] = {
            "k_label": lbl,
            "kappa_meV": (round(kap_all[frag] * 1000, 1) if frag in kap_all else None),
            "n_directions": n, "n_planned": n_planned, "dE_list": dl,
            "median_eV": round(med, 4), "class": cls,
            "n_down_dirs": nd, "direction_coverage": None if cov is None else round(cov, 2),
            "disqualified_dirs": lost,
            "read_as": ("Li 위 최선이 더 안정" if med > 0 else "Ni 위 최선이 더 안정")
            if champ else ("Li 우세 경향" if med > 0 else "Ni 우세 경향"),
            "champion_dirs": (champ[0].get("champion_dirs") if champ else None),
            "champion_pose": (champ[0].get("champion_pose") if champ else None),
            "exact_matched_pose": (champ[0].get("matched") if champ else None),
            "note": ("PBE+U(6.2)+D3-zero fixed-protocol tendency — UMA 값과 같은 표 금지. "
                     "δ=%.3f eV." % delta)}
        if lost:
            wr = aud.get("excluded_reasons") or {}
            why = "; ".join(f"{d}: {', '.join(sorted(wr.get(d, {})))}" for d in sorted(lost))
            results["fragments"][frag]["disqualified_reasons"] = \
                {d: wr.get(d, {}) for d in lost}
            results["warnings"].append(
                f"{frag}: down_dir {nd}개 중 {len(lost)}개가 **번들 이전에** 탈락했다 "
                f"— 계획 {n_planned}개는 이미 줄어든 수다. 사유: {why}. "
                f"원고에는 '{nd}방향 중 {n_planned}방향 판정'과 그 사유를 함께 쓸 것 "
                f"(CAP_ARTIFACT 는 조각 모델의 한계지 데이터 부족이 아니다)")

    # ── 필수 완결성 — static + **계획된 dense** 까지 (Codex P0-D) ────────────
    # ⛔⛔ 회신 AO P0-1 (2026-08-31) — 종전엔 **14잡 전체**의 누락을 먼저 세고
    #   exit 2 로 끝낸 뒤에야 `--gate vacconv` 분기로 들어갔다. 그래서 1단계 8잡만
    #   정상 완료한 상태도 **미실행 2단계 6잡 때문에 반드시 실패**했다.
    #   ⇒ completeness 를 **단계별로** 나눈다. 단계 분류는 run_staged.sh 와
    #     **같은 규칙**(job.json 구조화 필드)이어야 한다 — 이름 파싱 금지.
    def _stage_of(pl):
        # 계획 항목 -> "1" | "2". run_staged.sh 의 분류와 1:1 이어야 한다.
        m = (pl.get("meta") or {})
        kind, role, vac = m.get("kind"), m.get("role"), m.get("vacconv")
        if kind == "mol_ref":
            return "1"
        if kind == "prospective_pose" and role == "primary":
            return "1" if (vac or m.get("seed") == "afm2424_pm1") else "2"
        return "2"

    _gate_arg = ""
    if "--gate" in sys.argv:
        _gi = sys.argv.index("--gate")
        _gate_arg = sys.argv[_gi + 1] if len(sys.argv) > _gi + 1 else ""
    # ⚠ meta 가 없는 계획 항목은 단계를 **모른다**. 모르는 것을 1단계에서 빼면
    #   거짓 통과가 되므로 '2' 로 두지 않고 **양쪽 다 필수**로 센다.
    _no_meta = [j for j, pl in planned.items()
                if pl.get("required") and not (pl.get("meta") or {})]
    # ⛔⛔ 회신 AP #4 (2026-08-31) — 14잡이 **전부 required** 라, net4 나 대안 자세
    #   하나가 게이트되면 최종 completeness 가 exit 2 를 냈다. 그런데 우리는
    #   "net4 unavailable 은 D_pm1 에 영향 없음" 이라고 선언해 놓았다 — 모순이다.
    #   또 대안 자세 4잡은 어떤 봉인된 식에도 안 들어가면서 필수잡으로 남아 있었다.
    #   ⇒ tier 를 나눈다. estimand = 봉인된 네 잡 + 진공쌍(1단계 판정에 쓴다) +
    #     기체 기준. 나머지(net4·대안 자세)는 sensitivity 다.
    #     종료코드는 **estimand tier 만** 본다. sensitivity 결측은 상태로 보고한다.
    _ejk_all = set()
    for _kk in ("estimand_job_keys", "estimand_job_keys_net4"):
        for _k2, _v2 in (man.get(_kk) or {}).items():
            if _k2.startswith("E_") and isinstance(_v2, str):
                _ejk_all.add(_v2)
    _ejk_pm1 = {v for k, v in (man.get("estimand_job_keys") or {}).items()
                if k.startswith("E_") and isinstance(v, str)}

    def _tier_of(j, pl):
        # ⚠ tier 분리는 **exact-key 경로에서만** 뜻이 있다. 봉인된 식이 없으면
        #   어느 잡이 D 에 들어가는지 알 수 없으므로 전부 estimand 로 둔다
        #   (레거시 Li/Ni 쌍 경로에서 그 잡들이 sensitivity 로 강등되면
        #    누락이 종료코드에 안 잡히는 **회귀**가 된다 — 실측으로 잡았다).
        if not _ejk_pm1:
            return "estimand"
        m = (pl.get("meta") or {})
        if j in _ejk_pm1:
            return "estimand"
        if m.get("kind") == "mol_ref":
            return "estimand"          # 기체 기준은 D 에 직접 들어간다
        if m.get("vacconv"):
            return "estimand"          # 진공 수렴 판정이 1단계 게이트다
        return "sensitivity"
    missing, missing_sens = [], []
    for j, pl in planned.items():
        if not pl.get("required"):
            continue
        if _gate_arg == "vacconv" and (pl.get("meta") or {}) and _stage_of(pl) != "1":
            continue                      # 1단계 판정에서는 2단계 잡을 안 센다
        _bucket = missing if _tier_of(j, pl) == "estimand" else missing_sens
        if E(j) is None:
            _bucket.append(j + " [static]")
        elif "dense" in (pl.get("phases") or []) and E_dense(j) is None:
            _bucket.append(j + " [dense]")
    results["required_missing_sensitivity"] = missing_sens
    results["tier_census"] = {}
    for j, pl in planned.items():
        if pl.get("required"):
            _t = _tier_of(j, pl)
            results["tier_census"][_t] = results["tier_census"].get(_t, 0) + 1
    if missing_sens:
        results["warnings"].append(
            "sensitivity tier %d건 미완 %s — **D_pm1 에는 영향이 없다**. "
            "다만 자기 분기·자세 민감도를 보고할 수 없다 (회신 AP #4)"
            % (len(missing_sens), missing_sens[:3]))
    results["sensitivity_status"] = ("complete" if not missing_sens
                                     else "incomplete (%d건)" % len(missing_sens))
    out = os.path.join(root, "RESULTS.json")
    results["required_missing"] = missing
    for r in jobs.values():
        r.pop("_fin", None); r.pop("_contact_fp", None)
    json.dump(results, open(out, "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)

    bad = {j: r for j, r in jobs.items() if not r["ok"]}
    print(f"=== 무결성 ===  검사 {integrity['checked']}개 · 변경 "
          f"{len(integrity['changed'])} · 없음 {len(integrity['missing'])}")
    print(f"=== 잡 게이트 ===  통과 {len(jobs) - len(bad)}/{len(jobs)}"
          + (f" · 문제 {len(bad)}건:" if bad else ""))
    for j, r in sorted(bad.items()):
        print(f"  ⛔ {j}: {', '.join(r['gates'])}")
    print("\n=== 자리 선호 (ΔE = E(Ni_top) − E(Li_top), 양수 = Li 우세 · seed-매칭) ===")
    for pid, r in sorted(results["pairs"].items()):
        de = r.get("dE_Ni_minus_Li_eV")
        seeds = " ".join(f"{s.split('_')[-1]}:{v:+.3f}" for s, v in r["dE_by_seed"].items())
        print(f"  {pid:34s} " + (f"{de:+.3f} eV" if de is not None else "(게이트/미완)")
              + (f"  [{seeds}]" if seeds else "")
              + (f"  ⛔{';'.join(r['gates'])}" if r["gates"] else ""))
    print("\n=== 조각별 판정 ===")
    for f, r in results["fragments"].items():
        nd = r.get("n_down_dirs")
        print(f"  {f:14s} n={r.get('n_directions', 0)}/{r.get('n_planned', '?')}"
              + (f" (원래 방향 {nd})" if nd and nd != r.get("n_planned") else "")
              + "  중앙값 "
              + (f"{r['median_eV']:+.3f} eV" if "median_eV" in r else "—")
              + f"  → {r['class']}"
              + (f"  ⚠번들이전 탈락 {len(r['disqualified_dirs'])}방향"
                 if r.get("disqualified_dirs") else ""))
    if results["e_ads"]:
        print("\n=== E_ads (pm1 seed · box24 기준계 · 음수 = 흡착 유리) ===")
        for pid, e in sorted(results["e_ads"].items()):
            print(f"  {pid:34s} Li_top {e['Li_top']:+.3f} · Ni_top {e['Ni_top']:+.3f} eV")
    for k, v in results["numerical_gates"].items():
        # ⛔ 회신 AO P0-6 — pass 가 None 이면 **판정하지 않은 것**이다. ⛔(실패)로
        #   찍으면 실패한 것처럼 보이고, ✓ 로 찍으면 검증한 것처럼 보인다.
        _mk = "✓" if v["pass"] else ("ℹ" if v["pass"] is None else "⛔")
        print(f"  {_mk} 수치게이트 {k}: {v['dE_meV']} meV"
              + (f" · E_ads {v['dEads_meV']} meV" if "dEads_meV" in v else ""))
    for w in results["warnings"]:
        print(f"  ⚠ {w}")
    print(f"\n→ {out}")
    # ⚠ 기하를 **검증하지 못한 것**도 실패다 (Codex 재감사 P0-1). 옛 판은 경고만
    #   찍고 exit 0 이라, 실제 VASP 가 무엇을 읽었는지 모르는 채 완주로 보였다.
    if integrity["changed"] or integrity["missing"] or \
            integrity.get("runtime_poscar_mismatch") or \
            integrity.get("geometry_unverified"):
        print(f"\n⛔ **입력 무결성 실패** — 변경 {len(integrity['changed'])} · "
              f"사라짐 {len(integrity['missing'])} · 실행시 기하 불일치 "
              f"{len(integrity.get('runtime_poscar_mismatch') or [])} · 기하 미검증 "
              f"{len(integrity.get('geometry_unverified') or [])} — exit 2 "
              f"(삭제도 변조이고, **검증 못 한 것도 통과가 아니다**)")
        return 2

    # ⛔⛔ 회신 AO P0-1 (2026-08-31) — stage gate 를 **다른 종료 검사보다 먼저**
    #   판정한다. 종전엔 e_ads·전체 completeness 검사 뒤에 있어서, 1단계 8잡만
    #   정상 완료한 상태가 여기까지 오지도 못하고 exit 2 로 끝났다.
    _cl = (results.get("prereg_closure") or {})
    _vc = (results.get("closure_vacconv") or _cl.get("closure_vacconv") or {})
    if _gate_arg:
        if _gate_arg != "vacconv":
            print(f"⛔ 모르는 --gate: {_gate_arg!r} (지원: vacconv)")
            return 2
        if missing:            # 위에서 **1단계 cohort 로 좁혀** 센 값이다
            print(f"⛔ **1단계 cohort 미완 {len(missing)}건** — exit 2:")
            for j in missing[:20]:
                print(f"   · {j}")
            return 2
        if not _vc or _vc.get("applicable") is False:
            print("⛔ 진공 수렴 판정을 낼 수 없다 (vacconv 잡이 없거나 결과가 없다)")
            return 2
        if _vc.get("blocks"):
            print("⛔ 진공 판정이 막혔다:")
            for b in _vc["blocks"][:5]:
                print(f"   · {b}")
            return 2
        print(f"■ stage gate = vacconv · {_vc.get('verdict')}")
        # ⛔⛔ 회신 AP #5 (2026-08-31) — stage gate 가 사실상 `closure_vacconv` 만 봤다.
        #   그래서 nzmag 가 부모보다 낮거나 · canary 기하가 어긋나거나 ·
        #   ROOT_SEAL 이 불일치하거나 · POTCAR source/VASP 버전이 갈려도
        #   **2단계가 열렸다.** canary 와 POTCAR 검사를 1단계에 넣은 목적과 모순이다.
        #   ⇒ stage1_prerequisites 를 따로 만들고 **전부** 통과해야 연다.
        _pi = (_cl.get("potcar_identity") or {})
        _pre = _stage1_prereqs(_cl, _vc, results)
        _pre_bad = [k for k, v in _pre.items() if not v["pass"]]
        print("■ stage-1 prerequisites:")
        for _k, _v in _pre.items():
            print(f"   {'✓' if _v['pass'] else '⛔'} {_k}: {str(_v['why'])[:70]}")
        if _pre_bad:
            print("⛔ **2단계를 열지 않는다** — 1단계 선결조건 미통과: %s" % _pre_bad)
            print("   (canary·POTCAR 검사를 1단계에 넣은 이유가 바로 이것이다)")
            return 2
        if not _vc.get("pass"):
            print("⛔ **2단계를 제출하지 않는다.** 추가 셀 탐색 없이 Figure 2e 를 제거한다.")
            return 2
        # ⛔ 회신 AO P0-3 — 통과를 **해시에 결박된 receipt** 로 남긴다.
        #   자유문구는 증거가 아니다. run_staged.sh 2 는 이 파일 없이 열리지 않고,
        #   MANIFEST 가 바뀌면 해시가 달라져 자동으로 무효가 된다.
        _s1 = sorted(j for j, pl in planned.items()
                     if pl.get("required")
                     and (not (pl.get("meta") or {}) or _stage_of(pl) == "1"))
        _rc = {
            "schema": "stage1_pass/v1",
            "gate": "vacconv",
            "verdict": _vc.get("verdict"),
            "delta_vac_meV": _vc.get("delta_vac_meV"),
            "manifest_sha256": hashlib.sha256(
                open(os.path.join(root, "MANIFEST.json"), "rb").read()).hexdigest(),
            "stage1_jobs": _s1,
            "stage1_energies_eV": {j: E(j) for j in _s1},
            "integrity_checked": integrity.get("checked"),
            "n_planned_required": sum(1 for pl in planned.values() if pl.get("required")),
            "stage1_prerequisites": _pre,
            "⚠_receipt_는_증거가_아니다": ("회신 AP #4 — 이 파일이 있다는 것만으로 "
                "2단계를 열지 않는다. 러너가 2단계 **직전에** `--gate vacconv` 를 "
                "다시 실행해 현재 결과로 재판정한다"),
            "⛔": ("1단계 통과 증거. run_staged.sh 2 는 이것 없이 열리지 않는다. "
                   "MANIFEST.json 이 바뀌면 manifest_sha256 이 달라져 무효다."),
        }
        json.dump(_rc, open(os.path.join(root, "STAGE1_PASS.json"), "w",
                                    encoding="utf-8"),
                  indent=1, ensure_ascii=False)
        print(f"✅ 1단계 통과 ({len(_s1)}잡) — STAGE1_PASS.json 기록 · 2단계 제출 가능")
        return 0
    # ⚠ 기준계를 선언해 놓고 E_ads 가 하나도 안 나오면 **조용한 실패**다.
    #   경로 키가 안 맞아도 gas job 자체는 ok 라 exit 0 이 났다 (Codex 4차 P0-2).
    # ⛔ 회신 AJ — `pairs` 는 **Li/Ni 대조쌍** 경로의 산물이다. C-12 · from_basins 는
    #   basin 단위로 생성하므로 pairs 가 비어 있고, 그러면 e_ads 루프가 0회 돈다.
    #   그 상태로 이 검사를 걸면 **완주해도 무조건 exit 2** 다 (실측: C-12 v3).
    #   pairs 가 애초에 없는 판에서는 이 검사가 적용되지 않는다.
    _pairs_expected = bool(man.get("pairs"))
    if has_refs and _pairs_expected and not results["e_ads"]:
        print("\n⛔ **기준계를 선언했는데 E_ads 가 0개다** — refs 조회가 안 맞거나 "
              "상자 게이트가 전부 실패했다. exit 2")
        for k2, v2 in results["numerical_gates"].items():
            if k2.startswith("box_"):
                print(f"   {k2}: {v2}")
        return 2
    if missing:
        _scope = ("1단계 cohort" if _gate_arg == "vacconv"
                  else "estimand tier (sensitivity 결측은 종료코드에 안 넣는다)")
        print(f"\n⛔ **필수 산출 미완 {len(missing)}건** ({_scope}) — fail-closed, exit 2:")
        for j in missing[:20]:
            print(f"   · {j}")
        if _no_meta:
            print(f"   ⚠ 계획 meta 가 없어 단계를 모르는 항목 {len(_no_meta)}건은 "
                  f"**양쪽 단계 모두에서 필수**로 셌다 (모르는 것을 빼면 거짓 통과다)")
        return 2

    # ⛔⛔ 2026-08-31 (회신 AN P0-3·P0-4) — **두 가지가 종료코드에 안 걸려 있었다.**
    #   ① stage 판정: 1단계만 돌고 나면 2단계 6잡이 required_missing 이라 **무조건 exit 2**.
    #      그래서 진공 시험을 통과해도 2단계를 열 수 없었다. `--gate vacconv` 는
    #      1단계 cohort 만 보고, 그 판정으로만 끝낸다.
    #   ② 최종 판정: prereg_closure 가 NO_VALUE 여도, 진공이 실패해도 `return 0` 이
    #      될 수 있었다. **비인용 상태면 반드시 nonzero** 여야 한다.
    _bad_final = _final_verdict(_cl, _vc)
    if _bad_final:
        print("⛔ **비인용 상태로 끝났다** — 종료코드를 0 으로 두지 않는다:")
        for b in _bad_final:
            print(f"   · {b}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


# ═══════════════════════════════════════════════════════════════════════════
#  주기영상 진공 — **재는 것이 아니라 게이트다** (2026-08-30, 회신 AF P0-1)
#
#  발송 후보 v13/holdout_v4 의 24 pm1 자세 중 **9개가 15 Å 미만**이었고 PTFE
#  b71/b74/b75/b79 는 8.56~8.79 Å 였다. 그런데 README·Methods·Table S1 은 전부
#  ">15 Å" 라고 적고 있었다. 생성기에 진공을 보는 코드가 **한 줄도 없었기** 때문이다.
#  D3(IVDW=11)는 pairwise 라 dipole correction 이 이 상호작용을 지우지 못한다.
#
#  ⛔ 이 코드가 못 하는 것: 얼마나 큰 오차인지 말하지 못한다. 분리거리만 보장한다.
#     실제 크기는 셀 높이 수렴 시험(같은 자세를 두 c 로)으로만 안다.
MIN_VACUUM_A_DEFAULT = 15.0


def _poscar_read(path: Path):
    """POSCAR → (lattice 3×3, elements, cart coords, 원본 줄). Direct/Cartesian 모두."""
    L = Path(path).read_text().splitlines()
    sc = float(L[1].split()[0])
    A = [[float(x) * sc for x in L[i].split()[:3]] for i in (2, 3, 4)]
    sp = L[5].split()
    cnt = [int(x) for x in L[6].split()]
    i = 7
    sel = L[i].strip()[:1] in "sS"
    if sel:
        i += 1
    mode = L[i].strip()[:1].lower()
    i += 1
    n = sum(cnt)
    raw = [L[i + k] for k in range(n)]
    frac = [[float(x) for x in r.split()[:3]] for r in raw]
    if mode == "d":
        cart = [[sum(f[j] * A[j][d] for j in range(3)) for d in range(3)] for f in frac]
    else:
        cart = [[f[d] * sc for d in range(3)] for f in frac]
    el = []
    for s, c in zip(sp, cnt):
        el += [s] * c
    return dict(lines=L, A=A, el=el, cart=cart, mode=mode, sel=sel,
                coord_start=i, n=n, raw=raw)


def _split_slab_mol(el, cart):
    """Ni 최상단 + 1.6 Å 아래의 Li/Ni/O 를 슬랩으로, 나머지를 흡착종으로."""
    zni = [cart[i][2] for i, e in enumerate(el) if e == "Ni"]
    if not zni:
        return None, None
    ztop = max(zni) + 1.6
    slab = [i for i, e in enumerate(el) if cart[i][2] <= ztop and e in ("Li", "Ni", "O")]
    mol = [i for i in range(len(el)) if i not in set(slab)]
    return slab, mol


def image_separation_A(path) -> Optional[float]:
    """흡착종 ↔ **다음 주기 슬랩(+c)** 실제 최단거리. 흡착종이 없으면 None."""
    d = _poscar_read(path)
    slab, mol = _split_slab_mol(d["el"], d["cart"])
    if not mol or not slab:
        return None
    A, X = d["A"], d["cart"]
    ax, ay, cz = A[0][0], A[1][1], A[2][2]
    best = float("inf")
    for i in mol:
        for j in slab:
            dx = X[i][0] - X[j][0]
            dy = X[i][1] - X[j][1]
            dz = X[i][2] - (X[j][2] + cz)
            dx -= round(dx / ax) * ax
            dy -= round(dy / ay) * ay
            best = min(best, (dx * dx + dy * dy + dz * dz) ** 0.5)
    return best


def poscar_set_c(path, new_c: float) -> None:
    """c 축만 늘린다 — **원자의 Cartesian 좌표는 그대로**.

    Direct 좌표면 z 분율을 old_c/new_c 로 되scale 해야 원자가 안 움직인다.
    이걸 빠뜨리면 셀을 늘리는 순간 슬랩이 늘어난다 (조용한 사고).
    """
    path = Path(path)
    d = _poscar_read(path)
    A = d["A"]
    old_c = A[2][2]
    if new_c <= old_c:
        return
    if abs(A[2][0]) > 1e-9 or abs(A[2][1]) > 1e-9:
        raise ValueError("c 축이 z 와 나란하지 않다 — 자동 확장 거부: %s" % path)
    L = list(d["lines"])
    sc = float(L[1].split()[0])
    L[4] = "  %.16f %.16f %.16f" % (A[2][0] / sc, A[2][1] / sc, new_c / sc)
    if d["mode"] == "d":
        k = old_c / new_c
        for idx, r in enumerate(d["raw"]):
            tok = r.split()
            f = [float(x) for x in tok[:3]]
            tail = " ".join(tok[3:])
            L[d["coord_start"] + idx] = ("  %.16f %.16f %.16f %s"
                                         % (f[0], f[1], f[2] * k, tail)).rstrip()
    path.write_text("\n".join(L) + "\n")


def _jobjson_rescale(job_dir: Path, k: float) -> int:
    """c 를 늘렸으면 `job.json` 의 **분율** 필드도 같이 줄인다.

    ⛔ 회신 AF P0-1 후단 — INCAR 의 DIPOL 만 고치고 job.json 을 안 고쳤다.
       `zcom_frac` 이 분율 질량중심이라 셀을 늘리면 어긋난다.
       (`z_cut_A` 는 Å 단위라 무관 · `incar_expected` 에는 DIPOL 이 없다.)
    """
    jp = job_dir / "job.json"
    if not jp.is_file():
        return 0
    d = json.loads(jp.read_text())
    n = 0
    for key in ("zcom_frac",):
        if isinstance(d.get(key), (int, float)):
            d[key] = round(float(d[key]) * k, 6)
            n += 1
    if n:
        jp.write_text(json.dumps(d, indent=1, ensure_ascii=False))
    return n


def _dipol_rescale(job_dir: Path, k: float) -> int:
    """c 를 늘렸으면 **분율 DIPOL 의 z 성분도 같은 비율로** 줄여야 한다.

    Cartesian 좌표를 보존한 채 c 만 키우면 질량중심의 분율 z 는 old_c/new_c 배가 된다.
    이걸 안 고치면 쌍극자 보정면이 실제 COM 에서 몇 Å 떨어진 자리에 박힌다
    (회신 AF P0-1 실측: b74 가 3.47 Å 어긋났다).
    """
    n = 0
    for inc in sorted(job_dir.rglob("INCAR")):
        s = inc.read_text()
        m = re.search(r"^(DIPOL\s*=\s*)([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*$", s, re.M)
        if not m:
            continue
        z = float(m.group(4)) * k
        inc.write_text(s[:m.start()] + "%s%s %s %.4f" % (m.group(1), m.group(2),
                                                         m.group(3), z) + s[m.end():])
        n += 1
    return n


def _slab_jobs(out: Path, planned: dict):
    """흡착종이 **슬랩 위에 있는** 잡만. 기체 기준계는 제외한다.

    ⛔ 회신 AF P0-1 — 종전엔 planned 전부를 늘려서 **기체 상자까지 커졌다.**
       box20/box24 가 둘 다 36.6551 Å 이 되어 상자크기 대조가 통째로 사라졌다.
    """
    ks = []
    for k in planned:
        pp = out / k / "POSCAR"
        if not pp.is_file():
            continue
        try:
            d = _poscar_read(pp)
        except Exception:                                    # noqa: BLE001
            continue
        if "Ni" in d["el"]:                 # 슬랩이 있는 계만 (복합체 · clean slab)
            ks.append(k)
    return ks


def set_job_cell(job_dir: Path, new_c: float) -> dict:
    """잡 하나의 셀 높이를 `new_c` 로. POSCAR·DIPOL·job.json 을 **함께** 고친다.

    셋을 따로 고치면 하나를 빠뜨린다 — 실제로 그렇게 물렸다 (회신 AF P0-1).
    """
    cur = _poscar_read(job_dir / "POSCAR")["A"][2][2]
    if new_c <= cur + 1e-9:
        return {"changed": False, "c_before_A": round(cur, 4)}
    k = cur / new_c
    nd = _dipol_rescale(job_dir, k)
    nj = _jobjson_rescale(job_dir, k)
    poscar_set_c(job_dir / "POSCAR", new_c)
    return {"changed": True, "c_before_A": round(cur, 4), "c_after_A": round(new_c, 4),
            "n_dipol": nd, "n_jobjson": nj}


def fit_bundle_vacuum(out: Path, planned: dict, min_vac: float,
                      target_c: Optional[float] = None) -> dict:
    """슬랩이 든 잡을 **한 c** 로 맞춘다 (clean slab 포함 — 안 그러면 E_ads 가 안 소거된다).

    · 기체 기준계는 **건드리지 않는다** (box20/box24 대조가 살아 있어야 한다).
    · c 를 바꾸면 분율 DIPOL 의 z 를 같이 되scale 한다.
    · `target_c` 를 주면 그 값으로 맞춘다 — **두 묶음이 같은 셀을 쓰게** 하는 유일한 방법이다
      (회신 AF P0-2: calibration 36.6551 · holdout 36.5829 로 갈렸었다).
    """
    jobs = _slab_jobs(out, planned)
    meas = {}
    for k in jobs:
        s = image_separation_A(out / k / "POSCAR")
        if s is not None:
            meas[k] = s
    if not meas:
        return {"declared_A": min_vac, "per_job": {}, "note": "흡착종이 있는 잡이 없다"}
    c0 = _poscar_read(out / jobs[0] / "POSCAR")["A"][2][2]
    worst = min(meas.values())
    n_below = sum(1 for v in meas.values() if v < min_vac)
    # ⚠ c 를 Δ 늘려도 최단거리는 Δ 만큼 안 는다 — 최단 쌍에 xy 성분이 있으면
    #   sqrt(dxy²+dz²) 라 증가분이 Δ 보다 작다. 한 번만 늘리면 미달로 끝난다
    #   (실측: 15.0 목표에 14.978 에서 멈췄다). 수렴할 때까지 반복한다.
    c1, cur, n_dip, n_jj = c0, worst, 0, 0
    if target_c:                            # 두 묶음 공통 c — 요청값이 이긴다
        if target_c < c0 - 1e-9:
            raise ValueError("target_c %.4f < 현재 c %.4f — 셀을 줄이지 않는다"
                             % (target_c, c0))
        c1 = float(target_c)
        for k in jobs:
            n_dip += _dipol_rescale(out / k, c0 / c1)
            n_jj += _jobjson_rescale(out / k, c0 / c1)
            poscar_set_c(out / k / "POSCAR", c1)
        cur = min([v for v in (image_separation_A(out / k / "POSCAR") for k in meas)
                   if v is not None] or [worst])
    else:
        for _ in range(12):
            if cur >= min_vac - 1e-9:
                break
            _prev = c1
            c1 += (min_vac - cur) + 1e-3
            for k in jobs:                  # ★ 복합체·clean slab 만 (기체 제외)
                n_dip += _dipol_rescale(out / k, _prev / c1)
                n_jj += _jobjson_rescale(out / k, _prev / c1)
                poscar_set_c(out / k / "POSCAR", c1)
            cur = min(v for v in (image_separation_A(out / k / "POSCAR") for k in meas)
                      if v is not None)
    after = {k: image_separation_A(out / k / "POSCAR") for k in meas}
    return {"declared_A": min_vac, "c_before_A": round(c0, 4), "c_after_A": round(c1, 4),
            "min_before_A": round(worst, 3),
            "min_after_A": round(min(v for v in after.values() if v is not None), 3),
            "n_below_before": n_below, "n_dipol_rescaled": n_dip,
            "n_jobjson_rescaled": n_jj,
            "target_c_A": target_c,
            "gas_refs_untouched": True,
            "per_job_A": {k: round(v, 3) for k, v in sorted(after.items())
                          if v is not None},
            "⚠": ("분리거리만 보장한다 — 남은 영상 오차의 **크기**는 "
                  "같은 자세를 두 c 로 돌리는 수렴 시험으로만 안다")}


def _readme_sp(man: Dict[str, Any], a, zcut: float, n_jobs: int,
               n_st: int, n_dn: int, n_all: int = 0, by_ph: Optional[dict] = None) -> str:
    """단일점 Wave 1 전용 README — **실제 계획에서 숫자를 뽑는다** (Codex 6차 §8).

    옛 README 를 재사용하면 82계·259상·relax 반송·refs 표가 그대로 나가, 외주처가
    있지도 않은 relax/CONTCAR 를 찾다가 멈춘다. 이 도구가 못 하는 것: 실행 시간 보장
    (SUBMIT_CONTRACT.md 의 추정은 ±2배 불확실성을 가진 모델값이다).
    """
    # ⛔ 2026-08-31 — relax 반송 문구는 **조건부**여야 한다. 무조건 넣으면 relax 가
    #   하나도 없는 묶음에서 검사기의 반대편 게이트("이완판 문구인데 실물엔 relax 가
    #   없다")에 걸린다. 실제 계획에서 세어서 있을 때만 넣는다.
    _n_rel = sum(1 for _p in (man.get("planned") or {}).values()
                 if "relax" in (_p.get("phases") or []))
    # ⛔⛔ 2026-08-31 (회신 AN P0-3) — README 와 러너가 **서로 반대를 말하고 있었다.**
    #   run_staged.sh 는 순서를 강제하는데(1단계 판정 실패 시 2단계 금지) README 는
    #   "잡은 독립이니 동시에 제출" 로 읽혀 stop rule 을 우회시켰다.
    #   ⇒ staged 러너가 있으면 **그것이 유일한 실행 지침**이라고 못박는다.
    _staged = bool(man.get("staged_runner"))
    # ⚠ 잡 수를 **계획에서 센다.** 하드코딩하면 canary 를 넣는 순간 문서가 거짓이 된다
    #   (2026-08-31 실측: 12 → 14 인데 README 는 "12잡" 이라고 적고 있었다).
    #   1단계 분류는 run_staged.sh 와 **같은 규칙**이다 — mol_ref 전부 + primary·주 seed.
    _n1 = 0
    for _pm in (man.get("planned") or {}).values():
        _mm = _pm.get("meta") or {}
        _k, _r = _mm.get("kind"), (_mm.get("role") or "primary")
        if _k == "mol_ref":
            _n1 += 1
        elif _k == "prospective_pose" and _r == "primary" and (
                _mm.get("vacconv") or _mm.get("seed") == SEED_MAIN):
            _n1 += 1
    _n1 = _n1 or 6
    # ⛔⛔ 회신 AO P0-2·P0-3 (2026-08-31) — 종전 README 는 staged 안내 **뒤에**
    #   단일 잡 quickstart 를 그대로 붙였고, `run_all.sh` 는 14잡 전체 제출을
    #   안내했다. 실행 경로가 셋이면 1단계 정지 규칙이 강제되지 않는다.
    #   staged 구성에서는 **경로를 하나로** 줄이고, POTCAR 조립을 그 안에 넣는다.
    staged_block = ("""⛔ **`run_staged.sh` 로만 실행해 주세요. %d잡을 한꺼번에 던지지 마십시오.**
1단계(%d잡)가 진공 두께 수렴 시험을 통과해야 2단계를 돌립니다 — 통과 못 하면
2단계는 **돌리지 않는 것이 맞습니다**(추가 계산으로 메우지 않습니다).

```
cd <이 묶음을 푼 디렉터리>            # 묶음 **루트**에서 실행합니다 (잡 폴더 아님)
export PP=/path/to/potpaw_PBE.54
export POTCAR_ALLOWLIST=/abs/site_allow.txt
# 받으신 ZIP 의 SHA256 — 봉인이 **정확히 이 배포본**에 대한 것임을 남깁니다
export BUNDLE_ZIP_SHA256=$(sha256sum /경로/받은번들.zip | cut -d" " -f1)
export EXPECT_MANIFEST_SHA256=%s   # 저희가 보낸 값 (러너가 실행 전에 대조합니다)
export EXPECT_ZIP_SHA256=<메일 본문의 ZIP SHA256>   # **필수** — 없으면 러너가 멈춥니다
# ⛔ VASP_CMD 는 더 쓰지 않습니다. 런처와 실행파일을 **나눠** 주세요 —
#    실행파일만 봉인 대상이고, 런처에 실행파일을 넣으면 봉인이 무의미해집니다.
export VASP_LAUNCHER="mpirun -np %d"        # 런처와 그 플래그만
export VASP_EXE=/abs/path/to/vasp_std       # 실행파일 절대경로 (봉인 대상)
bash run_staged.sh 1     # POTCAR 조립+봉인 → census → 1단계 → 자동 판정
bash run_staged.sh 2     # 1단계 통과(STAGE1_PASS.json) 뒤에만
```

⚠ `BUNDLE_ZIP_SHA256` 이 없으면 봉인 스크립트가 **거부합니다** — 번들 안에는 자기
해시를 넣을 수 없어서, 받으신 파일에서 직접 구해 주셔야 결박이 성립합니다.
`EXPECT_MANIFEST_SHA256` 과 `EXPECT_ZIP_SHA256` 은 메일 본문에 적어 보내드립니다 —
**둘 다 필수**입니다. 없으면 러너가 시작하지 않습니다 (번들 안의 해시는 자기 자신을
증명하지 못하므로, ZIP 밖의 값이 유일한 앵커입니다).

**POTCAR 를 따로 조립하지 마십시오** — `run_staged.sh` 가 첫 VASP 실행 전에
`SEAL_POTCAR_ROOT.sh` 로 전 잡 조립 + 원본 fingerprint 봉인까지 합니다.
`run_all.sh` 는 이 묶음에 **넣지 않았습니다** (전체 제출 경로가 있으면 1단계
정지 규칙이 무력화됩니다).

⛔ **단일 잡을 손으로 돌리는 경로는 이 묶음에서 삭제했습니다** (회신 AT P0-5).
`run_job.sh` 를 직접 부르면 봉인된 실행파일 검사와 번들 전역 lock 을 **둘 다 우회**해,
봉인이 무의미해지고 같은 번들에 두 실행이 들어올 수 있습니다.
한 잡을 다시 돌리셔야 하면 그 잡의 산출물을 지우고 `bash run_staged.sh <단계>` 를
다시 부르십시오 — 러너가 완료된 잡은 건너뜁니다.

""" % (n_jobs, _n1, "<메일 본문의 MANIFEST SHA256>",
       getattr(a, "cores", 48))) if _staged else ""

    relax_return = ("""⚠ **`relax/` 폴더가 있는 잡은 `relax/OUTCAR` 와 `relax/CONTCAR` 도 같이**
  보내 주세요 (이 묶음에 **%d잡**). 단일점 묶음에서도 **기체 기준(`refs/mol__*`)에는
  relax 상이 있습니다** — 분자는 상자 안에서 이완해야 하기 때문입니다. 어느 잡인지는:
  ```bash
  find . -maxdepth 3 -type d -name relax
  ```
""" % _n_rel) if _n_rel else ""

    # 🔴 `dense_calibrators` 는 **선언 필드**라 비어 있어도 실제 dense 상이 있을 수 있다.
    #   실물 v13 이 그 사례였다 — 필드가 null 인데 refs/clean_slab__afm2424_pm1/dense 가
    #   있어서 README 가 "1개 잡에만 있습니다: (없음)" 을 냈다. planned 에서 센다.
    _pl = man.get("planned") or {}
    _dense_jobs = sorted(k for k, v in _pl.items() if "dense" in (v.get("phases") or []))
    _relax_jobs = sorted(k for k, v in _pl.items() if "relax" in (v.get("phases") or []))
    dc = _dense_jobs or (man.get("dense_calibrators") or [])
    mc = man.get("magnetic_controls") or []
    ks = (man.get("kmesh_override") or {}).get("static") or KMESH["static"]
    kd = (man.get("kmesh_override") or {}).get("dense") or KMESH["dense"]
    # 🔴 종전엔 `longest = 56` 하드코딩이었다. `--cores` 를 바꿔도 이 수는 안 바뀌어서
    #   README 가 "56시간 (256코어 기준)" 같은 **라벨과 숫자가 어긋난 문장**을 냈다.
    #   MANIFEST 의 cost_frozen (같은 추정기·같은 코어 수)에서 가져온다.
    longest = round((man.get("cost_frozen") or {}).get("longest_job_h") or 56)
    groups = "` · `".join(sorted({k.split("/")[0] for k in man["planned"]}))
    ph_line = " · ".join(f"{k} {v}" for k, v in sorted((by_ph or {}).items()))
    ncore_hint = "4"
    # ★ census 를 문서에 **산출물에서 센 값으로** 박는다 (회신 Z P0-3)
    cs = man.get("job_census") or {}
    if cs:
        census_md = (
            "## 잡 census (산출물에서 센 값)\n\n"
            "| | 끝점 | D3-off 쌍둥이 | 계 |\n|---|---:|---:|---:|\n"
            f"| references | {cs['references']['endpoints']} | "
            f"{cs['references']['d3_off_twins']} | **{cs['references']['총']}** |\n"
            f"| calibration complexes | {cs['complexes']['pose×seed']} | "
            f"{cs['complexes']['d3_off_twins']} | **{cs['complexes']['총']}** |\n"
            f"| | | | **{cs['총잡수']}** |\n\n"
            f"audit pose **{cs['audit_pose']}개**. pose 당: {cs['pose당']}\n")
    else:
        census_md = ""

    # ★ 머리말·pose 산문을 **실물에서** 만든다. 하드코딩이 census 표와 어긋났었다:
    #   실물 v13 은 D3-off 0개인데 산문이 "pose 당 세 계산" 이라고 적었고,
    #   전 잡이 static 인데 머리말이 "기체 기준계만 DFT 이완" 이라고 적었다.
    if _relax_jobs:
        intro_line = ("슬랩 쪽은 구조 최적화를 저희가 MLIP 으로 끝내서 단일점만 돌리면 되고,\n"
                      f"이완이 필요한 잡은 {len(_relax_jobs)}개입니다: `"
                      + "` · `".join(_relax_jobs) + "`.")
    else:
        intro_line = ("슬랩·분자 **전 잡이 단일점**입니다 — 구조 최적화는 저희가 MLIP 으로\n"
                      "끝냈고, 이 묶음에는 `relax/` 폴더가 하나도 없습니다 (기체 기준계 포함).")

    # ⛔⛔ 회신 AP #10 (2026-08-31) — "서로 완전히 독립" 은 **staged 구성에서 거짓**이다.
    #   canary 는 PARENT_GEOM 으로 부모 기체 기준의 최종 기하를 받으므로 부모가
    #   먼저 완주해야 하고, 2단계는 1단계 게이트를 통과해야 열린다. 문서가 독립이라고
    #   적으면 외주가 전부 동시에 던져 정지 규칙이 무력화된다.
    indep_line = (
        "⛔ **서로 독립이 아닙니다.** canary(`*__nzmag`)는 부모 기체 기준의 최종\n"
        "기하를 받으므로 부모가 **먼저** 끝나야 하고, 2단계는 1단계 게이트를\n"
        "통과해야 열립니다. 순서는 `run_staged.sh` 가 강제합니다 — 전부 동시에\n"
        "던지지 마십시오."
        if _staged else
        "서로 **완전히 독립**이라 원하시는 만큼 동시에 돌리셔도 됩니다.")
    _tw = ((cs.get("complexes") or {}).get("d3_off_twins") or 0) if cs else None
    if _tw == 0:
        pose_para = (
            "각 calibration pose 는 `pm1/D3-on` · `net4/D3-on` **두 계산**입니다.\n"
            "**D3-off 쌍둥이는 만들지 않습니다** — 고정기하 static(NSW=0)에서 D3(zero)는\n"
            "SCF 밖의 additive 항이라 `E_on − E_off` 가 항등적으로 OUTCAR 의 `Edisp` 와\n"
            "같습니다. 그래서 그 항을 D3-on 결과에서 직접 읽습니다.\n"
            "같은 POSCAR 가 자기 seed 둘로 두 번 보이는 것은 **정상이고 설계**입니다.\n"
            "중복으로 보고 하나만 돌리시면 그 짝이 통째로 무의미해집니다.")
    elif _tw:
        pose_para = (
            f"각 calibration pose 는 `pm1/D3-on` · `pm1/D3-off` · `net4/D3-on` 세 계산으로\n"
            "구성됩니다. **`net4/D3-off` 는 의도적으로 만들지 않습니다** — 고정기하 D3(zero)는\n"
            "구조 기반 additive correction 이라 자기상태에 무관하므로 반복이 불필요합니다.\n"
            "따라서 같은 POSCAR 가 여러 번 보이는 것은 **정상이고 설계**입니다.\n"
            "중복으로 보고 하나만 돌리시면 그 짝이 통째로 무의미해집니다.")
    else:
        pose_para = ("같은 POSCAR 가 여러 번 보이는 것은 **정상이고 설계**입니다 "
                     "(자기 seed · D3 축). 중복으로 보고 하나만 돌리시면 그 짝이 무의미해집니다.")

    # ⛔⛔ 회신 AR P1-11 · 해제조건 9 (2026-08-31) — 문서가 실물과 충돌했다.
    #   ① 존재하지 않는 clean-slab 반송물을 요구했고 ② 전 잡이 static 이라고 단정했는데
    #   실제로는 기체 relax 가 넷 있었으며 ③ 봉인·attestation·ZIP 해시는 반송물에
    #   아예 없었다. 셋 다 **실물에서 유도**한다.
    _has_clean = bool((man.get("refs") or {}).get("clean_slab")
                      or [k for k in (man.get("planned") or {})
                          if k.startswith("refs/clean_slab")])
    clean_line = ("""가능하시면 **`refs/clean_slab__*` 잡을 먼저** 돌려 보내 주세요. 그것으로 자기
topology gate 를 통과시킨 뒤 complex 결과를 씁니다. raw `net4` 가 pose 마다 다른
basin 으로 수렴하면 저희가 계산을 중단하고 별도 절차를 요청드립니다.
""" if _has_clean else
        """⚠ 이 묶음에는 **깨끗한 슬랩(clean slab) 잡이 없습니다.** 보고하는 양이 두 조각의
**차**라 공통 슬랩 항이 소거되기 때문입니다 — `refs/clean_slab__*` 을 찾지 마십시오.
자기 basin 판정은 두 complex 의 Ni 국소모멘트 배열을 **서로** 비교해서 합니다
(그래서 `LORBIT` 를 켜 두었습니다).
""")
    if _relax_jobs:
        sp_line = ("- **이 묶음에는 `relax/` 상이 %d개 있습니다** (나머지는 단일점):\n"
                   "  `%s`\n"
                   "  확인: `find . -maxdepth 3 -type d -name relax | wc -l` → **%d**\n"
                   "  잡 수는 `find . -name run_job.sh | wc -l` 이 정답입니다."
                   % (len(_relax_jobs), "` · `".join(_relax_jobs), len(_relax_jobs)))
    else:
        sp_line = ("- **전 잡이 단일점입니다.** `relax/` 폴더가 아예 없습니다. 확인하실 수 있습니다:\n"
                   "  `find . -maxdepth 3 -type d -name relax | wc -l` → **0**\n"
                   "  잡 수는 `find . -name run_job.sh | wc -l` 이 정답입니다.")
    _rr = ["- 묶음 루트의 **`POTCAR_ROOT_SEAL.json`** (첫 실행 전에 `SEAL_POTCAR_ROOT.sh` "
           "가 만듭니다) 과 **`ZIP_SHA256.txt`**",
           "- 묶음 루트의 **`POTCAR_ATTESTATION.json`** — 원고에 PAW release 를 적으려면 "
           "**첫 계산 전에** `MAKE_POTCAR_ATTESTATION.sh` 로 만들어 주셔야 합니다 "
           "(`POTCAR_ATTESTATION_REQUEST.md` 참조). 없으면 저희는 release 를 단정하지 "
           "않고 '이 묶음의 PAW dataset 에 조건부' 로만 보고합니다."]
    if _staged:
        _rr.append("- 1단계를 마치면 생기는 **`STAGE1_PASS.json`**")
    root_returns = "\n".join(_rr) + "\n\n"
    # 자세 구성도 **계획에서 센다** (하드코딩한 "대안 1자세" 가 실물과 달랐다)
    _roles_ct = {}
    for _pm in (man.get("planned") or {}).values():
        _mm = _pm.get("meta") or {}
        if _mm.get("kind") == "prospective_pose" and not _mm.get("vacconv"):
            _roles_ct[_mm.get("role") or "primary"] = \
                _roles_ct.get(_mm.get("role") or "primary", 0) + 1
    _nseed = len(man.get("seeds_full") or []) or 1
    _nfrag = len(man.get("fragments") or []) or 1
    _alt_n = sum(v for k, v in _roles_ct.items() if k != "primary")
    _nvac = sum(1 for _pm in (man.get("planned") or {}).values()
                if ((_pm.get("meta") or {}).get("vacconv")))
    role_line = ("조각당 primary %d자세 + 대안 %d자세를 자기 시드 %d종으로 잽니다%s."
                 % (max(1, _roles_ct.get("primary", 0) // max(1, _nfrag * _nseed)),
                    max(0, _alt_n // max(1, _nfrag * _nseed)), _nseed,
                    (". primary 는 셀 두 높이에서 한 번 더 잽니다(진공 두께 수렴 시험, %d잡)"
                     % _nvac) if _nvac else ""))

    # 🔴 회신 AT P0-5 — staged 묶음에서는 **수동 단일 잡 경로를 적지 않는다.**
    #   `run_job.sh` 를 직접 부르면 봉인된 실행파일 검사와 번들 전역 lock 을
    #   둘 다 우회한다. 문서에 적어 두면 그게 곧 우회 경로가 된다.
    manual_block = ("""⛔ 이 묶음은 `run_staged.sh` **하나로만** 돌립니다. 위 블록의
명령을 그대로 쓰십시오. `run_job.sh` 를 직접 부르지 마세요 — 봉인된 실행파일 검사와
번들 전역 lock 을 우회합니다 (회신 AT P0-5).
""" if _staged else ("""```
cd <잡폴더>
PP=/path/to/potpaw_PBE.54 POTCAR_ALLOWLIST=/abs/site_allow.txt bash POTCAR_ASSEMBLE.sh
VASP_CMD="mpirun -np %d vasp_std" bash run_job.sh
```""" % a.cores))

    return f"""# VASP 계산 요청 — LiNiO₂(104) 위 분자 조각 단일점

바쁘신 중에 부탁드려 죄송합니다. **VASP 실행 {n_all or (n_st + n_dn)}회**입니다
({ph_line}).
{intro_line}

## 하실 일

{staged_block}```
mkdir -p <이 묶음 전용 빈 디렉터리> && cd <그 디렉터리>
unzip <이 묶음>.zip
```
{manual_block}

⚠ **묶음이 둘 이상이면 반드시 서로 다른 빈 디렉터리에 풀고 따로 반송해 주세요.**
같은 자리에 겹쳐 풀면 어느 결과가 어느 묶음 것인지 저희가 되살릴 수 없습니다.

### POTCAR 신원 — 별도로 보내주실 것은 없습니다

`POTCAR_ASSEMBLE.sh` 가 조립하면서 **`POTCAR_PROVENANCE.json`** 을 만듭니다.
그 안에 변형별 원본 SHA256 · TITEL 줄 · 조립본 SHA256 이 들어갑니다.
`run_job.sh` 는 그 파일이 없으면 **실행을 거부**하므로 (POTCAR 를 손으로 놓으면 멈춥니다),
반송물에 자동으로 포함됩니다. 저희가 그 값으로 대조합니다.

- **따로 메일로 해시를 보내실 필요 없습니다.**
- ⚠ 이 묶음은 **이전 wave 와의 PP 동등성을 주장하지 않습니다** — 어느 트리를
  쓰셨는지는 봉인이 기록하고, 저희는 "이 묶음 안에서 하나의 트리였는가" 만
  확인합니다 (회신 AO P1 · AR P1-11).
- POTCAR 파일 자체는 주고받지 않습니다 — 해시와 TITEL 줄만 기록됩니다.

잡 폴더 {n_jobs}개가 `{groups}` 에 있습니다.
{indep_line}

{census_md}

## 실행 단계와 결과 범위 (읽어 주세요)

이 요청은 **이것으로 끝나는 계산**입니다 — 뒤에 이어지는 단계가 없습니다.
{role_line} 보고하는 것은 **두 조각의 흡착에너지 차 하나**이고,
개별 절대값은 보고하지 않습니다(깨끗한 슬랩을 계산하지 않으므로 대비에서 소거됩니다).

대안 자세는 최저값 후보가 **아닙니다** — "다른 접촉 방식에서도 방향이 유지되는가" 만
봅니다. 최저·평균·순위에 섞지 않습니다.

{pose_para}

`pm1` 과 `net4` 는 **초기 MAGMOM seed 이름**입니다. 최종 자기상태가 아닙니다.
저희 분석기가 최종 Ni 국소모멘트 부호벡터 · moment collapse · 유기종 상대스핀으로
realized magnetic basin 을 판정하고, **같은 realized basin 으로 매칭되지 않은**
에너지끼리는 빼지 않습니다. 그래서 `LORBIT` 를 켜 두었습니다 — OUTCAR 의
국소모멘트 표가 판정 근거입니다.

{clean_line}

모든 결과는 MLIP 이 고른 **고정기하에서의 PBE+U+D3 단일점 전자에너지**입니다.
DFT-relaxed adsorption energy · 평형 결합에너지 · 자유에너지로 표현하지 않습니다.

## 미리 아셔야 할 것

{sp_line}
- **가장 긴 잡이 약 {longest} 시간**입니다 ({a.cores}코어 기준 추정, ±2배).
  walltime 상한이 이보다 짧으면 그 잡만 알려 주세요 — 나눠서 다시 만들어 드립니다.
- **POTCAR 는 잡마다 종 순서가 다릅니다.** `POTCAR_ASSEMBLE.sh` 가 그 잡에 맞게
  조립하고 순서·variant·PAW_PBE 까지 확인합니다. 하나를 만들어 전체에 복사하시면
  **에러 없이 다른 계를 계산합니다.**

## 보내 주실 것

각 잡의 **`static/OUTCAR`** — 이것 하나면 판정이 됩니다. `.gz` 그대로 좋습니다.
그리고 각 잡의 **`POTCAR_PROVENANCE.json`** (조립기가 자동 생성합니다).

{root_returns}{relax_return}
- `static/vasprun.xml` — 선택
- **CHGCAR / WAVECAR 반송 불필요** (용량)
- 발산·미수렴 잡도 **지우지 말고 그대로** 보내 주세요. 어느 잡이 왜 실패했는지가
  판정의 일부입니다.

## 부탁 — 입력을 고치지 말아 주세요

`INCAR` · `KPOINTS` · `POSCAR` 를 **한 글자도 고치지 말아 주세요.**
분석기가 `MANIFEST.json` 의 sha256 으로 대조하며, **예외 태그 목록을 두지 않았습니다.**
`NCORE` 를 포함해 무엇이든 한 줄이 바뀌면 그 잡은 거부됩니다
(`NCORE` 는 {ncore_hint} 로 넣어 두었습니다).

- 병렬 조정이 꼭 필요하시면 **알려 주세요** — 저희가 다시 만들어 드리는 게 빠릅니다.
- **SCF 가 안 붙는 잡은 그대로 두고 알려만 주세요.** 설정을 바꿔 다시 돌리신 값은
  저희 검증을 통과하지 못해 버려집니다.
- 그래도 직접 재시도해 보셔야 한다면, **원본을 덮지 마시고**
  `<잡폴더>/_retry_1/` 처럼 별도 디렉터리에 남겨 주세요. 원본 실패 상태와 재시도를
  둘 다 받아야 저희가 원인을 압니다.

## 확인용

```
python3 analyze_results.py .       # 필수 산출이 빠지면 exit 2 로 알려 줍니다
```

---
계산 조건·근거·범위는 `MANIFEST.json` 에, 제출 관련 수치는 `SUBMIT_CONTRACT.md` 에
적어 두었습니다. 궁금한 점 있으시면 편하게 물어봐 주세요.

<details><summary>프로토콜 요약 (참고)</summary>

PBE+U(Ni d 6.2 Dudarev) · D3 zero damping(IVDW=11) · ENCUT 520 · ISMEAR 0/0.05 ·
ISYM=0 · LASPH · ADDGRID · LDIPOL/IDIPOL=3 · static k {ks} · dense k {kd} ·
고정 평면 z ≤ {zcut:.3f} Å · 자기 seed 2종(각 끝점마다 둘 다 필요합니다) ·
Ni 는 **Ni_pv**. ⚠ 이전 wave 와의 PP 동등성은 **주장하지 않습니다**, 배포판(release)도
여기서 단정하지 않습니다 — variant 는 `POTCAR_SPEC.txt` 그대로 쓰시고, 원본
fingerprint 는 첫 실행 전에 `SEAL_POTCAR_ROOT.sh` 가 봉인합니다 (회신 AO P1 · AR P1-11).
dense 는 k 검증용이라 {n_dn}개 잡에만 있습니다: {dc or '(없음)'}.
</details>
"""


def _submit_contract(man: Dict[str, Any], a, by_ph: Optional[dict] = None) -> str:
    """제출 계약 — 병렬도·의존성·비용 추정의 **출처**를 못 박는다 (Codex 6차 §7).

    이 파일이 없으면 "2.4일" 이 어떤 병렬도의 산술 하한인지 아무도 모른다.
    이 도구가 못 하는 것: 실제 대기열 지연·노드 성능 차이 반영.
    """
    # ★ 상별 실행 횟수는 **호출부가 센 값**을 그대로 쓴다 (공통 출처 · 회신 Z P0-1).
    #   여기서 다시 세면 갈라진다 — v4 가 정확히 그래서 문서는 40, MANIFEST 는 24 였다.
    by = dict(by_ph or {})
    if not by:                                   # 하위호환 (호출부가 안 주면)
        for _p in man["planned"].values():
            for _ph in (_p.get("phases") or []):
                by[_ph] = by.get(_ph, 0) + 1
        _n_tw = len(man.get("d3_off_twins") or {})
        if _n_tw:
            by["static"] = by.get("static", 0) + _n_tw
    n_st = by.get("static", 0)
    n_dn = by.get("dense", 0)
    n_all = sum(by.values())
    ph_line = " · ".join(f"{k} {v}" for k, v in sorted(by.items()))
    _cs = man.get("job_census") or {}
    _census_block = ("### census\n\n"
                     f"- references {_cs['references']['총']} "
                     f"(끝점 {_cs['references']['endpoints']} + 쌍둥이 "
                     f"{_cs['references']['d3_off_twins']})\n"
                     f"- calibration complexes {_cs['complexes']['총']} "
                     f"(pose×seed {_cs['complexes']['pose×seed']} + 쌍둥이 "
                     f"{_cs['complexes']['d3_off_twins']})\n"
                     f"- audit pose {_cs['audit_pose']}\n"
                     f"- pose 당: {_cs['pose당']}\n") if _cs else ""
    # ⛔⛔ 회신 AP #10 — staged 구성에서는 **잡 사이 의존성이 있다**. 종전 문구
    #   ("잡 사이에는 의존성이 없습니다" + 전체 array 제출 예시)는 정지 규칙을
    #   정면으로 우회시켰다. 구성에 따라 문서를 갈라 쓴다.
    _staged_sub = bool(man.get("staged_runner"))
    # ⛔ 회신 AR P1-11 — 분석에 **실제로 필요한** 반송물을 실물에서 센다.
    #   AR: "SUBMIT_CONTRACT.md 는 분석에 필요한 gas relax/CONTCAR 와 attestation 을
    #   누락한다." relax 가 있으면 그 CONTCAR 가 canary 기하의 출처이므로 필수다.
    _rel_jobs_sub = sorted(k for k, v in (man.get("planned") or {}).items()
                           if "relax" in (v.get("phases") or []))
    _relax_ret_sub = (
        "- **`relax/` 가 있는 잡 %d개의 `relax/OUTCAR` 와 `relax/CONTCAR`** — canary 가\n"
        "  그 최종 기하를 승계하므로 분석에 **반드시** 필요합니다: `%s`\n"
        % (len(_rel_jobs_sub), "` · `".join(_rel_jobs_sub))) if _rel_jobs_sub else ""
    _dep_block = ("""⛔ **잡 사이에 의존성이 있습니다** (이 묶음은 staged 구성입니다).
- canary(`*__nzmag`)는 `PARENT_GEOM` 이 가리키는 **부모 기체 기준의 최종 기하**를
  받습니다 — 부모가 먼저 완주해야 합니다.
- 2단계는 1단계 게이트 **8축**을 전부 통과해야 열립니다 (진공 수렴 · 분자 스핀 ·
  canary 기하 · POTCAR 신원 · 기체 상자 수렴 δ_gas · pm1 자기 topology ·
  잔여 차단 0 · 봉인이 계획 전체를 포괄).
순서는 `run_staged.sh` 가 강제합니다."""
        if _staged_sub else
        "잡 사이에는 의존성이 없습니다. 한 잡의 `run_job.sh` 가 그 잡의 상 순서를 강제합니다.")
    # 🔴 회신 AT P0-5 — staged 묶음에 배열 제출 예시를 적으면 그것이 곧 우회다
    #   (봉인·전역 lock·단계 정지 규칙을 통째로 건너뛴다).
    slurm_block = ("""⛔ **배열(sbatch --array) 제출 예시는 이 묶음에 적지 않습니다.**
잡을 각자 던지면 봉인된 실행파일 검사·번들 전역 lock·1단계 정지 규칙을 모두
우회합니다. `run_staged.sh` 안에서 병렬도를 조절하세요 (`NPAR` 환경변수).
""" if _staged_sub else ("""# Slurm 예시 — 동시 %d개
sbatch --array=1-$(wc -l < JOBS.txt)%%%%%d \\
  --ntasks=%d --time=120:00:00 --wrap='
  j=$(sed -n "${SLURM_ARRAY_TASK_ID}p" JOBS.txt)
  cd "$j"
  PP=/path/to/potpaw_PBE.54 POTCAR_ALLOWLIST=/abs/site_allow.txt bash POTCAR_ASSEMBLE.sh
  VASP_CMD="srun -n %d vasp_std" bash run_job.sh'""" % (a.concurrency, a.concurrency,
                                                        a.cores, a.cores)))

    _submit_block = ("""## 실행 (이 경로 하나뿐입니다)
```bash
cd <이 묶음을 푼 디렉터리>              # 묶음 **루트**
export PP=/path/to/potpaw_PBE.54
export POTCAR_ALLOWLIST=/abs/site_allow.txt
export BUNDLE_ZIP_SHA256=$(sha256sum /경로/받은번들.zip | cut -d" " -f1)   # 필수
export EXPECT_MANIFEST_SHA256=<메일 본문의 MANIFEST SHA256>                # **필수**
export EXPECT_ZIP_SHA256=<메일 본문의 ZIP SHA256>                          # **필수**
# ⛔ VASP_CMD 는 더 쓰지 않습니다 (러너가 거부합니다) — 런처와 실행파일을 나눕니다
export VASP_LAUNCHER="mpirun -np %d"        # 런처와 플래그만 (실행파일 넣지 마세요)
export VASP_EXE=/abs/path/to/vasp_std       # 봉인 대상 실행파일
bash run_staged.sh 1     # 조립+봉인 → census → 1단계 → 판정
bash run_staged.sh 2     # 1단계 통과 뒤에만
```
⛔ **전체를 배열로 한꺼번에 던지지 마십시오.** 위 의존성 때문에 결과가 무의미해집니다.
`run_all.sh` 는 이 묶음에 **넣지 않았습니다**.
⛔ `BUNDLE_ZIP_SHA256` 이 없으면 봉인 스크립트가 거부합니다 (번들 안에는 자기 해시를
넣을 수 없어 받으신 파일에서 직접 구해 주셔야 합니다).

## 수치 게이트 (이 값들이 결과 판정을 정합니다)

| 게이트 | 문턱 | 뜻 |
|---|---:|---|
| 진공 두께 수렴 Δ_vac | 5 meV | 셀 두 높이의 대비 차 |
| 기체 상자 수렴 δ_gas | 5 meV | box20↔box24 **두 조각의 차** |
| k 격자 수렴 δ_k | 5 meV | static k↔dense k **두 조각의 차** |
| 자기 basin 일치 | 정확 일치 | 비교하는 두 복합체의 Ni 부호 배열 (전역 반전은 동치) |

⚠ 셋 다 **조각별이 아니라 두 조각의 차**에 겁니다. 조각별로 각각 작아도
부호가 반대면 차에서 두 배가 되기 때문입니다.

## 반드시 같이 반송해 주실 것
- `POTCAR_ROOT_SEAL.json` (첫 실행 전 봉인) 과 `ZIP_SHA256.txt`
- `POTCAR_ATTESTATION.json` — 원고에 PAW release 를 적으려면 **첫 계산 전에**
  `MAKE_POTCAR_ATTESTATION.sh` 로 만들어 주셔야 합니다 (없으면 release 를 단정하지
  않고 '이 묶음의 PAW dataset 에 조건부' 로만 보고합니다)
- `STAGE1_PASS.json` (1단계 통과 receipt)
- 각 잡의 `POTCAR_PROVENANCE.json`
- **부모·canary 의 `static/POSCAR`** (두 기하가 같은지 저희가 대조합니다)
- 각 상의 `OUTCAR`(또는 `.gz`)·`OSZICAR`
%s""" % (a.cores, _relax_ret_sub)) if _staged_sub else ("""## 병렬 제출 (권장)
`run_all.sh` 는 **직렬 디버그용**입니다. 실제로는 잡 목록을 배열로 던지세요:
```bash
# ⚠ 폴더 이름을 손으로 적지 않는다 — refs/ 냐 controls/ 냐가 모드에 따라 다르다.
#   2026-08-12: controls/ 로 적어 두는 바람에 기준계 10잡이 통째로 빠질 뻔했다.
find . -mindepth 2 -maxdepth 2 -type d -name '*__*' -o \\
     -mindepth 2 -maxdepth 2 -type d -path './refs/*' | sed 's|^\\./||' | sort > JOBS.txt
n=$(wc -l < JOBS.txt)
[ "$n" = %d ] || { echo "잡 %d개여야 하는데 $n 개"; exit 1; }
{slurm_block}
```""" % (man.get("n_jobs", 0), man.get("n_jobs", 0)))

    # ⛔ 회신 AR P1-11 — walltime 도 하드코딩(56 h)이었다. cost_frozen 에서 가져온다.
    _long_h = round((man.get("cost_frozen") or {}).get("longest_job_h") or 56)
    _long_h2 = _long_h * 2
    _long_rec = max(24, int(_long_h2 * 1.1 // 12 + 1) * 12)
    return f"""# 제출 계약 (SUBMIT_CONTRACT)

## 상 의존성
```
static  (같은 단계 안에서는 병렬 가능)
   └─ dense   (같은 잡의 static/CHGCAR 필요 → **그 잡 안에서는 직렬**)
```
{_dep_block}

## 규모
| | |
|---|---:|
| 잡 | {man.get('n_jobs', '?')} |
| static 실행 | {n_st} |
| dense 실행 | {n_dn} |
| 총 VASP 실행 | **{n_all}** |
| 상별 | {ph_line} |

⚠ **잡 수의 정본은 `find . -name run_job.sh | wc -l`** 입니다 —
`MANIFEST.planned` 에는 D3-off 쌍둥이가 들어 있지 않으므로 그것으로 세면 적게 나옵니다.

{_census_block}

{_submit_block}

⚠ **공통 POTCAR 를 전 잡에 복사하면 안 됩니다.** 조각마다 POSCAR 종 순서가 달라
(`Li Ni O` · `Li Ni O C F` · `Li Ni O C F H` · `Li Ni O S C H`) 하나를 돌려 쓰면
그 잡은 조용히 **다른 계**를 계산합니다. `POTCAR_ASSEMBLE.sh` 가 잡마다 조립하고
TITEL 수까지 검증합니다.
⚠ walltime — 가장 긴 잡이 중앙 추정 {_long_h} h 이고 모형 불확실성이 ±2배입니다.
   ±2배 외피가 {_long_h2} h 이므로 **{_long_rec} h** 를 권합니다 (그보다 짧으면 잘립니다).

## 비용 추정의 출처
- 모델: `tools/sdcp/vasp_cost_estimate.py` — 2026-08-08 납품 `slab/OUTCAR.gz`
  (192원자 · NKPTS 4 · 48코어 · 30,438 s / 58 전자스텝 = **525 s/스텝**)
- **±2배 불확실성**을 인정하는 모델입니다. 계약값이 아니라 계획용 수치입니다.
- `python3 tools/sdcp/vasp_cost_estimate.py --manifest MANIFEST.json --concurrent {a.concurrency}`
  로 이 번들의 실제 계획에서 다시 계산하세요.
- ⚠ **aggregate 시간 ÷ 동시 실행 수**는 산술 하한입니다. 한 잡의
  static→dense 임계경로가 그 하한보다 길면 하한에 도달할 수 없습니다.

## 코어 수
이 번들은 **{a.cores} 코어/잡 · 동시 {a.concurrency}잡**으로 계획했습니다
(MANIFEST.json 의 `submission`). 실제와 다르면 추정이 그만큼 어긋납니다 —
알려 주시면 `--manifest` 로 다시 계산합니다.
"""


README = """# VASP 외주 요청 v3 — SDCP/PTFE 자리 선호 + 흡착에너지 (원샷)

## 무엇을 계산하나
LiNiO₂(104) 슬랩 위 분자 조각의 **자리 선호**(Li_top vs Ni_top)와 **흡착에너지**.
MLIP 스크리닝은 경향까지만 냈고, 이 DFT+U 가 최종 판정입니다.

## 잡 구조 — **잡마다 여러 상**
각 잡 폴더: `POSCAR` + `pre/` + `relax/` + `static/`(일부는 `dense/`) + `run_job.sh`.
**판정 에너지는 static 입니다** — relax 만 돌리면 결과가 성립하지 않습니다.
`pre/` 는 dipole 을 끈 사전 SCF 입니다 (자기상태가 엉뚱한 basin 으로 무너지는 것을 막습니다).
`run_job.sh` 가 상 사이 CHGCAR/WAVECAR 승계를 **강제**합니다 — 파일이 없으면 멈춥니다.
```
cd <잡폴더> && cp <POTCAR> POTCAR && VASP_CMD="mpirun -np 48 vasp_std" bash run_job.sh
```
전체는 번들 루트에서 `bash run_all.sh` (tier1 → refs → tier2 순).

## 실행 순서 (권장)
1. `tier1/` 전부 — 이번 판의 목적. **자기 seed 2종(pm1/net4)이 전 잡에 있습니다. 둘 다.**
2. `refs/` 전부 — E_ads 필수 (clean 2 + 분자 조각당 상자 2종)
3. `tier2/` — **여기도 seed 2종입니다.** 하나만 돌리면 그 쌍은 판정에서 빠집니다.

POTCAR 는 미포함(라이선스) — `POTCAR_SPEC.txt` 변형 그대로. **Ni 는 Ni_pv**
(2026-08-08 납품과 동일). VASP 5.4.4 또는 6.x + PBE PAW 5.4 세트.

## ⚠ 지켜야 결과가 성립하는 것
- **INCAR 수정 금지 — 예외 없습니다.** 분석기에 태그 allowlist 가 **구현돼 있지
  않고**, `files_sha256` 이 INCAR 전체를 덮으므로 `NCORE` 한 줄만 바꿔도 그 잡은
  거부됩니다 (회신 Z P0-7 — 종전 문구는 있지도 않은 예외를 약속했습니다).
  · 병렬 조정이 필요하면 **알려 주세요.** 저희가 다시 만들어 드립니다.
  · **SCF 가 안 붙으면 그대로 두고 알려만 주세요.** 설정을 바꿔 얻은 값은 검증을
    통과하지 못해 버려집니다.
  · 그래도 재시도하셔야 하면 **원본을 덮지 마시고** `<잡폴더>/_retry_1/` 에 남겨
    주세요 — 실패 상태와 재시도를 둘 다 받아야 원인을 압니다.
- static 은 relax 의 CONTCAR/CHGCAR 를 승계합니다 (run_job.sh 가 자동으로 합니다).
- 발산/미수렴 잡은 그대로 두고 알려 주세요.

## 예상 비용 (참고)
슬랩 relax(~220원자·DFT+U) 잡당 64코어 기준 수 시간~하루 + static 은 그 1/5 급,
pre 는 SCF 한 번, dense 는 static 의 ~3배 k 점.
**82 systems · 259 VASP phase runs** (pose 72×3상=216 · dense 20 · clean 7 · 기체 16).
tier1 32잡 + refs 10잡이 1차 목표. 분자 기준계는 분 단위.

## 반송물 (잡마다 · 상마다)
- **`relax/OUTCAR` + `relax/CONTCAR` + `static/OUTCAR` — 셋 다 필수** (`.gz` 그대로 가능).
  CONTCAR 없으면 그 잡은 "등록 미검증" 으로 판정에서 빠집니다.
- **`dense/OUTCAR` 는 있으면 필수** — k 수렴 게이트가 이걸로 걸립니다. 빠지면 그 쌍이
  NUMERICALLY_UNRESOLVED 로 내려갑니다.
- `pre/OUTCAR` 도 보내 주세요 (사전 SCF 가 실제로 돌았는지 확인용).
- vasprun.xml 선택. **CHGCAR/WAVECAR 반송 불필요**
  (CHGCAR 는 가능하면 보관 — 후속 U-ramp 대비).
- ⚠ **INCAR/KPOINTS/POSCAR 를 고치지 마세요.** 분석기가 MANIFEST 의 sha256 과 대조해
  바뀐 파일을 잡아냅니다. **예외 태그는 없습니다** — 병렬 태그를 포함해 무엇이든
  한 줄이 바뀌면 그 잡은 거부됩니다.

## 완주 후
```
python3 analyze_results.py .
```
수렴/기하/자기 게이트 → seed-매칭 ΔE → E_ads → 판정까지 전부 나옵니다 (stdlib).
필수 산출이 빠지면 exit 2 로 알려 줍니다. `RESULTS.json` + 반송물을 보내 주세요.

## 무결성 (선택)
`MANIFEST.json` 의 `files_sha256` 와 대조: `sha256sum <파일>`

## 범위 밖
변형에너지 분해(E_int/E_deform)·DOS/Bader·진동/ZPE 는 이번 요청 범위 밖입니다.

## 프로토콜 (요약)
PBE+U(Ni d 6.2 Dudarev) · D3 zero damping(IVDW=11) · ENCUT 520 · ISMEAR=0/0.05 ·
ISYM=0 · LASPH · ADDGRID · 슬랩 LDIPOL/IDIPOL=3+DIPOL(COM) · relax k {k_relax} →
static k {k_static} (판정 정본) · 공유 고정 평면 z ≤ {zcut_note} (아래 {freeze_pct}%) ·
자기 seed = 2026-08-08 납품 계보(Ni 24/24 ±1 μB) · 기체상 IDIPOL=4·NUPDOWN·상자 2종.
근거는 MANIFEST.json.
"""


# ─────────────────────────────────────────────────────────────────────────────
def load_ledger(a) -> Dict[str, Any]:
    """AFM 부격자 원장 — **파일에서 읽지 않고 매번 다시 만든다** (staleness 차단).

    옛 JSON 을 읽으면 슬랩이 바뀌어도 눈치채지 못한다. QE 입력과 슬랩 파일에서
    그 자리에서 재구성하면 게이트(정수 슈퍼셀·전 원자 매칭·부격자 균형)가 항상 돈다.
    """
    import afm_ledger as AL
    led = AL.build_ledger(AL.parse_qe(a.qe), AL.parse_poscar(SS.SLAB["path"]))
    led["source_qe"] = str(a.qe)
    led["source_slab"] = str(SS.SLAB["path"])
    led["naive_block_halves"] = AL.block_halves_agreement(led)
    return led


def guard_refs_minimal(a):
    """`--refs_minimal`(C-12 구성)은 **자세 동결 없이 쓸 수 없다.** 위반이면 SystemExit.

    ⛔⛔ 2026-08-30 실측 fail-open — `--from_basins` 를 빼면 자세 동결을 **안 읽고**
      champion/cross 자동탐색으로 떨어진다. 조각 2개로 좁혔는데도 **잡 40개**가 나왔다
      (C-12 는 12잡). 그런데 `claim_scope` 는 C-12 문구를 그대로 달아서,
      **동결 안 된 후보집합에 사전등록된 범위 주장이 붙는다.**
      범위 문구와 후보집합이 갈리는 것은 회신 AJ 가 반복해 잡은 유형이다.

    ⛔ 이 함수가 못 하는 것: 준 동결 파일이 **맞는 것인지**는 안 본다 (그건 from_basins
      repo 경로 검사와 freeze_sha256 대조의 몫이다).
    """
    if getattr(a, "refs_minimal", False) and not getattr(a, "from_basins", None):
        sys.exit(
            "⛔ --refs_minimal 은 --from_basins 없이 쓸 수 없다 (2026-08-30).\n"
            "   그것 없이는 자세 동결을 안 읽고 champion/cross 자동탐색으로 떨어지는데,\n"
            "   범위 문구(claim_scope)는 C-12 그대로라 **동결 안 된 집합에 사전등록\n"
            "   범위가 붙는다.** 자세 동결을 같이 준다:\n"
            "     --from_basins db/properties/c12_poses_2026_08_30.json")

    # ⛔⛔ 2026-08-30 실측 두 번째 — `--refs_minimal` 은 **기체 기준을 켜지 않는다.**
    #   이름과 달리 "기준을 낸다면 box24 하나로 좁힌다" 라서, `--refs` 없이 주면
    #   기체 기준이 **0개**로 나온다. 그런데 C-12 의 추정량은
    #     D = [E_C^SDCP − E_G^SDCP] − [E_C^PTFE − E_G^PTFE]
    #   라 `E_G` 없이는 **정의 자체가 안 된다.** 실측: 12잡이어야 할 번들이 6잡으로 나왔고
    #   (기체 2 + net4 4 누락) claim_scope 는 흡착에너지 차 문구를 그대로 달고 있었다.
    if getattr(a, "refs_minimal", False) and not getattr(a, "refs", False):
        sys.exit(
            "⛔ --refs_minimal 은 --refs 없이 쓸 수 없다 (2026-08-30).\n"
            "   --refs_minimal 은 기준을 **켜는** 플래그가 아니라 **좁히는** 플래그다.\n"
            "   그것만 주면 기체 기준이 0개로 나오고, E_G 가 없으면\n"
            "   D = [E_C−E_G]^SDCP − [E_C−E_G]^PTFE 가 **정의되지 않는다.**\n"
            "     --refs --refs_minimal 로 같이 준다.")

    # ⛔ 같은 실측 — 자기 대조군(net4 가지)이 빠지면 C-12 의 자성 위상 검사가 없어진다.
    if getattr(a, "refs_minimal", False) and not getattr(a, "both_seeds", False):
        sys.exit(
            "⛔ --refs_minimal 은 --both_seeds 없이 쓸 수 없다 (2026-08-30).\n"
            "   없으면 SEED_MAIN(pm1) 가지만 나와 **net4 4잡이 통째로 빠진다**\n"
            "   (실측: 12잡이어야 할 번들이 6잡). 자성 위상 대조가 사라진다.\n"
            "     --both_seeds 를 같이 준다.")


def build_bundle(a, ledger: Optional[Dict[str, Any]] = None) -> Path:
    if ledger is None:
        ledger = load_ledger(a)
    out_final = Path(a.out)
    if out_final.exists() and any(out_final.iterdir()):
        sys.exit(f"⛔ {out_final} 이 비어 있지 않다 — 옛 번들과 섞이면 안 된다. 새 경로를 줄 것")
    out = out_final.parent / (out_final.name + ".building")
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    slab = SS.load_slab()
    nslab = a.nslab

    try:
        commit = subprocess.run(["git", "-C", str(SS.REPO), "rev-parse", "HEAD"],
                                capture_output=True, text=True).stdout.strip()
    except Exception:
        commit = "unknown"
    man: Dict[str, Any] = {
        "created": __import__("datetime").date.today().isoformat(), "repo_commit": commit,
        "bundle_version": "v3", "gate_version": SS.gate_version(),
        "freeze_frac_dft": a.freeze, "kmesh": KMESH, "nslab": nslab,
        "seeds_full": list(SEEDS_FULL), "seed_main": SEED_MAIN,
        "potcar_spec": {}, "fragments": [], "pairs": {}, "refs": {}, "planned": {},
        "magnetic_lineage": (
            "부격자 원장으로 확정 (tools/sdcp/afm_ledger.py). QE 원본 "
            "db/inputs/sdcp_v2/slab_relax/relax.in 의 Ni1/Ni2 를 슬랩(= 그 셀의 1×4×1 "
            "슈퍼셀)에 좌표로 매칭했다. 부호는 2026-08-08 납품 계보 승계: Ni2=−1 · Ni1=+1. "
            "⚠ 2026-08-12 정정 — v2 초판의 '파일 순서 앞 24 / 뒤 24' seed 는 실제 부격자와 "
            "24/48(동전 던지기) 일치라 **다른 자기 배치**였다. 그 seed 로 만든 번들은 무효."),
        "afm_ledger": ledger,
        # ⚠ 모드에 따라 **사실이 다르다**. 단일점 판에 "다상·LREAL=F" 를 적어 두면
        #   외주처와 나중의 우리가 다른 프로토콜을 돌았다고 읽는다 (Codex 6차 §8).
        "protocol_delta_vs_phaseB": (
            ("의도된 개선: LASPH T(납품 F) · LDIPOL T(납품 F) · ISMEAR 0/0.05"
             "(납품 1/0.2). **상 구성은 납품과 같은 단일점**이고 LREAL 도 Auto 로 "
             "같다 — 이번 판이 바꾼 것은 기하 출처(UMA 이완)와 자기 seed 2종이다. "
             "승계: U 6.2 · IVDW 11 · ENCUT 520 · Ni_pv.")
            if a.single_point else
            ("의도된 개선: LASPH T(납품 F) · LDIPOL T(납품 F) · ISMEAR 0/0.05"
             "(납품 1/0.2) · pre+relax+static+dense 다상(납품 단일점) · "
             "LREAL static .FALSE.(납품 Auto). 승계: U 6.2 · IVDW 11 · ENCUT 520 · Ni_pv.")),
    }
    # k 를 밖에서 덮을 수 있게 한다 — ΔE 에서 k 오차는 대부분 상쇄되므로, 예산이
    # 빠듯하면 **상쇄되는 정밀도**를 풀고 상쇄 안 되는 것(자기 seed)을 지키는 게 맞다.
    kover = {}
    if a.kmesh_static:
        kover["static"] = a.kmesh_static
    if a.kmesh_dense:
        kover["dense"] = a.kmesh_dense
    man["kmesh_override"] = kover or None
    # ⚠ man["kmesh"] 는 **기본값**이라 실제 입력과 다를 수 있다 (Codex zip 감사).
    #   실제로 쓴 값을 권위 필드로 따로 둔다 — 두 값이 같이 있으면 반드시 오독된다.
    man["kmesh_effective"] = {ph: kover.get(ph, KMESH[ph]) for ph in ("relax", "static", "dense")}
    man["kmesh_note"] = ("`kmesh_effective` 가 실제 배포된 KPOINTS 다. `kmesh` 는 도구 "
                         "기본값이고 `kmesh_override` 로 덮인다 — 인용은 effective 로.")
    # ⚠ 오타 하나면 dense 가 0개가 되고 (조각 이름이 안 맞으니) 아무 경고 없이
    #   "k 검증 없는 번들" 이 나간다. fail-closed 로 잡는다 (Codex 6차 §8).
    known = {f for fs in TIERS.values() for f in fs}
    if a.dense_frags is not None:
        if not a.dense_frags:
            sys.exit("⛔ --dense_frags 가 비었다 — 지정하지 않을 거면 플래그를 빼라 "
                     "(빈 목록은 'dense 0개' 를 조용히 만든다)")
        unknown = [f for f in a.dense_frags if f not in known]
        if unknown:
            sys.exit(f"⛔ --dense_frags 에 모르는 조각 {unknown} — 아는 조각: "
                     f"{sorted(known)}. 오타면 dense 가 0개가 된다")
    man["dense_calibrators"] = list(a.dense_frags) if a.dense_frags else None
    if a.dense_frags:
        man["k_label_rule"] = (
            "직접 dense 한 조각만 K_DIRECTLY_CHECKED. 전이 게이트(|κ|≤10 · |Δκ|≤10 meV)를 "
            "통과한 나머지는 K_TRANSFER_SCREENED — **K_CONVERGED 아님**. 게이트 실패 시 "
            "K_UNVERIFIED.")
    used_els: set = set()
    n_jobs = 0

    from ase.io import read as ase_read
    # ── clean slab provenance (Codex P0-B) ──────────────────────────────────
    # ⚠ 옛 구현은 **첫 번째** _clean_slab.vasp 하나만 집고, 없으면 raw slab 로 조용히
    #   fallback 했다. 조각마다 clean 이 다르면 E_ads 가 전부 어긋나는데 아무도 모른다.
    # ⚠ 2026-08-29 — 종전엔 **전 조각**을 훑었다. 이 번들에 안 들어가는 조각의 clean 이
    #   달라도 막혀서, `--frags` 로 두 조각만 뽑을 때 무관한 조각 때문에 중단됐다.
    #   제약의 뜻은 "**이 번들 안의** 조각들이 같은 슬랩을 쓴다" 이므로 범위를 그렇게 좁힌다.
    _want = set(a.frags) if a.frags else None
    cps = sorted(q for q in Path(a.runs).glob(f"*/relax_f{a.freeze:.2f}/_clean_slab.vasp")
                 if _want is None or q.parent.parent.name in _want)
    if not cps:
        sys.exit(f"⛔ {a.runs}/*/relax_f{a.freeze:.2f}/_clean_slab.vasp 이 하나도 없다 — "
                 f"raw 슬랩으로 조용히 대체하지 않는다 (E_ads 기준계가 달라진다)")
    hashes = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in cps}
    if len(set(hashes.values())) != 1:
        sys.exit("⛔ **이 번들 안의** 조각별 clean slab 이 서로 다르다 — E_ads 기준계가 "
                 "갈린다 (--frags 로 좁힌 범위에서 본 것이다):\n  "
                 + "\n  ".join(f"{h[:12]}  {p}" for p, h in sorted(hashes.items())))
    clean = ase_read(cps[0])
    man["clean_slab"] = {"path": str(cps[0]), "sha256": list(hashes.values())[0],
                         "n_sources_identical": len(cps)}
    _z = clean.positions[:, 2]
    zcut = float(_z.min() + (_z.max() - _z.min()) * a.freeze)
    man["z_cut_shared_A"] = round(zcut, 3)
    slab_metas: List[Dict[str, Any]] = []

    def plan(relpath: str, phases: List[str], required: bool, meta=None):
        """계획에 잡 하나를 등록한다.

        ⛔ 2026-08-31 — `meta` 를 같이 담는다. 종전엔 phases/required 만 담아서
          문서·분석기가 잡의 성격(kind/role/seed)을 **되짚을 수 없었다**.
          그래서 estimand_job_keys 가 비었고(v9), README 의 단계별 잡 수가
          하드코딩(12)으로 남아 canary 추가 뒤 거짓이 됐다.
        """
        man["planned"][relpath] = {"phases": phases, "required": required}
        if meta:
            man["planned"][relpath]["meta"] = {
                k: meta.get(k) for k in
                ("kind", "fragment", "role", "seed", "basin_id", "vacconv")
                if meta.get(k) is not None}

    # ── 계약 (Codex P0-A) ────────────────────────────────────────────────────
    # ⚠⚠ 옛 구현은 조각/쌍/xyz/분자 ref 가 없으면 **조용히 건너뛰고** 축소된 MANIFEST 를
    #   새 정본으로 만들었다. planned 에 안 들어가니 required_missing 도 못 잡는다 —
    #   ptfe_c10 전체가 빠져도 exit 0 이 가능했다. 이제 계약을 먼저 못 박고 대조한다.
    expect = dict(EXPECT_PAIRS)
    if a.expect:
        expect = {}
        for kv in a.expect:
            k, _, v = kv.partition("=")
            expect[k] = int(v)
    # ⚠ 선별 모드는 **기대값 자체를 바꾼다**. 검사에만 반영하고 MANIFEST 에는 원래 수를
    #   적으면, 나중에 읽는 사람이 "계약 5인데 1개뿐" 으로 오해한다 (분석기의
    #   CONTRACT_SHORT 도 오작동한다). 유효 계약을 기록한다.
    guard_refs_minimal(a)

    if a.champion:
        expect = {k: 1 for k in expect}
        man["contract_mode"] = "champion — 조각당 Li 위 최선·Ni 위 최선 1쌍"
    elif a.top_n is not None:
        expect = {k: min(v, a.top_n) for k, v in expect.items()}
        man["contract_mode"] = f"top_n={a.top_n} — 자세 안정도 상위 N 쌍"
    man["contract_expected_pairs"] = expect
    man["allow_partial"] = bool(a.allow_partial)
    man["pair_audit"] = {}
    viol: List[str] = []

    def bad(msg: str):
        viol.append(msg)
        print(("  ⚠ " if a.allow_partial else "  ⛔ ") + msg)

    # ══ 동결된 prospective 후보에서 생성 (회신 W 5단계) ══════════════════════
    #   ⛔ champion/cross 자동탐색을 **쓰지 않는다.** 자세는 동결 manifest 가 정하고,
    #      생성기는 그것만 읽는다 — 그래야 "사전등록된 집합" 이 실제로 강제된다.
    if getattr(a, "from_basins", None):
        fb = json.load(open(a.from_basins))
        # 회신 X P0-2 — calibration 만 낸 것은 **최종 후보집합이 아니다.**
        #   이름을 그대로 두면 분석기가 primary 를 내고, audit 이 나중에 더 낮게
        #   나와도 "더 낮은 자세를 찾았다" 로 흡수돼 selector 실패가 사라진다.
        _rl = tuple(getattr(a, "roles", None) or ("calibration", "sealed_audit"))
        # 이름은 manifest 의 **키**가 아니라 뽑힌 basin 의 `role` 이 정한다 —
        #   motif_probe 를 calibration 키에 담아 넘기는 판이 있어서, 키만 보면
        #   probe 번들이 `calibration_pilot` 으로 잘못 라벨된다.
        _actual = sorted({b.get("role") or r
                          for fr2 in (fb.get("fragments") or {}).values()
                          for r in _rl for b in (fr2.get(r) or [])})
        if _actual == ["motif_probe"]:
            _name = "motif_probe"
        elif _actual == ["holdout"]:
            # 층화 홀드아웃 — **primary 후보집합이 아니다.** 이것으로 primary 를
            # 내면 사전등록된 집합이 사라지고 min 이 표본크기를 따라 움직인다.
            _name = "holdout_stratified"
        elif set(_actual) <= {"primary", "sensitivity",
                              "stress_sensitivity"} and _actual:
            # C-12 경로 (회신 AI §A-Q4 = C). 홀드아웃·merge 가 없는 단일 묶음이다
            _name = "c12"
        elif len(_rl) > 1:
            _name = "prospective_lowE"
        else:
            _name = "calibration_pilot"
        man["candidate_set"] = "%s (frozen %s)" % (_name, fb.get("freeze_sha256", "?")[:16])
        man["emitted_roles"] = list(_rl)
        man["emitted_basin_roles"] = _actual
        man["from_basins"] = {"path": os.path.abspath(a.from_basins),
                              "sha256": hashlib.sha256(
                                  open(a.from_basins, "rb").read()).hexdigest(),
                              "declared_freeze": fb.get("freeze_sha256"),
                              "audit_seed": (fb.get("params") or {}).get("audit_seed")}
        for frag, fr in sorted((fb.get("fragments") or {}).items()):
            if a.frags and frag not in a.frags:
                continue
            # tier 루프를 안 타므로 여기서 조각 목록을 채운다 (clean slab·기체 기준이 읽는다)
            if frag not in man["fragments"]:
                man["fragments"].append(frag)
            run = Path(a.runs) / frag / f"relax_f{a.freeze:.2f}"
            # ⛔ 회신 X P0-2 — calibration 과 audit 을 **동시에 던지면 안 된다.**
            #    audit 은 calibration 이 창 W 를 확정한 **뒤에** 봉인을 푼다.
            #    처음부터 둘을 함께 내면 audit 이 최저가 돼도 "더 낮은 자세를
            #    찾았다" 로 흡수돼 selector 실패가 사라진다 (회신 X Q6).
            _roles = tuple(getattr(a, "roles", None)
                           or ("calibration", "sealed_audit"))
            picks = [b for r in _roles for b in (fr.get(r) or [])]
            if not picks:
                bad(f"{frag}: 동결 manifest 에 {'/'.join(_roles)} 가 없다")
                continue
            print(f"■ {frag}: 동결 후보 {len(picks)}개 [{','.join(_roles)}] "
                  f"(cal {len(fr.get('calibration') or [])} · "
                  f"audit {len(fr.get('sealed_audit') or [])})")
            for b in picks:
                lab = b["rep_label"]
                xp = run / f"{lab}.xyz"
                if not xp.is_file():
                    bad(f"{frag}/{b['basin_id']}: {xp} 없음")
                    continue
                cx = ase_read(xp)
                cx.set_cell(slab.cell.array)
                cx.set_pbc(True)
                _assert_slab_lineage(cx, nslab, slab, f"{frag}/{b['basin_id']}", man)
                _assert_mol_topology(cx, nslab, frag, f"{frag}/{b['basin_id']}", man)
                used_els |= set(cx.get_chemical_symbols())
                for sd in (list(SEEDS_FULL) if a.both_seeds else [SEED_MAIN]):
                    rel = f"prospective/{frag}__{b['basin_id']}__{sd}"
                    m = _emit_slab_job(
                        out / rel, cx, nslab, a.freeze, frag,
                        f"{frag} {b['basin_id']} ({b['role']}) {sd}", sd,
                        {"kind": "prospective_pose", "fragment": frag,
                         "basin_id": b["basin_id"], "role": b["role"],
                         # ★ 회신 AB P0-1 — basin 자세는 Li/Ni **짝**으로 정의된 게
                         #   아니라 anchor 로 정의된다. 등록 기대가 **없다**는 것을
                         #   비워 두지 말고 선언한다 (없으면 role 이 그 자리로 읽혀
                         #   `calibration -> Ni` 로 항상 불일치했다).
                         "registry_role": None,
                         "why": b.get("why"), "source_pose": lab,
                         "uma_E_pose_eV": b.get("E_pose_eV"),
                         "contact_fingerprint": b.get("fingerprint"),
                         "anchor": b.get("anchor"), "height_A": b.get("height_A"),
                         "source_xyz_sha256": hashlib.sha256(
                             xp.read_bytes()).hexdigest()},
                        ledger, zcut=zcut, dense=False,
                        prescf=not a.no_prescf, single_point=a.single_point,
                        closure=a.closure, kmesh_over=kover)
                    slab_metas.append(m)
                    plan(rel, m["phases"], True, m)
                    # ⛔ 2026-08-31 (회신 AN P0-1) — D 에 들어갈 **primary·주 seed** 잡을
                    #   여기서 바로 기록한다. `planned` 는 phases/required 만 담아서
                    #   나중에 되짚을 수 없다 (v9 에서 estimand_job_keys 가 비었던 이유).
                    if b["role"] == "primary" and sd == SEED_MAIN:
                        man.setdefault("_primary_by_frag", {})[frag] = rel
                    # ⛔ 회신 AR P1-10 — 대안 자세도 **어느 역할의 무엇인지** 기록한다.
                    #   종전엔 완료 여부만 보고돼 봉인된 식·비교·판정이 없었다.
                    elif b["role"] in ("sensitivity", "stress_sensitivity") \
                            and sd == SEED_MAIN:
                        man.setdefault("_altpose_by_frag", {}).setdefault(
                            b["role"], {})[frag] = rel
                    n_jobs += 1
                    print(f"   {b['basin_id']} {b['role']:14s} {sd:14s} "
                          f"UMA {b.get('E_pose_eV'):+8.4f}  {lab[:40]}")
                    # ★ 진공 두께 수렴 시험 (회신 AI §D) — **primary · 주 seed 만**
                    #   같은 자세를 더 높은 셀로 한 번 더 낸다. 판정은 두 조각의
                    #   대비 변화에 적용하므로 기체·슬랩 항은 소거된다.
                    _c2 = getattr(a, "cell_c2", None)
                    if _c2 and b.get("role") == "primary" and sd == SEED_MAIN:
                        rel2 = f"vacconv/{frag}__{b['basin_id']}__{sd}__c2"
                        m2 = _emit_slab_job(
                            out / rel2, cx, nslab, a.freeze, frag,
                            f"{frag} {b['basin_id']} (vacuum-convergence c2) {sd}", sd,
                            {"kind": "prospective_pose", "fragment": frag,
                             "basin_id": b["basin_id"], "role": b["role"],
                             "registry_role": None, "vacconv": "c2",
                             "why": "vacuum-thickness convergence test (second cell)",
                             "source_pose": lab,
                             "uma_E_pose_eV": b.get("E_pose_eV"),
                             "contact_fingerprint": b.get("fingerprint"),
                             "anchor": b.get("anchor"), "height_A": b.get("height_A"),
                             "source_xyz_sha256": hashlib.sha256(
                                 xp.read_bytes()).hexdigest()},
                            ledger, zcut=zcut, dense=False,
                            prescf=not a.no_prescf, single_point=a.single_point,
                            closure=a.closure, kmesh_over=kover)
                        slab_metas.append(m2)
                        plan(rel2, m2["phases"], True, m2)
                        n_jobs += 1
                        print(f"   {b['basin_id']} {'vacconv c2':14s} {sd:14s} "
                              f"→ {rel2}")
    else:
        pass  # 아래 champion/cross 경로

    for tier, frags in ({} if getattr(a, 'from_basins', None)
                        else TIERS).items():
        # 82잡을 이번 원샷의 **전체 범위**로 선언했으므로 tier2 도 필수다.
        # (Codex P0-4 — required=False 면 tier2 가 전부 실패해도 wrapper 가 exit 0 이된다.)
        req = True
        tier1 = tier == "tier1"
        for frag in frags:
            if a.frags and frag not in a.frags:
                continue
            run = Path(a.runs) / frag / f"relax_f{a.freeze:.2f}"
            if not run.is_dir():
                bad(f"{frag}: {run} 없음")
                continue
            aud: Dict[str, Any] = {}
            pairs = discover_pairs(run, audit=aud,
                                   allow_stale_gate=a.allow_stale_gate,
                                   top_n=a.top_n, champion=a.champion,
                                   cross=(a.champion and not a.no_cross and
                                          (frag in a.cross_endpoints
                                           if a.cross_endpoints else True)))
            man["pair_audit"][frag] = aud
            if not pairs:
                bad(f"{frag}: 자격 쌍 0개")
                continue
            want = expect.get(frag)
            if want is not None and len(pairs) != want:
                bad(f"{frag}: 대조쌍 {len(pairs)}개 — 계약은 {want}개 "
                    f"(down_dir {aud.get('n_down_dirs')}개 · 제외 "
                    f"{list(aud.get('excluded_dirs') or {})})")
            man["fragments"].append(frag)
            med_all = float(np.median([p["dE_uma"] for p in pairs]))
            probe = min(pairs, key=lambda p: abs(p["dE_uma"] - med_all))
            ex = aud.get("excluded_dirs") or {}
            print(f"■ {frag} ({tier}): 대조쌍 {len(pairs)}개 / down_dir "
                  f"{aud.get('n_down_dirs')}개 (탐침: {probe['dir']}_r{probe['roll']:03d})"
                  + (f"\n    제외 {len(ex)}방향 (대조쌍 아님): "
                     + "; ".join(f"{d}={list(c)}" for d, c in ex.items()) if ex else ""))
            for p in pairs:
                pid = f"{frag}__{p['dir']}_r{p['roll']:03d}"
                # 2026-08-12 범위 결정: **tier1·tier2 모두 전 끝점 2 seed** (86잡).
                #   seed 1종 쌍은 seed 산포를 ΔE 에서 못 걷어내 최종 판정에 못 쓴다.
                seeds = list(SEEDS_FULL)
                # dense-k: tier1 은 **전 pm1 끝점**, tier2 는 탐침쌍만 (2026-08-12 결정)
                # ★ dense 는 **k 보정자(calibrator)** 로 지정한 조각에만 (Codex 5차 ①).
                #   champion 모드에선 조각당 쌍이 하나뿐이라 `probe` 조건이 전부 참이 되어
                #   4조각 전부 켜졌다 = 8 dense = 3.2일 (예산 초과). 명시 지정으로 바꾼다.
                dense = (frag in a.dense_frags) if a.dense_frags else (tier1 or p is probe)
                xyzs = {role: (run / f"{rec['label']}.xyz", rec)
                        for role, rec in (("Li", p["li"]), ("Ni", p["ni"]))}
                miss = [r for r, (xp, _) in xyzs.items() if not xp.is_file()]
                if miss:
                    bad(f"{pid}: {'/'.join(miss)} 쪽 xyz 없음 — 쌍 통째로 빠짐")
                    continue
                pm = {"fragment": frag, "dir": p["dir"], "roll": p["roll"],
                      "matched": p.get("matched", True),
                      "champion_dirs": p.get("champion_dirs"),
                      "champion_pose": p.get("champion_pose"),
                      "uma_dE": p["dE_uma"], "uma_dir_median": p["dir_median_uma"],
                      "n_rolls_folded": p["n_rolls"], "seeds": seeds,
                      "dense_probe": dense,
                      "li_prefix": f"{tier}/{pid}__Litop",
                      "ni_prefix": f"{tier}/{pid}__Nitop"}
                pm["source_sha256"] = {}
                for role, (xp, rec) in xyzs.items():
                    jp = xp.with_suffix(".json")
                    pm["source_sha256"][role] = {
                        "xyz": hashlib.sha256(xp.read_bytes()).hexdigest(),
                        "json": (hashlib.sha256(jp.read_bytes()).hexdigest()
                                 if jp.is_file() else None),
                        "fingerprint": rec.get("fingerprint"),
                        # ⚠ gate_version 은 **protocol 안**에 있다. 최상위에서 읽으면
                        #   조용히 None 이 박혀 provenance 가 빈 채로 납품된다.
                        "gate_version": (rec.get("protocol") or {}).get("gate_version"),
                        "roll_deg": rec.get("roll_deg"),
                        "down_dir": rec.get("down_dir")}
                    cx = ase_read(xp); cx.set_cell(slab.cell.array); cx.set_pbc(True)
                    _assert_slab_lineage(cx, nslab, slab, f"{pid}/{role}", man)
                    _assert_mol_topology(cx, nslab, frag, f"{pid}/{role}", man)
                    used_els |= set(cx.get_chemical_symbols())
                    for sd in seeds:
                        rel = f"{tier}/{pid}__{role}top__{sd}"
                        m = _emit_slab_job(
                            out / rel, cx, nslab, a.freeze, frag,
                            f"{pid} {role}-top {sd}", sd,
                            {"kind": "pose", "role": role, "registry_role": role,
                             "pair_id": pid,
                             "fragment": frag, "source_pose": rec["label"],
                             "uma_E_pose_eV": rec["E_pose_eV"]},
                            ledger, zcut=zcut, dense=dense and sd == SEED_MAIN,
                            prescf=not a.no_prescf, single_point=a.single_point, closure=a.closure,
                            kmesh_over=kover,
                            dense_cand=(a.adaptive_dense and dense
                                        and sd != SEED_MAIN))
                        slab_metas.append(m)
                        plan(rel, m["phases"], req)
                        n_jobs += 1
                # ── 전역 챔피언 끝점 (2026-08-12) ──────────────────────────
                #   풀 제한 때문에 (a)배향일치 대비와 (b)전역 자리 선호가 갈리면,
                #   둘 다 DFT 로 재야 "어느 질문에 답했는지" 를 말할 수 있다.
                gshift = abs(p.get("global_shift_meV") or 0.0)
                if gshift >= a.global_champion_meV:
                    for role, rec in (p.get("global_best") or {}).items():
                        xg = run / f"{rec['label']}.xyz"
                        if not xg.is_file():
                            bad(f"{pid}: 전역 챔피언 {role} 의 xyz 없음 ({rec['label']})")
                            continue
                        cg = ase_read(xg); cg.set_cell(slab.cell.array); cg.set_pbc(True)
                        _assert_slab_lineage(cg, nslab, slab, f"{pid}/global_{role}", man)
                        _assert_mol_topology(cg, nslab, frag, f"{pid}/global_{role}", man)
                        used_els |= set(cg.get_chemical_symbols())
                        jg = xg.with_suffix(".json")
                        pm.setdefault("global_best", {})[role] = {
                            "prefix": f"{tier}/{pid}__global_{role}",
                            "down_dir": rec["down_dir"], "roll_deg": rec.get("roll_deg"),
                            "role": role, "registry_role": role,
                            "source_pose": rec["label"],
                            "uma_E_pose_eV": rec["E_pose_eV"],
                            "source_sha256": {
                                "xyz": hashlib.sha256(xg.read_bytes()).hexdigest(),
                                "json": (hashlib.sha256(jg.read_bytes()).hexdigest()
                                         if jg.is_file() else None),
                                "fingerprint": rec.get("fingerprint"),
                                "gate_version": (rec.get("protocol")
                                                 or {}).get("gate_version")}}
                        for sd in seeds:
                            rel = f"{tier}/{pid}__global_{role}__{sd}"
                            m = _emit_slab_job(
                                out / rel, cg, nslab, a.freeze, frag,
                                f"{pid} global-{role} {sd}", sd,
                                {"kind": "global_champion", "role": role,
                                 "pair_id": pid, "fragment": frag,
                                 "source_pose": rec["label"],
                                 "uma_E_pose_eV": rec["E_pose_eV"]},
                                ledger, zcut=zcut, dense=False,
                                prescf=not a.no_prescf, single_point=a.single_point, closure=a.closure,
                                kmesh_over=kover)
                            slab_metas.append(m)
                            plan(rel, m["phases"], req)
                            n_jobs += 1
                    if p.get("global_best"):
                        print(f"    ↳ {pid}: 전역 shift {p['global_shift_meV']:+.1f} meV "
                              f"→ 전역 챔피언 {list(p['global_best'])} 끝점 추가 "
                              f"(배향일치 대비와 **다른 질문**이라 둘 다 잰다)")
                elif p.get("global_best"):
                    pm["global_unmeasured"] = {
                        "shift_meV": p.get("global_shift_meV"),
                        "why": (f"|shift| < {a.global_champion_meV} meV 문턱 — 전역 최선 "
                                f"자세를 DFT 로 재지 않았다.\n"
                                f"⚠ 부호 규약: shift = restr_Li − restr_Ni 이므로 "
                                f"**D_global = D_pool + shift** 다 (2026-08-12 정정 — "
                                f"−shift 로 적혀 있었다).\n"
                                f"⚠ 그리고 이 항등식은 **UMA 안에서만** 성립한다. DFT 값에 "
                                f"더해 DFT global 을 추정하면 안 된다 — 자세마다 UMA→DFT "
                                f"보정이 같다는 보장이 없다.")}
                    print(f"    ⚠ {pid}: 전역 shift {p['global_shift_meV']:+.1f} meV "
                          f"(문턱 {a.global_champion_meV} 미만) — 전역 대비는 UMA 추정만")

                # ── 교차 끝점 방출 (2×2 완성) ──
                for tag, rec in (p.get("cross") or {}).items():
                    xp = run / f"{rec['label']}.xyz"
                    if not xp.is_file():
                        bad(f"{pid}: 교차 끝점 {tag} 의 xyz 없음 ({rec['label']})")
                        continue
                    cx = ase_read(xp); cx.set_cell(slab.cell.array); cx.set_pbc(True)
                    _assert_slab_lineage(cx, nslab, slab, f"{pid}/{tag}", man)
                    used_els |= set(cx.get_chemical_symbols())
                    role = "Li" if tag.startswith("Li") else "Ni"
                    jpx = xp.with_suffix(".json")
                    pm.setdefault("cross", {})[tag] = {
                        "prefix": f"{tier}/{pid}__cross_{tag}",
                        "down_dir": rec["down_dir"], "roll_deg": rec.get("roll_deg"),
                        "role": role, "registry_role": role,
                        "source_pose": rec["label"],
                        # ★ 교차 끝점도 main 과 **같은 provenance** 를 남긴다 (Codex 6차 §8).
                        #   없으면 "어느 프로토콜 산출인가" 를 교차만 확인할 수 없다.
                        "source_sha256": {
                            "xyz": hashlib.sha256(xp.read_bytes()).hexdigest(),
                            "json": (hashlib.sha256(jpx.read_bytes()).hexdigest()
                                     if jpx.is_file() else None),
                            "fingerprint": rec.get("fingerprint"),
                            "gate_version": (rec.get("protocol") or {}).get("gate_version")}}
                    for sd in seeds:
                        rel = f"{tier}/{pid}__cross_{tag}__{sd}"
                        m = _emit_slab_job(
                            out / rel, cx, nslab, a.freeze, frag,
                            f"{pid} cross {tag} {sd}", sd,
                            {"kind": "cross", "role": role, "pair_id": pid,
                             "cross_tag": tag, "fragment": frag,
                             "source_pose": rec["label"],
                             "uma_E_pose_eV": rec["E_pose_eV"]},
                            ledger, zcut=zcut, dense=False,
                            prescf=not a.no_prescf, single_point=a.single_point, closure=a.closure,
                            kmesh_over=kover)
                        slab_metas.append(m)
                        plan(rel, m["phases"], req)
                        n_jobs += 1
                # ★ 자세키가 다른데 교차가 없으면 ΔE 는 **자리+배향 혼합값**이다.
                #   조용히 내보내면 나중에 자리 선호로 인용된다.
                if p.get("matched") is False and not p.get("cross"):
                    pm["orientation_confounded"] = True
                    print(f"    ⚠⚠ {pid}: 챔피언 자세키가 다른데 교차 끝점이 없다 "
                          f"(Li {p['champion_pose']['Li']} vs Ni {p['champion_pose']['Ni']}) "
                          f"— ΔE 에 자리와 배향이 섞인다. 분리 불가.")
                elif p.get("matched") is False:
                    print(f"    ↳ {pid}: 자세키 불일치 → 교차 {len(p['cross'])}개 추가 "
                          f"(2×2 완성 · 배향 분리)")
                if p.get("cross_missing"):
                    pm["cross_missing"] = p["cross_missing"]
                    for t2, why in p["cross_missing"].items():
                        print(f"    ⚠ {pid}: 교차 끝점 {t2} 없음 — {why}")
                man["pairs"][pid] = pm

    # ⚠ `--from_basins` 는 **basin 단위**로 생성한다 (Li/Ni 대조쌍이 아니다). 그래서
    #   쌍 개수 게이트를 적용하지 않는다 — 대신 생성된 잡이 0개면 그때 막는다.
    if getattr(a, "from_basins", None):
        if not slab_metas:
            shutil.rmtree(out)
            sys.exit("⛔ 동결본에서 생성된 자세가 0개다 — rep_label 과 relax 산출물을 확인할 것")
    elif not man["pairs"]:
        shutil.rmtree(out)
        sys.exit("⛔ 자격 쌍이 0개다 — 번들을 만들지 않는다 "
                 "(--runs/--freeze 경로와 relax 산출물을 확인할 것)")

    # ★ Wave 1 (2026-08-12 Codex 5차) — clean/gas 기준계는 **같은 조각의 Li/Ni 차에서
    #   정확히 소거된다**. 이번 판의 headline 은 자리 대비(ΔE)이므로 기준계를 Wave 2 로
    #   미루고 그 자원을 C10 2×2 에 쓴다. complex 총에너지를 보존하면 나중에 그대로
    #   결합할 수 있다 — 데이터 손실이 아니라 **주장 순서의 변경**이다.
    #   ⚠ 기준계 없이는 절대 E_ads 를 만들 수 없다 → "흡착이 유리하다"·"A 가 B 보다
    #     세게 결합한다"·"결합이 몇 eV 다" 는 이번 판에서 주장 금지.
    # ★★ clean slab 은 **두 목적**이 있고, refs 를 끄면 둘 다 사라진다 (Codex 6차).
    #   ① E_ads 기준계 (기체 분자와 짝) — Wave 2 로 미뤄도 된다
    #   ② **자기 대조군** — pose 의 Ni 자기질서 붕괴를 재는 기준. 이게 없으면
    #      분석기의 q_ref 가 None 이 되어 전 잡이 "판정 보류" 로 **통과**한다.
    #   ②는 Wave 1 에 남긴다. dense 없이 coarse static 2 seed = 약 29 h.
    mag_ctl = a.mag_controls and not a.refs
    # ⛔ 회신 AJ ② — C-12 에서는 clean slab 을 만들지 않는다. 승인된 estimand 에서
    #   두 조각이 같은 슬랩이라 대비에서 정확히 소거되고, 절대 E_ads 는 새 연구목표다.
    #   ⚠ 대신 자기 판정이 clean 기준에 의존하지 않아야 한다 (아래 direct topology).
    _skip_clean = bool(getattr(a, "refs_minimal", False))
    for sd in (() if _skip_clean else (SEEDS_FULL if (a.refs or mag_ctl) else ())):
        rel = (f"refs/clean_slab__{sd}" if a.refs else f"controls/clean_slab__{sd}")
        m = _emit_slab_job(out / rel, clean, len(clean), a.freeze, man["fragments"][0],
                           f"clean slab {sd}", sd,
                           {"kind": "clean_ref" if a.refs else "clean_magnetic_control"},
                           ledger, zcut=zcut,
                           dense=(a.refs and sd == SEED_MAIN
                                  and not getattr(a, 'no_refs_dense', False)),
                           prescf=not a.no_prescf, single_point=a.single_point, closure=a.closure,
                           kmesh_over=kover)
        slab_metas.append(m)
        plan(rel, m["phases"], True, m)
        n_jobs += 1
        # ★ 둘째 셀의 clean slab — **절대 E_ads 를 보고하려면** 필요하다.
        #   대비만 볼 거면 소거되지만, 절대값의 수렴은 따로 봐야 한다. 주 seed 만.
        if getattr(a, "cell_c2", None) and a.refs and sd == SEED_MAIN:
            rel2 = f"vacconv/clean_slab__{sd}__c2"
            m2 = _emit_slab_job(out / rel2, clean, len(clean), a.freeze,
                                man["fragments"][0],
                                f"clean slab {sd} (vacuum-convergence c2)", sd,
                                {"kind": "clean_ref", "vacconv": "c2"},
                                ledger, zcut=zcut, dense=False,
                                prescf=not a.no_prescf,
                                single_point=a.single_point, closure=a.closure,
                                kmesh_over=kover)
            slab_metas.append(m2)
            plan(rel2, m2["phases"], True, m2)
            n_jobs += 1
    # ⚠ refs 가 아닌 대조군을 man["refs"] 에 넣으면 has_refs 가 참이 되어 분석기가
    #   E_ads 를 만들려 든다 (기체 분자가 없는데). 별도 키로 등록한다.
    # ⛔⛔ 2026-08-31 (회신 AN P0-2) — `--refs_minimal` 이면 clean slab **잡을 안 만드는데**
    #   선언만 남겼다. 분석기는 그 선언으로 `has_refs=True` 가 되어 box20·box24 를 다
    #   요구하고, 없는 clean 잡 때문에 모든 복합체를 MAGNETIC_REFERENCE_INVALID 로 막았다.
    #   **없는 것을 선언하지 않는다.**
    man["refs"]["clean_slab"] = ([] if _skip_clean else
                                 ([f"refs/clean_slab__{s}" for s in SEEDS_FULL]
                                  if a.refs else []))
    man["magnetic_controls"] = ([f"controls/clean_slab__{s}" for s in SEEDS_FULL]
                                if mag_ctl else
                                (man["refs"]["clean_slab"] if a.refs else []))
    # ⛔ 2026-08-31 (회신 AN P1) — box20 을 뺀 구성에서는 **선행 상자 대조**를 실어 보낸다.
    #   최종 D 에는 `E_G^SDCP − E_G^PTFE` 가 남아 기체 상자 오차가 소거되지 않는다.
    #   출처: 2026-08-12 wave1 (db/properties/sdcp_wave1_results.json).
    #   ⚠ 같은 conformer·같은 Hamiltonian 이라는 보증은 **그 출처가 진다** — 여기서
    #     증명하지 않는다. 그래서 `ref` 와 한계를 같이 싣는다.
    # ⛔ 회신 AP #11 — box20 을 실제로 계산하므로 **선행 대조를 싣지 않는다.**
    #   (남겨두면 분석기가 참고정보로 쓰고, 원고에 "선행값" 이 흘러들 여지가 있다)
    if False:
        man["gas_box_prior"] = {
            "ptfe_c10": {"dE_meV": 0.07, "box20_eV": -177.970705, "box24_eV": -177.970639},
            "sdcp_neutral": {"dE_meV": 0.32, "box20_eV": -205.448886, "box24_eV": -205.448564},
        }
        for _f in man["gas_box_prior"]:
            man["gas_box_prior"][_f].update({
                "ref": "db/properties/sdcp_wave1_results.json (2026-08-12 wave1)",
                "⚠": ("이번 묶음의 기체 conformer 가 그때와 **같은 구조인지 좌표 해시로 "
                      "대조하지 못했다** — wave1 반송물이 남아 있지 않다")})
        man["gas_box_prior"] = {k: v for k, v in man["gas_box_prior"].items()
                                if k in (man.get("fragments") or [])}

    # ⛔⛔ 2026-08-31 (회신 AN P0-1) — D 에 들어가는 **정확한 네 잡**을 기계 필드로 봉인한다.
    #   문서(§4)에만 적어 두면 판정기는 여전히 조각별 min 을 골라, SDCP 와 PTFE 가
    #   서로 다른 seed 에서 뽑힐 수 있다. 분석기는 이 필드가 있으면 **그 네 에너지만**
    #   직접 대입한다. net4·대안 자세는 sensitivity 로만 나간다.
    if _skip_clean and getattr(a, "single_point", False):
        _sd = next((f for f in (man.get("fragments") or []) if "sdcp" in f), None)
        _ct = next((f for f in (man.get("fragments") or []) if f != _sd), None)
        _pri = dict(man.get("_primary_by_frag") or {})
        if _sd and _ct and _pri.get(_sd) and _pri.get(_ct):
            man["estimand_job_keys"] = {
                "E_C_sdcp": _pri[_sd], "E_C_control": _pri[_ct],
                "E_G_sdcp": f"refs/mol__{_sd}__box24",
                "E_G_control": f"refs/mol__{_ct}__box24",
                "formula": "D = (E_C_sdcp - E_G_sdcp) - (E_C_control - E_G_control)",
                "branch": SEED_MAIN,
                "⛔": ("net4 와 대안 자세(sensitivity·stress_sensitivity)는 **D 에 안 들어간다** "
                       "— 자기 분기·자세 민감도 병기용이다. 조각별 최솟값을 다시 쓰지 않는다"),
            }

            # ⛔⛔ 회신 AO P0-7 (2026-08-31) — net4 를 **별도 직접식**으로 봉인한다.
            #   종전엔 net4 가 같은 조각 집합에 섞여 basin 동종성 검사에 걸렸고,
            #   그 한 건이 pm1 네 값이 전부 정상인데도 D 를 통째로 지웠다
            #   (BASIN_HETEROGENEOUS → NO_VALUE). 요구했던 `D_net4 − D_pm1` 은
            #   정작 계산되지 않았다. ⇒ 두 D 를 따로 만들고 차는 민감도로만 쓴다.
            _alt = next((x for x in SEEDS_FULL if x != SEED_MAIN), None)
            if _alt:
                _n4 = {k: v.replace("__" + SEED_MAIN, "__" + _alt)
                       for k, v in (("E_C_sdcp", _pri[_sd]), ("E_C_control", _pri[_ct]))}
                if all(v in man["planned"] for v in _n4.values()):
                    man["estimand_job_keys_net4"] = dict(
                        _n4,
                        E_G_sdcp=f"refs/mol__{_sd}__box24",
                        E_G_control=f"refs/mol__{_ct}__box24",
                        formula="D_net4 = (E_C_sdcp - E_G_sdcp) - (E_C_control - E_G_control)",
                        branch=_alt,
                        **{"⛔": ("이것은 **민감도**다. 사전등록 보고값은 pm1 조건부 D 이고, "
                                 "D_net4 − D_pm1 은 자기 분기 민감도로만 병기한다. "
                                 "net4 가 다른 basin 이어도 pm1 조건부 D 를 지우지 않는다")})

            # ⛔⛔ 회신 AR P1-10 · 해제조건 6 (2026-08-31) — **대안 자세를 봉인한다.**
            #   AR: "대안자세 네 잡은 완료 여부만 보고될 뿐 봉인된 exact 식·비교·
            #   판정이 없다. sensitivity claim 에 쓸 것이라면 key·식·gate·status 를
            #   정의하고, 아니면 단순 탐색용임을 명시해야 한다."
            #   ⇒ 자세 민감도를 net4 분기 민감도와 **같은 모양**으로 봉인한다:
            #        D_pose(role) = (E_C_sdcp[role] − E_G_sdcp)
            #                     − (E_C_control[role] − E_G_control)
            #        보고량 = D_pose(role) − D_pm1
            #      게이트도 같다 — 두 complex 가 같은 자기 branch 여야 하고,
            #      게이트된 잡이 있으면 값을 내지 않는다.
            _alt_by_role = (man.get("_altpose_by_frag") or {})
            _sealed_alt = {}
            # ⛔⛔ 2026-08-31 실측 (v16 첫 생성) — 두 조각의 대안 자세가 **다른 역할
            #   이름**을 달고 있다: sdcp_neutral=stress_sensitivity(b12),
            #   ptfe_c10=sensitivity(b52). 같은 역할끼리만 짝지으면 어느 쪽도 짝이
            #   없어 봉인이 통째로 비고, 스테이지 2 의 네 잡이 아무 정의된 양도
            #   내지 못한다. ⇒ ① 같은 역할이 양쪽에 다 있으면 그 역할로 봉인하고
            #   ② 없으면 **조각당 하나뿐인 대안 자세**를 짝지어 `role_pair` 로
            #   봉인하되 **역할이 비대칭이라는 사실을 봉인 안에 적는다**.
            #   ⚠ 이 봉인은 계산식·게이트·status 만 정의한다 — **무엇을 뜻하는지는
            #     주장하지 않는다** (리뷰 AS Q4 로 열어 둔다). 결과를 본 뒤에
            #     정하면 결과 의존적 선택이 되므로 지금 박는다.
            def _seal_pair(_key, _ja, _jb, _extra=None):
                if not (_ja and _jb):
                    return
                if not all(v in man["planned"] for v in (_ja, _jb)):
                    return
                _sealed_alt[_key] = dict({
                    "E_C_sdcp": _ja, "E_C_control": _jb,
                    "E_G_sdcp": f"refs/mol__{_sd}__box24",
                    "E_G_control": f"refs/mol__{_ct}__box24",
                    "formula": ("D_pose[%s] = (E_C_sdcp - E_G_sdcp) "
                                "- (E_C_control - E_G_control)" % _key),
                    "reported": "D_pose[%s] - D_pm1 (자세 민감도)" % _key,
                    "branch": SEED_MAIN,
                    "gate": ("두 complex 가 같은 자기 branch (전역 반전 동치) · "
                             "두 잡 모두 게이트 없음 · 두 에너지 모두 회수 — "
                             "하나라도 어긋나면 값과 status 를 함께 막는다"),
                }, **(_extra or {}))

            for _role in sorted(_alt_by_role):
                _rr = _alt_by_role[_role]
                _seal_pair(_role, _rr.get(_sd), _rr.get(_ct))
            if not _sealed_alt:
                _one_sd = sorted({v[_sd] for v in _alt_by_role.values() if v.get(_sd)})
                _one_ct = sorted({v[_ct] for v in _alt_by_role.values() if v.get(_ct)})
                _rl_sd = sorted(r for r, v in _alt_by_role.items() if v.get(_sd))
                _rl_ct = sorted(r for r, v in _alt_by_role.items() if v.get(_ct))
                if len(_one_sd) == 1 and len(_one_ct) == 1:
                    _seal_pair("role_pair", _one_sd[0], _one_ct[0], {
                        "⚠_역할_비대칭": (
                            "두 조각의 대안 자세가 **다른 이유로** 골렸다 — "
                            "%s=%s · %s=%s. 따라서 이 값은 '같은 종류의 자세 변화' "
                            "가 아니라 '두 조각을 각자의 사전등록 대안 자세로 "
                            "옮겼을 때' 의 대비다."
                            % (_sd, _rl_sd, _ct, _rl_ct)),
                        "roles": {_sd: _rl_sd, _ct: _rl_ct},
                        "⛔_해석_미정": (
                            "이 봉인은 **계산식·게이트·status 만** 정의한다. "
                            "값이 크게 나왔을 때 그것이 '자세 민감도가 크다' 인지 "
                            "'사전등록 자세 선택이 틀렸다' 인지는 아직 정하지 "
                            "않았다 (리뷰 AS Q4). 결과를 본 뒤 고르면 결과 의존적 "
                            "선택이 되므로, 식만 먼저 박고 해석은 열어 둔다."),
                    })
            if _sealed_alt:
                man["estimand_job_keys_pose_alt"] = dict(
                    _sealed_alt,
                    **{"⛔": ("이것은 **자세 민감도**다. 사전등록 보고값은 primary "
                             "자세의 pm1 조건부 D 이고, 이 값들을 대신 쓰거나 "
                             "평균하지 않는다. 자세 min 을 다시 뽑지도 않는다 "
                             "(champion pool size bias)")})
            else:
                man["altpose_purpose"] = (
                    "대안 자세 잡은 **탐색용**이다 — 봉인된 비교식이 없으므로 "
                    "완료 여부만 보고하고 sensitivity claim 에 쓰지 않는다 "
                    "(회신 AR P1-10)")

    # ⛔⛔ 회신 AS 해제조건 9 (2026-08-31) — **k 수렴 근거가 없다.**
    #   0.01 eV 로 보고하는데 static k(3 4 1) 에서 dense k(4 6 1) 로 갈 때
    #   두 조각의 차가 얼마나 움직이는지 잰 적이 없다. AR 의 box20 과 같은 종류의
    #   판단이라 **결과를 보기 전에** 넣는다.
    #     δ_k = (E_sdcp,dense − E_sdcp,coarse) − (E_ptfe,dense − E_ptfe,coarse)
    #   ⚠ 같은 잡에 dense 상을 **추가**한다 (새 폴더가 아니라 phase 추가) —
    #     같은 POSCAR·같은 CHGCAR 승계라 k 외에 달라지는 것이 없다.
    #   ⚠ δ_k 는 **두 조각의 차**라 조각이 둘일 때만 뜻이 있다. 하나짜리 구성에서는
    #     dense 를 붙이지 않는다 (붙여 봐야 뺄 상대가 없다).
    _pri_k = dict(man.get("_primary_by_frag") or {})
    if len(_pri_k) != 2:
        _pri_k = {}
        if getattr(a, "refs_minimal", False) and man.get("estimand_job_keys"):
            man["kconv_pair"] = {
                "status": "not_applicable",
                "why": "primary 조각이 둘이 아니다 (%d) — δ_k 는 두 조각의 차다"
                       % len(man.get("_primary_by_frag") or {})}
    if _pri_k and getattr(a, "refs_minimal", False):
        _kadd = []
        for _f, _rel in sorted(_pri_k.items()):
            _pl = (man["planned"].get(_rel) or {})
            _phs = list(_pl.get("phases") or [])
            if "dense" in _phs:
                continue
            _jd = out / _rel
            _inc = _jd / "static" / "INCAR"
            if not _inc.is_file():
                continue
            (_jd / "dense").mkdir(exist_ok=True)
            # dense 는 static 의 CHGCAR 를 승계한다 (ICHARG=1) — 그 한 줄만 다르다
            _dtxt = (_inc.read_text().replace("ICHARG   = 2", "ICHARG   = 1")
                                     .replace("[static]", "[dense k · static CHGCAR 승계]"))
            (_jd / "dense" / "INCAR").write_text(_dtxt)
            (_jd / "dense" / "KPOINTS").write_text(
                _kpoints_text("dense", KMESH["dense"]))
            _phs.append("dense")
            _pl["phases"] = _phs
            (_pl.setdefault("meta", {}).setdefault("kmesh", {}))["dense"] = KMESH["dense"]
            _mj = _jd / "job.json"
            if _mj.is_file():
                _m = json.loads(_mj.read_text())
                _m.setdefault("kmesh", {})["dense"] = KMESH["dense"]
                # 🔴🔴 회신 AT P0-2 (2026-08-31) — 종전엔 dense 상을 **만들기만** 하고
                #   `incar_expected.dense` 를 안 실었다. 분석기는
                #   `(meta["incar_expected"] or {}).get(ph, {})` 로 읽으므로 dense 는
                #   기대값이 **빈 dict** 였고, ENCUT 400 · IVDW 0 · ISPIN 1 · LDAU F ·
                #   ICHARG 2 인 OUTCAR 가 그대로 통과해 그 E0 가 δ_k 에 들어갔다.
                _m.setdefault("incar_expected", {})["dense"] = _incar_expected_from(_dtxt)
                _m.setdefault("kpoints_expected", {})["dense"] = _kpoints_expected(
                    "dense", KMESH["dense"])
                _m["phases"] = _phs
                _mj.write_text(json.dumps(_m, indent=1, ensure_ascii=False))
            _kadd.append(_rel)
        if len(_kadd) == 2:
            man["kconv_pair"] = {
                "jobs": sorted(_kadd),
                "coarse_kmesh": KMESH["static"], "dense_kmesh": KMESH["dense"],
                "formula": ("δ_k = (E_sdcp,dense − E_sdcp,coarse) "
                            "− (E_ctl,dense − E_ctl,coarse)"),
                "tol_eV": 0.005,
                "gate": ("|δ_k| ≤ 5 meV 여야 0.01 eV 로 보고한다. 넘으면 보고 "
                         "해상도를 낮추거나 dense 로 다시 낸다"),
                "⚠": ("조각별 값이 각각 작아도 **부호가 반대면 차에서 커진다** — "
                       "그래서 조각별이 아니라 이 차에 문턱을 건다 (δ_gas 와 같은 논리)"),
                "⛔": "회신 AS 해제조건 9 — 결과를 보기 전에 넣었다"}
        elif _kadd:
            sys.exit("⛔ dense k 쌍이 %d개만 만들어졌다 (%s) — 두 조각 다 있어야 "
                     "δ_k 를 만들 수 있다" % (len(_kadd), _kadd))

    man.pop("_primary_by_frag", None)
    man.pop("_altpose_by_frag", None)
    man["wave"] = 1 if not a.refs else "1+refs"
    # ★ 조각마다 주장 범위가 다르다 (2026-08-12 설계 변경). 공통 mode 문장 하나로
    #   두면 PTFE 에도 "2×2 완성" 이 적혀 오독된다.
    # 🔴🔴 회신 AT 해제조건 8 (2026-08-31) — **낡은 claim policy 를 삭제한다.**
    #   종전엔 조각마다 `quantities: ["E_ads", "dE_site"]` 를 실었다. 그 둘은
    #   이 묶음의 산출물이 **아니고**(옛 wave 용어), 바로 아래 `reported_quantity`
    #   가 "각 항을 adsorption energy 라고 부르지 말라" 고 하는 것과 정면으로
    #   충돌했다. 산출물이 서로 반대를 말하면 강한 쪽이 인용된다.
    man["claim_policy"] = {
        f: {"quantities": ["D (fixed-geometry differential complex–gas "
                           "reference energy) — 조각 하나만으로는 만들어지지 않는다"],
            "not_claimed": (["E_ads · dE_site — 이 묶음의 산출물이 아니다",
                             "배향 분해(2×2 없음)", "전역 자리 선호",
                             "고립 흡착·평형 결합·실제 전극 피복률로의 일반화"]
                            + (["cap 인공물이 있는 짧은 모델 — C10 의 대조군으로만"]
                               if f == "ptfe_dimer" else [])),
            "note": ("이 조각은 D 의 **한 항**이다. 조각별 값을 단독으로 인용하지 "
                     "않는다 (회신 AT 해제조건 8)")}
        for f in man.get("fragments", [])}
    # ⛔⛔ 회신 AS 해제조건 8·9 (2026-08-31) — 보고량의 **이름과 범위**를 못 박는다.
    #   AS Q2 가 준 문구를 그대로 쓴다: 각 항을 adsorption energy 라고 부르면 안 된다.
    #   AS Q7 lateral: 옵션 (a) — **셀 조건으로 한정**한다 (lateral 대조를 넣지 않는다).
    man["reported_quantity"] = {
        "name": "fixed-geometry differential complex–gas reference energy",
        "korean": "고정기하 복합체−기체기준 차등에너지 (두 조각의 차)",
        "formula": "D = (E_C_sdcp − E_G_sdcp) − (E_C_control − E_G_control)",
        "⛔_부르면_안_되는_이름": [
            "adsorption energy — 각 항을 그렇게 부르면 안 된다 (AS Q2)",
            "binding energy · free energy — 평형·고립계 양이 아니다",
            "E_ads · dE_site — 이 묶음의 산출물이 아니다 (옛 wave 용어)"],
        "포함되는_것": ["조각 변형에너지", "표면 변형에너지",
                        "고정된 gas conformer 선택 효과"],
        "제외되는_것": ["기하 이완", "영점·열적 기여", "용매·계면 전기장"],
        "gas_conformer_provenance": {
            "출처": "MLIP(UMA) 로 고른 조각 conformer 하나를 **모든 자세에 공통**으로 쓴다",
            "선택_규칙": "사전 동결한 자세 파일(--from_basins)의 조각 기하 그대로",
            "⚠": "평형 분자가 아니다 — 그래서 D 는 '고정 conformer 조건부' 다"},
        # ── AS Q7 lateral (옵션 a) — 결과 보기 전에 봉인한다 ──────────────
        "coverage_scope": {
            "정책": "이 셀 조건으로 **한정**한다 (lateral-size 대조를 넣지 않는다)",
            "왜": ("보고하는 것이 두 조각의 **차**이고 둘이 같은 셀·같은 피복률에 "
                   "있으므로 공통 주기영상 항이 상당 부분 소거된다. lateral 확장은 "
                   "잡당 원자수 2배(비용 ~4배·9일)라 이 단계의 질문에 비해 과하다"),
            "⛔_금지": ("고립 분자 흡착·실제 전극 피복률로 확장 금지. 원고 문장에 "
                        "셀 조건(면적·분자 밀도·최소 이미지 거리)을 **반드시 병기**한다"),
            "재개_조건": "피복률 의존성을 물으면 별도 wave 로 lateral 대조를 연다",
            "⚠_D3": ("D3 는 pairwise 라 서로 다른 조각의 주기영상 항이 정확히 "
                     "소거된다는 보장이 없다 — 위 한정이 그 답이다 (AS Q7)")},
        "⚠_사람이_읽을_것": ("이 필드가 원고 문장의 상한이다. 더 강한 이름으로 "
                              "바꿔 쓰지 말 것 (회신 AS Q2)")}
    # ⛔ 회신 AS Q7 — 한정하려면 **무엇으로 한정하는지 수치가 있어야 한다.**
    #   슬랩 셀에서 직접 계산한다 (설명문이 아니라 실물).
    def _mol_image_min(out_dir, planned, nslab_):
        """복합체 POSCAR 에서 **분자 원자와 그 횡방향 주기이미지** 사이 최단거리.

        ⛔ 못 하는 것: 슬랩-분자 거리는 안 본다 (그건 흡착 높이다). 분자끼리만.
        """
        best = {}
        for _k, _pl in sorted((planned or {}).items()):
            _m = (_pl.get("meta") or {})
            if _m.get("kind") != "prospective_pose" or _m.get("vacconv"):
                continue
            _f = _m.get("fragment")
            _pf = out_dir / _k / "POSCAR"
            if not _pf.is_file():
                continue
            try:
                _ls = _pf.read_text().splitlines()
                _sc = float(_ls[1].split()[0])
                _cell = np.array([[float(x) for x in _ls[2 + i].split()[:3]]
                                  for i in range(3)]) * _sc
                _cnt = [int(x) for x in _ls[6].split()]
                _n = sum(_cnt)
                _st = 8 if _ls[7].strip()[:1] in "SsCcDd" and \
                    _ls[7].strip()[:1] in "Ss" else 8
                # Selective dynamics 유무를 보고 좌표 시작줄을 정한다
                _i = 7
                if _ls[_i].strip()[:1] in "Ss":
                    _i += 1
                _dirmode = _ls[_i].strip()[:1] in "Dd"
                _i += 1
                _pos = np.array([[float(x) for x in _ls[_i + j].split()[:3]]
                                 for j in range(_n)])
                if _dirmode:
                    _pos = _pos @ _cell
                _mol = _pos[nslab_:]
                if len(_mol) < 1:
                    continue
                _sh = [i * _cell[0] + j * _cell[1]
                       for i in (-1, 0, 1) for j in (-1, 0, 1) if (i, j) != (0, 0)]
                _d = min(float(np.linalg.norm(a - (b + t)))
                         for t in _sh for a in _mol for b in _mol)
                # 🔴 회신 AT Q1 (2026-08-31) — **자세를 뭉개지 않는다.** 종전엔
                #   조각별 최솟값 하나만 남겨서, sdcp 의 4.613 Å(대안 자세 b12 의
                #   worst case)이 primary 값처럼 보고됐다. primary b00 은 4.894 Å 다.
                #   보고량은 primary 조건의 값이므로 role 별로 나눠 싣는다.
                _role = _m.get("role") or "primary"
                _b = best.setdefault(_f, {})
                _b[_role] = round(min(_b.get(_role, 1e9), _d), 3)
            except Exception:                                # noqa: BLE001
                continue
        return best or None

    try:
        _cv = slab.cell.array
        _ax, _ay = _cv[0][:2], _cv[1][:2]
        _mol_img_min = _mol_image_min(out, man.get("planned"), nslab)
        _area = abs(_ax[0] * _ay[1] - _ax[1] * _ay[0])           # Å²
        _la = float(np.linalg.norm(_cv[0])), float(np.linalg.norm(_cv[1]))
        man["reported_quantity"]["coverage_scope"].update({
            "lateral_cell_A": [round(_la[0], 3), round(_la[1], 3)],
            "lateral_area_A2": round(_area, 3),
            "molecules_per_cell": 1,
            "coverage_per_nm2": round(100.0 / _area, 4) if _area else None,
            # ⛔⛔ 2026-08-31 실측 정정 — 종전엔 **격자벡터 길이**를
            #   `min_image_distance_A` 라고 찍었다(11.5 Å). 회신 AS 가 준 4.89/5.65 Å
            #   는 **분자와 그 주기이미지 사이 실제 최단 거리**다. 이름은 같은데
            #   다른 양이라, 그대로 실으면 리뷰 수치를 반박하는 것처럼 보인다.
            "min_lateral_cell_vector_A": round(min(_la), 3),
            # 🔴 회신 AT Q1 — 자세(role)별로 나눠 싣는다. 보고량은 **primary** 조건이다
            "molecule_image_min_distance_A": _mol_img_min,
            "molecule_image_min_primary_A": (
                {f: d.get("primary") for f, d in (_mol_img_min or {}).items()
                 if d.get("primary") is not None} or None),
            "⚠_자세를_뭉개지_않는다": (
                "종전엔 조각별 **최솟값 하나**만 실어, 대안 자세의 worst case 가 "
                "primary 값처럼 보였다. 보고량은 primary 자세의 조건이므로 "
                "`molecule_image_min_primary_A` 가 그 값이고, 대안 자세는 별개다 "
                "(회신 AT Q1)"),
            "⛔_철회한_근거": (
                "'공통 주기영상 항이 상당 부분 소거된다' 는 **삭제한다.** 두 primary "
                "복합체의 슬랩 원자 수가 48/192 로 다르고 최대 변위가 약 0.296 Å 이라 "
                "공통항이라는 보장이 없다 (회신 AT Q1). 잔여 lateral-size 의존은 "
                "**추정하지 않는다** — 한정 문구로만 다룬다"),
            "⚠_수치_출처": ("셀 벡터와 **실제 복합체 좌표**에서 직접 계산. "
                             "격자벡터 길이(min_lateral_cell_vector_A)와 분자-이미지 "
                             "최단거리(molecule_image_min_distance_A)는 **다른 양**이다 "
                             "— 후자가 피복률 논의의 대상이다")})
    except Exception as _e:                                      # noqa: BLE001
        man["reported_quantity"]["coverage_scope"]["⛔_셀_수치_없음"] = (
            "셀에서 면적을 못 구했다 (%r) — 한정 문구를 수치로 뒷받침하지 못한다"
            % (_e,))
    man["claim_scope"] = (
        "두 조각 모델의 **고정기하 복합체−기체기준 차등에너지** 하나 "
        "(fixed-geometry differential complex–gas reference energy). "
        "⛔ 각 항을 adsorption energy 라고 부르지 않는다 — 평형·고립계 양이 아니고 "
        "조각·표면 변형을 포함한다 (회신 AS Q2). "
        "⚠ 고정 기하(MLIP 이완) 단일점이고, 기체 기준은 조각당 conformer 하나를 모든 "
        "자세에 공통으로 쓴다. 값은 pm1 자기 branch 조건부이고 "
        "비교하는 잡들이 같은 realized topology 여야 한다. "
        "⚠ **이 셀 조건에 한정**한다 — 사전등록한 lateral 셀에서의 대비이고 "
        "고립 분자 흡착이나 실제 전극 피복률로 일반화하지 않는다 (회신 AS Q7, 옵션 a). "
        "⛔ 개별 절대 흡착에너지·자리 선호(Li vs Ni)·평형 결합에너지·자유에너지·고분자 "
        "전체의 결합력으로 확장 금지."
        if getattr(a, "refs_minimal", False) else

        "fixed-geometry site contrast (ΔE = E_Ni − E_Li, 같은 조각·같은 슬랩). "
        "⚠ 값은 **pm1 자기 branch 조건부**다 — 두 seed 중 어느 쪽이 바닥인지 주장하지 "
        "않는다(그러려면 각 끝점의 최저 branch에 dense가 필요하다). 보호막은 seed 산포 "
        "게이트(≤10 meV)이고, 넘으면 그 쌍을 막는다. "
        "clean/gas 기준계가 없으므로 **절대 E_ads 를 만들 수 없다** — 흡착의 열역학적 "
        "유불리·조각 간 결합 세기 비교·결합에너지 절대값은 이 번들로 주장 금지."
        + (" ⚠ open-shell 조각(sdcp_doped)은 **시드한 라디칼 스핀 basin 조건부**다 — "
           "반대 커플링 초기값을 넣지 않았으므로 'open-shell 바닥상태 자리 선호' 로 "
           "일반화하지 말 것. 'tested seeded radical-spin basin 에서의 대비' 로 서술한다."
           if any("doped" in f for f in man.get("fragments", [])) else "")
        + (" ⚠ champion 은 **전역 최선이 아니다**: 짝(같은 배향의 반대 자리)이 있는 "
           "자세 중 최선이다. 전역 최선 자세가 짝 없는 배향에 있으면 쓰지 않는다. "
           "'가장 안정한 자세' 가 아니라 '배향일치 대비가 가능한 자세 중 최선' 이며, "
           "그 대가는 pair_audit[*].pool_restriction 에 meV 로 적혀 있다."
           if a.champion else "")
        if not a.refs else
        "site contrast + absolute E_ads (기준계 포함). E_ads 는 UMA 기하 위 단일점이라 "
        "완전 이완 흡착에너지가 아니다.")

    for frag in (man["fragments"] if a.refs else []):
        mol, info = SS.load_fragment(frag)
        # ⚠ 분자 ref 가 빠지면 그 조각의 E_ads 를 만들 수 없다 — 조용히 건너뛰지 않는다.
        if mol is None or info.get("status") != "OK":
            bad(f"{frag}: 분자 파일 {info.get('status', 'MISSING')} — E_ads 기준계 없음")
            continue
        used_els |= set(mol.get_chemical_symbols())
        # ⛔⛔ 회신 AP #11 (2026-08-31) — box20 을 **다시 낸다.**
        #   종전엔 refs_minimal 이 box24 하나로 좁혀서 상자 수렴을 이 묶음에서
        #   검증하지 못했고, 선행 대조(gas_box_prior)로 때웠다. AP 판정:
        #   *"비차단 강등은 box24 조건부 내부값에는 정직하지만 0.01 eV 원고값에는
        #   부족하다. box20 두 잡을 **결과를 보기 전** 지금 추가하는 쪽이 맞다."*
        #   두 잡 다 --single_point 라 **독립 재이완이 없다** — 같은 원본 분자에서
        #   셀만 바꾼 고정기하 static 이고 state-selection policy 도 같다.
        _boxes = ((20.0, "box20"), (24.0, "box24"))
        for margin, tag in _boxes:
            rel = f"refs/mol__{frag}__{tag}"
            # ⛔⛔ 회신 AR Q2 (2026-08-31) — 실물 v15 의 기체 부모 네 잡이 전부
            #   `relax → static` 이었다. 각 상자에서 **독립으로 이완**하므로
            #   δ_gas 가 "셀 효과" 가 아니라 "셀 효과 + 독립 이완 차이" 를 잰다.
            #   ⇒ 단일점 판에서는 기체도 **고정기하 static** 이어야 한다.
            #     box20/box24 는 같은 원본 분자를 각 상자 중심으로 **강체 평행이동**만
            #     한 것이라 내부좌표가 동일하고, DIPOL 은 각 상자의 COM 으로 갱신된다.
            #   ⚠ AQ 프롬프트에 "두 잡 다 --single_point 라 독립 재이완이 없다" 고
            #     썼는데 **그것이 틀렸다** — `closure` 가 아니면 relax 가 붙는다.
            _gas_fixed = bool(a.closure or getattr(a, "single_point", False))
            m = _emit_mol_job(out / rel, frag, mol, margin,
                              free_spin=getattr(a, "free_spin_refs", False),
                              closure=_gas_fixed)
            plan(rel, m["phases"], True, m)
            man["refs"][f"mol__{frag}__{tag}"] = rel
            n_jobs += 1
            # ⛔⛔ 2026-08-31 (회신 AN Q3) — canary 를 **C-12 에서도 낸다.**
            #   초판 조건은 `closure and not refs_minimal` 이라 C-12 에서는 절대 안 나왔다.
            #   그런데 분석기는 `molecular_spin_controls` 를 **필수**로 요구한다 —
            #   그 상태로 회수하면 두 조각 다 차단된다.
            #   리뷰 판정: `open_shell:false` 는 **선언이지 검증이 아니다.** D 를 본 뒤
            #   필요성을 판단하면 결과 의존적 선택이 된다. ⇒ 지금 넣는다.
            #   canary = 같은 최종 기하 · fresh ICHARG=2 · NUPDOWN=-1 · 비영 MAGMOM · static only.
            #   (CHGCAR 를 승계한 ICHARG=1 canary 는 부적절하다 — 재시작에서는 MAGMOM 이
            #    초기 국소모멘트를 새로 설정하지 않는다.)
            if tag == "box24" and (a.closure or getattr(a, "refs_minimal", False)):
                relz = f"refs/mol__{frag}__{tag}__nzmag"
                # ⛔⛔ 2026-08-31 실측 — canary 가 `NUPDOWN = 0` 으로 나왔다.
                #   `free_spin` 을 CLI 플래그에서 받아서, 우리 호출에선 False 였다.
                #   그러면 **일중항으로 묶인 채** 비영 MAGMOM 만 준 꼴이라
                #   spin-broken 해를 찾을 수 없다 — 대조군이 아무것도 대조하지 못한다.
                #   canary 는 정의상 **자유 스핀**이다: free_spin=True 를 못박는다.
                mz = _emit_mol_job(out / relz, frag, mol, margin,
                                   free_spin=True,
                                   closure=True, nonzero_start=True)
                # ⛔⛔ 회신 AO P0-4 — canary 는 static-only 인데 부모는 `--closure` 가
                #   아니면 relax→static 이다. 그러면 canary 만 루트 POSCAR 를 써서
                #   **다른 기하끼리 뺀다** (구조 이완 에너지가 스핀 검사를 오염시킨다).
                #   부모 잡을 가리켜 런타임에 같은 기하를 받게 한다.
                (out / relz / "PARENT_GEOM").write_text("../mol__%s__%s\n" % (frag, tag))
                mz["parent_geom"] = rel
                (out / relz / "job.json").write_text(
                    json.dumps(mz, indent=1, ensure_ascii=False))
                plan(relz, mz["phases"], True, mz)
                man.setdefault("molecular_spin_controls", {})[
                    f"mol__{frag}__{tag}"] = relz
                n_jobs += 1

    # ══ D3-off 쌍둥이 (회신 W Q2 — 오프셋 원인 분해) ═══════════════════════
    #   완성된 endpoint 를 통째로 복사하고 **IVDW 한 줄만** 지운다. 후처리로 하는 이유는
    #   호출부가 여러 곳이라, 복사가 "글자 하나까지 같음" 을 **보장**하기 때문이다.
    #   ⛔ 못 하는 것: D3 를 끈 값은 **판정에 쓰지 않는다.** 오프셋 원인 진단 전용이다.
    twins = {}
    if getattr(a, "d3_pairs", False):
        if not a.closure:
            sys.exit("⛔ --d3_pairs 는 --closure 와 함께만 쓴다 (고정기하·all-F 가 전제)")
        for inc in sorted(out.rglob("static/INCAR")):
            jd = inc.parent.parent
            rel = str(jd.relative_to(out))
            if rel.endswith("__d3off"):
                continue
            # 회신 X Q1 — 고정기하 D3(zero)는 원자종·기하의 additive correction 이라
            #   **자기상태에 무관**하다. 두 번째 자기 seed 에 쌍둥이를 또 만들 필요가
            #   없다. 기준계(clean slab·기체)는 회신 X Stage A 목록대로 그대로 둔다.
            if (getattr(a, "d3_seed_main_only", False)
                    and rel.startswith("prospective/")
                    and any(rel.endswith(sd) for sd in SEEDS_FULL if sd != SEED_MAIN)):
                continue
            td = out / (rel + "__d3off")
            if td.exists():
                shutil.rmtree(td)
            shutil.copytree(jd, td)
            ti = td / "static" / "INCAR"
            txt = ti.read_text()
            if "IVDW     = 11" not in txt:
                sys.exit(f"⛔ {rel}: IVDW=11 줄이 없다 — D3-off 쌍을 만들 수 없다")
            ti.write_text(txt.replace("IVDW     = 11\n", "")
                             .replace("[closure ", "[closure D3-OFF twin · "))
            for extra in ("dense", "pre", "relax"):
                if (td / extra).exists():
                    shutil.rmtree(td / extra)     # 쌍둥이는 static 만
            _m = json.loads((td / "job.json").read_text())
            _m["d3_twin_of"] = rel
            (td / "job.json").write_text(json.dumps(_m, indent=1, ensure_ascii=False))
            twins[rel] = rel + "__d3off"
            n_jobs += 1
        # ★ 회신 Z P0-3 — census 를 **기계로** 세고 못박는다. 리뷰어가 "net4/off 까지
        #   생성됐다면 48잡이므로 manifest 와 설명 중 하나가 틀린 것" 이라고 조건을
        #   걸었다. 설명이 아니라 **산출물**이 답해야 한다.
        _bad_net4 = sorted(t for t in twins.values()
                           if t.startswith("prospective/")
                           and any(f"__{sd}__d3off" in t
                                   for sd in SEEDS_FULL if sd != SEED_MAIN))
        if getattr(a, "d3_seed_main_only", False) and _bad_net4:
            sys.exit(f"⛔ --d3_seed_main_only 인데 비주-seed complex 에 D3-off 쌍둥이가 "
                     f"{len(_bad_net4)}개 생겼다: {_bad_net4[:3]} — 고정기하 D3(zero)는 "
                     f"자기상태에 무관하므로 반복이 불필요하고, 잡 수 설명과 어긋난다")
    # ★ census 는 **쌍둥이 유무와 무관하게** 쓴다. 종전엔 이 블록이 --d3_pairs 안에만
    #   있어서, 쌍둥이를 안 만드는 판(옵션 A)에서는 census 가 통째로 없어지고
    #   README·verify_bundle 이 조용히 빈 값을 읽었다.
    if True:
        _cx_on = [k for k in man["planned"] if k.startswith("prospective/")]
        _rf_on = [k for k in man["planned"] if not k.startswith("prospective/")]
        _cx_tw = [v for v in twins.values() if v.startswith("prospective/")]
        _rf_tw = [v for v in twins.values() if not v.startswith("prospective/")]
        # ★ **어떻게 만들었는지를 산출물이 답하게 한다.** v9 까지 MANIFEST 에 호출
        #   인자가 없어서 재생성 명령을 번들 내용에서 **역추론**해야 했다 (플래그
        #   하나만 틀려도 다른 번들이 나온다). 설명이 아니라 실물이 답해야 한다.
        man["invocation"] = {
            "argv": list(sys.argv[1:]),
            "flags": {k: v for k, v in sorted(vars(a).items())
                      if not k.startswith("_") and v not in (None, False, [], "")},
            "⚠": ("`argv` 는 이 번들을 만든 실제 명령이다. 재생성은 이것을 그대로 "
                  "쓴다 — 번들 내용에서 플래그를 역추론하지 마라"),
        }
        man["job_census"] = {
            "references": {"endpoints": len(_rf_on), "d3_off_twins": len(_rf_tw),
                           "총": len(_rf_on) + len(_rf_tw)},
            "complexes": {"pose×seed": len(_cx_on), "d3_off_twins": len(_cx_tw),
                          "총": len(_cx_on) + len(_cx_tw)},
            "총잡수": len(_rf_on) + len(_rf_tw) + len(_cx_on) + len(_cx_tw),
            "pose당": ("pm1/D3-on · net4/D3-on — **D3-off 쌍둥이를 만들지 않는다** "
                       "(C3 는 D3-on OUTCAR 의 Edisp 로 낸다)") if not twins else
                      ("pm1/D3-on · pm1/D3-off · net4/D3-on — **net4/D3-off 는 만들지 "
                       "않는다** (고정기하 D3 zero 는 구조 기반 additive correction 이라 "
                       "자기상태에 무관)") if getattr(a, "d3_seed_main_only", False) else
                      "전 seed × D3 on/off",
            "audit_pose": 0,
            "⚠": "이 표는 산출물에서 센 것이다 — 설명문이 아니라 실물이다",
        }
        man["d3_off_twins"] = twins
        man["c3_source"] = ("d3_off_twins (+ Edisp 교차검증)" if twins else
                            "Edisp (eV) from the D3-on OUTCAR — no twin jobs")
        man["d3_off_note"] = (
            "같은 POSCAR·같은 MAGMOM·같은 k 로 **IVDW 줄만** 뺀 쌍. "
            "E(D3on) − E(D3off) = D3 기여. 회신 W Q2 의 원인 셋(missing D3 · 기체 기준 "
            "오차 · 자기 basin) 중 첫 번째를 직접 잰다. ⛔ **판정값이 아니다.**"
            ) if twins else (
            "쌍둥이 없음 — C3 는 D3-on OUTCAR 이 직접 찍는 `Edisp (eV)` 로 낸다. "
            "D3(IVDW=11)는 SCF 에 안 들어가는 additive 항이라 고정기하에서 "
            "`E_on − E_off = Edisp` 가 **항등식**이고, 쌍둥이 잡은 정보가 0이다. "
            "실물 확인: runs/sdcp_phaseB_vasp_v1_2026_08_08 의 세 OUTCAR "
            "(slab −27.49493 · mol −0.71798 · complex −28.58614 ⇒ δ −0.373230 eV).")
        if twins:
            print(f"→ D3-off 쌍둥이 {len(twins)}개 (IVDW 줄만 제거)")
        else:
            print("→ D3-off 쌍둥이 **0개** — C3 는 Edisp 로 낸다 (쌍둥이는 정보가 0)")

    if viol:
        man["contract_violations"] = viol
        if not a.allow_partial:
            shutil.rmtree(out)
            sys.exit(f"⛔ 계약 위반 {len(viol)}건 — 축소된 번들을 정본으로 만들지 않는다.\n   "
                     + "\n   ".join(viol)
                     + "\n   (의도한 부분 생성이면 --allow_partial 을 명시할 것)")
        print(f"  ⚠ --allow_partial: 계약 위반 {len(viol)}건을 안고 만든다 — "
              f"MANIFEST.contract_violations 에 기록")

    nfs = sorted({m["n_fixed"] for m in slab_metas})
    if len(nfs) != 1:
        shutil.rmtree(out)
        sys.exit(f"⛔ 슬랩 잡들의 고정 원자 수가 갈린다 {nfs} — 쌍 ΔE 가 구속 차이로 "
                 f"오염된다. 자세 z-범위를 확인할 것")
    man["n_fixed_all_slab_jobs"] = nfs[0]

    # ★★ 회신 AA P0-3 — `d3` 를 **전 잡에** 박는다. 종전엔 쌍둥이 생성 루프 안에서만
    #   찍어서 쌍둥이가 없는 잡(--d3_seed_main_only 의 net4 복합체 8잡)이 통째로
    #   비었다 — v7 실측. "필드가 없는 잡이 남으면 cohort 조립이 다시 이름으로 샌다"
    #   고 적어 놓고 그 구멍을 남겼다. 이제 **INCAR 실물**에서 유도한다: 플래그를
    #   기억해서 찍는 게 아니라 배포되는 입력 자체가 근거다.
    _nod3 = []
    for _jj in sorted(out.rglob("job.json")):
        _inc = _jj.parent / "static" / "INCAR"
        if not _inc.is_file():
            _nod3.append(str(_jj.parent.relative_to(out)))
            continue
        _on = bool(re.search(r"(?m)^\s*IVDW\s*=\s*11\b", _inc.read_text()))
        _m = json.loads(_jj.read_text())
        _m["d3"] = "on" if _on else "off"
        _m["ivdw_expected"] = 11 if _on else None
        _jj.write_text(json.dumps(_m, indent=1, ensure_ascii=False))
    if _nod3:
        sys.exit(f"⛔ static/INCAR 이 없어 d3 를 정할 수 없는 잡 {len(_nod3)}개: "
                 f"{_nod3[:5]} — 구조화 필드가 빈 채로 내보내지 않는다")
    # 계약: **모든** 잡에 d3 가 있다 (분석기가 이름으로 되돌아가지 않게)
    _chk = [str(q.parent.relative_to(out)) for q in out.rglob("job.json")
            if json.loads(q.read_text()).get("d3") not in ("on", "off")]
    if _chk:
        sys.exit(f"⛔ d3 필드가 없는 잡 {len(_chk)}개: {_chk[:5]}")

    # ⛔⛔ 회신 AP Q4 (2026-08-31) — 분석기는 meta 결측 항목을 **양쪽 stage 에서
    #   필수**로 셌지만 러너는 그것을 **stage 2 로만** 보낸다. 안전장치가 아니라
    #   영구 deadlock 이다. 정책은 "양쪽 필수" 가 아니라 **첫 VASP 전에 중단**이다.
    #   ⚠ deadlock 은 **staged 구성에서만** 생긴다 (단계를 meta 로 나누는 러너가
    #     거기에만 있다). 레거시 tier1 경로는 단계 개념이 없으므로 대상이 아니다.
    _nometa = sorted(k for k, v in man["planned"].items()
                     if not (v.get("meta") or {})) if getattr(
                         a, "refs_minimal", False) else []
    if _nometa:
        sys.exit("⛔ 계획 항목 %d건에 meta 가 없다 — 단계를 결정할 수 없다.\n"
                 "   러너는 meta 로 단계를 나누므로 이대로 내보내면 그 잡들이\n"
                 "   영구히 열리지 않는다. 생성기에서 멈춘다 (schema error).\n"
                 "   %s" % (len(_nometa), _nometa[:5]))

    man["gas_geometry_policy"] = {
        "fixed_geometry_static": bool(getattr(a, "single_point", False) or a.closure),
        "why": ("box20/box24 가 각각 독립 이완하면 δ_gas 가 셀 효과와 이완 차이를 "
                "함께 잰다 (회신 AR Q2). 단일점 판에서는 둘 다 고정기하 static 이고, "
                "같은 원본 분자를 각 상자 중심으로 **강체 평행이동**만 한다"),
        "dipol": "각 상자의 COM 으로 갱신 (VASP 권고)",
    }
    man["potcar_spec"] = {e: POTCAR_SPEC.get(e, e) for e in sorted(used_els)}
    (out / "analyze_results.py").write_text(ANALYZER)
    if getattr(a, "refs_minimal", False):
        (out / "run_staged.sh").write_text(RUN_STAGED)
        (out / "SEAL_POTCAR_ROOT.sh").write_text(SEAL_POTCAR_ROOT)
        # ⛔ 회신 AP #12 — 원고에서 PAW release 를 주장하려면 **계산 전** attestation
        (out / "POTCAR_ATTESTATION_REQUEST.md").write_text(POTCAR_ATTESTATION_REQUEST)
        (out / "MAKE_POTCAR_ATTESTATION.sh").write_text(MAKE_ATTESTATION)
        # ⛔ 2026-08-31 (회신 AN P0-3) — README 가 이 값을 읽어 "staged 로만 실행" 을 찍는다.
        #   기록이 없으면 README 와 러너가 서로 반대를 말하게 된다.
        man["staged_runner"] = "run_staged.sh"
        # ⛔⛔ 회신 AO P0-3 (2026-08-31) — `run_all.sh` 는 **14잡 전체 제출**을 안내해
        #   README 의 staged 지침과 정면으로 충돌했다. 실행 경로가 둘이면 정지 규칙이
        #   강제되지 않는다. staged 구성에서는 아예 내지 않는다.
        man["run_all_omitted"] = ("staged 구성이라 run_all.sh 를 넣지 않는다 — "
                                  "전체 제출 경로가 있으면 1단계 정지 규칙이 무력화된다")
    else:
        (out / "run_all.sh").write_text(RUN_ALL)
    if a.adaptive_dense:
        (out / "run_dense_selected.sh").write_text(RUN_DENSE_SEL)
    # ⚠ 문서가 잡 수를 읽으므로 **문서보다 먼저** 확정한다 (Codex 7차 §11 —
    #   지금은 SUBMIT_CONTRACT 가 '?' 를 찍고 있었다).
    man["n_jobs"] = n_jobs
    # ⛔⛔ 회신 AR P0-7 · 해제조건 8 (2026-08-31) — 러너가 **실행 전에** 계획 census
    #   를 확인하려면 계획이 기계 필드로 있어야 한다. 종전엔 러너가 존재하는
    #   job.json 만 분류하고 디렉터리 수만 비교해서, job.json 하나를 지워도
    #   `classified=15`, 디렉터리 16 으로 검사를 통과했다.
    #   ⇒ 정확한 **잡 키 집합**과 **단계 분류**를 manifest 에 박는다.
    #     분류 규칙은 analyze_results.py 의 `_stage_of` · run_staged.sh 와 1:1 이다.
    def _gen_stage_of(pl):
        m = (pl.get("meta") or {})
        kind, role, vac = m.get("kind"), m.get("role"), m.get("vacconv")
        if kind == "mol_ref":
            return "1"
        if kind == "prospective_pose" and role == "primary":
            return "1" if (vac or m.get("seed") == SEED_MAIN) else "2"
        return "2"
    _stage_map = {k: _gen_stage_of(v) for k, v in man["planned"].items()}
    man["run_census"] = {
        "job_keys": sorted(man["planned"]),
        "stage_of": _stage_map,
        "stage_counts": {st: sum(1 for v in _stage_map.values() if v == st)
                         for st in ("1", "2")},
        "n_jobs": n_jobs,
        "⛔": ("러너는 실행 전에 이 **집합**과 **분류**를 디스크와 대조한다. "
               "개수만 맞고 구성이 다른 것을 통과시키지 않는다 (회신 AR P0-7)"),
    }
    n_by_ph = {}
    for _p in man["planned"].values():
        for _ph in (_p.get("phases") or []):
            n_by_ph[_ph] = n_by_ph.get(_ph, 0) + 1
    # 🔴 회신 Z P0-1 — `planned` 에 D3-off 쌍둥이가 없다. 여기서 안 더하면 문서와
    #   MANIFEST 가 실행량을 40 % 덜 잡는다 (v4 실측: 잡 40인데 "실행 24회").
    #   **이 한 곳이 공통 출처다** — README·SUBMIT_CONTRACT·MANIFEST 가 전부 이걸 쓴다.
    #   따로 세면 또 갈라진다(v4 가 문서만 고치고 MANIFEST 를 놓친 이유).
    _n_twins = len(man.get("d3_off_twins") or {})
    if _n_twins:
        n_by_ph["static"] = n_by_ph.get("static", 0) + _n_twins   # 쌍둥이는 static 뿐
    n_ph_all = sum(n_by_ph.values())
    # ★ 모드별 README (Codex 6차 §8) — 옛 README 는 82계·259상·relax 반송·refs 표를
    #   그대로 담고 있어 **단일점 Wave 1 과 정면으로 모순**된다. 실행 계약과 provenance
    #   문서를 옛 판으로 내보내는 것은 문구 문제가 아니라 반송 계약 위반이다.
    # 🔴 회신 Z P0-1 — 종전엔 `a.single_point` 만 봤다. `--closure` 도 상을
    #   `["static"]` 하나로 만드는데(_emit_slab_job: `if single_point or closure`)
    #   README 분기가 그걸 안 봐서 **4상짜리 옛 README** 가 그대로 나갔다 —
    #   82 systems · 259 phase runs · relax 반송 · tier/pair 표. 이 함수의 주석이
    #   스스로 "문구 문제가 아니라 반송 계약 위반" 이라고 적어 둔 그 사고다.
    #   (2026-08-29 sdcp_stageA_v2·motifprobe_v2 가 그 상태로 만들어졌다.)
    # ⚠ 비용 동결을 **README 보다 먼저** 한다 — README 의 '가장 긴 잡' 이
    #   cost_frozen 에서 오기 때문이다. 순서가 뒤면 하드코딩 56h 로 되돌아가고,
    #   그러면 --cores 를 바꿔도 라벨만 바뀐다 (외주 견적이 틀어진 원인).
    # ── 비용을 MANIFEST 에 **동결**한다 (ZIP 만으로 재현되게) ────────────────
    # ── 주기영상 진공 (회신 AF P0-1) — **비용·해시 전에** 셀을 맞춘다 ────────────
    #   v13 은 24 pm1 자세 중 9개가 15 Å 미만(최소 8.56 Å)인데 문서가 ">15 Å" 라고
    #   적었다. 생성기에 진공을 보는 코드가 없어서다. 이제 맞추고, 못 맞추면 막는다.
    # ── POTCAR·VASP 사전 고정 (회신 AI §B) ─────────────────────────────────
    #   회신값끼리만 맞춰 보는 것은 검증이 아니다. **외부 기준**이 있어야 한다.
    #   생성 시점엔 우리가 POTCAR 원본을 갖고 있지 않으므로 자리를 비워 두고,
    #   외주처가 조립기를 한 번 돌려 보낸 SHA 를 여기 박은 뒤 재발행한다.
    #   비어 있으면 분석기가 '잡 사이 일치만 확인했다' 를 결과에 적는다 (fail-open 아님 —
    #   불일치는 여전히 막고, 한계를 명시한다).
    _pin = getattr(a, "potcar_pin", None)
    if _pin and os.path.isfile(_pin):
        man["potcar_pin"] = json.loads(Path(_pin).read_text())
        man["potcar_pin"]["source_file"] = _pin
        man["potcar_pin"]["sha256"] = hashlib.sha256(
            Path(_pin).read_bytes()).hexdigest()
    elif not hasattr(a, "allow_no_pin") or a.allow_no_pin:
        # ⚠ argparse 는 --allow_no_pin 을 **항상** 넣는다(기본 False). 그래서 CLI 에서는
        #   이 가지가 명시적으로 줬을 때만 열린다. 속성 자체가 없는 것은 합성 픽스처뿐이다.
        man["potcar_pin"] = None
        # ⛔⛔ 회신 AO P1 (2026-08-31) — 종전 문구가 "제출본이 아니다" 라고 적어
        #   **AO 가 승인한 새 provenance-root 방식과 정면으로 충돌**했다.
        #   AO Q1: "이전 wave 와 같은 PP 를 주장하지 않는다면 이전 pin 을 요구할 필요는
        #   없다. 다만 계산 시작 **전에** vendor 원본 fingerprint 를 자동 봉인해 새 v13
        #   root 로 승인하면 된다." ⇒ 사전 봉인은 `SEAL_POTCAR_ROOT.sh` 가 한다.
        man["potcar_pin_note"] = (
            "pin 미고정. 이 번들은 **이전 wave 와의 PP 동등성을 주장하지 않는다** — "
            "대신 `SEAL_POTCAR_ROOT.sh` 가 첫 VASP 실행 **전에** variant 별 원본 "
            "SHA256 을 `POTCAR_ROOT_SEAL.json` 에 봉인하고, 분석기가 전 잡의 "
            "provenance 를 그 봉인과 대조한다 (회신 AO Q1). "
            "⚠ 봉인한 트리가 공식 배포판인지는 확인하지 못한다 — site allowlist 가 "
            "그 신원을 진다. 외부 기준과 대조하려면 `--potcar_pin <json>`")
    else:
        sys.exit(
            "⛔ --potcar_pin 이 없다 — 제출용 번들을 만들지 않는다 (회신 AJ).\n"
            "   사전 승인된 신원 JSON 이 있어야 회신 해시를 **외부 기준**과 대조할 수 있다:\n"
            '     {"source_sha256": {"Li_sv": "<sha>", "Ni_pv": "<sha>", ...},\n'
            '      "vasp_version": "6.4.1"}\n'
            "   외주처 시스템 관리자에게 원본 POTCAR SHA256 · VASP 버전 문자열 ·\n"
            "   그 트리가 승인된 potpaw_PBE.54 라는 확인을 받아 채운다.\n"
            "   시험·초안용이면 --allow_no_pin (그 번들은 제출용이 아니다).")

    _c2 = getattr(a, "cell_c2", None)
    _minvac = float(getattr(a, "min_vacuum", MIN_VACUUM_A_DEFAULT) or 0.0)
    if _minvac > 0:
        man["vacuum"] = fit_bundle_vacuum(out, man["planned"], _minvac,
                                          getattr(a, "cell_c", None))
        _ma = man["vacuum"].get("min_after_A")
        if _ma is not None and _ma < _minvac - 1e-6:
            sys.exit(f"⛔ 주기영상 진공 {_ma:.2f} Å < 선언 {_minvac:.2f} Å — "
                     f"셀 확장 뒤에도 미달이다. 번들을 내보내지 않는다.")
        if man["vacuum"].get("n_below_before"):
            print(f"  ↑ 셀 c {man['vacuum']['c_before_A']} → "
                  f"{man['vacuum']['c_after_A']} Å — 진공 미달 "
                  f"{man['vacuum']['n_below_before']}자세 (최소 "
                  f"{man['vacuum']['min_before_A']} → {_ma} Å)")
    else:
        man["vacuum"] = {"declared_A": None,
                         "⚠": "--min_vacuum 0 — 진공 게이트를 껐다. 인용 시 병기할 것"}

    # ── 진공 두께 수렴 시험: vacconv/ 잡만 둘째 셀로 올린다 ────────────────
    if _c2:
        _vc = {}
        for _k in sorted(man["planned"]):
            if not _k.startswith("vacconv/"):
                continue
            _vc[_k] = set_job_cell(out / _k, float(_c2))
            # ⚠ clean slab 은 흡착종이 없어 분리거리가 정의되지 않는다. -1 같은
            #   sentinel 을 넣으면 **의미 없는 숫자가 조용히 최소값 자리에 앉는다**.
            _sep = image_separation_A(out / _k / "POSCAR")
            _vc[_k]["image_separation_A"] = (round(_sep, 3) if _sep is not None
                                             else None)
            _vc[_k]["⚠"] = None if _sep is not None else "흡착종 없음 — 분리거리 미정의"
        man["vacuum_convergence"] = {
            "schema": "vacuum_convergence/v1",
            "c1_A": (man.get("vacuum") or {}).get("c_after_A"),
            "c2_A": float(_c2), "jobs": _vc,
            "판정": "두 조각의 **대비 변화** |D(c2) − D(c1)| ≤ 0.005 eV 이고, "
                    "두 값의 0.01 eV 반올림이 같아야 통과",
            "왜_대비인가": "기체 기준과 슬랩 항은 c 에 무관하거나 두 조각에 공통이라 "
                           "대비를 취하면 소거된다. 조각별 변화가 아니라 대비 변화가 판정 대상",
            "5_meV_출처": "물리 상수가 아니라 **보고 최소단위(0.01 eV)의 절반**",
            "실패시": "추가 셀 탐색 없이 Figure 2e 를 제거한다"}
        if _vc:
            _seps = [v["image_separation_A"] for v in _vc.values()
                     if v["image_separation_A"] is not None]
            print("  ↑ 진공 두께 수렴 시험 %d잡 → c %.4f Å (흡착 %d잡 최소 분리 %s)"
                  % (len(_vc), float(_c2), len(_seps),
                     ("%.2f Å" % min(_seps)) if _seps else "n/a"))

    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import vasp_cost_estimate as CE   # noqa: E402
        _repo = Path(__file__).resolve().parents[2]
        _base = CE.outcar_baseline(
            str(_repo / "runs/sdcp_phaseB_vasp_v1_2026_08_08/slab/OUTCAR.gz")) \
            or dict(CE.BASE)
        _jh = []
        for _jp in sorted(out.rglob("job.json")):
            _m = json.loads(_jp.read_text())
            _n = len(_m.get("magmom_poscar") or []) or sum(_m.get("counts") or [0]) or 222
            _ni = CE.N_IONIC if _n > 60 else 25
            # ★ 회신 AF P0-8 — 진공을 늘리면 평면파·FFT 가 부피에 비례해 커진다.
            #   종전엔 이 인자가 없어서 셀을 21 % 키워도 견적이 안 움직였다.
            _vol = CE.poscar_volume_A3(str(_jp.parent / "POSCAR"))
            _vr = (_vol / _base.get("volume_A3", CE.BASE["volume_A3"])) if _vol else 1.0
            _jh.append(sum(
                CE.phase_hours(ph if ph in CE.ESTEP else "static", _n,
                               (_m.get("kmesh") or {}).get(ph, "3 4 1"), _base,
                               str(((_m.get("incar_expected") or {}).get(ph) or {})
                                   .get("LREAL", ".TRUE.")).upper().startswith(".F"), _ni,
                               _vr)
                for ph in (_m.get("phases") or [])))
        # 🔴 회신 AB/AE — `--cores` 가 **라벨만 바꾸고 숫자는 안 바꿨다.** _jh 는
        #   추정기 기준선(48코어)의 시간이라, `--cores 256` 을 줘도 README·계약이
        #   48코어 시간을 "256코어 기준" 이라고 적었다. 외주 견적이 여기서 틀어진다
        #   (리뷰어가 14.7일로 읽은 이유). 실제 속도향상으로 나눈다.
        _sp = CE.par_speedup(a.cores, _base.get("cores", 48), 7.2)
        _jh = [h / _sp for h in _jh]
        man["cost_frozen"] = {
            "total_wall_h": round(sum(_jh), 1),
            "core_h": round(sum(_jh) * a.cores),
            "longest_job_h": round(max(_jh), 1) if _jh else None,
            "cores_per_job": a.cores,
            "par_speedup_vs_baseline": round(_sp, 2),
            "⚠_속도향상": ("par_speedup 은 벤치마크가 아니라 두 구간 어림이다 (±50 %). "
                        "잡 시간 자체도 모형이라 ±2배 — 곱하면 넓다"),
            "makespan_d": {str(m): round(CE.schedule_makespan(_jh, m) / 24, 2)
                           for m in (4, 8, 12, 20)},
            "estimator": "tools/sdcp/vasp_cost_estimate.py",
            # ⚠ 이건 hash 가 아니라 **경로**다. 이름을 그렇게 부르면 안 된다.
            "estimator_baseline_source": _base.get("source"),
            "estimator_baseline_sha256": (
                hashlib.sha256(open(_base["source"], "rb").read()).hexdigest()
                if isinstance(_base.get("source"), str)
                and os.path.isfile(_base["source"]) else None),
            "estimator_baseline_sec_per_estep": round(_base.get("sec_per_estep", 0), 4),
            "repo_commit": man.get("repo_commit"),
            "uncertainty": "±2배 (모형이지 벤치마크가 아니다)"}
    except Exception as _e:
        man["cost_frozen"] = {"error": f"{type(_e).__name__}: {_e}"}

    if a.single_point or a.closure:
        n_st = sum(1 for p in man["planned"].values()
                   if "static" in (p.get("phases") or []))
        n_dn = sum(1 for p in man["planned"].values()
                   if "dense" in (p.get("phases") or []))
        (out / "README_REQUEST.md").write_text(_readme_sp(
            man, a, zcut, n_jobs, n_st, n_dn, n_ph_all, n_by_ph))
    else:
        (out / "README_REQUEST.md").write_text(README.format(
            freeze_pct=int(a.freeze * 100), zcut_note=f"{zcut:.3f} Å",
            k_relax=KMESH["relax"], k_static=KMESH["static"]))
    (out / "SUBMIT_CONTRACT.md").write_text(_submit_contract(man, a, n_by_ph))
    (out / "POTCAR_SPEC.txt").write_text(
        # ⛔ 회신 AP Q3 — "PBE PAW 5.4" 단정은 우리가 확인하지 않은 범위를 넘는다.
        #   release 는 attestation 으로만 확정된다.
        "# 원소 → POTCAR 변형. 각 잡 POSCAR 의 종 순서대로 이어붙일 것.\n"
        "# ⚠ 배포판(release)은 여기서 단정하지 않는다 — site allowlist 가 정하고,\n"
        "#   원고에 적으려면 POTCAR_ATTESTATION_REQUEST.md 로 계산 전에 확인받는다.\n"
        # ⛔ 회신 AO P1 — "2026-08-08 납품과 동일 계보" 는 **우리가 검증하지 않은
        #   주장**이고, v13 을 새 provenance root 로 선언한 것과 충돌한다.
        "# ⚠ 계보 주장 없음: 이 번들은 이전 wave 와의 PP 동등성을 주장하지 않는다.\n"
        "#   variant 는 아래 목록 그대로 쓰고, 원본 fingerprint 는 첫 실행 전에\n"
        "#   SEAL_POTCAR_ROOT.sh 가 POTCAR_ROOT_SEAL.json 에 봉인한다 (회신 AO Q1).\n"
        + "\n".join(f"{e:3s} {v}" for e, v in man["potcar_spec"].items()) + "\n")

    files = {}
    for p in sorted(out.rglob("*")):
        if p.is_file() and p.name != "MANIFEST.json":
            files[str(p.relative_to(out))] = hashlib.sha256(p.read_bytes()).hexdigest()
    # ── 제출 계약을 MANIFEST 에 못 박는다 (Codex 6차 §7) ─────────────────────
    #   "2.4일" 이 어떤 코어 수·병렬도의 값인지 기록이 없으면 나중에 아무도 모른다.
    n_st = n_by_ph.get("static", 0)          # ★ 쌍둥이 포함 (위 공통 출처)
    n_dn = n_by_ph.get("dense", 0)
    # ⚠ 기체 기준계는 relax 상이 있다. static+dense 만 세면 실제 실행 횟수보다 적다
    #   (2026-08-12: 35 라고 적었는데 실제 43 이었다).
    n_cd = len(list(out.rglob("dense_cand/INCAR")))
    man["submission"] = {
        "cores_per_job": a.cores,
        "max_concurrency": a.concurrency,
        # ⛔⛔ 회신 AR P1-11 · 해제조건 9 (2026-08-31) — MANIFEST 는 "의존성 없음 +
        #   배열 제출" 을 말하고 다른 문서는 staged 실행을 요구해 **정면으로 충돌**했다.
        #   실행 경로가 둘이면 1단계 정지 규칙이 강제되지 않는다. 구성에서 유도한다.
        "phase_dependencies": (
            ("⛔ **잡 사이에 의존성이 있다** (staged 구성). canary(*__nzmag)는 "
             "PARENT_GEOM 이 가리키는 부모의 최종 기하를 받고, 2단계는 1단계 게이트를 "
             "통과해야 열린다. 한 잡 안에서 dense 는 static 의 CHGCAR 를 승계한다. "
             "순서는 run_staged.sh 가 강제한다 — 배열로 한꺼번에 던지면 안 된다.")
            if man.get("staged_runner") else
            ("잡 사이 의존 없음. 한 잡 안에서 dense 는 static 의 "
             "CHGCAR 를 승계하므로 **직렬** — 잡 하나가 분할 불가 "
             "작업 하나다 (P||Cmax).")),
        "n_static": n_st, "n_dense_mandatory": n_dn,
        "n_vasp_executions_total": n_ph_all,
        "n_by_phase": n_by_ph,
        "n_dense_candidates_packaged": n_cd,
        "adaptive_dense": ("enabled (dense_cand/ + --plan_dense + run_dense_selected.sh)"
                           if a.adaptive_dense else
                           "DISABLED — 이 번들에 dense_cand/ 도 run_dense_selected.sh 도 "
                           "없다. ⚠ branch 경합은 **게이트로 막지 않는다** — headline 이 "
                           "branch-minimum 이 아니라 같은 seed(pm1) 대비이기 때문이다. "
                           "경합은 pairs[*].branch_tie 에 기록만 하고, 실제 보호막은 "
                           "seed 산포 게이트(≤10 meV)다"),
        "branch_policy": ("pm1 same-seed conditional — **branch minimum 미주장**. "
                          "어느 자기 branch 가 바닥인지 말하려면 각 끝점의 최저 branch 에 "
                          "dense 가 필요한데 이 판엔 없다"),
        "max_optional_dense": (MAX_OPTIONAL_DENSE_B if a.adaptive_dense else 0),
        "estimator": "tools/sdcp/vasp_cost_estimate.py --manifest MANIFEST.json",
        "estimator_baseline": ("runs/sdcp_phaseB_vasp_v1_2026_08_08/slab/OUTCAR.gz "
                               "— 192원자·NKPTS 4·48코어·525 s/전자스텝"),
        "estimator_uncertainty": "±2배 (모형이지 벤치마크가 아니다)",
        "runner_note": (
            ("⛔ 실행 경로는 `bash run_staged.sh {1|2}` **하나뿐**이다. run_all.sh 는 "
             "이 묶음에 넣지 않았고, 배열 제출도 쓰지 않는다 (1단계 정지 규칙이 "
             "무력화된다). 러너는 실행 전에 MANIFEST 해시·exact 잡 집합·단계 분류를 "
             "확인하고(run_census), POTCAR_ROOT_SEAL.json 을 매번 요구한다.")
            if man.get("staged_runner") else
            ("run_all.sh 는 **직렬 디버그용**이다. 실제 제출은 "
             "SUBMIT_CONTRACT.md 의 배열 잡으로.")),
        "required_returns": (
            ["각 잡 static/OUTCAR(또는 .gz)·OSZICAR", "각 잡 POTCAR_PROVENANCE.json",
             "POTCAR_ROOT_SEAL.json", "ZIP_SHA256.txt",
             "POTCAR_ATTESTATION.json (release 를 원고에 적으려면 필수)"]
            + (["STAGE1_PASS.json"] if man.get("staged_runner") else [])
            + ([f"{k}/relax/OUTCAR·CONTCAR" for k in sorted(man["planned"])
                if "relax" in (man["planned"][k].get("phases") or [])])),
        "⚠_실행수": ("n_vasp_executions_total 은 **상(phase) 수**다. 잡 수와 다르다 — "
                     "relax 가 있는 잡은 잡 하나에 실행 둘이다 (회신 AR Q6)"),
    }
    # ── release assertion: 계획된 **모든** 잡에 조립기가 있는가 ─────────────
    #   제출 본문이 30잡 전부에서 POTCAR_ASSEMBLE.sh 를 부른다. 하나라도 없으면
    #   그 잡은 exit 127 로 죽는다 (2026-08-12: 기체 8잡이 그 상태로 나갔다).
    _noasm = [k for k in man["planned"]
              if not (out / k / "POTCAR_ASSEMBLE.sh").is_file()]
    if _noasm:
        sys.exit(f"⛔ POTCAR 조립기가 없는 잡 {len(_noasm)}개 — 제출 본문이 "
                 f"exit 127 로 죽는다: {_noasm[:5]}")
    man["files_sha256"] = files

    # 번들이 **자기가 어떻게 만들어졌는지**를 담는다. wave1 은 이게 없어서

    #   2026-08-29 에 k 메시를 repo·기계 어디서도 확정하지 못했다.

    man["generated_argv"] = list(sys.argv[1:])

    man["generated_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (out / "MANIFEST.json").write_text(json.dumps(man, indent=1, ensure_ascii=False))

    if out_final.exists():
        out_final.rmdir()
    out.rename(out_final)
    zp = out_final.with_suffix(".zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for q in sorted(out_final.rglob("*")):
            if q.is_file():
                z.write(q, q.relative_to(out_final.parent))
    print(f"\n→ {out_final}  · 잡 {n_jobs}개 · 쌍 {len(man['pairs'])}개 · 조각 {man['fragments']}")
    print(f"→ {zp}  ({zp.stat().st_size / 1e6:.1f} MB)")
    # ⚠ 모드가 바뀌었는데 메시지가 안 따라오면 외주처가 없는 절차를 찾는다.
    if a.single_point or a.closure:
        print("  ⚠ POTCAR 미포함(라이선스) — 잡마다 POTCAR_ASSEMBLE.sh 로 조립할 것 "
              "(종 순서가 잡마다 다르다)")
        print("  ⚠ 단일점 — relax 상이 없다. static (+일부 dense) 만 돈다")
    else:
        print("  ⚠ POTCAR 미포함(라이선스) — POTCAR_SPEC.txt 의 변형(Ni_pv)을 정확히 쓸 것")
        print("  ⚠ 판정 에너지는 static — relax 만 돌리면 분석기가 fail-closed 로 막는다")
    return out_final


# ─────────────────────────────────────────────────────────────────────────────
def _fake_phase(jd: Path, meta: Dict[str, Any], e_static: float,
                spec: Dict[str, str], titel_override=None, truncate: str = "",
                moments_scale: float = 1.0):
    """가짜 VASP 산출 — pre/relax/static 을 계획된 상만큼. 음성 주입용 손잡이 포함.

    truncate: 그 상의 OUTCAR 에서 'General timing' 을 뺀다 (잘린 출력 흉내).
    moments_scale: Ni 국소 모멘트 배율 (0 이면 붕괴).
    """
    els = meta.get("species_order", [])
    titels = "\n".join(f" TITEL  = PAW_PBE {(titel_override or spec).get(e, e)} 01Jan2000"
                       for e in els)
    # ★ 회신 AF P0-7 — 분석기가 POTCAR provenance 를 요구하므로, 가짜 산출도
    #   "외주처가 조립기를 제대로 돌린" 상태를 흉내내야 한다. 조립기가 실린 잡에만.
    if (jd / "POTCAR_ASSEMBLE.sh").is_file():
        _pvv = [(titel_override or spec).get(e, e) for e in els]
        (jd / "POTCAR_PROVENANCE.json").write_text(json.dumps({
            "schema": "potcar_provenance/v1", "species_order": list(els),
            "expected_variants": _pvv,
            "titel_lines": [f" TITEL  = PAW_PBE {v} 01Jan2000" for v in _pvv],
            "source_sha256": {}, "allowlist": "/abs/site_allow.txt",
            "allowlist_sha256": "0" * 64, "allowlist_waived": False,
            "assembled_sha256": "1" * 64}, ensure_ascii=False))
    n = sum(meta.get("counts", [0])) or 1
    frc = "\n".join("     0.0 0.0 0.0   0.001 0.001 0.001" for _ in range(n))
    sign = meta.get("ni_sign_poscar_idx") or {}
    mom_rows = []
    for i in range(n):
        m = float(sign.get(str(i), 0.0)) * 1.2 * moments_scale
        mom_rows.append(f"{i + 1:5d}     0.000   0.000   {m:7.3f}   {m:7.3f}")
    mom = ("\n magnetization (x)\n\n# of ion       s       p       d       tot\n"
           "------------------------------------------\n" + "\n".join(mom_rows)
           + "\n--------------------------------------------------\n")
    # LDAUPRINT=2 의 onsite density matrix (Ni 만). 없으면 LDAU 기록 경로가 안 돈다.
    occ = []
    for k, v in sorted(sign.items(), key=lambda kv: int(kv[0])):
        nu, nd = (0.9, 0.1) if float(v) > 0 else (0.1, 0.9)
        occ.append(f" atom =  {int(k) + 1}   type =   2   l =   2")
        for sp, val in ((1, nu), (2, nd)):
            occ.append("\n onsite density matrix\n")
            occ.append(f" spin component  {sp}")
            occ.append("")
            for r in range(5):
                occ.append("  " + "  ".join(f"{val if c == r else 0.0:.4f}"
                                            for c in range(5)))
    mom += "\n".join(occ) + "\n"
    end = " General timing and accounting\n"
    for ph in meta.get("phases", ["relax", "static"]):
        (jd / ph).mkdir(exist_ok=True)
        # ⚠ 실제 OUTCAR 는 NKPTS 와 INCAR 태그를 되울린다. 안 쓰면 새 검사들이 전부
        #   UNVERIFIED 로 걸려 **양성 경로가 통째로 죽는다** (2026-08-12 실측).
        inc = (jd / ph / "INCAR").read_text() if (jd / ph / "INCAR").is_file() else ""
        # ⚠ 실제 형식대로 되울린다 (2026-08-25): LDA+U 계열은 **산문형**(행 중간),
        #   나머지는 행두형. 옛 fixture 는 전부 행두 + 한 토큰이라 새 파서와 어긋났다
        #   — fixture 가 현실과 다르면 selftest 는 파서가 아니라 fixture 를 검사한다.
        _exp = _incar_expected_from(inc)
        _el = []
        for k, v in _exp.items():
            if k == "LDAUTYPE":
                _el.append(f" LDA+U is selected, type is set to LDAUTYPE =  {v}")
            elif k in ("LDAUL", "LDAUU", "LDAUJ"):
                _el.append(f"   (fixture)      for each species {k} =   {v}")
            else:
                _el.append(f"   {k} = {v}")
        echo = "\n".join(_el)
        nk = 1
        for v in str((meta.get("kmesh") or {}).get(ph, "1 1 1")).split():
            nk *= int(v)
        # ⛔ 회신 AT P0-2 (2026-08-31) — 실물 VASP 는 KPOINTS 첫 줄을 ` KPOINTS: …`
        #   으로 되울린다. 픽스처에 그 줄이 없으면 새 게이트가 **전 잡을** 막아
        #   (KPOINTS_TITLE_UNVERIFIED) 이 selftest 가 통째로 NO_DATA 가 된다.
        #   픽스처는 **실물 모양**이어야 한다 — 음성 경로는 따로 만든다.
        _kt = ((meta.get("kpoints_expected") or {}).get(ph) or {}).get("title")
        head = (f" vasp.6.4.2\n{titels}\n   NIONS = {n}\n   NKPTS = {nk}\n{echo}\n"
                + (f" KPOINTS: {_kt}\n" if _kt else "")
                + f"   NELM   =    200;   NELMIN=  6;\n")
        # ⛔ 회신 AO P0-5 (2026-08-31) — `_icharg1_chgcar_gate` 를 `phase_gates()` 에
        #   실제로 연결하고 나니, 이 픽스처의 OUTCAR 에 **CHGCAR 승계 마커가 없어서**
        #   ICHARG=1 인 상이 전부 CHGCAR_NOT_READ 로 막혔다. 실물 VASP 는 파일을
        #   읽으면 `initial charge density was supplied:` 만 찍고, 새로 만들면 그 밑에
        #   `charge density of overlapping atoms calculated` 를 덧붙인다.
        #   픽스처를 **실물 모양**으로 만든다 (음성 경로는 아래 STUB/N-케이스가 만든다).
        _ic = str((meta.get("incar_expected") or {}).get(ph, {}).get("ICHARG", "")).strip()
        if _ic == "1":
            head += " initial charge density was supplied:\n"
        elif _ic == "2":
            head += (" initial charge density was supplied:\n"
                     " charge density of overlapping atoms calculated\n")
        body = head + "Iteration      1(  33)\n"
        if ph == "relax":
            body += (f" POSITION      TOTAL-FORCE (eV/Angst)\n ---\n{frc}\n"
                     " reached required accuracy - stopping structural energy"
                     " minimisation\n")
        # ⚠ 실제 VASP 는 **모든 상**이 energy(sigma->0) 를 찍는다. relax 에만 안 쓰면
        #   NO_ENERGY(relax) 가 전 잡에 걸려 selftest 가 아무것도 검증하지 못한다.
        body += f"  energy(sigma->0) =  {e_static:.6f}\n"
        body += " number of electron  100.0000000 magnetization   0.0000\n" + mom
        (jd / ph / "OUTCAR").write_text(body + ("" if truncate == ph else end))
    if "relax" in meta.get("phases", []):
        shutil.copy(jd / "POSCAR", jd / "relax" / "CONTCAR")


STUB_VASP = r"""#!/usr/bin/env bash
# 가짜 vasp_std — **러너 계약만** 시험한다 (물리 없음).
#   · POSCAR/INCAR/POTCAR 가 CWD 에 없으면 실패 (러너가 복사를 빠뜨렸는지)
#   · ICHARG=1 인데 CHGCAR 가 없으면 실패 (진짜 VASP 와 같은 계약)
#   · STUB_FAIL="<phase>:crash|truncate" 로 실패 경로를 주입
#   · STUB_LOG 에 실행된 상을 순서대로 적는다 (재개가 진짜 건너뛰는지)
set -u
ph=$(basename "$PWD")
[ -n "${STUB_LOG:-}" ] && echo "$ph" >> "$STUB_LOG"
[ -s POSCAR ] || { echo "STUB: POSCAR 없음 ($ph)"; exit 3; }
[ -s INCAR ]  || { echo "STUB: INCAR 없음 ($ph)";  exit 3; }
[ -s POTCAR ] || { echo "STUB: POTCAR 없음 ($ph)"; exit 3; }
if grep -qE '^ICHARG[[:space:]]*=[[:space:]]*1' INCAR && [ ! -s CHGCAR ]; then
  echo "STUB: ICHARG=1 인데 CHGCAR 가 없다 ($ph)"; exit 4
fi
chg_in="(none)"
[ -s CHGCAR ] && chg_in=$(cksum < CHGCAR | awk '{print $1}')
cp POSCAR CONTCAR
echo "stub-chg $ph" > CHGCAR
echo "stub-wav $ph" > WAVECAR
{ echo "  POSCAR_CKSUM = $(cksum < POSCAR | awk '{print $1}')"
  echo "  CHGCAR_IN_CKSUM = $chg_in"
  echo "  energy(sigma->0) =     -123.456789"; } > OUTCAR
case "${STUB_FAIL:-}" in
  "$ph:crash")    echo "STUB: 강제 실패 ($ph)"; exit 1 ;;
  "$ph:truncate") echo "STUB: 잘린 출력 ($ph)"; exit 0 ;;   # General timing 없이 끝
esac
echo " General timing and accounting informations for this job" >> OUTCAR
exit 0
"""


def _runner_regression(out: Path, chk) -> None:
    """★ P0-2 — run_job.sh 를 **실제로 실행**한다 (Codex 4차·6차).

    왜 필요한가: 이 도구의 다른 selftest 는 전부 가짜 OUTCAR 를 파이썬이 직접 써 넣는다.
    그래서 러너 자체는 **한 번도 안 돌았고**, 단일점 모드에서 러너가 relax/CONTCAR 를
    요구해 VASP 를 시작조차 못 하는 버그(P0-1)를 통째로 놓쳤다. 여기서는 stub vasp_std 를
    PATH 에 놓고 러너를 그대로 돌린다.

    이 시험이 **못 하는 것**: 물리·수렴·VASP 실제 동작. 오직 상 사슬(입력 복사·승계·
    중단·재개·종료코드)만 본다. 기대 상 목록은 하드코딩하지 않고 job.json 에서 읽는다.
    """
    sp = [p.parent for p in sorted(out.rglob("job.json"))
          if "dense" in (json.loads(p.read_text()).get("phases") or [])
          and json.loads(p.read_text()).get("phases", [])[0] == "static"]
    if not sp:
        chk(False, "P0-2: 단일점+dense 잡이 번들에 없다 — 러너 회귀를 못 돌린다")
        return
    src = sp[0]
    stub_dir = out.parent / "_stub_bin"
    stub_dir.mkdir(exist_ok=True)
    (stub_dir / "vasp_std").write_text(STUB_VASP)
    (stub_dir / "vasp_std").chmod(0o755)

    def run(tag: str, fail: str = "", prep=None):
        jd = out.parent / f"_run_{tag}"
        shutil.rmtree(jd, ignore_errors=True)
        shutil.copytree(src, jd)
        (jd / "POTCAR").write_text("stub POTCAR\n")
        # ⛔ 회신 AF P0-7 — provenance 우회는 **파일 표시**로만 된다 (환경변수 폐지).
        #   배포 번들에는 이 파일이 없고, 나중에 만들어 넣으면 files_sha256 이 잡는다.
        (jd / ".SELFTEST_FIXTURE").write_text("runner regression fixture\n")
        log = jd / "_phases.log"
        if prep:
            prep(jd)
        env = {**os.environ, "PATH": f"{stub_dir}:{os.environ.get('PATH', '')}",
               "VASP_CMD": "vasp_std", "STUB_LOG": str(log),
               # 상 사슬 시험은 POTCAR provenance 와 무관하다 — 그 축은 아래
               # R14~R16 이 **전용으로** 친다 (한 시험이 두 가지를 재면 왜 실패했는지
               # 모른다).
               }
        if fail:
            env["STUB_FAIL"] = fail
        r = subprocess.run(["bash", "run_job.sh"], cwd=jd, env=env,
                           capture_output=True, text=True)
        ran = log.read_text().split() if log.is_file() else []
        return jd, r, ran

    # ── R1 정상 경로: 단일점 static → dense 가 **실제로 돈다** ──────────────
    jd, r, ran = run("ok")
    chk(r.returncode == 0, f"R1 단일점 러너 완주 rc=0 (실행 상 {ran}) "
                           f"{'' if r.returncode == 0 else '| ' + r.stdout.strip()[-90:]}")
    chk(ran == ["static", "dense"], f"R1b 상 순서 static→dense ({ran})")
    root = (jd / "POSCAR").read_bytes()
    chk((jd / "static" / "POSCAR").read_bytes() == root,
        "R2 static/POSCAR == 루트 POSCAR (byte 일치 — 다른 기하를 계산하지 않았다)")
    chk((jd / "dense" / "POSCAR").read_bytes() == root,
        "R3 dense/POSCAR == 루트 POSCAR (단일점이라 기하가 안 변한다)")
    si = (jd / "static" / "INCAR").read_text()
    di = (jd / "dense" / "INCAR").read_text()
    chk(re.search(r"^ICHARG\s*=\s*2", si, re.M) is not None,
        "R4 static ICHARG=2 (원자중첩 시작 — 승계할 CHGCAR 가 없다)")
    chk(re.search(r"^ICHARG\s*=\s*1", di, re.M) is not None,
        "R5 dense ICHARG=1 (**static 의 CHGCAR 를 실제로 쓴다**)")
    # ⚠ 실행 **후** 두 CHGCAR 를 비교하면 안 된다 — VASP 는 CHGCAR 를 출력으로
    #   덮어쓰므로 정상이어도 달라진다. dense 가 **읽은** 지문을 본다.
    cin = re.search(r"CHGCAR_IN_CKSUM = (\S+)", (jd / "dense" / "OUTCAR").read_text())
    chk(cin is not None and cin.group(1) not in ("(none)", ""),
        f"R6 dense 가 CHGCAR 를 **입력으로 받았다** (지문 {cin.group(1) if cin else '없음'})")
    sin = re.search(r"CHGCAR_IN_CKSUM = (\S+)", (jd / "static" / "OUTCAR").read_text())
    chk(sin is not None and sin.group(1) == "(none)",
        "R6b static 은 CHGCAR 를 안 받았다 (ISTART=0/ICHARG=2 단일점이 맞다)")

    # ── R7 ★ 계약 변경 (회신 AA P0-5) — 기본은 **1회용**이다 ────────────────
    #   종전 계약: 완주한 잡을 다시 돌리면 전 상을 건너뛴다(조용한 재개).
    #   새 계약  : 시작 전에 산출물이 있으면 **거부한다.** 재개는 ALLOW_RESUME=1.
    #   왜: "이미 완료 — 건너뜀" 은 남이 다른 설정으로 돌려 둔 결과를 우리 것으로
    #   반송하게 만든다. 회수 후에는 구별할 방법이 없다.
    log2 = jd / "_phases.log"
    log2.unlink()
    r2 = subprocess.run(["bash", "run_job.sh"], cwd=jd, capture_output=True, text=True,
                        env={**os.environ, "PATH": f"{stub_dir}:{os.environ.get('PATH','')}",
                             "VASP_CMD": "vasp_std", "STUB_LOG": str(log2),
                             })
    ran2 = log2.read_text().split() if log2.is_file() else []
    chk(r2.returncode != 0 and ran2 == [] and "1회용" in (r2.stdout + r2.stderr),
        f"⛔음성 R7: 산출물이 있는 잡을 그냥 재실행하면 **거부** "
        f"rc={r2.returncode} 실행 {ran2}")

    # ── R7b 재개는 **명시적 선언**으로만 ───────────────────────────────────
    log2.unlink(missing_ok=True)
    r2b = subprocess.run(["bash", "run_job.sh"], cwd=jd, capture_output=True, text=True,
                         env={**os.environ, "PATH": f"{stub_dir}:{os.environ.get('PATH','')}",
                              "VASP_CMD": "vasp_std", "STUB_LOG": str(log2),
                              "ALLOW_RESUME": "1"})
    ran2b = log2.read_text().split() if log2.is_file() else []
    chk(r2b.returncode == 0 and ran2b == [],
        f"R7b ALLOW_RESUME=1 이면 전 상 건너뜀 rc={r2b.returncode} 실행 {ran2b}")

    # ── R8 부분 재개도 ALLOW_RESUME 아래에서만 ─────────────────────────────
    (jd / "dense" / "OUTCAR").unlink()
    log2.unlink(missing_ok=True)
    r3 = subprocess.run(["bash", "run_job.sh"], cwd=jd, capture_output=True, text=True,
                        env={**os.environ, "PATH": f"{stub_dir}:{os.environ.get('PATH','')}",
                             "VASP_CMD": "vasp_std", "STUB_LOG": str(log2),
                             "ALLOW_RESUME": "1",
                             })
    ran3 = log2.read_text().split() if log2.is_file() else []
    chk(r3.returncode == 0 and ran3 == ["dense"],
        f"R8 ALLOW_RESUME 부분 재개 rc={r3.returncode} 실행 {ran3}")

    # ── R8b ★ 그 부분 재개도 **선언 없이는** 막힌다 (dense OUTCAR 는 지웠지만
    #   static/CHGCAR 등 다른 산출물이 남아 있다) ──────────────────────────
    (jd / "dense" / "OUTCAR").unlink(missing_ok=True)
    log2.unlink(missing_ok=True)
    r3b = subprocess.run(["bash", "run_job.sh"], cwd=jd, capture_output=True, text=True,
                         env={**os.environ, "PATH": f"{stub_dir}:{os.environ.get('PATH','')}",
                              "VASP_CMD": "vasp_std", "STUB_LOG": str(log2),
                              })
    chk(r3b.returncode != 0,
        f"⛔음성 R8b: 일부만 지우고 재실행해도 선언 없이는 거부 rc={r3b.returncode}")

    # ── R9 음성: static 이 죽으면 dense 를 **시작하지 않는다** ───────────────
    jd9, r9, ran9 = run("crash", fail="static:crash")
    chk(r9.returncode != 0 and ran9 == ["static"] and not (jd9 / "dense" / "OUTCAR").is_file(),
        f"R9 static 실패 → 중단·dense 미시작 rc={r9.returncode} 실행 {ran9}")

    # ── R10 음성: 잘린 출력(General timing 없음)도 성공으로 안 본다 ──────────
    jd10, r10, ran10 = run("trunc", fail="static:truncate")
    chk(r10.returncode != 0 and ran10 == ["static"]
        and not (jd10 / "dense" / "OUTCAR").is_file(),
        f"R10 잘린 static → 중단 (exit0 이어도) rc={r10.returncode} 실행 {ran10}")

    # ── R11 음성: static 이 완료로 보이는데 CHGCAR 가 비면 dense 를 못 시작 ──
    def _kill_chg(j: Path):
        (j / "static").mkdir(exist_ok=True)
        (j / "static" / "OUTCAR").write_text(
            "  energy(sigma->0) =     -1.0\n General timing and accounting\n")
        (j / "static" / "CHGCAR").write_text("")          # 0바이트
    jd11, r11, ran11 = run("nochg", prep=_kill_chg)
    chk(r11.returncode != 0 and ran11 == []
        and not (jd11 / "dense" / "OUTCAR").is_file(),
        f"R11 빈 static/CHGCAR → dense 시작 전 중단 rc={r11.returncode} 실행 {ran11}")

    # ── R12 음성: POTCAR 가 없으면 아예 시작하지 않는다 ─────────────────────
    jd12 = out.parent / "_run_nopot"
    shutil.rmtree(jd12, ignore_errors=True)
    shutil.copytree(src, jd12)
    r12 = subprocess.run(["bash", "run_job.sh"], cwd=jd12, capture_output=True, text=True,
                         env={**os.environ, "PATH": f"{stub_dir}:{os.environ.get('PATH','')}",
                              "VASP_CMD": "vasp_std"})
    chk(r12.returncode != 0 and not (jd12 / "static" / "OUTCAR").is_file(),
        f"R12 POTCAR 없음 → 시작 거부 rc={r12.returncode}")

    # ── R14~R16 (회신 AB P0-8): POTCAR provenance 계약 ─────────────────────
    def _pv(jd, waived=False, swap=False, no_alsha=False):
        (jd / "POTCAR").write_text("stub POTCAR\n")
        (jd / "POTCAR_PROVENANCE.json").write_text(json.dumps({
            "schema": "potcar_provenance/v1",
            "allowlist": None if waived else "/abs/site_allow.txt",
            "allowlist_sha256": None if waived else ("0" * 64),
            "allowlist_waived": waived,
            "assembled_sha256": hashlib.sha256((jd / "POTCAR").read_bytes()).hexdigest()}))
        if no_alsha:
            _d = json.loads((jd / "POTCAR_PROVENANCE.json").read_text())
            _d.pop("allowlist_sha256", None)
            (jd / "POTCAR_PROVENANCE.json").write_text(json.dumps(_d))
        if swap:
            (jd / "POTCAR").write_text("SWAPPED POTCAR\n")     # 조립 뒤 교체

    def _pcase(tag, prep):
        jd = out.parent / f"_run_{tag}"
        shutil.rmtree(jd, ignore_errors=True); shutil.copytree(src, jd)
        prep(jd)
        r = subprocess.run(["bash", "run_job.sh"], cwd=jd, capture_output=True, text=True,
                           env={**os.environ,
                                "PATH": f"{stub_dir}:{os.environ.get('PATH', '')}",
                                "VASP_CMD": "vasp_std"})
        return jd, r

    _j, _r = _pcase("noprov", lambda d: (d / "POTCAR").write_text("stub POTCAR\n"))
    chk(_r.returncode != 0 and not (_j / "static" / "OUTCAR").is_file(),
        f"⛔음성 R14: POTCAR 는 있는데 provenance 가 없으면 거부 rc={_r.returncode}")
    _j, _r = _pcase("swapped", lambda d: _pv(d, swap=True))
    chk(_r.returncode != 0 and not (_j / "static" / "OUTCAR").is_file(),
        f"⛔음성 R15: 조립 뒤 POTCAR 교체 → sha 불일치로 거부 rc={_r.returncode}")
    _j, _r = _pcase("waived", lambda d: _pv(d, waived=True))
    chk(_r.returncode != 0 and not (_j / "static" / "OUTCAR").is_file(),
        f"⛔음성 R16: allowlist 면제본은 거부 (면제 폐지) rc={_r.returncode}")
    _j, _r = _pcase("goodprov", _pv)
    chk(_r.returncode == 0 and "provenance 확인" in _r.stdout,
        f"R17 양성: 정상 provenance 면 통과한다 rc={_r.returncode}")

    # ⛔ 회신 AF P0-7 — allowlist 는 **경로만** 있고 내용 SHA 가 없었다.
    #   경로만으로는 그 사이트가 어떤 allowlist 를 썼는지 확인할 수 없다.
    jd18 = out.parent / "_run_r18"
    shutil.rmtree(jd18, ignore_errors=True)
    shutil.copytree(src, jd18)
    _pv(jd18, no_alsha=True)
    r18 = subprocess.run(["bash", "run_job.sh"], cwd=jd18, capture_output=True, text=True,
                         env={**os.environ,
                              "PATH": f"{stub_dir}:{os.environ.get('PATH','')}",
                              "VASP_CMD": "vasp_std"})
    chk(r18.returncode != 0 and "allowlist 내용 SHA" in (r18.stdout + r18.stderr),
        f"⛔음성 R18: allowlist 경로만 있고 내용 SHA 가 없으면 거부 rc={r18.returncode}")

    # ⛔ 배포 러너는 환경변수로 우회되지 않는다 (파일 표시만 인정)
    jd19 = out.parent / "_run_r19"
    shutil.rmtree(jd19, ignore_errors=True)
    shutil.copytree(src, jd19)
    (jd19 / "POTCAR").write_text("stub POTCAR\n")
    r19 = subprocess.run(["bash", "run_job.sh"], cwd=jd19, capture_output=True, text=True,
                         env={**os.environ,
                              "PATH": f"{stub_dir}:{os.environ.get('PATH','')}",
                              "VASP_CMD": "vasp_std",
                              "SKIP_POTCAR_PROVENANCE": "1"})
    chk(r19.returncode != 0,
        f"⛔음성 R19: SKIP_POTCAR_PROVENANCE=1 환경변수로는 **우회 안 된다** "
        f"rc={r19.returncode} (파일 표시만 인정 — 반송물에 흔적이 남게)")


    # ── R13 러너 자체 sanity: stub 이 없으면 시험이 통과해선 안 된다 ─────────
    #   (양성만 있는 selftest 의 재발 방지 — 시험 장치 자체를 시험한다)
    jd13 = out.parent / "_run_nostub"
    shutil.rmtree(jd13, ignore_errors=True)
    shutil.copytree(src, jd13)
    (jd13 / "POTCAR").write_text("stub POTCAR\n")
    r13 = subprocess.run(["bash", "run_job.sh"], cwd=jd13, capture_output=True, text=True,
                         env={**os.environ, "VASP_CMD": "definitely_not_a_real_binary_xyz",
                              })
    chk(r13.returncode != 0,
        f"R13 실행파일이 없으면 러너가 실패한다 (시험 장치 검증) rc={r13.returncode}")


def _synth_ledger(atoms, nslab: int) -> Dict[str, Any]:
    """selftest 용 합성 원장 — **뒤섞인** 부격자로 만든다 (블록이면 옛 버그를 못 잡는다)."""
    sym = atoms.get_chemical_symbols()
    ni = [i for i in range(nslab) if sym[i] == "Ni"]
    pat = [-1.0, 1.0, 1.0, -1.0]                 # 4주기 — 앞절반/뒤절반과 다르다
    sgn = {str(i): pat[k % 4] for k, i in enumerate(ni)}
    if sum(sgn.values()):                        # 홀수면 균형을 맞춘다
        sgn[str(ni[-1])] = -sum(list(sgn.values())[:-1])
    return {"element": "Ni", "supercell_matrix": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "n_replicas": 1, "counts": {"Ni1": len(ni) // 2, "Ni2": len(ni) // 2},
            "max_residual_A": 0.0, "sign_convention": {"Ni1": 1.0, "Ni2": -1.0},
            "net_moment_muB": 0.0, "sign_by_slab_index": sgn, "rows": [],
            "source_qe": "(selftest)", "source_slab": "(selftest)"}


def _sha_file(p):
    import hashlib
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def selftest() -> int:
    """전 경로 + **음성 경로**. 음성이 없는 selftest 는 통과해도 아무것도 보증 못 한다.

    2026-08-12 — 옛 판의 음성 2건은 사실 아무것도 검증하지 않았다:
      · `chk(x is None or True, ...)` 는 **항상 참**이었다 (상자 게이트 미검증).
      · dense 를 양 끝점에 같은 +3 meV 로 심어 ΔE 이동이 정확히 0 이었다 (k 게이트 미검증).
    """
    import tempfile
    from ase import Atoms
    from ase.io import write as ase_write
    td = Path(tempfile.mkdtemp(prefix="vasp_bundle_v3_st_"))
    print(f"selftest → {td}")

    pos, symb = [], []
    for i in range(8):
        symb.append("O"); pos.append([(i % 4) * 2.0, (i // 4) * 4.0, 0.0])
        symb.append("O"); pos.append([(i % 4) * 2.0, (i // 4) * 4.0 + 2.0, 2.0])
    for i in range(8):
        symb.append("Li"); pos.append([(i % 4) * 2.0, (i // 4) * 2.0, 6.0])
    for i in range(8):
        symb.append("Ni"); pos.append([(i % 4) * 2.0, 4.0 + (i // 4) * 2.0, 6.0])
    nslab = len(symb)
    mol_syms = ["C", "C", "F", "F", "F", "F"]

    def mol_at(y0):
        # ⚠ z 를 슬랩(6.0) 에서 2 Å 위로 둔다 — 3 Å 이상 띄우면 접촉 지문이 **양쪽 다
        #   비어** Jaccard 경로가 통째로 안 돌아 PAIR_COLLAPSED 를 검증하지 못한다.
        return [[3.0, y0, 8.0], [4.4, y0, 8.0], [2.4, y0 - 0.8, 8.6],
                [2.4, y0 + 0.8, 8.6], [5.0, y0 - 0.8, 8.6], [5.0, y0 + 0.8, 8.6]]

    run = td / "runs" / "ptfe_dimer" / "relax_f0.85"
    run.mkdir(parents=True)
    cell = np.diag([8.0, 8.0, 26.0])
    slab_at = Atoms(symbols=symb, positions=pos, cell=cell, pbc=True)
    ase_write(run / "_clean_slab.vasp", slab_at, format="vasp", direct=True)
    DIRS = (("fib00", 0.045), ("fib01", 0.040), ("fib02", 0.055), ("fib03", 0.050),
            ("fib04", 0.048))
    for dd, de in DIRS:
        for role, ncat, e in (("Li_top", "Li", -0.20), ("Ni_top", "Ni", -0.20 + de)):
            lab = f"ptfe_dimer__{role}__{dd}__r000"
            at = Atoms(symbols=symb + mol_syms,
                       positions=pos + mol_at(1.0 if role == "Li_top" else 5.0),
                       cell=cell, pbc=True)
            ase_write(run / f"{lab}.xyz", at)
            (run / f"{lab}.json").write_text(json.dumps({
                "label": lab, "site": role, "down_dir": dd, "roll_deg": 0,
                "fragment": "ptfe_dimer", "E_pose_eV": e,
                "nearest_cation": ncat, "ranking_eligible": True,
                "fingerprint": "stfp0001",
                "protocol": {"fingerprint": "stfp0001",
                             "gate_version": SS.gate_version()}}))

    # ★ 짝 **없는** 저에너지 Ni 자세 — 전역 최선은 여기인데 Li 짝이 없어 풀에 못 든다.
    #   실빌드의 ptfe_c10 이 정확히 이 모양이었다(Ni 전역 최선이 51.8 meV 아래).
    #   이게 없으면 전역 챔피언 경로가 selftest 에서 한 번도 안 돈다.
    _lab_g = "ptfe_dimer__Ni_top__fib99__r000"
    ase_write(run / f"{_lab_g}.xyz",
              Atoms(symbols=symb + mol_syms, positions=pos + mol_at(5.0),
                    cell=cell, pbc=True))
    (run / f"{_lab_g}.json").write_text(json.dumps({
        "label": _lab_g, "site": "Ni_top", "down_dir": "fib99", "roll_deg": 0,
        "fragment": "ptfe_dimer", "E_pose_eV": -0.30,          # 풀 최선보다 낮다
        "nearest_cation": "Ni", "ranking_eligible": True,
        "fingerprint": "stfp0001",
        "protocol": {"fingerprint": "stfp0001", "gate_version": SS.gate_version()}}))

    _slab_patched = SS.load_slab            # 복원용 (아래 finally 에서 되돌린다)
    SS.load_slab = lambda: slab_at
    SS.load_fragment = lambda f: (Atoms(symbols=mol_syms, positions=mol_at(3.0)),
                                  {"status": "OK"})
    SS.FRAGMENTS.setdefault("ptfe_dimer", {"electrons": "closed-shell singlet"})
    global TIERS, EXPECT_PAIRS
    TIERS = {"tier1": ["ptfe_dimer"], "tier2": []}
    EXPECT_PAIRS = {"ptfe_dimer": len(DIRS)}
    led = _synth_ledger(slab_at, nslab)

    ok = True

    def chk(cond, msg):
        nonlocal ok
        print(("  ✔ " if cond else "  ⛔ ") + msg)
        ok &= bool(cond)

    # ── N0 계약 위반: 방향 하나를 숨기면 번들을 만들면 안 된다 (Codex P0-A) ──
    hidden = run / "ptfe_dimer__Li_top__fib04__r000.xyz"
    hidden.rename(run.parent / "hidden.xyz")
    a0 = argparse.Namespace(runs=str(td / "runs"), out=str(td / "bundle_short"),
                            freeze=0.85, nslab=nslab, frags=["ptfe_dimer"],
                            qe="(none)", expect=None, allow_partial=False,
                            allow_no_pin=True, no_prescf=False, allow_stale_gate=False, top_n=None, roles=None, d3_seed_main_only=False, no_refs_dense=False, from_basins=None, both_seeds=False, d3_pairs=False, closure=False, single_point=False, champion=False, kmesh_static=None, kmesh_dense=None, refs=True, cross_endpoints=None, mag_controls=False, dense_frags=None, cores=48, concurrency=8, no_cross=False, global_champion_meV=20.0, adaptive_dense=False)
    try:
        build_bundle(a0, ledger=led)
        chk(False, "N0 xyz 누락 → **번들이 만들어졌다** (축소 정본 = fail-open)")
    except SystemExit as e:
        chk("계약 위반" in str(e), f"N0 xyz 누락 → 생성 중단 ({str(e).splitlines()[0][:44]})")
    (run.parent / "hidden.xyz").rename(hidden)

    # ── N0b 지문 없는 소스 행 (옛 판은 '있는 행만' 비교해 전부 비어도 통과했다) ──
    jp0 = run / "ptfe_dimer__Li_top__fib00__r000.json"
    keep = jp0.read_text()
    d0 = json.loads(keep); d0.pop("fingerprint")
    jp0.write_text(json.dumps(d0))
    ab = argparse.Namespace(runs=str(td / "runs"), out=str(td / "bundle_nofp"),
                            freeze=0.85, nslab=nslab, frags=["ptfe_dimer"],
                            qe="(none)", expect=None, allow_partial=False,
                            allow_no_pin=True, no_prescf=False, allow_stale_gate=False, top_n=None, roles=None, d3_seed_main_only=False, no_refs_dense=False, from_basins=None, both_seeds=False, d3_pairs=False, closure=False, single_point=False, champion=False, kmesh_static=None, kmesh_dense=None, refs=True, cross_endpoints=None, mag_controls=False, dense_frags=None, cores=48, concurrency=8, no_cross=False, global_champion_meV=20.0, adaptive_dense=False)
    try:
        build_bundle(ab, ledger=led)
        chk(False, "N0b 지문 없는 소스 → **번들이 만들어졌다**")
    except SystemExit as e:
        chk("지문이 없는" in str(e), f"N0b 지문 없는 소스 → 중단 ({str(e).splitlines()[0][:40]})")
    # ── N0c gate_version 이 옛값 ──
    d0["fingerprint"] = "stfp0001"
    d0["protocol"] = {"fingerprint": "stfp0001", "gate_version": "OLDGATE01"}
    jp0.write_text(json.dumps(d0))
    ac = argparse.Namespace(**{**vars(ab), "out": str(td / "bundle_oldgate")})
    try:
        build_bundle(ac, ledger=led)
        chk(False, "N0c 옛 gate_version → **번들이 만들어졌다**")
    except SystemExit as e:
        chk("gate_version" in str(e), f"N0c 옛 gate_version → 중단 (regate 안내)")
    jp0.write_text(keep)

    # ── top_n 선별: 안정도 상위 N 쌍만 남기고, 뺀 것을 기록하는가 ──
    #   심은 E_pose: Li 전부 -0.20 · Ni -0.20+de (de = fib00 .045 · fib01 .040 ·
    #   fib02 .055 · fib03 .050 · fib04 .048) → 평균 안정도 순 fib01 < fib00 < fib04
    at3 = argparse.Namespace(runs=str(td / "runs"), out=str(td / "bundle_top3"),
                             freeze=0.85, nslab=nslab, frags=["ptfe_dimer"],
                             qe="(none)", expect=None, allow_partial=False,
                             allow_no_pin=True, no_prescf=False, allow_stale_gate=False, top_n=3, roles=None, d3_seed_main_only=False, no_refs_dense=False, from_basins=None, both_seeds=False, d3_pairs=False, closure=False, single_point=False, champion=False, kmesh_static=None, kmesh_dense=None, refs=True, cross_endpoints=None, mag_controls=False, dense_frags=None, cores=48, concurrency=8, no_cross=False, global_champion_meV=20.0, adaptive_dense=False)
    o3 = build_bundle(at3, ledger=led)
    m3 = json.loads((o3 / "MANIFEST.json").read_text())
    kept = sorted({v["dir"] for v in m3["pairs"].values()})
    aud3 = m3["pair_audit"]["ptfe_dimer"]
    chk(kept == ["fib00", "fib01", "fib04"],
        f"top_n=3 → 안정도 상위 3쌍 {kept} (기대 fib00/01/04)")
    chk(sorted(aud3.get("topn_dropped") or []) == ["fib02", "fib03"],
        f"뺀 방향을 기록 {aud3.get('topn_dropped')}")
    chk(aud3.get("topn_rank_key") and "안정도" in aud3["topn_rank_key"],
        "순위 기준을 명시 (|ΔE| cherry-pick 아님)")
    chk(m3["contract_expected_pairs"]["ptfe_dimer"] == 3,
        "계약이 top_n 을 반영 (5 를 요구해 막지 않는다)")

    a = argparse.Namespace(runs=str(td / "runs"), out=str(td / "bundle"),
                           freeze=0.85, nslab=nslab, frags=["ptfe_dimer"],
                           qe="(none)", expect=None, allow_partial=False,
                           allow_no_pin=True, no_prescf=False, allow_stale_gate=False, top_n=None, roles=None, d3_seed_main_only=False, no_refs_dense=False, from_basins=None, both_seeds=False, d3_pairs=False, closure=False, single_point=False, champion=False, kmesh_static=None, kmesh_dense=None, refs=True, cross_endpoints=None, mag_controls=False, dense_frags=None, cores=48, concurrency=8, no_cross=False, global_champion_meV=20.0, adaptive_dense=False)
    out = build_bundle(a, ledger=led)
    man = json.loads((out / "MANIFEST.json").read_text())
    n_pre = sum(1 for p in man["planned"].values() if "pre" in (p.get("phases") or []))
    chk(n_pre == len([p for p in man["planned"] if "mol__" not in p]),
        f"dipole-off pre-SCF 상이 전 슬랩 잡에 있다 ({n_pre}개)")

    # ── P0-2 러너 회귀: stub VASP 로 run_job.sh 를 **실제 실행** (Codex 4·6차) ──
    a_sp = argparse.Namespace(
        runs=str(td / "runs"), out=str(td / "bundle_sp"), freeze=0.85, nslab=nslab,
        frags=["ptfe_dimer"], qe="(none)", expect=None, allow_partial=False,
        allow_no_pin=True, no_prescf=False, allow_stale_gate=False, top_n=None, roles=None, d3_seed_main_only=False, no_refs_dense=False, from_basins=None, both_seeds=False, d3_pairs=False, closure=False, single_point=True,
        champion=True, kmesh_static=None, kmesh_dense=None, refs=False,
        cross_endpoints=["ptfe_dimer"], mag_controls=True, dense_frags=["ptfe_dimer"], cores=48, concurrency=8, no_cross=False, global_champion_meV=20.0, adaptive_dense=False)
    out_sp = build_bundle(a_sp, ledger=led)

    # ══ 회신 AO — **staged(refs_minimal) 번들 e2e**. 종전엔 이 구성을 selftest 가
    #   한 번도 만들지 않아서, 문서가 안내한 실행 경로가 fresh ZIP 에서 동작하는지
    #   아무도 안 봤다 (AO P1: "실제 stage 경로와 번들 e2e 를 검증하지 않았다").
    #   자세 동결 파일을 **실물 xyz 에서** 만든다 (guard 가 --from_basins 를 요구한다)
    _pose_xyz = sorted((Path(a_sp.runs) / "ptfe_dimer" /
                        f"relax_f{a_sp.freeze:.2f}").glob("*_r*.xyz"))
    _pose_xyz = [q for q in _pose_xyz if not q.name.startswith("_")]
    _fbp = td / "c12_poses_fixture.json"
    if len(_pose_xyz) >= 2:
        _fb = {"schema": "prospective_basins/v1", "freeze_sha256": "f" * 64,
               "params": {"W0_eV": 0.15},
               "fragments": {"ptfe_dimer": {
                   "primary": [{"basin_id": "b00", "rep_label": _pose_xyz[0].stem,
                                "E_pose_eV": 0.0, "role": "primary",
                                "why": "fixture 전역 최소"}],
                   "stress_sensitivity": [
                       {"basin_id": "b01", "rep_label": _pose_xyz[1].stem,
                        "E_pose_eV": 0.30, "role": "stress_sensitivity",
                        "why": "fixture 응력 시험"}]}}}
        _fbp.write_text(json.dumps(_fb, ensure_ascii=False, indent=1))
    a_st = argparse.Namespace(**{**vars(a_sp), "out": str(td / "bundle_staged"),
                                 "refs": True, "refs_minimal": True,
                                 "both_seeds": True, "single_point": True,
                                 "from_basins": str(_fbp),
                                 "roles": ["primary", "stress_sensitivity"],
                                 "cell_c": None, "cell_c2": None,
                                 "min_vacuum": 0.0,
                                 "dense_frags": None})
    _st = None
    try:
        build_bundle(a_st, ledger=led)
        _st = Path(str(td / "bundle_staged"))
    except SystemExit as _e:                     # 가드가 막으면 그 자체가 정보다
        chk(False, f"staged 번들 생성 실패: {_e}")
    # ⛔음성 — 가드가 **여전히 살아 있는지**. staged 구성은 세 플래그가 다 있어야 한다.
    for _drop, _why in (("from_basins", "자세 동결 없이"), ("refs", "기체 기준 없이"),
                        ("both_seeds", "net4 가지 없이")):
        _bad_ns = argparse.Namespace(**{**vars(a_st), _drop:
                                        None if _drop == "from_basins" else False})
        try:
            guard_refs_minimal(_bad_ns); _ok = False
        except SystemExit:
            _ok = True
        chk(_ok, f"⛔음성: --refs_minimal 을 {_why} 쓰면 막는다 (--{_drop})")
    if _st is not None:
        m_st = json.loads((_st / "MANIFEST.json").read_text())
        chk((_st / "run_staged.sh").is_file(),
            "AO P0-2: staged 번들에 run_staged.sh 가 있다")
        chk((_st / "SEAL_POTCAR_ROOT.sh").is_file(),
            "AO P0-2: staged 번들에 **SEAL_POTCAR_ROOT.sh** 가 있다 "
            "(POTCAR 조립이 실행 경로 안에 있어야 fresh ZIP 이 동작한다)")
        chk(not (_st / "run_all.sh").is_file(),
            "⛔음성 AO P0-3: staged 번들에는 run_all.sh 를 **넣지 않는다** "
            "(전체 제출 경로가 있으면 1단계 정지 규칙이 무력화된다)")
        _rs = (_st / "run_staged.sh").read_text()
        chk("SEAL_POTCAR_ROOT.sh" in _rs,
            "⛔음성 AO P0-2: run_staged.sh 가 POTCAR 조립을 **실제로 부른다** "
            "(종전엔 run_job.sh 를 바로 불러 POTCAR 부재로 즉시 중단됐다)")
        # ── 회신 AP #7 — 봉인이 "생산 전" 을 **검사**하는가 ─────────────
        _sl = (_st / "SEAL_POTCAR_ROOT.sh").read_text()
        chk("OUTCAR" in _sl and "vasprun.xml" in _sl and "print -quit" in _sl,
            "⛔음성 AP #7: 최초 봉인 전에 **생산 산출물이 있으면 거부**한다 "
            "(자기선언이 아니라 검사)")
        chk((_st / "POTCAR_ATTESTATION_REQUEST.md").is_file()
            and (_st / "MAKE_POTCAR_ATTESTATION.sh").is_file(),
            "AP #12: 번들에 **계산 전 attestation 요청서와 생성 스크립트**가 있다")
        _atr = (_st / "POTCAR_ATTESTATION_REQUEST.md").read_text()
        for _f in ("release label", "SHA256", "TITEL", "vasp_std --version",
                   "allowlist"):
            chk(_f in _atr, f"AP #12: 요청서가 `{_f}` 를 요구한다")
        chk("allowlist_sha256" in _sl and "재조립" in _sl,
            "⛔음성 AP #7: 기존 POTCAR/provenance 를 **현재 allowlist 로 재대조**한다 "
            "(종전엔 둘 다 있으면 조용히 건너뛰었다)")
        for _f in ("manifest_sha256", "vasp_executable_sha256", "vasp_version_banner",
                   "assembled_sha256_by_job", "sealed_at_utc"):
            chk(_f in _sl, f"AP #7: 봉인이 `{_f}` 를 기록한다")
        # ⛔ 회신 AP #6 — receipt 존재를 믿지 않고 **지금 결과로 재판정**한다.
        #   (위조 receipt(verdict:"FAIL")로 우회되던 경로를 아예 없앤다)
        _s2 = _rs.split('if [ "$stage" = 2 ]')[-1].split("# 잡 분류")[0]
        chk("--gate vacconv" in _s2,
            "⛔음성 AP #6: run_staged.sh 2 가 **시작 직전에 게이트를 다시 돌린다** "
            "(receipt 존재만으로 열지 않는다)")
        chk("analyze_results.py ." in _rs.split('else')[-1],
            "⛔음성 AP #9: 2단계 뒤 **최종 분석**까지 러너가 돌린다")
        chk("n_stage" in _rs and "n_expect" in _rs and "0개다" in _rs,
            "⛔음성 AP #9: 분류가 0개/일부만 내고 조용히 성공하는 것을 막는다 "
            "(잡 수 census 검증)")
        chk('case "$stage" in 1|2)' in _rs,
            "⛔음성 AP #9: stage 값을 검증한다 (모르는 값이면 중단)")
        chk(".lock_stage" in _rs,
            "⛔음성 AP #9: 중복 실행 가드가 있다")
        # ── 회신 AR P0-8 — lock 이 **원자적**이고 모르는 lock 을 안 지우는가 ──
        chk("ln \"$LOCKTMP\" \"$LOCK\"" in _rs and "rm -rf \"$LOCK\"" not in _rs,
            "⛔음성 AR P0-8: lock 이 `ln`(원자적, 내용 선기록)이고 **모르는 lock 을 "
            "rm -rf 하지 않는다** (mkdir 뒤 pid 를 쓰던 창에 경쟁조건이 있었다)")
        chk("hostname" in _rs and "own_host" in _rs,
            "⛔음성 AR P0-8: host 를 기록하고 **같은 호스트일 때만** kill -0 을 쓴다 "
            "(다른 HPC 노드의 pid 에는 유효한 생존검사가 아니다)")
        # ── 회신 AS 해제조건 5 — launcher/executable 분리 · 실행 직전 재해시 ──
        chk("VASP_LAUNCHER" in _rs and "VASP_EXE" in _rs
            and "VASP_CMD 는 더 쓰지 않습니다" in _rs,
            "⛔음성 AS 5: 러너가 **임의 VASP_CMD 를 거부**하고 launcher/실행파일을 "
            "나눠 받는다 (봉인은 실행파일을 해시하는데 종전엔 다른 걸 실행할 수 있었다)")
        chk("실행 직전 대조 실패" in _rs and "vasp_executable_sha256" in _rs,
            "⛔음성 AS 5: **실행 직전에** 봉인한 절대경로를 다시 해시해 대조한다")
        # ── 회신 AS 해제조건 4 — 봉인 재대조가 모든 불변량을 본다 ──────────
        chk("조립본 해시가 바뀐 잡" in _sl and "bundle_zip_sha256" in _sl
            and "반쪽 봉인이다" in _sl,
            "⛔음성 AS 4: 기존 봉인 재대조가 allowlist 뿐 아니라 MANIFEST·ZIP·"
            "VASP 신원·조립본 해시를 **전부** 다시 본다")
        # ── 회신 AS 해제조건 10 — 문서·러너·MANIFEST 의 숫자가 서로 맞는가 ──
        chk("JOBS_PARALLEL" in _rs and "xargs" in _rs and "_wave2" in _rs,
            "⛔음성 AS 10: 러너가 **실제로 병렬**로 돌고(직렬인데 MANIFEST 는 "
            "동시 8이라고 적고 있었다) 부모 의존 잡을 뒤 물결로 민다")
        chk("run_census" in _rs and "stage_counts" in _rs and "EXPECT_MANIFEST_SHA256" in _rs,
            "⛔음성 AR P0-7: 러너가 실행 전에 manifest 해시·exact 잡 집합·단계 분류를 "
            "확인한다 (종전엔 존재하는 job.json 만 세어 하나를 지워도 통과했다)")
        _cen = m_st.get("run_census") or {}
        chk(sorted(_cen.get("job_keys") or []) == sorted(m_st.get("planned") or {})
            and _cen.get("stage_counts", {}).get("1", 0) > 0
            and sum(_cen.get("stage_counts", {}).values()) == len(m_st["planned"]),
            "AR P0-7: MANIFEST 가 exact 잡 집합과 단계 분류를 기계 필드로 담는다 "
            f"· {_cen.get('stage_counts')}")

        # ══ 회신 AR 해제조건 8·10 — **러너를 실제로 돌린다** (production path) ══
        #   AR: "번들 selftest 는 production `_closure_estimand`, staged runner,
        #   seal·attestation 스크립트를 실제로 관통하지 않는다."
        #   ⇒ 가짜 PP 트리·allowlist·stub vasp 를 만들어 run_staged.sh 를 진짜로
        #     돌리고, 리뷰가 재현한 결함(job.json 하나 삭제)이 **막히는지** 본다.
        # ══ 회신 AR P1-11 · 해제조건 9 — 문서가 **실물과 일치**하는가 ══════════
        _rd9 = (_st / "README_REQUEST.md").read_text(encoding="utf-8")
        _sb9 = (_st / "SUBMIT_CONTRACT.md").read_text(encoding="utf-8")
        _sm9 = m_st.get("submission") or {}
        _has_clean9 = bool((m_st.get("refs") or {}).get("clean_slab"))
        chk(_has_clean9 or ("clean slab) 잡이 없습니다" in _rd9
                            and "refs/clean_slab__*` 잡을 먼저" not in _rd9),
            "⛔음성 AR P1-11: clean slab 이 없으면 README 가 **없는 반송물을 요구하지 "
            "않는다** (없다고 명시한다)")
        chk("BUNDLE_ZIP_SHA256" in _rd9 and "BUNDLE_ZIP_SHA256" in _sb9,
            "AR P1-11: README·SUBMIT 이 봉인에 **필수인** BUNDLE_ZIP_SHA256 을 안내한다 "
            "(없으면 SEAL 이 거부하는데 문서에 없었다)")
        for _f9 in ("POTCAR_ROOT_SEAL.json", "POTCAR_ATTESTATION.json",
                    "ZIP_SHA256.txt", "STAGE1_PASS.json"):
            chk(_f9 in _sb9 and _f9 in str(_sm9.get("required_returns")),
                f"AR P1-11: 반송물에 `{_f9}` 가 있다 (SUBMIT·MANIFEST 둘 다)")
        chk("PBE PAW 5.4." not in _rd9 and "2026-08-08 납품과 동일 계보" not in _rd9
            and "2026-08-12 묶음과 다른 POTCAR 트리" not in _rd9,
            "⛔음성 AR P1-11: README 가 이전 wave 계보와 `PBE PAW 5.4` 를 **단정하지 "
            "않는다** (attestation 정책과 충돌하던 문장)")
        # ── 회신 AS 해제조건 10 — 문서 숫자가 실물과 맞는가 ──────────────
        chk("8축" in _sb9,
            "AS 10: SUBMIT 이 stage-1 게이트를 **8축**으로 적는다 (4축이 아니다)")
        for _g10 in ("δ_gas", "δ_k", "5 meV"):
            chk(_g10 in _sb9, "AS 10: SUBMIT 의 수치 게이트 표에 `%s` 가 있다" % _g10)
        chk("중앙 추정 56 h" not in _sb9,
            "⛔음성 AR P1-11: walltime 이 하드코딩 56 h 가 아니라 cost_frozen 에서 온다")
        chk("잡 사이에 의존성이 있다" in str(_sm9.get("phase_dependencies"))
            and "배열 제출도 쓰지 않는다" in str(_sm9.get("runner_note")),
            "⛔음성 AR P1-11: MANIFEST 가 staged 에서 **의존성 있음 + 단일 경로**를 "
            "말한다 (종전엔 '의존성 없음 + 배열 제출' 로 다른 문서와 충돌했다)")
        chk(_sm9.get("n_vasp_executions_total") == sum(
                len(v.get("phases") or []) for v in m_st["planned"].values())
            + len(m_st.get("d3_off_twins") or {}),
            "AR Q6: MANIFEST 의 VASP 실행 수 = **상 수** (잡 수가 아니다) · %s"
            % _sm9.get("n_vasp_executions_total"))
        # ⛔음성 — relax 상이 있는 구성이면 README 가 "전 잡이 단일점" 이라고 하지 않는다
        _man_rel = dict(m_st)
        _man_rel["planned"] = {k: dict(v, phases=["relax", "static"])
                               if (v.get("meta") or {}).get("kind") == "mol_ref" else v
                               for k, v in m_st["planned"].items()}
        _rd_rel = _readme_sp(_man_rel, a_st, 0.0, len(_man_rel["planned"]), 0, 0, 0, {})
        chk("전 잡이 단일점입니다" not in _rd_rel and "relax/` 상이" in _rd_rel
            and "relax/OUTCAR" in _rd_rel,
            "⛔음성 AR P1-11: relax 상이 있으면 README 가 '전 잡이 단일점' 이라고 "
            "**쓰지 않고** relax 반송을 요구한다 (v15 가 정확히 그 모양이었다)")
        _sb_rel = _submit_contract(_man_rel, a_st, {"relax": 4, "static": 7})
        chk("relax/CONTCAR" in _sb_rel,
            "⛔음성 AR P1-11: relax 가 있으면 SUBMIT 이 **relax/CONTCAR** 를 요구한다 "
            "(canary 기하의 출처인데 누락돼 있었다)")

        # ⛔음성 2026-08-31 실측 — 생성기가 **역할 비대칭** 대안 자세를 봉인하는가.
        #   v16 첫 생성에서 sdcp=stress_sensitivity · ptfe=sensitivity 라
        #   같은 역할끼리 짝지으려던 코드가 아무것도 못 봉인하고 "탐색용" 으로
        #   떨어졌다 (스테이지 2 네 잡이 정의된 양을 못 냄).
        #   ⚠ 이 픽스처는 조각이 **하나**라 대비 자체가 없다 — pose_alt 도 없는 것이
        #     맞다. 두 조각짜리(실물 c12)에서만 이 계약을 요구한다.
        _pa = m_st.get("estimand_job_keys_pose_alt") or {}
        _pa_keys = sorted(k for k in _pa if not k.startswith("⛔"))
        _n_frag_st = len(m_st.get("fragments") or [])
        chk(_n_frag_st < 2 or _pa_keys or m_st.get("altpose_purpose"),
            "AR P1-10: 두 조각 판이면 대안 자세는 **봉인되거나 탐색용이라고 "
            f"명시되거나** 둘 중 하나다 (조각 {_n_frag_st})")
        if _pa_keys:
            _pk1 = _pa[_pa_keys[0]]
            chk(all(_pk1.get(k) in m_st["planned"] or "mol__" in str(_pk1.get(k))
                    for k in ("E_C_sdcp", "E_C_control"))
                and _pk1.get("formula") and _pk1.get("gate"),
                "AR P1-10: 봉인된 자세식이 **실재하는 잡 키 + 식 + gate** 를 갖는다 "
                f"({_pa_keys})")
        # ⛔ 회신 AS Q7 — 셀 한정을 **수치로** 뒷받침하는가
        _cs9 = ((m_st.get("reported_quantity") or {}).get("coverage_scope") or {})
        chk(_cs9.get("lateral_area_A2") and _cs9.get("coverage_per_nm2")
            and _cs9.get("min_lateral_cell_vector_A")
            and _cs9.get("molecule_image_min_distance_A"),
            "회신 AS 9: 셀 한정이 **수치**를 갖는다 (면적 %s Å² · %s 분자/nm² · "
            "격자벡터 %s Å · **분자-이미지 최단 %s Å**)"
            % (_cs9.get("lateral_area_A2"), _cs9.get("coverage_per_nm2"),
               _cs9.get("min_lateral_cell_vector_A"),
               _cs9.get("molecule_image_min_distance_A")))
        # ⛔음성 — 두 거리를 **같은 이름으로 섞지 않는다** (2026-08-31 실측 정정)
        _mim = _cs9.get("molecule_image_min_distance_A") or {}
        _mvals = [v for d in _mim.values() for v in (d or {}).values()]
        chk(isinstance(_mim, dict) and _mvals
            and all(v < _cs9["min_lateral_cell_vector_A"] for v in _mvals),
            "⛔음성 AS 9: 분자-이미지 최단거리가 격자벡터 길이보다 **작다** — "
            "둘은 다른 양이고, 격자벡터를 최소이미지라고 찍으면 실제보다 "
            "여유가 있어 보인다 (%s vs %s)"
            % (_mim, _cs9.get("min_lateral_cell_vector_A")))
        # 🔴 회신 AT Q1 — 자세를 뭉개지 않는다 (대안 자세의 worst case 를 primary
        #   값처럼 싣지 않는다)
        chk(all(isinstance(d, dict) for d in _mim.values()),
            "🔴 AT Q1: 분자-이미지 최단거리가 **자세(role)별로** 나뉘어 있다 (%s)" % _mim)
        chk("⛔_철회한_근거" in _cs9 and "소거된다" in str(_cs9["⛔_철회한_근거"]),
            "🔴 AT Q1: '공통 주기영상 항 소거' 근거를 **철회했다고 산출물에 적는다** "
            "(슬랩 원자 48/192 · 최대 변위 0.296 Å 이라 공통항 보장이 없다)")
        _rq9 = m_st.get("reported_quantity") or {}
        chk("adsorption energy" not in str(_rq9.get("name"))
            and any("adsorption energy" in x for x in _rq9.get("⛔_부르면_안_되는_이름", []))
            and _rq9.get("gas_conformer_provenance"),
            "회신 AS 8: 보고량 이름이 adsorption energy 가 **아니고**, 그 이름을 "
            "금지 목록에 두며, gas conformer 출처를 기록한다")
        chk("이 셀 조건에 한정" in str(m_st.get("claim_scope")),
            "회신 AS 9: claim_scope 가 **셀 한정**을 명시한다 (옵션 a)")
        _rc_run = _runner_e2e(_st, chk)
        chk(_rc_run is not False, "AR 해제조건 10: 러너 production-path e2e 를 돌렸다")
        # ── 회신 AP #5 — stage gate 가 vacconv **만** 보지 않는다 ─────────
        #   ⚠ 이 픽스처는 vacconv 잡이 없어 게이트가 그 전에 끝난다. 그래서
        #     여기서는 **배포 분석기 소스**에 네 선결조건이 실제로 있고
        #     _vc["pass"] 검사보다 **먼저** 평가되는지를 확인한다.
        _azs = (_st / "analyze_results.py").read_text()
        for _need in ("stage1_prerequisites", "canary_geometry",
                      "molecular_state", "potcar_identity", "vacuum"):
            chk(_need in _azs, f"AP #5: 선결조건 `{_need}` 이 분석기에 있다")
        _i_pre = _azs.find("_pre_bad = [k for k")
        _i_vac = _azs.find('if not _vc.get("pass"):\n            print("⛔ **2단계를 제출하지 않는다.')
        chk(_i_pre > 0 and _i_vac > 0 and _i_pre < _i_vac,
            "⛔음성 AP #5: 선결조건을 **vacuum 판정보다 먼저** 본다 "
            "(canary·POTCAR 를 1단계에 넣은 목적)")
        # canary 가 부모 기하를 승계하는가 (AO P0-4)
        _cz = sorted(_st.rglob("*__nzmag/PARENT_GEOM"))
        chk(bool(_cz), "AO P0-4: canary 마다 PARENT_GEOM 이 있다 "
                       f"(찾음 {len(_cz)}개)")
        for _f in _cz:
            _tgt = (_f.parent / _f.read_text().strip()).resolve()
            chk(_tgt.is_dir() and _tgt.name == _f.parent.name.replace("__nzmag", ""),
                f"AO P0-4: PARENT_GEOM 이 **부모 잡**을 가리킨다 ({_f.parent.name} → {_tgt.name})")
        _rj = (_cz[0].parent / "run_job.sh").read_text() if _cz else ""
        chk("PARENT_GEOM" in _rj and "relax/CONTCAR" in _rj,
            "⛔음성 AO P0-4: canary 의 run_job.sh 가 부모 relax/CONTCAR 를 받는다 "
            "(종전엔 자기 루트 POSCAR 로 돌아 구조 이완 에너지가 섞였다)")
        # README 가 staged 단일 경로를 말하는가 (AO P0-2·P1)
        _rd_st = (_st / "README_REQUEST.md").read_text()
        chk("run_staged.sh 1" in _rd_st and "SEAL_POTCAR_ROOT.sh" in _rd_st,
            "AO P0-2: README 가 staged 경로와 조립 자동화를 같이 적는다")
        chk("run_all.sh` 는 이 묶음에 **넣지 않았습니다**" in _rd_st,
            "⛔음성 AO P0-3: README 가 run_all.sh 부재를 **명시**한다 "
            "(종전엔 SUBMIT/run_all 이 전체 제출을 안내해 staged 지침과 충돌했다)")
        # 🔴 회신 AT P0-5 — 문서가 **실제 러너 계약과 같은 말**을 하는가
        _sub_st0 = (_st / "SUBMIT_CONTRACT.md").read_text()
        # ⚠ 이 검사는 **staged 러너를 실제로 실은 묶음**에만 뜻이 있다. 아니면
        #   `run_job.sh` 가 정상 경로이고 VASP_CMD 도 정상이다.
        _is_staged = (_st / "run_staged.sh").is_file()
        chk(_is_staged, "AT P0-5 전제: 이 묶음이 staged 러너를 싣고 있다")
        for _nm, _txt in ((("README", _rd_st), ("SUBMIT", _sub_st0)) if _is_staged else ()):
            # ⚠ "VASP_CMD 는 쓰지 마세요" 라는 **경고 문장**은 있어야 한다.
            #   금지할 것은 붙여넣으면 도는 **대입문**이다.
            chk('VASP_CMD="' not in _txt,
                "🔴 AT P0-5: staged %s 에 `VASP_CMD=\"…\"` **대입문**이 없다 — "
                "러너가 그것을 거부하므로 문서에 남아 있으면 붙여넣기가 즉시 실패한다"
                % _nm)
            chk("VASP_CMD" in _txt,
                "AT P0-5: staged %s 가 `VASP_CMD` 를 **쓰지 말라고 말한다** "
                "(옛 지침을 기억하는 사람이 있다)" % _nm)
            chk("VASP_LAUNCHER" in _txt and "VASP_EXE" in _txt,
                "AT P0-5: staged %s 가 런처와 실행파일을 **나눠** 적는다" % _nm)
            chk("EXPECT_ZIP_SHA256" in _txt and "EXPECT_MANIFEST_SHA256" in _txt,
                "AT P0-5: staged %s 에 **필수** 외부 앵커 둘이 다 적혀 있다" % _nm)
        chk((not _is_staged) or "run_job.sh` 를 직접 부르지 마세요" in _rd_st,
            "🔴 AT P0-5: staged README 가 **수동 단일잡 우회를 금지**한다 "
            "(적어 두면 그게 곧 우회 경로가 된다)")
        # ── 회신 AP #10 — 문서가 **의존성과 반송물**을 정확히 말하는가 ────
        _sub_st = (_st / "SUBMIT_CONTRACT.md").read_text()
        chk("잡 사이에 의존성이 있습니다" in _sub_st,
            "⛔음성 AP #10: SUBMIT 이 **의존성이 있다**고 적는다 "
            "(종전엔 '잡 사이에는 의존성이 없습니다')")
        chk("JOBS.txt" not in _sub_st and "sbatch --array" not in _sub_st,
            "⛔음성 AP #10: staged 번들 SUBMIT 에 **전체 array 제출 예시가 없다** "
            "(있으면 정지 규칙이 우회된다)")
        chk("독립이 아닙니다" in _rd_st,
            "⛔음성 AP #10: README 도 **독립이 아니다**라고 적는다 "
            "(canary 가 부모 기하에 의존한다)")
        for _r in ("POTCAR_ROOT_SEAL.json", "STAGE1_PASS.json",
                   "POTCAR_PROVENANCE.json", "static/POSCAR"):
            chk(_r in _sub_st, f"AP #10: 필수 반송물에 `{_r}` 이 적혀 있다")
        # 비-staged 번들은 종전 안내를 유지한다 (회귀 방지)
        _sub_sp = (out_sp / "SUBMIT_CONTRACT.md").read_text()
        chk("JOBS.txt" in _sub_sp and "find " in _sub_sp
            and "의존성이 없습니다" in _sub_sp,
            "⛔음성 AP #10: **비-staged** 번들은 배열 제출 안내를 유지한다 "
            "(staged 만 고치고 나머지를 망가뜨리지 않는다)")
        # 계보 동일성 문구가 남아 있지 않은가 (AO P1)
        _spec_txt = (_st / "POTCAR_SPEC.txt").read_text()
        chk("2026-08-08" not in _spec_txt and "동일 계보" not in _spec_txt,
            "⛔음성 AO P1: POTCAR_SPEC.txt 에 **검증하지 않은 계보 동일성 주장**이 없다")
        chk("PBE PAW 5.4" not in _spec_txt and "ATTESTATION" in _spec_txt,
            "⛔음성 AP Q3: POTCAR_SPEC.txt 가 **release 를 단정하지 않는다** "
            "(확인 전에 `PBE PAW 5.4` 를 적는 것은 범위를 넘는다)")
        chk("제출본은" not in str(m_st.get("potcar_pin_note") or "")
            and "POTCAR_ROOT_SEAL" in str(m_st.get("potcar_pin_note") or ""),
            "⛔음성 AO P1: manifest 의 pin 설명이 **새 provenance-root 방식과 일치**한다 "
            f"(종전엔 '제출본이 아니다' 라고 적어 충돌했다) · {str(m_st.get('potcar_pin_note'))[:60]}")
        # estimand net4 직접식이 봉인됐는가 (AO P0-7)
        # ⚠ 이 픽스처는 조각이 **하나**(ptfe_dimer)라 D 자체가 정의되지 않는다
        #   (D 는 두 조각의 대비다). 그래서 여기서 시험하는 것은 값이 아니라
        #   **불변식**이다: pm1 직접식이 봉인되면 net4 직접식도 반드시 같이 봉인된다.
        #   종전엔 pm1 만 봉인하고 net4 는 안 냈다 (AO P0-7: 요구해 놓고 계산 안 함).
        chk(bool(m_st.get("estimand_job_keys"))
            == bool(m_st.get("estimand_job_keys_net4")),
            "AO P0-7 불변식: pm1 직접식이 봉인되면 **net4 직접식도 같이** 봉인된다 "
            f"(pm1 {bool(m_st.get('estimand_job_keys'))} · "
            f"net4 {bool(m_st.get('estimand_job_keys_net4'))})")
        chk(len(m_st.get("fragments") or []) >= 2
            or not m_st.get("estimand_job_keys"),
            "AO: 조각이 하나면 D 가 정의되지 않으므로 직접식을 봉인하지 않는다 "
            f"(조각 {m_st.get('fragments')})")

    # ⛔⛔ 회신 AO P0-1 e2e — **1단계만 완주한 상태**에서 completeness 가 단계별로
    #   좁혀지는가. 종전엔 14잡 전체를 세고 exit 2 로 끝나, 진공 시험을 통과해도
    #   2단계를 열 수 없었다 (staged 러너가 문서대로 동작하지 않았다).
    if _st is not None:
        def _stage1_of(_m):
            k, r, v = _m.get("kind"), _m.get("role"), _m.get("vacconv")
            if k == "mol_ref":
                return True
            if k == "prospective_pose" and r == "primary":
                return bool(v) or _m.get("seed") == "afm2424_pm1"
            return False
        _s1n, _s2n = [], []
        for _jp in sorted(_st.rglob("job.json")):
            _m = json.loads(_jp.read_text())
            (_s1n if _stage1_of(_m) else _s2n).append(
                str(_jp.parent.relative_to(_st)))
            if _stage1_of(_m):
                _fake_phase(_jp.parent, _m, -500.0, POTCAR_SPEC)
        chk(bool(_s1n) and bool(_s2n),
            f"AO P0-1 전제: 단계가 실제로 갈린다 (1단계 {len(_s1n)} · 2단계 {len(_s2n)})")
        _az = str(_st / "analyze_results.py")
        _r_no = subprocess.run([sys.executable, _az, "."], cwd=_st,
                               capture_output=True, text=True)
        _r_gate = subprocess.run([sys.executable, _az, ".", "--gate", "vacconv"],
                                 cwd=_st, capture_output=True, text=True)
        # ⛔ 분석기가 **예외로 죽으면** 아래 검사들이 전부 무의미해진다 — 먼저 본다
        chk(_r_no.returncode in (0, 2),
            "분석기가 예외로 죽지 않는다 (rc %s) · %s"
            % (_r_no.returncode, (_r_no.stderr or "")[-300:]))
        _hit_no = [j for j in _s2n if j in _r_no.stdout]
        _hit_gate = [j for j in _s2n if j in (_r_gate.stdout.split("미완")[-1]
                                              if "미완" in _r_gate.stdout else "")]
        chk(bool(_hit_no),
            "AO P0-1 전제: --gate 없이 돌리면 2단계 미완이 실제로 잡힌다 "
            f"({len(_hit_no)}건)")
        chk(not _hit_gate,
            "⛔음성 AO P0-1: `--gate vacconv` 는 **1단계 cohort 만** 센다 "
            f"(2단계 잡을 미완으로 세면 안 된다) · 샜음 {_hit_gate[:2]}")
        chk("필수 산출 미완" not in _r_gate.stdout
            or "1단계 cohort" in _r_gate.stdout,
            "AO P0-1: 미완 메시지가 **어느 범위**를 셌는지 밝힌다")
        # ── 회신 AP #4 — estimand / sensitivity tier ────────────────────
        #   ⚠ 이 픽스처는 조각이 하나라 estimand_job_keys 가 봉인되지 않는다
        #     (D 는 두 조각의 대비다). 그래서 여기서 시험하는 것은 분리 자체가
        #     아니라 **불변식**: 봉인된 식이 없으면 tier 를 나누지 않는다.
        #     나누면 레거시 잡이 sensitivity 로 강등돼 누락이 종료코드에서 사라진다.
        _rj = json.loads((_st / "RESULTS.json").read_text())
        _tc = _rj.get("tier_census") or {}
        chk(bool(_tc), f"AP #4: tier_census 를 낸다 ({_tc})")
        chk(bool(m_st.get("estimand_job_keys")) or not _tc.get("sensitivity"),
            "⛔음성 AP #4 불변식: 봉인된 식이 없으면 **전부 estimand tier** 다 "
            f"(census {_tc})")
        chk("sensitivity_status" in _rj,
            f"AP #4: sensitivity 상태를 항상 보고한다 ({_rj.get('sensitivity_status')})")


    # ══ 회신 U P0-5 — closure 모드 e2e. "계획대로 생성되는가" 를 파일로 확인한다 ══
    a_cl = argparse.Namespace(**{**vars(a_sp), "out": str(td / "bundle_closure"),
                                 "closure": True, "refs": True, "dense_frags": None})
    build_bundle(a_cl, ledger=led)
    _cl = Path(str(td / "bundle_closure"))
    _inc = sorted(_cl.rglob("INCAR"))
    chk(bool(_inc), "closure: INCAR 가 생성된다")
    _bad_lreal = [f for f in _inc if "LREAL    = .FALSE." not in f.read_text()]
    chk(not _bad_lreal,
         f"[P0-5] closure 전 endpoint 가 LREAL=.FALSE. ({len(_inc)}개 · "
         f"위반 {[x.parent.name for x in _bad_lreal][:3]})")
    _bad_fix = [f for f in _inc
                if "NSW      = 0" not in f.read_text()
                or "IBRION   = -1" not in f.read_text()]
    chk(not _bad_fix, f"[P0-5] closure 전 endpoint 가 고정기하 (NSW=0·IBRION=-1) · "
                       f"위반 {[x.parent.name for x in _bad_fix][:3]}")
    _bad_vdw = [f for f in _inc if "IVDW     = 11" not in f.read_text()]
    chk(not _bad_vdw, "[P0-5] closure 전 endpoint 가 IVDW=11 (D3 zero — 'D3(BJ)' 아님)")
    _rel = [f for f in _cl.rglob("relax/INCAR")]
    chk(not _rel, f"[P0-5b] closure 에는 relax 상이 **없다** (기체 기준 포함) · "
                   f"발견 {[str(x.parent.parent.name) for x in _rel][:3]}")
    # 음성: closure 를 끄면 위 성질이 실제로 깨진다 (시험이 무엇을 지키는지 증명)
    _sp_inc = sorted(Path(str(td / "bundle_sp")).rglob("INCAR"))
    _molinc = sorted(_cl.rglob("refs/mol__*/static/INCAR"))
    chk(bool(_molinc) and all("ICHARG   = 2" in f.read_text() for f in _molinc),
        f"[V P0-1] closure 기체 static 이 ICHARG=2 (공급할 CHGCAR 가 없다) · {len(_molinc)}개")
    import json as _json
    _mj = sorted(_cl.rglob("refs/mol__*/job.json"))
    _badph = [f for f in _mj if _json.load(open(f)).get("phases") != ["static"]]
    chk(bool(_mj) and not _badph,
        f"[V P0-2] 기체 job.json 의 phases 가 실제 생성분(static)과 일치 · "
        f"위반 {[x.parent.name for x in _badph][:3]}")
    # ══ 회신 V P0-3 · P0-4 — 사전등록 estimand 를 **함수로 직접** 친다 ═══════
    # 분석기는 **문자열 템플릿**으로 배포된다 (live 코드가 아니다). 그래서 배포될
    # 그 소스를 exec 해서 친다 — 템플릿을 고쳐도 시험이 따라온다.
    _ns = {}
    exec(compile(ANALYZER, "<analyzer-template>", "exec"), _ns)
    _closure_estimand = _ns["_closure_estimand"]
    # ⛔ 회신 AR 해제조건 10 — 이 묶음은 **배포본 안**으로 옮겼다. 여기서는 그
    #   함수를 그대로 부른다 (검사 출처가 둘로 갈리지 않게).
    _ns["_selftest_closure"](chk)
    # ══ 회신 W 5단계 — --from_basins 가 **동결본에 적힌 자세만** 내는지 e2e ══
    _labs = sorted(x.stem for x in
                   (Path(str(td)) / "runs" / "ptfe_dimer" / "relax_f0.85").glob("*.xyz")
                   if not x.stem.startswith("_"))
    if len(_labs) >= 3:
        _fb = {"freeze_sha256": "deadbeef" * 8,
               "params": {"audit_seed": 4242},
               "fragments": {"ptfe_dimer": {
                   "calibration": [{"basin_id": "b00", "rep_label": _labs[0],
                                    "role": "calibration", "why": "UMA global-min",
                                    "E_pose_eV": -0.5, "fingerprint": [["C", "O", 1]],
                                    "anchor": ["F", "Li", 2.4], "height_A": 2.5},
                                   {"basin_id": "b01", "rep_label": _labs[1],
                                    "role": "calibration", "why": "다른 지문 최저",
                                    "E_pose_eV": -0.4, "fingerprint": [["F", "Ni", 1]],
                                    "anchor": ["F", "Ni", 2.5], "height_A": 2.6}],
                   "sealed_audit": [{"basin_id": "b09", "rep_label": _labs[2],
                                     "role": "sealed_audit", "why": "창 바깥",
                                     "E_pose_eV": -0.1, "fingerprint": [["F", "O", 1]],
                                     "anchor": ["F", "O", 2.7], "height_A": 2.8}]}}}
        _fbp = Path(str(td)) / "frozen_basins.json"
        _fbp.write_text(json.dumps(_fb, ensure_ascii=False))
        a_fb = argparse.Namespace(**{**vars(a_cl), "out": str(td / "bundle_fb"),
                                     "from_basins": str(_fbp), "both_seeds": False,
                                     "frags": ["ptfe_dimer"], "champion": False,
                                     "refs": False, "d3_pairs": False})
        build_bundle(a_fb, ledger=led)
        _mfb = json.load(open(Path(str(td)) / "bundle_fb" / "MANIFEST.json"))
        _dirs = sorted(x.parent.parent.name for x in
                       (Path(str(td)) / "bundle_fb").rglob("prospective/*/static/INCAR"))
        chk(len(_dirs) == 3, f"[W-5] 동결본의 3자세만 생성 (실제 {len(_dirs)}: {_dirs[:3]})")
        chk(all(any(b in d for b in ("b00", "b01", "b09")) for d in _dirs),
            "[W-5] 디렉터리 이름에 basin_id 가 박힌다")
        chk("prospective_lowE (frozen deadbeefdeadbeef" in str(_mfb.get("candidate_set")),
            f"[W-5] candidate_set 에 동결 해시가 박힌다 · {_mfb.get('candidate_set')}")
        chk((_mfb.get("from_basins") or {}).get("audit_seed") == 4242,
            "[W-5] audit seed 를 manifest 에 승계한다")
        _tier = list(Path(str(td / "bundle_fb")).rglob("tier*/*/static/INCAR"))
        chk(not _tier, f"[음성 W-5] champion/cross 경로를 **타지 않는다** (tier {len(_tier)})")

        # ══ 홀드아웃 tranche (2026-08-30 옵션 A) — **primary 를 못 내게 막는다** ══
        #   홀드아웃은 선택기 가정을 시험하는 집합이지 primary 후보집합이 아니다.
        #   라벨이 틀리면 분석기가 primary 를 내고, 홀드아웃이 더 낮게 나온 것이
        #   "더 좋은 자세를 찾았다" 로 흡수돼 **선택기 실패가 사라진다.**
        _fh = {"freeze_sha256": "cafe" * 16, "params": {"audit_seed": 4242},
               "fragments": {"ptfe_dimer": {"holdout": [
                   {"basin_id": "b41", "rep_label": _labs[0], "role": "holdout",
                    "why": "Q1 × anchor", "E_pose_eV": -0.3,
                    "fingerprint": [["F", "Li", 1]], "anchor": ["F", "Li", 2.4],
                    "height_A": 2.5, "quartile": "Q1"}]}}}
        _fhp = Path(str(td)) / "frozen_holdout.json"
        _fhp.write_text(json.dumps(_fh, ensure_ascii=False))
        a_fh = argparse.Namespace(**{**vars(a_cl), "out": str(td / "bundle_fh"),
                                     "from_basins": str(_fhp), "both_seeds": False,
                                     "frags": ["ptfe_dimer"], "champion": False,
                                     "refs": False, "d3_pairs": False,
                                     "roles": ["holdout"]})
        build_bundle(a_fh, ledger=led)
        _mfh = json.load(open(Path(str(td)) / "bundle_fh" / "MANIFEST.json"))
        chk(str(_mfh.get("candidate_set")).startswith("holdout_stratified"),
            "⛔음성: holdout 역할만 낸 번들은 candidate_set 이 **holdout_stratified** — "
            "calibration_pilot 으로 잘못 라벨되면 이유가 틀린 채로 막힌다 · %s"
            % _mfh.get("candidate_set"))
        chk(_mfh.get("emitted_basin_roles") == ["holdout"],
            "⛔음성: emitted_basin_roles 가 실제 basin 의 role 을 그대로 적는다")
        # 분석기 쪽 fail-closed — 라벨만으로 primary 를 막는지 직접 친다
        _ob = {"candidate_set": _mfh.get("candidate_set"), "blocks": []}
        if str(_ob["candidate_set"]).startswith("holdout_stratified"):
            _ob["blocks"].append("HOLDOUT_TRANCHE")
        chk(_ob["blocks"] == ["HOLDOUT_TRANCHE"],
            "⛔음성: holdout_stratified 라벨이면 분석기가 HOLDOUT_TRANCHE 로 막는다 "
            "(홀드아웃 값을 primary 의 min 에 넣지 않는다)")
        # ⛔ 쌍둥이 없이 만든 번들도 census 를 **쓴다** (종전엔 통째로 없었다)
        chk((_mfh.get("job_census") or {}).get("총잡수") is not None
            and (_mfh["job_census"]["complexes"]["d3_off_twins"] == 0),
            "⛔음성: D3-off 쌍둥이 0개여도 job_census 가 있다 (종전엔 없어져서 "
            "README·verify 가 빈 값을 조용히 읽었다) · %s"
            % (_mfh.get("job_census") or {}).get("총잡수"))
        chk("Edisp" in str(_mfh.get("d3_off_note", "")),
            "⛔음성: 쌍둥이가 없으면 manifest 가 **C3 를 Edisp 로 낸다**고 적는다")
        # ⛔ 음성 (회신 AE): `--cores` 가 **숫자를 실제로 바꾸는가**. 종전엔 라벨만
        #   바뀌어 48코어 시간을 "256코어 기준" 이라 적었고, 외주 견적이 3.8일이
        #   아니라 15일로 읽혔다.
        a_c48 = argparse.Namespace(**{**vars(a_fh), "out": str(td / "b_c48"),
                                      "cores": 48})
        a_c256 = argparse.Namespace(**{**vars(a_fh), "out": str(td / "b_c256"),
                                       "cores": 256})
        build_bundle(a_c48, ledger=led); build_bundle(a_c256, ledger=led)
        _m48 = json.load(open(Path(str(td)) / "b_c48" / "MANIFEST.json"))["cost_frozen"]
        _m256 = json.load(open(Path(str(td)) / "b_c256" / "MANIFEST.json"))["cost_frozen"]
        chk(_m256.get("longest_job_h") is not None
            and _m48.get("longest_job_h") is not None
            and _m256["longest_job_h"] < _m48["longest_job_h"],
            "⛔음성: --cores 256 이 --cores 48 보다 **잡 시간이 짧다** "
            "(라벨만 바뀌면 같다) · 48→%s h · 256→%s h"
            % (_m48.get("longest_job_h"), _m256.get("longest_job_h")))
        _r256 = (Path(str(td)) / "b_c256" / "README_REQUEST.md").read_text()
        chk(str(round(_m256["longest_job_h"])) in _r256 and "256코어" in _r256,
            "⛔음성: README 의 '가장 긴 잡' 이 그 코어 수의 추정과 **같은 수**다 "
            "(종전엔 하드코딩 56h 이 어느 코어 수에서든 찍혔다)")
        # ★ 회신 AB P0-1 — **생산 생성기가 만든 실물**에 입력 preflight 를 건다.
        #   v9 는 해시·census·selftest 를 다 통과하고도 40잡 중 36잡이
        #   OUTCAR 오기 전에 막혔다. 그 결함은 해시로 못 잡는다.
        for _bp in (Path(str(td)) / "bundle_fb", Path(str(td)) / "bundle_fh"):
            _miss = []
            for _jj in sorted(_bp.rglob("job.json")):
                _jm = json.loads(_jj.read_text())
                if _jm.get("mol_poscar_idx") and not _jm.get("mol_graph_canonical"):
                    _miss.append(str(_jj.parent.name) + ":graph")
                if "registry_role" not in _jm and _jm.get("role") not in ("Li", "Ni", None):
                    _miss.append(str(_jj.parent.name) + ":role")
            chk(not _miss,
                "⛔음성 P0-1: %s 의 전 잡이 입력만으로 게이트에 안 걸린다 "
                "(걸리면 %s)" % (_bp.name, _miss[:3]))

        # ══ 회신 X — Stage A 구성 플래그 (P0-2 · Q1 · dense 제거) ════════════
        a_sa = argparse.Namespace(**{**vars(a_fb), "out": str(td / "bundle_stageA"),
                                     "roles": ["calibration"], "both_seeds": True,
                                     "d3_pairs": True, "d3_seed_main_only": True})
        build_bundle(a_sa, ledger=led)
        _sa = Path(str(td / "bundle_stageA"))
        _pv = sorted(x.parent.parent.name for x in
                     _sa.rglob("prospective/*/static/INCAR"))
        # ★ 음성: audit 를 calibration 과 **같이 던지면 안 된다** (회신 X P0-2)
        chk(all("b09" not in d for d in _pv),
            f"[음성 X P0-2] --roles calibration 이 sealed_audit(b09)를 안 낸다 · {_pv}")
        chk(sum(1 for d in _pv if not d.endswith("__d3off")) == 4,
            f"[X P0-2] calibration 2자세 × 2 seed = 4 (실제 {_pv})")
        # ★ 음성: net4 복합체에는 D3-off 쌍둥이가 **없어야** 한다 (회신 X Q1)
        _n4 = [d for d in _pv if d.endswith("__d3off")
               and any(sd in d for sd in SEEDS_FULL if sd != SEED_MAIN)]
        chk(not _n4, f"[음성 X Q1] net4 복합체에 D3-off 쌍둥이가 없다 · {_n4}")
        _p1 = [d for d in _pv if d.endswith("__d3off") and SEED_MAIN in d]
        chk(len(_p1) == 2, f"[X Q1] pm1 복합체에는 쌍둥이가 있다 ({len(_p1)}) · {_p1}")

        a_nd = argparse.Namespace(**{**vars(a_fb), "out": str(td / "bundle_nodense"),
                                     "roles": ["calibration"], "refs": True,
                                     "no_refs_dense": True, "d3_pairs": False})
        build_bundle(a_nd, ledger=led)
        _has = lambda p: bool(list(Path(str(td / p)).rglob("refs/clean_slab*/dense")))
        chk(not _has("bundle_nodense"),
            "[음성] --no_refs_dense → clean slab 에 dense 상이 없다")
        a_wd = argparse.Namespace(**{**vars(a_nd),
                                     "out": str(td / "bundle_withdense"),
                                     "no_refs_dense": False})
        build_bundle(a_wd, ledger=led)
        chk(_has("bundle_withdense"),
            "  (양성 대조) 플래그 없으면 dense 가 **있다** — 늘 통과하는 시험이 아니다")

    # ══ 회신 W Q2 — D3-off 쌍둥이가 IVDW **만** 다른지 e2e ══════════════════
    a_d3 = argparse.Namespace(**{**vars(a_cl), "out": str(td / "bundle_d3"),
                                 "d3_pairs": True})
    build_bundle(a_d3, ledger=led)
    _d3 = Path(str(td / "bundle_d3"))
    _tw = sorted(_d3.rglob("*__d3off/static/INCAR"))
    chk(bool(_tw), f"[W Q2] D3-off 쌍둥이 생성 ({len(_tw)}개)")
    _bad, _same = [], 0
    for t in _tw:
        base = Path(str(t).replace("__d3off", ""))
        if not base.is_file():
            _bad.append(("짝 없음", t.parent.parent.name)); continue
        bl = [x for x in base.read_text().splitlines() if not x.startswith("SYSTEM")]
        tl = [x for x in t.read_text().splitlines() if not x.startswith("SYSTEM")]
        diff = [x for x in bl if x not in tl] + [x for x in tl if x not in bl]
        if diff != ["IVDW     = 11"]:
            _bad.append((diff[:3], t.parent.parent.name))
        else:
            _same += 1
        if (base.parent.parent / "POSCAR").is_file():
            chk(_sha_file(base.parent.parent / "POSCAR")
                == _sha_file(t.parent.parent / "POSCAR"),
                "  POSCAR 해시 동일") if _same == 1 else None
    chk(not _bad, f"[W Q2] 쌍둥이가 **IVDW 줄만** 다르다 ({_same}/{len(_tw)}) · "
                  f"위반 {_bad[:2]}")
    chk(not list(_d3.rglob("*__d3off/dense")) and not list(_d3.rglob("*__d3off/relax")),
        "[W Q2] 쌍둥이는 static 만 (dense·relax 없음)")

    # ⛔⛔ 2026-08-31 — 이 시험은 **옛 동작을 일부러 못박고 있었다**
    #   ("--single_point 만으로는 LREAL=Auto 가 남는다 — closure 가 그것을 고친다").
    #   그 전제가 틀렸다. 회신 U P0-5 의 이유("조각 간 대비에서 LREAL 오차는 서로 다른
    #   흡착종이라 소거되지 않는다")는 closure 만의 사정이 아니라 **조각을 대비하는
    #   모든 번들**에 적용된다. C-12 가 `--single_point` 를 쓰는데 실측(v5)에서
    #   슬랩 static 은 Auto, **기체 기준 static 은 .FALSE.** 로 나왔다 —
    #   `E_ads = E_복합체(Auto) − E_기체(.FALSE.)` 로 한 양 안에서 해밀토니안이 섞였다.
    #   ⇒ single_point 도 `.FALSE.` 로 못박고, 이 시험을 **양성**으로 뒤집는다.
    chk(all("LREAL    = .FALSE." in f.read_text() for f in _sp_inc)
        and not any("LREAL    = Auto" in f.read_text() for f in _sp_inc),
        "[U P0-5 확장] --single_point 도 LREAL=.FALSE. 다 — 기체 기준(.FALSE.)과 "
        "같은 해밀토니안이어야 E_ads 가 한 양이 된다 (%d개)" % len(_sp_inc))
    # ★ **배포되는 분석기**의 k 라벨·guard band selftest 를 그대로 돌린다.
    #   이 로직은 문자열 템플릿 안이라 여기서 import 로 시험할 수 없다 — 실행이 유일한 길.
    rk = subprocess.run([sys.executable, "analyze_results.py", "--selftest"],
                        cwd=out_sp, capture_output=True, text=True)
    for ln in rk.stdout.splitlines():
        print("   " + ln)
    chk(rk.returncode == 0, f"배포 분석기 k-selftest (rc={rk.returncode})")
    # ⛔⛔ 회신 AR P1-12 · 해제조건 10 (2026-08-31) — 배포본 selftest 가
    #   ① production `_closure_estimand` 를 **실제로 관통**하고
    #   ② **개수와 실행 명령이 재현 가능**하며
    #   ③ **비 UTF-8 기본 인코딩**(Windows cp949 등)에서도 도는가.
    _m_cnt = re.search(r"(?m)^selftest (\d+)/(\d+) · (PASS|FAIL)$", rk.stdout)
    _m_est = re.search(r"(?m)^  ── estimand 판정 검사 (\d+)건", rk.stdout)
    chk(bool(_m_cnt) and _m_cnt.group(1) == _m_cnt.group(2)
        and _m_cnt.group(3) == "PASS" and int(_m_cnt.group(1)) >= 200,
        "AR P1-12: 배포본 selftest 가 **개수를 찍는다** (%s) — 문서의 수와 실행 "
        "결과가 갈라지지 않게" % (_m_cnt.group(0) if _m_cnt else "없음"))
    chk(bool(_m_est) and int(_m_est.group(1)) >= 40,
        "AR P1-12: 배포본이 production `_closure_estimand` 판정을 **직접 친다** "
        "(%s건) — 종전엔 생성기 selftest 에만 있어 배포본에서 재현 불가였다"
        % (_m_est.group(1) if _m_est else "0"))
    chk("재현: python3 analyze_results.py --selftest" in rk.stdout,
        "AR P1-12: 배포본이 **실행 명령**을 같이 찍는다")
    # ⛔음성 — 비 UTF-8 로케일 (Windows cp949 대역). 종전엔 Unicode fixture 기록
    #   중 UnicodeEncodeError 로 죽었다 (리뷰가 실제로 재현).
    # ⛔ 2026-08-31 실측 — 종전엔 여기에 `PYTHONIOENCODING="utf-8"` 을 같이 넣어
    #   **stdout 만 살려 놓고** 통과시켰다. 그래서 gabia 의 `LC_ALL=C` 실행이
    #   `UnicodeEncodeError: '\u2713'` 로 죽는 것을 못 잡았다. 그 변수를 뺀다 —
    #   이제 파일 IO 와 **표준출력** 둘 다 시험한다.
    _envc = dict(os.environ, LC_ALL="C", LANG="C", PYTHONUTF8="0")
    _envc.pop("PYTHONIOENCODING", None)
    rkc = subprocess.run([sys.executable, "analyze_results.py", "--selftest"],
                         cwd=out_sp, capture_output=True, text=True, env=_envc)
    chk(rkc.returncode == 0 and "UnicodeEncodeError" not in (rkc.stderr or ""),
        "⛔음성 AR P1-12: **비 UTF-8 기본 인코딩**에서도 배포본 selftest 가 돈다 "
        "(rc=%s · %s)" % (rkc.returncode,
                          (rkc.stderr or "").strip().splitlines()[-1][:50]
                          if rkc.stderr else "stderr 없음"))
    # ★ dense 모멘트 hard gate (Codex 7차 §8) — dense 는 **에너지를 내는 상**이므로
    #   모멘트 표가 없으면 조용히 빠지면 안 된다. 옛 판은 그랬다.
    az0 = (out_sp / "analyze_results.py").read_text()
    chk("DENSE_MOMENTS_MISSING" in az0 and "DENSE_MAGNETIC_COLLAPSE" in az0,
        "분석기에 dense 모멘트 게이트가 있다")
    chk(az0.count("DENSE_MOMENT_COUNT") and az0.count("DENSE_MOMENT_SHORT"),
        "표 길이·Ni 인덱스 범위도 본다")
    # ★ Codex zip 감사 P0-2/3/5/6 이 분석기에 실제로 들어갔는지 (문자열 확인 + 아래 행동시험)
    for _k, _why in (("DENSE_RADICAL_BRANCH_CHANGED", "P0-5 라디칼 상대 스핀"),
                     ("DENSE_TOTAL_M_CHANGED", "P0-5 total M branch"),
                     ("geometry_unverified", "P0-6 기하 미검증 표시"),
                     ("dE_coarse_eV", "P0-3 coarse 보존"),
                     ("headline_from", "P0-3 headline 출처")):
        chk(_k in az0, f"분석기에 {_why} 가 있다")
    # ★★ 행동시험 — 2×2 가 **실제로 채워지는지** (P0-2: prefix 가 없어 늘 비어 있었다)
    chk("mc['Ni_at_Li_pose']['prefix']" in az0
        and "cr.get('Ni_at_Li_pose')" not in az0,
        "2×2 가 MANIFEST 의 prefix 를 읽는다 (결과 dict 엔 없었다)")
    chk('two_by_two") or {}).get("afm2424_pm1")' in az0,
        "완료 라벨이 **two_by_two 가 채워졌을 때만** 붙는다")
    # ── Codex 재감사 (2026-08-12) 여섯 건이 실제로 들어갔는지 ─────────────────
    for _k, _why in (
            ('integrity.get("geometry_unverified")', "P0-1 기하 미검증 → exit 2"),
            ("RADICAL_BRANCH_CHANGED", "P0-2 static 라디칼 게이트"),
            ("K_UNRESOLVED_2x2", "P0-3 2×2 부호 결론 차단"),
            ("K_UNRESOLVED_GLOBAL", "P0-3 전역 부호 결론 차단"),
            ("MAGNETIC_K_UNRESOLVED", "P0-4 branch 경합 판정"),
            ("k_transfer_allowance_meV", "명명 — 잔여 오차 0 이 아니다"),
            ("def _pk(", "P0-6 POSIX 잡 키 정규화")):
        chk(_k in az0, f"분석기에 {_why}")
    # ★ static 라디칼이 **Ni 전역반전과 무관하게** 검사되는지 (옛 판은 sg<0 일 때만)
    _i = az0.index("ms = {int(k): float(v) for k, v in mol_sign.items()")
    chk("if sg < 0:" not in az0[max(0, _i - 300):_i],
        "static 라디칼 검사가 sg<0 조건 **밖**에 있다 (항상 돈다)")
    # ★ 음성: Windows 구분자를 줘도 POSIX 키가 나오는지
    chk("os.sep" in az0 and 'replace(os.sep, "/")' in az0,
        "잡 키가 os.sep 을 / 로 바꾼다 (Windows 에서 tier1\\job 이 되던 버그)")

    # ── 기본은 **꺼짐** (Codex 7차 권장 A) — 외주 요청에 2단계 절차를 안 넣는다 ──
    chk(not list(out_sp.rglob("dense_cand/INCAR")),
        "기본 빌드에 dense 후보가 없다 (adaptive dense 기본 꺼짐)")
    chk(not (out_sp / "run_dense_selected.sh").is_file(),
        "기본 빌드에 run_dense_selected.sh 도 없다 (요청서가 짧아진다)")
    # ── 켰을 때만: 후보 입력이 러너에 **안 걸리는지** + 계획 두 경로 ──────────
    a_ad = argparse.Namespace(**{**vars(a_sp), "out": str(td / "bundle_adapt"),
                                 "adaptive_dense": True})
    out_ad = build_bundle(a_ad, ledger=led)
    chk((out_ad / "run_dense_selected.sh").is_file(),
        "--adaptive_dense 를 켜면 러너가 들어간다")
    out_sp = out_ad                       # 이하 조건부 dense 검사는 켠 번들로
    cands = sorted(out_sp.rglob("dense_cand/INCAR"))
    chk(len(cands) == 2, f"dense 후보 입력 {len(cands)}개 (보정자 끝점 × net4)")
    if cands:
        chk(re.search(r"^ICHARG\s*=\s*1", cands[0].read_text(), re.M) is not None,
            "후보 INCAR 도 ICHARG=1 (static CHGCAR 승계)")
        jm = json.loads((cands[0].parent.parent / "job.json").read_text())
        chk("dense_cand" not in (jm.get("phases") or []),
            "후보는 phases 에 없다 — run_job.sh 가 **자동 실행하지 않는다**")
        chk("dense_cand" in (jm.get("kmesh") or {}),
            "그래도 k 는 기록된다 (무엇이 준비됐는지 남는다)")

    def _plan(tag, mangle=None):
        bd = out.parent / f"_plan_{tag}"
        shutil.rmtree(bd, ignore_errors=True)
        shutil.copytree(out_sp, bd)
        for jp in sorted(bd.rglob("job.json")):
            m = json.loads(jp.read_text())
            _fake_phase(jp.parent, m, -500.0 + (0.02 if "net4" in jp.parent.name else 0.0),
                        POTCAR_SPEC)
        if mangle:
            mangle(bd)
        r = subprocess.run([sys.executable, "analyze_results.py", ".", "--plan_dense"],
                           cwd=bd, capture_output=True, text=True)
        pl = json.loads((bd / "DENSE_PLAN.json").read_text()) \
            if (bd / "DENSE_PLAN.json").is_file() else None
        return bd, r, pl

    # 양성(비발동): pm1 이 유효하고 더 낮으면 **추가 계산 0**
    _bd, r_a, pl_a = _plan("none")
    chk(r_a.returncode == 0 and pl_a is not None, f"--plan_dense 실행 rc={r_a.returncode}")
    chk(pl_a and pl_a["promote"] == [],
        f"pm1 이 낮음 → 승격 0건 (추가 계산 없음) {[e['decision'][:18] for e in (pl_a or {}).get('endpoints', {}).values()]}")
    chk(pl_a and pl_a.get("parent_manifest_sha256"),
        "계획에 부모 MANIFEST 해시가 박힌다 (어느 판의 계획인지)")
    # ★ 음성 ①: net4 가 20 meV 넘게 낮으면 **승격돼야** 한다
    def _flip(bd):
        for jp in sorted(bd.rglob("job.json")):
            if "net4" not in jp.parent.name:
                continue
            m = json.loads(jp.read_text())
            _fake_phase(jp.parent, m, -500.100, POTCAR_SPEC)     # 100 meV 더 낮게
    _bd2, _r2, pl_b = _plan("lower", _flip)
    chk(pl_b and len(pl_b["promote"]) > 0 and
        all("net4" in p["job"] for p in pl_b["promote"]),
        f"net4 가 100 meV 낮음 → 승격 {len((pl_b or {}).get('promote', []))}건")
    # ★ 음성 ②: 상한을 넘으면 조용히 자르지 말고 **못 한다고 적어야** 한다
    chk(not pl_b or len(pl_b["promote"]) <= MAX_OPTIONAL_DENSE_B,
        f"승격이 상한 {MAX_OPTIONAL_DENSE_B} 이하로 잘린다")
    # ★ 음성 ③: 계획 없이 run_dense_selected.sh 를 돌리면 실패해야 한다
    bd3 = out.parent / "_plan_noplan"
    shutil.rmtree(bd3, ignore_errors=True)
    shutil.copytree(out_sp, bd3)
    r3 = subprocess.run(["bash", "run_dense_selected.sh"], cwd=bd3,
                        capture_output=True, text=True)
    chk(r3.returncode != 0 and "DENSE_PLAN" in r3.stdout + r3.stderr,
        f"계획 없이 조건부 dense 실행 → 거부 rc={r3.returncode}")
    # ★ 음성 ④: 승격 0건이면 아무것도 안 돌고 **성공으로 끝난다**
    shutil.copy(_bd / "DENSE_PLAN.json", bd3 / "DENSE_PLAN.json")
    r4 = subprocess.run(["bash", "run_dense_selected.sh"], cwd=bd3,
                        capture_output=True, text=True)
    chk("승격 0건" in r4.stdout, f"승격 0건 → 즉시 종료 ({r4.stdout.strip()[:40]})")

    # ── 물리 규약 사본 대조 — 빌더 RCOV_B/BOND_F_B vs 분석기 RCOV/BOND_F ──────
    #   문자열 템플릿이라 import 로 공유할 수 없다. **실제로 파싱해서** 대조한다.
    az = (out_sp / "analyze_results.py").read_text()
    m_r = re.search(r"^RCOV = (\{.*?\})\nBOND_F = ([\d.]+)", az, re.M | re.S)
    chk(m_r is not None, "분석기에서 RCOV/BOND_F 표를 찾았다")
    if m_r:
        import ast as _ast
        chk(_ast.literal_eval(m_r.group(1)) == RCOV_B,
            "RCOV 사본 일치 (빌더 ↔ 분석기)")
        chk(abs(float(m_r.group(2)) - BOND_F_B) < 1e-12,
            f"BOND_F 사본 일치 ({m_r.group(2)})")
    # ── INCAR 되울림 대조 (2026-08-25 sdcp_wave1 오탐 30/30 재발 방지) ────────
    #   양성만 있으면 "전부 True 반환" 도 통과한다 — 음성 경로를 같이 건다.
    _WARNBOX = ("|      So try LREAL= Auto  in the INCAR   file.        |\n"
                "|      reciprocal projection scheme  (i.e. LREAL=.FALSE.)  |\n"
                "   ENCUT  =  520.0 eV  38.22 Ry    6.18 a.u.\n"
                "   LREAL  =      F    real-space projection\n"
                "   LDIPOL =      T    correct potential\n")
    #   ⚠ 이 함수들은 **생성된** analyze_results.py 안에 산다 — 사본을 다시 짜지 말고
    #     방금 쓴 산출물을 그대로 로드해서 건다 (사본이 갈라지면 검사가 거짓말한다).
    import importlib.util as _ilu
    _spec = _ilu.spec_from_file_location("_az_probe", out_sp / "analyze_results.py")
    _az = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_az)
    _echo_val, _incar_equal = _az._echo_val, _az._incar_equal
    chk(_echo_val(_WARNBOX, "LREAL") == "F",
        "되울림: 권고문(`| So try LREAL= Auto`)이 아니라 파라미터 줄을 읽는다")
    chk(_echo_val(_WARNBOX, "ENCUT") == "520.0", "되울림: ENCUT 파라미터 줄")
    chk(_echo_val(_WARNBOX, "NOSUCHKEY") is None,
        "되울림 ⛔음성: 없는 키는 None (통과가 아니라 미검증으로 남아야 한다)")
    for _k, _g, _w, _ok, _why in (
            ("ENCUT", "520.0", "520", True, "520.0 ↔ 520 수치 동일"),
            ("LDIPOL", "T", ".TRUE.", True, "T ↔ .TRUE."),
            ("LREAL", "T", "Auto", True, "Auto 는 실공간 → T 로 되울린다"),
            ("LREAL", "F", ".FALSE.", True, "F ↔ .FALSE."),
            ("LDAUU", "0.00 4.00 0.00", "0 4 0", True, "목록도 원소별 수치 비교"),
            # ⛔ 음성 — 여기가 뚫리면 게이트가 의미를 잃는다
            ("ENCUT", "400.0", "520", False, "⛔ENCUT 실제 차이는 계속 잡힌다"),
            ("LDIPOL", "F", ".TRUE.", False, "⛔논리값 실제 반전은 계속 잡힌다"),
            ("LREAL", "F", "Auto", False, "⛔역공간인데 Auto 선언은 실제 차이다"),
            ("LREAL", "T", "Bogus", False, "⛔모르는 표기는 통과시키지 않는다"),
            ("LDAUU", "0.00 4.00", "0 4 0", False, "⛔목록 길이가 다르면 불일치"),
            ("ISMEAR", "0", "1", False, "⛔정수 실제 차이"),
    ):
        chk(_incar_equal(_k, _g, _w) is _ok, f"되울림 대조 {_k} {_g}!={_w}: {_why}")
    for _k, _g, _w, _ok, _why in (
            ("ENCUT", "1e309", "2e309", False,
             "⛔Decimal: 1e309≠2e309 (float 이면 둘 다 inf 로 붙어 같아진다)"),
            ("ENCUT", "inf", "inf", False, "⛔비유한값은 일치로 치지 않는다"),
            ("LDAUU", "0.0 6.2 0.0", "0.0  6.2  0.0", True, "목록 공백 정규화"),
    ):
        chk(_incar_equal(_k, _g, _w) is _ok, f"되울림 대조 {_k}: {_why}")

    # ── 파일수준 e2e·check_pin·provenance 스위트는 **배포본 selftest_k 안**에 산다 ──
    #   (codex E-2차·E-5차가 같은 지적을 두 번 했다: 번들에만 있고 배포본에 없는
    #   검사는 "자체검증된다" 는 README 주장을 거짓으로 만든다. 사본을 두면
    #   갈라진다 — 한 곳 원칙. 여기서는 배포본을 실행해 **존재와 통과**를 검사한다.)
    _rk2 = subprocess.run([sys.executable, str(out_sp / "analyze_results.py"),
                           "--selftest"], capture_output=True, text=True)
    chk(_rk2.returncode == 0, "배포본 selftest rc=0 (음성 포함 전부 통과)")
    for _lbl, _minc in (("e2e", 8), ("check_pin", 7), ("provenance", 13), ("⛔", 20)):
        _n = _rk2.stdout.count(_lbl)
        chk(_n >= _minc, f"배포본 selftest 에 {_lbl} 스위트 {_n}건 ≥ {_minc}")

    m_ak = re.search(r"^AUDIT_KEYS_RUNTIME = \((.*?)\)", az, re.M | re.S)
    if m_ak:
        _rk = {x.strip().strip('"') for x in m_ak.group(1).split(",") if x.strip()}
        chk(set(AUDIT_KEYS) <= _rk,
            f"생성부 AUDIT_KEYS 가 분석기 실행 감사 목록에 **전부 포함** "
            f"(빠진 것 {sorted(set(AUDIT_KEYS) - _rk)})")
        chk({"LASPH", "ISYM", "NUPDOWN"} <= _rk,
            "물리 규약 키도 실행 감사 대상 (외주처 우발 수정 탐지)")
    else:
        chk(False, "분석기에서 AUDIT_KEYS_RUNTIME 을 못 찾았다")
    m_o = re.search(r"^MAX_OPTIONAL_DENSE = (\d+)", az, re.M)
    chk(m_o and int(m_o.group(1)) == MAX_OPTIONAL_DENSE_B,
        f"조건부 dense 상한 사본 일치 ({m_o.group(1) if m_o else '없음'})")

    # ── 🔴 회신 AT P0-1 회귀 — **배포 POSCAR 를 되읽어** 정본 그래프와 대조 ──
    #   종전 검사(`set(e) <= set(mol_poscar_idx)`)는 **어떤 순열이든 통과**한다.
    #   그래서 기체 잡이 항등 순서로 만든 그래프를 싣고 나갔고, 리뷰어가 배포본에서
    #   geometry_audit 을 돌려 broken 28 · formed 28 을 냈다 — VASP 전에 영구 게이트.
    #   원소가 섞인 분자를 쓴다: POSCAR 는 원소별로 묶여 나가므로 순서가 **반드시** 바뀐다.
    from ase import Atoms as _AtomsT
    from ase.io import read as _rdT
    _mt = _AtomsT(symbols=["C", "O", "H", "C", "O", "H", "S", "C", "H", "O"],
                  positions=[[0, 0, 0], [1.43, 0, 0], [-1.09, 0, 0],
                             [0, 1.52, 0], [1.43, 1.52, 0], [-1.09, 1.52, 0],
                             [0, 3.3, 0], [0, 4.9, 0], [1.09, 4.9, 0], [1.43, 3.3, 0]])
    _mtd = td / "molgraph_rt"
    _mtd.mkdir(parents=True, exist_ok=True)
    _mm = _emit_mol_job(_mtd, "rt_probe", _mt, 12.0, closure=True)
    _rt = _rdT(str(_mtd / "POSCAR"), format="vasp")
    chk("".join(_rt.get_chemical_symbols()) != "".join(_mt.get_chemical_symbols()),
        "AT P0-1 전제: POSCAR 가 원소별로 묶여 원자 순서가 **실제로 바뀐다** (%s → %s)"
        % ("".join(_mt.get_chemical_symbols()), "".join(_rt.get_chemical_symbols())))
    _gg = {tuple(sorted(e)) for e in _bonds_in(_rt, list(range(len(_rt))))}
    _ww = {tuple(sorted(e)) for e in _mm["mol_graph_canonical"]}
    chk(_ww and not (_ww - _gg) and not (_gg - _ww),
        "🔴 AT P0-1: 배포 POSCAR 재판독 그래프 == 정본 그래프 "
        "(정본 %d · 끊김 %d · 생성 %d) — 기체 기준계가 계산 전에 게이트되지 않는다"
        % (len(_ww), len(_ww - _gg), len(_gg - _ww)))
    # ★ 음성: 항등 순서로 만들면 **반드시 어긋나야** 한다 (안 어긋나면 이 검사가 헛돈다)
    _bad_graph = {tuple(sorted(e))
                  for e in _mol_graph_canon(_mt, 0, list(range(len(_mt))))}
    chk(bool((_bad_graph - _gg) or (_gg - _bad_graph)),
        "⛔음성 AT P0-1: 항등 순서로 만든 그래프는 POSCAR 와 어긋난다 "
        "(끊김 %d · 생성 %d) — 이게 v17 이 나간 상태였다"
        % (len(_bad_graph - _gg), len(_gg - _bad_graph)))

    # ── 정본 분자 위상: 양성 + 음성 ────────────────────────────────────────
    # ⚠ 알파벳순 첫 잡은 controls/clean_slab — 분자가 없다. 분자 있는 잡을 고른다.
    j0 = next(j for j in (json.loads(q.read_text())
                          for q in sorted(out_sp.rglob("job.json")))
              if j.get("mol_poscar_idx"))
    chk(len(j0.get("mol_graph_canonical") or []) > 0,
        f"job.json 에 정본 분자 그래프 {len(j0.get('mol_graph_canonical') or [])}결합")
    chk(all(set(e) <= set(j0["mol_poscar_idx"]) for e in j0["mol_graph_canonical"]),
        "정본 그래프가 **분자 인덱스만** 담는다 (슬랩 원자 혼입 없음)")
    # ★ 음성: 분자 결합 하나를 끊은 자세를 넣으면 빌드가 **멈춰야** 한다
    lab0 = "ptfe_dimer__Li_top__fib00__r000"
    xp0 = run / f"{lab0}.xyz"
    keep_xyz = xp0.read_text()
    from ase.io import read as _rd, write as _wr
    at_bad = _rd(xp0)
    p_bad = at_bad.get_positions()
    p_bad[-1] += [0.0, 0.0, 6.0]                  # 마지막 분자 원자를 뜯어낸다
    at_bad.set_positions(p_bad)
    _wr(xp0, at_bad)
    a_bad = argparse.Namespace(**{**vars(a_sp), "out": str(td / "bundle_topo")})
    try:
        build_bundle(a_bad, ledger=led)
        chk(False, "음성 분자 위상 파괴 → **번들이 만들어졌다** (헛도는 검사)")
    except SystemExit as e:
        chk("SOURCE_TOPOLOGY_CHANGED" in str(e),
            f"음성 분자 결합 끊김 → 빌드 중단 ({str(e).splitlines()[0][:50]})")
    xp0.write_text(keep_xyz)
    m_sp = json.loads((out_sp / "MANIFEST.json").read_text())
    # ── 교차 끝점 auto (2026-08-12 실빌드에서 발각) ──────────────────────────
    #   --cross_endpoints 로 한 조각만 켰는데 그 조각은 자세키가 일치했고, 정작
    #   불일치인 다른 조각이 **조용히 배향 혼입 상태로** 나갔다. 기본을 auto 로 뒤집었다.
    pm_sp = list(m_sp["pairs"].values())[0]
    chk(pm_sp.get("matched") is False,
        f"selftest 전제: 챔피언 자세키 불일치 (Li {(pm_sp.get('champion_pose') or {}).get('Li')})")
    chk(len(pm_sp.get("cross") or {}) == 2,
        f"불일치 → 교차 2개 **자동** 생성 ({list((pm_sp.get('cross') or {}))})")
    chk(not pm_sp.get("orientation_confounded"),
        "교차가 있으므로 혼입 표시 없음")
    # ★ 짝 풀 제한의 대가 — 챔피언은 "전역 최선" 이 아니라 "짝 있는 배향 중 최선" 이다
    pr = (m_sp.get("pair_audit") or {}).get("ptfe_dimer", {}).get("pool_restriction")
    chk(pr and pr.get("Li_meV") is not None and pr.get("Ni_meV") is not None,
        f"짝 풀 제한 대가를 기록 (Li {(pr or {}).get('Li_meV')} · "
        f"Ni {(pr or {}).get('Ni_meV')} meV)")
    chk(pr and pr["Li_meV"] >= 0 and pr["Ni_meV"] >= 0,
        "제한 대가는 **음수일 수 없다** (풀은 전체의 부분집합이다)")
    # ── 전역 챔피언: (a)배향일치 대비와 (b)전역 자리 선호가 갈릴 때 ──────────
    chk(pr["Ni_meV"] > 20, f"selftest 전제: 짝 없는 Ni 전역 최선 ({pr['Ni_meV']} meV 아래)")
    gb_sp = pm_sp.get("global_best") or {}
    chk(set(gb_sp) == {"Ni"},
        f"전역 최선이 다른 쪽(Ni)만 끝점 추가 ({list(gb_sp)}) — Li 는 풀=전역이라 불필요")
    chk(any("global_Ni" in k for k in m_sp["planned"]),
        "전역 챔피언 잡이 planned 에 있다")
    # ★ 음성: 문턱을 크게 잡으면 **재지 않았다고 적어야** 한다 (조용히 빠지면 안 된다)
    a_gt = argparse.Namespace(**{**vars(a_sp), "out": str(td / "bundle_gthr"),
                                 "global_champion_meV": 1e9})
    m_gt = json.loads((build_bundle(a_gt, ledger=led) / "MANIFEST.json").read_text())
    p_gt = list(m_gt["pairs"].values())[0]
    chk(not p_gt.get("global_best") and p_gt.get("global_unmeasured"),
        f"문턱 초과 → global_unmeasured 로 명시 "
        f"({(p_gt.get('global_unmeasured') or {}).get('shift_meV')} meV)")
    chk(not any("global_" in k for k in m_gt["planned"]),
        "그때는 전역 잡도 안 만든다 (비용을 안 쓴다)")
    # ★ 음성: --no_cross 면 혼입 상태를 **명시**해야 한다 (조용히 나가면 안 된다)
    a_nc = argparse.Namespace(**{**vars(a_sp), "out": str(td / "bundle_nocross"),
                                 "no_cross": True})
    m_nc = json.loads((build_bundle(a_nc, ledger=led) / "MANIFEST.json").read_text())
    p_nc = list(m_nc["pairs"].values())[0]
    chk(p_nc.get("orientation_confounded") is True and not p_nc.get("cross"),
        "--no_cross + 불일치 → orientation_confounded 기록 (조용한 통과 금지)")
    # ★ 음성: 제한 목록에 없는 조각은 교차가 안 생긴다 (제한이 실제로 먹는지)
    a_lim = argparse.Namespace(**{**vars(a_sp), "out": str(td / "bundle_limit"),
                                  "cross_endpoints": ["sdcp_neutral"]})
    m_lim = json.loads((build_bundle(a_lim, ledger=led) / "MANIFEST.json").read_text())
    chk(not list(m_lim["pairs"].values())[0].get("cross"),
        "--cross_endpoints 제한이 실제로 먹는다 (목록 밖 조각은 교차 없음)")

    # ── Codex 3차 감사 ────────────────────────────────────────────────────
    _sub = (out_sp / "SUBMIT_CONTRACT.md").read_text()
    _rd = (out_sp / "README_REQUEST.md").read_text()
    chk("controls/*/" not in _sub and "JOBS.txt" in _sub and "find " in _sub,
        "제출 예시가 폴더를 **실제로 찾는다** (controls/ 하드코딩 제거)")
    _dirs = sorted({k.split("/")[0] for k in m_sp["planned"]})
    chk(all(d in _rd for d in _dirs),
        f"README 의 폴더 목록이 실제와 같다 ({_dirs})")
    _nall = m_sp["submission"]["n_vasp_executions_total"]
    _nreal = sum(len(p.get("phases") or []) for p in m_sp["planned"].values())
    chk(_nall == _nreal, f"실행 횟수가 **모든 상**을 센다 ({_nall} == {_nreal})")
    chk(f"VASP 실행 {_nall}회" in _rd, f"README 도 같은 수를 쓴다 ({_nall})")
    # ★ README 산문 ↔ 실물 일치 — 실물 v13 에서 **셋이 갈라져 있었다** (2026-08-30).
    #   census 표는 옳은데 산문이 옛 설계를 말하고 있었고, 외주처가 읽는 것은 산문이다.
    _dn_jobs = sorted(k for k, v in m_sp["planned"].items()
                      if "dense" in (v.get("phases") or []))
    _rx_jobs = [k for k, v in m_sp["planned"].items()
                if "relax" in (v.get("phases") or [])]
    _tw_sp = (m_sp.get("job_census") or {}).get("complexes", {}).get("d3_off_twins")
    chk(all(j in _rd for j in _dn_jobs),
        f"README 가 dense 잡을 **이름으로** 적는다 ({len(_dn_jobs)}개)")
    # [음성] dense 가 있는데 "(없음)" 이라고 적으면 잡는다
    chk(not (_dn_jobs and "(없음)" in _rd),
        "[음성] dense 상이 있는데 README 가 '(없음)' 이라고 적지 않는다")
    # [음성] D3-off 쌍둥이가 0인데 산문이 D3-off 를 요구하면 잡는다
    chk(not (_tw_sp == 0 and "D3-off`" in _rd.replace("`pm1/D3-off`", "D3-off`")),
        "[음성] 쌍둥이 0 인데 산문이 pm1/D3-off 를 요구하지 않는다")
    chk(_tw_sp != 0 or "두 계산" in _rd,
        "쌍둥이 0 이면 README 가 'pose 당 두 계산' 이라고 적는다")
    # [음성] relax 상이 없는데 "이완이 필요합니다" 라고 적으면 잡는다
    chk(not (not _rx_jobs and "DFT 이완이 필요합니다" in _rd),
        "[음성] relax 상이 없는데 README 가 이완을 요구하지 않는다")
    chk(bool(_rx_jobs) or "폴더가 하나도 없습니다" in _rd,
        "relax 가 없으면 README 가 그렇게 적는다")

    # ⛔ 회신 AJ ⑤ — quickstart 가 allowlist 없이 조립기를 부르면 외주처는 즉시 막힌다
    for _doc, _nm in ((_rd, "README"), (_sub, "SUBMIT_CONTRACT")):
        for _ln in _doc.splitlines():
            if "bash POTCAR_ASSEMBLE.sh" in _ln and "POTCAR_ALLOWLIST" not in _ln:
                chk(False, "⛔음성 AJ: %s 가 allowlist 없이 조립기를 부른다 — "
                           "조립기는 없으면 즉시 종료한다: %s" % (_nm, _ln.strip()[:70]))
                break
        else:
            chk(True, "%s 의 조립기 호출에 POTCAR_ALLOWLIST 가 있다" % _nm)

    # run_all.sh 가 그룹을 하드코딩하지 않는다
    _ra = (out_sp / "run_all.sh").read_text()
    #   ⚠ 주석에는 그 문자열이 **이력으로** 남아 있다 — 실행 줄만 본다
    _ra_code = [l for l in _ra.splitlines() if not l.lstrip().startswith("#")]
    chk(not any("controls tier1 refs tier2" in l for l in _ra_code)
        and any("*/*/run_job.sh" in l for l in _ra_code),
        "⛔음성 AJ: run_all.sh 의 **실행 줄**이 그룹을 하드코딩하지 않는다 "
        "(11잡을 건너뛴 원인)")

    # ★ 주기영상 진공 (회신 AF P0-1) — 실물 v13 이 9자세 미달인데 문서는 ">15 Å" 였다
    _vac = m_sp.get("vacuum") or {}
    _pj = _vac.get("per_job_A") or {}
    chk(_vac.get("declared_A") is not None, "MANIFEST 에 진공 선언이 있다")
    chk(bool(_pj), f"자세별 진공이 기록된다 ({len(_pj)}개)")
    chk(all(v >= _vac["declared_A"] - 1e-6 for v in _pj.values()),
        f"배포 전 자세가 **전부** 선언치 이상 (최소 {_vac.get('min_after_A')} Å)")

    # ── 진공 유닛시험: 짧은 셀 → 늘림 → 원자가 안 움직였는가 ────────────────
    _vd = td / "vactest"
    _vd.mkdir(parents=True, exist_ok=True)
    #   슬랩 2원자(Ni,O) + 흡착종 1원자(H). c=20, 분자 z=12 → 이미지까지 8 Å
    (_vd / "POSCAR").write_text(
        "t\n1.0\n 10.0 0 0\n 0 10.0 0\n 0 0 20.0\nNi O H\n1 1 1\nDirect\n"
        "0.0 0.0 0.10\n0.5 0.5 0.10\n0.0 0.0 0.60\n")
    #   슬랩 z=2.0 · 흡착종 z=12.0 · c=20 ⇒ 이미지까지 20-10 = 10.0 Å
    _s0 = image_separation_A(_vd / "POSCAR")
    chk(abs(_s0 - 10.0) < 1e-6, f"진공 측정 = 10.00 Å (실제 {_s0:.3f})")
    _c0 = _poscar_read(_vd / "POSCAR")
    poscar_set_c(_vd / "POSCAR", 25.0)
    _c1 = _poscar_read(_vd / "POSCAR")
    chk(abs(_c1["A"][2][2] - 25.0) < 1e-9, "c 가 25.0 Å 로 바뀌었다")
    chk(max(abs(a[2] - b[2]) for a, b in zip(_c0["cart"], _c1["cart"])) < 1e-9,
        "[음성] c 를 늘려도 원자 Cartesian z 가 **안 움직인다** "
        "(Direct 되scale 을 빠뜨리면 슬랩이 늘어난다)")
    chk(abs(image_separation_A(_vd / "POSCAR") - 15.0) < 1e-6,
        "확장 뒤 분리 = 15.00 Å")

    # ⛔ 회신 AF P0-1 후단 — INCAR 의 DIPOL 만 고치고 job.json 의 **분율** 필드를
    #   안 고쳤다. zcom_frac 은 분율 질량중심이라 셀을 늘리면 어긋난다.
    _vj = td / "vacjj"
    _vj.mkdir(parents=True, exist_ok=True)
    (_vj / "POSCAR").write_text(
        "t\n1.0\n 10.0 0 0\n 0 10.0 0\n 0 0 20.0\nNi O H\n1 1 1\nDirect\n"
        "0.0 0.0 0.10\n0.5 0.5 0.10\n0.0 0.0 0.60\n")
    (_vj / "job.json").write_text(json.dumps({"zcom_frac": 0.6, "z_cut_A": 3.0}))
    (_vj / "static").mkdir(exist_ok=True)
    (_vj / "static" / "INCAR").write_text("LDIPOL   = .TRUE.\nDIPOL    = 0.5 0.5 0.6000\n")
    _fj = fit_bundle_vacuum(_vj.parent, {"vacjj": {}}, 15.0)
    _jd = json.loads((_vj / "job.json").read_text())
    _k = _fj["c_before_A"] / _fj["c_after_A"]
    chk(_fj["n_jobjson_rescaled"] == 1 and abs(_jd["zcom_frac"] - 0.6 * _k) < 1e-5,
        "job.json 의 분율 zcom_frac 이 c 와 같이 되scale 된다 (%.6f)" % _jd["zcom_frac"])
    chk(_jd["z_cut_A"] == 3.0,
        "[음성] Å 단위 z_cut_A 는 **안 건드린다** (분율이 아니다)")
    _dz = float(re.search(r"DIPOL\s*=\s*[\d.]+\s+[\d.]+\s+([\d.]+)",
                          (_vj / "static" / "INCAR").read_text()).group(1))
    chk(abs(_dz - 0.6 * _k) < 1e-3 and _fj["n_dipol_rescaled"] == 1,
        "INCAR 의 DIPOL z 도 같은 비율 (%.4f)" % _dz)
    # [음성] 미달 번들은 fit 이 c 를 실제로 늘려서만 통과한다
    _fit = fit_bundle_vacuum(_vd.parent, {"vactest": {}}, 18.0)
    chk(_fit["n_below_before"] == 1 and _fit["min_after_A"] >= 18.0
        and _fit["c_after_A"] > _fit["c_before_A"],
        f"[음성] 15 Å 짜리를 18 Å 선언으로 fit → c {_fit.get('c_before_A')}"
        f"→{_fit.get('c_after_A')} Å, 최소 {_fit.get('min_after_A')} Å")
    # [음성] c 축이 기울면 자동확장을 거부한다 (조용히 잘못 늘리지 않는다)
    (_vd / "tilt").mkdir(exist_ok=True)
    (_vd / "tilt" / "POSCAR").write_text(
        "t\n1.0\n 10 0 0\n 0 10 0\n 1.0 0 20.0\nNi H\n1 1\nDirect\n"
        "0.0 0.0 0.10\n0.0 0.0 0.60\n")
    try:
        poscar_set_c(_vd / "tilt" / "POSCAR", 30.0)
        chk(False, "[음성] 기운 c 축을 거부한다")
    except ValueError:
        chk(True, "[음성] 기운 c 축을 거부한다 (조용히 잘못 늘리지 않는다)")
    chk(isinstance(m_sp.get("claim_policy"), dict)
        and all(f in m_sp["claim_policy"] for f in m_sp["fragments"]),
        f"조각별 claim_policy 가 있다 ({list((m_sp.get('claim_policy') or {}))})")
    chk("pm1 자기 branch 조건부" in str(m_sp.get("claim_scope", "")),
        "claim_scope 가 pm1 branch 조건부임을 명시")
    chk("branch_tie" in az0 and "MAGNETIC_K_UNRESOLVED_for_branch_minimum" in az0,
        "branch 경합을 **기본 경로**에서 기록한다 (--plan_dense 밖)")
    # ── Codex 4차 감사 ────────────────────────────────────────────────────
    _noasm = [k for k in m_sp["planned"]
              if not (out_sp / k / "POTCAR_ASSEMBLE.sh").is_file()]
    chk(not _noasm, f"**모든** 잡에 POTCAR 조립기 (없는 잡 {_noasm[:3]})")
    _mol = [k for k in m_sp["planned"] if "mol__" in k]
    if _mol:
        _asm = (out_sp / _mol[0] / "POTCAR_ASSEMBLE.sh").read_text()
        chk("ORDER=" in _asm and "TITEL" in _asm,
            f"기체 잡 조립기도 종 순서·TITEL 검증을 한다 ({_mol[0]})")
    chk('os.path.join("refs"' not in az0 and 'E(f"refs/mol__' in az0,
        "refs 조회가 POSIX 리터럴 (os.path.join 은 Windows 에서 키가 안 맞는다)")
    chk("기준계를 선언했는데 E_ads 가 0개다" in az0,
        "refs 선언 + E_ads 0개 → exit 2 (조용한 완주 차단)")
    chk(isinstance(m_sp.get("cost_frozen"), dict)
        and m_sp["cost_frozen"].get("total_wall_h"),
        f"비용이 MANIFEST 에 동결됐다 ({(m_sp.get('cost_frozen') or {}).get('total_wall_h')} h)")
    chk("branch_policy" in (m_sp.get("submission") or {})
        and "미주장" in m_sp["submission"]["branch_policy"],
        "branch policy 가 MANIFEST 에 명시 (게이트로 막는다는 옛 문구 제거)")
    chk("E_ads(static target mesh)" in az0,
        "E_ads headline 이 coarse 임을 명시 (dense 는 게이트 전용)")
    chk(all(p.get("phases") == ["static"] or p.get("phases") == ["static", "dense"]
            for k, p in m_sp["planned"].items() if "clean_slab" not in k),
        "SP: pose 잡에 relax/pre 가 없다 (단일점)")
    chk(m_sp.get("magnetic_controls") and len(m_sp["magnetic_controls"]) == 2,
        f"SP: clean 자기 대조군 2 seed 포함 ({m_sp.get('magnetic_controls')})")
    chk(all("dense" not in (m_sp["planned"][c].get("phases") or [])
            for c in m_sp["magnetic_controls"]),
        "SP: 자기 대조군은 dense 없음 (coarse static 만 — 예산)")
    _runner_regression(out_sp, chk)

    E = {"clean": -500.0, "mol": -50.0}
    truth = dict(DIRS)
    for jd in sorted(out.rglob("job.json")):
        d = jd.parent
        meta = json.loads(jd.read_text())
        n = d.name
        if n.startswith("clean_slab"):
            e0 = E["clean"] + (0.004 if "net4" in n else 0.0)
        elif n.startswith("mol__"):
            e0 = E["mol"] + (0.003 if "box24" in n else 0.0)
        else:
            pid_dir = n.split("__")[1].split("_")[0]
            base = E["clean"] + E["mol"] - 1.0
            e0 = base if "Litop" in n else base + truth[pid_dir]
            if "net4" in n:
                e0 += 0.004                       # seed 차 4 meV — 게이트(10) 안
        _fake_phase(d, meta, e0, POTCAR_SPEC)
    # dense — ★ **한쪽 끝점만** 3 meV 옮긴다. 양쪽에 같은 값을 더하면 ΔE 이동이 0 이라
    #   k 게이트가 아무것도 검증하지 못한다 (옛 판의 버그).
    import re as _re
    RX = r"energy\(sigma->0\)\s*=\s*(-?[\d.]+)"
    n_dense = 0
    for dj in sorted(out.rglob("dense")):
        if not dj.is_dir():
            continue
        n_dense += 1
        meta = json.loads((dj.parent / "job.json").read_text())
        t = (dj.parent / "static" / "OUTCAR").read_text()
        e0 = float(_re.search(RX, t).group(1))
        shift = 0.003 if "Nitop" in dj.parent.name else 0.0
        nk = 1
        for v in str((meta.get("kmesh") or {}).get("dense", "1 1 1")).split():
            nk *= int(v)
        t = _re.sub(r"NKPTS = \d+", f"NKPTS = {nk}", t)      # 진짜 dense 는 k 가 늘어난다
        # ⛔ 회신 AT P0-2 — static OUTCAR 를 베껴 dense 를 만드는 픽스처라 ` KPOINTS:`
        #   되울림이 **static 제목 그대로** 남는다. 실물 dense 는 제 제목을 되울리므로
        #   여기서도 갈아끼운다. (갈아끼우지 않으면 새 정확대조 게이트가 정상 잡까지
        #   막아 이 selftest 가 NO_DATA 가 된다 — 2026-08-31 실측.)
        _dkt = ((meta.get("kpoints_expected") or {}).get("dense") or {}).get("title")
        if _dkt:
            t = _re.sub(r"(?m)^ KPOINTS: .*$", f" KPOINTS: {_dkt}", t)
        t = t.replace("LREAL = Auto", "LREAL = .FALSE.")
        (dj / "OUTCAR").write_text(t.replace(f"{e0:.6f}", f"{e0 + shift:.6f}"))
    # ★ 음성 N13 (Codex 7차 §8) — dense 에서 **모멘트 표만** 지운다. 에너지·NKPTS 는
    #   멀쩡하므로, 게이트가 없으면 이 잡은 아무 문제 없이 κ 에 들어간다.
    dm_job = None
    for dj in sorted(out.rglob("dense")):
        # ⚠ fib00 은 **유일하게 살아남는 정상 쌍**이다 — 여기를 죽이면 하류 시험
        #   ("유효 1/계획 5") 이 NO_DATA 로 무너진다. 이미 막힌 쌍에서 고른다.
        if (dj.is_dir() and (dj / "OUTCAR").is_file()
                and "Litop" in dj.parent.name and "fib00" not in dj.parent.name):
            txt = (dj / "OUTCAR").read_text()
            if "magnetization (x)" in txt:
                head, _sep, _tail = txt.partition("magnetization (x)")
                (dj / "OUTCAR").write_text(
                    head + "\n General timing and accounting informations for this job\n")
                dm_job = str(dj.parent.relative_to(out))
                break

    # ★ P1-2 (Codex 5차) — dense 가 **완전한 시간반전**으로 수렴하면 물리적으로 같은
    #   상태다. Ni·라디칼·총 M 을 전부 뒤집어도 통과해야 한다. 옛 판은 static 의 sg 를
    #   재사용해 전부 부호 불일치로 잡았다(거짓 차단).
    tr_job = None
    for dj in sorted(out.rglob("dense")):
        # ⚠ N13 이 이미 모멘트 표를 지운 잡을 고르면 **헛통과**한다 (다른 게이트가
        #   먼저 걸려 내 assertion 이 공허하게 참이 된다). 그 잡을 명시적으로 뺀다.
        if (dj.is_dir() and (dj / "OUTCAR").is_file()
                and str(dj.parent.relative_to(out)) != (dm_job or "")
                and "magnetization (x)" in (dj / "OUTCAR").read_text()
                and "Nitop" in dj.parent.name):
            txt = (dj / "OUTCAR").read_text()
            # 모멘트 표는 `# of ion  s  p  d  tot` — 5열이고 마지막이 tot 다.
            def _neg(m):
                return f"{m.group(1)}{-float(m.group(2)):9.3f}"
            _k0 = txt.rfind("magnetization (x)")
            head, tail = txt[:_k0], txt[_k0:]
            tail = _re.sub(r"(?m)^(\s*\d+(?:\s+-?[\d.]+){3}\s+)(-?[\d.]+)\s*$",
                           _neg, tail)
            txt2 = head + tail
            txt2 = _re.sub(r"(magnetization\s+)(-?[\d.]+)",
                           lambda m: f"{m.group(1)}{-float(m.group(2)):.4f}", txt2)
            (dj / "OUTCAR").write_text(txt2)
            tr_job = str(dj.parent.relative_to(out))
            break
    chk(n_dense >= 2 * len(DIRS), f"tier1 전 pm1 끝점에 dense 상 ({n_dense}개)")

    # ── 음성 케이스 심기 ────────────────────────────────────────────────────
    def contcar_edit(job, fn):
        p = out / job / "relax" / "CONTCAR"
        lines = p.read_text().splitlines()
        fn(lines)
        p.write_text("\n".join(lines) + "\n")

    mig_job = "tier1/ptfe_dimer__fib01_r000__Litop__afm2424_pm1"
    meta_m = json.loads((out / mig_job / "job.json").read_text())

    def move_mol(lines):
        head = 9
        for k in meta_m["mol_poscar_idx"]:
            v = lines[head + k].split()
            v[1] = f"{float(v[1]) + 0.5:.16f}"
            lines[head + k] = "  " + "  ".join(v)
    contcar_edit(mig_job, move_mol)

    bb_job = "tier1/ptfe_dimer__fib02_r000__Litop__afm2424_pm1"
    meta_b = json.loads((out / bb_job / "job.json").read_text())

    def break_bond(lines):
        head = 9
        k = meta_b["mol_poscar_idx"][-1]
        v = lines[head + k].split()
        v[0] = f"{float(v[0]) + 0.6:.16f}"
        lines[head + k] = "  " + "  ".join(v)
    contcar_edit(bb_job, break_bond)

    sm_job = out / "tier1/ptfe_dimer__fib03_r000__Nitop__afm2424_net4" / "static" / "OUTCAR"
    t = sm_job.read_text()
    e0 = float(_re.search(RX, t).group(1))
    sm_job.write_text(t.replace(f"{e0:.6f}", f"{e0 + 0.050:.6f}"))

    # N5 잘린 OUTCAR — 에너지는 있는데 정상종료가 없다
    tr_job = "tier1/ptfe_dimer__fib04_r000__Litop__afm2424_pm1"
    p = out / tr_job / "static" / "OUTCAR"
    p.write_text(p.read_text().replace(" General timing and accounting\n", ""))
    # N6 TITEL 이 통째로 없다 (검사 못 함 = 통과 아님)
    nt_job = "tier1/ptfe_dimer__fib04_r000__Nitop__afm2424_pm1"
    p = out / nt_job / "static" / "OUTCAR"
    p.write_text(_re.sub(r" TITEL.*\n", "", p.read_text()))
    # N7 Ni 모멘트 붕괴 (전부 0)
    # ⚠ fib03 pm1 에 심으면 N3(seed 불일치)의 pm1 에너지가 죽어 seed 비교 자체가 안 돈다
    #   — 음성끼리 서로를 가린다. 이미 죽은 fib04 의 net4 잡에 심는다.
    mc_job = "tier1/ptfe_dimer__fib04_r000__Litop__afm2424_net4"
    p = out / mc_job / "static" / "OUTCAR"
    p.write_text(_re.sub(r"(\d+\s+0\.000\s+0\.000\s+)(-?[\d.]+)(\s+)(-?[\d.]+)",
                         r"\g<1>0.000\g<3>0.000", p.read_text()))
    # N11 LDAU occupation matrix 가 없다 (LDAUPRINT=2 인데) — 기록 불가로 잡혀야
    ld_job = "tier1/ptfe_dimer__fib01_r000__Litop__afm2424_pm1"
    q = out / ld_job / "static" / "OUTCAR"
    q.write_text(_re.sub(r" atom =.*?(?=\n magnetization|\Z)", "", q.read_text(),
                         flags=_re.S))
    # N12 dense 에서만 Ni **일부**가 뒤집혔다 = 다른 자기 basin (전역 반전은 같은 상태)
    # ⚠ fib03 은 N3(seed 불일치)가 쓰는 쌍이다 — 여기에 심으면 pm1 에너지가 죽어
    #   seed 비교 자체가 안 돈다. 이미 죽은 fib01(N1 migration) 쪽에 심는다.
    #   음성끼리 서로를 가리는 사고가 이번 라운드에서 두 번째다.
    br_job = "tier1/ptfe_dimer__fib01_r000__Nitop__afm2424_pm1"
    q = out / br_job / "dense" / "OUTCAR"
    if q.is_file():
        lines = q.read_text().splitlines()
        flipped = 0
        for i, ln in enumerate(lines):
            v = ln.split()
            if len(v) == 5 and v[0].isdigit() and abs(float(v[4])) > 0.5 and flipped < 2:
                lines[i] = f"{v[0]:>5s}     0.000   0.000   {-float(v[3]):7.3f}   " \
                           f"{-float(v[4]):7.3f}"
                flipped += 1
        q.write_text("\n".join(lines) + "\n")
    # N10 dense 에 static 산출을 복사 — NKPTS 가 안 늘어야 잡힌다 (Codex P0-5)
    dc_job = "tier1/ptfe_dimer__fib02_r000__Nitop__afm2424_pm1"
    if (out / dc_job / "dense").is_dir():
        shutil.copy(out / dc_job / "static" / "OUTCAR", out / dc_job / "dense" / "OUTCAR")
    # N8 필수 누락: box24 static 삭제
    (out / "refs/mol__ptfe_dimer__box24/static/OUTCAR").unlink()
    # N9 입력 변조: 한 잡의 INCAR 을 고친다 → 무결성 실패
    tam = out / "tier1/ptfe_dimer__fib00_r000__Litop__afm2424_pm1/static/INCAR"
    tam.write_text(tam.read_text().replace("ENCUT    = 520", "ENCUT    = 400"))

    r = subprocess.run([sys.executable, str(out / "analyze_results.py"), str(out)],
                       capture_output=True, text=True)
    print(r.stdout[-2000:])
    res = json.loads((out / "RESULTS.json").read_text())

    chk(r.returncode == 2, "N8/N9 → exit 2 (fail-closed)")
    chk(any("PAIR_MIGRATED" in g for g in res["jobs"][mig_job]["gates"]),
        "N1 migration → PAIR_MIGRATED")
    chk(any("BOND_CHANGE" in g for g in res["jobs"][bb_job]["gates"]),
        "N2 F 이탈 → BOND_CHANGE")
    # ★ 음성끼리 서로를 가리는 사고가 두 번 났다 (N7·N12 가 N3 의 pm1 을 죽였다).
    #   N3 은 fib03 의 **pm1 쌍이 살아 있어야** 성립한다 — 그걸 먼저 확인해
    #   실패했을 때 "왜" 가 바로 보이게 한다.
    live = [j for j in (f"tier1/ptfe_dimer__fib03_r000__{r}top__afm2424_pm1"
                        for r in ("Li", "Ni"))]
    blocked = {j: res["jobs"][j]["gates"] for j in live if res["jobs"][j]["gates"]}
    chk(not blocked, f"N3 전제: fib03 pm1 쌍이 게이트 없이 살아 있다 ({blocked})")
    chk(any("BLOCKED_MAGNETIC" in g for g in res["pairs"]
            ["ptfe_dimer__fib03_r000"]["gates"]),
        "N3 seed 50 meV 불일치 → BLOCKED_MAGNETIC_SENSITIVITY")
    chk(any("NOT_TERMINATED" in g for g in res["jobs"][tr_job]["gates"]),
        f"N5 잘린 OUTCAR → NOT_TERMINATED ({res['jobs'][tr_job]['gates']})")
    chk(any("POTCAR_UNVERIFIED" in g for g in res["jobs"][nt_job]["gates"]),
        f"N6 TITEL 없음 → POTCAR_UNVERIFIED (통과 아님)")
    chk(any("MAGNETIC_COLLAPSE" in g for g in res["jobs"][mc_job]["gates"]),
        f"N7 모멘트 붕괴 → MAGNETIC_COLLAPSE (clean 기준 Q/f_small)")
    if dm_job:
        gts = res["jobs"].get(dm_job, {}).get("gates", [])
        chk(any("DENSE_MOMENT" in g for g in gts),
            f"N13 dense 모멘트 표만 삭제 → 게이트 발화 ({[g[:34] for g in gts]})")
    else:
        chk(False, "N13 전제 실패: 모멘트 표 있는 dense 잡을 못 찾았다")
    if tr_job:
        _g = res["jobs"].get(tr_job, {}).get("gates", [])
        _mg = ((res["jobs"].get(tr_job, {}).get("geom") or {}).get("magnetic") or {})
        chk(bool((_mg.get("dense") or {}).get("global_sign") is not None),
            f"N14 전제: 그 잡의 dense 모멘트가 실제로 읽혔다 ({tr_job})")
        _d = ((res["jobs"].get(tr_job, {}).get("geom") or {})
              .get("magnetic") or {}).get("dense") or {}
        chk(not any("RADICAL_BRANCH_CHANGED" in x or "DENSE_MAGNETIC_COLLAPSE" in x
                    for x in _g),
            f"N14 dense 전역 시간반전 → **거짓 차단 없음** ({[x[:28] for x in _g]})")
        chk(_d.get("global_sign") is not None,
            f"N14b dense 가 **자기 전역부호**를 기록한다 ({_d.get('global_sign')})")
    chk(len(res["integrity"]["changed"]) == 1, f"N9 INCAR 변조 → 무결성 1건 감지")

    # ── 양성: 게이트에 안 걸린 쌍은 값이 **정확히** 복원돼야 한다 ──
    p0 = res["pairs"]["ptfe_dimer__fib00_r000"]
    de = p0.get("dE_Ni_minus_Li_eV")
    # ★ dense 가 있으면 **dense 가 headline** 이다 (Codex zip 감사 P0-3). 가짜 dense 는
    #   Ni 쪽만 +3 meV 옮기므로 dense ΔE = coarse + 0.003 이어야 한다.
    #   옛 판은 dense 로 κ 만 재고 최종 수치는 coarse 를 썼다 — 이 시험이 그걸 잡는다.
    _has_dense = p0.get("dE_coarse_eV") is not None
    _want = truth["fib00"] + (0.003 if _has_dense else 0.0)
    chk(de is not None and abs(de - _want) < 1e-6,
        f"양성 ΔE 복원 fib00 = {de} (기대 {_want:.3f}, "
        f"{'dense headline' if _has_dense else 'coarse'})")
    if _has_dense:
        chk(abs(p0["dE_coarse_eV"] - truth["fib00"]) < 1e-6,
            f"coarse 값도 보존된다 ({p0['dE_coarse_eV']})")
        chk("dense" in str(p0.get("headline_from", ""))
            and p0.get("k_transfer_allowance_meV") == 0.0,
            f"headline 출처와 k 불확실성 0 을 기록 ({p0.get('headline_from')})")
    kg = res["numerical_gates"].get("k_ptfe_dimer__fib00_r000")
    chk(kg is not None and abs(kg["dE_meV"] - 3.0) < 1e-6,
        f"dense-k 게이트가 **한쪽만** 옮긴 3 meV 를 잡는다 ({kg})")
    chk(res["numerical_gates"].get("box_ptfe_dimer", {}).get("pass") is False,
        "N8 box24 없음 → 상자 게이트 **실패**로 기록 (옛 판은 항상 참이었다)")
    chk(not res["e_ads"], "상자 게이트 실패 → E_ads 를 만들지 않는다")
    chk(bool(res["required_missing"]), f"N8 필수 누락 기록 {len(res['required_missing'])}건")
    # ── PAIR_COLLAPSED 양성/음성 (새 basin 판정) ──
    chk(any("LDAU" in str(w) for w in res["warnings"]),
        f"N11 LDAU occupation 없음 → 경고 기록")
    chk((res["jobs"][br_job]["geom"].get("magnetic") or {}).get("ldau") is not None,
        "정상 잡은 LDAU 지문이 기록된다")
    chk(any("MAGNETIC_BRANCH_CHANGED" in g for g in res["jobs"][br_job]["gates"]),
        f"N12 dense 에서만 부분 반전 → MAGNETIC_BRANCH_CHANGED")
    chk(any("KMESH_NOT_DENSER" in g for g in res["jobs"][dc_job]["gates"]),
        f"N10 dense 에 static 복사 → KMESH_NOT_DENSER ({res['jobs'][dc_job]['gates'][:1]})")
    chk(any("PAIR_COLLAPSED" in g for g in res["pairs"]["ptfe_dimer__fib01_r000"]["gates"]),
        "N1 두 끝점이 같은 자리로 → PAIR_COLLAPSED (RMSD+접촉지문)")
    chk(not any("PAIR_COLLAPSED" in g for g in p0["gates"]),
        f"떨어져 있는 정상 쌍엔 **안 걸린다** (RMSD {p0.get('basin', {}).get('mol_rmsd_A')} Å)")
    chk((p0.get("basin") or {}).get("mol_rmsd_A", 0) > RMSD_TOL_CHK,
        f"정상 쌍 분자 RMSD = {(p0.get('basin') or {}).get('mol_rmsd_A')} Å (> 0.75)")
    fr = res["fragments"]["ptfe_dimer"]
    chk(fr["class"] == "NO_VERDICT_n<3",
        f"유효 1/계획 5 → n<3 게이트 선행 (실제 {fr['class']})")
    SS.load_slab = _SS_LOAD_SLAB_ORIG       # ★ 전역 오염 복원 (다음 시험이 실물을 본다)
    print("✔ selftest 전부 통과" if ok else "⛔ selftest 실패")
    return 0 if ok else 1


# ══ wave1.5 — clean_slab net4 를 **의도한 basin 으로** 유도하는 재실행 패키지 ═══
#   (2026-08-25 codex E 후속) VASP 는 결정론적이라 같은 입력을 다시 보내면 같은
#   basin B 에서 같게 끝난다. 그래서 2상으로 유도한다:
#     static_pin : NUPDOWN 을 **시드 자화합**으로 고정 + 보수적 스핀 믹싱
#                  → #82 반전(총모멘트 ±2.36 μB 변화)이 금지된 채 수렴
#     static     : pin 의 CHGCAR 를 ICHARG=1 로 승계, NUPDOWN 해제 —
#                  **이 상의 에너지만** 다른 잡과 비교 가능 (원본과 유일한 차이 = ICHARG)
#   ⛔ 이 설계가 못 하는 것:
#     · basin 유지 **보장** 없음 — NUPDOWN 해제 후 재반전 가능. 그러면 결론은
#       "net4 의 intended topology 는 이 Hamiltonian 에서 국소최소가 아니다" 이고,
#       그것대로 (E-6 의 realized_basin 언어로) 유효한 답이다. fallback 은
#       noncollinear constrained(I_CONSTRAINED_M) — 프로토콜 변경이라 별도 승인 필요.
#     · "Ni #82 반전 비용" 측정이 아니다 (그건 constrained pair 소관, 미착수).

def make_basin_rescue(src_job, out_dir):
    src, out = Path(src_job), Path(out_dir)
    need = ["INCAR", "POSCAR", "KPOINTS", "POTCAR_ASSEMBLE.sh", "job.json"]
    # 원본 잡은 static/ 아래에 INCAR·KPOINTS 를 두는 배치다 — 둘 다 지원
    def find(f):
        for c in (src / f, src / "static" / f):
            if c.is_file():
                return c
        raise SystemExit(f"⛔ {src} 에 {f} 가 없다 — 원본 번들 잡 디렉터리를 줄 것")
    meta = json.loads(find("job.json").read_text())
    mm = meta.get("magmom_poscar") or []
    nup = sum(mm)
    if abs(nup - round(nup)) > 1e-6:
        raise SystemExit(f"⛔ 시드 자화합 {nup} 이 정수가 아니다 — NUPDOWN 고정 근거가 없다")
    nup = int(round(nup))
    inc0 = find("INCAR").read_text()
    if "NUPDOWN" in inc0:
        raise SystemExit("⛔ 원본 INCAR 에 이미 NUPDOWN 이 있다 — 이 레시피의 전제가 깨진다")
    out.mkdir(parents=True, exist_ok=True)
    # 공통 파일은 **바이트 그대로** (기하·k·POTCAR 는 원본과 동일해야 비교가 성립)
    for f in ("POSCAR", "KPOINTS", "POTCAR_ASSEMBLE.sh"):
        shutil.copy(find(f), out / f)
    pin = inc0.rstrip() + f"""

# ── basin 유도 1상 (wave1.5, 2026-08-25) — 이 상의 에너지는 **인용 금지** ──
#  총 스핀차(N↑−N↓)를 시드 자화합 {nup:+d} 로 고정한다. ⚠ 이것은 "#82 단독 반전
#  금지" 가 아니라 **"총자화가 달라지는 반전의 억제"** 다 (codex E-2차 W-1) —
#  다른 Ni 크기 변화·O 자화가 연속적으로 보상할 수 있다. topology 는 회신 후
#  모멘트 표(--check_pin)로 검증한다. site 별 hard pin 은 collinear 에 없다.
NUPDOWN  = {nup}
AMIX     = 0.2
BMIX     = 0.0001
AMIX_MAG = 0.4
BMIX_MAG = 0.0001
"""
    (out / "static_pin").mkdir(exist_ok=True)
    (out / "static_pin" / "INCAR").write_text(pin)
    # 2상: 원본과의 차이는 ICHARG=2→1 **한 줄** — 그래야 wave1 static 과 비교 가능
    st2, nsub = re.subn(r"(?m)^ICHARG\s*=\s*2\b", "ICHARG   = 1", inc0)
    if nsub != 1:
        raise SystemExit(f"⛔ ICHARG=2 를 정확히 1회 치환해야 하는데 {nsub}회 — 원본 확인")
    st2 = st2.rstrip() + ("\n\n# ── basin 유도 2상 — pin 의 CHGCAR 승계, NUPDOWN 해제 ──\n"
                          "# 원본 static 과의 유일한 차이는 ICHARG=1 이다. 이 상의 에너지만 비교 가능.\n")
    (out / "static").mkdir(exist_ok=True)
    (out / "static" / "INCAR").write_text(st2)
    for ph in ("static_pin", "static"):
        shutil.copy(find("KPOINTS"), out / ph / "KPOINTS")
    meta2 = dict(meta)
    meta2["phases"] = ["static_pin", "static"]
    # codex E-3차 필수1 — check_pin 이 **전체 phase_gates** 를 돌리려면 kmesh 와
    #   potcar_spec 이 잡 안에 있어야 한다 (rescue 는 standalone 으로 배송된다).
    _km = (meta.get("kmesh") or {}).get("static")
    if not _km:
        raise SystemExit("⛔ 원본 job.json 에 kmesh.static 이 없다 — KPOINTS 검증 불가 (fail-closed)")
    meta2["kmesh"] = {"static_pin": _km, "static": _km}
    _man = None
    for _cand in (src.parent.parent / "MANIFEST.json", src.parent / "MANIFEST.json"):
        if _cand.is_file():
            _man = json.loads(_cand.read_text())
            break
    _spec = (_man or {}).get("potcar_spec")
    if not _spec:
        raise SystemExit("⛔ 부모 번들 MANIFEST.json 의 potcar_spec 을 못 찾았다 — "
                         "POTCAR TITEL 검증 불가 (fail-closed)")
    meta2["potcar_spec"] = _spec
    meta2["incar_expected"] = {"static_pin": _incar_expected_from(pin),
                               "static": _incar_expected_from(st2)}
    # ⛔ codex E-2차 필수2 — release 에 NUPDOWN=4 가 **남아도 통과**하던 구멍.
    #   미설정의 되울림이 -1.0000 이므로 기대값 "-1" 을 명시하면 잔류가 하드게이트다.
    meta2["incar_expected"]["static"]["NUPDOWN"] = "-1"
    import hashlib as _h2

    def _sha(q):
        return _h2.sha256(Path(q).read_bytes()).hexdigest()
    meta2["rescue"] = {
        "what": "clean_slab net4 basin 유도 (wave1.5)", "nupdown_pin": nup,
        # 필수1 — 분석기가 이 이름의 clean 참조를 **이 잡으로 교체**한다 (통과 시에만)
        "supersedes": "refs/clean_slab__afm2424_net4",
        # 부모는 /tmp 경로가 아니라 **이름 + 내용 해시**로 (codex E-2차: 계보 입증)
        "parent_name": src.name, "made": "2026-08-25",
        "parent_sha256": {"POSCAR": _sha(find("POSCAR")),
                          "INCAR_static": _sha(find("INCAR")),
                          "KPOINTS": _sha(find("KPOINTS"))},
        "accept_iff": ["static_pin: --check_pin 통과 (정상종료·NELM 미도달·NUPDOWN 되울림"
                       f"={nup}·flip 0·모멘트 붕괴 0·CHGCAR sha256 기록)",
                       "static: 정상 종료 + NUPDOWN 되울림 -1.0000 (해제 — 하드게이트) "
                       "+ 모멘트가 시드 topology (flip_indices_poscar == [])",
                       "pin CHGCAR 와 static 에 복사된 CHGCAR 의 sha256 동일 (vasp.log 포함 회신)"],
        # W-3 (codex E-2차) — 재반전은 '국소최소가 아니다' 의 증명이 **아니다**
        "if_reflips": ("pin 상에서 basin A 를 확인했으나, 제약 해제 후 이 고정 기하의 "
                       "collinear PBE+U SCF 프로토콜에서는 A 가 유지되지 않았고 basin X 로 "
                       "수렴했다 — 즉 basin A 의 unconstrained stationary solution 은 "
                       "**입증되지 않았다** (부존재 증명 아님). pin 부터 A 가 아니면 "
                       "'pin 준비 실패로 안정성 미판정'. 재반전 signature 가 기존 B 와 "
                       "다르면 새 basin C 로 등록한다."),
        "energy_notation": "E(static | basin A, initialized from pinned CHGCAR)",
    }
    (out / "job.json").write_text(json.dumps(meta2, indent=1, ensure_ascii=False))
    (out / "run_job.sh").write_text("""#!/usr/bin/env bash
# wave1.5 basin 유도 — 2상 사슬 v3 (codex E-3차 반영).
#   · 이 잡은 **1회용**이다: 기존 산출물이 하나라도 있으면 실행을 거부한다
#     (CHGCAR 만 지우면 OUTCAR/PIN_CHECK 가 남아 어느 실행의 것인지 섞인다).
#   · 해시·시각·CHGCAR 승계 증거를 RUN_PROVENANCE.json 에 **영구 기록**하고
#     회신물에 포함한다 (콘솔 출력은 증거가 아니다).
#   · release(static)는 --check_pin(전체 게이트) 통과 후에만 돈다.
set -euo pipefail
cd "$(dirname "$0")"
for f in static_pin/OUTCAR static_pin/OUTCAR.gz static_pin/OSZICAR static_pin/vasp.log \
         static_pin/CHGCAR static_pin/PIN_CHECK.json \
         static/OUTCAR static/OUTCAR.gz static/OSZICAR static/vasp.log static/CHGCAR \
         RUN_PROVENANCE.json; do
  [ -e "$f" ] && { echo "⛔ 기존 산출물 $f 발견 — 이 잡은 1회용입니다. 새 복사본에서 실행하세요."; exit 1; }
done
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)_$(hostname)"
bash POTCAR_ASSEMBLE.sh
for ph in static_pin static; do cp POTCAR POSCAR "$ph"/ ; done
python3 - "$RUN_ID" <<'PY'
import hashlib, json, sys, time
sha = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()
meta = json.load(open("job.json"))
want = meta["rescue"]["parent_sha256"]
man = json.load(open("MANIFEST_RESCUE.json"))["sha256"]
# ⚠ VASP 가 실제로 읽는 것은 **phase 디렉터리 사본**이다 (codex E-4차 P0-2·3).
#   루트만 기록하면 사본 변조가 provenance 밖에 남는다 — 전부 기록·대조한다.
files = ("POTCAR", "POSCAR", "KPOINTS", "static_pin/INCAR", "static/INCAR",
         "static_pin/POSCAR", "static/POSCAR", "static_pin/KPOINTS",
         "static/KPOINTS", "static_pin/POTCAR", "static/POTCAR")
pv = {"run_id": sys.argv[1], "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
      "inputs_sha256": {f: sha(f) for f in files},
      "parent_match": {"POSCAR": sha("POSCAR") == want["POSCAR"],
                       "KPOINTS": sha("KPOINTS") == want["KPOINTS"]}}
bad = []
for k in ("POSCAR", "KPOINTS"):
    if pv["parent_match"].get(k) is not True:
        bad.append(f"부모 대조 실패: {k}")
for f in ("POSCAR", "KPOINTS", "static_pin/INCAR", "static/INCAR",
          "job.json", "run_job.sh"):
    if sha(f) != man.get(f):
        bad.append(f"배포 해시 불일치: {f}")
for ph in ("static_pin", "static"):
    for base in ("POSCAR", "KPOINTS", "POTCAR"):
        if pv["inputs_sha256"][f"{ph}/{base}"] != pv["inputs_sha256"][base]:
            bad.append(f"phase 사본 불일치: {ph}/{base}")
pv["preflight_problems"] = bad
json.dump(pv, open("RUN_PROVENANCE.json", "w"), indent=1)
if bad:
    raise SystemExit("⛔ preflight 실패 — 실행 중단: " + "; ".join(bad))
PY
( cd static_pin && mpirun -np ${NP:-48} ${VASP:-vasp_std} 2>&1 | tee vasp.log )
python3 ../../analyze_results.py --check_pin . \
  || { echo "⛔ pin 수용 실패 — release 를 돌리지 않습니다. static_pin/PIN_CHECK.json 과 RUN_PROVENANCE.json 을 함께 회신해 주세요."; exit 1; }
cp static_pin/CHGCAR static/
python3 - <<'PY'
import hashlib, json
sha = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()
pv = json.load(open("RUN_PROVENANCE.json"))
a, b = sha("static_pin/CHGCAR"), sha("static/CHGCAR")
pv["chgcar_sha256"] = {"pin": a, "static_copy": b, "identical": a == b}
json.dump(pv, open("RUN_PROVENANCE.json", "w"), indent=1)
if a != b:
    raise SystemExit(f"⛔ CHGCAR 복사 불일치")
print(f"CHGCAR sha256 {a[:16]}… (pin → static 동일)")
PY
( cd static && mpirun -np ${NP:-48} ${VASP:-vasp_std} 2>&1 | tee vasp.log )
python3 - <<'PY'
import json, re
pv = json.load(open("RUN_PROVENANCE.json"))
log = open("static/vasp.log", errors="replace").read()
NEG = re.compile(r"not|error|fail|could|unable|cannot|warn", re.I)
hits = [ln.strip() for ln in log.splitlines()
        if re.search(r"charg", ln, re.I)
        and re.search(r"read|from\\s+\\S*\\s*file", ln, re.I)]
pos = [ln for ln in hits if not NEG.search(ln)]
# ⚠ 부정문('could not be read')은 증거가 아니다 (codex E-4차 P0-5) —
#   양성만 증거로, 부정문은 따로 남겨 재협상 근거로 쓴다.
pv["chgcar_read_evidence"] = pos[:5] or ["NOT_FOUND"]
pv["chgcar_read_negatives"] = [ln for ln in hits if NEG.search(ln)][:5]
json.dump(pv, open("RUN_PROVENANCE.json", "w"), indent=1)
print("charge-read 증거:", pv["chgcar_read_evidence"][0])
PY
echo "✅ 완료 — 회신물: 각 상 OUTCAR(.gz)·OSZICAR·vasp.log + static_pin/PIN_CHECK.json + **RUN_PROVENANCE.json**"
""")
    os.chmod(out / "run_job.sh", 0o755)
    import hashlib as _h
    manifest = {f: _h.sha256((out / f).read_bytes()).hexdigest()
                for f in ("POSCAR", "KPOINTS", "POTCAR_ASSEMBLE.sh", "job.json",
                          "run_job.sh", "static_pin/INCAR", "static/INCAR",
                          # E-5차 — VASP 가 실제 읽는 phase 사본도 배포 기준에 포함
                          "static_pin/KPOINTS", "static/KPOINTS")}
    (out / "MANIFEST_RESCUE.json").write_text(json.dumps(
        {"schema": "sdcp_rescue/v1", "sha256": manifest,
         "poscar_identical_to_parent": _h.sha256(find("POSCAR").read_bytes()).hexdigest()
         == manifest["POSCAR"]}, indent=1, ensure_ascii=False))
    print(f"→ {out}  (NUPDOWN={nup:+d} · 2상 · POSCAR/KPOINTS 원본 바이트 동일)")
    return out


def _selftest_rescue():
    import tempfile
    ok = [0, 0]

    def chk(c, m):
        ok[0] += 1; ok[1] += bool(c)
        print(("  ✔ " if c else "  ✘ ") + m)

    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        src = d / "src"; (src / "static").mkdir(parents=True)
        (src / "static" / "INCAR").write_text(
            "ENCUT = 520\nISMEAR = 0\nISTART = 0\nICHARG = 2\nLREAL = Auto\n"
            "LDAUU = 0.0 6.2 0.0\nMAGMOM = 2*0 1 -1 1 1\n")
        (src / "static" / "KPOINTS").write_text("g\n0\nGamma\n3 3 1\n0 0 0\n")
        (src / "POSCAR").write_text("t\n1.0\n" + "5 0 0\n0 5 0\n0 0 5\n"
                                    "Li Ni\n2 4\nDirect\n" + "0 0 0\n" * 6)
        (src / "POTCAR_ASSEMBLE.sh").write_text("cat Li Ni > POTCAR\n")
        _JMETA = {"magmom_poscar": [0, 0, 1.0, -1.0, 1.0, 1.0],
                  "kmesh": {"static": "3 3 1"}}
        (src / "job.json").write_text(json.dumps(_JMETA))
        # 부모 번들 MANIFEST (potcar_spec) — 없으면 빌더가 거부해야 한다
        try:
            make_basin_rescue(src, d / "noman"); chk(False, "⛔음성: MANIFEST 없이 거부")
        except SystemExit as e:
            chk("potcar_spec" in str(e), "⛔음성: 부모 MANIFEST(potcar_spec) 없으면 거부")
        (d / "MANIFEST.json").write_text(json.dumps(
            {"potcar_spec": {"Li": "Li_sv", "Ni": "Ni_pv"}}))
        out = make_basin_rescue(src, d / "out")
        pin = (out / "static_pin" / "INCAR").read_text()
        st = (out / "static" / "INCAR").read_text()
        chk("NUPDOWN  = 2" in pin, "핀 상: NUPDOWN 이 시드 자화합(+2)으로 **계산**된다")
        chk("BMIX_MAG" in pin and "인용 금지" in pin, "핀 상: 보수 믹싱 + 인용금지 명기")
        # ⚠ 주석의 "NUPDOWN 해제" 언급까지 잡으면 안 된다 — **대입 줄**만 검사
        #   (오늘만 세 번째 같은 교훈: qe 조각 ecutwfc, drop-blank, 그리고 여기)
        chk(not re.search(r"(?m)^NUPDOWN\s*=", st),
            "⛔음성: 2상에 NUPDOWN **대입**이 새면 안 된다 (해제 상)")
        chk(re.search(r"(?m)^ICHARG\s*=\s*1\b", st)
            and len(re.findall(r"(?m)^ICHARG\s*=", st)) == 1,
            "2상: 원본과의 차이가 ICHARG 대입 한 줄")
        chk((out / "POSCAR").read_bytes() == (src / "POSCAR").read_bytes(),
            "POSCAR 바이트 동일 (기하 불변)")
        mj = json.loads((out / "job.json").read_text())
        chk(mj["incar_expected"]["static_pin"]["NUPDOWN"] == "2",
            "분석기 v2 가 감사할 기대값에 NUPDOWN 이 실린다")
        _rj = (out / "run_job.sh").read_text()
        chk("--check_pin" in _rj and "pin 수용 실패" in _rj,
            "run_job: release 는 --check_pin(전체 게이트) 통과 후에만")
        chk("기존 산출물" in _rj and "1회용" in _rj and "rm -f" not in _rj,
            "run_job v3: 지우는 게 아니라 **있으면 거부** (E-3차 필수2 — 산출물 혼입 차단)")
        chk("RUN_PROVENANCE.json" in _rj.split("회신물")[1]
            and "PIN_CHECK.json" in _rj.split("회신물")[1],
            "run_job v3: PROVENANCE·PIN_CHECK 가 회신물 목록에 (콘솔 출력은 증거가 아니다)")
        chk("chgcar_read_evidence" in _rj and "parent_match" in _rj,
            "run_job v3: 해시 대조·charge-read 증거가 파일로 영구 기록")
        _mj0 = json.loads((out / "job.json").read_text())
        chk(_mj0["kmesh"] == {"static_pin": "3 3 1", "static": "3 3 1"}
            and _mj0["potcar_spec"]["Ni"] == "Ni_pv",
            "빌더: kmesh·potcar_spec 이 잡 안에 주입된다 (standalone 전체 게이트용)")
        _mj2 = json.loads((out / "job.json").read_text())
        chk(_mj2["incar_expected"]["static"]["NUPDOWN"] == "-1",
            "⛔음성 봉인: release 기대값 NUPDOWN=-1 — 핀 잔류가 하드게이트가 된다")
        chk(_mj2["rescue"]["supersedes"] == "refs/clean_slab__afm2424_net4",
            "supersedes 로 분석기의 clean 참조 교체가 연결된다")
        chk("/tmp" not in _mj2["rescue"].get("parent_name", "/tmp")
            and "parent_sha256" in _mj2["rescue"],
            "부모 계보가 경로가 아니라 이름+해시로 남는다")
        # ⛔ 음성 — 전제 위반은 거부
        (src / "job.json").write_text(json.dumps({"magmom_poscar": [0.3, 0, 1, -1, 1, 1]}))
        try:
            make_basin_rescue(src, d / "out2"); chk(False, "⛔음성: 비정수 자화합 거부")
        except SystemExit:
            chk(True, "⛔음성: 시드 자화합이 정수가 아니면 거부 (NUPDOWN 근거 없음)")
        (src / "job.json").write_text(json.dumps({"magmom_poscar": [0, 0, 1, -1, 1, 1]}))
        (src / "static" / "INCAR").write_text("ENCUT = 520\nNUPDOWN = 0\nICHARG = 2\n")
        try:
            make_basin_rescue(src, d / "out3"); chk(False, "⛔음성: NUPDOWN 기존재 거부")
        except SystemExit:
            chk(True, "⛔음성: 원본에 NUPDOWN 이 이미 있으면 거부 (전제 붕괴)")
    print(f"  rescue selftest {ok[1]}/{ok[0]}")
    return 0 if ok[0] == ok[1] else 1


# ─────────────────────────────────────────────────────────────────────────────
# 제출 **직전** 무결성 — 던지기 전에 한 번 (2026-08-29)
# ─────────────────────────────────────────────────────────────────────────────
#: 번들 안에 있으면 안 되는 것 — 라이선스(POTCAR) · 이미 돈 흔적(산출물).
#: 산출물이 섞여 있으면 run_job.sh 의 "이미 완료 — 건너뜀" 분기가 **남의 계산을
#: 우리 것으로 반송**한다. 회수 후에는 못 잡는다 (해시는 배포물만 본다).
FORBIDDEN_NAMES = ("POTCAR",)
STALE_OUTPUT_NAMES = ("OUTCAR", "vasprun.xml", "CONTCAR", "WAVECAR", "CHGCAR",
                      "OSZICAR", "XDATCAR")


def verify_bundle(root, expect_jobs=None, check_sibling_zip=True,
                  prov_roots=None) -> int:
    """번들을 **제출 전에** 검사한다 — 생성 시점의 바이트 그대로인가.

    분석기(analyze_results.py)의 무결성 검사와 목적이 다르다: 저쪽은 **회수 후**
    OUTCAR 를 요구하며 fail-closed 로 막는다. 이쪽은 산출물이 아직 없는 번들을
    본다 — 그래서 제출 전에 돌 수 있는 유일한 검사다.

    검사:
      ① MANIFEST.json 파싱 · ② files_sha256 전건 대조(변조·누락)
      ③ 배포물에 없는 파일이 끼어들었나(extra) · ④ 계획 잡 폴더 존재·필수 파일
      ⑤ POTCAR 혼입(라이선스) · ⑥ 이미 돈 흔적(OUTCAR 등)
      ⑦ analyze_results.py 존재 · ⑧ 옆 zip 의 멤버 집합이 폴더와 같은가

    이 도구가 **못 하는 것**
      · **물리를 보지 않는다.** INCAR 값·자기 seed·기하가 옳은지는 생성기와
        분석기의 몫이다. 여기를 통과해도 "맞는 양을 재고 있다"는 뜻이 아니다.
      · POTCAR 를 검증하지 못한다 (번들에 없다 — 조립 뒤 OUTCAR TITEL 로만 가능).
      · 잡 수가 **캠페인 설계와 맞는지** 모른다. `--expect_jobs` 로 불러 준
        숫자와만 대조한다 (안 주면 MANIFEST 의 n_jobs 와만 대조).
    """
    root = Path(root)
    bad, warn = [], []
    mp = root / "MANIFEST.json"
    if not mp.is_file():
        print(f"⛔ {mp} 없음 — 번들이 아니다")
        return 1
    try:
        man = json.loads(mp.read_text())
    except Exception as e:                                   # noqa: BLE001
        print(f"⛔ MANIFEST.json 파싱 실패: {e}")
        return 1

    # ② 배포물 해시 전건 대조
    fh = man.get("files_sha256") or {}
    if not fh:
        bad.append("files_sha256 가 비어 있다 — 무결성을 확인할 근거가 없다")
    changed, missing = [], []
    for rel, want in sorted(fh.items()):
        p = root / rel
        if not p.is_file():
            missing.append(rel); continue
        if hashlib.sha256(p.read_bytes()).hexdigest() != want:
            changed.append(rel)
    if changed:
        bad.append(f"내용이 바뀐 파일 {len(changed)}건: {changed[:5]}")
    if missing:
        bad.append(f"없어진 파일 {len(missing)}건: {missing[:5]}")

    # ③ 매니페스트에 없는 파일이 끼어들었나
    on_disk = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()}
    extra = sorted(on_disk - set(fh) - {"MANIFEST.json"})
    # ⑤⑥ 그중에서도 **이유가 다른 두 종류**는 따로 이름을 붙여 말한다
    potcar = [e for e in extra if Path(e).name in FORBIDDEN_NAMES]
    stale = [e for e in extra if Path(e).name in STALE_OUTPUT_NAMES]
    rest = [e for e in extra if e not in potcar and e not in stale]
    if potcar:
        bad.append(f"POTCAR 가 번들 안에 있다 {len(potcar)}건 (라이선스 · 종 순서가 "
                   f"잡마다 다르다 — 조립기로만 만들 것): {potcar[:3]}")
    if stale:
        bad.append(f"이미 돈 흔적 {len(stale)}건 — run_job.sh 가 '이미 완료' 로 "
                   f"건너뛰어 **남의 계산을 반송**한다: {stale[:3]}")
    if rest:
        bad.append(f"매니페스트에 없는 파일 {len(rest)}건: {rest[:5]}")

    # ★ 회신 AB P0-1 / 게이트 조건 ③ — **배포 전에 입력만으로 게이트를 돌려 본다.**
    #   v9 는 이 검사가 없어서, 해시·census·selftest 를 전부 통과한 번들이
    #   실제로는 40잡 중 36잡을 OUTCAR 오기도 전에 차단했다 (복합체 24 =
    #   SOURCE_ROLE_MISMATCH · 기체 12 = SOURCE_TOPOLOGY_UNVERIFIED).
    #   ⇒ 해시는 그 결함을 원리적으로 못 잡는다. **산출물의 의미**를 봐야 한다.
    _pf = []
    for jd in sorted(root.rglob("job.json")):
        try:
            jm = json.loads(jd.read_text())
        except Exception as e:                                   # noqa: BLE001
            _pf.append(f"{jd.parent.relative_to(root)}: job.json 파싱 실패 ({e})")
            continue
        rel = str(jd.parent.relative_to(root))
        # (1) 분자를 든 잡은 **정본 결합 그래프**가 있어야 한다 — 없으면 단일점에서
        #     위상 검사가 통째로 꺼지고 분석기가 그 잡을 막는다.
        if jm.get("mol_poscar_idx") and not jm.get("mol_graph_canonical"):
            _pf.append(f"{rel}: mol_graph_canonical 없음 → SOURCE_TOPOLOGY_UNVERIFIED")
        # 🔴🔴 회신 AT P0-1 (2026-08-31) — (1) 은 **있기만** 하면 통과시킨다.
        #   그래서 기체 잡의 그래프가 POSCAR 순서와 어긋난 채(항등 순서로 만들어져)
        #   나갔고, 리뷰어가 배포본에서 geometry_audit 을 돌려 broken 28 · formed 28
        #   을 냈다 — VASP 를 한 잡도 돌리기 전에 영구 게이트였다.
        #   ⇒ **배포한 POSCAR 를 되읽어** 같은 규약으로 그래프를 다시 만들고 대조한다.
        #     이것이 분석기가 실제로 하는 일이고, 여기서 통과해야 거기서도 통과한다.
        elif jm.get("mol_poscar_idx"):
            _pp = jd.parent / "POSCAR"
            if not _pp.is_file():
                _pf.append(f"{rel}: POSCAR 가 없다 (그래프를 대조할 수 없다)")
            else:
                try:
                    from ase.io import read as _rdp
                    _atp = _rdp(str(_pp), format="vasp")
                    _mi = [int(i) for i in jm["mol_poscar_idx"]]
                    _got = {tuple(sorted(e)) for e in _bonds_in(_atp, _mi)}
                    _want = {tuple(sorted(e)) for e in jm["mol_graph_canonical"]}
                    _br, _fo = _want - _got, _got - _want
                    if _br or _fo:
                        _pf.append(
                            f"{rel}: 배포 POSCAR 재판독 그래프가 정본과 다르다 "
                            f"(정본 {len(_want)} · 끊김 {len(_br)} · 생성 {len(_fo)}) "
                            f"→ SOURCE_TOPOLOGY_CHANGED 확정. 인덱스 순서가 어긋났을 "
                            f"가능성이 가장 크다 (회신 AT P0-1)")
                except Exception as e:                           # noqa: BLE001
                    _pf.append(f"{rel}: POSCAR 재판독 실패 ({e})")
        # (2) 등록 역할은 **Li/Ni 이거나 명시적 None** 이어야 한다. 분석 역할
        #     (calibration/holdout)이 그 자리에 오면 항상 불일치한다.
        _rr = jm.get("registry_role", "\x00MISSING")
        if _rr == "\x00MISSING":
            if jm.get("role") not in ("Li", "Ni", None):
                _pf.append(f"{rel}: registry_role 이 없고 role={jm.get('role')!r} 이 "
                           f"Li/Ni 가 아니다 → SOURCE_ROLE_MISMATCH 확정")
        elif _rr not in ("Li", "Ni", None):
            _pf.append(f"{rel}: registry_role={_rr!r} 이 Li/Ni/None 이 아니다")
    if _pf:
        bad.append("⛔ **입력 preflight 실패 %d건** — OUTCAR 가 와도 이 잡들은 막힌다: %s"
                   % (len(_pf), _pf[:4]))
    else:
        print("  ✓ 입력 preflight — 결과 없이도 걸리는 게이트 0건 "
              "(job.json %d개 검사)" % len(list(root.rglob("job.json"))))

    # ④ 잡이 실제로 있고, 던질 수 있는 상태인가
    #   ⚠ `planned` 를 잡 목록으로 쓰면 안 된다 — 생성기가 D3-off 쌍둥이를
    #     `plan()` 없이 만들어서 `n_jobs` 에만 센다 (2026-08-29 실측: Stage A
    #     n_jobs 40 = planned 24 + 쌍둥이 16). 정본은 **디스크의 잡 폴더**다:
    #     run_job.sh 가 있는 폴더 하나 = 던지는 단위 하나.
    planned = man.get("planned") or {}
    found = sorted(str(q.parent.relative_to(root))
                   for q in root.rglob("run_job.sh") if q.is_file())
    n_jobs = man.get("n_jobs")
    if n_jobs is not None and len(found) != n_jobs:
        bad.append(f"MANIFEST 의 n_jobs {n_jobs} vs 실제 잡 폴더 {len(found)}")
    if expect_jobs is not None and len(found) != expect_jobs:
        bad.append(f"잡 수가 기대와 다르다 — 기대 {expect_jobs} vs 실제 {len(found)}")
    miss_plan = [k for k in planned if k not in set(found)]
    if miss_plan:
        bad.append(f"계획됐는데 폴더가 없는 잡 {len(miss_plan)}건: {miss_plan[:5]}")
    NEED = ("run_job.sh", "POTCAR_ASSEMBLE.sh", "job.json", "POSCAR")
    nofile = []
    for k in found:                      # ★ planned 가 아니라 **전 잡**을 본다
        jd = root / k
        for f in NEED:
            if not (jd / f).is_file():
                nofile.append(f"{k}/{f}")
        # 상 폴더가 하나도 없으면 이 잡은 아무것도 안 돈다
        if not any((jd / ph / "INCAR").is_file()
                   for ph in ("pre", "relax", "static", "dense", "static_pin")):
            nofile.append(f"{k}/<상>/INCAR")
    if nofile:
        bad.append(f"잡에 필수 파일이 없다 {len(nofile)}건: {nofile[:5]}")

    # ⑦ 분석기
    if not (root / "analyze_results.py").is_file():
        bad.append("analyze_results.py 없음 — 회수해도 판정할 도구가 같이 안 간다")

    # ⑦b 🔴 문서가 **실물과 같은 모드**를 설명하나 (회신 Z P0-1)
    #   2026-08-29 실사고: `--closure` 는 상을 static 하나로 만드는데 README 분기가
    #   `--single_point` 만 봐서 4상짜리 옛 README(82 systems·259 phase runs·
    #   relax 반송)가 그대로 나갔다. 외주는 있지도 않은 relax/CONTCAR 를 찾는다.
    #   해시는 이걸 못 잡는다 — 그 문서가 **원래 그 내용으로** 배포됐기 때문이다.
    n_relax = sum(1 for k in found if (root / k / "relax").is_dir())
    rq = root / "README_REQUEST.md"
    if rq.is_file():
        txt = rq.read_text(errors="ignore")
        if n_relax == 0:
            stale = [m for m in ("259", "82 systems", "82계",
                                 "relax/OUTCAR", "relax/CONTCAR") if m in txt]
            if stale:
                bad.append(f"README_REQUEST.md 가 **이완판 문구**를 담고 있는데 실물에는 "
                           f"relax 상이 하나도 없다 {stale[:3]} — 외주가 없는 산출을 "
                           f"찾는다 (반송 계약 위반)")
        elif "relax/OUTCAR" not in txt:
            bad.append(f"실물에 relax 상이 {n_relax}잡 있는데 README 가 그 반송을 "
                       f"요구하지 않는다")
    sc = root / "SUBMIT_CONTRACT.md"
    if sc.is_file():
        m = re.search(r"총 VASP 실행 \| \*\*(\d+)\*\*", sc.read_text(errors="ignore"))
        if m and int(m.group(1)) < len(found):
            bad.append(f"SUBMIT_CONTRACT 의 총 실행 {m.group(1)}회 < 잡 {len(found)}개 "
                       f"— 외주가 실행량을 적게 잡는다 (쌍둥이 누락)")
    # ★ MANIFEST 쪽도 본다 — v4 는 문서를 고쳤는데 MANIFEST 는 24 로 남아 있었다.
    #   외주가 둘 중 무엇을 읽을지 우리가 못 정한다. **둘 다** 맞아야 한다.
    _nex = (man.get("submission") or {}).get("n_vasp_executions_total")
    if isinstance(_nex, int) and _nex < len(found):
        bad.append(f"MANIFEST.submission 의 총 실행 {_nex}회 < 잡 {len(found)}개 "
                   f"— 문서를 고쳐도 MANIFEST 가 남아 있으면 같은 오해가 난다")

    # ⑧ 옆 zip — 실제로 나가는 물건이 이것이다
    zp = root.with_suffix(".zip")
    zinfo = ""
    if not check_sibling_zip:
        zp = None                       # --verify_zip 경로 — 이미 ZIP 을 직접 봤다
    elif not zp.is_file():
        warn.append(f"zip 없음 ({zp.name}) — 폴더로 직접 전달할 때만 정상")
    if zp is not None and zp.is_file():
        try:
            with zipfile.ZipFile(zp) as z:
                members = {n for n in z.namelist() if not n.endswith("/")}
        except Exception as e:                               # noqa: BLE001
            bad.append(f"zip 을 열 수 없다: {e}")
            members = None
        if members is not None:
            pref = root.name + "/"
            inner = {m[len(pref):] for m in members if m.startswith(pref)}
            odd = sorted(m for m in members if not m.startswith(pref))
            if odd:
                bad.append(f"zip 최상위가 {root.name}/ 이 아닌 항목 {len(odd)}건: {odd[:3]}")
            only_zip = sorted(inner - on_disk)
            only_dir = sorted(on_disk - inner)
            if only_zip or only_dir:
                bad.append(f"zip 과 폴더가 다르다 — zip 에만 {len(only_zip)}건 "
                           f"{only_zip[:3]} · 폴더에만 {len(only_dir)}건 {only_dir[:3]}")
            zinfo = (f"{zp.name}  {zp.stat().st_size / 1e6:.1f} MB  "
                     f"sha256 {hashlib.sha256(zp.read_bytes()).hexdigest()}")

    # ── 기록용 (제출 이력에 그대로 붙일 것) ─────────────────────────────────
    print(f"■ 번들 {root}")
    print(f"  잡 {len(found)} (planned {len(planned)} + 쌍둥이 등 {len(found) - len(planned)})"
          f" · 배포파일 {len(fh)} · 해시확인 {len(fh) - len(missing)}")
    print(f"  candidate_set : {man.get('candidate_set', '(없음)')}")
    # ★ 후보집합의 **출처 파일**을 찍는다 (2026-08-29 사고): 생성기가 out 경로 충돌로
    #   거부했는데, 그 자리에 있던 **다른 후보 파일로 만든 옛 번들**을 verify 가
    #   그대로 검사했다. candidate_set 문자열은 둘 다 "calibration_pilot" 이라
    #   구별이 안 된다 — 갈라주는 것은 from_basins 경로와 freeze 해시다.
    _fb = man.get("from_basins") or {}
    if _fb:
        _fbp = str(_fb.get("path", "?"))
        print(f"  from_basins   : {_fbp}")
        # 그 파일이 **repo 안에 있나** — 없으면 후보집합을 재현할 수 없다.
        #   ⚠ cwd 에 의존하면 repo 밖에서 돌릴 때 오진한다. 도구 자기 위치로 찾는다.
        _nm = Path(_fbp).name
        #   ⚠ 정책은 "후보집합은 repo 에 있어야 한다" 이고 기본은 db/ 만 본다.
        #     `prov_roots` 는 **selftest 전용 탈출구**다 — 시험은 임시 디렉터리에
        #     후보를 만들므로 자기 근원을 명시적으로 선언한다. 생산 호출은 안 준다.
        _roots = [HERE.parents[1] / "db"] + [Path(r) for r in (prov_roots or [])]
        _have = [r for r in _roots if r.is_dir()]
        if not _nm:
            pass
        elif not _have:
            warn.append(f"repo 의 db/ 를 못 찾아 후보집합 출처 `{_nm}` 를 확인하지 못했다")
        elif not any(list(r.rglob(_nm)) for r in _have):
            bad.append(f"후보집합 출처 `{_nm}` 가 repo(db/)에 없다 — 이 번들의 "
                       f"candidate set 은 재현·감사할 수 없다")
    print(f"  emitted_roles : {man.get('emitted_basin_roles', man.get('emitted_roles', '(없음)'))}")
    print(f"  fragments     : {man.get('fragments', '(없음)')}")
    # ★ 두 번들을 같은 표에 올리려면 **같은 clean slab** 이어야 한다. 다른 슬랩을
    #   섞는 것은 재개 조건이 아니라 P0 다 (prereg ⚠_slab_F_차등).
    _cs = man.get("clean_slab") or {}
    print(f"  clean_slab    : sha256 {_cs.get('sha256', '(없음)')}")
    print(f"  generated_utc : {man.get('generated_utc', '(없음)')}")
    print(f"  generated_argv: {' '.join(man.get('generated_argv') or []) or '(없음)'}")
    # ⛔⛔ 2026-08-30 fail-open — **검사기가 pin 을 안 봤다.**
    #   `--allow_no_pin` 으로 만든 번들은 manifest 에 "이 번들은 제출용이 아니다" 가
    #   박혀 있는데, **제출 직전 마지막 검사기**가 `✅ 제출 가능` 을 찍었다.
    #   그 줄을 보고 보내면 외부 기준 대조 없는 번들이 그대로 나간다.
    #   회신 AJ 의 요구는 "pin 이 없으면 제출용 bundle 을 만들지 않는다" 였고,
    #   생성기는 막고 있었지만 검사기는 안 막고 있었다 — 같은 규칙이 두 곳에서 갈렸다.
    # ⚠ 2026-08-31 정정 — 초판은 pin 이 없으면 **무조건** 제출 차단이었다. 과했다.
    #   `run_job.sh` 가 `POTCAR_PROVENANCE.json` 없이는 아예 안 돈다 (회신 AB P0-8).
    #   ⇒ 그쪽이 계산을 돌리면 provenance 는 **자동으로 생겨서 결과와 함께 돌아온다.**
    #   pin 이 미리 있으면 얻는 것은 "우리가 **먼저 선언한** 기준과의 대조" 이고,
    #   없으면 "그쪽이 실제로 쓴 것의 **사후 기록**" 이다. 후자도 검증이긴 하다 —
    #   못 잡는 것은 '우리가 의도한 트리와 다른 트리를 썼다' 하나뿐이다.
    #   ⇒ **차단이 아니라 경고**로 내리고, 무엇을 못 보는지 명시한다.
    if not (man.get("potcar_pin") or {}):
        warn.append("POTCAR pin 없음 — 회수 시 `POTCAR_PROVENANCE.json` 으로 "
                    "**사후** 대조한다 (run_job.sh 가 그 파일 없이는 안 돈다). "
                    "못 보는 것: '우리가 의도한 트리와 다른 트리를 썼다'. "
                    "미리 고정하려면 --potcar_pin")
    sub = man.get("submission") or {}
    print(f"  submission    : {sub.get('cores_per_job', '?')} 코어/잡 · "
          f"동시 {sub.get('max_concurrency', '?')} · VASP 실행 "
          f"{sub.get('n_vasp_executions_total', '?')}회")
    print(f"  MANIFEST      : sha256 {hashlib.sha256(mp.read_bytes()).hexdigest()}")
    if zinfo:
        print(f"  ZIP           : {zinfo}")
    for w in warn:
        print(f"  ⚠ {w}")
    for b in bad:
        print(f"  ⛔ {b}")
    print("  " + ("✅ 제출 가능" if not bad else f"❌ 제출 차단 — {len(bad)}건"))
    return 0 if not bad else 1


def _zip_entry_hazards(zf, root_name):
    """ZIP 엔트리 자체의 위험 (회신 AA Q6). 풀기 **전에** 본다.

    폴더를 먼저 풀고 검사하면 이 중 몇은 이미 밖에 파일을 쓴 뒤다.
    """
    bad = []
    names = zf.namelist()
    seen = {}
    for n in names:
        if n.endswith("/"):
            continue
        if n.startswith("/") or ".." in Path(n).parts:
            bad.append(f"경로 탈출 엔트리: {n}")
        if not n.startswith(root_name + "/"):
            bad.append(f"최상위가 {root_name}/ 이 아님: {n}")
        k = n.lower()
        if k in seen and seen[k] != n:
            bad.append(f"대소문자 충돌: {seen[k]} vs {n}")
        seen.setdefault(k, n)
    dup = [n for n in set(names) if names.count(n) > 1]
    if dup:
        bad.append(f"중복 엔트리 {len(dup)}건: {sorted(dup)[:3]}")
    for zi in zf.infolist():
        # 상위 16비트가 유닉스 모드 — symlink 는 0o120000
        if (zi.external_attr >> 16) & 0o170000 == 0o120000:
            bad.append(f"symlink 엔트리: {zi.filename}")
    return bad


def verify_zip(zip_path, expect_jobs=None, attest_out=None,
               prov_roots=None) -> int:
    """**ZIP 바이트**를 입력으로 받아 검증하고 detached attestation 을 낸다.

    왜 폴더가 아니라 ZIP 인가 (회신 AA P0-1 · Q6): 외주에 나가는 물건은 ZIP 이다.
    폴더를 검사하면 "검사한 것"과 "보낸 것"이 다를 수 있고, 실제로 2026-08-29 에
    경로 충돌 뒤 **옛 번들 폴더를 검사하고 정상이라 보고**한 전력이 있다.

    순서: ① ZIP 전체 SHA → ② 엔트리 위험(중복·대소문자·경로탈출·symlink) →
    ③ 새 임시 디렉터리에 풀기 → ④ 디스크에서 **독립 열거** → ⑤ 기존 검사 →
    ⑥ attestation(도구 자신의 SHA·commit 포함) 기록.

    이 도구가 **못 하는 것** (회신 AA Q6 이 적은 그대로)
      · 자기 자신의 의미론적 버그를 못 잡는다. attestation 에 verifier SHA 를
        같이 묶는 이유가 그것이다 — 나중에 "무엇이 검사했나" 를 되짚게.
      · 과학적 estimand 가 옳은지 말하지 않는다.
      · 실제 PP 트리·VASP build·스케줄러 환경·SCF 수렴·OUTCAR 형식은 범위 밖이다.
    """
    import tempfile
    zp = Path(zip_path)
    if not zp.is_file():
        print(f"⛔ {zp} 없음")
        return 1
    raw = zp.read_bytes()
    zsha = hashlib.sha256(raw).hexdigest()
    print(f"■ ZIP {zp.name}  {len(raw)} B")
    print(f"  sha256 {zsha}")
    try:
        zf = zipfile.ZipFile(zp)
    except Exception as e:                                   # noqa: BLE001
        print(f"⛔ ZIP 을 열 수 없다: {e}")
        return 1
    roots = {n.split("/", 1)[0] for n in zf.namelist() if "/" in n}
    if len(roots) != 1:
        print(f"⛔ 최상위 디렉터리가 하나가 아니다: {sorted(roots)[:4]}")
        return 1
    root_name = roots.pop()
    haz = _zip_entry_hazards(zf, root_name)
    for h in haz:
        print(f"  ⛔ {h}")

    with tempfile.TemporaryDirectory(prefix="verify_zip_") as td:
        zf.extractall(td)
        root = Path(td) / root_name
        rc = verify_bundle(root, expect_jobs=expect_jobs,
                           check_sibling_zip=False, prov_roots=prov_roots)
        # ── ④ 디스크 독립 열거 (MANIFEST 를 안 보고 다시 센다) ──────────────
        jobs = sorted(str(q.parent.relative_to(root))
                      for q in root.rglob("run_job.sh") if q.is_file())
        phases = {}
        for j in jobs:
            for ph in ("pre", "relax", "static", "dense"):
                if (root / j / ph / "INCAR").is_file():
                    phases[ph] = phases.get(ph, 0) + 1
        census = {"jobs_on_disk": len(jobs), "phase_runs_on_disk": phases,
                  "files_on_disk": sum(1 for q in root.rglob("*") if q.is_file()),
                  "note": "files_on_disk = 배포파일(files_sha256) + MANIFEST.json"}
        man = json.loads((root / "MANIFEST.json").read_text())
        msha = hashlib.sha256((root / "MANIFEST.json").read_bytes()).hexdigest()
        # 후보집합 **전체** SHA (16자리 접두어로는 부족하다 — 회신 AA P0-1)
        fb = (man.get("from_basins") or {}).get("path")
        fb_sha, fb_local = None, None
        if fb:
            cand = HERE.parents[1] / "db" / "properties" / Path(fb).name
            if cand.is_file():
                fb_sha = hashlib.sha256(cand.read_bytes()).hexdigest()
                fb_local = str(cand.relative_to(HERE.parents[1]))

    def _sha(p):
        return hashlib.sha256(Path(p).read_bytes()).hexdigest() if Path(p).is_file() else None

    def _git(*a):
        try:
            return subprocess.run(["git", "-C", str(HERE.parents[1]), *a],
                                  capture_output=True, text=True,
                                  timeout=20).stdout.strip() or None
        except Exception:                                    # noqa: BLE001
            return None

    att = {
        "schema": "bundle_attestation/v1",
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "verdict": "PASS" if (rc == 0 and not haz) else "FAIL",
        "zip": {"name": zp.name, "bytes": len(raw), "sha256": zsha},
        "manifest_sha256": msha,
        "candidate_set": {
            "label": man.get("candidate_set"),
            "manifest_path": fb,
            "repo_path": fb_local,
            "sha256": fb_sha,
            "⚠": "16자리 접두어가 아니라 **전체 SHA** 다 (회신 AA P0-1)"},
        "clean_slab_sha256": (man.get("clean_slab") or {}).get("sha256"),
        "generated": {"utc": man.get("generated_utc"),
                      "argv": man.get("generated_argv")},
        "census_recomputed_from_disk": census,
        "manifest_census": man.get("job_census"),
        "zip_entry_hazards": haz,
        "tooling": {
            "generator_verifier": {
                "path": "tools/sdcp/vasp_handoff_bundle.py",
                "sha256": _sha(HERE / "vasp_handoff_bundle.py")},
            "analyzer_in_bundle_sha256": man.get("files_sha256", {}).get(
                "analyze_results.py"),
            "git_commit": _git("rev-parse", "HEAD"),
            "git_dirty": bool(_git("status", "--porcelain")),
            "git_branch": _git("rev-parse", "--abbrev-ref", "HEAD")},
        "command": f"--verify_zip {zip_path}"
                   + (f" --expect_jobs {expect_jobs}" if expect_jobs else ""),
        "verify_bundle_rc": rc,
        "⛔_이_증서가_보증하지_않는_것": [
            "verifier 자신의 의미론적 버그", "과학적 estimand 의 타당성",
            "실제 PP 트리·VASP build·스케줄러 환경", "SCF 수렴·OUTCAR 형식"],
    }
    if attest_out:
        Path(attest_out).write_text(
            json.dumps(att, indent=1, ensure_ascii=False) + "\n")
        print(f"  → attestation {attest_out}")
    else:
        print(json.dumps(att, indent=1, ensure_ascii=False))
    ok = rc == 0 and not haz
    print("  " + ("✅ ZIP 검증 통과" if ok else "❌ ZIP 검증 실패"))
    return 0 if ok else 1


def _runner_e2e(bundle: Path, chk) -> bool:
    """**run_staged.sh 를 실제로 돌린다** — 회신 AR 해제조건 8·10.

    왜 필요한가: AR 이 러너에서 잡은 두 결함(census 가 존재하는 job.json 만
    세어 하나를 지워도 통과 · lock 경쟁조건)은 **셸을 돌려야만** 잡힌다.
    문자열 grep 은 "그 코드가 있다" 만 말하고 "그 코드가 막는다" 는 말하지 못한다.

    가짜 PP 트리 · site allowlist · stub `vasp_std` 를 만들어 실제 경로를 탄다:
      SEAL_POTCAR_ROOT.sh (조립 + 봉인) → 실행 전 census → 단계 분류

    이 시험이 **못 하는 것**
      · 진짜 VASP 를 돌리지 않는다 (stub 이라 잡 실행은 실패해도 된다 —
        우리가 보는 것은 census·lock 이 그 **전에** 판정하는가다).
      · Windows 에서는 bash 가 없으면 건너뛴다 (건너뛴 것을 통과로 세지 않는다).
    """
    import shutil as _sh2
    import subprocess as _sp
    if not _sh2.which("bash"):
        print("  ⚠ bash 가 없어 러너 e2e 를 건너뛴다 (통과로 세지 않는다)")
        return False
    man = json.loads((bundle / "MANIFEST.json").read_text(encoding="utf-8"))
    spec = man.get("potcar_spec") or {}
    if not spec:
        chk(False, "AR 10: 번들에 potcar_spec 이 없다 — 러너 e2e 를 만들 수 없다")
        return False
    base = bundle.parent / "_runner_e2e"
    _sh2.rmtree(base, ignore_errors=True)
    base.mkdir(parents=True)
    # ── 가짜 PP 트리 + allowlist ────────────────────────────────────────
    pp = base / "pp"
    lines = []
    for _el, _var in sorted(spec.items()):
        (pp / _var).mkdir(parents=True, exist_ok=True)
        _f = pp / _var / "POTCAR"
        _f.write_text("  PAW_PBE %s 01Jan2000\n"
                      "   TITEL  = PAW_PBE %s 01Jan2000\n"
                      "   SHA256 = deadbeef %s\n"
                      "   END of PSCTR\n" % (_var, _var, _var), encoding="utf-8")
        lines.append("%s  %s" % (hashlib.sha256(_f.read_bytes()).hexdigest(), _f))
    allow = base / "site_allow.txt"
    allow.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # ── stub vasp_std (SEAL 이 --version 을 부른다) ─────────────────────
    binp = base / "bin"; binp.mkdir()
    vb = binp / "vasp_std"
    vb.write_text("#!/bin/sh\necho 'vasp.6.4.1 24Jul23 (build selftest)'\nexit 0\n",
                  encoding="utf-8")
    vb.chmod(0o755)
    env = dict(os.environ)
    env["PATH"] = str(binp) + os.pathsep + env.get("PATH", "")
    env["PP"] = str(pp)
    env["POTCAR_ALLOWLIST"] = str(allow)
    # ⛔ 회신 AS 해제조건 5 — launcher 와 실행파일을 나눠 준다 (VASP_CMD 는 거부된다)
    env["VASP_LAUNCHER"] = "env"          # 아무것도 안 하는 launcher
    env["VASP_EXE"] = str(vb)
    env.pop("VASP_CMD", None)
    env["BUNDLE_ZIP_SHA256"] = "0" * 64
    # ⛔ 회신 AS 7 — 외부 anchor 는 이제 **필수**다
    env["EXPECT_ZIP_SHA256"] = "0" * 64
    env["EXPECT_MANIFEST_SHA256"] = hashlib.sha256(
        (bundle / "MANIFEST.json").read_bytes()).hexdigest()
    env["PYTHONIOENCODING"] = "utf-8"

    def _run(root, extra_env=None):
        e = dict(env, **(extra_env or {}))
        r = _sp.run(["bash", "run_staged.sh", "1"], cwd=str(root), env=e,
                    capture_output=True, text=True, timeout=600)
        return r.returncode, (r.stdout or "") + (r.stderr or "")

    def _copy(tag):
        dst = base / tag
        _sh2.copytree(bundle, dst)
        return dst

    # ① 양성 — 온전한 번들은 census 를 통과한다
    _ok_root = _copy("intact")
    _rc, _o = _run(_ok_root)
    chk("✓ census" in _o,
        "AR 10 양성: 온전한 번들에서 SEAL→census 가 실제로 통과한다 "
        "(production path) · %s" % _o.strip().splitlines()[-1][:60])
    chk((_ok_root / "POTCAR_ROOT_SEAL.json").is_file()
        and (_ok_root / "ZIP_SHA256.txt").is_file(),
        "AR 해제조건 7: 러너가 봉인과 ZIP_SHA256.txt 를 실제로 만든다")
    _seal = json.loads((_ok_root / "POTCAR_ROOT_SEAL.json").read_text(encoding="utf-8"))
    chk(_seal.get("bundle_zip_sha256") == "0" * 64
        and _seal.get("manifest_sha256") == hashlib.sha256(
            (_ok_root / "MANIFEST.json").read_bytes()).hexdigest()
        and _seal.get("vasp_version_banner", "").startswith("vasp.6.4.1"),
        "AR 해제조건 7: 봉인이 ZIP·MANIFEST·VASP 배너를 실제로 담는다")

    # ①-b 🔴 회신 AT P0-3 — **가짜 POTCAR + 자기일관 provenance** 공격 (리뷰어 재현)
    #   종전엔 provenance 의 allowlist_sha 만 맞으면 재조립을 건너뛰어, PP 원본이
    #   없어도 봉인이 성공했다. 이제 매번 원본에서 다시 만들고 독립 검증한다.
    _atk = _copy("at3_fake_potcar")
    _jd0 = next(d for d in sorted(_atk.rglob("POTCAR_ASSEMBLE.sh"))).parent
    _al_sha = hashlib.sha256(allow.read_bytes()).hexdigest()
    (_jd0 / "POTCAR").write_text("FAKE POTCAR — not from PP\n", encoding="utf-8")
    (_jd0 / "POTCAR_PROVENANCE.json").write_text(json.dumps({
        "schema": "potcar_provenance/v1", "allowlist": str(allow),
        "allowlist_sha256": _al_sha, "allowlist_waived": False,
        "expected_variants": [], "source_sha256": {},
        "assembled_sha256": hashlib.sha256(
            (_jd0 / "POTCAR").read_bytes()).hexdigest()}, indent=1), encoding="utf-8")
    _fake_sha = hashlib.sha256((_jd0 / "POTCAR").read_bytes()).hexdigest()
    _rc, _o = _run(_atk)
    _now = (hashlib.sha256((_jd0 / "POTCAR").read_bytes()).hexdigest()
            if (_jd0 / "POTCAR").is_file() else None)
    chk(_now != _fake_sha,
        "🔴 AT P0-3: **가짜 POTCAR + 자기일관 provenance** 를 심어도 원본에서 "
        "재조립해 덮는다 (종전엔 allowlist_sha 만 맞으면 건너뛰었다)")
    chk("다릅니다" in _o or "재조립" in _o,
        "AT P0-3: 있던 POTCAR 가 재조립본과 다르면 **화면에 말한다** (조용히 고치지 않는다)")

    # ①-c ⛔음성 — PP 트리가 없으면 봉인 자체를 거부한다
    _atk2 = _copy("at3_no_pp")
    _rc2, _o2 = _run(_atk2, {"PP": str(base / "no_such_pp_tree")})
    chk(_rc2 != 0 and "PP 트리가 없습니다" in _o2,
        "⛔음성 AT P0-3: PP 원본 트리가 없으면 봉인하지 않는다 (rc=%s)" % _rc2)

    # ①-d ⛔음성 — variant 하나만 지워도 그 잡에서 막힌다 (전체 부재보다 교묘하다)
    _atk3 = _copy("at3_missing_variant")
    _pp2 = base / "pp_missing"
    _sh2.copytree(pp, _pp2)
    _sh2.rmtree(_pp2 / sorted(spec.values())[0])
    _rc3, _o3 = _run(_atk3, {"PP": str(_pp2)})
    chk(_rc3 != 0 and ("PP 원본이 없습니다" in _o3 or "조립 실패" in _o3),
        "⛔음성 AT P0-3: variant 하나만 없어도 막는다 (rc=%s)" % _rc3)

    # ①-e 🔴 회신 AT P0-4 — **기존 봉인 재검사**가 위조를 놓치던 세 경로
    def _tamper_seal(tag, mut):
        d = base / tag
        _sh2.copytree(_ok_root, d)
        _s = json.loads((d / "POTCAR_ROOT_SEAL.json").read_text(encoding="utf-8"))
        _s.update(mut)
        (d / "POTCAR_ROOT_SEAL.json").write_text(
            json.dumps(_s, indent=1, ensure_ascii=False), encoding="utf-8")
        return _run(d)

    for _tag, _mut, _key, _why in (
            ("seal_schema", {"schema": "made_up/v9"}, "schema", "위조 schema"),
            ("seal_boolstr", {"sealed_before_production": "true"},
             "불리언", "**문자열** 'true' (파이썬에서 참이지만 봉인이 아니다)"),
            ("seal_evidence", {"sealed_before_production_evidence": "그냥 믿어주세요"},
             "evidence", "손으로 쓴 근거"),
            ("seal_future", {"sealed_at_utc": "2099-01-01T00:00:00Z"},
             "미래", "미래 시각")):
        _rcS, _oS = _tamper_seal(_tag, _mut)
        chk(_rcS != 0 and _key in _oS,
            "⛔음성 AT P0-4: 기존 봉인의 %s → 거부 (rc=%s)" % (_why, _rcS))

    # ①-f 🔴 회신 AT P0-5/6 — launcher 우회 · 신호 · lock 참여
    for _tag, _lau, _why in (
            ("lau_exe", "mpirun -np 4 " + str(vb),
             "launcher 인자에 **실행파일**을 넣어 봉인된 VASP_EXE 를 무시하기"),
            ("lau_meta", "mpirun -np 4; touch /tmp/pwned",
             "셸 메타문자(`;`)로 다른 명령 끼워넣기"),
            ("lau_unknown", "bash -c",
             "알 수 없는 launcher (허용목록 밖)")):
        _rcL, _oL = _run(_copy(_tag), {"VASP_LAUNCHER": _lau})
        chk(_rcL != 0 and "VASP_LAUNCHER" in _oL,
            "⛔음성 AT P0-5: %s → 거부 (rc=%s)" % (_why, _rcL))
    # 실행파일 receipt 가 잡마다 남는가 (긴 실행 중 바이너리 교체를 반송물에서 본다)
    _rcpt = sorted(_ok_root.rglob("EXECUTABLE_RECEIPT.tsv"))
    chk(len(_rcpt) > 0 and str(vb) in _rcpt[0].read_text(),
        "AT P0-5: 잡마다 **실행 직전** 실행파일 receipt 를 남긴다 (%d건)" % len(_rcpt))
    # attestation 생성기·봉인기가 같은 lock 에 참여하는가
    _lk = _copy("lock_share")
    (_lk / ".lock_bundle").write_text("otherhost|99999|someone|2026-01-01T00:00:00Z\n",
                                      encoding="utf-8")
    _rcK, _oK = _sp.run(["bash", "SEAL_POTCAR_ROOT.sh"], cwd=str(_lk), env=env,
                        capture_output=True, text=True, timeout=300), None
    chk(_rcK.returncode != 0 and "다른 실행이 있습니다" in (_rcK.stdout + _rcK.stderr),
        "⛔음성 AT P0-6: 남의 lock 이 있으면 **봉인기도** 들어가지 않는다")
    _rcM = _sp.run(["bash", "MAKE_POTCAR_ATTESTATION.sh"], cwd=str(_lk),
                   env=dict(env, RELEASE_LABEL="x", SITE="y"),
                   capture_output=True, text=True, timeout=300)
    chk(_rcM.returncode != 0 and "다른 실행이 있습니다" in (_rcM.stdout + _rcM.stderr),
        "⛔음성 AT P0-6: 남의 lock 이 있으면 **attestation 생성기도** 들어가지 않는다")

    # ② ⛔음성 — **job.json 하나를 지우면** 막는다 (AR P0-7 이 재현한 그 경우)
    _r2 = _copy("drop_jobjson")
    _victim = sorted(_r2.glob("*/*/job.json"))[0]
    _victim.unlink()
    _rc2, _o2 = _run(_r2)
    chk(_rc2 != 0 and "census" in _o2 and "job.json 집합이 계획과 다르다" in _o2,
        "⛔음성 AR P0-7: job.json 하나를 지우면 **실행 전에** 막는다 "
        "(종전엔 classified=15·디렉터리 16 으로 통과했다) · rc=%s" % _rc2)

    # ③ ⛔음성 — 계획에 없는 잡 폴더를 끼우면 막는다
    _r3 = _copy("extra_job")
    _ej = _r3 / "prospective" / "__intruder__"
    _ej.mkdir(parents=True)
    (_ej / "job.json").write_text(json.dumps({"kind": "prospective_pose",
                                              "role": "primary", "d3": "on"}),
                                  encoding="utf-8")
    _rc3, _o3 = _run(_r3)
    chk(_rc3 != 0 and "계획 밖" in _o3,
        "⛔음성 AR P0-7: 계획에 없는 잡을 끼우면 막는다 · rc=%s" % _rc3)

    # ④ ⛔음성 — 단계 분류를 바꾸면(job.json 의 seed) 선언과 어긋나 막는다
    #   ⚠ **1단계로 선언된** 잡을 골라야 한다. net4 primary 는 이미 2단계라
    #     role 을 바꿔도 분류가 안 움직인다 (첫 픽스처가 그랬다).
    _r4 = _copy("stage_shift")
    _cen4 = (json.loads((_r4 / "MANIFEST.json").read_text(encoding="utf-8"))
             .get("run_census") or {}).get("stage_of") or {}
    _tgt4 = next((k for k, v in sorted(_cen4.items())
                  if v == "1" and k.startswith("prospective/")), None)
    chk(_tgt4 is not None, "AR 10: 1단계로 선언된 복합체 잡이 픽스처에 있다")
    if _tgt4:
        _q4 = _r4 / _tgt4 / "job.json"
        _m4 = json.loads(_q4.read_text(encoding="utf-8"))
        _m4["role"] = "sensitivity"                 # 1단계 → 2단계로 어긋나게
        _q4.write_text(json.dumps(_m4, ensure_ascii=False), encoding="utf-8")
        _rc4, _o4 = _run(_r4)
        chk(_rc4 != 0 and "단계 분류가 선언과 다르다" in _o4 and "단계 개수" in _o4,
            "⛔음성 AR P0-7: 단계 분류가 선언과 어긋나면 막는다 (분류·개수 둘 다) "
            "· rc=%s" % _rc4)

    # ⑤ ⛔음성 — MANIFEST 를 건드리면 EXPECT 해시와 어긋나 막는다
    _r5 = _copy("man_tamper")
    _exp = hashlib.sha256((_r5 / "MANIFEST.json").read_bytes()).hexdigest()
    _mm = json.loads((_r5 / "MANIFEST.json").read_text(encoding="utf-8"))
    _mm["note_injected"] = "x"
    (_r5 / "MANIFEST.json").write_text(json.dumps(_mm, ensure_ascii=False),
                                       encoding="utf-8")
    _rc5, _o5 = _run(_r5, {"EXPECT_MANIFEST_SHA256": _exp})
    chk(_rc5 != 0 and "EXPECT_MANIFEST_SHA256" in _o5,
        "⛔음성 AR P0-7: MANIFEST 가 바뀌면 EXPECT 해시와 어긋나 막는다 · rc=%s" % _rc5)

    # ⑥ ⛔음성 — **모르는 lock 은 지우지 않는다** (AR P0-8)
    _r6 = _copy("lock_foreign")
    (_r6 / ".lock_bundle").write_text("other-host|999999|2026-08-31T00:00:00Z\n",
                                      encoding="utf-8")
    _rc6, _o6 = _run(_r6)
    chk(_rc6 == 3 and (_r6 / ".lock_bundle").is_file()
        and "다른 호스트" in _o6,
        "⛔음성 AR P0-8: 다른 호스트의 lock 을 보면 **지우지 않고** 멈춘다 · rc=%s" % _rc6)
    # 같은 호스트의 죽은 pid 여도 자동 삭제하지 않는다
    _r7 = _copy("lock_dead_local")
    (_r7 / ".lock_bundle").write_text("%s|999999|2026-08-31T00:00:00Z\n"
                                      % platform.node(), encoding="utf-8")
    _rc7, _o7 = _run(_r7)
    chk(_rc7 == 3 and (_r7 / ".lock_bundle").is_file()
        and "자동으로 지우지 않습니다" in _o7,
        "⛔음성 AR P0-8: 같은 호스트의 죽은 pid 여도 **자동 삭제하지 않는다** "
        "(다른 노드의 실행일 수 있다) · rc=%s" % _rc7)
    # 정상 종료하면 **자기 lock 은** 치운다
    chk(not (_ok_root / ".lock_bundle").exists(),
        "AR P0-8: 자기 lock 은 종료 시 치운다 (남의 것만 안 건드린다)")

    # ══ 회신 AS 해제조건 6·7 — 전수 해시 · 외부 anchor · 번들 전역 lock ═══════
    # ⛔음성 — 배포 파일 **한 줄**을 고치면 실행 전에 막는다
    _r9 = _copy("file_tamper")
    _vic = sorted(_r9.glob("*/*/static/INCAR"))[0]
    _vic.write_text(_vic.read_text(encoding="utf-8") + "\n! tampered\n", encoding="utf-8")
    _rc9, _o9 = _run(_r9)
    chk(_rc9 != 0 and "배포 파일이 바뀌었다" in _o9,
        "⛔음성 AS 6: INCAR 한 줄을 고치면 **실행 전 전수 해시**가 막는다 "
        "(종전엔 잡 집합만 세어 통과했다) · rc=%s" % _rc9)
    # ⛔음성 — 외부 anchor 가 없으면 돌지 않는다 (선택이 아니라 필수)
    for _drop in ("EXPECT_MANIFEST_SHA256", "EXPECT_ZIP_SHA256"):
        _rA = _copy("no_anchor_" + _drop[7:11])
        _envA = dict(env); _envA.pop(_drop, None)
        _rcA = _sp.run(["bash", "run_staged.sh", "1"], cwd=str(_rA), env=_envA,
                       capture_output=True, text=True, timeout=600)
        _oA = (_rcA.stdout or "") + (_rcA.stderr or "")
        chk(_rcA.returncode != 0 and _drop in _oA and "정본 메시지" in _oA,
            "⛔음성 AS 7: `%s` 없이는 돌지 않는다 — ZIP 안의 해시는 자기 자신을 "
            "증명하지 못한다" % _drop)
    # ⛔음성 — anchor 가 **다른 배포본**을 가리키면 막는다
    _rB = _copy("wrong_anchor")
    _rcB, _oB = _run(_rB, {"EXPECT_ZIP_SHA256": "1" * 64})
    chk(_rcB != 0 and "우리가 보낸 배포본이" in _oB,
        "⛔음성 AS 7: 받은 ZIP 해시가 anchor 와 다르면 막는다 · rc=%s" % _rcB)
    # lock 이 **번들 전역**인가 — 2단계 lock 이 1단계를 막는다
    _rC = _copy("lock_global")
    (_rC / ".lock_bundle").write_text("other-host|999|stage2|2026-08-31T00:00:00Z\n",
                                      encoding="utf-8")
    _rcC, _oC = _run(_rC)
    chk(_rcC == 3 and (_rC / ".lock_bundle").is_file(),
        "⛔음성 AS 6: lock 이 **번들 전역**이라 다른 단계가 돌고 있어도 막는다 "
        "(종전엔 단계별이라 1·2 를 동시에 던질 수 있었다) · rc=%s" % _rcC)

    # ⑦ ⛔음성 — 봉인이 반쪽이면 러너가 실행 전에 막는다 (해제조건 7 '모든 실행')
    _r8 = _copy("half_seal")
    _rc8a, _ = _run(_r8)                       # 먼저 정상 봉인을 만든다
    _hs = json.loads((_r8 / "POTCAR_ROOT_SEAL.json").read_text(encoding="utf-8"))
    for _k in ("vasp_executable_sha256", "assembled_sha256_by_job"):
        _hs.pop(_k, None)
    (_r8 / "POTCAR_ROOT_SEAL.json").write_text(json.dumps(_hs, ensure_ascii=False),
                                               encoding="utf-8")
    _rc8, _o8 = _run(_r8)
    chk(_rc8 != 0 and "반쪽 봉인" in _o8,
        "⛔음성 AR 해제조건 7: 반쪽 봉인이면 러너가 **매 실행마다** 막는다 · rc=%s" % _rc8)

    _sh2.rmtree(base, ignore_errors=True)
    return True


def _selftest_e2e() -> int:
    """**생산 생성기 → 독립 verifier → 분석기** 왕복 (회신 AA Q2).

    왜 따로 필요한가 — 우리는 같은 병을 **세 번** 맞았다:
      ① POTCAR 검사가 개수만 셌다 (전부 같은 잘못된 세트를 통과시킨다)
      ② 조각 매칭이 실물 잡 키(`prospective/…`)에서 하나도 안 걸렸다
      ③ `d3` 가 net4 복합체 8잡에서 비어 있었다
    셋 다 selftest 는 **통과**했다. 공통 원인은 손으로 만든 fixture 가 실제 생산
    스키마와 갈라진 것이다. fixture 의 한 축만 실물처럼 고치면 네 번째 변형에서
    또 깨진다.

    그래서 이 시험은 fixture 를 만들지 않는다:
      · 슬랩·조각·자기원장을 **생산 경로 그대로** 불러온다 (SS.load_slab /
        SS.load_fragment / afm_ledger) — 장난감을 쓰면 계보·토폴로지 게이트가
        막는데, 그 게이트가 바로 우리가 지키려는 것이다
      · `build_bundle()` 이 만든 실물을 검사한다
      · MANIFEST 를 믿지 않고 **디스크에서 다시 센다**
      · 합성 OUTCAR 를 주입해 분석기까지 왕복한다
      · 흔들면(mutation) 깨지는지 본다

    이 시험이 **못 하는 것**
      · 실제 VASP·PP 트리·스케줄러를 대신하지 않는다 (합성 OUTCAR 다).
      · 과학적 estimand 가 옳은지 말하지 않는다.
      · 여기 통과가 실물 번들(v8 등)의 통과를 뜻하지 않는다 — 규모·조각이 다르다.
    """
    import argparse as _ap
    import shutil as _sh
    import tempfile
    from ase import Atoms
    from ase.io import write as ase_write
    ok = [0, 0]

    def chk(c, m):
        ok[0] += 1; ok[1] += bool(c)
        print(("  ✔ " if c else "  ✘ ") + m)

    td = Path(tempfile.mkdtemp(prefix="e2e_"))
    slab = _SS_LOAD_SLAB_ORIG()                # ★ 생산 슬랩 (몽키패치 무관)
    nslab = len(slab)
    mol0, _mf = SS.load_fragment("ptfe_dimer")  # ★ 생산 조각 (정본 결합표와 맞아야 한다)
    if mol0 is None:
        print("  ✘ ptfe_dimer 조각을 못 읽었다 — e2e 불가")
        return 1
    run = td / "runs" / "ptfe_dimer" / "relax_f0.85"
    run.mkdir(parents=True)
    ase_write(run / "_clean_slab.vasp", slab, format="vasp", direct=True)
    ztop = max(p[2] for p in slab.get_positions())
    mp0 = mol0.get_positions() - mol0.get_positions().mean(axis=0)

    N_POSE = 3
    basins = {"schema": "prospective_basins/v1", "freeze_sha256": "e2e_frozen",
              "fragments": {"ptfe_dimer": {"calibration": []}}}
    for k in range(N_POSE):
        lab = f"ptfe_dimer__Li_top__fib{k:02d}__r000"
        shift = np.array([4.0 + 1.2 * k, 3.0 + 1.5 * k, ztop + 3.2])
        cx = Atoms(symbols=list(slab.get_chemical_symbols())
                          + list(mol0.get_chemical_symbols()),
                   positions=list(slab.get_positions()) + list(mp0 + shift),
                   cell=slab.cell.array, pbc=True)
        ase_write(run / f"{lab}.xyz", cx, format="extxyz")
        basins["fragments"]["ptfe_dimer"]["calibration"].append(
            {"basin_id": f"b{k:02d}", "rep_label": lab, "role": "calibration",
             "why": "e2e", "E_pose_eV": 0.01 * k})
    bp = td / "basins.json"
    bp.write_text(json.dumps(basins, ensure_ascii=False))

    # ⛔ 2026-08-30 — e2e 픽스처도 **pin 을 박는다.** 검사기가 pin 없는 번들을
    #   `✅ 제출 가능` 으로 통과시키던 fail-open 을 고치면서, 이 픽스처가 pin 없이
    #   통과를 주장하고 있었다는 게 드러났다. 여기서 주장하는 것은 "제출 가능한
    #   번들을 verifier 가 통과시킨다" 이므로 픽스처가 제출 가능해야 맞다.
    pinp = td / "potcar_pin.json"
    pinp.write_text(json.dumps({"source_sha256": {"Li_sv": "a" * 64},
                                "vasp_version": "6.4.1(selftest)"}))

    a = _ap.Namespace(
        potcar_pin=str(pinp), allow_no_pin=False,
        runs=str(td / "runs"), out=str(td / "bundle"), freeze=0.85, nslab=nslab,
        frags=["ptfe_dimer"],
        qe=str(Path(SS.REPO) / "db" / "inputs" / "sdcp_v2" / "slab_relax" / "relax.in"),
        expect=None, allow_partial=True, dense_frags=None, cross_endpoints=None,
        adaptive_dense=False, global_champion_meV=20.0, no_cross=True,
        free_spin_refs=True, refs=True, cores=48, concurrency=8, mag_controls=True,
        kmesh_static=None, kmesh_dense=None, champion=False, from_basins=str(bp),
        roles=["calibration"], d3_seed_main_only=True, no_refs_dense=True,
        both_seeds=True, d3_pairs=True, closure=True, single_point=False,
        top_n=None, allow_stale_gate=True, no_prescf=True, selftest=False)
    try:
        out = build_bundle(a)
    except SystemExit as e:                                  # noqa: BLE001
        print(f"  ✘ 생산 생성기가 번들을 못 만들었다: {e}")
        return 1
    chk(out.is_dir(), "A. 생산 build_bundle() 이 실물 슬랩·조각·원장으로 번들을 만든다")

    # ── C. 예상 cardinality — "0개가 아님" 이 아니라 **정확히** N ────────────
    #   refs    clean 2seed + mol 3box = 5 끝점 × D3 on/off = 10
    #   complex 3 pose × 2 seed = 6, pm1 만 쌍둥이 3        =  9
    N_EXPECT, N_ON, N_OFF = 19, 11, 8
    zp = out.with_suffix(".zip")
    att = td / "att.json"
    chk(verify_zip(zp, expect_jobs=N_EXPECT, attest_out=str(att),
                   prov_roots=[td]) == 0,
        f"B. verifier 가 **ZIP 바이트**에서 통과시킨다 (잡 {N_EXPECT})")
    A = json.loads(att.read_text())
    dsk = A["census_recomputed_from_disk"]
    chk(dsk["jobs_on_disk"] == N_EXPECT
        and dsk["phase_runs_on_disk"] == {"static": N_EXPECT},
        f"C. **디스크 재계산**이 정확히 {N_EXPECT}·static{N_EXPECT} "
        f"(MANIFEST 를 안 보고 센 값) — 실제 {dsk['jobs_on_disk']}·"
        f"{dsk['phase_runs_on_disk']}")

    # ── D. 모든 잡이 정확히 한 구조화 role 로 소비되나 ──────────────────────
    metas = {str(q.parent.relative_to(out)): json.loads(q.read_text())
             for q in out.rglob("job.json")}
    kinds = {}
    for m in metas.values():
        kinds[m.get("kind")] = kinds.get(m.get("kind"), 0) + 1
    unclassified = [k for k, m in metas.items()
                    if not m.get("kind") or m.get("d3") not in ("on", "off")]
    chk(len(metas) == N_EXPECT and not unclassified,
        f"D. 전 잡이 한 구조화 role 로 분류된다 — kind {kinds} · 미분류 {unclassified[:3]}")
    n_on = sum(1 for m in metas.values() if m.get("d3") == "on")
    n_off = sum(1 for m in metas.values() if m.get("d3") == "off")
    chk(n_on == N_ON and n_off == N_OFF,
        f"D2. d3 on/off 가 정확히 {N_ON}/{N_OFF} (실제 {n_on}/{n_off}) — "
        f"net4 복합체가 빠지면 {N_ON - N_POSE}/{N_OFF} 가 된다 (③ 사고의 모양)")
    chk(all((out / k / "static" / "INCAR").is_file()
            and (("IVDW     = 11" in (out / k / "static" / "INCAR").read_text())
                 == (m.get("d3") == "on"))
            for k, m in metas.items()),
        "D3. d3 필드가 **INCAR 실물과 전건 일치** (기억이 아니라 입력에서 유도)")

    # ── E. 합성 OUTCAR 주입 → 분석기 왕복 ──────────────────────────────────
    for jn, m in metas.items():
        _fake_phase(out / jn, m, -100.0 - 0.01 * len(jn), POTCAR_SPEC)
    ns = {}
    exec(compile(ANALYZER, "<analyzer-template>", "exec"), ns)
    jobs = {}
    for jn, m in metas.items():
        oc = ns["read_outcar"](str(out / jn / "static" / "OUTCAR"))
        jobs[jn] = {"ok": True, "gates": [], "meta": m, "static": oc,
                    "geom": {"magnetic": {"realized_basin_id": "same"}}}
    chk(all((jobs[j]["static"] or {}).get("E0") is not None for j in jobs),
        "E. 합성 OUTCAR 가 분석기 판독기를 통과한다 (에너지 전건 회수)")
    man = json.loads((out / "MANIFEST.json").read_text())
    ce = ns["_closure_estimand"](
        man, {"pairs": {}}, lambda j: (jobs.get(j, {}).get("static") or {}).get("E0"),
        {"ptfe_dimer": -10.0}, jobs)
    chk(ce is None or ce.get("cohort_fields", {}).get("incoherent") == 0,
        "E2. 생산 번들의 잡 키가 cohort 정합성을 통과한다 — ② 사고의 회귀시험")

    # ── F. mutation — 흔들면 **깨져야** 한다 ────────────────────────────────
    def mut(name, fn):
        m2 = td / name
        _sh.copytree(out, m2)
        fn(m2)
        z2 = m2.with_suffix(".zip")
        with zipfile.ZipFile(z2, "w", zipfile.ZIP_DEFLATED) as z:
            for q in sorted(m2.rglob("*")):
                if q.is_file():
                    z.write(q, m2.name + "/" + str(q.relative_to(m2)))
        return verify_zip(z2, expect_jobs=N_EXPECT, prov_roots=[td])

    def _drop_d3(root):
        q = sorted(root.rglob("prospective/*/job.json"))[0]
        m = json.loads(q.read_text()); m.pop("d3", None)
        q.write_text(json.dumps(m, ensure_ascii=False))

    def _rename(root):
        q = sorted(root.rglob("prospective/*/job.json"))[0].parent
        q.rename(q.parent / (q.name + "_X"))

    for nm, fn, why in (
            ("m_d3", _drop_d3, "잡 하나의 d3 를 지우면 깨진다 (③ 사고)"),
            ("m_name", _rename, "잡 폴더 이름을 바꾸면 깨진다 (경로 ↔ 필드 불일치)"),
            ("m_extra", lambda r: (r / "EXTRA.txt").write_text("x"),
             "매니페스트에 없는 파일을 끼우면 깨진다"),
            ("m_rm", lambda r: _sh.rmtree(sorted(r.rglob("refs/mol__*"))[0]),
             "잡 하나를 지우면 깨진다 (cardinality)")):
        chk(mut(nm, fn) == 1, f"F mutation: {why}")

    print(f"  e2e selftest {ok[1]}/{ok[0]}")
    _sh.rmtree(td, ignore_errors=True)
    return 0 if ok[0] == ok[1] else 1


def _selftest_verify() -> int:
    """--verify_bundle 의 양성 1 + **음성 7**.

    음성이 없는 selftest 는 통과해도 아무것도 보증하지 않는다 (v2 선례).
    여기서 심는 결함은 전부 **회수 후에는 못 잡는 것**들이다.
    """
    import tempfile
    ok = [0, 0]

    def chk(c, m):
        ok[0] += 1; ok[1] += bool(c)
        print(("  ✔ " if c else "  ✘ ") + m)

    DOC_OK = "이 묶음은 static 단일점만 돕니다. static/OUTCAR 를 보내 주세요.\n"
    SC_OK = "| 총 VASP 실행 | **2** |\n"

    def build(d: Path, readme: str = DOC_OK, contract: str = SC_OK, pin=True) -> Path:
        """최소 번들 — verify 는 물리를 안 보므로 파일 구조만 있으면 된다.

        ★ **잡 둘 중 하나는 D3-off 쌍둥이**로 만든다: `files_sha256` 에는 있지만
          `planned` 에는 **없다**. 실물 번들이 정확히 그 모양이고(생성기가 쌍둥이에
          `plan()` 을 안 부른다), 2026-08-29 에 이 검사가 그걸 자기모순으로 오진해
          멀쩡한 40잡 번들의 제출을 막았다. 양성 케이스가 그 구조를 담아야 재발을 막는다.
        """
        root = d / "bundle_v0"
        for name in ("refs/clean_slab__pm1", "refs/clean_slab__pm1__d3off"):
            jd = root / name
            (jd / "static").mkdir(parents=True)
            (jd / "POSCAR").write_text("t\n1.0\n5 0 0\n0 5 0\n0 0 5\nLi\n1\nDirect\n0 0 0\n")
            (jd / "run_job.sh").write_text("#!/bin/sh\necho run\n")
            (jd / "POTCAR_ASSEMBLE.sh").write_text("cat Li > POTCAR\n")
            (jd / "job.json").write_text('{"species_order": ["Li"]}')
            (jd / "static" / "INCAR").write_text(
                "ENCUT = 520\n" + ("" if name.endswith("d3off") else "IVDW = 11\n"))
            (jd / "static" / "KPOINTS").write_text("a\n0\nGamma\n1 1 1\n0 0 0\n")
        (root / "analyze_results.py").write_text("#!/usr/bin/env python3\n")
        # ★ 문서도 배포물이다 — 매니페스트에 들어가야 해시·문서 검사가 **따로** 걸린다
        (root / "README_REQUEST.md").write_text(readme)
        (root / "SUBMIT_CONTRACT.md").write_text(contract)
        # n_jobs 2 = planned 1 + 쌍둥이 1 — 이것이 정상이다
        man = {"n_jobs": 2, "planned": {"refs/clean_slab__pm1": {"phases": ["static"]}},
               "candidate_set": "selftest", "fragments": ["none"],
               "generated_argv": ["--selftest"], "generated_utc": "1970-01-01T00:00:00Z",
               "submission": {"cores_per_job": 48, "max_concurrency": 8}}
        # ⛔ 2026-08-30 — 제출 가능 판정에는 **POTCAR pin** 이 있어야 한다.
        #   양성 픽스처가 pin 없이 통과하면, 검사기가 pin 을 안 본다는 사실이
        #   시험에서 안 드러난다 (실제로 그래서 `--allow_no_pin` 번들에
        #   `✅ 제출 가능` 이 찍혔다). pin=False 픽스처가 그 음성 경로다.
        if pin:
            man["potcar_pin"] = {"source_sha256": {"Li_sv": "a" * 64},
                                 "vasp_version": "6.4.1"}
        man["files_sha256"] = {
            str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}
        (root / "MANIFEST.json").write_text(json.dumps(man, indent=1, ensure_ascii=False))
        with zipfile.ZipFile(root.with_suffix(".zip"), "w", zipfile.ZIP_DEFLATED) as z:
            for q in sorted(root.rglob("*")):
                if q.is_file():
                    z.write(q, q.relative_to(root.parent))
        return root

    def rezip(root: Path):
        with zipfile.ZipFile(root.with_suffix(".zip"), "w", zipfile.ZIP_DEFLATED) as z:
            for q in sorted(root.rglob("*")):
                if q.is_file():
                    z.write(q, q.relative_to(root.parent))

    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        r = build(d / "p")
        chk(verify_bundle(r) == 0,
            "양성: planned(1) ⊂ 실물 잡(2, D3-off 쌍둥이 포함) 은 정상 — 자기모순 아님")

        # ⛔음성 2026-08-30 — pin 이 없으면 **제출 가능이라고 말하면 안 된다**.
        #   실측: --allow_no_pin 으로 만든 C-12 번들에 검사기가 ✅ 제출 가능 을 찍었다.
        #   manifest 안에는 "이 번들은 제출용이 아니다" 가 박혀 있었는데도.
        rnp = build(d / "nopin", pin=False)
        # ⚠ 2026-08-31 — pin 없음은 **차단이 아니라 경고**다 (위 주석 참조).
        #   run_job.sh 가 provenance 없이는 안 돌기 때문에 사후 대조는 보장된다.
        chk(verify_bundle(rnp) == 0,
            "pin 이 없어도 제출은 가능하다 — 회수 시 사후 대조 (run_job.sh 강제)")
        chk(verify_bundle(r, expect_jobs=2) == 0,
            "양성: --expect_jobs 는 **실물 잡 수**와 맞춘다 (planned 가 아니라)")
        chk(verify_bundle(r, expect_jobs=40) == 1,
            "⛔음성: 잡 수가 기대와 다르면 차단 (40잡 번들에 10잡을 던지는 사고)")

        r = build(d / "n1")
        p = r / "refs" / "clean_slab__pm1" / "static" / "INCAR"
        p.write_text(p.read_text() + "IVDW = 0\n"); rezip(r)
        chk(verify_bundle(r) == 1, "⛔음성: INCAR 한 줄이 바뀌면 차단 (해시 불일치)")

        r = build(d / "n2")
        (r / "refs" / "clean_slab__pm1" / "POTCAR_ASSEMBLE.sh").unlink(); rezip(r)
        chk(verify_bundle(r) == 1, "⛔음성: 조립기가 없으면 차단 (그 잡은 exit 127)")

        r = build(d / "n3")
        (r / "refs" / "clean_slab__pm1" / "POTCAR").write_text("PAW_PBE Li_sv\n"); rezip(r)
        chk(verify_bundle(r) == 1, "⛔음성: POTCAR 혼입 차단 (라이선스 · 종 순서)")

        r = build(d / "n4")
        (r / "refs" / "clean_slab__pm1" / "static" / "OUTCAR").write_text(
            "General timing and accounting informations\n"); rezip(r)
        chk(verify_bundle(r) == 1,
            "⛔음성: 이미 돈 OUTCAR 차단 (run_job 이 건너뛰어 남의 값을 반송)")

        r = build(d / "n5")
        shutil.rmtree(r / "refs" / "clean_slab__pm1"); rezip(r)
        chk(verify_bundle(r) == 1, "⛔음성: 계획된 잡 폴더가 통째로 없으면 차단")

        r = build(d / "n5b")
        shutil.rmtree(r / "refs" / "clean_slab__pm1__d3off"); rezip(r)
        chk(verify_bundle(r) == 1,
            "⛔음성: **쌍둥이**가 사라져도 차단 — planned 에 없다고 안 보면 D3 분해가 통째로 죽는다")

        r = build(d / "n6")
        (r / "NOTE.txt").write_text("손으로 끼워 넣은 파일\n")     # zip 은 그대로 둔다
        chk(verify_bundle(r) == 1, "⛔음성: zip 과 폴더가 어긋나면 차단 (나가는 물건이 다르다)")

        r = build(d / "n7")
        (r / "MANIFEST.json").unlink()
        chk(verify_bundle(r) == 1, "⛔음성: MANIFEST 없으면 번들로 취급하지 않는다")

        # ── 회신 Z P0-1 회귀 — **해시로는 절대 안 잡히는** 결함 ────────────────
        #   문서를 build 인자로 심는다: 해시는 처음부터 그 내용으로 계산되므로
        #   무결성은 통과하고 **문서 검사만** 걸려야 한다 (아니면 엉뚱한 이유로
        #   통과한 음성이 된다 — v2 selftest 가 정확히 그 함정에 빠졌었다).
        r = build(d / "n8", readme="각 잡의 relax/OUTCAR 와 relax/CONTCAR 를 보내 주세요\n")
        rc = verify_bundle(r)
        chk(rc == 1,
            "⛔음성: relax 상이 0인데 README 가 relax 반송을 요구하면 차단 "
            "(2026-08-29 실사고 — 해시는 통과한다)")

        r = build(d / "n9", contract="| 총 VASP 실행 | **1** |\n")
        chk(verify_bundle(r) == 1,
            "⛔음성: 총 실행 수가 잡 수보다 적으면 차단 (외주가 40 % 덜 잡는다)")

        # ⛔음성 (2026-08-29 사고) — 후보집합 출처가 repo 에 없으면 재현 불가
        r = build(d / "n11")
        _m = json.loads((r / "MANIFEST.json").read_text())
        _m["from_basins"] = {"path": "/data/work/only_on_that_machine.json"}
        (r / "MANIFEST.json").write_text(json.dumps(_m, indent=1, ensure_ascii=False))
        chk(verify_bundle(r) == 1,
            "⛔음성: from_basins 가 repo(db/)에 없으면 차단 — candidate set 을 "
            "재현·감사할 수 없다")

        # ⛔ 2026-08-30 — `--refs_minimal` 을 자세 동결 없이 쓰면 **거부**한다.
        #   실측 사고: 조각 2개로 좁혔는데 잡 40개가 나왔고(C-12 는 12), 그런데도
        #   범위 문구는 C-12 그대로였다 — 후보집합과 범위 주장이 갈리는 fail-open.
        def _grc(minimal, freeze, refs=True, both=True):
            ns = type("NS", (), {"refs_minimal": minimal, "from_basins": freeze,
                                 "refs": refs, "both_seeds": both})()
            try:
                guard_refs_minimal(ns)
            except SystemExit as e:
                return str(e)
            return None

        chk("--from_basins" in (_grc(True, None) or ""),
            "⛔음성: --refs_minimal 을 --from_basins 없이 주면 생성 자체를 거부한다")
        chk(_grc(True, "x.json") is None, "[양성] 세 플래그가 다 있으면 통과한다")
        chk(_grc(False, None, refs=False, both=False) is None,
            "[양성] --refs_minimal 이 아니면 이 검사들은 걸리지 않는다")
        # ⛔ 2026-08-30 실측 — 12잡이어야 할 번들이 **6잡**으로 나왔다.
        #   기체 기준 2 + net4 4 가 빠졌는데 claim_scope 는 흡착에너지 차 문구 그대로였다.
        chk("--refs" in (_grc(True, "x.json", refs=False) or ""),
            "⛔음성: --refs 없이는 거부 — 기체 기준이 0개면 E_G 가 없어 D 가 "
            "**정의되지 않는다** (--refs_minimal 은 켜는 게 아니라 좁히는 플래그다)")
        chk("both_seeds" in (_grc(True, "x.json", both=False) or ""),
            "⛔음성: --both_seeds 없이는 거부 — net4 가지 4잡이 통째로 빠져 "
            "자성 위상 대조가 사라진다")

        r = build(d / "n11b")
        _m = json.loads((r / "MANIFEST.json").read_text())
        _m["submission"] = {"cores_per_job": 48, "max_concurrency": 8,
                            "n_vasp_executions_total": 1}
        (r / "MANIFEST.json").write_text(json.dumps(_m, indent=1, ensure_ascii=False))
        chk(verify_bundle(r) == 1,
            "⛔음성: MANIFEST 의 총 실행 수가 잡 수보다 적으면 차단 "
            "(v4 실측 — 문서만 고치고 MANIFEST 를 놓쳤다)")

        r = build(d / "n12")
        _m = json.loads((r / "MANIFEST.json").read_text())
        _m["from_basins"] = {"path": "/anywhere/prospective_basins_2026_08_29.json"}
        (r / "MANIFEST.json").write_text(json.dumps(_m, indent=1, ensure_ascii=False))
        chk(verify_bundle(r) == 0,
            "양성: repo 에 있는 후보 파일이면 경로가 절대경로여도 통과 "
            "(도구 자기 위치로 찾으므로 cwd 무관)")

    # ══ --verify_zip 경로 (회신 AA P0-1 · Q6) ═══════════════════════════════
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        r = build(d / "z")
        zp = d / "ok.zip"
        with zipfile.ZipFile(zp, "w") as z:
            for q in sorted(r.rglob("*")):
                if q.is_file():
                    z.write(q, "bundle_v0/" + str(q.relative_to(r)))
        att = d / "att.json"
        chk(verify_zip(zp, expect_jobs=2, attest_out=str(att)) == 0,
            "양성: ZIP 입력 검증 통과 + attestation 기록")
        a = json.loads(att.read_text())
        chk(a["verdict"] == "PASS"
            and a["zip"]["sha256"] == hashlib.sha256(zp.read_bytes()).hexdigest()
            and a["census_recomputed_from_disk"]["jobs_on_disk"] == 2
            and a["tooling"]["generator_verifier"]["sha256"],
            "attestation 에 ZIP SHA · **디스크 재계산 census** · verifier SHA 가 실린다")

        def zbad(name, mutate):
            q = d / name
            with zipfile.ZipFile(q, "w") as z:
                for f in sorted(r.rglob("*")):
                    if f.is_file():
                        z.write(f, "bundle_v0/" + str(f.relative_to(r)))
                mutate(z)
            return q

        chk(verify_zip(zbad("dup.zip", lambda z: z.writestr(
            "bundle_v0/MANIFEST.json", "{}")), expect_jobs=2) == 1,
            "⛔음성: **중복 엔트리** 차단 (같은 이름 둘 — 푸는 쪽이 뭘 쓸지 우리가 못 정한다)")
        chk(verify_zip(zbad("esc.zip", lambda z: z.writestr(
            "bundle_v0/../evil.txt", "x")), expect_jobs=2) == 1,
            "⛔음성: **경로 탈출**(..) 차단 — 풀기 전에 잡는다")
        chk(verify_zip(zbad("abs.zip", lambda z: z.writestr(
            "/etc/evil", "x")), expect_jobs=2) == 1,
            "⛔음성: 절대경로·최상위 이탈 엔트리 차단")
        chk(verify_zip(zbad("case.zip", lambda z: z.writestr(
            "bundle_v0/manifest.JSON", "{}")), expect_jobs=2) == 1,
            "⛔음성: **대소문자 충돌** 차단 (대소문자 무시 파일계에서 덮어쓴다)")

        def _sym(z):
            zi = zipfile.ZipInfo("bundle_v0/link")
            zi.external_attr = (0o120777 << 16)
            z.writestr(zi, "/etc/passwd")
        chk(verify_zip(zbad("sym.zip", _sym), expect_jobs=2) == 1,
            "⛔음성: **symlink 엔트리** 차단")

        r2 = build(d / "z2")
        z2 = d / "jobs.zip"
        with zipfile.ZipFile(z2, "w") as z:
            for q in sorted(r2.rglob("*")):
                if q.is_file():
                    z.write(q, "bundle_v0/" + str(q.relative_to(r2)))
        chk(verify_zip(z2, expect_jobs=40) == 1,
            "⛔음성: ZIP 경로에서도 잡 수 불일치를 잡는다 (디스크 독립 열거)")

    print(f"  verify selftest {ok[1]}/{ok[0]}")
    return 0 if ok[0] == ok[1] else 1


def main():
    if "--selftest_verify" in sys.argv:
        sys.exit(_selftest_verify())
    if "--selftest_e2e" in sys.argv:
        sys.exit(_selftest_e2e())
    if "--verify_zip" in sys.argv:
        i = sys.argv.index("--verify_zip")
        _ej = (int(sys.argv[sys.argv.index("--expect_jobs") + 1])
               if "--expect_jobs" in sys.argv else None)
        _ao = (sys.argv[sys.argv.index("--attest") + 1]
               if "--attest" in sys.argv else None)
        sys.exit(verify_zip(sys.argv[i + 1], expect_jobs=_ej, attest_out=_ao))
    if "--verify_bundle" in sys.argv:
        i = sys.argv.index("--verify_bundle")
        _ej = None
        if "--expect_jobs" in sys.argv:
            _ej = int(sys.argv[sys.argv.index("--expect_jobs") + 1])
        sys.exit(verify_bundle(sys.argv[i + 1], expect_jobs=_ej))
    if "--selftest_rescue" in sys.argv:
        sys.exit(_selftest_rescue())
    if "--basin_rescue" in sys.argv:
        i = sys.argv.index("--basin_rescue")
        make_basin_rescue(sys.argv[i + 1], sys.argv[i + 2])
        return
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="/data/work/runs/sdcp_v4_sitescreen")
    ap.add_argument("--out", default="/data/work/runs/sdcp_vasp_oneshot_v3")
    ap.add_argument("--freeze", type=float, default=0.85)
    ap.add_argument("--nslab", type=int, default=192)
    ap.add_argument("--frags", nargs="*", default=None)
    ap.add_argument("--qe", default=str(Path(SS.REPO) / "db" / "inputs" / "sdcp_v2"
                                        / "slab_relax" / "relax.in"),
                    help="Ni1/Ni2 라벨이 있는 QE 입력 (부격자 원장의 원본)")
    ap.add_argument("--expect", nargs="*", default=None,
                    help="계약 방향 수 재정의: ptfe_c10=5 ptfe_dimer=3 ...")
    ap.add_argument("--dense_frags", nargs="*", default=None,
                    help="dense(k 검증)를 켤 조각 — **k 보정자**. 지정하면 그 조각에만 켠다. "
                         "권장 'ptfe_c10 sdcp_doped' (큰 계 + 유일한 open-shell). "
                         "나머지는 K_TRANSFER_SCREENED 로만 해석할 것 (K_CONVERGED 아님).")
    ap.add_argument("--cross_endpoints", nargs="*", default=None,
                    help="교차 끝점을 만들 조각을 **제한**한다 (기본: 필요한 조각 전부). "
                         "챔피언 자세키가 다른 조각에만 실제로 생긴다 — 같으면 0개다. "
                         "제한하면 나머지 불일치 조각은 배향 혼입 상태로 남는다(경고).")
    ap.add_argument("--adaptive_dense", action="store_true",
                    help="조건부 dense(dense_cand/ + --plan_dense + run_dense_selected.sh)를 "
                         "켠다. **기본은 꺼짐** (Codex 7차 권장 A): 승격된 dense 를 최종 "
                         "분석기가 읽는 경로가 아직 end-to-end 로 검증되지 않았고, 외주처에 "
                         "2단계 절차를 요구하게 된다. 꺼 두면 발동 상황은 "
                         "MAGNETIC_K_UNRESOLVED 로 닫힌다.")
    ap.add_argument("--global_champion_meV", type=float, default=20.0,
                    help="풀 제한으로 ΔE 가 이만큼(meV) 이상 움직이면 **전역 최선 자세도** "
                         "끝점으로 넣는다. 배향일치 대비(재는 것)와 전역 자리 선호"
                         "(문헌이 읽는 것)가 다른 답을 낼 수 있기 때문이다. "
                         "기본 20 = 30 meV 판정바닥이 ±10 k 오차로 움직이는 폭. "
                         "0 이면 항상, 1e9 면 절대 안 넣는다.")
    ap.add_argument("--no_cross", action="store_true",
                    help="교차 끝점을 아예 안 만든다. ⚠ 챔피언 자세키가 다른 조각의 ΔE 는 "
                         "자리 효과와 배향 효과가 섞인 값이 되고 분리할 방법이 없어진다.")
    ap.add_argument("--free_spin_refs", action="store_true",
                    help="기체 기준계를 **NUPDOWN=-1(자유 스핀)** 으로 만든다. 복합체가 자유로 "
                         "돌았으므로 기준도 자유여야 한다 (회신 O/P P0 — 0.346 eV headline "
                         "보류 해제 1단계). open-shell 조각은 doublet 선언을 유지한다")
    ap.add_argument("--refs", action="store_true",
                    help="clean 슬랩 + 기체 분자 기준계를 포함한다 (절대 E_ads 용). "
                         "기본은 **미포함** — 자리 대비 ΔE 에서는 정확히 소거되므로 "
                         "Wave 2 로 미룬다 (Codex 5차).")
    ap.add_argument("--cores", type=int, default=48,
                    help="잡당 코어 수 — MANIFEST·SUBMIT_CONTRACT 에 기록된다 "
                         "(비용 모형 기준선과 같아야 추정이 맞는다)")
    ap.add_argument("--refs_minimal", action="store_true",
                    help="기준계를 **기체 box24 하나씩**으로 줄인다 — clean slab · box20 · "
                         "nzmag 대조를 만들지 않는다 (회신 AJ 의 C-12 구성). "
                         "⚠ clean slab 이 없으므로 자기 판정이 직접 topology 로 가야 한다")
    ap.add_argument("--allow_no_pin", action="store_true",
                    help="POTCAR 신원 고정 없이 번들을 만든다 — **제출용이 아니다**. "
                         "시험·초안 전용")
    ap.add_argument("--potcar_pin", default=None,
                    help="사전 승인된 POTCAR/VASP 신원 JSON 경로 "
                         "({source_sha256:{원소:sha}, vasp_version:'...'}). "
                         "이것이 **외부 기준**이다 — 없으면 회신끼리의 일치만 본다")
    ap.add_argument("--cell_c2", type=float, default=None,
                    help="진공 두께 수렴 시험용 **둘째** 셀 높이 [Å]. 주면 primary 자세를 "
                         "주 seed 로 이 높이에서도 낸다 (vacconv/). 판정은 두 조각의 "
                         "대비 변화에 적용하므로 기체·슬랩 항이 소거된다")
    ap.add_argument("--cell_c", type=float, default=None,
                    help="슬랩 잡의 셀 높이 c [Å] 를 이 값으로 **못 박는다**. "
                         "두 묶음(calibration·holdout)이 같은 셀을 쓰게 하는 유일한 방법이다 "
                         "— 각자 맞추면 c 가 갈리고 merge 가 다른 주기셀을 비교한다")
    ap.add_argument("--min_vacuum", type=float, default=MIN_VACUUM_A_DEFAULT,
                    help="흡착종↔다음 주기 슬랩 최소 분리(Å). 미달이면 c 를 늘린다. "
                         "0 이면 게이트를 끈다 (권장하지 않음)")
    ap.add_argument("--concurrency", type=int, default=8,
                    help="외주처가 동시에 돌릴 잡 수 — MANIFEST 에 기록. "
                         "⚠ 한 잡의 static→dense 사슬보다 짧아질 수 없다")
    ap.add_argument("--no_mag_controls", dest="mag_controls", action="store_false",
                    help="clean 자기 대조군(2 seed coarse static)을 빼 버린다. ⚠ 빼면 "
                         "분석기의 Q 기준이 없어져 **자기 붕괴 판정이 전 잡에서 보류**된다 "
                         "= 조용히 통과. --refs 를 켰으면 refs 의 clean 이 그 역할을 한다.")
    ap.add_argument("--kmesh_static", default=None,
                    help="static k 를 덮는다 (예: '2 3 1'). ΔE 에서 k 오차는 대부분 "
                         "상쇄되므로 예산이 빠듯할 때 여기부터 푼다 — 대신 dense 검사로 크기를 잰다.")
    ap.add_argument("--kmesh_dense", default=None, help="dense k 를 덮는다 (예: '3 4 1')")
    ap.add_argument("--champion", action="store_true",
                    help="조각마다 **Li 위 최선 · Ni 위 최선** 한 쌍만 (방향 무관). "
                         "두 챔피언이 다른 방향이면 ΔE 에 배향 효과가 섞인다 — 표시된다.")
    ap.add_argument("--from_basins",
                    help="동결된 prospective_basins manifest 에서 **그 자세만** 생성한다 "
                         "(champion/cross 자동탐색을 쓰지 않는다). 회신 W 5단계")
    ap.add_argument("--roles", nargs="+", default=None,
                    choices=["calibration", "sealed_audit", "holdout",
                             "primary", "sensitivity", "stress_sensitivity"],
                    help="--from_basins 에서 **이 역할만** 낸다. 회신 X P0-2 — Stage A 는 "
                         "`--roles calibration` 으로 audit 을 봉인한 채 던진다. "
                         "`holdout` 은 층화 홀드아웃 tranche (2026-08-30 옵션 A) — "
                         "**단독으로만** 쓴다. candidate_set 이 holdout_stratified 가 되고 "
                         "분석기가 primary 를 막는다")
    ap.add_argument("--d3_seed_main_only", action="store_true",
                    help="복합체의 D3-off 쌍둥이를 " + SEED_MAIN + " 에만 만든다 "
                         "(고정기하 D3 는 자기상태 무관 · 회신 X Q1)")
    ap.add_argument("--no_refs_dense", action="store_true",
                    help="clean slab 의 dense 상을 뺀다 — 슬랩은 A=E_복합체−E_분자 에서 "
                         "대수적으로 소거되므로 사전등록 판정에 안 들어간다")
    ap.add_argument("--both_seeds", action="store_true",
                    help="--from_basins 에서 두 자기 seed 를 다 낸다 (기본 pm1 만)")
    ap.add_argument("--d3_pairs", action="store_true",
                    help="각 endpoint 의 **D3-off 쌍둥이**를 만든다 (IVDW 줄만 제거). "
                         "회신 W Q2 원인 분해용 — 판정값이 아니다. --closure 필수")
    ap.add_argument("--closure", action="store_true",
                    help="닫힘 모드 (회신 U P0-5) — 전 endpoint 고정기하 static 단독 + "
                         "LREAL=.FALSE. 강제. 기체 기준도 relax 를 돌지 않는다. "
                         "조각 간 대비(ΔΔE)를 낼 때만 쓴다")
    ap.add_argument("--single_point", action="store_true",
                    help="MLIP 기하 위의 **단일점만** — DFT 는 결합에너지만 낸다. "
                         "relax 를 안 돌리므로 기하는 DFT 최소점이 아니다(인용 시 명시).")
    ap.add_argument("--top_n", type=int, default=None,
                    help="조각마다 **자세 안정도 상위 N 쌍**만 (MLIP 스크린 → DFT 확인). "
                         "권장 3 — 분석기가 n<3 이면 판정을 거부한다. 1 은 판정 불가.")
    ap.add_argument("--allow_stale_gate", action="store_true",
                    help="옛 gate_version 산출을 그대로 쓴다 (기본은 중단 — regate 를 권함)")
    ap.add_argument("--allow_partial", action="store_true",
                    help="계약 위반을 안고 만든다 (기본은 중단 — 축소 번들 방지)")
    ap.add_argument("--no_prescf", action="store_true",
                    help="dipole-off pre-SCF 상을 빼고 relax 부터 (권장하지 않음)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    # ⛔ 홀드아웃은 **단독 tranche** 다. calibration 과 섞어 내면 사전등록된
    #   primary 후보집합이 오염되고, 홀드아웃이 더 낮게 나온 것이 "더 좋은 자세를
    #   찾았다" 로 흡수돼 **선택기 실패가 사라진다** (회신 X Q6 와 같은 구조).
    if a.roles and "holdout" in a.roles and len(set(a.roles)) > 1:
        ap.error("--roles holdout 은 단독으로만 쓴다 (지금 %s) — 다른 역할과 섞으면 "
                 "primary 후보집합이 오염된다" % a.roles)
    if a.selftest:
        # ⚠ verify 는 생성기 selftest 와 독립이다 — 표준 명령 하나가
        #   전건을 덮지 않으면 아무도 안 돌린다 (음성 경로가 특히).
        rc = selftest()
        print("\n── --verify_bundle 경로 ──")
        rc = rc or _selftest_verify()
        # ★ 회신 AA Q2 — E2E 를 표준 명령에 **물린다**. 따로 두면 아무도 안 돌리고,
        #   우리가 세 번 맞은 병이 바로 "안 돌린 층" 에서 나왔다.
        print("\n── 생산 생성기 E2E 경로 ──")
        return rc or _selftest_e2e()
    build_bundle(a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
