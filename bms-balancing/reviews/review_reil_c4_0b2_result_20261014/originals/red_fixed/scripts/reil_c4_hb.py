"""REIL C4-0b2 — 골격 (RED 용 · 이름만 있고 동작은 없다). 구현은 RED 뒤에 채운다 (상태 문서 §55)."""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve()
BMS = HERE.parents[1]
if str(BMS) not in sys.path:
    sys.path.insert(0, str(BMS))

from scripts import reil_c4_h as h  # noqa: E402

HStop = h.HStop


class RayNotImplemented(HStop):
    """ray (부속 A §4-6) 는 유보 — 미구현 (범위 확인 §9-2)."""


def _todo(*a, **kw):
    raise NotImplementedError("C4-0b2 골격")


residuals_b = profile_problem = sim_problem = nominal_problem = run_phase_b = _todo
nominal_interval = nominal_grid = run_nominal_grid = run_nominal_stage = _todo
profile_order = inner_neighbor = profile_starts = sealed_block = seal_starts = verify_seal = _todo
grid_point_value = profile_point = run_profile_k = sim_starts = run_simultaneous = _todo
h4_candidates = h4_positive = h4_negative = record_h4 = h4_block = _todo
point_status = compat_individual = compat_simultaneous = width = extra_labels = _todo
new_store = direct_runner = supervise_runner = stage_a = rho_wave = run_searches = stage_b = _todo
finalize = common_update_once = pool_records = unit_points = plan_counts = dryrun_b = main = _todo
