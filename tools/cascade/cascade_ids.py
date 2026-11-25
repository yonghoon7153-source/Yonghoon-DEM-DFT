#!/usr/bin/env python3
"""cascade_ids.py — 캐스케이드 CSV 를 읽는 도구들이 **같은 방식으로 묶게** 하는 정본.

왜 이게 따로 있나
  `cascade_v23_all.csv` 의 `dopant` 열에는 generator 변형 접미사가 붙는다:
  `WO3` 와 `WO3+Clrich` 는 **같은 화학종의 두 레시피**다. 그런데 `dopant` 를 그대로
  그룹 키로 쓰면 둘이 다른 종이 되고, 라벨 사이에서 변형이 바뀐 종은 **어느 이름으로도
  3점이 안 돼 통째로 사라진다.**

  2026-08-16 하루에 이 함정을 **세 번** 밟았다:
    ① 조성족 감사 — 챔피언 슬롯을 세다가
    ② label scatter 감사 — 81종이 전수인 줄 알았다 (실제 90종)
    ③ 슬롯당 후보 수 — max 40 이라고 했는데 실제 50 (MgO plain 10 + Clrich 40)
  세 번 다 "왜 숫자가 작지?" 를 나중에 알아챘다. 그래서 함수를 여기 하나로 모으고,
  `convention_check.py` 가 raw `dopant` 그룹핑을 **위반으로 잡는다.**

쓰기
    from cascade_ids import base_species, slot_key
    base_species("WO3+Clrich")           # -> "WO3"
    slot_key(row)                        # -> ("WO3", "x005")

이 모듈이 **못 하는 것**
  · 어느 그룹핑이 옳은지 상황별로 판단하지 않는다. 변형끼리 **구별해야 하는** 분석
    (예: plain vs chain 조성족 대조)에서는 `dopant` 를 그대로 쓰는 게 맞다.
    그때는 `variant_key()` 를 쓰고, 왜 raw 가 필요한지 주석으로 남길 것.
  · 접미사 규약이 `+` 하나뿐이라고 가정한다. 새 generator 가 다른 구분자를 쓰면
    여기부터 고쳐야 한다 (`VARIANT_SEP`).
  · 조성이 같은지는 보지 않는다 — 이름만 다룬다.
"""
import sys

#: generator 변형 접미사 구분자. `WO3+Clrich` 의 `+`.
VARIANT_SEP = "+"


def base_species(dopant_label):
    """`WO3+Clrich` → `WO3`. 접미사를 떼고 **화학종**으로 만든다.

    None/빈 문자열도 죽지 않는다 (빈 문자열을 돌려준다).
    """
    return (dopant_label or "").split(VARIANT_SEP, 1)[0]


def variant_suffix(dopant_label):
    """`WO3+Clrich` → `Clrich`. 접미사가 없으면 빈 문자열."""
    s = dopant_label or ""
    return s.split(VARIANT_SEP, 1)[1] if VARIANT_SEP in s else ""


def variant_key(dopant_label):
    """raw 라벨 그대로. **변형끼리 구별해야 하는 분석에서만** 쓴다.

    쓸 때는 왜 base 가 아닌지 주석으로 남길 것 — 안 그러면 다음 사람이 버그로 읽는다.
    """
    return dopant_label or ""


def slot_key(row, label_col="concentration_label", dopant_col="dopant"):
    """캐스케이드의 실행 슬롯 = (화학종, 농도라벨). **base 기준**이다.

    ⚠ 농도라벨은 농도가 아니다 — 셀이 4 f.u. 라 x002/x005/x010 이 전부
      generator loading 0.25 로 양자화됐다. 슬롯 식별자로만 쓸 것.
    """
    return (base_species(row.get(dopant_col, "")), row.get(label_col, ""))


def group_by_base(rows, key_col="concentration_label", rank_col="rank_combined",
                  rank=None, min_labels=None):
    """{화학종: {농도라벨: 행}}. rank 를 주면 그 값만, min_labels 를 주면 그만큼 있는 것만."""
    import collections
    by = collections.defaultdict(dict)
    for r in rows:
        if rank is not None and r.get(rank_col) != rank:
            continue
        by[base_species(r.get("dopant", ""))][r.get(key_col, "")] = r
    if min_labels:
        return {k: v for k, v in by.items() if len(v) >= min_labels}
    return dict(by)


def selftest():
    ok = fail = 0

    def chk(name, cond):
        nonlocal ok, fail
        if cond:
            ok += 1
        else:
            fail += 1
            try: print(f"  ✗ {name}")
            except Exception: print(f"  FAIL {name}")

    chk("접미사 제거", base_species("WO3+Clrich") == "WO3")
    chk("접미사 없으면 그대로", base_species("WO3") == "WO3")
    chk("None 안전", base_species(None) == "")
    chk("빈 문자열 안전", base_species("") == "")
    chk("접미사 여럿이어도 첫 것만", base_species("A+B+C") == "A")
    chk("접미사 추출", variant_suffix("WO3+Clrich") == "Clrich")
    chk("접미사 없으면 빈 문자열", variant_suffix("WO3") == "")
    chk("variant_key 는 그대로", variant_key("WO3+Clrich") == "WO3+Clrich")
    # 음성 ①: base 와 variant 를 헷갈리면 안 된다
    chk("음성: base ≠ variant", base_species("WO3+Clrich") != variant_key("WO3+Clrich"))
    chk("슬롯 키", slot_key({"dopant": "WO3+Clrich", "concentration_label": "x005"})
        == ("WO3", "x005"))

    rows = [{"dopant": "WO3+Clrich", "concentration_label": "x002", "rank_combined": "1"},
            {"dopant": "WO3+Clrich", "concentration_label": "x005", "rank_combined": "1"},
            {"dopant": "WO3", "concentration_label": "x010", "rank_combined": "1"},
            {"dopant": "WO3", "concentration_label": "x002", "rank_combined": "2"}]
    g = group_by_base(rows, rank="1", min_labels=3)
    chk("base 로 묶으면 3점이 된다", set(g) == {"WO3"} and len(g["WO3"]) == 3)
    # 음성 ②: raw 로 묶으면 사라진다 — 이 **함정을 재현**하는 것이 목적이다
    #   (convention_check 의 raw-dopant 가드는 이 주석을 보고 통과시킨다)
    import collections
    raw = collections.defaultdict(dict)
    for r in rows:
        if r["rank_combined"] == "1":
            raw[r["dopant"]][r["concentration_label"]] = r
    chk("음성: raw 로 묶으면 3점짜리가 없다",
        not [k for k, v in raw.items() if len(v) >= 3])
    # 음성 ③: rank 필터가 실제로 걸리는가
    chk("음성: rank 2 행은 안 들어온다",
        "x002" not in g["WO3"] or g["WO3"]["x002"]["rank_combined"] == "1")
    chk("음성: min_labels 미만은 제외",
        group_by_base(rows[:1], rank="1", min_labels=3) == {})

    try: print(f"\nselftest: {ok} passed, {fail} failed")
    except Exception: print(f"\nselftest: {ok} passed, {fail} failed")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(selftest() if "--selftest" in sys.argv else 0)
