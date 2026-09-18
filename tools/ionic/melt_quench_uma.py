#!/usr/bin/env python3
"""melt_quench_uma.py — LPSCl@Li₂S **1층**: 비정질 계면상 후보를 UMA NPT melt-quench 로 만들고 판정 지표를 찍는다.

카드: db/properties/lpscl_li2s_interphase_prereg_2026_09_11.json
      §2 ⭐_1층_개정_2026_09_11b (타깃·판정 지표) · §4 ⭐_1층_게이트 G1–G4

후보 (조성은 복합체 x 와 무관 — LPSCl 1 f.u. → Li₃PS₄ + LiCl, Li₂S 는 소모되지 않는다)
  A              Li₄PS₄Cl × n_fu(40) = 400 원자   a-Li₃PS₄·LiCl 균질 (Cl 이 유리망 안에)
  B              Li₃PS₄  × n_fu(50) = 400 원자   a-Li₃PS₄ 단독 (Cl 은 결정 LiCl 로 빠졌다는 가정)
  control_li7ps6 Li₇PS₆  × n_fu(28) = 392 원자   대조잡 — 1저자 원가설. 스스로 Li₃PS₄-like + Li₂S-like 로 갈라지나

절차 (G2 담금질 속도 선언 · G3 시드 ≥ 5 · G4 NPT 0 GPa, 밀도는 결과)
  ① 무작위 셀 — PS₄ 사면체(P–S 2.05 Å)를 **단위로** 무작위 배치(무작위 회전) + 자유 S·Li·Cl 무작위, 서로 다른 원자쌍 최소거리
     2.0 Å, 시작 밀도 1.2 g/cm³ (NPT 가 고친다)
  ② 짧은 FIRE 완화 (fmax 1.0 eV/Å · ≤ 200 스텝) — 겹침만 푼다
  ③ NPT Berendsen 0 GPa: T_melt(1200 K) 유지 --melt_ps → **선형 담금질** T_melt → T_final(300 K), 속도 --quench_rate [K/s]
     (10¹² K/s 면 900 ps) → T_final 유지 --hold_ps
  ④ 최종 FIRE 완화 (fmax 0.05) → final.xyz + final.vasp (VESTA 규율: xyz+POSCAR 쌍) + traj.xyz(--save_ps 간격) + result.json

판정 지표 (문턱은 카드에 있다 — 이 도구는 **값만 찍는다**)
  · PS₄ 보존율 = P 중 S 이웃(≤ 2.6 Å)이 정확히 4개인 비율 · P–S–P 가교 S 수 · P–P(≤ 2.4 Å) 수
  · Cl 환경 = Cl 의 Li 배위수(≤ 3.0 Å) 분포 · 6-배위 분율 · Cl–Cl 최근접 거리 분포와 3.4–3.9 Å 창 분율
  · Li₂S 국소질서 = S 중 Li 이웃(≤ 2.8 Å)이 8개 이상인 비율
  · 밀도 · 부분 g(r) (P–S · S–S · Li–S · Li–Cl · Cl–Cl) → Origin-ready CSV

⛔ 이 도구가 못 하는 것
  · 판정하지 않는다 — 지표를 찍고, 문턱 대조는 카드·사람이 한다.
  · UMA 오차를 모른다 — G1(QE 단일점 대조)은 별도 도구·별도 잡이다.
  · 담금질 속도가 물리적으로 타당한지 보증 못 한다 — 선언하고 기록할 뿐이다 (G2).
  · 결정화 여부를 못 가른다 — g(r)·배위수만 준다. XRD 지문은 tools/xrd/phase_fingerprint.py.
  · 2층(전도)을 하지 않는다 — 최종 구조를 넘길 뿐이다. 시드 하나만 돌리며, 앙상블 통계는 호출자가 모은다 (G3).
  · Berendsen 은 앙상블이 엄밀하지 않다 — 구조 생성용이지 수송 계산용이 아니다.
  · **밀도가 낮게 나온 원인을 스스로 못 가른다** — 배선인지 UMA·구조인지는 --npt_control 대조 잡이 가른다.
    그 대조도 "배로스탯이 ρ_UMA(0K) 를 지키나" 까지만 말한다. UMA 자신의 밀도 오차는 그 판정 밖이다.

  python3 tools/ionic/melt_quench_uma.py --system A --seed 1 --quench_rate 1e12 --out_root /data/work/runs/li2s_layer1
  python3 tools/ionic/melt_quench_uma.py --npt_control db/structures/sei_li2s_mp-1153.vasp --out_root /data/work/runs/li2s_layer1
  python3 tools/ionic/melt_quench_uma.py --selftest
"""
from __future__ import annotations
import argparse, json, math, os, pathlib, re, sys, time
import numpy as np

MASS = {"Li": 6.94, "P": 30.974, "S": 32.06, "Cl": 35.45}
EV_A3_TO_GPA = 160.21766208
# ⭐ 배로스탯 설정은 여기 한 곳에만 있다 — 대조 잡(--npt_control)이 생산 런과 **같은 설정**을 쓰지 않으면
#    아무것도 증명하지 못한다. 바꾸려면 여기서 바꾸고, 두 경로가 같이 따라간다.
BARO = {"taut_fs": 100.0, "taup_fs": 1000.0, "compressibility_au": 8.0}   # 8.0 Å³/eV ≈ 1/(20 GPa)
# ⭐ 앙상블 **선언** — G4("담금질은 NPT(0 GPa)")가 읽을 값이다. 실제로 쓰는 자리(run_melt_quench)와
#    같은 상수에서 plan.json 으로 내려가고, --gate_check 가 그것을 다시 읽어 thermo.csv 와 대조한다.
#    2026-09-14 추가: 이 필드가 없어서 seed1 의 앙상블을 thermo 에서 **역추적**해야 했다 —
#    게이트가 읽을 값이 기록에 없는 것은 9/13 에 부류로 정리한 '조용히 틀린 경로' 다.
ENSEMBLE = {"ensemble": "NPT", "thermostat": "Berendsen", "barostat": "Berendsen",
            "target_pressure_GPa": 0.0, "barostat_params": dict(BARO),
            "⛔_엄밀성": "Berendsen 은 부피 변동을 정확한 NPT 분포로 표본화하지 않는다 "
                        "(Bernetti–Bussi 2020) — 구조 생성용이지 앙상블 통계용이 아니다."}
FINAL_RELAX = {"kind": "FIRE", "fmax_eV_A": 0.05, "cell": "fixed",
               "⛔": "밀도는 **마지막 NPT 셀**의 값이고 구조 지표는 그 셀을 고정한 완화 구조의 값이다 "
                     "(개정 ③ — '300 K 평형 유리의 평균값' 이 아니다)."}
BAND_CARD = "db/properties/lpscl_li2s_layer1_amendment_2026_09_12.json"
BAND_PATH = ("1_바꾸는_것", "⑤_밴드_산수_정정")   # → 중심 · 밴드_±15%
P_TOL_GPA = 0.10        # --gate_check: |⟨P⟩| 허용 (npt_control 의 --control_p_tol 과 같은 눈금)
SYSTEMS = {                       # 식단위 조성 · 기본 n_fu
    "A":              ({"Li": 4, "P": 1, "S": 4, "Cl": 1}, 40),
    "B":              ({"Li": 3, "P": 1, "S": 4, "Cl": 0}, 50),
    "control_li7ps6": ({"Li": 7, "P": 1, "S": 6, "Cl": 0}, 28),
}
PS_BOND = 2.05          # Å — PS₄ 단위 초기 P–S
MIN_DIST = 2.0          # Å — Li 가 낀 쌍의 최소거리
MIN_DIST_ANION = 3.0    # Å — P·S·Cl 끼리(다른 단위) 최소거리: P 에 제3의 S 가 2.6 Å 안에 못 들어온다 (PS₄ 보존율 정의와 정합)
R_PS, R_PP, R_CLLI, R_SLI = 2.6, 2.4, 3.0, 2.8     # 지표 컷오프 (카드 §2 판정_지표)
CLCL_WIN = (3.4, 3.9)   # LiCl 결정 Cl–Cl 3.63 Å 창

# ───────────────────────── 기하 유틸 (numpy · MIC · 직교/비직교 셀) ─────────────────────────
def mic_dists(A, B, cell):
    """A(n,3) 와 B(m,3) 사이 최소상 거리 행렬 (n,m)."""
    cinv = np.linalg.inv(cell)
    d = A[:, None, :] - B[None, :, :]
    f = d @ cinv
    f -= np.round(f)
    return np.linalg.norm(f @ cell, axis=2)


def counts_within(A, B, cell, rcut, exclude_self=False):
    D = mic_dists(A, B, cell)
    if exclude_self:
        np.fill_diagonal(D, np.inf)
    return (D <= rcut).sum(axis=1), D


# ───────────────────────── ① 무작위 셀 ─────────────────────────
def _tetra_vertices(rng):
    """정사면체 4 꼭짓점(단위벡터)에 무작위 회전."""
    v = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float) / math.sqrt(3)
    q = rng.normal(size=4); q /= np.linalg.norm(q)            # 무작위 단위 사원수 → 회전행렬
    a, b, c, d = q
    R = np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                  [2*(b*c+a*d), a*a-b*b+c*c-d*d, 2*(c*d-a*b)],
                  [2*(b*d-a*c), 2*(c*d+a*b), a*a-b*b-c*c+d*d]])
    return v @ R.T


def build_random_cell(system, seed, density_g_cm3=1.2, n_fu=None, min_dist=MIN_DIST, max_tries=60000):
    """PS₄ 단위 + 자유 원자를 무작위로 채운 입방 셀. → (symbols list, positions (N,3), cell (3,3))"""
    if system not in SYSTEMS:
        raise SystemExit(f"⛔ 모르는 계 {system!r} — 카드에 있는 것: {sorted(SYSTEMS)}")
    comp, n_default = SYSTEMS[system]
    n_fu = int(n_fu or n_default)
    counts = {k: v * n_fu for k, v in comp.items() if v}
    mass_g = sum(MASS[k] * v for k, v in counts.items()) / 6.02214076e23
    L = (mass_g / density_g_cm3 * 1e24) ** (1.0 / 3.0)                 # Å
    cell = np.eye(3) * L
    rng = np.random.default_rng(seed)
    n_P = counts.get("P", 0)
    n_S_free = counts.get("S", 0) - 4 * n_P
    if n_S_free < 0:
        raise SystemExit(f"⛔ S 가 PS₄ 를 만들기에 모자란다 ({counts})")
    sym, pos = [], []
    def ok(new, new_sym):
        if not pos:
            return True
        D = mic_dists(np.asarray(new), np.asarray(pos), cell)
        heavy_new = np.array([s != "Li" for s in new_sym])[:, None]
        heavy_old = np.array([s != "Li" for s in sym])[None, :]
        need = np.where(heavy_new & heavy_old, MIN_DIST_ANION, min_dist)
        return bool((D >= need).all())
    tries = 0
    for _ in range(n_P):                                                 # PS₄ 단위
        while True:
            tries += 1
            if tries > max_tries:
                raise SystemExit(f"⛔ {system} 밀도 {density_g_cm3} g/cm³ 에 {max_tries}회 안에 못 채웠다 — 밀도를 낮춰라")
            p = rng.uniform(0, L, 3)
            unit = np.vstack([p, p + PS_BOND * _tetra_vertices(rng)])
            if ok(unit, ["P", "S", "S", "S", "S"]):
                sym += ["P", "S", "S", "S", "S"]; pos += unit.tolist(); break
    for el, n in (("S", n_S_free), ("Cl", counts.get("Cl", 0)), ("Li", counts.get("Li", 0))):
        for _ in range(n):
            while True:
                tries += 1
                if tries > max_tries:
                    raise SystemExit(f"⛔ {system} 밀도 {density_g_cm3} g/cm³ 에 {max_tries}회 안에 못 채웠다 — 밀도를 낮춰라")
                p = rng.uniform(0, L, 3)
                if ok([p], [el]):
                    sym.append(el); pos.append(p.tolist()); break
    return sym, np.asarray(pos), cell


