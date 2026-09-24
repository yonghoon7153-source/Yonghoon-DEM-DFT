"""검수가 권한 회로·하한으로 한꺼번에 다시 맞추기 — `bml refit` (ADR 0045).

**옛 맞춤은 지우지 않는다.**  검수가 받아들인 새 맞춤을 더하고 그것을 고른다
(``chosen_at``) — 그 스펙트럼의 쓰는 맞춤이 바뀐다.  묶음마다 이름
(``origin = refit-…``)을 달고, 되돌리기는 그 묶음의 맞춤만 지운다.  그러면 옛
맞춤이 다시 쓰는 맞춤이 된다.

무엇을 맞춰 보고 무엇을 받아들일지는 `wrdkit.eis.refit` 에 있다.  여기는 DB 에서
쓰는 맞춤과 점을 모으고, 맞추고, 검수에 다시 넣고, 저장하고, 글로 찍는다.  검수에
넣는 길은 `bml audit` 과 같다 (`audit_of_fit`) — 그래야 "검수가 받아들였다" 가
다음 `bml audit` 에서도 참이다.

저주파 끝이 Kramers–Kronig 를 어긴 스펙트럼은 같은 회로를 판정이 권한 하한부터
다시 맞춘다 (보완 4).  새 맞춤이 그 하한부터 맞췄으므로 다음 검수의 그 판정은
참고로 내려가고 하한을 싣지 않는다 — 다음 `bml refit` 의 대상이 아니다.

글(``format=text``)은 **흘려 보낸다.**  실측 82 건이면 십수 분이 걸릴 수 있는데,
끝에 한꺼번에 찍으면 그동안 터미널이 말이 없다.  스펙트럼 하나가 끝날 때마다 한
줄씩 나가고, 끝에 정리가 붙는다.  도중에 끊기면 거기까지 저장된 것이 남는다 —
되돌리기는 그것도 지운다.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from datetime import datetime, timezone

import numpy as np
from anyio import from_thread
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse, StreamingResponse
from sqlmodel import Session, select

from wrdkit.eis import Spectrum
from wrdkit.eis.audit import PROBLEM, FitAudit, audit_spectrum
from wrdkit.eis.refit import (
    Candidate,
    accept_refit,
    moved_number,
    refit_candidates,
    remaining_problems,
    seed_values,
)

from ..db import engine, get_session
from ..live import revision
from ..models import SpectrumFit, SpectrumRecord
from ..schemas import (
    EisRefitOut,
    EisRefitUndoOut,
    RefitSkipOut,
    RefitSpectrumOut,
    RefitTryOut,
    RefitUndoneOut,
    RefitValueOut,
)
from .eis import _best_fit, _fit_row, _load_points
from .eis_audit import _e, _finding_out, _fitted_from, _g, audit_of_fit

router = APIRouter(prefix="/api/eis", tags=["eis"])

#: 묶음 이름의 머리.  되돌리기가 이것으로 묶음을 찾는다.
ORIGIN_PREFIX = "refit-"
#: 경계에 붙은 파라미터 — 그 값은 답이 아니라 벽이라 시작점으로 옮기지 않는다.
_RAILED = ("at_lower_bound", "at_upper_bound")

#: 글에 적는 문제의 짧은 이름.  모르는 코드는 코드 그대로 적는다.
_PROBLEM_WORDS = {
    "tail_mimicked_by_arc": "꼬리를 흉내 낸 아크",
    "arcs_are_electrode": "전극 크기 아크를 벌크·입계로 부름",
    "label_contradicts_capacitance": "이름과 커패시턴스가 어긋남",
    "blocking_element_on_open_cell": "안 막는 셀에 막는 소자",
}
_START_WORDS = {"seeded": "쓰던 값에서", "default": "기본 시작점에서"}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def batch_name(when: datetime) -> str:
    """``refit-20260923T161000`` — UTC.  글자 순서가 곧 시간 순서다."""
    return ORIGIN_PREFIX + when.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%S")


@dataclass
class _Target:
    """다시 맞출 스펙트럼 하나 — 쓰는 맞춤과 그 검수를 들고 다닌다."""

    record: SpectrumRecord
    fit: SpectrumFit
    spectrum: Spectrum
    audit: FitAudit
    reference: object
    candidates: list[Candidate]
    conductivity: dict | None = None
    #: 쓰는 맞춤의 파라미터 (교환 대칭을 정리한 것) — 하한만 올린 맞춤과 견준다.
    parameters: list[dict] | None = None

    @property
    def low_hz(self) -> float | None:
        """판정이 권한 하한 — 어느 후보든 같은 하나다 (`refit_candidates`)."""
        return next((one.low_hz for one in self.candidates if one.low_hz is not None),
                    None)


@dataclass
class _Started:
    origin: str
    generated_at: datetime
    total: int
    targets: int
    skipped: list[RefitSkipOut]
    unoffered: int = 0
    windows: int = 0


@dataclass
class _Progress:
    index: int
    count: int
    spectrum: RefitSpectrumOut | None = None
    skip: RefitSkipOut | None = None


def _name(record: SpectrumRecord) -> str:
    return record.name or record.original_name


def _sigma_ohm(conductivity: dict | None) -> float | None:
    """σ 에 쓰는 저항 (Ω) — 막는 전고체 대칭셀에서 전체 σ 를 냈을 때만."""
    if not conductivity or conductivity.get("total_s_cm") is None:
        return None
    value = conductivity.get("total_ohm")
    return float(value) if value is not None else None


def _announce() -> None:
    """저장한 것이 있다고 열린 화면들에 알린다 — **이벤트 루프에서**.

    이 생성기는 일꾼 스레드에서 돈다 (흘려 보낼 때는 `iterate_in_threadpool`,
    JSON 이면 동기 창구의 스레드).  `revision.bump` 는 `asyncio.Event` 를 켜는데,
    asyncio 의 것은 스레드에 안전하지 않다.  일꾼 스레드에서 바로 켜 보니, 루프의
    디버그 모드에서는 ``RuntimeError: Non-thread-safe operation`` 이 났고 기다리던
    쪽(화면의 이벤트 흐름)은 제 시간 제한(2 초)이 지나도 영영 안 깼다.  디버그가
    아니면 깨긴 했지만 그것은 보장이 아니다.  루프 밖에서 직접 부른 경우(일꾼
    스레드가 아니다)에만 그 자리에서 올린다.
    """
    try:
        from_thread.run_sync(revision.bump)
    except RuntimeError:
        revision.bump()


def _targets(session: Session) -> tuple[int, list[_Target], list[RefitSkipOut], int]:
    """쓰는 맞춤을 전부 검수해, 회로를 실은 문제 판정이 있거나 저주파 끝의 하한이
    권해진 것만 고른다 (보완 4).  점의 검수에 쓰는 맞춤의 하한을 넣는다 — 이미 그
    하한부터 맞춘 스펙트럼은 하한을 싣지 않아 대상이 아니다.

    넷째 값은 맞춤 판정에 문제가 있는데 **권할 회로가 없는** 스펙트럼의 수다.
    글 머리에 적는다 — 검수의 "문제 82" 와 여기의 "대상" 이 왜 다른지 묻지 않게.
    """
    total = 0
    unoffered = 0
    targets: list[_Target] = []
    skipped: list[RefitSkipOut] = []
    records = session.exec(select(SpectrumRecord).order_by(SpectrumRecord.id)).all()
    for record in records:
        best = _best_fit(session, record.id or 0)
        if best is None:
            continue
        total += 1
        try:
            spectrum = _load_points(record)
        except HTTPException as exc:
            skipped.append(RefitSkipOut(id=record.id or 0, name=_name(record),
                                        reason=str(exc.detail)))
            continue
        points = audit_spectrum(spectrum, fitted_from_hz=_fitted_from(best))
        reference = points.reference
        audit, parameters, conductivity = audit_of_fit(session, record, spectrum, best,
                                                       reference)
        candidates = refit_candidates([*audit.findings, *points.findings],
                                      circuit=best.circuit)
        if candidates:
            targets.append(_Target(record, best, spectrum, audit, reference, candidates,
                                   conductivity, parameters))
        elif any(one.severity == PROBLEM for one in audit.findings):
            unoffered += 1
    return total, targets, skipped, unoffered


def _refit_one(session: Session, target: _Target, origin: str,
               dry_run: bool) -> RefitSpectrumOut:
    """권한 회로를 차례로 맞춰 보고, 받아들여진 것 중 문제가 가장 적게 남는 것을
    고른다 (같으면 권한 순서).  문제가 하나도 안 남는 것이 나오면 거기서 멈춘다.

    검수가 받아들여도 모양을 덜 그리면서 σ 에 쓰는 저항을 옮기면 받지 않는다
    (`moved_number`) — 이름은 맞아지고 수는 틀려지는 경우다.

    판정이 하한을 권했으면 (보완 4) 후보마다 그 하한부터 쓰는 맞춤의 상한까지
    맞춘다.  하한 아래 점은 셀이 변하는 동안 잰 것이다.
    """
    record, best, spectrum = target.record, target.fit, target.spectrum
    stored = json.loads(best.parameters_json) if best.parameters_json else []
    values = {row["name"]: float(row["value"]) for row in stored
              if isinstance(row.get("value"), (int, float))}
    railed = [row["name"] for row in stored if row.get("reason") in _RAILED]
    window = ((best.frequency_low_hz, best.frequency_high_hz)
              if best.frequency_low_hz is not None and best.frequency_high_hz is not None
              else None)
    top = (best.frequency_high_hz if best.frequency_high_hz is not None
           else float(np.max(spectrum.frequency_hz)))
    old_low = (best.frequency_low_hz if best.frequency_low_hz is not None
               else float(np.min(spectrum.frequency_hz)))
    old_misfit = target.audit.misfit.mean if target.audit.misfit else None
    old_sigma = _sigma_ohm(target.conductivity)
    out = RefitSpectrumOut(
        id=record.id or 0, name=_name(record), old_fit_id=best.id or 0,
        old_circuit=best.circuit, old_chi_squared=best.chi_squared,
        old_misfit_mean=old_misfit, old_sigma_ohm=old_sigma,
        problems=[_finding_out(one) for one in target.audit.findings
                  if one.severity == PROBLEM and one.circuits],
        old_problems=[_finding_out(one) for one in target.audit.findings
                      if one.severity == PROBLEM],
        old_low_hz=old_low, low_hz=target.low_hz)

    chosen: tuple[int, SpectrumFit, FitAudit, float | None, list[dict]] | None = None
    for candidate in target.candidates:
        seed = seed_values(best.circuit, values, candidate.circuit, skip=railed)
        starts = ([("seeded", seed)] if seed else []) + [("default", None)]
        # 창과 유도성 점 빼기는 쓰는 맞춤의 것 — `bml reparse` 와 같다.  하한을
        # 권했으면 그 하한부터.
        span = window if candidate.low_hz is None else (candidate.low_hz, top)
        for start, start_from in starts:
            try:
                row = _fit_row(record, spectrum, candidate.circuit,
                               drop_inductive=best.dropped_inductive > 0,
                               window=span, start_from=start_from)
            except HTTPException as exc:
                out.tries.append(RefitTryOut(circuit=candidate.circuit, start=start,
                                             converged=False, reason=str(exc.detail),
                                             low_hz=candidate.low_hz))
                break
            if not row.converged or row.chi_squared is None:
                out.tries.append(RefitTryOut(
                    circuit=row.circuit, start=start, converged=False,
                    reason="수렴하지 않았습니다" + (f" — {row.reason}" if row.reason else ""),
                    low_hz=candidate.low_hz))
                continue
            audit, parameters, conductivity = audit_of_fit(session, record, spectrum, row,
                                                           target.reference)
            misfit = audit.misfit.mean if audit.misfit else None
            sigma = _sigma_ohm(conductivity)
            verdict = accept_refit(target.audit.findings, audit.findings,
                                   candidate.triggers, converged=True,
                                   old_misfit=old_misfit, new_misfit=misfit)
            accepted, reason = verdict.accepted, verdict.reason
            if accepted:
                reason = moved_number(old_sigma, sigma, old_misfit, misfit)
                accepted = not reason
            left = remaining_problems(audit.findings) if accepted else None
            out.tries.append(RefitTryOut(
                circuit=row.circuit, start=start, converged=True,
                chi_squared=row.chi_squared, misfit_mean=misfit, sigma_ohm=sigma,
                accepted=accepted, reason=reason, problems_left=left,
                low_hz=candidate.low_hz))
            if accepted:
                if chosen is None or left < chosen[0]:
                    chosen = (left, row, audit, sigma, parameters)
                break
        if chosen is not None and chosen[0] == 0:
            break
    if chosen is None:
        return out

    _, row, audit, sigma, parameters = chosen
    out.new_circuit = row.circuit
    out.new_chi_squared = row.chi_squared
    out.new_misfit_mean = audit.misfit.mean if audit.misfit else None
    out.new_sigma_ohm = sigma
    out.new_problems = [_finding_out(one) for one in audit.findings
                        if one.severity == PROBLEM]
    out.new_low_hz = row.frequency_low_hz
    if out.new_low_hz is not None and out.new_low_hz > old_low:
        frequency = np.asarray(spectrum.frequency_hz, dtype=float)
        gone = frequency[(frequency >= old_low) & (frequency < out.new_low_hz)]
        out.dropped_points = int(gone.size)
        out.dropped_band_hz = [float(gone.min()), float(gone.max())] if gone.size else []
    if row.circuit == best.circuit:
        out.values = _value_changes(target.parameters or [], parameters)
    if not dry_run:
        row.chosen_at = _now().replace(tzinfo=None)
        row.origin = origin
        session.add(row)
        record.last_circuit = row.circuit
        session.add(record)
        session.commit()
        session.refresh(row)
        out.new_fit_id = row.id
    return out


def _number(value) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _determined(row: dict) -> bool:
    """검수 글의 ``?`` 와 같은 규칙 — 저장된 판정이 ``undetermined`` 일 때만 아니다."""
    status = row.get("status") or ("determined" if row.get("determined") else "")
    return status != "undetermined"


def _value_changes(old: list[dict], new: list[dict]) -> list[RefitValueOut]:
    """같은 회로의 두 맞춤 — 파라미터마다 옛 값 → 새 값, 새 맞춤의 순서로."""
    before = {row.get("name"): row for row in old}
    out: list[RefitValueOut] = []
    for row in new:
        was = before.get(row.get("name"))
        out.append(RefitValueOut(
            name=str(row.get("name")), new=_number(row.get("value")),
            old=_number(was.get("value")) if was else None,
            determined=_determined(row),
            was_determined=_determined(was) if was else False))
    return out


def _run(dry_run: bool) -> Iterator[_Started | _Progress | EisRefitOut]:
    """한 묶음 — 시작, 스펙트럼마다 하나, 끝의 정리 순으로 내보낸다."""
    started = _now()
    origin = batch_name(started)
    with Session(engine) as session:
        total, targets, skipped, unoffered = _targets(session)
        windows = sum(1 for target in targets if target.low_hz is not None)
        yield _Started(origin, started, total, len(targets), list(skipped), unoffered,
                       windows)
        spectra: list[RefitSpectrumOut] = []
        for index, target in enumerate(targets, start=1):
            try:
                one = _refit_one(session, target, origin, dry_run)
            except Exception as exc:  # noqa: BLE001 — 한 스펙트럼이 묶음을 멈추지 않는다
                session.rollback()
                skip = RefitSkipOut(id=target.record.id or 0, name=_name(target.record),
                                    reason=f"다시 맞추다 멈췄습니다 — "
                                           f"{type(exc).__name__}: {exc}")
                skipped.append(skip)
                yield _Progress(index, len(targets), skip=skip)
                continue
            spectra.append(one)
            yield _Progress(index, len(targets), spectrum=one)
        changed = sum(1 for one in spectra if one.new_circuit)
        if changed and not dry_run:
            # 요청이 시작될 때 한 번 올렸지만 그때는 저장한 것이 없었다.
            _announce()
        yield EisRefitOut(origin=origin, dry_run=dry_run, generated_at=started,
                          total=total, targets=len(targets), windows=windows,
                          unoffered=unoffered, changed=changed,
                          kept=len(spectra) - changed, spectra=spectra, skipped=skipped)


@router.post("/audit/refit", response_model=EisRefitOut)
def refit_by_audit(dry_run: bool = Query(False),
                   format: str = Query("json", pattern="^(json|text)$")):
    """검수가 권한 회로·하한으로 한꺼번에 다시 맞춘다 (ADR 0045) — `bml refit`.

    회로를 실은 **문제** 판정이 있는 스펙트럼과, 저주파 끝이 KK 를 어겨 하한이
    권해진 스펙트럼(같은 회로를 그 하한부터, 보완 4)만 맞춘다.  검수가 받아들인
    새 맞춤을 더하고 쓰는 맞춤으로 고른다.  옛 맞춤은 그대로다.  ``dry_run`` 이면
    맞춰 보기만 하고 아무것도 저장하지 않는다.

    ``format=text`` 는 한 줄씩 흘려 보낸다 (모듈 머리말).  세션은 여기서 연다 —
    흘려 보내는 동안 요청의 세션은 이미 닫혀 있을 수 있다.
    """
    events = _run(dry_run)
    if format == "text":
        return StreamingResponse(
            _render(events), media_type="text/plain; charset=utf-8",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
    out = None
    for event in events:
        if isinstance(event, EisRefitOut):
            out = event
    return out


@router.post("/audit/refit/undo", response_model=EisRefitUndoOut)
def undo_refit(format: str = Query("json", pattern="^(json|text)$"),
               session: Session = Depends(get_session)):
    """마지막 묶음이 저장한 맞춤을 지운다 — 그 스펙트럼들은 묶음 전으로 돌아간다.

    옛 맞춤은 묶음이 지우지 않았으므로 그대로 있고, 고른 것 중 가장 최근 것
    (없으면 χ² 최소)이 다시 쓰는 맞춤이 된다.  묶음이 없으면 아무것도 안 한다.
    """
    origin = session.exec(
        select(SpectrumFit.origin)
        .where(SpectrumFit.origin.startswith(ORIGIN_PREFIX))   # type: ignore[attr-defined]
        .order_by(SpectrumFit.origin.desc())                     # type: ignore[attr-defined]
    ).first()
    out = EisRefitUndoOut()
    if origin:
        rows = session.exec(select(SpectrumFit).where(SpectrumFit.origin == origin)
                            .order_by(SpectrumFit.spectrum_id)).all()
        removed = [(row.spectrum_id, row.circuit, row.frequency_low_hz) for row in rows]
        for row in rows:
            session.delete(row)
        session.commit()
        out = EisRefitUndoOut(origin=origin, removed=len(removed))
        for spectrum_id, circuit, low in removed:
            record = session.get(SpectrumRecord, spectrum_id)
            now = _best_fit(session, spectrum_id)
            if record is not None and now is not None:
                record.last_circuit = now.circuit
                session.add(record)
            out.spectra.append(RefitUndoneOut(
                id=spectrum_id, name=_name(record) if record else "",
                removed_circuit=circuit, now_circuit=now.circuit if now else "",
                removed_low_hz=low, now_low_hz=now.frequency_low_hz if now else None))
        session.commit()
    if format == "text":
        return PlainTextResponse(render_undo_text(out))
    return out


# --------------------------------------------------------------------------
# 글
# --------------------------------------------------------------------------

def _percent(value: float | None) -> str:
    if value is None:
        return "—"
    # 합성 셀은 3e-06 % 로 맞는다 — 그 자릿수는 읽을 거리가 아니다.
    return "< 0.01 %" if value * 100 < 0.01 else f"{value * 100:.2g} %"


def _words(code: str) -> str:
    return _PROBLEM_WORDS.get(code, code)


def _clip(text: str, limit: int = 110) -> str:
    return text if len(text) <= limit else text[:limit - 1] + "…"


def _sigma_change(old: float | None, new: float | None) -> str:
    """``σ 저항 8.48 → 8.3 Ω (-2.2 %)`` — 둘 다 없으면 빈 문자열."""
    if old is None and new is None:
        return ""
    if old is None or new is None or old <= 0:
        return (f"σ 저항 {'—' if old is None else f'{old:.4g} Ω'} → "
                f"{'—' if new is None else f'{new:.4g} Ω'}")
    shift = (new - old) / old * 100
    # 반올림하면 0 인 변화에 부호를 달면 "−0.0 %" 가 된다 (실측 B15 #7 #8).
    return (f"σ 저항 {old:.4g} → {new:.4g} Ω "
            f"({'0.0' if abs(shift) < 0.05 else f'{shift:+.1f}'} %)")


def _resolved(one: RefitSpectrumOut) -> list[str]:
    """실제로 풀린 문제의 코드 — 새 맞춤에서 그 코드의 수가 줄었다.

    회로를 실은 판정 전부가 아니다: 꼬리 흉내만 풀고 전극 크기 아크는 남는
    맞춤이 받아들여질 수 있다 (실측 B17_ACTI E C01 #2 #3).
    """
    before = Counter(p.code for p in one.old_problems)
    after = Counter(p.code for p in one.new_problems)
    return [code for code in dict.fromkeys(p.code for p in one.problems)
            if after[code] < before[code]]


def _hz(value: float | None) -> str:
    return f"{_g(value)} Hz"


def _lowered(one: RefitSpectrumOut) -> bool:
    """새 맞춤이 하한을 올려 점을 뺐다 (보완 4)."""
    return bool(one.new_circuit) and one.dropped_points > 0


def _low_change(one: RefitSpectrumOut) -> str:
    return f"하한 {_g(one.old_low_hz)} → {_hz(one.new_low_hz)}"


def _try_line(one: RefitTryOut) -> str:
    head = (f"{one.circuit} · "
            + (f"{_hz(one.low_hz)} 부터 · " if one.low_hz is not None else "")
            + _START_WORDS.get(one.start, one.start))
    if one.accepted:
        return f"{head} — 받아들임 (오차 평균 {_percent(one.misfit_mean)})"
    return f"{head} — {one.reason}"


def _progress_line(event: _Progress) -> str:
    width = len(str(event.count))
    head = f"[{event.index:>{width}}/{event.count}]"
    if event.skip is not None:
        return f"{head} #{event.skip.id}  {event.skip.name}  건너뜀 — {event.skip.reason}"
    one = event.spectrum
    if one.new_circuit:
        # 문제는 **전부** 센다 — 회로를 실은 것만 세면 원래 있던 이름 판정이
        # 새로 생긴 것처럼 읽힌다 (실측 첫 맞춰 보기: "문제 1 → 2" 가 사실 3 → 2).
        sigma = _sigma_change(one.old_sigma_ohm, one.new_sigma_ohm)
        changes = []
        if one.new_circuit != one.old_circuit:
            changes.append(f"{one.old_circuit} → {one.new_circuit}")
        if _lowered(one):
            changes.append(_low_change(one))
        if one.new_circuit == one.old_circuit:
            # 하한만 올렸다 — 풀 문제 판정이 없으니 그림이 어떻게 됐는지 적는다.
            changes.append(f"회로 그대로 · 오차 평균 {_percent(one.old_misfit_mean)} → "
                           f"{_percent(one.new_misfit_mean)}")
        else:
            changes.append(f"문제 {len(one.old_problems)} → {len(one.new_problems)}")
        return (f"{head} #{one.id}  {one.name}  바꿈  " + " · ".join(changes)
                + (f" · {sigma}" if sigma else ""))
    last = one.tries[-1] if one.tries else None
    why = _clip(_try_line(last)) if last is not None else "맞춰 볼 회로가 없습니다"
    return f"{head} #{one.id}  {one.name}  그대로  ({why})"


def _render(events: Iterable[_Started | _Progress | EisRefitOut]) -> Iterator[str]:
    """사람이 읽고 그대로 붙여 넣을 글 — 스펙트럼마다 한 줄, 끝에 정리."""
    for event in events:
        if isinstance(event, _Started):
            when = event.generated_at.strftime("%Y-%m-%d %H:%M UTC")
            lines = [f"EIS 다시 맞추기 — {when} · 묶음 {event.origin}",
                     f"맞춘 스펙트럼 {event.total}개 중 대상 {event.targets}개 — 회로를 "
                     f"권한 문제 판정이 있거나, 저주파 끝이 KK 를 어겨 하한이 권해진 것"]
            if event.windows:
                lines.append(f"하한이 권해진 {event.windows}개는 그 하한부터 맞춥니다 — 그 "
                             f"아래 점은 셀이 변하는 동안 잰 것입니다. 권한 회로가 없으면 "
                             f"쓰던 회로 그대로입니다")
            if event.unoffered:
                lines.append(f"맞춤 판정에 문제가 있지만 권할 회로가 없는 {event.unoffered}개는 "
                             f"건드리지 않습니다 — `bml audit` 에 그대로 남습니다")
            lines.append("옛 맞춤은 지우지 않습니다. 검수가 받아들인 새 맞춤만 더하고, "
                         "그것을 씁니다.")
            yield "\n".join(lines) + "\n\n"
        elif isinstance(event, _Progress):
            yield _progress_line(event) + "\n"
        else:
            yield "\n" + render_refit_summary(event)


def render_refit_summary(out: EisRefitOut) -> str:
    """끝의 정리 — 바꾼 것, 그대로 둔 것과 그 까닭, 되돌리는 길."""
    lines: list[str] = []
    changed = [one for one in out.spectra if one.new_circuit]
    kept = [one for one in out.spectra if not one.new_circuit]
    if changed:
        title = "받아들일 것" if out.dry_run else "바꾼 것"
        lines += [f"━━ {title} ({len(changed)}) " + "━" * 40]
        for one in changed:
            chosen = next((t for t in one.tries if t.accepted
                           and t.circuit == one.new_circuit), None)
            start = f" ({_START_WORDS.get(chosen.start, chosen.start)})" if chosen else ""
            sigma = _sigma_change(one.old_sigma_ohm, one.new_sigma_ohm)
            circuit = (f"{one.old_circuit} → {one.new_circuit}"
                       if one.new_circuit != one.old_circuit
                       else f"회로 그대로 {one.new_circuit}")
            low = f"{_low_change(one)} · " if _lowered(one) else ""
            lines += [f"#{one.id}  {one.name}",
                      f"    {low}{circuit}{start} · χ² "
                      f"{_e(one.old_chi_squared)} → {_e(one.new_chi_squared)} · 오차 평균 "
                      f"{_percent(one.old_misfit_mean)} → {_percent(one.new_misfit_mean)}"
                      + (f" · {sigma}" if sigma else "")]
            solved = _resolved(one)
            if solved or not _lowered(one):
                lines.append("    풀린 문제: " + ", ".join(_words(code) for code in solved))
            if _lowered(one):
                lines.append(f"    뺀 점: {_dropped(one)} — 저주파 끝이 KK 를 어긴 곳")
            lines += _value_lines(one)
            lines += [f"    남은 문제: {_words(p.code)} — {p.message}"
                      for p in one.new_problems]
        lines.append("")
    if kept:
        lines += [f"━━ 그대로 둔 것 ({len(kept)}) " + "━" * 40]
        for one in kept:
            aims = list(dict.fromkeys(_words(p.code) for p in one.problems))
            if one.low_hz is not None:
                aims.append(f"저주파 끝을 빼고 {_hz(one.low_hz)} 부터")
            lines.append(f"#{one.id}  {one.name}  ({one.old_circuit}) — "
                         f"{'풀려던 문제' if one.problems else '하려던 것'}: "
                         + ", ".join(aims))
            lines += [f"    {_try_line(t)}" for t in one.tries]
        lines.append("")
    if out.skipped:
        lines += [f"━━ 건너뜀 ({len(out.skipped)}) " + "━" * 40]
        lines += [f"#{one.id}  {one.name} — {one.reason}" for one in out.skipped]
        lines.append("")
    lines.append(f"대상 {out.targets} · {'받아들일 것' if out.dry_run else '바꾼 것'} "
                 f"{out.changed} · 그대로 {out.kept} · 건너뜀 {len(out.skipped)}")
    if out.dry_run:
        lines.append("맞춰 보기만 했습니다 — 아무것도 저장하지 않았습니다. 저장하려면 "
                     "`bml refit`.")
    elif out.changed:
        lines += [f"되돌리기: `bml refit --undo` — 이 묶음({out.origin})의 맞춤 "
                  f"{out.changed}개만 지웁니다. 옛 맞춤이 그대로 있어 묶음 전으로 "
                  f"돌아갑니다.",
                  "다시 검수: `bml audit`"]
    return "\n".join(lines) + "\n"


def _dropped(one: RefitSpectrumOut) -> str:
    """``0.01–1.02 Hz 의 점 21개``."""
    band = one.dropped_band_hz
    if len(band) == 2 and band[0] != band[1]:
        where = f"{_g(band[0])}–{_hz(band[1])}"
    elif band:
        where = _hz(band[0])
    else:
        where = f"{_hz(one.new_low_hz)} 아래"
    return f"{where} 의 점 {one.dropped_points}개"


#: 하한만 올린 맞춤의 값 줄에 적는 변화 — 이보다 작게 움직인 값은 세기만 한다.
#: 풀셀의 TL 회로는 파라미터가 열셋이라 전부 적으면 한 줄이 읽히지 않는다.
MOVED_VALUE = 0.01


def _value_lines(one: RefitSpectrumOut) -> list[str]:
    """같은 회로로 하한만 올렸을 때 — 정해진 값 중 1 % 넘게 움직인 것의 옛 → 새,
    그리고 이번에 정해지지 않게 된 값.  회로가 바뀌었으면 비었다 (같은 이름이
    다른 소자다)."""
    if not one.values:
        return []
    moved, still = [], 0
    for v in one.values:
        if not v.determined or v.old is None or v.new is None:
            continue
        if v.old and abs(v.new - v.old) > MOVED_VALUE * abs(v.old):
            moved.append(f"{v.name} {_g(v.old)} → {_g(v.new)} "
                         f"({(v.new - v.old) / abs(v.old) * 100:+.0f} %)")
        elif v.old or v.new:
            still += 1
    lost = [v.name for v in one.values if not v.determined and v.was_determined]
    lines = []
    if moved:
        lines.append("    값: " + " · ".join(moved)
                     + (f" · 나머지 {still}개는 1 % 안" if still else ""))
    elif still:
        lines.append(f"    값: 정해진 {still}개 모두 1 % 안에서 그대로")
    if lost:
        lines.append("    새로 미결정: " + ", ".join(lost)
                     + " — 뺀 점들이 정하던 값입니다")
    return lines


def _undone_line(one: RefitUndoneOut) -> str:
    moved = (one.removed_low_hz is not None and one.now_low_hz is not None
             and one.removed_low_hz != one.now_low_hz)
    low = f"하한 {_g(one.removed_low_hz)} → {_hz(one.now_low_hz)}"
    if one.now_circuit and one.now_circuit == one.removed_circuit:
        change = f"{low} ({one.now_circuit})" if moved else one.now_circuit
    else:
        change = (f"{one.removed_circuit} → {one.now_circuit or '쓸 맞춤 없음'}"
                  + (f" · {low}" if moved else ""))
    return f"    #{one.id}  {one.name} — {change}"


def render_undo_text(out: EisRefitUndoOut) -> str:
    if not out.origin:
        return "되돌릴 묶음이 없습니다 — `bml refit` 이 저장한 맞춤이 없습니다.\n"
    lines = [f"묶음 {out.origin} 의 맞춤 {out.removed}개를 지웠습니다 — 그 스펙트럼들은 "
             f"묶음 전의 맞춤으로 돌아갔습니다."]
    lines += [_undone_line(one) for one in out.spectra]
    return "\n".join(lines) + "\n"
