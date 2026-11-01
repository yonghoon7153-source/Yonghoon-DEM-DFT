#!/usr/bin/env python3
"""fig_weekly_2026_11_01.py — 주간보고 (2026-10-26 ~ 11-01) 그림 1 장 + Origin CSV 1 벌.

그림: Nd Q3′ 같은 셀 두 모델 (MP_07 = Nd@P · MLi_04 = Nd@Li) 과 10-19 Q3 셀 (120 원자) 의 **밀도 품질 진단** —
  (a) 원자마다 '그 원자에 붙은 유의 Bader 극대 수' (BCF.dat 의 'ATOM' 열 = bader 가 붙인 원자) — 점 하나 = 원자 하나 ·
      가로 막대 = 원소별 위쪽 중앙값 (sorted[n//2] · 기록이 쓴 정의 — 원자 둘이면 큰 쪽이다)
  (b) pp.x 가 AE 재구성 (punch_plot) **앞**에 찍는 'negative rho (up)' — 저장된 밀도의 음의 부분 적분 (e)
  이번 주 MP_07 Bader 판독을 **보류**한 근거 그림이다 (nd_q3p_runlog_2026_10_27.json `Bader_회수` · `Bader_MP_07_진단`).

    python3 tools/figures/fig_weekly_2026_11_01.py
    python3 tools/figures/fig_weekly_2026_11_01.py --selftest   # 기록 재현 (양성) · 깨기 (음성)

읽는 것 (전부 기록 · 새 계산 없음)
  · db/raw/nd_q3p_bader_2026_10_30/<모델>/{BCF.dat, bader_run.out, pp_ae.out, scf_input_copy.in}
  · db/raw/nd_q3_bader_2026_10_19/{BCF.dat, bader_run.out, pp_ae.out, scf_input_copy.in}
  · db/properties/nd_q3p_runlog_2026_10_27.json — 교차검산 기준 (원소별 평균 · 음의 밀도 · 극대 수)

⛔ 이 그림이 못 하는 것
  · Bader 순전하 (net charge) 를 그리지 않는다 — MP_07 판독은 보류 중이고, 값은 판독 기록에서만 쓴다.
  · 밀도가 왜 시끄러운지 판정하지 않는다 — 같은 입력 SCF 다시 (tmux ndrerun) 가 가른다 (기록의 ① save 밀도 ② 기하 · PP 조합).
  · '극대 수 = 품질' 의 문턱을 정하지 않는다 — 카드에 밀도 품질 게이트가 **없었다** (결과 뒤 진단이다).
  · Q3 셀의 pp_ae.out 에는 negative rho 줄이 없다 → (b) 에 0 으로 그리지 않고 'not printed' 로 적는다.
  · 극대를 원자에 붙이는 규칙은 bader 의 BCF 'ATOM' 열 (가장 가까운 원자) 그대로다 — 다시 계산하지 않는다.
"""
from __future__ import annotations

import csv
import json
import pathlib
import re
import sys
from collections import Counter

R = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/figures"))
import house_style as H  # noqa: E402

DB = R / "db/properties"
RUNLOG = DB / "nd_q3p_runlog_2026_10_27.json"
OUT = R / "docs/figures/weekly_2026_11_01"
CSV = DB / "weekly_nd_q3p_bader_density_check_origin_2026_11_01.csv"
ELEMS = ("Li", "Nd", "Cl", "S", "O", "P")
#: (키, 폴더, 그림 라벨, 색) — 색은 house_style 원소 팔레트와 겹치지 않게 모델 색을 따로 쓴다
MODELS = (
    ("MP_07", R / "db/raw/nd_q3p_bader_2026_10_30/MP_07", "Nd on P site (MP_07, 66 atoms)", "#7c3aed"),
    ("MLi_04", R / "db/raw/nd_q3p_bader_2026_10_30/MLi_04", "Nd on Li site (MLi_04, 58 atoms)", "#0d9488"),
    ("Q3_1019", R / "db/raw/nd_q3_bader_2026_10_19", "Q3 cell, Oct 19 (120 atoms)", "#6b7280"),
)
#: 기록 (runlog `Bader_MP_07_진단_2026_10_30` 잡음_분포) 의 원소별 '원자당' 수 — **평균이 아니라 위쪽 중앙값**
#:   (10-30 진단 명령이 sorted(v)[len(v)//2] 로 냈다 · 2026-11-01 이 그림을 만들다 평균으로 대조해서 빨강이 나 알았다)
REC_PER_ELEM = {"MP_07": {"Li": 164, "Nd": 162, "Cl": 94, "S": 77, "O": 30, "P": 29},
                "MLi_04": {"Li": 5, "Nd": 61, "Cl": 26, "S": 13, "O": 4, "P": 3}}


