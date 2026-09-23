"""Is this an impedance spectrum at all? -- the linear Kramers–Kronig test (ADR 0043).

A spectrum is only worth fitting if it came from a linear, time-invariant and
causal system; the Kramers–Kronig relations tie the real part to the imaginary
part for exactly such systems (``SCHOENLEBER2014.kk-requires-lti-causal``).  A
cell that drifted during the sweep -- a pellet still warming up, a cell that
was not rested -- breaks them, and no circuit fixes that: the fit simply
spends its parameters on the drift.  The reviews say to test before modelling
(``VADHVA2021.kk-validation-before-modelling``, ``LASIA1999.kk-linear-voigt-test``).

**The test** is Boukamp's linear one, with the size chosen the way Schönleber,
Klotz & Ivers-Tiffée (2014) do it:

* fit ``Ẑ = R_ohm + Σ R_k / (1 + jωτ_k)`` (``SCHOENLEBER2014.voigt-model``) with
  the ``τ_k`` fixed and log-spaced from ``1/ω_max`` to ``1/ω_min`` -- only the
  resistances are unknown, so it is linear least squares and has no starting
  values to get wrong;
* real and imaginary parts together, each weighted by the **measured**
  ``1/|Z|`` (the complex fit);
* add ``M`` one at a time and stop at the first ``M`` whose negative
  resistances weigh more than 15 % of the positive ones --
  ``μ = 1 − Σ|R_k<0| / Σ|R_k≥0| < 0.85`` (``SCHOENLEBER2014.mu-threshold-c``).
  An ideal spectrum does not oscillate, and fixed-τ elements only oscillate
  with negative resistances, so μ falling is over-fitting starting;
* the residuals ``Δ = (Z − Ẑ)/|Z|``, real and imaginary apart
  (``SCHOENLEBER2014.residuals``), are the result.

A series capacitor joins the model when the low-frequency end diverges
capacitively (a blocking cell), and a series inductor when the top of the sweep
is inductive (cables) -- both as the paper does for its measured cells.  A
blocking spectrum without the capacitor cannot be matched by elements whose
resistances all return to the axis (``LASIA1999.kk-blocking-systems``).

**What the paper does not give is a threshold on the residuals**
(``SCHOENLEBER2014.no-numeric-residual-threshold``).  The verdicts built on
this in `audit` use our own numbers and say so.

Numpy only -- ``np.linalg.lstsq`` is the whole solver.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

__all__ = ["KKResult", "MU_LIMIT", "lin_kk"]

#: ``c`` of Schönleber et al. -- "from the author's experience ... an excellent
#: choice", and the value their validation used.
MU_LIMIT = 0.85
#: Fewer points than this and the test has nothing to say.
FEWEST_POINTS = 8


@dataclass(frozen=True)
class KKResult:
    """The linear KK test of one spectrum.

    ``judged`` is ``False`` when there was nothing to test (too few points),
    and then ``reason`` says why and the arrays are empty.
    """

    judged: bool
    reason: str = ""
    frequency_hz: np.ndarray = field(default_factory=lambda: np.empty(0))
    #: ``(Z_re − Ẑ_re)/|Z|`` and ``(Z_im − Ẑ_im)/|Z|``, point by point.
    residual_re: np.ndarray = field(default_factory=lambda: np.empty(0))
    residual_im: np.ndarray = field(default_factory=lambda: np.empty(0))
    fitted: np.ndarray = field(default_factory=lambda: np.empty(0, dtype=complex))
    #: Voigt elements used, and per decade of the sweep.
    m: int = 0
    per_decade: float = 0.0
    mu: float = 1.0
    #: μ for every ``M`` tried, from 1.
    mu_trace: tuple[float, ...] = ()
    with_capacitance: bool = False
    with_inductance: bool = False
    #: μ never fell below the limit before ``M`` reached its cap.
    capped: bool = False

    @property
    def residual(self) -> np.ndarray:
        """``|Z − Ẑ|/|Z|`` -- both parts together."""
        return np.hypot(self.residual_re, self.residual_im)

    @property
    def max_residual(self) -> float | None:
        return float(np.max(self.residual)) if self.residual.size else None

    @property
    def at_hz(self) -> float | None:
        """Where the largest residual is."""
        if not self.residual.size:
            return None
        return float(self.frequency_hz[int(np.argmax(self.residual))])

    @property
    def rms(self) -> float | None:
        if not self.residual.size:
            return None
        return float(np.sqrt(np.mean(self.residual_re ** 2 + self.residual_im ** 2)))

    @property
    def decades(self) -> float:
        if self.frequency_hz.size < 2:
            return 0.0
        return float(np.log10(self.frequency_hz.max() / self.frequency_hz.min()))


def _time_constants(omega_min: float, omega_max: float, m: int) -> np.ndarray:
    """``τ_1 = 1/ω_max … τ_M = 1/ω_min``, equal steps in log (paper Eqs. 10–12).

    ``M = 1`` is not defined there; one element sits in the middle of the band.
    """
    if m == 1:
        return np.array([1.0 / math.sqrt(omega_min * omega_max)])
    return np.logspace(math.log10(1.0 / omega_max), math.log10(1.0 / omega_min), m)


def _design(omega: np.ndarray, tau: np.ndarray, weight: np.ndarray, *,
            with_capacitance: bool, with_inductance: bool) -> np.ndarray:
    """Rows ``[real; imaginary]``, columns ``R_ohm, R_1..R_M, (1/C), (L)``."""
    wt = omega[:, None] * tau[None, :]
    real = [np.ones_like(omega)[:, None], 1.0 / (1.0 + wt ** 2)]
    imag = [np.zeros_like(omega)[:, None], -wt / (1.0 + wt ** 2)]
    if with_capacitance:
        real.append(np.zeros_like(omega)[:, None])
        imag.append((-1.0 / omega)[:, None])
    if with_inductance:
        real.append(np.zeros_like(omega)[:, None])
        imag.append(omega[:, None])
    top = np.hstack(real) * weight[:, None]
    bottom = np.hstack(imag) * weight[:, None]
    return np.vstack([top, bottom])


def _mu(resistances: np.ndarray) -> float:
    positive = float(np.sum(resistances[resistances >= 0]))
    negative = float(np.sum(np.abs(resistances[resistances < 0])))
    if positive <= 0:
        return -math.inf
    return 1.0 - negative / positive


def _diverges_capacitively(frequency: np.ndarray, z_im: np.ndarray) -> bool:
    """The lowest points climb: ``−Im Z`` grows as the frequency falls.

    Not the phase: a blocking cell with a large resistance still has a shallow
    phase at the last point, but its ``−Im Z`` keeps rising (a closed arc's
    falls back to the axis).
    """
    order = np.argsort(frequency)[:3]           # 가장 낮은 셋, 낮은 것부터
    minus_im = -z_im[order]
    return bool(np.all(minus_im > 0) and np.all(np.diff(minus_im) < 0))


def lin_kk(frequency_hz, z_re, z_im, *, mu_limit: float = MU_LIMIT,
           capacitance: bool | None = None, inductance: bool | None = None,
           max_per_decade: float = 12.0) -> KKResult:
    """The linear Kramers–Kronig test, sized by μ.

    ``capacitance`` / ``inductance``: add a series C / L to the model; ``None``
    decides from the spectrum (C when the lowest points climb capacitively, L
    when the top of the sweep is above the axis).  ``max_per_decade`` caps
    ``M`` -- above the point density it is over-fitting by construction
    (``SCHOENLEBER2014``, p. 26); the cap is also never above the number of
    equations.
    """
    frequency = np.asarray(frequency_hz, dtype=np.float64).ravel()
    real = np.asarray(z_re, dtype=np.float64).ravel()
    imag = np.asarray(z_im, dtype=np.float64).ravel()
    if not (frequency.size == real.size == imag.size):
        return KKResult(False, "주파수와 임피던스의 점 수가 다릅니다")
    good = (np.isfinite(frequency) & np.isfinite(real) & np.isfinite(imag)
            & (frequency > 0) & (np.hypot(real, imag) > 0))
    frequency, real, imag = frequency[good], real[good], imag[good]
    if frequency.size < FEWEST_POINTS:
        return KKResult(False, f"점이 {frequency.size}개뿐이라 KK 를 볼 수 없습니다")
    if frequency.max() / frequency.min() < 10:
        return KKResult(False, "측정 대역이 한 decade 가 안 됩니다")

    z = real + 1j * imag
    omega = 2.0 * np.pi * frequency
    weight = 1.0 / np.abs(z)
    target = np.concatenate([real * weight, imag * weight])
    with_c = (_diverges_capacitively(frequency, imag) if capacitance is None
              else bool(capacitance))
    top = np.argsort(frequency)[::-1][:3]
    with_l = bool(np.any(imag[top] > 0)) if inductance is None else bool(inductance)
    extra = 1 + int(with_c) + int(with_l)
    decades = math.log10(frequency.max() / frequency.min())
    cap = max(1, min(int(math.ceil(max_per_decade * decades)),
                     2 * frequency.size - extra - 1))

    trace: list[float] = []
    chosen = None
    for m in range(1, cap + 1):
        tau = _time_constants(omega.min(), omega.max(), m)
        design = _design(omega, tau, weight, with_capacitance=with_c,
                         with_inductance=with_l)
        solution, *_ = np.linalg.lstsq(design, target, rcond=None)
        mu = _mu(solution[1:1 + m])
        trace.append(mu)
        chosen = (m, tau, solution)
        if mu < mu_limit:
            break
    m, tau, solution = chosen
    capped = trace[-1] >= mu_limit

    wt = omega[:, None] * tau[None, :]
    resistances = solution[1:1 + m]
    fitted = solution[0] + np.sum(resistances[None, :] / (1.0 + 1j * wt), axis=1)
    at = 1 + m
    if with_c:
        fitted = fitted - 1j * solution[at] / omega
        at += 1
    if with_l:
        fitted = fitted + 1j * omega * solution[at]
    magnitude = np.abs(z)
    return KKResult(
        judged=True, frequency_hz=frequency,
        residual_re=(real - fitted.real) / magnitude,
        residual_im=(imag - fitted.imag) / magnitude,
        fitted=fitted, m=m, per_decade=m / decades if decades > 0 else float(m),
        mu=trace[-1], mu_trace=tuple(trace), with_capacitance=with_c,
        with_inductance=with_l, capped=capped)
