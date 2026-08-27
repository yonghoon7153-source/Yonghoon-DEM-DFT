"""Shared route helpers."""

from __future__ import annotations

import math

from fastapi import HTTPException
from sqlmodel import Session, select

from wrdkit import BASES, ResolvedCell, basis_label

from .models import ExperimentGroup, Run, Sample
from .schemas import ComponentOut, ResolvedCellOut


def circle_cm2(diameter_mm: float) -> float:
    """원형 펠릿의 면적 (cm²).  지름은 mm 로 받는다 -- 캘리퍼가 그렇게 읽는다.

    EIS(전도도의 분모)와 GITT(확산계수의 계면 면적)가 같은 원을 잰다.  두 벌로
    두면 한쪽만 고쳐지고, 그러면 같은 셀의 두 화면이 다른 면적을 말한다.
    """
    return float(math.pi * (diameter_mm / 20.0) ** 2)


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


def group_scope(session: Session, group_id: int) -> list[int]:
    """The group ids a filter on ``group_id`` should actually match.

    A cell sits in exactly one node, so a parent group holds no cells of its
    own once its cells have been sorted into sub-groups -- filtering by the
    parent alone would show an empty list for a group that plainly has cells
    in it.  Every count and every filter goes through here so the number on a
    dropdown always matches what selecting it shows.

    Nesting is one level deep (ADR 0025), so this is the parent and its
    children -- no recursion, and no cycle to guard against.
    """
    children = session.exec(
        select(ExperimentGroup.id).where(ExperimentGroup.parent_id == group_id)
    ).all()
    return [group_id, *[int(c) for c in children]]


#: 측정이 스스로 가질 수 있는 조건들 (ADR 0027).  이름이 셀 쪽과 같아서
#: 물려받는 규칙이 한 줄로 끝난다.
MEASUREMENT_CONDITIONS = ("group_id", "test_date", "cathode_type", "process",
                          "temperature_c")


def resolve_conditions(session: Session, record) -> dict:
    """이 측정에 실제로 쓰이는 조건과, 그중 무엇을 셀에서 빌려 왔는지.

    규칙 하나: **적어 넣은 값이 이긴다.**  비어 있는 칸만 붙은 셀에서 가져온다
    (`thickness_um`/`area_cm2` 가 이미 그렇게 산다).  같은 셀의 임피던스를 다른
    온도에서 재는 일이 실제로 있고, 그때 셀의 온도는 이 측정의 온도가 아니다.

    빌려 온 칸의 이름을 함께 내는 이유는 화면이 그것을 **회색으로** 그려야
    하기 때문이다.  물려받은 값과 적어 넣은 값이 같은 검정으로 보이면, 셀을
    고쳤을 때 왜 이 측정의 표시가 따라 바뀌는지 알 수 없다 (§0.4).
    """
    sample = None
    if getattr(record, "sample_id", None):
        sample = session.get(Sample, record.sample_id)

    out: dict = {}
    inherited: list[str] = []
    for field in MEASUREMENT_CONDITIONS:
        own = getattr(record, field, None)
        blank = own is None or own == ""
        value = own
        if blank and sample is not None:
            borrowed = getattr(sample, field, None)
            if borrowed is not None and borrowed != "":
                value = borrowed
                inherited.append(field)
        out[f"{field}_effective"] = value
    # 숫자 열의 "없음" 은 빈 문자열이 아니라 None 이다.
    if out.get("temperature_c_effective") == "":
        out["temperature_c_effective"] = None
    out["inherited"] = inherited

    group_id = out.get("group_id_effective")
    group = session.get(ExperimentGroup, group_id) if group_id else None
    if group is None:
        out["group_label"] = ""
        out["group_name_effective"] = ""
        out["group_parent_name_effective"] = ""
    else:
        parent = (session.get(ExperimentGroup, group.parent_id)
                  if group.parent_id else None)
        out["group_label"] = f"{parent.name} · {group.name}" if parent else group.name
        # 붙여 놓은 한 줄만 내면 화면이 그것을 다시 갈라야 하는데, 구분자가
        # `·` 라 이름에 `·` 가 들어간 그룹에서 조용히 틀린다.  폴더 트리는
        # 부모와 자식을 따로 알아야 하므로 (ADR 0035) 여기서 함께 낸다.
        out["group_name_effective"] = group.name
        out["group_parent_name_effective"] = parent.name if parent else ""
    return out


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


def order_by_date_anchor(rows: list, *, anchor, recency) -> list:
    """표의 차례 — **날짜를 아직 안 적은 것이 맨 위**, 그 아래가 날짜 최신순.

    두 무리를 나누는 이유가 서로 다르다.

    * 시험일을 안 적은 줄은 **할 일이 남은 줄**이다.  올려는 놓고 조건을 아직
      안 채운 것이라, 날짜순 어디에도 낄 자리가 없다 (없는 날짜는 0 도
      아니고 오늘도 아니다).  그런 줄을 날짜 정렬의 끝으로 밀면 -- SQL 의
      ``ORDER BY date DESC`` 가 정확히 그렇게 한다 -- 표가 길어질수록
      **방금 올린 것이 맨 아래**로 간다.  채워 넣으라고 보여 주는 자리가
      가장 안 보이는 자리가 되는 셈이다.
    * 시험일을 적은 줄은 **정리가 끝난 줄**이고, 그때 사람이 찾는 차례는
      실험 날짜순이다.

    그래서 안 적은 무리 안에서는 *올린 때* 로, 적은 무리 안에서는 *시험일* 로
    센다.  둘 다 최신이 위다.

    ``rows`` 는 이미 동률용 차례(대개 이름순)로 정렬돼 있다고 본다.  파이썬의
    정렬은 안정적이므로 그 차례가 동률 안에 그대로 남는다 -- 한 key 에
    ``reverse=True`` 로 묶으면 이름까지 거꾸로 간다.

    ``anchor`` 와 ``recency`` 는 **None 을 돌려주지 않아야 한다** (빈 문자열이나
    ``datetime.min``).  섞이면 파이썬이 비교에서 죽는다.
    """
    undated = [row for row in rows if not anchor(row)]
    dated = [row for row in rows if anchor(row)]
    for bucket in (undated, dated):
        bucket.sort(key=recency, reverse=True)
    dated.sort(key=anchor, reverse=True)
    return undated + dated