class Refuse(RuntimeError):
    """교차검산이 틀렸다 — 그리지 않는다."""


def species(scf_in: pathlib.Path) -> list[str]:
    """ATOMIC_POSITIONS 블록의 원소 이름 (ACF/BCF 원자 번호 순서)."""
    txt = scf_in.read_text(errors="ignore")
    m = re.search(r"\bnat\s*=\s*(\d+)", txt)
    if not m:
        raise Refuse(f"{scf_in}: nat 가 없다")
    nat = int(m.group(1))
    lines = txt.split("ATOMIC_POSITIONS", 1)[1].splitlines()[1:]
    sp = []
    for ln in lines:
        tok = ln.split()
        if len(tok) < 4:
            break
        sp.append(re.sub(r"\d+$", "", tok[0]))
        if len(sp) == nat:
            break
    if len(sp) != nat:
        raise Refuse(f"{scf_in}: 원자 {len(sp)} 개 ≠ nat {nat}")
    return sp


def bcf_atoms(bcf: pathlib.Path) -> list[int]:
    """BCF.dat 의 극대마다 'ATOM' 열 (1 부터)."""
    out = []
    for ln in bcf.read_text(errors="ignore").splitlines():
        tok = ln.split()
        if len(tok) == 7 and tok[0].isdigit():
            out.append(int(tok[5]))
    return out


def significant_maxima(run_out: pathlib.Path) -> int:
    m = re.search(r"SIGNIFICANT MAXIMA FOUND:\s*(\d+)", run_out.read_text(errors="ignore"))
    if not m:
        raise Refuse(f"{run_out}: SIGNIFICANT MAXIMA 줄이 없다")
    return int(m.group(1))


def negative_rho_up(pp_out: pathlib.Path):
    """punch_plot **앞**의 'negative rho (up, down)' 첫 값. 줄이 없으면 None (0 이 아니다)."""
    txt = pp_out.read_text(errors="ignore")
    pre = txt.split("Calling punch_plot", 1)[0]
    m = re.search(r"negative rho \(up, down\):\s*([0-9.Ee+-]+)", pre)
    return float(m.group(1)) if m else None


