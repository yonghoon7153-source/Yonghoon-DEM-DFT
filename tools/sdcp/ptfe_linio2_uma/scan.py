#!/usr/bin/env python3
"""PTFE/LiNiO2 UMA fixed-axis pose prescreen.

This program deliberately treats UMA energies as an internal geometry score only.
It freezes the complete slab, rejects periodic-image overlap and molecular bond
changes, and writes one atomic JSON record per pose so an interrupted run resumes
without losing completed work.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import sys
import time
from collections import Counter
from functools import lru_cache
from importlib import metadata
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

PACKAGE_DIR = Path(__file__).resolve().parent
INPUT_DIR = PACKAGE_DIR / "inputs"
EXPECTED = {
    "slab": {
        "path": INPUT_DIR / "linio2_104_1x4_relaxed.vasp",
        "counts": {"Li": 48, "Ni": 48, "O": 96},
        "sha256": "26a48473060243fef55e86d151050b6a27d6e65801b4d3ccd818678913aee25e",
    },
    "dimer": {
        "path": INPUT_DIR / "ptfe_dimer_c4h2f8.xyz",
        "counts": {"C": 4, "H": 2, "F": 8},
        "sha256": "dcc0f678202ced02c222cded61a0892a78f177ad12dbb107839bc462ea3bdb7b",
    },
    "c10": {
        "path": INPUT_DIR / "ptfe_c10f22.xyz",
        "counts": {"C": 10, "F": 22},
        "sha256": "66dd0bcc4badd26d6db42cc3ed429fbd9ec50a0d467f76a07d2532329efc2d57",
    },
}
AZIMUTHS_DEG = (15, 60, 165)
ROLLS_DEG = {"dimer": (0, 120, 240), "c10": (0, 90, 180, 270)}
RELAX_LIMIT = {"dimer": 8, "c10": 12}
SITE_ORDER = (
    "Li_top",
    "Ni_top",
    "O_top",
    "LiO_bridge",
    "NiO_bridge",
    "LiNi_bridge",
    "hollow",
)


class UnsafeGeometry(RuntimeError):
    """Raised when an optimization leaves the nonreactive prescreen domain."""


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def atomic_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".tmp.{os.getpid()}")
    tmp.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, path)


def atomic_csv(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".tmp.{os.getpid()}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with tmp.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    os.replace(tmp, path)


def imports():
    try:
        from ase.constraints import FixAtoms
        from ase.io import read, write
    except ImportError as exc:
        raise SystemExit(f"ASE import failed: {exc}")
    return FixAtoms, read, write


def fire_class():
    try:
        from ase.optimize import FIRE
    except ImportError as exc:
        raise SystemExit(f"ASE optimizer import failed: {exc}")
    return FIRE


def installed_version(*names: str) -> str:
    for name in names:
        try:
            return metadata.version(name)
        except metadata.PackageNotFoundError:
            continue
    return "unknown"


@lru_cache(maxsize=1)
def code_sha256() -> str:
    return sha256(Path(__file__).resolve())


def protocol_payload(args, stage: str) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "stage": stage,
        "scan_py_sha256": code_sha256(),
        "input_sha256": {name: spec["sha256"] for name, spec in EXPECTED.items()},
        "model": args.model,
        "task": args.task,
        "device": args.device,
        "gap_A": float(args.gap),
        "python_version": platform.python_version(),
        "numpy_version": installed_version("numpy"),
        "ase_version": installed_version("ase"),
        "torch_version": installed_version("torch"),
        "fairchem_version": installed_version("fairchem-core", "fairchem"),
        "package_commit": os.environ.get("PACKAGE_COMMIT", "UNRECORDED"),
        "model_cache_manifest_sha256": os.environ.get(
            "UMA_WEIGHTS_FINGERPRINT", "UNRECORDED"
        ),
    }
    if stage == "pilot":
        payload.update({
            "fmax_eV_A": float(args.fmax),
            "pilot_steps": int(args.pilot_steps),
        })
    elif stage == "relaxed":
        payload.update({
            "fmax_eV_A": float(args.fmax),
            "steps": int(args.steps),
        })
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    payload["fingerprint"] = hashlib.sha256(encoded).hexdigest()
    return payload


def require_matching_record(path: Path, fingerprint: str) -> Dict[str, Any] | None:
    if not path.is_file():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("protocol_fingerprint") != fingerprint:
        raise SystemExit(
            f"stale/incompatible record: {path}\n"
            f"have={payload.get('protocol_fingerprint')} want={fingerprint}\n"
            "Use a new OUT directory; do not mix or overwrite protocols."
        )
    return payload


def finite_number(value: float, label: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise UnsafeGeometry(f"non-finite {label}: {number}")
    return number


def require_finite_array(values: np.ndarray, label: str) -> None:
    if not np.all(np.isfinite(np.asarray(values, dtype=float))):
        raise UnsafeGeometry(f"non-finite {label}")


def require_finite_metrics(metrics: Dict[str, Any]) -> None:
    for key, value in metrics.items():
        if value is None or isinstance(value, (str, bool, list, dict)):
            continue
        if isinstance(value, (int, float, np.integer, np.floating)) and not math.isfinite(float(value)):
            raise UnsafeGeometry(f"non-finite geometry metric {key}: {value}")


def validate_inputs() -> Dict[str, Any]:
    _, read, _ = imports()
    report: Dict[str, Any] = {}
    for name, spec in EXPECTED.items():
        path = spec["path"]
        if not path.is_file():
            raise SystemExit(f"missing input: {path}")
        got_hash = sha256(path)
        if got_hash != spec["sha256"]:
            raise SystemExit(
                f"SHA256 mismatch for {name}: {got_hash} != {spec['sha256']}\n"
                "Do not run with an unreviewed structure."
            )
        atoms = read(path)
        got_counts = dict(Counter(atoms.get_chemical_symbols()))
        if got_counts != spec["counts"]:
            raise SystemExit(f"composition mismatch for {name}: {got_counts} != {spec['counts']}")
        report[name] = {
            "path": str(path),
            "sha256": got_hash,
            "natoms": len(atoms),
            "counts": got_counts,
        }
    slab = read(EXPECTED["slab"]["path"])
    cell = np.asarray(slab.cell.array, dtype=float)
    if slab.cell.rank != 3 or abs(np.linalg.det(cell)) < 1.0:
        raise SystemExit("slab cell is missing or degenerate")
    if not np.all(slab.pbc):
        slab.pbc = True
    report["slab"]["cell_A"] = cell.tolist()
    report["slab"]["area_A2"] = float(np.linalg.norm(np.cross(cell[0], cell[1])))
    report["slab"]["z_range_A"] = [float(slab.positions[:, 2].min()), float(slab.positions[:, 2].max())]
    return report


def mic_vec_xy(p_from: np.ndarray, p_to: np.ndarray, cell: np.ndarray) -> np.ndarray:
    frac_from = np.linalg.solve(cell.T, p_from)
    frac_to = np.linalg.solve(cell.T, p_to)
    dfrac = frac_to - frac_from
    dfrac[:2] -= np.round(dfrac[:2])
    dfrac[2] = 0.0
    return dfrac @ cell


def wrap_xy(point: np.ndarray, cell: np.ndarray) -> np.ndarray:
    frac = np.linalg.solve(cell.T, point)
    frac[:2] %= 1.0
    return frac @ cell


def center_distance(point: np.ndarray, cell: np.ndarray) -> float:
    center = 0.5 * cell[0] + 0.5 * cell[1]
    return float(np.linalg.norm(mic_vec_xy(center, point, cell)[:2]))


def surface_candidates(slab, element: str) -> List[int]:
    symbols = slab.get_chemical_symbols()
    zmax = float(slab.positions[:, 2].max())
    for depth in (1.0, 1.5, 2.2, 3.0):
        found = [
            i for i, symbol in enumerate(symbols)
            if symbol == element and slab.positions[i, 2] >= zmax - depth
        ]
        if found:
            return found
    raise SystemExit(f"no surface candidate found for {element}")


def central_atom(slab, indices: Sequence[int]) -> int:
    cell = np.asarray(slab.cell.array)
    return min(indices, key=lambda i: center_distance(slab.positions[i], cell))


def nearest_pair_anchor(slab, left: Sequence[int], right: Sequence[int]) -> np.ndarray:
    cell = np.asarray(slab.cell.array)
    best = None
    for i in left:
        for j in right:
            vec = mic_vec_xy(slab.positions[i], slab.positions[j], cell)
            distance = float(np.linalg.norm(vec[:2]))
            midpoint = slab.positions[i].copy() + 0.5 * vec
            midpoint[2] = 0.5 * (slab.positions[i, 2] + slab.positions[j, 2])
            score = (distance, center_distance(midpoint, cell))
            if best is None or score < best[0]:
                best = (score, midpoint)
    assert best is not None
    return wrap_xy(best[1], cell)


def hollow_anchor(slab, li: Sequence[int], ni: Sequence[int], oxy: Sequence[int]) -> np.ndarray:
    cell = np.asarray(slab.cell.array)
    best = None
    for i in li:
        pi = slab.positions[i]
        for j in ni:
            pj = pi + mic_vec_xy(pi, slab.positions[j], cell)
            pj[2] = slab.positions[j, 2]
            for k in oxy:
                pk = pi + mic_vec_xy(pi, slab.positions[k], cell)
                pk[2] = slab.positions[k, 2]
                edges = (
                    np.linalg.norm((pj - pi)[:2]),
                    np.linalg.norm((pk - pi)[:2]),
                    np.linalg.norm((pk - pj)[:2]),
                )
                centroid = (pi + pj + pk) / 3.0
                score = (float(sum(edges)), center_distance(centroid, cell))
                if best is None or score < best[0]:
                    best = (score, centroid)
    assert best is not None
    return wrap_xy(best[1], cell)


def site_anchors(slab) -> Dict[str, np.ndarray]:
    li = surface_candidates(slab, "Li")
    ni = surface_candidates(slab, "Ni")
    oxy = surface_candidates(slab, "O")
    anchors = {
        "Li_top": slab.positions[central_atom(slab, li)].copy(),
        "Ni_top": slab.positions[central_atom(slab, ni)].copy(),
        "O_top": slab.positions[central_atom(slab, oxy)].copy(),
        "LiO_bridge": nearest_pair_anchor(slab, li, oxy),
        "NiO_bridge": nearest_pair_anchor(slab, ni, oxy),
        "LiNi_bridge": nearest_pair_anchor(slab, li, ni),
        "hollow": hollow_anchor(slab, li, ni, oxy),
    }
    return {name: wrap_xy(anchors[name], np.asarray(slab.cell.array)) for name in SITE_ORDER}


def rotation_from_to(source: np.ndarray, target: np.ndarray) -> np.ndarray:
    a = source / np.linalg.norm(source)
    b = target / np.linalg.norm(target)
    cross = np.cross(a, b)
    sine = np.linalg.norm(cross)
    cosine = float(np.clip(np.dot(a, b), -1.0, 1.0))
    if sine < 1e-12:
        if cosine > 0:
            return np.eye(3)
        helper = np.array([1.0, 0.0, 0.0])
        if abs(a[0]) > 0.8:
            helper = np.array([0.0, 1.0, 0.0])
        axis = np.cross(a, helper)
        axis /= np.linalg.norm(axis)
        return axis_angle(axis, 180.0)
    k = cross / sine
    skew = np.array([[0.0, -k[2], k[1]], [k[2], 0.0, -k[0]], [-k[1], k[0], 0.0]])
    return np.eye(3) + sine * skew + (1.0 - cosine) * (skew @ skew)


def axis_angle(axis: np.ndarray, degrees: float) -> np.ndarray:
    axis = axis / np.linalg.norm(axis)
    angle = math.radians(degrees)
    skew = np.array(
        [[0.0, -axis[2], axis[1]], [axis[2], 0.0, -axis[0]], [-axis[1], axis[0], 0.0]]
    )
    return np.eye(3) + math.sin(angle) * skew + (1.0 - math.cos(angle)) * (skew @ skew)


def internal_f_indices(molecule) -> List[int]:
    symbols = molecule.get_chemical_symbols()
    carbons = [i for i, symbol in enumerate(symbols) if symbol == "C"]
    fluorines = [i for i, symbol in enumerate(symbols) if symbol == "F"]
    if len(carbons) < 3:
        return fluorines
    internal_carbons = set(carbons[1:-1])
    selected = []
    for fi in fluorines:
        nearest = min(carbons, key=lambda ci: np.linalg.norm(molecule.positions[fi] - molecule.positions[ci]))
        if nearest in internal_carbons:
            selected.append(fi)
    return selected or fluorines


def lower_internal_f_indices(molecule, window_A: float = 0.35) -> List[int]:
    candidates = internal_f_indices(molecule)
    zmin = min(float(molecule.positions[i, 2]) for i in candidates)
    return [i for i in candidates if float(molecule.positions[i, 2]) <= zmin + window_A]


def orient_molecule(molecule, azimuth_deg: float, roll_deg: float, anchor: np.ndarray, slab, gap: float):
    mol = molecule.copy()
    symbols = mol.get_chemical_symbols()
    carbons = [i for i, symbol in enumerate(symbols) if symbol == "C"]
    if len(carbons) < 2:
        raise ValueError("PTFE model needs at least two carbon atoms")
    positions = mol.positions - mol.get_center_of_mass()
    chain = positions[carbons[-1]] - positions[carbons[0]]
    az = math.radians(azimuth_deg)
    target = np.array([math.cos(az), math.sin(az), 0.0])
    align = rotation_from_to(chain, target)
    positions = positions @ align.T
    positions = positions @ axis_angle(target, roll_deg).T
    mol.positions = positions
    contact_f = lower_internal_f_indices(mol)
    contact_xy = positions[contact_f, :2].mean(axis=0)
    positions[:, :2] += anchor[:2] - contact_xy
    ztop = float(slab.positions[:, 2].max())
    positions[:, 2] += ztop + gap - float(positions[contact_f, 2].min())
    mol.positions = positions
    mol.set_cell(slab.cell)
    mol.set_pbc(True)
    return mol


def min_block_distance(left: np.ndarray, right: np.ndarray) -> float:
    distances = np.linalg.norm(left[:, None, :] - right[None, :, :], axis=2)
    return float(distances.min())


def lateral_image_min(mol_positions: np.ndarray, cell: np.ndarray) -> float:
    best = float("inf")
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if i == 0 and j == 0:
                continue
            shifted = mol_positions + i * cell[0] + j * cell[1]
            best = min(best, min_block_distance(mol_positions, shifted))
    return best


def vertical_image_min(mol_positions: np.ndarray, slab_positions: np.ndarray, cell: np.ndarray) -> float:
    best = float("inf")
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            lateral = i * cell[0] + j * cell[1]
            for k in (-1, 1):
                shift = lateral + k * cell[2]
                best = min(best, min_block_distance(mol_positions, slab_positions + shift))
                best = min(best, min_block_distance(mol_positions, mol_positions + shift))
    return best


def min_distances_by_element(complex_atoms, nslab: int) -> Dict[str, Any]:
    symbols = complex_atoms.get_chemical_symbols()
    f_indices = [i for i in range(nslab, len(complex_atoms)) if symbols[i] == "F"]
    c_indices = [i for i in range(nslab, len(complex_atoms)) if symbols[i] == "C"]
    mol_indices = list(range(nslab, len(complex_atoms)))
    result: Dict[str, Any] = {}
    for element, cutoff in (("Li", 2.8), ("Ni", 2.8), ("O", 3.2)):
        slab_indices = [i for i in range(nslab) if symbols[i] == element]
        values = []
        contacted_indices = []
        nearest_pair = None
        for fi in f_indices:
            distances = np.asarray(complex_atoms.get_distances(fi, slab_indices, mic=True), dtype=float)
            local = int(np.argmin(distances))
            distance = float(distances[local])
            values.append(distance)
            if distance <= cutoff:
                contacted_indices.append(fi - nslab)
            pair = (distance, fi - nslab, slab_indices[local])
            if nearest_pair is None or pair < nearest_pair:
                nearest_pair = pair
        result[f"min_F_{element}_A"] = min(values) if values else None
        result[f"contact_F_{element}_count"] = len(contacted_indices)
        result[f"contact_F_{element}_indices"] = contacted_indices
        result[f"nearest_F_{element}_index"] = nearest_pair[1] if nearest_pair else None
        result[f"nearest_{element}_slab_index"] = nearest_pair[2] if nearest_pair else None
        carbon_distances = [
            float(np.asarray(complex_atoms.get_distances(ci, slab_indices, mic=True)).min())
            for ci in c_indices
        ]
        result[f"min_C_{element}_A"] = min(carbon_distances) if carbon_distances else None
    closest = float("inf")
    closest_symbol = ""
    for mi in mol_indices:
        distances = np.asarray(complex_atoms.get_distances(mi, list(range(nslab)), mic=True), dtype=float)
        k = int(np.argmin(distances))
        if float(distances[k]) < closest:
            closest = float(distances[k])
            closest_symbol = symbols[mi]
    result["min_molecule_slab_A"] = closest
    result["closest_molecule_element"] = closest_symbol
    h_indices = [i for i in mol_indices if symbols[i] == "H"]
    if h_indices:
        result["min_H_slab_A"] = min(
            float(np.asarray(complex_atoms.get_distances(i, list(range(nslab)), mic=True)).min())
            for i in h_indices
        )
    else:
        result["min_H_slab_A"] = None
    li = result["min_F_Li_A"]
    ni = result["min_F_Ni_A"]
    result["nearest_cation"] = "Li" if li <= ni else "Ni"
    result["registry_signature"] = (
        f"LiF{result['contact_F_Li_indices']}_NiF{result['contact_F_Ni_indices']}_"
        f"OF{result['contact_F_O_indices']}_near{result['nearest_cation']}"
    )
    return result


def expected_bonds(molecule) -> List[Tuple[int, int, str]]:
    symbols = molecule.get_chemical_symbols()
    distances = molecule.get_all_distances(mic=False)
    cutoffs = {("C", "C"): 1.75, ("C", "F"): 1.55, ("C", "H"): 1.25}
    bonds = []
    for i in range(len(molecule)):
        for j in range(i + 1, len(molecule)):
            pair = tuple(sorted((symbols[i], symbols[j])))
            cutoff = cutoffs.get(pair)
            if cutoff is not None and distances[i, j] <= cutoff:
                bonds.append((i, j, "-".join(pair)))
    return bonds


def bond_metrics(molecule, bonds: Sequence[Tuple[int, int, str]]) -> Dict[str, Any]:
    limits = {"C-C": 1.90, "C-F": 1.70, "C-H": 1.35}
    formation = {"C-C": 1.75, "C-F": 1.55, "C-H": 1.25}
    lower = {"C-C": 1.20, "C-F": 1.10, "C-H": 0.85}
    result: Dict[str, Any] = {
        "broken_bonds": 0,
        "broken_bond_labels": [],
        "formed_bonds": 0,
        "formed_bond_labels": [],
        "too_short_bonds": 0,
        "too_short_bond_labels": [],
    }
    expected = {(min(i, j), max(i, j), label) for i, j, label in bonds}
    maxima: Dict[str, float] = {}
    for i, j, label in bonds:
        distance = float(np.linalg.norm(molecule.positions[i] - molecule.positions[j]))
        maxima[label] = max(maxima.get(label, 0.0), distance)
        if distance > limits[label]:
            result["broken_bonds"] += 1
            result["broken_bond_labels"].append(f"{label}:{i}-{j}:{distance:.3f}")
        if distance < lower[label]:
            result["too_short_bonds"] += 1
            result["too_short_bond_labels"].append(f"{label}:{i}-{j}:{distance:.3f}")
    symbols = molecule.get_chemical_symbols()
    for i in range(len(molecule)):
        for j in range(i + 1, len(molecule)):
            label = "-".join(sorted((symbols[i], symbols[j])))
            if label not in formation or (i, j, label) in expected:
                continue
            distance = float(np.linalg.norm(molecule.positions[i] - molecule.positions[j]))
            if distance < formation[label]:
                result["formed_bonds"] += 1
                result["formed_bond_labels"].append(f"{label}:{i}-{j}:{distance:.3f}")
    for label in ("C-C", "C-F", "C-H"):
        result[f"max_{label}_A"] = maxima.get(label)
    result["topology_changes"] = (
        result["broken_bonds"] + result["formed_bonds"] + result["too_short_bonds"]
    )
    return result


def geometry_metrics(complex_atoms, nslab: int, slab_reference, molecule_reference) -> Dict[str, Any]:
    require_finite_array(complex_atoms.positions, "complex positions")
    require_finite_array(complex_atoms.cell.array, "complex cell")
    mol = complex_atoms[nslab:].copy()
    cell = np.asarray(complex_atoms.cell.array, dtype=float)
    metrics = min_distances_by_element(complex_atoms, nslab)
    metrics.update(bond_metrics(mol, expected_bonds(molecule_reference)))
    metrics["lateral_image_min_A"] = lateral_image_min(mol.positions, cell)
    metrics["vertical_image_min_A"] = vertical_image_min(
        mol.positions, complex_atoms.positions[:nslab], cell
    )
    displacement = np.linalg.norm(
        complex_atoms.positions[:nslab] - slab_reference.positions[:nslab], axis=1
    )
    metrics["slab_max_displacement_A"] = float(displacement.max())
    li_indices = [
        i for i, symbol in enumerate(slab_reference.get_chemical_symbols()) if symbol == "Li"
    ]
    metrics["Li_max_displacement_A"] = float(displacement[li_indices].max())
    contact_f = lower_internal_f_indices(mol)
    metrics["lower_internal_F_indices"] = contact_f
    metrics["lower_internal_F_count"] = len(contact_f)
    symbols = mol.get_chemical_symbols()
    carbons = [i for i, symbol in enumerate(symbols) if symbol == "C"]
    chain = mol.positions[carbons[-1]] - mol.positions[carbons[0]]
    chain_norm = float(np.linalg.norm(chain))
    metrics["chain_azimuth_deg_mod180"] = float(
        math.degrees(math.atan2(chain[1], chain[0])) % 180.0
    )
    metrics["chain_tilt_from_plane_deg"] = float(
        math.degrees(math.asin(np.clip(abs(chain[2]) / chain_norm, 0.0, 1.0)))
    )
    metrics["molecule_COM_height_above_slab_top_A"] = float(
        mol.get_center_of_mass()[2] - slab_reference.positions[:, 2].max()
    )
    require_finite_metrics(metrics)
    return metrics


def anchor_offset_A(complex_atoms, nslab: int, anchor: Sequence[float]) -> float:
    mol = complex_atoms[nslab:].copy()
    indices = lower_internal_f_indices(mol)
    centroid = mol.positions[indices].mean(axis=0)
    vector = mic_vec_xy(np.asarray(anchor, dtype=float), centroid, np.asarray(complex_atoms.cell.array))
    return finite_number(np.linalg.norm(vector[:2]), "contact-F anchor offset")


def classify(metrics: Dict[str, Any], model_name: str) -> Tuple[str, str, bool]:
    reasons = []
    status = "OK"
    if metrics["min_molecule_slab_A"] < 1.5:
        status = "QUARANTINE"
        reasons.append("molecule-slab clash <1.5 A")
    elif metrics["min_molecule_slab_A"] > 4.0:
        status = "DETACHED"
        reasons.append("no retained surface contact: molecule-slab minimum >4.0 A")
    if metrics["lateral_image_min_A"] < 4.5:
        status = "QUARANTINE"
        reasons.append("lateral molecule-image clearance <4.5 A")
    elif metrics["lateral_image_min_A"] < 5.0 and status == "OK":
        status = "WARNING"
        reasons.append("lateral molecule-image clearance <5.0 A")
    if metrics["vertical_image_min_A"] < 5.0:
        status = "QUARANTINE"
        reasons.append("vertical periodic-image clearance <5.0 A")
    if metrics["topology_changes"]:
        status = "UMA_UNSUPPORTED_REACTION"
        reasons.append("PTFE bond topology changed")
    if metrics.get("max_C-F_A") is not None and metrics["max_C-F_A"] > 1.55:
        status = "UMA_UNSUPPORTED_REACTION"
        reasons.append("C-F stretch >1.55 A entered a reaction-like region")
    if (
        metrics.get("min_C_Ni_A") is not None and metrics["min_C_Ni_A"] < 2.1
    ) or (
        metrics.get("min_C_O_A") is not None and metrics["min_C_O_A"] < 1.8
    ) or (
        metrics.get("min_C_Li_A") is not None and metrics["min_C_Li_A"] < 2.1
    ):
        status = "UMA_UNSUPPORTED_REACTION"
        reasons.append("surface-carbon short contact entered a reaction-like region")
    if metrics["min_F_Ni_A"] < 1.8 or metrics["min_F_O_A"] < 1.6:
        status = "UMA_UNSUPPORTED_REACTION"
        reasons.append("F-Ni/O short contact entered a reaction-like region")
    if metrics["slab_max_displacement_A"] > 1e-6:
        status = "QUARANTINE"
        reasons.append("frozen slab moved")
    if model_name == "dimer" and (
        metrics["closest_molecule_element"] == "H"
        or (metrics.get("min_H_slab_A") is not None and metrics["min_H_slab_A"] < 1.8)
    ):
        status = "CAP_ARTIFACT"
        reasons.append("artificial H cap is the surface contact")
    eligible = status in ("OK", "WARNING")
    return status, "; ".join(reasons), eligible


def build_pose_specs(slab, gap: float) -> List[Dict[str, Any]]:
    anchors = site_anchors(slab)
    specs = []
    for model_name in ("dimer", "c10"):
        for site in SITE_ORDER:
            for azimuth in AZIMUTHS_DEG:
                for roll in ROLLS_DEG[model_name]:
                    pose_id = f"{model_name}_{site}_az{azimuth:03d}_r{roll:03d}_h{gap:.1f}"
                    specs.append(
                        {
                            "pose_id": pose_id,
                            "model_name": model_name,
                            "initial_site": site,
                            "azimuth_deg": azimuth,
                            "roll_deg": roll,
                            "gap_A": gap,
                            "anchor_A": [float(x) for x in anchors[site]],
                        }
                    )
    return specs


def load_calculator(model: str, task: str, device: str):
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator

    predictor = pretrained_mlip.get_predict_unit(model, device=device)
    return FAIRChemCalculator(predictor, task_name=task)


def gpu_snapshot() -> Dict[str, Any]:
    snapshot: Dict[str, Any] = {}
    try:
        import torch

        snapshot["torch_version"] = torch.__version__
        snapshot["cuda_available"] = bool(torch.cuda.is_available())
        if torch.cuda.is_available():
            snapshot["gpu_name"] = torch.cuda.get_device_name(0)
            snapshot["allocated_MiB"] = round(torch.cuda.memory_allocated(0) / 2**20, 1)
            snapshot["reserved_MiB"] = round(torch.cuda.memory_reserved(0) / 2**20, 1)
            snapshot["max_allocated_MiB"] = round(torch.cuda.max_memory_allocated(0) / 2**20, 1)
    except Exception as exc:  # diagnostic only
        snapshot["gpu_probe_error"] = str(exc)
    return snapshot


def prepare_structures():
    _, read, _ = imports()
    slab = read(EXPECTED["slab"]["path"])
    slab.set_pbc(True)
    molecules = {
        "dimer": read(EXPECTED["dimer"]["path"]),
        "c10": read(EXPECTED["c10"]["path"]),
    }
    return slab, molecules


def make_complex(slab, molecule, spec: Dict[str, Any]):
    FixAtoms, _, _ = imports()
    anchor = np.asarray(spec["anchor_A"], dtype=float)
    mol = orient_molecule(
        molecule,
        float(spec["azimuth_deg"]),
        float(spec["roll_deg"]),
        anchor,
        slab,
        float(spec["gap_A"]),
    )
    complex_atoms = slab.copy()
    complex_atoms.extend(mol)
    complex_atoms.set_cell(slab.cell)
    complex_atoms.set_pbc(True)
    complex_atoms.set_constraint(FixAtoms(indices=list(range(len(slab)))))
    return complex_atoms


def reference_energies(calc, slab, molecules: Dict[str, Any], out: Path, args) -> Dict[str, float]:
    path = out / "references.json"
    protocol = protocol_payload(args, "references")
    existing = require_matching_record(path, protocol["fingerprint"])
    if existing is not None:
        payload = existing
        return {name: float(value) for name, value in payload["energies_eV"].items()}

    energies: Dict[str, float] = {}
    slab_ref = slab.copy()
    slab_ref.calc = calc
    energies["slab"] = finite_number(slab_ref.get_potential_energy(), "slab reference energy")
    for name, source in molecules.items():
        gas = source.copy()
        gas.set_cell([25.0, 25.0, 30.0 if name == "c10" else 25.0])
        gas.center()
        gas.set_pbc(False)
        gas.calc = calc
        energies[name] = finite_number(gas.get_potential_energy(), f"{name} gas reference energy")
    payload = {
        "model": args.model,
        "task": args.task,
        "protocol_fingerprint": protocol["fingerprint"],
        "protocol": protocol,
        "energies_eV": energies,
        "warning": "Internal UMA pose scores only; not citable adsorption energies.",
        "created_unix": time.time(),
    }
    atomic_json(path, payload)
    return energies


def write_structure_pair(base: Path, atoms) -> Dict[str, str]:
    _, _, write = imports()
    base.parent.mkdir(parents=True, exist_ok=True)
    xyz = base.parent / f"{base.name}.xyz"
    vasp = base.parent / f"{base.name}.vasp"
    write(xyz, atoms)
    write(vasp, atoms, format="vasp", direct=False, sort=False)
    return {
        "structure_xyz_sha256": sha256(xyz),
        "structure_vasp_sha256": sha256(vasp),
    }


def verify_structure_record(row: Dict[str, Any], structures_dir: Path, label: str) -> None:
    pose_id = str(row.get("pose_id", ""))
    failures = []
    for extension in ("xyz", "vasp"):
        path = structures_dir / f"{pose_id}.{extension}"
        key = f"structure_{extension}_sha256"
        expected = row.get(key)
        if not path.is_file():
            failures.append(f"missing {path}")
        elif not expected:
            failures.append(f"missing {key} in record")
        else:
            actual = sha256(path)
            if actual != expected:
                failures.append(f"{path}: have={actual} record={expected}")
    if failures:
        raise SystemExit(
            f"{label} geometry/record provenance mismatch for {pose_id}\n"
            + "\n".join(failures)
            + "\nUse a new OUT directory; do not overwrite or mix completed records."
        )


def ordered_handoff_atoms(atoms, nslab: int):
    FixAtoms, _, _ = imports()
    prepared = atoms.copy()
    prepared.set_constraint()
    slab_z = np.asarray(prepared.positions[:nslab, 2], dtype=float)
    zcut = float(slab_z.min() + 0.5 * (slab_z.max() - slab_z.min()))
    fixed = [i for i in range(nslab) if float(prepared.positions[i, 2]) < zcut]
    prepared.set_constraint(FixAtoms(indices=fixed))
    species_order = {name: rank for rank, name in enumerate(("Li", "Ni", "O", "C", "F", "H"))}
    indices = sorted(
        range(len(prepared)),
        key=lambda i: (species_order.get(prepared[i].symbol, 999), i),
    )
    old_to_new = {old: new for new, old in enumerate(indices)}
    fixed_new = sorted(old_to_new[i] + 1 for i in fixed)
    return prepared[indices], len(fixed), zcut, old_to_new, fixed_new


def write_handoff_pair(base: Path, atoms, nslab: int) -> Dict[str, Any]:
    ordered, fixed_count, zcut, old_to_new, fixed_new = ordered_handoff_atoms(atoms, nslab)
    structure_hashes = write_structure_pair(base, ordered)
    present = set(ordered.get_chemical_symbols())
    order = [name for name in ("Li", "Ni", "O", "C", "F", "H") if name in present]
    return {
        "species_order": order,
        "fixed_count": fixed_count,
        "zcut_A": zcut,
        "old_to_new_zero_based": old_to_new,
        "fixed_vasp_indices_1based": fixed_new,
        "slab_last_vasp_index_1based": nslab,
        "molecule_first_vasp_index_1based": nslab + 1,
        "handoff_xyz_sha256": structure_hashes["structure_xyz_sha256"],
        "handoff_vasp_sha256": structure_hashes["structure_vasp_sha256"],
    }


def verify_existing_handoff(out: Path) -> None:
    manifest = out / "DFT_HANDOFF.json"
    if not manifest.is_file():
        return
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    failures = []
    for row in payload.get("rows", []):
        base = out / "DFT_HANDOFF" / str(row.get("handoff_basename", ""))
        for extension in ("xyz", "vasp"):
            path = base.parent / f"{base.name}.{extension}"
            key = f"handoff_{extension}_sha256"
            expected = row.get(key)
            if not path.is_file():
                failures.append(f"missing {path}")
            elif not expected:
                failures.append(f"missing {key} for {base.name}")
            else:
                actual = sha256(path)
                if actual != expected:
                    failures.append(f"{path}: have={actual} manifest={expected}")
    if failures:
        raise SystemExit(
            "DFT handoff structure/manifest provenance mismatch\n"
            + "\n".join(failures)
            + "\nDo not overwrite returned DFT inputs; use a new OUT directory."
        )


def handoff_contact_indices(row: Dict[str, Any], mapping: Dict[int, int], nslab: int) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for element in ("Li", "Ni", "O"):
        slab_old = row.get(f"nearest_{element}_slab_index")
        f_local = row.get(f"nearest_F_{element}_index")
        result[f"nearest_{element}_vasp_index_1based"] = (
            mapping[int(slab_old)] + 1 if slab_old is not None else None
        )
        result[f"nearest_F_to_{element}_vasp_index_1based"] = (
            mapping[nslab + int(f_local)] + 1 if f_local is not None else None
        )
        result[f"contacting_F_for_{element}_vasp_indices_1based"] = [
            mapping[nslab + int(index)] + 1
            for index in row.get(f"contact_F_{element}_indices", [])
        ]
    return result


def record_base(spec: Dict[str, Any], args, stage: str) -> Dict[str, Any]:
    protocol = protocol_payload(args, stage)
    return {
        **spec,
        "stage": stage,
        "model": args.model,
        "task": args.task,
        "device": args.device,
        "host": platform.node(),
        "timestamp_unix": time.time(),
        "protocol_fingerprint": protocol["fingerprint"],
        "protocol": protocol,
        "warning": "UMA geometry prescreen only; score is not a binding energy.",
    }


def run_pilot(args) -> None:
    inputs = validate_inputs()
    slab, molecules = prepare_structures()
    specs = build_pose_specs(slab, args.gap)
    chosen = [
        next(spec for spec in specs if spec["model_name"] == "dimer"),
        next(spec for spec in specs if spec["model_name"] == "c10"),
    ]
    protocol = protocol_payload(args, "pilot")
    existing = require_matching_record(args.out / "PILOT.json", protocol["fingerprint"])
    if existing is not None:
        for row in existing.get("rows", []):
            verify_structure_record(row, args.out / "pilot_structures", "pilot")
        print(json.dumps(existing, indent=2, sort_keys=True, allow_nan=False))
        if not existing.get("ok"):
            raise SystemExit("existing pilot failed")
        return
    calc = load_calculator(args.model, args.task, args.device)
    energies = reference_energies(calc, slab, molecules, args.out, args)
    FIRE = fire_class()
    pilot_dir = args.out / "pilot_structures"
    pilot_logs = args.out / "pilot_optimizer_logs"
    pilot_dir.mkdir(parents=True, exist_ok=True)
    pilot_logs.mkdir(parents=True, exist_ok=True)
    rows = []
    for spec in chosen:
        comp = make_complex(slab, molecules[spec["model_name"]], spec)
        comp.calc = calc
        energy_initial = finite_number(comp.get_potential_energy(), f"{spec['pose_id']} pilot energy")
        require_finite_array(comp.get_forces(), f"{spec['pose_id']} pilot forces")
        metrics_initial = geometry_metrics(comp, len(slab), slab, molecules[spec["model_name"]])
        metrics_initial["initial_contact_F_anchor_offset_A"] = anchor_offset_A(
            comp, len(slab), spec["anchor_A"]
        )
        if metrics_initial["initial_contact_F_anchor_offset_A"] > 1e-6:
            raise SystemExit(
                f"contact-F placement error for {spec['pose_id']}: "
                f"{metrics_initial['initial_contact_F_anchor_offset_A']:.6g} A"
            )
        guard_state = {"reason": "", "status": ""}

        def guard() -> None:
            current = geometry_metrics(comp, len(slab), slab, molecules[spec["model_name"]])
            current_status, reason, current_eligible = classify(current, spec["model_name"])
            if not current_eligible and current_status != "WARNING":
                guard_state["reason"] = reason
                guard_state["status"] = current_status
                raise UnsafeGeometry(reason)

        optimizer = FIRE(
            comp,
            logfile=str(pilot_logs / f"{spec['pose_id']}.log"),
            trajectory=str(pilot_dir / f"{spec['pose_id']}.traj"),
        )
        optimizer.attach(guard, interval=1)
        interrupted = False
        pilot_converged = False
        try:
            pilot_converged = bool(optimizer.run(fmax=args.fmax, steps=args.pilot_steps))
        except UnsafeGeometry:
            interrupted = True
        energy = finite_number(comp.get_potential_energy(), f"{spec['pose_id']} post-FIRE pilot energy")
        forces = np.asarray(comp.get_forces(), dtype=float)[len(slab):]
        require_finite_array(forces, f"{spec['pose_id']} post-FIRE pilot forces")
        metrics = geometry_metrics(comp, len(slab), slab, molecules[spec["model_name"]])
        metrics["contact_F_anchor_offset_A"] = anchor_offset_A(comp, len(slab), spec["anchor_A"])
        status, reason, eligible = classify(metrics, spec["model_name"])
        if interrupted:
            status = guard_state["status"] or "QUARANTINE"
            reason = guard_state["reason"]
            eligible = False
        structure_hashes = write_structure_pair(pilot_dir / spec["pose_id"], comp)
        rows.append(
            {
                **record_base(spec, args, "pilot"),
                **metrics,
                **structure_hashes,
                "E_initial_complex_eV": energy_initial,
                "E_complex_eV": energy,
                "pose_score_eV": energy - energies["slab"] - energies[spec["model_name"]],
                "pilot_FIRE_tested": True,
                "pilot_converged": pilot_converged,
                "pilot_steps_completed": int(getattr(optimizer, "nsteps", -1)),
                "fmax_after_pilot_eV_A": float(np.linalg.norm(forces, axis=1).max()),
                "status": status,
                "reason": reason,
                "ranking_eligible": eligible,
            }
        )
    payload = {
        "ok": all(row["ranking_eligible"] for row in rows),
        "inputs": inputs,
        "model": args.model,
        "task": args.task,
        "protocol_fingerprint": protocol["fingerprint"],
        "protocol": protocol,
        "rows": rows,
        "gpu": gpu_snapshot(),
    }
    atomic_json(args.out / "PILOT.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
    if not payload["ok"]:
        raise SystemExit("pilot geometry gate failed")


def run_rigid(args) -> None:
    validate_inputs()
    slab, molecules = prepare_structures()
    specs = build_pose_specs(slab, args.gap)
    calc = load_calculator(args.model, args.task, args.device)
    energies = reference_energies(calc, slab, molecules, args.out, args)
    records_dir = args.out / "rigid_records"
    structures_dir = args.out / "rigid_structures"
    total = len(specs)
    fingerprint = protocol_payload(args, "rigid")["fingerprint"]
    for number, spec in enumerate(specs, 1):
        record_path = records_dir / f"{spec['pose_id']}.json"
        existing = require_matching_record(record_path, fingerprint)
        if existing is not None:
            verify_structure_record(existing, structures_dir, "rigid")
            print(f"[rigid {number:03d}/{total:03d}] skip {spec['pose_id']}", flush=True)
            continue
        started = time.time()
        comp = make_complex(slab, molecules[spec["model_name"]], spec)
        metrics = geometry_metrics(comp, len(slab), slab, molecules[spec["model_name"]])
        metrics["initial_contact_F_anchor_offset_A"] = anchor_offset_A(
            comp, len(slab), spec["anchor_A"]
        )
        if metrics["initial_contact_F_anchor_offset_A"] > 1e-6:
            raise SystemExit(
                f"contact-F placement error for {spec['pose_id']}: "
                f"{metrics['initial_contact_F_anchor_offset_A']:.6g} A"
            )
        status, reason, eligible = classify(metrics, spec["model_name"])
        energy = None
        score = None
        if status not in ("QUARANTINE", "UMA_UNSUPPORTED_REACTION", "CAP_ARTIFACT"):
            comp.calc = calc
            energy = finite_number(comp.get_potential_energy(), f"{spec['pose_id']} rigid energy")
            score = energy - energies["slab"] - energies[spec["model_name"]]
        structure_hashes = write_structure_pair(structures_dir / spec["pose_id"], comp)
        row = {
            **record_base(spec, args, "rigid"),
            **metrics,
            **structure_hashes,
            "E_complex_eV": energy,
            "pose_score_eV": score,
            "status": status,
            "reason": reason,
            "ranking_eligible": bool(eligible and score is not None),
            "wall_seconds": round(time.time() - started, 3),
        }
        atomic_json(record_path, row)
        print(
            f"[rigid {number:03d}/{total:03d}] {spec['pose_id']} "
            f"score={score if score is not None else float('nan'):+.4f} status={status}",
            flush=True,
        )
    rows = collect_json(records_dir)
    validate_record_set(
        rows,
        [spec["pose_id"] for spec in specs],
        fingerprint,
        "rigid",
        structures_dir,
    )
    atomic_csv(args.out / "rigid_poses.csv", rows)
    write_shortlist(args.out, rows, args)


def collect_json(directory: Path) -> List[Dict[str, Any]]:
    rows = []
    if directory.is_dir():
        for path in sorted(directory.glob("*.json")):
            rows.append(json.loads(path.read_text(encoding="utf-8")))
    return rows


def validate_record_set(
    rows: Sequence[Dict[str, Any]],
    expected_ids: Sequence[str],
    fingerprint: str,
    label: str,
    structures_dir: Path,
) -> None:
    actual_ids = [str(row.get("pose_id", "")) for row in rows]
    duplicates = sorted(name for name, count in Counter(actual_ids).items() if count > 1)
    missing = sorted(set(expected_ids) - set(actual_ids))
    extra = sorted(set(actual_ids) - set(expected_ids))
    mismatched = sorted(
        str(row.get("pose_id", ""))
        for row in rows
        if row.get("protocol_fingerprint") != fingerprint
    )
    if duplicates or missing or extra or mismatched:
        raise SystemExit(
            f"incomplete/incompatible {label} records\n"
            f"duplicates={duplicates}\nmissing={missing}\nextra={extra}\n"
            f"fingerprint_mismatch={mismatched}\n"
            "Resume the matching protocol or use a new OUT directory."
        )
    for row in rows:
        verify_structure_record(row, structures_dir, label)


def choose_diverse(rows: Sequence[Dict[str, Any]], model_name: str, limit: int) -> List[Dict[str, Any]]:
    eligible = [
        row for row in rows
        if row.get("model_name") == model_name
        and row.get("ranking_eligible")
        and row.get("pose_score_eV") is not None
    ]
    eligible.sort(key=lambda row: (row.get("status") != "OK", float(row["pose_score_eV"])))
    required = {
        *(('site', site) for site in SITE_ORDER),
        *(('azimuth', angle) for angle in AZIMUTHS_DEG),
        *(('roll', angle) for angle in ROLLS_DEG[model_name]),
    }

    def categories(row: Dict[str, Any]) -> set:
        return {
            ("site", row["initial_site"]),
            ("azimuth", int(row["azimuth_deg"])),
            ("roll", int(row["roll_deg"])),
        }

    ok_only = [row for row in eligible if row.get("status") == "OK"]
    pool = ok_only if set().union(*(categories(row) for row in ok_only)) >= required else eligible
    selected: List[Dict[str, Any]] = []
    used = set()
    covered = set()
    while not required <= covered and len(selected) < limit:
        candidates = [row for row in pool if row["pose_id"] not in used]
        if not candidates:
            break
        row = min(
            candidates,
            key=lambda candidate: (
                -len(categories(candidate) & (required - covered)),
                candidate.get("status") != "OK",
                float(candidate["pose_score_eV"]),
            ),
        )
        new_count = len(categories(row) & (required - covered))
        if new_count == 0:
            break
        selected.append(row)
        used.add(row["pose_id"])
        covered |= categories(row)
    if not required <= covered:
        raise SystemExit(
            f"cannot preserve required {model_name} site/azimuth/roll diversity "
            f"within {limit} relax slots; missing={sorted(required - covered)}"
        )
    for row in eligible:
        if len(selected) >= limit:
            break
        if row["pose_id"] not in used:
            selected.append(row)
            used.add(row["pose_id"])
    return selected[:limit]


def write_shortlist(out: Path, rows: Sequence[Dict[str, Any]], args) -> List[Dict[str, Any]]:
    shortlist: List[Dict[str, Any]] = []
    for model_name in ("dimer", "c10"):
        shortlist.extend(choose_diverse(rows, model_name, RELAX_LIMIT[model_name]))
    atomic_csv(out / "RELAX_SHORTLIST.csv", shortlist)
    atomic_json(
        out / "RELAX_SHORTLIST.json",
        {
            "protocol_fingerprint": protocol_payload(args, "rigid")["fingerprint"],
            "selection": "greedy coverage of every representative site, azimuth, and roll; then lowest remaining scores",
            "warning": "Diversity-preserving geometry funnel, not a physical site-preference result.",
            "rows": shortlist,
        },
    )
    return shortlist


def run_relax(args) -> None:
    validate_inputs()
    slab, molecules = prepare_structures()
    specs = build_pose_specs(slab, args.gap)
    rigid_rows = collect_json(args.out / "rigid_records")
    rigid_fingerprint = protocol_payload(args, "rigid")["fingerprint"]
    validate_record_set(
        rigid_rows,
        [spec["pose_id"] for spec in specs],
        rigid_fingerprint,
        "rigid",
        args.out / "rigid_structures",
    )
    shortlist = write_shortlist(args.out, rigid_rows, args)
    calc = load_calculator(args.model, args.task, args.device)
    energies = reference_energies(calc, slab, molecules, args.out, args)
    records_dir = args.out / "relaxed_records"
    structures_dir = args.out / "relaxed_structures"
    logs_dir = args.out / "optimizer_logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    FIRE = fire_class()
    total = len(shortlist)
    fingerprint = protocol_payload(args, "relaxed")["fingerprint"]
    for number, spec in enumerate(shortlist, 1):
        record_path = records_dir / f"{spec['pose_id']}.json"
        existing = require_matching_record(record_path, fingerprint)
        if existing is not None:
            verify_structure_record(existing, structures_dir, "relaxed")
            print(f"[relax {number:02d}/{total:02d}] skip {spec['pose_id']}", flush=True)
            continue
        started = time.time()
        comp = make_complex(slab, molecules[spec["model_name"]], spec)
        comp.calc = calc
        finite_number(comp.get_potential_energy(), f"{spec['pose_id']} initial relax energy")
        require_finite_array(comp.get_forces(), f"{spec['pose_id']} initial relax forces")
        trajectory = structures_dir / f"{spec['pose_id']}.traj"
        trajectory.parent.mkdir(parents=True, exist_ok=True)
        optimizer = FIRE(
            comp,
            logfile=str(logs_dir / f"{spec['pose_id']}.log"),
            trajectory=str(trajectory),
        )
        guard_state = {"reason": "", "status": "", "last": {}}

        def guard() -> None:
            metrics = geometry_metrics(comp, len(slab), slab, molecules[spec["model_name"]])
            guard_state["last"] = metrics
            current_status, reason, current_eligible = classify(metrics, spec["model_name"])
            if not current_eligible and current_status != "WARNING":
                guard_state["reason"] = reason
                guard_state["status"] = current_status
                raise UnsafeGeometry(reason)

        optimizer.attach(guard, interval=1)
        converged = False
        interrupted = False
        try:
            converged = bool(optimizer.run(fmax=args.fmax, steps=args.steps))
        except UnsafeGeometry as exc:
            interrupted = True
            print(f"  quarantine: {exc}", flush=True)
        energy = finite_number(comp.get_potential_energy(), f"{spec['pose_id']} relaxed energy")
        metrics = geometry_metrics(comp, len(slab), slab, molecules[spec["model_name"]])
        metrics["contact_F_anchor_offset_A"] = anchor_offset_A(comp, len(slab), spec["anchor_A"])
        status, reason, eligible = classify(metrics, spec["model_name"])
        if interrupted:
            status = guard_state["status"] or "QUARANTINE"
            reason = guard_state["reason"]
            eligible = False
        if not converged and not interrupted:
            status = "NOT_CONVERGED"
            reason = f"FIRE did not reach fmax={args.fmax} eV/A in {args.steps} steps"
            eligible = False
        forces = np.asarray(comp.get_forces(), dtype=float)[len(slab):]
        require_finite_array(forces, f"{spec['pose_id']} relaxed molecular forces")
        fmax_final = float(np.linalg.norm(forces, axis=1).max())
        score = energy - energies["slab"] - energies[spec["model_name"]]
        structure_hashes = write_structure_pair(structures_dir / spec["pose_id"], comp)
        row = {
            **record_base(spec, args, "relaxed"),
            **metrics,
            **structure_hashes,
            "E_complex_eV": energy,
            "pose_score_eV": score,
            "converged": converged,
            "fmax_final_eV_A": fmax_final,
            "optimizer_steps": int(getattr(optimizer, "nsteps", -1)),
            "status": status,
            "reason": reason,
            "ranking_eligible": bool(eligible and converged),
            "wall_seconds": round(time.time() - started, 3),
        }
        atomic_json(record_path, row)
        print(
            f"[relax {number:02d}/{total:02d}] {spec['pose_id']} score={score:+.4f} "
            f"conv={int(converged)} status={status}",
            flush=True,
        )
    rows = collect_json(records_dir)
    validate_record_set(
        rows,
        [spec["pose_id"] for spec in shortlist],
        fingerprint,
        "relaxed",
        structures_dir,
    )
    write_report(args.out, rows, args)


def molecule_rmsd_A(left, right, nslab: int) -> float:
    if left.get_chemical_symbols() != right.get_chemical_symbols() or len(left) != len(right):
        return float("inf")
    cell = np.asarray(left.cell.array, dtype=float)
    delta = np.asarray(right.positions[nslab:] - left.positions[nslab:], dtype=float)
    frac = np.linalg.solve(cell.T, delta.T).T
    candidates = []
    for replica_shift_b in (0.0, 0.25, 0.5, 0.75):
        shifted = frac.copy()
        shifted[:, 1] -= replica_shift_b
        shifted[:, :2] -= np.round(shifted[:, :2])
        cart = shifted @ cell
        candidates.append(np.sqrt(np.mean(np.sum(cart * cart, axis=1))))
    return finite_number(min(candidates), "basin RMSD")


def coarse_basin_fingerprint(row: Dict[str, Any]) -> str:
    def distance_bin(key: str) -> int:
        return int(round(float(row[key]) / 0.5))

    payload = {
        "nearest_cation": row["nearest_cation"],
        "F_Li_count": min(int(row["contact_F_Li_count"]), 4),
        "F_Ni_count": min(int(row["contact_F_Ni_count"]), 4),
        "F_O_count": min(int(row["contact_F_O_count"]), 6),
        "F_Li_distance_bin_0p5A": distance_bin("min_F_Li_A"),
        "F_Ni_distance_bin_0p5A": distance_bin("min_F_Ni_A"),
        "F_O_distance_bin_0p5A": distance_bin("min_F_O_A"),
        "azimuth_bin_30deg_mod180": int(float(row["chain_azimuth_deg_mod180"]) // 30.0),
        "tilt_bin_15deg": int(float(row["chain_tilt_from_plane_deg"]) // 15.0),
        "height_bin_0p5A": int(
            round(float(row["molecule_COM_height_above_slab_top_A"]) / 0.5)
        ),
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def same_coarse_basin(left: Dict[str, Any], right: Dict[str, Any]) -> bool:
    if left["nearest_cation"] != right["nearest_cation"]:
        return False
    for element in ("Li", "Ni", "O"):
        if abs(int(left[f"contact_F_{element}_count"]) - int(right[f"contact_F_{element}_count"])) > 1:
            return False
        if abs(float(left[f"min_F_{element}_A"]) - float(right[f"min_F_{element}_A"])) > 0.6:
            return False
    az_left = float(left["chain_azimuth_deg_mod180"])
    az_right = float(right["chain_azimuth_deg_mod180"])
    az_delta = abs(az_left - az_right)
    az_delta = min(az_delta, 180.0 - az_delta)
    if az_delta > 35.0:
        return False
    if abs(float(left["chain_tilt_from_plane_deg"]) - float(right["chain_tilt_from_plane_deg"])) > 20.0:
        return False
    if abs(
        float(left["molecule_COM_height_above_slab_top_A"])
        - float(right["molecule_COM_height_above_slab_top_A"])
    ) > 0.75:
        return False
    return True


def cluster_relaxed_basins(
    out: Path,
    rows: Sequence[Dict[str, Any]],
    nslab: int,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    _, read, _ = imports()
    enriched = [dict(row) for row in rows]
    by_id = {row["pose_id"]: row for row in enriched}
    best_by_basin: List[Dict[str, Any]] = []
    for model_name in ("dimer", "c10"):
        subset = [
            row for row in enriched
            if row.get("model_name") == model_name
            and row.get("ranking_eligible")
            and row.get("pose_score_eV") is not None
        ]
        subset.sort(key=lambda row: (row.get("status") != "OK", float(row["pose_score_eV"])))
        representatives: List[Tuple[int, Dict[str, Any], Any]] = []
        for row in subset:
            path = out / "relaxed_structures" / f"{row['pose_id']}.vasp"
            if not path.is_file():
                raise SystemExit(f"missing relaxed structure for basin clustering: {path}")
            atoms = read(path)
            fingerprint = coarse_basin_fingerprint(row)
            assigned = None
            rmsd_to_rep = None
            for basin_id, representative, rep_atoms in representatives:
                if same_coarse_basin(representative, row):
                    candidate_rmsd = molecule_rmsd_A(rep_atoms, atoms, nslab)
                    if candidate_rmsd <= 0.75:
                        assigned = basin_id
                        rmsd_to_rep = candidate_rmsd
                        break
            if assigned is None:
                assigned = len(representatives) + 1
                rmsd_to_rep = 0.0
                representatives.append((assigned, row, atoms))
                best_by_basin.append(row)
            by_id[row["pose_id"]]["basin_id"] = f"{model_name}_B{assigned:02d}"
            by_id[row["pose_id"]]["basin_rmsd_to_representative_A"] = rmsd_to_rep
            by_id[row["pose_id"]]["coarse_basin_fingerprint"] = fingerprint
    for row in enriched:
        row.setdefault("basin_id", "")
        row.setdefault("basin_rmsd_to_representative_A", None)
        row.setdefault("coarse_basin_fingerprint", "")
    return enriched, best_by_basin


def matched_li_ni_counterfactual(
    rigid_rows: Sequence[Dict[str, Any]], model_name: str
) -> List[Dict[str, Any]]:
    groups: Dict[Tuple[int, int], Dict[str, Dict[str, Any]]] = {}
    for row in rigid_rows:
        if row.get("model_name") != model_name or not row.get("ranking_eligible"):
            continue
        site = row.get("initial_site")
        if site not in ("Li_top", "Ni_top"):
            continue
        key = (int(row["azimuth_deg"]), int(row["roll_deg"]))
        groups.setdefault(key, {})[site] = row
    pairs = []
    for key, group in groups.items():
        if "Li_top" in group and "Ni_top" in group:
            pairs.append((
                float(group["Li_top"]["pose_score_eV"])
                + float(group["Ni_top"]["pose_score_eV"]),
                key,
                group,
            ))
    if not pairs:
        return []
    _, _, best = min(pairs, key=lambda item: item[0])
    return [best["Li_top"], best["Ni_top"]]


def write_report(out: Path, rows: Sequence[Dict[str, Any]], args) -> None:
    verify_existing_handoff(out)
    slab, _ = prepare_structures()
    rows, basin_best = cluster_relaxed_basins(out, rows, len(slab))
    atomic_csv(out / "relaxed_poses.csv", rows)
    eligible = [
        row for row in rows
        if row.get("ranking_eligible") and row.get("pose_score_eV") is not None
    ]
    basin_counts = Counter(row["model_name"] for row in basin_best)
    eligible_counts = Counter(row["model_name"] for row in eligible)
    gate_failures = [
        f"{name}: only {eligible_counts.get(name, 0)} eligible relaxed candidates; need at least 3 for manual basin audit"
        for name in ("dimer", "c10")
        if eligible_counts.get(name, 0) < 3
    ]
    handoff_rows: List[Dict[str, Any]] = []
    rigid_rows = collect_json(out / "rigid_records")
    counterfactuals = {
        name: matched_li_ni_counterfactual(rigid_rows, name) for name in ("dimer", "c10")
    }
    for name, pair in counterfactuals.items():
        if len(pair) != 2:
            gate_failures.append(f"{name}: no matched Li-top/Ni-top rigid counterfactual pair")
    _, read, _ = imports()
    handoff_dir = out / "DFT_HANDOFF"
    handoff_dir.mkdir(parents=True, exist_ok=True)
    for model_name in ("dimer", "c10"):
        subset = [row for row in eligible if row["model_name"] == model_name]
        subset.sort(key=lambda row: (row.get("status") != "OK", float(row["pose_score_eV"])))
        if not subset:
            continue
        baseline = min(float(row["pose_score_eV"]) for row in subset)
        for rank, row in enumerate(subset, 1):
            source = out / "relaxed_structures" / f"{row['pose_id']}.vasp"
            atoms = read(source)
            output_name = f"{row['basin_id']}_{row['pose_id']}"
            handoff_meta = write_handoff_pair(
                handoff_dir / output_name, atoms, len(slab)
            )
            contact_meta = handoff_contact_indices(
                row, handoff_meta["old_to_new_zero_based"], len(slab)
            )
            handoff_rows.append({
                "model_name": model_name,
                "basin_id": row["basin_id"],
                "pose_id": row["pose_id"],
                "geometry_stage": "relaxed_shortlist_candidate",
                "site_role": "relaxed_candidate_manual_basin_audit",
                "priority_tier": "manual_union_candidate",
                "initial_site": row["initial_site"],
                "azimuth_deg": row["azimuth_deg"],
                "roll_deg": row["roll_deg"],
                "registry_signature": row["registry_signature"],
                "relative_pose_score_eV": float(row["pose_score_eV"]) - baseline,
                "source_vasp": str(source.relative_to(out)),
                "handoff_basename": output_name,
                "POSCAR_species_order": " ".join(handoff_meta["species_order"]),
                "DFT_fixed_slab_atoms": handoff_meta["fixed_count"],
                "DFT_fixed_vasp_indices_1based": handoff_meta["fixed_vasp_indices_1based"],
                "DFT_zcut_A": handoff_meta["zcut_A"],
                "DFT_constraint_policy": "bottom half of 192-atom slab fixed; top half and PTFE free",
                "slab_last_vasp_index_1based": handoff_meta["slab_last_vasp_index_1based"],
                "molecule_first_vasp_index_1based": handoff_meta["molecule_first_vasp_index_1based"],
                "handoff_xyz_sha256": handoff_meta["handoff_xyz_sha256"],
                "handoff_vasp_sha256": handoff_meta["handoff_vasp_sha256"],
                **contact_meta,
                "warning": "Per-head UMA geometry candidate; DFT-D3 reranking required.",
            })
    for model_name, pair in counterfactuals.items():
        if len(pair) != 2:
            continue
        baseline = min(float(row["pose_score_eV"]) for row in pair)
        for row in pair:
            source = out / "rigid_structures" / f"{row['pose_id']}.vasp"
            if not source.is_file():
                raise SystemExit(f"missing rigid counterfactual structure: {source}")
            atoms = read(source)
            site_role = "matched_Li_counterfactual" if row["initial_site"] == "Li_top" else "matched_Ni_counterfactual"
            output_name = f"{model_name}_{site_role}_{row['pose_id']}"
            handoff_meta = write_handoff_pair(
                handoff_dir / output_name, atoms, len(slab)
            )
            contact_meta = handoff_contact_indices(
                row, handoff_meta["old_to_new_zero_based"], len(slab)
            )
            handoff_rows.append({
                "model_name": model_name,
                "basin_id": "",
                "pose_id": row["pose_id"],
                "geometry_stage": "rigid_counterfactual",
                "site_role": site_role,
                "priority_tier": "required_matched_site_pair",
                "initial_site": row["initial_site"],
                "azimuth_deg": row["azimuth_deg"],
                "roll_deg": row["roll_deg"],
                "registry_signature": row["registry_signature"],
                "relative_pose_score_eV": float(row["pose_score_eV"]) - baseline,
                "source_vasp": str(source.relative_to(out)),
                "handoff_basename": output_name,
                "POSCAR_species_order": " ".join(handoff_meta["species_order"]),
                "DFT_fixed_slab_atoms": handoff_meta["fixed_count"],
                "DFT_fixed_vasp_indices_1based": handoff_meta["fixed_vasp_indices_1based"],
                "DFT_zcut_A": handoff_meta["zcut_A"],
                "DFT_constraint_policy": "bottom half of 192-atom slab fixed; top half and PTFE free",
                "slab_last_vasp_index_1based": handoff_meta["slab_last_vasp_index_1based"],
                "molecule_first_vasp_index_1based": handoff_meta["molecule_first_vasp_index_1based"],
                "handoff_xyz_sha256": handoff_meta["handoff_xyz_sha256"],
                "handoff_vasp_sha256": handoff_meta["handoff_vasp_sha256"],
                **contact_meta,
                "warning": "Same-azimuth/roll Li-vs-Ni starting pair; both require the identical DFT relaxation protocol.",
            })
    atomic_csv(out / "DFT_HANDOFF.csv", handoff_rows)
    atomic_json(out / "DFT_HANDOFF.json", {
        "protocol_fingerprint": protocol_payload(args, "relaxed")["fingerprint"],
        "minimum_eligible_relaxed_candidates_for_manual_basin_audit": {"dimer": 3, "c10": 3},
        "gate_passed": not gate_failures,
        "gate_failures": gate_failures,
        "basin_definition": "diagnostic proxy: similar contact/orientation/height metrics and atom-wise molecular RMSD <= 0.75 A after 1x4 replica translations",
        "basin_proxy_caveat": "No candidate is dropped by automatic clustering. All eligible relaxed candidates are handed off; manual visual merging/audit is required before claiming independent physical basins.",
        "manual_structure_audit_required": True,
        "warning": "Candidate manifest for DFT-D3; not a site-preference or energy conclusion.",
        "rows": handoff_rows,
    })
    lines = [
        "# PTFE/LiNiO2 UMA geometry-prescreen report",
        "",
        f"- Model/task: `{args.model}` / `{args.task}`",
        "- Slab: fully frozen 192-atom LiNiO2(104), fixed-axis 1x4 coverage screen",
        "- Score: internal UMA pose score only; **not a binding energy**",
        "- Dimer and C10 scores are never compared with each other",
        "- Any bond change, artificial H-cap contact, or image overlap is excluded",
        f"- Completion: {len(rows)}/{sum(RELAX_LIMIT.values())} relaxed records",
        f"- Strict eligible basin proxies (manual audit pending): dimer={basin_counts.get('dimer', 0)}, c10={basin_counts.get('c10', 0)}",
        f"- Candidate handoff completeness gate (not physical basin validation): {'PASS' if not gate_failures else 'FAIL'}",
        "",
    ]
    for model_name in ("dimer", "c10"):
        subset = [row for row in eligible if row["model_name"] == model_name]
        subset.sort(key=lambda row: (row.get("status") != "OK", float(row["pose_score_eV"])))
        lines.extend([f"## {model_name}", ""])
        if not subset:
            lines.extend(["No eligible converged pose.", ""])
            continue
        lines.extend([
            "| rank | pose | initial site | post-relax registry | relative score (eV) | image min (A) | status |",
            "|---:|---|---|---|---:|---:|---|",
        ])
        baseline = min(float(row["pose_score_eV"]) for row in subset)
        for rank, row in enumerate(subset[:8], 1):
            delta = float(row["pose_score_eV"]) - baseline
            lines.append(
                f"| {rank} | `{row['pose_id']}` | {row['initial_site']} | "
                f"{row['registry_signature']} ({row['basin_id']}) | {delta:+.4f} | "
                f"{float(row['lateral_image_min_A']):.2f} | {row['status']} |"
            )
        lines.extend([
            "",
            "A 0.05 eV window is only a minimum duplicate-grouping heuristic, not calibrated uncertainty.",
            "Scores outside that window are not automatically resolved. Preserve basin/head diversity for DFT-D3.",
            "",
        ])
    excluded = Counter(str(row.get("status", "UNKNOWN")) for row in rows if not row.get("ranking_eligible"))
    lines.extend(["## Excluded or pending", "", f"`{dict(excluded)}`", ""])
    if gate_failures:
        lines.extend(["## Blocking gate failures", ""] + [f"- {item}" for item in gate_failures] + [""])
    (out / "RESULTS.md").write_text("\n".join(lines), encoding="utf-8")
    if gate_failures:
        raise SystemExit("DFT handoff blocked: " + "; ".join(gate_failures))


def run_report(args) -> None:
    validate_inputs()
    slab, _ = prepare_structures()
    specs = build_pose_specs(slab, args.gap)
    rigid_rows = collect_json(args.out / "rigid_records")
    validate_record_set(
        rigid_rows,
        [spec["pose_id"] for spec in specs],
        protocol_payload(args, "rigid")["fingerprint"],
        "rigid",
        args.out / "rigid_structures",
    )
    shortlist = write_shortlist(args.out, rigid_rows, args)
    rows = collect_json(args.out / "relaxed_records")
    validate_record_set(
        rows,
        [spec["pose_id"] for spec in shortlist],
        protocol_payload(args, "relaxed")["fingerprint"],
        "relaxed",
        args.out / "relaxed_structures",
    )
    write_report(args.out, rows, args)
    print((args.out / "RESULTS.md").read_text(encoding="utf-8"))


def run_plan(args) -> None:
    report = validate_inputs()
    slab, _ = prepare_structures()
    specs = build_pose_specs(slab, args.gap)
    anchors = {name: [float(x) for x in point] for name, point in site_anchors(slab).items()}
    counts = Counter(spec["model_name"] for spec in specs)
    protocol = protocol_payload(args, "plan")
    payload = {
        "protocol_fingerprint": protocol["fingerprint"],
        "protocol": protocol,
        "inputs": report,
        "anchors_A": anchors,
        "pose_counts": dict(counts),
        "total_rigid_poses": len(specs),
        "relax_limits": RELAX_LIMIT,
        "azimuths_deg": AZIMUTHS_DEG,
        "rolls_deg": ROLLS_DEG,
        "gap_A": args.gap,
        "scope": "fixed-axis, frozen-slab geometry prescreen only",
    }
    args.out.mkdir(parents=True, exist_ok=True)
    atomic_json(args.out / "PLAN.json", payload)
    atomic_csv(args.out / "POSE_PLAN.csv", specs)
    print(json.dumps(payload, indent=2, sort_keys=True))


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("stage", choices=("plan", "pilot", "rigid", "relax", "report"))
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--model", default=os.environ.get("UMA_MODEL", "uma-s-1p1"))
    ap.add_argument("--task", default=os.environ.get("UMA_TASK", "oc20"))
    ap.add_argument("--device", default=os.environ.get("UMA_DEVICE", "cuda"))
    ap.add_argument("--gap", type=float, default=2.9)
    ap.add_argument("--fmax", type=float, default=0.05)
    ap.add_argument("--steps", type=int, default=200)
    ap.add_argument("--pilot-steps", type=int, default=2)
    return ap


def main() -> int:
    global np
    if sys.version_info < (3, 8):
        raise SystemExit("Python 3.8+ is required")
    args = parser().parse_args()
    try:
        import numpy as np
    except ImportError as exc:
        raise SystemExit(f"NumPy import failed: {exc}")
    args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=True)
    if args.stage == "plan":
        run_plan(args)
    elif args.stage == "pilot":
        run_pilot(args)
    elif args.stage == "rigid":
        run_rigid(args)
    elif args.stage == "relax":
        run_relax(args)
    elif args.stage == "report":
        run_report(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
