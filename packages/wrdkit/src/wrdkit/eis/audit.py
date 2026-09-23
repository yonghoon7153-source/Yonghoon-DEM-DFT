"""Checking a stored fit against its spectrum, and against physics (ADR 0040).

A fit that converged is not a fit that is right.  One cell on 2026-09-23 had
all three of the quiet failures this module looks for: a blocking element on a
cell that does not block (the fit drove it to its bound to make it vanish),
arcs named bulk and grain boundary whose capacitances rule both names out, and
a conductivity computed on top of those names.  The screen showed each as a
line of small print, or not at all.

Every check here returns a :class:`Finding` -- a severity, a stable code and a
sentence -- and changes nothing.  Repairing while reporting erases what was
wrong, and a fit is "the number that was quoted" (``SpectrumFit``).

Severities:

``problem``  a number on the screen is probably wrong, or wrongly named;
``check``    somebody should look -- there is no proof it is wrong;
``note``     worth knowing.

The functions take plain values and duck-typed fits (anything with
``.circuit`` and ``.parameters`` whose items have ``.name`` and ``.value``,
and optionally ``.status`` / ``.reason``), so the API's stored rows and a
fresh :class:`~wrdkit.eis.fit.FitResult` are audited by the same code.
"""

from __future__ import annotations

import math
import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field

import numpy as np

from .capacitance import LOWEST_N, ArcCapacitance, arc_capacitances, process
from .circuit import Circuit, CircuitError, parse_circuit, series_parts
from .derive import SOLID, SYMMETRIC, blocking_verdict, label_arcs
from .fit import edge_misfit
from .spectrum import Spectrum

__all__ = ["CHECK", "Finding", "FitAudit", "Misfit", "NOTE", "PROBLEM",
           "SEVERITIES", "SEVERITY_LABELS", "audit_conductivity_scan",
           "audit_fit", "audit_record", "circuit_end", "config_from_name",
           "misfit", "sort_findings", "thickness_from_name", "worst"]

PROBLEM = "problem"
CHECK = "check"
NOTE = "note"
SEVERITIES = (PROBLEM, CHECK, NOTE)
SEVERITY_LABELS = {PROBLEM: "문제", CHECK: "확인", NOTE: "참고"}

#: 평균 상대오차가 이만큼이면 회로가 스펙트럼 **전체**를 못 그린다.  랩의
#: 실측 비교(프리셋 note)에서 좋은 회로는 1 % 안쪽, 나쁜 회로가 2 % 대였다.
MEAN_MISFIT_LIMIT = 0.03
#: 한 점이라도 이만큼 어긋나면 어디서인지 적는다.  `L1` 없이 맞춘 하프셀이
#: 고주파 끝에서 12–15 % 를 냈고, 그것이 화면의 "반원 둘이 안 나온다" 였다.
MAX_MISFIT_LIMIT = 0.10
#: 오차가 저주파 끝에 몰렸다는 말은 그 오차가 이만큼은 될 때만 한다.
EDGE_MISFIT_FLOOR = 0.05
#: 고체 전해질로 있을 수 있는 전도도 (S/cm).  위는 액체 전해질보다 크고,
#: 아래는 영하의 나쁜 소재보다도 작다 — 그 밖이면 단위를 먼저 의심한다.
SIGMA_RANGE_S_CM = (1e-9, 1e-1)
#: 두께·면적이 이 밖이면 단위를 잘못 적은 크기다 (mm ↔ µm, mm² ↔ cm²).
THICKNESS_RANGE_UM = (5.0, 5000.0)
AREA_RANGE_CM2 = (0.01, 20.0)
#: 이름이 말하는 두께와 적힌 두께가 이만큼(비율) 넘게 다르면 적는다.
NAME_THICKNESS_TOLERANCE = 0.05
#: 적은 저항과 실수축 교점의 비가 이 밖이면 적는다.  열 배는 소수점이다.
TYPED_VS_CROSSING_LIMIT = 3.0
#: 점이 이보다 적으면 무엇을 맞춰도 파라미터보다 점이 모자란다.
FEWEST_POINTS = 10

#: 직렬 경로에 있으면 **DC 를 막는** 소자.  `Wo` 는 반사 경계라 저주파에서
#: 축전기가 된다 (`Ws` 는 투과 경계라 실수축으로 돌아온다 — 반대다).
BLOCKING_KINDS = frozenset({"C", "CPE", "Wo"})

