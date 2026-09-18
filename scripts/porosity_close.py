#!/usr/bin/env python3
"""CLOSE the porosity regression on the DECLARED corpus.

Method: production-form gated target, LOOCV over the declared corpus, plus residual
ranking and regime classification as **diagnostics**.  The closed number is the one
the canon publishes: `docs/porosity_regression_final.md` (gated LOOCV, n=129).

⛔⛔ **2026-09-18 정정 (원장 `GAP3-18`) — 옛 판은 사후 래칫이었다.**
  옛 코드는 `if r2t > r2c + 0.002` 로 **보고 지표가 오를 때만** 케이스를 지웠다.
  제외 *채택* 조건이 보고 지표 자신이면 그렇게 나온 LOOCV 는 일반화 추정치가 아니다.
  ★ 실측이 그것을 못박는다 — 정당화 클래스(코너·SE-rich) **36건을 클래스로 빼면
    LOOCV 가 0.583 → 0.516 으로 내려간다**.  그런데 옛 판은 그 36건 중 지표를 올려 주는
    **한 건만** 골라 뺐다 (`input_1mAh_9_S1`, 0.583 → 0.603).  물성 기준이라면 36건이
    같이 나가야 한다.  한 건만 나간 것은 **기준이 물성이 아니었다**는 뜻이다.
  ⇒ 제외는 **선언으로만** 정한다 (`DECLARED_EXCLUSIONS`).  `close_corpus()` 는 지표를
    보지 않으며, `--selftest` 가 y 를 흔들어 그 불변성을 **실제로 단언**한다.

  ⚠ 옛 docstring 의 지시 *"maximise R2 on our data; … out-of-envelope CORNERS may be
    set as OUTLIERS"* 는 **폐기된 지시다**.  정본이 그 뒤의 결정을 적는다:
      · `:19`      "Outlier 제외 = **물성(영률 등)-다른 것만**"
      · `:219-220` "코너 포함이 R²를 올린다 … **제외 안 함**"
      · 사용자 지시 2026-06-30 — **"코너도 추가"**
    ⇒ 이 스크립트 **안**의 제외 집합은 비어 있다.  물성-다른 것(E 변종 · sub-µm SE ·
      particulate · S-series)은 **상류에서** 이미 빠진다: `load_pairs(exclude_particulate)`
      + `BROKEN`.  되살리지 말 것.
"""
import argparse
import math
import sys

import numpy as np

from porosity_physics_regression import features, FEAT_KEYS, loocv_r2, se_of_solid
from porosity_plastic_vs_rigid import load_pairs

GATE = 4.0
BROKEN = "1mAh_100"               # CLAUDE.md: plate_z metadata bug -> bad porosity

#  ★ 이 스크립트가 빼는 것 — **비어 있다** (위 정정 블록 참조).
#    여기에 이름을 넣는 것은 "지표를 보고 고른 것이 아니라 **먼저 선언한 것**" 일 때뿐이다.
#    코퍼스에 없는 이름을 넣으면 `close_corpus` 가 **거부한다** (조용히 안 빠지는 것을 막는다).
DECLARED_EXCLUSIONS: tuple = ()


def real_rAM(case):
    """actual AM radii (collection reconstructs 6/2; the 1mAh/8mAh series are 5/2.5)."""
    base = ("1mAh_", "8mAh_")
    if any(b in case for b in base) and "real" not in case:
        return 5.0, 2.5
    return 6.0, 2.0


def build_rows():
    """선언된 코퍼스를 만든다 — 상류 제외(particulate/S, BROKEN)까지가 전부다."""
    rows = load_pairs()                       # particulate/S already excluded
    rows = [r for r in rows if BROKEN not in r["case"]]   # drop broken-sim series
    for r in rows:
        g = r["dem"] - r["mpm"]
        r["best"] = r["dem"] if g > GATE else r["mpm"]
        r["gap"] = g
        r["ses"] = se_of_solid(r["amwt"])
        # (geometry-by-name fix tested -> HURT LOOCV 0.53->0.49, reverted; the reconstruct
        #  6/2 is a better average than guessing 5/2.5, so keep it.)
    return rows


