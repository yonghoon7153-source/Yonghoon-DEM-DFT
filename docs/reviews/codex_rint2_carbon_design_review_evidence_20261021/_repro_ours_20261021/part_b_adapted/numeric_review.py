"""Independent scientific input parsing probes; no source changes or simulation."""
from pathlib import Path
import contextlib
import io
import json
import os
import sys
import types
import warnings

ROOT = Path('/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rint2rev_repro/part_b')
WORK = Path('/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad')
BASELINE = "--baseline" in sys.argv
SRC = (WORK / "rint_g2_impl_reverify_20261015/source") if BASELINE else Path('/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rint2rev_repro/source')
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"
sys.dont_write_bytecode = True
sys.path[:0] = [str(SRC / "scripts"), str(WORK / "lhs_coverage_review_20260930/deps"),
               str(WORK / "gen2_network_reverify3_20261007/deps")]
if os.name == "nt":
    resource = types.ModuleType("resource")
    resource.RUSAGE_SELF = 0
    resource.getrusage = lambda _: types.SimpleNamespace(ru_maxrss=float("nan"))
    sys.modules["resource"] = resource
import numpy as np
import rint_iface_join as J
import step3_sigma as S
from lens_geometry import intersection_disc_area

TAG = "baseline" if BASELINE else "current"
TMP = ROOT / "tmp" / ("numeric_" + TAG)
TMP.mkdir(parents=True, exist_ok=True)
RESULT = {"source": str(SRC), "tag": TAG, "cases": {}}
TM = {1: "AM_P", 2: "SE"}


def standard():
    xyz = [[.002, .002, .002], [.0035, .002, .002]]
    box = ["ITEM: BOX BOUNDS ff ff ff", "0 0.01", "0 0.01", "0 0.01"]
    atom = ["ITEM: TIMESTEP", "100", "ITEM: NUMBER OF ATOMS", "2"] + box + ["ITEM: ATOMS id type x y z radius"]
    atom += [f"{i+1} 1 " + " ".join("%g" % x for x in [*xyz[i], .001]) for i in range(2)]
    area = intersection_disc_area(.001, .001, .0005)
    ct = [*map(lambda x: "%g" % x, xyz[0] + xyz[1]), "1", "2", "0"] + ["0"] * 12 + ["%g" % area, "0.0005"]
    contact = ["ITEM: TIMESTEP", "100", "ITEM: NUMBER OF ENTRIES", "1"] + box + [
        "ITEM: ENTRIES " + " ".join(f"c_cpl[{i}]" for i in range(1, 24)), " ".join(ct)]
    scaffold = [",".join(["1", *(f"{x:.12f}" for x in [*p, .001])]) for p in xyz]
    return [scaffold, atom, contact]


def put(lines, fi, row, col, val):
    sep = "," if fi == 0 else " "
    tok = lines[fi][row].split(sep)
    tok[col] = val
    lines[fi][row] = sep.join(tok)


def save(tag, lines):
    paths = [TMP / f"{tag}_{n}" for n in ("sc.csv", "atom.dump", "contact.dump")]
    for p, v in zip(paths, lines):
        p.write_text("\n".join(v) + "\n", encoding="utf8")
    return paths


def codes(x):
    return [r["code"] for r in x["rejections"]]


def consume(j, ledger=None, sid=None):
    ledger = NORMAL_LEDGER if ledger is None else ledger
    sid = NORMAL_SID if sid is None else sid
    p = S.am_iface_plan(ledger, {"AM_P|AM_P": .001}, join=j,
                       gap_law="cut", unreg_law="cut", ambiguous_arm="cut")
    out = {"plan_codes": codes(p), "plan_join_status": p["record"]["iface_join"]["status"]}
    try:
        S.iface_require_quantitative(p, sid=sid, vox=.25)
        out["quantitative"] = "ACCEPT"
    except Exception as e:
        out["quantitative"] = f"{type(e).__name__}: {e}"
    return out


normal = J.am_iface_join(*save("normal", standard()), type_map=TM)
with contextlib.redirect_stdout(io.StringIO()):
    NORMAL_SID, _ = S.rasterize(*(normal["particles"][k] for k in ("c_um", "r_um", "t")),
                                None, None, (0, 0, 0), (6, 4, 4), .25, bridge_um=.24)
NORMAL_LEDGER = S.am_iface_ledger(*(normal["particles"][k] for k in ("c_um", "r_um", "t")),
                                 NORMAL_SID, NORMAL_SID, (0, 0, 0), .25,
                                 delta_bound_um=normal["g_geo"]["delta_bound_um"], bridge_um=.24)


