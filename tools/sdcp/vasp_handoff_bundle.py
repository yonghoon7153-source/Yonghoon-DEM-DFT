#!/usr/bin/env python3
"""vasp_handoff_bundle.py — VASP 외주 **원샷** 번들: 자세 쌍 + 기준계 + 회수 분석기 + zip.

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
POTCAR_SPEC = {"Li": "Li_sv", "Ni": "Ni", "O": "O", "S": "S", "C": "C", "F": "F",
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
    rows = [json.loads(p.read_text()) for p in sorted(run_dir.glob("*.json"))
            if not p.name.startswith("_")]
    fs = [r for r in rows if r.get("ranking_eligible") and r.get("E_pose_eV") is not None]
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
                   extra_meta: Dict[str, Any]) -> Dict[str, Any]:
    """슬랩 계열 잡 하나 (pose 또는 clean). POSCAR 재정렬 → MAGMOM 재매핑 → 검산."""
    jd.mkdir(parents=True, exist_ok=True)
    pos = SS._write_poscar(jd / "POSCAR", atoms, nslab, freeze)
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
    order = ["Li", "Ni", "O", "S", "C", "F", "H"]
    sym = at.get_chemical_symbols()
    idx = [i for el in order for i in range(len(at)) if sym[i] == el]
    idx += [i for i in range(len(at)) if sym[i] not in order]
    counts, seen = [], []
    for el in order + sorted({s for s in sym if s not in order}):
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
import json, math, os, re, sys
from glob import glob

DELTA = 0.030          # eV — 유한설계 분류의 실무 임계 (UMA 쪽과 같은 값·같은 규칙)
MAG_TOL = 0.030        # eV — 자기 초기값 2종 불일치 경고


def read_outcar(p):
    try:
        t = open(p, errors="ignore").read()
    except OSError:
        return None
    e = re.findall(r"energy\(sigma->0\)\s*=\s*(-?[\d.]+)", t)
    ionic = "reached required accuracy" in t
    nelm = re.search(r"NELM\s*=\s*(\d+)", t)
    iters = re.findall(r"Iteration\s+\d+\(\s*(\d+)\)", t)
    nelm_hit = bool(nelm and iters and int(iters[-1]) >= int(nelm.group(1)))
    titels = re.findall(r"TITEL\s*=\s*(.+)", t)
    mag = re.findall(r"number of electron\s+[\d.]+\s+magnetization\s+(-?[\d.]+)", t)
    return {"E0": float(e[-1]) if e else None, "ionic_conv": ionic,
            "nelm_hit": nelm_hit, "titels": [x.strip() for x in titels],
            "mag_total": float(mag[-1]) if mag else None}


def read_contcar(p):
    try:
        L = open(p).read().splitlines()
    except OSError:
        return None
    scale = float(L[1].split()[0])
    cell = [[float(x) * scale for x in L[i].split()[:3]] for i in (2, 3, 4)]
    i = 5
    if not L[i].split()[0].isdigit():
        i += 1                                    # 종 이름 줄
    counts = [int(x) for x in L[i].split()]
    i += 1
    if L[i].strip() and L[i].strip()[0] in "Ss":
        i += 1                                    # Selective dynamics
    direct = L[i].strip() and L[i].strip()[0] in "DdKk" and L[i].strip()[0] in "Dd"
    i += 1
    n = sum(counts)
    pos = []
    for k in range(n):
        v = [float(x) for x in L[i + k].split()[:3]]
        if direct:
            v = [sum(v[j] * cell[j][ax] for j in range(3)) for ax in range(3)]
        pos.append(v)
    return {"cell": cell, "pos": pos}


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
                if rg and want and rg["nearest"] != want:
                    rec["gates"].append(f"PAIR_MIGRATED:{want}->{rg['nearest']}")
        rec["ok"] = not rec["gates"]
        jobs[os.path.relpath(jd, root).rstrip("/")] = rec

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
                                            "registry": r.get("registry_after_relax")}
                             for j, r in jobs.items()}}
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
UMA(MLIP) 스크리닝이 경향까지만 냈고(문서: MARGINAL_TENDENCY / SIGN_CONSISTENT_SMALL),
DFT+U 가 최종 판정입니다.

## 실행 순서 (권장)
1. `tier1/` 전부 (ptfe_c10 · ptfe_dimer — 이번 판의 목적)
2. `refs/` 전부 (**흡착에너지에 필수** — clean slab 2 + 분자 기준계)
3. `tier2/` (sdcp 2종 — 여유 되면)

각 잡 폴더에 POSCAR/INCAR/KPOINTS 가 있습니다. **POTCAR 만 붙이면 됩니다**
(라이선스 문제로 미포함 — `POTCAR_SPEC.txt` 의 변형을 정확히 써 주세요.
분석기가 OUTCAR 의 TITEL 을 대조합니다).

## ⚠ 지켜야 결과가 성립하는 것
- **INCAR 를 수정하지 말 것** — Li_top/Ni_top 쌍은 모든 설정이 같아야 ΔE 가 의미 있습니다.
  (예외: NCORE/KPAR 등 병렬 설정은 자유)
- `__afm_balanced` / `__afm_net4` 는 같은 구조의 **자기 초기값 2종**입니다. 둘 다 돌려 주세요
  (대표 쌍에만 있습니다).
- 발산/미수렴 잡은 그대로 두고 알려 주세요 — 설정을 바꿔 다시 돌리지 말아 주세요.

## 완주 후
```
python3 analyze_results.py .
```
이거 하나면 수렴 게이트 → 자리 유지 검사 → ΔE/E_ads/판정까지 전부 나옵니다
(표준 라이브러리만 사용). `RESULTS.json` 과 화면 표를 회신해 주시면 됩니다.
가능하면 각 잡의 `OUTCAR`(또는 최소 `OSZICAR`+`CONTCAR`)를 함께 보내 주세요.

## 프로토콜 (요약)
PBE+U(Ni d, U=6.2 Dudarev) · D3 zero damping(IVDW=11) · ENCUT 520 · ISMEAR=0/0.05
· 슬랩: 쌍극자 보정(IDIPOL=3) · 아래 {freeze_pct}% 고정(Selective dynamics)
· 분자 기준계: Γ-only · U/쌍극자 없음 · 같은 범함수/분산
자세한 근거·출처는 MANIFEST.json 에 있습니다.
"""


