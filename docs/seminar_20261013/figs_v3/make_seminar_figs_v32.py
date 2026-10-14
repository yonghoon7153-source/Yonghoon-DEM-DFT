"""연구세미나 덱 v3.2 (2026-10-14) — 새 그림 하나: Problem 4 (판 반력 "300 MPa" 의 속) — F_p4.

값은 전부 기록된 값 그대로 (새 계산 없음 · --selftest 가 아래 정본 파일에서 같은 글자를 찾는다):
  docs/data/ps73_damping_branch_20261007/README.md  §1 (원 런 이완 끝 165.34 MPa) · §4 (등록 예측 B2 띠 8.3–11.7 % · 10.0 %) ·
                                                    §12-4 (가지 B: 멈춘 step 300.906 MPa · 111.052 µm · ε_sphere 14.953 % · 감쇠 저항 434.18 N = 57.89 % ·
                                                           서보 유지 끝 299.274 MPa · 105.842 µm · ε_sphere 10.769 %)
  docs/reviews/findings.json DEMP-01 (434.3 N · 57.9 %)
한정어 (그림에 같이): 한 침대 · 모델 내부 진단값 — 서보 유지 끝 = 빗금 (MV-01 · 02 · 08 검사 전) · ε_sphere ≠ exact union.
양식 = make_seminar_figs.py (v3) 그대로 (글씨 ≈ 12 pt · 배치 1:1 · png + svg + csv · 그려진 글자 겹침 0).
실행: python3 make_seminar_figs_v32.py <out_dir>   · selftest: python3 make_seminar_figs_v32.py --selftest [<리포>]
"""
import csv
import json
import sys
from pathlib import Path

import make_seminar_figs as m   # 같은 폴더 (v3 양식 · rcParams · 색 · _save · _fmt · 겹침 검사)
plt = m.plt

README = "docs/data/ps73_damping_branch_20261007/README.md"
# 기록된 값 (문자열 = README 의 글자 그대로 · selftest 가 찾는다)
P4 = dict(
    stop_MPa="300.906", relaxed_MPa="165.34", hold_MPa="299.274",          # §12-4 · §1 · §12-4
    stop_eps="14.953", hold_eps="10.769",                                  # §12-4 ε_sphere (%)
    stop_um="111.052", hold_um="105.842",                                  # §12-4 두께 (µm)
    drag_N="434.18", drag_pct="57.89",                                     # §12-4 멈춘 step 감쇠 저항 (750 N 의 %)
    band_lo="8.3", band_hi="11.7", band_point="10.0",                      # §4 B2 등록 띠 · 점 (ε_sphere %)
)
HATCH = "////"


def fig_p4(out):
    v = {k: float(s) for k, s in P4.items()}
    fig, (a, b) = plt.subplots(1, 2, figsize=(13.8 * m.CM, 6.9 * m.CM), gridspec_kw=dict(width_ratios=[1.45, 1.0]))
    # (a) 판 압력 세 상태 — 멈춘 step (감쇠 0.5 · 판 이동 중) · 판 고정 이완 끝 (원 런 · 감쇠 1e-5) · 서보 유지 끝 (가지 B · 감쇠 1e-5)
    xa = [0, 1, 2]
    vals_a = [v["stop_MPa"], v["relaxed_MPa"], v["hold_MPa"]]
    cols_a = [m.NAVY, m.GRAY, m.NAVY]
    hat_a = [None, None, HATCH]
    for x, y, c, h in zip(xa, vals_a, cols_a, hat_a):
        a.bar(x, y, 0.68, color=c, hatch=h, edgecolor="white" if h else c, lw=0.6)
        a.text(x, y + 8, f"{y:.1f}", ha="center", va="bottom", fontsize=11, color="#333333")
    # 멈춘 step 의 감쇠 저항 몫 (목표 판 힘 750 N 대비 · 기록값) — 막대 안 흰 글씨
    a.text(0, v["stop_MPa"] / 2, f"drag\n{v['drag_pct']:.1f} %", ha="center", va="center", fontsize=10, color="white", linespacing=1.15)
    a.set_xticks(xa)
    a.set_xticklabels(["stop\nγ 0.5", "relaxed\nγ 1e-5", "servo end\nγ 1e-5"], fontsize=10.5)
    a.set_ylabel("Plate pressure (MPa)")
    a.set_ylim(0, 380)
    a.set_xlim(-0.55, 2.55)
    a.set_title("(a)", loc="left")
    m._fmt(a, ny=4)
    # (b) ε_sphere 멈춘 step ↔ 서보 유지 끝 · 등록 띠 (런 전) 는 서보 막대 자리에만
    xb = [0, 1.6]
    b.fill_between([xb[1] - 0.42, xb[1] + 0.42], v["band_lo"], v["band_hi"], color=m.LIGHT, alpha=0.55, lw=0)
    b.hlines(v["band_point"], xb[1] - 0.42, xb[1] + 0.42, colors=m.GRAY, linestyles="--", lw=1.0)
    for x, y, h in zip(xb, [v["stop_eps"], v["hold_eps"]], [None, HATCH]):
        b.bar(x, y, 0.62, color=m.NAVY, hatch=h, edgecolor="white" if h else m.NAVY, lw=0.6)
        b.text(x, y + 0.45, f"{y:.2f}", ha="center", va="bottom", fontsize=11, color="#333333")
    b.set_xticks(xb)
    b.set_xticklabels([f"stop\n{v['stop_um']:.2f} µm", f"servo end\n{v['hold_um']:.2f} µm"], fontsize=10)
    b.set_ylabel("ε$_{sphere}$ (%)")
    b.set_ylim(0, 18)
    b.set_xlim(-0.75, 2.35)
    b.set_title("(b)", loc="left")
    m._fmt(b, ny=4)
    fig.tight_layout(pad=0.3, w_pad=1.6)
    rows = [("a", "stop (damping 0.5, plate moving)", P4["stop_MPa"], "MPa", "README §12-4"),
            ("a", "relaxed at fixed platen (original run, damping 1e-5)", P4["relaxed_MPa"], "MPa", "README §1"),
            ("a", "servo hold end (branch B, damping 1e-5)", P4["hold_MPa"], "MPa", "README §12-4"),
            ("a", "damping drag at stop (share of 750 N target)", P4["drag_pct"], "%", "README §12-4"),
            ("b", "stop eps_sphere", P4["stop_eps"], "%", "README §12-4"),
            ("b", "servo hold end eps_sphere", P4["hold_eps"], "%", "README §12-4"),
            ("b", "stop thickness", P4["stop_um"], "um", "README §12-4"),
            ("b", "servo hold end thickness", P4["hold_um"], "um", "README §12-4"),
            ("b", "registered band low (before the run)", P4["band_lo"], "%", "README §4 B2"),
            ("b", "registered band high (before the run)", P4["band_hi"], "%", "README §4 B2"),
            ("b", "registered point (before the run)", P4["band_point"], "%", "README §4 B2")]
    m._save(fig, out, "F_p4", rows=rows, header=["panel", "state", "value (as recorded)", "unit", "source"])


