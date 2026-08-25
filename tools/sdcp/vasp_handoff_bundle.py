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
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import site_screen as SS                      # noqa: E402  (게이트·POSCAR·조각 레지스트리)

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
              "LDAUTYPE", "LDAUL", "LDAUU", "LDAUJ")


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
need() { [ -s "$1" ] || { echo "⛔ $1 없음/빈 파일 — $2"; exit 1; }; }
for ph in pre relax static dense; do
  [ -d "$ph" ] || continue
  if [ -f "$ph/OUTCAR" ] && grep -aq "General timing" "$ph/OUTCAR"; then
    echo "  ✓ $ph 이미 완료 — 건너뜀"; continue
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

RUN_ALL = """#!/usr/bin/env bash
# ⚠⚠ 이건 **직렬 디버그 러너**다 — 병렬 제출기가 아니다.
#   이대로 돌리면 잡을 하나씩 순서대로 돈다 (Wave 1 기준 20일 규모).
#   실제 제출은 SUBMIT_CONTRACT.md 의 배열 잡/스케줄러로 할 것.
#   여기서는 계약(상 의존성·종료코드 전파)을 보여 주고, 소수 잡을 손으로 돌릴 때 쓴다.
# 전체 실행 순서: controls → tier1 → refs → tier2.  VASP_CMD 로 실행 명령 지정.
set -u
fail=0
for grp in controls tier1 refs tier2; do
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


def _write_potcar_asm(jd: Path, species_order: List[str]) -> None:
    """그 잡 전용 POTCAR 조립기. **슬랩·기체 공통**이다.

    ⚠ 처음엔 슬랩에만 넣었다. 기체 8잡에는 없어서 제출 본문(`bash POTCAR_ASSEMBLE.sh`)
      이 exit 127 로 죽었고, E_ads 를 하나도 못 만드는 상태였다 (Codex 4차 감사 P0-1).
      잡을 만드는 자리가 두 곳이면 배포물도 두 곳에서 만들어야 한다 — 한 함수로 뺀다.
    """
    pv = [POTCAR_SPEC.get(e, e) for e in species_order]
    (jd / "POTCAR_ASSEMBLE.sh").write_text(
        "#!/usr/bin/env bash\n"
        "# 이 잡의 POTCAR 를 만든다. PBE PAW 5.4 세트 경로를 PP 로 준다.\n"
        "#   PP=/path/to/potpaw_PBE.54 bash POTCAR_ASSEMBLE.sh\n"
        "# ⚠ 종 순서는 이 잡 POSCAR 전용이다 — 다른 잡에 복사하지 말 것.\n"
        "set -e\n"
        f'ORDER="{" ".join(pv)}"\n'
        ': "${PP:?PP 를 지정하세요 (PBE PAW 5.4 세트 루트)}"\n'
        'rm -f POTCAR\n'
        'for v in $ORDER; do\n'
        '  f="$PP/$v/POTCAR"\n'
        '  [ -f "$f" ] || { echo "⛔ 없음: $f"; exit 1; }\n'
        '  cat "$f" >> POTCAR\n'
        'done\n'
        'n=$(grep -ac TITEL POTCAR)\n'
        f'[ "$n" = {len(pv)} ] || {{ echo "⛔ TITEL {len(pv)}개여야 하는데 $n개"; exit 1; }}\n'
        'grep -a TITEL POTCAR\n'
        f'echo "✔ 조립 완료 — 종 순서 {" ".join(species_order)}"\n')


def _emit_slab_job(jd: Path, atoms, nslab: int, freeze: float, frag: str,
                   system: str, seed_name: str, extra_meta: Dict[str, Any],
                   ledger: Dict[str, Any], zcut=None, dense: bool = False,
                   prescf: bool = True, single_point: bool = False,
                   kmesh_over: Optional[Dict[str, str]] = None,
                   dense_cand: bool = False) -> Dict[str, Any]:
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
    if single_point:
        # MLIP 로 기하를 닫고 DFT 는 결합에너지만.
        # ⚠ dense 는 static 의 CHGCAR 를 승계해야 하므로 ICHARG=1 이어야 한다.
        #   같은 SLAB_SP(ICHARG=2)를 재사용하면 복사한 CHGCAR 를 **안 쓴다**.
        tpls = {"static": SLAB_SP,
                "dense": SLAB_SP.replace("ICHARG   = 2", "ICHARG   = 1")
                                .replace("[static · single-point]", "[dense · single-point]")}
    if not prescf:
        # ⚠ pre 를 빼면 relax 의 ISTART=1 이 읽을 WAVECAR 가 없다. VASP 는 조용히
        #   처음부터 시작하므로 "승계했다" 는 기록만 남고 실제로는 안 한 게 된다.
        tpls["relax"] = SLAB_RELAX.replace("ISTART   = 1", "ISTART   = 0") \
                                  .replace("ICHARG   = 0", "ICHARG   = 2")
    phases = (["static"] if single_point
              else (["pre"] if prescf else []) + ["relax", "static"]) \
        + (["dense"] if dense else [])
    kmesh, incar_exp = {}, {}
    for ph in phases:
        (jd / ph).mkdir(exist_ok=True)
        txt = tpls[ph].format(**fmt)
        (jd / ph / "INCAR").write_text(txt)
        km = KMESH["relax"] if ph == "pre" else kmesh_over.get(ph, KMESH[ph])
        (jd / ph / "KPOINTS").write_text(f"auto\n0\nGamma\n{km}\n0 0 0\n")
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
        (jd / "dense_cand" / "KPOINTS").write_text(f"auto\n0\nGamma\n{km}\n0 0 0\n")
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


def _emit_mol_job(jd: Path, frag: str, mol, margin: float) -> Dict[str, Any]:
    """기체상 기준계 v3 — 상자 span+margin, IDIPOL=4+DIPOL(COM), NUPDOWN, 2상."""
    from ase import Atoms
    jd.mkdir(parents=True, exist_ok=True)
    p = mol.get_positions()
    p = p - p.min(axis=0)
    box = p.max(axis=0) + margin
    at = Atoms(symbols=mol.get_chemical_symbols(), positions=p + margin / 2.0,
               cell=np.diag(box), pbc=True)
    open_shell = "DOUBLET" in str(SS.FRAGMENTS.get(frag, {}).get("electrons", "")).upper()
    mags = [0.0] * len(at)
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
           "nupdown": 1 if open_shell else 0,
           "magmom": " ".join(f"{mags[i]:.3f}" for i in idx)}
    kmesh, incar_exp = {}, {}
    for ph, tpl in (("relax", MOL_RELAX), ("static", MOL_STATIC)):
        (jd / ph).mkdir(exist_ok=True)
        txt = tpl.format(**fmt)
        (jd / ph / "INCAR").write_text(txt)
        (jd / ph / "KPOINTS").write_text("gamma-only\n0\nGamma\n1 1 1\n0 0 0\n")
        kmesh[ph] = "1 1 1"
        incar_exp[ph] = {k: m.group(1) for k in AUDIT_KEYS
                         for m in [re.search(rf"^{k}\s*=\s*(\S+)", txt, re.M)] if m}
    _write_potcar_asm(jd, seen)
    (jd / "run_job.sh").write_text(RUN_JOB)
    meta = {"kind": "mol_ref", "fragment": frag, "species_order": seen, "counts": counts,
            "kmesh": kmesh, "incar_expected": incar_exp,
            "open_shell": open_shell, "box_margin_A": margin, "phases": ["relax", "static"],
            "box_A": [round(float(b), 2) for b in box],
            # ⚠ 기체 기준계도 결합 그래프를 감사해야 한다 — 없으면 그 검사가 꺼진다
            #   (Codex P0-G). 슬랩이 없으므로 registry/탈착 검사는 분석기가 건너뛴다.
            "mol_poscar_idx": list(range(len(at))),
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
import gzip, hashlib, json, math, os, re, sys
from glob import glob

DELTA = 0.030
SEED_TOL = 0.010          # eV — seed-매칭 ΔE 게이트
BOX_TOL = 0.010           # eV — 기체상 상자 수렴
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
                      "ISPIN", "LDAUL", "LDAUJ", "MAGMOM")

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
                    return gzip.open(path, "rt", errors="ignore").read()
            return open(path, errors="ignore").read()
        if os.path.isfile(path + ".gz"):
            return gzip.open(path + ".gz", "rt", errors="ignore").read()
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
        except (OSError, EOFError, gzip.BadGzipFile) as e:
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
                "nelm_hit": False, "ionic_conv": False, "nions": None, "nkpts": None,
                "titels": [], "incar_echo": {}, "moments": None, "mag_total": None,
                "run_segments": None}
    if t is None:
        return None
    t, seg = _last_run_segment(t)
    e = re.findall(r"energy\(sigma->0\)\s*=\s*(-?[\d.]+)", t)
    nions = re.search(r"NIONS\s*=\s*(\d+)", t)
    nk = re.search(r"NKPTS\s*=\s*(\d+)", t)
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
    return {"E0": float(e[-1]) if e else None,
            "ionic_conv": "reached required accuracy" in t,
            # ⚠ 정상종료를 안 보면 **잘린 OUTCAR 도 에너지만 있으면 통과**한다
            "normal_end": "General timing and accounting" in t,
            "nelm_hit": bool(nelm and iters
                             and any(int(x) >= int(nelm.group(1)) for x in iters)),
            "nions": int(nions.group(1)) if nions else None,
            "nkpts": int(nk.group(1)) if nk else None,
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
        want = meta.get("role")
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
    with open(op, "w") as fh:
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


def selftest_k() -> int:
    """k 라벨·guard band 의 **순수 산술**을 시험한다 (음성 포함).

    이 시험이 못 하는 것: OUTCAR 회수·게이트 연동. 그건 번들 selftest 몫이다.
    """
    ok = True

    def chk(c, m):
        nonlocal ok
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
    print("k-selftest PASS" if ok else "k-selftest FAIL")
    return 0 if ok else 1


def phase_gates(oc, ph, meta, spec, want_ionic=False):
    """상 하나의 fail-closed 검사. oc 가 None 이면 NOT_RUN.

    ⚠ **게이트 통과가 보증하는 것** (codex E-2, 과대해석 금지):
      "제공된 단일 완결 실행 세그먼트에서, incar_expected 에 등록된 유한한 키
       집합이 되울림과 일치했다" — 딱 여기까지다.
    보증하지 못하는 것: 등록되지 않은 키 전부 · 정확한 k-grid shift · POTCAR 원문
    해시 · WAVECAR/CHGCAR 실제 내용과 승계 계보 · 기본값/명시값 구분 · LREAL 의
    정확한 모드(등가류까지만). ISTART/ICHARG 되울림은 재시작 파일이 **실제로
    쓰였다는 증거가 아니다.** 각 상의 incar_audit(4분류)가 이 경계의 기계 기록이다.
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
    return g


