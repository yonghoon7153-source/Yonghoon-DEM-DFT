#!/usr/bin/env python3
"""extract_gap.py — nscf(fixed occupations) 출력에서 **VBM/CBM 고유값**으로 갭을 낸다.

⚠⚠ 이것이 갭의 **정본**이다. DOS 문턱으로 읽으면 Gaussian 퍼짐 때문에 ~0.3 eV
  과소평가된다 (CLAUDE.md 규율). DOS/PDOS 는 그림과 성분 분해 전용이다.

  VBM = max over k of  E(N/2 번째 밴드)
  CBM = min over k of  E(N/2+1 번째 밴드)
  gap = CBM − VBM   (≤ 0 이면 금속/반금속)

  python3 extract_gap.py --nscf 03_nscf_gap.out --tag li2o --json gap.json
"""
import argparse, json, re, sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nscf", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--json", required=True)
    a = ap.parse_args()
    t = open(a.nscf, errors="ignore").read()

    m = re.search(r"number of electrons\s*=\s*([\d.]+)", t)
    if not m:
        sys.exit("⛔ number of electrons 를 못 읽었다")
    nelec = float(m.group(1))
    ms = re.search(r"number of Kohn-Sham states\s*=\s*(\d+)", t)
    nbnd = int(ms.group(1)) if ms else None
    spin = "SPIN UP" in t
    nocc = int(round(nelec / (1 if spin else 2)))

    # k 점별 밴드 블록
    blocks = re.findall(r"bands \(ev\):\s*\n\s*\n((?:\s*[-\d.]+[^\n]*\n)+)", t)
    if not blocks:
        sys.exit("⛔ 밴드 블록을 못 찾았다 (verbosity 가 낮으면 안 찍힌다)")
    vbm, cbm = -1e9, 1e9
    for b in blocks:
        e = [float(x) for x in b.split()]
        if len(e) < nocc + 1:
            continue
        vbm = max(vbm, e[nocc - 1])
        cbm = min(cbm, e[nocc])
    gap = cbm - vbm
    verdict = ("금속/반금속 (겹침)" if gap <= 0.02 else
               "좁은 갭" if gap < 1.0 else "절연체")
    print(f"  VBM {vbm:.3f} · CBM {cbm:.3f} · **gap {gap:.3f} eV** ({verdict})")
    print(f"    (전자 {nelec:.0f} · 점유 밴드 {nocc} · nbnd {nbnd} · k점 {len(blocks)}"
          + (" · spin-polarized" if spin else "") + ")")
    if nbnd and nocc >= nbnd:
        print("    ⚠ nbnd 가 점유 밴드 수와 같거나 작다 — CBM 을 못 봤다. nbnd 를 늘릴 것.")
    json.dump({"tag": a.tag, "vbm": vbm, "cbm": cbm, "gap": gap, "verdict": verdict,
               "nelec": nelec, "n_occ_bands": nocc, "nbnd": nbnd, "nk": len(blocks),
               "spin_polarized": spin,
               "method": "fixed-occupation nscf eigenvalues (NOT DOS threshold)",
               "warning": "PBE gap; systematically 30-50% underestimated for wide-gap insulators"},
              open(a.json, "w"), ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
