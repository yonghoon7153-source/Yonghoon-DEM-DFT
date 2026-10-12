#!/usr/bin/env python3
"""Paper-grade total-DOS + element-resolved PDOS from QE dos.x / projwfc.x output.

Reads:
  - <prefix>_dos.dat                          (total DOS, EF in header)
  - <prefix>_pdos.pdos_atm#N(El)_wfc#M(L)     (per-atom per-orbital PDOS)

Generates:
  - <out>_dos_raw.png        — total DOS only, with EF and gap shading
  - <out>_dos_pdos.png       — total + element-stacked PDOS (Li/P/S/Cl)
  - <out>_dos_summary.json   — EF, VBM, CBM, gap, peak positions, and
                               VBM/CBM orbital character

Algorithm notes:
  - Gap detection: contiguous interval of DOS < dos_thresh above e_min
    (skip deep semicores). Prefer the run straddling EF; otherwise longest.
  - VBM_peak / CBM_peak: closest local DOS maximum to VBM (below) / CBM (above)
    with min_height filter to ignore broadening noise.
  - VBM/CBM character: integrate each (element, orbital) PDOS over the
    0.5 eV window adjacent to the edge → percentages.

Usage:
    python3 plot_dos.py --dir /path/to/output --prefix V0 --out_prefix V0
"""
import argparse
import json
import re
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# ⛔ 2026-09-10 — 이 도구는 자체 팔레트를 갖고 있었고 **하우스와 전부 달랐다**
#   (Li 회색 vs #0d9488 · P 주황 vs #7c3aed · S 금색 vs #c05621 · Cl 초록 vs #65a30d ·
#    O 빨강 vs #be123c · Br sienna 는 S 와 겹침). 같은 계의 DOS 와 COHP 그림이
#   원소마다 다른 색으로 나오면 사람이 둘을 같은 계로 못 읽는다. 팔레트를 한 곳에서 온다.
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "figures"))
try:
    import house_style as _hs
    _HOUSE = True
except ImportError:          # house_style 이 없으면 그림은 나오되 그 사실을 밝힌다
    _HOUSE = False
    print("  ⚠ house_style 을 못 읽었다 — 하우스 팔레트가 아닌 대비색으로 그린다")

# ⛔ 스무딩을 여기 다시 구현하지 않는다 — plot_lobster_4panel.gaussian_smooth 가
#   이미 있고 extract_cohp_curves 도 그걸 빌려 쓴다. 복사하면 규약이 갈라진다.
import importlib.util as _ilu
_p4 = Path(__file__).resolve().parent / "plot_lobster_4panel.py"
_spec = _ilu.spec_from_file_location("_p4", _p4)
_m4 = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_m4)
gaussian_smooth = _m4.gaussian_smooth


# 하우스 팔레트가 정본. 폴백은 house_style 이 없을 때만 쓰고, 그 사실을 위에서 찍는다.
_FALLBACK_COLOR = {"Li": "#888888", "P": "#FF9933", "S": "#E0C200", "Cl": "#3E8E41",
                   "Br": "#A0522D", "O": "#D62728", "Nd": "#17BECF", "B": "#0284c7"}
ELEM_COLOR = dict(_hs.ELEM) if _HOUSE else dict(_FALLBACK_COLOR)
for _e, _c in _FALLBACK_COLOR.items():      # 하우스에 없는 원소는 폴백으로 메운다
    ELEM_COLOR.setdefault(_e, _c)
ELEM_ORDER = ["Li", "P", "S", "Cl", "Br", "O", "B", "Nd"]
ORB_LABEL = {"s": "s", "p": "p", "d": "d", "f": "f"}


