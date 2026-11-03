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
  python3 tools/ionic/melt_quench_uma.py --seed_gate <run_dir> [<run_dir> ...]   # 시드 게이트 입력 · 원시/relax 두 판 · md_init_raw.xyz
  python3 tools/ionic/melt_quench_uma.py --melt_window_check <run_dir>   # li2s-2 녹음 판정 (창 안 원점 · 0 통과 · 2 미충족 · 3 미완 · 4 무효)
  python3 tools/ionic/melt_quench_uma.py --stage1_verdict <run_dir> …    # li2s-2 1 단계 시드 판정 (카드 필드 직접 · stage1_verdict.json)
  python3 tools/ionic/melt_quench_uma.py --stage1_summary <out_root>     # li2s-2 1 단계 묶음 판정 · 2 단계 시드 (stage1_summary.json)
    ⭐ 회신 DG (2026-11-03): 시드 판정에 원자료 · 카드 값 · 도구 지문 · 최종 구조 대조 · 첫 시드 녹음 미충족 = closes_system ·
       묶음은 지문을 다시 재고 선언된 시드 전부 판정 끝 · 비용 장부 상한 · 카드 값 검사 (validate_li2s2_values)
    ⭐ 회신 DH (2026-11-03): --run_id (러너가 주는 실행 식별자 → plan.json) · 시드 판정 = 폴더 (계, 시드) · plan · run_id 대조 ·
       판정을 덮어쓰기 전에 이전 판정 전체 · 지문 변화 · 사유를 stage1_verdict_history.jsonl 에 · 묶음은 장부를 판정과 대조
       (ledger_check: 누락 · 음수 · 근거 없음 · run_id 중복 · 다른 시드 = 무효 · 안 끝난 런 = 대기)
  python3 tools/ionic/melt_quench_uma.py --selftest

⚠ final.xyz 는 **relax 본**이다 (④ · plan.json 게이트_입력.final_relax). 담금질 원시는 traj.xyz 마지막 프레임뿐이고,
  `--seed_gate` 가 그것을 md_init_raw.xyz 로 뽑는다. (2026-09-24 — 카드 문구가 반대로 적은 적이 있다)

⭐ 2026-11-03 `--fix_density ρ` (li2s-2 카드 db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json §1b):
  ③ 을 **NVT** 로 바꾼다 — 열욕은 NVTBerendsen 에 같은 taut (BARO taut_fs) · 바로스탯만 없다. melt 첫 --compress_ps 동안
  시작 밀도 → ρ 로 **밀도에 선형으로 등방 압축** (50 스텝마다 셀·좌표를 같이 늘임) 한 뒤 나머지 melt · 담금질 · 유지는 ρ 고정.
  plan.json 게이트_입력 의 앙상블이 NVT 로 내려가고 `--gate_check` 는 압력 대신 **밀도 = ρ** 를 본다 (압력은 기록).
  ⛔ 못 하는 것: 고정 밀도라 UMA 셀에 남는 내부 압력을 없애지 않는다 (thermo.csv P 로 **기록만**) · ρ 가 물리적으로
     맞는지 모른다 (목표 밀도는 카드가 정한다) · 압축 중 겹침을 따로 막지 않는다 (1200 K 액체에서 압축한다 — melt_check 가
     압축 **뒤** 반쪽 창 [melt_ps/2, melt_ps] 에서 골격 확산을 본다) · 옵션을 안 주면 옛 NPT 경로와 바이트까지 같은 동작이다.
