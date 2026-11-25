#!/usr/bin/env python3
"""committee_sweep_verdict.py — 위원회 불일치 **온도 스윕** 판정 (T1).

왜 이게 필요한가 — watch 가 잘못 경보했다
------------------------------------------
watch_all.py 는 각 온도 표본에서 **600 K 에서 뽑은 고정 절대 문턱**(break = 600 K p95)을
넘는 프레임 수를 세어 800 K 59/200, 1000 K 118/200 을 "⚠⚠ 급증" 으로 찍었다.
그런데 조화 고체에서 RMS 힘은 √T 로 커진다. 모델 간 **상대** 오차가 완전히 같아도
절대 불일치는 √T 로 커지고, 고정 문턱을 넘는 프레임은 당연히 는다.
→ **그 경보는 온도 스케일링을 외삽으로 오독한 것일 수 있다.** 이 도구가 판별한다.

무엇을 재는가 (세 가지를 나란히)
  A. 절대   : 그대로의 불일치 (eV/Å). 궤적 잡음의 실제 크기 — 이건 이것대로 사실이다.
  B. 상대   : 불일치 / 그 표본의 평균 힘 크기. **이 지표의 원래 목적(외삽 판정)에 맞는 양.**
  C. 스케일 문턱 : 600 K 문턱에 힘크기 비를 곱해 다시 센 초과 수.
     A 의 초과가 C 에서 사라지면 = 열적 스케일링, 남으면 = 진짜 외삽.

  python3 tools/ionic/committee_sweep_verdict.py --glob '~/work/committee_modelc_T*'
"""
import argparse
import csv
import json
import os
import re
import sys
from glob import glob
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mlip_committee import load_preds, frame_disagreement, force_scale   # noqa: E402

# ⚠ 이 온도가 교정(기준선) 표본이다. 여기서 문턱을 뽑았으므로 이 온도의 초과 수는
#   정의상 5% 라 **결과가 아니다** (mlip_committee 의 순환성 주석과 같은 함정).
BASE_T = 600


# ── 판정 조각 (순수 함수 — selftest 가 여기를 그대로 부른다) ──────────────────
def signed_max_by_magnitude(values):
    """크기가 제일 큰 값을 **부호를 유지한 채** 돌려준다.

    ⛔⛔ 왜 이 함수가 따로 있나 (회신 AW 해제조건 ⑤ · 2026-09-07)
      종전 코드는 `max(...)` 였다. `(-30%, -5%)` 가 오면 `-5%` 가 뽑혀
      `abs(drift) < 10` 을 통과했다 — **30 % 표류가 "열적 스케일링" 초록으로 나갔다.**
      크기로 골라야 게이트가 성립하고, 부호는 진단(어느 방향으로 벌어지나)이라 남긴다.
    """
    vals = list(values)
    return max(vals, key=abs) if vals else 0.0


def drift_class(drift, resid, n_frames):
    """표류·잔차 → `'ok' | 'extrapolation' | 'middle'`.

    resid/n_frames 는 `{T: 개수}` · `{T: 프레임수}`.
    ⚠ 문턱(10 % · 25 % · 잔차 10 %)은 종전 값 그대로다 — 이번 변경은 **부호 처리만**이다.
    """
    if abs(drift) < 10 and all(v <= 0.10 * n_frames[T] for T, v in resid.items()):
        return "ok"
    if abs(drift) > 25:          # ⚠ abs — 종전 `drift > 25` 는 음의 큰 표류를 놓쳤다
        return "extrapolation"
    return "middle"