def main():
    if "--selftest" in sys.argv:
        return selftest_k()
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    delta = DELTA
    if "--delta" in sys.argv:
        delta = float(sys.argv[sys.argv.index("--delta") + 1])
    man = json.load(open(os.path.join(root, "MANIFEST.json")))
    spec = man.get("potcar_spec", {})
    planned = man.get("planned", {})

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
    integrity["runtime_poscar_mismatch"] = []
    for jd in sorted(glob(os.path.join(root, "*", "*", ""))):
        rp = os.path.join(jd, "POSCAR")
        if not os.path.isfile(rp):
            continue
        rh = hashlib.sha256(open(rp, "rb").read()).hexdigest()
        for ph in ("static", "dense"):
            pp = os.path.join(jd, ph, "POSCAR")
            if not os.path.isfile(pp):
                continue
            if os.path.isdir(os.path.join(jd, "relax")):
                continue          # 이완판은 CONTCAR 승계가 정상 — 달라야 맞다
            if hashlib.sha256(open(pp, "rb").read()).hexdigest() != rh:
                integrity["runtime_poscar_mismatch"].append(
                    _pk(pp, root))
    # ★ phase POSCAR 를 반송받지 못하면 위 검사는 **조용히 건너뛴다** = fail-open.
    #   OUTCAR 가 있는데 POSCAR 가 없으면 OUTCAR 좌표로 대조한다 (Codex P0-6).
    integrity["geometry_unverified"] = []
    for jd in sorted(glob(os.path.join(root, "*", "*", ""))):
        rp = os.path.join(jd, "POSCAR")
        if not os.path.isfile(rp) or os.path.isdir(os.path.join(jd, "relax")):
            continue
        want = read_poscar(rp)
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
    for jd in sorted(glob(os.path.join(root, "*", "*", ""))):
        jp = os.path.join(jd, "job.json")
        if not os.path.isfile(jp):
            continue
        meta = json.load(open(jp))
        rel = _pk(jd, root)
        phases = (planned.get(rel) or {}).get("phases") or meta.get("phases") or \
            ["relax", "static"]
        ocs = {ph: read_outcar(os.path.join(jd, ph, "OUTCAR")) for ph in phases}
        rec = {"meta": meta, "static": ocs.get("static"), "dense": ocs.get("dense"),
               "gates": []}
        for ph in phases:
            rec["gates"] += phase_gates(ocs[ph], ph, meta, spec,
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
                    "flip_indices_poscar": sorted(flip),
                    "flip_moments_muB": {str(i): round(got[i], 3) for i in flip},
                    "n_small": len(small), "min_abs_muB": round(min(map(abs, got.values())), 3),
                    "abs_mean_muB": round(sum(map(abs, got.values())) / len(got), 3),
                    "total_muB": st.get("mag_total")}
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
    q_by_seed: Dict[str, Optional[float]] = {}
    ref_bad: Dict[str, str] = {}
    for sd in (man.get("seeds_full") or ["afm2424_pm1", "afm2424_net4"]):
        cj = [(j, r) for j, r in jobs.items() if "clean_slab" in j and j.endswith(sd)]
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
            mg["verdict"] = "clean 기준 없음/무효 — 자기 붕괴 판정 보류"
            if "clean_slab" not in j:
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
               "numerical_gates": {}, "warnings": [], "integrity": integrity,
               # incar_audit (codex E-2) — 게이트 통과가 **무엇까지 보증하는지**의
               #   기계 기록: verified_exact / verified_equivalence_class /
               #   unverified / mismatch + 실행 세그먼트 정보. 사람용 요약(README)과
               #   어긋나면 이쪽이 정본이다.
               "jobs": {j: {"ok": r["ok"], "gates": r["gates"],
                            "E0_static": (r["static"] or {}).get("E0"),
                            "vasp_version": (r["static"] or {}).get("vasp_version"),
                            "incar_audit": {ph: (r.get(ph) or {}).get("incar_audit")
                                            for ph in ("static", "dense")
                                            if (r.get(ph) or {}).get("incar_audit")},
                            "run_segments": {ph: (r.get(ph) or {}).get("run_segments")
                                             for ph in ("static", "dense")
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
    has_refs = bool(man.get("refs", {}).get("clean_slab"))
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
        ok = e20 is not None and e24 is not None and abs(e20 - e24) <= BOX_TOL
        mol_ok[f] = ok
        emol[f] = e24 if ok else None          # 실패하면 E_ads 를 만들지 않는다
        if e20 is not None and e24 is not None:
            d = abs(e20 - e24)
            results["numerical_gates"][f"box_{f}"] = {
                "dE_meV": round(d * 1000, 1), "pass": d <= BOX_TOL}
            if not ok:
                results["warnings"].append(
                    f"mol__{f}: 상자 20↔24 Å 차 {d * 1000:.1f} meV > 10 — "
                    f"이 조각의 E_ads 를 만들지 않는다")
        else:
            results["numerical_gates"][f"box_{f}"] = {"dE_meV": None, "pass": False}
            results["warnings"].append(f"mol__{f}: 상자 2종 중 하나가 없다 — E_ads 불가")

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
    missing = []
    for j, pl in planned.items():
        if not pl.get("required"):
            continue
        if E(j) is None:
            missing.append(j + " [static]")
        elif "dense" in (pl.get("phases") or []) and E_dense(j) is None:
            missing.append(j + " [dense]")
    out = os.path.join(root, "RESULTS.json")
    results["required_missing"] = missing
    for r in jobs.values():
        r.pop("_fin", None); r.pop("_contact_fp", None)
    json.dump(results, open(out, "w"), indent=1, ensure_ascii=False)

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
        print(f"  {'✓' if v['pass'] else '⛔'} 수치게이트 {k}: {v['dE_meV']} meV"
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
    # ⚠ 기준계를 선언해 놓고 E_ads 가 하나도 안 나오면 **조용한 실패**다.
    #   경로 키가 안 맞아도 gas job 자체는 ok 라 exit 0 이 났다 (Codex 4차 P0-2).
    if has_refs and not results["e_ads"]:
        print("\n⛔ **기준계를 선언했는데 E_ads 가 0개다** — refs 조회가 안 맞거나 "
              "상자 게이트가 전부 실패했다. exit 2")
        for k2, v2 in results["numerical_gates"].items():
            if k2.startswith("box_"):
                print(f"   {k2}: {v2}")
        return 2
    if missing:
        print(f"\n⛔ **필수 산출 미완 {len(missing)}건** (tier1/refs) — fail-closed, exit 2:")
        for j in missing[:20]:
            print(f"   · {j}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


def _readme_sp(man: Dict[str, Any], a, zcut: float, n_jobs: int,
               n_st: int, n_dn: int, n_all: int = 0, by_ph: Optional[dict] = None) -> str:
    """단일점 Wave 1 전용 README — **실제 계획에서 숫자를 뽑는다** (Codex 6차 §8).

    옛 README 를 재사용하면 82계·259상·relax 반송·refs 표가 그대로 나가, 외주처가
    있지도 않은 relax/CONTCAR 를 찾다가 멈춘다. 이 도구가 못 하는 것: 실행 시간 보장
    (SUBMIT_CONTRACT.md 의 추정은 ±2배 불확실성을 가진 모델값이다).
    """
    dc = man.get("dense_calibrators") or []
    mc = man.get("magnetic_controls") or []
    ks = (man.get("kmesh_override") or {}).get("static") or KMESH["static"]
    kd = (man.get("kmesh_override") or {}).get("dense") or KMESH["dense"]
    longest = 56          # h — C10 static→dense 사슬 (비용 모형 중앙 추정, ±2배)
    groups = "` · `".join(sorted({k.split("/")[0] for k in man["planned"]}))
    ph_line = " · ".join(f"{k} {v}" for k, v in sorted((by_ph or {}).items()))
    return f"""# VASP 계산 요청 — LiNiO₂(104) 위 분자 조각 단일점

바쁘신 중에 부탁드려 죄송합니다. **VASP 실행 {n_all or (n_st + n_dn)}회**입니다
({ph_line}).
슬랩 쪽은 구조 최적화를 저희가 MLIP 으로 끝내서 단일점만 돌리면 되고,
기체 분자 기준계만 DFT 이완이 필요합니다 (잡당 몇 분).

## 하실 일

```
cd <잡폴더>
PP=/path/to/potpaw_PBE.54 bash POTCAR_ASSEMBLE.sh     # 그 잡 전용 POTCAR 조립
VASP_CMD="mpirun -np {a.cores} vasp_std" bash run_job.sh
```

잡 폴더 {n_jobs}개가 `{groups}` 에 있습니다.
서로 **완전히 독립**이라 원하시는 만큼 동시에 돌리셔도 됩니다.

## 미리 아셔야 할 것 두 가지

- **가장 긴 잡이 약 {longest} 시간**입니다 (48코어 기준 추정, ±2배). walltime 상한이
  이보다 짧으면 그 잡만 알려 주세요 — 저희가 나눠서 다시 만들어 드리겠습니다.
- **POTCAR 는 잡마다 종 순서가 다릅니다.** 위 `POTCAR_ASSEMBLE.sh` 가 그 잡에 맞게
  만들고 검증까지 합니다. 하나를 만들어 전체에 복사하시면 틀립니다.

## 보내 주실 것

각 잡의 **`static/OUTCAR`** (있는 잡은 `dense/OUTCAR` 도). `.gz` 그대로 좋습니다.

⚠ **`refs/mol__*` 잡만은 `relax/OUTCAR` 와 `relax/CONTCAR` 도 함께** 보내 주세요.
   분자가 이완 중에 깨지지 않았는지 좌표로 확인합니다. 이게 없으면 그 조각의
   결합에너지를 못 만듭니다.

슬랩 잡의 `CONTCAR`·`CHGCAR`·`WAVECAR` 는 필요 없습니다.

## 부탁

`INCAR`·`KPOINTS`·`POSCAR` 를 **한 글자도 고치지 말아 주세요.** 분석기가 sha256 으로
대조해서, 병렬 태그 한 줄만 바꿔도 전체를 거부합니다 (NCORE 는 4 로 넣어 두었습니다).
병렬 조정이 꼭 필요하시면 알려 주세요 — 저희가 다시 만들어 드리는 게 빠릅니다.

SCF 가 안 붙는 잡이 있으면 **그대로 두고 알려만 주세요.** 설정을 바꿔 다시 돌리시는
것보다, 저희가 그 잡만 새로 만들어 드리는 편이 확실합니다 (바뀐 입력은 저희 쪽
검증을 통과하지 못합니다).

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
Ni 는 **Ni_pv** (2026-08-08 납품과 동일 계보) · VASP 5.4.4 또는 6.x + PBE PAW 5.4.
dense 는 k 검증용이라 {n_dn}개 잡에만 있습니다: {dc or '(없음)'}.
</details>
"""


def _submit_contract(man: Dict[str, Any], a) -> str:
    """제출 계약 — 병렬도·의존성·비용 추정의 **출처**를 못 박는다 (Codex 6차 §7).

    이 파일이 없으면 "2.4일" 이 어떤 병렬도의 산술 하한인지 아무도 모른다.
    이 도구가 못 하는 것: 실제 대기열 지연·노드 성능 차이 반영.
    """
    n_st = sum(1 for p in man["planned"].values()
               if "static" in (p.get("phases") or []))
    n_dn = sum(1 for p in man["planned"].values()
               if "dense" in (p.get("phases") or []))
    # ⚠ 기체 기준계는 relax 상이 있다 — static+dense 만 세면 실제보다 적다
    by = {}
    for _p in man["planned"].values():
        for _ph in (_p.get("phases") or []):
            by[_ph] = by.get(_ph, 0) + 1
    n_all = sum(by.values())
    ph_line = " · ".join(f"{k} {v}" for k, v in sorted(by.items()))
    return f"""# 제출 계약 (SUBMIT_CONTRACT)

## 상 의존성
```
static  (독립 — 잡끼리 완전 병렬)
   └─ dense   (같은 잡의 static/CHGCAR 필요 → **그 잡 안에서는 직렬**)
```
잡 사이에는 의존성이 없습니다. 한 잡의 `run_job.sh` 가 그 잡의 상 순서를 강제합니다.

## 규모
| | |
|---|---:|
| 잡 | {man.get('n_jobs', '?')} |
| static 실행 | {n_st} |
| dense 실행 | {n_dn} |
| 총 VASP 실행 | **{n_all}** |
| 상별 | {ph_line} |

## 병렬 제출 (권장)
`run_all.sh` 는 **직렬 디버그용**입니다. 실제로는 잡 목록을 배열로 던지세요:
```bash
# ⚠ 폴더 이름을 손으로 적지 않는다 — refs/ 냐 controls/ 냐가 모드에 따라 다르다.
#   2026-08-12: controls/ 로 적어 두는 바람에 기준계 10잡이 통째로 빠질 뻔했다.
find . -mindepth 2 -maxdepth 2 -type d -name '*__*' -o \
     -mindepth 2 -maxdepth 2 -type d -path './refs/*' | sed 's|^\./||' | sort > JOBS.txt
n=$(wc -l < JOBS.txt)
[ "$n" = {man.get("n_jobs", 0)} ] || {{ echo "⛔ 잡 {man.get("n_jobs", 0)}개여야 하는데 $n 개"; exit 1; }}
# Slurm 예시 — 동시 8개
sbatch --array=1-$(wc -l < JOBS.txt)%{a.concurrency} \
  --ntasks={a.cores} --time=120:00:00 --wrap='
  j=$(sed -n "${{SLURM_ARRAY_TASK_ID}}p" JOBS.txt)
  cd "$j"
  PP=/path/to/potpaw_PBE.54 bash POTCAR_ASSEMBLE.sh    # ★ 잡마다 종 순서가 다르다
  VASP_CMD="srun -n {a.cores} vasp_std" bash run_job.sh'
```
⚠ **공통 POTCAR 를 전 잡에 복사하면 안 됩니다.** 조각마다 POSCAR 종 순서가 달라
(`Li Ni O` · `Li Ni O C F` · `Li Ni O C F H` · `Li Ni O S C H`) 하나를 돌려 쓰면
그 잡은 조용히 **다른 계**를 계산합니다. `POTCAR_ASSEMBLE.sh` 가 잡마다 조립하고
TITEL 수까지 검증합니다.
⚠ walltime — 가장 긴 잡이 중앙 추정 56 h 이고 모형 불확실성이 ±2배입니다.
   ±2배 외피가 112 h 이므로 **120 h** 를 권합니다 (24–48 h 면 그 잡이 잘립니다).

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
- **INCAR 수정 금지.** 예외 ①: NCORE/KPAR/NSIM 등 병렬 자유.
  예외 ② — SCF 가 안 붙을 때만, 순서대로: 1) `ALGO = All`
  2) `AMIX=0.1 · BMIX=0.0001 · AMIX_MAG=0.2 · BMIX_MAG=0.0001` — 쓴 것을 그 잡의
  `NOTES.txt` 에 남기고, 그래도 안 되면 그 잡은 중단 후 알려 주세요.
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
  바뀐 파일을 잡아냅니다 (병렬 태그 NCORE/KPAR/NSIM 은 예외 — 고쳤으면 알려 주세요).

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
    cps = sorted(Path(a.runs).glob(f"*/relax_f{a.freeze:.2f}/_clean_slab.vasp"))
    if not cps:
        sys.exit(f"⛔ {a.runs}/*/relax_f{a.freeze:.2f}/_clean_slab.vasp 이 하나도 없다 — "
                 f"raw 슬랩으로 조용히 대체하지 않는다 (E_ads 기준계가 달라진다)")
    hashes = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in cps}
    if len(set(hashes.values())) != 1:
        sys.exit("⛔ 조각별 clean slab 이 서로 다르다 — E_ads 기준계가 갈린다:\n  "
                 + "\n  ".join(f"{h[:12]}  {p}" for p, h in sorted(hashes.items())))
    clean = ase_read(cps[0])
    man["clean_slab"] = {"path": str(cps[0]), "sha256": list(hashes.values())[0],
                         "n_sources_identical": len(cps)}
    _z = clean.positions[:, 2]
    zcut = float(_z.min() + (_z.max() - _z.min()) * a.freeze)
    man["z_cut_shared_A"] = round(zcut, 3)
    slab_metas: List[Dict[str, Any]] = []

    def plan(relpath: str, phases: List[str], required: bool):
        man["planned"][relpath] = {"phases": phases, "required": required}

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

    for tier, frags in TIERS.items():
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
                            {"kind": "pose", "role": role, "pair_id": pid,
                             "fragment": frag, "source_pose": rec["label"],
                             "uma_E_pose_eV": rec["E_pose_eV"]},
                            ledger, zcut=zcut, dense=dense and sd == SEED_MAIN,
                            prescf=not a.no_prescf, single_point=a.single_point,
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
                            "role": role, "source_pose": rec["label"],
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
                                prescf=not a.no_prescf, single_point=a.single_point,
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
                        "role": role, "source_pose": rec["label"],
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
                            prescf=not a.no_prescf, single_point=a.single_point,
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

    if not man["pairs"]:
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
    for sd in (SEEDS_FULL if (a.refs or mag_ctl) else ()):
        rel = (f"refs/clean_slab__{sd}" if a.refs else f"controls/clean_slab__{sd}")
        m = _emit_slab_job(out / rel, clean, len(clean), a.freeze, man["fragments"][0],
                           f"clean slab {sd}", sd,
                           {"kind": "clean_ref" if a.refs else "clean_magnetic_control"},
                           ledger, zcut=zcut, dense=(a.refs and sd == SEED_MAIN),
                           prescf=not a.no_prescf, single_point=a.single_point,
                           kmesh_over=kover)
        slab_metas.append(m)
        plan(rel, m["phases"], True)
        n_jobs += 1
    # ⚠ refs 가 아닌 대조군을 man["refs"] 에 넣으면 has_refs 가 참이 되어 분석기가
    #   E_ads 를 만들려 든다 (기체 분자가 없는데). 별도 키로 등록한다.
    man["refs"]["clean_slab"] = ([f"refs/clean_slab__{s}" for s in SEEDS_FULL]
                                 if a.refs else [])
    man["magnetic_controls"] = ([f"controls/clean_slab__{s}" for s in SEEDS_FULL]
                                if mag_ctl else
                                (man["refs"]["clean_slab"] if a.refs else []))
    man["wave"] = 1 if not a.refs else "1+refs"
    # ★ 조각마다 주장 범위가 다르다 (2026-08-12 설계 변경). 공통 mode 문장 하나로
    #   두면 PTFE 에도 "2×2 완성" 이 적혀 오독된다.
    man["claim_policy"] = {
        f: ({"quantities": ["E_ads", "dE_site"],
             "not_claimed": ["배향 분해(2×2 없음)", "전역 자리 선호"],
             "note": ("cap 인공물이 있는 짧은 모델 — C10 의 대조군으로만, 단독 인용 금지"
                      if f == "ptfe_dimer" else "결합에너지 중심")}
            if f.startswith("ptfe") else
            {"quantities": ["E_ads", "dE_site"]
             + (["2x2 배향 분해"] if any(p.get("cross") for p in man["pairs"].values()
                                       if p["fragment"] == f) else []),
             "not_claimed": (["open-shell 바닥상태 일반화 — 시드 basin 조건부"]
                             if f == "sdcp_doped" else []),
             "note": "자리 선호 중심"})
        for f in man.get("fragments", [])}
    man["claim_scope"] = (
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
        for margin, tag in ((20.0, "box20"), (24.0, "box24")):
            rel = f"refs/mol__{frag}__{tag}"
            m = _emit_mol_job(out / rel, frag, mol, margin)
            plan(rel, m["phases"], True)
            man["refs"][f"mol__{frag}__{tag}"] = rel
            n_jobs += 1

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

    man["potcar_spec"] = {e: POTCAR_SPEC.get(e, e) for e in sorted(used_els)}
    (out / "analyze_results.py").write_text(ANALYZER)
    (out / "run_all.sh").write_text(RUN_ALL)
    if a.adaptive_dense:
        (out / "run_dense_selected.sh").write_text(RUN_DENSE_SEL)
    # ⚠ 문서가 잡 수를 읽으므로 **문서보다 먼저** 확정한다 (Codex 7차 §11 —
    #   지금은 SUBMIT_CONTRACT 가 '?' 를 찍고 있었다).
    man["n_jobs"] = n_jobs
    n_by_ph = {}
    for _p in man["planned"].values():
        for _ph in (_p.get("phases") or []):
            n_by_ph[_ph] = n_by_ph.get(_ph, 0) + 1
    n_ph_all = sum(n_by_ph.values())
    # ★ 모드별 README (Codex 6차 §8) — 옛 README 는 82계·259상·relax 반송·refs 표를
    #   그대로 담고 있어 **단일점 Wave 1 과 정면으로 모순**된다. 실행 계약과 provenance
    #   문서를 옛 판으로 내보내는 것은 문구 문제가 아니라 반송 계약 위반이다.
    if a.single_point:
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
    (out / "SUBMIT_CONTRACT.md").write_text(_submit_contract(man, a))
    (out / "POTCAR_SPEC.txt").write_text(
        "# 원소 → POTCAR 변형 (PBE PAW 5.4). 각 잡 POSCAR 의 종 순서대로 이어붙일 것.\n"
        "# Ni_pv 는 2026-08-08 납품과 동일 계보다 — 바꾸지 말 것.\n"
        + "\n".join(f"{e:3s} {v}" for e, v in man["potcar_spec"].items()) + "\n")

    files = {}
    for p in sorted(out.rglob("*")):
        if p.is_file() and p.name != "MANIFEST.json":
            files[str(p.relative_to(out))] = hashlib.sha256(p.read_bytes()).hexdigest()
    # ── 제출 계약을 MANIFEST 에 못 박는다 (Codex 6차 §7) ─────────────────────
    #   "2.4일" 이 어떤 코어 수·병렬도의 값인지 기록이 없으면 나중에 아무도 모른다.
    n_st = sum(1 for p in man["planned"].values()
               if "static" in (p.get("phases") or []))
    n_dn = sum(1 for p in man["planned"].values()
               if "dense" in (p.get("phases") or []))
    # ⚠ 기체 기준계는 relax 상이 있다. static+dense 만 세면 실제 실행 횟수보다 적다
    #   (2026-08-12: 35 라고 적었는데 실제 43 이었다).
    n_cd = len(list(out.rglob("dense_cand/INCAR")))
    man["submission"] = {
        "cores_per_job": a.cores,
        "max_concurrency": a.concurrency,
        "phase_dependencies": ("잡 사이 의존 없음. 한 잡 안에서 dense 는 static 의 "
                               "CHGCAR 를 승계하므로 **직렬** — 잡 하나가 분할 불가 "
                               "작업 하나다 (P||Cmax)."),
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
        "runner_note": ("run_all.sh 는 **직렬 디버그용**이다. 실제 제출은 "
                        "SUBMIT_CONTRACT.md 의 배열 잡으로."),
    }
    # ── release assertion: 계획된 **모든** 잡에 조립기가 있는가 ─────────────
    #   제출 본문이 30잡 전부에서 POTCAR_ASSEMBLE.sh 를 부른다. 하나라도 없으면
    #   그 잡은 exit 127 로 죽는다 (2026-08-12: 기체 8잡이 그 상태로 나갔다).
    _noasm = [k for k in man["planned"]
              if not (out / k / "POTCAR_ASSEMBLE.sh").is_file()]
    if _noasm:
        sys.exit(f"⛔ POTCAR 조립기가 없는 잡 {len(_noasm)}개 — 제출 본문이 "
                 f"exit 127 로 죽는다: {_noasm[:5]}")
    # ── 비용을 MANIFEST 에 **동결**한다 (ZIP 만으로 재현되게) ────────────────
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
            _jh.append(sum(
                CE.phase_hours(ph if ph in CE.ESTEP else "static", _n,
                               (_m.get("kmesh") or {}).get(ph, "3 4 1"), _base,
                               str(((_m.get("incar_expected") or {}).get(ph) or {})
                                   .get("LREAL", ".TRUE.")).upper().startswith(".F"), _ni)
                for ph in (_m.get("phases") or [])))
        man["cost_frozen"] = {
            "total_wall_h": round(sum(_jh), 1),
            "core_h": round(sum(_jh) * a.cores),
            "longest_job_h": round(max(_jh), 1) if _jh else None,
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
    man["files_sha256"] = files
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
    if a.single_point:
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
        head = (f" vasp.6.4.2\n{titels}\n   NIONS = {n}\n   NKPTS = {nk}\n{echo}\n"
                f"   NELM   =    200;   NELMIN=  6;\n")
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
        log = jd / "_phases.log"
        if prep:
            prep(jd)
        env = {**os.environ, "PATH": f"{stub_dir}:{os.environ.get('PATH', '')}",
               "VASP_CMD": "vasp_std", "STUB_LOG": str(log)}
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

    # ── R7 재개: 다 끝난 잡을 다시 돌리면 **아무 상도 안 돈다** ──────────────
    log2 = jd / "_phases.log"
    log2.unlink()
    r2 = subprocess.run(["bash", "run_job.sh"], cwd=jd, capture_output=True, text=True,
                        env={**os.environ, "PATH": f"{stub_dir}:{os.environ.get('PATH','')}",
                             "VASP_CMD": "vasp_std", "STUB_LOG": str(log2)})
    ran2 = log2.read_text().split() if log2.is_file() else []
    chk(r2.returncode == 0 and ran2 == [],
        f"R7 완주 잡 재실행 → 전 상 건너뜀 rc={r2.returncode} 실행 {ran2}")

    # ── R8 부분 재개: dense 산출만 지우면 dense 만 다시 돈다 ────────────────
    (jd / "dense" / "OUTCAR").unlink()
    log2.unlink(missing_ok=True)
    r3 = subprocess.run(["bash", "run_job.sh"], cwd=jd, capture_output=True, text=True,
                        env={**os.environ, "PATH": f"{stub_dir}:{os.environ.get('PATH','')}",
                             "VASP_CMD": "vasp_std", "STUB_LOG": str(log2)})
    ran3 = log2.read_text().split() if log2.is_file() else []
    chk(r3.returncode == 0 and ran3 == ["dense"],
        f"R8 dense 만 재개 rc={r3.returncode} 실행 {ran3}")

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

    # ── R13 러너 자체 sanity: stub 이 없으면 시험이 통과해선 안 된다 ─────────
    #   (양성만 있는 selftest 의 재발 방지 — 시험 장치 자체를 시험한다)
    jd13 = out.parent / "_run_nostub"
    shutil.rmtree(jd13, ignore_errors=True)
    shutil.copytree(src, jd13)
    (jd13 / "POTCAR").write_text("stub POTCAR\n")
    r13 = subprocess.run(["bash", "run_job.sh"], cwd=jd13, capture_output=True, text=True,
                         env={**os.environ, "VASP_CMD": "definitely_not_a_real_binary_xyz"})
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
                            no_prescf=False, allow_stale_gate=False, top_n=None, single_point=False, champion=False, kmesh_static=None, kmesh_dense=None, refs=True, cross_endpoints=None, mag_controls=False, dense_frags=None, cores=48, concurrency=8, no_cross=False, global_champion_meV=20.0, adaptive_dense=False)
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
                            no_prescf=False, allow_stale_gate=False, top_n=None, single_point=False, champion=False, kmesh_static=None, kmesh_dense=None, refs=True, cross_endpoints=None, mag_controls=False, dense_frags=None, cores=48, concurrency=8, no_cross=False, global_champion_meV=20.0, adaptive_dense=False)
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
                             no_prescf=False, allow_stale_gate=False, top_n=3, single_point=False, champion=False, kmesh_static=None, kmesh_dense=None, refs=True, cross_endpoints=None, mag_controls=False, dense_frags=None, cores=48, concurrency=8, no_cross=False, global_champion_meV=20.0, adaptive_dense=False)
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
                           no_prescf=False, allow_stale_gate=False, top_n=None, single_point=False, champion=False, kmesh_static=None, kmesh_dense=None, refs=True, cross_endpoints=None, mag_controls=False, dense_frags=None, cores=48, concurrency=8, no_cross=False, global_champion_meV=20.0, adaptive_dense=False)
    out = build_bundle(a, ledger=led)
    man = json.loads((out / "MANIFEST.json").read_text())
    n_pre = sum(1 for p in man["planned"].values() if "pre" in (p.get("phases") or []))
    chk(n_pre == len([p for p in man["planned"] if "mol__" not in p]),
        f"dipole-off pre-SCF 상이 전 슬랩 잡에 있다 ({n_pre}개)")

    # ── P0-2 러너 회귀: stub VASP 로 run_job.sh 를 **실제 실행** (Codex 4·6차) ──
    a_sp = argparse.Namespace(
        runs=str(td / "runs"), out=str(td / "bundle_sp"), freeze=0.85, nslab=nslab,
        frags=["ptfe_dimer"], qe="(none)", expect=None, allow_partial=False,
        no_prescf=False, allow_stale_gate=False, top_n=None, single_point=True,
        champion=True, kmesh_static=None, kmesh_dense=None, refs=False,
        cross_endpoints=["ptfe_dimer"], mag_controls=True, dense_frags=["ptfe_dimer"], cores=48, concurrency=8, no_cross=False, global_champion_meV=20.0, adaptive_dense=False)
    out_sp = build_bundle(a_sp, ledger=led)
    # ★ **배포되는 분석기**의 k 라벨·guard band selftest 를 그대로 돌린다.
    #   이 로직은 문자열 템플릿 안이라 여기서 import 로 시험할 수 없다 — 실행이 유일한 길.
    rk = subprocess.run([sys.executable, "analyze_results.py", "--selftest"],
                        cwd=out_sp, capture_output=True, text=True)
    for ln in rk.stdout.splitlines():
        print("   " + ln)
    chk(rk.returncode == 0, f"배포 분석기 k-selftest (rc={rk.returncode})")
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

    # ── end-to-end: OUTCAR **파일** → read_outcar → phase_gates (codex E-1 필수) ──
    #   문자열 단위 검사는 통합 경로의 결함(예: 한 토큰 잘림)을 못 잡는다 —
    #   wave1 에서 실제로 그랬다. 실제 파일로 전 경로를 통과시킨다.
    import gzip as _gz
    import tempfile as _tf
    _BODY = (" vasp.5.4.4.18Apr17-6-g9f103f2a35 (build test) complex\n"
             "|      So try LREAL= Auto  in the INCAR   file.        |\n"
             "   ENCUT  =  520.0 eV  38.22 Ry\n"
             "   ISPIN  =      2    spin polarized calculation?\n"
             "   LREAL  =      T    real-space projection\n"
             "   LDIPOL =      T    correct potential\n"
             "   NUPDOWN=      4.0000    fix difference up-down\n"
             " LDA+U is selected, type is set to LDAUTYPE =  2\n"
             "   angular momentum for each species LDAUL =    -1    2   -1\n"
             "   U (eV)           for each species LDAUU =   0.0  6.2  0.0\n"
             "   J (eV)           for each species LDAUJ =   0.0  0.0  0.0\n"
             "  energy(sigma->0) =     -100.000000\n"
             " General timing and accounting\n")
    _EXP = {"ENCUT": "520", "LREAL": "Auto", "LDIPOL": ".TRUE.", "ISPIN": "2",
            "NUPDOWN": "4", "LDAUTYPE": "2", "LDAUL": "-1 2 -1",
            "LDAUU": "0.0 6.2 0.0", "LDAUJ": "0.0 0.0 0.0"}

    def _e2e(body_bytes, want=None, gz_trunc=False, both=False):
        with _tf.TemporaryDirectory() as _d:
            _o = os.path.join(_d, "OUTCAR")
            if gz_trunc:
                full = _gz.compress(body_bytes)
                open(_o + ".gz", "wb").write(full[:len(full) // 2])
            elif both:
                open(_o, "wb").write(body_bytes)
                open(_o + ".gz", "wb").write(_gz.compress(body_bytes))
            else:
                open(_o, "wb").write(body_bytes)
            _oc = _az.read_outcar(_o)
            _g2 = _az.phase_gates(_oc, "static",
                                  {"incar_expected": {"static": want or _EXP}}, {})
            return _oc, _g2

    _oc, _g2 = _e2e(_BODY.encode())
    chk(not any("INCAR" in x for x in _g2), f"e2e 정상: INCAR 게이트 0건 ({_g2})")
    _au = _oc["incar_audit"]
    chk("LDAUU" in _au["verified_exact"] and "NUPDOWN" in _au["verified_exact"],
        f"e2e: LDAUU 목록·NUPDOWN(4.0000↔4) 이 exact ({_au['verified_exact']})")
    chk("LREAL" in _au["verified_equivalence_class"],
        "e2e: LREAL 은 equal 이 아니라 **등가류** (Auto/On 구분 불가를 기록)")
    chk(any(x.startswith("MAGMOM") for x in _au["unverified"]),
        "e2e: MAGMOM 은 **명시적 unverified** (조용한 통과 금지)")
    _oc, _g2 = _e2e(_BODY.encode(), want=dict(_EXP, LDAUU="0.0 5.0 0.0"))
    chk(any("INCAR_MISMATCH(static.LDAUU" in x for x in _g2),
        f"⛔e2e음성: LDAUU 실제 차이(6.2 vs 5.0)가 **전 경로**에서 잡힌다")
    _oc, _g2 = _e2e(_BODY.encode().replace(b"ENCUT", b"ENC\xffUT"))
    chk(any("OUTCAR_READ_ERROR" in x for x in _g2),
        f"⛔e2e음성: 깨진 바이트(ENC\\xffUT) → 판독 실패 (조용한 오독 금지) ({_g2[:1]})")
    _oc, _g2 = _e2e(_BODY.encode(), gz_trunc=True)
    chk(any("OUTCAR_READ_ERROR" in x and "gzip" in x for x in _g2),
        "⛔e2e음성: 잘린 gzip → 예외가 아니라 판독 실패 게이트")
    _oc, _g2 = _e2e(_BODY.encode(), both=True)
    chk(any("OUTCAR_READ_ERROR" in x and "둘 다" in x for x in _g2),
        "⛔e2e음성: OUTCAR + OUTCAR.gz 공존 → 정본 판정 불가")
    _TWO = (_BODY.replace("-100.000000", "-1.000000") + _BODY.replace("-100.000000",
                                                                      "-2.000000"))
    _oc, _g2 = _e2e(_TWO.encode())
    chk(any("MULTI_RUN_OUTCAR" in x for x in _g2) and _oc["E0"] == -2.0,
        f"⛔e2e음성: 이어붙은 2실행 → MULTI_RUN + **마지막 완결 실행만** 읽음 (E0={_oc['E0']})")
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
    print("✔ selftest 전부 통과" if ok else "⛔ selftest 실패")
    return 0 if ok else 1


def main():
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
    ap.add_argument("--refs", action="store_true",
                    help="clean 슬랩 + 기체 분자 기준계를 포함한다 (절대 E_ads 용). "
                         "기본은 **미포함** — 자리 대비 ΔE 에서는 정확히 소거되므로 "
                         "Wave 2 로 미룬다 (Codex 5차).")
    ap.add_argument("--cores", type=int, default=48,
                    help="잡당 코어 수 — MANIFEST·SUBMIT_CONTRACT 에 기록된다 "
                         "(비용 모형 기준선과 같아야 추정이 맞는다)")
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
    if a.selftest:
        return selftest()
    build_bundle(a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
