#!/usr/bin/env python3
"""electronic_class.py — 상이 **금속인가 절연체인가**를 한 곳에서 읽는다.

왜 모듈로 빼나 (2026-08-11)
  우리 SEI 파이프라인은 **넓은 갭 절연체 전용**으로 만들어졌다. Li₃Nd 같은 금속에
  그대로 돌리면 세 곳이 조용히 틀린다:
    ① `build_dft_inputs.py` ③단계 fixed-occ 갭 — 금속엔 VBM/CBM 이 없는데 **숫자는 나온다**
    ② `build_neb_inputs.py` tot_charge=−1 + jellium — 금속은 공공을 전도전자가 가려준다
    ③ `collect_neb.py` 의 "tot_charge=0 은 옛 규약" 차단 — 금속엔 **정반대로** 틀린 게이트
  네 도구가 각자 판단하면 서로 어긋난다. 판정은 db/properties/sei_electronic_class.json
  하나에만 두고 전부 여기로 읽는다.

⛔ `undetermined` 는 **금속 선언이 아니다.** Nd 4f 를 원자가에 둔 계산이 갭 0 을 내는 건
  방법의 실패지 금속성이 아니다 — LiNdO₂ 를 metal 로 분류하면 NEB 이 틀린 전하로 돈다.

  python3 tools/sei/electronic_class.py            # 표를 본다
  python3 tools/sei/electronic_class.py --tag li3nd
"""
import json
import os
import sys

REGISTRY = "db/properties/sei_electronic_class.json"


def _repo_path(rel):
    """repo 루트 기준 경로 — 도구를 어디서 실행하든 레지스트리를 찾게 한다."""
    if os.path.isfile(rel):
        return rel
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(os.path.dirname(os.path.dirname(here)), rel)


def load(path=REGISTRY):
    p = _repo_path(path)
    if not os.path.isfile(p):
        return {}
    try:
        return json.load(open(p, encoding="utf-8")).get("results", {})
    except (OSError, ValueError):
        return {}


def normalize(tag):
    """`li2o_mp-1960` · `sei_li2o` 같은 변형을 레지스트리 키로 맞춘다."""
    t = str(tag).lower()
    if t.startswith("sei_"):
        t = t[4:]
    if "_mp-" in t:
        t = t.split("_mp-")[0]
    return t


def get(tag, reg=None):
    """상의 분류 레코드. 등록되지 않았으면 `unregistered` 를 돌려준다 —
    ⚠ 미등록을 조용히 절연체로 간주하지 않는다. 그게 Li₃Nd 함정의 입구다."""
    reg = load() if reg is None else reg
    r = reg.get(normalize(tag))
    if r is None:
        return {"class": "unregistered", "evidence": None,
                "note": f"'{tag}' 가 {REGISTRY} 에 없다 — 금속/절연체를 추측하지 않는다. "
                        "레지스트리에 먼저 등록할 것."}
    return r


def is_metal(tag, reg=None):
    return get(tag, reg).get("class") == "metal"


def is_insulator(tag, reg=None):
    return get(tag, reg).get("class") == "insulator"


def blocked_reason(tag, reg=None):
    """계산을 걸면 안 되는 이유. 걸어도 되면 None.

    metal 인데 evidence='declared' 면 **아직 확인 전**이다 — DOS 로 E_F 상태를
    확인하기 전에 NEB 을 걸면 '금속이라 가정했더니 금속 답이 나왔다' 가 된다.
    """
    r = get(tag, reg)
    c = r.get("class")
    if c == "unregistered":
        return r["note"]
    if c == "undetermined":
        return (f"electronic_class=undetermined — {r.get('blocker', '판정 불가')}"
                + (f"  해소: {r['unblock']}" if r.get("unblock") else ""))
    if c == "metal" and r.get("evidence") == "declared":
        return ("electronic_class=metal 이지만 evidence=declared 다 — "
                "DOS/PDOS 로 E_F 에 상태가 있는지 **먼저 확인**할 것. "
                + str(r.get("must_confirm", "")))
    return None


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", help="하나만 본다")
    a = ap.parse_args()
    reg = load()
    if not reg:
        print(f"⛔ {REGISTRY} 를 못 읽었다")
        return 1
    tags = [normalize(a.tag)] if a.tag else sorted(reg)
    print(f"{'상':10s} {'분류':14s} {'근거':11s} {'갭[eV]':>8s}  비고")
    for t in tags:
        r = get(t, reg)
        g = r.get("gap_eV")
        note = r.get("blocker") or r.get("must_confirm") or r.get("note") or ""
        print(f"{t:10s} {r.get('class', '?'):14s} {str(r.get('evidence')):11s} "
              f"{(f'{g:.4f}' if isinstance(g, (int, float)) else '—'):>8s}  {note[:70]}")
        b = blocked_reason(t, reg)
        if b:
            print(f"{'':10s} ⛔ {b[:110]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