def resolve_base_T(rows, want):
    """기준 온도를 정한다. 없으면 **멈춘다** — 조용히 대체하지 않는다.

    ⛔ 왜 함수로 뺐나 (회신 BG ⑤ · 2026-09-07): 이 판정이 `main()` 안에 있어서
      `_selftest()` 가 **실제 missing-base-T 경로를 한 번도 안 밟았다.** 게이트를
      고쳐 놓고 시험은 그 옆을 지나가고 있었다.
    """
    if want not in rows:
        raise SystemExit(
            f"⛔ 기준 온도 {want} K 의 자료가 없다 (있는 것: {sorted(rows)}).\n"
            f"   조용히 다른 온도로 대체하지 않는다 — 기준이 바뀌면 표류의 정의가 바뀐다.\n"
            f"   다른 기준을 쓰려면 명시한다:  --base_T {sorted(rows)[0] if rows else '<T>'}")
    return want


def _selftest():
    ok = bad = 0
    def chk(c, msg):
        nonlocal ok, bad
        print(("  ⭕ " if c else "  ⛔ ") + msg); ok, bad = ok + (1 if c else 0), bad + (0 if c else 1)

    chk(signed_max_by_magnitude([5.0, 3.0]) == 5.0, "양수는 큰 쪽")
    chk(signed_max_by_magnitude([]) == 0.0, "빈 입력은 0")
    chk(signed_max_by_magnitude([-30.0, -5.0]) == -30.0,
        "⛔음성: **(−30, −5) 에서 −30 을 고른다** — 종전 max 는 −5 를 골라 게이트를 통과시켰다")
    chk(signed_max_by_magnitude([-30.0, 12.0]) == -30.0, "⛔음성: 부호가 섞여도 크기로 고른다")
    chk(signed_max_by_magnitude([-4.0, 9.0]) == 9.0, "크기가 같은 방향이면 그대로")

    nf = {800: 100, 1000: 100}
    chk(drift_class(5.0, {800: 0, 1000: 0}, nf) == "ok", "작은 표류 + 잔차 없음 = ok")
    chk(drift_class(-30.0, {800: 0, 1000: 0}, nf) == "extrapolation",
        "⛔음성: **음의 30 % 표류를 잡는다** (종전 `drift > 25` 는 못 잡았다)")
    chk(drift_class(30.0, {800: 0, 1000: 0}, nf) == "extrapolation", "양의 30 % 도 잡는다")
    chk(drift_class(15.0, {800: 0, 1000: 0}, nf) == "middle", "사이는 middle — 단정 금지")
    chk(drift_class(5.0, {800: 50, 1000: 0}, nf) == "middle",
        "⛔음성: 표류가 작아도 **잔차가 문턱을 넘으면 ok 가 아니다**")
    # ── 기준온도 부재 (회신 BG ⑤) — 이 경로를 종전 selftest 가 **한 번도 안 밟았다** ──
    chk(resolve_base_T({600: 1, 800: 2}, 600) == 600, "있는 기준온도는 그대로 쓴다")
    try:
        resolve_base_T({800: 1, 1000: 2}, 600); _hit = False
    except SystemExit:
        _hit = True
    chk(_hit, "⛔음성: **기준온도 자료가 없으면 멈춘다** — 조용히 다른 온도로 대체하면 "
              "표류의 정의 자체가 바뀐다")
    try:
        resolve_base_T({}, 600); _hit2 = False
    except SystemExit:
        _hit2 = True
    chk(_hit2, "⛔음성: 자료가 아예 비어도 멈춘다 (빈 dict 에서 KeyError 로 죽지 않는다)")

    print(f"  selftest: ⭕ {ok} · ⛔ {bad}")
    return 0 if bad == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", default="~/work/committee_modelc_T*")
    ap.add_argument("--base_T", type=int, default=BASE_T)
    ap.add_argument("--out_json", default=None)
    ap.add_argument("--out_csv", default=None)
    ap.add_argument("--selftest", action="store_true",
                    help="판정 조각만 시험한다 (자료·GPU 불필요)")
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())

    dirs = {}
    for p in sorted(glob(os.path.expanduser(a.glob))):
        m = re.search(r"_T(\d+)$", p)
        if m and os.path.isdir(p):
            dirs[int(m.group(1))] = p
    if not dirs:
        sys.exit(f"온도 디렉터리를 못 찾음: {a.glob}")

    rows = {}
    for T in sorted(dirs):
        preds = load_preds(dirs[T])
        names = sorted(preds)
        F = {k: preds[k]["forces"] for k in names}
        pf, _ = frame_disagreement(F, names)
        scale = force_scale(F, names)
        syms = [str(s) for s in preds[names[0]]["symbols"]]
        rel_el = {}
        for el in sorted(set(syms)):
            m = np.array([s == el for s in syms])
            vals = [np.sqrt(((F[x] - F[y])[:, m, :] ** 2).sum(axis=2)).mean()
                    for i, x in enumerate(names) for y in names[i + 1:]]
            mag = force_scale(F, names, m)
            rel_el[el] = float(np.mean(vals) / mag) if mag > 1e-9 else None
        rows[T] = {"dir": dirs[T], "engines": names, "n_frames": int(len(pf)),
                   "per_frame": pf, "force_scale_eV_per_A": scale,
                   "median": float(np.median(pf)), "p95": float(np.percentile(pf, 95)),
                   "relative_median": float(np.median(pf)) / scale,
                   "by_element_relative": rel_el}

    # ⛔⛔ 2026-09-07 (회신 AW 해제조건 ⑤) — 종전엔 기준 온도가 없으면 **말없이**
    #   최저 T 로 갈아탔다. 그러면 "600 K 대비 표류" 라고 찍힌 숫자가 실은 800 K 대비이고,
    #   화면·JSON 어디에도 그 사실이 안 남는다. 표류는 기준이 바뀌면 값이 통째로 바뀌는 양이다.
    #   ⇒ 대체하지 않고 **멈춘다.** 일부러 다른 기준을 쓰려면 `--base_T` 로 **선언**한다.
    if False:  # (판정은 resolve_base_T 로 옮겼다 — 아래 한 줄)
        raise SystemExit(
            f"⛔ 기준 온도 {a.base_T} K 의 자료가 없다 (있는 것: {sorted(rows)}).\n"
            f"   최저 T 로 조용히 갈아타지 않는다 — 표류는 기준이 바뀌면 값이 바뀐다.\n"
            f"   다른 기준을 쓰려면 명시한다:  --base_T {sorted(rows)[0]}")
    bT = resolve_base_T(rows, a.base_T)
    brk = rows[bT]["p95"]
    s0 = rows[bT]["force_scale_eV_per_A"]

    print("=" * 78)
    print(f"위원회 온도 스윕 판정 — 기준선 T{bT} (break = 그 표본의 p95 = {brk:.4f} eV/Å)")
    print("=" * 78)
    print(f"{'T':>6s} {'n':>5s} {'힘크기':>8s} {'√(T/T0)':>8s} | "
          f"{'중앙(abs)':>10s} {'중앙(rel)':>10s} | {'고정문턱초과':>12s} {'스케일문턱초과':>14s}")
    for T in sorted(rows):
        r = rows[T]
        sc = r["force_scale_eV_per_A"]
        fixed = int((r["per_frame"] > brk).sum())
        scaled_brk = brk * sc / s0                    # 힘 크기에 비례해 문턱을 옮긴다
        scaled = int((r["per_frame"] > scaled_brk).sum())
        r.update(n_above_fixed=fixed, n_above_scaled=scaled,
                 scaled_threshold=scaled_brk, sqrtT=float(np.sqrt(T / bT)))
        tag = "  ← 기준선(자명)" if T == bT else ""
        print(f"{T:6d} {r['n_frames']:5d} {sc:8.4f} {np.sqrt(T/bT):8.3f} | "
              f"{r['median']:10.4f} {r['relative_median']:10.4f} | "
              f"{fixed:6d}/{r['n_frames']:<5d} {scaled:8d}/{r['n_frames']:<5d}{tag}")

    print("-" * 78)
    # ── 불일치를 힘으로 설명하는 모형 ────────────────────────────────────
    # ⚠ 왜 이걸 봐야 하나: 상대(=D/F)가 온도와 함께 **줄면** 언뜻 "고온이 더 안전"으로
    #   읽히지만, 불일치에 온도무관 바닥 a 가 있으면 D/F = a/F + b 라서 F 가 커질수록
    #   자동으로 준다. 즉 감소 자체는 결론이 아니다. a 를 실제로 재서 분리한다.
    Ts = sorted(rows)
    Fv = np.array([rows[T]["force_scale_eV_per_A"] for T in Ts])
    Dv = np.array([rows[T]["median"] for T in Ts])
    fit = {}
    if len(Ts) >= 3:
        (b_, a_), *_ = np.linalg.lstsq(np.vstack([Fv, np.ones_like(Fv)]).T, Dv, rcond=None)
        r2 = 1 - ((Dv - (a_ + b_ * Fv)) ** 2).sum() / ((Dv - Dv.mean()) ** 2).sum()
        (n_, c_), *_ = np.linalg.lstsq(
            np.vstack([np.log(Fv), np.ones_like(Fv)]).T, np.log(Dv), rcond=None)
        r2p = 1 - ((np.log(Dv) - (c_ + n_ * np.log(Fv))) ** 2).sum() / \
            ((np.log(Dv) - np.log(Dv).mean()) ** 2).sum()
        floor_share = float(a_ / rows[bT]["median"])
        fit = {"linear_intercept_eV_per_A": float(a_), "linear_slope": float(b_),
               "linear_R2": float(r2), "power_exponent": float(n_), "power_R2": float(r2p),
               "floor_share_at_base_T": floor_share}
        print(f"D = a + b·F :  a = {a_:+.4f} eV/Å (온도무관 바닥) · b = {b_:.4f} · R² = {r2:.4f}")
        print(f"D = c·F^n   :  n = {n_:.3f} · R² = {r2p:.4f}   (n<1 = 힘보다 느리게 증가)")
        print(f"→ T{bT} 불일치의 {floor_share*100:.0f}% 가 **열운동과 무관한 바닥**이다. "
              f"상대값 감소는 그만큼 자동이므로 '고온이 더 안전'으로 읽지 말 것.")
        print("-" * 78)

    # ── 판정 ────────────────────────────────────────────────────────────
    rel = {T: rows[T]["relative_median"] for T in rows}
    hi = [T for T in rel if T > bT]
    drift = signed_max_by_magnitude((rel[T] / rel[bT] - 1) * 100 for T in hi)
    print(f"상대 불일치 표류 (고온 **최대 크기** vs T{bT}): {drift:+.1f}%")
    resid = {T: rows[T]["n_above_scaled"] for T in hi}
    print(f"스케일 문턱 초과 (고온): " + " · ".join(
        f"T{T} {resid[T]}/{rows[T]['n_frames']}" for T in sorted(resid)) if resid else "")
    _cls = drift_class(drift, resid, {T: rows[T]["n_frames"] for T in rows})
    if _cls == "ok":
        verdict = ("✅ **열적 스케일링이다 — 외삽 아님.** 절대 불일치 증가는 힘 크기(√T) 를 "
                   "따라간 것이고, 상대 불일치는 평평하다. 600/800/1000 K 3점 Arrhenius 는 "
                   "이 지표로는 막히지 않는다. watch 의 '⚠⚠ 급증' 은 고정 절대 문턱의 착시.")
    elif _cls == "extrapolation":
        # ⚠ 방향을 문구에 적는다 — 커지는 것과 작아지는 것은 다른 얘기다.
        _dir = ("커진다" if drift > 0 else
                "**작아진다**(고온에서 상대 불일치가 줄어든다 — 스케일링 가정이 "
                "반대로 깨진 것일 수 있다)")
        verdict = (f"⛔ **진짜 외삽 신호.** 힘 크기로 정규화해도 상대 불일치가 {_dir} → "
                   "고온 배열이 훈련 분포 밖일 수 있다. Arrhenius 상단 신뢰 불가.")
    else:
        verdict = ("🔶 **중간 — 단정 금지.** 상대 표류가 작지 않지만 결정적이지도 않다. "
                   "프레임 수를 늘리거나(200→500) 고온 표본에 DFT 단일점 스팟체크를 붙여야 한다.")
    print(verdict)
    print("-" * 78)
    print("원소별 **상대** 불일치 (abs/평균힘) — 어느 화학이 온도와 함께 벌어지나")
    els = sorted({e for r in rows.values() for e in r["by_element_relative"]})
    print("  " + f"{'T':>6s} " + " ".join(f"{e:>7s}" for e in els))
    for T in sorted(rows):
        v = rows[T]["by_element_relative"]
        print("  " + f"{T:6d} " + " ".join(
            f"{v[e]:7.4f}" if v.get(e) is not None else f"{'—':>7s}" for e in els))
    print("=" * 78)
    print("⛔ 규율: 이 지표는 **절대 정확도를 말하지 않는다** (세 엔진 전부 PBE 계열). "
          "일치해도 절대 σ 인용 금지는 그대로다.")

    # ── 산출물 ──────────────────────────────────────────────────────────
    out = {"property": "mlip_committee_temperature_sweep", "base_T": bT,
           "fixed_threshold_eV_per_A": brk, "verdict": verdict,
           "relative_drift_pct": drift,
           # ⚠ 2026-09-01 이전엔 fit 을 콘솔에만 찍고 JSON 에 안 남겼다 —
           #   /benchmarks 가 없는 키를 읽다 깨진 원인. 이제 지속한다.
           "force_model": fit,
           "by_T": {str(T): {k: v for k, v in r.items() if k != "per_frame"}
                    for T, r in rows.items()},
           "honesty": [
               "고정 절대 문턱을 온도가 다른 표본에 적용하면 √T 힘 스케일링을 외삽으로 오독한다 "
               "— watch_all.py 의 '급증' 경보가 그 사례다.",
               "상대 불일치(abs/평균힘)가 이 지표의 목적(외삽 판정)에 맞는 양이다.",
               "절대 불일치 증가 자체는 사실이다 — 고온 궤적의 힘 잡음은 실제로 더 크다. "
               "다만 그것은 '훈련 분포 밖'이 아니라 '더 격렬한 열운동'이다.",
           ]}
    if a.out_json:
        Path(a.out_json).write_text(json.dumps(out, ensure_ascii=False, indent=2,
                                               default=float) + "\n")
        print(f"→ {a.out_json}")
    if a.out_csv:
        with open(a.out_csv, "w", newline="", encoding="utf-8-sig") as f:
            f.write("# MLIP committee disagreement vs temperature (modelc / LPSCl1.6)\n")
            f.write(f"# fixed break threshold {brk:.4f} eV/A from T{bT} p95; "
                    f"scaled = threshold x (force_scale_T / force_scale_T{bT})\n")
            w = csv.writer(f)
            w.writerow(["T_K", "n_frames", "force_scale_eV_per_A", "median_abs_eV_per_A",
                        "median_relative", "n_above_fixed", "n_above_scaled",
                        "scaled_threshold_eV_per_A"] + [f"relative_{e}" for e in els])
            for T in sorted(rows):
                r = rows[T]
                w.writerow([T, r["n_frames"], f"{r['force_scale_eV_per_A']:.5f}",
                            f"{r['median']:.5f}", f"{r['relative_median']:.5f}",
                            r["n_above_fixed"], r["n_above_scaled"],
                            f"{r['scaled_threshold']:.5f}"]
                           + [f"{r['by_element_relative'].get(e) or float('nan'):.5f}" for e in els])
        print(f"→ {a.out_csv}")


if __name__ == "__main__":
    main()
