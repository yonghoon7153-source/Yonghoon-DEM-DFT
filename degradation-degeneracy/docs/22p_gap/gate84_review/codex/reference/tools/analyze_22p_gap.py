"""analyze_22p_gap.py — 22p 동작점에서 두 전극을 가를 수 있는가.

★ 이 저장소의 원래 질문에 **직접** 답하는 분석이다.

v4 본 격자는 `0.0:0.20:0.02` 라 값이 전부 짝수 백분위여서 22p 조건
(LAM_PE ≈ LAM_NE ≈ 0.13, LLI ≈ 0.17) 이 격자에 없었다. `verdict_22p` 가
반경 0.021 로 잡은 8점은 그 조건을 둘러싼 corner 이고 참 격차가 0 또는 2%p
뿐이라 wide-gap 이 하나도 없었다 — "참 격차가 큰데도 같다고 답하는가" 를
그 표본으로는 물을 수 없다 (v4 결론 3 의 한계).

`configs/grid_22p.yaml` 은 22p 를 격자에 정확히 넣고 평균 LAM 을 0.13 에
고정한 채 |ΔLAM| 을 0 → 12%p 로 쓴다. 이 도구는 그 스윕을 읽어

  · 참 격차별 **붕괴율** (복원 격차 < tol) 과 복원/참 비
  · 22p 동작점(LLI 0.17 · 평균 LAM 0.13 · noise 0) 만의 값
  · 평균·LLI·noise 를 넓혀 n 을 키운 값

을 나란히 낸다. **둘을 함께 봐야 한다** — 좁히면 n 이 작고, 넓히면 동작점이
아니다.

    python tools/analyze_22p_gap.py --in results/fit_22p_v1
    python tools/analyze_22p_gap.py --in results/fit_22p_v1 --plot out.png

★ 기준 곡선(grid ↔ half-cell)을 비교할 때는 `--restrict-to` 로 **모집단을
  맞춰야 한다.** `src/scoring.py` 는 reference != "grid" 이면 recoverable 을
  True 로 고정하므로, 그냥 나란히 놓으면 남는 차이가 기준 효과인지 난이도가
  다른 모집단인지 구분되지 않는다 (`tools/compare_cases.py` 의 경고와 같다).

    python tools/analyze_22p_gap.py --in results/fit_22p_fine_hc \
           --restrict-to results/fit_22p_fine
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

log = logging.getLogger(__name__)

#: 22p 동작점
P22 = {"lli": 0.17, "lam_mean": 0.13}


def _fmt_pp(x) -> str:
    return "—" if x is None or (isinstance(x, float) and np.isnan(x)) \
        else f"{100 * float(x):.1f}%p"


#: 격차가 bin 중심에서 이만큼(bin 폭 대비) 넘게 떨어져 있으면 격자 불일치로 본다
_BIN_FIT_ATOL = 0.05


def gap_table(df: pd.DataFrame, tol: float = 0.02,
              bin_w: float = 0.01) -> pd.DataFrame:
    """참 격차 구간별 복원 성적.

    붕괴 = 참 격차가 있는데 복원 격차 < tol → "두 전극이 같다" 고 답한 것.

    `bin_w` 는 **격자 간격과 맞아야 한다.** 0.01 로 묶는데 0.005 격자를 넣으면
    numpy 의 half-to-even 때문에 0.005 → 0%p, 0.015 → 2%p 로 조용히 어긋난다.
    참 격차 0.5%p 인 조건이 "참 격차 0" 칸에 섞이면 거짓 분리율이 통째로
    오염되므로, 안 맞으면 **멈춘다**.
    """
    from tools.compare_objectives import gap_lt

    g = df.copy()
    g["gap_true"] = (g["lam_pe"] - g["lam_ne"]).abs()
    g["gap_hat"] = g["pe_ne_gap_recovered"]

    q = np.asarray(g["gap_true"], dtype=float) / bin_w
    off = np.abs(q - np.round(q))
    if len(off) and off.max() > _BIN_FIT_ATOL:
        bad = float(g["gap_true"].iloc[int(np.argmax(off))])
        raise SystemExit(
            f"참 격차 {bad:.4f} 가 bin 폭 {bin_w} 의 배수가 아닙니다 "
            f"(어긋남 {off.max():.2f} bin). 그대로 묶으면 표가 거짓이 됩니다 — "
            f"격자 간격에 맞는 --gap-bin 을 주세요 (예: 0.005 격자면 0.005).")

    g["gap_bin"] = np.round(q).astype(int)          # bin_w 단위

    # ★ 라벨은 **실제 판정선**을 말해야 한다. 예전엔 "복원<2%p" 로 박혀 있어서
    #   `--tol 0.04` 로 돌린 출력이 다른 수치를 내면서도 머리글은 2%p 라고
    #   했다. 이 출력이 문서의 인용 근거로 커밋되므로 어긋나면 안 된다.
    collapse_col = f"붕괴(복원<{100 * tol:.0f}%p)"

    rows = []
    for b, sub in g.groupby("gap_bin", sort=True):
        collapsed = gap_lt(sub["gap_hat"], tol)
        rows.append({
            "참 격차": f"{100 * b * bin_w:g}%p",
            "n": int(len(sub)),
            collapse_col: f"{int(collapsed.sum())}/{len(sub)}"
                          f" ({100 * collapsed.mean():.1f}%)",
            "복원 격차 중앙값": _fmt_pp(sub["gap_hat"].median()),
            # ★ 이름이 방향을 주장하면 안 된다. 촘촘한 격자 실측에서 이 값은
            #   전 구간 1보다 컸다 (복원 격차가 참보다 **크다**) — "shrinkage"
            #   라고 부르면 읽는 쪽이 부호를 반대로 읽는다.
            "복원/참 중앙값": ("—" if b == 0 else
                            f"{float((sub['gap_hat'] / sub['gap_true']).median()):.2f}"),
        })
    return pd.DataFrame(rows)


def _leg_digest(d: Path) -> str | None:
    """실행 디렉터리의 manifest 에서 code identity(source_digest)를 읽는다.

    ★ 자체 리뷰(sig 렌즈) — dense 비교의 grid 다리는 src 8fe84240, hc 다리는
      7250c6e6 에서 생산됐는데 이 도구가 어느 쪽 manifest 도 읽지 않아
      무언급으로 지나갔다. 이번엔 두 커밋 사이 src/ diff 가 비어 무해했지만,
      다음에 fit 코드가 낀 두 다리를 비교하면 조용히 통과한다.
    """
    import yaml
    mp = Path(d) / "manifest.yaml"
    if not mp.exists():
        return None
    try:
        man = yaml.safe_load(mp.read_text(encoding="utf-8")) or {}
    except Exception:  # noqa: BLE001 — 못 읽으면 unknown 으로 보고만 한다
        return None
    return (man.get("run_spec") or {}).get("source_digest") or man.get("source_digest")


def _as_dirs(x) -> list[Path]:
    return [Path(x)] if isinstance(x, (str, Path)) else [Path(p) for p in x]


def _pooled(dirs: list[Path], objective: str, tol: float, what: str) -> pd.DataFrame:
    """여러 실행의 채점 결과를 이어붙인다 (seed 스윕용).

    ★ 같은 `cond_id` 가 둘 이상 나오면 **멈춘다**. `noise_seed` 를 안 바꾸고
      돌리면 완전히 같은 행이 그대로 두 배가 되어 n 만 부풀고 새 정보는 0 이다.
      조용히 통과시키면 "n=300" 이 거짓이 된다.
    """
    from tools.compare_cases import _scored

    frames = []
    for d in dirs:
        f = _scored(d / "fits.parquet", tol)
        f = f[f["objective"] == objective]
        if f.empty:
            raise SystemExit(f"{what} {d}: 목적함수 {objective} 행이 없습니다")
        frames.append(f.assign(_run_dir=str(d)))

    df = pd.concat(frames, ignore_index=True)
    dup = df["cond_id"].duplicated()
    if dup.any():
        ex = sorted(df.loc[dup, "cond_id"].unique())[:5]
        raise SystemExit(
            f"{what}: 실행들 사이에 같은 cond_id 가 {int(dup.sum())}건 겹칩니다 "
            f"(예: {ex}). seed 스윕이라면 실행마다 --noise-seed 를 다르게 주세요 "
            f"— 안 그러면 같은 행이 중복돼 n 만 부풀고 새 정보는 없습니다.")
    return df


def run(in_dir, objective: str = "pocv_dvdq", tol: float = 0.02,
        plot: str | None = None, restrict_to=None, noise: float = 0.0,
        bin_w: float = 0.01, breakdown: bool = False) -> dict:
    """`in_dir` 은 디렉터리 하나 또는 **여러 개**(seed 스윕을 모을 때).

    `noise` — ①·①'·② 가 볼 잡음 수준. 기본 0. **noise 0 에서는 잡음 실현이
    없으므로 `--noise-seed` 를 바꿔도 결과가 똑같다** — seed 스윕은 noise > 0
    에서만 의미가 있고, 그때 이 인자로 그 층을 지목한다.

    `restrict_to` — **모집단을 맞추는** 기준 실행 (보통 grid 기준 fit 디렉터리).

    `src/scoring.py` 는 `reference != "grid"` 이면 `recoverable` 을 True 로
    **고정**한다 (전 범위 half-cell 테이블은 창이 부족할 일이 없다는 물리
    가정). 그래서 같은 조건 집합을 돌려도 half-cell 쪽 표본이 grid 쪽보다
    크다. 그 상태로 두 기준을 나란히 놓으면 남는 차이가 기준 효과인지
    **난이도가 다른 모집단**인지 구분되지 않는다 — `compare_cases.py` 가
    맨 앞에서 경고하는 함정과 같다.

    `restrict_to` 를 주면 `공통 cond_id ∩ 그쪽에서 복원가능` 으로 좁힌다.

    `breakdown` — ①' 의 **참 격차 0 칸**을 LLI·LAM 축으로 쪼개 본다. 이 칸은
    거짓 분리율의 분모이자 §0 결론의 절반인데, 균질하다는 보장이 없다.
    실제로 조밀 격자에서 촘촘 격자와 겹치는 15조건은 80%, 나머지 66조건은
    15% 로 갈렸고 **22p 동작점 자신이 앞쪽 무리에 있다** — 평균만 인용하면
    동작점의 값을 잘못 말하게 된다.
    """
    from tools.compare_objectives import gap_is_zero, gap_lt

    in_dirs = _as_dirs(in_dir)
    df = _pooled(in_dirs, objective, tol, "--in")

    # ★ 자체 리뷰 F-B — 실패한 fit(NaN hat)은 gap_lt(NaN, tol)=False 로
    #   "붕괴 아님" = "전극을 갈랐다" 쪽에 집계된다. 실패가 많을수록 지표가
    #   좋아지는 방향의 오염이므로 멈춘다.
    bad = df["pe_ne_gap_recovered"].isna()
    if bad.any():
        ex = sorted(df.loc[bad, "cond_id"].astype(str))[:5]
        raise SystemExit(
            f"복원 격차가 NaN 인 행이 {int(bad.sum())}건 있습니다 (예: {ex}). "
            f"실패한 fit 이 섞이면 붕괴율이 좋은 쪽으로 왜곡됩니다 — "
            f"해당 조건의 fit 로그를 확인하세요.")

    df = df.copy()
    df["lam_mean"] = (df["lam_pe"] + df["lam_ne"]) / 2
    df["gap_true"] = (df["lam_pe"] - df["lam_ne"]).abs()

    restriction = None
    if restrict_to is not None:
        ref_dirs = _as_dirs(restrict_to)
        ref = _pooled(ref_dirs, objective, tol, "--restrict-to")
        # `isin` 이 이미 이쪽에 없는 cond_id 를 걸러내므로 교집합은 불필요하다
        # (M24 로 확인 — 넣고 빼도 결과가 같은 죽은 코드였다).
        keep = set(ref.loc[ref["recoverable"], "cond_id"])
        # ★ 자체 리뷰 F-A — 기준의 복원가능 조건이 이쪽에 없으면 멈춘다.
        #   중단·resume 실패한 부분 fit 을 넣으면 "모집단을 맞췄다"는 머리말
        #   아래에서 진부분집합이 조용히 비교되던 경로다 (fail-closed 위반).
        missing = sorted(keep - set(df["cond_id"]))
        if missing:
            raise SystemExit(
                f"--restrict-to: 기준 실행의 복원가능 조건 {len(missing)}개가 "
                f"이쪽 실행에 없습니다 (예: {missing[:5]}). 부분 fit(중단된 "
                f"실행)인지 확인하세요 — 이대로 비교하면 모집단이 다릅니다.")
        before = int(len(df))
        dropped = sorted(set(df["cond_id"]) - keep)
        df = df[df["cond_id"].isin(keep)].copy()
        # 모집단은 기준 실행이 정한다 — 이쪽의 recoverable 열은 더 이상 안 본다
        df["recoverable"] = True
        restriction = {
            "run_dir": str(ref_dirs[0]) if len(ref_dirs) == 1
                       else [str(d) for d in ref_dirs],
            "n_runs": len(ref_dirs),
            "정의": "공통 cond_id ∩ 기준 실행에서 recoverable",
            "n_kept": int(len(df)),
            "n_dropped": before - int(len(df)),
            "n_dropped_conditions": len(dropped),
            "dropped_examples": [str(c) for c in dropped[:5]],
        }
        if df.empty:
            raise SystemExit(f"--restrict-to {ref_dirs}: 남는 조건이 없습니다")

    rec = df[df["recoverable"]] if "recoverable" in df.columns else df

    # ── ① 22p 동작점만 (LLI 0.17 · 평균 LAM 0.13 · noise 0) ─────────────
    tight = rec[(rec["lli"].sub(P22["lli"]).abs() < 1e-9)
                & (rec["lam_mean"].sub(P22["lam_mean"]).abs() < 1e-9)
                & (rec["noise"] == noise)]

    # ── ①' 동작점 **근방** — 좁히면 n 이 작고 넓히면 동작점이 아니다.
    #      그 사이를 메우는 중간 층 (★ 첫 실행에서 ① 이 n=5 였다).
    near = rec[(rec["lli"].sub(P22["lli"]).abs() <= 0.021)
               & (rec["lam_mean"].sub(P22["lam_mean"]).abs() <= 0.021)
               & (rec["noise"] == noise)]

    # ── ② 넓힌 표본 — LLI 전부 · 평균 전체 · noise 0 ──────────────────────
    wide = rec[rec["noise"] == noise]

    out = {
        "objective": objective, "tol": tol, "noise": noise, "bin_w": bin_w,
        "in_dirs": [str(d) for d in in_dirs],
        "n_runs": len(in_dirs),
        "n_rows_total": int(len(df)),
        "n_recoverable": int(len(rec)),
        "tight": {"n": int(len(tight)),
                  "정의": f"LLI=0.17 · 평균 LAM=0.13 · noise={noise:g} · 복원가능군"},
        "near": {"n": int(len(near)),
                 "정의": f"|LLI−0.17|≤2%p · |평균 LAM−0.13|≤2%p · noise={noise:g}"
                         " · 복원가능군"},
        "wide": {"n": int(len(wide)),
                 "정의": f"noise={noise:g} · 복원가능군 (평균·LLI 전부)"},
    }
    if restriction is not None:
        out["restricted_to"] = restriction

    identity = {str(d): _leg_digest(d) for d in in_dirs}
    if restrict_to is not None:
        identity.update({str(d): _leg_digest(d) for d in _as_dirs(restrict_to)})
    out["code_identity"] = identity

    print("=" * 74)
    print(f" 22p 동작점에서 두 전극을 가를 수 있는가  (objective={objective})")
    print("=" * 74)
    if len(in_dirs) > 1:
        print(f"\n※ 실행 {len(in_dirs)}개를 모았다 (seed 스윕): "
              + ", ".join(str(d) for d in in_dirs))
    if restriction is not None:
        print(f"\n※ 모집단을 {restriction['run_dir']} 의 복원가능군에 맞췄다 "
              f"(유지 {restriction['n_kept']}행 · 제외 {restriction['n_dropped']}행).")
        print("   기준 곡선끼리 비교하려면 이렇게 맞춘 뒤에만 나란히 놓을 수 있다.")
    digests = {v for v in identity.values() if v}
    if len(digests) > 1:
        print("\n⚠ 두 다리의 code identity(source_digest) 가 다릅니다: "
              + ", ".join(sorted(digests))
              + "\n  fit 코드(src/·run.sh)가 그 사이 안 바뀌었는지 git diff 로 "
                "확인하고, 인용 시 이 사실을 명시하세요.")
    print(f"\n전체 {len(df)}행 중 복원가능군 {len(rec)}행 "
          f"({100 * len(rec) / len(df):.0f}%)\n")

    print(f"① 22p 동작점만 — LLI 0.17 · 평균 LAM 0.13 · noise {noise:g}")
    print(f"   (평균을 고정했으므로 '격차 때문인지 총 열화량 때문인지' 가 안 섞인다)\n")
    if len(tight):
        t1 = gap_table(tight, tol, bin_w)
        print(t1.to_string(index=False))
        out["tight"]["table"] = t1.to_dict("records")
    else:
        print("   조건 없음 — 격자에 그 동작점이 없다")
    print(f"\n   ⚠ n={len(tight)} 로 작다. 아래 넓힌 표본과 **함께** 볼 것.\n")

    print(f"①' 동작점 근방 — |LLI−17%| ≤ 2%p · |평균 LAM−13%| ≤ 2%p"
          f" · noise {noise:g}")
    print("   (① 과 ② 사이 — 동작점을 크게 벗어나지 않으면서 n 을 키운다)\n")
    if len(near):
        tn = gap_table(near, tol, bin_w)
        print(tn.to_string(index=False))
        out["near"]["table"] = tn.to_dict("records")
    else:
        print("   조건 없음")
    print()

    print(f"② 넓힌 표본 — noise {noise:g} · 복원가능군 (평균 LAM·LLI 전부)")
    print("   (n 은 크지만 22p 동작점이 아닌 조건이 섞인다)\n")
    t2 = gap_table(wide, tol, bin_w)
    print(t2.to_string(index=False))
    out["wide"]["table"] = t2.to_dict("records")

    # ── 참 격차 0 칸의 축별 분해 (--breakdown) ─────────────────────────
    if breakdown and len(near):
        z = near[gap_is_zero(near["lam_pe"] - near["lam_ne"])].copy()
        z["_split"] = ~gap_lt(z["pe_ne_gap_recovered"], tol)
        bd: dict = {"n": int(len(z)), "정의": f"①' ∩ 참 격차 0 ∩ noise {noise:g}",
                    "lli": {}, "lam": {}}
        print(f"\n★ 참 격차 0 칸 분해 — n={len(z)} "
              f"(거짓 분리 {int(z['_split'].sum())}/{len(z)})")
        for axis, col in (("lli", "lli"), ("lam", "lam_pe")):
            print(f"   {axis:>4s} | " + "  ".join(
                f"{k:g}:{int(v['_split'].sum())}/{len(v)}"
                for k, v in sorted(z.groupby(col))))
            bd[axis] = {f"{k:g}": {"n": int(len(v)),
                                   "false_split": int(v["_split"].sum())}
                        for k, v in sorted(z.groupby(col))}
        print("   ⚠ 축마다 비율이 크게 다르면 평균은 동작점의 값이 아니다.")
        out["gap0_breakdown"] = bd

    # ── ③ 22p 조건 자체 ────────────────────────────────────────────────
    exact = df[(df["lli"].sub(0.17).abs() < 1e-9)
               & (df["lam_pe"].sub(0.13).abs() < 1e-9)
               & (df["lam_ne"].sub(0.13).abs() < 1e-9)]
    # ③ 은 의도적으로 **전 noise 층**을 보여준다 (행마다 noise 라벨이 붙는다).
    #   ①/①'/② 가 --noise 로 한 층만 볼 때도 ③ 은 안 걸러진다 — 머리말에 밝힌다.
    print(f"\n③ 22p 조건 그 자체 (0.13, 0.13, 0.17) — n={len(exact)} (전 noise 층)")
    for _, r in exact.iterrows():
        print(f"   noise={r['noise']:<6g} 복원 LAM_PE={r['lam_pe_hat']:.4f} "
              f"LAM_NE={r['lam_ne_hat']:.4f} LLI={r['lli_hat']:.4f} "
              f"| 복원 격차 {_fmt_pp(r['pe_ne_gap_recovered'])}"
              f" | recoverable={bool(r.get('recoverable', True))}")
    out["exact_22p"] = exact[["noise", "lam_pe_hat", "lam_ne_hat", "lli_hat",
                              "pe_ne_gap_recovered"]].to_dict("records")

    # ── ④ 누적 사건률 — 인용 가능한 한 줄이 표에서 바로 나오게 ───────────
    from tools.compare_objectives import gap_lt as _lt
    print(f"\n④ 누적 — '참 격차가 이만큼 이상인데 같다고 답한' 비율"
          f"  (판정선 {100 * tol:.0f}%p)")
    for label, sub in (("동작점 근방(①')", near), ("넓힌 표본(②)", wide)):
        if not len(sub):
            continue
        g = sub.copy()
        g["gap_true"] = (g["lam_pe"] - g["lam_ne"]).abs()
        line = []
        for thr in (0.04, 0.06, 0.08):
            s2 = g[g["gap_true"] >= thr - 1e-9]
            if not len(s2):
                line.append(f"≥{100*thr:.0f}%p: n=0")
                continue
            k = int(_lt(s2["pe_ne_gap_recovered"], tol).sum())
            # ★ 자체 리뷰(통계 렌즈) — seed 스윕을 모으면 행 수 ≠ 독립 표본 수
            #   (306행 = 51조건 × 6 seed). 조건 수를 병기해야 rule of three 를
            #   행 수에 적용하는 과신(0.98% vs 조건 단위 ~5.9%)을 막는다.
            n_cond = int(s2[["lli", "lam_pe", "lam_ne"]].drop_duplicates().shape[0])
            tail = f" [조건 {n_cond}]" if n_cond < len(s2) else ""
            line.append(f"≥{100*thr:.0f}%p: {k}/{len(s2)} ({100*k/len(s2):.1f}%){tail}")
            out.setdefault("cumulative", {}).setdefault(label, {})[
                f">={100*thr:.0f}pp"] = {"k": k, "n": int(len(s2)),
                                         "n_conditions": n_cond}
        print(f"   {label:<16s} " + "  ·  ".join(line))
    print("   ⚠ 동일가중 합성격자의 **조건부 사건률**이다 — 실제 셀 posterior 가 아니다.")
    if len(in_dirs) > 1:
        print("   ⚠ 여러 실행을 모았다 — 신뢰구간·rule of three 는 행 수가 아니라 "
              "[조건 N] 을 독립 단위로 계산할 것.")

    if plot:
        _plot(wide, tight, plot, objective, tol, noise=noise)
        print(f"\n그림: {plot}")
    print()
    return out


def _scatter_label(noise: float) -> str:
    # ★ 자체 리뷰 F-D — "noise 0" 하드코딩이었다. gap_table 라벨 버그(F tol)와
    #   같은 유형: 출력이 인용 근거가 되므로 라벨은 실제 값을 말해야 한다.
    return f"all (noise {noise:g}, recoverable)"


def _plot(wide: pd.DataFrame, tight: pd.DataFrame, path: str,
          objective: str, tol: float, noise: float = 0.0) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6.6, 6.2))
    hi = max(0.14, float(wide["gap_true"].max()) * 1.05)

    ax.axhspan(0, tol, color="#dc2626", alpha=.07)
    ax.axhline(tol, color="#dc2626", lw=1, ls=":")
    ax.text(0.004, tol * 1.06, f'judged "same"  (< {100*tol:.0f}%p)',
            fontsize=8.5, color="#dc2626")
    ax.plot([0, hi], [0, hi], color="#059669", lw=1.6, ls="--",
            label="perfect recovery")

    ax.scatter(wide["gap_true"] * 100, wide["gap_hat"] * 100 if "gap_hat" in wide
               else wide["pe_ne_gap_recovered"] * 100,
               s=16, c="#9aa5b1", alpha=.55, label=_scatter_label(noise))
    if len(tight):
        ax.scatter(tight["gap_true"] * 100,
                   tight["pe_ne_gap_recovered"] * 100,
                   s=95, marker="D", facecolors="none", edgecolors="#2563eb",
                   linewidths=2, label="22p operating point\n(LLI 17%, mean LAM 13%)")
    ax.set(xlabel="TRUE gap  |LAM_PE − LAM_NE|  [%p]",
           ylabel="RECOVERED gap  [%p]",
           title=f"Can the fit tell the electrodes apart?  ({objective})")
    ax.legend(fontsize=8.5, loc="upper left")
    ax.grid(alpha=.25)
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description="22p 동작점 격차 복원력 분석")
    ap.add_argument("--in", dest="in_dir", required=True, nargs="+",
                    help="fit 디렉터리. 여러 개 주면 모아서 센다 (seed 스윕). "
                         "실행마다 --noise-seed 가 달라야 한다 — 같으면 "
                         "cond_id 가 겹쳐 멈춘다.")
    ap.add_argument("--objective", default="pocv_dvdq")
    ap.add_argument("--tol", type=float, default=0.02)
    ap.add_argument("--plot", default=None)
    ap.add_argument("--restrict-to", dest="restrict_to", default=None, nargs="+",
                    help="모집단을 맞출 기준 실행 디렉터리 (보통 grid 기준 fit). "
                         "half-cell 기준은 recoverable 이 True 로 고정되므로 "
                         "이걸 주지 않고 두 기준을 비교하면 안 된다.")
    ap.add_argument("--noise", type=float, default=0.0,
                    help="①·①'·② 가 볼 잡음 수준 (기본 0). seed 스윕은 "
                         "noise>0 에서만 의미가 있다.")
    ap.add_argument("--gap-bin", dest="bin_w", type=float, default=0.01,
                    help="참 격차 bin 폭. 격자 간격과 맞아야 한다 "
                         "(0.005 격자면 0.005). 안 맞으면 멈춘다.")
    ap.add_argument("--breakdown", action="store_true",
                    help="참 격차 0 칸을 LLI·LAM 축으로 쪼개 본다 — 이 칸이 "
                         "균질한지(평균이 동작점의 값인지) 확인용.")
    ap.add_argument("--log-level", default="WARNING")
    args = ap.parse_args()
    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    run(args.in_dir, args.objective, args.tol, args.plot,
        restrict_to=args.restrict_to, noise=args.noise, bin_w=args.bin_w,
        breakdown=args.breakdown)


if __name__ == "__main__":
    main()