# ───────────────────────── 판정 지표 ─────────────────────────
def indicators(sym, pos, cell):
    sym = np.asarray(sym); pos = np.asarray(pos, float); cell = np.asarray(cell, float)
    P = pos[sym == "P"]; S = pos[sym == "S"]; Li = pos[sym == "Li"]; Cl = pos[sym == "Cl"]
    out = {}
    if len(P) and len(S):
        nS, D_PS = counts_within(P, S, cell, R_PS)
        out["PS4_fraction"] = float((nS == 4).mean())
        out["P_S_coord_hist"] = {int(k): int(v) for k, v in zip(*np.unique(nS, return_counts=True))}
        nP_per_S = (D_PS.T <= R_PS).sum(axis=1)
        out["bridging_S_P2S7_like"] = int((nP_per_S >= 2).sum())
        nPP, _ = counts_within(P, P, cell, R_PP, exclude_self=True)
        out["P_P_bonds_P2S6_like"] = int(nPP.sum() // 2)
    if len(Cl):
        nLi, _ = counts_within(Cl, Li, cell, R_CLLI) if len(Li) else (np.zeros(len(Cl), int), None)
        out["Cl_Li_coord_hist"] = {int(k): int(v) for k, v in zip(*np.unique(nLi, return_counts=True))}
        out["Cl_6coord_fraction"] = float((nLi == 6).mean())
        if len(Cl) > 1:
            Dcc = mic_dists(Cl, Cl, cell); np.fill_diagonal(Dcc, np.inf)
            nn = Dcc.min(axis=1)
            out["ClCl_nearest_A"] = {"median": float(np.median(nn)), "min": float(nn.min()),
                                     "in_window_fraction": float(((nn >= CLCL_WIN[0]) & (nn <= CLCL_WIN[1])).mean()),
                                     "window_A": list(CLCL_WIN)}
    if len(S) and len(Li):
        nLiS, _ = counts_within(S, Li, cell, R_SLI)
        out["S_Li8_fraction_Li2S_like"] = float((nLiS >= 8).mean())
        out["S_Li_coord_hist"] = {int(k): int(v) for k, v in zip(*np.unique(nLiS, return_counts=True))}
    vol = abs(np.linalg.det(cell))
    if all(x in MASS for x in sym):
        mass_g = sum(MASS[x] for x in sym) / 6.02214076e23
    else:                                    # 카드 밖 원소(B 등) — ASE 질량
        from ase.data import atomic_masses, atomic_numbers
        mass_g = sum(atomic_masses[atomic_numbers[x]] for x in sym) / 6.02214076e23
    out["density_g_cm3"] = float(mass_g / (vol * 1e-24))
    out["n_atoms"] = int(len(sym)); out["cell_A"] = cell.tolist()
    return out


def partial_gr(sym, pos, cell, pairs=(("P", "S"), ("S", "S"), ("Li", "S"), ("Li", "Cl"), ("Cl", "Cl")), rmax=8.0, dr=0.05):
    sym = np.asarray(sym); pos = np.asarray(pos, float); vol = abs(np.linalg.det(cell))
    edges = np.arange(0, rmax + dr, dr); rc = 0.5 * (edges[1:] + edges[:-1])
    cols = {"r_A": rc}
    for a, b in pairs:
        A = pos[sym == a]; B = pos[sym == b]
        if not len(A) or not len(B):
            continue
        D = mic_dists(A, B, cell)
        if a == b:
            np.fill_diagonal(D, np.inf)
        h, _ = np.histogram(D[D < rmax], bins=edges)
        shell = 4 * math.pi * rc ** 2 * dr
        cols[f"g_{a}{b}"] = h / (len(A) * len(B) / vol) / shell
    return cols


# ───────────────────────── ③ MD ─────────────────────────
def make_calc(device="cuda", turbo=False):
    """UMA-s-1p1 · omat. turbo=True 면 fairchem 의 MD 용 inference_settings="turbo" 를 시도한다
    (원자 수·조성이 고정된 MD 전용 · 보통 ~2배). 이 fairchem 판에 없으면 **기본으로 내려가고 화면에 적는다** —
    조용히 다른 설정으로 돌지 않는다 (결과 파일 plan.json 에 실제 모드를 남긴다)."""
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    mode = "default"
    if turbo:
        try:
            pu = pretrained_mlip.get_predict_unit("uma-s-1p1", device=device, inference_settings="turbo"); mode = "turbo"
        except Exception as e:
            print(f"⚠ turbo 불가 ({type(e).__name__}: {e}) — 기본 모드로 돈다")
            pu = pretrained_mlip.get_predict_unit("uma-s-1p1", device=device)
    else:
        pu = pretrained_mlip.get_predict_unit("uma-s-1p1", device=device)
    calc = FAIRChemCalculator(pu, task_name="omat"); calc._mq_mode = mode
    return calc


def pressure_GPa(atoms, include_ideal_gas=True):
    """순간 압력 [GPa] = -tr(σ)/3.

    ⛔ 기본으로 **운동 항(ideal-gas)을 포함한다** — ASE 의 NPTBerendsen 이 제어하는 양이 그것이다.
    virial 만 찍으면 81원자·300 K·1283 Å³ 에서 NkT/V = 0.26 GPa 를 빠뜨려, 목표가 0 GPa 인데
    −0.30 으로 보인다. 2026-09-12 에 그 때문에 **배로스탯이 고장난 줄 알았다** (실제 총 압력은
    −0.05 GPa 로 정상이었다). 응력을 못 주는 계산기면 0 이 아니라 NaN.
    """
    try:
        try:
            sig = np.asarray(atoms.get_stress(voigt=True, include_ideal_gas=include_ideal_gas), float)
            return float(-(sig[0] + sig[1] + sig[2]) / 3.0 * EV_A3_TO_GPA)
        except TypeError:                                   # 구버전 ASE — 손으로 더한다
            sig = np.asarray(atoms.get_stress(voigt=True), float)
            P = -(sig[0] + sig[1] + sig[2]) / 3.0 * EV_A3_TO_GPA
            if include_ideal_gas:                           # P_kin = (2/3)·E_kin/V = NkT/V
                P += 2.0 / 3.0 * atoms.get_kinetic_energy() / atoms.get_volume() * EV_A3_TO_GPA
            return float(P)
    except Exception:
        return float("nan")


def cell_widths_A(cell):
    """셀의 **면간거리** (각 축에 수직인 폭) = V / |a_j × a_k|.

    ⛔ 원자 수가 아니라 이 값이 MIC 의 기준이다 — 이게 컷오프보다 작으면 원자가 자기 이미지를
    본다. primitive 셀은 원자 수가 같아도 폭이 훨씬 작다 (2026-09-12: Li₂S primitive ×2³ 는
    24 원자에 폭 6.6 Å 였고, 나는 conventional 을 가정해 96 원자로 알고 있었다).
    """
    C = np.asarray(cell, float)
    V = abs(np.linalg.det(C))
    return np.array([V / np.linalg.norm(np.cross(C[(i + 1) % 3], C[(i + 2) % 3])) for i in range(3)])


def auto_repeat(cell, min_width_A):
    """각 축 면간거리가 min_width 이상이 되도록 필요한 반복수 (1 이상)."""
    w = cell_widths_A(cell)
    return tuple(int(max(1, math.ceil(min_width_A / x - 1e-9))) for x in w)


def density_g_cm3(atoms):
    """g/cm³. 카드 밖 원소(대조 잡에 아무 결정이나 넣을 수 있다)는 ASE 질량으로 — MASS 는 4원소뿐이라
    예전 같으면 KeyError 로 죽었다. 생산 런 경로는 MASS 를 그대로 쓰므로 숫자가 안 바뀐다."""
    sy = atoms.get_chemical_symbols()
    m = sum(MASS[x] for x in sy) if all(x in MASS for x in sy) else float(atoms.get_masses().sum())
    return float(m / 6.02214076e23 / (atoms.get_volume() * 1e-24))


def _flushing_print(*a, **k):
    print(*a, **k); sys.stdout.flush()          # ⛔ 로그 리다이렉트 시 블록 버퍼링 (CLAUDE.md 규율)


def run_npt_control(atoms, calc, out, *, T_K, ps, dt_fs, save_ps=1.0, tol=0.03, p_tol=0.10,
                    min_width_A=9.0, cell_relax=True, max_relax_dV=0.10, log=_flushing_print):
    """⭐ 배로스탯 **대조 잡** — 알려진 결정을 같은 NPT 배선에 넣어 밀도를 지키는지 본다.

    비정질 밀도가 낮게 나왔을 때 원인이 두 갈래다: (ⓐ 우리 배선·단위가 틀렸다 / ⓑ UMA 또는 구조가 그렇다).
    이 잡이 그 둘을 가른다 — 결정을 **UMA 0 K 가변셀로 먼저 완화**해 ρ_UMA(0K) 를 얻고(= UMA 자신의 답),
    그 구조로 **생산 런과 같은 BARO 설정** NPT 를 돌려 ρ_NPT 를 얻는다.
      · **판정은 압력이다**: |⟨P_total⟩| ≤ p_tol (기본 0.10 GPa) 이면 배로스탯이 목표를 지킨다.
      · 밀도 drift(0 K → T_K)는 **열팽창이라 판정이 아니다** — 관측값으로만 적는다.
        2026-09-12 에 drift 3 % 를 배선 고장으로 읽은 적이 있다(실제 총 압력 −0.02 GPa).
    ρ_UMA(0K) 와 파일 밀도의 차이는 **UMA 자신의 오차**라 tol 판정에 넣지 않는다 — 따로 찍어서 사람이 본다.
    """
    from ase import units
    from ase.md.nptberendsen import NPTBerendsen
    from ase.md.velocitydistribution import MaxwellBoltzmannDistribution, Stationary
    from ase.io import write
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    w0 = cell_widths_A(atoms.get_cell())
    log(f"  [대조] {len(atoms)} 원자 · 면간거리 {w0[0]:.2f}/{w0[1]:.2f}/{w0[2]:.2f} Å (최소 {w0.min():.2f})")
    if w0.min() < min_width_A:
        log(f"  ⚠ 최소 면간거리 {w0.min():.2f} Å < {min_width_A} Å — MIC 여유가 얇다. "
            f"drift 가 문턱 근처로 나오면 배로스탯 탓인지 셀 탓인지 **못 가른다**.")
    atoms.calc = calc
    rho_file = density_g_cm3(atoms)
    ind_file = indicators(atoms.get_chemical_symbols(), atoms.get_positions(), np.asarray(atoms.get_cell()))
    rho_0K = P_0K = None; relax_note = "skipped"
    if cell_relax:
        try:
            from ase.filters import FrechetCellFilter as _CF
        except ImportError:
            from ase.constraints import ExpCellFilter as _CF        # 구버전 ASE
        from ase.optimize import LBFGS
        # ⛔ FIRE + 셀 필터는 셀 자유도에 큰 걸음을 내딛어 발산한다 (2026-09-12: Li₆PS₅Cl 이
        #    부피 +34 %, a 10.25 → 11.3 Å). LBFGS + maxstep 제한으로 바꿨다.
        opt = LBFGS(_CF(atoms), logfile=str(out / "cellrelax.log"), maxstep=0.05)
        opt.run(fmax=0.02, steps=500)
        rho_0K = density_g_cm3(atoms); P_0K = pressure_GPa(atoms)
        dV = rho_file / rho_0K - 1.0
        write(str(out / "relaxed_0K.xyz"), atoms, format="extxyz")
        ind_0K = indicators(atoms.get_chemical_symbols(), atoms.get_positions(), np.asarray(atoms.get_cell()))
        relax_note = f"steps={opt.get_number_of_steps()} fmax_reached={opt.converged()}"
        log(f"  [대조] ρ(파일) {rho_file:.3f} → ρ_UMA(0K) {rho_0K:.3f} g/cm³ "
            f"(부피 {100*dV:+.1f} % · P {P_0K:+.3f} GPa · {relax_note})")
        if ind_file.get("PS4_fraction") is not None:
            log(f"  [대조] PS₄ 보존 {ind_file['PS4_fraction']:.3f} → {ind_0K.get('PS4_fraction'):.3f}")
            if ind_0K.get("PS4_fraction", 1.0) < ind_file["PS4_fraction"] - 0.05:
                raise SystemExit("⛔ 0 K 완화에서 PS₄ 가 깨졌다 — 이 구조로는 밀도 대조가 성립하지 않는다. 멈춘다.")
        if abs(dV) > max_relax_dV:
            raise SystemExit(
                f"⛔ 0 K 완화가 부피를 {100*dV:+.1f} % 바꿨다 (허용 ±{100*max_relax_dV:.0f} %) — "
                "**이만큼 움직이면 대조가 아니다**. 시작 구조나 최적화를 먼저 고쳐라. "
                "NPT 만으로 판정하려면 --control_no_cellrelax 를 써라 (그때 기준은 파일 밀도다).")
    else:
        log(f"  [대조] ρ(파일) {rho_file:.3f} g/cm³ · 0 K 완화 건너뜀 — 기준은 **파일 밀도**다")
    MaxwellBoltzmannDistribution(atoms, temperature_K=T_K, rng=np.random.default_rng(0)); Stationary(atoms)
    dt = dt_fs * units.fs
    dyn = NPTBerendsen(atoms, dt, temperature_K=T_K, pressure_au=0.0,
                       taut=BARO["taut_fs"] * units.fs, taup=BARO["taup_fs"] * units.fs,
                       compressibility_au=BARO["compressibility_au"])
    n = int(round(ps * 1000 / dt_fs)); save_int = max(1, int(round(save_ps * 1000 / dt_fs))); _t0 = time.time()
    tlog = open(out / "thermo.csv", "w"); tlog.write("t_ps,T_K,T_set_K,density_g_cm3,volume_A3,E_pot_eV,P_GPa,P_virial_GPa\n")
    rows = []
    for step in range(n + 1):
        if step % save_int == 0:
            r, P = density_g_cm3(atoms), pressure_GPa(atoms)
            rows.append((step * dt_fs / 1000, r, P))
            tlog.write(f"{step*dt_fs/1000:.3f},{atoms.get_temperature():.1f},{T_K:.1f},{r:.4f},"
                       f"{atoms.get_volume():.2f},{atoms.get_potential_energy():.4f},{P:.4f},"
                       f"{pressure_GPa(atoms, include_ideal_gas=False):.4f}\n"); tlog.flush()
            if step and step % max(save_int, n // 10 or 1) == 0:
                log(f"  [대조] {step*dt_fs/1000:6.2f}/{ps:.0f} ps  ρ {r:.4f}  P {P:+.3f} GPa  "
                    f"({(time.time()-_t0)/60:.1f} min)")
        if step < n:
            dyn.run(1)
    tlog.close()
    half = [x for x in rows if x[0] >= rows[-1][0] / 2] or rows
    rho_npt = float(np.mean([x[1] for x in half])); P_npt = float(np.mean([x[2] for x in half]))
    ref, ref_name = ((rho_0K, "rho_UMA_0K") if rho_0K is not None else (rho_file, "rho_file"))
    drift = rho_npt / ref - 1.0
    res = {"kind": "npt_barostat_control", "T_K": T_K, "ps": ps, "dt_fs": dt_fs, "baro": dict(BARO),
           "cell_widths_A": [float(x) for x in w0], "min_cell_width_A": float(w0.min()),
           "min_width_required_A": min_width_A, "cell_wide_enough": bool(w0.min() >= min_width_A),
           "n_atoms": len(atoms), "composition": {e: atoms.get_chemical_symbols().count(e) for e in sorted(set(atoms.get_chemical_symbols()))},
           "rho_file_g_cm3": rho_file, "rho_UMA_0K_g_cm3": rho_0K, "P_UMA_0K_GPa": P_0K,
           "cell_relax": bool(cell_relax), "cell_relax_note": relax_note,
           "reference_for_drift": ref_name, "PS4_fraction_file": ind_file.get("PS4_fraction"),
           "rho_NPT_mean_last_half_g_cm3": rho_npt, "P_NPT_mean_last_half_GPa": P_npt,
           "drift_vs_UMA_0K": drift, "tol": tol,
           # ⭐ 배선 판정은 **압력**이다 (2026-09-12 재설계). 밀도 drift 로 판정하면 0 K 기준과
           #    300 K MD 사이의 **열팽창**을 배선 고장으로 읽는다 — 실제로 그렇게 오판했다
           #    (Li₂S: drift −3.0 % 인데 총 압력은 −0.02 GPa 로 정상이었다).
           "P_tol_GPa": p_tol, "plumbing_ok": bool(abs(P_npt) <= p_tol),
           "density_drift_is_thermal_expansion": ("0 K 기준 → %.0f K NPT 의 밀도 변화다. "
                                                  "판정이 아니라 관측값이다." % T_K),
           "alpha_V_apparent_per_K": (float(-drift / T_K) if T_K else None),
           "drift_tol_legacy_not_a_gate": True,
           "UMA_vs_file": (rho_0K / rho_file - 1.0) if rho_0K is not None else None,
           "⛔": "판정은 배선(배로스탯·단위)에 한정된다. UMA 자신의 밀도 오차(UMA_vs_file)는 이 판정 밖이다."}
    (out / "control.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    return res


def npt_msd(sym, pos, cells, dt_ps):
    """**NPT** 궤적의 원소별 MSD [Å²]. 셀이 프레임마다 변하므로 분수좌표에서 unwrap 한다.

    NVT 용 도구(framework_site_census.py 등)를 여기 쓰면 안 된다 — 그쪽은 셀이 변하면 멈춘다.
    절차: 분수좌표 차분 → MIC(round 빼기) → 그 프레임 셀로 실공간 증분 → 누적 → **전체 평균
    병진(드리프트) 제거** → 원소별 평균 제곱변위.
    """
    sym = np.asarray(sym); pos = np.asarray(pos, float); cells = np.asarray(cells, float)
    T, N, _ = pos.shape
    frac = np.einsum("tnj,tjk->tnk", pos, np.linalg.inv(cells))
    df = np.diff(frac, axis=0)
    df -= np.round(df)
    steps = np.einsum("tnj,tjk->tnk", df, cells[1:])
    disp = np.concatenate([np.zeros((1, N, 3)), np.cumsum(steps, axis=0)])
    disp -= disp.mean(axis=1, keepdims=True)
    t = np.arange(T) * dt_ps
    return t, {str(e): ((disp[:, sym == e] ** 2).sum(-1)).mean(-1) for e in sorted(set(sym))}


def fit_D(t, msd, t_from, t_to):
    """자유절편 선형맞춤 msd = 6 D t + c → D [cm²/s] (1 Å²/ps = 1e-4 cm²/s)."""
    m = (t >= t_from) & (t <= t_to)
    if m.sum() < 4:
        return None, None
    a, c = np.polyfit(t[m], msd[m], 1)
    return float(a / 6.0 * 1e-4), float(c)


def melt_check(run_dir, *, d_melt_cm2s=1e-6, log=print):
    """⭐ **녹았나** — melt 구간에서 P 골격이 확산했는지 본다 (관측 후 진단, 사전등록 게이트 아님).

    안 녹았으면 담금질은 초기 무작위 충전의 채움밀도를 그대로 얼린 것이고, 그때 밀도는
    물리가 아니라 생성기 설정이다. G4 밴드를 논하기 **전에** 이걸 먼저 가른다.

    ⛔ 못 하는 것: 결정화 여부를 못 본다(g(r)·XRD 가 따로 있다) · 문턱 1e-6 cm²/s 는
    액체/고체를 가르는 **진단값**이고 카드 문턱이 아니다 · 시드 하나로 판정하지 않는다.
    """
    from ase.io import read
    run = pathlib.Path(run_dir)
    plan = json.loads((run / "plan.json").read_text(encoding="utf-8"))
    frames = read(str(run / "traj.xyz"), index=":")
    if len(frames) < 8:
        raise SystemExit(f"⛔ 프레임이 {len(frames)}개뿐이다 — MSD 를 못 낸다")
    dt_ps = plan["save_ps"] if "save_ps" in plan else None
    if dt_ps is None:                       # 옛 plan.json — 전체 길이에서 유도한다
        total = plan["melt_ps"] + plan["quench_ps"] + plan["hold_ps"]
        dt_ps = total / (len(frames) - 1)
        log(f"  ⚠ plan.json 에 save_ps 가 없다 — 전체 {total:.0f} ps / {len(frames)-1} 구간 = {dt_ps:.3f} ps 로 유도")
    sym = frames[0].get_chemical_symbols()
    pos = np.array([f.get_positions() for f in frames])
    cells = np.array([np.asarray(f.get_cell()) for f in frames])
    t, msd = npt_msd(sym, pos, cells, dt_ps)
    melt_ps = float(plan["melt_ps"])
    half = melt_ps / 2.0
    out = {"kind": "melt_check", "run": str(run), "n_frames": len(frames), "dt_ps": dt_ps,
           "melt_ps": melt_ps, "fit_window_ps": [half, melt_ps], "T_melt_K": plan.get("T_melt_K"),
           "d_melt_threshold_cm2_s": d_melt_cm2s, "per_element": {}}
    for e, m in msd.items():
        i = int(np.searchsorted(t, melt_ps))
        D, c = fit_D(t, m, half, melt_ps)
        out["per_element"][e] = {"msd_at_melt_end_A2": float(m[min(i, len(m) - 1)]),
                                "D_melt_cm2_s": D, "intercept_A2": c}
        log(f"  [melt] {e:2s}  MSD({melt_ps:.0f} ps) {m[min(i,len(m)-1)]:8.2f} Å²  "
            f"D {('%.3e' % D) if D is not None else '—':>10s} cm²/s")
    P = out["per_element"].get("P", {})
    DP = P.get("D_melt_cm2_s")
    out["framework_diffused"] = bool(DP is not None and DP > d_melt_cm2s)
    out["verdict"] = ("melted" if out["framework_diffused"] else "not_melted_framework_frozen")
    out["⛔"] = ("진단이다. 'melted' 가 구조가 좋다는 뜻이 아니고, 'not_melted' 면 그 담금질의 밀도는 "
                 "물리가 아니라 생성기 채움밀도다 — G4 밴드를 논하기 전에 이걸 고친다.")
    return out


def schedule(T_melt, T_final, quench_rate_K_s, dt_fs):
    if quench_rate_K_s is None or quench_rate_K_s <= 0:
        raise SystemExit("⛔ --quench_rate [K/s] 를 주어라 (G2: 담금질 속도는 결과 보기 전에 선언한다). 기본값은 없다.")
    quench_ps = (T_melt - T_final) / quench_rate_K_s * 1e12
    n = int(round(quench_ps * 1000.0 / dt_fs))
    return quench_ps, n


def run_melt_quench(atoms, calc, out, *, seed, T_melt, T_final, melt_ps, quench_rate, hold_ps, dt_fs, save_ps,
                    pre_relax=True, log=print):
    from ase import units
    from ase.io import write
    from ase.md.nptberendsen import NPTBerendsen
    from ase.md.velocitydistribution import MaxwellBoltzmannDistribution, Stationary
    from ase.optimize import FIRE
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    atoms.calc = calc
    if pre_relax:
        FIRE(atoms, logfile=str(out / "prerelax.log")).run(fmax=1.0, steps=200)
    MaxwellBoltzmannDistribution(atoms, temperature_K=T_melt, rng=np.random.default_rng(seed)); Stationary(atoms)
    dt = dt_fs * units.fs
    dyn = NPTBerendsen(atoms, dt, temperature_K=T_melt, pressure_au=0.0,
                       taut=BARO["taut_fs"] * units.fs, taup=BARO["taup_fs"] * units.fs,
                       compressibility_au=BARO["compressibility_au"])
    quench_ps, n_q = schedule(T_melt, T_final, quench_rate, dt_fs)
    n_m = int(round(melt_ps * 1000 / dt_fs)); n_h = int(round(hold_ps * 1000 / dt_fs))
    save_int = max(1, int(round(save_ps * 1000 / dt_fs)))
    trj = out / "traj.xyz"; trj.unlink(missing_ok=True)
    tlog = open(out / "thermo.csv", "w"); tlog.write("t_ps,T_K,T_set_K,density_g_cm3,volume_A3,E_pot_eV,P_GPa,P_virial_GPa\n")
    step = 0; t0 = time.time()
    def record(T_set):
        nonlocal step
        if step % save_int == 0:
            write(str(trj), atoms, format="extxyz", append=True)
            vol = atoms.get_volume(); rho = sum(MASS[s] for s in atoms.get_chemical_symbols()) / 6.02214076e23 / (vol * 1e-24)
            tlog.write(f"{step*dt_fs/1000:.3f},{atoms.get_temperature():.1f},{T_set:.1f},{rho:.4f},{vol:.2f},"
                       f"{atoms.get_potential_energy():.4f},{pressure_GPa(atoms):.4f},"
                       f"{pressure_GPa(atoms, include_ideal_gas=False):.4f}\n"); tlog.flush()
    chunk = 50
    for phase, n_steps, Tfun in (("melt", n_m, lambda i: T_melt),
                                 ("quench", n_q, lambda i: T_melt - (T_melt - T_final) * i / max(1, n_q)),
                                 ("hold", n_h, lambda i: T_final)):
        i = 0
        while i < n_steps:
            T_set = Tfun(i); dyn.set_temperature(temperature_K=T_set)
            k = min(chunk, n_steps - i)
            for _ in range(k):
                record(T_set); dyn.run(1); step += 1
            i += k
            if (i // chunk) % 200 == 0:
                log(f"  [{phase}] {i}/{n_steps} T_set={T_set:.0f} K T={atoms.get_temperature():.0f} K "
                    f"ρ={sum(MASS[s] for s in atoms.get_chemical_symbols())/6.02214076e23/(atoms.get_volume()*1e-24):.3f} "
                    f"({(time.time()-t0)/60:.1f} min)")
                sys.stdout.flush()   # ⛔ 로그 리다이렉트 시 블록 버퍼링 — 안 하면 진행 줄이 몇 시간 뒤에 뜬다
    record(T_final); tlog.close()
    FIRE(atoms, logfile=str(out / "final_relax.log")).run(fmax=0.05, steps=2000)
    write(str(out / "final.xyz"), atoms, format="extxyz")
    write(str(out / "final.vasp"), atoms, format="vasp", direct=True, sort=True)
    return {"quench_ps": quench_ps, "n_steps": {"melt": n_m, "quench": n_q, "hold": n_h}, "wall_min": (time.time() - t0) / 60}


def write_gr_csv(cols, path):
    keys = list(cols)
    with open(path, "w") as f:
        f.write(",".join(keys) + "\n")
        for i in range(len(cols["r_A"])):
            f.write(",".join(f"{cols[k][i]:.5f}" for k in keys) + "\n")


def build_plan(system, seed, sym, density, T_melt, T_final, melt_ps,
               quench_rate, quench_ps, hold_ps, dt_fs, save_ps):
    """plan.json 의 내용. **게이트가 읽을 값이 여기서 들어간다** — 읽는 곳은 `--gate_check`."""
    return {"system": system, "seed": seed, "n_atoms": len(sym),
            "composition": {e: sym.count(e) for e in sorted(set(sym))},
            "start_density_g_cm3": density, "T_melt_K": T_melt, "T_final_K": T_final, "melt_ps": melt_ps,
            "quench_rate_K_s": quench_rate, "quench_ps": quench_ps, "hold_ps": hold_ps, "dt_fs": dt_fs,
            "save_ps": save_ps,   # ⛔ 빠뜨리면 --melt_check 가 dt 를 **유도**한다 (2026-09-12)
            "G2_declared_before_results": True,
            "card": "db/properties/lpscl_li2s_interphase_prereg_2026_09_11.json",
            # ⭐ 게이트가 읽는 값 — 누가 읽나: `--gate_check`. 없으면 그 모드가 **기록없음** 으로 fail-closed 한다.
            "게이트_입력": {"G2_quench_rate_K_s": quench_rate, **ENSEMBLE, "final_relax": FINAL_RELAX,
                         "G4_band_card": BAND_CARD, "읽는_곳": "melt_quench_uma.py --gate_check <run_dir>"}}


# ───────────────────────── --mode_stress: 실행모드별 **응력** 대조 (회신 BR Q4) ─────────────────────────
KAPPA_PER_GPA = 1.0 / 20.0      # BARO compressibility_au 8.0 Å³/eV ≈ 1/(20 GPa). 환산 규칙이지 문턱이 아니다.


def read_frame_card(card):
    """봉인된 프레임 표본을 카드에서 읽는다. 도구가 프레임을 **고르지 않는다**.

    ⛔ 못 하는 것: 카드가 없거나 t_ps 목록이 없으면 죽는다 — 기본 표본을 지어내지 않는다."""
    q = pathlib.Path(card)
    if not q.exists():
        q = pathlib.Path(__file__).resolve().parents[2] / card
    d = json.loads(q.read_text(encoding="utf-8"))
    try:
        want = list(d["1_프레임_표본_봉인"]["t_ps"])
    except (KeyError, TypeError):
        raise KeyError(f"{q}: `1_프레임_표본_봉인.t_ps` 가 없다 — 표본을 도구가 지어내지 않는다")
    if not want or len(set(want)) != len(want):
        raise ValueError(f"{q}: t_ps 가 비었거나 중복이다 ({want})")
    return [float(x) for x in want], str(q)


def frame_index_map(traj_path, thermo_path):
    """traj 프레임 수와 thermo 행 수가 같은지 확인하고 t_ps ↔ 색인 대응을 만든다.

    ⛔ 다르면 **멈춘다**. '아마 같은 간격일 것' 으로 넘어가면 엉뚱한 프레임을 재게 된다."""
    from ase.io import iread
    n_traj = sum(1 for _ in iread(str(traj_path), index=":", format="extxyz"))
    t = read_thermo(thermo_path)
    n_thermo = len(t["t_ps"])
    if n_traj != n_thermo:
        raise ValueError(f"⛔ traj 프레임 {n_traj} ≠ thermo 행 {n_thermo} — 색인 대응을 만들 수 없다")
    return {float(v): i for i, v in enumerate(t["t_ps"])}, n_traj


def stress_report(atoms, calc):
    """같은 **미완화** 셀·좌표에서 potential/virial 응력과 힘. (운동 항 없음 — 비교 규칙)"""
    atoms = atoms.copy(); atoms.calc = calc
    sig = np.asarray(atoms.get_stress(voigt=False))          # eV/Å³
    F = np.asarray(atoms.get_forces())
    return {"P_virial_GPa": float(-np.trace(sig) / 3.0 * EV_A3_TO_GPA),
            "sigma_GPa": sig * EV_A3_TO_GPA, "F": F,
            "sigma_rms_GPa": float(np.sqrt(((sig * EV_A3_TO_GPA) ** 2).mean())),
            "F_rms_eVA": float(np.sqrt((F ** 2).mean()))}


def mode_stress(run, card, device="cuda", log=print):
    """봉인된 프레임에서 turbo − default 의 **응력·힘** 차이를 찍는다. 새 MD 0.

    ⛔ 이 함수가 못 하는 것
      · 합격/불합격을 정하지 않는다 — 카드 §3 이 '문턱을 정하지 않는다' 고 봉인했다.
      · UMA 가 맞는지 모른다 — 그것은 G1(QE 참조)이다.
      · 작은 차이를 **전체 담금질 경로의 승인**으로 읽지 않는다 (그 프레임들의 일치까지다).
    """
    run = pathlib.Path(run)
    want, card_path = read_frame_card(card)
    idx, n_traj = frame_index_map(run / "traj.xyz", run / "thermo.csv")
    missing = [w for w in want if w not in idx]
    if missing:
        raise ValueError(f"⛔ 봉인된 프레임 중 traj 에 없는 것: {missing}")
    from ase.io import iread
    wanted_i = {idx[w]: w for w in want}
    frames = {}
    for i, at in enumerate(iread(str(run / "traj.xyz"), index=":", format="extxyz")):
        if i in wanted_i:
            frames[wanted_i[i]] = at
        if len(frames) == len(want):
            break
    log(f"카드: {card_path}")
    log(f"봉인된 프레임 {len(want)}개 · traj {n_traj} 프레임에서 색인 대조 통과")
    cal_d = make_calc(device, turbo=False)
    cal_t = make_calc(device, turbo=True)
    if getattr(cal_t, "_mq_mode", "default") != "turbo":
        log("⛔ turbo 를 못 켰다 — 두 모드가 같은 것이라 비교가 성립하지 않는다. 멈춘다.")
        raise SystemExit(3)
    rows = []
    for w in want:
        at = frames[w]
        rd, rt = stress_report(at, cal_d), stress_report(at, cal_t)
        dP = rt["P_virial_GPa"] - rd["P_virial_GPa"]
        dsig = float(np.abs(rt["sigma_GPa"] - rd["sigma_GPa"]).max())
        dF = float(np.abs(rt["F"] - rd["F"]).max())
        rows.append({"t_ps": w, "P_default_GPa": rd["P_virial_GPa"], "P_turbo_GPa": rt["P_virial_GPa"],
                     "dP_GPa": dP, "dV_over_V_pct": 100.0 * dP * KAPPA_PER_GPA,
                     "max_dsigma_GPa": dsig, "sigma_rms_GPa": rd["sigma_rms_GPa"],
                     "max_dF_eVA": dF, "F_rms_eVA": rd["F_rms_eVA"]})
        log(f"  t={w:7.1f} ps  P_def {rd['P_virial_GPa']:+8.4f}  P_tur {rt['P_virial_GPa']:+8.4f}  "
            f"ΔP {dP:+.4f} GPa (ΔV/V {100.0*dP*KAPPA_PER_GPA:+.3f} %)  "
            f"max|Δσ| {dsig:.4f}  max|ΔF| {dF:.2e} (|F|rms {rd['F_rms_eVA']:.3f})")
    res = {"card": card_path, "run": str(run), "n_frames": len(rows), "frames": rows,
           "max_abs_dP_GPa": max(abs(r["dP_GPa"]) for r in rows),
           "max_abs_dV_over_V_pct": max(abs(r["dV_over_V_pct"]) for r in rows),
           "max_dsigma_GPa": max(r["max_dsigma_GPa"] for r in rows),
           "max_dF_eVA": max(r["max_dF_eVA"] for r in rows),
           "⛔_문턱": "카드 §3 — 이 잡은 문턱을 정하지 않는다. 앵커는 G1 의 default − QE 응력 차이다.",
           "⛔_작은_차이의_뜻": "이 프레임들의 일치일 뿐 전체 담금질 경로의 승인이 아니다."}
    log(f"\n  max|ΔP| {res['max_abs_dP_GPa']:.4f} GPa → ΔV/V {res['max_abs_dV_over_V_pct']:+.3f} % "
        f"· max|Δσ| {res['max_dsigma_GPa']:.4f} GPa · max|ΔF| {res['max_dF_eVA']:.2e} eV/Å")
    log("  ⛔ 문턱 없음 — 보고만 한다. 작은 차이는 이 프레임들의 일치이지 경로 전체의 승인이 아니다.")
    return res


# ───────────────────────── --gate_check: 기록이 게이트를 먹여주는가 ─────────────────────────
def read_thermo(path):
    """thermo.csv → {열이름: np.array}. 열이 없으면 **죽는다** (없는 값을 0 으로 그리지 않는다)."""
    lines = pathlib.Path(path).read_text(encoding="utf-8").strip().splitlines()
    if len(lines) < 2:
        raise ValueError(f"{path}: 자료 줄이 없다")
    keys = lines[0].split(",")
    cols = np.array([[float(x) for x in ln.split(",")] for ln in lines[1:] if ln.strip()])
    return {k: cols[:, i] for i, k in enumerate(keys)}


def read_band(card=BAND_CARD):
    """G4 밴드를 **카드에서** 읽는다 — 도구가 숫자를 자체 보관하지 않는다.
    절이나 키가 없으면 KeyError 로 죽는다: '못 찾음' 을 기본값으로 채우지 않는다."""
    q = pathlib.Path(card)
    if not q.exists():                       # repo 루트 상대 (도구가 어디서 불리든 같은 카드)
        q = pathlib.Path(__file__).resolve().parents[2] / card
    d = json.loads(q.read_text(encoding="utf-8"))
    for k in BAND_PATH:
        if not isinstance(d, dict) or k not in d:
            raise KeyError(f"{q}: 밴드 절 '{k}' 가 없다 — 밴드를 도구가 지어내지 않는다")
        d = d[k]
    lo, hi = d["밴드_±15%"]
    return float(d["중심"]), float(lo), float(hi)


def hold_segment(t):
    """thermo 의 **마지막 연속 T_set 일정 구간**(= 300 K 유지)의 불리언 마스크.

    ⚠ 담금질 램프의 **마지막 프레임은 T_set 이 이미 T_final** 이라 유지 구간에 포함된다. 의도한 선택이다
    (그 순간부터 목표 온도다). 프레임 하나 차이이고, 배제하려면 호출부가 t 범위를 직접 자른다.

    ⛔ 이 함수가 못 하는 것: 유지 구간이 평형인지 말하지 않는다. 어디까지가 유지인지만 고른다."""
    if "T_set_K" not in t:
        raise KeyError("thermo.csv 에 T_set_K 가 없다 — 유지 구간을 **추측하지 않는다**")
    ts = t["T_set_K"]
    last = ts[-1]
    m = np.isclose(ts, last)
    # 마지막 연속 구간만 (담금질 램프가 지나가며 같은 값을 스칠 수 있다)
    i = len(m) - 1
    while i > 0 and m[i - 1]:
        i -= 1
    out = np.zeros_like(m); out[i:] = True
    return out


def hold_trend(t, n_blocks=5):
    """유지 구간 **전체**를 n 블록으로 나눠 블록별 ⟨P⟩·⟨ρ⟩ 와 ρ 표류를 찍는다. 새 계산 0.

    ⛔ 판정이 아니다 — 표류는 '유지시간이 모자랐다' 의 근거가 되고, 무표류는 **그 구간의 안정**만 지지한다.
    ⛔ 블록 평균의 산포는 표본 표준편차이지 평균의 신뢰구간이 아니다 (자기상관이 크다)."""
    m = hold_segment(t)
    tt, P, rho = t["t_ps"][m], t["P_GPa"][m], t["density_g_cm3"][m]
    if len(tt) < n_blocks:
        n_blocks = max(1, len(tt))
    idx = np.array_split(np.arange(len(tt)), n_blocks)
    blocks = [{"t_from_ps": float(tt[k[0]]), "t_to_ps": float(tt[k[-1]]), "n": int(len(k)),
               "P_mean_GPa": float(P[k].mean()), "rho_mean": float(rho[k].mean())} for k in idx if len(k)]
    span = float(tt[-1] - tt[0])
    slope = float(np.polyfit(tt, rho, 1)[0]) if len(tt) > 1 and span > 0 else 0.0
    return {"hold_from_ps": float(tt[0]), "hold_to_ps": float(tt[-1]), "hold_len_ps": span,
            "n_frames": int(len(tt)), "n_blocks": len(blocks), "blocks": blocks,
            "rho_slope_per_ps": slope, "rho_drift_pct_over_hold": float(100.0 * slope * span / rho.mean()),
            "block_rho_spread_pct": float(100.0 * (max(b["rho_mean"] for b in blocks)
                                                   - min(b["rho_mean"] for b in blocks)) / rho.mean()),
            "⛔": "관측이지 평형 검정이 아니다. 표류 없음은 **이 구간의 안정**만 지지한다."}


def gate_check(run, band_card=BAND_CARD, win_ps=10.0, p_tol=P_TOL_GPA, n_blocks=5, log=print):
    """plan.json 의 **앙상블 선언**이 있는지 보고, 있으면 thermo.csv 로 대조한 뒤 G4(밀도 밴드)를 찍는다.

    ⛔ 이 함수가 못 하는 것
      · 판정하지 않는다 — G4 가 '밴드 밖' 으로 발화하는지까지만 말하고, 원인(UMA·셀·담금질)은 안 가른다.
      · ⟨P⟩≈0 을 정확한 NPT 표본화의 증명으로 읽지 않는다 (Berendsen).
      · 기록이 없는 옛 런에서 thermo 로 **역추적**은 하되, 그것을 기록으로 승격하지 않는다.
    """
    run = pathlib.Path(run)
    plan = json.loads((run / "plan.json").read_text(encoding="utf-8"))
    g = plan.get("게이트_입력")
    res = {"run": str(run), "record_has_gate_input": bool(g),
           "출처": "plan.json 선언" if g else "thermo.csv 역추적 (기록 아님)"}
    if not g:
        log("⛔ plan.json 에 `게이트_입력` 이 없다 — G4 가 요구하는 앙상블·목표압력이 **기록에 없다**.")
        log("   2026-09-12 이전 실행이다. 아래 수치는 thermo 에서 역추적한 것이고, 기록이 아니다.")
    t = read_thermo(run / "thermo.csv")
    tail = t["t_ps"] >= t["t_ps"].max() - win_ps
    P, rho, T = t["P_GPa"][tail], t["density_g_cm3"][tail], t["T_K"][tail]
    res.update({"win_ps": win_ps, "n_frames": int(tail.sum()),
                "★_통계의_뜻": {
                  "P_sd_GPa": "저장된 표본의 **표준편차**다. 평균의 신뢰구간이 아니고 자기상관이 크다.",
                  "rho_flat_pct": "(최대−최소)/평균이다. **표류·평형을 검정한 값이 아니다.**",
                  "P_GPa": "**운동 항을 포함한 총 수압**이다. 평균이 0에 가까워도 응력텐서 전체가 0은 아니다."},
                "T_mean_K": float(T.mean()),
                "P_mean_GPa": float(P.mean()), "P_sd_GPa": float(P.std(ddof=1)) if tail.sum() > 1 else 0.0,
                "rho_mean": float(rho.mean()), "rho_min": float(rho.min()), "rho_max": float(rho.max()),
                "rho_last": float(t["density_g_cm3"][-1])})
    tgt = float(g["target_pressure_GPa"]) if g else 0.0
    res["target_pressure_GPa"] = tgt
    res["pressure_ok"] = abs(res["P_mean_GPa"] - tgt) <= p_tol
    res["rho_flat_pct"] = 100.0 * (res["rho_max"] - res["rho_min"]) / res["rho_mean"]
    c, lo, hi = read_band(band_card)
    res.update({"band_center": c, "band_lo": lo, "band_hi": hi, "band_card": str(band_card),
                "dev_pct_vs_center": 100.0 * (res["rho_last"] / c - 1.0),
                "in_band": bool(lo <= res["rho_last"] <= hi)})
    res["G4_fires"] = not res["in_band"]
    res["G4_role"] = "alert"        # ⭐ 합격선이 아니다 (D-2026-09-14-li2s-layer1-density-alert)
    res["G4_원인_지정"] = None       # 게이트는 원인을 지정하지 않는다 (셀·모델·후보상 어느 것도)
    res["허용_서술"] = ("마지막 {:.0f} ps 에서 목표 근처의 총 수압 평균과 좁은 밀도 범위가 관측됐다. "
                     "충분한 밀도 이완·준비 이력 소멸·모델의 압력–부피 정확성은 아직 확인되지 않았다."
                     ).format(win_ps)
    try:
        res["hold_trend"] = hold_trend(t, n_blocks)
    except KeyError as e:
        res["hold_trend"] = {"⛔": str(e)}
    log(f"  앙상블 기록 {'있음' if g else '⛔없음'} · {res['출처']}")
    log(f"  마지막 {win_ps:.0f} ps ({res['n_frames']} 표본): ⟨P_총수압⟩ {res['P_mean_GPa']:+.3f} GPa "
        f"(표본 sd {res['P_sd_GPa']:.3f}, 목표 {tgt:+.2f}, 허용 ±{p_tol}) "
        f"→ {'목표 근처' if res['pressure_ok'] else '목표에서 벗어남'}")
    log(f"  ρ {res['rho_min']:.4f}–{res['rho_max']:.4f} (범위/평균 {res['rho_flat_pct']:.2f} %) · "
        f"마지막 {res['rho_last']:.4f} g/cm³")
    ht = res.get("hold_trend", {})
    if "blocks" in ht:
        log(f"  유지 구간 {ht['hold_from_ps']:.0f}–{ht['hold_to_ps']:.0f} ps 를 {ht['n_blocks']} 블록으로:")
        for b in ht["blocks"]:
            log(f"    {b['t_from_ps']:7.1f}–{b['t_to_ps']:7.1f} ps (n={b['n']:4d})  "
                f"⟨P⟩ {b['P_mean_GPa']:+.3f} GPa  ⟨ρ⟩ {b['rho_mean']:.4f}")
        log(f"    ρ 표류 {ht['rho_drift_pct_over_hold']:+.3f} % / 유지 전체 · "
            f"블록 산포 {ht['block_rho_spread_pct']:.3f} %")
    else:
        log(f"  ⛔ 유지 구간 블록 추세 없음: {ht.get('⛔', '계산 안 됨')}")
    log(f"  밴드 [{lo:.4f}, {hi:.4f}] 중심 {c:.4f} → {res['dev_pct_vs_center']:+.2f} % · "
        + ("G4 **경보**" if res["G4_fires"] else "밴드 안"))
    log("  ⛔ G4 는 **합격선이 아니라 적정성 경보**다 — 셀 오류·모델 오류·후보상 기각 중 아무것도 확정하지 않는다.")
    log("  ⛔ 위 수치는 **단기 안정성**이다. 밀도 이완·준비 이력 소멸·모델의 압력–부피 정확성은 확인되지 않았다.")
    return res


# ───────────────────────── --gb2: G-B2 겹침 (소셀 ↔ 400 원자) ─────────────────────────
#: 판정량은 카드 §4 G-B2 가 정한다 — 도구가 쌍을 고르지 않는다.
GB2_CARD = "db/properties/lpscl_smallcell_uma_qe_force_estimand_2026_09_16.json"
GB2_PAIRS = (("P", "S"), ("Li", "S"), ("Li", "Cl"), ("S", "S"))
GR_FLOOR = 1.0          # 첫 봉우리 탐색 바닥 — g > 1 (무상관 밀도 위). 잡음 스파이크 배제용.

#: 문턱 산문에서 숫자를 캐는 패턴. **사본을 만들지 않는다** (아래 docstring).
GB2_PATS = {
    "gr_first_peak_A": r"첫 봉우리 위치가\s*\*{0,2}([0-9.]+)\s*Å\s*이내",
    "coord_mean":      r"배위수 평균이\s*\*{0,2}([0-9.]+)\s*이내",
    "ps4_pp":          r"PS₄ 보존율 차이가\s*\*{0,2}([0-9.]+)\s*%p\s*이내",
    "r_window_A":      r"r\s*≤\s*\*{0,2}([0-9.]+)\s*Å",
}


def read_gb2_thresholds(card=GB2_CARD):
    """G-B2 문턱 넷을 **봉인된 산문에서 직접** 판다.

    왜 옮겨 적지 않나: 카드의 문턱은 산문 한 줄이다. 기계용으로 전사하면 **두 벌**이 되고
    둘이 갈라진다 — 원장이 이기는데 도구는 사본을 본다. 그래서 사본을 만들지 않고 원문을 판다.
    넷 중 하나라도 못 찾으면 **죽는다**: 기본값을 지어내지 않는다.
    """
    q = pathlib.Path(card)
    if not q.exists():
        q = pathlib.Path(__file__).resolve().parents[2] / card
    d = json.loads(q.read_text(encoding="utf-8"))
    try:
        prose = d["4_검증_게이트_결과_보기_전에_정한다"]["G-B2_겹침_🔴_이_카드의_핵심"]["문턱"]
        why_r = d["4_검증_게이트_결과_보기_전에_정한다"]["G-B2_겹침_🔴_이_카드의_핵심"]["왜_r_≤_5_Å"]
    except (KeyError, TypeError):
        raise KeyError(f"{q}: G-B2 `문턱` 절이 없다 — 도구가 문턱을 지어내지 않는다")
    src = f"{prose}\n{why_r}"
    th = {}
    for k, pat in GB2_PATS.items():
        m = re.search(pat, src)
        if not m:
            raise ValueError(f"⛔ {q}: G-B2 문턱 '{k}' 를 산문에서 못 찾았다 — "
                             f"카드 문구가 바뀌었으면 **도구를 고치고 시험을 다시 친다**. "
                             f"기본값으로 넘어가지 않는다.\n  판 문장: {src[:200]}")
        th[k] = float(m.group(1))
    return th, str(q)


def first_peak_A(r, g, rmax, floor=GR_FLOOR):
    """r ≤ rmax 안에서 **첫 국소최대**의 위치 [Å]. 최대봉우리 위치도 같이 준다.

    ⛔ '첫 봉우리' 와 '최대 봉우리' 가 다르면 그 사실을 **올린다** — 조용히 하나를 고르지 않는다.
       (이 계의 P–S·Li–S 는 보통 같지만, S–S 는 다를 수 있다.)
    ⛔ 봉우리가 아예 없으면 None — 0.0 으로 그리지 않는다."""
    r = np.asarray(r, float); g = np.asarray(g, float)
    m = r <= rmax
    r, g = r[m], g[m]
    if len(r) < 3 or not np.isfinite(g).any():
        return None
    g = np.nan_to_num(g, nan=0.0, posinf=0.0, neginf=0.0)
    gi = int(np.argmax(g))
    if g[gi] < floor:
        return None                      # 전부 무상관 — 봉우리가 **없다** ("못 찾음" 과 구분)
    fi = None
    for i in range(1, len(g) - 1):
        if g[i] >= floor and g[i] >= g[i - 1] and g[i] > g[i + 1]:
            fi = i
            break
    fallback = fi is None
    if fallback:
        fi = gi                          # 국소최대가 없다(단조 상승) → 최대점을 쓰고 **표시한다**
    return {"first_A": float(r[fi]), "global_A": float(r[gi]),
            "g_first": float(g[fi]), "g_global": float(g[gi]),
            "first_is_global": bool(fi == gi), "no_local_max": bool(fallback)}


def _coord_mean(hist):
    """배위수 히스토그램 {배위수: 개수} → 평균. 비면 None (0.0 으로 그리지 않는다)."""
    if not hist:
        return None
    n = sum(hist.values())
    return (sum(int(k) * v for k, v in hist.items()) / n) if n else None


def _gb2_frames(run, want, log=print):
    """봉인된 t_ps 프레임만 뽑는다. 색인 대응은 frame_index_map 이 검증한다."""
    run = pathlib.Path(run)
    idx, n_traj = frame_index_map(run / "traj.xyz", run / "thermo.csv")
    missing = [w for w in want if w not in idx]
    if missing:
        raise ValueError(f"⛔ {run}: 봉인된 프레임 중 traj 에 없는 것 {missing} — "
                         f"다른 프레임으로 **대체하지 않는다** (카드 §6 무효 조건)")
    from ase.io import iread
    wanted = {idx[w]: w for w in want}
    out = {}
    for i, at in enumerate(iread(str(run / "traj.xyz"), index=":", format="extxyz")):
        if i in wanted:
            out[wanted[i]] = (list(at.get_chemical_symbols()),
                              np.asarray(at.get_positions(), float),
                              np.asarray(at.get_cell(), float))
        if len(out) == len(want):
            break
    log(f"  {run.name}: traj {n_traj} 프레임 → 봉인 {len(out)} 프레임 회수")
    return out


def gb2_compare(run_small, run_big, card=GB2_CARD, frame_card=None, log=print):
    """G-B2 — 소셀과 400 원자의 **같은 t_ps 프레임**에서 국소환경이 겹치는가. 새 계산 0.

    판정 규칙 (결과 보기 전에 선언 · 2026-09-18)
      · 같은 t_ps 끼리 **짝지어** 재고, 10 짝의 **최댓값**으로 판정한다.
        담금질 속도가 같아 같은 t_ps 는 같은 온도다 — 융체는 융체와, 유리는 유리와 비교한다.
        (프레임을 뭉쳐 평균내면 융체와 유리가 섞여 봉우리가 뭉개진다.)
      · 평균차·풀링 g(r) 도 **같이 찍지만 판정에 쓰지 않는다** — 최댓값 이탈이 통계잡음인지
        사람이 보라고 내는 정보다.

    ⛔ 이 도구가 **못 하는 것**
      · 단일 프레임 g(r) 의 **통계잡음을 문턱과 분리하지 못한다.** 120 원자에서 Li–Cl 은
        48×12 쌍뿐이라 첫 봉우리가 dr 한두 칸 흔들릴 수 있다. 그래서 풀링 값을 같이 낸다.
      · 힘이 같다고 말하지 않는다 — 구조가 겹쳐도 힘이 같다는 보증은 없다 (카드 §4).
      · 전이를 승인하지 않는다. 통과는 **전이의 근거**이고, 판단은 사람이 한다.
      · 밀도를 판정하지 않는다 — 카드가 "밀도는 문턱이 아니다" 로 봉인했다. **보고만** 한다.
    """
    th, card_path = read_gb2_thresholds(card)
    want, fcard = read_frame_card(frame_card or
                                  "db/properties/li2s_layer1_g2_mode_stress_prereg_2026_09_14.json")
    log(f"문턱 카드: {card_path}")
    log(f"  첫봉우리 ≤ {th['gr_first_peak_A']} Å · 배위수평균 ≤ {th['coord_mean']} · "
        f"PS₄ ≤ {th['ps4_pp']} %p · 창 r ≤ {th['r_window_A']} Å")
    log(f"프레임 카드: {fcard} — 봉인 {len(want)} 점 (도구가 고르지 않는다)")
    S = _gb2_frames(run_small, want, log)
    B = _gb2_frames(run_big, want, log)

    rows, acc = [], {}
    for w in want:
        ss, sp, sc = S[w]; bs, bp, bc = B[w]
        i_s, i_b = indicators(ss, sp, sc), indicators(bs, bp, bc)
        g_s = partial_gr(ss, sp, sc, pairs=GB2_PAIRS)
        g_b = partial_gr(bs, bp, bc, pairs=GB2_PAIRS)
        row = {"t_ps": w, "n_small": i_s["n_atoms"], "n_big": i_b["n_atoms"],
               "rho_small": i_s["density_g_cm3"], "rho_big": i_b["density_g_cm3"]}
        # ① 부분 g(r) 첫 봉우리
        row["peaks"] = {}
        for a, b in GB2_PAIRS:
            key = f"g_{a}{b}"
            if key not in g_s or key not in g_b:
                row["peaks"][f"{a}{b}"] = {"d_A": None, "왜": "그 쌍이 한쪽에 없다"}
                continue
            ps = first_peak_A(g_s["r_A"], g_s[key], th["r_window_A"])
            pb = first_peak_A(g_b["r_A"], g_b[key], th["r_window_A"])
            if ps is None or pb is None:
                row["peaks"][f"{a}{b}"] = {"d_A": None, "왜": "봉우리 없음 (무상관)"}
                continue
            d = abs(ps["first_A"] - pb["first_A"])
            row["peaks"][f"{a}{b}"] = {
                "small_A": ps["first_A"], "big_A": pb["first_A"], "d_A": d,
                "⚠_첫봉우리≠최대봉우리": (not ps["first_is_global"]) or (not pb["first_is_global"]),
                "⚠_국소최대없음": ps["no_local_max"] or pb["no_local_max"]}
            acc.setdefault(f"peak_{a}{b}", []).append(d)
        # ② 배위수 평균 (Cl–Li · S–Li)
        row["coord"] = {}
        for name, hk in (("Cl_Li", "Cl_Li_coord_hist"), ("S_Li", "S_Li_coord_hist")):
            ms, mb = _coord_mean(i_s.get(hk)), _coord_mean(i_b.get(hk))
            if ms is None or mb is None:
                row["coord"][name] = {"d": None, "왜": "히스토그램이 비었다"}
                continue
            row["coord"][name] = {"small": ms, "big": mb, "d": abs(ms - mb)}
            acc.setdefault(f"coord_{name}", []).append(abs(ms - mb))
        # ③ PS₄ 보존율
        fs, fb = i_s.get("PS4_fraction"), i_b.get("PS4_fraction")
        if fs is None or fb is None:
            row["PS4"] = {"d_pp": None, "왜": "P 또는 S 가 없다"}
        else:
            row["PS4"] = {"small": fs, "big": fb, "d_pp": abs(fs - fb) * 100.0}
            acc.setdefault("PS4_pp", []).append(abs(fs - fb) * 100.0)
        rows.append(row)
        log(f"  t={w:7.1f} ps  PS₄ Δ{row['PS4'].get('d_pp', float('nan')):5.1f} %p  " +
            "  ".join(f"{k} Δ{(v['d_A'] if v.get('d_A') is not None else float('nan')):.3f}"
                      for k, v in row["peaks"].items()))

    def _worst(keys, lim):
        bad = []
        for k in keys:
            v = acc.get(k)
            if not v:
                bad.append((k, None, "잰 프레임이 없다"))
                continue
            mx = max(v)
            if mx > lim:
                bad.append((k, mx, f"> {lim}"))
        return bad

    peak_keys = [f"peak_{a}{b}" for a, b in GB2_PAIRS]
    fails = (_worst(peak_keys, th["gr_first_peak_A"])
             + _worst(["coord_Cl_Li", "coord_S_Li"], th["coord_mean"])
             + _worst(["PS4_pp"], th["ps4_pp"]))
    #: ⛔ 잰 프레임이 아예 없는 항목은 **통과가 아니다** — 미판정이다.
    unmeasured = [k for k, mx, _ in fails if mx is None]
    verdict = ("미판정" if unmeasured else ("탈락" if fails else "통과"))
    res = {"card": card_path, "frame_card": fcard, "thresholds": th,
           "run_small": str(run_small), "run_big": str(run_big),
           "판정_규칙": "같은 t_ps 짝의 **최댓값**으로 판정 (2026-09-18 선언 · 결과 보기 전)",
           "요약": {k: {"max": max(v), "mean": float(np.mean(v)), "n": len(v)} for k, v in acc.items()},
           "frames": rows, "판정": verdict,
           "실패항목": [{"항목": k, "max": mx, "왜": why} for k, mx, why in fails],
           "⛔_밀도는_문턱이_아니다": "카드 §4 — 국소환경을 요구하고 밀도는 보고만 한다.",
           "⛔_통과가_뜻하지_않는_것": "구조가 겹쳐도 힘이 같다는 보증은 아니다. 전이는 G-B3 통과와 "
                                    "함께, 그리고 **통과 방향으로만** 흐른다 (카드 §5-b)."}
    log(f"\n  판정: **{verdict}**")
    for k, mx, why in fails:
        log(f"    ⛔ {k}: {mx if mx is not None else '미측정'} {why}")
    if verdict == "통과":
        log("  ⛔ 통과는 **전이의 근거**이지 승인이 아니다 — 판단은 사람이 한다 (카드 §5-b).")
    return res


# ───────────────────────── selftest ─────────────────────────
def _selftest():
    ok = bad = 0
    def chk(c, m):
        nonlocal ok, bad
        print(("  ⭕ " if c else "  ⛔ ") + m); ok += c; bad += (not c)
    # ① 무작위 셀
    for sysname, n_exp in (("A", 400), ("B", 400), ("control_li7ps6", 392)):
        sym, pos, cell = build_random_cell(sysname, seed=1)
        comp, n_fu = SYSTEMS[sysname]
        cnt = {e: sym.count(e) for e in set(sym)}
        chk(len(sym) == n_exp and all(cnt.get(k, 0) == v * n_fu for k, v in comp.items()), f"{sysname}: 원자 {n_exp} · 조성 정확")
        D = mic_dists(pos, pos, cell); np.fill_diagonal(D, np.inf)
        P = np.where(np.asarray(sym) == "P")[0]
        ps = np.array([sorted(D[i])[:4] for i in P])
        chk(abs(ps - PS_BOND).max() < 1e-6, f"{sysname}: 모든 P 의 최근접 4 S 가 {PS_BOND} Å (PS₄ 단위)")
        # 단위 밖 최소거리
        unit = -np.ones(len(sym), int)
        for u, i in enumerate(P): unit[i:i+5] = u
        mask = (unit[:, None] != unit[None, :]) | (unit[:, None] < 0)
        heavy = np.array([x != "Li" for x in sym])
        hh = heavy[:, None] & heavy[None, :]
        chk(D[mask & hh].min() >= MIN_DIST_ANION - 1e-9 and D[mask & ~hh].min() >= MIN_DIST - 1e-9,
            f"{sysname}: 단위 밖 최소거리 — 음이온·P 끼리 ≥ {MIN_DIST_ANION} Å · Li 쌍 ≥ {MIN_DIST} Å")
    ind = indicators(sym, pos, cell)
    chk(abs(ind["density_g_cm3"] - 1.2) < 0.02, "밀도 지표가 시작 밀도 1.2 를 재현한다")
    try:
        build_random_cell("A", seed=1, density_g_cm3=6.0, max_tries=3000); ok_d = False
    except SystemExit as e:
        ok_d = "밀도" in str(e)
    chk(ok_d, "⛔음성: 6 g/cm³ 는 못 채우고 멈춘다 (조용히 겹치게 두지 않는다)")
    try:
        build_random_cell("Z", seed=1); ok_z = False
    except SystemExit:
        ok_z = True
    chk(ok_z, "⛔음성: 카드에 없는 계 이름은 거부")
    try:
        schedule(1200, 300, None, 2.0); ok_q = False
    except SystemExit as e:
        ok_q = "quench_rate" in str(e)
    chk(ok_q, "⛔음성: 담금질 속도를 안 주면 시작하지 않는다 (G2)")
    qp, nq = schedule(1200, 300, 1e12, 2.0)
    chk(abs(qp - 900.0) < 1e-9 and nq == 450000, "10¹² K/s · 1200→300 K = 900 ps = 450000 스텝 @ 2 fs")
    # ② 지표 — 합성 구조
    symA, posA, cellA = build_random_cell("A", seed=3)
    iA = indicators(symA, posA, cellA)
    chk(iA["PS4_fraction"] == 1.0 and iA["bridging_S_P2S7_like"] == 0, "무작위 PS₄ 단위 셀: PS₄ 보존율 1.0 · 가교 0")
    first_S = next(i for i, x in enumerate(symA) if x == "S")
    symB = [x for i, x in enumerate(symA) if i != first_S]; posB = np.delete(posA, first_S, axis=0)   # S 하나를 없앤다
    chk(abs(indicators(symB, posB, cellA)["PS4_fraction"] - (1 - 1 / 40)) < 1e-9, "⛔음성: S 하나를 없애면 보존율 39/40")
    a = 5.13; n = 3; rs = []; rsym = []                                    # 암염 LiCl
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for base, el in (((0, 0, 0), "Cl"), ((0.5, 0.5, 0), "Cl"), ((0.5, 0, 0.5), "Cl"), ((0, 0.5, 0.5), "Cl"),
                                 ((0.5, 0, 0), "Li"), ((0, 0.5, 0), "Li"), ((0, 0, 0.5), "Li"), ((0.5, 0.5, 0.5), "Li")):
                    rs.append(((np.array(base) + [i, j, k]) * a).tolist()); rsym.append(el)
    iL = indicators(rsym, np.array(rs), np.eye(3) * a * n)
    chk(iL["Cl_6coord_fraction"] == 1.0 and iL["ClCl_nearest_A"]["in_window_fraction"] == 1.0
        and abs(iL["ClCl_nearest_A"]["median"] - a / math.sqrt(2)) < 1e-6, "암염 LiCl: Cl 6-배위 1.0 · Cl–Cl 3.63 Å 창 분율 1.0")
    a2 = 5.71; qs = []; qsym = []                                          # 반형석 Li₂S
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for base in ((0, 0, 0), (0.5, 0.5, 0), (0.5, 0, 0.5), (0, 0.5, 0.5)):
                    qs.append(((np.array(base) + [i, j, k]) * a2).tolist()); qsym.append("S")
                for base in ((.25, .25, .25), (.75, .75, .75), (.75, .25, .25), (.25, .75, .75),
                             (.25, .75, .25), (.75, .25, .75), (.25, .25, .75), (.75, .75, .25)):
                    qs.append(((np.array(base) + [i, j, k]) * a2).tolist()); qsym.append("Li")
    iQ = indicators(qsym, np.array(qs), np.eye(3) * a2 * 2)
    chk(iQ["S_Li8_fraction_Li2S_like"] == 1.0, "반형석 Li₂S: S 의 Li 8-배위 분율 1.0")
    chk(iA["S_Li8_fraction_Li2S_like"] < 0.2, "무작위 A 셀은 Li₂S 국소질서가 거의 없다 (< 0.2)")
    gr = partial_gr(symA, posA, cellA)
    chk("g_PS" in gr and abs(gr["r_A"][int(np.argmax(gr["g_PS"]))] - PS_BOND) < 0.06, "g_PS 첫 봉우리가 2.05 Å")
    # ③ MD 연기 시험 — fairchem 없이 LJ 로 배선만 (n_fu 2 · 몇 스텝)
    import tempfile
    from ase import Atoms
    from ase.calculators.lj import LennardJones
    symS, posS, cellS = build_random_cell("A", seed=5, n_fu=2, density_g_cm3=0.8)
    at = Atoms(symbols=symS, positions=posS, cell=cellS, pbc=True)
    with tempfile.TemporaryDirectory() as td:
        info = run_melt_quench(at, LennardJones(sigma=2.5, epsilon=0.05, rc=6.0), td, seed=5, T_melt=600, T_final=300,
                               melt_ps=0.02, quench_rate=3e14, hold_ps=0.02, dt_fs=2.0, save_ps=0.004, pre_relax=False, log=lambda *a: None)
        n_frames = open(os.path.join(td, "traj.xyz")).read().count("Lattice=")
        chk(info["n_steps"]["quench"] == 500 and n_frames >= 5, f"LJ 연기: 담금질 500 스텝 · 궤적 {n_frames} 프레임 기록")
        chk(os.path.isfile(os.path.join(td, "final.xyz")) and os.path.isfile(os.path.join(td, "final.vasp"))
            and os.path.isfile(os.path.join(td, "thermo.csv")), "final.xyz + final.vasp + thermo.csv 생성 (xyz·POSCAR 쌍)")
        hdr = open(os.path.join(td, "thermo.csv")).readline().strip().split(",")
        row = open(os.path.join(td, "thermo.csv")).readlines()[1].strip().split(",")
        chk(hdr[-2:] == ["P_GPa", "P_virial_GPa"] and len(row) == len(hdr)
            and row[-1] not in ("", "nan") and row[-2] != row[-1],
            f"thermo.csv 에 총 압력과 virial 을 **둘 다** 기록하고 서로 다르다 ({row[-2]} / {row[-1]} GPa)")
    # ④ 배로스탯 대조 잡 — LJ 결정(fcc)으로 배선만. 같은 BARO 를 쓰는지까지 본다
    from ase.build import bulk
    with tempfile.TemporaryDirectory() as td:
        cr = bulk("Li", "fcc", a=4.3, cubic=True).repeat(2)
        # LJ 파라미터가 Li 격자와 안 맞아 0 K 완화가 20 %대로 움직인다 — 여기선 **배선**만 본다
        res = run_npt_control(cr, LennardJones(sigma=3.0, epsilon=0.20, rc=8.0), td,
                              T_K=50, ps=0.4, dt_fs=2.0, save_ps=0.02, max_relax_dV=0.5,
                              log=lambda *a: None)
        chk(res["baro"] == BARO, "대조 잡이 생산 런과 **같은** BARO 상수를 쓴다 (다르면 아무것도 증명 못 한다)")
        chk(math.isfinite(res["rho_UMA_0K_g_cm3"]) and math.isfinite(res["P_NPT_mean_last_half_GPa"])
            and os.path.isfile(os.path.join(td, "control.json")),
            f"대조 잡 배선: ρ(0K) {res['rho_UMA_0K_g_cm3']:.3f} · P_NPT {res['P_NPT_mean_last_half_GPa']:+.3f} GPa · control.json")
        chk(abs(res["P_UMA_0K_GPa"]) < 0.5, f"가변셀 완화가 0 GPa 근처로 간다 (P_0K {res['P_UMA_0K_GPa']:+.3f} GPa)")
        chk(res["cell_relax"] and "steps=" in res["cell_relax_note"] and res["reference_for_drift"] == "rho_UMA_0K",
            f"0 K 완화 기록이 남는다 ({res['cell_relax_note']})")
        chk(res["cell_wide_enough"] is False and abs(res["min_cell_width_A"] - 8.6) < 0.01,
            f"⛔음성: 폭 {res['min_cell_width_A']:.2f} Å < 9 Å 인 셀을 **조건부**로 표시한다 (조용히 통과 안 시킨다)")
    # ⑤ 면간거리 — 원자 수가 아니라 이게 MIC 기준이다
    cub = np.eye(3) * 10.0
    chk(np.allclose(cell_widths_A(cub), 10.0), "입방 셀 면간거리 = 변 길이")
    prim = np.array([[0., 2., 2.], [2., 0., 2.], [2., 2., 0.]])          # fcc primitive (a=4)
    wp = cell_widths_A(prim)
    chk(abs(wp.min() - 4.0 / math.sqrt(3)) < 1e-9,
        f"fcc primitive(a=4): 벡터 길이 2.83 인데 폭은 a/√3 = {wp.min():.3f} Å — 원자 수로는 안 보이는 값")
    r = auto_repeat(prim, 9.0)
    chk(cell_widths_A((np.diag(r) @ prim)).min() >= 9.0,
        f"auto_repeat 가 폭 문턱을 채운다 ×{r} → {cell_widths_A((np.diag(r) @ prim)).min():.2f} Å")
    # ⛔음성: 0 K 완화가 부피를 많이 바꾸면 멈춘다 (그만큼 움직이면 대조가 아니다)
    with tempfile.TemporaryDirectory() as td:
        cr2 = bulk("Li", "fcc", a=3.2, cubic=True).repeat(2)      # 일부러 압축해 둔 격자
        try:
            run_npt_control(cr2, LennardJones(sigma=3.0, epsilon=0.20, rc=8.0), td,
                            T_K=50, ps=0.2, dt_fs=2.0, save_ps=0.02, max_relax_dV=0.02,
                            log=lambda *a: None)
            g = False
        except SystemExit as e:
            g = "대조가 아니다" in str(e)
        chk(g, "⛔음성: 0 K 완화 부피변화가 허용 밖이면 조용히 진행하지 않고 멈춘다")
    # 0 K 완화를 건너뛰면 기준이 파일 밀도로 바뀐다
    with tempfile.TemporaryDirectory() as td:
        cr3 = bulk("Li", "fcc", a=4.3, cubic=True).repeat(2)
        r3 = run_npt_control(cr3, LennardJones(sigma=3.0, epsilon=0.20, rc=8.0), td,
                             T_K=50, ps=0.2, dt_fs=2.0, save_ps=0.02, cell_relax=False, log=lambda *a: None)
        chk(r3["reference_for_drift"] == "rho_file" and r3["rho_UMA_0K_g_cm3"] is None
            and r3["UMA_vs_file"] is None,
            "--control_no_cellrelax: 기준이 파일 밀도로 바뀌고 0 K 항목은 None (0 으로 안 채운다)")
    # ⛔음성: 압력을 못 주는 계산기는 0 이 아니라 NaN
    class _NoStress(LennardJones):
        implemented_properties = ["energy", "forces"]
        def get_stress(self, atoms=None):
            raise RuntimeError("stress 없음")
    at2 = bulk("Li", "fcc", a=4.3, cubic=True); at2.calc = _NoStress()
    chk(math.isnan(pressure_GPa(at2)), "⛔음성: 응력을 못 주면 NaN — 0 GPa 로 조용히 적지 않는다")
    # ⑥ 운동 항 — 배로스탯이 보는 압력은 virial 이 아니다 (2026-09-12 오독)
    from ase.md.velocitydistribution import MaxwellBoltzmannDistribution as _MB
    hot = bulk("Li", "fcc", a=4.3, cubic=True).repeat(3)
    hot.calc = LennardJones(sigma=3.0, epsilon=0.2, rc=8.0)
    _MB(hot, temperature_K=300)
    _v, _t = pressure_GPa(hot, include_ideal_gas=False), pressure_GPa(hot)
    _kin = 2.0 / 3.0 * hot.get_kinetic_energy() / hot.get_volume() * EV_A3_TO_GPA
    chk(abs((_t - _v) - _kin) < 1e-9 and _kin > 0.05,
        f"총 압력 − virial = NkT/V ({_kin:+.4f} GPa) — 이걸 빼먹으면 0 GPa 목표가 −0.3 으로 보인다")
    cold = bulk("Li", "fcc", a=4.3, cubic=True).repeat(2)
    cold.calc = LennardJones(sigma=3.0, epsilon=0.2, rc=8.0)
    chk(abs(pressure_GPa(cold) - pressure_GPa(cold, include_ideal_gas=False)) < 1e-12,
        "속도 0 이면 두 값이 같다 — 차이는 순전히 운동 항이다")
    # ⑦ NPT MSD — 셀이 숨쉬는 것을 확산으로 읽지 않는지 (이게 핵심 음성시험)
    rng = np.random.default_rng(7)
    N, T = 40, 60
    f0 = rng.uniform(0, 1, (N, 3))
    L = np.linspace(20.0, 18.0, T)                       # 셀이 10 % 수축한다
    cells_b = np.array([np.eye(3) * x for x in L])
    pos_b = np.array([f0 @ cells_b[i] for i in range(T)])  # 분수좌표 고정 = 강체
    symb = ["P"] * N
    _t, m_b = npt_msd(symb, pos_b, cells_b, 1.0)
    naive = ((pos_b - pos_b[0]) ** 2).sum(-1).mean(-1).max()
    chk(m_b["P"].max() < 1e-16 < naive and naive > 1.0,
        f"⛔음성: 셀 10 % 수축 + 분수좌표 고정 → MSD {m_b['P'].max():.2e} Å² (실공간 순진계산은 {naive:.1f} Å²)")
    # 전체 병진(드리프트)도 확산이 아니다
    pos_d = pos_b + (np.arange(T)[:, None, None] * np.array([0.3, 0.0, 0.0]))
    _t, m_d = npt_msd(symb, pos_d, cells_b, 1.0)
    chk(m_d["P"].max() < 1e-12, f"⛔음성: 전체 병진 {0.3*T:.0f} Å 를 확산으로 읽지 않는다 ({m_d['P'].max():.2e} Å²)")
    # 자유절편 맞춤이 D 를 되찾는다
    tt = np.arange(0, 101.0, 1.0); Dtrue = 2.5e-5
    D_hat, c_hat = fit_D(tt, 6 * (Dtrue * 1e4) * tt + 3.0, 50.0, 100.0)
    chk(abs(D_hat / Dtrue - 1) < 1e-9 and abs(c_hat - 3.0) < 1e-6,
        f"fit_D 가 D={Dtrue:.1e} 와 절편 3.0 을 되찾는다 (D̂ {D_hat:.3e} · ĉ {c_hat:.3f})")
    # 실제로 움직이면 잡아낸다 — 한 원소만 무작위걷기
    step = 0.25
    walk = np.cumsum(rng.normal(0, step, (T, N, 3)), axis=0)
    pos_w = pos_b + walk
    _t, m_w = npt_msd(symb, pos_w, cells_b, 1.0)
    chk(m_w["P"][-1] > 3.0, f"움직이는 골격은 잡아낸다 (MSD {m_w['P'][-1]:.2f} Å²)")
    # ⑧ --gate_check: 기록 ↔ 실행 ↔ 게이트 (2026-09-14)
    import tempfile, inspect
    def _mkrun(d, plan, rows):
        d = pathlib.Path(d); d.mkdir(parents=True, exist_ok=True)
        (d / "plan.json").write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        with open(d / "thermo.csv", "w") as f:
            f.write("t_ps,T_K,T_set_K,density_g_cm3,volume_A3,E_pot_eV,P_GPa,P_virial_GPa\n")
            for r in rows:
                f.write(",".join(f"{x:.4f}" for x in r) + "\n")
        return d
    def _rows(rho_tail, p_tail):
        out = []
        for i in range(100):                      # 앞 50 프레임은 **일부러 거칠게** 둔다 (창 시험)
            calm = i >= 50
            out.append((float(i), 300.0 if calm else 1200.0, 300.0 if calm else 1200.0,
                        rho_tail if calm else 1.2000, 8000.0, -1000.0,
                        (p_tail + 0.02 * ((-1) ** i)) if calm else 5.0,
                        0.0))
        return out
    sym_A, _pos, _cell = build_random_cell("A", seed=1)
    plan_ok = build_plan("A", 1, sym_A, 1.2, 1200.0, 300.0, 100.0, 1e12, 900.0, 50.0, 2.0, 1.0)
    gi = plan_ok.get("게이트_입력", {})       # ⛔ 필드가 사라지면 **빨간불**이지 예외가 아니다
    chk(gi.get("ensemble") == "NPT" and gi.get("target_pressure_GPa") == 0.0,
        "build_plan 이 앙상블·목표압력을 plan 에 **기록**한다 (G4 가 읽을 값)")
    src = inspect.getsource(run_melt_quench)
    chk("NPTBerendsen" in src and "pressure_au=0.0" in src
        and ENSEMBLE["barostat"] == "Berendsen" and ENSEMBLE["target_pressure_GPa"] == 0.0,
        "선언(ENSEMBLE) 이 실행 경로(NPTBerendsen · pressure_au=0.0)와 같은 것을 말한다")
    c0, lo0, hi0 = read_band()
    chk(abs(c0 - 1.91347) < 1e-4 and abs(lo0 / c0 - 0.85) < 1e-4 and abs(hi0 / c0 - 1.15) < 1e-4,
        f"read_band 가 카드에서 중심 {c0:.5f} · ±15 % 밴드를 읽는다 (도구가 숫자를 안 갖는다)")
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        r = gate_check(_mkrun(td / "good", plan_ok, _rows(1.9000, 0.00)), win_ps=10.0, log=lambda *a: None)
        chk(r["record_has_gate_input"] and r["pressure_ok"] and r["in_band"] and not r["G4_fires"],
            "정상 런: 기록 있음 · ⟨P⟩≈0 · 밴드 안 → G4 침묵")
        chk(abs(r["P_mean_GPa"]) < 0.05,
            f"⛔음성: 창이 **마지막 {10:.0f} ps 만** 본다 — 앞 50 ps 의 P=5 GPa 가 안 섞인다 (⟨P⟩ {r['P_mean_GPa']:+.3f})")
        plan_old = {k: v for k, v in plan_ok.items() if k != "게이트_입력"}
        r2 = gate_check(_mkrun(td / "old", plan_old, _rows(1.9000, 0.00)), win_ps=10.0, log=lambda *a: None)
        chk(r2["record_has_gate_input"] is False and "역추적" in r2["출처"],
            "⛔음성: 게이트_입력 없는 옛 plan 을 **기록없음** 으로 잡고 역추적이라고 이름 붙인다")
        r3 = gate_check(_mkrun(td / "poff", plan_ok, _rows(1.9000, 0.50)), win_ps=10.0, log=lambda *a: None)
        chk(not r3["pressure_ok"], f"⛔음성: ⟨P⟩ {r3['P_mean_GPa']:+.2f} GPa 가 목표 0 에서 벗어난 것을 잡는다")
        r4 = gate_check(_mkrun(td / "thin", plan_ok, _rows(1.5717, 0.00)), win_ps=10.0, log=lambda *a: None)
        chk(r4["G4_fires"] and abs(r4["dev_pct_vs_center"] + 17.86) < 0.02,
            f"⛔음성: 밴드 밖 밀도에 G4 가 발화한다 ({r4['dev_pct_vs_center']:+.2f} %)")
        bad_card = td / "nocard.json"
        bad_card.write_text(json.dumps({"1_바꾸는_것": {}}, ensure_ascii=False), encoding="utf-8")
        try:
            read_band(bad_card); hit = False
        except KeyError:
            hit = True
        chk(hit, "⛔음성: 밴드 절이 없는 카드에서 기본값으로 때우지 않고 죽는다")
        empty = td / "empty"; empty.mkdir()
        (empty / "thermo.csv").write_text("t_ps,T_K\n", encoding="utf-8")
        try:
            read_thermo(empty / "thermo.csv"); hit2 = False
        except ValueError:
            hit2 = True
        chk(hit2, "⛔음성: 자료 줄 없는 thermo.csv 를 빈 배열로 넘기지 않는다")
    # ⑨ 회신 BR 이행: 유지 구간 블록 추세 · 통계 라벨 · G4 는 경보 (2026-09-14)
    def _rows_hold(rho_start, rho_end, n_hold=60):
        """melt(T_set 1200) → 램프 → hold(T_set 300). hold 동안 ρ 가 선형으로 rho_start→rho_end."""
        out = []
        for i in range(20):                              # melt
            out.append((float(i), 1200.0, 1200.0, 1.2000, 8000.0, -1000.0, 5.0, 0.0))
        for i in range(20):                              # 담금질 램프 (마지막 프레임이 T_set=300 이다)
            Tset = 1200.0 - (1200.0 - 300.0) * (i + 1) / 20.0
            out.append((float(20 + i), Tset, Tset, 1.4000 + (rho_start - 1.4000) * (i + 1) / 20.0,
                        8000.0, -1000.0, 1.0, 0.0))
        for i in range(n_hold):                          # hold
            f = i / max(1, n_hold - 1)
            out.append((float(40 + i), 300.0, 300.0, rho_start + (rho_end - rho_start) * f,
                        8000.0, -1000.0, 0.01 * ((-1) ** i), 0.0))
        return out
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        flat = gate_check(_mkrun(td / "flat", plan_ok, _rows_hold(1.9000, 1.9000)),
                          win_ps=10.0, n_blocks=5, log=lambda *a: None)
        ht = flat["hold_trend"]
        chk(ht["hold_from_ps"] == 39.0 and ht["n_frames"] == 61 and ht["n_blocks"] == 5,
            f"유지 구간을 담금질 램프와 갈라 잡는다 — 램프의 **마지막 프레임(T_set 이 이미 300)**을 포함한다 "
            f"({ht['hold_from_ps']:.0f}–{ht['hold_to_ps']:.0f} ps · {ht['n_frames']} 표본)")
        chk(abs(ht["rho_drift_pct_over_hold"]) < 1e-9 and abs(ht["block_rho_spread_pct"]) < 1e-9,
            "표류 없는 유지 구간은 표류 0 으로 나온다")
        drift = gate_check(_mkrun(td / "drift", plan_ok, _rows_hold(1.9000, 1.8620)),
                           win_ps=10.0, n_blocks=5, log=lambda *a: None)
        hd = drift["hold_trend"]
        chk(abs(hd["rho_drift_pct_over_hold"] + 2.0) < 0.15 and hd["rho_drift_pct_over_hold"] < -1.0,
            f"⛔음성: 유지 전체에 걸친 −2 % ρ 표류를 잡아낸다 ({hd['rho_drift_pct_over_hold']:+.3f} %)")
        chk(drift["rho_flat_pct"] < abs(hd["rho_drift_pct_over_hold"]) / 3.0,
            f"⛔음성: **10 ps 창이 표류를 축소해 보여준다** (창 범위/평균 {drift['rho_flat_pct']:.3f} % vs "
            f"유지 전체 {hd['rho_drift_pct_over_hold']:+.2f} %, {abs(hd['rho_drift_pct_over_hold'])/drift['rho_flat_pct']:.1f}배) "
            f"— 창만 보면 '평탄' 으로 오독한다")
        chk(hd["blocks"][0]["rho_mean"] > hd["blocks"][-1]["rho_mean"],
            "블록 평균이 표류 방향을 보여준다 (첫 블록 > 마지막 블록)")
        chk(flat["G4_role"] == "alert" and flat["G4_원인_지정"] is None,
            "G4 는 **경보**로 표시되고 원인을 지정하지 않는다 (D-2026-09-14-li2s-layer1-density-alert)")
        chk("확인되지 않았다" in flat["허용_서술"] and "총 수압" in flat["허용_서술"],
            "허용 서술이 '단기 관측 · 이완/이력/압력-부피 정확성 미확인' 을 달고 나간다")
        chk("표준편차" in flat["★_통계의_뜻"]["P_sd_GPa"] and "신뢰구간이 아니" in flat["★_통계의_뜻"]["P_sd_GPa"]
            and "검정한 값이 아니" in flat["★_통계의_뜻"]["rho_flat_pct"],
            "통계 라벨이 결과에 같이 실린다 (sd ≠ 신뢰구간 · 범위 ≠ 평형검정)")
        noTset = td / "noTset"; noTset.mkdir()
        (noTset / "plan.json").write_text(json.dumps(plan_ok, ensure_ascii=False), encoding="utf-8")
        with open(noTset / "thermo.csv", "w") as f:
            f.write("t_ps,T_K,density_g_cm3,volume_A3,E_pot_eV,P_GPa,P_virial_GPa\n")
            for i in range(30):
                f.write(f"{float(i):.4f},300.0,1.9,8000.0,-1000.0,0.0,0.0\n")
        r5 = gate_check(noTset, win_ps=10.0, log=lambda *a: None)
        chk("⛔" in r5["hold_trend"] and "T_set_K" in r5["hold_trend"]["⛔"],
            "⛔음성: T_set_K 없는 thermo 에서 유지 구간을 **추측하지 않고** 없다고 말한다")
    # ⑩ --mode_stress: 봉인된 프레임 표본 · 색인 대조 (2026-09-14, 회신 BR Q4)
    from ase import Atoms as _A
    from ase.io import write as _w
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        want, cpath = read_frame_card("db/properties/li2s_layer1_g2_mode_stress_prereg_2026_09_14.json")
        chk(want == [20.0, 50.0, 80.0, 200.0, 400.0, 700.0, 900.0, 1005.0, 1025.0, 1045.0],
            f"프레임 표본을 **카드에서** 읽는다 ({len(want)}점, 도구가 고르지 않는다)")
        badcard = td / "nocard.json"
        badcard.write_text(json.dumps({"1_프레임_표본_봉인": {}}, ensure_ascii=False), encoding="utf-8")
        try:
            read_frame_card(badcard); hit = False
        except KeyError:
            hit = True
        chk(hit, "⛔음성: t_ps 없는 카드에서 기본 표본을 지어내지 않고 죽는다")
        dupcard = td / "dup.json"
        dupcard.write_text(json.dumps({"1_프레임_표본_봉인": {"t_ps": [10, 10, 20]}}, ensure_ascii=False), encoding="utf-8")
        try:
            read_frame_card(dupcard); hit2 = False
        except ValueError:
            hit2 = True
        chk(hit2, "⛔음성: 중복된 프레임 목록을 거부한다")
        def _mk(n_traj, n_thermo, d):
            d.mkdir(parents=True, exist_ok=True)
            ats = [_A("Li2", positions=[[0, 0, 0], [1.5, 0, 0]], cell=np.eye(3) * 6, pbc=True)
                   for _ in range(n_traj)]
            (d / "traj.xyz").unlink(missing_ok=True)
            for a_ in ats:
                _w(str(d / "traj.xyz"), a_, format="extxyz", append=True)
            with open(d / "thermo.csv", "w") as f:
                f.write("t_ps,T_K,T_set_K,density_g_cm3,volume_A3,E_pot_eV,P_GPa,P_virial_GPa\n")
                for i in range(n_thermo):
                    f.write(f"{float(i):.3f},300.0,300.0,1.9,216.0,-1.0,0.0,0.0\n")
            return d
        good = _mk(6, 6, td / "ok")
        m, n = frame_index_map(good / "traj.xyz", good / "thermo.csv")
        chk(n == 6 and m[3.0] == 3 and m[0.0] == 0,
            f"프레임 수와 thermo 행 수가 맞으면 t_ps ↔ 색인을 만든다 ({n} 프레임)")
        mis = _mk(5, 6, td / "mismatch")
        try:
            frame_index_map(mis / "traj.xyz", mis / "thermo.csv"); hit3 = False
        except ValueError:
            hit3 = True
        chk(hit3, "⛔음성: traj 프레임 수 ≠ thermo 행 수면 **멈춘다** (간격을 추측하지 않는다)")
    # ⑪ --gb2: G-B2 겹침 (2026-09-18) — **음성 경로가 본체다**
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)

        # ⓐ 진짜 카드가 파싱되는가 — 사본을 안 만들기로 했으니 이게 배선의 전부다
        th, cpath = read_gb2_thresholds()
        chk(th == {"gr_first_peak_A": 0.05, "coord_mean": 0.3, "ps4_pp": 10.0, "r_window_A": 5.0},
            f"봉인된 카드 산문에서 G-B2 문턱 넷을 판다 {th}")

        raw = json.loads(pathlib.Path(cpath).read_text(encoding="utf-8"))
        g = raw["4_검증_게이트_결과_보기_전에_정한다"]["G-B2_겹침_🔴_이_카드의_핵심"]
        mang = td / "mangled.json"
        mang.write_text(json.dumps({"4_검증_게이트_결과_보기_전에_정한다": {
            "G-B2_겹침_🔴_이_카드의_핵심": {
                "문턱": g["문턱"].replace("PS₄ 보존율 차이가 **10 %p 이내**", "PS₄ 는 적당히"),
                "왜_r_≤_5_Å": g["왜_r_≤_5_Å"]}}}, ensure_ascii=False), encoding="utf-8")
        try:
            read_gb2_thresholds(mang); hitA = False
        except ValueError:
            hitA = True
        chk(hitA, "⛔음성: 문턱 하나가 산문에서 사라지면 **죽는다** (기본값을 지어내지 않는다)")

        noseg = td / "noseg.json"
        noseg.write_text(json.dumps({"4_검증_게이트_결과_보기_전에_정한다": {}}, ensure_ascii=False), encoding="utf-8")
        try:
            read_gb2_thresholds(noseg); hitB = False
        except KeyError:
            hitB = True
        chk(hitB, "⛔음성: G-B2 절이 없는 카드를 통과시키지 않는다")

        # ⓑ first_peak_A — 없는 것을 0 으로 그리지 않는다
        rr = np.arange(0.025, 8.0, 0.05)
        chk(first_peak_A(rr, np.zeros_like(rr), 5.0) is None,
            "⛔음성: 봉우리가 없으면 None — **0.0 으로 그리지 않는다**")
        gg = np.zeros_like(rr)
        gg[(rr > 2.0) & (rr < 2.1)] = 2.0          # 첫 봉우리 2.05 (낮음)
        gg[(rr > 4.0) & (rr < 4.1)] = 9.0          # 최대 봉우리 4.05
        pk = first_peak_A(rr, gg, 5.0)
        chk(pk is not None and abs(pk["first_A"] - 2.025) < 0.06 and abs(pk["global_A"] - 4.025) < 0.06
            and not pk["first_is_global"],
            "첫 봉우리 ≠ 최대 봉우리를 **구분해서 올린다** (조용히 하나를 고르지 않는다)")

        # ⓒ 합성 궤적 — 지표를 내가 정한 값으로 만든다
        _TET = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)
        _TET = _TET / np.linalg.norm(_TET[0])

        def _fix(scale=1.0, drop_S=False, li_on_cl=3):
            L = 14.0 * scale
            sym, pos = [], []
            for k, c in enumerate([(3.0, 3.0, 3.0), (3.0, 10.0, 10.0), (10.0, 3.0, 10.0)]):
                c = np.array(c, float) * scale
                sym.append("P"); pos.append(c)
                for j, v in enumerate(_TET):
                    r = 4.5 if (drop_S and k == 0 and j == 0) else 2.05
                    sym.append("S"); pos.append(c + v * r * scale)
            for m, cc in enumerate([(10.0, 10.0, 3.0), (7.0, 7.0, 12.0)]):
                cc = np.array(cc, float) * scale
                sym.append("Cl"); pos.append(cc)
                for q in range(li_on_cl):           # Cl 둘레 Li — 배위수를 손으로 정한다
                    ang = 2 * math.pi * q / max(li_on_cl, 1)
                    sym.append("Li")
                    pos.append(cc + np.array([math.cos(ang), math.sin(ang), 0.3]) * 2.5 * scale)
            return sym, np.array(pos, float), np.eye(3) * L

        FRAMES = [10.0, 20.0, 30.0]
        fcard = td / "frames.json"
        fcard.write_text(json.dumps({"1_프레임_표본_봉인": {"t_ps": FRAMES}}, ensure_ascii=False), encoding="utf-8")

        def _run(d, **kw):
            d = pathlib.Path(d); d.mkdir(parents=True, exist_ok=True)
            sym, pos, cell = _fix(**kw)
            (d / "traj.xyz").unlink(missing_ok=True)
            for _ in FRAMES:
                _w(str(d / "traj.xyz"), _A(sym, positions=pos, cell=cell, pbc=True),
                   format="extxyz", append=True)
            with open(d / "thermo.csv", "w") as f:
                f.write("t_ps,T_K,density_g_cm3,volume_A3,E_pot_eV,P_GPa,P_virial_GPa\n")
                for t in FRAMES:
                    f.write(f"{t:.3f},300.0,1.9,{abs(np.linalg.det(cell)):.1f},-1.0,0.0,0.0\n")
            return d

        _q = lambda *a, **k: None
        base = _run(td / "base")
        same = _run(td / "same")
        r_ok = gb2_compare(base, same, card=cpath, frame_card=fcard, log=_q)
        chk(r_ok["판정"] == "통과" and r_ok["요약"]["PS4_pp"]["max"] == 0.0,
            "[양성] 같은 구조 두 벌 → **통과** · 모든 차이 0")

        r_ps4 = gb2_compare(base, _run(td / "dropS", drop_S=True), card=cpath, frame_card=fcard, log=_q)
        chk(r_ps4["판정"] == "탈락" and r_ps4["요약"]["PS4_pp"]["max"] > 10.0,
            f"⛔음성: PS₄ 보존율이 {r_ps4['요약']['PS4_pp']['max']:.0f} %p 벌어지면 막는다")

        r_gr = gb2_compare(base, _run(td / "scaled", scale=1.06), card=cpath, frame_card=fcard, log=_q)
        chk(r_gr["판정"] == "탈락" and r_gr["요약"]["peak_PS"]["max"] > 0.05,
            f"⛔음성: g(r) 첫 봉우리가 {r_gr['요약']['peak_PS']['max']:.3f} Å 밀리면 막는다")

        r_cn = gb2_compare(base, _run(td / "moreLi", li_on_cl=6), card=cpath, frame_card=fcard, log=_q)
        chk(r_cn["판정"] == "탈락" and r_cn["요약"]["coord_Cl_Li"]["max"] > 0.3,
            f"⛔음성: Cl–Li 배위수 평균이 {r_cn['요약']['coord_Cl_Li']['max']:.2f} 벌어지면 막는다")

        badf = td / "badframes.json"
        badf.write_text(json.dumps({"1_프레임_표본_봉인": {"t_ps": [10.0, 999.0]}}, ensure_ascii=False),
                        encoding="utf-8")
        # ⚠ 다른 예외(KeyError 등)를 **통과로도, 죽음으로도** 두지 않는다 — 빨간줄로 만든다.
        #   깨보기 실측 2026-09-18: 가드를 빼면 뒤늦게 KeyError 가 나 selftest 전체가 죽었다.
        #   시험이 죽으면 그 뒤 시험이 안 돌아 — "빨간불 확인" 이 성립하지 않는다.
        hitC = None
        try:
            gb2_compare(base, same, card=cpath, frame_card=badf, log=_q); hitC = "통과시켰다"
        except ValueError:
            hitC = True
        except Exception as e:
            hitC = f"엉뚱한 예외 {type(e).__name__} — 가드가 아니라 뒤늦은 붕괴다"
        chk(hitC is True,
            "⛔음성: 봉인된 프레임이 traj 에 없으면 **대체하지 않고 ValueError 로 죽는다** (카드 §6)"
            + ("" if hitC is True else f"  ← {hitC}"))

        chk(r_ok["판정_규칙"].startswith("같은 t_ps 짝의"),
            "판정 규칙(짝지어 최댓값)을 결과 파일에 **적어서** 내보낸다")

    print(f"selftest: ⭕ {ok} · ⛔ {bad}")
    return 0 if bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description="LPSCl@Li₂S 1층 melt-quench (UMA NPT)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--system", choices=sorted(SYSTEMS), help="A · B · control_li7ps6 (카드 §2)")
    ap.add_argument("--seed", type=int, help="담금질 시드 (G3: ≥ 5개, 호출마다 하나)")
    ap.add_argument("--n_fu", type=int, help="식단위 수 (기본: A 40 · B 50 · control 28)")
    ap.add_argument("--density", type=float, default=1.2, help="시작 밀도 g/cm³ (NPT 가 고친다; 음이온 3 Å 배제라 1.5 도 못 채운다)")
    ap.add_argument("--T_melt", type=float, default=1200.0)
    ap.add_argument("--T_final", type=float, default=300.0)
    ap.add_argument("--melt_ps", type=float, default=100.0)
    ap.add_argument("--quench_rate", type=float, help="K/s — G2 선언값. 기본값 없음 (예: 1e12 → 900 ps)")
    ap.add_argument("--hold_ps", type=float, default=50.0)
    ap.add_argument("--dt_fs", type=float, default=2.0)
    ap.add_argument("--save_ps", type=float, default=1.0)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--turbo", action="store_true", help="fairchem inference_settings='turbo' 시도 (없으면 기본으로 내려가고 기록)")
    ap.add_argument("--out_root", help="출력 루트 → <out_root>/<system>/seed<seed>/")
    ap.add_argument("--pcheck", nargs="+", metavar="STRUCT",
                    help="⭐구조 파일들의 **단일점 압력**을 UMA 로 찍는다 (완화 없음). "
                         "고정 셀 MD 가 어떤 내부 압력에서 돌고 있는지 보는 용도")
    ap.add_argument("--melt_check", metavar="RUN_DIR",
                    help="⭐이미 끝난 런에서 melt 구간 P 골격이 확산했는지 본다 (새 계산 없음)")
    ap.add_argument("--d_melt_cm2_s", type=float, default=1e-6, help="--melt_check 액체 판정 진단 문턱")
    ap.add_argument("--npt_control", metavar="STRUCT",
                    help="⭐배로스탯 대조 잡: 결정 구조 파일(.vasp/.cif/.xyz)을 같은 NPT 배선에 넣어 밀도 유지 확인")
    ap.add_argument("--control_repeat", type=int, default=None,
                    help="--npt_control 셀 반복을 손으로 고정 (기본: --control_min_width 를 채우도록 자동)")
    ap.add_argument("--control_min_width", type=float, default=9.0,
                    help="--npt_control 최소 면간거리 [Å] — 원자 수가 아니라 이 폭이 MIC 기준이다 (기본 9.0)")
    ap.add_argument("--control_ps", type=float, default=20.0, help="--npt_control NPT 길이 [ps]")
    ap.add_argument("--control_no_cellrelax", action="store_true",
                    help="--npt_control 에서 0 K 가변셀 완화를 건너뛴다 (기준이 **파일 밀도**로 바뀐다)")
    ap.add_argument("--control_max_relax_dV", type=float, default=0.10,
                    help="0 K 완화가 부피를 이보다 더 바꾸면 멈춘다 — 그만큼 움직이면 대조가 아니다 (기본 0.10)")
    ap.add_argument("--control_p_tol", type=float, default=0.10,
                    help="배선 통과 문턱 |⟨P_total⟩| [GPa] — **판정은 압력이다** (밀도 drift 는 열팽창)")
    ap.add_argument("--control_tol", type=float, default=0.03, help="--npt_control 통과 문턱 |Δρ/ρ_UMA(0K)|")
    ap.add_argument("--control_out", help="--npt_control 출력 폴더 (기본 <out_root>/npt_control)")
    ap.add_argument("--dry_run", action="store_true", help="셀만 만들고 계획을 찍는다 (UMA 안 부름)")
    ap.add_argument("--gate_check", metavar="RUN_DIR",
                    help="plan.json 의 앙상블 선언 + thermo.csv 대조 + G4 밴드 (판정 아님, 기록 점검)")
    ap.add_argument("--band_card", default=BAND_CARD, help="--gate_check G4 밴드 출처 카드")
    ap.add_argument("--gate_win_ps", type=float, default=10.0, help="--gate_check 평균 창 [ps]")
    ap.add_argument("--mode_stress", metavar="RUN_DIR",
                    help="⭐봉인된 프레임에서 turbo − default 의 응력·힘 차이 (새 MD 0, 회신 BR Q4)")
    ap.add_argument("--frame_card", default="db/properties/li2s_layer1_g2_mode_stress_prereg_2026_09_14.json",
                    help="--mode_stress 프레임 표본 카드 (도구가 프레임을 고르지 않는다)")
    ap.add_argument("--gb2", nargs=2, metavar=("RUN_SMALL", "RUN_BIG"),
                    help="G-B2 겹침 — 소셀 런디렉터리와 400 원자 런디렉터리. 새 계산 0")
    ap.add_argument("--gb2_card", default=GB2_CARD,
                    help="--gb2 문턱 출처 카드 (도구가 문턱을 자체 보관하지 않는다)")
    ap.add_argument("--gb2_out", help="--gb2 결과 JSON 경로 (기본 <RUN_SMALL>/gb2_overlap.json)")
    ap.add_argument("--hold_blocks", type=int, default=5,
                    help="--gate_check 유지 구간을 몇 블록으로 나눠 추세를 볼지 (회신 BR Q3: 제일 싼 첫 단계)")
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if a.gb2:
        r = gb2_compare(a.gb2[0], a.gb2[1], a.gb2_card, a.frame_card)
        out = pathlib.Path(a.gb2_out) if a.gb2_out else pathlib.Path(a.gb2[0]) / "gb2_overlap.json"
        out.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"→ {out}")
        #: 통과 0 · 탈락 2 · 미판정 3 — **미판정을 통과로 내보내지 않는다**
        raise SystemExit({"통과": 0, "탈락": 2}.get(r["판정"], 3))
    if a.mode_stress:
        r = mode_stress(a.mode_stress, a.frame_card, a.device)
        out = pathlib.Path(a.mode_stress) / "mode_stress.json"
        out.write_text(json.dumps({k: v for k, v in r.items()}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"→ {out}")
        return
    if a.gate_check:
        r = gate_check(a.gate_check, a.band_card, a.gate_win_ps, n_blocks=a.hold_blocks)
        (pathlib.Path(a.gate_check) / "gate_check.json").write_text(
            json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
        raise SystemExit(0 if (r["record_has_gate_input"] and r["pressure_ok"]) else 2)
    if a.pcheck:
        from ase.io import read
        calc = make_calc(a.device, a.turbo)
        print(f"UMA {getattr(calc, '_mq_mode', 'default')} · 단일점 (완화 없음) — 우리 MD 셀의 내부 압력")
        for f in a.pcheck:
            at = read(f); at.calc = calc
            w = cell_widths_A(at.get_cell())
            print(f"  {pathlib.Path(f).name:40s} {len(at):4d}원자 ρ {density_g_cm3(at):.3f} g/cm³ "
                  f"폭 {w.min():5.2f} Å  P(virial, 0 K) {pressure_GPa(at, include_ideal_gas=False):+7.3f} GPa")
        print("  ⛔ 이건 **그 셀에서의 압력**이다. 양수면 UMA 가 더 큰 셀을 원한다는 뜻이고, "
              "그 자체가 구조가 틀렸다는 뜻은 아니다 (DFT 로 완화한 셀이면 UMA-DFT 차이다).")
        return
    if a.melt_check:
        res = melt_check(a.melt_check, d_melt_cm2s=a.d_melt_cm2_s)
        (pathlib.Path(a.melt_check) / "melt_check.json").write_text(
            json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        print(json.dumps({k: res[k] for k in ("verdict", "framework_diffused", "fit_window_ps",
                                              "d_melt_threshold_cm2_s")}, ensure_ascii=False))
        print("⭕ 녹았다 — 밀도는 물리다. G4 밴드 쪽을 본다" if res["framework_diffused"]
              else "⛔ 안 녹았다 — 이 담금질의 밀도는 생성기 채움밀도다. melt 조건을 먼저 고친다")
        return
    if a.npt_control:
        if not os.path.isfile(a.npt_control):
            raise SystemExit(f"⛔ 구조 파일이 없다: {a.npt_control}")
        from ase.io import read
        at = read(a.npt_control)
        rep = ((a.control_repeat,) * 3 if a.control_repeat else auto_repeat(at.get_cell(), a.control_min_width))
        at = at.repeat(rep); at.pbc = True
        cout = pathlib.Path(a.control_out or (pathlib.Path(a.out_root or ".") / "npt_control"))
        _w = cell_widths_A(at.get_cell())
        print(f"[대조 잡] {a.npt_control} ×{rep} = {len(at)} 원자 · 면간거리 최소 {_w.min():.2f} Å "
              f"({'자동' if not a.control_repeat else '손지정'}) · {a.T_final:.0f} K · {a.control_ps:.0f} ps → {cout}", flush=True)
        calc = make_calc(a.device, a.turbo)
        res = run_npt_control(at, calc, cout, T_K=a.T_final, ps=a.control_ps, dt_fs=a.dt_fs,
                              tol=a.control_tol, p_tol=a.control_p_tol, min_width_A=a.control_min_width,
                              cell_relax=not a.control_no_cellrelax,
                              max_relax_dV=a.control_max_relax_dV)
        res["repeat"] = list(rep)
        res["uma_inference_mode"] = getattr(calc, "_mq_mode", "default")
        res["structure_file"] = a.npt_control
        (cout / "control.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
        print(json.dumps({k: res[k] for k in ("rho_file_g_cm3", "rho_UMA_0K_g_cm3", "P_UMA_0K_GPa",
                                              "rho_NPT_mean_last_half_g_cm3", "P_NPT_mean_last_half_GPa",
                                              "drift_vs_UMA_0K", "alpha_V_apparent_per_K",
                                              "reference_for_drift", "UMA_vs_file", "P_tol_GPa",
                                              "plumbing_ok", "min_cell_width_A", "cell_wide_enough",
                                              "cell_relax", "cell_relax_note", "PS4_fraction_file")},
                         ensure_ascii=False, indent=1))
        if not res["cell_wide_enough"]:
            print(f"⚠ 셀 폭 {res['min_cell_width_A']:.2f} Å < {a.control_min_width} Å — 이 판정은 조건부다")
        print(f"⭕ 배선 정상 — ⟨P⟩ {res['P_NPT_mean_last_half_GPa']:+.3f} GPa 가 0 을 지킨다"
              if res["plumbing_ok"] else
              f"⛔ 배선 이상 — ⟨P⟩ {res['P_NPT_mean_last_half_GPa']:+.3f} GPa (허용 ±{res['P_tol_GPa']})")
        print(f"   밀도 {res['rho_file_g_cm3']:.3f}(파일) → "
              f"{('%.3f' % res['rho_UMA_0K_g_cm3']) if res['rho_UMA_0K_g_cm3'] else '—'}(0K) → "
              f"{res['rho_NPT_mean_last_half_g_cm3']:.3f}({a.T_final:.0f}K) · "
              f"0K→T 변화 {100*res['drift_vs_UMA_0K']:+.2f} % = **열팽창, 판정 아님**")
        return
    if not (a.system and a.seed is not None and a.out_root):
        ap.error("--system · --seed · --out_root 가 필요하다")
    quench_ps, n_q = schedule(a.T_melt, a.T_final, a.quench_rate, a.dt_fs)
    sym, pos, cell = build_random_cell(a.system, a.seed, a.density, a.n_fu)
    out = pathlib.Path(a.out_root) / a.system / f"seed{a.seed}"; out.mkdir(parents=True, exist_ok=True)
    plan = build_plan(a.system, a.seed, sym, a.density, a.T_melt, a.T_final, a.melt_ps,
                      a.quench_rate, quench_ps, a.hold_ps, a.dt_fs, a.save_ps)
    (out / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1))
    from ase import Atoms
    from ase.io import write
    at = Atoms(symbols=sym, positions=pos, cell=cell, pbc=True)
    write(str(out / "initial.xyz"), at, format="extxyz")
    print(f"[{a.system} seed{a.seed}] {len(sym)} 원자 · 셀 {cell[0,0]:.2f} Å · 담금질 {quench_ps:.0f} ps ({n_q} 스텝) → {out}", flush=True)
    if a.dry_run:
        print("dry_run — 여기서 멈춘다"); return
    calc = make_calc(a.device, a.turbo)
    plan["uma_inference_mode"] = getattr(calc, "_mq_mode", "default")
    (out / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1))
    print(f"UMA inference mode: {plan['uma_inference_mode']}", flush=True)
    info = run_melt_quench(at, calc, out, seed=a.seed, T_melt=a.T_melt, T_final=a.T_final, melt_ps=a.melt_ps,
                           quench_rate=a.quench_rate, hold_ps=a.hold_ps, dt_fs=a.dt_fs, save_ps=a.save_ps)
    ind = indicators(at.get_chemical_symbols(), at.get_positions(), np.asarray(at.get_cell()))
    gr = partial_gr(at.get_chemical_symbols(), at.get_positions(), np.asarray(at.get_cell()))
    write_gr_csv(gr, out / "gr_partials.csv")
    res = {"plan": plan, "run": info, "indicators": ind, "E_final_eV": float(at.get_potential_energy()),
           "files": ["initial.xyz", "traj.xyz", "thermo.csv", "final.xyz", "final.vasp", "gr_partials.csv"],
           "⛔": "지표만 찍었다 — 문턱 대조는 카드 §2 판정_지표. 이 시드 하나로 판정하지 않는다 (G3)."}
    (out / "result.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(json.dumps({"indicators": ind, "wall_min": round(info["wall_min"], 1)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
