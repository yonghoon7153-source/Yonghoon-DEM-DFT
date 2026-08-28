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
from dataclasses import dataclass
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


def _cnt(frac, n, digits: int = 2) -> str:
    """★ 15차 발견 2 — **사건 수를 먼저** 쓰고 percent 는 괄호에 넣는다.

    `_pct(1/245, 0)` 은 `0%` 로 반올림한다. 실제로는 245조건 중 1건이고,
    0건이었다면 사건률 비가 유한값이 아니라 무한대여야 한다 — 보고서가 스스로
    모순된 숫자를 실었다. count/denominator 를 잃지 않는 표기로 바꾼다.
    """
    if frac is None or pd.isna(frac) or n is None:
        return "—"
    k = round(float(frac) * int(n))
    return f"{k}/{int(n)} ({100 * float(frac):.{digits}f}%)"


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


def _fit_flags(rs: dict) -> list[str]:
    """서명된 fit `run_spec` → `./run.sh --mode fit` 의 nondefault 플래그.

    ★ 13차 발견 6 / 14차 발견 6 / 14차 3차 발견 4 — 재현 명령은 그 artifact 의
    서명된 설정에서 만든다. 주 fit 과 half-cell 기준 fit 이 같은 규칙을 써야
    "렌더된 절과 같은 signed 조건을 재현한다"가 두 쪽 모두에서 참이 된다.
    """
    out: list[str] = []
    # clean fit(v_col == v_full)은 --clean 없이는 재현되지 않는다 (기본 noisy)
    if rs.get("v_col") == "v_full":
        out.append("--clean")
    if rs.get("objective_order"):
        out.append(f"--objective {','.join(rs['objective_order'])}")
    if rs.get("reference") and rs["reference"] != "grid":
        out.append(f"--reference {rs['reference']}")
    if rs.get("bounds_preset") and rs["bounds_preset"] not in ("expanded",):
        out.append(f"--bounds {rs['bounds_preset']}")
    if rs.get("n_restarts"):
        out.append(f"--n-restarts {rs['n_restarts']}")
    if (rs.get("optimizer") or {}).get("adaptive") is False:
        out.append("--no-adaptive")
    if rs.get("warm_start") is False:
        out.append("--no-warm-start")
    return out


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


def _next_no(lines: list[str]) -> int:
    """다음 결론 번호. ★ 15차 — `len(lines)+1` 은 ⓘ·⚠ 같은 **부속 줄까지** 세서
    번호가 3 다음 5 로 건너뛰었다. `N. ` 로 시작하는 줄만 센다."""
    import re
    return sum(1 for x in lines if re.match(r"^\d+\. ", x)) + 1


@dataclass(frozen=True)
class P22RenderFacts:
    """22p 문장을 만드는 데 필요한 **불변 fact 묶음** (★ 18차 Q4 2층).

    세 층을 분리한다.

      canonical derived metric   `objective_comparison.yaml` 에 봉인되는 수치
      render-only presentation   sealed fits 에서 즉시 재계산되는 표시용 값
      provenance/status          어느 artifact·spec 이 문장을 만들었는가

    이전 판은 렌더 시점에 `cmp_res['verdict_22p']` 를 `.update()` 해서 앞의 두
    층을 한 dict 에 섞었다. 그 dict 를 다시 저장하는 코드가 생기는 순간 봉인
    schema 가 오염된다 — 17차에 실제로 인용 금지 배너를 냈던 경로다. 그래서
    canonical dict 는 **읽기만** 하고, 문장 재료는 여기로 복사해 얼린다.
    """

    objective: str
    noise: float
    radius: float
    radius_fallback: bool
    n_near: int
    gap_thresh: float = 0.06
    n_near_exact_equal: int | None = None
    max_true_pe_ne_gap: float | None = None

    @property
    def known(self) -> bool:
        """참값 구성을 아는가 (구버전 artifact 면 지어내지 않는다)."""
        return (self.n_near_exact_equal is not None
                and self.max_true_pe_ne_gap is not None)

    @classmethod
    def build(cls, verdict: dict, composition: dict | None,
              gap: dict | None = None) -> "P22RenderFacts":
        """canonical verdict + render-only 구성 → 얼린 fact.

        ★ 17차 발견 9 의 불변식(구성과 verdict 가 같은 표본인가)을 **fact 생성
        시점**으로 끌어올린다. 예전에는 문장을 만들다가 뒤늦게 터졌다.
        """
        comp = composition or {}
        n = int(verdict.get("n_near", 0))
        n_comp = comp.get("n_near_composition")
        if n_comp is not None and int(n_comp) != n:
            raise ValueError(
                f"22p 구성이 verdict 와 다른 표본이다 (구성 n={n_comp}, "
                f"verdict n={n}) — selection protocol(radius·noise·objective)이 "
                f"어긋났다")
        return cls(
            objective=str(verdict.get("objective", "pocv_dvdq")),
            noise=float(verdict.get("noise", 0.0)),
            radius=float(verdict.get("radius", 0.021)),
            radius_fallback=bool(verdict.get("radius_fallback")
                                 or comp.get("p22_radius_fallback")),
            n_near=n,
            gap_thresh=float((gap or {}).get("gap_thresh", 0.06)),
            n_near_exact_equal=(None if comp.get("n_near_exact_equal") is None
                                else int(comp["n_near_exact_equal"])),
            max_true_pe_ne_gap=(None if comp.get("max_true_pe_ne_gap") is None
                                else float(comp["max_true_pe_ne_gap"])),
        )


def _denominator_note(cmp_res: dict) -> str:
    """★ 17차 사전 — 결론 4 의 '98·245조건, 22p 는 8조건' 도 상수였다.

    분모가 결론의 해석을 좌우하는데 artifact 와 무관하게 고정돼 있었다.
    """
    base = "pocv_dvdq"
    g = (cmp_res.get("gap_analysis") or {}).get(base) or {}
    v = (cmp_res.get("verdict_22p") or {}).get(base) or {}
    small, wide = g.get("n_small_gap_true"), g.get("n_wide_gap_true")
    n22 = v.get("n_near")
    if small is None or wide is None or n22 is None:
        return "gap 분석과 22p 의 분모는 서로 다르다 — 각 절의 표를 볼 것."
    noise = g.get("noise", 0.0)
    return (f"gap 분석의 분모는 noise={noise:g} 의 {small}·{wide}조건, "
            f"22p 는 {n22}조건으로 각각 다르다.")


def _noise_note(rows) -> str:
    """★ 17차 발견 3 — 노이즈별 서술은 **표에서** 나와야 한다.

    이전 판은 "dQ/dV 의 이점은 노이즈에서 희석된다" 를 무조건 출력했다.
    paired 정본의 실제 방향은 34p−33p 가 noise 0/0.001/0.005 에서
    `+28/+26/+22%p` 로 **어느 noise 에서도 이점이 없다** — 문장이 표와 정반대다.
    """
    by = {}
    for r in rows or []:
        o, n = r.get("objective"), r.get("noise")
        if o in ("pocv_dvdq", "pocv_dvdq_dqdv") and n is not None:
            by.setdefault(float(n), {})[o] = float(r.get("degenerate_frac", float("nan")))
    diffs = {n: v["pocv_dvdq_dqdv"] - v["pocv_dvdq"]
             for n, v in sorted(by.items())
             if "pocv_dvdq" in v and "pocv_dvdq_dqdv" in v}
    if not diffs:
        return ("노이즈 수준별로 나눠 싣는다 — 어느 한 수준의 값만 인용하면 "
                "protocol 의존성이 감춰진다.")
    seq = ", ".join(f"noise {n:g} → {100 * d:+.0f}%p" for n, d in diffs.items())
    worse = all(d > 0 for d in diffs.values())
    better = all(d < 0 for d in diffs.values())
    if worse:
        verdict = ("이 실행에서는 **모든 노이즈 수준에서 34p 의 recovery failure 가 "
                   "더 크다** — 노이즈 0 에서도 34p 의 이점이 관측되지 않는다.")
    elif better:
        verdict = "이 실행에서는 모든 노이즈 수준에서 34p 가 더 낫다."
    else:
        verdict = "노이즈 수준에 따라 **방향이 바뀐다** — 한 수준만 인용하면 안 된다."
    return (f"34p − 33p 의 recovery failure 차이는 {seq} 다. {verdict} "
            f"관측 방향·크기는 noise 수준과 실행 protocol 에 함께 의존하므로 "
            f"표 전체를 함께 본다. 이것은 dQ/dV 의 정보량 우열을 증명하지 않는다 "
            f"— optimizer difficulty 와 분리되지 않았다.")


def _agree_frac_note(adaptive: bool) -> str:
    """★ 17차 발견 4 — fixed-budget 실행에 adaptive 조기 종료 설명을 붙이면 안 된다."""
    head = ("> ⚠ `degeneracy_summary.yaml`의 `restart_conditioned` 블록에 있는 "
            "`agree_frac`과 `p_spread`는 인용하지 마세요. ")
    if adaptive:
        return head + ("adaptive 조기 종료 때문에 `agree_frac`은 restart를 5까지 간 "
                       "조건에서 **정의상 0**이고, `p_spread = 0`은 qualifying restart 가 "
                       "하나였거나 **여러 restart 가 같은 파라미터에 수렴한** 경우 "
                       "모두 가능하므로 단독으로 해석하지 마세요. 위 표가 그 자리를 "
                       "대신합니다.\n")
    return head + ("이 실행은 adaptive 를 끄고 restart 예산을 **고정**했으므로 조기 "
                   "종료는 없습니다. 그럼에도 두 값은 `j_tol`·`p_tol` 판정에 그대로 "
                   "의존하고, `p_spread = 0`은 qualifying restart 가 하나였거나 "
                   "**여러 restart 가 같은 파라미터에 수렴한** 경우 모두 가능하므로 "
                   "단독으로 해석하지 마세요. 위 표가 그 자리를 대신합니다.\n")


def _unrecoverable_note() -> str:
    """★ 17차 발견 6 — 결론에서 완화한 표현이 본문에서 "원리적으로" 로 되돌아갔다.

    실제 분류는 `src/scoring.py` 의 `alpha_true >= 1 - atol` 이라는 **eligibility
    rule** 이다. bounds 전체의 표현 가능성도, 다른 reference·parameterization 의
    불가능성도 검사하지 않는다.
    """
    return ("복원불가군(참 α<1)은 **현재 grid-reference 의 α-window eligibility "
            "rule 밖**이다 (`src/scoring.py`: `alpha_true >= 1 − atol`). 위 표에서 "
            "뺀 근거는 그것이다. 이것은 bounds 전체의 표현 가능성 판정도, 다른 "
            "reference·parameterization 에서의 불가능성 판정도 아니다. 다만 그 "
            "제외가 난이도와 무관하지 않으므로(저LLI에서 복원가능 비율이 훨씬 낮다) "
            "전체군을 같이 싣는다.\n")


def _gap_table_legend() -> str:
    """★ 17차 발견 10-3 — "측정이 아니라 임계 설정의 결과" 는 과도한 단정."""
    return ("- **붕괴에 필요한 격차오차**: 붕괴로 세려면 격차를 6%p에서 2%p 아래로 "
            "끌어내려야 하므로 최소 4%p의 격차 오차가 필요합니다. 이 값이 실측 "
            "격차오차 중앙값보다 크면, **낮은 붕괴율의 일부는 측정이 아니라 오차 "
            "스케일이 임계 간격보다 작다는 사실에서 옵니다** — 관측률 전체가 임계 "
            "설정만의 결과라는 뜻은 아니지만, 그대로 떼어 인용하지 마세요.\n")


