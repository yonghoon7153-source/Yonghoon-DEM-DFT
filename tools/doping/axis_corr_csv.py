#!/usr/bin/env python3
"""axis_corr_csv.py — 정본 cascade CSV 의 **목적 축들이 서로 붙어 있나**를 본다.

왜 (2026-08-25, Yang 2026(BML) `Fig. 17` 에서 이전):
  다목적 최적화는 축이 **독립일 때만** 일을 한다. 두 축이 좁은 띠를 그리면 그건 사실상
  한 축이고, Pareto 를 돌려도 그 축은 안 움직인다. 저쪽 실측: σ↔Q_CC 가 붙어 있어
  Pareto 후 σ 는 −2.9 %, 독립축인 Damage 만 −64.5 % 였다.
  우리는 지금 가중합(`--w_e/w_v/w_s/w_c`)으로 축을 하나의 숫자로 **뭉개고** 있어서
  충돌이 있는지조차 화면에 안 나온다 (open_items #11: b2o3 전도 1등 ↔ 공기안정성 최악군).

  ⚠ 출처는 **DEM 축 문헌**이고 여기 적용 대상은 **DFT 축 cascade** 다. 이전한 것은
    수치가 아니라 **절차**뿐이다 (kb/methodology/microstructure_ml_transfer_to_cascade_2026_08_25.md).

이 도구가 **못 하는 것**
  · 인과를 말하지 않는다. 붙어 있다 ≠ 하나가 다른 하나를 만든다.
  · 상관이 낮다고 그 축이 **중요한** 것도 아니다 — 독립일 뿐이다.
  · 결측이 많은 축은 그 사실만 적고 판정하지 않는다 (적은 표본의 ρ 는 못 믿는다).
  · 순위를 매기거나 후보를 고르지 않는다.

    python3 tools/doping/axis_corr_csv.py
    python3 tools/doping/axis_corr_csv.py --csv <경로> --min_n 50
    python3 tools/doping/axis_corr_csv.py --pareto
    python3 tools/doping/axis_corr_csv.py --stability      # 축이 자기 자신을 재현하나
    python3 tools/doping/axis_corr_csv.py --selftest

⭐ `--stability` (2026-08-30) — front·사전등록이 서 있는 축들이 **같은 구조를 다시 쟀을 때
   같은 순위를 주는지** 본다. 새 계산 0. 이걸 안 재고 사전등록 `|ρ| ≥ 0.35` 를 시험하면
   실패 가지가 물리가 아니라 재평가 잡음으로 켜질 수 있다.
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_CSV = os.path.join(ROOT, "db", "properties", "cascade_v23_all.csv")

#: |ρ| 가 이보다 크면 '사실상 한 축' 으로 본다.
COLLINEAR = 0.85
#: 이보다 표본이 적으면 판정하지 않는다 — 적은 n 의 ρ 는 우연이 쉽다.
MIN_N = 30

#: 우리 cascade 의 목적 축. **부호를 여기서 통일한다** — "클수록 좋다" 로 맞춰야
#: 상관의 부호가 곧 '같이 좋아지나 / 반대로 가나' 를 뜻한다.
#:   (열이름, 표시이름, higher_is_better)
AXES = [
    ("screen_de_per_atom",      "안정성(ΔE)",   False),   # 낮을수록 안정
    ("li_mobility_score",       "Li 이동도",    True),
    ("sigma_300K_S_cm_NE",      "σ(300K)",      True),
    ("bvs_li_proxy_score",      "BVS 프록시",   True),
    ("elastic_G_hill_GPa",      "전단탄성 G",   True),
    ("elastic_pugh_GoverB",     "Pugh G/B",     False),   # 낮을수록 연성
    ("wad_J_m2_mean",           "부착일 W_ad",  True),
    ("screen_dV_over_V0",       "|ΔV/V0|",      False),   # 작을수록 좋다(절대값)
    ("migration_volume_fraction", "이동부피비", True),
    # ⭐ 2026-08-28 신설 — 절대 σ 를 대체하는 **비** 축. host(modelc) 대비 600 K D 비.
    #   아직 비어 있다: T13(200 ps 타당성)이 내일 답해지면 Pareto front 39설계에 돌린다.
    ("D_rel_vs_host",           "D비(vs host)", True),
]

#: ⛔ **파생 축** — 다른 축들의 산술 조합이라 그 축들과의 상관이 **정의상** 높다.
#:   그걸 '독립성이 깨졌다' 로 읽으면 안 된다. 발견이 아니라 공식이다.
#:   li_mobility_score = 3*migration_volume_fraction + bvs_li_proxy_score
#:     (tools/doping/bvse_proxy.py backfill_one)
#:   실측: ρ(이동도, 이동부피비)=+0.77 · ρ(이동도, BVS)=+0.48 — 3:1 가중과 정확히 정합.
DERIVED = {
    "li_mobility_score": ("migration_volume_fraction", "bvs_li_proxy_score"),
}


#: 이 축들은 **절대값**으로 읽는다 — 열은 부호 있는 값인데 의미는 크기다.
#:   ⛔ 2026-08-28 — `analyse()` 는 이 규칙을 지키고 있었는데 새로 붙인 `pareto()` 가
#:     안 지켜서, 부피가 **33 % 줄어든** 후보가 5 % 줄어든 후보를 이기고 front 에 올랐다.
#:     같은 파일 안에서 두 경로가 갈렸다 — 규약을 이름 하나로 묶어 다시 갈라지지 않게 한다.
ABS_AXES = {"screen_dV_over_V0"}


#: ⛔⛔ **이미 무효 판정이 난 축** — 2026-08-19 (kb/projects/cascade_pipeline_fixes_2026_08_19.md).
#:   기준 구조가 미수렴이라 그 기준에 대한 상대·절대값이 둘 다 의미가 없다.
#:   그런데 2026-08-28 A3 Pareto 를 **이 축들을 넣은 채로** 돌렸다 — 9일 전에 우리가
#:   직접 내린 판정을 안 읽었다. front 160/681 은 그래서 물리가 아니라 진단이었다.
#:   ⇒ 이제 **도구가 거부한다.** 사람이 기억하기를 기다리면 또 놓친다.
INVALID_AXES = {
    "screen_dV_over_V0":
        "미수렴 기준 대비 미수렴 값 — 비율 자체가 무의미 (2026-08-19 판정)",
    "screen_de_per_atom":
        "기준이 미수렴이라 **절대값 인용 금지**. Pareto 는 설계간 절대 비교라 해당된다 "
        "(2026-08-19 판정). 같은 cascade 안 상대 비교는 별개 문제다",
    # ⛔ 2026-08-28 결정 — 절대 σ 는 **우리가 스스로 인용 금지한 값**이다.
    #   CLAUDE.md: "σ는 Nernst–Einstein(Haven=1) — 절대값 인용 금지, 비율도 멀티시드 판정만."
    #   컬럼 이름이 절대값(S/cm)이라, 채우면 못 쓴다고 정한 값을 축으로 삼는 셈이 된다.
    #   ⇒ 대체 축은 `D_rel_vs_host` (아래). 같은 MD 로 나오지만 **비**라서 규율에 맞고,
    #     1T 로 충분해 아레니우스(3T)보다 3배 싸다.
    "sigma_300K_S_cm_NE":
        "절대 σ 는 인용 금지 (CLAUDE.md). 대체 축 `D_rel_vs_host` 를 쓸 것 (2026-08-28 결정)",
    "sigma_md_D_300K_cm2s":
        "절대 D 도 같은 이유로 축이 될 수 없다 — 비로 바꿀 것 (2026-08-28)",
    # ⛔ W_ad 는 '무효' 가 아니라 **미교정**이다. rigid-분리 W_ad 가 45–225 J/m² 인데
    #   실험은 0.2–0.4 다 (adhesion_calibration_decision_2026_05_17.md). 100배 어긋난 축을
    #   채우는 것은 빈 축보다 나쁘다 — 빈 축은 없다는 걸 알지만, 틀린 축은 믿게 된다.
    #   교정된 v2 melt-quench 계열(1.107 J/m²)로 파이프라인을 옮긴 뒤 풀 것.
    "wad_J_m2_mean":
        "**미교정** — rigid-분리 45–225 J/m² vs 실험 0.2–0.4. v2 melt-quench 로 교정 후 해제 "
        "(2026-08-28 보류)",
}

#: 상대 D 축의 게이트. **외부 근거**: Deng 2026 Angew (litdb `deng2026_polysulfate…`) 가
#: 표면 개질에서 σ 손실 **7 % 는 허용, 31 %(0.4 M) 는 실패**로 실험 경계를 그었다.
#: 우리 문턱은 그 사이에서 보수적으로 잡는다 — host 대비 D 가 이 값 아래로 떨어지면 탈락.
#: ⛔ 이건 **문헌에서 빌린 경계**지 우리가 잰 값이 아니다. 우리 계에서 재검토할 것.
D_REL_GATE = 0.90


def preregister(designs, targets, predictor="li_mobility_score", top_k=10):
    """**측정 전에** 예측을 얼려 둔다 → 나중에 진짜 prospective 검증이 된다.

    ⛔⛔ 왜 필요한가 (2026-08-28, tu2026 에서 이전) — 우리 acquisition 근거는
      `db/properties/cascade_audit_ml_validation.csv` 의 enrichment 1.22 (p=0.426) 와
      ordering 3.35 인데, **둘 다 retrospective** 다. 이미 아는 답 위에서 순위를 매긴 것이라
      "맞혔다" 가 사후 서술이 된다. tu2026 은 prospective 검증(n=4)을 냈고 우리는 0이다.
      그쪽 CV 규약은 우리와 병치 못 하지만(랜덤 폴드), **prospective 를 한다는 절차 자체**는
      우리에게 없던 것이고, 비판만 옮기면 그대로 되돌아온다.

    무엇을 얼리나: 라벨이 **아직 존재하지 않는** 39설계에 대한 순위 + 성공 기준 + 입력 해시.
    D_rel 측정이 내일 들어오면 그때 채점한다. 지금은 채점할 수 없다 — 그게 요점이다.

    ⛔ 못 하는 것
      · **채점하지 않는다.** 라벨이 없다. 이 함수는 기록만 남긴다.
      · 예측기를 고르지 않는다 — 부르는 쪽이 정하고, 그 이름이 기록에 남는다.
      · 순위가 맞아도 **인과가 아니다.** 이동도 기술자와 D 가 같이 움직인다는 것뿐이다.
    """
    by_name = {}
    for d in designs:
        nm = d.get("name")
        if nm:
            by_name[nm] = d
    rows = []
    for t in targets:
        d = by_name.get(t.get("name"))
        v = _f((d or {}).get(predictor))
        rows.append({"name": t.get("name"), "dopant": t.get("dopant"),
                     predictor: v})
    scored = [r for r in rows if r[predictor] is not None]
    scored.sort(key=lambda r: -r[predictor])          # 클수록 이동도가 높다는 예측
    for i, r in enumerate(scored):
        r["predicted_rank"] = i + 1
    return {
        "frozen_at": _dt.datetime.now().isoformat(timespec="seconds"),
        "predictor": predictor,
        "predictor_definition": "li_mobility_score = 3×migration_volume_fraction "
                                "+ bvs_li_proxy_score (tools/doping/bvse_proxy.py)",
        "n_targets": len(targets), "n_scored": len(scored),
        "unscored": [r["name"] for r in rows if r[predictor] is None],
        "예측": f"이 순위가 곧 측정될 D_rel_vs_host 순위와 **양의 상관**을 가진다",
        "성공기준_사전확정": {
            "1_주기준": "Spearman(predicted_rank, D_rel) < 0 (순위가 반대이므로 음수가 정합) "
                       "이고 |ρ| ≥ 0.35 · p < 0.05",
            "2_보조": f"상위 {top_k}개의 게이트 통과율(D_rel ≥ {D_REL_GATE})이 "
                     f"하위 {top_k}개보다 높다",
            "3_실패로_읽는_경우": "|ρ| < 0.2 이면 이동도 기술자는 D 를 예측하지 못한다 — "
                              "cascade 이동도 축의 근거가 없어진다",
            "⛔": "기준을 **측정 뒤에 고치지 않는다.** 고치면 이 기록의 의미가 사라진다"},
        "ranking": scored,
    }


def axis_fill(rows, axes):
    """축별 채움 수 → {키: n}. Pareto 를 돌리기 **전에** 본다.

    ⛔⛔ 2026-08-28 실측 — 왜 이게 필요한가. 기본 축 6개로 돌렸더니 채점 가능한 행이
      **0개**였다. 원인은 `sigma_300K_S_cm_NE` 와 `wad_J_m2_mean` 이 **3,615행 전부 비어
      있어서**다. 한 축이라도 완전히 비면 교집합이 0 이 되어 front 가 통째로 사라진다.
      그런데 예전 출력은 "채점 가능 0개" 한 줄뿐이라 **어느 축 때문인지** 안 보였다.
      ⇒ 데이터가 아예 없는 축은 비교에 기여할 수 없으므로 **빼고, 뺐다고 크게 말한다.**
    """
    return {k: sum(1 for r in rows if _f(r.get(k)) is not None) for k, _l, _h in axes}


def valid_axes(axes, allow_invalid=False):
    """축 목록에서 무효 축을 걷어낸다 → (남은 축, 걷어낸 [(키, 사유)])."""
    if allow_invalid:
        return list(axes), []
    keep = [a for a in axes if a[0] not in INVALID_AXES]
    drop = [(a[0], INVALID_AXES[a[0]]) for a in axes if a[0] in INVALID_AXES]
    return keep, drop


def axis_value(key, v):
    """축 하나의 **읽는 값**. 절대값 축이면 크기로 바꾼다."""
    return None if v is None else (abs(v) if key in ABS_AXES else v)


def design_key(row, comp_cols):
    """**설계 하나**의 정체. 이름이 아니라 실제 조성으로 만든다.

    ⛔⛔ 왜 필요한가 (2026-08-28, 리뷰 K) — 정본 CSV 3,615행은 3,615개 설계가 **아니다.**
      `n_units = max(1, round(n_fu_actual × x))` 인데 `n_fu_actual = 4` 라서
      x=0.02/0.05/0.10 이 전부 `round(...)=0 → max(1,0)=1` 로 접힌다. 실측:
      **`concentration` 열이 3,615행 전부 0.25** 다. 즉 x020·x050·x100 은 같은 조성의
      **다른 이름**이고, 거기에 시드 s00–s04 가 곱해져 있다.
      ⇒ 이름으로 세면 3,615, 조성으로 세면 **237**. 그 차이를 표본 수로 쓰면
      "3,615개 중 160개" 같은 문장이 만들어진다 — 표본이 15배 부풀려진 것이다.

    ⛔ 못 하는 것
      · **원자 매핑 해시가 아니다.** CSV 에 시작 구조 해시가 없어서 조성+자리+전하보상으로
        대신한다. 같은 조성인데 도판트 **배치**가 다른 것은 여기서 같은 설계로 묶인다
        (그건 사실상 시드다 — 그래서 묶는 게 맞지만, 구조가 진짜 다르면 놓친다).
      · 이름 기반 셈(x 라벨 제거 후 229)과 **8개 차이**가 난다. 어느 쪽도 아직 검증 안 됐다.
    """
    return (tuple(row.get(c, "") for c in comp_cols),
            row.get("cation_site", ""), row.get("anion_site", ""),
            row.get("charge_compensation", ""))


def _median(xs):
    s = sorted(xs)
    n = len(s)
    return None if not n else (s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2]))


def aggregate_designs(rows, axes):
    """행 → **설계**. 축마다 복제본의 중앙값을 쓰고 산포를 같이 남긴다.

    중앙값인 이유: 복제본은 시드(그리고 가짜 x 라벨)이고, 그중 일부는 미수렴이라
    평균이 끌려간다. 순위 상관·Pareto 는 중앙값으로 충분하다.

    돌려주는 것: (designs, info). designs 의 각 행은 원 CSV 행 모양 + `n_replicates`,
    축별 `<축>__spread` (max−min).

    ⛔ 못 하는 것
      · 산포를 **오차막대로 쓰지 마라.** 시드 5개(+가짜 x 3개)는 같은 파이프라인의
        같은 설정이라 계통오차가 공통이다. 통계오차 하한일 뿐이다.
    """
    comp_cols = [c for c in (rows[0] if rows else {}) if c.startswith("composition_")]
    g = {}
    for r in rows:
        g.setdefault(design_key(r, comp_cols), []).append(r)
    out = []
    for _k, v in g.items():
        base = dict(v[0])
        base["n_replicates"] = len(v)
        for key, _lab, _hi in axes:
            vals = [x for x in (_f(r.get(key)) for r in v) if x is not None]
            base[key] = "" if not vals else _median(vals)
            base[key + "__spread"] = "" if len(vals) < 2 else (max(vals) - min(vals))
        out.append(base)
    return out, {"n_rows": len(rows), "n_designs": len(out),
                 "comp_cols": len(comp_cols),
                 "replicates_per_design": sorted({d["n_replicates"] for d in out})}


def is_definitional(a, b):
    """두 축이 '파생 축 ↔ 그 재료' 관계인가. → bool"""
    return b in DERIVED.get(a, ()) or a in DERIVED.get(b, ())


def _f(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def spearman(a, b):
    """순위 상관 (scipy 없이). 동점은 평균순위. 못 재면 None."""
    if len(a) < 3:
        return None
    if len(set(a)) < 2 or len(set(b)) < 2:
        return None          # 한쪽이 상수 — 상관이 정의되지 않는다

    def rank(x):
        order = sorted(range(len(x)), key=lambda i: x[i])
        r = [0.0] * len(x)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and x[order[j + 1]] == x[order[i]]:
                j += 1
            avg = (i + j) / 2.0
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    ra, rb = rank(a), rank(b)
    ma, mb = sum(ra) / len(ra), sum(rb) / len(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))
    return num / den if den else None


def load(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def analyse(rows, min_n=MIN_N):
    cols, cover = {}, {}
    for key, label, hib in AXES:
        vals = [_f(r.get(key)) for r in rows]
        n = sum(v is not None for v in vals)
        cover[key] = (label, n, len(rows))
        if n >= min_n:
            # 부호 통일: 전부 "클수록 좋다" 로. |ΔV| 는 절대값을 먼저 취한다.
            vals = [axis_value(key, v) for v in vals]
            cols[key] = (label, [(-v if (v is not None and not hib) else v) for v in vals])
    pairs = []
    keys = list(cols)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            va, vb = [], []
            for x, y in zip(cols[a][1], cols[b][1]):
                if x is not None and y is not None:
                    va.append(x); vb.append(y)
            if len(va) < min_n:
                pairs.append({"a": a, "b": b, "la": cols[a][0], "lb": cols[b][0],
                              "rho": None, "n": len(va), "collinear": False,
                              "definitional": is_definitional(a, b),
                              "why": "표본 부족"})
                continue
            rho = spearman(va, vb)
            pairs.append({"a": a, "b": b, "la": cols[a][0], "lb": cols[b][0],
                          "rho": rho, "n": len(va),
                          "collinear": bool(rho is not None and abs(rho) >= COLLINEAR),
                          "definitional": is_definitional(a, b),
                          "why": None if rho is not None else "한쪽이 상수"})
    pairs.sort(key=lambda p: -(abs(p["rho"]) if p["rho"] is not None else -1))
    return {"pairs": pairs, "coverage": cover, "n_rows": len(rows), "min_n": min_n}


def report(rep):
    print(f"\n{'='*76}")
    print(f" cascade 목적 축 상관 — Pareto·가중치 조정이 일을 할 수 있나 (행 {rep['n_rows']})")
    print(f"{'='*76}")
    print("  ⚠ 부호는 '클수록 좋다' 로 통일했다 — ρ>0 = 같이 좋아진다 · ρ<0 = 상충(trade-off)\n")
    print("  ── 축 커버리지 (결측이 많으면 판정 자체를 안 한다) ──")
    for key, (label, n, tot) in rep["coverage"].items():
        pct = 100.0 * n / tot if tot else 0
        mark = "✅" if n >= rep["min_n"] else "·"
        print(f"    {mark} {label:12s} {n:5d}/{tot} ({pct:5.1f} %)  {key}")
    print("\n  ── 축 쌍 ──")
    col = [p for p in rep["pairs"] if p["collinear"] and not p.get("definitional")]
    defn = [p for p in rep["pairs"] if p.get("definitional") and p["rho"] is not None]
    trade = [p for p in rep["pairs"]
             if p["rho"] is not None and p["rho"] <= -0.3
             and not p["collinear"] and not p.get("definitional")]
    for p in rep["pairs"]:
        if p["rho"] is None:
            print(f"    ·  {p['la']:12s} ↔ {p['lb']:12s}   ρ = —      ({p['why']}, n={p['n']})")
            continue
        if p.get("definitional"):
            m, tail = "📐", "   ← 정의상 (파생축 ↔ 그 재료)"
        else:
            m = "⛔" if p["collinear"] else ("🔻" if p["rho"] <= -0.3 else
                                            ("🟡" if abs(p["rho"]) >= 0.6 else "✅"))
            tail = ""
        print(f"    {m} {p['la']:12s} ↔ {p['lb']:12s}   ρ = {p['rho']:+.3f}   n={p['n']}{tail}")
    print()
    if col:
        print(f"  ⛔ **사실상 한 축인 쌍 {len(col)}건** — 그 축들끼리는 Pareto 가 선택지를 못 준다:")
        for p in col:
            print(f"       {p['la']} ↔ {p['lb']}  (ρ {p['rho']:+.3f})")
    if trade:
        print(f"  🔻 **상충하는 쌍 {len(trade)}건** — 여기가 다목적이 실제로 일하는 자리다:")
        for p in trade[:6]:
            print(f"       {p['la']} ↔ {p['lb']}  (ρ {p['rho']:+.3f})")
    if defn:
        print(f"  📐 **정의상 붙은 쌍 {len(defn)}건 — 판정에서 제외했다.**")
        for p in defn:
            print(f"       {p['la']} ↔ {p['lb']}  (ρ {p['rho']:+.3f})  "
                  f"{p['a'] if p['a'] in DERIVED else p['b']} 가 상대의 산술 조합이다")
        print(f"     발견이 아니라 공식이다 — 독립성 판정의 근거로 쓰면 안 된다.")
    free = [p for p in rep["pairs"]
            if p["rho"] is not None and not p.get("definitional")]
    if free:
        top = max(free, key=lambda p: abs(p["rho"]))
        print(f"  ▸ **정의상 쌍을 뺀 최대 |ρ| = {abs(top['rho']):.3f}** "
              f"({top['la']} ↔ {top['lb']}) — 공선성 문턱 {COLLINEAR} 대비")
    if not col and not trade:
        print("  ✅ 뚜렷한 공선성도 상충도 없다 — 축이 대체로 독립이다.")
    print("\n  ⛔ 인과는 말하지 않는다. 상관이 낮다고 그 축이 중요한 것도 아니다(독립일 뿐).")


def _selftest():
    ok = True

    def say(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m)
        ok = ok and c

    print("── axis_corr_csv selftest ──")
    say(abs(spearman(list(range(20)), list(range(20))) - 1.0) < 1e-12, "① 완전 일치 → ρ=1")
    say(abs(spearman(list(range(20)), list(range(19, -1, -1))) + 1.0) < 1e-12,
        "① 완전 역순 → ρ=−1")
    say(spearman([1, 1, 1], [1, 2, 3]) is None, "② [음성] 한쪽이 상수면 None (0 이 아니다)")
    say(spearman([1, 2], [1, 2]) is None, "② [음성] 표본 3 미만이면 None")
    say(abs(spearman([1, 2, 2, 3], [1, 2, 2, 3]) - 1.0) < 1e-12, "③ 동점 평균순위 처리")
    # ④ [음성] 결측이 많은 축은 판정에서 빠져야 한다
    rows = [{"screen_de_per_atom": str(i), "li_mobility_score": ""} for i in range(50)]
    rep = analyse(rows, min_n=30)
    say(all(p["a"] != "li_mobility_score" and p["b"] != "li_mobility_score"
            for p in rep["pairs"]),
        "④ [음성] 결측 축은 쌍에서 빠진다 (적은 n 의 ρ 를 믿지 않는다)")
    # ⑤ 부호 통일 — '낮을수록 좋은' 두 축은 뒤집힌 뒤 **양의 상관**이어야 한다
    rows = [{"screen_de_per_atom": str(i), "screen_dV_over_V0": str(i / 100.0)}
            for i in range(60)]
    rep = analyse(rows, min_n=30)
    p = rep["pairs"][0]
    say(p["rho"] is not None and p["rho"] > 0.99,
        f"⑤ 낮을수록 좋은 두 축은 부호 통일 뒤 ρ>0 ({p['rho']})")
    # ── 파생 축 (2026-08-25) ────────────────────────────────────────────
    say(is_definitional("li_mobility_score", "migration_volume_fraction"),
        "⑥ 파생축 ↔ 그 재료를 '정의상' 으로 잡는다")
    say(is_definitional("migration_volume_fraction", "li_mobility_score"),
        "⑥ 순서를 바꿔도 잡는다")
    say(not is_definitional("screen_de_per_atom", "elastic_G_hill_GPa"),
        "⑥ [음성] 무관한 두 축을 정의상으로 오인하지 않는다")
    say(not is_definitional("migration_volume_fraction", "bvs_li_proxy_score"),
        "⑥ [음성] 같은 공식의 **재료끼리**는 정의상 아니다 (서로 독립 측정)")

    # ── Pareto (A3, 2026-08-28) — **음성 경로가 핵심**이다 ────────────────────
    # ⚠ 2026-08-28 — 이 fixture 는 원래 `screen_de_per_atom` 을 썼는데 그 축이 **무효 판정**을
    #   받아 도구가 거부한다. 여기서 시험하는 건 Pareto 역학이지 그 축이 아니므로,
    #   유효한 "낮을수록 좋은" 축(Pugh G/B)으로 바꾼다. **2026-08-28 재차**: 짝이던
    #   `wad_J_m2_mean` 도 미교정으로 보류돼 `elastic_G_hill_GPa` 로 바꿨다. --allow_invalid 로 우회하지 않는다 —
    #   그러면 거부 기능이 테스트에서만 꺼진 채 남는다.
    A = [("elastic_pugh_GoverB", "낮을수록", False), ("elastic_G_hill_GPa", "높을수록", True)]
    R = [{"id": "win_both", "elastic_pugh_GoverB": "-1.0", "elastic_G_hill_GPa": "9.0"},
         {"id": "lose_both", "elastic_pugh_GoverB": "0.0", "elastic_G_hill_GPa": "1.0"},
         {"id": "tradeoff_a", "elastic_pugh_GoverB": "-2.0", "elastic_G_hill_GPa": "1.0"},
         # ⚠ wad 를 10 으로 둔다 — 9 면 win_both(-1.0, 9.0) 에게 **지배당해서**
         #   "둘 다 남는다" 를 시험하지 못한다 (fixture 를 한 번 그렇게 짰다)
         {"id": "tradeoff_b", "elastic_pugh_GoverB": "0.0", "elastic_G_hill_GPa": "10.0"},
         {"id": "missing", "elastic_pugh_GoverB": "-9.0", "elastic_G_hill_GPa": ""}]
    fr, sc, _ax = pareto(R, axes=A, min_axes=2)
    ids = {r["id"] for r in fr}
    say("lose_both" not in ids, "[Pareto] 전 축에서 지는 점은 빠진다")
    say({"tradeoff_a", "tradeoff_b"} <= ids,
        "[Pareto] 서로 다른 축에서 이기는 둘은 **둘 다** 남는다 (가중합이 지우는 충돌)")
    say("missing" not in ids and len(sc) == 4,
        "[Pareto·음성] **축이 빈 행은 front 에 안 넣는다** — 넣으면 결측이 front 를 채운다")
    say("win_both" in ids, "[Pareto] 전 축에서 이기는 점은 남는다")
    #   방향 뒤집기: 낮을수록 좋은 축을 안 뒤집으면 tradeoff_a 가 지배당해 사라진다
    fr2, _s, _a = pareto([r for r in R if r["id"] in ("tradeoff_a", "win_both")],
                         axes=A, min_axes=2)
    say(len({r["id"] for r in fr2}) == 2,
        "[Pareto·방향] '낮을수록 좋다' 축의 부호를 뒤집는다 (안 뒤집으면 하나가 사라진다)")
    #   ★★ 실측회귀 (2026-08-28): 절대값 축을 부호 그대로 쓰면 **부피가 크게 줄어든 후보가
    #      이긴다.** analyse() 는 지키던 규칙을 pareto() 가 안 지켜서 실제로 그렇게 나왔다.
    AV = [("screen_dV_over_V0", "|ΔV/V0|", False)]
    RV = [{"id": "small_shrink", "screen_dV_over_V0": "-0.05"},
          {"id": "huge_shrink", "screen_dV_over_V0": "-0.30"}]
    frv, _s, _a = pareto(RV, axes=AV, min_axes=1, allow_invalid=True)
    say({r["id"] for r in frv} == {"small_shrink"},
        "[Pareto·실측회귀] |ΔV/V0| 는 **절대값**으로 읽는다 — 33 % 수축이 5 % 를 못 이긴다")
    #   파생 축은 기본 축 집합에서 빠진다 (같은 방향에 가중치 두 번 금지)
    _f3, _s3, ax3 = pareto([], axes=None)
    say(all(k != "li_mobility_score" for k, _l, _h in ax3),
        "[Pareto] 파생 축(li_mobility_score)은 기본 축에서 뺀다")

    # ★★★ 무효 축 거부 (2026-08-28, 리뷰 K) — 9일 전 판정을 도구가 대신 기억한다 ★★★
    say(all(k not in INVALID_AXES for k, _l, _h in ax3),
        f"[무효축·양성] 기본 축 집합에 무효 축이 없다 ({sorted(INVALID_AXES)})")
    _keep, _drop = valid_axes(AXES)
    _in_axes = {k for k, _l, _h in AXES} & set(INVALID_AXES)
    say({k for k, _w in _drop} == _in_axes,
        f"[무효축] AXES 안의 무효 축 {len(_drop)}개를 **사유와 함께** 걷어낸다 "
        f"(INVALID_AXES 에는 {len(INVALID_AXES)}개 — 나머지는 AXES 에 없는 방어용)")
    say(all(w.strip() for _k, w in _drop), "[무효축] 사유가 빈 항목이 없다")
    # 음성: 무효 축만 주면 front 를 만들지 않고 **빈손으로** 돌려준다 (조용히 통과 금지)
    _fi, _si, _ai = pareto(RV, axes=AV, min_axes=1)
    say(_fi == [] and _ai == [],
        "[무효축·음성] 무효 축만 주면 **front 를 안 만든다** (예전엔 그대로 돌았다)")
    say(pareto(RV, axes=AV, min_axes=1, allow_invalid=True)[2] != [],
        "[무효축] --allow_invalid_axes 로는 강제 통과된다 (진단용 경로가 살아 있다)")

    # ★★★ 행 → 설계 묶기 (리뷰 K) — 3,615 는 설계 수가 아니다 ★★★
    AG = [("screen_de_per_atom", "ΔE", False), ("elastic_G_hill_GPa", "G", True)]
    RG = [{"composition_Mg": "1", "composition_O": "1", "cation_site": "Li_24g",
           "anion_site": "S_16e", "charge_compensation": "cs",
           "screen_de_per_atom": v, "elastic_G_hill_GPa": g}
          for v, g in (("0.10", "10"), ("0.20", "12"), ("0.30", "14"))]
    RG.append({"composition_Mg": "2", "composition_O": "1", "cation_site": "Li_24g",
               "anion_site": "S_16e", "charge_compensation": "cs",
               "screen_de_per_atom": "0.50", "elastic_G_hill_GPa": "9"})
    dz, gi = aggregate_designs(RG, AG)
    say(gi["n_rows"] == 4 and gi["n_designs"] == 2,
        f"[묶기·양성] 같은 조성 3행이 **설계 1개**로 접힌다 (4행 → {gi['n_designs']}설계)")
    big = [d for d in dz if d["n_replicates"] == 3][0]
    say(abs(big["screen_de_per_atom"] - 0.20) < 1e-9,
        f"[묶기] 복제본은 **중앙값**으로 접는다 ({big['screen_de_per_atom']})")
    say(abs(big["screen_de_per_atom__spread"] - 0.20) < 1e-9,
        f"[묶기] 산포(max−min)를 같이 남긴다 ({big['screen_de_per_atom__spread']})")
    # 음성: 조성이 다르면 **묶이면 안 된다** (묶는 도구는 다 묶어도 통과할 수 있다)
    say(len({d["n_replicates"] for d in dz}) == 2 and
        sorted(d["n_replicates"] for d in dz) == [1, 3],
        "[묶기·음성] 조성이 다른 행은 안 묶인다 (3+1 이지 4 가 아니다)")
    # 음성: 자리만 달라도 다른 설계다
    RS = [dict(RG[0]), dict(RG[0])]
    RS[1]["anion_site"] = "S_4a"
    _ds, gs = aggregate_designs(RS, AG)
    say(gs["n_designs"] == 2, "[묶기·음성] 조성이 같아도 **자리가 다르면** 다른 설계다")

    # ★★★ 2026-08-28 결정: 절대 σ 는 축이 될 수 없다 (CLAUDE.md 인용금지) ★★★
    say("sigma_300K_S_cm_NE" in INVALID_AXES and "sigma_md_D_300K_cm2s" in INVALID_AXES,
        "[결정] 절대 σ·D 는 무효 축이다 — 우리가 인용 금지한 값을 축으로 안 쓴다")
    say("wad_J_m2_mean" in INVALID_AXES,
        "[결정] W_ad 는 **미교정**이라 보류다 (45–225 vs 실험 0.2–0.4)")
    say(any(k == "D_rel_vs_host" for k, _l, _h in AXES),
        "[결정] 대체 축 `D_rel_vs_host` 가 AXES 에 있다")
    _dr = [a for a in AXES if a[0] == "D_rel_vs_host"][0]
    say(_dr[2] is True, "[결정] D비는 클수록 좋다")
    say(0.5 < D_REL_GATE < 1.0,
        f"[결정] 게이트가 (0,1) 안이다 ({D_REL_GATE}) — host 대비 비이므로")
    # 음성: 절대 σ 를 축으로 주면 **거부해야** 한다
    _fs, _ss, _as = pareto([{"sigma_300K_S_cm_NE": "1e-3"}, {"sigma_300K_S_cm_NE": "2e-3"}],
                           axes=[("sigma_300K_S_cm_NE", "σ", True)], min_axes=1)
    say(_as == [], "[결정·음성] 절대 σ 만 주면 front 를 안 만든다")

    # ★★★ 빈 축 (2026-08-28 실측) — σ·W_ad 가 3,615행 **전부** 비어 있었다 ★★★
    AF = [("elastic_G_hill_GPa", "G", True), ("sigma_300K_S_cm_NE", "σ", True)]
    RF = [{"elastic_G_hill_GPa": "10", "sigma_300K_S_cm_NE": ""},
          {"elastic_G_hill_GPa": "20", "sigma_300K_S_cm_NE": ""}]
    ff = axis_fill(RF, AF)
    say(ff["elastic_G_hill_GPa"] == 2 and ff["sigma_300K_S_cm_NE"] == 0,
        f"[빈축·양성] 축별 채움을 센다 ({ff})")
    # 음성: 빈 축을 그대로 두면 front 가 **0개**가 된다 — 그래서 빼야 한다는 근거
    _fe, _se, _ae = pareto(RF, axes=AF, min_axes=2)
    say(len(_se) == 0,
        "[빈축·음성·실측회귀] 빈 축을 두면 채점 가능 행이 0 이 된다 (σ·W_ad 가 실제로 그랬다)")
    _fk, _sk, _ak = pareto(RF, axes=AF[:1], min_axes=1)
    say(len(_sk) == 2, "[빈축] 빈 축을 빼면 나머지 축으로 정상 채점된다")

    # ★★★ 사전등록 (2026-08-28, tu2026 에서 이전) — prospective 의 준비 ★★★
    DS = [{"name": "a", "li_mobility_score": "1.2"},
          {"name": "b", "li_mobility_score": "0.5"},
          {"name": "c", "li_mobility_score": ""}]
    TG = [{"name": "a", "dopant": "A"}, {"name": "b", "dopant": "B"},
          {"name": "c", "dopant": "C"}, {"name": "zz", "dopant": "Z"}]
    pr = preregister(DS, TG)
    say([r["name"] for r in pr["ranking"]] == ["a", "b"],
        f"[사전등록] 값이 큰 순으로 얼린다 ({[r['name'] for r in pr['ranking']]})")
    say(pr["ranking"][0]["predicted_rank"] == 1, "[사전등록] 순위가 1부터 매겨진다")
    # 음성 ①: 값이 없는 설계를 **조용히 빼지 않는다** — 뺀 걸 적어야 사후에 셈이 맞는다
    say(sorted(pr["unscored"]) == ["c", "zz"],
        f"[사전등록·음성] 채점 불가를 **기록**한다 ({pr['unscored']}) — 조용히 빠지면 "
        f"나중에 '39개 중 몇 개' 가 안 맞는다")
    # 음성 ②: 성공 기준이 **지금** 박혀 있어야 한다. 없으면 사후에 만들 수 있다.
    k = pr.get("성공기준_사전확정") or {}
    say(all(x in k for x in ("1_주기준", "2_보조", "3_실패로_읽는_경우")),
        "[사전등록·음성] 성공·실패 기준이 **측정 전에** 박혀 있다")
    say("3_실패로_읽는_경우" in k and "예측하지 못한다" in k["3_실패로_읽는_경우"],
        "[사전등록] **실패 조건**도 적는다 — 성공 조건만 적으면 사후해석이 열린다")
    say(pr.get("frozen_at") and pr.get("predictor") == "li_mobility_score",
        "[사전등록] 언제·무엇으로 얼렸는지 남는다")

    # ── 재평가 안정성 (2026-08-30) — **음성 경로가 핵심**이다 ──────────────────
    say(replicate_label("Ag2O_x050_cLi24gaS4a_s03") == "x050", "[안정성] x 라벨을 뽑는다")
    say(seed_label("Ag2O_x050_cLi24gaS4a_s03") == "s03", "[안정성] 시드 조각을 뽑는다")
    say(replicate_label("LaF3_s00") is None,
        "[안정성·음성] x 라벨이 없으면 None (아무 조각이나 x 로 읽지 않는다)")
    say(seed_label("Ag2O_x050_cLi24ga") is None,
        "[안정성·음성] 끝이 sNN 이 아니면 None")

    def _mk(i, x, s, bvs, g, pu, mvf, de="-1.0"):
        return {"name": f"D{i}_{x}_site_{s}", "composition_A": str(i),
                "cation_site": "c", "anion_site": "a", "charge_compensation": "cc",
                "bvs_li_proxy_score": str(bvs), "elastic_G_hill_GPa": str(g),
                "elastic_pugh_GoverB": str(pu), "migration_volume_fraction": str(mvf),
                "screen_de_per_atom": de}
    SAX = [("bvs_li_proxy_score", "BVS", True), ("elastic_G_hill_GPa", "G", True),
           ("elastic_pugh_GoverB", "Pugh", False),
           ("migration_volume_fraction", "MVF", True)]
    # ⓐ [양성] 세 재평가가 **완전히 같으면** ρ=1 · front Jaccard=1
    R = []
    for i in range(40):
        for x in X_LABELS:
            R.append(_mk(i, x, "s00", 0.5 + i / 100, 10 + i, 0.6 + i / 200, 0.1 + i / 500))
    st1 = stability(R, axes=SAX)
    say(st1["info"]["n_triplets"] == 40, f"[안정성] 삼중쌍 40개 ({st1['info']['n_triplets']})")
    say(all(abs(v["mean"] - 1.0) < 1e-9 for v in st1["retest"].values()),
        "ⓐ 재평가가 같으면 모든 축 ρ=1")
    say(all(j == 1.0 for j in st1["jaccard"].values()), "ⓐ front 도 완전히 같다 (Jaccard 1)")
    # ⓑ [음성] 재평가가 **뒤집히면** ρ<0 이어야 한다 — '안정' 으로 읽으면 안 된다
    R2 = []
    for i in range(40):
        R2.append(_mk(i, "x020", "s00", 0.5 + i / 100, 10 + i, 0.6, 0.1))
        R2.append(_mk(i, "x050", "s00", 0.5 + i / 100, 10 + i, 0.6, 0.1))
        R2.append(_mk(i, "x100", "s00", 0.5 + (39 - i) / 100, 10 + i, 0.6, 0.1))
    st2 = stability(R2, axes=SAX)
    say(st2["retest"]["bvs_li_proxy_score"]["mean"] < 0.4,
        f"ⓑ [음성] 한 재평가가 역순이면 평균 ρ 가 내려간다 "
        f"({st2['retest']['bvs_li_proxy_score']['mean']:+.3f})")
    say(any(r < -0.9 for r in st2["retest"]["bvs_li_proxy_score"]["pairs"]),
        "ⓑ [음성] 역순 쌍이 ρ≈−1 로 **그대로 보인다** (평균에 숨지 않는다)")
    # ⓒ [음성] 시드가 섞인 삼중쌍은 '재측정' 이 아니다 → 세지 않는다
    R3 = []
    for i in range(40):
        R3.append(_mk(i, "x020", "s00", 0.5, 10, 0.6, 0.1))
        R3.append(_mk(i, "x050", "s00", 0.5, 10, 0.6, 0.1))
        R3.append(_mk(i, "x100", "s01", 0.5, 10, 0.6, 0.1))   # ← 다른 시드
    st3 = stability(R3, axes=SAX)
    say(st3["info"]["n_triplets"] == 0 and st3["info"]["n_mixed_seed"] == 40,
        f"ⓒ [음성] 시드가 섞이면 삼중쌍이 아니다 "
        f"(삼중쌍 {st3['info']['n_triplets']} · 시드섞임 {st3['info']['n_mixed_seed']})")
    # ⓓ [음성] 에너지가 다르면 '같은 구조' 전제가 깨진다 → strict 에서 제외
    R4 = []
    for i in range(40):
        R4.append(_mk(i, "x020", "s00", 0.5, 10, 0.6, 0.1, de="-1.000000"))
        R4.append(_mk(i, "x050", "s00", 0.5, 10, 0.6, 0.1, de="-1.000001"))
        R4.append(_mk(i, "x100", "s00", 0.5, 10, 0.6, 0.1, de="-1.500000"))  # ← 딴 구조
    say(stability(R4, axes=SAX)["info"]["n_triplets"] == 0,
        "ⓓ [음성] 에너지가 어긋난 삼중쌍은 strict 에서 빠진다")
    say(stability(R4, axes=SAX, strict=False)["info"]["n_triplets"] == 40,
        "ⓓ --loose_identity 로는 들어온다 (진단용 — 구조 동일 물증 없음)")
    # ⓔ [음성] 삼중쌍이 MIN_N 미만이면 **판정하지 않는다** (없는 판정력을 쓰지 않는다)
    say(stability(R[:3 * (MIN_N - 1)], axes=SAX)["retest"] == {},
        f"ⓔ [음성] 삼중쌍 {MIN_N} 미만이면 축별 ρ 를 내지 않는다")
    # ⓕ [음성] **빈 축을 need 에 넣으면 삼중쌍이 0** — 실제로 2026-08-30 에 그렇게 됐다
    SAX_EMPTY = SAX + [("D_rel_vs_host", "D비", True)]
    say(stability(R, axes=SAX_EMPTY)["info"]["n_triplets"] == 40,
        "ⓕ [음성] 한 줄도 없는 축은 자동으로 빠진다 (안 빼면 삼중쌍이 0 이 된다)")

    print("  " + ("✅ selftest 통과" if ok else "⛔ selftest 실패"))
    return 0 if ok else 1


def pareto(rows, axes=None, min_axes=3, allow_invalid=False):
    """정본 CSV 의 **비지배 집합**. 가중합이 지우는 축 충돌을 그대로 남긴다.

    ⛔ 못 하는 것 (analyze_screening.pareto_front 와 같은 한계 + CSV 특유의 것)
      · **순위가 아니다.** Pareto 는 집합이고, 그 안에서 무엇을 고를지는 사람이 정한다.
      · **결측 행은 front 에 안 넣는다.** 축이 비어 있는 행을 넣으면 "아무 축에서도 지지
        않는다" 가 되어 front 가 결측 행으로 채워진다 — 정확히 반대 결과다.
        우리 CSV 는 축 대부분이 18.8 % 밖에 안 차 있어서 이 함정이 크다.
      · 그래서 **어느 축 집합으로 쟀는지와 표본 수를 같이 낸다.** 그게 없으면
        "3,615개 중 47개가 front" 라는 문장이 3,615 를 대표하는 것처럼 읽힌다.
      · 파생 축(li_mobility_score)은 기본 축 집합에서 뺀다 — 재료 축과 같이 넣으면
        그 방향에 **가중치를 두 번** 주는 셈이다.
    """
    ax = axes or [(k, lab, hi) for k, lab, hi in AXES
                  if k not in DERIVED and k != "li_mobility_score"]
    ax, _dropped = valid_axes(ax, allow_invalid)
    if not ax:
        return [], [], []
    pts, keep = [], []
    for r in rows:
        v = [axis_value(k, _f(r.get(k))) for k, _l, _h in ax]
        if sum(x is not None for x in v) < min_axes or any(x is None for x in v):
            continue
        # 전부 "클수록 좋다" 로 방향을 맞춘다 (낮을수록 좋은 축은 부호를 뒤집는다)
        keep.append(r)
        pts.append([(x if hi else -x) for x, (_k, _l, hi) in zip(v, ax)])
    front = []
    for i, p_ in enumerate(pts):
        dominated = any(
            i != j and all(q >= p_[k] for k, q in enumerate(qq)) and any(q > p_[k] for k, q in enumerate(qq))
            for j, qq in enumerate(pts))
        if not dominated:
            front.append(keep[i])
    return front, keep, ax


def print_pareto(front, scored, ax, total):
    print("\n" + "=" * 78)
    print("■ Pareto 비지배 집합 (가중합이 지우는 축 충돌을 남긴다)")
    print(f"   축 {len(ax)}개: " + " · ".join(l for _k, l, _h in ax))
    print(f"   ⚠ **{total}행 중 이 축들이 다 찬 행은 {len(scored)}개** "
          f"({100*len(scored)/max(total,1):.1f} %) — front 는 그 안에서만 뜻이 있다.")
    if not scored:
        print("   ⛔ 채점 가능한 행이 없다 — 축이 비어 있다.")
        return
    print(f"   front **{len(front)}개** ({100*len(front)/len(scored):.1f} % of {len(scored)})")
    key = next((k for k in ("cascade_id", "id", "dopant", "formula") if k in front[0]), None)
    for r in front[:25]:
        who = r.get(key, "?") if key else "?"
        vals = " ".join(
            (f"{l}={axis_value(k, _f(r.get(k))):.3g}"
             if _f(r.get(k)) is not None else f"{l}=—") for k, l, _h in ax)
        print(f"     {str(who)[:28]:28} {vals}")
    if len(front) > 25:
        print(f"     … 외 {len(front)-25}개")


    print("   ⛔ 이건 **집합이지 순위가 아니다.** front 안의 선택은 사람이 한다.")


# ── 재평가 안정성 (2026-08-30) ────────────────────────────────────────────────
#: 같은 설계 안에서 **동일 구조를 다시 잰** 복제본을 가르는 이름 조각.
#:   2026-08-28 판정: `n_units = max(1, round(n_fu×x)) = 1` 이라 x020/x050/x100 은
#:   **같은 조성의 다른 이름**이다 (concentration 열이 3,615행 전부 0.25).
#:   시드 s00–s04 는 도판트 **배치**가 달라지지만 x 라벨은 그렇지 않다.
#:   ⇒ 한 시드 안의 x 세 개는 다른 설계가 아니라 **같은 구조의 재측정**이고,
#:      그 셋이 얼마나 갈리는지가 곧 그 축의 **재평가 잡음**이다.
X_LABELS = ("x020", "x050", "x100")

#: 구조 동일성의 물증으로 쓰는 축 — 같은 구조면 에너지는 같은 값이 나와야 한다.
#:   ⚠ 이 축은 `INVALID_AXES` 다 (2026-08-19: 기준이 미수렴이라 **절대값 인용 금지**).
#:     여기서는 값을 인용하지 않고 **같은 구조가 같은 숫자를 주는지**만 본다 — 자기일치
#:     검사라서 기준의 수렴 여부와 무관하다. 채점 축으로는 절대 쓰지 않는다.
IDENTITY_PROBE = "screen_de_per_atom"
#: 이 상대편차 안이면 '같은 구조' 로 본다 (실측 중앙값은 1e-4 급).
IDENTITY_TOL = 1e-4


def replicate_label(name):
    """이름에서 가짜 x 라벨을 뽑는다 (`Ag2O_x050_cLi24gaS4a_s03` → `x050`). 없으면 None."""
    for p in str(name).split("_"):
        if p.startswith("x") and p[1:].isdigit():
            return p
    return None


def seed_label(name):
    """이름 끝의 시드 조각 (`..._s03` → `s03`). 없으면 None."""
    tail = str(name).rsplit("_", 1)[-1]
    return tail if tail[:1] == "s" and tail[1:].isdigit() else None


def retest_triplets(rows, need, strict=True):
    """**같은 구조를 세 번 잰** 삼중쌍만 고른다. → (triplets, info)

    triplets 는 [{x라벨: 행}] 이고, 각 삼중쌍은 세 조건을 다 만족한다:
      ① 같은 설계 (design_key — 조성 + 자리 + 전하보상)
      ② **같은 시드** — 시드가 섞이면 배치가 달라져 '재측정' 이 아니다
      ③ `need` 축이 세 행 모두 차 있다
    `strict` 면 ④ `IDENTITY_PROBE` 가 세 행에서 `IDENTITY_TOL` 안 — 즉 에너지가
    같은 값이라 **정말 같은 이완 구조**라는 물증이 있는 것만 남긴다.

    ⛔ 이 함수가 못 하는 것
      · 원자 매핑 해시를 보지 않는다. 구조 동일성은 **에너지 일치라는 정황**이지 증명이 아니다.
      · 시드끼리는 비교하지 않는다 (s00 vs s01 은 배치가 달라 재측정이 아니다).
      · 삼중쌍이 안 되는 설계를 '일치' 로 세지 않는다 — 그냥 뺀다 (분모에서도 뺀다).
    """
    comp_cols = [c for c in (rows[0] if rows else {}) if c.startswith("composition_")]
    g = {}
    for r in rows:
        g.setdefault(design_key(r, comp_cols), []).append(r)
    trip, n_mixed_seed, n_partial, n_not_identical = [], 0, 0, 0
    for _k, rs in g.items():
        got = [r for r in rs if all(_f(r.get(c)) is not None for c in need)]
        by = {}
        for r in got:
            x, s = replicate_label(r.get("name", "")), seed_label(r.get("name", ""))
            by.setdefault(s, {})[x] = r
        full = [d for d in by.values() if set(d) == set(X_LABELS)]
        if not full:
            if got:
                if len(got) >= len(X_LABELS):
                    n_mixed_seed += 1
                else:
                    n_partial += 1
            continue
        d = full[0]
        if strict:
            v = [_f(d[x].get(IDENTITY_PROBE)) for x in X_LABELS]
            if any(t is None for t in v) or _mean(v) == 0 or \
               (max(v) - min(v)) / abs(_mean(v)) > IDENTITY_TOL:
                n_not_identical += 1
                continue
        trip.append(d)
    return trip, {"n_designs": len(g), "n_triplets": len(trip),
                  "n_mixed_seed": n_mixed_seed, "n_partial": n_partial,
                  "n_not_identical": n_not_identical, "strict": strict}


def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def stability(rows, axes=None, strict=True):
    """재평가 안정성 — **같은 구조를 세 번 잰 값이 같은 순위를 주는가.** → dict

    왜 (2026-08-30): Pareto front 39설계와 사전등록 순위가 이 축들 위에 서 있는데,
    그 축들이 자기 자신을 재현하는지는 **한 번도 안 쟀다.** 재현 못 하는 예측기로
    사전등록 `|ρ| ≥ 0.35` 를 시험하면 실패 가지(|ρ| < 0.2 ⇒ '이동도 축 근거 소멸')가
    물리가 아니라 잡음으로 켜진다.

    ⛔ 못 하는 것
      · **어느 축이 옳은지 말하지 않는다.** 재현성이 낮다 ≠ 값이 틀렸다.
      · 잡음의 **원인**을 말하지 않는다 (후처리 RNG · 이완 경로 · 파싱 — 못 가른다).
      · 시드 간(배치) 변동은 안 본다 — 그건 다른 질문이다.
    """
    ax = axes or [(k, lab, hi) for k, lab, hi in AXES
                  if k not in DERIVED and k != "li_mobility_score"]
    ax, _dropped = valid_axes(ax, False)
    # ⛔ 2026-08-30 — **빈 축을 남기면 삼중쌍이 0 이 된다.** `D_rel_vs_host` 는 아직
    #   한 줄도 없어서(측정 전이다) `need` 에 넣으면 모든 설계가 탈락한다.
    #   main() 의 Pareto 경로가 이미 같은 함정을 막고 있었는데 여기서 또 갈릴 뻔했다.
    fill = axis_fill(rows, ax)
    ax = [a for a in ax if fill[a[0]] > 0]
    need = [k for k, _l, _h in ax]
    trip, info = retest_triplets(rows, need, strict=strict)
    info["dropped_empty"] = [k for k, _l, _h in (axes or []) or [] if fill.get(k) == 0]
    out = {"info": info, "axes": [(k, l) for k, l, _h in ax], "retest": {}, "front": {}}
    if len(trip) < MIN_N:
        return out
    for k, lab, _hi in ax + [("li_mobility_score", "Li 이동도(합성)", True)]:
        vals = {x: [_f(d[x].get(k)) for d in trip] for x in X_LABELS}
        if any(v is None for xs in vals.values() for v in xs):
            continue
        rr = [spearman(vals[a], vals[b]) for a, b in
              (("x020", "x050"), ("x020", "x100"), ("x050", "x100"))]
        rr = [r for r in rr if r is not None]
        out["retest"][k] = {"label": lab, "pairs": rr,
                            "mean": (sum(rr) / len(rr)) if rr else None}
    fronts = {}
    for x in X_LABELS:
        fr, sc, _a = pareto([d[x] for d in trip], axes=ax)
        fronts[x] = {i for i, d in enumerate(trip) if d[x] in fr}
        out["front"][x] = len(fronts[x])
    med = []
    for i, d in enumerate(trip):
        base = dict(d["x020"])
        for k, _l, _h in ax:
            base[k] = _median([_f(d[x].get(k)) for x in X_LABELS])
        med.append(base)
    fr, _sc, _a = pareto(med, axes=ax)
    fronts["median"] = {i for i, r in enumerate(med) if r in fr}
    out["front"]["median"] = len(fronts["median"])
    out["jaccard"] = {}
    for a, b in (("x020", "x050"), ("x020", "x100"), ("x050", "x100"),
                 ("median", "x020"), ("median", "x050"), ("median", "x100")):
        u = fronts[a] | fronts[b]
        out["jaccard"][f"{a}|{b}"] = (len(fronts[a] & fronts[b]) / len(u)) if u else None
    return out


def print_stability(s):
    i = s["info"]
    print("\n" + "=" * 78)
    print("■ 재평가 안정성 — **같은 구조를 세 번 잰 값이 같은 순위를 주나**")
    print(f"   삼중쌍 **{i['n_triplets']}개** / {i['n_designs']}설계 "
          f"(같은 시드 안의 x020·x050·x100"
          + (f" · {IDENTITY_PROBE} 일치 {IDENTITY_TOL:g} 이내" if i["strict"] else "") + ")")
    print(f"   제외: 시드 섞임 {i['n_mixed_seed']} · 축 결측 {i['n_partial']} · "
          f"에너지 불일치 {i['n_not_identical']}")
    if not s["retest"]:
        print(f"   ⛔ 삼중쌍이 {MIN_N}개 미만이거나 축이 비어 판정하지 않는다.")
        return
    print("\n   축별 재검사 상관 (ρ=1 이면 완전 재현):")
    for k, v in s["retest"].items():
        mark = "🔴" if v["mean"] is not None and abs(v["mean"]) < 0.5 else "  "
        print(f"     {mark} {v['label'][:14]:14} ρ = "
              + " / ".join(f"{r:+.3f}" for r in v["pairs"])
              + f"   평균 **{v['mean']:+.3f}**")
    print("\n   같은 설계 집합에서 **재평가마다 다시 뽑은 Pareto front**:")
    print("     크기: " + " · ".join(f"{k} {v}" for k, v in s["front"].items()))
    print("     겹침(Jaccard): " + " · ".join(
        f"{k} {v:.2f}" for k, v in s["jaccard"].items() if v is not None))
    print("\n   ⛔ 이 표는 **어느 값이 옳은지 말하지 않는다.** 축이 자기 자신을 얼마나"
          "\n      재현하는지만 잰다 — 그게 낮으면 그 축으로 세운 순위·front·사전등록의"
          "\n      판정력이 그만큼 깎인다 (감쇠 상한 = √(재검사 신뢰도)).")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", default=DEFAULT_CSV)
    ap.add_argument("--min_n", type=int, default=MIN_N)
    ap.add_argument("--pareto", action="store_true",
                    help="비지배 집합도 낸다 (A3). 축이 다 찬 행에서만 — 결측 행은 뺀다")
    ap.add_argument("--axes", default=None,
                    help="Pareto 축을 직접 고른다 (쉼표 구분 열이름). 기본은 파생·무효 축을 뺀 전부")
    ap.add_argument("--no_group", action="store_true",
                    help="⛔ 행을 **설계로 묶지 않고** 그대로 쓴다. 표본이 15배 부풀려진다 "
                         "— 진단 목적일 때만")
    ap.add_argument("--stability", action="store_true",
                    help="**같은 구조를 세 번 잰** 값이 같은 순위를 주는지 본다 "
                         "(재검사 상관 + front 재추출). 새 계산 0 — 있는 CSV 만 읽는다")
    ap.add_argument("--loose_identity", action="store_true",
                    help="--stability 에서 에너지 일치 조건을 끈다 "
                         "(구조 동일 물증 없이 삼중쌍을 쓴다 — 진단용)")
    ap.add_argument("--allow_invalid_axes", action="store_true",
                    help="⛔ 무효 판정된 축을 강제로 넣는다 (2026-08-19 판정을 무시)")
    ap.add_argument("--preregister", default=None, metavar="TARGETS_JSON",
                    help="측정 전 예측을 얼려 기록한다 (prospective 검증의 준비). "
                         "인자는 대상 목록 JSON (db/properties/d_rel_targets_*.json)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not os.path.isfile(a.csv):
        print(f"⛔ 없다: {a.csv}")
        return 2
    rows = load(a.csv)
    if a.stability:
        print_stability(stability(rows, strict=not a.loose_identity))
        import hashlib
        with open(a.csv, "rb") as f:
            print(f"\n[provenance] csv={os.path.basename(a.csv)} "
                  f"sha256:{hashlib.sha256(f.read()).hexdigest()[:16]} "
                  f"strict_identity={not a.loose_identity}")
        return 0
    if a.preregister:
        import hashlib
        import json as _json
        tj = _json.load(open(a.preregister, encoding="utf-8"))
        designs, _gi = aggregate_designs(rows, AXES)
        pre = preregister(designs, tj.get("targets") or [])
        with open(a.csv, "rb") as f:
            pre["source_csv_sha256"] = hashlib.sha256(f.read()).hexdigest()
        pre["targets_file"] = os.path.basename(a.preregister)
        out = os.path.join(ROOT, "db", "properties",
                           "prereg_d_rel_" + _dt.date.today().strftime("%Y_%m_%d") + ".json")
        with open(out, "w", encoding="utf-8") as f:
            _json.dump(pre, f, ensure_ascii=False, indent=2)
        print(f"■ 사전등록 — 라벨이 **아직 없는** {pre['n_scored']}설계 순위를 얼렸다")
        print(f"   예측기 {pre['predictor']} · 채점 불가 {len(pre['unscored'])}개")
        for r in pre["ranking"][:8]:
            print(f"     {r['predicted_rank']:2}. {str(r['dopant'])[:16]:16} "
                  f"{pre['predictor']}={r[pre['predictor']]:.4f}")
        print(f"   … 하위 3: " + " · ".join(
            f"{r['predicted_rank']}.{r['dopant']}" for r in pre["ranking"][-3:]))
        print(f"   ⛔ 성공기준을 **지금** 못박았다 — 측정 뒤에 고치면 의미가 사라진다")
        print(f"   저장: {out}")
        return 0
    # ⛔ 2026-08-28 (리뷰 K) — 상관도 **설계 단위**로 봐야 한다. 행 단위로 보면 n=681 인데
    #   그중 독립인 것은 227뿐이라(복제본 3배) 유의성이 3배 부풀려진다. ρ 자체는 거의
    #   안 변하지만 n 은 변하고, 우리가 인용하는 건 둘 다다.
    if a.no_group:
        corr_rows, ginfo = rows, {"n_rows": len(rows), "n_designs": len(rows), "comp_cols": 0,
                                  "replicates_per_design": [1]}
    else:
        corr_rows, ginfo = aggregate_designs(rows, AXES)
        print(f"■ 행 → 설계 묶기: **{ginfo['n_rows']}행 → {ginfo['n_designs']}설계** "
              f"(조성 {ginfo['comp_cols']}열 + 자리 + 전하보상)")
        print(f"   설계당 복제본 {ginfo['replicates_per_design']}개 — 가짜 x 라벨"
              f"(x020/050/100 이 전부 실제 0.25) × 시드 s00–s04\n")
    report(analyse(corr_rows, a.min_n))
    if a.pareto:
        # ---- 축 선택 ----
        if a.axes:
            want = [w.strip() for w in a.axes.split(",") if w.strip()]
            known = {k: (k, lab, hi) for k, lab, hi in AXES}
            unknown = [w for w in want if w not in known]
            if unknown:
                print(f"⛔ 모르는 축: {unknown}\n   가능: {sorted(known)}")
                return 2
            ax0 = [known[w] for w in want]
        else:
            ax0 = [(k, lab, hi) for k, lab, hi in AXES
                   if k not in DERIVED and k != "li_mobility_score"]
        ax0, dropped = valid_axes(ax0, a.allow_invalid_axes)
        if dropped:
            print("\n⛔ **무효 판정된 축을 뺐다** (2026-08-19):")
            for k, why in dropped:
                print(f"     · {k} — {why}")
            print("   (강제로 넣으려면 --allow_invalid_axes — 그럼 결과는 물리가 아니다)")
        if a.allow_invalid_axes:
            print("\n⛔⛔ `--allow_invalid_axes` — 무효 축이 들어간다. **인용 금지.**")
        if not ax0:
            print("⛔ 남은 축이 없다.")
            return 2
        # ---- 빈 축 걸러내기 (한 축이라도 비면 front 가 통째로 사라진다) ----
        use = corr_rows
        fill = axis_fill(use, ax0)
        empty = [(k, l) for k, l, _h in ax0 if fill[k] == 0]
        if empty:
            print("\n⛔ **데이터가 하나도 없는 축을 뺐다** — 두면 교집합이 0 이 되어 "
                  "front 가 통째로 사라진다:")
            for k, l in empty:
                print(f"     · {k} ({l}) — 0 / {len(use)}설계")
            ax0 = [a for a in ax0 if fill[a[0]] > 0]
        print("   축별 채움: " + " · ".join(
            f"{l} {fill[k]}({100*fill[k]/max(len(use),1):.0f}%)" for k, l, _h in ax0))
        if len(ax0) < 2:
            print(f"⛔ 쓸 수 있는 축이 {len(ax0)}개다 — Pareto 는 2축부터다.")
            return 2
        if a.no_group:
            print(f"\n⛔ `--no_group` — {len(use)}행을 그대로 쓴다. "
                  f"**표본이 부풀려져 있다** (복제본을 독립 설계로 센다).")
        fr, sc, ax = pareto(use, axes=ax0, allow_invalid=a.allow_invalid_axes)
        print_pareto(fr, sc, ax, len(use))
        # ---- provenance ----
        import hashlib
        with open(a.csv, "rb") as f:
            sha = hashlib.sha256(f.read()).hexdigest()[:16]
        print(f"\n[provenance] csv={os.path.basename(a.csv)} sha256:{sha} "
              f"rows={ginfo['n_rows']} designs={ginfo['n_designs']} "
              f"axes={[k for k, _l, _h in ax]} "
              f"grouped={not a.no_group} allow_invalid={a.allow_invalid_axes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