#: 셀 구성이 아크에 붙이는 이름이 **어느 과정**을 말하는가.  고주파부터.
#: 여기 없는 조합은 이름이 과정을 주장하지 않으므로 판정하지 않는다
#: ("고주파 아크" 는 틀릴 수가 없다).
EXPECTED_PROCESSES: dict[tuple[str, str], tuple[str | None, ...]] = {
    (SOLID, SYMMETRIC): ("bulk", "grain_boundary", None),
}


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str

    @property
    def label(self) -> str:
        return SEVERITY_LABELS.get(self.severity, self.severity)


def sort_findings(findings: Iterable[Finding]) -> list[Finding]:
    """Worst first, then in the order they were found."""
    order = {one: i for i, one in enumerate(SEVERITIES)}
    return sorted(findings, key=lambda one: order.get(one.severity, len(order)))


def worst(findings: Iterable[Finding]) -> str | None:
    """The most severe severity present, or ``None`` for a clean list."""
    present = {one.severity for one in findings}
    return next((one for one in SEVERITIES if one in present), None)


# --------------------------------------------------------------------------
# the record: what was written about the measurement
# --------------------------------------------------------------------------

_THICKNESS_IN_NAME = re.compile(
    r"(?<![\d.,eE+-])(\d+(?:\.\d+)?)\s*(?:um|µm|μm)(?![a-z0-9])", re.IGNORECASE)


def thickness_from_name(name: str | None) -> float | None:
    """The thickness a file name mentions, in µm -- the last one wins.

    The same rule as the screen's ``thicknessFromName`` (`lib/format.ts`):
    ``(?![a-z0-9])`` rather than ``\\b``, because ``_`` is a word character
    and this lab's names are ``…_70um_sym_01``.
    """
    found = None
    for match in _THICKNESS_IN_NAME.finditer(name or ""):
        value = float(match.group(1))
        if value > 0:
            found = value
    return found


def config_from_name(name: str | None) -> str | None:
    """``sym`` / ``half`` / ``full`` when the name says so, else ``None``.

    Mirrors ``cellConfigFromName``: ``symmetry`` is not ``sym``, and the
    capital F of ``LiFull`` is not a full cell.
    """
    text = (name or "").lower()
    if re.search(r"(^|[^a-z])sym(m|metric|metrical)?([^a-z]|$)", text):
        return "sym"
    if re.search(r"(^|[^a-z])half([^a-z]|$)", text):
        return "half"
    if re.search(r"(^|[^a-z])full(cell)?([^a-z]|$)", text):
        return "full"
    return None


_CONFIG_WORDS = {"sym": "대칭셀", "full": "풀셀", "half": "하프셀", "": "비어 있음"}


def audit_record(*, name: str, kind: str, config: str = "",
                 thickness_um: float | None = None, area_cm2: float | None = None,
                 n_points: int | None = None) -> list[Finding]:
    """What was written about the measurement, before any fit is looked at."""
    out: list[Finding] = []
    if n_points is not None and n_points < FEWEST_POINTS:
        out.append(Finding(CHECK, "few_points",
                           f"점이 {n_points}개뿐입니다 — 회로 파라미터보다 점이 "
                           f"모자라면 무엇을 맞춰도 값이 정해지지 않습니다"))
    if kind == SOLID and not config:
        out.append(Finding(CHECK, "config_missing",
                           "전고체인데 셀 구성이 비어 있습니다 — 아크를 벌크·입계로도 "
                           "계면으로도 부르지 못하고, 전도도도 안 나옵니다"))
    hinted = config_from_name(name)
    if hinted and hinted != (config or ""):
        out.append(Finding(CHECK, "config_differs_from_name",
                           f"이름은 {_CONFIG_WORDS[hinted]}인데 셀 구성은 "
                           f"{_CONFIG_WORDS.get(config or '', config)}입니다"))
    named = thickness_from_name(name)
    if named and thickness_um and \
            abs(thickness_um - named) > NAME_THICKNESS_TOLERANCE * named:
        out.append(Finding(CHECK, "thickness_differs_from_name",
                           f"이름은 {named:g} µm 인데 적힌 두께는 {thickness_um:g} µm "
                           f"입니다 — 전도도가 {thickness_um / named:.3g}배 달라집니다"))
    low, high = THICKNESS_RANGE_UM
    if thickness_um is not None and not low <= thickness_um <= high:
        out.append(Finding(CHECK, "thickness_out_of_range",
                           f"두께 {thickness_um:g} µm 는 펠릿이나 전극의 두께가 "
                           f"아닙니다 — mm 와 µm 를 바꿔 적었는지 보세요"))
    low, high = AREA_RANGE_CM2
    if area_cm2 is not None and not low <= area_cm2 <= high:
        out.append(Finding(CHECK, "area_out_of_range",
                           f"면적 {area_cm2:g} cm² 는 셀의 면적이 아닙니다 — "
                           f"mm² 로 적었거나 지름을 넣었는지 보세요"))
    return out


