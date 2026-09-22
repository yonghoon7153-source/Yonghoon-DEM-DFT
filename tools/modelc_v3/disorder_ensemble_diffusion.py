#!/usr/bin/env python3
"""disorder_ensemble_diffusion.py — Test whether Cl-/S2- site disorder lowers
the Li migration barrier Ea (the experimental Minafra/Kraft/Zeier narrative),
for comp1 (LPSCl) and modelc (LPSCl1.6).

Motivation
----------
Our earlier single-cell UMA Arrhenius gave modelc (LPSCl1.6) a HIGHER Ea than
comp1 (LPSCl) and attributed the conductivity gain to the prefactor — OPPOSITE
to the experimental "disorder flattens the landscape -> lower Ea" picture. But
both starting cells are nearly ORDERED on the Cl-/S2- (free-anion) sublattice
(comp1 fully ordered; modelc only 1/8 anti-site), so they structurally cannot
show the disorder effect. This script builds an ENSEMBLE of Cl/S anti-site
configurations at controlled disorder levels and measures Ea(disorder).

If Ea drops with disorder -> we reproduce the experiment and our earlier
ordered-cell Ea was the artifact. If Ea stays high even fully disordered ->
the prefactor mechanism is robust. Either outcome resolves the tension.

Disorder model
--------------
Free anions = S NOT bonded to any P (the free S2-) + all Cl. An "anti-site
swap" exchanges the chemical identity of one free-S site and one Cl site at
FIXED positions (lattice unchanged, only S<->Cl labels swap). Composition and
charge are conserved (atom counts unchanged). disorder_frac d = fraction of
free-anion sites that are anti-occupied = 2*n_swaps / n_free_anion_sites.

Pipeline (one UMA load for the whole ensemble)
----------------------------------------------
for each disorder level d:
    for each config replica:
        generate anti-site config
        for each T: Langevin MD (equilib + prod) -> Li MSD -> D(T)
        Arrhenius ln D vs 1/T -> Ea_config, D0_config
    Ea(d) = mean +/- std over replicas

Usage (v100, GPU free after comp1-600K):
    python3 disorder_ensemble_diffusion.py \
        --v0_xyz db/structures/comp1_V0_k444.xyz --label comp1 \
        --out_root /home/ubuntu/work/runs/comp1_v3/disorder_diffusion \
        --disorder_levels 0.0 0.5 --n_configs 3 \
        --temperatures 600 800 1000 --equilib_ps 5 --prod_ps 50 \
        --device cuda
Then the same for modelc (--v0_xyz <modelc V0 xyz> --label modelc ...).

Cost ~ (n_levels with d=0 counts as 1 replica) * n_configs * n_T MD runs.
Default comp1: (1 + 3) configs * 3 T = 12 MD * ~35-45 min = ~7-9 h. Run in bg.
"""
import argparse
import sys
import json
import time
from pathlib import Path
import numpy as np

from ase import units
from ase.io import read, write
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.optimize import FIRE

kB_eV = 8.617333262e-5  # eV/K


# ----------------------------- disorder model -----------------------------
def identify_free_anions(atoms, p_s_cut=2.6):
    """Return (free_S_idx, hal_idx). free S = S with no P neighbor < p_s_cut.
    hal_idx = ALL halides (Cl, Br, I) so mixed-halide argyrodites (e.g. comp2
    Li6PS5Cl0.5Br0.5) disorder BOTH Cl<->S2- and Br<->S2-. Pure-Cl systems
    (comp1/modelc) are unaffected (no Br/I present)."""
    syms = np.array(atoms.get_chemical_symbols())
    P_idx = np.where(syms == "P")[0]
    S_idx = np.where(syms == "S")[0]
    Cl_idx = np.where(np.isin(syms, ["Cl", "Br", "I"]))[0].tolist()
    if len(P_idx) == 0:
        return S_idx.tolist(), Cl_idx
    D = atoms.get_all_distances(mic=True)
    free_S = []
    for s in S_idx:
        if D[s, P_idx].min() >= p_s_cut:
            free_S.append(int(s))
    return free_S, Cl_idx


def make_disordered(atoms, n_swaps, free_S, cl_idx, rng):
    """Swap n_swaps free-S <-> Cl identities at fixed positions. Returns a copy."""
    a = atoms.copy()
    syms = list(a.get_chemical_symbols())
    if n_swaps <= 0:
        return a, []
    s_pick = rng.choice(free_S, size=n_swaps, replace=False)
    c_pick = rng.choice(cl_idx, size=n_swaps, replace=False)
    swaps = []
    for s, c in zip(s_pick, c_pick):
        syms[s], syms[c] = syms[c], syms[s]   # S-site becomes Cl, Cl-site becomes S
        swaps.append((int(s), int(c)))
    a.set_chemical_symbols(syms)
    return a, swaps


