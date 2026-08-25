"""Complex non-linear least squares, run enough times to be trusted.

The lab's procedure is: guess, fit, look at the shape, look at chi-square, fix
some parameters, fit again.  The sheet even warns that *우연하게 말도 안 되는
것을 집어넣어도 피팅이 되는 경우가 있음* -- a fit can converge on numbers that
are not measurements.  So this module does three things a single call to an
optimiser does not:

* it starts from several places (the data-driven guess and scattered variants)
  and keeps the best, because one start finds one local minimum;
* it reports a confidence interval per parameter, from the Jacobian at the
  solution, and marks a parameter whose interval swamps its own value as
  **undetermined** rather than printing it as a measurement (§0.4);
* it says which frequencies it actually used, since dropping the inductive tail
  moves the series resistance and a number that moved silently is worse than no
  number.

Weighting is proportional (each residual divided by |Z|).  Impedance spans
decades within one spectrum -- ohms at high frequency, kiloohms at low -- so
unweighted least squares fits the low-frequency end and ignores everything
else.  This is what ZView calls "Calc-Modulus" and what its chi-square means.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .circuit import Circuit, parse_circuit
from .guess import inductive_mask, initial_guess
from .spectrum import Spectrum

__all__ = ["FitResult", "Parameter", "fit_circuit", "SCIPY_MISSING"]

SCIPY_MISSING = (
    "이 피팅에는 scipy 가 필요합니다 — `pip install 'wrdkit[eis]'` "
    "(닫힌 해가 없어 최적화가 필요하고, 신뢰구간은 해에서의 야코비안에서 나옵니다)"
)


@dataclass
class Parameter:
    """One fitted number and how much of it is real."""

    name: str
    value: float
    unit: str = ""
    #: One standard error, from the covariance at the solution.  ``None`` when
    #: the Jacobian was singular -- which itself is a finding: the parameter
    #: does not change the fit.
    stderr: float | None = None

    @property
    def relative_error(self) -> float | None:
        if self.stderr is None or not np.isfinite(self.stderr) or self.value == 0:
            return None
        return abs(self.stderr / self.value)

    @property
    def determined(self) -> bool:
        """False when the error bar is as big as the value.

        A parameter like that has not been measured.  ZView prints it anyway;
        we mark it, because the number reads exactly like the ones that mean
        something.
        """
        relative = self.relative_error
        if relative is None:
            return False
        return relative < 0.5


@dataclass
class FitResult:
    circuit: str
    parameters: list[Parameter]
    #: Sum of squared proportional residuals, divided by degrees of freedom.
    #: Comparable between spectra, which the raw sum is not.
    chi_squared: float
    #: Per-point proportional residuals, real and imaginary interleaved.
    residuals: np.ndarray = field(repr=False)
    #: Frequencies the fit was computed on, after any trimming.
    frequency_hz: np.ndarray = field(repr=False)
    #: The model's impedance at those frequencies.
    fitted: np.ndarray = field(repr=False)
    converged: bool = True
    #: Why not, when not.  Empty on success.
    reason: str = ""
    #: How many starting points were tried and how many reached a solution.
    starts: int = 1
    starts_converged: int = 1
    #: Points dropped before fitting, and why.
    dropped_inductive: int = 0
    dropped_out_of_range: int = 0

    def values(self) -> dict[str, float]:
        return {p.name: p.value for p in self.parameters}

    @property
    def undetermined(self) -> list[str]:
        return [p.name for p in self.parameters if not p.determined]


def _residuals(values, circuit, frequency, z, weights):
    model = circuit.impedance(values, frequency)
    diff = model - z
    return np.concatenate([diff.real * weights, diff.imag * weights])


def _to_unbounded(values, lower, upper):
    """Map a bounded parameter onto the whole line, in log space.

    Resistances and CPE magnitudes span orders of magnitude, so a linear step
    that is sensible for a 40 ohm resistor is meaningless for a 1e-5 CPE.  In
    log space one step means one factor for both.
    """
    span = np.log(upper) - np.log(lower)
    frac = (np.log(values) - np.log(lower)) / span
    frac = np.clip(frac, 1e-9, 1 - 1e-9)
    return np.log(frac / (1 - frac))


def _from_unbounded(free, lower, upper):
    frac = 1.0 / (1.0 + np.exp(-np.clip(free, -700, 700)))
    span = np.log(upper) - np.log(lower)
    return np.exp(np.log(lower) + frac * span)


def fit_circuit(spectrum: Spectrum, circuit: str | Circuit, *,
                guess: np.ndarray | None = None,
                drop_inductive: bool = True,
                frequency_range: tuple[float, float] | None = None,
                restarts: int = 8,
                seed: int = 0) -> FitResult:
    """Fit *circuit* to *spectrum* and say how well it went.

    ``drop_inductive`` removes the points above the real axis.  They are wiring,
    not cell, and no cell circuit reproduces them -- but the count comes back in
    the result so the screen can say how many went.

    ``restarts`` scatters extra starting points around the data-driven guess
    (a factor of a few on each parameter, log-uniform).  Eight is enough to
    escape the shallow local minima this family of circuits has, and cheap:
    each fit is a few milliseconds on a hundred points.
    """
    try:
        from scipy.optimize import least_squares
    except ImportError as exc:                       # pragma: no cover
        raise ImportError(SCIPY_MISSING) from exc

    model = circuit if isinstance(circuit, Circuit) else parse_circuit(circuit)

    working = spectrum.sorted_by_frequency(descending=True)
    dropped_inductive = 0
    if drop_inductive:
        mask = ~inductive_mask(working)
        dropped_inductive = int(np.sum(~mask))
        working = working.select(mask)

    dropped_range = 0
    if frequency_range is not None:
        low, high = sorted(frequency_range)
        mask = (working.frequency_hz >= low) & (working.frequency_hz <= high)
        dropped_range = int(np.sum(~mask))
        working = working.select(mask)

    n_params = len(model.parameter_names)
    if len(working) < n_params:
        return _failed(model, working,
                       f"점이 {len(working)}개뿐이라 파라미터 {n_params}개를 "
                       "결정할 수 없습니다", dropped_inductive, dropped_range)

    z = working.z
    magnitude = np.abs(z)
    if not np.all(np.isfinite(magnitude)) or np.any(magnitude == 0):
        return _failed(model, working, "스펙트럼에 0 이거나 유한하지 않은 점이 있습니다",
                       dropped_inductive, dropped_range)
    weights = 1.0 / magnitude

    start = np.asarray(guess, dtype=float) if guess is not None else \
        initial_guess(working, model)
    start = np.clip(start, model.lower * 1.0001, model.upper * 0.9999)

    rng = np.random.default_rng(seed)
    starts = [start]
    for _ in range(max(0, restarts)):
        scatter = np.exp(rng.uniform(-np.log(5.0), np.log(5.0), size=n_params))
        candidate = np.clip(start * scatter, model.lower * 1.0001,
                            model.upper * 0.9999)
        # Exponents are not scale-free; scattering 0.85 by a factor of five
        # lands outside the physical range every time.
        for i, name in enumerate(model.parameter_names):
            if name.endswith("_n"):
                candidate[i] = float(np.clip(start[i] + rng.uniform(-0.15, 0.15),
                                             model.lower[i] + 1e-6,
                                             model.upper[i] - 1e-6))
        starts.append(candidate)

    best = None
    converged_count = 0
    for candidate in starts:
        try:
            solution = least_squares(
                lambda free: _residuals(
                    _from_unbounded(free, model.lower, model.upper),
                    model, working.frequency_hz, z, weights),
                _to_unbounded(candidate, model.lower, model.upper),
                method="lm", max_nfev=4000)
        except (ValueError, FloatingPointError):
            continue
        if not np.all(np.isfinite(solution.fun)):
            continue
        converged_count += 1
        cost = float(np.sum(solution.fun ** 2))
        if best is None or cost < best[0]:
            best = (cost, solution)

    if best is None:
        return _failed(model, working, "어느 시작점에서도 수렴하지 않았습니다",
                       dropped_inductive, dropped_range)

    cost, solution = best
    values = _from_unbounded(solution.x, model.lower, model.upper)
    residuals = solution.fun
    dof = max(len(residuals) - n_params, 1)
    chi2 = cost / dof

    stderrs = _standard_errors(solution, values, model, chi2, dof)
    values, stderrs = _order_arcs_by_frequency(model, values, stderrs)
    parameters = [
        Parameter(name=name, value=float(value), unit=unit, stderr=stderr)
        for name, unit, value, stderr in zip(
            model.parameter_names, model.parameter_units, values, stderrs,
            strict=True)
    ]

    at_bound = [p.name for p, low, high in zip(parameters, model.lower,
                                               model.upper, strict=True)
                if p.value <= low * 1.01 or p.value >= high * 0.99]
    reason = ""
    if at_bound:
        reason = ("물리적 한계에 붙은 파라미터: " + ", ".join(at_bound)
                  + " — 회로가 이 스펙트럼을 설명하지 못한다는 뜻일 수 있습니다")

    return FitResult(
        circuit=model.text,
        parameters=parameters,
        chi_squared=float(chi2),
        residuals=residuals,
        frequency_hz=working.frequency_hz,
        fitted=model.impedance(values, working.frequency_hz),
        converged=True,
        reason=reason,
        starts=len(starts),
        starts_converged=converged_count,
        dropped_inductive=dropped_inductive,
        dropped_out_of_range=dropped_range,
    )


def _order_arcs_by_frequency(model, values, stderrs):
    """Put the R-CPE branches in frequency order, fastest first.

    ``p(R1,CPE1)-p(R2,CPE2)`` is the same circuit as the same two branches the
    other way round, so an optimiser is free to return either -- and it does,
    depending on where it started.  That is fine as arithmetic and wrong as a
    report: the names carry physics.  In a liquid cell the first arc is the SEI
    and the second is charge transfer; in an ion-blocking solid cell the first
    is the grain interior and the second the grain boundary (ADR 0019).  Swap
    them and every label is on the wrong number.

    The characteristic frequency of an R-CPE pair is ``(R Q)^(-1/n)``, so the
    branches can be sorted by something measured rather than by which one the
    optimiser happened to move first.
    """
    names = list(model.parameter_names)
    branches = []
    # 짝은 괄호가 정의한다.  "CPE 바로 앞의 맨 R" 로 찾던 첫 구현은
    # p(CPE1,R1) 표기에서 직렬저항을 아크와 맞바꿨다 -- 재정렬된 값으로
    # fitted 까지 다시 계산되어, chi² 는 완벽한데 곡선은 데이터와 35 Ω
    # 어긋나는 보고서가 나왔다.
    for r_name, cpe_name in model.parallel_rc_branches():
        r_at = names.index(r_name)
        q_at = names.index(cpe_name + "_Q")
        n_at = names.index(cpe_name + "_n")
        r, q, n = values[r_at], values[q_at], values[n_at]
        omega = (r * q) ** (-1.0 / n) if r > 0 and q > 0 and n > 0 else 0.0
        branches.append((omega, (r_at, q_at, n_at)))

    if len(branches) < 2:
        return values, stderrs
    order = [slots for _, slots in sorted(branches, key=lambda item: -item[0])]
    original = [slots for _, slots in branches]

    new_values = np.array(values, dtype=float)
    new_errors = list(stderrs)
    for target, source in zip(original, order, strict=True):
        for to, frm in zip(target, source, strict=True):
            new_values[to] = values[frm]
            new_errors[to] = stderrs[frm]
    return new_values, new_errors


def _standard_errors(solution, values, model, chi2, dof) -> list[float | None]:
    """Errors on the **fitted** parameters, not on the transformed ones.

    The optimiser works on a squashed, logarithmic coordinate; its covariance
    is in that coordinate too.  Reporting it directly would give a resistance
    an error bar in units of nothing.  The chain rule puts it back:
    ``sigma_p = |dp/dfree| * sigma_free``.
    """
    jac = solution.jac
    try:
        _, s, vt = np.linalg.svd(jac, full_matrices=False)
    except np.linalg.LinAlgError:                    # pragma: no cover
        return [None] * len(values)
    threshold = np.finfo(float).eps * max(jac.shape) * (s[0] if len(s) else 0)
    good = s > threshold
    if not np.any(good):
        return [None] * len(values)
    covariance = (vt[good].T / s[good] ** 2) @ vt[good]
    variance = np.diag(covariance) * chi2

    # dp/dfree for p = lower * (upper/lower)^sigmoid(free)
    span = np.log(model.upper) - np.log(model.lower)
    frac = (np.log(values) - np.log(model.lower)) / span
    frac = np.clip(frac, 1e-12, 1 - 1e-12)
    derivative = values * span * frac * (1 - frac)

    out: list[float | None] = []
    for i, var in enumerate(variance):
        usable = np.isfinite(var) and var >= 0
        out.append(float(np.sqrt(var) * abs(derivative[i])) if usable else None)
    return out


def _failed(model, working, reason, dropped_inductive, dropped_range) -> FitResult:
    """A result that carries the reason instead of numbers (§0.4)."""
    return FitResult(
        circuit=model.text,
        parameters=[],
        chi_squared=float("nan"),
        residuals=np.array([]),
        frequency_hz=working.frequency_hz,
        fitted=np.array([], dtype=complex),
        converged=False,
        reason=reason,
        starts=0,
        starts_converged=0,
        dropped_inductive=dropped_inductive,
        dropped_out_of_range=dropped_range,
    )
