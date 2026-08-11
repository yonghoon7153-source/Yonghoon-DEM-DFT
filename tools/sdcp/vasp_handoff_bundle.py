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
  ③ **범위** (2026-08-12 결정): tier1·tier2 **전 끝점 2 seed** = 86 잡. seed 1종 쌍은
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
EXPECT_PAIRS = {"ptfe_c10": 5, "ptfe_dimer": 3, "sdcp_neutral": 5, "sdcp_doped": 5}
SEEDS_FULL = ("afm2424_pm1", "afm2424_net4")       # tier1 전 끝점 · clean
SEED_MAIN = "afm2424_pm1"                          # 판정 headline
#: Ni_pv = 2026-08-08 실납품 TITEL 계보 (자체검토 P0-2)
POTCAR_SPEC = {"Li": "Li_sv", "Ni": "Ni_pv", "O": "O", "S": "S", "C": "C", "F": "F",
               "H": "H", "B": "B", "P": "P", "Cl": "Cl", "Na": "Na_pv"}
KMESH = {"relax": "2 3 1", "static": "3 4 1", "dense": "4 6 1"}   # a=18.3 > b=11.5 Å

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
# pre 의 WAVECAR(ISTART=1)를 승계해 dipole 을 켠 채 다시 수렴시킨다.
{common}EDIFF    = 1E-5
EDIFFG   = -0.02
IBRION   = 2
NSW      = 200
ISIF     = 2
LREAL    = Auto
ISTART   = 1
ICHARG   = 0
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
#   VASP_CMD="mpirun -np 64 vasp_std" bash run_job.sh
#
# 상 사슬 (하나라도 끊기면 **멈춘다** — 조용히 건너뛰면 다른 계를 계산하게 된다):
#   pre    dipole off, LWAVE=T          → WAVECAR·CHGCAR
#   relax  ISTART=1 (pre 의 WAVECAR)     → CONTCAR·CHGCAR
#   static ICHARG=1 (relax 의 CHGCAR)    → 판정 에너지
#   dense  ICHARG=1 (**static** 의 CHGCAR) → k 수렴 확인
set -e
V=${VASP_CMD:-"mpirun -np ${NP:-64} vasp_std"}
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
    static) need relax/CONTCAR "relax 를 먼저 완주시킬 것"
            need relax/CHGCAR  "ICHARG=1 인데 승계할 전하밀도가 없다 (relax LCHARG=.TRUE. 확인)"
            cp relax/CONTCAR static/POSCAR
            cp relax/CHGCAR  static/CHGCAR ;;
    dense)  need relax/CONTCAR "relax 를 먼저 완주시킬 것"
            need static/CHGCAR "dense 는 **static** 의 전하밀도를 승계한다 — static 먼저"
            cp relax/CONTCAR dense/POSCAR
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