def loo(rows):
    X = np.array([[features(r)[k] for k in FEAT_KEYS] for r in rows])
    y = np.array([r["best"] for r in rows])
    r2, pred = loocv_r2(X, y)
    return r2, pred, y


def classify(r):
    """이 케이스가 어느 레짐인지 — **진단 라벨이다.  제외 기준이 아니다.**

    ⚠ 옛 판은 이 라벨을 *"지워도 되는 후보"* 필터로 쓰고 실제 채택은 LOOCV 로 했다.
      라벨은 그대로 두되(진단으로 유용하다) 제외와의 배선을 끊었다.
    """
    if r["gap"] > GATE:                        return "mono/SE-poor CORNER (gated DEM, bracket)"
    elif 2.5 < r["gap"] <= GATE:               return "borderline corner (gap~4)"
    elif r["ses"] > 0.55:                      return "SE-rich (eps over-compress edge)"
    return "in-envelope"


def close_corpus(rows, declared=DECLARED_EXCLUSIONS):
    """제외 집합을 **선언만으로** 정한다 — 보고 지표를 보지 않는다.

    ★ 계약: 반환값은 각 행의 `best`(= 회귀 타깃 y)에 **의존하지 않는다**.
      `--selftest` 의 ① 이 y 를 흔들어 그것을 단언한다.  옛 래칫은 이 시험에서 죽는다.
    ⚠ 선언한 이름이 코퍼스에 없으면 **거부한다** — 조용히 안 빠지면 뺐다고 믿게 된다
      (거짓 초록).
    """
    have = {r["case"] for r in rows}
    missing = [c for c in declared if c not in have]
    if missing:
        raise SystemExit(f"⛔ 선언된 제외가 코퍼스에 없다: {missing}  "
                         f"— 이름이 틀렸거나 상류에서 이미 빠졌다.  둘 다 조용히 두지 않는다.")
    names = set(declared)
    keep = [r for r in rows if r["case"] not in names]
    excl = [(r["case"], classify(r)) for r in rows if r["case"] in names]
    return keep, excl


def report():
    rows = build_rows()
    print(f"FULL production corpus n={len(rows)}")
    r2, pred, y = loo(rows)
    print(f"  baseline gated LOOCV = {r2:.3f}  RMSE {math.sqrt(np.mean((y - pred) ** 2)):.2f}%p")

    for r, p, yy in zip(rows, pred, y):
        r["resid"] = yy - p
    ranked = sorted(rows, key=lambda r: -abs(r["resid"]))
    print("\nTop residual cases (진단 — 제외 후보가 **아니다**):")
    for r in ranked[:12]:
        print(f"  {r['case'][:26]:26s} resid {r['resid']:+5.1f}  gap {r['gap']:+4.1f}  "
              f"se {r['ses'] * 100:4.0f}%  -> {classify(r)}")

    keep, excl = close_corpus(rows)
    r2f, predf, yf = loo(keep)
    print(f"\nCLOSED form: n={len(keep)} (선언 제외 {len(excl)}건)")
    print(f"  LOOCV = {r2f:.3f}  RMSE {math.sqrt(np.mean((yf - predf) ** 2)):.2f}%p")
    if excl:
        print("  exclusion ledger (선언):")
        for c, why in excl:
            print(f"    - {c[:26]:26s} [{why}]")
    else:
        print("  exclusion ledger: 비어 있다 — 정본 :19 · :219-220 · 사용자 지시 2026-06-30")

    #  ★ 두 수를 **나란히** 적는다.  하나만 적으면 고르는 자리가 생긴다.
    inenv = [r for r in rows if classify(r) == "in-envelope"]
    r2i, *_ = loo(inenv)
    print(f"\n  reference: in-envelope-only (n={len(inenv)}) LOOCV = {r2i:.3f}")
    print(f"  ⇒ 코너를 클래스로 빼면 {r2:.3f} → {r2i:.3f} 로 **내려간다** "
          f"(정본 :219-220 이 적는 그대로) — 그래서 빼지 않는다.")
    return 0


# ══════════════════════════════════════════════════════════════════════
#  자기검사 — 옛 래칫을 재현해 죽인다 (원장 `GAP3-18`)
# ══════════════════════════════════════════════════════════════════════