def find_total_dos(d: Path, prefix: str):
    """dos.x 산출 파일을 찾는다. 캠페인 안에서 이름이 두 가지다.

    ⛔ 2026-09-10 실측 — 이 도구는 `<prefix>_dos.dat` 만 찾았는데,
      run_gap_nscf_gabia.sh 의 DOS 분기는 `<prefix>.dos` 로 쓴다. **우리 도구
      둘의 인터페이스가 어긋나 있었다** — Nd n5fu 의 DOS 그림이 그래서 못 나왔다.
      플래그를 새로 다는 대신 캠페인이 실제로 쓰는 이름들을 순서대로 본다.
      (없으면 폴더에 뭐가 있는지 보여준다 — '파일 없음' 만 던지지 않는다)

    이 함수가 못 하는 것: 찾은 파일이 **tetrahedra DOS 인지 fixed-occ 인지**
      구분하지 않는다. 갭 판정은 DOS 가 아니라 nscf_gap 의 VBM/CBM 이다
      (CLAUDE.md 데이터 규율).
    """
    for name in (f"{prefix}_dos.dat", f"{prefix}.dos", f"{prefix}.dos.dat",
                 f"{prefix}_dos", "dos.dat"):
        c = d / name
        if c.is_file():
            return c
    have = sorted(x.name for x in d.iterdir() if "dos" in x.name.lower())[:12]
    raise SystemExit(
        f"⛔ dos.x 산출을 못 찾았다 (찾아본 이름: {prefix}_dos.dat · {prefix}.dos · "
        f"{prefix}.dos.dat · {prefix}_dos · dos.dat)\n"
        f"   폴더의 dos 관련 파일: {have or '없음'}\n"
        f"   dos.x 가 아직 안 돌았으면 그것부터 돌린다.")


def read_total_dos(dos_dat: Path):
    EF = None
    with open(dos_dat) as f:
        head = f.readline()
        m = re.search(r"EFermi\s*=\s*([\-\d.]+)\s*eV", head)
        if m:
            EF = float(m.group(1))
    data = np.loadtxt(dos_dat, comments="#")
    E = data[:, 0]
    DOS = data[:, 1]
    return E, DOS, EF


def read_pdos_files(pdos_dir: Path, prefix: str):
    """Returns (E, per_elem, per_elem_orb)
    per_elem[el]:        summed PDOS over all atoms & orbitals of element el
    per_elem_orb[el][o]: summed PDOS for orbital o ('s','p','d','f') of element el
    """
    # ⛔ 2026-09-10 — 여기도 관례가 갈려 있었다. 이 도구는 `<prefix>_pdos.pdos_atm#…`
    #   만 찾는데 projwfc.x 는 `<prefix>.pdos.pdos_atm#…` 으로 쓴다
    #   (sum_pdos.py 는 후자를 보고 169개를 멀쩡히 읽었다). 그래서 E_p 가 None 이 되어
    #   character_at_edge 에서 TypeError 로 죽었다 — **원인이 파일명인데 예외는 비교
    #   연산에서 났다.** 둘 다 받는다.
    pat = re.compile(rf"{re.escape(prefix)}[._]pdos\.pdos_atm#(\d+)\(([A-Za-z]+)\)"
                     rf"_wfc#(\d+)\(([a-z])\)$")
    per_elem = {}
    per_elem_orb = {}
    E_ref = None
    for fp in sorted(pdos_dir.iterdir()):
        m = pat.match(fp.name)
        if not m:
            continue
        _, elem, _, orb = m.groups()
        data = np.loadtxt(fp, comments="#")
        E = data[:, 0]
        ldos = data[:, 1]
        if E_ref is None:
            E_ref = E
        per_elem.setdefault(elem, np.zeros_like(ldos))
        per_elem[elem] += ldos
        per_elem_orb.setdefault(elem, {})
        per_elem_orb[elem].setdefault(orb, np.zeros_like(ldos))
        per_elem_orb[elem][orb] += ldos
    if E_ref is None:
        have = sorted(x.name for x in pdos_dir.iterdir() if "pdos" in x.name)[:4]
        raise SystemExit(
            f"⛔ PDOS 파일을 하나도 못 읽었다 (prefix='{prefix}')\n"
            f"   찾는 형태: <prefix>.pdos.pdos_atm#N(El)_wfc#M(l)  또는  <prefix>_pdos.pdos_atm#…\n"
            f"   폴더의 pdos 파일 예: {have or '없음'}\n"
            f"   projwfc.x 가 아직 안 돌았으면 그것부터 돌린다.")
    return E_ref, per_elem, per_elem_orb