# --------------------------------------------------------------------------
# the fit
# --------------------------------------------------------------------------

def circuit_end(circuit: str | Circuit) -> str:
    """How the circuit's low-frequency end closes.

    ``blocking``  a ``C``/``CPE``/``Wo`` in the series path: ``|Z| -> inf``,
                  phase towards -90°.  Position does not matter.
    ``diffusive`` a semi-infinite ``W`` and nothing blocking: -45° for ever.
    ``resistive`` everything else: the spectrum returns to the real axis.
    """
    model = parse_circuit(circuit) if isinstance(circuit, str) else circuit
    kinds = {kind for _, kind in model.series_element_kinds()}
    if kinds & BLOCKING_KINDS:
        return "blocking"
    if "W" in kinds:
        return "diffusive"
    return "resistive"


@dataclass(frozen=True)
class Misfit:
    """``|Z_fit − Z| / |Z|`` over the points the fit used."""

    mean: float
    max: float
    at_hz: float
    points: int


def _band(spectrum: Spectrum, band: tuple[float, float] | None) -> Spectrum:
    """The points inside the fitted window, or all of them when it is unknown
    or leaves fewer than two (the API's ``_fitted_band`` rule)."""
    if band is None or band[0] is None or band[1] is None:
        return spectrum
    low, high = band
    kept = spectrum.select((spectrum.frequency_hz >= low)
                           & (spectrum.frequency_hz <= high))
    return kept if len(kept) >= 2 else spectrum


def misfit(spectrum: Spectrum, circuit: str | Circuit,
           values: dict[str, float], band: tuple[float, float] | None = None
           ) -> tuple[Misfit | None, np.ndarray | None, Spectrum]:
    """The relative misfit of ``values`` on ``spectrum`` inside ``band``.

    Returns the summary, the model's impedance on the used points, and those
    points.  ``None`` for the first two when a parameter is missing or the
    arithmetic gives nothing finite.
    """
    model = parse_circuit(circuit) if isinstance(circuit, str) else circuit
    used = _band(spectrum, band)
    try:
        ordered = np.array([float(values[name]) for name in model.parameter_names])
    except KeyError:
        return None, None, used
    fitted = model.impedance(ordered, used.frequency_hz)
    measured = used.z
    magnitude = np.abs(measured)
    good = np.isfinite(fitted) & np.isfinite(measured) & (magnitude > 0)
    if not good.any():
        return None, None, used
    relative = np.abs(fitted[good] - measured[good]) / magnitude[good]
    at = int(np.argmax(relative))
    return (Misfit(mean=float(np.mean(relative)), max=float(relative[at]),
                   at_hz=float(used.frequency_hz[good][at]),
                   points=int(good.sum())),
            fitted, used)


@dataclass
class FitAudit:
    findings: list[Finding] = field(default_factory=list)
    misfit: Misfit | None = None
    #: One entry per capacitive arc, with the name the cell gives it.
    arcs: list[dict] = field(default_factory=list)
    blocking: dict | None = None
    end: str = ""


def _status(parameter) -> str:
    return str(getattr(parameter, "status", "") or "")


def _railed(parameter, model: Circuit) -> str:
    """``lower`` / ``upper`` / ``""`` -- from the stored reason, or from the
    circuit's bounds for rows saved before the reason existed."""
    reason = str(getattr(parameter, "reason", "") or "")
    if reason == "at_lower_bound":
        return "lower"
    if reason == "at_upper_bound":
        return "upper"
    try:
        at = model.parameter_names.index(parameter.name)
    except ValueError:
        return ""
    value = float(parameter.value)
    for side, bound in (("lower", model.lower[at]), ("upper", model.upper[at])):
        if bound and abs(value - bound) <= 1e-6 * abs(bound):
            return side
    return ""


