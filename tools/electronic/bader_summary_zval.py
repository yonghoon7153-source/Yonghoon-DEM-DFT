#!/usr/bin/env python3
"""bader_summary_zval.py — ACF.dat → 원소별 (+ 자리별) net charge (ZVAL 규약).

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

2026-10-19 확장 (Nd Q3 · 결정 D-2026-10-19-nd-q23-ppswap-structure) — 옛 쓰임은 그대로 돈다:
  · --struct 에 QE 입력 (.in) 을 받는다 — CELL_PARAMETERS · ATOMIC_POSITIONS · ATOMIC_SPECIES · pseudo_dir
  · --zval_from_upf [DIR] — ZVAL 을 UPF 의 z_valence 에서 읽는다 (DIR 없으면 QE 입력의 pseudo_dir).
    표에 있는 원소가 UPF 와 다르면 **멈춘다** (pseudo 가 바뀌었는데 표를 안 고친 경우) · 표에 없는 원소는 UPF 로 채운다.
  · --sites CSV — 원자마다 자리 분류 · net · N_bader · Bader 부피 (Å³) · N_bader/부피 (e/Å³) · 가장 가까운 Nd 거리.
    분류 거리는 아래 R_* 상수 — **Nd Q3 결과를 보기 전에 박았다** (카드 ndo_lpscl16_site_stability §2 Q3 범주:
    S(PS₄·Nd 이웃) · S(PS₄·Li 만) · S(자유) · O(P–O) · Nd · Li · P).
  · 부피 단위는 ACF 부피 합 = 셀 부피 로 가른다 (Bohr³ 이면 ×0.148185) — 둘 다 2 % 안에 안 맞으면 멈춘다.

  python3 tools/electronic/bader_summary_zval.py --acf ACF.dat --struct kprobe.in --zval_from_upf \
      --sites nd_bader_sites.csv --out nd_bader_summary.json

⛔ 이 도구가 못 하는 것
  · Bader 분할을 하지 않는다 (bader 프로그램 몫) · 밀도가 plot_num 17 인지 모른다 — ZVAL 규약은 17 일 때만 맞다 (호출자 책임).
  · 자리 분류는 **거리 하나**로 한다 — 배위 각도 · 결합 차수 · 2 차 이웃은 안 본다. 문턱 근처 (±0.1 Å) 원자는 CSV 의
    거리 열로 사람이 본다.
  · 셀이 없는 xyz 로는 --sites 를 못 한다 (거리에 주기 경계가 필요하다) — QE 입력이나 POSCAR 를 준다.
  · 호스트 (도핑 전) 와의 자리별 비교는 못 한다 — 기존 호스트 표 (bader_ae_modelc_LPSCl16.csv) 는 **원소 평균**뿐이다.
"""
import argparse
import itertools
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# kjpaw_psl 세트의 가전자 수 — pseudo 를 바꾸면 여기도 바꿔야 한다 (--zval_from_upf 가 대조한다).
# Nd = Nd.pbe-spdn-kjpaw_psl.1.0.0.UPF (4f-in-core · 5s 5p 5d 6s = 11) — 2026-09-16 PP 교체 카드.
ZVAL = {"Li": 3, "P": 5, "S": 6, "Cl": 7, "O": 6, "B": 3, "Nd": 11}
REF = {"b2o3":    {"Li": 0.881, "P": 4.691, "S": -1.80, "Cl": -0.914},
       "LPSCl16": {"Li": 0.883, "P": 4.340, "S": -1.736, "Cl": -0.918}}

BOHR = 0.529177210903
BOHR3 = BOHR ** 3
# 자리 분류 거리 (Å) — 2026-10-19 결과 전 (6 월 Nd@Li 실측: Nd–S 2.62–3.18 · Nd–O 2.48 · 2.61 · Nd–Cl 2.75–2.80 · P–O 1.55–1.60 · P–S 2.02–2.10)
R_PS = 2.4     # P–S 결합 (PS₄ 모서리) — 이 안에 P 가 없으면 '자유 S'
R_PO = 1.9     # P–O 결합
R_NDX = 3.3    # Nd–S · Nd–Cl 첫 배위권
R_NDO = 2.9    # Nd–O 첫 배위권


