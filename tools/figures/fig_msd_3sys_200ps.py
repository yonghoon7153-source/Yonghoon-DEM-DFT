#!/usr/bin/env python3
"""fig_msd_3sys_200ps.py — 3계(LPSCl1.6 · LPSOCl1.6 · B2O3@LPSCl1.6) MSD 3패널.

한 패널 = 한 계, 그 안에 600/800/1000 K 세 곡선. **궤적 전체(200 ps)를 도시**하고
적합선은 창 안에서만 굵게, 창 밖으로는 얇게 연장해 "창 밖에서도 직선인가"를 눈으로 본다.

⚠⚠ **적합을 그냥 하지 않는다 — 창마다 검산해서 그림에 박는다.**
  · beta = d log MSD / d log t 를 **적합 창 안에서** 재고 (0.8-1.2 = Fickian) 라벨에 쓴다
  · 창 끝 MSD < 3 A^2 이면 이온이 자리를 못 벗어난 것 → 게이트 탈락 표시
  · 절편을 0 으로 강제하지 않는다. MSD = 6Dt + c 로 맞추고 c 를 CSV 에 남긴다
    (원점 강제는 케이지 진동 오프셋을 D 에 밀어넣어 저온 D 를 과대평가한다)
  · 게이트 탈락 곡선은 **적합선을 점선·회색**으로 그려 "이 값은 인용 금지"를 시각화

⚠ 단일 시드 곡선은 **계층 예시 전용**. 정량 D/Ea/sigma 는 멀티시드 *_md_arrhenius.json.
  (CLAUDE.md 규율 — 캡션·CSV 머리말에 그대로 박는다)

입력은 둘 중 하나:
  --run  LABEL=RUNDIR   (msd.json 을 직접 훑는다. 서버에서 이게 정석)
  --csv  PATH           (공통격자 CSV. 열이름 <label>_<T>K 형식)

  # 서버 (gabia/kgy) — 런 디렉토리에서 바로
  python3 tools/figures/fig_msd_3sys_200ps.py \
      --run modelc=~/work/runs/modelc_md --run lpsocl=~/work/runs/lpsocl_md/ladder \
      --run b2o3=~/work/runs/b2o3_md --out_png docs/figures/msd_3sys_200ps.png
"""
import argparse
import csv
import glob
import json
import math
import os
import re
import sys

import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from tools.figures.house_style import INK, MUT, SYS, apply_axes  # noqa: E402

# 사용자 표기 관례 (2026-08-04)
DISPLAY = {"modelc": "LPSCl1.6", "lpsocl": "LPSOCl1.6", "b2o3": "B2O3@LPSCl1.6",
           "comp1": "LPSCl", "LPSCl1.6": "LPSCl1.6"}
MD_EA = {"modelc": "0.197 ± 0.032", "lpsocl": "0.287 ± 0.024", "b2o3": "0.199 ± 0.034",
         "comp1": "0.253"}
T_WANT = (600, 800, 1000)
# CSV 왕복용 역매핑 — CSV 열은 표시명(LPSCl1.6 등)으로 저장되는데, 색(SYS)·Ea(MD_EA)는
# 내부명(modelc 등) 키다. 역매핑 없이는 CSV 로 다시 그릴 때 전 계가 잉크색이 된다.
INV_DISPLAY = {v: k for k, v in DISPLAY.items() if k != v}  # self-엔트리가 역매핑을 덮지 않게
BETA_OK = (0.80, 1.20)
MSD_MIN = 3.0            # A^2, msd_diffusive_check.py 와 같은 게이트


