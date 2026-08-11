#!/usr/bin/env python3
"""vasp_handoff_bundle.py — VASP 외주 **원샷** 번들: 자세 쌍 + 기준계 + 회수 분석기 + zip.

⛔⛔ 2026-08-11 Codex 재검토 **HOLD — 이 판(v1)으로 외주 발송 금지.**
  v2 필수 반영 (kb/reviews/vasp_bundle_codex_reply_2026_08_11.md 체크리스트):
   ① relax 만으로 끝냄 → **pre-SCF → relax(2×3×1) → final static(3×4×1 · LREAL=.FALSE. ·
      EDIFF=1e-6) → 민감도(4×6×1 대표쌍)** 4상 러너. 에너지는 final static 에서만 회수.
   ② afm_balanced 는 정본 계보가 아니다 → **tools/sdcp/ptfe_linio2_uma/vasp_stage.py 의
      ni_afm_signs() 12-Ni 패턴 ×4** 를 기본 seed 로 (qe_afm24_24_pm1). afm_net4 는 탐사용.
   ③ 자기 seed 는 tier1 **전 끝점 2종** + seed-매칭 ΔE (독립 min 금지) ·
      |ΔE_s1−ΔE_s2| ≤ 10 meV 게이트 · 실패 시 BLOCKED_MAGNETIC_SENSITIVITY.
   ④ 기체상: IDIPOL=4 + DIPOL(COM) · doped NUPDOWN=1 / closed NUPDOWN=0 ·
      상자 span+20/+24 Å 2종 (|ΔE_mol| ≤ 10 meV 게이트).
   ⑤ 기하 감사: 최근접 하나 → **결합 그래프 변화**(vasp_stage.py geometry_audit 재사용) ·
      PAIR_COLLAPSED · 탈착 · 고정원자 drift · Ni 모멘트/LDAU 점유행렬 완결성.
   ⑥ 잡 수 정정: pose 46 + refs 6 = **52** (요청문의 58 은 오산).
  δ=30 meV 는 'practical indifference floor' 로 유지 (Codex 동의) + 수치 게이트 3종.

왜 이 도구인가 (2026-08-11)
  기존 `site_screen.py dft-handoff` 는 자세 쌍(POSCAR/INCAR)만 내보냈다. 그러면:
    · **E_ads(흡착에너지)를 못 낸다** — 깨끗한 슬랩·기체상 분자 기준계 잡이 없다
    · 회수 판정(수렴·등록 유지·자기상태 일관성·유한설계 분류)을 우리가 손으로 해야 한다
    · 외주와 두 번 왕복하게 된다 — "기준계도 돌려 주세요" 가 반드시 두 번째 메일이 된다
  한 번 보내면 끝나야 한다. 그래서 이 도구는 **잡 + 기준계 + 독립 분석기 + 매니페스트**를
  한 zip 에 담는다. 분석기(analyze_results.py)는 **표준 라이브러리만** 쓴다 —
  받는 쪽 클러스터에서도, 우리 쪽에서도 `python3 analyze_results.py <dir>` 하나로 돈다.

무엇이 나오나
  bundle/
    tier1/<frag>__<dir>_r<roll>__{Li,Ni}top__<mag>/   POSCAR·INCAR·KPOINTS·job.json
    tier2/…                                           (보조 조각 — 선택 실행)
    refs/clean_slab__<mag>/                           E_ads 기준 ① (같은 selective dynamics)
    refs/mol__<frag>/                                 E_ads 기준 ② (기체상, Γ-only, U·쌍극자 없음)
    analyze_results.py    ← 완주 후 이거 하나로 site preference + E_ads + 게이트 전부
    README_REQUEST.md · POTCAR_SPEC.txt · MANIFEST.json
  + bundle.zip

쌍 선택 규칙 (verdict 와 동일한 자격 규칙)
  · Li_top ↔ Ni_top 이 같은 (down_dir, roll) 로 짝지어지고, **최종 registry 가 시작 자리와
    일치**(nearest_cation Li/Ni)하는 쌍만 자격이 있다.
  · roll 변형은 독립 표본이 아니다 — **방향(down_dir)마다 하나**, 그 방향의 ΔE 중앙값에
    가장 가까운 roll 을 대표로 뽑는다.
  · 자기 초기값 2종(afm_balanced/afm_net4)은 **대표 1쌍에만** 걸고(자기상태 탐침),
    나머지 쌍은 afm_balanced 하나로 돈다 — 비용을 절반으로 줄이면서 자기상태
    민감도는 잃지 않는다 (탐침 쌍에서 두 초기값이 30 meV 넘게 갈리면 전체 재검토).

  gabia 에서:
    python3 tools/sdcp/vasp_handoff_bundle.py \
        --runs /data/work/runs/sdcp_v4_sitescreen --freeze 0.85 \
        --out  /data/work/runs/sdcp_vasp_oneshot_v1
    python3 tools/sdcp/vasp_handoff_bundle.py --selftest    # 어디서든 (GPU·데이터 불필요)
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
import site_screen as SS                      # noqa: E402  (단일 출처: 게이트·POSCAR·MAGMOM)

TIERS = {  # 판정 시급도 순 — tier1 이 이번 판의 목적(미해결 경향 2건)이다
    "tier1": ["ptfe_c10", "ptfe_dimer"],
    "tier2": ["sdcp_neutral", "sdcp_doped"],
}
#: POTCAR 는 라이선스 때문에 못 넣는다 — **정확한 변형(variant)을 못 박는다.**
#: 분석기가 OUTCAR 의 TITEL 을 읽어 이 표와 대조하고, 다르면 결과에 경고를 박는다.
#: ⚠ Ni 는 **Ni_pv** — 2026-08-08 같은 외주처 납품(OUTCAR TITEL `PAW_PBE Ni_pv`)과의
#:   연속성이다. plain Ni 로 바꾸면 Phase-B 수치와 비교 불가가 되고, 스펙만 Ni 로 두면
#:   외주처가 기존 세팅(Ni_pv)을 재사용하는 순간 **전 슬랩 잡이 POTCAR_MISMATCH** 로
#:   회수에서 제외된다(자체검토 P0-2 — 58잡 돌리고 결과 0건이 되는 경로).
POTCAR_SPEC = {"Li": "Li_sv", "Ni": "Ni_pv", "O": "O", "S": "S", "C": "C", "F": "F",
               "H": "H", "B": "B", "P": "P", "Cl": "Cl", "Na": "Na_pv"}

MOL_INCAR = """SYSTEM = {system}
# 기체상 분자 기준계 — E_ads = E(pose) - E(clean slab) - E(이것).
# ⚠ 범함수·분산은 슬랩 잡과 **동일**해야 한다 (PBE + IVDW=11 zero damping).
#   U 는 없다(Ni 없음) · 쌍극자 보정 없다(중성 분자 · 큰 상자) · Γ-only.
ISTART = 0 ; ICHARG = 2
PREC   = Accurate
ENCUT  = 520
EDIFF  = 1E-6
EDIFFG = -0.02
IBRION = 2 ; NSW = 300 ; ISIF = 2
ISMEAR = 0 ; SIGMA = 0.05
ALGO   = Normal
# ⚠ LREAL 은 슬랩 잡(Auto)과 **같아야** 한다 — E_ads = E(pose) − E(clean) − E(mol) 의
#   세 성분이 다른 투영 설정이면 그 차이가 그대로 E_ads 오차가 된다. 작은 상자에
#   Auto 는 다소 과하지만 **일관성이 정밀도보다 우선**이다 (흡착에너지 표준 관행).
LREAL  = Auto
NELM   = 200
ISPIN  = 2
MAGMOM = {magmom}
IVDW   = 11
LORBIT = 11
LWAVE  = .FALSE. ; LCHARG = .FALSE.
NCORE  = 4
"""


# ─────────────────────────────────────────────────────────────────────────────
# 쌍 발견 — verdict 와 같은 자격 규칙, 방향 접기, 대표 roll 선택
# ─────────────────────────────────────────────────────────────────────────────
def discover_pairs(run_dir: Path) -> List[Dict[str, Any]]:
    """자격 있는 대조쌍을 방향마다 하나씩. [{dir, roll, li, ni, dE, n_rolls}]"""
    rows = []
    for jp in sorted(run_dir.glob("*.json")):
        if jp.name.startswith("_"):
            continue
        try:
            rows.append(json.loads(jp.read_text()))
        except ValueError:
            print(f"  ⚠ 깨진 JSON 건너뜀 (죽은 런의 반쪽 파일?): {jp.name}")
    fs = [r for r in rows if r.get("ranking_eligible") and r.get("E_pose_eV") is not None]
    # ⚠ verdict 와 같은 이유(자체검토 P1-2) — 지문이 섞인 디렉터리에서 쌍을 만들면
    #   서로 다른 프로토콜의 에너지를 한 쌍으로 비교하게 된다. 균질성 검사.
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
        # 자격: 이완 **후** registry 가 시작 자리와 일치해야 한다 (PAIR_MIGRATED 차단)
        if r.get("nearest_cation") != "Li" or q.get("nearest_cation") != "Ni":
            continue
        by_dir.setdefault(dd, []).append((float(ro), q["E_pose_eV"] - r["E_pose_eV"], r, q))
    out = []
    for dd, lst in sorted(by_dir.items()):
        med = float(np.median([de for _ro, de, _r, _q in lst]))
        ro, de, r, q = min(lst, key=lambda t: abs(t[1] - med))   # 방향 중앙값에 가장 가까운 roll
        out.append({"dir": dd, "roll": int(ro), "li": r, "ni": q,
                    "dE_uma": round(de, 4), "n_rolls": len(lst),
                    "dir_median_uma": round(med, 4)})
    return out


def _job_incar(system: str, els: List[str], mag_poscar: List[float]) -> str:
    return SS.INCAR_TEMPLATE.format(
        system=system,
        ldaul=" ".join("2" if e == "Ni" else "-1" for e in els),
        ldauu=" ".join("6.2" if e == "Ni" else "0.0" for e in els),
        ldauj=" ".join("0.0" for _ in els),
        magmom=" ".join(f"{m:.3f}" for m in mag_poscar))


def _emit_slab_job(jd: Path, atoms, nslab: int, freeze: float, frag: str,
                   system: str, mag_name: str, kmesh: str,
                   extra_meta: Dict[str, Any], zcut=None) -> Dict[str, Any]:
    """슬랩 계열 잡 하나 (pose 또는 clean). POSCAR 재정렬 → MAGMOM 재매핑 → 검산."""
    jd.mkdir(parents=True, exist_ok=True)
    pos = SS._write_poscar(jd / "POSCAR", atoms, nslab, freeze, zcut=zcut)
    mag_orig = SS._magmom_configs(atoms, nslab, frag)[mag_name]
    mag_poscar = [mag_orig[i] for i in pos["order"]]
    # ★ MAGMOM 순열 검산 — 0 아닌 모멘트는 Ni 이거나 (라디칼 씨앗이면) 분자 원자여야 한다.
    #   2026-08-11 실측: 재매핑 없이는 48개 중 36개가 Li/O 에 걸렸다. 어기면 즉사한다.
    sym = atoms.get_chemical_symbols()
    for k, m in enumerate(mag_poscar):
        i = pos["order"][k]
        if abs(m) > 1e-9 and sym[i] != "Ni" and i < nslab:
            raise SystemExit(f"⛔ MAGMOM 순열 검산 실패: POSCAR {k + 1}번({sym[i]})에 {m}")
    (jd / "INCAR").write_text(_job_incar(system, pos["species_order"], mag_poscar))
    (jd / "KPOINTS").write_text(f"auto\n0\nGamma\n{kmesh}\n0 0 0\n")
    # 분석기가 등록 유지 게이트에 쓸 인덱스 — POSCAR 기준(0-based)으로 미리 계산
    meta = {**pos, **extra_meta, "magnetic": mag_name, "nslab": nslab,
            "mol_poscar_idx": [k for k, i in enumerate(pos["order"]) if i >= nslab],
            "slab_li_poscar_idx": [k for k, i in enumerate(pos["order"])
                                   if i < nslab and sym[i] == "Li"],
            "slab_ni_poscar_idx": [k for k, i in enumerate(pos["order"])
                                   if i < nslab and sym[i] == "Ni"]}
    (jd / "job.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    return meta


def _emit_mol_job(jd: Path, frag: str, mol, vac: float = 14.0) -> Dict[str, Any]:
    """기체상 분자 기준계 — 큰 직교 상자, Γ-only, U/쌍극자 없음."""
    from ase import Atoms
    jd.mkdir(parents=True, exist_ok=True)
    p = mol.get_positions()
    p = p - p.min(axis=0)
    box = p.max(axis=0) + vac
    at = Atoms(symbols=mol.get_chemical_symbols(), positions=p + vac / 2.0,
               cell=np.diag(box), pbc=True)
    # 열린 껍질 조각(doped 라디칼)은 씨앗을 준다 — 전부 0 이면 doublet 이 닫혀 버린다
    open_shell = "DOUBLET" in SS.FRAGMENTS[frag]["electrons"].upper()
    mags = [0.0] * len(at)
    if open_shell:
        gi = SS.group_indices(at, "SO3")
        seed = [i for i in gi if at.get_chemical_symbols()[i] == "O"] or list(range(len(at)))
        for i in seed:
            mags[i] = round(1.0 / len(seed), 3)
    # ⚠ 자체검토 P2 — leftover 를 원본 순서로 idx 에 붙이면서 counts 는 정렬 순회라
    #   [Na,P,Na,S] 에서 헤더와 좌표가 어긋났다(다른 분자를 조용히 계산). 같은 순회로.
    order = ["Li", "Ni", "O", "S", "C", "F", "H"]
    sym = at.get_chemical_symbols()
    order_ext = order + sorted({x for x in sym if x not in order})
    idx = [i for el in order_ext for i in range(len(at)) if sym[i] == el]
    counts, seen = [], []
    for el in order_ext:
        n = sum(1 for i in idx if sym[i] == el)
        if n:
            counts.append(n); seen.append(el)
    lines = [f"gas-phase {frag}", "1.0"]
    lines += [f"  {v[0]:.10f} {v[1]:.10f} {v[2]:.10f}" for v in np.diag(box).reshape(3, 3)]
    lines += ["  " + "  ".join(seen), "  " + "  ".join(str(c) for c in counts), "Cartesian"]
    for i in idx:
        lines.append(f"  {at.positions[i, 0]:.10f} {at.positions[i, 1]:.10f} "
                     f"{at.positions[i, 2]:.10f}")
    (jd / "POSCAR").write_text("\n".join(lines) + "\n")
    (jd / "INCAR").write_text(MOL_INCAR.format(
        system=f"gas {frag}",
        magmom=" ".join(f"{mags[i]:.3f}" for i in idx)))
    (jd / "KPOINTS").write_text("gamma-only\n0\nGamma\n1 1 1\n0 0 0\n")
    meta = {"kind": "mol_ref", "fragment": frag, "species_order": seen, "counts": counts,
            "open_shell": open_shell, "box_A": [round(float(b), 2) for b in box]}
    (jd / "job.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    return meta


# ─────────────────────────────────────────────────────────────────────────────
# 독립 분석기 — 번들에 파일로 들어간다 (표준 라이브러리만)
# ─────────────────────────────────────────────────────────────────────────────
ANALYZER = r'''#!/usr/bin/env python3
"""analyze_results.py — VASP 완주 후 이 스크립트 **하나**로 회수한다 (stdlib only).

  python3 analyze_results.py <bundle_dir> [--delta 0.030]

