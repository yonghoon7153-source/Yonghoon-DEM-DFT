#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② S0 — 표현 원장 (raster-only · 솔브 없음 · CPU) — 시험 먼저 단계의 API 스텁 (구현 전).

설계 정본 = docs/reviews/rint_carbon_additive_design_v1_20261020.md §2 · 등록 R §2-1 · §11.
이 파일은 시험 (`scripts/test_ca_s0_census.py`) 이 부르는 이름만 둔다 — 전부 NotImplementedError.
"""


class S0Error(Exception):
    """S0 입력 · 단계 계약 위반 — 조용히 강등하지 않고 거부한다."""


def _todo(*_a, **_k):
    raise NotImplementedError('S0 구현 전 (시험 먼저)')


seg_seg_closest = pieces_of = spacing_stats = make_plan = plan_bytes_of = check_plan = _todo
verify_plan_commit = vv_census = port_of = voxel_relation = sdcp_via = via_sdcp_depth = _todo
membership_counts = fiber_sphere_instances = schema_forbidden_keys = find_run_dir = _todo
resolve_payload_argv = validate_kit_arrays = capture_raster_inputs = census_kit = run_stage = main = _todo
