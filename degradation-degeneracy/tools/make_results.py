"""make_results.py — docs/RESULTS.md 자동 생성 (Phase 6).

숫자를 손으로 옮겨 적지 않는다. 모든 값은 결과 파일에서 읽어 채운다.
격자를 다시 돌리면 문서도 다시 생성하면 된다.

문서 구조는 "질문 → 답 → 근거 → 한계" 순서다. 특히 **한계**를 마지막이 아니라
결론 바로 밑에 붙인다. 리뷰에서 유보된 항목(F4/F7/F14 등)이 결론과 떨어져
있으면 결론만 인용되기 때문이다.
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

# run.sh 없이 직접 실행해도 src/tools를 찾도록 (PYTHONPATH 미설정 대비)
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import pandas as pd
import yaml

log = logging.getLogger(__name__)


def _pct(x, digits: int = 0) -> str:
    return "—" if x is None or pd.isna(x) else f"{100 * float(x):.{digits}f}%"


def _pp(x, digits: int = 1) -> str:
    return "—" if x is None or pd.isna(x) else f"{100 * float(x):.{digits}f}%p"


def _load(path: Path):
    if not path.exists():
        return None
    if path.suffix == ".yaml":
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    if path.suffix == ".csv":
        return pd.read_csv(path)
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    return None


def _conclusion(cmp_res: dict, summary: dict) -> list[str]:
    """핵심 결론 3줄 — 숫자에서 직접 만든다."""
    tbl = pd.DataFrame(cmp_res["table"]).set_index("objective")
    lines = []

    base, imp = "pocv_dvdq", "pocv_dvdq_dqdv"
    if base in tbl.index and imp in tbl.index:
        b, i = tbl.loc[base], tbl.loc[imp]
        d = float(i["degenerate_frac"]) - float(b["degenerate_frac"])
        # ★ 방향을 숫자에서 읽는다. "줄었다"를 고정하면 늘었을 때 거짓말이 된다.
        if d < -0.02:
            verdict = f"**{_pct(abs(d))}p 줄어든다** — 34p 개선안의 실측 이득이다."
        elif d > 0.02:
            verdict = (f"오히려 **{_pct(d)}p 늘어난다.** 34p 개선안이 이 격자에서는 "
                       f"이득을 주지 못한다.")
        else:
            verdict = ("**사실상 변화가 없다**(차이 2%p 이내). 즉 34p의 dQ/dV 추가는 "
                       "이 합성 격자에서 최종 오차를 측정 가능하게 줄이지 못한다.")
        lines.append(
            f"1. dQ/dV 항을 넣으면 degeneracy가 {_pct(b['degenerate_frac'])} → "
            f"{_pct(i['degenerate_frac'])}로 {verdict} "
            f"(평균 |오차| {_pp(b['mean_abs_err'])} → {_pp(i['mean_abs_err'])}, "
            f"PE-NE 상쇄 {_pct(b['pe_ne_antisym_frac'])} → "
            f"{_pct(i['pe_ne_antisym_frac'])})")
    elif base in tbl.index:
        lines.append(f"1. 기존 목적함수({base})의 degeneracy는 "
                     f"{_pct(tbl.loc[base, 'degenerate_frac'])}다.")

    # ★ 22p 질문의 직접적인 답 — 22p 근방 성적보다 이게 먼저다.
    #   22p 근방 격자점은 참값이 LAM_PE = LAM_NE라 "복원값도 같더라"가 증거가 안 된다.
    g = cmp_res.get("gap_analysis", {}).get(base, {})
    if g and "error" not in g and "gap_collapse_frac" in g:
        collapse, split = g["gap_collapse_frac"], g.get("false_split_frac")
        fact = (f"2. 참값이 뚜렷이 다른 조건(|ΔLAM|_true ≥ {_pp(g['gap_thresh'], 0)})에서 "
                f"fitting이 두 전극을 같다고 답하는 비율은 "
                f"**{_pct(collapse)}** (n={g['n_wide_gap_true']}). "
                f"참 격차 {_pp(g['mean_true_gap_wide'])} → 복원 격차 "
                f"{_pp(g['mean_recovered_gap_wide'])}, shrinkage {g['shrinkage']:.2f}. ")
        lr = g.get("likelihood_ratio_equal")
        if lr is not None and split is not None:
            fact += (f"\n\n   관측 \"두 전극이 같다\"가 어느 쪽을 지지하는지는 우도비로 나온다.\n\n"
                     f"   > P(같다고 답 | 참값 같음) = {_pct(1 - split)}\n"
                     f"   > P(같다고 답 | 참값 {_pp(g['gap_thresh'], 0)} 이상 차이) = {_pct(collapse, 1)}\n"
                     f"   > **우도비 ≈ {lr:.0f} : 1**\n\n"
                     f"   → **22p의 `LAM_PE ≈ LAM_NE`는 degeneracy의 증거가 아니라, 두 전극이 "
                     f"실제로 비슷하게 열화했다는 쪽의 증거다.**")
        # ★ 임계 의존성은 **항상** 싣는다. 표에만 두면 결론만 인용될 때 빠진다.
        if "collapse_requires_gap_err" in g:
            fact += (f"\n\n   ⚠ 이 숫자들은 임계 설정에 의존한다. 붕괴로 세려면 격차를 "
                     f"{_pp(g['gap_thresh'], 0)}에서 {_pp(g['tol'], 0)} 아래로 끌어내려야 하므로 "
                     f"최소 {_pp(g['collapse_requires_gap_err'], 0)}의 격차 오차가 필요한데, "
                     f"실측 격차 오차는 중앙값 {_pp(g['gap_err_median'])}·"
                     f"99분위 {_pp(g['gap_err_p99'])}다. ")
            fact += ("붕괴가 원리적으로 관측 가능한 범위이긴 하나, 낮은 붕괴율의 상당 부분은 "
                     "**오차 스케일이 임계 간격보다 작다**는 사실에서 온다."
                     if g.get("collapse_measurable", True) else
                     "즉 낮은 붕괴율은 **이 임계 설정에서 붕괴가 관측되기 어렵다**는 사실의 "
                     "재진술에 가깝고, 우도비도 그만큼 임계 의존적이다.")
        lines.append(fact)

    v = cmp_res.get("verdict_22p", {}).get(base, {})
    if v and "error" not in v:
        anti = v.get("pe_ne_antisym_frac", 0)
        gap_t, gap_r = v.get("true_pe_ne_gap"), v.get("recovered_pe_ne_gap")
        lines.append(
            f"3. **22p 조건(LAM_PE≈LAM_NE≈13%, LLI≈17%) 근방 자체의 degeneracy는 "
            f"{_pct(v['degenerate_frac'])}**"
            f" — 최근접 {v['n_near']}개 조건의 평균 |오차| {_pp(v['mean_abs_err'])}, "
            f"PE-NE 오차 상쇄 {_pct(anti)}, "
            f"참 PE-NE 격차 {_pp(gap_t)} → 복원 격차 {_pp(gap_r)}. "
            f"⚠ 이 근방은 참값이 애초에 LAM_PE = LAM_NE인 격자점이므로, "
            f"여기서 복원이 잘 된다는 사실만으로는 22p 결과를 옹호할 수 없다 "
            f"(위 2번이 답이다).")

    coup = summary.get("hessian_pe_ne_coupled_frac")
    if coup is not None:
        lines.append(
            f"{len(lines) + 1}. **평평한 방향이 PE-NE 결합인 조건은 {_pct(coup)}다.** "
            f"22p 패턴이 \"PE와 NE를 함께 움직여도 곡선이 안 변해서\" 생겼다는 가설의 "
            f"직접적인 음성 결과다 — 목적함수가 잘 정의되지 않은 방향은 있지만, "
            f"그 방향이 두 전극의 동반 이동은 아니다.")

    ur = cmp_res.get("unrecoverable_frac", 0.0)
    lines.append(
        f"{len(lines) + 1}. **격자의 {_pct(ur)}는 grid 기준에서 원리적으로 복원 불가**"
        f"(참값 α<1 → 재구성 창이 reference 범위를 벗어남)다. "
        f"위 숫자는 모두 복원가능군 {summary.get('n_rows_recoverable', '?')}행에서만 센 값이며, "
        f"복원불가군을 섞으면 목적함수 간 차이가 묻힌다.")
    return lines


def build(in_dir, out_path="docs/RESULTS.md", repo_root=".") -> Path:
    in_dir, repo_root = Path(in_dir), Path(repo_root)
    cmp_res = _load(in_dir / "objective_comparison.yaml")
    if cmp_res is None:
        raise SystemExit(f"{in_dir}/objective_comparison.yaml 없음 — "
                         f"먼저 python tools/compare_objectives.py --in {in_dir}")
    summary = _load(in_dir / "degeneracy_summary.yaml") or {}
    manifest = _load(in_dir / "manifest.yaml") or {}
    wsweep = _load(in_dir / "wsweep" / "weight_sweep.yaml")
    hess_by_obj = {}
    for hp in sorted(in_dir.glob("hessian_*.parquet")):
        d = _load(hp)
        if d is not None and len(d):
            hess_by_obj[hp.stem.replace("hessian_", "")] = d
    hess = next(iter(hess_by_obj.values()), None)

    from tools.compare_objectives import OBJ_ORDER as OBJ_ORDER_LOCAL, to_markdown

    tbl = pd.DataFrame(cmp_res["table"])
    tbl_noise = pd.DataFrame(cmp_res.get("table_by_noise", []))

    P = []
    P.append("# RESULTS — full-cell 곡선으로 LAM_PE와 LAM_NE를 분리할 수 있는가\n")
    P.append("> 이 파일은 `tools/make_results.py`가 결과 파일에서 자동 생성한다. "
             "직접 수정하지 말 것.\n")
    P.append(f"생성: {datetime.now(timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M %Z')}  ")
    P.append(f"입력: `{in_dir}`  ")
    if manifest:
        P.append(f"git: `{manifest.get('git_commit', '?')}`"
                 f"{' (dirty)' if manifest.get('git_dirty') else ''}  ")
    P.append("")

    # ── 질문 ──
    P.append("## 질문\n")
    P.append("2026-08-05 연구세미나 22p에서 `LAM_PE ≈ LAM_NE ≈ 13%`, `LLI ≈ 17%`가 "
             "나왔다. 이것이 실제 물리인가, 아니면 full-cell 곡선 하나로는 두 전극을 "
             "가를 수 없어서 생긴 **fitting degeneracy**인가.\n")
    P.append("정답을 아는 PyBaMM 합성 곡선을 격자로 만들고, 기존 α·β fitting이 "
             "그 정답을 복원하는지 채점해 답한다.\n")

    # ── 결론 ──
    P.append("## 핵심 결론\n")
    for line in _conclusion(cmp_res, summary):
        P.append(line + "\n")

    # ── 한계 (결론 바로 밑) ──
    P.append("### 이 결론이 말하지 않는 것\n")
    gap = summary.get("coverage_gap") or {}
    P.append(f"- **격자 공백(F14)**: 완방 프레임 guard 때문에 저LLI 영역에 고LAM_PE "
             f"조건이 없다. 저LLI(≤2%)에서 도달한 최대 LAM_PE는 "
             f"`{gap.get('max_lam_pe_at_low_lli', '?')}`, 격자 전체 최대는 "
             f"`{gap.get('max_lam_pe_overall', '?')}`. "
             f"고LAM_PE 결론은 고LLI가 동반된 조건에서만 검증된 것이다.")
    P.append("- **restart 불일치율(F4)**: adaptive 조기 종료로 조건마다 restart 수가 "
             "달라, multi-start 불일치율을 목적함수 간 비교 지표로 쓰지 않았다. "
             "`degeneracy_summary.yaml`의 `restart_conditioned` 항목에 "
             "restart 수로 조건화한 값만 있다.")
    P.append("- **방법 바이어스(F5)**: 판정 기준 2%p가 방법 자체의 계통 편향과 "
             "같은 크기일 수 있어, 바이어스를 뺀 보정 판정을 표에 나란히 뒀다. "
             "두 값이 크게 다르면 그 목적함수의 결론은 약하다.")
    P.append("- 모두 **합성 데이터** 결과다. 실제 셀의 모델 오차(SEI, 저항 분포 등)는 "
             "여기에 없다. 즉 이 값들은 degeneracy의 **하한**이다 — 실제는 더 나쁘다.\n")

    # ── 비교표 ──
    P.append("## 목적함수 4종 비교\n")
    P.append("복원가능군(F1)만, 노이즈 전체 합산.\n")
    P.append(to_markdown(tbl) + "\n")
    if len(tbl_noise):
        P.append("### 노이즈 수준별 (F10)\n")
        P.append("dQ/dV의 이점은 노이즈에서 희석된다. 노이즈 0 결과만 인용하면 "
                 "과대평가가 된다.\n")
        P.append(to_markdown(tbl_noise) + "\n")

    # ── 22p ──
    P.append("## 22p 실험 조건 판정\n")
    P.append("*모두 `noise = 0` 조건이다. 노이즈가 있으면 값이 달라진다(F10) — `objective_comparison.yaml`의 `verdict_22p.noise` 참조.*\n")
    P.append("| objective | 근방 조건 | degeneracy | 평균 \\|err\\| | "
             "err LAM_PE | err LAM_NE | PE-NE 상쇄 |")
    P.append("|---|---|---|---|---|---|---|")
    for o, v in cmp_res.get("verdict_22p", {}).items():
        if "error" in v:
            continue
        P.append(f"| {o} | {v['n_near']} | {_pct(v['degenerate_frac'])} | "
                 f"{_pp(v['mean_abs_err'])} | {_pp(v['mean_err_lam_pe'])} | "
                 f"{_pp(v['mean_err_lam_ne'])} | {_pct(v['pe_ne_antisym_frac'])} |")
    P.append("")
    P.append("`err LAM_PE`와 `err LAM_NE`의 **부호가 반대**면, 한쪽을 과대평가한 만큼 "
             "다른 쪽을 과소평가해 full-cell 곡선에서 상쇄된 것이다 — degeneracy의 "
             "특징적 지문이다.\n")

    # ── 전극 격차 복원력 ──
    gaps = cmp_res.get("gap_analysis") or {}
    if any("gap_collapse_frac" in g for g in gaps.values()):
        P.append("## 전극 격차를 구분하는가 — 22p 질문의 직접적인 답\n")
        P.append("*`noise = 0` 조건 기준.*\n")
        P.append("22p 근방 격자점은 **참값이 애초에 `LAM_PE = LAM_NE`** 다. 거기서 "
                 "복원값이 비슷하게 나오는 건 아무 증거가 못 된다. 물어야 할 것은 "
                 "반대 방향이다 — **참값이 뚜렷이 다를 때도 fitting이 둘을 같다고 "
                 "말하는가.**\n")
        P.append("| objective | 넓은 격차 조건 n | **격차 붕괴율** | shrinkage | "
                 "거짓 분리율 | 붕괴에 필요한 격차오차 / 실측 중앙값 |")
        P.append("|---|---|---|---|---|---|")
        for o, g in gaps.items():
            if "gap_collapse_frac" not in g:
                continue
            need = (f"{_pp(g['collapse_requires_gap_err'], 0)} / "
                    f"{_pp(g['gap_err_median'])}"
                    if "collapse_requires_gap_err" in g else "—")
            P.append(f"| {o} | {g['n_wide_gap_true']} | "
                     f"**{_pct(g['gap_collapse_frac'])}** | "
                     f"{g['shrinkage']:.2f} | "
                     f"{_pct(g.get('false_split_frac'))} | {need} |")
        P.append("")
        P.append("- **격차 붕괴율**: 참 격차 ≥ 6%p인데 복원 격차 < 2%p로 답한 비율. "
                 "높을수록 \"두 전극이 비슷하다\"는 관측이 무의미해진다.")
        P.append("- **shrinkage**: 복원 격차 / 참 격차의 평균. 1이면 격차를 그대로 "
                 "복원, 0에 가까우면 전부 뭉갠다.")
        P.append("- **거짓 분리율**: 참값은 같은데 다르다고 답한 비율 (반대 방향 오류).")
        P.append("- **붕괴에 필요한 격차오차**: 붕괴로 세려면 격차를 6%p에서 2%p 아래로 "
                 "끌어내려야 하므로 최소 4%p의 격차 오차가 필요합니다. 이 값이 실측 "
                 "격차오차 중앙값보다 크면, **낮은 붕괴율은 측정이 아니라 임계 설정의 "
                 "결과**입니다 — 그대로 인용하지 마세요.\n")

    # ── Hessian ──
    if hess_by_obj:
        P.append("## 곡률 진단 (Hessian) — 최적화와 무관한 측정\n")
        P.append("최적점에서 목적함수의 2차 미분. 최소 고윳값 방향으로는 파라미터를 "
                 "움직여도 곡선이 거의 안 변한다 = **데이터가 그 조합을 구분하지 "
                 "못한다**. optimizer가 어떻게 헤맸는지와 무관한 국소 지표라는 점이 "
                 "장점이지만, **목적함수가 비매끄러우면 곡률 자체가 잘 정의되지 "
                 "않는다** — 아래 두 경고를 반드시 함께 볼 것.\n")
        P.append("| objective | n | 조건수(중앙값) | flat score | 최소고윳값>0 | α_PE·α_NE 결합 |")
        P.append("|---|---|---|---|---|---|")
        for o in (list(OBJ_ORDER_LOCAL) + sorted(set(hess_by_obj) - set(OBJ_ORDER_LOCAL))):
            d = hess_by_obj.get(o)
            if d is None:
                continue
            coup = (_pct(d["pe_ne_coupled"].mean())
                    if "pe_ne_coupled" in d.columns else "—")
            pos = (_pct(d["min_eigval_positive"].mean())
                   if "min_eigval_positive" in d.columns else "—")
            P.append(f"| {o} | {len(d)} | {d['condition_number'].median():.3g} | "
                     f"{d['flat_direction_score'].median():.2g} | {pos} | {coup} |")
        P.append("")
        P.append("- **조건수**는 매끄러운 목적함수라면 작을수록 최적점이 잘 정의돼 "
                 "있다는 뜻이다. 다만 그 해석은 아래 조건이 모두 만족될 때만 쓸 수 있다.")
        eps_vals = sorted({float(d["eps"].iloc[0]) for d in hess_by_obj.values()
                           if "eps" in d.columns})
        P.append("- ⚠ **조건수의 절대값은 인용하지 마세요.** 목적함수가 여러 스케일에서 "
                 "울퉁불퉁하면 수치 Hessian이 수렴하지 않아, eps를 바꾸면 값이 자릿수 "
                 "단위로 움직입니다 (F23). 의미가 있는 것은 **같은 eps에서의 순서**뿐입니다"
                 + (f" (이 표는 eps={eps_vals[0]:g})." if len(eps_vals) == 1
                    else f" (⚠ 이 표에 eps가 {eps_vals} 로 섞여 있습니다 — 다시 뽑으세요)."))
        # ★ 조건수 순서가 실제 복원 성능과 어긋나면 그 사실을 문서가 스스로 말해야 한다
        try:
            err_by = {r["objective"]: r["mean_abs_err"] for r in cmp_res["table"]}
            pairs = [(d["condition_number"].median(), err_by[o])
                     for o, d in hess_by_obj.items() if o in err_by]
            if len(pairs) >= 3:
                import numpy as _np
                rho = float(_np.corrcoef([p[0] for p in pairs],
                                         [p[1] for p in pairs])[0, 1])
                if rho < 0:
                    best_c = min(hess_by_obj.items(),
                                 key=lambda kv: kv[1]["condition_number"].median())[0]
                    P.append(f"- ⚠⚠ **이 격자에서 조건수 순서는 실제 복원 성능과 "
                             f"역상관입니다** (상관계수 {rho:.2f}). "
                             f"예: `{best_c}`가 조건수는 가장 좋은데 평균 |오차|는 "
                             f"{_pp(err_by[best_c])}로 나쁩니다. 지형이 거칠면 곡률이 "
                             f"크게 잡히므로, 낮은 조건수가 \"잘 정의된 최적점\"이 아니라 "
                             f"**울퉁불퉁함**을 잰 것일 수 있습니다. "
                             f"조건수를 \"정보가 더 많다\"의 단독 근거로 쓰지 마세요.")
        except Exception:  # noqa: BLE001
            pass
        P.append("- **최소고윳값>0** — 100%가 아니면 그만큼은 최적점이 아니라 **안장점**에서 "
                 "곡률을 잰 것입니다. 그 조건들의 조건수는 해석하지 마세요.")
        P.append("- **α_PE·α_NE 결합** — 평평한 방향에서 두 전극이 같은 부호로 묶여 "
                 "있는 비율. 높으면 \"PE와 NE를 함께 움직여도 곡선이 안 변한다\"는 "
                 "뜻이고, 22p에서 LAM_PE ≈ LAM_NE가 나온 것이 물리가 아니라 수학이라는 "
                 "직접 증거가 된다.\n")

    # ── multi-start (F21) ──
    # ★ F21b: 목적함수 간 비교는 무작위 restart끼리만 해야 공정하다.
    #   warm start 지점(restart 0)이 섞이면 dQ/dV 계열이 인위적으로
    #   multimodal 쪽으로 쏠린다.
    fair = (summary or {}).get("multistart_random_only")
    ms = fair or (summary or {}).get("multistart") or {}
    ms_rows = {k: v for k, v in ms.items() if not k.startswith("_")}
    if ms_rows:
        P.append("## multi-start 진단 — 진짜 degeneracy와 최적화 난이도의 구분\n")
        P.append("같은 조건을 여러 초기값에서 다시 풀었을 때 어떻게 갈리는지를 봅니다. "
                 "**두 실패 모드는 처방이 정반대**라 반드시 나눠야 합니다.\n")
        if fair:
            P.append("> 아래 표는 **무작위 restart끼리만** 비교한 것입니다(F21b). "
                     "dQ/dV 목적함수는 첫 restart에 매끄러운 해를 초기값으로 받으므로, "
                     "그것을 포함하면 최적 J에 닿는 restart가 정의상 하나뿐이 되어 "
                     "항상 multimodal로 찍힙니다.\n")
            # ★ F4 검정력 편향 — restart 0을 빼고 2개 미만이 남으면 그 조건은 제외되는데,
            #   adaptive 조기 종료로 restart 수가 조건마다 달라 목적함수별 n이 어긋난다.
            ns = {k: v.get("n") for k, v in ms_rows.items() if v.get("n")}
            if ns and max(ns.values()) - min(ns.values()) > 0.1 * max(ns.values()):
                lo = min(ns, key=ns.get)
                P.append(f"> ⚠ **표본 수가 목적함수마다 다릅니다** "
                         f"({min(ns.values())}~{max(ns.values())}, 최소는 `{lo}`). "
                         f"adaptive 조기 종료로 restart 수가 조건마다 다르고, "
                         f"restart 0을 뺀 뒤 2개 미만이면 그 조건이 빠지기 때문입니다. "
                         f"**서로 다른 모집단을 비교하는 것**이므로 소수점 차이는 "
                         f"읽지 마세요 (F4).\n")
        P.append("| objective | n | **flat valley** | multimodal | unique min |")
        P.append("|---|---|---|---|---|")
        for o, d in ms_rows.items():
            P.append(f"| {o} | {d['n']} | **{_pct(d['flat_valley_frac'])}** | "
                     f"{_pct(d['multimodal_frac'])} | {_pct(d['unique_min_frac'])} |")
        P.append("")
        P.append("- **flat valley** — 같은 J인데 해가 서로 멀다. "
                 "**데이터가 그 조합을 구분하지 못한다는 직접 증거**입니다. "
                 "초기값을 아무리 잘 줘도 사라지지 않고, 측정 방식을 바꿔야 줄어듭니다.")
        P.append("- **multimodal** — J가 다른 국소최소가 여럿. degeneracy가 아니라 "
                 "**최적화 난이도**입니다. 좋은 초기값을 주면 사라집니다 "
                 "(dQ/dV 항이 이 경우였습니다 — 아래 참조).")
        P.append("- **unique min** — 해가 유일. 문제 없음.\n")
        worst = max(ms_rows.items(), key=lambda kv: kv[1].get("multimodal_frac", 0))
        if worst[1].get("multimodal_frac", 0) > 0.9:
            P.append(f"> ⚠ **`{worst[0]}`의 multimodal이 "
                     f"{_pct(worst[1]['multimodal_frac'])}로 극단적입니다.** "
                     f"flat valley 판정은 restart 2개 이상이 같은 J에 닿아야 성립하므로, "
                     f"이렇게 지형이 울퉁불퉁하면 flat valley가 있어도 **관측되지 "
                     f"않습니다.** 이 목적함수의 낮은 flat valley 값을 "
                     f"\"degeneracy가 적다\"로 읽으면 안 됩니다 — "
                     f"최적화와 무관한 곡률(Hessian) 쪽을 보세요.\n")
        P.append("> ⚠ `degeneracy_summary.yaml`의 `restart_conditioned` 블록에 있는 "
                 "`agree_frac`과 `p_spread`는 인용하지 마세요. adaptive 조기 종료 때문에 "
                 "`agree_frac`은 restart를 5까지 간 조건에서 **정의상 0**이고, "
                 "`p_spread = 0`은 \"해가 일치\"가 아니라 \"최적 J에 도달한 restart가 "
                 "하나뿐\"이라는 뜻입니다. 위 표가 그 자리를 대신합니다.\n")

    # ── 기준 곡선 비교 (Case 1 vs Case 2) ──
    case = _load(in_dir / "case_comparison.yaml")
    if case:
        from tools.compare_cases import to_markdown as case_md
        P.append("## 기준 곡선 비교 — Case 1 (전 범위 half-cell) vs Case 2 (격자 곡선)\n")
        P.append("목적함수를 바꾸는 것과 **기준 곡선을 바꾸는 것** 중 어느 쪽이 큰지.\n")
        P.append(case_md(case) + "\n")
        P.append("> ⚠ halfcell 쪽의 \"복원불가 0%\"는 **측정이 아닙니다.** "
                 "`src/scoring.py`가 `reference != \"grid\"`이면 `recoverable=True`로 "
                 "고정합니다(전 범위 테이블이라 창 부족이 없다는 물리적 근거). "
                 "그래서 위 표는 **두 실행의 공통 조건 중 grid 기준에서 복원가능한 것**으로 "
                 "행 수를 맞춰 비교한 것입니다.\n")

    # ── 가중치 ──
    if wsweep:
        opt = wsweep.get("optimum", {})
        P.append("## dQ/dV 가중치 — 임의 튜닝이 아니라는 근거\n")
        P.append(f"`w_dqdv`를 {wsweep.get('w_grid')}로 훑어 degeneracy 비율이 "
                 f"최소가 되는 값을 찾았다 "
                 f"(층화 표본 {wsweep.get('n_conditions')}조건, "
                 f"restart {wsweep.get('n_restarts')}).\n")
        P.append(f"- 노이즈 평균 최적: **w_dqdv = {opt.get('w_star_mean_over_noise')}** "
                 f"({opt.get('metric')} = {_pct(opt.get('value_at_w_star'), 1)}), "
                 f"기본값 w=1.0일 때 {_pct(opt.get('value_at_w1'), 1)}")
        for n, d in (opt.get("per_noise") or {}).items():
            P.append(f"- noise={n}: 최적 w = {d.get('w_dqdv')} "
                     f"({_pct(d.get(opt.get('metric')), 1)}, n={d.get('n')})")
        P.append(f"\n{opt.get('_주의', '')}\n")
        if wsweep.get("warm_start", True):
            P.append("> ⚠ **이 sweep은 `w=0` 행을 인용할 수 없습니다.** seed 목적함수 없이 "
                     "실행돼, `w=0`만 warm start를 못 받고 나머지는 받았습니다. "
                     "`w=0`이 유독 나쁘게 나오는 것은 dQ/dV 효과가 아니라 초기값 차이입니다 "
                     "(F20b). `w ≥ 0.25`끼리의 비교만 유효합니다.\n")
        P.append("결과: `configs/objectives_optimized.yaml`\n")

    # ── 그림 ──
    figs = cmp_res.get("figures") or {}
    if figs:
        P.append("## 그림\n")
        for k, p in figs.items():
            try:
                rel = Path(p).resolve().relative_to(repo_root.resolve())
            except ValueError:
                rel = Path(p)
            P.append(f"- `{rel}` — {k}")
        P.append("")

    # ── 재현 ──
    P.append("## 재현\n")
    P.append("```bash")
    P.append("./scripts/setup_env.sh && source .venv/bin/activate")
    P.append("./run.sh --mode verify")
    P.append(f"./run.sh --mode grid --config configs/grid_fine.yaml "
             f"--nproc $(nproc) --out {in_dir}")
    P.append(f"./run.sh --mode fit   --in {in_dir} --nproc $(nproc)")
    P.append(f"./run.sh --mode score --in {in_dir}")
    P.append(f"./run.sh --mode hessian --in {in_dir}")
    P.append(f"./run.sh --mode report --in {in_dir}")
    P.append("```\n")
    P.append("관련 문서: `docs/06_REVIEW_DECISIONS.md`(해석 규칙), "
             "`docs/07_LAM_LLI.md`(열화모드 정의), `docs/GPU_NOTES.md`(GPU 판정)\n")

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(P), encoding="utf-8")
    log.info("저장: %s (%d줄)", out, len(P))
    return out


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description="docs/RESULTS.md 자동 생성")
    ap.add_argument("--in", dest="in_dir", required=True)
    ap.add_argument("--out", default="docs/RESULTS.md")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()
    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    print(build(args.in_dir, args.out))


if __name__ == "__main__":
    main()
