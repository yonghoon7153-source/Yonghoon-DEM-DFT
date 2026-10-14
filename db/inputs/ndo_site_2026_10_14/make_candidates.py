#!/usr/bin/env python3
"""make_candidates.py — Nd/O-LPSCl1.6 Nd 자리 비교의 후보 구조 (같은 예산).

카드 db/properties/ndo_lpscl16_site_stability_estimand_2026_10_14.json §1-b · §3 (결정 D-2026-10-14-ndo-site-stability-estimand).
트랙 CEI/Nd · 1저자 = 실험 쪽. 기존 도구 두 개만 부른다 — 새 물리 규약을 만들지 않는다.

  M_P  (Nd@4b · Rietveld 방식 · Cl8Li31Nd2O3P3S19 · 66 원자)
       tools/doping/b2o3_enumerate.py --rietveld_cif (5 f.u. · n_B 2 · n_O 3) → Ewald 서로 다른 상위 N × O-distributed
       (O 배치는 O 배치 카드 G2 가 DFT 로 고른 'distributed' 로 고정한다)
  M_Li (Nd@Li · Cl8Li21Nd2O3P5S19 · 58 원자)
       같은 격자의 도핑 전 host (b2o3_enumerate --n_B 0) 서로 다른 할로겐 배열 상위 H 개 →
       tools/doping/substitute_compound.py Type A (Nd2O3 1 단위 · Li 자리 --method random · O→S_16e · 공공 random / near_cation) →
       'O 3 개가 서로 다른 PS4' 만 남김 → 같은 형식전하 Ewald 로 서로 다른 상위 N
  host (Cl8Li27P5S22 · 62 원자) — 도핑 전 서로 다른 상위 3 (Q2 · Q3 기준)

같은 예산: 두 모델 다 '형식전하 Ewald 로 거른 서로 다른 상위 N' 을 UMA 로 넘긴다. M_P 는 할로겐 배열을 Nd 와 함께 고르므로
M_Li 도 host 할로겐 배열 H 개에서 출발시켜 같은 자유도를 준다.

⛔ 이 도구가 못 하는 것
  · 에너지 순위를 주지 않는다 — Ewald 는 사전 거르기이고 O 배치(S 와 같은 −2)에는 눈멀다. 순위는 UMA 어닐·이완 → DFT 단일점이다.
  · '서로 다른' 은 Ewald 값 1e-3 eV 반올림으로 가른다 — 대칭 동등 배치를 완전히 가르는 구조 정합이 아니다.
  · 두 모델의 Ewald 값끼리는 비교하지 않는다 (조성이 다르다).
  · 1저자 목표 농도 (Nd/(Nd+P) 0.02) 가 아니다 — 0.40 이다 (카드 §1-b).

사용:
  python3 db/inputs/ndo_site_2026_10_14/make_candidates.py --selftest
  python3 db/inputs/ndo_site_2026_10_14/make_candidates.py --out db/inputs/ndo_site_2026_10_14/candidates
"""
from __future__ import annotations

import argparse, hashlib, json, subprocess, sys, tempfile
from collections import Counter
from pathlib import Path

import numpy as np
from ase.io import read, write

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "tools" / "doping"))
from b2o3_enumerate import ewald_matrix, ewald_energy          # noqa: E402  (같은 Ewald — 규약 복제 안 함)

RIETVELD = REPO / "db/structures/ndo_lpscl16_rietveld_2026_09_07/00_SOURCE_Rietveld_NdO_LPSCl1.6.cif"
ENUM = REPO / "tools/doping/b2o3_enumerate.py"
SUBST = REPO / "tools/doping/substitute_compound.py"
Q = {"Li": 1, "P": 5, "Nd": 3, "S": -2, "O": -2, "Cl": -1}
WANT = {"MP": {"Cl": 8, "Li": 31, "Nd": 2, "O": 3, "P": 3, "S": 19},
        "MLi": {"Cl": 8, "Li": 21, "Nd": 2, "O": 3, "P": 5, "S": 19},
        "host": {"Cl": 8, "Li": 27, "P": 5, "S": 22}}
CELL = [6.92802, 6.92802, 34.6401, 60.0, 60.0, 60.0]


def comp(atoms):
    return dict(Counter(atoms.get_chemical_symbols()))


