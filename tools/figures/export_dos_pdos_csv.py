#!/usr/bin/env python3
"""export_dos_pdos_csv.py — clean, figure-matching DOS/PDOS CSV.
Reads a *_pdos_compact.csv (E-EF, total, <elements>), trims to the valence
window (drops Li-1s semicore etc.), Gaussian-broadens each column, reorders
columns, and writes a tidy CSV for Origin re-plot. Matches the 0.15 eV figures.

Usage:
  python3 export_dos_pdos_csv.py --csv docs/figures/modelc_pdos_compact.csv \
     --out docs/figures/dos_pdos_smooth/modelc_dos_pdos_0.15.csv \
     --order S P Cl Li --gap 2.10 --label "modelC (LPSCl1.6)"
"""
import argparse, csv, pathlib
import numpy as np
try:
    from scipy.ndimage import gaussian_filter1d
    def smooth(y, s_pts): return gaussian_filter1d(y, s_pts)
except Exception:
    def smooth(y, s_pts):
        n = max(1, int(round(4 * s_pts))); x = np.arange(-n, n + 1)
        k = np.exp(-0.5 * (x / s_pts) ** 2); k /= k.sum()
        return np.convolve(y, k, mode="same")

# ----------------------------------------------------------------------
# 이미 스무딩된 CSV 를 **더** 넓히기 (2026-09-07 신설)
# ----------------------------------------------------------------------
#   왜: 가우시안은 합성된다 — σ_eff² = σ_base² + σ_add². 원자료(고유값)가 없어도
#   이미 σ_base 로 스무딩된 곡선에 σ_add 를 더 걸면 정확히 σ_eff 가 된다.
#   2026-08-04 에 PDOS 를 이 방식으로 0.05 → 0.15 로 올렸는데 **총 DOS 를 빠뜨렸다**
#   (lpsocl_dos_smooth.csv 가 0.05 인 채 PDOS 만 0.15 였다 — 2026-09-07 1저자 지적).
#
# ⛔ 이 경로가 **못 하는 것**
#   · 원자료를 대체하지 않는다. σ 를 **줄일 수는 없다** (정보를 되돌리지 못한다).
#   · 창 밖(±8 eV 밖)의 상태를 모른다 — 가장자리 ±4σ_add 는 패딩 가정에 의존한다.
#   · 밴드갭을 재지 않는다. 스무딩을 키우면 갭 안 꼬리가 **커진다** — 갭은 언제나
#     fixed-occupations nscf 고유값에서 읽는다 (CLAUDE.md 데이터 규율).

def compose_sigma(base, target):
    """σ_add = sqrt(target² − base²). target ≤ base 면 **거부한다**."""
    if target <= base:
        raise SystemExit(f"⛔ 목표 σ({target})가 기존 σ({base}) 이하다 — 스무딩은 "
                         f"되돌릴 수 없다. 줄이려면 원자료에서 다시 만들어야 한다.")
    return (target ** 2 - base ** 2) ** 0.5


def smooth_edge_safe(y, s_pts):
    """가장자리를 **값 유지(edge)** 로 패딩해 넓힌다.

    ⛔ zero-padding 을 쓰면 창 끝에서 DOS 가 인위적으로 **꺼진다** — 우리 창(±8 eV)은
      실제 띠 한가운데를 자른 것이라 바깥이 0 이 아니다. 상수 배열이 상수로 남는지를
      selftest 가 음성으로 확인한다.
    """
    n = max(1, int(round(4 * s_pts)))
    pad = np.pad(np.asarray(y, float), n, mode="edge")
    x = np.arange(-n, n + 1)
    k = np.exp(-0.5 * (x / s_pts) ** 2); k /= k.sum()
    return np.convolve(pad, k, mode="same")[n:-n]