def find_gap(E, DOS, EF, e_min=-3.0, dos_thresh=0.5):
    mask = E >= e_min
    Em = E[mask]; Dm = DOS[mask]
    low = Dm < dos_thresh
    runs = []
    i = 0
    while i < len(low):
        if low[i]:
            j = i
            while j < len(low) and low[j]:
                j += 1
            runs.append((i, j - i))
            i = j
        else:
            i += 1
    runs = [r for r in runs if r[1] >= 3]
    if not runs:
        return None, None, None
    chosen = None
    if EF is not None:
        for (s, n) in runs:
            e_lo = Em[s]
            e_hi = Em[min(s + n - 1, len(Em) - 1)]
            if e_lo <= EF <= e_hi:
                chosen = (s, n)
                break
    if chosen is None:
        chosen = max(runs, key=lambda r: r[1])
    s, n = chosen
    vbm_idx = max(s - 1, 0)
    cbm_idx = min(s + n, len(Em) - 1)
    return float(Em[vbm_idx]), float(Em[cbm_idx]), float(Em[cbm_idx] - Em[vbm_idx])


def local_maxima(E, DOS, min_height=1.0):
    """Returns list of (E, DOS) at local maxima above min_height."""
    peaks = []
    for i in range(1, len(DOS) - 1):
        if DOS[i] > DOS[i - 1] and DOS[i] >= DOS[i + 1] and DOS[i] >= min_height:
            peaks.append((float(E[i]), float(DOS[i])))
    return peaks


def closest_peak_below(peaks, edge):
    cand = [p for p in peaks if p[0] < edge]
    return max(cand, key=lambda p: p[0]) if cand else None  # largest E < edge


def closest_peak_above(peaks, edge):
    cand = [p for p in peaks if p[0] > edge]
    return min(cand, key=lambda p: p[0]) if cand else None  # smallest E > edge


def character_at_edge(E_p, per_elem_orb, edge, window, side):
    """Integrate per-(elem, orb) PDOS over [edge - window, edge] for VBM (side='valence')
    or [edge, edge + window] for CBM (side='conduction'). Returns sorted percent breakdown.
    """
    if side == "valence":
        lo, hi = edge - window, edge
    else:
        lo, hi = edge, edge + window
    mask = (E_p >= lo) & (E_p <= hi)
    if not mask.any():
        return []
    contribs = []
    total = 0.0
    for el, orb_d in per_elem_orb.items():
        for orb, p in orb_d.items():
            I = float(np.trapezoid(p[mask], E_p[mask]))
            if I > 0:
                contribs.append((el, orb, I))
                total += I
    if total <= 0:
        return []
    contribs.sort(key=lambda x: -x[2])
    return [{"element": el, "orbital": orb, "percent": round(100 * I / total, 1)}
            for (el, orb, I) in contribs if (100 * I / total) >= 1.0]


def format_character(breakdown, top_n=3):
    if not breakdown:
        return None
    parts = [f"{b['element']} {b['orbital']} ({b['percent']:.0f}%)" for b in breakdown[:top_n]]
    return " + ".join(parts)


def _ylim_in_window(xlim, *series):
    """x 창 **안**의 값만으로 y 상한을 정한다 → (top, 창밖최대/창안최대).

    ⛔⛔ 2026-09-10 실측 — 이 도구는 `set_xlim` 만 하고 y 는 matplotlib 자동배율에
      맡겼다. 자동배율은 **그려 넣은 전 구간**을 보므로, 창 밖(깊은 준core)의 거대한
      델타가 y 상한을 끌어올려 **창 안 곡선이 전부 바닥에 깔렸다**
      (ndo_lpscl16_n5fu: y축이 5×10⁵ states/eV 까지 갔고 그림이 백지로 보였다).
      원인은 계산이 아니라 **축 설정**이었다.

    이 함수가 못 하는 것: 창 밖 스파이크의 정체를 밝히지 않는다. 비율만 돌려주므로
      호출부가 그 사실을 사람에게 알릴 수 있다.
    """
    lo, hi = xlim
    tops_in, tops_all = [], []
    for E, y in series:
        E = np.asarray(E); y = np.asarray(y)
        m = (E >= lo) & (E <= hi)
        if m.any():
            tops_in.append(float(np.max(y[m])))
        tops_all.append(float(np.max(y)))
    if not tops_in:
        return None, 1.0
    t_in, t_all = max(tops_in), max(tops_all)
    return t_in * 1.08, (t_all / t_in if t_in > 0 else float("inf"))


