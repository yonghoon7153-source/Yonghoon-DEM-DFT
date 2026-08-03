#!/usr/bin/env python3
"""harvest_msd_curves.py — MD 런 디렉토리의 msd.json 을 그림용 공통 격자 CSV 로 모은다.

왜 필요한가
  db/properties 에는 D·Ea 만 있고 **MSD 시계열은 없다**. 곡선은 각 런 디렉토리의
  msd.json 안에만 있어서, 그림을 그리려면 매번 서버를 뒤져야 했다.
  기존 3계 CSV(msd_LPSCl_LPSCl16_b2o3.csv)는 손으로 만든 것이라 LPSOCl 을 붙일 수 없었다.

  # gabia/kgy 에서 (런 디렉토리가 있는 쪽)
  python3 tools/figures/harvest_msd_curves.py \
      --run lpsocl=~/work/runs/lpsocl_md/ladder \
      --out db/properties/msd_lpsocl_origin.csv

⚠⚠ **단일 시드 MSD 는 '계층 예시'로만 쓴다.** 정량 D/Ea/sigma 는 멀티시드 산출물
  (lpsocl_md_arrhenius.json 등)에서 가져온다 — 기존 CSV 머리말도 그렇게 적혀 있다.
  곡선 하나에서 기울기를 읽어 D 라고 인용하면 안 된다.

⚠ 공통 격자(0-49 ps @ 1 ps)로 **선형보간**한다. 원 저장 간격(save_fs 100 = 0.1 ps)이
  계마다 같더라도, 격자를 맞춰야 여러 계를 한 CSV·한 그림에 올릴 수 있다.
  보간은 표시용이며 D 는 원 시계열에서 계산된 값을 쓴다(위 규율).
"""
import argparse
import csv
import glob
import json
import os
import re

import numpy as np

T_WANT = (600, 800, 1000)
GRID = np.arange(0.0, 50.0, 1.0)          # 기존 3계 CSV 와 동일한 격자


def find_msd(root, T):
    """run_root 아래에서 온도 T 의 msd.json 을 찾는다. 여러 개면 시드 최소(대표)."""
    hits = []
    for f in glob.glob(os.path.join(os.path.expanduser(root), "**", "msd.json"),
                       recursive=True):
        try:
            d = json.load(open(f))
        except Exception:
            continue
        if abs(float(d.get("T_K", -1)) - T) < 1:
            hits.append((f, d))
    if not hits:
        return None, None
    # ⚠ 시드가 여럿이면 **가장 작은 시드**를 대표로 고른다(임의 선택 금지 — 재현 가능해야).
    hits.sort(key=lambda x: (re.findall(r"s(\d+)", x[0]) or ["0"])[0])
    return hits[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="append", required=True,
                    metavar="LABEL=PATH", help="예: lpsocl=~/work/runs/lpsocl_md/ladder")
    ap.add_argument("--out", required=True)
    ap.add_argument("--merge", help="기존 CSV 에 열을 덧붙인다(같은 격자여야 한다)")
    a = ap.parse_args()

    cols, meta = {}, []
    for spec in a.run:
        label, root = spec.split("=", 1)
        for T in T_WANT:
            f, d = find_msd(root, T)
            if d is None:
                print(f"  ⛔ {label} {T} K — msd.json 못 찾음 ({root})")
                continue
            t = np.asarray(d["times_ps"], float)
            y = np.asarray(d["msd_Li_A2"], float)
            if t.max() < GRID.max():
                print(f"  ⚠ {label} {T} K — 궤적이 {t.max():.0f} ps 로 짧다. "
                      f"{GRID.max():.0f} ps 격자 뒤쪽은 비운다.")
            g = np.where(GRID <= t.max(), np.interp(GRID, t, y), np.nan)
            cols[f"{label}_{T}K"] = g
            meta.append(f"{label} {T}K ← {os.path.relpath(f, os.path.expanduser(root))} "
                        f"(D={d.get('D_Li_cm2_s', float('nan')):.4e} cm2/s)")
            print(f"  ✓ {label} {T} K  ({len(t)}점 → 격자 {len(GRID)}점, "
                  f"MSD@49ps {g[-1]:.2f} A^2)")

    if not cols:
        raise SystemExit("⛔ 수확한 곡선이 없다")

    base_cols, base_rows = [], None
    if a.merge and os.path.isfile(a.merge):
        L = [l for l in open(a.merge, encoding="utf-8-sig").read().splitlines()
             if l.strip() and not l.lstrip().startswith(('#', '"#'))]
        r = list(csv.reader(L))
        base_cols = r[0][1:]
        base_rows = np.array([[float(x) for x in row[1:]] for row in r[1:]])
        if len(base_rows) != len(GRID):
            raise SystemExit(f"⛔ merge 대상 격자가 다르다 ({len(base_rows)} vs {len(GRID)})")
        print(f"  + 기존 {len(base_cols)}열 병합: {a.merge}")

    with open(a.out, "w", newline="", encoding="utf-8-sig") as f:
        f.write('"# Li MSD (A^2) vs time, MLIP-MD. Common 0-49 ps @ 1 ps grid '
                '(linear interpolation, display only)."\n')
        f.write('"# D = slope/6 over 2-50 ps. Raw single-seed MSD = ILLUSTRATIVE HIERARCHY ONLY. '
                'Quantitative D/Ea/sigma: the multiseed *_md_arrhenius.json files."\n')
        for m in meta:
            f.write(f'"# {m}"\n')
        w = csv.writer(f)
        w.writerow(["t_ps"] + base_cols + list(cols))
        for i, t in enumerate(GRID):
            row = [f"{t:.1f}"]
            if base_rows is not None:
                row += [f"{v:.3f}" for v in base_rows[i]]
            row += ["" if np.isnan(cols[c][i]) else f"{cols[c][i]:.3f}" for c in cols]
            w.writerow(row)
    print(f"\n→ {a.out}  ({len(base_cols) + len(cols)} 계열 × {len(GRID)} 점)")


if __name__ == "__main__":
    main()
