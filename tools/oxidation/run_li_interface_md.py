#!/usr/bin/env python3
"""run_li_interface_md.py — relax + NVT MD of an interface with UMA (no DFT).

Loads the interface built by build_li_interface.py, re-applies the bottom-layer
freeze (SE atoms within --fix_bottom A of the slab bottom), relaxes the geometry,
then runs Langevin NVT MD and dumps a trajectory for decomposition analysis.
Same fairchem/UMA machinery as tools/modelc_v3/disorder_ensemble_diffusion.py.

  python3 tools/oxidation/run_li_interface_md.py \
    --interface interface_b2o3_Li.xyz --label b2o3 \
    --temperature 600 --equilib_ps 2 --prod_ps 50 --device cuda

2026-11-17 ([혁주] MD-0 · 카드 db/properties/hyeokju_lzo_md_card_2026_11_16.json ⏩_개정_1_2026_11_17_MD0_실행_결과_전)
  --freeze_idx FILE.json   이 인덱스 (JSON 정수 목록) 를 고정한 채 이완 · --schedule 을 돈다 (--fix_bottom 과 같이 쓰면 거부)
  --schedule "hold:T:ps,ramp:T0:T1:ps,…"   고정 구간 온도 일정 (Langevin · dt = --schedule_dt_fs) — ramp 는 10 스텝마다 목표 T 를 선형으로 옮긴다
  --release                일정이 끝나면 고정을 풀고 마지막 NVT (평형 + 생산) 를 돈다
  --seed                   속도 (MaxwellBoltzmann) · Langevin 난수 둘 다 이 시드에서 나온다
                           ⛔ 2026-11-17 전에는 --seed 를 받고 **안 썼다** (속도 · Langevin 둘 다 전역 난수) — 재현이 안 됐다
  생산 궤적 저장은 결정적이다: 프레임 0 = 생산 시작 · 프레임 k = 생산 시각 k × save_fs (info['t_prod_ps']) —
    ASE attach(interval) 의 첫 호출 관례 (판마다 다를 수 있다) 에 기대지 않는다. generate_dft_inputs --from_traj 의
    index = round(t·1000/save_fs) 규칙과 그대로 맞는다.
  <label>_md_log.json: 설정 · 시드 · 난수 경로 · 단계별 평균 T · hold 단계 MSD (--msd_elements · 기록만) · 프레임 시각
  --stream_traj            (2026-11-20 · [혁주] MD-1) 생산 프레임을 저장할 때마다 <label>_traj.xyz.part 에 덧붙이고 flush 한다 ·
                           끝나면 그 파일을 <label>_traj.xyz 로 이름만 바꾼다 (원자적) — 긴 런 (1 ns ≈ 하루) 이 중간에 끊겨도 앞부분이 남는다 ·
                           최종 파일은 스트림 없이 쓴 것과 바이트까지 같다 (selftest) · 끊기면 .part 만 남고 _traj.xyz 는 안 생긴다 (끝난 런과 섞이지 않는다)
  마지막 NVT 를 시작할 때 모든 원자의 속도를 --temperature 로 다시 뽑는다 (풀린 원자는 속도 0 이었다)

⛔ 이 도구가 못 하는 것
  · 녹았는지 판정하지 않는다 — hold MSD 는 기록만 한다 (문턱은 카드가 정하고, MD-0 카드는 문턱을 두지 않았다)
  · NPT 가 없다 — 셀 고정 · 압력은 판정하지 않는다
  · UMA 힘이 맞는지 모른다 — mlip_committee.py md0_check 가 DFT 와 맞댄다
  · Langevin 이 rng 인자를 못 받는 옛 ASE 면 전역 np.random.seed 로 내려간다 (로그에 'rng_path' 로 적는다)

  python3 tools/oxidation/run_li_interface_md.py --selftest    # EMT (Cu) 로 고정 · 일정 · 시드 · 프레임 시각 시험 (UMA 안 부름)
"""
import argparse
import inspect
import json
import os
import sys

import numpy as np
from ase.io import read, write
from ase.constraints import FixAtoms
from ase.optimize import FIRE
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase import units

RAMP_CHUNK = 10   # ramp 목표 T 를 몇 스텝마다 옮기나


