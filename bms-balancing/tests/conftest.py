"""테스트가 **전역 상태를 되돌려 놓았는지** 매번 확인한다 (W-07, 2026-09-14).

왜 이 파일이 생겼나 — 실측:

`tests/test_review_findings.py::test_r5_08` 이 `pytest.MonkeyPatch()` 를 만들고 **손잡이를 버렸다**.
`undo()` 를 부를 수 없으니 그 패치(`verify.minimize` → 항상 `success=False` 인 가짜, `verify.multistart` →
상수를 돌려주는 lambda, `verify.build` → 가짜 Objective)가 **세션이 끝날 때까지 남았다.**

pytest 는 파일을 알파벳 순으로 돈다. 그래서 `test_review_findings` 뒤에 오는 파일의 테스트가 그 가짜를
그대로 뒤집어쓴다. 증상이 고약한 이유는 **단독 실행은 통과하기 때문**이다 — 전체 실행에서만 빨갛고,
빨간 이유가 자기 코드와 무관하다. 이번에 실제로 세 건이 그렇게 났고(`tests/test_widths.py`), 그중 하나는
5-파라미터 목적함수에 **4-벡터** `[1.2, -0.25, 1.4, -0.15]` 가 들어와 broadcast 오류를 냈다. 그 값은
`_r3_profile_mocks` 의 `nonconverged` 가 돌려주는 바로 그 배열이다.

더 나쁜 것은 **조용한 통과** 쪽이다: 뒤따르는 테스트가 가짜 optimizer 로 "통과" 하면 그 테스트는 아무것도
안 재고 있었던 것이 된다. 이 저장소가 fixture 감사에서 네 번 넘게 본 모양이다 — fixture 가 진실을 가린다.

그래서 규칙을 기계가 지킨다: **테스트 하나가 끝나면 모듈 전역이 시작할 때와 같아야 한다.** 다르면 그
테스트를 실패시킨다 (다음 테스트가 아니라 **범인**이 빨개진다).

지키는 축은 "가짜로 바꿔치기하면 다른 테스트가 조용히 거짓 통과할 수 있는 것" 들이다. 이름만 늘리지 말고,
실제로 그런 사고가 난 축을 넣는다.
"""
from __future__ import annotations

import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

#: 감시하는 (모듈경로, 속성) — 바꿔치기하면 뒤따르는 테스트가 거짓으로 통과할 수 있는 것들.
_WATCHED = (
    ("bms_balancing.verify", "minimize"),        # ← 실제로 샜던 축 (W-07)
    ("bms_balancing.verify", "multistart"),      # ← 실제로 샜던 축 (W-07)
    ("bms_balancing.verify", "build"),           # ← 실제로 샜던 축 (W-07)
    ("bms_balancing.verify", "resolve_box"),     # 상자 규칙의 한 자리 (W-05)
    ("bms_balancing.verify", "near_optimal_extrema"),
    ("bms_balancing.verify", "mode_profile_extrema"),
    ("bms_balancing.verify", "active_bounds"),
    ("bms_balancing.verify", "degradation_modes"),
    ("bms_balancing.cycles", "multistart"),
    ("bms_balancing.cycles", "active_bounds"),
)


def _snapshot():
    """지금 값을 찍는다. 아직 import 되지 않은 모듈은 **건너뛴다** (import 를 강제하지 않는다)."""
    seen = {}
    for mod, attr in _WATCHED:
        m = sys.modules.get(mod)
        if m is not None and hasattr(m, attr):
            seen[(mod, attr)] = getattr(m, attr)
    return seen


@pytest.fixture(autouse=True)
def _no_leaked_global_patches():
    """테스트 전후로 감시 축을 대조한다 — `is` 로 본다 (값이 아니라 **같은 객체**인가).

    ⚠ 테스트가 끝난 **뒤**에 검사하므로, 범인 테스트 자신이 빨개진다. 이것이 요점이다 —
      전 판에서는 엉뚱한 파일의 테스트가 빨개져서 원인을 찾는 데 한참 걸렸다.

    ⚠ 테스트가 이미 실패한 경우에도 이 검사는 돈다. 그때는 실패가 둘이 되지만, 누출은 그대로
      알려야 한다 — 실패한 테스트가 정리를 안 하고 나간 것도 사실이다.
    """
    before = _snapshot()
    yield
    after = _snapshot()
    leaked = [f"{mod}.{attr}" for (mod, attr), v in before.items()
              if (mod, attr) in after and after[(mod, attr)] is not v]
    assert not leaked, (
        "이 테스트가 모듈 전역을 되돌려 놓지 않았다: " + ", ".join(leaked) +
        " — `pytest.MonkeyPatch()` 를 직접 만들었으면 `undo()` 를 부르거나, "
        "그냥 `monkeypatch` fixture 를 쓴다 (자동으로 되돌아간다). "
        "안 되돌리면 알파벳 순으로 뒤에 오는 테스트가 가짜를 뒤집어쓰고, 그쪽은 "
        "**단독 실행에서는 통과**하기 때문에 원인을 찾기가 아주 어렵다 (W-07 실측)."
    )
