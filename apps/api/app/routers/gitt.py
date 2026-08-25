"""GITT: 펄스와 휴지에서 준평형 곡선과 확산계수를 뽑는다 (ADR 0020).

충방전과 같은 `.wrd` 를 읽지만 **다른 표**에 둔다.  GITT 파일을 사이클링처럼
요약하면 아무 뜻도 없는 사이클 수백 개가 나오고, 그것이 라이브러리에서 진짜
사이클 옆에 앉는다.  섹션도 따로다 — 충방전 도중 임피던스를 재는 일은 흔하지만
GITT 를 끼우는 일은 드물어서, 이어 붙일 이유가 없다.

재료 상수는 이 기록에 붙는다.  같은 분말도 셀이 다르면 계면 면적이 다르고,
확산계수는 그 제곱에 비례한다.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone

import numpy as np
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlmodel import Session, select

from wrdkit import WrdError, read_wrd_bytes
from wrdkit.gitt import diffusion, pseudo_ocv, segment_pulses

from .. import storage
from ..db import get_session
from ..models import GittRun
from ..schemas import (
    DiffusionOut,
    DiffusionPointOut,
    GittRunOut,
    GittRunUpdate,
    PocvOut,
    PocvPointOut,
)
from ..settings import settings

router = APIRouter(prefix="/api/gitt", tags=["gitt"])

#: 확산계수에 필요한, 파일에 없는 것들.  화면과 같은 말을 쓴다.
MATERIAL_FIELDS = (
    ("molar_volume_cm3", "몰부피 V_M"),
    ("molar_mass_g", "몰질량 M_B"),
    ("active_mass_g", "활물질 질량"),
    ("area_cm2", "계면 면적 S"),
)


def _get(session: Session, gitt_id: int) -> GittRun:
    record = session.get(GittRun, gitt_id)
    if record is None:
        raise HTTPException(404, f"gitt run {gitt_id} not found")
    return record


def _missing(record: GittRun) -> list[str]:
    return [label for field, label in MATERIAL_FIELDS
            if not getattr(record, field) or getattr(record, field) <= 0]


def _out(record: GittRun) -> GittRunOut:
    return GittRunOut(**record.model_dump(),
                      missing_for_diffusion=_missing(record))


def _pulse_note(blocks) -> str:
    """펄스와 휴지의 길이에 대한 한 줄.  **판정이 아니라 관찰이다.**

    사이클링 파일과 GITT 파일을 확실히 가르는 표식은 `.wrd` 안에 없다 — 둘 다
    충전·방전·휴지로 이루어져 있다.  펄스의 **개수**로는 갈리지 않는다:
    8사이클짜리 사이클링 파일에도 펄스가 열여섯 개다.

    갈리는 것은 **길이의 비**다.  GITT 는 짧게 밀고 길게 쉰다(분:시간), 사이클링은
    길게 밀고 잠깐 쉰다(시간:분).  휴지가 펄스보다 길지 않으면 그 기록에서
    "휴지 끝의 전압" 은 평형이 아니고, pOCV 라는 이름이 붙을 수 없다.

    그래도 거절하지는 않는다.  이 비가 애매한 프로토콜이 실재하고, 무엇을
    올렸는지는 올린 사람이 훨씬 잘 안다 (§0.4).
    """
    pulses = [block.duration_s for block in blocks
              if block.mode != "rest" and block.duration_s > 0]
    rests = [block.duration_s for block in blocks
             if block.mode == "rest" and block.duration_s > 0]
    if not pulses or not rests:
        return "휴지가 없습니다 — pOCV 는 휴지 끝의 전압에서 나옵니다"
    pulse = float(np.median(pulses))
    rest = float(np.median(rests))
    if rest <= pulse:
        return (f"휴지({_hms(rest)})가 펄스({_hms(pulse)})보다 길지 않습니다 — "
                "GITT 기록이 맞는지 확인해 주세요. 사이클링 파일이 대개 이런 "
                "모양입니다.")
    return ""


def _hms(seconds: float) -> str:
    if seconds >= 3600:
        return f"{seconds / 3600:.1f} h"
    if seconds >= 60:
        return f"{seconds / 60:.0f} min"
    return f"{seconds:.0f} s"


def _load(record: GittRun):
    wrd = storage.load_gitt(record.sha256)
    if wrd is None:
        raise HTTPException(
            409, f"{record.name}: 원본 파일을 읽지 못했습니다 — 다시 올려 주세요")
    return wrd


# --------------------------------------------------------------------------
# 목록과 올리기
# --------------------------------------------------------------------------
@router.get("/runs", response_model=list[GittRunOut])
def list_runs(session: Session = Depends(get_session),
              search: str | None = Query(None)):
    records = session.exec(
        select(GittRun).order_by(GittRun.uploaded_at.desc())).all()
    if search:
        needle = search.lower()
        records = [r for r in records
                   if needle in r.name.lower() or needle in r.original_name.lower()]
    return [_out(record) for record in records]


@router.post("/runs/upload", response_model=GittRunOut, status_code=201)
async def upload_run(file: UploadFile = File(...),
                     session: Session = Depends(get_session)):
    """Store one GITT ``.wrd`` and count what is in it.

    The same bytes twice is the same record.  Nothing is analysed here beyond
    the pulse count -- the material constants have to be typed in first, and
    the pOCV is cheap enough to compute per request.
    """
    if file.size is not None and file.size > settings.max_upload_bytes:
        raise HTTPException(413, f"file is {file.size / 1e6:.0f} MB; the limit is "
                                 f"{settings.max_upload_bytes / 1e6:.0f} MB")
    content = await file.read()
    if not content:
        raise HTTPException(422, "uploaded file is empty")

    digest = hashlib.sha256(content).hexdigest()
    existing = session.exec(select(GittRun).where(GittRun.sha256 == digest)).first()
    if existing is not None:
        # The recovery path.  Analysis re-parses the immutable original; when
        # that file is gone the screen says "다시 올려 주세요", and a dedup
        # that returned without storing made the advice a lie (#23).
        storage.store_upload(content, digest)
        return _out(existing)

    try:
        wrd = read_wrd_bytes(content, source_name=file.filename or "gitt.wrd")
    except WrdError as exc:
        raise HTTPException(422, f"could not read {file.filename!r}: {exc}") from exc

    blocks = segment_pulses(wrd)
    pulses = [block for block in blocks if block.mode != "rest"]
    if not pulses:
        raise HTTPException(
            422,
            f"{file.filename!r} 에는 전류가 흐른 구간이 없습니다 — "
            "휴지만 있는 기록으로는 아무것도 뽑을 수 없습니다")

    storage.store_upload(content, digest)
    seconds = wrd.seconds("test_time")
    record = GittRun(
        name=(file.filename or "gitt").rsplit(".", 1)[0],
        original_name=file.filename or "",
        sha256=digest,
        size_bytes=len(content),
        n_points=len(wrd),
        n_pulses=len(pulses),
        duration_h=float(seconds[-1] - seconds[0]) / 3600.0 if len(wrd) else None,
        start_time=wrd.metadata.start_time,
        pulse_note=_pulse_note(blocks),
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    return _out(record)


@router.get("/runs/{gitt_id}", response_model=GittRunOut)
def read_run(gitt_id: int, session: Session = Depends(get_session)):
    return _out(_get(session, gitt_id))


@router.patch("/runs/{gitt_id}", response_model=GittRunOut)
def update_run(gitt_id: int, payload: GittRunUpdate,
               session: Session = Depends(get_session)):
    record = _get(session, gitt_id)
    values = payload.model_dump(exclude_unset=True, exclude={"clear"})
    if "name" in values:
        name = (values["name"] or "").strip()
        if not name:
            raise HTTPException(422, "gitt run name cannot be empty")
        values["name"] = name
    for key, value in values.items():
        setattr(record, key, value)
    for field in payload.clear:
        # 재료 상수만 — duration/start_time 같은 파일 유래 값은 사실이라
        # 지울 수 없다 (리뷰 #24).
        if field not in CLEARABLE_GITT_FIELDS:
            raise HTTPException(
                422, f"{field!r} 은 비울 수 없습니다 — 계측기 파일에서 온 "
                     f"값입니다 (비울 수 있는 것: "
                     f"{', '.join(sorted(CLEARABLE_GITT_FIELDS))})")
        setattr(record, field, None)
    record.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    session.add(record)
    session.commit()
    session.refresh(record)
    return _out(record)


#: PATCH ``clear`` 가 비울 수 있는 필드 — 사람이 입력하는 재료 상수들이다.
CLEARABLE_GITT_FIELDS = {"molar_volume_cm3", "molar_mass_g", "active_mass_g",
                         "area_cm2"}


@router.delete("/runs/{gitt_id}", status_code=204)
def delete_run(gitt_id: int, session: Session = Depends(get_session)):
    """Forget the record.  The original ``.wrd`` stays (§0.2)."""
    record = _get(session, gitt_id)
    session.delete(record)
    session.commit()


# --------------------------------------------------------------------------
# 분석
# --------------------------------------------------------------------------
@router.get("/runs/{gitt_id}/pocv", response_model=PocvOut)
def run_pocv(gitt_id: int, session: Session = Depends(get_session)):
    """준평형 전압 곡선 — 재료 상수 없이 나온다.

    확산계수와 나란히 두지만 비어 있는 이유가 다르다: 이쪽은 파일만 있으면
    되고, 저쪽은 사람이 넣어야 하는 값이 넷이다.
    """
    record = _get(session, gitt_id)
    curve = pseudo_ocv(_load(record), min_rest_s=record.min_rest_s)
    return PocvOut(
        gitt_id=gitt_id,
        charge=[PocvPointOut(**{k: getattr(point, k) for k in
                                ("capacity_mah", "voltage_v", "rest_s", "drift_mv")})
                for point in curve.charge],
        discharge=[PocvPointOut(**{k: getattr(point, k) for k in
                                   ("capacity_mah", "voltage_v", "rest_s", "drift_mv")})
                   for point in curve.discharge],
        skipped_charge=curve.skipped_charge,
        skipped_discharge=curve.skipped_discharge,
        # 같은 문장이 스무 번 반복되면 읽히지 않는다.
        skipped_reasons=sorted(set(curve.skipped_reasons)),
    )


@router.get("/runs/{gitt_id}/diffusion", response_model=DiffusionOut)
def run_diffusion(gitt_id: int, session: Session = Depends(get_session)):
    """펄스마다의 확산계수 — 가정을 검사한 뒤에만 숫자가 나온다 (ADR 0020)."""
    record = _get(session, gitt_id)
    result = diffusion(
        _load(record),
        molar_volume_cm3=record.molar_volume_cm3,
        molar_mass_g=record.molar_mass_g,
        mass_g=record.active_mass_g,
        area_cm2=record.area_cm2,
        min_rest_s=record.min_rest_s,
    )
    points = [DiffusionPointOut(
        capacity_mah=point.capacity_mah, voltage_v=point.voltage_v,
        d_cm2_s=point.d_cm2_s, delta_es_v=point.delta_es_v,
        delta_et_v=point.delta_et_v, pulse_s=point.pulse_s,
        sqrt_t_r_squared=point.sqrt_t_r_squared, reason=point.reason,
        rest_s=point.rest_s, drift_mv=point.drift_mv)
        for point in result.points]
    return DiffusionOut(
        gitt_id=gitt_id,
        points=points,
        missing=result.missing,
        molar_volume_cm3=result.molar_volume_cm3,
        molar_mass_g=result.molar_mass_g,
        mass_g=result.mass_g,
        area_cm2=result.area_cm2,
        usable=len(result.usable),
        total=len(points),
    )