def parse_schedule(s):
    """'hold:2500:10,ramp:2500:600:19' → [(kind, T0, T1, ps)] · 못 읽으면 ValueError (조용히 빼지 않는다)."""
    out = []
    if not s:
        return out
    for tok in s.split(","):
        p = [x.strip() for x in tok.strip().split(":")]
        try:
            if p[0] == "hold" and len(p) == 3:
                st = ("hold", float(p[1]), float(p[1]), float(p[2]))
            elif p[0] == "ramp" and len(p) == 4:
                st = ("ramp", float(p[1]), float(p[2]), float(p[3]))
            else:
                raise ValueError
        except ValueError:
            raise ValueError(f"⛔ 일정 조각을 못 읽었다: {tok!r} (hold:T:ps · ramp:T0:T1:ps)")
        if st[3] <= 0 or min(st[1], st[2]) <= 0:
            raise ValueError(f"⛔ 일정 조각의 T · ps 는 양수여야 한다: {tok!r}")
        out.append(st)
    return out


def _accepts(fn, name):
    try:
        return name in inspect.signature(fn).parameters
    except (TypeError, ValueError):
        return False


def _mb(atoms, T, rng):
    if _accepts(MaxwellBoltzmannDistribution, "rng"):
        MaxwellBoltzmannDistribution(atoms, temperature_K=T, rng=rng)
        return "rng"
    np.random.seed(int(rng.integers(0, 2**31 - 1)))
    MaxwellBoltzmannDistribution(atoms, temperature_K=T)
    return "global_seed"


def _langevin(atoms, dt_fs, T, friction, rng):
    kw = {"rng": rng} if _accepts(Langevin.__init__, "rng") else {}
    if not kw:
        np.random.seed(int(rng.integers(0, 2**31 - 1)))
    dyn = Langevin(atoms, dt_fs * units.fs, temperature_K=T, friction=friction / units.fs, **kw)
    return dyn, ("rng" if kw else "global_seed")


def _set_T(dyn, T):
    try:
        dyn.set_temperature(temperature_K=T)
    except TypeError:                                   # 옛 ASE
        dyn.set_temperature(T * units.kB)


def _target_T(dyn):
    """열욕이 실제로 들고 있는 목표 T [K] (ASE Langevin.temp = kT [eV]) — 기록이 아니라 dyn 에서 읽는다."""
    t = getattr(dyn, "temp", None)
    return float(t / units.kB) if t is not None else None