def check(atoms, kind):
    c = comp(atoms)
    if c != WANT[kind]:
        raise ValueError(f"{kind}: 조성 {c} ≠ 카드 {WANT[kind]}")
    cp = [round(float(x), 4) for x in atoms.cell.cellpar()]
    if any(abs(a - b) > 2e-3 for a, b in zip(cp, CELL)):
        raise ValueError(f"{kind}: 셀 {cp} ≠ Rietveld 5 f.u. 셀 {CELL}")


def ewald(atoms):
    q = np.array([Q[s] for s in atoms.get_chemical_symbols()], float)
    if abs(q.sum()) > 1e-9:
        raise ValueError(f"전하 중성이 아니다 (Σq = {q.sum()})")
    return ewald_energy(ewald_matrix(atoms.get_positions(), np.array(atoms.cell)), q)


def o_on_distinct_ps4(atoms):
    """O 셋이 서로 다른 P 에 붙어 있나 (최근접 P 거리 < 2.4 Å · 서로 다른 P)."""
    sym = np.array(atoms.get_chemical_symbols()); P = np.where(sym == "P")[0]; O = np.where(sym == "O")[0]
    owners = []
    for i in O:
        d = atoms.get_distances(i, P, mic=True)
        if d.min() > 2.4:
            return False
        owners.append(P[d.argmin()])
    return len(set(owners)) == len(owners)


def distinct_top(items, n):
    """items: (E, path) — Ewald 1e-3 eV 반올림으로 서로 다른 것만, 낮은 순 n 개."""
    seen, out = set(), []
    for e, p in sorted(items):
        k = round(e, 3)
        if k in seen:
            continue
        seen.add(k); out.append((e, p))
        if len(out) == n:
            break
    return out


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(cmd):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"실패: {' '.join(map(str, cmd))}\n{r.stdout[-800:]}\n{r.stderr[-800:]}")
    return r.stdout


def build(out, n_each, n_host_seed, n_seeds, n_near):
    out = Path(out); tmp = Path(tempfile.mkdtemp(prefix="ndsite_"))
    cmds = []
    # ── M_P ──────────────────────────────────────────────────────────────
    c = [sys.executable, ENUM, "--rietveld_cif", RIETVELD, "--primitive", "--supercell", 1, 1, 5, "--dopant", "Nd",
         "--n_B", 2, "--n_O", 3, "--top", 60, "--o_motif_top", 60, "--seed", 0, "--out", tmp / "mp"]
    run(c); cmds.append(" ".join(map(str, c)))
    ranked = json.loads((tmp / "mp" / "stage0_ranked.json").read_text())
    rows = ranked if isinstance(ranked, list) else ranked.get("ranked", ranked.get("rows", []))
    mp_items = [(float(r["ewald_eV"]), tmp / "mp" / "cif" / f"{r['name']}_O-distributed.cif") for r in rows
                if (tmp / "mp" / "cif" / f"{r['name']}_O-distributed.cif").exists()]
    mp = distinct_top(mp_items, n_each)
    # ── host ─────────────────────────────────────────────────────────────
    c = [sys.executable, ENUM, "--rietveld_cif", RIETVELD, "--primitive", "--supercell", 1, 1, 5, "--dopant", "Nd",
         "--n_B", 0, "--n_O", 0, "--top", 45, "--o_motif_top", 0, "--seed", 0, "--out", tmp / "host"]
    run(c); cmds.append(" ".join(map(str, c)))
    hr = json.loads((tmp / "host" / "stage0_ranked.json").read_text())
    hrows = hr if isinstance(hr, list) else hr.get("ranked", hr.get("rows", []))
    host_all = distinct_top([(float(r["ewald_eV"]), tmp / "host" / "cif" / f"{r['name']}.cif") for r in hrows], max(3, n_host_seed))
    # ── M_Li ─────────────────────────────────────────────────────────────
    mli_items, n_gen, n_rej_o = [], 0, 0
    for h, (_, hpath) in enumerate(host_all[:n_host_seed]):
        # Nd 자리는 --method random (시드마다 다름 · 파일 이름 _sNN) · 공공은 random / near_cation 두 갈래
        jobs = [("random", 1000 * (h + 1), n_seeds), ("near_cation", 1000 * (h + 1) + 500, n_near)]
        for meth, seed, ns in jobs:
            d = tmp / f"mli_h{h}_{meth}_{seed}"
            c = [sys.executable, SUBST, "--base", hpath, "--compound", "Nd2O3", "--x_compound", 0.25,
                 "--cation_site", "Li_48h", "--anion_site", "S_16e", "--method", "random", "--vacancy_method", meth,
                 "--seed", seed, "--n_seeds", ns, "--out", d]
            run(c); cmds.append(" ".join(map(str, c)))
            for f in sorted(d.glob("*.xyz")):
                a = read(f); n_gen += 1
                check(a, "MLi")
                if not o_on_distinct_ps4(a):
                    n_rej_o += 1; continue
                mli_items.append((ewald(a), f))
    mli = distinct_top(mli_items, n_each)
    # ── 쓰기 ─────────────────────────────────────────────────────────────
    man = {"card": "db/properties/ndo_lpscl16_site_stability_estimand_2026_10_14.json",
           "decision": "D-2026-10-14-ndo-site-stability-estimand",
           "git_head": run(["git", "-C", REPO, "rev-parse", "HEAD"]).strip(),
           "commands": cmds, "budget": {"n_each": n_each, "M_Li_hosts": n_host_seed, "random_seeds_per_host": n_seeds,
                                         "near_cation_per_host": n_near},
           "M_Li_generated": n_gen, "M_Li_rejected_O_same_PS4": n_rej_o, "M_Li_pool_after_filter": len(mli_items),
           "M_P_pool": len(mp_items), "files": {}}
    for kind, sel in (("MP", mp), ("MLi", mli), ("host", host_all[:3])):
        (out / kind).mkdir(parents=True, exist_ok=True)
        for i, (e, p) in enumerate(sel):
            a = read(p); check(a, kind)
            if kind == "MLi" and not o_on_distinct_ps4(a):
                raise ValueError("M_Li 거르기 뒤에 O 가 같은 PS4 에 있다")
            dst = out / kind / f"{kind}_{i:02d}.xyz"
            write(dst, a, format="extxyz")
            man["files"][str(dst.relative_to(out))] = {"source": f"{Path(p).parent.name}/{Path(p).name}", "ewald_eV": round(e, 4),
                                                       "sha256": sha(dst)}
    (out / "manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n")
    return man


