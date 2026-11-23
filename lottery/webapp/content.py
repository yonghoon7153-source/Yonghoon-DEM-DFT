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
import sys
from pathlib import Path
from statistics import NormalDist

ROOT = Path(__file__).resolve().parents[1]  # lottery/
RESULTS = ROOT / "results" / "analysis.json"
sys.path.insert(0, str(ROOT))
import dataset  # noqa: E402  — 원본(data/raw) 검증 파서. 표준 라이브러리만 쓴다 (Pages 빌드에서도 돈다)
W = 760  # SVG viewBox 폭 — CSS 가 칸에 맞춰 늘이고 줄인다 (본체 .chart 규칙)

_cache: dict = {"mtime": None, "data": None, "view": None}
_raw: dict = {"mtime": None, "lotto": None, "pension": None, "manifest": None}

SECTIONS = [  # (이름, 경로, 메뉴 제목, 메뉴 꼬리표, 아이콘, 무리)
    ("make", "/make", "번호 만들기", "수동 구매용", "i-dice", "도구"),
    ("history", "/history", "회차별 당첨번호", "누적 히스토리", "i-list", "도구"),
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


def raw() -> dict:
    """원본 정본(data/raw) — 회차별 2~5등 당첨금·당첨자 수까지 필요한 화면(누적 히스토리·백테스트)용.
    analysis.json 의 draws 는 1등 금액만 있는 사본이다. mtime 이 바뀌면 다시 읽고 다시 검증한다."""
    d = dataset.RAW_DIR  # 확인하는 폴더와 읽는 폴더가 같아야 한다 (load_* 의 기본 인자는 import 때 고정된다)
    mt = tuple((d / f).stat().st_mtime for f in ("lotto645.json", "pension720.json", "MANIFEST.json"))
    if _raw["mtime"] != mt:  # 세 파일 중 하나라도 바뀌면 (연금만 바뀌어도) 다시 읽는다
        _raw.update(mtime=mt, lotto=dataset.load_lotto(d), pension=dataset.load_pension(d),
                    manifest=json.loads((d / "MANIFEST.json").read_text(encoding="utf-8")))
        _cache["view"] = None
    return _raw


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


def josa(n, pair: str = "이가") -> str:
    """숫자 뒤 조사 — 한국어로 읽은 끝소리에 맞춘다: 끝자리 2(이)·4(사)·5(오)·9(구)는 받침이 없다.
    값에서 만든 문장이 '2 이 1위다' 처럼 되지 않게 (pair: "이가" · "을를" · "은는")."""
    return f"{n} {pair[1] if int(n) % 10 in (2, 4, 5, 9) else pair[0]}"


FILTERS = {"p": fmt_p, "won": won, "pct": pct, "signed": signed, "num": num, "josa": josa}


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
    raw()  # 원본(data/raw)이 바뀌었으면 다시 읽고 화면을 다시 만든다 — 받기만 하고 분석을 안 돌려도 /history 가 따라간다
    if _cache["view"] is None:
        _cache["view"] = _build_view(D)
    return _cache["view"]


def holm_sig(summary: list[dict], key: str) -> bool:
    """질문 문구에 key 가 든 행 하나의 Holm 보정 p < ALPHA. 문구가 바뀌어 0개나 여러 개가 걸리면 멈춘다
    — 조용히 '구분 안 됨' 으로 두지 않는다."""
    rows = [r for r in summary if key in r["question"]]
    if len(rows) != 1:
        raise KeyError(f"판정할 질문을 하나로 정하지 못함: {key!r} → {len(rows)}개")
    return rows[0]["p_holm"] < dataset.ALPHA


def verdicts(D: dict) -> dict:
    """화면의 판정 — 머리 칩 · 홈 카드 · 판정표가 모두 여기서 나온다 (자체 리뷰 K1: 고정 문구는 주간 갱신으로
    p 가 바뀌어도 그대로 남아, 한 화면에서 머리와 표가 반대로 말할 수 있었다)."""
    lo, pe, a = D["lotto"], D["pension"], dataset.ALPHA

    def tests(summary: list[dict]) -> dict:
        n, sig = len(summary), [r["question"] for r in summary if r["p_holm"] < a]
        if sig:
            return {"kind": "diff", "label": "무작위와 다른 점 있음", "sig": sig,
                    "text": f"질문 {n}개 중 {len(sig)}개가 보정 후에도 p < {a}: " + " · ".join(sig),
                    "card": f"{n}개 질문 중 {len(sig)}개가 보정 후에도 무작위와 다르다 — 원인을 확인하기 전까지 결론을 보류한다."}
        return {"kind": "same", "label": "무작위와 구분 안 됨", "sig": [],
                "text": f"질문 {n}개 모두 — 보정 후 가장 작은 p 가 {fmt_p(min(r['p_holm'] for r in summary))}",
                "card": f"{n}개 질문 모두 무작위와 구분되지 않는다."}

    def models(rows: list[dict], what: str) -> dict:
        sig, p = [r["model"] for r in rows if r["p_bonferroni"] < a], min(r["p_bonferroni"] for r in rows)
        if sig:
            return {"kind": "diff", "label": "무작위보다 나은 전략 있음", "sig": sig, "min_p": p,
                    "text": " · ".join(sig) + f" — 보정 후에도 {what}이 무작위보다 높다 (p < {a}). "
                            "다른 기간에서 재현되기 전에는 예측력으로 보지 않는다",
                    "card": f"보정 후에도 무작위보다 나은 전략이 {len(sig)}개 나왔다 — 재현을 확인하기 전까지 결론을 보류한다."}
        return {"kind": "same", "label": "무작위보다 낫지 않음", "sig": [], "min_p": p,
                "text": f"{len(rows)}개 전략 모두 {what}이 무작위보다 높다고 할 수 없다 (보정 후 가장 작은 p = {fmt_p(p)})",
                "card": "무작위보다 나은 전략은 없었다."}

    t5, ne = lo["popularity"]["tiers"]["5"], lo["popularity"]["number_effect"]
    if ne["wald_p"] < a and t5["r2_oof"] > 0:
        people = {"kind": "diff", "label": "뚜렷한 패턴 있음",
                  "text": f"5등 당첨자 수만으로 그 주 번호의 인기를 {pct(t5['r2_oof'])} 설명한다 (처음 보는 회차 기준)"}
    else:
        people = {"kind": "same", "label": "패턴 안 보임",
                  "text": f"번호별 인기 차이가 유의하지 않거나(p = {fmt_p(ne['wald_p'])}) 처음 보는 회차를 설명하지 "
                          f"못한다 (R² {t5['r2_oof']:.3f})"}
    out = {"random": tests(lo["stats"]["summary"]), "pension": tests(pe["stats"]["summary"]),
           "ml": models(lo["ml"]["real"]["rows"], "평균 적중"),
           "pension_ml": models(pe["ml"]["real"]["rows"], "정답률"), "people": people}
    out["changed"] = [what for what, bad in (
        ("로또 추첨기: " + out["random"]["card"], out["random"]["kind"] == "diff"),
        ("연금 추첨: " + out["pension"]["card"], out["pension"]["kind"] == "diff"),
        ("로또 예측: " + out["ml"]["card"], out["ml"]["kind"] == "diff"),
        ("연금 예측: " + out["pension_ml"]["card"], out["pension_ml"]["kind"] == "diff"),
        ("사람들의 선택: " + people["text"], people["kind"] == "same")) if bad]
    out["thesis"] = not out["changed"]  # 홈의 결론 문장('추첨기에는 패턴이 없고, 사람에게는 있다')이 맞는가
    return out


def _build_view(D: dict) -> dict:
    lo, pe, meta = D["lotto"], D["pension"], D["meta"]
    st, pop, S = lo["stats"], lo["popularity"], lo["popularity"]["score"]
    n = st["n_draws"]
    v: dict = {"D": D, "meta": meta, "S": S}
    vd = v["verdict"] = verdicts(D)
    v["sig"] = lambda key: holm_sig(st["summary"], key)  # 템플릿: {% if V.sig('간격 분포') %}
    v["psig"] = lambda key: holm_sig(pe["stats"]["summary"], key)

    # ── 공통 요약
    all_summary = st["summary"] + pe["stats"]["summary"]
    hits = [r["mean_hits"] for r in lo["ml"]["real"]["rows"]]
    i10 = S["pct"].index(10.0)
    v["facts"] = {
        "n_tests": len(all_summary), "min_holm": min(r["p_holm"] for r in all_summary),
        "n_sig": sum(r["p_holm"] < dataset.ALPHA for r in all_summary),
        "n_models": len(hits), "hit_lo": min(hits), "hit_hi": max(hits),
        # 생성기 기본값(인기 하위 20% 안에서 균등하게 고름)의 1등 기대 수령액 ÷ 자동(무작위) 구매 − 1.
        # popularity.fit 이 make.js 규칙 그대로 전 조합을 열거한 구간 평균 (자체 리뷰 J1 — 전에는 백분위 격자
        # 평균으로 근사했고 기준이 '인기도 0 인 조합' 이라 +14% 로 보였다)
        "gain20": S["bucket_gain"]["20"] - 1,
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
    v["alpha"] = dataset.ALPHA
    # ── 값에서 만드는 문장의 재료 (자체 리뷰 L1 — 고정 문장은 값이 바뀌어도 그대로 남았다)
    v["era_top_distinct"] = len({t[0] for t in st["eras"]["top_by_era"]}) == len(st["eras"]["top_by_era"])
    band = fq["band_bonferroni"]
    v["freq_in_band"] = band[0] <= min(fq["counts"]) and max(fq["counts"]) <= band[1]
    v["feature_sig"] = [r["question"] for r in st["summary"]
                        if "무작위 조합과 다른가" in r["question"] and r["p_holm"] < dataset.ALPHA]
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
    v["logloss_better"] = [r["model"] for r in real["rows"] if r.get("dlogloss") is not None and r["dlogloss"] < 0]
    svr = lo["svr"]["r2_oof"]
    ols = next(v_ for k, v_ in svr.items() if k.startswith("OLS"))
    v["svr_better"] = [k for k, r2 in svr.items() if k.startswith("SVR") and r2 > ols]
    dd = lo["ddpm"]
    # 확산 모델 적중의 판정 — 양측 검정, 기준은 ALPHA (고정 문구 "무작위와 같음" 대신, 자체 리뷰 K1)
    v["ddpm_hits_same"] = abs(dd["hits_one_per_draw"]["z"]) < NormalDist().inv_cdf(1 - dataset.ALPHA / 2)
    # 학습 데이터의 우연한 빈도와의 상관 — 45개 번호의 상관이라 r 만으로는 판정할 수 없다 (Fisher z, 양측)
    r = dd["corr_with_train_freq"]
    v["ddpm_corr_p"] = math.erfc(abs(math.atanh(r) * math.sqrt(45 - 3)) / math.sqrt(2))
    # 번호 사용 편차 = X² / 39 (비복원 6개 추출이라 균등 무작위일 때 X² 의 기대가 39) — 기록된 값으로 판정한다
    # (전에는 analysis.json 에 없는 '학습을 4배로 늘려도 3배 이상' 을 적었다). X²·44/39 ~ χ²(44), 임계값은
    # Wilson–Hilferty 근사 (웹앱은 scipy 없이 돈다).
    eg = dd["n_generated"] * 6 / 45
    gx2 = sum((c - eg) ** 2 / eg for c in dd["number_counts"])
    zq = NormalDist().inv_cdf(1 - dataset.ALPHA)
    crit = 44 * (1 - 2 / (9 * 44) + zq * math.sqrt(2 / (9 * 44))) ** 3
    v["ddpm_disp"], v["train_disp"] = gx2 / 39, st["frequency"]["chi2"] / 39
    v["ddpm_disp_sig"] = gx2 * 44 / 39 > crit
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
    shares = [s / S["share_auto_mean"] for s in S["share_at_pct"]]  # 기준 = 자동(무작위) 구매의 평균 몫
    i90 = S["pct"].index(90.0)
    v["payoff_chart"] = line_chart(
        S["pct"], shares, ref=1.0, x_ticks=[0, 25, 50, 75, 100], x_fmt=lambda t: f"{t:g}%",
        y_fmt=lambda t: f"{t:.2f}배",
        marks=[{"x": 10.0, "label": f"10% 지점: {shares[i10]:.2f}배"},  # 곡선 위의 점 (구간 평균은 bucket_gain)
               {"x": 90.0, "label": f"90% 지점: {shares[i90]:.2f}배", "anchor": "end"}],
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

    # ── 원본 정본과 분석 스냅샷이 같은가 (fetch 만 하고 build_results 를 안 돌리면 갈라진다)
    R = raw()
    want = {k: f["sha256"] for k, f in R["manifest"]["files"].items()}
    have = {k: f["sha256"] for k, f in meta["source"]["files"].items()}
    v["stale"] = want != have
    v["raw_latest"] = R["lotto"][-1].round

    # ── 회차별 당첨번호 (누적 히스토리 — 동행복권 '누적히스토리'·'1등 당첨금 비교' 를 참고)
    L = R["lotto"]
    v["history"] = [{"round": d.round, "date": d.date.isoformat(), "nums": " · ".join(f"{x:02d}" for x in d.numbers),
                     "bonus": f"{d.bonus:02d}", "w": d.winners, "p1": d.prize[0],
                     "split": None if d.first_auto is None else (d.first_auto, d.first_manual, d.first_semi),
                     "sales": d.sales} for d in reversed(L)]
    v["latest_draw"] = {"round": L[-1].round, "date": L[-1].date.isoformat(),
                        "nums": [(x, _ball_cls(x)) for x in L[-1].numbers], "bonus": (L[-1].bonus, _ball_cls(L[-1].bonus)),
                        "w": L[-1].winners, "prize": L[-1].prize}
    recent = L[-104:]
    paid = [d for d in recent if d.winners[0] > 0]
    avg1 = sum(d.prize[0] for d in paid) / len(paid)
    v["prize_chart"] = columns(
        [d.prize[0] / 1e8 for d in recent], [str(d.round) for d in recent], x_every=13, ref=avg1 / 1e8,
        y_fmt=lambda t: f"{t:g}억", aria="최근 104회 1등 1인당 당첨금",
        titles=[f"{d.round}회 ({d.date}): 1인당 {won(d.prize[0])}원 · 1등 {d.winners[0]}명" for d in recent])
    v["winners_chart"] = columns(
        [d.winners[0] for d in recent], [str(d.round) for d in recent], x_every=13,
        ref=sum(d.games for d in recent) / len(recent) / dataset.N_COMB, y_fmt=lambda t: f"{t:g}명",
        aria="최근 104회 1등 당첨자 수",
        titles=[f"{d.round}회: 1등 {d.winners[0]}명 · 판매 {won(d.games)}게임" for d in recent])
    v["prize_avg1"] = avg1
    v["prize_minmax"] = (min(paid, key=lambda d: d.prize[0]), max(paid, key=lambda d: d.prize[0]))
    v["phistory"] = [{"round": d.round, "date": d.date.isoformat(), "group": d.group, "number": d.number,
                      "bonus": d.bonus} for d in reversed(R["pension"])]

    # ── 흔한 주장 판정표 — 국내 로또 앱·사이트의 공통 기능(출현·미출현 통계, 궁합수, 패턴 필터,
    #    AI 추천 …)과 동행복권 '복권의 오해와 진실' 을 참고해, 각 주장에 이 데이터의 답을 붙인다.
    b5 = pop["number_effect"]["beta"]
    th, thp = pop["tiers"]["5"]["theta"], pop["tiers"]["5"]["theta_p"]
    v["birthday_more"] = sum(b5[:31]) / 31 > sum(b5[31:]) / 14
    v["avoid_prev"] = th["prev_overlap"] < 0 and thp["prev_overlap"] < dataset.ALPHA
    v["pref_prev"] = th["prev_overlap"] > 0 and thp["prev_overlap"] < dataset.ALPHA
    v["row1_more"] = sum(b5[:7]) / 7 > sum(b5) / 45 > sum(b5[42:]) / 3  # 용지 첫 줄 인기 · 마지막 줄 비인기
    v["number_effect_sig"] = pop["number_effect"]["wald_p"] < dataset.ALPHA
    feats, sig = st["features"], v["sig"]
    check = "차이 있음 — 검토"  # 보정 후 유의: 원인을 확인하기 전까지 그 주장을 판정하지 않는다
    hot, half = sig("특정 번호가 더 잘 나오나"), sig("과거 빈도가 미래 빈도를 예고하나")
    gap = sig("간격 분포")
    pairs = pr["n_sig_holm"] > 0 or any(sig(k) for k in ("990쌍", "가장 자주 함께", "세 개 묶음"))
    run = sig("연번 쌍") or sig("이월수")
    v["myths"] = [
        ("핫·콜드 번호 (많이 나온 번호가 또 나온다)", check if hot or half else "다르지 않음",
         f"번호별 빈도 p = {fmt_p(fq['p_mc'])}. 전반기·후반기 빈도 상관 r = {fq['half_split_r']:.2f} — "
         + ("보정 후에도 유의한 관계다" if half else "많이 나온 번호가 이후에 더 나오지 않았다"),
         "random", "freq"),
        ("오래 안 나온 번호는 나올 때가 됐다", check if gap else "다르지 않음",
         f"출현 간격이 기하분포와 다르다 (보정 후에도 유의, p = {fmt_p(gp['p_mc'])})" if gap else
         f"출현 간격은 기하분포 그대로 (p = {fmt_p(gp['p_mc'])}). 몇 회를 쉬었든 다음 회 확률은 6/45 = 13.3%",
         "random", "gaps"),
        ("궁합수 (같이 잘 나오는 번호)", check if pairs else "다르지 않음",
         f"990쌍 중 다중비교 보정 후 유의한 쌍 {pr['n_sig_holm']}개. 보정 전 p<0.05 {pr['n_raw_p05']}쌍 "
         f"(우연 기대 {pr['n_raw_p05_expected']:.0f}쌍)",
         "random", "pairs"),
        ("총합·홀짝·고저·구간 패턴으로 거르기", check if v["feature_sig"] else "확률 불변",
         "보정 후에도 전수 분포와 다른 지표: " + " · ".join(v["feature_sig"]) if v["feature_sig"] else
         f"분포가 814만 조합 전수와 구분되지 않는다 (총합 p = {fmt_p(feats['sum']['p'])}, 홀짝 p = {fmt_p(feats['odd']['p'])}). "
         "거르면 고를 조합 수만 줄고 한 장의 확률은 그대로",
         "random", "sum"),
        ("연속번호·이월수", check if run else "다르지 않음",
         f"연번 분포 p = {fmt_p(feats['consec']['p'])}, 이월수 p = {fmt_p(lg['carry_p'])}",
         "random", "carry"),
        ("AI·머신러닝 번호 예측", check if vd["ml"]["sig"] else "못 맞힘",
         f"{len(hits)}개 전략 평균 적중 {v['facts']['hit_lo']:.2f}~{v['facts']['hit_hi']:.2f}개 (무작위 0.8개), "
         f"보정 후 가장 작은 p = {fmt_p(vd['ml']['min_p'])}",
         "ml", "board"),
        ("고정수·제외수 지정", "기능으로 채택",
         "본인이 고르고 싶은 번호를 반영하는 편의 기능. 당첨 확률은 바뀌지 않는다", "make", None),
        ("내 번호로 지난 회차를 다시 사 보기 (백테스트)", "기능으로 채택",
         "1회부터 매주 같은 번호를 샀다면 — 등수별 횟수와 받은 돈 vs 쓴 돈. 과거 성적은 운이다", "make", "check"),
        ("세금·실수령액 계산", "기능으로 채택",
         "동행복권 당첨자 가이드의 원천징수 세율 (200만 원 이하 비과세, 3억까지 22%, 초과분 33%)", "make", "tax"),
        ("휠링 (번호 여러 개를 여러 게임으로 덮기)", "채택 안 함",
         "한 장의 기대값은 그대로이고 작은 당첨을 고르게 만들 뿐이다 (위키백과 Lottery wheeling)", None, None),
        ("명당 판매점", "판정 안 함",
         "판매점별 판매량 자료가 없어 이 데이터로는 판정할 수 없다", None, None),
    ]
    return v


def generator_payload() -> dict:
    """번호 생성기(make.js)가 받는 값 — 인기도 점수 계수, 확산 모델 번호 풀, 전 회차(백테스트용).

    rounds 는 원본 정본에서: [회차, 번호 6개, 보너스, 1~5등 1인당 당첨금, 게임 가격, 1~3등 당첨자 수].
    1~3등은 나눠 갖는 몫이라 백테스트가 '내가 한 명 더' 로 1인당 × w/(w+1) 을 쓴다 (자체 리뷰 H1). 그 등수
    당첨자가 없던 회차는 금액이 0 으로 기록돼 있어 금액 미상으로 따로 센다. backtest 는 같은 규칙으로 814만
    조합 전부의 회수율 분포 — 내 번호의 순위를 매기는 기준이다.
    """
    D, R = load(), raw()
    return {
        "score": D["lotto"]["popularity"]["score"],
        "ddpm_pool": D["lotto"]["ddpm_pool"],
        "rounds": [[d.round, *d.numbers, d.bonus, *d.prize, d.price, *d.winners[:3]] for d in R["lotto"]],
        "backtest": D["lotto"]["backtest"],
        "pension_past": [[d.round, d.number] for d in R["pension"]],
        "latest_round": R["lotto"][-1].round,
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
        ("history", "prizes", "1등 1인당 당첨금 추이"), ("history", "all-rounds", "전 회차 당첨번호 표"),
        ("make", "tax", "당첨금 세금 계산"), ("make", "check", "내 번호 백테스트"), ("home", "myths", "흔한 주장 판정표"),
    ]:
        items.append({"t": title, "d": dict((s[0], s[2]) for s in SECTIONS)[name], "u": u(name, anchor), "k": "카드"})
    return items
