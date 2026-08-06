"""make_results.py — docs/RESULTS.md 자동 생성 (Phase 6).

숫자를 손으로 옮겨 적지 않는다. 모든 값은 결과 파일에서 읽어 채운다.
격자를 다시 돌리면 문서도 다시 생성하면 된다.

문서 구조는 "질문 → 답 → 근거 → 한계" 순서다. 특히 **한계**를 마지막이 아니라
결론 바로 밑에 붙인다. 리뷰에서 유보된 항목(F4/F7/F14 등)이 결론과 떨어져
있으면 결론만 인용되기 때문이다.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path

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
        lines.append(
            f"1. **dQ/dV 항을 넣으면 degeneracy가 {_pct(b['degenerate_frac'])} → "
            f"{_pct(i['degenerate_frac'])}로 준다** "
            f"(평균 |오차| {_pp(b['mean_abs_err'])} → {_pp(i['mean_abs_err'])}, "
            f"PE-NE 상쇄 {_pct(b['pe_ne_antisym_frac'])} → "
            f"{_pct(i['pe_ne_antisym_frac'])}). "
            f"33p 기존 목적함수 대비 34p 개선안의 실측 효과다.")
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
        # ★ 결론 문장은 숫자를 따라간다. 서사를 고정하면 데이터가 반대일 때 거짓말이 된다.
        if collapse >= 0.20:
            fact += (f"→ **실측에서 `LAM_PE ≈ LAM_NE`가 나와도 두 전극이 실제로 비슷하게 "
                     f"열화했다는 증거가 못 된다.** 방법이 서로 다른 전극을 상당 비율로 "
                     f"뭉개므로, 22p 결과를 물리로 읽으려면 이 붕괴율을 먼저 낮춰야 한다.")
        else:
            fact += (f"→ **이 방법은 서로 다른 전극을 같다고 뭉개지는 않는다.** "
                     f"따라서 22p의 `LAM_PE ≈ LAM_NE`를 \"둘을 구분 못 해서 생긴 값\"으로 "
                     f"단정할 수 없다.")
            if split is not None and split >= 0.20:
                fact += (f" 다만 실패는 **반대 방향**으로 나타난다 — 참값이 같은 조건의 "
                         f"{_pct(split)}에서 오히려 없는 격차를 만들어낸다. "
                         f"즉 이 방법으로 얻은 PE-NE **격차**는 신뢰도가 낮고, "
                         f"22p처럼 격차가 작게 나온 결과가 오히려 드문 축에 속한다.")
        if split is not None and split < 0.20:
            fact += f" (참값이 같은데 다르다고 답하는 비율은 {_pct(split)}.)"
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
    hess = next((_load(p) for p in sorted(in_dir.glob("hessian_*.parquet"))), None)

    from tools.compare_objectives import to_markdown

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
        P.append("22p 근방 격자점은 **참값이 애초에 `LAM_PE = LAM_NE`** 다. 거기서 "
                 "복원값이 비슷하게 나오는 건 아무 증거가 못 된다. 물어야 할 것은 "
                 "반대 방향이다 — **참값이 뚜렷이 다를 때도 fitting이 둘을 같다고 "
                 "말하는가.**\n")
        P.append("| objective | 넓은 격차 조건 n | **격차 붕괴율** | shrinkage | "
                 "거짓 분리율 |")
        P.append("|---|---|---|---|---|")
        for o, g in gaps.items():
            if "gap_collapse_frac" not in g:
                continue
            P.append(f"| {o} | {g['n_wide_gap_true']} | "
                     f"**{_pct(g['gap_collapse_frac'])}** | "
                     f"{g['shrinkage']:.2f} | "
                     f"{_pct(g.get('false_split_frac'))} |")
        P.append("")
        P.append("- **격차 붕괴율**: 참 격차 ≥ 6%p인데 복원 격차 < 2%p로 답한 비율. "
                 "높을수록 \"두 전극이 비슷하다\"는 관측이 무의미해진다.")
        P.append("- **shrinkage**: 복원 격차 / 참 격차의 평균. 1이면 격차를 그대로 "
                 "복원, 0에 가까우면 전부 뭉갠다.")
        P.append("- **거짓 분리율**: 참값은 같은데 다르다고 답한 비율 (반대 방향 오류).\n")

    # ── Hessian ──
    if hess is not None and len(hess):
        P.append("## 곡률 진단 (Hessian)\n")
        P.append("최적점에서 목적함수의 2차 미분. 최소 고윳값 방향으로는 파라미터를 "
                 "움직여도 곡선이 거의 안 변한다 = 데이터가 그 조합을 구분하지 못한다.\n")
        P.append(f"- 조건수 중앙값: **{hess['condition_number'].median():.3g}**")
        P.append(f"- flat direction score 중앙값: "
                 f"**{hess['flat_direction_score'].median():.2g}** (0에 가까울수록 평평)")
        if "pe_ne_coupled" in hess.columns:
            P.append(f"- **α_PE·α_NE가 같은 부호로 묶인 조건: "
                     f"{_pct(hess['pe_ne_coupled'].mean())}** — "
                     f"\"PE와 NE를 함께 움직여도 곡선이 안 변한다\"가 성립하는 비율. "
                     f"22p에서 LAM_PE ≈ LAM_NE가 나온 것이 물리가 아니라 수학일 수 "
                     f"있다는 직접 증거다.")
        P.append("")

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
