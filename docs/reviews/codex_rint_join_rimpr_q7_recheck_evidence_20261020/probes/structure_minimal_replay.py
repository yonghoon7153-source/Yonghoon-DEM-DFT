"""Small standalone reproduction of malformed section-header certification."""
from pathlib import Path
import contextlib
import io
import json
import os
import sys
import types

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "tmp/structure_minimal"
TMP.mkdir(parents=True, exist_ok=True)
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
            "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"
for key in ("TEMP", "TMP", "TMPDIR"):
    os.environ[key] = str(TMP)
sys.path[:0] = [
    str(ROOT / "source/scripts"),
    str(ROOT.parent / "lhs_coverage_review_20260930/deps"),
    str(ROOT.parent / "gen2_network_reverify3_20261007/deps"),
]
try:
    import resource
except ImportError:
    resource = types.ModuleType("resource")
    resource.RUSAGE_SELF = 0
    resource.getrusage = lambda _: types.SimpleNamespace(ru_maxrss=float("nan"))
    sys.modules["resource"] = resource
import numpy as np
import rint_iface_join as J
import step3_sigma as S

# Prior independent baseline; actual bytes, no submitted fixture helper.
D = ROOT.parent / "rint_g2_impl_reverify_20261015/tmp/join_independent"
paths = [D / ("baseline_" + s) for s in ("sc.csv", "atom.dump", "contact.dump")]
base = J.am_iface_join(*paths, type_map={1: "AM_P", 2: "SE"})
c, r, t = (base["particles"][k] for k in ("c_um", "r_um", "t"))
with contextlib.redirect_stdout(io.StringIO()):
    sid, _ = S.rasterize(c, r, t, None, None, (0, 0, 0), (6, 4, 4),
                        .25, bridge_um=.24)
ledger = S.am_iface_ledger(
    c, r, t, sid, sid, (0, 0, 0), .25,
    delta_bound_um=base["g_geo"]["delta_bound_um"], bridge_um=.24)

rows = []
for tag, old_header, new_header in (
    ("missing_token_boundary", "ITEM: ATOMS id type x y z radius",
     "ITEM: ATOMSid type x y z radius"),
    ("discarded_header_tokens", "ITEM: BOX BOUNDS ff ff ff",
     "ITEM: BOX BOUNDS ff ff ff ITEM: BOX BOUNDS"),
):
    mutated = TMP / (tag + "_atom.dump")
    text = paths[1].read_text(encoding="utf8")
    assert text.count(old_header) == 1
    mutated.write_text(text.replace(old_header, new_header, 1), encoding="utf8")
    join = J.am_iface_join(paths[0], mutated, paths[2], type_map={1: "AM_P", 2: "SE"})
    plan = S.am_iface_plan(
        ledger, {"AM_P|AM_P": .001}, join=join, gap_law="cut",
        unreg_law="cut", ambiguous_arm="cut")
    guard = S.iface_require_quantitative(plan, sid=sid, vox=.25)
    before, after = J.read_atom_dump_frame(paths[1]), J.read_atom_dump_frame(mutated)
    fields_equal = {k: bool(np.array_equal(before[k], after[k]))
                    for k in ("ids", "types", "x", "r", "hx", "hr", "box_lo", "box_hi")}
    rows.append({
        "case": tag, "original_header": old_header, "malformed_header": new_header,
        "join_status": join["status"], "join_codes": [r["code"] for r in join["rejections"]],
        "entrance_status": join["entrance"]["status"],
        "frame_layout": join["entrance"]["frame_layout"],
        "box_format": join["entrance"]["box"],
        "plan_codes": [r["code"] for r in plan["rejections"]],
        "quantitative_guard": "ACCEPT" if guard is plan else "OTHER",
        "all_consumed_atom_fields_unchanged": all(fields_equal.values()),
        "field_equality": fields_equal,
        "fixture": str(mutated),
    })
(ROOT / "evidence/structure_minimal_replay.json").write_text(
    json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf8")
print(json.dumps(rows, ensure_ascii=False, indent=2))
