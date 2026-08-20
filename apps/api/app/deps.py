"""Shared route helpers."""

from __future__ import annotations

from fastapi import HTTPException
from sqlmodel import Session

from wrdkit import BASES, ResolvedCell, basis_label

from .models import ExperimentGroup, Run, Sample
from .schemas import ComponentOut, ResolvedCellOut


def get_sample(session: Session, sample_id: int) -> Sample:
    sample = session.get(Sample, sample_id)
    if sample is None:
        raise HTTPException(404, f"sample {sample_id} not found")
    return sample


def get_run(session: Session, run_id: int) -> Run:
    run = session.get(Run, run_id)
    if run is None:
        raise HTTPException(404, f"run {run_id} not found")
    return run


def get_group(session: Session, group_id: int) -> ExperimentGroup:
    group = session.get(ExperimentGroup, group_id)
    if group is None:
        raise HTTPException(404, f"group {group_id} not found")
    return group


def validate_basis(basis: str) -> str:
    if basis not in BASES:
        raise HTTPException(422, f"basis must be one of {list(BASES)}, got {basis!r}")
    return basis


def resolved_cell_out(cell: ResolvedCell) -> ResolvedCellOut:
    composition = cell.composition or None
    return ResolvedCellOut(
        active_mass_g=cell.active_mass_g,
        active_wt_percent=cell.active_wt_percent,
        composition=[ComponentOut(**c) for c in (composition.to_json() if composition else [])],
        composition_label=cell.composition_label,
        composition_compact_label=cell.composition_compact_label,
        composition_problems=cell.composition_problems,
        area_cm2=cell.area_cm2,
        volume_cm3=cell.volume_cm3,
        loading_mg_cm2=cell.loading_mg_cm2,
        nominal_capacity_mah=cell.nominal_capacity_mah,
        nominal_specific_capacity_mah_g=cell.nominal_specific_capacity_mah_g,
        available_bases=cell.available_bases(),
        unavailable={b: reason for b in BASES
                     if (reason := cell.missing_for(b)) is not None},
        notes=cell.notes,
    )


def basis_label_for(basis: str) -> str:
    return basis_label(basis)
