#!/usr/bin/env python3
"""site_preference.py — Phase-A 자세들이 **어느 표면 양이온 위에 앉았나**를 집계한다.

왜 필요한가 (2026-08-06 1저자: "신기하네 Ni 위로 안 가는게")
  챔피언 두 개가 다 Li 위였다. 그런데 그게 "Ni 를 이겼다"인지 "Ni 를 안 재봤다"인지는
  전혀 다른 이야기다. 앞은 결과고, 뒤는 스캔 설계의 구멍이다 — 심사에서 반드시 물어본다.
  216개 자세는 이미 다 있으므로 새 계산 없이 답할 수 있다.

무엇을 하나
  자세마다 분자의 **표면에 가장 가까운 원자**(앵커)를 잡고, 그 앵커에서 가장 가까운
  표면 양이온의 원소로 자세를 분류한 뒤 E_bind 분포를 낸다.

⚠ 해석 주의
  · UMA E_bind 는 **순위용**이다 (Phase-A CSV 자체가 그렇게 적어 놨다). 절대값 인용 금지.
  · Phase-A 는 슬랩을 통째로 얼렸다(freeze_frac 1.0). Ni 자리 결합은 표면 재배열을
    동반하는 경우가 많아 **고정 슬랩이 Ni 쪽에 불리하게 작용할 수 있다** — 이 표는
    "고정 슬랩 + UMA 기준의 자리 선호"이지 열역학적 자리 선호가 아니다.

  python3 tools/sdcp/site_preference.py                       # 기본 경로
  python3 tools/sdcp/site_preference.py --scan <dir> --slab <slab.vasp>
"""
import argparse
import csv
import glob
import os
import sys
from collections import defaultdict

import numpy as np
from ase.io import read

