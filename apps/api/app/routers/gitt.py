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

from wrdkit import WrdError, lttb_indices, read_wrd_bytes
from wrdkit.gitt import diffusion, pseudo_ocv, segment_pulses

from .. import storage
from ..db import get_session
from ..models import ExperimentGroup, GittRun, Sample
from ..schemas import (
    DiffusionOut,
    DiffusionPointOut,
    GittDashboardOut,
    GittDashboardRow,
    GittRunOut,
    GittRunUpdate,
    PocvOut,
    PocvPointOut,
    RawTraceOut,
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



def _group_names(session: Session, sample) -> tuple[int | None, str, str]:
    """(그룹 id, 그룹 이름, 상위 그룹 이름).

    셋을 함께 내는 이유는 화면이 이 한 줄로 두 가지를 하기 때문이다: 그룹·
    소그룹으로 거르기(id)와 "부모 · 자식" 으로 적기(이름 둘).  id 만 주면
    화면이 그룹 표를 한 번 더 물어야 하고, 이름만 주면 소그룹으로 거를 수
    없다 (ADR 0025).
    """
    group = sample.group
    if group is None:
        return None, "", ""
    parent = session.get(ExperimentGroup, group.parent_id) if group.parent_id else None
    return group.id, group.name, parent.name if parent else ""

def _missing(record: GittRun) -> list[str]:
    return [label for field, label in MATERIAL_FIELDS
            if not getattr(record, field) or getattr(record, field) <= 0]


def _out(record: GittRun, session: Session | None = None) -> GittRunOut:
    """한 줄로 내보낼 모양.  셀 이름은 붙어 있을 때만 채운다.

    id 만 보내면 화면이 이름을 얻으려고 셀을 한 번 더 물어야 하고, GITT 목록은
    한 줄에 한 번씩 그것을 하게 된다.
    """
    sample_name = None
    if session is not None and record.sample_id:
        sample = session.get(Sample, record.sample_id)
        sample_name = sample.name if sample else None
    return GittRunOut(**record.model_dump(), sample_name=sample_name,
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
              search: str | None = Query(None),
              sample_id: int | None = Query(None)):
    statement = select(GittRun)
    if sample_id is not None:
        statement = statement.where(GittRun.sample_id == sample_id)
    records = session.exec(statement.order_by(GittRun.uploaded_at.desc())).all()
    if search:
        needle = search.lower()
        records = [r for r in records
                   if needle in r.name.lower() or needle in r.original_name.lower()]
    return [_out(record, session) for record in records]


@router.post("/runs/upload", response_model=GittRunOut, status_code=201)
async def upload_run(file: UploadFile = File(...),
                     sample_id: int | None = Query(None, description="이 셀에 붙인다"),
                     purpose: str = Query("", description="무엇을 보려고 잰 측정인가"),
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

    if sample_id is not None and session.get(Sample, sample_id) is None:
        raise HTTPException(404, f"sample {sample_id} not found")

    digest = hashlib.sha256(content).hexdigest()
    existing = session.exec(select(GittRun).where(GittRun.sha256 == digest)).first()
    if existing is not None:
        # The recovery path.  Analysis re-parses the immutable original; when
        # that file is gone the screen says "다시 올려 주세요", and a dedup
        # that returned without storing made the advice a lie (#23).
        storage.store_upload(content, digest)
        # 같은 파일을 셀에 붙이려고 다시 올리는 일이 실제로 있다: 파일부터
        # 올려 두고 나중에 셀을 만드는 순서가 흔하기 때문이다.  이미 붙어
        # 있으면 조용히 옮기지 않는다 -- 남의 셀에서 떼어 오는 것이 된다.
        if sample_id is not None and existing.sample_id is None:
            existing.sample_id = sample_id
            session.add(existing)
        # 목적도 같다: 비어 있을 때만 채운다.  다시 올리면서 빈 칸을 두었다고
        # 먼저 적어 둔 것을 지우지 않는다.
        if purpose and not existing.purpose:
            existing.purpose = purpose
            session.add(existing)
        if session.dirty:
            session.commit()
            session.refresh(existing)
        return _out(existing, session)

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
        sample_id=sample_id,
        purpose=purpose.strip(),
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
    return _out(record, session)


@router.get("/runs/{gitt_id}", response_model=GittRunOut)
def read_run(gitt_id: int, session: Session = Depends(get_session)):
    return _out(_get(session, gitt_id), session)


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
    if values.get("sample_id") is not None \
            and session.get(Sample, values["sample_id"]) is None:
        # 없는 셀에 붙이면 목록에서 사라진 것처럼 보인다: 어느 셀 화면에도
        # 안 나오고, GITT 목록은 지워진 셀 이름을 못 찾아 빈칸을 그린다.
        raise HTTPException(404, f"sample {values['sample_id']} not found")
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
        # 비어 있음의 모양은 열마다 다르다: 숫자 열은 NULL 이지만 `purpose`
        # 는 NOT NULL 문자열이라 None 을 쓰면 IntegrityError 로 500 이 난다.
        # 지금 저장된 값의 종류로 정한다 -- 컬럼을 하나 더 나열하지 않는다.
        blank = "" if isinstance(getattr(record, field), str) else None
        setattr(record, field, blank)
    record.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    session.add(record)
    session.commit()
    session.refresh(record)
    return _out(record, session)


#: PATCH ``clear`` 가 비울 수 있는 필드 — 사람이 입력하는 재료 상수들이다.
CLEARABLE_GITT_FIELDS = {"purpose",
                         "molar_volume_cm3", "molar_mass_g", "active_mass_g",
                         "area_cm2",
                         # 셀에서 떼어내는 길.  붙이는 것과 달리 값이 `None`
                         # 이라 `sample_id: null` 로는 "안 보냄" 과 구별되지
                         # 않는다 -- 그래서 clear 를 쓴다.
                         "sample_id"}


@router.delete("/runs/{gitt_id}", status_code=204)
def delete_run(gitt_id: int, session: Session = Depends(get_session)):
    """Forget the record and its parse cache.  The original ``.wrd`` stays (§0.2)."""
    record = _get(session, gitt_id)
    others = session.exec(select(GittRun).where(GittRun.sha256 == record.sha256,
                                                GittRun.id != record.id)).first()
    if others is None:
        # 캐시는 원본 해시로 열리므로, 같은 바이트를 가리키는 행이 하나라도
        # 남아 있으면 지우지 않는다.
        storage.drop_gitt_cache(record.sha256)
    session.delete(record)
    session.commit()


# --------------------------------------------------------------------------
# 분석
# --------------------------------------------------------------------------
#: 원본 곡선 한 갈래에 보낼 점의 상한.  펄스 하나가 수천 점이라 그대로 보내면
#: 응답이 수 MB 가 되는데, 화면은 380 px 짜리 그래프다.  LTTB 는 봉우리와 골을
#: 남기고 줄이므로 (`wrdkit.downsample`), 펄스의 분극 폭이 죽지 않는다.
RAW_TRACE_POINTS = 2000


def _raw_out(trace) -> RawTraceOut:
    x = np.asarray(trace.capacity_mah, dtype=float)
    y = np.asarray(trace.voltage_v, dtype=float)
    if x.size > RAW_TRACE_POINTS:
        keep = lttb_indices(x, y, RAW_TRACE_POINTS)
        x, y = x[keep], y[keep]
    return RawTraceOut(capacity_mah=[float(v) for v in x],
                       voltage_v=[float(v) for v in y])


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
        charge_raw=_raw_out(curve.charge_raw),
        discharge_raw=_raw_out(curve.discharge_raw),
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


# --------------------------------------------------------------------------
# 대시보드 -- 셀 한 줄
# --------------------------------------------------------------------------
@router.get("/dashboard", response_model=GittDashboardOut)
def dashboard(session: Session = Depends(get_session)):
    """셀마다 한 줄: D 를 낼 수 있는가, 없다면 무엇이 없어서인가.

    확산계수의 **범위**를 주고 평균은 주지 않는다.  D 는 SOC 를 따라 자릿수로
    움직이므로 (ADR 0020), 한 숫자로 줄이면 그 숫자가 아무 SOC 도 뜻하지
    않는다 -- 최소와 최대는 적어도 둘 다 실제로 나온 값이다.

    D 를 세려면 기록을 실제로 계산해 봐야 한다.  펄스가 수백 개인 파일이
    여럿이면 무거워지므로, **재료 상수가 다 갖춰진 기록만** 계산한다: 없는
    것은 어차피 `None` 이 나오고, 없다는 사실은 파싱 없이도 안다.
    """
    records = session.exec(select(GittRun)).all()
    by_sample: dict[int, list[GittRun]] = {}
    #: 셀에 안 붙은 기록은 저마다 한 줄이다 (EIS 대시보드와 같은 규칙).
    loose: list[GittRun] = []
    for record in records:
        if record.sample_id is None:
            loose.append(record)
            continue
        by_sample.setdefault(record.sample_id, []).append(record)

    rows = []
    for sample_id, items in by_sample.items():
        sample = session.get(Sample, sample_id)
        if sample is None:
            # 셀이 지워졌는데 기록이 남아 있다 -- 갈 곳 없는 것은 마찬가지다.
            loose.extend(items)
            continue
        items = sorted(items, key=lambda r: (r.start_time or r.uploaded_at))

        missing: list[str] = []
        values: list[float] = []
        for record in items:
            gaps = _missing(record)
            for name in gaps:
                if name not in missing:
                    missing.append(name)
            if gaps:
                continue
            try:
                result = diffusion(
                    _load(record),
                    molar_volume_cm3=record.molar_volume_cm3,
                    molar_mass_g=record.molar_mass_g,
                    mass_g=record.active_mass_g,
                    area_cm2=record.area_cm2,
                    min_rest_s=record.min_rest_s,
                )
            except HTTPException:
                # 원본이 사라진 기록.  대시보드가 그 한 줄 때문에 통째로
                # 500 이 되면 나머지 셀도 못 본다.
                continue
            values.extend(p.d_cm2_s for p in result.usable if p.d_cm2_s)

        latest = items[-1]
        group_id, group_name, parent_name = _group_names(session, sample)
        rows.append(GittDashboardRow(
            sample_id=sample_id,
            sample_name=sample.name,
            name=latest.original_name or latest.name,
            gitt_id=latest.id,
            group_id=group_id,
            group_name=group_name,
            group_parent_name=parent_name,
            purposes=sorted({r.purpose for r in items if r.purpose}),
            owner=sample.created_by or "",
            records=len(items),
            pulses=sum(r.n_pulses for r in items),
            ready=sum(1 for r in items if not _missing(r)),
            missing=missing,
            diffusion_low=min(values) if values else None,
            diffusion_high=max(values) if values else None,
            measured_at=latest.start_time or latest.uploaded_at,
        ))

    # 안 붙은 기록도 줄로.  셀 칸이 비어 있다는 것 자체가 "이 파일에는 아직
    # 할 일이 있다" 이고, 수만 세면 그게 무엇인지는 다른 화면에 가야 안다.
    for record in sorted(loose, key=lambda r: (r.start_time or r.uploaded_at)):
        rows.append(GittDashboardRow(
            sample_id=None,
            sample_name="",
            name=record.original_name or record.name,
            gitt_id=record.id,
            attached=False,
            purposes=[record.purpose] if record.purpose else [],
            owner=record.created_by or "",
            records=1,
            pulses=record.n_pulses,
            ready=0 if _missing(record) else 1,
            missing=_missing(record),
            # D 는 계산하지 않는다.  붙지 않은 기록은 재료 상수가 비어 있는 것이
            # 보통이고, 그때 이 칸은 어차피 빈다 (§0.4).
            diffusion_low=None,
            diffusion_high=None,
            measured_at=record.start_time or record.uploaded_at,
        ))

    rows.sort(key=lambda r: (not r.attached, r.group_name, r.sample_name, r.name))
    return GittDashboardOut(rows=rows, unattached=len(loose))