def plot_raw(E, DOS, EF, vbm, cbm, vbm_peak, cbm_peak, gap, out_path,
             xlim=(-15, 10), title="Total DOS"):
    _extra_series = ()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(E, DOS, color="black", lw=1.0)
    ax.fill_between(E, 0, DOS, color="lightgray", alpha=0.6)
    if EF is not None:
        ax.axvline(EF, color="red", ls="--", lw=1.0, label=f"E$_F$ = {EF:.3f} eV")
    if vbm is not None and cbm is not None:
        ax.axvspan(vbm, cbm, color="lightyellow", alpha=0.6,
                   label=f"gap = {gap:.2f} eV ({vbm:.2f} → {cbm:.2f})"
                         f"  [{globals().get('_GAP_SRC','?')}]")
    if vbm_peak is not None:
        ax.axvline(vbm_peak[0], color="#0066CC", ls=":", lw=0.9, alpha=0.7)
        ax.annotate(f"VBM peak\n{vbm_peak[0]:.2f}", xy=(vbm_peak[0], vbm_peak[1]),
                    xytext=(-30, 10), textcoords="offset points",
                    fontsize=8, color="#0066CC",
                    arrowprops=dict(arrowstyle="-", lw=0.7, color="#0066CC"))
    if cbm_peak is not None:
        ax.axvline(cbm_peak[0], color="#CC0066", ls=":", lw=0.9, alpha=0.7)
        ax.annotate(f"CBM peak\n{cbm_peak[0]:.2f}", xy=(cbm_peak[0], cbm_peak[1]),
                    xytext=(10, 10), textcoords="offset points",
                    fontsize=8, color="#CC0066",
                    arrowprops=dict(arrowstyle="-", lw=0.7, color="#CC0066"))
    ax.set_xlim(*xlim)
    _top, _ratio = _ylim_in_window(xlim, (E, DOS), *_extra_series)
    ax.set_ylim(bottom=0, top=_top)
    if _ratio > 3:
        print(f"  ⚠ 창({xlim[0]}..{xlim[1]} eV) 밖 최대가 창 안의 {_ratio:.0f}배다 — "
              f"깊은 준core 델타로 보인다. y 상한은 **창 안 기준**으로 잡았다.")
    ax.set_xlabel("E (eV)")
    ax.set_ylabel("DOS (states/eV/cell)")
    if _HOUSE:
        _hs.apply_axes(ax)   # spines top/right 제거 · 하우스 글꼴·눈금
    ax.set_title(title)
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor="white", bbox_inches="tight")
    print(f"  → {out_path}")
    plt.close()


def plot_pdos(E, DOS, EF, vbm, cbm, gap, E_p, per_elem,
              vbm_char, cbm_char, out_path, xlim=(-15, 10), title=None):
    _extra_series = tuple((E_p, v) for v in per_elem.values())
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(E, DOS, color="black", lw=1.2, label="Total")
    for el in ELEM_ORDER:
        if el in per_elem:
            ax.plot(E_p, per_elem[el], color=ELEM_COLOR[el], lw=1.2, label=el)
            ax.fill_between(E_p, 0, per_elem[el], color=ELEM_COLOR[el], alpha=0.3)
    if EF is not None:
        ax.axvline(EF, color="red", ls="--", lw=1.0, label=f"E$_F$ = {EF:.2f} eV")
    if vbm is not None and cbm is not None:
        ax.axvspan(vbm, cbm, color="lightyellow", alpha=0.5,
                   label=f"gap = {gap:.2f} eV  [{globals().get('_GAP_SRC','?')}]")
    ax.set_xlim(*xlim)
    _top, _ratio = _ylim_in_window(xlim, (E, DOS), *_extra_series)
    ax.set_ylim(bottom=0, top=_top)
    if _ratio > 3:
        print(f"  ⚠ 창({xlim[0]}..{xlim[1]} eV) 밖 최대가 창 안의 {_ratio:.0f}배다 — "
              f"깊은 준core 델타로 보인다. y 상한은 **창 안 기준**으로 잡았다.")
    ax.set_xlabel("E (eV)")
    ax.set_ylabel("DOS / PDOS (states/eV/cell)")
    if _HOUSE:
        _hs.apply_axes(ax)   # spines top/right 제거 · 하우스 글꼴·눈금
    t = title or "Total DOS + element-resolved PDOS"
    if vbm_char and cbm_char:
        t += f"\nVBM: {vbm_char}    CBM: {cbm_char}"
    ax.set_title(t, fontsize=11)
    ax.legend(loc="upper left", fontsize=9, ncol=2)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor="white", bbox_inches="tight")
    print(f"  → {out_path}")
    plt.close()


