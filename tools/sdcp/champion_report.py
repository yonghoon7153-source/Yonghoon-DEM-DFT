#!/usr/bin/env python3
"""champion_report.py — 재스캔 챔피언이 **화학흡착인가, Li 추출인가**를 한 번에 본다.

왜 필요한가 (2026-08-06)
  freeze_frac 을 1.0 → 0.85 로 풀었더니 E_bind 가 −0.258 → −1.267 eV 로 5배 깊어졌다.
  ⚠ 이걸 곧바로 "화학흡착" 이라고 읽으면 **비약**이다. 0.6(2개 층 자유)에서 똑같이 깊어졌을 때
  실제 정체는 **표면 Li⁺ 추출**이었다. 깊어진 이유는 셋 중 하나다:
    (a) 진짜 화학흡착 — 표면이 분자를 향해 이완하며 결합 형성
    (b) 반응 — 분자가 표면 원자를 뽑아냈다 (얼렸을 땐 막혀 있던 경로가 열린 것)
    (c) 슬랩 기준 이완 미수렴 → E_bind 가 통째로 오염

⚠ 기준선 문제와 그 해법
  스캔 스크립트는 **이완된 맨 슬랩을 디스크에 안 쓴다.** 그래서 원본(DFT) 슬랩과 비교하면
  'UMA 가 자기 최소로 간 몫'과 '분자가 끌어당긴 몫'이 섞인다.
  → 해법: **분자가 멀리 있는 자세들의 슬랩부를 맨 표면 이완의 대용 기준으로 쓴다.**
    분자가 5 Å 밖이면 표면은 사실상 맨 표면이다. 이 기준 대비 초과분만이 분자의 몫이다.

  python3 tools/sdcp/champion_report.py \\
      --scan /data/work/runs/sdcp_v2/phaseA_top1free \\
      --slab db/structures/linio2_104_sym_1x4L4_relaxed.vasp
"""
import argparse
import csv
import glob
import os
import sys
from collections import defaultdict

import numpy as np
from ase.io import read

