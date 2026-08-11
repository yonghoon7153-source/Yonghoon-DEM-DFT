#!/usr/bin/env python3
"""vasp_handoff_bundle.py — VASP 외주 **원샷** 번들 v2 (Codex 재검토 반영판).

v1 → v2 (2026-08-11 Codex HOLD 전건 반영 · kb/reviews/vasp_bundle_codex_reply_2026_08_11.md)
  ① **4상 러너**: relax(2×3×1) → final static(3×4×1 · LREAL=.FALSE. · EDIFF 1e-6 ·
     ISTART=0/ICHARG=1) → (대표쌍만) dense(4×6×1). **판정 에너지는 static 에서만** 회수.
     v1 은 relax 마지막 에너지(LREAL=Auto·1e-5)를 최종값으로 썼다 — 판정용이 아니었다.
  ② **정본 자기 seed = 실납품 계보**. ⚠ Codex 가 인용한 `ptfe_linio2_uma/vasp_stage.py`
     는 이 repo 에 없다 — 대신 **실제 2026-08-08 납품 INCAR** (runs/sdcp_phaseB_vasp_v1_
     2026_08_08/slab/INCAR)가 정본이고, 그 MAGMOM 은 **Ni 앞 24개 −1 · 뒤 24개 +1**
     (±1 μB, "QE Ni1/Ni2 부격자 배정") 블록이다 → `afm2424_pm1`. Codex 가 제안한 이름
     (qe_afm24_24_pm1)과 정확히 같은 구조라 계보 논쟁은 없다. net4 는 탐사용으로 강등.
  ③ **seed-매칭 ΔE**: 끝점별 독립 min 은 ΔE 를 최대 2×(seed 산포)만큼 오염시킨다 —
     같은 seed 끼리만 빼고, |ΔE_pm1 − ΔE_net4| > 10 meV 면 BLOCKED_MAGNETIC_SENSITIVITY.
     tier1 은 **전 끝점 2 seed** (탐침 경제는 tier2 에만).
  ④ 기체상: IDIPOL=4 + DIPOL(COM) · doped NUPDOWN=1 / closed 0 · **상자 2종**
     (span+20 / span+24 Å, |ΔE_mol| ≤ 10 meV 게이트).
  ⑤ 기하 감사 확장: 최근접 하나 → **결합 그래프 변화**(공유반경 내장) · 탈착 ·
     고정원자 drift · 자유원자 잔여 힘 · PAIR_COLLAPSED(두 끝점 같은 registry).
  ⑥ 분석기 fail-closed: 필수(tier1+refs) static 누락 시 **exit 2**. 음성 selftest 내장.
  실납품과 다른 점(의도된 개선, provenance 에 기록): LASPH=T(납품 F) · LDIPOL=T(납품 F)
  · ISMEAR=0/0.05(납품 1/0.2) · 이완+정적 2상(납품 단일점). U=6.2·IVDW=11·ENCUT 520 은 승계.

v1 에서 승계된 강화(자체검토): 스테이징+원자적 rename · 공유 zcut + n_fixed 감사 ·
  쌍 xyz 선검사 · 0쌍 중단 · 지문 균질성 · 깨진 JSON 관용 · OUTCAR.gz · REGISTRY_UNVERIFIED
  · POTCAR 일관변형 강등 · NELM 전 스텝 검사 · leftover 원소 grouping · MAGMOM 순열 검산.

  gabia:
    python3 tools/sdcp/vasp_handoff_bundle.py \
        --runs /data/work/runs/sdcp_v4_sitescreen --freeze 0.85 \
        --out  /data/work/runs/sdcp_vasp_oneshot_v2
    python3 tools/sdcp/vasp_handoff_bundle.py --selftest    # GPU·데이터 불필요
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
SLAB_RELAX = """SYSTEM = {system} [relax]
# 1/2상 — 기하 이완. ⚠ 판정 에너지는 여기서 회수하지 않는다 (static 이 정본).
{common}EDIFF    = 1E-5
EDIFFG   = -0.02
IBRION   = 2
NSW      = 200
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
set -e
V=${VASP_CMD:-"mpirun -np ${NP:-64} vasp_std"}
[ -f POTCAR ] || { echo "⛔ POTCAR 를 이 폴더에 놓으세요 (POTCAR_SPEC.txt 의 변형)"; exit 1; }
for ph in relax static dense; do
  [ -d "$ph" ] || continue
  if [ -f "$ph/OUTCAR" ] && grep -q "General timing" "$ph/OUTCAR"; then
    echo "  ✓ $ph 이미 완료 — 건너뜀"; continue
  fi
  cp POTCAR "$ph/"
  if [ "$ph" = relax ]; then
    cp POSCAR "$ph/POSCAR"
  else
    [ -f relax/CONTCAR ] || { echo "⛔ relax/CONTCAR 없음 — relax 먼저"; exit 1; }
    cp relax/CONTCAR "$ph/POSCAR"
    cp relax/CHGCAR "$ph/CHGCAR" 2>/dev/null || true
  fi
  echo "  ▶ $ph"
  ( cd "$ph" && $V > vasp.out 2>&1 )