def run(tag, edit=None, kwargs=None, lines=None, do_consume=True):
    ls = standard() if lines is None else lines
    if edit:
        edit(ls)
    try:
        with warnings.catch_warnings(record=True) as ws:
            warnings.simplefilter("always")
            j = J.am_iface_join(*save(tag, ls), type_map=TM, **(kwargs or {}))
        out = {"status": j["status"], "codes": codes(j), "entrance": j["entrance"],
               "g_geo": j["g_geo"], "g_frame": j["g_frame"],
               "particles_finite": bool(np.isfinite(j["particles"]["c_um"]).all() and np.isfinite(j["particles"]["r_um"]).all()),
               "dem_area_finite": bool(np.isfinite(j["dem_am_am"]["area_um2"]).all()),
               "warnings": [str(w.message) for w in ws]}
        if do_consume:
            out.update(consume(j))
        RESULT["cases"][tag] = out
        return j
    except Exception as e:
        RESULT["cases"][tag] = {"exception": type(e).__name__, "message": str(e)}
        return None


run("normal")
tokens = {
    "exp_pos": "1e309", "exp_neg": "-1e309",
    "fixed_pos": "1" + "0" * 309 + ".000000000000",
    "fixed_neg": "-1" + "0" * 309 + ".000000000000",
}
for col, name in enumerate(("x", "y", "z", "radius"), 1):
    for kind, tok in tokens.items():
        run(f"scaffold_{name}_{kind}", lambda ls, c=col, t=tok: put(ls, 0, 1, c, t))
    for sign, tok in (("pos", "1e306"), ("neg", "-1e306")):
        run(f"scaffold_{name}_unit_overflow_{sign}", lambda ls, c=col, t=tok: put(ls, 0, 1, c, t))

for col, name in enumerate(("x", "y", "z", "radius"), 2):
    for kind, tok in (("pos", "1e309"), ("neg", "-1e309")):
        run(f"atom_{name}_overflow_{kind}", lambda ls, c=col, t=tok: put(ls, 1, 9, c, t))
for col in (0, 1, 2, 3, 4, 5, 8, 21, 22):
    for kind, tok in (("pos", "1e309"), ("neg", "-1e309")):
        run(f"contact_col{col}_overflow_{kind}", lambda ls, c=col, t=tok: put(ls, 2, 9, c, t))
for fi in (1, 2):
    for row in (5, 6, 7):
        for col in (0, 1):
            run(f"box_f{fi}_r{row}_c{col}", lambda ls, f=fi, r=row, c=col: put(ls, f, r, c, "1e309"))

# Every consumed integer position, beyond either int64 endpoint.
int_positions = [(0, 0, 0, "sc_type"), (1, 9, 0, "atom_id"), (1, 9, 1, "atom_type"),
                 (2, 9, 6, "contact_id1"), (2, 9, 7, "contact_id2")]
for fi in (1, 2):
    for row, label in ((1, "step"), (3, "count")):
        int_positions.append((fi, row, 0, f"f{fi}_{label}"))
for fi, row, col, name in int_positions:
    for kind, tok in (("over", str(2**63)), ("under", str(-2**63-1)), ("long", "9" * 5000)):
        run(f"int_{name}_{kind}", lambda ls, f=fi, r=row, c=col, t=tok: put(ls, f, r, c, t))

# Exact endpoint identifiers can match: no truncation through float.
for name, tok in (("i64_max", str(2**63-1)), ("i64_min", str(-2**63)), ("i64_leading_zeros", "0"*5000+"1")):
    run(name, lambda ls, t=tok: (put(ls, 1, 9, 0, t), put(ls, 2, 9, 6, t)))
for name, tok in (("step_i64_max", str(2**63-1)), ("step_i64_min", str(-2**63))):
    run(name, lambda ls, t=tok: (put(ls, 1, 1, 0, t), put(ls, 2, 1, 0, t)))

# RIMPR-03: accepted Unicode decimal digits preserve numerical identity.
def unicode_ints(ls):
    trans = str.maketrans("0123456789", "０１２３４５６７８９")
    for fi, row, col, _ in int_positions:
        sep = "," if fi == 0 else " "
        put(ls, fi, row, col, ls[fi][row].split(sep)[col].translate(trans))
    put(ls, 0, 1, 0, "１")
    put(ls, 1, 10, 0, "２")
    put(ls, 1, 10, 1, "１")
u = run("unicode_fullwidth_integers", unicode_ints)
RESULT["unicode_numeric_equivalence"] = {
    "particles_equal": u is not None and u["fp_particles"] == normal["fp_particles"],
    "atom_ids_equal": u is not None and np.array_equal(u["atom_id_of_row"], normal["atom_id_of_row"])}

# Float canonical format is tested separately from integer grammar.
for tok, name in (("+0.002", "plus"), ("0.0020", "trailing_zero"),
                  ("2e-03", "alternative_exponent"), ("０.００２", "fullwidth"),
                  ("0.0_02", "underscore"), ("0x1p-9", "hex"), ("1e-9999", "underflow")):
    run(f"atom_format_{name}", lambda ls, t=tok: put(ls, 1, 9, 2, t))