def _same_def_overlap_note(sens, tol: float, gap_thresh: float) -> str:
    """★ 17차 자체 발견 — F34 의 두 "같다" 정의가 인용 지점에서 같은 집합인가.

    격자 step 이 0.02 이므로 canonical 하게 `참 격차 < 2%p` 는 `참 격차 == 0` 과
    같은 집합이다. 그러면 민감도 표의 두 패널이 그 열에서 완전히 동일해진다.
    F34 가 두 정의를 나눈 이유는 "exact-zero 는 tol 과 무관한 고정 집합이라
    임계 효과만 분리해 볼 수 있다" 였는데, **인용 지점에서 그 분리가 성립하지
    않는다**. 나란히 싣고 아무 말도 안 하면 독립인 두 확인으로 읽힌다.
    """
    def pick(defn):
        for r in sens or []:
            if (r.get("same_def") == defn
                    and round(float(r.get("tol", -1)), 6) == round(tol, 6)
                    and round(float(r.get("gap_thresh", -1)), 6) == round(gap_thresh, 6)):
                return r
        return None
    a, b = pick("lt_tol"), pick("exact_zero")
    if not a or not b or a.get("n_same") != b.get("n_same"):
        return ""
    return (f"> ⓘ **이 격자에서 두 정의는 인용 지점(`참 격차 ≥ {_pp(gap_thresh, 0)}`, "
            f"`동일 판정 < {_pp(tol, 0)}`)에서 같은 집합이다** — 양쪽 모두 "
            f"{a['n_same']}조건이다. 격자 step 이 2%p 라 `< 2%p` 가 `= 0` 과 "
            f"같아지기 때문이다. 두 패널을 **서로 독립인 두 확인으로 읽지 마세요**; "
            f"정의가 갈리는 것은 `동일 판정` 임계를 3%p 이상으로 넓힐 때부터다.\n")


def _random_only_note(warm_start: bool) -> str:
    """★ 18차 발견 2 — no-warm 실행에 warm-start 인과를 설명하면 안 된다.

    `multistart_random_only` 블록의 **존재**만 보고 warm 전용 문장을 냈다.
    `--no-warm-start` 실행에서 restart 0 은 warm solution 이 아니라
    `base_init`(결정론적 초기값)이다 (`src/fitting.py`).
    """
    if warm_start:
        return ("> 아래 표는 **무작위 restart끼리만** 비교한 것입니다(F21b). "
                "dQ/dV 목적함수는 첫 restart에 매끄러운 해를 초기값으로 받으므로, "
                "그것을 포함하면 최적 J에 닿는 restart가 정의상 하나뿐이 되어 "
                "항상 multimodal로 찍힙니다.\n")
    return ("> 아래 표는 **무작위 restart끼리만** 비교한 것입니다(F21b). "
            "이 실행은 warm start 를 껐으므로 restart 0 은 **결정론적 "
            "`base_init`** 입니다 — 목적함수마다 같은 초기값에서 출발하는 그 "
            "restart 를 빼고 무작위 restart 만 견줍니다.\n")


def _objective_section_heading(n_objectives: int) -> str:
    """★ 18차 발견 2 — 제목의 종수를 **표에서** 센다 (paired 는 2종이다)."""
    return f"## 목적함수 {int(n_objectives)}종 비교"


def _reproduction_scope_note(has_wsweep: bool, has_halfcell: bool,
                             has_hessian: bool, warm_start: bool) -> str:
    """★ 18차 발견 4 — 재현 범위를 **실제로 출력한 명령**에서 만든다.

    이전 판은 고정 boilerplate 라, sweep·half-cell 절이 없는 paired 보고서도
    그 설정을 복원한다고 썼고, Hessian 은 명령 전체가 빠졌는데 "비기본 eps" 만
    미출력 축인 것처럼 읽혔다.
    """
    covered = ["fit(objective·restart·clean/noisy·adaptive·warm start·"
               "reference·bounds preset)"]
    missing = []
    if has_wsweep:
        covered.append("weight sweep(w_grid·stride·restart)")
        missing.append("sweep 의 bounds·reference·tol·optimizer method")
    if has_halfcell:
        covered.append("half-cell 기준 곡선(method) 과 Case 1↔2 비교")
    note = ("> **재현 범위**: 위 명령은 이 산출물의 서명된 "
            + " · ".join(covered) + " 설정을 복원합니다.")
    if has_hessian:
        missing.append("**Hessian 절 전체**(기본 eps 포함 — 명령을 싣지 않습니다)")
    if not warm_start:
        note += (" 이 실행은 warm start 를 끄고 restart 예산을 고정했으므로 "
                 "그 축도 명령에 포함돼 있습니다.")
    if missing:
        note += (" 아직 명령으로 내보내지 않는 축은 " + " · ".join(missing)
                 + " 입니다 — 해당 절은 `manifest.yaml` 의 `run_spec` 을 직접 "
                   "보고 맞춰야 합니다.")
    return note + "\n"


def _p22_composition(v, g: dict | None = None) -> dict:
    """★ 16차 발견 4 (17차 사전) — 22p 근방 표본의 **참값 구성**을 문장으로.

    이전 판은 "절반은 PE=NE, 절반은 |ΔLAM|=2%p", "wide-gap 은 하나도 없다" 를
    문자열 상수로 박아 두었다. v4 격자에서는 우연히 맞지만 반경·step·noise 를
    바꾸면 provenance 통과 배지를 단 채 거짓을 말한다. 전부 verdict_22p 가
    보고한 count 에서 만든다.
    """
    # ★ Q4 2층 — dict 를 받으면 그 자리에서 얼린 fact 로 승격한다 (호출부
    #   호환용). 이미 P22RenderFacts 면 그대로 쓴다.
    f = v if isinstance(v, P22RenderFacts) else P22RenderFacts.build(v, v, g)
    n = f.n_near
    thr = f.gap_thresh
    if not f.known:
        # 구버전 artifact — 구성을 모른다. 지어내지 않고 모른다고 쓴다.
        return {"known": False,
                "headline": f"이 {n}점의 참값 구성은 이 artifact 에 기록되어 있지 않다",
                "detail": "구버전 `verdict_22p` 라 구성을 인용하려면 재생성이 필요하다",
                "wide": f"wide-gap(≥{_pp(thr, 0)}) 포함 여부를 확인할 수 없으므로"}
    # (표본 일치 불변식은 P22RenderFacts.build 에서 이미 강제된다 — 17차 발견 9)
    k = f.n_near_exact_equal
    mx = f.max_true_pe_ne_gap
    if k >= n:
        headline = f"이 {n}점은 참값이 모두 LAM_PE = LAM_NE 다"
        detail = f"PE=NE 가 {k}/{n} 이고 최대 참 격차가 {_pp(mx)} 다"
    else:
        headline = f"이 {n}점은 참값이 모두 같은 격자점이 아니다"
        detail = (f"PE=NE 가 {k}/{n}, |ΔLAM|>0 이 {n - k}/{n} 이고 "
                  f"최대 참 격차가 {_pp(mx)} 다")
    # ★ 18차 발견 9 — 여기만 raw `<` 를 쓰고 있었다. 공통 규약을 쓴다.
    from tools.compare_objectives import gap_ge as _gap_ge
    wide = (f"여기에 wide-gap(≥{_pp(thr, 0)})은 **하나도 없으므로**"
            if not bool(_gap_ge(mx, thr))
            else f"여기에 wide-gap(≥{_pp(thr, 0)})이 섞여 있으나 n={n} 의 국소 "
                 f"표본이므로")
    return {"known": True, "headline": headline, "detail": detail, "wide": wide}


