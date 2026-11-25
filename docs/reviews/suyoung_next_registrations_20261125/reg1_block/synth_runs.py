"""Synthetic, format-faithful contact-mini (reg1) runs for the block tests.

DEVELOPMENT_ONLY test helper.  No MPM step is taken here: every stress, force and monitor value
is invented to exercise the execution block and its reader, and none of it is a physics result.
What is real is the format: the registered arm names, the registered schedule heights
(`Engine.schedule`), the trace columns, the result.json keys and the receipt.json, all taken from
the pinned thin driver (`driver.py`) and its own helpers (`Monitors`, `read_receipt`,
`write_json`, `csv_value`).

The invented loading curve is bilinear in ε = (u - u_geo)/D: 4.924 MPa per unit ε up to 0.40 MPa,
then 0.7 MPa per unit ε.  A two-disk arm gets σ_G2(u) = σ_G1(u/2) (the reg1 J3 identity), so an
unperturbed synthetic run is "converged" everywhere.  `Spec` perturbs single arms.
"""
import csv
import dataclasses
import hashlib
import importlib.util
import json
import math
from pathlib import Path


DRIVER_REL = "docs/reviews/suyoung_next_registrations_20261125/driver/driver.py"
ELASTIC_MPA, KNEE_MPA, PLASTIC_MPA = 4.924, .40, .7
CORES = {0: [0, 0], 1: [0, 1]}
_LOADED = {}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load_driver(root):
    """The pinned driver module and an Engine over `root` (cached per root)."""
    root = Path(root).resolve()
    if root not in _LOADED:
        spec = importlib.util.spec_from_file_location("synth_runs_driver", root / DRIVER_REL)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _LOADED[root] = (module, module.Engine(root))
    return _LOADED[root]


def base_sigma(eps):
    """Invented bilinear compression curve (MPa, compression positive)."""
    if eps <= 0.:
        return 0.
    knee = KNEE_MPA / ELASTIC_MPA
    return ELASTIC_MPA * eps if eps <= knee else KNEE_MPA + PLASTIC_MPA * (eps - knee)


def plate_sigma(arm, u, const, geometry):
    """σ_b at the arm's displacement u; a two-disk arm reads the one-disk curve at u/2."""
    if arm.geometry == "G1":
        return base_sigma((u - geometry["u_geo"]) / const.D)
    return base_sigma((u / 2. - geometry["u_geo"] / 2.) / const.D)


@dataclasses.dataclass
class Spec:
    scale: float = 1.            # multiplies σ_b on every step
    top_scale: float = 1.        # top force = top_scale x bottom force
    sigma: object = None         # optional callable(arm, u, const, geometry) -> σ_b in MPa
    lateral_D: float = 0.        # upper_dx_over_D on every step after the first
    side_hits_at: int = None     # one side-wall hit at this step
    penetration: float = 0.      # floor_max_penetration from step 1 on
    nan_at: int = None           # kinetic_energy is NaN at this step
    status: str = "COMPLETE"     # COMPLETE | TIME_LIMIT (half the steps) | INCOMPLETE (incomplete.json only)
    empty: bool = False          # leave the arm folder empty (rc 0)
    rc: int = None               # execution rc (default from status)
    tamper_sources: bool = False # one source sha in result.json changed
    affinity: list = None        # recorded affinity (default [cpu])


def default_rc(spec):
    if spec.rc is not None:
        return spec.rc
    return {"COMPLETE": 0, "TIME_LIMIT": 3, "INCOMPLETE": 4}[spec.status]


def environment(driver, cpu, spec):
    env = driver.environment()
    env["threads"] = {k: "1" for k in driver.THREAD_VARIABLES}
    env["affinity"] = [cpu] if spec.affinity is None else list(spec.affinity)
    return env


