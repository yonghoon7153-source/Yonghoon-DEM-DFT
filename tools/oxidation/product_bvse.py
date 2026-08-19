#!/usr/bin/env python3
"""product_bvse.py — 계면 **분해산물**이 Li 를 통과시키는지 BVSE 로 싸게 잰다.

왜 (2026-08-19)
  계면 판정에 세 조각이 필요한데 둘만 있었다:
    ① 반응이 일어나나        → 열역학    ✅ cascade_interface_*.jsonl
    ② 생긴 층이 전자를 막나  → 밴드갭    ✅ cascade_product_gaps.json (69 % 가 금속 산물)
    ③ 생긴 층이 Li 를 통과시키나 → **이 도구**
  ③ 없이는 "69 % 가 금속" 이 얼마나 나쁜지 말할 수 없다. 전자를 막아도 Li 를 막으면
  저항층이고, 전자를 통해도 Li 를 잘 통하면 자가방전이다 — 두 축을 같이 봐야 판정이 된다.

무엇을 하나
  cascade_product_gaps.json 의 mp-id 로 MP 에서 구조를 받아, 우리 BVSE 도구
  (tools/comp1_v3/compute_bvse_map.py — 14장 지형 그림에 쓴 그것)를 태우고,
  퍼콜레이션 onset(=이 문턱 아래가 셀을 관통해 이어지는 최소 BVSE)을 낸다.

이 도구가 **못 하는 것**
  · eV 가 아니다. softBV 경험값(valence²)이라 **순서로만** 쓴다. NEB 대체 아님.
  · 파라미터가 없는 음이온(F·Br·I·N)은 **재지 않고 사유를 남긴다.** ⛔ 그냥 돌리면
    compute_bvse_map 이 그 원소를 음이온으로 **안 세고 조용히 틀린 답**을 낸다.
  · 금속간 화합물(음이온 없음)은 애초에 BVSE 가 의미 없다 — 건너뛴다.
  · 실제 층은 다결정·비정질일 수 있다. 여기 값은 **결정 벌크** 기준이다.

  python3 tools/oxidation/product_bvse.py --selftest
  python3 tools/oxidation/product_bvse.py --limit 5      # 시범
  python3 tools/oxidation/product_bvse.py                # 전수
"""
import argparse, io, json, os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "comp1_v3"))

GAPS = ROOT / "db" / "properties" / "cascade_product_gaps.json"
OUT = ROOT / "db" / "properties" / "cascade_product_bvse.json"

#: CLAUDE.md 가 못박은 softBV Li–X R0 (b=0.37). **이 셋 밖은 재지 않는다.**
HAVE_ANIONS = {"S", "Cl", "O"}
ANIONS = {"O", "S", "Cl", "F", "Br", "I", "N", "Se", "Te"}
#: 채널 부피를 재는 iso 준위 (valence², above-min) — 기존 표와 같은 값
ISO_LEVELS = (0.25, 0.5, 1.0, 2.0)


def elements_of(formula):
    return set(re.findall(r"[A-Z][a-z]?", formula))


def can_measure(formula):
    """(가능?, 사유). ⛔ 조용히 건너뛰지 않는다 — 사유를 문장으로 남긴다."""
    els = elements_of(formula)
    if "Li" not in els:
        return False, "Li 가 없다 — 이 층은 애초에 Li 를 못 나른다"
    an = els & ANIONS
    if not an:
        return False, "음이온이 없다 (금속간 화합물) — BVSE 가 정의되지 않는다"
    if not an <= HAVE_ANIONS:
        bad = sorted(an - HAVE_ANIONS)
        return False, (f"softBV R0 없음: {'/'.join(bad)} — 그냥 돌리면 그 원소를 "
                       f"음이온으로 안 세고 조용히 틀린 답이 나온다")
    return True, ""


def percolation_onset(bvse, n_levels=60):
    """이 문턱 아래가 셀을 **관통**하는 최소 BVSE (above-min). 없으면 None."""
    import numpy as np
    from scipy import ndimage
    from bvse_percolation_analysis import percolates
    m = bvse - float(bvse.min())
    hi = float(np.percentile(m, 60))
    for lv in np.linspace(m.min(), hi, n_levels):
        mask = m <= lv
        lab, n = ndimage.label(mask, structure=np.ones((3, 3, 3)))
        if n == 0:
            continue
        for i in range(1, n + 1):
            if any(percolates(lab == i, ax) for ax in range(3)):
                return float(lv)
    return None


def run_one(struct, grid=24):
    """ASE Atoms → (onset, iso 채널부피 %, Li 자리 BVS 평균)."""
    import numpy as np
    from compute_bvse_map import compute_bvs_map, existing_li_bvs
    import numpy as _np
    L = _np.linalg.norm(_np.array(struct.get_cell()), axis=1)
    shape = tuple(int(max(10, min(60, round(grid * float(x) / float(L.min())))))
                  for x in L)
    _, bvse = compute_bvs_map(struct, shape)
    m = bvse - float(bvse.min())
    iso = {str(t): round(100.0 * float((m <= t).sum()) / m.size, 3) for t in ISO_LEVELS}
    onset = percolation_onset(bvse)
    try:
        li = existing_li_bvs(struct, shape)
    except Exception:
        li = None
    return onset, iso, shape, li