def _conclusion(cmp_res: dict, summary: dict, fits=None,
                p22_facts: dict | None = None) -> list[str]:
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
        # ★ 15차 발견 1 — 정수 반올림(62→87)이 비대칭 pipeline 값(62→63)과
        #   헷갈리는 통로가 됐다. count 와 소수 한 자리를 함께 낸다.
        lines.append(
            f"1. dQ/dV 항을 넣으면 recovery failure 가 "
            f"{_cnt(b['degenerate_frac'], b['n'], 1)} → "
            f"{_cnt(i['degenerate_frac'], i['n'], 1)} 로 {verdict} "
            f"(행별 max-mode 절대오차의 평균 {_pp(b['mean_abs_err'])} → "
            f"{_pp(i['mean_abs_err'])}, "
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
    #   22p 근방 격자점은 참 격차가 작아 "복원값도 같더라"가 증거가 안 된다.
    g = cmp_res.get("gap_analysis", {}).get(base, {})
    if g and "error" not in g and "gap_collapse_frac" in g:
        collapse, split = g["gap_collapse_frac"], g.get("false_split_frac")
        # ★ 15차 발견 2 — count 를 먼저 쓴다. `_pct(1/245, 0)` 은 0% 로 반올림해
        #   "붕괴 없음" 으로 읽혔고, 그 값과 우도비 90 이 서로 모순이었다.
        n_wide = g.get("n_wide_gap_true")
        n_small = g.get("n_small_gap_true") or g.get("n_narrow_gap_true")
        fact = (f"2. 참값이 뚜렷이 다른 조건(|ΔLAM|_true ≥ {_pp(g['gap_thresh'], 0)})에서 "
                f"fitting이 두 전극을 같다고 답한 것은 "
                f"**{_cnt(collapse, n_wide)}** 다. "
                f"참 격차 {_pp(g['mean_true_gap_wide'])} → 복원 격차 "
                f"{_pp(g['mean_recovered_gap_wide'])}, shrinkage {g['shrinkage']:.2f}. ")
        lr = g.get("likelihood_ratio_equal")
        if lr is not None and split is not None:
            # ★ 15차 발견 3·6 — "우도비" 라는 무조건적 표현 대신 조건부임을 이름에
            #   박고, 전체 격자 값을 **같은 문단에** 병기한다.
            _all = ((cmp_res.get("gap_analysis_all_conditions") or {}).get(base) or {})
            fact += (f"\n\n   이 관측이 어느 쪽을 지지하는지 **동일가중 합성격자의 "
                     f"조건부 사건률 비**로 보면 (population="
                     f"{g.get('population', 'recoverable')})\n\n"
                     f"   > P(같다고 답 | 참 격차 < {_pp(g['tol'], 0)}) = "
                     f"{_cnt(1 - split, n_small)}\n"
                     f"   > P(같다고 답 | 참 격차 ≥ {_pp(g['gap_thresh'], 0)}) = "
                     f"{_cnt(collapse, n_wide)}\n"
                     f"   > 사건률 비 = {lr:.1f}")
            if _all.get("likelihood_ratio_equal") is not None:
                # ★ 17차 발견 10-1 — 반대쪽 분자(작은-격차에서 "같다")를 함께
                #   내지 않으면 핵심 결론만으로 사건률 비를 검산할 수 없다.
                _asm = (f"{_cnt(1 - _all['false_split_frac'], _all['n_small_gap_true'])}"
                        if _all.get("false_split_frac") is not None
                        and _all.get("n_small_gap_true") else None)
                fact += (f"\n\n   같은 지표를 **전체 생성성공 격자**(population=all)에서 "
                         f"재계산하면 작은 격차에서 \"같다\" "
                         f"{_asm or '(분자 미기록)'}, 넓은 격차 붕괴 "
                         f"{_cnt(_all.get('gap_collapse_frac'), _all.get('n_wide_gap_true'))}, "
                         f"사건률 비 **{_all['likelihood_ratio_equal']:.2f}** 다. "
                         f"즉 위 값은 복원가능군 선택에 강하게 의존한다 — "
                         f"두 값을 **함께** 인용하지 않으면 안 된다.")
            # ★ 이 값을 결론으로 승격시키지 않는다. 아래 세 제약을 같은 문단에 붙인다.
            lo, hi = g.get("lr_sensitivity_min"), g.get("lr_sensitivity_max")
            med = g.get("lr_sensitivity_median")
            fact += "\n\n   **이 값을 '두 전극이 실제로 비슷하다'로 읽을 수 없다.** 세 가지 때문이다.\n"
            if lo is not None:
                spike = g.get("lr_is_local_spike")
                # ★ 18차 발견 8 — 이 범위는 `<tol` 패널에서만 계산된다. 보고서는
                #   exact-zero 패널도 함께 싣고 그쪽 최대값이 다르므로, 한 범위를
                #   전체 민감도 범위처럼 쓰면 안 된다.
                _ez = g.get("lr_sensitivity_max_exact_zero")
                _ez_txt = (f" (이 범위는 첫 `<tol` 정의 패널의 값이다 — exact-zero "
                           f"정의 패널은 별도로 최대 {_ez:.1f} 였다)"
                           if _ez is not None else
                           " (이 범위는 첫 `<tol` 정의 패널의 값이다)")
                fact += (f"\n   1. **임계 의존** — 같은 데이터에서 (참격차, 동일판정) 임계를 "
                         f"흔들면 사건률 비가 {lo:.1f}~{hi:.1f}(중앙값 {med:.1f})로 움직인다"
                         f"{_ez_txt}. "
                         + ("현재 조합은 이웃보다 유독 높은 **국소 봉우리**다 — 이 값을 "
                            "대표값으로 인용하면 사후선택이 된다. "
                            if spike else "")
                         + "아래 임계 민감도 표를 함께 볼 것.\n")
            fact += ("\n   2. **posterior가 아님** — 이건 두 합성 가설 아래의 *사건률 비*다. "
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
            # ★ 18차 발견 1 — "붕괴가 원리적으로 관측 가능한 범위" 는 삭제했다.
            #   같은 결과에서 뽑은 오차분포로 그 결과의 낮은 사건률을 방어하는
            #   순환 논리였고, 부호·행별 필요량을 버린 지표에 기대고 있었다.
            #   남기는 것은 **부호 있는 행별 여유의 기술통계**뿐이다.
            if "collapse_margin_median" in g:
                fact += (f"부호를 살려 행별로 보면 복원 격차가 판정 임계까지 "
                         f"남긴 여유(= tol − 복원 격차)는 중앙값 "
                         f"{_pp(g['collapse_margin_median'])}·최대 "
                         f"{_pp(g['collapse_margin_max'])} 이고, 넓은 격차 "
                         f"{g.get('n_wide_gap_true', '?')}조건 중 격차가 줄어든 "
                         f"방향은 {g.get('n_wide_gap_toward_collapse', '?')}조건이다. "
                         f"이 값들은 **기술통계일 뿐, 붕괴가 관측 가능했다는 "
                         f"근거가 아니다** — 같은 결과에서 뽑은 오차분포로 그 "
                         f"결과의 낮은 사건률을 방어할 수 없다. 낮은 사건률의 "
                         f"견고성은 아래 임계 민감도 표와 모집단 제한으로만 "
                         f"판단할 것.")
        lines.append(fact)

    v = cmp_res.get("verdict_22p", {}).get(base, {})
    if v and "error" not in v:
        anti = v.get("pe_ne_antisym_frac", 0)
        gap_t, gap_r = v.get("true_pe_ne_gap"), v.get("recovered_pe_ne_gap")
        # ★ Q4 2층 — 얼린 fact 가 있으면 그것만 쓴다 (canonical v 는 읽기 전용)
        comp = _p22_composition((p22_facts or {}).get(base) or v, g)
        # ★ 15차 발견 7 — 이 값은 artifact·목적함수·noise·반경·임계에 모두
        #   조건부다. count 를 먼저 쓰고 조건을 문장에 박는다.
        lines.append(
            f"3. **22p 조건(LAM_PE≈LAM_NE≈13%, LLI≈17%) 근방의 recovery failure 는 "
            f"{_cnt(v['degenerate_frac'], v['n_near'])}** "
            f"(목적함수 `{base}`, noise={v.get('noise', 0):g}, "
            # ★ 19차 사전 발견 3 — fallback 이면 "radius 안" 은 거짓이다.
            #   radius 밖 최근접 1점으로 대체됐음을 그대로 쓴다.
            + (f"radius={v.get('radius', 0.021):g} 안에 조건이 없어 radius **밖** "
               f"최근접 {v['n_near']}점으로 대체, "
               if v.get('radius_fallback') else
               f"radius={v.get('radius', 0.021):g} 안의 최근접 {v['n_near']} grid 조건, ")
            + f"raw max-mode 오차 > {_pp(g.get('tol', 0.02), 0) if g else '2%p'} 임계) "
            f" — 행별 max-mode 절대오차의 평균 {_pp(v['mean_abs_err'])}, "
            f"raw PE/NE 오차 반대부호 비율 {_pct(anti)}, "
            f"참 PE-NE 격차 {_pp(gap_t)} → 복원 격차 {_pp(gap_r)}. "
            f"⚠ **{comp['headline']}** — {comp['detail']}. 평균 참 격차는 "
            f"{_pp(gap_t)} 다. {comp['wide']}, 이 표본으로는 \"참 격차가 큰 조건이 "
            f"'같다'로 붕괴하는가\" 를 물을 수 없다 — 그 질문의 답은 위 2번이다. "
            f"이 {v['n_near']}개는 실제 셀이 아니라 설계 격자의 최근접 점이며, "
            f"임계·반경·noise·목적함수를 바꾸면 값이 달라진다.")

    # ★ F33 — Hessian은 결론에서 뺐다. `pe_ne_coupled`는 평평한 방향에서 α_PE와
    #   α_NE가 **같은 부호**인지를 세는데, 22p 가설(한쪽 과대·다른쪽 과소)은
    #   LAM에서 부호가 반대이고 α = (1−LAM)/r 이므로 α에서도 반대다. 즉 지표가
    #   묻는 질문이 가설과 다르다. (반대부호 방향도 재보니 0.0~0.5%였지만,
    #   eps 미수렴·안장점 혼입 때문에 어느 쪽으로도 근거가 못 된다.)

    ur = cmp_res.get("unrecoverable_frac", 0.0)
    # ★ 15차 발견 9 — "원리적으로 복원 불가" 는 실제 셀·다른 reference·다른
    #   parameterization 까지 확장되는 물리 명제로 읽힌다. 지금 판정하는 것은
    #   **선택한 grid-reference 의 α-window eligibility criterion** 이다.
    #   ★ 18차 발견 3 — `classify_recoverability()` 는 `alpha_true >= 1 − atol`
    #   두 개만 본다. configured box bounds 도 β 도 물리 feasible domain 도
    #   보지 않으므로 `α/bounds feasible domain` 은 그보다 넓은 주장이다.
    lines.append(
        f"{_next_no(lines)}. **생성성공 격자의 {_pct(ur)}는 선택한 grid-reference "
        f"의 현재 α-window eligibility criterion 을 통과하지 못한다**"
        f"(`src/scoring.py`: `alpha_true >= 1 − atol`). 이 판정은 설정된 box "
        f"bounds 도, β 도, 물리적 표현 가능성도 검사하지 않는다 — 두 α 값 "
        f"하나만 본다. 위 숫자는 모두 "
        f"그 안쪽 **목적함수당 {int((summary.get('n_rows_recoverable') or 0) / max(len(tbl.index), 1))}조건** "
        f"에서만 센 값이며(파일의 objective-condition 행 합계는 "
        f"{summary.get('n_rows_recoverable', '?')}), 바깥을 섞으면 목적함수 간 "
        f"차이가 묻힌다. 이는 데이터의 물리 속성이 아니라 **현재 채점 규칙의 "
        f"자격 판정**이다. **단 위 2번의 전체 생성성공 격자 값(population=all)은 이 "
        f"안쪽 바깥을 함께 센 예외다.** " + _denominator_note(cmp_res))
    return lines


def _recheck_derived(in_dir: Path, name: str, repo_root=None) -> dict | None:
    """★ F69 — 파생 YAML 의 숫자를 **fits 에서 다시 계산해** 대조한다.

    보고서는 저장된 YAML 을 그대로 렌더한다. 그래서 비율 한 개만 고쳐도
    (`0.944444 → 0.123456`) 보고서가 12% 를 싣고 인용 금지 배너는 뜨지 않았다.
    저장된 `ok`·digest 는 자기신고이므로 믿지 않는다.

    반환 None = 그 파일이 없음 (검사 대상 아님).
    """
    import math

    y = _load(in_dir / name)
    if not y:
        return None
    try:
        if name == "case_comparison.yaml":
            from tools.compare_cases import compare
            prov = y.get("provenance") or {}
            if set(prov) != {"grid", "halfcell"}:
                return {"ok": False, "why": "provenance tag 가 불완전해 재계산할 수 없다"}
            now = compare(Path(prov["grid"]["scored_file"]),
                          Path(prov["halfcell"]["scored_file"]),
                          repo_root=repo_root)   # ★ 16차 발견 1
            # ★ 10차 발견 5 — 세 지표만 짝짓던 방식은 `n_conditions_common` 등
            #   나머지 숫자의 변조(999999)를 그대로 통과시켰고, 보고서가 그 값을
            #   렌더했다 (리뷰 실측). key 집합 + 숫자 **전체**를 대조하고,
            #   호출 쪽이 재계산본을 렌더 원본으로 쓰도록 함께 돌려준다.
            ok = _numbers_equal(y, now)
            return {"ok": ok, "now": now,
                    "why": "" if ok else "저장본 숫자가 fits 재계산과 다르다"}
        else:
            # ★ map 이 아니라 **정본 fits 에서 다시 채점**해 대조한다.
            #   degeneracy_map.parquet 자체가 변조된 경우까지 잡기 위해서다.
            from tools.compare_cases import _scored
            from tools.compare_objectives import run_compare
            now = run_compare(in_dir, write=False,
                              df=_scored(in_dir / "fits.parquet", 0.02))
            pairs = _flat_pairs(y, now)
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "why": f"재계산 실패: {e}"}

    bad = [(a, b) for a, b in pairs
           if a is None or b is None
           or not math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=1e-12)]
    return {"ok": not bad,
            "why": "" if not bad else
                   f"{len(bad)}개 값이 다르다 (예: 저장 {bad[0][0]} vs 재계산 {bad[0][1]})"}


def _flat_pairs(saved, now, path=""):
    """중첩 구조의 **숫자만** 짝지어 뽑는다 (문자열 주석·경로는 제외).

    ★ F77 — list 를 건너뛰던 것이 발견 6 의 통로였다. `objective_comparison` 의
    핵심 `table` 들이 전부 list of dict 라 변조가 통과했다. 길이가 다르면
    (None, "길이불일치") 쌍을 넣어 반드시 실패하게 한다.
    """
    out = []
    if isinstance(saved, dict) and isinstance(now, dict):
        for k in saved:
            if isinstance(k, str) and k.startswith("_"):
                continue          # 주석·주의 문구
            if k in ("provenance", "provenance_ok", "공통_run_spec", "figures"):
                continue
            out += _flat_pairs(saved[k], now.get(k), f"{path}.{k}")
    elif isinstance(saved, (list, tuple)):
        if not isinstance(now, (list, tuple)) or len(saved) != len(now):
            out.append((None, f"길이불일치@{path}"))
        else:
            for i, (a, b) in enumerate(zip(saved, now)):
                out += _flat_pairs(a, b, f"{path}[{i}]")
    elif isinstance(saved, bool):
        out.append((int(saved), int(now) if isinstance(now, bool) else now))
    elif isinstance(saved, (int, float)):
        out.append((saved, now))
    return out


