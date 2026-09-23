"""EIS 검수와 재파싱 — 저장된 스펙트럼 전부를 한 번에 (ADR 0040).

**검수는 아무것도 바꾸지 않는다.**  맞춤도, 라벨도, 캐시도.  캐시가 없으면
원본에서 읽되 쓰지 않는다 — 고치면서 보고하면 무엇이 틀려 있었는지가 지워진다.
판정 규칙은 전부 `wrdkit.eis.audit` 에 있고, 여기는 DB 에서 그 규칙이 먹을
값을 모으고 글로 찍는 일만 한다.

**재파싱은 바꾼다** — 파생 데이터(점 캐시)만.  원본은 불변이다 (§0.2).
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

import numpy as np
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse
from sqlmodel import Session, select

from wrdkit.eis import SOLID, Spectrum, UnknownColumn, ionic_conductivity, knowledge
from wrdkit.eis.audit import (
    CHECK,
    NOTE,
    PROBLEM,
    SEVERITIES,
    SEVERITY_LABELS,
    Finding,
    audit_conductivity_scan,
    audit_fit,
    audit_record,
    audit_spectrum,
    sort_findings,
    worst,
)
from wrdkit.eis.conductivity import (
    activation_energy,
    backwards_steps,
    conductivity_ms_cm,
    real_axis_crossing,
)
from wrdkit.eis.derive import BLOCKING_PHASE_DEG, blocking_verdict

from .. import storage
from ..db import get_session
from ..models import SpectrumFit, SpectrumRecord
from ..schemas import (
    AuditFindingOut,
    AuditReferenceOut,
    AuditScanOut,
    AuditSpectrumOut,
    EisAuditOut,
    EisReparseChange,
    EisReparseOut,
)
from .eis import (
    MIN_SCAN_SWEEPS,
    _best_fit,
    _FitStub,
    _geometry,
    _is_symmetric,
    _parse_sweeps,
    _pick_sweep,
    _scan_display_name,
    _stub_parameters,
    _sweep_resistance,
    apply_exchangeable,
    presets_for,
)

router = APIRouter(prefix="/api/eis", tags=["eis"])


def _finding_out(one: Finding) -> AuditFindingOut:
    return AuditFindingOut(severity=one.severity, label=one.label, code=one.code,
                           message=one.message, refs=list(one.refs))


def _references(findings) -> list[AuditReferenceOut]:
    """판정들이 인용한 논문 기록 — 처음 나온 순서로, 한 번씩 (ADR 0042)."""
    seen: dict[str, AuditReferenceOut] = {}
    for finding in findings:
        for record_id in finding.refs:
            if record_id in seen:
                continue
            record = knowledge.record(record_id)
            seen[record_id] = AuditReferenceOut(
                id=record_id, citation=knowledge.cite(record_id),
                claim_ko=record.claim_ko, quote=record.quote)
    return list(seen.values())


class _Originals:
    """원본 파일의 상태와 점 — 파일 하나를 **한 번만** 해시하고 한 번만 파싱한다.

    스캔 하나가 스윕 스물을 한 원본에서 나눠 가지므로, 스윕마다 하면 같은 일을
    스무 번 한다.  그렇다고 **바이트를 들고 있지는 않는다** — 52 MB `.mpt` 열 개가
    검수 내내 메모리에 남는다.  해시는 조각으로 읽어 내고, 점이 필요할 때(캐시가
    없을 때)만 한 번 읽어 파싱한 **스윕들**(작은 배열)만 기억한다.
    """

    def __init__(self) -> None:
        self._state: dict[tuple[str, str], str] = {}
        self._parsed: dict[tuple[str, str], list | Exception] = {}

    @staticmethod
    def _key(record: SpectrumRecord) -> tuple[str, str]:
        return (record.sha256, record.source_format)

    def state(self, record: SpectrumRecord) -> str:
        """``"ok"`` | ``"missing"`` | ``"mismatch"``."""
        key = self._key(record)
        if key not in self._state:
            path = storage.spectrum_upload_path(record.sha256, record.source_format)
            digest = hashlib.sha256()
            try:
                with path.open("rb") as handle:
                    for chunk in iter(lambda: handle.read(1 << 20), b""):
                        digest.update(chunk)
            except OSError:
                self._state[key] = "missing"
            else:
                self._state[key] = ("ok" if digest.hexdigest() == record.sha256
                                    else "mismatch")
        return self._state[key]

    def spectrum(self, record: SpectrumRecord) -> Spectrum:
        """이 기록의 스윕을 원본에서.  `_sweep_spectrum` 과 같은 예외를 낸다."""
        key = self._key(record)
        if key not in self._parsed:
            if self.state(record) != "ok":
                raise ValueError("원본이 없거나 기록과 다릅니다")
            path = storage.spectrum_upload_path(record.sha256, record.source_format)
            try:
                self._parsed[key] = _parse_sweeps(
                    path.read_bytes(), record.original_name or record.name)[0]
            except (HTTPException, UnknownColumn, ValueError, OSError) as exc:
                self._parsed[key] = exc
        parsed = self._parsed[key]
        if isinstance(parsed, Exception):
            raise parsed
        return _pick_sweep(record, parsed)


def _points(record: SpectrumRecord, originals: _Originals
            ) -> tuple[Spectrum | None, list[Finding]]:
    """검수가 볼 점과, 원본·캐시에 대한 판정.  **캐시를 쓰지 않는다.**"""
    findings: list[Finding] = []
    state = originals.state(record)
    if state == "missing":
        findings.append(Finding(PROBLEM, "original_missing",
                                "원본 파일이 없습니다 — 점을 되살릴 수도, 파서를 고쳐 "
                                "다시 읽을 수도 없습니다. 원본을 다시 올려 주세요"))
    elif state == "mismatch":
        findings.append(Finding(PROBLEM, "original_mismatch",
                                "원본 자리에 있는 파일의 내용이 기록(sha256)과 "
                                "다릅니다 — 다른 파일이 그 이름으로 들어가 있습니다"))
    if record.parse_error:
        findings.append(Finding(PROBLEM, "parse_error",
                                f"올릴 때 읽기 오류가 있었습니다: {record.parse_error}"))
    spectrum = storage.load_spectrum(record.id, record.sha256)
    if spectrum is None and state == "ok":
        try:
            spectrum = originals.spectrum(record)
        except (HTTPException, UnknownColumn, ValueError, OSError) as exc:
            detail = exc.detail if isinstance(exc, HTTPException) else str(exc)
            findings.append(Finding(PROBLEM, "original_unreadable",
                                    f"원본을 읽지 못했습니다 — {detail}"))
        else:
            findings.append(Finding(NOTE, "cache_missing",
                                    "점 캐시가 없어 원본에서 읽었습니다 — 화면을 열거나 "
                                    "`bml reparse` 가 다시 만듭니다"))
    elif spectrum is None:
        findings.append(Finding(PROBLEM, "points_missing",
                                "점이 없습니다 — 캐시도 원본도 없어 검수할 모양이 "
                                "없습니다"))
    return spectrum, findings


def _parameter_rows(parameters: list[dict]) -> list[dict]:
    return [{"name": one.get("name"), "value": one.get("value"),
             "status": one.get("status") or ("determined" if one.get("determined")
                                             else "")}
            for one in parameters]


def _audit_spectrum(session: Session, record: SpectrumRecord,
                    originals: _Originals) -> AuditSpectrumOut:
    spectrum, findings = _points(record, originals)
    thickness_cm, area = _geometry(session, record)
    findings += audit_record(
        name=record.name or record.original_name, kind=record.kind,
        config=record.cell_config,
        thickness_um=thickness_cm * 1e4 if thickness_cm else None, area_cm2=area,
        n_points=len(spectrum) if spectrum is not None else record.n_points,
        file_name=record.original_name if record.original_name != record.name
        else "", amplitude_mv=record.amplitude_mv)

    out = AuditSpectrumOut(
        id=record.id or 0, name=record.name or record.original_name,
        kind=record.kind, cell_config=record.cell_config, purpose=record.purpose,
        sweep_index=record.sweep_index, sweep_count=record.sweep_count,
        sha256=record.sha256,
        n_points=len(spectrum) if spectrum is not None else record.n_points,
        thickness_um=thickness_cm * 1e4 if thickness_cm else None, area_cm2=area)
    # 점 자체 — 회로와 무관한 Kramers–Kronig 검사 (ADR 0043).
    points = audit_spectrum(spectrum)
    findings += points.findings
    out.kk = points.kk

    best = _best_fit(session, record.id or 0)
    if best is None:
        tried = session.exec(select(SpectrumFit).where(
            SpectrumFit.spectrum_id == record.id)).first()
        if tried is not None:
            findings.append(Finding(CHECK, "fit_never_converged",
                                    "맞춤이 있지만 하나도 수렴하지 않았습니다 — 값이 "
                                    "하나도 없습니다"))
        else:
            findings.append(Finding(NOTE, "not_fitted", "아직 맞추지 않았습니다"))
        if spectrum is not None:
            out.blocking = blocking_verdict(spectrum.frequency_hz, spectrum.z_re,
                                            spectrum.z_im)
    else:
        parameters = apply_exchangeable(
            best.circuit, json.loads(best.parameters_json) if best.parameters_json
            else [])
        stub = _FitStub(circuit=best.circuit,
                        parameters=_stub_parameters(best.circuit, parameters))
        conductivity = None
        if record.kind == SOLID and spectrum is not None:
            verdict = blocking_verdict(spectrum.frequency_hz, spectrum.z_re,
                                       spectrum.z_im)
            conductivity = ionic_conductivity(stub, thickness_cm=thickness_cm,
                                              area_cm2=area,
                                              config=record.cell_config,
                                              blocking=verdict)
        audit = audit_fit(stub, spectrum, kind=record.kind, config=record.cell_config,
                          thickness_cm=thickness_cm, area_cm2=area,
                          band=(best.frequency_low_hz, best.frequency_high_hz),
                          conductivity=conductivity,
                          alternatives=_offered(record),
                          reference=points.reference)
        findings += audit.findings
        out.circuit = best.circuit
        out.chi_squared = best.chi_squared
        out.parameters = _parameter_rows(parameters)
        out.blocking = audit.blocking or {}
        out.arcs = audit.arcs
        if audit.misfit is not None:
            out.misfit_mean = audit.misfit.mean
            out.misfit_max = audit.misfit.max
            out.misfit_at_hz = audit.misfit.at_hz

    ordered = sort_findings(findings)
    out.findings = [_finding_out(one) for one in ordered]
    out.worst = worst(ordered)
    return out


def _offered(record: SpectrumRecord) -> list[str]:
    """The circuits this kind of cell is offered — the audit recommends from these."""
    try:
        return [one["circuit"] for one in presets_for(record.kind, record.cell_config)]
    except KeyError:
        return []


def _sweep_times(spectrum: Spectrum) -> tuple[float | None, float | None]:
    """When the sweep ran, seconds from the start of the record.

    The cache keeps every column the file had; ``time/s`` is the same name in
    ``.mpr`` and ``.mpt``.  Missing means missing — no guess from the order.
    """
    times = spectrum.columns.get("time/s") if spectrum.columns else None
    if times is None:
        return None, None
    finite = np.asarray(times, dtype=float)
    finite = finite[np.isfinite(finite)]
    if not finite.size:
        return None, None
    return float(finite.min()), float(finite.max())


def _audit_scan(session: Session, records: list[SpectrumRecord],
                originals: _Originals) -> AuditScanOut:
    head = records[0]
    out = AuditScanOut(sha256=head.sha256, name=_scan_display_name(head),
                       purpose=head.purpose, sweeps=len(records),
                       symmetric=_is_symmetric(head))
    findings: list[Finding] = []
    if out.symmetric:
        temperatures: list[float | None] = []
        sigmas: list[float | None] = []
        for record in records:
            typed, _ = _sweep_resistance(record)
            spectrum = storage.load_spectrum(record.id, record.sha256)
            if spectrum is None and originals.state(record) == "ok":
                try:
                    spectrum = originals.spectrum(record)
                except (HTTPException, UnknownColumn, ValueError, OSError):
                    spectrum = None
            crossing = re_min = re_max = None
            verdict: dict = {}
            start = end = None
            if spectrum is not None:
                crossing = real_axis_crossing(spectrum.frequency_hz, spectrum.z_re,
                                              spectrum.z_im)
                real = spectrum.z_re[np.isfinite(spectrum.z_re)]
                if real.size:
                    re_min, re_max = float(real.min()), float(real.max())
                verdict = blocking_verdict(spectrum.frequency_hz, spectrum.z_re,
                                           spectrum.z_im)
                start, end = _sweep_times(spectrum)
            thickness_cm, area = _geometry(session, record)
            out.rows.append({"index": record.sweep_index,
                             "temperature_c": record.temperature_c,
                             "typed_ohm": typed, "crossing_ohm": crossing,
                             "re_min_ohm": re_min, "re_max_ohm": re_max,
                             "blocking": verdict.get("blocking"),
                             "phase_deg": verdict.get("phase_deg"),
                             "start_s": start, "end_s": end})
            temperatures.append(record.temperature_c)
            sigmas.append(conductivity_ms_cm(
                typed, thickness_mm=thickness_cm * 10.0 if thickness_cm else None,
                area_cm2=area))
        result = activation_energy(temperatures, sigmas)
        # 첫 스윕을 뺀 Ea — 첫 걸음만 거꾸로 갈 때 무엇이 달라지는지 같이 낸다
        # (실측 9개 스캔 중 5개가 60 °C 저항이 50 °C 보다 컸다).
        rest = activation_energy(temperatures[1:], sigmas[1:])
        without_first = ((rest.activation_energy_ev, rest.fit.r_squared)
                         if rest.activation_energy_ev is not None and rest.fit
                         else None)
        findings += audit_conductivity_scan(out.rows, warnings=result.warnings,
                                            reason=result.reason or "",
                                            without_first=without_first,
                                            backwards=backwards_steps(temperatures,
                                                                      sigmas))
    elif all(record.soc_percent is None for record in records) \
            and "SOC" in (head.purpose or "").upper():
        findings.append(Finding(NOTE, "soc_missing",
                                "SOC 스캔인데 SOC 를 아직 안 적었습니다 — 추세의 "
                                "x축이 전위·용량으로만 나옵니다"))
    # 스윕 하나만 지우는 것은 라이브러리가 허락하는 일이다 ("스윕 2/3 만").
    # 틀린 것이 아니라 알고 있어야 하는 것이다 — 활성화에너지가 그만큼 적은
    # 점으로 나온다.
    if len(records) < (head.sweep_count or 1):
        kept = ", ".join(str(record.sweep_index) for record in records)
        findings.append(Finding(NOTE, "sweeps_removed",
                                f"파일은 스윕 {head.sweep_count}개인데 {len(records)}개만 "
                                f"남아 있습니다 (스윕 {kept}) — 지운 것이면 그대로 "
                                f"두면 됩니다"))
    ordered = sort_findings(findings)
    out.findings = [_finding_out(one) for one in ordered]
    out.worst = worst(ordered)
    return out


def build_report(session: Session) -> EisAuditOut:
    records = session.exec(select(SpectrumRecord).order_by(
        SpectrumRecord.id)).all()
    originals = _Originals()
    spectra = [_audit_spectrum(session, record, originals) for record in records]

    grouped: dict[str, list[SpectrumRecord]] = {}
    for record in records:
        if (record.sweep_count or 1) > 1:
            grouped.setdefault(record.sha256, []).append(record)
    scans = [
        _audit_scan(session, sorted(group, key=lambda one: one.sweep_index), originals)
        for group in grouped.values()
        if len(group) >= MIN_SCAN_SWEEPS or group[0].sweep_count >= MIN_SCAN_SWEEPS
    ]

    counts = dict.fromkeys(SEVERITIES, 0)
    counts["clean"] = 0
    for one in spectra:
        counts[one.worst or "clean"] += 1
    every = [f for one in spectra for f in one.findings] + [
        f for scan in scans for f in scan.findings]
    return EisAuditOut(generated_at=datetime.now(timezone.utc), total=len(spectra),
                       counts=counts, spectra=spectra, scans=scans,
                       references=_references(every))


@router.get("/audit", response_model=EisAuditOut)
def audit_all(format: str = Query("json", pattern="^(json|text)$"),
              session: Session = Depends(get_session)):
    """저장된 스펙트럼 전부를 검수한다 — **읽기만** (ADR 0040).

    ``format=text`` 는 사람이 읽고 그대로 붙여 넣을 글이다 (`bml audit`).  글의
    모양을 셸이 아니라 여기서 만드는 이유는 판정 문장이 두 군데에 살지 않게
    하려는 것이다.
    """
    report = build_report(session)
    if format == "text":
        return PlainTextResponse(render_text(report))
    return report


# --------------------------------------------------------------------------
# 글
# --------------------------------------------------------------------------

_KIND_WORDS = {"solid": "전고체", "liquid": "액체"}
_CONFIG_WORDS = {"sym": "대칭셀", "full": "풀셀", "half": "하프셀"}


def _g(value, digits: int = 3) -> str:
    if value is None:
        return "—"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not np.isfinite(number):
        return "—"
    return f"{number:.{digits}g}"


def _e(value) -> str:
    if value is None:
        return "—"
    return f"{float(value):.2e}"


def _headline(one: AuditSpectrumOut) -> str:
    bits = [_KIND_WORDS.get(one.kind, one.kind)]
    if one.cell_config:
        bits.append(_CONFIG_WORDS.get(one.cell_config, one.cell_config))
    if one.sweep_count > 1:
        bits.append(f"스윕 {one.sweep_index}/{one.sweep_count}")
    if one.purpose:
        bits.append(one.purpose)
    return f"#{one.id}  {one.name}  ({' · '.join(bits)})"


class _Numbers:
    """글 속 근거 번호 — 처음 인용된 순서로 [1], [2], …"""

    def __init__(self) -> None:
        self.order: list[str] = []

    def suffix(self, finding: AuditFindingOut) -> str:
        if not finding.refs:
            return ""
        numbers = []
        for record_id in finding.refs:
            if record_id not in self.order:
                self.order.append(record_id)
            numbers.append(str(self.order.index(record_id) + 1))
        return f"  [근거 {'·'.join(numbers)}]"


def _block(one: AuditSpectrumOut, numbers: _Numbers) -> list[str]:
    lines = [_headline(one)]
    geometry = []
    if one.thickness_um is not None:
        geometry.append(f"두께 {_g(one.thickness_um)} µm")
    if one.area_cm2 is not None:
        geometry.append(f"면적 {_g(one.area_cm2)} cm²")
    if one.circuit:
        fit = [f"회로 {one.circuit}", f"χ² {_e(one.chi_squared)}"]
        if one.misfit_mean is not None:
            fit.append(f"오차 평균 {one.misfit_mean * 100:.2g} % · 최대 "
                       f"{one.misfit_max * 100:.2g} % ({_g(one.misfit_at_hz)} Hz)")
        lines.append("    " + " · ".join(fit))
    if geometry or one.blocking.get("phase_deg") is not None:
        extra = list(geometry)
        phase = one.blocking.get("phase_deg")
        if phase is not None:
            verdict = {True: "막음", False: "안 막음", None: "애매"}[
                one.blocking.get("blocking")]
            # 위상이 -60° 위면 판정은 꼬리의 각도도 보고 낸 것이다 — 같이 적는다.
            # 실측 풀셀 #7 이 "저주파 위상 -5° (막음)" 으로 찍혀 수와 판정이 어긋나
            # 보였다 (꼬리는 섰는데 저항이 커서 위상이 얕다, `blocking_verdict`).
            tail = one.blocking.get("tail_deg")
            rise = (f", 꼬리 {round(tail)}°" if tail is not None
                    and phase > BLOCKING_PHASE_DEG else "")
            extra.append(f"저주파 위상 {round(phase)}°{rise} ({verdict})")
        lines.append("    " + " · ".join(extra))
    if one.parameters:
        shown = []
        for item in one.parameters:
            mark = "?" if item.get("status") in ("undetermined",) else ""
            shown.append(f"{item['name']}={_g(item['value'])}{mark}")
        lines.append("    값 " + " ".join(shown) + ("   (?=미결정)" if any(
            s.endswith("?") for s in shown) else ""))
    kk = one.kk or {}
    cables = (f" · 꼭대기 배선 유도 {kk['dropped_inductive']}점 뺌"
              if kk.get("dropped_inductive") else "")
    if kk.get("range_switches_hz"):
        cables += " · 전류 범위 바뀜 " + ", ".join(
            f"{_g(value)} Hz" for value in kk["range_switches_hz"])
    if kk.get("judged"):
        lines.append(f"    KK 잔차 최대 {kk['max_residual'] * 100:.2g} % "
                     f"({_g(kk['at_hz'])} Hz) · 잡음 σ {kk['sigma'] * 100:.2g} % · "
                     f"Voigt {kk['m']}개 (decade 당 {kk['per_decade']:.1f}){cables}")
        if kk.get("reason"):
            lines.append(f"      ({kk['reason']})")
    elif kk.get("reason"):
        lines.append(f"    KK 판정 안 함 — {kk['reason']}{cables}")
    for arc in one.arcs:
        where = ("→ " + " 또는 ".join(arc["candidate_labels"])
                 if arc.get("candidate_labels") else
                 (f"→ 판정 안 함 ({arc['reason']})" if arc.get("reason") else ""))
        permittivity = (f" · εr ≈ {arc['permittivity']:.2g}"
                        if arc.get("permittivity") else "")
        lines.append(f"    아크 {arc['resistor']} ({arc['label'] or '—'}) "
                     f"{_g(arc['resistance_ohm'])} Ω · C {_e(arc['capacitance_f'])} F"
                     f"{permittivity} · f₀ {_e(arc['peak_hz'])} Hz {where}".rstrip())
    for finding in one.findings:
        lines.append(f"    [{finding.label}] {finding.message}{numbers.suffix(finding)}")
    return lines


def _scan_block(scan: AuditScanOut, numbers: _Numbers) -> list[str]:
    kind = "대칭셀" if scan.symmetric else "스캔"
    lines = [f"{scan.name}  ({kind} · 스윕 {scan.sweeps}"
             + (f" · {scan.purpose}" if scan.purpose else "") + ")"]
    if scan.rows:
        lines.append("    스윕  온도(°C)  적은 R(Ω)  실수축 교점(Ω)  Re(Z) 범위(Ω)"
                     "  저주파 위상  앞에서 쉰 시간")
        previous_end = 0.0
        for row in scan.rows:
            span = (f"{_g(row.get('re_min_ohm'), 4)}–{_g(row.get('re_max_ohm'), 4)}"
                    if row.get("re_min_ohm") is not None else "—")
            phase = row.get("phase_deg")
            shown_phase = f"{round(phase)}°" if phase is not None else "—"
            rest = "—"
            if row.get("start_s") is not None:
                gap = float(row["start_s"]) - previous_end
                rest = (f"{gap / 3600:.1f} h" if gap >= 3600 else f"{gap / 60:.0f} min")
                previous_end = float(row.get("end_s") or row["start_s"])
            lines.append(f"    {row['index']:>4}  {_g(row['temperature_c']):>8}  "
                         f"{_g(row['typed_ohm'], 4):>9}  {_g(row['crossing_ohm'], 4):>14}"
                         f"  {span:<16} {shown_phase:>6}  {rest:>8}")
    for finding in scan.findings:
        lines.append(f"    [{finding.label}] {finding.message}{numbers.suffix(finding)}")
    return lines


def _same_words(items: list[AuditSpectrumOut]) -> list[list[AuditSpectrumOut]]:
    """한 파일의 스윕이 **같은 말**을 하면 한 묶음으로.

    온도 스캔 하나가 스윕 아홉이고, 두께를 안 적었으면 아홉이 같은 참고를
    한다.  아홉 줄로 늘어놓으면 다른 파일의 말이 묻힌다.
    """
    groups: list[list[AuditSpectrumOut]] = []
    for one in items:
        key = (one.sha256, [f.message for f in one.findings])
        if groups and one.sweep_count > 1:
            previous = groups[-1][-1]
            if (previous.sha256, [f.message for f in previous.findings]) == key:
                groups[-1].append(one)
                continue
        groups.append([one])
    return groups


def render_text(report: EisAuditOut) -> str:
    """사람이 읽고, 그대로 붙여 넣을 글.

    **셀의 목록이 아니라 판정의 목록이다.**  문제·확인이 있는 스펙트럼만 수와
    함께 펼치고, 참고만 있는 것은 한 줄, 깨끗한 것은 번호만 모은다 — 수백 개를
    다 펼치면 읽을 것이 묻힌다.
    """
    counts = report.counts
    when = report.generated_at.strftime("%Y-%m-%d %H:%M UTC")
    out = [f"EIS 검수 — {when} · 스펙트럼 {report.total}개 · 스캔 {len(report.scans)}개",
           f"문제 {counts.get(PROBLEM, 0)} · 확인 {counts.get(CHECK, 0)} · "
           f"참고만 {counts.get(NOTE, 0)} · 깨끗 {counts.get('clean', 0)}",
           "(문제 = 화면의 수가 틀렸거나 이름이 틀렸을 가능성이 높다 · "
           "확인 = 사람이 한 번 봐야 한다 · 참고 = 알고 있으면 좋다)"]
    numbers = _Numbers()
    for severity in (PROBLEM, CHECK):
        chosen = [one for one in report.spectra if one.worst == severity]
        if not chosen:
            continue
        out += ["", f"━━ {SEVERITY_LABELS[severity]} ({len(chosen)}) " + "━" * 40]
        for one in chosen:
            out += [""] + _block(one, numbers)
    noted = [one for one in report.spectra if one.worst == NOTE]
    if noted:
        out += ["", f"━━ 참고만 ({len(noted)}) " + "━" * 40]
        for group in _same_words(noted):
            head, last = group[0], group[-1]
            words = " · ".join(f.message for f in head.findings)
            if len(group) == 1:
                out.append(f"#{head.id}  {head.name} — {words}")
            else:
                out.append(f"#{head.id}–#{last.id}  {head.name} … 스윕 "
                           f"{head.sweep_index}–{last.sweep_index} ({len(group)}개) — "
                           f"{words}")
    clean = [one for one in report.spectra if one.worst is None]
    if clean:
        out += ["", f"━━ 깨끗 ({len(clean)}) " + "━" * 40]
        out.append(", ".join(f"#{one.id} {one.name}" for one in clean))
    flagged = [scan for scan in report.scans if scan.findings or scan.symmetric]
    if flagged:
        out += ["", f"━━ 스캔 ({len(flagged)}) " + "━" * 40]
        for scan in flagged:
            out += [""] + _scan_block(scan, numbers)
    if numbers.order:
        # 판정의 근거 — 논문 기록 (ADR 0042).  같은 판정이 백 번 나와도 근거는
        # 한 번만 적는다.
        out += ["", f"━━ 근거 ({len(numbers.order)}) " + "━" * 40]
        for number, record_id in enumerate(numbers.order, start=1):
            record = knowledge.record(record_id)
            out.append(f"[{number}] {knowledge.cite(record_id)} — {record.claim_ko}")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------
# 재파싱
# --------------------------------------------------------------------------

def _difference(old: Spectrum | None, new: Spectrum) -> str:
    """옛 캐시와 새 점이 **다르면** 무엇이 다른지, 같으면 ``""``."""
    if old is None:
        return ""
    if len(old) != len(new):
        return f"점 {len(old)} → {len(new)}개"
    if not np.allclose(old.frequency_hz, new.frequency_hz, rtol=1e-9, atol=0):
        return (f"주파수 {old.frequency_hz.max():.3g}–{old.frequency_hz.min():.3g} → "
                f"{new.frequency_hz.max():.3g}–{new.frequency_hz.min():.3g} Hz")
    magnitude = np.abs(new.z)
    moved = np.abs(new.z - old.z) / np.where(magnitude > 0, magnitude, 1.0)
    if np.all(np.isfinite(moved)) and float(np.max(moved)) <= 1e-9:
        return ""
    return f"|Z| 가 최대 {float(np.nanmax(moved)) * 100:.3g} % 달라졌습니다"


@router.post("/reparse", response_model=EisReparseOut)
def reparse_all(format: str = Query("json", pattern="^(json|text)$"),
                session: Session = Depends(get_session)):
    """EIS 원본을 전부 다시 읽어 점 캐시를 새로 쓴다 (ADR 0040).

    지금까지 `bml reparse` 는 충방전만 원본에서 다시 읽고, EIS 는 **캐시된 점**
    으로 다시 맞췄다 — 파서가 고쳐져도 옛 점이 남았다.

    원본 하나를 한 번만 읽는다 (스캔은 스윕 스물이 한 원본이다).  스윕 수가
    기록과 다르면 그 파일은 **건드리지 않고** 적는다.  점이 달라진 스펙트럼은
    이름과 무엇이 달라졌는지를 돌려준다 — 그 맞춤은 옛 점으로 한 것이다.
    """
    records = session.exec(select(SpectrumRecord).order_by(SpectrumRecord.id)).all()
    grouped: dict[tuple[str, str], list[SpectrumRecord]] = {}
    for record in records:
        grouped.setdefault((record.sha256, record.source_format), []).append(record)

    done = 0
    changed: list[EisReparseChange] = []
    failed: list[dict] = []
    for (sha, source_format), group in grouped.items():
        path = storage.spectrum_upload_path(sha, source_format)
        try:
            content = path.read_bytes()
        except OSError:
            failed += [{"run_id": one.id, "name": one.name,
                        "reason": "원본 파일이 없습니다"} for one in group]
            continue
        if hashlib.sha256(content).hexdigest() != sha:
            failed += [{"run_id": one.id, "name": one.name,
                        "reason": "원본의 내용이 기록과 다릅니다"} for one in group]
            continue
        head = group[0]
        try:
            sweeps, _ = _parse_sweeps(content, head.original_name or head.name)
        except (HTTPException, UnknownColumn, ValueError) as exc:
            reason = exc.detail if isinstance(exc, HTTPException) else str(exc)
            failed += [{"run_id": one.id, "name": one.name, "reason": str(reason)}
                       for one in group]
            continue
        for record in group:
            try:
                fresh = _pick_sweep(record, sweeps)
            except ValueError as exc:
                failed.append({"run_id": record.id, "name": record.name,
                               "reason": f"{exc} — 점은 그대로 두었습니다"})
                continue
            old = storage.load_spectrum(record.id, record.sha256)
            detail = _difference(old, fresh)
            storage.cache_spectrum(record.id, fresh, record.sha256)
            if detail:
                changed.append(EisReparseChange(id=record.id or 0, name=record.name,
                                                detail=detail))
            record.n_points = len(fresh)
            record.frequency_start_hz = float(np.max(fresh.frequency_hz))
            record.frequency_end_hz = float(np.min(fresh.frequency_hz))
            record.parse_error = ""
            session.add(record)
            done += 1
    session.commit()
    out = EisReparseOut(total=len(records), reparsed=done, changed=changed,
                        failed=failed)
    if format == "text":
        # `bml reparse` 가 그대로 찍는다 — 셸에서 JSON 을 깎지 않는다.
        return PlainTextResponse(render_reparse_text(out))
    return out


def render_reparse_text(out: EisReparseOut) -> str:
    lines = [f"EIS 원본 {out.reparsed}/{out.total} 개를 다시 읽었습니다."]
    if out.changed:
        lines.append(f"점이 달라진 스펙트럼 {len(out.changed)}개 — 그 맞춤은 옛 점으로 "
                     f"한 것입니다:")
        lines += [f"    #{one.id} {one.name} — {one.detail}" for one in out.changed]
    if out.failed:
        lines.append(f"못 읽은 것 {len(out.failed)}개 — 점은 그대로 두었습니다:")
        lines += [f"    #{one.run_id} {one.name} — {one.reason}" for one in out.failed]
    return "\n".join(lines) + "\n"