def _rail_finding(name: str, value: float, side: str, *,
                  in_series: bool) -> Finding:
    """What a parameter on its bound means, element by element.

    ``in_series``: the element sits in the top-level series path.  A vanishing
    series element can simply be left out; a vanishing element inside
    ``p(R,CPE)`` takes its whole arc with it.
    """
    element, _, suffix = name.partition("_")
    kind = re.match(r"[A-Za-z]+", element).group(0) if element else ""
    shown = f"{value:.4g}"
    if kind == "CPE" and suffix == "n" and side == "upper":
        return Finding(NOTE, "cpe_ideal",
                       f"{element} 의 n 이 1 에 붙었습니다 — 이상적인 축전기입니다 "
                       f"(틀린 것은 아닙니다)")
    if kind == "CPE" and suffix == "Q" and side == "upper":
        return Finding(CHECK, "element_vanishing",
                       f"{element} 의 Q 가 상한({shown})에 붙었습니다 — 임피던스가 "
                       f"0 이 되려는, 사라지려는 소자입니다. "
                       + ("이 소자 없이 맞춰 보세요" if in_series
                          else "그 아크 전체가 없어지려 합니다 — 아크 하나를 빼고 "
                               "맞춰 보세요"))
    if kind == "R" and side == "lower":
        return Finding(CHECK, "element_vanishing",
                       f"{name} 이 0 에 붙었습니다 ({shown} Ω) — "
                       + ("이 저항은 없어도 되는 소자입니다" if in_series
                          else "그 아크가 없어지려 합니다 — 아크 하나를 빼고 맞춰 "
                               "보세요"))
    if kind == "R" and side == "upper":
        return Finding(CHECK, "branch_open",
                       f"{name} 이 상한({shown} Ω)에 붙었습니다 — 그 가지는 열린 "
                       f"것과 같습니다")
    if kind == "L" and side == "lower":
        return Finding(NOTE, "no_inductance",
                       f"{name} 이 0 에 붙었습니다 — 이 파일에는 배선 인덕턴스가 "
                       f"안 보입니다")
    where = "하한" if side == "lower" else "상한"
    return Finding(CHECK, "at_bound",
                   f"{name} 이 {where}({shown})에 붙었습니다 — 경계가 물리적으로 "
                   f"맞는 값인지 보세요")


def _fmt(value: float | None, unit: str = "") -> str:
    """Capacitances span fifteen decades -- always in exponent form."""
    if value is None or not math.isfinite(value):
        return "—"
    return f"{value:.2e}{(' ' + unit) if unit else ''}"


def _deg(phase: float | None) -> str:
    """``-0°`` reads like a sign that means something; it does not."""
    if phase is None or not math.isfinite(phase):
        return "—"
    return f"{round(phase)}°"


def _suggest_without(circuit: str, names: Sequence[str]) -> str:
    """The circuit with the named series leaves taken out, or ``""``."""
    try:
        parts = [part for part in series_parts(circuit) if part not in names]
    except CircuitError:
        return ""
    return "-".join(parts)


