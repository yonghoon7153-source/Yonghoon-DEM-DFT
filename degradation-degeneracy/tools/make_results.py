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

import numpy as np
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


def _warm_start_asymmetry(fits) -> str | None:
    """dQ/dV 계열만 warm start를 받았는지 실측한다 (F20d/F39).

    한때 "34p가 유리한 조건인데도 못 이겼으니 결론이 보수적"이라고 썼다가
    내렸다. 그 논리는 warm start가 목적함수를 **단조롭게** 개선할 때만
    성립하는데, 비볼록 문제에서 특정 seed가 항상 더 좋은 basin으로 데려간다는
    보장이 없다. adaptive 조기 종료와 겹치면 평가 budget도 달라진다.
    지금은 "protocol이 다르다"는 사실만 적고 방향은 판단하지 않는다.
    """
    if fits is None or "warm_started" not in getattr(fits, "columns", []):
        return None
    w = fits.groupby("objective")["warm_started"].mean()
    base, imp = "pocv_dvdq", "pocv_dvdq_dqdv"
    if base not in w.index or imp not in w.index:
        return None
    if not (w[imp] > 0.5 and w[base] < 0.5):
        return None
    return (f"   ⚠ **두 목적함수의 optimizer protocol이 다릅니다.** dQ/dV 계열은 "
            f"매끄러운 해를 초기값으로 받고(`pocv_dvdq_dqdv` 중 {_pct(w[imp])}), "
            f"`pocv_dvdq`는 그 시드 제공자라 받지 않습니다({_pct(w[base])}). "
            f"adaptive 조기 종료까지 겹치면 평가 budget도 달라집니다. "
            f"따라서 위 수치는 **현재 pipeline에서 관측된 값**이지 목적함수의 "
            f"정보량 비교가 아닙니다. 어느 쪽이 유리한지도 단정할 수 없습니다 — "
            f"비볼록 문제에서 특정 seed가 항상 더 좋은 basin으로 데려간다는 보장이 "
            f"없기 때문입니다. 정보량을 비교하려면 동일 seed·동일 restart budget·"
            f"early stop off의 paired 재실행이 필요합니다.")


