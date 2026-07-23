#!/usr/bin/env python3
"""A3 validation — PTFE binder wt% sweep → MPM porosity/mechanics check.

★ 확정 결과 (docs/a3_binder_sweep_result.md, real14/384/CUDA): 생산압(300 MPa)에서 porosity 는
  MONOTONE-감소 (15.91→4.40 %, 0→8 wt%) — PTFE(E=0.30, σ_y=0.05 GPa)가 50 MPa≪300 에서 항복해
  void 를 **채우기** 때문.  binder_cap 비단조(0.93→0.96→0.50→0.07)는 volume-fill 에 **가려짐**.
  → non-monotonic 바인더 역할은 **기계 무결성 + 수송 σ-block** 에 있지 raw porosity 아님.
  ∪(propping bump)는 ≲5 MPa (항복-게이트 지지) 에서만 나타남.

Tests the A3 binder model (mpm3d_compaction.binder_cap): cohesion peaks at --binder-opt-wt and
decays for over-application (Hong 2026 void −6.4%p; over-crosslink Cho 2024).  The verdict logic
(:96-119) correctly prints MONOTONE at production pressure; run at low --target-gpa to see the ∪.

Runs mpm3d_compaction once per PTFE wt% (real14 scaffold by default) and collects
porosity.  GPU: --arch cuda.  One command after `git pull`:

  python3 scripts/a3_binder_sweep.py --arch cuda --n-grid 384

Lower --n-grid (256) for a faster trend pass; the ∪ is a RELATIVE comparison at
fixed resolution, so the shape is resolution-robust even if the absolute shifts.
"""
import argparse, json, math, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from mpm3d_compaction import binder_cap   # the exact A3 cap used in the run


