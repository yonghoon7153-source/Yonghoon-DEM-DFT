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

from .capacitance import (
    BULK,
    FACE,
    LOWEST_N,
    UNDETERMINED_SPREAD,
    ArcCapacitance,
    arc_capacitances,
    effective_capacitance,
    process,
    size_class,
    spread_for,
)
from .circuit import (
    BLOCKING_KINDS,
    Circuit,
    CircuitError,
    circuit_end,
    parse_circuit,
    series_parts,
)
from .conductivity import BOLTZMANN_EV_PER_K, backwards_warning, real_axis_crossing
from .derive import SOLID, SYMMETRIC, blocking_verdict, label_arcs
from .fit import edge_misfit
from .kk import KKResult, lin_kk
from .spectrum import Spectrum

__all__ = ["CHECK", "Finding", "FitAudit", "Misfit", "NOTE", "PROBLEM",
           "REFERENCES", "SEVERITIES", "SpectrumAudit", "audit_spectrum", "SEVERITY_LABELS", "audit_conductivity_scan",
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
#: 적은 저항이 그 스윕의 Re(Z) 가 지나간 범위를 이만큼 넘어 벗어나면 적는다.
#:
#: 처음에는 "실수축 교점의 세 배" 로 봤다.  틀렸다: 아크가 보이는 스윕에서
#: 랩은 아크의 **오른쪽 끝**을 읽고, 그것은 고주파 교점보다 몇 배 크다 —
#: 합성 온도 스캔에서 교점 2.0 Ω, 맞게 읽은 값 9.69 Ω.  제대로 읽은 값이면
#: 무엇이든 **곡선 위의 점**이므로, 곡선이 지나간 Re 범위 안에 있어야 한다.
#: 그 밖이면 소수점이거나 다른 스윕의 값이다.
TYPED_OUTSIDE_SPAN_MARGIN = 0.10
#: 점이 이보다 적으면 무엇을 맞춰도 파라미터보다 점이 모자란다.
FEWEST_POINTS = 10
#: 아크의 저항이 맞춘 구간의 가장 작은 |Z| 의 이만큼(비율)도 안 되면 그 아크는
#: 스펙트럼에 아무것도 그리지 않는다 — 좋은 스윕의 잡음(0.1 %)보다 작다.
VANISHED_ARC_SHARE = 1e-3

#: 셀 구성이 아크에 붙이는 이름이 **어느 과정**을 말하는가.  고주파부터.
#: 여기 없는 조합은 이름이 과정을 주장하지 않으므로 판정하지 않는다
#: ("고주파 아크" 는 틀릴 수가 없다).
EXPECTED_PROCESSES: dict[tuple[str, str], tuple[str | None, ...]] = {
    (SOLID, SYMMETRIC): ("bulk", "grain_boundary", None),
}


#: 판정 코드마다 그 판정이 기대는 논문 기록 (ADR 0042, `wrdkit.eis.knowledge`).
#: 근거가 없는 코드는 우리 규칙(경계 붙음, 점 수, 단위)이거나 실측에서 나온
#: 것이다 — 그것도 사실이므로 없는 근거를 지어 붙이지 않는다.
REFERENCES: dict[str, tuple[str, ...]] = {
    # 아크의 이름과 커패시턴스
    "label_contradicts_capacitance": ("ISW1990.table1-capacitance-interpretation",
                                      "ISW1990.assign-by-capacitance-magnitude",
                                      "ISW1990.bulk-capacitance-unit-cell-constant",
                                      "HIRSCHORN2010.hsu-mansfeld-normal-eq18"),
    "arcs_are_electrode": ("ISW1990.table1-capacitance-interpretation",
                           "ISW1990.bulk-arc-off-scale",
                           "VADHVA2021.sulfide-bulk-gb-overlap"),
    "bulk_above_window": ("ISW1990.bulk-arc-off-scale",
                          "ISW1990.table1-capacitance-interpretation",
                          "VADHVA2021.in-li-full-cell-assignment"),
    # 저주파 끝 — 막는가
    "tail_mimicked_by_arc": ("ISW1990.blocking-electrode-spike",
                             "HIRSCHORN2010.brug-surface-blocking-eq12"),
    "open_end_on_blocking_cell": ("ISW1990.blocking-electrode-spike",
                                  "VADHVA2021.blocking-cell-circuit-r0-offset"),
    "blocking_element_on_open_cell": ("ISW1990.no-spike-means-electronic",
                                      "VADHVA2021.electrode-types"),
    "symmetric_cell_does_not_block": ("ISW1990.no-spike-means-electronic",
                                      "VADHVA2021.electrode-types"),
    "cpe_like_diffusion": ("LASIA1999.cpe-exponent-limits",
                           "ISW1990.diffusion-spike-45-degrees"),
    # 곡선이 점을 지나가나
    "misfit_everywhere": ("LASIA1999.residuals-should-be-random",),
    "misfit_somewhere": ("LASIA1999.residuals-should-be-random",),
    "misfit_at_edge": ("LASIA1999.residuals-should-be-random",),
    "inductance_missing": ("LASIA1999.impedance-range-artefacts",),
    # 온도 스캔
    "sweep_unlike_its_neighbours": ("ISW1990.blocking-electrode-spike",),
    "short_rest_before_sweep": ("VADHVA2021.relax-to-ocp-before-eis",
                                "LASIA1999.stationarity-repeat-and-up-down-scans"),
    "first_sweep_suspect": ("LASIA1999.stationarity-repeat-and-up-down-scans",),
    "sweep_off_the_line": ("ISW1990.arrhenius-format",
                           "ISW1990.bulk-and-gb-have-different-activation",
                           "LASIA1999.stationarity-repeat-and-up-down-scans"),
    # 스펙트럼 자체 — Kramers–Kronig (ADR 0043)
    "kk_violation": ("VADHVA2021.kk-validation-before-modelling",
                     "SCHOENLEBER2014.residuals",
                     "SCHOENLEBER2014.no-numeric-residual-threshold"),
    "kk_outlier": ("LASIA1999.kk-linear-voigt-test", "SCHOENLEBER2014.residuals"),
    "kk_high_frequency": ("LASIA1999.impedance-range-artefacts",
                          "SCHOENLEBER2014.optional-series-c-l"),
    "kk_noisy": ("SCHOENLEBER2014.residuals",
                 "SCHOENLEBER2014.no-numeric-residual-threshold"),
    "low_frequency_inductive": ("VADHVA2021.qss-low-frequency-cutoff",
                                "LASIA1999.low-frequency-pseudo-inductive-loop"),
    # 기록
    "amplitude_large": ("VADHVA2021.small-amplitude-linearity",
                        "LASIA1999.linearity-amplitude-limit"),
}

#: 진공의 유전율 (F/cm) — 겉보기 εr = C·l/(A·ε0) (``ISW1990.bulk-capacitance-unit-cell-constant``).
EPS0_F_PER_CM = 8.8541878128e-14
#: 교류 진폭이 이보다 크면 선형 범위를 의심한다 — "typically <50 mV"
#: (``VADHVA2021.small-amplitude-linearity``).
AMPLITUDE_LIMIT_MV = 50.0


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str

    @property
    def label(self) -> str:
        return SEVERITY_LABELS.get(self.severity, self.severity)

    @property
    def refs(self) -> tuple[str, ...]:
        """The knowledge records this kind of finding rests on (``REFERENCES``)."""
        return REFERENCES.get(self.code, ())


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


#: 펠릿·코인 셀의 면적이 이만큼(cm²) 넘으면 지름(mm)을 면적 칸에 적었는지
#: 묻는다.  실측: 같은 조건의 두 셀 중 하나만 "면적 10 cm²" 였다 (10 mm 셀 —
#: 옳게 적은 짝은 0.785 cm²).  20 cm² 를 넘으면 셀의 면적이 아니다.
LARGE_AREA_CM2 = 5.0


def audit_record(*, name: str, kind: str, config: str = "",
                 thickness_um: float | None = None, area_cm2: float | None = None,
                 n_points: int | None = None, file_name: str = "",
                 amplitude_mv: float | None = None) -> list[Finding]:
    """What was written about the measurement, before any fit is looked at.

    ``name`` is what the screen shows, ``file_name`` what was uploaded.  A
    hint in the shown name that disagrees with the record is worth a look; a
    hint only in the file name is usually a file named before the cell was
    re-labelled, so it is only noted -- **with the file name**, because "the
    name says full" next to a name that says ``sym`` reads like a bug
    (실측 2026-09-23: 화면 이름은 ``…_sym_#01`` 인데 "이름은 풀셀" 이 떴다).
    """
    out: list[Finding] = []
    if amplitude_mv is not None and amplitude_mv > AMPLITUDE_LIMIT_MV:
        out.append(Finding(NOTE, "amplitude_large",
                           f"교류 진폭이 {amplitude_mv:g} mV 입니다 — 보통 "
                           f"{AMPLITUDE_LIMIT_MV:g} mV 미만으로 잰다 (선형 범위). KK 잔차가 "
                           f"크면 이것부터 의심하세요"))
    if n_points is not None and n_points < FEWEST_POINTS:
        out.append(Finding(CHECK, "few_points",
                           f"점이 {n_points}개뿐입니다 — 회로 파라미터보다 점이 "
                           f"모자라면 무엇을 맞춰도 값이 정해지지 않습니다"))
    if kind == SOLID and not config:
        out.append(Finding(CHECK, "config_missing",
                           "전고체인데 셀 구성이 비어 있습니다 — 아크를 벌크·입계로도 "
                           "계면으로도 부르지 못하고, 전도도도 안 나옵니다"))
    if (kind, config) == (SOLID, SYMMETRIC) and (not thickness_um or not area_cm2):
        missing = ("두께·면적이" if not thickness_um and not area_cm2
                   else "두께가" if not thickness_um else "면적이")
        out.append(Finding(NOTE, "geometry_missing",
                           f"대칭셀인데 {missing} 없습니다 — σ 도, 커패시턴스로 아크 "
                           f"이름을 검사하는 것도 안 나옵니다"))
    shown_config = config_from_name(name)
    file_config = config_from_name(file_name) if file_name else None
    now = _CONFIG_WORDS.get(config or "", config)
    if shown_config and shown_config != (config or ""):
        out.append(Finding(CHECK, "config_differs_from_name",
                           f"이름은 {_CONFIG_WORDS[shown_config]}인데 셀 구성은 "
                           f"{now}입니다"))
    elif file_config and file_config != (config or "") and not shown_config:
        out.append(Finding(CHECK, "config_differs_from_name",
                           f"원본 파일 이름({file_name})은 {_CONFIG_WORDS[file_config]}"
                           f"인데 셀 구성은 {now}입니다"))
    elif file_config and file_config != (config or ""):
        out.append(Finding(NOTE, "file_name_differs",
                           f"원본 파일 이름({file_name})은 "
                           f"{_CONFIG_WORDS[file_config]}입니다 — 이름을 고쳐 둔 "
                           f"것이면 그대로 두세요"))
    named = thickness_from_name(name) or (thickness_from_name(file_name)
                                          if file_name else None)
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
    if area_cm2 is not None and (area_cm2 < low or area_cm2 >= LARGE_AREA_CM2):
        as_diameter = math.pi * (area_cm2 / 10.0) ** 2 / 4.0
        hint = (f" — 지름 {area_cm2:g} mm 를 적은 것이면 {as_diameter:.3g} cm² 입니다"
                if area_cm2 >= LARGE_AREA_CM2 else " — mm² 로 적었는지 보세요")
        out.append(Finding(CHECK, "area_out_of_range" if not low <= area_cm2 <= high
                           else "area_looks_like_diameter",
                           f"면적 {area_cm2:g} cm² 는 펠릿·코인 셀의 면적으로 "
                           f"{'맞지 않습니다' if area_cm2 < low else '큽니다'}{hint}"))
    return out


# --------------------------------------------------------------------------
# the fit
# --------------------------------------------------------------------------

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
    if kind == "CPE" and suffix == "n" and side == "lower":
        return Finding(CHECK, "at_bound",
                       f"{element} 의 n 이 하한({shown})에 붙었습니다 — 반원도 꼬리도 "
                       f"아닌, 모양이 정해지지 않은 소자입니다")
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


def _compatible(alternatives: Iterable[str], ends: set[str], current: str, *,
                arcs: int | None = None, exact: bool = False) -> list[str]:
    """The offered circuits whose low-frequency end is one of ``ends``, best first.

    Best is: a cable inductor in it (the lab's sulfide pellets were off by
    11–30 % at the top of the band without one), then the arc count closest to
    ``arcs`` (the arcs worth keeping), then the smaller circuit.  ``exact``
    keeps only that many arcs.  In offered order the first blocking circuit had
    no inductor: 27 of the lab's tail-mimicking fits were told to go to it.
    """
    ranked: list[tuple[tuple, int, str]] = []
    for position, alternative in enumerate(alternatives):
        try:
            model = parse_circuit(alternative)
            end = circuit_end(model)
        except CircuitError:
            continue
        if end not in ends or alternative == current or \
                alternative in [one for _, _, one in ranked]:
            continue
        kinds = {name.partition("_")[0].rstrip("0123456789")
                 for name in model.parameter_names}
        distance = abs(len(model.capacitive_arcs()) - arcs) if arcs is not None else 0
        if exact and distance:
            continue
        ranked.append(((0 if "L" in kinds else 1, distance,
                        len(model.parameter_names)), position, alternative))
    return [one for _, _, one in sorted(ranked)]


def _arcs_to_keep(arcs: Sequence[ArcCapacitance], claims: dict[str, str | None],
                  statuses: dict[str, str], drop: set[str]) -> int:
    """How many arcs a refit should keep: not ``drop`` (a cause explained them
    away), and not an arc named bulk / grain boundary whose capacitance is the
    electrode's -- the refit would give it the same wrong name (the names go
    by position, `derive.label_arcs`)."""
    undetermined = {name for name, status in statuses.items() if status == "undetermined"}
    keep = 0
    for arc in arcs:
        if arc.resistor in drop:
            continue
        if claims.get(arc.resistor) in ("bulk", "grain_boundary") and \
                size_class(arc, spread=spread_for(arc, undetermined)) == FACE:
            continue
        keep += 1
    return keep


def _suggest(candidates: Iterable[str], limit: int = 3) -> str:
    """```a` 또는 `b``` -- at most ``limit``, first come first."""
    unique = list(dict.fromkeys(c for c in candidates if c))[:limit]
    return " 또는 ".join(f"`{c}`" for c in unique)


def _series_resistance(model: Circuit, values: dict[str, float]) -> float | None:
    """The plain resistances in the top-level series path, added up."""
    names = [name for name, kind in model.series_element_kinds() if kind == "R"]
    if not names:
        return None
    return float(sum(values[name] for name in names))


#: 미결정 파라미터로 만든 커패시턴스라도 이름이 말하는 범위에서 이만큼(배)
#: 넘게 떨어져 있으면 판정한다.  미결정의 문턱은 값이 세 배 흔들리거나 오차
#: 막대가 50 % 인 것이다 — Q 가 세 배 흔들리면 C_eff 는 3^{1/n} 배(n=0.87
#: 에서 3.5 배)라 한 자릿수면 그 흔들림을 넉넉히 넘는다.  실측 B11 스캔의
#: "벌크" 들은 벌크 상한의 수만 배였고 전부 미결정이라 판정에서 빠졌었다.
FAR_OUTSIDE = UNDETERMINED_SPREAD


def _distance_outside(arc: ArcCapacitance, claim: str) -> float | None:
    """How many times outside the claimed process's range the arc sits
    (``1.0`` = on the boundary), or ``None`` when it cannot be said."""
    row = process(claim)
    value = arc.per_length if row.scaling == "thickness" else arc.per_area
    if value is None or value <= 0:
        return None
    if row.high is not None and value >= row.high:
        return value / row.high
    if row.low is not None and value < row.low:
        return row.low / value
    return 1.0


def _is_railed_arc(arc: ArcCapacitance, railed: dict[str, str]) -> bool:
    names = [arc.resistor, f"{arc.element}_Q", f"{arc.element}_n", arc.element]
    return any(railed.get(name) in ("lower", "upper") for name in names
               if not name.endswith("_n"))


def audit_fit(fit, spectrum: Spectrum | None, *, kind: str, config: str = "",
              thickness_cm: float | None = None, area_cm2: float | None = None,
              band: tuple[float, float] | None = None,
              conductivity: dict | None = None,
              alternatives: Sequence[str] = ()) -> FitAudit:
    """Every check one stored fit can be put through.

    ``band`` is the frequency window the fit used (its misfit is measured
    there, and an arc apex outside it was extrapolated).  ``conductivity`` is
    what ``ionic_conductivity`` gave for it, when it was asked.
    ``alternatives`` are the circuits offered for this kind of cell (the API's
    presets); a finding that says "use another circuit" picks from them the
    ones whose low-frequency end matches what the spectrum does.

    **One cause, one finding.**  The first version reported the lab's blocking
    pellets three times over -- "the circuit closes on the real axis", "R1
    cannot be bulk", "R1's apex is below the window" -- for one fact: the arc
    was the blocking tail in disguise.  131 real spectra produced 90 checks
    that way (2026-09-23).  Causes that explain several symptoms are named
    once, and the symptoms they explain are not repeated.
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
    series_kinds = model.series_element_kinds()
    in_series = {name for name, _ in series_kinds}
    railed = {p.name: _railed(p, model) for p in parameters}
    r0 = _series_resistance(model, values)
    low_edge = band[0] if band is not None and band[0] is not None else None
    high_edge = band[1] if band is not None and band[1] is not None else None

    # -- 아크와 그 이름 ---------------------------------------------------------
    arcs = arc_capacitances(model, values, thickness_cm=thickness_cm,
                            area_cm2=area_cm2)
    try:
        labels = {meaning.parameter: meaning.label
                  for meaning in label_arcs(fit, kind, config)}
    except ValueError:
        # 모르는 종류·구성 — 이름이 없으면 이름을 검사할 것도 없다.
        labels = {}
    series_r = {name for name, element_kind in series_kinds if element_kind == "R"}
    arc_order = [name for name in labels if name not in series_r]
    expected = EXPECTED_PROCESSES.get((kind, config))
    claims: dict[str, str | None] = {}
    for arc in arcs:
        position = arc_order.index(arc.resistor) if arc.resistor in arc_order else None
        claim = None
        if expected is not None and position is not None:
            claim = expected[min(position, len(expected) - 1)]
        claims[arc.resistor] = claim
        out.arcs.append(_arc_row(arc, labels.get(arc.resistor, ""), claim))

    #: 한 원인으로 묶인 아크 — 그 아크의 증상은 따로 적지 않는다.
    explained: set[str] = set()
    #: 한 원인으로 설명된 파라미터 — 경계에 붙은 것을 따로 적지 않는다.
    quiet: set[str] = set()

    # -- 사라진 아크 -------------------------------------------------------------
    # 저항이 0 인 아크는 아크가 아니다: 꼭지(f₀ = 1/2πRC)도, 커패시턴스의 이름도,
    # 옆 CPE 의 n 도 뜻이 없다 — "R 이 0" 한 줄이 전부다.  맞춤의 경계 판정(1 %)을
    # 비껴간 것까지: 실측 R1 = 1.13e-9 Ω 인 아크에 "꼭지 3.6e19 Hz 가 맞춘 구간
    # 위 — 반원의 꼭대기를 못 보고 정한 저항" 이 붙었다.
    floor = 0.0
    if spectrum is not None and len(spectrum):
        magnitude = np.abs(_band(spectrum, band).z)
        magnitude = magnitude[np.isfinite(magnitude) & (magnitude > 0)]
        floor = VANISHED_ARC_SHARE * float(magnitude.min()) if magnitude.size else 0.0
    # 옆 CPE 의 Q 가 경계에 붙은 것은 그 결과다 — 0 Ω 이 가린 소자는 어디로든 간다.
    vanished = [arc for arc in arcs if railed.get(arc.resistor) == "lower"
                or arc.resistance_ohm < floor]
    for arc in vanished:
        explained.add(arc.resistor)
        quiet.update({f"{arc.element}_Q", f"{arc.element}_n", arc.element})
        if railed.get(arc.resistor) != "lower":
            out.findings.append(_rail_finding(arc.resistor, arc.resistance_ohm,
                                              "lower", in_series=False))
        for row in out.arcs:
            if row["resistor"] == arc.resistor:
                row.update(candidates=None, candidate_labels=None,
                           reason="저항이 0 이라 아크가 아닙니다")

    # -- 곡선이 점을 지나가나 --------------------------------------------------
    verdict: dict = {}
    if spectrum is not None and len(spectrum):
        summary, fitted, used = misfit(spectrum, model, values, band)
        out.misfit = summary
        verdict = blocking_verdict(spectrum.frequency_hz, spectrum.z_re, spectrum.z_im)
        out.blocking = verdict
        if summary is not None:
            _misfit_findings(out, summary, used, fitted, model, series_kinds,
                             high_edge)

    blocking = verdict.get("blocking")
    phase = verdict.get("phase_deg")
    sym_solid = (kind, config) == (SOLID, SYMMETRIC)

    # -- 막는 셀인가, 회로도 그렇게 말하나 -------------------------------------
    blockers = [name for name, element_kind in series_kinds
                if element_kind in BLOCKING_KINDS]
    if blocking is False and blockers:
        # 실수축으로 돌아오는 끝만 권한다 — 반무한 W 도 -45° 로 끝없이 발산해
        # 돌아오지 않는다 (``LASIA1999.semi-infinite-warburg``).
        suggestion = _suggest([_suggest_without(fit.circuit, blockers)]
                              + _compatible(alternatives, {"resistive"}, fit.circuit,
                                            arcs=len(arcs)))
        out.findings.append(Finding(
            PROBLEM, "blocking_element_on_open_cell",
            f"스펙트럼은 저주파에서 실수축으로 내려오는데 (위상 {_deg(phase)}) "
            f"회로 끝에 막는 소자 {', '.join(blockers)} 가 있습니다 — 맞춤이 그 "
            f"소자를 지우려고 경계로 갑니다"
            + (f". {suggestion} 로 다시 맞추세요" if suggestion else "")))
        # 그 소자의 경계 붙음은 이 한 줄이 설명한다.
        quiet.update(name for name in model.parameter_names
                     if name.partition("_")[0] in blockers)

    if blocking is True and out.end == "resistive":
        tail = _tail_arc(arcs, low_edge, railed)
        # 꼬리를 흉내 낸 아크는 아크가 아니다 — 권하는 회로는 그만큼 아크가 적다.
        suggestion = _suggest(_compatible(
            alternatives, {"blocking"}, fit.circuit,
            arcs=_arcs_to_keep(arcs, claims, statuses,
                               {arc.resistor for arc in vanished}
                               | ({tail.resistor} if tail is not None else set()))))
        if tail is not None:
            explained.add(tail.resistor)
            quiet.update({tail.resistor, f"{tail.element}_Q", f"{tail.element}_n",
                          tail.element})
            label = labels.get(tail.resistor, "")
            where = (f"꼭지 {tail.peak_hz:.3g} Hz 가 맞춘 구간(≥ {low_edge:.3g} Hz) "
                     f"아래이고" if tail.peak_hz is not None and low_edge is not None
                     and tail.peak_hz < low_edge else
                     f"저항이 상한({tail.resistance_ohm:.3g} Ω)에 붙었고")
            double_layer = _blocking_capacitance(tail, arcs, r0, railed)
            per_area = (double_layer / area_cm2 if double_layer is not None
                        and area_cm2 and area_cm2 > 0 else None)
            size = (f", 막는 계면의 커패시턴스 {_fmt(double_layer, 'F')} (C/A "
                    f"{_fmt(per_area, 'F/cm²')}) 는 전극 이중층의 크기입니다"
                    if per_area is not None and per_area >= 1e-7 else "")
            electrolyte = (f". 이 셀의 전해질 저항은 고주파 절편 R0 = {r0:.4g} Ω 입니다"
                           if sym_solid and r0 is not None else "")
            out.findings.append(Finding(
                PROBLEM, "tail_mimicked_by_arc",
                f"{tail.resistor}" + (f" ({label})" if label else "")
                + f" 은 반원이 아니라 블로킹 꼬리(위상 {_deg(phase)})를 흉내 낸 "
                f"것입니다 — {where}{size}{electrolyte}"
                + (f". {suggestion} 로 다시 맞추세요" if suggestion
                   else ". 끝에 CPE 를 달아 다시 맞추세요")))
        else:
            out.findings.append(Finding(
                CHECK, "open_end_on_blocking_cell",
                f"스펙트럼은 저주파에서 수직으로 서는데 (위상 {_deg(phase)}) 회로의 "
                f"저주파 끝이 실수축으로 닫힙니다 — 마지막 아크가 꼬리를 흉내 "
                f"냅니다" + (f". {suggestion} 로 다시 맞추세요" if suggestion
                             else ". 끝에 CPE 를 달아 보세요")))

    # 막는 대칭셀에서 벌크·입계라 부른 아크 중 **벌크 크기가 하나도 없으면**
    # 벌크 반원은 잰 주파수 위에 있고 그 저항은 고주파 절편에 들어 있다 —
    # Irvine–Sinclair–West 그림 4b 의 읽기다.  황화물 펠릿에서 흔하다: 실측
    # B11–B14·B7 스캔 44개 스윕은 두 아크가 모두 전극 쪽(이중층) 크기였다.
    if sym_solid and blocking is True:
        hidden = _hidden_bulk(arcs, claims, statuses, railed, explained)
        if hidden is not None:
            face, boundary = hidden
            for arc in face + boundary:
                explained.add(arc.resistor)
                quiet.update({arc.resistor, f"{arc.element}_Q", f"{arc.element}_n",
                              arc.element})
            crossing = (real_axis_crossing(spectrum.frequency_hz, spectrum.z_re,
                                           spectrum.z_im)
                        if spectrum is not None and len(spectrum) else None)
            # 전극 쪽 아크를 남기면 다시 맞춰도 같은 이름(벌크·입계)이 붙는다 —
            # 이름이 맞는 것은 아크가 없는 회로다.  아크가 정말 보이는 셀에는
            # 아크 하나짜리를 따로 적는다.
            out.findings.append(_hidden_bulk_finding(
                face, boundary, labels, r0, crossing,
                _suggest(_compatible(alternatives, {"blocking"}, fit.circuit,
                                     arcs=0, exact=True)),
                _suggest(_compatible(alternatives, {"blocking"}, fit.circuit,
                                     arcs=1, exact=True), limit=1)))

    if sym_solid and blocking is False and arcs:
        out.findings.append(Finding(
            CHECK, "symmetric_cell_does_not_block",
            "이 대칭셀은 이온을 막지 않습니다 — 벌크·입계 σ 가 나올 수 없는 "
            "측정입니다. 2026-09-23 전 화면은 σ 를 냈으므로, 슬라이드에 옮긴 "
            "값이 있으면 다시 보세요"))

    # -- 경계에 붙은 것, 미결정, 옛 행 -----------------------------------------
    # **사라지려는 소자의 나머지 파라미터는 말하지 않는다.**  CPE 의 Q 가
    # 상한에 붙으면 그 임피던스는 n 과 상관없이 0 이고, n 은 아무 데나 떠서
    # 경계에 붙는다 — 그것을 따로 적으면 한 가지 사실이 세 줄이 된다 (합성
    # 쌍둥이에서 "Q 상한" · "n 하한" · "n = 0.30 확산" 이 함께 떴다).
    vanishing = {name.partition("_")[0] for name, side in railed.items()
                 if (side == "upper" and name.endswith("_Q"))}
    for parameter in parameters:
        side = railed.get(parameter.name, "")
        element, _, suffix = parameter.name.partition("_")
        if not side or parameter.name in quiet or (element in vanishing
                                                   and suffix != "Q"):
            continue
        out.findings.append(_rail_finding(
            parameter.name, float(parameter.value), side,
            in_series=element in in_series))
    for name in model.parameter_names:
        element, _, suffix = name.partition("_")
        if suffix != "n" or not element.startswith("CPE") or element in vanishing \
                or name in quiet or values[name] > LOWEST_N:
            continue
        if railed.get(name) == "lower":
            continue            # 경계 붙음이 이미 같은 말을 했다
        if element in in_series:
            message = (f"{element} 의 n = {values[name]:.2f} — 막는 꼬리(수직)가 아니라 "
                       f"확산 꼬리(45°)에 가깝습니다")
        else:
            message = (f"{element} 의 n = {values[name]:.2f} — 반원이 아니라 확산에 "
                       f"가깝습니다. 그 아크의 저항을 계면·입계 저항으로 읽기 "
                       f"어렵습니다")
        out.findings.append(Finding(CHECK, "cpe_like_diffusion", message))
    undetermined = [name for name in model.parameter_names
                    if statuses.get(name) == "undetermined" and name not in quiet]
    if undetermined:
        out.findings.append(Finding(NOTE, "undetermined",
                                    "미결정 파라미터: " + ", ".join(undetermined)))
    if any(statuses.get(name) == "legacy_unknown" for name in model.parameter_names):
        out.findings.append(Finding(NOTE, "legacy_fit",
                                    "판정 기록이 없는 옛 맞춤입니다 — `bml reparse` "
                                    "가 같은 회로로 다시 맞춥니다"))

    # -- 아크 하나하나 -----------------------------------------------------------
    for arc in arcs:
        if arc.resistor in explained:
            continue
        _arc_findings(out, arc, labels.get(arc.resistor, ""), claims.get(arc.resistor),
                      statuses, railed, low_edge, high_edge)

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


#: 가장 크게 어긋난 점이 맞춘 구간의 꼭대기 이만큼(비율) 안에 있으면 "고주파
#: 끝에서" 어긋난 것으로 본다 — 한 칸(10 점/decade 면 1.26 배)보다 넉넉히.
_TOP_OF_BAND = 0.5


def _misfit_findings(out: FitAudit, summary: Misfit, used: Spectrum,
                     fitted: np.ndarray, model: Circuit,
                     series_kinds: list[tuple[str, str]],
                     high_edge: float | None) -> None:
    edge = edge_misfit(used.frequency_hz, used.z, fitted, len(model.parameter_names))
    top = float(np.max(used.frequency_hz)) if len(used) else high_edge
    at_top = top is not None and summary.at_hz >= _TOP_OF_BAND * top
    has_l = any(kind == "L" for _, kind in series_kinds)
    if summary.mean >= MEAN_MISFIT_LIMIT:
        out.findings.append(Finding(
            CHECK, "misfit_everywhere",
            f"맞춤이 평균 {summary.mean * 100:.1f} % 어긋납니다 — 회로가 이 "
            f"스펙트럼의 모양을 못 그립니다 (최대 {summary.max * 100:.0f} %, "
            f"{summary.at_hz:.3g} Hz)"))
    # 가장 크게 어긋난 곳이 **고주파 끝**이고 회로에 인덕턴스가 없으면 원인이
    # 거의 정해져 있다: 케이블·셀 홀더의 인덕턴스가 그 점들을 휘게 하고, 빼낸
    # 유도성 점 바로 아래가 이미 휘어 있다.  실측: 같은 스캔의 L1 있는 첫 스윕은
    # 최대 1.4–3.7 %, 없는 나머지는 11–30 % 였다 (B15–B17, 2026-09-23).
    if at_top and not has_l and summary.max >= MAX_MISFIT_LIMIT:
        out.findings.append(Finding(
            CHECK, "inductance_missing",
            f"가장 크게 어긋난 곳({summary.max * 100:.0f} %)이 맞춘 구간의 고주파 "
            f"끝 {summary.at_hz:.3g} Hz 입니다 — 회로에 배선 인덕턴스가 없습니다. "
            f"앞에 `L1-` 를 붙여 다시 맞춰 보세요"))
        return
    # 오차가 **몰렸다**는 것만으로는 적지 않는다.  거의 완벽한 맞춤도 가장 작은
    # 오차들이 어딘가에는 몰려 있다 — 실측 셀의 합성 쌍둥이(최대 0.07 %)에서
    # "98 % 가 저주파에" 가 떴다.
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


def _tail_arc(arcs: list[ArcCapacitance], low_edge: float | None,
              railed: dict[str, str]) -> ArcCapacitance | None:
    """The arc that is really the blocking tail: the slowest one, when its
    apex is below the fitted window or its resistance went to the bound.

    Inside the window an interface-sized arc can be a real interphase with the
    tail simply missing from the circuit -- that is ``open_end_on_blocking_cell``,
    not this.
    """
    if not arcs:
        return None
    slowest = min(arcs, key=lambda arc: arc.peak_hz if arc.peak_hz is not None
                  else math.inf)
    below = (slowest.peak_hz is not None and low_edge is not None
             and slowest.peak_hz < low_edge)
    open_branch = railed.get(slowest.resistor) == "upper"
    return slowest if (below or open_branch) else None


def _blocking_capacitance(tail: ArcCapacitance, arcs: list[ArcCapacitance],
                          r0: float | None, railed: dict[str, str]) -> float | None:
    """The capacitance of the blocking interface an arc was mimicking, in F.

    A blocking interface is an ohmic resistance in series with a CPE, and its
    capacitance is Brug's -- Hirschorn et al., *Electrochim. Acta* 55, 6218
    (2010), Eq. (12) (``HIRSCHORN2010.brug-surface-blocking-eq12``):
    ``C = Q^{1/n} · R_e^{(1-n)/n}`` with the **ohmic** resistance ``R_e``.  The arc's own resistance is the wrong one: it is the
    fit's bound or an extrapolation, and with ``n < 1`` the number follows it
    (17 times too large at ``n = 0.85`` for 1e9 Ω against 100 Ω).  ``R_e`` is
    what is in series before the tail -- R0 and the faster arcs, which are
    plain resistors at the tail's frequencies.  That sum is our reading; the
    paper's circuit has a single ``R_e``.
    """
    if tail.n < LOWEST_N:
        return None
    faster = sum(arc.resistance_ohm for arc in arcs
                 if arc is not tail and railed.get(arc.resistor) != "upper")
    r_e = (r0 or 0.0) + faster
    return effective_capacitance(r_e, tail.q, tail.n) if r_e > 0 else None


def _hidden_bulk(arcs: list[ArcCapacitance], claims: dict[str, str | None],
                 statuses: dict[str, str], railed: dict[str, str],
                 explained: set[str]
                 ) -> tuple[list[ArcCapacitance], list[ArcCapacitance]] | None:
    """``(face, boundary)`` -- the arcs named bulk / grain boundary, split by
    what their capacitance says, when **none** of them can be the bulk;
    otherwise ``None`` (the names are then checked arc by arc).

    Each arc's side has to hold when its capacitance moves by the formula's
    own uncertainty, or by an undetermined value's (``size_class`` /
    ``spread_for``) -- the same rule `ionic_conductivity` uses to put R0 into
    the electrolyte, so the report and the number say the same thing.  실측
    B14 #9: "입계" 아크는 n 만 미결정(상한)인 이상적 축전기로 입계 상한의
    9.9 배, "벌크" 는 4 만 배 — 둘 다 전극 쪽이다.
    """
    claimed = [arc for arc in arcs if claims.get(arc.resistor) in ("bulk", "grain_boundary")
               and arc.resistor not in explained]
    if not claimed:
        return None
    undetermined = {name for name, status in statuses.items() if status == "undetermined"}
    face: list[ArcCapacitance] = []
    boundary: list[ArcCapacitance] = []
    for arc in claimed:
        if railed.get(arc.resistor) == "upper":
            return None
        side = size_class(arc, spread=spread_for(arc, undetermined))
        if side is None or side == BULK:
            return None
        (face if side == FACE else boundary).append(arc)
    return face, boundary


def _hidden_bulk_finding(face: list[ArcCapacitance], boundary: list[ArcCapacitance],
                         labels: dict[str, str], r0: float | None,
                         crossing: float | None, suggestion: str,
                         with_arc: str = "") -> Finding:
    def named(arc: ArcCapacitance) -> str:
        label = labels.get(arc.resistor, "")
        return f"{arc.resistor}" + (f" ({label})" if label else "")

    where = (f" (실수축 교점 {crossing:.4g} Ω)" if crossing is not None else "")
    if not boundary:
        listed = ", ".join(f"{named(arc)} C/A {_fmt(arc.per_area, 'F/cm²')}"
                           for arc in face)
        return Finding(
            PROBLEM, "arcs_are_electrode",
            f"벌크·입계라 부른 아크가 모두 전극 쪽 크기입니다 — {listed}. "
            f"벌크·입계 아크는 잰 주파수 위에 있어 고주파 절편에 들어 있습니다"
            + (f": 전해질 저항 ≈ R0 = {r0:.4g} Ω" if r0 is not None else "")
            + where + ". 이 아크들로 낸 벌크·입계 σ 는 쓰지 마세요"
            + (f"; {suggestion} 로 다시 맞추면 이름이 맞습니다" if suggestion
               else "")
            + (f". 꼬리 앞에 아크가 정말 보여 그것으로 안 그려지면 {with_arc} — "
               f"그 아크는 전극 계면입니다 (화면의 σ 는 이미 R0 로 냅니다)"
               if suggestion and with_arc else ""))
    sides = ([f"{named(arc)} 는 입계 쪽(C·l/A {_fmt(arc.per_length, 'F/cm')})"
              for arc in boundary]
             + [f"{named(arc)} 는 전극 쪽(C/A {_fmt(arc.per_area, 'F/cm²')})"
                for arc in face])
    total = (r0 + sum(arc.resistance_ohm for arc in boundary)
             if r0 is not None else None)
    parts = " + ".join(["R0"] + [arc.resistor for arc in boundary])
    return Finding(
        PROBLEM, "bulk_above_window",
        "벌크 크기의 아크가 없습니다 — 벌크 반원은 잰 주파수 위에 있어 고주파 "
        "절편 R0 에 들어 있습니다 (Irvine–Sinclair–West 그림 4b 의 읽기). "
        + ", ".join(sides)
        + (f": 전해질 저항 ≈ {parts} = {total:.4g} Ω" if total is not None else "")
        + where + ". 이름대로 낸 벌크 σ 는 쓰지 마세요")


def _arc_row(arc: ArcCapacitance, label: str, claim: str | None) -> dict:
    return {
        "resistor": arc.resistor, "element": arc.element, "label": label,
        "resistance_ohm": arc.resistance_ohm, "q": arc.q, "n": arc.n,
        "capacitance_f": arc.capacitance_f, "peak_hz": arc.peak_hz,
        "per_length": arc.per_length, "per_area": arc.per_area,
        "permittivity": (arc.per_length / EPS0_F_PER_CM
                         if arc.per_length is not None else None),
        "candidates": list(arc.candidates) if arc.candidates is not None else None,
        "candidate_labels": ([process(key).label for key in arc.candidates]
                             if arc.candidates is not None else None),
        "claims": claim, "reason": arc.reason,
    }


def _arc_findings(out: FitAudit, arc: ArcCapacitance, label: str,
                  claim: str | None, statuses: dict[str, str],
                  railed: dict[str, str], low: float | None,
                  high: float | None) -> None:
    # 경계에 붙은 아크의 꼭지는 뜻이 없다 — 경계 붙음이 이미 그 말을 했다
    # (실측: R2 = 1e9 Ω 인 아크마다 "꼭지가 1e-5 Hz" 가 한 줄 더 붙었다).
    # 반원이 아닌 것(n < 0.6)의 꼭지도 없다 — 목록이 이미 "판정 안 함" 이라
    # 적는 소자에 실측 여덟 건이 "반원의 꼭대기를 못 보고" 를 달았다.
    if arc.peak_hz is not None and arc.n >= LOWEST_N \
            and not _is_railed_arc(arc, railed):
        if high is not None and arc.peak_hz > high:
            out.findings.append(Finding(
                CHECK, "arc_apex_above_window",
                f"{arc.resistor} 아크의 꼭지(f₀ = {arc.peak_hz:.3g} Hz)가 맞춘 구간 "
                f"위(≤ {high:.3g} Hz)에 있습니다 — 반원의 꼭대기를 못 보고 정한 "
                f"저항입니다"))
        elif low is not None and arc.peak_hz < low:
            out.findings.append(Finding(
                CHECK, "arc_apex_below_window",
                f"{arc.resistor} 아크의 꼭지(f₀ = {arc.peak_hz:.3g} Hz)가 맞춘 구간 "
                f"아래(≥ {low:.3g} Hz)에 있습니다 — 반원이 닫히는 것을 못 보고 정한 "
                f"저항입니다"))
    if claim is None or arc.candidates is None or _is_railed_arc(arc, railed):
        return
    if claim in arc.candidates:
        return
    names = [arc.resistor]
    names += ([f"{arc.element}_Q", f"{arc.element}_n"] if arc.element_kind == "CPE"
              else [arc.element])
    shaky = [name for name in names if statuses.get(name) == "undetermined"]
    distance = _distance_outside(arc, claim)
    if shaky and (distance is None or distance < FAR_OUTSIDE):
        out.findings.append(Finding(
            NOTE, "capacitance_not_judged",
            f"{arc.resistor} 아크는 {', '.join(shaky)} 가 미결정이라 커패시턴스로 "
            f"이름을 검사하지 않았습니다"))
        return
    allowed = " 또는 ".join(process(key).label for key in arc.candidates)
    # 벌크라는 이름에는 누구나 확인할 수 있는 수가 하나 더 있다: 겉보기 유전율.
    # 비강유전체 벌크는 ~10, 10³–10⁵ 는 강유전체뿐이다 (Irvine–Sinclair–West).
    permittivity = (f" — 겉보기 εr ≈ {arc.per_length / EPS0_F_PER_CM:.2g} (벌크라면 "
                    f"~10, 10³–10⁵ 는 강유전체뿐입니다)"
                    if claim == "bulk" and arc.per_length is not None else "")
    out.findings.append(Finding(
        PROBLEM, "label_contradicts_capacitance",
        f"{arc.resistor} ({label}) 의 커패시턴스 {_fmt(arc.capacitance_f, 'F')} "
        f"(C·l/A {_fmt(arc.per_length)}, C/A {_fmt(arc.per_area, 'F/cm²')}) 는 "
        f"{process(claim).label}일 수 없습니다 — "
        + (f"{allowed}의 크기입니다" if allowed else "표의 어느 범위에도 안 듭니다")
        + permittivity
        + (" (미결정 값이지만 범위에서 한 자릿수 넘게 벗어납니다)" if shaky else "")))


# --------------------------------------------------------------------------
# the spectrum itself: Kramers–Kronig (ADR 0043)
# --------------------------------------------------------------------------

#: KK 잔차(|Z| 대비)가 이만큼 넘고 **그리고** 잡음의 ``KK_NOISE_MULTIPLE`` 배도
#: 넘어야 어긋남으로 본다.  논문에는 수치 기준이 없다
#: (``SCHOENLEBER2014.no-numeric-residual-threshold``) — 우리 합성 시험에서 KK 를
#: 만족하는 스펙트럼(잡음 0.1–0.5 %)은 최대 1.5 % 를 넘지 않았고, 한 점이 5 %
#: 튀면 4.0 %, 10 Hz 아래가 5 % 계단으로 바뀌면 2.8 % 였다.
KK_LIMIT = 0.02
#: 잡음만으로도 점 백 개의 최대는 σ 의 3.5–4 배다 — 여섯 배면 잡음이 아니다.
KK_NOISE_MULTIPLE = 6.0
#: μ 가 decade 당 이보다 성긴 곳에서 멈추고 잔차(rms)가 ``KK_LIMIT`` 를 넘으면
#: 그 결과로는 판정하지 않고 두 번째로 본다.  날카로운 아크(n = 1)나 참 저주파
#: 유도성 루프에서 μ 기준이 일찍 멈춘다 — 에이전트의 재현과 우리 시험에서 KK 를
#: 만족하는데 잔차가 25–71 % 였다 (M = 4, decade 당 0.5).
KK_EARLY_STOP_PER_DECADE = 1.5
#: 잡음 자체가 이만큼이면 따로 적는다 — 파라미터의 오차 막대가 그만큼 크다.
KK_NOISY = 0.01
#: 판정이 나오려 하거나 μ 가 일찍 멈추면 한 번 더 본다: 소자를 decade 당 이만큼
#: (그리고 μ 가 고른 수보다 적지 않게) 둔다.  논문의 IS1a 에서 μ 가 고른
#: 밀도(그림 8 에서 읽은 decade 당 2–4 개)의 가운데다.  소자가 모자라면 멀쩡한
#: 스펙트럼도 무효로 나온다 (``SCHOENLEBER2014.example-is1a-under-over-fit``) —
#: 실측 풀셀 꼴(합성, KK 만족)에서 μ 가 decade 당 1.4–2.2 개에서 멈춰 저주파
#: 끝이 2–5 % 어긋났고, 3 개로 보면 0.9 % 였다.
KK_SECOND_LOOK_PER_DECADE = 3.0
#: 두 번째로 볼 때 시정수를 대역 밖으로 이만큼(decade) 넓힌다 — 대역 아래로
#: 이어지는 CPE 꼬리(황화물 펠릿, n ≈ 0.88)의 가장 낮은 점이 2 % 어긋나던 것이
#: 0.8 % 가 된다.  10 Hz 아래 5 % 계단(2.7 %)과 10 % 드리프트(2.1–2.5 %)는
#: 그대로 걸린다.  매끄러운 5 % 드리프트는 이것 없이도 못 본다 (ADR 0043 비용).
KK_SECOND_LOOK_EXTEND = 0.25
#: 어긋난 구간이 꼭대기에서 이만큼(decade) 안이면 "고주파 끝" 이다 — 실측에서
#: 1.7–4.4 MHz (꼭대기 7 MHz 의 바로 아래)가 "가운데" 로 읽혀 "접촉이 바뀌었다"
#: 가 떴다.  저주파 끝은 가장 낮은 점을 품어야 끝이다: 드리프트는 가장 늦게 잰
#: 가장 낮은 점에서 가장 크다 (``SCHOENLEBER2014.drift-shows-at-low-frequency``).
#: 같은 반 decade 규칙을 아래에도 쓰자 실측 B13 #2 의 25–51 Hz (그 아래 10–20 Hz
#: 는 멀쩡) 가 "저주파 끝" 이 되어 하한 64 Hz 를 권했다.
KK_EDGE_DECADES = 0.5
#: 전류 범위가 바뀐 자리에서 이만큼(배) 안에 어긋난 구간이 닿으면 그 전환의
#: 흔적으로 본다 — decade 당 10 점이면 이웃 한 점까지다.
RANGE_SWITCH_REACH = 10.0 ** 0.15
#: 전환은 한 자리의 계단이다 — 어긋난 구간이 이보다(배) 넓거나 저주파 끝이면
#: 전환 하나로 설명하지 않는다.  실측 풀셀의 저주파 끝 0.01–1.6 Hz (두 decade)
#: 가 그 안의 전환(0.14 Hz) 때문에 "기기 탓" 참고로 내려갔다 — 드리프트일 수
#: 있는 것을.  이 기기는 전류가 한 decade 바뀔 때마다 범위를 바꿔, 넓은 구간
#: 안에는 거의 늘 전환이 하나 있다.
RANGE_SWITCH_SPAN = 10.0
#: 저주파 끝의 +Im 은 |Z| 의 이만큼은 넘어야 센다 — 실수축으로 내려온 셀의
#: 마지막 점들은 잡음만으로도 축 위에 설 수 있다.
LOW_FREQUENCY_INDUCTIVE_SHARE = 0.01


@dataclass
class SpectrumAudit:
    findings: list[Finding] = field(default_factory=list)
    #: 화면·보고서에 적을 KK 의 수 — ``judged`` 가 거짓이면 ``reason``.
    kk: dict = field(default_factory=dict)


def audit_spectrum(spectrum: Spectrum | None) -> SpectrumAudit:
    """What the points say before any circuit is fitted: the linear KK test.

    A spectrum that breaks Kramers–Kronig was not measured on a linear,
    time-invariant system -- a jump, a point that flew, a cell that changed
    under the sweep.  The finding says **where**, because that is what to cut
    from the fit.  Smooth drift spread over a decade is a different matter:
    the test cannot see it, and this does not pretend to (ADR 0043).
    """
    out = SpectrumAudit()
    if spectrum is None or not len(spectrum):
        out.kk = {"judged": False, "reason": "점이 없습니다"}
        return out
    inductive = _low_frequency_inductive(spectrum)
    if inductive is not None:
        count, below = inductive
        out.findings.append(Finding(
            CHECK, "low_frequency_inductive",
            f"가장 낮은 {count}개 점({below:.3g} Hz 아래)이 실수축 위(유도성)에 "
            f"있습니다 — 측정 중에 셀이 변했거나(쉬지 않은 셀, 드리프트), 흡착 "
            f"중간체의 느린 루프입니다. 이온을 막는 셀이면 앞의 것입니다"))
    result = lin_kk(spectrum.frequency_hz, spectrum.z_re, spectrum.z_im)
    out.kk, chosen = _kk_summary(result, spectrum)
    switches = _range_switches(spectrum)
    if switches:
        out.kk["range_switches_hz"] = switches
    if out.kk["judged"]:
        out.findings += _kk_findings(chosen, out.kk, switches)
    out.findings = sort_findings(out.findings)
    return out


def _range_switches(spectrum: Spectrum) -> list[float]:
    """Where the instrument changed its current range during the sweep -- the
    geometric mean of the two neighbouring frequencies, from EC-Lab's
    ``I Range`` column when the file carries it.

    A range change is a step in the gain and phase of the measurement, not of
    the cell, and it lands where ``|I| = amplitude / |Z|`` crosses a range
    boundary: 10 mV across the ~1 kΩ of a blocking pellet's tail near 100 Hz
    is 10 µA.  실측 두 번째 검수에서 황화물 펠릿 11 개가 64–410 Hz 에서 함께
    어긋났다 — 셀이 달라도, 온도가 달라도 같은 자리였다.
    """
    codes = (spectrum.columns or {}).get("I Range")
    if codes is None or len(codes) != len(spectrum):
        return []
    codes = np.asarray(codes)
    frequency = spectrum.frequency_hz
    return [float(np.sqrt(frequency[i] * frequency[i - 1]))
            for i in range(1, len(codes))
            if codes[i] != codes[i - 1] and frequency[i] > 0 and frequency[i - 1] > 0]


def _low_frequency_inductive(spectrum: Spectrum) -> tuple[int, float] | None:
    """``(몇 개, 그 위 주파수)`` -- the run of points **above** the real axis at the
    low-frequency end, when there are at least two and the spectrum is capacitive
    somewhere above them (not a sweep that is inductive all the way)."""
    order = np.argsort(spectrum.frequency_hz)      # 낮은 주파수부터
    imag = spectrum.z_im[order]
    magnitude = np.hypot(spectrum.z_re[order], imag)
    count = 0
    while count < len(imag) and imag[count] > LOW_FREQUENCY_INDUCTIVE_SHARE * magnitude[count]:
        count += 1
    if count < 2 or count == len(imag) or not np.any(imag[count:] < 0):
        return None
    return count, float(spectrum.frequency_hz[order[count - 1]])


def _kk_sigma(result: KKResult) -> float:
    """The noise of the residuals -- 1.4826 × their median absolute value."""
    parts = np.concatenate([result.residual_re, result.residual_im])
    return float(1.4826 * np.median(np.abs(parts)))


def _would_flag(result: KKResult) -> bool:
    """The findings would say the spectrum breaks KK (not only that it is noisy)."""
    if not result.judged or not result.residual.size:
        return False
    worst = float(result.max_residual)
    return worst >= KK_LIMIT and worst >= KK_NOISE_MULTIPLE * _kk_sigma(result)


def _kk_summary(result: KKResult, spectrum: Spectrum) -> tuple[dict, KKResult]:
    """The numbers to print, and the result the findings are read from.

    **Before a finding, a second look.**  When the μ-sized fit would report a
    violation, or μ stopped too early to judge, the points are fitted again
    with at least three elements per decade (never fewer than μ chose) and
    the time constants a quarter decade beyond the band.  That model is still
    Kramers–Kronig-consistent, only less starved: if it draws the points, the
    deviation was the first fit's, not the cell's.  On the lab's full-cell
    shapes μ stopped at 1.4–2.2 per decade and the low end was 2–5 % off on
    spectra built to satisfy KK; seen again it was 0.9 %.  A step in the
    points stays: 5 % below 10 Hz is 2.7 % either way.
    """
    if not result.judged:
        return {"judged": False, "reason": result.reason}, result
    chosen = result
    reason = ""
    early = result.per_decade < KK_EARLY_STOP_PER_DECADE and result.rms >= KK_LIMIT
    if early or _would_flag(result):
        count = max(math.ceil(KK_SECOND_LOOK_PER_DECADE * result.decades), result.m)
        second = lin_kk(spectrum.frequency_hz, spectrum.z_re, spectrum.z_im, m=count,
                        extend=KK_SECOND_LOOK_EXTEND)
        if second.judged and (early or second.max_residual < result.max_residual):
            chosen = second
            where = (f"μ 기준이 decade 당 {result.per_decade:.1f}개에서 멈췄습니다 — "
                     f"날카로운 아크나 저주파 유도성 루프에서 이 기준이 일찍 "
                     f"멈춥니다" if early else
                     f"μ 기준(decade 당 {result.per_decade:.1f}개)으로는 "
                     f"{result.at_hz:.3g} Hz 가 {result.max_residual * 100:.1f} % "
                     f"어긋났습니다")
            again = (f"decade 당 {second.per_decade:.1f}개, 대역 밖 1/4 decade "
                     f"까지 시정수를 두고 다시 보니 잔차가 "
                     f"{second.max_residual * 100:.1f} %")
            if _would_flag(second):
                reason = f"{where}. {again} 입니다"
            elif second.max_residual < KK_LIMIT:
                reason = f"{where}. {again} 라 어긋남은 없습니다"
            else:
                # 실측 B11 0 °C: "잔차가 25 % 라 어긋남은 없습니다" 로 읽혔다 —
                # 어긋남이 없는 것이 아니라 잡음이 그만큼 크다.
                reason = (f"{where}. {again} 지만 잡음(σ ≈ "
                          f"{_kk_sigma(second) * 100:.2f} %)의 여섯 배 안이라 "
                          f"어긋남으로 보지 않습니다")
    sigma = _kk_sigma(chosen)
    return ({
        "judged": True, "reason": reason, "m": chosen.m,
        "per_decade": chosen.per_decade, "mu": chosen.mu,
        "max_residual": chosen.max_residual, "at_hz": chosen.at_hz,
        "rms": chosen.rms, "sigma": sigma,
        "with_capacitance": chosen.with_capacitance,
        "with_inductance": chosen.with_inductance, "capped": chosen.capped,
        "dropped_inductive": chosen.dropped_inductive,
    }, chosen)


def _kk_findings(result: KKResult, summary: dict,
                 switches: Sequence[float] = ()) -> list[Finding]:
    worst = summary["max_residual"]
    sigma = summary["sigma"]
    noisy = (Finding(NOTE, "kk_noisy",
                     f"잡음이 큽니다 (KK 잔차의 σ ≈ {sigma * 100:.1f} %) — 어긋남은 "
                     f"잡음 수준이지만 맞춘 값의 오차 막대도 그만큼 큽니다")
             if sigma >= KK_NOISY else None)
    if worst < KK_LIMIT or worst < KK_NOISE_MULTIPLE * sigma:
        return [noisy] if noisy else []

    frequency = result.frequency_hz
    residual = result.residual
    order = np.argsort(frequency)                   # 낮은 주파수부터
    rank = int(np.where(order == int(np.argmax(residual)))[0][0])
    floor = max(3.0 * sigma, KK_LIMIT / 2)
    low = high = rank
    while low > 0 and residual[order[low - 1]] > floor:
        low -= 1
    while high < len(order) - 1 and residual[order[high + 1]] > floor:
        high += 1
    f_low, f_high = float(frequency[order[low]]), float(frequency[order[high]])
    at_top = f_high * 10.0 ** KK_EDGE_DECADES >= float(frequency.max())
    at_bottom = low == 0
    size = f"최대 {worst * 100:.1f} %, 잡음 σ ≈ {sigma * 100:.2f} %"
    span = f"{f_low:.3g}–{f_high:.3g} Hz" if low != high else f"{f_low:.3g} Hz"
    if at_top and not at_bottom:
        if result.capped:
            return []
        return [Finding(NOTE, "kk_high_frequency",
                        f"고주파 끝 {span} 가 Kramers–Kronig 를 어깁니다 ({size}) — "
                        f"배선·기기의 한계입니다. 맞춤의 상한을 {f_low:.3g} Hz 아래로 "
                        f"두세요")]
    switch = next((one for one in switches
                   if f_low / RANGE_SWITCH_REACH <= one <= f_high * RANGE_SWITCH_REACH),
                  None)
    also = (f". {'바로 옆' if low == high else '그 근처'} {switch:.3g} Hz 에서 기기의 "
            f"전류 범위도 바뀌었습니다 — 드리프트인지 범위 전환인지는 범위를 고정하고 "
            f"다시 재면 가려집니다" if switch is not None else "")
    if switch is not None and not at_bottom and f_high / f_low <= RANGE_SWITCH_SPAN:
        return [Finding(NOTE, "kk_range_switch",
                        f"{span} 가 Kramers–Kronig 를 어깁니다 ({size}) — 기기의 전류 "
                        f"범위가 {switch:.3g} Hz 에서 바뀐 자리입니다. 셀이 변한 것이 "
                        f"아니라 범위 전환의 흔적일 가능성이 큽니다: 그 점들은 덜 "
                        f"믿고, 그 구간을 지나는 아크가 중요하면 전류 범위를 고정해 "
                        f"다시 재세요")]
    if low == high:
        if at_bottom:
            return [Finding(NOTE, "kk_outlier",
                            f"가장 낮은 점 {span} 하나가 Kramers–Kronig 를 어깁니다 "
                            f"({size}) — 측정 끝에서 셀이 변하기 시작했거나 튄 "
                            f"점입니다. 맞춤에서 빼 보세요{also}")]
        return [Finding(NOTE, "kk_outlier",
                        f"{span} 의 점 하나가 Kramers–Kronig 를 어깁니다 ({size}) — "
                        f"튄 점입니다. 맞춤에서 빼 보세요")]
    if at_bottom:
        above = float(frequency[order[high + 1]]) if high + 1 < len(order) else f_high
        return [Finding(CHECK, "kk_violation",
                        f"저주파 끝 {span} 가 Kramers–Kronig 를 어깁니다 ({size}) — "
                        f"측정 중에 셀이 변했습니다 (온도가 덜 올라왔거나, 쉬지 않은 "
                        f"셀). 그 점들로 정한 꼬리·저항은 믿지 말고, 하한을 "
                        f"{above:.3g} Hz 로 두고 다시 맞추세요{also}")]
    return [Finding(CHECK, "kk_violation",
                    f"{span} 에서 Kramers–Kronig 를 어깁니다 ({size}) — 그 사이에 "
                    f"셀·접촉이 바뀌었거나 그 주파수에서 측정이 흔들렸습니다 (기기의 "
                    f"전류 범위 전환, 전원 잡음). 그 구간을 지나는 아크의 값은 믿지 "
                    f"마세요{also}")]


# --------------------------------------------------------------------------
# a temperature scan (ADR 0039)
# --------------------------------------------------------------------------

def audit_conductivity_scan(sweeps: Sequence[dict], *,
                            warnings: Sequence[str] = (),
                            reason: str = "",
                            without_first: tuple[float, float] | None = None,
                            backwards: Sequence[tuple[float, float]] = ()
                            ) -> list[Finding]:
    """The per-sweep numbers a conductivity scan rests on.

    ``sweeps`` items: ``{"index", "temperature_c", "typed_ohm", "re_min_ohm",
    "re_max_ohm"}`` and, when known, ``"crossing_ohm"``, ``"blocking"`` /
    ``"phase_deg"`` (the sweep's low-frequency verdict) and ``"start_s"`` /
    ``"end_s"`` (when it was measured, seconds from the start of the record).
    ``warnings`` / ``reason`` are the activation energy's own (ADR 0039);
    ``without_first`` is ``(Ea eV, R²)`` of the same fit with the first sweep
    left out; ``backwards`` the steps it found going the wrong way
    (``conductivity.backwards_steps``) -- said here instead of in its warning,
    without the steps a sweep named below already explains.
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
        typed = one.get("typed_ohm")
        low, high = one.get("re_min_ohm"), one.get("re_max_ohm")
        if not typed or typed <= 0 or low is None or high is None:
            continue
        margin = TYPED_OUTSIDE_SPAN_MARGIN
        if typed < low * (1 - margin) or typed > high * (1 + margin):
            out.append(Finding(
                CHECK, "typed_outside_spectrum",
                f"스윕 {one['index']}: 적은 저항 {typed:.4g} Ω 이 그 스윕의 Re(Z) "
                f"범위({low:.4g}–{high:.4g} Ω) 밖입니다 — 곡선 위에 없는 값입니다. "
                f"소수점이나 다른 스윕의 값을 적었는지 보세요"))
    odd, named = _blocking_outliers(sweeps)
    out += odd
    off, far = _off_the_line(sweeps)
    if off is not None:
        out.append(off)
        named |= far
    out += _short_rests(sweeps)
    told = backwards_warning(backwards) if backwards else None
    for warning in warnings:
        if warning != told:
            out.append(Finding(CHECK, "activation_warning", warning))
    if without_first is not None and _first_step_goes_up(sweeps):
        ea, r_squared = without_first
        out.append(Finding(
            NOTE, "first_sweep_suspect",
            f"첫 스윕만 온도와 거꾸로 갑니다 — 첫 가열에서 펠릿이 자리를 잡거나 "
            f"(접촉·치밀화) 평형 전에 잰 경우에 흔합니다. 첫 스윕을 빼면 Ea = "
            f"{ea:.3f} eV (R² = {r_squared:.3f})"))
        named.add(min(one["index"] for one in sweeps))
    wrong_way = _backwards_finding(sweeps, backwards, named)
    if wrong_way is not None:
        out.append(wrong_way)
    if reason:
        out.append(Finding(NOTE, "activation_missing", f"활성화에너지 없음 — {reason}"))
    return sort_findings(out)


#: 한 스윕의 저주파 위상이 스캔의 나머지(중앙값)에서 이만큼(도) 떨어지면 튄다.
PHASE_OUTLIER_DEG = 30.0


def _backwards_finding(sweeps: Sequence[dict], backwards: Sequence[tuple[float, float]],
                       named: set[int]) -> Finding | None:
    """The steps where the conductivity does not fall on cooling, less the
    ones a named sweep explains.

    The first version said it next to the finding that explained it --
    실측 B13·B15·B18: "60→50 °C 가 거꾸로 — 저항을 다시 읽어 주세요" (확인) 옆에
    "첫 스윕만 거꾸로 갑니다 — 첫 가열에서 흔합니다" (참고).  And "read it again"
    is wrong when the typed value is where the spectrum crosses the axis: the
    reading is right, the measurement moved (B17: 모든 스윕이 교점 그대로).
    """
    at: dict[float, list[dict]] = {}
    for one in sweeps:
        if one.get("temperature_c") is not None:
            at.setdefault(float(one["temperature_c"]), []).append(one)
    left = [(high, low) for high, low in backwards
            if not any(one["index"] in named
                       for one in at.get(float(high), []) + at.get(float(low), []))]
    if not left:
        return None
    involved = [one for high, low in left for one in at.get(float(high), [])
                + at.get(float(low), [])]
    measured = involved and all(
        one.get("typed_ohm") and one.get("crossing_ohm")
        and abs(one["crossing_ohm"] / one["typed_ohm"] - 1) < 0.1 for one in involved)
    where = ", ".join(f"{high:g}→{low:g} °C" for high, low in left[:4])
    advice = ("적은 저항은 그 스윕들의 실수축 교점과 같습니다 — 읽기가 아니라 측정이 "
              "벗어났으니 그 온도를 다시 재세요" if measured
              else "그 온도의 저항을 다시 읽어 주세요")
    return Finding(CHECK, "conductivity_goes_backwards",
                   f"온도가 내려가는데 이온전도도가 안 내려가는 구간이 {len(left)}개 "
                   f"있습니다 ({where}) — {advice}")


def _blocking_outliers(sweeps: Sequence[dict]) -> tuple[list[Finding], set[int]]:
    """Sweeps whose low-frequency phase is far from the rest of the scan, and
    their indices.

    A blocking pellet stays blocking from 60 °C to -20 °C; one sweep that
    suddenly passes DC is a measurement that went wrong (a contact, frost in
    the chamber), not a new material.  실측 B11 의 0 °C 스윕: 나머지 여덟은
    -70°대였는데 그것만 -12° 였고, 실수축 교점도 없었다.

    **The phase, not the verdict.**  The first version compared verdicts, and
    once the verdict learned to say "unclear" (ADR 0044) that sweep became
    unclear instead of open -- and dropped out of the comparison.  What differs
    is the phase itself.
    """
    phased = [one for one in sweeps if one.get("phase_deg") is not None]
    if len(phased) < 3:
        return [], set()
    usual = float(np.median([one["phase_deg"] for one in phased]))
    odd = [one for one in phased if abs(one["phase_deg"] - usual) > PHASE_OUTLIER_DEG]
    if not odd or len(odd) * 3 > len(phased):
        return [], set()
    names = ", ".join(
        f"스윕 {one['index']}"
        + (f" ({one['temperature_c']:g} °C)" if one.get("temperature_c") is not None
           else "")
        + f" 위상 {_deg(one.get('phase_deg'))}"
        for one in odd)
    return [Finding(
        CHECK, "sweep_unlike_its_neighbours",
        f"{names} 만 저주파 위상이 나머지({_deg(usual)} 안팎)와 딴판입니다 — 같은 "
        f"펠릿이 한 온도에서만 달라질 이유는 없습니다. 그 측정 자체(접촉·결로·"
        f"온도)를 의심하고, 그 스윕의 저항은 쓰지 마세요")], {one["index"] for one in odd}


#: Arrhenius 직선에서 ln R 로 이만큼(1.5 배) 넘게 떨어진 스윕을 짚는다.
OFF_THE_LINE = math.log(1.5)


def _line(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    """Least squares ``y = slope·x + intercept`` and its R² (flat when every
    ``x`` is the same -- there is no line to draw)."""
    if float(np.ptp(x)) == 0.0:
        return 0.0, float(np.mean(y)), 0.0
    slope, intercept = np.polyfit(x, y, 1)
    residual = y - (slope * x + intercept)
    spread = float(np.sum((y - y.mean()) ** 2))
    r_squared = 1.0 - float(np.sum(residual ** 2)) / spread if spread > 0 else 1.0
    return float(slope), float(intercept), r_squared


def _off_the_line(sweeps: Sequence[dict]) -> tuple[Finding | None, set[int]]:
    """Sweeps whose typed resistance sits far off the Arrhenius line the others
    draw -- named, with the value the line expects, and their indices.

    One point at a time: the one furthest from the line fitted **without it**
    goes, while it is more than 1.5 times off and more than four robust
    spreads of the rest, and never more than a third of the sweeps.  A scan
    that is scattered everywhere names nobody -- the R² warning speaks for it.
    A gentle bend is not an outlier: bulk and grain boundary have their own
    slopes (``ISW1990.bulk-and-gb-have-different-activation``), so a summed R
    curves -- 1.5 times off one point is not that.
    The expected values come from the final line, both outliers out.
    실측 B11: 0 °C (1.11e5 Ω, 직선은 37.7 Ω)와 20 °C (79.9 Ω, 직선은 19 Ω)를 빼면
    R² 0.270 → 0.986.  따로 잰 0 °C 스펙트럼(#68)의 R0 는 36 Ω 이었다 — 직선이 맞다.
    B17 은 넷이 흩어져 아무도 짚지 않는다.
    """
    rows = [one for one in sweeps if one.get("temperature_c") is not None
            and one.get("typed_ohm") and one["typed_ohm"] > 0]
    if len(rows) < 5 or len({one["temperature_c"] for one in rows}) < 3:
        return None, set()           # 온도가 셋은 되어야 직선이 있다
    x = np.array([1.0 / (one["temperature_c"] + 273.15) for one in rows])
    y = np.log([float(one["typed_ohm"]) for one in rows])
    keep = np.ones(len(rows), dtype=bool)
    removed: list[int] = []
    while keep.sum() > 4 and len(removed) < len(rows) // 3:
        worst, worst_off = -1, 0.0
        for index in np.flatnonzero(keep):
            others = keep.copy()
            others[index] = False
            slope, intercept, _ = _line(x[others], y[others])
            off = abs(y[index] - (slope * x[index] + intercept))
            if off > worst_off:
                worst, worst_off = int(index), off
        others = keep.copy()
        others[worst] = False
        slope, intercept, _ = _line(x[others], y[others])
        rest = np.abs(y[others] - (slope * x[others] + intercept))
        if worst_off < max(OFF_THE_LINE, 4.0 * 1.4826 * float(np.median(rest))):
            break
        keep[worst] = False
        removed.append(worst)
    first = min(range(len(rows)), key=lambda i: rows[i]["index"])
    if not removed or removed == [first]:
        return None, set()           # 첫 스윕만이면 first_sweep_suspect 가 말한다
    slope, intercept, r_squared = _line(x[keep], y[keep])
    named = sorted(removed, key=lambda i: rows[i]["index"])
    listed = ", ".join(
        f"스윕 {rows[i]['index']} ({rows[i]['temperature_c']:g} °C, "
        f"{rows[i]['typed_ohm']:.3g} Ω)" for i in named)
    expected = ", ".join(f"{math.exp(slope * x[i] + intercept):.3g} Ω" for i in named)
    # 적은 값이 그 스윕의 실수축 교점과 같으면 읽기 실수가 아니다 (실측 B11 20 °C).
    measured = [rows[i] for i in named if rows[i].get("crossing_ohm")
                and abs(rows[i]["crossing_ohm"] / rows[i]["typed_ohm"] - 1) < 0.1]
    if measured:
        who = ", ".join(f"스윕 {one['index']}" for one in measured)
        advice = (f"{who} 는 스펙트럼의 실수축 교점도 그 값입니다 — 읽기 실수가 "
                  f"아니라 측정이 벗어났으니 그 온도를 다시 재세요")
    else:
        advice = "그 스윕을 다시 읽거나 다시 재세요"
    return Finding(
        CHECK, "sweep_off_the_line",
        f"{listed} 가 나머지 {int(keep.sum())}개가 그리는 Arrhenius 직선에서 "
        f"멉니다 — 직선이 말하는 값은 {expected} 입니다. {advice}. 빼면 "
        f"Ea = {slope * BOLTZMANN_EV_PER_K:.3f} eV (R² = {r_squared:.3f})"), \
        {rows[i]["index"] for i in named}


#: 앞 스윕 뒤에 쉰 시간이 다른 스윕들의 이만큼(비율)도 안 되면 평형 전일 수 있다.
_SHORT_REST = 0.5


def _short_rests(sweeps: Sequence[dict]) -> list[Finding]:
    """Sweeps measured after a much shorter rest than the others.

    The rest *is* the temperature equilibration: the chamber moves, the pellet
    follows with a delay, and a sweep taken too early reads a temperature the
    pellet is not at yet.  The first sweep's rest is counted from the start of
    the record.
    """
    timed = [one for one in sweeps
             if one.get("start_s") is not None and one.get("end_s") is not None]
    if len(timed) < 3:
        return []
    timed = sorted(timed, key=lambda one: one["start_s"])
    rests = [float(timed[0]["start_s"])]
    rests += [float(b["start_s"]) - float(a["end_s"]) for a, b in zip(timed, timed[1:],
                                                                      strict=False)]
    others = sorted(rests[1:])
    usual = float(np.median(others)) if others else 0.0
    if usual <= 0:
        return []
    short = [(one, rest) for one, rest in zip(timed, rests, strict=True)
             if rest < _SHORT_REST * usual]
    if not short:
        return []
    listed = ", ".join(
        f"스윕 {one['index']} ({_hours(rest)})" for one, rest in short)
    return [Finding(
        CHECK, "short_rest_before_sweep",
        f"{listed} 은 앞 스윕 뒤(첫 스윕은 기록 시작 뒤) 쉰 시간이 다른 스윕들"
        f"({_hours(usual)}) 보다 한참 짧습니다 — 온도가 평형에 닿기 전에 잰 것일 수 "
        f"있습니다")]


def _hours(seconds: float) -> str:
    if seconds >= 3600:
        return f"{seconds / 3600:.1f} h"
    return f"{seconds / 60:.0f} min"


def _first_step_goes_up(sweeps: Sequence[dict]) -> bool:
    """The first two sweeps go the wrong way (resistance up as the temperature
    goes down... the other way round) and nothing after them does."""
    rows = [one for one in sweeps
            if one.get("temperature_c") is not None and one.get("typed_ohm")]
    if len(rows) < 4:
        return False

    def wrong(a: dict, b: dict) -> bool:
        cooler_b = b["temperature_c"] < a["temperature_c"]
        return (b["typed_ohm"] < a["typed_ohm"]) if cooler_b else (
            b["typed_ohm"] > a["typed_ohm"])

    steps = [wrong(a, b) for a, b in zip(rows, rows[1:], strict=False)]
    return steps[0] and not any(steps[1:])