def _conclusion(cmp_res: dict, summary: dict, fits=None) -> list[str]:
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
            f"raw PE/NE 오차 반대부호 비율 {_pct(b['pe_ne_antisym_frac'])} → "
            f"{_pct(i['pe_ne_antisym_frac'])} — **물리적 상쇄로 해석 불가**)")
        # ★ pe_ne_antisym은 raw 오차의 **부호**만 센다. 목적함수마다 전역 편향의
        #   부호가 다르면 그 차이가 곧바로 "상쇄"로 잡힌다. 실측에서 편향을 빼면
        #   방향이 뒤집혔다(70.5→52.6% raw vs 33.1→42.9% 중심화). 인과로 읽지 말 것.
        lines.append(
            "   ⓘ **위 반대부호 비율을 '34p가 상쇄를 줄였다'로 읽지 마세요.** 이 지표는 "
            "raw 오차의 부호만 세는데, 목적함수마다 전역 편향의 부호가 달라 그 차이가 "
            "그대로 잡힙니다. 목적함수별 평균편향을 뺀 뒤 다시 세면 방향이 뒤집힙니다. "
            "전압 민감도로 가중하지 않은 파라미터 오차 부호는 full-cell 곡선에서 실제로 "
            "상쇄되는 양을 재지도 않습니다.")
        # ★ 모집단이 결론의 방향을 바꾸는지 — compare_objectives가 스스로 판정한 값
        ps = cmp_res.get("population_sensitivity") or {}
        if ps.get("direction_flips"):
            lines.append(
                f"   ⚠ **이 순위는 모집단에 따라 뒤집힙니다.** 복원가능군에서는 34p−33p = "
                f"{_pp(ps['dqdv_minus_base_recoverable'])}인데 전체 격자에서는 "
                f"{_pp(ps['dqdv_minus_base_all'])}입니다. 복원불가군(참 α<1)은 grid 기준에서 "
                f"정답이 표현 불가능한 조건이라 제외에 근거가 있지만, **그 제외가 우열을 "
                f"바꾸므로** 어느 모집단인지 없이 인용하면 안 됩니다.")
        note = _warm_start_asymmetry(fits)
        if note:
            lines.append(note)
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
            fact += (f"\n\n   관측 \"두 전극이 같다\"가 어느 쪽을 지지하는지 **사건 우도비**로 보면\n\n"
                     f"   > P(같다고 답 | 참 격차 < {_pp(g['tol'], 0)}) = {_pct(1 - split)}\n"
                     f"   > P(같다고 답 | 참 격차 ≥ {_pp(g['gap_thresh'], 0)}) = {_pct(collapse, 1)}\n"
                     f"   > 우도비 = {lr:.1f}")
            # ★ 이 값을 결론으로 승격시키지 않는다. 아래 세 제약을 같은 문단에 붙인다.
            lo, hi = g.get("lr_sensitivity_min"), g.get("lr_sensitivity_max")
            med = g.get("lr_sensitivity_median")
            fact += "\n\n   **이 값을 '두 전극이 실제로 비슷하다'로 읽을 수 없다.** 세 가지 때문이다.\n"
            if lo is not None:
                spike = g.get("lr_is_local_spike")
                fact += (f"\n   1. **임계 의존** — 같은 데이터에서 (참격차, 동일판정) 임계를 "
                         f"흔들면 우도비가 {lo:.1f}~{hi:.1f}(중앙값 {med:.1f})로 움직인다. "
                         + ("현재 조합은 이웃보다 유독 높은 **국소 봉우리**다 — 이 값을 "
                            "대표값으로 인용하면 사후선택이 된다. "
                            if spike else "")
                         + "아래 임계 민감도 표를 함께 볼 것.\n")
            fact += ("\n   2. **posterior가 아님** — 이건 두 합성 가설 아래의 *사건* 우도비다. "
                     "`P(참값이 같다 | fitting이 같다고 답함)`으로 바꾸려면 실제 셀 집단의 "
                     "사전확률과, 여기서 버린 중간 격차 구간의 주변분포가 필요하다. "
                     "격자점을 같은 빈도로 센 것은 실제 셀의 분포가 아니다.\n")
            fact += (f"\n   3. **부분집단 조건화** — 복원가능군"
                     f"(population={g.get('population', 'recoverable')})에서만 센 값이다. "
                     "실제 셀이 그 부분집단에 속한다는 독립 근거가 없으면 적용할 수 없고, "
                     "전체 격자에서는 값이 크게 달라진다(아래 표).\n")
            fact += ("\n   → 지금 자료로 방어할 수 있는 문장은 하나뿐이다: **이 합성 격자의 "
                     "복원가능군에서, 참 격차가 뚜렷한 조건이 '같다'로 붕괴하는 일은 드물었다.** "
                     "22p가 물리인지 degeneracy인지는 이것만으로 판정되지 않는다.")
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
            f"raw PE/NE 오차 반대부호 비율 {_pct(anti)}, "
            f"참 PE-NE 격차 {_pp(gap_t)} → 복원 격차 {_pp(gap_r)}. "
            f"⚠ 이 근방은 참값이 애초에 LAM_PE = LAM_NE인 격자점이므로, "
            f"여기서 복원이 잘 된다는 사실만으로는 22p 결과를 옹호할 수 없다 "
            f"(위 2번이 답이다).")

    # ★ F33 — Hessian은 결론에서 뺐다. `pe_ne_coupled`는 평평한 방향에서 α_PE와
    #   α_NE가 **같은 부호**인지를 세는데, 22p 가설(한쪽 과대·다른쪽 과소)은
    #   LAM에서 부호가 반대이고 α = (1−LAM)/r 이므로 α에서도 반대다. 즉 지표가
    #   묻는 질문이 가설과 다르다. (반대부호 방향도 재보니 0.0~0.5%였지만,
    #   eps 미수렴·안장점 혼입 때문에 어느 쪽으로도 근거가 못 된다.)

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
    fits = _load(in_dir / "fits.parquet")
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

    # ★ F35 — provenance가 없는 artifact에서 생성됐으면 문서 맨 위에 인용 금지
    #   배너를 박는다. 회답을 별도 문서에만 두면 저장소를 여는 사람은 철회 전
    #   결론을 먼저 본다.
    # 열 존재 여부만 보면 임의의 문자열 하나로 배너가 사라진다 (F38).
    from src.io import validate_provenance
    prov = validate_provenance(in_dir)
    # ★ F52b — 배너는 주 입력만 보면 안 된다. 비교표에 쓰인 half-cell artifact도
    #   전이적 입력이므로 그 검증 결과를 합친다 (compare_cases 가 봉인해 둔다).
    cc = _load(in_dir / "case_comparison.yaml") or {}
    cc_prov = cc.get("provenance") or {}
    for tag, v in cc_prov.items():
        if not v.get("ok"):
            prov["ok"] = False
            prov["fail"] = list(prov["fail"]) + [f"비교입력_{tag}"]
            prov["reasons"] = list(prov["reasons"]) + [
                f"{v.get('run_dir')} 가 provenance 검증 실패: {v.get('fail')}"]
            prov["checks"][f"비교입력_{tag}"] = f"실패 — {v.get('fail')}"
        else:
            prov["checks"][f"비교입력_{tag}"] = "통과"
    if cc and not cc_prov:
        prov["ok"] = False
        prov["fail"] = list(prov["fail"]) + ["비교입력_provenance_없음"]
        prov["reasons"] = list(prov["reasons"]) + [
            "case_comparison.yaml에 provenance 블록이 없다 (F52 이전 산출물)"]
        prov["checks"]["비교입력_provenance_없음"] = "실패 — F52 이전 산출물"
    if not prov["ok"]:
        P.append(
            "> # ⛔ 인용 금지\n"
            "> \n"
            "> 이 문서는 **재현 정보가 갖춰지지 않은 artifact**에서 생성됐습니다. "
            "실패한 검사: "
            + ", ".join(f"`{k}` — {r}" for k, r in zip(prov["fail"], prov["reasons"]))
            + ".\n> \n"
            "> 우도비, half-cell 목적함수 비교, raw PE/NE 부호 통계, multi-start, "
            "Hessian 수치를 인용하지 마십시오.\n"
            "> \n"
            "> 방향성 관측(예: half-cell 기준이 grid 기준보다 오차가 작다)까지만 "
            "참고하고, **정확한 비율과 p-value는 clean 재실행 후에** 쓰십시오. "
            "경위와 철회 목록은 `docs/08_REVIEW_RESPONSE.md`에 있습니다.\n")
    else:
        P.append("> ✅ provenance 검증 통과 — "
                 + ", ".join(f"`{k}`" for k in prov["checks"]) + "\n")
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
    for line in _conclusion(cmp_res, summary, fits):
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
             "여기에 없다. 합성 truth 생성이 LLI를 양·음극 초기농도에 일률적으로 "
             "적용하는 **한 가지 규약**에 조건부이기도 하다 (SEI·plating·전극별 "
             "endpoint 이동은 같은 총 inventory loss에서도 다른 곡선을 만든다). "
             "실제 셀이 더 나쁠지 나을지는 **증명되지 않았다** — 복잡성이 추가 "
             "정보를 만들 수도, 없앨 수도 있다.\n")

    # ── 비교표 ──
    P.append("## 목적함수 4종 비교\n")
    P.append("복원가능군(F1)만, 노이즈 전체 합산.\n")
    P.append(to_markdown(tbl) + "\n")
    # ★ F29 — 복원가능군 제외가 결론을 만드는지 보이려면 전체군을 나란히 둔다.
    tbl_all = pd.DataFrame(cmp_res.get("table_all_conditions") or [])
    if len(tbl_all):
        P.append("### 전체 격자 (복원불가군 포함)\n")
        ps = cmp_res.get("population_sensitivity") or {}
        P.append(
            "복원불가군(참 α<1)은 grid 기준에서 정답이 재구성 창 밖이라 **원리적으로** "
            "복원되지 않는 조건이다. 위 표에서 뺀 근거는 그것이다. 다만 그 제외가 "
            "난이도와 무관하지 않으므로(저LLI에서 복원가능 비율이 훨씬 낮다) 전체군을 "
            "같이 싣는다.\n")
        if ps.get("direction_flips"):
            P.append("> ⚠ **두 표에서 33p와 34p의 우열이 뒤집힙니다.** 결론 문장에 어느 "
                     "모집단인지 반드시 함께 쓰세요.\n")
        P.append(to_markdown(tbl_all) + "\n")

    if len(tbl_noise):
        P.append("### 노이즈 수준별 (F10)\n")
        P.append("dQ/dV의 이점은 노이즈에서 희석된다. 노이즈 0 결과만 인용하면 "
                 "과대평가가 된다.\n")
        P.append(to_markdown(tbl_noise) + "\n")

    # ── 22p ──
    P.append("## 22p 실험 조건 판정\n")
    P.append("*모두 `noise = 0` 조건이다. 노이즈가 있으면 값이 달라진다(F10) — `objective_comparison.yaml`의 `verdict_22p.noise` 참조.*\n")
    P.append("| objective | 근방 조건 | degeneracy | 평균 \\|err\\| | "
             "err LAM_PE | err LAM_NE | raw 반대부호 |")
    P.append("|---|---|---|---|---|---|---|")
    for o, v in cmp_res.get("verdict_22p", {}).items():
        if "error" in v:
            continue
        P.append(f"| {o} | {v['n_near']} | {_pct(v['degenerate_frac'])} | "
                 f"{_pp(v['mean_abs_err'])} | {_pp(v['mean_err_lam_pe'])} | "
                 f"{_pp(v['mean_err_lam_ne'])} | {_pct(v['pe_ne_antisym_frac'])} |")
    P.append("")
    P.append("> ⚠ **`raw 반대부호` 열을 degeneracy의 지문으로 읽지 마세요.** 이 열은 raw "
             "오차의 부호가 반대인 비율일 뿐이고, 목적함수마다 전역 편향의 부호가 다르면 "
             "그 차이가 그대로 잡힙니다. 편향을 중심화하면 목적함수 간 순서가 뒤집힙니다. "
             "또 전압 민감도로 가중하지 않은 파라미터 오차 부호는 full-cell 곡선에서 "
             "실제로 상쇄되는 양을 재지 않습니다.\n")

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

        # ★ F28 — 임계 2차원 민감도. 한 칸만 떼어 인용하지 못하게 표 전체를 싣는다.
        sens = (cmp_res.get("gap_sensitivity") or {}).get("pocv_dvdq") or []
        if sens:
            P.append("### 임계 민감도 — 위 숫자를 인용하기 전에 볼 것\n")
            P.append("같은 데이터에서 (참 격차 cutoff, 동일 판정 tol) 두 임계만 바꿔 "
                     "우도비를 다시 센 것이다 (`pocv_dvdq`, noise=0, 복원가능군). "
                     "값이 한 자릿수에서 수십까지 움직이면, 특정 조합의 값은 "
                     "**측정이 아니라 선택**이다.\n")
            for same_def, title in (("lt_tol", "참값 \"같다\" = 참 격차 < tol"),
                                    ("exact_zero", "참값 \"같다\" = 참 격차 정확히 0")):
                rows = [r for r in sens if r.get("same_def") == same_def]
                if not rows:
                    continue
                P.append(f"**{title}**\n")
                tols = sorted({r["tol"] for r in rows})
                gts = sorted({r["gap_thresh"] for r in rows})
                P.append("| 참 격차 ≥ \\ 동일 판정 < | "
                         + " | ".join(_pp(t, 0) for t in tols) + " |")
                P.append("|---" * (len(tols) + 1) + "|")
                look = {(r["gap_thresh"], r["tol"]): r for r in rows}
                for gt in gts:
                    cells = []
                    for t in tols:
                        r = look.get((gt, t))
                        if r is None:
                            cells.append("—")
                        elif not np.isfinite(r["likelihood_ratio"]):
                            cells.append(f"∞ (0/{r['n_wide']})")
                        else:
                            # 분자/분모를 같이 — 표본 1~2개짜리 칸을 가리지 않는다
                            cells.append(
                                f"{r['likelihood_ratio']:.1f}"
                                f"<br><sub>{r['n_same_called_same']}/{r['n_same']}"
                                f" ÷ {r['n_wide_called_same']}/{r['n_wide']}</sub>")
                    P.append(f"| **{_pp(gt, 0)}** | " + " | ".join(cells) + " |")
                P.append("")
            P.append("각 칸은 `우도비` 아래에 `분자/분모 ÷ 분자/분모`를 함께 적었다. "
                     "`∞`는 넓은 격차군에서 붕괴가 0건이라는 뜻이며, 요약 통계의 "
                     "min/max 범위에서는 제외되므로 개수를 "
                     "`gap_analysis.lr_sensitivity_n_infinite`로 따로 센다. "
                     "표의 최댓값을 대표값으로 쓰지 말 것.\n")

        # ★ F29 — 전체 격자에서의 같은 지표
        gaps_all = cmp_res.get("gap_analysis_all_conditions") or {}
        ga = gaps_all.get("pocv_dvdq") or {}
        if "likelihood_ratio_equal" in ga and "likelihood_ratio_equal" in (
                gaps.get("pocv_dvdq") or {}):
            P.append("### 모집단을 바꾸면 (복원불가군 포함)\n")
            P.append(f"| 모집단 | n(참격차 작음) | n(참격차 큼) | 붕괴율 | 우도비 |")
            P.append("|---|---|---|---|---|")
            for label, gg in (("복원가능군", gaps["pocv_dvdq"]), ("전체 격자", ga)):
                P.append(f"| {label} | {gg.get('n_small_gap_true', '—')} | "
                         f"{gg.get('n_wide_gap_true', '—')} | "
                         f"{_pct(gg.get('gap_collapse_frac'))} | "
                         f"{gg['likelihood_ratio_equal']:.1f} |")
            P.append("")
            P.append("복원가능군 조건화는 물리적 근거가 있지만(참 α<1이면 정답이 재구성 "
                     "창 밖), **그 조건화가 우도비를 크게 바꾼다**는 사실은 결론과 같은 "
                     "무게로 적어야 한다.\n")

    # ── Hessian ──
    if hess_by_obj:
        P.append("## 곡률 진단 (Hessian) — 참고용, 결론 근거 아님\n")
        P.append("> ⚠⚠ **이 절의 수치를 식별성(degeneracy) 근거로 인용하지 마세요.** "
                 "적대적 리뷰에서 세 가지가 확인됐습니다 (F33). ① 목적함수가 보간·미분·"
                 "peak 연산을 포함해 비매끄러운데 절대 step `eps` 하나를 모든 파라미터에 "
                 "씁니다 — 34p 조건수 중앙값이 eps=1e-3/1e-4/1e-5에서 12.8/229/17381로 "
                 "움직입니다. 수렴하지 않았다는 뜻입니다. ② `min_eigval_positive`가 "
                 "100%가 아닌 만큼은 최적점이 아니라 **안장점**에서 곡률을 잰 것인데 "
                 "flat score와 결합 판정은 그대로 집계됩니다. ③ `α_PE·α_NE 결합`은 "
                 "**같은 부호**를 세는데, 22p 가설(한쪽 과대·다른쪽 과소)은 α에서 부호가 "
                 "**반대**입니다 — 지표가 묻는 질문이 가설과 다릅니다.\n")
        P.append("최적점에서 목적함수의 2차 미분입니다. 아래는 진단 참고로만 두고, "
                 "결론이나 optimizer 방어 문장에 쓰지 않습니다.\n")
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
                     f"\"degeneracy가 적다\"로 읽으면 안 됩니다. "
                     f"(예전에는 여기서 Hessian을 대안으로 안내했으나, 그 지표도 eps 미수렴·"
                     f"안장점 혼입·가설과 다른 부호 규약으로 근거가 되지 못합니다 — F33.)\n")
        P.append("> ⚠ `degeneracy_summary.yaml`의 `restart_conditioned` 블록에 있는 "
                 "`agree_frac`과 `p_spread`는 인용하지 마세요. adaptive 조기 종료 때문에 "
                 "`agree_frac`은 restart를 5까지 간 조건에서 **정의상 0**이고, "
                 "`p_spread = 0`은 \"해가 일치\"가 아니라 \"최적 J에 도달한 restart가 "
                 "하나뿐\"이라는 뜻입니다. 위 표가 그 자리를 대신합니다.\n")

    # ── 기준 곡선 비교 (Case 1 vs Case 2) ──
    case = _load(in_dir / "case_comparison.yaml")
    if case and "grid" in case:
        from tools.compare_cases import to_markdown as case_md
        P.append("## 기준 곡선 비교 — Case 1 (전 범위 half-cell) vs Case 2 (격자 곡선)\n")
        P.append("목적함수를 바꾸는 것과 **기준 곡선을 바꾸는 것** 중 어느 쪽이 큰지.\n")
        # F52: 두 artifact의 provenance 판정을 표 바로 위에 싣는다
        cp = case.get("provenance") or {}
        if cp:
            P.append("| artifact | 경로 | provenance |")
            P.append("|---|---|---|")
            for tag, v in cp.items():
                st = "✅ 통과" if v.get("ok") else f"⛔ 실패 — {v.get('fail')}"
                P.append(f"| {tag} | `{v.get('run_dir')}` | {st} |")
            P.append("")
        else:
            P.append("> ⚠ 이 비교표에는 provenance 봉인이 없습니다 (F52 이전 산출물).\n")
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
        # ★ sweep의 optimizer 설정이 본 실행과 다르면 이 절 전체를 인용할 수 없다.
        #   경고 문구는 weight_sweep.yaml이 스스로 달아 두므로 그대로 옮긴다 (F20d).
        if wsweep.get("_경고"):
            P.append(f"> ⚠ **이 sweep의 최적 w를 인용하지 마세요.** {wsweep['_경고']}\n")
        elif not wsweep.get("warm_start", True) or wsweep.get("n_restarts", 0) < 5:
            P.append(f"> ⚠ **이 sweep은 본 실행과 optimizer 설정이 다릅니다** "
                     f"(warm_start={wsweep.get('warm_start')}, "
                     f"n_restarts={wsweep.get('n_restarts')}). 가중치가 아니라 최적화 "
                     f"난이도를 잰 값일 수 있습니다 — `tools/check_sweep_consistency.py`로 "
                     f"본 실행과 대조한 뒤 인용하세요 (F20d).\n")
        else:
            P.append(f"> sweep은 본 실행과 같은 설정으로 돌렸습니다 "
                     f"(warm_start={wsweep.get('warm_start')}, "
                     f"n_restarts={wsweep.get('n_restarts')}). `w=0`은 `pocv_dvdq`와, "
                     f"`w=1`은 `pocv_dvdq_dqdv`와 정의가 같으므로 위 표의 두 끝점은 "
                     f"목적함수 비교표와 일치해야 합니다 — "
                     f"`tools/check_sweep_consistency.py`가 확인합니다.\n")
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