def redraw_from_csv(args):
    """PDOS figure from a raw per-element table + this tool's summary json (2026-10-13: vector copies for
    the seminar deck). Same smoothing (gaussian_smooth, --smooth σ on total and PDOS alike) and the same
    plot_pdos. The gap band and label come from the summary, and only a fixed-occ nscf gap is drawn unless
    --allow_dos_gap. What it cannot do: recompute VBM/CBM or the band-edge characters (it reads them)."""
    import csv as _csv
    if not args.summary:
        raise SystemExit("⛔ --from_csv needs --summary (EF, VBM/CBM and the gap source come from it)")
    sm = json.loads(Path(args.summary).read_text(encoding='utf-8'))
    src = sm.get("band_gap_source", "?")
    if src != "fixed-occ nscf" and not args.allow_dos_gap:
        raise SystemExit(f"⛔ summary gap source is '{src}', not fixed-occ nscf — CLAUDE.md band-gap rule "
                         "(use --allow_dos_gap to draw it with that label)")
    rows = [r for r in _csv.reader(open(args.from_csv, encoding='utf-8')) if r and not r[0].startswith('#')]
    head, body = rows[0], np.array([[float(x) for x in r] for r in rows[1:]])
    if 'E_eV' not in head or 'total_dos' not in head:
        raise SystemExit(f"⛔ {args.from_csv}: needs E_eV and total_dos columns (got {head})")
    E = body[:, head.index('E_eV')]
    DOS = body[:, head.index('total_dos')]
    per_elem = {el: body[:, head.index(el)] for el in ELEM_ORDER if el in head}
    if args.smooth and args.smooth > 0:
        DOS = gaussian_smooth(DOS, E, args.smooth)
        per_elem = {el: gaussian_smooth(v, E, args.smooth) for el, v in per_elem.items()}
    globals()["_GAP_SRC"] = src
    keep = (E >= args.xlim[0] - 1.0) & (E <= args.xlim[1] + 1.0)   # after smoothing: no edge effect inside xlim;
    E, DOS = E[keep], DOS[keep]                                       # keeps vector files small (the semicore delta
    per_elem = {el: v[keep] for el, v in per_elem.items()}            # at −42 eV is outside every window)
    stem = Path(args.out_prefix or Path(args.from_csv).stem)
    for ext in [e.strip().lstrip('.') for e in args.formats.split(',') if e.strip()]:
        plt.rcParams['svg.fonttype'] = 'path'
        plot_pdos(E, DOS, sm["EF_eV_qe"], sm["VBM_eV"], sm["CBM_eV"], sm["band_gap_eV"], E, per_elem,
                  sm.get("VBM_character"), sm.get("CBM_character"), f"{stem}_dos_pdos.{ext}",
                  xlim=tuple(args.xlim), title=args.title)