def selftest(repo=m.REPO):
    repo = Path(repo)
    t = (repo / README).read_text(encoding="utf-8")
    sec12 = t[t.index("### 12-4"):]
    sec1 = t[t.index("## 1. 출발점"):t.index("## 2. 갈래")]
    sec4 = t[t.index("## 4. 사전 등록 예측"):t.index("## 5. 분석 계획")]
    for k in ("stop_MPa", "hold_MPa", "stop_eps", "hold_eps", "stop_um", "hold_um", "drag_N", "drag_pct"):
        assert P4[k] in sec12, (k, P4[k], "not in README §12-4")
    assert P4["relaxed_MPa"] + " MPa" in sec1, "165.34 MPa not in README §1"
    assert f"ε {P4['band_lo']}–{P4['band_hi']} %" in sec4 and f"ε_sphere **{P4['band_point']} %**" in sec4, "B2 band / point not in README §4"
    led = json.loads((repo / "docs/reviews/findings.json").read_text(encoding="utf-8"))
    led = led["findings"] if isinstance(led, dict) else led
    demp = next(f for f in led if f.get("id") == "DEMP-01")
    assert "434.3 N" in demp["title"] and "57.9 %" in demp["title"], "DEMP-01 title values"
    assert demp["status"] == "open"
    for k in ("MV-01", "MV-02", "MV-08"):
        assert next(f for f in led if f.get("id") == k)["status"] == "open", k
    ban = json.loads((repo / "docs/reviews/claims.json").read_text(encoding="utf-8")).get("quotation_ban", [])
    pats = [q.get("pattern") if isinstance(q, dict) else q for q in ban]
    src = Path(__file__).read_text(encoding="utf-8")
    hits = [p for p in pats if p and p in src]
    assert not hits, hits
    import tempfile
    m.OVERLAPS.clear()
    with tempfile.TemporaryDirectory() as d:
        fig_p4(d)
        with open(Path(d, "F_p4.csv"), encoding="utf-8") as f:
            vals = {r[1]: r[2] for r in list(csv.reader(f))[1:]}
        assert set(vals.values()) <= set(P4.values()), "F_p4.csv carries only recorded strings"
        svg = Path(d, "F_p4.svg").read_text(encoding="utf-8")
        for s in ("300.9", "165.3", "299.3", "14.95", "10.77", "111.05", "105.84", "57.9"):
            assert s in svg, s
        assert "static" not in svg.lower(), "no 'static' wording in the figure (MV-01)"
    assert not m.OVERLAPS, f"overlapping text in F_p4: {m.OVERLAPS}"
    print("selftest ok — F_p4 values = recorded strings in README §1 · §4 · §12-4 and DEMP-01 · no banned strings · no overlapping text")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest(sys.argv[2] if len(sys.argv) > 2 else m.REPO)
    else:
        out = sys.argv[1] if len(sys.argv) > 1 else "."
        Path(out).mkdir(parents=True, exist_ok=True)
        fig_p4(out)
        print("written", out)