def shade(hex_color, f):
    """hex 색을 흰색 쪽으로 f 만큼 (0=원색, 1=흰색). 같은 계열 3온도를 명도로 구분."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = lambda c: int(round(c + (255 - c) * f))
    return f"#{m(r):02x}{m(g):02x}{m(b):02x}"


def fit_window(t, y, lo, hi):
    """[lo,hi] 창에서 (slope, intercept, R^2, beta, MSD@hi). 점 3개 미만이면 None."""
    m = [(a, b) for a, b in zip(t, y) if lo <= a <= hi and not (b != b)]
    if len(m) < 3:
        return None
    xs = np.array([p[0] for p in m]); ys = np.array([p[1] for p in m])
    A = np.polyfit(xs, ys, 1)
    pred = A[0] * xs + A[1]
    ss = float(((ys - pred) ** 2).sum()); st = float(((ys - ys.mean()) ** 2).sum())
    r2 = 1 - ss / st if st > 1e-30 else float("nan")
    g = [(math.log(a), math.log(b)) for a, b in m if a > 0 and b > 0]
    beta = (np.polyfit([p[0] for p in g], [p[1] for p in g], 1)[0]
            if len(g) >= 3 else float("nan"))
    return float(A[0]), float(A[1]), r2, float(beta), float(ys[-1])


def load_runs(specs, tmax, seed_mode='mean', exclude=('BROKEN',)):
    """--run LABEL=DIR 들에서 msd.json 을 훑는다. 시드 여럿이면 최소 시드(재현 가능)."""
    out = {}
    for spec in specs:
        label, root = spec.split("=", 1)
        for T in T_WANT:
            hits = []
            for f in glob.glob(os.path.join(os.path.expanduser(root), "**", "msd.json"),
                               recursive=True):
                # ⚠ 제외 패턴 (2026-08-04 실측 2건): BROKEN(좌표버그 폐기본)은 기본 제외.
                #   licube 류 — **같은 시드의 재실행**(밀도 cube 용 50 ps)이라 독립 시드가
                #   아니고, 평균에 넣으면 이중계상 + 최단길이 절단으로 200 ps 를 50 ps 로
                #   깎아 먹는다. --exclude licube 로 뺄 것.
                if any(pat in f for pat in exclude if pat):
                    continue
                try:
                    d = json.load(open(f))
                except Exception:
                    continue
                if abs(float(d.get("T_K", -1)) - T) < 1:
                    hits.append((f, d))
            if not hits:
                print(f"  ⛔ {label} {T} K — msd.json 못 찾음 ({root})")
                continue
            hits.sort(key=lambda x: x[0])
            root_abs = os.path.expanduser(root)
            if seed_mode == "mean" and len(hits) > 1:
                # ⚠⚠ **시드 평균이 기본이어야 하는 이유 (2026-08-04 실측).** 같은 계·같은 T
                #   인데 시드만 다른 두 파일에서 beta 가 0.98 vs 0.52 로 갈렸다. 대표 하나를
                #   고르는 규칙은 그 갈림을 **숨긴다**. 독립 시드는 같은 계의 다른 초기속도라
                #   MSD 앙상블 평균이 정당하다 (msd_diffusive_check.py --average 와 같은 논리).
                lens = [float(np.asarray(h[1]["times_ps"], float).max()) for h in hits]
                Tend = min(min(lens), tmax)
                if max(lens) - min(lens) > 1.0:
                    print(f"  ⚠ {label} {T} K — 시드 길이 불일치 {sorted(set(round(v) for v in lens))} ps."
                          f" 평균이 최단 {Tend:.0f} ps 로 절단된다. 짧은 파일이 보조런이면"
                          f" --exclude 로 뺄 것.")
                g = np.arange(0.0, Tend + 1e-9, 0.1)
                ys = []
                for hf, hd in hits:
                    tt = np.asarray(hd["times_ps"], float)
                    yy = np.asarray(hd["msd_Li_A2"], float)
                    ys.append(np.interp(g, tt, yy))
                ymean = np.mean(ys, axis=0)
                spread = float(np.std([y[-1] for y in ys]) / max(np.mean([y[-1] for y in ys]), 1e-9))
                out[(label, T)] = {"t": g, "y": ymean, "src": f"{root} (mean of {len(hits)})",
                                   "traj_ps": Tend, "n_seed": len(hits),
                                   "spread": spread, "D_stored": None}
                print(f"  ✓ {label} {T} K  [시드 {len(hits)}개 평균]  궤적 {Tend:.0f} ps · "
                      f"MSD@끝 {ymean[-1]:.1f} A^2 · 시드산포 {spread*100:.0f}%")
                for hf, hd in hits:
                    print(f"        · {os.path.relpath(hf, root_abs)}  "
                          f"({float(np.asarray(hd['times_ps'],float).max()):.0f} ps)")
                continue
            f, d = hits[0]
            t = np.asarray(d["times_ps"], float); y = np.asarray(d["msd_Li_A2"], float)
            k = t <= tmax + 1e-9
            out[(label, T)] = {"t": t[k], "y": y[k], "src": f, "n_seed": 1, "spread": 0.0,
                               "traj_ps": float(t.max()),
                               "D_stored": d.get("D_Li_cm2_s")}
            print(f"  ✓ {label} {T} K  ({k.sum()}점, 궤적 {t.max():.0f} ps, "
                  f"MSD@{t[k].max():.0f}ps {y[k][-1]:.1f} A^2)")
            print(f"        ← {os.path.relpath(f, root_abs)}"
                  + (f"   ⚠ 후보 {len(hits)}개 중 1개만 씀 — --seed_mode mean 권장"
                     if len(hits) > 1 else ""))
    return out


def load_csv(path, tmax):
    L = [l for l in open(path, encoding="utf-8-sig").read().splitlines()
         if l.strip() and not l.lstrip().startswith(("#", '"#'))]
    r = list(csv.reader(L)); hdr = r[0][1:]
    t = np.array([float(x[0]) for x in r[1:]])
    out = {}
    for i, h in enumerate(hdr):
        m = re.match(r"(.+)_(\d+)K$", h)
        if not m:
            continue
        label, T = m.group(1), int(m.group(2))
        label = INV_DISPLAY.get(label, label)          # 표시명 → 내부명
        if T not in T_WANT:
            continue
        y = np.array([float(x[i + 1]) if x[i + 1] else float("nan") for x in r[1:]])
        k = (t <= tmax + 1e-9) & ~np.isnan(y)
        if k.sum() < 3:
            continue
        out[(label, T)] = {"t": t[k], "y": y[k], "src": path, "n_seed": 1, "spread": 0.0,
                           "traj_ps": float(t[k].max()), "D_stored": None}
        print(f"  ✓ {label} {T} K  ({k.sum()}점, {t[k].max():.0f} ps, "
              f"MSD_end {y[k][-1]:.1f} A^2)")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="append", default=[], metavar="LABEL=DIR")
    ap.add_argument("--csv", action="append", default=[], metavar="PATH")
    ap.add_argument("--order", nargs="+", default=["modelc", "lpsocl", "b2o3"],
                    help="패널 순서 (라벨)")
    ap.add_argument("--tmax", type=float, default=200.0, help="도시 상한 [ps]")
    ap.add_argument("--panel_note", nargs="*", default=[], metavar="LABEL=TEXT",
                    help="패널 하단 좌측 주석 (영문 — 예: lpsocl='mean of 4 seeds'). "
                         "CSV 왕복은 시드 수 정보를 잃으므로 확정본에서 손으로 명시한다.")
    ap.add_argument("--exclude", nargs="*", default=["BROKEN"],
                    help="경로에 이 문자열이 들어간 msd.json 은 무시 (기본 BROKEN). "
                         "예: --exclude BROKEN licube")
    ap.add_argument("--seed_mode", choices=["mean", "min"], default="mean",
                    help="같은 (계,T) 에 msd.json 이 여럿일 때. mean=MSD 곡선 앙상블 평균(기본, "
                         "권장) · min=경로 사전순 첫 파일 하나(옛 동작, 시드 갈림을 숨긴다)")
    ap.add_argument("--fit", type=float, nargs=2, default=[2.0, 50.0],
                    help="적합 창 [ps] (기본 2 50 = 캠페인 규약)")
    ap.add_argument("--out_png", default="docs/figures/msd_3sys_200ps.png")
    ap.add_argument("--out_csv", default="db/properties/msd_3sys_200ps_origin.csv")
    a = ap.parse_args()

    data = {}
    print("── 수확")
    if a.run:
        data.update(load_runs(a.run, a.tmax, a.seed_mode, tuple(a.exclude)))
    for c in a.csv:
        data.update(load_csv(c, a.tmax))
    if not data:
        raise SystemExit("⛔ 곡선이 없다 — --run 또는 --csv 를 줄 것")

    labels = [l for l in a.order if any(k[0] == l for k in data)]
    missing = [l for l in a.order if l not in labels]
    if missing:
        print(f"  ⚠ 패널 없음: {missing} — 그 계의 msd.json/열을 못 찾았다")

    lo, hi = a.fit
    print(f"\n── 적합 (창 {lo:g}-{hi:g} ps · MSD = 6Dt + c, 절편 자유)")
    # ⚠ 열 이름은 **창 끝 시각을 명시**한다 (2026-08-04). 'MSD@창끝' 이라고만 쓰니
    #   궤적 길이로 오독됐다 — 궤적은 200 ps 인데 표는 창(50 ps) 값을 보여 준다.
    print(f"{'계':<14}{'T':>6}{'slope':>9}{'절편':>8}{'R^2':>7}{'beta':>7}"
          f"{'MSD@'+format(hi,'g')+'ps':>11}{'D (cm2/s)':>12}{'seed':>6}  게이트")
    fits = {}
    for lab in labels:
        for T in T_WANT:
            d = data.get((lab, T))
            if d is None:
                continue
            f = fit_window(d["t"], d["y"], lo, hi)
            if f is None:
                print(f"{DISPLAY.get(lab,lab):<14}{T:>6}   창 안 점 3개 미만 — 적합 불가")
                continue
            s, c, r2, beta, msd_end = f
            D = s / 6.0 * 1e-4
            ok_b = BETA_OK[0] <= beta <= BETA_OK[1]
            ok_m = msd_end >= MSD_MIN
            gate = "확산 ✓" if (ok_b and ok_m) else (
                "⛔ beta" if not ok_b else "") + ("⛔ MSD<3" if not ok_m else "")
            fits[(lab, T)] = {"slope": s, "intercept": c, "r2": r2, "beta": beta,
                              "msd_end": msd_end, "D": D, "gate_ok": ok_b and ok_m}
            print(f"{DISPLAY.get(lab,lab):<14}{T:>6}{s:>9.3f}{c:>8.2f}{r2:>7.3f}"
                  f"{beta:>7.2f}{msd_end:>11.1f}{D:>12.3e}"
                  f"{d.get('n_seed',1):>6}  {gate}")

    tlens = sorted({round(v["traj_ps"]) for v in data.values()})
    print(f"  (궤적 길이 {tlens} ps · 위 MSD 열은 **창 끝 {hi:g} ps** 값이지 궤적 끝이 아니다)")

    # ── Origin CSV ────────────────────────────────────────────────────────
    os.makedirs(os.path.dirname(a.out_csv), exist_ok=True)
    grid = np.arange(0.0, a.tmax + 1e-9, 1.0)
    cols, meta = {}, []
    for lab in labels:
        for T in T_WANT:
            d = data.get((lab, T))
            if d is None:
                continue
            cols[f"{DISPLAY.get(lab,lab)}_{T}K"] = np.where(
                grid <= d["t"].max(), np.interp(grid, d["t"], d["y"]), np.nan)
            fq = fits.get((lab, T))
            if fq:
                meta.append(f"{DISPLAY.get(lab,lab)} {T}K: slope {fq['slope']:.4f} A^2/ps, "
                            f"intercept {fq['intercept']:.3f} A^2, R2 {fq['r2']:.4f}, "
                            f"beta {fq['beta']:.3f}, D {fq['D']:.4e} cm2/s, "
                            f"gate {'PASS' if fq['gate_ok'] else 'FAIL'}, "
                            f"traj {d['traj_ps']:.0f} ps")
    with open(a.out_csv, "w", newline="", encoding="utf-8-sig") as f:
        f.write(f'"# Li MSD (A^2) vs time, MLIP-MD (UMA-s-1p1/omat). 0-{a.tmax:.0f} ps @ 1 ps grid."\n')
        f.write(f'"# Linear fit over {lo:g}-{hi:g} ps with FREE intercept: MSD = 6Dt + c. '
                'beta = dlogMSD/dlogt in the same window (0.8-1.2 = Fickian gate)."\n')
        f.write('"# SINGLE-SEED curves = ILLUSTRATIVE HIERARCHY ONLY. Quantitative D / Ea / sigma '
                'come from the multiseed *_md_arrhenius.json sets."\n')
        for m in meta:
            f.write(f'"# {m}"\n')
        w = csv.writer(f)
        w.writerow(["t_ps"] + list(cols))
        for i, tt in enumerate(grid):
            w.writerow([f"{tt:.1f}"] + ["" if np.isnan(cols[c][i]) else f"{cols[c][i]:.3f}"
                                         for c in cols])
    print(f"\n→ {a.out_csv}")

    # ── 그림 ──────────────────────────────────────────────────────────────
    pnotes = dict(x.split("=", 1) for x in a.panel_note)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    n = len(labels)
    fig, axs = plt.subplots(1, n, figsize=(4.7 * n, 4.0), sharex=True)
    axs = np.atleast_1d(axs)
    ymax = max(np.nanmax(data[k]["y"]) for k in data) * 1.08
    SH = {600: 0.55, 800: 0.28, 1000: 0.0}          # 저온=연함
    MK = {600: "o", 800: "s", 1000: "^"}
    for axp, lab in zip(axs, labels):
        base = SYS.get(lab, INK)
        pend = []
        nfail = 0
        for T in T_WANT:
            d = data.get((lab, T))
            if d is None:
                continue
            col = shade(base, SH[T])
            axp.plot(d["t"], d["y"], "-", color=col, lw=1.5, zorder=3)
            k = np.linspace(0, len(d["t"]) - 1, min(14, len(d["t"]))).astype(int)
            axp.plot(d["t"][k], d["y"][k], MK[T], color=col, ms=4.5, mec="none", zorder=4)
            fq = fits.get((lab, T))
            if not fq:
                continue
            # 적합선: 창 안 굵게, 창 밖 얇게 연장 (창 밖에서도 직선인가를 눈으로)
            xin = np.linspace(lo, hi, 20)
            xout = np.linspace(hi, min(a.tmax, d["t"].max()), 40)
            style = dict(color=INK if fq["gate_ok"] else MUT,
                         ls="--" if fq["gate_ok"] else ":")
            axp.plot(xin, fq["slope"] * xin + fq["intercept"], lw=1.6, zorder=5, **style)
            axp.plot(xout, fq["slope"] * xout + fq["intercept"], lw=0.9, alpha=0.5,
                     zorder=2, **style)
            # 곡선 끝 직접 라벨 (범례 대신 — 색맹 안전).
            # ⚠ 라벨은 **짧게** 유지한다 (2026-08-04). "(gate fail)" 같은 긴 문구를 붙이면
            #   우측정렬 글자가 왼쪽으로 뻗어 다른 곡선을 덮는다 — 실측 후 별표+각주로 뺐다.
            tag = f"{T} K  β {fq['beta']:.2f}" + ("" if fq["gate_ok"] else " *")
            pend.append({"x": d["t"][-1], "y": d["y"][-1], "tag": tag, "c": col})
            if not fq["gate_ok"]:
                nfail += 1
        # ⚠ 라벨 세로 충돌 제거 (2026-08-04). 궤적이 짧아 곡선 끝이 몰리면 글자가 겹친다
        #   — 아래에서 위로 훑으며 최소 간격을 확보한다(순서·값은 안 바꾸고 위치만).
        pend.sort(key=lambda p: p["y"])
        minsep = ymax * 0.085
        for i in range(1, len(pend)):
            if pend[i]["y"] - pend[i - 1]["y"] < minsep:
                pend[i]["y"] = pend[i - 1]["y"] + minsep
        for p in pend:
            axp.annotate(p["tag"], (p["x"], min(p["y"], ymax * 0.965)),
                         xytext=(-5, 5), textcoords="offset points",
                         ha="right", va="bottom", fontsize=9.5, color=p["c"],
                         fontweight="bold", zorder=6,
                         # 흰 배경 — 다른 곡선 위를 지날 때 글자가 묻히지 않게
                         bbox=dict(fc="white", ec="none", alpha=0.75, pad=1.2))
        axp.axvspan(lo, hi, color="#fef9c3", alpha=0.55, zorder=0)
        axp.text((lo + hi) / 2, ymax * 0.30, f"fit\n{lo:g}–{hi:g} ps",
                 ha="center", va="center", fontsize=8.5, color="#92400e",
                 linespacing=1.4, zorder=1)
        # 계 이름은 **좌상단** — 곡선 끝 라벨(우측)과 안 겹치게 (2026-08-04 충돌 수정)
        axp.text(0.025, 0.975, f"{DISPLAY.get(lab, lab)}",
                 ha="left", va="top", fontsize=13, color=INK, fontweight="bold",
                 transform=axp.transAxes, zorder=6)
        axp.text(0.025, 0.905, f"multiseed $E_a$ = {MD_EA.get(lab,'?')} eV",
                 ha="left", va="top", fontsize=9, color=MUT,
                 transform=axp.transAxes, zorder=6)
        if lab in pnotes:
            axp.text(0.025, 0.845, pnotes[lab], ha="left", va="top", fontsize=8.2,
                     color=MUT, style="italic", transform=axp.transAxes, zorder=6)
        if nfail:
            axp.text(0.5, 0.012, "* β outside 0.8–1.2 → not a diffusive fit; D not quotable",
                     ha="center", va="bottom", fontsize=8.2, color="#b45309",
                     transform=axp.transAxes, zorder=6)
        axp.set_xlim(0, a.tmax); axp.set_ylim(0, ymax)
        apply_axes(axp, xlabel="Time (ps)",
                   ylabel="Li MSD (Å$^2$)" if axp is axs[0] else None)
    fig.suptitle("Li mean-squared displacement, MLIP-MD (single seed — illustrative hierarchy only; "
                 "quantitative D/$E_a$ from the multiseed Arrhenius sets)",
                 fontsize=9.5, color=MUT, y=0.995)
    fig.tight_layout()
    os.makedirs(os.path.dirname(a.out_png), exist_ok=True)
    fig.savefig(a.out_png, dpi=300)
    print(f"→ {a.out_png}")


if __name__ == "__main__":
    main()
