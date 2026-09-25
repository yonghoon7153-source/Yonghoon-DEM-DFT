"""검수가 권한 회로로 다시 맞추기 — 무엇을, 어디서 시작해, 받아들일지 (ADR 0045).

맞추기와 저장은 API 가 한다 (`POST /api/eis/audit/refit`, `bml refit`).  여기는
그 사이의 판단만 둔다.

- `refit_candidates` — 문제 판정이 실은 회로를 어떤 순서로, 어느 하한부터 맞춰
  볼지.  저주파 끝이 KK 를 어겼으면 쓰는 회로도 그 하한부터 다시 맞춰 본다 (보완 4).
  배선 인덕턴스가 빠졌으면 앞에 ``L1-`` 를 붙인 회로도 맞춰 본다 (보완 8).  차가운
  펠릿의 아크가 구간 위에 걸쳤으면 아크 하나를 더한 회로도 맞춰 본다 (보완 10).
- `seed_values` — 쓰는 맞춤의 값을 새 회로의 어느 파라미터로 옮길지.
  `seed_arc` — 더한 아크는 판정이 아는 수(교점, 옛 직렬 저항)에서 시작한다.
- `accept_refit` — 새 맞춤을 다시 검수한 결과를 받아들일지.
- `moved_number` — 받아들여도, 모양을 덜 그리면서 σ 의 저항을 옮기면 안 받는다.
- `electrolyte_short` — 아크를 더한 맞춤의 σ 저항이 교점에 못 미치면 안 받는다.
- `remaining_problems` — 받아들여진 것이 여럿이면 무엇을 고를지.

**받아들이는 잣대는 검수 자신이다.**  χ² 는 파라미터 수가 다른 회로를 견주지
못한다 — 권한 회로는 옛 회로보다 단순해서 χ² 가 거의 늘 더 크다.  그래서 "더 잘
맞았나" 를 묻지 않고 "그 문제가 풀렸나, 없던 문제가 생겼나, 모양을 그리나" 를
묻는다.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass

import numpy as np

from .audit import ARC_ABOVE_SHARE, PROBLEM, Finding
from .circuit import BLOCKING_KINDS, Circuit, CircuitError, parse_circuit
from .guess import ARC_START_N

#: σ 에 쓰는 저항이 이 비율보다 많이 움직이면서 맞춤이 더 어긋나면 받지 않는다
#: (`moved_number`).  판단이다: 합성 펠릿에서 아크 없는 회로가 전극 크기 아크(1.5 Ω)를
#: 삼키자 R0 가 8.0 → 9.34 Ω (+17 %) 로 갔고 오차는 1 % 라 검수는 받아들였다.
#: 모양을 더 잘 그리는 맞춤은 이 문턱과 상관없이 받는다.
RESISTANCE_SHIFT_LIMIT = 0.05

#: 평균 오차가 이만큼(퍼센트포인트 0.5)까지 늘면 **같은 그림**으로 본다.  실측 B12
#: #4 는 1.9 → 2.0 % 였다 — 그 셀의 KK 잡음(σ 0.28 %) 안이고, 옛 맞춤은 배선 L 이
#: 없어 고주파 끝이 12 % 어긋나 있었다.  그 0.1 을 "더 어긋난다" 로 읽어 L 보정을
#: 막았다 (첫 적용, 2026-09-23 17:03 UTC).
MISFIT_TOLERANCE = 0.005

#: 이것이 **새로** 뜨면 받아들이지 않는다 — "회로가 이 스펙트럼의 모양을 못
#: 그립니다".  이름을 고치려고 모양을 못 그리는 회로로 바꾸지 않는다.  심각도
#: (확인)와 상관없이 막는다.  옛 맞춤도 같은 판정이었으면 더 어긋나지만 않으면
#: 된다 — 실측 B15 #9 · B16 #9 의 옛 `R0-p(R1,CPE1)` 는 R1 이 10⁹ Ω 로 가 곧
#: `R0-CPE1` 이었고, 새 `L1-R0-CPE1` 와 둘 다 3.2 % 였다.  같은 모양을 이름만 바로
#: 그린 것을 모양 탓으로 막았다.
SHAPE_CODES = ("misfit_everywhere",)

#: 확인인데도 실은 회로로 다시 맞추는 판정 (보완 8).  배선 소자를 더할 뿐이라 셀을
#: 읽는 방식 — 아크의 수·이름, σ 에 쓰는 소자 — 이 그대로다.  사람이 고를 것이
#: 없다.  다른 확인은 사람 몫이다 (결정 3).
WIRING_CODES = ("inductance_missing",)

#: 확인인데도 실은 회로로 다시 맞추는 판정 중, 셀을 읽는 방식이 바뀌는 것 (보완 10).
#: 차가운 펠릿의 전해질 아크가 구간 위에 걸쳐, 아크 없는 회로의 R0 도 교점도 전해질
#: 저항을 작게 읽는다.  아크를 더하면 σ 의 저항이 R0 에서 R0 + R1 로 간다.  그래도
#: 사람이 고를 것이 없다 — 판정이 까닭을 말하고, `accept_refit` 과
#: `electrolyte_short` 가 새 맞춤에서 그 까닭을 확인한다.
ARC_CODES = ("arc_above_window",)

#: 회로를 부르는 확인 전부.
REFIT_CHECKS = WIRING_CODES + ARC_CODES

#: 아크를 더한 맞춤에 **새로** 뜨면 받지 않는 판정 — 고주파 절편이 0 으로 갔다
#: (보완 10).  판정의 까닭은 "R0 뒤, 교점 너머에 아크가 있다" 인데, R0 가 0 이면 더한
#: 소자가 절편까지 가져간 것이다.  실측 #123 (11:44 맞춰 보기): R0 1e-9 Ω (경계),
#: R1 143 Ω 한 덩어리의 넓은 분산(꼭지 74.5 MHz)이 σ 142.7 Ω 으로 받아들여졌다.
INTERCEPT_LOST = ("series_resistance_gone",)


@dataclass(frozen=True)
class Candidate:
    """다시 맞춰 볼 회로 하나와, 그것을 권한 문제 판정들."""

    circuit: str
    #: 이 회로를 권한 **문제** 판정의 코드.  다시 맞춘 뒤 이것들이 없어야 한다.
    #: 쓰는 회로를 하한만 올려 다시 맞추는 후보는 비었다 — 풀 문제 판정이 없다.
    triggers: tuple[str, ...]
    #: 맞출 주파수 창의 하한 — 저주파 끝이 Kramers–Kronig 를 어겨 판정이 권한 것
    #: (``Finding.low_hz``).  ``None`` 이면 쓰는 맞춤의 창 그대로다.
    low_hz: float | None = None
    #: 맞출 주파수 창의 상한 — 구간 위에 아크가 걸쳐 판정이 권한 것 (``Finding.high_hz``,
    #: 보완 10).  ``None`` 이면 쓰는 맞춤의 창 그대로다.
    high_hz: float | None = None


def refit_candidates(findings: Iterable[Finding], *,
                     circuit: str = "") -> list[Candidate]:
    """다시 맞춰 볼 것들 — 문제 판정이 권한 회로를 권한 순서대로 한 번씩, 그리고
    하한이 권해졌으면 쓰는 회로(``circuit``)를 그 하한부터, 맨 끝에.

    **문제**만 회로를 부른다.  확인(``open_end_on_blocking_cell`` 등)은 사람이 보고
    정할 일이라 한꺼번에 바꾸지 않는다 (ADR 0045).  같은 회로를 여러 판정이 권하면
    한 후보로 합치고 그 판정들을 모두 적는다 — 다시 맞춘 뒤 그 모두가 풀려야 한다.

    예외가 셋이다.  사람이 고를 것이 없는 것들이다.

    - 저주파 끝이 KK 를 어긴 판정(확인)이 싣는 하한(``low_hz``).  그 아래 점은
      셀이 변하는 동안 잰 것이라 **어느 회로로 맞추든** 뺀다 — 권한 회로도 그
      하한부터 맞춘다.  회로를 바꾸는 것이 아니라 점을 덜 쓰는 것이다 (보완 4).
    - 배선 인덕턴스가 빠졌다는 판정(`WIRING_CODES`, 확인)이 싣는 ``L1-`` 회로.
      셀을 읽는 방식은 그대로이고 케이블의 소자 하나를 더한다 (보완 8).
    - 구간 위에 아크가 걸쳤다는 판정(`ARC_CODES`, 확인)이 싣는, 아크 하나를 더한
      회로 (보완 10).  판정이 상한(``high_hz``)도 실으면 그 회로는 거기까지 맞춘다 —
      아크가 쓰는 맞춤의 구간 위에 있다.

    ``findings`` 에는 맞춤의 판정과 점의 판정을 같이 준다.
    """
    order: dict[str, list[str]] = {}
    high: dict[str, float] = {}
    low_hz: float | None = None
    for finding in findings:
        if finding.low_hz is not None:
            # 한 스펙트럼에 하한은 하나다 (`KKReference.low_limit_hz`).
            low_hz = finding.low_hz if low_hz is None else max(low_hz, finding.low_hz)
        if finding.severity != PROBLEM and finding.code not in REFIT_CHECKS:
            continue
        for offered in finding.circuits:
            codes = order.setdefault(offered, [])
            if finding.code not in codes:
                codes.append(finding.code)
            if finding.high_hz is not None:
                high[offered] = max(high.get(offered, 0.0), finding.high_hz)
    out = [Candidate(offered, tuple(codes), low_hz, high.get(offered))
           for offered, codes in order.items()]
    if low_hz is not None and circuit and circuit not in order:
        out.append(Candidate(circuit, (), low_hz))
    return out


def _blocking_tail(model: Circuit) -> tuple[str, str] | None:
    """직렬 경로의 마지막 막는 소자 ``(이름, 종류)`` — 없으면 ``None``."""
    tail = [(name, kind) for name, kind in model.series_element_kinds()
            if kind in BLOCKING_KINDS]
    return tail[-1] if tail else None


def _element(name: str) -> tuple[str, str]:
    """``CPE1_Q`` → ``("CPE1", "Q")``, ``R0`` → ``("R0", "")``."""
    head, _, suffix = name.partition("_")
    return head, suffix


def seed_values(old_circuit: str, old_values: Mapping[str, float],
                new_circuit: str, *, skip: Iterable[str] = ()) -> dict[str, float]:
    """쓰는 맞춤의 값 중 새 회로로 옮길 수 있는 것 — ``{새 파라미터: 값}``.

    - **이름이 같으면 이름으로** 옮긴다 (``R0`` → ``R0``, ``L1`` → ``L1``).
    - **끝의 막는 소자는 끝의 것끼리** 옮긴다.  옛
      ``R0-p(R1,CPE1)-p(R2,CPE2)-CPE3`` 의 꼬리 CPE3 는 새 ``L1-R0-CPE1`` 의
      CPE1 이다.  이름만 보면 옛 CPE1 — 아크의 것 — 이 새 꼬리로 들어간다.
      그래서 한쪽에서만 꼬리인 소자는 이름으로 옮기지 않는다.
    - ``skip`` (경계에 붙은 파라미터)은 옮기지 않는다.  그 값은 답이 아니라
      벽이다.

    못 옮긴 파라미터는 빠진다 — 맞추는 쪽이 데이터로 잡은 기본 시작점을 쓴다
    (`fit_circuit` 의 ``start_from``).  회로를 못 읽으면 빈 사전이다.

    왜 옮기나: 합성 펠릿(아크 하나 + 꼬리)에서 기본 시작점은 아크의 R 을
    상한으로 보냈고 오차가 3.0 % 였다.  참값 근처에서 시작하자 0.22 % 로 맞았다.
    """
    try:
        old = parse_circuit(old_circuit)
        new = parse_circuit(new_circuit)
    except CircuitError:
        return {}
    skipped = set(skip)
    old_tail = _blocking_tail(old)
    new_tail = _blocking_tail(new)
    same_tail = (old_tail is not None and new_tail is not None
                 and old_tail[1] == new_tail[1])
    seeded: dict[str, float] = {}
    for name in new.parameter_names:
        head, suffix = _element(name)
        is_new_tail = new_tail is not None and head == new_tail[0]
        if is_new_tail:
            if not same_tail:
                continue
            source = f"{old_tail[0]}_{suffix}" if suffix else old_tail[0]
        else:
            if old_tail is not None and head == old_tail[0]:
                continue
            source = name
        if source in skipped or source not in old_values:
            continue
        value = float(old_values[source])
        if np.isfinite(value):
            seeded[name] = value
    return seeded


def added_arc(old_circuit: str, new_circuit: str) -> tuple[str, str] | None:
    """``(R, CPE)`` of the arc the new circuit puts in front -- its fastest branch,
    when it has exactly one branch more than the old one.  ``None`` otherwise.

    Branches are reported fastest first (`fit_circuit`), so an arc added above the
    window is the new circuit's first branch.
    """
    try:
        old = parse_circuit(old_circuit)
        new = parse_circuit(new_circuit)
    except CircuitError:
        return None
    branches = new.parallel_rc_branches()
    if len(branches) != len(old.parallel_rc_branches()) + 1:
        return None
    return branches[0]


def seed_arc(old_circuit: str, old_values: Mapping[str, float], new_circuit: str, *,
             series_ohm: float, crossing_ohm: float, top_hz: float,
             skip: Iterable[str] = ()) -> dict[str, float]:
    """아크 하나를 앞에 더한 회로의 시작점 — `seed_values` 위에 더한 아크를 얹는다 (보완 10).

    `seed_values` 는 이름으로 옮긴다.  아크를 앞에 더하면 이름이 한 자리씩 어긋난다 —
    옛 ``R1`` 은 새 ``R2`` 다 (가지는 빠른 것부터, `fit_circuit`).  그래서 가지는 가지끼리
    한 자리 뒤로 옮기고, 맨 앞 가지는 판정이 아는 수로 채운다.

    - 직렬 저항은 교점(``crossing_ohm``)에서.  회로의 고주파 절편은 교점 위일 수 없다.
    - 더한 아크의 R 은 옛 직렬 저항 − 교점에서 — 옛 회로가 직렬 저항에 넣은, 교점
      너머의 몫이다.
    - 그 꼭지는 맞출 구간의 꼭대기(``top_hz``)에 두고 n 은 `ARC_START_N` 이다.

    **왜 데이터로 잡는 시작점이 아닌가.**  `initial_guess` 는 −Z'' 의 봉우리에서 아크를
    찾는데, 이 아크는 꼭지가 구간 위라 봉우리가 없다.  차가운 펠릿 쌍둥이에서 새 아크가
    꼬리의 봉우리(R1 8.8 kΩ, Q 1e-4)에서 시작했다.  옛 값만 옮기면 쌍둥이 열다섯 중
    여섯에서 아크가 꼬리를 삼켰다 (R1 10⁶ Ω, 꼬리의 n 0.3).  이 시작점에서는 열다섯
    모두 아크를 찾았다.

    가지가 정확히 하나 늘지 않았거나 직렬 저항이 하나가 아니면 `seed_values` 그대로다.
    """
    seeded = seed_values(old_circuit, old_values, new_circuit, skip=skip)
    try:
        old = parse_circuit(old_circuit)
        new = parse_circuit(new_circuit)
    except CircuitError:
        return seeded
    old_arcs = old.parallel_rc_branches()
    new_arcs = new.parallel_rc_branches()
    series = [name for name, kind in new.series_element_kinds() if kind == "R"]
    if len(new_arcs) != len(old_arcs) + 1 or len(series) != 1 \
            or not (crossing_ohm > 0 and top_hz > 0):
        return seeded
    for resistor, element in new_arcs:
        for name in (resistor, f"{element}_Q", f"{element}_n"):
            seeded.pop(name, None)
    skipped = set(skip)
    for (old_r, old_e), (new_r, new_e) in zip(old_arcs, new_arcs[1:], strict=True):
        for source, target in ((old_r, new_r), (f"{old_e}_Q", f"{new_e}_Q"),
                               (f"{old_e}_n", f"{new_e}_n")):
            value = old_values.get(source)
            if source not in skipped and value is not None and np.isfinite(value):
                seeded[target] = float(value)
    resistor, element = new_arcs[0]
    arc_ohm = max(series_ohm - crossing_ohm, ARC_ABOVE_SHARE * crossing_ohm)
    seeded[series[0]] = float(crossing_ohm)
    seeded[resistor] = float(arc_ohm)
    seeded[f"{element}_Q"] = float(1.0 / (arc_ohm * (2 * np.pi * top_hz) ** ARC_START_N))
    seeded[f"{element}_n"] = ARC_START_N
    return seeded


@dataclass(frozen=True)
class Acceptance:
    accepted: bool
    #: 받아들이지 않은 까닭 한 문장.  받아들였으면 빈 문자열.
    reason: str = ""


def _codes(findings: Iterable[Finding]) -> Counter:
    return Counter(finding.code for finding in findings if finding.severity == PROBLEM)


def accept_refit(old: Sequence[Finding], new: Sequence[Finding],
                 triggers: Iterable[str], *, converged: bool,
                 old_misfit: float | None = None,
                 new_misfit: float | None = None,
                 new_top_misfit: tuple[float, float] | None = None,
                 old_top_misfit: tuple[float, float] | None = None,
                 new_above_crossing: tuple[float, float] | None = None) -> Acceptance:
    """다시 맞춘 것을 받아들일까 — 넷 다 만족해야 한다 (ADR 0045).

    ``old``·``new`` 는 옛 맞춤과 새 맞춤을 **같은 점·같은 주파수 창**에서
    검수한 판정이다 (맞춤에 딸린 것만 — 점 자체의 KK 판정은 둘에 같다).
    ``old_misfit``·``new_misfit`` 는 두 맞춤의 평균 오차(비율)다.
    ``new_top_misfit``·``old_top_misfit`` 는 두 맞춤의 `FitAudit.top_misfit` 이다.
    ``new_above_crossing`` 는 새 맞춤의 `FitAudit.above_crossing` 이다.

    1. 수렴했다.
    2. 이 회로를 권한 판정(``triggers``)이 문제로 남지 않았다.
    3. 없던 문제가 생기지 않았다 — 코드별 **개수**로 센다.  아크가 둘인데 한
       아크의 이름만 고쳐져도 같은 코드가 그대로 남으니, 늘지만 않으면 된다.
    4. 모양을 못 그린다는 판정(`SHAPE_CODES`)이 새로 생기지 않았다.  옛 맞춤에도
       있었으면 새 것이 더 어긋나지 않아야 한다 (`MISFIT_TOLERANCE` 안).  두
       오차를 모르면 막는다.

    배선 판정(`WIRING_CODES`)이 권한 회로는 둘을 더 본다 (보완 8).  L 이 있는
    회로에는 그 판정이 뜰 수 없어 2 가 늘 참이므로, 판정이 본 **증상**을 본다.

    - 고주파 끝이 풀렸다: 가장 크게 어긋난 점이 더는 맞춘 구간의 고주파 끝에서
      문턱을 넘지 않는다 (``new_top_misfit`` 가 비었다).
    - 평균이 더 어긋나지 않았다.  옛 회로에 소자 하나를 더한 회로라 제대로 맞으면
      늘 수 없다 — 늘었으면 다른 골짜기다.

    구간 위 아크 판정(`ARC_CODES`)이 권한 회로도 증상을 본다 (보완 10).  판정은 L 이
    0 일 때만 뜨니 코드로는 풀린 것처럼 보일 수 있다.

    - 직렬 저항이 교점까지 내려왔다 (``new_above_crossing`` 이 비었다).
    - 그 직렬 저항이 0 으로 가지 않았다 (`INTERCEPT_LOST` 가 새로 뜨지 않았다) — 교점
      아래로 내려온 것이 절편을 잃어서면 까닭과 다르다.
    - 평균이 더 어긋나지 않았다 — 아크 하나를 더한 회로다.
    - 더한 아크가 σ 에 들고 σ 저항이 교점 이상인지는 σ 를 아는 쪽이 따로 본다
      (`electrolyte_short`).
    """
    if not converged:
        return Acceptance(False, "수렴하지 않았습니다")
    triggers = tuple(dict.fromkeys(triggers))
    before = _codes(old)
    after = _codes(new)
    left = [code for code in triggers if after[code]]
    if left:
        message = next(f.message for f in new if f.code == left[0]
                       and f.severity == PROBLEM)
        return Acceptance(False, f"그 문제가 그대로입니다 — {message}")
    wiring = any(code in WIRING_CODES for code in triggers)
    arc = any(code in ARC_CODES for code in triggers)
    if wiring and new_top_misfit is not None:
        return Acceptance(False, _top_left(old_top_misfit, new_top_misfit))
    if arc and new_above_crossing is not None:
        return Acceptance(False, _still_above(*new_above_crossing))
    if arc:
        lost = next((f for f in new if f.code in INTERCEPT_LOST
                     and not any(one.code == f.code for one in old)), None)
        if lost is not None:
            return Acceptance(False, f"더한 아크가 고주파 절편까지 가져갔습니다 — "
                                     f"{lost.message}")
    if wiring or arc:
        if old_misfit is None or new_misfit is None:
            return Acceptance(False, "오차 평균을 몰라 옛 맞춤과 견줄 수 없습니다")
        if not _no_worse(old_misfit, new_misfit):
            return Acceptance(False, f"오차 평균이 {_percent(old_misfit)} → "
                                     f"{_percent(new_misfit)} % 로 늘었습니다 — "
                                     f"{'아크' if arc else '소자'} 하나를 더했는데 더 "
                                     f"어긋나면 다른 골짜기입니다")
    worse = [code for code in after if after[code] > before[code]]
    if worse:
        message = next(f.message for f in new if f.code == worse[0]
                       and f.severity == PROBLEM)
        return Acceptance(False, f"없던 문제가 생깁니다 — {message}")
    shape = next((f for f in new if f.code in SHAPE_CODES), None)
    if shape is not None:
        inherited = any(f.code == shape.code for f in old)
        if not (inherited and _no_worse(old_misfit, new_misfit)):
            return Acceptance(False, shape.message)
    return Acceptance(True)


def _top_left(old: tuple[float, float] | None, new: tuple[float, float]) -> str:
    """L 을 넣고도 고주파 끝이 문턱을 넘을 때의 까닭 — 줄었으면 얼마에서 얼마로.

    실측 #105 (2026-09-25 맞춰 보기): 38 → 11 % 로 줄었는데 "고주파 끝이
    그대로입니다" 라고 적었다.  줄었는지 아닌지를 옛 맞춤의 증상과 견주어 적는다.
    """
    share, hz = new
    if old is not None and share < old[0] * _LESS:
        return (f"고주파 끝이 아직 가장 크게 어긋납니다 — L 을 넣어 {hz:.3g} Hz 가 "
                f"{old[0] * 100:.0f} → {share * 100:.0f} % 로 줄었지만 문턱을 넘습니다. "
                f"L 하나로는 그 끝을 다 못 그립니다")
    return (f"고주파 끝이 그대로입니다 — L 을 넣어도 {hz:.3g} Hz 가 {share * 100:.0f} % "
            f"어긋납니다. L 로는 그 끝이 안 그려집니다")


#: 고주파 끝의 어긋남이 옛것의 이 비율 아래로 내려가야 "줄었다" 고 적는다 — 반올림
#: 한 자리 안의 차이를 줄었다고 하지 않는다.
_LESS = 0.95


def _still_above(series_ohm: float, crossing_ohm: float) -> str:
    """아크를 더하고도 직렬 저항이 교점 위일 때의 까닭."""
    more = (series_ohm / crossing_ohm - 1.0) * 100.0
    return (f"직렬 저항 {series_ohm:.4g} Ω 이 아직 실수축 교점 {crossing_ohm:.4g} Ω 보다 "
            f"{more:.0f} % 큽니다 — 더한 아크가 구간 위의 아크를 그리지 않았습니다")


def electrolyte_short(crossing_ohm: float | None, conductivity: Mapping | None,
                      added: str) -> str:
    """아크를 더한 맞춤이 그 아크를 전해질 저항으로 읽지 않으면 그 까닭 — 아니면 빈
    문자열 (보완 10).

    판정의 까닭은 "구간 위에 걸친 아크가 전해질이다" 다.  그래서 새 맞춤에서 둘을 본다.

    1. **더한 아크(``added``)가 σ 에 든다** — `ionic_conductivity` 의 ``total_parts``.
       커패시턴스가 전극 쪽이라 하면 σ 가 뺀다 (ADR 0041).  그 아크는 구간 위의 아크가
       아니라 다른 것(꼬리의 굽이)을 그린 것이다.
    2. **σ 저항이 교점 이상이다.**  교점은 그 아크 도중이다.  벌크 크기로 읽혀 R0 를
       배선으로 뺀 것도 여기서 걸린다.

    처음에는 2 만 봤다.  실측 첫 맞춰 보기(2026-09-25 11:15 UTC)의 #114 가 σ 135.9 →
    120.1 Ω 으로 받아들여졌다.  새 R0 가 교점(114.9 Ω)보다 5 % 안으로 크면, 아크가 σ 에서
    빠져도 σ = R0 가 교점 위라 통과한다 — 1 이 그 틈을 막는다.

    σ 를 못 내도 (미결정 저항 등) 교점을 몰라도 받지 않는다.  확인할 수가 없다.
    """
    conductivity = conductivity or {}
    total = (conductivity.get("total_ohm")
             if conductivity.get("total_s_cm") is not None else None)
    if total is None:
        why = ", ".join(conductivity.get("missing") or ())
        return (f"σ 를 못 냅니다{f' ({why})' if why else ''} — 더한 아크가 전해질 저항에 "
                f"드는지 확인할 수 없습니다")
    if added not in (conductivity.get("total_parts") or ()):
        return (f"더한 아크 {added} 이 σ 에 안 듭니다 — 커패시턴스가 전극 쪽이라 구간 위의 "
                f"아크가 아닙니다")
    if crossing_ohm is None:
        return "실수축 교점을 몰라 σ 저항과 견줄 수 없습니다"
    if total < crossing_ohm:
        return (f"σ 저항 {total:.4g} Ω 이 실수축 교점 {crossing_ohm:.4g} Ω 보다 "
                f"작습니다 — 새 맞춤이 구간 위의 아크를 전해질 저항으로 읽지 않았습니다. "
                f"판정의 까닭과 어긋나니 사람이 봅니다")
    return ""


def _no_worse(old_misfit: float | None, new_misfit: float | None) -> bool:
    """새 맞춤이 옛 것보다 `MISFIT_TOLERANCE` 넘게 더 어긋나지 않았다."""
    return (old_misfit is not None and new_misfit is not None
            and new_misfit <= old_misfit + MISFIT_TOLERANCE)


def moved_number(old_ohm: float | None, new_ohm: float | None,
                 old_misfit: float | None, new_misfit: float | None) -> str:
    """모양을 덜 그리는 맞춤이 σ 의 저항을 옮기면 그 까닭 — 아니면 빈 문자열.

    검수가 받아들이는 것은 **이름과 모양**이다.  σ 에 쓰는 저항(막는 대칭셀의
    R0, 또는 R0 + 입계)은 따로 봐야 한다: 아크가 정말 보이는데 아크 없는 회로로
    맞추면 그 아크가 R0 로 들어가도 평균 오차는 3 % 아래일 수 있다 (합성 펠릿:
    +17 %, 오차 1 %).  이름은 맞아지고 수는 틀려진다 — 랩이 쓰는 것은 수다.

    그래서 새 맞춤이 **더 어긋나면서** (`MISFIT_TOLERANCE` 넘게) 그 저항을
    `RESISTANCE_SHIFT_LIMIT` 넘게 옮기면 받지 않는다.  같게 또는 더 잘 그리면 옮겨도
    받는다 — 옛 맞춤이 틀렸을 수 있다 (실측: 배선 L 없이 맞춘 펠릿은 새 맞춤이
    오차를 3.7 → 0.92 % 로 줄였다).
    값이 하나라도 없으면 (σ 를 못 내는 셀, 미결정) 판단하지 않는다.
    """
    if None in (old_ohm, new_ohm, old_misfit, new_misfit) or not old_ohm or old_ohm <= 0:
        return ""
    shift = (new_ohm - old_ohm) / old_ohm
    if abs(shift) <= RESISTANCE_SHIFT_LIMIT or _no_worse(old_misfit, new_misfit):
        return ""
    return (f"σ 에 쓰는 저항이 {old_ohm:.4g} → {new_ohm:.4g} Ω ({shift * 100:+.0f} %) 로 "
            f"옮겨 가는데 맞춤은 더 어긋납니다 (오차 평균 {_percent(old_misfit)} → "
            f"{_percent(new_misfit)} %) — 모양을 덜 그리는 회로가 수를 바꾸게 두지 않습니다")


def _percent(fraction: float) -> str:
    """``0.025`` → ``2.5``.  합성 셀은 2.4e-08 로 맞는다 — 그 자릿수는 읽을 거리가 아니다."""
    return "< 0.01" if fraction * 100 < 0.01 else f"{fraction * 100:.2g}"


def remaining_problems(findings: Iterable[Finding]) -> int:
    """받아들여진 새 맞춤에 남은 문제의 수 — 적을수록 낫다.

    후보마다 권한 판정이 다르다: 꼬리 흉내를 푸는 아크 하나짜리 회로와, 전극
    크기 아크를 푸는 아크 없는 회로.  둘 다 받아들여지면 문제가 덜 남는 쪽이
    낫다.  같으면 검수가 권한 순서를 따른다 (부르는 쪽이 앞의 것을 둔다).
    """
    return sum(_codes(findings).values())
