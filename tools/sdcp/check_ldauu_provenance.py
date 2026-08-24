#!/usr/bin/env python3
"""check_ldauu_provenance.py — 우리 U(Ni 3d) = 6.2 eV 가 어디서 온 값인지 확인한다.

왜 필요한가
  `kb/methodology/terminology_register.md` §42 가 우리 U 값을 **"⚠ 원전 미보유"** 로
  기록하고 있다. SDCP 원고 v5 의 SI Table S1 은 정량값에 출처를 요구하는데
  (2026-08-23 지도교수 지시), 이 한 값만 출처가 비어 있다.
  유력 가설: **Materials Project / pymatgen 의 산화물 기본 U 와 같은 값**이다.
  이 도구는 로컬 pymatgen 설정에서 LDAUU 를 읽어 그 가설을 확인/반증한다.

무엇을 하나
  ① pymatgen 설정에서 LDAUU 를 읽는다 (API 속성 → YAML 파일 순으로 시도)
  ② 음이온 그룹(O/F) 중첩을 풀어 해당 원소의 U 를 찾는다
  ③ 우리 값과 대조해 MATCH / MISMATCH / NOT_FOUND 판정

이 도구가 **못 하는 것**
  · **"6.2 이 이 계에 옳다" 를 말하지 않는다.** MP 기본값과 같은 값인지만 본다.
    U 민감도(4 vs 6.2)는 별개 계산이고 우리는 안 돌렸다.
  · MATCH 가 나와도 **인용 논문을 확정해 주지 않는다.** MP 의 U 세트 계보는
    Wang–Maxisch–Ceder PRB 73, 195107 (2006) / Jain PRB 84, 045115 (2011) 이지만,
    어느 쪽을 다는지는 사람이 정한다.
  · pymatgen 이 없으면 아무것도 못 한다 (설치를 권하지 않는다 — MP 웹에서 직접 봐도 된다).
  · MP 가 아닌 다른 출처(예: 지도교수 관례, 옛 외주)일 가능성을 배제하지 못한다.
    MISMATCH 는 "MP 가 아니다" 까지만 말한다.

  python3 tools/sdcp/check_ldauu_provenance.py
  python3 tools/sdcp/check_ldauu_provenance.py --element Co --value 3.32
  python3 tools/sdcp/check_ldauu_provenance.py --selftest
"""
import argparse
import glob
import os
import sys

OUR_U = 6.2
OUR_ELEMENT = "Ni"


def find_element_u(ldauu, element):
    """LDAUU 딕셔너리에서 element 의 U 를 전부 찾는다 -> [(anion_group, value)].

    MP 의 LDAUU 는 {음이온: {원소: U}} 중첩이다 (O 그룹 · F 그룹).
    평평한 {원소: U} 형태도 받는다.
    """
    hits = []

    def walk(node, path=""):
        if not isinstance(node, dict):
            return
        for k, v in node.items():
            if isinstance(v, dict):
                walk(v, path + k + "/")
            elif k == element:
                hits.append((path or "(flat)", v))

    walk(ldauu)
    return hits


def verdict(hits, our_value):
    """[(group, U)] -> (판정, 설명). 값이 여럿이면 하나라도 맞으면 MATCH."""
    if not hits:
        return "NOT_FOUND", "설정에 이 원소의 U 가 없다"
    vals = [v for _, v in hits]
    if any(abs(float(v) - our_value) < 1e-9 for v in vals):
        return "MATCH", f"우리 값 {our_value} 와 일치 (찾은 값 {vals})"
    return "MISMATCH", f"우리 값 {our_value} 와 다르다 (찾은 값 {vals})"


def collect_configs():
    """로컬 pymatgen 에서 LDAUU 를 담은 설정들을 모은다 -> {출처: ldauu}."""
    import pymatgen  # noqa: F401  (없으면 호출부에서 잡는다)

    found = {}
    try:
        from pymatgen.io.vasp.sets import MPRelaxSet
        for attr in ("CONFIG", "_config_dict"):
            cfg = getattr(MPRelaxSet, attr, None)
            if isinstance(cfg, dict) and "INCAR" in cfg:
                found["API.MPRelaxSet." + attr] = cfg["INCAR"].get("LDAUU", {})
                break
    except Exception as exc:                                    # noqa: BLE001
        print(f"   (API 경로 실패: {exc})", file=sys.stderr)

    try:
        import yaml
        # ⚠ pymatgen 은 namespace package 라 __file__ 이 None 일 수 있다 (2026-08-23 gabia 실측:
        #   "expected str, bytes or os.PathLike object, not NoneType"). __path__ 로 받는다.
        root = (os.path.dirname(pymatgen.__file__) if getattr(pymatgen, "__file__", None)
                else next(iter(pymatgen.__path__), None))
        if not root:
            raise RuntimeError("pymatgen 설치 경로를 못 찾았다")
        for path in sorted(glob.glob(root + "/**/MPRelaxSet.yaml", recursive=True)):
            data = yaml.safe_load(open(path)) or {}
            found[path.replace(root, "pymatgen")] = data.get("INCAR", {}).get("LDAUU", {})
    except Exception as exc:                                    # noqa: BLE001
        print(f"   (YAML 경로 실패: {exc})", file=sys.stderr)

    return found


