#!/usr/bin/env python3
"""hydrolysis_speciation.py — 가수분해 MD 스냅샷의 화학종을 RDF-정의 컷오프로 재집계.

`tools/oxidation/analyze_interface_decomp.py` 의 형제 도구다. 그쪽은 **궤적**에서
**평균 배위수의 시간변화**를 보고(SE|Li 계면 환원), 이쪽은 **최종 스냅샷 한 장**에서
**배위수 분포와 분자종**을 센다(SE|H2O 계면 가수분해). 컷오프를 손으로 박지 않고
**RDF 첫 최소**에서 뽑는다는 점이 결정적으로 다르다 — 그래서 새 파일이다.

무엇을 내나
  1) 조성 (원소별 개수, H:O 비)
  2) 원소쌍 RDF g(r) + **첫 최소 자동 검출** + **골짜기 폭에 대한 배위수 민감도**
     (골짜기 안에서 컷오프를 어디로 잡든 배위수가 같으면 컷오프는 자유변수가 아니다)
  3) 중심원자별 배위수 **분포** (P/Sn 의 CN(S), CN(O) 결합분포 -> PS4 / PS(4-x)Ox / SnS4 ...)
  4) 표면법선축 **자동 판별** + 그 축 방향 z-binned 밀도 (H 를 H-O / H-S 로 쪼개서)
  5) 분자종: 유리 S(골격에 안 붙은 S)의 H 개수 -> S(2-), SH(-), **H2S**;
     O 의 H 개수 -> O(2-)/OH(-)/H2O/H3O(+); H2 분자; S-S 이황화
  6) H 원자별 분류 (컷오프 기반 + **컷오프 없는 최근접 원소** 교차확인)
  7) `--frames-report`: extxyz 궤적/데이터셋 진단 — 프레임 수·조성/셀 고정 여부·
     **중복 프레임**·`forces` 열이 `DFT_forces` 의 복사본인지(=MLP 힘이 실제로 없는지)·
     (`--fidelity-csv` 를 주면) **프레임 -> Step 대응표와 파일순서=시간순서 여부**

이 도구가 **못 하는 것** (읽는 사람이 반드시 알아야 함)
  · **동역학을 못 본다.** 스냅샷 한 장이다. "몇 개가 생겼나"는 세지만 "언제·어떤 경로로"는
    말하지 못한다. 반응속도·활성화에너지는 이 도구 밖이다.
  · **오차막대가 없다.** 단일 구조 단일 궤적이면 통계오차를 낼 방법이 없다. 개수의 차이가
    유의한지 판단하지 않는다 — 개수만 낸다.
  · **전하를 모른다.** OH(-)/H3O(+)/S(2-) 라는 이름은 **H 개수로 붙인 이름표**이지 전자구조
    계산이 아니다. Bader/ICOHP 가 아니다.
  · **결합을 거리로만 판정한다.** 거리컷은 공유결합과 매우 짧은 수소결합을 완벽히 가르지
    못한다. 그래서 골짜기 폭 민감도와 최근접-원소 교차확인을 **같이** 낸다.
  · **초기 구조를 모르면 '변화량'을 못 낸다.** 최종 스냅샷만 주면 최종 개수만 나온다.
    "반응으로 생겼다"는 판정은 이상적 조성 대비 기대값(--ideal-free-S 등)이 있어야 한다.
  · **주기경계에서 슬랩이 잘려 있으면** z-프로파일 원점을 골격 빈틈 중앙으로 옮긴다.
    슬랩이 두 조각 이상으로 쪼개진 계는 다루지 못한다 (경고만 낸다).
  · 셀이 **직교가 아니면** z-프로파일은 축 성분(cartesian z)이 아니라 분율좌표 축을 쓴다 —
    비직교 셀에서는 깊이가 왜곡된다. 경고를 낸다.

사용
    python3 tools/oxidation/hydrolysis_speciation.py \
        --struct LPSC-H2O=a.cif --struct LPSC-ion=b.cif --struct LPSnSC-ion=c.cif \
        --outdir db/external/kim2026_argyrodite_hydrolysis
    python3 tools/oxidation/hydrolysis_speciation.py --frames-report traj.xyz
    python3 tools/oxidation/hydrolysis_speciation.py --selftest
"""
import argparse
import csv
import json
import pathlib
import sys
from collections import Counter

import numpy as np

# ── 우리가 재는 원소쌍 ───────────────────────────────────────────────────────
#   (A, B, rmax_for_first_min) — rmax 는 **첫 최소를 찾을 범위**이지 컷오프가 아니다.
#   rmax 는 "다음 껍질(수소결합/2차이웃)이 시작되기 전"으로 잡는다. 그러지 않으면
#   argmax 가 공유결합 봉우리가 아니라 더 큰 다음 껍질을 집는다 (H-S 에서 실제로 그랬다).
PAIRS = [
    ("P", "S", 3.5), ("P", "O", 3.0),
    ("Sn", "S", 3.5), ("Sn", "O", 3.0),
    ("H", "O", 1.6), ("H", "S", 1.9), ("H", "Cl", 2.0),
    ("O", "O", 2.4), ("Li", "S", 4.2), ("Li", "O", 3.6),
]

# ⚠ RDF 자동검출을 **일부러 쓰지 않는** 쌍 — 왜 못 쓰는지까지 적는다.
#   RDF 는 다수 화학종이 지배한다. 아래 둘은 우리가 세려는 것이 **희소종**이라
#   g(r) 에서 봉우리로 안 뜬다. 고정 컷오프를 쓰고 CSV 에 fixed_documented 로 찍는다.
FIXED_CUT = {
    # H2 분자 (d(H-H)=0.741 Å). H-H RDF 는 **물 분자 내부 H...H (1.5 Å)** 가 지배해서
    # 자동검출이 그 봉우리를 집는다 -> 물 전체가 'H2' 로 오분류된다 (실제 겪은 버그).
    ("H", "H"): (0.90, "H2 bond 0.741 A; H-H RDF is dominated by intramolecular H...H of H2O (1.5 A)"),
    # 이황화 S-S (2.0-2.1 Å). S-S RDF 는 **PS4 사면체 내부 S...S (3.35 Å)** 가 지배한다.
    ("S", "S"): (2.40, "disulfide S-S 2.0-2.1 A; S-S RDF is dominated by intra-PS4 S...S (3.35 A)"),
}

# 컷오프 자동검출이 실패했을 때만 쓰는 대비값 (Å). 쓰이면 CSV 의 `source` 열에 fallback 으로 찍힌다.
FALLBACK_CUT = {
    ("P", "S"): 2.60, ("P", "O"): 2.10, ("Sn", "S"): 3.00, ("Sn", "O"): 2.50,
    ("H", "O"): 1.25, ("H", "S"): 1.70, ("H", "Cl"): 1.70, ("H", "H"): 0.90,
    ("S", "S"): 2.40, ("O", "O"): 1.80, ("Li", "S"): 3.10, ("Li", "O"): 2.60,
}

FRAMEWORK = ("Li", "P", "S", "Cl", "Sn")   # 고체 골격 쪽
FLUID = ("H", "O")                          # 물 쪽


def pair_key(a, b):
    return (a, b) if (a, b) in FALLBACK_CUT else (b, a)


