#!/usr/bin/env python3
"""orchestrate.py — plan + human-in-loop gates + provenance for the report-card
pipeline (factory v1.1).

Constraints honored: no auto-SSH/no auto-execute of remote jobs. Instead this
detects which report-card sections are already DONE (db/ cache, via the
assembler), plans the PENDING stages (compute backend, cost, the gate that must
clear first, and the exact command to run), prints a run plan, and writes a
provenance manifest. The operator runs the emitted commands on gabia/KISTI; when
db/ updates, re-run to refresh the plan / re-assemble the card.

  python3 factory/orchestrate.py b2o3                  # run plan + gates
  python3 factory/orchestrate.py b2o3 --assemble       # re-build card from db/
  python3 factory/orchestrate.py b2o3 --stamp 2026-06-30T12:00:00Z  # provenance time

The card itself is built by assemble_report_card.py (reused here); this layer is
the scheduler/gatekeeper around it.
"""
import argparse, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import assemble_report_card as A  # reuse db checks + build()

RUNS = HERE / "runs"

# stage order + metadata (mirrors registry/stages.yaml) + command templates.
# command(sys) returns the operator-facing command for a PENDING stage.
def _xyz(s):
    return s.get("structure_ref", "").replace(".cif", ".xyz")


STAGE_META = {
    "screening": dict(backend="cascade(upstream)", cost="—", gate=None,
        cmd=lambda s: "(upstream cascade; re-link by version+candidate_id if cascade evolves)"),
    "transport": dict(backend="gabia(MLIP)", cost="medium", gate="prep_gate",
        cmd=lambda s: f"python3 tools/modelc_v3/disorder_ensemble_diffusion.py --v0_xyz {_xyz(s)} "
                      f"--label {s['id']} --temperatures 600 800 1000 --equilib_ps 10 --prod_ps 100 "
                      f"--save_fs 100 --fit_window_ps 2 50 --save_traj   # protocol: kb/methodology/md_conductivity_protocol.md"),
    "thermodynamic_stability": dict(backend="gabia/local(MP)", cost="low", gate=None,
        cmd=lambda s: f"python3 tools/doping/convex_hull_ehull.py --structure {s['structure_ref']} --mode uma"),
    "electrochemical_window": dict(backend="gabia/local(MP)", cost="low", gate=None,
        cmd=lambda s: "python3 tools/oxidation/esw_grand_potential.py ... && python3 tools/oxidation/sei_product_gaps.py ..."),
    "mechanical": dict(backend="KISTI(QE)", cost="high", gate="cost_gate",
        cmd=lambda s: "python3 tools/comp1_v3/build_elastic_strain_inputs.py --relaxed_ion ... "
                      "(12 strain SCF on KISTI) && fit_elastic_cij_stress.py"),
    "electronic": dict(backend="KISTI(QE)", cost="medium", gate="prep_gate",
        cmd=lambda s: "standard_dos recipe: scf -> nscf -> projwfc (KISTI)"),
    "structure_chemistry": dict(backend="local+KISTI", cost="low", gate=None,
        cmd=lambda s: "bond/coordination (local) + pp.x charge cube -> Bader/Lowdin (KISTI)"),
    "dynamical_stability": dict(backend="gabia(MLIP)", cost="medium", gate="cost_gate",
        cmd=lambda s: f"python3 tools/electronic/uma_phonon.py --xyz {_xyz(s)}"),
    "testable_predictions": dict(backend="derived", cost="—", gate=None,
        cmd=lambda s: "(derived from structure_chemistry + dynamical_stability; no new run)"),
}

GATE_Q = {
    "prep_gate": "structure relaxed OK?",
    "cost_gate": "approve expensive DFT/DFPT stage?",
    "rank_gate": "approve final report card?",
}


def plan(sysid, stamp=None):
    card = A.build(sysid, stamp=stamp)
    s = A.SYSTEMS[sysid]
    secs = [k for k in STAGE_META]
    done, pending = [], []
    for sec in secs:
        st = card.get(sec, {}).get("status")
        (done if st in ("done", "n.a.") else pending).append(sec)
    return card, s, done, pending


def render(card, s, done, pending):
    L = [f"╔══ factory orchestrator — {s['id']} ({s['composition']}) ══╗",
         f"  completeness: {card['overall']['completeness']}",
         "\n■ DONE (cached in db/):"]
    for sec in done:
        d = card[sec]
        L.append(f"   ✅ {sec:24s} [{d.get('confidence') or '-'}] {(d.get('method') or '')[:48]}")
    L.append("\n■ PENDING (operator runs; gates first):")
    if not pending:
        L.append("   (none — card complete; → rank_gate: approve final card?)")
    gates_needed = []
    for sec in pending:
        m = STAGE_META[sec]
        g = m["gate"]
        if g and g not in gates_needed:
            gates_needed.append(g)
        L.append(f"   ▶ {sec:24s} backend={m['backend']:14s} cost={m['cost']:6s} gate={g or '-'}")
        L.append(f"       $ {m['cmd'](s)}")
    if gates_needed:
        L.append("\n■ HUMAN-IN-LOOP GATES to clear:")
        for g in gates_needed:
            L.append(f"   ⛔ {g}: {GATE_Q.get(g,'?')}")
    L.append("\n■ NEXT: clear gate(s) → run pending command(s) → `orchestrate.py {} --assemble` to refresh.".format(s['id']))
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("system", choices=list(A.SYSTEMS))
    ap.add_argument("--assemble", action="store_true", help="re-build card JSON+MD from db/")
    ap.add_argument("--stamp", default=None, help="provenance UTC (default: now)")
    args = ap.parse_args()

    card, s, done, pending = plan(args.system, stamp=args.stamp)
    print(render(card, s, done, pending))

    if args.assemble:
        A.CARDS.mkdir(parents=True, exist_ok=True)
        (A.CARDS / f"{args.system}_report_card.json").write_text(json.dumps(card, indent=2, ensure_ascii=False))
        (A.CARDS / f"{args.system}_report_card.md").write_text(A.to_md(card))
        print(f"\n→ re-assembled factory/cards/{args.system}_report_card.{{json,md}}")

    # provenance manifest
    RUNS.mkdir(parents=True, exist_ok=True)
    manifest = {
        "system": args.system, "stamp": args.stamp,
        "completeness": card["overall"]["completeness"],
        "done": done, "pending": pending,
        "next_gates": sorted({STAGE_META[p]["gate"] for p in pending if STAGE_META[p]["gate"]}),
        "planned_commands": {p: STAGE_META[p]["cmd"](s) for p in pending},
    }
    (RUNS / f"{args.system}_run.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"→ provenance: factory/runs/{args.system}_run.json")


if __name__ == "__main__":
    main()
