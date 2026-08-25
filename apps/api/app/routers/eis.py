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
import re
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
from wrdkit.eis.biologic import read_mpr_sweeps, read_mpt_sweeps
from wrdkit.eis.circuit import CircuitError, parse_circuit
from wrdkit.eis.derive import CONFIGS, FULL, HALF, SYMMETRIC

from .. import storage
from ..db import get_session
from ..models import Sample, SpectrumFit, SpectrumRecord
from ..schemas import (
    DrtOut,
    DrtPeakOut,
    DrtSweepOut,
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

#: 무엇을 쟀는지가 **어떤 회로를 기본으로 줄지**까지 정한다.
#:
#: 전해질 종류만으로는 부족하다.  같은 액체 전해질이라도 리튬 대극을 쓴
#: 하프셀은 대극의 계면이 아크를 하나 더 얹고, 대칭셀은 같은 전극이 둘이라
#: 아크가 두 배로 나온다 (한쪽 값은 절반이다).  풀셀은 두 전극이 겹쳐 보여
#: 분리가 안 된다.  아크의 *이름*은 이미 이 구분을 따르므로(ADR 0019,
#: derive.BY_CONFIG), 회로도 같은 축에 놓는다.
#:
#: 여기 없는 조합은 종류별 기본(``PRESETS``)으로 떨어진다.
PRESETS_BY_CONFIG: dict[tuple[str, str], list[dict]] = {
    (LIQUID, HALF): [
        {"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)-W3",
         "label": "대극 계면 + 전하이동 + 확산",
         "note": "리튬 대극 하프셀. 고주파 아크는 대개 리튬 표면 필름, "
                 "저주파 아크가 작동전극의 전하이동, 끝의 45° 가 확산."},
        {"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)-Ws3",
         "label": "확산이 유한할 때 (Ws)",
         "note": "저주파에서 45° 직선이 꺾여 반원으로 닫히면 유한 확산이다."},
        {"circuit": "R0-p(R1,CPE1)-W2",
         "label": "아크 하나 + 확산",
         "note": "대극 아크와 작동전극 아크가 겹쳐 하나로 보일 때."},
    ],
    (LIQUID, FULL): [
        {"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)-W3",
         "label": "SEI + 전하이동 + 확산",
         "note": "풀셀은 두 전극이 함께 보인다 — 어느 쪽 아크인지는 이 "
                 "측정만으로 못 가른다."},
        {"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)",
         "label": "두 아크 (절차서 기본)",
         "note": "확산 꼬리가 안 보이거나 저주파를 안 잰 경우."},
        {"circuit": "R0-p(R1,CPE1)",
         "label": "한 아크",
         "note": "반원이 하나만 보일 때."},
    ],
    (LIQUID, SYMMETRIC): [
        {"circuit": "R0-p(R1,CPE1)-W2",
         "label": "대칭셀 — 한 아크 + 확산",
         "note": "같은 전극이 둘이라 아크는 두 전극의 합이다. "
                 "한쪽 전극 값은 절반으로 본다."},
        {"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)",
         "label": "두 아크",
         "note": "필름과 전하이동이 갈려 보일 때. 역시 한쪽은 절반이다."},
    ],
    (SOLID, SYMMETRIC): PRESETS[SOLID],
    (SOLID, FULL): [
        {"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)-W3",
         "label": "전해질 + 계면 + 확산",
         "note": "전고체 풀셀. 저주파 아크는 전극/전해질 계면이 지배하고, "
                 "벌크와 입계는 대개 하나로 합쳐 보인다."},
        {"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)",
         "label": "전해질 + 계면",
         "note": "확산 꼬리가 안 보일 때."},
    ],
    (SOLID, HALF): [
        {"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)-W3",
         "label": "전해질 + 작동전극 계면 + 확산",
         "note": "전고체 하프셀. 상대 전극(리튬/인듐) 계면이 아크를 더할 수 "
                 "있어 아크 수가 늘기도 한다."},
        {"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)-CPE3",
         "label": "블로킹 꼬리로 끝날 때",
         "note": "저주파가 45° 가 아니라 수직으로 서면 확산이 아니라 블로킹이다."},
    ],
}


def presets_for(kind: str, config: str = "") -> list[dict]:
    """The circuits to offer for this measurement, most likely first."""
    return PRESETS_BY_CONFIG.get((kind, config)) or PRESETS[kind]


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


def _out(session: Session, record: SpectrumRecord, *,
         duplicate: bool = False) -> SpectrumOut:
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
        duplicate=duplicate,
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
    kind_label = {LIQUID: "액체 전해질", SOLID: "전고체"}
    config_label = {SYMMETRIC: "대칭셀", FULL: "풀셀", HALF: "하프셀"}
    return {
        "kinds": [{"kind": kind, "label": kind_label[kind],
                   "presets": PRESETS[kind]} for kind in KINDS],
        # 여섯 조합 — 화면의 드롭박스 하나가 이것을 그대로 쓴다.  아크의
        # 이름과 회로가 같은 축에서 갈리므로, 고르는 것도 한 번이어야 한다.
        "combinations": [
            {"kind": kind, "cell_config": config,
             "label": f"{kind_label[kind]} · {config_label[config]}",
             "presets": presets_for(kind, config)}
            for kind in KINDS for config in CELL_CONFIGS
        ],
    }


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
    # 사이클 번호가 있으면 그 순서가 사람이 보고 싶은 순서다 — 올린 순서는
    # 누가 파일을 어떤 순으로 끌어다 놓았느냐일 뿐이다.  번호 없는 것은 뒤로.
    records = sorted(records, key=lambda r: (r.at_cycle is None,
                                             r.at_cycle if r.at_cycle is not None else 0,
                                             r.uploaded_at))
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


def _load_points(record: SpectrumRecord):
    """This spectrum's points -- from the cache, or rebuilt from the original.

    The cache is verified against the record's hash (a swapped or stale file
    under the right id returned another cell's impedance, review #12), and a
    missing or wrong cache is not the user's problem while the immutable
    original is still on disk: it is re-parsed and re-cached here.  Only when
    the original is gone too does this ask for a re-upload -- and the upload
    path restores originals even for known hashes, so that advice now works.
    """
    spectrum = storage.load_spectrum(record.id, record.sha256)
    if spectrum is not None:
        return spectrum
    path = storage.spectrum_upload_path(record.sha256, record.source_format)
    try:
        content = path.read_bytes()
    except OSError:
        raise HTTPException(
            409, f"{record.name}: 파싱 결과도 원본도 없습니다 — "
                 f"파일을 다시 올려 주세요") from None
    if hashlib.sha256(content).hexdigest() != record.sha256:
        raise HTTPException(
            409, f"{record.name}: 저장된 원본이 기록과 다릅니다 — "
                 f"파일을 다시 올려 주세요")
    try:
        spectrum, _ = _parse(content, record.original_name or record.name)
    except HTTPException:
        raise
    except (UnknownColumn, ValueError) as exc:
        raise HTTPException(409, f"{record.name}: 원본을 다시 읽지 못했습니다 "
                                 f"— {exc}") from exc
    storage.cache_spectrum(record.id, spectrum, record.sha256)
    return spectrum


@router.get("/points", response_model=list[SpectrumPointsOut])
def many_points(ids: str = Query(..., description="쉼표로 구분한 스펙트럼 id"),
                session: Session = Depends(get_session)):
    """여러 스펙트럼의 점을 한 번에.

    나이퀴스트를 겹쳐 그리려면 두세 개가 동시에 필요하고, 하나씩 부르면 화면이
    부분적으로 채워지며 축이 두 번 다시 잡힌다.  못 읽은 것은 **조용히 빠지지
    않고** 그 자리에서 404 로 말한다 — 곡선 하나가 없는 그림은 있는 그림과
    구분되지 않는다.
    """
    wanted = []
    for chunk in ids.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if not chunk.lstrip("-").isdigit():
            raise HTTPException(422, f"스펙트럼 id 가 아닙니다: {chunk!r}")
        wanted.append(int(chunk))
    if not wanted:
        raise HTTPException(422, "고른 스펙트럼이 없습니다")
    if len(wanted) > 12:
        raise HTTPException(422, "한 번에 12개까지만 겹쳐 그립니다")

    out = []
    for spectrum_id in wanted:
        record = _get(session, spectrum_id)
        out.append(_points_out(record, _load_points(record)))
    return out


def _points_out(record: SpectrumRecord, spectrum) -> SpectrumPointsOut:
    return SpectrumPointsOut(
        id=record.id,
        name=record.name,
        kind=record.kind,
        at_cycle=record.at_cycle,
        frequency_hz=[float(v) for v in spectrum.frequency_hz],
        z_re=[float(v) for v in spectrum.z_re],
        z_im=[float(v) for v in spectrum.z_im],
        magnitude=[float(v) for v in spectrum.magnitude],
        phase_deg=[float(v) for v in spectrum.phase_deg],
    )


@router.get("/spectra/{spectrum_id}/points", response_model=SpectrumPointsOut)
def spectrum_points(spectrum_id: int, session: Session = Depends(get_session)):
    """The measured points, raw ohms and hertz (ADR 0001)."""
    record = _get(session, spectrum_id)
    return _points_out(record, _load_points(record))


# --------------------------------------------------------------------------
# writing
# --------------------------------------------------------------------------
def _parse_sweeps(content: bytes, filename: str):
    """Every impedance sweep in the upload, by content not by name (ADR 0022)."""
    if content[:22] == b"BIO-LOGIC MODULAR FILE":
        return read_mpr_sweeps(content), "mpr"
    text = content.decode("latin-1", errors="replace")
    if "Nb header lines" in text:
        return read_mpt_sweeps(text), "mpt"
    raise HTTPException(
        422,
        f"{filename!r} 은 BioLogic .mpr 도 EC-Lab .mpt 도 아닙니다 — "
        "EC-Lab 에서 저장한 원본이나 텍스트 내보내기를 올려 주세요")


def _parse(content: bytes, filename: str) -> tuple[Spectrum, str]:
    """The single sweep in an upload -- used by the cache-repair path."""
    if content[:22] == b"BIO-LOGIC MODULAR FILE":
        return read_mpr_bytes(content), "mpr"
    text = content.decode("latin-1", errors="replace")
    if "Nb header lines" in text:
        return read_mpt_text(text), "mpt"
    raise HTTPException(
        422,
        f"{filename!r} 은 BioLogic .mpr 도 EC-Lab .mpt 도 아닙니다 — "
        "EC-Lab 에서 저장한 원본이나 텍스트 내보내기를 올려 주세요")


def _normalised_stem(filename: str) -> str:
    """The experiment name a file belongs to: extension off, channel off.

    EC-Lab appends ``_C01`` to the data files of an experiment and not to its
    ``.mps`` -- `A_C01.mpr` pairs with `A.mps`.
    """
    stem = re.sub(r"\.[^.]+$", "", filename or "")
    return re.sub(r"_C\d+$", "", stem, flags=re.IGNORECASE)


def _check_settings_stem(data_name: str | None, settings_name: str | None) -> None:
    """Refuse a settings file that names a different experiment.

    The client pairs by name too, but it once had a "one of each -- just
    attach it" fallback that stored another experiment's amplitude and device
    as this measurement's conditions (review #13).  The server cannot know
    which pairing the client intended, but it can see the names disagree.
    """
    if not data_name or not settings_name:
        return
    data_stem = _normalised_stem(data_name)
    settings_stem = _normalised_stem(settings_name)
    if data_stem and settings_stem and data_stem != settings_stem:
        raise HTTPException(
            422,
            f"설정 파일 {settings_name!r} 은 {data_name!r} 의 짝이 아닙니다 — "
            f"실험 이름이 다릅니다 ({settings_stem!r} ≠ {data_stem!r})")


@router.post("/spectra/upload", response_model=SpectrumOut, status_code=201)
async def upload_spectrum(
    file: UploadFile = File(...),
    settings_file: UploadFile | None = File(None),
    sample_id: int | None = Query(None),
    kind: str = Query(LIQUID),
    cell_config: str = Query(""),
    at_cycle: int | None = Query(None, ge=0),
    purpose: str = Query("", description="무엇을 보려고 잰 측정인가 (자유 입력)"),
    session: Session = Depends(get_session),
):
    """Store one ``.mpr`` or ``.mpt``, with its ``.mps`` when there is one.

    The same bytes twice is the same spectrum, as with cycling files: the same
    measurement reaches us from the instrument PC and from somebody's laptop.
    """
    _validate_kind(kind)
    _validate_config(cell_config)
    # PATCH 는 확인하는데 업로드는 안 하고 있었다.  없는 셀 번호로 올리면
    # 스펙트럼이 아무 데도 안 붙은 채 조용히 저장되고, 셀 화면에서는 영영
    # 안 보인다 -- 붙였다고 생각한 사람에게는 사라진 것과 같다.
    if sample_id is not None and session.get(Sample, sample_id) is None:
        raise HTTPException(404, f"sample {sample_id} not found")
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
        # Re-uploading known bytes is also the recovery path: the screen says
        # "올려 주세요" when the original or the cache is gone, and a dedup
        # that returns before storing anything made that advice a lie (#23).
        storage.store_bytes(content, storage.spectrum_upload_path(
            digest, existing.source_format))
        if storage.load_spectrum(existing.id, existing.sha256) is None:
            try:
                spectrum, _ = _parse(content, file.filename or "upload")
                storage.cache_spectrum(existing.id, spectrum, existing.sha256)
            except (HTTPException, UnknownColumn, ValueError):
                pass          # the read paths will say what is wrong
        # Blank fields the first upload did not carry may be filled by a
        # later one -- filled ones are never overwritten (§0.3 spirit).
        # ``kind`` stays as it is: its default is a real value, so a repeat
        # upload cannot tell "chose liquid" from "did not choose" (#22).
        changed = False
        if sample_id is not None and existing.sample_id is None:
            existing.sample_id = sample_id
            changed = True
        if cell_config and not existing.cell_config:
            existing.cell_config = cell_config
            changed = True
        if at_cycle is not None and existing.at_cycle is None:
            existing.at_cycle = at_cycle
            changed = True
        if purpose and not existing.purpose:
            existing.purpose = purpose
            changed = True
        if settings_file is not None and not existing.settings_json:
            _check_settings_stem(file.filename, settings_file.filename)
            raw = await settings_file.read()
            if raw:
                existing.settings_sha256 = hashlib.sha256(raw).hexdigest()
                existing.settings_name = settings_file.filename or ""
                storage.store_bytes(raw, storage.spectrum_upload_path(
                    existing.settings_sha256, "mps"))
                changed = True
                try:
                    meta = read_mps_text(raw.decode("latin-1", errors="replace"))
                except ValueError:
                    meta = {}
                if meta:
                    existing.settings_json = json.dumps(meta, ensure_ascii=False)
                    if existing.amplitude_mv is None:
                        existing.amplitude_mv = _float(meta.get("amplitude_mv"))
                    if not existing.device:
                        existing.device = str(meta.get("Device", ""))
                    if not existing.technique:
                        existing.technique = str(meta.get("technique", ""))
        if changed:
            session.add(existing)
            session.commit()
            session.refresh(existing)
        return _out(session, existing, duplicate=True)

    try:
        sweeps, source_format = _parse_sweeps(content, file.filename or "upload")
    except UnknownColumn as exc:
        raise HTTPException(422, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(422, f"could not read {file.filename!r}: {exc}") from exc
    if not sweeps:
        raise HTTPException(422, f"{file.filename!r} 에 임피던스 스윕이 없습니다")

    meta: dict = {}
    settings_sha = ""
    settings_name = ""
    if settings_file is not None:
        _check_settings_stem(file.filename, settings_file.filename)
        raw = await settings_file.read()
        if raw:
            # 원문 보존이 먼저다 (§0.2 정신, 리뷰 #21).  settings_json 은
            # 파서가 이해한 부분집합이고, 파서가 모르는 줄은 원문 바이트에서만
            # 되찾는다.
            settings_sha = hashlib.sha256(raw).hexdigest()
            settings_name = settings_file.filename or ""
            storage.store_bytes(raw, storage.spectrum_upload_path(settings_sha,
                                                                  "mps"))
            try:
                meta = read_mps_text(raw.decode("latin-1", errors="replace"))
            except ValueError:
                meta = {}

    storage.store_bytes(content,
                        storage.spectrum_upload_path(digest, source_format))

    stem = (file.filename or "spectrum").rsplit(".", 1)[0]
    # 파일이 스스로 말하는 것은 묻지 않는다 (§0.3).  스윕이 여럿이고 용량이
    # 스윕마다 다르면 그것이 SOC 스캔이라는 뜻이다.
    measured_purpose = purpose
    if not measured_purpose and len(sweeps) > 1:
        # 용량이 먼저다.  용량 컬럼이 없는 내보내기도 있어서, 그때는 전위가
        # SOC 의 대리값이다 -- 같은 SOC 를 온도만 바꿔 잰 파일은 둘 다
        # 안 움직이므로 목적을 지어내지 않는다 (§0.4).
        for values, floor in ((
                [sw.capacity_mah for sw in sweeps if sw.capacity_mah is not None], 1e-6),
                ([sw.potential_v for sw in sweeps if sw.potential_v is not None], 0.01)):
            if len(values) > 1 and max(values) - min(values) > floor:
                measured_purpose = "SOC별"
                break

    created: list[SpectrumRecord] = []
    for sweep in sweeps:
        spectrum = sweep.spectrum
        record = SpectrumRecord(
            sample_id=sample_id,
            # 스윕이 여럿이면 이름으로 구별돼야 한다 -- 같은 파일에서 나온
            # 21개가 전부 같은 이름이면 목록에서 고를 수가 없다.
            name=stem if len(sweeps) == 1 else f"{stem} #{sweep.index}",
            kind=kind,
            cell_config=cell_config,
            at_cycle=at_cycle,
            purpose=measured_purpose,
            sweep_index=sweep.index,
            sweep_count=len(sweeps),
            potential_v=sweep.potential_v,
            capacity_mah=sweep.capacity_mah,
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
            settings_sha256=settings_sha,
            settings_name=settings_name,
        )
        session.add(record)
        created.append(record)
    session.commit()
    for record, sweep in zip(created, sweeps, strict=True):
        session.refresh(record)
        storage.cache_spectrum(record.id, sweep.spectrum, record.sha256)
    return _out(session, created[0])


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
        # 사람이 넣은 것만 비울 수 있다.  hasattr 전체를 열어 두면 주파수
        # 범위·측정 시각 같은 **계측기가 준** 값까지 지워지는데(리뷰 #24),
        # 그것은 파일에서 온 사실이라 지우면 재업로드 dedup 로도 안 돌아온다.
        if field not in CLEARABLE_SPECTRUM_FIELDS:
            raise HTTPException(
                422, f"{field!r} 은 비울 수 없습니다 — 계측기 파일에서 온 "
                     f"값입니다 (비울 수 있는 것: "
                     f"{', '.join(sorted(CLEARABLE_SPECTRUM_FIELDS))})")
        setattr(record, field, None)
    record.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    session.add(record)
    session.commit()
    session.refresh(record)
    return _out(session, record)


#: PATCH ``clear`` 가 비울 수 있는 필드 — 전부 사람이 입력하는 것들이다.
CLEARABLE_SPECTRUM_FIELDS = {"sample_id", "at_cycle", "thickness_um",
                             "area_cm2", "measured_at"}


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
    fitted_frequency: list[float] | None = None
    fitted_re: list[float] | None = None
    fitted_im: list[float] | None = None
    fitted_note = ""
    if parameters:
        # The curve the parameters mean, evaluated by the same AST that fitted
        # them.  The screen used to rebuild it from the parameter names and
        # silently drew a different curve for any circuit with L, Ws, Wo or
        # nesting (review #6); now the server is the only evaluator.
        try:
            model = parse_circuit(fit.circuit)
            spectrum = storage.load_spectrum(record.id, record.sha256)
            if spectrum is not None:
                # By name, not position: the stored list is re-ordered so the
                # high-frequency arc comes first, which is not always the
                # circuit's own parameter order.
                by_name = {p["name"]: float(p["value"]) for p in parameters}
                values = np.array([by_name[name]
                                   for name in model.parameter_names])
                z = model.impedance(values, spectrum.frequency_hz)
                fitted_frequency = [float(v) for v in spectrum.frequency_hz]
                fitted_re = [float(v) for v in z.real]
                fitted_im = [float(v) for v in z.imag]
            else:
                fitted_note = "파싱 결과가 없어 곡선을 계산하지 못했습니다"
        except (CircuitError, KeyError) as exc:
            fitted_note = f"회로를 읽지 못해 곡선이 없습니다: {exc}"
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
        fitted_frequency_hz=fitted_frequency,
        fitted_z_re=fitted_re,
        fitted_z_im=fitted_im,
        fitted_note=fitted_note,
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
    spectrum = _load_points(record)

    text = circuit or presets_for(record.kind, record.cell_config)[0]["circuit"]
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
        except Exception as exc:  # noqa: BLE001
            # 하나의 예기치 못한 예외가 나머지 스물을 세우면 안 된다 — 이
            # 함수의 존재 이유가 그것이다 (리뷰 A6).  무엇이었는지는 남긴다.
            failed.append({"spectrum_id": spectrum_id,
                           "detail": f"{type(exc).__name__}: {exc}"})
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


# --------------------------------------------------------------------------
# DRT
# --------------------------------------------------------------------------
def _drt_out(spectrum_id: int, result) -> DrtOut:
    return DrtOut(
        spectrum_id=spectrum_id,
        regularisation=result.regularisation,
        derivative_order=result.derivative_order,
        tau_s=[float(v) for v in result.tau_s],
        gamma_ohm=[float(v) for v in result.gamma_ohm],
        r_inf_ohm=result.r_inf_ohm,
        inductance_h=result.inductance_h,
        chi_squared=result.chi_squared,
        residual_norm=result.residual_norm,
        penalty_norm=result.penalty_norm,
        peaks=[DrtPeakOut(**vars(peak)) for peak in result.peaks],
        total_polarisation_ohm=result.total_polarisation_ohm,
        dropped_inductive=result.dropped_inductive,
    )


def _drt_module():
    try:
        from wrdkit.eis import drt as module
    except ImportError as exc:                       # pragma: no cover
        raise HTTPException(503, str(exc)) from exc
    return module


@router.get("/spectra/{spectrum_id}/drt", response_model=DrtOut)
def spectrum_drt(spectrum_id: int,
                 regularisation: float = Query(1e-3, gt=0),
                 derivative_order: int = Query(1, ge=0, le=2),
                 drop_inductive: bool = Query(True),
                 session: Session = Depends(get_session)):
    """이완 시간 분포 하나 — 주어진 λ 에서.

    저장하지 않는다.  피팅과 달리 DRT 는 같은 입력에 같은 답을 주고(볼록 문제),
    수십 밀리초면 끝난다.  저장하면 λ 를 바꿔 볼 때마다 행이 쌓이는데, λ 를
    바꿔 보는 것이 이 화면에서 하는 일의 전부다.
    """
    record = _get(session, spectrum_id)
    spectrum = _load_points(record)
    module = _drt_module()
    try:
        result = module.drt(spectrum, regularisation=regularisation,
                            derivative_order=derivative_order,
                            drop_inductive=drop_inductive)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    return _drt_out(spectrum_id, result)


@router.get("/spectra/{spectrum_id}/drt/sweep", response_model=DrtSweepOut)
def spectrum_drt_sweep(spectrum_id: int,
                       derivative_order: int = Query(1, ge=0, le=2),
                       drop_inductive: bool = Query(True),
                       session: Session = Depends(get_session)):
    """λ 를 여섯 자리에 걸쳐 훑고, L 곡선 모서리를 이유와 함께 짚는다.

    고르는 것이 아니라 **보여 주는** 것이다 (ADR 0005 와 같은 태도): 양 끝의
    실패 모드 -- 잡음 봉우리의 숲과 하나로 뭉친 덩어리 -- 가 함께 보여야 가운데가
    선택으로 읽힌다.  모서리가 없으면 없다고 말한다.
    """
    record = _get(session, spectrum_id)
    spectrum = _load_points(record)
    module = _drt_module()
    results = module.sweep(spectrum, derivative_order=derivative_order,
                           drop_inductive=drop_inductive)
    if not results:
        raise HTTPException(422, "이 스펙트럼으로는 DRT 를 풀지 못했습니다")
    index, reason = module.lcurve_corner(results)
    return DrtSweepOut(
        spectrum_id=spectrum_id,
        results=[_drt_out(spectrum_id, result) for result in results],
        suggested_index=index,
        suggested_reason=reason,
    )