"""
from __future__ import annotations
import argparse, datetime, hashlib, json, math, os, pathlib, re, sys, time
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
def ensemble_fixed_density(rho_g_cm3, compress_ps):
    """`--fix_density` 의 앙상블 **선언** — ENSEMBLE 과 같은 자리 (plan.json 게이트_입력) 로 내려간다.
    읽는 곳: `gate_check` (ensemble == "NVT" 면 압력 대신 밀도를 본다)."""
    return {"ensemble": "NVT", "thermostat": "Berendsen", "barostat": None,
            "target_density_g_cm3": float(rho_g_cm3),
            "thermostat_params": {"taut_fs": BARO["taut_fs"]},
            "compress": {"over_ps": float(compress_ps), "kind": "등방 · 밀도에 선형 · melt 첫 구간 · 50 스텝마다"},
            "⛔_엄밀성": "고정 밀도 — 내부 압력은 결과다 (thermo.csv P · 기록만). Berendsen 열욕은 구조 생성용."}


def validate_fix_density(rho_g_cm3, compress_ps, melt_ps):
    """`--fix_density` 입력 검사 — 틀리면 시작하지 않는다 (조용히 고치지 않는다)."""
    if rho_g_cm3 is None:
        return
    if not (rho_g_cm3 > 0 and math.isfinite(rho_g_cm3)):
        raise SystemExit(f"⛔ --fix_density 는 양수여야 한다 (받은 값 {rho_g_cm3})")
    if not (compress_ps > 0 and math.isfinite(compress_ps)):
        raise SystemExit(f"⛔ --compress_ps 는 양수여야 한다 (받은 값 {compress_ps})")
    if compress_ps > melt_ps:
        raise SystemExit(f"⛔ --compress_ps {compress_ps} 가 --melt_ps {melt_ps} 보다 길다 — 압축은 melt 안에서 끝나야 한다")
    if compress_ps > melt_ps / 2.0 + 1e-9:   # 회신 DF Q-DF-8 — 녹음 판정 창 [melt/2, melt] 과 겹치지 않게
        raise SystemExit(f"⛔ --compress_ps {compress_ps} 가 녹음 판정 창 시작 (melt_ps/2 = {melt_ps/2:g} ps) 보다 늦게 끝난다 — "
                         "압축은 판정 창 전에 끝나야 한다")


def scale_to_density(atoms, rho_g_cm3):
    """셀과 좌표를 같이 등방으로 늘여 밀도를 ρ 로 맞춘다 (속도는 그대로). 맞춘 밀도를 돌려준다."""
    s = (density_g_cm3(atoms) / float(rho_g_cm3)) ** (1.0 / 3.0)
    atoms.set_cell(np.asarray(atoms.get_cell()) * s, scale_atoms=True)
    return density_g_cm3(atoms)


FINAL_RELAX = {"kind": "FIRE", "fmax_eV_A": 0.05, "cell": "fixed",
               "⛔": "밀도는 **마지막 NPT 셀**의 값이고 구조 지표는 그 셀을 고정한 완화 구조의 값이다 "
                     "(개정 ③ — '300 K 평형 유리의 평균값' 이 아니다)."}
FINAL_RELAX_NVT = {"kind": "FIRE", "fmax_eV_A": 0.05, "cell": "fixed",
                   "⛔": "밀도는 **고정 밀도 셀** (NVT · 카드 목표 ρ) 의 값이고 구조 지표는 그 셀을 고정한 완화 구조의 값이다 "
                         "('300 K 평형 유리의 평균값' 이 아니다 · 회신 DG P2 — NVT plan 에 'NPT 셀' 이라 적던 것)."}


def final_relax_decl(fix_density=None):
    """plan.json 게이트_입력.final_relax — 앙상블에 맞는 설명 (FIRE 설정은 같다)."""
    return FINAL_RELAX if fix_density is None else FINAL_RELAX_NVT
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
    if plan.get("fix_density_g_cm3") is not None:   # 회신 DF P0 · P2 — 누적 원점 판정 · '밀도는 물리다' 출력이 고정 밀도에 안 맞는다
        raise SystemExit("⛔ 고정 밀도 (--fix_density) 런이다 — 옛 --melt_check (0 ps 누적 원점) 대신 --melt_window_check 를 쓴다")
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


# ───────────────────────── li2s-2 (카드 lpscl_glass_dense_window) — 회신 DF P0 · P1-2 · P1-3 · 회신 DG P1-4 · P1-5 · P1-7 ─────────────────────────
#: ⛔ 2026-11-03 회신 DF P0 — 옛 `melt_check` 는 0 ps 부터 **누적한** 변위로 MSD 를 만들고 회귀 점만 [melt/2, melt] 로 잘랐다.
#:   그래서 압축 · 초기 재배열 때 생긴 변위와 뒤 변위의 교차항이 판정에 남는다 (창 좌표가 같아도 이력만 달라 21 배 · 70 ps 에서
#:   끊긴 궤적도 '창 [50, 100]' 으로 기록). 아래 `melt_window_check` 는 **창 안 프레임만** 읽고 **창 안 시간원점만** 쓴다.
#:   문턱 (1e-6 cm²/s) 은 옛 진단값을 승계한다 — 그 승계는 카드 · 결정에 결과 전에 적었다. 옛 진단 결과는 덮지 않는다.
#: ⛔ 2026-11-03 회신 DG — 판정이 원자료에 안 묶여 있었다: final.xyz 에 5 원자 PS₄ 를 넣어도 통과 · 판정 파일만 남은 폴더도
#:   통과 · 다섯째 시드가 미완이어도 묶음 통과 · 녹음 상태 'unknown' 통과 · plan 밀도 NaN 통과 · 소프트웨어 반쪽 기록 통과 ·
#:   virial 열을 지워도 '압력 기록' · 카드 estimator 이름을 바꿔도 window_mto_v1 실행 · 0 번 프레임의 종 배치만 바꿔도 판정이 바뀜.
#:   아래는 그 구멍을 막는다: 카드 값 검사 (`validate_li2s2_values`) · 비교 전 유한성 (`_same`) · 프레임 종 일치 · 최종 구조 대조
#:   (`final_structure_check`) · 판정에 원자료 지문 (`run_provenance`) · 묶음은 지문을 다시 재고 선언된 시드 **전부** 판정 끝 ·
#:   첫 시드 녹음 미충족은 **그 계를 닫는 사건** (`closes_system`) 으로 판정 파일에 남긴다 (일반 시드 탈락과 가른다 · DG P0-1) ·
#:   비용 장부의 합이 상한을 넘으면 통과로 올리지 않는다 (DG P0-3 의 소비자 쪽).
LI2S2_CARD = "db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json"
MELT_WINDOW_ESTIMATOR = "window_mto_v1"
STAGE1_RC = {"pass": 0, "fail": 2, "incomplete": 3, "invalid": 4}
SUMMARY_RC = {"stage1_pass": 0, "stop_track": 2, "pending": 3, "invalid": 4, "cap_incomplete": 5}
LI2S2_STATUSES = ("pass", "fail", "incomplete", "invalid")
DENSITY_REL_TOL = 1e-4          # 고정 밀도 대조 (gate_check NVT · 최종 구조) — 한 곳에서만 정한다
PROVENANCE_FILES = ("plan.json", "thermo.csv", "traj.xyz", "final.xyz", "result.json")
ATTEMPT_NAME = "stage1_attempt.json"  # 러너가 실행 전에 쓰는 식별 기록 — 보존 폴더도 비용 검사 대상
LEDGER_NAME = "stage1_ledger.json"   # li2s2_stage1_runner.py 가 쓰는 비용 장부 — stage1_summary 가 상한을 여기서 다시 잰다
RUN_ID_RE = re.compile(r"^[0-9a-f]{32}$")   # 회신 DH P0-2 — 러너가 담금질마다 주는 실행 식별자 (plan.json run_id · 장부 run_id)
RETRY_BIND_CODES = {"invalid": ("invalid",), "interrupted": ("interrupted", "abnormal", "resume", "cap")}   # 재시도 확인 STOP 의 code (종류별)
VERDICT_HISTORY = "stage1_verdict_history.jsonl"   # 회신 DH P1-5 — 판정을 덮어쓰기 전 이전 판정 전체 · 지문 변화 · 사유
COST_BASES = ("measured", "upper_bound", "attested_upper_bound")    # 장부 런 비용 근거 — 측정 · 보수 상한 · 사람이 근거를 보고 적은 상한 (재부팅 고아 런 · --attest_cost) —  시작)


def _fin(x):
    """유한한 수인가 — None · NaN · inf · 문자열 · bool 은 아니다."""
    if isinstance(x, bool):
        return False
    try:
        return x is not None and math.isfinite(float(x))
    except (TypeError, ValueError):
        return False


def _same(a, b, rel=1e-9, abs_=0.0):
    """둘 다 유한하고 |a − b| ≤ max(abs_, rel·max(1, |b|)) — NaN · None 은 '다르다' (회신 DG P1-7: NaN 이 비교를 빠져나가던 것)."""
    if not (_fin(a) and _fin(b)):
        return False
    a, b = float(a), float(b)
    return abs(a - b) <= max(float(abs_), float(rel) * max(1.0, abs(b)))


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def values_sha16(v):
    """카드 기계_판독_값의 지문 — 판정이 **어느 카드 값으로** 났는지 묶는다."""
    return hashlib.sha256(json.dumps(v, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]


def driver_sha16():
    return _sha256_file(__file__)[:16]


def run_provenance(run):
    """판정이 기댄 원자료의 지문 (회신 DG P1-4) — 없으면 None 으로 적는다 ('없음' 도 지문이다)."""
    run = pathlib.Path(run)
    return {f: (_sha256_file(run / f) if (run / f).is_file() else None) for f in PROVENANCE_FILES}


def validate_li2s2_values(v):
    """카드 `기계_판독_값` 검사 — 문제 목록 (빈 목록이면 통과). 이 도구가 구현하지 않은 판독량 · 비유한 값 · 꼴 오류를 거부한다."""
    bad = []
    try:
        mw = v["melt_window"]
        if mw.get("estimator") != MELT_WINDOW_ESTIMATOR:
            bad.append(f"melt_window.estimator {mw.get('estimator')!r} ≠ 이 도구가 구현한 {MELT_WINDOW_ESTIMATOR!r}")
        a_, b_ = mw["t_from_frac_of_melt"], mw["t_to_frac_of_melt"]
        if not (_fin(a_) and _fin(b_) and 0.0 <= float(a_) < float(b_) <= 1.0):
            bad.append(f"melt_window 창 비율 [{a_!r}, {b_!r}]")
        lo, hi = mw["lag_fit_ps"]
        if not (_fin(lo) and _fin(hi) and 0.0 < float(lo) < float(hi)):
            bad.append(f"melt_window.lag_fit_ps [{lo!r}, {hi!r}]")
        if not (_fin(mw["D_threshold_cm2_s"]) and float(mw["D_threshold_cm2_s"]) > 0):
            bad.append(f"melt_window.D_threshold_cm2_s {mw['D_threshold_cm2_s']!r}")
        if not isinstance(mw.get("element"), str) or mw["element"] not in MASS:
            bad.append(f"melt_window.element {mw.get('element')!r}")
        sched = v["schedule"]
        for k in ("T_melt_K", "T_final_K", "melt_ps", "quench_rate_K_s", "hold_ps", "dt_fs", "save_ps", "compress_ps", "n_atoms"):
            if not (_fin(sched.get(k)) and float(sched[k]) > 0):
                bad.append(f"schedule.{k} {sched.get(k)!r}")
        if all(_fin(sched.get(k)) for k in ("compress_ps", "melt_ps")) and float(sched["compress_ps"]) > float(sched["melt_ps"]) / 2 + 1e-9:
            bad.append("schedule.compress_ps > melt_ps/2 (판정 창과 겹친다)")
        comp = v.get("composition")
        for s_ in ("A", "B"):
            rho = (v.get("fix_density_g_cm3") or {}).get(s_)
            if not (_fin(rho) and float(rho) > 0):
                bad.append(f"fix_density_g_cm3.{s_} {rho!r}")
            c = (comp or {}).get(s_)
            if (not isinstance(c, dict) or not c or any(e not in MASS or isinstance(n, bool) or not isinstance(n, int) or n <= 0
                                                       for e, n in c.items())
                    or not _fin(sched.get("n_atoms")) or sum(c.values()) != int(sched["n_atoms"])):
                bad.append(f"composition.{s_} {c!r} (원소 · 양의 정수 · 합 = n_atoms)")
        if not isinstance(v.get("uma_inference_mode"), str):
            bad.append(f"uma_inference_mode {v.get('uma_inference_mode')!r}")
        req = v.get("software_required")
        if (not isinstance(req, dict) or not all(isinstance(req.get(k), str) and req.get(k) for k in ("model", "task"))
                or not isinstance(req.get("versions_present"), list) or not req["versions_present"]):
            bad.append(f"software_required {req!r} (model · task · versions_present)")
        cols = v.get("thermo_required_columns")
        if not isinstance(cols, list) or not {"t_ps", "T_set_K", "density_g_cm3", "P_GPa", "P_virial_GPa"} <= set(cols):
            bad.append(f"thermo_required_columns {cols!r} (t_ps · T_set_K · density_g_cm3 · P_GPa · P_virial_GPa 포함)")
        sg = v["seed_gate"]
        if sg.get("version") not in ("relaxed", "raw") or not _fin(sg.get("PS4_fraction_min")) or not _fin(sg.get("min_pair_excl_PS_A_gt")):
            bad.append(f"seed_gate {sg!r}")
        if not (_fin(v["gate_check"].get("win_ps")) and float(v["gate_check"]["win_ps"]) > 0):
            bad.append(f"gate_check.win_ps {v['gate_check'].get('win_ps')!r}")
        seeds = v["seeds"]
        if (not isinstance(seeds, list) or not seeds or any(isinstance(x, bool) or not isinstance(x, int) for x in seeds)
                or len(set(seeds)) != len(seeds) or seeds != sorted(seeds)):
            bad.append(f"seeds {seeds!r} (서로 다른 정수 · 오름차순)")
        need = v["stage1_need_pass"]
        if isinstance(need, bool) or not isinstance(need, int) or not (1 <= need <= len(seeds or [])):
            bad.append(f"stage1_need_pass {need!r}")
        if not isinstance(seeds, list) or not seeds or v.get("first_seed") != seeds[0]:
            bad.append(f"first_seed {v.get('first_seed')!r} ≠ seeds[0] — 첫 시드 녹음 판정의 '첫' 을 카드가 정한다")
        m = v["stage2_machines"]
        if not isinstance(m, list) or len(m) < 2 or not all(isinstance(x, str) and x for x in m):
            bad.append(f"stage2_machines {m!r}")
        cap = v.get("stage1_cap_gpu_h")
        if not (_fin(cap) and float(cap) > 0):
            bad.append(f"stage1_cap_gpu_h {cap!r}")
        rr_ = v.get("retry_reasons")
        if (not isinstance(rr_, dict) or set(rr_) != {"invalid", "interrupted"}
                or not all(isinstance(x, list) and x and all(isinstance(y, str) and y for y in x) for x in rr_.values())):
            bad.append(f"retry_reasons {rr_!r} (invalid · interrupted 각각 허용 사유 목록 — 결과와 무관한 사건만)")
        orr = v.get("outage_reasons")
        if not (isinstance(orr, list) and orr and isinstance(rr_, dict) and set(orr) <= set(rr_.get("interrupted") or [])):
            bad.append(f"outage_reasons {orr!r} (interrupted 사유의 부분집합)")
        ex = v.get("stage1_outage_extra_budget_gpu_h")
        if not (_fin(ex) and float(ex) >= 0):
            bad.append(f"stage1_outage_extra_budget_gpu_h {ex!r}")
        cr = v.get("cap_retry_reasons")
        if not (isinstance(cr, list) and cr and isinstance(rr_, dict) and set(cr) <= set(rr_.get("interrupted") or [])
                and not (set(cr) & set(orr if isinstance(orr, list) else []))):
            bad.append(f"cap_retry_reasons {cr!r} (interrupted 사유의 부분집합 · 정전 사유와 겹치지 않음 — 상한으로 멈춘 런에만)")
        af = v.get("attestation_required_fields")
        if not (isinstance(af, list) and {"event", "time_reference", "uncertainty_h", "derivation", "confirmer", "confirmed_at"} <= set(af)):
            bad.append(f"attestation_required_fields {af!r}")
        mr = v.get("stage1_max_interrupt_retries_per_seed")
        if isinstance(mr, bool) or not isinstance(mr, int) or mr < 0:
            bad.append(f"stage1_max_interrupt_retries_per_seed {mr!r} (0 이상 정수 — 끊긴 런 재시도 한도 · 정전 복구 개정)")
    except (KeyError, TypeError, ValueError, AttributeError) as e:
        bad.append(f"꼴 오류 {type(e).__name__}: {e}")
    return bad


def read_li2s2_values(card=LI2S2_CARD):
    """li2s-2 카드의 `기계_판독_값` — 이 도구는 그 카드의 문턱 · 일정 · 목표 밀도를 **자체 보관하지 않는다**.
    값이 이 도구가 구현한 것과 안 맞으면 (estimator 이름 · 비유한 값 · 빠진 필드) **읽기에서 죽는다** (회신 DG P1-7)."""
    d = json.loads(pathlib.Path(card).read_text(encoding="utf-8"))
    v = d.get("기계_판독_값")
    if not v:
        raise KeyError(f"{card} 에 '기계_판독_값' 이 없다 — 카드 없이 판정하지 않는다")
    bad = validate_li2s2_values(v)
    if bad:
        raise ValueError(f"{card} 기계_판독_값 거부 — " + " · ".join(bad))
    return v


def software_versions(mode):
    """plan.json 에 남길 실행 소프트웨어 (회신 DF Q-DF-6: 기계 이름이 아니라 판 · 체크포인트 · 추론 설정을 고정한다)."""
    from importlib import metadata
    out = {"model": "uma-s-1p1", "task": "omat", "inference": mode}
    for pkg in ("fairchem-core", "torch", "ase"):
        try:
            out[pkg] = metadata.version(pkg)
        except Exception as e:
            out[pkg] = f"?({type(e).__name__})"
    return out


def _leading_frames(traj_path, n_need):
    """traj.xyz 의 앞 n_need 프레임만 읽는다 — 쓰는 중인 파일이면 끝의 반쪽 프레임에서 멈춘다 (멈춘 이유를 돌려준다)."""
    from ase.io import iread
    frames, why = [], None
    try:
        for fr in iread(str(traj_path), index=slice(0, n_need)):
            frames.append(fr)
    except Exception as e:
        why = f"{type(e).__name__}: {e}"
    return frames, why


def window_mto_msd(sym, pos, cells, lags):
    """창 안 프레임들로 원소별 **다중 시간원점** MSD [Å²] — 원점은 창 안에서만 고른다.

    분수좌표 차분 → MIC → 그 프레임 셀로 실공간 증분 → 창 첫 프레임 기준 누적 → 전체 평균 병진 제거 (npt_msd 와 같은 꼴)
    → 지연 k 마다 모든 (j, j+k) 쌍 평균. 창 밖 이력은 들어갈 길이 없다."""
    sym = np.asarray(sym); pos = np.asarray(pos, float); cells = np.asarray(cells, float)
    T, N, _ = pos.shape
    frac = np.einsum("tnj,tjk->tnk", pos, np.linalg.inv(cells))
    df = np.diff(frac, axis=0); df -= np.round(df)
    steps = np.einsum("tnj,tjk->tnk", df, cells[1:])
    disp = np.concatenate([np.zeros((1, N, 3)), np.cumsum(steps, axis=0)])
    disp -= disp.mean(axis=1, keepdims=True)
    out = {}
    for e in sorted(set(sym.tolist())):
        d = disp[:, sym == e]
        out[str(e)] = np.array([((d[k:] - d[:-k]) ** 2).sum(-1).mean() if 0 < k < T else np.nan for k in lags])
    return out


def _species_check(frames, plan, values):
    """프레임마다 원자 수 · 종 순서가 같고, plan · 카드 조성과 맞는가 (회신 DG P1-7: 종을 frames[0] 에서만 가져오던 것).
    문제 목록을 돌려준다 — 이런 파일은 다른 물리 판정을 내릴 것이 아니라 **무효**다."""
    why = []
    if not frames:
        return why
    syms = [tuple(f.get_chemical_symbols()) for f in frames]
    if len(set(syms)) > 1:
        i = next(k for k, x in enumerate(syms) if x != syms[0])
        why.append(f"프레임마다 원자 수 · 종 순서가 다르다 (프레임 0 대 {i})")
    s0 = syms[0]
    comp = {e: s0.count(e) for e in sorted(set(s0))}
    if plan.get("n_atoms") is not None and len(s0) != plan.get("n_atoms"):
        why.append(f"traj 원자 수 {len(s0)} ≠ plan {plan.get('n_atoms')}")
    if plan.get("composition") is not None and comp != plan["composition"]:
        why.append(f"traj 조성 {comp} ≠ plan {plan['composition']}")
    if "composition" in values:
        want = (values.get("composition") or {}).get(plan.get("system"))
        if want is None or comp != want:
            why.append(f"traj 조성 {comp} ≠ 카드 {plan.get('system')} {want}")
    return why


def melt_window_check(run_dir, *, values=None, card=LI2S2_CARD, log=print):
    """⭐ li2s-2 녹음 판정 — 압축 **뒤** 창 [melt_ps·a, melt_ps·b] 안 프레임 · 창 안 시간원점만 쓰는 P 골격 D (회신 DF P0).

    verdict: pass (D_P > 문턱) · fail · incomplete (plan · traj 가 아직 없다 · 창 전체가 없다 · 쓰는 중) ·
             invalid (카드 estimator ≠ 구현 · 고정 밀도 plan 아님 · 압축이 창과 겹침 · 좌표 비유한 · 프레임 종 · 원자 수 불일치).
    ⛔ 못 하는 것: 'pass' 는 '이 밀도 · 온도 · 시간에서 사전 정의한 P 골격 이동 기준을 충족했다' 까지다 — 평형 액체의 인증이
       아니다. 'fail' 은 '1200 K 에서 액체가 없다' 가 아니다 (회신 DF Q-DF-3 문구). 결정화 · 구조는 안 본다.
       겹치는 시간원점들은 독립 표본이 아니다 (회신 DG ①) — D 는 운영 판독량이지 오차막대가 붙은 측정이 아니다."""
    v = values if values is not None else read_li2s2_values(card)
    mw = v["melt_window"]
    run = pathlib.Path(run_dir)
    out = {"kind": "melt_window_check", "estimator": MELT_WINDOW_ESTIMATOR, "estimator_card": mw.get("estimator"), "run": str(run),
           "estimator_def": "창 안 프레임만 · 창 안 시간원점 (다중 원점) · 창 첫 프레임 기준 unwrap · 전체 병진 제거 · "
                            "지연 [lag_fit] 자유절편 선형맞춤 MSD = 6Dτ + c",
           "overlap_ok": None, "coverage_ok": None, "finite_ok": None, "species_ok": None, "window_used_ps": None,
           "per_element": {}, "D_framework_cm2_s": None}
    def done(verdict, msg):
        out["verdict"] = verdict; out["message"] = msg; log(f"  [melt_window] {verdict} — {msg}"); return out
    if mw.get("estimator") != MELT_WINDOW_ESTIMATOR:     # 회신 DG P1-7 — 카드가 다른 판독량을 부르면 이 이름으로 돌리지 않는다
        return done("invalid", f"카드 estimator {mw.get('estimator')!r} ≠ 이 도구가 구현한 {MELT_WINDOW_ESTIMATOR!r}")
    try:                                                  # 회신 DG P0-2 — 담금질 시작 직후에는 plan.json 이 아직 없다
        plan = json.loads((run / "plan.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        return done("incomplete", "plan.json 이 아직 없다 (담금질 시작 직후) — 기다린다")
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return done("incomplete", f"plan.json 을 아직 못 읽는다 ({type(e).__name__} · 쓰는 중일 수 있다) — 기다린다")
    if plan.get("fix_density_g_cm3") is None:
        return done("invalid", "고정 밀도 plan 이 아니다 (fix_density_g_cm3 없음) — 이 판독량은 li2s-2 고정 밀도 런 전용")
    if not (_fin(plan.get("melt_ps")) and _fin(plan.get("save_ps")) and float(plan["save_ps"]) > 0):
        return done("invalid", f"plan 의 melt_ps · save_ps 가 유한한 양수가 아니다 ({plan.get('melt_ps')!r} · {plan.get('save_ps')!r})")
    melt_ps, save_ps = float(plan["melt_ps"]), float(plan["save_ps"])
    t_from, t_to = float(mw["t_from_frac_of_melt"]) * melt_ps, float(mw["t_to_frac_of_melt"]) * melt_ps
    lag_lo, lag_hi = (float(x) for x in mw["lag_fit_ps"])
    comp = float(plan.get("compress_ps")) if _fin(plan.get("compress_ps")) else float("nan")
    thr, el = float(mw["D_threshold_cm2_s"]), str(mw["element"])
    out.update({"window_declared_ps": [t_from, t_to], "lag_fit_ps": [lag_lo, lag_hi], "compress_end_ps": comp,
                "element": el, "D_threshold_cm2_s": thr, "threshold_source": mw.get("threshold_source"),
                "overlap_ok": bool(comp <= t_from + 1e-9)})
    if not out["overlap_ok"]:
        return done("invalid", f"압축 끝 {comp:g} ps 가 판정 창 시작 {t_from:g} ps 보다 늦다 (또는 비유한) — 창이 강제 압축과 겹친다")
    if not (run / "traj.xyz").is_file():
        return done("incomplete", "traj.xyz 가 아직 없다 — 기다린다")
    n_need = int(round(t_to / save_ps)) + 1
    frames, why = _leading_frames(run / "traj.xyz", n_need)
    out["n_frames_read"], out["read_stop"] = len(frames), why
    sp_why = _species_check(frames, plan, v)
    out["species_ok"] = not sp_why
    if sp_why:
        return done("invalid", " · ".join(sp_why))
    times = np.arange(len(frames)) * save_ps
    sel = np.where((times >= t_from - 1e-6) & (times <= t_to + 1e-6))[0]
    if sel.size:
        out["window_used_ps"] = [float(times[sel[0]]), float(times[sel[-1]])]
    out["coverage_ok"] = bool(sel.size >= 2 and times[sel[0]] <= t_from + 1e-6 and times[sel[-1]] >= t_to - 1e-6)
    if not out["coverage_ok"]:
        return done("incomplete", f"창 [{t_from:g}, {t_to:g}] ps 가 다 없다 — 읽은 프레임 {len(frames)} · 쓴 창 {out['window_used_ps']}")
    sym = frames[sel[0]].get_chemical_symbols()            # 종도 **창 안** 프레임에서 (프레임 종 일치는 위에서 봤다)
    pos = np.array([frames[i].get_positions() for i in sel]); cells = np.array([np.asarray(frames[i].get_cell()) for i in sel])
    out["finite_ok"] = bool(np.isfinite(pos).all() and np.isfinite(cells).all())
    if not out["finite_ok"]:
        return done("invalid", "창 안 좌표 · 셀에 유한하지 않은 값이 있다")
    k_lo, k_hi = int(math.ceil(lag_lo / save_ps - 1e-9)), int(math.floor(lag_hi / save_ps + 1e-9))
    lags = list(range(max(1, k_lo), k_hi + 1))
    msd = window_mto_msd(sym, pos, cells, lags)
    tau = np.array(lags) * save_ps
    for e, m in msd.items():
        ok = np.isfinite(m)
        if ok.sum() < 4:
            out["per_element"][e] = {"D_cm2_s": None}; continue
        a, c = np.polyfit(tau[ok], m[ok], 1)
        out["per_element"][e] = {"D_cm2_s": float(a / 6.0 * 1e-4), "intercept_A2": float(c),
                                 "msd_at_lag_hi_A2": float(m[ok][-1])}
    D = out["per_element"].get(el, {}).get("D_cm2_s")
    out["D_framework_cm2_s"] = D
    if D is None or not math.isfinite(D):
        return done("invalid", f"{el} 의 D 를 못 냈다 (지연 점 부족)")
    if D > thr:
        return done("pass", f"이 밀도 · 온도 · 시간에서 사전 정의한 {el} 골격 이동 기준을 충족했다 (D {D:.2e} > {thr:g} cm²/s) — 평형 액체 인증 아님")
    return done("fail", f"이 밀도 · 온도 · 시간에서 사전 정의한 {el} 골격 이동 기준을 충족하지 못했다 (D {D:.2e} ≤ {thr:g} cm²/s) — '액체가 없다' 가 아님")


def final_structure_check(run, plan, values, raw_last=None):
    """⭐ 회신 DG P1-4 — final.xyz 가 **이 런의** 최종 구조인가: 원자 수 · 조성 (카드 · plan) · 종 순서 (traj 마지막 프레임과) ·
    셀 (traj 마지막 셀과 — 고정 셀 FIRE) · 밀도 (카드 목표, 상대 DENSITY_REL_TOL). 문제가 있으면 ok False + 이유.
    ⛔ 못 하는 것: final.xyz 가 '그 traj 에서 FIRE 로 나온 것' 인지까지는 모른다 — 같은 원자 수 · 조성 · 셀의 다른 구조로 바꿔치면
       못 잡는다 (원시와의 변위는 seed_gate 가 기록만 한다). 일관된 전면 위조는 막지 않는다 (회신 DG 도 그 가정은 안 했다)."""
    from ase.io import read
    run = pathlib.Path(run)
    res = {"ok": False, "why": []}
    try:
        fa = read(str(run / "final.xyz"))
    except Exception as e:
        res["why"].append(f"final.xyz 를 못 읽었다 ({type(e).__name__}: {e})")
        return res
    sym = fa.get_chemical_symbols()
    sysname = plan.get("system")
    comp = {e: sym.count(e) for e in sorted(set(sym))}
    rho = density_g_cm3(fa) if all(e in MASS for e in sym) and fa.get_volume() > 0 else float("nan")
    res.update({"n_atoms": len(sym), "composition": comp, "density_g_cm3": rho})
    want_n = values["schedule"]["n_atoms"]
    if not (_same(len(sym), want_n) and _same(len(sym), plan.get("n_atoms"))):
        res["why"].append(f"원자 수 {len(sym)} ≠ 카드 {want_n} · plan {plan.get('n_atoms')}")
    want_comp = (values.get("composition") or {}).get(sysname)
    if want_comp is None or comp != want_comp:
        res["why"].append(f"조성 {comp} ≠ 카드 {sysname} {want_comp}")
    if plan.get("composition") is not None and comp != plan["composition"]:
        res["why"].append(f"조성 {comp} ≠ plan {plan['composition']}")
    tgt = (values.get("fix_density_g_cm3") or {}).get(sysname)
    dev = abs(rho / float(tgt) - 1.0) if (_fin(tgt) and _fin(rho)) else float("nan")
    res["density_rel_dev"] = dev
    if not (dev <= DENSITY_REL_TOL):
        res["why"].append(f"밀도 {rho} ≠ 카드 {tgt} (상대 차 {dev:.1e} > {DENSITY_REL_TOL:g})")
    if raw_last is None:
        res["why"].append("traj 마지막 프레임이 없다 — 종 순서 · 셀을 대조하지 못했다")
    else:
        same_order = list(raw_last.get_chemical_symbols()) == list(sym)
        res["species_order_same_as_traj_last"] = same_order
        if not same_order:
            res["why"].append("종 순서 · 원자 수가 traj 마지막 프레임과 다르다")
        dc = float(np.abs(np.asarray(raw_last.get_cell()) - np.asarray(fa.get_cell())).max())
        res["cell_vs_traj_last_max_A"] = dc
        if not (dc <= 1e-6):
            res["why"].append(f"고정 셀인데 final 셀이 traj 마지막 셀과 {dc:.2e} Å 다르다")
    res["ok"] = not res["why"]
    return res


def combine_stage1(plan, values, gate, melt, seedg, files, checks=None):
    """li2s-2 1 단계 시드 판정 — 카드가 요구하는 필드를 **직접** 읽는다 (회신 DF P1-2: 종료코드를 합쳐 판정하지 않는다).

    입력은 이미 계산된 dict (plan.json · gate_check · melt_window_check · seed_gate · 파일 존재 · checks) — 순수 함수라 시험이 가볍다.
    checks (회신 DG): thermo_header · traj_frames · final_structure · seed_gate_error — 있으면 본다.
    우선순위: invalid (카드와 다른 실행 · 기록 꼴 · 원자료 불일치) > [첫 시드 녹음 미충족 = 그 계를 닫는 사건] > incomplete > fail > pass.
    ⭐ 회신 DG P0-1 — 계의 첫 시드 (카드 first_seed) 녹음 미충족은 일반 시드 탈락이 아니라 **그 계를 닫는 사건**이다:
       closes_system True · 상태 fail (러너가 멈춰서 일정이 미완이어도). 다른 invalid 이유가 있으면 닫지 않고 invalid (카드 런이 아니다)."""
    checks = checks or {}
    reasons = {"invalid": [], "incomplete": [], "fail": []}
    sched, sysname = values["schedule"], plan.get("system")
    tgt = (values.get("fix_density_g_cm3") or {}).get(sysname)
    if not _same(plan.get("fix_density_g_cm3"), tgt, rel=0.0, abs_=1e-6):
        reasons["invalid"].append(f"고정 밀도 {plan.get('fix_density_g_cm3')!r} ≠ 카드 {tgt!r} ({sysname}) — 비유한 값도 '다름'")
    for k, want in sched.items():
        if not _same(plan.get(k), want):
            reasons["invalid"].append(f"일정 {k} {plan.get(k)!r} ≠ 카드 {want!r}")
    want_comp = (values.get("composition") or {}).get(sysname)
    if want_comp is None or plan.get("composition") != want_comp:
        reasons["invalid"].append(f"조성 plan {plan.get('composition')} ≠ 카드 {sysname} {want_comp}")
    sw = plan.get("software") or {}
    req = values.get("software_required") or {}
    sw_bad = [] if req else ["카드 software_required 없음"]
    if sw.get("inference") != values.get("uma_inference_mode"):
        sw_bad.append(f"inference {sw.get('inference')!r} ≠ {values.get('uma_inference_mode')!r}")
    for k in ("model", "task"):
        if sw.get(k) != req.get(k):
            sw_bad.append(f"{k} {sw.get(k)!r} ≠ {req.get(k)!r}")
    for k in req.get("versions_present") or []:
        x = sw.get(k)
        if not isinstance(x, str) or not x or x.startswith("?"):
            sw_bad.append(f"{k} 판 {x!r}")
    if sw_bad:
        reasons["invalid"].append("소프트웨어 기록이 카드 요구와 다르다 — " + " · ".join(sw_bad))
    for f, ok in files.items():
        if not ok:
            reasons["incomplete"].append(f"{f} 없음")
    th = checks.get("thermo_header")
    if th is not None and not th.get("ok"):
        reasons["invalid"].append(f"thermo.csv 열 {th.get('missing')} 없음 — 이 드라이버가 쓰는 꼴이 아니다")
    sched_done = bool(gate and gate.get("schedule_complete"))
    if gate is None:
        if th is None or th.get("ok"):
            reasons["incomplete"].append("gate_check 없음")
    elif gate.get("error"):
        reasons["incomplete"].append(f"gate_check 오류 ({gate['error']}) — 쓰는 중일 수 있다")
    else:
        if gate.get("thermo_columns_ok") is False:
            reasons["invalid"].append(f"thermo 압력 열이 다 있지 않다 ({gate.get('pressure_columns')}) — 총압 · virial 둘 다 있어야 한다")
        if not _same(gate.get("target_density_g_cm3"), tgt, rel=0.0, abs_=1e-6):
            reasons["invalid"].append(f"gate_check 목표 밀도 {gate.get('target_density_g_cm3')!r} ≠ 카드 {tgt!r}")
        if not sched_done:
            reasons["incomplete"].append("계획한 일정 (melt · 담금질 · 유지) 을 다 돌지 않았다")
        for k, why in (("window_in_hold", "판정 창이 300 K 유지 구간 안이 아니다"), ("density_ok", "밀도 ≠ 목표"),
                       ("pressure_recorded", "압력 기록이 없다 (NaN · 빈 칸) — '기록했다' 와 '없다' 를 가른다")):
            if sched_done and not gate.get(k):
                reasons["fail"].append(why)
    mv = None if melt is None else melt.get("verdict")
    if mv is None or mv == "incomplete":
        reasons["incomplete"].append(f"녹음 판정 {mv}")
    elif mv == "invalid":
        reasons["invalid"].append(f"녹음 판정 invalid — {melt.get('message')}")
    elif mv == "fail":
        reasons["fail"].append(melt.get("message"))
    elif mv != "pass":                                     # 회신 DG P1-7 — 모르는 상태를 통과로 떨어뜨리지 않는다
        reasons["invalid"].append(f"녹음 판정 상태 {mv!r} 를 모른다 (허용: {', '.join(LI2S2_STATUSES)})")
    if checks.get("seed_gate_error"):
        reasons["invalid"].append(f"시드 게이트를 못 냈다 — {checks['seed_gate_error']}")
    sg, rel = values["seed_gate"], (seedg or {}).get(values["seed_gate"]["version"])
    if not rel:
        if not checks.get("seed_gate_error"):
            reasons["incomplete"].append(f"시드 게이트 {values['seed_gate']['version']} 판 없음")
    else:
        if not (_fin(rel.get("PS4_fraction")) and float(rel["PS4_fraction"]) >= float(sg["PS4_fraction_min"]) - 1e-12):
            reasons["fail"].append(f"PS₄ 보존율 {rel.get('PS4_fraction')} < {sg['PS4_fraction_min']}")
        if not (_fin(rel.get("min_pair_excl_PS_A")) and float(rel["min_pair_excl_PS_A"]) > float(sg["min_pair_excl_PS_A_gt"])):
            reasons["fail"].append(f"최단 원자간 (P–S 제외) {rel.get('min_pair_excl_PS_A')} ≤ {sg['min_pair_excl_PS_A_gt']} Å")
    tf = checks.get("traj_frames")
    if tf is not None:
        n, want = tf.get("n"), tf.get("expected")
        if n is None:
            reasons["invalid"].append("traj 프레임 수를 못 셌다 (줄 수가 원자수+2 의 배수가 아니다)")
        elif want is not None and n != want:
            (reasons["invalid"] if (sched_done or n > want) else reasons["incomplete"]).append(
                f"traj 프레임 {n} ≠ 계획 {want}" + (" — thermo 는 끝났는데 traj 가 다르다" if sched_done else ""))
    fs = checks.get("final_structure")
    if fs is not None and not fs.get("ok"):
        reasons["invalid"].append("최종 구조가 이 런과 안 맞는다 — " + " · ".join(fs.get("why") or ["?"]))
    idc = checks.get("identity")
    if idc is not None and not idc.get("ok"):
        reasons["invalid"].append("실행 식별이 안 맞는다 — " + " · ".join(idc.get("why") or ["?"]))
    first = values.get("first_seed")
    closes = bool(first is not None and plan.get("seed") == first and mv == "fail" and not reasons["invalid"])
    if reasons["invalid"]:
        status = "invalid"
    elif closes:
        status = "fail"
    else:
        status = next((s for s in ("incomplete", "fail") if reasons[s]), "pass")
    return {"status": status, "reasons": reasons, "system": sysname, "seed": plan.get("seed"), "software": sw,
            "run_id": plan.get("run_id"), "closes_system": closes,
            "closing_event": ("계의 첫 시드 녹음 판정 미충족 — 그 계를 닫는다 (카드 S1 ② · 일반 시드 탈락과 다르다)" if closes else None)}


def folder_identity(run_dir):
    """<out_root>/<계>/seed<S>/ 의 (계, 시드) — 꼴이 아니면 (None, None)."""
    run = pathlib.Path(run_dir)
    m = re.fullmatch(r"seed(\d+)", run.name)
    return (run.parent.name, int(m.group(1))) if m else (None, None)


def identity_check(run_dir, plan):
    """⭐ 회신 DH P0-2 — 폴더 (계, 시드) = plan (계, 시드) · plan 에 러너의 실행 식별자 (run_id · 32 hex) 가 있다.
    폴더를 통째로 복사하면 (A11 → A12) plan 의 시드가 폴더와 달라 여기서 무효가 된다 · plan 시드까지 고치면 run_id 가 겹치거나
    장부의 그 run_id 런이 다른 시드라서 묶음 (stage1_summary) 에서 무효가 된다."""
    fs, fsd = folder_identity(run_dir)
    why = []
    if fs is None:
        why.append(f"폴더 이름 {pathlib.Path(run_dir).name!r} 이 seed<번호> 꼴이 아니다")
    elif (plan.get("system"), plan.get("seed")) != (fs, fsd):
        why.append(f"폴더 ({fs}, {fsd}) ≠ plan ({plan.get('system')}, {plan.get('seed')}) — 다른 시드의 폴더를 옮겨 왔거나 잘못 회수했다")
    rid = plan.get("run_id")
    if not (isinstance(rid, str) and RUN_ID_RE.match(rid)):
        why.append(f"plan.json 에 실행 식별자 run_id 가 없다 ({rid!r}) — 러너 밖에서 돌린 담금질은 장부에 안 잡힌다")
    return {"folder": [fs, fsd], "plan": [plan.get("system"), plan.get("seed")], "run_id": rid, "ok": not why, "why": why}


def _append_history(run, prev, res, reason):
    """⭐ 회신 DH P1-5 — 판정을 덮어쓰기 전에 이전 판정 **전체** 와 지문 변화 · 사유를 한 줄 덧붙인다 (지우지 않는다)."""
    pp, npv = (prev.get("provenance") or {}), (res.get("provenance") or {})
    pf, nf = (pp.get("files_sha256") or {}), (npv.get("files_sha256") or {})
    rec = {"at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "reason": reason,
           "prev_status": prev.get("status"), "new_status": res.get("status"),
           "changed": {"status": prev.get("status") != res.get("status"),
                       "files": sorted(k for k in set(pf) | set(nf) if pf.get(k) != nf.get(k)),
                       "card_values": pp.get("card_values_sha16") != npv.get("card_values_sha16"),
                       "driver": pp.get("driver_sha16") != npv.get("driver_sha16"),
                       "run_id": prev.get("run_id") != res.get("run_id")},
           "prev_provenance": pp, "new_provenance": npv, "prev": prev}
    with open(pathlib.Path(run) / VERDICT_HISTORY, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
    return rec


def stage1_verdict(run_dir, *, values=None, card=LI2S2_CARD, log=print, reason="수동 (--stage1_verdict)"):
    """li2s-2 1 단계 시드 판정을 **원자료에서 새로 계산해서** 낸다 (gate_check · melt_window_check · seed_gate · 최종 구조 ·
    traj 프레임 수 · thermo 열 · 실행 식별) → stage1_verdict.json. 판정에는 원자료 지문 · 카드 값 지문 · 도구 지문을 같이 적는다
    (회신 DG P1-4). 이미 판정이 있으면 덮어쓰기 **전에** 그 판정 전체와 지문 변화 · 사유를 stage1_verdict_history.jsonl 에 남긴다 (회신 DH P1-5)."""
    from ase.io import read
    v = values if values is not None else read_li2s2_values(card)
    run = pathlib.Path(run_dir)
    plan = None
    try:
        plan = json.loads((run / "plan.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        res = {"status": "incomplete", "reasons": {"incomplete": ["plan.json 없음"]}, "run": str(run)}
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        res = {"status": "incomplete", "reasons": {"incomplete": [f"plan.json 을 못 읽는다 ({type(e).__name__})"]}, "run": str(run)}
    if plan is not None:
        files = {f: (run / f).is_file() for f in ("result.json", "final.xyz", "thermo.csv", "traj.xyz")}
        checks = {}
        if files["thermo.csv"]:
            with open(run / "thermo.csv", encoding="utf-8", errors="replace") as fh:
                hdr = fh.readline().strip().split(",")
            miss = [c for c in v["thermo_required_columns"] if c not in hdr]
            checks["thermo_header"] = {"columns": hdr, "missing": miss, "ok": not miss}
        gate = melt = seedg = None
        if files["thermo.csv"] and checks["thermo_header"]["ok"]:
            try:
                gate = gate_check(run, win_ps=float(v["gate_check"]["win_ps"]), log=lambda *a: None)
            except Exception as e:
                gate = {"schedule_complete": False, "error": f"{type(e).__name__}: {e}"}
        if files["traj.xyz"]:
            melt = melt_window_check(run, values=v, log=lambda *a: None)
            n_fr = _xyz_frames(run / "traj.xyz")
            want = None
            if all(_fin(plan.get(k)) for k in ("melt_ps", "quench_ps", "hold_ps", "save_ps")) and float(plan["save_ps"]) > 0:
                want = int(round((float(plan["melt_ps"]) + float(plan["quench_ps"]) + float(plan["hold_ps"])) / float(plan["save_ps"]))) + 1
            checks["traj_frames"] = {"n": n_fr, "expected": want}
        if files["final.xyz"] and files["traj.xyz"]:
            try:
                seedg = seed_gate(run, write_raw=True, log=lambda *a: None)
            except SystemExit as e:                       # md_init_raw.xyz 가 다르다 — 그 자리에서 죽지 않고 판정에 싣는다
                checks["seed_gate_error"] = str(e)
            except Exception as e:
                checks["seed_gate_error"] = f"{type(e).__name__}: {e}"
        checks["identity"] = identity_check(run, plan)
        if files["final.xyz"]:
            raw_last = None
            if files["traj.xyz"]:
                try:
                    raw_last = read(str(run / "traj.xyz"), index=-1)
                except Exception:
                    raw_last = None
            checks["final_structure"] = final_structure_check(run, plan, v, raw_last)
        res = combine_stage1(plan, v, gate, melt, seedg, files, checks=checks)
        res.update({"run": str(run), "gate_check": gate, "melt_window_check": melt, "checks": checks,
                    "seed_gate_view": (seedg or {}).get(v["seed_gate"]["version"])})
    res["provenance"] = {"files_sha256": run_provenance(run), "card_values_sha16": values_sha16(v), "driver_sha16": driver_sha16(),
                         "⛔": "묶음 판정 (stage1_summary) 이 이 지문을 지금 파일 · 카드 값 · 도구와 다시 잰다 — 안 맞으면 그 시드는 무효 (다시 판정)"}
    res["reason"] = reason
    vf = run / "stage1_verdict.json"
    if vf.is_file():
        try:
            prev = json.loads(vf.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            prev = {"status": None, "⛔": f"이전 판정 파일을 못 읽었다 ({type(e).__name__})", "raw_text": vf.read_text(encoding="utf-8", errors="replace")}
        h = _append_history(run, prev, res, reason)
        res["history"] = {"file": VERDICT_HISTORY, "prev_status": h["prev_status"], "changed": h["changed"]}
    tmp = vf.with_name(vf.name + ".tmp")
    tmp.write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    os.replace(tmp, vf)
    log(f"  [stage1] {run} → {res['status']}" + (" · ⛔ 그 계를 닫는 사건" if res.get("closes_system") else "") + "  "
        + "; ".join(str(x) for k in ("invalid", "incomplete", "fail") for x in res["reasons"].get(k, [])))
    return res


def summarize_stage1(verdicts, values, cost=None):
    """li2s-2 1 단계 묶음 판정 (회신 DF P1-3 · 회신 DG P0-1 · P0-3 · P1-5) — verdicts: {(계, 시드): stage1_verdict dict 또는 None}.

    계마다: invalid 가 있으면 invalid · 첫 시드 녹음 미충족 (closes_system) 이면 그 계 닫힘 · 탈락이 (시드 수 − need) 를 넘으면 탈락 ·
    **선언된 시드가 전부 판정 끝 (pass · fail)** 이고 pass ≥ need 면 통과 · 아니면 대기 (missing · incomplete 가 남음).
    허용 상태 밖 ('unknown' 등) 은 invalid. 한쪽 계라도 닫힘 · 탈락이면 비교 트랙 전체 멈춤.
    cost = {"total_h", "cap_h"} (러너 비용 장부) — total > cap 이면 '상한 · 미완결' (통과로 올리지 않는다) · None 이면 상한을 확인하지
    못했으므로 두 계가 통과여도 1 단계 통과로 올리지 않는다 (대기). 두 계 통과면 2 단계 시드 = 두 계 **모두** 통과한 시드 중 작은 둘 ·
    기계는 그 순서로 (카드 stage2_machines)."""
    seeds, need = list(values["seeds"]), int(values["stage1_need_pass"])
    per, sw_seen, unknown, ident = {}, {}, [], []
    rid_at = {}
    for (s, sd), vv in verdicts.items():                  # 회신 DH P0-2 — 같은 실행을 여러 시드로 세지 않는다
        if vv is not None and vv.get("run_id"):
            rid_at.setdefault(vv["run_id"], []).append(f"{s}{sd}")
    dup = {k: x for k, x in rid_at.items() if len(x) > 1}
    for s in ("A", "B"):
        st, closed = {}, []
        for sd in seeds:
            vv = verdicts.get((s, sd))
            x = "missing" if vv is None else vv.get("status")
            if x not in LI2S2_STATUSES and x != "missing":
                unknown.append(f"{s}{sd}={x!r}"); x = "invalid"
            if vv is not None and x != "missing":
                if vv.get("system") is not None and (vv.get("system"), vv.get("seed")) != (s, sd):
                    ident.append(f"{s}{sd} 자리의 판정이 ({vv.get('system')}, {vv.get('seed')}) 런이다"); x = "invalid"
                if vv.get("run_id") in dup:
                    ident.append(f"{s}{sd} 의 run_id 가 {dup[vv['run_id']]} 와 같다 (한 실행을 여러 시드로)"); x = "invalid"
            st[sd] = x
            if vv is not None and vv.get("closes_system") is True:
                closed.append(sd)
        n_pass = sum(1 for x in st.values() if x == "pass")
        n_fail = sum(1 for x in st.values() if x == "fail")
        n_bad = sum(1 for x in st.values() if x == "invalid")
        n_open = sum(1 for x in st.values() if x in ("missing", "incomplete"))
        status = ("invalid" if n_bad else "closed" if closed else "fail" if n_fail > len(seeds) - need
                  else "pass" if (n_open == 0 and n_pass >= need) else "pending")
        per[s] = {"status": status, "per_seed": st, "n_pass": n_pass, "n_fail": n_fail, "n_open": n_open,
                  "closed_by_first_seed": closed}
        for sd in seeds:
            vv = verdicts.get((s, sd)) or {}
            if vv.get("status") == "pass":
                sw = {k: x for k, x in (vv.get("software") or {}).items()}
                sw_seen[json.dumps(sw, sort_keys=True)] = sw
    out = {"per_system": per, "software_variants": list(sw_seen.values()), "stage2": None, "unknown_status": unknown,
           "identity_problems": ident, "cost": cost}
    led_bad = list((cost or {}).get("invalid") or [])
    led_open = list((cost or {}).get("pending") or [])
    over = bool(cost is not None and not (_fin(cost.get("total_h")) and _fin(cost.get("cap_h"))
                                         and float(cost["total_h"]) <= float(cost["cap_h"])))
    if any(per[s]["status"] == "invalid" for s in per) or len(sw_seen) > 1 or led_bad:
        out["track"] = "invalid"
        out["why"] = ("카드와 다른 실행 · 원자료와 안 맞는 판정 · 실행 식별 불일치 · 모르는 판정 상태 · 장부 불완전 · 또는 통과 시드의 소프트웨어 판이 "
                      "둘 이상 — 자료 · 기록 오류 (과학적 판정 아님) · 고친 뒤 다시"
                      + (f" (모르는 상태 {unknown})" if unknown else "") + (f" (식별 {ident})" if ident else "")
                      + (f" (장부 {led_bad})" if led_bad else ""))
    elif any(per[s]["status"] == "closed" for s in per):
        out["track"] = "stop_track"
        out["why"] = ("계의 첫 시드 녹음 판정 미충족 → 그 계 닫힘 → 두 계 비교 트랙 전체 멈춤 (회신 DG P0-1 · 재시작으로 다시 열지 않는다) — "
                      + " · ".join(f"{s}{per[s]['closed_by_first_seed']}" for s in per if per[s]["closed_by_first_seed"]))
    elif any(per[s]["status"] == "fail" for s in per):
        out["track"] = "stop_track"; out["why"] = "한쪽 계가 1 단계에서 닫혔다 → 두 계 비교 트랙 전체 멈춤 (회신 DF P1-3)"
    elif over:
        out["track"] = "cap_incomplete"
        out["why"] = (f"비용 장부 {cost.get('total_h')} h > 상한 {cost.get('cap_h')} h (또는 비유한) — 1 단계 미완결 · "
                      "그때 끝난 시드만 골라 판정하지 않는다 (회신 DG P0-3)")
    elif all(per[s]["status"] == "pass" for s in per):
        common = sorted(sd for sd in seeds if per["A"]["per_seed"][sd] == "pass" and per["B"]["per_seed"][sd] == "pass")
        if cost is None:
            out["track"] = "pending"; out["why"] = "두 계 모두 통과지만 비용 장부를 못 봤다 — 상한 안인지 확인 전에는 1 단계 통과로 올리지 않는다"
        elif led_open:
            out["track"] = "pending"; out["why"] = f"두 계 모두 통과지만 장부에 비용이 확정 안 된 런이 있다 ({led_open}) — 통과로 올리지 않는다"
        elif len(common) < 2:
            out["track"] = "stop_track"; out["why"] = f"두 계 공통 통과 시드가 {len(common)} 개 — 2 단계에 둘이 필요하다"
        else:
            m = list(values["stage2_machines"])
            out["track"] = "stage1_pass"
            out["stage2"] = {"seeds": common[:2], "machines": {str(sd): m[i] for i, sd in enumerate(common[:2])},
                             "common_pass_seeds": common, "rule": "두 계 모두 통과한 시드 중 작은 둘 · 기계는 그 순서"}
            out["why"] = "두 계 모두 통과 (선언된 시드 전부 판정 끝 · 비용 상한 안)"
    else:
        out["track"] = "pending"
        out["why"] = "시드 판정이 덜 끝났다 (미판정 · 미완이 남으면 통과로 올리지 않는다 — 회신 DG P1-5)"
    return out


def attempt_inventory(out_root):
    """현재 · 보존된 시드 폴더의 실행을 읽는다. plan 이 아직 없어도 실행 전 기록으로 장부와 잇는다.
    기록을 모두 지우거나 root 밖으로 옮긴 실행을 복원하는 도구는 아니다. 기존 plan-only 실행은 신원을 읽되 추정하지 않는다.
    """
    found, invalid = {}, []
    root = pathlib.Path(out_root)
    for system in ("A", "B"):
        parent = root / system
        if not parent.is_dir():
            continue
        for rd in sorted(parent.iterdir()):
            if not rd.is_dir():
                continue
            ids, att_rec = [], None
            for name in (ATTEMPT_NAME, "plan.json"):
                p = rd / name
                if not p.is_file():
                    continue
                try:
                    rec = json.loads(p.read_text(encoding="utf-8"))
                    rid, sysn, seed = rec.get("run_id"), rec.get("system"), rec.get("seed")
                    if not (isinstance(rid, str) and RUN_ID_RE.fullmatch(rid)
                            and sysn == system and type(seed) is int):
                        raise ValueError("실행 식별 필드 불일치")
                except (OSError, ValueError, AttributeError) as e:
                    invalid.append(f"{p}: 실행 신원을 못 읽음 ({type(e).__name__})")
                    continue
                ids.append((rid, sysn, seed))
                if name == ATTEMPT_NAME:
                    att_rec = {k: rec.get(k) for k in ("retry_of", "retry_stop_id", "retry_kind")}
            if len(set(ids)) > 1:
                invalid.append(f"{rd}: 실행 전 기록과 plan 신원이 다름")
            for rid, sysn, seed in set(ids):
                if rid in found:
                    invalid.append(f"run_id {rid} 산출물 폴더가 둘: {found[rid]['path']} · {rd}")
                found[rid] = {"system": sysn, "seed": seed, "path": str(rd), "attempt": att_rec}
    return found, invalid


def folder_stage(folder):
    """⭐ 회신 DJ Q2 — 실행 폴더의 완료 단계: 'final' (result.json · final.xyz) · 'md_complete' (traj 가 계획 프레임까지 · final 없음 =
    FIRE 미완) · 'md_incomplete' · 'no_plan' · 'unreadable' (plan · traj 머리를 못 읽음). 쓰는 중에 끊긴 마지막 반쪽 프레임은 세지 않는다."""
    f = pathlib.Path(folder)
    if any((f / x).is_file() for x in ("result.json", "final.xyz")):
        return "final"
    if not (f / "plan.json").is_file():
        return "no_plan"
    try:
        plan = json.loads((f / "plan.json").read_text(encoding="utf-8"))
        want = int(round((float(plan["melt_ps"]) + float(plan["quench_ps"]) + float(plan["hold_ps"])) / float(plan["save_ps"]))) + 1
    except (OSError, ValueError, KeyError, TypeError, ZeroDivisionError, AttributeError):
        return "unreadable"
    tr = f / "traj.xyz"
    if not tr.is_file():
        return "md_incomplete"
    try:
        with open(tr, encoding="utf-8", errors="replace") as fh:
            head = fh.readline().replace("\x00", "").strip()
            n_lines = 1 + sum(1 for _ in fh)
    except OSError:
        return "unreadable"
    if not head:                                      # 빈 파일 · NUL 만 (정전 때 디스크에 안 내려간 꼬리) = 프레임 0
        return "md_incomplete"
    try:
        nat = int(head)
    except ValueError:
        return "unreadable"
    if nat <= 0:
        return "unreadable"
    return "md_complete" if n_lines // (nat + 2) >= want else "md_incomplete"


def verdict_file_status(folder):
    """판정 파일 상태 — None (파일 없음) · 허용 상태 · 'unreadable' (있는데 못 읽음 · 모르는 상태). 회신 DJ P0-2: 없음과 판독 불가를 가른다."""
    vf = pathlib.Path(folder) / "stage1_verdict.json"
    if not vf.is_file():
        return None
    try:
        st = json.loads(vf.read_text(encoding="utf-8")).get("status")
    except (OSError, ValueError, AttributeError):
        return "unreadable"
    return st if st in LI2S2_STATUSES else "unreadable"


def declaration_problems(decl, kind, values, rejudge_needed=False, prev_status=None):
    """⭐ 회신 DJ Q1 · Q4 — 재시도 선언 (확인 STOP 에 붙인 것) 검사: 그 종류에 허용된 **결과와 무관한** 사유 (카드 retry_reasons) ·
    상한으로 멈춘 런 (장부 상태 'cap') 은 카드 cap_retry_reasons 만 · 그 사유는 상한 런에만 · 사건 · 근거 · 선언자 · 선언 시각 ·
    (MD 까지 · 끝까지 돈 invalid 런이면) 있는 파일을 고쳐 다시 판정할 수 없다는 이유. 문제 목록 (빈 목록 = 통과).
    ⛔ 못 하는 것: 사람이 적은 사건이 참인지 · 결과를 보고 멈춘 것이 아닌지는 모른다 — 기록 (사건 · 근거 · 선언자) 을 남겨 감사할 수 있게 할 뿐."""
    if not isinstance(decl, dict):
        return ["재시도 선언이 없다 (사유 · 사건 · 근거 · 선언자 — 결과와 무관한 설비 · 운영 사건만 · Ctrl-C · abnormal · resume 는 사유가 아니다)"]
    why = []
    allowed = list(((values.get("retry_reasons") or {}).get(kind)) or [])
    cap_r = list(values.get("cap_retry_reasons") or [])
    reason = decl.get("reason")
    if reason not in allowed:
        why.append(f"사유 {reason!r} 는 {kind} 재시도에 허용된 사유 {allowed} 가 아니다")
    elif prev_status == "cap" and reason not in cap_r:
        why.append(f"상한으로 멈춘 런의 재시도 사유는 {cap_r} 뿐이다 ({reason!r} 아님 — 정전 사유로 상한을 늘리지 않는다)")
    elif reason in cap_r and prev_status != "cap":
        why.append(f"사유 {reason!r} 는 상한으로 멈춘 런 (장부 상태 cap) 에만 — 앞 런 상태 {prev_status!r}")
    for k in ("event", "evidence", "declared_by", "declared_at"):
        if not (isinstance(decl.get(k), str) and decl[k].strip()):
            why.append(f"선언 {k} 없음")
    if rejudge_needed and not (isinstance(decl.get("rejudge_impossible_reason"), str) and decl["rejudge_impossible_reason"].strip()):
        why.append("MD 까지 (또는 끝까지) 돈 invalid 런 — 있는 파일을 고쳐 다시 판정할 수 없다는 이유 (rejudge_impossible_reason) 가 없다")
    return why


#: 정전 손실로 셀 수 있는 '도중에 끊긴' 장부 상태 — 상한 멈춤 (cap) · 녹음 판정 멈춤 (fail · invalid) · 정상 끝 (rc 0) 은 아니다
CUT_SHORT_STATUSES = ("interrupted", "orphaned")


def _cut_short(r):
    return (r.get("verdict") not in ("pass", "fail", "invalid")
            and (r.get("status") in CUT_SHORT_STATUSES or (r.get("status") == "ended" and r.get("rc") not in (0, None))))


def effective_cap(runs, stop_history, values, inventory=None):
    """⭐ 회신 DJ Q4 — 실효 상한 = 카드 stage1_cap_gpu_h + min(정전 손실, 카드 stage1_outage_extra_budget_gpu_h).
    정전 손실 = 확인된 STOP 에 정전 사유 (카드 outage_reasons) 로 선언된 런 중 **도중에 끊긴** 런 (판정 없음 · 상태 interrupted ·
    orphaned · rc ≠ 0 끝) 의 확정 비용 — inventory 를 주면 그 폴더가 MD 미완 (md_incomplete · no_plan) 일 때만 (MD 완료 · 최종 산출은
    잃은 것이 아니다 — 판정 · FIRE 복구 대상). 그 밖의 상한 인상은 카드 개정 (결정) 뿐."""
    base = float(values["stage1_cap_gpu_h"])
    extra = float(values["stage1_outage_extra_budget_gpu_h"])
    outage = set(values["outage_reasons"])
    lost = {h.get("run_id") for h in (stop_history or []) if isinstance(h, dict) and h.get("acked_at")
            and isinstance(h.get("declaration"), dict) and h["declaration"].get("reason") in outage}
    loss, counted = 0.0, []
    for r in (runs or []):
        if not (isinstance(r, dict) and r.get("run_id") in lost and _fin(r.get("wall_h")) and float(r["wall_h"]) >= 0 and _cut_short(r)):
            continue
        if inventory is not None:
            rec = inventory.get(r["run_id"])
            if not rec or folder_stage(rec["path"]) not in ("md_incomplete", "no_plan"):
                continue
        loss += float(r["wall_h"]); counted.append(f"{r.get('system')}{r.get('seed')}:{str(r['run_id'])[:8]}")
    return base + min(loss, extra), {"base_h": base, "outage_loss_h": loss, "outage_extra_budget_h": extra, "outage_runs": counted}


def ledger_check(out_root, verdicts, values):
    """⭐ 회신 DH P0-1 · DI · DJ — 장부 = **실행 목록**. 장부가 없으면 None (확인 못 함 → 통과 안 됨).
    invalid: 장부 꼴 · run_id 꼴 · 중복 · 비용이 유한한 비음수가 아님 · 근거가 측정 · 보수 상한 · 증언 상한이 아님 · 증언 상한의 근거 필드
             (카드 attestation_required_fields) · 하한 (유한 · heartbeat 이상 · 증언 때 하한과 같음) · 폴더 ↔ 장부 양쪽 (보존 누락 포함) ·
             재시도 이력 (두 번째 실행부터: retry_of = 바로 앞 실행 · retry_kind = 앞 실행 종류 · retry_stop_id = 그 앞 실행에 묶여 확인된 STOP ·
             그 STOP 의 선언 · stage1_attempt.json 의 재시도 필드 = 장부 · 과학적 판정 · 판독 불가 판정 · 끝까지 / MD 까지 돈 런 뒤 재시도 ·
             끊긴 런 재시도 수 (앞 실행 종류로 센다) > 카드 한도) · 판정 ↔ 장부.
    pending: 끝나지 않은 런 (heartbeat 는 하한일 뿐). total_h = 확정 비용 합 · cap_h = 실효 상한 (effective_cap)."""
    p = pathlib.Path(out_root) / LEDGER_NAME
    if not p.is_file():
        return None
    invalid, pending, by_id, attested = [], [], {}, []
    try:
        led = json.loads(p.read_text(encoding="utf-8"))
        runs, stop_hist = led.get("runs"), led.get("stop_history", [])
    except (json.JSONDecodeError, UnicodeDecodeError, AttributeError) as e:
        return {"total_h": float("nan"), "cap_h": float(values["stage1_cap_gpu_h"]), "invalid": [f"장부를 못 읽었다 ({type(e).__name__})"],
                "pending": [], "runs": 0, "attested": [], "source": str(p)}
    if not isinstance(runs, list):
        invalid.append("장부 runs 가 목록이 아니다"); runs = []
    if not isinstance(stop_hist, list):
        invalid.append("장부 stop_history 가 목록이 아니다"); stop_hist = []
    req_att = list(values.get("attestation_required_fields") or [])
    tot = 0.0
    for r in runs:
        if not isinstance(r, dict):
            invalid.append("장부 runs 원소가 객체가 아니다"); continue
        key = f"{r.get('system')}{r.get('seed')}"
        rid = r.get("run_id")
        if not (isinstance(rid, str) and RUN_ID_RE.match(rid)):
            invalid.append(f"{key} 런의 run_id {rid!r} 꼴이 아니다 — 폴더 · 판정과 못 잇는다"); continue
        if rid in by_id:
            invalid.append(f"장부에 run_id {rid[:8]} 가 둘 ({key})")
        by_id[rid] = r
        if r.get("end") is None:
            pending.append(f"{key} 런이 끝나지 않았다 (상태 {r.get('status')} · 비용 미확정 — heartbeat {r.get('wall_h_so_far')} h 는 하한)")
            continue
        w = r.get("wall_h")
        if not (_fin(w) and float(w) >= 0.0):
            invalid.append(f"{key} 런 비용 {w!r} — 유한한 비음수가 아니다"); continue
        if r.get("cost_basis") not in COST_BASES:
            invalid.append(f"{key} 런 비용 근거 {r.get('cost_basis')!r} — 측정 · 보수 상한 · 증언 상한이 아니면 확정 비용이 아니다"); continue
        if r.get("cost_basis") == "attested_upper_bound":       # 정전 복구 · 회신 DJ P0-3 · Q3 — 증언 상한
            at, lo, hb = r.get("attestation"), r.get("wall_h_lower"), r.get("wall_h_so_far")
            bad = []
            if r.get("status") != "orphaned":
                bad.append(f"증언 상한은 재부팅 고아 런 (orphaned) 에만 — 상태 {r.get('status')!r}")
            if not isinstance(at, dict):
                bad.append("근거 (attestation) 없음"); at = {}
            for f_ in req_att:
                x = at.get(f_)
                ok_ = (_fin(x) and float(x) >= 0) if f_ == "uncertainty_h" else (isinstance(x, str) and x.strip())
                if not ok_:
                    bad.append(f"근거 {f_} 없음")
            if not (_fin(lo) and _fin(hb) and float(lo) >= 0 and float(hb) >= 0 and float(lo) >= float(hb) - 1e-9):
                bad.append(f"하한이 미상 · 잘못 (하한 {lo!r} · heartbeat {hb!r}) — 하한 미상이면 비용도 미상")
            elif not (_same(at.get("lower_at_attest"), lo, rel=0.0, abs_=1e-9) and _same(at.get("heartbeat_at_attest"), hb, rel=0.0, abs_=1e-9)):
                bad.append(f"증언 때 하한 · heartbeat ({at.get('lower_at_attest')!r} · {at.get('heartbeat_at_attest')!r}) ≠ 장부 ({lo!r} · {hb!r})")
            elif float(w) < float(lo):
                bad.append(f"증언 상한 {w} h < 하한 {lo} h")
            if bad:
                invalid.append(f"{key} 런 증언 상한 — " + " · ".join(bad)); continue
            attested.append(f"{key} {float(w):g} h ({str(at.get('event'))[:40]} · {at.get('confirmer')})")
        tot += float(w)
    inventory, inventory_bad = attempt_inventory(out_root)
    invalid.extend(inventory_bad)
    for rid, rec in inventory.items():
        r = by_id.get(rid)
        if r is None:
            invalid.append(f"보존 포함 실행 {rid} ({rec['path']}) 이 장부에 없다")
        elif (r.get("system"), r.get("seed")) != (rec["system"], rec["seed"]):
            invalid.append(f"실행 {rid} 의 산출물 · 장부 계/시드가 다름")
    for rid, r in by_id.items():                              # 회신 DJ P0-2 — 장부 → 보존 폴더 방향
        if rid not in inventory:
            invalid.append(f"장부의 {r.get('system')}{r.get('seed')} 런 ({rid[:8]}) 폴더가 run_root 의 계 폴더 안에 없다 (보존 누락 · 지우거나 밖으로 옮김)")
    hist = {h.get("stop_id"): h for h in stop_hist if isinstance(h, dict) and h.get("stop_id")}
    seen = {}
    for r in runs:
        if isinstance(r, dict) and isinstance(r.get("run_id"), str):
            seen.setdefault((r.get("system"), r.get("seed")), []).append(r)
    max_int = int(values["stage1_max_interrupt_retries_per_seed"])      # 카드 검사가 0 이상 정수를 보장 — 없으면 여기서 멈춘다 (검사를 끄지 않는다)
    fields = ("retry_of", "retry_stop_id", "retry_kind")
    for k, rr_ in seen.items():
        tag = f"{k[0]}{k[1]}"
        n_int = 0
        for i_, r in enumerate(rr_):
            inv_rec = inventory.get(r.get("run_id"))
            att = (inv_rec or {}).get("attempt")
            if inv_rec is not None and att is None:
                invalid.append(f"{tag}: 실행 {r['run_id'][:8]} 폴더에 실행 전 기록 ({ATTEMPT_NAME}) 이 없다 — 재시도 필드를 대조할 수 없다")
            elif att is not None and any(att.get(f_) != r.get(f_) for f_ in fields):
                invalid.append(f"{tag}: 실행 {r['run_id'][:8]} 의 {ATTEMPT_NAME} 재시도 필드가 장부와 다르다")
            if i_ == 0:
                if any(r.get(f_) for f_ in fields):
                    invalid.append(f"{tag}: 첫 실행 {r['run_id'][:8]} 에 재시도 필드가 있다")
                continue
            p_ = rr_[i_ - 1]
            pf = (inventory.get(p_.get("run_id")) or {}).get("path")
            pfs = verdict_file_status(pf) if pf else None
            pv = p_.get("verdict")
            if pv in ("pass", "fail") or pfs in ("pass", "fail"):
                invalid.append(f"{tag}: 과학적 판정 ({pv or pfs}) 뒤에 같은 시드를 다시 돌렸다"); continue
            if pfs == "unreadable":
                invalid.append(f"{tag}: 앞 실행 {str(p_.get('run_id'))[:8]} 판정 파일을 못 읽는데 다시 돌렸다"); continue
            kind = "invalid" if (pv == "invalid" or pfs == "invalid") else "interrupted"
            if kind == "interrupted":
                n_int += 1
            if r.get("retry_of") != p_.get("run_id"):
                invalid.append(f"{tag}: 실행 {r['run_id'][:8]} 의 retry_of {str(r.get('retry_of'))[:8]} ≠ 바로 앞 실행 {str(p_.get('run_id'))[:8]}")
            if r.get("retry_kind") != kind:
                invalid.append(f"{tag}: 실행 {r['run_id'][:8]} 의 retry_kind {r.get('retry_kind')!r} ≠ 앞 실행 종류 {kind!r}")
            h = hist.get(r.get("retry_stop_id"))
            if not (h and h.get("acked_at") and h.get("run_id") == p_.get("run_id") and h.get("code") in RETRY_BIND_CODES[kind]):
                invalid.append(f"{tag}: 실행 {r['run_id'][:8]} 이 앞 실행에 묶여 확인된 STOP ({' · '.join(RETRY_BIND_CODES[kind])}) 과 안 묶인다")
            else:
                st_ = folder_stage(pf) if pf else None
                dp = declaration_problems(h.get("declaration"), kind, values, prev_status=p_.get("status"),
                                          rejudge_needed=(kind == "invalid" and st_ in ("final", "md_complete")))
                if dp:
                    invalid.append(f"{tag}: 재시도 선언 — " + " · ".join(dp))
            st_p = folder_stage(pf) if pf else None
            if st_p == "unreadable":
                invalid.append(f"{tag}: 앞 실행 {str(p_.get('run_id'))[:8]} 폴더의 완료 단계를 못 읽는데 다시 돌렸다")
            elif kind == "interrupted" and st_p in ("final", "md_complete"):
                invalid.append(f"{tag}: 앞 실행이 끝까지 (또는 MD 까지) 돌았는데 다시 돌렸다 — 판정 · FIRE 복구 대상")
        if n_int > max_int:
            invalid.append(f"{tag}: 끊긴 런 재시도 {n_int} 번 > 카드 한도 {max_int} (앞 실행 종류로 셈)")
    for r in runs:                                            # 실패를 보존 폴더로 옮겨 새 실행으로 대체해도 과학적 탈락은 사라지지 않는다
        if not isinstance(r, dict) or r.get("verdict") != "fail":
            continue
        vv = verdicts.get((r.get("system"), r.get("seed")))
        if vv is not None and vv.get("run_id") != r.get("run_id"):
            invalid.append(f"{r.get('system')}{r.get('seed')}: 과학적 fail 실행을 다른 실행으로 대체했다")
    for (s, sd), vv in verdicts.items():
        if vv is None:
            continue
        rid = vv.get("run_id")
        if not (isinstance(rid, str) and rid):
            (pending if vv.get("status") == "incomplete" else invalid).append(f"{s}{sd} 판정에 run_id 가 없다 — 장부와 못 잇는다")
            continue
        r = by_id.get(rid)
        if r is None:
            invalid.append(f"{s}{sd} 판정의 run_id {rid[:8]} 가 장부에 없다 — 비용이 안 잡힌 실행")
        elif (r.get("system"), r.get("seed")) != (s, sd):
            invalid.append(f"{s}{sd} 판정의 run_id {rid[:8]} 는 장부에서 {r.get('system')}{r.get('seed')} 런이다")
    cap_eff, cap_info = effective_cap([r for r in runs if isinstance(r, dict)], stop_hist, values, inventory=inventory)
    return {"total_h": tot, "cap_h": cap_eff, "cap_info": cap_info, "invalid": invalid, "pending": pending,
            "runs": len(runs), "attested": attested, "source": str(p)}


def stage1_summary(out_root, *, values=None, card=LI2S2_CARD, log=print):
    """<out_root>/<A|B>/seed<S>/stage1_verdict.json 을 모아 묶음 판정 → <out_root>/stage1_summary.json.
    ⭐ 회신 DG P1-4 — 판정 파일을 그대로 믿지 않는다: 지문 (원자료 · 카드 값 · 도구) 을 지금 것과 다시 잰다 → 안 맞으면 그 시드는
    invalid ('다시 판정하라'). 비용 장부 (러너) 로 상한을 다시 잰다 (DG P0-3)."""
    v = values if values is not None else read_li2s2_values(card)
    root = pathlib.Path(out_root); ver = {}
    cur_vals, cur_drv = values_sha16(v), driver_sha16()
    stale = []
    for s in ("A", "B"):
        for sd in v["seeds"]:
            rd = root / s / f"seed{sd}"
            p = rd / "stage1_verdict.json"
            if not p.is_file():
                ver[(s, sd)] = None; continue
            vv = json.loads(p.read_text(encoding="utf-8"))
            pv = vv.get("provenance") or {}
            bad = []
            if pv.get("files_sha256") != run_provenance(rd):
                bad.append("원자료 지문이 지금 파일과 다르다 (판정 뒤 파일이 바뀌었거나 판정만 복사됐다)")
            if pv.get("card_values_sha16") != cur_vals:
                bad.append(f"카드 값 지문 {pv.get('card_values_sha16')} ≠ 지금 {cur_vals}")
            if pv.get("driver_sha16") != cur_drv:
                bad.append(f"도구 지문 {pv.get('driver_sha16')} ≠ 지금 {cur_drv}")
            if bad:
                stale.append(f"{s}{sd}")
                vv = {**vv, "status": "invalid", "closes_system": vv.get("closes_system") is True,
                      "reasons": {**(vv.get("reasons") or {}), "invalid": list((vv.get("reasons") or {}).get("invalid", []))
                                  + [f"⛔ 판정이 원자료에 안 묶였다 — {' · '.join(bad)} → --stage1_verdict 로 다시 판정"]}}
            ver[(s, sd)] = vv
    res = summarize_stage1(ver, v, cost=ledger_check(root, ver, v))
    res["stale_verdicts"] = stale
    (root / "stage1_summary.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    log(f"  [stage1 묶음] {res['track']} — {res['why']} · " +
        " · ".join(f"{s} {res['per_system'][s]['status']} ({res['per_system'][s]['n_pass']} 통과)" for s in ("A", "B")) +
        (f" · 2 단계 시드 {res['stage2']['seeds']} {res['stage2']['machines']}" if res.get("stage2") else "") +
        (f" · 비용 {res['cost']['total_h']:.1f}/{res['cost']['cap_h']:g} h" if res.get("cost") and _fin(res["cost"].get("total_h")) else "") +
        (f" · ⛔ 지문 불일치 {stale}" if stale else ""))
    return res


def schedule(T_melt, T_final, quench_rate_K_s, dt_fs):
    if quench_rate_K_s is None or quench_rate_K_s <= 0:
        raise SystemExit("⛔ --quench_rate [K/s] 를 주어라 (G2: 담금질 속도는 결과 보기 전에 선언한다). 기본값은 없다.")
    quench_ps = (T_melt - T_final) / quench_rate_K_s * 1e12
    n = int(round(quench_ps * 1000.0 / dt_fs))
    return quench_ps, n


def run_melt_quench(atoms, calc, out, *, seed, T_melt, T_final, melt_ps, quench_rate, hold_ps, dt_fs, save_ps,
                    pre_relax=True, fix_density=None, compress_ps=20.0, log=print):
    from ase import units
    from ase.io import write
    from ase.md.nptberendsen import NPTBerendsen
    from ase.md.velocitydistribution import MaxwellBoltzmannDistribution, Stationary
    from ase.optimize import FIRE
    validate_fix_density(fix_density, compress_ps, melt_ps)
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    atoms.calc = calc
    if pre_relax:
        FIRE(atoms, logfile=str(out / "prerelax.log")).run(fmax=1.0, steps=200)
    MaxwellBoltzmannDistribution(atoms, temperature_K=T_melt, rng=np.random.default_rng(seed)); Stationary(atoms)
    dt = dt_fs * units.fs
    if fix_density is None:
        dyn = NPTBerendsen(atoms, dt, temperature_K=T_melt, pressure_au=0.0,
                           taut=BARO["taut_fs"] * units.fs, taup=BARO["taup_fs"] * units.fs,
                           compressibility_au=BARO["compressibility_au"])
    else:   # ⭐ li2s-2 — 같은 열욕 (taut) · 바로스탯 없음 · melt 첫 compress_ps 동안 밀도를 ρ 로 끌어올린다
        from ase.md.nvtberendsen import NVTBerendsen
        dyn = NVTBerendsen(atoms, dt, temperature_K=T_melt, taut=BARO["taut_fs"] * units.fs)
        rho0 = density_g_cm3(atoms)
        n_c = max(1, int(round(compress_ps * 1000 / dt_fs)))
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
            if fix_density is not None and phase == "melt" and i < n_c:
                # 이 덩어리가 끝날 때의 목표 밀도로 먼저 맞춘다 — 마지막 덩어리에서 정확히 ρ 에 닿는다
                scale_to_density(atoms, rho0 + (float(fix_density) - rho0) * min(1.0, (i + k) / n_c))
            for _ in range(k):
                record(T_set); dyn.run(1); step += 1
            i += k
            if (i // chunk) % 200 == 0:
                log(f"  [{phase}] {i}/{n_steps} T_set={T_set:.0f} K T={atoms.get_temperature():.0f} K "
                    f"ρ={sum(MASS[s] for s in atoms.get_chemical_symbols())/6.02214076e23/(atoms.get_volume()*1e-24):.3f} "
                    f"({(time.time()-t0)/60:.1f} min)")
                sys.stdout.flush()   # ⛔ 로그 리다이렉트 시 블록 버퍼링 — 안 하면 진행 줄이 몇 시간 뒤에 뜬다
    record(T_final); tlog.close()
    if fix_density is not None:
        rho_end = density_g_cm3(atoms)
        if abs(rho_end / float(fix_density) - 1.0) > 1e-9:   # 압축이 덜 끝났거나 셀이 움직였다 — 조용히 넘기지 않는다
            raise SystemExit(f"⛔ --fix_density {fix_density}: 담금질 끝 밀도 {rho_end:.6f} 가 목표와 다르다")
    FIRE(atoms, logfile=str(out / "final_relax.log")).run(fmax=0.05, steps=2000)
    write(str(out / "final.xyz"), atoms, format="extxyz")
    write(str(out / "final.vasp"), atoms, format="vasp", direct=True, sort=True)
    info = {"quench_ps": quench_ps, "n_steps": {"melt": n_m, "quench": n_q, "hold": n_h}, "wall_min": (time.time() - t0) / 60}
    if fix_density is not None:
        info["fix_density"] = {"target_g_cm3": float(fix_density), "start_g_cm3": rho0, "compress_steps": n_c,
                               "final_g_cm3": density_g_cm3(atoms)}
    return info


def write_gr_csv(cols, path):
    keys = list(cols)
    with open(path, "w") as f:
        f.write(",".join(keys) + "\n")
        for i in range(len(cols["r_A"])):
            f.write(",".join(f"{cols[k][i]:.5f}" for k in keys) + "\n")


def build_plan(system, seed, sym, density, T_melt, T_final, melt_ps,
               quench_rate, quench_ps, hold_ps, dt_fs, save_ps, fix_density=None, compress_ps=20.0):
    """plan.json 의 내용. **게이트가 읽을 값이 여기서 들어간다** — 읽는 곳은 `--gate_check`.
    `fix_density` 를 주면 게이트_입력 의 앙상블이 NVT (ensemble_fixed_density) 로 바뀐다 — 옵션이 없으면 옛 plan 과 같은 키다."""
    ens = ENSEMBLE if fix_density is None else ensemble_fixed_density(fix_density, compress_ps)
    extra = {} if fix_density is None else {"fix_density_g_cm3": float(fix_density), "compress_ps": float(compress_ps),
                                            "card_fix_density": "db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json"}
    return {"system": system, "seed": seed, "n_atoms": len(sym), **extra,
            "composition": {e: sym.count(e) for e in sorted(set(sym))},
            "start_density_g_cm3": density, "T_melt_K": T_melt, "T_final_K": T_final, "melt_ps": melt_ps,
            "quench_rate_K_s": quench_rate, "quench_ps": quench_ps, "hold_ps": hold_ps, "dt_fs": dt_fs,
            "save_ps": save_ps,   # ⛔ 빠뜨리면 --melt_check 가 dt 를 **유도**한다 (2026-09-12)
            "G2_declared_before_results": True,
            "card": "db/properties/lpscl_li2s_interphase_prereg_2026_09_11.json",
            # ⭐ 게이트가 읽는 값 — 누가 읽나: `--gate_check`. 없으면 그 모드가 **기록없음** 으로 fail-closed 한다.
            "게이트_입력": {"G2_quench_rate_K_s": quench_rate, **ens, "final_relax": final_relax_decl(fix_density),
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
    res["rho_flat_pct"] = 100.0 * (res["rho_max"] - res["rho_min"]) / res["rho_mean"]
    if g and g.get("ensemble") == "NVT":
        # ⭐ li2s-2 고정 밀도 런 — 압력은 결과 (기록) · 게이트는 '밀도 = 선언값' · 옛 G4 밴드 (1층 카드) 는 해당 없음
        rt = float(g["target_density_g_cm3"])
        dev = max(abs(res["rho_min"] / rt - 1.0), abs(res["rho_max"] / rt - 1.0), abs(res["rho_last"] / rt - 1.0))
        rho_ok = bool(dev <= DENSITY_REL_TOL)   # ⭐ 한 곳에서만 정한다 — density_ok 와 gate_ok 가 갈리면 깨기 시험이 못 본다 (11-03 실측)
        # ⭐ 회신 DF P1-2 — 밀도만 맞으면 통과하던 구멍 셋을 막는다: ① 계획한 일정 끝까지 ② 판정 창이 실제 유지 구간 안
        #   ③ 압력이 **기록돼 있다** (크기는 판정 아님 · NaN · 빈 칸이면 '압력이 없다' 로 가른다)
        total = float(plan["melt_ps"]) + float(plan.get("quench_ps") or 0.0) + float(plan["hold_ps"])
        sched_ok = bool(float(t["t_ps"].max()) >= total - float(plan["save_ps"]) - 1e-6)
        T_fin = float(plan["T_final_K"])
        in_hold = bool(tail.sum() > 0 and np.allclose(t["T_set_K"][tail], T_fin))
        try:
            ht = hold_trend(t, n_blocks)
        except KeyError as e:
            ht = {"⛔": str(e)}
        hold_ok = bool(in_hold and ht.get("hold_len_ps", 0.0) >= 0.9 * float(plan["hold_ps"]) - 1e-9)
        # ⛔ 회신 DG P1-7 — virial 열을 지워도 '기록 있음' 이던 구멍: 두 압력 열이 **다 있고** 유한해야 기록이다
        p_cols = [c for c in ("P_GPa", "P_virial_GPa") if c in t]
        cols_ok = len(p_cols) == 2 and all(c in t for c in ("t_ps", "T_set_K", "density_g_cm3"))
        p_tail = np.concatenate([t[c][tail] for c in p_cols]) if p_cols else np.array([])
        p_rec = bool(cols_ok and p_tail.size > 0 and np.isfinite(p_tail).all())
        gate_ok = bool(rho_ok and sched_ok and hold_ok and p_rec)
        res.update({"mode": "NVT_fixed_density", "target_density_g_cm3": rt, "density_max_rel_dev": dev,
                    "density_ok": rho_ok, "pressure_ok": None, "target_pressure_GPa": None,
                    "schedule_complete": sched_ok, "planned_total_ps": total, "window_in_hold": hold_ok,
                    "pressure_recorded": p_rec, "pressure_columns": p_cols, "thermo_columns_ok": cols_ok, "hold_trend": ht,
                    "gate_ok": gate_ok, "G4_fires": None, "G4_role": "해당 없음 (고정 밀도 · 1층 밴드 카드 밖)",
                    "P_role": "기록 — 고정 밀도에서 UMA 셀에 남는 내부 압력 (크기는 판정 아님 · 기록 유무는 판정)"})
        log(f"  NVT 고정 밀도 — 목표 {rt:.4f} · 마지막 {win_ps:g} ps ρ {res['rho_min']:.5f}–{res['rho_max']:.5f} "
            f"(최대 상대 차 {dev:.1e} → {'같음' if rho_ok else '⛔ 다름'}) · 일정 {'끝' if sched_ok else '⛔ 미완'} "
            f"({float(t['t_ps'].max()):g}/{total:g} ps) · 창 {'유지 구간 안' if hold_ok else '⛔ 유지 구간 밖'} · "
            f"⟨P⟩ {res['P_mean_GPa']:+.3f} GPa ({'기록' if p_rec else '⛔ 기록 없음'})")
        return res
    tgt = float(g["target_pressure_GPa"]) if g else 0.0
    res["target_pressure_GPa"] = tgt
    res["pressure_ok"] = abs(res["P_mean_GPa"] - tgt) <= p_tol
    res["gate_ok"] = res["pressure_ok"]
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


# ───────────────────────── --seed_gate: 시드 게이트 입력을 **원시·relax 두 판**으로 ─────────────────────────
#: ⛔ 2026-09-24 발견 — 소셀 유리 MD 카드(`lpscl_smallcell_glass_md_estimand_2026_09_21.json`) 해명 1 은
#:   *"final.xyz = 담금질 마지막 프레임, 원시 (relax 안 한다)"* 라고 적었다. **이 파일과 안 맞는다** —
#:   `run_melt_quench` 는 FIRE(fmax 0.05 · 고정셀) **뒤에** final.xyz 를 쓴다 (FINAL_RELAX · 개정 ③ 이 이미 그렇게 적는다).
#:   원시는 traj.xyz 의 **마지막 프레임**뿐이다. 그래서 이 모드는 두 판을 **나란히** 찍고, 게이트를 어느 판으로
#:   잴지는 정하지 않는다 (카드·사람 몫 · 정오 기록 `lpscl_smallcell_glass_md_gateA_erratum_2026_09_24.json`).
#:   MD 초기구조로 쓸 원시 판은 `md_init_raw.xyz` 로 떨군다 — 이름이 곧 내용이다.
SEED_GATE_RAW = "md_init_raw.xyz"


def _min_pair(sym, pos, cell, skip=()):
    """최소상 최단 원자간 거리와 그 쌍의 원소. `skip` 의 원소쌍은 뺀다."""
    sym = np.asarray(sym)
    D = mic_dists(pos, pos, cell)
    np.fill_diagonal(D, np.inf)
    for a_el, b_el in skip:
        ia, ib = sym == a_el, sym == b_el
        D[np.ix_(ia, ib)] = np.inf
        D[np.ix_(ib, ia)] = np.inf
    i, j = np.unravel_index(np.argmin(D), D.shape)
    return float(D[i, j]), "-".join(sorted((str(sym[i]), str(sym[j]))))


def _gate_view(at):
    """시드 게이트가 보는 값만 — PS₄ · 다리 S · P–P · 최단 원자간(전체 · P–S 제외) · 밀도."""
    sym, pos, cell = at.get_chemical_symbols(), at.get_positions(), np.asarray(at.get_cell())
    ind = indicators(sym, pos, cell)
    v = {k: ind[k] for k in ("PS4_fraction", "P_S_coord_hist", "bridging_S_P2S7_like",
                             "P_P_bonds_P2S6_like", "density_g_cm3", "n_atoms") if k in ind}
    v["min_pair_A"], v["min_pair_kind"] = _min_pair(sym, pos, cell)
    v["min_pair_excl_PS_A"], v["min_pair_excl_PS_kind"] = _min_pair(sym, pos, cell, skip=(("P", "S"),))
    return v


def _xyz_frames(path):
    """extxyz 프레임 수 — 프레임마다 (원자수 + 2) 줄이라는 것만 쓴다. 안 맞으면 None (세지 못함 ≠ 0)."""
    with open(path, encoding="utf-8", errors="replace") as f:
        first = f.readline().strip()
        n_lines = 1 + sum(1 for _ in f)
    try:
        nat = int(first)
    except ValueError:
        return None
    return n_lines // (nat + 2) if n_lines % (nat + 2) == 0 else None


def seed_gate(run, write_raw=True, log=print):
    """시드 게이트의 **입력값**을 원시(traj 마지막 프레임)와 relax 본(final.xyz) 양쪽에서 찍는다.

    ⛔ 이 함수가 못 하는 것
      · 판정하지 않는다 — 어느 판으로 잴지, 문턱이 무엇인지는 카드·사람이 정한다.
      · 원시가 없으면(traj.xyz 없음) **final.xyz 로 대신하지 않는다** — 원시 칸을 비우고 이유를 적는다.
      · 마지막 프레임이 유지 구간 끝인지는 plan.json 길이와 **프레임 수로만** 대조한다 — traj 가 잘렸으면
        경보하고 그대로 둔다 (버리지 않는다). 프레임 헤더에 t 가 없어서 시각을 직접 읽지는 못한다.
      · `md_init_raw.xyz` 가 이미 있고 다르면 **덮어쓰지 않고 멈춘다** — 그 파일로 MD 가 이미 돌았을 수 있다.
    """
    import hashlib
    from ase import Atoms
    from ase.io import read, write
    run = pathlib.Path(run)
    res = {"run": str(run), "raw": None, "relaxed": None, "raw_vs_relaxed": None, "warnings": [],
           "⛔": "판정 아님 — 게이트를 어느 판으로 잴지는 카드·사람 몫 (이 도구의 final.xyz 는 relax 본이다)"}
    plan = json.loads((run / "plan.json").read_text(encoding="utf-8")) if (run / "plan.json").exists() else {}
    fr = (plan.get("게이트_입력") or {}).get("final_relax")
    res["final_xyz_is"] = ("relax 본 (plan.json 게이트_입력.final_relax: "
                           + ", ".join(f"{k}={fr[k]}" for k in ("kind", "fmax_eV_A", "cell") if k in fr) + ")"
                           if fr else "relax 본 (plan.json 에 기록 없음 — 2026-09-12 이전 런 · 코드상 FIRE 뒤에 쓴다)")
    raw_at = None
    traj = run / "traj.xyz"
    if traj.exists():
        n_fr = _xyz_frames(traj)
        raw_at = read(str(traj), index=-1)
        save_ps = plan.get("save_ps")
        res["raw"] = {"source": "traj.xyz", "frame": (n_fr - 1) if n_fr else None,
                      "t_ps": (n_fr - 1) * float(save_ps) if (n_fr and save_ps) else None, **_gate_view(raw_at)}
        if n_fr and save_ps and all(k in plan for k in ("melt_ps", "quench_ps", "hold_ps")):
            want = int(round((plan["melt_ps"] + plan["quench_ps"] + plan["hold_ps"]) / float(save_ps))) + 1
            res["raw"]["frames_expected"] = want
            if n_fr < want:
                res["warnings"].append(f"traj 가 잘렸다 ({n_fr}/{want} 프레임) — 마지막 프레임이 유지 구간 끝이 아니다")
        elif not n_fr:
            res["warnings"].append("traj 프레임 수를 못 셌다 (줄 수가 원자수+2 의 배수가 아니다) — 시각 미상")
    else:
        res["raw_why"] = "traj.xyz 없음 — 원시를 못 구했다 (final.xyz 로 대신하지 않는다)"
    rel_at = None
    if (run / "final.xyz").exists():
        rel_at = read(str(run / "final.xyz"))
        res["relaxed"] = {"source": "final.xyz", **_gate_view(rel_at)}
    else:
        res["relaxed_why"] = "final.xyz 없음"
    if raw_at is not None and rel_at is not None:
        if raw_at.get_chemical_symbols() == rel_at.get_chemical_symbols():
            cell = np.asarray(raw_at.get_cell())
            d = (rel_at.get_positions() - raw_at.get_positions()) @ np.linalg.inv(cell)
            d = np.linalg.norm((d - np.round(d)) @ cell, axis=1)
            res["raw_vs_relaxed"] = {"disp_max_A": float(d.max()), "disp_rms_A": float(np.sqrt((d ** 2).mean())),
                                     "cell_max_abs_diff_A": float(np.abs(cell - np.asarray(rel_at.get_cell())).max())}
            if d.max() < 1e-6:
                res["warnings"].append("final.xyz 가 원시와 같다 — relax 가 안 됐거나 다른 도구가 쓴 파일이다")
        else:
            res["raw_vs_relaxed_why"] = "원자 수·순서가 달라 변위를 못 쟀다"
            res["warnings"].append(res["raw_vs_relaxed_why"])
    if raw_at is not None and write_raw:
        clean = Atoms(symbols=raw_at.get_chemical_symbols(), positions=raw_at.get_positions(),
                      cell=raw_at.get_cell(), pbc=True)
        clean.wrap()
        clean.info = {"source": "traj.xyz", "frame": res["raw"]["frame"], "t_ps": res["raw"]["t_ps"],
                      "raw": True, "wrapped": True, "made_by": "melt_quench_uma.py --seed_gate"}
        out = run / SEED_GATE_RAW
        if out.exists():
            old = read(str(out))
            same = (old.get_chemical_symbols() == clean.get_chemical_symbols()
                    and np.abs(np.asarray(old.get_cell()) - np.asarray(clean.get_cell())).max() < 1e-8)
            if same:
                dd = (old.get_positions() - clean.get_positions()) @ np.linalg.inv(np.asarray(clean.get_cell()))
                same = np.linalg.norm((dd - np.round(dd)) @ np.asarray(clean.get_cell()), axis=1).max() < 1e-6
            if not same:
                raise SystemExit(f"⛔ {out} 이 이미 있고 지금 뽑은 원시와 다르다 — 덮어쓰지 않는다 "
                                 "(그 파일로 MD 가 이미 돌았을 수 있다. 사람이 확인한다)")
            status = "이미 있음 · 같음"
        else:
            write(str(out), clean, format="extxyz")
            status = "썼다"
        res["md_init_raw"] = {"path": str(out), "status": status,
                              "sha256": hashlib.sha256(out.read_bytes()).hexdigest()}

    def _row(tag, v):
        return (f"  {tag:<12s} {v['PS4_fraction']:.4f}  {v['bridging_S_P2S7_like']:>3d}  {v['P_P_bonds_P2S6_like']:>3d}"
                f"   {v['min_pair_A']:.3f} ({v['min_pair_kind']:<5s})  {v['min_pair_excl_PS_A']:.3f} "
                f"({v['min_pair_excl_PS_kind']:<5s})  {v['density_g_cm3']:.4f}")
    log(f"[{run.parent.name}/{run.name}] final.xyz = {res['final_xyz_is']}")
    log("               PS4   다리S  P–P   최단 (쌍)        최단·P–S 제외     ρ g/cm³")
    if res["raw"]:
        t = res["raw"]["t_ps"]
        log(_row(f"원시 t={t:.0f}" if t is not None else "원시 t=?", res["raw"]))
    else:
        log(f"  원시         —  ({res['raw_why']})")
    log(_row("relax", res["relaxed"]) if res["relaxed"] else f"  relax        —  ({res['relaxed_why']})")
    if res["raw_vs_relaxed"]:
        rv = res["raw_vs_relaxed"]
        log(f"  원시↔relax 변위 max {rv['disp_max_A']:.3f} · rms {rv['disp_rms_A']:.3f} Å · "
            f"셀 차 {rv['cell_max_abs_diff_A']:.1e} Å")
    if res.get("md_init_raw"):
        log(f"  → {SEED_GATE_RAW} {res['md_init_raw']['status']} (sha256 {res['md_init_raw']['sha256'][:16]})")
    for w in res["warnings"]:
        log(f"  ⚠ {w}")
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


# ═══ NEB 끝점 게이트 (카드 §0b-②-4) ══════════════════════════════════════
NEB_CARD = "db/properties/lpscl_smallcell_neb_estimand_2026_09_18.json"
NEB_PATS = {
    "gate_A_li_min_A":  r"두 위치 차\(MIC\)\s*≥\s*\*{0,2}([0-9.]+)\s*Å",
    "gate_B_rmsd_max_A": r"RMSD\(두 끝점 사이, MIC\)\s*≤\s*\*{0,2}([0-9.]+)\s*Å",
}


def read_neb_gate_thresholds(card=NEB_CARD):
    """게이트 A/B 문턱을 **봉인된 산문에서 직접** 판다 (read_gb2_thresholds 와 같은 규약).

    사본을 만들지 않는다 — 두 벌이 되면 갈라지고, 원장이 이기는데 도구는 사본을 본다.
    둘 중 하나라도 못 찾으면 **죽는다**: 기본값을 지어내지 않는다.
    """
    q = pathlib.Path(card)
    if not q.exists():
        q = pathlib.Path(__file__).resolve().parents[2] / card
    d = json.loads(q.read_text(encoding="utf-8"))
    try:
        g = d["0b_경로선택·집계_규칙_제안_2026_09_18"]["②_경로_선택_규칙"][
            "4_★_끝점_게이트_두_개_다_통과해야_후보다"]
        src = g["게이트_A_서로_다른_최소"] + "\n" + g["게이트_B_골격이_안_바뀜"]
    except (KeyError, TypeError):
        raise KeyError(f"{q}: §0b-②-4 끝점 게이트 절이 없다 — 도구가 문턱을 지어내지 않는다")
    th = {}
    for k, pat in NEB_PATS.items():
        m = re.search(pat, src)
        if not m:
            raise ValueError(f"⛔ {q}: 게이트 문턱 '{k}' 를 산문에서 못 찾았다 — "
                             f"카드 문구가 바뀌었으면 **도구를 고치고 시험을 다시 친다**.")
        th[k] = float(m.group(1))
    return th


def mic_dist(a, b, cell):
    """두 점 사이 최소상 거리 [Å]."""
    f = (np.asarray(b) - np.asarray(a)) @ np.linalg.inv(cell)
    f -= np.round(f)
    return float(np.linalg.norm(f @ cell))


def non_li_rmsd(at0, at1):
    """비-Li 원자의 MIC RMSD [Å]. 골격이 재배열했는지 본다.

    ⛔ 못 하는 것: 전체 병진을 빼지 않는다. 셀 고정 이완이라 병진 자유도가 없다
      (있었다면 이 값이 병진으로 부풀었을 것이고, 그건 다른 시험이 필요하다).
    """
    sym = np.array(at0.get_chemical_symbols())
    m = sym != "Li"
    cell = np.array(at0.get_cell())
    p0, p1 = at0.get_positions()[m], at1.get_positions()[m]
    d = np.array([mic_dist(x, y, cell) for x, y in zip(p0, p1)])
    return float(np.sqrt((d ** 2).mean())), int(m.sum()), float(d.max())


def endpoint_gate(events_dir, out_json=None, card=NEB_CARD, device="cuda",
                  turbo=False, fmax=None, steps=2000, log=print):
    """§0b-②-4 끝점 게이트 — **UMA 탐침**.

    ⛔ 이 함수가 하지 않는 것
      · 비준된 게이트를 **집행하지 않는다**. §0b 는 이완을 QE(G1 §3)로 적었다.
        여기 결과는 `gate_engine: "UMA(탐침)"` 로 표시되고, 판정도 `provisional_*` 이다.
      · 장벽을 계산하지 않는다.
      · 사건을 고르지 않는다 — events.json 에 있는 것을 전부 본다.
    """
    from ase.io import read as ase_read
    from ase.optimize import FIRE
    ev_dir = pathlib.Path(events_dir)
    meta = json.loads((ev_dir / "events.json").read_text(encoding="utf-8"))
    th = read_neb_gate_thresholds(card)
    # 이완 설정은 이 궤적을 만든 것과 **같은 것**을 쓴다 (새 눈금을 만들지 않는다)
    fm = float(FINAL_RELAX["fmax_eV_A"]) if fmax is None else float(fmax)
    log(f"[endpoint_gate] 사건 {len(meta['events'])} 건 · 문턱 A ≥ {th['gate_A_li_min_A']} Å · "
        f"B ≤ {th['gate_B_rmsd_max_A']} Å · FIRE fmax {fm} (셀 고정, FINAL_RELAX 승계)")
    calc = make_calc(turbo=turbo, device=device)
    rows, n_a, n_b = [], 0, 0
    for e in meta["events"]:
        tag, ai = e["tag"], int(e["atom_index"])
        got = {}
        for side in ("i", "f"):
            at = ase_read(ev_dir / f"{tag}_{side}.xyz")
            at.calc = calc
            opt = FIRE(at, logfile=None)
            opt.run(fmax=fm, steps=steps)
            #: ⭐ 이완된 구조와 **에너지**를 남긴다 (2026-09-18).
            #   전에는 판정만 하고 버렸는데, ⓑ 카드 §2 가 E_i·E_f 를 요구하고
            #   NEB 는 **이완된** 끝점에서 출발해야 한다. 다시 이완하면 같은 값이
            #   나오겠지만, 그건 '같을 것이다' 라는 가정이고 파일이 증거다.
            e_tot = float(at.get_potential_energy())
            rel_dir = ev_dir / "relaxed"; rel_dir.mkdir(exist_ok=True)
            at.write(str(rel_dir / f"{tag}_{side}_relaxed.xyz"))
            got[side] = (at, opt.get_number_of_steps(), bool(opt.converged()), e_tot)
        (a0, s0, c0, E_i), (a1, s1, c1, E_f) = got["i"], got["f"]
        cell = np.array(a0.get_cell())
        dLi = mic_dist(a0.get_positions()[ai], a1.get_positions()[ai], cell)
        rmsd, n_fw, dmax = non_li_rmsd(a0, a1)
        okA, okB = dLi >= th["gate_A_li_min_A"], rmsd <= th["gate_B_rmsd_max_A"]
        n_a += okA; n_b += okB
        why = [] if (okA and okB) else (
            (["A: 이완 후 같은 최소로 모였다"] if not okA else []) +
            (["B: 골격이 재배열했다 — 같은 계가 아니다"] if not okB else []))
        rows.append({"tag": tag, "atom_index": ai, "disp_md_A": e["disp_A"],
                     #: ⓑ 카드 §2 의 원시량. ⛔ 장벽이 아니다 — 끝점 에너지다.
                     "E_i_eV": round(E_i, 6), "E_f_eV": round(E_f, 6),
                     "dE_f_minus_i_eV": round(E_f - E_i, 6),
                     "relaxed_xyz": [f"relaxed/{tag}_i_relaxed.xyz",
                                     f"relaxed/{tag}_f_relaxed.xyz"],
                     "li_sep_after_relax_A": round(dLi, 4),
                     "non_li_rmsd_A": round(rmsd, 4), "non_li_max_A": round(dmax, 4),
                     "n_framework_atoms": n_fw,
                     "gate_A_pass": bool(okA), "gate_B_pass": bool(okB),
                     "survives": bool(okA and okB), "rejected_because": why,
                     "relax_steps": [s0, s1], "relax_converged": [c0, c1]})
        log(f"  {tag:14s} MD {e['disp_A']:.2f} Å → 이완 후 Li {dLi:.2f} Å "
            f"({'A✓' if okA else 'A✗'}) · 골격 RMSD {rmsd:.3f} Å "
            f"({'B✓' if okB else 'B✗'}) · {'생존' if okA and okB else '기각'}")
    surv = [r for r in rows if r["survives"]]
    res = {
        "date": time.strftime("%Y-%m-%d"), "kind": "endpoint_gate_probe",
        "⛔_gate_engine": "UMA(탐침) — **비준된 §0b 는 이완을 QE(G1 §3)로 적었다.** "
                          "이 결과는 기각률을 먼저 알아 QE 예산을 정하기 위한 것이고, "
                          "게이트를 **집행하지 않는다**. 판정은 provisional 이다.",
        "card": card, "thresholds": th,
        "relax": {"kind": "FIRE", "fmax_eV_A": fm, "cell": "fixed",
                  "uma_mode": getattr(calc, "_mq_mode", "?"), "승계": "FINAL_RELAX"},
        "n_events": len(rows), "provisional_n_survive": len(surv),
        "provisional_reject_rate": round(1 - len(surv) / len(rows), 4) if rows else None,
        "gate_A_pass": int(n_a), "gate_B_pass": int(n_b),
        "rows": rows,
        "⇒_§0b_②_5": ("**전부 기각** — §0b-②-5 에 따라 장벽 분포를 내지 않는다. "
                       "⚠ 단 이 판정은 UMA 이완 기준이다. QE 로 확정하려면 1저자 결정이 필요하다."
                       if not surv else
                       f"생존 {len(surv)} 건 — 이들에 대해서만 QE 예산을 잡는다."),
    }
    if out_json:
        pathlib.Path(out_json).write_text(json.dumps(res, ensure_ascii=False, indent=1),
                                          encoding="utf-8")
        log(f"  → {out_json}")
    log(f"  ⇒ 생존 {len(surv)}/{len(rows)} (A 통과 {n_a} · B 통과 {n_b}) — {res['⇒_§0b_②_5']}")
    return res


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
# ───────────────────────── 모델 검증 카드: 0 K 등방 경로 (UMA) ─────────────────────────
MC_CARD = "db/properties/lpscl_smallcell_glass_model_check_estimand_2026_10_19.json"


def read_mc_values(card=MC_CARD):
    """모델 검증 카드의 `기계_판독_값` — 키가 없으면 KeyError 로 죽는다 (숫자를 지어내지 않는다)."""
    q = pathlib.Path(card)
    if not q.exists():                       # repo 루트 상대 (도구가 어디서 불리든 같은 카드)
        q = pathlib.Path(__file__).resolve().parents[2] / card
    return json.loads(q.read_text(encoding="utf-8"))["기계_판독_값"], q


def eos_label(path):
    """…/<A|B>/seed<N>/<파일> → 'A_s<N>' — 경로에서 계 · 시드를 읽는다 (못 읽으면 죽는다 · 추측 안 한다)."""
    p = pathlib.Path(path)
    m = re.fullmatch(r"seed(\d+)", p.parent.name)
    if not m or p.parent.parent.name not in ("A", "B"):
        raise SystemExit(f"⛔ {path}: '…/<A|B>/seed<N>/<파일>' 꼴이 아니다 — 라벨을 추측하지 않는다")
    return f"{p.parent.parent.name}_s{int(m.group(1))}"


def eos_topology(atoms, rPS, rSS):
    """(P–S ≤ rPS 결합 수, S–S ≤ rSS 쌍 수) — 카드 토폴로지 규칙의 입력 (최소상 · 직교 셀)."""
    sym = np.array(atoms.get_chemical_symbols()); pos = atoms.get_positions(); cell = atoms.cell.array
    P, S = pos[sym == "P"], pos[sym == "S"]
    nPS = int((mic_dists(P, S, cell) <= rPS).sum()) if len(P) and len(S) else 0
    nSS = 0
    if len(S) > 1:
        D = mic_dists(S, S, cell); np.fill_diagonal(D, np.inf); nSS = int((D <= rSS).sum() // 2)
    return nPS, nSS


def eos_path(structs, out_dir, which="main", device="cuda", card=MC_CARD, calc=None, log=print):
    """모델 검증 카드 §1b 경로 — 구조마다 등방 스케일 점 (분율 좌표 유지) 에서 UMA **default** 고정셀 FIRE 이완.

    점마다 <out>/<라벨>/x<0.85>.xyz (기하만) 와 <out>/<라벨>/uma_path.json
    (E · virial P (운동 항 없음) · σ · Fmax · 스텝 · 수렴 · P–S/S–S 수 · 기하 sha256).
    which = 'main' (path_scales) · 'ext_low' · 'ext_high' (카드 연장 점 — 판독 도구가 연장 규칙을 말할 때만).
    json 에 이미 있는 점은 건너뛴다 (재개 · 같은 입력 sha 일 때만).

    ⛔ 못 하는 것: QE · D3 · BM3 를 하지 않는다 (판독 도구 몫) · turbo 를 안 쓴다 (카드 uma_mode) ·
      셀 모양을 안 바꾼다 (등방 스케일만) · 카드 밖 격자를 받지 않는다 (결과 보고 격자를 넓히지 않는다) ·
      점마다 스케일된 원본에서 따로 시작한다 (연쇄 아님 — 카드 §1b).
    """
    import hashlib
    from ase.io import read, write
    from ase.optimize import FIRE
    v, card_path = read_mc_values(card)
    key = {"main": "path_scales", "ext_low": "path_ext_low", "ext_high": "path_ext_high"}[which]
    scales = [float(x) for x in v[key]]
    fmax, steps = float(v["relax_fmax_eV_A"]), int(v["relax_max_steps"])
    rPS, rSS = float(v["topo_PS_A"]), float(v["topo_SS_A"])
    if v["uma_mode"] != "default":
        raise SystemExit(f"⛔ 카드 uma_mode = {v['uma_mode']} — 이 경로는 default 만 안다")
    if calc is None:
        calc = make_calc(device, turbo=False)
    mode = getattr(calc, "_mq_mode", None)
    if mode != "default":
        raise SystemExit(f"⛔ 계산기 모드 {mode!r} — default 여야 한다 (카드 §1b)")
    try:
        import fairchem
        fc_ver = getattr(fairchem, "__version__", "?")
    except Exception:
        fc_ver = None
    out = pathlib.Path(out_dir)
    res = {}
    for sp in structs:
        lab = eos_label(sp)
        at0 = read(str(sp))
        d = out / lab; d.mkdir(parents=True, exist_ok=True)
        jp = d / "uma_path.json"
        src_sha = hashlib.sha256(pathlib.Path(sp).read_bytes()).hexdigest()
        if jp.exists():
            J = json.loads(jp.read_text(encoding="utf-8"))
            if J["meta"]["source_sha256"] != src_sha:
                raise SystemExit(f"⛔ {jp}: 다른 입력 구조의 경로다 (sha 다름) — 섞지 않는다")
        else:
            J = {"meta": {"label": lab, "source": str(sp), "source_sha256": src_sha,
                          "card": str(card_path), "card_sha256": hashlib.sha256(card_path.read_bytes()).hexdigest(),
                          "uma": "uma-s-1p1 · task omat", "mode": mode, "fairchem": fc_ver, "device": device,
                          "relax": {"kind": "FIRE", "cell": "fixed", "fmax_eV_A": fmax, "max_steps": steps},
                          "V_final_A3": float(at0.get_volume()),
                          "⛔": "P_virial 은 운동 항 없음 (0 K 정적) · 기하는 UMA 이완본 — QE 단일점의 입력"},
                 "points": []}
        done = {round(p["x"], 4) for p in J["points"]}
        for x in scales:
            if round(x, 4) in done:
                log(f"  {lab} x={x:.2f} 이미 있음 — 건너뜀"); continue
            at = at0.copy()
            at.set_cell(at0.cell.array * x ** (1.0 / 3.0), scale_atoms=True)
            at.calc = calc
            opt = FIRE(at, logfile=None)
            t0 = time.time()
            conv = opt.run(fmax=fmax, steps=steps)
            F = at.get_forces(); fm = float(np.linalg.norm(F, axis=1).max())
            conv = bool(conv) if isinstance(conv, (bool, np.bool_)) else (fm <= fmax)
            E = float(at.get_potential_energy())
            sig = np.asarray(at.get_stress(voigt=False)) * EV_A3_TO_GPA
            nPS, nSS = eos_topology(at, rPS, rSS)
            g = at.copy(); g.calc = None
            fx = d / f"x{x:.2f}.xyz"
            write(str(fx), g, format="extxyz")
            pt = {"x": x, "V_A3": float(at.get_volume()), "E_eV": E,
                  "P_virial_GPa": float(-np.trace(sig) / 3.0), "sigma_GPa": sig.tolist(),
                  "Fmax_eV_A": fm, "steps": int(opt.nsteps), "converged": conv,
                  "n_PS": nPS, "n_SS": nSS, "geom": fx.name,
                  "geom_sha256": hashlib.sha256(fx.read_bytes()).hexdigest(), "wall_s": round(time.time() - t0, 1)}
            J["points"].append(pt)
            J["points"].sort(key=lambda p: p["x"])
            jp.write_text(json.dumps(J, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            log(f"  {lab} x={x:.2f} V={pt['V_A3']:.1f} E={E:.4f} P={pt['P_virial_GPa']:+.3f} GPa "
                f"Fmax={fm:.3f} steps={pt['steps']} conv={conv} P–S={nPS} S–S={nSS} ({pt['wall_s']} s)")
        res[lab] = J
    return res


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
    # ③b li2s-2 --fix_density — NVT 고정 밀도 경로 (LJ 배선) · 옵션이 없으면 옛 plan 과 같은 키
    #     (회신 DF Q-DF-8 뒤: 압축은 melt/2 전에 끝나야 한다 → melt 0.8 · 압축 0.3 ps)
    symF, posF, cellF = build_random_cell("A", seed=5, n_fu=2, density_g_cm3=0.8)
    with tempfile.TemporaryDirectory() as td:
        atF = Atoms(symbols=symF, positions=posF, cell=cellF, pbc=True)
        infoF = run_melt_quench(atF, LennardJones(sigma=2.5, epsilon=0.05, rc=6.0), td, seed=5, T_melt=600, T_final=300,
                                melt_ps=0.8, quench_rate=3e14, hold_ps=0.02, dt_fs=2.0, save_ps=0.004, pre_relax=False,
                                fix_density=1.2, compress_ps=0.3, log=lambda *a: None)
        thF = read_thermo(os.path.join(td, "thermo.csv"))
        rhoF, tF = thF["density_g_cm3"], thF["t_ps"]
        chk(abs(density_g_cm3(atF) / 1.2 - 1.0) < 1e-9 and abs(infoF["fix_density"]["final_g_cm3"] / 1.2 - 1.0) < 1e-9
            and abs(infoF["fix_density"]["start_g_cm3"] - 0.8) < 0.02,
            f"고정 밀도: 0.8 에서 시작해 담금질 · 완화 끝 밀도가 1.2 (1e-9) — 끝 {infoF['fix_density']['final_g_cm3']:.6f}")
        ramp, after = rhoF[tF < 0.3 - 1e-9], rhoF[tF >= 0.3 - 1e-9]
        chk(ramp.size >= 3 and rhoF[0] < 1.15 and np.all(np.diff(ramp) >= -1e-9) and len(set(np.round(ramp, 4))) >= 3,
            f"고정 밀도: 압축 구간 밀도가 단계적으로 오른다 ({rhoF[0]:.3f} → … · 단계 {len(set(np.round(ramp, 4)))})")
        chk(after.size > 50 and np.all(np.abs(after - 1.2) < 1e-3), "고정 밀도: 압축 뒤 (melt 나머지 · 담금질 · 유지) 밀도가 1.2 에 머문다")
        planF = build_plan("A", 5, list(symF), 0.8, 600, 300, 0.8, 3e14, 1.0, 0.02, 2.0, 0.004, fix_density=1.2, compress_ps=0.3)
        gF = planF["게이트_입력"]
        chk(gF["ensemble"] == "NVT" and gF["barostat"] is None and gF["target_density_g_cm3"] == 1.2
            and "target_pressure_GPa" not in gF and planF["fix_density_g_cm3"] == 1.2,
            "고정 밀도 plan: 게이트_입력 앙상블 = NVT · 목표 밀도 1.2 · 목표 압력 키 없음")
        (pathlib.Path(td) / "plan.json").write_text(json.dumps(planF, ensure_ascii=False), encoding="utf-8")
        gcF = gate_check(td, win_ps=0.015, log=lambda *a: None)
        chk(gcF["mode"] == "NVT_fixed_density" and gcF["gate_ok"] and gcF["pressure_ok"] is None and gcF["schedule_complete"]
            and gcF["window_in_hold"] and gcF["pressure_recorded"] and math.isfinite(gcF["P_mean_GPa"]),
            "--gate_check: 고정 밀도 런 — 일정 완주 · 창이 유지 구간 안 · 압력 기록 · 밀도 = 목표 → 통과")
        tp = pathlib.Path(td) / "thermo.csv"
        orig = tp.read_text(encoding="utf-8")
        lines = orig.splitlines()
        cols = lines[-3].split(","); cols[3] = "1.2500"; lines[-3] = ",".join(cols)
        tp.write_text("\n".join(lines) + "\n", encoding="utf-8")
        chk(not gate_check(td, win_ps=0.015, log=lambda *a: None)["gate_ok"],
            "⛔음성: 유지 구간 한 줄의 밀도를 1.25 로 바꾸면 --gate_check 가 잡는다")
        # 회신 DF P1-2 반례 ① — 담금질 · 유지 없이 melt 기록만 (밀도는 맞음)
        keep = [ln for ln in orig.splitlines()[1:] if float(ln.split(",")[0]) <= 0.79]
        tp.write_text(orig.splitlines()[0] + "\n" + "\n".join(keep) + "\n", encoding="utf-8")
        gm = gate_check(td, win_ps=0.015, log=lambda *a: None)
        chk(not gm["gate_ok"] and not gm["schedule_complete"],
            "⛔음성 DF: melt 기록만 있으면 (일정 미완 · 창이 유지 구간 밖) 밀도가 맞아도 통과 못 한다")
        # 회신 DF P1-2 반례 ② — 압력 열을 NaN 으로
        rows = [orig.splitlines()[0]] + [",".join(c[:-2] + ["nan", "nan"]) for c in (ln.split(",") for ln in orig.splitlines()[1:])]
        tp.write_text("\n".join(rows) + "\n", encoding="utf-8")
        gn = gate_check(td, win_ps=0.015, log=lambda *a: None)
        chk(not gn["gate_ok"] and not gn["pressure_recorded"] and gn["density_ok"],
            "⛔음성 DF: 압력이 NaN 이면 '압력 기록 없음' 으로 통과 못 한다 (압력 크기는 판정하지 않는다)")
        # 회신 DG P1-7 — virial 열을 지우면 (총압만 남음) '기록 있음' 이던 구멍
        rows = [",".join(c[:-1]) for c in (ln.split(",") for ln in orig.splitlines())]
        tp.write_text("\n".join(rows) + "\n", encoding="utf-8")
        gv = gate_check(td, win_ps=0.015, log=lambda *a: None)
        chk(not gv["gate_ok"] and not gv["pressure_recorded"] and gv["thermo_columns_ok"] is False and gv["pressure_columns"] == ["P_GPa"],
            "⛔음성 DG P1-7: thermo 에서 virial 압력 열을 지우면 '압력 기록 없음' · 열 꼴 불일치 (통과 못 한다)")
        chk(planF["게이트_입력"]["final_relax"]["⛔"].startswith("밀도는 **고정 밀도 셀**")
            and build_plan("A", 5, list(symF), 0.8, 600, 300, 0.4, 3e14, 1.0, 0.02, 2.0, 0.004)["게이트_입력"]["final_relax"] is FINAL_RELAX,
            "DG P2: NVT plan 의 final_relax 설명은 '고정 밀도 셀' · NPT plan 은 옛 설명 그대로")
        tp.write_text(orig, encoding="utf-8")
        try:
            melt_check(td, log=lambda *a: None); legacy_refused = False
        except SystemExit as e:
            legacy_refused = "--melt_window_check" in str(e)
        chk(legacy_refused, "⛔음성 DF: 고정 밀도 런에 옛 --melt_check (0 ps 누적 원점) 를 쓰면 거부하고 --melt_window_check 를 가리킨다")
    plan0 = build_plan("A", 5, list(symF), 0.8, 600, 300, 0.4, 3e14, 1.0, 0.02, 2.0, 0.004)
    chk("fix_density_g_cm3" not in plan0 and plan0["게이트_입력"]["ensemble"] == "NPT"
        and plan0["게이트_입력"]["target_pressure_GPa"] == 0.0 and plan0["게이트_입력"]["barostat"] == "Berendsen",
        "옵션이 없으면 plan 은 옛 NPT 0 GPa 그대로 (fix_density 키 없음)")
    for nm, args in (("밀도 0", (0.0, 20.0, 100.0)), ("밀도 음수", (-1.9, 20.0, 100.0)), ("압축 0 ps", (1.9, 0.0, 100.0)),
                     ("압축이 melt 보다 김", (1.9, 120.0, 100.0)), ("밀도 nan", (float("nan"), 20.0, 100.0)),
                     ("압축이 판정 창 (melt/2) 에 걸림 — DF", (1.9, 60.0, 100.0))):
        try:
            validate_fix_density(*args); refused = False
        except SystemExit:
            refused = True
        chk(refused, f"⛔음성: --fix_density 입력 거부 — {nm}")
    try:
        validate_fix_density(None, 0.0, 0.0); validate_fix_density(1.9, 50.0, 100.0); off_ok = True
    except SystemExit:
        off_ok = False
    chk(off_ok, "옵션을 안 주면 (None) 검사하지 않고 · 압축이 판정 창 시작 (50/100) 에 딱 끝나면 받는다")
    # ③c li2s-2 녹음 판정 (회신 DF P0) — 합성 궤적: 창 [50, 100] 좌표가 같고 앞 이력만 다른 둘 · 70 ps 에서 끊긴 것 · 겹침 · NaN
    from ase.io import write as _w
    VAL = {"melt_window": {"t_from_frac_of_melt": 0.5, "t_to_frac_of_melt": 1.0, "lag_fit_ps": [2.0, 25.0], "element": "P",
                           "D_threshold_cm2_s": 1e-6, "threshold_source": "selftest"},
           "fix_density_g_cm3": {"A": 1.91347, "B": 1.88},
           "schedule": {"T_melt_K": 1200.0, "T_final_K": 300.0, "melt_ps": 100.0, "quench_rate_K_s": 1e12, "hold_ps": 50.0,
                        "dt_fs": 2.0, "save_ps": 1.0, "compress_ps": 20.0, "n_atoms": 120},
           "uma_inference_mode": "turbo", "seed_gate": {"version": "relaxed", "PS4_fraction_min": 1.0, "min_pair_excl_PS_A_gt": 2.0},
           "gate_check": {"win_ps": 10.0}, "seeds": [11, 12, 13, 14, 15], "stage1_need_pass": 4, "stage2_machines": ["kgy", "gabia"],
           # 회신 DG — 카드에 더한 값 (T 는 합성 궤적용 8 원자 계 · 실제 카드에는 A · B 만)
           "composition": {"A": {"Cl": 12, "Li": 48, "P": 12, "S": 48}, "B": {"Li": 45, "P": 15, "S": 60}, "T": {"P": 4, "S": 4}},
           "software_required": {"model": "uma-s-1p1", "task": "omat", "versions_present": ["fairchem-core", "torch", "ase"]},
           "thermo_required_columns": ["t_ps", "T_K", "T_set_K", "density_g_cm3", "P_GPa", "P_virial_GPa"],
           "first_seed": 11, "stage1_cap_gpu_h": 230.0, "stage1_max_interrupt_retries_per_seed": 1,
           "retry_reasons": {"interrupted": ["power_outage", "host_crash_or_reboot", "hardware_fault", "budget_cap_raised"],
                             "invalid": ["invalid_cause_fixed"]},
           "outage_reasons": ["power_outage", "host_crash_or_reboot", "hardware_fault"], "stage1_outage_extra_budget_gpu_h": 45.0,
           "cap_retry_reasons": ["budget_cap_raised"],
           "attestation_required_fields": ["event", "time_reference", "uncertainty_h", "derivation", "confirmer", "confirmed_at"]}
    VAL["melt_window"]["estimator"] = MELT_WINDOW_ESTIMATOR
    rng = np.random.default_rng(7); L = 12.0
    base = rng.uniform(1, L - 1, (8, 3)); symW = ["P"] * 4 + ["S"] * 4
    win = [base.copy()]
    for _ in range(50):
        nxt = win[-1].copy(); nxt[:4] += rng.normal(0, 0.6, (4, 3)); win.append(nxt)          # t = 50 … 100 · P 만 움직임
    pre_moving = [win[0].copy()]
    for _ in range(50):
        prv = pre_moving[-1].copy(); prv[:4] += rng.normal(0, 0.9, (4, 3)); pre_moving.append(prv)
    pre_moving = pre_moving[::-1]                                                               # t = 0 … 50 · 끝이 창 첫 프레임
    def _mk_win(td_, frames, plan_extra=None, syms=None):
        pl = {"melt_ps": 100.0, "save_ps": 1.0, "fix_density_g_cm3": 1.2, "compress_ps": 20.0,
              "system": "T", "n_atoms": 8, "composition": {"P": 4, "S": 4}}; pl.update(plan_extra or {})
        (pathlib.Path(td_) / "plan.json").write_text(json.dumps(pl), encoding="utf-8")
        _w(str(pathlib.Path(td_) / "traj.xyz"), [Atoms(symbols=(syms or {}).get(i, symW), positions=f, cell=np.eye(3) * L, pbc=True)
                                                 for i, f in enumerate(frames)], format="extxyz")
    with tempfile.TemporaryDirectory() as ta, tempfile.TemporaryDirectory() as tb, tempfile.TemporaryDirectory() as tc:
        _mk_win(ta, pre_moving[:-1] + win)                       # 앞 50 ps 크게 움직임 → 창
        _mk_win(tb, [win[0]] * 50 + win)                         # 앞 50 ps 얼어 있음 → 같은 창
        ra = melt_window_check(ta, values=VAL, log=lambda *a: None); rb = melt_window_check(tb, values=VAL, log=lambda *a: None)
        chk(ra["D_framework_cm2_s"] is not None and ra["D_framework_cm2_s"] == rb["D_framework_cm2_s"] and ra["verdict"] == rb["verdict"]
            and ra["window_used_ps"] == [50.0, 100.0],
            f"DF 반례: 창 [50, 100] 좌표가 같으면 앞 이력과 무관하게 D 가 같다 ({ra['D_framework_cm2_s']:.3e} · {ra['verdict']})")
        chk(ra["verdict"] == "pass", "합성 확산 창 (P 이동) 은 통과")
        _mk_win(tc, pre_moving[:-1] + [win[0]] * 51)            # 앞은 크게 움직였지만 창 안은 얼어 있음
        rc = melt_window_check(tc, values=VAL, log=lambda *a: None)
        chk(rc["verdict"] == "fail", f"⛔음성 DF: 창 안이 얼어 있으면 앞 이력이 커도 '미충족' ({rc['D_framework_cm2_s']:.1e})")
    with tempfile.TemporaryDirectory() as td:
        _mk_win(td, (pre_moving[:-1] + win)[:71])                # 70 ps 에서 끊김
        rt = melt_window_check(td, values=VAL, log=lambda *a: None)
        chk(rt["verdict"] == "incomplete" and rt["window_used_ps"] == [50.0, 70.0] and not rt["coverage_ok"],
            "⛔음성 DF: 70 ps 에서 끊긴 궤적은 '미완' — 실제 쓴 창 [50, 70] 을 그대로 적는다")
        with open(pathlib.Path(td) / "traj.xyz", "a") as fh:
            fh.write("8\nLattice=\"12 0 0 0 12 0 0 0 12\" Properties=species:S:1:pos:R:3\nP 1.0 2.0")   # 쓰는 중 반쪽 프레임
        rt2 = melt_window_check(td, values=VAL, log=lambda *a: None)
        chk(rt2["verdict"] == "incomplete" and rt2["n_frames_read"] == 71, "쓰는 중인 반쪽 프레임에서 멈추고 '미완' (죽지 않는다)")
    with tempfile.TemporaryDirectory() as td:
        _mk_win(td, pre_moving[:-1] + win, plan_extra={"compress_ps": 60.0})
        chk(melt_window_check(td, values=VAL, log=lambda *a: None)["verdict"] == "invalid",
            "⛔음성 DF: 압축 끝 (60 ps) 이 판정 창 시작 (50 ps) 보다 늦으면 '무효'")
    with tempfile.TemporaryDirectory() as td:
        badf = [f.copy() for f in pre_moving[:-1] + win]; badf[80][0, 0] = np.nan
        _mk_win(td, badf)
        chk(melt_window_check(td, values=VAL, log=lambda *a: None)["verdict"] == "invalid", "⛔음성 DF: 창 안 좌표가 NaN 이면 '무효'")
    # 회신 DG P0-2 — 시작 직후 (plan · traj 없음 · plan 쓰는 중) 는 예외가 아니라 '미완' · P1-7 — estimator 이름 · 종 배치
    with tempfile.TemporaryDirectory() as td:
        r0 = melt_window_check(td, values=VAL, log=lambda *a: None)
        (pathlib.Path(td) / "plan.json").write_text('{"melt_ps": 100.0, "save_', encoding="utf-8")
        r1 = melt_window_check(td, values=VAL, log=lambda *a: None)
        (pathlib.Path(td) / "plan.json").write_text(json.dumps({"melt_ps": 100.0, "save_ps": 1.0, "fix_density_g_cm3": 1.2,
                                                                "compress_ps": 20.0, "system": "T", "n_atoms": 8,
                                                                "composition": {"P": 4, "S": 4}}), encoding="utf-8")
        r2 = melt_window_check(td, values=VAL, log=lambda *a: None)
        chk(r0["verdict"] == r1["verdict"] == r2["verdict"] == "incomplete",
            f"⛔음성 DG P0-2: plan.json 없음 · 쓰는 중 · traj 없음 → 예외가 아니라 '미완' ({r0['verdict']} · {r1['verdict']} · {r2['verdict']})")
    with tempfile.TemporaryDirectory() as td:
        _mk_win(td, pre_moving[:-1] + win)
        VALx = json.loads(json.dumps(VAL)); VALx["melt_window"]["estimator"] = "window_mto_v2"
        chk(melt_window_check(td, values=VALx, log=lambda *a: None)["verdict"] == "invalid",
            "⛔음성 DG P1-7: 카드 estimator 를 다른 이름으로 바꾸면 window_mto_v1 을 돌리지 않고 '무효'")
        chk(any("estimator" in x for x in validate_li2s2_values(VALx)), "⛔음성 DG P1-7: 카드 값 검사가 모르는 estimator 를 거부한다")
    with tempfile.TemporaryDirectory() as td:
        sw_ = ["S"] + symW[1:4] + ["P"] + symW[5:]                 # 0 번 프레임만 P·S 자리를 바꿈 (조성은 같다)
        _mk_win(td, pre_moving[:-1] + win, syms={0: sw_})
        r_sp = melt_window_check(td, values=VAL, log=lambda *a: None)
        chk(r_sp["verdict"] == "invalid" and r_sp["species_ok"] is False,
            f"⛔음성 DG P1-7: 0 번 프레임의 종 배치만 바꾸면 판정이 바뀌지 않고 '무효' ({r_sp['verdict']})")
    with tempfile.TemporaryDirectory() as td:
        _mk_win(td, pre_moving[:-1] + win, plan_extra={"n_atoms": 9})
        chk(melt_window_check(td, values=VAL, log=lambda *a: None)["verdict"] == "invalid", "⛔음성 DG: traj 원자 수 ≠ plan → '무효'")
    # ③d li2s-2 1 단계 시드 판정 · 묶음 판정 (회신 DF P1-2 · P1-3) — 순수 함수
    SW_OK = {"model": "uma-s-1p1", "task": "omat", "inference": "turbo", "fairchem-core": "2.21.0", "torch": "2.8.0", "ase": "3.26.0"}
    plan_ok = {"system": "A", "seed": 12, "fix_density_g_cm3": 1.91347, "n_atoms": 120, "composition": dict(VAL["composition"]["A"]),
               "software": dict(SW_OK), **VAL["schedule"]}
    plan_ok.pop("n_atoms"); plan_ok["n_atoms"] = 120
    g_ok = {"schedule_complete": True, "window_in_hold": True, "density_ok": True, "pressure_recorded": True,
            "thermo_columns_ok": True, "target_density_g_cm3": 1.91347}
    m_ok = {"verdict": "pass"}; s_ok = {"relaxed": {"PS4_fraction": 1.0, "min_pair_excl_PS_A": 2.31}}
    f_ok = {"result.json": True, "final.xyz": True, "thermo.csv": True, "traj.xyz": True}
    chk(combine_stage1(plan_ok, VAL, g_ok, m_ok, s_ok, f_ok)["status"] == "pass", "1 단계 시드 판정: 모두 맞으면 통과")
    for nm, kw, want in (("PS₄ 0.9167", {"seedg": {"relaxed": {"PS4_fraction": 11 / 12, "min_pair_excl_PS_A": 2.31}}}, "fail"),
                         ("최단 원자간 1.98 Å", {"seedg": {"relaxed": {"PS4_fraction": 1.0, "min_pair_excl_PS_A": 1.98}}}, "fail"),
                         ("녹음 미충족", {"melt": {"verdict": "fail", "message": "x"}}, "fail"),
                         ("녹음 미완", {"melt": {"verdict": "incomplete"}}, "incomplete"),
                         ("일정 미완", {"gate": dict(g_ok, schedule_complete=False)}, "incomplete"),
                         ("압력 기록 없음", {"gate": dict(g_ok, pressure_recorded=False)}, "fail"),
                         ("final.xyz 없음", {"files": dict(f_ok, **{"final.xyz": False})}, "incomplete"),
                         ("밀도 1.9 로 돌림", {"plan": dict(plan_ok, fix_density_g_cm3=1.9)}, "invalid"),
                         ("melt 80 ps 로 돌림", {"plan": dict(plan_ok, melt_ps=80.0)}, "invalid"),
                         ("소프트웨어 기록 없음", {"plan": {k: x for k, x in plan_ok.items() if k != "software"}}, "invalid"),
                         # 회신 DG P1-7 표 — 모르는 상태 · NaN · 반쪽 소프트웨어 · virial 열 없음 · 조성 · 최종 구조 · traj 프레임
                         ("녹음 상태 'unknown' (DG)", {"melt": {"verdict": "unknown"}}, "invalid"),
                         ("plan 목표 밀도 NaN (DG)", {"plan": dict(plan_ok, fix_density_g_cm3=float("nan"))}, "invalid"),
                         ("plan melt_ps NaN (DG)", {"plan": dict(plan_ok, melt_ps=float("nan"))}, "invalid"),
                         ("소프트웨어 fairchem·inference 만 (DG)", {"plan": dict(plan_ok, software={"inference": "turbo", "fairchem-core": "2.21.0"})}, "invalid"),
                         ("torch 판이 ?(오류) (DG)", {"plan": dict(plan_ok, software=dict(SW_OK, torch="?(PackageNotFoundError)"))}, "invalid"),
                         ("virial 열 없음 (DG)", {"gate": dict(g_ok, thermo_columns_ok=False, pressure_recorded=False)}, "invalid"),
                         ("thermo 머리줄에 virial 없음 (DG)", {"checks": {"thermo_header": {"ok": False, "missing": ["P_virial_GPa"]}}, "gate": None}, "invalid"),
                         ("gate 목표 밀도 NaN (DG)", {"gate": dict(g_ok, target_density_g_cm3=float("nan"))}, "invalid"),
                         ("조성 다름 (DG)", {"plan": dict(plan_ok, composition={"Li": 45, "P": 15, "S": 60})}, "invalid"),
                         ("final.xyz 가 5 원자 (DG)", {"checks": {"final_structure": {"ok": False, "why": ["원자 수 5 ≠ 120"]}}}, "invalid"),
                         ("thermo 끝났는데 traj 잘림 (DG)", {"checks": {"traj_frames": {"n": 900, "expected": 1051}}}, "invalid"),
                         ("traj 프레임 수를 못 셈 (DG)", {"checks": {"traj_frames": {"n": None, "expected": 1051}}}, "invalid"),
                         ("일정 미완 · traj 짧음 (DG)", {"gate": dict(g_ok, schedule_complete=False), "checks": {"traj_frames": {"n": 900, "expected": 1051}}}, "incomplete"),
                         ("md_init_raw 불일치 (DG)", {"checks": {"seed_gate_error": "⛔ 이미 있고 다르다"}, "seedg": None}, "invalid")):
        args = {"plan": plan_ok, "gate": g_ok, "melt": m_ok, "seedg": s_ok, "files": f_ok, "checks": None}; args.update(kw)
        got = combine_stage1(args["plan"], VAL, args["gate"], args["melt"], args["seedg"], args["files"], checks=args["checks"])["status"]
        chk(got == want, f"⛔음성 DF/DG: 1 단계 시드 판정 — {nm} → {want} (받음 {got})")
    # 회신 DG P0-1 — 계의 첫 시드 녹음 미충족은 '그 계를 닫는 사건' (러너가 멈춰 일정 미완이어도) · 둘째 시드는 일반 탈락
    c_first = combine_stage1(dict(plan_ok, seed=11), VAL, dict(g_ok, schedule_complete=False), {"verdict": "fail", "message": "x"},
                             None, dict(f_ok, **{"final.xyz": False, "result.json": False}))
    c_second = combine_stage1(plan_ok, VAL, g_ok, {"verdict": "fail", "message": "x"}, s_ok, f_ok)
    c_bad = combine_stage1(dict(plan_ok, seed=11, fix_density_g_cm3=1.9), VAL, g_ok, {"verdict": "fail", "message": "x"}, s_ok, f_ok)
    chk(c_first["status"] == "fail" and c_first["closes_system"] and not c_second["closes_system"] and c_second["status"] == "fail"
        and c_bad["status"] == "invalid" and not c_bad["closes_system"],
        "DG P0-1: 첫 시드 (11) 녹음 미충족 → fail + closes_system (일정 미완이어도) · 둘째 시드는 일반 탈락 · 카드와 다른 런이면 닫지 않고 무효")
    def _v(st, fc="2.21.0"):
        return {"status": st, "software": {"inference": "turbo", "fairchem-core": fc}}
    ver = {("A", 11): _v("fail"), ("A", 12): _v("pass"), ("A", 13): _v("pass"), ("A", 14): _v("pass"), ("A", 15): _v("pass"),
           ("B", 11): _v("pass"), ("B", 12): _v("pass"), ("B", 13): _v("pass"), ("B", 14): _v("pass"), ("B", 15): _v("fail")}
    COST = {"total_h": 150.0, "cap_h": 230.0}
    sm = summarize_stage1(ver, VAL, cost=COST)
    chk(sm["track"] == "stage1_pass" and sm["stage2"]["seeds"] == [12, 13] and sm["stage2"]["machines"] == {"12": "kgy", "13": "gabia"},
        f"DF P1-3: A11 · B15 탈락이어도 4/5 씩 통과 → 2 단계 시드 = 공통 통과 중 작은 둘 {sm['stage2'] and sm['stage2']['seeds']} (11 고정 아님)")
    sm2 = summarize_stage1({**ver, ("A", 12): _v("fail")}, VAL, cost=COST)
    chk(sm2["track"] == "stop_track" and sm2["per_system"]["A"]["status"] == "fail" and sm2["stage2"] is None,
        "⛔음성 DF: 한쪽 계가 1 단계에서 닫히면 (A 3/5) 다른 계가 통과해도 비교 트랙 전체가 멈춘다")
    sm3 = summarize_stage1({k: (None if k in (("B", 14), ("B", 15)) else x) for k, x in ver.items()} | {("B", 15): None}, VAL, cost=COST)
    chk(sm3["track"] == "pending", "시드 판정이 덜 끝났으면 (B 3 통과 · 2 없음) 대기")
    sm4 = summarize_stage1({**ver, ("B", 13): _v("pass", fc="2.19.0")}, VAL, cost=COST)
    chk(sm4["track"] == "invalid", "⛔음성 DF: 통과 시드의 fairchem 판이 둘 이상이면 무효 (기계 이름이 아니라 판을 고정)")
    all4 = {(s_, sd): _v("pass") for s_ in ("A", "B") for sd in (11, 12, 13, 14)}
    sm5 = summarize_stage1({**all4, ("A", 15): _v("incomplete"), ("B", 15): _v("incomplete")}, VAL, cost=COST)
    sm6 = summarize_stage1({**all4, ("A", 15): None, ("B", 15): None}, VAL, cost=COST)
    chk(sm5["track"] == "pending" and sm6["track"] == "pending" and sm5["stage2"] is None,
        f"⛔음성 DG P1-5: 11–14 통과 · 15 미완 (또는 판정 없음) 이면 묶음은 통과가 아니라 대기 ({sm5['track']} · {sm6['track']})")
    sm7 = summarize_stage1({**ver, ("A", 13): _v("unknown")}, VAL, cost=COST)
    chk(sm7["track"] == "invalid" and bool(sm7["unknown_status"]), "⛔음성 DG P1-7: 판정 상태 'unknown' 은 통과 · 대기가 아니라 무효")
    closed = {**{k: None for k in ver}, ("A", 11): dict(_v("fail"), closes_system=True)}
    closed.update({("B", sd): _v("pass") for sd in (11, 12, 13, 14, 15)})
    closed.update({("A", sd): _v("pass") for sd in (12, 13, 14, 15)})
    sm8 = summarize_stage1(closed, VAL, cost=COST)
    chk(sm8["track"] == "stop_track" and sm8["per_system"]["A"]["status"] == "closed",
        "⛔음성 DG P0-1: A11 이 계를 닫으면 (첫 시드 녹음 미충족) 나머지 아홉이 통과해도 (A 4/5) 트랙 멈춤 — 일반 탈락과 다르다")
    sm9 = summarize_stage1(ver, VAL, cost={"total_h": 240.0, "cap_h": 230.0})
    sm10 = summarize_stage1(ver, VAL, cost=None)
    sm11 = summarize_stage1(ver, VAL, cost={"total_h": float("nan"), "cap_h": 230.0})
    chk(sm9["track"] == "cap_incomplete" and sm10["track"] == "pending" and sm11["track"] == "cap_incomplete" and not sm9["stage2"],
        f"⛔음성 DG P0-3: 비용 240 > 상한 230 → 미완결 · 장부 없음 → 대기 · 비유한 → 미완결 ({sm9['track']} · {sm10['track']} · {sm11['track']})")
    chk(validate_li2s2_values(VAL) == [] or [x for x in validate_li2s2_values(VAL) if "composition.T" not in x] == [],
        f"카드 값 검사: 시험 값은 통과 ({validate_li2s2_values(VAL)})")
    # 회신 DH P0-2 — 실행 식별: 자리 (계, 시드) ≠ 판정 · run_id 중복 · 장부 불완전 (invalid) · 장부 미확정 (pending)
    RID = lambda k: f"{k:032x}"
    vid = {(s_, sd): dict(_v("pass"), system=s_, seed=sd, run_id=RID(100 * (s_ == "A") + sd)) for s_ in ("A", "B") for sd in (11, 12, 13, 14, 15)}
    chk(summarize_stage1(vid, VAL, cost=COST)["track"] == "stage1_pass", "실행 식별이 다 맞으면 (자리 = 판정 · run_id 서로 다름) 통과")
    cp = dict(vid); cp[("A", 12)] = dict(vid[("A", 11)])
    sm_cp = summarize_stage1(cp, VAL, cost=COST)
    allc = {k: dict(vid[(k[0], 11)]) for k in vid}
    sm_all = summarize_stage1(allc, VAL, cost=COST)
    ed = dict(vid); ed[("A", 12)] = dict(vid[("A", 11)], seed=12)
    sm_ed = summarize_stage1(ed, VAL, cost=COST)
    chk(sm_cp["track"] == "invalid" and sm_all["track"] == "invalid" and sm_ed["track"] == "invalid" and bool(sm_cp["identity_problems"]),
        f"⛔음성 DH P0-2: A11 판정을 A12 자리에 · 모든 자리에 · 시드만 고쳐서 (run_id 같음) → 한 실행을 여러 시드로 못 센다 ({sm_cp['track']} · {sm_all['track']} · {sm_ed['track']})")
    swp = dict(vid); swp[("A", 12)], swp[("A", 13)] = vid[("A", 13)], vid[("A", 12)]
    chk(summarize_stage1(swp, VAL, cost=COST)["track"] == "invalid",
        "⛔음성 DH P0-2: A12 · A13 판정 파일이 서로 자리를 바꾸면 (run_id 는 각자 하나) 자리 ≠ 판정 이라 무효")
    sm_li = summarize_stage1(vid, VAL, cost=dict(COST, invalid=["A12 판정의 run_id 가 장부에 없다"]))
    sm_lp = summarize_stage1(vid, VAL, cost=dict(COST, pending=["A11 런이 끝나지 않았다"]))
    chk(sm_li["track"] == "invalid" and sm_lp["track"] == "pending",
        f"⛔음성 DH P0-1: 장부 불완전 (누락 · 음수 · 근거 없음) → 무효 · 비용 미확정 런 → 대기 ({sm_li['track']} · {sm_lp['track']})")
    with tempfile.TemporaryDirectory() as td_:
        rd_ = pathlib.Path(td_) / "A" / "seed12"; rd_.mkdir(parents=True)
        ic_ok = identity_check(rd_, {"system": "A", "seed": 12, "run_id": RID(5)})
        ic_cp = identity_check(rd_, {"system": "A", "seed": 11, "run_id": RID(5)})
        ic_no = identity_check(rd_, {"system": "A", "seed": 12})
        ic_bad = identity_check(pathlib.Path(td_) / "A" / "s12", {"system": "A", "seed": 12, "run_id": RID(5)})
    chk(ic_ok["ok"] and not ic_cp["ok"] and not ic_no["ok"] and not ic_bad["ok"],
        "⛔음성 DH P0-2: 폴더 seed12 에 plan 시드 11 → 무효 · run_id 없음 → 무효 · 폴더 이름 꼴 아님 → 무효 (맞으면 통과)")
    chk(combine_stage1(plan_ok, VAL, g_ok, m_ok, s_ok, f_ok, checks={"identity": ic_cp})["status"] == "invalid",
        "⛔음성 DH P0-2: 시드 판정이 실행 식별 불일치를 무효로")
    for nm_, mut in (("재시도 한도 -1", {"stage1_max_interrupt_retries_per_seed": -1}), ("재시도 한도 없음", {"stage1_max_interrupt_retries_per_seed": None}),
                     ("first_seed 12 (seeds[0] 아님)", {"first_seed": 12}), ("상한 NaN", {"stage1_cap_gpu_h": float("nan")}),
                     ("조성 합 ≠ n_atoms", {"composition": {"A": {"Li": 48}, "B": VAL["composition"]["B"]}}),
                     ("software_required 없음", {"software_required": None}), ("밀도 NaN", {"fix_density_g_cm3": {"A": float("nan"), "B": 1.88}}),
                     ("압력 열 목록에 virial 없음", {"thermo_required_columns": ["t_ps", "T_set_K", "density_g_cm3", "P_GPa"]})):
        chk(validate_li2s2_values({**VAL, **mut}) != [], f"⛔음성 DG: 카드 값 검사가 거부한다 — {nm_}")
    # 회신 DJ — 재시도 사유 · 실효 상한 · 증언 필드 (카드 값) · 완료 단계 · 판정 파일 상태 · 선언 검사 (드라이버 단위)
    for nm_, mut in (("retry_reasons 없음", {"retry_reasons": None}), ("retry_reasons 한 종류만", {"retry_reasons": {"interrupted": ["power_outage"]}}),
                     ("retry_reasons 빈 목록", {"retry_reasons": {"interrupted": [], "invalid": ["invalid_cause_fixed"]}}),
                     ("outage_reasons 가 interrupted 밖", {"outage_reasons": ["user_ctrl_c"]}), ("정전 추가 예산 NaN", {"stage1_outage_extra_budget_gpu_h": float("nan")}),
                     ("정전 추가 예산 -1", {"stage1_outage_extra_budget_gpu_h": -1.0}), ("정전 추가 예산 없음", {"stage1_outage_extra_budget_gpu_h": None}),
                     ("증언 필드에 확인자 없음", {"attestation_required_fields": ["event", "time_reference", "uncertainty_h", "derivation", "confirmed_at"]}),
                     ("상한 사유가 정전 사유와 겹침", {"cap_retry_reasons": ["power_outage"]}), ("상한 사유 없음", {"cap_retry_reasons": None})):
        chk(validate_li2s2_values({**VAL, **mut}) != [], f"⛔음성 DJ: 카드 값 검사가 거부한다 — {nm_}")
    with tempfile.TemporaryDirectory() as td_:
        def _fs(name, plan=True, traj=None, final=False):
            d = pathlib.Path(td_) / name; d.mkdir()
            if plan is True:
                (d / "plan.json").write_text(json.dumps({"melt_ps": 2.0, "quench_ps": 1.0, "hold_ps": 1.0, "save_ps": 1.0}), encoding="utf-8")
            elif isinstance(plan, str):
                (d / "plan.json").write_text(plan, encoding="utf-8")
            if traj is not None:
                (d / "traj.xyz").write_bytes(traj if isinstance(traj, bytes) else
                                             "".join("2\nLattice=\"5 0 0 0 5 0 0 0 5\"\nLi 0 0 0\nLi 1 1 1\n" for _ in range(traj)).encode())
            if final:
                (d / "final.xyz").write_text("x", encoding="utf-8")
            return folder_stage(d)
        fs_ = {"final": _fs("f", traj=5, final=True), "md_complete": _fs("c", traj=5), "md_incomplete": _fs("i", traj=4),
               "no_plan": _fs("n", plan=False, traj=5), "unreadable_plan": _fs("u", plan='{"melt_ps": 2', traj=5),
               "empty_traj": _fs("e", traj=b""), "nul_traj": _fs("z", traj=b"\x00" * 64), "garbage": _fs("g", traj=b"abc\n1\n"),
               "half_frame": _fs("h", traj=("2\nL\nLi 0 0 0\nLi 1 1 1\n" * 4 + "2\nL\nLi 0 0 0\n").encode())}
        chk(fs_ == {"final": "final", "md_complete": "md_complete", "md_incomplete": "md_incomplete", "no_plan": "no_plan",
                    "unreadable_plan": "unreadable", "empty_traj": "md_incomplete", "nul_traj": "md_incomplete", "garbage": "unreadable",
                    "half_frame": "md_incomplete"},
            f"⛔음성 DJ Q2: 완료 단계 — 최종 · MD 완료 (FIRE 미완) · MD 미완 · plan 없음 · plan 잘림 = 판독 불가 · 빈 / NUL traj = 프레임 0 · "
            f"머리 깨짐 = 판독 불가 · 끝의 반쪽 프레임은 안 센다 ({fs_})")
        vd = pathlib.Path(td_) / "v"; vd.mkdir()
        v_none = verdict_file_status(vd)
        (vd / "stage1_verdict.json").write_text('{"status": "pass"}', encoding="utf-8"); v_pass = verdict_file_status(vd)
        (vd / "stage1_verdict.json").write_text('{"status": "pa', encoding="utf-8"); v_cut = verdict_file_status(vd)
        (vd / "stage1_verdict.json").write_text('{"status": "maybe"}', encoding="utf-8"); v_unk = verdict_file_status(vd)
        (vd / "stage1_verdict.json").write_text('[1, 2]', encoding="utf-8"); v_list = verdict_file_status(vd)
    chk(v_none is None and v_pass == "pass" and v_cut == v_unk == v_list == "unreadable",
        f"⛔음성 DJ P0-2: 판정 파일 없음 (None) 과 있는데 못 읽음 (잘림 · 모르는 상태 · 객체 아님 = unreadable) 을 가른다 ({v_none} · {v_pass} · {v_cut} · {v_unk} · {v_list})")
    D_ = lambda **k: {"reason": "power_outage", "event": "kgy 정전 (selftest)", "evidence": "UPS 로그 (selftest)", "declared_by": "selftest",
                      "declared_at": "2026-11-03 00:00:00", **k}
    dp = {"none": declaration_problems(None, "interrupted", VAL), "ok": declaration_problems(D_(), "interrupted", VAL),
          "ctrl_c": declaration_problems(D_(reason="user_ctrl_c"), "interrupted", VAL),
          "inv_reason_for_int": declaration_problems(D_(reason="invalid_cause_fixed"), "interrupted", VAL),
          "inv_ok": declaration_problems(D_(reason="invalid_cause_fixed"), "invalid", VAL),
          "no_by": declaration_problems(D_(declared_by=" "), "interrupted", VAL),
          "rejudge_missing": declaration_problems(D_(reason="invalid_cause_fixed"), "invalid", VAL, rejudge_needed=True),
          "rejudge_ok": declaration_problems(D_(reason="invalid_cause_fixed", rejudge_impossible_reason="traj 0 번 프레임 종이 바뀜 (selftest)"),
                                             "invalid", VAL, rejudge_needed=True),
          "cap_outage": declaration_problems(D_(), "interrupted", VAL, prev_status="cap"),
          "cap_ok": declaration_problems(D_(reason="budget_cap_raised"), "interrupted", VAL, prev_status="cap"),
          "raise_noncap": declaration_problems(D_(reason="budget_cap_raised"), "interrupted", VAL, prev_status="interrupted")}
    chk(all(dp[k] for k in ("none", "ctrl_c", "inv_reason_for_int", "no_by", "rejudge_missing", "cap_outage", "raise_noncap"))
        and not any(dp[k] for k in ("ok", "inv_ok", "rejudge_ok", "cap_ok")),
        "⛔음성 DJ Q1 · Q4: 재시도 선언 — 없음 · 허용 밖 사유 (Ctrl-C) · 다른 종류 사유 · 선언자 없음 · 다시 판정 못 하는 이유 없음 · "
        "상한 런에 정전 사유 · 상한 아닌 런에 상한 사유 → 거부 (맞는 선언은 통과)")
    ack_ = lambda rid, reason, acked=True: {"stop_id": rid[:4], "run_id": rid, "code": "resume", **({"acked_at": "t"} if acked else {}),
                                            "declaration": D_(reason=reason)}
    runs_ = [{"system": "A", "seed": 12, "run_id": "1" * 32, "status": "orphaned", "end": "t", "wall_h": 30.0},
             {"system": "B", "seed": 12, "run_id": "2" * 32, "status": "ended", "rc": 0, "end": "t", "wall_h": 100.0},
             {"system": "A", "seed": 13, "run_id": "3" * 32, "status": "cap", "end": "t", "wall_h": 100.0},
             {"system": "B", "seed": 13, "run_id": "4" * 32, "status": "ended", "rc": 137, "end": "t", "wall_h": 100.0}]
    ec0 = effective_cap(runs_, [], VAL)[0]
    ec1 = effective_cap(runs_, [ack_("1" * 32, "power_outage")], VAL)[0]
    ec2 = effective_cap(runs_, [ack_("1" * 32, "power_outage"), ack_("4" * 32, "hardware_fault")], VAL)[0]
    ec3 = effective_cap(runs_, [ack_("2" * 32, "power_outage"), ack_("3" * 32, "power_outage")], VAL)[0]
    ec4 = effective_cap(runs_, [ack_("1" * 32, "power_outage", acked=False), ack_("1" * 32, "budget_cap_raised")], VAL)[0]
    with tempfile.TemporaryDirectory() as td_:
        dc, di = pathlib.Path(td_) / "c", pathlib.Path(td_) / "i"
        for d_, n_ in ((dc, 5), (di, 2)):
            d_.mkdir(); (d_ / "plan.json").write_text(json.dumps({"melt_ps": 2.0, "quench_ps": 1.0, "hold_ps": 1.0, "save_ps": 1.0}), encoding="utf-8")
            (d_ / "traj.xyz").write_text("".join("1\nL\nLi 0 0 0\n" for _ in range(n_)), encoding="utf-8")
        ec5 = effective_cap(runs_, [ack_("1" * 32, "power_outage")], VAL, inventory={"1" * 32: {"path": str(dc)}})[0]
        ec6 = effective_cap(runs_, [ack_("1" * 32, "power_outage")], VAL, inventory={"1" * 32: {"path": str(di)}})[0]
        ec7 = effective_cap(runs_, [ack_("1" * 32, "power_outage")], VAL, inventory={})[0]
    chk(ec0 == 230.0 and ec1 == 260.0 and ec2 == 275.0 and ec3 == 230.0 and ec4 == 230.0 and ec5 == 230.0 and ec6 == 260.0 and ec7 == 230.0,
        f"⛔음성 DJ Q4: 실효 상한 = 230 + min(정전 손실, 45) — 끊긴 런 30 h → 260 · 더 끊김 → 275 (45 상한) · 정상 끝 · 상한 런에 정전 선언 → 그대로 · "
        f"확인 안 된 선언 · 정전 아닌 사유 → 그대로 · 폴더가 MD 완료 · 없음 → 그대로 ({ec0} {ec1} {ec2} {ec3} {ec4} {ec5} {ec6} {ec7})")
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

    # ── NEB 끝점 게이트 (§0b-②-4) — UMA 없이 되는 부분만 ──────────────────
    #   ⛔ 이완 자체는 UMA 가 있어야 돌므로 여기서 안 친다. 대신 **판정 산수**와
    #     **문턱 판독**을 친다 — 조용히 틀릴 수 있는 곳이 거기다.
    th = read_neb_gate_thresholds("db/properties/lpscl_smallcell_neb_estimand_2026_09_18.json")
    chk(th == {"gate_A_li_min_A": 1.0, "gate_B_rmsd_max_A": 0.5},
        f"끝점 게이트 문턱을 **카드 산문에서** 읽는다 {th}")
    # ⛔음성 — 절이 없으면 **죽는다**. 기본값을 지어내지 않는다.
    import tempfile as _tf
    _bad = pathlib.Path(_tf.mkdtemp()) / "nocard.json"
    _bad.write_text('{"제목": "문턱 절이 없는 카드"}', encoding="utf-8")
    try:
        read_neb_gate_thresholds(str(_bad)); _died = False
    except KeyError:
        _died = True
    chk(_died, "⛔음성: 게이트 절이 없는 카드면 **죽는다** (기본값을 지어내지 않는다)")
    # ⛔음성 — 문구는 있는데 숫자가 없으면 죽는다
    _bad2 = pathlib.Path(_tf.mkdtemp()) / "nonum.json"
    _bad2.write_text(json.dumps({"0b_경로선택·집계_규칙_제안_2026_09_18": {"②_경로_선택_규칙": {
        "4_★_끝점_게이트_두_개_다_통과해야_후보다": {
            "게이트_A_서로_다른_최소": "두 위치 차가 충분히 크면 통과",
            "게이트_B_골격이_안_바뀜": "골격이 그대로면 통과"}}}}, ensure_ascii=False),
        encoding="utf-8")
    try:
        read_neb_gate_thresholds(str(_bad2)); _died2 = False
    except ValueError:
        _died2 = True
    chk(_died2, "⛔음성: 산문에 숫자가 없으면 **죽는다** (문구만 보고 통과시키지 않는다)")

    # mic_dist — 셀 경계를 넘는 짝
    _c = np.eye(3) * 10.0
    chk(abs(mic_dist([0.5, 0, 0], [9.5, 0, 0], _c) - 1.0) < 1e-9,
        "mic_dist: 경계를 넘는 짝을 **1.0 Å** 로 본다 (9.0 이 아니다)")

    # non_li_rmsd — Li 를 **빼고** 잰다
    from ase import Atoms as _A
    _s = ["Li", "Li", "P", "S"]
    _p0 = np.array([[0, 0, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0]], float)
    _p1 = _p0.copy(); _p1[0, 0] += 5.0                       # Li 만 크게 움직인다
    r, n, dm = non_li_rmsd(_A(_s, positions=_p0, cell=_c, pbc=True),
                           _A(_s, positions=_p1, cell=_c, pbc=True))
    chk(abs(r) < 1e-9 and n == 2,
        f"⛔음성: Li 가 5 Å 움직여도 골격 RMSD 는 **0** 이다 (n_framework={n}, rmsd={r:.4f})")
    _p2 = _p0.copy(); _p2[3, 0] += 1.0                       # S 가 움직인다
    r2, _, _ = non_li_rmsd(_A(_s, positions=_p0, cell=_c, pbc=True),
                           _A(_s, positions=_p2, cell=_c, pbc=True))
    chk(abs(r2 - (1.0 / np.sqrt(2))) < 1e-9,
        f"골격 원자 하나가 1 Å 움직이면 RMSD = 1/√2 = {r2:.4f} (2 원자 중 하나)")

    # ── endpoint_gate **본문**을 탄다 (UMA 대신 stub 계산기) ─────────────
    #   ⛔ 2026-09-18 실측: 위 시험들은 헬퍼만 불렀고 함수 본문은 한 번도 안 탔다.
    #     그래서 본문의 `_today()` NameError 가 **kgy 에서 9 건을 다 돌린 뒤에야**
    #     JSON 쓰기 직전에 터졌다. 이 파일이 같은 실패(함수만 시험, 배선은 안 탐)를
    #     겪은 세 번째다. stub 계산기로 전 경로를 태운다.
    from ase import Atoms as _A2
    from ase.calculators.lj import LennardJones as _LJ
    _td = pathlib.Path(_tf.mkdtemp()) / "events"; _td.mkdir(parents=True)
    _cell = np.eye(3) * 12.0
    _sym2 = ["Li", "Li", "P", "S", "S", "Cl"]
    _base = np.array([[1, 1, 1], [5, 1, 1], [3, 3, 3], [3, 5, 3], [5, 3, 3], [8, 8, 8]], float)
    _evs = []
    for k, (ai, dx) in enumerate([(0, 2.0), (1, 0.2)], 1):
        tag = f"ev{k:02d}_atom{ai}"
        for side, shift in (("i", 0.0), ("f", dx)):
            q = _base.copy(); q[ai, 0] += shift
            _A2(_sym2, positions=q, cell=_cell, pbc=True).write(str(_td / f"{tag}_{side}.xyz"))
        _evs.append({"tag": tag, "atom_index": ai, "disp_A": dx,
                     "t_start_ps": 0.0, "t_end_ps": 5.0})
    (_td / "events.json").write_text(json.dumps({"events": _evs}, ensure_ascii=False),
                                     encoding="utf-8")
    _real_make_calc = make_calc
    try:
        globals()["make_calc"] = lambda turbo=False, device="cuda": _LJ(epsilon=0.01, sigma=2.5)
        _r = endpoint_gate(str(_td), out_json=str(_td / "g.json"),
                           card="db/properties/lpscl_smallcell_neb_estimand_2026_09_18.json",
                           steps=2, log=lambda *a, **k: None)
    finally:
        globals()["make_calc"] = _real_make_calc
    chk(_r["n_events"] == 2, f"[배선] endpoint_gate 본문이 끝까지 돈다 (사건 {_r.get('n_events')})")
    chk((_td / "g.json").exists(), "[배선] 결과 JSON 을 **쓴다** (여기서 _today() NameError 가 났었다)")
    _need = {"date", "kind", "⛔_gate_engine", "thresholds", "rows",
             "provisional_n_survive", "provisional_reject_rate", "⇒_§0b_②_5"}
    chk(_need <= set(_r), f"[배선] 결과에 필수 키가 다 있다 (빠진 것: {_need - set(_r)})")
    chk("게이트를 **집행하지 않는다**" in _r["⛔_gate_engine"],
        "⛔음성: 결과가 스스로 **비준된 게이트가 아님**을 말한다")
    _rows = {r["tag"]: r for r in _r["rows"]}
    chk(_rows["ev01_atom0"]["li_sep_after_relax_A"] > _rows["ev02_atom1"]["li_sep_after_relax_A"],
        "[배선] 많이 움직인 쪽이 이완 후에도 더 벌어져 있다 (자리를 안 뒤바꾼다)")
    chk(all(isinstance(r["rejected_because"], list) for r in _r["rows"]),
        "기각 사유를 사건마다 **적는다** (빈 리스트라도 자리가 있다)")
    # ⓑ 카드 §2 가 요구하는 원시량 — 전에는 판정만 하고 **버렸다**
    _r0 = _r["rows"][0]
    chk({"E_i_eV", "E_f_eV", "dE_f_minus_i_eV"} <= set(_r0),
        f"[배선] 끝점 에너지 E_i·E_f·ΔE 를 남긴다 (ⓑ 카드 §2 원시량)")
    chk(abs(_r0["dE_f_minus_i_eV"] - (_r0["E_f_eV"] - _r0["E_i_eV"])) < 1e-6,
        "ΔE 가 E_f − E_i 와 일치한다 (부호를 뒤집지 않는다)")
    _rx = [_td / x for x in _r0["relaxed_xyz"]]
    chk(all(q.exists() for q in _rx),
        f"[배선] **이완된** 끝점 구조를 파일로 남긴다 (NEB 출발점이다)")
    # ⛔음성 — 저장된 것이 이완 **전** 구조면 안 된다
    from ase.io import read as _rd
    _a_raw = _rd(str(_td / f"{_r0['tag']}_i.xyz"))
    _a_rel = _rd(str(_rx[0]))
    chk(np.abs(_a_raw.get_positions() - _a_rel.get_positions()).max() > 1e-6,
        "⛔음성: 저장된 것이 **이완 후** 구조다 (원본을 그대로 복사하지 않는다)")

    # ── --seed_gate: 원시(traj 마지막 프레임)·relax 본(final.xyz) 두 판 (2026-09-24) ──
    import tempfile as _tf
    from ase import Atoms as _At
    from ase.io import write as _wsg, read as _rsg
    _q = lambda *a, **k: None
    _sym, _pos, _cell = build_random_cell("A", seed=3, n_fu=4)
    _rng = np.random.default_rng(7)
    _frames = [_At(_sym, positions=_pos + _rng.normal(0, 0.05, _pos.shape), cell=_cell, pbc=True) for _ in range(3)]
    _frames[-1].positions[0] += _cell[0]        # 원시 NPT 궤적처럼 셀 밖 좌표 — 뽑을 때 감겨야 한다
    _plan = {"melt_ps": 1.0, "quench_ps": 0.0, "hold_ps": 1.0, "save_ps": 1.0,
             "게이트_입력": {"final_relax": FINAL_RELAX}}

    def _mk_sg(name, traj=True, final="relaxed", plan=_plan):
        d = pathlib.Path(_tf.mkdtemp()) / "A" / name
        d.mkdir(parents=True)
        if traj:
            for f in _frames:
                _wsg(str(d / "traj.xyz"), f, format="extxyz", append=True)
        fin = _frames[-1].copy()
        if final == "relaxed":
            fin.positions += np.random.default_rng(11).normal(0, 0.03, _pos.shape)
        _wsg(str(d / "final.xyz"), fin, format="extxyz")
        (d / "plan.json").write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        return d

    _d1 = _mk_sg("seed9")
    _g1 = seed_gate(_d1, log=_q)
    chk(bool(_g1["raw"]) and bool(_g1["relaxed"]), "--seed_gate: 원시·relax 두 판을 다 찍는다")
    chk(_g1["raw"]["frame"] == 2 and _g1["raw"]["t_ps"] == 2.0 and not _g1["warnings"],
        "--seed_gate: 원시 = traj **마지막** 프레임 (프레임 2 · t 2 ps · 길이 plan 과 일치)")
    chk(_g1["raw_vs_relaxed"]["disp_max_A"] > 1e-3,
        "⛔음성: relax 본과 원시를 **구분**한다 (변위 > 0 — final.xyz 를 원시로 읽으면 0 이 된다)")
    _rf = _rsg(str(_d1 / SEED_GATE_RAW))
    _dd = (_rf.get_positions() - _frames[-1].get_positions()) @ np.linalg.inv(_cell)
    _sp = _rf.get_scaled_positions(wrap=False)
    chk(np.linalg.norm((_dd - np.round(_dd)) @ _cell, axis=1).max() < 1e-6
        and _sp.min() > -1e-9 and _sp.max() < 1 + 1e-9,
        "--seed_gate: md_init_raw.xyz = 원시 마지막 프레임 (최소상 동일 · 셀 안으로 감김)")
    chk(bool(_rf.info.get("raw")) and int(_rf.info.get("frame")) == 2,
        "--seed_gate: md_init_raw.xyz 가 출처(원시 · 프레임 번호)를 달고 있다")
    chk(_g1["raw"]["min_pair_excl_PS_kind"] != "P-S",
        "--seed_gate: '최단·P–S 제외' 에 P–S 쌍이 안 들어간다")
    _g1b = seed_gate(_d1, log=_q)
    chk(_g1b["md_init_raw"]["status"] == "이미 있음 · 같음",
        "--seed_gate: 다시 돌려도 같은 원시면 그대로 둔다 (멱등)")
    _d2 = _mk_sg("seed8", traj=False)
    _g2 = seed_gate(_d2, log=_q)
    chk(_g2["raw"] is None and "대신하지 않는다" in _g2.get("raw_why", "") and not (_d2 / SEED_GATE_RAW).exists(),
        "⛔음성: traj 가 없으면 원시 칸을 비운다 — final.xyz 를 원시로 쓰지도, md_init_raw.xyz 를 만들지도 않는다")
    _g3 = seed_gate(_mk_sg("seed7", final="same"), log=_q)
    chk(any("원시와 같다" in w for w in _g3["warnings"]),
        "⛔음성: final.xyz 가 원시와 똑같으면 경보한다 (relax 본이어야 할 파일)")
    _g4 = seed_gate(_mk_sg("seed6", plan=dict(_plan, hold_ps=8.0)), log=_q)
    chk(any("잘렸다" in w for w in _g4["warnings"]),
        "⛔음성: traj 가 plan 길이보다 짧으면 경보한다 (마지막 프레임 ≠ 유지 끝)")
    _bad = _rf.copy()
    _bad.positions[0] += 0.5
    _wsg(str(_d1 / SEED_GATE_RAW), _bad, format="extxyz")
    try:
        seed_gate(_d1, log=_q)
        _ok_ow = False
    except SystemExit as e:
        _ok_ow = "덮어쓰지 않는다" in str(e)
    chk(_ok_ow, "⛔음성: 이미 있는 md_init_raw.xyz 가 다르면 덮어쓰지 않고 멈춘다")

    # ── 모델 검증 경로 (--eos_path) — 가짜 계산기 (LJ) 로 배선만 본다 (UMA 아님) ──
    import tempfile as _tf
    from ase import Atoms as _At
    from ase.calculators.lj import LennardJones as _LJ
    chk(eos_label("x/A/seed3/final.xyz") == "A_s3" and eos_label("y/B/seed12/final.xyz") == "B_s12",
        "--eos_path: 경로에서 라벨 (A_s3 · B_s12)")
    try:
        eos_label("x/C/seed3/final.xyz"); _ok_l = False
    except SystemExit:
        _ok_l = True
    chk(_ok_l, "⛔음성: <A|B>/seed<N> 꼴이 아니면 라벨을 추측하지 않고 멈춘다")
    _mv, _ = read_mc_values()
    with _tf.TemporaryDirectory() as _td:
        _td = pathlib.Path(_td)
        _sd = _td / "B" / "seed9"; _sd.mkdir(parents=True)
        _at = _At("PS4LiCl", positions=[[4, 4, 4], [5.2, 5.2, 5.2], [2.8, 2.8, 5.2], [2.8, 5.2, 2.8], [5.2, 2.8, 2.8],
                                        [1.0, 1.0, 1.0], [6.8, 1.2, 6.8]], cell=[8.0, 8.0, 8.0], pbc=True)
        from ase.io import write as _w
        _w(str(_sd / "final.xyz"), _at, format="extxyz")
        _lj = _LJ(sigma=2.0, epsilon=0.01, rc=5.0); _lj._mq_mode = "default"
        _q = lambda *a, **k: None
        _r = eos_path([_sd / "final.xyz"], _td / "out", calc=_lj, log=_q)["B_s9"]
        _xs = [p["x"] for p in _r["points"]]
        chk(_xs == sorted(float(x) for x in _mv["path_scales"]), f"--eos_path: 카드 격자 그대로 {_xs}")
        _V0 = _r["meta"]["V_final_A3"]
        chk(all(abs(p["V_A3"] / _V0 - p["x"]) < 1e-9 for p in _r["points"]), "--eos_path: 점마다 V/V_final = x (등방 스케일)")
        chk(all(p["converged"] and p["Fmax_eV_A"] <= float(_mv["relax_fmax_eV_A"]) + 1e-12 for p in _r["points"]),
            "--eos_path: 점마다 카드 fmax 로 수렴")
        chk(_r["meta"]["mode"] == "default" and _r["meta"]["relax"]["cell"] == "fixed", "--eos_path: 모드 default · 고정셀 기록")
        chk(all((_td / "out" / "B_s9" / p["geom"]).is_file() for p in _r["points"]), "--eos_path: 점마다 기하 파일")
        _logs = []
        eos_path([_sd / "final.xyz"], _td / "out", calc=_lj, log=lambda m: _logs.append(m))
        chk(len(_logs) == len(_xs) and all("이미 있음" in m for m in _logs), "--eos_path: 다시 부르면 다 건너뛴다 (재개)")
        _lj2 = _LJ(sigma=2.0, epsilon=0.01, rc=5.0); _lj2._mq_mode = "turbo"
        try:
            eos_path([_sd / "final.xyz"], _td / "out2", calc=_lj2, log=_q); _ok_t = False
        except SystemExit:
            _ok_t = True
        chk(_ok_t, "⛔음성: turbo 계산기면 멈춘다 (카드 default)")
        _at.positions[0] += 0.3
        _w(str(_sd / "final.xyz"), _at, format="extxyz")
        try:
            eos_path([_sd / "final.xyz"], _td / "out", calc=_lj, log=_q); _ok_s = False
        except SystemExit:
            _ok_s = True
        chk(_ok_s, "⛔음성: 입력 sha 가 바뀐 구조를 옛 경로 json 에 섞지 않고 멈춘다")
        (_td / "c.json").write_text(json.dumps({"x": 1}), encoding="utf-8")
        try:
            read_mc_values(str(_td / "c.json")); _ok_c = False
        except KeyError:
            _ok_c = True
        chk(_ok_c, "⛔음성: 기계_판독_값 없는 카드 → KeyError")

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
    ap.add_argument("--run_id", default=None,
                    help="⭐li2s-2: 러너가 담금질마다 주는 실행 식별자 (32 hex · plan.json run_id · 장부 run_id 와 묶는다 — 회신 DH P0-2)")
    ap.add_argument("--fix_density", type=float, default=None,
                    help="⭐li2s-2: 담금질을 NVT 로 — melt 첫 --compress_ps 동안 이 밀도 [g/cm³] 로 압축한 뒤 고정 "
                         "(같은 Berendsen 열욕 · 바로스탯 없음). 안 주면 옛 NPT 0 GPa 그대로")
    ap.add_argument("--compress_ps", type=float, default=20.0, help="--fix_density 압축 구간 [ps] (melt 안 · 기본 20)")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--turbo", action="store_true", help="fairchem inference_settings='turbo' 시도 (없으면 기본으로 내려가고 기록)")
    ap.add_argument("--out_root", help="출력 루트 → <out_root>/<system>/seed<seed>/")
    ap.add_argument("--pcheck", nargs="+", metavar="STRUCT",
                    help="⭐구조 파일들의 **단일점 압력**을 UMA 로 찍는다 (완화 없음). "
                         "고정 셀 MD 가 어떤 내부 압력에서 돌고 있는지 보는 용도")
    ap.add_argument("--melt_window_check", metavar="RUN_DIR",
                    help="⭐li2s-2 녹음 판정 (회신 DF P0) — 압축 뒤 창 안 프레임 · 창 안 시간원점만 · 카드 문턱. 종료 0 통과 · 2 미충족 · 3 미완 · 4 무효")
    ap.add_argument("--stage1_verdict", nargs="+", metavar="RUN_DIR",
                    help="⭐li2s-2 1 단계 시드 판정 (일정 완주 · 유지 구간 · 압력 기록 · 밀도 · 녹음 · 시드 게이트 · 카드 일정) → stage1_verdict.json")
    ap.add_argument("--stage1_summary", metavar="OUT_ROOT",
                    help="⭐li2s-2 1 단계 묶음 판정 (판정 지문 다시 잼 · 선언 시드 전부 판정 끝 · 첫 시드 녹음 미충족 = 그 계 닫힘 · "
                         "한쪽 탈락 = 트랙 멈춤 · 비용 장부 > 상한 = 미완결 · 2 단계 시드 = 공통 통과 중 작은 둘). "
                         "종료 0 통과 · 2 멈춤 · 3 대기 · 4 무효 · 5 상한 미완결")
    ap.add_argument("--li2s2_card", default=LI2S2_CARD, help="li2s-2 카드 (기계_판독_값 출처 — 도구가 문턱을 자체 보관하지 않는다)")
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
    ap.add_argument("--seed_gate", nargs="+", metavar="RUN_DIR",
                    help="시드 게이트 입력(PS₄·다리 S·P–P·최단 원자간·밀도)을 **원시(traj 마지막 프레임)·relax 본"
                         "(final.xyz)** 두 판으로 찍고, 원시 판을 md_init_raw.xyz 로 떨군다 (판정 안 함 · seed_gate.json)")
    ap.add_argument("--no_write_raw", action="store_true",
                    help="--seed_gate 에서 md_init_raw.xyz 를 쓰지 않는다 (읽기만)")
    ap.add_argument("--band_card", default=BAND_CARD, help="--gate_check G4 밴드 출처 카드")
    ap.add_argument("--gate_win_ps", type=float, default=10.0, help="--gate_check 평균 창 [ps]")
    ap.add_argument("--mode_stress", metavar="RUN_DIR",
                    help="⭐봉인된 프레임에서 turbo − default 의 응력·힘 차이 (새 MD 0, 회신 BR Q4)")
    ap.add_argument("--frame_card", default="db/properties/li2s_layer1_g2_mode_stress_prereg_2026_09_14.json",
                    help="--mode_stress 프레임 표본 카드 (도구가 프레임을 고르지 않는다)")
    ap.add_argument("--eos_path", nargs="+", metavar="STRUCT",
                    help="모델 검증 카드 §1b — …/<A|B>/seed<N>/final.xyz 마다 등방 경로 UMA default 고정셀 이완 (--eos_out 필요)")
    ap.add_argument("--eos_out", help="--eos_path 출력 루트 → <eos_out>/<A_sN>/uma_path.json · x<..>.xyz")
    ap.add_argument("--eos_which", choices=("main", "ext_low", "ext_high"), default="main",
                    help="--eos_path 격자: 카드 path_scales (기본) · 연장 점 (판독 도구가 연장 규칙을 말할 때만)")
    ap.add_argument("--gb2", nargs=2, metavar=("RUN_SMALL", "RUN_BIG"),
                    help="G-B2 겹침 — 소셀 런디렉터리와 400 원자 런디렉터리. 새 계산 0")
    ap.add_argument("--gb2_card", default=GB2_CARD,
                    help="--gb2 문턱 출처 카드 (도구가 문턱을 자체 보관하지 않는다)")
    ap.add_argument("--gb2_out", help="--gb2 결과 JSON 경로 (기본 <RUN_SMALL>/gb2_overlap.json)")
    ap.add_argument("--endpoint_gate", metavar="EVENTS_DIR",
                    help="NEB 끝점 게이트 A/B **UMA 탐침** (카드 §0b-②-4). "
                         "⛔ 비준된 게이트(QE)를 집행하지 않는다 — 기각률을 먼저 본다")
    ap.add_argument("--endpoint_gate_out", help="--endpoint_gate 결과 JSON 경로")
    ap.add_argument("--neb_card", default=NEB_CARD,
                    help="--endpoint_gate 문턱 출처 카드 (도구가 문턱을 자체 보관하지 않는다)")
    ap.add_argument("--hold_blocks", type=int, default=5,
                    help="--gate_check 유지 구간을 몇 블록으로 나눠 추세를 볼지 (회신 BR Q3: 제일 싼 첫 단계)")
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if a.eos_path:
        if not a.eos_out:
            raise SystemExit("⛔ --eos_path 는 --eos_out 이 필요하다")
        for s in a.eos_path:
            if not pathlib.Path(s).is_file():
                raise SystemExit(f"⛔ 구조 파일이 없다: {s}")
        r = eos_path(a.eos_path, a.eos_out, which=a.eos_which, device=a.device, log=_flushing_print)
        n_bad = sum(1 for J in r.values() for p in J["points"] if not p["converged"])
        print(f"■ 끝 — 구조 {len(r)} · 점 {sum(len(J['points']) for J in r.values())} · 미수렴 {n_bad}")
        raise SystemExit(0 if n_bad == 0 else 2)
    if a.endpoint_gate:
        r = endpoint_gate(a.endpoint_gate,
                          out_json=a.endpoint_gate_out or
                          str(pathlib.Path(a.endpoint_gate).parent / "endpoint_gate_uma.json"),
                          card=a.neb_card, device=a.device, turbo=a.turbo)
        raise SystemExit(0 if r["n_events"] else 3)
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
        raise SystemExit(0 if (r["record_has_gate_input"] and r["gate_ok"]) else 2)
    if a.seed_gate:
        rows = []
        for rd in a.seed_gate:
            r = seed_gate(rd, write_raw=not a.no_write_raw)
            (pathlib.Path(rd) / "seed_gate.json").write_text(json.dumps(r, ensure_ascii=False, indent=1),
                                                             encoding="utf-8")
            rows.append(r)
            print()
        print("⛔ 판정하지 않았다 — 게이트를 원시·relax 어느 판으로 잴지, 문턱이 무엇인지는 카드·사람 몫이다.")
        #: 0 = 두 판 다 찍음 · 2 = 한 판이라도 비었음 (**비었음을 통과로 내보내지 않는다**)
        raise SystemExit(0 if all(x["raw"] and x["relaxed"] for x in rows) else 2)
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
    if a.melt_window_check:
        res = melt_window_check(a.melt_window_check, card=a.li2s2_card)
        (pathlib.Path(a.melt_window_check) / "melt_window_check.json").write_text(
            json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        raise SystemExit({"pass": 0, "fail": 2, "incomplete": 3}.get(res["verdict"], 4))
    if a.stage1_verdict:
        rcs = [STAGE1_RC.get(stage1_verdict(rd, card=a.li2s2_card)["status"], 4) for rd in a.stage1_verdict]
        raise SystemExit(max(rcs))
    if a.stage1_summary:
        res = stage1_summary(a.stage1_summary, card=a.li2s2_card)
        raise SystemExit(SUMMARY_RC.get(res["track"], 4))
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
    validate_fix_density(a.fix_density, a.compress_ps, a.melt_ps)
    sym, pos, cell = build_random_cell(a.system, a.seed, a.density, a.n_fu)
    out = pathlib.Path(a.out_root) / a.system / f"seed{a.seed}"; out.mkdir(parents=True, exist_ok=True)
    plan = build_plan(a.system, a.seed, sym, a.density, a.T_melt, a.T_final, a.melt_ps,
                      a.quench_rate, quench_ps, a.hold_ps, a.dt_fs, a.save_ps,
                      fix_density=a.fix_density, compress_ps=a.compress_ps)
    if a.run_id is not None and not RUN_ID_RE.match(a.run_id):
        raise SystemExit(f"⛔ --run_id {a.run_id!r} 는 32 자리 소문자 hex 여야 한다 (러너가 준다)")
    plan["run_id"] = a.run_id
    (out / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1))
    from ase import Atoms
    from ase.io import write
    at = Atoms(symbols=sym, positions=pos, cell=cell, pbc=True)
    write(str(out / "initial.xyz"), at, format="extxyz")
    print(f"[{a.system} seed{a.seed}] {len(sym)} 원자 · 셀 {cell[0,0]:.2f} Å · 담금질 {quench_ps:.0f} ps ({n_q} 스텝) → {out}", flush=True)
    print(("  앙상블: NPT Berendsen 0 GPa (옛 경로)" if a.fix_density is None else
           f"  앙상블: NVT 고정 밀도 {a.fix_density:.5f} g/cm³ (melt 첫 {a.compress_ps:g} ps 동안 압축 · 같은 열욕)"), flush=True)
    if a.dry_run:
        print("dry_run — 여기서 멈춘다"); return
    calc = make_calc(a.device, a.turbo)
    plan["uma_inference_mode"] = getattr(calc, "_mq_mode", "default")
    plan["software"] = software_versions(plan["uma_inference_mode"])   # 회신 DF Q-DF-6 — 판 · 모델 · 추론 설정을 기록
    (out / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1))
    print(f"UMA inference mode: {plan['uma_inference_mode']}", flush=True)
    info = run_melt_quench(at, calc, out, seed=a.seed, T_melt=a.T_melt, T_final=a.T_final, melt_ps=a.melt_ps,
                           quench_rate=a.quench_rate, hold_ps=a.hold_ps, dt_fs=a.dt_fs, save_ps=a.save_ps,
                           fix_density=a.fix_density, compress_ps=a.compress_ps)
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
