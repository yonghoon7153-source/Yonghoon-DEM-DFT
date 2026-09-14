"""시험용 **완전한** 실행 영수증 (62차 P2-1).

61차까지의 시험은 `{"packages": …, "startup": {"startup_history": …}}` 같은
최소 dict 로 reader 를 통과시켰다 — reader 가 `status` 만 봤기 때문이다.
62차 P2-1 이 reader 를 재귀 exact schema 로 바꾸면서 그 fixture 가 먼저
깨져야 정상이고, 깨졌다 (CLAUDE.md 규율 2). 여기 것이 그 schema 의 정본
예시다 — schema 를 바꾸면 이것도 같이 바뀐다.
"""
from __future__ import annotations

import copy

_H = "0123456789abcdef"


def _parent_view() -> dict:
    """★ 62차 자체 리뷰 F1 — 부모가 child 의 customization 을 자기 시야와
    대조하므로, 완전한 영수증은 그 값을 **실제 부모 시야**에서 가져와야 한다."""
    import sys
    from pathlib import Path

    gap = Path(__file__).resolve().parent.parent / "docs" / "22p_gap"
    if str(gap) not in sys.path:
        sys.path.insert(0, str(gap))
    import mutation_replay as mr

    return mr._parent_customization_view()


def full_receipt(**over) -> dict:
    """schema 에 정확히 맞는 영수증. `over` 는 최상위 키를 덮는다."""
    rec = {
        "interpreter": "3.11.2",
        "packages": {"status": "measured",
                     "dists": {"numpy": "2.4.6"},
                     "positions": {"numpy": 3},
                     "shadowed": []},
        "env": {"PYTHONHASHSEED": "0"},
        "inputs": {"status": "measured", "files": {"configs/base.yaml": _H}},
        "startup": {
            "status": "measured",
            "executable_sha256": _H,
            "customization": _parent_view(),
            "startup_modules": {"os": _H},
            "startup_history": {"status": "measured",
                                "modules": {"os": _H}, "unfiled": 3},
            "importable_roots": {"0/x.py": _H},
            "pth": [["/usr/lib/python3/dist-packages/x.pth", _H]],
            "version": "3.11.2",
            "env": {"PYTHONHASHSEED": "0"},
        },
    }
    rec = copy.deepcopy(rec)
    rec.update(over)
    return rec