def run_one(wt, a, out_dir):
    mj = os.path.join(out_dir, f"m_ptfe_{wt}.json")
    cmd = ["python3", os.path.join(HERE, "mpm3d_compaction.py"),
           "--am-scaffold", a.scaffold_am, "--se-dump", a.scaffold_se, "--periodic",
           "--lateral-box", str(a.lateral_box), "--n-grid", str(a.n_grid),
           "--arch", a.arch, "--protocol", "hold", "--frames", str(a.frames),
           "--e-se", str(a.e_se), "--nu-se", str(a.nu_se), "--target-gpa", str(a.target_gpa),
           "--coh-ptfe", str(a.coh_ptfe), "--binder-opt-wt", str(a.opt_wt),
           "--save-metrics", mj]
    if wt > 0:                                            # wt=0 = baseline, no binder
        cmd += ["--add-recipe", f"PTFE={wt:g}", "--mixing", a.mixing]
    print(f"\n### PTFE {wt:g} wt%  (binder_cap={binder_cap(wt, a.opt_wt):.3f}, "
          f"coh={a.coh_ptfe*binder_cap(wt, a.opt_wt):.4f} GPa) ###")
    print("  " + " ".join(cmd))
    try:
        subprocess.run(cmd, check=True, cwd=REPO)
    except subprocess.CalledProcessError as e:
        print(f"  [run failed wt={wt}: {e}]")
        return None
    if not os.path.exists(mj):
        return None
    d = json.load(open(mj))
    por = d.get("porosity_at_target_pct") or d.get("porosity_settled_pct")
    return dict(wt=wt, cap=binder_cap(wt, a.opt_wt), porosity=por,
                thickness=d.get("thickness_um"),
                readout=("at_target" if d.get("porosity_at_target_pct") else "settled"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scaffold-am", default="docs/data/real14_am_scaffold.csv")
    ap.add_argument("--scaffold-se", default="docs/data/real14_se_scaffold.csv")
    ap.add_argument("--lateral-box", type=float, default=0.05, help="real14 ≈ 0.05")
    ap.add_argument("--n-grid", type=int, default=384)
    ap.add_argument("--arch", default="cuda", choices=["cpu", "gpu", "cuda", "vulkan"])
    ap.add_argument("--frames", type=int, default=150)
    ap.add_argument("--wts", default="0,0.5,1,2,4,8", help="PTFE wt%% list")
    ap.add_argument("--opt-wt", type=float, default=1.5)
    ap.add_argument("--coh-ptfe", type=float, default=0.10)
    ap.add_argument("--mixing", default="thinky")
    ap.add_argument("--e-se", type=float, default=1.53)
    ap.add_argument("--nu-se", type=float, default=0.49)
    ap.add_argument("--target-gpa", type=float, default=0.30)
    ap.add_argument("--out-dir", default="a3_sweep_out")
    a = ap.parse_args()
    a.scaffold_am = a.scaffold_am if os.path.isabs(a.scaffold_am) else os.path.join(REPO, a.scaffold_am)
    a.scaffold_se = a.scaffold_se if os.path.isabs(a.scaffold_se) else os.path.join(REPO, a.scaffold_se)
    os.makedirs(os.path.join(REPO, a.out_dir), exist_ok=True)
    out_dir = os.path.join(REPO, a.out_dir)
    wts = [float(w) for w in a.wts.split(",")]

    rows = [r for r in (run_one(w, a, out_dir) for w in wts) if r and r["porosity"] is not None]

    print("\n" + "=" * 64)
    print(f"A3 PTFE binder sweep  (opt {a.opt_wt} wt%, coh_ptfe {a.coh_ptfe} GPa, "
          f"n_grid {a.n_grid}, {a.arch})")
    print(f"{'PTFE wt%':>9} {'binder_cap':>11} {'porosity%':>10} {'thick µm':>9}  readout")
    for r in rows:
        print(f"{r['wt']:>9g} {r['cap']:>11.3f} {r['porosity']:>10.2f} "
              f"{(r['thickness'] or 0):>9.2f}  {r['readout']}")

    # Shape diagnosis. Two real signals: (1) a ∪ (porosity min at an interior wt%,
    # rising both sides — the cohesion-driven shape), and (2) a low-loading propping
    # BUMP (porosity rises ABOVE the no-binder baseline at small wt% — the yield-gated
    # propping that appears below σ_y pressure, A3 5 MPa result). Report whichever is real.
    pos = [r for r in rows if r["wt"] > 0]
    base = next((r["porosity"] for r in rows if r["wt"] == 0), None)
    if len(pos) >= 3:
        pmin = min(pos, key=lambda r: r["porosity"])
        interior = pos[0]["wt"] < pmin["wt"] < pos[-1]["wt"]
        rises_right = pos[-1]["porosity"] > pmin["porosity"] + 0.3
        rises_left = pos[0]["porosity"] > pmin["porosity"] + 0.3
        # propping bump: any binder point sits ≥0.3 %p above the no-binder baseline
        bump = max(pos, key=lambda r: r["porosity"])
        propping = base is not None and bump["porosity"] > base + 0.3
        print(f"\n  min porosity {pmin['porosity']:.2f}% at PTFE {pmin['wt']:g} wt% "
              f"(binder_cap {pmin['cap']:.2f})")
        if propping:
            print(f"  propping bump: porosity {bump['porosity']:.2f}% at {bump['wt']:g} wt% "
                  f"> baseline {base:.2f}% (+{bump['porosity']-base:.2f} %p)")
        verdict = ("∪-SHAPE ✓ (min at optimal, rises both sides) — A3 ↔ Hong/Cho"
                   if interior and rises_right and rises_left else
                   "NON-MONOTONE: low-loading PROPPING bump (binder opens the bed above "
                   "baseline at small wt%, then volume-fill wins) — expected below σ_y "
                   "pressure (A3 5 MPa); means the binder is NOT yielding here"
                   if propping else
                   "half-∪ (rises on over-application side only) — partial A3 support"
                   if rises_right else
                   "MONOTONE — binder volume-fill dominates; binder yields (≥σ_y pressure) "
                   "so no propping. Correct at 300 MPa production")
        print(f"  VERDICT: {verdict}")
    print("=" * 64)


if __name__ == "__main__":
    main()