# ══ RDF ═════════════════════════════════════════════════════════════════════
def rdf(atoms, A, B, rmax=6.0, dr=0.02, nl=None):
    """부분 RDF g_AB(r). nl 은 (i, j, d) 미리 계산한 이웃목록 (rmax 이상이어야 함)."""
    sym = np.array(atoms.get_chemical_symbols())
    nA, nB = int((sym == A).sum()), int((sym == B).sum())
    bins = np.arange(0.0, rmax + dr, dr)
    r = 0.5 * (bins[1:] + bins[:-1])
    if nA == 0 or nB == 0:
        return r, np.zeros_like(r), np.zeros_like(r, dtype=int)
    i, j, d = nl
    m = (sym[i] == A) & (sym[j] == B) & (d <= rmax)
    h, _ = np.histogram(d[m], bins=bins)
    V = atoms.get_volume()
    shell = 4.0 * np.pi * r ** 2 * dr
    # A==B 이면 i!=j 쌍이 양방향으로 세어지므로 정규화 분모도 그대로 nA*(nB/V) 로 맞다
    denom = nA * (nB / V) * shell
    g = np.divide(h, denom, out=np.zeros_like(r), where=denom > 0)
    return r, g, h


def smooth(y, w=5):
    if w <= 1 or len(y) < w:
        return y.copy()
    k = np.ones(w) / w
    return np.convolve(y, k, mode="same")


def first_minimum(r, g, h, rmax_search, smooth_w=5, min_contrast=0.20,
                  min_gap=0.20, valley_frac=0.5):
    """첫 피크 뒤의 **첫 최소(=결합 컷오프)** 를 찾는다. 눈대중 없음.

    ① 첫 피크: r <= rmax_search 안에서 **평활화한 g** 의 최대.
       (rmax_search 는 다음 껍질 전에서 끊는다 — PAIRS 의 셋째 값. raw 개수가 아니라
        g 로 찾는 이유: 4*pi*r^2 정규화 없이는 먼 껍질이 항상 더 커 보인다.)
    ② **대비 검사**: 피크 뒤 최소가 g_min <= min_contrast*g_peak 이어야 봉우리로 인정.
       없으면 균일기체(구조 없음)에서도 잡음 극값을 컷오프라고 우긴다 (selftest 음성 경로).
       절대 크기가 아니라 대비로 보는 이유: H-S 처럼 희소한 결합은 g_peak<1 이어도 진짜다.
    ③ **비어 있는 골짜기(1순위)**: 피크 뒤에서 **원시 개수 h 가 정확히 0 인 연속 구간**이
       min_gap(기본 0.20 Å) 이상이면 그 구간이 골짜기다. 컷오프 = **구간 시작**.
       이때 배위수는 구간 어디를 잘라도 **정의상 같다** (사이에 원자쌍이 아예 없으니까).
       -> method="empty_valley". P-S, H-S, Sn-S 가 여기 해당한다.
    ④ 그런 구간이 없으면(H-O 처럼 수소결합 껍질이 이어 붙는 경우) **평활 g 의 극소점**을
       컷오프로 쓰고, 골짜기 = g <= (1+valley_frac)*g_min 인 연속 구간.
       -> method="smoothed_argmin". 이건 **컷오프 민감**하다 — cutoff_sensitivity.csv 를 봐야 한다.
    """
    sel = r <= rmax_search
    rr, gg = r[sel], smooth(g[sel], smooth_w)
    if gg.size < 5 or gg.max() <= 0:
        return {"ok": False, "reason": "no signal in search range"}
    ip = int(np.argmax(gg))
    if ip >= len(gg) - 3:
        return {"ok": False, "reason": "peak at edge of search range"}
    tail = gg[ip + 1:]
    gmin = float(tail.min())
    if gmin > min_contrast * gg[ip]:
        return {"ok": False,
                "reason": f"no peak/valley contrast: g_min/g_peak={gmin / gg[ip]:.2f} "
                          f"> {min_contrast:.2f}"}
    base = {"ok": True, "r_peak": float(rr[ip]), "g_peak": float(gg[ip]), "g_min": gmin}

    # ③ 빈 골짜기 — 원시 개수 0 인 연속 구간 (탐색범위 밖까지 이어지면 그대로 따라간다)
    dr = float(r[1] - r[0])
    need = max(int(round(min_gap / dr)), 2)
    k = ip + 1
    n = len(h)
    while k < n:
        if h[k] == 0:
            e = k
            while e + 1 < n and h[e + 1] == 0:
                e += 1
            if (e - k + 1) >= need:
                return {**base, "method": "empty_valley",
                        "r_min": float(r[k]), "valley_lo": float(r[k]),
                        "valley_hi": float(r[e]), "valley_width": float(r[e] - r[k])}
            k = e + 1
        else:
            k += 1

    # ④ 평활 극소점
    imin = ip + 1 + int(np.argmin(tail))
    thr = (1.0 + valley_frac) * gmin
    lo = imin
    while lo - 1 > ip and gg[lo - 1] <= thr:
        lo -= 1
    hi = imin
    while hi + 1 < len(gg) and gg[hi + 1] <= thr:
        hi += 1
    return {**base, "method": "smoothed_argmin", "r_min": float(rr[imin]),
            "valley_lo": float(rr[lo]), "valley_hi": float(rr[hi]),
            "valley_width": float(rr[hi] - rr[lo])}


# ══ 배위 ════════════════════════════════════════════════════════════════════
def coord_counts(sym, nl, A, B, cut):
    """A 원자마다 cut 안의 B 이웃 수 (전체 길이 배열, A 아닌 곳은 0)."""
    i, j, d = nl
    m = (sym[i] == A) & (sym[j] == B) & (d < cut)
    out = np.zeros(len(sym), dtype=int)
    np.add.at(out, i[m], 1)
    return out


def nearest_from_nl(sym, nl, centers, targets):
    """centers 각각에 대해 targets 중 최근접 원소와 거리 (컷오프 없음, 이웃목록 반경 안).

    이웃목록 반경 밖이면 (None, inf). 반경을 충분히 크게 잡고 부른다.
    """
    i, j, d = nl
    tmask = np.isin(sym[j], list(targets))
    best = {c: (None, np.inf) for c in centers}
    cset = set(int(c) for c in centers)
    for a, b, dd in zip(i[tmask], j[tmask], d[tmask]):
        a = int(a)
        if a in cset and dd < best[a][1]:
            best[a] = (str(sym[b]), float(dd))
    return best


