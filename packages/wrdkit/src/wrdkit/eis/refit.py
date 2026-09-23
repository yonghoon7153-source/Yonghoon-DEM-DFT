"""검수가 권한 회로로 다시 맞추기 — 무엇을, 어디서 시작해, 받아들일지 (ADR 0045).

맞추기와 저장은 API 가 한다 (`POST /api/eis/audit/refit`, `bml refit`).  여기는
그 사이의 판단만 둔다.

- `refit_candidates` — 문제 판정이 실은 회로를 어떤 순서로 맞춰 볼지.
- `seed_values` — 쓰는 맞춤의 값을 새 회로의 어느 파라미터로 옮길지.
- `accept_refit` — 새 맞춤을 다시 검수한 결과를 받아들일지.
- `moved_number` — 받아들여도, 모양을 덜 그리면서 σ 의 저항을 옮기면 안 받는다.
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

from .audit import PROBLEM, Finding
from .circuit import BLOCKING_KINDS, Circuit, CircuitError, parse_circuit

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


@dataclass(frozen=True)
class Candidate:
    """다시 맞춰 볼 회로 하나와, 그것을 권한 문제 판정들."""

    circuit: str
    #: 이 회로를 권한 **문제** 판정의 코드.  다시 맞춘 뒤 이것들이 없어야 한다.
    triggers: tuple[str, ...]


def refit_candidates(findings: Iterable[Finding]) -> list[Candidate]:
    """문제 판정이 실은 회로들 — 판정이 권한 순서대로, 한 번씩.

    **문제**만 본다.  확인(``open_end_on_blocking_cell`` 등)은 사람이 보고 정할
    일이라 한꺼번에 바꾸지 않는다 (ADR 0045).  같은 회로를 여러 판정이 권하면
    한 후보로 합치고 그 판정들을 모두 적는다 — 다시 맞춘 뒤 그 모두가 풀려야
    한다.
    """
    order: dict[str, list[str]] = {}
    for finding in findings:
        if finding.severity != PROBLEM:
            continue
        for circuit in finding.circuits:
            codes = order.setdefault(circuit, [])
            if finding.code not in codes:
                codes.append(finding.code)
    return [Candidate(circuit, tuple(codes)) for circuit, codes in order.items()]


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
                 new_misfit: float | None = None) -> Acceptance:
    """다시 맞춘 것을 받아들일까 — 넷 다 만족해야 한다 (ADR 0045).

    ``old``·``new`` 는 옛 맞춤과 새 맞춤을 **같은 점·같은 주파수 창**에서
    검수한 판정이다 (맞춤에 딸린 것만 — 점 자체의 KK 판정은 둘에 같다).
    ``old_misfit``·``new_misfit`` 는 두 맞춤의 평균 오차(비율)다.

    1. 수렴했다.
    2. 이 회로를 권한 판정(``triggers``)이 문제로 남지 않았다.
    3. 없던 문제가 생기지 않았다 — 코드별 **개수**로 센다.  아크가 둘인데 한
       아크의 이름만 고쳐져도 같은 코드가 그대로 남으니, 늘지만 않으면 된다.
    4. 모양을 못 그린다는 판정(`SHAPE_CODES`)이 새로 생기지 않았다.  옛 맞춤에도
       있었으면 새 것이 더 어긋나지 않아야 한다 (`MISFIT_TOLERANCE` 안).  두
       오차를 모르면 막는다.
    """
    if not converged:
        return Acceptance(False, "수렴하지 않았습니다")
    before = _codes(old)
    after = _codes(new)
    left = [code for code in dict.fromkeys(triggers) if after[code]]
    if left:
        message = next(f.message for f in new if f.code == left[0]
                       and f.severity == PROBLEM)
        return Acceptance(False, f"그 문제가 그대로입니다 — {message}")
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
