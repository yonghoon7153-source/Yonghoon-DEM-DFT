#!/usr/bin/env python3
"""fig_weekly_2026_09_27.py — 주간보고(2026-09-21 ~ 09-27) 그림 3장 + Origin CSV 4벌.

  (1) review_traffic.png — 이번 주 리뷰 왕복 지도
      (a) 채널별 회신 타임라인: li2s 외부 1저자 · Codex(W_ad 계획 / A′ 카드) · Codex(V5 VASP 외주 준비본)
          색 = 판정. Codex 판정은 **점착 원장** `reviews[].verdict` 에서, 날짜는 `kb/reviews/INDEX.md` 의
          회신 파일 이름에서 읽는다. li2s 회신은 GO/NO-GO 가 아니라 규칙·판정 회신이라 회색이다.
      (b) V5 VASP 준비본 라운드별 P0·P1 개수 (CE → CK) — 회신 원문의 `### P0-n` / `### P1-n` 제목을 센다
          (CI·CJ 는 `## … — P1 하나 / P1 한 묶음` 절 제목 형식이라 1 로 센다).
  (2) b2o3_event_rate.png — b2o3 골격 사건 빈도. 값은 결과 기록의 봉인 문장과 **글자 단위로 대조**한 뒤 그린다.
      대조군(30 런 · 사건 0)의 단측 95 % 상한은 설계(런 수 · 길이 · 온도 수)에서 다시 계산해 기록 문장과 맞춘다.
  (3) li2s_glass_week.png — (a) 담금질 중 P 4배위 이탈 프레임 비율 (시드 5 × 구간 3)
                           (b) MSD 지수 β vs 카드 C2 게이트 띠 (σ = 블록 부트스트랩 사다리 끝 = 하한)

    python3 tools/figures/fig_weekly_2026_09_27.py            # PNG 3장 + CSV 4벌
    python3 tools/figures/fig_weekly_2026_09_27.py --selftest # 양성 + 음성

이 도구가 **못 하는 것**
  · 값을 판정하지 않는다 — 전부 원장·회신 원문에서 읽고, 교차검산이 틀리면 **그리지 않는다**.
  · ⛔ W_ad 숫자(SE|SE 4층 · A′ V2 W_sep · ATM 열)는 그리지 않는다. 결과 기록이 *"원장·화면 게재는
    1저자 별도"* 로 막아 두었고, 점착 원장 판정 문장도 숫자 없이 적는다.
  · b2o3: 사건 빈도는 **이온 이동 장벽도 전도도도 아니다** (카드 금지). 포아송(Garwood) 구간은 사건 독립을
    가정하는데 런이 과분산(분산/평균 2.3–17.5)이라 **구간이 좁게 나온다** — 그림에 적는다.
    대조군과는 셀이 다르다(558 vs 512 원자) — 셀당 비교는 어림이다.
  · li2s: **외부 1저자 트랙**이다. β·배위 통계는 내부 진단(`citable: false`)이고 판정은 외부 1저자 몫이다.
    배위는 거리 컷(R_PS 2.6 Å) 기준 — 결합 차수를 안 보고, 1 프레임짜리 이탈은 열진동일 수 있다.
  · 리뷰 P0/P1 개수는 **제목 세기 규칙**이다. 회신이 제목 없이 본문으로만 적으면 못 센다 —
    그때는 NO-GO 인데 0 개가 되므로 **죽는다** (0 으로 두지 않는다).
  · 다른 주의 그림을 만들지 않는다 — 날짜가 파일명에 박힌 일회성 산출물이다.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import pathlib
import re
import sys

R = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/figures"))
import house_style as H  # noqa: E402

DB = R / "db/properties"
OUT = R / "docs/figures/weekly_2026_09_27"

PIPE = R / "db/pipelines/adhesion_pipeline.json"
RIDX = R / "kb/reviews/INDEX.md"
REVDIR = R / "kb/reviews"
B2O3 = DB / "b2o3_framework_event_rate_result_2026_09_26.json"
PCOORD = R / "db/raw/lpscl_smallcell_glass_cc_2026_09_26/p_coord_5seeds_cd_2026_09_27.json"
FOLLOW = DB / "lpscl_smallcell_glass_md_cc_followup_2026_09_26.json"
CARD = DB / "lpscl_smallcell_glass_md_estimand_2026_09_21.json"

WEEK = (dt.date(2026, 9, 21), dt.date(2026, 9, 27))
V5_ROUNDS = ("CE", "CF", "CG", "CI", "CJ", "CK")

# 판정 색 — 원소 팔레트와 별개인 의미색 (good / warning / critical)
VCOL = {"nogo": "#b91c1c", "cond": "#d97706", "go": "#15803d", "reply": "#6b7280", "sent": "#6b7280"}
VLAB = {"nogo": "NO-GO", "cond": "conditional GO", "go": "GO",
        "reply": "reply (rules / judgments — not a GO vote)", "sent": "sent, reply pending"}
CHAN = ("li2s", "wad", "v5")
CHAN_LAB = {"li2s": "li2s glass\nexternal first author",
            "wad": "Codex + internal\nW_ad plan, A′ pilot card",
            "v5": "Codex\nV5 VASP outsourcing pkg"}


def _rel(p) -> str:
    p = pathlib.Path(p)
    try:
        return str(p.relative_to(R))
    except ValueError:
        return str(p)


def _date_from_name(name: str) -> dt.date:
    m = re.search(r"_(\d{4})_(\d{2})_(\d{2})\.md$", name)
    if not m:
        raise ValueError(f"파일 이름에 날짜가 없다: {name}")
    return dt.date(int(m[1]), int(m[2]), int(m[3]))


def _verdict_class(v: str) -> str:
    v = (v or "").strip()
    if v.startswith("NO-GO"):
        return "nogo"
    if v.startswith("조건부 GO"):
        return "cond"
    if v.startswith("GO"):
        return "go"
    raise ValueError(f"판정 문장을 분류 못 했다: {v[:40]!r}")


def count_findings(text: str) -> tuple[int, int]:
    """회신 원문 → (P0, P1). 번호 제목(`### P0-3.`)을 중복 없이 센다.
    CI·CJ 처럼 절 제목이 `## … — P1 하나` / `P1 한 묶음` 이면 1 로 센다."""
    n = {}
    for lv in ("P0", "P1"):
        k = len(set(re.findall(rf"^###\s*{lv}-(\d+)", text, re.M)))
        if k == 0 and re.search(rf"^##\s.*{lv} (하나|한 묶음)", text, re.M):
            k = 1
        n[lv] = k
    return n["P0"], n["P1"]


def load_reviews(idx=RIDX, pipe=PIPE, revdir=REVDIR) -> dict:
    """INDEX 표 행 + 점착 원장 판정 → 이번 주 리뷰 목록. ⛔ 판정을 만들지 않는다 — 원장에서 읽는다."""
    led = json.loads(pathlib.Path(pipe).read_text(encoding="utf-8"))
    # 원장 reviews[] 는 두 판이 섞여 있다 — 앞 넷은 `record`, BY 부터는 `reply` 가 회신 파일이다
    by_rec = {}
    for r in led.get("reviews", []):
        for key in ("record", "reply"):
            if r.get(key):
                by_rec[pathlib.Path(r[key]).name] = r
    row = re.compile(r"^\| ([A-Z]{1,3}) \| (\d{4}-\d{2}-\d{2}) \| `([^`]+)` \| (?:`([^`]+)`|—) \|")
    items = []
    for ln in pathlib.Path(idx).read_text(encoding="utf-8").splitlines():
        m = row.match(ln)
        if not m:
            continue
        letter, pdate, prompt, reply = m[1], dt.date.fromisoformat(m[2]), m[3], m[4]
        when = _date_from_name(reply) if reply else _date_from_name(prompt)
        if not (WEEK[0] <= when <= WEEK[1] or WEEK[0] <= pdate <= WEEK[1]):
            continue
        if prompt.startswith("li2s1a_"):
            chan = "li2s"
        elif prompt.startswith("codex_"):
            chan = "v5" if "v5_vasp" in prompt else "wad"
        else:
            raise ValueError(f"채널을 모르는 편지: {letter} {prompt}")
        if not reply:
            vc = "sent"
        elif chan == "li2s":
            vc = "reply"
        else:
            rv = by_rec.get(reply)
            if rv is None:
                raise ValueError(f"점착 원장에 {letter} 회신 판정이 없다 ({reply})")
            vc = _verdict_class(rv.get("verdict", ""))
        it = {"letter": letter, "chan": chan, "date": when, "vclass": vc,
              "reply": reply or "", "p0": None, "p1": None}
        if chan == "v5" and reply:
            p0, p1 = count_findings((pathlib.Path(revdir) / reply).read_text(encoding="utf-8"))
            if vc == "nogo" and p0 + p1 == 0:
                raise ValueError(f"{letter}: NO-GO 인데 P0/P1 을 못 셌다 (회신 형식이 바뀌었나)")
            if vc == "go" and p0 + p1 > 0:
                raise ValueError(f"{letter}: GO 인데 P0/P1 이 {p0}/{p1} 남았다 — 모순")
            it["p0"], it["p1"] = p0, p1
        items.append(it)
    # 내부 리뷰(편지 번호 없음)는 원장에서만 온다
    for name, rv in by_rec.items():
        if name.startswith("internal_review_") and "wad" in name:
            when = _date_from_name(name)
            if WEEK[0] <= when <= WEEK[1]:
                items.append({"letter": "Fable", "chan": "wad", "date": when,
                              "vclass": _verdict_class(rv.get("verdict", "")),
                              "reply": name, "p0": None, "p1": None, "internal": True})
    if not items:
        raise ValueError("이번 주 리뷰가 하나도 안 읽혔다")
    v5 = [it for it in items if it["chan"] == "v5"]
    if [it["letter"] for it in sorted(v5, key=lambda x: x["letter"])] != list(V5_ROUNDS):
        raise ValueError(f"V5 라운드가 {V5_ROUNDS} 와 다르다: {[it['letter'] for it in v5]}")
    return {"items": items, "source": [_rel(idx), _rel(pipe), _rel(revdir) + "/codex_C[E-K]_reply_*.md"]}


def load_b2o3(p=B2O3) -> dict:
    d = json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
    rep = d[next(k for k in d if k.startswith("온도별_보고량"))]
    sealed = d[next(k for k in d if k.startswith("봉인_문장"))]
    ctrl = d[next(k for k in d if k.startswith("대조군"))]["문장"]
    groups = ("P_center", "S_free", "Cl")
    temps = sorted(rep, key=float)
    rows = []
    for T in temps:
        for g in groups:
            v = rep[T][g]
            lo, hi = v["ci95"]
            want = (f"{T} K 에서 {g} 사건 빈도는 {v['rate_per_ns_cell']:.2f} /ns/셀 "
                    f"[{lo:.2f}, {hi:.2f}] 이고 5런 중 {v['k_runs']} 런에서 났다.")
            if want not in sealed:
                raise ValueError(f"봉인 문장과 다르다: {T} K {g}")
            rows.append({"T": int(T), "g": g, "rate": v["rate_per_ns_cell"], "lo": lo, "hi": hi,
                         "k": v["k_runs"], "n": v["k_of"], "sum": v["sum_N_ev"],
                         "disp": v["dispersion_index_var_over_mean"]})
    m_runs = re.search(r"(\d+) 런", ctrl)
    m_ps = re.search(r"(\d+) ps", ctrl)
    m_T = re.search(r"(\d+(?:/\d+)+) K", ctrl)
    m_ub = re.search(r"온도당 단측 95 % 상한 ≈ ([0-9.]+)", ctrl)
    if not (m_runs and m_ps and m_T and m_ub):
        raise ValueError("대조군 문장에서 설계(런·길이·온도·상한)를 못 읽었다")
    n_T = len(m_T[1].split("/"))
    exposure_ns = int(m_runs[1]) / n_T * int(m_ps[1]) / 1000.0
    ub = -math.log(0.05) / exposure_ns        # 사건 0 의 포아송 단측 95 % 상한
    if abs(ub - float(m_ub[1])) > 0.01:
        raise ValueError(f"대조군 상한 재계산 {ub:.3f} 이 기록 {m_ub[1]} 와 다르다")
    disp = [r["disp"] for r in rows]
    return {"rows": rows, "temps": [int(t) for t in temps], "groups": groups,
            "ctrl_ub": ub, "ctrl_runs": int(m_runs[1]), "disp_range": (min(disp), max(disp)),
            "source": [_rel(p)]}


def load_pcoord(p=PCOORD) -> dict:
    d = json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
    tr = d["trajectory"]
    want = {}
    for key, pat in (("melt_hold", r"용융 유지 (\d+)"), ("quench", r"냉각 (\d+)"),
                     ("final_hold", r"최종 유지 (\d+)")):
        m = re.search(pat, tr)
        if not m:
            raise ValueError(f"궤적 설명에서 {key} 프레임 수를 못 읽었다")
        want[key] = int(m[1])
    seeds = sorted(d["seeds"], key=lambda s: int(re.sub(r"\D", "", s)))
    out = {}
    for s in seeds:
        f = d["seeds"][s]["frames_any_not4"]
        out[s] = {}
        for st in ("melt_hold", "quench", "final_hold"):
            n, N = f[st]
            if N != want[st] or not (0 <= n <= N):
                raise ValueError(f"{s} {st}: {n}/{N} — 궤적 설명({want[st]} 프레임)과 안 맞는다")
            out[s][st] = (n, N)
    return {"seeds": seeds, "frames": out, "stages_N": want, "source": [_rel(p)]}


def load_beta(follow=FOLLOW, card=CARD) -> dict:
    f = json.loads(pathlib.Path(follow).read_text(encoding="utf-8"))
    c = json.loads(pathlib.Path(card).read_text(encoding="utf-8"))
    band_txt = c["5_게이트_결과_보기_전"]["C2_beta"]
    m = re.search(r"\*\*([0-9.]+)–([0-9.]+)\*\*", band_txt)
    if not m:
        raise ValueError("카드 C2 에서 β 띠를 못 읽었다")
    lo, hi = float(m[1]), float(m[2])
    cons = f["회신_CD_판정_2026_09_27"]["보수값_재계산"]
    spec = (("P-2_550K_MTO", 550, 400), ("P-1_400K_400ps_MTO", 400, 400),
            ("pilot800_400K_MTO", 400, 800))
    runs = []
    for key, T, ps in spec:
        v = cons[key]
        dos = (v["beta"] - lo) / v["sigma_ladder_end"]
        if abs(dos - v["d_over_sigma"]) > 0.1:
            raise ValueError(f"{key}: (β−{lo})/σ = {dos:.2f} 가 원장 {v['d_over_sigma']} 와 다르다")
        runs.append({"key": key, "T": T, "ps": ps, "beta": v["beta"],
                     "sigma": v["sigma_ladder_end"], "dos": v["d_over_sigma"]})
    return {"band": (lo, hi), "runs": runs, "source": [_rel(follow), _rel(card)]}


# ────────────────────────────────────────────────────────────── 그림
def _plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return plt


def fig_reviews(rv: dict, out_png=OUT / "review_traffic.png") -> str:
    plt = _plt()
    from matplotlib.lines import Line2D
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(14.2, 5.4),
                                 gridspec_kw={"width_ratios": [2.35, 1]})
    days = [WEEK[0] + dt.timedelta(d) for d in range(7)]
    ypos = {"li2s": 2, "wad": 1, "v5": 0}
    cells = {}
    for it in sorted(rv["items"], key=lambda x: (x["date"], x["letter"] != "Fable", x["letter"])):
        cells.setdefault((it["chan"], it["date"]), []).append(it)
    for (ch, day), grp in cells.items():
        n = len(grp)
        for i, it in enumerate(grp):
            x = (day - WEEK[0]).days + (i - (n - 1) / 2) * 0.19   # 0.15 면 편지 라벨이 붙는다
            y = ypos[ch]
            col = VCOL[it["vclass"]]
            mk = "D" if it.get("internal") else "o"
            face = "white" if it["vclass"] == "sent" else col
            ax.scatter([x], [y], s=150, marker=mk, facecolor=face, edgecolor=col, lw=1.8, zorder=3)
            ax.text(x, y + 0.2, it["letter"], ha="center", va="bottom", fontsize=8.5,
                    color=H.INK, rotation=90 if it["letter"] == "Fable" else 0)
    ax.set_xlim(-0.6, 6.6)
    ax.set_ylim(-0.6, 2.85)
    ax.set_xticks(range(7))
    ax.set_xticklabels([d.strftime("%b %d\n%a") for d in days])
    ax.set_yticks([ypos[c] for c in CHAN])
    ax.set_yticklabels([CHAN_LAB[c] for c in CHAN], fontsize=9.5)
    for y in (0.5, 1.5):
        ax.axhline(y, color="#e5e7eb", lw=0.8, zorder=0)
    n_letters = sum(1 for it in rv["items"] if not it.get("internal"))
    H.apply_axes(ax, title=f"(a)  Review round-trips, Sep 21–27  ({n_letters} letters + 1 internal review)")
    handles = [Line2D([], [], marker="o", ls="", markersize=9, markerfacecolor=VCOL[k],
                      markeredgecolor=VCOL[k], label=VLAB[k]) for k in ("nogo", "cond", "go", "reply")]
    handles.append(Line2D([], [], marker="o", ls="", markersize=9, markerfacecolor="white",
                          markeredgecolor=VCOL["sent"], label=VLAB["sent"]))
    handles.append(Line2D([], [], marker="D", ls="", markersize=8, markerfacecolor=VCOL["nogo"],
                          markeredgecolor=VCOL["nogo"], label="internal review (Fable)"))
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3,
              frameon=False, fontsize=8.8)

    v5 = sorted((it for it in rv["items"] if it["chan"] == "v5"), key=lambda x: x["letter"])
    xs = list(range(len(v5)))
    w = 0.36
    p0 = [it["p0"] for it in v5]
    p1 = [it["p1"] for it in v5]
    bx.bar([x - w / 2 for x in xs], p0, w, color=VCOL["nogo"], label="P0  critical")
    bx.bar([x + w / 2 for x in xs], p1, w, color=VCOL["cond"], label="P1  required fix")
    for x, a, b in zip(xs, p0, p1):
        bx.text(x - w / 2, a + 0.08, str(a), ha="center", va="bottom", fontsize=9, color=H.INK)
        bx.text(x + w / 2, b + 0.08, str(b), ha="center", va="bottom", fontsize=9, color=H.INK)
    bx.set_xticks(xs)
    bx.set_xticklabels([it["letter"] for it in v5])
    last = v5[-1]
    if last["vclass"] == "go":
        bx.annotate("GO\n(technical review only —\nnot approval to run or cite)",
                    xy=(xs[-1], 0.15), xytext=(xs[-1] - 0.35, 3.2), ha="center", fontsize=8.5,
                    color=VCOL["go"], arrowprops=dict(arrowstyle="->", color=VCOL["go"], lw=1))
    bx.set_ylim(0, max(p0 + p1) + 1.4)
    H.apply_axes(bx, xlabel="review round (all on Sep 27)", ylabel="findings that block sending",
                 title="(b)  V5 package: fixes converge to zero")
    bx.legend(frameon=False, fontsize=9, loc="upper right")
    fig.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return _rel(out_png)


GLAB = {"P_center": "P center (whole PS$_4$ / PS$_3$O unit)", "S_free": "free S", "Cl": "Cl"}
GCOL = {"P_center": H.ELEM["P"], "S_free": H.ELEM["S"], "Cl": H.ELEM["Cl"]}


def fig_b2o3(b: dict, out_png=OUT / "b2o3_event_rate.png") -> str:
    plt = _plt()
    fig, ax = plt.subplots(figsize=(9.2, 5.4))
    w = 0.26
    for j, g in enumerate(b["groups"]):
        for i, T in enumerate(b["temps"]):
            r = next(x for x in b["rows"] if x["T"] == T and x["g"] == g)
            x = i + (j - 1) * w
            ax.bar(x, r["rate"], w * 0.92, color=GCOL[g], label=GLAB[g] if i == 0 else None)
            ax.errorbar(x, r["rate"], yerr=[[r["rate"] - r["lo"]], [r["hi"] - r["rate"]]],
                        fmt="none", ecolor=H.INK, elinewidth=1, capsize=3)
            ax.text(x, r["hi"] * 1.12, f"{r['k']}/{r['n']}", ha="center", va="bottom",
                    fontsize=8.5, color=H.MUT)
    # 대조군 선의 설명은 막대 위에 얹지 않는다 — 오른쪽 끝에 자리를 내서 선 옆에 붙인다
    ax.axhline(b["ctrl_ub"], color=H.MUT, ls="--", lw=1.2)
    ax.text(2.5, b["ctrl_ub"],
            f"control: LPSCl1.6 + LPSOCl1.6\n{b['ctrl_runs']} runs, 0 events\n"
            f"one-sided 95 % upper\nbound per T = {b['ctrl_ub']:.2f}",
            ha="left", va="center", fontsize=8.5, color=H.MUT)
    ax.set_yscale("log")
    ax.set_ylim(0.3, 250)
    ax.set_xlim(-0.5, 3.3)
    ax.set_xticks(range(len(b["temps"])))
    ax.set_xticklabels([f"{T} K" for T in b["temps"]])
    H.apply_axes(ax, ylabel="framework-site events per ns per cell",
                 title="B2O3@LPSCl1.6 framework events  (512 atoms · 5 seeds × 400 ps per T)")
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    lo, hi = b["disp_range"]
    # 각주는 축 폭 안에 들게 줄을 나눈다 (길면 tight bbox 가 캔버스를 오른쪽으로 늘린다)
    ax.text(0.0, -0.12,
            "Values = sealed sentences of the pre-registered card.  x/5 = runs with ≥ 1 event.\n"
            "Event frequency — not an ion-migration barrier, not a conductivity.\n"
            "Error bars: Poisson CI95 (assumes independent events). Runs are over-dispersed\n"
            f"(var/mean {lo:.1f}–{hi:.1f}), so these CIs are too narrow.  "
            "No P-bonded S or O left its site in any of the 15 runs.",
            transform=ax.transAxes, fontsize=8.2, color=H.MUT, va="top")
    fig.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return _rel(out_png)


STAGE_LAB = {"melt_hold": "melt hold 1200 K", "quench": "quench 1200→300 K",
             "final_hold": "final hold 300 K"}
STAGE_COL = {"melt_hold": "#c2410c", "quench": "#7c3aed", "final_hold": "#1f2937"}


def fig_li2s(pc: dict, be: dict, out_png=OUT / "li2s_glass_week.png") -> str:
    plt = _plt()
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(13.2, 5.0), gridspec_kw={"width_ratios": [1.45, 1]})
    w = 0.26
    stages = ("melt_hold", "quench", "final_hold")
    for j, st in enumerate(stages):
        for i, s in enumerate(pc["seeds"]):
            n, N = pc["frames"][s][st]
            pct = 100.0 * n / N
            x = i + (j - 1) * w
            ax.bar(x, pct, w * 0.92, color=STAGE_COL[st],
                   label=f"{STAGE_LAB[st]}  ({N} frames)" if i == 0 else None)
            ax.text(x, pct + 1.5, f"{n}", ha="center", va="bottom", fontsize=7.8, color=H.MUT)
    ax.set_xticks(range(len(pc["seeds"])))
    ax.set_xticklabels([s.replace("seed", "seed ") for s in pc["seeds"]])
    ax.set_ylim(0, 112)
    last = pc["seeds"][-1]
    if pc["frames"][last]["final_hold"][0] == pc["frames"][last]["final_hold"][1]:
        ax.annotate("one P never returned\nto 4-fold (P30)", xy=(len(pc["seeds"]) - 1 + w, 100),
                    xytext=(len(pc["seeds"]) - 1.65, 104), fontsize=8.5, color=H.INK, ha="center",
                    arrowprops=dict(arrowstyle="->", color=H.MUT, lw=1))
    H.apply_axes(ax, ylabel="saved frames with ≥ 1 P not 4-fold (%)",
                 title="(a)  P–S breaks during melt–quench, all 5 seeds  (cut 2.6 Å)")
    ax.legend(frameon=False, fontsize=8.8, loc="upper left")
    ax.text(0.0, -0.13, "Numbers over bars = frame counts (1 ps apart). Distance criterion only; "
            "1-frame events can be thermal vibration.", transform=ax.transAxes, fontsize=8,
            color=H.MUT, va="top")

    lo, hi = be["band"]
    bx.axhspan(lo, hi, color="#dcfce7", zorder=0)
    bx.axhline(1.0, color=H.MUT, ls=":", lw=1)
    bx.text(2.42, hi - 0.02, f"gate C2: {lo}–{hi}", ha="right", va="top", fontsize=8.8,
            color="#15803d")
    bx.text(2.42, 1.0 + 0.012, "β = 1  normal diffusion", ha="right", va="bottom", fontsize=8,
            color=H.MUT)
    for i, r in enumerate(be["runs"]):
        col = "#15803d" if r["beta"] >= lo else VCOL["nogo"]
        bx.errorbar(i, r["beta"], yerr=r["sigma"], fmt="o", ms=8, color=col, capsize=4, lw=1.4)
        bx.text(i + 0.1, r["beta"], f"{r['dos']:+.1f}σ".replace("-", "−"), va="center",
                ha="left", fontsize=9, color=col)
    bx.set_xticks(range(len(be["runs"])))
    bx.set_xticklabels([f"{r['T']} K\n{r['ps']} ps" for r in be["runs"]])
    bx.set_xlim(-0.5, 2.55)
    bx.set_ylim(0.3, 1.3)
    H.apply_axes(bx, ylabel="MSD exponent β  (d log MSD / d log t)",
                 title="(b)  Is Li motion diffusive yet?  (MTO, pilot runs)")
    bx.text(0.0, -0.2, "σ = time-origin block bootstrap at the end of the ladder = lower bound.\n"
            "Internal diagnostic — the external first author makes the call.",
            transform=bx.transAxes, fontsize=8, color=H.MUT, va="top")
    fig.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return _rel(out_png)


# ────────────────────────────────────────────────────────────── CSV
def write_csvs(rv, b, pc, be, d=DB) -> dict:
    d = pathlib.Path(d)
    out = {}
    p = d / "weekly_review_traffic_origin_2026_09_27.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["# Review letters with prompt or reply dated 2026-09-21..27. verdict_class: Codex "
                    "verdicts from db/pipelines/adhesion_pipeline.json reviews[].verdict; li2s = reply "
                    "(rules/judgments, not a GO vote); sent = reply pending."])
        w.writerow(["# P0/P1 (V5 rounds only) = count of '### P0-n' / '### P1-n' headings in the reply "
                    "(section heading 'P1 하나/한 묶음' counts 1). sources: " + " ; ".join(rv["source"])])
        w.writerow(["letter", "channel", "date", "day_index", "verdict_class", "P0_count", "P1_count",
                    "reply_file"])
        for it in sorted(rv["items"], key=lambda x: (x["date"], x["letter"])):
            w.writerow([it["letter"], it["chan"], it["date"].isoformat(), (it["date"] - WEEK[0]).days,
                        it["vclass"], "" if it["p0"] is None else it["p0"],
                        "" if it["p1"] is None else it["p1"], it["reply"]])
    out["csv_reviews"] = _rel(p)

    p = d / "b2o3_event_rate_origin_2026_09_27.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["# B2O3@LPSCl1.6 framework-site event rate (512 atoms, 5 seeds x 400 ps per T). "
                    "Values = sealed sentences. Not an ion-migration barrier; not conductivity."])
        w.writerow([f"# CI95 = Poisson (Garwood), assumes independent events; runs over-dispersed "
                    f"(var/mean {b['disp_range'][0]:.3f}-{b['disp_range'][1]:.3f}). "
                    f"control_ub = one-sided 95% upper bound for 0 events in "
                    f"{b['ctrl_runs']} control runs. source: " + " ; ".join(b["source"])])
        w.writerow(["T_K", "group", "rate_per_ns_cell", "CI95_lo", "CI95_hi", "runs_with_events",
                    "runs_total", "events_total", "var_over_mean", "control_ub_per_T_per_ns_cell"])
        for r in b["rows"]:
            w.writerow([r["T"], r["g"], r["rate"], r["lo"], r["hi"], r["k"], r["n"], r["sum"],
                        r["disp"], f"{b['ctrl_ub']:.4f}"])
    out["csv_b2o3"] = _rel(p)

    p = d / "li2s_p_coord_frames_origin_2026_09_27.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["# li2s small-cell glass melt-quench (120 atoms): saved frames (1 ps apart) with >= 1 "
                    "P not 4-coordinated (P-S distance cut 2.6 A). Internal diagnostic, citable false. "
                    "source: " + " ; ".join(pc["source"])])
        w.writerow(["seed", "stage", "frames_with_P_not4", "frames_total", "percent"])
        for s in pc["seeds"]:
            for st in ("melt_hold", "quench", "final_hold"):
                n, N = pc["frames"][s][st]
                w.writerow([s, st, n, N, f"{100.0 * n / N:.2f}"])
    out["csv_pcoord"] = _rel(p)

    p = d / "li2s_beta_gate_origin_2026_09_27.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([f"# li2s glass pilot runs (seed1): MSD exponent beta (MTO) vs card gate C2 "
                    f"{be['band'][0]}-{be['band'][1]}. sigma = block-bootstrap ladder end (lower bound). "
                    "Internal diagnostic, citable false. source: " + " ; ".join(be["source"])])
        w.writerow(["run", "T_K", "prod_ps", "beta_MTO", "sigma_lower_bound", "d_over_sigma_vs_gate_lo",
                    "gate_lo", "gate_hi"])
        for r in be["runs"]:
            w.writerow([r["key"], r["T"], r["ps"], r["beta"], r["sigma"], r["dos"],
                        be["band"][0], be["band"][1]])
    out["csv_beta"] = _rel(p)
    return out


# ────────────────────────────────────────────────────────────── 시험
def _selftest() -> int:
    import shutil
    import tempfile
    ok = True

    def chk(c, m):
        nonlocal ok
        ok = ok and bool(c)
        print(f"  {'✓' if c else '✗'} {m}")

    def dies(fn, frag):
        try:
            fn()
        except (ValueError, KeyError) as e:
            return frag in str(e)
        except Exception as e:  # noqa: BLE001
            print(f"    (다른 예외: {type(e).__name__}: {e})")
            return False
        return False

    rv = load_reviews()
    letters = {it["letter"] for it in rv["items"] if not it.get("internal")}
    chk(len(letters) == 19, f"[양성] 이번 주 편지 19 통 (얻은 {len(letters)}: {sorted(letters)})")
    v5 = sorted((it for it in rv["items"] if it["chan"] == "v5"), key=lambda x: x["letter"])
    chk([it["p0"] for it in v5] == [4, 3, 0, 0, 0, 0], f"[양성] V5 P0 = 4·3·0·0·0·0 ({[it['p0'] for it in v5]})")
    chk([it["p1"] for it in v5] == [5, 3, 3, 1, 1, 0], f"[양성] V5 P1 = 5·3·3·1·1·0 ({[it['p1'] for it in v5]})")
    vc = {}
    for it in rv["items"]:
        vc[it["vclass"]] = vc.get(it["vclass"], 0) + 1
    chk(vc == {"nogo": 10, "cond": 3, "go": 1, "reply": 5, "sent": 1},
        f"[양성] 판정 분포 NO-GO 10(내부 1 포함)·조건부 3·GO 1·회신 5·대기 1 ({vc})")

    b = load_b2o3()
    chk(len(b["rows"]) == 9, "[양성] b2o3 3 온도 × 3 원소군 = 9 칸")
    chk(abs(b["ctrl_ub"] - 0.749) < 0.001, f"[양성] 대조군 상한 재계산 {b['ctrl_ub']:.4f} ≈ 0.749")
    chk(abs(b["disp_range"][0] - 2.317) < 1e-3 and abs(b["disp_range"][1] - 17.475) < 1e-3,
        f"[양성] 과분산 범위 {b['disp_range']} = 기록 서술 2.3–17.5")
    pc = load_pcoord()
    chk(pc["frames"]["seed5"]["final_hold"] == (52, 52) and
        all(pc["frames"][s]["final_hold"][0] == 0 for s in pc["seeds"] if s != "seed5"),
        "[양성] 최종 유지에서 이탈이 남은 것은 seed5 뿐")
    be = load_beta()
    chk(be["band"] == (0.8, 1.2), f"[양성] 카드 C2 띠 {be['band']}")
    chk([r["beta"] >= be["band"][0] for r in be["runs"]] == [True, False, False],
        "[양성] 550 K 만 띠 안 · 400 K 두 런은 아래")

    td = pathlib.Path(tempfile.mkdtemp(prefix="figw0927_"))

    def _mk(name, text):
        p = td / name
        p.write_text(text, encoding="utf-8")
        return p

    # ⛔ 음성 1 — 회신이 제목 없이 쓰이면 NO-GO 인데 0 개 → 죽어야 한다
    rd = td / "rev"
    rd.mkdir()
    for f in REVDIR.glob("codex_C[E-K]_reply_*.md"):
        shutil.copy(f, rd / f.name)
    ce = next(rd.glob("codex_CE_reply_*.md"))
    ce.write_text(re.sub(r"^### P[01]-\d+\.", "#### 지적.", ce.read_text(encoding="utf-8"),
                         flags=re.M), encoding="utf-8")
    chk(dies(lambda: load_reviews(revdir=rd), "NO-GO 인데 P0/P1 을 못 셌다"),
        "[음성] 제목 형식이 바뀌어 0 개가 되면 0 으로 그리지 않고 죽는다")

    # ⛔ 음성 2 — 원장 판정을 GO 로 바꿨는데 P1 이 남아 있으면 모순
    def _file(r):
        return pathlib.Path(r.get("reply") or r.get("record") or "").name

    led = json.loads(PIPE.read_text(encoding="utf-8"))
    for r in led["reviews"]:
        if _file(r).startswith("codex_CJ_reply"):
            r["verdict"] = "GO (조작)"
    chk(dies(lambda: load_reviews(pipe=_mk("pipe.json", json.dumps(led, ensure_ascii=False))),
             "GO 인데 P0/P1"), "[음성] GO 판정에 P1 이 남으면 모순으로 죽는다")

    # ⛔ 음성 3 — 원장에 판정이 없는 Codex 회신
    led2 = json.loads(PIPE.read_text(encoding="utf-8"))
    led2["reviews"] = [r for r in led2["reviews"] if not _file(r).startswith("codex_BY_reply")]
    chk(dies(lambda: load_reviews(pipe=_mk("pipe2.json", json.dumps(led2, ensure_ascii=False))),
             "점착 원장에 BY"), "[음성] 원장에 판정이 없으면 판정을 지어내지 않는다")

    # ⛔ 음성 4 — b2o3 값을 흔들면 봉인 문장 대조에서 걸린다
    bj = json.loads(B2O3.read_text(encoding="utf-8"))
    k = next(x for x in bj if x.startswith("온도별_보고량"))
    bj[k]["650"]["Cl"]["rate_per_ns_cell"] = 9.5
    chk(dies(lambda: load_b2o3(_mk("b.json", json.dumps(bj, ensure_ascii=False))), "봉인 문장과 다르다"),
        "[음성] 봉인 문장과 1 칸이라도 다르면 그리지 않는다")

    # ⛔ 음성 5 — 대조군 상한 문장이 설계와 안 맞으면
    bj2 = json.loads(B2O3.read_text(encoding="utf-8"))
    kc = next(x for x in bj2 if x.startswith("대조군"))
    bj2[kc]["문장"] = bj2[kc]["문장"].replace("30 런", "60 런")
    chk(dies(lambda: load_b2o3(_mk("b2.json", json.dumps(bj2, ensure_ascii=False))), "대조군 상한 재계산"),
        "[음성] 런 수를 바꾸면 상한 재계산이 기록과 어긋나 죽는다")

    # ⛔ 음성 6 — 프레임 분모가 궤적 설명과 다르면
    pj = json.loads(PCOORD.read_text(encoding="utf-8"))
    pj["seeds"]["seed3"]["frames_any_not4"]["quench"] = [185, 890]
    chk(dies(lambda: load_pcoord(_mk("p.json", json.dumps(pj, ensure_ascii=False))), "궤적 설명"),
        "[음성] 분모가 897 이 아니면 비율을 그리지 않는다")

    # ⛔ 음성 7 — β 를 흔들면 d/σ 가 원장과 어긋난다
    fj = json.loads(FOLLOW.read_text(encoding="utf-8"))
    fj["회신_CD_판정_2026_09_27"]["보수값_재계산"]["P-2_550K_MTO"]["beta"] = 0.90
    chk(dies(lambda: load_beta(follow=_mk("f.json", json.dumps(fj, ensure_ascii=False))), "원장"),
        "[음성] β 와 d/σ 가 원장끼리 안 맞으면 그리지 않는다")

    # ⛔ 음성 8 — 카드의 게이트 띠를 못 읽으면 손으로 0.8 을 넣지 않는다
    cj = json.loads(CARD.read_text(encoding="utf-8"))
    cj["5_게이트_결과_보기_전"]["C2_beta"] = "β 는 적당히"
    chk(dies(lambda: load_beta(card=_mk("c.json", json.dumps(cj, ensure_ascii=False))), "β 띠를 못 읽었다"),
        "[음성] 카드에 띠가 없으면 문턱을 지어내지 않는다")

    # 양성 — 그림·CSV 가 tmp 에 실제로 써진다
    outs = [fig_reviews(rv, td / "r.png"), fig_b2o3(b, td / "b.png"), fig_li2s(pc, be, td / "l.png")]
    chk(all(pathlib.Path(o).stat().st_size > 20000 for o in outs), "[양성] PNG 3 장이 써진다")
    cs = write_csvs(rv, b, pc, be, d=td)
    chk(len(cs) == 4 and all(pathlib.Path(v).exists() for v in cs.values()), "[양성] CSV 4 벌이 써진다")

    shutil.rmtree(td, ignore_errors=True)
    print("selftest " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    RV, B, PC, BE = load_reviews(), load_b2o3(), load_pcoord(), load_beta()
    res = {"png": [fig_reviews(RV), fig_b2o3(B), fig_li2s(PC, BE)], **write_csvs(RV, B, PC, BE)}
    print(json.dumps(res, ensure_ascii=False, indent=1))