# ══ 표면 법선축 판별 ════════════════════════════════════════════════════════
def normal_axis(atoms, bin_w=1.0):
    """골격이 셀을 다 채우지 **못하는** 축이 법선축이다. 세 축 진단을 모두 낸다.

    지표 두 개를 같이 본다 (하나만 보고 정하지 않는다):
      occ_fw  : 골격 원자가 하나라도 있는 1 Å 빈의 비율 — 법선축에서만 1 보다 작다
      overlap : 골격/유체 z-분포의 겹침계수 sum(min(p_fw, p_fluid)) — 법선축에서 작다
    """
    sym = np.array(atoms.get_chemical_symbols())
    pos = atoms.get_positions()
    L = atoms.cell.lengths()
    fw = np.isin(sym, FRAMEWORK)
    fl = np.isin(sym, FLUID)
    diag = []
    for ax in range(3):
        nb = max(int(round(L[ax] / bin_w)), 4)
        hf, _ = np.histogram(pos[fw, ax], bins=nb, range=(0, L[ax]))
        hl, _ = np.histogram(pos[fl, ax], bins=nb, range=(0, L[ax]))
        occ = float((hf > 0).mean())
        if hf.sum() and hl.sum():
            ov = float(np.minimum(hf / hf.sum(), hl / hl.sum()).sum())
        else:
            ov = 1.0
        diag.append({"axis": ax, "L": float(L[ax]), "occ_framework": occ, "overlap": ov})
    # occ 가 가장 작은 축 — 동률이면 overlap 이 가장 작은 축
    best = min(diag, key=lambda d: (round(d["occ_framework"], 3), d["overlap"]))
    return best["axis"], diag


def cation_layers(atoms, axis, cations=("P", "Sn"), gap=2.0):
    """법선축을 따라 **사면체 중심 양이온 층**을 끊고 층별 조성을 낸다.

    왜 필요한가 — 도펀트가 **무작위 고용체**인지 **층으로 정렬**돼 있는지에 따라
    "도펀트가 표면을 보호한다" 는 해석이 완전히 달라진다. 층 종단이 다르면
    두 표면이 화학적으로 다른 계다. 가정하지 말고 세어 본다.

    ⛔ 못 하는 것: 층 안의 **면내 배열**(클러스터링 vs 무작위)은 안 본다. 축 방향만이다.
    """
    sym = np.array(atoms.get_chemical_symbols())
    z = atoms.get_positions()[:, axis]
    idx = np.where(np.isin(sym, list(cations)))[0]
    if idx.size == 0:
        return []
    order = idx[np.argsort(z[idx])]
    layers, cur = [], [order[0]]
    for k in order[1:]:
        if z[k] - z[cur[-1]] > gap:
            layers.append(cur); cur = []
        cur.append(k)
    layers.append(cur)
    out = []
    for n, lay in enumerate(layers):
        c = Counter(sym[lay].tolist())
        tot = sum(c.values())
        out.append({"layer": n, "z_mean": float(np.mean(z[lay])), "n_total": int(tot),
                    **{f"n_{el}": int(c.get(el, 0)) for el in cations},
                    "dopant_percent": round(100.0 * sum(c.get(el, 0) for el in cations[1:]) / tot, 2)})
    return out


def slab_origin_shift(atoms, axis, bin_w=1.0, frac=0.15):
    """골격의 가장 넓은 **저밀도 구간**(=물/진공층) 중앙이 셀 경계에 오도록 원점을 옮긴다.

    ⚠ '정확히 0' 이 아니라 '플래토의 frac 미만' 으로 판정한다. 침출된 Li/S/Cl 이 물층에
    흩어져 있으면 완전히 빈 빈이 거의 없어서 0-런 규칙이 3 Å 짜리 가짜 빈틈을 잡는다
    (실제 겪음 — LPSC-H2O 에서 15 Å 물층을 3 Å 로 잘못 봤다).

    반환 (shift, gap_width). 옮긴 뒤 (z - shift) % L 로 쓰면 슬랩이 이어진다.
    """
    sym = np.array(atoms.get_chemical_symbols())
    pos = atoms.get_positions()
    L = float(atoms.cell.lengths()[axis])
    fw = np.isin(sym, FRAMEWORK)
    nb = max(int(round(L / bin_w)), 8)
    h, edges = np.histogram(pos[fw, axis], bins=nb, range=(0, L))
    plateau = float(np.median(h[h > 0])) if (h > 0).any() else 0.0
    empty = (h < frac * plateau).astype(int)
    if empty.sum() == 0:
        return 0.0, 0.0
    # 원형 배열에서 가장 긴 0-런
    dbl = np.concatenate([empty, empty])
    bestlen, bestst, cur, st = 0, 0, 0, 0
    for k in range(len(dbl)):
        if dbl[k]:
            if cur == 0:
                st = k
            cur += 1
            if cur > bestlen:
                bestlen, bestst = cur, st
        else:
            cur = 0
    bestlen = min(bestlen, nb)
    w = L / nb
    centre = (bestst + bestlen / 2.0) * w
    return float(centre % L), float(bestlen * w)