def _vec(s):
    return [float(x) for x in s.split()[:3]]


def read_qe_input(path):
    """QE 입력 → (symbols, cart Å, cell Å 3×3, species→UPF, pseudo_dir)."""
    t = Path(path).read_text()
    lines = t.splitlines()
    m = re.search(r"pseudo_dir\s*=\s*['\"]([^'\"]+)['\"]", t)
    pdir = m.group(1) if m else None
    m = re.search(r"\bnat\s*=\s*(\d+)", t)
    nat = int(m.group(1)) if m else None
    upf, cell, sym, raw, mode = {}, None, [], [], None
    i = 0
    while i < len(lines):
        L = lines[i].strip()
        if L.upper().startswith("ATOMIC_SPECIES"):
            j = i + 1
            while j < len(lines) and len(lines[j].split()) >= 3 and re.match(r"^[A-Z][a-z]?\w*$", lines[j].split()[0]):
                p = lines[j].split(); upf[p[0]] = p[2]; j += 1
            i = j; continue
        if L.upper().startswith("CELL_PARAMETERS"):
            unit = (re.findall(r"[a-z]+", L.lower().replace("cell_parameters", "")) or ["bohr"])[0]
            v = [_vec(lines[i + k]) for k in (1, 2, 3)]
            if unit.startswith("ang"):
                cell = v
            elif unit.startswith("bohr"):
                cell = [[x * BOHR for x in r] for r in v]
            else:
                raise SystemExit(f"CELL_PARAMETERS 단위 '{unit}' 는 못 읽는다 (angstrom · bohr 만)")
            i += 4; continue
        if L.upper().startswith("ATOMIC_POSITIONS"):
            mode = (re.findall(r"[a-z]+", L.lower().replace("atomic_positions", "")) or ["alat"])[0]
            j = i + 1
            while j < len(lines):
                p = lines[j].split()
                if len(p) < 4 or not re.match(r"^[A-Z][a-z]?$", p[0]):
                    break
                sym.append(p[0]); raw.append([float(x) for x in p[1:4]]); j += 1
            i = j; continue
        i += 1
    if cell is None or not sym:
        raise SystemExit(f"{path}: CELL_PARAMETERS · ATOMIC_POSITIONS 를 못 찾았다")
    if nat is not None and nat != len(sym):
        raise SystemExit(f"{path}: nat {nat} ≠ 위치 줄 {len(sym)}")
    if mode.startswith("crystal"):
        cart = [[sum(f[k] * cell[k][c] for k in range(3)) for c in range(3)] for f in raw]
    elif mode.startswith("ang"):
        cart = raw
    elif mode.startswith("bohr"):
        cart = [[x * BOHR for x in r] for r in raw]
    else:
        raise SystemExit(f"ATOMIC_POSITIONS 단위 '{mode}' 는 못 읽는다 (crystal · angstrom · bohr 만)")
    return sym, cart, cell, upf, pdir


def read_poscar(path):
    L = Path(path).read_text().splitlines()
    s = float(L[1].split()[0])
    cell = [[s * x for x in _vec(L[k])] for k in (2, 3, 4)]
    sp, cnt = L[5].split(), [int(x) for x in L[6].split()]
    sym = [e for e, n in zip(sp, cnt) for _ in range(n)]
    k = 7 + (1 if L[7].strip()[:1].lower() == "s" else 0)
    direct = L[k].strip()[:1].lower() == "d"
    raw = [_vec(L[k + 1 + n]) for n in range(len(sym))]
    cart = ([[sum(f[a] * cell[a][c] for a in range(3)) for c in range(3)] for f in raw] if direct
            else [[s * x for x in r] for r in raw])
    return sym, cart, cell


def read_struct(path):
    """→ (symbols, cart|None, cell|None, upf, pseudo_dir)."""
    p = str(path)
    if p.endswith(".xyz"):
        L = Path(p).read_text().splitlines()
        nat = int(L[0].split()[0])
        return [ln.split()[0] for ln in L[2:2 + nat]], None, None, {}, None
    if p.endswith(".in") or "ATOMIC_POSITIONS" in Path(p).read_text()[:200000]:
        return read_qe_input(p)
    sym, cart, cell = read_poscar(p)
    return sym, cart, cell, {}, None