def main():
    ap = argparse.ArgumentParser()
    # ⛔⛔ CLAUDE.md 데이터 규율: **Band gap 은 fixed-occupations nscf 의 VBM/CBM
    #   고유값만 인정하고 DOS-threshold 판독은 금지**다. 그런데 이 도구는 DOS 문턱으로
    #   구한 갭을 그림 라벨에 `gap = X.XX eV` 로 그대로 박아 왔다 — 그 PNG 가 발표·
    #   webapp 으로 나가면 금지된 수가 인용 가능한 수처럼 보인다.
    #   실측(2026-09-10, ndo_lpscl16_n5fu): DOS 문턱 2.260 eV vs fixed-occ 정본 2.1616 eV.
    #   ⇒ 정본을 주면 그걸 쓰고, 안 주면 **라벨에 '인용 불가' 를 같이 그린다**
    #     (경고를 옆에 두는 게 아니라 라벨 안에 넣는다 — 값이 잘려 나가도 따라가게).
    ap.add_argument("--vbm", type=float, default=None,
                    help="fixed-occ nscf 의 VBM (eV). --cbm 과 같이 주면 그림 갭이 정본이 된다")
    ap.add_argument("--cbm", type=float, default=None,
                    help="fixed-occ nscf 의 CBM (eV)")
    # ⛔⛔ 2026-09-10 실측 — 이 도구는 **스무딩을 전혀 안 했다.** raw dos.x 출력을
    #   그대로 그리는데, 2×2×1 같은 성긴 k 격자의 tetrahedra DOS 는 델타 빗이라
    #   y축이 5×10⁵ states/eV 까지 튀고 곡선이 바닥에 깔려 아무것도 안 보였다.
    #   family 규약은 σ 0.15 eV 다 (tools/figures/export_dos_pdos_csv.py).
    #   ⚠ 2026-09-07 사고: PDOS 만 0.15 로 올리고 **총 DOS 를 빠뜨렸다**
    #     (lpsocl_dos_smooth.csv 가 0.05 인 채였다) ⇒ 여기서는 **둘에 같은 σ**를 건다.
    #   ⛔ 스무딩은 k 격자 미수렴을 고치지 않는다 — 보기 좋게 만들 뿐이다.
    ap.add_argument("--smooth", type=float, default=0.15,
                    help="Gaussian sigma (eV). family 규약 0.15. 0 이면 raw")
    ap.add_argument("--dir", default=None)
    ap.add_argument("--from_csv", default=None,
                    help="redraw the PDOS figure from a raw table (E_eV,…,total_dos,<element>…; e.g. "
                         "db/properties/<sys>_pdos.csv) — QE files not needed. Needs --summary")
    ap.add_argument("--summary", default=None,
                    help="<sys>_dos_summary.json written by this tool (EF, VBM/CBM, gap source, characters)")
    ap.add_argument("--formats", default="png",
                    help="--from_csv only: comma list of file types, e.g. 'png,svg,pdf'")
    ap.add_argument("--allow_dos_gap", action="store_true",
                    help="--from_csv only: draw even if the summary gap is not fixed-occ nscf (label says so)")
    ap.add_argument("--prefix", default="V0")
    ap.add_argument("--out_prefix", default=None)
    ap.add_argument("--e_min", type=float, default=-3.0)
    ap.add_argument("--dos_thresh", type=float, default=0.5)
    ap.add_argument("--peak_min_height", type=float, default=1.0)
    ap.add_argument("--char_window", type=float, default=0.5,
                    help="energy window (eV) below VBM / above CBM for orbital character")
    ap.add_argument("--xlim", type=float, nargs=2, default=[-15, 10])
    ap.add_argument("--title", default=None,
                    help="optional plot title (e.g., composition)")
    args = ap.parse_args()
    if args.from_csv:
        return redraw_from_csv(args)
    if not args.dir:
        raise SystemExit("⛔ give --dir (QE dos.x/projwfc.x output) or --from_csv + --summary")

    d = Path(args.dir)
    out_pref = args.out_prefix or args.prefix
    _dosf = find_total_dos(d, args.prefix)
    print(f"  total DOS ← {_dosf.name}")
    E, DOS, EF = read_total_dos(_dosf)
    _raw_max = float(np.max(DOS))
    print(f"read total DOS: {len(E)} points, EF = {EF}")

    E_p, per_elem, per_elem_orb = read_pdos_files(d, args.prefix)
    for el, p in per_elem.items():
        print(f"  PDOS sum for {el}: integral = {np.trapezoid(p, E_p):.2f} states")

    vbm, cbm, gap = find_gap(E, DOS, EF, e_min=args.e_min, dos_thresh=args.dos_thresh)
    if args.smooth and args.smooth > 0:
        DOS = gaussian_smooth(DOS, E, args.smooth)
        print(f"  스무딩 σ={args.smooth} eV — 총 DOS 최대 {_raw_max:.3g} → {np.max(DOS):.3g} states/eV")
        if _raw_max > 1e4:
            print(f"  ⚠⚠ raw 최대가 {_raw_max:.3g} states/eV 다 — 델타 빗(성긴 k 격자의 "
                  f"tetrahedra) 신호다. **스무딩은 k 미수렴을 고치지 않는다.**")
    if (args.vbm is None) != (args.cbm is None):
        raise SystemExit("⛔ --vbm 과 --cbm 은 **둘 다** 줘야 한다 (하나만 주면 갭이 섞인다)")
    if args.vbm is not None:
        _dos_gap = gap
        vbm, cbm = args.vbm, args.cbm
        gap = cbm - vbm
        GAP_SRC = "fixed-occ nscf"
        print(f"  ★ 갭을 fixed-occ 정본으로 대체: {gap:.4f} eV "
              f"(DOS-threshold 였다면 {_dos_gap:.3f} eV — 차 {abs(gap-_dos_gap):.3f})")
    else:
        GAP_SRC = "DOS threshold — not citable"
        print("  ⚠ --vbm/--cbm 이 없다 — 그림 갭은 **DOS-threshold** 이고 "
              "CLAUDE.md 상 인용 불가다. 라벨에 그렇게 적어 나간다.")
    globals()["_GAP_SRC"] = GAP_SRC
    if vbm is None:
        print("no gap found"); return
    i_vbm = int(np.argmin(np.abs(E - vbm)))
    i_cbm = int(np.argmin(np.abs(E - cbm)))
    print(f"VBM={vbm:.3f} (DOS={DOS[i_vbm]:.3f})  "
          f"CBM={cbm:.3f} (DOS={DOS[i_cbm]:.3f})  gap={gap:.3f} eV")

    peaks = local_maxima(E, DOS, min_height=args.peak_min_height)
    vbm_peak_t = closest_peak_below(peaks, vbm)
    cbm_peak_t = closest_peak_above(peaks, cbm)
    if vbm_peak_t:
        print(f"  closest VBM peak: {vbm_peak_t[0]:.3f} eV (DOS={vbm_peak_t[1]:.2f})")
    if cbm_peak_t:
        print(f"  closest CBM peak: {cbm_peak_t[0]:.3f} eV (DOS={cbm_peak_t[1]:.2f})")

    if args.smooth and args.smooth > 0:
        for _el in list(per_elem):
            per_elem[_el] = gaussian_smooth(per_elem[_el], E_p, args.smooth)
    vbm_break = character_at_edge(E_p, per_elem_orb, vbm,
                                   window=args.char_window, side="valence")
    cbm_break = character_at_edge(E_p, per_elem_orb, cbm,
                                   window=args.char_window, side="conduction")
    vbm_char = format_character(vbm_break)
    cbm_char = format_character(cbm_break)
    if vbm_char: print(f"  VBM character: {vbm_char}")
    if cbm_char: print(f"  CBM character: {cbm_char}")

    summary = {
        "EF_eV_qe": EF,
        "VBM_eV": vbm,
        "CBM_eV": cbm,
        "band_gap_eV": gap,
        "band_gap_source": globals().get("_GAP_SRC", "?"),
        "smoothing_sigma_eV": args.smooth,
        "total_dos_raw_max_states_per_eV": _raw_max,
        "⛔": ("DOS-threshold 갭은 CLAUDE.md 상 인용 불가다 — 정본은 fixed-occ nscf 의 "
               "VBM/CBM 고유값이다. --vbm/--cbm 으로 주면 이 값이 정본으로 바뀐다."),
        "VBM_peak_eV": vbm_peak_t[0] if vbm_peak_t else None,
        "CBM_peak_eV": cbm_peak_t[0] if cbm_peak_t else None,
        "VBM_character": vbm_char,
        "CBM_character": cbm_char,
        "VBM_character_breakdown_pct": vbm_break,
        "CBM_character_breakdown_pct": cbm_break,
        "character_window_eV": args.char_window,
        "dos_threshold_states_per_eV": args.dos_thresh,
        "e_min_eV": args.e_min,
        "method": (
            f"VBM/CBM = edges of low-DOS run (DOS<{args.dos_thresh}, E>{args.e_min} eV) "
            f"straddling EF; peaks = nearest local maxima with height≥{args.peak_min_height}; "
            f"character = PDOS percent within {args.char_window} eV of edge."
        ),
    }
    json_path = d / f"{out_pref}_dos_summary.json"
    json_path.write_text(json.dumps(summary, indent=2))
    print(f"  → {json_path}")

    plot_raw(E, DOS, EF, vbm, cbm, vbm_peak_t, cbm_peak_t, gap,
             d / f"{out_pref}_dos_raw.png", xlim=tuple(args.xlim),
             title=args.title or "Total DOS")
    plot_pdos(E, DOS, EF, vbm, cbm, gap, E_p, per_elem,
              vbm_char, cbm_char,
              d / f"{out_pref}_dos_pdos.png", xlim=tuple(args.xlim),
              title=args.title)


if __name__ == "__main__":
    main()