산출: RESULTS.json + 표.  게이트를 통과한 값만 판정에 들어간다:
  ① 이온 수렴 (reached required accuracy) · 전자 수렴 (마지막 스텝이 NELM 미만)
  ② 등록 유지 — 이완 후에도 분자의 최근접 슬랩 양이온이 시작 라벨(Li/Ni)과 같은가
  ③ 자기 초기값 2종이 있으면 각자 낮은 쪽을 쓰고, 30 meV 넘게 갈리면 경고
  ④ POTCAR TITEL 이 스펙과 같은가 (다르면 결과에 경고 — 조용히 넘어가지 않는다)
"""
import gzip, json, math, os, re, sys
from glob import glob

DELTA = 0.030          # eV — 유한설계 분류의 실무 임계 (UMA 쪽과 같은 값·같은 규칙)
MAG_TOL = 0.030        # eV — 자기 초기값 2종 불일치 경고


def _read_text(path):
    """평문 또는 .gz — 2026-08-08 실납품이 OUTCAR.gz 였다. 둘 다 받는다."""
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
    # ⚠ 마지막 이온 스텝만 보면 **중간 스텝의 SCF 실패**가 통과한다 — 전 스텝 검사
    nelm_hit = bool(nelm and iters and any(int(x) >= int(nelm.group(1)) for x in iters))
    ver = re.search(r"vasp\.([\w.]+)", t)
    titels = re.findall(r"TITEL\s*=\s*(.+)", t)
    mag = re.findall(r"number of electron\s+[\d.]+\s+magnetization\s+(-?[\d.]+)", t)
    return {"E0": float(e[-1]) if e else None, "ionic_conv": ionic,
            "nelm_hit": nelm_hit, "titels": [x.strip() for x in titels],
            "vasp_version": ver.group(1) if ver else None,
            "mag_total": float(mag[-1]) if mag else None}


def read_contcar(p):
    """VASP CONTCAR 는 항상 Direct 로 나온다. 잘리거나 빈 파일이면 None —
    잡 하나가 회수 전체를 죽이면 안 된다 (0바이트 CONTCAR 에서 IndexError 로
    분석기가 전멸하던 것, 자체검토 P1-1)."""
    t = _read_text(p)
    if t is None:
        return None
    try:
        L = t.splitlines()
        scale = float(L[1].split()[0])
        cell = [[float(x) * scale for x in L[i].split()[:3]] for i in (2, 3, 4)]
        i = 5
        if not L[i].split()[0].isdigit():
            i += 1                                    # 종 이름 줄
        counts = [int(x) for x in L[i].split()]
        i += 1
        if L[i].strip() and L[i].strip()[0] in "Ss":
            i += 1                                    # Selective dynamics
        direct = bool(L[i].strip()) and L[i].strip()[0] in "Dd"
        i += 1
        n = sum(counts)
        pos = []
        for k in range(n):
            v = [float(x) for x in L[i + k].split()[:3]]
            if direct:
                v = [sum(v[j] * cell[j][ax] for j in range(3)) for ax in range(3)]
            else:
                v = [x * scale for x in v]            # Cartesian 은 scale 을 좌표에도
            pos.append(v)
        return {"cell": cell, "pos": pos}
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


def registry(job_dir, meta):
    """이완 후 분자의 최근접 슬랩 양이온 종 — 시작 라벨과 대조한다."""
    c = read_contcar(os.path.join(job_dir, "CONTCAR"))
    if not c or not meta.get("mol_poscar_idx"):
        return None
    def dmin(idxs):
        return min((mic_dist(c["pos"][m], c["pos"][i], c["cell"])
                    for m in meta["mol_poscar_idx"] for i in idxs), default=1e9)
    dli, dni = dmin(meta["slab_li_poscar_idx"]), dmin(meta["slab_ni_poscar_idx"])
    return {"d_Li": round(dli, 3), "d_Ni": round(dni, 3),
            "nearest": "Li" if dli < dni else "Ni"}


def classify(dl, delta):
    n = len(dl)
    if n < 3:
        return "NO_VERDICT_n<3"
    med = sorted(dl)[n // 2] if n % 2 else 0.5 * (sorted(dl)[n // 2 - 1] + sorted(dl)[n // 2])
    side = 1 if med > 0 else -1
    fs = sum(1 for x in dl if x * side > 0) / n
    fe = sum(1 for x in dl if x * side > delta) / n
    if fs >= 0.8 and fe >= 0.8:
        return "ROBUST_SCREENING"
    if fs >= 0.8 and abs(med) > delta:
        return "MARGINAL_TENDENCY"
    if fs >= 0.8:
        return "SIGN_CONSISTENT_SMALL"
    return "UNRESOLVED_MIXED"


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
        oc = read_outcar(os.path.join(jd, "OUTCAR"))
        rec = {"meta": meta, "outcar": oc, "gates": []}
        if oc is None:
            rec["gates"].append("NOT_RUN")
        else:
            if oc["E0"] is None:
                rec["gates"].append("NO_ENERGY")
            if not oc["ionic_conv"]:
                rec["gates"].append("IONIC_NOT_CONVERGED")
            if oc["nelm_hit"]:
                rec["gates"].append("ELECTRONIC_NELM_HIT")
            expect = [spec.get(e, e) for e in meta.get("species_order", [])]
            got = [t.split()[1] if len(t.split()) > 1 else t for t in oc["titels"]]
            if got and expect and got != expect:
                rec["gates"].append(f"POTCAR_MISMATCH:{got}!={expect}")
            if meta.get("mol_poscar_idx"):
                rg = registry(jd, meta)
                rec["registry_after_relax"] = rg
                want = meta.get("role")
                if want:
                    # ⛔ P0-1 — CONTCAR 가 없으면 등록유지 게이트가 **무음으로 꺼졌다**.
                    #   검증 못 했으면 못 했다고 게이트를 박는다 (통과가 아니다).
                    if rg is None:
                        rec["gates"].append("REGISTRY_UNVERIFIED(CONTCAR 없음/파싱 실패)")
                    elif rg["nearest"] != want:
                        rec["gates"].append(f"PAIR_MIGRATED:{want}->{rg['nearest']}")
        rec["ok"] = not rec["gates"]
        jobs[os.path.relpath(jd, root).rstrip("/")] = rec

    # ── POTCAR 변형: **전 잡이 일관되게** 스펙과 다른 경우는 치명 게이트가 아니라
    #   경고다 (자체검토 P0-2 — 외주처가 기존 Ni_pv 세팅을 재사용하면 58잡 전부가
    #   MISMATCH 로 제외되던 경로). 같은 원소가 잡마다 다른 변형이면(혼합) 치명 유지.
    subs, mixed = {}, False
    for r in jobs.values():
        oc = r.get("outcar") or {}
        expect = [spec.get(e, e) for e in r["meta"].get("species_order", [])]
        got = [x.split()[1] if len(x.split()) > 1 else x for x in oc.get("titels") or []]
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
                       + " — 내부 비교(ΔE·E_ads)는 유효. 스펙과의 차이를 기록으로 남긴다")

    def emin(prefix):
        """자기 초기값 여러 개 중 수렴한 것들의 최저 E0 (+불일치 폭)."""
        es = [(j, r["outcar"]["E0"]) for j, r in jobs.items()
              if j.startswith(prefix) and r["ok"] and r["outcar"]["E0"] is not None]
        if not es:
            return None, None, []
        vals = sorted(v for _j, v in es)
        return vals[0], (vals[-1] - vals[0] if len(vals) > 1 else 0.0), [j for j, _v in es]

    results = {"delta_eV": delta, "pairs": {}, "fragments": {}, "e_ads": {},
               "warnings": [], "jobs": {j: {"ok": r["ok"], "gates": r["gates"],
                                            "E0": (r["outcar"] or {}).get("E0"),
                                            "vasp_version": (r["outcar"] or {}).get("vasp_version"),
                                            "registry": r.get("registry_after_relax")}
                             for j, r in jobs.items()}}
    if potcar_warn:
        results["warnings"].append(potcar_warn)
    eclean, dclean, _ = emin(os.path.join("refs", "clean_slab"))
    emol = {}
    for f in man.get("fragments", []):
        e, _d, _ = emin(os.path.join("refs", f"mol__{f}"))
        emol[f] = e
    for pid, pm in man.get("pairs", {}).items():
        frag = pm["fragment"]
        eli, dli, _ = emin(pm["li_prefix"])
        eni, dni, _ = emin(pm["ni_prefix"])
        rec = {"fragment": frag, "dir": pm["dir"], "roll": pm["roll"],
               "uma_dE": pm.get("uma_dE"), "E_Li": eli, "E_Ni": eni,
               "mag_spread_Li": dli, "mag_spread_Ni": dni}
        if eli is not None and eni is not None:
            rec["dE_Ni_minus_Li_eV"] = round(eni - eli, 4)
            for nm, sp in (("Li", dli), ("Ni", dni)):
                if sp and sp > MAG_TOL:
                    results["warnings"].append(
                        f"{pid}/{nm}: 자기 초기값 2종이 {sp * 1000:.0f} meV 갈린다 — "
                        f"국소 모멘트를 눈으로 확인할 것")
            if eclean is not None and emol.get(frag) is not None:
                results["e_ads"][pid] = {
                    "Li_top": round(eli - eclean - emol[frag], 4),
                    "Ni_top": round(eni - eclean - emol[frag], 4)}
        results["pairs"][pid] = rec
    for frag in man.get("fragments", []):
        dl = [r["dE_Ni_minus_Li_eV"] for r in results["pairs"].values()
              if r["fragment"] == frag and "dE_Ni_minus_Li_eV" in r]
        if not dl:
            results["fragments"][frag] = {"n": 0, "class": "NO_DATA"}
            continue
        med = sorted(dl)[len(dl) // 2] if len(dl) % 2 else \
            0.5 * (sorted(dl)[len(dl) // 2 - 1] + sorted(dl)[len(dl) // 2])
        results["fragments"][frag] = {
            "n_directions": len(dl), "dE_list": dl, "median_eV": round(med, 4),
            "class": classify(dl, delta),
            "read_as": ("Li 우세 경향" if med > 0 else "Ni 우세 경향") if dl else None,
            "note": "DFT+U 판정 — UMA 값과 같은 표에 놓지 말 것. δ=%.3f eV 기준." % delta}
    out = os.path.join(root, "RESULTS.json")
    json.dump(results, open(out, "w"), indent=1, ensure_ascii=False)

    print("=== 잡 게이트 ===")
    bad = {j: r for j, r in jobs.items() if not r["ok"]}
    print(f"통과 {len(jobs) - len(bad)}/{len(jobs)}"
          + (f" · 문제 {len(bad)}건:" if bad else ""))
    for j, r in sorted(bad.items()):
        print(f"  ⛔ {j}: {', '.join(r['gates'])}")
    print("\n=== 자리 선호 (ΔE = E(Ni_top) − E(Li_top), 양수 = Li 우세) ===")
    for pid, r in sorted(results["pairs"].items()):
        de = r.get("dE_Ni_minus_Li_eV")
        print(f"  {pid:34s} " + (f"{de:+.3f} eV" if de is not None else "(미완)")
              + (f"   [UMA {r['uma_dE']:+.3f}]" if r.get("uma_dE") is not None else ""))
    print("\n=== 조각별 판정 ===")
    for f, r in results["fragments"].items():
        print(f"  {f:14s} n={r.get('n_directions', 0)}  중앙값 "
              + (f"{r['median_eV']:+.3f} eV" if "median_eV" in r else "—")
              + f"  → {r['class']}")
    if results["e_ads"]:
        print("\n=== E_ads (흡착에너지, 음수 = 흡착 유리) ===")
        for pid, e in sorted(results["e_ads"].items()):
            print(f"  {pid:34s} Li_top {e['Li_top']:+.3f} · Ni_top {e['Ni_top']:+.3f} eV")
    for w in results["warnings"]:
        print(f"  ⚠ {w}")
    print(f"\n→ {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


README = """# VASP 외주 요청 — SDCP/PTFE 자리 선호 + 흡착에너지 (원샷)