# ─────────────────────────────────────────────────────────────────────────────
def build_bundle(a) -> Path:
    out = Path(a.out)
    if out.exists() and any(out.iterdir()):
        sys.exit(f"⛔ {out} 이 비어 있지 않다 — 옛 번들과 섞이면 안 된다. 새 경로를 줄 것")
    out.mkdir(parents=True, exist_ok=True)
    slab = SS.load_slab()
    nslab = a.nslab

    try:
        commit = subprocess.run(["git", "-C", str(SS.REPO), "rev-parse", "HEAD"],
                                capture_output=True, text=True).stdout.strip()
    except Exception:
        commit = "unknown"
    man: Dict[str, Any] = {
        "created": "2026-08-11", "repo_commit": commit,
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
                for role, rec in (("Li", p["li"]), ("Ni", p["ni"])):
                    xyz = run / f"{rec['label']}.xyz"
                    if not xyz.is_file():
                        print(f"  ⚠ {rec['label']}.xyz 없음 — 쌍 통째로 건너뜀")
                        break
                    cx = ase_read(xyz); cx.set_cell(slab.cell.array); cx.set_pbc(True)
                    used_els |= set(cx.get_chemical_symbols())
                    for mg in mags:
                        _emit_slab_job(out / tier / f"{pid}__{role}top__{mg}",
                                       cx, nslab, a.freeze, frag,
                                       f"{pid} {role}-top {mg}", mg, a.kmesh,
                                       {"kind": "pose", "role": role, "pair_id": pid,
                                        "fragment": frag, "source_pose": rec["label"],
                                        "uma_E_pose_eV": rec["E_pose_eV"]})
                        n_jobs += 1
                else:
                    man["pairs"][pid] = pm

    # ── 기준계 ① 깨끗한 슬랩 (같은 구속·양쪽 자기 초기값) ─────────────────────
    clean = None
    for frag in man["fragments"]:
        cp = Path(a.runs) / frag / f"relax_f{a.freeze:.2f}" / "_clean_slab.vasp"
        if cp.is_file():
            clean = ase_read(cp); break
    if clean is None:
        clean = slab.copy()
    for mg in ("afm_balanced", "afm_net4"):
        _emit_slab_job(out / "refs" / f"clean_slab__{mg}", clean, len(clean), a.freeze,
                       man["fragments"][0] if man["fragments"] else "ptfe_c10",
                       f"clean slab {mg}", mg, a.kmesh, {"kind": "clean_ref"})
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

    man["potcar_spec"] = {e: POTCAR_SPEC.get(e, e) for e in sorted(used_els)}
    (out / "analyze_results.py").write_text(ANALYZER)
    (out / "README_REQUEST.md").write_text(README.format(freeze_pct=int(a.freeze * 100)))
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

    zp = out.with_suffix(".zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(out.parent))
    print(f"\n→ {out}  · 잡 {n_jobs}개 · 쌍 {len(man['pairs'])}개 · 조각 {man['fragments']}")
    print(f"→ {zp}  ({zp.stat().st_size / 1e6:.1f} MB)")
    print("  ⚠ POTCAR 미포함(라이선스) — POTCAR_SPEC.txt 의 변형을 정확히 쓸 것")
    return out


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
