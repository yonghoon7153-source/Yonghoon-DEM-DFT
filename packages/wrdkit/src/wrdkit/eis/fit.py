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


#: 시작점을 몇 개나 흩을까.  확산이 든 회로는 더 많이 -- 위 docstring 참고.
_DEFAULT_RESTARTS = 8
_DIFFUSION_RESTARTS = 24

#: 훑기 한 번에 허용하는 함수 호출 수.  골짜기를 **고르는** 데는 이만큼이면
#: 충분하고, 바닥까지 내려가는 것은 다음 단계의 일이다.
_SCREEN_NFEV = 200

#: 끝까지 미는 시작점의 수, 그리고 그때의 예산.
_POLISH_KEEP = 4
_POLISH_NFEV = 4000


def _is_warburg_sigma(model, name: str) -> bool:
    """``W`` 의 단일 파라미터인가.  ``Ws_R``/``Wo_R`` 은 저항이라 아니다."""
    if "_" in name:
        return False
    return name.startswith("W") and not name.startswith(("Ws", "Wo"))


#: 자릿수를 넘나드는 파라미터의 접미사 — 여기에 걸리면 **결정된 사다리**로
#: 훑고, 재시작도 늘린다.
#:
#: 예전에는 `_tau` 와 반무한 `W` 의 σ 만 봤다.  그래서 전송선(`TL`)이 통째로
#: 빠졌다: 그 시간상수 이름은 `_Wt` 라 `_tau` 로 끝나지 않고, σ 도 아니다.
#: 결과가 화면에 그대로 찍혔다 — `Ws` 회로는 `시작점 29`, 파라미터가 **열셋**
#: 으로 더 어려운 `TL` 회로는 `시작점 9`.  더 험한 지형을 더 적은 시작점으로
#: 훑고 있었고, 그래서 저주파 꼬리를 놓친 채 멈춘 답이 나왔다.
_WIDE_SUFFIXES = ("_tau", "_Wt", "_Wr")