def audit_fit(fit, spectrum: Spectrum | None, *, kind: str, config: str = "",
              thickness_cm: float | None = None, area_cm2: float | None = None,
              band: tuple[float, float] | None = None,
              conductivity: dict | None = None) -> FitAudit:
    """Every check one stored fit can be put through.

    ``band`` is the frequency window the fit used (its misfit is measured
    there, and an arc apex outside it was extrapolated).  ``conductivity`` is
    what ``ionic_conductivity`` gave for it, when it was asked.
    """
    out = FitAudit()
    try:
        model = parse_circuit(fit.circuit)
    except CircuitError as exc:
        out.findings.append(Finding(PROBLEM, "circuit_unreadable",
                                    f"회로 `{fit.circuit}` 를 읽지 못합니다: {exc}"))
        return out
    parameters = list(fit.parameters)
    values = {p.name: float(p.value) for p in parameters}
    statuses = {p.name: _status(p) for p in parameters}
    missing = [name for name in model.parameter_names if name not in values]
    if missing:
        out.findings.append(Finding(PROBLEM, "parameters_missing",
                                    "저장된 맞춤에 회로의 파라미터가 빠져 있습니다: "
                                    + ", ".join(missing)))
        return out
    out.end = circuit_end(model)

    # -- 곡선이 점을 지나가나 --------------------------------------------------
    if spectrum is not None and len(spectrum):
        summary, fitted, used = misfit(spectrum, model, values, band)
        out.misfit = summary
        if summary is not None:
            edge = edge_misfit(used.frequency_hz, used.z, fitted,
                               len(model.parameter_names))
            if summary.mean >= MEAN_MISFIT_LIMIT:
                out.findings.append(Finding(
                    CHECK, "misfit_everywhere",
                    f"맞춤이 평균 {summary.mean * 100:.1f} % 어긋납니다 — 회로가 이 "
                    f"스펙트럼의 모양을 못 그립니다 (최대 {summary.max * 100:.0f} %, "
                    f"{summary.at_hz:.3g} Hz)"))
            # 오차가 **몰렸다**는 것만으로는 적지 않는다.  거의 완벽한 맞춤도
            # 가장 작은 오차들이 어딘가에는 몰려 있다 — 실측 셀의 합성 쌍둥이
            # (최대 0.07 %)에서 "98 % 가 저주파에" 가 떴다.
            if edge is not None and summary.max >= EDGE_MISFIT_FLOOR:
                out.findings.append(Finding(
                    CHECK if summary.max >= MAX_MISFIT_LIMIT else NOTE,
                    "misfit_at_edge",
                    f"오차의 {edge.share * 100:.0f} % 가 가장 낮은 {edge.count}개 "
                    f"점(≤ {edge.upper_hz:.3g} Hz)에 몰려 있습니다 (최대 "
                    f"{summary.max * 100:.0f} %) — 하한을 {edge.threshold_hz:.3g} Hz "
                    f"로 두고 다시 맞춰 보세요"))
            elif summary.mean < MEAN_MISFIT_LIMIT and summary.max >= MAX_MISFIT_LIMIT:
                out.findings.append(Finding(
                    CHECK, "misfit_somewhere",
                    f"{summary.at_hz:.3g} Hz 에서 {summary.max * 100:.0f} % 어긋납니다 "
                    f"(평균 {summary.mean * 100:.1f} %) — 그 주파수의 모양을 회로가 "
                    f"못 그립니다"))

        # -- 막는 셀인가, 회로도 그렇게 말하나 ---------------------------------
        verdict = blocking_verdict(spectrum.frequency_hz, spectrum.z_re, spectrum.z_im)
        out.blocking = verdict
        blockers = [name for name, element_kind in model.series_element_kinds()
                    if element_kind in BLOCKING_KINDS]
        phase = verdict.get("phase_deg")
        if verdict.get("blocking") is False and blockers:
            suggestion = _suggest_without(fit.circuit, blockers)
            out.findings.append(Finding(
                PROBLEM, "blocking_element_on_open_cell",
                f"스펙트럼은 저주파에서 실수축으로 내려오는데 (위상 {_deg(phase)}) "
                f"회로 끝에 막는 소자 {', '.join(blockers)} 가 있습니다 — 맞춤이 그 "
                f"소자를 지우려고 경계로 갑니다"
                + (f". `{suggestion}` 로 다시 맞추세요" if suggestion else "")))
        if verdict.get("blocking") is True and out.end == "resistive":
            out.findings.append(Finding(
                CHECK, "open_end_on_blocking_cell",
                f"스펙트럼은 저주파에서 수직으로 서는데 (위상 {_deg(phase)}) 회로의 "
                f"저주파 끝이 실수축으로 닫힙니다 — 마지막 아크가 꼬리를 흉내 "
                f"냅니다. 끝에 CPE 를 달아 보세요"))
        if (kind, config) == (SOLID, SYMMETRIC) and verdict.get("blocking") is False:
            out.findings.append(Finding(
                CHECK, "symmetric_cell_does_not_block",
                "이 대칭셀은 이온을 막지 않습니다 — 벌크·입계 σ 가 나올 수 없는 "
                "측정입니다. 2026-09-23 전 화면은 σ 를 냈으므로, 슬라이드에 옮긴 "
                "값이 있으면 다시 보세요"))

    # -- 경계에 붙은 것, 미결정, 옛 행 -----------------------------------------
    in_series = {name for name, _ in model.series_element_kinds()}
    for parameter in parameters:
        side = _railed(parameter, model)
        if side:
            out.findings.append(_rail_finding(
                parameter.name, float(parameter.value), side,
                in_series=parameter.name.partition("_")[0] in in_series))
    for name in model.parameter_names:
        element, _, suffix = name.partition("_")
        if suffix == "n" and element.startswith("CPE") and values[name] <= LOWEST_N:
            out.findings.append(Finding(
                CHECK, "cpe_like_diffusion",
                f"{element} 의 n = {values[name]:.2f} — 반원이 아니라 확산에 "
                f"가깝습니다. 그 아크의 저항을 계면·입계 저항으로 읽기 어렵습니다"))
    undetermined = [name for name in model.parameter_names
                    if statuses.get(name) == "undetermined"]
    if undetermined:
        out.findings.append(Finding(NOTE, "undetermined",
                                    "미결정 파라미터: " + ", ".join(undetermined)))
    if any(statuses.get(name) == "legacy_unknown" for name in model.parameter_names):
        out.findings.append(Finding(NOTE, "legacy_fit",
                                    "판정 기록이 없는 옛 맞춤입니다 — `bml reparse` "
                                    "가 같은 회로로 다시 맞춥니다"))

    # -- 아크의 커패시턴스 ------------------------------------------------------
    arcs = arc_capacitances(model, values, thickness_cm=thickness_cm,
                            area_cm2=area_cm2)
    try:
        labels = {meaning.parameter: meaning.label
                  for meaning in label_arcs(fit, kind, config)}
    except ValueError:
        # 모르는 종류·구성 — 이름이 없으면 이름을 검사할 것도 없다.
        labels = {}
    series = {name for name, element_kind in model.series_element_kinds()
              if element_kind == "R"}
    arc_order = [name for name in labels if name not in series]
    expected = EXPECTED_PROCESSES.get((kind, config))
    for arc in arcs:
        position = arc_order.index(arc.resistor) if arc.resistor in arc_order else None
        claim = None
        if expected is not None and position is not None:
            claim = expected[min(position, len(expected) - 1)]
        out.arcs.append(_arc_row(arc, labels.get(arc.resistor, ""), claim))
        _arc_findings(out, arc, labels.get(arc.resistor, ""), claim, statuses, band)

    # -- 전도도의 크기 ----------------------------------------------------------
    total = (conductivity or {}).get("total_s_cm")
    low, high = SIGMA_RANGE_S_CM
    if total is not None and not low <= total <= high:
        out.findings.append(Finding(
            CHECK, "sigma_out_of_range",
            f"σ_total = {total:.3g} S/cm 는 고체 전해질로 있을 수 없는 크기입니다 — "
            f"두께(µm)·면적(cm²) 단위를 먼저 보세요"))
    out.findings = sort_findings(out.findings)
    return out


