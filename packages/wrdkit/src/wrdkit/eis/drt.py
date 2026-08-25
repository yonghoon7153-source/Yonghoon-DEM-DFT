"""Distribution of relaxation times.

An equivalent circuit answers "how many arcs, and how big".  It cannot answer
"how many processes are there" -- that is decided in advance by whoever wrote
the circuit.  The DRT does not decide it: it asks the spectrum how much
polarisation sits at each relaxation time,

    Z(w) = R_inf + jwL + integral over ln(tau) of  gamma(tau) / (1 + jw tau)

and hands back the whole curve.  Two processes a hundredth of a decade apart
appear as two peaks in gamma; in a Nyquist plot they are one arc.

The catch is that the inversion is ill-posed: many gamma reproduce the same
spectrum to within the noise.  Tikhonov regularisation picks one by penalising
roughness, and **the penalty weight decides the answer** -- too small and the
curve is a forest of noise peaks, too large and two real processes merge into
one.  This is the same problem the knee detector has, and it gets the same
treatment (ADR 0005): do not pick one value silently.  ``sweep`` computes a
range and ``lcurve_corner`` says which one the L-curve suggests and why, so
the choice is on screen instead of buried in a default.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .guess import inductive_mask
from .spectrum import Spectrum

__all__ = ["DrtResult", "DrtPeak", "drt", "sweep", "lcurve_corner", "SCIPY_MISSING"]

SCIPY_MISSING = (
    "DRT 에는 scipy 가 필요합니다 — `pip install 'wrdkit[eis]'` "
    "(음수가 아닌 해를 구속 최소자승으로 풀어야 합니다)"
)


@dataclass
class DrtPeak:
    """One process the spectrum shows, with the resistance it accounts for."""

    #: Relaxation time at the top of the peak.
    tau_s: float
    #: The frequency a person would look for it at: ``1 / (2 pi tau)``.
    frequency_hz: float
    #: Peak height of gamma.
    gamma_ohm: float
    #: Area under the peak in ln(tau) -- the polarisation resistance it carries.
    resistance_ohm: float
    #: Where the peak starts and ends, in seconds.
    tau_low_s: float
    tau_high_s: float


@dataclass
class DrtResult:
    tau_s: np.ndarray = field(repr=False)
    gamma_ohm: np.ndarray = field(repr=False)
    #: The high-frequency real-axis intercept the fit found.
    r_inf_ohm: float = 0.0
    #: Series inductance, when it was fitted.  Cable, not cell.
    inductance_h: float | None = None
    #: The penalty weight that produced this gamma.  Part of the answer.
    regularisation: float = 0.0
    derivative_order: int = 0
    #: Proportional residual norm and penalty norm -- the two axes of the L curve.
    residual_norm: float = 0.0
    penalty_norm: float = 0.0
    #: Mean squared proportional residual, comparable with a circuit fit's.
    chi_squared: float = 0.0
    peaks: list[DrtPeak] = field(default_factory=list)
    frequency_hz: np.ndarray = field(default_factory=lambda: np.array([]), repr=False)
    fitted: np.ndarray = field(default_factory=lambda: np.array([]), repr=False)
    dropped_inductive: int = 0
    #: Total polarisation resistance: the area under the whole of gamma.
    total_polarisation_ohm: float = 0.0


def _tau_grid(frequency_hz: np.ndarray, per_decade: int,
              extend_decades: float) -> np.ndarray:
    """Relaxation times to solve on.

    Extended past the measured band on both sides on purpose: a process whose
    peak sits just outside the window still has a shoulder inside it, and a
    grid that stops at the band edge has nowhere to put that shoulder -- so it
    piles it onto the last grid point, producing a spike at the edge that reads
    as a real process.
    """
    low = 1.0 / (2 * np.pi * np.max(frequency_hz))
    high = 1.0 / (2 * np.pi * np.min(frequency_hz))
    start = np.log10(low) - extend_decades
    stop = np.log10(high) + extend_decades
    count = max(int(round((stop - start) * per_decade)) + 1, 8)
    return np.logspace(start, stop, count)


def _log_weights(tau_s: np.ndarray) -> np.ndarray:
    """Trapezoid weights over ``ln tau`` -- the one quadrature everything uses.

    The kernel and the reported totals must integrate gamma with the *same*
    weights.  The first version gave the kernel ``np.gradient`` weights (full
    step at the endpoints) and the report ``np.trapezoid`` (half step), so on
    a spectrum with endpoint mass the model's DC limit and the printed
    "total polarisation" were two different numbers -- 7-10 % apart in the
    review reproduction, a clean factor 2 for endpoint-only gamma.
    """
    weights = np.gradient(np.log(tau_s))
    weights[0] /= 2.0
    weights[-1] /= 2.0
    return weights


def _kernel(frequency_hz: np.ndarray, tau_s: np.ndarray) -> np.ndarray:
    """Complex ``A`` with ``Z_polarisation = A @ gamma``.

    The integral is over ``ln tau``, so each column carries its own weight:
    with a log grid that is one constant inside, but writing it per column
    keeps the arithmetic right if the grid is ever made non-uniform.
    """
    omega = 2 * np.pi * frequency_hz[:, None]
    kernel = 1.0 / (1.0 + 1j * omega * tau_s[None, :])
    return kernel * _log_weights(tau_s)[None, :]


def _difference_matrix(size: int, order: int) -> np.ndarray:
    """What "rough" means.  Order 0 penalises size, 1 slope, 2 curvature."""
    matrix = np.eye(size)
    for _ in range(max(0, order)):
        matrix = np.diff(matrix, axis=0)
    return matrix


def drt(spectrum: Spectrum, *, regularisation: float = 1e-3,
        tau_per_decade: int = 10, extend_decades: float = 0.5,
        derivative_order: int = 0, fit_inductance: bool = True,
        drop_inductive: bool = True) -> DrtResult:
    """Solve for ``gamma(tau)`` at one penalty weight.

    ``gamma`` is constrained to be non-negative.  That is physics, not
    convenience: a negative relaxation strength would be a process that
    *supplies* polarisation.  Without the constraint the solver buys a better
    residual with a positive spike next to a negative one, and both are
    reported as processes.
    """
    try:
        from scipy.optimize import lsq_linear
    except ImportError as exc:                       # pragma: no cover
        raise ImportError(SCIPY_MISSING) from exc

    working = spectrum.sorted_by_frequency(descending=True)
    dropped = 0
    if drop_inductive:
        mask = ~inductive_mask(working)
        dropped = int(np.sum(~mask))
        working = working.select(mask)
    if len(working) < 6:
        raise ValueError(f"DRT 에는 점이 더 필요합니다 — {len(working)}개 남았습니다")

    frequency = working.frequency_hz
    z = working.z
    tau = _tau_grid(frequency, tau_per_decade, extend_decades)
    kernel = _kernel(frequency, tau)

    # Columns: gamma over the tau grid, then R_inf, then (optionally) L.
    extra = [np.ones((len(frequency), 1), dtype=complex)]
    if fit_inductance:
        extra.append(1j * 2 * np.pi * frequency[:, None])
    design = np.hstack([kernel, *extra])

    # Proportional weighting, as in the circuit fit: impedance spans decades
    # inside one spectrum, so an unweighted solve fits the low-frequency end.
    weights = 1.0 / np.abs(z)
    real = np.vstack([design.real * weights[:, None],
                      design.imag * weights[:, None]])
    target = np.concatenate([z.real * weights, z.imag * weights])

    n_extra = design.shape[1] - len(tau)
    penalty = _difference_matrix(len(tau), derivative_order)
    penalty = np.hstack([penalty, np.zeros((penalty.shape[0], n_extra))])
    # R_inf and L are not part of the curve being smoothed; penalising them
    # would drag the intercept toward zero and call the difference a process.
    augmented = np.vstack([real, np.sqrt(regularisation) * penalty])
    augmented_target = np.concatenate([target, np.zeros(penalty.shape[0])])

    lower = np.concatenate([np.zeros(len(tau)), np.full(n_extra, -np.inf)])
    upper = np.full(augmented.shape[1], np.inf)
    # BVLS on unit-norm columns, not TRF.  TRF is iterative and was run with a
    # step cap; on some platforms it stalls far from the optimum and the code
    # accepted the stalled answer without looking at ``status`` -- the review
    # reproduced a clean one-RC spectrum coming back with half its resistance
    # and eight phantom peaks.  BVLS is an exact active-set solve, and with
    # the columns scaled it is also the fastest of the three options tried
    # (5 ms against TRF's 41 ms on the same system).  Bounds scale with the
    # columns: zero and infinity survive the multiplication unchanged.
    scale = np.linalg.norm(augmented, axis=0)
    scale[scale == 0] = 1.0
    solution = lsq_linear(augmented / scale, augmented_target,
                          bounds=(lower * scale, upper), method="bvls")
    if not solution.success:
        raise ValueError(f"DRT 해가 수렴하지 않았습니다 (λ={regularisation:g}): "
                         f"{solution.message}")
    solution.x = solution.x / scale

    gamma = solution.x[:len(tau)]
    r_inf = float(solution.x[len(tau)])
    inductance = float(solution.x[len(tau) + 1]) if fit_inductance else None

    model = design @ solution.x
    residual = (model - z) * weights
    residual_norm = float(np.linalg.norm(np.concatenate([residual.real,
                                                         residual.imag])))
    penalty_norm = float(np.linalg.norm(penalty @ solution.x))
    dof = max(2 * len(frequency) - 1, 1)

    return DrtResult(
        tau_s=tau,
        gamma_ohm=gamma,
        r_inf_ohm=r_inf,
        inductance_h=inductance,
        regularisation=regularisation,
        derivative_order=derivative_order,
        residual_norm=residual_norm,
        penalty_norm=penalty_norm,
        chi_squared=residual_norm ** 2 / dof,
        peaks=find_peaks(tau, gamma),
        frequency_hz=frequency,
        fitted=model,
        dropped_inductive=dropped,
        # The same weights the kernel used, so this IS the model's DC limit:
        # Z(0) - R_inf equals this number exactly, and a test holds it there.
        total_polarisation_ohm=float(np.sum(gamma * _log_weights(tau)))
        if len(tau) > 1 else 0.0,
    )


def find_peaks(tau_s: np.ndarray, gamma_ohm: np.ndarray, *,
               floor: float = 0.02) -> list[DrtPeak]:
    """Processes in gamma, each with the resistance it accounts for.

    A peak under *floor* of the tallest is not reported.  Regularised
    inversions ring: a real peak leaves small oscillations beside it, and
    printing those as processes is how a DRT plot ends up with nine of them.
    """
    if len(gamma_ohm) < 3 or not np.any(gamma_ohm > 0):
        return []
    tallest = float(np.max(gamma_ohm))
    peaks: list[DrtPeak] = []
    for i in range(1, len(gamma_ohm) - 1):
        if not (gamma_ohm[i] >= gamma_ohm[i - 1] and gamma_ohm[i] > gamma_ohm[i + 1]):
            continue
        if gamma_ohm[i] < floor * tallest:
            continue
        left = i
        while left > 0 and gamma_ohm[left - 1] < gamma_ohm[left]:
            left -= 1
        right = i
        while right < len(gamma_ohm) - 1 and gamma_ohm[right + 1] < gamma_ohm[right]:
            right += 1
        area = float(np.trapezoid(gamma_ohm[left:right + 1],
                                  np.log(tau_s[left:right + 1]))) \
            if right > left else 0.0
        peaks.append(DrtPeak(
            tau_s=float(tau_s[i]),
            frequency_hz=float(1.0 / (2 * np.pi * tau_s[i])),
            gamma_ohm=float(gamma_ohm[i]),
            resistance_ohm=area,
            tau_low_s=float(tau_s[left]),
            tau_high_s=float(tau_s[right]),
        ))
    peaks.sort(key=lambda peak: peak.tau_s)
    return peaks


def sweep(spectrum: Spectrum, *, regularisations: list[float] | None = None,
          **options) -> list[DrtResult]:
    """One solve per penalty weight, so the choice can be seen instead of made.

    Six decades by default.  Fewer would not show both failure modes -- the
    noise forest at one end and the single merged blob at the other -- and it
    is the pair that makes the middle look like a choice rather than a default.
    """
    if regularisations is None:
        regularisations = [10.0 ** power for power in range(-6, 1)]
    out = []
    for value in regularisations:
        try:
            out.append(drt(spectrum, regularisation=value, **options))
        except (ValueError, np.linalg.LinAlgError):
            continue
    return out


def lcurve_corner(results: list[DrtResult]) -> tuple[int, str]:
    """Which penalty weight the L curve points at, and why -- or that it does not.

    Plotted log-log, residual against penalty, an ill-posed inverse problem's
    solutions trace an L: the vertical arm is over-fitting, the horizontal arm
    is over-smoothing, and the corner is where buying more smoothness starts
    costing real fit.  Maximum curvature finds the corner.

    Returns ``(-1, reason)`` when there is no corner to find.  A spectrum whose
    L curve is a straight line has not told us which weight to use, and
    inventing one is exactly the thing the knee work stopped doing (§0.4).
    """
    # Indices, not the results themselves.  ``list.index`` compares dataclasses
    # field by field, and these carry numpy arrays -- the comparison raises
    # rather than answering.
    usable = [i for i, r in enumerate(results)
              if r.residual_norm > 0 and r.penalty_norm > 0]
    if len(usable) < 3:
        return -1, "L 곡선을 그릴 만큼 결과가 많지 않습니다"

    x = np.log10([results[i].penalty_norm for i in usable])
    y = np.log10([results[i].residual_norm for i in usable])
    if np.ptp(x) < 1e-9 or np.ptp(y) < 1e-9:
        return -1, "L 곡선이 한 점에 모여 있어 모서리가 없습니다"

    # Curvature of the discrete curve, by finite differences on the log-log
    # trace.  The endpoints have no curvature to speak of and are skipped.
    dx = np.gradient(x)
    dy = np.gradient(y)
    ddx = np.gradient(dx)
    ddy = np.gradient(dy)
    denominator = (dx ** 2 + dy ** 2) ** 1.5
    with np.errstate(divide="ignore", invalid="ignore"):
        curvature = np.abs(dx * ddy - dy * ddx) / denominator
    curvature[~np.isfinite(curvature)] = 0.0
    curvature[0] = curvature[-1] = 0.0
    if not np.any(curvature > 0):
        return -1, "L 곡선이 거의 직선이라 모서리가 없습니다"

    # 곡률이 큰 순서로 훑되, **측정하지 않은 주파수에 봉우리가 있는 답은
    # 추천하지 않는다.**  τ 격자는 측정 대역 밖으로 조금 넘겨 잡는다 -- 대역
    # 바로 밖의 실제 과정이 어깨를 놓을 자리가 필요해서다.  하지만 그 연장
    # 구간에 *봉우리*(극대)가 서 있다면 그것은 아무 주파수도 재지 않은 곳에서
    # "과정을 찾았다" 는 뜻이고, 정칙화가 막으려던 바로 그 과대적합이다.
    #
    # 실측 파일에서 이것이 갈랐다: 곡률 최대는 λ=1e-5 인데 그 답에는 측정
    # 대역(≤1.39 MHz) 밖 2.19 MHz 봉우리가 있었다.  건너뛰고 그 이유를 말한다.
    skipped: list[str] = []
    for rank in np.argsort(-curvature):
        index = usable[int(rank)]
        chosen = results[index]
        if curvature[rank] <= 0:
            continue
        outside = _peaks_outside_band(chosen)
        if outside:
            skipped.append(f"λ={chosen.regularisation:g} 은 측정 대역 밖 "
                           f"({', '.join(outside)}) 에 봉우리가 있어 건너뜁니다")
            continue
        reason = (f"L 곡선의 곡률이 가장 큰 지점 (λ={chosen.regularisation:g}, "
                  f"봉우리 {len(chosen.peaks)}개)")
        if skipped:
            reason += " — " + "; ".join(skipped)
        return index, reason
    if skipped:
        return -1, "모든 후보에 측정 대역 밖 봉우리가 있습니다: " + "; ".join(skipped)
    return -1, "L 곡선에서 모서리를 찾지 못했습니다"


def _peaks_outside_band(result: DrtResult) -> list[str]:
    """Peaks -- and edge pile-ups -- at frequencies this spectrum never measured.

    Returned as text because that is what the caller does with them -- the
    number itself is only useful inside the sentence explaining the skip.
    """
    if not len(result.frequency_hz):
        return []
    low = float(np.min(result.frequency_hz))
    high = float(np.max(result.frequency_hz))
    outside = [f"{peak.frequency_hz:.3g} Hz" for peak in result.peaks
               if not low <= peak.frequency_hz <= high]
    # A process past the end of the grid has no interior maximum for
    # ``find_peaks`` to report -- gamma just climbs into the edge and stops.
    # That is still a claim about frequencies nobody measured, and it slipped
    # through when only the peaks list was checked: the review's 10 MHz
    # process on a 100 kHz measurement produced "0 peaks" and got its lambda
    # recommended.  An edge the curve rises into, tall enough to matter,
    # counts as out of band like any peak there would.
    gamma = result.gamma_ohm
    if len(gamma) >= 2 and np.any(gamma > 0):
        tallest = float(np.max(gamma))
        for index in (0, len(gamma) - 1):
            neighbour = 1 if index == 0 else len(gamma) - 2
            if gamma[index] <= gamma[neighbour] or gamma[index] < 0.02 * tallest:
                continue
            edge_hz = float(1.0 / (2 * np.pi * result.tau_s[index]))
            if not low <= edge_hz <= high:
                outside.append(f"{edge_hz:.3g} Hz (격자 끝)")
    return outside
