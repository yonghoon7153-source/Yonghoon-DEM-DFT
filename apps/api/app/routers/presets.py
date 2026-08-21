"""Saved builds: a blend plus the cell settings that come with it.

The list used to be eight formulations hard-coded in ``wrdkit``.  None of them
was what this lab actually presses, and adding one meant editing Python.  Now
the researcher saves what is in front of them, by name, and both people share
the list because it lives here rather than in one browser (ADR 0010).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from wrdkit import Composition

from ..db import get_session
from ..models import CompositionPreset
from ..schemas import (
    ComponentOut,
    CompositionPresetIn,
    CompositionPresetOut,
    PresetSettings,
)

router = APIRouter(prefix="/api/composition-presets", tags=["presets"])


def _components(preset: CompositionPreset) -> Composition:
    if not preset.components_json:
        return Composition()
    try:
        return Composition.from_json(json.loads(preset.components_json))
    except (ValueError, TypeError):
        return Composition()


def _settings(preset: CompositionPreset) -> PresetSettings:
    """Never let a bad blob take the whole list down.

    A preset with unreadable settings is still a usable blend, and a 500 on
    ``GET`` would hide every other preset behind it.
    """
    if not preset.settings_json:
        return PresetSettings()
    try:
        return PresetSettings.model_validate_json(preset.settings_json)
    except ValueError:
        return PresetSettings()


def _out(preset: CompositionPreset) -> CompositionPresetOut:
    composition = _components(preset)
    text = composition.label()
    return CompositionPresetOut(
        id=preset.id,
        name=preset.name,
        text=text,
        # The dropdown has to say what a preset *is*, not only what it is
        # called: "건식 80" tells you nothing six months later, and the ratio
        # is the thing being chosen.
        label=f"{preset.name} · {text}" if text else preset.name,
        composition=[ComponentOut(**c) for c in composition.to_json()],
        settings=_settings(preset),
        created_at=preset.created_at,
        updated_at=preset.updated_at,
    )


@router.get("", response_model=list[CompositionPresetOut])
def list_presets(session: Session = Depends(get_session)):
    presets = session.exec(
        select(CompositionPreset).order_by(CompositionPreset.name)).all()
    return [_out(preset) for preset in presets]


@router.post("", response_model=CompositionPresetOut, status_code=201)
def save_preset(payload: CompositionPresetIn,
                session: Session = Depends(get_session)):
    name = payload.name.strip()
    if not name:
        raise HTTPException(422, "preset name cannot be empty")
    if not payload.composition and not payload.settings.filled():
        raise HTTPException(422, "a preset needs a composition or a setting to carry")

    composition = Composition.from_json([c.model_dump() for c in payload.composition])
    existing = session.exec(
        select(CompositionPreset).where(CompositionPreset.name == name)).first()
    if existing is not None and not payload.overwrite:
        raise HTTPException(409, f'"{name}" 프리셋이 이미 있습니다')

    preset = existing or CompositionPreset(name=name)
    preset.components_json = json.dumps(composition.to_json(), ensure_ascii=False)
    preset.settings_json = payload.settings.model_dump_json(exclude_none=True)
    preset.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    session.add(preset)
    session.commit()
    session.refresh(preset)
    return _out(preset)


@router.delete("/{preset_id}", status_code=204)
def delete_preset(preset_id: int, session: Session = Depends(get_session)):
    preset = session.get(CompositionPreset, preset_id)
    if preset is None:
        raise HTTPException(404, "preset not found")
    session.delete(preset)
    session.commit()
