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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", default="~/work/committee_modelc_T*")
    ap.add_argument("--base_T", type=int, default=BASE_T)
    ap.add_argument("--out_json", default=None)
    ap.add_argument("--out_csv", default=None)
    a = ap.parse_args()

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

    bT = a.base_T if a.base_T in rows else sorted(rows)[0]
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
    drift = max((rel[T] / rel[bT] - 1) * 100 for T in hi) if hi else 0.0
    print(f"상대 불일치 표류 (고온 최대 vs T{bT}): {drift:+.1f}%")
    resid = {T: rows[T]["n_above_scaled"] for T in hi}
    print(f"스케일 문턱 초과 (고온): " + " · ".join(
        f"T{T} {resid[T]}/{rows[T]['n_frames']}" for T in sorted(resid)) if resid else "")
    if abs(drift) < 10 and all(v <= 0.10 * rows[T]["n_frames"] for T, v in resid.items()):
        verdict = ("✅ **열적 스케일링이다 — 외삽 아님.** 절대 불일치 증가는 힘 크기(√T) 를 "
                   "따라간 것이고, 상대 불일치는 평평하다. 600/800/1000 K 3점 Arrhenius 는 "
                   "이 지표로는 막히지 않는다. watch 의 '⚠⚠ 급증' 은 고정 절대 문턱의 착시.")
    elif drift > 25:
        verdict = ("⛔ **진짜 외삽 신호.** 힘 크기로 정규화해도 상대 불일치가 크게 는다 → "
                   "고온 배열이 훈련 분포 밖. Arrhenius 상단 신뢰 불가.")
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
