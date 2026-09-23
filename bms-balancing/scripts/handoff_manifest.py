#!/usr/bin/env python3
"""handoff 묶음 manifest 의 **항목 목록**을 고르는 한 자리.

## 왜 따로 있나 (2026-09-15)

`preserve_handoff.sh` 가 `m.get("entries")` 하나만 봤다. 그런데 묶음마다 목록 키가 다르다 —
실측:

    desktop_postproc      entries
    electrolyte_guard     files
    physical600_b_review  files
    electrolyte_recovery  payload

셋이 5 단계에서 "manifest 에 entries 가 없다" 로 멈췄다. ZIP 크기·SHA·manifest 해시는 셋 다
전달값과 **정확히 일치**했으니, 다른 것은 자료가 아니라 목록 키였다. 멈춘 것 자체는 옳다 —
모르는 모양을 추측해서 보존하면 무엇을 대조한 것인지 알 수 없다.

그래서 넓히는 것은 **아는 키**뿐이고, 모르는 모양은 계속 멈춘다. 규칙을 bash 안의 heredoc 에
두면 시험할 수 없어서 여기로 뺐다 — 회귀는 `tests/test_r15_open_items.py`.

## 2026-09-24 — 경로 키의 별칭

B_A8R1 묶음(세 겹: HANDOFF · PACKAGE · EXTERNAL_PACKAGE manifest)은 항목 키가 `file` · `bytes` ·
`sha256` 이다. `path` 가 없어 세 겹 전부 "경로 없음" 으로 멈췄다. `file` 을 `path` 의 별칭으로
받되 돌려주는 항목은 **`path` 로 정규화**한다 — 소비 자리 셋이 전부 `e["path"]` 를 읽는다.
둘 다 있는데 다르면 거부한다. 회귀는 같은 파일의 `test_an_entry_may_name_its_path_with_the_key_file`.

## 계약

- 항목마다 `path`(또는 별칭 `file`) 와 `sha256` 이 **둘 다** 있어야 한다. 대조할 수 없는 것을 보존하면 보존의
  뜻이 사라진다.
- 후보 키가 **둘 이상** 쓸 만하면 고르지 않고 멈춘다. 무엇을 대조한 것인지는 사람이 정한다.
- 빈 목록·목록 아님·항목이 dict 아님은 전부 거부다 (부재는 안전값이 아니다).
"""
from __future__ import annotations

#: 실측으로 본 목록 키. 새 묶음이 또 다른 이름을 쓰면 **여기 한 줄**을 늘린다.
ENTRY_KEYS = ("entries", "files", "payload")


#: `path` 의 별칭. 새 묶음이 또 다른 이름을 쓰면 여기 한 줄을 늘린다 (추측하지 않는다).
PATH_KEYS = ("path", "file")


def _path_of(e) -> str | None:
    """항목의 경로. `path`·`file` 이 둘 다 있고 서로 다르면 `ValueError` — 무엇을 대조한 것인지 알 수 없다."""
    if not isinstance(e, dict):
        return None
    vals = {k: e[k] for k in PATH_KEYS if e.get(k)}
    if len(set(vals.values())) > 1:
        raise ValueError(f"항목의 경로 키가 서로 다르다 ({vals}) — 어느 쪽을 대조한 것인지 사람이 정해야 한다")
    return next(iter(vals.values()), None)


def _usable(v) -> bool:
    return (isinstance(v, list) and bool(v)
            and all(isinstance(e, dict) and _path_of(e) and e.get("sha256") for e in v))


def _normalized(v: list) -> list:
    """`path` 를 채운 사본 목록. 원본 dict 는 건드리지 않는다."""
    return [dict(e, path=_path_of(e)) for e in v]


def entry_list(manifest) -> list:
    """manifest 에서 항목 목록을 돌려준다. 못 고르면 `ValueError` — 추측하지 않는다."""
    if not isinstance(manifest, dict):
        raise ValueError(f"manifest 가 객체가 아니다 ({type(manifest).__name__})")
    hits = [k for k in ENTRY_KEYS if _usable(manifest.get(k))]
    if len(hits) > 1:
        raise ValueError(
            f"쓸 만한 항목 목록이 **둘 이상**이다 ({', '.join(hits)}) — 무엇을 대조한 것인지 "
            "사람이 정해야 한다. 추측해서 고르지 않는다")
    if hits:
        return _normalized(manifest[hits[0]])
    seen = sorted(manifest)
    for k in ENTRY_KEYS:
        v = manifest.get(k)
        if isinstance(v, list) and v:
            missing = [i for i, e in enumerate(v)
                       if not (isinstance(e, dict) and _path_of(e) and e.get("sha256"))]
            raise ValueError(
                f"`{k}` 는 목록인데 항목 {len(missing)} 개에 `path`(또는 `file`)·`sha256` 이 둘 다 있지 "
                f"않다 (첫 자리 {missing[0]}) — 대조할 수 없는 것은 보존하지 않는다")
    raise ValueError(
        f"manifest 에서 항목 목록을 못 찾았다. 아는 키: {', '.join(ENTRY_KEYS)} · "
        f"이 manifest 의 최상위 키: {', '.join(seen) if seen else '(없음)'} — "
        "새 규약이면 `scripts/handoff_manifest.py` 의 ENTRY_KEYS 에 더하고 회귀를 같이 넣을 것")
