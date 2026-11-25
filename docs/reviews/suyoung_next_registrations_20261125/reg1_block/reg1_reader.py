"""Reader for the Suyoung 2D registration 1 (contact mini): J1-J5, first force, watch, §5 decision.

DEVELOPMENT_ONLY.  Reads a returned run folder and writes summary.json; it never steps the MPM
(the driver's run_arm and ArmRunner are replaced by refusals and every refusal is counted).

    python3 -I -X utf8 -B reg1_reader.py selfcheck ROOT
    python3 -I -X utf8 -B reg1_reader.py summary ROOT RUN
    python3 -I -X utf8 -B reg1_reader.py replay ROOT RUN RETURN_DIRECTORY RECEIPT_OUT

Registered rules (docs/reviews/suyoung_next_registrations_20261125/reg1_contact_mini_20261125.md §4-§5):
  * J1 = the U6(c) ⑥ force rule, executed from its pinned file (force_rule.compare: closed common
    support [0, smaller end], union of native displacements, linear interpolation, 20 N <= D on
    unrounded values) for 16↔32 and 24↔48 (judged) and 8↔16, 32↔48 (report).  The pair verdicts are
    combined by the same file's `aggregate` (any valid exceedance -> EXCEEDS, all within -> CONVERGED,
    otherwise HOLD).
  * J2 = max |top force - bottom force| / max |bottom force| <= 0.05 (exact 1/20, force_rule.exceeds).
  * J3 = force_rule.compare(σ_b^G2(u), σ_b^G1(u/2)) per cell, judged at 32 and 48, V0/4 arms that pass J2.
  * J4 (report) = ρ = σ_b / (4.924 MPa x ε) at ε = (u - 2 g_p)/D = 0.01, 0.02, 0.04 on the elastic one-disk arms.
  * J5 (report) = knee stress and post-knee slope of σ_b and of the volume-average σ_yy (ΣV0τ_yy / ΣV0J,
    recorded by the driver for one-disk arms; compression positive here) on the plastic one-disk V0/4 arms.
  * watch (§4-4, a violation holds that arm): two-disk lateral offset |Δx| <= 0.01 D, side wall hits 0,
    floor penetration <= 2e-12, non-finite values 0.
Reader interpretations fixed before any result are listed in READER_RULES (they go into summary.json).
"""
import csv
import dataclasses
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import sys
from types import SimpleNamespace

import numpy as np


HERE = Path(__file__).resolve().parent


