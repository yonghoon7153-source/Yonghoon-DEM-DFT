"""Initial values, read off the spectrum instead of typed in.

The lab's procedure sheet is explicit that this is the step that decides
whether a fit works: *R1 은 전극의 Solution Bulk Resistance (X절편 값), R2 는
첫번째 Semi-Circle 지름, R3 는 두번째 Semi-Circle 지름, CPE-T 는 1e-4/1e-3,
CPE-P 는 0.6~1.2*.  Those are rules a person applies by looking at the plot, so
they are rules code can apply too -- and then the fit can be run many times
without anybody looking at anything.

Each arc is found where it actually lives: at its own characteristic frequency,
the top of a hump in -Z'' against log f.  Two arcs that overlap on the Nyquist
plot are still two humps there, because their relaxation times differ -- which
is the whole reason impedance is measured across frequency at all.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .circuit import ELEMENTS, Circuit
from .spectrum import Spectrum

__all__ = ["Arc", "find_arcs", "initial_guess", "inductive_mask"]


@dataclass
class Arc:
    """One hump in -Z'' vs log f, and what it implies for an R-CPE pair."""

    #: Frequency at the top of the hump.  ``w_peak * tau = 1``.
    peak_hz: float
    #: -Z'' at the top.  For an ideal arc this is half the diameter.
    peak_neg_z_im: float
    #: Estimated diameter -- the resistance of the R in the R-CPE pair.
    diameter_ohm: float
    #: Where the arc starts on the real axis.
    left_ohm: float
    index: int


def inductive_mask(spectrum: Spectrum) -> np.ndarray:
    """Points that sit **above** the real axis -- wiring, not the cell.

    Real spectra start inductive: the reference file is positive-imaginary from
    7 MHz down to a few hundred kHz.  Those points are the cables and the cell
    holder, and no cell circuit can reproduce them.  Left in, they drag the
    series resistance and the first arc off by whole ohms; dropped silently,
    the series resistance changes and nobody knows why.  So this returns the
    mask and the caller decides -- and says so on screen (ADR 0019).
    """
    return spectrum.z_im > 0


def _smooth(values: np.ndarray, window: int) -> np.ndarray:
    """Moving average, edge-padded.  Nothing clever: this only has to stop a
    single noisy point from being called an arc."""
    if window < 3 or len(values) < window:
        return values
    if window % 2 == 0:
        window += 1
    pad = window // 2
    padded = np.concatenate([np.full(pad, values[0]), values,
                             np.full(pad, values[-1])])
    kernel = np.ones(window) / window
    return np.convolve(padded, kernel, mode="valid")


def find_arcs(spectrum: Spectrum, *, max_arcs: int = 3,
              smoothing: int = 3) -> list[Arc]:
    """Locate arcs, high frequency first.

    A hump has to clear two hurdles to count.  It must be a local maximum of
    -Z'' with real minima on both sides (a shoulder on the way down to the
    diffusion tail is not an arc), and its height must be a real fraction of
    the largest hump -- otherwise measurement noise on a flat stretch becomes a
    third arc, and the fit gains two free parameters describing nothing.
    """
    ordered = spectrum.sorted_by_frequency(descending=True)
    keep = ~inductive_mask(ordered)
    ordered = ordered.select(keep)
    if len(ordered) < 5:
        return []

    neg_im = -ordered.z_im
    smoothed = _smooth(neg_im, smoothing)
    peaks = []
    for i in range(1, len(smoothed) - 1):
        if smoothed[i] >= smoothed[i - 1] and smoothed[i] > smoothed[i + 1]:
            peaks.append(i)
    if not peaks:
        return []

    tallest = max(smoothed[i] for i in peaks)
    #: A hump under a tenth of the tallest is noise or a shoulder.  Ten per
    #: cent is low enough to keep a small bulk arc next to a large boundary arc
    #: -- the case this lab actually has in solid electrolytes.
    peaks = [i for i in peaks if smoothed[i] >= 0.10 * tallest]
    peaks = sorted(peaks, key=lambda i: -smoothed[i])[:max_arcs]
    peaks.sort()

    arcs = []
    for order, i in enumerate(peaks):
        left_i = i
        while left_i > 0 and smoothed[left_i - 1] < smoothed[left_i]:
            left_i -= 1
        right_i = i
        while right_i < len(smoothed) - 1 and smoothed[right_i + 1] < smoothed[right_i]:
            right_i += 1
        left = float(ordered.z_re[left_i])
        right = float(ordered.z_re[right_i])
        # An ideal arc's height is half its diameter; a depressed one is
        # shorter.  Take whichever of the two readings is larger -- the width
        # on the real axis, or twice the height -- because under-estimating the
        # diameter is what starts a fit inside the wrong arc.
        diameter = max(right - left, 2.0 * float(neg_im[i]))
        arcs.append(Arc(peak_hz=float(ordered.frequency_hz[i]),
                        peak_neg_z_im=float(neg_im[i]),
                        diameter_ohm=diameter, left_ohm=left, index=order))
    return arcs


def series_resistance(spectrum: Spectrum) -> float:
    """The high-frequency real-axis intercept -- the procedure sheet's R1.

    Not simply ``min(Z')``: on a spectrum with an inductive tail the smallest
    real part can sit up at megahertz where the cell is not being measured at
    all.  Take the real part where the (non-inductive) spectrum starts, and
    never let it go negative.
    """
    ordered = spectrum.sorted_by_frequency(descending=True)
    usable = ordered.select(~inductive_mask(ordered))
    if len(usable) == 0:
        usable = ordered
    candidate = float(usable.z_re[0])
    floor = float(np.min(usable.z_re))
    return max(min(candidate, floor), 1e-6)


#: What to start a CPE at when the spectrum cannot say.  The procedure sheet's
#: numbers: 1e-4 for the first, 1e-3 for the second.
_CPE_FALLBACK_Q = (1e-4, 1e-3, 1e-2)

#: ``-Z''`` of a transmissive finite Warburg peaks at ``w tau ~ 2.53``.  Used
#: both ways: from a visible peak to tau, and -- when the sweep stopped before
#: the tail turned over -- from the lowest measured frequency to the smallest
#: tau consistent with what was seen.
_WS_PEAK_OMEGA_TAU = 2.53


def _tail(spectrum: Spectrum, arcs: list[Arc]) -> tuple[float, float, float]:
    """(lowest usable frequency in Hz, its ``Z'``, its ``-Z''``).

    "Usable" means non-inductive: the megahertz end is cables, and a diffusion
    element started from a cable measurement is started from nothing.
    """
    ordered = spectrum.sorted_by_frequency(descending=True)
    usable = ordered.select(~inductive_mask(ordered))
    if len(usable) == 0:
        usable = ordered
    return (float(usable.frequency_hz[-1]), float(usable.z_re[-1]),
            float(-usable.z_im[-1]))


def _warburg_sigma(spectrum: Spectrum, arcs: list[Arc]) -> float:
    """Start for a semi-infinite Warburg, in Ω·s^-½.

    ``Z_W = sigma (1-j)/sqrt(w)``, so ``-Z'' = sigma / sqrt(w)`` and the
    lowest measured point reads sigma straight off: ``sigma = -Z'' sqrt(w)``.

    This used to start at the spectrum's real span, which is a resistance --
    the wrong dimension entirely.  On the lab's own solid-state scan that put
    the start at 122 where the answer was 20, and the eight restarts were what
    rescued it.  A start that needs rescuing is a start that fails whenever the
    rescue is turned down (`restarts=0`) or the spectrum is a little harder.
    """
    _, _, neg_im = _tail(spectrum, arcs)
    omega = 2.0 * np.pi * _tail(spectrum, arcs)[0]
    if neg_im <= 0 or omega <= 0:
        return max(float(np.max(spectrum.z_re) - np.min(spectrum.z_re)), 1e-6)
    return max(neg_im * np.sqrt(omega), 1e-9)


def _finite_warburg(spectrum: Spectrum, arcs: list[Arc], kind: str,
                    branches: int) -> tuple[float, float]:
    """(R, tau) start for ``Ws``/``Wo``.

    **R** is what the real axis has left over: the lowest-frequency ``Z'``
    minus the series resistance and every arc diameter already accounted for.
    Starting at the whole span instead double-counts the arcs, which puts the
    tail's foot inside the last arc.

    The two elements land differently, so the leftover means different things.
    A transmissive ``Ws`` returns to the real axis at ``R``, so the leftover
    *is* R.  A blocking ``Wo`` rises capacitively and its real part settles at
    ``R/3``, so the leftover is a third of it.  Using one rule for both starts
    ``Wo`` three times too small, which is where its tail comes from.

    **tau** comes from where ``-Z''`` turns over, if the sweep went low enough
    to see it -- only ``Ws`` has such a turn-over (``Wo`` diverges instead).
    If the sweep stopped first, the turn-over is below the last measured
    frequency, so ``tau >= 2.53 / w_low``: start there rather than at one
    second, which is a number about no spectrum in particular.
    """
    frequency, z_re_low, _ = _tail(spectrum, arcs)
    span = float(np.max(spectrum.z_re) - np.min(spectrum.z_re)) or 1.0

    # 꼬리가 화면 안에서 완전히 닫혔으면 `find_arcs` 가 그것까지 아크로 센다 --
    # 그 봉우리는 정말 반원처럼 생겼기 때문이다.  회로가 가진 R-CPE 가지 수를
    # 넘는 **가장 낮은** 아크가 곧 그 꼬리이고, 그때는 지름과 꼭짓점이 R 과
    # tau 를 바로 말해 준다.  이 경우를 놓치면 남는 실축 길이가 음수가 되어
    # 폴백(전체 span)으로 떨어지고, tau 는 잡음 봉우리에서 나온다.
    for_branches = arcs[:branches]
    tail_arc = arcs[branches] if len(arcs) > branches else None

    accounted = series_resistance(spectrum) + sum(
        arc.diameter_ohm for arc in for_branches)
    leftover = z_re_low - accounted
    peak = 0.0
    if tail_arc is not None:
        # 꼭짓점은 아크에서, 지름은 **둘 중 큰 쪽**에서.  화면 안에서 아직 다
        # 닫히지 않은 꼬리는 아크로 재면 지름이 실제보다 작게 나오는데, 실축이
        # 이미 간 거리보다 작을 수는 없다.
        leftover = max(tail_arc.diameter_ohm, leftover)
        peak = tail_arc.peak_hz
    elif kind == "Ws":
        peak = _tail_peak_hz(spectrum, arcs)

    resistance = leftover * (3.0 if kind == "Wo" else 1.0)
    if not np.isfinite(resistance) or resistance <= 0:
        resistance = span
    omega = 2.0 * np.pi * (peak if peak else frequency)
    tau = _WS_PEAK_OMEGA_TAU / omega if omega > 0 else 1.0
    return max(resistance, 1e-6), float(np.clip(tau, 1e-6, 1e6))


def _tail_peak_hz(spectrum: Spectrum, arcs: list[Arc]) -> float:
    """Where ``-Z''`` turns over below the last arc, or 0 if it never does.

    A finite diffusion layer bends the 45-degree line back toward the real
    axis, and the bend has a top.  That top is the one frequency in the whole
    spectrum that speaks directly to the diffusion time constant, so it is
    worth finding even though `find_arcs` deliberately throws it away (a
    diffusion hump is not an arc, and calling it one adds two free parameters
    describing nothing).
    """
    ordered = spectrum.sorted_by_frequency(descending=True)
    usable = ordered.select(~inductive_mask(ordered))
    if len(usable) < 5:
        return 0.0
    smoothed = _smooth(-usable.z_im, 3)
    lowest_arc = min((arc.peak_hz for arc in arcs), default=float("inf"))
    #: 꼬리의 꼭대기는 그 스펙트럼에서 가장 큰 것들 축에 든다 (Ws 의 정점은
    #: 0.417 R).  이 문턱이 없으면 저주파 끝의 잡음 한 점이 꼭대기로 뽑히고,
    #: **틀린 확신**이 담긴 시작점은 중립적인 시작점보다 나쁘다 -- 재시작의
    #: 산포(로그 ×5)로는 두 자릿수를 되돌아올 수 없다.
    floor = 0.2 * float(np.max(smoothed)) if len(smoothed) else 0.0
    for i in range(len(smoothed) - 2, 0, -1):
        # 낮은 주파수에서 위로 훑는다 -- 꼬리의 꼭대기는 아크들보다 아래에 있다.
        if usable.frequency_hz[i] >= lowest_arc:
            break
        if smoothed[i] < floor:
            continue
        if smoothed[i] >= smoothed[i - 1] and smoothed[i] > smoothed[i + 1]:
            return float(usable.frequency_hz[i])
    return 0.0


def initial_guess(spectrum: Spectrum, circuit: Circuit) -> np.ndarray:
    """Starting values for every parameter of *circuit*.

    Arcs are matched to ``p(R, CPE)`` pairs in circuit order, highest frequency
    first, because that is the order they are written in and the order they
    happen in.  Anything the spectrum cannot speak to falls back to the
    procedure sheet's numbers rather than to 1.0 -- a CPE started at 1 F is
    twelve orders of magnitude out and no optimiser walks that far.
    """
    arcs = find_arcs(spectrum)
    rs = series_resistance(spectrum)
    span = float(np.max(spectrum.z_re) - np.min(spectrum.z_re)) or 1.0

    names = list(circuit.parameter_names)
    values = np.zeros(len(names))
    element_kinds = _kinds_by_name(circuit)
    branch_count = len(circuit.parallel_rc_branches())

    arc_index = 0
    used_series_r = False
    for i, name in enumerate(names):
        kind = element_kinds[name]
        if kind == "R":
            if not used_series_r:
                values[i] = rs
                used_series_r = True
            else:
                # arc_index 는 자유롭게 증가한다.  전에는 마지막 인덱스에
                # 클램프해서 `else span/...` 폴백이 사문(死文)이 됐고, 아크보다
                # R-CPE 가지가 많으면 초과 가지 전부가 마지막 아크의 지름을
                # 그대로 받아 대칭·축퇴 시작점이 됐다 (리뷰 F5) — restarts 가
                # 보통 구제하지만 시작점 결함은 시작점에서 고친다.
                arc = arcs[arc_index] if arc_index < len(arcs) else None
                values[i] = arc.diameter_ohm if arc else span / (len(arcs) + 1)
                arc_index += 1
        elif name.endswith("_Q"):
            # w_peak = 1 / (R Q)^(1/n) for an R-CPE pair; with n near 1 that
            # is Q = 1 / (R w_peak), which turns the located arc into a
            # capacitance instead of a guess.
            slot = min(_cpe_slot(names, i), len(_CPE_FALLBACK_Q) - 1)
            paired_r = _preceding_arc_resistance(names, values, i)
            arc = arcs[slot] if slot < len(arcs) else None
            if arc and paired_r > 0:
                omega = 2 * np.pi * arc.peak_hz
                values[i] = float(np.clip(1.0 / (paired_r * omega), 1e-12, 1e2))
            else:
                values[i] = _CPE_FALLBACK_Q[slot]
        elif name.endswith("_n"):
            # 0.85 rather than 1.0: real arcs are depressed, and starting at
            # the boundary leaves the optimiser pressed against it.
            values[i] = 0.85
        elif kind == "C":
            values[i] = 1e-6
        elif kind == "L":
            values[i] = 1e-7
        elif kind == "W":
            values[i] = _warburg_sigma(spectrum, arcs)
        elif name.endswith("_R") or name.endswith("_tau"):
            # Ws/Wo 의 두 값은 함께 나온다 -- R 은 남은 실축 길이, tau 는 꼬리가
            # 꺾이는 자리다.  따로 구하면 서로 모순되는 시작점이 된다.
            resistance, tau = _finite_warburg(spectrum, arcs, kind, branch_count)
            values[i] = resistance if name.endswith("_R") else tau
        else:
            values[i] = 1.0
    return np.clip(values, circuit.lower, circuit.upper)


def _kinds_by_name(circuit: Circuit) -> dict[str, str]:
    out: dict[str, str] = {}
    for element in circuit.element_names():
        kind = "".join(ch for ch in element if ch.isalpha())
        for suffix in ELEMENTS[kind].suffixes:
            out[element + suffix] = kind
    return out


def _cpe_slot(names: list[str], index: int) -> int:
    """How many CPE ``_Q`` parameters come before this one."""
    return sum(1 for name in names[:index] if name.endswith("_Q"))


def _preceding_arc_resistance(names: list[str], values: np.ndarray,
                              index: int) -> float:
    """The resistance this CPE is in parallel with -- the R just before it.

    Circuit order puts ``p(R2,CPE1)`` next to each other, so the nearest
    preceding plain ``R`` is the pair.  It is a convention, not a deduction,
    which is why it only sets a starting point.
    """
    for i in range(index - 1, -1, -1):
        if "_" not in names[i] and names[i][0] == "R":
            return float(values[i])
    return 0.0