def _selftest():
    ok = 0
    def chk(c, m):
        nonlocal ok
        if not c:
            raise SystemExit(f"selftest FAIL: {m}")
        ok += 1
    from ase import Atoms
    a = Atoms("Li2S", positions=[[0, 0, 0], [1.5, 1.5, 0], [0.75, 0.75, 1.5]], cell=[4, 4, 4], pbc=True)
    try:
        check(a, "MP"); chk(False, "[negative] 틀린 조성은 멈춰야 한다")
    except ValueError:
        ok += 1
    b = Atoms("LiP", positions=[[0, 0, 0], [2, 2, 2]], cell=[5, 5, 5], pbc=True)
    try:
        ewald(b); chk(False, "[negative] 전하가 안 맞으면 멈춰야 한다")
    except ValueError:
        ok += 1
    chk(distinct_top([(1.0001, "a"), (1.0002, "b"), (0.5, "c"), (2.0, "d")], 2) == [(0.5, "c"), (1.0001, "a")],
        "서로 다른 상위: 1e-3 반올림으로 같은 값은 하나만 · 낮은 순")
    # PS4 거르기: P 둘 · O 둘이 각자 다른 P → True, 같은 P → False
    def mk(o2):
        return Atoms("P2O2", positions=[[0, 0, 0], [5, 0, 0], [1.55, 0, 0], o2], cell=[12, 12, 12], pbc=True)
    chk(o_on_distinct_ps4(mk([6.55, 0, 0])), "O 둘이 서로 다른 P 에 붙으면 통과")
    chk(not o_on_distinct_ps4(mk([0, 1.55, 0])), "[negative] O 둘이 같은 P 에 붙으면 거른다")
    print(f"selftest PASS ({ok})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--n_each", type=int, default=10)
    ap.add_argument("--n_host_seed", type=int, default=5)
    ap.add_argument("--n_seeds", type=int, default=40)
    ap.add_argument("--n_near", type=int, default=10)
    A = ap.parse_args()
    if A.selftest:
        _selftest()
    else:
        m = build(A.out, A.n_each, A.n_host_seed, A.n_seeds, A.n_near)
        print(json.dumps({k: m[k] for k in ("M_P_pool", "M_Li_generated", "M_Li_rejected_O_same_PS4", "M_Li_pool_after_filter")}, ensure_ascii=False))
        print(f"files {len(m['files'])} → {A.out}/manifest.json")
