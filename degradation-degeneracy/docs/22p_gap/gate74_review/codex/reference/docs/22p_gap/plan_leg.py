#!/usr/bin/env python3
"""70차 E9 — 새 다리의 **prospective 계획 항목**을 production 과 같은 함수로 만들어 **보여 준다** (쓰지 않는다).

왜 이 도구인가. 계획 gate(46차 P0-11 · 48차 P0-5)는 `LEG_PRESERVATION.yaml` 의 `planned:` 에 사람이 적은
prospective 항목을 요구하고, 그 항목의 `run_spec` 은 grid/fit 이 **실행 시점에 살아 있는 입력에서 만드는 축**
(`src.grid.live_grid_axis` · `src.fitting.live_fit_axis` → `tools.preserve.leg_run_spec`)과 digest 까지 같아야
claim 이 열린다. 사람이 그 dict 를 손으로 적을 수는 없다 — 그래서 `tests/test_lifecycle_e2e.py::_MAKE_PLAN` 이
production 함수를 그대로 불러 만들었다. 이 도구는 그 절차를 실행 명세 하나(`--leg` · `--config` · `--out` ·
fit 옵션)에서 **stdout 으로** 내놓는다.

리뷰어 제약을 지킨다: "사용자 승인 없이 승인 JSON 을 true 로 바꾸지 않는다." — 이 도구는 원장을 **읽기만**
하고 항목을 출력한다. 원장에 넣는 것은 사람이며(복사해 붙인다), 그 커밋이 승인 행위다. `--write` 같은 문은 없다.

주의 — 출력의 `authorized_source_digest` 는 **지금 checkout 의 RUN_SCOPE** 다. RUN_SCOPE 가 그 뒤 바뀌면
`assert_planned_leg` 가 "승인 code identity 가 지금과 다르다" 로 거부한다 (의도된 것). 그러므로 이 도구는
**최종 커밋에서, 실행할 기계에서** 돌린다 (`discharged_cache_sha256` 도 그 기계의 캐시 실재 여부를 담는다).

사용 (저장소의 degradation-degeneracy/ 에서):
    python3 docs/22p_gap/plan_leg.py --leg grid_fit_v5 --cohort g18_2026_09_15 \
        --config configs/grid_fine.yaml --out results/grid_fit_v5 --recorded-on 2026-09-25 \
        --근거 "71차 …"
출력: YAML 블록 하나 (`planned:` 항목) + 사람이 확인할 요약 (조건 수 · digest · 실행 명령).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def build_entry(leg: str, cohort: str, config: str, out_rel: str, *, objective: str | None,
                bounds: str, n_restarts: int | None, clean: bool, adaptive: bool, warm_start: bool,
                reference: str, halfcell_method: str, halfcell_args: list[str],
                recorded_on: str, 근거: str) -> tuple[dict, dict]:
    """production 과 **같은 함수**로 spec 을 만든다 — 여기서 새 규칙을 만들지 않는다."""
    from src.config import load_config
    from src.fitting import live_fit_axis, parse_halfcell_kw
    from src.grid import conditions_from_config, live_grid_axis
    from src.io import source_digest
    from tools.preserve import (check_id, leg_run_spec, planned_index,
                                run_spec_digest)

    check_id(leg)
    if leg in planned_index():
        raise SystemExit(f"✗ {leg!r} 은 이미 계획 index 에 있다 — 같은 이름을 두 번 적지 않는다 "
                         "(실행 기록은 다음 실행의 승인이 아니다)")
    cfg = load_config(config)
    # `run.sh --mode all` 은 `--noise`/`--noise-seed` 를 주지 않았을 때 config 의 값을 그대로 쓴다
    # (`src.grid.main`: CLI 가 없으면 cfg). 이 도구도 CLI 축 override 를 받지 않는다 — 실행 명세는
    # config 파일 하나로 고정한다 (승인 뒤 argv 로 축을 갈 수 없게).
    conds = conditions_from_config(cfg, cli={})
    out_dir = REPO / out_rel
    grid_axis = live_grid_axis(cfg, conds, out_dir)

    ocfg = load_config("configs/objectives.yaml")
    objectives = dict(ocfg["objectives"])
    if objective:
        want = [s.strip() for s in objective.split(",")]
        missing = [w for w in want if w not in objectives]
        if missing:
            raise SystemExit(f"✗ objectives.yaml 에 없는 목적함수: {missing}")
        objectives = {k: objectives[k] for k in want}
    fcfg = ocfg["fitting"]
    if bounds not in fcfg["bounds_presets"]:
        raise SystemExit(f"✗ 알 수 없는 bounds preset: {bounds}")
    halfcell_kw = parse_halfcell_kw(halfcell_args)
    fit_axis = live_fit_axis(
        objectives, ocfg, fcfg["bounds_presets"][bounds], bounds,
        n_restarts or int(fcfg.get("n_restarts", 5)), not clean, None, None, reference,
        warm_start, adaptive, str(fcfg.get("method", "Nelder-Mead")), halfcell_method,
        halfcell_kw, out_dir, out_dir, base_config="configs/base.yaml")
    fit_axis["in_digest"] = None          # 이 다리의 grid 가 입력을 만든다 (49차 P0-5)
    spec = leg_run_spec(leg, grid_axis, fit_axis)
    entry = {
        "leg_id": leg,
        "cohort_id": cohort,
        "status": "planned",
        "authorization_kind": "prospective",
        "authorized_source_digest": source_digest(),
        "run_spec_digest": run_spec_digest(spec),
        "run_spec": spec,
        "recorded_on": recorded_on,
        "근거": 근거,
    }
    fit_argv = []
    if objective:
        fit_argv += ["--objective", objective]
    if bounds != "expanded":
        fit_argv += ["--bounds", bounds]
    if n_restarts:
        fit_argv += ["--n-restarts", str(n_restarts)]
    if clean:
        fit_argv += ["--clean"]
    if not adaptive:
        fit_argv += ["--no-adaptive"]
    if not warm_start:
        fit_argv += ["--no-warm-start"]
    if reference != "grid":
        fit_argv += ["--reference", reference]
    if halfcell_method != "ocp":
        fit_argv += ["--halfcell-method", halfcell_method]
    for a in halfcell_args:
        fit_argv += ["--halfcell-arg", a]
    summary = {
        "n_conditions": len(conds),
        "grid_axis": grid_axis,
        "objectives": list(objectives),
        "source_digest": entry["authorized_source_digest"],
        "run_spec_digest": entry["run_spec_digest"],
        "command": " ".join(["./run.sh", "--mode", "all", "--leg", leg, "--config", config,
                             "--nproc", "$(nproc)", "--out", out_rel, *fit_argv]),
    }
    return entry, summary


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--leg", required=True)
    ap.add_argument("--cohort", required=True, help="active cohort 의 id (frozen 이면 gate 가 거부한다)")
    ap.add_argument("--config", default="configs/grid_fine.yaml")
    ap.add_argument("--out", required=True, help="저장소 상대 경로. 기존 디렉터리를 덮지 않는 새 이름")
    ap.add_argument("--objective", default=None)
    ap.add_argument("--bounds", default="expanded")
    ap.add_argument("--n-restarts", dest="n_restarts", type=int, default=None)
    ap.add_argument("--clean", action="store_true")
    ap.add_argument("--no-adaptive", dest="adaptive", action="store_false")
    ap.add_argument("--no-warm-start", dest="warm_start", action="store_false")
    ap.add_argument("--reference", default="grid", choices=["grid", "halfcell"])
    ap.add_argument("--halfcell-method", default="ocp", choices=["ocp", "ocpbias", "sim"])
    ap.add_argument("--halfcell-arg", dest="halfcell_arg", action="append", default=[])
    ap.add_argument("--recorded-on", required=True, help="YYYY-MM-DD — 사람이 승인하는 날")
    ap.add_argument("--근거", dest="근거", required=True, help="왜 이 실행인가 (한 문장)")
    a = ap.parse_args(argv)
    if (REPO / a.out).exists():
        raise SystemExit(f"✗ {a.out} 이 이미 있다 — 기존 산출을 덮는 계획은 만들지 않는다 (새 이름을 쓰라)")
    entry, summary = build_entry(
        a.leg, a.cohort, a.config, a.out, objective=a.objective, bounds=a.bounds,
        n_restarts=a.n_restarts, clean=a.clean, adaptive=a.adaptive, warm_start=a.warm_start,
        reference=a.reference, halfcell_method=a.halfcell_method, halfcell_args=a.halfcell_arg,
        recorded_on=a.recorded_on, 근거=a.근거)
    print("# ── LEG_PRESERVATION.yaml 의 `planned:` 에 **사람이** 붙여 넣는 항목 (이 도구는 쓰지 않는다) ──")
    print(yaml.safe_dump([entry], allow_unicode=True, sort_keys=False, width=100), end="")
    print("# ── cohort 항목의 `prospective_legs:` 에도 이 leg_id 를 더한다 ──")
    print("# ── 요약 (사람이 확인) ──")
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
