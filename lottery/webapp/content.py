"""content.py — 분석 결과 파일을 화면용 값과 차트 좌표로 바꾼다.

이 앱은 계산하지 않는다. 통계·머신러닝은 `lottery/build_results.py` 가 한 번 돌려
`lottery/results/analysis.json` 에 남기고(정본), 여기서는 그 파일을 읽어
  (1) 표·문장에 들어갈 값을 꺼내고
  (2) 차트 좌표를 계산한다.

CSP 가 `script-src 'self'` 라 차트 라이브러리를 못 쓴다. 본체 webapp 의 `sweep_chart()`
처럼 **좌표는 서버가 계산하고 템플릿(_macros.html)은 그리기만** 한다. 마크마다 `<title>`
을 달아 마우스를 올리면 값이 보인다 — 자바스크립트가 없어도 된다. 색은 CSS 토큰을 쓰므로
다크 모드에서도 따라온다 (좌표만 서버, 색은 스타일시트).

파일은 요청마다 mtime 을 확인해 바뀌었으면 다시 읽는다 (본체 앱의 "화면이 파일과
다르다" 함정을 피하는 규칙과 같다).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # lottery/
RESULTS = ROOT / "results" / "analysis.json"
W = 760  # SVG viewBox 폭 — CSS 가 칸에 맞춰 늘이고 줄인다 (본체 .chart 규칙)

_cache: dict = {"mtime": None, "data": None, "view": None}

SECTIONS = [  # (이름, 경로, 메뉴 제목, 메뉴 꼬리표, 아이콘, 무리)
    ("make", "/make", "번호 만들기", "수동 구매용", "i-dice", "도구"),
    ("home", "/", "한눈에 보기", "처음이면 여기", "i-home", "근거"),
    ("random", "/random", "추첨기는 무작위인가", None, "i-chart", "근거"),
    ("ml", "/ml", "머신러닝 대결", "SVM·확산 모델", "i-flow", "근거"),
    ("people", "/people", "사람들의 선택", "핵심", "i-question", "근거"),
    ("pension", "/pension", "연금복권720+", None, "i-compass", "근거"),
    ("data", "/data", "데이터와 방법", None, "i-paper", "부록"),
]


def load() -> dict:
    mt = RESULTS.stat().st_mtime
    if _cache["mtime"] != mt:
        _cache.update(mtime=mt, data=json.loads(RESULTS.read_text(encoding="utf-8")), view=None)
    return _cache["data"]


# ───────────────────────────── 숫자 표기 ─────────────────────────────

_SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def fmt_p(p) -> str:
    if p is None:
        return "–"
    if p >= 0.001:
        return "1.00" if p >= 0.995 else f"{p:.3f}"
    e = math.floor(math.log10(p))
    return f"{p / 10 ** e:.1f}×10{str(e).translate(_SUP)}"


def won(x) -> str:
    x = float(x)
    if x >= 1e12:
        return f"{x / 1e12:.1f}조"
    if x >= 1e8:
        return f"{x / 1e8:.1f}억"
    if x >= 1e4:
        return f"{round(x / 1e4):,}만"
    return f"{round(x):,}"


def pct(x, d=0) -> str:
    return f"{x * 100:.{d}f}%"


def signed(x, d=2) -> str:
    return ("+" if x >= 0 else "−") + f"{abs(x):.{d}f}"


def num(x, d=0) -> str:
    return f"{x:,.{d}f}"


FILTERS = {"p": fmt_p, "won": won, "pct": pct, "signed": signed, "num": num}


# ───────────────────────────── 차트 좌표 ─────────────────────────────

def nice(lo: float, hi: float, n: int = 4) -> tuple[float, float, list[float]]:
    if lo == hi:
        lo, hi = lo - 1, hi + 1
    raw = (hi - lo) / n
    mag = 10 ** math.floor(math.log10(raw))
    e = raw / mag
    step = (10 if e >= 7.5 else 5 if e >= 3.5 else 2 if e >= 1.5 else 1) * mag
    a = math.floor(lo / step + 1e-9) * step
    b = math.ceil(hi / step - 1e-9) * step
    ticks, v = [], a
    while v <= b + step / 2:
        ticks.append(0.0 if abs(v) < step * 1e-6 else round(v, 10))
        v += step
    return a, b, ticks


def _f(v: float) -> str:
    return f"{v:.1f}"


def _bar_path(x: float, w: float, y0: float, y1: float, r: float = 4.0) -> str:
    """데이터 끝만 4px 둥글게, 기준선 쪽은 각지게 (dataviz 막대 규격)."""
    h = abs(y1 - y0)
    r = min(r, w / 2, h)
    if h < 0.5:
        return f"M{_f(x)},{_f(y0)}H{_f(x + w)}"
    s = -1 if y1 < y0 else 1
    return (f"M{_f(x)},{_f(y0)}V{_f(y1 - s * r)}Q{_f(x)},{_f(y1)} {_f(x + r)},{_f(y1)}"
            f"H{_f(x + w - r)}Q{_f(x + w)},{_f(y1)} {_f(x + w)},{_f(y1 - s * r)}V{_f(y0)}Z")


def columns(values, labels, *, height=230, ref=None, band=None, band2=None, line=None,
            errors=None, x_every=1, y_min=None, y_max=None, y_fmt=lambda v: f"{v:,.0f}",
            tones=None, titles=None, ml=50, aria="") -> dict:
    """세로 막대. ref=기대선, band=95% 범위, line=범주별 기대값(선+점), errors=[lo,hi]."""
    m = {"l": ml, "r": 10, "t": 14, "b": 30}
    iw, ih = W - m["l"] - m["r"], height - m["t"] - m["b"]
    ext = list(values) + [0]
    for extra in (([ref] if ref is not None else []), band or [], band2 or [], line or []):
        ext += list(extra)
    for e in errors or []:
        ext += list(e)
    lo, hi, ticks = nice(min(ext) if y_min is None else y_min, max(ext) if y_max is None else y_max)
    y = lambda v: m["t"] + ih - (v - lo) / (hi - lo) * ih
    n = len(values)
    step = iw / n
    bw = max(2.0, min(24.0, step - 2))
    base = y(max(lo, 0.0))
    bars = []
    for i, v in enumerate(values):
        x = m["l"] + i * step + (step - bw) / 2
        bars.append({"d": _bar_path(x, bw, base, y(v)), "cls": (tones[i] if tones else ""),
                     "title": (titles[i] if titles else ""), "hx": _f(m["l"] + i * step),
                     "hw": _f(step), "cx": x + bw / 2})
    out = {
        "w": W, "h": height, "l": m["l"], "r": W - m["r"], "top": m["t"], "bottom": _f(m["t"] + ih),
        "ih": _f(ih), "aria": aria,
        "grid": [{"y": _f(y(t)), "label": y_fmt(t), "zero": t == 0} for t in ticks],
        "bars": bars, "xly": height - m["b"] + 19,
        # 마지막 눈금은 바로 앞 눈금과 붙지 않을 때만 (총합 차트의 '240 250' 겹침)
        "xlabels": [{"x": _f(m["l"] + i * step + step / 2), "t": labels[i]} for i in range(n)
                    if labels and (i % x_every == 0 or (i == n - 1 and i % x_every >= max(2, x_every / 2)))],
    }
    if band:
        out["band"] = {"y": _f(y(band[1])), "h": _f(y(band[0]) - y(band[1]))}
    if band2:
        out["band2"] = {"y": _f(y(band2[1])), "h": _f(y(band2[0]) - y(band2[1]))}
    if ref is not None:
        out["ref"] = _f(y(ref))
    if line:
        pts = [(m["l"] + i * step + step / 2, y(v)) for i, v in enumerate(line)]
        out["line"] = {"points": " ".join(f"{_f(a)},{_f(b)}" for a, b in pts),
                       "dots": [{"cx": _f(a), "cy": _f(b)} for a, b in pts] if n <= 30 else []}
    if errors:
        out["errors"] = [{"x": _f(bars[i]["cx"]), "y1": _f(y(e[0])), "y2": _f(y(e[1]))}
                         for i, e in enumerate(errors)]
    return out


def heatmap(matrix, *, limit, titles, row_labels=None, col_labels=None, ml=34, mt=22,
            max_cell=16.0, aria="") -> dict:
    """발산형 칸 그림. 값을 ±limit 안에서 9단계(-4..+4)로 나눠 CSS 클래스로 칠한다."""
    rows, cols = len(matrix), len(matrix[0])
    cell = min((W - ml - 6) / cols, max_cell)
    gap = 1.0 if cell > 6 else 0.0
    cells = []
    for i, row in enumerate(matrix):
        for j, v in enumerate(row):
            if v is None:
                continue
            k = max(-4, min(4, round(v / limit * 4)))
            cells.append({"x": _f(ml + j * cell), "y": _f(mt + i * cell), "s": _f(cell - gap),
                          "cls": f"hm-{'n' if k < 0 else 'p'}{abs(k)}" if k else "hm-0",
                          "title": titles(i, j)})
    return {"w": W, "h": _f(mt + 6 + cell * rows), "cells": cells, "aria": aria,
            "rl": [{"y": _f(mt + i * cell + cell / 2), "t": t} for i, t in enumerate(row_labels or []) if t],
            "cl": [{"x": _f(ml + j * cell + cell / 2), "t": t} for j, t in enumerate(col_labels or []) if t],
            "rlx": ml - 6, "cly": mt - 7}


def dotwhisker(rows, *, ref, ref_label, aria="") -> dict:
    """가로 점·구간: rows = [{label, v, lo, hi, v2, title}]. v2 = 비교 기준(빈 점)."""
    m = {"l": 236, "r": 22, "t": 28, "b": 30}
    rh = 27
    h = m["t"] + m["b"] + rh * len(rows)
    iw = W - m["l"] - m["r"]
    ext = [ref] + [v for r in rows for v in (r["lo"], r["hi"], r.get("v2", r["v"]))]
    lo, hi, ticks = nice(min(ext), max(ext), 4)
    x = lambda v: m["l"] + (v - lo) / (hi - lo) * iw
    return {
        "w": W, "h": h, "aria": aria, "top": m["t"] - 8, "bottom": h - m["b"], "lx": m["l"] - 12,
        "grid": [{"x": _f(x(t)), "label": f"{t:.2f}"} for t in ticks], "tly": h - m["b"] + 19,
        "ref": {"x": _f(x(ref)), "label": ref_label},
        "rows": [{"y": _f(m["t"] + i * rh + rh / 2), "label": r["label"], "x": _f(x(r["v"])),
                  "lo": _f(x(r["lo"])), "hi": _f(x(r["hi"])),
                  "x2": _f(x(r["v2"])) if r.get("v2") is not None else None, "title": r.get("title", "")}
                 for i, r in enumerate(rows)],
    }


def line_chart(xs, ys, *, ref=None, x_ticks=(), x_fmt=str, y_fmt=str, marks=(), titles=None,
               height=240, aria="") -> dict:
    m = {"l": 56, "r": 16, "t": 18, "b": 32}
    iw, ih = W - m["l"] - m["r"], height - m["t"] - m["b"]
    lo, hi, ticks = nice(min(list(ys) + ([ref] if ref is not None else [])),
                         max(list(ys) + ([ref] if ref is not None else [])))
    x0, x1 = min(xs), max(xs)
    X = lambda v: m["l"] + (v - x0) / (x1 - x0) * iw
    Y = lambda v: m["t"] + ih - (v - lo) / (hi - lo) * ih
    pts = [(X(a), Y(b)) for a, b in zip(xs, ys)]
    path = " ".join(f"{_f(a)},{_f(b)}" for a, b in pts)
    out = {
        "w": W, "h": height, "aria": aria, "l": m["l"], "r": W - m["r"],
        "grid": [{"y": _f(Y(t)), "label": y_fmt(t)} for t in ticks],
        "xt": [{"x": _f(X(t)), "t": x_fmt(t)} for t in x_ticks], "xty": height - m["b"] + 19,
        "points": path, "area": f"{_f(pts[0][0])},{_f(Y(lo))} {path} {_f(pts[-1][0])},{_f(Y(lo))}",
        "marks": [], "hits": [],
    }
    if ref is not None:
        out["ref"] = _f(Y(ref))
    for mk in marks:
        i = list(xs).index(mk["x"])
        out["marks"].append({"cx": _f(pts[i][0]), "cy": _f(pts[i][1]), "label": mk["label"],
                             "anchor": mk.get("anchor", "start")})
    if titles:
        out["hits"] = [{"cx": _f(pts[i][0]), "cy": _f(pts[i][1]), "title": titles(i)}
                       for i in range(0, len(xs), max(1, len(xs) // 40))]
    return out


# ───────────────────────────── 화면별 값 ─────────────────────────────

def _ball_cls(n: int) -> str:
    return "b1" if n <= 10 else "b2" if n <= 20 else "b3" if n <= 30 else "b4" if n <= 40 else "b5"


def view() -> dict:
    D = load()
    if _cache["view"] is None:
        _cache["view"] = _build_view(D)
    return _cache["view"]


def _build_view(D: dict) -> dict:
    lo, pe, meta = D["lotto"], D["pension"], D["meta"]
    st, pop, S = lo["stats"], lo["popularity"], lo["popularity"]["score"]
    n = st["n_draws"]
    v: dict = {"D": D, "meta": meta, "S": S}

    # ── 공통 요약
    all_summary = st["summary"] + pe["stats"]["summary"]
    hits = [r["mean_hits"] for r in lo["ml"]["real"]["rows"]]
    i10 = S["pct"].index(10.0)
    v["facts"] = {
        "n_tests": len(all_summary), "min_holm": min(r["p_holm"] for r in all_summary),
        "n_models": len(hits), "hit_lo": min(hits), "hit_hi": max(hits),
        "gain10": S["share_at_pct"][i10] / S["share_avg"] - 1,
        "r2_5": pop["tiers"]["5"]["r2_oof"],
    }
    v["recent"] = [{"round": d[0], "date": d[1], "nums": [(x, _ball_cls(x)) for x in d[2:8]],
                    "bonus": (d[8], _ball_cls(d[8])), "w1": d[9], "prize1": d[14],
                    "split": None if d[16] is None else (d[16], d[17], d[18])}
                   for d in reversed(lo["draws"][-8:])]
    v["precent"] = list(reversed(pe["draws"][-6:]))

    # ── 추첨기는 무작위인가
    fq = st["frequency"]
    v["freq_chart"] = columns(
        fq["counts"], [str(i + 1) for i in range(45)], x_every=5, ref=fq["expected"],
        band=fq["band95"], band2=fq["band_bonferroni"], aria="번호별 출현 횟수",  # 막대는 0 에서 (축 자르기 금지)
        titles=[f"{i + 1}번: {c}회 (기대 {fq['expected']:.1f}) · 최근 100회 {fq['recent100'][i]}회 · "
                f"지금 {fq['current_gap'][i]}회째 안 나옴" for i, c in enumerate(fq["counts"])])
    pr = st["pairs"]
    z = pr["z_matrix"]
    sd2 = math.sqrt(n * (1 / 66) * (65 / 66))
    v["pair_chart"] = heatmap(
        [[None if i == j else z[i][j] for j in range(45)] for i in range(45)], limit=3.5,
        row_labels=[str(i + 1) if (i + 1) % 5 == 0 else "" for i in range(45)],
        col_labels=[str(j + 1) if (j + 1) % 5 == 0 else "" for j in range(45)],
        titles=lambda i, j: f"{i + 1}·{j + 1}번: {round(pr['expected'] + z[i][j] * sd2)}회 "
                            f"(기대 {pr['expected']:.1f}, z {signed(z[i][j])})",
        aria="45×45 번호 쌍 동시 출현 표준점수")
    lg = st["lag"]
    v["carry_chart"] = columns(
        lg["carry_hist"][:5], ["0개", "1개", "2개", "3개", "4개"], line=lg["carry_expected"][:5],
        aria="이월수 분포", titles=[f"{k}개 이월: {lg['carry_hist'][k]}회 (기대 {lg['carry_expected'][k]:.1f})"
                                   for k in range(5)])
    gp = st["gaps"]
    v["gap_chart"] = columns(
        gp["hist"], [f"{gp['cap']}+" if i + 1 == gp["cap"] else str(i + 1) for i in range(len(gp["hist"]))],
        x_every=5, line=gp["expected"], aria="출현 간격 분포",
        titles=[f"간격 {i + 1}{'회 이상' if i + 1 == gp['cap'] else '회'}: {h}번 (기대 {gp['expected'][i]:.0f})"
                for i, h in enumerate(gp["hist"])])
    v["freq_rows"] = [(i + 1, c, fq["recent100"][i], fq["current_gap"][i]) for i, c in enumerate(fq["counts"])]
    v["pair_rows"] = [("·".join(map(str, r["pair"])), r["count"], f"{pr['expected']:.1f}", fmt_p(r["p"]),
                       fmt_p(r["p_holm"])) for r in pr["top"]]
    v["feature_rows"] = [(f["label"], f"{f['obs_mean']:.2f}", f"{f['exp_mean']:.2f}", fmt_p(f["p"]))
                         for f in st["features"].values()]
    sf = st["features"]["sum"]
    v["sum_chart"] = columns(
        sf["obs"], [str(x) for x in sf["values"]], x_every=2, line=sf["exp"], aria="총합 분포",
        titles=[f"총합 {x}~{x + 9}: {o}회 (기대 {e:.1f})" for x, o, e in zip(sf["values"], sf["obs"], sf["exp"])])

    # ── 머신러닝
    real, nul = lo["ml"]["real"], lo["ml"]["null"]
    v["ml_chart"] = dotwhisker(
        [{"label": r["model"], "v": r["mean_hits"], "lo": r["ci95"][0], "hi": r["ci95"][1],
          "v2": nr["mean_hits"],
          "title": f"{r['model']}: 평균 {r['mean_hits']:.3f}개 (95% {r['ci95'][0]:.2f}~{r['ci95'][1]:.2f}, "
                   f"보정 p {fmt_p(r['p_bonferroni'])}) · 가상 무작위 역사 {nr['mean_hits']:.3f}개"}
         for r, nr in zip(real["rows"], nul["rows"])],
        ref=0.8, ref_label="무작위 기대 0.8", aria="전략별 평균 적중 수")
    v["ml_roi"] = (min(r["won"] / r["spent"] for r in real["rows"]), max(r["won"] / r["spent"] for r in real["rows"]))
    v["ml_best_raw_p"] = min(r["p_better"] for r in real["rows"])
    dd = lo["ddpm"]
    v["ddpm_chart"] = columns(
        dd["number_counts"], [str(i + 1) for i in range(45)], x_every=5, ref=dd["n_generated"] * 6 / 45,
        aria="확산 모델 번호 사용 횟수",
        titles=[f"{i + 1}번: {c}회 (균등이면 {dd['n_generated'] * 6 / 45:.0f})" for i, c in enumerate(dd["number_counts"])])

    # ── 사람들의 선택
    ne = pop["number_effect"]
    beta = [b * 100 for b in ne["beta"]]
    se = [s * 100 for s in ne["se"]]
    rank = sorted(range(45), key=lambda i: -beta[i])
    v["pop_rank"] = [i + 1 for i in rank]
    v["pop_chart"] = columns(
        beta, [str(i + 1) for i in range(45)], x_every=5,
        errors=[[b - 1.96 * s, b + 1.96 * s] for b, s in zip(beta, se)],
        tones=["pos4" if b > 0 else "neg4" for b in beta],  # 크기는 높이가 말한다 — 색은 부호만
        y_fmt=lambda t: f"{t:+.1f}" if t else "0", aria="번호별 인기도",
        titles=[f"{i + 1}번: {signed(beta[i])}% (±{1.96 * se[i]:.2f}) · 인기 {rank.index(i) + 1}위/45"
                for i in range(45)])
    v["pop_rows"] = [(i + 1, signed(beta[i]), f"{1.96 * se[i]:.2f}", rank.index(i) + 1) for i in range(45)]
    mm = pop["manual_model"]
    v["manual_chart"] = columns(
        [x["manual_share"] * 100 for x in mm["by_s"]], ["하위 20%", "", "중간", "", "상위 20%"], y_min=0,
        y_fmt=lambda t: f"{t:.0f}%", aria="인기도 5분위별 1등 중 수동 비율",
        titles=[f"인기도 {k + 1}분위: 수동 {x['manual_share'] * 100:.1f}% (1등 {x['winners']:,}명)"
                for k, x in enumerate(mm["by_s"])])
    cal = pop["first_prize_model"]["calibration"]
    v["calib_chart"] = columns(
        [c["obs"] / c["exp_uniform"] for c in cal], [str(k + 1) for k in range(10)],
        line=[c["pred"] / c["exp_uniform"] for c in cal], y_min=0.6, y_max=1.3,
        y_fmt=lambda t: f"{t:.1f}", aria="인기도 10분위별 1등 당첨자 수 비율",
        titles=[f"인기도 {k + 1}분위: 실제 1등 평균 {c['obs']:.1f}명 (무작위 기대 {c['exp_uniform']:.1f}, "
                f"모델 {c['pred']:.1f})" for k, c in enumerate(cal)])
    shares = [s / S["share_avg"] for s in S["share_at_pct"]]
    i90 = S["pct"].index(90.0)
    v["payoff_chart"] = line_chart(
        S["pct"], shares, ref=1.0, x_ticks=[0, 25, 50, 75, 100], x_fmt=lambda t: f"{t:g}%",
        y_fmt=lambda t: f"{t:.2f}배",
        marks=[{"x": 10.0, "label": f"하위 10%: {shares[i10]:.2f}배"},
               {"x": 90.0, "label": f"상위 10%: {shares[i90]:.2f}배", "anchor": "end"}],
        titles=lambda i: f"인기도 {S['pct'][i]:g}%: {shares[i]:.3f}배 (1등 시 약 {won(S['pool1_recent_mean'] * S['share_at_pct'][i])}원)",
        aria="인기도 백분위별 1등 기대 수령액")
    v["shares10"] = (shares[i10], shares[i90])

    # ── 연금
    ps = pe["stats"]
    pn = ps["n_draws"]
    v["pen_chart"] = heatmap(
        [[(c - pn / 10) / math.sqrt(pn * 0.09) for c in r["counts"]] for r in ps["positions"]], limit=3,
        row_labels=[f"{'1등' if r['which'] == '1등' else '보너스'} {r['pos']}" for r in ps["positions"]],
        col_labels=[str(d) for d in range(10)], ml=78, max_cell=40,
        titles=lambda i, j: f"{ps['positions'][i]['which']} {ps['positions'][i]['pos']}번째 자리 숫자 {j}: "
                            f"{ps['positions'][i]['counts'][j]}회 (기대 {pn / 10:.1f})",
        aria="연금복권 자리별 숫자 표준점수")
    v["pen_min_pos_holm"] = min(r["p_holm"] for r in ps["positions"])
    return v


def generator_payload() -> dict:
    """번호 생성기(make.js)가 받는 값 — 인기도 점수 계수, 확산 모델 번호 풀, 과거 1등."""
    D = load()
    lo = D["lotto"]
    return {
        "score": lo["popularity"]["score"],
        "ddpm_pool": lo["ddpm_pool"],
        "past": [[d[0], *d[2:8]] for d in lo["draws"]],
        "pension_past": [[d[0], d[3]] for d in D["pension"]["draws"]],
        "latest_round": lo["draws"][-1][0],
    }


def palette_items(onepage: bool = False) -> list[dict]:
    """⌘K 팔레트 목적지 — 화면 이름과 그 안의 주요 카드."""
    def u(name, anchor=None):
        path = dict((s[0], s[1]) for s in SECTIONS)[name]
        if onepage:
            return "#" + (anchor or name)
        return path + ("#" + anchor if anchor else "")
    items = [{"t": s[2], "d": s[3] or "", "u": u(s[0]), "k": "화면"} for s in SECTIONS]
    for name, anchor, title in [
        ("random", "freq", "번호별 출현 횟수"), ("random", "pairs", "궁합수 지도"),
        ("random", "carry", "이월수"), ("random", "gaps", "미출현 간격"), ("random", "sum", "총합 분포"),
        ("ml", "board", "전략별 적중 수"), ("ml", "ddpm", "확산 모델"), ("ml", "em", "EM·SVR"),
        ("people", "numbers", "번호별 인기도"), ("people", "manual", "수동 비율 검증"),
        ("people", "payoff", "인기도별 기대 수령액"), ("data", "course", "강의와의 연결"),
    ]:
        items.append({"t": title, "d": dict((s[0], s[2]) for s in SECTIONS)[name], "u": u(name, anchor), "k": "카드"})
    return items