def model_row(key: str, folder: pathlib.Path, sp_override=None) -> dict:
    sp = sp_override if sp_override is not None else species(folder / "scf_input_copy.in")
    atoms = bcf_atoms(folder / "BCF.dat")
    n_sig = significant_maxima(folder / "bader_run.out")
    if len(atoms) != n_sig:
        raise Refuse(f"{key}: BCF 극대 {len(atoms)} 개 ≠ bader_run.out SIGNIFICANT {n_sig}")
    if max(atoms) > len(sp):
        raise Refuse(f"{key}: BCF 원자 번호 {max(atoms)} > 원자 수 {len(sp)} — 원소 목록이 이 셀 것이 아니다")
    per_atom = Counter(atoms)
    n_el = Counter(sp)
    per_elem = {}
    for el in ELEMS:
        idx = [i + 1 for i, s in enumerate(sp) if s == el]
        if idx:
            counts = [per_atom[i] for i in idx]
            per_elem[el] = {"n_atoms": len(idx), "maxima": sum(counts), "counts": counts, "idx": idx,
                            "upper_median": sorted(counts)[len(counts) // 2], "max": max(counts)}
    unknown = set(n_el) - set(ELEMS)
    if unknown:
        raise Refuse(f"{key}: 그림에 없는 원소 {sorted(unknown)}")
    return {"key": key, "nat": len(sp), "maxima": n_sig, "per_elem": per_elem,
            "neg_rho_up": negative_rho_up(folder / "pp_ae.out")}


def compute(models=MODELS, sp_for=None) -> list[dict]:
    """세 셀을 세고 기록과 대조한다. sp_for = {key: 원소 목록} (selftest 의 깨기용)."""
    rows = [model_row(k, f, (sp_for or {}).get(k)) for k, f, _, _ in models]
    rec = json.loads(RUNLOG.read_text(encoding="utf-8"))
    diag = rec["Bader_MP_07_진단_2026_10_30"]["잡음_분포"]
    rec2 = rec["Bader_MP_07_다시_걸림_2026_10_30"]["다음"]
    by = {r["key"]: r for r in rows}
    for key, want in REC_PER_ELEM.items():
        got = {el: v["upper_median"] for el, v in by[key]["per_elem"].items()}
        if got != want:
            raise Refuse(f"{key}: 원소별 극대/원자 (위쪽 중앙) {got} ≠ 기록 {want} (runlog 잡음_분포: {diag[:60]}…)")
    # 기록 문장의 숫자 (첫 판 0.1885 e · 7,580 · MLi_04 0.00064 e · 692) 와 대조
    for key, neg, nmax in (("MP_07", 0.1885, 7580), ("MLi_04", 0.00064, 692)):
        if f"{nmax:,}" not in rec2 or by[key]["maxima"] != nmax:
            raise Refuse(f"{key}: 극대 수 {by[key]['maxima']} 가 기록 ({nmax:,}) 과 다르다")
        if by[key]["neg_rho_up"] is None or abs(by[key]["neg_rho_up"] - neg) > 0.02 * neg:
            raise Refuse(f"{key}: 음의 밀도 {by[key]['neg_rho_up']} 가 기록 {neg} 와 다르다")
    q3 = by.get("Q3_1019")
    if q3 and (q3["nat"], q3["maxima"]) != (120, 940):
        raise Refuse(f"Q3: (원자, 극대) = ({q3['nat']}, {q3['maxima']}) ≠ 기록 (120, 940)")
    return rows


def _selftest() -> int:
    ok = bad = 0

    def chk(c, m):
        nonlocal ok, bad
        print(("  ✓ " if c else "  ✗ ") + m)
        ok, bad = ok + bool(c), bad + (not c)

    rows = compute()
    by = {r["key"]: r for r in rows}
    chk(by["MP_07"]["maxima"] == 7580 and by["MLi_04"]["maxima"] == 692 and by["Q3_1019"]["maxima"] == 940,
        "[양성] 유의 극대 수 = bader_run.out = 기록 (7,580 · 692 · 940)")
    chk(round(by["MP_07"]["maxima"] / by["MP_07"]["nat"]) == 115 and round(by["MLi_04"]["maxima"] / 58) == 12,
        "[양성] 원자당 극대 = 기록 (MP_07 115 · MLi_04 12)")
    chk(by["Q3_1019"]["neg_rho_up"] is None, "[양성] Q3 pp_ae.out 에 negative rho 줄 없음 → None (0 아님)")

    def refused_by(fn, needle):
        try:
            fn()
        except Refuse as e:
            return needle in str(e)
        return False

    mli = species(MODELS[1][1] / "scf_input_copy.in")
    mp = species(MODELS[0][1] / "scf_input_copy.in")
    chk(refused_by(lambda: compute(sp_for={"MP_07": mli}), "원소 목록이 이 셀 것이 아니다"),
        "[음성] MP_07 에 MLi_04 원소 목록 (58 원자) 을 넣으면 원자 번호 검사가 거부")
    swapped = list(mp)
    i_li, i_s = swapped.index("Li"), swapped.index("S")
    swapped[i_li], swapped[i_s] = swapped[i_s], swapped[i_li]
    chk(refused_by(lambda: compute(sp_for={"MP_07": swapped}), "원소별 극대/원자"),
        "[음성] MP_07 원소 순서를 한 쌍 (Li↔S) 바꾸면 원소별 기록 대조가 거부")
    fake = pathlib.Path(__file__).resolve().parent / "__nonexistent__"
    chk(not fake.exists() and _raises(lambda: compute(models=((MODELS[0][0], fake, "x", "#000"),) + MODELS[1:])),
        "[음성] 폴더가 없으면 그리지 않는다 (예외)")
    pre = "     negative rho (up, down):  1.885E-01 0.000E+00\n"
    post = "     Calling punch_plot, plot_num =  17\n"
    tmp = OUT.parent / ".selftest_pp.out"
    try:
        tmp.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(post + pre)
        chk(negative_rho_up(tmp) is None, "[음성] punch_plot **뒤**에 찍힌 negative rho 줄은 읽지 않는다")
        tmp.write_text(pre + post)
        chk(abs(negative_rho_up(tmp) - 0.1885) < 1e-9, "[양성] punch_plot 앞 줄은 읽는다")
    finally:
        tmp.unlink(missing_ok=True)
    print(f"fig selftest: ✓ {ok} · ✗ {bad}")
    return 0 if bad == 0 else 1


def _raises(fn) -> bool:
    try:
        fn()
    except (Refuse, FileNotFoundError, OSError):
        return True
    return False


def main() -> int:
    if "--selftest" in sys.argv:
        return _selftest()
    rows = compute()
    print("교차검산 ✓ " + " · ".join(f"{r['key']} 극대 {r['maxima']:,} / {r['nat']} 원자" for r in rows))

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    OUT.mkdir(parents=True, exist_ok=True)
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(10.6, 4.3), gridspec_kw={"width_ratios": [2.3, 1.0]})
    w = 0.27
    x = np.arange(len(ELEMS))
    rng = np.random.default_rng(20261101)                   # 점 흩뿌림만 (값은 안 바뀐다) · 고정 시드
    for j, (key, _, label, col) in enumerate(MODELS):
        r = next(t for t in rows if t["key"] == key)
        for i, el in enumerate(ELEMS):
            v = r["per_elem"].get(el)
            if not v:
                continue
            xc = x[i] + (j - 1) * w
            ax.scatter(xc + rng.uniform(-0.07, 0.07, len(v["counts"])), v["counts"], s=11, color=col,
                       alpha=0.75 if key != "Q3_1019" else 0.5, lw=0, zorder=3)
            ax.plot([xc - 0.11, xc + 0.11], [v["upper_median"]] * 2, color=H.INK, lw=1.6, zorder=4)
        ax.scatter([], [], s=22, color=col, label=f"{label}: {r['maxima'] / r['nat']:.1f} maxima/atom")
    ax.plot([], [], color=H.INK, lw=1.6, label="upper median per element")
    ax.set_yscale("log")
    ax.set_ylim(0.7, 4000)                                  # 위 한 자릿수는 범례 자리 (점과 안 겹친다)
    ax.set_xticks(x, ELEMS)
    H.apply_axes(ax, xlabel="element (one dot = one atom)",
                 ylabel="significant Bader maxima on the atom", title="(a) Bader maxima per atom", fontsize=11)
    ax.legend(fontsize=7.6, frameon=False, loc="upper right", ncol=1)
    keys = [k for k, _, _, _ in MODELS]
    vals = [next(t for t in rows if t["key"] == k)["neg_rho_up"] for k in keys]
    for i, (k, v) in enumerate(zip(keys, vals)):
        col = MODELS[i][3]
        if v is None:
            bx.text(i, 1.5e-4, "not printed", ha="center", va="bottom", fontsize=8.5, color=H.MUT, rotation=90)
        else:
            bx.bar(i, v, 0.6, color=col, alpha=0.9)
            bx.text(i, v * 1.25, f"{v:.2g} e", ha="center", va="bottom", fontsize=8.5, color=H.INK)
    bx.set_yscale("log")
    bx.set_ylim(1e-4, 1.0)
    bx.set_xticks(range(len(keys)), ["MP_07", "MLi_04", "Q3 (Oct 19)"])
    H.apply_axes(bx, xlabel="", ylabel="negative density before AE reconstruction (e)",
                 title="(b) pp.x 'negative rho' (up)", fontsize=11)
    fig.suptitle("Nd Q3' same-cell Bader: the Nd-on-P density is noisy, so its charges are on hold "
                 "(same-input SCF rerun queued)", fontsize=11, color=H.INK)
    fig.tight_layout()
    png = OUT / "nd_q3p_bader_density_check.png"
    fig.savefig(png, dpi=300)
    src = {k: str(f.relative_to(R)) for k, f, _, _ in MODELS}
    with CSV.open("w", newline="") as f:
        wr = csv.writer(f)
        # 원자 한 줄 (Origin 점 그림 그대로) · 음의 밀도 칸은 줄이 없으면 빈칸 (0 아님)
        wr.writerow(["model", "cell_atoms", "atom_index_1based", "element", "maxima_on_atom",
                     "element_upper_median", "cell_significant_maxima", "negative_rho_up_e_before_AE",
                     "source_dir"])
        for r in rows:
            neg = "" if r["neg_rho_up"] is None else f"{r['neg_rho_up']:.4E}"
            for el in ELEMS:
                v = r["per_elem"].get(el)
                for i, c in zip(v["idx"], v["counts"]) if v else ():
                    wr.writerow([r["key"], r["nat"], i, el, c, v["upper_median"], r["maxima"], neg, src[r["key"]]])
    print(f"→ {png.relative_to(R)} · {CSV.relative_to(R)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