def read_symbols(path):
    return read_struct(path)[0]


def upf_zval(path):
    t = Path(path).read_text(errors="replace")[:200000]
    m = re.search(r'z_valence\s*=\s*"\s*([0-9.eEdD+-]+)\s*"', t)
    if m:
        return float(m.group(1).replace("d", "e").replace("D", "e"))
    m = re.search(r"^\s*([0-9.eEdD+-]+)\s+Z valence", t, re.M)
    if m:
        return float(m.group(1).replace("d", "e").replace("D", "e"))
    raise SystemExit(f"{path}: z_valence 를 못 읽었다")


def zval_table(sym, upf, pdir, table=ZVAL):
    """UPF z_valence 로 ZVAL 을 정한다 — 표에 있는 원소가 다르면 멈춘다."""
    out, log = {}, {}
    for e in sorted(set(sym)):
        if e not in upf:
            raise SystemExit(f"--zval_from_upf: {e} 의 UPF 가 ATOMIC_SPECIES 에 없다")
        z = upf_zval(Path(pdir) / upf[e])
        if abs(z - round(z)) > 1e-6:
            raise SystemExit(f"{upf[e]}: z_valence {z} 가 정수가 아니다")
        z = int(round(z))
        if e in table and table[e] != z:
            raise SystemExit(f"ZVAL 표 {e}={table[e]} ≠ UPF {upf[e]} z_valence {z} — pseudo 가 바뀌었다. 표를 고치거나 pseudo 를 확인할 것")
        out[e] = z; log[e] = f"{upf[e]} → {z}"
    return out, log


def _inv3(m):
    a, b, c = m
    det = (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0]))
    if abs(det) < 1e-12:
        raise SystemExit("셀 행렬이 특이하다")
    inv = [[(b[1] * c[2] - b[2] * c[1]) / det, (a[2] * c[1] - a[1] * c[2]) / det, (a[1] * b[2] - a[2] * b[1]) / det],
           [(b[2] * c[0] - b[0] * c[2]) / det, (a[0] * c[2] - a[2] * c[0]) / det, (a[2] * b[0] - a[0] * b[2]) / det],
           [(b[0] * c[1] - b[1] * c[0]) / det, (a[1] * c[0] - a[0] * c[1]) / det, (a[0] * b[1] - a[1] * b[0]) / det]]
    return inv, abs(det)


def mic_dist(r1, r2, cell, inv):
    """최소 이미지 거리 (Å) — 분율 차를 감은 뒤 ±1 이미지 27 개를 다 본다 (기울어진 셀에서 감기만으로는 틀린다)."""
    d = [r2[c] - r1[c] for c in range(3)]
    f = [sum(d[c] * inv[c][k] for c in range(3)) for k in range(3)]
    f = [x - round(x) for x in f]
    best = 1e30
    for s in itertools.product((-1, 0, 1), repeat=3):
        g = [f[k] + s[k] for k in range(3)]
        v = [sum(g[k] * cell[k][c] for k in range(3)) for c in range(3)]
        best = min(best, (v[0] ** 2 + v[1] ** 2 + v[2] ** 2) ** 0.5)
    return best


def classify(sym, cart, cell):
    """원자마다 (범주, 가장 가까운 Nd 거리 Å | None)."""
    inv, _ = _inv3(cell)
    idx = defaultdict(list)
    for i, s in enumerate(sym):
        idx[s].append(i)
    near = lambda i, e, r: any(mic_dist(cart[i], cart[j], cell, inv) <= r for j in idx[e] if j != i)
    out = []
    for i, s in enumerate(sym):
        dnd = min((mic_dist(cart[i], cart[j], cell, inv) for j in idx["Nd"] if j != i), default=None)
        if s == "S":
            cat = ("S_PS4" if near(i, "P", R_PS) else "S_free") + ("_nearNd" if dnd is not None and dnd <= R_NDX else "")
        elif s == "O":
            cat = ("O_P" if near(i, "P", R_PO) else "O_free") + ("_nearNd" if dnd is not None and dnd <= R_NDO else "")
        elif s == "Cl":
            cat = "Cl" + ("_nearNd" if dnd is not None and dnd <= R_NDX else "")
        elif s == "P":
            cat = "P_withO" if near(i, "O", R_PO) else "P_S4"
        else:
            cat = s
        out.append((cat, dnd))
    return out