def selftest():
    ok = True

    def chk(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m)
        ok &= bool(c)

    chk(can_measure("Li2S")[0], "[양성] Li2S 는 잰다 (S 는 파라미터 있음)")
    chk(can_measure("Li3PO4")[0],
        "[양성] Li3PO4 도 잰다 — P 는 다중음이온의 양이온이지 음이온이 아니다")
    chk(not can_measure("LiF")[0] and "F" in can_measure("LiF")[1],
        "[음성] LiF 는 안 잰다 (F softBV R0 없음) + 사유에 F 가 나온다")
    chk(not can_measure("LiAl")[0] and "금속간" in can_measure("LiAl")[1],
        "[음성] 금속간(LiAl)은 안 잰다")
    chk(not can_measure("CoS2")[0] and "Li" in can_measure("CoS2")[1],
        "[음성] Li 없는 상은 안 잰다")
    chk(can_measure("Li7PN4")[0] is False,
        "[음성] N 이 섞이면 막는다 (Li7PN4)")
    if GAPS.exists():
        g = json.load(io.open(GAPS, encoding="utf-8"))
        n = sum(1 for k, v in g["gaps"].items()
                if isinstance(v, dict) and "material_id" in v and can_measure(k)[0])
        chk(n == 78, f"[양성] 산물 중 잴 수 있는 것 78종 (얻은 것 {n})")
    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gaps", default=str(GAPS))
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--limit", type=int)
    ap.add_argument("--grid", type=int, default=24, help="최단축 격자수 (~0.25 Å 목표)")
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    a = ap.parse_args()

    g = json.load(io.open(a.gaps, encoding="utf-8"))
    todo, skipped = [], {}
    for k, v in g["gaps"].items():
        if not (isinstance(v, dict) and "material_id" in v):
            continue
        can, why = can_measure(k)
        (todo.append((k, v["material_id"])) if can else skipped.setdefault(k, why))
    todo.sort()
    if a.limit:
        todo = todo[: a.limit]
    print(f"잴 산물 {len(todo)}종 · 건너뛴 것 {len(skipped)}종 (사유는 출력에 남긴다)")

    key = os.environ.get("MP_API_KEY") or os.environ.get("PMG_MAPI_KEY")
    if not key:
        raise SystemExit("MP_API_KEY 를 설정하고 gabia 에서 돌릴 것")
    from mp_api.client import MPRester
    from pymatgen.io.ase import AseAtomsAdaptor
    import time

    rows, prev = {}, {}
    if Path(a.out).exists():
        prev = json.load(io.open(a.out, encoding="utf-8")).get("products", {})
        print(f"[resume] 기존 {len(prev)}종은 건너뛴다")
    with MPRester(key) as mpr:
        for i, (f, mid) in enumerate(todo, 1):
            if f in prev:
                rows[f] = prev[f]
                continue
            t0 = time.time()
            try:
                st = AseAtomsAdaptor.get_atoms(mpr.get_structure_by_material_id(mid))
                onset, iso, shape, li = run_one(st, a.grid)
                rows[f] = {"material_id": mid, "natoms": len(st), "grid": list(shape),
                           "perc_onset_val2": None if onset is None else round(onset, 3),
                           "iso_channel_pct": iso,
                           "Li_site_BVS_mean": None if li is None else round(
                               float(li.get("mean", li) if isinstance(li, dict) else li), 3),
                           "seconds": round(time.time() - t0, 1)}
                print(f"[{i}/{len(todo)}] {f:16s} onset "
                      f"{'—' if onset is None else '%.3f' % onset}  "
                      f"iso0.5 {iso['0.5']:5.2f} %  ({rows[f]['seconds']:.0f}s)")
            except Exception as ex:
                rows[f] = {"material_id": mid, "error": f"{type(ex).__name__}: {ex}"[:160]}
                print(f"[{i}/{len(todo)}] {f:16s} ERR {type(ex).__name__}")

    Path(a.out).write_text(json.dumps({
        "note": "softBV BVSE on interface decomposition products. perc_onset_val2 = "
                "lowest above-min BVSE whose sub-threshold region percolates through "
                "the cell. LOWER = Li moves more easily.",
        "caveat": "Empirical softBV (valence^2), NOT eV and NOT a NEB barrier. Use "
                  "ORDER only. Crystalline bulk - the real interphase may be amorphous.",
        "softBV_R0": {"S": 2.105, "Cl": 2.249, "O": 1.466, "b": 0.37},
        "iso_levels_val2": list(ISO_LEVELS),
        "skipped_with_reason": skipped,
        "products": rows,
    }, ensure_ascii=False, indent=2))
    print(f"\n→ {a.out}  ({len(rows)}종)")


if __name__ == "__main__":
    main()