def _arc_row(arc: ArcCapacitance, label: str, claim: str | None) -> dict:
    return {
        "resistor": arc.resistor, "element": arc.element, "label": label,
        "resistance_ohm": arc.resistance_ohm, "q": arc.q, "n": arc.n,
        "capacitance_f": arc.capacitance_f, "peak_hz": arc.peak_hz,
        "per_length": arc.per_length, "per_area": arc.per_area,
        "candidates": list(arc.candidates) if arc.candidates is not None else None,
        "candidate_labels": ([process(key).label for key in arc.candidates]
                             if arc.candidates is not None else None),
        "claims": claim, "reason": arc.reason,
    }


def _arc_findings(out: FitAudit, arc: ArcCapacitance, label: str,
                  claim: str | None, statuses: dict[str, str],
                  band: tuple[float, float] | None) -> None:
    if arc.peak_hz is not None and band is not None \
            and band[0] is not None and band[1] is not None:
        low, high = band
        if arc.peak_hz > high:
            out.findings.append(Finding(
                CHECK, "arc_apex_above_window",
                f"{arc.resistor} 아크의 꼭지(f₀ = {arc.peak_hz:.3g} Hz)가 맞춘 구간 "
                f"위(≤ {high:.3g} Hz)에 있습니다 — 반원의 꼭대기를 못 보고 정한 "
                f"저항입니다"))
        elif arc.peak_hz < low:
            out.findings.append(Finding(
                CHECK, "arc_apex_below_window",
                f"{arc.resistor} 아크의 꼭지(f₀ = {arc.peak_hz:.3g} Hz)가 맞춘 구간 "
                f"아래(≥ {low:.3g} Hz)에 있습니다 — 반원이 닫히는 것을 못 보고 정한 "
                f"저항입니다"))
    if claim is None or arc.candidates is None:
        return
    names = [arc.resistor]
    names += ([f"{arc.element}_Q", f"{arc.element}_n"] if arc.element_kind == "CPE"
              else [arc.element])
    shaky = [name for name in names if statuses.get(name) == "undetermined"]
    if shaky:
        out.findings.append(Finding(
            NOTE, "capacitance_not_judged",
            f"{arc.resistor} 아크는 {', '.join(shaky)} 가 미결정이라 커패시턴스로 "
            f"이름을 검사하지 않았습니다"))
        return
    if claim in arc.candidates:
        return
    allowed = " 또는 ".join(process(key).label for key in arc.candidates)
    out.findings.append(Finding(
        PROBLEM, "label_contradicts_capacitance",
        f"{arc.resistor} ({label}) 의 커패시턴스 {_fmt(arc.capacitance_f, 'F')} "
        f"(C·l/A {_fmt(arc.per_length)}, C/A {_fmt(arc.per_area, 'F/cm²')}) 는 "
        f"{process(claim).label}일 수 없습니다 — "
        + (f"{allowed}의 크기입니다" if allowed else "표의 어느 범위에도 안 듭니다")))


