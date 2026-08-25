#!/usr/bin/env python3
"""axis_corr_csv.py — 정본 cascade CSV 의 **목적 축들이 서로 붙어 있나**를 본다.

왜 (2026-08-25, Yang 2026(BML) `Fig. 17` 에서 이전):
  다목적 최적화는 축이 **독립일 때만** 일을 한다. 두 축이 좁은 띠를 그리면 그건 사실상
  한 축이고, Pareto 를 돌려도 그 축은 안 움직인다. 저쪽 실측: σ↔Q_CC 가 붙어 있어
  Pareto 후 σ 는 −2.9 %, 독립축인 Damage 만 −64.5 % 였다.
  우리는 지금 가중합(`--w_e/w_v/w_s/w_c`)으로 축을 하나의 숫자로 **뭉개고** 있어서
  충돌이 있는지조차 화면에 안 나온다 (open_items #11: b2o3 전도 1등 ↔ 공기안정성 최악군).

  ⚠ 출처는 **DEM 축 문헌**이고 여기 적용 대상은 **DFT 축 cascade** 다. 이전한 것은
    수치가 아니라 **절차**뿐이다 (kb/methodology/microstructure_ml_transfer_to_cascade_2026_08_25.md).

이 도구가 **못 하는 것**
  · 인과를 말하지 않는다. 붙어 있다 ≠ 하나가 다른 하나를 만든다.
  · 상관이 낮다고 그 축이 **중요한** 것도 아니다 — 독립일 뿐이다.
  · 결측이 많은 축은 그 사실만 적고 판정하지 않는다 (적은 표본의 ρ 는 못 믿는다).
  · 순위를 매기거나 후보를 고르지 않는다.

    python3 tools/doping/axis_corr_csv.py
    python3 tools/doping/axis_corr_csv.py --csv <경로> --min_n 50
    python3 tools/doping/axis_corr_csv.py --selftest
"""
from __future__ import annotations

import argparse
import csv
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_CSV = os.path.join(ROOT, "db", "properties", "cascade_v23_all.csv")

#: |ρ| 가 이보다 크면 '사실상 한 축' 으로 본다.
COLLINEAR = 0.85
#: 이보다 표본이 적으면 판정하지 않는다 — 적은 n 의 ρ 는 우연이 쉽다.
MIN_N = 30

#: 우리 cascade 의 목적 축. **부호를 여기서 통일한다** — "클수록 좋다" 로 맞춰야
#: 상관의 부호가 곧 '같이 좋아지나 / 반대로 가나' 를 뜻한다.
#:   (열이름, 표시이름, higher_is_better)
AXES = [
    ("screen_de_per_atom",      "안정성(ΔE)",   False),   # 낮을수록 안정
    ("li_mobility_score",       "Li 이동도",    True),
    ("sigma_300K_S_cm_NE",      "σ(300K)",      True),
    ("bvs_li_proxy_score",      "BVS 프록시",   True),
    ("elastic_G_hill_GPa",      "전단탄성 G",   True),
    ("elastic_pugh_GoverB",     "Pugh G/B",     False),   # 낮을수록 연성
    ("wad_J_m2_mean",           "부착일 W_ad",  True),
    ("screen_dV_over_V0",       "|ΔV/V0|",      False),   # 작을수록 좋다(절대값)
    ("migration_volume_fraction", "이동부피비", True),
]

#: ⛔ **파생 축** — 다른 축들의 산술 조합이라 그 축들과의 상관이 **정의상** 높다.
#:   그걸 '독립성이 깨졌다' 로 읽으면 안 된다. 발견이 아니라 공식이다.
#:   li_mobility_score = 3*migration_volume_fraction + bvs_li_proxy_score
#:     (tools/doping/bvse_proxy.py backfill_one)
#:   실측: ρ(이동도, 이동부피비)=+0.77 · ρ(이동도, BVS)=+0.48 — 3:1 가중과 정확히 정합.
DERIVED = {
    "li_mobility_score": ("migration_volume_fraction", "bvs_li_proxy_score"),
}


def is_definitional(a, b):
    """두 축이 '파생 축 ↔ 그 재료' 관계인가. → bool"""
    return b in DERIVED.get(a, ()) or a in DERIVED.get(b, ())