def _sibling(name):
    spec = importlib.util.spec_from_file_location("reg1_reader_" + name, HERE / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


Q = _sibling("reg1_queue")
LABEL = "DEVELOPMENT_ONLY"
REGISTRATION_NAME = "reg1_contact_mini_20261125"
J1_JUDGED = ((16, 32), (24, 48))
J1_REPORTED = ((8, 16), (32, 48))
J1_ORDER = ((8, 16), (16, 32), (24, 48), (32, 48))
J3_CELLS = (32, 48)
J4_EPS = (.01, .02, .04)
J4_SLOPE_MPA = 4.924
J4_BAND = .20
NZ22 = dict(source="litdb-canon:nezamabadi2022_mpm_cd_plastic_particle_compaction", status="card reading, report only",
            knee_stress_MPa=[.40, .42], knee_eps=[.035, .04], post_knee_slope_MPa=.7)
SERIES = ("G1-PLATE-P-V0", "G1-PLATE-P-V4", "G1-PLATE-E-V4", "G2-S-P-V0", "G2-F2-P-V0", "G2-S-P-V4",
          "G2-S-E-V4", "G2-F2-P-V4", "G2-F2-E-V4", "G2-F1-P-V4")
J3_KEYS = (("S", "P"), ("F2", "P"), ("S", "E"), ("F2", "E"), ("F1", "P"))
DECISION_ROWS = ((1, "MINI_PLATE_NOT_CONVERGED"), (2, "MINI_SPEED_BRANCH_PLATE"), (3, "MINI_TWO_BODY_CONVERGED"),
                 (4, "MINI_IDENTITY_HELD"), (5, "MINI_CONVERGED_OFF_IDENTITY"), (6, "MINI_SPEED_BRANCH_CONTACT"),
                 (7, "MINI_INTERPARTICLE_NOT_CONVERGED"))
TECHNICAL, HELD, GAP_FLAG = "TECHNICAL_INCOMPLETE", "MINI_HELD", "MINI_GAP_CORRECTION_HURTS"
THRESHOLDS = dict(J1="20 N <= D on unrounded values (rule.json U6c-06, executed from force_rule.py)",
                  J1_judged_pairs=[list(p) for p in J1_JUDGED], J1_reported_pairs=[list(p) for p in J1_REPORTED],
                  J2_Q_max="1/20", J3_I_max="1/20", J3_cells=list(J3_CELLS), J4_eps=list(J4_EPS),
                  J4_slope_MPa=J4_SLOPE_MPA, J4_band=J4_BAND, first_force_MPa=.008, lateral_limit_D=.01,
                  side_wall_hits_max=0, floor_penetration_max=2e-12, nonfinite_max=0)
READER_RULES = dict(
    J2_support="each arm's own native samples on [0, its end displacement] (top and bottom force share them)",
    J3_combination="U6(c) aggregate over the judged cells 32 and 48: a valid exceedance is a mismatch, "
                   "both within is a match, otherwise held (hold kind J2 when every held judged cell is a J2 hold)",
    J3_inputs="V0/4 arms, same cells, same material; the one-disk arm read at u/2 (u_G2 = 2 u_G1)",
    J5_method="continuous two-segment least squares on samples with ε >= 0, hinge at a native sample with >= 3 "
              "samples on the left and >= 2 on the right; σ_yy is taken compression positive (-recorded value)",
    decision="first row among 1-7 that is TRUE in three-valued logic (HOLD = unknown); rows still unknown above "
             "it are listed; no TRUE row -> MINI_HELD",
    row7_plate_condition="'(G1 수렴)' read as the plastic one-disk V0/4 J1 converged",
    row4_condition="J1 parts of 'converging contact X' true and J3 held only by J2 holds",
    lateral_watch="two-disk arms only (§4-4 names the upper disk of G2); the one-disk value is reported",
    technical="RELEASE or manifest differs, execution record missing, incomplete or with a retry, "
              "CPUs not two distinct physical cores, worker rc 1 or 2, or an arm whose sources, environment, "
              "affinity, threads or registered configuration differ -> TECHNICAL_INCOMPLETE, no physics")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _json_safe(value):
    """Non-finite floats become null (they can only sit in report fields of held arms)."""
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    return value


def canonical(value):
    return json.loads(json.dumps(_json_safe(value), sort_keys=True, allow_nan=False))


def load(root):
    """Pinned driver, U6(c) force rule and engine over ROOT, with the solver entry points refused."""
    root = Path(root).resolve()
    driver = Q.load_pinned(root, Q.DRIVER, "reg1_reader_driver")
    force = Q.load_pinned(root, Q.FORCE_RULE, "reg1_reader_force_rule")
    for relative in (Q.RULE_JSON, Q.DOUBLING, Q.REGISTRATION):
        Q.check_pin(root, relative)
    Q.require(force.RULE_SHA256 == Q.PINS[Q.RULE_JSON] and force.PREVIOUS_SHA256 == Q.PINS[Q.DOUBLING],
              "force rule pins")
    engine = driver.Engine(root)
    calls = {"count": 0}

    def refuse(*_args, **_kwargs):
        calls["count"] += 1
        raise RuntimeError("solver call during read refused")
    driver.run_arm = refuse
    driver.ArmRunner = refuse
    arms = {a.name: a for a in driver.reg1_arms()}
    Q.require(set(arms) == {f"R1-{s}-{n:02d}" for s in SERIES for n in driver.REG1_CELLS}, "registered arm table")
    return SimpleNamespace(root=root, driver=driver, engine=engine, force=force, curves=force.curves, arms=arms,
                           solver_calls=calls)


def first_force(rows, threshold, u_geo, diameter):
    """First native sample after the initial one with σ_b strictly above the noise floor."""
    out = dict(threshold_MPa=threshold, u_geo=u_geo, u_on=None, step_on=None, u_on_minus_u_geo=None,
               u_on_minus_u_geo_over_D=None)
    for k, (u, sigma) in enumerate(rows):
        if k and sigma > threshold:
            out.update(u_on=u, step_on=k, u_on_minus_u_geo=u - u_geo, u_on_minus_u_geo_over_D=(u - u_geo) / diameter)
            break
    return out


def _finish(rec):
    rec["reasons"] = sorted(set(rec["reasons"]))
    rec["block_errors"] = sorted(set(rec["block_errors"]))
    rec["usable"] = not rec["reasons"] and not rec["block_errors"]
    return rec


def read_arm(ctx, name, folder, row, physical_cores, target_environment, parse_trace=True):
    """One returned arm: identity (block level), record consistency, trace, watch, first force."""
    d, e = ctx.driver, ctx.engine
    arm = ctx.arms[name]
    folder = Path(folder)
    g, plan = e.geometry(arm), e.plan(arm)
    rec = dict(name=name, series=name[3:-3], cells=arm.cells, rc=row.get("rc"), usable=False, reasons=[],
               block_errors=[], result_status=None, steps_done=None, trace_sha256=None, monitors=None,
               first_force=None, curve=None, forces=None, sigma_yy=None, u_geo=g["u_geo"])
    reasons, blocks = rec["reasons"], rec["block_errors"]
    rc, cpu = row.get("rc"), row.get("cpu")
    if rc in (1, 2):
        blocks.append(f"WORKER_RC_{rc} {name}")
    if rc != 0:
        reasons.append(f"RC_{rc}")
    if row.get("killed"):
        reasons.append("KILLED_AFTER_LIMIT")
    if list(row.get("physical_core") or []) != list(physical_cores.get(cpu, [None])):
        blocks.append(f"CORE_ASSIGNMENT {name} physical core")
    if (folder / "incomplete.json").exists():
        reasons.append("INCOMPLETE_JSON")
    paths = {n: folder / n for n in ("trace.csv", "result.json", "receipt.json")}
    if not all(p.is_file() for p in paths.values()):
        reasons.append("MISSING_FILES")
        return _finish(rec)
    try:
        result_raw = paths["result.json"].read_bytes()
        result = json.loads(result_raw)
        Q.require(isinstance(result, dict), "result")
    except (OSError, ValueError):
        reasons.append("RESULT_UNREADABLE")
        return _finish(rec)
    rec.update(result_status=result.get("status"), steps_done=result.get("steps_done"))
    if result.get("sources") != e.source_record():
        blocks.append(f"SOURCE_IDENTITY {name}")
    env = result.get("environment") if isinstance(result.get("environment"), dict) else {}
    if (env.get("python"), env.get("numpy")) != tuple(target_environment):
        blocks.append(f"ENVIRONMENT_IDENTITY {name} python={env.get('python')} numpy={env.get('numpy')}")
    if env.get("affinity") != [cpu] or env.get("threads") != {k: "1" for k in d.THREAD_VARIABLES}:
        blocks.append(f"CORE_ASSIGNMENT {name} affinity or threads")
    expected = dict(label=d.LABEL, physics_result=False, registration="reg1", arm=dataclasses.asdict(arm),
                    schedule_kind="RUN", plan=plan, dt=plan["dt"], grid=plan["grid"], points=plan["points"],
                    disks=g["disks"], box_width=e.const.MINI_WIDTH, floor=e.const.LO, initial_height=g["h0"],
                    limit_s=plan["limit_s"], steps_scheduled=plan["steps"], steps_planned=plan["steps"],
                    stage3_go=False, three_dimensional_go=False)
    for key, value in expected.items():
        if canonical(result.get(key)) != canonical(value):
            blocks.append(f"ARM_IDENTITY {name} {key}")
    if result.get("status") != "COMPLETE":
        reasons.append(f"STATUS_{result.get('status')}")
    if result.get("steps_done") != plan["steps"]:
        reasons.append("STEPS_INCOMPLETE")
    if not parse_trace:
        return _finish(rec)
    raw = paths["trace.csv"].read_bytes()
    rec["trace_sha256"] = sha(raw)
    if rec["trace_sha256"] != result.get("trace_sha256"):
        reasons.append("TRACE_SHA")
    try:
        receipt = json.loads(paths["receipt.json"].read_bytes())
        if receipt != dict(d.read_receipt(folder, result), result_sha256=sha(result_raw)):
            reasons.append("RECEIPT_MISMATCH")
    except (OSError, ValueError, KeyError, IndexError, TypeError):
        reasons.append("RECEIPT_MISMATCH")
    parsed = _parse_trace(ctx, arm, raw, result.get("steps_done"))
    if parsed is None:
        reasons.append("TRACE_FORMAT")
        return _finish(rec)
    values, nonfinite = parsed
    heights = [h for _, _, h, _ in e.schedule(arm, 1.)]
    trace_heights, trace_u = values["height"], values["u"]
    if (trace_heights[0] != g["h0"] or trace_u[0] != 0. or len(trace_heights) - 1 > len(heights)
            or any(h != s for h, s in zip(trace_heights[1:], heights))
            or any(u != g["h0"] - h for u, h in zip(trace_u[1:], trace_heights[1:]))):
        reasons.append("SCHEDULE")
    monitors = _watch(ctx, arm, values, nonfinite, result.get("monitors"))
    reasons += monitors.pop("violations")
    curve = list(zip(trace_u, values["bottom_MPa"]))
    first = None
    if not nonfinite:
        first = first_force(curve, e.const.THETA_MPA, g["u_geo"], e.const.D)
        recorded = result.get("first_force") if isinstance(result.get("first_force"), dict) else {}
        if any(recorded.get(k) != first[k] for k in ("u_on", "step_on", "u_geo", "u_on_minus_u_geo")):
            reasons.append("FIRST_FORCE_MISMATCH")
    rec.update(monitors=monitors, first_force=first, curve=curve,
               forces=list(zip(values["top_force"], values["bottom_force"])),
               sigma_yy=values.get("sigma_yy_avg_MPa"))
    return _finish(rec)


def _parse_trace(ctx, arm, raw, steps_done):
    """Trace columns as floats (None on a format error) and the count of non-finite values."""
    d = ctx.driver
    try:
        rows = list(csv.reader(io.StringIO(raw.decode("ascii"), newline="")))
    except (UnicodeDecodeError, csv.Error):
        return None
    if not rows or tuple(rows[0]) != tuple(d.COLUMNS) or not isinstance(steps_done, int) or len(rows) != steps_done + 2:
        return None
    index = {c: i for i, c in enumerate(d.COLUMNS)}
    numeric = ["step", "time_code", "height", "bottom_pressure_E", "u", "bottom_force", "top_force", "bottom_MPa",
               "top_MPa", "kinetic_energy", "momentum_y", "momentum_residual", "upper_center_x", "upper_dx_over_D",
               "side_wall_hits", "floor_max_penetration"]
    empty = ["phi_m"]
    for column in ("sigma_yy_avg_MPa",):
        (numeric if arm.geometry == "G1" else empty).append(column)
    for column in ("interfield_normal_impulse", "two_field_nodes", "multi_field_nodes"):
        (numeric if arm.contact in d.F_CONTACTS else empty).append(column)
    values = {c: [] for c in numeric}
    nonfinite = 0
    for k, row in enumerate(rows[1:]):
        if (len(row) != len(d.COLUMNS) or row[index["step"]] != str(k)
                or row[index["phase"]] != ("INITIAL" if k == 0 else "LOAD")
                or any(row[index[c]] != "" for c in empty)):
            return None
        for column in numeric:
            try:
                value = float(row[index[column]])
            except ValueError:
                return None
            if not math.isfinite(value):
                nonfinite += 1
            values[column].append(value)
    return values, nonfinite


def _watch(ctx, arm, values, nonfinite, recorded):
    """§4-4 technical watch recomputed from the trace, and its agreement with the driver's record."""
    d = ctx.driver
    finite = [abs(v) for v in values["upper_dx_over_D"] if math.isfinite(v)]
    lateral = max(finite, default=0.)
    side = sum(v for v in values["side_wall_hits"] if math.isfinite(v))
    penetration = max((v for v in values["floor_max_penetration"] if math.isfinite(v)), default=0.)
    residual = max((abs(v) for v in values["momentum_residual"] if math.isfinite(v)), default=0.)
    watch = arm.geometry == "G2"
    first_lateral = next((k for k, v in enumerate(values["upper_dx_over_D"]) if abs(v) > d.LATERAL_LIMIT_D), None)
    violations = []
    if watch and first_lateral is not None:
        violations.append("LATERAL_OFFSET")
    if side > 0:
        violations.append("SIDE_WALL_CONTACT")
    if penetration > d.PENETRATION_LIMIT:
        violations.append("FLOOR_PENETRATION")
    if nonfinite:
        violations.append("NONFINITE")
    recorded = recorded if isinstance(recorded, dict) else {}
    if not nonfinite and (recorded.get("max_abs_upper_dx_over_D") != lateral
                          or recorded.get("side_wall_hits_total") != side
                          or recorded.get("max_floor_penetration") != penetration):
        violations.append("RESULT_TRACE_MISMATCH")
    return dict(lateral_watch_applies=watch, lateral_limit_D=d.LATERAL_LIMIT_D, max_abs_upper_dx_over_D=lateral,
                first_lateral_violation_step=first_lateral, side_wall_hits_total=side,
                max_floor_penetration=penetration, penetration_limit=d.PENETRATION_LIMIT, nonfinite_values=nonfinite,
                max_abs_momentum_residual=residual,
                driver_technical_hold_reasons=recorded.get("technical_hold_reasons"), violations=violations)


def j1_pair(ctx, coarse, fine):
    base = dict(coarse_arm=coarse["name"], fine_arm=fine["name"], coarse_trace_sha256=coarse.get("trace_sha256"),
                fine_trace_sha256=fine.get("trace_sha256"))
    held = [r["name"] for r in (coarse, fine) if not r["usable"]]
    if held:
        return dict(base, **ctx.force.held("ARM_HELD"), held_arms=held)
    return dict(base, **ctx.force.compare(coarse["curve"], fine["curve"]))


def j1_verdict(ctx, pairs):
    """Judged pairs 16↔32 and 24↔48 combined by the U6(c) `aggregate` (its two slots, in order)."""
    first, second = ctx.force.PAIRS
    state = ctx.force.aggregate({first: pairs["16_32"], second: pairs["24_48"]})
    return {"WITHIN": "CONVERGED"}.get(state, state)


def j1_series(ctx, records, series):
    pairs = {}
    for coarse, fine in J1_ORDER:
        entry = j1_pair(ctx, records[f"R1-{series}-{coarse:02d}"], records[f"R1-{series}-{fine:02d}"])
        entry["judged"] = (coarse, fine) in J1_JUDGED
        pairs[f"{coarse}_{fine}"] = entry
    return dict(pairs=pairs, judged_pairs=["16_32", "24_48"], verdict=j1_verdict(ctx, pairs))


def j2(ctx, rec):
    if not rec["usable"]:
        return dict(status="HOLD", reason="ARM_HELD", quasi_static=None, Q=None, numerator_force=None,
                    denominator_force=None, samples=None)
    forces = rec["forces"]
    numerator = max((abs(t - b) for t, b in forces), default=0.)
    denominator = max((abs(b) for _, b in forces), default=0.)
    if not denominator > 0. or not math.isfinite(numerator):
        return dict(status="HOLD", reason="ZERO_BOTTOM_FORCE", quasi_static=None, Q=None, numerator_force=numerator,
                    denominator_force=denominator, samples=len(forces))
    exceeds = ctx.force.exceeds(float(numerator), float(denominator))
    return dict(status="NOT_QUASI_STATIC" if exceeds else "QUASI_STATIC", reason=None, quasi_static=not exceeds,
                Q=numerator / denominator, numerator_force=numerator, denominator_force=denominator,
                samples=len(forces))


def j3_cell(ctx, g2, g1, g2_quasi, g1_quasi):
    base = dict(g2_arm=g2["name"], g1_arm=g1["name"])
    held = [r["name"] for r in (g2, g1) if not r["usable"]]
    if held:
        return dict(base, **ctx.force.held("ARM_HELD"), held_arms=held, hold_kind="TECHNICAL", I=None)
    if g2_quasi is not True or g1_quasi is not True:
        return dict(base, **ctx.force.held("J2_NOT_PASSED"), hold_kind="J2", I=None)
    result = ctx.force.compare(g2["curve"], [(2. * u, sigma) for u, sigma in g1["curve"]])
    return dict(base, **result, hold_kind=None if result["comparison"] != "HOLD" else "TECHNICAL",
                I=result.get("ratio"))


def j3_verdict(ctx, cells):
    first, second = ctx.force.PAIRS
    judged = [cells[str(n)] for n in J3_CELLS]
    state = ctx.force.aggregate({first: judged[0], second: judged[1]})
    if state != "HOLD":
        return {"WITHIN": "MATCH", "EXCEEDS": "MISMATCH"}[state], None
    kinds = [c.get("hold_kind") for c in judged if c.get("comparison", "HOLD") == "HOLD"]
    return "HOLD", "J2" if kinds and all(k == "J2" for k in kinds) else "TECHNICAL"


def j3(ctx, records, j2s, contact, material):
    cells = {}
    for n in ctx.driver.REG1_CELLS:
        g2, g1 = records[f"R1-G2-{contact}-{material}-V4-{n:02d}"], records[f"R1-G1-PLATE-{material}-V4-{n:02d}"]
        cell = j3_cell(ctx, g2, g1, j2s[g2["name"]]["quasi_static"], j2s[g1["name"]]["quasi_static"])
        cell["judged"] = n in J3_CELLS
        cells[str(n)] = cell
    verdict, kind = j3_verdict(ctx, cells)
    return dict(cells=cells, judged_cells=list(J3_CELLS), verdict=verdict, hold_kind=kind)


def j4(ctx, rec, j2_result):
    if not rec["usable"] or j2_result.get("quasi_static") is not True:
        return dict(status="HOLD", reason="ARM_HELD" if not rec["usable"] else "J2_NOT_PASSED", points=None)
    axis = [u for u, _ in rec["curve"]]
    points = []
    for eps in J4_EPS:
        u = rec["u_geo"] + eps * ctx.engine.const.D
        try:
            sigma = ctx.curves.interpolate(u, axis, rec["curve"])
        except (ValueError, IndexError):
            return dict(status="HOLD", reason="OUTSIDE_TRACE", points=None)
        rho = sigma / (J4_SLOPE_MPA * eps)
        points.append(dict(eps=eps, u=u, sigma_b_MPa=sigma, rho=rho,
                           category="WITHIN_20_PERCENT" if abs(rho - 1.) <= J4_BAND else "OUTSIDE_20_PERCENT"))
    return dict(status="REPORTED", reason=None, points=points, slope_MPa=J4_SLOPE_MPA,
                eps_definition="(u - 2 g_p) / D", note="report only (reg1 §4-3)")


def hinge(x, y):
    """Continuous two-segment least squares; the hinge sits at a native sample (>= 3 left, >= 2 right)."""
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    n = len(x)
    if n < 5 or len(y) != n or not (np.isfinite(x).all() and np.isfinite(y).all()) or (np.diff(x) <= 0).any():
        return None
    mean = float(x.mean())
    xc = x - mean

    def suffix(v):
        return np.concatenate((np.cumsum(v[::-1])[::-1], [0.]))
    s1, s2, sy, sxy, syy = xc.sum(), (xc * xc).sum(), y.sum(), (xc * y).sum(), (y * y).sum()
    t1, t2, ty, txy = suffix(xc), suffix(xc * xc), suffix(y), suffix(xc * y)
    j = np.arange(2, n - 2)
    t = xc[j]
    c0 = (n - 1 - j).astype(float)
    c1, c2, cy, cxy = t1[j + 1], t2[j + 1], ty[j + 1], txy[j + 1]
    h1, hx, h2, hy = c1 - t * c0, c2 - t * c1, c2 - 2 * t * c1 + t * t * c0, cxy - t * cy
    a = np.empty((len(j), 3, 3))
    a[:, 0, 0], a[:, 1, 1], a[:, 2, 2] = n, s2, h2
    a[:, 0, 1] = a[:, 1, 0] = s1
    a[:, 0, 2] = a[:, 2, 0] = h1
    a[:, 1, 2] = a[:, 2, 1] = hx
    b = np.stack([np.full(len(j), sy), np.full(len(j), sxy), hy], axis=1)
    beta = np.linalg.solve(a, b[..., None])[..., 0]
    sse = syy - np.einsum("ki,ki->k", beta, b)
    k = int(np.argmin(sse))
    knee = int(j[k])
    b0, b1, b2 = (float(v) for v in beta[k])
    return dict(knee_eps=float(x[knee]), knee_MPa=b0 + b1 * float(xc[knee]), pre_knee_slope_MPa=b1,
                post_knee_slope_MPa=b1 + b2, samples=n, hinge_index=knee,
                rms_residual_MPa=math.sqrt(max(float(sse[k]), 0.) / n))


def j5(ctx, rec, j2_result):
    if not rec["usable"] or j2_result.get("quasi_static") is not True:
        return dict(status="HOLD", reason="ARM_HELD" if not rec["usable"] else "J2_NOT_PASSED")
    if rec["sigma_yy"] is None:
        return dict(status="HOLD", reason="NO_SIGMA_YY")
    diameter = ctx.engine.const.D
    points = [((u - rec["u_geo"]) / diameter, s, yy) for (u, s), yy in zip(rec["curve"], rec["sigma_yy"])
              if u >= rec["u_geo"]]
    eps = [p[0] for p in points]
    return dict(status="REPORTED", reason=None, samples=len(points), eps_definition="(u - 2 g_p) / D",
                sigma_b=hinge(eps, [p[1] for p in points]),
                compression_positive_sigma_yy_avg=hinge(eps, [-p[2] for p in points]),
                note="report only (reg1 §4-3); σ_yy = ΣV0τ_yy / ΣV0J recorded by the driver")


def _tv(verdict, true, false):
    return True if verdict == true else False if verdict == false else None


def _and(*values):
    if any(v is False for v in values):
        return False
    return True if all(v is True for v in values) else None


def _or(*values):
    if any(v is True for v in values):
        return True
    return False if all(v is False for v in values) else None


def decide(j1, j3_results):
    """§5: the first TRUE row among 1-7 (three-valued; HOLD = unknown), else MINI_HELD; row 8 is a flag."""
    conv = {s: _tv(v, "CONVERGED", "EXCEEDS") for s, v in j1.items()}
    exc = {s: _tv(v, "EXCEEDS", "CONVERGED") for s, v in j1.items()}
    g1v0, g1v4 = "G1-PLATE-P-V0", "G1-PLATE-P-V4"
    contacts = {}
    for x in ("S", "F2"):
        x0, x4, j = f"G2-{x}-P-V0", f"G2-{x}-P-V4", j3_results[f"{x}-P"]
        both = _and(conv[g1v0], conv[g1v4], conv[x0], conv[x4])
        match = _tv(j["verdict"], "MATCH", "MISMATCH")
        held_by_j2 = False if j["verdict"] != "HOLD" else (True if j.get("hold_kind") == "J2" else None)
        contacts[x] = dict(J1_V0=j1[x0], J1_V4=j1[x4], J3=j["verdict"], J3_hold_kind=j.get("hold_kind"),
                           j1_both_speeds_with_plate=both, converging_contact=_and(both, match),
                           identity_held_by_j2=_and(both, held_by_j2),
                           converged_off_identity=_and(both, _tv(j["verdict"], "MISMATCH", "MATCH")),
                           speed_branch=_and(conv[x4], exc[x0]), v4_exceeds=exc[x4])
    gap = _and(conv["G2-F1-P-V4"], exc["G2-F2-P-V4"])
    contacts["F1"] = dict(J1_V4=j1["G2-F1-P-V4"], J3=j3_results["F1-P"]["verdict"], gap_correction_flag=gap)
    values = {1: exc[g1v4], 2: _and(conv[g1v4], exc[g1v0]),
              3: _or(*(contacts[x]["converging_contact"] for x in ("S", "F2"))),
              4: _or(*(contacts[x]["identity_held_by_j2"] for x in ("S", "F2"))),
              5: _or(*(contacts[x]["converged_off_identity"] for x in ("S", "F2"))),
              6: _or(*(contacts[x]["speed_branch"] for x in ("S", "F2"))),
              7: _and(conv[g1v4], contacts["S"]["v4_exceeds"], contacts["F2"]["v4_exceeds"])}
    rows = [dict(row=n, code=code, value=values[n]) for n, code in DECISION_ROWS]
    decided = next((r for r in rows if r["value"] is True), None)
    stop = decided["row"] if decided else len(rows) + 1
    return dict(decision=decided["code"] if decided else HELD, flags=[GAP_FLAG] if gap is True else [], rows=rows,
                undetermined_rows_before_decision=[r["row"] for r in rows if r["row"] < stop and r["value"] is None],
                contacts=contacts)


def execution_problems(ctx, execution):
    if not isinstance(execution, dict):
        return ["EXECUTION_MISSING"]
    problems = []
    if execution.get("label") != LABEL:
        problems.append("EXECUTION_LABEL")
    if execution.get("complete") is not True:
        problems.append("EXECUTION_INCOMPLETE")
    if execution.get("retries") != 0:
        problems.append("EXECUTION_RETRIES")
    if execution.get("grace_s") != Q.GRACE_S:
        problems.append("EXECUTION_GRACE")
    arms = execution.get("arms") if isinstance(execution.get("arms"), dict) else {}
    if set(arms) != set(ctx.arms):
        problems.append("EXECUTION_ARMS")
    cpus, cores = execution.get("cpus"), execution.get("physical_cores")
    cores_ok = (isinstance(cpus, list) and len(cpus) == 2 and len(set(cpus)) == 2 and isinstance(cores, dict)
                and set(cores) == {str(c) for c in cpus} and len({tuple(v) for v in cores.values()}) == 2)
    if not cores_ok:
        problems.append("CORE_ASSIGNMENT two distinct physical cores")
    for name, row in arms.items():
        if not isinstance(row, dict) or row.get("arm") != name or row.get("attempts") != 1 or row.get("threads") != 1:
            problems.append(f"EXECUTION_ROW {name}")
        elif cores_ok and row.get("cpu") not in cpus:
            problems.append(f"CORE_ASSIGNMENT {name} cpu")
    return problems


def _read_optional(path):
    try:
        return Path(path).read_bytes()
    except OSError:
        return None


def summarize(root, run, target_environment=None, ctx=None):
    ctx = ctx or load(root)
    run = Path(run)
    target = tuple(Q.TARGET_ENVIRONMENT if target_environment is None else target_environment)
    errors = []
    for name in ("RELEASE", "SOURCE_SHA256SUMS"):
        ours, theirs = _read_optional(ctx.root / name), _read_optional(run / name)
        if ours is None or ours != theirs:
            errors.append(f"RUN_{name}_DIFFERS")
    release = (_read_optional(run / "RELEASE") or b"").decode("ascii", "replace").strip() or None
    manifest = _read_optional(run / "SOURCE_SHA256SUMS")
    try:
        execution = json.loads((run / "execution.json").read_bytes())
    except (OSError, ValueError):
        execution = None
    errors += execution_problems(ctx, execution)
    rows = execution.get("arms") if isinstance(execution, dict) and isinstance(execution.get("arms"), dict) else {}
    cores = {}
    if isinstance(execution, dict) and isinstance(execution.get("physical_cores"), dict):
        cores = {int(k): v for k, v in execution["physical_cores"].items() if str(k).lstrip("-").isdigit()}
    parse = not errors
    records = {}
    for name in ctx.arms:
        row = rows.get(name)
        if isinstance(row, dict):
            records[name] = read_arm(ctx, name, run / "arms" / name, row, cores, target, parse_trace=parse)
            errors += records[name]["block_errors"]
    common = dict(label=LABEL, registration=REGISTRATION_NAME, registration_sha256=Q.PINS[Q.REGISTRATION],
                  release=release, source_manifest_sha256=None if manifest is None else sha(manifest),
                  after_result_amendment=True, thresholds=THRESHOLDS, reader_rules=READER_RULES,
                  stage3_go=False, three_dimensional_go=False)
    arms = {n: dict(rc=r["rc"], result_status=r["result_status"], steps_done=r["steps_done"], usable=r["usable"],
                    reasons=r["reasons"]) for n, r in records.items()}
    execution_summary = None
    if isinstance(execution, dict):
        execution_summary = dict(cpus=execution.get("cpus"), physical_cores=execution.get("physical_cores"),
                                 retries=execution.get("retries"), complete=execution.get("complete"),
                                 timeouts=sum(1 for n, r in rows.items() if isinstance(r, dict) and
                                              (r.get("rc") == 124 or records.get(n, {}).get("result_status") == "TIME_LIMIT")),
                                 nonzero_rc=sorted(n for n, r in rows.items() if isinstance(r, dict) and r.get("rc") != 0))
    if errors:
        # Physics is not judged: arms are listed with their exit codes and reasons only.
        arms = {n: dict(a, usable=None) for n, a in arms.items()}
        return canonical(dict(common, decision=TECHNICAL, flags=[], block_errors=sorted(set(errors)),
                              decision_rows=None, undetermined_rows_before_decision=None, contacts=None, J1=None,
                              J2=None, J3=None, J4=None, J5=None, first_force=None, monitors=None, trace_sha256=None,
                              arms=arms, execution=execution_summary,
                              solver_calls_during_read=ctx.solver_calls["count"]))
    J1 = {s: j1_series(ctx, records, s) for s in SERIES}
    J2 = {n: j2(ctx, r) for n, r in records.items()}
    J3 = {f"{c}-{m}": j3(ctx, records, J2, c, m) for c, m in J3_KEYS}
    J4 = {n: j4(ctx, records[n], J2[n]) for n in sorted(records) if n.startswith("R1-G1-PLATE-E-V4-")}
    J5 = dict(nz22_reference=NZ22, arms={n: j5(ctx, records[n], J2[n]) for n in sorted(records)
                                         if n.startswith("R1-G1-PLATE-P-V4-")})
    decision = decide({s: J1[s]["verdict"] for s in SERIES},
                      {k: dict(verdict=v["verdict"], hold_kind=v["hold_kind"]) for k, v in J3.items()})
    return canonical(dict(common, decision=decision["decision"], flags=decision["flags"], block_errors=[],
                          decision_rows=decision["rows"],
                          undetermined_rows_before_decision=decision["undetermined_rows_before_decision"],
                          contacts=decision["contacts"], J1=J1, J2=J2, J3=J3, J4=J4, J5=J5,
                          first_force={n: r["first_force"] for n, r in records.items()},
                          monitors={n: r["monitors"] for n, r in records.items()},
                          trace_sha256={n: r["trace_sha256"] for n, r in records.items()}, arms=arms,
                          execution=execution_summary, solver_calls_during_read=ctx.solver_calls["count"]))


def write_summary(root, run, target_environment=None, ctx=None):
    summary = summarize(root, run, target_environment, ctx)
    with (Path(run) / "summary.json").open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(summary, stream, indent=2, sort_keys=True, allow_nan=False, ensure_ascii=False)
        stream.write("\n")
    return summary


def replay_summary(root, run, target_environment=None, ctx=None):
    summary = summarize(root, run, target_environment, ctx)
    try:
        archived = json.loads((Path(run) / "summary.json").read_bytes())
    except (OSError, ValueError):
        archived = None
    Q.require(archived == summary, "ARCHIVED_SUMMARY_MISMATCH")
    return summary


def return_receipt(ctx, run, return_directory, summary):
    run, return_directory = Path(run), Path(return_directory)
    execution = json.loads((run / "execution.json").read_bytes())
    arms = {}
    for name in sorted(execution["arms"]):
        row = execution["arms"][name]
        path = run / "arms" / name / "result.json"
        result = json.loads(path.read_bytes()) if path.is_file() else None
        arms[name] = dict(cpu=row["cpu"], physical_core=row["physical_core"], threads=row["threads"], rc=row["rc"],
                          steps=None if result is None else result["steps_done"],
                          status=result["status"] if result else ("KILLED" if row["killed"] else "INCOMPLETE"),
                          native_elapsed_s=None if result is None else result["elapsed_s"],
                          started_ns=str(row["started_ns"]), ended_ns=str(row["ended_ns"]),
                          elapsed_including_wrapper_s=row["elapsed_including_wrapper_s"])
    return dict(status="CONTACT_MINI_READBACK_COMPLETE", scope=LABEL, mode="READBACK",
                release=(run / "RELEASE").read_text("ascii").strip(),
                return_tar_sha256=sha((return_directory / Q.RESULT_TAR).read_bytes()),
                screen_sha256=sha((return_directory / "screen.txt").read_bytes()), readback_rc=0,
                solver_runs_during_readback=ctx.solver_calls["count"],
                timeouts=sum(1 for a in arms.values() if a["rc"] == 124 or a["status"] == "TIME_LIMIT"),
                retries=execution["retries"], decision=summary["decision"], flags=summary["flags"], arms=arms)


def report_lines(summary):
    lines = [f"DECISION {summary['decision']}", "FLAGS " + (",".join(summary["flags"]) or "none")]
    if summary["block_errors"]:
        lines += ["BLOCK_ERROR " + e for e in summary["block_errors"]]
        return lines
    for series, entry in summary["J1"].items():
        ratios = " ".join(f"{k}={'-' if p['ratio'] is None else format(100 * p['ratio'], '.4f') + '%'}"
                          f"({p['comparison']})" for k, p in entry["pairs"].items())
        lines.append(f"J1 {series} {entry['verdict']} {ratios}")
    for key, entry in summary["J3"].items():
        lines.append(f"J3 {key} {entry['verdict']}" + (f" hold_kind={entry['hold_kind']}" if entry["hold_kind"] else ""))
    held = sorted(n for n, a in summary["arms"].items() if not a["usable"])
    lines.append("HELD_ARMS " + (",".join(held) or "none"))
    lines.append("ROWS " + " ".join(f"{r['row']}={r['value']}" for r in summary["decision_rows"]))
    return lines


def selfcheck(root):
    """Exercise the packaged rules on hand-made inputs (no trace, no MPM step)."""
    ctx = load(root)
    checks = 0

    def rec(curve, forces=None):
        return dict(name="SELF", usable=True, curve=curve, forces=forces or [(s, s) for _, s in curve],
                    trace_sha256=None, u_geo=0., sigma_yy=None)

    def need(condition, text):
        nonlocal checks
        Q.require(condition, "reader self-check: " + text)
        checks += 1
    fine = rec([(0., 0.), (1., 20.), (2., 1000.)])
    within = j1_pair(ctx, rec([(0., 0.), (1., 21.)]), fine)
    above = j1_pair(ctx, rec([(0., 0.), (1., 21.01)]), fine)
    need(within["comparison"] == "WITHIN" and within["fine_peak_MPa"] == 20. and within["union_knots"] == 2, "J1 at 5 %")
    need(above["comparison"] == "EXCEEDS", "J1 above 5 %")
    W, E, H = ({"comparison": c} for c in ("WITHIN", "EXCEEDS", "HOLD"))
    need(j1_verdict(ctx, {"8_16": E, "16_32": W, "24_48": W, "32_48": E}) == "CONVERGED", "report pairs")
    need(j1_verdict(ctx, {"8_16": W, "16_32": E, "24_48": H, "32_48": W}) == "EXCEEDS", "exceedance survives a hold")
    need(j2(ctx, rec([(0., 0.), (1., 20.)], [(0., 0.), (21., 20.)]))["quasi_static"] is True, "J2 at 5 %")
    need(j2(ctx, rec([(0., 0.), (1., 20.)], [(0., 0.), (21.01, 20.)]))["quasi_static"] is False, "J2 above 5 %")
    cell = j3_cell(ctx, rec([(0., 0.), (2., 1.), (4., 3.)]), rec([(0., 0.), (1., 1.), (2., 3.)]), True, True)
    need(cell["comparison"] == "WITHIN" and cell["max_abs_difference_MPa"] == 0., "J3 u/2")
    need(first_force([(0., 0.), (1., .008), (2., .0081)], .008, 0., 1.)["u_on"] == 2., "first force strict")
    x = [i / 100 for i in range(21)]
    fit = hinge(x, [5 * v if v <= .08 else .4 + .7 * (v - .08) for v in x])
    need(abs(fit["knee_MPa"] - .4) < 1e-9 and abs(fit["post_knee_slope_MPa"] - .7) < 1e-9, "J5 hinge")
    j1 = {s: "CONVERGED" for s in SERIES}
    j3s = {f"{c}-{m}": dict(verdict="MATCH", hold_kind=None) for c, m in J3_KEYS}
    need(decide(j1, j3s)["decision"] == "MINI_TWO_BODY_CONVERGED", "row 3")
    need(decide(dict(j1, **{"G1-PLATE-P-V4": "EXCEEDS"}), j3s)["decision"] == "MINI_PLATE_NOT_CONVERGED", "row 1")
    seven = decide(dict(j1, **{"G2-S-P-V4": "EXCEEDS", "G2-F2-P-V4": "EXCEEDS"}), j3s)
    need(seven["decision"] == "MINI_INTERPARTICLE_NOT_CONVERGED" and seven["flags"] == [GAP_FLAG], "row 7 and flag")
    need(decide(dict(j1, **{"G1-PLATE-P-V4": "HOLD"}), j3s)["decision"] == HELD, "held")
    need(ctx.solver_calls["count"] == 0, "no solver call")
    return checks


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    mode = args.pop(0) if args else ""
    try:
        if mode == "selfcheck" and len(args) == 1:
            print(f"READER_SELFCHECK_OK checks={selfcheck(args[0])} solver_calls=0")
            return 0
        if mode == "summary" and len(args) == 2:
            print("\n".join(report_lines(write_summary(*args))))
            return 0
        if mode == "replay" and len(args) == 4:
            root, run, returned, out = args
            ctx = load(root)
            summary = replay_summary(root, run, ctx=ctx)
            receipt = return_receipt(ctx, run, returned, summary)
            with Path(out).open("x", encoding="utf-8", newline="\n") as stream:
                json.dump(receipt, stream, indent=2, sort_keys=True, allow_nan=False)
                stream.write("\n")
            print("\n".join(report_lines(summary)))
            print(f"READBACK_COMPLETE RETURN_RECEIPT={out} solver_runs={ctx.solver_calls['count']}")
            return 0
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as exc:
        print("REG1_READER_REFUSED", type(exc).__name__, exc)
        return 4
    print("usage: selfcheck ROOT | summary ROOT RUN | replay ROOT RUN RETURN_DIRECTORY RECEIPT_OUT")
    return 2


if __name__ == "__main__":
    sys.exit(main())
