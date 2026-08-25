"""Cells: their composition, their normalisation inputs, their state."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from wrdkit import BASES
from wrdkit.health import DEFAULT_REFERENCE_CYCLE

from .. import storage
from ..db import get_session
from ..deps import get_sample, resolved_cell_out, validate_basis
from ..models import (
    CycleRecord,
    ExperimentGroup,
    GittRun,
    Run,
    Sample,
    SpectrumRecord,
)
from ..schemas import (
    ComponentOut,
    MeasurementOut,
    MeasurementsOut,
    SampleIn,
    SampleOut,
    SampleUpdate,
)
from ..services import (
    apply_composition,
    resolve_cell,
    sample_composition,
    sample_formation,
    sample_reference_cycle,
)

router = APIRouter(prefix="/api/samples", tags=["samples"])

VALID_STATES = {"auto", "running", "finished"}


def _out(session: Session, sample: Sample) -> SampleOut:
    runs = session.exec(select(Run).where(Run.sample_id == sample.id)).all()
    cycles = sum(run.complete_cycle_count for run in runs)
    group_name = None
    if sample.group_id:
        group = session.get(ExperimentGroup, sample.group_id)
        group_name = group.name if group else None
    composition = sample_composition(sample)
    # 저장된 기준 사이클과 **실제로 쓰이는** 기준 사이클은 다를 수 있다:
    # formation 이 없는 스케줄은 1번에 앵커한다 (ADR 0018).  둘 다 낸다 --
    # 입력란은 저장값을 보여 줘야 하고, 화면 문구는 쓰이는 값을 말해야 한다.
    formation = sample_formation(sample)
    anchor, anchor_reason = sample_reference_cycle(sample)
    return SampleOut(
        **sample.model_dump(exclude={"composition_json"}),
        group_name=group_name,
        run_count=len(runs),
        cycle_count=cycles,
        composition=[ComponentOut(**c) for c in composition.to_json()],
        composition_label=composition.label(),
        resolved_cell=resolved_cell_out(resolve_cell(sample)),
        reference_cycle_effective=anchor,
        reference_cycle_reason=anchor_reason,
        formation=formation,
    )


@router.get("", response_model=list[SampleOut])
def list_samples(
    session: Session = Depends(get_session),
    group_id: int | None = None,
    cathode_type: str | None = None,
    process: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    c_rate: float | None = None,
    search: str | None = None,
):
    """Filter the library the way the bench does: by group, chemistry, date."""
    statement = select(Sample)
    if group_id is not None:
        statement = statement.where(Sample.group_id == group_id)
    if cathode_type:
        statement = statement.where(Sample.cathode_type == cathode_type)
    if process:
        statement = statement.where(Sample.process == process)
    if date_from:
        statement = statement.where(Sample.test_date >= date_from)
    if date_to:
        statement = statement.where(Sample.test_date <= date_to)
    if c_rate is not None:
        statement = statement.where(Sample.c_rate == c_rate)
    samples = session.exec(statement.order_by(Sample.test_date.desc(),
                                              Sample.name)).all()
    if search:
        needle = search.lower()
        samples = [
            s for s in samples
            if needle in s.name.lower()
            or needle in (s.cathode_detail or "").lower()
            or needle in (s.notes or "").lower()
        ]
    return [_out(session, sample) for sample in samples]


@router.get("/facets")
def sample_facets(session: Session = Depends(get_session)):
    """Distinct values for the filter controls, so the UI need not guess."""
    samples = session.exec(select(Sample)).all()

    def distinct(attribute: str) -> list:
        values = {getattr(s, attribute) for s in samples}
        return sorted(v for v in values if v not in (None, ""))

    return {
        "cathode_type": distinct("cathode_type"),
        "cathode_detail": distinct("cathode_detail"),
        "process": distinct("process"),
        "electrolyte": distinct("electrolyte"),
        "anode": distinct("anode"),
        "c_rate": distinct("c_rate"),
        "temperature_c": distinct("temperature_c"),
        "test_date": distinct("test_date"),
        "bases": list(BASES),
    }


@router.post("", response_model=SampleOut, status_code=201)
def create_sample(payload: SampleIn, session: Session = Depends(get_session)):
    if not payload.name.strip():
        raise HTTPException(422, "sample name cannot be empty")
    if payload.declared_state not in VALID_STATES:
        raise HTTPException(422, f"declared_state must be one of {sorted(VALID_STATES)}")
    values = payload.model_dump(exclude={"composition", "composition_text"})
    values["name"] = payload.name.strip()
    if "reference_cycle" in payload.model_fields_set:
        # 스키마 기본값 3 도 model_dump 에 실려 오므로, 보낸 값과 기본값은
        # model_fields_set 으로만 구별된다.  적어 두지 않으면 formation 없는
        # 스케줄이 POST 로 준 기준을 영원히 1 로 덮어쓴다 (ADR 0018).
        values["reference_cycle_source"] = "user"
    sample = Sample(**values)
    apply_composition(sample, payload.composition, payload.composition_text,
                      explicit_wt_percent=payload.active_wt_percent is not None)
    session.add(sample)
    session.commit()
    session.refresh(sample)
    return _out(session, sample)


@router.get("/{sample_id}", response_model=SampleOut)
def read_sample(sample_id: int, session: Session = Depends(get_session)):
    return _out(session, get_sample(session, sample_id))


@router.patch("/{sample_id}", response_model=SampleOut)
def update_sample(sample_id: int, payload: SampleUpdate,
                  session: Session = Depends(get_session)):
    """Correcting a mass here re-normalises every reading instantly (ADR 0001)."""
    sample = get_sample(session, sample_id)
    sent = payload.model_dump(exclude_unset=True)
    values = payload.model_dump(exclude_unset=True,
                                exclude={"clear", "composition", "composition_text"})
    if "declared_state" in values and values["declared_state"] not in VALID_STATES:
        raise HTTPException(422, f"declared_state must be one of {sorted(VALID_STATES)}")
    # POST refuses an empty name; PATCH has to refuse it too.  A blank name
    # leaves a row that is a link with nothing to click on every screen, and
    # nothing else identifies the cell -- the id is not shown anywhere.
    if "name" in values:
        name = (values["name"] or "").strip()
        if not name:
            raise HTTPException(422, "sample name cannot be empty")
        values["name"] = name
    reference = values.get("reference_cycle")
    if reference is not None and reference < 1:
        raise HTTPException(422, "reference_cycle must be 1 or greater")
    if reference is not None:
        # 사람이 친 값이라고 적어 둔다.  저장된 3 이 기본값인지 입력인지
        # 구별되지 않으면, formation 없는 스케줄이 그것을 영원히 1 로
        # 덮어쓴다 (ADR 0018).
        values["reference_cycle_source"] = "user"
    for key, value in values.items():
        setattr(sample, key, value)
    # Clearing happens first so a request that drops a hand-typed wt% and
    # sends a composition in the same breath ends with the composition's
    # value stored, not a null.
    for field in payload.clear:
        if field == "composition":
            sample.composition_json = ""
        elif field == "reference_cycle":
            # 고정 해제이지 NULL 이 아니다.  컬럼은 NOT NULL 이고 SampleOut 도
            # int 라 None 은 500 이 된다.  기본값으로 되돌리고 출처를 지워서
            # 자동 해석(기본 3, formation 없으면 1)이 다시 일하게 한다.
            sample.reference_cycle = DEFAULT_REFERENCE_CYCLE
            sample.reference_cycle_source = ""
        elif hasattr(sample, field):
            setattr(sample, field, None)
    if "composition" in sent or "composition_text" in sent:
        apply_composition(sample, payload.composition, payload.composition_text,
                          explicit_wt_percent="active_wt_percent" in sent)
    sample.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    session.add(sample)
    session.commit()
    session.refresh(sample)
    return _out(session, sample)


@router.delete("/{sample_id}", status_code=204)
def delete_sample(sample_id: int, session: Session = Depends(get_session),
                  delete_runs: bool = Query(False,
                                            description="also delete the sample's files")):
    """Detach the sample's runs by default; the uploads themselves are never removed."""
    sample = get_sample(session, sample_id)
    runs = session.exec(select(Run).where(Run.sample_id == sample_id)).all()
    for run in runs:
        if delete_runs:
            for cycle in session.exec(
                    select(CycleRecord).where(CycleRecord.run_id == run.id)).all():
                session.delete(cycle)
            # Same promise as DELETE /api/runs/{id}: the row goes, the parse
            # cache goes with it (the original .wrd stays).  Without this the
            # npz -- megabytes per file, and the largest thing we write -- is
            # orphaned the moment its run id stops resolving.
            storage.drop_run_cache(run.id)
            session.delete(run)
        else:
            run.sample_id = None
            session.add(run)
    # Spectra too.  A row left pointing at a deleted sample id is a live wire:
    # SQLite reuses row ids, so the next cell created inherited the dead
    # cell's impedance as its own measurement (review #9).  Detach, never
    # delete -- the spectrum is a measurement in its own right.
    for spectrum in session.exec(
            select(SpectrumRecord).where(SpectrumRecord.sample_id == sample_id)).all():
        spectrum.sample_id = None
        session.add(spectrum)
    session.delete(sample)
    session.commit()


