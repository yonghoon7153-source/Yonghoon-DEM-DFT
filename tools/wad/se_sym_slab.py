#!/usr/bin/env python3
"""se_sym_slab.py — comp1 (001) PS₄ 보존 **대칭 슬랩** 두 장 빌더·검증기 (W_ad · SE|SE 대조)

결정: D-2026-09-23-wad-se-termination-symmetric (active · ratified)
카드: kb/projects/wad_lpscl_agc_vgcf_plan_2026_09_23.md §0′ *SE 종결 선택지*
문헌: litdb/papers/pustorino2025_lpscl_bulk_surface_mechanical_electronic_li_filament.md
      (6층 (100) Li₂S-rich Li₇₆P₁₂S₆₂Cl₁₂ · Li₂S-deficient Li₆₈P₁₂S₅₈Cl₁₂ 와 같은 정의)

하는 일
  1. 벌크에서 PS₄ 단위(P–S < 2.5 Å)를 찾고, 그 z 폭의 합집합 **밖**을 절단 창으로 잡는다.
  2. 창 안 원자 z 사이 틈마다 아래/위 조각의 형식전하(Li +1 · 자유 S −2 · Cl −1)를 센다.
     두 조각 전하가 같은 틈(Tasker 보상)만 후보다. 극성 틈(4|4 → +4/0)은 버린다.
     보상 틈은 둘이다 — 자유 S 가 **위** 조각으로 가는 틈 A · **아래** 조각으로 가는 틈 B.
  3. 슬랩 = 창 i 의 틈에서 위를 갖고, PS₄ 층 N 개 위 창 i+N 의 틈에서 아래를 갖는다.
       s_outer  (S 바깥 · Li₂S-rich 형)        : 아래 면 A · 위 면 B
       li_outer (Li·PS₄ 바깥 · Li₂S-deficient 형): 아래 면 B · 위 면 A
  4. 검증 — **하나라도 실패하면 파일을 쓰지 않는다** (결정의 enforcement):
       · PS₄ 온전: P 마다 2.5 Å 안 S 가 정확히 4개 · 그 S 가 벌크의 **같은 부모 S**
         (원자 ID + 셀 이미지로 추적 — 개수만 세면 이웃 S 로 채워진 것을 못 잡는다)
       · 조성: 벌크 (N/2) 셀 ± 2 Li₂S (s_outer +2 · li_outer −2) · 형식전하 0
       · 양면 동일: z → −z 로 보내는 점연산 {R|t} 중 슬랩을 자기 자신에 겹치는 것이 있다
         (최대 편차 ≤ --tol_sym). 윗면 = 아랫면의 대칭상이라는 뜻이다.
         comp1_V0_k444 에서는 x 축 2회 회전(편차 1e-4 Å)이 그것이다 — −4 축은 **없다**
         (Li 정렬이 입방 대칭을 깨서 F-43m 이 아니다. 2026-09-23 실측).
       · 면 조성 동일(바깥 PS₄ 층 밖 원자) · 최단 원자간 거리 ≥ 1.5 Å · 창 안 Cl 0
  5. 대칭축을 y = 0, 슬랩 중심을 z = c/2 에 놓는다 → 그 C2 가 분수 병진 없이 격자에
     얹혀서 pw.x 가 대칭으로 잡는다 (k 점 절약).

실행
  python3 tools/wad/se_sym_slab.py --selftest
  python3 tools/wad/se_sym_slab.py --scan                    # 창·틈·전하만 본다
  python3 tools/wad/se_sym_slab.py --out db/structures/wad_se_slabs_2026_09_23
  python3 tools/wad/se_sym_slab.py --out <구조폴더> --qe_out <입력폴더>   # SE|SE 대조 QE 입력까지
  python3 tools/wad/se_sym_slab.py --relax_check <잡>/pw.in <최종좌표.txt|pw.out>   # 이완 점검 (PS₄·짝·진공·층별 변위 · 판정 아님)

⛔ 이 도구가 **못 하는 것**
  · 이완하지 않는다 — 벌크 절단 좌표 그대로다. 이완은 QE 입력(relax)으로 따로 돈다.
  · (001) 밖의 면, Cl 바깥 종결(음이온 자리바꿈 48H^inv, Pustorino #4/#5)은 만들지 않는다.
  · 양면 동일 검사는 **점연산 8개(z 뒤집기 × 면내 부호순열)** 만 본다. 벌크가 그 대칭을
    잃은 구조(무질서 Li 등)면 실패하고, 그걸 '면이 다르다' 와 '벌크 대칭이 깨졌다' 로
    구분하지 못한다 — 실패 메시지를 보고 사람이 판단한다.
  · 표면 재구성·Li 재배치 탐색 없음. 에너지를 계산하지 않는다.
  · QE 입력은 comp1 정본 설정(USPP GBRV Li/S/Cl v1.4 + P rrkjus psl 1.0.0 · 52/520 Ry)만
    쓴다. PP 파일이 서버에 있는지·해시는 **러너**가 본다 (여기서는 이름만 적는다).
"""
import argparse
import hashlib
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
BULK_DEFAULT = os.path.join(REPO, "db", "structures", "comp1_V0_k444.cif")

FORMAL = {"Li": 1, "P": 5, "S": -2, "Cl": -1}  # PS₄ = P⁵⁺ + 4 S²⁻ → PS₄³⁻
R_PS = 2.5            # P–S 결합 (벌크 2.04/2.11 Å · 다음 P–S 는 4 Å 밖)
MIN_GAP = 0.25        # 이보다 좁은 틈에서는 자르지 않는다 [Å]
TERMS = {             # 종결 → (아래 면 틈, 위 면 틈, Li₂S 과부족)
    "s_outer": ("A", "B", +1),
    "li_outer": ("B", "A", -1),
}

# comp1 정본 DFT 설정 (kb/methodology/computational_methods_canonical.md §2 · 472행)
QE_PP = {"Li": (6.941, "li_pbe_v1.4.uspp.F.UPF"), "P": (30.974, "P.pbe-n-rrkjus_psl.1.0.0.UPF"),
         "S": (32.06, "s_pbe_v1.4.uspp.F.UPF"), "Cl": (35.45, "cl_pbe_v1.4.uspp.F.UPF")}
#: PP **내용** 해시 (comp1 정본 세트 — runs/static_ab/manifest.json · b2o3_uma_vs_dft_force_prereg 와 같은 값).
#:   이름이 같아도 다른 파일이 있다 (P rrkjus: QE 사이트판 atomic v6.3 ≠ 우리 v5.1 — cascade_rebuild_log §3-2).
#:   jobs.json 에 적고 러너(run_sese_gpu.sh)가 실행 기계의 파일과 **대조한다** — 다르면 시작하지 않는다.
PP_SHA256 = {
    "li_pbe_v1.4.uspp.F.UPF": "02cc4b3810e28a43b570277840d9631ca24f634d922928200c047b72c0a86bf5",
    "P.pbe-n-rrkjus_psl.1.0.0.UPF": "2d112dfec2e2d9b75a971574d9116aa92249988177791659bbcd2ba15f23c20c",
    "s_pbe_v1.4.uspp.F.UPF": "84ad731864187f416f714e961c3ad2f04dcbf811618e724d277885c18cb470df",
    "cl_pbe_v1.4.uspp.F.UPF": "5b1ebdea1e5ba743fba0100806206287e1f7f00460c7e6f19791446beaee0655",
}
ECUTWFC, ECUTRHO = 52.0, 520.0


class SlabError(RuntimeError):
    """검증 실패 — 이게 나면 파일을 쓰지 않는다."""


# ─────────────────────────────── 벌크 분석 ───────────────────────────────
def _mic(d, cell, pbc):
    """최소이미지 변위 (pbc 가 False 인 축은 감지 않는다)."""
    inv = np.linalg.inv(cell)
    f = d @ inv
    for k in range(3):
        if pbc[k]:
            f[..., k] -= np.round(f[..., k])
    return f @ cell


def check_orthogonal_c(atoms):
    C = atoms.cell.array
    if abs(C[0, 2]) > 1e-6 or abs(C[1, 2]) > 1e-6 or abs(C[2, 0]) > 1e-6 or abs(C[2, 1]) > 1e-6:
        raise SlabError("c 축이 z 와 나란하고 a·b 가 z 에 수직이어야 한다 (이 도구는 (001) 전용)")
    if abs(float(np.dot(C[0], C[1]))) > 1e-6:
        raise SlabError("a ⟂ b 여야 한다 — 양면 동일 검사의 점연산(면내 부호순열)이 직교 셀 전제다")


def _pairs(atoms, a_el, b_el, rcut):
    """(a, b, 거리, 정수 셀이동 S) — ASE neighbor_list 로 **모든 이미지**를 센다.

    ⛔ 2026-09-23 selftest 가 잡은 버그: 처음엔 분수좌표 반올림 최소이미지로 셌다.
       그건 원자 하나당 이미지 **하나**만 보여서, 작은 육방 셀(R 전개 LiNiO₂, a 2.878 Å)
       에서 Ni–O 6배위를 **2** 로 셌다 (같은 O 의 세 이미지가 전부 1.973 Å 인데 하나만 셌다).
    """
    from ase.neighborlist import neighbor_list
    sym = np.array(atoms.get_chemical_symbols())
    i, j, d, S = neighbor_list("ijdS", atoms, rcut)
    m = (sym[i] == a_el) & (sym[j] == b_el)
    return i[m], j[m], d[m], S[m]