## 무엇을 계산하나
LiNiO₂(104) 슬랩 위 분자 조각의 **자리 선호**(Li_top vs Ni_top)와 **흡착에너지**.
MLIP 스크리닝은 경향까지만 냈고, 이 DFT+U 가 최종 판정입니다.

## 실행 순서 (권장)
1. `tier1/` 전부 (ptfe_c10 · ptfe_dimer — 이번 판의 목적)
2. `refs/` 전부 (**흡착에너지에 필수** — clean slab 2 + 분자 기준계)
3. `tier2/` (sdcp 2종 — 여유 되면)

각 잡 폴더에 POSCAR/INCAR/KPOINTS 가 있습니다. **POTCAR 만 붙이면 됩니다**
(라이선스 문제로 미포함 — `POTCAR_SPEC.txt` 의 변형을 정확히. 특히 **Ni 는 Ni_pv** —
2026-08-08 납품과 같은 변형입니다. 분석기가 OUTCAR TITEL 을 대조합니다).
VASP 5.4.4 또는 6.x + **PBE PAW 5.4 세트**를 권장합니다.

## 예상 비용 (참고)
슬랩 잡(~220원자·DFT+U·이완) 1개당 64코어 기준 대략 **수 시간~하루**.
tier1 20잡 + refs 6잡이 1차 목표입니다. 분자 기준계는 분 단위입니다.