def read_acf(path):
    rows = [l.split() for l in open(path) if re.match(r"^\s*\d+\s", l)]
    return [(float(r[4]), float(r[6]) if len(r) > 6 else None) for r in rows]


def vol_factor(vols, cell_vol):
    s = sum(vols)
    if abs(s * BOHR3 - cell_vol) / cell_vol < 0.02:
        return BOHR3, "bohr3"
    if abs(s - cell_vol) / cell_vol < 0.02:
        return 1.0, "ang3"
    raise SystemExit(f"Bader 부피 합 {s:.2f} 가 셀 부피 {cell_vol:.2f} Å³ 와 Å³·Bohr³ 어느 쪽으로도 2 % 안에 안 맞는다 — "
                     "진공 부피가 있거나 다른 구조의 ACF 다")


def summarize(acf_rows, sym, zv, cart=None, cell=None, sites_csv=None):
    if len(acf_rows) != len(sym):
        raise SystemExit(f"원자 수 불일치: ACF {len(acf_rows)} vs 구조 {len(sym)} — 같은 구조로 돈 게 맞는지 확인")
    miss = sorted({s for s in sym if s not in zv})
    if miss:
        raise SystemExit(f"ZVAL 미등록 원소: {miss} — 이 스크립트의 ZVAL 표에 추가하거나 --zval_from_upf")
    per = defaultdict(list)
    for s, (q, _) in zip(sym, acf_rows):
        per[s].append(zv[s] - q)
    res = {"method": ("AE **valence** density plot_num=17, PAW kjpaw_psl. "
                      "net = ZVAL - N_bader (NOT Z - N_bader)."),
           "zval_used": {k: zv[k] for k in sorted(per)},
           "per_species": {k: {"n": len(v), "mean": round(sum(v) / len(v), 3),
                               "min": round(min(v), 3), "max": round(max(v), 3)}
                           for k, v in sorted(per.items())}}
    if sites_csv is not None:
        if cart is None or cell is None:
            raise SystemExit("--sites 에는 셀이 있는 구조 (QE 입력 · POSCAR) 가 필요하다 — xyz 는 주기 경계를 모른다")
        if any(v is None for _, v in acf_rows):
            raise SystemExit("ACF.dat 에 부피 열이 없다 — --sites 를 못 한다")
        _, cvol = _inv3(cell)
        fac, unit = vol_factor([v for _, v in acf_rows], cvol)
        cats = classify(sym, cart, cell)
        rows, byc = [], defaultdict(list)
        for i, (s, (q, v), (c, dnd)) in enumerate(zip(sym, acf_rows, cats)):
            va = v * fac
            r = {"index": i + 1, "element": s, "category": c, "net_e": round(zv[s] - q, 4), "N_bader_e": round(q, 4),
                 "V_bader_A3": round(va, 3), "N_per_V_e_A3": round(q / va, 5) if va > 0 else None,
                 "d_Nd_min_A": round(dnd, 3) if dnd is not None else None}
            rows.append(r); byc[c].append(r)
        cols = list(rows[0])
        Path(sites_csv).write_text(",".join(cols) + "\n" + "\n".join(
            ",".join("" if r[k] is None else str(r[k]) for k in cols) for r in rows) + "\n")
        mean = lambda xs: round(sum(xs) / len(xs), 4)
        res["sites"] = {"csv": str(sites_csv), "ACF_volume_unit": unit, "cell_volume_A3": round(cvol, 3),
                        "rules_A": {"R_PS": R_PS, "R_PO": R_PO, "R_NdX": R_NDX, "R_NdO": R_NDO,
                                    "note": "2026-10-19 Nd Q3 결과 전에 박은 거리 · 거리 하나로 분류 (각도 안 봄)"},
                        "per_category": {c: {"n": len(v), "net_mean": mean([r["net_e"] for r in v]),
                                             "net_min": min(r["net_e"] for r in v), "net_max": max(r["net_e"] for r in v),
                                             "V_mean_A3": mean([r["V_bader_A3"] for r in v]),
                                             "N_per_V_mean_e_A3": mean([r["N_per_V_e_A3"] for r in v])}
                                         for c, v in sorted(byc.items())}}
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--acf")
    ap.add_argument("--struct")
    ap.add_argument("--out", default=None)
    ap.add_argument("--zval_from_upf", nargs="?", const="", default=None,
                    help="UPF 의 z_valence 로 ZVAL 을 정한다 (값 없으면 QE 입력의 pseudo_dir)")
    ap.add_argument("--sites", default=None, help="원자별 자리 분류 CSV 경로 (셀이 있는 구조 필요)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.acf and a.struct):
        ap.error("--acf · --struct 가 필요하다")

    sym, cart, cell, upf, pdir = read_struct(a.struct)
    zv, zlog = dict(ZVAL), None
    if a.zval_from_upf is not None:
        d = a.zval_from_upf or pdir
        if not d:
            raise SystemExit("--zval_from_upf: 디렉터리를 주거나 QE 입력에 pseudo_dir 이 있어야 한다")
        z2, zlog = zval_table(sym, upf, d)
        zv.update(z2)
    res = summarize(read_acf(a.acf), sym, zv, cart, cell, a.sites)
    if zlog:
        res["zval_from_upf"] = zlog
    print("원소별 net charge (ZVAL − N_bader):")
    for k, v in res["per_species"].items():
        print(f"  {k:3s} n={v['n']:3d}  {v['mean']:+.3f}  [{v['min']:+.3f}, {v['max']:+.3f}]")
    if "sites" in res:
        print(f"\n자리별 (부피 단위 {res['sites']['ACF_volume_unit']} → Å³):")
        for c, v in res["sites"]["per_category"].items():
            print(f"  {c:16s} n={v['n']:3d}  net {v['net_mean']:+.3f} [{v['net_min']:+.3f}, {v['net_max']:+.3f}]"
                  f"  V {v['V_mean_A3']:.2f} Å³  N/V {v['N_per_V_mean_e_A3']:.4f} e/Å³")
    print("\n같은 방법(AE plot_num=17 + kjpaw) 비교 상대 (원소 평균):")
    for name, d in REF.items():
        print(f"  {name:9s} " + " · ".join(f"{k} {v:+.3f}" for k, v in d.items()))
    bad = [k for k, v in res["per_species"].items() if abs(v["mean"]) > 8]
    if bad:
        print(f"\n⛔ {bad} 의 절대값이 8 e 를 넘는다 — ZVAL 표가 틀렸을 가능성이 크다.")
    if a.out:
        Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n")
        print(f"\n→ {a.out}")


def selftest():
    import tempfile
    ok = [0, 0]

    def ck(name, cond, info=""):
        ok[0 if cond else 1] += 1
        print(f"  {'✓' if cond else '✗'} {name}" + ("" if cond else f"  {info}"))

    def raises(fn):
        try:
            fn()
        except SystemExit:
            return True
        return False

    T = Path(tempfile.mkdtemp(prefix="bader_st_"))
    # ① 손으로 만든 셀 (입방 10 Å) — 분류 기대값이 정해진 배치
    cell = [[10.0, 0, 0], [0, 10.0, 0], [0, 0, 10.0]]
    atoms = [("P", (0.2, 0.0, 0.0)), ("S", (2.25, 0.0, 0.0)), ("S", (8.15, 0.0, 0.0)),   # 둘째 S 는 주기 경계 너머 P–S 2.05
             ("O", (0.2, 0.0, 1.75)),                                                     # P–O 1.75 · Nd 멀다
             ("Nd", (5.0, 5.0, 5.0)), ("S", (5.0, 5.0, 2.2)),                             # 자유 S · Nd 2.8
             ("Cl", (7.5, 5.0, 5.0)), ("Cl", (5.0, 9.0, 5.0)),                            # Nd 2.5 · Nd 4.0
             ("P", (5.0, 2.0, 7.0)), ("S", (5.0, 2.0, 5.0)), ("O", (5.0, 2.0, 8.6)),     # S: P 2.0 · Nd 3.0 → PS4_nearNd · O: P 1.6 · Nd 4.4
             ("Li", (8.0, 8.0, 8.0))]
    sym = [e for e, _ in atoms]; cart = [list(r) for _, r in atoms]
    cats = [c for c, _ in classify(sym, cart, cell)]
    want = ["P_withO", "S_PS4", "S_PS4", "O_P", "Nd", "S_free_nearNd", "Cl_nearNd", "Cl", "P_withO", "S_PS4_nearNd", "O_P", "Li"]
    ck("분류 = 손으로 정한 기대값 (주기 경계 너머 P–S · 자유 S · Nd 이웃 S/Cl · P–O)", cats == want, f"{cats}")
    # ①b 셀 밖 좌표 (vc-relax 출력처럼 분율 1.8 · −0.6) — 감기 없이 ±1 이미지만 보면 놓친다
    cart_out = [list(r) for r in cart]
    cart_out[2] = [18.15, 0.0, 0.0]          # = 8.15 + 10 (분율 1.815) · P–S 여전히 2.05
    cart_out[9] = [5.0, 2.0, -15.0]          # = 5.0 − 20 (분율 −1.5) · P 2.0 · Nd 3.0
    cats_out = [c for c, _ in classify(sym, cart_out, cell)]
    ck("셀 밖 좌표 (분율 1.8 · −1.5) 도 같은 분류 — 감고 나서 ±1 이미지", cats_out == want, f"{cats_out}")
    # ② 기울어진 60° 셀에서 MIC = 125 이미지 전수
    c60 = [[6.928, 0, 0], [3.464, 6.0, 0], [3.464, 2.0, 5.657]]
    inv, _ = _inv3(c60)
    import random
    random.seed(7)
    bad = 0
    for _ in range(300):
        f1 = [random.random() for _ in range(3)]; f2 = [random.random() for _ in range(3)]
        r1 = [sum(f1[k] * c60[k][c] for k in range(3)) for c in range(3)]
        r2 = [sum(f2[k] * c60[k][c] for k in range(3)) for c in range(3)]
        bf = min(sum((r2[c] + sum(s[k] * c60[k][c] for k in range(3)) - r1[c]) ** 2 for c in range(3)) ** 0.5
                 for s in itertools.product(range(-2, 3), repeat=3))
        bad += abs(bf - mic_dist(r1, r2, c60, inv)) > 1e-9
    ck("60° 셀 최소 이미지 = 125 이미지 전수 (300 쌍)", bad == 0, f"어긋남 {bad}")
    # ③ 부피 단위: Bohr³ · Å³ 판별 · 둘 다 아니면 멈춤
    cv = 1000.0
    vb = [cv / BOHR3 / len(sym)] * len(sym)
    ck("부피 단위 Bohr³ 판별", vol_factor(vb, cv)[1] == "bohr3")
    ck("부피 단위 Å³ 판별", vol_factor([cv / len(sym)] * len(sym), cv)[1] == "ang3")
    ck("⛔음성: 부피 합이 셀과 안 맞으면 멈춘다", raises(lambda: vol_factor([1.0] * len(sym), cv)))
    # ④ ZVAL — UPF v2 · v1 형식 읽기 · 표와 다르면 멈춤 · 표에 없는 원소는 채움
    (T / "Nd.upf").write_text('<PP_HEADER\n   z_valence="1.100000000000e+01"\n/>')
    (T / "S.upf").write_text('<PP_HEADER z_valence="6.0" />')
    (T / "Xx.upf").write_text("  4.00000000000    Z valence\n")
    (T / "Sbad.upf").write_text('<PP_HEADER z_valence="4.0" />')
    z, _ = zval_table(["Nd", "S", "Xx"], {"Nd": "Nd.upf", "S": "S.upf", "Xx": "Xx.upf"}, T)
    ck("UPF z_valence 읽기 (v2 지수 · v1 줄) · 표에 없는 원소 채움", z == {"Nd": 11, "S": 6, "Xx": 4}, f"{z}")
    ck("⛔음성: 표 (S=6) 와 UPF (4) 가 다르면 멈춘다", raises(lambda: zval_table(["S"], {"S": "Sbad.upf"}, T)))
    ck("⛔음성: ATOMIC_SPECIES 에 없는 원소면 멈춘다", raises(lambda: zval_table(["Nd"], {}, T)))
    # ⑤ summarize — net = ZVAL − N · 자리 CSV · 원자 수 · 셀 없음 · ZVAL 없음
    acf = [(ZVAL[s] - 0.5, cv / BOHR3 / len(sym)) for s in sym]       # net 전부 +0.5
    csvp = T / "sites.csv"
    r = summarize(acf, sym, dict(ZVAL), cart, cell, csvp)
    ck("net = ZVAL − N_bader (전부 +0.5)", all(abs(v["mean"] - 0.5) < 1e-9 for v in r["per_species"].values()))
    ck("자리 CSV 행 수 = 원자 수 · 범주 = 분류", len(csvp.read_text().splitlines()) == len(sym) + 1
       and set(r["sites"]["per_category"]) == set(want))
    ck("⛔음성: 원자 수 다르면 멈춘다", raises(lambda: summarize(acf[:-1], sym, dict(ZVAL))))
    ck("⛔음성: --sites 인데 셀 없으면 (xyz) 멈춘다", raises(lambda: summarize(acf, sym, dict(ZVAL), None, None, csvp)))
    ck("⛔음성: ZVAL 없는 원소면 멈춘다", raises(lambda: summarize([(1.0, 1.0)], ["Xq"], dict(ZVAL))))
    # ⑥ QE 입력 읽기 (crystal · angstrom) = 같은 데카르트 · 옛 xyz 경로 그대로
    qin = T / "x.in"
    fr = [[sum(cart[i][c] * _inv3(cell)[0][c][k] for c in range(3)) for k in range(3)] for i in range(len(sym))]
    qin.write_text("&CONTROL\n pseudo_dir='" + str(T) + "'\n/\n&SYSTEM\n nat = %d\n/\nATOMIC_SPECIES\n" % len(sym)
                   + "".join(f"  {e} 1.0 {e}.upf\n" for e in sorted(set(sym)))
                   + "CELL_PARAMETERS angstrom\n" + "".join("  %f %f %f\n" % tuple(v) for v in cell)
                   + "ATOMIC_POSITIONS crystal\n" + "".join(f"  {e} {f[0]:.10f} {f[1]:.10f} {f[2]:.10f}\n" for e, f in zip(sym, fr))
                   + "K_POINTS automatic\n 1 1 1 0 0 0\n")
    s2, c2, cl2, up2, pd2 = read_struct(qin)
    ck("QE 입력 (crystal) 읽기 = 같은 원자 · 데카르트 · pseudo_dir",
       s2 == sym and max(abs(c2[i][k] - cart[i][k]) for i in range(len(sym)) for k in range(3)) < 1e-6 and pd2 == str(T))
    xyz = T / "x.xyz"
    xyz.write_text(f"{len(sym)}\n\n" + "".join(f"{e} {r[0]} {r[1]} {r[2]}\n" for e, r in zip(sym, cart)))
    ck("옛 xyz 경로 — 기호만 · 셀 없음", read_struct(xyz)[0] == sym and read_struct(xyz)[2] is None)
    qbad = T / "bad.in"
    qbad.write_text(qin.read_text().replace(f"nat = {len(sym)}", f"nat = {len(sym) + 1}"))
    ck("⛔음성: nat ≠ 위치 줄 수면 멈춘다", raises(lambda: read_struct(qbad)))
    print(f"{'✅' if ok[1] == 0 else '⛔'} bader_summary_zval selftest {ok[0]}/{ok[0] + ok[1]} 통과")
    return 0 if ok[1] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