def selftest():
    """양성 + **음성** 경로. 음성이 없으면 통과해도 아무것도 보증 못 한다."""
    cases = [
        # (이름, ldauu, element, our, 기대 판정)
        ("중첩 O 그룹에서 찾기", {"O": {"Co": 3.32, "Ni": 6.2}}, "Ni", 6.2, "MATCH"),
        ("평평한 형태",         {"Ni": 6.2},                     "Ni", 6.2, "MATCH"),
        ("⛔ 값이 다르면 잡는다", {"O": {"Ni": 6.0}},              "Ni", 6.2, "MISMATCH"),
        ("⛔ 원소가 없으면 잡는다", {"O": {"Co": 3.32}},           "Ni", 6.2, "NOT_FOUND"),
        ("⛔ 빈 설정",           {},                              "Ni", 6.2, "NOT_FOUND"),
        ("⛔ 다른 원소를 U 로 오인하지 않는다",
         {"O": {"Nb": 6.2}}, "Ni", 6.2, "NOT_FOUND"),
        ("F 그룹도 훑는다",     {"F": {"Ni": 6.0}, "O": {"Ni": 6.2}}, "Ni", 6.2, "MATCH"),
    ]
    bad = 0
    for name, ldauu, el, our, want in cases:
        got, why = verdict(find_element_u(ldauu, el), our)
        ok = got == want
        bad += not ok
        print(f"  {'✅' if ok else '⛔'} {name}: {got}" + ("" if ok else f"  (기대 {want} · {why})"))
    print(f"\nselftest: {len(cases) - bad}/{len(cases)} 통과")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--element", default=OUR_ELEMENT)
    ap.add_argument("--value", type=float, default=OUR_U, help="우리 값 (기본 6.2)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    try:
        import pymatgen
    except ImportError:
        print("⛔ pymatgen 이 없다.")
        print("   설치할 것 없이 Materials Project 웹에서 LiNiO2 엔트리의 계산 상세 →")
        print("   LDAUU 를 봐도 같은 답이 나온다.")
        return 2

    ver = getattr(pymatgen, "__version__", None)
    if not ver:
        try:
            from importlib.metadata import version as _v
            ver = _v("pymatgen")
        except Exception:                                       # noqa: BLE001
            ver = "?"
    print(f"pymatgen {ver}")
    configs = collect_configs()
    if not configs:
        print("⛔ LDAUU 를 담은 설정을 못 찾았다 — pymatgen 버전을 알려줄 것")
        return 2

    results = []
    for src, ldauu in configs.items():
        hits = find_element_u(ldauu, args.element)
        v, why = verdict(hits, args.value)
        results.append(v)
        print(f"\n[{src}]")
        for group, val in hits:
            print(f"   {args.element}  U = {val}   (anion group: {group})")
        ox = ldauu.get("O") if isinstance(ldauu, dict) else None
        if isinstance(ox, dict):
            side = {k: ox[k] for k in ("Co", "Mn", "Ni", "Fe") if k in ox}
            print(f"   O-group 대조: {side}")
        print(f"   → {v} — {why}")

    print()
    if "MATCH" in results:
        print(f"✅ MATCH — 우리 U({args.element}) = {args.value} 는 MP 기본값과 같다.")
        print("   인용 후보: Wang, Maxisch, Ceder, Phys. Rev. B 73, 195107 (2006)")
        print("             Jain et al., Phys. Rev. B 84, 045115 (2011)")
        print("   ⚠ 이건 '같은 값' 까지다. '이 계에 옳다' 는 별개(U 민감도 미실시).")
        return 0
    print(f"⛔ MP 기본값이 아니다 — 우리 {args.element} U 의 출처는 다른 데 있다.")
    print("   Table S1 의 Source 는 '-' 로 두고, 이 사실을")
    print("   kb/syntheses/sdcp_eads_revision_defense_2026_08_23.md 에 기록할 것.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