def ps4_units(atoms):
    """{P 인덱스: [(S 인덱스, 정수 셀이동(3,), 결합길이), ...]} · 자유 S 목록.

    P 마다 R_PS 안 S 가 정확히 4개가 아니면 SlabError. 주기성은 atoms.pbc 를 따른다.
    """
    sym = np.array(atoms.get_chemical_symbols())
    i, j, d, S = _pairs(atoms, "P", "S", R_PS)
    units, bonded = {}, set()
    for p in np.where(sym == "P")[0]:
        m = i == p
        if int(m.sum()) != 4:
            raise SlabError(f"P{p}: {R_PS} Å 안 S 가 {int(m.sum())}개 (4 여야 한다 — PS₄ 가 끊겼거나 겹쳤다)")
        units[int(p)] = [(int(jj), np.array(ss, int), float(dd)) for jj, ss, dd in zip(j[m], S[m], d[m])]
        bonded.update(int(x) for x in j[m])
    free = [int(s) for s in np.where(sym == "S")[0] if int(s) not in bonded]
    return units, free


def windows(atoms, units):
    """PS₄ z 폭의 합집합 밖 구간들 (0 ≤ lo < c, hi 는 lo 위 — 원형 z 축)."""
    pos = atoms.get_positions()
    c = atoms.cell.array[2, 2]
    iv = []
    for p, lst in units.items():
        zp = pos[p, 2]
        dz = [pos[s, 2] + img[2] * c - zp for s, img, _ in lst]
        lo, hi = zp + min(dz), zp + max(dz)
        for k in (-1, 0, 1):
            iv.append((lo + k * c, hi + k * c))
    iv.sort()
    merged = []
    for lo, hi in iv:
        if merged and lo <= merged[-1][1] + 1e-9:
            merged[-1][1] = max(merged[-1][1], hi)
        else:
            merged.append([lo, hi])
    out = []
    for (a0, a1), (b0, b1) in zip(merged[:-1], merged[1:]):
        if 0.0 <= a1 < c and b0 > a1:
            out.append((a1, b0))
    return sorted(out)


def window_atoms(atoms, units, win):
    """창 안(엄밀히) 원자 인덱스와 z (창 lo 기준으로 펼친 값)."""
    sym = np.array(atoms.get_chemical_symbols())
    z = atoms.get_positions()[:, 2]
    c = atoms.cell.array[2, 2]
    lo, hi = win
    idx, zz = [], []
    for i in range(len(atoms)):
        zi = (z[i] - lo) % c + lo
        if lo < zi < hi:
            idx.append(i)
            zz.append(zi)
    return idx, zz, sym


def cut_candidates(atoms, units, win, free):
    """창 안의 틈마다 {z, 폭, 아래/위 조성, 전하, 종류}. 종류: A · B · mixed · polar."""
    idx, zz, sym = window_atoms(atoms, units, win)
    order = np.argsort(zz)
    idx = [idx[k] for k in order]
    zz = [zz[k] for k in order]
    edges = [win[0]] + zz + [win[1]]
    freeset = set(free)
    out = []
    for k in range(len(edges) - 1):
        z0, z1 = edges[k], edges[k + 1]
        if z1 - z0 < MIN_GAP:
            continue
        below, above = idx[:k], idx[k:]

        def comp(ids):
            d = {}
            for i in ids:
                key = "S_free" if (sym[i] == "S" and i in freeset) else str(sym[i])
                d[key] = d.get(key, 0) + 1
            return d

        def q(ids):
            return int(sum(FORMAL[str(sym[i])] for i in ids))

        qb, qa = q(below), q(above)
        cb, ca = comp(below), comp(above)
        if qb != qa:
            kind = "polar"
        elif ca.get("S_free", 0) and not cb.get("S_free", 0):
            kind = "A"
        elif cb.get("S_free", 0) and not ca.get("S_free", 0):
            kind = "B"
        else:
            kind = "mixed"
        out.append({"z": round((z0 + z1) / 2, 4), "gap_A": round(z1 - z0, 4),
                    "below": cb, "above": ca, "q_below": qb, "q_above": qa, "kind": kind})
    return out


def scan(atoms):
    check_orthogonal_c(atoms)
    units, free = ps4_units(atoms)
    ws = windows(atoms, units)
    sym = np.array(atoms.get_chemical_symbols())
    rep = {"n_P": len(units), "n_free_S": len(free), "windows": []}
    for w in ws:
        idx, _, _ = window_atoms(atoms, units, w)
        comp = {}
        for i in idx:
            comp[str(sym[i])] = comp.get(str(sym[i]), 0) + 1
        rep["windows"].append({"lo": round(w[0], 4), "hi": round(w[1], 4),
                               "width": round(w[1] - w[0], 4), "atoms": comp,
                               "cuts": cut_candidates(atoms, units, w, free)})
    return units, free, rep


# ─────────────────────────────── 슬랩 제작 ───────────────────────────────
def _pick_cut(win_rep, kind):
    c = [x for x in win_rep["cuts"] if x["kind"] == kind]
    if len(c) != 1:
        raise SlabError(f"창 [{win_rep['lo']}, {win_rep['hi']}] 에 {kind} 틈이 {len(c)}개 (1개여야 한다)")
    return c[0]