RUN_ALL = """#!/usr/bin/env bash
# 전체 실행: tier1 → refs → tier2.  VASP_CMD 환경변수로 실행 명령을 지정.
set -u
fail=0
for grp in tier1 refs tier2; do
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
def discover_pairs(run_dir: Path, audit: Optional[Dict[str, Any]] = None
                   ) -> List[Dict[str, Any]]:
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
    fps = sorted({str(r.get("fingerprint")) for r in fs if r.get("fingerprint")})
    if len(fps) > 1:
        sys.exit(f"⛔ {run_dir} 에 프로토콜 지문이 {len(fps)}종 섞여 있다: {fps} — "
                 f"regate/재실행으로 정리한 뒤 다시 만들 것")
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
    if audit is not None:
        seen: Dict[str, Dict[str, int]] = {}
        for r in rows:
            d = str(r.get("down_dir"))
            key = str(r.get("site")) + ("" if r.get("ranking_eligible") else "(부적격)")
            seen.setdefault(d, {})[key] = seen.setdefault(d, {}).get(key, 0) + 1
        audit["n_down_dirs"] = len(seen)
        audit["n_contrast_pairs"] = len(out)
        audit["excluded_dirs"] = {d: c for d, c in sorted(seen.items())
                                  if d not in by_dir}
        audit["note"] = ("제외된 방향은 Li_top↔Ni_top 대조쌍이 없는 것이다 — 자리 종류를 "
                         "훑은 방향이거나(O_top·hollow·*_bridge) 한쪽이 부적격인 경우다. "
                         "누락이 아니라 대조쌍 정의 밖이다.")
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


def _emit_slab_job(jd: Path, atoms, nslab: int, freeze: float, frag: str,
                   system: str, seed_name: str, extra_meta: Dict[str, Any],
                   ledger: Dict[str, Any], zcut=None, dense: bool = False,
                   prescf: bool = True) -> Dict[str, Any]:
    """슬랩 잡 v2 — POSCAR(루트) + pre/ + relax/ + static/ (+dense/). MAGMOM 재매핑·검산."""
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
    phases = (["pre"] if prescf else []) + ["relax", "static"] + (["dense"] if dense else [])
    for ph in phases:
        (jd / ph).mkdir(exist_ok=True)
        (jd / ph / "INCAR").write_text(tpls[ph].format(**fmt))
        km = KMESH["relax"] if ph == "pre" else KMESH[ph]
        (jd / ph / "KPOINTS").write_text(f"auto\n0\nGamma\n{km}\n0 0 0\n")
    (jd / "run_job.sh").write_text(RUN_JOB)
    top = _top_cations(atoms, nslab, sym)
    rev = {i: k for k, i in enumerate(pos["order"])}      # 원본 → POSCAR 위치
    meta = {**pos, **extra_meta, "seed": seed_name, "nslab": nslab,
            "phases": phases, "zcom_frac": round(zcom, 4),
            "magmom_poscar": [round(m, 3) for m in mag_poscar],
            "ni_sign_poscar_idx": {str(rev[i]): mag_orig[i] for i in range(nslab)
                                   if sym[i] == "Ni"},
            "mol_poscar_idx": [k for k, i in enumerate(pos["order"]) if i >= nslab],
            "slab_li_poscar_idx": [k for k, i in enumerate(pos["order"])
                                   if i < nslab and sym[i] == "Li"],
            "slab_ni_poscar_idx": [k for k, i in enumerate(pos["order"])
                                   if i < nslab and sym[i] == "Ni"],
            "top_li_poscar_idx": sorted(rev[i] for i in top["Li"]),
            "top_ni_poscar_idx": sorted(rev[i] for i in top["Ni"])}
    (jd / "job.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    return meta


def _emit_mol_job(jd: Path, frag: str, mol, margin: float) -> Dict[str, Any]:
    """기체상 기준계 v2 — 상자 span+margin, IDIPOL=4+DIPOL(COM), NUPDOWN, 2상."""
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
    for ph, tpl in (("relax", MOL_RELAX), ("static", MOL_STATIC)):
        (jd / ph).mkdir(exist_ok=True)
        (jd / ph / "INCAR").write_text(tpl.format(**fmt))
        (jd / ph / "KPOINTS").write_text("gamma-only\n0\nGamma\n1 1 1\n0 0 0\n")
    (jd / "run_job.sh").write_text(RUN_JOB)
    meta = {"kind": "mol_ref", "fragment": frag, "species_order": seen, "counts": counts,
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
RMSD_TOL = 0.75           # Å — 두 끝점이 같은 basin 인가 (0.50/1.00 민감도도 같이 뽑는다)
CONTACT_A = 3.0           # Å — 접촉 지문 반경
FP_JACCARD = 0.80         # 접촉 지문 겹침 — 경계 원자 하나로 뒤집히지 않게 완전일치 대신
RCOV = {"H": 0.31, "B": 0.84, "C": 0.76, "N": 0.71, "O": 0.66, "F": 0.57,
        "Na": 1.66, "P": 1.07, "S": 1.05, "Cl": 1.02, "Li": 1.28, "Ni": 1.24}
BOND_F = 1.25             # 결합 = d < BOND_F × (r_i + r_j)
DETACH_A = 4.0            # 분자-슬랩 최소거리가 이보다 크면 탈착
FIX_DRIFT_A = 0.10        # 고정(F F F) 원자가 이보다 움직이면 파일 불일치
FORCE_TOL = 0.05          # eV/Å — 자유원자 잔여 힘 경고
MOM_MIN = 0.30            # μB — Ni 국소 모멘트가 이보다 작으면 붕괴로 본다
#: 준중심(semicore) 변형이 다르면 원자가 전자 수가 달라진다 — 일관돼도 치명이다.
SEMICORE = ("_pv", "_sv", "_h", "_s", "_d")


def _read_text(path):
    try:
        if os.path.isfile(path):
            return open(path, errors="ignore").read()
        if os.path.isfile(path + ".gz"):
            return gzip.open(path + ".gz", "rt", errors="ignore").read()
    except OSError:
        pass
    return None


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


def read_outcar(p):
    t = _read_text(p)
    if t is None:
        return None
    e = re.findall(r"energy\(sigma->0\)\s*=\s*(-?[\d.]+)", t)
    nions = re.search(r"NIONS\s*=\s*(\d+)", t)
    nelm = re.search(r"NELM\s*=\s*(\d+)", t)
    iters = re.findall(r"Iteration\s+\d+\(\s*(\d+)\)", t)
    ver = re.search(r"vasp\.([\w.]+)", t)
    titels = re.findall(r"TITEL\s*=\s*(.+)", t)
    mag = re.findall(r"number of electron\s+[\d.]+\s+magnetization\s+(-?[\d.]+)", t)
    forces = None
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
            "titels": [x.strip() for x in titels],
            "vasp_version": ver.group(1) if ver else None,
            "mag_total": float(mag[-1]) if mag else None,
            "moments": read_moments(t), "forces": forces,
            "incar_echo": {k2: (re.search(k2 + r"\s*=\s*([-\w.]+)", t).group(1)
                                if re.search(k2 + r"\s*=\s*([-\w.]+)", t) else None)
                           for k2 in ("ISTART", "ICHARG", "LDIPOL", "IVDW", "LREAL",
                                      "ENCUT", "ISMEAR")}}


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
    fin = read_poscar(os.path.join(jd, "relax", "CONTCAR"))
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
            gates.append(f"PAIR_MIGRATED:{want}->{info['registry']['nearest']}")
        slab_idx = (meta.get("slab_li_poscar_idx") or []) + \
                   (meta.get("slab_ni_poscar_idx") or [])
        dsl = min((mic_dist(fin["pos"][m], fin["pos"][i], fin["cell"])
                   for m in mol for i in slab_idx), default=1e9)
        info["mol_slab_min_A"] = round(dsl, 3)
        if dsl > DETACH_A:
            gates.append(f"DETACHED(분자-슬랩 {dsl:.2f} Å > {DETACH_A})")
        info["_contact_fp"] = sorted(contact_fp(fin, mol, slab_idx))
    if mol:
        # 기체 기준계도 여기 온다 (슬랩이 없어 위 블록은 건너뛴다) — 결합 감사는 한다
        b0, b1 = mol_bond_graph(init, mol), mol_bond_graph(fin, mol)
        broke, formed = b0 - b1, b1 - b0
        info["bonds"] = {"initial": len(b0), "broken": len(broke), "formed": len(formed)}
        if broke or formed:
            gates.append(f"BOND_CHANGE(끊김 {len(broke)} · 생성 {len(formed)})")
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


def phase_gates(oc, ph, meta, spec, want_ionic=False):
    """상 하나의 fail-closed 검사. oc 가 None 이면 NOT_RUN."""
    g = []
    if oc is None:
        return [f"NOT_RUN({ph})"]
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
    nat = sum(meta.get("counts", []) or [])
    if nat and oc["nions"] and oc["nions"] != nat:
        g.append(f"NIONS_MISMATCH({ph}: {oc['nions']}!={nat})")
    return g


def main():
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

    jobs = {}
    for jd in sorted(glob(os.path.join(root, "*", "*", ""))):
        jp = os.path.join(jd, "job.json")
        if not os.path.isfile(jp):
            continue
        meta = json.load(open(jp))
        rel = os.path.relpath(jd, root).rstrip("/")
        phases = (planned.get(rel) or {}).get("phases") or meta.get("phases") or \
            ["relax", "static"]
        ocs = {ph: read_outcar(os.path.join(jd, ph, "OUTCAR")) for ph in phases}
        rec = {"meta": meta, "static": ocs.get("static"), "dense": ocs.get("dense"),
               "gates": []}
        for ph in phases:
            rec["gates"] += phase_gates(ocs[ph], ph, meta, spec,
                                        want_ionic=(ph == "relax"))
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
        # ── 자기상태 감사 (Codex P0-E) ──
        st = ocs.get("static")
        want_sign = meta.get("ni_sign_poscar_idx") or {}
        if st is not None and want_sign:
            mom = st.get("moments")
            if not mom:
                rec["gates"].append("MAGNETIC_UNVERIFIED(LORBIT 모멘트 표 없음)")
            else:
                ni = {int(k): v for k, v in want_sign.items() if int(k) < len(mom)}
                got_m = {i: mom[i] for i in ni}
                small = [i for i, m in got_m.items() if abs(m) < MOM_MIN]
                flip = [i for i, m in got_m.items() if ni[i] * m < 0]
                rec["geom"]["magnetic"] = {
                    "n_ni": len(ni), "n_small": len(small), "n_sign_flipped": len(flip),
                    "abs_mean_muB": round(sum(abs(m) for m in got_m.values())
                                          / max(1, len(got_m)), 3),
                    "total_muB": st.get("mag_total")}
                if small:
                    rec["gates"].append(f"MOMENT_COLLAPSED({len(small)}개 |m|<{MOM_MIN})")
                if flip:
                    rec["geom"]["magnetic"]["note"] = (
                        "시드 부호와 다른 Ni 가 있다 — 다른 자기 basin 으로 수렴했다")
                if len(flip) == len(ni) and ni:
                    rec["gates"].append("MAGNETIC_ALL_FLIPPED(전 Ni 부호 반전 — 같은 상태)")
        rec["ok"] = not rec["gates"]
        jobs[rel] = rec

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
    fatal_subs = {e: g for e, g in subs.items()
                  if any(s in e for s in SEMICORE) != any(s in g for s in SEMICORE)
                  or e.split("_")[0] != g.split("_")[0]}
    if subs:
        txt = ", ".join(f"{e}→{g}" for e, g in sorted(subs.items()))
        if mixed or fatal_subs:
            for r in jobs.values():
                r["gates"].append(f"POTCAR_WRONG({txt})")
                r["ok"] = False
        else:
            potcar_warn = (f"POTCAR 변형이 스펙과 **일관되게** 다르다: {txt} — 같은 원자가라 "
                           f"내부 비교는 유효, 절대값 인용 시 기록할 것")

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

    results = {"delta_eV": delta, "pairs": {}, "fragments": {}, "e_ads": {},
               "numerical_gates": {}, "warnings": [], "integrity": integrity,
               "jobs": {j: {"ok": r["ok"], "gates": r["gates"],
                            "E0_static": (r["static"] or {}).get("E0"),
                            "vasp_version": (r["static"] or {}).get("vasp_version"),
                            "geom": r.get("geom")} for j, r in jobs.items()}}
    if potcar_warn:
        results["warnings"].append(potcar_warn)
    if integrity["changed"]:
        results["warnings"].append(
            f"⛔ 번들 입력 {len(integrity['changed'])}개가 바뀌었다 (INCAR/POSCAR 변조?): "
            + ", ".join(integrity["changed"][:8]))

    # ── 기체상 — 상자 게이트. **정본은 큰 상자(box24)** ──────────────────────
    emol, mol_ok = {}, {}
    for f in man.get("fragments", []):
        e20 = E(os.path.join("refs", f"mol__{f}__box20"))
        e24 = E(os.path.join("refs", f"mol__{f}__box24"))
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

    eclean = {s: E(os.path.join("refs", f"clean_slab__{s}"))
              for s in man.get("seeds_full", ["afm2424_pm1", "afm2424_net4"])}
    eclean_dense = E_dense(os.path.join("refs", "clean_slab__afm2424_pm1"))

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
                    # ⚠ 양쪽 다 접촉이 없으면 지문은 **정보가 없다**. 빈 집합끼리 같다고
                    #   해서도, 다르다고 해서도 안 된다 — RMSD 로만 판정하고 그렇게 적는다.
                    #   (진짜 떠 있으면 DETACHED 가 따로 잡는다.)
                    jac, fp_ok, why = None, True, "접촉 없음 — RMSD 로만"
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
                    rec["gates"].append(
                        f"PAIR_COLLAPSED(분자 RMSD {rms:.2f} Å ≤ {RMSD_TOL} · {why})")
        de_main = rec["dE_by_seed"].get("afm2424_pm1")
        de_alt = rec["dE_by_seed"].get("afm2424_net4")
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
                dk = abs((dni - dli) - de_main)
                ok_k = dk <= K_TOL
                gate = {"dE_meV": round(dk * 1000, 1), "pass": ok_k}
                # E_ads 자체의 k 수렴도 본다 (ΔE 만 보면 상쇄로 숨는다)
                if eclean_dense is not None and emol.get(frag) is not None \
                        and E(f"{pm['li_prefix']}__afm2424_pm1") is not None:
                    ea_s = E(f"{pm['li_prefix']}__afm2424_pm1") \
                        - eclean.get("afm2424_pm1", 0.0) - emol[frag]
                    ea_d = dli - eclean_dense - emol[frag]
                    gate["dEads_meV"] = round(abs(ea_d - ea_s) * 1000, 1)
                    ok_k = ok_k and abs(ea_d - ea_s) <= K_TOL
                    gate["pass"] = ok_k
                results["numerical_gates"][f"k_{pid}"] = gate
                if not ok_k:
                    rec["gates"].append(f"NUMERICALLY_UNRESOLVED(dense-k {gate})")

        if de_main is not None and not rec["gates"]:
            rec["dE_Ni_minus_Li_eV"] = de_main
            ec = eclean.get("afm2424_pm1")
            if ec is not None and emol.get(frag) is not None:
                eli = E(f"{pm['li_prefix']}__afm2424_pm1")
                eni = E(f"{pm['ni_prefix']}__afm2424_pm1")
                results["e_ads"][pid] = {
                    "Li_top": round(eli - ec - emol[frag], 4),
                    "Ni_top": round(eni - ec - emol[frag], 4),
                    "mol_ref": "box24"}
        results["pairs"][pid] = rec

    for frag in man.get("fragments", []):
        dl = [r["dE_Ni_minus_Li_eV"] for r in results["pairs"].values()
              if r["fragment"] == frag and "dE_Ni_minus_Li_eV" in r]
        n_planned = sum(1 for p in man["pairs"].values() if p["fragment"] == frag)
        expect_dirs = (man.get("contract_expected_pairs") or {}).get(frag)
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
        if expect_dirs and n_planned != expect_dirs:
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
        results["fragments"][frag] = {
            "n_directions": n, "n_planned": n_planned, "dE_list": dl,
            "median_eV": round(med, 4), "class": cls,
            "n_down_dirs": nd, "direction_coverage": None if cov is None else round(cov, 2),
            "disqualified_dirs": lost,
            "read_as": "Li 우세 경향" if med > 0 else "Ni 우세 경향",
            "note": ("PBE+U(6.2)+D3-zero fixed-protocol tendency — UMA 값과 같은 표 금지. "
                     "δ=%.3f eV." % delta)}
        if lost:
            results["warnings"].append(
                f"{frag}: down_dir {nd}개 중 {len(lost)}개가 **번들 이전에** 탈락했다 "
                f"({', '.join(sorted(lost))}) — 계획 {n_planned}개는 이미 줄어든 수다. "
                f"탈락 사유가 물리적으로 정당한지 확인하고 원고에 방향 수를 명시할 것")

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
    if integrity["changed"]:
        print(f"\n⛔ **입력 무결성 실패** {len(integrity['changed'])}건 — exit 2")
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


README = """# VASP 외주 요청 v2 — SDCP/PTFE 자리 선호 + 흡착에너지 (원샷)