def _selftest():
    ok = fail = 0

    def chk(name, cond, extra=""):
        nonlocal ok, fail
        if cond:
            ok += 1
        else:
            fail += 1
            print(f"  ✗ {name}   {extra}")

    def mk(case, gap, ses, best):
        return {"case": case, "gap": gap, "ses": ses, "best": best}

    #  코너 1 · SE-rich 1 · in-envelope 2
    base = [mk("corner_A", 9.0, 0.30, 20.0), mk("serich_B", -1.0, 0.70, 11.0),
            mk("clean_C", 0.0, 0.40, 15.0), mk("clean_D", 1.0, 0.45, 16.0)]

    #  ★① 지표 불변 — y 를 흔들어도 제외 집합이 **한 글자도** 안 바뀐다.
    #     옛 래칫은 여기서 죽는다: y 를 바꾸면 어느 케이스를 지울지가 바뀐다.
    shook = [dict(r, best=r["best"] * 3.0 + 7.0) for r in base]
    k1, e1 = close_corpus(base)
    k2, e2 = close_corpus(shook)
    chk("★① y(보고 지표)를 흔들어도 제외 집합이 같다",
        e1 == e2 and [r["case"] for r in k1] == [r["case"] for r in k2], f"{e1} vs {e2}")

    #  ★② 어떤 y 를 줘도 기본 선언에서는 아무도 안 빠진다 (정본 정합)
    chk("★② 기본 선언은 비어 있다 — 아무도 안 빠진다",
        e1 == [] and len(k1) == len(base), f"excl={e1}")
    chk("② 정본 정합: DECLARED_EXCLUSIONS 가 비어 있다",
        DECLARED_EXCLUSIONS == (), str(DECLARED_EXCLUSIONS))

    #  ③ 선언하면 실제로 빠진다 (기능이 죽은 것이 아니다)
    k3, e3 = close_corpus(base, declared=("corner_A",))
    chk("③ 선언한 것은 실제로 빠진다",
        len(k3) == 3 and [c for c, _ in e3] == ["corner_A"], f"{e3}")
    chk("③ 빠진 것의 라벨이 붙는다", e3 and "CORNER" in e3[0][1], str(e3))

    #  ★④ 코퍼스에 없는 이름은 **거부**한다 (조용히 안 빠지는 거짓 초록 차단)
    try:
        close_corpus(base, declared=("없는케이스",))
        chk("★④ 없는 이름을 거부한다", False, "거부하지 않았다")
    except SystemExit:
        chk("★④ 없는 이름을 거부한다", True)

    #  ⑤ 음성 대조 — classify 는 y 를 보지 않는다
    chk("⑤ classify 가 y 에 불변",
        [classify(r) for r in base] == [classify(r) for r in shook])

    #  ★⑥ 옛 래칫을 실제로 재현해 **시험이 그것을 잡는지** 확인한다.
    #     (시험이 빨간불을 못 냈을 때 "검사기가 못 잡았다" 와 "시험이 안 돌았다" 를
    #      구분하라 — 2026-09-17 교훈.  그래서 여기서 옛 규칙을 되살려 돌려 본다.)
    def _ratchet(rows, score):
        """옛 판의 축약: 지표가 오르면 후보를 지운다."""
        keep = list(rows)
        for cand in sorted(rows, key=lambda r: -abs(r["best"])):
            if classify(cand) == "in-envelope":
                continue
            trial = [r for r in keep if r is not cand]
            if score(trial) > score(keep) + 0.002:
                keep = trial
                break
        return [r["case"] for r in keep]
    #  y 가 큰 쪽을 지우면 '점수' 가 오르는 장난감 지표
    score = lambda rs: -np.var([r["best"] for r in rs]) / 100.0 if rs else 0.0
    a = _ratchet(base, score)
    b = _ratchet(shook, score)
    chk("★⑥ 옛 래칫은 y 에 따라 결과가 달라진다 (= ① 이 실효 시험이다)",
        a != b or len(a) != len(base), f"{a} vs {b}")

    print(f"porosity_close selftest: {ok}/{ok + fail} PASS")
    return 1 if fail else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--selftest', action='store_true',
                    help='자기검사 (외부 데이터 불요, <1s)')
    a = ap.parse_args()
    return _selftest() if a.selftest else report()


if __name__ == '__main__':
    sys.exit(main())
