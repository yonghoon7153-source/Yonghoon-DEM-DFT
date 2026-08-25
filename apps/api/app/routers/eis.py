"""Impedance: upload a spectrum, fit a circuit, read the parameters off.

The workflow this replaces is manual end to end -- open the ``.mpr`` in
EC-Lab, export ``.mpt``, open that in ZView, draw a circuit, type six starting
values, fit, copy to the clipboard, paste into Excel.  Everything here is that
same sequence with nobody in it, which is only honest if the failures are as
visible as the successes: a fit that did not converge, a parameter whose error
bar swallows it, points dropped before fitting.  See ADR 0019.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

import numpy as np
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlmodel import Session, select

from wrdkit.eis import (
    LIQUID,
    SOLID,
    Spectrum,
    UnknownColumn,
    ionic_conductivity,
    label_arcs,
    read_mpr_bytes,
    read_mps_text,
    read_mpt_text,
    total_resistance,
)
from wrdkit.eis.derive import CONFIGS

from .. import storage
from ..db import get_session
from ..models import Sample, SpectrumFit, SpectrumRecord
from ..schemas import (
    SpectrumDetailOut,
    SpectrumFitOut,
    SpectrumOut,
    SpectrumPointsOut,
    SpectrumUpdate,
)
from ..settings import settings

router = APIRouter(prefix="/api/eis", tags=["eis"])

KINDS = (LIQUID, SOLID)

#: 무엇을 쟀나.  전해질이 무엇이냐와는 다른 질문이고, 아크의 뜻을 바꾼다 —
#: 전고체 **대칭셀**의 두 아크는 벌크와 입계지만 **풀셀**의 두 아크는 아니다.
CELL_CONFIGS = CONFIGS

#: Circuits offered on screen, per measurement kind.  The first is the default.
#: These are the ones this lab actually uses -- the liquid list comes from the
#: procedure sheet, the solid one from an ion-blocking symmetric cell (two arcs
#: and a blocking tail).  A person can still type any circuit.
PRESETS: dict[str, list[dict]] = {
    LIQUID: [
        {"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)",
         "label": "두 아크 (SEI + 전하이동)",
         "note": "절차서의 기본 회로. 물리적으로 100% 맞지는 않지만 "
                 "피팅이 쉽고 오차가 크지 않아 관례로 쓴다."},
        {"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)-W1",
         "label": "두 아크 + 확산 꼬리",
         "note": "저주파에 45° 직선이 보일 때. 전극 내부 리튬 확산."},
        {"circuit": "R0-p(R1,CPE1)",
         "label": "한 아크",
         "note": "반원이 하나만 보일 때."},
    ],
    SOLID: [
        {"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)-CPE3",
         "label": "벌크 + 입계 + 블로킹",
         "note": "이온 블로킹 전극 대칭셀. 고주파 아크가 grain 내부, "
                 "저주파 아크가 grain boundary, 끝의 CPE 가 리튬 블로킹."},
        {"circuit": "p(R1,CPE1)-p(R2,CPE2)-CPE3",
         "label": "직렬 저항 없이",
         "note": "고주파 절편이 사실상 0 일 때."},
        {"circuit": "R0-p(R1,CPE1)-CPE3",
         "label": "아크 하나 + 블로킹",
         "note": "벌크와 입계가 분리되지 않을 때."},
    ],
}


def _get(session: Session, spectrum_id: int) -> SpectrumRecord:
    record = session.get(SpectrumRecord, spectrum_id)
    if record is None:
        raise HTTPException(404, f"spectrum {spectrum_id} not found")
    return record


def _validate_kind(kind: str) -> str:
    if kind not in KINDS:
        raise HTTPException(422, f"kind must be one of {', '.join(KINDS)}")
    return kind


def _validate_config(config: str) -> str:
    """빈 문자열은 "아직 안 정함" 이다 — 틀린 값이 아니라 없는 값."""
    if config and config not in CELL_CONFIGS:
        raise HTTPException(
            422, f"cell_config must be one of {', '.join(CELL_CONFIGS)} (or empty)")
    return config


def _out(session: Session, record: SpectrumRecord) -> SpectrumOut:
    sample_name = None
    if record.sample_id:
        sample = session.get(Sample, record.sample_id)
        sample_name = sample.name if sample else None
    fits = session.exec(
        select(SpectrumFit).where(SpectrumFit.spectrum_id == record.id)).all()
    best = min((f for f in fits if f.converged and f.chi_squared is not None),
               key=lambda f: f.chi_squared, default=None)
    return SpectrumOut(
        **record.model_dump(exclude={"settings_json"}),
        sample_name=sample_name,
        fit_count=len(fits),
        best_chi_squared=best.chi_squared if best else None,
        best_circuit=best.circuit if best else "",
    )


def _geometry(session: Session, record: SpectrumRecord) -> tuple[float | None, float | None]:
    """Thickness in cm and area in cm², the spectrum's own or the cell's.

    Returns ``None`` for whatever is missing rather than a default: a
    conductivity computed from a made-up thickness is a made-up conductivity
    and looks exactly like a measured one (§0.4).
    """
    thickness_um = record.thickness_um
    area = record.area_cm2
    if (thickness_um is None or area is None) and record.sample_id:
        sample = session.get(Sample, record.sample_id)
        if sample is not None:
            if thickness_um is None:
                thickness_um = sample.thickness_um
            if area is None:
                area = sample.area_cm2
                if area is None and sample.diameter_mm:
                    radius_cm = sample.diameter_mm / 20.0
                    area = float(np.pi * radius_cm ** 2)
    thickness_cm = thickness_um / 1e4 if thickness_um else None
    return thickness_cm, area


# --------------------------------------------------------------------------
# reading
# --------------------------------------------------------------------------
@router.get("/circuits")
def circuits():
    """The circuits the screen offers, and what each one is for."""
    return {"kinds": [{"kind": kind,
                       "label": "액체 전해질" if kind == LIQUID else "전고체",
                       "presets": PRESETS[kind]} for kind in KINDS]}


@router.get("/spectra", response_model=list[SpectrumOut])
def list_spectra(session: Session = Depends(get_session),
                 kind: str | None = Query(None),
                 cell_config: str | None = Query(None),
                 sample_id: int | None = Query(None),
                 search: str | None = Query(None)):
    statement = select(SpectrumRecord)
    if kind:
        statement = statement.where(SpectrumRecord.kind == _validate_kind(kind))
    if cell_config:
        statement = statement.where(
            SpectrumRecord.cell_config == _validate_config(cell_config))
    if sample_id is not None:
        statement = statement.where(SpectrumRecord.sample_id == sample_id)
    records = session.exec(
        statement.order_by(SpectrumRecord.uploaded_at.desc())).all()
    if search:
        needle = search.lower()
        records = [r for r in records
                   if needle in r.name.lower() or needle in r.original_name.lower()]
    return [_out(session, record) for record in records]


@router.get("/spectra/{spectrum_id}", response_model=SpectrumDetailOut)
def read_spectrum(spectrum_id: int, session: Session = Depends(get_session)):
    record = _get(session, spectrum_id)
    thickness_cm, area = _geometry(session, record)
    fits = session.exec(
        select(SpectrumFit).where(SpectrumFit.spectrum_id == spectrum_id)
        .order_by(SpectrumFit.created_at.desc())).all()
    return SpectrumDetailOut(
        **_out(session, record).model_dump(),
        settings=json.loads(record.settings_json) if record.settings_json else {},
        thickness_cm=thickness_cm,
        area_cm2_effective=area,
        fits=[_fit_out(session, record, fit) for fit in fits],
    )


@router.get("/spectra/{spectrum_id}/points", response_model=SpectrumPointsOut)
def spectrum_points(spectrum_id: int, session: Session = Depends(get_session)):
    """The measured points, raw ohms and hertz (ADR 0001)."""
    record = _get(session, spectrum_id)
    spectrum = storage.load_spectrum(spectrum_id)
    if spectrum is None:
        raise HTTPException(
            409, "이 스펙트럼의 파싱 결과가 없습니다 — 파일을 다시 올려 주세요")
    return SpectrumPointsOut(
        id=spectrum_id,
        name=record.name,
        kind=record.kind,
        frequency_hz=[float(v) for v in spectrum.frequency_hz],
        z_re=[float(v) for v in spectrum.z_re],
        z_im=[float(v) for v in spectrum.z_im],
        magnitude=[float(v) for v in spectrum.magnitude],
        phase_deg=[float(v) for v in spectrum.phase_deg],
    )


# --------------------------------------------------------------------------
# writing
# --------------------------------------------------------------------------
def _parse(content: bytes, filename: str) -> tuple[Spectrum, str]:
    """Read whichever of the two formats this is, by content not by name."""
    if content[:22] == b"BIO-LOGIC MODULAR FILE":
        return read_mpr_bytes(content), "mpr"
    text = content.decode("latin-1", errors="replace")
    if "Nb header lines" in text:
        return read_mpt_text(text), "mpt"
    raise HTTPException(
        422,
        f"{filename!r} 은 BioLogic .mpr 도 EC-Lab .mpt 도 아닙니다 — "
        "EC-Lab 에서 저장한 원본이나 텍스트 내보내기를 올려 주세요")


@router.post("/spectra/upload", response_model=SpectrumOut, status_code=201)
async def upload_spectrum(
    file: UploadFile = File(...),
    settings_file: UploadFile | None = File(None),
    sample_id: int | None = Query(None),
    kind: str = Query(LIQUID),
    cell_config: str = Query(""),
    session: Session = Depends(get_session),
):
    """Store one ``.mpr`` or ``.mpt``, with its ``.mps`` when there is one.

    The same bytes twice is the same spectrum, as with cycling files: the same
    measurement reaches us from the instrument PC and from somebody's laptop.
    """
    _validate_kind(kind)
    _validate_config(cell_config)
    if file.size is not None and file.size > settings.max_upload_bytes:
        raise HTTPException(413, f"file is {file.size / 1e6:.0f} MB; the limit is "
                                 f"{settings.max_upload_bytes / 1e6:.0f} MB")
    content = await file.read()
    if not content:
        raise HTTPException(422, "uploaded file is empty")

    digest = hashlib.sha256(content).hexdigest()
    existing = session.exec(
        select(SpectrumRecord).where(SpectrumRecord.sha256 == digest)).first()
    if existing is not None:
        if sample_id is not None and existing.sample_id is None:
            existing.sample_id = sample_id
            session.add(existing)
            session.commit()
            session.refresh(existing)
        return _out(session, existing)

    try:
        spectrum, source_format = _parse(content, file.filename or "upload")
    except UnknownColumn as exc:
        raise HTTPException(422, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(422, f"could not read {file.filename!r}: {exc}") from exc

    meta: dict = {}
    if settings_file is not None:
        raw = await settings_file.read()
        if raw:
            try:
                meta = read_mps_text(raw.decode("latin-1", errors="replace"))
            except ValueError:
                meta = {}

    storage.store_bytes(content,
                        storage.spectrum_upload_path(digest, source_format))

    name = (file.filename or "spectrum").rsplit(".", 1)[0]
    record = SpectrumRecord(
        sample_id=sample_id,
        name=name,
        kind=kind,
        cell_config=cell_config,
        original_name=file.filename or "",
        sha256=digest,
        size_bytes=len(content),
        source_format=source_format,
        n_points=len(spectrum),
        frequency_start_hz=float(np.max(spectrum.frequency_hz)),
        frequency_end_hz=float(np.min(spectrum.frequency_hz)),
        amplitude_mv=_float(meta.get("amplitude_mv")),
        device=str(meta.get("Device", "")),
        technique=str(meta.get("technique", spectrum.metadata.get("technique", ""))),
        settings_json=json.dumps(meta, ensure_ascii=False) if meta else "",
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    storage.cache_spectrum(record.id, spectrum)
    return _out(session, record)


def _float(value) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


@router.patch("/spectra/{spectrum_id}", response_model=SpectrumOut)
def update_spectrum(spectrum_id: int, payload: SpectrumUpdate,
                    session: Session = Depends(get_session)):
    record = _get(session, spectrum_id)
    values = payload.model_dump(exclude_unset=True, exclude={"clear"})
    if "kind" in values:
        _validate_kind(values["kind"])
    if "cell_config" in values:
        values["cell_config"] = _validate_config(values["cell_config"] or "")
    if "name" in values:
        name = (values["name"] or "").strip()
        if not name:
            raise HTTPException(422, "spectrum name cannot be empty")
        values["name"] = name
    if (values.get("sample_id") is not None
            and session.get(Sample, values["sample_id"]) is None):
        raise HTTPException(404, f"sample {values['sample_id']} not found")
    for key, value in values.items():
        setattr(record, key, value)
    for field in payload.clear:
        if hasattr(record, field):
            setattr(record, field, None)
    record.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    session.add(record)
    session.commit()
    session.refresh(record)
    return _out(session, record)


@router.delete("/spectra/{spectrum_id}", status_code=204)
def delete_spectrum(spectrum_id: int, session: Session = Depends(get_session)):
    """Forget the record and its parsed points.  The original file stays (§0.2)."""
    record = _get(session, spectrum_id)
    for fit in session.exec(
            select(SpectrumFit).where(SpectrumFit.spectrum_id == spectrum_id)).all():
        session.delete(fit)
    storage.drop_spectrum_cache(spectrum_id)
    session.delete(record)
    session.commit()


# --------------------------------------------------------------------------
# fitting
# --------------------------------------------------------------------------
def _fit_out(session: Session, record: SpectrumRecord,
             fit: SpectrumFit) -> SpectrumFitOut:
    """A stored fit, with the labels and conductivities derived now.

    The numbers are frozen at fit time; the **names** are not.  Deriving them
    on read means a better label scheme reaches old fits, and -- more to the
    point -- a spectrum whose kind was corrected from liquid to solid shows the
    right names without refitting.  ``fit.kind`` is what the fit was reported
    under; the record's current kind is what the screen asks about, so both are
    sent and the screen can say when they disagree.
    """
    parameters = json.loads(fit.parameters_json) if fit.parameters_json else []
    thickness_cm, area = _geometry(session, record)
    arcs: list[dict] = []
    conductivity: dict = {}
    if parameters:
        stub = _FitStub(circuit=fit.circuit, parameters=[
            _ParameterStub(**p) for p in parameters])
        for meaning in label_arcs(stub, record.kind, record.cell_config):
            arcs.append({"parameter": meaning.parameter, "label": meaning.label,
                         "note": meaning.note, "value_ohm": meaning.value_ohm,
                         "determined": meaning.determined})
        if record.kind == SOLID:
            conductivity = ionic_conductivity(stub, thickness_cm=thickness_cm,
                                              area_cm2=area,
                                              config=record.cell_config)
        total = total_resistance(stub)
        if total is not None:
            conductivity.setdefault("total_ohm", total)
    return SpectrumFitOut(
        **fit.model_dump(exclude={"parameters_json"}),
        parameters=parameters,
        arcs=arcs,
        conductivity=conductivity,
        kind_now=record.kind,
    )


class _ParameterStub:
    """Enough of ``wrdkit.eis.Parameter`` for the labelling helpers.

    Rebuilding the real dataclass would mean re-deriving ``determined`` from a
    stored stderr, and the two definitions would drift.  The stored flag is the
    one the fit reported; that is the one to show.
    """

    def __init__(self, name: str, value: float, unit: str = "",
                 stderr: float | None = None, determined: bool = False,
                 **_ignored) -> None:
        self.name = name
        self.value = value
        self.unit = unit
        self.stderr = stderr
        self.determined = determined


class _FitStub:
    def __init__(self, circuit: str, parameters: list) -> None:
        self.circuit = circuit
        self.parameters = parameters


@router.post("/spectra/{spectrum_id}/fit", response_model=SpectrumFitOut,
             status_code=201)
def fit_spectrum(spectrum_id: int,
                 circuit: str = Query(None, description="비우면 그 종류의 기본 회로"),
                 drop_inductive: bool = Query(True),
                 frequency_low_hz: float | None = Query(None),
                 frequency_high_hz: float | None = Query(None),
                 restarts: int = Query(8, ge=0, le=64),
                 session: Session = Depends(get_session)):
    """Fit one circuit to one spectrum and keep the result."""
    return _run_fit(session, spectrum_id, circuit=circuit,
                    drop_inductive=drop_inductive,
                    frequency_low_hz=frequency_low_hz,
                    frequency_high_hz=frequency_high_hz, restarts=restarts)


def _run_fit(session: Session, spectrum_id: int, *, circuit: str | None,
             drop_inductive: bool = True, frequency_low_hz: float | None = None,
             frequency_high_hz: float | None = None,
             restarts: int = 8) -> SpectrumFitOut:
    """The work behind both fit endpoints.

    A plain function rather than one route calling the other: FastAPI fills a
    route's defaults from its ``Query`` objects only when the request goes
    through the router, so calling it directly hands the *Query objects
    themselves* to the fitter -- which fails somewhere far away, in the
    comparison of two frequencies.

    Failure is stored too.  A spectrum that will not fit is a finding about the
    cell or the circuit, and hiding it means the next person tries the same
    thing and waits for the same answer.
    """
    record = _get(session, spectrum_id)
    spectrum = storage.load_spectrum(spectrum_id)
    if spectrum is None:
        raise HTTPException(409, "이 스펙트럼의 파싱 결과가 없습니다")

    text = circuit or PRESETS[record.kind][0]["circuit"]
    window = None
    if frequency_low_hz is not None or frequency_high_hz is not None:
        window = (frequency_low_hz or 0.0,
                  frequency_high_hz or float(np.max(spectrum.frequency_hz)))

    try:
        from wrdkit.eis import fit_circuit
        from wrdkit.eis.circuit import CircuitError
    except ImportError as exc:                       # pragma: no cover
        raise HTTPException(503, str(exc)) from exc

    try:
        result = fit_circuit(spectrum, text, drop_inductive=drop_inductive,
                             frequency_range=window, restarts=restarts)
    except CircuitError as exc:
        raise HTTPException(422, f"회로를 읽지 못했습니다: {exc}") from exc

    used = result.frequency_hz
    fit = SpectrumFit(
        spectrum_id=spectrum_id,
        circuit=result.circuit,
        kind=record.kind,
        converged=result.converged,
        chi_squared=None if not np.isfinite(result.chi_squared)
        else float(result.chi_squared),
        reason=result.reason,
        parameters_json=json.dumps([
            {"name": p.name, "value": p.value, "unit": p.unit,
             "stderr": p.stderr, "determined": p.determined,
             "relative_error": p.relative_error}
            for p in result.parameters], ensure_ascii=False),
        dropped_inductive=result.dropped_inductive,
        dropped_out_of_range=result.dropped_out_of_range,
        frequency_low_hz=float(np.min(used)) if len(used) else None,
        frequency_high_hz=float(np.max(used)) if len(used) else None,
        starts=result.starts,
        starts_converged=result.starts_converged,
    )
    session.add(fit)
    record.last_circuit = result.circuit
    session.add(record)
    session.commit()
    session.refresh(fit)
    return _fit_out(session, record, fit)


@router.post("/fit-batch")
def fit_batch(spectrum_ids: list[int],
              circuit: str | None = Query(None),
              restarts: int = Query(8, ge=0, le=64),
              session: Session = Depends(get_session)):
    """Fit many spectra in one go -- the point of automating this at all.

    Each spectrum is reported separately, success or failure, because one that
    will not fit must not stop the other twenty.  The reply says how many did
    and how many did not; a caller that only counted the successes would read
    a half-failed batch as a small one.
    """
    if not spectrum_ids:
        raise HTTPException(422, "고른 스펙트럼이 없습니다")
    if len(spectrum_ids) > 200:
        raise HTTPException(422, "한 번에 200개까지만 맞춥니다")

    done, failed = [], []
    for spectrum_id in spectrum_ids:
        try:
            out = _run_fit(session, spectrum_id, circuit=circuit,
                           restarts=restarts)
        except HTTPException as exc:
            failed.append({"spectrum_id": spectrum_id, "detail": exc.detail})
            continue
        done.append(out)
    return {"fitted": done, "failed": failed,
            "requested": len(spectrum_ids),
            "converged": sum(1 for out in done if out.converged)}


@router.delete("/fits/{fit_id}", status_code=204)
def delete_fit(fit_id: int, session: Session = Depends(get_session)):
    fit = session.get(SpectrumFit, fit_id)
    if fit is None:
        raise HTTPException(404, f"fit {fit_id} not found")
    session.delete(fit)
    session.commit()