def _resmooth_selftest():
    bad = []
    def chk(c, m):
        print(("  ✓ " if c else "  ✗ ") + m)
        if not c: bad.append(m)

    chk(abs(compose_sigma(0.05, 0.15) - 0.1414213562) < 1e-6,
        "합성: 0.05 → 0.15 의 추가 σ 는 0.14142 (PDOS 헤더의 그 값)")
    for t in (0.05, 0.03, 0.0):
        try:
            compose_sigma(0.05, t); hit = False
        except SystemExit:
            hit = True
        chk(hit, f"⛔음성: 목표 σ={t} ≤ 기존 0.05 을 거부한다 (스무딩은 되돌릴 수 없다)")

    dE, N = 0.02, 801
    y = np.zeros(N); y[N // 2] = 1.0 / dE            # 델타
    s1 = smooth_edge_safe(y, 0.05 / dE)
    both = smooth_edge_safe(s1, compose_sigma(0.05, 0.15) / dE)
    once = smooth_edge_safe(y, 0.15 / dE)
    chk(float(np.abs(both - once).max()) < 2e-3,
        "합성이 실제로 성립한다 — (0.05 → +0.1414) 결과가 (0.15 한 번)과 같다")

    const = np.full(N, 7.0)
    out = smooth_edge_safe(const, 0.15 / dE)
    chk(float(np.abs(out - 7.0).max()) < 1e-9,
        "⛔음성: **상수 배열이 가장자리에서 안 꺼진다** (zero-padding 이면 끝이 꺼진다)")

    area0 = float(np.trapezoid(s1, dx=dE)); area1 = float(np.trapezoid(both, dx=dE))
    chk(abs(area1 - area0) / max(area0, 1e-12) < 1e-3,
        f"넓이 보존 ({area0:.5f} → {area1:.5f})")
    chk(float(both.min()) >= -1e-12, "⛔음성: 음의 DOS 를 만들지 않는다")

    print(f"resmooth selftest {'PASS' if not bad else 'FAIL'} — {8 - len(bad)}/8")
    return 1 if bad else 0


ap = argparse.ArgumentParser()
ap.add_argument("--resmooth_from", help="이미 스무딩된 CSV 를 더 넓힌다 (--csv 대신)")
ap.add_argument("--base_sigma", type=float, default=0.05, help="그 CSV 의 기존 σ")
ap.add_argument("--target_sigma", type=float, default=0.15, help="맞출 목표 σ")
ap.add_argument("--note", default="", help="헤더에 남길 사유")
ap.add_argument("--selftest", action="store_true")
ap.add_argument("--csv")
ap.add_argument("--out")
ap.add_argument("--order", nargs="+", help="element column order")
ap.add_argument("--window", type=float, nargs=2, default=[-8.0, 5.0])
ap.add_argument("--sigma", type=float, default=0.15)
ap.add_argument("--gap", type=float, default=None)
ap.add_argument("--label", default="")
a = ap.parse_args()

if a.selftest:
    raise SystemExit(_resmooth_selftest())

if a.resmooth_from:
    # ── 이미 스무딩된 CSV 를 목표 σ 로 넓힌다 (원자료 불필요) ──────────────
    import datetime as _dt
    src = pathlib.Path(a.resmooth_from)
    head, rows = [], []
    for ln in src.read_text(encoding="utf-8-sig").splitlines():
        if ln.startswith("#"):
            head.append(ln); continue
        if not ln.strip():
            continue
        rows.append(ln.split(","))
    cols = rows[0]
    dat = np.array([[float(x) for x in r] for r in rows[1:]])
    E = dat[:, 0]
    dE = float(E[1] - E[0])
    s_add = compose_sigma(a.base_sigma, a.target_sigma)
    out = dat.copy()
    for j in range(1, dat.shape[1]):
        out[:, j] = smooth_edge_safe(dat[:, j], s_add / dE)
    if not a.out:
        raise SystemExit("⛔ --out 이 필요하다")
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        for h in head:
            w.writerow([h])
        w.writerow([f"# re-smoothed {_dt.date.today()}: base sigma={a.base_sigma} eV "
                    f"+ added {s_add:.4f} -> effective sigma={a.target_sigma} eV "
                    f"({a.base_sigma}^2 + {s_add:.4f}^2 = {a.target_sigma}^2). "
                    f"Edge-padded (not zero) — outermost +-{4*s_add:.2f} eV is padding-dependent."])
        w.writerow([f"# source: {src.as_posix()} (preserved unchanged)"])
        if a.note:
            w.writerow([f"# {a.note}"])
        w.writerow(cols)
        for r in out:
            w.writerow([f"{r[0]:.4f}"] + [f"{v:.4f}" for v in r[1:]])
    a0 = float(np.trapezoid(dat[:, 1], E)); a1 = float(np.trapezoid(out[:, 1], E))
    print(f"-> {a.out}  ({len(E)} rows, sigma {a.base_sigma} + {s_add:.4f} = {a.target_sigma})")
    print(f"   area(col1): {a0:.4f} -> {a1:.4f}  ({100*(a1-a0)/a0:+.3f} %)")
    raise SystemExit(0)

if not (a.csv and a.out and a.order):
    raise SystemExit("⛔ --csv --out --order 가 모두 필요하다 (또는 --resmooth_from)")

rows = list(csv.reader(open(a.csv)))
hdr = [h.split("#")[0].strip() for h in rows[0]]          # strip trailing "# ..."
data = np.array([[float(x) for x in r[:len(hdr)]] for r in rows[1:] if r])
col = {h: data[:, i] for i, h in enumerate(hdr)}

# ⛔ 2026-09-10 — 같은 사슬에서 열 이름이 **세 번째로** 갈렸다.
#   이 도구는 `E-EF`/`total` 을 찾는데 tools/electronic/standard_dos/sum_pdos.py 는
#   `E_minus_Ef`/`total_dos` 로 쓴다 (앞에 `E_eV` 열이 하나 더 붙는다).
#   projwfc → sum_pdos → 이 스무더 가 한 파이프라인인데 중간에서 이름이 끊겼다.
#   ⇒ 별칭을 받는다. 못 찾으면 **있는 열 이름을 보여준다** — KeyError 만 던지면
#     사람이 파일이 틀린 건지 이름이 다른 건지 못 가른다.
def _pick(names, what):
    for n in names:
        if n in col:
            return n
    raise SystemExit(f"⛔ {what} 열을 못 찾았다. 찾아본 이름: {names}\n"
                     f"   이 CSV 의 열: {hdr}")

_e   = _pick(["E-EF", "E_minus_Ef", "E_minus_EF_eV"], "에너지(E−E_F)")
_tot = _pick(["total", "total_dos", "DOS_total"], "총 DOS")
if _e != "E-EF":
    col["E-EF"] = col[_e]
if _tot != "total":
    col["total"] = col[_tot]
E = col["E-EF"]
m = (E >= a.window[0]) & (E <= a.window[1])
E = E[m]
dE = np.median(np.diff(E))
s_pts = a.sigma / dE

out_cols = ["total"] + list(a.order)
# Nd: also sum 4f sub-columns if present
extra = {}
if "Nd" in col and "Nd1_4f" in col and "Nd2_4f" in col:
    extra["Nd_4f"] = col["Nd1_4f"][m] + col["Nd2_4f"][m]

with open(a.out, "w", newline="") as f:
    w = csv.writer(f)
    tag = f" gap={a.gap} eV," if a.gap else ""
    w.writerow([f"# {a.label} DOS/PDOS (states/eV),{tag} Gaussian sigma={a.sigma} eV, EF=0, bonding=below 0"])
    head = ["E_minus_EF_eV"] + [f"DOS_{c}" for c in out_cols] + [f"DOS_{k}" for k in extra]
    w.writerow(head)
    sm = {c: smooth(col[c][m], s_pts) for c in out_cols}
    sm.update({k: smooth(v, s_pts) for k, v in extra.items()})
    for i, e in enumerate(E):
        w.writerow([f"{e:.3f}"] + [f"{sm[c][i]:.4f}" for c in out_cols]
                   + [f"{sm[k][i]:.4f}" for k in extra])
print(f"-> {a.out}  ({m.sum()} rows, {a.window[0]}..{a.window[1]} eV, sigma {a.sigma})")
