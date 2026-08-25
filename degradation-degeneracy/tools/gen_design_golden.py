import sys, pathlib, yaml
sys.path.insert(0, ".")
from tools.design_wire import (canonical_design_spec, pairing_design_sha256,
                               parameter_order_sha256, pair_group_id, bank_id,
                               candidate_id, coords_from_condition)

ORDER = ["lli", "lam_pe", "lam_ne", "p_ini_scale", "shift"]
spec = canonical_design_spec(
    label="p22_halfcell_2x2_v6", arms=["A", "B", "C", "D"],
    parameter_order=ORDER, bounds_policy="exact_ordered_bounds_digest",
    objective_plan=["pocv_dvdq", "pocv_dvdq_dqdv"],
    bank_generator="pcg64", bank_version="v6.0",
    seed_derivation="H(pair_group_id, bank_version)", dtype="float64",
    endian="little", coordinate_unit="fraction")
grid = canonical_design_spec(
    label="p22_grid_primary_v6", arms=["G_A", "G_C"],
    parameter_order=ORDER, bounds_policy="exact_ordered_bounds_digest",
    objective_plan=["pocv_dvdq", "pocv_dvdq_dqdv"],
    bank_generator="pcg64", bank_version="v6.0",
    seed_derivation="H(pair_group_id, bank_version)", dtype="float64",
    endian="little", coordinate_unit="fraction")

pos = parameter_order_sha256(ORDER)
BANK_SHA = "f" * 64
BOUNDS_SHA = "a" * 64
PAYLOADS = {
    "base_init": {"base_coord_sha256": "1" * 64},
    "warm": {"provider_objective": "pocv_dvdq",
             "provider_artifact_sha256": "2" * 64,
             "solution_map_sha256": "3" * 64},
    "random": {"bank_index": 7, "unit_cube_bytes_sha256": "4" * 64},
}
COORDS = [
    {"lli": "0.17", "lam_pe": "0.13", "lam_ne": "0.13",
     "lam_pe_type": "capacity", "lam_ne_type": "capacity"},
    {"lli": "0.170", "lam_pe": "0.13", "lam_ne": "0.13",     # 후행 0 은 다른 문자열
     "lam_pe_type": "capacity", "lam_ne_type": "capacity"},
    {"lli": "0", "lam_pe": "0", "lam_ne": "0",
     "lam_pe_type": "capacity", "lam_ne_type": "capacity"},
]
vectors = []
for i, c in enumerate(COORDS):
    pg = pair_group_id(pairing_design_sha256(spec), c, pos)
    bk = bank_id(pg, "v6.0", BANK_SHA)
    vectors.append({
        "name": f"halfcell_2x2_coord{i}", "coords": c,
        "pair_group_id": pg, "bank_id": bk,
        # ★ 26차 P1-8 — source 마다 **다른** provenance 다. 초판은 셋 다
        #   placeholder `{"i": 0}` 이었으므로 provenance 를 고정한 것이 아니었다.
        "candidate_payloads": {k: dict(v) for k, v in PAYLOADS.items()},
        "candidate_ids": {
            src: candidate_id(bk, BOUNDS_SHA, src, PAYLOADS[src],
                                objective_plan=["pocv_dvdq", "pocv_dvdq_dqdv"])
            for src in ("base_init", "warm", "random")},
    })
pgg = pair_group_id(pairing_design_sha256(grid), COORDS[0], pos)
# ★ 26차 P1-8 — 실제 `src/grid.Condition` (float) 과 결속한다. 이것이 없으면
#   ID 체계가 격자와 무관한 장난감이다.
from src.grid import Condition
PLACES = 12
grid_rows = []
for c in (Condition(lli=0.17, lam_pe=0.13, lam_ne=0.13, lam_pe_type="capacity",
                    lam_ne_type="capacity", noise=0.001, seed=404),
          Condition(lli=0.0, lam_pe=0.0, lam_ne=0.0, lam_pe_type="capacity",
                    lam_ne_type="capacity", noise=0.0, seed=1),
          Condition(lli=0.055, lam_pe=0.2075, lam_ne=0.13, lam_pe_type="de",
                    lam_ne_type="capacity", noise=0.005, seed=404)):
    wc = coords_from_condition(c, PLACES)
    grid_rows.append({"cond_id": c.cond_id, "wire_coords": wc,
                      "pair_group_id": pair_group_id(pairing_design_sha256(spec), wc, pos)})

golden = {
    "_주의": ("손으로 고치지 않는다. 이 값이 바뀌면 ID 도메인이 바뀐 것이고, "
            "이미 만든 모든 pair_group_id·bank_id·candidate_id 가 무효가 된다. "
            "재생성: python3 tools/gen_design_golden.py"),
    "schema_version": 1,
    "parameter_order": ORDER,
    "objective_plan": ["pocv_dvdq", "pocv_dvdq_dqdv"],
    "parameter_order_sha256": pos,
    "unit_cube_bank_sha256": BANK_SHA,
    "exact_bounds_sha256": BOUNDS_SHA,
    "designs": {
        "p22_halfcell_2x2_v6": {"arms": ["A", "B", "C", "D"],
                                "pairing_design_sha256": pairing_design_sha256(spec)},
        "p22_grid_primary_v6": {"arms": ["G_A", "G_C"],
                                "pairing_design_sha256": pairing_design_sha256(grid)},
    },
    "vectors": vectors,
    "decimal_places": PLACES,
    "grid_linkage": {
        "note": ("`src.grid.Condition` 의 float 좌표를 십진 문자열로 옮긴 것. "
                 "왕복하지 않으면 `decimal_from_float` 가 거부한다 — 조용한 "
                 "반올림으로 다른 조건이 합쳐지는 것을 막는다."),
        "rows": grid_rows,
    },
    "cross_design_same_coords": {
        "note": "같은 좌표라도 설계가 다르면 다른 pair_group_id 여야 한다",
        "halfcell": vectors[0]["pair_group_id"],
        "grid": pgg,
    },
}
p = pathlib.Path("tools/design_golden.yaml")
p.write_text(yaml.safe_dump(golden, allow_unicode=True, sort_keys=False, width=100),
             encoding="utf-8")
print("wrote", p, "vectors:", len(vectors))
print("halfcell design sha:", golden["designs"]["p22_halfcell_2x2_v6"]["pairing_design_sha256"][:16])
print("v0 pair_group_id:", vectors[0]["pair_group_id"][:16])
print("v1 (0.170) differs:", vectors[0]["pair_group_id"] != vectors[1]["pair_group_id"])
print("cross-design differs:", vectors[0]["pair_group_id"] != pgg)