## ⚠ 지켜야 결과가 성립하는 것
- **INCAR 를 수정하지 말 것** — Li_top/Ni_top 쌍은 모든 설정이 같아야 ΔE 가 의미 있습니다.
  (예외 ①: NCORE/KPAR/NSIM 등 병렬 설정은 자유)
  (예외 ② — **SCF 가 안 붙을 때만**, 사전 승인된 사다리를 순서대로:
     1) `ALGO = All`   2) `AMIX = 0.1 · BMIX = 0.0001 · AMIX_MAG = 0.2 · BMIX_MAG = 0.0001`
   무엇을 썼는지 그 잡 폴더에 `NOTES.txt` 로 남겨 주세요. 이걸로도 안 되면 그 잡은
   중단하고 알려 주세요 — 다른 설정을 임의로 바꾸지 말아 주세요.)
- `__afm_balanced` / `__afm_net4` 는 같은 구조의 **자기 초기값 2종**입니다(대표 쌍에만
  있음). 둘 다 돌려 주세요.
- 발산/미수렴 잡은 그대로 두고 알려 주세요.

## 반송물 (잡마다)
- **OUTCAR 와 CONTCAR — 둘 다 필수** (`.gz` 압축 그대로 보내셔도 됩니다. 분석기가 읽습니다).
  CONTCAR 가 없으면 해당 잡은 "등록 미검증" 으로 판정에서 빠집니다.
