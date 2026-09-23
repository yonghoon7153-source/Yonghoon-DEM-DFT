"""검수가 권한 회로로 다시 맞추기 — 무엇을, 어디서 시작해, 받아들일지 (ADR 0045).

맞추기와 저장은 API 가 한다 (`POST /api/eis/audit/refit`, `bml refit`).  여기는
그 사이의 판단만 둔다.

- `refit_candidates` — 문제 판정이 실은 회로를 어떤 순서로 맞춰 볼지.
- `seed_values` — 쓰는 맞춤의 값을 새 회로의 어느 파라미터로 옮길지.
- `accept_refit` — 새 맞춤을 다시 검수한 결과를 받아들일지.
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

#: 이것이 뜨면 받아들이지 않는다 — "회로가 이 스펙트럼의 모양을 못 그립니다".
#: 이름을 고치려고 모양을 못 그리는 회로로 바꾸지 않는다.  심각도(확인)와
#: 상관없이 막는다: 문제가 하나 줄어도 곡선이 점을 안 지나가면 값이 없다.
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
                 triggers: Iterable[str], *, converged: bool) -> Acceptance:
    """다시 맞춘 것을 받아들일까 — 넷 다 만족해야 한다 (ADR 0045).

    ``old``·``new`` 는 옛 맞춤과 새 맞춤을 **같은 점·같은 주파수 창**에서
    검수한 판정이다 (맞춤에 딸린 것만 — 점 자체의 KK 판정은 둘에 같다).

    1. 수렴했다.
    2. 이 회로를 권한 판정(``triggers``)이 문제로 남지 않았다.
    3. 없던 문제가 생기지 않았다 — 코드별 **개수**로 센다.  아크가 둘인데 한
       아크의 이름만 고쳐져도 같은 코드가 그대로 남으니, 늘지만 않으면 된다.
    4. 모양을 그린다 (`SHAPE_CODES` 가 없다).
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
        return Acceptance(False, shape.message)
    return Acceptance(True)


def remaining_problems(findings: Iterable[Finding]) -> int:
    """받아들여진 새 맞춤에 남은 문제의 수 — 적을수록 낫다.

    후보마다 권한 판정이 다르다: 꼬리 흉내를 푸는 아크 하나짜리 회로와, 전극
    크기 아크를 푸는 아크 없는 회로.  둘 다 받아들여지면 문제가 덜 남는 쪽이
    낫다.  같으면 검수가 권한 순서를 따른다 (부르는 쪽이 앞의 것을 둔다).
    """
    return sum(_codes(findings).values())