@router.get("/{sample_id}/bases")
def sample_bases(sample_id: int, session: Session = Depends(get_session),
                 basis: str = Query("mAh")):
    """Which capacity axes this sample can currently express, and why not."""
    validate_basis(basis)
    sample = get_sample(session, sample_id)
    return resolved_cell_out(resolve_cell(sample)).model_dump()


# --------------------------------------------------------------------------
# 이 셀에 무엇이 붙어 있나
# --------------------------------------------------------------------------
def _frequency_span(record: SpectrumRecord) -> str:
    """`7 MHz–10 mHz`.  둘 중 하나라도 없으면 빈 문자열이다 (§0.4)."""
    start, end = record.frequency_start_hz, record.frequency_end_hz
    if start is None or end is None:
        return ""
    return f"{_hz(start)}–{_hz(end)}"


def _hz(value: float) -> str:
    for scale, unit in ((1e6, "MHz"), (1e3, "kHz"), (1.0, "Hz"), (1e-3, "mHz")):
        if abs(value) >= scale:
            return f"{value / scale:g} {unit}"
    return f"{value:g} Hz"


@router.get("/{sample_id}/measurements", response_model=MeasurementsOut)
def sample_measurements(sample_id: int, session: Session = Depends(get_session)):
    """이 셀의 충방전·임피던스·GITT 를 한 번에.

    세 섹션은 서로 독립이지만 셀은 하나다.  같은 셀을 세 번 재 놓고 세 화면을
    따로 열어야 한다면 그건 나눈 것이 아니라 흩어 놓은 것이다.  각 상세
    페이지가 이 한 번의 물음으로 "이 셀의 다른 측정" 을 그린다.

    붙어 있지 않은 측정은 여기 없다.  `sample_id` 가 비어 있는 파일은 이름이
    비슷해도 같은 셀이라고 단정하지 않는다 -- 이름은 기록이지 관계가 아니다.
    """
    sample = session.get(Sample, sample_id)
    if sample is None:
        raise HTTPException(404, f"sample {sample_id} not found")

    runs = session.exec(
        select(Run).where(Run.sample_id == sample_id)
        .order_by(Run.start_time, Run.id)).all()
    spectra = session.exec(
        select(SpectrumRecord).where(SpectrumRecord.sample_id == sample_id)).all()
    spectra = sorted(spectra, key=lambda r: (r.at_cycle is None,
                                             r.at_cycle if r.at_cycle is not None else 0,
                                             r.uploaded_at, r.sweep_index))
    gitt = session.exec(
        select(GittRun).where(GittRun.sample_id == sample_id)
        .order_by(GittRun.start_time, GittRun.id)).all()

    return MeasurementsOut(
        sample_id=sample_id,
        sample_name=sample.name,
        cycling=[MeasurementOut(
            kind="cycling", id=run.id or 0,
            name=run.original_name or f"run {run.id}",
            detail=(f"{run.complete_cycle_count} 사이클"
                    if run.complete_cycle_count else "사이클 없음"),
            measured_at=run.start_time,
        ) for run in runs],
        eis=[MeasurementOut(
            kind="eis", id=record.id or 0,
            name=record.name or record.original_name,
            # 스윕이 여럿인 파일은 몇 번째인지가 곧 SOC 다 (ADR 0022).
            detail=" · ".join(part for part in (
                _frequency_span(record),
                f"{record.sweep_index}/{record.sweep_count}"
                if record.sweep_count > 1 else "",
                record.purpose,
            ) if part),
            measured_at=record.measured_at,
        ) for record in spectra],
        gitt=[MeasurementOut(
            kind="gitt", id=record.id or 0,
            name=record.name or record.original_name,
            detail=f"펄스 {record.n_pulses}개",
            measured_at=record.start_time,
        ) for record in gitt],
    )