DEF_SCAN = "/data/work/runs/sdcp_v2/phaseA"
DEF_SLAB = "db/structures/linio2_104_sym_1x4L4_relaxed.vasp"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", default=DEF_SCAN)
    ap.add_argument("--slab", default=None, help="셀·표면 판정용 슬랩 (기본: repo 이완본)")
    ap.add_argument("--nslab", type=int, default=192)
    ap.add_argument("--csv", default=None, help="기본: <scan>/phaseA_v7c_results.csv")
    ap.add_argument("--surf", type=float, default=2.0, help="표면으로 볼 두께 [Å]")
    a = ap.parse_args()

    slabf = a.slab
    if not slabf:
        here = os.path.join(os.path.dirname(__file__), "..", "..", DEF_SLAB)
        slabf = here if os.path.isfile(here) else None
    if not slabf or not os.path.isfile(slabf):
        sys.exit(f"⛔ 슬랩 파일을 못 찾았다 — --slab 로 지정할 것 (찾은 값: {slabf})")
    slab = read(slabf)
    cell = slab.cell.array.copy()

    # E_bind 표 (없어도 자리 분류는 된다)
    eb = {}
    cpath = a.csv or os.path.join(a.scan, "phaseA_v7c_results.csv")
    if os.path.isfile(cpath):
        with open(cpath) as f:
            for row in csv.DictReader(l for l in f if not l.startswith("#")):
                try:
                    if int(row.get("converged", 1)):
                        eb[row["label"]] = float(row["E_bind_eV"])
                except (ValueError, KeyError, TypeError):
                    pass
        print(f"E_bind 표: {cpath}  ({len(eb)}개 수렴)")
    else:
        print(f"⚠ {cpath} 없음 — 자리 분류만 한다 (에너지 없음)")

    files = sorted(glob.glob(os.path.join(a.scan, "complex_*.xyz")))
    if not files:
        sys.exit(f"⛔ {a.scan} 에 complex_*.xyz 가 없다")

    groups = defaultdict(list)     # (tag, site_el) -> [(E, label, d)]
    contacts = []                  # (tag, label, E, d_min, pair, site)
    nprob = 0
    for fp in files:
        label = os.path.basename(fp)[len("complex_"):-len(".xyz")]
        at = read(fp)
        if len(at) <= a.nslab:
            nprob += 1; continue
        at.set_cell(cell); at.set_pbc(True)
        sym = at.get_chemical_symbols()
        z = at.positions[:, 2]
        ztop = z[:a.nslab].max()
        cats = [i for i in range(a.nslab)
                if sym[i] in ("Li", "Ni") and z[i] > ztop - a.surf]
        mol = list(range(a.nslab, len(at)))
        # 앵커 = 표면에 가장 가까운 분자 원자
        anchor = min(mol, key=lambda i: z[i])
        d = at.get_distances(anchor, cats, mic=True)
        k = int(np.argmin(d))
        site = sym[cats[k]]
        tag = label.split("_")[0]                       # doped / neutral
        groups[(tag, site)].append((eb.get(label), label, float(d[k])))
        # 전 쌍 최단 접촉 — "UMA 순위가 표면 접촉을 따라가나"를 보려고 따로 잰다
        dmin, dpair = 1e9, ""
        for m in mol:
            dd = at.get_distances(m, list(range(a.nslab)), mic=True)
            j = int(np.argmin(dd))
            if dd[j] < dmin:
                dmin, dpair = float(dd[j]), f"{sym[m]}···{sym[j]}"
        contacts.append((tag, label, eb.get(label), dmin, dpair, site))

    if nprob:
        print(f"⚠ 원자수가 --nslab({a.nslab}) 이하인 파일 {nprob}개는 건너뜀")

    print("\n① 자세가 어느 양이온 위에 앉았나  (앵커 = 분자 최하단 원자)")
    print(f"{'종':8s} {'자리':4s} {'개수':>5s}  {'최저 E_bind':>12s}  {'중앙값':>9s}  "
          f"{'앵커–양이온 최단':>14s}   최저 자세")
    order = sorted(groups, key=lambda k: (k[0], k[1]))
    for key in order:
        tag, site = key
        rows = groups[key]
        es = sorted([r[0] for r in rows if r[0] is not None])
        best = min((r for r in rows if r[0] is not None), key=lambda r: r[0], default=None)
        med = f"{es[len(es)//2]:+.3f}" if es else "—"
        print(f"{tag:8s} {site:4s} {len(rows):5d}  "
              f"{(f'{es[0]:+.3f}' if es else '—'):>12s}  {med:>9s}  "
              f"{min(r[2] for r in rows):11.2f} Å   {best[1] if best else '—'}")

    print("\n② 판정")
    for tag in sorted({k[0] for k in groups}):
        sites = {k[1]: groups[k] for k in groups if k[0] == tag}
        if len(sites) < 2:
            only = next(iter(sites))
            print(f"   ⛔ {tag}: **{only} 자리밖에 없다** — 다른 양이온 자리를 스캔이 "
                  f"애초에 만들지 않았다는 뜻이다. '{only} 를 선호한다'고 쓸 수 없다"
                  " (재본 적이 없으니까). 격자를 넓혀 다시 스캔할 것.")
            continue
        best = {s: min((r[0] for r in v if r[0] is not None), default=None)
                for s, v in sites.items()}
        if any(v is None for v in best.values()):
            print(f"   · {tag}: 에너지가 없는 자리가 있어 비교 보류")
            continue
        lo = min(best, key=lambda s: best[s])
        hi = [s for s in best if s != lo]
        gaps = {s: best[s] - best[lo] for s in hi}
        print(f"   · {tag}: 최저는 **{lo}** ({best[lo]:+.3f}) · "
              + " · ".join(f"{s} 는 {gaps[s]:+.3f} eV 불리 ({best[s]:+.3f})" for s in hi))
        if min(gaps.values()) < 0.05:
            print("     ⚠ 차이가 50 meV 미만 — UMA 순위로 자리를 가릴 수 있는 폭이 아니다.")

    # ③ UMA 순위가 '표면 접촉'을 따라가나 — 안 따라가면 순위 자체가 표면 얘기가 아니다.
    print("\n③ E_bind 가 표면 접촉거리를 따라가나  (분자↔슬랩 전 쌍 최단)")
    for tag in sorted({c[0] for c in contacts}):
        rows = [c for c in contacts if c[0] == tag and c[2] is not None]
        if len(rows) < 5:
            continue
        E = np.array([r[2] for r in rows]); D = np.array([r[3] for r in rows])
        r = float(np.corrcoef(E, D)[0, 1]) if E.std() > 0 and D.std() > 0 else float("nan")
        print(f"   {tag:8s} n={len(rows):3d} · d_min {D.min():.2f}–{D.max():.2f} Å · "
              f"상관 r(E_bind, d_min) = {r:+.2f}")
        print("     " + ("· 상관을 낼 수 없다 (거리 또는 에너지가 전부 같다)" if np.isnan(r) else
                         "· 더 가까울수록 더 붙는다 — 순위가 표면 상호작용을 반영한다"
                         if r < -0.3 else
                         "⚠ 상관이 약하다 — 순위가 표면 접촉이 아니라 다른 것(분자 변형·"
                         "분산 접촉면적)에 끌려간다는 뜻. 자세 선택의 근거가 약해진다"))
        for c in sorted(rows, key=lambda x: x[2])[:3]:
            print(f"       {c[2]:+.3f} eV  d_min {c[3]:.2f} Å ({c[4]}) · {c[5]} 자리 · {c[1]}")

    print("\n⚠ 이 표는 '고정 슬랩(freeze_frac 1.0) + UMA' 기준의 자리 선호다.")
    print("   Ni 자리 결합은 표면 재배열을 동반하는 일이 많아 고정 슬랩이 불리하게 작용할 수 있고,")
    print("   UMA 는 산화상태·스핀을 명시적으로 안 본다 — 즉 Li vs Ni 는 UMA 가 제일 약한 종류의 질문이다.")
    print("   결론으로 쓰려면 Ni 자리 최저 자세도 DFT+U 로 한 점 찍어 대조해야 한다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