#: ★ 11차 발견 5 — 정의가 **글자 그대로 같은** sweep 끝점 ↔ 본 실행 목적함수.
#: (`tools/check_sweep_consistency.DEFAULT_PAIRS` 와 같은 쌍)
_ENDPOINT_PAIRS = (("wdqdv_0.00", "pocv_dvdq"),
                   ("wdqdv_1.00", "pocv_dvdq_dqdv"))


def _norm_weights(w):
    """목적함수 가중치 dict 를 비교 가능한 정규형으로 (없는 항 = 0.0).

    `pocv_dvdq` 는 `w_dqdv` 키가 아예 없고 `wdqdv_0.00` 은 `w_dqdv: 0.0` 을
    명시한다 — 정의는 같은데 dict 는 다르다. 채워서 비교한다.
    """
    if not isinstance(w, dict):
        return None
    return {k: float(w.get(k, 0.0)) for k in ("w_pocv", "w_dvdq", "w_dqdv")}


def _numbers_equal(saved, now) -> bool:
    """저장본과 재계산본의 숫자가 전부 일치하는가 (F77 stale 판정).

    ★ F87/9차 발견 8 — `_flat_pairs` 는 **저장본의 key 를 중심으로** 순회한다.
    저장본이 빈 mapping 이면 비교할 쌍이 0개라 "일치"로 판정됐다. 표 숫자는
    재계산본을 렌더하므로 직접 오염은 없지만, **저장본이 현재 fits 에 대응한다는
    보장이 사라진다.** 양쪽 key 집합의 동일성을 먼저 본다.
    """
    import math

    def _keys(x, path=""):
        out = set()
        if isinstance(x, dict):
            for k in x:
                if isinstance(k, str) and (
                        k.startswith("_") or k in ("provenance", "provenance_ok",
                                                   "공통_run_spec", "figures")):
                    continue
                out.add(f"{path}.{k}")
                out |= _keys(x[k], f"{path}.{k}")
        elif isinstance(x, (list, tuple)):
            out.add(f"{path}[len={len(x)}]")
            for i, v in enumerate(x):
                out |= _keys(v, f"{path}[{i}]")
        return out

    if _keys(saved) != _keys(now):
        return False
    for a, b in _flat_pairs(saved, now):
        if a is None or b is None or isinstance(b, str):
            return False
        try:
            if not math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=1e-12):
                return False
        except (TypeError, ValueError):
            return False
    return True