# ══ 한 구조 분석 ════════════════════════════════════════════════════════════
def analyse(atoms, label, dr=0.02, rmax_nl=6.5, zbin=2.0, valley_frac=0.5):
    from ase.neighborlist import neighbor_list
    sym = np.array(atoms.get_chemical_symbols())
    present = set(sym.tolist())
    i, j, d = neighbor_list("ijd", atoms, rmax_nl)
    nl = (i, j, d)
    out = {"label": label, "n_atoms": len(atoms),
           "cell_lengths": [float(x) for x in atoms.cell.lengths()],
           "cell_angles": [float(x) for x in atoms.cell.angles()],
           "volume": float(atoms.get_volume()),
           "composition": {k: int(v) for k, v in sorted(Counter(sym.tolist()).items())}}
    nH, nO = out["composition"].get("H", 0), out["composition"].get("O", 0)
    out["H_over_O"] = (nH / nO) if nO else None

    # ── RDF + 컷오프 ────────────────────────────────────────────────────────
    cuts, rdf_curves, cutrows = {}, {}, []
    todo = [(A, B, rms, "auto") for A, B, rms in PAIRS]
    todo += [(A, B, 3.5, "fixed") for (A, B) in FIXED_CUT]
    for A, B, rms, mode in todo:
        if A not in present or B not in present:
            continue
        r, g, h = rdf(atoms, A, B, rmax=6.0, dr=dr, nl=nl)
        rdf_curves[f"{A}-{B}"] = (r, g)
        key = pair_key(A, B)
        n_in_range = int(h[r <= rms].sum())
        if mode == "fixed":
            cut, why = FIXED_CUT[(A, B)]
            fm = {"ok": False, "reason": why}
            src = "fixed_documented"
            n_in_range = int(h[r <= cut].sum())
        else:
            fm = first_minimum(r, g, h, rms, valley_frac=valley_frac)
            if fm["ok"]:
                cut, src = fm["r_min"], fm["method"]
            else:
                cut, src = FALLBACK_CUT[key], "fallback"
        cuts[(A, B)] = cut
        row = {"pair": f"{A}-{B}", "source": src,
               "search_rmax": rms if mode == "auto" else "",
               "n_pairs_in_search_range": n_in_range,
               "r_peak": round(fm["r_peak"], 3) if fm["ok"] else "",
               "g_peak": round(fm["g_peak"], 2) if fm["ok"] else "",
               "g_min": round(fm["g_min"], 3) if fm["ok"] else "",
               "cutoff_used": round(cut, 3),
               "valley_lo": round(fm["valley_lo"], 3) if fm["ok"] else "",
               "valley_hi": round(fm["valley_hi"], 3) if fm["ok"] else "",
               "valley_width": round(fm["valley_width"], 3) if fm["ok"] else "",
               "note": "" if fm["ok"] else fm.get("reason", "")}
        # 골짜기 안 컷오프 민감도 — lo / mid / hi 에서 총 배위수가 같은가
        if fm["ok"] and fm["valley_width"] > 0:
            lo, hi = fm["valley_lo"], fm["valley_hi"]
            tot = [int(coord_counts(sym, nl, A, B, c).sum())
                   for c in (lo, 0.5 * (lo + hi), hi)]
            row.update({"CN_total_at_lo": tot[0], "CN_total_at_mid": tot[1],
                        "CN_total_at_hi": tot[2],
                        "cut_invariant": "YES" if len(set(tot)) == 1 else "NO"})
        else:
            row.update({"CN_total_at_lo": "", "CN_total_at_mid": "",
                        "CN_total_at_hi": "", "cut_invariant": ""})
        cutrows.append(row)
    out["cutoffs"] = {f"{a}-{b}": round(c, 3) for (a, b), c in cuts.items()}
    out["cutoff_rows"] = cutrows

    def C(A, B):
        if (A, B) in cuts:
            return coord_counts(sym, nl, A, B, cuts[(A, B)])
        if (B, A) in cuts:
            return coord_counts(sym, nl, A, B, cuts[(B, A)])
        return np.zeros(len(sym), dtype=int)

    # ── 사면체 중심 (P, Sn) 배위 분포 ───────────────────────────────────────
    tetra = {}
    for M in ("P", "Sn"):
        if M not in present:
            continue
        cS, cO = C(M, "S"), C(M, "O")
        idx = np.where(sym == M)[0]
        joint = Counter(zip(cS[idx].tolist(), cO[idx].tolist()))
        tetra[M] = {
            "n_centres": int(len(idx)),
            "CN_S_dist": {str(k): int(v) for k, v in sorted(Counter(cS[idx].tolist()).items())},
            "CN_O_dist": {str(k): int(v) for k, v in sorted(Counter(cO[idx].tolist()).items())},
            "joint_S_O": {f"{a}S{b}O": int(v) for (a, b), v in sorted(joint.items())},
            "mean_CN_S": float(cS[idx].mean()), "mean_CN_O": float(cO[idx].mean()),
            "n_intact_MX4": int(((cS[idx] + cO[idx]) == 4).sum()),
            "n_pure_MS4": int(((cS[idx] == 4) & (cO[idx] == 0)).sum()),
            "n_with_O": int((cO[idx] > 0).sum()),
        }
    out["tetrahedra"] = tetra

    # ── S 화학종 ────────────────────────────────────────────────────────────
    cSP = C("S", "P")
    cSSn = C("S", "Sn") if "Sn" in present else np.zeros(len(sym), int)
    cSH = C("S", "H")
    cSS = C("S", "S")
    S = np.where(sym == "S")[0]
    framework_S = (cSP + cSSn)[S] > 0
    nS_free = int((~framework_S).sum())
    freeS = S[~framework_S]
    fwS = S[framework_S]
    out["sulfur"] = {
        "n_S": int(len(S)),
        "n_S_in_MS4": int(framework_S.sum()),
        "n_S_free": nS_free,
        "free_S_H_dist": {str(k): int(v) for k, v in sorted(Counter(cSH[freeS].tolist()).items())},
        "n_H2S": int((cSH[freeS] == 2).sum()),
        "n_SH_minus": int((cSH[freeS] == 1).sum()),
        "n_S2minus_bare": int((cSH[freeS] == 0).sum()),
        "n_framework_S_with_H": int((cSH[fwS] > 0).sum()),
        "n_SH_bonds_total": int(cSH[S].sum()),
        "n_SS_bonds": int(cSS[S].sum() // 2),
    }

    # ── O 화학종 ────────────────────────────────────────────────────────────
    cOH = C("O", "H")
    cOP = C("O", "P") if "P" in present else np.zeros(len(sym), int)
    O = np.where(sym == "O")[0]
    out["oxygen"] = {
        "n_O": int(len(O)),
        "O_H_dist": {str(k): int(v) for k, v in sorted(Counter(cOH[O].tolist()).items())},
        "n_H2O": int((cOH[O] == 2).sum()), "n_OH": int((cOH[O] == 1).sum()),
        "n_H3O": int((cOH[O] == 3).sum()), "n_bare_O": int((cOH[O] == 0).sum()),
        "n_O_bonded_to_P": int((cOP[O] > 0).sum()),
    }
    # H-O 컷오프는 골짜기가 평평하지 않다 (수소결합 껍질이 이어짐) -> 민감도를 명시한다.
    sens = []
    for c in (1.15, 1.20, 1.25, 1.30, 1.35):
        co = coord_counts(sym, nl, "O", "H", c)
        sens.append({"cut_HO": c,
                     "n_H2O": int((co[O] == 2).sum()), "n_OH": int((co[O] == 1).sum()),
                     "n_H3O": int((co[O] == 3).sum()), "n_bare_O": int((co[O] == 0).sum()),
                     "n_OH_bonds": int(co[O].sum())})
    out["oxygen"]["cutoff_sensitivity"] = sens
    # H-S 도 같은 검사 (골짜기 안 1.45-1.85)
    sensS = []
    for c in (1.45, 1.55, 1.65, 1.75, 1.85):
        chs = coord_counts(sym, nl, "S", "H", c)
        sensS.append({"cut_HS": c, "n_SH_bonds": int(chs[S].sum()),
                      "n_S_with_H": int((chs[S] > 0).sum()),
                      "n_S_with_2H": int((chs[S] == 2).sum())})
    out["sulfur"]["cutoff_sensitivity"] = sensS

    # ── H 분류 ──────────────────────────────────────────────────────────────
    #   공유결합은 **O 와 S 만** 본다. H...Cl 은 이 계에서 수소결합 접촉이지
    #   공유결합이 아니다 (RDF 첫 봉우리가 2.1 Å) — 분류에 넣으면 오분류가 된다.
    cHO, cHS, cHH = C("H", "O"), C("H", "S"), C("H", "H")
    cHCl = C("H", "Cl") if "Cl" in present else np.zeros(len(sym), int)
    H = np.where(sym == "H")[0]
    klass = []
    for k in H:
        nO_, nS_, nH_ = cHO[k], cHS[k], cHH[k]
        if nO_ > 0 and nS_ > 0:
            klass.append("bridging_O_S")
        elif nS_ > 0:
            klass.append("H-S")
        elif nO_ > 0:
            klass.append("H-O")
        elif nH_ > 0:
            klass.append("H2")
        else:
            klass.append("unbound")
    klass = np.array(klass)
    kc = Counter(klass.tolist())
    # 컷오프 없는 교차확인 — H 마다 최근접 무거운 원소 (분류가 컷오프 인공물인지 본다)
    near = nearest_from_nl(sym, nl, H.tolist(), ("O", "S", "Cl", "P", "Sn", "Li"))
    nearc = Counter(v[0] for v in near.values())
    unb = H[klass == "unbound"]
    out["hydrogen"] = {
        "n_H": int(len(H)),
        "class_cutoff": {k: int(v) for k, v in sorted(kc.items())},
        "nearest_heavy_element": {str(k): int(v) for k, v in sorted(nearc.items(), key=lambda x: -x[1])},
        "n_H_S_bonds": int(cHS[H].sum()),
        "n_H2_molecules": int(cHH[H].sum() // 2),
        "n_H_Cl_contacts": int(cHCl[H].sum()),
        "unbound_nearest": [{"element": near[int(k)][0], "d": round(near[int(k)][1], 3)}
                            for k in unb],
    }

    # ── z 프로파일 ──────────────────────────────────────────────────────────
    ax, axdiag = normal_axis(atoms)
    ang = atoms.cell.angles()
    ortho = bool(np.allclose(ang, 90.0, atol=1.0))
    L = float(atoms.cell.lengths()[ax])
    shift, gap_w = slab_origin_shift(atoms, ax)
    pos = atoms.get_positions()
    z = (pos[:, ax] - shift) % L
    nb = max(int(round(L / zbin)), 8)
    edges = np.linspace(0, L, nb + 1)
    zc = 0.5 * (edges[1:] + edges[:-1])
    fwmask = np.isin(sym, FRAMEWORK)
    prof = {"z": zc}
    prof["framework"] = np.histogram(z[fwmask], bins=edges)[0]
    for el in ("P", "S", "Cl", "Li", "Sn", "O", "H"):
        if el in present:
            prof[el] = np.histogram(z[sym == el], bins=edges)[0]
    hcl = klass
    for tag, name in (("H-O", "H_O"), ("H-S", "H_S"), ("bridging_O_S", "H_bridge"), ("H2", "H_H2")):
        prof[name] = np.histogram(z[H[hcl == tag]], bins=edges)[0]

    # 슬랩 표면: 골격밀도가 (bulk plateau)/2 를 넘는 첫/마지막 빈의 경계
    fwp = prof["framework"].astype(float)
    plateau = float(np.median(fwp[fwp > 0])) if (fwp > 0).any() else 0.0
    inside = np.where(fwp >= 0.5 * plateau)[0]
    if inside.size:
        z_lo, z_hi = float(edges[inside[0]]), float(edges[inside[-1] + 1])
    else:
        z_lo, z_hi = 0.0, L
    depth = np.where(z < z_lo, z - z_lo, np.where(z > z_hi, z_hi - z, np.minimum(z - z_lo, z_hi - z)))
    hs_idx = H[hcl == "H-S"]
    ho_idx = H[hcl == "H-O"]
    # S-H 를 **어디에 붙었나**로 쪼갠다 — 이게 '반응이 골격에서 일어났나' 를 가른다.
    sh_S = S[cSH[S] > 0]
    out["sulfur"]["SH_location"] = {
        "on_framework_S": int(((cSP + cSSn)[sh_S] > 0).sum()),
        "on_free_S_inside_slab": int((((cSP + cSSn)[sh_S] == 0) & (depth[sh_S] > 0)).sum()),
        "on_free_S_in_fluid": int((((cSP + cSSn)[sh_S] == 0) & (depth[sh_S] <= 0)).sum()),
    }
    # 표면 두 쪽을 따로 (LPSnSC 는 두 표면의 양이온 종단이 다르다)
    lo_side = H[(hcl == "H-S") & (z[H] < 0.5 * (z_lo + z_hi)) & (depth[H] > 0)]
    hi_side = H[(hcl == "H-S") & (z[H] >= 0.5 * (z_lo + z_hi)) & (depth[H] > 0)]
    out["zprofile"] = {
        "axis": int(ax), "axis_letter": "abc"[ax], "orthogonal_cell": ortho,
        "axis_diagnostics": axdiag, "origin_shift": shift, "fluid_gap_width": gap_w,
        "slab_lo": z_lo, "slab_hi": z_hi, "slab_thickness": z_hi - z_lo,
        "bin_width": float(L / nb),
        "n_H_inside_slab": int((depth[H] > 0).sum()),
        "n_H_S_inside_slab": int((depth[hs_idx] > 0).sum()) if hs_idx.size else 0,
        "n_H_S_inside_lo_side": int(len(lo_side)),
        "n_H_S_inside_hi_side": int(len(hi_side)),
        "z_lo_side_raw": float((z_lo + shift) % L), "z_hi_side_raw": float((z_hi + shift) % L),
        "max_H_penetration_depth": float(depth[H].max()) if H.size else 0.0,
        "max_H_S_penetration_depth": float(depth[hs_idx].max()) if hs_idx.size else 0.0,
        "mean_H_S_depth": float(depth[hs_idx].mean()) if hs_idx.size else float("nan"),
        "mean_H_O_depth": float(depth[ho_idx].mean()) if ho_idx.size else float("nan"),
        "n_framework_in_fluid": {el: int(((depth[sym == el]) < -1.0).sum())
                                 for el in ("Li", "S", "Cl", "P", "Sn") if el in present},
    }
    out["cation_layers"] = cation_layers(atoms, ax)
    out["_profile_arrays"] = prof
    out["_rdf_curves"] = rdf_curves
    out["_depth"] = depth
    out["_sym"] = sym
    return out


# ══ xyz 프레임 진단 ═════════════════════════════════════════════════════════
def frames_report(path, fidelity_csv=None, energy_col="DFT (eV)"):
    """combined.xyz 의 성격 — 프레임 수·조성·셀 고정·**중복 프레임**·시간순서 여부.

    fidelity_csv 를 주면 프레임의 free_energy(없으면 energy) 를 CSV 의 DFT 에너지에
    **탐욕 최근접 유일매칭**해서 프레임 -> Step 대응표를 만든다. 파일 저장 순서가
    시간 순서가 아닐 수 있기 때문에 이 표가 있어야 궤적으로 쓸 수 있다.

    ⛔ 못 하는 것: 에너지가 거의 겹치는 프레임이 있으면 매칭이 틀릴 수 있다.
       그래서 매칭 잔차(max_match_residual_eV)를 같이 낸다 — 크면 믿지 마라.
    """
    from ase.io import read
    frames = read(str(path), index=":")
    rows = []
    pos = []
    for k, at in enumerate(frames):
        c = Counter(at.get_chemical_symbols())
        e = fe = ""
        try:
            fe = float(at.calc.results.get("free_energy"))
        except Exception:
            fe = ""
        try:
            e = float(at.get_potential_energy())
        except Exception:
            e = ""
        rows.append({"frame": k, "n_atoms": len(at),
                     "formula": "".join(f"{el}{c[el]}" for el in sorted(c)),
                     "a": round(float(at.cell.lengths()[0]), 4),
                     "b": round(float(at.cell.lengths()[1]), 4),
                     "c": round(float(at.cell.lengths()[2]), 4),
                     "volume": round(float(at.get_volume()), 3),
                     "energy_eV": e, "free_energy_eV": fe, "step": ""})
        pos.append(at.get_positions())
    forms = {r["formula"] for r in rows}
    cells = {(r["a"], r["b"], r["c"]) for r in rows}
    dups = [[k, m] for k in range(len(pos)) for m in range(k + 1, len(pos))
            if pos[k].shape == pos[m].shape and np.allclose(pos[k], pos[m], atol=1e-6)]
    # 저장된 `forces` 열이 `DFT_forces` 와 같은가 (= MLP 힘이 실제로는 없는가)
    forces_alias = None
    if "DFT_forces" in frames[0].arrays:
        try:
            forces_alias = all(np.array_equal(f.arrays["DFT_forces"], f.get_forces())
                               for f in frames)
        except Exception:
            forces_alias = None
    out = {"file": str(path), "n_frames": len(frames),
           "composition_constant": len(forms) == 1,
           "distinct_formulas": sorted(forms)[:5],
           "cell_constant": len(cells) == 1,
           "distinct_cells": [list(c) for c in sorted(cells)][:5],
           "duplicate_frame_pairs": dups,
           "n_unique_frames": len(frames) - len(dups),
           "forces_column_equals_DFT_forces": forces_alias,
           "rows": rows}
    if fidelity_csv:
        ref = list(csv.DictReader(open(fidelity_csv)))
        kstep = list(ref[0].keys())[0]           # BOM 대비 — 첫 열이 Step
        vals = [float(r[energy_col]) for r in ref]
        steps = [float(r[kstep]) for r in ref]
        pool = [float(r["free_energy_eV"]) if r["free_energy_eV"] != "" else
                float(r["energy_eV"]) for r in rows]
        used, order, resid = set(), [], []
        for v in vals:
            cand = [m for m in range(len(pool)) if m not in used]
            best = min(cand, key=lambda m: abs(pool[m] - v))
            used.add(best); order.append(best); resid.append(abs(pool[best] - v))
        for st, m in zip(steps, order):
            rows[m]["step"] = st
        out["csv_rows"] = len(ref)
        out["max_match_residual_eV"] = float(max(resid)) if resid else None
        out["file_order_is_time_order"] = bool(order == sorted(order))
        out["step_to_frame"] = [[st, m] for st, m in zip(steps, order)]
        out["frames_without_csv_row"] = sorted(set(range(len(rows))) - used)
    return out


# ══ CSV 쓰기 ════════════════════════════════════════════════════════════════
def write_csv(path, rows, header=None):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    header = header or list(rows[0].keys())
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def emit(results, outdir):
    outdir = pathlib.Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    labels = [r["label"] for r in results]

    # 1) 조성
    els = sorted({e for r in results for e in r["composition"]})
    rows = []
    for r in results:
        row = {"system": r["label"], "n_atoms": r["n_atoms"]}
        row.update({e: r["composition"].get(e, 0) for e in els})
        row["H_over_O"] = round(r["H_over_O"], 4) if r["H_over_O"] else ""
        row["a_A"], row["b_A"], row["c_A"] = [round(x, 4) for x in r["cell_lengths"]]
        row["volume_A3"] = round(r["volume"], 2)
        rows.append(row)
    write_csv(outdir / "composition.csv", rows,
              ["system", "n_atoms"] + els + ["H_over_O", "a_A", "b_A", "c_A", "volume_A3"])

    # 2) 컷오프 (RDF 첫 최소 + 민감도)
    rows = []
    for r in results:
        for cr in r["cutoff_rows"]:
            rows.append({"system": r["label"], **cr})
    write_csv(outdir / "rdf_cutoffs.csv", rows,
              ["system", "pair", "source", "search_rmax", "n_pairs_in_search_range",
               "r_peak", "g_peak", "g_min", "cutoff_used",
               "valley_lo", "valley_hi", "valley_width",
               "CN_total_at_lo", "CN_total_at_mid", "CN_total_at_hi", "cut_invariant", "note"])

    # 2b) 컷오프 민감도 (H-O, H-S) — 결론이 컷오프에 얼마나 매달려 있나
    rows = []
    for r in results:
        for s in r["oxygen"]["cutoff_sensitivity"]:
            rows.append({"system": r["label"], "pair": "H-O", "cutoff_A": s["cut_HO"],
                         "n_H2O": s["n_H2O"], "n_OH": s["n_OH"], "n_H3O": s["n_H3O"],
                         "n_bare_O": s["n_bare_O"], "n_SH_bonds": "", "n_S_with_H": "",
                         "n_S_with_2H": ""})
        for s in r["sulfur"]["cutoff_sensitivity"]:
            rows.append({"system": r["label"], "pair": "H-S", "cutoff_A": s["cut_HS"],
                         "n_H2O": "", "n_OH": "", "n_H3O": "", "n_bare_O": "",
                         "n_SH_bonds": s["n_SH_bonds"], "n_S_with_H": s["n_S_with_H"],
                         "n_S_with_2H": s["n_S_with_2H"]})
    write_csv(outdir / "cutoff_sensitivity.csv", rows,
              ["system", "pair", "cutoff_A", "n_H2O", "n_OH", "n_H3O", "n_bare_O",
               "n_SH_bonds", "n_S_with_H", "n_S_with_2H"])

    # 3) RDF 곡선 (Origin-ready: r 한 열 + 계·쌍별 g 열)
    pairs = sorted({p for r in results for p in r["_rdf_curves"]})
    r0 = None
    cols = {}
    for r in results:
        for p, (rr, gg) in r["_rdf_curves"].items():
            r0 = rr if r0 is None else r0
            cols[f"g_{p}__{r['label']}"] = gg
    if r0 is not None:
        names = ["r_Angstrom"] + sorted(cols)
        with open(outdir / "rdf_curves.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(names)
            for k in range(len(r0)):
                w.writerow([f"{r0[k]:.3f}"] + [f"{cols[n][k]:.4f}" for n in names[1:]])

    # 4) 사면체 배위 분포
    rows = []
    for r in results:
        for M, t in r["tetrahedra"].items():
            for kk, v in t["joint_S_O"].items():
                nS_ = int(kk.split("S")[0]); nO_ = int(kk.split("S")[1].rstrip("O"))
                rows.append({"system": r["label"], "centre": M, "CN_S": nS_, "CN_O": nO_,
                             "species": f"{M}S{nS_}O{nO_}" if nO_ else f"{M}S{nS_}",
                             "count": v, "n_centres": t["n_centres"],
                             "frac_percent": round(100.0 * v / t["n_centres"], 2)})
    write_csv(outdir / "tetrahedra_coordination.csv", rows,
              ["system", "centre", "CN_S", "CN_O", "species", "count", "n_centres", "frac_percent"])

    # 5) 화학종 요약
    rows = []
    for r in results:
        t = r["tetrahedra"]
        row = {"system": r["label"]}
        for M in ("P", "Sn"):
            if M in t:
                row[f"n_{M}"] = t[M]["n_centres"]
                row[f"n_{M}S4_intact"] = t[M]["n_pure_MS4"]
                row[f"n_{M}_with_O"] = t[M]["n_with_O"]
                row[f"mean_CN_{M}_S"] = round(t[M]["mean_CN_S"], 3)
                row[f"mean_CN_{M}_O"] = round(t[M]["mean_CN_O"], 3)
        row.update({
            "n_S_total": r["sulfur"]["n_S"], "n_S_free": r["sulfur"]["n_S_free"],
            "n_H2S": r["sulfur"]["n_H2S"], "n_SH_minus": r["sulfur"]["n_SH_minus"],
            "n_SH_bonds_total": r["sulfur"]["n_SH_bonds_total"],
            "n_framework_S_with_H": r["sulfur"]["n_framework_S_with_H"],
            "n_SS_bonds": r["sulfur"]["n_SS_bonds"],
            "n_H2O": r["oxygen"]["n_H2O"], "n_OH": r["oxygen"]["n_OH"],
            "n_H3O": r["oxygen"]["n_H3O"], "n_bare_O": r["oxygen"]["n_bare_O"],
            "n_O_bonded_to_P": r["oxygen"]["n_O_bonded_to_P"],
            "n_H2_molecules": r["hydrogen"]["n_H2_molecules"],
            "n_H_inside_slab": r["zprofile"]["n_H_inside_slab"],
            "n_H_S_inside_slab": r["zprofile"]["n_H_S_inside_slab"],
            "n_H_S_inside_lo_side": r["zprofile"]["n_H_S_inside_lo_side"],
            "n_H_S_inside_hi_side": r["zprofile"]["n_H_S_inside_hi_side"],
            "n_SH_on_framework_S": r["sulfur"]["SH_location"]["on_framework_S"],
            "n_SH_on_free_S_inside": r["sulfur"]["SH_location"]["on_free_S_inside_slab"],
            "n_SH_on_free_S_in_fluid": r["sulfur"]["SH_location"]["on_free_S_in_fluid"],
            "max_H_penetration_A": round(r["zprofile"]["max_H_penetration_depth"], 2),
            "max_H_S_penetration_A": round(r["zprofile"]["max_H_S_penetration_depth"], 2),
            "slab_thickness_A": round(r["zprofile"]["slab_thickness"], 2),
            "normal_axis": r["zprofile"]["axis_letter"],
        })
        row.update({f"n_{e}_in_fluid": v for e, v in r["zprofile"]["n_framework_in_fluid"].items()})
        rows.append(row)
    hdr = []
    for row in rows:
        for k in row:
            if k not in hdr:
                hdr.append(k)
    write_csv(outdir / "speciation_summary.csv", rows, hdr)

    # 6) H 분류
    rows = []
    for r in results:
        h = r["hydrogen"]
        for k, v in h["class_cutoff"].items():
            rows.append({"system": r["label"], "method": "cutoff", "class": k, "count": v,
                         "percent": round(100.0 * v / h["n_H"], 2)})
        for k, v in h["nearest_heavy_element"].items():
            rows.append({"system": r["label"], "method": "nearest_heavy_atom", "class": k, "count": v,
                         "percent": round(100.0 * v / h["n_H"], 2)})
    write_csv(outdir / "hydrogen_classification.csv", rows,
              ["system", "method", "class", "count", "percent"])

    # 7) z 프로파일 (Origin-ready)
    for r in results:
        p = r["_profile_arrays"]
        names = ["z_Angstrom"] + [k for k in p if k != "z"]
        rows = []
        zlo = r["zprofile"]["slab_lo"]; zhi = r["zprofile"]["slab_hi"]
        for k in range(len(p["z"])):
            zz = p["z"][k]
            dep = (zz - zlo) if zz < zlo else ((zhi - zz) if zz > zhi else min(zz - zlo, zhi - zz))
            row = {"z_Angstrom": round(float(zz), 3), "depth_from_surface_A": round(float(dep), 3)}
            row.update({n: int(p[n][k]) for n in names[1:]})
            rows.append(row)
        write_csv(outdir / f"zprofile_{r['label']}.csv", rows,
                  ["z_Angstrom", "depth_from_surface_A"] + names[1:])

    # 7b) 양이온 층 조성 (도펀트가 무작위인가 층정렬인가)
    rows = []
    for r in results:
        for L in r.get("cation_layers", []):
            rows.append({"system": r["label"], **L})
    if rows:
        hdr = []
        for row in rows:
            for k in row:
                if k not in hdr:
                    hdr.append(k)
        write_csv(outdir / "cation_layers.csv", rows, hdr)

    # 8) JSON 전체
    dump = []
    for r in results:
        dump.append({k: v for k, v in r.items() if not k.startswith("_")})
    (outdir / "speciation_full.json").write_text(json.dumps(dump, indent=2, ensure_ascii=False))
    return outdir


# ══ selftest ════════════════════════════════════════════════════════════════
def _selftest():
    """합성 구조로 검증 — **음성 경로 포함**.

    양성만 있는 selftest 는 '항상 4 를 반환' 하는 코드도 통과시킨다. 그래서
    (a) 일부러 O 를 섞은 PS3O 를 만들어 **잡히는지**,
    (b) 일부러 컷오프 밖에 둔 원자가 **안 잡히는지**,
    (c) 법선축이 아닌 축을 골라내지 **않는지**,
    (d) 골짜기가 없는 (균일기체) 계에서 첫 최소 검출이 **실패로 보고되는지** 를 본다.
    """
    from ase import Atoms
    ok = [0, 0]

    def chk(c, m):
        ok[0] += 1
        ok[1] += bool(c)
        print(("  PASS " if c else "  FAIL ") + m)

    rng = np.random.default_rng(0)

    # ── (1) PS4 3개 + PS3O 1개 + 자유 S 2개(H2S 1 + S2- 1) + 물 2개 ────────
    L = 24.0
    pos, sym = [], []

    def tet(centre, c_el, ligs):
        v = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)
        v /= np.linalg.norm(v, axis=1)[:, None]
        pos.append(centre); sym.append(c_el)
        for k, (el, dist) in enumerate(ligs):
            pos.append(centre + v[k] * dist); sym.append(el)

    for k in range(3):
        tet(np.array([3.0 + 6 * k, 3.0, 3.0]), "P", [("S", 2.05)] * 4)
    tet(np.array([3.0, 9.0, 3.0]), "P", [("S", 2.05), ("S", 2.05), ("S", 2.05), ("O", 1.55)])
    # 자유 S: H2S (S + 2H at 1.35) / bare S
    pos.append(np.array([12.0, 12.0, 12.0])); sym.append("S")
    pos.append(np.array([12.0 + 1.35, 12.0, 12.0])); sym.append("H")
    pos.append(np.array([12.0, 12.0 + 1.35, 12.0])); sym.append("H")
    pos.append(np.array([18.0, 12.0, 12.0])); sym.append("S")
    # 물 2개
    for k in range(2):
        c = np.array([6.0 + 4 * k, 18.0, 18.0])
        pos.append(c); sym.append("O")
        pos.append(c + [0.96, 0, 0]); sym.append("H")
        pos.append(c + [-0.24, 0.93, 0]); sym.append("H")
    # 컷오프 밖 미끼: P 에서 3.5 Å 떨어진 O — **PS3O 로 세면 안 된다**
    pos.append(np.array([3.0, 3.0, 6.5])); sym.append("O")
    at = Atoms(symbols=sym, positions=np.array(pos), cell=[L, L, L], pbc=True)
    r = analyse(at, "selftest", zbin=2.0)

    t = r["tetrahedra"]["P"]
    chk(t["n_centres"] == 4, f"P centres = 4 (got {t['n_centres']})")
    chk(t["n_pure_MS4"] == 3, f"pure PS4 = 3 (got {t['n_pure_MS4']})  [음성: 미끼 O 를 안 셈]")
    chk(t["joint_S_O"].get("3S1O") == 1, f"PS3O = 1 (got {t['joint_S_O'].get('3S1O')})")
    chk(t["n_with_O"] == 1, f"P with O = 1 (got {t['n_with_O']})  [음성: 3.5 A O 는 미결합]")
    chk(r["sulfur"]["n_S_free"] == 2, f"free S = 2 (got {r['sulfur']['n_S_free']})")
    chk(r["sulfur"]["n_H2S"] == 1, f"H2S = 1 (got {r['sulfur']['n_H2S']})")
    chk(r["sulfur"]["n_S2minus_bare"] == 1, f"bare S2- = 1 (got {r['sulfur']['n_S2minus_bare']})")
    chk(r["oxygen"]["n_H2O"] == 2, f"H2O = 2 (got {r['oxygen']['n_H2O']})")
    chk(r["hydrogen"]["class_cutoff"].get("H-S") == 2,
        f"H-S class = 2 (got {r['hydrogen']['class_cutoff'].get('H-S')})")
    chk(r["hydrogen"]["class_cutoff"].get("H-O") == 4,
        f"H-O class = 4 (got {r['hydrogen']['class_cutoff'].get('H-O')})")

    # ── (2) 음성: 완전히 균일한 랜덤 기체 → 첫 최소 검출이 '실패' 로 보고돼야 ──
    n = 400
    gas = Atoms(symbols=["S"] * n, positions=rng.random((n, 3)) * 30.0,
                cell=[30.0] * 3, pbc=True)
    from ase.neighborlist import neighbor_list
    nlg = neighbor_list("ijd", gas, 6.0)
    rr, gg, hh = rdf(gas, "S", "S", rmax=6.0, dr=0.05, nl=nlg)
    fm = first_minimum(rr, gg, hh, 3.2)
    chk(not fm["ok"], f"uniform gas -> first_minimum ok=False (got {fm})  [음성 경로]")

    # ── (3) 법선축 판별: 벌크(빈틈 없음)면 축이 애매해야 하고, 슬랩이면 그 축을 골라야 ──
    zl = []
    for k in range(300):
        zl.append([rng.random() * 20, rng.random() * 20, rng.random() * 12.0])   # z 0..12 슬랩
    for k in range(150):
        zl.append([rng.random() * 20, rng.random() * 20, 14.0 + rng.random() * 10.0])
    s2 = ["S"] * 300 + ["O"] * 150
    slab = Atoms(symbols=s2, positions=np.array(zl), cell=[20, 20, 24.0], pbc=True)
    ax, diag = normal_axis(slab)
    chk(ax == 2, f"slab normal axis = 2 (got {ax})")
    bulk = Atoms(symbols=["S"] * 400, positions=rng.random((400, 3)) * 20.0,
                 cell=[20.0] * 3, pbc=True)
    axb, diagb = normal_axis(bulk)
    chk(all(d["occ_framework"] > 0.9 for d in diagb),
        "bulk: 세 축 모두 occ>0.9 (법선축 없음이 드러남)  [음성 경로]")

    # ── (4) 컷오프 민감도 플래그가 실제로 동작하나 ──────────────────────────
    row = [c for c in r["cutoff_rows"] if c["pair"] == "P-S"]
    chk(bool(row) and row[0]["cut_invariant"] == "YES",
        f"P-S 골짜기 안에서 배위수 불변 (got {row[0]['cut_invariant'] if row else 'n/a'})")

    print(f"\n  {ok[1]}/{ok[0]} passed")
    return 0 if ok[1] == ok[0] else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--struct", action="append", default=[],
                    metavar="LABEL=PATH", help="분석할 구조 (여러 번). 예: LPSC-H2O=a.cif")
    ap.add_argument("--outdir", default=None, help="CSV/JSON 출력 폴더")
    ap.add_argument("--frames-report", action="append", default=[],
                    metavar="PATH", help="combined.xyz 프레임 진단")
    ap.add_argument("--fidelity-csv", action="append", default=[],
                    metavar="PATH", help="--frames-report 와 같은 순서로. 프레임->Step 대응")
    ap.add_argument("--zbin", type=float, default=2.0, help="z-프로파일 빈 폭 (Å)")
    ap.add_argument("--dr", type=float, default=0.02, help="RDF 빈 폭 (Å)")
    ap.add_argument("--valley-frac", type=float, default=0.5,
                    help="smoothed_argmin 경로의 골짜기 폭 문턱 = (1+valley_frac) x g_min")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        return _selftest()

    if a.frames_report:
        out = []
        for k, p in enumerate(a.frames_report):
            fc = a.fidelity_csv[k] if k < len(a.fidelity_csv) else None
            fr = frames_report(p, fidelity_csv=fc)
            out.append(fr)
            print(f"{fr['file']}: {fr['n_frames']} frames "
                  f"({fr['n_unique_frames']} unique) | "
                  f"composition_constant={fr['composition_constant']} | "
                  f"cell_constant={fr['cell_constant']}")
            print(f"  formulas: {fr['distinct_formulas']}")
            print(f"  cells:    {fr['distinct_cells']}")
            print(f"  duplicate frame pairs: {fr['duplicate_frame_pairs']}")
            print(f"  `forces` column == `DFT_forces`: "
                  f"{fr['forces_column_equals_DFT_forces']}  "
                  f"(True => no MLP forces stored)")
            if fc:
                print(f"  csv rows {fr['csv_rows']} | file order == time order: "
                      f"{fr['file_order_is_time_order']} | max match residual "
                      f"{fr['max_match_residual_eV']:.2e} eV | frames w/o csv row "
                      f"{fr['frames_without_csv_row']}")
        if a.outdir:
            rows = []
            for fr in out:
                for r in fr["rows"]:
                    rows.append({"file": pathlib.Path(fr["file"]).name, **r})
            write_csv(pathlib.Path(a.outdir) / "xyz_frames.csv", rows)

    if not a.struct:
        return 0

    from ase.io import read
    results = []
    for spec in a.struct:
        if "=" not in spec:
            ap.error(f"--struct 는 LABEL=PATH 형식이어야 한다: {spec}")
        label, path = spec.split("=", 1)
        atoms = read(path)
        r = analyse(atoms, label, dr=a.dr, zbin=a.zbin, valley_frac=a.valley_frac)
        results.append(r)
        c = r["composition"]
        t = r["tetrahedra"]
        print(f"\n=== {label}  ({r['n_atoms']} atoms, "
              f"{'/'.join(f'{k}{v}' for k, v in c.items())})")
        print(f"  normal axis = {r['zprofile']['axis_letter']} "
              f"(slab {r['zprofile']['slab_lo']:.1f}-{r['zprofile']['slab_hi']:.1f} Å)")
        for M in t:
            print(f"  {M}: {t[M]['joint_S_O']}  meanCN(S)={t[M]['mean_CN_S']:.3f} "
                  f"meanCN(O)={t[M]['mean_CN_O']:.3f}")
        print(f"  S: free={r['sulfur']['n_S_free']} H2S={r['sulfur']['n_H2S']} "
              f"SH-={r['sulfur']['n_SH_minus']} S-H bonds={r['sulfur']['n_SH_bonds_total']} "
              f"S-S={r['sulfur']['n_SS_bonds']}")
        print(f"  O: H2O={r['oxygen']['n_H2O']} OH={r['oxygen']['n_OH']} "
              f"H3O={r['oxygen']['n_H3O']} bare={r['oxygen']['n_bare_O']}")
        print(f"  H: {r['hydrogen']['class_cutoff']}  H2={r['hydrogen']['n_H2_molecules']}")

    if a.outdir:
        d = emit(results, a.outdir)
        print(f"\nwrote CSV/JSON -> {d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