- vasprun.xml 은 선택. **CHGCAR/WAVECAR 는 반송 불필요** — CHGCAR 는 가능하면 그쪽에
  보관해 주세요 (후속 U-ramp 가 필요해질 때 요청드릴 수 있습니다).

## 완주 후
```
python3 analyze_results.py .
```
이거 하나면 수렴 게이트 → 자리 유지 검사 → ΔE/E_ads/판정까지 전부 나옵니다
(표준 라이브러리만 사용). `RESULTS.json` 과 화면 표 + 위 반송물을 보내 주시면 됩니다.

## 무결성 확인 (선택)
MANIFEST.json 의 `files_sha256_16` 과 대조: `sha256sum <파일> | cut -c1-16`

## 범위 밖 (미리 밝혀 둡니다)
변형에너지 분해(E_int/E_deform — frozen-geometry 단일점)는 이번 요청 범위 밖입니다.
필요해지면 별도로 요청드립니다.

## 프로토콜 (요약)
PBE+U(Ni d, U=6.2 Dudarev) · D3 zero damping(IVDW=11) · ENCUT 520 · ISMEAR=0/0.05
· 슬랩: 쌍극자 보정(IDIPOL=3) · 공유 고정 평면 z ≤ {zcut_note} (Selective dynamics,
아래 {freeze_pct}%) · 분자 기준계: Γ-only · U/쌍극자 없음 · 같은 범함수/분산/LREAL.
자세한 근거·출처는 MANIFEST.json 에 있습니다.
"""


# ─────────────────────────────────────────────────────────────────────────────
def build_bundle(a) -> Path:
    out_final = Path(a.out)
    if out_final.exists() and any(out_final.iterdir()):
        sys.exit(f"⛔ {out_final} 이 비어 있지 않다 — 옛 번들과 섞이면 안 된다. 새 경로를 줄 것")
    # ★ 스테이징 (자체검토 P2) — MAGMOM 검산 등으로 중간에 죽으면 옛 코드는 반쪽 번들을
    #   a.out 에 남겼고, 재실행은 '비어 있지 않다' 로 거부돼 수동 rm 을 강제했다.
    #   임시 디렉터리에 다 만들고 끝에 원자적으로 rename 한다.
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
        "gate_version": SS.gate_version(), "freeze_frac_dft": a.freeze,
        "kmesh": a.kmesh, "nslab": nslab, "potcar_spec": {},
        "fragments": [], "pairs": {}, "refs": {},
        "protocol_note": ("PBE+U(Ni 6.2, Dudarev)+D3 zero damping(IVDW=11)·LASPH·LDIPOL/"
                          "IDIPOL=3·ISMEAR=0·ENCUT 520. 자기 초기값 2종은 대표 쌍에만(탐침). "
                          "UMA E_pose 는 순위 출처일 뿐 — DFT 결과와 같은 표 금지."),
    }
    used_els: set = set()
    n_jobs = 0

    from ase.io import read as ase_read
    # ── 깨끗한 슬랩을 **먼저** 찾는다 — 전 잡이 공유할 고정 평면(zcut)을 여기서 정한다.
    #   자세마다 자기 z-범위로 재면 UMA 이완 후 표면이 뜬 자세에서 고정 원자 집합이
    #   어긋나고, 그 구속 차이가 쌍 ΔE 에 그대로 들어간다 (자체검토 P2 → 설계로 승격).
    clean = None
    for cp in sorted(Path(a.runs).glob(f"*/relax_f{a.freeze:.2f}/_clean_slab.vasp")):
        clean = ase_read(cp); break
    if clean is None:
        clean = slab.copy()
    _z = clean.positions[:, 2]
    zcut = float(_z.min() + (_z.max() - _z.min()) * a.freeze)
    man["z_cut_shared_A"] = round(zcut, 3)
    slab_metas: List[Dict[str, Any]] = []

    for tier, frags in TIERS.items():
        if a.frags and not any(f in a.frags for f in frags):
            continue
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
            probe = min(pairs, key=lambda p: abs(p["dE_uma"] - med_all))   # 자기 탐침 쌍
            print(f"■ {frag}: 방향 {len(pairs)}개 (자기 탐침: {probe['dir']}_r{probe['roll']:03d})")
            for p in pairs:
                pid = f"{frag}__{p['dir']}_r{p['roll']:03d}"
                mags = ["afm_balanced", "afm_net4"] if p is probe else ["afm_balanced"]
                pm = {"fragment": frag, "dir": p["dir"], "roll": p["roll"],
                      "uma_dE": p["dE_uma"], "uma_dir_median": p["dir_median_uma"],
                      "n_rolls_folded": p["n_rolls"], "magnetic_probe": p is probe,
                      "li_prefix": f"{tier}/{pid}__Litop", "ni_prefix": f"{tier}/{pid}__Nitop"}
                # ⚠ 두 xyz 를 **먼저** 검사한다 — 옛 코드는 Li 쪽 잡을 이미 써 놓고
                #   break 해서 고아 잡이 디스크에 남았다(외주처가 헛돈 돌린다).
                xyzs = {role: (run / f"{rec['label']}.xyz", rec)
                        for role, rec in (("Li", p["li"]), ("Ni", p["ni"]))}
                miss = [r for r, (xp, _) in xyzs.items() if not xp.is_file()]
                if miss:
                    print(f"  ⚠ {pid}: {'/'.join(miss)} 쪽 xyz 없음 — 쌍 통째로 건너뜀")
                    continue
                for role, (xp, rec) in xyzs.items():
                    cx = ase_read(xp); cx.set_cell(slab.cell.array); cx.set_pbc(True)
                    used_els |= set(cx.get_chemical_symbols())
                    for mg in mags:
                        slab_metas.append(_emit_slab_job(
                            out / tier / f"{pid}__{role}top__{mg}",
                            cx, nslab, a.freeze, frag,
                            f"{pid} {role}-top {mg}", mg, a.kmesh,
                            {"kind": "pose", "role": role, "pair_id": pid,
                             "fragment": frag, "source_pose": rec["label"],
                             "uma_E_pose_eV": rec["E_pose_eV"]}, zcut=zcut))
                        n_jobs += 1
                man["pairs"][pid] = pm

    if not man["pairs"]:
        shutil.rmtree(out)
        sys.exit("⛔ 자격 쌍이 0개다 — 번들을 만들지 않는다 "
                 "(--runs/--freeze 경로와 relax 산출물을 확인할 것)")

    # ── 기준계 ① 깨끗한 슬랩 (공유 zcut·양쪽 자기 초기값) ─────────────────────
    for mg in ("afm_balanced", "afm_net4"):
        slab_metas.append(_emit_slab_job(
            out / "refs" / f"clean_slab__{mg}", clean, len(clean), a.freeze,
            man["fragments"][0], f"clean slab {mg}", mg, a.kmesh,
            {"kind": "clean_ref"}, zcut=zcut))
        n_jobs += 1
    man["refs"]["clean_slab"] = "refs/clean_slab__{afm_balanced,afm_net4}"

    # ── 기준계 ② 기체상 분자 (조각마다 1개) ─────────────────────────────────
    for frag in man["fragments"]:
        mol, _info = SS.load_fragment(frag)
        if mol is None:
            print(f"  ⚠ {frag} 분자 파일 없음 — E_ads 기준계 빠짐 (자리 선호는 영향 없음)")
            continue
        used_els |= set(mol.get_chemical_symbols())
        _emit_mol_job(out / "refs" / f"mol__{frag}", frag, mol)
        man["refs"][f"mol__{frag}"] = f"refs/mol__{frag}"
        n_jobs += 1

    # ── 고정 원자 수 감사 — 공유 zcut 불변식이 깨졌으면 여기서 죽는 게 싸다
    nfs = sorted({m["n_fixed"] for m in slab_metas})
    if len(nfs) != 1:
        shutil.rmtree(out)
        sys.exit(f"⛔ 슬랩 잡들의 고정 원자 수가 갈린다 {nfs} — 쌍 ΔE 가 구속 차이로 "
                 f"오염된다. 자세 z-범위를 확인할 것")
    man["n_fixed_all_slab_jobs"] = nfs[0]

    man["potcar_spec"] = {e: POTCAR_SPEC.get(e, e) for e in sorted(used_els)}
    (out / "analyze_results.py").write_text(ANALYZER)
    (out / "README_REQUEST.md").write_text(README.format(
        freeze_pct=int(a.freeze * 100), zcut_note=f"{zcut:.3f} Å"))
    (out / "POTCAR_SPEC.txt").write_text(
        "# 원소 → POTCAR 변형 (PBE 5.4 권장). 이 순서가 아니라 각 잡 POSCAR 의 종 순서대로.\n"
        + "\n".join(f"{e:3s} {v}" for e, v in man["potcar_spec"].items()) + "\n")

    # sha256 매니페스트 — 받는 쪽이 전송 손상·누락을 검증할 수 있게
    files = {}
    for p in sorted(out.rglob("*")):
        if p.is_file() and p.name != "MANIFEST.json":
            files[str(p.relative_to(out))] = hashlib.sha256(p.read_bytes()).hexdigest()[:16]
    man["n_jobs"] = n_jobs
    man["files_sha256_16"] = files
    (out / "MANIFEST.json").write_text(json.dumps(man, indent=1, ensure_ascii=False))

    if out_final.exists():
        out_final.rmdir()                       # 위에서 '비어 있음' 을 확인했다
    out.rename(out_final)
    zp = out_final.with_suffix(".zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for q in sorted(out_final.rglob("*")):
            if q.is_file():
                z.write(q, q.relative_to(out_final.parent))
    print(f"\n→ {out_final}  · 잡 {n_jobs}개 · 쌍 {len(man['pairs'])}개 · 조각 {man['fragments']}")
    print(f"→ {zp}  ({zp.stat().st_size / 1e6:.1f} MB)")
    print("  ⚠ POTCAR 미포함(라이선스) — POTCAR_SPEC.txt 의 변형(Ni_pv 포함)을 정확히 쓸 것")
    return out_final


# ─────────────────────────────────────────────────────────────────────────────
def selftest() -> int:
    """GPU·실데이터 없이 전체 경로 검증: 합성 자세 → 번들 → 가짜 OUTCAR → 분석기."""
    import tempfile
    from ase import Atoms
    td = Path(tempfile.mkdtemp(prefix="vasp_bundle_st_"))
    print(f"selftest → {td}")

    # 작은 가짜 슬랩 — **꼭대기 층에 Li 줄(y≈1)과 Ni 줄(y≈5)을 나란히** 둔다.
    #   그래야 Li_top 자세(분자를 Li 줄 위에)와 Ni_top 자세(Ni 줄 위)가 등록 게이트를
    #   각자 통과한다. 첫 판 selftest 는 이걸 안 나눠서 게이트가 전부 잡았다 —
    #   게이트가 작동한다는 증명이었지만, 통과 경로도 검증해야 한다.
    pos, symb = [], []
    for i in range(8):                                   # 바닥 O 채움 (z 0–2)
        symb.append("O"); pos.append([(i % 4) * 2.0, (i // 4) * 4.0, 0.0])
        symb.append("O"); pos.append([(i % 4) * 2.0, (i // 4) * 4.0 + 2.0, 2.0])
    for i in range(8):                                   # 꼭대기 Li 줄 (y 0–2, z 6)
        symb.append("Li"); pos.append([(i % 4) * 2.0, (i // 4) * 2.0, 6.0])
    for i in range(8):                                   # 꼭대기 Ni 줄 (y 4–6, z 6)
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
    from ase.io import write as ase_write
    ase_write(run / "_clean_slab.vasp", slab_at, format="vasp", direct=True)

    # 자격 쌍 3방향 (같은 구조 재사용 — 검증 대상은 배선이지 물리가 아니다)
    for dd, de in (("fib00", 0.040), ("fib01", 0.035), ("fib02", 0.050)):
        for role, ncat, e in (("Li_top", "Li", -0.20), ("Ni_top", "Ni", -0.20 + de)):
            lab = f"ptfe_dimer__{role}__{dd}__r000"
            mol_pos = mol_at(1.0 if role == "Li_top" else 5.0)   # 각자 자기 줄 위
            at = Atoms(symbols=symb + mol_syms, positions=pos + mol_pos, cell=cell, pbc=True)
            ase_write(run / f"{lab}.xyz", at)
            (run / f"{lab}.json").write_text(json.dumps({
                "label": lab, "site": role, "down_dir": dd, "roll_deg": 0,
                "fragment": "ptfe_dimer", "E_pose_eV": e,
                "nearest_cation": ncat, "ranking_eligible": True}))

    # load_slab/load_fragment 를 합성물로 대치
    SS.load_slab = lambda: slab_at
    SS.load_fragment = lambda f: (Atoms(symbols=mol_syms, positions=mol_at(3.0)), {})
    SS.FRAGMENTS.setdefault("ptfe_dimer", {"electrons": "closed-shell singlet"})

    a = argparse.Namespace(runs=str(td / "runs"), out=str(td / "bundle"),
                           freeze=0.85, kmesh="2 2 1", nslab=nslab, frags=["ptfe_dimer"])
    out = build_bundle(a)

    # 가짜 VASP 산출 — 알려진 에너지를 심고 분석기가 그대로 복원하는지 본다
    E = {"clean": -500.0, "mol": -50.0}
    # ⚠ 심는 값은 전부 δ=0.030 **초과**여야 ROBUST 검산이 성립한다 — 0.030 을 심으면
    #   `> δ` 경계에 걸려 MARGINAL 이 나온다 (첫 판 selftest 가 그렇게 틀렸다).
    truth = {"fib00": 0.045, "fib01": 0.040, "fib02": 0.055}   # DFT ΔE(심는 값)
    def fake(jd: Path, e0: float):
        meta = json.loads((jd / "job.json").read_text())
        titels = "\n".join(f" TITEL  = PAW_PBE {POTCAR_SPEC.get(e, e)} 01Jan2000"
                           for e in meta.get("species_order", []))
        (jd / "OUTCAR").write_text(
            f"{titels}\n   NELM   =    200\n"
            f"Iteration      1(  33)\n"
            f"  energy(sigma->0) =  {e0:.6f}\n"
            f" number of electron  100.0000000 magnetization   0.0000\n"
            f" reached required accuracy - stopping structural energy minimisation\n")
        shutil.copy(jd / "POSCAR", jd / "CONTCAR")
    for jd in sorted(out.rglob("job.json")):
        d = jd.parent
        n = d.name
        if n.startswith("clean_slab"):
            fake(d, E["clean"])
        elif n.startswith("mol__"):
            fake(d, E["mol"])
        else:
            pid_dir = n.split("__")[1]          # ptfe_dimer__fibXX_r000__...
            base = E["clean"] + E["mol"] - 1.0  # 흡착 −1.0 eV
            e0 = base if "Litop" in n else base + truth[pid_dir.split("_")[0]]
            if "afm_net4" in n:
                e0 += 0.010                     # 자기 초기값 차이 (경고 임계 아래)
            fake(d, e0)

    r = subprocess.run([sys.executable, str(out / "analyze_results.py"), str(out)],
                       capture_output=True, text=True)
    print(r.stdout)
    if r.returncode != 0:
        print(r.stderr); return 1
    res = json.loads((out / "RESULTS.json").read_text())
    ok = True
    for pid, rec in res["pairs"].items():
        want = truth[rec["dir"]]
        got = rec.get("dE_Ni_minus_Li_eV")
        ok &= got is not None and abs(got - want) < 1e-6
        print(f"  검산 {pid}: ΔE {got} (심은 값 {want}) {'✔' if ok else '⛔'}")
    fr = res["fragments"]["ptfe_dimer"]
    ok &= fr.get("class") == "ROBUST_SCREENING" and fr.get("n_directions") == 3
    print(f"  검산 분류: {fr.get('class')} (기대 ROBUST_SCREENING)")
    if res["e_ads"]:
        ea = res["e_ads"][sorted(res["e_ads"])[0]]["Li_top"]
        print(f"  검산 E_ads(Li_top): {ea} (기대 -1.0)")
        ok &= abs(ea - (-1.0)) < 1e-6
    else:
        print("  ⛔ e_ads 비어 있음"); ok = False
    # 등록 유지 게이트: CONTCAR=POSCAR 이므로 PAIR_MIGRATED 가 없어야 한다
    ok &= not any("PAIR_MIGRATED" in g for j in res["jobs"].values() for g in j["gates"])
    print("✔ selftest 전부 통과" if ok else "⛔ selftest 실패")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="/data/work/runs/sdcp_v4_sitescreen",
                    help="site_screen 실행 뿌리 (<runs>/<frag>/relax_f<freeze>)")
    ap.add_argument("--out", default="/data/work/runs/sdcp_vasp_oneshot_v1")
    ap.add_argument("--freeze", type=float, default=0.85)
    ap.add_argument("--kmesh", default="2 2 1")
    ap.add_argument("--nslab", type=int, default=192,
                    help="슬랩 원자 수 (LiNiO2 104 1x4L4 = 192)")
    ap.add_argument("--frags", nargs="*", default=None, help="일부 조각만")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    build_bundle(a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
