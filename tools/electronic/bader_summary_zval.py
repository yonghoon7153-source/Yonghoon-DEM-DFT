#!/usr/bin/env python3
"""bader_summary_zval.py — ACF.dat → 원소별 net charge (ZVAL 규약).

왜 독립 스크립트인가
  run_lpsocl_bader_gabia.sh 안의 요약 블록을 `sed` 로 잘라내 재실행하려다 실패했다
  (heredoc 이라 argv 가 안 넘어가고 `ts` 함수도 없어서). 요약만 다시 돌 일이 많으므로
  (ZVAL 표 정정, pseudo 교체 등) **따로 뗀다.** 재계산 없이 ACF.dat 만 다시 읽는다.

⚠⚠ **net = ZVAL − N_bader 다. Z 가 아니다.**
  QE 의 plot_num=17 은 all-electron **valence** charge density(PAW 증강 복원)라
  basin 에 들어오는 건 ZVAL 이다. 이걸 Z 로 빼서 Cl +9.086 · S +8.227 · P +14.524
  같은 값이 나온 사고가 있었다(2026-07-30). Li 만 우연히 안 틀렸다 —
  Li.pbe-sl-kjpaw 는 semicore 포함이라 ZVAL=3=Z.

  python3 tools/electronic/bader_summary_zval.py \
      --acf /data/work/runs/lpsocl_bader/ACF.dat \
      --struct db/structures/lpsocl_relaxV0.xyz \
      --out /data/work/runs/lpsocl_bader/lpsocl_bader_summary.json
"""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

# kjpaw_psl 세트의 가전자 수 — pseudo 를 바꾸면 여기도 바꿔야 한다.
ZVAL = {"Li": 3, "P": 5, "S": 6, "Cl": 7, "O": 6, "B": 3}
REF = {"b2o3":    {"Li": 0.881, "P": 4.691, "S": -1.80, "Cl": -0.914},
       "LPSCl16": {"Li": 0.883, "P": 4.340, "S": -1.736, "Cl": -0.918}}


def read_symbols(path):
    L = Path(path).read_text().splitlines()
    if path.endswith(".xyz"):
        nat = int(L[0].split()[0])
        return [ln.split()[0] for ln in L[2:2 + nat]]
    sp, cnt = L[5].split(), [int(x) for x in L[6].split()]     # POSCAR
    return [s for s, n in zip(sp, cnt) for _ in range(n)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--acf", required=True)
    ap.add_argument("--struct", required=True)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    sym = read_symbols(a.struct)
    rows = [l.split() for l in open(a.acf) if re.match(r"^\s*\d+\s", l)]
    if len(rows) != len(sym):
        raise SystemExit(f"원자 수 불일치: ACF {len(rows)} vs 구조 {len(sym)} — "
                         "같은 구조로 돈 게 맞는지 확인")
    miss = sorted({s for s in sym if s not in ZVAL})
    if miss:
        raise SystemExit(f"ZVAL 미등록 원소: {miss} — 이 스크립트의 ZVAL 표에 추가할 것")

    per = defaultdict(list)
    for s, r in zip(sym, rows):
        per[s].append(ZVAL[s] - float(r[4]))          # net = ZVAL - N_bader

    res = {"method": ("AE **valence** density plot_num=17, PAW kjpaw_psl. "
                      "net = ZVAL - N_bader (NOT Z - N_bader)."),
           "zval_used": {k: ZVAL[k] for k in sorted(per)},
           "per_species": {k: {"n": len(v), "mean": round(sum(v) / len(v), 3),
                               "min": round(min(v), 3), "max": round(max(v), 3)}
                           for k, v in sorted(per.items())}}
    print("원소별 net charge (ZVAL − N_bader):")
    for k, v in res["per_species"].items():
        print(f"  {k:3s} n={v['n']:3d}  {v['mean']:+.3f}  [{v['min']:+.3f}, {v['max']:+.3f}]")
    print("\n같은 방법(AE plot_num=17 + kjpaw) 비교 상대:")
    for name, d in REF.items():
        print(f"  {name:9s} " + " · ".join(f"{k} {v:+.3f}" for k, v in d.items()))
    bad = [k for k, v in res["per_species"].items() if abs(v["mean"]) > 8]
    if bad:
        print(f"\n⛔ {bad} 의 절대값이 8 e 를 넘는다 — ZVAL 표가 틀렸을 가능성이 크다.")
    if a.out:
        Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n")
        print(f"\n→ {a.out}")


if __name__ == "__main__":
    main()