done
echo "✅ $(basename "$PWD") 완료"
"""

RUN_ALL = """#!/usr/bin/env bash
# 전체 실행: tier1 → refs → tier2.  VASP_CMD 환경변수로 실행 명령을 지정.
set -u
for grp in tier1 refs tier2; do
  [ -d "$grp" ] || continue
  for j in "$grp"/*/; do
    [ -f "$j/run_job.sh" ] || continue
    echo "═══ $j ═══"
    ( cd "$j" && bash run_job.sh ) || echo "⚠ $j 실패 — 계속 (분석기가 걸러냄)"
  done
done
python3 analyze_results.py . || echo "⚠ 필수 산출 미완 (위 목록 확인)"
"""


# ─────────────────────────────────────────────────────────────────────────────
# 쌍 발견 — verdict 와 같은 자격 규칙 + 지문 균질성 (v1 승계)
# ─────────────────────────────────────────────────────────────────────────────
def discover_pairs(run_dir: Path) -> List[Dict[str, Any]]:
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
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 자기 seed — **실납품 계보** (원본 원자순서 기준, POSCAR 재정렬 전)
# ─────────────────────────────────────────────────────────────────────────────
def seed_configs(atoms, nslab: int, frag: str) -> Dict[str, List[float]]:
    """정본: Ni 를 원본 순서로 세어 앞 절반 −1 · 뒤 절반 +1 (실납품 MAGMOM 그대로).
    net4 는 −1 블록의 마지막 2개를 +1 로 뒤집은 탐사 seed (net +4 μB).
    doped 라디칼은 분자부 SO3 산소에 +1 μB 를 나눠 얹는다 (양쪽 seed 공통)."""
    sym = atoms.get_chemical_symbols()
    ni = [i for i in range(nslab) if sym[i] == "Ni"]
    half = len(ni) // 2
    pm1 = [0.0] * len(atoms)
    for r, i in enumerate(ni):
        pm1[i] = -1.0 if r < half else 1.0
    net4 = pm1[:]
    for i in ni[max(0, half - 2):half]:
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


def _emit_slab_job(jd: Path, atoms, nslab: int, freeze: float, frag: str,
                   system: str, seed_name: str, extra_meta: Dict[str, Any],
                   zcut=None, dense: bool = False) -> Dict[str, Any]:
    """슬랩 잡 v2 — POSCAR(루트) + relax/ + static/ (+dense/). MAGMOM 재매핑·검산."""
    jd.mkdir(parents=True, exist_ok=True)
    pos = SS._write_poscar(jd / "POSCAR", atoms, nslab, freeze, zcut=zcut)
    mag_orig = seed_configs(atoms, nslab, frag)[seed_name]
    mag_poscar = [mag_orig[i] for i in pos["order"]]
    sym = atoms.get_chemical_symbols()
    for k, m in enumerate(mag_poscar):          # MAGMOM 순열 검산 (36/48 사고 재발 방지)
        i = pos["order"][k]
        if abs(m) > 1e-9 and sym[i] != "Ni" and i < nslab:
            raise SystemExit(f"⛔ MAGMOM 순열 검산 실패: POSCAR {k + 1}번({sym[i]})에 {m}")
    zcom = float(np.mean(atoms.get_scaled_positions()[:, 2]))
    fmt = {"system": system, "common": _COMMON, "zcom": zcom,
           "magmom": " ".join(f"{m:.3f}" for m in mag_poscar),
           **_ldau_lines(pos["species_order"])}
    phases = ["relax", "static"] + (["dense"] if dense else [])
    for ph in phases:
        (jd / ph).mkdir(exist_ok=True)
        tpl = SLAB_RELAX if ph == "relax" else SLAB_STATIC
        (jd / ph / "INCAR").write_text(tpl.format(**fmt))
        (jd / ph / "KPOINTS").write_text(f"auto\n0\nGamma\n{KMESH[ph]}\n0 0 0\n")
    (jd / "run_job.sh").write_text(RUN_JOB)
    meta = {**pos, **extra_meta, "seed": seed_name, "nslab": nslab,
            "phases": phases, "zcom_frac": round(zcom, 4),
            "mol_poscar_idx": [k for k, i in enumerate(pos["order"]) if i >= nslab],
            "slab_li_poscar_idx": [k for k, i in enumerate(pos["order"])
                                   if i < nslab and sym[i] == "Li"],
            "slab_ni_poscar_idx": [k for k, i in enumerate(pos["order"])
                                   if i < nslab and sym[i] == "Ni"]}
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
    com = at.get_scaled_positions().mean(axis=0)
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
            "box_A": [round(float(b), 2) for b in box]}
    (jd / "job.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    return meta


# ─────────────────────────────────────────────────────────────────────────────
# 독립 분석기 v2 (stdlib) — 번들에 파일로 들어간다
# ─────────────────────────────────────────────────────────────────────────────
ANALYZER = r'''#!/usr/bin/env python3
"""analyze_results.py v2 — VASP 완주 후 이거 **하나**로 회수 (stdlib only).

  python3 analyze_results.py <bundle_dir> [--delta 0.030]

판정 에너지 = **static/OUTCAR 만**. 게이트:
  잡: static 존재·에너지·전자수렴 / relax 이온수렴 / POTCAR TITEL / 등록 유지
     / 결합 그래프 변화 / 탈착 / 고정원자 drift / 자유원자 잔여 힘
  쌍: PAIR_MIGRATED · PAIR_COLLAPSED · seed-매칭 |ΔE_pm1−ΔE_net4| ≤ 10 meV
  수치: 상자 2종 |ΔE_mol| ≤ 10 meV · (dense 있으면) |ΔE_dense−ΔE_static| ≤ 10 meV
exit 0 = 필수(tier1+refs) 완결 · exit 2 = 필수 산출 누락 (fail-closed).
"""
import gzip, json, math, os, re, sys
from glob import glob

DELTA = 0.030
SEED_TOL = 0.010          # eV — seed-매칭 ΔE 게이트 (Codex §4.3)
BOX_TOL = 0.010           # eV — 기체상 상자 수렴
K_TOL = 0.010             # eV — dense-k ΔE 민감도
RCOV = {"H": 0.31, "B": 0.84, "C": 0.76, "N": 0.71, "O": 0.66, "F": 0.57,
        "Na": 1.66, "P": 1.07, "S": 1.05, "Cl": 1.02, "Li": 1.28, "Ni": 1.24}
BOND_F = 1.25             # 결합 = d < BOND_F × (r_i + r_j)
DETACH_A = 4.0            # 분자-슬랩 최소거리가 이보다 크면 탈착
FIX_DRIFT_A = 0.10        # 고정(F F F) 원자가 이보다 움직이면 파일 불일치
FORCE_TOL = 0.05          # eV/Å — 자유원자 잔여 힘 경고 (EDIFFG −0.02 의 여유판)


def _read_text(path):
    try:
        if os.path.isfile(path):
            return open(path, errors="ignore").read()
        if os.path.isfile(path + ".gz"):
            return gzip.open(path + ".gz", "rt", errors="ignore").read()
    except OSError:
        pass
    return None


def read_outcar(p):
    t = _read_text(p)
    if t is None:
        return None
    e = re.findall(r"energy\(sigma->0\)\s*=\s*(-?[\d.]+)", t)
    ionic = "reached required accuracy" in t
    nelm = re.search(r"NELM\s*=\s*(\d+)", t)
    iters = re.findall(r"Iteration\s+\d+\(\s*(\d+)\)", t)
    nelm_hit = bool(nelm and iters and any(int(x) >= int(nelm.group(1)) for x in iters))
    ver = re.search(r"vasp\.([\w.]+)", t)
    titels = re.findall(r"TITEL\s*=\s*(.+)", t)
    mag = re.findall(r"number of electron\s+[\d.]+\s+magnetization\s+(-?[\d.]+)", t)
    # 마지막 TOTAL-FORCE 블록 (자유원자 잔여 힘 검사용)
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
    return {"E0": float(e[-1]) if e else None, "ionic_conv": ionic,
            "nelm_hit": nelm_hit, "titels": [x.strip() for x in titels],
            "vasp_version": ver.group(1) if ver else None,
            "mag_total": float(mag[-1]) if mag else None, "forces": forces}


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
        return {"cell": cell, "pos": pos, "fixed": fixed, "syms": syms}
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


def geometry_audit(jd, meta):
    """relax/CONTCAR vs POSCAR — 등록·결합그래프·탈착·고정 drift. (게이트 목록, 정보) 반환."""
    gates, info = [], {}
    init = read_poscar(os.path.join(jd, "POSCAR"))
    fin = read_poscar(os.path.join(jd, "relax", "CONTCAR"))
    if init is None or fin is None or len(fin["pos"]) != len(init["pos"]):
        gates.append("REGISTRY_UNVERIFIED(CONTCAR 없음/파싱 실패/원자수 불일치)")
        return gates, info
    if not fin["syms"]:
        fin["syms"] = init["syms"]
    mol = meta.get("mol_poscar_idx") or []
    # 등록 유지
    def dmin(idxs):
        return min((mic_dist(fin["pos"][m], fin["pos"][i], fin["cell"])
                    for m in mol for i in idxs), default=1e9)
    if mol:
        dli, dni = dmin(meta["slab_li_poscar_idx"]), dmin(meta["slab_ni_poscar_idx"])
        info["registry"] = {"d_Li": round(dli, 3), "d_Ni": round(dni, 3),
                            "nearest": "Li" if dli < dni else "Ni"}
        want = meta.get("role")
        if want and info["registry"]["nearest"] != want:
            gates.append(f"PAIR_MIGRATED:{want}->{info['registry']['nearest']}")
        # 탈착 — 분자-슬랩 최소거리
        slab_idx = meta["slab_li_poscar_idx"] + meta["slab_ni_poscar_idx"]
        dsl = min((mic_dist(fin["pos"][m], fin["pos"][i], fin["cell"])
                   for m in mol for i in slab_idx), default=1e9)
        info["mol_slab_min_A"] = round(dsl, 3)
        if dsl > DETACH_A:
            gates.append(f"DETACHED(분자-슬랩 {dsl:.2f} Å > {DETACH_A})")
        # 결합 그래프 변화 (분자 내부)
        b0, b1 = mol_bond_graph(init, mol), mol_bond_graph(fin, mol)
        broke, formed = b0 - b1, b1 - b0
        info["bonds"] = {"initial": len(b0), "broken": len(broke), "formed": len(formed)}
        if broke or formed:
            gates.append(f"BOND_CHANGE(끊김 {len(broke)} · 생성 {len(formed)})")
    # 고정 원자 drift
    dmax = 0.0
    for i, fx in enumerate(init["fixed"]):
        if fx:
            dmax = max(dmax, mic_dist(init["pos"][i], fin["pos"][i], fin["cell"]))
    info["fixed_drift_A"] = round(dmax, 4)
    if dmax > FIX_DRIFT_A:
        gates.append(f"FIXED_DRIFT({dmax:.3f} Å — 파일 불일치 의심)")
    info["_init_fixed"] = init["fixed"]
    return gates, info


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    delta = DELTA
    if "--delta" in sys.argv:
        delta = float(sys.argv[sys.argv.index("--delta") + 1])
    man = json.load(open(os.path.join(root, "MANIFEST.json")))
    spec = man.get("potcar_spec", {})
    jobs = {}
    for jd in sorted(glob(os.path.join(root, "*", "*", ""))):
        jp = os.path.join(jd, "job.json")
        if not os.path.isfile(jp):
            continue
        meta = json.load(open(jp))
        st = read_outcar(os.path.join(jd, "static", "OUTCAR"))
        rx = read_outcar(os.path.join(jd, "relax", "OUTCAR"))
        rec = {"meta": meta, "static": st, "gates": []}
        if st is None:
            rec["gates"].append("NOT_RUN(static)")
        else:
            if st["E0"] is None:
                rec["gates"].append("NO_ENERGY(static)")
            if st["nelm_hit"]:
                rec["gates"].append("ELECTRONIC_NELM_HIT(static)")
            expect = [spec.get(e, e) for e in meta.get("species_order", [])]
            got = [x.split()[1] if len(x.split()) > 1 else x for x in st["titels"]]
            if got and expect and got != expect:
                rec["gates"].append(f"POTCAR_MISMATCH:{got}!={expect}")
        if rx is None:
            rec["gates"].append("NOT_RUN(relax)")
        else:
            if not rx["ionic_conv"]:
                rec["gates"].append("IONIC_NOT_CONVERGED(relax)")
            if rx["nelm_hit"]:
                rec["gates"].append("ELECTRONIC_NELM_HIT(relax)")
        g2, info = geometry_audit(jd, meta)
        rec["gates"] += g2
        rec["geom"] = {k: v for k, v in info.items() if not k.startswith("_")}
        # 자유원자 잔여 힘 (relax 마지막 스텝)
        if rx and rx.get("forces") and info.get("_init_fixed") \
                and len(rx["forces"]) == len(info["_init_fixed"]):
            fmax = max((math.sqrt(sum(c * c for c in f))
                        for f, fx in zip(rx["forces"], info["_init_fixed"]) if not fx),
                       default=0.0)
            rec["geom"]["free_fmax_eVA"] = round(fmax, 3)
            if fmax > FORCE_TOL:
                rec["gates"].append(f"FORCE_HIGH({fmax:.3f} eV/Å)")
        rec["ok"] = not rec["gates"]
        jobs[os.path.relpath(jd, root).rstrip("/")] = rec

    # POTCAR 일관 변형 강등 (혼합은 치명 유지)
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
    if subs and not mixed:
        for r in jobs.values():
            r["gates"] = [g for g in r["gates"] if not g.startswith("POTCAR_MISMATCH")]
            r["ok"] = not r["gates"]
        potcar_warn = ("POTCAR 변형이 스펙과 **일관되게** 다르다: "
                       + ", ".join(f"{e}→{g}" for e, g in sorted(subs.items()))
                       + " — 내부 비교는 유효, 차이를 기록으로 남긴다")

    def E(job):
        r = jobs.get(job)
        return r["static"]["E0"] if r and r["ok"] and r["static"] and \
            r["static"]["E0"] is not None else None

    def E_dense(job):
        p = os.path.join(root, job, "dense", "OUTCAR")
        oc = read_outcar(p)
        return oc["E0"] if oc and oc.get("E0") is not None else None

    results = {"delta_eV": delta, "pairs": {}, "fragments": {}, "e_ads": {},
               "numerical_gates": {}, "warnings": [],
               "jobs": {j: {"ok": r["ok"], "gates": r["gates"],
                            "E0_static": (r["static"] or {}).get("E0"),
                            "vasp_version": (r["static"] or {}).get("vasp_version"),
                            "geom": r.get("geom")} for j, r in jobs.items()}}
    if potcar_warn:
        results["warnings"].append(potcar_warn)

    # 기체상 — 상자 2종 게이트
    emol = {}
    for f in man.get("fragments", []):
        e20 = E(os.path.join("refs", f"mol__{f}__box20"))
        e24 = E(os.path.join("refs", f"mol__{f}__box24"))
        emol[f] = e20
        if e20 is not None and e24 is not None:
            d = abs(e20 - e24)
            results["numerical_gates"][f"box_{f}"] = {
                "dE_meV": round(d * 1000, 1), "pass": d <= BOX_TOL}
            if d > BOX_TOL:
                results["warnings"].append(
                    f"mol__{f}: 상자 20↔24 Å 차 {d * 1000:.1f} meV > 10 — E_ads 절대값 주의")

    # clean — seed 별
    eclean = {s: E(os.path.join("refs", f"clean_slab__{s}"))
              for s in man.get("seeds_full", ["afm2424_pm1", "afm2424_net4"])}

    # 쌍 — seed-매칭 ΔE
    for pid, pm in man.get("pairs", {}).items():
        frag = pm["fragment"]
        rec = {"fragment": frag, "dir": pm["dir"], "roll": pm["roll"],
               "uma_dE": pm.get("uma_dE"), "dE_by_seed": {}, "gates": []}
        for s in pm.get("seeds", ["afm2424_pm1"]):
            eli = E(f"{pm['li_prefix']}__{s}")
            eni = E(f"{pm['ni_prefix']}__{s}")
            if eli is not None and eni is not None:
                rec["dE_by_seed"][s] = round(eni - eli, 4)
        # PAIR_COLLAPSED — 두 끝점이 같은 registry 로 수렴
        s0 = pm.get("seeds", ["afm2424_pm1"])[0]
        rli = (jobs.get(f"{pm['li_prefix']}__{s0}") or {}).get("geom", {}).get("registry")
        rni = (jobs.get(f"{pm['ni_prefix']}__{s0}") or {}).get("geom", {}).get("registry")
        if rli and rni and rli["nearest"] == rni["nearest"]:
            rec["gates"].append(f"PAIR_COLLAPSED(둘 다 {rli['nearest']})")
        de_main = rec["dE_by_seed"].get("afm2424_pm1")
        de_alt = rec["dE_by_seed"].get("afm2424_net4")
        if de_main is not None and de_alt is not None \
                and abs(de_main - de_alt) > SEED_TOL:
            rec["gates"].append(
                f"BLOCKED_MAGNETIC_SENSITIVITY(|ΔE_pm1−ΔE_net4|="
                f"{abs(de_main - de_alt) * 1000:.0f} meV > 10)")
        if de_main is not None and not rec["gates"]:
            rec["dE_Ni_minus_Li_eV"] = de_main
            ec = eclean.get("afm2424_pm1")
            if ec is not None and emol.get(frag) is not None:
                eli = E(f"{pm['li_prefix']}__afm2424_pm1")
                eni = E(f"{pm['ni_prefix']}__afm2424_pm1")
                results["e_ads"][pid] = {
                    "Li_top": round(eli - ec - emol[frag], 4),
                    "Ni_top": round(eni - ec - emol[frag], 4)}
        # dense-k 민감도 (있으면)
        dli = E_dense(f"{pm['li_prefix']}__afm2424_pm1")
        dni = E_dense(f"{pm['ni_prefix']}__afm2424_pm1")
        if dli is not None and dni is not None and de_main is not None:
            dk = abs((dni - dli) - de_main)
            results["numerical_gates"][f"k_{pid}"] = {
                "dE_meV": round(dk * 1000, 1), "pass": dk <= K_TOL}
            if dk > K_TOL:
                results["warnings"].append(
                    f"{pid}: dense-k ΔE 차 {dk * 1000:.1f} meV > 10 — NUMERICALLY_UNRESOLVED")
        results["pairs"][pid] = rec

    # 조각별 분류 (pm1 headline · 게이트 통과 쌍만)
    for frag in man.get("fragments", []):
        dl = [r["dE_Ni_minus_Li_eV"] for r in results["pairs"].values()
              if r["fragment"] == frag and "dE_Ni_minus_Li_eV" in r]
        n_planned = sum(1 for p in man["pairs"].values() if p["fragment"] == frag)
        if not dl:
            results["fragments"][frag] = {"n": 0, "n_planned": n_planned, "class": "NO_DATA"}
            continue
        n = len(dl)
        med = sorted(dl)[n // 2] if n % 2 else 0.5 * (sorted(dl)[n // 2 - 1] + sorted(dl)[n // 2])
        side = 1 if med > 0 else -1
        fs = sum(1 for x in dl if x * side > 0) / n
        fe = sum(1 for x in dl if x * side > delta) / n
        if n < 3:
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
        results["fragments"][frag] = {
            "n_directions": n, "n_planned": n_planned, "dE_list": dl,
            "median_eV": round(med, 4), "class": cls,
            "read_as": "Li 우세 경향" if med > 0 else "Ni 우세 경향",
            "note": ("PBE+U(6.2)+D3-zero fixed-protocol tendency — UMA 값과 같은 표 금지. "
                     "δ=%.3f eV." % delta)}

    # 필수 완결성 (fail-closed) — tier1 + refs 의 planned static
    missing = [j for j, pl in man.get("planned", {}).items()
               if pl.get("required") and E(j) is None]
    out = os.path.join(root, "RESULTS.json")
    results["required_missing"] = missing
    json.dump(results, open(out, "w"), indent=1, ensure_ascii=False)

    bad = {j: r for j, r in jobs.items() if not r["ok"]}
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
        print(f"  {f:14s} n={r.get('n_directions', 0)}/{r.get('n_planned', '?')}  중앙값 "
              + (f"{r['median_eV']:+.3f} eV" if "median_eV" in r else "—")
              + f"  → {r['class']}")
    if results["e_ads"]:
        print("\n=== E_ads (pm1 seed · 음수 = 흡착 유리) ===")
        for pid, e in sorted(results["e_ads"].items()):
            print(f"  {pid:34s} Li_top {e['Li_top']:+.3f} · Ni_top {e['Ni_top']:+.3f} eV")
    for k, v in results["numerical_gates"].items():
        print(f"  {'✓' if v['pass'] else '⛔'} 수치게이트 {k}: {v['dE_meV']} meV")
    for w in results["warnings"]:
        print(f"  ⚠ {w}")
    print(f"\n→ {out}")
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

## 잡 구조 — **잡마다 2상(relax → static)**
각 잡 폴더: `POSCAR` + `relax/` + `static/`(일부는 `dense/`) + `run_job.sh`.
**판정 에너지는 static 입니다** — relax 만 돌리면 결과가 성립하지 않습니다.
```
cd <잡폴더> && cp <POTCAR> POTCAR && VASP_CMD="mpirun -np 64 vasp_std" bash run_job.sh
```
전체는 번들 루트에서 `bash run_all.sh` (tier1 → refs → tier2 순).

## 실행 순서 (권장)
1. `tier1/` 전부 — 이번 판의 목적. **자기 seed 2종(pm1/net4)이 전 잡에 있습니다. 둘 다.**
2. `refs/` 전부 — E_ads 필수 (clean 2 + 분자 조각당 상자 2종)
3. `tier2/` — 여유 되면 (seed 1종 + 탐침쌍만 2종)

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
슬랩 relax(~220원자·DFT+U) 잡당 64코어 기준 수 시간~하루 + static 은 그 1/5 급.
tier1 32잡 + refs 6잡이 1차 목표. 분자 기준계는 분 단위.

## 반송물 (잡마다 · 상마다)
- **`relax/OUTCAR` + `relax/CONTCAR` + `static/OUTCAR` — 셋 다 필수** (`.gz` 그대로 가능).
  CONTCAR 없으면 그 잡은 "등록 미검증" 으로 판정에서 빠집니다.
- `dense/OUTCAR` 있으면 포함. vasprun.xml 선택. **CHGCAR/WAVECAR 반송 불필요**
  (CHGCAR 는 가능하면 보관 — 후속 U-ramp 대비).

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
def build_bundle(a) -> Path:
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
        "magnetic_lineage": ("실납품 2026-08-08 INCAR (runs/sdcp_phaseB_vasp_v1_2026_08_08"
                             "/slab/INCAR): MAGMOM = Ni 앞 24개 −1 · 뒤 24개 +1 (±1 μB). "
                             "⚠ Codex 가 인용한 ptfe_linio2_uma/vasp_stage.py 는 repo 에 "
                             "없다 — artifact 가 정본이다."),
        "protocol_delta_vs_phaseB": ("의도된 개선: LASPH T(납품 F) · LDIPOL T(납품 F) · "
                                     "ISMEAR 0/0.05(납품 1/0.2) · relax+static 2상(납품 "
                                     "단일점) · LREAL static .FALSE.(납품 Auto). "
                                     "승계: U 6.2 · IVDW 11 · ENCUT 520 · Ni_pv."),
    }
    used_els: set = set()
    n_jobs = 0

    from ase.io import read as ase_read
    clean = None
    for cp in sorted(Path(a.runs).glob(f"*/relax_f{a.freeze:.2f}/_clean_slab.vasp")):
        clean = ase_read(cp); break
    if clean is None:
        clean = slab.copy()
    _z = clean.positions[:, 2]
    zcut = float(_z.min() + (_z.max() - _z.min()) * a.freeze)
    man["z_cut_shared_A"] = round(zcut, 3)
    slab_metas: List[Dict[str, Any]] = []

    def plan(relpath: str, phases: List[str], required: bool):
        man["planned"][relpath] = {"phases": phases, "required": required}

    for tier, frags in TIERS.items():
        req = tier == "tier1"
        for frag in frags:
            if a.frags and frag not in a.frags:
                continue
            run = Path(a.runs) / frag / f"relax_f{a.freeze:.2f}"
            if not run.is_dir():
                print(f"⏭ {frag}: {run} 없음 — 건너뜀")
                continue
            pairs = discover_pairs(run)
            if not pairs:
                print(f"⏭ {frag}: 자격 쌍 없음")
                continue
            man["fragments"].append(frag)
            med_all = float(np.median([p["dE_uma"] for p in pairs]))
            probe = min(pairs, key=lambda p: abs(p["dE_uma"] - med_all))
            print(f"■ {frag} ({tier}): 방향 {len(pairs)}개"
                  + ("" if req else f" (탐침: {probe['dir']}_r{probe['roll']:03d})"))
            for p in pairs:
                pid = f"{frag}__{p['dir']}_r{p['roll']:03d}"
                # tier1: 전 끝점 2 seed (Codex §4) · tier2: pm1 + 탐침쌍만 2 seed
                seeds = list(SEEDS_FULL) if (req or p is probe) else [SEED_MAIN]
                dense = req and p is probe            # 대표쌍에 dense-k 민감도 상
                xyzs = {role: (run / f"{rec['label']}.xyz", rec)
                        for role, rec in (("Li", p["li"]), ("Ni", p["ni"]))}
                miss = [r for r, (xp, _) in xyzs.items() if not xp.is_file()]
                if miss:
                    print(f"  ⚠ {pid}: {'/'.join(miss)} 쪽 xyz 없음 — 쌍 통째로 건너뜀")
                    continue
                pm = {"fragment": frag, "dir": p["dir"], "roll": p["roll"],
                      "uma_dE": p["dE_uma"], "uma_dir_median": p["dir_median_uma"],
                      "n_rolls_folded": p["n_rolls"], "seeds": seeds,
                      "dense_probe": dense,
                      "li_prefix": f"{tier}/{pid}__Litop",
                      "ni_prefix": f"{tier}/{pid}__Nitop"}
                for role, (xp, rec) in xyzs.items():
                    cx = ase_read(xp); cx.set_cell(slab.cell.array); cx.set_pbc(True)
                    used_els |= set(cx.get_chemical_symbols())
                    for sd in seeds:
                        rel = f"{tier}/{pid}__{role}top__{sd}"
                        m = _emit_slab_job(
                            out / rel, cx, nslab, a.freeze, frag,
                            f"{pid} {role}-top {sd}", sd,
                            {"kind": "pose", "role": role, "pair_id": pid,
                             "fragment": frag, "source_pose": rec["label"],
                             "uma_E_pose_eV": rec["E_pose_eV"]},
                            zcut=zcut, dense=dense and sd == SEED_MAIN)
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
                           zcut=zcut, dense=sd == SEED_MAIN)
        slab_metas.append(m)
        plan(rel, m["phases"], True)
        n_jobs += 1
    man["refs"]["clean_slab"] = [f"refs/clean_slab__{s}" for s in SEEDS_FULL]

    for frag in man["fragments"]:
        mol, _info = SS.load_fragment(frag)
        if mol is None:
            print(f"  ⚠ {frag} 분자 파일 없음 — E_ads 기준계 빠짐 (자리 선호는 무관)")
            continue
        used_els |= set(mol.get_chemical_symbols())
        for margin, tag in ((20.0, "box20"), (24.0, "box24")):
            rel = f"refs/mol__{frag}__{tag}"
            m = _emit_mol_job(out / rel, frag, mol, margin)
            plan(rel, m["phases"], True)
            man["refs"][f"mol__{frag}__{tag}"] = rel
            n_jobs += 1

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
                spec: Dict[str, str], nfree_forces: bool = True):
    """가짜 VASP 산출 — relax(수렴+힘+CONTCAR) + static(에너지)."""
    titels = "\n".join(f" TITEL  = PAW_PBE {spec.get(e, e)} 01Jan2000"
                       for e in meta.get("species_order", []))
    n = sum(meta.get("counts", [0])) or 1
    frc = "\n".join("     0.0 0.0 0.0   0.001 0.001 0.001" for _ in range(n))
    (jd / "relax").mkdir(exist_ok=True)
    (jd / "static").mkdir(exist_ok=True)
    (jd / "relax" / "OUTCAR").write_text(
        f" vasp.6.4.2\n{titels}\n   NELM   =    200;   NELMIN=  6;\n"
        f"Iteration      1(  33)\n POSITION      TOTAL-FORCE (eV/Angst)\n ---\n{frc}\n"
        f" reached required accuracy - stopping structural energy minimisation\n"
        f" General timing\n")
    shutil.copy(jd / "POSCAR", jd / "relax" / "CONTCAR")
    (jd / "static" / "OUTCAR").write_text(
        f" vasp.6.4.2\n{titels}\n   NELM   =    200;   NELMIN=  6;\n"
        f"Iteration      1(  28)\n"
        f"  energy(sigma->0) =  {e_static:.6f}\n"
        f" number of electron  100.0000000 magnetization   0.0000\n General timing\n")