def _f(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def spearman(a, b):
    """순위 상관 (scipy 없이). 동점은 평균순위. 못 재면 None."""
    if len(a) < 3:
        return None
    if len(set(a)) < 2 or len(set(b)) < 2:
        return None          # 한쪽이 상수 — 상관이 정의되지 않는다

    def rank(x):
        order = sorted(range(len(x)), key=lambda i: x[i])
        r = [0.0] * len(x)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and x[order[j + 1]] == x[order[i]]:
                j += 1
            avg = (i + j) / 2.0
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    ra, rb = rank(a), rank(b)
    ma, mb = sum(ra) / len(ra), sum(rb) / len(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))
    return num / den if den else None


def load(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def analyse(rows, min_n=MIN_N):
    cols, cover = {}, {}
    for key, label, hib in AXES:
        vals = [_f(r.get(key)) for r in rows]
        n = sum(v is not None for v in vals)
        cover[key] = (label, n, len(rows))
        if n >= min_n:
            # 부호 통일: 전부 "클수록 좋다" 로. |ΔV| 는 절대값을 먼저 취한다.
            if key == "screen_dV_over_V0":
                vals = [abs(v) if v is not None else None for v in vals]
            cols[key] = (label, [(-v if (v is not None and not hib) else v) for v in vals])
    pairs = []
    keys = list(cols)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            va, vb = [], []
            for x, y in zip(cols[a][1], cols[b][1]):
                if x is not None and y is not None:
                    va.append(x); vb.append(y)
            if len(va) < min_n:
                pairs.append({"a": a, "b": b, "la": cols[a][0], "lb": cols[b][0],
                              "rho": None, "n": len(va), "collinear": False,
                              "definitional": is_definitional(a, b),
                              "why": "표본 부족"})
                continue
            rho = spearman(va, vb)
            pairs.append({"a": a, "b": b, "la": cols[a][0], "lb": cols[b][0],
                          "rho": rho, "n": len(va),
                          "collinear": bool(rho is not None and abs(rho) >= COLLINEAR),
                          "definitional": is_definitional(a, b),
                          "why": None if rho is not None else "한쪽이 상수"})
    pairs.sort(key=lambda p: -(abs(p["rho"]) if p["rho"] is not None else -1))
    return {"pairs": pairs, "coverage": cover, "n_rows": len(rows), "min_n": min_n}


def report(rep):
    print(f"\n{'='*76}")
    print(f" cascade 목적 축 상관 — Pareto·가중치 조정이 일을 할 수 있나 (행 {rep['n_rows']})")
    print(f"{'='*76}")
    print("  ⚠ 부호는 '클수록 좋다' 로 통일했다 — ρ>0 = 같이 좋아진다 · ρ<0 = 상충(trade-off)\n")
    print("  ── 축 커버리지 (결측이 많으면 판정 자체를 안 한다) ──")
    for key, (label, n, tot) in rep["coverage"].items():
        pct = 100.0 * n / tot if tot else 0
        mark = "✅" if n >= rep["min_n"] else "·"
        print(f"    {mark} {label:12s} {n:5d}/{tot} ({pct:5.1f} %)  {key}")
    print("\n  ── 축 쌍 ──")
    col = [p for p in rep["pairs"] if p["collinear"] and not p.get("definitional")]
    defn = [p for p in rep["pairs"] if p.get("definitional") and p["rho"] is not None]
    trade = [p for p in rep["pairs"]
             if p["rho"] is not None and p["rho"] <= -0.3
             and not p["collinear"] and not p.get("definitional")]
    for p in rep["pairs"]:
        if p["rho"] is None:
            print(f"    ·  {p['la']:12s} ↔ {p['lb']:12s}   ρ = —      ({p['why']}, n={p['n']})")
            continue
        if p.get("definitional"):
            m, tail = "📐", "   ← 정의상 (파생축 ↔ 그 재료)"
        else:
            m = "⛔" if p["collinear"] else ("🔻" if p["rho"] <= -0.3 else
                                            ("🟡" if abs(p["rho"]) >= 0.6 else "✅"))
            tail = ""
        print(f"    {m} {p['la']:12s} ↔ {p['lb']:12s}   ρ = {p['rho']:+.3f}   n={p['n']}{tail}")
    print()
    if col:
        print(f"  ⛔ **사실상 한 축인 쌍 {len(col)}건** — 그 축들끼리는 Pareto 가 선택지를 못 준다:")
        for p in col:
            print(f"       {p['la']} ↔ {p['lb']}  (ρ {p['rho']:+.3f})")
    if trade:
        print(f"  🔻 **상충하는 쌍 {len(trade)}건** — 여기가 다목적이 실제로 일하는 자리다:")
        for p in trade[:6]:
            print(f"       {p['la']} ↔ {p['lb']}  (ρ {p['rho']:+.3f})")
    if defn:
        print(f"  📐 **정의상 붙은 쌍 {len(defn)}건 — 판정에서 제외했다.**")
        for p in defn:
            print(f"       {p['la']} ↔ {p['lb']}  (ρ {p['rho']:+.3f})  "
                  f"{p['a'] if p['a'] in DERIVED else p['b']} 가 상대의 산술 조합이다")
        print(f"     발견이 아니라 공식이다 — 독립성 판정의 근거로 쓰면 안 된다.")
    free = [p for p in rep["pairs"]
            if p["rho"] is not None and not p.get("definitional")]
    if free:
        top = max(free, key=lambda p: abs(p["rho"]))
        print(f"  ▸ **정의상 쌍을 뺀 최대 |ρ| = {abs(top['rho']):.3f}** "
              f"({top['la']} ↔ {top['lb']}) — 공선성 문턱 {COLLINEAR} 대비")
    if not col and not trade:
        print("  ✅ 뚜렷한 공선성도 상충도 없다 — 축이 대체로 독립이다.")
    print("\n  ⛔ 인과는 말하지 않는다. 상관이 낮다고 그 축이 중요한 것도 아니다(독립일 뿐).")


def _selftest():
    ok = True

    def say(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m)
        ok = ok and c

    print("── axis_corr_csv selftest ──")
    say(abs(spearman(list(range(20)), list(range(20))) - 1.0) < 1e-12, "① 완전 일치 → ρ=1")
    say(abs(spearman(list(range(20)), list(range(19, -1, -1))) + 1.0) < 1e-12,
        "① 완전 역순 → ρ=−1")
    say(spearman([1, 1, 1], [1, 2, 3]) is None, "② [음성] 한쪽이 상수면 None (0 이 아니다)")
    say(spearman([1, 2], [1, 2]) is None, "② [음성] 표본 3 미만이면 None")
    say(abs(spearman([1, 2, 2, 3], [1, 2, 2, 3]) - 1.0) < 1e-12, "③ 동점 평균순위 처리")
    # ④ [음성] 결측이 많은 축은 판정에서 빠져야 한다
    rows = [{"screen_de_per_atom": str(i), "li_mobility_score": ""} for i in range(50)]
    rep = analyse(rows, min_n=30)
    say(all(p["a"] != "li_mobility_score" and p["b"] != "li_mobility_score"
            for p in rep["pairs"]),
        "④ [음성] 결측 축은 쌍에서 빠진다 (적은 n 의 ρ 를 믿지 않는다)")
    # ⑤ 부호 통일 — '낮을수록 좋은' 두 축은 뒤집힌 뒤 **양의 상관**이어야 한다
    rows = [{"screen_de_per_atom": str(i), "screen_dV_over_V0": str(i / 100.0)}
            for i in range(60)]
    rep = analyse(rows, min_n=30)
    p = rep["pairs"][0]
    say(p["rho"] is not None and p["rho"] > 0.99,
        f"⑤ 낮을수록 좋은 두 축은 부호 통일 뒤 ρ>0 ({p['rho']})")
    # ── 파생 축 (2026-08-25) ────────────────────────────────────────────
    say(is_definitional("li_mobility_score", "migration_volume_fraction"),
        "⑥ 파생축 ↔ 그 재료를 '정의상' 으로 잡는다")
    say(is_definitional("migration_volume_fraction", "li_mobility_score"),
        "⑥ 순서를 바꿔도 잡는다")
    say(not is_definitional("screen_de_per_atom", "elastic_G_hill_GPa"),
        "⑥ [음성] 무관한 두 축을 정의상으로 오인하지 않는다")
    say(not is_definitional("migration_volume_fraction", "bvs_li_proxy_score"),
        "⑥ [음성] 같은 공식의 **재료끼리**는 정의상 아니다 (서로 독립 측정)")

    print("  " + ("✅ selftest 통과" if ok else "⛔ selftest 실패"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", default=DEFAULT_CSV)
    ap.add_argument("--min_n", type=int, default=MIN_N)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not os.path.isfile(a.csv):
        print(f"⛔ 없다: {a.csv}")
        return 2
    report(analyse(load(a.csv), a.min_n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