LI_LO, LI_HI = 1.90, 2.20          # Li⁺–O 배위 기준
FAR = 4.5                          # 이보다 멀면 '맨 표면' 대용으로 쓴다
EJECT = 0.50                       # 이 이상 움직인 슬랩 원자는 이탈 후보
CLEAR = 1.50                       # 이 이상이면 **명백한 추출** (층간격 2.09 Å 의 ~7할)
                                   #   0.50–1.50 은 애매해서 비교쌍에 안 쓴다


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", required=True)
    ap.add_argument("--slab", required=True, help="원본(DFT) 슬랩 — 셀·기준 좌표")
    ap.add_argument("--nslab", type=int, default=192)
    ap.add_argument("--top", type=int, default=4, help="종별 상위 몇 개를 자세히 볼까")
    a = ap.parse_args()

    ref = read(a.slab)
    cell, rpos, rsym = ref.cell, ref.positions.copy(), ref.get_chemical_symbols()

    eb = {}
    cpath = os.path.join(a.scan, "phaseA_v7c_results.csv")
    if os.path.isfile(cpath):
        with open(cpath) as f:
            for row in csv.DictReader(l for l in f if not l.startswith("#")):
                try:
                    if int(row["converged"]):
                        eb[row["label"]] = float(row["E_bind_eV"])
                except (ValueError, KeyError, TypeError):
                    pass
    if not eb:
        sys.exit(f"⛔ {cpath} 를 못 읽었다")

    # ── 전 자세 1회 통과: 접촉거리와 슬랩 좌표를 모은다 ──────────────────────
    poses = {}
    for fp in sorted(glob.glob(os.path.join(a.scan, "complex_*.xyz"))):
        lab = os.path.basename(fp)[len("complex_"):-len(".xyz")]
        if lab not in eb:
            continue
        at = read(fp)
        if len(at) <= a.nslab:
            continue
        at.set_cell(cell); at.set_pbc(True)
        sym = at.get_chemical_symbols()
        mol = list(range(a.nslab, len(at)))
        dmin = min(float(at.get_distances(m, list(range(a.nslab)), mic=True).min())
                   for m in mol)
        poses[lab] = {"at": at, "sym": sym, "mol": mol, "dmin": dmin,
                      "slab": at.positions[:a.nslab].copy(), "E": eb[lab]}
    if not poses:
        sys.exit(f"⛔ {a.scan} 에서 읽을 자세가 없다")

    # ── 기준선: 분자가 먼 자세들의 슬랩 평균 = '맨 표면 이완' 대용 ──────────
    ref_relaxed = os.path.join(a.scan, "slab_ref_relaxed.xyz")
    far = [p for p in poses.values() if p["dmin"] > FAR]
    if os.path.isfile(ref_relaxed):
        base = read(ref_relaxed).positions[:a.nslab].copy()
        src = f"{os.path.basename(ref_relaxed)} — 같은 구속으로 이완한 맨 슬랩 (정본)"
    elif far:
        base = np.mean([p["slab"] for p in far], axis=0)
        src = f"분자가 {FAR} Å 밖인 자세 {len(far)}개의 평균"
    else:
        # ⚠ 원본 DFT 슬랩을 기준으로 쓰면 UMA 자체 이완(실측 ~0.17 Å)이 섞인다.
        #   추출은 소수 자세에서만 일어나므로 **전 자세의 원자별 중앙값**이 훨씬 나은
        #   '맨 표면' 추정치다 — 중앙값은 소수의 큰 이탈에 안 흔들린다.
        base = np.median(np.stack([p["slab"] for p in poses.values()]), axis=0)
        src = (f"⚠ 이완된 맨 슬랩 파일도, 먼 자세도 없다 → **전 {len(poses)}개 자세의 "
               f"원자별 중앙값**으로 대신함 (추출은 소수라 중앙값이 맨 표면에 가깝다)")
    base_shift = float(np.linalg.norm(base - rpos[:a.nslab], axis=1).max())

    print(f"스캔 {a.scan}   자세 {len(poses)}개")
    print(f"기준선 = {src}")
    print(f"  · 그 기준선이 원본(DFT) 대비 이미 {base_shift:.3f} Å 움직여 있다"
          f" — 이건 **UMA 자체 이완**이지 분자의 몫이 아니다")
    print("─" * 76)

    by_tag = defaultdict(list)
    for lab, p in poses.items():
        by_tag[lab.split("_")[0]].append((p["E"], lab))

    for tag in sorted(by_tag):
        print(f"\n═══ {tag} — 상위 {a.top} ═══")
        for E, lab in sorted(by_tag[tag])[:a.top]:
            p = poses[lab]
            at, sym, mol = p["at"], p["sym"], p["mol"]
            d = np.linalg.norm(p["slab"] - base, axis=1)     # 분자가 끌어당긴 몫
            d_raw = np.linalg.norm(p["slab"] - rpos[:a.nslab], axis=1)
            moved = np.argsort(-d)[:3]
            eject = [i for i in range(a.nslab) if d[i] > EJECT]

            li = [i for i in range(a.nslab) if sym[i] == "Li"]
            mo = [i for i in mol if sym[i] == "O"]
            d_lio = (min(float(at.get_distances(m, li, mic=True).min()) for m in mo)
                     if mo and li else float("nan"))

            print(f"\n  {lab}   E_bind {E:+.3f} eV")
            print(f"    분자–표면 최단 {p['dmin']:5.2f} Å · 분자 O ↔ 표면 Li {d_lio:5.2f} Å "
                  + ("★ 배위" if d_lio <= LI_HI else
                     "· 접근" if d_lio < 2.5 else "  멀다"))
            print(f"    슬랩 변위: 기준선 대비 max {d.max():.3f} Å "
                  f"(원본 대비 {d_raw.max():.3f} — 그중 {base_shift:.3f} 는 UMA 몫)")
            print("      가장 많이 움직인 3원자: " + " · ".join(
                f"{sym[i]}{i} {d[i]:.2f} Å" for i in moved))

            if eject:
                print(f"    ⛔⛔ **{len(eject)}개 슬랩 원자가 {EJECT} Å 넘게 움직였다 — "
                      f"흡착이 아니라 반응(추출) 의심**")
                for i in eject[:5]:
                    dm = float(at.get_distances(i, mol, mic=True).min())
                    j = mol[int(np.argmin(at.get_distances(i, mol, mic=True)))]
                    print(f"       {sym[i]}{i} 가 {d[i]:.2f} Å 이동 · "
                          f"분자 {sym[j]}{j} 까지 {dm:.2f} Å"
                          + ("  ← 분자에 배위됐다" if dm < 2.3 else ""))
                print("       ⚠ UMA 는 전하분리를 판정할 수 없다 — 이 경로는 DFT 로만 결론 낸다")
            elif d.max() < 0.05:
                print("    ⚠ 표면이 기준선에서 사실상 안 움직였다 — **분자가 표면을 못 끌어당긴다**")
                print("       그러면 E_bind 가 깊어진 것은 표면 응답이 아니라 다른 이유다")
                print("       (맨 표면 이완이 슬랩 기준 에너지를 낮춘 몫일 수 있다 — 아래 ⚠ 참고)")
            else:
                print(f"    ✓ 표면이 분자 쪽으로 {d.max():.3f} Å 응답했다 (이탈은 없다)")

    # ── ★ DFT 비교쌍 — ΔE_extract 를 오염 없이 재려면 **같은 스캔**에서 둘을 뽑아야 한다 ──
    print("\n" + "═" * 76)
    print("★ DFT+U 비교쌍 제안 — ΔE_extract = E(추출) − E(물리흡착)")
    print("  ⚠ 두 기하를 **다른 스캔**에서 뽑으면 안 된다. phaseA(표면 DFT 고정)와")
    print("     phaseA_top1free(표면 UMA 이완)를 섞으면 ΔE 에 'UMA 기하를 DFT 로 채점한 벌점'이")
    print("     추출 쪽에만 붙는다. 같은 스캔 안에서 뽑아야 그 항이 상쇄된다.")
    print(f"  판정: 슬랩 최대변위 < {EJECT} Å = 물리흡착 · > {CLEAR} Å = 명백한 추출"
          f" (그 사이는 애매해서 안 쓴다)")

    disp = {}
    for lab, p in poses.items():
        disp[lab] = float(np.linalg.norm(p["slab"] - base, axis=1).max())

    for tag in sorted(by_tag):
        labs = [lab for _, lab in by_tag[tag]]
        ds = np.array([disp[l] for l in labs])
        print(f"\n  ── {tag} (자세 {len(labs)}) — 슬랩 최대변위 분포")
        print(f"     중앙값 {np.median(ds):.2f} · 90%p {np.percentile(ds,90):.2f} · "
              f"최대 {ds.max():.2f} Å · "
              f"물리흡착권(<{EJECT}) {int((ds<EJECT).sum())}개 · "
              f"명백추출(>{CLEAR}) {int((ds>CLEAR).sum())}개")
        phys = sorted((poses[l]["E"], l) for l in labs if disp[l] < EJECT)
        extr = sorted((poses[l]["E"], l) for l in labs if disp[l] > CLEAR)
        if phys:
            print(f"     물리흡착 기준: {phys[0][1]}  E {phys[0][0]:+.3f} · 변위 {disp[phys[0][1]]:.2f} Å")
        else:
            print(f"     ⚠ 변위 {EJECT} Å 미만인 자세가 없다 — 이 종은 비교쌍을 못 만든다")
        if extr:
            print(f"     추출   기준: {extr[0][1]}  E {extr[0][0]:+.3f} · 변위 {disp[extr[0][1]]:.2f} Å")
        else:
            print(f"     ⚠ 변위 {CLEAR} Å 넘는 자세가 **하나도 없다**")
            print(f"        → 이 종은 UMA 가 추출 경로를 아예 못 찾았다는 뜻이고, 그 자체가 결과다")
        if phys and extr:
            print(f"     ΔE_extract(UMA) = {extr[0][0] - phys[0][0]:+.3f} eV "
                  f"← DFT+U 가 이 부호를 유지하는지가 판정")

    print("\n" + "─" * 76)
    print("⚠ 읽는 법")
    print("  · '기준선 대비' 만이 분자의 몫이다. '원본 대비' 에는 UMA 자체 이완이 섞여 있다.")
    print("  · 이탈(⛔)이 뜨면 그 자세의 E_bind 는 흡착에너지가 아니다 — 반응에너지다.")
    print("  · 이탈도 없고 표면 응답도 없는데 E_bind 만 깊어졌다면, 슬랩 기준 에너지가")
    print("    바뀐 것(맨 표면이 이완해 E_slab 이 내려감)이 원인일 수 있다 —")
    print("    그건 흡착이 강해진 게 아니라 **기준점이 움직인 것**이다. 두 스캔의 E_bind 를")
    print("    직접 비교하면 안 되는 이유다(각 스캔은 자기 E_slab 을 쓴다).")
    print("  · UMA 절대값 인용 금지. 순위·차이만.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