def build(in_dir, out_path="docs/RESULTS.md", repo_root=".") -> Path:
    """★ F77/8차 발견 6 — 보고서는 **정본 fits 에서 재계산한 값**을 렌더한다.

    예전에는 저장된 YAML 을 그대로 렌더하고 재검산(`_recheck_derived`)은 dict
    스칼라만 봤다. 핵심 표(`table`·`table_all_conditions`·`table_by_noise`)는
    **list** 라 순회에서 빠졌고, `degeneracy_summary`·sweep 은 재검산 자체가
    없었다. 리뷰 실측: `0.944→0.123456` 표 변조, `n_rows_recoverable→987654`,
    `optimum w→123.456` 전부 녹색 보고서에 그대로 실렸다.

    이제 렌더 원본이 재계산 결과이므로 저장 YAML 을 바꿔도 보고서 숫자는 안
    바뀐다. 저장본이 재계산과 다르면(=stale/변조) 인용 금지 배너 사유에 싣는다 —
    YAML 을 직접 읽는 다른 소비자가 있기 때문이다.
    """
    import math
    import tempfile

    in_dir, repo_root = Path(in_dir), Path(repo_root)
    saved_cmp = _load(in_dir / "objective_comparison.yaml")
    if saved_cmp is None:
        raise SystemExit(f"{in_dir}/objective_comparison.yaml 없음 — "
                         f"먼저 python tools/compare_objectives.py --in {in_dir}")
    stale: list[str] = []
    # ★ 17차 발견 2 — nested wsweep 검증 결과를 header 검사 목록에 노출한다.
    #   지금까지는 실패하면 stale 로만 새고, 통과했을 때 "검증 범위에 wsweep 이
    #   들어 있었는가" 를 문서만 보고 확인할 수 없었다.
    wsweep_prov: dict | None = None
    #: ★ Q4 2층 — objective → P22RenderFacts (canonical 과 분리된 층)
    p22_facts: dict = {}

    saved_summary = _load(in_dir / "degeneracy_summary.yaml") or {}
    manifest = _load(in_dir / "manifest.yaml") or {}
    saved_ws = _load(in_dir / "wsweep" / "weight_sweep.yaml")

    cmp_res, summary, wsweep = saved_cmp, saved_summary, saved_ws
    # 10차 발견 4/5 — sweep 렌더·판정에 쓰는 검증 원본 (기본: 검증 불가 상태)
    sweep_vs_main: list[str] | None = None   # None = 대조 자체를 못 했다
    wspec_verified: dict = {}
    can_recompute = (in_dir / "fits.parquet").exists()
    if not can_recompute:
        # 정본이 없으면 재계산도 없다 — 저장본을 렌더하되 **인용 금지**를 강제한다
        stale.append("재계산_불가(fits.parquet 없음)")
    else:
        try:
            from tools.compare_cases import _scored as _scored_fn
            from tools.compare_objectives import run_compare as _rc
            _scored_df = _scored_fn(in_dir / "fits.parquet", 0.02)
            cmp_res = _rc(in_dir, write=False, df=_scored_df)
            # figures 는 계산 산출물이 아니라 그림 경로 목록 — 저장본에서만 온다
            if isinstance(saved_cmp, dict) and saved_cmp.get("figures"):
                cmp_res["figures"] = saved_cmp["figures"]
            if (in_dir / "objective_comparison.yaml").exists() \
                    and not _numbers_equal(saved_cmp, cmp_res):
                stale.append("objective_comparison.yaml")
            # ★ 17차 사전 — 22p 근방의 참값 구성은 **렌더 전용 파생값**이다.
            #   verdict_22p 의 반환에 넣었더니 봉인된 objective_comparison.yaml
            #   과 key 집합이 달라져 F87 이 stale 을 올렸다(v4 재생성에서 인용
            #   금지 배너 실측). 그러므로 **stale 대조가 끝난 뒤에** 주입한다.
            from tools.compare_objectives import p22_truth_composition as _p22c
            # ★ 18차 Q4 2층 — canonical dict 는 **읽기만** 한다. 렌더 재료는
            #   얼린 fact 로 따로 만든다 (예전엔 여기서 `.update()` 했다).
            #   ★ 17차 발견 9 — **기록된** radius 를 쓴다 (기본값 재사용 금지)
            for _o, _v in (cmp_res.get("verdict_22p") or {}).items():
                if isinstance(_v, dict) and "error" not in _v:
                    _comp = _p22c(_scored_df, _o, _v.get("noise", 0.0),
                                  _v.get("radius", 0.021))
                    p22_facts[_o] = P22RenderFacts.build(
                        {**_v, "objective": _o}, _comp,
                        (cmp_res.get("gap_analysis") or {}).get(_o))
        except Exception as e:  # noqa: BLE001
            cmp_res = saved_cmp
            stale.append(f"objective_comparison.yaml (재계산 실패: {e})")
        try:
            from src.scoring import run_scoring as _rs
            with tempfile.TemporaryDirectory() as _td:
                summary = _rs(in_dir, out_dir=_td, tol=0.02, repo_root=repo_root)
            # ★ F87 — `saved_summary` 가 빈 dict 면 falsy 라 **조건 자체를
            #   건너뛰었다** — 발견 8 이 지적한 형태 그대로다. 파일 존재로 본다.
            if (in_dir / "degeneracy_summary.yaml").exists() \
                    and not _numbers_equal(saved_summary, summary):
                stale.append("degeneracy_summary.yaml")
        except Exception as e:  # noqa: BLE001
            summary = saved_summary
            stale.append(f"degeneracy_summary.yaml (재계산 실패: {e})")
        if saved_ws and (in_dir / "wsweep" / "fits.parquet").exists():
            try:
                from src.scoring import (add_error_columns, apply_bias_correction,
                                         classify_recoverability, clean_bias)
                from src.weight_sweep import pick_optimum, sweep_summary
                _tol = float(saved_ws.get("tol", 0.02))
                _sw = classify_recoverability(add_error_columns(
                    pd.read_parquet(in_dir / "wsweep" / "fits.parquet"), _tol))
                _sw = apply_bias_correction(_sw, clean_bias(_sw), _tol)
                opt_now = pick_optimum(sweep_summary(_sw, _tol))
                if not _numbers_equal(saved_ws.get("optimum"), opt_now):
                    stale.append("wsweep/weight_sweep.yaml")
                wsweep = dict(saved_ws, optimum=opt_now)   # 렌더는 재계산 값으로
            except Exception as e:  # noqa: BLE001
                stale.append(f"wsweep/weight_sweep.yaml (재계산 실패: {e})")
                wsweep = None
            # ★ F88/9차 발견 6 — sweep 은 **자기 provenance 를 갖는 실행**이다.
            #   optimum 만 재계산하고 nested validator·metadata 대조를 안 하면,
            #   보고서만으로 sweep 의 설정·표본 수·optimizer 조건을 확정할 수 없다.
            from src.io import validate_provenance as _vp
            # ★ 17차 발견 2 — 여기서 repo_root 가 끊겨 있었다. 격리 root 로
            #   복원한 보고서에서도 이 검증만 **원본 저장소**를 봤다.
            _wv = _vp(in_dir / "wsweep", repo_root=repo_root)
            wsweep_prov = _wv                    # header 검사 목록에 노출한다
            if not _wv["ok"]:
                stale.append(f"wsweep provenance ({_wv['fail'][:3]})")
            _wman = _load(in_dir / "wsweep" / "manifest.yaml") or {}
            _wspec = _wman.get("run_spec") or {}
            _meta_bad = []
            if saved_ws.get("n_restarts") != _wspec.get("n_restarts"):
                _meta_bad.append("n_restarts")
            _wopt = _wspec.get("optimizer") or {}
            for k in ("method", "adaptive"):
                if saved_ws.get(k) is not None and saved_ws.get(k) != _wopt.get(k):
                    _meta_bad.append(k)
            if saved_ws.get("n_conditions") != _wspec.get("n_conditions"):
                _meta_bad.append("n_conditions")
            # ★ 10차 발견 4 — 자기신고 w_grid 를 **서명된 spec 의 목적함수
            #   이름**(wdqdv_X.XX)에서 재구성해 대조한다. 이름은 run_sig 에
            #   들어가므로 위조하면 행 서명이 갈린다.
            _w_names_want = {f"wdqdv_{float(w):.2f}"
                             for w in (saved_ws.get("w_grid") or [])}
            _w_names_got = {str(n) for n in (_wspec.get("objectives") or {})
                            if str(n).startswith("wdqdv_")}
            if _w_names_want != _w_names_got:
                _meta_bad.append(
                    f"w_grid(기록 {sorted(_w_names_want)} ≠ "
                    f"spec {sorted(_w_names_got)})")
            if _meta_bad:
                stale.append(f"wsweep metadata 불일치 ({_meta_bad})")
            # ★ 10차 발견 4/F20d — "본 실행과 같은 설정" 문장을 **자기신고가
            #   아니라 두 run_spec 의 대조**로 판정한다. 예전에는 weight_sweep.yaml
            #   의 warm_start·n_restarts 만 보고 초록 문장을 실었다.
            _mspec = manifest.get("run_spec") or {}
            _mopt = _mspec.get("optimizer") or {}
            sweep_vs_main = []
            for k in ("method", "adaptive"):
                if _mopt.get(k) != _wopt.get(k):
                    sweep_vs_main.append(
                        f"optimizer.{k}({_mopt.get(k)}≠{_wopt.get(k)})")
            for k in ("n_restarts", "warm_start", "reference", "v_col",
                      "bounds_preset"):
                if _mspec.get(k) != _wspec.get(k):
                    sweep_vs_main.append(
                        f"{k}({_mspec.get(k)}≠{_wspec.get(k)})")
            # ★ 11차 발견 5 — **같은 실험인가**를 먼저 본다. 예전에는 optimizer
            #   축만 봐서, sweep 이 아예 다른 곡선으로 돌아도(curves_sha 불일치)
            #   "본 실행과 같은 설정" 초록 문장이 실렸다 (리뷰 실측).
            for k in ("curves_sha", "producer_sha", "base_config_sha",
                      "source_digest", "env", "inventory", "obj_cfg"):
                if _mspec.get(k) != _wspec.get(k):
                    sweep_vs_main.append(f"{k} 불일치")
            # 끝점 목적함수의 **정의 동치** (이름이 아니라 가중치 dict)
            for _wname, _mname in _ENDPOINT_PAIRS:
                a = _norm_weights((_wspec.get("objectives") or {}).get(_wname))
                b = _norm_weights((_mspec.get("objectives") or {}).get(_mname))
                if a is None or b is None:
                    sweep_vs_main.append(f"끝점 {_wname}↔{_mname} 한쪽이 없다")
                elif a != b:
                    sweep_vs_main.append(f"끝점 정의 {_wname}({a})≠{_mname}({b})")
            # tol — 보고서 전체 재계산이 0.02 를 쓰므로 sweep 도 같아야
            # 이 절의 비율을 다른 절과 나란히 읽을 수 있다
            _ws_tol = float(saved_ws.get("tol", 0.02))
            if abs(_ws_tol - 0.02) > 1e-12:
                sweep_vs_main.append(f"tol({_ws_tol}≠0.02)")
            # ★ 11차 발견 5 — 설정 대조만으로는 "같은 답을 낸다"가 증명되지
            #   않는다. 정의가 같은 두 끝점을 **실제 결과로** 대조한다
            #   (`tools/check_sweep_consistency.py`). 보고서가 "이 도구가
            #   확인한다"고 써 왔지만 아무도 호출하지 않았다.
            try:
                from tools.check_sweep_consistency import run_check
                _chk = run_check(in_dir / "wsweep", in_dir, tol=_ws_tol)
                # ★ 12차 발견 3 — 판정은 조건 coverage + 조건별 수치 동일성이다
                #   (다수결·5%p 허용이 아니다). checker 가 이미 그렇게 낸다.
                _bad_pairs = [f"{p['sweep_objective']}↔{p['main_objective']}"
                              f"({str(p.get('판정', ''))[:60]})"
                              for p in _chk["pairs"] if not p.get("일치")]
                if _bad_pairs:
                    sweep_vs_main.append(f"끝점 결과 불일치: {_bad_pairs}")
            except Exception as e:  # noqa: BLE001
                sweep_vs_main.append(f"끝점 일치 확인 실패({type(e).__name__})")
            wspec_verified = _wspec       # 렌더는 서명된 spec 값으로 (발견 5)
        elif saved_ws:
            stale.append("wsweep/weight_sweep.yaml (fits.parquet 없음 — 재계산 불가)")
            wsweep = None
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
    # ★ 12차 발견 7 — paired(공정) 실행에서 만든 보고서는 **어떤 protocol 의
    #   결과인지**를 문서 스스로 밝혀야 한다. 기본 RESULTS 는 비대칭 pipeline
    #   (adaptive 조기 종료 + warm start 연쇄) 결과라 결론 2 의 해석이 다르다.
    _mopt0 = (manifest.get("run_spec") or {}).get("optimizer") or {}
    _mspec0 = manifest.get("run_spec") or {}
    if _mopt0.get("adaptive") is False and _mspec0.get("warm_start") is False:
        P.append(
            "> ## 이 문서의 protocol — 공정 paired 비교\n"
            "> \n"
            f"> `--no-adaptive --no-warm-start`, restart {_mspec0.get('n_restarts')}개 "
            f"고정, 목적함수 {list(_mspec0.get('objective_order') or [])}.\n"
            "> 모든 조건이 **같은 restart index 집합**을 끝까지 돌고, 목적함수 간 "
            "warm start 연쇄가 없다 (F66/F86).\n"
            "> \n"
            "> 기본 `docs/RESULTS.md` 는 adaptive 조기 종료 + warm start 연쇄가 있는 "
            "**비대칭 pipeline** 결과다. 목적함수 간 비교(결론 2)는 이 문서의 값을 "
            "쓰고, 기본 문서의 multi-start 수치와 섞지 말 것.\n")

    # ★ F35 — provenance가 없는 artifact에서 생성됐으면 문서 맨 위에 인용 금지
    #   배너를 박는다. 회답을 별도 문서에만 두면 저장소를 여는 사람은 철회 전
    #   결론을 먼저 본다.
    # 열 존재 여부만 보면 임의의 문자열 하나로 배너가 사라진다 (F38).
    from src.io import validate_provenance
    # ★ 16차 발견 1 — 격리 root 를 validator 까지 관통시킨다
    prov = validate_provenance(in_dir, repo_root=repo_root)
    # ★ F52b — 배너는 주 입력만 보면 안 된다. 비교표에 쓰인 half-cell artifact도
    #   전이적 입력이므로 그 검증 결과를 합친다 (compare_cases 가 봉인해 둔다).
    cc = _load(in_dir / "case_comparison.yaml") or {}
    cc_prov = cc.get("provenance") or {}
    # ★ F60 — 저장된 `ok` 를 믿으면 stale·변조 artifact 가 녹색으로 통과한다.
    #   **지금 시점에 직접 다시 검증**하고 digest 도 재계산해 대조한다.
    from src.io import file_digest as _fd
    for tag, v in list(cc_prov.items()):
        rd, sf = v.get("run_dir"), v.get("scored_file")
        now = (validate_provenance(rd, repo_root=repo_root, fits_path=sf)
               if rd else {"ok": False, "fail": ["run_dir 없음"]})
        if not now["ok"]:
            v["ok"] = False
            v["fail"] = now["fail"]
            v["_재검증"] = "생성 시점 재검증 실패"
        elif sf and v.get("fits_sha256") and _fd(sf) != v["fits_sha256"]:
            v["ok"] = False
            v["fail"] = ["fits_digest_불일치"]
            v["_재검증"] = "봉인된 digest와 현재 파일이 다르다"
    # tag 집합·최상위 플래그도 강제한다
    if cc and set(cc_prov) != {"grid", "halfcell"}:
        prov["ok"] = False
        prov["fail"] = list(prov["fail"]) + ["비교입력_tag불완전"]
        prov["reasons"] = list(prov["reasons"]) + [
            f"provenance tag가 {sorted(cc_prov)}다 (grid·halfcell 필요)"]
        prov["checks"]["비교입력_tag불완전"] = f"실패 — {sorted(cc_prov)}"
    if cc and cc.get("provenance_ok") is not True:
        prov["ok"] = False
        prov["fail"] = list(prov["fail"]) + ["비교입력_provenance_ok_아님"]
        prov["reasons"] = list(prov["reasons"]) + ["case_comparison.provenance_ok가 참이 아니다"]
        prov["checks"]["비교입력_provenance_ok_아님"] = "실패"
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

    # ★ F69 — 저장된 **숫자**를 재계산해 대조한다.
    #   F60 은 fits digest 만 다시 봤다. 그래서 `case_comparison.yaml` 의
    #   `degenerate_frac: 0.944444 → 0.123456` 이나 `objective_comparison.yaml` 의
    #   `94.44% → 12.3456%` 같은 **파생 숫자 변조**가 그대로 렌더됐고 배너도 없었다.
    #   보고서가 렌더하는 값은 전부 fits 에서 다시 나와야 한다.
    # ★ F77 — objective_comparison·summary·sweep 은 로드 시점에 재계산해
    #   렌더 원본으로 삼았고, 저장본이 다르면 stale 로 이미 표시됐다.
    for s in stale:
        prov["ok"] = False
        prov["fail"] = list(prov["fail"]) + [f"파생_stale_{s}"]
        prov["reasons"] = list(prov["reasons"]) + [
            f"{s}의 저장본이 정본 fits 재계산과 다르다 — 보고서는 재계산 값을 "
            f"실었지만, 이 파일을 직접 읽는 소비자는 틀린 숫자를 본다"]
        prov["checks"][f"파생_stale_{s}"] = "실패 — 재계산과 불일치"
    if wsweep_prov is not None:
        prov["checks"]["wsweep_provenance"] = (
            "통과" if wsweep_prov["ok"] else f"실패 — {wsweep_prov['fail'][:3]}")
    elif (in_dir / "wsweep").exists():
        prov["checks"]["wsweep_provenance"] = "미검증 — 재계산 경로를 타지 못했다"
    _case_render = None
    for name, why in (("case_comparison.yaml", "비교표"),):
        rc = _recheck_derived(in_dir, name, repo_root=repo_root)
        if rc is None:
            continue
        prov["checks"][f"파생_{name}"] = "통과" if rc["ok"] else f"실패 — {rc['why']}"
        if not rc["ok"]:
            prov["ok"] = False
            prov["fail"] = list(prov["fail"]) + [f"파생_{name}"]
            prov["reasons"] = list(prov["reasons"]) + [
                f"{why}({name})의 숫자가 fits 에서 재계산한 값과 다르다: {rc['why']}"]
        # ★ 10차 발견 5 — 비교표 렌더 원본은 저장본이 아니라 **재계산본**이다.
        #   저장본 렌더는 배너가 떠도 틀린 숫자(n_conditions 999999)를 실었다.
        if name == "case_comparison.yaml" and rc.get("now"):
            _case_render = rc["now"]
            # ★ 10차 자체 리뷰 — provenance_ok(= 두 artifact 검증 ∧ MUST_MATCH
            #   spec 일치)도 **재계산 값**으로 강제한다. 위의 검사는 저장본의
            #   자기신고를 읽으므로 True 로 위조하면 spec 불일치가 배너를
            #   피해 갔다.
            if _case_render.get("provenance_ok") is not True:
                prov["ok"] = False
                prov["fail"] = list(prov["fail"]) + ["비교입력_재계산_불합격"]
                prov["reasons"] = list(prov["reasons"]) + [
                    "다시 계산한 case 비교의 provenance_ok 가 참이 아니다 "
                    f"(artifact 검증 실패 또는 spec 불일치: "
                    f"{_case_render.get('_주의_공통성', '')[:80]})"]
                prov["checks"]["비교입력_재계산_불합격"] = "실패"

    # ★ F69 — 채점 자체가 정본에서 나왔는가. `--fits` 로 임의 parquet 을 채점하면
    #   degeneracy 가 94% → 0% 로 바뀌는데 배너는 정본만 봤다.
    _sm = _load(in_dir / "degeneracy_summary.yaml") or {}
    _src = _sm.get("_채점원본")
    if _sm and _src is not None and not _src.get("인용가능"):
        prov["ok"] = False
        prov["fail"] = list(prov["fail"]) + ["채점원본_비정본"]
        prov["reasons"] = list(prov["reasons"]) + [
            f"채점 대상이 인용 가능한 정본이 아니다: {_src.get('봉인상태')}"]
        prov["checks"]["채점원본_비정본"] = f"실패 — {_src.get('봉인상태')}"
    elif _sm and _src is None:
        prov["ok"] = False
        prov["fail"] = list(prov["fail"]) + ["채점원본_기록없음"]
        prov["reasons"] = list(prov["reasons"]) + [
            "degeneracy_summary.yaml 에 _채점원본 표식이 없다 (F69 이전 산출물)"]
        prov["checks"]["채점원본_기록없음"] = "실패 — F69 이전 산출물"
    if not prov["ok"]:
        P.append(
            "> # ⛔ 인용 금지\n"
            "> \n"
            "> 이 문서는 **재현 정보가 갖춰지지 않은 artifact**에서 생성됐습니다. "
            "실패한 검사: "
            + ", ".join(f"`{k}` — {r}" for k, r in zip(prov["fail"], prov["reasons"]))
            + ".\n> \n"
            "> 사건률 비, half-cell 목적함수 비교, raw PE/NE 부호 통계, multi-start, "
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
    # ★ 16차 발견 10 — 계산 artifact 를 만든 코드와 **이 문장을 만든 코드**는
    #   다르다. 하나의 `git:` 로 합치면 인용자가 둘을 구분할 수 없다.
    if manifest:
        P.append(f"artifact producer git/source_digest: "
                 f"`{manifest.get('git_commit', '?')}`"
                 f"{' (dirty)' if manifest.get('git_dirty') else ''}"
                 f" / `{(manifest.get('run_spec') or {}).get('source_digest', '?')}`  ")
    try:
        from src.io import git_info as _gi, source_digest as _sd
        _rroot = Path(__file__).resolve().parent.parent   # renderer 의 저장소 root
        _rg = _gi(_rroot)
        P.append(f"report generator git/source_digest/dirty: "
                 f"`{_rg.get('git_commit', '?')}` / `{_sd(_rroot)}` / "
                 f"`{_rg.get('git_dirty')}`  ")
    except Exception as e:  # noqa: BLE001
        P.append(f"report generator: 확인 불가 ({type(e).__name__})  ")
    # ★ 10차 자체 확인 1 — untracked 산출물의 진본성 앵커. manifest 의 seal 은
    #   자기신고라 "값 변조 + 재봉인"을 구분하지 못한다. 이 문서가 커밋되면
    #   아래 digest 가 저장소 이력에 남아, 이후 변조는 보고서 재생성 diff 로
    #   드러난다 (fits: 지금 재계산 / curves: run_spec 에 봉인된 값).
    # ★ 11차 발견 7 — prefix 가 아니라 **full 64자리**를 싣는다. artifacts/
    #   artifact_index.yaml 의 같은 키와 글자 그대로 대조할 수 있어야 한다.
    if (in_dir / "fits.parquet").exists():
        _spec_a = manifest.get("run_spec") or {}
        P.append(f"앵커 fits_sha256: `{_fd(in_dir / 'fits.parquet', full=True)}`  ")
        P.append(f"앵커 curves_sha256(sealed): "
                 f"`{(_spec_a.get('producer') or {}).get('curves_sha256')}`  ")
        P.append("(대조: `artifacts/artifact_index.yaml` — 두 값이 같은 묶음이 "
                 "이 보고서의 근거다)  ")
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
    for line in _conclusion(cmp_res, summary, fits, p22_facts):
        P.append(line + "\n")
    # ★ 14차 발견 6 — 비대칭 pipeline 보고서는 목적함수 간 비교(결론 2)의
    #   인용 정본이 어디인지 스스로 밝혀야 한다. "paired 재실행이 필요하다"는
    #   경고만으로는 독자가 그 문서를 찾을 수 없다.
    if not (_mopt0.get("adaptive") is False and _mspec0.get("warm_start") is False):
        P.append("   → **목적함수 간 비교(결론 2)의 인용 정본은 공정 paired "
                 "보고서 `docs/RESULTS_PAIRED_FIXED5.md` 다** "
                 "(`results/paired_fixed5_v4` 에서 생성). 위 1번은 비대칭 "
                 "pipeline(adaptive 조기 종료 + warm start 연쇄)에서 관측된 "
                 "값이므로 단독 인용하지 말 것.\n")

    # ── 한계 (결론 바로 밑) ──
    P.append("### 이 결론이 말하지 않는 것\n")
    gap = summary.get("coverage_gap") or {}
    P.append(f"- **격자 공백(F14)**: 완방 프레임 guard 때문에 저LLI 영역에 고LAM_PE "
             f"조건이 없다. 저LLI(≤2%)에서 도달한 최대 LAM_PE는 "
             f"`{gap.get('max_lam_pe_at_low_lli', '?')}`, 격자 전체 최대는 "
             f"`{gap.get('max_lam_pe_overall', '?')}`. "
             f"고LAM_PE 결론은 고LLI가 동반된 조건에서만 검증된 것이다.")
    # ★ 16차 발견 7 — 이 경고는 adaptive 실행에만 해당한다. fixed-budget paired
    #   문서에 그대로 실리면 문서가 자기 protocol 과 모순된다.
    if _mopt0.get("adaptive") is not False:
        P.append("- **restart 불일치율(F4)**: adaptive 조기 종료로 조건마다 restart 수가 "
                 "달라, multi-start 불일치율을 목적함수 간 비교 지표로 쓰지 않았다. "
                 "`degeneracy_summary.yaml`의 `restart_conditioned` 항목에 "
                 "restart 수로 조건화한 값만 있다.")
    else:
        P.append(f"- **restart 예산(F4)**: 이 실행은 adaptive 조기 종료를 끄고 "
                 f"restart {_mspec0.get('n_restarts')}개를 고정했다. 따라서 조건마다 "
                 f"예산이 다른 문제는 없다. 남는 한계는 유한 restart 표본이라는 "
                 f"점이며, multi-start 지표는 그 budget 안에서만 유효하다.")
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
    P.append(_objective_section_heading(len(tbl.index)) + "\n")
    P.append("복원가능군(F1)만, 노이즈 전체 합산.\n")
    P.append(to_markdown(tbl) + "\n")
    # ★ F29 — 복원가능군 제외가 결론을 만드는지 보이려면 전체군을 나란히 둔다.
    tbl_all = pd.DataFrame(cmp_res.get("table_all_conditions") or [])
    if len(tbl_all):
        P.append("### 전체 격자 (복원불가군 포함)\n")
        ps = cmp_res.get("population_sensitivity") or {}
        P.append(_unrecoverable_note())
        if ps.get("direction_flips"):
            P.append("> ⚠ **두 표에서 33p와 34p의 우열이 뒤집힙니다.** 결론 문장에 어느 "
                     "모집단인지 반드시 함께 쓰세요.\n")
        P.append(to_markdown(tbl_all) + "\n")

    if len(tbl_noise):
        P.append("### 노이즈 수준별 (F10)\n")
        P.append(_noise_note(cmp_res.get("table_by_noise")
                             or cmp_res.get("table_noise") or []) + "\n")
        P.append(to_markdown(tbl_noise) + "\n")

    # ── 22p ──
    P.append("## 22p 실험 조건 판정\n")
    P.append("*모두 `noise = 0` 조건이다. 노이즈가 있으면 값이 달라진다(F10) — `objective_comparison.yaml`의 `verdict_22p.noise` 참조.*\n")
    # ★ 16차 발견 4 — "최근접 8점이 모두 LAM_PE = LAM_NE" 는 사실이 아니다.
    #   0.02 step 에서 (0.13, 0.13, 0.17) 의 8 corner 는 PE=NE 4개 + |PE-NE|=2%p
    #   4개이고 평균 참 격차가 1%p 다 (그 값을 같은 줄에 쓰면서 모순이었다).
    _v22b = (p22_facts.get("pocv_dvdq")
             or (cmp_res.get("verdict_22p") or {}).get("pocv_dvdq") or {})
    _c22b = _p22_composition(_v22b, (cmp_res.get("gap_analysis") or {}).get("pocv_dvdq"))
    P.append(f"> ⚠ **{_c22b['headline']}.** {_c22b['detail']}. "
             f"{_c22b['wide']} 22p 판정에 쓸 수 있는 것은 "
             f"\"참 격차가 큰 조건이 붕괴하는가\" 가 아니라 국소 "
             f"n={getattr(_v22b, 'n_near', None) or (_v22b.get('n_near', '?') if isinstance(_v22b, dict) else '?')} 표본의 복원 성적뿐이다 "
             f"(그 질문의 답은 결론 2 다).\n")
    # ★ 16차 발견 6 — 이 열도 행별 max-mode 절대오차의 평균이다
    P.append("| objective | 근방 조건 | recovery failure | 평균 max-mode \\|err\\| | "
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
        # ★ 16차 발견 4 의 잔여 — 결론과 22p 절은 고쳤는데 이 도입부가 여전히
        #   "근방은 애초에 PE=NE" 라고 단정해 같은 문서 안에서 자기모순이었다.
        #   근방은 참 격차가 **작을 뿐**이고, 그것만으로도 논지는 성립한다.
        _v22 = (p22_facts.get("pocv_dvdq")
                or (cmp_res.get("verdict_22p") or {}).get("pocv_dvdq") or {})
        _c22 = _p22_composition(_v22, gaps.get("pocv_dvdq"))
        _intro = (f"22p 근방 격자점은 **참 격차가 작다** — {_c22['detail']}."
                  if _c22["known"] else
                  f"22p 근방 격자점의 참값 구성은 이 artifact 에 기록되어 있지 "
                  f"않다 — {_c22['detail']}.")
        P.append(f"{_intro} "
                 f"거기서 복원값이 비슷하게 나오는 건 아무 증거가 못 된다. "
                 f"물어야 할 것은 반대 방향이다 — **참값이 뚜렷이 다를 때도 "
                 f"fitting이 둘을 같다고 말하는가.**\n")
        P.append("| objective | 넓은 격차 조건 n | **격차 붕괴율** | shrinkage | "
                 "거짓 분리율 | 붕괴에 필요한 격차오차 / 실측 중앙값 |")
        P.append("|---|---|---|---|---|---|")
        for o, g in gaps.items():
            if "gap_collapse_frac" not in g:
                continue
            need = (f"{_pp(g['collapse_requires_gap_err'], 0)} / "
                    f"{_pp(g['gap_err_median'])}"
                    if "collapse_requires_gap_err" in g else "—")
            # ★ 16차 발견 2 — 상세표도 count 우선. 핵심 문단은 1/245 라고
            #   쓰면서 여기서 0% 로 반올림하면 문서가 스스로 모순된다.
            P.append(f"| {o} | {g['n_wide_gap_true']} | "
                     f"**{_cnt(g['gap_collapse_frac'], g['n_wide_gap_true'])}** | "
                     f"{g['shrinkage']:.2f} | "
                     f"{_cnt(g.get('false_split_frac'), g.get('n_small_gap_true'))} | "
                     f"{need} |")
        P.append("")
        P.append("- **격차 붕괴율**: 참 격차 ≥ 6%p인데 복원 격차 < 2%p로 답한 비율. "
                 "높을수록 \"두 전극이 비슷하다\"는 관측이 무의미해진다.")
        P.append("- **shrinkage**: 복원 격차 / 참 격차의 평균. 1이면 격차를 그대로 "
                 "복원, 0에 가까우면 전부 뭉갠다.")
        P.append("- **거짓 분리율**: 참값은 같은데 다르다고 답한 비율 (반대 방향 오류).")
        P.append(_gap_table_legend())

        # ★ F28 — 임계 2차원 민감도. 한 칸만 떼어 인용하지 못하게 표 전체를 싣는다.
        sens = (cmp_res.get("gap_sensitivity") or {}).get("pocv_dvdq") or []
        if sens:
            P.append("### 임계 민감도 — 위 숫자를 인용하기 전에 볼 것\n")
            P.append("같은 데이터에서 (참 격차 cutoff, 동일 판정 tol) 두 임계만 바꿔 "
                     "사건률 비를 다시 센 것이다 (`pocv_dvdq`, noise=0, 복원가능군). "
                     "값이 한 자릿수에서 수십까지 움직이면, 특정 조합의 값은 "
                     "**측정이 아니라 선택**이다.\n")
            _gref = (gaps.get("pocv_dvdq") or {})
            _ov = _same_def_overlap_note(sens, tol=_gref.get("tol", 0.02),
                                         gap_thresh=_gref.get("gap_thresh", 0.06))
            if _ov:
                P.append(_ov)
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
            P.append("각 칸은 `사건률 비` 아래에 `분자/분모 ÷ 분자/분모`를 함께 적었다. "
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
            # ★ 16차 발견 5 — 분자를 숨기면 독자가 사건률 비를 감사할 수 없다.
            #   양쪽 군 모두 k/n 으로 낸다.
            P.append(f"| 모집단 | 작은 격차에서 \"같다\" | 넓은 격차 붕괴 | 사건률 비 |")
            P.append("|---|---|---|---|")
            for label, gg in (("복원가능군", gaps["pocv_dvdq"]),
                              ("전체 생성성공 격자", ga)):
                _sp = gg.get("false_split_frac")
                P.append(f"| {label} | "
                         f"{_cnt(None if _sp is None else 1 - _sp, gg.get('n_small_gap_true'))} | "
                         f"{_cnt(gg.get('gap_collapse_frac'), gg.get('n_wide_gap_true'))} | "
                         f"{gg['likelihood_ratio_equal']:.2f} |")
            P.append("")
            P.append("복원가능군 조건화는 물리적 근거가 있지만(참 α<1이면 정답이 재구성 "
                     "창 밖), **그 조건화가 사건률 비를 크게 바꾼다**는 사실은 결론과 같은 "
                     "무게로 적어야 한다.\n")

    # ── Hessian ──
    if hess_by_obj:
        P.append("## 곡률 진단 (Hessian) — 참고용, 결론 근거 아님\n")
        # ★ 17차 발견 7 — 상단의 초록 검사 목록은 fit provenance 다. Hessian 의
        #   곡선·obj_cfg·v_col·reference·표본·eps 연결은 **하나도 검증하지 않는다.**
        P.append("> ⛔ **이 절은 문서 상단 provenance 검증 범위 밖입니다.** 상단의 "
                 "초록 검사 목록은 fit artifact 를 검증한 결과이며, Hessian 산출물의 "
                 "곡선·`obj_cfg`·`v_col`·reference·표본·`eps` 연결은 **어느 검사도 "
                 "보지 않습니다**. 비인용 부록으로만 읽으세요 (A·A'·B·C 미수정).\n")
        P.append("> ⚠⚠ **이 절의 수치를 식별성(degeneracy) 근거로 인용하지 마세요.** "
                 "적대적 리뷰에서 세 가지가 확인됐습니다 (F33). ① 목적함수가 보간·미분·"
                 "peak 연산을 포함해 비매끄러운데 절대 step `eps` 하나를 모든 파라미터에 "
                 "씁니다 — 34p 조건수 중앙값이 eps=1e-3/1e-4/1e-5에서 12.8/229/17381로 "
                 "움직입니다. 수렴하지 않았다는 뜻입니다. ② `min_eigval_positive`가 "
                 "100%가 아닌 만큼은 양의 정부호 국소 최소점임이 **입증되지 "
                 "않은** 지점이고, 그것이 실제 saddle 인지 유한차분·비매끄러움 "
                 "artifact 인지 현재 자료로는 **구분하지 않습니다**. 그런데도 "
                 "flat score와 결합 판정은 그대로 집계됩니다. ③ `α_PE·α_NE 결합`은 "
                 "**같은 부호**를 세는데, 22p 가설(한쪽 과대·다른쪽 과소)은 α에서 부호가 "
                 "**반대**입니다 — 지표가 묻는 질문이 가설과 다릅니다.\n")
        P.append("optimizer 가 반환한 해에서 목적함수의 2차 미분입니다 — 그 점이 "
                 "정상점(stationary)임은 검증되지 않았습니다. 아래는 진단 참고로만 "
                 "두고, 결론이나 optimizer 방어 문장에 쓰지 않습니다.\n")
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
        # ★ 17차 발견 7 추가 — "같은 eps 에서의 순서는 의미 있다" 는 지지되지
        #   않는다. eps 를 바꾸면 값이 자릿수로 움직이고, 순서가 eps 에 안정적이라는
        #   근거가 없다. objective 가 하나뿐이면 순서 자체가 없다.
        P.append("- ⚠ **조건수의 절대값도, 목적함수 간 순서도 인용하지 마세요.** "
                 "목적함수가 여러 스케일에서 울퉁불퉁하면 수치 Hessian 이 수렴하지 "
                 "않아 eps 를 바꾸면 값이 자릿수 단위로 움직입니다 (F23). 순서가 "
                 "eps 에 안정적이라는 근거는 확인되지 않았습니다"
                 + (f" (이 표는 eps={eps_vals[0]:g}, objective {len(hess_by_obj)}개)."
                    if len(eps_vals) == 1
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
        # ★ 18차 발견 10 — eps 미수렴·stationarity 미검증 상태에서 saddle 과
        #   수치 artifact 를 구분할 수 없다. 단정하지 않는다.
        P.append("- **최소고윳값>0** — 100%가 아니면 그만큼은 양의 정부호 국소 "
                 "최소점임이 입증되지 않은 지점입니다. 실제 saddle 인지 "
                 "유한차분·비매끄러움 효과인지는 **구분하지 않습니다**. 그 "
                 "조건들의 조건수는 해석하지 마세요.")
        # ★ 15차 부수 발견 — 위 :172 는 이 지표가 22p 가설과 부호 규약이 달라
        #   근거가 못 된다고 올바르게 경고해 놓고, 여기서 다시 "직접 증거" 라고
        #   썼다. 자기모순이라 후자를 삭제한다.
        P.append("- **α_PE·α_NE 결합** — 평평한 방향에서 두 전극이 같은 부호로 묶여 "
                 "있는 비율입니다. **22p 가설(한쪽 과대·다른쪽 과소)은 부호가 반대**라 "
                 "이 지표는 그 가설에 적용할 수 없습니다 (F33). 진단 참고로만 보세요.\n")

    # ── multi-start (F21) ──
    # ★ F21b: 목적함수 간 비교는 무작위 restart끼리만 해야 공정하다.
    #   warm start 지점(restart 0)이 섞이면 dQ/dV 계열이 인위적으로
    #   multimodal 쪽으로 쏠린다.
    fair = (summary or {}).get("multistart_random_only")
    ms = fair or (summary or {}).get("multistart") or {}
    # ★ 10차 발견 3 — n_restarts≥3이면 이 블록에 목적함수 행 말고도
    #   `random_only_적용`(bool)·`평균_제외_restart수`(float)·`pairwise`(dict)·
    #   `paired`(중첩 summary) 같은 메타 키가 섞인다. `_` 접두사만 거르면
    #   bool에 .get()을 불러 report 생성이 통째로 죽는다 (리뷰 실측:
    #   AttributeError 'bool' object has no attribute 'get').
    #   **목적함수 행의 스키마를 가진 dict만** 표에 올린다.
    _ROW_KEYS = {"n", "flat_valley_frac", "multimodal_frac", "unique_min_frac"}
    ms_rows = {k: v for k, v in ms.items()
               if not k.startswith("_") and isinstance(v, dict)
               and _ROW_KEYS <= set(v)}
    if ms_rows:
        P.append("## multi-start 진단 — 진짜 degeneracy와 최적화 난이도의 구분\n")
        P.append("같은 조건을 여러 초기값에서 다시 풀었을 때 어떻게 갈리는지를 봅니다. "
                 "**두 실패 모드는 처방이 정반대**라 반드시 나눠야 합니다.\n")
        if fair:
            P.append(_random_only_note(_mspec0.get("warm_start") is not False))
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
        # ★ 16차 발견 8 — 이 셋은 유한 restart 표본에 J·parameter tolerance 를
        #   적용한 **휴리스틱 분류**다. 구조적 식별성의 증명이 아니다.
        P.append(f"- **flat valley** — 같은 J(허용 `j_tol`) 안에서 해가 "
                 f"`p_tol` 보다 멀다. 이 solver·restart 예산에서 관측된 "
                 f"**실용적 flatness 신호**이며, 데이터가 그 조합을 구분하지 "
                 f"못한다는 구조적 증명은 아니다.")
        P.append("- **multimodal** — J가 다른 국소최소가 여럿 잡혔다. "
                 "**optimizer difficulty 와 일치하는 관측**이며, 목적함수의 "
                 "고유 정보량 부족과 분리되지 않는다.")
        P.append("- **unique min** — 관측된 restart 범위에서 다른 동등해를 "
                 "찾지 못했다. 전역 유일해의 증명이 아니다.")
        P.append(f"\n*분류 임계와 예산: `j_tol`·`p_tol`·restart "
                 f"{_mspec0.get('n_restarts', '?')}개 (`src/scoring.py`).*\n")
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
        P.append(_agree_frac_note(_mopt0.get("adaptive") is not False))

    # ── 기준 곡선 비교 (Case 1 vs Case 2) ──
    # ★ 10차 발견 5 — 재계산본(_case_render)이 있으면 그것을 렌더한다.
    #   재계산이 불가능했던 경우에만 저장본을 쓰고, 그때는 배너가 이미 붉다.
    case = _case_render or _load(in_dir / "case_comparison.yaml")
    # ★ 14차 2차 발견 4 — 재현 블록이 **렌더된 절과 같은 조건**으로 명령을 낸다
    _case_rendered = bool(case and {"grid", "halfcell"} <= set(case))
    if _case_rendered:
        from tools.compare_cases import to_markdown as case_md
        P.append("## 기준 곡선 비교 — Case 1 (전 범위 half-cell) vs Case 2 (격자 곡선)\n")
        # ★ 15차 발견 5 — 두 실행은 reference 외에 bounds·p_ini·half-cell
        #   cache/recipe·mode 변환도 다르다. "기준 곡선이 원인" 이라는 인과
        #   귀속은 이 자료로 성립하지 않는다.
        P.append("> ⚠ **이것은 reference 단독의 인과효과가 아닙니다.** 두 실행은 "
                 "기준 곡선 외에 bounds preset·초기값 `p_ini`·half-cell "
                 "cache/recipe·mode 변환도 함께 다릅니다. 따라서 아래 수치는 "
                 "**두 reference-specific fitting pipeline 에서 관측된 값**으로만 "
                 "읽어야 하며, reference 단독 효과를 주장하려면 나머지 축을 통제한 "
                 "별도 대조가 필요합니다. 아래 `reference별_허용차이`·`_인과범위` 를 "
                 "함께 보세요.\n")
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
        # ★ F78 — 인과 문구의 범위. bounds 가 reference 별로 다르므로 이 표는
        #   "기준 곡선 단독"이 아니라 pipeline 수준의 비교다.
        if case.get("_인과범위"):
            P.append(f"> ⚠ {case['_인과범위']}\n")
        # ★ 10차 자체 리뷰 — 보정 계수의 추정 모집단 명시
        if case.get("_주의_바이어스"):
            P.append(f"> ⚠ {case['_주의_바이어스']}\n")
        P.append("> ⚠ halfcell 쪽의 \"복원불가 0%\"는 **측정이 아닙니다.** "
                 "`src/scoring.py`가 `reference != \"grid\"`이면 `recoverable=True`로 "
                 "고정합니다(전 범위 테이블이라 창 부족이 없다는 물리적 근거). "
                 "그래서 위 표는 **두 실행의 공통 조건 중 grid 기준에서 복원가능한 것**으로 "
                 "행 수를 맞춰 비교한 것입니다.\n")

    # ── 가중치 ──
    if wsweep:
        opt = wsweep.get("optimum", {})
        # ★ 10차 발견 5 — 표본 수·restart·warm start 는 자기신고
        #   (weight_sweep.yaml)가 아니라 **서명된 run_spec** 값을 렌더한다.
        _ws_wgrid = (sorted(float(str(n).split("_", 1)[1])
                            for n in (wspec_verified.get("objectives") or {})
                            if str(n).startswith("wdqdv_"))
                     or wsweep.get("w_grid"))
        _ws_ncond = wspec_verified.get("n_conditions", wsweep.get("n_conditions"))
        _ws_nres = wspec_verified.get("n_restarts", wsweep.get("n_restarts"))
        _ws_warm = wspec_verified.get("warm_start", wsweep.get("warm_start"))
        P.append("## dQ/dV 가중치 — 임의 튜닝이 아니라는 근거\n")
        P.append(f"`w_dqdv`를 {_ws_wgrid}로 훑어 degeneracy 비율이 "
                 f"최소가 되는 값을 찾았다 "
                 f"(층화 표본 {_ws_ncond}조건, restart {_ws_nres}).\n")
        P.append(f"- 노이즈 평균 최적: **w_dqdv = {opt.get('w_star_mean_over_noise')}** "
                 f"({opt.get('metric')} = {_pct(opt.get('value_at_w_star'), 1)}), "
                 f"기본값 w=1.0일 때 {_pct(opt.get('value_at_w1'), 1)}")
        for n, d in (opt.get("per_noise") or {}).items():
            P.append(f"- noise={n}: 최적 w = {d.get('w_dqdv')} "
                     f"({_pct(d.get(opt.get('metric')), 1)}, n={d.get('n')})")
        P.append(f"\n{opt.get('_주의', '')}\n")
        # ★ F20d — sweep 의 optimizer 설정이 본 실행과 다르면 이 절 전체를 인용할
        #   수 없다. ★ 10차 발견 4 — 그 판정을 자기신고가 아니라 **두 run_spec 의
        #   대조 결과**(sweep_vs_main)로 한다. None 은 대조 자체를 못 한 것이다.
        if wsweep.get("_경고"):
            P.append(f"> ⚠ **이 sweep의 최적 w를 인용하지 마세요.** {wsweep['_경고']}\n")
        elif sweep_vs_main is None:
            P.append("> ⚠ **sweep과 본 실행의 설정 대조를 하지 못했습니다** "
                     "(wsweep manifest/run_spec 없음). 같은 설정임이 증명되지 "
                     "않았으므로 최적 w를 인용하지 마세요 (F20d).\n")
        elif sweep_vs_main:
            P.append(f"> ⚠ **이 sweep은 본 실행과 설정이 다릅니다** "
                     f"({', '.join(sweep_vs_main)}). 가중치가 아니라 최적화 "
                     f"난이도를 잰 값일 수 있습니다 — `tools/check_sweep_consistency.py`로 "
                     f"본 실행과 대조한 뒤 인용하세요 (F20d).\n")
        else:
            P.append(f"> sweep은 본 실행과 같은 설정으로 돌렸습니다 — 두 run_spec 의 "
                     f"optimizer·warm_start·bounds·reference·v_col 대조로 확인 "
                     f"(warm_start={_ws_warm}, restart {_ws_nres}). "
                     f"`w=0`은 `pocv_dvdq`와, "
                     f"`w=1`은 `pocv_dvdq_dqdv`와 정의가 같으므로 위 표의 두 끝점은 "
                     f"목적함수 비교표와 일치해야 합니다 — "
                     f"`tools/check_sweep_consistency.py`가 확인합니다.\n")
        P.append("결과: 실행 디렉터리의 `wsweep/objectives_optimized.yaml` — "
                 "configs/ 로의 승격은 검토 후 커밋으로 한다 (F79)\n")

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
    # ★ 14차 발견 6 — 경로도 **이 산출물의 manifest 에서** 만든다. 예전에는
    #   grid --out / fit --in 에 전부 in_dir(fit 산출물)를 써서, producer 와
    #   fit 이 다른 디렉터리인 실제 배치(grid_curves_v4 → grid_fit_v4)에서
    #   그대로 실행하면 fit 산출물 위에 곡선을 만들고 자기 자신을 입력으로
    #   fit 하는 다른 pipeline 이 됐다. manifest.input 이 producer 경로다
    #   (없는 옛 산출물은 in==out 실행이었으므로 in_dir 로 fallback).
    _curves_dir = manifest.get("input") or str(in_dir)
    P.append(f"./run.sh --mode grid --config configs/grid_fine.yaml "
             f"--nproc $(nproc) --out {_curves_dir}")
    # ★ 13차 발견 6 — 재현 명령을 **이 산출물의 run_spec 에서** 만든다.
    #   예전에는 항상 기본 fit 명령이라, paired(--no-adaptive --no-warm-start)
    #   보고서를 보고 그대로 실행하면 다른 비대칭 pipeline 이 돌았다.
    _rs = manifest.get("run_spec") or {}
    _fit = [f"./run.sh --mode fit   --in {_curves_dir} --out {in_dir} "
            f"--nproc $(nproc)", *_fit_flags(_rs)]
    P.append(" ".join(_fit))
    P.append(f"./run.sh --mode score --in {in_dir}")
    # ★ 17차 발견 7 — Hessian 재현 명령을 **아예 싣지 않는다**. 분리배치에서는
    #   `src/hessian.py:135` 가 곡선을 못 찾아 실패하고(A 미수정), 곡선을 임시로
    #   놓아도 `degeneracy_summary.yaml` 을 변이시켜 보고서를 stale 로 만든다
    #   (B 미수정). 독자가 그대로 실행하면 artifact 가 망가진다.
    if hess_by_obj:
        P.append("")
        P.append("# Hessian 절은 이 재현 체인에 들어 있지 않습니다 (A·B 미수정).")
        P.append("#   분리배치에서 hessian 모드는 곡선을 찾지 못하고, 실행하면")
        P.append("#   degeneracy_summary.yaml 을 변이시켜 이 보고서를 stale 로 만듭니다.")
    # ★ 14차 2차 발견 4 — 이 블록만 실행하면 **이 문서가 렌더한 절이 전부**
    #   다시 나와야 한다. 예전에는 주 fit chain 만 있어서, sweep 절과
    #   Case 1↔Case 2 절을 렌더하면서도 재실행하면 그 두 절이 생기지 않았다.
    #   명령은 서명된 metadata(sweep run_spec, case_comparison.provenance)에서
    #   만든다 — 자기신고 값으로 만들면 재현이 문서와 어긋난다.
    if wsweep:
        # ★ 14차 3차 발견 1 — sweep 의 정본 위치는 `<main-fit>/wsweep` 이다.
        #   `run_weight_sweep` 은 명시된 `--out` 을 그대로 쓰고 생략 시에만
        #   `<in>/wsweep` 을 기본값으로 하므로, main fit 디렉터리를 주면
        #   보고서·strict smoke 가 읽는 nested 구조가 재현되지 않는다.
        # ★ 14차 3차 발견 2 — wrapper 옵션명은 `--w-stride` 다 (`--stride` 는
        #   `알 수 없는 인자` 로 exit 1).
        _sw = [f"./run.sh --mode wsweep --in {_curves_dir} "
               f"--out {Path(in_dir) / 'wsweep'} --nproc $(nproc)"]
        if _ws_wgrid:
            _sw.append(f"--w-grid {','.join(str(w) for w in _ws_wgrid)}")
        if wsweep.get("stride") is not None:
            _sw.append(f"--w-stride {wsweep['stride']}")
        if _ws_nres:
            _sw.append(f"--n-restarts {_ws_nres}")
        if (wspec_verified.get("optimizer") or {}).get("adaptive") is False:
            _sw.append("--no-adaptive")
        if _ws_warm is False:
            _sw.append("--no-warm-start")
        P.append(" ".join(_sw))
    # Case 1 (전 범위 half-cell) 절을 렌더했으면 그 기준 실행까지 재현한다
    _hc_dir = (((case.get("provenance") or {}).get("halfcell") or {}
                ).get("run_dir") if _case_rendered else None)
    if _hc_dir:
        # ★ 14차 3차 발견 4 — half-cell 도 **그 artifact 의 서명된 run_spec** 에서
        #   플래그를 만든다. `--reference halfcell` 만 붙이면 nondefault
        #   protocol(restart 수·clean target·adaptive/warm off)이 복원되지 않아
        #   Case 1 절이 다른 설정으로 다시 계산된다.
        _hrs = (_load(Path(_hc_dir) / "manifest.yaml") or {}).get("run_spec") or {}
        # ★ 14차 4차 발견 4 — 기준 곡선을 만든 방법(ocp/sim)도 서명값이다.
        #   기본값을 박으면 `method=sim` artifact 가 다른 기준으로 재계산된다.
        _hc_method = (_hrs.get("halfcell_recipe") or {}).get("method") or "ocp"
        P.append(f"python -m src.halfcell --config configs/base.yaml "
                 f"--method {_hc_method} --force --verify")
        _hfit = [f"./run.sh --mode fit   --in {_curves_dir} --out {_hc_dir} "
                 f"--nproc $(nproc)",
                 *(_fit_flags({**_hrs, "reference": "halfcell"}))]
        P.append(" ".join(_hfit))
        P.append(f"./run.sh --mode score --in {_hc_dir}")
        P.append(f"./run.sh --mode report --in {in_dir} --compare {_hc_dir}")
    else:
        P.append(f"./run.sh --mode report --in {in_dir}")
    P.append("```\n")
    # ★ 14차 4차 발견 4 — 재현 범위를 문서가 스스로 한정한다. 위 명령은 이
    #   artifact 의 서명값에서 만들지만, 아직 명령으로 내보내지 않는 축이 있다.
    #   "전 절 재현"이라고 읽히면 비기본 실행에서 다른 수치가 나온다.
    P.append(_reproduction_scope_note(
        has_wsweep=bool(wsweep), has_halfcell=bool(case),
        has_hessian=bool(hess_by_obj),
        warm_start=_mspec0.get("warm_start") is not False))
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
    # ★ 48차 P0-8 — smoke 산출은 정본 보고서가 될 수 없다. `--out` 이 어디든
    #   **입력**이 면제 namespace 안이면 그 결과는 인용 대상이 아니다.
    from tools.preserve import assert_not_smoke_provenance
    assert_not_smoke_provenance([args.in_dir], "보고서")
    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    print(build(args.in_dir, args.out))


if __name__ == "__main__":
    main()