def write_arm(root, name, folder, cpu, spec=None, live_environment=False):
    """Write one synthetic arm folder in the driver's format; return the rc the driver would give."""
    spec = spec or Spec()
    driver, engine = load_driver(root)
    arm = {a.name: a for a in driver.reg1_arms()}[name]
    folder = Path(folder)
    folder.mkdir(parents=True)
    rc = default_rc(spec)
    if spec.empty:
        return rc
    const, g, plan = engine.const, engine.geometry(arm), engine.plan(arm)
    dt, width = engine.dt(arm.cells), const.MINI_WIDTH
    rows = engine.schedule(arm, 1.)
    done = {"COMPLETE": rows, "TIME_LIMIT": rows[:len(rows)//2], "INCOMPLETE": rows[:len(rows)//3]}[spec.status]
    x0 = .5
    initial = {k: 0 for k in driver.COLUMNS}
    initial.update(height=g["h0"], phase="INITIAL", phi_m=None, upper_center_x=x0, upper_dx_over_D=0,
                   sigma_yy_avg_MPa=0 if arm.geometry == "G1" else None)
    if arm.contact not in driver.F_CONTACTS:
        initial.update(interfield_normal_impulse=None, two_field_nodes=None, multi_field_nodes=None)
    monitors = driver.Monitors(mini=True)
    first = dict(threshold_MPa=const.THETA_MPA, u_geo=g["u_geo"], u_on=None, step_on=None,
                 u_on_minus_u_geo=None, sigma_b="bottom force / D x 10 MPa")
    sigma_of = spec.sigma or plate_sigma
    with (folder / "trace.csv").open("x", encoding="ascii", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(driver.COLUMNS)
        writer.writerow([driver.csv_value(initial[c]) for c in driver.COLUMNS])
        for k, phase, height, _ in done:
            u = g["h0"] - height
            pressure = sigma_of(arm, u, const, g) * spec.scale * const.D / (const.E_MPA * width)
            bottom_force = pressure * width
            top_force = spec.top_scale * bottom_force
            cx = x0 + spec.lateral_D * const.D
            rec = dict(step=k, time_code=k*dt, height=height, bottom_pressure_E=pressure, phi_m=None, phase=phase,
                       u=u, bottom_force=bottom_force, top_force=top_force,
                       bottom_MPa=bottom_force / const.D * const.E_MPA, top_MPa=top_force / const.D * const.E_MPA,
                       kinetic_energy=math.nan if spec.nan_at == k else 0., momentum_y=0., momentum_residual=0.,
                       upper_center_x=cx, upper_dx_over_D=(cx - x0) / const.D, sigma_yy_avg_MPa=None,
                       interfield_normal_impulse=None, two_field_nodes=None, multi_field_nodes=None,
                       side_wall_hits=1 if spec.side_hits_at == k else 0, floor_max_penetration=spec.penetration)
            if arm.geometry == "G1":
                rec["sigma_yy_avg_MPa"] = -.9 * rec["bottom_MPa"]
            if arm.contact in driver.F_CONTACTS:
                rec.update(interfield_normal_impulse=0., two_field_nodes=0, multi_field_nodes=0)
            writer.writerow([driver.csv_value(rec[c]) for c in driver.COLUMNS])
            monitors.update(k, rec)
            if first["u_on"] is None and rec["bottom_MPa"] > first["threshold_MPa"]:
                first.update(u_on=rec["u"], step_on=k, u_on_minus_u_geo=rec["u"] - first["u_geo"])
    steps_done = done[-1][0] if done else 0
    if spec.status == "INCOMPLETE":
        driver.write_json(folder / "incomplete.json", dict(label=driver.LABEL, arm=name, status="INCOMPLETE",
                                                           steps_done=steps_done, reason="synthetic failure"))
        return rc
    sources = engine.source_record()
    if spec.tamper_sources:
        first_key = sorted(sources)[0]
        sources[first_key] = "0" * 64
    started = 1_800_000_000_000_000_000
    env = driver.environment() if live_environment else environment(driver, cpu, spec)
    result = dict(
        label=driver.LABEL, physics_result=False, registration=arm.reg, arm=dataclasses.asdict(arm),
        schedule_kind="RUN", status=spec.status, steps_scheduled=len(rows), steps_planned=plan["steps"],
        steps_done=steps_done, elapsed_s=1.25, limit_s=plan["limit_s"], started_ns=started,
        ended_ns=started + 1_250_000_000, plan=plan, dt=dt, grid=round(arm.cells / const.D), points=plan["points"],
        disks=g["disks"], box_width=width, floor=const.LO, initial_height=g["h0"], sources=sources,
        seed_sha256=["0" * 64] * 3, boundary_sha256=["0" * 64] * 3,
        trace_sha256=sha((folder / "trace.csv").read_bytes()), final_state_sha256=["0" * 64] * 4,
        floor_audit=dict(steps=steps_done, max_penetration=spec.penetration),
        observer_calls=dict(other_walls=2 * steps_done, contact=steps_done),
        observed_functions=["material_floor._other_walls"],
        private_constants=dict(box_width=width, plate_speed_load=const.V0 / arm.load_div, plate_speed_unload=None,
                               material_yield="inf (registered elastic E)" if arm.material == "E" else "pinned 3a",
                               contact_friction_passed=.5),
        monitors=monitors.summary(), first_force=first, unloading=None, last_step_pairs=[], environment=env,
        stage3_go=False, three_dimensional_go=False,
        note="SYNTHETIC TEST ARM - invented numbers, no MPM step")
    driver.write_json(folder / "result.json", result)
    driver.write_json(folder / "receipt.json", dict(driver.read_receipt(folder, result),
                                                    result_sha256=sha((folder / "result.json").read_bytes())))
    return rc


def arm_names(root):
    driver, _ = load_driver(root)
    return [a.name for a in driver.reg1_arms()]


def write_run(root, run, specs=None, base=None, omit=(), cores=None, cpu_of=None, retries=0):
    """A whole synthetic run folder: RELEASE, SOURCE_SHA256SUMS, arms/, logs/, execution.json.

    Arms not in `specs` are symlinked from `base` (an earlier synthetic run) when it is given.
    """
    root, run = Path(root), Path(run)
    specs = specs or {}
    cores = CORES if cores is None else cores
    cpus = sorted(cores)
    run.mkdir(parents=True)
    (run / "arms").mkdir()
    (run / "logs").mkdir()
    for name in ("RELEASE", "SOURCE_SHA256SUMS"):
        if (root / name).is_file():
            (run / name).write_bytes((root / name).read_bytes())
    arms = {}
    started = 1_800_000_000_000_000_000
    for i, name in enumerate(arm_names(root)):
        if name in omit:
            continue
        cpu = cpus[i % len(cpus)] if cpu_of is None else cpu_of(name)
        spec = specs.get(name)
        if spec is None and base is not None:
            (run / "arms" / name).symlink_to((Path(base) / "arms" / name).resolve(), target_is_directory=True)
            rc = 0
        else:
            rc = write_arm(root, name, run / "arms" / name, cpu, spec)
        (run / "logs" / (name + ".log")).write_bytes(b"")
        arms[name] = dict(arm=name, cpu=cpu, physical_core=list(cores[cpu]), threads=1, rc=rc, killed=False,
                          limit_s=load_driver(root)[1].plan({a.name: a for a in load_driver(root)[0].reg1_arms()}[name])["limit_s"],
                          started_ns=started + i * 10**9, ended_ns=started + i * 10**9 + 2 * 10**9,
                          elapsed_including_wrapper_s=2.0, attempts=1 + retries, log=f"logs/{name}.log")
    execution = dict(label="DEVELOPMENT_ONLY", complete=True, cpus=cpus,
                     physical_cores={str(c): list(cores[c]) for c in cpus}, grace_s=30,
                     queue_order=list(arms), retries=retries, arms=arms)
    with (run / "execution.json").open("x", encoding="ascii") as stream:
        json.dump(execution, stream, indent=2, sort_keys=True)
        stream.write("\n")
    return run
