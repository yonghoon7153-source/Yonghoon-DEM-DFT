import sys, pathlib, yaml
sys.path.insert(0, ".")
from tools.design_wire import (canonical_design_spec, pairing_design_sha256,
                               parameter_order_sha256, pair_group_id, bank_id,
                               candidate_id)

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
        "candidate_ids": {
            src: candidate_id(bk, BOUNDS_SHA, src, {"i": 0})
            for src in ("base_init", "warm", "random")},
    })
pgg = pair_group_id(pairing_design_sha256(grid), COORDS[0], pos)
golden = {
    "_주의": ("손으로 고치지 않는다. 이 값이 바뀌면 ID 도메인이 바뀐 것이고, "
            "이미 만든 모든 pair_group_id·bank_id·candidate_id 가 무효가 된다. "
            "재생성: python3 tools/gen_design_golden.py"),
    "schema_version": 1,
    "parameter_order": ORDER,
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
