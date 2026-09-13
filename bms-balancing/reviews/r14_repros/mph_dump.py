#!/usr/bin/env python3
"""COMSOL .mph(=ZIP) 의 dmodel.xml 을 **소유권과 활성 상태를 보존해서** 덤프한다.

`docs/MICROSHORT_MPH_REVIEW.md` 7절의 전 판 정규식 추출기를 대체한다.
전 판은 부모 PhysicsFeature 를 **첫 번째** `</PhysicsFeature>` 까지 잘랐다. 그래서

  · 자식의 param 을 부모의 것으로 출력하고
  · 자식의 entityFlags(DISABLED)를 부모의 것으로 오인하고
  · 자식 뒤에 오는 부모 자신의 param 을 통째로 버렸다.

Codex 1차 리뷰 §2.6 이 지적했고 `test_extractor_ownership()` 이 그 반례를 고정한다.
이 판은 ElementTree 로 트리를 걷고, 각 노드의 **직계** param 만 그 노드 것으로 세며,
활성 상태는 (a) 자기 flags 와 (b) 조상 사슬(Physics 인터페이스 포함)을 나눠서 보고한다.

    python3 mph_dump.py <dmodel.xml> [--params k1,k2,...] [--refs name1,name2,...]
    python3 mph_dump.py --self-test
"""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET

DEFAULT_PARAMS = (
    "csinit", "cEeqref", "cEeqref_mat", "epss", "epssadd", "epsl", "sigma", "rp", "Ds",
    "Eeq", "Eeq_mat", "MaterialOption", "EeqrefType", "ElectrodeKinetics",
    "ParticleConcentrationType", "ElectricCorrModel", "IonicCorrModel", "ParticleMaterial",
)


def _own_flags(el) -> str:
    return "".join(c.text or "" for c in el if c.tag == "entityFlags")


def _own_params(el) -> dict:
    """직계 자식의 <param> 만. 손자(자식 노드의 param)는 세지 않는다."""
    out = {}
    for c in el:
        if c.tag == "param" and c.get("param"):
            out[c.get("param")] = c.get("value")
        elif c.tag not in ("PhysicsFeature", "Physics"):
            # COMSOL 은 param 을 컨테이너 한 겹 안에 두기도 한다 (예: <param T="33">).
            for g in c:
                if g.tag == "param" and g.get("param"):
                    out.setdefault(g.get("param"), g.get("value"))
    return out


def walk_features(root):
    """(path, tag, op, name, own_disabled, inherited_disabled, params) 를 순서대로 낸다."""
    rows = []

    def rec(el, path, inherited):
        for c in list(el):
            if c.tag in ("PhysicsFeature", "Physics"):
                own = "DISABLED" in _own_flags(c)
                tag = c.get("tag") or c.tag
                rows.append((
                    path + "/" + tag, tag, c.get("op") or c.tag, c.get("name") or "",
                    own, inherited, _own_params(c),
                ))
                rec(c, path + "/" + tag, inherited or own)
            else:
                rec(c, path, inherited)

    rec(root, "", False)
    return rows


def live_expressions(root):
    """live 표현식만. <actions> 는 **이력**이라 제외한다 (과거 설정을 현재로 오독하지 않기)."""
    out = []

    def rec(el, path):
        if el.tag == "actions":
            return
        for k, v in el.attrib.items():
            if v and k not in ("name", "tag", "op", "descr"):
                out.append((path, el.tag, k, v))
        for c in el:
            rec(c, path + "/" + (c.get("tag") or c.tag))

    rec(root, "")
    return out


def count_refs(exprs, name):
    """식별자로서의 참조만 센다 (문자열 등장 횟수 != 소비자 수)."""
    pat = re.compile(r"(?<![A-Za-z0-9_.])" + re.escape(name) + r"(?![A-Za-z0-9_])")
    hits = []
    for path, tag, key, val in exprs:
        if tag == "expressions" and key == "name":
            continue                      # 자기 정의의 이름 칸
        if tag == "expressions" and key == "expr" and val.strip() == name:
            continue
        if pat.search(val):
            hits.append((path, tag, key, val))
    return hits


def test_extractor_ownership():
    """Codex 1차 §2.6 의 반례 — 전 판은 실패하고 이 판은 통과해야 한다."""
    xml = (
        '<root><PhysicsFeature op="Parent" tag="par1" name="Parent">'
        '<param T="33" param="epss" value="PARENT_EPSS"></param>'
        '<PhysicsFeature op="Child" tag="ch1" name="Child">'
        '<entityFlags T="51">DISABLED</entityFlags>'
        '<param T="33" param="csinit" value="CHILD_CSINIT"></param>'
        '</PhysicsFeature>'
        '<param T="33" param="rp" value="PARENT_RP_AFTER_CHILD"></param>'
        '</PhysicsFeature></root>'
    )
    rows = walk_features(ET.fromstring(xml))
    by_tag = {r[1]: r for r in rows}
    par, ch = by_tag["par1"], by_tag["ch1"]
    assert par[4] is False, "부모를 DISABLED 로 오인했다 (자식 flags 전파)"
    assert ch[4] is True, "자식의 DISABLED 를 놓쳤다"
    assert set(par[6]) == {"epss", "rp"}, f"부모 param 오류: {sorted(par[6])}"
    assert par[6]["rp"] == "PARENT_RP_AFTER_CHILD", "자식 뒤 부모 param 을 버렸다"
    assert set(ch[6]) == {"csinit"}, f"자식 param 오류: {sorted(ch[6])}"
    assert ch[5] is False and par[5] is False
    print("test_extractor_ownership: OK")


def main(argv):
    if "--self-test" in argv:
        test_extractor_ownership()
        return 0
    if len(argv) < 2:
        print(__doc__)
        return 2
    root = ET.parse(argv[1]).getroot()

    keys = DEFAULT_PARAMS
    if "--params" in argv:
        keys = tuple(argv[argv.index("--params") + 1].split(","))

    print("=== PhysicsFeature 트리 (own = 자기 flags, inh = 조상 사슬) ===")
    for path, tag, op, name, own, inh, params in walk_features(root):
        state = "DISABLED(own)" if own else ("disabled(inherited)" if inh else "active")
        print(f"{path:52s} {op:32s} {state:22s} {name}")
        for k in keys:
            if k in params:
                print(f"      {k:26s} = {params[k]}")

    if "--refs" in argv:
        exprs = live_expressions(root)
        print("\n=== live 참조 그래프 (<actions> 이력 제외) ===")
        for nm in argv[argv.index("--refs") + 1].split(","):
            hits = count_refs(exprs, nm)
            print(f"\n### {nm}: live 참조 {len(hits)} 건")
            for path, tag, key, val in hits[:10]:
                print(f"   {path[-60:]:60s} <{tag} {key}> {val[:80]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