## 무엇을 계산하나
LiNiO₂(104) 슬랩 위 분자 조각의 **자리 선호**(Li_top vs Ni_top)와 **흡착에너지**.
MLIP 스크리닝은 경향까지만 냈고, 이 DFT+U 가 최종 판정입니다.

## 잡 구조 — **잡마다 여러 상**
각 잡 폴더: `POSCAR` + `pre/` + `relax/` + `static/`(일부는 `dense/`) + `run_job.sh`.
**판정 에너지는 static 입니다** — relax 만 돌리면 결과가 성립하지 않습니다.
`pre/` 는 dipole 을 끈 사전 SCF 입니다 (자기상태가 엉뚱한 basin 으로 무너지는 것을 막습니다).
`run_job.sh` 가 상 사이 CHGCAR/WAVECAR 승계를 **강제**합니다 — 파일이 없으면 멈춥니다.
```
cd <잡폴더> && cp <POTCAR> POTCAR && VASP_CMD="mpirun -np 64 vasp_std" bash run_job.sh
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
        "bundle_version": "v2", "gate_version": SS.gate_version(),
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
        "protocol_delta_vs_phaseB": ("의도된 개선: LASPH T(납품 F) · LDIPOL T(납품 F) · "
                                     "ISMEAR 0/0.05(납품 1/0.2) · relax+static 2상(납품 "
                                     "단일점) · LREAL static .FALSE.(납품 Auto). "
                                     "승계: U 6.2 · IVDW 11 · ENCUT 520 · Ni_pv."),
    }
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
    man["contract_expected_pairs"] = expect
    man["allow_partial"] = bool(a.allow_partial)
    man["pair_audit"] = {}
    viol: List[str] = []

    def bad(msg: str):
        viol.append(msg)
        print(("  ⚠ " if a.allow_partial else "  ⛔ ") + msg)

    for tier, frags in TIERS.items():
        req = tier == "tier1"
        for frag in frags:
            if a.frags and frag not in a.frags:
                continue
            run = Path(a.runs) / frag / f"relax_f{a.freeze:.2f}"
            if not run.is_dir():
                bad(f"{frag}: {run} 없음")
                continue
            aud: Dict[str, Any] = {}
            pairs = discover_pairs(run, audit=aud)
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
                dense = req or (p is probe)
                xyzs = {role: (run / f"{rec['label']}.xyz", rec)
                        for role, rec in (("Li", p["li"]), ("Ni", p["ni"]))}
                miss = [r for r, (xp, _) in xyzs.items() if not xp.is_file()]
                if miss:
                    bad(f"{pid}: {'/'.join(miss)} 쪽 xyz 없음 — 쌍 통째로 빠짐")
                    continue
                pm = {"fragment": frag, "dir": p["dir"], "roll": p["roll"],
                      "uma_dE": p["dE_uma"], "uma_dir_median": p["dir_median_uma"],
                      "n_rolls_folded": p["n_rolls"], "seeds": seeds,
                      "dense_probe": dense,
                      "li_prefix": f"{tier}/{pid}__Litop",
                      "ni_prefix": f"{tier}/{pid}__Nitop"}
                for role, (xp, rec) in xyzs.items():
                    cx = ase_read(xp); cx.set_cell(slab.cell.array); cx.set_pbc(True)
                    _assert_slab_lineage(cx, nslab, slab, f"{pid}/{role}", man)
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
                            prescf=not a.no_prescf)
                        slab_metas.append(m)
                        plan(rel, m["phases"], req)
                        n_jobs += 1
                man["pairs"][pid] = pm

    if not man["pairs"]:
        shutil.rmtree(out)
        sys.exit("⛔ 자격 쌍이 0개다 — 번들을 만들지 않는다 "
                 "(--runs/--freeze 경로와 relax 산출물을 확인할 것)")

    for sd in SEEDS_FULL:
        rel = f"refs/clean_slab__{sd}"
        m = _emit_slab_job(out / rel, clean, len(clean), a.freeze, man["fragments"][0],
                           f"clean slab {sd}", sd, {"kind": "clean_ref"},
                           ledger, zcut=zcut, dense=sd == SEED_MAIN,
                           prescf=not a.no_prescf)
        slab_metas.append(m)
        plan(rel, m["phases"], True)
        n_jobs += 1
    man["refs"]["clean_slab"] = [f"refs/clean_slab__{s}" for s in SEEDS_FULL]

    for frag in man["fragments"]:
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
    (out / "README_REQUEST.md").write_text(README.format(
        freeze_pct=int(a.freeze * 100), zcut_note=f"{zcut:.3f} Å",
        k_relax=KMESH["relax"], k_static=KMESH["static"]))
    (out / "POTCAR_SPEC.txt").write_text(
        "# 원소 → POTCAR 변형 (PBE PAW 5.4). 각 잡 POSCAR 의 종 순서대로 이어붙일 것.\n"
        "# Ni_pv 는 2026-08-08 납품과 동일 계보다 — 바꾸지 말 것.\n"
        + "\n".join(f"{e:3s} {v}" for e, v in man["potcar_spec"].items()) + "\n")

    files = {}
    for p in sorted(out.rglob("*")):
        if p.is_file() and p.name != "MANIFEST.json":
            files[str(p.relative_to(out))] = hashlib.sha256(p.read_bytes()).hexdigest()
    man["n_jobs"] = n_jobs
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
    head = (f" vasp.6.4.2\n{titels}\n   NIONS = {n}\n"
            f"   NELM   =    200;   NELMIN=  6;\n")
    end = " General timing and accounting\n"
    for ph in meta.get("phases", ["relax", "static"]):
        (jd / ph).mkdir(exist_ok=True)
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
                "nearest_cation": ncat, "ranking_eligible": True}))

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
                            no_prescf=False)
    try:
        build_bundle(a0, ledger=led)
        chk(False, "N0 xyz 누락 → **번들이 만들어졌다** (축소 정본 = fail-open)")
    except SystemExit as e:
        chk("계약 위반" in str(e), f"N0 xyz 누락 → 생성 중단 ({str(e).splitlines()[0][:44]})")
    (run.parent / "hidden.xyz").rename(hidden)

    a = argparse.Namespace(runs=str(td / "runs"), out=str(td / "bundle"),
                           freeze=0.85, nslab=nslab, frags=["ptfe_dimer"],
                           qe="(none)", expect=None, allow_partial=False,
                           no_prescf=False)
    out = build_bundle(a, ledger=led)
    man = json.loads((out / "MANIFEST.json").read_text())
    n_pre = sum(1 for p in man["planned"].values() if "pre" in (p.get("phases") or []))
    chk(n_pre == len([p for p in man["planned"] if "mol__" not in p]),
        f"dipole-off pre-SCF 상이 전 슬랩 잡에 있다 ({n_pre}개)")

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
        t = (dj.parent / "static" / "OUTCAR").read_text()
        e0 = float(_re.search(RX, t).group(1))
        shift = 0.003 if "Nitop" in dj.parent.name else 0.0
        (dj / "OUTCAR").write_text(t.replace(f"{e0:.6f}", f"{e0 + shift:.6f}"))
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
    chk(any("BLOCKED_MAGNETIC" in g for g in res["pairs"]
            ["ptfe_dimer__fib03_r000"]["gates"]),
        "N3 seed 50 meV 불일치 → BLOCKED_MAGNETIC_SENSITIVITY")
    chk(any("NOT_TERMINATED" in g for g in res["jobs"][tr_job]["gates"]),
        f"N5 잘린 OUTCAR → NOT_TERMINATED ({res['jobs'][tr_job]['gates']})")
    chk(any("POTCAR_UNVERIFIED" in g for g in res["jobs"][nt_job]["gates"]),
        f"N6 TITEL 없음 → POTCAR_UNVERIFIED (통과 아님)")
    chk(any("MOMENT_COLLAPSED" in g for g in res["jobs"][mc_job]["gates"]),
        f"N7 모멘트 붕괴 → MOMENT_COLLAPSED ({res['jobs'][mc_job]['gates']})")
    chk(len(res["integrity"]["changed"]) == 1, f"N9 INCAR 변조 → 무결성 1건 감지")

    # ── 양성: 게이트에 안 걸린 쌍은 값이 **정확히** 복원돼야 한다 ──
    p0 = res["pairs"]["ptfe_dimer__fib00_r000"]
    de = p0.get("dE_Ni_minus_Li_eV")
    chk(de is not None and abs(de - truth["fib00"]) < 1e-6,
        f"양성 ΔE 복원 fib00 = {de} (심은 값 {truth['fib00']})")
    kg = res["numerical_gates"].get("k_ptfe_dimer__fib00_r000")
    chk(kg is not None and abs(kg["dE_meV"] - 3.0) < 1e-6,
        f"dense-k 게이트가 **한쪽만** 옮긴 3 meV 를 잡는다 ({kg})")
    chk(res["numerical_gates"].get("box_ptfe_dimer", {}).get("pass") is False,
        "N8 box24 없음 → 상자 게이트 **실패**로 기록 (옛 판은 항상 참이었다)")
    chk(not res["e_ads"], "상자 게이트 실패 → E_ads 를 만들지 않는다")
    chk(bool(res["required_missing"]), f"N8 필수 누락 기록 {len(res['required_missing'])}건")
    # ── PAIR_COLLAPSED 양성/음성 (새 basin 판정) ──
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
    ap.add_argument("--out", default="/data/work/runs/sdcp_vasp_oneshot_v2")
    ap.add_argument("--freeze", type=float, default=0.85)
    ap.add_argument("--nslab", type=int, default=192)
    ap.add_argument("--frags", nargs="*", default=None)
    ap.add_argument("--qe", default=str(Path(SS.REPO) / "db" / "inputs" / "sdcp_v2"
                                        / "slab_relax" / "relax.in"),
                    help="Ni1/Ni2 라벨이 있는 QE 입력 (부격자 원장의 원본)")
    ap.add_argument("--expect", nargs="*", default=None,
                    help="계약 방향 수 재정의: ptfe_c10=5 ptfe_dimer=3 ...")
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