# --------------------------------------------------------------------------
# a temperature scan (ADR 0039)
# --------------------------------------------------------------------------

def audit_conductivity_scan(sweeps: Sequence[dict], *,
                            warnings: Sequence[str] = (),
                            reason: str = "") -> list[Finding]:
    """The per-sweep numbers a conductivity scan rests on.

    ``sweeps`` items: ``{"index", "temperature_c", "typed_ohm", "crossing_ohm"}``.
    ``warnings`` / ``reason`` are the activation energy's own (ADR 0039) --
    repeated here so the report has them in one place.
    """
    out: list[Finding] = []
    blank = [str(one["index"]) for one in sweeps if one.get("temperature_c") is None]
    if blank and len(blank) == len(sweeps):
        out.append(Finding(NOTE, "temperatures_missing",
                           "온도를 아직 안 적었습니다 — 활성화에너지가 안 나옵니다"))
    elif blank:
        out.append(Finding(CHECK, "temperatures_partly_missing",
                           "온도가 빈 스윕: " + ", ".join(blank)))
    untyped = [str(one["index"]) for one in sweeps if one.get("typed_ohm") is None]
    if untyped and len(untyped) == len(sweeps):
        out.append(Finding(NOTE, "resistances_missing",
                           "저항을 아직 안 적었습니다 — 이온전도도가 안 나옵니다"))
    elif untyped:
        out.append(Finding(NOTE, "resistance_partly_missing",
                           "저항을 안 적은 스윕: " + ", ".join(untyped)))
    for one in sweeps:
        typed, crossing = one.get("typed_ohm"), one.get("crossing_ohm")
        if not typed or not crossing or typed <= 0 or crossing <= 0:
            continue
        ratio = typed / crossing
        if ratio >= TYPED_VS_CROSSING_LIMIT or ratio <= 1 / TYPED_VS_CROSSING_LIMIT:
            out.append(Finding(
                CHECK, "typed_far_from_crossing",
                f"스윕 {one['index']}: 적은 저항 {typed:.4g} Ω 이 실수축 교점 "
                f"{crossing:.4g} Ω 의 {ratio:.3g}배입니다 — 소수점을 보세요 (아크의 "
                f"오른쪽 끝을 읽었다면 맞는 값입니다)"))
    for warning in warnings:
        out.append(Finding(CHECK, "activation_warning", warning))
    if reason:
        out.append(Finding(NOTE, "activation_missing", f"활성화에너지 없음 — {reason}"))
    return sort_findings(out)