def _is_wide(model, name: str) -> bool:
    return name.endswith(_WIDE_SUFFIXES) or _is_warburg_sigma(model, name)


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
                restarts: int | None = None,
                seed: int = 0) -> FitResult:
    """Fit *circuit* to *spectrum* and say how well it went.

    ``drop_inductive`` removes the points above the real axis.  They are wiring,
    not cell, and no cell circuit reproduces them -- but the count comes back in
    the result so the screen can say how many went.

    ``restarts`` scatters extra starting points around the data-driven guess
    (a factor of a few on each parameter, log-uniform).  Left unset it depends
    on the circuit: eight for plain arc circuits, and more when a diffusion
    element is present.  Those have one more decade-wide parameter and a second
    shallow minimum beside the answer (a long ``tau`` imitating a semi-infinite
    Warburg), and eight starts reached the better of the two on only two of six
    seeds on the lab's own solid-state sweep -- the same spectrum and circuit
    reporting chi-square 1.0e-3 or 9.6e-3 depending on nothing the user can
    see.  Twenty-four reached it on five of six, and the two-stage search below
    made that no slower than eight used to be.
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

    if restarts is None:
        restarts = (_DIFFUSION_RESTARTS
                    if any(_is_wide(model, name) for name in model.parameter_names)
                    else _DEFAULT_RESTARTS)

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

    # 확산 파라미터는 **결정된 사다리**로도 훑는다.
    #
    # 꼬리가 화면 안에서 꺾이지 않으면 tau 는 하한만 알 수 있고, 그 하한
    # 근처에는 "tau 를 크게 보내 반무한 Warburg 를 흉내내는" 얕은 골이 하나 더
    # 있다.  무작위 산포(로그 다섯 배)로는 그 골에서 못 나오고, 산포를 넓히면
    # 이번에는 **뽑기 운**에 답이 달린다 -- 같은 스펙트럼 같은 회로가 seed 에
    # 따라 chi^2 1.4e-3 과 1.0e-2 사이를 오갔다.  그래서 무작위 대신 두
    # 자릿수를 양쪽으로 결정적으로 훑는다: 결과가 재현되고, 스윕 스물한 개가
    # 서로 비교 가능해진다.
    wide = [i for i, name in enumerate(model.parameter_names)
            if _is_wide(model, name)]
    for i in wide:
        for factor in (1e-2, 1e-1, 1e1, 1e2):
            candidate = start.copy()
            candidate[i] = float(np.clip(start[i] * factor,
                                         model.lower[i] * 1.0001,
                                         model.upper[i] * 0.9999))
            starts.append(candidate)

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

    def solve(candidate, budget):
        try:
            solution = least_squares(
                lambda free: _residuals(
                    _from_unbounded(free, model.lower, model.upper),
                    model, working.frequency_hz, z, weights),
                _to_unbounded(candidate, model.lower, model.upper),
                method="lm", max_nfev=budget)
        except (ValueError, FloatingPointError):
            return None
        if not np.all(np.isfinite(solution.fun)):
            return None
        return solution

    # 두 단계로 나눈다: **싸게 훑고, 몇 개만 끝까지.**
    #
    # 한 시작점을 끝까지 미는 데 드는 비용이 대충 훑는 비용의 스무 배다.  전부
    # 끝까지 밀면 시작점을 스물넷으로 늘리는 것이 그대로 스물넷 배가 되고,
    # 그래서 여덟에 묶여 있었다 -- 그런데 확산이 든 회로(파라미터 아홉 개)는
    # 여덟으로 부족했다: 실측 스윕 하나에서 seed 여섯 개 중 둘만 최소에
    # 도달했고, 나머지는 chi^2 가 아홉 배인 답을 냈다.  같은 스펙트럼 같은
    # 회로가 뽑기에 따라 다른 답을 내는 것은 보고할 수 없는 수다.
    screened = []
    for index, candidate in enumerate(starts):
        solution = solve(candidate, _SCREEN_NFEV)
        if solution is None:
            continue
        screened.append((float(np.sum(solution.fun ** 2)), index,
                         _from_unbounded(solution.x, model.lower, model.upper)))
    screened.sort(key=lambda item: item[0])

    best = None
    converged_count = 0
    seen: set[int] = set()
    for _, index, polished_start in screened[:_POLISH_KEEP]:
        seen.add(index)
        solution = solve(polished_start, _POLISH_NFEV)
        if solution is None:
            continue
        converged_count += 1
        cost = float(np.sum(solution.fun ** 2))
        if best is None or cost < best[0]:
            best = (cost, solution)
    # 훑기에서 살아남았지만 다듬지 않은 것들도 "수렴했다" 에는 든다 -- 그 수는
    # 화면이 "몇 곳에서 출발해 몇 곳이 답에 닿았나" 로 읽는 값이다.
    converged_count += sum(1 for _, index, _ in screened if index not in seen)

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

    at_bound = []
    for parameter, low, high in zip(parameters, model.lower, model.upper,
                                    strict=True):
        if not (parameter.value <= low * 1.01 or parameter.value >= high * 0.99):
            continue
        at_bound.append(parameter.name)
        # 경계에 눌린 파라미터는 자유롭지 않다.  그 자리의 공분산은 "이 값을
        # 얼마나 잘 쟀나" 가 아니라 "벽이 얼마나 단단한가" 이고, 작은 오차
        # 막대는 가장 정밀해 보이는 숫자를 가장 못 본 숫자에 붙인다 (§0.4).
        parameter.stderr = None
    notes = []
    if at_bound:
        notes.append("물리적 한계에 붙은 파라미터: " + ", ".join(at_bound)
                     + " — 회로가 이 스펙트럼을 설명하지 못한다는 뜻일 수 있습니다")
    # 전송선의 두 레일은 맞바꿔도 임피던스가 **정확히** 같다 (circuit.py 의
    # `transmission_line` 을 보라).  둘을 서로 다른 측정값처럼 읽으면 안 되는데,
    # 화면에는 이름이 다른 두 줄로 나오므로 여기서 한 번 말해 준다.
    swappable = sorted({name.split("_")[0] for name in model.parameter_names
                        if name.endswith(("_Ri", "_Re"))})
    if swappable:
        notes.append(", ".join(f"{name}_Ri ↔ {name}_Re" for name in swappable)
                     + " 는 맞바꿔도 같은 곡선입니다 — 스펙트럼은 둘의 짝만 "
                       "정하고 어느 쪽이 이온인지는 말하지 않습니다")
    reason = " / ".join(notes)

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

    # 데이터가 그 파라미터를 보고 있는가.  야코비안 컬럼이 수치적으로 0 이면
    # (절단 SVD 가 그 방향의 분산을 0 으로 만든다) stderr 가 ~0 이 되어,
    # **아무 정보도 없는** 파라미터가 "초정밀 측정값" 으로 보고된다 -- 리뷰
    # 재현: 무너진 가지의 CPE_n=1.000 이 stderr 1e-27, determined=True.
    # 경계에 눌린 파라미터(frac→0/1, dp/dfree→0)도 같은 길로 0 이 된다.
    # 둘 다 "모른다" 이므로 None 으로 낸다 (§0.4).
    column_norms = np.linalg.norm(jac, axis=0)
    biggest = float(np.max(column_norms)) if column_norms.size else 0.0
    blind = column_norms <= np.finfo(float).eps * max(jac.shape) * biggest
    pressed = (frac <= 1e-9) | (frac >= 1 - 1e-9)
    # 내부 축퇴: 한 아크가 두 가지로 쪼개져 같은 τ 를 공유하면 개별 컬럼은
    # 살아 있어도 그 **차이 방향**이 널이다.  절단 SVD 가 버린 방향에 파라미터
    # 축이 절반 넘게 실려 있으면, 그 파라미터의 분산은 계산에서 그 방향을 뺀
    # 과소평가다 -- 개별값이 아무 뜻 없는 R1=37.5/R2=2.5 가 "정밀" 로 나온다.
    if np.any(~good):
        leak = np.sqrt(np.sum(vt[~good] ** 2, axis=0))
    else:
        leak = np.zeros(len(values))
    degenerate = leak > 0.5

    out: list[float | None] = []
    for i, var in enumerate(variance):
        usable = (np.isfinite(var) and var >= 0
                  and not blind[i] and not pressed[i] and not degenerate[i])
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