def run_protocol(atoms, calc, *, label, out_dir=".", freeze_idx=None, schedule=(), schedule_dt_fs=1.0,
                 release=False, relax_fmax=0.08, relax_steps=300, temperature=600.0, equilib_ps=2.0,
                 prod_ps=50.0, dt_fs=1.0, friction=0.01, save_fs=200.0, seed=1234, msd_elements=("Zr",),
                 log_extra=None, stream_traj=False):
    """이완 → (고정한 채) 온도 일정 → (풀고) NVT 평형 + 생산. 계산기는 밖에서 준다 (시험은 EMT)."""
    save_int = save_fs / dt_fs
    if abs(save_int - round(save_int)) > 1e-9 or round(save_int) < 1:
        raise ValueError(f"⛔ save_fs ({save_fs}) 가 dt_fs ({dt_fs}) 의 양의 정수배가 아니다 — 프레임 시각이 어긋난다")
    save_int = int(round(save_int))
    n_save = prod_ps * 1000.0 / save_fs
    if abs(n_save - round(n_save)) > 1e-9:
        raise ValueError(f"⛔ prod_ps ({prod_ps}) 가 save_fs ({save_fs}) 의 정수배가 아니다")
    n_save = int(round(n_save))
    os.makedirs(out_dir, exist_ok=True)
    rng = np.random.default_rng(seed)
    sym = np.array(atoms.get_chemical_symbols())
    if freeze_idx:
        fi = sorted(set(int(i) for i in freeze_idx))
        if fi[0] < 0 or fi[-1] >= len(atoms):
            raise ValueError(f"⛔ 고정 인덱스가 원자 범위 밖이다 (0..{len(atoms) - 1})")
        atoms.set_constraint(FixAtoms(indices=fi))
    else:
        fi = []
    atoms.calc = calc
    log = {"label": label, "n_atoms": len(atoms), "formula": atoms.get_chemical_formula(), "seed": seed,
           "freeze_idx_n": len(fi), "release": bool(release), "relax": {"fmax": relax_fmax, "steps": relax_steps},
           "schedule": [list(s) for s in schedule], "schedule_dt_fs": schedule_dt_fs,
           "nvt": {"temperature_K": temperature, "equilib_ps": equilib_ps, "prod_ps": prod_ps, "dt_fs": dt_fs,
                   "friction_per_fs": friction, "save_fs": save_fs},
           "stages": [], "rng_path": {}}
    if log_extra:
        log.update(log_extra)
    if relax_steps > 0:
        FIRE(atoms, logfile=os.path.join(out_dir, f"{label}_relax.log")).run(fmax=relax_fmax, steps=relax_steps)
    write(os.path.join(out_dir, f"{label}_relaxed.xyz"), atoms)

    if schedule:
        log["rng_path"]["schedule_velocities"] = _mb(atoms, schedule[0][1], rng)
        for kind, T0, T1, ps in schedule:
            n = int(round(ps * 1000.0 / schedule_dt_fs))
            print(f"  [{label}] 일정 {kind} {T0:.0f}→{T1:.0f} K · {ps} ps ({n} 스텝) 시작", flush=True)
            dyn, path = _langevin(atoms, schedule_dt_fs, T0, friction, rng)
            log["rng_path"]["schedule_langevin"] = path
            p0 = atoms.get_positions().copy()
            Ts, done = [], 0
            while done < n:
                k = min(RAMP_CHUNK, n - done)
                if kind == "ramp":
                    _set_T(dyn, T0 + (T1 - T0) * (done + k) / n)
                dyn.run(k)
                done += k
                Ts.append(float(atoms.get_temperature()))
            st = {"kind": kind, "T0_K": T0, "T1_K": T1, "ps": ps, "steps": n,
                  "T_inst_mean_K": float(np.mean(Ts)), "T_inst_last_K": Ts[-1],
                  "T_target_last_K": _target_T(dyn)}
            if kind == "hold":
                disp = atoms.get_positions() - p0
                free = np.ones(len(atoms), bool)
                free[fi] = False
                st["msd_A2_record_only"] = {el: float((disp[(sym == el) & free] ** 2).sum(1).mean())
                                            for el in msd_elements if ((sym == el) & free).any()}
                st["msd_n_atoms"] = {el: int(((sym == el) & free).sum()) for el in msd_elements}
            log["stages"].append(st)
            print(f"  [{label}] 일정 {kind} 끝 · 평균 T {st['T_inst_mean_K']:.0f} K · 목표 끝 {st['T_target_last_K']:.0f} K", flush=True)
        write(os.path.join(out_dir, f"{label}_schedule_end.xyz"), atoms)
    if release and fi:
        atoms.set_constraint()
    log["frozen_during_nvt"] = (len(fi) if (fi and not release) else 0)

    log["rng_path"]["nvt_velocities"] = _mb(atoms, temperature, rng)
    dyn, path = _langevin(atoms, dt_fs, temperature, friction, rng)
    log["rng_path"]["nvt_langevin"] = path
    print(f"  [{label}] NVT {temperature:.0f} K 평형 {equilib_ps} ps 시작 (고정 {log['frozen_during_nvt']})", flush=True)
    dyn.run(int(round(equilib_ps * 1000.0 / dt_fs)))

    def snap(k):
        c = atoms.copy()
        c.info["t_prod_ps"] = round(k * save_fs / 1000.0, 6)
        c.info["T_inst_K"] = float(atoms.get_temperature())
        c.info["E_pot_eV"] = float(atoms.get_potential_energy())
        return c

    final = os.path.join(out_dir, f"{label}_traj.xyz")
    part = final + ".part"
    fh = None
    if stream_traj:
        if os.path.exists(part):
            raise ValueError(f"⛔ {part} 가 이미 있다 — 끊긴 런의 흔적이다 (옮겨 보존한 뒤 다시 · 덮지 않는다)")
        fh = open(part, "w")
        log["stream_traj"] = {"part": os.path.basename(part), "규칙": "프레임마다 덧붙이고 flush · 끝나면 이름만 바꾼다"}
    frames = [snap(0)]
    if fh:
        write(fh, frames[0], format="extxyz"); fh.flush()
    per_ps = max(1, int(round(1000.0 / save_fs)))
    for k in range(1, n_save + 1):
        dyn.run(save_int)
        frames.append(snap(k))
        if fh:
            write(fh, frames[-1], format="extxyz"); fh.flush()
        if k % per_ps == 0:
            print(f"  [{label}] 생산 {frames[-1].info['t_prod_ps']:.1f} / {prod_ps} ps · T {frames[-1].info['T_inst_K']:.0f} K", flush=True)
    if fh:
        fh.close()
        os.replace(part, final)
    else:
        write(final, frames, format="extxyz")
    log["frames"] = {"n": len(frames), "t_prod_ps_first": frames[0].info["t_prod_ps"],
                     "t_prod_ps_last": frames[-1].info["t_prod_ps"], "save_fs": save_fs,
                     "규칙": "프레임 k = 생산 시각 k × save_fs (프레임 0 = 생산 시작) — from_traj index = round(t·1000/save_fs)"}
    log["T_prod_mean_K"] = float(np.mean([f.info["T_inst_K"] for f in frames]))
    with open(os.path.join(out_dir, f"{label}_md_log.json"), "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=1)
    return frames, log


def selftest():
    import shutil
    import tempfile
    from ase.build import bulk
    from ase.calculators.emt import EMT
    res = []

    def chk(name, cond):
        res.append(bool(cond)); print(("  ✓ " if cond else "  ✗ ") + name)

    def refused(fn):
        try:
            fn()
        except (ValueError, SystemExit):
            return True
        return False

    root = tempfile.mkdtemp(prefix="rlim_")
    try:
        base = bulk("Cu", "fcc", a=3.6, cubic=True).repeat((2, 2, 2))      # 32 원자
        kw = dict(relax_steps=0, temperature=300.0, equilib_ps=0.02, prod_ps=0.04, dt_fs=2.0, friction=0.02,
                  save_fs=10.0, msd_elements=("Cu",))
        a = base.copy()
        fr, lg = run_protocol(a, EMT(), label="t1", out_dir=root, freeze_idx=[0, 1, 2],
                              schedule=parse_schedule("hold:600:0.02,ramp:600:300:0.02"), schedule_dt_fs=1.0,
                              release=True, seed=7, **kw)
        se = read(os.path.join(root, "t1_schedule_end.xyz"))
        chk("양성: 고정한 원자는 일정 동안 안 움직인다", np.allclose(se.positions[:3], base.positions[:3], atol=1e-9))
        chk("양성: 안 고정한 원자는 움직인다", not np.allclose(se.positions[3:], base.positions[3:], atol=1e-6))
        chk("양성: --release 뒤 고정했던 원자도 움직인다 (생산 마지막 프레임)",
            not np.allclose(fr[-1].positions[:3], base.positions[:3], atol=1e-6))
        chk("양성: 프레임 수 = prod/save + 1 (프레임 0 = 생산 시작)", len(fr) == 5 and lg["frames"]["n"] == 5)
        chk("양성: 프레임 k 의 t_prod_ps = k × save_fs", [f.info["t_prod_ps"] for f in fr] == [0.0, 0.01, 0.02, 0.03, 0.04])
        chk("양성: ramp 끝에 열욕의 실제 목표 T = T1 (300 K) · hold 는 600 K",
            abs(lg["stages"][1]["T_target_last_K"] - 300.0) < 1e-6 and abs(lg["stages"][0]["T_target_last_K"] - 600.0) < 1e-6)
        chk("양성: hold 단계 MSD 를 기록만 한다 — 고정 3 원자를 빼고 29 원자 평균",
            "Cu" in lg["stages"][0]["msd_A2_record_only"] and lg["stages"][0]["msd_n_atoms"]["Cu"] == 29)
        b = base.copy()
        fr2, _ = run_protocol(b, EMT(), label="t2", out_dir=root, freeze_idx=[0, 1, 2],
                              schedule=parse_schedule("hold:600:0.02,ramp:600:300:0.02"), schedule_dt_fs=1.0,
                              release=True, seed=7, **kw)
        chk("양성: 같은 시드 → 같은 궤적 (재현)", np.allclose(fr[-1].positions, fr2[-1].positions, atol=1e-10))
        c = base.copy()
        fr3, _ = run_protocol(c, EMT(), label="t3", out_dir=root, freeze_idx=[0, 1, 2],
                              schedule=parse_schedule("hold:600:0.02,ramp:600:300:0.02"), schedule_dt_fs=1.0,
                              release=True, seed=8, **kw)
        chk("⛔음성: 다른 시드 → 다른 궤적", not np.allclose(fr[-1].positions, fr3[-1].positions, atol=1e-6))
        d = base.copy()
        fr4, lg4 = run_protocol(d, EMT(), label="t4", out_dir=root, freeze_idx=[0, 1, 2],
                                schedule=parse_schedule("hold:600:0.02"), schedule_dt_fs=1.0, release=False,
                                seed=7, **kw)
        chk("양성: --release 없으면 생산 동안에도 고정 그대로", np.allclose(fr4[-1].positions[:3], base.positions[:3], atol=1e-9)
            and lg4["frozen_during_nvt"] == 3)
        chk("⛔음성: 못 읽는 일정 조각 → 거부", refused(lambda: parse_schedule("hold:600")))
        chk("⛔음성: 음수 온도 · 0 ps → 거부", refused(lambda: parse_schedule("ramp:600:-1:2")) and refused(lambda: parse_schedule("hold:600:0")))
        chk("⛔음성: save_fs 가 dt 의 정수배가 아니면 거부",
            refused(lambda: run_protocol(base.copy(), EMT(), label="t5", out_dir=root, relax_steps=0, dt_fs=2.0,
                                         save_fs=5.0, prod_ps=0.04, equilib_ps=0.0)))
        chk("⛔음성: 고정 인덱스가 범위 밖이면 거부",
            refused(lambda: run_protocol(base.copy(), EMT(), label="t6", out_dir=root, freeze_idx=[99], relax_steps=0,
                                         dt_fs=2.0, save_fs=10.0, prod_ps=0.02, equilib_ps=0.0)))
        chk("⛔음성: CLI 에서 --fix_bottom 과 --freeze_idx 를 같이 주면 거부",
            refused(lambda: main(["--interface", "x.xyz", "--label", "x", "--freeze_idx", "f.json", "--fix_bottom", "6"])))
        # ── --stream_traj (2026-11-20) ──
        e = base.copy()
        run_protocol(e, EMT(), label="s1", out_dir=root, freeze_idx=[0, 1, 2],
                     schedule=parse_schedule("hold:600:0.02,ramp:600:300:0.02"), schedule_dt_fs=1.0,
                     release=True, seed=7, stream_traj=True, **kw)
        b1 = open(os.path.join(root, "t1_traj.xyz"), "rb").read()
        b2 = open(os.path.join(root, "s1_traj.xyz"), "rb").read()
        chk("양성: --stream_traj 최종 궤적 = 스트림 없이 쓴 궤적 (같은 시드 · 바이트까지)", b1 == b2 and len(b1) > 0)
        chk("양성: 끝나면 .part 가 남지 않는다 (이름만 바꿈)", not os.path.exists(os.path.join(root, "s1_traj.xyz.part")))

        class Boom(EMT):
            n = 0
            def calculate(self, *args, **kws):
                Boom.n += 1
                if Boom.n > 60:
                    raise RuntimeError("일부러 낸 중단")
                return super().calculate(*args, **kws)

        def crash():
            run_protocol(base.copy(), Boom(), label="s2", out_dir=root, relax_steps=0, temperature=300.0,
                         equilib_ps=0.0, prod_ps=0.2, dt_fs=2.0, friction=0.02, save_fs=10.0, seed=7, stream_traj=True)
        try:
            crash(); crashed = False
        except RuntimeError:
            crashed = True
        part2 = os.path.join(root, "s2_traj.xyz.part")
        nf = len(read(part2, index=":", format="extxyz")) if os.path.exists(part2) else 0
        chk("⛔음성: 생산 도중 끊기면 .part 에 앞부분이 남고 _traj.xyz 는 안 생긴다",
            crashed and nf >= 1 and not os.path.exists(os.path.join(root, "s2_traj.xyz")))
        chk("⛔음성: 끊긴 런의 .part 가 있으면 같은 이름으로 다시 시작하지 않는다 (덮지 않는다)",
            refused(lambda: run_protocol(base.copy(), EMT(), label="s2", out_dir=root, relax_steps=0, temperature=300.0,
                                         equilib_ps=0.0, prod_ps=0.02, dt_fs=2.0, friction=0.02, save_fs=10.0,
                                         seed=7, stream_traj=True)))
    finally:
        shutil.rmtree(root, ignore_errors=True)
    n_bad = len(res) - sum(res)
    print(f"selftest: {sum(res)} 통과 / {n_bad} 실패")
    return 0 if n_bad == 0 else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--interface")
    ap.add_argument("--label")
    ap.add_argument("--out_dir", default=".")
    ap.add_argument("--temperature", type=float, default=600.0)
    ap.add_argument("--equilib_ps", type=float, default=2.0)
    ap.add_argument("--prod_ps", type=float, default=50.0)
    ap.add_argument("--dt_fs", type=float, default=1.0, help="1 fs (reactive interface + Li metal)")
    ap.add_argument("--friction", type=float, default=0.01, help="Langevin friction [1/fs]")
    ap.add_argument("--save_fs", type=float, default=200.0)
    ap.add_argument("--fix_bottom", type=float, default=None,
                    help="freeze SE atoms within this many A of the slab bottom (기본 6.0 — --freeze_idx 를 주면 쓰지 않는다)")
    ap.add_argument("--freeze_idx", help="고정할 원자 인덱스 JSON (정수 목록 또는 {'freeze_idx': [...]})")
    ap.add_argument("--schedule", default="", help="hold:T:ps,ramp:T0:T1:ps,… (고정 구간 온도 일정)")
    ap.add_argument("--schedule_dt_fs", type=float, default=1.0)
    ap.add_argument("--release", action="store_true", help="일정 뒤 고정을 풀고 마지막 NVT")
    ap.add_argument("--msd_elements", nargs="*", default=["Zr"], help="hold 단계 MSD 를 기록할 원소 (기록만)")
    ap.add_argument("--relax_fmax", type=float, default=0.08)
    ap.add_argument("--relax_steps", type=int, default=300)
    ap.add_argument("--seed", type=int, default=1234, help="속도 · Langevin 난수 시드 (재현)")
    ap.add_argument("--uma_model", default="uma-s-1p1")
    ap.add_argument("--uma_task", default="omat")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--stream_traj", action="store_true", help="생산 프레임을 .part 에 덧붙이며 쓴다 (끝나면 _traj.xyz 로 이름 변경)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.interface and a.label):
        ap.error("--interface 와 --label 이 필요하다")
    if a.freeze_idx and a.fix_bottom is not None:
        raise SystemExit("⛔ --fix_bottom 과 --freeze_idx 를 같이 주지 않는다 (무엇이 고정됐는지 갈린다)")
    schedule = parse_schedule(a.schedule)
    atoms = read(a.interface)
    freeze = None
    if a.freeze_idx:
        j = json.load(open(a.freeze_idx, encoding="utf-8"))
        freeze = j["freeze_idx"] if isinstance(j, dict) else j
    else:
        fb = 6.0 if a.fix_bottom is None else a.fix_bottom
        sym = np.array(atoms.get_chemical_symbols())
        z = atoms.positions[:, 2]
        se_mask = sym != "Li"
        zmin_se = z[se_mask].min() if se_mask.any() else 0.0
        freeze = [int(i) for i in np.where(se_mask & (z < zmin_se + fb))[0]]
    if schedule and not freeze:
        print("  ⚠ 일정은 있는데 고정 원자가 없다 — 전부 같은 온도 일정을 겪는다")
    print(f"[{a.label}] atoms={len(atoms)}  frozen={len(freeze)}  schedule={schedule or '—'}  release={a.release}  seed={a.seed}")

    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    calc = FAIRChemCalculator(pretrained_mlip.get_predict_unit(a.uma_model, device=a.device), task_name=a.uma_task)
    frames, log = run_protocol(atoms, calc, label=a.label, out_dir=a.out_dir, freeze_idx=freeze, schedule=schedule,
                               schedule_dt_fs=a.schedule_dt_fs, release=a.release, relax_fmax=a.relax_fmax,
                               relax_steps=a.relax_steps, temperature=a.temperature, equilib_ps=a.equilib_ps,
                               prod_ps=a.prod_ps, dt_fs=a.dt_fs, friction=a.friction, save_fs=a.save_fs,
                               seed=a.seed, msd_elements=tuple(a.msd_elements),
                               log_extra={"interface": a.interface, "uma_model": a.uma_model, "uma_task": a.uma_task},
                               stream_traj=a.stream_traj)
    print(f">> done: {len(frames)} production frames -> {os.path.join(a.out_dir, a.label + '_traj.xyz')}  "
          f"(T_prod mean {log['T_prod_mean_K']:.0f} K · stages {[(s['kind'], round(s['T_inst_mean_K'])) for s in log['stages']]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