def build_slab(atoms, term, n_layers=6, vacuum=20.0, cuts=None, _rep=None):
    """term ∈ TERMS 또는 cuts=(아래 틈 종류, 위 틈 종류) 직접 지정(시험용).

    반환: (Atoms, meta). 원자마다 atoms.arrays['parent'] = 벌크 인덱스,
    atoms.arrays['image'] = 벌크 셀 z 이미지 번호.
    """
    from ase import Atoms
    check_orthogonal_c(atoms)
    units, free, rep = _rep if _rep else scan(atoms)
    for w in rep["windows"]:
        if w["atoms"].get("Cl", 0):
            raise SlabError(f"창 {w['lo']}–{w['hi']} 안에 Cl 이 있다 — comp1 가정(창 = Li + 자유 S)이 깨졌다")
    if cuts is None:
        if term not in TERMS:
            raise SlabError(f"모르는 종결: {term}")
        kb, kt = TERMS[term][0], TERMS[term][1]
    else:
        kb, kt = cuts
    nw = len(rep["windows"])          # 셀당 창 수 = 셀당 PS₄ 층 수
    c = atoms.cell.array[2, 2]
    wb = rep["windows"][0]
    kwin = n_layers                   # 창 0 에서 PS₄ 층 n_layers 개 위의 창
    wt = rep["windows"][kwin % nw]
    shift_t = (kwin // nw) * c

    def zcut(w, kind):
        if kind in ("A", "B"):
            return _pick_cut(w, kind)["z"]
        if kind == "naive":           # 시험용 — 창 밖(PS₄ 층 한가운데)에서 자른다
            return w["hi"] + 0.5 * (c / nw - w["width"])
        if kind == "polar":
            p = [x for x in w["cuts"] if x["kind"] == "polar"]
            if not p:
                raise SlabError("극성 틈이 없다")
            return p[len(p) // 2]["z"]
        raise SlabError(f"모르는 틈 종류: {kind}")

    zb = zcut(wb, kb)
    zt = zcut(wt, kt) + shift_t
    if kb == "polar" or kt == "polar":
        raise SlabError("극성 절단(4|4 · 형식전하 +4/0)은 만들지 않는다 — Tasker 보상 틈(A·B)만")
    pos = atoms.get_positions()
    sym = atoms.get_chemical_symbols()
    nimg = int(np.ceil((zt - zb) / c)) + 2
    keep_s, keep_p, keep_par, keep_img = [], [], [], []
    for m in range(-1, nimg + 1):
        for i in range(len(atoms)):
            z = pos[i, 2] + m * c
            if zb < z < zt:
                keep_s.append(sym[i])
                keep_p.append([pos[i, 0], pos[i, 1], z])
                keep_par.append(i)
                keep_img.append(m)
    keep_p = np.array(keep_p)
    keep_p[:, 2] -= keep_p[:, 2].min()
    thick = float(keep_p[:, 2].max())
    C = atoms.cell.array.copy()
    C[2] = [0.0, 0.0, thick + vacuum]
    keep_p[:, 2] += (C[2, 2] - thick) / 2.0
    slab = Atoms(keep_s, positions=keep_p, cell=C, pbc=(True, True, False))
    slab.arrays["parent"] = np.array(keep_par, int)
    slab.arrays["image"] = np.array(keep_img, int)
    meta = {"term": term, "cut_kinds": [kb, kt], "n_layers": n_layers, "vacuum_A": vacuum,
            "z_cut_bottom_bulk": round(zb, 4), "z_cut_top_bulk": round(zt, 4),
            "thickness_A": round(thick, 4), "c_A": round(float(C[2, 2]), 4)}
    return slab, meta


# ─────────────────────────────── 검증 ───────────────────────────────
def coordination(atoms, center, ligand, rcut):
    """center 마다 rcut 안 ligand 수(모든 이미지)와 그 안 최단거리 (atoms.pbc 를 따른다)."""
    sym = np.array(atoms.get_chemical_symbols())
    i, _, d, _ = _pairs(atoms, center, ligand, rcut)
    out = []
    for a in np.where(sym == center)[0]:
        m = i == a
        out.append((int(a), int(m.sum()), float(d[m].min()) if m.any() else float("nan")))
    return out


def symmetric_op(slab, tol):
    """z → −z 점연산 {R|t} 중 슬랩을 자기 자신에 겹치는 것 (최소 편차). (R, t, dev)."""
    sym = np.array(slab.get_chemical_symbols())
    pos = slab.get_positions()
    C = slab.cell.array
    pbc = (True, True, False)
    P = np.where(sym == "P")[0]
    ref = P if len(P) else np.arange(len(slab))
    best = (np.inf, None, None)
    for perm in ((0, 1), (1, 0)):
        for sx in (1, -1):
            for sy in (1, -1):
                R = np.zeros((3, 3))
                R[0, perm[0]], R[1, perm[1]], R[2, 2] = sx, sy, -1
                for j in ref:
                    t = pos[j] - R @ pos[ref[0]]
                    new = pos @ R.T + t
                    worst = 0.0
                    for s, p in zip(sym, new):
                        cand = np.where(sym == s)[0]
                        d = _mic(pos[cand] - p, C, pbc)
                        worst = max(worst, float(np.min(np.linalg.norm(d, axis=1))))
                        if worst > best[0]:
                            break
                    if worst < best[0]:
                        best = (worst, R, t)
    return best[1], best[2], best[0]


def validate(slab, meta, bulk, bulk_units, bulk_free, tol_sym=0.01):
    """검증 보고서 dict. 실패 항목이 있으면 report['ok'] = False."""
    rep = {"checks": {}, "ok": True}

    def put(name, ok, **kw):
        rep["checks"][name] = dict(ok=bool(ok), **kw)
        if not ok:
            rep["ok"] = False

    sym = np.array(slab.get_chemical_symbols())
    par = slab.arrays["parent"]
    img = slab.arrays["image"]
    # ① PS₄ 온전 + 부모 S 동일 (원자 ID · z 이미지). 슬랩은 z 비주기라 슬랩 쪽 셀이동 z 는 0.
    try:
        su, sfree = ps4_units(slab)
        bad = []
        for p, lst in su.items():
            bp = int(par[p])
            want = set((s, int(img[p]) + int(im[2])) for s, im, _ in bulk_units[bp])
            got = set((int(par[s]), int(img[s])) for s, _, _ in lst)
            if got != want:
                bad.append(int(p))
        put("ps4_intact_parent", not bad, n_P=len(su), mismatched_P=bad)
        # 자유 S 가 벌크에서도 자유 S 였나 (PS₄ S 가 떨어져 나와 자유 S 로 둔갑하지 않았나)
        orphan = [int(s) for s in sfree if int(par[s]) not in set(bulk_free)]
        put("no_orphan_ps4_S", not orphan, orphan_S=orphan)
    except SlabError as e:
        put("ps4_intact_parent", False, error=str(e))
    # ② 조성
    n = {el: int((sym == el).sum()) for el in ("Li", "P", "S", "Cl")}
    bsym = np.array(bulk.get_chemical_symbols())
    nb = {el: int((bsym == el).sum()) for el in ("Li", "P", "S", "Cl")}
    ncell = n["P"] / nb["P"] if nb["P"] else 0
    base = {el: nb[el] * ncell for el in nb}
    d_li2s = (n["Li"] - base["Li"]) / 2.0
    comp_ok = (float(ncell).is_integer() and n["Cl"] == base["Cl"]
               and abs((n["S"] - base["S"]) - d_li2s) < 1e-9 and float(d_li2s).is_integer())
    want = None
    if meta.get("term") in TERMS:
        want = 2 * TERMS[meta["term"]][2]
        comp_ok = comp_ok and d_li2s == want
    put("composition", comp_ok, counts=n, bulk_cells=ncell, delta_Li2S=d_li2s,
        want_delta_Li2S=want, formula=slab.get_chemical_formula(mode="metal"))
    q = int(sum(FORMAL[s] for s in sym))
    put("formal_charge_zero", q == 0, q=q)
    # ③ 양면 동일 (z 뒤집기 대칭)
    R, t, dev = symmetric_op(slab, tol_sym)
    put("faces_equivalent", dev <= tol_sym, max_dev_A=round(float(dev), 5),
        R=None if R is None else R.astype(int).tolist(),
        t_A=None if t is None else np.round(t, 4).tolist(), tol_A=tol_sym)
    # ④ 면 조성 (바깥 PS₄ 층 밖)
    pos = slab.get_positions()
    try:
        su, _ = ps4_units(slab)
        zs = [pos[s, 2] for lst in su.values() for s, _, _ in lst]
        zlo, zhi = min(zs), max(zs)
        f_lo = sorted(str(s) for s, z in zip(sym, pos[:, 2]) if z < zlo - 1e-6)
        f_hi = sorted(str(s) for s, z in zip(sym, pos[:, 2]) if z > zhi + 1e-6)
        put("face_composition_equal", f_lo == f_hi,
            bottom={e: f_lo.count(e) for e in set(f_lo)}, top={e: f_hi.count(e) for e in set(f_hi)})
    except SlabError as e:
        put("face_composition_equal", False, error=str(e))
    # ⑤ 원자 겹침
    from ase.geometry import get_distances
    _, L = get_distances(pos, cell=slab.cell, pbc=slab.pbc)
    np.fill_diagonal(L, np.inf)
    put("min_distance", float(L.min()) >= 1.5, min_A=round(float(L.min()), 4))
    return rep


# ─────────────────────────────── 배치·출력 ───────────────────────────────
def place_for_qe(slab, R, t):
    """C2 축을 y = 0(또는 x = 0), 슬랩 중심을 z = c/2 로 — 분수 병진 없는 연산이 되게."""
    s = slab.copy()
    pos = s.get_positions()
    c = s.cell.array[2, 2]
    shift = np.zeros(3)
    # {R|t}: r → R r + t. 고정점(축): R r0 + t = r0 의 해 중 R 이 −1 인 성분
    for k in range(2):
        if abs(R[k, k] + 1) < 1e-9:
            shift[k] = -t[k] / 2.0
    zc = t[2] / 2.0
    shift[2] = c / 2.0 - zc
    s.set_positions(pos + shift)
    s.wrap(pbc=(True, True, False))
    return s


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def qe_input(atoms, kind, prefix, kpts, pseudo_dir, calc="scf"):
    """comp1 정본 설정 + W_ad 분산 결정(D3 2체 명시). kind ∈ {slab, bulk}."""
    els = [e for e in ("Li", "P", "S", "Cl") if e in atoms.get_chemical_symbols()]
    d3 = calc == "scf"
    # disk_io='medium': k 점이 여럿이면 파동함수를 **디스크**에 둔다. 'low'(scf 기본)는 전 k 점을
    #   호스트 RAM 에 들고 있어 162원자·k 6개면 ~9 GB 다 — gabia 는 CPU 잡(Nd k-탐침 34 GB)과
    #   RAM 을 나눠 쓰므로 OOM 킬러가 남의 잡을 칠 수 있다 (2026-09-23 설계 검토).
    L = ["&CONTROL", f"  calculation = '{calc}'", f"  prefix = '{prefix}'", "  outdir = './tmp'",
         f"  pseudo_dir = '{pseudo_dir}'", "  tprnfor = .true.", "  disk_io = 'medium'"]
    if kind == "bulk":
        L.append("  tstress = .true.")
    if calc == "relax":
        L += ["  etot_conv_thr = 1.0d-5", "  forc_conv_thr = 1.0d-3", "  nstep = 200"]
    L += ["/", "&SYSTEM", "  ibrav = 0", f"  nat = {len(atoms)}", f"  ntyp = {len(els)}",
          f"  ecutwfc = {ECUTWFC}", f"  ecutrho = {ECUTRHO}",
          "  occupations = 'smearing'", "  smearing = 'gaussian'", "  degauss = 0.005"]
    if d3:
        # ⛔ D-2026-09-23-wad-d3-twobody-atm-separate: 2체만 · 명시. D3 는 SCF 뒤 가산항이라
        #   같은 출력에서 E(PBE) = E(tot) − E(Dispersion) 로 PBE 값도 나온다.
        L += ["  vdw_corr = 'grimme-d3'", "  dftd3_version = 4", "  dftd3_threebody = .false."]
    else:
        # 이완은 PBE(분산 끔) — Pustorino 2025(PBE · vdW 없음 · 완전 이완)와 같은 조건.
        L += ["  vdw_corr = 'none'"]
    L += ["/", "&ELECTRONS", "  conv_thr = 1.0d-8", "  mixing_beta = 0.3", "  electron_maxstep = 200"]
    if kind == "slab":
        L.append("  mixing_mode = 'local-TF'")
    L += ["/"]
    if calc == "relax":
        L += ["&IONS", "  ion_dynamics = 'bfgs'", "/"]
    L += ["", "ATOMIC_SPECIES"]
    for e in els:
        L.append(f"  {e:2s} {QE_PP[e][0]:8.3f}  {QE_PP[e][1]}")
    L += ["", "CELL_PARAMETERS angstrom"]
    for v in atoms.cell.array:
        L.append("  %16.10f %16.10f %16.10f" % tuple(v))
    L += ["", "ATOMIC_POSITIONS angstrom"]
    for s, p in zip(atoms.get_chemical_symbols(), atoms.get_positions()):
        L.append(f"  {s:2s} %16.10f %16.10f %16.10f" % tuple(p))
    L += ["", "K_POINTS automatic", "  %d %d %d 0 0 0" % tuple(kpts), ""]
    return "\n".join(L)


def write_outputs(out, bulk_path, n_layers, vacuum, tol_sym, qe_out=None, pseudo_dir="/data/work/pseudo",
                  kslab=(4, 4, 1), kbulk=(4, 4, 4)):
    from ase.io import read, write
    bulk = read(bulk_path)
    units, free, rep = scan(bulk)
    os.makedirs(out, exist_ok=True)
    man = {"tool": "tools/wad/se_sym_slab.py", "decision": "D-2026-09-23-wad-se-termination-symmetric",
           "bulk": os.path.relpath(bulk_path, REPO), "bulk_sha256": sha256(bulk_path),
           "bulk_formula": bulk.get_chemical_formula(mode="metal"), "scan": rep, "slabs": {}}
    built = {}
    for term in TERMS:
        slab, meta = build_slab(bulk, term, n_layers, vacuum, _rep=(units, free, rep))
        v = validate(slab, meta, bulk, units, free, tol_sym)
        if not v["ok"]:
            bad = {k: x for k, x in v["checks"].items() if not x["ok"]}
            raise SlabError(f"{term} 검증 실패 — 파일을 쓰지 않는다: {json.dumps(bad, ensure_ascii=False)}")
        R = np.array(v["checks"]["faces_equivalent"]["R"], float)
        t = np.array(v["checks"]["faces_equivalent"]["t_A"], float)
        placed = place_for_qe(slab, R, t)
        v2 = validate(placed, meta, bulk, units, free, tol_sym)   # 옮긴 뒤에도 같은 검증
        if not v2["ok"]:
            raise SlabError(f"{term}: 배치 이동 뒤 검증 실패 — {v2['checks']}")
        R2 = np.array(v2["checks"]["faces_equivalent"]["t_A"], float)
        stem = f"comp1_001_{term}_L{n_layers}"
        pv = os.path.join(out, stem + ".vasp")
        px = os.path.join(out, stem + ".xyz")
        write(pv, placed, format="vasp", direct=True, sort=True)
        write(px, placed, format="xyz")
        area = float(np.linalg.norm(np.cross(placed.cell.array[0], placed.cell.array[1])))
        man["slabs"][term] = {**meta, "nat": len(placed), "formula": placed.get_chemical_formula(mode="metal"),
                              "area_A2": round(area, 4), "files": {"vasp": os.path.basename(pv),
                                                                   "xyz": os.path.basename(px)},
                              "sha256": {"vasp": sha256(pv), "xyz": sha256(px)},
                              "validation": v2["checks"], "c2_t_after_placement_A": np.round(R2, 4).tolist()}
        built[term] = placed
    man["cleavage_identity"] = (
        "W_cleave(Li 2|6, (001)) = γ(s_outer) + γ(li_outer) = [E(s_outer) + E(li_outer) − "
        f"{2 * n_layers // len(rep['windows'])}·E(bulk 셀)] / (2A) — Li₂S 과부족(+2/−2)이 상쇄돼 μ 가 필요 없다. "
        "Pustorino 2025 대응값 (0.74 + 0.20)/2 ≈ 0.47 J/m² (PBE · 이완)")
    mp = os.path.join(out, "manifest.json")
    with open(mp, "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=1)
    if qe_out:
        write_qe_set(qe_out, built, bulk, man, pseudo_dir, kslab, kbulk, n_layers=n_layers, vacuum=vacuum,
                     manifest_path=mp)
    return man


def write_qe_set(qe_out, built, bulk, man, pseudo_dir, kslab, kbulk, n_layers=None, vacuum=None,
                 manifest_path=None):
    """SE|SE 대조 잡 5개: 벌크 SCF · 두 슬랩 SCF(무이완 W_sep) · 두 슬랩 PBE 이완.

    jobs.json 의 decisions 에 경보 결정(ALARM — 집계기와 같은 ID)과 주장 범위(A′)를 같이 적는다
    (2026-09-24 · 4층 세트부터. 6층 세트의 jobs.json 은 옛 두 ID 그대로 둔다 — 입력 해시와 무관한 메타다).
    """
    os.makedirs(qe_out, exist_ok=True)
    jobs = [("01_bulk_scf", bulk, "bulk", "scf", kbulk)]
    for term in TERMS:
        jobs.append((f"02_{term}_scf", built[term], "slab", "scf", kslab))
    for term in TERMS:
        jobs.append((f"03_{term}_relax_pbe", built[term], "slab", "relax", kslab))
    idx = {"decisions": ["D-2026-09-23-wad-se-termination-symmetric",
                         "D-2026-09-23-wad-d3-twobody-atm-separate",
                         ALARM["decision"], "D-2026-09-23-wad-a-prime-scope"],
           "structures_manifest_sha256": sha256(manifest_path) if manifest_path else None, "settings": {
               "n_layers": n_layers, "vacuum_total_A": vacuum,
               "k_and_vacuum_status": "출발값 — 수렴 판정이 아니다 (Codex BW Q5). 벌크 k 는 슬랩 면내 밀도와 맞춘다",
               "pp": {e: v[1] for e, v in QE_PP.items()}, "ecutwfc_Ry": ECUTWFC, "ecutrho_Ry": ECUTRHO,
               "pp_sha256": {v[1]: PP_SHA256[v[1]] for v in QE_PP.values()},
               "smearing": "gaussian 0.005 Ry", "k_slab": list(kslab), "k_bulk": list(kbulk),
               "d3": "scf: grimme-d3 · dftd3_version=4 (BJ) · dftd3_threebody=.false. (2체) · "
                     "relax: vdw_corr='none' (PBE — Pustorino 조건)",
               "why_52_520": "comp1_V0_k444 구조를 낸 정본 설정 (computational_methods_canonical.md 472행)"},
           "jobs": []}
    for name, at, kind, calc, k in jobs:
        d = os.path.join(qe_out, name)
        os.makedirs(d, exist_ok=True)
        txt = qe_input(at, kind, name, k, pseudo_dir, calc)
        p = os.path.join(d, "pw.in")
        with open(p, "w") as f:
            f.write(txt)
        idx["jobs"].append({"dir": name, "kind": kind, "calc": calc, "nat": len(at), "kpts": list(k),
                            "pw_in_sha256": sha256(p)})
    with open(os.path.join(qe_out, "jobs.json"), "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=1)


# ─────────────────────────────── 집계 (결과 전에 식을 고정) ───────────────────────────────
RY_J = 2.179872361103e-18     # 1 Ry [J]
_RE_E = r"^!\s+total energy\s+=\s+(-?\d+\.\d+)\s+Ry"
_RE_D3 = r"(?:DFT-D3 Dispersion|Dispersion Correction)\s+=\s+(-?\d+\.\d+)\s+Ry"
_RE_TS = r"smearing contrib\. \(-TS\)\s+=\s+(-?\d+\.\d+)\s+Ry"


def parse_pw(out_path, calc, d3):
    """pw.out → {E_tot, E_d3, E_pbe, mTS, nat}. 완료·수렴·(D3 줄) 이 없으면 SlabError.

    완료 판정은 run_sese_gpu.sh 의 _done 과 같은 기준이다 (한 곳이 바뀌면 둘 다 본다).
    """
    import re
    if not os.path.isfile(out_path):
        raise SlabError(f"{out_path} 없음")
    t = open(out_path, errors="ignore").read()
    if "JOB DONE" not in t or "convergence has been achieved" not in t:
        raise SlabError(f"{out_path}: 미완료 또는 SCF 미수렴")
    if calc == "relax":
        if not re.search(r"End final coordinates|bfgs converged", t) or \
                "The maximum number of steps has been reached" in t:
            raise SlabError(f"{out_path}: 이완 미수렴")
    E = re.findall(_RE_E, t, re.M)
    if not E:
        raise SlabError(f"{out_path}: '!    total energy' 줄 없음")
    D = re.findall(_RE_D3, t)
    if d3 and not D:
        # ⛔ D3 를 켠 잡에서 분산 줄을 못 찾으면 0 으로 두지 않는다 (없는 값을 0 으로 그리지 않는다)
        raise SlabError(f"{out_path}: D3 잡인데 분산 에너지 줄이 없다")
    if not d3 and D:
        raise SlabError(f"{out_path}: 분산 끈 잡인데 분산 줄이 있다 — 입력이 바뀌었나")
    TS = re.findall(_RE_TS, t)
    nat = re.findall(r"number of atoms/cell\s+=\s+(\d+)", t)
    e = float(E[-1])
    ed = float(D[-1]) if D else None
    return {"E_tot_Ry": e, "E_d3_Ry": ed, "E_pbe_Ry": e - ed if ed is not None else e,
            "mTS_Ry": float(TS[-1]) if TS else None, "nat": int(nat[-1]) if nat else None}


#: SE|SE 경보 운영값 — D-2026-09-23-wad-sese-alarm-band-v2 (1저자 봉인 · **결과 전** · 합격선이 아니다)
#:   v2 (2026-09-23): 구간은 v1 그대로, 결정문의 벽개식 계수만 일반형 n = (P_s + P_li)/4 로 (4층이면 4 · Codex BW Q5).
ALARM = {"decision": "D-2026-09-23-wad-sese-alarm-band-v2", "band_J_m2": (0.3, 0.7), "cut_suspect_above_J_m2": 1.0}


def sese_alarms(w):
    """봉인된 경보 규칙을 W 값에 건다. 경보 문장 목록 (빈 목록 = 경보 없음). 원인을 지정하지 않는다."""
    out = []
    rel = w.get("W_cleave_relaxed_PBE")
    unr = w.get("W_sep_unrelaxed_PBE")
    lo, hi = ALARM["band_J_m2"]
    if rel is None:
        out.append("판정 보류 — W_cleave_relaxed_PBE 없음 (이완 미완)")
    elif rel > ALARM["cut_suspect_above_J_m2"]:
        out.append(f"⚠ 경보: 이완 W_cleave {rel:.3f} > {ALARM['cut_suspect_above_J_m2']} J/m² — "
                   "먼저 볼 것: PS₄ 절단·wrap (원인 확정 아님)")
    elif not (lo <= rel <= hi):
        out.append(f"⚠ 경보: 이완 W_cleave {rel:.3f} J/m² 가 운영 구간 {lo}–{hi} 밖 (원인 미분류)")
    if rel is not None and unr is not None and unr < rel:
        out.append(f"⚠ 경보: 무이완 W_sep {unr:.3f} < 이완 W_cleave {rel:.3f} (PBE 끼리) — 이완이 에너지를 올렸다")
    return out


def collect(run, qe_in=None):
    """<run>/<잡>/pw.out → W_sep(무이완 · PBE / PBE+D3 2체) · W_cleave(PBE 이완). J/m².

    W = [E(s_outer) + E(li_outer) − n·E(bulk 셀)] / (2A),  n = (P_s + P_li) / P_bulk.
    Li₂S 과부족 +2/−2 가 상쇄돼 μ 가 필요 없다. 개별 γ 는 μ_Li₂S 가 있어야 해서 **내지 않는다**.
    """
    qe_in = qe_in or os.path.join(REPO, "db", "inputs", "wad_sese_control_2026_09_23")
    jobs = {j["dir"]: j for j in json.load(open(os.path.join(qe_in, "jobs.json")))["jobs"]}
    res, miss = {}, {}
    for name, j in jobs.items():
        d3 = j["calc"] == "scf"
        try:
            r = parse_pw(os.path.join(run, name, "pw.out"), j["calc"], d3)
            if r["nat"] is not None and r["nat"] != j["nat"]:
                raise SlabError(f"{name}: nat {r['nat']} ≠ 입력 {j['nat']}")
            res[name] = r
        except SlabError as e:
            miss[name] = str(e)

    def cell_area(name):
        txt = open(os.path.join(qe_in, name, "pw.in")).read().split("CELL_PARAMETERS")[1].splitlines()[1:3]
        a = np.array([float(x) for x in txt[0].split()])
        b = np.array([float(x) for x in txt[1].split()])
        return float(np.linalg.norm(np.cross(a, b)))

    def n_p(name):
        txt = open(os.path.join(qe_in, name, "pw.in")).read().split("ATOMIC_POSITIONS")[1]
        return sum(1 for ln in txt.splitlines() if ln.split()[:1] == ["P"])

    out = {"run": run, "missing": miss, "jobs": res, "W_J_m2": {}, "notes": []}
    A = cell_area("02_s_outer_scf")
    nb = n_p("01_bulk_scf")
    n = (n_p("02_s_outer_scf") + n_p("02_li_outer_scf")) / nb
    out.update(area_A2=round(A, 4), n_bulk_cells=n)
    conv = RY_J / (2 * A * 1e-20)

    def W(e_s, e_l, e_b):
        return round((e_s + e_l - n * e_b) * conv, 4)

    if all(k in res for k in ("01_bulk_scf", "02_s_outer_scf", "02_li_outer_scf")):
        b, s, l = res["01_bulk_scf"], res["02_s_outer_scf"], res["02_li_outer_scf"]
        out["W_J_m2"]["W_sep_unrelaxed_PBE"] = W(s["E_pbe_Ry"], l["E_pbe_Ry"], b["E_pbe_Ry"])
        out["W_J_m2"]["W_sep_unrelaxed_PBE_D3BJ_2body"] = W(s["E_tot_Ry"], l["E_tot_Ry"], b["E_tot_Ry"])
    if all(k in res for k in ("01_bulk_scf", "03_s_outer_relax_pbe", "03_li_outer_relax_pbe")):
        b = res["01_bulk_scf"]
        out["W_J_m2"]["W_cleave_relaxed_PBE"] = W(res["03_s_outer_relax_pbe"]["E_pbe_Ry"],
                                                 res["03_li_outer_relax_pbe"]["E_pbe_Ry"], b["E_pbe_Ry"])
    out["alarms"] = sese_alarms(out["W_J_m2"])
    out["alarm_rule"] = {"decision": ALARM["decision"], "band_J_m2": list(ALARM["band_J_m2"]),
                         "cut_suspect_above_J_m2": ALARM["cut_suspect_above_J_m2"],
                         "뜻": "합격선이 아니라 경보다 — 구간 안이어도 물리적 타당성이 입증되지 않는다"}
    big_ts = {k: v["mTS_Ry"] for k, v in res.items() if v["mTS_Ry"] is not None and abs(v["mTS_Ry"]) > 1e-4}
    if big_ts:
        out["notes"].append(f"⚠ |−TS| > 1e-4 Ry 인 잡 {big_ts} — 표면 준위가 갭을 닫았을 수 있다 (절연체 가정 점검)")
    out["notes"] += [
        "문헌 대응: Pustorino 2025 (PBE · vdW 없음 · 이완) (0.74 + 0.20)/2 ≈ 0.47 J/m² → W_cleave_relaxed_PBE 와 비교",
        "무이완 W_sep 은 이완값보다 커야 정상이다 (계획 §0′)",
        f"경보 운영값 {ALARM['band_J_m2'][0]}–{ALARM['band_J_m2'][1]} J/m² · >{ALARM['cut_suspect_above_J_m2']} "
        f"PS₄ 절단 의심 — {ALARM['decision']} (결과 전 봉인 · 합격선 아님)",
        "ΔW_ATM (3체): 미계산 — 같은 기하에서 dftd3 후처리 (D-2026-09-23-wad-d3-twobody-atm-separate)",
        "개별 γ(s_outer)·γ(li_outer): μ_Li₂S 가 필요해 내지 않는다",
    ]
    return out


# ─────────────────── 이완 점검 (경보 v2 후속 · 점검 제안 A · 2026-09-25) ───────────────────
#: 결과 전 문턱 — db/properties/wad_sese_4L_result_2026_09_25.json `다음_점검_제안_1저자_결정.A` 와 같은 값.
#:   ⛔ 결과를 보고 바꾸지 않는다 (바꾸면 그 기록과 갈린다).
RELAX_MID_THR_A = 0.3      # 가운데 층 원자 변위 max 가 이걸 넘으면 '속층 이완' 신호 (원인 후보 ②)
RELAX_VAC_TOL_A = 1.0      # 처음 슬랩 z 범위 밖으로 이만큼 넘게 나간 원자 = 진공 쪽 이탈
RELAX_MID_FRAC = 1.0 / 3   # '가운데 층' = 처음 z 범위의 가운데 1/3


def _read_positions_block(text):
    """ATOMIC_POSITIONS (angstrom) → (기호 목록, (n,3) 배열).

    'Begin final coordinates … End final coordinates' 가 있으면 **그 안만** 본다 (pw.out 통째도 된다).
    ⛔ angstrom 이 아니면 멈춘다 — bohr·crystal 을 조용히 Å 로 읽으면 변위가 통째로 틀린다.
    """
    import re
    m = re.search(r"Begin final coordinates(.*?)End final coordinates", text, re.S)
    body = m.group(1) if m else text
    h = re.search(r"ATOMIC_POSITIONS\s*[({]?\s*([A-Za-z]+)", body)
    if not h:
        raise SlabError("ATOMIC_POSITIONS 줄이 없다")
    if h.group(1).lower() != "angstrom":
        raise SlabError(f"좌표 단위가 angstrom 이 아니다 ({h.group(1)}) — 이 점검은 angstrom 만 읽는다")
    sym, xyz = [], []
    for ln in body[h.end():].splitlines()[1:]:
        p = ln.split()
        if len(p) >= 4 and re.fullmatch(r"[A-Z][a-z]?", p[0]):
            try:
                xyz.append([float(v) for v in p[1:4]])
                sym.append(p[0])
                continue
            except ValueError:
                pass
        if sym:
            break
    if not sym:
        raise SlabError("ATOMIC_POSITIONS 아래에 원자 줄이 없다")
    return sym, np.array(xyz)


def _read_cell_block(text):
    import re
    h = re.search(r"CELL_PARAMETERS\s*[({]?\s*([A-Za-z]+)", text)
    if not h or h.group(1).lower() != "angstrom":
        raise SlabError("CELL_PARAMETERS (angstrom) 가 없다")
    rows = [ln.split() for ln in text[h.end():].splitlines()[1:4]]
    return np.array([[float(v) for v in r[:3]] for r in rows])


def relax_check(pw_in_text, final_text, mid_thr=RELAX_MID_THR_A, vac_tol=RELAX_VAC_TOL_A, mid_frac=RELAX_MID_FRAC):
    """이완 전(pw.in) ↔ 이완 끝(최종 좌표) 비교 — PS₄ 온전 · 결합 짝 · 진공 이탈 · 층별 변위.

    ⛔ 이 함수가 못 하는 것
      · 원인을 정하지 않는다 — 신호만 낸다 (경보 v2 는 원인 미분류 규칙이다).
      · 에너지를 보지 않는다 — 기준 벌크 불일치의 **크기**는 벌크 이완 잡(점검 B)이 잰다.
      · 면내는 주기, z 는 비주기(진공)로 본다 — (001) 대칭 슬랩 전용.
    """
    from ase import Atoms
    cell = _read_cell_block(pw_in_text)
    s0, x0 = _read_positions_block(pw_in_text)
    s1, x1 = _read_positions_block(final_text)
    if s0 != s1:
        raise SlabError(f"원자 수·순서가 다르다 (처음 {len(s0)} · 나중 {len(s1)}) — 같은 잡의 좌표인가")
    pbc = (True, True, False)
    d = _mic(x1 - x0, cell, pbc)
    disp = np.linalg.norm(d, axis=1)
    sym = np.array(s1)
    z0 = x0[:, 2]
    zlo, zhi = float(z0.min()), float(z0.max())
    th = zhi - zlo
    lo_m, hi_m = zlo + th * (1 - mid_frac) / 2, zhi - th * (1 - mid_frac) / 2
    mid = (z0 >= lo_m) & (z0 <= hi_m)

    def partners(x):
        i, j, _, _ = _pairs(Atoms(s1, positions=x, cell=cell, pbc=pbc), "P", "S", R_PS)
        return {int(p): sorted(int(v) for v in j[i == p]) for p in np.where(sym == "P")[0]}
    p0, p1 = partners(x0), partners(x1)
    broken = {p: len(v) for p, v in p1.items() if len(v) != 4}
    swapped = [p for p in p0 if p0[p] != p1[p] and p not in broken]
    z1 = x1[:, 2]
    out_vac = [int(k) for k in np.where((z1 < zlo - vac_tol) | (z1 > zhi + vac_tol))[0]]
    edges = np.linspace(zlo, zhi + 1e-9, 9)
    prof = []
    for b in range(8):
        m = (z0 >= edges[b]) & (z0 < edges[b + 1])
        if m.any():
            prof.append({"z_from_A": round(float(edges[b] - zlo), 2), "z_to_A": round(float(edges[b + 1] - zlo), 2),
                         "n": int(m.sum()), "disp_max_A": round(float(disp[m].max()), 3),
                         "disp_mean_A": round(float(disp[m].mean()), 3)})
    mid_by_el = {el: round(float(disp[mid & (sym == el)].max()), 3) for el in sorted(set(s1)) if (mid & (sym == el)).any()}
    mid_max = float(disp[mid].max()) if mid.any() else None
    top = [{"i": int(k), "el": s1[k], "z0_rel_A": round(float(z0[k] - zlo), 2), "disp_A": round(float(disp[k]), 3)}
           for k in np.argsort(-disp)[:5]]
    flags = []
    if broken:
        flags.append(f"PS₄ 깨짐 — P {len(broken)} 개가 {R_PS} Å 안 S 수 ≠ 4 ({broken}) → 원인 후보 ③")
    if swapped:
        flags.append(f"PS₄ 결합 짝 바뀜 — P {swapped} (S 수는 4 인데 다른 S) → 원인 후보 ③")
    if out_vac:
        flags.append(f"진공 쪽 이탈 — 원자 {out_vac} 가 처음 z 범위 ± {vac_tol} Å 밖")
    if mid_max is not None and mid_max > mid_thr:
        flags.append(f"속층 이완 신호 — 가운데 1/3 원자 변위 max {mid_max:.3f} Å > {mid_thr} Å (원인 후보 ②)")
    return {"n_atoms": len(s1), "slab_z_A": [round(zlo, 3), round(zhi, 3)], "mid_band_A": [round(lo_m - zlo, 2), round(hi_m - zlo, 2)],
            "disp_max_A": round(float(disp.max()), 3), "disp_rms_A": round(float(np.sqrt((disp ** 2).mean())), 3),
            "mid_disp_max_A": round(mid_max, 3) if mid_max is not None else None, "mid_disp_max_by_element_A": mid_by_el,
            "layer_profile": prof, "top5": top, "ps4_broken": broken, "ps4_partner_changed": swapped,
            "out_to_vacuum": out_vac, "flags": flags,
            "thresholds": {"mid_disp_A": mid_thr, "vac_tol_A": vac_tol, "mid_frac": mid_frac, "R_PS_A": R_PS},
            "⛔": "신호만 낸다 — 원인 분류·판정 아님 (경보 v2 는 원인 미분류)"}


# ─────────────────────────────── selftest ───────────────────────────────
def _selftest_relax_check(ck):
    """--relax_check: 실제 4층 S 바깥 입력을 출발로, 합성 '최종 좌표' 로 양성·음성을 본다."""
    src = os.path.join(REPO, "db", "inputs", "wad_sese_control_4L_2026_09_24", "03_s_outer_relax_pbe", "pw.in")
    if not os.path.isfile(src):
        ck("relax_check: 시험 입력(4층 S 바깥 pw.in)이 repo 에 있다", False, src)
        return
    t = open(src, encoding="utf-8").read()
    sym, x = _read_positions_block(t)
    rng = np.random.default_rng(5)

    def fin(xx, unit="angstrom", drop=False):
        rows = [f"{a:2s} {p[0]:14.8f} {p[1]:14.8f} {p[2]:14.8f}" for a, p in zip(sym, xx)]
        if drop:
            rows = rows[:-1]
        return "Begin final coordinates\n\nATOMIC_POSITIONS (" + unit + ")\n" + "\n".join(rows) + "\n\nEnd final coordinates\n"
    base = x + rng.normal(0, 0.02, x.shape)
    r0 = relax_check(t, fin(base))
    ck("relax_check 양성: 작은 흔들림 → 신호 없음", not r0["flags"], r0["flags"])
    ck("relax_check: 층 8 칸 · 가운데 1/3 띠", len(r0["layer_profile"]) >= 6 and r0["mid_disp_max_A"] is not None, r0["layer_profile"])
    S = [i for i, a in enumerate(sym) if a == "S"]
    P = [i for i, a in enumerate(sym) if a == "P"]
    D = np.linalg.norm(_mic(x[S][:, None, :] - x[P][None, :, :], _read_cell_block(t), (True, True, False)), axis=2)
    s_b = S[int(np.argmin(D.min(axis=1)))]                      # P 에 붙은 S 하나
    xb = base.copy(); xb[s_b, 2] += 1.2 * np.sign(xb[s_b, 2] - x[:, 2].mean() or 1.0)
    rb = relax_check(t, fin(xb))
    ck("⛔음성: P–S 하나를 1.2 Å 떼면 PS₄ 깨짐을 잡는다", bool(rb["ps4_broken"]), rb["flags"])
    zc = x[:, 2].mean()
    li_mid = min((i for i, a in enumerate(sym) if a == "Li"), key=lambda i: abs(x[i, 2] - zc))
    xm = base.copy(); xm[li_mid, 0] += 0.5
    rm = relax_check(t, fin(xm))
    ck("⛔음성: 가운데 Li 를 0.5 Å 옮기면 속층 이완 신호", any("속층" in f for f in rm["flags"]), rm["flags"])
    top = int(np.argmax(x[:, 2]))
    xv = base.copy(); xv[top, 2] += 3.0
    rv = relax_check(t, fin(xv))
    ck("⛔음성: 바깥 원자를 3 Å 띄우면 진공 이탈을 잡는다", top in rv["out_to_vacuum"], rv["flags"])
    pa, pb = P[0], P[1]
    sa = S[int(np.argmin(D[:, P.index(pa)]))]; sb = S[int(np.argmin(D[:, P.index(pb)]))]
    xs = base.copy(); xs[[sa, sb]] = xs[[sb, sa]]
    rs = relax_check(t, fin(xs))
    ck("⛔음성: 두 PS₄ 의 S 자리를 맞바꾸면 짝 바뀜을 잡는다 (개수 검사만으로는 통과)", bool(rs["ps4_partner_changed"]) and not rs["ps4_broken"], rs["flags"])
    for name, kw in (("원자 하나 빠짐", {"drop": True}), ("단위 bohr", {"unit": "bohr"})):
        try:
            relax_check(t, fin(base, **kw)); ok = False
        except SlabError:
            ok = True
        ck(f"⛔음성: {name} → 멈춘다 (조용히 읽지 않는다)", ok)


def _selftest_collect(ck):
    """합성 pw.out 로 집계 식을 검산 (양성 + 음성)."""
    import tempfile
    qe_in = os.path.join(REPO, "db", "inputs", "wad_sese_control_2026_09_23")
    if not os.path.isfile(os.path.join(qe_in, "jobs.json")):
        print("   ⚠ 집계 시험 건너뜀 — 입력 폴더가 없다:", qe_in)
        return
    jobs = json.load(open(os.path.join(qe_in, "jobs.json")))["jobs"]
    E = {"01_bulk_scf": (-1000.0, -0.5), "02_s_outer_scf": (-3020.0, -1.4), "02_li_outer_scf": (-2979.0, -1.3),
         "03_s_outer_relax_pbe": (-3018.61, None), "03_li_outer_relax_pbe": (-2977.71, None)}

    def fake(root, skip=(), no_d3=(), unconv=(), maxstep=()):
        for j in jobs:
            if j["dir"] in skip:
                continue
            d = os.path.join(root, j["dir"])
            os.makedirs(d, exist_ok=True)
            e, ed = E[j["dir"]]
            L = [f"     number of atoms/cell      =          {j['nat']}"]
            if j["dir"] not in unconv:
                L.append("     convergence has been achieved in  12 iterations")
            L.append(f"!    total energy              =   {e:.8f} Ry")
            if ed is not None and j["dir"] not in no_d3:
                L.append(f"     DFT-D3 Dispersion         =      {ed:.8f} Ry")
            L.append("     smearing contrib. (-TS)   =      -0.00000001 Ry")
            if j["calc"] == "relax":
                if j["dir"] in maxstep:     # nstep 소진 — QE 는 이때도 JOB DONE 과 최종 좌표를 찍는다
                    L += ["     The maximum number of steps has been reached.", "End final coordinates"]
                else:
                    L += ["     bfgs converged in  20 scf cycles", "End final coordinates"]
            L.append("   JOB DONE.")
            open(os.path.join(d, "pw.out"), "w").write("\n".join(L) + "\n")

    with tempfile.TemporaryDirectory() as r:
        fake(r)
        o = collect(r, qe_in)
        A = o["area_A2"]
        conv = RY_J / (2 * A * 1e-20)
        want_d3 = round((-3020.0 - 2979.0 - 6 * -1000.0) * conv, 4)
        want_pbe = round(((-3020.0 + 1.4) + (-2979.0 + 1.3) - 6 * (-1000.0 + 0.5)) * conv, 4)
        want_rel = round((-3018.61 - 2977.71 - 6 * (-1000.0 + 0.5)) * conv, 4)
        ck("집계: n_bulk_cells = 6", o["n_bulk_cells"] == 6, o["n_bulk_cells"])
        ck("집계: W_sep PBE+D3 식", o["W_J_m2"].get("W_sep_unrelaxed_PBE_D3BJ_2body") == want_d3, o["W_J_m2"])
        ck("집계: W_sep PBE = D3 뺀 값", o["W_J_m2"].get("W_sep_unrelaxed_PBE") == want_pbe, o["W_J_m2"])
        ck("집계: W_cleave 이완 = 이완 PBE − n·벌크 PBE", o["W_J_m2"].get("W_cleave_relaxed_PBE") == want_rel,
           o["W_J_m2"])
        ck("집계: 누락 0", not o["missing"], o["missing"])
    # 경보 규칙 (봉인값) — 양성 1 · 음성 4
    ck("경보: 0.47 · 무이완 0.6 → 경보 없음", sese_alarms({"W_cleave_relaxed_PBE": 0.47, "W_sep_unrelaxed_PBE": 0.6}) == [])
    a1 = sese_alarms({"W_cleave_relaxed_PBE": 1.2, "W_sep_unrelaxed_PBE": 1.5})
    ck("⛔경보: 1.2 → PS₄ 절단 먼저 보라", len(a1) == 1 and "PS₄" in a1[0], a1)
    a2 = sese_alarms({"W_cleave_relaxed_PBE": 0.2, "W_sep_unrelaxed_PBE": 0.5})
    ck("⛔경보: 0.2 → 구간 밖 (원인 미분류)", len(a2) == 1 and "구간" in a2[0], a2)
    a3 = sese_alarms({"W_cleave_relaxed_PBE": 0.5, "W_sep_unrelaxed_PBE": 0.4})
    ck("⛔경보: 무이완 < 이완 → 경보", len(a3) == 1 and "무이완" in a3[0], a3)
    a4 = sese_alarms({"W_sep_unrelaxed_PBE": 0.5})
    ck("경보: 이완값 없음 → 판정 보류 (0 으로 두지 않는다)", len(a4) == 1 and "보류" in a4[0], a4)
    with tempfile.TemporaryDirectory() as r:
        fake(r, no_d3=("02_s_outer_scf",))
        o = collect(r, qe_in)
        ck("⛔집계: D3 줄 없는 D3 잡 → 누락 처리 · W 안 냄", "02_s_outer_scf" in o["missing"]
           and "W_sep_unrelaxed_PBE" not in o["W_J_m2"], o["missing"])
    with tempfile.TemporaryDirectory() as r:
        fake(r, maxstep=("03_li_outer_relax_pbe",))
        o = collect(r, qe_in)
        ck("⛔집계: nstep 소진 이완 → W_cleave 안 냄 (무이완 W_sep 은 낸다)",
           "W_cleave_relaxed_PBE" not in o["W_J_m2"] and "W_sep_unrelaxed_PBE" in o["W_J_m2"], o["W_J_m2"])
    with tempfile.TemporaryDirectory() as r:
        fake(r, unconv=("01_bulk_scf",))
        o = collect(r, qe_in)
        ck("⛔집계: 벌크 미수렴 → W 전부 안 냄", not o["W_J_m2"], o["W_J_m2"])


def _selftest():
    from ase import Atoms
    from ase.io import read
    n_ok, n_bad = 0, 0

    def ck(name, cond, info=""):
        nonlocal n_ok, n_bad
        if cond:
            n_ok += 1
        else:
            n_bad += 1
            print(f"  ✗ {name} {info}")

    bulk = read(BULK_DEFAULT)
    units, free, rep = scan(bulk)
    R = (units, free, rep)
    ck("벌크 PS₄ 4개 · 자유 S 4개", len(units) == 4 and len(free) == 4, (len(units), len(free)))
    ck("창 2개", len(rep["windows"]) == 2, len(rep["windows"]))
    for w in rep["windows"]:
        ck("창 폭 ≈ 2.54 Å", abs(w["width"] - 2.542) < 0.02, w["width"])
        ck("창 = Li 8 + S 2 · Cl 0", w["atoms"] == {"Li": 8, "S": 2}, w["atoms"])
        kinds = sorted(x["kind"] for x in w["cuts"])
        ck("창마다 A 1 · B 1 · 극성 ≥ 2", kinds.count("A") == 1 and kinds.count("B") == 1
           and kinds.count("polar") >= 2, kinds)
        for x in w["cuts"]:
            if x["kind"] in ("A", "B"):
                ck("보상 틈 전하 +2/+2", x["q_below"] == 2 and x["q_above"] == 2, x)
    # ── 양성: 두 종결 ──
    want = {"s_outer": {"Li": 76, "P": 12, "S": 62, "Cl": 12},      # Pustorino Li₇₆P₁₂S₆₂Cl₁₂
            "li_outer": {"Li": 68, "P": 12, "S": 58, "Cl": 12}}     # Pustorino Li₆₈P₁₂S₅₈Cl₁₂
    for term in TERMS:
        slab, meta = build_slab(bulk, term, 6, 20.0, _rep=R)
        v = validate(slab, meta, bulk, units, free)
        ck(f"{term} 검증 통과", v["ok"], {k: x for k, x in v["checks"].items() if not x["ok"]})
        ck(f"{term} 조성 = Pustorino 6층", v["checks"]["composition"]["counts"] == want[term],
           v["checks"]["composition"]["counts"])
        fe = v["checks"]["faces_equivalent"]
        ck(f"{term} 대칭연산 = x 축 C2", fe["R"] == [[1, 0, 0], [0, -1, 0], [0, 0, -1]], fe["R"])
        Rm, t = np.array(fe["R"], float), np.array(fe["t_A"], float)
        pl = place_for_qe(slab, Rm, t)
        v2 = validate(pl, meta, bulk, units, free)
        t2 = np.array(v2["checks"]["faces_equivalent"]["t_A"], float)
        c = pl.cell.array[2, 2]
        frac = t2 / np.array([pl.cell.array[0, 0], pl.cell.array[1, 1], c])
        ck(f"{term} 배치 후 C2 분수 병진 0 (mod 1)", v2["ok"] and np.allclose(frac - np.round(frac), 0, atol=1e-4),
           frac)
        # ⛔음성 ⓐ: 면 원자 하나를 0.3 Å 옮기면 양면 동일이 떨어져야 한다
        bad = slab.copy()
        bad.arrays["parent"] = slab.arrays["parent"].copy()
        bad.arrays["image"] = slab.arrays["image"].copy()
        top = int(np.argmax(bad.get_positions()[:, 2]))
        p = bad.get_positions()
        p[top, 0] += 0.3
        bad.set_positions(p)
        vb = validate(bad, meta, bulk, units, free)
        ck(f"⛔{term} 면 원자 0.3 Å 이동 → faces_equivalent 실패", not vb["checks"]["faces_equivalent"]["ok"],
           vb["checks"]["faces_equivalent"])
        # ⛔음성 ⓑ: Li 하나를 빼면 조성·전하가 떨어져야 한다
        li = [i for i, s in enumerate(slab.get_chemical_symbols()) if s == "Li"][0]
        rm = slab.copy()
        del rm[li]
        vr = validate(rm, meta, bulk, units, free)
        ck(f"⛔{term} Li 1개 제거 → 조성·전하 실패", not vr["checks"]["composition"]["ok"]
           and not vr["checks"]["formal_charge_zero"]["ok"])
        # ⛔음성 ⓒ: PS₄ S 와 자유 S 의 **자리를 맞바꾸면** 개수 검사는 통과하지만 부모 검사가 잡아야 한다
        sw = slab.copy()
        sw.arrays["parent"] = slab.arrays["parent"].copy()
        sw.arrays["image"] = slab.arrays["image"].copy()
        su, sf = ps4_units(sw)
        s_ps4 = su[next(iter(su))][0][0]
        s_free = sf[0]
        pp = sw.get_positions()
        pp[[s_ps4, s_free]] = pp[[s_free, s_ps4]]
        sw.set_positions(pp)
        vs = validate(sw, meta, bulk, units, free)
        ck(f"⛔{term} PS₄ S ↔ 자유 S 자리바꿈 → 부모 검사 실패", not vs["checks"]["ps4_intact_parent"]["ok"],
           vs["checks"]["ps4_intact_parent"])
    # ⛔음성 ⓗ: 이름표와 기하가 어긋남 — li_outer 기하(B·A)에 s_outer 이름표 → ΔLi₂S(−2 ≠ +2)로 떨어져야 한다
    #   (대칭·전하·PS₄ 는 전부 통과하는 슬랩이라, 이 검사가 없으면 종결이 뒤바뀐 파일이 조용히 나간다.
    #    2026-09-23 돌연변이 시험에서 이 요구를 지워도 초록이었다 → 이 시험을 넣었다)
    ml, mm = build_slab(bulk, "s_outer", 6, 20.0, cuts=("B", "A"), _rep=R)
    vm = validate(ml, mm, bulk, units, free)
    ck("⛔이름표 s_outer · 기하 li_outer → composition 실패", not vm["checks"]["composition"]["ok"]
       and vm["checks"]["faces_equivalent"]["ok"], vm["checks"]["composition"])
    # ⛔음성 ⓓ: 비대칭(화학량론) 슬랩 — A 아래 · A 위 → 양면 동일·조성 둘 다 실패
    asym, ma = build_slab(bulk, "asym_test", 6, 20.0, cuts=("A", "A"), _rep=R)
    va = validate(asym, ma, bulk, units, free)
    ck("⛔비대칭 슬랩 → faces_equivalent 실패", not va["checks"]["faces_equivalent"]["ok"],
       va["checks"]["faces_equivalent"])
    ck("⛔비대칭 슬랩 = 화학량론(ΔLi₂S 0)", va["checks"]["composition"]["delta_Li2S"] == 0,
       va["checks"]["composition"])
    ck("⛔비대칭 슬랩 → 면 조성 불일치", not va["checks"]["face_composition_equal"]["ok"])
    # ⛔음성 ⓔ: 순진한 z 절단(PS₄ 층 한가운데) → PS₄ 검사 실패
    try:
        nv, mn = build_slab(bulk, "naive_test", 6, 20.0, cuts=("naive", "naive"), _rep=R)
        vn = validate(nv, mn, bulk, units, free)
        ck("⛔순진한 절단 → ps4_intact_parent 실패", not vn["checks"]["ps4_intact_parent"]["ok"],
           vn["checks"]["ps4_intact_parent"])
    except SlabError as e:
        ck("⛔순진한 절단 → 거부", True, str(e))
    # ⛔음성 ⓕ: 극성 절단은 만들지 않는다
    try:
        build_slab(bulk, "polar_test", 6, 20.0, cuts=("polar", "polar"), _rep=R)
        ck("⛔극성 절단 → 거부", False, "만들어졌다")
    except SlabError:
        ck("⛔극성 절단 → 거부", True)
    # ⛔음성 ⓖ: 러너(build_ncm_1L)의 LiNiO₂ — R-centering 없는 4 좌표 → Ni 주변 O 0
    #   (run_cathode_interface.py 의 좌표를 pymatgen 없이 그대로 옮겼다)
    a, c = 2.878, 14.19
    Ch = np.array([[a, 0, 0], [-a / 2, a * np.sqrt(3) / 2, 0], [0, 0, c]])
    fr = np.array([[0, 0, 0.5], [0, 0, 0], [0, 0, 0.2584], [0, 0, 0.7416]])
    bad_ncm = Atoms(["Li", "Ni", "O", "O"], scaled_positions=fr, cell=Ch, pbc=True)
    co = coordination(bad_ncm, "Ni", "O", 2.5)
    ck("⛔러너 LiNiO₂ → Ni–O 6배위 아님", all(n != 6 for _, n, _ in co), co)
    # 양성 대조: R-centering 을 전개하면 Ni–O 1.97 Å × 6
    rc = [np.zeros(3), np.array([2 / 3, 1 / 3, 1 / 3]), np.array([1 / 3, 2 / 3, 2 / 3])]
    frg, spg = [], []
    for sh in rc:
        for s, f in zip(["Li", "Ni", "O", "O"], fr):
            frg.append((f + sh) % 1.0)
            spg.append(s)
    good_ncm = Atoms(spg, scaled_positions=np.array(frg), cell=Ch, pbc=True)
    co2 = coordination(good_ncm, "Ni", "O", 2.5)
    ck("R 전개 LiNiO₂ → Ni–O 6배위 (양성 대조)", all(n == 6 for _, n, _ in co2), co2)
    # QE 입력: D3 2체 명시 · relax 는 분산 끔
    slab, meta = build_slab(bulk, "s_outer", 6, 20.0, _rep=R)
    txt = qe_input(slab, "slab", "t", (4, 4, 1), "/x", "scf")
    ck("QE scf 입력에 dftd3_threebody = .false. 명시", "dftd3_threebody = .false." in txt
       and "dftd3_version = 4" in txt)
    txr = qe_input(slab, "slab", "t", (4, 4, 1), "/x", "relax")
    ck("QE relax 입력은 vdw_corr='none' (PBE)", "vdw_corr = 'none'" in txr and "grimme" not in txr)
    ck("QE 입력 원자 수 일치", f"nat = {len(slab)}" in txt)
    _selftest_collect(ck)
    _selftest_relax_check(ck)
    print(f"{'✅' if n_bad == 0 else '⛔'} se_sym_slab selftest {n_ok}/{n_ok + n_bad} 통과")
    return 0 if n_bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--bulk", default=BULK_DEFAULT)
    ap.add_argument("--scan", action="store_true", help="창·틈·전하만 찍는다 (파일 안 씀)")
    ap.add_argument("--layers", type=int, default=6, help="PS₄ 층 수 (기본 6 = Pustorino 2025)")
    ap.add_argument("--vacuum", type=float, default=20.0, help="진공 합계 [Å]")
    ap.add_argument("--tol_sym", type=float, default=0.01, help="양면 동일 허용 편차 [Å]")
    ap.add_argument("--out", help="구조 폴더 (.vasp + .xyz + manifest.json)")
    ap.add_argument("--qe_out", help="SE|SE 대조 QE 입력 폴더 (잡 5개 + jobs.json)")
    ap.add_argument("--pseudo_dir", default="/data/work/pseudo", help="QE 입력에 적을 서버 경로")
    ap.add_argument("--kslab", default="4 4 1", help="슬랩 k (기본 = comp1 k444 의 면내 밀도)")
    ap.add_argument("--kbulk", default="4 4 4")
    ap.add_argument("--collect", metavar="RUN", help="실행 폴더의 pw.out 들 → W (J/m²) · <RUN>/sese_result.json")
    ap.add_argument("--qe_in", help="--collect 가 대조할 입력 폴더 (기본 db/inputs/wad_sese_control_2026_09_23)")
    ap.add_argument("--relax_check", nargs=2, metavar=("PW_IN", "FINAL"),
                    help="이완 전 pw.in ↔ 최종 좌표(pw.out 또는 붙여넣은 Begin/End final coordinates) — PS₄ · 짝 · 진공 · 층별 변위 (판정 아님)")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if a.relax_check:
        r = relax_check(open(a.relax_check[0], encoding="utf-8").read(), open(a.relax_check[1], encoding="utf-8", errors="ignore").read())
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 0 if not r["flags"] else 2
    if a.collect:
        o = collect(a.collect, a.qe_in)
        with open(os.path.join(a.collect, "sese_result.json"), "w", encoding="utf-8") as f:
            json.dump(o, f, ensure_ascii=False, indent=1)
        print(json.dumps({k: o[k] for k in ("W_J_m2", "alarms", "missing", "area_A2", "n_bulk_cells")},
                         ensure_ascii=False, indent=1))
        for n_ in o["notes"]:
            print("  ·", n_)
        return 0
    from ase.io import read
    if a.scan:
        _, _, rep = scan(read(a.bulk))
        print(json.dumps(rep, ensure_ascii=False, indent=1))
        return 0
    if not a.out:
        ap.error("--out 이 필요하다 (또는 --scan / --selftest)")
    man = write_outputs(a.out, a.bulk, a.layers, a.vacuum, a.tol_sym, a.qe_out, a.pseudo_dir,
                        tuple(int(x) for x in a.kslab.split()), tuple(int(x) for x in a.kbulk.split()))
    for term, s in man["slabs"].items():
        fe = s["validation"]["faces_equivalent"]
        print(f"✓ {term:9s} {s['formula']:16s} {s['nat']:4d}원자 · 두께 {s['thickness_A']:.2f} Å · "
              f"c {s['c_A']:.2f} Å · C2 편차 {fe['max_dev_A']:.1e} Å · 검증 {len(s['validation'])}/{len(s['validation'])}")
    print("  " + man["cleavage_identity"])
    if a.qe_out:
        print(f"→ QE 입력: {a.qe_out}/jobs.json")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SlabError as e:
        print(f"⛔ {e}")
        sys.exit(2)
