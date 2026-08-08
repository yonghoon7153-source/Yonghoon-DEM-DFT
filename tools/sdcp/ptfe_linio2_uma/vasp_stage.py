#!/usr/bin/env python3
"""Prepare and analyze the VASP DFT validation stage after the PTFE UMA screen.

This script never runs VASP and never distributes POTCAR data.  ``prepare``
turns the UMA ``DFT_HANDOFF.json`` into a reproducible job matrix. ``analyze``
parses returned OUTCAR files, chooses the lowest electronic solution across
magnetic starts, and reports adsorption energies and matched Li/Ni site gaps.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple


PACKAGE_DIR = Path(__file__).resolve().parent
N_SLAB = 192
SPECIES_ORDER = ("Li", "Ni", "O", "C", "F", "H")
POTCAR_MAP = {
    "Li": "Li_sv",
    "Ni": "Ni_pv",
    "O": "O",
    "C": "C",
    "F": "F",
    "H": "H",
}
COARSE_MESH = (2, 3, 1)
DENSE_MESH = (3, 4, 1)
U_NI_EV = 6.2
SURFACE_C_A = 34.6
PILOT_RELAXED_BY_MODEL = {"dimer": 1, "c10": 2}
SEED_SPREAD_WARN_EV = 0.030
KPOINT_TOL_EV = 0.010
PREFERENCE_FLOOR_EV = 0.030
FORCE_GATE_EV_A = 0.020
GAS_BOX_TOL_EV = 0.010
FINALIST_WINDOW_EV = 0.150
SURFACE_LI_DISPLACEMENT_MAX_A = 0.80
SURFACE_NI_O_DISPLACEMENT_MAX_A = 0.50
SURFACE_LI_O_COORDINATION_CUTOFF_A = 2.50
SURFACE_LI_O_MAX_COORDINATION_LOSS = 1


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".tmp.{os.getpid()}")
    # Path.write_text gained ``newline`` only in newer Python releases.  The
    # vendor package deliberately supports Python 3.8+, so use open() here.
    with tmp.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    os.replace(tmp, path)


def atomic_json(path: Path, payload: Any) -> None:
    atomic_text(path, json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n")


def atomic_csv(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".tmp.{os.getpid()}")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(tmp, path)


def write_input_manifest(root: Path) -> None:
    paths: List[Path] = []
    for name in (
        "VASP_PLAN.json",
        "VASP_PLAN.csv",
        "README_GENERATED.md",
        "VASP_README_KO.md",
        "vasp_run.sh",
        "vasp_stage.py",
        "vasp_vendor.conf.example",
        "UPSTREAM_DFT_HANDOFF.json",
        "PACKAGE_COMMIT.txt",
    ):
        paths.append(root / name)
    for path in sorted((root / "jobs").glob("*/*")):
        if path.is_file():
            paths.append(path)
    lines = [f"{sha256(path)}  {path.relative_to(root).as_posix()}" for path in paths]
    atomic_text(root / "VASP_INPUT_MANIFEST.sha256", "\n".join(lines) + "\n")


def verify_input_manifest(root: Path) -> None:
    manifest = root / "VASP_INPUT_MANIFEST.sha256"
    if not manifest.is_file():
        raise SystemExit(f"existing VASP package lacks input manifest: {manifest}")
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, separator, relative = line.partition("  ")
        if not separator or not expected or not relative:
            raise SystemExit(f"malformed VASP input manifest line: {line!r}")
        path = root / relative
        if not path.is_file() or sha256(path) != expected:
            raise SystemExit(f"existing VASP package input drift: {relative}")


def ase_imports():
    try:
        import numpy as np
        from ase.constraints import FixAtoms
        from ase.io import read, write
    except ImportError as exc:
        raise SystemExit(f"ASE/NumPy import failed: {exc}")
    return np, FixAtoms, read, write


def present_species(atoms) -> List[str]:
    symbols = atoms.get_chemical_symbols()
    runs: List[str] = []
    for symbol in symbols:
        if not runs or runs[-1] != symbol:
            runs.append(symbol)
    if runs != [element for element in SPECIES_ORDER if element in set(symbols)]:
        raise SystemExit(f"atoms are not grouped in VASP species order: {runs}")
    return runs


def reorder_atoms(atoms):
    order = {symbol: rank for rank, symbol in enumerate(SPECIES_ORDER)}
    indices = sorted(range(len(atoms)), key=lambda index: (order[atoms[index].symbol], index))
    return atoms[indices]


def apply_bottom_half_constraint(atoms, nslab: int = N_SLAB) -> Tuple[int, float]:
    np, FixAtoms, _, _ = ase_imports()
    atoms.set_constraint()
    slab_z = np.asarray(atoms.positions[:nslab, 2], dtype=float)
    zcut = float(slab_z.min() + 0.5 * (slab_z.max() - slab_z.min()))
    fixed = [index for index in range(nslab) if float(atoms.positions[index, 2]) < zcut]
    atoms.set_constraint(FixAtoms(indices=fixed))
    return len(fixed), zcut


def boxed_molecule(path: Path, model_name: str, large: bool):
    _, _, read, _ = ase_imports()
    atoms = read(path)
    atoms.set_constraint()
    if model_name == "c10":
        lengths = (32.0, 32.0, 40.0) if large else (28.0, 28.0, 36.0)
    else:
        lengths = (28.0, 28.0, 28.0) if large else (24.0, 24.0, 24.0)
    atoms.set_cell(lengths)
    atoms.center()
    atoms.set_pbc(True)
    return reorder_atoms(atoms)


def expand_surface_cell(atoms):
    """Use the common 34.6-A slab cell without moving Cartesian atoms."""
    np, _, _, _ = ase_imports()
    cell = np.asarray(atoms.cell.array, dtype=float).copy()
    cvec = cell[2]
    clen = float(np.linalg.norm(cvec))
    if clen <= 0.0:
        raise SystemExit("invalid surface c vector")
    if abs(float(cvec[0])) > 1.0e-6 or abs(float(cvec[1])) > 1.0e-6:
        raise SystemExit("surface c vector is not normal to the xy plane")
    if clen > SURFACE_C_A + 1.0e-6:
        raise SystemExit(f"source c={clen:.6f} A exceeds the fixed {SURFACE_C_A} A protocol")
    cell[2] = cvec * (SURFACE_C_A / clen)
    atoms.set_cell(cell, scale_atoms=False)
    atoms.set_pbc(True)
    return atoms


def ni_afm_signs(atoms, nslab: int) -> Dict[int, float]:
    """Reproduce the canonical QE Ni1/Ni2 pattern in each 48-atom replica."""
    ni = [
        index for index, symbol in enumerate(atoms.get_chemical_symbols()[:nslab])
        if symbol == "Ni"
    ]
    if len(ni) != 48:
        raise SystemExit(f"expected 48 slab Ni atoms, found {len(ni)}")
    # Ni2/Ni1 signs in db/inputs/sdcp_v2/slab_relax/relax.in, in the
    # canonical grouped-Ni order.  The tracked 1x4 slab repeats this 12-Ni
    # primitive pattern four times.  Geometry-only x/z alternation would make
    # ferromagnetic stripes and matches only half of this lineage.
    primitive_pattern = (
        -1.0, 1.0, 1.0, 1.0, -1.0, -1.0,
        -1.0, 1.0, 1.0, -1.0, -1.0, 1.0,
    )
    signs = {
        atom_index: primitive_pattern[local_index % len(primitive_pattern)]
        for local_index, atom_index in enumerate(ni)
    }
    counts = Counter(1 if value > 0 else -1 for value in signs.values())
    if counts[1] != 24 or counts[-1] != 24:
        raise SystemExit(f"unbalanced AFM seed: {counts}")
    return signs


def nearest_seed_ni(atoms, nslab: int) -> int:
    np, _, _, _ = ase_imports()
    symbols = atoms.get_chemical_symbols()
    ni = [index for index in range(nslab) if symbols[index] == "Ni"]
    symbols = atoms.get_chemical_symbols()
    contact_f = [index for index in range(nslab, len(atoms)) if symbols[index] == "F"]
    if contact_f:
        return min(
            ni,
            key=lambda index: float(
                np.asarray(atoms.get_distances(index, contact_f, mic=True), dtype=float).min()
            ),
        )
    top = max(float(atoms.positions[index, 2]) for index in ni)
    surface = [index for index in ni if float(atoms.positions[index, 2]) >= top - 0.6]
    centre = 0.5 * (atoms.cell.array[0] + atoms.cell.array[1])
    return min(surface, key=lambda index: float(np.linalg.norm(atoms.positions[index, :2] - centre[:2])))


def magmom_values(atoms, nslab: int, seed: str) -> Tuple[List[float], int | None]:
    values = [0.0] * len(atoms)
    if "Ni" not in atoms.get_chemical_symbols()[:nslab]:
        return values, None
    signs = ni_afm_signs(atoms, nslab)
    for index, value in signs.items():
        if seed == "afm_net2":
            values[index] = -0.9583333333 if value < 0 else 1.0416666667
        else:
            values[index] = value
    target = None
    if seed == "contactNi":
        target = nearest_seed_ni(atoms, nslab)
        values[target] = 0.1 if values[target] > 0 else -0.1
    elif seed not in ("afm_balanced", "afm_net2"):
        raise ValueError(f"unknown magnetic seed: {seed}")
    return values, target


def rle(values: Sequence[float]) -> str:
    if not values:
        return ""
    pieces = []
    start = 0
    for index in range(1, len(values) + 1):
        if index == len(values) or values[index] != values[start]:
            count = index - start
            value = f"{values[start]:g}"
            pieces.append(f"{count}*{value}" if count > 1 else value)
            start = index
    return " ".join(pieces)


def kpoints(mesh: Tuple[int, int, int]) -> str:
    return (
        "Gamma-centered mesh\n"
        "0\n"
        "Gamma\n"
        f"{mesh[0]} {mesh[1]} {mesh[2]}\n"
        "0 0 0\n"
    )


def direct_com(atoms) -> Tuple[float, float, float]:
    np, _, _, _ = ase_imports()
    com = np.asarray(atoms.get_center_of_mass(), dtype=float)
    frac = np.linalg.solve(np.asarray(atoms.cell.array, dtype=float).T, com)
    frac[:2] %= 1.0
    frac[2] = min(max(float(frac[2]), 0.0), 1.0)
    return tuple(float(value) for value in frac)


def incar(
    atoms, nslab: int, seed: str, role: str, stage: str, molecule: bool
) -> Tuple[str, int | None]:
    species = present_species(atoms)
    has_ni = "Ni" in species
    values, target = magmom_values(atoms, nslab, seed) if has_ni else ([0.0] * len(atoms), None)
    ldaul = " ".join("2" if element == "Ni" else "-1" for element in species)
    ldauu = " ".join(f"{U_NI_EV:g}" if element == "Ni" else "0" for element in species)
    ldauj = " ".join("0" for _ in species)
    dipol = direct_com(atoms)
    lines = [
        f"SYSTEM = PTFE/LiNiO2 {role} {seed} {stage}",
        "PREC = Accurate",
        "ENCUT = 520",
        "GGA = PE",
        "ALGO = Normal",
        "NELM = 240",
        "NELMIN = 6",
        "ISYM = 0",
        "LASPH = .TRUE.",
        "ADDGRID = .TRUE.",
        "LREAL = .FALSE.",
        "IVDW = 11",
        "ISMEAR = 0",
        "SIGMA = 0.05",
        "ISPIN = 1" if not has_ni else "ISPIN = 2",
        "LORBIT = 11" if has_ni else "LORBIT = 10",
    ]
    if has_ni:
        lines.extend([
            "LDAU = .TRUE.",
            "LDAUTYPE = 2",
            f"LDAUL = {ldaul}",
            f"LDAUU = {ldauu}",
            f"LDAUJ = {ldauj}",
            "LDAUPRINT = 2",
            "LMAXMIX = 4",
            f"MAGMOM = {rle(values)}",
        ])
    lines.extend([
        "LDIPOL = .TRUE.",
        f"IDIPOL = {4 if molecule else 3}",
        f"DIPOL = {dipol[0]:.8f} {dipol[1]:.8f} {dipol[2]:.8f}",
        "AMIN = 0.01",
    ])
    if stage == "relax":
        lines.extend([
            "EDIFF = 1E-5",
            "EDIFFG = -0.02",
            "IBRION = 2",
            "NSW = 120",
            "ISIF = 2",
            "POTIM = 0.30",
            "LWAVE = .TRUE.",
            "LCHARG = .TRUE.",
            "ISTART = 0",
            "ICHARG = 2",
        ])
    elif stage == "static":
        lines.extend([
            "EDIFF = 1E-6",
            "IBRION = -1",
            "NSW = 0",
            "ISIF = 2",
            "LWAVE = .FALSE.",
            "LCHARG = .TRUE.",
            "ISTART = 1",
            "ICHARG = 1",
        ])
    elif stage == "dense":
        lines.extend([
            "EDIFF = 1E-6",
            "IBRION = -1",
            "NSW = 0",
            "ISIF = 2",
            "LWAVE = .FALSE.",
            "LCHARG = .FALSE.",
            # The 2x3x1 WAVECAR is incompatible with the 3x4x1 mesh.  Start
            # orbitals afresh but reuse the converged real-space CHGCAR.
            "ISTART = 0",
            "ICHARG = 1",
        ])
    else:
        raise ValueError(stage)
    return "\n".join(lines) + "\n", target


def write_potcar_spec(path: Path, species: Sequence[str]) -> None:
    lines = ["# POSCAR species order; assemble licensed PAW-PBE POTCAR in this order"]
    lines.extend(f"{element}\t{POTCAR_MAP[element]}" for element in species)
    atomic_text(path, "\n".join(lines) + "\n")


def safe_name(text: str) -> str:
    clean = re.sub(r"[^A-Za-z0-9_.-]+", "_", text).strip("_")
    return clean[:90]


def choose_handoff_rows(payload: Dict[str, Any], scope: str) -> List[Dict[str, Any]]:
    rows = list(payload.get("rows", []))
    matched = [row for row in rows if row.get("geometry_stage") == "rigid_counterfactual"]
    if len(matched) != 4:
        raise SystemExit(f"expected four matched Li/Ni counterfactual rows, found {len(matched)}")
    relaxed_all = [
        row for row in rows
        if row.get("geometry_stage") == "relaxed_shortlist_candidate"
    ]
    counts = Counter(str(row.get("model_name")) for row in relaxed_all)
    insufficient = {
        model: counts.get(model, 0) for model in ("dimer", "c10")
        if counts.get(model, 0) < 3
    }
    if insufficient:
        raise SystemExit(
            "DFT handoff must retain at least three eligible relaxed candidates per fragment; "
            f"found {dict(counts)}"
        )
    selected = list(matched)
    for model in ("dimer", "c10"):
        relaxed = [
            row for row in rows
            if row.get("model_name") == model
            and row.get("geometry_stage") == "relaxed_shortlist_candidate"
        ]
        relaxed.sort(key=lambda row: float(row["relative_pose_score_eV"]))
        if scope == "pilot":
            # Preserve structural diversity rather than using UMA score alone.
            wanted = PILOT_RELAXED_BY_MODEL[model]
            diverse: List[Dict[str, Any]] = []
            seen = set()
            for row in relaxed:
                key = (
                    row.get("basin_id"),
                    row.get("registry_signature"),
                    row.get("azimuth_deg"),
                )
                if key in seen:
                    continue
                seen.add(key)
                diverse.append(row)
                if len(diverse) == wanted:
                    break
            if len(diverse) != wanted:
                raise SystemExit(f"not enough diverse {model} pilot candidates")
            relaxed = diverse
        elif scope != "all":
            raise ValueError(scope)
        selected.extend(relaxed)
    unique: Dict[str, Dict[str, Any]] = {}
    for row in selected:
        key = str(row["handoff_basename"])
        if key in unique:
            raise SystemExit(f"duplicate handoff basename: {key}")
        unique[key] = row
    return list(unique.values())


def source_role(row: Dict[str, Any], relaxed_rank: Dict[Tuple[str, str], int]) -> str:
    if row["geometry_stage"] == "rigid_counterfactual":
        return str(row["site_role"])
    rank = relaxed_rank[(str(row["model_name"]), str(row["handoff_basename"]))]
    return f"uma_relaxed_rank{rank}"


def expected_counts(model: str) -> Counter:
    base = Counter({"Li": 48, "Ni": 48, "O": 96})
    if model == "dimer":
        base.update({"C": 4, "F": 8, "H": 2})
    elif model == "c10":
        base.update({"C": 10, "F": 22})
    elif model != "slab":
        raise ValueError(model)
    return base


def validate_counts(atoms, model: str) -> None:
    found = Counter(atoms.get_chemical_symbols())
    wanted = expected_counts(model)
    if found != wanted:
        raise SystemExit(f"{model} composition mismatch: found {dict(found)}, expected {dict(wanted)}")


def write_job(job_dir: Path, atoms, metadata: Dict[str, Any], nslab: int, seed: str, molecule: bool) -> Dict[str, Any]:
    _, _, _, write = ase_imports()
    job_dir.mkdir(parents=True, exist_ok=False)
    atoms = reorder_atoms(atoms)
    fixed_count = 0
    zcut = None
    if not molecule:
        atoms = expand_surface_cell(atoms)
        fixed_count, zcut = apply_bottom_half_constraint(atoms, nslab)
        if fixed_count != 96:
            raise SystemExit(f"{job_dir.name}: expected exactly 96 fixed slab atoms, got {fixed_count}")
    else:
        atoms.set_constraint()
    poscar = job_dir / "POSCAR"
    write(poscar, atoms, format="vasp", direct=False, sort=False, vasp5=True)
    species = present_species(atoms)
    relax_text, target = incar(
        atoms, nslab, seed, str(metadata["structure_id"]), "relax", molecule
    )
    static_text, _ = incar(
        atoms, nslab, seed, str(metadata["structure_id"]), "static", molecule
    )
    dense_text, _ = incar(
        atoms, nslab, seed, str(metadata["structure_id"]), "dense", molecule
    )
    atomic_text(job_dir / "INCAR.relax", relax_text)
    atomic_text(job_dir / "INCAR.static", static_text)
    atomic_text(job_dir / "INCAR.dense", dense_text)
    atomic_text(job_dir / "KPOINTS", kpoints((1, 1, 1) if molecule else COARSE_MESH))
    atomic_text(job_dir / "KPOINTS.dense", kpoints((1, 1, 1) if molecule else DENSE_MESH))
    write_potcar_spec(job_dir / "POTCAR.spec", species)
    row = {
        **metadata,
        "job_name": job_dir.name,
        "seed": seed,
        "n_atoms": len(atoms),
        "n_slab": nslab,
        "fixed_atoms": fixed_count,
        "zcut_A": zcut,
        "local_seed_Ni_vasp_index_1based": target + 1 if target is not None else None,
        "species_order": " ".join(species),
        "kmesh": "1x1x1" if molecule else "2x3x1",
        "dense_kmesh": "1x1x1" if molecule else "3x4x1",
        "poscar_sha256": sha256(poscar),
        "initial_magmom_sum": sum(magmom_values(atoms, nslab, seed)[0]) if "Ni" in species else 0.0,
        "protocol_role": "molecule" if molecule else "surface",
    }
    atomic_json(job_dir / "SOURCE.json", row)
    return row


def prepare(args) -> int:
    np, _, read, _ = ase_imports()
    uma_out = args.uma_out.resolve()
    vasp_out = args.vasp_out.resolve()
    manifest_path = uma_out / "DFT_HANDOFF.json"
    if not manifest_path.is_file():
        raise SystemExit(f"missing UMA handoff manifest: {manifest_path}")
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not payload.get("gate_passed"):
        raise SystemExit(f"UMA handoff gate failed: {payload.get('gate_failures')}")
    selected = choose_handoff_rows(payload, args.scope)
    gas_inputs = {
        "dimer": PACKAGE_DIR / "inputs" / "ptfe_dimer_c4h2f8.xyz",
        "c10": PACKAGE_DIR / "inputs" / "ptfe_c10f22.xyz",
    }
    support_inputs = {
        name: PACKAGE_DIR / name
        for name in ("vasp_run.sh", "VASP_README_KO.md", "vasp_vendor.conf.example")
    }
    package_commit = "UNRECORDED"
    for candidate in (uma_out / "PACKAGE_COMMIT.txt", uma_out.parent / "PACKAGE_COMMIT.txt"):
        if candidate.is_file():
            package_commit = candidate.read_text(encoding="utf-8").strip() or "UNRECORDED"
            break
    protocol = {
        "vasp_stage_sha256": sha256(Path(__file__).resolve()),
        "uma_handoff_sha256": sha256(manifest_path),
        "uma_protocol_fingerprint": payload.get("protocol_fingerprint", "UNRECORDED"),
        "package_commit": package_commit,
        "gas_input_sha256": {key: sha256(path) for key, path in gas_inputs.items()},
        "support_file_sha256": {key: sha256(path) for key, path in support_inputs.items()},
        "scope": args.scope,
        "u_ni_eV": U_NI_EV,
        "coarse_mesh": COARSE_MESH,
        "dense_mesh": DENSE_MESH,
        "encut_eV": 520,
        "dispersion": "VASP IVDW=11 (D3)",
        "constraint": "bottom half of 192-atom slab fixed; top half and PTFE free",
        "surface_c_A": SURFACE_C_A,
        "force_gate_eV_A": FORCE_GATE_EV_A,
    }
    protocol["fingerprint"] = hashlib.sha256(
        json.dumps(protocol, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if vasp_out.exists():
        verify_input_manifest(vasp_out)
        old = vasp_out / "VASP_PLAN.json"
        if not old.is_file():
            raise SystemExit(f"refusing to overwrite existing non-package directory: {vasp_out}")
        existing = json.loads(old.read_text(encoding="utf-8"))
        if existing.get("protocol", {}).get("fingerprint") != protocol["fingerprint"]:
            raise SystemExit("existing VASP package has a different fingerprint; use a new --vasp-out")
        print(f"matching VASP package already exists: {vasp_out}")
        return 0
    jobs_dir = vasp_out / "jobs"
    jobs_dir.mkdir(parents=True)
    shutil.copy2(manifest_path, vasp_out / "UPSTREAM_DFT_HANDOFF.json")
    atomic_text(vasp_out / "PACKAGE_COMMIT.txt", package_commit + "\n")
    handoff_dir = uma_out / "DFT_HANDOFF"
    first_source = handoff_dir / f"{selected[0]['handoff_basename']}.vasp"
    first_atoms = read(first_source)
    if len(first_atoms) <= N_SLAB:
        raise SystemExit("handoff complex does not contain PTFE atoms")
    slab = first_atoms[:N_SLAB].copy()
    slab.set_cell(first_atoms.cell)
    slab.set_pbc(True)
    slab = reorder_atoms(slab)
    validate_counts(slab, "slab")
    source_slab_positions = np.asarray(first_atoms.positions[:N_SLAB], dtype=float)
    source_cell = np.asarray(first_atoms.cell.array, dtype=float)
    models = {
        "dimer": boxed_molecule(
            PACKAGE_DIR / "inputs" / "ptfe_dimer_c4h2f8.xyz", "dimer", large=True
        ),
        "c10": boxed_molecule(
            PACKAGE_DIR / "inputs" / "ptfe_c10f22.xyz", "c10", large=True
        ),
    }
    jobs: List[Dict[str, Any]] = []
    surface_seeds = ("afm_balanced", "afm_net2")
    for seed in surface_seeds:
        name = f"ref_slab__{seed}"
        jobs.append(write_job(
            jobs_dir / name,
            slab.copy(),
            {
                "structure_id": "ref_slab",
                "role": "clean_slab_reference",
                "model_name": "slab",
                "source": str(first_source),
                "source_handoff_vasp_sha256": sha256(first_source),
                "source_handoff_protocol_fingerprint": payload.get(
                    "protocol_fingerprint", "UNRECORDED"
                ),
            },
            N_SLAB,
            seed,
            False,
        ))
    for model, molecule_atoms in models.items():
        name = f"ref_{model}__closed_shell"
        jobs.append(write_job(
            jobs_dir / name,
            molecule_atoms.copy(),
            {
                "structure_id": f"ref_{model}",
                "role": "isolated_fragment_reference",
                "model_name": model,
                "source": str(gas_inputs[model]),
                "source_xyz_sha256": sha256(gas_inputs[model]),
            },
            0,
            "closed_shell",
            True,
        ))
        if args.scope == "all":
            small = boxed_molecule(
                PACKAGE_DIR / "inputs" / f"ptfe_{'dimer_c4h2f8' if model == 'dimer' else 'c10f22'}.xyz",
                model,
                large=False,
            )
            jobs.append(write_job(
                jobs_dir / f"ref_{model}_boxcheck__closed_shell",
                small,
                {
                    "structure_id": f"ref_{model}_boxcheck",
                    "role": "isolated_fragment_box_check",
                    "model_name": model,
                    "source": str(gas_inputs[model]),
                    "source_xyz_sha256": sha256(gas_inputs[model]),
                },
                0,
                "closed_shell",
                True,
            ))
    relaxed_rank: Dict[Tuple[str, str], int] = {}
    for model in ("dimer", "c10"):
        subset = [row for row in selected if row["model_name"] == model and row["geometry_stage"] == "relaxed_shortlist_candidate"]
        subset.sort(key=lambda row: float(row["relative_pose_score_eV"]))
        for rank, row in enumerate(subset, 1):
            relaxed_rank[(model, str(row["handoff_basename"]))] = rank
    for row in selected:
        source = handoff_dir / f"{row['handoff_basename']}.vasp"
        if not source.is_file():
            raise SystemExit(f"missing handoff POSCAR-format structure: {source}")
        if sha256(source) != row.get("handoff_vasp_sha256"):
            raise SystemExit(f"handoff structure hash mismatch: {source}")
        atoms = read(source)
        model = str(row["model_name"])
        validate_counts(atoms, model)
        if not np.allclose(np.asarray(atoms.cell.array, dtype=float), source_cell, atol=1.0e-8):
            raise SystemExit(f"handoff cell differs across candidates: {source}")
        if not np.allclose(
            np.asarray(atoms.positions[:N_SLAB], dtype=float), source_slab_positions, atol=1.0e-6
        ):
            raise SystemExit(f"frozen UMA slab coordinates differ across candidates: {source}")
        role = source_role(row, relaxed_rank)
        structure_hash = sha256(source)[:10]
        structure_id = safe_name(f"cmp_{model}_{role}_{structure_hash}")
        for seed in surface_seeds:
            name = safe_name(f"{structure_id}__{seed}")
            jobs.append(write_job(
                jobs_dir / name,
                atoms.copy(),
                {
                    "structure_id": structure_id,
                    "role": role,
                    "model_name": model,
                    "site_role": row.get("site_role", ""),
                    "initial_site": row.get("initial_site", ""),
                    "azimuth_deg": row.get("azimuth_deg"),
                    "roll_deg": row.get("roll_deg"),
                    "uma_pose_id": row.get("pose_id"),
                    "uma_basin_id": row.get("basin_id"),
                    "uma_relative_pose_score_eV": row.get("relative_pose_score_eV"),
                    "source": str(source),
                    "source_handoff_vasp_sha256": row.get("handoff_vasp_sha256"),
                    "source_handoff_xyz_sha256": row.get("handoff_xyz_sha256"),
                    "source_handoff_protocol_fingerprint": payload.get(
                        "protocol_fingerprint", "UNRECORDED"
                    ),
                },
                N_SLAB,
                seed,
                False,
            ))
    plan = {
        "protocol": protocol,
        "uma_out": str(uma_out),
        "scope": args.scope,
        "job_templates": len(jobs),
        "vasp_executions_before_dense": 2 * len(jobs),
        "jobs": jobs,
        "warning": "VASP DFT+U+D3 validation matrix; POTCAR is not distributed.",
    }
    atomic_json(vasp_out / "VASP_PLAN.json", plan)
    atomic_csv(vasp_out / "VASP_PLAN.csv", jobs)
    atomic_text(
        vasp_out / "README_GENERATED.md",
        "# Generated PTFE/LiNiO2 VASP validation matrix\n\n"
        f"- Scope: `{args.scope}`\n"
        f"- Job templates: {len(jobs)}\n"
        f"- Relax + static executions: {2 * len(jobs)}\n"
        "- Each surface structure has canonical-QE AFM and net-2 ferrimagnetic starts.\n"
        "- Molecules are closed-shell Gamma jobs.\n"
        "- Use `vasp_run.sh`; do not add POTCAR files to the returned archive.\n",
    )
    for name in ("vasp_run.sh", "VASP_README_KO.md", "vasp_vendor.conf.example"):
        source = PACKAGE_DIR / name
        if not source.is_file():
            raise SystemExit(f"package support file is missing: {source}")
        shutil.copy2(source, vasp_out / name)
    shutil.copy2(Path(__file__).resolve(), vasp_out / "vasp_stage.py")
    write_input_manifest(vasp_out)
    print(json.dumps({"vasp_out": str(vasp_out), "job_templates": len(jobs), "executions": 2 * len(jobs), "scope": args.scope}, indent=2))
    return 0


FLOAT = r"[-+]?\d+(?:\.\d*)?(?:[Ee][-+]?\d+)?"


def parse_outcar(path: Path, require_relax: bool = False) -> Dict[str, Any]:
    if not path.is_file():
        return {"complete": False, "reason": "missing OUTCAR"}
    text = path.read_text(encoding="utf-8", errors="ignore")
    complete = "General timing and accounting" in text
    scf_ok = "aborting loop because EDIFF is reached" in text
    e0_matches = re.findall(r"energy\s+without entropy=\s*(%s).*?energy\(sigma->0\)\s*=\s*(%s)" % (FLOAT, FLOAT), text)
    toten_matches = re.findall(r"free\s+energy\s+TOTEN\s*=\s*(%s)" % FLOAT, text)
    ionic_ok = "reached required accuracy - stopping structural energy minimisation" in text
    force_blocks = [match.end() for match in re.finditer(r"TOTAL-FORCE \(eV/Angst\)", text)]
    forces: List[List[float]] = []
    if force_blocks:
        for line in text[force_blocks[-1]:].splitlines()[2:]:
            fields = line.split()
            if len(fields) < 6:
                if forces:
                    break
                continue
            try:
                forces.append([float(fields[3]), float(fields[4]), float(fields[5])])
            except ValueError:
                if forces:
                    break
    moment_starts = [
        match.end() for match in re.finditer(r"^\s*magnetization \(x\)\s*$", text, re.M)
    ]
    moments: Dict[int, float] = {}
    if moment_starts:
        for line in text[moment_starts[-1]:].splitlines():
            match = re.match(
                rf"^\s*(\d+)\s+{FLOAT}\s+{FLOAT}\s+{FLOAT}\s+({FLOAT})\s*$", line
            )
            if match:
                moments[int(match.group(1))] = float(match.group(2))
            elif moments and re.match(r"^\s*tot\s+", line):
                break
    system_matches = re.findall(r"^\s*SYSTEM\s*=\s*(.*?)\s*$", text, re.M)
    nions_matches = re.findall(r"\bNIONS\s*=\s*(\d+)", text)
    nkpts_matches = re.findall(r"\bNKPTS\s*=\s*(\d+)", text)
    ivdw_matches = re.findall(r"\bIVDW\s*=\s*(-?\d+)", text)
    ldauu_matches = re.findall(r"^\s*LDAUU\s*=\s*([^\r\n]+)", text, re.M)
    version_matches = re.findall(r"\b(vasp\.\d+(?:\.\d+)+[^\s]*)", text, re.I)
    result = {
        "complete": bool(complete and e0_matches and toten_matches and scf_ok),
        "terminated": complete,
        "scf_converged": scf_ok,
        "ionic_converged": ionic_ok if require_relax else None,
        "E0_eV": float(e0_matches[-1][1]) if e0_matches else None,
        "energy_without_entropy_eV": float(e0_matches[-1][0]) if e0_matches else None,
        "TOTEN_eV": float(toten_matches[-1]) if toten_matches else None,
        "forces_eV_A": forces,
        "magnetization_x": moments,
        "ldau_occupation_present": bool(
            re.search(r"occup(?:ation|ancy) matrix", text, re.I)
        ),
        "system": system_matches[-1] if system_matches else None,
        "nions": int(nions_matches[-1]) if nions_matches else None,
        "nkpts": int(nkpts_matches[-1]) if nkpts_matches else None,
        "ivdw": int(ivdw_matches[-1]) if ivdw_matches else None,
        "ldauu_eV": (
            [float(value) for value in re.findall(FLOAT, ldauu_matches[-1])]
            if ldauu_matches else []
        ),
        "vasp_version": version_matches[-1] if version_matches else None,
    }
    if require_relax and not ionic_ok:
        result["complete"] = False
        result["reason"] = "ionic relaxation did not reach EDIFFG"
    elif not result["complete"]:
        result["reason"] = "termination/energy/SCF gate failed"
    return result


def protocol_audit(job: Dict[str, Any], parsed: Dict[str, Any], stage: str) -> Dict[str, Any]:
    reasons: List[str] = []
    expected_system = f"PTFE/LiNiO2 {job['structure_id']} {job['seed']} {stage}"
    expected_nkpts = 1 if job["protocol_role"] == "molecule" else (
        int(DENSE_MESH[0] * DENSE_MESH[1] * DENSE_MESH[2])
        if stage == "dense"
        else int(COARSE_MESH[0] * COARSE_MESH[1] * COARSE_MESH[2])
    )
    if parsed.get("system") != expected_system:
        reasons.append(f"SYSTEM mismatch: {parsed.get('system')!r}")
    if parsed.get("nions") != int(job["n_atoms"]):
        reasons.append(f"NIONS mismatch: {parsed.get('nions')!r}")
    if parsed.get("nkpts") != expected_nkpts:
        reasons.append(f"NKPTS mismatch: {parsed.get('nkpts')!r}, expected {expected_nkpts}")
    if parsed.get("ivdw") != 11:
        reasons.append(f"IVDW mismatch: {parsed.get('ivdw')!r}")
    if job["protocol_role"] == "surface":
        if not any(abs(float(value) - U_NI_EV) <= 1.0e-6 for value in parsed.get("ldauu_eV", [])):
            reasons.append(f"Ni LDAUU={U_NI_EV:g} eV not found")
    return {
        "protocol_ok": not reasons,
        "protocol_reason": "; ".join(reasons),
    }


def load_plan(vasp_out: Path) -> Dict[str, Any]:
    path = vasp_out / "VASP_PLAN.json"
    if not path.is_file():
        raise SystemExit(f"missing VASP plan: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def pair_min(atoms, left: Sequence[int], right: Sequence[int]) -> Tuple[float, int, int]:
    np, _, _, _ = ase_imports()
    best = (float("inf"), -1, -1)
    for index in left:
        distances = np.asarray(atoms.get_distances(index, right, mic=True), dtype=float)
        local = int(np.argmin(distances))
        candidate = (float(distances[local]), index, int(right[local]))
        if candidate < best:
            best = candidate
    return best


def molecule_image_clearance(atoms, nslab: int) -> float:
    np, _, _, _ = ase_imports()
    positions = np.asarray(atoms.positions[nslab:], dtype=float)
    cell = np.asarray(atoms.cell.array, dtype=float)
    best = float("inf")
    for ia in (-1, 0, 1):
        for ib in (-1, 0, 1):
            if ia == ib == 0:
                continue
            shifted = positions + ia * cell[0] + ib * cell[1]
            distances = np.linalg.norm(positions[:, None, :] - shifted[None, :, :], axis=2)
            best = min(best, float(distances.min()))
    return best


def bond_audit(initial, final) -> Dict[str, Any]:
    np, _, _, _ = ase_imports()
    symbols = initial.get_chemical_symbols()
    if symbols != final.get_chemical_symbols():
        return {"topology_ok": False, "reason": "molecule atom order changed"}
    initial_d = np.asarray(initial.get_all_distances(mic=False), dtype=float)
    final_d = np.asarray(final.get_all_distances(mic=False), dtype=float)
    formation = {("C", "C"): 1.75, ("C", "F"): 1.55, ("C", "H"): 1.25}
    upper = {("C", "C"): 1.90, ("C", "F"): 1.70, ("C", "H"): 1.35}
    lower = {("C", "C"): 1.20, ("C", "F"): 1.10, ("C", "H"): 0.85}
    broken: List[str] = []
    formed: List[str] = []
    short: List[str] = []
    max_cf = 0.0
    for i in range(len(initial)):
        for j in range(i + 1, len(initial)):
            pair = tuple(sorted((symbols[i], symbols[j])))
            if pair not in formation:
                continue
            label = f"{symbols[i]}{i + 1}-{symbols[j]}{j + 1}"
            was_bonded = initial_d[i, j] <= formation[pair]
            if was_bonded and final_d[i, j] > upper[pair]:
                broken.append(label)
            if not was_bonded and final_d[i, j] <= formation[pair]:
                formed.append(label)
            if was_bonded and final_d[i, j] < lower[pair]:
                short.append(label)
            if was_bonded and pair == ("C", "F"):
                max_cf = max(max_cf, float(final_d[i, j]))
    return {
        "topology_ok": not (broken or formed or short),
        "broken_bonds": broken,
        "formed_bonds": formed,
        "too_short_bonds": short,
        "max_C_F_A": max_cf,
    }


def fixed_indices_from_atoms(atoms) -> List[int]:
    indices: List[int] = []
    for constraint in atoms.constraints:
        getter = getattr(constraint, "get_indices", None)
        if getter is not None:
            indices.extend(int(index) for index in getter())
    return sorted(set(indices))


def surface_reconstruction_audit(
    complex_contcar: Path, clean_contcar: Path, initial_poscar: Path
) -> Dict[str, Any]:
    np, _, read, _ = ase_imports()
    try:
        complex_atoms = read(complex_contcar)
        clean_atoms = read(clean_contcar)
        initial = read(initial_poscar)
    except Exception as exc:
        return {
            "surface_reconstruction_ok": False,
            "surface_reconstruction_reason": f"surface reference read failed: {exc}",
        }
    if len(complex_atoms) < N_SLAB or len(clean_atoms) != N_SLAB:
        return {
            "surface_reconstruction_ok": False,
            "surface_reconstruction_reason": "clean/complex slab atom count mismatch",
        }
    if complex_atoms.get_chemical_symbols()[:N_SLAB] != clean_atoms.get_chemical_symbols():
        return {
            "surface_reconstruction_ok": False,
            "surface_reconstruction_reason": "clean/complex slab atom order mismatch",
        }
    cell = np.asarray(clean_atoms.cell.array, dtype=float)
    if not np.allclose(np.asarray(complex_atoms.cell.array, dtype=float), cell, atol=1.0e-8):
        return {
            "surface_reconstruction_ok": False,
            "surface_reconstruction_reason": "clean/complex surface cells differ",
        }
    fixed = set(fixed_indices_from_atoms(initial))
    free_slab = [index for index in range(N_SLAB) if index not in fixed]
    delta = (
        np.asarray(complex_atoms.positions[:N_SLAB], dtype=float)
        - np.asarray(clean_atoms.positions, dtype=float)
    )
    fractional = np.linalg.solve(cell.T, delta.T).T
    fractional[:, :2] -= np.round(fractional[:, :2])
    displacement = np.linalg.norm(fractional @ cell, axis=1)
    symbols = clean_atoms.get_chemical_symbols()
    maxima = {
        element: max(
            (float(displacement[index]) for index in free_slab if symbols[index] == element),
            default=0.0,
        )
        for element in ("Li", "Ni", "O")
    }
    li_indices = [index for index in free_slab if symbols[index] == "Li"]
    o_indices = [index for index in range(N_SLAB) if symbols[index] == "O"]
    max_coordination_loss = 0
    for index in li_indices:
        clean_count = int(
            sum(
                distance <= SURFACE_LI_O_COORDINATION_CUTOFF_A
                for distance in clean_atoms.get_distances(index, o_indices, mic=True)
            )
        )
        complex_count = int(
            sum(
                distance <= SURFACE_LI_O_COORDINATION_CUTOFF_A
                for distance in complex_atoms.get_distances(index, o_indices, mic=True)
            )
        )
        max_coordination_loss = max(max_coordination_loss, clean_count - complex_count)
    reasons: List[str] = []
    if maxima["Li"] > SURFACE_LI_DISPLACEMENT_MAX_A:
        reasons.append("top-layer Li extraction/reconstruction relative to clean slab")
    if maxima["Ni"] > SURFACE_NI_O_DISPLACEMENT_MAX_A:
        reasons.append("top-layer Ni reconstruction relative to clean slab")
    if maxima["O"] > SURFACE_NI_O_DISPLACEMENT_MAX_A:
        reasons.append("top-layer O reconstruction relative to clean slab")
    if max_coordination_loss > SURFACE_LI_O_MAX_COORDINATION_LOSS:
        reasons.append("top-layer Li lost multiple O neighbors")
    return {
        "surface_reconstruction_ok": not reasons,
        "surface_reconstruction_reason": "; ".join(reasons),
        "surface_vs_clean_max_Li_displacement_A": maxima["Li"],
        "surface_vs_clean_max_Ni_displacement_A": maxima["Ni"],
        "surface_vs_clean_max_O_displacement_A": maxima["O"],
        "surface_vs_clean_max_Li_O_coordination_loss": max_coordination_loss,
    }


def geometry_audit(job_dir: Path, job: Dict[str, Any], static: Dict[str, Any]) -> Dict[str, Any]:
    np, _, read, _ = ase_imports()
    path = job_dir / "relax" / "CONTCAR"
    if not path.is_file() or path.stat().st_size == 0:
        return {"geometry_ok": False, "geometry_reason": "missing relax/CONTCAR"}
    try:
        final = read(path)
        initial = read(job_dir / "POSCAR")
    except Exception as exc:
        return {"geometry_ok": False, "geometry_reason": f"structure read failed: {exc}"}
    if len(final) != int(job["n_atoms"]) or len(initial) != len(final):
        return {"geometry_ok": False, "geometry_reason": "atom count changed"}
    if not np.isfinite(np.asarray(final.positions, dtype=float)).all():
        return {"geometry_ok": False, "geometry_reason": "non-finite CONTCAR coordinates"}
    fixed_indices = fixed_indices_from_atoms(initial)
    fixed_set = set(fixed_indices)
    cell_drift = float(
        np.max(
            np.abs(
                np.asarray(final.cell.array, dtype=float)
                - np.asarray(initial.cell.array, dtype=float)
            )
        )
    )
    fixed_max_displacement = (
        max(
            float(
                np.linalg.norm(
                    np.asarray(final.positions[index], dtype=float)
                    - np.asarray(initial.positions[index], dtype=float)
                )
            )
            for index in fixed_indices
        )
        if fixed_indices else 0.0
    )
    forces = static.get("forces_eV_A") or []
    free_indices: List[int] = []
    if len(forces) == len(final):
        if job["protocol_role"] == "molecule":
            free_indices = list(range(len(final)))
        else:
            free_indices = [index for index in range(len(final)) if index not in fixed_set]
        max_force = max(
            float(np.linalg.norm(np.asarray(forces[index], dtype=float)))
            for index in free_indices
        )
    else:
        max_force = None
    result: Dict[str, Any] = {
        "final_contcar_sha256": sha256(path),
        "free_atom_max_force_eV_A": max_force,
        "force_gate_ok": max_force is not None and max_force <= FORCE_GATE_EV_A + 1.0e-8,
        "cell_max_abs_drift_A": cell_drift,
        "fixed_atom_count_from_POSCAR": len(fixed_indices),
        "fixed_atom_max_displacement_A": fixed_max_displacement,
        "final_registry": "not_applicable",
        "geometry_ok": True,
        "geometry_reason": "",
    }
    if job["protocol_role"] == "molecule":
        bonds = bond_audit(initial, final)
        lateral = molecule_image_clearance(final, 0)
        vertical = float(final.cell.lengths()[2] + final.positions[:, 2].min() - final.positions[:, 2].max())
        reasons: List[str] = []
        if not result["force_gate_ok"]:
            reasons.append("final free-atom force exceeds 0.02 eV/A or is missing")
        if not bonds.get("topology_ok") or float(bonds.get("max_C_F_A", 0.0)) > 1.70:
            reasons.append("gas-fragment bond topology/length changed")
        if lateral < 8.0 or vertical < 8.0:
            reasons.append("gas-fragment periodic-image clearance failed")
        if cell_drift > 1.0e-8:
            reasons.append("gas cell changed despite fixed-cell protocol")
        result.update({
            "geometry_ok": not reasons,
            "geometry_reason": "; ".join(reasons),
            "lateral_image_min_A": lateral,
            "vertical_image_min_A": vertical,
            **bonds,
        })
        return result
    if job["role"] == "clean_slab_reference":
        reasons: List[str] = []
        if not result["force_gate_ok"]:
            reasons.append("final free-atom force exceeds 0.02 eV/A or is missing")
        if len(fixed_indices) != int(job["fixed_atoms"]):
            reasons.append("Selective-Dynamics fixed-atom count changed")
        if fixed_max_displacement > 1.0e-6:
            reasons.append("fixed slab atoms moved")
        if cell_drift > 1.0e-8:
            reasons.append("surface cell changed despite ISIF=2")
        result["geometry_ok"] = not reasons
        result["geometry_reason"] = "; ".join(reasons)
        return result
    symbols = final.get_chemical_symbols()
    f_indices = [index for index in range(N_SLAB, len(final)) if symbols[index] == "F"]
    c_indices = [index for index in range(N_SLAB, len(final)) if symbols[index] == "C"]
    h_indices = [index for index in range(N_SLAB, len(final)) if symbols[index] == "H"]
    li_indices = [index for index in range(N_SLAB) if symbols[index] == "Li"]
    ni_indices = [index for index in range(N_SLAB) if symbols[index] == "Ni"]
    o_indices = [index for index in range(N_SLAB) if symbols[index] == "O"]
    mol_indices = list(range(N_SLAB, len(final)))
    min_li = pair_min(final, f_indices, li_indices)
    min_ni = pair_min(final, f_indices, ni_indices)
    min_o = pair_min(final, f_indices, o_indices)
    contact_li = sum(
        int(float(np.asarray(final.get_distances(index, li_indices, mic=True)).min()) <= 2.8)
        for index in f_indices
    )
    contact_ni = sum(
        int(float(np.asarray(final.get_distances(index, ni_indices, mic=True)).min()) <= 2.8)
        for index in f_indices
    )
    contact_o = sum(
        int(float(np.asarray(final.get_distances(index, o_indices, mic=True)).min()) <= 2.5)
        for index in f_indices
    )
    # Registry is a contact/nearest-site label, not a claim of a short chemical
    # bond.  O-dominated and ambiguous/hollow geometries must not be forced
    # into the Li-vs-Ni contrast merely because one cation is slightly nearer.
    active_contacts = [
        label for label, count in (("Li", contact_li), ("Ni", contact_ni), ("O", contact_o))
        if count > 0
    ]
    if len(active_contacts) > 1:
        registry = "mixed"
        registry_basis = "multi-element F contacts"
    elif active_contacts == ["Li"]:
        registry = "Li"
        registry_basis = "exclusive multi-F Li contact"
    elif active_contacts == ["Ni"]:
        registry = "Ni"
        registry_basis = "exclusive multi-F Ni contact"
    elif active_contacts == ["O"]:
        registry = "O"
        registry_basis = "exclusive multi-F O contact"
    elif min_o[0] + 0.15 < min(min_li[0], min_ni[0]):
        registry = "O"
        registry_basis = "nearest-F distance"
    elif min_li[0] + 0.15 < min(min_ni[0], min_o[0]):
        registry = "Li"
        registry_basis = "nearest-F distance"
    elif min_ni[0] + 0.15 < min(min_li[0], min_o[0]):
        registry = "Ni"
        registry_basis = "nearest-F distance"
    else:
        registry = "other"
        registry_basis = "no exclusive Li/Ni/O registry"
    molecule_slab = pair_min(final, mol_indices, list(range(N_SLAB)))[0]
    min_c_li = pair_min(final, c_indices, li_indices)[0]
    min_c_ni = pair_min(final, c_indices, ni_indices)[0]
    min_c_o = pair_min(final, c_indices, o_indices)[0]
    vertical = float(final.cell.lengths()[2] + final.positions[:, 2].min() - final.positions[:, 2].max())
    lateral = molecule_image_clearance(final, N_SLAB)
    bonds = bond_audit(initial[N_SLAB:], final[N_SLAB:])
    h_min = pair_min(final, h_indices, list(range(N_SLAB)))[0] if h_indices else None
    closest_element = min(
        (
            pair_min(final, [index], list(range(N_SLAB)))[0],
            symbols[index],
        )
        for index in mol_indices
    )[1]
    reasons: List[str] = []
    if not result["force_gate_ok"]:
        reasons.append("final free-atom force exceeds 0.02 eV/A or is missing")
    if len(fixed_indices) != int(job["fixed_atoms"]):
        reasons.append("Selective-Dynamics fixed-atom count changed")
    if fixed_max_displacement > 1.0e-6:
        reasons.append("fixed slab atoms moved")
    if cell_drift > 1.0e-8:
        reasons.append("surface cell changed despite ISIF=2")
    if not bonds.get("topology_ok") or float(bonds.get("max_C_F_A", 0.0)) > 1.70:
        reasons.append("PTFE bond topology/length changed")
    if molecule_slab < 1.5:
        reasons.append("molecule-slab clash <1.5 A")
    if molecule_slab > 4.0:
        reasons.append("fragment detached: molecule-slab minimum >4.0 A")
    if lateral < 4.5 or vertical < 8.0:
        reasons.append("periodic-image clearance failed")
    if min_c_ni < 2.1 or min_c_li < 2.1 or min_c_o < 1.8:
        reasons.append("reaction-like surface-carbon contact")
    if min_ni[0] < 1.8 or min_o[0] < 1.6:
        reasons.append("reaction-like F-Ni/O contact")
    if job["model_name"] == "dimer" and (
        closest_element == "H" or (h_min is not None and h_min < 1.8)
    ):
        reasons.append("artificial H cap controls the contact")
    result.update({
        "geometry_ok": not reasons,
        "geometry_reason": "; ".join(reasons),
        "final_registry": registry,
        "final_registry_basis": registry_basis,
        "min_F_Li_A": min_li[0],
        "min_F_Ni_A": min_ni[0],
        "min_F_O_A": min_o[0],
        "contact_F_Li_count": contact_li,
        "contact_F_Ni_count": contact_ni,
        "contact_F_O_count": contact_o,
        "min_molecule_slab_A": molecule_slab,
        "lateral_image_min_A": lateral,
        "vertical_image_min_A": vertical,
        "min_H_slab_A": h_min,
        **bonds,
    })
    return result


def magnetic_audit(job: Dict[str, Any], static: Dict[str, Any], job_dir: Path) -> Dict[str, Any]:
    if job["protocol_role"] == "molecule":
        return {"ni_moment_count": 0, "magnetic_table_ok": True, "magnetic_review": False}
    _, _, read, _ = ase_imports()
    atoms = read(job_dir / "POSCAR")
    expected, _ = magmom_values(atoms, N_SLAB, str(job["seed"]))
    moments = static.get("magnetization_x") or {}
    ni_indices = [index for index, symbol in enumerate(atoms.get_chemical_symbols()) if symbol == "Ni"]
    values = [moments.get(index + 1) for index in ni_indices]
    complete = len(values) == 48 and all(value is not None for value in values)
    flips = 0
    small = 0
    if complete:
        for index, value in zip(ni_indices, values):
            assert value is not None
            if abs(float(value)) <= 0.2:
                small += 1
            elif float(value) * float(expected[index]) < 0:
                flips += 1
    return {
        "ni_moment_count": sum(value is not None for value in values),
        "ni_small_moment_count": small if complete else None,
        "ni_sign_flip_count": flips if complete else None,
        "magnetic_table_ok": complete,
        "magnetic_review": (not complete) or flips > 0 or small > 0,
        "ldau_occupation_present": bool(static.get("ldau_occupation_present")),
    }


def seed_spreads(rows: Sequence[Dict[str, Any]], energy_key: str) -> Dict[str, float]:
    grouped: Dict[str, List[float]] = defaultdict(list)
    for row in rows:
        if row.get(energy_key) is not None and str(row["structure_id"]).startswith("cmp_"):
            grouped[str(row["structure_id"])].append(float(row[energy_key]))
    return {
        key: max(values) - min(values) if len(values) > 1 else 0.0
        for key, values in grouped.items()
    }


def best_row(rows: Sequence[Dict[str, Any]], predicate, energy_key: str) -> Dict[str, Any] | None:
    subset = [row for row in rows if predicate(row) and row.get(energy_key) is not None]
    return min(subset, key=lambda row: float(row[energy_key])) if subset else None


def compute_metrics(
    rows: Sequence[Dict[str, Any]], energy_key: str, gas_reference: Dict[str, float] | None = None
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    slab = best_row(rows, lambda row: row["role"] == "clean_slab_reference", energy_key)
    if gas_reference is None:
        gas_reference = {}
        for model in ("dimer", "c10"):
            ref = best_row(
                rows,
                lambda row, model=model: row["model_name"] == model
                and row["role"] == "isolated_fragment_reference",
                energy_key,
            )
            if ref is not None:
                gas_reference[model] = float(ref[energy_key])
    if slab is None or set(gas_reference) != {"dimer", "c10"}:
        return [], {"complete": False, "reason": "slab/gas reference energies incomplete"}
    slab_e = float(slab[energy_key])
    spreads = seed_spreads(rows, energy_key)
    adsorption: List[Dict[str, Any]] = []
    for row in rows:
        if not str(row["structure_id"]).startswith("cmp_") or row.get(energy_key) is None:
            continue
        model = str(row["model_name"])
        adsorption.append({
            "structure_id": row["structure_id"],
            "model_name": model,
            "role": row["role"],
            "site_role": row.get("site_role", ""),
            "job_name": row["job_name"],
            "seed": row["seed"],
            "final_registry": row.get("final_registry"),
            "E_complex_eV": row[energy_key],
            "E_ads_eV": float(row[energy_key]) - slab_e - gas_reference[model],
            "seed_spread_eV": spreads.get(str(row["structure_id"]), 0.0),
            "uma_pose_id": row.get("uma_pose_id"),
            "magnetic_review": row.get("magnetic_review"),
        })
    adsorption.sort(key=lambda row: (str(row["model_name"]), float(row["E_ads_eV"])))
    site: Dict[str, Any] = {}
    for model in ("dimer", "c10"):
        subset = [row for row in adsorption if row["model_name"] == model]
        global_min = min(subset, key=lambda row: float(row["E_ads_eV"])) if subset else None
        sampled_li = best_row(subset, lambda row: row["final_registry"] == "Li", "E_ads_eV")
        sampled_ni = best_row(subset, lambda row: row["final_registry"] == "Ni", "E_ads_eV")
        matched_li = best_row(
            subset,
            lambda row: row["role"] == "matched_Li_counterfactual"
            and row["final_registry"] == "Li",
            "E_ads_eV",
        )
        matched_ni = best_row(
            subset,
            lambda row: row["role"] == "matched_Ni_counterfactual"
            and row["final_registry"] == "Ni",
            "E_ads_eV",
        )
        if not all((sampled_li, sampled_ni, matched_li, matched_ni)):
            site[model] = {
                "blocked": "DFT-relaxed distinct Li and Ni basins were not both retained",
                "global_lowest_registry": global_min["final_registry"] if global_min else None,
                "global_lowest_job": global_min["job_name"] if global_min else None,
                "sampled_Li_present": sampled_li is not None,
                "sampled_Ni_present": sampled_ni is not None,
                "matched_Li_retained": matched_li is not None,
                "matched_Ni_retained": matched_ni is not None,
            }
            continue
        assert sampled_li and sampled_ni and matched_li and matched_ni
        sampled_gap = float(sampled_ni["E_ads_eV"]) - float(sampled_li["E_ads_eV"])
        matched_gap = float(matched_ni["E_ads_eV"]) - float(matched_li["E_ads_eV"])
        site[model] = {
            "quantity": "Li-vs-Ni nearest-F contact contrast within the sampled candidates",
            "sampled_DeltaE_Ni_minus_Li_eV": sampled_gap,
            "matched_DeltaE_Ni_minus_Li_eV": matched_gap,
            "sampled_lower_registry": "Li" if sampled_gap > 0 else "Ni",
            "matched_lower_registry": "Li" if matched_gap > 0 else "Ni",
            "sampled_Li_job": sampled_li["job_name"],
            "sampled_Ni_job": sampled_ni["job_name"],
            "matched_Li_job": matched_li["job_name"],
            "matched_Ni_job": matched_ni["job_name"],
            "max_seed_spread_eV": max(
                float(sampled_li["seed_spread_eV"]),
                float(sampled_ni["seed_spread_eV"]),
                float(matched_li["seed_spread_eV"]),
                float(matched_ni["seed_spread_eV"]),
            ),
            "magnetic_review": any(
                bool(row.get("magnetic_review"))
                for row in (sampled_li, sampled_ni, matched_li, matched_ni)
            ),
            "global_lowest_registry": global_min["final_registry"],
            "global_lowest_job": global_min["job_name"],
            "global_lowest_E_ads_eV": global_min["E_ads_eV"],
        }
    return adsorption, {
        "complete": True,
        "surface_reference_job": slab["job_name"],
        "gas_reference_eV": gas_reference,
        "li_vs_ni_contact_contrast": site,
    }


def dense_selection(rows: Sequence[Dict[str, Any]], adsorption: Sequence[Dict[str, Any]]) -> List[str]:
    selected: set[str] = set()
    slab_rows = [row for row in rows if row["role"] == "clean_slab_reference"]
    if slab_rows:
        # There are only two slab magnetic starts.  Dense-check both so a
        # k-dependent magnetic winner switch cannot contaminate absolute Eads.
        selected.update(str(row["job_name"]) for row in slab_rows)
    complex_rows = [row for row in rows if str(row["structure_id"]).startswith("cmp_")]
    selected.update(
        str(row["job_name"])
        for row in complex_rows
        if row["role"] in ("matched_Li_counterfactual", "matched_Ni_counterfactual")
    )
    for model in ("dimer", "c10"):
        subset = [row for row in adsorption if row["model_name"] == model]
        if not subset:
            continue
        floor = min(float(row["E_ads_eV"]) for row in subset)
        finalists = {
            str(row["job_name"])
            for row in subset
            if float(row["E_ads_eV"]) <= floor + FINALIST_WINDOW_EV
        }
        for registry in ("Li", "Ni", "O", "other", "mixed"):
            registry_rows = [row for row in subset if row["final_registry"] == registry]
            if registry_rows:
                finalists.add(str(min(registry_rows, key=lambda row: float(row["E_ads_eV"]))["job_name"]))
        structures = {
            str(row["structure_id"])
            for row in subset if str(row["job_name"]) in finalists
        }
        selected.update(
            str(row["job_name"])
            for row in complex_rows if str(row["structure_id"]) in structures
        )
    return sorted(selected)


def analyze(args) -> int:
    vasp_out = args.vasp_out.resolve()
    plan = load_plan(vasp_out)
    rows: List[Dict[str, Any]] = []
    for job in plan["jobs"]:
        job_dir = vasp_out / "jobs" / job["job_name"]
        relax = parse_outcar(job_dir / "relax" / "OUTCAR", require_relax=True)
        static = parse_outcar(job_dir / "static" / "OUTCAR")
        row = {**job}
        for prefix, parsed in (("relax", relax), ("static", static)):
            for key, value in parsed.items():
                if key not in ("forces_eV_A", "magnetization_x"):
                    row[f"{prefix}_{key}"] = value
            audit = protocol_audit(job, parsed, prefix)
            row[f"{prefix}_protocol_ok"] = audit["protocol_ok"]
            row[f"{prefix}_protocol_reason"] = audit["protocol_reason"]
        if relax.get("complete") and static.get("complete"):
            row.update(geometry_audit(job_dir, job, static))
            row.update(magnetic_audit(job, static, job_dir))
        else:
            row.update({
                "geometry_ok": False,
                "geometry_reason": "relax/static electronic or ionic completion gate failed",
                "magnetic_table_ok": False,
                "magnetic_review": True,
            })
        row["analysis_eligible"] = bool(
            relax.get("complete")
            and static.get("complete")
            and row.get("relax_protocol_ok")
            and row.get("static_protocol_ok")
            and row.get("geometry_ok")
            and row.get("magnetic_table_ok")
        )
        rows.append(row)
    clean_by_seed = {
        str(row["seed"]): vasp_out / "jobs" / str(row["job_name"]) / "relax" / "CONTCAR"
        for row in rows if row.get("role") == "clean_slab_reference"
    }
    for row in rows:
        if row.get("protocol_role") == "surface" and row.get("role") != "clean_slab_reference":
            clean_path = clean_by_seed.get(str(row["seed"]))
            if clean_path is None:
                reconstruction = {
                    "surface_reconstruction_ok": False,
                    "surface_reconstruction_reason": "matching clean-slab magnetic seed is missing",
                }
            else:
                reconstruction = surface_reconstruction_audit(
                    vasp_out / "jobs" / str(row["job_name"]) / "relax" / "CONTCAR",
                    clean_path,
                    vasp_out / "jobs" / str(row["job_name"]) / "POSCAR",
                )
            row.update(reconstruction)
            if not reconstruction["surface_reconstruction_ok"]:
                prior = str(row.get("geometry_reason", "")).strip()
                reason = str(reconstruction.get("surface_reconstruction_reason", "")).strip()
                row["geometry_ok"] = False
                row["geometry_reason"] = "; ".join(value for value in (prior, reason) if value)
        row["analysis_eligible"] = bool(
            row.get("relax_complete")
            and row.get("static_complete")
            and row.get("relax_protocol_ok")
            and row.get("static_protocol_ok")
            and row.get("geometry_ok")
            and row.get("magnetic_table_ok")
        )
    atomic_csv(vasp_out / "VASP_RESULTS.csv", rows)
    all_complete = all(
        bool(row.get("relax_complete")) and bool(row.get("static_complete")) for row in rows
    )
    all_geometry_ok = all(bool(row.get("geometry_ok")) for row in rows)
    all_magnetic_tables = all(bool(row.get("magnetic_table_ok")) for row in rows)
    all_force_gates = all(bool(row.get("force_gate_ok")) for row in rows)
    all_protocol_gates = all(
        bool(row.get("relax_protocol_ok")) and bool(row.get("static_protocol_ok"))
        for row in rows
    )
    raw_eligible = [row for row in rows if row["analysis_eligible"]]

    # A surface energy is usable only as a complete two-seed unit.  Silently
    # retaining one magnetic start would turn its seed spread into a false
    # zero and could promote a metastable singleton.  Molecule references are
    # singletons by design and are checked separately.
    surface_groups: Dict[str, List[Dict[str, Any]]] = {}
    for row in rows:
        if row.get("protocol_role") == "surface":
            surface_groups.setdefault(str(row["structure_id"]), []).append(row)
    seed_pair_failures: List[Dict[str, Any]] = []
    paired_surface_rows: List[Dict[str, Any]] = []
    for structure_id, group in sorted(surface_groups.items()):
        good = [row for row in group if row["analysis_eligible"]]
        seeds = {str(row["seed"]) for row in group}
        good_seeds = {str(row["seed"]) for row in good}
        if len(group) == 2 and len(seeds) == 2 and len(good) == 2 and good_seeds == seeds:
            paired_surface_rows.extend(good)
        else:
            seed_pair_failures.append({
                "structure_id": structure_id,
                "planned_jobs": [str(row["job_name"]) for row in group],
                "eligible_jobs": [str(row["job_name"]) for row in good],
                "reason": "surface structure requires two distinct, analysis-eligible magnetic seeds",
            })
    molecule_rows = [row for row in rows if row.get("protocol_role") == "molecule"]
    molecule_reference_failures = [
        str(row["job_name"]) for row in molecule_rows if not row["analysis_eligible"]
    ]
    seed_pair_matrix_complete = not seed_pair_failures
    molecule_reference_matrix_complete = not molecule_reference_failures
    hard_analysis_complete = (
        all_complete
        and all_magnetic_tables
        and all_force_gates
        and all_protocol_gates
        and seed_pair_matrix_complete
        and molecule_reference_matrix_complete
    )
    eligible = paired_surface_rows + [
        row for row in molecule_rows if row["analysis_eligible"]
    ]
    adsorption, summary = compute_metrics(eligible, "static_E0_eV")
    atomic_csv(vasp_out / "ADSORPTION_RESULTS.csv", adsorption)
    gas_box: Dict[str, Any] = {}
    if plan["scope"] == "all":
        for model in ("dimer", "c10"):
            primary = best_row(
                eligible,
                lambda row, model=model: row["model_name"] == model
                and row["role"] == "isolated_fragment_reference",
                "static_E0_eV",
            )
            check = best_row(
                eligible,
                lambda row, model=model: row["model_name"] == model
                and row["role"] == "isolated_fragment_box_check",
                "static_E0_eV",
            )
            if primary and check:
                shift = abs(float(primary["static_E0_eV"]) - float(check["static_E0_eV"]))
                gas_box[model] = {"shift_eV": shift, "pass_10meV": shift <= GAS_BOX_TOL_EV}
            else:
                gas_box[model] = {"pass_10meV": False, "reason": "box check incomplete"}
    selection_names = dense_selection(eligible, adsorption) if summary.get("complete") else []
    selection = {
        "jobs": selection_names,
        "purpose": "3x4x1 static k-point check; Gamma-only gas references are reused",
        "generated_from": "VASP_RESULTS.csv",
        "window_eV": FINALIST_WINDOW_EV,
    }
    atomic_json(vasp_out / "DENSE_SELECTION.json", selection)
    dense_rows: List[Dict[str, Any]] = []
    for row in eligible:
        if row["job_name"] not in selection_names:
            continue
        dense = parse_outcar(vasp_out / "jobs" / row["job_name"] / "dense" / "OUTCAR")
        dense_row = dict(row)
        for key, value in dense.items():
            if key not in ("forces_eV_A", "magnetization_x"):
                dense_row[f"dense_{key}"] = value
        dense_mag = magnetic_audit(row, dense, vasp_out / "jobs" / row["job_name"])
        dense_protocol = protocol_audit(row, dense, "dense")
        dense_row["dense_protocol_ok"] = dense_protocol["protocol_ok"]
        dense_row["dense_protocol_reason"] = dense_protocol["protocol_reason"]
        dense_row["dense_magnetic_table_ok"] = dense_mag["magnetic_table_ok"]
        dense_row["dense_magnetic_review"] = dense_mag["magnetic_review"]
        dense_row["dense_ni_sign_flip_count"] = dense_mag.get("ni_sign_flip_count")
        dense_row["dense_ni_small_moment_count"] = dense_mag.get("ni_small_moment_count")
        dense_row["magnetic_review"] = bool(
            dense_row.get("magnetic_review") or dense_mag.get("magnetic_review")
        )
        if (
            dense.get("complete")
            and dense_mag["magnetic_table_ok"]
            and dense_protocol["protocol_ok"]
        ):
            dense_rows.append(dense_row)
    dense_complete = bool(selection_names) and len(dense_rows) == len(selection_names)
    dense_summary: Dict[str, Any] | None = None
    dense_adsorption: List[Dict[str, Any]] = []
    if dense_complete and summary.get("complete"):
        dense_adsorption, dense_summary = compute_metrics(
            dense_rows,
            "dense_E0_eV",
            gas_reference={key: float(value) for key, value in summary["gas_reference_eV"].items()},
        )
        atomic_csv(vasp_out / "ADSORPTION_RESULTS_DENSE.csv", dense_adsorption)
    verdicts: Dict[str, Any] = {}
    for model in ("dimer", "c10"):
        if not hard_analysis_complete:
            verdicts[model] = {
                "status": "INCOMPLETE_AUDIT",
                "reason": (
                    "planned completion, <=0.02 eV/A force, complete two-seed surface matrix, "
                    "molecule-reference geometry, OUTCAR protocol identity, or 48-Ni moment-table gate failed"
                ),
            }
            continue
        coarse_item = summary.get("li_vs_ni_contact_contrast", {}).get(model, {})
        if "blocked" in coarse_item or not coarse_item:
            verdicts[model] = {"status": "BLOCKED_GEOMETRY", **coarse_item}
            continue
        if plan["scope"] != "all":
            verdicts[model] = {
                "status": "PILOT_ONLY_NO_PREFERENCE_CLAIM",
                "coarse_sampled_gap_eV": coarse_item["sampled_DeltaE_Ni_minus_Li_eV"],
                "coarse_matched_gap_eV": coarse_item["matched_DeltaE_Ni_minus_Li_eV"],
            }
            continue
        if not dense_complete or dense_summary is None:
            verdicts[model] = {
                "status": "DENSE_K_REQUIRED",
                "coarse_sampled_gap_eV": coarse_item["sampled_DeltaE_Ni_minus_Li_eV"],
                "coarse_matched_gap_eV": coarse_item["matched_DeltaE_Ni_minus_Li_eV"],
            }
            continue
        dense_item = dense_summary.get("li_vs_ni_contact_contrast", {}).get(model, {})
        if "blocked" in dense_item or not dense_item:
            verdicts[model] = {"status": "BLOCKED_DENSE_GEOMETRY", **dense_item}
            continue
        coarse_sampled = float(coarse_item["sampled_DeltaE_Ni_minus_Li_eV"])
        coarse_matched = float(coarse_item["matched_DeltaE_Ni_minus_Li_eV"])
        dense_sampled = float(dense_item["sampled_DeltaE_Ni_minus_Li_eV"])
        dense_matched = float(dense_item["matched_DeltaE_Ni_minus_Li_eV"])
        kshift = abs(dense_sampled - coarse_sampled)
        matched_kshift = abs(dense_matched - coarse_matched)
        threshold = max(
            PREFERENCE_FLOOR_EV,
            float(coarse_item["max_seed_spread_eV"]),
            float(dense_item["max_seed_spread_eV"]),
            kshift,
            matched_kshift,
        )
        signs_agree = dense_sampled * dense_matched > 0.0
        numeric_pass = (
            abs(dense_sampled) > threshold
            and abs(dense_matched) > threshold
            and kshift <= KPOINT_TOL_EV
            and matched_kshift <= KPOINT_TOL_EV
            and signs_agree
        )
        pairwise_lower = "Li" if dense_sampled > 0 else "Ni"
        global_registry = str(dense_item.get("global_lowest_registry"))
        if global_registry not in ("Li", "Ni"):
            status = "PAIRWISE_CONTRAST_ONLY__GLOBAL_MINIMUM_IS_MIXED_OR_OTHER"
        elif global_registry != pairwise_lower:
            status = "INCONSISTENT_GLOBAL_AND_PAIRWISE_REGISTRY"
        else:
            status = (
                "NUMERIC_PASS_FIXED_U6.2_D3__MANUAL_MAGNETIC_AUDIT_REQUIRED"
                if numeric_pass
                else "UNRESOLVED_WITHIN_NUMERICAL_SENSITIVITY"
            )
        verdicts[model] = {
            "status": status,
            "quantity": "Li-vs-Ni nearest-F contact contrast, not an exhaustive site preference",
            "lower_contact_registry_if_audit_passes": pairwise_lower,
            "global_lowest_sampled_registry": global_registry,
            "global_lowest_sampled_job": dense_item.get("global_lowest_job"),
            "coarse_sampled_gap_eV": coarse_sampled,
            "dense_sampled_gap_eV": dense_sampled,
            "dense_matched_gap_eV": dense_matched,
            "kpoint_shift_eV": kshift,
            "matched_kpoint_shift_eV": matched_kshift,
            "resolution_threshold_eV": threshold,
            "matched_and_sampled_sign_agree": signs_agree,
            "U_dispersion_sensitivity_done": False,
        }
    adsorption_verdicts: Dict[str, Any] = {}
    for model in ("dimer", "c10"):
        coarse_model = [row for row in adsorption if row["model_name"] == model]
        dense_model = [row for row in dense_adsorption if row["model_name"] == model]
        if not hard_analysis_complete or not coarse_model:
            adsorption_verdicts[model] = {"status": "INCOMPLETE_AUDIT"}
            continue
        coarse_min = min(coarse_model, key=lambda row: float(row["E_ads_eV"]))
        box = gas_box.get(model, {})
        if plan["scope"] != "all":
            adsorption_verdicts[model] = {
                "status": "PILOT_ONLY",
                "coarse_E_ads_eV": coarse_min["E_ads_eV"],
            }
        elif not box.get("pass_10meV"):
            adsorption_verdicts[model] = {
                "status": "BLOCKED_GAS_BOX_CONVERGENCE",
                "coarse_E_ads_eV": coarse_min["E_ads_eV"],
                "gas_box": box,
            }
        elif not dense_complete or not dense_model:
            adsorption_verdicts[model] = {
                "status": "DENSE_K_REQUIRED",
                "coarse_E_ads_eV": coarse_min["E_ads_eV"],
            }
        else:
            dense_min = min(dense_model, key=lambda row: float(row["E_ads_eV"]))
            shift = abs(float(dense_min["E_ads_eV"]) - float(coarse_min["E_ads_eV"]))
            adsorption_verdicts[model] = {
                "status": (
                    "NUMERIC_PASS_FIXED_U6.2_D3__MANUAL_MAGNETIC_AUDIT_REQUIRED"
                    if shift <= KPOINT_TOL_EV
                    else "UNRESOLVED_KPOINT_CONVERGENCE"
                ),
                "coarse_E_ads_eV": coarse_min["E_ads_eV"],
                "dense_E_ads_eV": dense_min["E_ads_eV"],
                "kpoint_shift_eV": shift,
                "coarse_job": coarse_min["job_name"],
                "dense_job": dense_min["job_name"],
                "gas_box_shift_eV": box.get("shift_eV"),
            }
    numeric_claim_gates_all_passed = all(
        verdicts.get(model, {}).get("status")
        == "NUMERIC_PASS_FIXED_U6.2_D3__MANUAL_MAGNETIC_AUDIT_REQUIRED"
        and adsorption_verdicts.get(model, {}).get("status")
        == "NUMERIC_PASS_FIXED_U6.2_D3__MANUAL_MAGNETIC_AUDIT_REQUIRED"
        for model in ("dimer", "c10")
    )
    report = {
        "plan_fingerprint": plan["protocol"]["fingerprint"],
        "scope": plan["scope"],
        "completed_relax_static_jobs": sum(
            bool(row.get("relax_complete")) and bool(row.get("static_complete")) for row in rows
        ),
        "total_jobs": len(rows),
        "all_geometry_ok": all_geometry_ok,
        "geometry_excluded_jobs": [
            {"job_name": row["job_name"], "reason": row.get("geometry_reason", "")}
            for row in rows if row.get("relax_complete") and row.get("static_complete")
            and not row.get("geometry_ok")
        ],
        "all_force_gates_passed": all_force_gates,
        "all_magnetic_tables_present": all_magnetic_tables,
        "all_outcar_protocol_gates_passed": all_protocol_gates,
        "surface_seed_pair_matrix_complete": seed_pair_matrix_complete,
        "surface_seed_pair_failures": seed_pair_failures,
        "molecule_reference_matrix_complete": molecule_reference_matrix_complete,
        "molecule_reference_failures": molecule_reference_failures,
        "dense_complete": dense_complete,
        "gas_box_convergence": gas_box,
        "coarse": summary,
        "dense": dense_summary,
        "li_vs_ni_contact_contrast_verdicts": verdicts,
        "adsorption_verdicts": adsorption_verdicts,
        "numeric_claim_gates_all_passed": numeric_claim_gates_all_passed,
        "archive_semantics": (
            "A final archive means the planned computational/audit return set is complete; "
            "BLOCKED or UNRESOLVED numeric outcomes are preserved and are not converted to passes."
        ),
        "warning": (
            "Finite-fragment, fixed-axis, finite-candidate, 1x4 fixed-coverage PBE+U(6.2)+D3 result. "
            "A numeric pass remains conditional on manual Ni occupation/moment review and is not a U/dispersion-independent claim."
        ),
    }
    atomic_json(vasp_out / "VASP_ANALYSIS.json", report)
    lines = [
        "# PTFE/LiNiO2 VASP DFT validation",
        "",
        f"- Completed relax+static jobs: {report['completed_relax_static_jobs']}/{len(rows)}",
        f"- Dense selection complete: {dense_complete}",
        f"- All numeric claim gates passed: {numeric_claim_gates_all_passed}",
        "- Energy: E0 (energy sigma->0); E_ads = E_complex - E_slab - E_fragment",
        "- DeltaE(Ni-Li) > 0 means the sampled Li-contact branch is lower",
        "- Scope: 0 K electronic energy; finite fragment, fixed axis/candidates, 1x4 fixed coverage",
        "",
        "## Li-vs-Ni contact contrast",
        "",
    ]
    for model in ("dimer", "c10"):
        lines.append(f"- **{model}**: `{json.dumps(verdicts.get(model), ensure_ascii=False)}`")
    lines.extend(["", "## Adsorption-energy gate", ""])
    for model in ("dimer", "c10"):
        lines.append(
            f"- **{model}**: `{json.dumps(adsorption_verdicts.get(model), ensure_ascii=False)}`"
        )
    lines.extend([
        "",
        "## Coarse-k adsorption branches",
        "",
        "| model | final registry | role | E_ads (eV) | seed | job |",
        "|---|---|---|---:|---|---|",
    ])
    for row in adsorption:
        lines.append(
            f"| {row['model_name']} | {row['final_registry']} | {row['role']} | "
            f"{float(row['E_ads_eV']):+.6f} | {row['seed']} | {row['job_name']} |"
        )
    lines.extend([
        "",
        "## Interpretation limits",
        "",
        "- ORCA energies are not used in E_ads; ORCA supplies starting geometries only.",
        "- Dimer and C10 have different caps, so their total E_ads values are not a chain-length series.",
        "- Inspect the 48 Ni local moments and LDAU occupation matrices of every winning branch.",
        "- U and dispersion sensitivity are not automated here; any pass is conditional on U=6.2 eV and IVDW=11.",
        "",
    ])
    atomic_text(vasp_out / "VASP_RESULTS.md", "\n".join(lines))
    print((vasp_out / "VASP_RESULTS.md").read_text(encoding="utf-8"))
    if not hard_analysis_complete:
        return 2
    if args.require_dense and not dense_complete:
        return 3
    return 0


def list_jobs(args) -> int:
    vasp_out = args.vasp_out.resolve()
    if args.dense:
        selection = json.loads((vasp_out / "DENSE_SELECTION.json").read_text(encoding="utf-8"))
        names = selection.get("jobs", [])
    else:
        names = [job["job_name"] for job in load_plan(vasp_out)["jobs"]]
    for name in names:
        print(name)
    return 0


def print_direct_com(args) -> int:
    _, _, read, _ = ase_imports()
    atoms = read(args.poscar.resolve())
    values = direct_com(atoms)
    print(f"{values[0]:.8f} {values[1]:.8f} {values[2]:.8f}")
    return 0


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    prep = sub.add_parser("prepare")
    prep.add_argument("--uma-out", type=Path, required=True)
    prep.add_argument("--vasp-out", type=Path, required=True)
    prep.add_argument("--scope", choices=("pilot", "all"), default="all")
    ana = sub.add_parser("analyze")
    ana.add_argument("--vasp-out", type=Path, required=True)
    ana.add_argument("--require-dense", action="store_true")
    ls = sub.add_parser("list-jobs")
    ls.add_argument("--vasp-out", type=Path, required=True)
    ls.add_argument("--dense", action="store_true")
    com = sub.add_parser("direct-com")
    com.add_argument("--poscar", type=Path, required=True)
    return ap


def main() -> int:
    args = parser().parse_args()
    if args.command == "prepare":
        return prepare(args)
    if args.command == "analyze":
        return analyze(args)
    if args.command == "list-jobs":
        return list_jobs(args)
    if args.command == "direct-com":
        return print_direct_com(args)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