# ----------------------------- MSD (cell-correct) -----------------------------
def msd_multi_origin(cart_li, dt_ps, n_lag=150):
    """Multi-time-origin (windowed) MSD:  MSD(tau) = <|r(t0+tau) - r(t0)|^2>_{t0, ions}.

    WHY (2026-08-03, first-author question "is a 2-50 ps fit window right?").
      The MSD above uses a SINGLE time origin (ref = cart[0]).  With only 27 Li in the
      62-atom cells (58 in b2o3), that is 27 samples per lag -- the curve is dominated by
      whichever few ions happened to find a fast channel.  Measured consequence: modelc
      600 K has beta = 0.76 over 2-50 ps but 1.00 over 1-100 ps, and the slope changes
      1.75x.  Averaging over every time origin multiplies the sample count by the number
      of (weakly correlated) origins at no extra MD cost.

    ⚠ Only lags up to n_frames/2 are returned.  At lag ~ n_frames there is a single
      origin left and the estimator is noisier than the single-origin curve, which is
      exactly the failure this is meant to remove.

    ⚠ This does NOT replace msd_Li_A2 / D_Li_cm2_s.  Those stay byte-identical so every
      published number stays reproducible; the MTO curve is stored alongside as
      msd_Li_A2_mto for the window/statistics audit (tools/ionic/msd_refit_window.py --mto).
    """
    nt = cart_li.shape[0]
    if nt < 8:
        return [], [], []
    lag_max = max(2, nt // 2)
    lags = np.unique(np.linspace(1, lag_max, min(n_lag, lag_max)).astype(int))
    tau, msd, norig = [], [], []
    for L in lags:
        d = cart_li[L:] - cart_li[:-L]               # (nt-L, n_Li, 3)
        msd.append(float((d ** 2).sum(-1).mean()))
        tau.append(float(L * dt_ps))
        norig.append(int(nt - L))
    return tau, msd, norig


#: He/Zhu/Epstein/Mo, npj Comput. Mater. 4, 18 (2018) 식 (8)·(9) 의 `a`.
#: `msd_diffusive_check.D_HOP_A` 와 **같은 값·같은 뜻**이다 (이웃 Li 자리 간격).
#: ⛔ 여기 박아 두는 이유: `msd.json` 만 보고 N_eff 를 다시 낼 수 있어야 하는데,
#:   `a` 가 기록에 없으면 다음 사람이 **딴 값을 가정**한다.
HE2018_SITE_DISTANCE_A = 3.0


def he2018_neff(n_li, msd_max_a2, a=HE2018_SITE_DISTANCE_A):
    """He 2018 식 (8) 의 유효 점프 수 `N_eff = n_Li · max(MSD) / a²`.

    ⛔⛔ **`max(MSD)` 는 궤적 전체의 최대값이다 — 적합 창끝 값이 아니다.**
    2026-09-22 회신 BT 에서 내가 정확히 그 둘을 헷갈렸다: C1·C2 게이트의 문턱
    (창끝 50 ps 의 3 / 48.88 Å²)을 궤적 전체(400 ps) 공식에 넣어 **N_eff 를 8 배
    과소평가**했고, 거기서 "셀이 정밀도 천장 25 % 를 정한다" 는 틀린 결론을 냈다.
    그래서 `msd.json` 은 **두 값을 다른 이름으로 따로** 적는다.

    ⛔ 이 함수가 **못 하는 것**: He 식은 **lag 창을 제한한 적합**에 대해 검증된 적이
    없다. 궤적이 길어지면 정밀도가 좋아지는데 식에는 그게 안 들어간다(회신 BT §6-e).
    런 내부 오차의 정본은 **시간원점 블록 부트스트랩**이고 이 값은 **귀무모형**이다.
    """
    if not n_li or msd_max_a2 is None or msd_max_a2 <= 0:
        return None
    return float(n_li) * float(msd_max_a2) / float(a) ** 2


def li_diffusion_from_frames(frames, save_fs, fit_window_ps):
    """Cell-correct unwrap in fractional coords; MSD(Li); D from MSD=6Dt fit.

    Returns (D, t_ps, msd, extra) where extra carries the multi-time-origin curve.
    """
    syms = np.array(frames[0].get_chemical_symbols())
    li = syms == "Li"
    cell = frames[0].cell.array  # NVT -> fixed cell
    # fractional positions, wrapped
    spos = np.array([f.get_scaled_positions(wrap=True) for f in frames])  # (T,N,3)
    dspos = np.diff(spos, axis=0)
    dspos -= np.round(dspos)                       # minimum image in fractional
    spos_uw = np.concatenate([spos[:1], spos[:1] + np.cumsum(dspos, axis=0)],
                             axis=0)
    cart = spos_uw @ cell                          # (T,N,3) Cartesian, unwrapped
    ref = cart[0, li]
    disp2 = ((cart[:, li] - ref) ** 2).sum(axis=-1)  # (T, n_Li)
    msd = disp2.mean(axis=-1)                        # (T,)
    t_ps = np.arange(len(frames)) * save_fs / 1000.0

    # --- multi-time-origin companion curve (free: no extra MD, no extra disk) ------
    tau, msd_mto, norig = msd_multi_origin(cart[:, li], save_fs / 1000.0)
    lo, hi = fit_window_ps
    n_li = int(li.sum())
    # ⛔ **두 MSD 를 다른 이름으로 적는다** (회신 BT — 내가 이 둘을 헷갈려 N_eff 를
    #   8 배 과소평가했다). 이름이 같으면 다음 사람도 똑같이 헷갈린다.
    #   · msd_max_A2            = **궤적 전체** 최대 → He 2018 N_eff 용
    #   · msd_at_fit_window_end_A2 = **적합 창끝** 값 → C1·C2 게이트용
    extra = {"times_ps_mto": tau, "msd_Li_A2_mto": msd_mto, "n_origins_mto": norig,
             "n_Li": n_li,
             "msd_max_A2": float(np.max(msd)) if len(msd) else None,
             "site_distance_A": HE2018_SITE_DISTANCE_A,
             "site_distance_source":
                 "msd_diffusive_check.D_HOP_A 와 같은 규약 (이웃 Li 자리 간격)",
             "n_eff_he2018": he2018_neff(n_li, float(np.max(msd)) if len(msd) else None),
             "n_eff_note":
                 "He 2018 식 (8). **궤적 전체 max(MSD)** 로 냈다 — 창끝 값이 아니다. "
                 "⛔ He 식은 lag 창을 제한한 적합에 대해 **검증되지 않았다**(회신 BT §6-e); "
                 "런 내부 오차의 정본은 시간원점 블록 부트스트랩이고 이 값은 귀무모형이다."}
    if tau:
        mm = [(a, b) for a, b in zip(tau, msd_mto) if lo <= a <= hi]
        if len(mm) >= 3:
            s = np.polyfit([p[0] for p in mm], [p[1] for p in mm], 1)[0]
            extra["D_Li_cm2_s_mto"] = float(s / 6.0 * 1e-4)

    m = (t_ps >= lo) & (t_ps <= hi)
    if m.sum() < 3:
        # ⛔ **'못 구함' 과 '없음' 을 가른다** — 키를 빼면 다음 사람이 0 으로 읽는다.
        extra["msd_at_fit_window_end_A2"] = None
        extra["msd_at_fit_window_end_why"] = (
            f"적합 창 [{lo}, {hi}] ps 안에 점이 {int(m.sum())} 개뿐이라 안 구했다 "
            "(구했는데 0 인 것이 아니다)")
        return None, t_ps.tolist(), msd.tolist(), extra
    extra["msd_at_fit_window_end_A2"] = float(msd[m][-1])   # C1·C2 게이트가 보는 값
    slope = np.polyfit(t_ps[m], msd[m], 1)[0]        # Å²/ps
    D = slope / 6.0 * 1e-4                            # Å²/ps -> cm²/s
    return float(D), t_ps.tolist(), msd.tolist(), extra


def anneal_relax_config(atoms, calc, anneal_T, anneal_ps, dt_fs, friction, fmax, seed):
    """Prepare a disordered (label-swapped) config for MD: ANNEAL the Li sublattice at
    anneal_T so Li redistributes around the new anion arrangement, keep the lowest-E
    snapshot, then RELAX (FIRE) to a real local minimum. Without this, a Br/Cl label
    forced onto a small S2- site stays metastable -> unphysical over-diffusion in MD
    (sigma_300K blew up to ~70 mS/cm, 2026-07-27). Returns (relaxed_atoms, E0, E_relaxed).
    Anions are heavy -> stay put; only Li hops + local anion settling occur."""
    a = atoms.copy(); a.calc = calc
    E0 = float(a.get_potential_energy())
    MaxwellBoltzmannDistribution(a, temperature_K=anneal_T, rng=np.random.default_rng(seed))
    md = Langevin(a, dt_fs * units.fs, temperature_K=anneal_T, friction=friction,
                  rng=np.random.default_rng(seed + 7919), logfile=None)   # ★ P1-3
    best = {"E": E0, "at": a.copy()}

    def _track(a=a, best=best):
        e = float(a.get_potential_energy())
        if e < best["E"]:
            best["E"] = e; best["at"] = a.copy()
    md.attach(_track, interval=max(1, int(50.0 / dt_fs)))   # sample ~every 50 fs
    md.run(int(anneal_ps * 1000 / dt_fs))
    r = best["at"]; r.calc = calc
    FIRE(r, logfile=None).run(fmax=fmax, steps=400)
    return r, E0, float(r.get_potential_energy())


def run_md(atoms, calc, T, equilib_ps, prod_ps, dt_fs, friction, save_fs,
           out_dir, fit_window_ps, seed, save_traj=False):
    out_dir.mkdir(parents=True, exist_ok=True)
    # resume-safe: 완료된 (config,T)는 msd.json 있으면 재계산 없이 그대로 사용
    mj = out_dir / "msd.json"
    if mj.exists():
        try:
            d = json.loads(mj.read_text())
            if d.get("D_Li_cm2_s") is not None:
                print(f"    [resume] {out_dir.name} msd.json 있음 -> skip "
                      f"(D={d['D_Li_cm2_s']:.3e})")
                return float(d["D_Li_cm2_s"])
        except Exception:
            pass
    atoms = atoms.copy()
    atoms.calc = calc
    rng_seed = seed
    # ⛔⛔ 2026-08-11 자체검토 P1-3 — 옛 코드는 아래 Langevin 에 rng 를 안 넘겼다.
    #   ASE 는 rng=None 이면 **전역 np.random** 을 쓰는데 이 드라이버는 전역을 seed 하지
    #   않는다(default_rng 는 전역을 안 건드린다). 즉 --seed 가 초기속도·disorder 만
    #   고정하고 **thermostat 잡음은 매 실행 달랐다** → 궤적이 재현되지 않았다.
    #   ⚠ 파급: kb/open_items.md 의 "comp1 s2 **같은 시드**, 200 → 1600 ps" 비교는
    #     통제된 비교가 아니었다. 같은 시드라도 앞 50 ps 가 같을 수 없으므로
    #     β 0.64 → 0.37 을 "시간을 늘리면 나빠진다" 의 근거로 쓸 수 없다 — 재검토 대상.
    MaxwellBoltzmannDistribution(atoms, temperature_K=T, rng=np.random.default_rng(rng_seed))
    dt = dt_fs * units.fs
    md = Langevin(atoms, dt, temperature_K=T, friction=friction,
                  rng=np.random.default_rng(rng_seed),   # ★ P1-3 — 없으면 전역 RNG
                  logfile=str(out_dir / "md.log"))
    md.run(int(equilib_ps * 1000 / dt_fs))
    save_int = max(1, int(save_fs / dt_fs))
    frames = []
    # ⭐⭐ 2026-08-27 — **궤적을 진행 중에 쓴다** (Codex 회신 G 권고 ①).
    #   옛 판은 frames 를 메모리에만 쌓고 `write(traj.xyz)` 를 **끝에 한 번** 했다. 두 가지가 깨졌다:
    #     (a) 진행 중 누적 prefix(100/200/400 ps) 분석이 **원리적으로 불가능**했다 —
    #         디스크에 아무것도 없으니 D_inc plateau 를 보고 조기 종료할 수가 없다.
    #         800 ps 런에서 이건 곧 "20시간 넘게 더 돌지 말지" 를 못 정한다는 뜻이다.
    #     (b) 45시간짜리가 죽으면 **궤적과 MSD 가 통째로** 날아간다. md.log 는 ASE
    #         MDLogger 라 위치가 없어 아무것도 복구 못 한다.
    #   → 스냅샷마다 append 한다. 메모리 목록은 그대로 유지해 MSD 계산 경로를 안 바꾼다
    #     (기존 D 값이 그대로 재현돼야 한다 — 아래 ⚠ 규약).
    if save_traj:
        _trj = out_dir / "traj.xyz"
        _trj.unlink(missing_ok=True)          # resume 시 옛 프레임에 이어붙지 않게

        def _snap():
            a = atoms.copy()
            frames.append(a)
            # ⚠ append=True 는 프레임마다 열고 닫는다. save_fs 100 fs 면 8050 프레임 =
            #   45시간에 걸쳐 20초당 한 번이라 비용이 무시할 만하다.
            write(str(_trj), a, append=True)
        md.attach(_snap, interval=save_int)
    else:
        md.attach(lambda: frames.append(atoms.copy()), interval=save_int)
    md.run(int(prod_ps * 1000 / dt_fs))
    D, t_ps, msd, extra = li_diffusion_from_frames(frames, save_fs, fit_window_ps)
    # ⚠ D_Li_cm2_s / times_ps / msd_Li_A2 의 정의는 **바꾸지 않는다** — 이미 나간 값들이
    #   그대로 재현돼야 한다. 다중 시간원점 곡선은 옆에 덧붙이기만 한다(창 감사용).
    # ⚠ 2026-08-11 — traj 를 **msd.json 보다 먼저** 쓴다. 옛 순서에서는 그 사이에 죽으면
    #   resume 이 msd.json 을 보고 건너뛰어 **traj 가 영영 안 생겼다** — --save_traj 를
    #   넣은 목적(소급 MTO·홉 통계 복구)이 정확히 그 상황에서 깨진다.
    if save_traj:
        # 궤적은 위에서 **이미 증분으로 다 썼다** — 여기서 다시 쓰지 않는다.
        # ⚠ 옛 판의 `write(traj.xyz, frames)` 를 남겨두면 같은 파일을 통째로 덮어써서
        #   증분 기록의 의미가 사라진다(그리고 8050 프레임을 한 번 더 직렬화한다).
        # sidecar meta 는 그대로 — downstream 도구가 save_fs 를 자동으로 읽는다.
        (out_dir / "aimd_results.json").write_text(json.dumps(
            {"T_K": T, "save_fs": save_fs, "n_frames": len(frames),
             "prod_ps": prod_ps, "dt_fs": dt_fs}, indent=2))
    (out_dir / "msd.json").write_text(json.dumps(
        {"T_K": T, "D_Li_cm2_s": D, "times_ps": t_ps, "msd_Li_A2": msd,
         "fit_window_ps": list(fit_window_ps), **extra}, indent=2))
    return D


def arrhenius(Ts, Ds):
    Ts, Ds = np.asarray(Ts, float), np.asarray(Ds, float)
    m = Ds > 0
    if m.sum() < 2:
        return None
    slope, intc = np.polyfit(1.0 / Ts[m], np.log(Ds[m]), 1)
    Ea = -slope * kB_eV
    D0 = float(np.exp(intc))
    D300 = D0 * np.exp(-Ea / (kB_eV * 300.0))
    return {"Ea_eV": float(Ea), "D0_cm2_s": D0,
            "D_300K_cm2_s": float(D300),
            "points": [{"T_K": float(t), "D_cm2_s": float(d)}
                       for t, d in zip(Ts[m], Ds[m])]}


def selftest():
    """He 2018 N_eff 기록 경로 — **음성 경로가 본체다** (2026-09-22 신설).

    왜 필요한가: 회신 BT 에서 내가 **적합 창끝 MSD 를 궤적 전체 공식에 넣어** N_eff 를
    8 배 과소평가했다. 코드는 그 계산을 안 했지만(그래서 실행에는 영향이 없었다),
    **`msd.json` 이 두 값을 구분해 적지 않으면 다음 사람이 같은 실수를 한다.**
    그래서 이 시험의 핵심은 *"두 값이 다른 이름으로, 실제로 다르게 적히는가"* 다.

    ⛔ 이 시험이 **못 하는 것**: He 식이 이 계에서 **맞는지**는 안 본다 (유리는 He 의
    적합 대상이 아니다 — 회신 BT §6-d). 기록이 맞는지만 본다.
    """
    import numpy as _np
    from ase import Atoms as _Atoms
    ok = [0, 0]

    def chk(name, cond):
        print(("  ⭕ " if cond else "  ⛔ ") + name)
        ok[0 if cond else 1] += 1

    # ── he2018_neff — 양성 + 음성 ────────────────────────────────────────
    chk("양성: N_eff = n_Li·max(MSD)/a²  (48 · 24 / 9 = 128)",
        abs(he2018_neff(48, 24.0) - 128.0) < 1e-9)
    chk("양성: a 를 바꾸면 제곱으로 들어간다 (a=6 이면 1/4)",
        abs(he2018_neff(48, 24.0, a=6.0) - 32.0) < 1e-9)
    chk("⛔음성: max(MSD) 가 None 이면 **None** 이다 (0 이 아니다 — 0 이면 RSD 가 발산한다)",
        he2018_neff(48, None) is None)
    chk("⛔음성: max(MSD) 가 0 이어도 None (자리 이탈 0 은 '쟀는데 0' 이 아니라 '못 잰 것')",
        he2018_neff(48, 0.0) is None)
    chk("⛔음성: n_Li 가 0 이면 None (Li 없는 계를 조용히 통과시키지 않는다)",
        he2018_neff(0, 24.0) is None)

    # ── 기록 경로 — **두 MSD 가 다르게 적히는가** ─────────────────────────
    #   합성 궤적: Li 1개가 x 로 등속 이동 ⇒ MSD = (v t)², 창끝과 전체가 **다르다**
    cell = _np.eye(3) * 100.0                  # 감김 없게 큰 셀
    nt, v, dt = 101, 0.5, 1.0                  # 100 ps · 0.5 Å/ps · save 1000 fs
    frames = [_Atoms("Li", positions=[[v * i * dt, 0, 0]], cell=cell, pbc=True)
              for i in range(nt)]
    D, t_ps, msd, ex = li_diffusion_from_frames(frames, save_fs=1000.0,
                                                fit_window_ps=(2.0, 50.0))
    chk("양성: 궤적 전체 max(MSD) 를 적는다 ((0.5·100)² = 2500)",
        ex["msd_max_A2"] is not None and abs(ex["msd_max_A2"] - 2500.0) < 1e-6)
    chk("양성: 적합 창끝 MSD 를 **따로** 적는다 ((0.5·50)² = 625)",
        abs(ex["msd_at_fit_window_end_A2"] - 625.0) < 1e-6)
    chk("⛔음성(핵심): **두 값이 실제로 다르다** — 같으면 구분이 무의미하다 (4 배)",
        abs(ex["msd_max_A2"] / ex["msd_at_fit_window_end_A2"] - 4.0) < 1e-6)
    chk("⛔음성: N_eff 는 **궤적 전체** 값으로 낸다 (창끝으로 내면 1/4 이 된다)",
        abs(ex["n_eff_he2018"] - he2018_neff(1, 2500.0)) < 1e-6)
    chk("양성: a 를 기록에 박는다 (없으면 다음 사람이 딴 값을 가정한다)",
        ex["site_distance_A"] == HE2018_SITE_DISTANCE_A and ex.get("site_distance_source"))
    chk("양성: He 식의 **미검증 범위**를 기록에 같이 적는다",
        "검증되지 않았다" in ex.get("n_eff_note", ""))

    # ── 창에 점이 모자랄 때 — '못 구함' 과 '없음' 을 가른다 ────────────────
    D2, _, _, ex2 = li_diffusion_from_frames(frames[:9], save_fs=1000.0,
                                             fit_window_ps=(100.0, 200.0))
    chk("⛔음성: 창 밖이면 D 는 None",
        D2 is None)
    chk("⛔음성: 창끝 MSD 를 **None 으로 명시**한다 (키를 빼면 0 으로 읽힌다)",
        "msd_at_fit_window_end_A2" in ex2 and ex2["msd_at_fit_window_end_A2"] is None)
    chk("⛔음성: **왜 못 구했는지**를 같이 적는다 ('구했는데 0' 과 구분)",
        "안 구했다" in ex2.get("msd_at_fit_window_end_why", ""))
    chk("⛔음성: 그래도 **N_eff 는 살아 있다** — 창과 무관한 양이다",
        ex2.get("msd_max_A2") is not None and ex2.get("n_eff_he2018") is not None)

    print(f"\n  selftest {ok[0]}/{ok[0]+ok[1]} 통과")
    return 1 if ok[1] else 0


def main():
    ap = argparse.ArgumentParser()
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    ap.add_argument("--v0_xyz", required=True)
    ap.add_argument("--supercell", type=int, nargs=3, default=None, metavar=("NA", "NB", "NC"),
                    help="V0 를 이 배수로 타일링한 뒤 MD 를 돈다 (예: 2 2 2). "
                         "⚠ comp1 판정(2026-08-06)의 **남은 수**가 이것이다 — 62원자 셀에 "
                         "Li 24개라 200 ps 는커녕 1600 ps 로도 600 K 가 β 0.37 로 케이지였다. "
                         "시간이 아니라 **이온 수**를 늘려 MSD 앙상블 평균의 통계를 채운다. "
                         "⚠ 비용은 원자 수에 대략 선형 — 2×2×2 는 8배다.")
    ap.add_argument("--label", required=True, help="comp1 or modelc")
    ap.add_argument("--out_root", required=True)
    ap.add_argument("--disorder_levels", type=float, nargs="+",
                    default=[0.0, 0.5],
                    help="anti-site fractions to test (0.0 = ordered baseline)")
    ap.add_argument("--n_configs", type=int, default=3,
                    help="replicas per disorder level (d=0 forced to 1)")
    ap.add_argument("--relax_configs", action="store_true",
                    help="anneal Li + relax each swapped config to a real minimum before "
                         "MD (prevents metastable label-swap over-diffusion). STRONGLY "
                         "recommended for mixed-halide (Br on S2- site).")
    ap.add_argument("--anneal_T", type=float, default=700.0,
                    help="Li-anneal temperature (K) for --relax_configs")
    ap.add_argument("--anneal_ps", type=float, default=20.0,
                    help="Li-anneal duration (ps) for --relax_configs")
    ap.add_argument("--relax_fmax", type=float, default=0.03,
                    help="FIRE force threshold (eV/A) for post-anneal relax")
    ap.add_argument("--temperatures", type=float, nargs="+",
                    default=[600, 800, 1000])
    ap.add_argument("--equilib_ps", type=float, default=5.0)
    ap.add_argument("--prod_ps", type=float, default=50.0)
    ap.add_argument("--timestep_fs", type=float, default=2.0)
    ap.add_argument("--friction", type=float, default=0.02)
    ap.add_argument("--save_fs", type=float, default=100.0)
    # ⛔ 2026-09-08 — 기본값이 [5.0, 40.0] 이었다. CLAUDE.md 정본은 **2–50 ps** 다.
    #   러너가 `--fit_window_ps` 를 안 적으면 이 기본값이 그대로 논문 숫자가 된다
    #   (run_b2o3_md.sh 가 실제로 안 적고 있었다 → 그 D 는 5–40 창 값이었다).
    #   convention_check.py ⑥ 가 이제 이 줄을 본다 — 되돌리면 검사에서 걸린다.
    ap.add_argument("--fit_window_ps", type=float, nargs=2, default=[2.0, 50.0],
                    metavar=("LO_PS", "HI_PS"),
                    help="MSD 자유절편 적합창 [ps] — 정본 2 50 (CLAUDE.md 데이터 규율)")
    ap.add_argument("--save_traj", action="store_true",
                    help="dump production frames to traj.xyz + aimd_results.json "
                         "(enables jump stats / Li-density cube / van Hove)")
    ap.add_argument("--p_s_cut", type=float, default=2.6)
    ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--uma_model", default="uma-s-1p1")
    ap.add_argument("--uma_task", default="omat")
    ap.add_argument("--turbo", action="store_true",
                    help="fairchem inference_settings='turbo' (MD 전용 · 실측 ≈1.9배). 없으면 기본 모드로 "
                         "내려가고 실제 모드를 결과 json 에 적는다. ⛔ 한 캠페인 안에서 섞지 말 것 — "
                         "등가성 근거는 db/properties/uma_turbo_equivalence_2026_09_11.json")
    ap.add_argument("--device", default="cuda")
    args = ap.parse_args()

    out_root = Path(args.out_root)
    out_root.mkdir(parents=True, exist_ok=True)
    base = read(args.v0_xyz)
    # ★ 2026-08-11 — 셀 확대. open_items #1 이 "시간으로는 못 닫는다 → 남은 수는 셀 확대"
    #   로 닫혔고 그 실행 손잡이다. **타일링은 물리를 안 바꾼다** (같은 결정, 같은 밀도) —
    #   바뀌는 건 MSD 를 평균낼 Li 개수뿐이다. 그래서 β 가 올라가면 그건 통계가 채워진
    #   것이지 다른 계를 잰 게 아니다. 그 논증이 성립하려면 밀도가 같아야 하므로 검산한다.
    sc = tuple(args.supercell) if args.supercell else (1, 1, 1)
    if sc != (1, 1, 1):
        n0 = len(base)
        nli0 = sum(1 for s in base.get_chemical_symbols() if s == "Li")
        rho0 = nli0 / base.get_volume()
        base = base.repeat(sc)
        nli = sum(1 for s in base.get_chemical_symbols() if s == "Li")
        rho = nli / base.get_volume()
        # 타일링이 밀도를 바꿨다면 xyz 에 격자가 없거나 pbc 가 꺼진 것이다 — 즉사시킨다
        if abs(rho - rho0) / rho0 > 1e-9:
            raise SystemExit(f"⛔ 타일링이 Li 밀도를 바꿨다 ({rho0:.6e} → {rho:.6e} Å⁻³) — "
                             f"{args.v0_xyz} 에 격자가 없거나 pbc 가 꺼져 있다. 중단.")
        print(f"[{args.label}] 셀 확대 {sc[0]}×{sc[1]}×{sc[2]}: "
              f"{n0} → {len(base)} 원자 · Li {nli0} → {nli} · "
              f"n_Li {rho * 1e24:.4e} cm⁻³ (불변 ✓)")
    free_S, cl_idx = identify_free_anions(base, args.p_s_cut)
    n_sites = len(free_S) + len(cl_idx)
    max_swaps = min(len(free_S), len(cl_idx))
    print(f"[{args.label}] {len(base)} atoms | free-S={len(free_S)} Cl={len(cl_idx)} "
          f"| free-anion sites={n_sites} | max_swaps={max_swaps}", flush=True)

    # ⭐ 2026-08-26 — **시작 즉시** run_meta.json 을 쓴다.
    #   왜: 위 print 는 `| tee` 를 물리면 stdout 이 블록 버퍼가 되어 몇 분~몇십 분 뒤에야 나온다.
    #   그 사이 `--supercell` 이 먹었는지 확인할 방법이 없어서, 62원자를 20시간 돌리는
    #   사고를 화면상 정상인 채로 겪을 수 있다 (2026-08-26 gabia 실측).
    #   ensemble_results.json 은 **끝나야** 나오므로 감시에 못 쓴다.
    try:
        out_root_p = Path(args.out_root); out_root_p.mkdir(parents=True, exist_ok=True)
        (out_root_p / "run_meta.json").write_text(json.dumps({
            "label": args.label, "n_atoms": len(base), "supercell": list(sc),
            "v0_xyz": str(args.v0_xyz), "temperatures": list(args.temperatures),
            "prod_ps": args.prod_ps, "equilib_ps": args.equilib_ps,
            "seed": args.seed, "fit_window_ps": list(args.fit_window_ps),
            "save_traj": bool(args.save_traj), "uma_model": args.uma_model,
            "uma_inference_mode_requested": ("turbo" if getattr(args, "turbo", False) else "default"),
            "note": "MD 시작 직후 기록 — 감시용. 결과는 ensemble_results.json 을 볼 것",
        }, ensure_ascii=False, indent=2))
    except Exception as e:                       # 감시용 파일 때문에 계산이 죽으면 안 된다
        print(f"  ⚠ run_meta.json 을 못 썼다 ({type(e).__name__}: {e}) — 계산은 계속한다")

    # one UMA load for the whole ensemble
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    # ⚠ 2026-09-11 — `--turbo` 는 fairchem 의 MD 전용 실행모드다(미리 컴파일 · 실측 ≈1.9배).
    #   **같은 가중치·같은 task** 이고 바뀌는 것은 실행경로뿐이지만, 컴파일러가 연산 순서를
    #   바꿔 힘이 끝자리에서 달라진다. 등가성 실측은 db/properties/uma_turbo_equivalence_2026_09_11.json:
    #   700 K 스냅샷에서 max|ΔF| 1.99e-3 eV/Å (0.194 %) = 모델 자신의 오차(0.4417)의 0.45 %.
    #   ⛔ **한 캠페인의 모든 런이 같은 모드여야 한다** — 섞으면 그 묶음을 한 표에 못 쓴다.
    #     그래서 실제 모드를 ensemble_results.json 의 uma_inference_mode 에 기록한다.
    _mode = "default"
    if getattr(args, "turbo", False):
        try:
            predictor = pretrained_mlip.get_predict_unit(args.uma_model, device=args.device,
                                                         inference_settings="turbo")
            _mode = "turbo"
        except Exception as e:
            print(f"⚠ turbo 불가 ({type(e).__name__}: {e}) — 기본 모드로 돈다", flush=True)
            predictor = pretrained_mlip.get_predict_unit(args.uma_model, device=args.device)
    else:
        predictor = pretrained_mlip.get_predict_unit(args.uma_model, device=args.device)
    print(f"UMA inference mode: {_mode}", flush=True)
    # ⛔ run_meta.json 은 UMA 로드 **전**에 쓰이므로 요청값만 담긴다 — turbo 가 못 걸렸을 때
    #   감시 파일이 거짓말한다. 실제 모드를 확정한 지금 같은 파일을 갱신한다.
    try:
        _rm = Path(args.out_root) / "run_meta.json"
        _d = json.loads(_rm.read_text(encoding="utf-8")); _d["uma_inference_mode"] = _mode
        _rm.write_text(json.dumps(_d, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"  ⚠ run_meta.json 갱신 실패 ({type(e).__name__}: {e}) — 계산은 계속한다", flush=True)
    calc = FAIRChemCalculator(predictor, task_name=args.uma_task)

    rng = np.random.default_rng(args.seed)
    t_start = time.time()
    levels_out = []
    for d in args.disorder_levels:
        n_swaps = int(round(d * n_sites / 2.0))
        n_swaps = min(n_swaps, max_swaps)
        d_actual = 2.0 * n_swaps / n_sites if n_sites else 0.0
        nconf = 1 if n_swaps == 0 else args.n_configs
        print(f"\n##### disorder d={d} -> n_swaps={n_swaps} (actual d={d_actual:.3f}), "
              f"{nconf} config(s) #####")
        config_results = []
        for ci in range(nconf):
            atoms_d, swaps = make_disordered(base, n_swaps, free_S, cl_idx, rng)
            cdir = out_root / f"d{d_actual:.2f}_cfg{ci}"
            cdir.mkdir(parents=True, exist_ok=True)
            # anneal Li + relax the swapped config to a real minimum before MD
            # (skip for d=0 ordered baseline; resume-safe via config_relaxed.xyz)
            if args.relax_configs and swaps:
                rx = cdir / "config_relaxed.xyz"
                if rx.exists():
                    atoms_d = read(str(rx))
                    print(f"    [resume] {cdir.name} config_relaxed.xyz 있음 -> skip anneal")
                else:
                    atoms_d, E0, E1 = anneal_relax_config(
                        atoms_d, calc, args.anneal_T, args.anneal_ps,
                        args.timestep_fs, args.friction, args.relax_fmax,
                        seed=args.seed + 500 + ci)
                    print(f"    cfg{ci} anneal({args.anneal_T}K,{args.anneal_ps}ps)+relax: "
                          f"E {E0:.3f} -> {E1:.3f} eV (dropped {E0 - E1:.3f})")
                    write(str(rx), atoms_d)
            write(str(cdir / "config.xyz"), atoms_d)
            Ds = []
            for T in args.temperatures:
                t0 = time.time()
                D = run_md(atoms_d, calc, T, args.equilib_ps, args.prod_ps,
                           args.timestep_fs, args.friction, args.save_fs,
                           cdir / f"T{int(T)}", tuple(args.fit_window_ps),
                           seed=args.seed + 1000 * ci + int(T),
                           save_traj=args.save_traj)
                Ds.append(D)
                print(f"    d={d_actual:.2f} cfg{ci} T={int(T)}: "
                      f"D_Li={D:.3e} cm²/s  ({(time.time()-t0)/60:.1f} min)")
            arr = arrhenius(args.temperatures, Ds)
            config_results.append({"config": ci, "swaps": swaps,
                                   "D_per_T": Ds, "arrhenius": arr})
            if arr:
                print(f"    -> cfg{ci} Ea={arr['Ea_eV']:.4f} eV  D0={arr['D0_cm2_s']:.3e}")
            # incremental save (crash-safe)
            (out_root / "ensemble_results.json").write_text(json.dumps({
                "label": args.label, "v0_xyz": args.v0_xyz,
                "supercell": list(sc), "n_atoms": len(base),
                "n_Li": sum(1 for s in base.get_chemical_symbols() if s == "Li"),
                "free_anion_sites": n_sites, "temperatures": args.temperatures,
                "equilib_ps": args.equilib_ps, "prod_ps": args.prod_ps,
                "fit_window_ps": args.fit_window_ps,
                "levels": levels_out + [{
                    "disorder_target": d, "disorder_actual": d_actual,
                    "n_swaps": n_swaps, "configs": config_results}],
            }, indent=2, default=str))
        # aggregate Ea over configs at this level
        Eas = [c["arrhenius"]["Ea_eV"] for c in config_results if c["arrhenius"]]
        D0s = [c["arrhenius"]["D0_cm2_s"] for c in config_results if c["arrhenius"]]
        agg = {"disorder_target": d, "disorder_actual": d_actual,
               "n_swaps": n_swaps, "n_configs": len(config_results),
               "Ea_mean_eV": float(np.mean(Eas)) if Eas else None,
               "Ea_std_eV": float(np.std(Eas)) if Eas else None,
               "D0_mean_cm2_s": float(np.mean(D0s)) if D0s else None,
               "configs": config_results}
        levels_out.append(agg)
        if Eas:
            print(f"### d={d_actual:.2f}: Ea = {np.mean(Eas):.4f} ± "
                  f"{np.std(Eas):.4f} eV  (n={len(Eas)})")

    summary = {
        "label": args.label, "v0_xyz": args.v0_xyz,
        "supercell": list(sc), "n_atoms": len(base),
        "n_Li": sum(1 for s in base.get_chemical_symbols() if s == "Li"),
        "free_anion_sites": n_sites, "temperatures": args.temperatures,
        "equilib_ps": args.equilib_ps, "prod_ps": args.prod_ps,
        "fit_window_ps": args.fit_window_ps,
        "uma_model": args.uma_model, "uma_task": args.uma_task, "uma_inference_mode": _mode,
        "runtime_min": (time.time() - t_start) / 60,
        "levels": levels_out,
        "headline": [{"d": L["disorder_actual"], "Ea_eV": L["Ea_mean_eV"],
                      "Ea_std": L["Ea_std_eV"], "D0": L["D0_mean_cm2_s"]}
                     for L in levels_out],
    }
    (out_root / "ensemble_results.json").write_text(
        json.dumps(summary, indent=2, default=str))
    print(f"\n==== {args.label} DONE ({summary['runtime_min']:.0f} min) ====")
    for h in summary["headline"]:
        print(f"  d={h['d']:.2f}  Ea={h['Ea_eV']} ± {h['Ea_std']} eV  D0={h['D0']}")
    print(f"  → {out_root / 'ensemble_results.json'}")


if __name__ == "__main__":
    main()