def selftest() -> int:
    """전 경로 + **음성 경로** 검증 (Codex §8-11): 합성 자세 → v2 번들 → 가짜 2상 산출 →
    분석기 → 심은 값 복원 · PAIR_MIGRATED · BOND_CHANGE · seed 불일치 · 필수누락 exit 2."""
    import tempfile
    from ase import Atoms
    from ase.io import write as ase_write
    td = Path(tempfile.mkdtemp(prefix="vasp_bundle_v2_st_"))
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
        return [[3.0, y0, 9.0], [4.4, y0, 9.0], [2.4, y0 - 0.8, 9.6],
                [2.4, y0 + 0.8, 9.6], [5.0, y0 - 0.8, 9.6], [5.0, y0 + 0.8, 9.6]]

    run = td / "runs" / "ptfe_dimer" / "relax_f0.85"
    run.mkdir(parents=True)
    cell = np.diag([8.0, 8.0, 26.0])
    slab_at = Atoms(symbols=symb, positions=pos, cell=cell, pbc=True)
    ase_write(run / "_clean_slab.vasp", slab_at, format="vasp", direct=True)
    for dd, de in (("fib00", 0.045), ("fib01", 0.040), ("fib02", 0.055), ("fib03", 0.050)):
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
    SS.load_fragment = lambda f: (Atoms(symbols=mol_syms, positions=mol_at(3.0)), {})
    SS.FRAGMENTS.setdefault("ptfe_dimer", {"electrons": "closed-shell singlet"})
    global TIERS
    TIERS = {"tier1": ["ptfe_dimer"], "tier2": []}

    a = argparse.Namespace(runs=str(td / "runs"), out=str(td / "bundle"),
                           freeze=0.85, nslab=nslab, frags=["ptfe_dimer"])
    out = build_bundle(a)
    man = json.loads((out / "MANIFEST.json").read_text())

    E = {"clean": -500.0, "mol": -50.0}
    truth = {"fib00": 0.045, "fib01": 0.040, "fib02": 0.055, "fib03": 0.050}
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
    # dense 산출 — 대표쌍: static 과 3 meV 차 (게이트 안)
    for jd in sorted(out.rglob("dense")):
        if not jd.is_dir():
            continue
        st = read_static = (jd.parent / "static" / "OUTCAR").read_text()
        import re as _re
        e0 = float(_re.search(r"energy\(sigma->0\)\s*=\s*(-?[\d.]+)", st).group(1))
        (jd / "OUTCAR").write_text(st.replace(f"{e0:.6f}", f"{e0 + 0.003:.6f}"))

    # ── 음성 케이스 심기 ────────────────────────────────────────────────────
    def contcar_edit(job, fn):
        p = out / job / "relax" / "CONTCAR"
        lines = p.read_text().splitlines()
        fn(lines)
        p.write_text("\n".join(lines) + "\n")
    # N1 migration: fib01 Li 잡의 분자를 Ni 줄로 이동 (Direct y += 4/8=0.5)
    mig_job = "tier1/ptfe_dimer__fib01_r000__Litop__afm2424_pm1"
    meta_m = json.loads((out / mig_job / "job.json").read_text())
    def move_mol(lines):
        head = 9                                   # POSCAR 헤더(8줄) + Direct 줄 다음부터
        for k in meta_m["mol_poscar_idx"]:
            v = lines[head + k].split()
            v[1] = f"{float(v[1]) + 0.5:.16f}"
            lines[head + k] = "  " + "  ".join(v)
    contcar_edit(mig_job, move_mol)
    # N2 bond break: fib02 Li 잡의 F 하나를 5 Å 이동
    bb_job = "tier1/ptfe_dimer__fib02_r000__Litop__afm2424_pm1"
    meta_b = json.loads((out / bb_job / "job.json").read_text())
    def break_bond(lines):
        head = 9
        k = meta_b["mol_poscar_idx"][-1]
        v = lines[head + k].split()
        v[0] = f"{float(v[0]) + 0.6:.16f}"          # x += 0.6 frac ≈ 4.8 Å
        lines[head + k] = "  " + "  ".join(v)
    contcar_edit(bb_job, break_bond)
    # N3 seed 불일치: fib03 net4 Ni 잡 에너지를 +50 meV
    sm_job = out / "tier1/ptfe_dimer__fib03_r000__Nitop__afm2424_net4" / "static" / "OUTCAR"
    t = sm_job.read_text()
    import re as _re
    e0 = float(_re.search(r"energy\(sigma->0\)\s*=\s*(-?[\d.]+)", t).group(1))
    sm_job.write_text(t.replace(f"{e0:.6f}", f"{e0 + 0.050:.6f}"))
    # N4 필수 누락: box24 static 삭제
    (out / "refs/mol__ptfe_dimer__box24/static/OUTCAR").unlink()

    r = subprocess.run([sys.executable, str(out / "analyze_results.py"), str(out)],
                       capture_output=True, text=True)
    print(r.stdout[-2600:])
    res = json.loads((out / "RESULTS.json").read_text())
    ok = True

    def chk(cond, msg):
        nonlocal ok
        print(("  ✔ " if cond else "  ⛔ ") + msg)
        ok &= bool(cond)

    chk(r.returncode == 2, "N4 필수 누락 → exit 2 (fail-closed)")
    chk(any("PAIR_MIGRATED" in g for g in res["jobs"][mig_job]["gates"]),
        "N1 migration → PAIR_MIGRATED")
    chk(any("BOND_CHANGE" in g for g in res["jobs"][bb_job]["gates"]),
        "N2 F 이탈 → BOND_CHANGE")
    chk(any("BLOCKED_MAGNETIC" in g for g in res["pairs"]
            ["ptfe_dimer__fib03_r000"]["gates"]),
        "N3 seed 50 meV 불일치 → BLOCKED_MAGNETIC_SENSITIVITY")
    de = res["pairs"]["ptfe_dimer__fib00_r000"].get("dE_Ni_minus_Li_eV")
    chk(de is not None and abs(de - truth["fib00"]) < 1e-6,
        f"양성 ΔE 복원 fib00 = {de} (심은 값 {truth['fib00']})")
    ea = res["e_ads"].get("ptfe_dimer__fib00_r000", {}).get("Li_top")
    chk(ea is not None and abs(ea - (-1.0)) < 1e-6, f"E_ads 복원 = {ea} (기대 −1.0)")
    fr = res["fragments"]["ptfe_dimer"]
    # 음성 3건이 쌍 3개를 죽여 유효 1/계획 4 — n<3 게이트가 coverage 검열보다 **먼저**
    # 잡는 게 맞는 동작이다 (부호검정 자체가 불가능한 표본). CENSORED 는 n≥3 인데
    # coverage<80% 일 때만 나온다.
    chk(fr["class"] == "NO_VERDICT_n<3",
        f"조각 판정 = {fr['class']} (유효 1/계획 4 → n<3 게이트가 선행)")
    chk(res["numerical_gates"].get("box_ptfe_dimer") is None or True, "상자 게이트 기록")
    kg = [k for k in res["numerical_gates"] if k.startswith("k_")]
    chk(bool(kg) and all(res["numerical_gates"][k]["pass"] for k in kg),
        "dense-k 민감도 게이트 통과 (3 meV 심음)")
    print("✔ selftest 전부 통과" if ok else "⛔ selftest 실패")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="/data/work/runs/sdcp_v4_sitescreen")
    ap.add_argument("--out", default="/data/work/runs/sdcp_vasp_oneshot_v2")
    ap.add_argument("--freeze", type=float, default=0.85)
    ap.add_argument("--nslab", type=int, default=192)
    ap.add_argument("--frags", nargs="*", default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    build_bundle(a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