RESULT["int_token_boundaries"] = []
for tok in [str(-2**63-1), str(-2**63), str(2**63-1), str(2**63), "０", "１", "١", "1_0", "1.0", "+0001", "-0000", "0"*5000+"1"]:
    entry = {"token": tok if len(tok) < 80 else f"{tok[:10]}...[{len(tok)} chars]"}
    try:
        entry["result"] = J._int_token(tok)
    except Exception as e:
        entry["exception"] = type(e).__name__
        entry["message"] = str(e)
    RESULT["int_token_boundaries"].append(entry)


def one_far(tok="1e+160"):
    ls = standard()
    ls[0] = [ls[0][0]]
    put(ls, 0, 0, 1, "1" + "0"*int(tok.split("+")[-1]) + ".000000000000")
    ls[1][3] = "1"
    ls[1] = ls[1][:10]
    put(ls, 1, 9, 2, tok)
    ls[2][3] = "0"
    ls[2] = ls[2][:9]
    return ls


for exp in (150, 159, 160, 200, 305, 306):
    j = run(f"one_far_1e{exp}", lines=one_far(f"1e+{exp}"), do_consume=False)
    if j is None or "delta_bound_um" not in j["g_geo"]:
        continue
    out = RESULT["cases"][f"one_far_1e{exp}"]
    # Call actual ledger API using derived bound; no raster allocation at astronomical scales.
    tiny = np.zeros((2, 2, 2), np.int8)
    try:
        with warnings.catch_warnings(record=True) as ws:
            warnings.simplefilter("always")
            led = S.am_iface_ledger(*(j["particles"][k] for k in ("c_um", "r_um", "t")),
                                    tiny, tiny, (0, 0, 0), .25,
                                    delta_bound_um=j["g_geo"]["delta_bound_um"], bridge_um=.24)
        out["matching_ledger"] = {"status": "RETURN", "codes": codes(led), "warnings": [str(w.message) for w in ws]}
        out["matching_ledger"].update(consume(j, led, tiny))
    except Exception as e:
        out["matching_ledger"] = {"exception": type(e).__name__, "message": str(e)}
    # Same particles, independently supplied finite bound: clarify actual consumer protection.
    if exp == 160:
        try:
            with warnings.catch_warnings(record=True) as ws:
                warnings.simplefilter("always")
                led = S.am_iface_ledger(*(j["particles"][k] for k in ("c_um", "r_um", "t")),
                                        tiny, tiny, (0, 0, 0), .25, delta_bound_um=.001, bridge_um=.24)
            out["finite_bound_override"] = {"codes": codes(led), "warnings": [str(w.message) for w in ws], **consume(j, led, tiny)}
        except Exception as e:
            out["finite_bound_override"] = {"exception": type(e).__name__, "message": str(e)}

# Known-scale data with a non-AM pair: frame checks apply to all contact rows.
def huge_nonam(ls, exponent=160, bound_box=False):
    ls[1][3] = "4"
    x1, x2 = f"1e+{exponent}", f"2e+{exponent}"
    ls[1] += [f"3 2 {x1} 0.002 0.002 0.001", f"4 2 {x2} 0.002 0.002 0.001"]
    ls[2][3] = "2"
    ct = [x1, "0.002", "0.002", x2, "0.002", "0.002", "3", "4", "0"] + ["0"]*12 + ["1e-06", "0.0005"]
    ls[2].append(" ".join(ct))
    if bound_box:
        ls[1][5] = ls[2][5] = f"0 3e+{exponent}"
run("huge_nonam_frame_distance", huge_nonam)
run("huge_nonam_inside_box", lambda ls: huge_nonam(ls, bound_box=True))
run("huge_nonam_1e150_control", lambda ls: huge_nonam(ls, exponent=150, bound_box=True))
run("finite_custom_scale_contact_area_overflow", kwargs={"sim_to_um": 1e160}, do_consume=False)

if not BASELINE:
    for label, sc, atom, contact, tm in [
        ("real14", "docs/data/real14_am_scaffold.csv",
         "docs/data/real14_reference_20260928/atom_2060000.liggghts.gz",
         "docs/data/real14_reference_20260928/contact_2060000.liggghts.gz",
         {1: "AM_P", 2: "AM_S", 3: "SE"}),
        ("case15", "docs/data/case15_corner_20261001/case15_am_scaffold.csv",
         "docs/data/case15_corner_20261001/atom_v4_1710000.liggghts.gz",
         "docs/data/case15_corner_20261001/contact_v4_1710000.liggghts.gz", TM)]:
        j = J.am_iface_join(SRC/sc, SRC/atom, SRC/contact, type_map=tm)
        RESULT[label] = {"status": j["status"], "codes": codes(j), "entrance": j["entrance"], "g_geo": j["g_geo"]}

outpath = ROOT / "evidence" / ("numeric_" + TAG + ".json")
outpath.write_text(json.dumps(RESULT, ensure_ascii=False, indent=2), encoding="utf8")
print(json.dumps({"file": str(outpath), "n_cases": len(RESULT["cases"]),
                  "counts": {status: sum(v.get("status", "EXCEPTION") == status for v in RESULT["cases"].values())
                             for status in ("PASS", "REJECT", "EXCEPTION")}}, ensure_ascii=False))
